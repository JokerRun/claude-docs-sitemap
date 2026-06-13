---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/define-outcomes
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: c926a04be3fc72a20a72e5c7336b53e8f2898859d5c2d4c94dfea7c7732a3c66
---

# Mendefinisikan hasil

Beri tahu agen seperti apa kondisi 'selesai' itu, dan biarkan agen melakukan iterasi hingga mencapainya.

---

`outcome` meningkatkan sebuah sesi dari sekadar *percakapan* menjadi *pekerjaan*. Anda mendefinisikan seperti apa hasil akhir yang diharapkan dan bagaimana mengukur kualitasnya. Agen bekerja menuju target tersebut, melakukan evaluasi mandiri dan iterasi hingga hasil tercapai.

Ketika Anda mendefinisikan sebuah outcome, harness secara otomatis menyediakan *grader* (penilai) untuk mengevaluasi artefak terhadap sebuah rubrik. Grader menggunakan jendela konteks terpisah agar tidak terpengaruh oleh pilihan implementasi agen utama.

Grader mengembalikan penjelasan yang merangkum kriteria mana yang lulus atau gagal, atau mengonfirmasi bahwa artefak memenuhi rubrik. Umpan balik tersebut diserahkan kembali ke agen untuk iterasi berikutnya.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat rubrik \{#create-a-rubric}

Rubrik adalah dokumen markdown yang menjelaskan penilaian per kriteria. Rubrik bersifat wajib.

<section title="Tips untuk menulis rubrik yang efektif">

Susun rubrik sebagai kriteria yang eksplisit dan dapat dinilai, seperti "CSV berisi kolom harga dengan nilai numerik" alih-alih "Datanya terlihat bagus." Grader menilai setiap kriteria secara independen, sehingga kriteria yang samar menghasilkan evaluasi yang tidak konsisten.

Jika Anda belum memiliki rubrik, coba berikan Claude contoh artefak yang diketahui baik dan minta Claude menganalisis apa yang membuat konten tersebut baik, lalu ubah analisis itu menjadi rubrik. Pendekatan jalan tengah ini sering kali menghasilkan hasil yang lebih baik daripada menulis kriteria dari awal.

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

Kirimkan rubrik sebagai teks inline pada `user.define_outcome` (lihat bagian berikutnya), atau unggah melalui Files API untuk digunakan kembali di berbagai sesi.

<Note>
Mengunggah melalui Files API memerlukan kedua header beta `managed-agents-2026-04-01` dan `files-api-2025-04-14`.
</Note>

<CodeGroup>
  
````bash
rubric=$(curl -fsSL https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14" \
  -F file=@/tmp/rubric.md)
rubric_id=$(jq -r '.id' <<<"$rubric")
printf 'Uploaded rubric: %s\n' "$rubric_id"
````

  
````bash
RUBRIC_ID=$(ant beta:files upload \
  --file /tmp/rubric.md \
  --transform id --raw-output)
````

  
````python
rubric = client.beta.files.upload(file=Path("/tmp/rubric.md"))
print(f"Uploaded rubric: {rubric.id}")
````

  
````typescript
const rubric = await client.beta.files.upload({
  file: await toFile(readFile("/tmp/rubric.md"), "/tmp/rubric.md"),
});
console.log(`Uploaded rubric: ${rubric.id}`);
````

  
````csharp
var rubric = await client.Beta.Files.Upload(new()
{
    File = File.OpenRead("/tmp/rubric.md"),
});
Console.WriteLine($"Uploaded rubric: {rubric.ID}");
````

  
````go
f, err := os.Open("/tmp/rubric.md")
if err != nil {
	panic(err)
}

uploaded, err := client.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
	File: anthropic.File(f, "/tmp/rubric.md", "text/markdown"),
})
if err != nil {
	panic(err)
}
fmt.Printf("Uploaded rubric: %s\n", uploaded.ID)
````

  
````java
var rubric = client.beta().files().upload(
    FileUploadParams.builder()
        .file(Path.of("/tmp/rubric.md"))
        .build());
