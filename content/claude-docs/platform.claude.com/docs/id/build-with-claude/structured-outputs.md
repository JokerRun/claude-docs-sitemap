---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 7ae6334a0314e95c50f45ffaca83049b6c5d3b640b9c76020b1e5790bd990f75
---

# Keluaran terstruktur

Dapatkan hasil JSON yang divalidasi dari alur kerja agen

---

Keluaran terstruktur membatasi respons Claude untuk mengikuti skema tertentu, memastikan keluaran yang valid dan dapat diurai untuk pemrosesan hilir. Keluaran terstruktur menyediakan dua fitur yang saling melengkapi:

- **Keluaran JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu
- **Penggunaan alat yang ketat** (`strict: true`): Jamin validasi skema pada nama alat dan input

Anda dapat menggunakan fitur-fitur ini secara independen atau bersama-sama dalam permintaan yang sama.

<Note>
Keluaran terstruktur tersedia secara umum di Claude API untuk [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Di Amazon Bedrock, keluaran terstruktur tersedia secara umum untuk Claude Mythos Preview, Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5; Claude Opus 4.7 tersedia melalui [pratinjau penelitian Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock-research-preview). Keluaran terstruktur dalam beta di Microsoft Foundry. Keluaran terstruktur tidak didukung di Vertex AI Google Cloud untuk Claude Mythos Preview.
</Note>

<Note>
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Tip>
**Bermigrasi dari beta?** Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Header beta lama (`structured-outputs-2025-11-13`) dan parameter `output_format` akan terus berfungsi selama periode transisi. Lihat contoh kode di bawah untuk bentuk API yang diperbarui.
</Tip>

## Mengapa menggunakan keluaran terstruktur

Tanpa keluaran terstruktur, Claude dapat menghasilkan respons JSON yang salah bentuk atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompt yang hati-hati, Anda mungkin mengalami:
- Kesalahan penguraian dari sintaks JSON yang tidak valid
- Bidang yang diperlukan hilang
- Tipe data yang tidak konsisten
- Pelanggaran skema yang memerlukan penanganan kesalahan dan percobaan ulang

Keluaran terstruktur menjamin respons yang sesuai dengan skema melalui decoding terbatas:
- **Selalu valid**: Tidak ada lagi kesalahan `JSON.parse()`
- **Aman tipe**: Tipe bidang dan bidang yang diperlukan dijamin
- **Andal**: Tidak perlu percobaan ulang untuk pelanggaran skema

## Keluaran JSON

Keluaran JSON mengontrol format respons Claude, memastikan Claude mengembalikan JSON yang valid sesuai dengan skema Anda. Gunakan keluaran JSON ketika Anda perlu:

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
    "model": "claude-opus-4-7",
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

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' \
  --format jsonl <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
messages:
  - role: user
    content: >-
      Extract the key information from this email: John Smith
      (john@example.com) is interested in our Enterprise plan and wants
      to schedule a demo for next Tuesday at 2pm.
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        name: {type: string}
        email: {type: string}
        plan_interest: {type: string}
        demo_requested: {type: boolean}
      required: [name, email, plan_interest, demo_requested]
      additionalProperties: false
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
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

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-7",
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

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

```csharp C#
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan." }],
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
                ["required"] = JsonSerializer.SerializeToElement(new[] { "name", "email", "plan_interest", "demo_requested" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go hidelines={1..10,-1}
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
			Model:     anthropic.ModelClaudeOpus4_7,
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{
				anthropic.NewUserMessage(
					anthropic.NewTextBlock("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."),
				),
			},
			OutputConfig: anthropic.OutputConfigParam{
				Format: anthropic.JSONOutputFormatParam{
					Schema: map[string]any{
						"type": "object",
						"properties": map[string]any{
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

```java Java hidelines={1..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

static class ContactInfo {
    public String name;
    public String email;
    public String plan_interest;
    public boolean demo_requested;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.")
        .outputConfig(ContactInfo.class)
        .build();

    StructuredMessage<ContactInfo> response = client.messages().create(params);
    ContactInfo contact = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(contact.name + " (" + contact.email + ")");
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'
        ]
    ],
    model: 'claude-opus-4-7',
    outputConfig: [
        'format' => [
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
    ],
);

echo $response->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-7",
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

</CodeGroup>

**Format respons:** JSON yang valid sesuai dengan skema Anda di `response.content[0].text`

```json Output
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
    Buat skema JSON yang mendeskripsikan struktur yang ingin diikuti Claude. Skema menggunakan format JSON Schema standar dengan beberapa batasan (lihat [batasan JSON Schema](#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan parameter output_config.format">
    Sertakan parameter `output_config.format` dalam permintaan API Anda dengan `type: "json_schema"` dan definisi skema Anda.
  </Step>
  <Step title="Urai respons">
    Respons Claude adalah JSON yang valid sesuai dengan skema Anda, dikembalikan di `response.content[0].text`.
  </Step>
</Steps>

### Bekerja dengan output JSON di SDK

SDK menyediakan helper yang memudahkan pekerjaan dengan output JSON, termasuk transformasi skema, validasi otomatis, dan integrasi dengan perpustakaan skema populer.

<Note>
SDK Python `client.messages.parse()` masih menerima `output_format` sebagai parameter kenyamanan dan menerjemahkannya ke `output_config.format` secara internal. SDK lainnya memerlukan `output_config` secara langsung. Contoh di bawah menunjukkan sintaks helper SDK.
</Note>

#### Menggunakan definisi skema native

Alih-alih menulis skema JSON mentah, Anda dapat menggunakan alat definisi skema yang familiar di bahasa Anda:

- **Python**: Model [Pydantic](https://docs.pydantic.dev/) dengan `client.messages.parse()`
- **TypeScript**: Skema [Zod](https://zod.dev/) dengan `zodOutputFormat()` atau literal JSON Schema yang diketik dengan `jsonSchemaOutputFormat()`
- **Java**: Kelas Java biasa dengan derivasi skema otomatis melalui `outputConfig(Class<T>)`
- **Ruby**: Kelas `Anthropic::BaseModel` dengan `output_config: {format: Model}`
- **PHP**: Kelas yang mengimplementasikan `StructuredOutputModel` dengan `outputConfig: ['format' => MyClass::class]`
- **CLI**, **C#**, **Go**: Skema JSON mentah dilewatkan melalui `output_config`

<CodeGroup>

```bash CLI
{ read -r _ NAME; read -r _ EMAIL; } < <(
  ant messages create \
    --transform 'content.0.text|@fromstr|{name,email}' --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
messages:
  - role: user
    content: >-
      Extract the key information from this email: John Smith
      (john@example.com) is interested in our Enterprise plan and wants
      to schedule a demo for next Tuesday at 2pm.
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        name: {type: string}
        email: {type: string}
        plan_interest: {type: string}
        demo_requested: {type: boolean}
      required: [name, email, plan_interest, demo_requested]
      additionalProperties: false
YAML
)
printf '%s (%s)\n' "$NAME" "$EMAIL"
```

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
    model="claude-opus-4-7",
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

```typescript TypeScript hidelines={1}
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
  model: "claude-opus-4-7",
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

// Automatically parsed and validated
console.log(response.parsed_output);
```

```csharp C#
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-7",
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

if (response.Content[0].TryPickText(out var textBlock))
{
    // JSON is guaranteed to match the schema
    var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
    Console.WriteLine($"{contact["name"]} ({contact["email"]})");
}
```

```go Go hidelines={1..2,4..7,27..29,-1}
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
		Model:     anthropic.ModelClaudeOpus4_7,
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

	for _, block := range message.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.TextBlock:
			var contact ContactInfo
			json.Unmarshal([]byte(variant.Text), &contact)
			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
		}
	}
}
```

```java Java hidelines={1..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

static class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
    public boolean demoRequested;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .outputConfig(ContactInfo.class)
        .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.")
        .build();

    StructuredMessage<ContactInfo> response = client.messages().create(createParams);
    ContactInfo contact = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(contact.name + " (" + contact.email + ")");
}
```

```php PHP hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

