---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: 22a77fe692f4c377fbc3df4e0c93b316ebbe39a01168b324b2b54d7267851626
---

# Output terstruktur

Dapatkan hasil JSON yang tervalidasi dari alur kerja agen

---

Output terstruktur membatasi respons Claude agar mengikuti skema tertentu, memastikan output yang valid dan dapat diurai untuk pemrosesan hilir. Dua fitur pelengkap tersedia:

- **Output JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu
- **Penggunaan alat ketat** (`strict: true`): Jaminan validasi skema pada nama alat dan input

Fitur-fitur ini dapat digunakan secara independen atau bersama-sama dalam permintaan yang sama.

<Note>
Output terstruktur umumnya tersedia di Claude API dan Amazon Bedrock untuk Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Output terstruktur tetap dalam beta publik di Microsoft Foundry.
</Note>

<Note>
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Tip>
**Bermigrasi dari beta?** Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Header beta lama (`structured-outputs-2025-11-13`) dan parameter `output_format` akan terus berfungsi selama periode transisi. Lihat contoh kode di bawah untuk bentuk API yang diperbarui.
</Tip>

## Mengapa menggunakan output terstruktur

Tanpa output terstruktur, Claude dapat menghasilkan respons JSON yang tidak valid atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompt yang cermat, Anda mungkin mengalami:
- Kesalahan penguraian dari sintaks JSON yang tidak valid
- Bidang yang diperlukan hilang
- Tipe data yang tidak konsisten
- Pelanggaran skema yang memerlukan penanganan kesalahan dan percobaan ulang

Output terstruktur menjamin respons yang sesuai skema melalui decoding terbatas:
- **Selalu valid**: Tidak ada lagi kesalahan `JSON.parse()`
- **Aman tipe**: Tipe bidang dan bidang yang diperlukan terjamin
- **Andal**: Tidak perlu percobaan ulang untuk pelanggaran skema

## Output JSON

Output JSON mengontrol format respons Claude, memastikan Claude mengembalikan JSON valid yang sesuai dengan skema Anda. Gunakan output JSON ketika Anda perlu:

- Mengontrol format respons Claude
- Mengekstrak data dari gambar atau teks
- Menghasilkan laporan terstruktur
- Memformat respons API

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
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
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
                    "demo_requested": {"type": "boolean"},
                },
                "required": ["name", "email", "plan_interest", "demo_requested"],
                "additionalProperties": False,
            },
        }
    },
)
print(response.content[0].text)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content:
        "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
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

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.*;

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

// Java SDK uses class-based structured outputs
// See the Java SDK page for annotation-based approach
MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_6)
    .maxTokens(1024)
    .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.")
    .build();

Message message = client.beta().messages().create(params);
System.out.println(message.content());
```

```go Go
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, _ := client.Messages.New(context.Background(),
		anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_6,
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{
				anthropic.NewUserMessage(
					anthropic.NewTextBlock("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."),
				),
			},
			OutputConfig: anthropic.OutputConfigParam{
				Format: anthropic.JSONOutputFormatParam{
					Schema: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"name":           map[string]string{"type": "string"},
							"email":          map[string]string{"type": "string"},
							"plan_interest":  map[string]string{"type": "string"},
							"demo_requested": map[string]string{"type": "boolean"},
						},
						"required":             []string{"name", "email", "plan_interest", "demo_requested"},
						"additionalProperties": false,
					},
				},
			},
		})

	fmt.Println(response.Content[0].Text)
}
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
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
)

puts response.content[0].text
```

```csharp C#
using Anthropic;

var client = new AnthropicClient();

var response = await client.Messages.CreateAsync(
    new MessageCreateParams
    {
        Model = "claude-opus-4-6",
        MaxTokens = 1024,
        Messages = new[]
        {
            new MessageParam
            {
                Role = "user",
                Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
            }
        },
        OutputConfig = new OutputConfig
        {
            Format = new JsonOutputFormat
            {
                Type = "json_schema",
                Schema = new
                {
                    type = "object",
                    properties = new
                    {
                        name = new { type = "string" },
                        email = new { type = "string" },
                        plan_interest = new { type = "string" },
                        demo_requested = new { type = "boolean" }
                    },
                    required = new[] { "name", "email", "plan_interest", "demo_requested" },
                    additionalProperties = false
                }
            }
        }
    });

Console.WriteLine(response.Content[0].Text);
```

```php PHP
<?php

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("ANTHROPIC_API_KEY")
);

$response = $client->beta->messages->create([
    'model' => 'claude-opus-4-6',
    'max_tokens' => 1024,
    'betas' => ['structured-outputs-2025-11-13'],
    'messages' => [
        [
            'role' => 'user',
            'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'
        ]
    ],
    'output_format' => [
        'type' => 'json_schema',
        'schema' => [
            'type' => 'object',
            'properties' => [
                'name' => ['type' => 'string'],
                'email' => ['type' => 'string'],
                'plan_interest' => ['type' => 'string'],
                'demo_requested' => ['type' => 'boolean']
            ],
            'required' => ['name', 'email', 'plan_interest', 'demo_requested'],
            'additionalProperties' => false
        ]
    ]
]);

