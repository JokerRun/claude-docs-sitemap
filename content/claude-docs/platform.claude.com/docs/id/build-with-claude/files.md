---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/files
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: d01992ea35dae9609e42c48216cd44eceec7e5785d5a9a7b95b26476c8242d14
---

# Files API

---

Files API memungkinkan Anda mengunggah dan mengelola file untuk digunakan dengan Claude API tanpa perlu mengunggah ulang konten pada setiap permintaan. Ini sangat berguna saat menggunakan [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk menyediakan input (misalnya dataset dan dokumen) lalu mengunduh output (misalnya grafik). Anda juga dapat menggunakan Files API untuk menghindari keharusan mengunggah ulang dokumen dan gambar yang sering digunakan secara terus-menerus di berbagai panggilan API. Anda dapat [menjelajahi referensi API secara langsung](/docs/id/api/files-create), selain panduan ini.

<Note>
Files API masih dalam versi beta. Hubungi kami melalui [formulir umpan balik](https://forms.gle/tisHyierGwgN4DUE9) untuk membagikan pengalaman Anda dengan Files API.
</Note>

<Note>
Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Model yang didukung \{#supported-models}

Mereferensikan `file_id` dalam permintaan Messages didukung pada semua model yang mendukung tipe file tersebut. [Gambar](/docs/id/build-with-claude/vision) didukung pada semua model Claude saat ini. Untuk [PDF](/docs/id/build-with-claude/pdf-support) dan [tipe file lainnya dengan code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility), lihat halaman yang ditautkan untuk dukungan model.

Files API tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Saat ini belum tersedia di Amazon Bedrock atau Vertex AI.

## Cara kerja Files API \{#how-the-files-api-works}

Files API menyediakan pendekatan sederhana buat-sekali, gunakan-berkali-kali untuk bekerja dengan file:

- **Unggah file** ke penyimpanan aman Anthropic dan terima `file_id` yang unik
- **Unduh file** yang dibuat dari skill atau code execution tool
- **Referensikan file** dalam permintaan [Messages](/docs/id/api/messages/create) menggunakan `file_id` alih-alih mengunggah ulang konten
- **Kelola file Anda** dengan operasi list, retrieve, dan delete

## Cara menggunakan Files API \{#how-to-use-the-files-api}

<Note>
Untuk menggunakan Files API, Anda perlu menyertakan header fitur beta: `anthropic-beta: files-api-2025-04-14`.
</Note>

### Mengunggah file \{#uploading-a-file}

Unggah file untuk direferensikan dalam panggilan API di masa mendatang:

<CodeGroup>

````bash
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@/path/to/document.pdf"
````

````bash
FILE_ID=$(ant beta:files upload \
  --file /path/to/document.pdf \
  --transform id --raw-output)
````

````python
uploaded = client.beta.files.upload(
    file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
)
````

````typescript
const uploaded = await client.beta.files.upload({
  file: await toFile(
    fs.createReadStream("/path/to/document.pdf"),
    undefined,
    { type: "application/pdf" },
  ),
});
````

````csharp
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
````

````go
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
````

````java
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
````

````php
$file = $client->beta->files->upload(
    FileParam::fromResource(fopen('/path/to/document.pdf', 'rb'), contentType: 'application/pdf'),
);

echo $file->id;
````

````ruby
file = client.beta.files.upload(
  file: Anthropic::FilePart.new(
    Pathname("/path/to/document.pdf"),
    content_type: "application/pdf"
  )
)

puts file.id
````

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

### Menggunakan file dalam messages \{#using-a-file-in-messages}

Setelah diunggah, referensikan file menggunakan `file_id`-nya:

<CodeGroup>

````bash
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
````

````bash
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
````

````python
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
````

````typescript
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
````

````csharp
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
````

````go
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
````

````java
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
````

````php
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
````

````ruby
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
````

</CodeGroup>

### Tipe file dan blok konten \{#file-types-and-content-blocks}

Files API mendukung berbagai tipe file yang sesuai dengan tipe blok konten yang berbeda:

| Tipe File | MIME Type | Tipe Blok Konten | Kasus Penggunaan |
| :--- | :--- | :--- | :--- |
| PDF | `application/pdf` | `document` | Analisis teks, pemrosesan dokumen |
| Teks biasa | `text/plain` | `document` | Analisis teks, pemrosesan |
| Gambar | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image` | Analisis gambar, tugas visual |
| [Dataset, lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#upload-and-analyze-your-own-files) | Bervariasi | `container_upload` | Menganalisis data, membuat visualisasi  |

### Bekerja dengan format file lainnya \{#working-with-other-file-formats}

Untuk tipe file yang tidak didukung sebagai blok `document` (.csv, .txt, .md, .docx, .xlsx), konversikan file tersebut ke teks biasa, dan sertakan kontennya langsung dalam pesan Anda:

<CodeGroup>
```bash cURL hidelines={3..4}
# Contoh: Membaca file teks dan mengirimnya sebagai teks biasa
# Catatan: Untuk file dengan karakter khusus, pertimbangkan encoding base64
TEXT_CONTENT="This is a sample document. It has multiple lines."

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

```bash CLI hidelines={1}
printf 'This is a test document for upload.\n' > document.txt
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

```python Python nocheck hidelines={2..5}
import pandas as pd
import anthropic

client = anthropic.Anthropic()

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

```typescript TypeScript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
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

```csharp C# nocheck
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

```go Go hidelines={11..15}
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func init() {
	os.WriteFile("document.txt", []byte("This is a test document for upload."), 0644)
}

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

```java Java nocheck hidelines={1..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

public class FileUploadExample {
    public static void main(String[] args) throws IOException {
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
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

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

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

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

#### Blok document \{#document-blocks}

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

#### Blok image \{#image-blocks}

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

### Mengelola file \{#managing-files}

#### Menampilkan daftar file \{#list-files}

Ambil daftar file yang telah Anda unggah:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```bash CLI nocheck
ant beta:files list
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
files = client.beta.files.list()
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();
const files = await anthropic.beta.files.list();
```

```csharp C# nocheck
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

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	files, err := client.Beta.Files.List(context.TODO(), anthropic.BetaFileListParams{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(files)
}
```

```java Java hidelines={1..2,4..6,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.files.FileListPage;

public class ListFiles {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        FileListPage files = client.beta().files().list();
        System.out.println(files);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$files = $client->beta->files->list();
print_r($files);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

files = client.beta.files.list
puts files
```
</CodeGroup>

#### Mendapatkan metadata file \{#get-file-metadata}

Ambil informasi tentang file tertentu:

<CodeGroup>

````bash
curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
````

````bash
ant beta:files retrieve-metadata \
  --file-id "$FILE_ID"
````

````python
file = client.beta.files.retrieve_metadata(file_id)
````

````typescript
const file = await client.beta.files.retrieveMetadata(uploaded.id);
````

````csharp
var file = await client.Beta.Files.RetrieveMetadata(fileId);
Console.WriteLine(file);
````

````go
metadata, err := client.Beta.Files.GetMetadata(
	context.TODO(),
	fileID,
	anthropic.BetaFileGetMetadataParams{},
)
if err != nil {
	log.Fatal(err)
}

fmt.Println(metadata)
````

````java
FileMetadata metadata = client.beta().files().retrieveMetadata(fileId);

System.out.println(metadata);
````

````php
$file = $client->beta->files->retrieveMetadata($fileId);
echo $file;
````

````ruby
file = client.beta.files.retrieve_metadata(file_id)
puts file
````

</CodeGroup>

#### Menghapus file \{#delete-a-file}

Hapus file dari workspace Anda:

<CodeGroup>

````bash
curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
````

````bash
ant beta:files delete \
  --file-id "$FILE_ID"
````

````python
result = client.beta.files.delete(file_id)
````

````typescript
await client.beta.files.delete(uploaded.id);
````

````csharp
await client.Beta.Files.Delete(fileId);
````

````go
_, err = client.Beta.Files.Delete(
	context.TODO(),
	fileID,
	anthropic.BetaFileDeleteParams{},
)
if err != nil {
	log.Fatal(err)
}
````

````java
client.beta().files().delete(fileId);
````

````php
$result = $client->beta->files->delete($fileId);
````

````ruby
result = client.beta.files.delete(file_id)
````

</CodeGroup>

### Mengunduh file \{#downloading-a-file}

Unduh file yang telah dibuat oleh skill atau code execution tool:

<CodeGroup>

````bash
curl -X GET "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output downloaded_file.txt
````

````bash
ant beta:files download \
  --file-id "$FILE_ID" \
  --output downloaded_file.txt
````

````python
file_content = client.beta.files.download(file_id)

# Save to file
file_content.write_to_file("downloaded_file.txt")
````

````typescript
const content = await client.beta.files.download(uploaded.id);

const bytes = Buffer.from(await content.arrayBuffer());
await fsp.writeFile("downloaded_file.txt", bytes);
````

````csharp
using var fileContent = await client.Beta.Files.Download(fileId);
await using var source = await fileContent.ReadAsStream();
await using var destination = File.Create("downloaded_file.txt");
await source.CopyToAsync(destination);
````

````go
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

````

````java
try (HttpResponse response = client.beta().files().download(fileId)) {
    try (InputStream body = response.body()) {
        Files.copy(body, Path.of("downloaded_file.txt"),
            StandardCopyOption.REPLACE_EXISTING);
    }
}
````

````php
$fileContent = $client->beta->files->download($fileId);

file_put_contents("downloaded_file.txt", $fileContent);
````

````ruby
file_content = client.beta.files.download(file_id)

File.binwrite("downloaded_file.txt", file_content.read)
````

</CodeGroup>

<Note>
Anda hanya dapat mengunduh file yang dibuat oleh [skill](/docs/id/build-with-claude/skills-guide) atau [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool). File yang Anda unggah tidak dapat diunduh.
</Note>

---

## Penyimpanan dan batasan file \{#file-storage-and-limits}

### Batasan penyimpanan \{#storage-limits}

- **Ukuran file maksimum:** 500 MB per file
- **Total penyimpanan:** 500 GB per organisasi

### Siklus hidup file \{#file-lifecycle}

- File dibatasi pada workspace dari kunci API. Kunci API lain dapat menggunakan file yang dibuat oleh kunci API lain mana pun yang terkait dengan workspace yang sama
- File tetap ada hingga Anda menghapusnya
- File yang dihapus tidak dapat dipulihkan
- File tidak dapat diakses melalui API segera setelah penghapusan, tetapi mungkin masih ada dalam panggilan API `Messages` yang aktif dan penggunaan alat terkait
- File yang dihapus pengguna akan dihapus sesuai dengan [kebijakan retensi data](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) Anthropic.

---

## Retensi data \{#data-retention}

File yang diunggah melalui Files API disimpan hingga dihapus secara eksplisit menggunakan endpoint `DELETE /v1/files/{file_id}`. File disimpan untuk digunakan kembali di berbagai permintaan API.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Penanganan error \{#error-handling}

Error umum saat menggunakan Files API meliputi:

- **File not found (404):** `file_id` yang ditentukan tidak ada atau Anda tidak memiliki akses ke file tersebut
- **Invalid file type (400):** Tipe file tidak cocok dengan tipe blok konten (misalnya, menggunakan file gambar dalam blok document)
- **Exceeds context window size (400):** File lebih besar dari ukuran jendela konteks (misalnya menggunakan file teks biasa 500 MB dalam permintaan `/v1/messages`)
- **Invalid filename (400):** Nama file tidak memenuhi persyaratan panjang (1-255 karakter) atau berisi karakter terlarang (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, atau karakter unicode 0-31)
- **File too large (413):** File melebihi batas 500 MB
- **Storage limit exceeded (403):** Organisasi Anda telah mencapai batas penyimpanan 500 GB

```json Output
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "File not found: file_011CNha8iCJcU1wXNR6q4V8w"
  }
}
```

## Penggunaan dan penagihan \{#usage-and-billing}

Operasi File API bersifat **gratis**:
- Mengunggah file
- Mengunduh file
- Menampilkan daftar file
- Mendapatkan metadata file
- Menghapus file

Konten file yang digunakan dalam permintaan `Messages` dihitung sebagai token input. Anda hanya dapat mengunduh file yang dibuat oleh [skill](/docs/id/build-with-claude/skills-guide) atau [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool).

### Batas laju \{#rate-limits}

Selama periode beta:
- Panggilan API terkait file dibatasi sekitar 100 permintaan per menit
- [Hubungi kami](mailto:sales@anthropic.com) jika Anda memerlukan batas yang lebih tinggi untuk kasus penggunaan Anda