$client = new Client();

class ContactInfo implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $name;
    public string $email;
    public string $plan_interest;
    public bool $demo_requested;
}

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.'],
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['format' => ContactInfo::class],
);

$contact = $message->parsedOutput();
if ($contact instanceof ContactInfo) {
    echo "{$contact->name} ({$contact->email})\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

class ContactInfo < Anthropic::BaseModel
  required :name, String
  required :email, String
  required :plan_interest, String
  required :demo_requested, Anthropic::Boolean
end

message = client.messages.create(
  model: "claude-opus-4-7",
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

</CodeGroup>

#### Metode spesifik SDK

Setiap SDK menyediakan helper yang membuat pekerjaan dengan output terstruktur lebih mudah. Lihat halaman SDK individual untuk detail lengkap.

<Tabs>
<Tab title="CLI">

**Skema JSON mentah melalui heredoc body**

CLI melewatkan skema JSON mentah sebagai heredoc body YAML. Gunakan modifier GJSON `@fromstr` dengan `--transform` untuk mengurai string JSON yang dikembalikan dalam `content[0].text` dan memproyeksikan field tertentu.

```bash
ant messages create \
  --transform 'content.0.text|@fromstr|{name,email}' \
  --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
messages:
  - role: user
    content: >-
      Extract contact info: John Smith, john@example.com,
      interested in the Pro plan
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        name: {type: string}
        email: {type: string}
        plan_interest: {type: string}
      required: [name, email, plan_interest]
      additionalProperties: false
YAML
```

```yaml Output
name: John Smith
email: john@example.com
```

</Tab>
<Tab title="Python">

**`client.messages.parse()` (Direkomendasikan)**

Metode `parse()` secara otomatis mengubah model Pydantic Anda, memvalidasi respons, dan mengembalikan atribut `parsed_output`.

```python hidelines={2..4,9..12}
from pydantic import BaseModel
import anthropic


class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str


client = anthropic.Anthropic()

response = client.messages.parse(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract contact info: John Smith, john@example.com, interested in the Pro plan",
        }
    ],
    output_format=ContactInfo,
)

# Access the parsed output directly
contact = response.parsed_output
print(contact.name, contact.email)
```

**Helper `transform_schema()`**

Untuk ketika Anda perlu secara manual mengubah skema sebelum mengirim, atau ketika Anda ingin memodifikasi skema yang dihasilkan Pydantic. Tidak seperti `client.messages.parse()`, yang mengubah skema yang disediakan secara otomatis, ini memberi Anda skema yang diubah sehingga Anda dapat menyesuaikannya lebih lanjut.

```python nocheck
from anthropic import transform_schema
from pydantic import TypeAdapter

# First convert Pydantic model to JSON schema, then transform
schema = TypeAdapter(ContactInfo).json_schema()
schema = transform_schema(schema)
# Modify schema if needed
schema["properties"]["custom_field"] = {"type": "string"}

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    output_config={
        "format": {"type": "json_schema", "schema": schema},
    },
)
```

</Tab>
<Tab title="TypeScript">

**`client.messages.parse()` dengan `zodOutputFormat()`**

Metode `parse()` menerima skema Zod, memvalidasi respons, dan mengembalikan atribut `parsed_output` dengan tipe TypeScript yang disimpulkan sesuai dengan skema.

```typescript hidelines={1}
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
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
    }
  ],
  output_config: { format: zodOutputFormat(ContactInfo) }
});

// Guaranteed type-safe
console.log(response.parsed_output!.email);
```

**`client.messages.parse()` dengan `jsonSchemaOutputFormat()`**

Helper `jsonSchemaOutputFormat()` menerima objek JSON Schema dan mengintegrasikannya dengan `parse()` tanpa memerlukan Zod. Zod adalah dependensi peer opsional yang Anda instal secara terpisah; `jsonSchemaOutputFormat()` bekerja langsung dari kotak karena SDK menggabungkan `json-schema-to-ts` secara langsung.

Untuk **literal skema inline** (dideklarasikan dengan `as const` di sumber Anda), Anda juga mendapatkan inferensi tipe waktu kompilasi: `parsed_output` diketik untuk mencocokkan struktur skema. Untuk **skema yang diimpor atau dihasilkan** (dari file JSON atau codegen OpenAPI), helper masih mengirim skema dan mengurai respons, tetapi tipe yang disimpulkan adalah `unknown` karena `as const` hanya dapat diterapkan pada ekspresi literal.

```typescript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { jsonSchemaOutputFormat } from "@anthropic-ai/sdk/helpers/json-schema";

const client = new Anthropic();

const response = await client.messages.parse({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
    }
  ],
  output_config: {
    format: jsonSchemaOutputFormat({
      type: "object",
      properties: {
        name: { type: "string" },
        email: { type: "string" },
        planInterest: { type: "string" }
      },
      required: ["name", "email", "planInterest"],
      additionalProperties: false
    } as const)
  }
});

// response.parsed_output is typed as { name: string; email: string; planInterest: string } | null
console.log(response.parsed_output!.email);
```

**Inferensi tipe memerlukan `as const`.** Gunakan ekspresi objek literal dengan pernyataan `const` sehingga TypeScript dapat mempersempit tipe properti. Tanpa `as const`, tipe yang disimpulkan runtuh menjadi `unknown`.

**Transformasi skema.** Secara default, helper mengubah skema dengan cara yang sama seperti `zodOutputFormat()`: menghapus batasan yang tidak didukung, menambahkan `additionalProperties: false` ke objek, dan memfilter format string. Lewatkan `jsonSchemaOutputFormat(schema, { transform: false })` untuk mengirim skema Anda ke API tanpa perubahan. Lihat [Cara kerja transformasi SDK](#how-sdk-transformation-works).

</Tab>
<Tab title="C#">

**Skema JSON mentah melalui `OutputConfig`**

SDK C# menggunakan skema JSON mentah yang dibangun secara terprogram dengan `JsonSerializer.SerializeToElement`. Deserialize respons JSON dengan `JsonSerializer.Deserialize`.

```csharp
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-7",
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

if (response.Content[0].TryPickText(out var textBlock))
{
    // JSON is guaranteed to match the schema
    var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
    Console.WriteLine($"{contact["name"]} ({contact["email"]})");
}
```

</Tab>
<Tab title="Go">

**Skema JSON mentah melalui `OutputConfigParam`**

SDK Go bekerja dengan skema JSON mentah. Tentukan struct Go dengan tag json, hasilkan skema JSON (misalnya, menggunakan `invopop/jsonschema`), dan unmarshal teks respons ke dalam struct Anda.

```go hidelines={1..2,4..7,26..28,-1}
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
		Model:     anthropic.ModelClaudeOpus4_7,
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

	for _, block := range message.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.TextBlock:
			var contact ContactInfo
			json.Unmarshal([]byte(variant.Text), &contact)
			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
		}
	}
}
```

</Tab>
<Tab title="Java">

Contoh Java di halaman ini menggunakan sintaks [JDK 25 compact source file](https://openjdk.org/jeps/512); lihat [persyaratan Java SDK](/docs/id/api/sdks/java#requirements) untuk substitusi pada JDK sebelumnya.

**Metode `outputConfig(Class<T>)`**

Lewatkan kelas Java ke `outputConfig()` dan SDK secara otomatis menurunkan skema JSON, memvalidasinya, dan mengembalikan `StructuredMessageCreateParams<T>`. Akses hasil yang diurai melalui `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`.

<Note>
Deklarasikan kelas skema Anda sebagai kelas tingkat atas atau kelas bersarang `static`. Persyaratan ini berasal dari perpustakaan Jackson Databind (`com.fasterxml.jackson.databind`), yang digunakan SDK untuk mendeserialisasi respons JSON ke dalam instance kelas Anda dan tidak dapat membuat instance kelas inner non-static.
</Note>

```java hidelines={1..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

static class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .outputConfig(ContactInfo.class)
        .addUserMessage("Extract contact info: John Smith, john@example.com, interested in the Pro plan")
        .build();

    StructuredMessage<ContactInfo> response = client.messages().create(createParams);
    ContactInfo contact = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(contact.name + " (" + contact.email + ")");
}
```

<section title="Penghapusan tipe generik">

Java mempertahankan informasi tipe generik untuk field dalam metadata kelas, tetapi penghapusan tipe generik berlaku dalam cakupan lain. Meskipun skema JSON dapat diturunkan dari field `BookList.books` dengan tipe `List<Book>`, skema JSON yang valid tidak dapat diturunkan dari variabel lokal dari tipe yang sama.

Jika kesalahan terjadi saat mengonversi respons JSON ke instance kelas Java, pesan kesalahan menyertakan respons JSON untuk membantu diagnosis. Jika respons JSON Anda mungkin berisi informasi sensitif, hindari mencatat langsung, atau pastikan Anda menyunting detail sensitif apa pun dari pesan kesalahan.

</section>

<section title="Validasi skema lokal">

Output terstruktur mendukung [subset dari bahasa JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). SDK menghasilkan skema secara otomatis dari kelas untuk selaras dengan subset ini. Metode `outputConfig(Class<T>)` melakukan pemeriksaan validasi pada skema yang diturunkan dari kelas yang ditentukan.

Poin kunci:

- **Validasi lokal** terjadi tanpa mengirim permintaan ke model AI jarak jauh.
- **Validasi jarak jauh** juga dilakukan oleh model AI saat menerima skema JSON.
- **Kompatibilitas versi**: Validasi lokal mungkin gagal sementara validasi jarak jauh berhasil jika versi SDK sudah ketinggalan zaman.
- **Menonaktifkan validasi lokal**: Lewatkan `JsonSchemaLocalValidation.NO` jika Anda mengalami masalah kompatibilitas:

```java hidelines={2..4}
import com.anthropic.core.JsonSchemaLocalValidation;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

static class BookList {
    public List<String> books;
}

void main() {
    StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(2048)
        .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
        .addUserMessage("List some famous late twentieth century novels.")
        .build();
}
```

</section>

<section title="Streaming">

Output terstruktur juga bekerja dengan streaming. Saat respons tiba dalam event stream, Anda perlu mengumpulkan respons lengkap sebelum mendeserialisasi JSON.

Gunakan `MessageAccumulator` untuk mengumpulkan string JSON dari stream. Setelah dikumpulkan, panggil `MessageAccumulator.message(Class<T>)` untuk mengonversi `Message` yang terakumulasi menjadi `StructuredMessage`, yang secara otomatis mendeserialisasi JSON ke dalam kelas Java Anda.

</section>

<section title="Properti skema JSON">

Ketika SDK menurunkan skema JSON dari kelas Java Anda, secara default menyertakan semua properti yang diwakili oleh field `public` atau metode getter `public` dan mengecualikan field non-`public` dan metode getter.

Anda dapat mengontrol visibilitas dengan anotasi:

- `@JsonIgnore` mengecualikan field `public` atau metode getter
- `@JsonProperty` menyertakan field atau metode getter non-`public`

Jika Anda mendefinisikan field `private` dengan metode getter `public`, SDK menurunkan nama properti dari getter (misalnya, field `private` `myValue` dengan metode `public` `getMyValue()` menghasilkan properti `"myValue"`). Untuk menggunakan nama getter non-konvensional, anotasi metode dengan `@JsonProperty`.

Setiap kelas harus mendefinisikan setidaknya satu properti untuk skema JSON. Kesalahan validasi terjadi jika tidak ada field atau metode getter yang dapat menghasilkan properti skema, seperti ketika:

- Tidak ada field atau metode getter di kelas
- Semua anggota `public` dianotasi dengan `@JsonIgnore`
- Semua anggota non-`public` tidak memiliki anotasi `@JsonProperty`
- Field menggunakan tipe `Map`, yang menghasilkan field `"properties"` kosong

</section>

<section title="Komposisi dan warisan">

Kelas Java Anda dapat menggunakan komposisi dan warisan untuk berbagi struktur saat mendefinisikan skema JSON. Setiap pola mempengaruhi struktur output secara berbeda.

**Komposisi** menghasilkan output JSON bersarang. Menurunkan skema dari kelas `Composed` yang menggabungkan `A` dan `B`:

```java hidelines={1..7,20..35}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;

static class A {
    public String a;
}

static class B {
    public String b;
}

static class Composed {
    public A composedA;
    public B composedB;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();
    StructuredMessageCreateParams<Composed> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .outputConfig(Composed.class)
        .addUserMessage("Populate field a with 'hello' and field b with 'world'.")
        .build();
    StructuredMessage<Composed> response = client.messages().create(params);
    Composed result = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println("composedA.a=" + result.composedA.a);
    IO.println("composedB.b=" + result.composedB.b);
}
```

Output JSON memiliki struktur bersarang ini:

```json
{
  "composedA": { "a": "hello" },
  "composedB": { "b": "world" }
}
```

**Warisan** menghasilkan output JSON datar. Menurunkan skema dari kelas `Derived` yang memperluas `Base`:

```java hidelines={1..7,15..30}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;

static class Base {
    public String a;
}

static class Derived extends Base {
    public String b;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();
    StructuredMessageCreateParams<Derived> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .outputConfig(Derived.class)
        .addUserMessage("Populate field a with 'hello' and field b with 'world'.")
        .build();
    StructuredMessage<Derived> response = client.messages().create(params);
    Derived result = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println("a=" + result.a);
    IO.println("b=" + result.b);
}
```

Output JSON memiliki struktur datar ini:

```json
{
  "a": "hello",
  "b": "world"
}
```

</section>

<section title="Anotasi (Jackson dan Swagger)">

Anda dapat menggunakan anotasi Jackson Databind untuk memperkaya skema JSON yang diturunkan dari kelas Java Anda:

```java hidelines={-2..}
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;

static class Person {

  @JsonPropertyDescription("The first name and surname of the person")
  public String name;

  public int birthYear;

  @JsonPropertyDescription("The year the person died, or 'present' if the person is living.")
  public String deathYear;
}

@JsonClassDescription("The details of one published book")
static class Book {

  public String title;
  public Person author;

  @JsonPropertyDescription("The year in which the book was first published.")
  public int publicationYear;

  @JsonIgnore
  public String genre;
}

static class BookList {
  public List<Book> books;
}

void main() {}
```

Ringkasan anotasi:

- `@JsonClassDescription`: Tambahkan deskripsi ke kelas
- `@JsonPropertyDescription`: Tambahkan deskripsi ke field atau metode getter
- `@JsonIgnore`: Kecualikan field `public` atau getter dari skema
- `@JsonProperty`: Sertakan field atau getter non-`public` dalam skema

Jika Anda menggunakan `@JsonProperty(required = false)`, SDK mengabaikan nilai `false`. Skema JSON Anthropic harus menandai semua properti sebagai diperlukan.

Anda juga dapat menggunakan anotasi OpenAPI Swagger 2 `@Schema` dan `@ArraySchema` untuk batasan khusus tipe:

```java hidelines={-2..}
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Schema;

static class Article {

  @ArraySchema(minItems = 1)
  public List<String> authors;

  public String title;

  @Schema(format = "date")
  public String publicationDate;

  @Schema(minimum = "1")
  public int pageCount;
}

void main() {}
```

Validasi lokal memeriksa bahwa Anda belum menggunakan kata kunci batasan yang tidak didukung, tetapi nilai batasan tidak divalidasi secara lokal. Misalnya, nilai `"format"` yang tidak didukung mungkin lulus validasi lokal tetapi menyebabkan kesalahan jarak jauh.

Jika Anda menggunakan anotasi Jackson dan Swagger untuk menetapkan field skema yang sama, anotasi Jackson memiliki prioritas.

</section>

<section title="Mendefinisikan skema tanpa kelas Java">

Derivasi skema berbasis kelas adalah jalur paling nyaman, tetapi untuk kontrol langsung atas struktur skema Anda dapat membangun `JsonOutputFormat.Schema` secara manual dan membungkusnya dalam `OutputConfig`.

```java hidelines={1..2,5..6}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.JsonOutputFormat;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.OutputConfig;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    JsonOutputFormat.Schema schema = JsonOutputFormat.Schema.builder()
        .putAdditionalProperty("type", JsonValue.from("object"))
        .putAdditionalProperty("properties", JsonValue.from(Map.of(
            "name", Map.of("type", "string"),
            "email", Map.of("type", "string"),
            "plan_interest", Map.of("type", "string"))))
        .putAdditionalProperty("required", JsonValue.from(
            List.of("name", "email", "plan_interest")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    OutputConfig outputConfig = OutputConfig.builder()
        .format(JsonOutputFormat.builder().schema(schema).build())
        .build();

    MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024)
        .outputConfig(outputConfig)
        .addUserMessage(
            "John Smith (john@example.com) is interested in our Enterprise plan.")
        .build();

    client.messages().create(createParams).content().stream()
        .flatMap(contentBlock -> contentBlock.text().stream())
        .forEach(textBlock -> IO.println(textBlock.text()));
}
```

Untuk contoh yang lebih luas yang membangun skema bersarang dengan array dan deskripsi, lihat [`StructuredOutputsRawExample.java`](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/StructuredOutputsRawExample.java) di repositori SDK.

</section>

</Tab>
<Tab title="PHP">

**Kelas melalui antarmuka `StructuredOutputModel`**

Tentukan kelas PHP yang mengimplementasikan `StructuredOutputModel` (menggunakan `StructuredOutputModelTrait`) dan lewatkan nama kelas ke `outputConfig: ['format' => MyClass::class]`. SDK menurunkan skema JSON dari tipe properti PHP 8 native Anda dan mengembalikan instance yang diketik melalui `$message->parsedOutput()`.

`parsedOutput()` mengembalikan instance model Anda saat berhasil, atau `null` (atau array kesalahan) jika penguraian gagal. Gunakan `instanceof` untuk mempersempit tipe sebelum mengakses field.

```php hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

$client = new Client();

class ContactInfo implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $name;
    public string $email;
    public string $plan_interest;
}

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['format' => ContactInfo::class],
);

$contact = $message->parsedOutput();
if ($contact instanceof ContactInfo) {
    echo "{$contact->name} ({$contact->email})\n";
}
```

<section title="Inferensi tipe">

SDK memetakan tipe properti PHP 8 native ke JSON Schema:

| Tipe PHP | JSON Schema |
|---|---|
| `string` | `"string"` |
| `int` | `"integer"` |
| `float` | `"number"` |
| `bool` | `"boolean"` |
| `array` | `"array"` (lihat di bawah) |
| `?type` (nullable) | Field opsional |
| Kelas yang mengimplementasikan `StructuredOutputModel` | Objek bersarang |

Untuk properti `array`, SDK menambahkan skema `items` hanya ketika tipe elemen adalah `StructuredOutputModel` bersarang, dideklarasikan melalui `#[Constrained(itemClass: MyModel::class)]` atau docblock `/** @var MyModel[] */`. Array skalar (`string[]`, `int[]`) memancarkan `{"type":"array"}` tanpa batasan.

Semua properti non-nullable menjadi field yang diperlukan.

</section>

<section title="Batasan melalui atribut #[Constrained]">

Tambahkan batasan dengan atribut `#[Constrained]`:

```php hidelines={..2} highlight={3}
<?php

use Anthropic\Lib\Attributes\Constrained;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

class Address implements StructuredOutputModel { use StructuredOutputModelTrait; public string $street; }

class Profile implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    #[Constrained(description: 'Age in years', minimum: 0, maximum: 150)]
    public int $age;

    #[Constrained(format: 'email')]
    public string $email;

    #[Constrained(itemClass: Address::class, minItems: 1)]
    public array $addresses;
}
```

**Batasan yang diberlakukan API** (dikirim dalam skema): `description`, `format`, `const`, `itemClass`, `minItems` (0 atau 1 saja).

**Batasan yang divalidasi SDK** (dihapus dari skema wire, ditambahkan ke deskripsi, dan divalidasi terhadap respons): `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`.

</section>

<section title="Fallback skema JSON mentah">

Untuk skema yang tidak dapat diekspresikan oleh petunjuk tipe PHP, lewatkan array asosiatif mentah melalui `OutputConfig::with()`. Jalur ini melewatkan helper `parsedOutput()`; decode respons dengan `json_decode()`:

```php hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Messages\OutputConfig;
use Anthropic\Messages\JSONOutputFormat;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
    ],
    model: 'claude-opus-4-7',
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

$contact = json_decode($message->content[0]->text, associative: true);
echo "{$contact['name']} ({$contact['email']})\n";
```

</section>

</Tab>
<Tab title="Ruby">

**`output_config: {format: Model}` dengan `parsed_output`**

Tentukan kelas model yang memperluas `Anthropic::BaseModel` dan lewatkan sebagai format ke `messages.create()`. Respons menyertakan atribut `parsed_output` dengan objek Ruby yang diketik.

```ruby hidelines={1..2}
require "anthropic"

class ContactInfo < Anthropic::BaseModel
  required :name, String
  required :email, String
  required :plan_interest, String
end

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
    }
  ],
  output_config: {format: ContactInfo}
)

contact = message.parsed_output
puts "#{contact.name} (#{contact.email})"
```

<section title="Fitur model lanjutan">

SDK Ruby mendukung fitur definisi model tambahan untuk skema yang lebih kaya:

- **Kata kunci `doc:`:** Tambahkan deskripsi ke field untuk output skema yang lebih informatif
- **`Anthropic::ArrayOf[T]`:** Array yang diketik. Lewatkan batasan tingkat array (`min_items:`, `max_items:`) sebagai kata kunci pada `required`/`optional`, bukan pada `ArrayOf` itu sendiri
- **`Anthropic::EnumOf[:a, :b]`:** Field enum dengan nilai terbatas
- **`Anthropic::UnionOf[T1, T2]`:** Tipe union dipetakan ke `anyOf`

```ruby
class FamousNumber < Anthropic::BaseModel
  required :value, Float
  optional :reason, String, doc: "why is this number mathematically significant?"
end

class Output < Anthropic::BaseModel
  required :numbers, Anthropic::ArrayOf[FamousNumber], min_items: 3, max_items: 5
end

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [{role: "user", content: "give me some famous numbers"}],
  output_config: {format: Output}
)

message.parsed_output
# => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi is...">...]>
```

</section>

</Tab>
</Tabs>

#### Cara kerja transformasi SDK

SDK Python, TypeScript, Ruby, dan PHP secara otomatis mengubah skema dengan fitur yang tidak didukung:

1. **Hapus batasan yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Perbarui deskripsi** dengan informasi batasan (misalnya, "Harus minimal 100"), ketika batasan tidak langsung didukung dengan output terstruktur
3. **Tambahkan `additionalProperties: false`** ke semua objek
4. **Filter format string** ke daftar yang didukung saja
5. **Validasi respons** terhadap skema asli Anda (dengan semua batasan)

Ini berarti Claude menerima skema yang disederhanakan, tetapi kode Anda masih memberlakukan semua batasan melalui validasi.

**Contoh:** Field Pydantic dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, tetapi SDK memperbarui deskripsi menjadi "Harus minimal 100" dan memvalidasi respons terhadap batasan asli.

### Kasus penggunaan umum

<section title="Ekstraksi data">

Ekstrak data terstruktur dari teks tidak terstruktur:

<CodeGroup>

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' --format jsonl <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
messages:
  - role: user
    content: "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        invoice_number: {type: string}
        date: {type: string}
        total_amount: {type: number}
        line_items:
          type: array
          items: {type: object, additionalProperties: false}
        customer_name: {type: string}
      required: [invoice_number, date, total_amount, line_items, customer_name]
      additionalProperties: false
YAML
```

```python Python hidelines={1}
import anthropic
from pydantic import BaseModel


class Invoice(BaseModel):
    invoice_number: str
    date: str
    total_amount: float
    line_items: list[dict]
    customer_name: str


client = anthropic.Anthropic()
invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

response = client.messages.parse(
    model="claude-opus-4-7",
    max_tokens=4096,
    output_format=Invoice,
    messages=[
        {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
    ],
)

print(response.parsed_output)
```

```typescript TypeScript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const client = new Anthropic();

const InvoiceSchema = z.object({
  invoice_number: z.string(),
  date: z.string(),
  total_amount: z.number(),
  line_items: z.array(z.record(z.string(), z.any())),
  customer_name: z.string()
});

const invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";
const response = await client.messages.parse({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  output_config: { format: zodOutputFormat(InvoiceSchema) },
  messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
});
console.log(response.parsed_output);
```

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

string invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 4096,
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    invoice_number = new { type = "string" },
                    date = new { type = "string" },
                    total_amount = new { type = "number" },
                    line_items = new
                    {
                        type = "array",
                        items = new
                        {
                            type = "object",
                            additionalProperties = false,
                        },
                    },
                    customer_name = new { type = "string" },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "invoice_number", "date", "total_amount", "line_items", "customer_name" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
    Messages = [new() { Role = Role.User, Content = $"Extract invoice data from: {invoiceText}" }]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
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

	invoiceText := "Invoice #12345, Date: 2024-01-15, Total: $500.00"

	schema := map[string]any{
		"type":                 "object",
		"additionalProperties": false,
		"properties": map[string]any{
			"invoice_number": map[string]any{"type": "string"},
			"date":           map[string]any{"type": "string"},
			"total_amount":   map[string]any{"type": "number"},
			"line_items": map[string]any{
				"type": "array",
				"items": map[string]any{
					"type":                 "object",
					"additionalProperties": false,
					"properties": map[string]any{
						"description": map[string]any{"type": "string"},
						"quantity":    map[string]any{"type": "number"},
						"unit_price":  map[string]any{"type": "number"},
					},
					"required": []string{"description", "quantity", "unit_price"},
				},
			},
			"customer_name": map[string]any{"type": "string"},
		},
		"required": []string{"invoice_number", "date", "total_amount", "line_items", "customer_name"},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 4096,
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: schema,
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Extract invoice data from: %s", invoiceText))),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.TextBlock:
			fmt.Println(variant.Text)
		}
	}
}
```

```java Java hidelines={1..6}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;

static class LineItem {
    @JsonProperty("description")
    public String description;

    @JsonProperty("quantity")
    public int quantity;

    @JsonProperty("unit_price")
    public double unitPrice;
}

static class Invoice {
    @JsonProperty("invoice_number")
    public String invoiceNumber;

    @JsonProperty("date")
    public String date;

    @JsonProperty("total_amount")
    public double totalAmount;

    @JsonProperty("line_items")
    public List<LineItem> lineItems;

    @JsonProperty("customer_name")
    public String customerName;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    String invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

    StructuredMessageCreateParams<Invoice> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(4096L)
        .outputConfig(Invoice.class)
        .addUserMessage("Extract invoice data from: " + invoiceText)
        .build();

    StructuredMessage<Invoice> response = client.messages().create(params);
    Invoice invoice = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(invoice.invoiceNumber + ": $" + invoice.totalAmount);
}
```

```php PHP hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

$client = new Client();

class Invoice implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $invoice_number;
    public string $date;
    public float $total_amount;
    public array $line_items;
    public string $customer_name;
}

$invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => "Extract invoice data from: $invoiceText"]
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['format' => Invoice::class],
);

$invoice = $message->parsedOutput();
if ($invoice instanceof Invoice) {
    echo "Invoice {$invoice->invoice_number}: \${$invoice->total_amount}\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

class LineItem < Anthropic::BaseModel
  required :description, String
  required :amount, Float
end

class Invoice < Anthropic::BaseModel
  required :invoice_number, String
  required :date, String
  required :total_amount, Float
  required :line_items, Anthropic::ArrayOf[LineItem]
  required :customer_name, String
end

invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  output_config: {format: Invoice},
  messages: [
    {role: "user", content: "Extract invoice data from: #{invoice_text}"}
  ]
)

invoice = message.parsed_output
puts "Invoice #{invoice.invoice_number}: $#{invoice.total_amount}"
```

</CodeGroup>

</section>

<section title="Klasifikasi">

Klasifikasikan konten dengan kategori terstruktur:

<CodeGroup>

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' --format jsonl <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
messages:
  - role: user
    content: "Classify this feedback: Great product, fast shipping!"
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        category:
          type: string
        confidence:
          type: number
        tags:
          type: array
          items:
            type: string
        sentiment:
          type: string
      required:
        - category
        - confidence
        - tags
        - sentiment
      additionalProperties: false
YAML
```

```python Python hidelines={1}
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()


class Classification(BaseModel):
    category: str
    confidence: float
    tags: list[str]
    sentiment: str


feedback_text = "Great product, but the delivery was slow."
response = client.messages.parse(
    model="claude-opus-4-7",
    max_tokens=1024,
    output_format=Classification,
    messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
)

print(response.parsed_output)
```

```typescript TypeScript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const client = new Anthropic();

const ClassificationSchema = z.object({
  category: z.string(),
  confidence: z.number(),
  tags: z.array(z.string()),
  sentiment: z.string()
});

const feedbackText = "Great product, but the delivery was slow.";
const response = await client.messages.parse({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  output_config: { format: zodOutputFormat(ClassificationSchema) },
  messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
});

console.log(response.parsed_output);
```

```csharp C# hidelines={1..6}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

string feedbackText = "Great product, fast shipping!";

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = $"Classify this feedback: {feedbackText}" }],
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    category = new { type = "string" },
                    confidence = new { type = "number" },
                    tags = new { type = "array", items = new { type = "string" } },
                    sentiment = new { type = "string" },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "category", "confidence", "tags", "sentiment" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go hidelines={1..14,-1}
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	feedbackText := "Great product, fast shipping!"

	schema := map[string]any{
		"type": "object",
		"properties": map[string]any{
			"category":   map[string]any{"type": "string"},
			"confidence": map[string]any{"type": "number"},
			"tags":       map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
			"sentiment":  map[string]any{"type": "string"},
		},
		"required":             []string{"category", "confidence", "tags", "sentiment"},
		"additionalProperties": false,
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: schema,
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Classify this feedback: %s", feedbackText))),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.TextBlock:
			var result map[string]any
			json.Unmarshal([]byte(variant.Text), &result)
			fmt.Println(result)
		}
	}
}
```

```java Java hidelines={1..6}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;

static class Classification {
    @JsonProperty("category")
    public String category;

    @JsonProperty("confidence")
    public double confidence;

    @JsonProperty("tags")
    public List<String> tags;

    @JsonProperty("sentiment")
    public String sentiment;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    String feedbackText = "Great product, fast shipping!";

    StructuredMessageCreateParams<Classification> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .outputConfig(Classification.class)
        .addUserMessage("Classify this feedback: " + feedbackText)
        .build();

    StructuredMessage<Classification> response = client.messages().create(params);
    Classification result = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(result.category + " (" + result.confidence + ")");
}
```

```php PHP hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

$client = new Client();

class Classification implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $category;
    public float $confidence;
    public array $tags;
    public string $sentiment;
}

