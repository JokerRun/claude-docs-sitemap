---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: d87478e21db450ea86c50fa4f2a9814acfc57475ec58177e90d8bb06fad583b9
---

# Penggunaan alat strict

Terapkan kepatuhan JSON Schema pada input alat Claude dengan grammar-constrained sampling.

---

Menetapkan `strict: true` pada definisi alat menjamin input alat Claude sesuai dengan JSON Schema Anda dengan membatasi pengambilan sampel token model hanya pada output yang valid menurut skema (teknik yang disebut "grammar-constrained sampling" (pengambilan sampel yang dibatasi tata bahasa)). Halaman ini membahas mengapa mode strict penting untuk agen, cara mengaktifkannya, dan kasus penggunaan umum. Untuk subset JSON Schema yang didukung, lihat [Batasan JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Untuk panduan skema non-strict, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools).

Penggunaan alat strict memvalidasi parameter alat, memastikan Claude memanggil fungsi Anda dengan argumen yang bertipe benar. Gunakan penggunaan alat strict ketika Anda perlu:

- Memvalidasi parameter alat
- Membangun alur kerja agentik
- Memastikan pemanggilan fungsi yang type-safe
- Menangani alat kompleks dengan properti bersarang

## Mengapa penggunaan alat strict penting untuk agen \{#why-strict-tool-use-matters-for-agents}

Membangun sistem agentik yang andal memerlukan jaminan kesesuaian skema. Tanpa mode strict, Claude mungkin mengembalikan tipe yang tidak kompatibel (`"2"` alih-alih `2`) atau menghilangkan field yang wajib, sehingga merusak fungsi Anda dan menyebabkan error runtime.

Penggunaan alat strict menjamin parameter yang type-safe:
- Fungsi menerima argumen dengan tipe yang benar setiap saat
- Tidak perlu memvalidasi dan mencoba ulang pemanggilan alat
- Agen siap produksi yang bekerja secara konsisten dalam skala besar

Misalnya, anggaplah sistem pemesanan membutuhkan `passengers: int`. Tanpa mode strict, Claude mungkin memberikan `passengers: "two"` atau `passengers: "2"`. Dengan `strict: true`, respons selalu berisi `passengers: 2`.

## Mulai cepat \{#quick-start}

<CodeGroup>

```bash cURL highlight={14}
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-8",
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

```bash CLI highlight={10}
ant messages create --transform content <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content: What is the weather in San Francisco?
tools:
  - name: get_weather
    description: Get the current weather in a given location
    strict: true
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
        unit:
          type: string
          enum: [celsius, fahrenheit]
      required: [location]
      additionalProperties: false
YAML
```

```python Python hidelines={1..2} highlight={13}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
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

```typescript TypeScript hidelines={1..2} highlight={20}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: "claude-opus-4-8",
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

```csharp C# highlight={17}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }],
    Tools = [
        new ToolUnion(new Tool()
        {
            Name = "get_weather",
            Description = "Get the current weather in a given location",
            Strict = true,
            InputSchema = new InputSchema(new Dictionary<string, JsonElement>
            {
                ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                {
                    ["location"] = new { type = "string", description = "The city and state, e.g. San Francisco, CA" },
                    ["unit"] = new { type = "string", @enum = new[] { "celsius", "fahrenheit" } },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "location" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            }),
        }),
    ]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go hidelines={1..11,-1} highlight={24}
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:        "get_weather",
				Description: anthropic.String("Get the current weather in a given location"),
				Strict:      anthropic.Bool(true),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"location": map[string]any{
							"type":        "string",
							"description": "The city and state, e.g. San Francisco, CA",
						},
						"unit": map[string]any{
							"type": "string",
							"enum": []string{"celsius", "fahrenheit"},
						},
					},
					Required: []string{"location"},
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

```java Java hidelines={1..12,-1..} highlight={42}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.List;
import java.util.Map;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    InputSchema schema = InputSchema.builder()
        .properties(
            JsonValue.from(
                Map.of(
                    "location", Map.of(
                        "type", "string",
                        "description", "The city and state, e.g. San Francisco, CA"
                    ),
                    "unit", Map.of(
                        "type", "string",
                        "enum", List.of("celsius", "fahrenheit")
                    )
                )
            )
        )
        .putAdditionalProperty("required", JsonValue.from(List.of("location")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("What's the weather like in San Francisco?")
        .addTool(
            Tool.builder()
                .name("get_weather")
                .description("Get the current weather in a given location")
                .strict(true)
                .inputSchema(schema)
                .build()
        )
        .build();

    Message response = client.messages().create(params);
    IO.println(response.content());
}
```

