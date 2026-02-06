---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 12c99186b4b4c89b01653470b1eb75514ffab2462d67ca14a3225ab9262ae52b
---

# Output terstruktur

Dapatkan hasil JSON yang divalidasi dari alur kerja agen

---

Output terstruktur membatasi respons Claude untuk mengikuti skema tertentu, memastikan output yang valid dan dapat diurai untuk pemrosesan hilir. Dua fitur yang saling melengkapi tersedia:

- **Output JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu
- **Penggunaan alat ketat** (`strict: true`): Jamin validasi skema pada nama alat dan input

<Warning>
Parameter `output_format` telah dipindahkan ke `output_config.format`. Parameter `output_format` lama masih berfungsi sementara tetapi sudah usang dan akan dihapus dalam versi API mendatang. Perbarui kode Anda untuk menggunakan `output_config: {format: {...}}` sebagai gantinya.
</Warning>

Fitur-fitur ini dapat digunakan secara independen atau bersama-sama dalam permintaan yang sama.

<Note>
Output terstruktur tersedia secara umum di Claude API dan Amazon Bedrock untuk Claude Opus 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Output terstruktur tetap dalam beta publik di Microsoft Foundry.
</Note>

<Tip>
**Bermigrasi dari beta?** Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Header beta lama (`structured-outputs-2025-11-13`) dan parameter `output_format` akan terus berfungsi selama periode transisi. Lihat contoh kode di bawah untuk bentuk API yang diperbarui.
</Tip>

## Mengapa menggunakan output terstruktur

Tanpa output terstruktur, Claude dapat menghasilkan respons JSON yang tidak terbentuk dengan baik atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompt yang hati-hati, Anda mungkin mengalami:
- Kesalahan penguraian dari sintaks JSON yang tidak valid
- Bidang yang diperlukan hilang
- Tipe data yang tidak konsisten
- Pelanggaran skema yang memerlukan penanganan kesalahan dan percobaan ulang

Output terstruktur menjamin respons yang sesuai dengan skema melalui decoding terbatas:
- **Selalu valid**: Tidak ada lagi kesalahan `JSON.parse()`
- **Aman tipe**: Tipe bidang dan bidang yang diperlukan dijamin
- **Andal**: Tidak perlu percobaan ulang untuk pelanggaran skema

## Output JSON

Output JSON mengontrol format respons Claude, memastikan Claude mengembalikan JSON yang valid sesuai dengan skema Anda. Gunakan output JSON ketika Anda perlu:

- Mengontrol format respons Claude
- Mengekstrak data dari gambar atau teks
- Menghasilkan laporan terstruktur
- Format respons API

### Mulai cepat

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }
    ],
    "output_config": {
      "format": {
        "type": "json_schema",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "plan_interest": {"type": "string"},
            "demo_requested": {"type": "boolean"}
          },
          "required": ["name", "email", "plan_interest", "demo_requested"],
          "additionalProperties": false
        }
      }
    }
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
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
        }
    ],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan_interest": {"type": "string"},
                    "demo_requested": {"type": "boolean"}
                },
                "required": ["name", "email", "plan_interest", "demo_requested"],
                "additionalProperties": False
            }
        }
    }
)
print(response.content[0].text)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }
  ],
  output_config: {
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          name: { type: "string" },
          email: { type: "string" },
          plan_interest: { type: "string" },
          demo_requested: { type: "boolean" }
        },
        required: ["name", "email", "plan_interest", "demo_requested"],
        additionalProperties: false
      }
    }
  }
});
console.log(response.content[0].text);
```

</CodeGroup>

**Format respons:** JSON yang valid sesuai dengan skema Anda di `response.content[0].text`

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "plan_interest": "Enterprise",
  "demo_requested": true
}
```

### Cara kerjanya

