---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 92deb346bc483c93f8fe8ea5a99163d5a1f37aa4b9ea330c0868db46f0933b32
---

# Tentukan alat

Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.

---

## Memilih model

Gunakan model Claude Opus terbaru (4.7) untuk alat yang kompleks dan kueri yang ambigu; model ini menangani beberapa alat dengan lebih baik dan mencari klarifikasi saat diperlukan.

Gunakan model Claude Haiku untuk alat yang sederhana, tetapi perhatikan bahwa mereka mungkin menyimpulkan parameter yang hilang.

<Tip>
Jika menggunakan Claude dengan penggunaan alat dan pemikiran yang diperluas, lihat [panduan pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) untuk informasi lebih lanjut.
</Tip>

## Menentukan alat klien

Alat klien (baik skema Anthropic maupun yang ditentukan pengguna) ditentukan dalam parameter tingkat atas `tools` dari permintaan API. Setiap definisi alat mencakup:

| Parameter      | Deskripsi                                                                                         |
| :------------- | :-------------------------------------------------------------------------------------------------- |
| `name`         | Nama alat. Harus cocok dengan regex `^[a-zA-Z0-9_-]{1,64}$`.                                 |
| `description`  | Deskripsi plaintext terperinci tentang apa yang dilakukan alat, kapan harus digunakan, dan bagaimana perilakunya. |
| `input_schema` | Objek [JSON Schema](https://json-schema.org/) yang mendefinisikan parameter yang diharapkan untuk alat.     |
| `input_examples` | (Opsional) Larik objek input contoh untuk membantu Claude memahami cara menggunakan alat. Lihat [Memberikan contoh penggunaan alat](#providing-tool-use-examples). |

Untuk set lengkap properti opsional yang tersedia pada definisi alat apa pun, termasuk `cache_control`, `strict`, `defer_loading`, dan `allowed_callers`, lihat [referensi Alat](/docs/id/agents-and-tools/tool-use/tool-reference#tool-definition-properties).

<section title="Contoh definisi alat sederhana">

```json JSON
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
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
    "required": ["location"]
  }
}
```

Alat ini, bernama `get_weather`, mengharapkan objek input dengan string `location` yang diperlukan dan string `unit` opsional yang harus berupa "celsius" atau "fahrenheit".

</section>

### Prompt sistem penggunaan alat

Ketika Anda memanggil Claude API dengan parameter `tools`, API membuat prompt sistem khusus dari definisi alat, konfigurasi alat, dan prompt sistem yang ditentukan pengguna. Prompt yang dibangun dirancang untuk menginstruksikan model untuk menggunakan alat yang ditentukan dan memberikan konteks yang diperlukan agar alat beroperasi dengan benar:

```text
In this environment you have access to a set of tools you can use to answer the user's question.
{{ FORMATTING INSTRUCTIONS }}
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}
{{ USER SYSTEM PROMPT }}
{{ TOOL CONFIGURATION }}
```

### Praktik terbaik untuk definisi alat

Untuk mendapatkan kinerja terbaik dari Claude saat menggunakan alat, ikuti panduan ini:

- **Berikan deskripsi yang sangat terperinci.** Ini adalah faktor paling penting dalam kinerja alat. Deskripsi Anda harus menjelaskan setiap detail tentang alat, termasuk:
  - Apa yang dilakukan alat
  - Kapan harus digunakan (dan kapan tidak boleh)
  - Apa arti setiap parameter dan bagaimana pengaruhnya terhadap perilaku alat
  - Peringatan atau batasan penting, seperti informasi apa yang tidak dikembalikan alat jika nama alat tidak jelas. Semakin banyak konteks yang dapat Anda berikan Claude tentang alat Anda, semakin baik dalam memutuskan kapan dan bagaimana menggunakannya. Targetkan setidaknya 3-4 kalimat per deskripsi alat, lebih banyak jika alat tersebut kompleks.
- **Prioritaskan deskripsi, tetapi pertimbangkan menggunakan `input_examples` untuk alat yang kompleks.** Deskripsi yang jelas paling penting, tetapi untuk alat dengan input kompleks, objek bersarang, atau parameter sensitif format, Anda dapat menggunakan bidang `input_examples` untuk memberikan contoh yang divalidasi skema. Lihat [Memberikan contoh penggunaan alat](#providing-tool-use-examples) untuk detail.
- **Konsolidasikan operasi terkait ke dalam lebih sedikit alat.** Daripada membuat alat terpisah untuk setiap tindakan (`create_pr`, `review_pr`, `merge_pr`), kelompokkan mereka ke dalam satu alat dengan parameter `action`. Lebih sedikit alat yang lebih mampu mengurangi ambiguitas pemilihan dan membuat permukaan alat Anda lebih mudah dinavigasi oleh Claude.
- **Gunakan penamaan namespace yang bermakna dalam nama alat.** Ketika alat Anda mencakup beberapa layanan atau sumber daya, awali nama dengan layanan (misalnya, `github_list_prs`, `slack_send_message`). Ini membuat pemilihan alat tidak ambigu saat perpustakaan Anda berkembang, dan sangat penting saat menggunakan [pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool).
- **Desain respons alat untuk mengembalikan hanya informasi sinyal tinggi.** Kembalikan pengidentifikasi semantik yang stabil (misalnya, slug atau UUID) daripada referensi internal yang buram, dan sertakan hanya bidang yang Claude butuhkan untuk bernalar tentang langkah berikutnya. Respons yang membengkak membuang konteks dan membuat lebih sulit bagi Claude untuk mengekstrak apa yang penting.

<section title="Contoh deskripsi alat yang baik">

```json JSON
{
  "name": "get_stock_price",
  "description": "Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
      }
    },
    "required": ["ticker"]
  }
}
```

</section>

<section title="Contoh deskripsi alat yang buruk">

```json JSON
{
  "name": "get_stock_price",
  "description": "Gets the stock price for a ticker.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string"
      }
    },
    "required": ["ticker"]
  }
}
```

</section>

Deskripsi yang baik dengan jelas menjelaskan apa yang dilakukan alat, kapan menggunakannya, data apa yang dikembalikan, dan apa arti parameter `ticker`. Deskripsi yang buruk terlalu singkat dan meninggalkan Claude dengan banyak pertanyaan terbuka tentang perilaku dan penggunaan alat.

<Tip>
Untuk panduan yang lebih mendalam tentang desain alat (konsolidasi, penamaan, dan pembentukan respons), lihat [Menulis alat untuk agen](https://www.anthropic.com/engineering/writing-tools-for-agents).
</Tip>

## Memberikan contoh penggunaan alat

Anda dapat memberikan contoh konkret dari input alat yang valid untuk membantu Claude memahami cara menggunakan alat Anda dengan lebih efektif. Ini sangat berguna untuk alat kompleks dengan objek bersarang, parameter opsional, atau input sensitif format.

### Penggunaan dasar

Tambahkan bidang `input_examples` opsional ke definisi alat Anda dengan larik objek input contoh. Setiap contoh harus valid sesuai dengan `input_schema` alat:

<CodeGroup>
```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
        unit:
          type: string
          enum: [celsius, fahrenheit]
          description: The unit of temperature
      required: [location]
    input_examples:
      - location: San Francisco, CA
        unit: fahrenheit
      - location: Tokyo, Japan
        unit: celsius
      - location: New York, NY  # 'unit' is optional
messages:
  - role: user
    content: What's the weather like in San Francisco?
YAML
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
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
                        "description": "The unit of temperature",
                    },
                },
                "required": ["location"],
            },
            "input_examples": [
                {"location": "San Francisco, CA", "unit": "fahrenheit"},
                {"location": "Tokyo, Japan", "unit": "celsius"},
                {
                    "location": "New York, NY"  # 'unit' is optional
                },
            ],
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)

print(response)
```

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          },
          unit: {
            type: "string",
            enum: ["celsius", "fahrenheit"],
            description: "The unit of temperature"
          }
        },
        required: ["location"]
      },
      input_examples: [
        {
          location: "San Francisco, CA",
          unit: "fahrenheit"
        },
        {
          location: "Tokyo, Japan",
          unit: "celsius"
        },
        {
          location: "New York, NY"
          // Demonstrates that 'unit' is optional
        }
      ]
    }
  ],
  messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
});

