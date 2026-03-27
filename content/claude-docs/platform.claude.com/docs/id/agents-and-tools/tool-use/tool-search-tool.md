---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: 38b08143e3028ffc6ca6cc4f455b4a3f630beb39d66d423117ad4884303a9b63
---

# Tool search tool

Memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuat alat secara dinamis sesuai kebutuhan.

---

Tool search tool memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuatnya secara dinamis sesuai kebutuhan. Alih-alih memuat semua definisi alat ke dalam jendela konteks di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan hanya memuat alat yang dibutuhkan.

Pendekatan ini memecahkan dua masalah yang berkembang pesat seiring bertambahnya skala pustaka alat:

- **Pembengkakan konteks**: Definisi alat menghabiskan anggaran konteks Anda dengan cepat. Pengaturan multi-server yang umum (GitHub, Slack, Sentry, Grafana, Splunk) dapat mengonsumsi ~55K token dalam definisi sebelum Claude melakukan pekerjaan nyata apa pun. Tool search biasanya mengurangi ini lebih dari 85%, hanya memuat 3–5 alat yang benar-benar dibutuhkan Claude untuk permintaan tertentu.
- **Akurasi pemilihan alat**: Kemampuan Claude untuk memilih alat yang tepat menurun secara signifikan setelah melebihi 30–50 alat yang tersedia. Dengan menampilkan sekumpulan alat yang relevan secara terfokus sesuai kebutuhan, tool search menjaga akurasi pemilihan tetap tinggi bahkan di antara ribuan alat.

<Tip>
Untuk latar belakang tentang tantangan penskalaan yang dipecahkan oleh tool search, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai kebutuhan dari tool search juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Meskipun ini disediakan sebagai alat sisi server, Anda juga dapat mengimplementasikan fungsionalitas tool search sisi klien Anda sendiri. Lihat [Implementasi tool search kustom](#custom-tool-search-implementation) untuk detailnya.

<Note>
Silakan hubungi kami melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA) untuk berbagi umpan balik Anda tentang fitur ini.
</Note>

<Note>
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Warning>
  Di Amazon Bedrock, tool search sisi server hanya tersedia melalui [invoke
  API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html),
  bukan converse API.
</Warning>

Anda juga dapat mengimplementasikan [tool search sisi klien](#custom-tool-search-implementation) dengan mengembalikan blok `tool_reference` dari implementasi pencarian Anda sendiri.

## Cara kerja tool search

Ada dua varian tool search:

- **Regex** (`tool_search_tool_regex_20251119`): Claude membuat pola regex untuk mencari alat
- **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat

Ketika Anda mengaktifkan tool search tool:

1. Anda menyertakan tool search tool (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar alat Anda
2. Anda menyediakan semua definisi alat dengan `defer_loading: true` untuk alat yang tidak boleh dimuat segera
3. Claude awalnya hanya melihat tool search tool dan alat yang tidak ditangguhkan
4. Ketika Claude membutuhkan alat tambahan, ia mencari menggunakan tool search tool
5. API mengembalikan 3-5 blok `tool_reference` yang paling relevan
6. Referensi ini secara otomatis diperluas menjadi definisi alat lengkap
7. Claude memilih dari alat yang ditemukan dan memanggilnya

Ini menjaga jendela konteks Anda tetap efisien sambil mempertahankan akurasi pemilihan alat yang tinggi.

## Mulai cepat

Berikut adalah contoh sederhana dengan alat yang ditangguhkan:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": "What is the weather in San Francisco?"
            }
        ],
        "tools": [
            {
                "type": "tool_search_tool_regex_20251119",
                "name": "tool_search_tool_regex"
            },
            {
                "name": "get_weather",
                "description": "Get the weather at a specific location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                },
                "defer_loading": true
            },
            {
                "name": "search_files",
                "description": "Search through files in the workspace",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "file_types": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["query"]
                },
                "defer_loading": true
            }
        ]
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": "What is the weather in San Francisco?"}],
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {
            "name": "get_weather",
            "description": "Get the weather at a specific location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
            "defer_loading": True,
        },
        {
            "name": "search_files",
            "description": "Search through files in the workspace",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "file_types": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["query"],
            },
            "defer_loading": True,
        },
    ],
)

print(response)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "What is the weather in San Francisco?"
      }
    ],
    tools: [
      {
        type: "tool_search_tool_regex_20251119",
        name: "tool_search_tool_regex"
      },
      {
        name: "get_weather",
        description: "Get the weather at a specific location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string" },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"]
        },
        defer_loading: true
      },
      {
        name: "search_files",
        description: "Search through files in the workspace",
        input_schema: {
          type: "object",
          properties: {
            query: { type: "string" },
            file_types: {
              type: "array",
              items: { type: "string" }
            }
          },
          required: ["query"]
        },
        defer_loading: true
      }
    ]
  });

  console.log(JSON.stringify(response, null, 2));
}

