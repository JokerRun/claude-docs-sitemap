---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: a917dd1f33b865492a8ba70ee8db0d509d7837fd7ff548224bf0454173c05ac4
---

# Alat pengambilan web

Alat pengambilan web memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

---

Alat pengambilan web memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi alat pengambilan web terbaru (`web_fetch_20260209`) mendukung **penyaringan dinamis** dengan Claude Opus 4.6 dan Sonnet 4.6. Claude dapat menulis dan menjalankan kode untuk menyaring konten yang diambil sebelum mencapai jendela konteks, menyimpan hanya informasi yang relevan dan membuang sisanya. Ini mengurangi konsumsi token sambil mempertahankan kualitas respons. Versi alat sebelumnya (`web_fetch_20250910`) tetap tersedia tanpa penyaringan dinamis.

<Note>
Silakan gunakan [formulir ini](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan umpan balik tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

<Note>
This feature is [Zero Data Retention (ZDR)](/docs/en/build-with-claude/zero-data-retention) eligible. When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

<Warning>
Mengaktifkan alat pengambilan web di lingkungan tempat Claude memproses input yang tidak dipercaya bersama data sensitif menimbulkan risiko exfiltration data. Kami merekomendasikan hanya menggunakan alat ini di lingkungan terpercaya atau saat menangani data non-sensitif.

Untuk meminimalkan risiko exfiltration, Claude tidak diizinkan untuk secara dinamis membangun URL. Claude hanya dapat mengambil URL yang telah secara eksplisit disediakan oleh pengguna atau yang berasal dari hasil pencarian web atau pengambilan web sebelumnya. Namun, masih ada risiko residual yang harus dipertimbangkan dengan hati-hati saat menggunakan alat ini.

Jika exfiltration data menjadi perhatian, pertimbangkan:
- Menonaktifkan alat pengambilan web sepenuhnya
- Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
- Menggunakan parameter `allowed_domains` untuk membatasi ke domain yang diketahui aman
</Warning>

## Model yang didukung

Pengambilan web tersedia di:

- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations)) (`claude-3-7-sonnet-20250219`)
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations)) (`claude-3-5-haiku-latest`)

## Cara kerja pengambilan web

Saat Anda menambahkan alat pengambilan web ke permintaan API Anda:

1. Claude memutuskan kapan harus mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, ekstraksi teks otomatis dilakukan.
4. Claude menganalisis konten yang diambil dan memberikan respons dengan kutipan opsional.

<Note>
Alat pengambilan web saat ini tidak mendukung situs web yang dirender secara dinamis melalui Javascript.
</Note>

### Penyaringan dinamis dengan Opus 4.6 dan Sonnet 4.6

Mengambil halaman web dan PDF lengkap dapat dengan cepat mengonsumsi token, terutama ketika hanya informasi spesifik yang diperlukan dari dokumen besar. Dengan versi alat `web_fetch_20260209`, Claude dapat menulis dan menjalankan kode untuk menyaring konten yang diambil sebelum memuatnya ke dalam konteks.

Penyaringan dinamis ini sangat berguna untuk:
- Mengekstrak bagian spesifik dari dokumen panjang
- Memproses data terstruktur dari halaman web
- Menyaring informasi yang relevan dari PDF
- Mengurangi biaya token saat bekerja dengan dokumen besar

<Note>
Penyaringan dinamis memerlukan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan. Alat pengambilan web (dengan dan tanpa penyaringan dinamis) tersedia di Claude API dan Microsoft Azure.
</Note>

Untuk mengaktifkan penyaringan dinamis, gunakan versi alat `web_fetch_20260209` dengan header beta `code-execution-web-tools-2026-02-09`:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: code-execution-web-tools-2026-02-09" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Fetch the content at https://example.com/research-paper and extract the key findings."
            }
        ],
        "tools": [{
            "type": "web_fetch_20260209",
            "name": "web_fetch"
        }]
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-web-tools-2026-02-09"],
    messages=[
        {
            "role": "user",
            "content": "Fetch the content at https://example.com/research-paper and extract the key findings.",
        }
    ],
    tools=[{"type": "web_fetch_20260209", "name": "web_fetch"}],
)
print(response)
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 4096,
    betas: ["code-execution-web-tools-2026-02-09"],
    messages: [
      {
        role: "user",
        content:
          "Fetch the content at https://example.com/research-paper and extract the key findings."
      }
    ],
    tools: [{ type: "web_fetch_20260209", name: "web_fetch" }]
  });

  console.log(response);
}

main().catch(console.error);
```
</CodeGroup>

## Cara menggunakan pengambilan web

Sediakan alat pengambilan web dalam permintaan API Anda:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "Please analyze the content at https://example.com/article"
            }
        ],
        "tools": [{
            "type": "web_fetch_20250910",
            "name": "web_fetch",
            "max_uses": 5
        }]
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Please analyze the content at https://example.com/article",
        }
    ],
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5}],
)
print(response)
```

```typescript TypeScript
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const response = await anthropic.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Please analyze the content at https://example.com/article"
      }
    ],
    tools: [{
      type: "web_fetch_20250910",
      name: "web_fetch",
      max_uses: 5
    }]
  });

  console.log(response);
}

main().catch(console.error);
```
</CodeGroup>

