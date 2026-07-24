---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: df7b14d413f837a84eccbc4493b9f167536979b9b627cb580c1cf0a7d0bf03e8
---

# Alat eksekusi kode

Jalankan kode Python dan bash dalam kontainer sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.

---

Claude dapat menganalisis data, membuat visualisasi, melakukan perhitungan kompleks, menjalankan perintah sistem, membuat dan mengedit file, serta memproses file yang diunggah langsung dalam percakapan API. Alat eksekusi kode memungkinkan Claude menjalankan perintah Bash dan memanipulasi file, termasuk menulis kode, dalam lingkungan yang aman dan ter-sandbox.

**Eksekusi kode gratis saat digunakan dengan web search atau web fetch (`web_search_20260209`, `web_fetch_20260209`, atau yang lebih baru).** Ketika salah satu alat tersebut ada dalam permintaan Anda, tidak ada biaya tambahan untuk eksekusi kode dalam permintaan tersebut di luar biaya token standar. Ini mencakup eksekusi kode di balik pemfilteran dinamis maupun kode apa pun yang dijalankan Claude secara langsung. Harga eksekusi kode standar berlaku ketika alat-alat tersebut tidak disertakan.

Eksekusi kode juga mendukung pemfilteran dinamis pada alat [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) dan [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool): Claude memfilter hasil di dalam lingkungan eksekusi kode sebelum hasil tersebut mencapai jendela konteks. Ketika pemfilteran dinamis berjalan, API secara otomatis menyediakan eksekusi kode yang dibutuhkan untuk permintaan tersebut, sehingga Anda tidak perlu menambahkan alat eksekusi kode ke permintaan Anda untuk itu.

<Note>
  Hubungi kami melalui [formulir umpan balik](https://forms.gle/LTAU6Xn2puCJMi1n6) untuk membagikan umpan balik Anda tentang fitur ini.
</Note>

<Note>
  Untuk mengetahui bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Kompatibilitas model

Alat eksekusi kode tersedia pada model-model berikut:

| Model                                                                                                                                  | Versi alat                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Claude Fable 5 (claude-fable-5)                                                                                                        | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Mythos 5 (claude-mythos-5)                                                                                                      | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 5 (claude-sonnet-5)                                                                                                      | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.8 (claude-opus-4-8)                                                                                                      | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.7 (claude-opus-4-7)                                                                                                      | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.6 (claude-opus-4-6)                                                                                                      | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 4.6 (claude-sonnet-4-6)                                                                                                  | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.5 (claude-opus-4-5-20251101)                                                                                             | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)                                                                                         | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001)                                                                                           | `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` |
| Claude Opus 4.1 (claude-opus-4-1-20250805) (tidak digunakan lagi, lihat [Penghentian model](/docs/id/about-claude/model-deprecations)) | `code_execution_20250825`                                                       |

Setiap versi alat dibangun di atas versi sebelumnya:

* `code_execution_20250825` mendukung perintah Bash dan operasi file serta tersedia pada setiap model dalam tabel.
* `code_execution_20260120` menambahkan persistensi state REPL dan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox. Claude Haiku 4.5 menerima tipe alat `code_execution_20260120` dan `code_execution_20260521`, tetapi pemanggilan alat terprogram dan persistensi state REPL yang bergantung padanya tidak tersedia di model tersebut, sehingga versi yang lebih baru berperilaku seperti `code_execution_20250825` di sana.
* `code_execution_20260521` adalah runtime yang sama dengan `code_execution_20260120`. Perbedaannya adalah deskripsi alat memberi tahu Claude tentang batas waktu nyata (wall-clock) 90 detik pada setiap sel Python dalam pemanggilan alat terprogram, sehingga Claude dapat mengatur anggaran untuk sel yang berjalan lama. Sel yang melebihi batas mengembalikan hasil eksekusi kode normal dengan `return_code` bukan nol dan pesan status `detection_timeout` dalam outputnya. Ini terpisah dari [kode kesalahan](#errors) `execution_time_exceeded`, yang dikembalikan API ketika seluruh pemanggilan alat melebihi waktu eksekusi maksimum.

Ketiga versi alat tersedia secara umum dan tidak memerlukan header `anthropic-beta`. Header beta eksekusi kode lama tetap merupakan opt-in yang valid.

Contoh-contoh di halaman ini menggunakan `code_execution_20250825` karena setiap model dalam tabel mendukungnya. Alat [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) dan [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool) saat ini (`web_search_20260209`, `web_fetch_20260209`, dan yang lebih baru) memerlukan `code_execution_20260120` atau yang lebih baru sebagai versi eksekusi kodenya.

<Note>
  Jika Anda masih menggunakan `code_execution_20250522` lama (hanya Python), lihat [Tingkatkan ke versi alat terbaru](#upgrade-to-latest-tool-version) untuk bermigrasi darinya.
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
  Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), eksekusi kode hanya didukung di Claude API dan Microsoft Foundry. Fitur ini tidak tersedia untuk Mythos Preview di Amazon Bedrock, Claude Platform on AWS, atau Google Cloud.
</Note>

## Mulai cepat

Berikut adalah contoh yang meminta Claude melakukan perhitungan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        }
      ],
      "tools": [
        {
          "type": "code_execution_20250825",
          "name": "code_execution"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 4096 \
    --message '{
      role: user,
      content: "Use the code execution tool to calculate the mean and standard
        deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
    }' \
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
              "content": "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  print(response.to_json())
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  console.log(JSON.stringify(response));
  ```

  ```csharp C#
  AnthropicClient client = new();

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" }],
      Tools = [new CodeExecutionTool20250825()]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(4096L)
      .addUserMessage("Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message response = client.messages().create(params);
  IO.println(ObjectMappers.jsonMapper().valueToTree(response));
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]',
          ],
      ],
      model: Model::CLAUDE_OPUS_4_8,
      tools: [new CodeExecutionTool20250825()],
  );

  echo json_encode($message, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      }
    ],
    tools: [Anthropic::CodeExecutionTool20250825.new]
  )

  puts message.to_json
  ```
</CodeGroup>

Respons menyisipkan blok `server_tool_use` (perintah yang dijalankan Claude) secara bergantian dengan blok hasil alatnya, diikuti oleh teks Claude. Tingkat teratas juga menyertakan objek `container` yang `id`-nya dapat Anda [gunakan kembali di berbagai permintaan](#container-reuse). Lihat [Format respons](#response-format) untuk bentuk bloknya.

## Cara kerja eksekusi kode

Ketika Anda menambahkan alat eksekusi kode ke permintaan API Anda:

1. Claude mengevaluasi apakah eksekusi kode akan membantu menjawab pertanyaan Anda

2. Alat ini secara otomatis memberi Claude kemampuan berikut:

   * **Perintah Bash:** Menjalankan perintah shell untuk operasi sistem
   * **Operasi file:** Membuat, melihat, dan mengedit file secara langsung, termasuk menulis kode

3. Claude dapat menggunakan kombinasi apa pun dari kemampuan ini dalam satu permintaan

4. Semua operasi berjalan dalam kontainer yang aman dan ter-sandbox. Kontainer tidak memiliki akses internet, sehingga Claude tidak dapat mengunduh paket saat runtime: hanya [pustaka yang sudah terpasang](#pre-installed-libraries) yang tersedia

5. API menjalankan setiap perintah di sisi server dan mengembalikan hasilnya ke Claude dalam permintaan yang sama, sehingga Anda tidak pernah mengeksekusi kode atau mengirim kembali blok `tool_result` sendiri. Satu pengecualian adalah ketika Claude memanggil salah satu alat klien Anda bersamaan dengan eksekusi kode: API mengembalikan panggilan eksekusi kode tanpa hasilnya. Hasilnya tiba dalam respons berikutnya, setelah Anda mengirim kembali blok `tool_result` untuk alat klien Anda

6. Setiap permintaan berjalan dalam kontainer baru kecuali Anda mengirimkan kembali ID kontainer dari respons sebelumnya (lihat [Penggunaan kembali kontainer](#container-reuse))

7. Claude memberikan hasil beserta grafik, perhitungan, atau analisis yang dihasilkan

Kontainer sudah memiliki Python terpasang. Claude menulis Python dengan sub-alat operasi file dan menjalankannya dengan perintah Bash. Dengan `code_execution_20260120` atau yang lebih baru dan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), state interpreter Python (seperti binding variabel) juga bertahan di seluruh permintaan yang menggunakan kembali kontainer tersebut.

### Kapan Claude menjalankan kode

Claude menjalankan kode ketika permintaan mendapat manfaat dari komputasi atau penanganan file:

* Matematika yang tidak sepele (angka besar, banyak langkah, hasil yang sensitif terhadap presisi)
* Analisis data, parsing file, atau visualisasi
* Eksekusi algoritma atau simulasi
* Permintaan eksplisit untuk "run", "compute", atau "execute"

Claude menjawab langsung tanpa menjalankan kode untuk:

* Aritmetika sederhana dan fakta matematika yang sudah dikenal luas
* Permintaan faktual, percakapan, atau kreatif
* Konversi satuan atau terjemahan sederhana

Jika Anda ingin Claude menjalankan kode untuk permintaan yang ambigu, mintalah secara eksplisit (misalnya, "jalankan kode untuk memverifikasi ini").

## Bekerja dengan file

### Unggah dan analisis file Anda sendiri

Untuk menganalisis file data Anda sendiri (seperti CSV, Excel, atau gambar), unggah melalui Files API dan referensikan dalam permintaan Anda:

<Note>
  Menggunakan Files API dengan eksekusi kode memerlukan header beta Files API: `"anthropic-beta": "files-api-2025-04-14"`
</Note>

Lingkungan Python dapat memproses berbagai tipe file yang diunggah melalui Files API, termasuk:

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
  # Pertama, unggah file dan ambil ID file-nya (menggunakan jq)
  FILE_ID=$(curl --fail-with-body -sS https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@data.csv" | jq -r '.id')

  # Kemudian gunakan file_id dengan eksekusi kode
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [{
        "role": "user",
        "content": [
          {"type": "text", "text": "Analyze this CSV data"},
          {"type": "container_upload", "file_id": "'"$FILE_ID"'"}
        ]
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```

  ```bash CLI
  # Pertama, unggah file dan simpan ID file-nya
  FILE_ID=$(ant beta:files upload \
    --file ./data.csv \
    --transform id --raw-output)

  # Kemudian gunakan file_id dengan eksekusi kode
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
  file_object = client.beta.files.upload(file=Path("data.csv"))

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

  print(response.to_json())
  ```

  ```typescript TypeScript
  import { createReadStream } from "node:fs";
  // ...
  const client = new Anthropic();

  // Unggah file
  const fileObject = await client.beta.files.upload({
    file: createReadStream("data.csv")
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

  console.log(JSON.stringify(response));
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Mengunggah file
  var fileObject = await client.Beta.Files.Upload(new FileUploadParams
  {
      File = File.OpenRead("data.csv")
  });

  // Gunakan file_id dengan eksekusi kode
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Betas = [AnthropicBeta.FilesApi2025_04_14],
      Messages = [
          new()
          {
              Role = Role.User,
              Content = new([
                  new BetaTextBlockParam { Text = "Analyze this CSV data" },
                  new BetaContainerUploadBlockParam { FileID = fileObject.ID }
              ])
          }
      ],
      Tools = [new BetaCodeExecutionTool20250825()]
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  // Unggah file
  file, err := os.Open("data.csv")
  if err != nil {
  	log.Fatal(err)
  }
  defer file.Close()

  fileObject, err := client.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
  	File: file,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan file_id dengan eksekusi kode
  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
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
  		anthropic.AnthropicBetaFilesAPI2025_04_14,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response.RawJSON())
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Unggah file
  FileMetadata fileObject = client.beta().files().upload(
      FileUploadParams.builder()
          .file(Path.of("data.csv"))
          .build()
  );

  // Gunakan file_id dengan eksekusi kode
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .addBeta(AnthropicBeta.FILES_API_2025_04_14)
          .maxTokens(4096L)
          .addUserMessageOfBetaContentBlockParams(List.of(
              BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
                  .text("Analyze this CSV data")
                  .build()),
              BetaContentBlockParam.ofContainerUpload(BetaContainerUploadBlockParam.builder()
                  .fileId(fileObject.id())
                  .build())
          ))
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build()
  );

  IO.println(ObjectMappers.jsonMapper().valueToTree(response));
  ```

  ```php PHP
  $client = new Client();

  // Unggah file
  $fileObject = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('data.csv', 'r')),
  );

  // Gunakan file_id dengan eksekusi kode
  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_4_8,
      maxTokens: 4096,
      betas: [AnthropicBeta::FILES_API_2025_04_14],
      messages: [
          [
              'role' => 'user',
              'content' => [
                  BetaTextBlockParam::with(text: 'Analyze this CSV data'),
                  BetaContainerUploadBlockParam::with(fileID: $fileObject->id),
              ],
          ],
      ],
      tools: [new BetaCodeExecutionTool20250825()],
  );

  echo json_encode($response), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Unggah file
  file_object = client.beta.files.upload(
    file: Pathname("data.csv")
  )

  # Gunakan file_id dengan eksekusi kode
  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
    betas: [Anthropic::AnthropicBeta::FILES_API_2025_04_14],
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
      Anthropic::Beta::BetaCodeExecutionTool20250825.new
    ]
  )

  puts response.to_json
  ```
