---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: 754384e497edad8f1bfd68488754629b973ab09901ffd8789f10542d2fe0f6f0
---

# Pemanggilan alat secara terprogram

Pelajari cara Claude memanggil alat secara terprogram dalam container eksekusi kode untuk mengurangi latensi dan konsumsi token.

---

Pemanggilan alat secara terprogram memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram dalam container [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), daripada memerlukan bolak-balik melalui model untuk setiap pemanggilan alat. Ini mengurangi latensi untuk alur kerja multi-alat dan mengurangi konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum mencapai jendela konteks model. Pada benchmark pencarian agentik seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji penelitian web multi-langkah dan pengambilan informasi yang kompleks, menambahkan pemanggilan alat secara terprogram di atas alat pencarian dasar adalah faktor kunci yang sepenuhnya membuka kinerja agen.

Perbedaannya bertambah cepat dalam alur kerja nyata. Pertimbangkan pemeriksaan kepatuhan anggaran di 20 karyawan: pendekatan tradisional memerlukan 20 bolak-balik model terpisah, menarik ribuan item baris pengeluaran ke dalam konteks di sepanjang jalan. Dengan pemanggilan alat secara terprogram, satu skrip menjalankan semua 20 pencarian, memfilter hasilnya, dan hanya mengembalikan karyawan yang melebihi batas mereka, menyusutkan apa yang perlu dipertimbangkan Claude dari ratusan kilobyte menjadi beberapa baris.

<Tip>
Untuk melihat lebih dalam biaya inferensi dan konteks yang ditangani oleh pemanggilan alat secara terprogram, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
Fitur ini memerlukan alat eksekusi kode untuk diaktifkan.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Kompatibilitas model

Pemanggilan alat secara terprogram tersedia pada model-model berikut:

| Model | Versi Alat |
|-------|--------------|
| Claude Opus 4.6 (`claude-opus-4-6`) | `code_execution_20260120` |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`) | `code_execution_20260120` |
| Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) | `code_execution_20260120` |
| Claude Opus 4.5 (`claude-opus-4-5-20251101`) | `code_execution_20260120` |

<Warning>
Pemanggilan alat secara terprogram tersedia melalui Claude API dan Microsoft Foundry.
</Warning>

## Mulai cepat

Berikut adalah contoh sederhana di mana Claude secara terprogram mengkueri database beberapa kali dan mengagregasi hasilnya:

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
                "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
            }
        ],
        "tools": [
            {
                "type": "code_execution_20260120",
                "name": "code_execution"
            },
            {
                "name": "query_database",
                "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL query to execute"
                        }
                    },
                    "required": ["sql"]
                },
                "allowed_callers": ["code_execution_20260120"]
            }
        ]
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
            "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue",
        }
    ],
    tools=[
        {"type": "code_execution_20260120", "name": "code_execution"},
        {
            "name": "query_database",
            "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL query to execute"}
                },
                "required": ["sql"],
            },
            "allowed_callers": ["code_execution_20260120"],
        },
    ],
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
        content:
          "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
      }
    ],
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description:
          "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  });

  console.log(response);
}

main().catch(console.error);
```
</CodeGroup>

## Cara kerja pemanggilan alat secara terprogram

Ketika Anda mengonfigurasi alat agar dapat dipanggil dari eksekusi kode dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat sebagai fungsi, yang berpotensi mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini dalam container yang disandbox melalui eksekusi kode
3. Ketika fungsi alat dipanggil, eksekusi kode dijeda dan API mengembalikan blok `tool_use`
4. Anda memberikan hasil alat, dan eksekusi kode berlanjut (hasil antara tidak dimuat ke dalam jendela konteks Claude)
5. Setelah semua eksekusi kode selesai, Claude menerima output akhir dan melanjutkan mengerjakan tugas

Pendekatan ini sangat berguna untuk:
- **Pemrosesan data besar**: Filter atau agregasi hasil alat sebelum mencapai konteks Claude
- **Alur kerja multi-langkah**: Hemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa mengambil sampel Claude di antara pemanggilan alat
- **Logika kondisional**: Membuat keputusan berdasarkan hasil alat antara