IO.println("Uploaded rubric: " + rubric.id());
````

  
````php
$rubric = $client->beta->files->upload(
    file: fopen('/tmp/rubric.md', 'r'),
);
echo "Uploaded rubric: {$rubric->id}\n";
````

  
````ruby
rubric = client.beta.files.upload(file: Pathname.new("/tmp/rubric.md"))
puts "Uploaded rubric: #{rubric.id}"
````

</CodeGroup>

## Membuat sesi dengan outcome \{#create-a-session-with-an-outcome}

Setelah membuat sesi, kirim event `user.define_outcome`. Agen segera mulai bekerja; tidak diperlukan event pesan pengguna tambahan.

<CodeGroup>
  
````bash
# Buat sebuah sesi
session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  --json @- <<EOF
{
  "agent": "$agent_id",
  "environment_id": "$environment_id",
  "title": "Financial analysis on Costco"
}
EOF
)
session_id=$(jq -r '.id' <<<"$session")

# Definisikan hasil — agen mulai bekerja saat menerimanya
curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id/events" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
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
# atau: "rubric": {"type": "file", "file_id": "$rubric_id"}
# "max_iterations" bersifat opsional; default 3, maks 20
````

  
````bash
# Buat sesi
SESSION_ID=$(ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment-id "$ENVIRONMENT_ID" \
  --title "Financial analysis on Costco" \
  --transform id --raw-output)

# Tentukan hasil — agen mulai bekerja saat menerima
ant beta:sessions:events send \
  --session-id "$SESSION_ID" <<YAML
events:
  - type: user.define_outcome
    description: Build a DCF model for Costco in .xlsx
    rubric: {type: file, file_id: $RUBRIC_ID}
    # atau: rubric: {type: text, content: "..."}
    max_iterations: 5  # optional; default 3, max 20
YAML
````

  
````python
# Buat sesi
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Financial analysis on Costco",
)

# Definisikan hasil — agen mulai bekerja saat menerimanya
client.beta.sessions.events.send(
    session_id=session.id,
    events=[
        {
            "type": "user.define_outcome",
            "description": "Build a DCF model for Costco in .xlsx",
            "rubric": {"type": "text", "content": RUBRIC},
            # atau: "rubric": {"type": "file", "file_id": rubric.id},
            "max_iterations": 5,  # optional; default 3, max 20
        }
    ],
)
````

  
````typescript
// Buat sesi
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  title: "Financial analysis on Costco",
});

// Definisikan hasil — agen mulai bekerja saat menerima
await client.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.define_outcome",
      description: "Build a DCF model for Costco in .xlsx",
      rubric: { type: "text", content: RUBRIC },
      // atau: rubric: { type: "file", file_id: rubric.id },
      max_iterations: 5, // optional; default 3, max 20
    },
  ],
});
````

  
````csharp
// Buat sesi
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
    Title = "Financial analysis on Costco",
});

// Tentukan hasil — agen mulai bekerja saat diterima
await client.Beta.Sessions.Events.Send(session.ID, new()
{
    Events =
    [
        new BetaManagedAgentsUserDefineOutcomeEventParams
        {
            Type = "user.define_outcome",
            Description = "Build a DCF model for Costco in .xlsx",
            Rubric = new BetaManagedAgentsTextRubricParams { Type = "text", Content = Rubric },
            // atau: Rubric = new BetaManagedAgentsFileRubricParams { Type = "file", FileID = rubric.ID },
            MaxIterations = 5, // optional; default 3, max 20
        },
    ],
});
````

  
````go
// Buat sesi
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

// Definisikan hasil — agen mulai bekerja saat menerimanya
_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
		OfUserDefineOutcome: &anthropic.BetaManagedAgentsUserDefineOutcomeEventParams{
			Description: "Build a DCF model for Costco in .xlsx",
			Rubric: anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsRubricUnion{
				OfText: &anthropic.BetaManagedAgentsTextRubricParams{Content: rubric},
			},
			// atau: OfFile: &anthropic.BetaManagedAgentsFileRubricParams{FileID: uploaded.ID},
			MaxIterations: anthropic.Int(5), // optional; default 3, max 20
		},
	}},
})
if err != nil {
	panic(err)
}
````

  
````java
// Buat sesi
var session = client.beta().sessions().create(
    SessionCreateParams.builder()
        .agent(agent.id())
        .environmentId(environment.id())
        .title("Financial analysis on Costco")
        .build());