```php PHP hidelines={1..4} highlight={17}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
    ],
    model: 'claude-opus-4-8',
    tools: [
        [
            'name' => 'get_weather',
            'description' => 'Get the current weather in a given location',
            'strict' => true,
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'location' => [
                        'type' => 'string',
                        'description' => 'The city and state, e.g. San Francisco, CA'
                    ],
                    'unit' => [
                        'type' => 'string',
                        'enum' => ['celsius', 'fahrenheit']
                    ]
                ],
                'required' => ['location'],
                'additionalProperties' => false
            ]
        ]
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2} highlight={15}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What's the weather like in San Francisco?" }
  ],
  tools: [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      strict: true,
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
)
puts message.content
```

</CodeGroup>

**Format respons:** Blok tool use dengan input yang tervalidasi di `response.content[x].input`

```json Output
{
  "type": "tool_use",
  "name": "get_weather",
  "input": {
    "location": "San Francisco, CA"
  }
}
```

**Jaminan:**
- `input` alat secara ketat mengikuti `input_schema`
- `name` alat selalu valid (dari alat yang disediakan atau alat server)

## Cara kerjanya \{#how-it-works}

<Steps>
  <Step title="Definisikan skema alat Anda">
    Buat skema JSON untuk `input_schema` alat Anda. Skema ini menggunakan format JSON Schema standar dengan beberapa batasan (lihat [Batasan JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations)).
  </Step>
  <Step title="Tambahkan strict: true">
    Tetapkan `"strict": true` sebagai properti tingkat atas dalam definisi alat Anda, bersama dengan `name`, `description`, dan `input_schema`.
  </Step>
  <Step title="Tangani pemanggilan alat">
    Ketika Claude menggunakan alat tersebut, field `input` dalam blok tool_use secara ketat mengikuti `input_schema` Anda, dan `name` selalu valid.
  </Step>
</Steps>

## Kasus penggunaan umum \{#common-use-cases}

<section title="Input alat yang tervalidasi">

Pastikan parameter alat sesuai persis dengan skema Anda:

<CodeGroup>

```bash CLI highlight={9}
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content: Search for flights to Tokyo departing June 1, 2026
tools:
  - name: search_flights
    strict: true
    input_schema:
      type: object
      properties:
        destination:
          type: string
        departure_date:
          type: string
          format: date
        passengers:
          type: integer
          enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      required: [destination, departure_date]
      additionalProperties: false
YAML
```

```python Python hidelines={1..2} highlight={16}
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Search for flights to Tokyo departing June 1, 2026",
        }
    ],
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

print(response)
```

```typescript TypeScript hidelines={1..2} highlight={7}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const searchFlightsTool: Anthropic.Tool = {
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
};

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Search for flights to Tokyo departing June 1, 2026" }],
  tools: [searchFlightsTool]
});

console.log(response);
```

