---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: 15be11a87bca46de88af0121db303d27c6450b137c8cb6dc16ad2841fb1c65f9
---

# Alat eksekusi kode

---

Claude dapat menganalisis data, membuat visualisasi, melakukan perhitungan kompleks, menjalankan perintah sistem, membuat dan mengedit file, serta memproses file yang diunggah langsung dalam percakapan API. Alat eksekusi kode memungkinkan Claude menjalankan perintah Bash dan memanipulasi file, termasuk menulis kode, dalam lingkungan sandbox yang aman.

**Eksekusi kode gratis saat digunakan dengan web search atau web fetch.** Ketika `web_search_20260209` atau `web_fetch_20260209` disertakan dalam permintaan Anda, tidak ada biaya tambahan untuk panggilan alat eksekusi kode di luar biaya token input dan output standar. Biaya eksekusi kode standar berlaku ketika alat-alat ini tidak disertakan.

Eksekusi kode adalah primitif inti untuk membangun agen berkinerja tinggi. Ini memungkinkan pemfilteran dinamis dalam alat web search dan web fetch, memungkinkan Claude memproses hasil sebelum mencapai jendela konteks—meningkatkan akurasi sekaligus mengurangi konsumsi token.

<Note>
Silakan hubungi kami melalui [formulir umpan balik](https://forms.gle/LTAU6Xn2puCJMi1n6) untuk berbagi masukan Anda tentang fitur ini.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Kompatibilitas model

Alat eksekusi kode tersedia pada model-model berikut:

| Model | Versi Alat |
|-------|--------------|
| Claude Opus 4.6 (`claude-opus-4-6`) | `code_execution_20250825` |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`) | `code_execution_20250825` |
| Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) | `code_execution_20250825` |
| Claude Opus 4.5 (`claude-opus-4-5-20251101`) | `code_execution_20250825` |
| Claude Opus 4.1 (`claude-opus-4-1-20250805`) | `code_execution_20250825` |
| Claude Opus 4 (`claude-opus-4-20250514`) | `code_execution_20250825` |
| Claude Sonnet 4 (`claude-sonnet-4-20250514`) | `code_execution_20250825` |
| Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) ([tidak didukung lagi](/docs/id/about-claude/model-deprecations)) | `code_execution_20250825` |
| Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | `code_execution_20250825` |
| Claude Haiku 3.5 (`claude-3-5-haiku-latest`) ([tidak didukung lagi](/docs/id/about-claude/model-deprecations)) | `code_execution_20250825` |

<Note>
Versi saat ini `code_execution_20250825` mendukung perintah Bash dan operasi file. Versi lama `code_execution_20250522` (hanya Python) juga tersedia. Lihat [Upgrade ke versi alat terbaru](#upgrade-to-latest-tool-version) untuk detail migrasi.
</Note>

<Warning>
Versi alat yang lebih lama tidak dijamin kompatibel ke belakang dengan model yang lebih baru. Selalu gunakan versi alat yang sesuai dengan versi model Anda.
</Warning>

## Ketersediaan platform

Eksekusi kode tersedia di:
- **Claude API** (Anthropic)
- **Microsoft Azure AI Foundry**

Eksekusi kode saat ini tidak tersedia di Amazon Bedrock atau Google Vertex AI.

## Mulai cepat

Berikut adalah contoh sederhana yang meminta Claude melakukan perhitungan:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
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

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
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
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const response = await anthropic.messages.create({
    model: "claude-opus-4-6",
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
}

main().catch(console.error);
```
</CodeGroup>

## Cara kerja eksekusi kode

Ketika Anda menambahkan alat eksekusi kode ke permintaan API Anda:

1. Claude mengevaluasi apakah eksekusi kode akan membantu menjawab pertanyaan Anda
2. Alat ini secara otomatis memberikan kemampuan berikut kepada Claude:
   - **Perintah Bash**: Menjalankan perintah shell untuk operasi sistem dan manajemen paket
   - **Operasi file**: Membuat, melihat, dan mengedit file secara langsung, termasuk menulis kode
3. Claude dapat menggunakan kombinasi kemampuan ini dalam satu permintaan
4. Semua operasi berjalan dalam lingkungan sandbox yang aman
5. Claude memberikan hasil dengan grafik, perhitungan, atau analisis yang dihasilkan

## Menggunakan eksekusi kode dengan alat eksekusi lainnya

Ketika Anda menyediakan eksekusi kode bersama alat yang disediakan klien yang juga menjalankan kode (seperti [alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) atau REPL kustom), Claude beroperasi dalam lingkungan multi-komputer. Alat eksekusi kode berjalan di container sandbox Anthropic, sementara alat yang disediakan klien berjalan di lingkungan terpisah yang Anda kendalikan. Claude terkadang dapat membingungkan lingkungan-lingkungan ini, mencoba menggunakan alat yang salah atau mengasumsikan status dibagikan di antara keduanya.

Untuk menghindari hal ini, tambahkan instruksi ke system prompt Anda yang mengklarifikasi perbedaannya:

```text
When multiple code execution environments are available, be aware that:
- Variables, files, and state do NOT persist between different execution environments
- Use the code_execution tool for general-purpose computation in Anthropic's sandboxed environment
- Use client-provided execution tools (e.g., bash) when you need access to the user's local system, files, or data
- If you need to pass results between environments, explicitly include outputs in subsequent tool calls rather than assuming shared state
```

Ini sangat penting saat menggabungkan eksekusi kode dengan [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), yang mengaktifkan eksekusi kode secara otomatis. Jika aplikasi Anda sudah menyediakan alat shell sisi klien, eksekusi kode otomatis menciptakan lingkungan eksekusi kedua yang perlu dibedakan oleh Claude.

## Cara menggunakan alat

### Menjalankan perintah Bash

Minta Claude untuk memeriksa informasi sistem dan menginstal paket:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": "Check the Python version and list installed packages"
        }],
        "tools": [{
            "type": "code_execution_20250825",
            "name": "code_execution"
        }]
    }'