<Steps>
  <Step title="Tentukan skema JSON Anda">
    Buat skema JSON yang mendeskripsikan struktur yang ingin Anda ikuti oleh Claude. Skema menggunakan format JSON Schema standar dengan beberapa batasan (lihat [batasan JSON Schema](#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan parameter output_config.format">
    Sertakan parameter `output_config.format` dalam permintaan API Anda dengan `type: "json_schema"` dan definisi skema Anda.
  </Step>
  <Step title="Urai respons">
    Respons Claude akan berupa JSON yang valid sesuai dengan skema Anda, dikembalikan di `response.content[0].text`.
  </Step>
</Steps>

### Bekerja dengan output JSON di SDK

SDK Python dan TypeScript menyediakan pembantu yang memudahkan pekerjaan dengan output JSON, termasuk transformasi skema, validasi otomatis, dan integrasi dengan perpustakaan skema populer.

<Note>
Metode pembantu SDK (seperti `.parse()` dan integrasi Pydantic/Zod) masih menerima `output_format` sebagai parameter kenyamanan. SDK menangani terjemahan ke `output_config.format` secara internal. Contoh di bawah menunjukkan sintaks pembantu SDK.
</Note>

#### Menggunakan Pydantic dan Zod

Untuk pengembang Python dan TypeScript, Anda dapat menggunakan alat definisi skema yang familiar seperti Pydantic dan Zod alih-alih menulis skema JSON mentah.

<CodeGroup>

```python Python
from pydantic import BaseModel
from anthropic import Anthropic, transform_schema

class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool

client = Anthropic()

# With .create() - requires transform_schema()
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
        }
    ],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": transform_schema(ContactInfo),
        }
    }
)

print(response.content[0].text)

# With .parse() - can pass Pydantic model directly
response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
        }
    ],
    output_format=ContactInfo,
)

print(response.parsed_output)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';

const ContactInfoSchema = z.object({
  name: z.string(),
  email: z.string(),
  plan_interest: z.string(),
  demo_requested: z.boolean(),
});

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }
  ],
  output_config: { format: zodOutputFormat(ContactInfoSchema) },
});

// Automatically parsed and validated
console.log(response.content[0].text);
```

</CodeGroup>

#### Metode khusus SDK

**Python: `client.messages.parse()` (Direkomendasikan)**

Metode `parse()` secara otomatis mengubah model Pydantic Anda, memvalidasi respons, dan mengembalikan atribut `parsed_output`.

<section title="Contoh penggunaan">

```python
from pydantic import BaseModel
import anthropic

class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str

client = anthropic.Anthropic()

response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    output_format=ContactInfo,
)

# Access the parsed output directly
contact = response.parsed_output
print(contact.name, contact.email)
```

</section>

**Python: pembantu `transform_schema()`**

Untuk ketika Anda perlu secara manual mengubah skema sebelum mengirim, atau ketika Anda ingin memodifikasi skema yang dihasilkan Pydantic. Tidak seperti `client.messages.parse()`, yang secara otomatis mengubah skema yang disediakan, ini memberi Anda skema yang diubah sehingga Anda dapat menyesuaikannya lebih lanjut.

<section title="Contoh penggunaan">

```python
from anthropic import transform_schema
from pydantic import TypeAdapter

# First convert Pydantic model to JSON schema, then transform
schema = TypeAdapter(ContactInfo).json_schema()
schema = transform_schema(schema)
# Modify schema if needed
schema["properties"]["custom_field"] = {"type": "string"}

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    output_config={
        "format": {"type": "json_schema", "schema": schema},
    },
)
```

</section>

#### Cara kerja transformasi SDK

SDK Python dan TypeScript secara otomatis mengubah skema dengan fitur yang tidak didukung:

1. **Hapus batasan yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Perbarui deskripsi** dengan informasi batasan (misalnya, "Harus setidaknya 100"), ketika batasan tidak langsung didukung dengan output terstruktur
3. **Tambahkan `additionalProperties: false`** ke semua objek
4. **Filter format string** ke daftar yang didukung saja
5. **Validasi respons** terhadap skema asli Anda (dengan semua batasan)

Ini berarti Claude menerima skema yang disederhanakan, tetapi kode Anda masih memberlakukan semua batasan melalui validasi.

**Contoh:** Bidang Pydantic dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, tetapi deskripsi diperbarui menjadi "Harus setidaknya 100", dan SDK memvalidasi respons terhadap batasan asli.

### Kasus penggunaan umum

<section title="Ekstraksi data">

Ekstrak data terstruktur dari teks tidak terstruktur:

<CodeGroup>

```python Python
from pydantic import BaseModel
from typing import List

class Invoice(BaseModel):
    invoice_number: str
    date: str
    total_amount: float
    line_items: List[dict]
    customer_name: str

response = client.messages.parse(
    model="claude-opus-4-6",
    output_format=Invoice,
    messages=[{"role": "user", "content": f"Extract invoice data from: {invoice_text}"}]
)
```

```typescript TypeScript
import { z } from 'zod';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';

const InvoiceSchema = z.object({
  invoice_number: z.string(),
  date: z.string(),
  total_amount: z.number(),
  line_items: z.array(z.record(z.string(), z.any())),
  customer_name: z.string(),
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(InvoiceSchema) },
  messages: [{"role": "user", "content": `Extract invoice data from: ${invoiceText}`}]
});
```

</CodeGroup>

</section>

<section title="Klasifikasi">

Klasifikasikan konten dengan kategori terstruktur:

<CodeGroup>

```python Python
from pydantic import BaseModel
from typing import List

class Classification(BaseModel):
    category: str
    confidence: float
    tags: List[str]
    sentiment: str

response = client.messages.parse(
    model="claude-opus-4-6",
    output_format=Classification,
    messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}]
)
```

```typescript TypeScript
import { z } from 'zod';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';

const ClassificationSchema = z.object({
  category: z.string(),
  confidence: z.number(),
  tags: z.array(z.string()),
  sentiment: z.string(),
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(ClassificationSchema) },
  messages: [{"role": "user", "content": `Classify this feedback: ${feedbackText}`}]
});
```

</CodeGroup>

</section>

<section title="Pemformatan respons API">

Hasilkan respons yang siap API:

<CodeGroup>

```python Python
from pydantic import BaseModel
from typing import List, Optional

class APIResponse(BaseModel):
    status: str
    data: dict
    errors: Optional[List[dict]]
    metadata: dict

response = client.messages.parse(
    model="claude-opus-4-6",
    output_format=APIResponse,
    messages=[{"role": "user", "content": "Process this request: ..."}]
)
```

```typescript TypeScript
import { z } from 'zod';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';

const APIResponseSchema = z.object({
  status: z.string(),
  data: z.record(z.string(), z.any()),
  errors: z.array(z.record(z.string(), z.any())).optional(),
  metadata: z.record(z.string(), z.any()),
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(APIResponseSchema) },
  messages: [{"role": "user", "content": "Process this request: ..."}]
});
```

</CodeGroup>

</section>

## Penggunaan alat ketat

Penggunaan alat ketat memvalidasi parameter alat, memastikan Claude memanggil fungsi Anda dengan argumen yang diketik dengan benar. Gunakan penggunaan alat ketat ketika Anda perlu:

- Memvalidasi parameter alat
- Membangun alur kerja agen
- Memastikan panggilan fungsi yang aman tipe
- Menangani alat kompleks dengan properti bersarang

### Mengapa penggunaan alat ketat penting untuk agen

Membangun sistem agen yang andal memerlukan kepatuhan skema yang dijamin. Tanpa mode ketat, Claude mungkin mengembalikan tipe yang tidak kompatibel (`"2"` alih-alih `2`) atau bidang yang diperlukan hilang, merusak fungsi Anda dan menyebabkan kesalahan runtime.

Penggunaan alat ketat menjamin parameter yang aman tipe:
- Fungsi menerima argumen yang diketik dengan benar setiap saat
- Tidak perlu memvalidasi dan mencoba ulang panggilan alat
- Agen siap produksi yang bekerja secara konsisten dalam skala besar

Misalnya, anggaplah sistem pemesanan memerlukan `passengers: int`. Tanpa mode ketat, Claude mungkin memberikan `passengers: "two"` atau `passengers: "2"`. Dengan `strict: true`, respons akan selalu berisi `passengers: 2`.

### Mulai cepat

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is the weather in San Francisco?"}
    ],
    "tools": [{
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "strict": true,
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"],
        "additionalProperties": false
      }
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
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "strict": True,  # Enable strict mode
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    ]
)
print(response.content)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "What's the weather like in San Francisco?"
    }
  ],
  tools: [{
    name: "get_weather",
    description: "Get the current weather in a given location",
    strict: true,  // Enable strict mode
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        },
        unit: {
          type: "string",
          enum: ["celsius", "fahrenheit"]
        }
      },
      required: ["location"],
      additionalProperties: false
    }
  }]
});
console.log(response.content);
```

</CodeGroup>

**Format respons:** Blok penggunaan alat dengan input yang divalidasi di `response.content[x].input`

```json
{
  "type": "tool_use",
  "name": "get_weather",
  "input": {
    "location": "San Francisco, CA"
  }
}
```

**Jaminan:**
- Input alat `input` ketat mengikuti `input_schema`
- Nama alat `name` selalu valid (dari alat yang disediakan atau alat server)

### Cara kerjanya

<Steps>
  <Step title="Tentukan skema alat Anda">
    Buat skema JSON untuk `input_schema` alat Anda. Skema menggunakan format JSON Schema standar dengan beberapa batasan (lihat [batasan JSON Schema](#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan strict: true">
    Atur `"strict": true` sebagai properti tingkat atas dalam definisi alat Anda, bersama dengan `name`, `description`, dan `input_schema`.
  </Step>
  <Step title="Tangani panggilan alat">
    Ketika Claude menggunakan alat, bidang `input` dalam blok tool_use akan ketat mengikuti `input_schema` Anda, dan `name` akan selalu valid.
  </Step>
</Steps>

### Kasus penggunaan umum

<section title="Input alat yang divalidasi">

Pastikan parameter alat persis sesuai dengan skema Anda:

<CodeGroup>

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Search for flights to Tokyo"}],
    tools=[{
        "name": "search_flights",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "departure_date": {"type": "string", "format": "date"},
                "passengers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
            },
            "required": ["destination", "departure_date"],
            "additionalProperties": False
        }
    }]
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  messages: [{"role": "user", "content": "Search for flights to Tokyo"}],
  tools: [{
    name: "search_flights",
    strict: true,
    input_schema: {
      type: "object",
      properties: {
        destination: {type: "string"},
        departure_date: {type: "string", format: "date"},
        passengers: {type: "integer", enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
      },
      required: ["destination", "departure_date"],
      additionalProperties: false
    }
  }]
});
```