<Note>
Alat kustom dikonversi menjadi fungsi Python async untuk mendukung pemanggilan alat paralel. Ketika Claude menulis kode yang memanggil alat Anda, ia menggunakan `await` (misalnya, `result = await query_database("<sql>")`) dan secara otomatis menyertakan fungsi pembungkus async yang sesuai.

Pembungkus async dihilangkan dari contoh kode dalam dokumentasi ini untuk kejelasan.
</Note>

## Konsep inti

### Bidang `allowed_callers`

Bidang `allowed_callers` menentukan konteks mana yang dapat memanggil alat:

```json
{
  "name": "query_database",
  "description": "Execute a SQL query against the database",
  "input_schema": {
    // ...
  },
  "allowed_callers": ["code_execution_20260120"]
}
```

**Nilai yang mungkin:**
- `["direct"]` - Hanya Claude yang dapat memanggil alat ini secara langsung (default jika dihilangkan)
- `["code_execution_20260120"]` - Hanya dapat dipanggil dari dalam eksekusi kode
- `["direct", "code_execution_20260120"]` - Dapat dipanggil baik secara langsung maupun dari eksekusi kode

<Tip>
Pilih salah satu `["direct"]` atau `["code_execution_20260120"]` untuk setiap alat daripada mengaktifkan keduanya, karena ini memberikan panduan yang lebih jelas kepada Claude tentang cara terbaik menggunakan alat tersebut.
</Tip>

### Bidang `caller` dalam respons

Setiap blok penggunaan alat menyertakan bidang `caller` yang menunjukkan bagaimana alat dipanggil:

**Pemanggilan langsung (penggunaan alat tradisional):**
```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": { "type": "direct" }
}
```

**Pemanggilan terprogram:**
```json
{
  "type": "tool_use",
  "id": "toolu_xyz789",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_abc123"
  }
}
```

`tool_id` mereferensikan alat eksekusi kode yang melakukan pemanggilan terprogram.

### Siklus hidup container

Pemanggilan alat secara terprogram menggunakan container yang sama dengan eksekusi kode:

- **Pembuatan container**: Container baru dibuat untuk setiap sesi kecuali Anda menggunakan kembali yang sudah ada
- **Kedaluwarsa**: Container kedaluwarsa setelah sekitar 4,5 menit tidak aktif (dapat berubah)
- **ID container**: Dikembalikan dalam respons melalui bidang `container`
- **Penggunaan ulang**: Berikan ID container untuk mempertahankan status di seluruh permintaan

<Warning>
Ketika alat dipanggil secara terprogram dan container menunggu hasil alat Anda, Anda harus merespons sebelum container kedaluwarsa. Pantau bidang `expires_at`. Jika container kedaluwarsa, Claude mungkin memperlakukan pemanggilan alat sebagai waktu habis dan mencoba lagi.
</Warning>

## Contoh alur kerja

Berikut adalah cara kerja alur pemanggilan alat secara terprogram yang lengkap:

### Langkah 1: Permintaan awal

Kirim permintaan dengan eksekusi kode dan alat yang memungkinkan pemanggilan terprogram. Untuk mengaktifkan pemanggilan terprogram, tambahkan bidang `allowed_callers` ke definisi alat Anda.

<Note>
Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude akan mencoba melakukan deserialisasi dan memproses hasilnya dalam kode. Semakin banyak detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara terprogram.
</Note>

<CodeGroup>
```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue",
        }
    ],
    tools=[
        {"type": "code_execution_20260120", "name": "code_execution"},
        {
            "name": "query_database",
            "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
            "input_schema": {
                # ...
            },
            "allowed_callers": ["code_execution_20260120"],
        },
    ],
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
        "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
    }
  ],
  tools: [
    {
      type: "code_execution_20260120",
      name: "code_execution"
    },
    {
      name: "query_database",
      description:
        "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
      input_schema: {
        // ...
      },
      allowed_callers: ["code_execution_20260120"]
    }
  ]
});
```
</CodeGroup>

### Langkah 2: Respons API dengan pemanggilan alat

