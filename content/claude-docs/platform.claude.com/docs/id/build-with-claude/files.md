---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/files
fetched_at: 2026-04-24T03:12:20.532875Z
sha256: b654fa35912f731b87ca57a93528d520cbd293234181b28ece0cbb7979d890af
---

# Files API

Unggah dan kelola file untuk digunakan dengan Claude API tanpa perlu mengunggah ulang konten dengan setiap permintaan.

---

Files API memungkinkan Anda mengunggah dan mengelola file untuk digunakan dengan Claude API tanpa perlu mengunggah ulang konten dengan setiap permintaan. Ini sangat berguna saat menggunakan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk menyediakan input (misalnya dataset dan dokumen) dan kemudian mengunduh output (misalnya bagan). Anda juga dapat menggunakan Files API untuk menghindari harus terus mengunggah ulang dokumen dan gambar yang sering digunakan di seluruh panggilan API. Anda dapat [menjelajahi referensi API secara langsung](/docs/id/api/files-create), selain panduan ini.

<Note>
Files API sedang dalam beta. Hubungi kami melalui [formulir umpan balik](https://forms.gle/tisHyierGwgN4DUE9) untuk berbagi pengalaman Anda dengan Files API.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Model yang didukung

Mereferensikan `file_id` dalam permintaan Messages didukung di semua model yang mendukung jenis file yang diberikan. Misalnya, [gambar](/docs/id/build-with-claude/vision) didukung di semua model Claude 3+, [PDF](/docs/id/build-with-claude/pdf-support) di semua model Claude 3.5+, dan [berbagai jenis file lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#supported-file-types) untuk alat eksekusi kode di Claude Haiku 4.5 plus semua model Claude 3.7+.

Files API saat ini tidak didukung di Amazon Bedrock atau Google Vertex AI.

## Cara kerja Files API

Files API menyediakan pendekatan buat-sekali-gunakan-berkali-kali yang sederhana untuk bekerja dengan file:

- **Unggah file** ke penyimpanan aman Anthropic dan terima `file_id` unik
- **Unduh file** yang dibuat dari skill atau alat eksekusi kode
- **Referensikan file** dalam permintaan [Messages](/docs/id/api/messages/create) menggunakan `file_id` alih-alih mengunggah ulang konten
- **Kelola file Anda** dengan operasi daftar, ambil, dan hapus

## Cara menggunakan Files API

<Note>
Untuk menggunakan Files API, Anda perlu menyertakan header fitur beta: `anthropic-beta: files-api-2025-04-14`.
</Note>

### Mengunggah file

Unggah file untuk direferensikan dalam panggilan API di masa depan:

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
  --transform id --format yaml)
````

````python
uploaded = client.beta.files.upload(
    file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
)
````

````typescript
const uploaded = await anthropic.beta.files.upload({
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
        File = File.OpenRead("/path/to/document.pdf")
    });

Console.WriteLine(uploaded.Id);
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

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("ANTHROPIC_API_KEY")
);

$file = $client->beta->files->upload(
    file: fopen('/path/to/document.pdf', 'r'),
    betas: ['files-api-2025-04-14'],
);

echo $file->id;
```

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

Respons dari mengunggah file akan mencakup:

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

### Menggunakan file dalam pesan

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
  "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
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
        Model = "claude-opus-4-6",
        MaxTokens = 1024,
        Betas = new[] { "files-api-2025-04-14" },
        Messages = new[]
        {
            new BetaMessageParam
            {
                Role = "user",
                Content = new object[]
                {
                    new { type = "text", text = "Please summarize this document for me." },
                    new
                    {
                        type = "document",
                        source = new
                        {
                            type = "file",
                            file_id = fileId
                        }
                    }
                }
            }
        }
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
    .model(Model.CLAUDE_OPUS_4_6)
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
    model: 'claude-opus-4-6',
    betas: ['files-api-2025-04-14'],
);

print_r($response);
````

````ruby
response = client.beta.messages.create(
  model: "claude-opus-4-6",
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

### Jenis file dan blok konten

Files API mendukung berbagai jenis file yang sesuai dengan jenis blok konten yang berbeda:

| Jenis File | Tipe MIME | Jenis Blok Konten | Kasus Penggunaan |
| :--- | :--- | :--- | :--- |
| PDF | `application/pdf` | `document` | Analisis teks, pemrosesan dokumen |
| Teks biasa | `text/plain` | `document` | Analisis teks, pemrosesan |
| Gambar | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image` | Analisis gambar, tugas visual |
| [Dataset, lainnya](/docs/id/agents-and-tools/tool-use/code-execution-tool#supported-file-types) | Bervariasi | `container_upload` | Analisis data, buat visualisasi  |

### Bekerja dengan format file lainnya

Untuk jenis file yang tidak didukung sebagai blok `document` (.csv, .txt, .md, .docx, .xlsx), konversi file ke teks biasa, dan sertakan konten langsung dalam pesan Anda:

<CodeGroup>
```bash Shell hidelines={3..4}
# Contoh: Membaca file teks dan mengirimnya sebagai teks biasa
# Catatan: Untuk file dengan karakter khusus, pertimbangkan pengkodean base64
TEXT_CONTENT="This is a sample document. It has multiple lines."

curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @- <<EOF
{
  "model": "claude-opus-4-7",
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
# Referensi "@./path" menyisipkan konten file langsung ke dalam bidang.
ant messages create \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --transform 'content.0.text' --format yaml <<'YAML'
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
    model="claude-opus-4-7",
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
    model: "claude-opus-4-7",
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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model(Model.CLAUDE_OPUS_4_7)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
    model: 'claude-opus-4-7',
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Contoh: Membaca file teks
text_content = File.read("document.txt")

message = client.messages.create(
  model: "claude-opus-4-7",
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
Untuk file .docx yang berisi gambar, konversi ke format PDF terlebih dahulu, kemudian gunakan [dukungan PDF](/docs/id/build-with-claude/pdf-support) untuk memanfaatkan penguraian gambar bawaan. Ini memungkinkan penggunaan kutipan dari dokumen PDF.
</Note>

#### Blok dokumen

Untuk PDF dan file teks, gunakan blok konten `document`:

```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
  },
  "title": "Document Title", // Opsional
  "context": "Context about the document", // Opsional
  "citations": { "enabled": true } // Opsional, mengaktifkan kutipan
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

