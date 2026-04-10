---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/define-outcomes
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 65f75ad1d4ed1bfa39fc9a1ff5cdd4ad123bbac921cc350207a771d7f5fef793
---

# Tentukan hasil

Beri tahu agen seperti apa 'selesai' itu, dan biarkan ia beriterasi hingga mencapainya.

---

<Tip>
Outcomes adalah fitur Research Preview. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Tip>

`outcome` meningkatkan sesi dari *percakapan* menjadi *pekerjaan*. Anda mendefinisikan seperti apa hasil akhirnya dan bagaimana mengukur kualitasnya. Agen bekerja menuju target tersebut, mengevaluasi diri sendiri dan beriterasi hingga hasil tercapai.

Ketika Anda mendefinisikan sebuah outcome, harness secara otomatis menyediakan *grader* untuk mengevaluasi artefak terhadap rubrik. Ini memanfaatkan jendela konteks terpisah untuk menghindari pengaruh dari pilihan implementasi agen utama.

Grader mengembalikan rincian per-kriteria: baik konfirmasi bahwa artefak memenuhi rubrik, atau kesenjangan spesifik antara pekerjaan saat ini dan persyaratan. Umpan balik tersebut diberikan kembali kepada agen untuk iterasi berikutnya.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. Fitur research preview juga memerlukan `managed-agents-2026-04-01-research-preview`. SDK menetapkan header beta ini secara otomatis.
</Note>

## Buat rubrik

Rubrik adalah dokumen markdown yang mendeskripsikan penilaian per-kriteria. Rubrik wajib ada.

<section title="Tips untuk menulis rubrik yang efektif">

Susun rubrik sebagai kriteria yang eksplisit dan dapat dinilai, seperti "CSV berisi kolom harga dengan nilai numerik" daripada "Data terlihat bagus." Grader menilai setiap kriteria secara independen, sehingga kriteria yang samar menghasilkan evaluasi yang tidak akurat.

Jika Anda tidak memiliki rubrik yang siap, coba berikan Claude contoh artefak yang diketahui baik dan minta untuk menganalisis apa yang membuat konten tersebut baik, lalu ubah analisis tersebut menjadi rubrik. Pendekatan jalan tengah ini sering menghasilkan hasil yang lebih baik daripada menulis kriteria dari awal.

</section>

Contoh rubrik:

```markdown
# DCF Model Rubric

## Revenue Projections
- Uses historical revenue data from the last 5 fiscal years
- Projects revenue for at least 5 years forward
- Growth rate assumptions are explicitly stated and reasonable

## Cost Structure
- COGS and operating expenses are modeled separately
- Margins are consistent with historical trends or deviations are justified

## Discount Rate
- WACC is calculated with stated assumptions for cost of equity and cost of debt
- Beta, risk-free rate, and equity risk premium are sourced or justified

## Terminal Value
- Uses either perpetuity growth or exit multiple method (stated which)
- Terminal growth rate does not exceed long-term GDP growth

## Output Quality
- All figures are in a single .xlsx file with clearly labeled sheets
- Key assumptions are on a separate "Assumptions" sheet
- Sensitivity analysis on WACC and terminal growth rate is included
```

Berikan rubrik sebagai teks inline pada `user.define_outcome` (ditampilkan di bagian berikutnya), atau unggah melalui Files API untuk digunakan kembali di berbagai sesi:

**Memerlukan header beta `files-api-2025-04-14`.**

<CodeGroup>
  
  ```bash curl
  rubric=$(curl -fsSL https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14" \
    -F file=@/path/to/pr_review_rubric.md)
  rubric_id=$(jq -r '.id' <<<"$rubric")
  printf 'Uploaded rubric: %s\n' "$rubric_id"
  ```
  
  ```bash CLI
  RUBRIC_ID=$(ant beta:files upload \
    --file /path/to/pr_review_rubric.md \
    --transform id --format yaml)
  ```
  ```python Python
  from pathlib import Path

  rubric = client.beta.files.upload(file=Path("/path/to/pr_review_rubric.md"))
  print(f"Uploaded rubric: {rubric.id}")
  ```
  ```typescript TypeScript
  import { readFile } from "node:fs/promises";
  import { toFile } from "@anthropic-ai/sdk";

  const rubric = await client.beta.files.upload({
    file: await toFile(readFile("/path/to/pr_review_rubric.md"), "pr_review_rubric.md")
  });
  console.log(`Uploaded rubric: ${rubric.id}`);
  ```
  ```csharp C#
  var rubric = await client.Beta.Files.Upload(new()
  {
      File = File.OpenRead("/path/to/pr_review_rubric.md"),
  });
  Console.WriteLine($"Uploaded rubric: {rubric.ID}");
  ```
  ```go Go
  f, err := os.Open("/path/to/pr_review_rubric.md")
  if err != nil {
  	panic(err)
  }

  rubric, err := client.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
  	File: anthropic.File(f, "pr_review_rubric.md", "text/markdown"),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Uploaded rubric: %s\n", rubric.ID)
  ```
  ```java Java
  var rubric = client.beta().files().upload(
      FileUploadParams.builder()
          .file(Path.of("/path/to/pr_review_rubric.md"))
          .build()
  );
  IO.println("Uploaded rubric: " + rubric.id());
  ```
  ```php PHP
  $rubric = $client->beta->files->upload(
      file: fopen('/path/to/pr_review_rubric.md', 'r'),
  );
  echo "Uploaded rubric: {$rubric->id}\n";
  ```
  ```ruby Ruby
  require "pathname"

  rubric = client.beta.files.upload(file: Pathname.new("/path/to/pr_review_rubric.md"))
  puts "Uploaded rubric: #{rubric.id}"
  ```
