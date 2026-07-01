---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: a1a5a7c08341918f4fe282e2ca1e3ba45c33e1e9bfac89f7b1b266ae44a5cf22
---

# Alat eksekusi kode

Jalankan kode Python dan bash dalam kontainer sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.

---

Claude dapat menganalisis data, membuat visualisasi, melakukan perhitungan kompleks, menjalankan perintah sistem, membuat dan mengedit file, serta memproses file yang diunggah secara langsung dalam percakapan API. Alat eksekusi kode memungkinkan Claude menjalankan perintah Bash dan memanipulasi file, termasuk menulis kode, dalam lingkungan sandbox yang aman.

**Eksekusi kode gratis ketika digunakan bersama web search atau web fetch.** Ketika `web_search_20260209` (atau yang lebih baru) atau `web_fetch_20260209` (atau yang lebih baru) disertakan dalam permintaan Anda, tidak ada biaya tambahan untuk panggilan alat eksekusi kode di luar biaya token input dan output standar. Biaya eksekusi kode standar berlaku ketika alat-alat ini tidak disertakan.

Eksekusi kode adalah primitif inti untuk membangun agen berkinerja tinggi. Ini memungkinkan pemfilteran dinamis pada alat web search dan web fetch, sehingga Claude dapat memproses hasil sebelum mencapai jendela konteks, meningkatkan akurasi sekaligus mengurangi konsumsi token.

<Note>
  Hubungi kami melalui [formulir umpan balik](https://forms.gle/LTAU6Xn2puCJMi1n6) untuk membagikan masukan Anda tentang fitur ini.
</Note>

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Kompatibilitas model

Alat eksekusi kode tersedia pada model-model berikut:

| Model                                                                                                         | Versi alat                                                                      |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Claude Fable 5 (claude-fable-5)                                                                               | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Mythos 5 (claude-mythos-5)                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 5 (claude-sonnet-5)                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.8 (claude-opus-4-8)                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.7 (claude-opus-4-7)                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.6 (claude-opus-4-6)                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 4.6 (claude-sonnet-4-6)                                                                         | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.5 (claude-opus-4-5-20251101)                                                                    | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)                                                                | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001)                                                                  | `code_execution_20250825`                                                       |
| Claude Opus 4.1 (claude-opus-4-1-20250805) ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) | `code_execution_20250825`                                                       |

<Note>
  `code_execution_20250825` mendukung perintah Bash dan operasi file, serta tersedia pada setiap model dalam tabel. `code_execution_20260120` menambahkan persistensi state REPL dan [pemanggilan alat secara programatik](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox, dan hanya tersedia pada Claude Fable 5, Claude Mythos 5, Opus 4.5+, dan Sonnet 4.5+. `code_execution_20260521` adalah runtime yang sama dengan `_20260120` dengan batas waktu eksekusi per sel yang diungkapkan dalam deskripsi alat, sehingga Claude dapat mengatur anggaran waktu untuk sel yang berjalan lama. Setiap sel memiliki batas waktu wall-clock 90 detik; kode yang melebihinya akan mengembalikan hasil `detection_timeout`. Jika Anda masih menggunakan `code_execution_20250522` lama (hanya Python), lihat [Upgrade ke versi alat terbaru](#upgrade-to-latest-tool-version) untuk bermigrasi darinya.
</Note>

<Warning>
  Versi alat yang lebih lama tidak dijamin kompatibel mundur dengan model yang lebih baru. Selalu gunakan versi alat yang sesuai dengan versi model Anda.
</Warning>

## Ketersediaan platform

Eksekusi kode tersedia di:

* **Claude API** (Anthropic)
* **[Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws)**
* **[Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry)** (memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure))

Eksekusi kode saat ini tidak tersedia di Amazon Bedrock atau Google Cloud.

<Note>
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), eksekusi kode hanya didukung di Claude API dan Microsoft Foundry. Fitur ini tidak tersedia untuk Mythos Preview di Amazon Bedrock, Google Cloud, atau Claude Platform on AWS.
</Note>

## Mulai cepat