### Definisi alat

Alat pengambilan web mendukung parameter berikut:

```json JSON
{
  "type": "web_fetch_20250910",
  "name": "web_fetch",

  // Optional: Limit the number of fetches per request
  "max_uses": 10,

  // Optional: Only fetch from these domains
  "allowed_domains": ["example.com", "docs.example.com"],

  // Optional: Never fetch from these domains
  "blocked_domains": ["private.example.com"],

  // Optional: Enable citations for fetched content
  "citations": {
    "enabled": true
  },

  // Optional: Maximum content length in tokens
  "max_content_tokens": 100000
}
```

#### Penggunaan maksimal

Parameter `max_uses` membatasi jumlah pengambilan web yang dilakukan. Jika Claude mencoba lebih banyak pengambilan daripada yang diizinkan, `web_fetch_tool_result` akan menjadi kesalahan dengan kode kesalahan `max_uses_exceeded`. Saat ini tidak ada batas default.

#### Penyaringan domain

Saat menggunakan filter domain:

- Domain tidak boleh menyertakan skema HTTP/HTTPS (gunakan `example.com` bukan `https://example.com`)
- Subdomain secara otomatis disertakan (`example.com` mencakup `docs.example.com`)
- Subpath didukung (`example.com/blog`)
- Anda dapat menggunakan `allowed_domains` atau `blocked_domains`, tetapi tidak keduanya dalam permintaan yang sama.

<Warning>
Perhatikan bahwa karakter Unicode dalam nama domain dapat menciptakan kerentanan keamanan melalui serangan homograf, di mana karakter yang terlihat serupa dari skrip berbeda dapat melewati filter domain. Misalnya, `аmazon.com` (menggunakan 'а' Cyrillic) mungkin terlihat identik dengan `amazon.com` tetapi mewakili domain yang berbeda.

Saat mengonfigurasi daftar izin/blokir domain:
- Gunakan nama domain ASCII-only jika memungkinkan
- Pertimbangkan bahwa parser URL dapat menangani normalisasi Unicode secara berbeda
- Uji filter domain Anda dengan variasi homograf potensial
- Audit secara teratur konfigurasi domain Anda untuk karakter Unicode yang mencurigakan
</Warning>

#### Batas konten

Parameter `max_content_tokens` membatasi jumlah konten yang akan disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, konten akan dipotong. Ini membantu mengontrol penggunaan token saat mengambil dokumen besar.

<Note>
Batas parameter `max_content_tokens` bersifat perkiraan. Jumlah token input aktual yang digunakan dapat bervariasi dalam jumlah kecil.
</Note>

#### Kutipan

Tidak seperti pencarian web di mana kutipan selalu diaktifkan, kutipan bersifat opsional untuk pengambilan web. Atur `"citations": {"enabled": true}` untuk memungkinkan Claude mengutip bagian spesifik dari dokumen yang diambil.

<Note>
Saat menampilkan output API secara langsung kepada pengguna akhir, kutipan harus disertakan ke sumber asli. Jika Anda membuat modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan kutipan sesuai kebutuhan berdasarkan konsultasi dengan tim hukum Anda.
</Note>

### Respons

Berikut adalah contoh struktur respons:

