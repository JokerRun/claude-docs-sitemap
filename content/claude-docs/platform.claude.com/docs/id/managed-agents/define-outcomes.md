---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/define-outcomes
fetched_at: 2026-08-21T02:32:13.524433Z
sha256: 3ea0f37bd84fa50a6374889526f27d23cc423c5e26f50bf0af04bd579455b02d
---

---
title: Definisikan hasil
url: https://platform.claude.com/docs/id/managed-agents/define-outcomes
description: Beri tahu agen seperti apa 'selesai' itu, dan biarkan agen melakukan iterasi hingga mencapainya.
---

Sebuah outcome (hasil) memberi tahu sesi seperti apa hasil akhirnya seharusnya dan bagaimana mengukur kualitasnya. Agen bekerja menuju target tersebut, mengevaluasi diri sendiri dan melakukan iterasi hingga hasil tercapai.

Ketika Anda mendefinisikan sebuah hasil, harness secara otomatis menyediakan *grader* (penilai) untuk mengevaluasi artefak terhadap sebuah rubrik. Grader menggunakan "context window" (jendela konteks) terpisah untuk menghindari pengaruh dari pilihan implementasi agen utama.

Grader mengembalikan penjelasan yang merangkum kriteria mana yang lulus atau gagal, atau mengonfirmasi bahwa artefak memenuhi rubrik. Umpan balik tersebut diserahkan kembali ke agen untuk iterasi berikutnya.

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Buat rubrik

Rubrik adalah dokumen markdown yang menjelaskan penilaian per kriteria. Rubrik ini wajib ada.

<Accordion title="Tips untuk menulis rubrik yang efektif">
  Susun rubrik sebagai kriteria yang eksplisit dan dapat dinilai, seperti "CSV berisi kolom price dengan nilai numerik" daripada "Datanya terlihat bagus." Grader menilai setiap kriteria secara independen, sehingga kriteria yang samar menghasilkan evaluasi yang tidak konsisten.

  Jika Anda tidak memiliki rubrik, coba berikan Claude contoh artefak yang sudah diketahui baik dan minta Claude menganalisis apa yang membuat konten tersebut baik, lalu ubah analisis itu menjadi rubrik. Pendekatan jalan tengah ini sering menghasilkan hasil yang lebih baik daripada menulis kriteria dari awal.
</Accordion>

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