$feedbackText = "Great product, fast shipping!";

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['format' => Classification::class],
);

$result = $message->parsedOutput();
if ($result instanceof Classification) {
    echo "{$result->category} ({$result->confidence}): {$result->sentiment}\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

class Classification < Anthropic::BaseModel
  required :category, String
  required :confidence, Float
  required :tags, Anthropic::ArrayOf[String]
  required :sentiment, String
end

feedback_text = "Great product, fast shipping!"

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  output_config: {format: Classification},
  messages: [
    {role: "user", content: "Classify this feedback: #{feedback_text}"}
  ]
)
puts message.parsed_output
```

</CodeGroup>

</section>

<section title="Pemformatan respons API">

Hasilkan respons siap API:

<CodeGroup>

```bash CLI
ant messages create \
  --transform 'content.0.text' --format yaml <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        status:
          type: string
        data:
          type: object
          additionalProperties: false
        errors:
          type: array
          items:
            type: object
            additionalProperties: false
        metadata:
          type: object
          additionalProperties: false
      required:
        - status
        - data
        - metadata
      additionalProperties: false
messages:
  - role: user
    content: "Process this request: ..."
YAML
```

```python Python hidelines={1}
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()


class APIResponse(BaseModel):
    status: str
    data: dict
    errors: list[dict] | None
    metadata: dict