```csharp C# highlight={16}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Search for flights to Tokyo departing June 1, 2026" }],
    Tools = [
        new ToolUnion(new Tool()
        {
            Name = "search_flights",
            Strict = true,
            InputSchema = new InputSchema(new Dictionary<string, JsonElement>
            {
                ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                {
                    ["destination"] = new { type = "string" },
                    ["departure_date"] = new { type = "string", format = "date" },
                    ["passengers"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 } },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "departure_date" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            }),
        }),
    ]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go hidelines={1..11,-1} highlight={23}
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Search for flights to Tokyo departing June 1, 2026")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:   "search_flights",
				Strict: anthropic.Bool(true),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"destination": map[string]any{
							"type": "string",
						},
						"departure_date": map[string]any{
							"type":   "string",
							"format": "date",
						},
						"passengers": map[string]any{
							"type": "integer",
							"enum": []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
						},
					},
					Required: []string{"destination", "departure_date"},
					ExtraFields: map[string]any{
						"additionalProperties": false,
					},
				}}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..12,-1..} highlight={39}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.List;
import java.util.Map;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    InputSchema schema = InputSchema.builder()
        .properties(
            JsonValue.from(
                Map.of(
                    "destination", Map.of("type", "string"),
                    "departure_date", Map.of("type", "string", "format", "date"),
                    "passengers", Map.of(
                        "type", "integer",
                        "enum", List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
                    )
                )
            )
        )
        .putAdditionalProperty("required", JsonValue.from(List.of("destination", "departure_date")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("Search for flights to Tokyo departing June 1, 2026")
        .addTool(
            Tool.builder()
                .name("search_flights")
                .strict(true)
                .inputSchema(schema)
                .build()
        )
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4} highlight={16}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Search for flights to Tokyo departing June 1, 2026']
    ],
    model: 'claude-opus-4-8',
    tools: [
        [
            'name' => 'search_flights',
            'strict' => true,
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'destination' => ['type' => 'string'],
                    'departure_date' => ['type' => 'string', 'format' => 'date'],
                    'passengers' => [
                        'type' => 'integer',
                        'enum' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    ]
                ],
                'required' => ['destination', 'departure_date'],
                'additionalProperties' => false
            ]
        ]
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2} highlight={14}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Search for flights to Tokyo departing June 1, 2026" }
  ],
  tools: [
    {
      name: "search_flights",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          destination: { type: "string" },
          departure_date: { type: "string", format: "date" },
          passengers: {
            type: "integer",
            enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
          }
        },
        required: ["destination", "departure_date"],
        additionalProperties: false
      }
    }
  ]
)
puts message
```

</CodeGroup>

</section>

<section title="Alur kerja agentik dengan beberapa alat yang tervalidasi">

Bangun agen multi-langkah yang andal dengan parameter alat yang terjamin:

<CodeGroup>

```bash CLI highlight={11,22}
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content: >-
      Help me plan a trip from New York to Paris for 2 people,
      departing June 1, 2026
tools:
  - name: search_flights
    strict: true
    input_schema:
      type: object
      properties:
        origin: {type: string}
        destination: {type: string}
        departure_date: {type: string, format: date}
        travelers: {type: integer, enum: [1, 2, 3, 4, 5, 6]}
      required: [origin, destination, departure_date]
      additionalProperties: false
  - name: search_hotels
    strict: true
    input_schema:
      type: object
      properties:
        city: {type: string}
        check_in: {type: string, format: date}
        guests: {type: integer, enum: [1, 2, 3, 4]}
      required: [city, check_in]
      additionalProperties: false
YAML
```

```python Python hidelines={1..2} highlight={16,31}
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026",
        }
    ],
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

print(response)
```

```typescript TypeScript hidelines={1..2} highlight={8,23}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
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
];

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content:
        "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026"
    }
  ],
  tools: tools
});

console.log(response);
```

```csharp C# highlight={16,33}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026" }],
    Tools = [
        new ToolUnion(new Tool()
        {
            Name = "search_flights",
            Strict = true,
            InputSchema = new InputSchema(new Dictionary<string, JsonElement>
            {
                ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                {
                    ["origin"] = new { type = "string" },
                    ["destination"] = new { type = "string" },
                    ["departure_date"] = new { type = "string", format = "date" },
                    ["travelers"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4, 5, 6 } },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "origin", "destination", "departure_date" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            }),
        }),
        new ToolUnion(new Tool()
        {
            Name = "search_hotels",
            Strict = true,
            InputSchema = new InputSchema(new Dictionary<string, JsonElement>
            {
                ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                {
                    ["city"] = new { type = "string" },
                    ["check_in"] = new { type = "string", format = "date" },
                    ["guests"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4 } },
                }),
                ["required"] = JsonSerializer.SerializeToElement(new[] { "city", "check_in" }),
                ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
            }),
        }),
    ]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
```

