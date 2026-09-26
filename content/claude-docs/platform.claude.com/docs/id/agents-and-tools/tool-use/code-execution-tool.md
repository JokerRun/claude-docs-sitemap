---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool
fetched_at: 2026-09-26T02:19:50.539049Z
sha256: 94c0607d1ac9f82d0646965f9bf69c1ff969d8301b29f9f82a3f2c20653c8fbc
---

---
title: Alat eksekusi kode
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool
description: Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.
featureMetadata:
  status: ga
  zdr: not-eligible
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-opus-5-5
    - claude-opus-5
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-5
    - claude-sonnet-4-6
    - claude-sonnet-4-5-20250929
    - claude-haiku-4-5-20251001
  supportedPlatforms:
    Claude API: ga
    Claude Platform on AWS: ga
    Amazon Bedrock: not available
    Google Cloud: not available
    Microsoft Foundry:
      availability: ga
      note: Di [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), eksekusi kode memerlukan [deployment Hosted on Anthropic](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).
  details:
    - Setiap model yang didukung menerima ketiga [versi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#tool-versions). Di Claude Haiku 4.5, pemanggilan alat terprogram dan persistensi status REPL tidak tersedia, sehingga versi yang lebih baru berperilaku seperti `code_execution_20250825` di sana.
    - Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), eksekusi kode didukung di Claude API dan Microsoft Foundry.
---

Claude dapat menganalisis data, membuat visualisasi, melakukan perhitungan kompleks, menjalankan perintah sistem, membuat dan mengedit file, serta memproses file yang diunggah langsung di dalam percakapan API. Alat eksekusi kode memungkinkan Claude menjalankan perintah Bash dan memanipulasi file, termasuk menulis kode, dalam lingkungan "sandbox" (lingkungan terisolasi) yang aman.

**Eksekusi kode gratis jika digunakan bersama pencarian web atau web fetch (`web_search_20260209`, `web_fetch_20260209`, atau yang lebih baru).** Jika salah satu alat tersebut ada dalam permintaan Anda, tidak ada biaya tambahan untuk eksekusi kode dalam permintaan itu selain biaya token standar. Ini mencakup eksekusi kode di balik pemfilteran dinamis maupun kode apa pun yang dijalankan Claude secara langsung. Harga eksekusi kode standar berlaku jika alat-alat tersebut tidak disertakan.

Eksekusi kode juga menjalankan "dynamic filtering" (pemfilteran dinamis) pada alat [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool): Claude memfilter hasil di dalam lingkungan eksekusi kode sebelum hasil tersebut mencapai "context window" (jendela konteks). Saat pemfilteran dinamis berjalan, API secara otomatis menyediakan eksekusi kode yang dibutuhkan untuk permintaan tersebut, sehingga Anda tidak perlu menambahkan alat eksekusi kode ke permintaan Anda untuk keperluan itu.