### Mengelola file

#### Daftar file

Ambil daftar file yang diunggah:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```bash CLI
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
const files = await anthropic.beta.files.list({
  betas: ["files-api-2025-04-14"]
});
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

        var files = await client.Beta.Files.List(new FileListParams
        {
            Betas = ["files-api-2025-04-14"]
        });
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

	files, err := client.Beta.Files.List(context.TODO(), anthropic.BetaFileListParams{
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
	})
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$files = $client->beta->files->list(
    betas: ['files-api-2025-04-14'],
);
print_r($files);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

files = client.beta.files.list(
  betas: ["files-api-2025-04-14"]
)
puts files
```
</CodeGroup>

#### Dapatkan metadata file

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
const file = await anthropic.beta.files.retrieveMetadata(uploaded.id);
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
$file = $client->beta->files->retrieveMetadata(
    fileID: $fileId,
);
echo $file;
````

````ruby
file = client.beta.files.retrieve_metadata(file_id)
puts file
````

</CodeGroup>

#### Hapus file

Hapus file dari ruang kerja Anda:

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
await anthropic.beta.files.delete(uploaded.id);
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
$result = $client->beta->files->delete(
    fileID: $fileId,
);
````

````ruby
result = client.beta.files.delete(file_id)
````

</CodeGroup>

### Mengunduh file

Unduh file yang telah dibuat oleh skill atau alat eksekusi kode:

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
const content = await anthropic.beta.files.download(uploaded.id);

const bytes = Buffer.from(await content.arrayBuffer());
await fsp.writeFile("downloaded_file.txt", bytes);
````

````csharp
byte[] fileContent = await client.Beta.Files.Download(fileId);

await File.WriteAllBytesAsync("downloaded_file.txt", fileContent);
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

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$fileContent = $client->beta->files->download(
    fileID: 'file_011CNha8iCJcU1wXNR6q4V8w',
    betas: ['files-api-2025-04-14'],
);

file_put_contents("downloaded_file.txt", $fileContent);
```

````ruby
file_content = client.beta.files.download(file_id)

File.binwrite("downloaded_file.txt", file_content.read)
````

</CodeGroup>

<Note>
Anda hanya dapat mengunduh file yang dibuat oleh [skill](/docs/id/build-with-claude/skills-guide) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool). File yang Anda unggah tidak dapat diunduh.
</Note>

---

## Penyimpanan file dan batas

### Batas penyimpanan

- **Ukuran file maksimal:** 500 MB per file
- **Total penyimpanan:** 500 GB per organisasi

### Siklus hidup file

- File dibatasi pada ruang kerja kunci API. Kunci API lain dapat menggunakan file yang dibuat oleh kunci API lain apa pun yang terkait dengan ruang kerja yang sama
- File bertahan sampai Anda menghapusnya
- File yang dihapus tidak dapat dipulihkan
- File tidak dapat diakses melalui API segera setelah penghapusan, tetapi mungkin tetap ada dalam panggilan API `Messages` aktif dan penggunaan alat terkait
- File yang dihapus pengguna akan dihapus sesuai dengan [kebijakan retensi data](/docs/id/build-with-claude/api-and-data-retention) Anthropic.

---

## Retensi data

File yang diunggah melalui Files API disimpan sampai dihapus secara eksplisit menggunakan endpoint `DELETE /v1/files/{file_id}`. File disimpan untuk digunakan kembali di seluruh permintaan API.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Penanganan kesalahan

Kesalahan umum saat menggunakan Files API meliputi:

- **File tidak ditemukan (404):** `file_id` yang ditentukan tidak ada atau Anda tidak memiliki akses ke file tersebut
- **Jenis file tidak valid (400):** Jenis file tidak cocok dengan jenis blok konten (misalnya, menggunakan file gambar dalam blok dokumen)
- **Melebihi ukuran jendela konteks (400):** File lebih besar dari ukuran jendela konteks (misalnya menggunakan file plaintext 500 MB dalam permintaan `/v1/messages`)
- **Nama file tidak valid (400):** Nama file tidak memenuhi persyaratan panjang (1-255 karakter) atau berisi karakter terlarang (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, atau karakter unicode 0-31)
- **File terlalu besar (413):** File melebihi batas 500 MB
- **Batas penyimpanan terlampaui (403):** Organisasi Anda telah mencapai batas penyimpanan 500 GB

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

Operasi File API **gratis**:
- Mengunggah file
- Mengunduh file
- Mendaftar file
- Mendapatkan metadata file
- Menghapus file

Konten file yang digunakan dalam permintaan `Messages` ditagih sebagai token input. Anda hanya dapat mengunduh file yang dibuat oleh [skill](/docs/id/build-with-claude/skills-guide) atau [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).

### Batas laju

Selama periode beta:
- Panggilan API terkait file dibatasi hingga sekitar 100 permintaan per menit
- [Hubungi kami](mailto:sales@anthropic.com) jika Anda memerlukan batas yang lebih tinggi untuk kasus penggunaan Anda