Berikan rubrik sebagai teks inline pada `user.define_outcome` (lihat [Buat sesi dengan hasil](https://platform.claude.com/docs/id/managed-agents/define-outcomes#create-a-session-with-an-outcome)), atau unggah melalui Files API untuk digunakan kembali di berbagai sesi.

<Note>
  Mengunggah melalui Files API memerlukan header beta yang memberikan akses Files API. Header beta Managed Agents Anda sudah memberikan akses ini dengan sendirinya, jadi Anda tidak perlu mengirim `files-api-2025-04-14` bersamanya. Contoh curl meneruskan header-nya secara eksplisit.
</Note>

<CodeGroup>
  ```bash cURL
  rubric=$(curl -fsSL https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -F file=@/tmp/rubric.md)
  rubric_id=$(jq -r '.id' <<<"$rubric")
  printf 'Uploaded rubric: %s\n' "$rubric_id"
  ```

  ```bash CLI
  RUBRIC_ID=$(ant files upload \
    --file /tmp/rubric.md \
    --transform id --raw-output)
  ```

  ```python Python
  import time
  from pathlib import Path

  from anthropic import Anthropic

  client = Anthropic()

  RUBRIC = """# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  """
  Path("/tmp/rubric.md").write_text(RUBRIC)

  rubric = client.files.upload(file=Path("/tmp/rubric.md"))
  print(f"Uploaded rubric: {rubric.id}")
  ```

  ```typescript TypeScript
  import { writeFile, readFile } from "node:fs/promises";

  import Anthropic from "@anthropic-ai/sdk";
  import { toFile } from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const RUBRIC = `# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  `;
  await writeFile("/tmp/rubric.md", RUBRIC);

  const rubric = await client.files.upload({
    file: await toFile(readFile("/tmp/rubric.md"), "/tmp/rubric.md"),
  });
  console.log(`Uploaded rubric: ${rubric.id}`);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta.Agents;
  using Anthropic.Models.Beta.Environments;
  using Anthropic.Models.Beta.Sessions;
  using Anthropic.Models.Beta.Sessions.Events;
  using Anthropic.Models.Files;

  var client = new AnthropicClient();

  const string Rubric = """
      # DCF Model Rubric

      ## Revenue Projections
      - Uses historical revenue data from the last 5 fiscal years
      - Projects revenue for at least 5 years forward

      ## Output Quality
      - All figures are in a single .xlsx file with clearly labeled sheets
      """;
  await File.WriteAllTextAsync("/tmp/rubric.md", Rubric);

  var rubric = await client.Files.Upload(new()
  {
      File = File.OpenRead("/tmp/rubric.md"),
  });
  Console.WriteLine($"Uploaded rubric: {rubric.ID}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"io"
  	"os"
  	"time"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  const rubric = `# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  `

  func main() {
  	ctx := context.Background()
  	client := anthropic.NewClient()

  	if err := os.WriteFile("/tmp/rubric.md", []byte(rubric), 0o644); err != nil {
  		panic(err)
  	}

  	f, err := os.Open("/tmp/rubric.md")
  	if err != nil {
  		panic(err)
  	}

  	uploaded, err := client.Files.Upload(ctx, anthropic.FileUploadParams{
  		File: anthropic.File(f, "rubric.md", "text/markdown"),
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("Uploaded rubric: %s\n", uploaded.ID)
  ```

  ```java Java
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponse;
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.agents.AgentCreateParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
  import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
  import com.anthropic.models.beta.environments.BetaCloudConfigParams;
  import com.anthropic.models.beta.environments.EnvironmentCreateParams;
  import com.anthropic.models.beta.files.FileListParams;
  import com.anthropic.models.beta.sessions.SessionCreateParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsTextRubricParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserDefineOutcomeEventParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserInterruptEventParams;
  import com.anthropic.models.beta.sessions.events.EventSendParams;
  import com.anthropic.models.files.FileUploadParams;

  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.nio.file.StandardCopyOption;

  void main() throws Exception {
      var client = AnthropicOkHttpClient.fromEnv();

      var RUBRIC = """
          # DCF Model Rubric

          ## Revenue Projections
          - Uses historical revenue data from the last 5 fiscal years
          - Projects revenue for at least 5 years forward

          ## Output Quality
          - All figures are in a single .xlsx file with clearly labeled sheets
          """;
      Files.writeString(Path.of("/tmp/rubric.md"), RUBRIC);

      var rubric = client.files().upload(
          FileUploadParams.builder()
              .file(Path.of("/tmp/rubric.md"))
              .build());
      IO.println("Uploaded rubric: " + rubric.id());
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  use Anthropic\Client;
  use Anthropic\Core\FileParam;

  $client = new Client();

  $rubricText = <<<'MD'
  # DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  MD;
  file_put_contents('/tmp/rubric.md', $rubricText);

  $rubric = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('/tmp/rubric.md', 'r'), contentType: 'text/markdown'),
  );
  echo "Uploaded rubric: {$rubric->id}\n";
  ```

  ```ruby Ruby
  require "anthropic"
  require "pathname"

  client = Anthropic::Client.new

  RUBRIC = <<~MD
    # DCF Model Rubric

    ## Revenue Projections
    - Uses historical revenue data from the last 5 fiscal years
    - Projects revenue for at least 5 years forward

    ## Output Quality
    - All figures are in a single .xlsx file with clearly labeled sheets
  MD
  File.write("/tmp/rubric.md", RUBRIC)

  rubric = client.files.upload(file: Pathname.new("/tmp/rubric.md"))
  puts "Uploaded rubric: #{rubric.id}"
  ```
</CodeGroup>

## Buat sesi dengan hasil

Contoh berikut membuat sebuah [sesi](https://platform.claude.com/docs/id/managed-agents/sessions) untuk [agen](https://platform.claude.com/docs/id/managed-agents/agent-setup) dan [lingkungan](https://platform.claude.com/docs/id/managed-agents/environments) yang sudah ada (keduanya dibuat secara terpisah), lalu mengirim event `user.define_outcome`. Agen langsung mulai bekerja. Tidak diperlukan event pesan pengguna tambahan.

<CodeGroup>
  ```bash cURL
  # Membuat sesi
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

  # Mendefinisikan hasil — agen mulai bekerja begitu menerimanya
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
  # "max_iterations" bersifat opsional; default 3, maksimum 20
  ```

  ```bash CLI
  # Create a session
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --title "Financial analysis on Costco" \
    --transform id --raw-output)

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
    title: "Financial analysis on Costco",
  });

  // Define the outcome — agent starts working on receipt
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.define_outcome",
        description: "Build a DCF model for Costco in .xlsx",
        rubric: { type: "text", content: RUBRIC },
        // or: rubric: { type: "file", file_id: rubric.id },
        max_iterations: 5, // optional; default 3, max 20
      },
    ],
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
              Type = BetaManagedAgentsUserDefineOutcomeEventParamsType.UserDefineOutcome,
              Description = "Build a DCF model for Costco in .xlsx",
              Rubric = new BetaManagedAgentsTextRubricParams
              {
                  Type = BetaManagedAgentsTextRubricParamsType.Text,
                  Content = Rubric,
              },
              // or: Rubric = new BetaManagedAgentsFileRubricParams
              //     { Type = BetaManagedAgentsFileRubricParamsType.File, FileID = rubric.ID },
              MaxIterations = 5, // optional; default 3, max 20
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
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserDefineOutcome: &anthropic.BetaManagedAgentsUserDefineOutcomeEventParams{
  			Type:        anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsTypeUserDefineOutcome,
  			Description: "Build a DCF model for Costco in .xlsx",
  			Rubric: anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsRubricUnion{
  				OfText: &anthropic.BetaManagedAgentsTextRubricParams{
  					Type:    anthropic.BetaManagedAgentsTextRubricParamsTypeText,
  					Content: rubric,
  				},
  			},
  			// or: OfFile: &anthropic.BetaManagedAgentsFileRubricParams{
  			//     Type: anthropic.BetaManagedAgentsFileRubricParamsTypeFile, FileID: uploaded.ID},
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
          .build());

  // Define the outcome — agent starts working on receipt
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsUserDefineOutcomeEventParams.builder()
              .type(BetaManagedAgentsUserDefineOutcomeEventParams.Type.USER_DEFINE_OUTCOME)
              .description("Build a DCF model for Costco in .xlsx")
              .rubric(BetaManagedAgentsTextRubricParams.builder()
                  .type(BetaManagedAgentsTextRubricParams.Type.TEXT)
                  .content(RUBRIC)
                  .build())
              // or: .rubric(BetaManagedAgentsFileRubricParams.builder()
              //     .type(BetaManagedAgentsFileRubricParams.Type.FILE).fileId(rubric.id()).build())
              .maxIterations(5) // optional; default 3, max 20
              .build())
          .build());
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
              'rubric' => ['type' => 'text', 'content' => $rubricText],
              // or: 'rubric' => ['type' => 'file', 'file_id' => $rubric->id],
              'max_iterations' => 5, // optional; default 3, max 20
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
        rubric: {type: "text", content: RUBRIC},
        # or: rubric: {type: "file", file_id: rubric.id},
        max_iterations: 5 # optional; default 3, max 20
      }
    ]
  )
  ```
</CodeGroup>

<Note>
  Anda juga dapat mendefinisikan hasil dalam permintaan pembuatan itu sendiri: berikan satu event `user.define_outcome` di [`initial_events`](https://platform.claude.com/docs/id/managed-agents/sessions#seed-the-session-with-initial-events) untuk membuat sesi dan memulai pekerjaan menuju hasil dalam satu panggilan.
</Note>

## Event hasil

Kemajuan pada sesi yang berorientasi hasil ditampilkan pada [stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) event.

* Event `agent.*` (seperti pesan dan penggunaan alat) menunjukkan kemajuan menuju hasil.
* Event `span.outcome_evaluation_*` hanya dipancarkan untuk sesi yang berorientasi hasil dan menunjukkan jumlah loop iterasi serta proses umpan balik grader.
* Anda juga dapat mengirim [event](https://platform.claude.com/docs/id/managed-agents/reference#event-types) `user.message` ke sesi yang berorientasi hasil untuk mengarahkan pekerjaan agen saat berlangsung, tetapi ini tidak wajib: agen bekerja menuju hasil dengan sendirinya, melakukan iterasi hingga berhasil atau kehabisan iterasi.
* Event `user.interrupt` menjeda pekerjaan pada hasil saat ini dan menandai `span.outcome_evaluation_end.result` sebagai `interrupted`, memungkinkan Anda memulai hasil baru.
* Setelah evaluasi hasil terakhir, sesi dapat dilanjutkan sebagai sesi percakapan, atau hasil baru dapat dimulai. Sesi menyimpan riwayat hasil sebelumnya.

### Event pengguna define outcome

<Note>
  Hanya satu hasil yang didukung pada satu waktu, tetapi Anda dapat merangkai hasil secara berurutan. Untuk melakukannya, kirim event `user.define_outcome` baru setelah event terminal `span.outcome_evaluation_end` dari hasil sebelumnya.
</Note>

Ini adalah event yang Anda kirim untuk memulai sebuah hasil. Event ini digemakan kembali saat diterima, termasuk timestamp `processed_at` dan `outcome_id`.

```json
{
  "type": "user.define_outcome",
  "description": "Build a DCF model for Costco in .xlsx",
  "rubric": { "type": "file", "file_id": "file_01..." },
  "max_iterations": 5
}
```

### Mulai evaluasi hasil

Dipancarkan saat grader memulai evaluasi pada satu loop iterasi. Field `iteration` adalah penghitung revisi berindeks 0: `0` adalah evaluasi pertama, `1` adalah evaluasi ulang setelah revisi pertama, dan seterusnya.

```json
{
  "type": "span.outcome_evaluation_start",
  "id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:01:45Z"
}
```

### Evaluasi hasil sedang berlangsung

Heartbeat yang dipancarkan saat grader berjalan. Penalaran internal grader bersifat tertutup: Anda melihat bahwa grader sedang bekerja, bukan apa yang sedang dipikirkannya.

```json
{
  "type": "span.outcome_evaluation_ongoing",
  "id": "sevt_01ghi...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:02:10Z"
}
```

### Akhir evaluasi hasil

Dipancarkan ketika siklus evaluasi hasil berakhir: setelah grader selesai mengevaluasi satu iterasi, atau ketika sesi diinterupsi saat sebuah hasil sedang aktif. Field `result` menunjukkan apa yang terjadi selanjutnya.

| Result                   | Selanjutnya                                                                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `satisfied`              | Sesi bertransisi ke `idle`.                                                                                                                                                                                                          |
| `needs_revision`         | Agen memulai siklus iterasi baru.                                                                                                                                                                                                    |
| `max_iterations_reached` | Satu giliran pengakuan terakhir mengikuti sebelum sesi bertransisi ke `idle`. Tidak ada evaluasi lebih lanjut yang dijalankan.                                                                                                       |
| `failed`                 | Sesi bertransisi ke `idle`. Dikembalikan ketika rubrik tidak berlaku untuk deliverable, misalnya jika deskripsi dan rubrik saling bertentangan.                                                                                      |
| `interrupted`            | Dipancarkan ketika sesi diinterupsi saat sebuah hasil sedang aktif, bahkan jika evaluasi belum dimulai. Jika tidak ada `outcome_evaluation_start` yang dipicu sebelum interupsi, `outcome_evaluation_start_id` adalah string kosong. |

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

## Periksa status hasil

Anda dapat mendengarkan [stream event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) untuk `span.outcome_evaluation_end`, atau melakukan polling `GET /v1/sessions/{session_id}` dan membaca `outcome_evaluations[].result`. Hingga evaluasi selesai, `result` melaporkan `pending`, `running`, atau `evaluating`:

<CodeGroup>
  ```bash cURL
  session=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  jq -r '.outcome_evaluations[] | "\(.outcome_id): \(.result)"' <<<"$session"
  # outc_01a...: satisfied
  ```

  ```bash CLI
  ant beta:sessions retrieve --session-id "$SESSION_ID" \
    --transform 'outcome_evaluations' --format yaml
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

