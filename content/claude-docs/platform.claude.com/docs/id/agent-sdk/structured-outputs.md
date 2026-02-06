---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/structured-outputs
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: eb2dfc546b58544cab178ae4df3bae37c93c31ebb57a94aebb142ecd36616d11
---

# Dapatkan output terstruktur dari agen

Kembalikan JSON yang divalidasi dari alur kerja agen menggunakan JSON Schema, Zod, atau Pydantic. Dapatkan data terstruktur yang aman tipe setelah penggunaan alat multi-putaran.

---

Output terstruktur memungkinkan Anda menentukan bentuk data yang tepat yang ingin Anda dapatkan kembali dari agen. Agen dapat menggunakan alat apa pun yang diperlukan untuk menyelesaikan tugas, dan Anda tetap mendapatkan JSON yang divalidasi sesuai dengan skema Anda di akhir. Tentukan [JSON Schema](https://json-schema.org/understanding-json-schema/about) untuk struktur yang Anda butuhkan, dan SDK menjamin output cocok dengannya.

Untuk keamanan tipe penuh, gunakan [Zod](#type-safe-schemas-with-zod-and-pydantic) (TypeScript) atau [Pydantic](#type-safe-schemas-with-zod-and-pydantic) (Python) untuk menentukan skema Anda dan dapatkan objek yang sangat diketik kembali.

## Mengapa output terstruktur?

Agen mengembalikan teks bentuk bebas secara default, yang berfungsi untuk obrolan tetapi tidak ketika Anda perlu menggunakan output secara terprogram. Output terstruktur memberi Anda data yang diketik yang dapat Anda teruskan langsung ke logika aplikasi, database, atau komponen UI Anda.

Pertimbangkan aplikasi resep di mana agen mencari web dan membawa kembali resep. Tanpa output terstruktur, Anda mendapatkan teks bentuk bebas yang perlu Anda parsing sendiri. Dengan output terstruktur, Anda menentukan bentuk yang Anda inginkan dan mendapatkan data yang diketik yang dapat Anda gunakan langsung di aplikasi Anda.

<section title="Tanpa output terstruktur">

```text
Berikut adalah resep kue cokelat chip klasik!

**Kue Cokelat Chip**
Waktu persiapan: 15 menit | Waktu memasak: 10 menit

Bahan-bahan:
- 2 1/4 cangkir tepung serbaguna
- 1 cangkir mentega, dilunakkan
...
```

Untuk menggunakan ini di aplikasi Anda, Anda perlu mengurai judul, mengonversi "15 menit" menjadi angka, memisahkan bahan dari instruksi, dan menangani pemformatan yang tidak konsisten di seluruh respons.

</section>
<section title="Dengan output terstruktur">

```json
{
  "name": "Chocolate Chip Cookies",
  "prep_time_minutes": 15,
  "cook_time_minutes": 10,
  "ingredients": [
    {"item": "all-purpose flour", "amount": 2.25, "unit": "cups"},
    {"item": "butter, softened", "amount": 1, "unit": "cup"},
    ...
  ],
  "steps": ["Preheat oven to 375°F", "Cream butter and sugar", ...]
}
```

Data yang diketik yang dapat Anda gunakan langsung di UI Anda.

</section>

## Mulai cepat

Untuk menggunakan output terstruktur, tentukan [JSON Schema](https://json-schema.org/understanding-json-schema/about) yang menggambarkan bentuk data yang Anda inginkan, kemudian teruskan ke `query()` melalui opsi `outputFormat` (TypeScript) atau opsi `output_format` (Python). Ketika agen selesai, pesan hasil mencakup bidang `structured_output` dengan data yang divalidasi sesuai dengan skema Anda.

Contoh di bawah ini meminta agen untuk meneliti Anthropic dan mengembalikan nama perusahaan, tahun didirikan, dan kantor pusat sebagai output terstruktur.

<CodeGroup>

```typescript TypeScript
import { query } from '@anthropic-ai/claude-agent-sdk'

// Tentukan bentuk data yang ingin Anda dapatkan kembali
const schema = {
  type: 'object',
  properties: {
    company_name: { type: 'string' },
    founded_year: { type: 'number' },
    headquarters: { type: 'string' }
  },
  required: ['company_name']
}

for await (const message of query({
  prompt: 'Research Anthropic and provide key company information',
  options: {
    outputFormat: {
      type: 'json_schema',
      schema: schema
    }
  }
})) {
  // Pesan hasil berisi structured_output dengan data yang divalidasi
  if (message.type === 'result' && message.structured_output) {
    console.log(message.structured_output)
    // { company_name: "Anthropic", founded_year: 2021, headquarters: "San Francisco, CA" }
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# Tentukan bentuk data yang ingin Anda dapatkan kembali
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "founded_year": {"type": "number"},
        "headquarters": {"type": "string"}
    },
    "required": ["company_name"]
}

async def main():
    async for message in query(
        prompt="Research Anthropic and provide key company information",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": schema
            }
        )
    ):
        # Pesan hasil berisi structured_output dengan data yang divalidasi
        if isinstance(message, ResultMessage) and message.structured_output:
            print(message.structured_output)
            # {'company_name': 'Anthropic', 'founded_year': 2021, 'headquarters': 'San Francisco, CA'}

asyncio.run(main())
```

</CodeGroup>

## Skema yang aman tipe dengan Zod dan Pydantic

Alih-alih menulis JSON Schema dengan tangan, Anda dapat menggunakan [Zod](https://zod.dev/) (TypeScript) atau [Pydantic](https://docs.pydantic.dev/latest/) (Python) untuk menentukan skema Anda. Perpustakaan ini menghasilkan JSON Schema untuk Anda dan memungkinkan Anda mengurai respons menjadi objek yang sepenuhnya diketik yang dapat Anda gunakan di seluruh basis kode Anda dengan pelengkapan otomatis dan pemeriksaan tipe.

Contoh di bawah ini menentukan skema untuk rencana implementasi fitur dengan ringkasan, daftar langkah (masing-masing dengan tingkat kompleksitas), dan risiko potensial. Agen merencanakan fitur dan mengembalikan objek `FeaturePlan` yang diketik. Anda kemudian dapat mengakses properti seperti `plan.summary` dan mengulangi `plan.steps` dengan keamanan tipe penuh.

<CodeGroup>

```typescript TypeScript
import { z } from 'zod'
import { query } from '@anthropic-ai/claude-agent-sdk'

// Tentukan skema dengan Zod
const FeaturePlan = z.object({
  feature_name: z.string(),
  summary: z.string(),
  steps: z.array(z.object({
    step_number: z.number(),
    description: z.string(),
    estimated_complexity: z.enum(['low', 'medium', 'high'])
  })),
  risks: z.array(z.string())
})

type FeaturePlan = z.infer<typeof FeaturePlan>

// Konversi ke JSON Schema
const schema = z.toJSONSchema(FeaturePlan)

// Gunakan dalam query
for await (const message of query({
  prompt: 'Plan how to add dark mode support to a React app. Break it into implementation steps.',
  options: {
    outputFormat: {
      type: 'json_schema',
      schema: schema
    }
  }
})) {
  if (message.type === 'result' && message.structured_output) {
    // Validasi dan dapatkan hasil yang sepenuhnya diketik
    const parsed = FeaturePlan.safeParse(message.structured_output)
    if (parsed.success) {
      const plan: FeaturePlan = parsed.data
      console.log(`Feature: ${plan.feature_name}`)
      console.log(`Summary: ${plan.summary}`)
      plan.steps.forEach(step => {
        console.log(`${step.step_number}. [${step.estimated_complexity}] ${step.description}`)
      })
    }
  }
}
```

```python Python
import asyncio
from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

class Step(BaseModel):
    step_number: int
    description: str
    estimated_complexity: str  # 'low', 'medium', 'high'

class FeaturePlan(BaseModel):
    feature_name: str
    summary: str
    steps: list[Step]
    risks: list[str]

async def main():
    async for message in query(
        prompt="Plan how to add dark mode support to a React app. Break it into implementation steps.",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": FeaturePlan.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            # Validasi dan dapatkan hasil yang sepenuhnya diketik
            plan = FeaturePlan.model_validate(message.structured_output)
            print(f"Feature: {plan.feature_name}")
            print(f"Summary: {plan.summary}")
            for step in plan.steps:
                print(f"{step.step_number}. [{step.estimated_complexity}] {step.description}")

asyncio.run(main())
```

</CodeGroup>

**Manfaat:**
- Inferensi tipe penuh (TypeScript) dan petunjuk tipe (Python)
- Validasi runtime dengan `safeParse()` atau `model_validate()`
- Pesan kesalahan yang lebih baik
- Skema yang dapat dikomposisi dan dapat digunakan kembali

## Konfigurasi format output

Opsi `outputFormat` (TypeScript) atau `output_format` (Python) menerima objek dengan:

- `type`: Atur ke `"json_schema"` untuk output terstruktur
- `schema`: Objek [JSON Schema](https://json-schema.org/understanding-json-schema/about) yang menentukan struktur output Anda. Anda dapat menghasilkan ini dari skema Zod dengan `z.toJSONSchema()` atau model Pydantic dengan `.model_json_schema()`

SDK mendukung fitur JSON Schema standar termasuk semua tipe dasar (object, array, string, number, boolean, null), `enum`, `const`, `required`, objek bersarang, dan definisi `$ref`. Untuk daftar lengkap fitur yang didukung dan batasan, lihat [Batasan JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations).

## Contoh: agen pelacakan TODO

Contoh ini menunjukkan bagaimana output terstruktur bekerja dengan penggunaan alat multi-langkah. Agen perlu menemukan komentar TODO dalam basis kode, kemudian mencari informasi git blame untuk masing-masing. Agen secara otonom memutuskan alat mana yang akan digunakan (Grep untuk mencari, Bash untuk menjalankan perintah git) dan menggabungkan hasil menjadi respons terstruktur tunggal.

Skema mencakup bidang opsional (`author` dan `date`) karena informasi git blame mungkin tidak tersedia untuk semua file. Agen mengisi apa yang dapat ditemukannya dan menghilangkan sisanya.

<CodeGroup>

```typescript TypeScript
import { query } from '@anthropic-ai/claude-agent-sdk'

// Tentukan struktur untuk ekstraksi TODO
const todoSchema = {
  type: 'object',
  properties: {
    todos: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          text: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'number' },
          author: { type: 'string' },
          date: { type: 'string' }
        },
        required: ['text', 'file', 'line']
      }
    },
    total_count: { type: 'number' }
  },
  required: ['todos', 'total_count']
}

// Agen menggunakan Grep untuk menemukan TODO, Bash untuk mendapatkan informasi git blame
for await (const message of query({
  prompt: 'Find all TODO comments in this codebase and identify who added them',
  options: {
    outputFormat: {
      type: 'json_schema',
      schema: todoSchema
    }
  }
})) {
  if (message.type === 'result' && message.structured_output) {
    const data = message.structured_output
    console.log(`Found ${data.total_count} TODOs`)
    data.todos.forEach(todo => {
      console.log(`${todo.file}:${todo.line} - ${todo.text}`)
      if (todo.author) {
        console.log(`  Added by ${todo.author} on ${todo.date}`)
      }
    })
  }
}
```

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# Tentukan struktur untuk ekstraksi TODO
todo_schema = {
    "type": "object",
    "properties": {
        "todos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "number"},
                    "author": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": ["text", "file", "line"]
            }
        },
        "total_count": {"type": "number"}
    },
    "required": ["todos", "total_count"]
}

async def main():
    # Agen menggunakan Grep untuk menemukan TODO, Bash untuk mendapatkan informasi git blame
    async for message in query(
        prompt="Find all TODO comments in this codebase and identify who added them",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": todo_schema
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            data = message.structured_output
            print(f"Found {data['total_count']} TODOs")
            for todo in data['todos']:
                print(f"{todo['file']}:{todo['line']} - {todo['text']}")
                if 'author' in todo:
                    print(f"  Added by {todo['author']} on {todo['date']}")

asyncio.run(main())
```

</CodeGroup>

## Penanganan kesalahan

Pembuatan output terstruktur dapat gagal ketika agen tidak dapat menghasilkan JSON yang valid sesuai dengan skema Anda. Ini biasanya terjadi ketika skema terlalu kompleks untuk tugas, tugas itu sendiri ambigu, atau agen mencapai batas percobaan ulangnya mencoba memperbaiki kesalahan validasi.

Ketika kesalahan terjadi, pesan hasil memiliki `subtype` yang menunjukkan apa yang salah:

| Subtype | Arti |
|---------|---------|
| `success` | Output dihasilkan dan divalidasi dengan berhasil |
| `error_max_structured_output_retries` | Agen tidak dapat menghasilkan output yang valid setelah beberapa upaya |

Contoh di bawah ini memeriksa bidang `subtype` untuk menentukan apakah output dihasilkan dengan berhasil atau jika Anda perlu menangani kegagalan:

<CodeGroup>

```typescript TypeScript
for await (const msg of query({
  prompt: 'Extract contact info from the document',
  options: {
    outputFormat: {
      type: 'json_schema',
      schema: contactSchema
    }
  }
})) {
  if (msg.type === 'result') {
    if (msg.subtype === 'success' && msg.structured_output) {
      // Gunakan output yang divalidasi
      console.log(msg.structured_output)
    } else if (msg.subtype === 'error_max_structured_output_retries') {
      // Tangani kegagalan - coba lagi dengan prompt yang lebih sederhana, kembali ke yang tidak terstruktur, dll.
      console.error('Could not produce valid output')
    }
  }
}
```

```python Python
async for message in query(
    prompt="Extract contact info from the document",
    options=ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "schema": contact_schema
        }
    )
):
    if isinstance(message, ResultMessage):
        if message.subtype == "success" and message.structured_output:
            # Gunakan output yang divalidasi
            print(message.structured_output)
        elif message.subtype == "error_max_structured_output_retries":
            # Tangani kegagalan
            print("Could not produce valid output")
```

</CodeGroup>

**Tips untuk menghindari kesalahan:**

- **Jaga skema tetap fokus.** Skema yang bersarang dalam dengan banyak bidang yang diperlukan lebih sulit untuk dipenuhi. Mulai sederhana dan tambahkan kompleksitas sesuai kebutuhan.
- **Cocokkan skema dengan tugas.** Jika tugas mungkin tidak memiliki semua informasi yang diperlukan skema Anda, buat bidang tersebut opsional.
- **Gunakan prompt yang jelas.** Prompt yang ambigu membuat lebih sulit bagi agen untuk mengetahui output apa yang harus diproduksi.

## Sumber daya terkait

- [Dokumentasi JSON Schema](https://json-schema.org/): pelajari sintaks JSON Schema untuk menentukan skema kompleks dengan objek bersarang, array, enum, dan batasan validasi
- [API Structured Outputs](/docs/id/build-with-claude/structured-outputs): gunakan output terstruktur dengan Claude API secara langsung untuk permintaan satu putaran tanpa penggunaan alat
- [Alat kustom](/docs/id/agent-sdk/custom-tools): berikan agen Anda alat kustom untuk dipanggil selama eksekusi sebelum mengembalikan output terstruktur