echo $response->content[0]->text;
```

</CodeGroup>

**Format respons:** JSON valid yang sesuai dengan skema Anda di `response.content[0].text`

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
    Buat skema JSON yang mendeskripsikan struktur yang ingin Anda ikuti oleh Claude. Skema menggunakan format JSON Schema standar dengan beberapa batasan (lihat [Batasan JSON Schema](#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan parameter output_config.format">
    Sertakan parameter `output_config.format` dalam permintaan API Anda dengan `type: "json_schema"` dan definisi skema Anda.
  </Step>
  <Step title="Urai respons">
    Respons Claude akan berupa JSON valid yang sesuai dengan skema Anda, dikembalikan dalam `response.content[0].text`.
  </Step>
</Steps>

### Bekerja dengan output JSON di SDK

SDK menyediakan helper yang memudahkan pengerjaan output JSON, termasuk transformasi skema, validasi otomatis, dan integrasi dengan library skema populer.

<Note>
Metode helper SDK (seperti `.parse()` dan integrasi Pydantic/Zod) masih menerima `output_format` sebagai parameter kenyamanan. SDK menangani terjemahan ke `output_config.format` secara internal. Contoh di bawah ini menunjukkan sintaks helper SDK.
</Note>

#### Menggunakan definisi skema native

Alih-alih menulis skema JSON mentah, Anda dapat menggunakan alat definisi skema yang familiar dalam bahasa Anda:

- **Python**: Model [Pydantic](https://docs.pydantic.dev/) dengan `client.messages.parse()`
- **TypeScript**: Skema [Zod](https://zod.dev/) dengan `zodOutputFormat()`
- **Java**: Kelas Java biasa dengan derivasi skema otomatis melalui `outputFormat(Class<T>)`
- **Ruby**: Kelas `Anthropic::BaseModel` dengan `output_config: {format: Model}`
- **C#**, **Go**, **PHP**: Skema JSON mentah yang diteruskan melalui `output_config`

<CodeGroup>

```python Python
from pydantic import BaseModel
from anthropic import Anthropic


class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool


client = Anthropic()

response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
        }
    ],
    output_format=ContactInfo,
)

print(response.parsed_output)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const ContactInfoSchema = z.object({
  name: z.string(),
  email: z.string(),
  plan_interest: z.string(),
  demo_requested: z.boolean()
});

const client = new Anthropic();

const response = await client.messages.parse({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content:
        "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }
  ],
  output_config: { format: zodOutputFormat(ContactInfoSchema) }
});

// Guaranteed type-safe
console.log(response.parsed_output.email);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
    public boolean demoRequested;
}

AnthropicClient client = AnthropicOkHttpClient.fromEnv();

StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
  .model(Model.CLAUDE_OPUS_4_6)
  .maxTokens(1024)
  .outputFormat(ContactInfo.class)
  .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.")
  .build();

var response = client.messages().create(createParams);
ContactInfo contact = response.output(ContactInfo.class);
System.out.println(contact.name + " (" + contact.email + ")");
```

```go Go
package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/invopop/jsonschema"
)

type ContactInfo struct {
	Name          string `json:"name" jsonschema:"description=Full name"`
	Email         string `json:"email" jsonschema:"description=Email address"`
	PlanInterest  string `json:"plan_interest" jsonschema:"description=Plan type"`
	DemoRequested bool   `json:"demo_requested" jsonschema:"description=Whether a demo was requested"`
}

func generateSchema(v any) map[string]any {
	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
	s := r.Reflect(v)
	b, _ := json.Marshal(s)
	var m map[string]any
	json.Unmarshal(b, &m)
	return m
}

func main() {
	client := anthropic.NewClient()
	schema := generateSchema(&ContactInfo{})

	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(
				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
			)),
		},
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: schema,
			},
		},
	})

	var contact ContactInfo
	json.Unmarshal([]byte(message.Content[0].AsResponseTextBlock().Text), &contact)
	fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
}
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

class ContactInfo < Anthropic::BaseModel
  required :name, String
  required :email, String
  required :plan_interest, String
  required :demo_requested, Anthropic::Boolean
end

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
  }],
  output_config: {format: ContactInfo}
)

contact = message.parsed_output
puts "#{contact.name} (#{contact.email})"
```

```csharp C#
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-6",
    MaxTokens = 1024,
    Messages = [new() {
        Role = Role.User,
        Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }],
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    name = new { type = "string" },
                    email = new { type = "string" },
                    plan_interest = new { type = "string" },
                    demo_requested = new { type = "boolean" },
                }),
                ["required"] = JsonSerializer.SerializeToElement(
                    new[] { "name", "email", "plan_interest", "demo_requested" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
});

var json = (response.Content.First().Value as TextBlock)!.Text;
// JSON is guaranteed to match the schema
var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(json);
Console.WriteLine($"{contact["name"]} ({contact["email"]})");
```

```php PHP
<?php

use Anthropic\Client;
use Anthropic\Messages\OutputConfig;
use Anthropic\Messages\JSONOutputFormat;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.'],
    ],
    model: 'claude-opus-4-6',
    outputConfig: OutputConfig::with(format: JSONOutputFormat::with(schema: [
        'type' => 'object',
        'properties' => [
            'name' => ['type' => 'string'],
            'email' => ['type' => 'string'],
            'plan_interest' => ['type' => 'string'],
            'demo_requested' => ['type' => 'boolean'],
        ],
        'required' => ['name', 'email', 'plan_interest', 'demo_requested'],
        'additionalProperties' => false,
    ])),
);