Claude menulis kode yang memanggil alat Anda. API dijeda dan mengembalikan:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll query the purchase history and analyze the results."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_abc123",
      "name": "code_execution",
      "input": {
        "code": "results = await query_database('<sql>')\ntop_customers = sorted(results, key=lambda x: x['revenue'], reverse=True)[:5]\nprint(f'Top 5 customers: {top_customers}')"
      }
    },
    {
      "type": "tool_use",
      "id": "toolu_def456",
      "name": "query_database",
      "input": { "sql": "<sql>" },
      "caller": {
        "type": "code_execution_20260120",
        "tool_id": "srvtoolu_abc123"
      }
    }
  ],
  "container": {
    "id": "container_xyz789",
    "expires_at": "2025-01-15T14:30:00Z"
  },
  "stop_reason": "tool_use"
}
```

### Langkah 3: Berikan hasil alat

Sertakan riwayat percakapan lengkap beserta hasil alat Anda:

<CodeGroup>
```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    container="container_xyz789",  # Gunakan kembali container
    messages=[
        {
            "role": "user",
            "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue",
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I'll query the purchase history and analyze the results.",
                },
                {
                    "type": "server_tool_use",
                    "id": "srvtoolu_abc123",
                    "name": "code_execution",
                    "input": {"code": "..."},
                },
                {
                    "type": "tool_use",
                    "id": "toolu_def456",
                    "name": "query_database",
                    "input": {"sql": "<sql>"},
                    "caller": {
                        "type": "code_execution_20260120",
                        "tool_id": "srvtoolu_abc123",
                    },
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_def456",
                    "content": '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                }
            ],
        },
    ],
    tools=[...],
)
```

```typescript TypeScript
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  container: "container_xyz789", // Gunakan kembali container
  messages: [
    {
      role: "user",
      content:
        "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
    },
    {
      role: "assistant",
      content: [
        { type: "text", text: "I'll query the purchase history and analyze the results." },
        {
          type: "server_tool_use",
          id: "srvtoolu_abc123",
          name: "code_execution",
          input: { code: "..." }
        },
        {
          type: "tool_use",
          id: "toolu_def456",
          name: "query_database",
          input: { sql: "<sql>" },
          caller: {
            type: "code_execution_20260120",
            tool_id: "srvtoolu_abc123"
          }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "toolu_def456",
          content:
            '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
        }
      ]
    }
  ],
  tools: [
    // ...
  ]
});
```
</CodeGroup>

### Langkah 4: Pemanggilan alat berikutnya atau penyelesaian

Eksekusi kode berlanjut dan memproses hasilnya. Jika pemanggilan alat tambahan diperlukan, ulangi Langkah 3 hingga semua pemanggilan alat terpenuhi.

### Langkah 5: Respons akhir

Setelah eksekusi kode selesai, Claude memberikan respons akhir:

```json
{
  "content": [
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_abc123",
      "content": {
        "type": "code_execution_result",
        "stdout": "Top 5 customers by revenue:\n1. Customer C1: $45,000\n2. Customer C2: $38,000\n3. Customer C5: $32,000\n4. Customer C8: $28,500\n5. Customer C3: $24,000",
        "stderr": "",
        "return_code": 0,
        "content": []
      }
    },
    {
      "type": "text",
      "text": "I've analyzed the purchase history from last quarter. Your top 5 customers generated $167,500 in total revenue, with Customer C1 leading at $45,000."
    }
  ],
  "stop_reason": "end_turn"
}
```

## Pola lanjutan

### Pemrosesan batch dengan loop

Claude dapat menulis kode yang memproses beberapa item secara efisien:

```python
# pembungkus async dihilangkan untuk kejelasan
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    data = await query_database(f"<sql for {region}>")
    results[region] = sum(row["revenue"] for row in data)

# Proses hasil secara terprogram
top_region = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")
```

Pola ini:
- Mengurangi bolak-balik model dari N (satu per wilayah) menjadi 1
- Memproses kumpulan hasil besar secara terprogram sebelum kembali ke Claude
- Menghemat token dengan hanya mengembalikan kesimpulan yang diagregasi alih-alih data mentah

### Penghentian awal

Claude dapat berhenti memproses segera setelah kriteria keberhasilan terpenuhi:

```python
# pembungkus async dihilangkan untuk kejelasan
endpoints = ["us-east", "eu-west", "apac"]
for endpoint in endpoints:
    status = await check_health(endpoint)
    if status == "healthy":
        print(f"Found healthy endpoint: {endpoint}")
        break  # Berhenti lebih awal, jangan periksa yang tersisa
