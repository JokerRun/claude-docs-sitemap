---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/files
fetched_at: 2026-07-14T03:07:36.677443Z
sha256: e93d3e9e18bfe1aeb5c9283e6e57b399ef8d5a4c4cdf8822157ac15eacf7966a
---

# Files API

Unggah file sekali, referensikan dengan file_id dalam permintaan Messages, dan unduh output yang dibuat oleh skills atau alat eksekusi kode.

---

Files API memungkinkan Anda mengunggah dan mengelola file untuk digunakan dengan Claude API tanpa mengunggah ulang konten pada setiap permintaan. Ini sangat berguna saat menggunakan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk menyediakan input (misalnya, dataset dan dokumen) dan kemudian mengunduh output (misalnya, grafik). Anda dapat [menjelajahi referensi API secara langsung](/docs/id/api/beta/files/upload), selain panduan ini.

<Note>
  Files API berada dalam tahap beta. Hubungi kami melalui [formulir umpan balik](https://forms.gle/tisHyierGwgN4DUE9) untuk berbagi pengalaman Anda dengan Files API.
</Note>

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Model yang didukung

Mereferensikan `file_id` dalam permintaan Messages didukung pada semua model yang mendukung tipe file yang diberikan. [Gambar](/docs/id/build-with-claude/vision) didukung pada semua model Claude saat ini. Untuk [PDF](/docs/id/build-with-claude/pdf-support) dan [tipe file lainnya dengan alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility), lihat halaman yang ditautkan untuk dukungan model.

Files API tersedia di Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, Files API memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Saat ini belum tersedia di Amazon Bedrock atau Google Cloud.

## Cara kerja Files API

Files API menyediakan pendekatan buat-sekali, gunakan-berkali-kali untuk bekerja dengan file:

* **Unggah file** ke penyimpanan aman Anthropic dan terima `file_id` yang unik
* **Unduh file** yang dibuat oleh skills atau alat eksekusi kode
* **Referensikan file** dalam permintaan [Messages](/docs/id/api/messages/create) menggunakan `file_id` alih-alih mengunggah ulang konten
* **Kelola file Anda** dengan operasi list, retrieve, dan delete

## Cara menggunakan Files API

<Note>
  Untuk menggunakan Files API, Anda perlu menyertakan header fitur beta: `anthropic-beta: files-api-2025-04-14`. SDK menambahkan header ini secara otomatis saat Anda memanggil metode pada namespace `beta.files`, sehingga contoh SDK di halaman ini tidak meneruskannya secara eksplisit untuk operasi file. Permintaan Messages yang mereferensikan file memang memerlukannya, yang diteruskan oleh contoh SDK melalui parameter `betas` mereka.
</Note>

### Mengunggah file

Unggah file untuk direferensikan dalam panggilan API di masa mendatang:

<CodeGroup>
  ```bash cURL
  FILE_ID=$(curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@/path/to/document.pdf" | jq -r '.id')
  echo "$FILE_ID"
  ```

  ```bash CLI
  FILE_ID=$(ant beta:files upload \
    --file /path/to/document.pdf \
    --transform id \
    --raw-output)
  echo "$FILE_ID"
  ```

  ```python Python
  uploaded = client.beta.files.upload(
      file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
  )
  file_id = uploaded.id
  print(file_id)
  ```

  ```typescript TypeScript
  const uploaded = await client.beta.files.upload({
    file: await toFile(
      fs.createReadStream("/path/to/document.pdf"),
      undefined,
      { type: "application/pdf" },
    ),
  });
  console.log(uploaded.id);
  ```

  ```csharp C#
  var uploaded = await client.Beta.Files.Upload(
      new FileUploadParams
      {
          File = new BinaryContent
          {
              Stream = File.OpenRead("/path/to/document.pdf"),
              FileName = "document.pdf",
              ContentType = new("application/pdf")
          }
      });

  var fileId = uploaded.ID;
  Console.WriteLine(fileId);
  ```

  ```go Go
  f, err := os.Open("/path/to/document.pdf")
  if err != nil {
  	log.Fatal(err)
  }
  defer f.Close()

  response, err := client.Beta.Files.Upload(context.Background(),
  	anthropic.BetaFileUploadParams{
  		File: anthropic.File(f, "document.pdf", "application/pdf"),
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fileID := response.ID
  fmt.Println(fileID)
  ```

  ```java Java
  FileMetadata file = client.beta().files().upload(
      FileUploadParams.builder()
          .file(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("/path/to/document.pdf")))
              .filename("document.pdf")
              .contentType("application/pdf")
              .build())
          .build()
  );

  String fileId = file.id();
  System.out.println(fileId);
  ```

  ```php PHP
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
  );

  $fileId = $file->id;
  echo $fileId;
  ```

  ```ruby Ruby
  file = client.beta.files.upload(
    file: Anthropic::FilePart.new(
      Pathname("/path/to/document.pdf"),
      content_type: "application/pdf"
    )
  )

  file_id = file.id
  puts file_id
  ```
</CodeGroup>

Respons dari pengunggahan file mencakup:

```json Response
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1024000,
  "created_at": "2025-01-01T00:00:00Z",
  "downloadable": false
}
```

`downloadable` bernilai `false` untuk file yang Anda unggah. Hanya file yang dibuat oleh [skills](/docs/id/build-with-claude/skills-guide) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang dapat diunduh. Lihat [Mengunduh file](#downloading-a-file).

### Menggunakan file dalam pesan

Setelah diunggah, referensikan file dengan meneruskan `id` dari respons unggahan sebagai `file_id`:

<CodeGroup>
  ```bash cURL
  curl -X POST https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Please summarize this document for me."
          },
          {
            "type": "document",
            "source": {
              "type": "file",
              "file_id": "$FILE_ID"
            }
          }
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:messages create --beta files-api-2025-04-14 <<YAML
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: text
          text: Please summarize this document for me.
        - type: document
          source:
            type: file
            file_id: $FILE_ID
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": "Please summarize this document for me."},
                  {
                      "type": "document",
                      "source": {
                          "type": "file",
                          "file_id": file_id,
                      },
                  },
              ],
          }
      ],
      betas=["files-api-2025-04-14"],
  )
  print(response)
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Please summarize this document for me.",
          },
          {
            type: "document",
            source: {
              type: "file",
              file_id: uploaded.id,
            },
          },
        ],
      },
    ],
    betas: ["files-api-2025-04-14"],
  });

  console.log(response);
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Betas = [AnthropicBeta.FilesApi2025_04_14],
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = new List<BetaContentBlockParam>
                  {
                      new BetaTextBlockParam { Text = "Please summarize this document for me." },
                      new BetaRequestDocumentBlock
                      {
                          Source = new BetaFileDocumentSource { FileID = fileId }
                      }
                  }
              }
          ]
      });

  Console.WriteLine(response);
  ```

  ```go Go
  msg, err := client.Beta.Messages.New(context.Background(),
  	anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(
  				anthropic.NewBetaTextBlock("Please summarize this document for me."),
  				anthropic.NewBetaDocumentBlock(anthropic.BetaFileDocumentSourceParam{
  					FileID: fileID,
  				}),
  			),
  		},
  	})
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(msg)
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .addBeta("files-api-2025-04-14")
      .maxTokens(1024)
      .addUserMessageOfBetaContentBlockParams(List.of(
          BetaContentBlockParam.ofText(BetaTextBlockParam.builder()
              .text("Please summarize this document for me.")
              .build()),
          BetaContentBlockParam.ofDocument(BetaRequestDocumentBlock.builder()
              .source(BetaFileDocumentSource.builder()
                  .fileId(fileId)
                  .build())
              .build())
      ))
      .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message);
  ```

  ```php PHP
  $response = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  ['type' => 'text', 'text' => 'Please summarize this document for me.'],
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'file',
                          'file_id' => $fileId
                      ]
                  ]
              ]
          ]
      ],
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
  );

  print_r($response);
  ```

  ```ruby Ruby
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    betas: ["files-api-2025-04-14"],
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Please summarize this document for me." },
          {
            type: "document",
            source: {
              type: "file",
              file_id: file_id
            }
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

### Tipe file dan blok konten

Files API mendukung berbagai tipe file yang sesuai dengan tipe blok konten yang berbeda:

| Tipe file                                                                                                    | Tipe MIME                                            | Tipe blok konten   | Kasus penggunaan                       |
| ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------ | -------------------------------------- |
| PDF                                                                                                          | `application/pdf`                                    | `document`         | Analisis teks, pemrosesan dokumen      |
| Teks biasa                                                                                                   | `text/plain`                                         | `document`         | Analisis teks, pemrosesan              |
| Gambar                                                                                                       | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image`            | Analisis gambar, tugas visual          |
| [Dataset, lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) | Bervariasi                                           | `container_upload` | Menganalisis data, membuat visualisasi |

#### Blok dokumen

Untuk PDF dan file teks, gunakan blok konten `document`:

```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
  },
  "title": "Document Title", // Optional
  "context": "Context about the document", // Optional
  "citations": { "enabled": true } // Optional, enables citations
}
```

#### Blok gambar

Untuk gambar, gunakan blok konten `image`:

```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w"
  }
}
```

#### Blok container upload

Untuk mengirim file ke [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files), gunakan blok konten `container_upload`:

```json
{
  "type": "container_upload",
  "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
}
```

### Bekerja dengan format file lainnya

Untuk tipe file yang tidak didukung oleh blok `document` (misalnya, .docx dan .xlsx), konversikan file tersebut ke teks biasa dan sertakan kontennya langsung dalam pesan Anda. File yang sudah berupa teks biasa, seperti file .csv dan .md, dapat dibaca dengan cara ini atau diunggah melalui Files API dengan tipe konten `text/plain` secara eksplisit. Untuk menganalisis dataset alih-alih membacanya sebagai teks, unggah dataset tersebut untuk [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) menggunakan blok `container_upload`.

Contoh berikut membaca file teks dan mengirim isinya sebagai teks biasa:

<CodeGroup>
  ```bash cURL
  # Baca file teks
  # Catatan: Untuk file dengan karakter khusus, pertimbangkan encoding base64
  TEXT_CONTENT=$(cat document.txt)

  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @- <<EOF
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Here's the document content:\n\n${TEXT_CONTENT}\n\nPlease summarize this document."
          }
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  # Referensi "@./path" menyisipkan isi file secara langsung ke dalam field tersebut.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --transform 'content.0.text' \
    --raw-output <<'YAML'
  messages:
    - role: user
      content:
        - type: text
          text: "Here's the document content:"
        - type: text
          text: "@./document.txt"
        - type: text
          text: "Please summarize this document."
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Baca file teks
  with open("document.txt") as f:
      text_content = f.read()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": f"Here's the document content:\n\n{text_content}\n\nPlease summarize this document.",
                  }
              ],
          }
      ],
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  import fs from "node:fs/promises";
  // ...
  const client = new Anthropic();

  // Baca file teks
  const textContent = await fs.readFile("document.txt", "utf-8");

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: `Here's the document content:\n\n${textContent}\n\nPlease summarize this document.`
          }
        ]
      }
    ]
  });

  const block = response.content[0];
  if (block.type === "text") {
    console.log(block.text);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Baca file teks
  string textContent = await File.ReadAllTextAsync("document.txt");

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new()
      {
          Role = Role.User,
          Content = $"Here's the document content:\n\n{textContent}\n\nPlease summarize this document."
      }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Baca file teks
  textContent, err := os.ReadFile("document.txt")
  if err != nil {
  	log.Fatal(err)
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			fmt.Sprintf("Here's the document content:\n\n%s\n\nPlease summarize this document.", string(textContent)),
  		)),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Baca file teks
  String textContent = Files.readString(Path.of("document.txt"));

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("Here's the document content:\n\n" + textContent + "\n\nPlease summarize this document.")
      .build();

  Message response = client.messages().create(params);
  response.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  // Baca file teks
  $textContent = file_get_contents("document.txt");

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => "Here's the document content:\n\n{$textContent}\n\nPlease summarize this document."
                  ]
              ]
          ]
      ],
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Baca file teks
  text_content = File.read("document.txt")

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Here's the document content:\n\n#{text_content}\n\nPlease summarize this document."
          }
        ]
      }
    ]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Note>
  Untuk file .docx yang berisi gambar, konversikan terlebih dahulu ke format PDF, lalu gunakan [dukungan PDF](/docs/id/build-with-claude/pdf-support) untuk memanfaatkan penguraian gambar bawaan. Ini memungkinkan penggunaan sitasi dari dokumen PDF.