response = client.messages.parse(
    model="claude-opus-4-7",
    max_tokens=1024,
    output_format=APIResponse,
    messages=[{"role": "user", "content": "Process this request: ..."}],
)

print(response.parsed_output)
```

```typescript TypeScript hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const client = new Anthropic();

const APIResponseSchema = z.object({
  status: z.string(),
  data: z.record(z.string(), z.any()),
  errors: z.array(z.record(z.string(), z.any())).optional(),
  metadata: z.record(z.string(), z.any())
});

const response = await client.messages.parse({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  output_config: { format: zodOutputFormat(APIResponseSchema) },
  messages: [{ role: "user", content: "Process this request..." }]
});

console.log(response.parsed_output);
```

```csharp C# hidelines={1..6}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Process this request: ..." }],
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    status = new { type = "string" },
                    data = new { type = "object", additionalProperties = false },
                    errors = new
                    {
                        type = "array",
                        items = new { type = "object", additionalProperties = false },
                    },
                    metadata = new { type = "object", additionalProperties = false },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "status", "data", "metadata" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: map[string]any{
					"type":                 "object",
					"additionalProperties": false,
					"properties": map[string]any{
						"status": map[string]any{
							"type": "string",
						},
						"data": map[string]any{
							"type":                 "object",
							"additionalProperties": false,
						},
						"errors": map[string]any{
							"type": "array",
							"items": map[string]any{
								"type":                 "object",
								"additionalProperties": false,
							},
						},
						"metadata": map[string]any{
							"type":                 "object",
							"additionalProperties": false,
						},
					},
					"required": []string{"status", "data", "metadata"},
				},
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Process this request: ...")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.TextBlock:
			fmt.Println(variant.Text)
		}
	}
}
```

```java Java hidelines={1..6}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;