```

### Pemilihan alat kondisional

```python
# pembungkus async dihilangkan untuk kejelasan
file_info = await get_file_info(path)
if file_info["size"] < 10000:
    content = await read_full_file(path)
else:
    content = await read_file_summary(path)
print(content)
```

### Pemfilteran data

```python
# pembungkus async dihilangkan untuk kejelasan
logs = await fetch_logs(server_id)
errors = [log for log in logs if "ERROR" in log]
print(f"Found {len(errors)} errors")
for error in errors[-10:]:  # Hanya kembalikan 10 error terakhir
    print(error)
```

## Format respons

### Pemanggilan alat terprogram

Ketika eksekusi kode memanggil alat:

```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_xyz789"
  }
}
```

### Penanganan hasil alat

Hasil alat Anda diteruskan kembali ke kode yang berjalan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_abc123",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000, \"orders\": 23}, {\"customer_id\": \"C2\", \"revenue\": 38000, \"orders\": 18}, ...]"
    }
  ]
}
```

### Penyelesaian eksekusi kode

Ketika semua pemanggilan alat terpenuhi dan kode selesai:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_xyz789",
  "content": {
    "type": "code_execution_result",
    "stdout": "Analysis complete. Top 5 customers identified from 847 total records.",
    "stderr": "",
    "return_code": 0,
    "content": []
  }
}
```

## Penanganan error

### Error umum

| Error | Deskripsi | Solusi |
|-------|-------------|----------|
| `invalid_tool_input` | Input alat tidak sesuai dengan skema | Validasi input_schema alat Anda |
| `tool_not_allowed` | Alat tidak mengizinkan jenis pemanggil yang diminta | Periksa `allowed_callers` menyertakan konteks yang tepat |
| `missing_beta_header` | Header beta yang diperlukan tidak disediakan | Tambahkan header beta yang diperlukan ke permintaan Anda |

### Kedaluwarsa container selama pemanggilan alat

Jika alat Anda membutuhkan waktu terlalu lama untuk merespons, eksekusi kode akan menerima `TimeoutError`. Claude melihat ini di stderr dan biasanya akan mencoba lagi:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc123",
  "content": {
    "type": "code_execution_result",
    "stdout": "",
    "stderr": "TimeoutError: Calling tool ['query_database'] timed out.",
    "return_code": 0,
    "content": []
  }
}
```

Untuk mencegah timeout:
- Pantau bidang `expires_at` dalam respons
- Implementasikan timeout untuk eksekusi alat Anda
- Pertimbangkan untuk memecah operasi panjang menjadi potongan yang lebih kecil

### Error eksekusi alat

Jika alat Anda mengembalikan error:

```python
# Berikan informasi error dalam hasil alat
{
    "type": "tool_result",
    "tool_use_id": "toolu_abc123",
    "content": "Error: Query timeout - table lock exceeded 30 seconds",
}
```

Kode Claude akan menerima error ini dan dapat menanganinya dengan tepat.

## Batasan dan keterbatasan

### Ketidakcocokan fitur

- **Output terstruktur**: Alat dengan `strict: true` tidak didukung dengan pemanggilan terprogram
- **Pilihan alat**: Anda tidak dapat memaksa pemanggilan terprogram alat tertentu melalui `tool_choice`
- **Penggunaan alat paralel**: `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Pembatasan alat

Alat-alat berikut saat ini tidak dapat dipanggil secara terprogram, tetapi dukungan mungkin ditambahkan dalam rilis mendatang:

- Alat yang disediakan oleh [konektor MCP](/docs/id/agents-and-tools/mcp-connector)

### Pembatasan format pesan

Saat merespons pemanggilan alat terprogram, ada persyaratan format yang ketat:

**Respons hanya hasil alat**: Jika ada pemanggilan alat terprogram yang tertunda menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil alat.

Tidak valid - Tidak dapat menyertakan teks saat merespons pemanggilan alat terprogram:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    },
    { "type": "text", "text": "What should I do next?" }
  ]
}
```