</CodeGroup>

### Mengambil file yang dihasilkan

Ketika Claude membuat file selama eksekusi kode, ID setiap file yang dibuat muncul dalam hasil alat eksekusi kode, dan Anda dapat mengunduhnya dengan [Files API](/docs/id/build-with-claude/files):

<CodeGroup>
  ```bash cURL
  # Mengunduh setiap file yang dihasilkan berarti melakukan loop atas ID file dalam hasil
  # alat, yang tidak dapat diubah menjadi satu perintah shell sekali jalan. Gunakan
  # salah satu contoh SDK sebagai gantinya.
  ```

  ```bash CLI
  # Mengekstrak setiap ID file dari hasil alat dan mengunduh masing-masing
  # memerlukan loop, yang tidak cocok diterjemahkan menjadi perintah CLI sekali jalan.
  # Gunakan salah satu contoh SDK sebagai gantinya.
  ```

  ```python Python
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
  def extract_file_ids(response: BetaMessage) -> list[str]:
      file_ids: list[str] = []
      for item in response.content:
          if item.type == "bash_code_execution_tool_result":
              content_item = item.content
              if content_item.type == "bash_code_execution_result":
                  for output_block in content_item.content:
                      file_ids.append(output_block.file_id)
      return file_ids


  # Unduh file yang dibuat
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(file_id)
      file_content = client.beta.files.download(file_id)
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();

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

  // Ekstrak ID file dari respons dan unduh setiap file yang dibuat
  for (const block of response.content) {
    if (block.type === "bash_code_execution_tool_result") {
      const result = block.content;
      if (result.type === "bash_code_execution_result") {
        for (const outputBlock of result.content) {
          const [fileMetadata, fileResponse] = await Promise.all([
            client.beta.files.retrieveMetadata(outputBlock.file_id),
            client.beta.files.download(outputBlock.file_id)
          ]);
          await writeFile(fileMetadata.filename, await fileResponse.bytes());
          console.log(`Downloaded: ${fileMetadata.filename}`);
        }
      }
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Betas = [AnthropicBeta.FilesApi2025_04_14],
      Messages = [new() { Role = Role.User, Content = "Create a matplotlib visualization and save it as output.png" }],
      Tools = [new BetaCodeExecutionTool20250825()]
  };

  var response = await client.Beta.Messages.Create(parameters);

  // Kumpulkan ID file dari hasil alat
  List<string> fileIds = [];
  foreach (var block in response.Content)
  {
      if (!block.TryPickBashCodeExecutionToolResult(out var toolResult))
          continue;
      if (!toolResult.Content.TryPickBetaBashCodeExecutionResultBlock(out var result))
          continue;
      foreach (var output in result.Content)
      {
          fileIds.Add(output.FileID);
      }
  }

  // Unduh setiap file yang dibuat
  foreach (var fileId in fileIds)
  {
      var fileMetadata = await client.Beta.Files.RetrieveMetadata(fileId);
      using var download = await client.Beta.Files.Download(fileId);
      var downloadStream = await download.ReadAsStream();
      await using var target = File.Create(fileMetadata.Filename);
      await downloadStream.CopyToAsync(target);
      Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
  }
  ```

  ```go Go
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a matplotlib visualization and save it as output.png")),
  		},
  		Tools: []anthropic.BetaToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.BetaCodeExecutionTool20250825Param{}},
  		},
  		Betas: []anthropic.AnthropicBeta{
  			anthropic.AnthropicBetaFilesAPI2025_04_14,
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fileIDs := extractFileIDs(response)

  	for _, fileID := range fileIDs {
  		fileMetadata, err := client.Beta.Files.GetMetadata(ctx, fileID, anthropic.BetaFileGetMetadataParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		fileContent, err := client.Beta.Files.Download(ctx, fileID, anthropic.BetaFileDownloadParams{})
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
  			// Kumpulkan ID file dari tool_result
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
  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .addBeta(AnthropicBeta.FILES_API_2025_04_14)
          .maxTokens(4096L)
          .addUserMessage("Create a matplotlib visualization and save it as output.png")
          .addTool(BetaCodeExecutionTool20250825.builder().build())
          .build();

      BetaMessage response = client.beta().messages().create(params);

      List<String> fileIds = extractFileIds(response);

      for (String fileId : fileIds) {
          FileMetadata fileMetadata = client.beta().files().retrieveMetadata(fileId);
          try (HttpResponse fileContent = client.beta().files().download(fileId)) {
              Files.copy(
                  fileContent.body(),
                  Path.of(fileMetadata.filename()),
                  StandardCopyOption.REPLACE_EXISTING);
          }
          IO.println("Downloaded: " + fileMetadata.filename());
      }
  }

  List<String> extractFileIds(BetaMessage response) {
      List<String> fileIds = new ArrayList<>();
      // Kumpulkan ID file dari hasil alat
      for (BetaContentBlock item : response.content()) {
          item.bashCodeExecutionToolResult().ifPresent(toolResult -> {
              if (toolResult.content().isBetaBashCodeExecutionResultBlock()) {
                  BetaBashCodeExecutionResultBlock result =
                      toolResult.content().asBetaBashCodeExecutionResultBlock();
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
  $client = new Client();

  // Minta eksekusi kode yang membuat file
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a matplotlib visualization and save it as output.png',
          ],
      ],
      model: Model::CLAUDE_OPUS_4_8,
      betas: [AnthropicBeta::FILES_API_2025_04_14],
      tools: [new BetaCodeExecutionTool20250825()],
  );

  /**
   * Extract file IDs from the response.
   *
   * @return list<string>
   */
  function extractFileIds(BetaMessage $response): array
  {
      $fileIds = [];
      foreach ($response->content as $block) {
          if ($block->type !== 'bash_code_execution_tool_result') {
              continue;
          }
          $resultBlock = $block->content;
          if ($resultBlock->type !== 'bash_code_execution_result') {
              continue;
          }
          foreach ($resultBlock->content as $outputBlock) {
              $fileIds[] = $outputBlock->fileID;
          }
      }
      return $fileIds;
  }

  // Unduh file yang telah dibuat
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
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
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
        # SOLUSI SEMENTARA untuk bug coercion union anthropic-sdk-ruby (SDK-636): item.content adalah
        # union konten bersarang, sehingga accessor bertipe pada `item.content` tidak dapat diandalkan.
        # Sebagai gantinya, baca data respons mentah melalui API publik `BaseModel#[]`.
        content_item = item.content
        if content_item[:type].to_s == "bash_code_execution_result"
          Array(content_item[:content]).each do |output_block|
            file_ids << output_block[:file_id]
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