</Note>

### Mengelola file

#### Menampilkan daftar file

Ambil daftar file yang telah Anda unggah. Endpoint ini dipaginasi: setiap permintaan mengembalikan hingga `limit` file (20 secara default), dan parameter `before_id` serta `after_id` mengambil halaman yang berdekatan. Lihat [referensi List Files API](/docs/id/api/beta/files/list). SDK mengembalikan halaman pertama dan menyediakan helper paginasi otomatis. Contoh CLI membatasi total dengan `--max-items`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files list \
    --max-items 10
  ```

  ```python Python
  client = anthropic.Anthropic()
  files = client.beta.files.list()
  print(files)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const files = await client.beta.files.list();
  console.log(files);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var files = await client.Beta.Files.List();
  Console.WriteLine(files);
  ```

  ```go Go
  client := anthropic.NewClient()

  files, err := client.Beta.Files.List(context.TODO(), anthropic.BetaFileListParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(files)
  ```

  ```java Java
  import com.anthropic.models.beta.files.FileListPage;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      FileListPage files = client.beta().files().list();
      System.out.println(files);
  }
  ```

  ```php PHP
  $client = new Client();

  $files = $client->beta->files->list();
  print_r($files);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  files = client.beta.files.list
  puts files
  ```
</CodeGroup>

#### Mendapatkan metadata file

Ambil informasi tentang file tertentu:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files retrieve-metadata \
    --file-id "$FILE_ID"
  ```

  ```python Python
  file = client.beta.files.retrieve_metadata(file_id)
  print(file)
  ```

  ```typescript TypeScript
  const file = await client.beta.files.retrieveMetadata(uploaded.id);
  console.log(file);
  ```

  ```csharp C#
  var file = await client.Beta.Files.RetrieveMetadata(fileId);
  Console.WriteLine(file);
  ```

  ```go Go
  metadata, err := client.Beta.Files.GetMetadata(
  	context.TODO(),
  	fileID,
  	anthropic.BetaFileGetMetadataParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(metadata)
  ```

  ```java Java
  FileMetadata metadata = client.beta().files().retrieveMetadata(fileId);

  System.out.println(metadata);
  ```

  ```php PHP
  $file = $client->beta->files->retrieveMetadata($fileId);
  echo $file;
  ```

  ```ruby Ruby
  file = client.beta.files.retrieve_metadata(file_id)
  puts file
  ```