console.log(response);
```

```csharp C# hidelines={1..7}
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Tools = [
        new ToolUnion(new Tool()
        {
            Name = "get_weather",
            Description = "Get the current weather in a given location",
            InputSchema = new InputSchema()
            {
                Properties = new Dictionary<string, JsonElement>
                {
                    ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                    ["unit"] = JsonSerializer.SerializeToElement(new { type = "string", @enum = new[] { "celsius", "fahrenheit" }, description = "The unit of temperature" }),
                },
                Required = ["location"],
            },
            InputExamples =
            [
                new Dictionary<string, JsonElement>()
                {
                    { "location", JsonSerializer.SerializeToElement("San Francisco, CA") },
                    { "unit", JsonSerializer.SerializeToElement("fahrenheit") },
                },
                new Dictionary<string, JsonElement>()
                {
                    { "location", JsonSerializer.SerializeToElement("Tokyo, Japan") },
                    { "unit", JsonSerializer.SerializeToElement("celsius") },
                },
                new Dictionary<string, JsonElement>()
                {
                    { "location", JsonSerializer.SerializeToElement("New York, NY") },
                },
            ],
        }),
    ],
    Messages = [
        new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }
    ]
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
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:        "get_weather",
				Description: anthropic.String("Get the current weather in a given location"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"location": map[string]any{
							"type":        "string",
							"description": "The city and state, e.g. San Francisco, CA",
						},
						"unit": map[string]any{
							"type":        "string",
							"enum":        []string{"celsius", "fahrenheit"},
							"description": "The unit of temperature",
						},
					},
					Required: []string{"location"},
				},
				InputExamples: []map[string]any{
					{
						"location": "San Francisco, CA",
						"unit":     "fahrenheit",
					},
					{
						"location": "Tokyo, Japan",
						"unit":     "celsius",
					},
					{
						"location": "New York, NY",
						// Demonstrates that 'unit' is optional
					},
				},
			}},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..12,-1..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.Map;