</CodeGroup>

</section>

<section title="Alur kerja agen dengan beberapa alat yang divalidasi">

Bangun agen multi-langkah yang andal dengan parameter alat yang dijamin:

<CodeGroup>

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Help me plan a trip to Paris for 2 people"}],
    tools=[
        {
            "name": "search_flights",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string", "format": "date"},
                    "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]}
                },
                "required": ["origin", "destination", "departure_date"],
                "additionalProperties": False
            }
        },
        {
            "name": "search_hotels",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "check_in": {"type": "string", "format": "date"},
                    "guests": {"type": "integer", "enum": [1, 2, 3, 4]}
                },
                "required": ["city", "check_in"],
                "additionalProperties": False
            }
        }
    ]
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  messages: [{"role": "user", "content": "Help me plan a trip to Paris for 2 people"}],
  tools: [
    {
      name: "search_flights",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          origin: {type: "string"},
          destination: {type: "string"},
          departure_date: {type: "string", format: "date"},
          travelers: {type: "integer", enum: [1, 2, 3, 4, 5, 6]}
        },
        required: ["origin", "destination", "departure_date"],
        additionalProperties: false
      }
    },
    {
      name: "search_hotels",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          city: {type: "string"},
          check_in: {type: "string", format: "date"},
          guests: {type: "integer", enum: [1, 2, 3, 4]}
        },
        required: ["city", "check_in"],
        additionalProperties: false
      }
    }
  ]
});
```

</CodeGroup>

</section>

## Menggunakan kedua fitur bersama-sama

Output JSON dan penggunaan alat ketat menyelesaikan masalah yang berbeda dan dapat digunakan bersama-sama:

- **Output JSON** mengontrol format respons Claude (apa yang Claude katakan)
- **Penggunaan alat ketat** memvalidasi parameter alat (bagaimana Claude memanggil fungsi Anda)

Ketika digabungkan, Claude dapat memanggil alat dengan parameter yang dijamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agen di mana Anda memerlukan panggilan alat yang andal dan output akhir yang terstruktur.

<CodeGroup>

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Help me plan a trip to Paris for next month"}],
    # JSON outputs: structured response format
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "next_steps": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["summary", "next_steps"],
                "additionalProperties": False
            }
        }
    },
    # Strict tool use: guaranteed tool parameters
    tools=[{
        "name": "search_flights",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "date": {"type": "string", "format": "date"}
            },
            "required": ["destination", "date"],
            "additionalProperties": False
        }
    }]
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Help me plan a trip to Paris for next month" }],
  // JSON outputs: structured response format
  output_config: {
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          summary: { type: "string" },
          next_steps: { type: "array", items: { type: "string" } }
        },
        required: ["summary", "next_steps"],
        additionalProperties: false
      }
    }
  },
  // Strict tool use: guaranteed tool parameters
  tools: [{
    name: "search_flights",
    strict: true,
    input_schema: {
      type: "object",
      properties: {
        destination: { type: "string" },
        date: { type: "string", format: "date" }
      },
      required: ["destination", "date"],
      additionalProperties: false
    }
  }]
});
```