Berikut adalah contoh sederhana yang meminta Claude untuk melakukan perhitungan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
              }
          ],
          "tools": [{
              "type": "code_execution_20250825",
              "name": "code_execution"
          }]
      }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 4096 \
    --message '{role: user, content: "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"}' \
    --tool '{type: code_execution_20250825, name: code_execution}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
          }
      ],
      Tools = [new ToolUnion(new CodeExecutionTool20250825())]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  	Betas: []anthropic.AnthropicBeta{"code-execution-2025-08-25"},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .addUserMessage("Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
              .addTool(CodeExecutionTool20250825.builder().build())
              .build();

          Message response = client.messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]'
          ]
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'code_execution_20250825',
              'name' => 'code_execution'
          ]
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  )

  puts message
  ```
</CodeGroup>

## Cara kerja eksekusi kode

Ketika Anda menambahkan alat eksekusi kode ke permintaan API Anda:

1. Claude mengevaluasi apakah eksekusi kode akan membantu menjawab pertanyaan Anda

2. Alat ini secara otomatis memberikan Claude kemampuan berikut:

   * **Perintah Bash**: Menjalankan perintah shell untuk operasi sistem dan manajemen paket
   * **Operasi file**: Membuat, melihat, dan mengedit file secara langsung, termasuk menulis kode

3. Claude dapat menggunakan kombinasi apa pun dari kemampuan ini dalam satu permintaan

4. Semua operasi berjalan dalam lingkungan sandbox yang aman

5. Claude memberikan hasil beserta grafik, perhitungan, atau analisis yang dihasilkan

### Kapan Claude menjalankan kode

Claude menjalankan kode ketika permintaan mendapat manfaat dari komputasi atau penanganan file:

* Matematika non-trivial (angka besar, banyak langkah, hasil yang sensitif terhadap presisi)
* Analisis data, parsing file, atau visualisasi
* Eksekusi algoritma atau simulasi
* Permintaan eksplisit untuk "jalankan", "hitung", atau "eksekusi"

Claude menjawab langsung tanpa menjalankan kode untuk:

* Aritmetika sederhana dan fakta matematika yang sudah dikenal luas
* Permintaan faktual, percakapan, atau kreatif
* Konversi unit atau terjemahan sederhana

Jika Anda ingin Claude menjalankan kode untuk permintaan yang berada di batas, minta secara eksplisit (misalnya, "jalankan kode untuk memverifikasi ini").

## Menggunakan eksekusi kode dengan alat eksekusi lainnya

Ketika Anda menyediakan eksekusi kode bersama dengan alat yang disediakan klien yang juga menjalankan kode (seperti [alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) atau REPL kustom), Claude beroperasi dalam lingkungan multi-komputer. Alat eksekusi kode berjalan di kontainer sandbox milik Anthropic, sementara alat yang disediakan klien Anda berjalan di lingkungan terpisah yang Anda kendalikan. Claude terkadang dapat membingungkan lingkungan-lingkungan ini, mencoba menggunakan alat yang salah atau mengasumsikan state dibagikan di antara keduanya.

Untuk menghindari hal ini, tambahkan instruksi ke prompt sistem Anda yang memperjelas perbedaannya:

```text wrap
When multiple code execution environments are available, be aware that:
- Variables, files, and state do NOT persist between different execution environments
- Use the code_execution tool for general-purpose computation in Anthropic's sandboxed environment
- Use client-provided execution tools (e.g., bash) when you need access to the user's local system, files, or data
- If you need to pass results between environments, explicitly include outputs in subsequent tool calls rather than assuming shared state
```

Hal ini sangat penting ketika menggabungkan eksekusi kode dengan [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), yang mengaktifkan eksekusi kode secara otomatis. Jika aplikasi Anda sudah menyediakan alat shell sisi klien, eksekusi kode otomatis menciptakan lingkungan eksekusi kedua yang perlu dibedakan oleh Claude.

## Cara menggunakan alat ini

### Unggah dan analisis file Anda sendiri

Untuk menganalisis file data Anda sendiri (seperti CSV, Excel, atau gambar), unggah melalui Files API dan referensikan dalam permintaan Anda:

<Note>
  Menggunakan Files API dengan Code Execution memerlukan header beta Files API: `"anthropic-beta": "files-api-2025-04-14"`
</Note>

Lingkungan Python dapat memproses berbagai jenis file yang diunggah melalui Files API, termasuk:

* CSV
* Excel (.xlsx, .xls)
* JSON
* XML
* Gambar (JPEG, PNG, GIF, WebP)
* File teks (.txt, .md, .py, dan lainnya)

#### Unggah dan analisis file

1. **Unggah file Anda** menggunakan [Files API](/docs/id/build-with-claude/files)
2. **Referensikan file** dalam pesan Anda menggunakan blok konten `container_upload`
3. **Sertakan alat eksekusi kode** dalam permintaan API Anda

<CodeGroup>
  ```bash cURL
  # Pertama, unggah sebuah file
  curl https://api.anthropic.com/v1/files \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: files-api-2025-04-14" \
      --form 'file=@"data.csv"'

  # Kemudian gunakan file_id dengan eksekusi kode
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: files-api-2025-04-14" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": [
                  {"type": "text", "text": "Analyze this CSV data"},
                  {"type": "container_upload", "file_id": "file_abc123"}
              ]
          }],
          "tools": [{
              "type": "code_execution_20250825",
              "name": "code_execution"
          }]
      }'
  ```

  ```bash CLI
  # Unggah file
  FILE_ID=$(ant beta:files upload \
    --file ./data.csv \
    --transform id --raw-output)

  # Gunakan file_id dengan eksekusi kode
  ant beta:messages create \
    --beta files-api-2025-04-14 <<YAML
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content:
        - type: text
          text: Analyze this CSV data
        - type: container_upload
          file_id: $FILE_ID
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Unggah file
  file_object = client.beta.files.upload(
      file=open("data.csv", "rb"),
  )

  # Gunakan file_id dengan eksekusi kode
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      betas=["files-api-2025-04-14"],
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": "Analyze this CSV data"},
                  {"type": "container_upload", "file_id": file_object.id},
              ],
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  print(response)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import { createReadStream } from "node:fs";

  const client = new Anthropic();
  // ...
    // Unggah file
    const fileObject = await client.beta.files.upload({
      file: await toFile(createReadStream("data.csv"), undefined, { type: "text/csv" })
    });

    // Gunakan file_id dengan eksekusi kode
    const response = await client.beta.messages.create({
      model: "claude-opus-4-8",
      betas: ["files-api-2025-04-14"],
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Analyze this CSV data" },
            { type: "container_upload", file_id: fileObject.id }
          ]
        }
      ],
      tools: [
        {
          type: "code_execution_20250825",
          name: "code_execution"
        }
      ]
    });

    console.log(response);
  ```

  ```csharp C#
  // Unggah file
  var fileObject = await client.Beta.Files.Upload(new FileUploadParams
  {
      File = File.OpenRead("data.csv")
  });

  // Gunakan file_id dengan eksekusi kode
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      Betas = ["files-api-2025-04-14"],
      MaxTokens = 4096,
      Messages = [
          new()
          {
              Role = Role.User,
              Content = [
                  new() { Type = "text", Text = "Analyze this CSV data" },
                  new() { Type = "container_upload", FileId = fileObject.Id }
              ]
          }
      ],
      Tools = [new ToolUnion(new CodeExecutionTool20250825())]
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )
  // ...
  func main() {
  	client := anthropic.NewClient()

  	// Unggah file
  	file, err := os.Open("data.csv")
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer file.Close()

  	fileObject, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
  		File: file,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Gunakan file_id dengan eksekusi kode
  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(
  				anthropic.NewBetaTextBlock("Analyze this CSV data"),
  				anthropic.NewBetaContainerUploadBlock(fileObject.ID),
  			),
  		},
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  		},
  		Betas: []anthropic.AnthropicBeta{
  			"code-execution-2025-08-25",
  			anthropic.AnthropicBetaFilesAPI2025_04_14,
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fmt.Println(response)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.files.FileMetadata;
  import com.anthropic.models.beta.files.FileUploadParams;
  // ...
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  // ...
  import com.anthropic.models.beta.messages.BetaContainerUploadBlockParam;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          // Unggah file
          FileMetadata fileMetadata = client.beta().files().upload(
              FileUploadParams.builder()
                  .file(Paths.get("data.csv"))
                  .build()
          );

          // Gunakan file_id dengan eksekusi kode
          BetaMessage response = client.beta().messages().create(
              MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .addBeta("files-api-2025-04-14")
                  .maxTokens(4096L)
                  .addUserMessageOfBetaContentBlockParams(List.of(
                      BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
                          .text("Analyze this CSV data")
                          .build()),
                      BetaContentBlockParam.ofContainerUpload(BetaContainerUploadBlockParam.builder()
                          .fileId(fileMetadata.id())
                          .build())
                  ))
                  .addTool(BetaCodeExecutionTool20250825.builder().build())
                  .build()
          );

          System.out.println(response);
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  // Unggah file
  $fileObject = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('data.csv', 'r')),
  );

  // Gunakan file_id dengan eksekusi kode
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  ['type' => 'text', 'text' => 'Analyze this CSV data'],
                  ['type' => 'container_upload', 'file_id' => $fileObject->id],
              ],
          ],
      ],
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution'],
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Unggah file
  file_object = client.beta.files.upload(
    file: File.open("data.csv", "rb")
  )

  # Gunakan file_id dengan eksekusi kode
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    betas: ["files-api-2025-04-14"],
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Analyze this CSV data" },
          { type: "container_upload", file_id: file_object.id }
        ]
      }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  puts response
  ```
</CodeGroup>

### Mengambil file yang dihasilkan

Ketika Claude membuat file selama eksekusi kode, Anda dapat mengambil file-file ini menggunakan Files API:

<CodeGroup>
  ```bash CLI
  # Minta eksekusi kode yang membuat file; ekstrak file_id dari hasil alat
  TOOL_RESULT='content.#(type=="bash_code_execution_tool_result")#'
  FILE_IDS=$(ant beta:messages create \
    --beta files-api-2025-04-14 \
    --transform "${TOOL_RESULT}.content.content|@flatten|#.file_id" \
    --format yaml \
      --model claude-opus-4-8 \
      --max-tokens 4096 \
      --message '{role: user, content: Create a matplotlib visualization and save it as output.png}' \
      --tool '{type: code_execution_20250825, name: code_execution}'
  )

  # Unduh setiap file yang dibuat
  while IFS= read -r LINE; do
    [[ "$LINE" != "- "* ]] && continue
    FILE_ID="${LINE#- }"
    FILENAME=$(ant beta:files retrieve-metadata \
      --file-id "$FILE_ID" \
      --transform filename --raw-output)
    ant beta:files download \
      --file-id "$FILE_ID" \
      --output "$FILENAME" > /dev/null
    printf 'Downloaded: %s\n' "$FILENAME"
  done <<< "$FILE_IDS"
  ```

  ```python Python
  # Inisialisasi klien
  client = Anthropic()

  # Minta eksekusi kode yang membuat file
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      betas=["files-api-2025-04-14"],
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Create a matplotlib visualization and save it as output.png",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )


  # Ekstrak ID file dari respons
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == "bash_code_execution_tool_result":
              content_item = item.content
              if content_item.type == "bash_code_execution_result":
                  # list bertipe konkret: List[BashCodeExecutionOutputBlock]
                  for file in content_item.content:
                      file_ids.append(file.file_id)
      return file_ids


  # Unduh file yang dibuat
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(file_id)
      file_content = client.beta.files.download(file_id)
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();
  // ...
    // Minta eksekusi kode yang membuat file
    const response = await client.beta.messages.create({
      model: "claude-opus-4-8",
      betas: ["files-api-2025-04-14"],
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: "Create a matplotlib visualization and save it as output.png"
        }
      ],
      tools: [
        {
          type: "code_execution_20250825",
          name: "code_execution"
        }
      ]
    });

    // Ekstrak ID file dari respons
    for (const item of response.content) {
      if (item.type === "bash_code_execution_tool_result") {
        const contentItem = item.content;
        if (contentItem.type === "bash_code_execution_result" && contentItem.content) {
          // list bertipe konkret: BashCodeExecutionOutputBlock
          for (const file of contentItem.content) {
            const fileMetadata = await client.beta.files.retrieveMetadata(file.file_id);
            const fileResponse = await client.beta.files.download(file.file_id);
            const fileBytes = Buffer.from(await fileResponse.arrayBuffer());
            await writeFile(fileMetadata.filename, fileBytes);
            console.log(`Downloaded: ${fileMetadata.filename}`);
          }
        }
      }
    }
  ```

  ```csharp C#
      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 4096,
          Messages = [
              new() {
                  Role = Role.User,
                  Content = "Create a matplotlib visualization and save it as output.png"
              }
          ],
          Tools = [new ToolUnion(new CodeExecutionTool20250825())]
      };

      var response = await client.Beta.Messages.Create(parameters, ["files-api-2025-04-14"]);

      var fileIds = ExtractFileIds(response);

      foreach (var fileId in fileIds)
      {
          var fileMetadata = await client.Beta.Files.RetrieveMetadata(fileId);
          var fileContent = await client.Beta.Files.Download(fileId);

          await File.WriteAllBytesAsync(fileMetadata.Filename, fileContent);
          Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
      }
  }

  static List<string> ExtractFileIds(dynamic response)
  {
      var fileIds = new List<string>();
      foreach (var item in response.Content)
      {
          if (item.Type == "bash_code_execution_tool_result")
          {
              var contentItem = item.Content;
              if (contentItem.Type == "bash_code_execution_result")
              {
                  // daftar bertipe konkret: BetaBashCodeExecutionOutputBlock
                  foreach (var file in contentItem.Content)
                  {
                      if (file.FileId != null)
                      {
                          fileIds.Add(file.FileId);
                      }
                  }
              }
          }
      }
      return fileIds;
  ```

  ```go Go
  	client := anthropic.NewClient()

  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a matplotlib visualization and save it as output.png")),
  		},
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  		},
  		Betas: []anthropic.AnthropicBeta{
  			"code-execution-2025-08-25",
  			anthropic.AnthropicBetaFilesAPI2025_04_14,
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fileIDs := extractFileIDs(response)

  	for _, fileID := range fileIDs {
  		fileMetadata, err := client.Beta.Files.GetMetadata(context.TODO(), fileID, anthropic.BetaFileGetMetadataParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		fileContent, err := client.Beta.Files.Download(context.TODO(), fileID, anthropic.BetaFileDownloadParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		outFile, err := os.Create(fileMetadata.Filename)
  		if err != nil {
  			log.Fatal(err)
  		}

  		_, err = io.Copy(outFile, fileContent.Body)
  		if err != nil {
  			log.Fatal(err)
  		}
  		outFile.Close()
  		fileContent.Body.Close()

  		fmt.Printf("Downloaded: %s\n", fileMetadata.Filename)
  	}
  // ...
  func extractFileIDs(response *anthropic.BetaMessage) []string {
  	var fileIDs []string
  	for _, item := range response.Content {
  		switch variant := item.AsAny().(type) {
  		case anthropic.BetaBashCodeExecutionToolResultBlock:
  			// list bertipe konkret: BashCodeExecutionOutputBlock
  			for _, file := range variant.Content.Content {
  				if file.FileID != "" {
  					fileIDs = append(fileIDs, file.FileID)
  				}
  			}
  		}
  	}
  	return fileIDs
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaCodeExecutionTool20250825;
  import com.anthropic.models.beta.messages.BetaBashCodeExecutionResultBlock;
  import com.anthropic.models.beta.messages.BetaBashCodeExecutionOutputBlock;
  import com.anthropic.models.beta.files.FileMetadata;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-opus-4-8")
          .addBeta("files-api-2025-04-14")
          .maxTokens(4096L)
          .addUserMessage("Create a matplotlib visualization and save it as output.png")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);

      List<String> fileIds = extractFileIds(response);

      for (String fileId : fileIds) {
          FileMetadata fileMetadata = client.beta().files().retrieveMetadata(fileId);
          try (HttpResponse fileContent = client.beta().files().download(fileId)) {
              try (FileOutputStream fos = new FileOutputStream(fileMetadata.filename())) {
                  fileContent.body().transferTo(fos);
              }
          }
          IO.println("Downloaded: " + fileMetadata.filename());
      }
  // ...
  List<String> extractFileIds(BetaMessage response) {
      List<String> fileIds = new ArrayList<>();
      // .ifPresent() adalah guard diskriminator (tidak bertipe konkret; scanner tidak bisa melihat guard lambda)
      for (BetaContentBlock item : response.content()) {
          item.bashCodeExecutionToolResult().ifPresent(toolResult -> {
              if (toolResult.content().isBetaBashCodeExecutionResultBlock()) {
                  BetaBashCodeExecutionResultBlock result =
                      toolResult.content().asBetaBashCodeExecutionResultBlock();
                  // list bertipe konkret: BetaBashCodeExecutionOutputBlock
                  for (BetaBashCodeExecutionOutputBlock output : result.content()) {
                      fileIds.add(output.fileId());
                  }
              }
          });
      }
      return fileIds;
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaMessage;
  // ...
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a matplotlib visualization and save it as output.png',
          ],
      ],
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
      tools: [
          [
              'type' => 'code_execution_20250825',
              'name' => 'code_execution',
          ],
      ],
  );

  function extractFileIds(BetaMessage $response): array
  {
      $fileIds = [];
      foreach ($response->content as $item) {
          if ($item->type !== 'bash_code_execution_tool_result') {
              continue;
          }
          $contentItem = $item->content;
          if ($contentItem->type !== 'bash_code_execution_result') {
              continue;
          }
          // list bertipe konkret: BashCodeExecutionOutputBlock
          foreach ($contentItem->content as $file) {
              $fileIds[] = $file->fileID;
          }
      }
      return $fileIds;
  }

  foreach (extractFileIds($response) as $fileId) {
      $fileMetadata = $client->beta->files->retrieveMetadata($fileId);
      $fileContent = $client->beta->files->download($fileId);

      file_put_contents($fileMetadata->filename, $fileContent);
      echo "Downloaded: {$fileMetadata->filename}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    betas: ["files-api-2025-04-14"],
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Create a matplotlib visualization and save it as output.png"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  )

  def extract_file_ids(response)
    file_ids = []
    response.content.each do |item|
      if item.type == :bash_code_execution_tool_result
        content_item = item.content
        if content_item.type == :bash_code_execution_result
          # list bertipe konkret: BashCodeExecutionOutputBlock
          content_item.content.each do |file|
            file_ids << file.file_id
          end
        end
      end
    end
    file_ids
  end

  extract_file_ids(response).each do |file_id|
    file_metadata = client.beta.files.retrieve_metadata(file_id)
    file_content = client.beta.files.download(file_id)

    File.open(file_metadata.filename, "wb") do |f|
      f.write(file_content.read)
    end

    puts "Downloaded: #{file_metadata.filename}"
  end
  ```
</CodeGroup>

## Definisi alat

Alat eksekusi kode tidak memerlukan parameter tambahan:

```json JSON
{
  "type": "code_execution_20250825",
  "name": "code_execution"
}
```

Ketika alat ini disediakan, Claude secara otomatis mendapatkan akses ke dua sub-alat:

* `bash_code_execution`: Menjalankan perintah shell
* `text_editor_code_execution`: Melihat, membuat, dan mengedit file, termasuk menulis kode

## Format respons

Alat eksekusi kode dapat mengembalikan dua jenis hasil tergantung pada operasinya:

### Respons perintah Bash

```json Output
{
  "type": "server_tool_use",
  "id": "srvtoolu_01B3C4D5E6F7G8H9I0J1K2L3",
  "name": "bash_code_execution",
  "input": {
    "command": "ls -la | head -5"
  }
},
{
  "type": "bash_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01B3C4D5E6F7G8H9I0J1K2L3",
  "content": {
    "type": "bash_code_execution_result",
    "stdout": "total 24\ndrwxr-xr-x 2 user user 4096 Jan 1 12:00 .\ndrwxr-xr-x 3 user user 4096 Jan 1 11:00 ..\n-rw-r--r-- 1 user user  220 Jan 1 12:00 data.csv\n-rw-r--r-- 1 user user  180 Jan 1 12:00 config.json",
    "stderr": "",
    "return_code": 0
  }
}
```

### Respons operasi file

**Melihat file:**

```json Output
{
  "type": "server_tool_use",
  "id": "srvtoolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "name": "text_editor_code_execution",
  "input": {
    "command": "view",
    "path": "config.json"
  }
},
{
  "type": "text_editor_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": {
    "type": "text_editor_code_execution_result",
    "file_type": "text",
    "content": "{\n  \"setting\": \"value\",\n  \"debug\": true\n}",
    "numLines": 4,
    "startLine": 1,
    "totalLines": 4
  }
}
```

**Membuat file:**

```json Output
{
  "type": "server_tool_use",
  "id": "srvtoolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "name": "text_editor_code_execution",
  "input": {
    "command": "create",
    "path": "new_file.txt",
    "file_text": "Hello, World!"
  }
},
{
  "type": "text_editor_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "content": {
    "type": "text_editor_code_execution_result",
    "is_file_update": false
  }
}
```

**Mengedit file (str\_replace):**

```json Output
{
  "type": "server_tool_use",
  "id": "srvtoolu_01E6F7G8H9I0J1K2L3M4N5O6",
  "name": "text_editor_code_execution",
  "input": {
    "command": "str_replace",
    "path": "config.json",
    "old_str": "\"debug\": true",
    "new_str": "\"debug\": false"
  }
},
{
  "type": "text_editor_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01E6F7G8H9I0J1K2L3M4N5O6",
  "content": {
    "type": "text_editor_code_execution_result",
    "oldStart": 3,
    "oldLines": 1,
    "newStart": 3,
    "newLines": 1,
    "lines": ["-  \"debug\": true", "+  \"debug\": false"]
  }
}
```

### Hasil

Semua hasil eksekusi mencakup:

* `stdout`: Output dari eksekusi yang berhasil
* `stderr`: Pesan error jika eksekusi gagal
* `return_code`: 0 untuk berhasil, bukan nol untuk gagal

Field tambahan untuk operasi file:

* **View**: `file_type`, `content`, `numLines`, `startLine`, `totalLines`
* **Create**: `is_file_update` (apakah file sudah ada sebelumnya)
* **Edit**: `oldStart`, `oldLines`, `newStart`, `newLines`, `lines` (format diff)

### Error

Setiap jenis alat dapat mengembalikan error tertentu:

**Error umum (semua alat):**

```json Output
{
  "type": "bash_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01VfmxgZ46TiHbmXgy928hQR",
  "content": {
    "type": "bash_code_execution_tool_result_error",
    "error_code": "unavailable"
  }
}
```

**Kode error berdasarkan jenis alat:**

| Alat         | Kode Error                | Deskripsi                                                 |
| ------------ | ------------------------- | --------------------------------------------------------- |
| Semua alat   | `unavailable`             | Alat sementara tidak tersedia                             |
| Semua alat   | `execution_time_exceeded` | Eksekusi melebihi batas waktu maksimum                    |
| Semua alat   | `container_expired`       | Kontainer kedaluwarsa dan tidak lagi tersedia             |
| Semua alat   | `invalid_tool_input`      | Parameter yang diberikan ke alat tidak valid              |
| Semua alat   | `too_many_requests`       | Batas laju terlampaui untuk penggunaan alat               |
| bash         | `output_file_too_large`   | Output perintah melebihi ukuran maksimum                  |
| text\_editor | `file_not_found`          | File tidak ada (untuk operasi view/edit)                  |
| text\_editor | `string_not_found`        | `old_str` tidak ditemukan dalam file (untuk str\_replace) |

#### Stop reason `pause_turn`

Respons dapat menyertakan stop reason `pause_turn`, yang menunjukkan bahwa API menjeda giliran yang berjalan lama. Anda dapat memberikan respons kembali apa adanya dalam permintaan berikutnya agar Claude melanjutkan gilirannya, atau memodifikasi konten jika Anda ingin menginterupsi percakapan.

## Kontainer

Alat eksekusi kode berjalan dalam lingkungan terkontainerisasi yang aman, dirancang khusus untuk eksekusi kode, dengan fokus lebih tinggi pada Python.

### Lingkungan runtime

* **Versi Python**: 3.11.12
* **Sistem operasi**: Kontainer berbasis Linux
* **Arsitektur**: x86\_64 (AMD64)

### Batas sumber daya

* **Memori**: 5GiB RAM
* **Ruang disk**: 5GiB penyimpanan workspace
* **CPU**: 1 CPU

### Jaringan dan keamanan

* **Akses internet**: Sepenuhnya dinonaktifkan demi keamanan
* **Koneksi eksternal**: Tidak ada permintaan jaringan keluar yang diizinkan
* **Isolasi sandbox**: Isolasi penuh dari sistem host dan kontainer lainnya
* **Akses file**: Terbatas hanya pada direktori workspace
* **Cakupan workspace**: Seperti [Files](/docs/id/build-with-claude/files), kontainer dicakup ke workspace dari kunci API
* **Kedaluwarsa**: Kontainer kedaluwarsa 30 hari setelah dibuat

### Library yang sudah terinstal

Lingkungan Python sandbox mencakup library yang umum digunakan berikut:

* **Data Science**: pandas, numpy, scipy, scikit-learn, statsmodels
* **Visualisasi**: matplotlib, seaborn
* **Pemrosesan File**: pyarrow, openpyxl, xlsxwriter, xlrd, pillow, python-pptx, python-docx, pypdf, pdfplumber, pypdfium2, pdf2image, pdfkit, tabula-py, reportlab\[pycairo], Img2pdf
* **Matematika & Komputasi**: sympy, mpmath
* **Utilitas**: tqdm, python-dateutil, pytz, joblib, unzip, unrar, 7zip, bc, rg (ripgrep), fd, sqlite

## Penggunaan ulang kontainer

Anda dapat menggunakan kembali kontainer yang ada di beberapa permintaan API dengan memberikan ID kontainer dari respons sebelumnya. Ini memungkinkan Anda mempertahankan file yang dibuat di antara permintaan.

### Contoh

<CodeGroup>
  ```bash cURL
  # Permintaan pertama: Buat file dengan angka acak
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": "Write a file with a random number and save it to \"/tmp/number.txt\""
          }],
          "tools": [{
              "type": "code_execution_20250825",
              "name": "code_execution"
          }]
      }' > response1.json

  # Ekstrak ID kontainer dari respons (menggunakan jq)
  CONTAINER_ID=$(jq -r '.container.id' response1.json)

  # Permintaan kedua: Gunakan kembali kontainer untuk membaca file
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "container": "'$CONTAINER_ID'",
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": "Read the number from \"/tmp/number.txt\" and calculate its square"
          }],
          "tools": [{
              "type": "code_execution_20250825",
              "name": "code_execution"
          }]
      }'
  ```

  ```bash CLI
  # Permintaan pertama: Buat file dengan angka acak
  CONTAINER_ID=$(ant messages create \
    --transform container.id --raw-output \
      --model claude-opus-4-8 \
      --max-tokens 4096 \
      --message '{role: user, content: Write a file with a random number and save it to "/tmp/number.txt"}' \
      --tool '{type: code_execution_20250825, name: code_execution}'
  )

  # Permintaan kedua: Gunakan kembali kontainer untuk membaca file
  ant messages create --container "$CONTAINER_ID" \
    --model claude-opus-4-8 \
    --max-tokens 4096 \
    --message '{role: user, content: Read the number from "/tmp/number.txt" and calculate its square}' \
    --tool '{type: code_execution_20250825, name: code_execution}'
  ```

  ```python Python
  # Permintaan pertama: Buat file dengan angka acak
  response1 = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Write a file with a random number and save it to '/tmp/number.txt'",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Ekstrak ID kontainer dari respons pertama
  container_id = response1.container.id

  # Permintaan kedua: Gunakan kembali kontainer untuk membaca file
  response2 = client.messages.create(
      container=container_id,  # Reuse the same container
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Read the number from '/tmp/number.txt' and calculate its square",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  print(response2)
  ```

  ```typescript TypeScript
  // Permintaan pertama: Buat file dengan angka acak
  const response1 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    betas: ["code-execution-2025-08-25"],
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Write a file with a random number and save it to '/tmp/number.txt'"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });

  // Ekstrak ID kontainer dari respons pertama
  const containerId = response1.container!.id;

  // Permintaan kedua: Gunakan kembali kontainer untuk membaca file
  const response2 = await client.beta.messages.create({
    container: containerId,
    model: "claude-opus-4-8",
    betas: ["code-execution-2025-08-25"],
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Read the number from '/tmp/number.txt' and calculate its square"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });

  console.log(response2.content);
  ```

  ```csharp C#
  var parameters1 = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Write a file with a random number and save it to '/tmp/number.txt'" }],
      Tools = [new ToolUnion(new CodeExecutionTool20250825())]
  };

  var response1 = await client.Messages.Create(parameters1);
  var containerId = response1.Container!.ID;

  var parameters2 = new MessageCreateParams
  {
      Container = containerId,
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Read the number from '/tmp/number.txt' and calculate its square" }],
      Tools = [new ToolUnion(new CodeExecutionTool20250825())]
  };

  var response2 = await client.Messages.Create(parameters2);
  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()

  response1, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Write a file with a random number and save it to '/tmp/number.txt'")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  	Betas: []anthropic.AnthropicBeta{"code-execution-2025-08-25"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  containerID := response1.Container.ID

  response2, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfString: anthropic.String(containerID),
  	},
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Read the number from '/tmp/number.txt' and calculate its square")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  	},
  	Betas: []anthropic.AnthropicBeta{"code-execution-2025-08-25"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response2.Content {
  	if block.Type == "text" {
  		fmt.Println(block.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params1 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .addUserMessage("Write a file with a random number and save it to '/tmp/number.txt'")
              .addTool(CodeExecutionTool20250825.builder().build())
              .build();

          Message response1 = client.messages().create(params1);
          String containerId = response1.container().get().id();

          MessageCreateParams params2 = MessageCreateParams.builder()
              .container(containerId)
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .addUserMessage("Read the number from '/tmp/number.txt' and calculate its square")
              .addTool(CodeExecutionTool20250825.builder().build())
              .build();

          Message response2 = client.messages().create(params2);
          System.out.println(response2);
  ```

  ```php PHP
  $client = new Client();

  $response1 = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => "Write a file with a random number and save it to '/tmp/number.txt'"]
      ],
      model: 'claude-opus-4-8',
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ],
  );

  $containerId = $response1->container->id;

  $response2 = $client->messages->create(
      container: $containerId,
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => "Read the number from '/tmp/number.txt' and calculate its square"]
      ],
      model: 'claude-opus-4-8',
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response1 = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Write a file with a random number and save it to '/tmp/number.txt'" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  container_id = response1.container.id

  response2 = client.messages.create(
    container: container_id,
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Read the number from '/tmp/number.txt' and calculate its square" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  puts response2.content
  ```
</CodeGroup>

## Streaming

Dengan streaming diaktifkan, Anda akan menerima event eksekusi kode saat terjadi:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "code_execution"}}

// Code execution streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"code\":\"import pandas as pd\\ndf = pd.read_csv('data.csv')\\nprint(df.head())\"}"}}

// Pause while code executes

// Execution results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "code_execution_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"stdout": "   A  B  C\n0  1  2  3\n1  4  5  6", "stderr": ""}}}
```

## Permintaan batch

Anda dapat menyertakan alat eksekusi kode dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat eksekusi kode melalui Messages Batches API dikenakan harga yang sama dengan permintaan Messages API reguler.

## Penggunaan dan harga

**Code execution gratis ketika digunakan bersama web search atau web fetch.** Ketika `web_search_20260209` (atau versi lebih baru) atau `web_fetch_20260209` (atau versi lebih baru) disertakan dalam permintaan API Anda, tidak ada biaya tambahan untuk panggilan alat code execution selain biaya token input dan output standar.

Ketika digunakan tanpa alat-alat tersebut, code execution ditagih berdasarkan waktu eksekusi, yang dilacak secara terpisah dari penggunaan token:

* Waktu eksekusi memiliki minimum 5 menit
* Setiap organisasi menerima **1.550 jam gratis** penggunaan per bulan
* Penggunaan tambahan di luar 1.550 jam ditagih sebesar **$0,05 per jam, per kontainer**
* Jika file disertakan dalam permintaan, waktu eksekusi tetap ditagih meskipun alat tidak dipanggil, karena file dimuat terlebih dahulu ke dalam kontainer

Penggunaan code execution dilacak dalam respons:

```json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
}
```

## Upgrade ke versi alat terbaru

Dengan melakukan upgrade ke `code-execution-2025-08-25`, Anda mendapatkan akses ke kemampuan manipulasi file dan Bash, termasuk kode dalam berbagai bahasa. Tidak ada perbedaan harga.

### Apa yang berubah

| Komponen     | Lama                        | Saat ini                                                          |
| ------------ | --------------------------- | ----------------------------------------------------------------- |
| Header beta  | `code-execution-2025-05-22` | `code-execution-2025-08-25`                                       |
| Tipe alat    | `code_execution_20250522`   | `code_execution_20250825`                                         |
| Kemampuan    | Hanya Python                | Perintah Bash, operasi file                                       |
| Tipe respons | `code_execution_result`     | `bash_code_execution_result`, `text_editor_code_execution_result` |

### Kompatibilitas mundur

* Semua eksekusi kode Python yang ada terus berfungsi persis seperti sebelumnya
* Tidak ada perubahan yang diperlukan untuk alur kerja yang hanya menggunakan Python

### Langkah-langkah upgrade

Untuk melakukan upgrade, perbarui tipe alat dalam permintaan API Anda:

```diff
- "type": "code_execution_20250522"
+ "type": "code_execution_20250825"
```

**Tinjau penanganan respons** (jika mem-parsing respons secara programatik):

* Blok sebelumnya untuk respons eksekusi Python tidak akan lagi dikirim
* Sebagai gantinya, tipe respons baru untuk Bash dan operasi file akan dikirim (lihat bagian Format Respons)

## Pemanggilan alat secara programatik

Untuk menjalankan alat di dalam kontainer eksekusi kode, lihat [Pemanggilan alat secara programatik](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling).

## Retensi data

Eksekusi kode berjalan dalam kontainer sandbox sisi server. Data kontainer, termasuk artefak eksekusi, file yang diunggah, dan output, disimpan hingga 30 hari. Retensi ini berlaku untuk semua data yang diproses dalam lingkungan kontainer. File yang dibuat oleh eksekusi kode di [Files API](/docs/id/build-with-claude/files) (dapat diambil melalui `client.beta.files.download()`) tetap ada hingga dihapus secara eksplisit.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Menggunakan eksekusi kode dengan Agent Skills

Alat eksekusi kode memungkinkan Claude menggunakan [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview). Skills adalah kemampuan modular yang terdiri dari instruksi, skrip, dan sumber daya yang memperluas fungsionalitas Claude.

Pelajari lebih lanjut di [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [Menggunakan Agent Skills dengan API](/docs/id/build-with-claude/skills-guide).