$data = json_decode($response->content[0]->text, true);
echo $data['name'] . ' (' . $data['email'] . ')';
```

</CodeGroup>

#### Metode khusus SDK

Setiap SDK menyediakan helper yang memudahkan pengerjaan structured outputs. Lihat halaman SDK individual untuk detail lengkap.

<Tabs>
<Tab title="Python">

**`client.messages.parse()` (Direkomendasikan)**

Metode `parse()` secara otomatis mentransformasi model Pydantic Anda, memvalidasi respons, dan mengembalikan atribut `parsed_output`.

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

**Helper `transform_schema()`**

Untuk saat Anda perlu mentransformasi skema secara manual sebelum mengirim, atau saat Anda ingin memodifikasi skema yang dihasilkan Pydantic. Tidak seperti `client.messages.parse()`, yang mentransformasi skema yang diberikan secara otomatis, ini memberi Anda skema yang telah ditransformasi sehingga Anda dapat menyesuaikannya lebih lanjut.

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

</Tab>
<Tab title="TypeScript">

**`client.messages.parse()` dengan `zodOutputFormat()`**

Metode `parse()` menerima skema Zod, memvalidasi respons, dan mengembalikan atribut `parsed_output` dengan tipe TypeScript yang disimpulkan sesuai skema.

<section title="Contoh penggunaan">

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const ContactInfo = z.object({
  name: z.string(),
  email: z.string(),
  planInterest: z.string()
});

const client = new Anthropic();

const response = await client.messages.parse({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "..." }],
  output_config: { format: zodOutputFormat(ContactInfo) }
});

// Guaranteed type-safe
console.log(response.parsed_output.email);
```

</section>

</Tab>
<Tab title="Java">

**Metode `outputFormat(Class<T>)`**

Teruskan kelas Java ke `outputFormat()` dan SDK secara otomatis menurunkan skema JSON, memvalidasinya, dan mengembalikan `StructuredMessageCreateParams<T>`. Akses hasil yang telah diurai melalui `response.output(Class<T>)`.

<section title="Contoh penggunaan">

```java
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
}

StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
  .model(Model.CLAUDE_OPUS_4_6)
  .maxTokens(1024)
  .outputFormat(ContactInfo.class)
  .addUserMessage("...")
  .build();

var response = client.messages().create(createParams);
ContactInfo contact = response.output(ContactInfo.class);
System.out.println(contact.name + " (" + contact.email + ")");
```

</section>

<section title="Penghapusan tipe generik">

Informasi tipe generik untuk field dipertahankan dalam metadata kelas, tetapi penghapusan tipe generik berlaku dalam cakupan lain. Meskipun skema JSON dapat diturunkan dari field `BookList.books` dengan tipe `List<Book>`, skema JSON yang valid tidak dapat diturunkan dari variabel lokal dengan tipe yang sama.

Jika terjadi kesalahan saat mengonversi respons JSON ke instance kelas Java, pesan kesalahan akan menyertakan respons JSON untuk membantu diagnosis. Jika respons JSON Anda mungkin mengandung informasi sensitif, hindari mencatatnya secara langsung, atau pastikan Anda menyunting detail sensitif dari pesan kesalahan.

</section>

<section title="Validasi skema lokal">