</CodeGroup>

## Pertimbangan penting

### Kompilasi tata bahasa dan caching

Output terstruktur menggunakan sampling terbatas dengan artefak tata bahasa yang dikompilasi. Ini memperkenalkan beberapa karakteristik kinerja yang perlu diperhatikan:

- **Latensi permintaan pertama**: Pertama kali Anda menggunakan skema tertentu, akan ada latensi tambahan saat tata bahasa dikompilasi
- **Caching otomatis**: Tata bahasa yang dikompilasi di-cache selama 24 jam dari penggunaan terakhir, membuat permintaan berikutnya jauh lebih cepat
- **Invalidasi cache**: Cache dibatalkan jika Anda mengubah:
  - Struktur skema JSON
  - Set alat dalam permintaan Anda (saat menggunakan output terstruktur dan penggunaan alat bersama-sama)
  - Mengubah hanya bidang `name` atau `description` tidak membatalkan cache

### Modifikasi prompt dan biaya token

Saat menggunakan output terstruktur, Claude secara otomatis menerima prompt sistem tambahan yang menjelaskan format output yang diharapkan. Ini berarti:

- Jumlah token input Anda akan sedikit lebih tinggi
- Prompt yang disuntikkan menghabiskan token Anda seperti prompt sistem lainnya
- Mengubah parameter `output_config.format` akan membatalkan [cache prompt](/docs/id/build-with-claude/prompt-caching) apa pun untuk utas percakapan itu