Valid - Hanya hasil alat saat merespons pemanggilan alat terprogram:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    }
  ]
}
```

Pembatasan ini hanya berlaku saat merespons pemanggilan alat terprogram (eksekusi kode). Untuk pemanggilan alat sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil alat.

### Batas laju

Pemanggilan alat terprogram tunduk pada batas laju yang sama dengan pemanggilan alat biasa. Setiap pemanggilan alat dari eksekusi kode dihitung sebagai pemanggilan terpisah.

### Validasi hasil alat sebelum digunakan

Saat mengimplementasikan alat kustom yang akan dipanggil secara terprogram:

- **Hasil alat dikembalikan sebagai string**: Dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang mungkin diproses oleh lingkungan eksekusi.
- **Validasi hasil alat eksternal**: Jika alat Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan diinterpretasikan atau dieksekusi sebagai kode.

## Efisiensi token

Pemanggilan alat secara terprogram dapat secara signifikan mengurangi konsumsi token:

- **Hasil alat dari pemanggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir yang ditambahkan
- **Pemrosesan antara terjadi dalam kode** - pemfilteran, agregasi, dll. tidak mengonsumsi token model
- **Beberapa pemanggilan alat dalam satu eksekusi kode** - mengurangi overhead dibandingkan dengan giliran model terpisah

Misalnya, memanggil 10 alat secara langsung menggunakan ~10x token dibandingkan memanggil secara terprogram dan mengembalikan ringkasan.

## Penggunaan dan harga

Pemanggilan alat secara terprogram menggunakan harga yang sama dengan eksekusi kode. Lihat [harga eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detailnya.

<Note>
Penghitungan token untuk pemanggilan alat terprogram: Hasil alat dari pemanggilan terprogram tidak dihitung terhadap penggunaan token input/output Anda. Hanya hasil eksekusi kode akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik

### Desain alat

- **Berikan deskripsi output yang terperinci**: Karena Claude melakukan deserialisasi hasil alat dalam kode, dokumentasikan format dengan jelas (struktur JSON, jenis bidang, dll.)
- **Kembalikan data terstruktur**: JSON atau format yang mudah diurai lainnya bekerja paling baik untuk pemrosesan terprogram
- **Jaga respons tetap ringkas**: Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram

**Kasus penggunaan yang baik:**
- Memproses kumpulan data besar di mana Anda hanya membutuhkan agregat atau ringkasan
- Alur kerja multi-langkah dengan 3+ pemanggilan alat yang bergantung
- Operasi yang memerlukan pemfilteran, pengurutan, atau transformasi hasil alat
- Tugas di mana data antara tidak boleh mempengaruhi penalaran Claude
- Operasi paralel di banyak item (misalnya, memeriksa 50 endpoint)

**Kasus penggunaan yang kurang ideal:**
- Pemanggilan alat tunggal dengan respons sederhana
- Alat yang membutuhkan umpan balik pengguna segera
- Operasi yang sangat cepat di mana overhead eksekusi kode akan melebihi manfaatnya

### Optimasi kinerja

- **Gunakan kembali container** saat membuat beberapa permintaan terkait untuk mempertahankan status
- **Batch operasi serupa** dalam satu eksekusi kode jika memungkinkan

## Pemecahan masalah

### Masalah umum

**Error "Tool not allowed"**
- Verifikasi definisi alat Anda menyertakan `"allowed_callers": ["code_execution_20260120"]`

**Kedaluwarsa container**
- Pastikan Anda merespons pemanggilan alat dalam masa hidup container (~4,5 menit)
- Pantau bidang `expires_at` dalam respons
- Pertimbangkan untuk mengimplementasikan eksekusi alat yang lebih cepat

**Hasil alat tidak diurai dengan benar**
- Pastikan alat Anda mengembalikan data string yang dapat dideserialisasi oleh Claude
- Berikan dokumentasi format output yang jelas dalam deskripsi alat Anda

### Tips debugging

1. **Catat semua pemanggilan alat dan hasilnya** untuk melacak alur
2. **Periksa bidang `caller`** untuk mengonfirmasi pemanggilan terprogram
3. **Pantau ID container** untuk memastikan penggunaan ulang yang tepat
4. **Uji alat secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan alat secara terprogram berhasil

Pelatihan Claude mencakup paparan ekstensif terhadap kode, membuatnya efektif dalam menalar dan merantai pemanggilan fungsi. Ketika alat disajikan sebagai fungsi yang dapat dipanggil dalam lingkungan eksekusi kode, Claude dapat memanfaatkan kekuatan ini untuk:

- **Menalar secara alami tentang komposisi alat**: Merantai operasi dan menangani dependensi senatural menulis kode Python apa pun
- **Memproses hasil besar secara efisien**: Memfilter output alat yang besar, mengekstrak hanya data yang relevan, atau menulis hasil antara ke file sebelum mengembalikan ringkasan ke jendela konteks
- **Mengurangi latensi secara signifikan**: Menghilangkan overhead pengambilan sampel ulang Claude di antara setiap pemanggilan alat dalam alur kerja multi-langkah

Pendekatan ini memungkinkan alur kerja yang tidak praktis dengan penggunaan alat tradisional (seperti memproses file lebih dari 1M token) dengan memungkinkan Claude bekerja dengan data secara terprogram daripada memuat semuanya ke dalam konteks percakapan.

## Implementasi alternatif

Pemanggilan alat secara terprogram adalah pola yang dapat digeneralisasi yang dapat diimplementasikan di luar eksekusi kode terkelola Anthropic. Berikut adalah ikhtisar pendekatan-pendekatannya:

### Eksekusi langsung sisi klien

Berikan Claude alat eksekusi kode dan jelaskan fungsi apa yang tersedia di lingkungan tersebut. Ketika Claude memanggil alat dengan kode, aplikasi Anda mengeksekusinya secara lokal di mana fungsi-fungsi tersebut didefinisikan.

**Keuntungan:**
- Mudah diimplementasikan dengan perubahan arsitektur minimal
- Kontrol penuh atas lingkungan dan instruksi

**Kerugian:**
- Mengeksekusi kode yang tidak dipercaya di luar sandbox
- Pemanggilan alat dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat mengeksekusi kode arbitrer dengan aman, Anda menginginkan solusi sederhana, dan penawaran terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi tersandbox yang dikelola sendiri

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan dalam container tersandbox dengan pembatasan keamanan (misalnya, tidak ada egress jaringan). Jika alat Anda memerlukan sumber daya eksternal, Anda memerlukan protokol untuk mengeksekusi pemanggilan alat di luar sandbox.

**Keuntungan:**
- Pemanggilan alat terprogram yang aman di infrastruktur Anda sendiri
- Kontrol penuh atas lingkungan eksekusi

**Kerugian:**
- Kompleks untuk dibangun dan dipelihara
- Memerlukan pengelolaan infrastruktur dan komunikasi antar-proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai dengan persyaratan Anda.

### Eksekusi terkelola Anthropic

Pemanggilan alat terprogram Anthropic adalah versi terkelola dari eksekusi tersandbox dengan lingkungan Python yang memiliki pendapat yang disetel untuk Claude. Anthropic menangani manajemen container, eksekusi kode, dan komunikasi pemanggilan alat yang aman.

**Keuntungan:**
- Aman dan terjamin secara default
- Mudah diaktifkan dengan konfigurasi minimal
- Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan untuk menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API.

## Retensi data

Pemanggilan alat secara terprogram dibangun di atas infrastruktur eksekusi kode dan menggunakan container sandbox yang sama. Data container, termasuk artefak dan output eksekusi, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [API dan Retensi Data](/docs/id/build-with-claude/api-and-data-retention).

## Fitur terkait

<CardGroup cols={2}>
  <Card title="Alat Eksekusi Kode" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Pelajari tentang kemampuan eksekusi kode yang mendasari yang mendukung pemanggilan alat secara terprogram.
  </Card>
  <Card title="Ikhtisar Penggunaan Alat" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Pahami dasar-dasar penggunaan alat dengan Claude.
  </Card>
  <Card title="Implementasi Penggunaan Alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/implement-tool-use">
    Panduan langkah demi langkah untuk mengimplementasikan alat.
  </Card>
</CardGroup>