static class APIData {
    @JsonProperty("message")
    public String message;

    @JsonProperty("resource_id")
    public String resourceId;
}

static class APIError {
    @JsonProperty("code")
    public String code;

    @JsonProperty("message")
    public String message;
}

static class APIMetadata {
    @JsonProperty("request_id")
    public String requestId;

    @JsonProperty("timestamp")
    public String timestamp;
}

static class APIResponse {
    @JsonProperty("status")
    public String status;

    @JsonProperty("data")
    public APIData data;

    @JsonProperty("errors")
    public List<APIError> errors;

    @JsonProperty("metadata")
    public APIMetadata metadata;
}

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    StructuredMessageCreateParams<APIResponse> params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .outputConfig(APIResponse.class)
        .addUserMessage("Process this request: ...")
        .build();

    StructuredMessage<APIResponse> response = client.messages().create(params);
    APIResponse result = response.content().stream()
        .flatMap(block -> block.text().stream())
        .findFirst().orElseThrow().text();
    IO.println(result.status);
}
```

```php PHP hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Attributes\Constrained;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;

$client = new Client();

class Payload implements StructuredOutputModel { use StructuredOutputModelTrait; public string $message; }

class APIError implements StructuredOutputModel { use StructuredOutputModelTrait; public string $code; public string $detail; }