```go Go hidelines={1..11,-1} highlight={23,38}
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:   "search_flights",
				Strict: anthropic.Bool(true),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"origin":         map[string]any{"type": "string"},
						"destination":    map[string]any{"type": "string"},
						"departure_date": map[string]any{"type": "string", "format": "date"},
						"travelers":      map[string]any{"type": "integer", "enum": []int{1, 2, 3, 4, 5, 6}},
					},
					Required: []string{"origin", "destination", "departure_date"},
					ExtraFields: map[string]any{
						"additionalProperties": false,
					},
				}}},
			{OfTool: &anthropic.ToolParam{
				Name:   "search_hotels",
				Strict: anthropic.Bool(true),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"city":     map[string]any{"type": "string"},
						"check_in": map[string]any{"type": "string", "format": "date"},
						"guests":   map[string]any{"type": "integer", "enum": []int{1, 2, 3, 4}},
					},
					Required: []string{"city", "check_in"},
					ExtraFields: map[string]any{
						"additionalProperties": false,
					},
				}}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..12,-1..} highlight={51,58}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.List;
import java.util.Map;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    InputSchema flightsSchema = InputSchema.builder()
        .properties(
            JsonValue.from(
                Map.of(
                    "origin", Map.of("type", "string"),
                    "destination", Map.of("type", "string"),
                    "departure_date", Map.of("type", "string", "format", "date"),
                    "travelers", Map.of("type", "integer", "enum", List.of(1, 2, 3, 4, 5, 6))
                )
            )
        )
        .putAdditionalProperty("required", JsonValue.from(List.of("origin", "destination", "departure_date")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    InputSchema hotelsSchema = InputSchema.builder()
        .properties(
            JsonValue.from(
                Map.of(
                    "city", Map.of("type", "string"),
                    "check_in", Map.of("type", "string", "format", "date"),
                    "guests", Map.of("type", "integer", "enum", List.of(1, 2, 3, 4))
                )
            )
        )
        .putAdditionalProperty("required", JsonValue.from(List.of("city", "check_in")))
        .putAdditionalProperty("additionalProperties", JsonValue.from(false))
        .build();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026")
        .addTool(
            Tool.builder()
                .name("search_flights")
                .strict(true)
                .inputSchema(flightsSchema)
                .build()
        )
        .addTool(
            Tool.builder()
                .name("search_hotels")
                .strict(true)
                .inputSchema(hotelsSchema)
                .build()
        )
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4} highlight={16,31}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026']
    ],
    model: 'claude-opus-4-8',
    tools: [
        [
            'name' => 'search_flights',
            'strict' => true,
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'origin' => ['type' => 'string'],
                    'destination' => ['type' => 'string'],
                    'departure_date' => ['type' => 'string', 'format' => 'date'],
                    'travelers' => ['type' => 'integer', 'enum' => [1, 2, 3, 4, 5, 6]]
                ],
                'required' => ['origin', 'destination', 'departure_date'],
                'additionalProperties' => false
            ]
        ],
        [
            'name' => 'search_hotels',
            'strict' => true,
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'city' => ['type' => 'string'],
                    'check_in' => ['type' => 'string', 'format' => 'date'],
                    'guests' => ['type' => 'integer', 'enum' => [1, 2, 3, 4]]
                ],
                'required' => ['city', 'check_in'],
                'additionalProperties' => false
            ]
        ]
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2} highlight={14,29}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026" }
  ],
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
)
puts message
```

</CodeGroup>

</section>

## Retensi data \{#data-retention}

Penggunaan alat strict mengompilasi definisi `input_schema` alat menjadi tata bahasa menggunakan pipeline yang sama dengan [structured outputs](/docs/id/build-with-claude/structured-outputs). Skema alat disimpan sementara dalam cache hingga 24 jam sejak penggunaan terakhir. Prompt dan respons tidak disimpan setelah respons API dikembalikan.

Penggunaan alat strict memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi skema alat**. API menyimpan skema yang telah dikompilasi dalam cache secara terpisah dari konten pesan, dan skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti `input_schema`, nilai `enum`, nilai `const`, atau ekspresi reguler `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana PHI dilindungi di bawah pengamanan HIPAA.

Untuk kelayakan ZDR dan HIPAA di seluruh fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Alat web fetch" icon="link" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil dan baca konten dari URL tertentu untuk membawa konten web langsung ke dalam konteks Claude.
  </Card>
  <Card title="Penggunaan alat dengan caching prompt" icon="database" href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh giliran untuk mengurangi biaya dan latensi.
  </Card>
  <Card title="Structured outputs" icon="code-brackets" href="/docs/id/build-with-claude/structured-outputs">
    Dapatkan respons JSON yang tervalidasi menggunakan grammar-constrained sampling yang sama.
  </Card>
  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kendalikan kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>