</CodeGroup>

#### Menghapus file

Hapus file dari workspace Anda:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files delete \
    --file-id "$FILE_ID"
  ```

  ```python Python
  client.beta.files.delete(file_id)
  ```

  ```typescript TypeScript
  await client.beta.files.delete(uploaded.id);
  ```

  ```csharp C#
  await client.Beta.Files.Delete(fileId);
  ```

  ```go Go
  _, err = client.Beta.Files.Delete(
  	context.TODO(),
  	fileID,
  	anthropic.BetaFileDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  client.beta().files().delete(fileId);
  ```

  ```php PHP
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client.beta.files.delete(file_id)
  ```
</CodeGroup>

### Mengunduh file

Unduh file yang dibuat oleh [skills](/docs/id/build-with-claude/skills-guide) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool). File yang Anda unggah tidak dapat diunduh. `file_id` dari file yang dihasilkan muncul di [blok konten `code_execution_tool_result`](/docs/id/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) dari respons Messages yang membuatnya:

<CodeGroup>
  ```bash cURL
  curl -X GET "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    --output downloaded_file.txt
  ```

  ```bash CLI
  ant beta:files download \
    --file-id "$FILE_ID" \
    --output downloaded_file.txt
  ```

  ```python Python
  file_content = client.beta.files.download(file_id)

  file_content.write_to_file("downloaded_file.txt")
  ```

  ```typescript TypeScript
  const content = await client.beta.files.download(uploaded.id);

  const bytes = Buffer.from(await content.arrayBuffer());
  await fsp.writeFile("downloaded_file.txt", bytes);
  ```

  ```csharp C#
  using var fileContent = await client.Beta.Files.Download(fileId);
  await using var source = await fileContent.ReadAsStream();
  await using var destination = File.Create("downloaded_file.txt");
  await source.CopyToAsync(destination);
  ```

  ```go Go
  func downloadFile(client anthropic.Client, fileID string) error {
  	resp, err := client.Beta.Files.Download(
  		context.TODO(),
  		fileID,
  		anthropic.BetaFileDownloadParams{},
  	)
  	if err != nil {
  		return err
  	}
  	defer resp.Body.Close()

  	fileContent, err := io.ReadAll(resp.Body)
  	if err != nil {
  		return err
  	}

  	return os.WriteFile("downloaded_file.txt", fileContent, 0644)
  }

  ```

  ```java Java
  try (HttpResponse response = client.beta().files().download(fileId)) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("downloaded_file.txt"),
              StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  $fileContent = $client->beta->files->download($fileId);

  file_put_contents("downloaded_file.txt", $fileContent);
  ```

  ```ruby Ruby
  file_content = client.beta.files.download(file_id)

  File.binwrite("downloaded_file.txt", file_content.read)
  ```
</CodeGroup>

<Note>
  File hanya dapat diunduh jika metadatanya menunjukkan `"downloadable": true`, yang berlaku untuk file yang dibuat oleh skills atau alat eksekusi kode. Mengunduh file yang Anda unggah akan mengembalikan error 400.
</Note>

## Penyimpanan dan batasan file

### Batasan penyimpanan

* **Ukuran file maksimum:** 500 MB per file
* **Total penyimpanan:** 500 GB per organisasi

### Siklus hidup file

* File dibatasi pada workspace dari kunci API yang mengunggahnya. Kunci API mana pun dalam workspace yang sama dapat mereferensikannya
* File tidak dapat dimodifikasi atau diganti namanya setelah diunggah. Untuk mengubah konten file, unggah file baru dan hapus file lama
* File tetap ada sampai Anda menghapusnya dengan endpoint `DELETE /v1/files/{file_id}`
* File yang dihapus tidak dapat dipulihkan
* File tidak dapat diakses melalui API segera setelah penghapusan, tetapi file tersebut mungkin tetap ada dalam panggilan Messages API yang aktif dan penggunaan alat terkait
* File yang dihapus pengguna akan dihapus sesuai dengan [kebijakan retensi data](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) Anthropic. Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention)

## Penanganan error

Error umum saat menggunakan Files API meliputi:

* **File tidak ditemukan (404):** `file_id` yang ditentukan tidak ada atau Anda tidak memiliki akses ke file tersebut
* **Tipe file tidak valid (400):** Tipe file tidak cocok dengan tipe blok konten (misalnya, menggunakan file gambar dalam blok dokumen)
* **Tidak dapat diunduh (400):** File yang Anda unggah memiliki `"downloadable": false` dan tidak dapat diunduh. Hanya file yang dibuat oleh skills atau alat eksekusi kode yang dapat diunduh
* **Melebihi ukuran jendela konteks (400):** File lebih besar dari ukuran jendela konteks (misalnya, menggunakan file teks biasa 500 MB dalam permintaan `/v1/messages`)
* **Nama file tidak valid (400):** Nama file tidak memenuhi persyaratan panjang (1-255 karakter) atau mengandung karakter terlarang (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, atau karakter Unicode 0-31)
* **File terlalu besar (413):** File melebihi batas 500 MB
* **Batas penyimpanan terlampaui (400):** Organisasi Anda telah mencapai batas penyimpanan 500 GB

```json Output
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "File `file_011CNha8iCJcU1wXNR6q4V8w` not found."
  },
  "request_id": "req_011CQFYcrRp7mCHLDsAYT8Qt"
}
```

## Penggunaan dan penagihan

Operasi Files API gratis:

* Mengunggah file
* Mengunduh file
* Menampilkan daftar file
* Mendapatkan metadata file
* Menghapus file

Konten file yang digunakan dalam permintaan Messages dikenakan biaya sebagai token input.

### Batas laju

Selama periode beta:

* Panggilan API terkait file dibatasi hingga sekitar 100 permintaan per menit
* [Hubungi kami](mailto:sales@anthropic.com) jika Anda memerlukan batas yang lebih tinggi untuk kasus penggunaan Anda

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Dukungan PDF" icon="file" href="/docs/id/build-with-claude/pdf-support">
    Proses PDF dengan Claude. Ekstrak teks, analisis grafik, dan pahami konten visual dari dokumen Anda.
  </Card>

  <Card title="Alat eksekusi kode" icon="terminal" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan mengiterasi solusi.
  </Card>

  <Card title="Vision" icon="image" href="/docs/id/build-with-claude/vision">
    Proses dan analisis input visual serta hasilkan teks dan kode dari gambar.
  </Card>
</CardGroup>