</CodeGroup>

## Buat sesi dengan outcome

Setelah membuat sesi, kirim event `user.define_outcome`. Agen mulai bekerja segera; tidak diperlukan event pesan pengguna tambahan.

<CodeGroup>
  
  ```bash curl
  # Create a session
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01-research-preview" \
    --json @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "title": "Financial analysis on Costco"
  }
  EOF
  )
  session_id=$(jq -r '.id' <<<"$session")

  # Define the outcome — agent starts working on receipt
  curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01-research-preview" \
    --json @- >/dev/null <<EOF
  {
    "events": [
      {
        "type": "user.define_outcome",
        "description": "Build a DCF model for Costco in .xlsx",
        "rubric": {"type": "text", "content": "# DCF Model Rubric\n..."},
        "max_iterations": 5
      }
    ]
  }
  EOF
  # or: "rubric": {"type": "file", "file_id": "$rubric_id"}
  # "max_iterations" is optional; default 3, max 20
  ```
  
  ```bash CLI
  # Create a session
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment "$ENVIRONMENT_ID" \
    --title "Financial analysis on Costco" \
    --transform id --format yaml)

  # Define the outcome — agent starts working on receipt
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" <<YAML
  events:
    - type: user.define_outcome
      description: Build a DCF model for Costco in .xlsx
      rubric: {type: file, file_id: $RUBRIC_ID}
      # or: rubric: {type: text, content: "..."}
      max_iterations: 5  # optional; default 3, max 20
  YAML
  ```
  ```python Python
  # Create a session
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      title="Financial analysis on Costco",
  )

  # Define the outcome — agent starts working on receipt
  client.beta.sessions.events.send(
      session_id=session.id,
      events=[
          {
              "type": "user.define_outcome",
              "description": "Build a DCF model for Costco in .xlsx",
              "rubric": {"type": "text", "content": RUBRIC},
              # or: "rubric": {"type": "file", "file_id": rubric.id},
              "max_iterations": 5,  # optional; default 3, max 20
          }
      ],
  )
  ```
  ```typescript TypeScript
  // Create a session
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    title: "Financial analysis on Costco"
  });

  // Define the outcome — agent starts working on receipt
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.define_outcome",
        description: "Build a DCF model for Costco in .xlsx",
        rubric: { type: "text", content: RUBRIC },
        // or: rubric: { type: "file", file_id: rubric.id },
        max_iterations: 5 // optional; default 3, max 20
      }
    ]
  });
  ```
  ```csharp C#
  // Create a session
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Title = "Financial analysis on Costco",
  });

  // Define the outcome — agent starts working on receipt
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserDefineOutcomeEventParams
          {
              Type = "user.define_outcome",
              Description = "Build a DCF model for Costco in .xlsx",
              Rubric = new BetaManagedAgentsTextRubricParams { Type = "text", Content = Rubric },
              // or: Rubric = new BetaManagedAgentsFileRubricParams { Type = "file", FileID = rubric.id },
              MaxIterations = 5,  // optional; default 3, max 20
          },
      ],
  });
  ```
  ```go Go
  	// Create a session
  	session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  		Agent: anthropic.BetaSessionNewParamsAgentUnion{
  			OfString: anthropic.String(agent.ID),
  		},
  		EnvironmentID: environment.ID,
  		Title:         anthropic.String("Financial analysis on Costco"),
  	})
  	if err != nil {
  		panic(err)
  	}

  	// Define the outcome — agent starts working on receipt
  	_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.SendEventsParamsUnion{{
  			OfUserDefineOutcome: &anthropic.BetaManagedAgentsUserDefineOutcomeEventParams{
  				Description: "Build a DCF model for Costco in .xlsx",
  				Rubric: anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsRubricUnion{
  					OfText: &anthropic.BetaManagedAgentsTextRubricParams{Content: rubric},
  				},
  				// or: OfFile: &anthropic.BetaManagedAgentsFileRubricParams{FileID: rubric.id},
  				MaxIterations: anthropic.Int(5), // optional; default 3, max 20
  			},
  		}},
  	})
  	if err != nil {
  		panic(err)
  	}
  ```
  ```java Java
      // Create a session
      var session = client.beta().sessions().create(
          SessionCreateParams.builder()
              .agent(agent.id())
              .environmentId(environment.id())
              .title("Financial analysis on Costco")
              .build()
      );

      // Define the outcome — agent starts working on receipt
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(
                  BetaManagedAgentsUserDefineOutcomeEventParams.builder()
                      .description("Build a DCF model for Costco in .xlsx")
                      .rubric(BetaTextRubric.builder().content(RUBRIC).build())
                      // or: .rubric(BetaFileRubric.builder().fileId(rubric.id()).build())
                      .maxIterations(5)  // optional; default 3, max 20
                      .build()
              )
              .build()
      );
  ```
  ```php PHP
  // Create a session
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      title: 'Financial analysis on Costco',
  );

  // Define the outcome — agent starts working on receipt
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.define_outcome',
              'description' => 'Build a DCF model for Costco in .xlsx',
              'rubric' => ['type' => 'text', 'content' => $rubric],
              // or: 'rubric' => ['type' => 'file', 'file_id' => $rubric->id],
              'max_iterations' => 5,  // optional; default 3, max 20
          ],
      ],
  );
  ```
  ```ruby Ruby
  # Create a session
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    title: "Financial analysis on Costco"
  )

  # Define the outcome — agent starts working on receipt
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.define_outcome",
        description: "Build a DCF model for Costco in .xlsx",
        rubric: {type: "text", content: rubric},
        # or: rubric: {type: "file", file_id: rubric.id},
        max_iterations: 5 # optional; default 3, max 20
      }
    ]
  )
  ```