<Note>
  Hubungi kami melalui [formulir umpan balik](https://forms.gle/LTAU6Xn2puCJMi1n6) untuk membagikan umpan balik Anda tentang fitur ini.
</Note>

## Versi alat

Alat eksekusi kode memiliki tiga versi saat ini, dan setiap [model yang didukung](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#compatibility) menerima ketiganya. Setiap versi dibangun di atas versi sebelumnya:

* `code_execution_20250825` mendukung perintah Bash dan operasi file.
* `code_execution_20260120` menambahkan "REPL state persistence" (persistensi status REPL) dan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dari dalam sandbox. Claude Haiku 4.5 menerima tipe alat `code_execution_20260120` dan `code_execution_20260521`, tetapi pemanggilan alat terprogram dan persistensi status REPL yang bergantung padanya tidak tersedia di model tersebut, sehingga versi yang lebih baru berperilaku seperti `code_execution_20250825` di sana.
* `code_execution_20260521` menggunakan runtime yang sama dengan `code_execution_20260120`. Perbedaannya adalah deskripsi alat memberi tahu Claude tentang batas waktu nyata 90 detik pada setiap sel Python dalam pemanggilan alat terprogram, sehingga Claude dapat mengatur anggaran untuk sel yang berjalan lama. Sel yang melebihi batas tersebut mengembalikan hasil eksekusi kode normal dengan `return_code` bukan nol dan pesan status `detection_timeout` dalam output-nya. Ini terpisah dari [kode error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#errors) `execution_time_exceeded`, yang dikembalikan API ketika seluruh pemanggilan alat melebihi waktu eksekusi maksimum.

Tidak satu pun dari ketiga versi alat memerlukan header `anthropic-beta`. Header beta eksekusi kode lama tetap valid sebagai opsi keikutsertaan.

Contoh-contoh di halaman ini menggunakan `code_execution_20250825`, yang mencakup operasi Bash dan file yang didemonstrasikan dan berperilaku sama di setiap model yang didukung; gunakan `code_execution_20260120` atau yang lebih baru jika Anda memerlukan pemanggilan alat terprogram atau persistensi status REPL. Alat [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) saat ini (`web_search_20260209`, `web_fetch_20260209`, dan yang lebih baru) memerlukan `code_execution_20260120` atau yang lebih baru sebagai versi eksekusi kodenya.

Versi alat yang lebih lama tidak dijamin tetap kompatibel dengan model yang lebih baru. Saat Anda mengadopsi model baru, periksa [Versi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#tool-versions) dan [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#compatibility), dan utamakan versi alat terbaru yang didukung integrasi Anda.

<Note>
  Jika Anda masih menggunakan `code_execution_20250522` lama (hanya Python), lihat [Upgrade ke versi alat terbaru](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk bermigrasi darinya.
</Note>

## Mulai cepat

Berikut contoh yang meminta Claude melakukan perhitungan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
    --model claude-opus-5-5 \
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
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Use the code execution tool to calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" }],
      Tools = [new CodeExecutionTool20250825()]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
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
      .model(Model.CLAUDE_OPUS_5_5)
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
      model: Model::CLAUDE_OPUS_5_5,
      tools: [new CodeExecutionTool20250825()],
  );

  echo json_encode($message, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

Respons menyelingi blok `server_tool_use` (perintah yang dijalankan Claude) dengan blok hasil alatnya, diikuti oleh teks Claude. Tingkat teratas juga menyertakan objek `container` yang `id`-nya dapat Anda [gunakan kembali di berbagai permintaan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#container-reuse). Lihat [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#response-format) untuk bentuk blok.

## Cara kerja eksekusi kode

Saat Anda menambahkan alat eksekusi kode ke permintaan API Anda:

1. Claude mengevaluasi apakah eksekusi kode akan membantu menjawab pertanyaan Anda

2. Alat ini secara otomatis memberi Claude kemampuan berikut:

   * **Perintah Bash:** Menjalankan perintah shell untuk operasi sistem
   * **Operasi file:** Membuat, melihat, dan mengedit file secara langsung, termasuk menulis kode

3. Claude dapat menggunakan kombinasi apa pun dari kemampuan ini dalam satu permintaan

4. Semua operasi berjalan dalam container sandbox yang aman. Container tidak memiliki akses internet, sehingga Claude tidak dapat mengunduh paket saat runtime: hanya [pustaka yang sudah terinstal](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#pre-installed-libraries) yang tersedia

5. API menjalankan setiap perintah di sisi server dan mengembalikan hasilnya ke Claude dalam permintaan yang sama, sehingga Anda tidak pernah mengeksekusi kode atau mengirim kembali blok `tool_result` sendiri. Satu pengecualian adalah ketika Claude memanggil salah satu alat klien Anda bersamaan dengan eksekusi kode: API mengembalikan panggilan eksekusi kode tanpa hasilnya. Hasilnya tiba dalam respons berikutnya, setelah Anda mengirim kembali blok `tool_result` untuk alat klien Anda

6. Setiap permintaan berjalan dalam container baru kecuali Anda meneruskan kembali ID container dari respons sebelumnya (lihat [Penggunaan ulang container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#container-reuse))

7. Claude memberikan hasil beserta grafik, perhitungan, atau analisis yang dihasilkan

Container sudah memiliki Python yang terinstal. Claude menulis Python dengan sub-alat operasi file dan menjalankannya dengan perintah Bash. Dengan `code_execution_20260120` atau yang lebih baru dan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), status interpreter Python (seperti binding variabel) juga bertahan di seluruh permintaan yang menggunakan kembali container.

### Kapan Claude menjalankan kode

Claude menjalankan kode ketika permintaan mendapat manfaat dari komputasi atau penanganan file:

* Matematika yang tidak sederhana (angka besar, banyak langkah, hasil yang sensitif terhadap presisi)
* Analisis data, parsing file, atau visualisasi
* Eksekusi algoritma atau simulasi
* Permintaan eksplisit untuk "run", "compute", atau "execute"

Claude menjawab langsung tanpa menjalankan kode untuk:

* Aritmetika sederhana dan fakta matematika yang sudah umum diketahui
* Permintaan faktual, percakapan, atau kreatif
* Konversi satuan atau terjemahan sederhana

Jika Anda ingin Claude menjalankan kode untuk permintaan yang berada di batas, mintalah secara eksplisit (misalnya, "jalankan kode untuk memverifikasi ini").

## Bekerja dengan file

### Unggah dan analisis file Anda sendiri

Untuk menganalisis file data Anda sendiri (seperti CSV, Excel, atau gambar), unggah file tersebut melalui Files API dan rujuk dalam permintaan Anda.

Lingkungan Python dapat memproses berbagai jenis file yang diunggah melalui Files API, termasuk:

* CSV
* Excel (.xlsx, .xls)
* JSON
* XML
* Gambar (JPEG, PNG, GIF, WebP)
* File teks (.txt, .md, .py, dan lainnya)

#### Unggah dan analisis file

1. **Unggah file Anda** menggunakan [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
2. **Rujuk file tersebut** dalam pesan Anda menggunakan blok konten `container_upload`
3. **Sertakan alat eksekusi kode** dalam permintaan API Anda

<CodeGroup>
  ```bash cURL
  # Pertama, unggah file dan simpan ID file-nya (menggunakan jq)
  FILE_ID=$(curl --fail-with-body -sS https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -F "file=@data.csv" | jq -r '.id')

  # Lalu gunakan file_id dengan eksekusi kode
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
  FILE_ID=$(ant files upload --file ./data.csv --transform id --raw-output)

  # Lalu gunakan file_id dengan eksekusi kode
  ant messages create <<YAML
  model: claude-opus-5-5
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
  file_object = client.files.upload(file=Path("data.csv"))

  # Gunakan file_id dengan eksekusi kode
  response = client.messages.create(
      model="claude-opus-5-5",
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
  const fileObject = await client.files.upload({
    file: createReadStream("data.csv")
  });

  // Gunakan file_id dengan eksekusi kode
  const response = await client.messages.create({
    model: "claude-opus-5-5",
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

  // Unggah file
  var fileObject = await client.Files.Upload(new FileUploadParams
  {
      File = File.OpenRead("data.csv")
  });

  // Gunakan file_id dengan eksekusi kode
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [
          new()
          {
              Role = Role.User,
              Content = new([
                  new TextBlockParam { Text = "Analyze this CSV data" },
                  new ContainerUploadBlockParam { FileID = fileObject.ID }
              ])
          }
      ],
      Tools = [new CodeExecutionTool20250825()]
  };

  var response = await client.Messages.Create(parameters);
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

  fileObject, err := client.Files.Upload(ctx, anthropic.FileUploadParams{
  	File: file,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan file_id dengan eksekusi kode
  response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewTextBlock("Analyze this CSV data"),
  			anthropic.NewContainerUploadBlock(fileObject.ID),
  		),
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

  // Unggah file
  FileMetadata fileObject = client.files().upload(
      FileUploadParams.builder()
          .file(Path.of("data.csv"))
          .build()
  );

  // Gunakan file_id dengan eksekusi kode
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofText(TextBlockParam.builder()
                  .text("Analyze this CSV data")
                  .build()),
              ContentBlockParam.ofContainerUpload(ContainerUploadBlockParam.builder()
                  .fileId(fileObject.id())
                  .build())
          ))
          .addTool(CodeExecutionTool20250825.builder().build())
          .build()
  );

  IO.println(ObjectMappers.jsonMapper().valueToTree(response));
  ```

  ```php PHP
  $client = new Client();

  // Unggah file
  $fileObject = $client->files->upload(
      file: FileParam::fromResource(fopen('data.csv', 'r')),
  );

  // Gunakan file_id dengan eksekusi kode
  $response = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  TextBlockParam::with(text: 'Analyze this CSV data'),
                  ContainerUploadBlockParam::with(fileID: $fileObject->id),
              ],
          ],
      ],
      tools: [new CodeExecutionTool20250825()],
  );

  echo json_encode($response), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Unggah file
  file_object = client.files.upload(
    file: Pathname("data.csv")
  )

  # Gunakan file_id dengan eksekusi kode
  response = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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
      Anthropic::CodeExecutionTool20250825.new
    ]
  )

  puts response.to_json
  ```
</CodeGroup>

### Mengambil file yang dihasilkan

Ketika Claude menyimpan file ke direktori output-nya selama eksekusi kode (lihat [Cara file yang dihasilkan ditangkap](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#how-generated-files-are-captured)), ID setiap file muncul dalam hasil alat eksekusi kode, dan Anda dapat mengunduhnya dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files):

<CodeGroup>
  ```bash cURL
  # Mengunduh setiap file yang dihasilkan berarti melakukan loop atas ID file di hasil
  # alat, yang tidak bisa diterjemahkan menjadi satu perintah shell sekali jalan. Gunakan salah satu
  # contoh SDK sebagai gantinya.
  ```

  ```bash CLI
  # Mengekstrak setiap ID file dari hasil alat dan mengunduh masing-masing
  # memerlukan loop, yang tidak cocok untuk perintah CLI sekali jalan.
  # Sebagai gantinya, gunakan salah satu contoh SDK.
  ```

  ```python Python
  client = Anthropic()

  # Minta eksekusi kode yang membuat file
  response = client.messages.create(
      model="claude-opus-5-5",
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
  def extract_file_ids(response: Message) -> list[str]:
      file_ids: list[str] = []
      for item in response.content:
          if item.type == "bash_code_execution_tool_result":
              content_item = item.content
              if content_item.type == "bash_code_execution_result":
                  for output_block in content_item.content:
                      file_ids.append(output_block.file_id)
      return file_ids


  # Unduh file yang telah dibuat
  for file_id in extract_file_ids(response):
      file_metadata = client.files.retrieve_metadata(file_id)
      file_content = client.files.download(file_id)
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();

  // Minta eksekusi kode yang membuat file
  const response = await client.messages.create({
    model: "claude-opus-5-5",
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
            client.files.retrieveMetadata(outputBlock.file_id),
            client.files.download(outputBlock.file_id)
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Create a matplotlib visualization and save it as output.png" }],
      Tools = [new CodeExecutionTool20250825()]
  };

  var response = await client.Messages.Create(parameters);

  // Kumpulkan ID file dari hasil alat
  List<string> fileIds = [];
  foreach (var block in response.Content)
  {
      if (!block.TryPickBashCodeExecutionToolResult(out var toolResult))
          continue;
      if (!toolResult.Content.TryPickBashCodeExecutionResultBlock(out var result))
          continue;
      foreach (var output in result.Content)
      {
          fileIds.Add(output.FileID);
      }
  }

  // Unduh setiap file yang dibuat
  foreach (var fileId in fileIds)
  {
      var fileMetadata = await client.Files.RetrieveMetadata(fileId);
      using var download = await client.Files.Download(fileId);
      var downloadStream = await download.ReadAsStream();
      await using var target = File.Create(fileMetadata.Filename);
      await downloadStream.CopyToAsync(target);
      Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
  }
  ```

  ```go Go
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 4096,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Create a matplotlib visualization and save it as output.png")),
  		},
  		Tools: []anthropic.ToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fileIDs := extractFileIDs(response)

  	for _, fileID := range fileIDs {
  		fileMetadata, err := client.Files.GetMetadata(ctx, fileID, anthropic.FileGetMetadataParams{})
  		if err != nil {
  			log.Fatal(err)
  		}

  		fileContent, err := client.Files.Download(ctx, fileID, anthropic.FileDownloadParams{})
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

  func extractFileIDs(response *anthropic.Message) []string {
  	var fileIDs []string
  	for _, item := range response.Content {
  		switch variant := item.AsAny().(type) {
  		case anthropic.BashCodeExecutionToolResultBlock:
  			// Kumpulkan ID file dari hasil alat
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
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addUserMessage("Create a matplotlib visualization and save it as output.png")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response = client.messages().create(params);

      List<String> fileIds = extractFileIds(response);

      for (String fileId : fileIds) {
          FileMetadata fileMetadata = client.files().retrieveMetadata(fileId);
          try (HttpResponse fileContent = client.files().download(fileId)) {
              Files.copy(
                  fileContent.body(),
                  Path.of(fileMetadata.filename()),
                  StandardCopyOption.REPLACE_EXISTING);
          }
          IO.println("Downloaded: " + fileMetadata.filename());
      }
  }

  List<String> extractFileIds(Message response) {
      List<String> fileIds = new ArrayList<>();
      // Kumpulkan ID file dari hasil alat
      for (ContentBlock item : response.content()) {
          item.bashCodeExecutionToolResult().ifPresent(toolResult -> {
              if (toolResult.content().isBashCodeExecutionResultBlock()) {
                  BashCodeExecutionResultBlock result =
                      toolResult.content().asBashCodeExecutionResultBlock();
                  for (BashCodeExecutionOutputBlock output : result.content()) {
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
  $response = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a matplotlib visualization and save it as output.png',
          ],
      ],
      model: Model::CLAUDE_OPUS_5_5,
      tools: [new CodeExecutionTool20250825()],
  );

  /**
   * Extract file IDs from the response.
   *
   * @return list<string>
   */
  function extractFileIds(Message $response): array
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
      $fileMetadata = $client->files->retrieveMetadata($fileId);
      $fileContent = $client->files->download($fileId);

      file_put_contents($fileMetadata->filename, $fileContent);
      echo "Downloaded: {$fileMetadata->filename}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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
        # SOLUSI SEMENTARA untuk bug koersi union anthropic-sdk-ruby (SDK-636): item.content adalah
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
    file_metadata = client.files.retrieve_metadata(file_id)
    file_content = client.files.download(file_id)

    File.open(file_metadata.filename, "wb") do |f|
      f.write(file_content.read)
    end

    puts "Downloaded: #{file_metadata.filename}"
  end
  ```
</CodeGroup>

#### Cara file yang dihasilkan ditangkap

Setiap panggilan `bash_code_execution` mendapatkan direktori baru yang kosong, yang tersedia bagi perintah sebagai `$OUTPUT_DIR`. Ketika perintah selesai, file-file di tingkat teratas direktori tersebut ditangkap dan dikembalikan sebagai entri `file_id` dalam daftar `content` pada hasil. File yang ditulis di tempat lain tetap berada di container dan tidak dikembalikan.

Deskripsi alat memberi tahu Claude untuk membagikan file dengan menyalinnya ke `$OUTPUT_DIR`. Jika aplikasi Anda bergantung pada penerimaan sebuah file, minta Claude untuk menyalinnya ke `$OUTPUT_DIR` dan menampilkan isi direktori tersebut dalam perintah yang sama, sehingga output `ls` mengonfirmasi penangkapan tersebut (Claude tidak melihat daftar `content`):

```bash
python /tmp/make_report.py && cp /tmp/report.pdf "$OUTPUT_DIR/" && ls "$OUTPUT_DIR"
```

File yang ditulis Claude di tempat lain masih berada di container, sehingga Anda dapat [menggunakan kembali container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#container-reuse) dan meminta Claude untuk menyalinnya ke `$OUTPUT_DIR`.

### Content Credentials pada file yang dihasilkan

Di Claude API, file gambar, video, dan audio yang didukung yang dihasilkan Claude di sandbox eksekusi kode membawa Content Credentials [C2PA](https://c2pa.org/) saat Anda mengunduhnya melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files). [Format yang didukung](https://opensource.contentauthenticity.org/docs/sdk-repos/c2pa-python/docs/supported-formats/) mencakup PNG, JPEG, GIF, WebP, TIFF, HEIC, AVIF, SVG, MP4, MOV, MP3, WAV, FLAC, dan M4A. Kredensial tersebut adalah manifes yang ditandatangani secara kriptografis dan disematkan dalam metadata file. Manifes ini mengidentifikasi Anthropic sebagai penerbit, membawa stempel waktu, dan mencatat deskripsi tindakan "Claude provided this file at the request of a user and may have created or modified the file contents."

Penandatanganan tidak memerlukan perubahan apa pun pada permintaan atau penanganan respons Anda, dan manifes tidak mencatat apa pun tentang Anda, organisasi Anda, atau permintaan Anda. Konten file yang terlihat tidak berubah. Manifes menambahkan beberapa kilobyte, sehingga ukuran dan checksum file yang diunduh berbeda dari file yang ada di dalam container. File teks, PDF, dan dokumen perkantoran tidak ditandatangani karena bukan format yang didukung untuk penandatanganan. File yang Anda unggah disimpan apa adanya, termasuk Content Credentials apa pun yang sudah dibawanya.

Untuk memverifikasi kredensial, periksa file dengan alat apa pun yang kompatibel dengan C2PA, seperti [utilitas command-line c2patool](https://github.com/contentauth/c2pa-rs) yang bersifat open-source. Encoding ulang, konversi format, tangkapan layar, dan alat yang menghapus metadata akan menghilangkan kredensial, sehingga kredensial yang tidak ada tidak berarti file tersebut tidak dihasilkan dengan Claude. Untuk informasi lebih lanjut tentang mengapa kredensial bisa tidak ada, lihat [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content).

## Definisi alat

Alat eksekusi kode tidak memerlukan parameter tambahan:

```json JSON
{
  "type": "code_execution_20250825",
  "name": "code_execution"
}
```

Kedua field bersifat tetap: `type` memilih versi alat, dan `name` harus berupa `code_execution`.

Saat Anda menyediakan alat ini, Claude secara otomatis mendapatkan akses ke dua sub-alat:

* `bash_code_execution`: Menjalankan perintah shell
* `text_editor_code_execution`: Melihat, membuat, dan mengedit file, termasuk menulis kode

Ketika Claude menjalankan kode, respons juga menyertakan objek `container` tingkat teratas dengan `id` container dan stempel waktu `expires_at`. Teruskan kembali ID tersebut dalam parameter permintaan `container` tingkat teratas untuk terus menggunakan container yang sama. Lihat [Penggunaan ulang container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#container-reuse).

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
* `stderr`: Pesan error jika eksekusi gagal
* `return_code`: 0 untuk berhasil, bukan nol untuk gagal
* `content`: Daftar dengan satu entri untuk setiap file yang ditinggalkan perintah di `$OUTPUT_DIR` (lihat [Cara file yang dihasilkan ditangkap](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#how-generated-files-are-captured)). Setiap entri membawa `file_id` untuk [mengambil file](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) dengan Files API

Hasil operasi file memiliki field-nya sendiri:

* **View** (`text_editor_code_execution_view_result`): `file_type`, `content`, `num_lines`, `start_line`, `total_lines`
* **Create** (`text_editor_code_execution_create_result`): `is_file_update` (apakah file sudah ada sebelumnya)
* **Edit** (`text_editor_code_execution_str_replace_result`): `old_start`, `old_lines`, `new_start`, `new_lines`, `lines` (format diff)

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

| Alat         | Kode error                | Deskripsi                                                  |
| ------------ | ------------------------- | ---------------------------------------------------------- |
| Semua alat   | `unavailable`             | Alat untuk sementara tidak tersedia                        |
| Semua alat   | `execution_time_exceeded` | Pemanggilan alat melebihi waktu eksekusi maksimum          |
| Semua alat   | `invalid_tool_input`      | Parameter yang diberikan ke alat tidak valid               |
| Semua alat   | `too_many_requests`       | "Rate limit" (batas laju) untuk penggunaan alat terlampaui |
| bash         | `output_file_too_large`   | Output perintah melebihi ukuran maksimum                   |
| text\_editor | `file_not_found`          | File tidak ada (untuk operasi view/edit)                   |

Container yang sudah kedaluwarsa tidak dapat digunakan kembali: permintaan yang merujuknya akan mengembalikan error alih-alih memulihkannya. Kirim ulang permintaan tanpa parameter `container` untuk mendapatkan container baru.

### Alasan berhenti `pause_turn`

Respons mungkin menyertakan alasan berhenti `pause_turn`, yang menunjukkan bahwa API menjeda giliran yang berjalan lama. Anda dapat memberikan respons tersebut kembali apa adanya dalam permintaan berikutnya agar Claude melanjutkan gilirannya, atau memodifikasi kontennya jika Anda ingin menginterupsi percakapan.

## Container

Alat eksekusi kode berjalan dalam lingkungan container yang aman yang dirancang khusus untuk eksekusi kode, dengan fokus lebih besar pada Python.

### Lingkungan runtime

* **Versi Python:** 3.11
* **Sistem operasi:** Container berbasis Linux
* **Arsitektur:** x86\_64 (AMD64)

### Batas sumber daya

* **Memori:** 5 GiB RAM
* **Ruang disk:** 5 GiB penyimpanan workspace
* **CPU:** 1 CPU
* **Waktu eksekusi:** Pemanggilan alat yang berjalan melewati waktu eksekusi maksimum mengembalikan [error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#errors) `execution_time_exceeded`. Dengan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), setiap sel REPL juga memiliki batas waktu nyata 90 detik

### Jaringan dan keamanan

* **Akses internet:** Dinonaktifkan sepenuhnya demi keamanan
* **Koneksi eksternal:** Tidak ada permintaan jaringan keluar yang diizinkan
* **Isolasi sandbox:** Isolasi penuh dari sistem host dan container lain
* **Akses file:** Terbatas hanya pada direktori workspace
* **Cakupan workspace:** Seperti [Files API](https://platform.claude.com/docs/id/build-with-claude/files), container dibatasi pada workspace permintaan
* **Kedaluwarsa:** Container kedaluwarsa 30 hari setelah dibuat

### Pustaka yang sudah terinstal

Lingkungan Python sandbox mencakup pustaka-pustaka yang umum digunakan berikut:

* **Ilmu data:** pandas, numpy, scipy, scikit-learn, statsmodels
* **Visualisasi:** matplotlib, seaborn
* **Pemrosesan file:** pyarrow, openpyxl, xlsxwriter, xlrd, pillow, python-pptx, python-docx, pypdf, pdfplumber, pypdfium2, pdf2image, pdfkit, tabula-py, reportlab\[pycairo], Img2pdf
* **Matematika dan komputasi:** sympy, mpmath
* **Utilitas:** tqdm, python-dateutil, pytz, joblib

Container juga menyertakan alat command-line seperti unzip, unrar, 7zip, bc, rg (ripgrep), fd, dan sqlite.

Container tidak memiliki akses internet, sehingga Claude tidak dapat mengunduh atau menginstal paket tambahan saat runtime: hanya pustaka yang sudah terinstal yang tersedia.

## Penggunaan ulang container

Anda dapat menggunakan kembali container yang sudah ada di beberapa permintaan API dengan memberikan ID container dari respons sebelumnya. Ini memungkinkan Anda mempertahankan file yang telah dibuat di antara permintaan. Dengan `code_execution_20260120` atau yang lebih baru dan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), status interpreter Python juga ikut bertahan.

Container kedaluwarsa 30 hari setelah dibuat. Setelah sekitar 5 menit tidak aktif, container akan di-checkpoint, dan mengirim permintaan dengan ID-nya dalam jangka waktu 30 hari akan memulihkannya. Stempel waktu `expires_at` dalam objek `container` pada respons adalah nilai bergulir yang lebih pendek dan tidak melaporkan batas 30 hari. Container yang sudah kedaluwarsa tidak dapat digunakan kembali. Kirim ulang permintaan tanpa parameter `container` untuk mendapatkan container baru.

### Contoh

<CodeGroup>
  ```bash cURL
  # Permintaan pertama: Buat file berisi angka acak, lalu ambil ID container (menggunakan jq)
  CONTAINER_ID=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
      "model": "claude-opus-5-5",
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
  # Permintaan pertama: Buat file berisi angka acak
  CONTAINER_ID=$(ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 4096 \
    --message '{role: user, content: Write a file with a random number and save it to "/tmp/number.txt"}' \
    --tool '{type: code_execution_20250825, name: code_execution}' \
    --transform container.id --raw-output)

  # Permintaan kedua: Gunakan kembali container untuk membaca file
  ant messages create \
    --container "$CONTAINER_ID" \
    --model claude-opus-5-5 \
    --max-tokens 4096 \
    --message '{role: user, content: Read the number from "/tmp/number.txt" and calculate its square}' \
    --tool '{type: code_execution_20250825, name: code_execution}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Permintaan pertama: buat file berisi angka acak di container baru
  response1 = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Write a file with a random number and save it to '/tmp/number.txt'",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Permintaan kedua: kirim kembali ID container agar Claude memakai ulang container yang sama
  response2 = client.messages.create(
      container=response1.container.id,
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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

  // Permintaan kedua: kirim kembali ID container agar container yang sama digunakan ulang
  const response2 = await client.messages.create({
    container: response1.container.id,
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Write a file with a random number and save it to '/tmp/number.txt'" }],
      Tools = [new CodeExecutionTool20250825()]
  });

  // Permintaan kedua: kirim kembali ID container agar Claude menggunakan ulang container yang sama
  var response2 = await client.Messages.Create(new()
  {
      Container = response1.Container!.ID,
      Model = Model.ClaudeOpus5_5,
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
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a file with a random number and save it to '/tmp/number.txt'")),
  	},
  	Tools: codeExecution,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Gunakan kembali container dari permintaan pertama agar file masih ada.
  response2, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfString: anthropic.String(response1.Container.ID),
  	},
  	Model:     anthropic.ModelClaudeOpus5_5,
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
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(4096L)
      .addUserMessage("Write a file with a random number and save it to '/tmp/number.txt'")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message response1 = client.messages().create(params1);

  // Permintaan kedua: kirim kembali ID container agar container yang sama digunakan ulang
  MessageCreateParams params2 = MessageCreateParams.builder()
      .container(response1.container().orElseThrow().id())
      .model(Model.CLAUDE_OPUS_5_5)
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
      model: Model::CLAUDE_OPUS_5_5,
      tools: [new CodeExecutionTool20250825()],
  );

  // Permintaan kedua: gunakan ulang container agar '/tmp/number.txt' masih ada
  $response2 = $client->messages->create(
      container: $response1->container->id,
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => "Read the number from '/tmp/number.txt' and calculate its square",
          ],
      ],
      model: Model::CLAUDE_OPUS_5_5,
      tools: [new CodeExecutionTool20250825()],
  );

  echo json_encode($response2), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Permintaan pertama: Claude membuat file di dalam container eksekusi kode yang baru
  response1 = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Write a file with a random number and save it to '/tmp/number.txt'"
      }
    ],
    tools: [Anthropic::CodeExecutionTool20250825.new]
  )

  # Permintaan kedua: kirim kembali ID container agar Claude memakai ulang container yang sama
  response2 = client.messages.create(
    container: response1.container.id,
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

Saat Anda menyediakan eksekusi kode bersama alat yang disediakan klien yang juga menjalankan kode (seperti [alat Bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool) atau REPL kustom), Claude beroperasi dalam lingkungan multikomputer. Alat eksekusi kode berjalan di container sandbox milik Anthropic, sedangkan alat yang disediakan klien Anda berjalan di lingkungan terpisah yang Anda kendalikan. Claude terkadang dapat tertukar antara lingkungan-lingkungan ini, mencoba menggunakan alat yang salah atau mengasumsikan bahwa status dibagikan di antara keduanya.

Untuk menghindari hal ini, tambahkan instruksi ke "system prompt" (prompt sistem) Anda yang memperjelas perbedaannya:

```text wrap
When multiple code execution environments are available, be aware that:
- Variables, files, and state do NOT persist between different execution environments
- Use the code_execution tool for general-purpose computation in Anthropic's sandboxed environment
- Use client-provided execution tools (e.g., bash) when you need access to the user's local system, files, or data
- If you need to pass results between environments, explicitly include outputs in subsequent tool calls rather than assuming shared state
```

Ini sangat penting saat menggabungkan eksekusi kode dengan [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), yang mengaktifkan eksekusi kode secara otomatis. Jika aplikasi Anda sudah menyediakan alat shell sisi klien, eksekusi kode otomatis akan menciptakan lingkungan eksekusi kedua yang perlu dibedakan oleh Claude.

Ketika Claude memanggil salah satu alat klien Anda bersamaan dengan eksekusi kode, API mengembalikan panggilan eksekusi kode tanpa hasilnya. Hasilnya tiba dalam respons berikutnya, setelah Anda mengirim kembali blok `tool_result` untuk alat klien Anda.

## Streaming

Dengan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) diaktifkan (`"stream": true`), Anda akan menerima event eksekusi kode saat event tersebut terjadi. Input sub-alat di-stream sebagai event `input_json_delta`, dan setiap blok hasil tiba secara utuh dalam satu event `content_block_start`:

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

Anda dapat menyertakan alat eksekusi kode dalam [Messages Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Panggilan alat eksekusi kode melalui Messages Batches API dikenakan harga yang sama dengan panggilan dalam permintaan Messages API biasa.

## Penggunaan dan harga

**Eksekusi kode gratis ketika digunakan bersama web search atau web fetch.** Ketika `web_search_20260209` (atau yang lebih baru) atau `web_fetch_20260209` (atau yang lebih baru) disertakan dalam permintaan API Anda, tidak ada biaya tambahan untuk pemanggilan alat eksekusi kode di luar biaya token input dan output standar.

Ketika digunakan tanpa alat-alat tersebut, eksekusi kode ditagih berdasarkan waktu eksekusi, yang dilacak secara terpisah dari penggunaan token:

* Waktu eksekusi memiliki minimum 5 menit
* Setiap organisasi menerima **1.550 jam gratis** penggunaan per bulan
* Penggunaan tambahan di atas 1.550 jam ditagih sebesar **$0,05 USD per jam, per kontainer**
* Jika file disertakan dalam permintaan, waktu eksekusi ditagih meskipun alat tidak dipanggil, karena file dimuat terlebih dahulu ke dalam kontainer

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

## Upgrade ke versi alat terbaru

Versi alat terbaru adalah `code_execution_20260521`. Untuk berpindah di antara ketiga versi saat ini, perbarui string `type` dalam permintaan Anda: ketiganya mengembalikan blok respons yang didokumentasikan dalam [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#response-format). Lihat [Versi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#tool-versions) untuk mengetahui apa yang ditambahkan setiap versi dan [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#compatibility) untuk model yang mendukungnya.

Bagian selanjutnya dari bagian ini membahas migrasi dari `code_execution_20250522` lama yang hanya mendukung Python ke versi alat saat ini.

### Apa yang berubah

| Komponen     | Lama                        | Saat ini                                                            |
| ------------ | --------------------------- | ------------------------------------------------------------------- |
| Header beta  | `code-execution-2025-05-22` | Tidak diperlukan                                                    |
| Tipe alat    | `code_execution_20250522`   | `code_execution_20250825` atau yang lebih baru                      |
| Kemampuan    | Hanya Python                | Perintah Bash, operasi file                                         |
| Tipe respons | `code_execution_result`     | `bash_code_execution_result`, `text_editor_code_execution_*_result` |

### Kompatibilitas mundur

* Semua eksekusi kode Python yang ada tetap berfungsi persis seperti sebelumnya
* Tidak diperlukan perubahan pada alur kerja yang hanya menggunakan Python

### Langkah-langkah upgrade

Untuk melakukan upgrade, perbarui tipe alat dalam permintaan API Anda:

```diff
- "type": "code_execution_20250522"
+ "type": "code_execution_20250825"
```

**Tinjau penanganan respons** (jika mem-parsing respons secara terprogram):

* API tidak lagi mengirim blok sebelumnya untuk respons eksekusi Python
* Sebagai gantinya, API mengirim tipe respons baru untuk operasi Bash dan file (lihat [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#response-format))

## Retensi data

Eksekusi kode berjalan di container sandbox sisi server. Data container, termasuk artefak eksekusi, file yang diunggah, dan output, disimpan hingga 30 hari. Retensi ini berlaku untuk semua data yang diproses di dalam lingkungan container. File yang dibuat oleh eksekusi kode di [Files API](https://platform.claude.com/docs/id/build-with-claude/files) (dapat diambil dengan `client.files.download()` (csharp, go: `client.Files.Download()`; java: `client.files().download()`; php: `$client->files->download()`)) tetap tersimpan hingga dihapus secara eksplisit.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat advisor" icon="compass" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool">
    Pasangkan model eksekutor yang lebih cepat dengan model advisor berkecerdasan lebih tinggi yang memberikan panduan strategis di tengah proses generasi.
  </Card>

  <Card title="Pemanggilan alat terprogram" icon="code" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling">
    Panggil alat Anda sendiri dari kode yang berjalan di dalam container eksekusi kode.
  </Card>

  <Card title="Files API" icon="file" href="https://platform.claude.com/docs/id/build-with-claude/files">
    Unggah file untuk dianalisis dan unduh file yang dibuat oleh eksekusi kode.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="book" href="https://platform.claude.com/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>
</CardGroup>