Structured outputs mendukung [subset bahasa JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Skema dihasilkan secara otomatis dari kelas untuk selaras dengan subset ini. Metode `outputFormat(Class<T>)` melakukan pemeriksaan validasi pada skema yang diturunkan dari kelas yang ditentukan.

Poin-poin utama:

- **Validasi lokal** terjadi tanpa mengirim permintaan ke model AI jarak jauh.
- **Validasi jarak jauh** juga dilakukan oleh model AI saat menerima skema JSON.
- **Kompatibilitas versi**: Validasi lokal mungkin gagal sementara validasi jarak jauh berhasil jika versi SDK sudah usang.
- **Menonaktifkan validasi lokal**: Teruskan `JsonSchemaLocalValidation.NO` jika Anda mengalami masalah kompatibilitas:

```java
import com.anthropic.core.JsonSchemaLocalValidation;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
  .model(Model.CLAUDE_OPUS_4_6)
  .maxTokens(2048)
  .outputFormat(BookList.class, JsonSchemaLocalValidation.NO)
  .addUserMessage("List some famous late twentieth century novels.")
  .build();
```

</section>

<section title="Streaming">

Structured outputs juga dapat digunakan dengan streaming. Saat respons tiba dalam event stream, Anda perlu mengakumulasi respons penuh sebelum mendeserialisasi JSON.

Gunakan `BetaMessageAccumulator` untuk mengumpulkan string JSON dari stream. Setelah terakumulasi, panggil `BetaMessageAccumulator.message(Class<T>)` untuk mengonversi `BetaMessage` yang terakumulasi menjadi `StructuredMessage`, yang secara otomatis mendeserialisasi JSON ke kelas Java Anda.

</section>

<section title="Properti skema JSON">

Ketika skema JSON diturunkan dari kelas Java Anda, semua properti yang diwakili oleh field `public` atau metode getter `public` disertakan secara default. Field dan metode getter non-`public` dikecualikan.

Anda dapat mengontrol visibilitas dengan anotasi:

- `@JsonIgnore` mengecualikan field atau metode getter `public`
- `@JsonProperty` menyertakan field atau metode getter non-`public`

Jika Anda mendefinisikan field `private` dengan metode getter `public`, nama properti diturunkan dari getter (misalnya, field `private` `myValue` dengan metode `public` `getMyValue()` menghasilkan properti `"myValue"`). Untuk menggunakan nama getter non-konvensional, anotasi metode dengan `@JsonProperty`.

Setiap kelas harus mendefinisikan setidaknya satu properti untuk skema JSON. Kesalahan validasi terjadi jika tidak ada field atau metode getter yang dapat menghasilkan properti skema, seperti ketika:

- Tidak ada field atau metode getter dalam kelas
- Semua anggota `public` dianotasi dengan `@JsonIgnore`
- Semua anggota non-`public` tidak memiliki anotasi `@JsonProperty`
- Sebuah field menggunakan tipe `Map`, yang menghasilkan field `"properties"` kosong

</section>

<section title="Anotasi (Jackson dan Swagger)">

Anda dapat menggunakan anotasi Jackson Databind untuk memperkaya skema JSON yang diturunkan dari kelas Java Anda:

```java
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;

class Person {

  @JsonPropertyDescription("The first name and surname of the person")
  public String name;

  public int birthYear;

  @JsonPropertyDescription("The year the person died, or 'present' if the person is living.")
  public String deathYear;
}

@JsonClassDescription("The details of one published book")
class Book {

  public String title;
  public Person author;

  @JsonPropertyDescription("The year in which the book was first published.")
  public int publicationYear;

  @JsonIgnore
  public String genre;
}

class BookList {

  public List<Book> books;
}
```

Ringkasan anotasi:

- `@JsonClassDescription` -- Menambahkan deskripsi ke kelas
- `@JsonPropertyDescription` -- Menambahkan deskripsi ke field atau metode getter
- `@JsonIgnore` -- Mengecualikan field atau getter `public` dari skema
- `@JsonProperty` -- Menyertakan field atau getter non-`public` dalam skema

Jika Anda menggunakan `@JsonProperty(required = false)`, nilai `false` diabaikan. Skema JSON Anthropic harus menandai semua properti sebagai required.

Anda juga dapat menggunakan anotasi OpenAPI Swagger 2 `@Schema` dan `@ArraySchema` untuk batasan spesifik tipe:

```java
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Schema;

class Article {

  @ArraySchema(minItems = 1)
  public List<String> authors;

  public String title;

  @Schema(format = "date")
  public String publicationDate;

  @Schema(minimum = "1")
  public int pageCount;
}
```

Validasi lokal memeriksa bahwa Anda tidak menggunakan kata kunci batasan yang tidak didukung, tetapi nilai batasan tidak divalidasi secara lokal. Misalnya, nilai `"format"` yang tidak didukung mungkin lolos validasi lokal tetapi menyebabkan kesalahan jarak jauh.

Jika Anda menggunakan anotasi Jackson dan Swagger untuk menetapkan field skema yang sama, anotasi Jackson yang diutamakan.

</section>

</Tab>
<Tab title="Go">

**Skema JSON mentah melalui `OutputConfigParam`**

Go SDK bekerja dengan skema JSON mentah. Definisikan struct Go dengan tag json, hasilkan skema JSON (misalnya, menggunakan `invopop/jsonschema`), dan unmarshal teks respons ke dalam struct Anda.

<section title="Contoh penggunaan">

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/invopop/jsonschema"
)

type ContactInfo struct {
	Name         string `json:"name" jsonschema:"description=Full name"`
	Email        string `json:"email" jsonschema:"description=Email address"`
	PlanInterest string `json:"plan_interest" jsonschema:"description=Plan type"`
}

func generateSchema(v any) map[string]any {
	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
	s := r.Reflect(v)
	b, _ := json.Marshal(s)
	var m map[string]any
	json.Unmarshal(b, &m)
	return m
}

func main() {
	client := anthropic.NewClient()
	schema := generateSchema(&ContactInfo{})

	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(
				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.",
			)),
		},
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: schema,
			},
		},
	})

	var contact ContactInfo
	json.Unmarshal([]byte(message.Content[0].AsResponseTextBlock().Text), &contact)
	fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
}
```

</section>

</Tab>
<Tab title="Ruby">

**`output_config: {format: Model}` dengan `parsed_output`**

Definisikan kelas model yang memperluas `Anthropic::BaseModel` dan teruskan sebagai format ke `messages.create()`. Respons menyertakan atribut `parsed_output` dengan objek Ruby yang bertipe.

<section title="Contoh penggunaan">

```ruby
require "anthropic"

class ContactInfo < Anthropic::BaseModel
  required :name, String
  required :email, String
  required :plan_interest, String
end

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "..."}],
  output_config: {format: ContactInfo}
)

contact = message.parsed_output
puts "#{contact.name} (#{contact.email})"
```

</section>

<section title="Fitur model lanjutan">

Ruby SDK mendukung fitur definisi model tambahan untuk skema yang lebih kaya:

- **Kata kunci `doc:`** -- Menambahkan deskripsi ke field untuk output skema yang lebih informatif
- **`Anthropic::ArrayOf[T]`** -- Array bertipe dengan batasan `min_length` dan `max_length`
- **`Anthropic::EnumOf[:a, :b]`** -- Field enum dengan nilai yang dibatasi
- **`Anthropic::UnionOf[T1, T2]`** -- Tipe union yang dipetakan ke `anyOf`

```ruby
class FamousNumber < Anthropic::BaseModel
  required :value, Float
  optional :reason, String, doc: "why is this number mathematically significant?"