Kedua field bersifat tetap: `type` memilih versi alat, dan `name` harus `code_execution`.

Ketika Anda menyediakan alat ini, Claude secara otomatis mendapatkan akses ke dua sub-alat:

* `bash_code_execution`: Menjalankan perintah shell
* `text_editor_code_execution`: Melihat, membuat, dan mengedit file, termasuk menulis kode

Ketika Claude menjalankan kode, respons juga menyertakan objek `container` tingkat atas dengan `id` kontainer dan timestamp `expires_at`. Kirimkan kembali ID tersebut dalam parameter permintaan `container` tingkat atas untuk terus menggunakan kontainer yang sama. Lihat [Penggunaan kembali kontainer](#container-reuse).

## Format respons

Alat eksekusi kode dapat mengembalikan dua tipe hasil tergantung pada operasinya:

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
    "return_code": 0,
    "content": []
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
    "type": "text_editor_code_execution_view_result",
    "file_type": "text",
    "content": "{\n  \"setting\": \"value\",\n  \"debug\": true\n}",
    "num_lines": 4,
    "start_line": 1,
    "total_lines": 4
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
    "type": "text_editor_code_execution_create_result",
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
    "type": "text_editor_code_execution_str_replace_result",
    "old_start": 3,
    "old_lines": 1,
    "new_start": 3,
    "new_lines": 1,
    "lines": ["-  \"debug\": true", "+  \"debug\": false"]
  }
}
```

### Hasil

Hasil perintah Bash (`bash_code_execution_result`) mencakup:

* `stdout`: Output dari eksekusi yang berhasil
* `stderr`: Pesan kesalahan jika eksekusi gagal
* `return_code`: 0 untuk berhasil, bukan nol untuk gagal
* `content`: Daftar dengan entri untuk setiap file yang dibuat oleh perintah. Setiap entri membawa `file_id` untuk [mengambil file](#retrieve-generated-files) dengan Files API

Hasil operasi file memiliki field-nya sendiri:

* **View** (`text_editor_code_execution_view_result`): `file_type`, `content`, `num_lines`, `start_line`, `total_lines`
* **Create** (`text_editor_code_execution_create_result`): `is_file_update` (apakah file sudah ada sebelumnya)
* **Edit** (`text_editor_code_execution_str_replace_result`): `old_start`, `old_lines`, `new_start`, `new_lines`, `lines` (format diff)

### Kesalahan

Setiap tipe alat dapat mengembalikan kesalahan tertentu:

**Kesalahan umum (semua alat):**

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

**Kode kesalahan berdasarkan tipe alat:**

| Alat         | Kode kesalahan            | Deskripsi                                         |
| ------------ | ------------------------- | ------------------------------------------------- |
| Semua alat   | `unavailable`             | Alat sementara tidak tersedia                     |
| Semua alat   | `execution_time_exceeded` | Pemanggilan alat melebihi waktu eksekusi maksimum |
| Semua alat   | `invalid_tool_input`      | Parameter yang diberikan ke alat tidak valid      |
| Semua alat   | `too_many_requests`       | Batas laju terlampaui untuk penggunaan alat       |
| bash         | `output_file_too_large`   | Output perintah melebihi ukuran maksimum          |
| text\_editor | `file_not_found`          | File tidak ada (untuk operasi view/edit)          |

Kontainer yang kedaluwarsa tidak dapat digunakan kembali: permintaan yang mereferensikannya mengembalikan kesalahan alih-alih memulihkannya. Kirim permintaan lagi tanpa parameter `container` untuk mendapatkan kontainer baru.

### Alasan berhenti `pause_turn`

Respons mungkin menyertakan alasan berhenti `pause_turn`, yang menunjukkan bahwa API menjeda giliran yang berjalan lama. Anda dapat memberikan respons kembali apa adanya dalam permintaan berikutnya agar Claude melanjutkan gilirannya, atau memodifikasi kontennya jika Anda ingin menginterupsi percakapan.

## Kontainer

Alat eksekusi kode berjalan dalam lingkungan terkontainerisasi yang aman dan dirancang khusus untuk eksekusi kode, dengan fokus lebih tinggi pada Python.

### Lingkungan runtime

* **Versi Python:** 3.11
* **Sistem operasi:** Kontainer berbasis Linux
* **Arsitektur:** x86\_64 (AMD64)

### Batas sumber daya

* **Memori:** 5 GiB RAM
* **Ruang disk:** 5 GiB penyimpanan workspace
* **CPU:** 1 CPU
* **Waktu eksekusi:** Pemanggilan alat yang berjalan melewati waktu eksekusi maksimum mengembalikan [kesalahan](#errors) `execution_time_exceeded`. Dengan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), setiap sel REPL juga memiliki batas waktu nyata (wall-clock) 90 detik

### Jaringan dan keamanan

* **Akses internet:** Sepenuhnya dinonaktifkan demi keamanan
* **Koneksi eksternal:** Tidak ada permintaan jaringan keluar yang diizinkan
* **Isolasi sandbox:** Isolasi penuh dari sistem host dan kontainer lain
* **Akses file:** Terbatas hanya pada direktori workspace
* **Cakupan workspace:** Seperti [Files API](/docs/id/build-with-claude/files), kontainer dicakup ke workspace dari kunci API
* **Kedaluwarsa:** Kontainer kedaluwarsa 30 hari setelah dibuat

### Pustaka yang sudah terpasang

Lingkungan Python yang ter-sandbox mencakup pustaka-pustaka yang umum digunakan berikut:

* **Ilmu data:** pandas, numpy, scipy, scikit-learn, statsmodels
* **Visualisasi:** matplotlib, seaborn
* **Pemrosesan file:** pyarrow, openpyxl, xlsxwriter, xlrd, pillow, python-pptx, python-docx, pypdf, pdfplumber, pypdfium2, pdf2image, pdfkit, tabula-py, reportlab\[pycairo], Img2pdf
* **Matematika dan komputasi:** sympy, mpmath
* **Utilitas:** tqdm, python-dateutil, pytz, joblib

Kontainer juga mencakup alat baris perintah seperti unzip, unrar, 7zip, bc, rg (ripgrep), fd, dan sqlite.

Kontainer tidak memiliki akses internet, sehingga Claude tidak dapat mengunduh atau memasang paket tambahan saat runtime: hanya pustaka yang sudah terpasang yang tersedia.

## Penggunaan kembali kontainer

Anda dapat menggunakan kembali kontainer yang sudah ada di beberapa permintaan API dengan memberikan ID kontainer dari respons sebelumnya. Ini memungkinkan Anda mempertahankan file yang dibuat di antara permintaan. Dengan `code_execution_20260120` atau yang lebih baru dan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), state interpreter Python juga bertahan.

Kontainer kedaluwarsa 30 hari setelah dibuat. Setelah sekitar 5 menit tidak aktif, kontainer di-checkpoint, dan mengirim permintaan dengan ID-nya dalam jendela 30 hari akan memulihkannya. Timestamp `expires_at` dalam objek `container` pada respons adalah nilai bergulir yang lebih pendek dan tidak melaporkan batas 30 hari. Kontainer yang telah kedaluwarsa tidak dapat digunakan kembali. Kirim permintaan lagi tanpa parameter `container` untuk mendapatkan kontainer baru.

### Contoh

<CodeGroup>
  ```bash cURL
  # Permintaan pertama: Buat file berisi angka acak, sambil menangkap ID container (menggunakan jq)
  CONTAINER_ID=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
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
    }' | jq -r '.container.id')

  # Permintaan kedua: Gunakan kembali container untuk membaca file tersebut
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "container": "'"$CONTAINER_ID"'",
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
    --model claude-opus-4-8 \
    --max-tokens 4096 \
    --message '{role: user, content: Write a file with a random number and save it to "/tmp/number.txt"}' \
    --tool '{type: code_execution_20250825, name: code_execution}' \
    --transform container.id --raw-output)

  # Permintaan kedua: Gunakan kembali container untuk membaca file
  ant messages create \
    --container "$CONTAINER_ID" \
    --model claude-opus-4-8 \
    --max-tokens 4096 \
    --message '{role: user, content: Read the number from "/tmp/number.txt" and calculate its square}' \
    --tool '{type: code_execution_20250825, name: code_execution}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Permintaan pertama: buat file berisi angka acak di container baru
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

  # Permintaan kedua: kirimkan kembali ID container agar Claude menggunakan kembali container yang sama
  response2 = client.messages.create(
      container=response1.container.id,
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

  print(response2.to_json())
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Permintaan pertama: Claude membuat file di dalam container eksekusi kode yang baru
  const response1 = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Write a file with a random number and save it to '/tmp/number.txt'"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Respons menyertakan container setelah alat eksekusi kode dijalankan
  if (!response1.container) {
    throw new Error("Expected the first response to include a container");
  }

  // Permintaan kedua: kirimkan kembali ID container agar container yang sama digunakan kembali
  const response2 = await client.messages.create({
    container: response1.container.id,
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Read the number from /tmp/number.txt and calculate its square" }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  console.log(JSON.stringify(response2));
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Permintaan pertama: Claude membuat file di dalam container eksekusi kode yang baru
  var response1 = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Write a file with a random number and save it to '/tmp/number.txt'" }],
      Tools = [new CodeExecutionTool20250825()]
  });

  // Permintaan kedua: kirimkan kembali ID container agar Claude menggunakan kembali container yang sama
  var response2 = await client.Messages.Create(new()
  {
      Container = response1.Container!.ID,
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Read the number from '/tmp/number.txt' and calculate its square" }],
      Tools = [new CodeExecutionTool20250825()]
  });

  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  codeExecution := []anthropic.ToolUnionParam{
  	{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  }

  // Permintaan pertama: buat file berisi angka acak di container baru
  response1, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a file with a random number and save it to '/tmp/number.txt'")),
  	},
  	Tools: codeExecution,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan kembali container dari permintaan pertama agar file tersebut masih ada.
  response2, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Container: anthropic.String(response1.Container.ID),
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Read the number from '/tmp/number.txt' and calculate its square")),
  	},
  	Tools: codeExecution,
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response2.RawJSON())
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Permintaan pertama: buat file berisi angka acak di container baru
  MessageCreateParams params1 = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(4096L)
      .addUserMessage("Write a file with a random number and save it to '/tmp/number.txt'")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message response1 = client.messages().create(params1);

  // Permintaan kedua: kirimkan kembali ID container agar container yang sama digunakan ulang
  MessageCreateParams params2 = MessageCreateParams.builder()
      .container(response1.container().orElseThrow().id())
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(4096L)
      .addUserMessage("Read the number from '/tmp/number.txt' and calculate its square")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message response2 = client.messages().create(params2);
  IO.println(ObjectMappers.jsonMapper().valueToTree(response2));
  ```

  ```php PHP
  $client = new Client();

  // Permintaan pertama: Claude menulis file di dalam container eksekusi kode yang baru
  $response1 = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => "Write a file with a random number and save it to '/tmp/number.txt'",
          ],
      ],
      model: Model::CLAUDE_OPUS_4_8,
      tools: [new CodeExecutionTool20250825()],
  );

  // Permintaan kedua: gunakan kembali container tersebut sehingga '/tmp/number.txt' masih ada
  $response2 = $client->messages->create(
      container: $response1->container->id,
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => "Read the number from '/tmp/number.txt' and calculate its square",
          ],
      ],
      model: Model::CLAUDE_OPUS_4_8,
      tools: [new CodeExecutionTool20250825()],
  );

  echo json_encode($response2), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Permintaan pertama: Claude membuat file di dalam container eksekusi kode yang baru
  response1 = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Write a file with a random number and save it to '/tmp/number.txt'"
      }
    ],
    tools: [Anthropic::CodeExecutionTool20250825.new]
  )

  # Permintaan kedua: kirimkan kembali ID container agar Claude menggunakan kembali container yang sama
  response2 = client.messages.create(
    container: response1.container.id,
    model: Anthropic::Model::CLAUDE_OPUS_4_8,
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Read the number from '/tmp/number.txt' and calculate its square"
      }
    ],
    tools: [Anthropic::CodeExecutionTool20250825.new]
  )

  puts response2.to_json
  ```
</CodeGroup>

## Menggunakan eksekusi kode dengan alat eksekusi lainnya

Ketika Anda menyediakan eksekusi kode bersamaan dengan alat yang disediakan klien yang juga menjalankan kode (seperti [alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool) atau REPL kustom), Claude beroperasi dalam lingkungan multikomputer. Alat eksekusi kode berjalan dalam kontainer sandbox Anthropic, sementara alat yang disediakan klien Anda berjalan di lingkungan terpisah yang Anda kendalikan. Claude terkadang dapat bingung membedakan lingkungan-lingkungan ini, mencoba menggunakan alat yang salah atau mengasumsikan state dibagikan di antara keduanya.

Untuk menghindari hal ini, tambahkan instruksi ke prompt sistem Anda yang memperjelas perbedaannya:

```text wrap
When multiple code execution environments are available, be aware that:
- Variables, files, and state do NOT persist between different execution environments
- Use the code_execution tool for general-purpose computation in Anthropic's sandboxed environment
- Use client-provided execution tools (e.g., bash) when you need access to the user's local system, files, or data
- If you need to pass results between environments, explicitly include outputs in subsequent tool calls rather than assuming shared state
```

Ini sangat penting ketika menggabungkan eksekusi kode dengan [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), yang mengaktifkan eksekusi kode secara otomatis. Jika aplikasi Anda sudah menyediakan alat shell sisi klien, eksekusi kode otomatis menciptakan lingkungan eksekusi kedua yang perlu dibedakan oleh Claude.

Ketika Claude memanggil salah satu alat klien Anda bersamaan dengan eksekusi kode, API mengembalikan panggilan eksekusi kode tanpa hasilnya. Hasilnya tiba dalam respons berikutnya, setelah Anda mengirim kembali blok `tool_result` untuk alat klien Anda.

## Streaming

Dengan [streaming](/docs/id/build-with-claude/streaming) diaktifkan (`"stream": true`), Anda akan menerima event eksekusi kode saat terjadi. Input sub-alat di-streaming sebagai event `input_json_delta`, dan setiap blok hasil tiba secara utuh dalam satu event `content_block_start`:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "bash_code_execution"}}

// Tool input streamed as partial JSON
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"command\": \"python analyze.py\"}"}}

// Pause while the command runs

// Execution result delivered as a complete block
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "bash_code_execution_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "bash_code_execution_result", "stdout": "   A  B  C\n0  1  2  3\n1  4  5  6", "stderr": "", "return_code": 0, "content": []}}}
```

