---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/structured-outputs
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 53e5d57ec28718db242965fe4c87dca4b6c04ae6acb0737fca6236d53b4947ae
---

# Output terstruktur

Dapatkan hasil JSON yang divalidasi dari alur kerja agen

---

Output terstruktur membatasi respons Claude untuk mengikuti skema tertentu, memastikan output yang valid dan dapat diurai untuk pemrosesan hilir. Dua fitur yang saling melengkapi tersedia:

- **Output JSON** (`output_config.format`): Dapatkan respons Claude dalam format JSON tertentu
- **Penggunaan alat ketat** (`strict: true`): Jamin validasi skema pada nama alat dan input

Fitur-fitur ini dapat digunakan secara independen atau bersama-sama dalam permintaan yang sama.

<Note>
Output terstruktur secara umum tersedia di Claude API dan Amazon Bedrock untuk [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Output terstruktur dalam beta di Microsoft Foundry. Output terstruktur tidak didukung di Google Cloud's Vertex AI untuk Claude Mythos Preview.
</Note>

<Note>
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Tip>
**Bermigrasi dari beta?** Parameter `output_format` telah dipindahkan ke `output_config.format`, dan header beta tidak lagi diperlukan. Header beta lama (`structured-outputs-2025-11-13`) dan parameter `output_format` akan terus berfungsi selama periode transisi. Lihat contoh kode di bawah untuk bentuk API yang diperbarui.
</Tip>

## Mengapa menggunakan output terstruktur

Tanpa output terstruktur, Claude dapat menghasilkan respons JSON yang salah bentuk atau input alat yang tidak valid yang merusak aplikasi Anda. Bahkan dengan prompting yang hati-hati, Anda mungkin mengalami:
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

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' \
  --format jsonl <<'YAML'
model: claude-opus-4-6
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

```typescript TypeScript hidelines={1..2}
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
const textBlock = response.content.find((block) => block.type === "text");
if (textBlock && textBlock.type === "text") {
  console.log(textBlock.text);
}
```

```csharp C#
using System.Collections.Generic;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
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

```java Java hidelines={1..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class ContactInfo {
    public String name;
    public String email;
    public String plan_interest;
    public boolean demo_requested;
}

public class StructuredOutputQuickStart {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(1024)
            .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.")
            .outputConfig(ContactInfo.class)
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(params);
        ContactInfo contact = response.content().get(0).asText().text();
        System.out.println(contact.name + " (" + contact.email + ")");
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("ANTHROPIC_API_KEY")
);

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'
        ]
    ],
    model: 'claude-opus-4-6',
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
  <Step title="Analisis respons">
    Respons Claude adalah JSON yang valid sesuai dengan skema Anda, dikembalikan di `response.content[0].text`.
  </Step>
</Steps>

### Bekerja dengan output JSON di SDK

SDK menyediakan helper yang memudahkan bekerja dengan output JSON, termasuk transformasi skema, validasi otomatis, dan integrasi dengan library skema populer.

<Note>
Metode helper SDK (seperti `.parse()` dan integrasi Pydantic/Zod) masih menerima `output_format` sebagai parameter kenyamanan. SDK menangani terjemahan ke `output_config.format` secara internal. Contoh di bawah menunjukkan sintaks helper SDK.
</Note>

#### Menggunakan definisi skema native

Alih-alih menulis skema JSON mentah, Anda dapat menggunakan alat definisi skema yang familiar di bahasa Anda:

- **Python**: Model [Pydantic](https://docs.pydantic.dev/) dengan `client.messages.parse()`
- **TypeScript**: Skema [Zod](https://zod.dev/) dengan `zodOutputFormat()`
- **Java**: Kelas Java biasa dengan derivasi skema otomatis via `outputConfig(Class<T>)`
- **Ruby**: Kelas `Anthropic::BaseModel` dengan `output_config: {format: Model}`
- **CLI**, **C#**, **Go**, **PHP**: Skema JSON mentah dilewatkan via `output_config`

<CodeGroup>

```bash CLI
{ read -r _ NAME; read -r _ EMAIL; } < <(
  ant messages create \
    --transform 'content.0.text|@fromstr|{name,email}' --format yaml <<'YAML'
model: claude-opus-4-6
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

```java Java hidelines={1..7,14..16,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
    public boolean demoRequested;
}

public class NativeSchemaExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(1024)
            .outputConfig(ContactInfo.class)
            .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.")
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(createParams);
        ContactInfo contact = response.content().get(0).asText().text();
        System.out.println(contact.name + " (" + contact.email + ")");
    }
}
```

```php PHP hidelines={1..3,6}
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

</CodeGroup>

#### Metode spesifik SDK

Setiap SDK menyediakan helper yang membuat bekerja dengan output terstruktur lebih mudah. Lihat halaman SDK individual untuk detail lengkap.

<Tabs>
<Tab title="CLI">

**Skema JSON mentah via heredoc body**

CLI melewatkan skema JSON mentah sebagai heredoc body YAML. Gunakan modifier GJSON `@fromstr` dengan `--transform` untuk mengurai string JSON yang dikembalikan dalam `content[0].text` dan memproyeksikan field tertentu.

<section title="Contoh penggunaan">

```bash
ant messages create \
  --transform 'content.0.text|@fromstr|{name,email}' \
  --format yaml <<'YAML'
model: claude-opus-4-6
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

</section>

</Tab>
<Tab title="Python">

**`client.messages.parse()` (Direkomendasikan)**

Metode `parse()` secara otomatis mengubah model Pydantic Anda, memvalidasi respons, dan mengembalikan atribut `parsed_output`.

<section title="Contoh penggunaan">

```python hidelines={2..4,9..12}
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

</section>

**Helper `transform_schema()`**

Untuk ketika Anda perlu secara manual mengubah skema sebelum mengirim, atau ketika Anda ingin memodifikasi skema yang dihasilkan Pydantic. Tidak seperti `client.messages.parse()`, yang mengubah skema yang disediakan secara otomatis, ini memberi Anda skema yang diubah sehingga Anda dapat menyesuaikannya lebih lanjut.

<section title="Contoh penggunaan">