end

class Output < Anthropic::BaseModel
  required :numbers, Anthropic::ArrayOf[FamousNumber], min_length: 3, max_length: 5
end

message = anthropic.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "give me some famous numbers"}],
  output_config: {format: Output}
)

message.parsed_output
# => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi is...">...]>
```

</section>

</Tab>
<Tab title="C#">

**Skema JSON mentah melalui `OutputConfig`**

C# SDK menggunakan skema JSON mentah yang dibangun secara programatik dengan `JsonSerializer.SerializeToElement`. Deserialisasi JSON respons dengan `JsonSerializer.Deserialize`.

<section title="Contoh penggunaan">

```csharp
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-6",
    MaxTokens = 1024,
    Messages = [new() {
        Role = Role.User,
        Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
    }],
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    name = new { type = "string" },
                    email = new { type = "string" },
                    plan_interest = new { type = "string" },
                }),
                ["required"] = JsonSerializer.SerializeToElement(
                    new[] { "name", "email", "plan_interest" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
});

var json = (response.Content.First().Value as TextBlock)!.Text;
// JSON is guaranteed to match the schema
var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(json);
Console.WriteLine($"{contact["name"]} ({contact["email"]})");
```

</section>

</Tab>
<Tab title="PHP">

**Skema JSON mentah melalui `OutputConfig::with()`**

PHP SDK meneruskan skema JSON mentah sebagai array asosiatif melalui `OutputConfig::with()`. Dekode respons dengan `json_decode()`.

<section title="Contoh penggunaan">

```php
<?php

use Anthropic\Client;
use Anthropic\Messages\OutputConfig;
use Anthropic\Messages\JSONOutputFormat;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
    ],
    model: 'claude-opus-4-6',
    outputConfig: OutputConfig::with(format: JSONOutputFormat::with(schema: [
        'type' => 'object',
        'properties' => [
            'name' => ['type' => 'string'],
            'email' => ['type' => 'string'],
            'plan_interest' => ['type' => 'string'],
        ],
        'required' => ['name', 'email', 'plan_interest'],
        'additionalProperties' => false,
    ])),
);

$data = json_decode($response->content[0]->text, true);
echo $data['name'] . ' (' . $data['email'] . ')';
```

</section>

</Tab>
</Tabs>

#### Cara kerja transformasi SDK

SDK Python dan TypeScript secara otomatis mentransformasi skema dengan fitur yang tidak didukung:

1. **Menghapus batasan yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Memperbarui deskripsi** dengan info batasan (misalnya, "Harus minimal 100"), ketika batasan tidak didukung langsung dengan structured outputs
3. **Menambahkan `additionalProperties: false`** ke semua objek
4. **Memfilter format string** hanya ke daftar yang didukung
5. **Memvalidasi respons** terhadap skema asli Anda (dengan semua batasan)

Ini berarti Claude menerima skema yang disederhanakan, tetapi kode Anda tetap menerapkan semua batasan melalui validasi.

**Contoh:** Field Pydantic dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, tetapi deskripsi diperbarui menjadi "Harus minimal 100", dan SDK memvalidasi respons terhadap batasan asli.

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
    messages=[
        {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
    ],
)
```

```typescript TypeScript
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const InvoiceSchema = z.object({
  invoice_number: z.string(),
  date: z.string(),
  total_amount: z.number(),
  line_items: z.array(z.record(z.string(), z.any())),
  customer_name: z.string()
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(InvoiceSchema) },
  messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
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
    messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
)
```

```typescript TypeScript
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const ClassificationSchema = z.object({
  category: z.string(),
  confidence: z.number(),
  tags: z.array(z.string()),
  sentiment: z.string()
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(ClassificationSchema) },
  messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
});
```

</CodeGroup>

</section>

<section title="Pemformatan respons API">

Hasilkan respons yang siap untuk API:

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
    messages=[{"role": "user", "content": "Process this request: ..."}],
)
```

```typescript TypeScript
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const APIResponseSchema = z.object({
  status: z.string(),
  data: z.record(z.string(), z.any()),
  errors: z.array(z.record(z.string(), z.any())).optional(),
  metadata: z.record(z.string(), z.any())
});