```

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Check the Python version and list installed packages",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "Check the Python version and list installed packages"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```
</CodeGroup>

### Membuat dan mengedit file secara langsung

Claude dapat membuat, melihat, dan mengedit file secara langsung di sandbox menggunakan kemampuan manipulasi file:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": "Create a config.yaml file with database settings, then update the port from 5432 to 3306"
        }],
        "tools": [{
            "type": "code_execution_20250825",
            "name": "code_execution"
        }]
    }'
```

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a config.yaml file with database settings, then update the port from 5432 to 3306",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content:
        "Create a config.yaml file with database settings, then update the port from 5432 to 3306"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```
</CodeGroup>

### Mengunggah dan menganalisis file Anda sendiri

Untuk menganalisis file data Anda sendiri (CSV, Excel, gambar, dll.), unggah melalui Files API dan referensikan dalam permintaan Anda:

<Note>
Menggunakan Files API dengan Code Execution memerlukan header beta Files API: `"anthropic-beta": "files-api-2025-04-14"`
</Note>

Lingkungan Python dapat memproses berbagai jenis file yang diunggah melalui Files API, termasuk:

- CSV
- Excel (.xlsx, .xls)
- JSON
- XML
- Gambar (JPEG, PNG, GIF, WebP)
- File teks (.txt, .md, .py, dll)

#### Mengunggah dan menganalisis file

1. **Unggah file Anda** menggunakan [Files API](/docs/id/build-with-claude/files)
2. **Referensikan file** dalam pesan Anda menggunakan blok konten `container_upload`
3. **Sertakan alat eksekusi kode** dalam permintaan API Anda

<CodeGroup>
```bash Shell
# First, upload a file
curl https://api.anthropic.com/v1/files \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: files-api-2025-04-14" \
    --form 'file=@"data.csv"' \

# Then use the file_id with code execution
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: files-api-2025-04-14" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
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

```python Python
import anthropic

client = anthropic.Anthropic()

# Upload a file
file_object = client.beta.files.upload(
    file=open("data.csv", "rb"),
)