```python nocheck
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

Metode `parse()` menerima skema Zod, memvalidasi respons, dan mengembalikan atribut `parsed_output` dengan tipe TypeScript yang disimpulkan sesuai dengan skema.

<section title="Contoh penggunaan">

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
  model: "claude-opus-4-6",
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

</section>

</Tab>
<Tab title="C#">

**Skema JSON mentah via `OutputConfig`**

SDK C# menggunakan skema JSON mentah yang dibangun secara terprogram dengan `JsonSerializer.SerializeToElement`. Deserialize respons JSON dengan `JsonSerializer.Deserialize`.

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
<Tab title="Go">

**Skema JSON mentah via `OutputConfigParam`**

SDK Go bekerja dengan skema JSON mentah. Tentukan struct Go dengan tag json, hasilkan skema JSON (misalnya, menggunakan `invopop/jsonschema`), dan unmarshal teks respons ke dalam struct Anda.

<section title="Contoh penggunaan">

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

</section>

</Tab>
<Tab title="Java">

**Metode `outputConfig(Class<T>)`**

Lewatkan kelas Java ke `outputConfig()` dan SDK secara otomatis menurunkan skema JSON, memvalidasinya, dan mengembalikan `StructuredMessageCreateParams<T>`. Akses hasil yang diparse via `response.content().get(0).asText().text()`.

<section title="Contoh penggunaan">

```java hidelines={1..7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class ContactInfo {
    public String name;
    public String email;
    public String planInterest;
}

public class StructuredOutputExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(1024)
            .outputConfig(ContactInfo.class)
            .addUserMessage("Extract contact info: John Smith, john@example.com, interested in the Pro plan")
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(createParams);
        ContactInfo contact = response.content().get(0).asText().text();
        System.out.println(contact.name + " (" + contact.email + ")");
    }
}
```

</section>

<section title="Penghapusan tipe generik">

Informasi tipe generik untuk field dipertahankan dalam metadata kelas, tetapi penghapusan tipe generik berlaku dalam cakupan lain. Meskipun skema JSON dapat diturunkan dari field `BookList.books` dengan tipe `List<Book>`, skema JSON yang valid tidak dapat diturunkan dari variabel lokal dari tipe yang sama.

Jika kesalahan terjadi saat mengonversi respons JSON ke instance kelas Java, pesan kesalahan mencakup respons JSON untuk membantu diagnosis. Jika respons JSON Anda mungkin berisi informasi sensitif, hindari mencatat langsung, atau pastikan Anda menyunting detail sensitif apa pun dari pesan kesalahan.

</section>

<section title="Validasi skema lokal">

Output terstruktur mendukung [subset dari bahasa JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Skema dihasilkan secara otomatis dari kelas untuk selaras dengan subset ini. Metode `outputConfig(Class<T>)` melakukan pemeriksaan validasi pada skema yang diturunkan dari kelas yang ditentukan.

Poin kunci:

- **Validasi lokal** terjadi tanpa mengirim permintaan ke model AI jarak jauh.
- **Validasi jarak jauh** juga dilakukan oleh model AI saat menerima skema JSON.
- **Kompatibilitas versi**: Validasi lokal mungkin gagal sementara validasi jarak jauh berhasil jika versi SDK sudah ketinggalan zaman.
- **Menonaktifkan validasi lokal**: Lewatkan `JsonSchemaLocalValidation.NO` jika Anda mengalami masalah kompatibilitas:

```java hidelines={1..2,4..15,22..23}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonSchemaLocalValidation;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;

class BookList {
    public java.util.List<String> books;
}

public class LocalValidationExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(2048)
            .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
            .addUserMessage("List some famous late twentieth century novels.")
            .build();
    }
}
```

</section>

<section title="Streaming">

Output terstruktur juga dapat digunakan dengan streaming. Saat respons tiba dalam event stream, Anda perlu mengumpulkan respons lengkap sebelum deserialize JSON.

Gunakan `BetaMessageAccumulator` untuk mengumpulkan string JSON dari stream. Setelah dikumpulkan, panggil `BetaMessageAccumulator.message(Class<T>)` untuk mengonversi `BetaMessage` yang terakumulasi menjadi `StructuredMessage`, yang secara otomatis mendeserialize JSON ke dalam kelas Java Anda.

</section>

<section title="Properti skema JSON">

Ketika skema JSON diturunkan dari kelas Java Anda, semua properti yang diwakili oleh field `public` atau metode getter `public` disertakan secara default. Field non-`public` dan metode getter dikecualikan.

Anda dapat mengontrol visibilitas dengan anotasi:

- `@JsonIgnore` mengecualikan field `public` atau metode getter
- `@JsonProperty` menyertakan field atau metode getter non-`public`

Jika Anda mendefinisikan field `private` dengan metode getter `public`, nama properti diturunkan dari getter (misalnya, field `private` `myValue` dengan metode `public` `getMyValue()` menghasilkan properti `"myValue"`). Untuk menggunakan nama getter non-konvensional, anotasi metode dengan `@JsonProperty`.

Setiap kelas harus mendefinisikan setidaknya satu properti untuk skema JSON. Kesalahan validasi terjadi jika tidak ada field atau metode getter yang dapat menghasilkan properti skema, seperti ketika:

- Tidak ada field atau metode getter dalam kelas
- Semua anggota `public` dianotasi dengan `@JsonIgnore`
- Semua anggota non-`public` tidak memiliki anotasi `@JsonProperty`
- Field menggunakan tipe `Map`, yang menghasilkan field `"properties"` kosong

</section>

<section title="Anotasi (Jackson dan Swagger)">

Anda dapat menggunakan anotasi Jackson Databind untuk memperkaya skema JSON yang diturunkan dari kelas Java Anda:

```java hidelines={4..5,-2..}
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import java.util.List;

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