const response = await client.messages.create({
  model: "claude-opus-4-6",
  output_config: { format: zodOutputFormat(APIResponseSchema) },
  messages: [{ role: "user", content: "Process this request: ..." }]
});
```

</CodeGroup>

</section>

## Penggunaan tool yang ketat

Penggunaan tool yang ketat memvalidasi parameter tool, memastikan Claude memanggil fungsi Anda dengan argumen yang bertipe dengan benar. Gunakan penggunaan tool yang ketat ketika Anda perlu:

- Memvalidasi parameter tool
- Membangun alur kerja agentic
- Memastikan pemanggilan fungsi yang type-safe
- Menangani tool kompleks dengan properti bersarang

### Mengapa penggunaan tool yang ketat penting untuk agen

Membangun sistem agentic yang andal memerlukan jaminan kesesuaian skema. Tanpa mode ketat, Claude mungkin mengembalikan tipe yang tidak kompatibel (`"2"` alih-alih `2`) atau field yang diperlukan hilang, merusak fungsi Anda dan menyebabkan kesalahan runtime.

Penggunaan tool yang ketat menjamin parameter yang type-safe:
- Fungsi menerima argumen yang bertipe dengan benar setiap saat
- Tidak perlu memvalidasi dan mencoba ulang pemanggilan tool
- Agen siap produksi yang bekerja secara konsisten dalam skala besar

Misalnya, anggaplah sistem pemesanan membutuhkan `passengers: int`. Tanpa mode ketat, Claude mungkin memberikan `passengers: "two"` atau `passengers: "2"`. Dengan `strict: true`, respons akan selalu berisi `passengers: 2`.

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
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
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
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
                    },
                },
                "required": ["location"],
                "additionalProperties": False,
            },
        }
    ],
)
print(response.content)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

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
  tools: [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      strict: true, // Enable strict mode
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
    }
  ]
});
console.log(response.content);
```

</CodeGroup>

**Format respons:** Blok penggunaan tool dengan input yang telah divalidasi di `response.content[x].input`

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
- `input` tool secara ketat mengikuti `input_schema`
- `name` tool selalu valid (dari tool yang disediakan atau server tools)

### Cara kerjanya

<Steps>
  <Step title="Definisikan skema tool Anda">
    Buat skema JSON untuk `input_schema` tool Anda. Skema menggunakan format JSON Schema standar dengan beberapa keterbatasan (lihat [Keterbatasan JSON Schema](#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan strict: true">
    Tetapkan `"strict": true` sebagai properti tingkat atas dalam definisi tool Anda, bersama dengan `name`, `description`, dan `input_schema`.
  </Step>
  <Step title="Tangani pemanggilan tool">
    Ketika Claude menggunakan tool, field `input` dalam blok tool_use akan secara ketat mengikuti `input_schema` Anda, dan `name` akan selalu valid.
  </Step>
</Steps>

### Kasus penggunaan umum

<section title="Input tool yang divalidasi">

Pastikan parameter tool persis sesuai dengan skema Anda:

<CodeGroup>

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Search for flights to Tokyo"}],
    tools=[
        {
            "name": "search_flights",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string", "format": "date"},
                    "passengers": {
                        "type": "integer",
                        "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    },
                },
                "required": ["destination", "departure_date"],
                "additionalProperties": False,
            },
        }
    ],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  messages: [{ role: "user", content: "Search for flights to Tokyo" }],
  tools: [
    {
      name: "search_flights",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          destination: { type: "string" },
          departure_date: { type: "string", format: "date" },
          passengers: { type: "integer", enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] }
        },
        required: ["destination", "departure_date"],
        additionalProperties: false
      }
    }
  ]
});
```

</CodeGroup>

</section>

<section title="Alur kerja agentic dengan beberapa tool yang divalidasi">

Bangun agen multi-langkah yang andal dengan parameter tool yang terjamin:

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
                    "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]},
                },
                "required": ["origin", "destination", "departure_date"],
                "additionalProperties": False,
            },
        },
        {
            "name": "search_hotels",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "check_in": {"type": "string", "format": "date"},
                    "guests": {"type": "integer", "enum": [1, 2, 3, 4]},
                },
                "required": ["city", "check_in"],
                "additionalProperties": False,
            },
        },
    ],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  messages: [{ role: "user", content: "Help me plan a trip to Paris for 2 people" }],
  tools: [
    {
      name: "search_flights",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          origin: { type: "string" },
          destination: { type: "string" },
          departure_date: { type: "string", format: "date" },
          travelers: { type: "integer", enum: [1, 2, 3, 4, 5, 6] }
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
          city: { type: "string" },
          check_in: { type: "string", format: "date" },
          guests: { type: "integer", enum: [1, 2, 3, 4] }
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

Output JSON dan penggunaan tool yang ketat memecahkan masalah yang berbeda dan dapat digunakan bersama-sama:

- **Output JSON** mengontrol format respons Claude (apa yang dikatakan Claude)
- **Penggunaan tool yang ketat** memvalidasi parameter tool (bagaimana Claude memanggil fungsi Anda)

Ketika digabungkan, Claude dapat memanggil tool dengan parameter yang terjamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agentic di mana Anda membutuhkan panggilan tool yang andal sekaligus output akhir yang terstruktur.

<CodeGroup>

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Help me plan a trip to Paris for next month"}
    ],
    # Output JSON: format respons terstruktur
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "next_steps": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["summary", "next_steps"],
                "additionalProperties": False,
            },
        }
    },
    # Penggunaan tool yang ketat: parameter tool yang terjamin
    tools=[
        {
            "name": "search_flights",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                    "date": {"type": "string", "format": "date"},
                },
                "required": ["destination", "date"],
                "additionalProperties": False,
            },
        }
    ],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Help me plan a trip to Paris for next month" }],
  // Output JSON: format respons terstruktur
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
  // Penggunaan tool yang ketat: parameter tool yang terjamin
  tools: [
    {
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
    }
  ]
});
```

</CodeGroup>

## Pertimbangan penting