# Use the file_id with code execution
response = client.beta.messages.create(
    model="claude-opus-4-6",
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
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";
import { createReadStream } from "fs";

const anthropic = new Anthropic();

async function main() {
  // Upload a file
  const fileObject = await anthropic.beta.files.create({
    file: createReadStream("data.csv")
  });

  // Use the file_id with code execution
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
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
}

main().catch(console.error);
```
</CodeGroup>

#### Mengambil file yang dihasilkan

Ketika Claude membuat file selama eksekusi kode, Anda dapat mengambil file-file ini menggunakan Files API:

<CodeGroup>
```python Python
from anthropic import Anthropic

# Initialize the client
client = Anthropic()

# Request code execution that creates files
response = client.beta.messages.create(
    model="claude-opus-4-6",
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


# Extract file IDs from the response
def extract_file_ids(response):
    file_ids = []
    for item in response.content:
        if item.type == "bash_code_execution_tool_result":
            content_item = item.content
            if content_item.type == "bash_code_execution_result":
                for file in content_item.content:
                    if hasattr(file, "file_id"):
                        file_ids.append(file.file_id)
    return file_ids


# Download the created files
for file_id in extract_file_ids(response):
    file_metadata = client.beta.files.retrieve_metadata(file_id)
    file_content = client.beta.files.download(file_id)
    file_content.write_to_file(file_metadata.filename)
    print(f"Downloaded: {file_metadata.filename}")
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";
import { writeFile } from "fs/promises";

// Initialize the client
const anthropic = new Anthropic();

async function main() {
  // Request code execution that creates files
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
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

  // Extract file IDs from the response
  function extractFileIds(response: any): string[] {
    const fileIds: string[] = [];
    for (const item of response.content) {
      if (item.type === "bash_code_execution_tool_result") {
        const contentItem = item.content;
        if (contentItem.type === "bash_code_execution_result" && contentItem.content) {
          for (const file of contentItem.content) {
            fileIds.push(file.file_id);
          }
        }
      }
    }
    return fileIds;
  }

  // Download the created files
  const fileIds = extractFileIds(response);
  for (const fileId of fileIds) {
    const fileMetadata = await anthropic.beta.files.retrieveMetadata(fileId);
    const fileContent = await anthropic.beta.files.download(fileId);

    // Convert ReadableStream to Buffer and save
    const chunks: Uint8Array[] = [];
    for await (const chunk of fileContent) {
      chunks.push(chunk);
    }
    const buffer = Buffer.concat(chunks);
    await writeFile(fileMetadata.filename, buffer);
    console.log(`Downloaded: ${fileMetadata.filename}`);
  }
}

main().catch(console.error);
```
</CodeGroup>

### Menggabungkan operasi

Alur kerja kompleks menggunakan semua kemampuan:

<CodeGroup>
```bash Shell
# First, upload a file
curl https://api.anthropic.com/v1/files \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: files-api-2025-04-14" \
    --form 'file=@"data.csv"' \
    > file_response.json

# Extract file_id (using jq)
FILE_ID=$(jq -r '.id' file_response.json)

# Then use it with code execution
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: files-api-2025-04-14" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this CSV data: create a summary report, save visualizations, and create a README with the findings"
                },
                {
                    "type": "container_upload",
                    "file_id": "'$FILE_ID'"
                }
            ]
        }],
        "tools": [{
            "type": "code_execution_20250825",
            "name": "code_execution"
        }]
    }'
```

```python Python
# Upload a file
file_object = client.beta.files.upload(
    file=open("data.csv", "rb"),
)