public class Example { public static void main(String[] args) {} }
```

Ringkasan anotasi:

- `@JsonClassDescription`: Tambahkan deskripsi ke kelas
- `@JsonPropertyDescription`: Tambahkan deskripsi ke field atau metode getter
- `@JsonIgnore`: Kecualikan field `public` atau getter dari skema
- `@JsonProperty`: Sertakan field atau getter non-`public` dalam skema

Jika Anda menggunakan `@JsonProperty(required = false)`, nilai `false` diabaikan. Skema JSON Anthropic harus menandai semua properti sebagai diperlukan.

Anda juga dapat menggunakan anotasi OpenAPI Swagger 2 `@Schema` dan `@ArraySchema` untuk batasan spesifik tipe:

```java hidelines={3..4,-2..}
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;

class Article {

  @ArraySchema(minItems = 1)
  public List<String> authors;

  public String title;

  @Schema(format = "date")
  public String publicationDate;

  @Schema(minimum = "1")
  public int pageCount;
}

public class Example { public static void main(String[] args) {} }
```

Validasi lokal memeriksa bahwa Anda belum menggunakan kata kunci batasan yang tidak didukung, tetapi nilai batasan tidak divalidasi secara lokal. Misalnya, nilai `"format"` yang tidak didukung mungkin lulus validasi lokal tetapi menyebabkan kesalahan jarak jauh.

Jika Anda menggunakan anotasi Jackson dan Swagger untuk menetapkan field skema yang sama, anotasi Jackson memiliki prioritas.

</section>

</Tab>
<Tab title="PHP">

**Skema JSON mentah via `OutputConfig::with()`**

SDK PHP melewatkan skema JSON mentah sebagai array asosiatif via `OutputConfig::with()`. Decode respons dengan `json_decode()`.

<section title="Contoh penggunaan">

```php hidelines={1..3,6}
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
<Tab title="Ruby">

**`output_config: {format: Model}` dengan `parsed_output`**

Tentukan kelas model yang memperluas `Anthropic::BaseModel` dan lewatkan sebagai format ke `messages.create()`. Respons mencakup atribut `parsed_output` dengan objek Ruby yang diketik.

<section title="Contoh penggunaan">

```ruby hidelines={1..2}
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

</section>

<section title="Fitur model lanjutan">

SDK Ruby mendukung fitur definisi model tambahan untuk skema yang lebih kaya:

- **Kata kunci `doc:`:** Tambahkan deskripsi ke field untuk output skema yang lebih informatif
- **`Anthropic::ArrayOf[T]`:** Array yang diketik dengan batasan `min_length` dan `max_length`
- **`Anthropic::EnumOf[:a, :b]`:** Field enum dengan nilai terbatas
- **`Anthropic::UnionOf[T1, T2]`:** Tipe union dipetakan ke `anyOf`

```ruby
class FamousNumber < Anthropic::BaseModel
  required :value, Float
  optional :reason, String, doc: "why is this number mathematically significant?"
end

class Output < Anthropic::BaseModel
  required :numbers, Anthropic::ArrayOf[FamousNumber], min_length: 3, max_length: 5
end