### Kompilasi grammar dan caching

Output terstruktur menggunakan constrained sampling dengan artefak grammar yang dikompilasi. Ini memperkenalkan beberapa karakteristik performa yang perlu diperhatikan:

- **Latensi permintaan pertama**: Pertama kali Anda menggunakan skema tertentu, akan ada latensi tambahan saat grammar dikompilasi
- **Caching otomatis**: Grammar yang dikompilasi di-cache selama 24 jam sejak terakhir digunakan, membuat permintaan berikutnya jauh lebih cepat
- **Invalidasi cache**: Cache akan diinvalidasi jika Anda mengubah:
  - Struktur skema JSON
  - Kumpulan tool dalam permintaan Anda (saat menggunakan output terstruktur dan penggunaan tool sekaligus)
  - Mengubah hanya field `name` atau `description` tidak menginvalidasi cache

### Modifikasi prompt dan biaya token

Saat menggunakan output terstruktur, Claude secara otomatis menerima system prompt tambahan yang menjelaskan format output yang diharapkan. Ini berarti:

- Jumlah token input Anda akan sedikit lebih tinggi
- Prompt yang disuntikkan membutuhkan token seperti system prompt lainnya
- Mengubah parameter `output_config.format` akan menginvalidasi [cache prompt](/docs/id/build-with-claude/prompt-caching) mana pun untuk thread percakapan tersebut

### Keterbatasan JSON Schema

Output terstruktur mendukung JSON Schema standar dengan beberapa keterbatasan. Baik output JSON maupun penggunaan tool yang ketat berbagi keterbatasan ini.

<section title="Fitur yang didukung">

- Semua tipe dasar: object, array, string, integer, number, boolean, null
- `enum` (hanya string, angka, bool, atau null - tidak ada tipe kompleks)
- `const`
- `anyOf` dan `allOf` (dengan keterbatasan - `allOf` dengan `$ref` tidak didukung)
- `$ref`, `$def`, dan `definitions` (eksternal `$ref` tidak didukung)
- Properti `default` untuk semua tipe yang didukung
- `required` dan `additionalProperties` (harus diatur ke `false` untuk objek)
- Format string: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
- Array `minItems` (hanya nilai 0 dan 1 yang didukung)

</section>

<section title="Tidak didukung">

- Skema rekursif
- Tipe kompleks dalam enum
- Eksternal `$ref` (misalnya, `'$ref': 'http://...'`)
- Batasan numerik (`minimum`, `maximum`, `multipleOf`, dll.)
- Batasan string (`minLength`, `maxLength`)
- Batasan array di luar `minItems` 0 atau 1
- `additionalProperties` diatur ke selain `false`

Jika Anda menggunakan fitur yang tidak didukung, Anda akan menerima error 400 dengan detailnya.

</section>

<section title="Dukungan pola (regex)">

**Fitur regex yang didukung:**
- Pencocokan penuh (`^...$`) dan pencocokan parsial
- Quantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
- Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
- Grup: `(...)`

**TIDAK didukung:**
- Backreference ke grup (misalnya, `\1`, `\2`)
- Pernyataan lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
- Batas kata: `\b`, `\B`
- Quantifier `{n,m}` kompleks dengan rentang besar

Pola regex sederhana bekerja dengan baik. Pola kompleks dapat menghasilkan error 400.

</section>