main();
```

</CodeGroup>

## Definisi alat

Tool search tool memiliki dua varian:

```json JSON
{
  "type": "tool_search_tool_regex_20251119",
  "name": "tool_search_tool_regex"
}
```

```json JSON
{
  "type": "tool_search_tool_bm25_20251119",
  "name": "tool_search_tool_bm25"
}
```

<Warning>
**Format kueri varian Regex: Python regex, BUKAN bahasa alami**

Saat menggunakan `tool_search_tool_regex_20251119`, Claude membuat pola regex menggunakan sintaks `re.search()` Python, bukan kueri bahasa alami. Pola umum:

- `"weather"` - mencocokkan nama/deskripsi alat yang mengandung "weather"
- `"get_.*_data"` - mencocokkan alat seperti `get_user_data`, `get_weather_data`
- `"database.*query|query.*database"` - pola OR untuk fleksibilitas
- `"(?i)slack"` - pencarian tidak peka huruf besar/kecil

Panjang kueri maksimum: 200 karakter

</Warning>

<Note>
**Format kueri varian BM25: Bahasa alami**

Saat menggunakan `tool_search_tool_bm25_20251119`, Claude menggunakan kueri bahasa alami untuk mencari alat.

</Note>

### Pemuatan alat yang ditangguhkan

Tandai alat untuk pemuatan sesuai kebutuhan dengan menambahkan `defer_loading: true`:

```json JSON
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" },
      "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["location"]
  },
  "defer_loading": true
}
```

**Poin-poin penting:**

- Alat tanpa `defer_loading` dimuat ke konteks segera
- Alat dengan `defer_loading: true` hanya dimuat ketika Claude menemukannya melalui pencarian
- Tool search tool itu sendiri **tidak boleh** memiliki `defer_loading: true`
- Pertahankan 3-5 alat yang paling sering digunakan sebagai non-deferred untuk performa optimal

Kedua varian tool search (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

## Format respons

Ketika Claude menggunakan tool search tool, respons menyertakan tipe blok baru:

```json JSON
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll search for tools to help with the weather information."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01ABC123",
      "name": "tool_search_tool_regex",
      "input": {
        "query": "weather"
      }
    },
    {
      "type": "tool_search_tool_result",
      "tool_use_id": "srvtoolu_01ABC123",
      "content": {
        "type": "tool_search_tool_search_result",
        "tool_references": [{ "type": "tool_reference", "tool_name": "get_weather" }]
      }
    },
    {
      "type": "text",
      "text": "I found a weather tool. Let me get the weather for San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01XYZ789",
      "name": "get_weather",
      "input": { "location": "San Francisco", "unit": "fahrenheit" }
    }
  ],
  "stop_reason": "tool_use"
}
```

### Memahami respons

- **`server_tool_use`**: Menunjukkan bahwa Claude sedang memanggil tool search tool
- **`tool_search_tool_result`**: Berisi hasil pencarian dengan objek `tool_search_tool_search_result` yang bersarang
- **`tool_references`**: Array objek `tool_reference` yang menunjuk ke alat yang ditemukan
- **`tool_use`**: Claude memanggil alat yang ditemukan

Blok `tool_reference` secara otomatis diperluas menjadi definisi alat lengkap sebelum ditampilkan ke Claude. Anda tidak perlu menangani perluasan ini sendiri. Ini terjadi secara otomatis di API selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

## Integrasi MCP

Tool search tool bekerja dengan [server MCP](/docs/id/agents-and-tools/mcp-connector). Tambahkan [beta header](/docs/id/api/beta-headers) `"mcp-client-2025-11-20"` ke permintaan API Anda, lalu gunakan `mcp_toolset` dengan `default_config` untuk menunda pemuatan alat MCP:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "anthropic-beta: mcp-client-2025-11-20" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-6",
    "max_tokens": 2048,
    "mcp_servers": [
      {
        "type": "url",
        "name": "database-server",
        "url": "https://mcp-db.example.com"
      }
    ],
    "tools": [
      {
        "type": "tool_search_tool_regex_20251119",
        "name": "tool_search_tool_regex"
      },
      {
        "type": "mcp_toolset",
        "mcp_server_name": "database-server",
        "default_config": {
          "defer_loading": true
        },
        "configs": {
          "search_events": {
            "defer_loading": false
          }
        }
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "What events are in my database?"
      }
    ]
  }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    betas=["mcp-client-2025-11-20"],
    max_tokens=2048,
    mcp_servers=[
        {"type": "url", "name": "database-server", "url": "https://mcp-db.example.com"}
    ],
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {
            "type": "mcp_toolset",
            "mcp_server_name": "database-server",
            "default_config": {"defer_loading": True},
            "configs": {"search_events": {"defer_loading": False}},
        },
    ],
    messages=[{"role": "user", "content": "What events are in my database?"}],
)

print(response)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.beta.messages.create({
    model: "claude-opus-4-6",
    betas: ["mcp-client-2025-11-20"],
    max_tokens: 2048,
    mcp_servers: [
      {
        type: "url",
        name: "database-server",
        url: "https://mcp-db.example.com"
      }
    ],
    tools: [
      {
        type: "tool_search_tool_regex_20251119",
        name: "tool_search_tool_regex"
      },
      {
        type: "mcp_toolset",
        mcp_server_name: "database-server",
        default_config: {
          defer_loading: true
        },
        configs: {
          search_events: {
            defer_loading: false
          }
        }
      }
    ],
    messages: [
      {
        role: "user",
        content: "What events are in my database?"
      }
    ]
  });

  console.log(JSON.stringify(response, null, 2));
}

main();
```