class Metadata implements StructuredOutputModel { use StructuredOutputModelTrait; public string $request_id; }

class APIResponse implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $status;
    public Payload $data;
    #[Constrained(itemClass: APIError::class)]
    public ?array $errors;
    public Metadata $metadata;
}

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Process this request: ...']
    ],
    model: 'claude-opus-4-7',
    outputConfig: ['format' => APIResponse::class],
);

$result = $message->parsedOutput();
if ($result instanceof APIResponse) {
    echo "{$result->status}: {$result->data->message}\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

class Payload < Anthropic::BaseModel
  required :message, String
end

class APIError < Anthropic::BaseModel
  required :code, String
  required :detail, String
end

class Metadata < Anthropic::BaseModel
  required :request_id, String
end

class APIResponse < Anthropic::BaseModel
  required :status, String
  required :data, Payload
  optional :errors, Anthropic::ArrayOf[APIError]
  required :metadata, Metadata
end

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  output_config: {format: APIResponse},
  messages: [
    {role: "user", content: "Process this request: ..."}
  ]
)
puts message.parsed_output
```

</CodeGroup>

</section>

## Penggunaan alat yang ketat

Untuk menegakkan kepatuhan JSON Schema pada input alat dengan pengambilan sampel yang dibatasi tata bahasa, lihat [Penggunaan alat yang ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use).

## Menggunakan kedua fitur bersama-sama

Output JSON dan penggunaan alat ketat menyelesaikan masalah yang berbeda dan bekerja bersama:

- **Output JSON** mengontrol format respons Claude (apa yang Claude katakan)
- **Penggunaan alat ketat** memvalidasi parameter alat (bagaimana Claude memanggil fungsi Anda)

Ketika digabungkan, Claude dapat memanggil alat dengan parameter yang dijamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agentic di mana Anda memerlukan panggilan alat yang andal dan output akhir yang terstruktur.

<CodeGroup>

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
messages:
  - role: user
    content: Help me plan a trip to Paris departing May 15, 2026
# JSON outputs: structured response format
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        summary:
          type: string
        next_steps:
          type: array
          items:
            type: string
      required: [summary, next_steps]
      additionalProperties: false
# Strict tool use: guaranteed tool parameters
tools:
  - name: search_flights
    strict: true
    input_schema:
      type: object
      properties:
        destination:
          type: string
        date:
          type: string
          format: date
      required: [destination, date]
      additionalProperties: false
YAML
```