<Tip>
SDK Python dan TypeScript dapat secara otomatis mengubah skema dengan fitur yang tidak didukung dengan menghapusnya dan menambahkan batasan ke deskripsi field. Lihat [metode khusus SDK](#sdk-specific-methods) untuk detailnya.
</Tip>

### Urutan properti

Saat menggunakan output terstruktur, properti dalam objek mempertahankan urutan yang ditentukan dari skema Anda, dengan satu catatan penting: **properti yang diperlukan muncul pertama, diikuti oleh properti opsional**.

Misalnya, dengan skema ini:

```json
{
  "type": "object",
  "properties": {
    "notes": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

Output akan mengurutkan properti sebagai:

1. `name` (diperlukan, dalam urutan skema)
2. `email` (diperlukan, dalam urutan skema)
3. `notes` (opsional, dalam urutan skema)
4. `age` (opsional, dalam urutan skema)

Ini berarti output mungkin terlihat seperti:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "notes": "Interested in enterprise plan",
  "age": 35
}
```

Jika urutan properti dalam output penting untuk aplikasi Anda, pastikan semua properti ditandai sebagai required, atau pertimbangkan pengurutan ulang ini dalam logika parsing Anda.

### Output yang tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam sebagian besar kasus, ada skenario di mana output mungkin tidak sesuai dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan properti keamanan dan kegunaannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keamanan:

- Respons akan memiliki `stop_reason: "refusal"`
- Anda akan menerima kode status 200
- Anda akan ditagih untuk token yang dihasilkan
- Output mungkin tidak sesuai dengan skema Anda karena pesan penolakan mengambil prioritas di atas batasan skema

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons terpotong karena mencapai batas `max_tokens`:

- Respons akan memiliki `stop_reason: "max_tokens"`
- Output mungkin tidak lengkap dan tidak sesuai dengan skema Anda
- Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap

### Batas kompleksitas skema

Output terstruktur bekerja dengan mengompilasi skema JSON Anda menjadi grammar yang membatasi output Claude. Skema yang lebih kompleks menghasilkan grammar yang lebih besar yang membutuhkan waktu lebih lama untuk dikompilasi. Untuk melindungi dari waktu kompilasi yang berlebihan, API memberlakukan beberapa batas kompleksitas.

#### Batas eksplisit

Batas berikut berlaku untuk semua permintaan dengan `output_config.format` atau `strict: true`:

| Batas | Nilai | Deskripsi |
|-------|-------|-------------|
| Tool ketat per permintaan | 20 | Jumlah maksimum tool dengan `strict: true`. Tool non-ketat tidak dihitung terhadap batas ini. |
| Parameter opsional | 24 | Total parameter opsional di semua skema tool ketat dan skema output JSON. Setiap parameter yang tidak tercantum dalam `required` dihitung terhadap batas ini. |
| Parameter dengan tipe union | 16 | Total parameter yang menggunakan `anyOf` atau array tipe (misalnya, `"type": ["string", "null"]`) di semua skema ketat. Ini sangat mahal karena menciptakan biaya kompilasi eksponensial. |

<Note>
Batas ini berlaku untuk total gabungan di semua skema ketat dalam satu permintaan. Misalnya, jika Anda memiliki 4 tool ketat dengan masing-masing 6 parameter opsional, Anda akan mencapai batas 24 parameter meskipun tidak ada satu tool pun yang tampak kompleks.
</Note>

#### Batas internal tambahan

Di luar batas eksplisit di atas, ada batas internal tambahan pada ukuran grammar yang dikompilasi. Batas ini ada karena kompleksitas skema tidak dapat direduksi menjadi satu dimensi: fitur seperti parameter opsional, tipe union, objek bersarang, dan jumlah tool berinteraksi satu sama lain dengan cara yang dapat membuat grammar yang dikompilasi menjadi sangat besar secara tidak proporsional.

Ketika batas ini terlampaui, Anda akan menerima error 400 dengan pesan "Schema is too complex for compilation." Error ini berarti kompleksitas gabungan skema Anda melebihi apa yang dapat dikompilasi secara efisien, bahkan jika setiap batas individual di atas terpenuhi. Sebagai langkah terakhir, API juga memberlakukan **batas waktu kompilasi 180 detik**. Skema yang melewati semua pemeriksaan eksplisit tetapi menghasilkan grammar yang dikompilasi sangat besar mungkin mencapai batas waktu ini.

#### Tips untuk mengurangi kompleksitas skema

Jika Anda mencapai batas kompleksitas, coba strategi berikut secara berurutan:

1. **Tandai hanya tool kritis sebagai ketat.** Jika Anda memiliki banyak tool, simpan untuk tool di mana pelanggaran skema menyebabkan masalah nyata, dan andalkan kepatuhan alami Claude untuk tool yang lebih sederhana.

2. **Kurangi parameter opsional.** Jadikan parameter `required` jika memungkinkan. Setiap parameter opsional kira-kira menggandakan sebagian ruang status grammar. Jika parameter selalu memiliki default yang wajar, pertimbangkan untuk menjadikannya required dan meminta Claude memberikan default tersebut secara eksplisit.

3. **Sederhanakan struktur bersarang.** Objek yang sangat bersarang dengan field opsional memperparah kompleksitas. Ratakan struktur jika memungkinkan.

4. **Bagi menjadi beberapa permintaan.** Jika Anda memiliki banyak tool ketat, pertimbangkan untuk membaginya ke permintaan atau sub-agen yang terpisah.

Untuk masalah persisten dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan definisi skema Anda.

## Retensi data

Prompt dan respons diproses dengan ZDR saat menggunakan output terstruktur. Namun, skema JSON itu sendiri di-cache sementara hingga 24 jam sejak terakhir digunakan untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan di luar respons API.

Untuk kelayakan ZDR di semua fitur, lihat [API dan Retensi Data](/docs/id/build-with-claude/api-and-data-retention).

## Kompatibilitas fitur

**Bekerja dengan:**
- **[Pemrosesan batch](/docs/id/build-with-claude/batch-processing)**: Proses output terstruktur dalam skala besar dengan diskon 50%
- **[Penghitungan token](/docs/id/build-with-claude/token-counting)**: Hitung token tanpa kompilasi
- **[Streaming](/docs/id/build-with-claude/streaming)**: Stream output terstruktur seperti respons normal
- **Penggunaan gabungan**: Gunakan output JSON (`output_config.format`) dan penggunaan tool yang ketat (`strict: true`) bersama-sama dalam permintaan yang sama

**Tidak kompatibel dengan:**
- **[Kutipan](/docs/id/build-with-claude/citations)**: Kutipan memerlukan penyisipan blok kutipan dengan teks, yang bertentangan dengan batasan skema JSON yang ketat. Mengembalikan error 400 jika kutipan diaktifkan dengan `output_config.format`.
- **Prefilling Pesan**: Tidak kompatibel dengan output JSON

<Tip>
**Cakupan grammar**: Grammar hanya berlaku untuk output langsung Claude, bukan untuk panggilan penggunaan tool, hasil tool, atau tag thinking (saat menggunakan [Extended Thinking](/docs/id/build-with-claude/extended-thinking)). Status grammar direset di antara bagian, memungkinkan Claude berpikir dengan bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>