## Permintaan batch

Anda dapat menyertakan alat eksekusi kode dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat eksekusi kode melalui Messages Batches API dikenakan harga yang sama dengan yang ada dalam permintaan Messages API reguler.

## Penggunaan dan harga

**Eksekusi kode gratis saat digunakan dengan web search atau web fetch.** Ketika `web_search_20260209` (atau yang lebih baru) atau `web_fetch_20260209` (atau yang lebih baru) disertakan dalam permintaan API Anda, tidak ada biaya tambahan untuk pemanggilan alat eksekusi kode di luar biaya token input dan output standar.

Saat digunakan tanpa alat-alat tersebut, eksekusi kode ditagih berdasarkan waktu eksekusi, yang dilacak secara terpisah dari penggunaan token:

* Waktu eksekusi memiliki minimum 5 menit
* Setiap organisasi menerima **1.550 jam gratis** penggunaan per bulan
* Penggunaan tambahan di atas 1.550 jam ditagih sebesar **$0,05 USD per jam, per container**
* Jika file disertakan dalam permintaan, waktu eksekusi tetap ditagih meskipun alat tidak dipanggil, karena file dimuat terlebih dahulu ke dalam container

Penggunaan eksekusi kode dilacak dalam respons:

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

## Tingkatkan ke versi alat terbaru