</CodeGroup>

**Opsi konfigurasi MCP:**

- `default_config.defer_loading`: Atur default untuk semua alat dari server MCP
- `configs`: Timpa default untuk alat tertentu berdasarkan nama
- Gabungkan beberapa server MCP dengan tool search untuk pustaka alat yang sangat besar

## Implementasi tool search kustom

Anda dapat mengimplementasikan logika tool search Anda sendiri (misalnya, menggunakan embeddings atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat kustom. Ketika Claude memanggil alat pencarian kustom Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas dengan `defer_loading: true`. Pendekatan ini memungkinkan Anda menggunakan algoritma pencarian yang lebih canggih sambil mempertahankan kompatibilitas dengan sistem tool search.

<Note>
Format `tool_search_tool_result` yang ditampilkan di bagian [Format respons](#response-format) adalah format sisi server yang digunakan secara internal oleh tool search bawaan Anthropic. Untuk implementasi sisi klien kustom, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan di atas.
</Note>

Untuk contoh lengkap menggunakan embeddings, lihat [cookbook tool search dengan embeddings](https://platform.claude.com/cookbooks) kami.

## Penanganan kesalahan

<Note>
  Tool search tool tidak kompatibel dengan [contoh penggunaan
  alat](/docs/id/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples).
  Jika Anda perlu memberikan contoh penggunaan alat, gunakan pemanggilan alat
  standar tanpa tool search.
</Note>

### Kesalahan HTTP (status 400)

Kesalahan ini mencegah permintaan diproses:

**Semua alat ditangguhkan:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "All tools have defer_loading set. At least one tool must be non-deferred."
  }
}
```

**Definisi alat tidak ditemukan:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Tool reference 'unknown_tool' has no corresponding tool definition"
  }
}
```

### Kesalahan hasil alat (status 200)

Kesalahan selama eksekusi alat mengembalikan respons 200 dengan informasi kesalahan di dalam body:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "srvtoolu_01ABC123",
  "content": {
    "type": "tool_search_tool_result_error",
    "error_code": "invalid_pattern"
  }
}
```

**Kode kesalahan:**

- `too_many_requests`: Batas laju terlampaui untuk operasi tool search
- `invalid_pattern`: Pola regex tidak valid
- `pattern_too_long`: Pola melebihi batas 200 karakter
- `unavailable`: Layanan tool search sementara tidak tersedia

### Kesalahan umum

<section title="Kesalahan 400: Semua alat ditangguhkan">

**Penyebab**: Anda menetapkan `defer_loading: true` pada SEMUA alat termasuk alat pencarian

**Perbaikan**: Hapus `defer_loading` dari tool search tool:

```json
{
  "type": "tool_search_tool_regex_20251119", // Tidak ada defer_loading di sini
  "name": "tool_search_tool_regex"
}
```

</section>

<section title="Kesalahan 400: Definisi alat tidak ditemukan">

**Penyebab**: Sebuah `tool_reference` menunjuk ke alat yang tidak ada dalam array `tools` Anda

**Perbaikan**: Pastikan setiap alat yang dapat ditemukan memiliki definisi lengkap:

```json
{
  "name": "my_tool",
  "description": "Full description here",
  "input_schema": {
    // skema lengkap
  },
  "defer_loading": true
}
```

</section>

<section title="Claude tidak menemukan alat yang diharapkan">

**Penyebab**: Nama atau deskripsi alat tidak cocok dengan pola regex

**Langkah debugging:**

1. Periksa nama dan deskripsi alat. Claude mencari KEDUA bidang tersebut
2. Uji pola Anda: `import re; re.search(r"your_pattern", "tool_name")`
3. Ingat pencarian peka huruf besar/kecil secara default (gunakan `(?i)` untuk tidak peka huruf besar/kecil)
4. Claude menggunakan pola luas seperti `".*weather.*"` bukan pencocokan tepat

**Tips**: Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemampuan penemuan

</section>

## Prompt caching

Tool search bekerja dengan [prompt caching](/docs/id/build-with-claude/prompt-caching). Tambahkan breakpoint `cache_control` untuk mengoptimalkan percakapan multi-giliran:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

# Permintaan pertama dengan tool search
messages = [{"role": "user", "content": "What's the weather in Seattle?"}]

response1 = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=messages,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {
            "name": "get_weather",
            "description": "Get weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
            "defer_loading": True,
        },
    ],
)

# Tambahkan respons Claude ke percakapan
messages.append({"role": "assistant", "content": response1.content})

# Permintaan kedua dengan breakpoint cache
messages.append(
    {
        "role": "user",
        "content": "What about New York?",
        "cache_control": {"type": "ephemeral"},
    }
)

response2 = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=messages,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {
            "name": "get_weather",
            "description": "Get weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
            "defer_loading": True,
        },
    ],
)

print(f"Cache read tokens: {response2.usage.get('cache_read_input_tokens', 0)}")
```
</CodeGroup>