```json
{
  "role": "assistant",
  "content": [
    // 1. Claude's decision to fetch
    {
      "type": "text",
      "text": "I'll fetch the content from the article to analyze it."
    },
    // 2. The fetch request
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01234567890abcdef",
      "name": "web_fetch",
      "input": {
        "url": "https://example.com/article"
      }
    },
    // 3. Fetch results
    {
      "type": "web_fetch_tool_result",
      "tool_use_id": "srvtoolu_01234567890abcdef",
      "content": {
        "type": "web_fetch_result",
        "url": "https://example.com/article",
        "content": {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "Full text content of the article..."
          },
          "title": "Article Title",
          "citations": {"enabled": true}
        },
        "retrieved_at": "2025-08-25T10:30:00Z"
      }
    },
    // 4. Claude's analysis with citations (if enabled)
    {
      "text": "Based on the article, ",
      "type": "text"
    },
    {
      "text": "the main argument presented is that artificial intelligence will transform healthcare",
      "type": "text",
      "citations": [
        {
          "type": "char_location",
          "document_index": 0,
          "document_title": "Article Title",
          "start_char_index": 1234,
          "end_char_index": 1456,
          "cited_text": "Artificial intelligence is poised to revolutionize healthcare delivery..."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

#### Hasil pengambilan

Hasil pengambilan mencakup:

- `url`: URL yang diambil
- `content`: Blok dokumen yang berisi konten yang diambil
- `retrieved_at`: Stempel waktu saat konten diambil

<Note>
Alat pengambilan web menyimpan hasil dalam cache untuk meningkatkan kinerja dan mengurangi permintaan yang berlebihan. Ini berarti konten yang dikembalikan mungkin tidak selalu merupakan versi terbaru yang tersedia di URL. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan jenis konten dan pola penggunaan yang berbeda.
</Note>

Untuk dokumen PDF, konten akan dikembalikan sebagai data yang dikodekan base64:

```json
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_02",
  "content": {
    "type": "web_fetch_result",
    "url": "https://example.com/paper.pdf",
    "content": {
      "type": "document",
      "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": "JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmo..."
      },
      "citations": {"enabled": true}
    },
    "retrieved_at": "2025-08-25T10:30:02Z"
  }
}
```

#### Kesalahan

Ketika alat pengambilan web mengalami kesalahan, Claude API mengembalikan respons 200 (berhasil) dengan kesalahan yang diwakili dalam badan respons:

```json
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_a93jad",
  "content": {
    "type": "web_fetch_tool_error",
    "error_code": "url_not_accessible"
  }
}
```

Ini adalah kode kesalahan yang mungkin:

- `invalid_input`: Format URL tidak valid
- `url_too_long`: URL melebihi panjang maksimum (250 karakter)
- `url_not_allowed`: URL diblokir oleh aturan penyaringan domain dan pembatasan model
- `url_not_accessible`: Gagal mengambil konten (kesalahan HTTP)
- `too_many_requests`: Batas laju terlampaui
- `unsupported_content_type`: Jenis konten tidak didukung (hanya teks dan PDF)
- `max_uses_exceeded`: Penggunaan alat pengambilan web maksimum terlampaui
- `unavailable`: Kesalahan internal terjadi

## Validasi URL

Untuk alasan keamanan, alat pengambilan web hanya dapat mengambil URL yang sebelumnya muncul dalam konteks percakapan. Ini mencakup:

- URL dalam pesan pengguna
- URL dalam hasil alat sisi klien
- URL dari hasil pencarian web atau pengambilan web sebelumnya

Alat tidak dapat mengambil URL arbitrer yang dihasilkan Claude atau URL dari alat server berbasis kontainer (Eksekusi Kode, Bash, dll.).

## Pencarian dan pengambilan gabungan

Pengambilan web bekerja dengan mulus dengan pencarian web untuk pengumpulan informasi yang komprehensif:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Find recent articles about quantum computing and analyze the most relevant one in detail",
        }
    ],
    tools=[
        {"type": "web_search_20250305", "name": "web_search", "max_uses": 3},
        {
            "type": "web_fetch_20250910",
            "name": "web_fetch",
            "max_uses": 5,
            "citations": {"enabled": True},
        },
    ],
)
```

Dalam alur kerja ini, Claude akan:
1. Menggunakan pencarian web untuk menemukan artikel yang relevan
2. Memilih hasil yang paling menjanjikan
3. Menggunakan pengambilan web untuk mengambil konten lengkap
4. Memberikan analisis terperinci dengan kutipan

## Caching prompt

Pengambilan web bekerja dengan [caching prompt](/docs/id/build-with-claude/prompt-caching). Untuk mengaktifkan caching prompt, tambahkan titik henti `cache_control` dalam permintaan Anda. Hasil pengambilan yang di-cache dapat digunakan kembali di seluruh putaran percakapan.

```python
import anthropic

client = anthropic.Anthropic()

# First request with web fetch
messages = [
    {
        "role": "user",
        "content": "Analyze this research paper: https://arxiv.org/abs/2024.12345",
    }
]

response1 = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=messages,
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch"}],
)

# Add Claude's response to conversation
messages.append({"role": "assistant", "content": response1.content})

# Second request with cache breakpoint
messages.append(
    {
        "role": "user",
        "content": "What methodology does the paper use?",
        "cache_control": {"type": "ephemeral"},
    }
)

response2 = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=messages,
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch"}],
)

# The second response benefits from cached fetch results
print(f"Cache read tokens: {response2.usage.get('cache_read_input_tokens', 0)}")
```

## Streaming

Dengan streaming diaktifkan, acara pengambilan adalah bagian dari aliran dengan jeda selama pengambilan konten:

```json
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Claude's decision to fetch

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_fetch"}}

// Fetch URL streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"url\":\"https://example.com/article\"}"}}

// Pause while fetch executes

// Fetch results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_fetch_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "web_fetch_result", "url": "https://example.com/article", "content": {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "Article content..."}}}}}

// Claude's response continues...
```

## Permintaan batch

Anda dapat menyertakan alat pengambilan web dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat pengambilan web melalui Messages Batches API dihargai sama dengan yang ada dalam permintaan Messages API reguler.

## Penggunaan dan harga

Web fetch usage has **no additional charges** beyond standard token costs:

```json
"usage": {
  "input_tokens": 25039,
  "output_tokens": 931,
  "cache_read_input_tokens": 0,
  "cache_creation_input_tokens": 0,
  "server_tool_use": {
    "web_fetch_requests": 1
  }
}
```

The web fetch tool is available on the Claude API at **no additional cost**. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the `max_content_tokens` parameter to set appropriate limits based on your use case and budget considerations.

Example token usage for typical content:
- Average web page (10KB): ~2,500 tokens
- Large documentation page (100KB): ~25,000 tokens  
- Research paper PDF (500KB): ~125,000 tokens