</CodeGroup>

## Event outcome

Kemajuan pada sesi yang berorientasi outcome ditampilkan pada [stream](/docs/id/managed-agents/events-and-streaming) event.

- Event `agent.*` (pesan, penggunaan alat, dll.) menunjukkan kemajuan menuju outcome.
- Event `span.outcome_evaluation_*` hanya dipancarkan untuk sesi yang berorientasi outcome dan menunjukkan jumlah loop iterasi serta proses umpan balik grader.
- Anda juga dapat mengirim [event](/docs/id/managed-agents/events-and-streaming#user-events) `user.message` ke sesi yang berorientasi outcome, untuk mengarahkan pekerjaan agen saat berlangsung, tetapi ini tidak terlalu diperlukan; agen tahu untuk bekerja hingga iterasinya habis atau outcome tercapai.
- Event `user.interrupt` akan menghentikan sementara pekerjaan pada outcome saat ini dan menandai `span.outcome_evaluation_end.result` sebagai `interrupted`, memungkinkan Anda memulai outcome baru.
- Setelah evaluasi outcome terakhir, sesi dapat dilanjutkan sebagai sesi percakapan, atau outcome baru dapat dimulai. Sesi akan menyimpan riwayat outcome sebelumnya.

### Event pengguna define outcome
<Note>
Hanya satu outcome yang didukung pada satu waktu, tetapi Anda dapat menggabungkan outcome secara berurutan. Untuk melakukan ini, kirim event `user.define_outcome` baru setelah event terminal dari outcome sebelumnya.
</Note>

Ini adalah event yang Anda kirim untuk memulai sebuah outcome. Event ini dikembalikan saat diterima, termasuk timestamp `processed_at` dan `outcome_id`.

```json
{
  "type": "user.define_outcome",
  "description": "Build a DCF model for Costco in .xlsx",
  "rubric": { "type": "file", "file_id": "file_01..." },
  "max_iterations": 5
}
```

### Mulai evaluasi outcome

Dipancarkan setelah grader memulai evaluasi atas satu loop iterasi. Field `iteration` adalah penghitung revisi yang diindeks dari 0: `0` adalah evaluasi pertama, `1` adalah evaluasi ulang setelah revisi pertama, dan seterusnya.

```json
{
  "type": "span.outcome_evaluation_start",
  "id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:01:45Z"
}
```

### Evaluasi outcome sedang berlangsung

Heartbeat yang dipancarkan saat grader berjalan. Penalaran internal grader bersifat tidak transparan: Anda melihat bahwa ia sedang bekerja, bukan apa yang sedang dipikirkannya.

```json
{
  "type": "span.outcome_evaluation_ongoing",
  "id": "sevt_01ghi...",
  "outcome_id": "outc_01a...",
  "processed_at": "2026-03-25T14:02:10Z"
}
```

### Akhir evaluasi outcome

Dipancarkan setelah grader selesai mengevaluasi satu iterasi. Field `result` menunjukkan apa yang terjadi selanjutnya.

| Hasil | Selanjutnya |
| --- | --- |
| `satisfied` | Sesi beralih ke `idle`. |
| `needs_revision` | Agen memulai siklus iterasi baru. |
| `max_iterations_reached` | Tidak ada siklus evaluasi lebih lanjut. Agen dapat menjalankan satu revisi terakhir sebelum sesi beralih ke `idle`. |
| `failed` | Sesi beralih ke `idle`. Dikembalikan ketika rubrik secara fundamental tidak cocok dengan tugas, misalnya jika deskripsi dan rubrik saling bertentangan. |
| `interrupted` | Hanya dipancarkan jika `outcome_evaluation_start` sudah terpicu sebelum interupsi. |

```json
{
  "type": "span.outcome_evaluation_end",
  "id": "sevt_01jkl...",
  "outcome_evaluation_start_id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "result": "satisfied",
  "explanation": "All 12 criteria met: revenue projections use 5 years of historical data, WACC assumptions are stated, sensitivity table is included...",
  "iteration": 0,
  "usage": {
    "input_tokens": 2400,
    "output_tokens": 350,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 1800
  },
  "processed_at": "2026-03-25T14:03:00Z"
}
```

## Memeriksa status outcome

Anda dapat mendengarkan [stream event](/docs/id/managed-agents/events-and-streaming) untuk `span.outcome_evaluation_end`, atau melakukan polling `GET /v1/sessions/:id` dan membaca `outcome_evaluations[].result`:

<CodeGroup>
  
  ```bash curl
  session=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01-research-preview")

  jq -r '.outcome_evaluations[] | "\(.outcome_id): \(.result)"' <<<"$session"
  # outc_01a...: satisfied
  ```
  
  ```bash CLI
  ant beta:sessions retrieve --session-id "$SESSION_ID"
  ```
  ```python Python
  session = client.beta.sessions.retrieve(session.id)

  for outcome in session.outcome_evaluations:
      print(f"{outcome.outcome_id}: {outcome.result}")
      # outc_01a...: satisfied
  ```
  ```typescript TypeScript
  const retrieved = await client.beta.sessions.retrieve(session.id);

  for (const outcome of retrieved.outcome_evaluations) {
    console.log(`${outcome.outcome_id}: ${outcome.result}`);
    // outc_01a...: satisfied
  }
  ```
  ```csharp C#
  session = await client.Beta.Sessions.Retrieve(session.ID);

  foreach (var outcome in session.OutcomeEvaluations)
  {
      Console.WriteLine($"{outcome.OutcomeID}: {outcome.Result}");
      // outc_01a...: satisfied
  }
  ```
  ```go Go
  	session, err = client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
  	if err != nil {
  		panic(err)
  	}

  	for _, outcome := range session.OutcomeEvaluations {
  		fmt.Printf("%s: %s\n", outcome.OutcomeID, outcome.Result)
  		// outc_01a...: satisfied
  	}
  ```
  ```java Java
      var retrieved = client.beta().sessions().retrieve(session.id());

      for (var outcome : retrieved.outcomeEvaluations()) {
          IO.println(outcome.outcomeId() + ": " + outcome.result());
          // outc_01a...: satisfied
      }
  ```
  ```php PHP
  $session = $client->beta->sessions->retrieve($session->id);

  foreach ($session->outcomeEvaluations as $outcome) {
      echo "{$outcome->outcomeID}: {$outcome->result}\n";
      // outc_01a...: satisfied
  }
  ```
  ```ruby Ruby
  session = client.beta.sessions.retrieve(session.id)

  session.outcome_evaluations.each do
    puts "#{it.outcome_id}: #{it.result}"
    # outc_01a...: satisfied
  end
  ```
</CodeGroup>

## Mengambil deliverable

Agen menulis file output ke `/mnt/session/outputs/` di dalam container. Setelah sesi idle, ambil melalui [Files API](/docs/id/build-with-claude/files) yang dicakup ke sesi:

<CodeGroup>
  ```bash curl
  # List files produced by this session
  curl -fsSL "https://api.anthropic.com/v1/files?scope_id=$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14,managed-agents-2026-04-01-research-preview" \
  | jq '.data[] | {id, filename, size_bytes}'

  # Download by file_id
  curl -fsSL "https://api.anthropic.com/v1/files/$file_id/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -o costco_dcf.xlsx
  ```
  ```python Python
  files = client.beta.files.list(scope_id=session.id)
  for f in files.data:
      print(f"{f.id}: {f.filename} ({f.size_bytes} bytes)")

  content = client.beta.files.download(files.data[0].id)
  content.write_to_file("costco_dcf.xlsx")
  ```
</CodeGroup>