// Definisikan hasil — agen mulai bekerja saat diterima
client.beta().sessions().events().send(
    session.id(),
    EventSendParams.builder()
        .addEvent(BetaManagedAgentsUserDefineOutcomeEventParams.builder()
            .description("Build a DCF model for Costco in .xlsx")
            .rubric(BetaManagedAgentsTextRubricParams.builder().content(RUBRIC).build())
            // atau: .rubric(BetaManagedAgentsFileRubricParams.builder().fileId(rubric.id()).build())
            .maxIterations(5) // optional; default 3, max 20
            .build())
        .build());
````

  
````php
// Buat sesi
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    title: 'Financial analysis on Costco',
);

// Definisikan hasil — agen mulai bekerja saat diterima
$client->beta->sessions->events->send(
    $session->id,
    events: [
        [
            'type' => 'user.define_outcome',
            'description' => 'Build a DCF model for Costco in .xlsx',
            'rubric' => ['type' => 'text', 'content' => $rubricText],
            // atau: 'rubric' => ['type' => 'file', 'file_id' => $rubric->id],
            'max_iterations' => 5, // optional; default 3, max 20
        ],
    ],
);
````

  
````ruby
# Buat sebuah sesi
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  title: "Financial analysis on Costco"
)

# Definisikan hasil — agen mulai bekerja saat menerimanya
client.beta.sessions.events.send_(
  session.id,
  events: [
    {
      type: "user.define_outcome",
      description: "Build a DCF model for Costco in .xlsx",
      rubric: {type: "text", content: RUBRIC},
      # atau: rubric: {type: "file", file_id: rubric.id},
      max_iterations: 5 # optional; default 3, max 20
    }
  ]
)
````

</CodeGroup>

## Event outcome \{#outcome-events}

Progres pada sesi berorientasi outcome ditampilkan pada [stream](/docs/id/managed-agents/events-and-streaming) event.