### Batasan JSON Schema

Output terstruktur mendukung JSON Schema standar dengan beberapa batasan. Baik output JSON maupun penggunaan alat ketat berbagi batasan ini.

<section title="Fitur yang didukung">

- Semua tipe dasar: object, array, string, integer, number, boolean, null
- `enum` (string, angka, bool, atau null saja - tidak ada tipe kompleks)
- `const`
- `anyOf` dan `allOf` (dengan batasan - `allOf` dengan `$ref` tidak didukung)
- `$ref`, `$def`, dan `definitions` (eksternal `$ref` tidak didukung)
- Properti `default` untuk semua tipe yang didukung
- `required` dan `additionalProperties` (harus diatur ke `false` untuk objek)
- Format string: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
- Array `minItems` (hanya nilai 0 dan 1 yang didukung)

</section>

<section title="Tidak didukung">

- Skema rekursif
- Tipe kompleks dalam enum
- `$ref` eksternal (misalnya, `'$ref': 'http://...'`)
- Batasan numerik (`minimum`, `maximum`, `multipleOf`, dll.)
- Batasan string (`minLength`, `maxLength`)
- Batasan array di luar `minItems` dari 0 atau 1
- `additionalProperties` diatur ke apa pun selain `false`

Jika Anda menggunakan fitur yang tidak didukung, Anda akan menerima kesalahan 400 dengan detail.