# Use it with code execution
response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["files-api-2025-04-14"],
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this CSV data: create a summary report, save visualizations, and create a README with the findings",
                },
                {"type": "container_upload", "file_id": file_object.id},
            ],
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Claude might:
# 1. Use bash to check file size and preview data
# 2. Use text_editor to write Python code to analyze the CSV and create visualizations
# 3. Use bash to run the Python code
# 4. Use text_editor to create a README.md with findings
# 5. Use bash to organize files into a report directory
```

```typescript TypeScript
// Upload a file
const fileObject = await anthropic.beta.files.create({
  file: createReadStream("data.csv")
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  betas: ["files-api-2025-04-14"],
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Analyze this CSV data: create a summary report, save visualizations, and create a README with the findings"
        },
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

// Claude might:
// 1. Use bash to check file size and preview data
// 2. Use text_editor to write Python code to analyze the CSV and create visualizations
// 3. Use bash to run the Python code
// 4. Use text_editor to create a README.md with findings
// 5. Use bash to organize files into a report directory
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
- `bash_code_execution`: Menjalankan perintah shell
- `text_editor_code_execution`: Melihat, membuat, dan mengedit file, termasuk menulis kode

## Format respons

Alat eksekusi kode dapat mengembalikan dua jenis hasil tergantung pada operasinya:

### Respons perintah Bash

```json hidelines={1,-1}
[
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
]
```

### Respons operasi file

**Melihat file:**
```json hidelines={1,-1}
[
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
]
```

**Membuat file:**
```json hidelines={1,-1}
[
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
]
```

**Mengedit file (str_replace):**
```json hidelines={1,-1}
[
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
]
```

### Hasil

Semua hasil eksekusi mencakup:
- `stdout`: Output dari eksekusi yang berhasil
- `stderr`: Pesan kesalahan jika eksekusi gagal
- `return_code`: 0 untuk sukses, bukan nol untuk kegagalan

Bidang tambahan untuk operasi file:
- **View**: `file_type`, `content`, `numLines`, `startLine`, `totalLines`
- **Create**: `is_file_update` (apakah file sudah ada)
- **Edit**: `oldStart`, `oldLines`, `newStart`, `newLines`, `lines` (format diff)

### Kesalahan

Setiap jenis alat dapat mengembalikan kesalahan tertentu:

**Kesalahan umum (semua alat):**
```json
{
  "type": "bash_code_execution_tool_result",
  "tool_use_id": "srvtoolu_01VfmxgZ46TiHbmXgy928hQR",
  "content": {
    "type": "bash_code_execution_tool_result_error",
    "error_code": "unavailable"
  }
}
```

**Kode kesalahan berdasarkan jenis alat:**

| Alat | Kode Kesalahan | Deskripsi |
|------|-----------|-------------|
| Semua alat | `unavailable` | Alat sementara tidak tersedia |
| Semua alat | `execution_time_exceeded` | Eksekusi melebihi batas waktu maksimum |
| Semua alat | `container_expired` | Container kedaluwarsa dan tidak lagi tersedia |
| Semua alat | `invalid_tool_input` | Parameter tidak valid yang diberikan ke alat |
| Semua alat | `too_many_requests` | Batas laju terlampaui untuk penggunaan alat |
| text_editor | `file_not_found` | File tidak ada (untuk operasi view/edit) |
| text_editor | `string_not_found` | `old_str` tidak ditemukan dalam file (untuk str_replace) |

#### Alasan berhenti `pause_turn`

Respons mungkin menyertakan alasan berhenti `pause_turn`, yang menunjukkan bahwa API menjeda giliran yang berjalan lama. Anda dapat memberikan respons kembali apa adanya dalam permintaan berikutnya untuk membiarkan Claude melanjutkan gilirannya, atau memodifikasi konten jika Anda ingin menginterupsi percakapan.

## Container

Alat eksekusi kode berjalan dalam lingkungan yang aman dan terkontainerisasi yang dirancang khusus untuk eksekusi kode, dengan fokus lebih tinggi pada Python.

### Lingkungan runtime
- **Versi Python**: 3.11.12
- **Sistem operasi**: Container berbasis Linux
- **Arsitektur**: x86_64 (AMD64)

### Batas sumber daya
- **Memori**: 5GiB RAM
- **Ruang disk**: 5GiB penyimpanan workspace
- **CPU**: 1 CPU

### Jaringan dan keamanan
- **Akses internet**: Sepenuhnya dinonaktifkan untuk keamanan
- **Koneksi eksternal**: Tidak ada permintaan jaringan keluar yang diizinkan
- **Isolasi sandbox**: Isolasi penuh dari sistem host dan container lainnya
- **Akses file**: Terbatas hanya pada direktori workspace
- **Cakupan workspace**: Seperti [Files](/docs/id/build-with-claude/files), container dicakupkan ke workspace kunci API
- **Kedaluwarsa**: Container kedaluwarsa 30 hari setelah pembuatan

### Pustaka yang sudah terinstal
Lingkungan Python sandbox mencakup pustaka yang umum digunakan ini:
- **Ilmu Data**: pandas, numpy, scipy, scikit-learn, statsmodels
- **Visualisasi**: matplotlib, seaborn
- **Pemrosesan File**: pyarrow, openpyxl, xlsxwriter, xlrd, pillow, python-pptx, python-docx, pypdf, pdfplumber, pypdfium2, pdf2image, pdfkit, tabula-py, reportlab[pycairo], Img2pdf
- **Matematika & Komputasi**: sympy, mpmath
- **Utilitas**: tqdm, python-dateutil, pytz, joblib, unzip, unrar, 7zip, bc, rg (ripgrep), fd, sqlite

## Penggunaan ulang container

Anda dapat menggunakan kembali container yang ada di beberapa permintaan API dengan menyediakan ID container dari respons sebelumnya. Ini memungkinkan Anda mempertahankan file yang dibuat di antara permintaan.

### Contoh

<CodeGroup>
```python Python
import os
from anthropic import Anthropic

# Initialize the client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# First request: Create a file with a random number
response1 = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Write a file with a random number and save it to '/tmp/number.txt'",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

# Extract the container ID from the first response
container_id = response1.container.id

# Second request: Reuse the container to read the file
response2 = client.messages.create(
    container=container_id,  # Reuse the same container
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Read the number from '/tmp/number.txt' and calculate its square",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  // First request: Create a file with a random number
  const response1 = await anthropic.messages.create({
    model: "claude-opus-4-6",
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

  // Extract the container ID from the first response
  const containerId = response1.container.id;

  // Second request: Reuse the container to read the file
  const response2 = await anthropic.messages.create({
    container: containerId, // Reuse the same container
    model: "claude-opus-4-6",
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
}

main().catch(console.error);
```

```bash Shell
# First request: Create a file with a random number
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
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

# Extract container ID from the response (using jq)
CONTAINER_ID=$(jq -r '.container.id' response1.json)

# Second request: Reuse the container to read the file
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "container": "'$CONTAINER_ID'",
        "model": "claude-opus-4-6",
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
</CodeGroup>

## Streaming

Dengan streaming diaktifkan, Anda akan menerima peristiwa eksekusi kode saat terjadi:

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

Anda dapat menyertakan alat eksekusi kode dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat eksekusi kode melalui Messages Batches API dihargai sama dengan yang ada dalam permintaan Messages API biasa.

## Penggunaan dan harga

**Code execution is free when used with web search or web fetch.** When `web_search_20260209` or `web_fetch_20260209` is included in your API request, there are no additional charges for code execution tool calls beyond the standard input and output token costs.

When used without these tools, code execution is billed by execution time, tracked separately from token usage:

- Execution time has a minimum of 5 minutes
- Each organization receives **1,550 free hours** of usage per month
- Additional usage beyond 1,550 hours is billed at **$0.05 per hour, per container**
- If files are included in the request, execution time is billed even if the tool is not invoked, due to files being preloaded onto the container

Code execution usage is tracked in the response:

```json
"usage": {
  "input_tokens": 105,
  "output_tokens": 239,
  "server_tool_use": {
    "code_execution_requests": 1
  }
}
```

## Upgrade ke versi alat terbaru

Dengan melakukan upgrade ke `code-execution-2025-08-25`, Anda mendapatkan akses ke manipulasi file dan kemampuan Bash, termasuk kode dalam berbagai bahasa. Tidak ada perbedaan harga.

### Yang berubah

| Komponen | Lama | Saat ini |
|-----------|------------------|----------------------------|
| Header beta | `code-execution-2025-05-22` | `code-execution-2025-08-25` |
| Jenis alat | `code_execution_20250522` | `code_execution_20250825` |
| Kemampuan | Hanya Python | Perintah Bash, operasi file |
| Jenis respons | `code_execution_result` | `bash_code_execution_result`, `text_editor_code_execution_result` |

### Kompatibilitas ke belakang

- Semua eksekusi kode Python yang ada terus bekerja persis seperti sebelumnya
- Tidak diperlukan perubahan pada alur kerja yang hanya menggunakan Python

### Langkah upgrade

Untuk melakukan upgrade, perbarui jenis alat dalam permintaan API Anda:

```diff
- "type": "code_execution_20250522"
+ "type": "code_execution_20250825"
```

**Tinjau penanganan respons** (jika mengurai respons secara terprogram):
- Blok sebelumnya untuk respons eksekusi Python tidak akan lagi dikirim
- Sebagai gantinya, jenis respons baru untuk Bash dan operasi file akan dikirim (lihat bagian Format Respons)

## Pemanggilan alat terprogram

Alat eksekusi kode mendukung [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), yang memungkinkan Claude menulis kode yang memanggil alat kustom Anda secara terprogram dalam container eksekusi. Ini memungkinkan alur kerja multi-alat yang efisien, pemfilteran data sebelum mencapai konteks Claude, dan logika kondisional yang kompleks.

<CodeGroup>
```python Python
# Enable programmatic calling for your tools
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Get weather for 5 cities and find the warmest"}
    ],
    tools=[
        {"type": "code_execution_20250825", "name": "code_execution"},
        {
            "name": "get_weather",
            "description": "Get weather for a city",
            "input_schema": {...},
            "allowed_callers": [
                "code_execution_20250825"
            ],  # Enable programmatic calling
        },
    ],
)
```
</CodeGroup>

Pelajari lebih lanjut dalam [dokumentasi pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling).

## Retensi data

Eksekusi kode berjalan di dalam container sandbox sisi server. Data container, termasuk artefak eksekusi, file yang diunggah, dan output, disimpan hingga 30 hari. Retensi ini berlaku untuk semua data yang diproses dalam lingkungan container.

Untuk kelayakan ZDR di semua fitur, lihat [API dan Retensi Data](/docs/id/build-with-claude/api-and-data-retention).

## Menggunakan eksekusi kode dengan Agent Skills

Alat eksekusi kode memungkinkan Claude untuk menggunakan [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview). Skills adalah kemampuan modular yang terdiri dari instruksi, skrip, dan sumber daya yang memperluas fungsionalitas Claude.

Pelajari lebih lanjut di [dokumentasi Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [panduan API Agent Skills](/docs/id/build-with-claude/skills-guide).