- Event `agent.*` (seperti pesan dan penggunaan alat) menunjukkan progres menuju outcome.
- Event `span.outcome_evaluation_*` hanya dipancarkan untuk sesi berorientasi outcome dan menunjukkan jumlah loop iterasi serta proses umpan balik grader.
- Anda juga dapat mengirim [event](/docs/id/managed-agents/reference#event-types) `user.message` ke sesi berorientasi outcome untuk mengarahkan pekerjaan agen selama berlangsung, tetapi ini tidak wajib: agen bekerja menuju outcome secara mandiri, melakukan iterasi hingga berhasil atau kehabisan iterasi.
- Event `user.interrupt` menjeda pekerjaan pada outcome saat ini dan menandai `span.outcome_evaluation_end.result` sebagai `interrupted`, memungkinkan Anda memulai outcome baru.
- Setelah evaluasi outcome terakhir, sesi dapat dilanjutkan sebagai sesi percakapan, atau outcome baru dapat dimulai. Sesi mempertahankan riwayat dari outcome sebelumnya.

### Event pengguna define outcome \{#define-outcome-user-event}
<Note>
Hanya satu outcome yang didukung dalam satu waktu, tetapi Anda dapat merangkai outcome secara berurutan. Untuk melakukannya, kirim event `user.define_outcome` baru setelah event terminal dari outcome sebelumnya.
</Note>

Ini adalah event yang Anda kirim untuk memulai sebuah outcome. Event ini dipantulkan kembali saat diterima, termasuk timestamp `processed_at` dan `outcome_id`.

```json
{
  "type": "user.define_outcome",
  "description": "Build a DCF model for Costco in .xlsx",
  "rubric": { "type": "file", "file_id": "file_01..." },
  "max_iterations": 5
}
```

### Outcome evaluation start \{#outcome-evaluation-start}

Dipancarkan begitu grader memulai evaluasi pada satu loop iterasi. Field `iteration` adalah penghitung revisi berbasis indeks 0: `0` adalah evaluasi pertama, `1` adalah evaluasi ulang setelah revisi pertama, dan seterusnya.

```json
{
  "type": "span.outcome_evaluation_start",
  "id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:01:45Z"
}
```

### Outcome evaluation ongoing \{#outcome-evaluation-ongoing}

Heartbeat yang dipancarkan selama grader berjalan. Penalaran internal grader bersifat tertutup: Anda melihat bahwa grader sedang bekerja, bukan apa yang sedang dipikirkannya.

```json
{
  "type": "span.outcome_evaluation_ongoing",
  "id": "sevt_01ghi...",
  "outcome_id": "outc_01a...",
  "processed_at": "2026-03-25T14:02:10Z"
}
```

### Outcome evaluation end \{#outcome-evaluation-end}

Dipancarkan setelah grader selesai mengevaluasi satu iterasi. Field `result` menunjukkan apa yang terjadi selanjutnya.

| Result | Selanjutnya |
| --- | --- |
| `satisfied` | Sesi bertransisi ke `idle`. |
| `needs_revision` | Agen memulai siklus iterasi baru. |
| `max_iterations_reached` | Tidak ada siklus evaluasi lebih lanjut. Agen dapat menjalankan satu revisi terakhir sebelum sesi bertransisi ke `idle`. |
| `failed` | Sesi bertransisi ke `idle`. Dikembalikan ketika rubrik secara fundamental tidak cocok dengan tugas, misalnya jika deskripsi dan rubrik saling bertentangan. |
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

## Memeriksa status outcome \{#checking-on-outcome-status}

Anda dapat mendengarkan pada [event stream](/docs/id/managed-agents/events-and-streaming) untuk `span.outcome_evaluation_end`, atau melakukan polling `GET /v1/sessions/:id` dan membaca `outcome_evaluations[].result`:

<CodeGroup>
  
````bash
session=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")

jq -r '.outcome_evaluations[] | "\(.outcome_id): \(.result)"' <<<"$session"
# outc_01a...: satisfied
````

  
````bash
ant beta:sessions retrieve --session-id "$SESSION_ID" \
  --transform 'outcome_evaluations' --format yaml
````

  
````python
session = client.beta.sessions.retrieve(session.id)

for outcome in session.outcome_evaluations:
    print(f"{outcome.outcome_id}: {outcome.result}")
    # outc_01a...: satisfied
````

  
````typescript
const retrieved = await client.beta.sessions.retrieve(session.id);

for (const outcome of retrieved.outcome_evaluations) {
  console.log(`${outcome.outcome_id}: ${outcome.result}`);
  // outc_01a...: satisfied
}
````

  
````csharp
session = await client.Beta.Sessions.Retrieve(session.ID);

foreach (var outcome in session.OutcomeEvaluations)
{
    Console.WriteLine($"{outcome.OutcomeID}: {outcome.Result}");
    // outc_01a...: satisfied
}
````

  
````go
session, err = client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
if err != nil {
	panic(err)
}

for _, outcome := range session.OutcomeEvaluations {
	fmt.Printf("%s: %s\n", outcome.OutcomeID, outcome.Result)
	// outc_01a...: satisfied
}
````

  
````java
var retrieved = client.beta().sessions().retrieve(session.id());

for (var outcome : retrieved.outcomeEvaluations()) {
    IO.println(outcome.outcomeId() + ": " + outcome.result());
    // outc_01a...: terpenuhi
}
````

  
````php
$session = $client->beta->sessions->retrieve($session->id);

foreach ($session->outcomeEvaluations as $outcome) {
    echo "{$outcome->outcomeID}: {$outcome->result}\n";
    // outc_01a...: terpenuhi
}
````

  
````ruby
session = client.beta.sessions.retrieve(session.id)

session.outcome_evaluations.each do
  puts "#{it.outcome_id}: #{it.result}"
  # outc_01a...: satisfied
end
````

</CodeGroup>

## Mengambil deliverable \{#retrieving-deliverables}

Agen menulis file output ke `/mnt/session/outputs/` di dalam sandbox. Setelah sesi berada dalam status idle, ambil file tersebut melalui [Files API](/docs/id/build-with-claude/files) yang dicakupkan ke sesi:

<CodeGroup>
  
````bash
# Daftar file yang dihasilkan oleh sesi ini
files=$(curl -fsSL "https://api.anthropic.com/v1/files?scope_id=$session_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01")
jq -r '.data[] | "\(.id) \(.filename)"' <<<"$files"

# Unduh sebuah file
file_id=$(jq -r '.data[0].id // empty' <<<"$files")
if [[ -n $file_id ]]; then
  curl -fsSL "https://api.anthropic.com/v1/files/$file_id/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -o /tmp/output.txt
fi
````

  
````bash
# Daftar file yang dihasilkan oleh sesi ini
ant beta:files list --scope-id "$SESSION_ID"

# Unduh file
FILE_ID=$(ant beta:files list --scope-id "$SESSION_ID" \
  --transform 'data[0].id' --raw-output)
if [[ -n $FILE_ID ]]; then
  ant beta:files download --file-id "$FILE_ID" --output /tmp/output.txt
fi
````

  
````python
# Daftar file yang dihasilkan oleh sesi ini
files = client.beta.files.list(scope_id=session.id)
for f in files:
    print(f.id, f.filename)

# Unduh sebuah file
if files.data:
    content = client.beta.files.download(files.data[0].id)
    content.write_to_file("/tmp/output.txt")
````

  
````typescript
// Daftar file yang dihasilkan oleh sesi ini
const files = await client.beta.files.list({ scope_id: session.id });
for (const f of files.data) {
  console.log(f.id, f.filename);
}

// Unduh file
if (files.data.length > 0) {
  const content = await client.beta.files.download(files.data[0].id);
  await writeFile("/tmp/output.txt", new Uint8Array(await content.arrayBuffer()));
}
````

  
````csharp
// Daftar file yang dihasilkan oleh sesi ini
var files = await client.Beta.Files.List(new() { ScopeID = session.ID });
foreach (var file in files.Data)
{
    Console.WriteLine($"{file.ID} {file.Filename}");
}

// Unduh file
if (files.Data.Count > 0)
{
    var content = await client.Beta.Files.Download(files.Data[0].ID);
    await File.WriteAllBytesAsync("/tmp/output.txt", content);
}
````

  
````go
// Daftar file yang dihasilkan oleh sesi ini
files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
	// berikan ScopeID: anthropic.String(session.ID) untuk memfilter
})
if err != nil {
	panic(err)
}
for _, file := range files.Data {
	fmt.Println(file.ID, file.Filename)
}