```python Python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Help me plan a trip to Paris departing May 15, 2026",
        }
    ],
    # JSON outputs: structured response format
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
    # Strict tool use: guaranteed tool parameters
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

print(response)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Help me plan a trip to Paris departing May 15, 2026" }],
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
  tools: [
    {
      name: "search_flights",
      description: "Search for available flights to a destination on a specific date",
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

// Claude may call the tool first (tool_use) or respond with JSON (text)
console.log("Stop reason:", response.stop_reason);
for (const block of response.content) {
  if (block.type === "tool_use") {
    console.log(`Tool call: ${block.name}(${JSON.stringify(block.input)})`);
  } else if (block.type === "text") {
    console.log("Response:", block.text);
  }
}
```

```csharp C# hidelines={1..6}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Help me plan a trip to Paris departing May 15, 2026" }],
    // JSON outputs: structured response format
    OutputConfig = new OutputConfig
    {
        Format = new JsonOutputFormat
        {
            Schema = new Dictionary<string, JsonElement>
            {
                ["type"] = JsonSerializer.SerializeToElement("object"),
                ["properties"] = JsonSerializer.SerializeToElement(new
                {
                    summary = new { type = "string" },
                    next_steps = new { type = "array", items = new { type = "string" } },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "summary", "next_steps" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            },
        },
    },
    // Strict tool use: guaranteed tool parameters
    Tools =
    [
        new Tool
        {
            Name = "search_flights",
            Strict = true,
            InputSchema = new InputSchema(new Dictionary<string, JsonElement>
            {
                ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                {
                    ["destination"] = new { type = "string" },
                    ["date"] = new { type = "string", format = "date" },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "date" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            }),
        }
    ],
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip to Paris departing May 15, 2026")),
		},
		// JSON outputs: structured response format
		OutputConfig: anthropic.OutputConfigParam{
			Format: anthropic.JSONOutputFormatParam{
				Schema: map[string]any{
					"type":                 "object",
					"additionalProperties": false,
					"properties": map[string]any{
						"summary":    map[string]any{"type": "string"},
						"next_steps": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
					},
					"required": []string{"summary", "next_steps"},
				},
			},
		},
		// Strict tool use: guaranteed tool parameters
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:   "search_flights",
				Strict: anthropic.Bool(true),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"destination": map[string]any{"type": "string"},
						"date":        map[string]any{"type": "string", "format": "date"},
					},
					Required: []string{"destination", "date"},
					ExtraFields: map[string]any{
						"additionalProperties": false,
					},
				}}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content)
}
```

```java Java hidelines={1..12,53}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.JsonOutputFormat;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.OutputConfig;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // JSON outputs: structured response format
    JsonOutputFormat.Schema outputSchema = JsonOutputFormat.Schema.builder()
        .putAdditionalProperty("type", JsonValue.from("object"))
        .putAdditionalProperty("properties", JsonValue.from(Map.of(
            "summary", Map.of("type", "string"),
            "next_steps", Map.of("type", "array", "items", Map.of("type", "string"))
        )))
        .putAdditionalProperty("required", JsonValue.from(List.of("summary", "next_steps")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    // Strict tool use: guaranteed tool parameters
    InputSchema toolSchema = InputSchema.builder()
        .properties(JsonValue.from(Map.of(
            "destination", Map.of("type", "string"),
            "date", Map.of("type", "string", "format", "date")
        )))
        .putAdditionalProperty("required", JsonValue.from(List.of("destination", "date")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .addUserMessage("Help me plan a trip to Paris departing May 15, 2026")
        .outputConfig(OutputConfig.builder()
            .format(JsonOutputFormat.builder().schema(outputSchema).build())
            .build())
        .addTool(Tool.builder()
            .name("search_flights")
            .description("Search for available flights to a destination on a specific date")
            .strict(true)
            .inputSchema(toolSchema)
            .build())
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..3}
<?php

use Anthropic\Client;
use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
use Anthropic\Lib\Contracts\StructuredOutputModel;
use Anthropic\Messages\ToolUseBlock;

$client = new Client();

class TripPlan implements StructuredOutputModel
{
    use StructuredOutputModelTrait;

    public string $summary;
    public array $next_steps;
}

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Help me plan a trip to Paris departing May 15, 2026']
    ],
    model: 'claude-opus-4-7',
    // JSON outputs: structured response format
    outputConfig: ['format' => TripPlan::class],
    // Strict tool use: guaranteed tool parameters
    tools: [
        [
            'name' => 'search_flights',
            'strict' => true,
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'destination' => ['type' => 'string'],
                    'date' => ['type' => 'string', 'format' => 'date']
                ],
                'required' => ['destination', 'date'],
                'additionalProperties' => false
            ]
        ]
    ],
);

// Claude may call the tool first (tool_use) or respond with JSON (text)
$plan = $message->parsedOutput();
if ($plan instanceof TripPlan) {
    echo $plan->summary, "\n";
} elseif ($toolUse = array_find($message->content, fn($block) => $block instanceof ToolUseBlock)) {
    echo "Tool call: {$toolUse->name}(", json_encode($toolUse->input), ")\n";
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    {role: "user", content: "Help me plan a trip to Paris departing May 15, 2026"}
  ],
  # JSON outputs: structured response format
  output_config: {
    format: {
      type: :json_schema,
      schema: {
        type: "object",
        properties: {
          summary: {type: "string"},
          next_steps: {type: "array", items: {type: "string"}}
        },
        required: ["summary", "next_steps"],
        additionalProperties: false
      }
    }
  },
  # Strict tool use: guaranteed tool parameters
  tools: [
    {
      name: "search_flights",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          destination: {type: "string"},
          date: {type: "string", format: "date"}
        },
        required: ["destination", "date"],
        additionalProperties: false
      }
    }
  ]
)
puts message
```

</CodeGroup>

## Pertimbangan penting

### Kompilasi tata bahasa dan caching

Output terstruktur menggunakan pengambilan sampel terbatas dengan artefak tata bahasa yang dikompilasi. Ini memperkenalkan beberapa karakteristik kinerja yang perlu diperhatikan:

- **Latensi permintaan pertama:** Pertama kali Anda menggunakan skema tertentu, ada latensi tambahan saat tata bahasa dikompilasi
- **Caching otomatis:** Tata bahasa yang dikompilasi di-cache selama 24 jam dari penggunaan terakhir, membuat permintaan berikutnya jauh lebih cepat
- **Invalidasi cache:** Cache dibatalkan jika Anda mengubah:
  - Struktur skema JSON
  - Set alat dalam permintaan Anda (saat menggunakan output terstruktur dan penggunaan alat bersama-sama)
  - Mengubah hanya bidang `name` atau `description` tidak membatalkan cache

### Modifikasi prompt dan biaya token

Saat menggunakan output terstruktur, Claude secara otomatis menerima prompt sistem tambahan yang menjelaskan format output yang diharapkan. Ini berarti:

- Jumlah token input Anda sedikit lebih tinggi
- Prompt yang disuntikkan menghabiskan token Anda seperti prompt sistem lainnya
- Mengubah parameter `output_config.format` akan membatalkan [prompt cache](/docs/id/build-with-claude/prompt-caching) apa pun untuk utas percakapan tersebut