import java.util.List;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .addTool(Tool.builder()
            .name("get_weather")
            .description("Get the current weather in a given location")
            .inputSchema(InputSchema.builder()
                .properties(JsonValue.from(Map.of(
                    "location", Map.of(
                        "type", "string",
                        "description", "The city and state, e.g. San Francisco, CA"
                    ),
                    "unit", Map.of(
                        "type", "string",
                        "enum", List.of("celsius", "fahrenheit"),
                        "description", "The unit of temperature"
                    )
                )))
                .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                .build())
            .putAdditionalProperty("input_examples", JsonValue.from(List.of(
                Map.of(
                    "location", "San Francisco, CA",
                    "unit", "fahrenheit"
                ),
                Map.of(
                    "location", "Tokyo, Japan",
                    "unit", "celsius"
                ),
                Map.of(
                    "location", "New York, NY"
                )
            )))
            .build())
        .addUserMessage("What's the weather like in San Francisco?")
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'name' => 'get_weather',
            'description' => 'Get the current weather in a given location',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'location' => [
                        'type' => 'string',
                        'description' => 'The city and state, e.g. San Francisco, CA'
                    ],
                    'unit' => [
                        'type' => 'string',
                        'enum' => ['celsius', 'fahrenheit'],
                        'description' => 'The unit of temperature'
                    ]
                ],
                'required' => ['location']
            ],
            'input_examples' => [
                [
                    'location' => 'San Francisco, CA',
                    'unit' => 'fahrenheit'
                ],
                [
                    'location' => 'Tokyo, Japan',
                    'unit' => 'celsius'
                ],
                [
                    'location' => 'New York, NY'
                ]
            ]
        ]
    ],
);
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          },
          unit: {
            type: "string",
            enum: ["celsius", "fahrenheit"],
            description: "The unit of temperature"
          }
        },
        required: ["location"]
      },
      input_examples: [
        {
          location: "San Francisco, CA",
          unit: "fahrenheit"
        },
        {
          location: "Tokyo, Japan",
          unit: "celsius"
        },
        {
          location: "New York, NY"
        }
      ]
    }
  ],
  messages: [
    { role: "user", content: "What's the weather like in San Francisco?" }
  ]
)
puts message
```
</CodeGroup>

Contoh disertakan dalam prompt bersama skema alat Anda, menunjukkan Claude pola konkret untuk panggilan alat yang terbentuk dengan baik. Ini membantu Claude memahami kapan harus menyertakan parameter opsional, format apa yang harus digunakan, dan cara menyusun input kompleks.

### Persyaratan dan batasan

- **Validasi skema** - Setiap contoh harus valid sesuai dengan `input_schema` alat. Contoh yang tidak valid mengembalikan kesalahan 400
- **Tidak didukung untuk alat sisi server** - Contoh input bekerja pada alat klien yang ditentukan pengguna dan skema Anthropic, tetapi bukan pada alat server seperti pencarian web atau eksekusi kode
- **Biaya token** - Contoh menambah token prompt: ~20-50 token untuk contoh sederhana, ~100-200 token untuk objek bersarang kompleks

## Mengontrol output Claude

### Memaksa penggunaan alat

Dalam beberapa kasus, Anda mungkin ingin Claude menggunakan alat tertentu untuk menjawab pertanyaan pengguna, bahkan jika Claude sebaliknya akan menjawab langsung tanpa memanggil alat. Anda dapat melakukan ini dengan menentukan alat dalam bidang `tool_choice` seperti ini:

```text
tool_choice = {"type": "tool", "name": "get_weather"}
```

Saat bekerja dengan parameter tool_choice, ada empat opsi yang mungkin:

- `auto` memungkinkan Claude memutuskan apakah akan memanggil alat yang disediakan atau tidak. Ini adalah nilai default ketika `tools` disediakan.
- `any` memberi tahu Claude bahwa ia harus menggunakan salah satu alat yang disediakan, tetapi tidak memaksa alat tertentu.
- `tool` memaksa Claude untuk selalu menggunakan alat tertentu.
- `none` mencegah Claude menggunakan alat apa pun. Ini adalah nilai default ketika tidak ada `tools` yang disediakan.

<Note>
Saat menggunakan [penyimpanan prompt](/docs/id/build-with-claude/prompt-caching#what-invalidates-the-cache), perubahan pada parameter `tool_choice` akan membatalkan blok pesan yang disimpan dalam cache. Definisi alat dan prompt sistem tetap disimpan dalam cache, tetapi konten pesan harus diproses ulang.
</Note>

Diagram ini mengilustrasikan cara kerja setiap opsi:

<Frame>
  ![Diagram showing the four tool_choice options: auto, any, tool, and none](/docs/images/tool_choice.png)
</Frame>

Perhatikan bahwa ketika Anda memiliki `tool_choice` sebagai `any` atau `tool`, API mengisi pesan asisten sebelumnya untuk memaksa alat digunakan. Ini berarti bahwa model tidak akan mengeluarkan respons bahasa alami atau penjelasan sebelum blok konten `tool_use`, bahkan jika secara eksplisit diminta untuk melakukannya.

<Note>
Saat menggunakan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) dengan penggunaan alat, `tool_choice: {"type": "any"}` dan `tool_choice: {"type": "tool", "name": "..."}` tidak didukung dan akan menghasilkan kesalahan. Hanya `tool_choice: {"type": "auto"}` (default) dan `tool_choice: {"type": "none"}` yang kompatibel dengan pemikiran yang diperluas.
</Note>

<Note>
[Claude Mythos Preview](https://anthropic.com/glasswing) tidak mendukung penggunaan alat yang dipaksa. Permintaan dengan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` mengembalikan kesalahan 400 pada model ini. Gunakan `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}` dan andalkan prompting untuk mempengaruhi pemilihan alat.
</Note>