// Unduh file
if len(files.Data) > 0 {
	resp, err := client.Beta.Files.Download(ctx, files.Data[0].ID, anthropic.BetaFileDownloadParams{})
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	fileContent, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	if err := os.WriteFile("/tmp/output.txt", fileContent, 0o644); err != nil {
		panic(err)
	}
}
````

  
````java
// Daftar file yang dihasilkan oleh sesi ini
var files = client.beta().files().list(
    FileListParams.builder()/* pass .scopeId(session.id()) to filter */.build());
for (var file : files.data()) {
    IO.println(file.id() + " " + file.filename());
}

// Unduh file
if (!files.data().isEmpty()) {
    try (HttpResponse response = client.beta().files().download(files.data().getFirst().id())) {
        try (InputStream body = response.body()) {
            Files.copy(body, Path.of("/tmp/output.txt"), StandardCopyOption.REPLACE_EXISTING);
        }
    }
}
````

  
````php
// Daftar file yang dihasilkan oleh sesi ini
$files = $client->beta->files->list(/* pass scopeID: $session->id to filter */);
foreach ($files->data as $file) {
    echo "{$file->id} {$file->filename}\n";
}

// Unduh file
if (count($files->data) > 0) {
    $content = $client->beta->files->download($files->data[0]->id);
    file_put_contents('/tmp/output.txt', $content);
}
````

  
````ruby
# Daftar file yang dihasilkan oleh sesi ini
files = client.beta.files.list(scope_id: session.id)
files.data.each { puts "#{it.id} #{it.filename}" }

# Unduh sebuah file
if (first = files.data.first)
  content = client.beta.files.download(first.id)
  File.binwrite("/tmp/output.txt", content.read)
end
````

</CodeGroup>