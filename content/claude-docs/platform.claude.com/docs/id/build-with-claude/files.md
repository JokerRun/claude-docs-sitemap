---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/files
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 9b8b22120f5f190f59ba9d848c966fbf15f2d418c96cf73b0b3eff25e9170e0b
---

# Files API

---

Files API memungkinkan Anda mengunggah dan mengelola file untuk digunakan dengan Claude API tanpa harus mengunggah ulang konten pada setiap permintaan. Ini sangat berguna saat menggunakan [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk menyediakan input (misalnya dataset dan dokumen) lalu mengunduh output (misalnya grafik). Anda juga dapat menggunakan Files API untuk menghindari keharusan mengunggah ulang dokumen dan gambar yang sering digunakan secara terus-menerus di beberapa panggilan API. Anda dapat [menjelajahi referensi API secara langsung](/docs/id/api/files-create), selain panduan ini.

<Note>
  Files API masih dalam tahap beta. Hubungi kami melalui [formulir umpan balik](https://forms.gle/tisHyierGwgN4DUE9) untuk berbagi pengalaman Anda dengan Files API.
</Note>

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Model yang didukung

Mereferensikan `file_id` dalam permintaan Messages didukung pada semua model yang mendukung tipe file tersebut. [Gambar](/docs/id/build-with-claude/vision) didukung pada semua model Claude saat ini. Untuk [PDF](/docs/id/build-with-claude/pdf-support) dan [tipe file lainnya dengan code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility), lihat halaman yang ditautkan untuk dukungan model.

Files API tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Saat ini belum tersedia di Amazon Bedrock atau Vertex AI.

## Cara kerja Files API

Files API menyediakan pendekatan sederhana buat-sekali, gunakan-berkali-kali untuk bekerja dengan file:

* **Unggah file** ke penyimpanan aman Anthropic dan terima `file_id` yang unik
* **Unduh file** yang dibuat dari skills atau code execution tool
* **Referensikan file** dalam permintaan [Messages](/docs/id/api/messages/create) menggunakan `file_id` alih-alih mengunggah ulang konten
* **Kelola file Anda** dengan operasi list, retrieve, dan delete

## Cara menggunakan Files API

<Note>
  Untuk menggunakan Files API, Anda perlu menyertakan header fitur beta: `anthropic-beta: files-api-2025-04-14`.
</Note>

### Mengunggah file

Unggah file untuk direferensikan dalam panggilan API di masa mendatang:

<CodeGroup>
  ```bash cURL
  curl -X POST https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -F "file=@/path/to/document.pdf"
  ```

  ```bash CLI
  FILE_ID=$(ant beta:files upload \
    --file /path/to/document.pdf \
    --transform id --raw-output)
  ```

  ```python Python
  uploaded = client.beta.files.upload(
      file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
  )
  ```

  ```typescript TypeScript
  const uploaded = await client.beta.files.upload({
    file: await toFile(
      fs.createReadStream("/path/to/document.pdf"),
      undefined,
      { type: "application/pdf" },
    ),
  });
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

  Console.WriteLine(uploaded.ID);
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

  fmt.Println(response.ID)
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

  System.out.println(file.id());
  ```

  ```php PHP
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
  );

  echo $file->id;
  ```

  ```ruby Ruby
  file = client.beta.files.upload(
    file: Anthropic::FilePart.new(
      Pathname("/path/to/document.pdf"),
      content_type: "application/pdf"
    )
  )

  puts file.id
  ```
</CodeGroup>

Respons dari pengunggahan file akan mencakup:

```json Output
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

### Menggunakan file dalam messages

Setelah diunggah, referensikan file menggunakan `file_id`-nya:

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
          Model = Messages::Model.ClaudeOpus4_6,
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
  		Model:     anthropic.ModelClaudeOpus4_6,
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

### Tipe file dan content block

Files API mendukung berbagai tipe file yang sesuai dengan tipe content block yang berbeda:

| Tipe File                                                                                                    | MIME Type                                            | Tipe Content Block | Kasus Penggunaan                       |
| ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------ | -------------------------------------- |
| PDF                                                                                                          | `application/pdf`                                    | `document`         | Analisis teks, pemrosesan dokumen      |
| Teks biasa                                                                                                   | `text/plain`                                         | `document`         | Analisis teks, pemrosesan              |
| Gambar                                                                                                       | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image`            | Analisis gambar, tugas visual          |
| [Dataset, lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) | Bervariasi                                           | `container_upload` | Menganalisis data, membuat visualisasi |

### Bekerja dengan format file lainnya

Untuk tipe file yang tidak didukung sebagai blok `document` (.csv, .txt, .md, .docx, .xlsx), konversikan file ke teks biasa, dan sertakan kontennya langsung dalam pesan Anda:

<CodeGroup>
  ```bash cURL
  # Contoh: Membaca file teks dan mengirimnya sebagai teks biasa
  # Catatan: Untuk file dengan karakter khusus, pertimbangkan encoding base64
  # ...
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
  # Referensi "@./path" menyisipkan isi file secara langsung ke dalam field.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --transform 'content.0.text' --raw-output <<'YAML'
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
  import pandas as pd
  # ...
  # Contoh: Membaca file CSV
  df = pd.read_csv("data.csv")
  csv_content = df.to_string()

  # Kirim sebagai teks biasa dalam pesan
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": f"Here's the CSV data:\n\n{csv_content}\n\nPlease analyze this data.",
                  }
              ],
          }
      ],
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  import fs from "fs/promises";

  const anthropic = new Anthropic();

  async function analyzeDocument() {
    // Contoh: Membaca file teks
    const textContent = await fs.readFile("document.txt", "utf-8");

    // Kirim sebagai teks biasa dalam pesan
    const response = await anthropic.messages.create({
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
  }

  analyzeDocument();
  ```

  ```csharp C#
  using System;
  using System.IO;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          // Contoh: Membaca file teks
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
      }
  }
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

  	// Contoh: Membaca file teks
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
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Contoh: Membaca file teks
  String textContent = Files.readString(Paths.get("document.txt"));

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

  // Contoh: Membaca file teks
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

  # Contoh: Membaca file teks
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
  Untuk file .docx yang berisi gambar, konversikan terlebih dahulu ke format PDF, lalu gunakan [dukungan PDF](/docs/id/build-with-claude/pdf-support) untuk memanfaatkan parsing gambar bawaan. Ini memungkinkan penggunaan sitasi dari dokumen PDF.
</Note>

#### Blok document

Untuk PDF dan file teks, gunakan content block `document`:

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

#### Blok image

Untuk gambar, gunakan content block `image`:

```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w"
  }
}
```

### Mengelola file

#### Menampilkan daftar file

Ambil daftar file yang telah Anda unggah:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```

  ```bash CLI
  ant beta:files list
  ```

  ```python Python
  client = anthropic.Anthropic()
  files = client.beta.files.list()
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();
  const files = await anthropic.beta.files.list();
  ```

  ```csharp C#
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Files;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var files = await client.Beta.Files.List();
          Console.WriteLine(files);
      }
  }
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
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          FileListPage files = client.beta().files().list();
          System.out.println(files);
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
  ```

  ```typescript TypeScript
  const file = await client.beta.files.retrieveMetadata(uploaded.id);
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
  result = client.beta.files.delete(file_id)
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
  $result = $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  result = client.beta.files.delete(file_id)
  ```