message = client.messages.create(
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
</Tabs>

#### Cara transformasi SDK bekerja

SDK Python dan TypeScript secara otomatis mengubah skema dengan fitur yang tidak didukung:

1. **Hapus batasan yang tidak didukung** (misalnya, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Perbarui deskripsi** dengan informasi batasan (misalnya, "Harus setidaknya 100"), ketika batasan tidak langsung didukung dengan output terstruktur
3. **Tambahkan `additionalProperties: false`** ke semua objek
4. **Filter format string** ke daftar yang didukung saja
5. **Validasi respons** terhadap skema asli Anda (dengan semua batasan)

Ini berarti Claude menerima skema yang disederhanakan, tetapi kode Anda masih menerapkan semua batasan melalui validasi.

**Contoh:** Field Pydantic dengan `minimum: 100` menjadi integer biasa dalam skema yang dikirim, tetapi deskripsi diperbarui menjadi "Harus setidaknya 100", dan SDK memvalidasi respons terhadap batasan asli.

### Kasus penggunaan umum

<section title="Ekstraksi data">

Ekstrak data terstruktur dari teks tidak terstruktur:

<CodeGroup>

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' --format jsonl <<'YAML'
model: claude-opus-4-6
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

```python Python nocheck
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
    max_tokens=4096,
    output_format=Invoice,
    messages=[
        {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
    ],
)
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
  model: "claude-opus-4-6",
  max_tokens: 4096,
  output_config: { format: zodOutputFormat(InvoiceSchema) },
  messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
});
```

```csharp C#
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class InvoiceExtraction
{
    public class Invoice
    {
        public string invoice_number { get; set; }
        public string date { get; set; }
        public double total_amount { get; set; }
        public List<Dictionary<string, object>> line_items { get; set; }
        public string customer_name { get; set; }
    }

    static async Task Main()
    {
        AnthropicClient client = new();

        string invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..6,8..10}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;

public class InvoiceExtraction {
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

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        String invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

        StructuredMessageCreateParams<Invoice> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(4096L)
            .outputConfig(Invoice.class)
            .addUserMessage("Extract invoice data from: " + invoiceText)
            .build();

        StructuredMessage<Invoice> response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => "Extract invoice data from: $invoiceText"]
    ],
    model: 'claude-opus-4-6',
    outputConfig: [
        'format' => [
            'type' => 'json_schema',
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'invoice_number' => ['type' => 'string'],
                    'date' => ['type' => 'string'],
                    'total_amount' => ['type' => 'number'],
                    'line_items' => [
                        'type' => 'array',
                        'items' => [
                            'type' => 'object',
                            'additionalProperties' => false
                        ]
                    ],
                    'customer_name' => ['type' => 'string']
                ],
                'required' => ['invoice_number', 'date', 'total_amount', 'line_items', 'customer_name'],
                'additionalProperties' => false
            ]
        ]
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 4096,
  output_config: {
    format: {
      type: :json_schema,
      schema: {
        type: "object",
        properties: {
          invoice_number: { type: "string" },
          date: { type: "string" },
          total_amount: { type: "number" },
          line_items: {
            type: "array",
            items: {
              type: "object",
              additionalProperties: false
            }
          },
          customer_name: { type: "string" }
        },
        required: ["invoice_number", "date", "total_amount", "line_items", "customer_name"],
        additionalProperties: false
      }
    }
  },
  messages: [
    { role: "user", content: "Extract invoice data from: #{invoice_text}" }
  ]
)
puts message.content.first.text
```

</CodeGroup>

</section>

<section title="Klasifikasi">

Klasifikasikan konten dengan kategori terstruktur:

<CodeGroup>

```bash CLI
ant messages create \
  --transform 'content.0.text|@fromstr' --format jsonl <<'YAML'
model: claude-opus-4-6
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
from typing import List

client = Anthropic()


class Classification(BaseModel):
    category: str
    confidence: float
    tags: List[str]
    sentiment: str


feedback_text = "Great product, but the delivery was slow."
response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    output_format=Classification,
    messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
)
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
  model: "claude-opus-4-6",
  max_tokens: 1024,
  output_config: { format: zodOutputFormat(ClassificationSchema) },
  messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
});
```

```csharp C# hidelines={1..7}
using System.Collections.Generic;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

string feedbackText = "Great product, fast shipping!";

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..6,8..9}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ClassificationExample {
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

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        String feedbackText = "Great product, fast shipping!";

        StructuredMessageCreateParams<Classification> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(1024L)
            .outputConfig(Classification.class)
            .addUserMessage("Classify this feedback: " + feedbackText)
            .build();

        StructuredMessage<Classification> response = client.messages().create(params);
        Classification result = response.content().get(0).asText().text();
        System.out.println(result.category + " (" + result.confidence + ")");
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$feedbackText = "Great product, fast shipping!";

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
    ],
    model: 'claude-opus-4-6',
    outputConfig: [
        'format' => [
            'type' => 'json_schema',
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'category' => ['type' => 'string'],
                    'confidence' => ['type' => 'number'],
                    'tags' => ['type' => 'array', 'items' => ['type' => 'string']],
                    'sentiment' => ['type' => 'string']
                ],
                'required' => ['category', 'confidence', 'tags', 'sentiment'],
                'additionalProperties' => false
            ]
        ]
    ],
);
echo $message->content[0]->text;
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
  model: "claude-opus-4-6",
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
model: claude-opus-4-6
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
from typing import List, Optional

client = Anthropic()


class APIResponse(BaseModel):
    status: str
    data: dict
    errors: Optional[List[dict]]
    metadata: dict


response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    output_format=APIResponse,
    messages=[{"role": "user", "content": "Process this request: ..."}],
)
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
  model: "claude-opus-4-6",
  max_tokens: 1024,
  output_config: { format: zodOutputFormat(APIResponseSchema) },
  messages: [{ role: "user", content: "Process this request..." }]
});
```

```csharp C# hidelines={1..7}
using System.Collections.Generic;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..6,8..9}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Model;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class StructuredOutputExample {
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

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<APIResponse> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(1024L)
            .outputConfig(APIResponse.class)
            .addUserMessage("Process this request: ...")
            .build();

        StructuredMessage<APIResponse> response = client.messages().create(params);
        APIResponse result = response.content().get(0).asText().text();
        System.out.println(result.status);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Process this request: ...']
    ],
    model: 'claude-opus-4-6',
    outputConfig: [
        'format' => [
            'type' => 'json_schema',
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'status' => ['type' => 'string'],
                    'data' => ['type' => 'object', 'additionalProperties' => false],
                    'errors' => [
                        'type' => 'array',
                        'items' => ['type' => 'object', 'additionalProperties' => false]
                    ],
                    'metadata' => ['type' => 'object', 'additionalProperties' => false]
                ],
                'required' => ['status', 'data', 'metadata'],
                'additionalProperties' => false
            ]
        ]
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  output_config: {
    format: {
      type: :json_schema,
      schema: {
        type: "object",
        properties: {
          status: { type: "string" },
          data: { type: "object", additionalProperties: false },
          errors: {
            type: "array",
            items: { type: "object", additionalProperties: false }
          },
          metadata: { type: "object", additionalProperties: false }
        },
        required: ["status", "data", "metadata"],
        additionalProperties: false
      }
    }
  },
  messages: [
    { role: "user", content: "Process this request: ..." }
  ]
)
puts message.content.first.text
```

</CodeGroup>

</section>

## Penggunaan alat yang ketat

Untuk menegakkan kepatuhan JSON Schema pada input alat dengan pengambilan sampel yang dibatasi tata bahasa, lihat [Penggunaan alat yang ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use).

## Menggunakan kedua fitur bersama-sama

Output JSON dan penggunaan alat ketat menyelesaikan masalah yang berbeda dan dapat digunakan bersama-sama:

- **Output JSON** mengontrol format respons Claude (apa yang Claude katakan)
- **Penggunaan alat ketat** memvalidasi parameter alat (bagaimana Claude memanggil fungsi Anda)

Ketika digabungkan, Claude dapat memanggil alat dengan parameter yang dijamin valid DAN mengembalikan respons JSON terstruktur. Ini berguna untuk alur kerja agentic di mana Anda memerlukan panggilan alat yang andal dan output akhir terstruktur.

<CodeGroup>

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-opus-4-6",
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

```csharp C# hidelines={1..7}
using System.Collections.Generic;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..15,-2..}
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
import java.util.List;
import java.util.Map;

public class StructuredOutputExample {
    public static void main(String[] args) {
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
            .model(Model.CLAUDE_OPUS_4_6)
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Help me plan a trip to Paris departing May 15, 2026']
    ],
    model: 'claude-opus-4-6',
    // JSON outputs: structured response format
    outputConfig: [
        'format' => [
            'type' => 'json_schema',
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'summary' => ['type' => 'string'],
                    'next_steps' => ['type' => 'array', 'items' => ['type' => 'string']]
                ],
                'required' => ['summary', 'next_steps'],
                'additionalProperties' => false
            ]
        ]
    ],
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
echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
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
- Mengubah parameter `output_config.format` akan membatalkan [prompt cache](/docs/id/build-with-claude/prompt-caching) untuk utas percakapan itu

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
- Pencocokan penuh (`^...$`) dan pencocokan sebagian
- Quantifier: `*`, `+`, `?`, kasus `{n,m}` sederhana
- Kelas karakter: `[]`, `.`, `\d`, `\w`, `\s`
- Grup: `(...)`

**TIDAK didukung:**
- Backreference ke grup (misalnya, `\1`, `\2`)
- Pernyataan lookahead/lookbehind (misalnya, `(?=...)`, `(?!...)`)
- Batas kata: `\b`, `\B`
- Quantifier `{n,m}` kompleks dengan rentang besar

Pola regex sederhana bekerja dengan baik. Pola kompleks mungkin menghasilkan kesalahan 400.

</section>

<Tip>
SDK Python dan TypeScript dapat secara otomatis mengubah skema dengan fitur yang tidak didukung dengan menghapusnya dan menambahkan batasan ke deskripsi bidang. Lihat [metode khusus SDK](#sdk-specific-methods) untuk detail.
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

Jika urutan properti dalam output penting untuk aplikasi Anda, pastikan semua properti ditandai sebagai diperlukan, atau pertimbangkan pengurutan ulang ini dalam logika parsing Anda.

### Output tidak valid

Meskipun output terstruktur menjamin kepatuhan skema dalam sebagian besar kasus, ada skenario di mana output mungkin tidak cocok dengan skema Anda:

**Penolakan** (`stop_reason: "refusal"`)

Claude mempertahankan properti keamanan dan kegunaannya bahkan saat menggunakan output terstruktur. Jika Claude menolak permintaan karena alasan keamanan:

- Respons memiliki `stop_reason: "refusal"`
- Anda akan menerima kode status 200
- Anda akan ditagih untuk token yang dihasilkan
- Output mungkin tidak cocok dengan skema Anda karena pesan penolakan mengambil alih batasan skema

**Batas token tercapai** (`stop_reason: "max_tokens"`)

Jika respons dipotong karena mencapai batas `max_tokens`:

- Respons memiliki `stop_reason: "max_tokens"`
- Output mungkin tidak lengkap dan tidak cocok dengan skema Anda
- Coba lagi dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan output terstruktur yang lengkap

### Batasan kompleksitas skema

Output terstruktur bekerja dengan mengkompilasi skema JSON Anda menjadi tata bahasa yang membatasi output Claude. Skema yang lebih kompleks menghasilkan tata bahasa yang lebih besar yang membutuhkan waktu lebih lama untuk dikompilasi. Untuk melindungi dari waktu kompilasi yang berlebihan, API memberlakukan beberapa batasan kompleksitas.

#### Batasan eksplisit

Batasan berikut berlaku untuk semua permintaan dengan `output_config.format` atau `strict: true`:

| Batasan | Nilai | Deskripsi |
|-------|-------|-------------|
| Alat ketat per permintaan | 20 | Jumlah maksimum alat dengan `strict: true`. Alat non-ketat tidak dihitung terhadap batasan ini. |
| Parameter opsional | 24 | Total parameter opsional di semua skema alat ketat dan skema output JSON. Setiap parameter yang tidak tercantum dalam `required` dihitung terhadap batasan ini. |
| Parameter dengan tipe union | 16 | Total parameter yang menggunakan `anyOf` atau array tipe (misalnya, `"type": ["string", "null"]`) di semua skema ketat. Ini sangat mahal karena menciptakan biaya kompilasi eksponensial. |

<Note>
Batasan ini berlaku untuk total gabungan di semua skema ketat dalam satu permintaan. Misalnya, jika Anda memiliki 4 alat ketat dengan 6 parameter opsional masing-masing, Anda akan mencapai batasan 24 parameter meskipun tidak ada satu alat pun yang tampak kompleks.
</Note>

#### Batasan internal tambahan

Di luar batasan eksplisit di atas, ada batasan internal tambahan pada ukuran tata bahasa yang dikompilasi. Batasan ini ada karena kompleksitas skema tidak berkurang menjadi satu dimensi: fitur seperti parameter opsional, tipe union, objek bersarang, dan jumlah alat berinteraksi satu sama lain dengan cara yang dapat membuat tata bahasa yang dikompilasi menjadi tidak proporsional besar.

Ketika batasan ini terlampaui, Anda akan menerima kesalahan 400 dengan pesan "Schema is too complex for compilation." Kesalahan ini berarti kompleksitas gabungan skema Anda melebihi apa yang dapat dikompilasi secara efisien, bahkan jika setiap batasan individual di atas terpenuhi. Sebagai penghenti terakhir, API juga memberlakukan **batas waktu kompilasi 180 detik**. Skema yang lulus semua pemeriksaan eksplisit tetapi menghasilkan tata bahasa yang dikompilasi sangat besar mungkin mencapai batas waktu ini.

#### Tips untuk mengurangi kompleksitas skema

Jika Anda mencapai batasan kompleksitas, coba strategi ini secara berurutan:

1. **Tandai hanya alat penting sebagai ketat.** Jika Anda memiliki banyak alat, cadangkan untuk alat di mana pelanggaran skema menyebabkan masalah nyata, dan andalkan kepatuhan alami Claude untuk alat yang lebih sederhana.

2. **Kurangi parameter opsional.** Buat parameter `required` jika memungkinkan. Setiap parameter opsional kira-kira menggandakan sebagian dari ruang keadaan tata bahasa. Jika parameter selalu memiliki default yang masuk akal, pertimbangkan untuk membuatnya diperlukan dan biarkan Claude memberikan default itu secara eksplisit.

3. **Sederhanakan struktur bersarang.** Objek bersarang dalam dengan bidang opsional menambah kompleksitas. Ratakan struktur jika memungkinkan.

4. **Pisahkan menjadi beberapa permintaan.** Jika Anda memiliki banyak alat ketat, pertimbangkan untuk membaginya di seluruh permintaan terpisah atau sub-agen.

Untuk masalah persisten dengan skema yang valid, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support) dengan definisi skema Anda.

## Retensi data

Prompt dan respons diproses dengan ZDR saat menggunakan output terstruktur. Namun, skema JSON itu sendiri di-cache sementara selama hingga 24 jam sejak penggunaan terakhir untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan di luar respons API.

Output terstruktur memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi skema JSON**. API mengkompilasi skema JSON menjadi tata bahasa yang di-cache terpisah dari konten pesan, dan skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti skema, nilai `enum`, nilai `const`, atau ekspresi reguler `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana dilindungi di bawah perlindungan HIPAA.

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
**Cakupan tata bahasa**: Tata bahasa hanya berlaku untuk output langsung Claude, bukan untuk panggilan penggunaan alat, hasil alat, atau tag pemikiran (saat menggunakan [Extended Thinking](/docs/id/build-with-claude/extended-thinking)). Status tata bahasa direset antar bagian, memungkinkan Claude berpikir bebas sambil tetap menghasilkan output terstruktur dalam respons akhir.
</Tip>