</section>

<section title="Dukungan pola (regex)">

**Fitur regex yang didukung:**
- Pencocokan penuh (`^...$`) dan pencocokan sebagian
- Quantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
- Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
- Grup: `(...)`

**TIDAK didukung:**
- Backreferences ke grup (misalnya, `\1`, `\2`)
- Asersi lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
- Batas kata: `\b`, `\B`
- Quantifier `{n,m}` kompleks dengan rentang besar

Pola regex sederhana bekerja dengan baik. Pola kompleks mungkin menghasilkan kesalahan 400.

</section>

<Tip>
SDK Python dan TypeScript dapat secara otomatis mengubah skema dengan fitur yang tidak didukung dengan menghapusnya dan menambahkan batasan ke deskripsi bidang. Lihat [metode khusus SDK](#sdk-specific-methods) untuk detail.
</Tip>

### Output yang tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam kebanyakan kasus, ada skenario di mana output mungkin tidak sesuai dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan properti keselamatan dan kegunaannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keselamatan:

- Respons akan memiliki `stop_reason: "refusal"`
- Anda akan menerima kode status 200
- Anda akan ditagih untuk token yang dihasilkan
- Output mungkin tidak sesuai dengan skema Anda karena pesan penolakan mengambil alih batasan skema

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons dipotong karena mencapai batas `max_tokens`:

- Respons akan memiliki `stop_reason: "max_tokens"`
- Output mungkin tidak lengkap dan tidak sesuai dengan skema Anda
- Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap

### Kesalahan validasi skema

Jika skema Anda menggunakan fitur yang tidak didukung atau terlalu kompleks, Anda akan menerima kesalahan 400:

**"Terlalu banyak definisi rekursif dalam skema"**
- Penyebab: Skema memiliki definisi rekursif yang berlebihan atau siklik
- Solusi: Sederhanakan struktur skema, kurangi kedalaman nesting

**"Skema terlalu kompleks"**
- Penyebab: Skema melebihi batas kompleksitas
- Solusi: Pecah menjadi skema yang lebih kecil, sederhanakan struktur, atau kurangi jumlah alat yang ditandai sebagai `strict: true`

Untuk masalah persisten dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan definisi skema Anda.

## Kompatibilitas fitur

**Bekerja dengan:**
- **[Pemrosesan batch](/docs/id/build-with-claude/batch-processing)**: Proses output terstruktur dalam skala besar dengan diskon 50%
- **[Penghitungan token](/docs/id/build-with-claude/token-counting)**: Hitung token tanpa kompilasi
- **[Streaming](/docs/id/build-with-claude/streaming)**: Stream output terstruktur seperti respons normal
- **Penggunaan gabungan**: Gunakan output JSON (`output_config.format`) dan penggunaan alat ketat (`strict: true`) bersama-sama dalam permintaan yang sama

**Tidak kompatibel dengan:**
- **[Kutipan](/docs/id/build-with-claude/citations)**: Kutipan memerlukan interleaving blok kutipan dengan teks, yang bertentangan dengan batasan skema JSON ketat. Mengembalikan kesalahan 400 jika kutipan diaktifkan dengan `output_config.format`.
- **Prefilling Pesan**: Tidak kompatibel dengan output JSON

<Tip>
**Cakupan tata bahasa**: Tata bahasa hanya berlaku untuk output langsung Claude, bukan untuk panggilan penggunaan alat, hasil alat, atau tag pemikiran (saat menggunakan [Extended Thinking](/docs/id/build-with-claude/extended-thinking)). Status tata bahasa direset antar bagian, memungkinkan Claude berpikir bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>