</CodeGroup>

### Mengunduh file

Unduh file yang telah dibuat oleh skills atau code execution tool:

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

  # Save to file
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
  Anda hanya dapat mengunduh file yang dibuat oleh [skills](/docs/id/build-with-claude/skills-guide) atau [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool). File yang Anda unggah tidak dapat diunduh.
</Note>

***

## Penyimpanan dan batasan file

### Batasan penyimpanan

* **Ukuran file maksimum:** 500 MB per file
* **Total penyimpanan:** 500 GB per organisasi

### Siklus hidup file

* File dibatasi pada workspace dari kunci API. Kunci API lain dapat menggunakan file yang dibuat oleh kunci API lain mana pun yang terkait dengan workspace yang sama
* File tetap ada hingga Anda menghapusnya
* File yang dihapus tidak dapat dipulihkan
* File tidak dapat diakses melalui API sesaat setelah penghapusan, tetapi mungkin masih ada dalam panggilan API `Messages` yang aktif dan penggunaan alat terkait
* File yang dihapus pengguna akan dihapus sesuai dengan [kebijakan retensi data](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) Anthropic.

***

## Retensi data

File yang diunggah melalui Files API disimpan hingga dihapus secara eksplisit menggunakan endpoint `DELETE /v1/files/{file_id}`. File disimpan untuk digunakan kembali di beberapa permintaan API.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Penanganan error

Error umum saat menggunakan Files API meliputi:

* **File not found (404):** `file_id` yang ditentukan tidak ada atau Anda tidak memiliki akses ke file tersebut
* **Invalid file type (400):** Tipe file tidak cocok dengan tipe content block (misalnya, menggunakan file gambar dalam blok document)
* **Exceeds context window size (400):** File lebih besar dari ukuran jendela konteks (misalnya menggunakan file teks biasa 500 MB dalam permintaan `/v1/messages`)
* **Invalid filename (400):** Nama file tidak memenuhi persyaratan panjang (1-255 karakter) atau berisi karakter terlarang (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, atau karakter unicode 0-31)
* **File too large (413):** File melebihi batas 500 MB
* **Storage limit exceeded (403):** Organisasi Anda telah mencapai batas penyimpanan 500 GB

```json Output
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "File not found: file_011CNha8iCJcU1wXNR6q4V8w"
  }
}
```

## Penggunaan dan penagihan

Operasi File API bersifat **gratis**:

* Mengunggah file
* Mengunduh file
* Menampilkan daftar file
* Mendapatkan metadata file
* Menghapus file

Konten file yang digunakan dalam permintaan `Messages` dikenakan biaya sebagai token input. Anda hanya dapat mengunduh file yang dibuat oleh [skills](/docs/id/build-with-claude/skills-guide) atau [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool).

### Batas laju

Selama periode beta:

* Panggilan API terkait file dibatasi sekitar 100 permintaan per menit
* [Hubungi kami](mailto:sales@anthropic.com) jika Anda memerlukan batas yang lebih tinggi untuk kasus penggunaan Anda