Sistem secara otomatis memperluas blok tool_reference di seluruh riwayat percakapan, sehingga Claude dapat menggunakan kembali alat yang ditemukan dalam giliran berikutnya tanpa perlu mencari ulang.

## Streaming

Dengan streaming diaktifkan, Anda akan menerima event tool search sebagai bagian dari stream:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "tool_search_tool_regex"}}

// Kueri pencarian di-stream
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"query\":\"weather\"}"}}

// Jeda saat pencarian dieksekusi

// Hasil pencarian di-stream
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "tool_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "tool_search_tool_search_result", "tool_references": [{"type": "tool_reference", "tool_name": "get_weather"}]}}}

// Claude melanjutkan dengan alat yang ditemukan
```

## Permintaan batch

Anda dapat menyertakan tool search tool dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Operasi tool search melalui Messages Batches API dihargai sama dengan yang ada dalam permintaan Messages API biasa.

## Retensi data

Tool search sisi server (alat `tool_search`) mengindeks dan menyimpan data katalog alat (nama alat, deskripsi, dan metadata argumen) di luar respons API langsung. Data disimpan sesuai dengan kebijakan retensi standar Anthropic. Implementasi tool search sisi klien kustom yang menggunakan Messages API standar sepenuhnya memenuhi syarat ZDR.

Untuk kelayakan ZDR di semua fitur, lihat [API dan Retensi Data](/docs/id/build-with-claude/api-and-data-retention).

## Batas dan praktik terbaik

### Batas

- **Alat maksimum**: 10.000 alat dalam katalog Anda
- **Hasil pencarian**: Mengembalikan 3-5 alat paling relevan per pencarian
- **Panjang pola**: Maksimum 200 karakter untuk pola regex
- **Dukungan model**: Sonnet 4.0+, Opus 4.0+ saja (tidak ada Haiku)

### Kapan menggunakan tool search

**Kasus penggunaan yang baik:**

- 10+ alat tersedia dalam sistem Anda
- Definisi alat mengonsumsi >10K token
- Mengalami masalah akurasi pemilihan alat dengan set alat yang besar
- Membangun sistem bertenaga MCP dengan beberapa server (200+ alat)
- Pustaka alat yang terus berkembang seiring waktu

**Kapan pemanggilan alat tradisional mungkin lebih baik:**

- Kurang dari 10 alat secara total
- Semua alat sering digunakan dalam setiap permintaan
- Definisi alat yang sangat kecil (\<100 token secara total)

### Tips optimasi

- Pertahankan 3-5 alat yang paling sering digunakan sebagai non-deferred
- Tulis nama dan deskripsi alat yang jelas dan deskriptif
- Gunakan penamaan yang konsisten dalam nama alat: awali dengan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga kueri pencarian secara alami menampilkan kelompok alat yang tepat
- Gunakan kata kunci semantik dalam deskripsi yang cocok dengan cara pengguna mendeskripsikan tugas
- Tambahkan bagian prompt sistem yang mendeskripsikan kategori alat yang tersedia: "You can search for tools to interact with Slack, GitHub, and Jira"
- Pantau alat mana yang ditemukan Claude untuk menyempurnakan deskripsi

## Penggunaan

Penggunaan tool search tool dilacak dalam objek penggunaan respons:

```json JSON
{
  "usage": {
    "input_tokens": 1024,
    "output_tokens": 256,
    "server_tool_use": {
      "tool_search_requests": 2
    }
  }
}
```