### Batasan JSON Schema

Output terstruktur mendukung JSON Schema standar dengan beberapa batasan. Baik output JSON maupun penggunaan alat ketat berbagi batasan ini.

<section title="Fitur yang didukung">

- Semua tipe dasar: object, array, string, integer, number, boolean, null
- `enum` (hanya string, angka, bool, atau null - tidak ada tipe kompleks)
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
- Eksternal `$ref` (misalnya, `'$ref': 'http://...'`)
- Batasan numerik (`minimum`, `maximum`, `multipleOf`, dll.)
- Batasan string (`minLength`, `maxLength`)
- Batasan array di luar `minItems` dari 0 atau 1
- `additionalProperties` diatur ke apa pun selain `false`

Jika Anda menggunakan fitur yang tidak didukung, Anda akan menerima kesalahan 400 dengan detail.

</section>

<section title="Dukungan pola (regex)">

**Fitur regex yang didukung:**
- Pencocokan penuh (`^...$`) dan pencocokan parsial
- Kuantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
- Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
- Grup: `(...)`

**TIDAK didukung:**
- Backreferences ke grup (misalnya, `\1`, `\2`)
- Pernyataan lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
- Batas kata: `\b`, `\B`
- Kuantifier `{n,m}` kompleks dengan rentang besar

Pola regex sederhana bekerja dengan baik. Pola kompleks dapat menghasilkan kesalahan 400.

</section>

<Tip>
SDK Python, TypeScript, Ruby, dan PHP dapat secara otomatis mengubah skema dengan fitur yang tidak didukung dengan menghapusnya dan menambahkan batasan ke deskripsi bidang. Lihat [metode khusus SDK](#sdk-specific-methods) untuk detail.
</Tip>

### Pengurutan properti

Saat menggunakan output terstruktur, properti dalam objek mempertahankan pengurutan yang ditentukan dari skema Anda, dengan satu peringatan penting: **properti yang diperlukan muncul terlebih dahulu, diikuti oleh properti opsional**.

Misalnya, diberikan skema ini:

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

Jika urutan properti dalam output penting untuk aplikasi Anda, tandai semua properti sebagai diperlukan, atau pertimbangkan pengurutan ulang ini dalam logika parsing Anda.

### Output tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam sebagian besar kasus, ada skenario di mana output mungkin tidak cocok dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan properti keselamatan dan kegunaannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keselamatan:

- Respons memiliki `stop_reason: "refusal"`
- Anda akan menerima kode status 200
- Anda akan ditagih untuk token yang dihasilkan
- Output mungkin tidak cocok dengan skema Anda karena pesan penolakan mengambil alih batasan skema

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons terpotong karena mencapai batas `max_tokens`:

- Respons memiliki `stop_reason: "max_tokens"`
- Output mungkin tidak lengkap dan tidak cocok dengan skema Anda
- Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap

### Batasan kompleksitas skema

Output terstruktur bekerja dengan mengkompilasi skema JSON Anda menjadi tata bahasa yang membatasi output Claude. Skema yang lebih kompleks menghasilkan tata bahasa yang lebih besar yang membutuhkan waktu lebih lama untuk dikompilasi. Untuk melindungi dari waktu kompilasi yang berlebihan, API memberlakukan beberapa batasan kompleksitas.

#### Batasan eksplisit

Batasan berikut berlaku untuk semua permintaan dengan `output_config.format` atau `strict: true`:

| Batasan | Nilai | Deskripsi |
|-------|-------|-------------|
| Alat ketat per permintaan | 20 | Jumlah maksimum alat dengan `strict: true`. Alat non-ketat tidak dihitung menuju batasan ini. |
| Parameter opsional | 24 | Total parameter opsional di semua skema alat ketat dan skema output JSON. Setiap parameter yang tidak tercantum dalam `required` dihitung menuju batasan ini. |
| Parameter dengan tipe union | 16 | Total parameter yang menggunakan `anyOf` atau array tipe (misalnya, `"type": ["string", "null"]`) di semua skema ketat. Ini sangat mahal karena menciptakan biaya kompilasi eksponensial. |

<Note>
Batasan ini berlaku untuk total gabungan di semua skema ketat dalam satu permintaan. Misalnya, jika Anda memiliki 4 alat ketat dengan 6 parameter opsional masing-masing, Anda akan mencapai batas parameter 24 meskipun tidak ada alat tunggal yang tampak kompleks.
</Note>

#### Batasan internal tambahan

Di luar batasan eksplisit di atas, ada batasan internal tambahan pada ukuran tata bahasa yang dikompilasi. Batasan ini ada karena kompleksitas skema tidak berkurang menjadi dimensi tunggal: fitur seperti parameter opsional, tipe union, objek bersarang, dan jumlah alat berinteraksi satu sama lain dengan cara yang dapat membuat tata bahasa yang dikompilasi secara tidak proporsional besar.

Ketika batasan ini terlampaui, Anda akan menerima kesalahan 400 dengan pesan "Schema is too complex for compilation." Kesalahan ini berarti kompleksitas gabungan skema Anda melebihi apa yang dapat dikompilasi secara efisien, bahkan jika setiap batasan individual di atas terpenuhi. Sebagai penghenti terakhir, API juga memberlakukan **waktu tunggu kompilasi 180 detik**. Skema yang melewati semua pemeriksaan eksplisit tetapi menghasilkan tata bahasa yang dikompilasi sangat besar mungkin mencapai waktu tunggu ini.

#### Tips untuk mengurangi kompleksitas skema

Jika Anda mencapai batasan kompleksitas, coba strategi ini secara berurutan:

1. **Tandai hanya alat penting sebagai ketat.** Jika Anda memiliki banyak alat, cadangkan untuk alat di mana pelanggaran skema menyebabkan masalah nyata, dan andalkan kepatuhan alami Claude untuk alat yang lebih sederhana.

2. **Kurangi parameter opsional.** Buat parameter `required` jika memungkinkan. Setiap parameter opsional kira-kira menggandakan sebagian dari ruang keadaan tata bahasa. Jika parameter selalu memiliki default yang masuk akal, pertimbangkan untuk membuatnya diperlukan dan memiliki Claude memberikan default itu secara eksplisit.

3. **Sederhanakan struktur bersarang.** Objek bersarang dalam dengan bidang opsional menambah kompleksitas. Ratakan struktur jika memungkinkan.

4. **Pisahkan menjadi beberapa permintaan.** Jika Anda memiliki banyak alat ketat, pertimbangkan untuk membaginya di seluruh permintaan terpisah atau sub-agen.

Untuk masalah berkelanjutan dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan definisi skema Anda.

## Retensi data

Prompt dan respons diproses dengan ZDR saat menggunakan output terstruktur. Namun, skema JSON itu sendiri disimpan dalam cache sementara selama hingga 24 jam sejak penggunaan terakhir untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan di luar respons API.

Output terstruktur memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi skema JSON**. API mengkompilasi skema JSON menjadi tata bahasa yang disimpan dalam cache terpisah dari konten pesan, dan skema yang disimpan dalam cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti skema, nilai `enum`, nilai `const`, atau ekspresi reguler `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana dilindungi di bawah perlindungan HIPAA.

Untuk kelayakan ZDR dan HIPAA di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

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
**Cakupan tata bahasa**: Tata bahasa hanya berlaku untuk output langsung Claude, bukan untuk panggilan penggunaan alat, hasil alat, atau tag pemikiran (saat menggunakan [Extended Thinking](/docs/id/build-with-claude/extended-thinking)). Status tata bahasa direset di antara bagian, memungkinkan Claude berpikir bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>