## Ambil deliverable

Agen menulis file output ke `/mnt/session/outputs/` di dalam sandbox. Setelah sesi idle, ambil file tersebut melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files) yang dicakup ke sesi tersebut.

<Note>
  Memfilter berdasarkan `scope_id` memerlukan header beta `managed-agents-2026-04-01` pada permintaan files. Metode files SDK hanya mengirim beta files secara otomatis, sehingga contoh-contoh meneruskannya secara eksplisit.
</Note>

<CodeGroup>
  ```bash cURL
  # Mencantumkan file yang dihasilkan oleh sesi ini
  # Pemfilteran scope_id memerlukan beta managed-agents
  files=$(curl -fsSL "https://api.anthropic.com/v1/files?scope_id=$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  jq -r '.data[] | "\(.id) \(.filename)"' <<<"$files"

  # Mengunduh file
  file_id=$(jq -r '.data[0].id // empty' <<<"$files")
  if [[ -n $file_id ]]; then
    curl -fsSL "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -o /tmp/output.txt
  fi
  ```

  ```bash CLI
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  ant beta:files list --scope-id "$SESSION_ID" \
    --beta managed-agents-2026-04-01

  # Download a file
  FILE_ID=$(ant beta:files list --scope-id "$SESSION_ID" \
    --beta managed-agents-2026-04-01 \
    --transform 'data[0].id' --raw-output)
  if [[ -n $FILE_ID ]]; then
    ant files download --file-id "$FILE_ID" --output /tmp/output.txt
  fi
  ```

  ```python Python
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  files = client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"])
  for file in files:
      print(file.id, file.filename)

  # Download a file
  if files.data:
      content = client.files.download(files.data[0].id)
      content.write_to_file("/tmp/output.txt")
  ```

  ```typescript TypeScript
  // List files produced by this session
  // scope_id filtering requires the managed-agents beta on the files request
  const files = await client.beta.files.list({
    scope_id: session.id,
    betas: ["managed-agents-2026-04-01"],
  });
  for (const file of files.data) {
    console.log(file.id, file.filename);
  }

  // Download a file
  if (files.data.length > 0) {
    const content = await client.files.download(files.data[0].id);
    await writeFile("/tmp/output.txt", new Uint8Array(await content.arrayBuffer()));
  }
  ```

  ```csharp C#
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  var files = await client.Beta.Files.List(new()
  {
      ScopeID = session.ID,
      Betas = ["managed-agents-2026-04-01"],
  });
  foreach (var file in files.Items)
  {
      Console.WriteLine($"{file.ID} {file.Filename}");
  }

  // Download a file
  if (files.Items.Count > 0)
  {
      using var download = await client.Files.Download(files.Items[0].ID);
      await using var output = File.Create("/tmp/output.txt");
      await (await download.ReadAsStream()).CopyToAsync(output);
  }
  ```

  ```go Go
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
  	ScopeID: anthropic.String(session.ID),
  	Betas:   []anthropic.AnthropicBeta{anthropic.AnthropicBetaManagedAgents2026_04_01},
  })
  if err != nil {
  	panic(err)
  }
  for _, file := range files.Data {
  	fmt.Println(file.ID, file.Filename)
  }

  // Download a file
  if len(files.Data) > 0 {
  	resp, err := client.Files.Download(ctx, files.Data[0].ID)
  	if err != nil {
  		panic(err)
  	}
  	defer resp.Body.Close()
  	out, err := os.Create("/tmp/output.txt")
  	if err != nil {
  		panic(err)
  	}
  	defer out.Close()
  	if _, err := io.Copy(out, resp.Body); err != nil {
  		panic(err)
  	}
  }
  ```

  ```java Java
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  var files = client.beta().files().list(
      FileListParams.builder()
          .scopeId(session.id())
          .addBeta(AnthropicBeta.MANAGED_AGENTS_2026_04_01)
          .build());
  for (var file : files.data()) {
      IO.println(file.id() + " " + file.filename());
  }

  // Download a file
  if (!files.data().isEmpty()) {
      try (HttpResponse response = client.files().download(files.data().getFirst().id())) {
          try (InputStream body = response.body()) {
              Files.copy(body, Path.of("/tmp/output.txt"), StandardCopyOption.REPLACE_EXISTING);
          }
      }
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // List files produced by this session
  // scope_id filtering requires the managed-agents beta on the files request
  $files = $client->beta->files->list(scopeID: $session->id, betas: ['managed-agents-2026-04-01']);
  foreach ($files->data as $file) {
      echo "{$file->id} {$file->filename}\n";
  }

  // Download a file
  if (count($files->data) > 0) {
      $content = $client->beta->files->download($files->data[0]->id);
      file_put_contents('/tmp/output.txt', $content);
  }
  ```

  ```ruby Ruby
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  files = client.beta.files.list(scope_id: session.id, betas: ["managed-agents-2026-04-01"])
  files.data.each { |file| puts "#{file.id} #{file.filename}" }

  # Download a file
  if (first = files.data.first)
    content = client.files.download(first.id)
    File.binwrite("/tmp/output.txt", content.read)
  end
  ```
</CodeGroup>

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Autentikasi dengan vault" icon="fingerprint" href="https://platform.claude.com/docs/id/managed-agents/vaults">
    Daftarkan kredensial per pengguna saat membuat sesi.
  </Card>

  <Card title="Stream event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau alihkan sesi Anda di tengah eksekusi.
  </Card>

  <Card title="Menambahkan file" icon="file" href="https://platform.claude.com/docs/id/managed-agents/files">
    Unggah file dan pasang di sandbox Anda untuk dibaca dan diproses.
  </Card>
</CardGroup>