Pengujian telah menunjukkan bahwa ini tidak boleh mengurangi kinerja. Jika Anda ingin model memberikan konteks bahasa alami atau penjelasan sambil tetap meminta model menggunakan alat tertentu, Anda dapat menggunakan `{"type": "auto"}` untuk `tool_choice` (default) dan menambahkan instruksi eksplisit dalam pesan `user`. Misalnya: `What's the weather like in London? Use the get_weather tool in your response.`

<Tip>
**Panggilan alat yang dijamin dengan alat ketat**

Gabungkan `tool_choice: {"type": "any"}` dengan [penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use) untuk menjamin bahwa salah satu alat Anda akan dipanggil DAN input alat akan ketat mengikuti skema Anda. Atur `strict: true` pada definisi alat Anda untuk mengaktifkan validasi skema.
</Tip>

### Respons model dengan alat

Saat menggunakan alat, Claude sering kali akan mengomentari apa yang sedang dilakukan atau merespons secara alami kepada pengguna sebelum memanggil alat.

Misalnya, diberikan prompt "What's the weather like in San Francisco right now, and what time is it there?", Claude mungkin merespons dengan:

```json JSON
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll help you check the current weather and time in San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": { "location": "San Francisco, CA" }
    }
  ]
}
```

Gaya respons alami ini membantu pengguna memahami apa yang dilakukan Claude dan menciptakan interaksi yang lebih percakapan. Anda dapat memandu gaya dan konten respons ini melalui prompt sistem Anda dan dengan memberikan `<examples>` dalam prompt Anda.

Penting untuk dicatat bahwa Claude dapat menggunakan berbagai frasa dan pendekatan saat menjelaskan tindakannya. Kode Anda harus memperlakukan respons ini seperti teks yang dihasilkan asisten lainnya, dan tidak mengandalkan konvensi pemformatan tertentu.

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/handle-tool-calls" title="Tangani panggilan alat">
    Parsing blok tool_use dan format respons tool_result.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-runner" title="Tool Runner (SDK)">
    Biarkan SDK menangani loop agentic secara otomatis.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori alat yang disediakan Anthropic dan properti opsional.
  </Card>
</CardGroup>