Versi alat terbaru adalah `code_execution_20260521`. Untuk berpindah di antara ketiga versi saat ini, perbarui string `type` dalam permintaan Anda: ketiganya mengembalikan blok respons yang didokumentasikan dalam [Format respons](#response-format). Lihat [Kompatibilitas model](#model-compatibility) untuk mengetahui apa yang ditambahkan setiap versi dan model mana yang mendukungnya.

Sisa bagian ini membahas migrasi dari `code_execution_20250522` lama yang hanya mendukung Python ke versi alat saat ini.

### Apa yang berubah

| Komponen     | Lama                        | Saat ini                                                            |
| ------------ | --------------------------- | ------------------------------------------------------------------- |
| Header beta  | `code-execution-2025-05-22` | Tidak diperlukan                                                    |
| Tipe alat    | `code_execution_20250522`   | `code_execution_20250825` atau yang lebih baru                      |
| Kemampuan    | Hanya Python                | Perintah Bash, operasi file                                         |
| Tipe respons | `code_execution_result`     | `bash_code_execution_result`, `text_editor_code_execution_*_result` |

### Kompatibilitas mundur

* Semua eksekusi kode Python yang ada terus bekerja persis seperti sebelumnya
* Tidak ada perubahan yang diperlukan untuk alur kerja yang hanya menggunakan Python

### Langkah-langkah peningkatan

Untuk meningkatkan, perbarui tipe alat dalam permintaan API Anda:

```diff
- "type": "code_execution_20250522"
+ "type": "code_execution_20250825"
```

**Tinjau penanganan respons** (jika mem-parsing respons secara terprogram):

* API tidak lagi mengirim blok sebelumnya untuk respons eksekusi Python
* Sebagai gantinya, API mengirim tipe respons baru untuk operasi Bash dan file (lihat [Format respons](#response-format))

## Retensi data

Eksekusi kode berjalan dalam kontainer sandbox sisi server. Data kontainer, termasuk artefak eksekusi, file yang diunggah, dan output, disimpan hingga 30 hari. Retensi ini berlaku untuk semua data yang diproses dalam lingkungan kontainer. File yang dibuat eksekusi kode di [Files API](/docs/id/build-with-claude/files) (dapat diambil dengan `client.beta.files.download()`) bertahan hingga dihapus secara eksplisit.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat advisor" icon="compass" href="/docs/id/agents-and-tools/tool-use/advisor-tool">
    Pasangkan model eksekutor yang lebih cepat dengan model advisor berintelegensi lebih tinggi yang memberikan panduan strategis di tengah proses generasi.
  </Card>

  <Card title="Pemanggilan alat terprogram" icon="code" href="/docs/id/agents-and-tools/tool-use/programmatic-tool-calling">
    Panggil alat Anda sendiri dari kode yang berjalan di dalam kontainer eksekusi kode.
  </Card>

  <Card title="Files API" icon="file" href="/docs/id/build-with-claude/files">
    Unggah file untuk dianalisis dan unduh file yang dibuat oleh eksekusi kode.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="book" href="/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>
</CardGroup>
