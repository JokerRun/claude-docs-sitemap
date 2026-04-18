---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 699d93be25bae88790056545eaa2fb1692172734ab278262b1510c6acbac7276
---

# Alat pencarian alat

Alat pencarian alat memungkinkan Claude untuk bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuat mereka sesuai permintaan.

---

Alat pencarian alat memungkinkan Claude untuk bekerja dengan ratusan atau ribuan alat dengan secara dinamis menemukan dan memuat mereka sesuai permintaan. Alih-alih memuat semua definisi alat ke jendela konteks di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan memuat hanya alat yang dibutuhkannya.

Pendekatan ini menyelesaikan dua masalah yang berkembang pesat seiring dengan skala perpustakaan alat:

- **Konteks bloat:** Definisi alat menghabiskan anggaran konteks Anda dengan cepat. Pengaturan multi-server yang khas (GitHub, Slack, Sentry, Grafana, Splunk) dapat mengonsumsi ~55k token dalam definisi sebelum Claude melakukan pekerjaan apa pun. Pencarian alat biasanya mengurangi ini lebih dari 85%, memuat hanya 3–5 alat yang benar-benar dibutuhkan Claude untuk permintaan tertentu.
- **Akurasi pemilihan alat:** Kemampuan Claude untuk memilih alat yang tepat menurun secara signifikan setelah Anda melampaui 30–50 alat yang tersedia. Dengan menampilkan serangkaian alat yang relevan dan terfokus sesuai permintaan, pencarian alat menjaga akurasi pemilihan tetap tinggi bahkan di seluruh ribuan alat.

<Tip>
Untuk latar belakang tantangan penskalaan yang diselesaikan oleh pencarian alat, lihat [Penggunaan alat tingkat lanjut](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai permintaan pencarian alat juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Rekayasa konteks yang efektif](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Meskipun ini disediakan sebagai alat sisi server, Anda juga dapat menerapkan fungsionalitas pencarian alat sisi klien Anda sendiri. Lihat [Implementasi pencarian alat khusus](#custom-tool-search-implementation) untuk detail.

<Note>
Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA).
</Note>

<Note>
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Warning>
  Di Amazon Bedrock, pencarian alat sisi server hanya tersedia melalui [API invoke](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html),
  bukan API converse.
</Warning>

Anda juga dapat menerapkan [pencarian alat sisi klien](#custom-tool-search-implementation) dengan mengembalikan blok `tool_reference` dari implementasi pencarian Anda sendiri.

## Cara kerja pencarian alat

Ada dua varian pencarian alat:

- **Regex** (`tool_search_tool_regex_20251119`): Claude membuat pola regex untuk mencari alat
- **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat

Ketika Anda mengaktifkan alat pencarian alat:

1. Anda menyertakan alat pencarian alat (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar alat Anda
2. Anda menyediakan semua definisi alat dengan `defer_loading: true` untuk alat yang tidak boleh dimuat segera
3. Claude awalnya hanya melihat alat pencarian alat dan alat non-deferred apa pun
4. Ketika Claude membutuhkan alat tambahan, ia mencari menggunakan alat pencarian alat
5. API mengembalikan 3-5 blok `tool_reference` paling relevan
6. Referensi ini secara otomatis diperluas menjadi definisi alat lengkap
7. Claude memilih dari alat yang ditemukan dan menginvokasinya

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
        "model": "claude-opus-4-7",
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

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-7
max_tokens: 2048
messages:
  - role: user
    content: What is the weather in San Francisco?
tools:
  - type: tool_search_tool_regex_20251119
    name: tool_search_tool_regex
  - name: get_weather
    description: Get the weather at a specific location
    input_schema:
      type: object
      properties:
        location:
          type: string
        unit:
          type: string
          enum: [celsius, fahrenheit]
      required: [location]
    defer_loading: true
  - name: search_files
    description: Search through files in the workspace
    input_schema:
      type: object
      properties:
        query:
          type: string
        file_types:
          type: array
          items:
            type: string
      required: [query]
    defer_loading: true
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
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

```typescript TypeScript hidelines={1..5,-3..-1}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.messages.create({
    model: "claude-opus-4-7",
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
          type: "object" as const,
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
          type: "object" as const,
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

```csharp C#
using System;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 2048,
            Messages = [
                new() {
                    Role = Role.User,
                    Content = "What is the weather in San Francisco?"
                }
            ],
            Tools = [
                new ToolUnion(new ToolSearchToolRegex20251119
                {
                    Type = ToolSearchToolRegex20251119Type.ToolSearchToolRegex20251119
                }),
                new ToolUnion(new Tool()
                {
                    Name = "get_weather",
                    Description = "Get the weather at a specific location",
                    InputSchema = new InputSchema()
                    {
                        Properties = new Dictionary<string, JsonElement>
                        {
                            ["location"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                            ["unit"] = JsonSerializer.SerializeToElement(new { type = "string", @enum = new[] { "celsius", "fahrenheit" } }),
                        },
                        Required = ["location"],
                    },
                    DeferLoading = true,
                }),
                new ToolUnion(new Tool()
                {
                    Name = "search_files",
                    Description = "Search through files in the workspace",
                    InputSchema = new InputSchema()
                    {
                        Properties = new Dictionary<string, JsonElement>
                        {
                            ["query"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                            ["file_types"] = JsonSerializer.SerializeToElement(new { type = "array", items = new { type = "string" } }),
                        },
                        Required = ["query"],
                    },
                    DeferLoading = true,
                }),
            ]
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 2048,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco?")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfToolSearchToolRegex20251119: &anthropic.ToolSearchToolRegex20251119Param{
				Type: anthropic.ToolSearchToolRegex20251119TypeToolSearchToolRegex20251119,
			}},
			{OfTool: &anthropic.ToolParam{
				Name:        "get_weather",
				Description: anthropic.String("Get the weather at a specific location"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"location": map[string]any{"type": "string"},
						"unit": map[string]any{
							"type": "string",
							"enum": []string{"celsius", "fahrenheit"},
						},
					},
					Required: []string{"location"},
				},
				DeferLoading: anthropic.Bool(true),
			}},
			{OfTool: &anthropic.ToolParam{
				Name:        "search_files",
				Description: anthropic.String("Search through files in the workspace"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"query":      map[string]any{"type": "string"},
						"file_types": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
					},
					Required: []string{"query"},
				},
				DeferLoading: anthropic.Bool(true),
			}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..8,10..14,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.ToolSearchToolRegex20251119;
import java.util.List;
import java.util.Map;

public class ToolSearchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        InputSchema weatherSchema = InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "location", Map.of("type", "string"),
                "unit", Map.of(
                    "type", "string",
                    "enum", List.of("celsius", "fahrenheit")
                )
            )))
            .putAdditionalProperty("required", JsonValue.from(List.of("location")))
            .build();

        InputSchema searchSchema = InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "query", Map.of("type", "string"),
                "file_types", Map.of(
                    "type", "array",
                    "items", Map.of("type", "string")
                )
            )))
            .putAdditionalProperty("required", JsonValue.from(List.of("query")))
            .build();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(2048L)
            .addUserMessage("What is the weather in San Francisco?")
            .addTool(ToolSearchToolRegex20251119.builder()
                .type(ToolSearchToolRegex20251119.Type.TOOL_SEARCH_TOOL_REGEX_20251119)
                .build())
            .addTool(Tool.builder()
                .name("get_weather")
                .description("Get the weather at a specific location")
                .inputSchema(weatherSchema)
                .deferLoading(true)
                .build())
            .addTool(Tool.builder()
                .name("search_files")
                .description("Search through files in the workspace")
                .inputSchema(searchSchema)
                .deferLoading(true)
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
    maxTokens: 2048,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather in San Francisco?'],
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'type' => 'tool_search_tool_regex_20251119',
            'name' => 'tool_search_tool_regex',
        ],
        [
            'name' => 'get_weather',
            'description' => 'Get the weather at a specific location',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'location' => ['type' => 'string'],
                    'unit' => [
                        'type' => 'string',
                        'enum' => ['celsius', 'fahrenheit'],
                    ],
                ],
                'required' => ['location'],
            ],
            'defer_loading' => true,
        ],
        [
            'name' => 'search_files',
            'description' => 'Search through files in the workspace',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'query' => ['type' => 'string'],
                    'file_types' => [
                        'type' => 'array',
                        'items' => ['type' => 'string'],
                    ],
                ],
                'required' => ['query'],
            ],
            'defer_loading' => true,
        ],
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 2048,
  messages: [
    { role: "user", content: "What is the weather in San Francisco?" }
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
)

puts message
```

</CodeGroup>

## Definisi alat

Alat pencarian alat memiliki dua varian:

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
**Format kueri varian Regex: Regex Python, BUKAN bahasa alami**

Saat menggunakan `tool_search_tool_regex_20251119`, Claude membuat pola regex menggunakan sintaks `re.search()` Python, bukan kueri bahasa alami. Pola umum:

- `"weather"` - cocok dengan nama alat/deskripsi yang berisi "weather"
- `"get_.*_data"` - cocok dengan alat seperti `get_user_data`, `get_weather_data`
- `"database.*query|query.*database"` - pola OR untuk fleksibilitas
- `"(?i)slack"` - pencarian tidak peka huruf besar-kecil

Panjang kueri maksimal: 200 karakter

</Warning>

<Note>
**Format kueri varian BM25: Bahasa alami**

Saat menggunakan `tool_search_tool_bm25_20251119`, Claude menggunakan kueri bahasa alami untuk mencari alat.

</Note>

### Pemuatan alat yang ditangguhkan

Tandai alat untuk pemuatan sesuai permintaan dengan menambahkan `defer_loading: true`:

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

**Poin kunci:**

- Alat tanpa `defer_loading` dimuat ke konteks segera
- Alat dengan `defer_loading: true` hanya dimuat ketika Claude menemukannya melalui pencarian
- Alat pencarian alat itu sendiri **tidak boleh** memiliki `defer_loading: true`
- Pertahankan 3-5 alat yang paling sering digunakan sebagai non-deferred untuk kinerja optimal

Kedua varian pencarian alat (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

**Cara penundaan bekerja secara internal:** Alat yang ditangguhkan tidak disertakan dalam awalan system-prompt. Ketika model menemukan alat yang ditangguhkan melalui pencarian alat, definisi alat ditambahkan secara inline sebagai blok `tool_reference` dalam percakapan. Awalan tidak tersentuh, sehingga caching prompt dipertahankan. Tata bahasa untuk mode ketat dibangun dari set alat lengkap, jadi `defer_loading` dan mode ketat bersusun tanpa kompilasi ulang tata bahasa.

## Format respons

Ketika Claude menggunakan alat pencarian alat, respons mencakup jenis blok baru:

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

- **`server_tool_use`:** Menunjukkan Claude menginvokan alat pencarian alat
- **`tool_search_tool_result`:** Berisi hasil pencarian dengan objek `tool_search_tool_search_result` bersarang
- **`tool_references`:** Array objek `tool_reference` yang menunjuk ke alat yang ditemukan
- **`tool_use`:** Claude menginvokan alat yang ditemukan

Blok `tool_reference` secara otomatis diperluas menjadi definisi alat lengkap sebelum ditampilkan kepada Claude. Anda tidak perlu menangani ekspansi ini sendiri. Ini terjadi secara otomatis di API selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

## Integrasi MCP

Untuk mengonfigurasi `mcp_toolset` dengan `defer_loading`, lihat [Konektor MCP](/docs/id/agents-and-tools/mcp-connector).

## Implementasi pencarian alat khusus

Anda dapat menerapkan logika pencarian alat Anda sendiri (misalnya, menggunakan embeddings atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat khusus. Ketika Claude memanggil alat pencarian khusus Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas dengan `defer_loading: true`. Pendekatan ini memungkinkan Anda menggunakan algoritma pencarian yang lebih canggih sambil mempertahankan kompatibilitas dengan sistem pencarian alat.

<Note>
Format `tool_search_tool_result` yang ditunjukkan dalam bagian [Format respons](#response-format) adalah format sisi server yang digunakan secara internal oleh pencarian alat bawaan Anthropic. Untuk implementasi sisi klien khusus, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan di atas.
</Note>

Untuk contoh lengkap menggunakan embeddings, lihat [cookbook pencarian alat dengan embeddings](https://platform.claude.com/cookbooks/tool_use).

## Penanganan kesalahan

<Note>
  Alat pencarian alat tidak kompatibel dengan [contoh penggunaan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples).
  Jika Anda perlu memberikan contoh penggunaan alat, gunakan pemanggilan alat standar
  tanpa pencarian alat.
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

**Definisi alat yang hilang:**

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

Kesalahan selama eksekusi alat mengembalikan respons 200 dengan informasi kesalahan dalam badan:

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

- `too_many_requests`: Batas laju terlampaui untuk operasi pencarian alat
- `invalid_pattern`: Pola regex yang salah format
- `pattern_too_long`: Pola melebihi batas 200 karakter
- `unavailable`: Layanan pencarian alat sementara tidak tersedia

### Kesalahan umum

<section title="Kesalahan 400: Semua alat ditangguhkan">

**Penyebab:** Anda menetapkan `defer_loading: true` pada SEMUA alat termasuk alat pencarian

**Perbaikan:** Hapus `defer_loading` dari alat pencarian alat:

```json
{
  "type": "tool_search_tool_regex_20251119", // Tidak ada defer_loading di sini
  "name": "tool_search_tool_regex"
}
```

</section>

<section title="Kesalahan 400: Definisi alat yang hilang">

**Penyebab:** `tool_reference` menunjuk ke alat yang tidak ada dalam array `tools` Anda

**Perbaikan:** Pastikan setiap alat yang dapat ditemukan memiliki definisi lengkap:

```json
{
  "name": "my_tool",
  "description": "Full description here",
  "input_schema": {
    // complete schema
  },
  "defer_loading": true
}
```

</section>

<section title="Claude tidak menemukan alat yang diharapkan">

**Penyebab:** Nama alat atau deskripsi tidak cocok dengan pola regex

**Langkah debug:**

1. Periksa nama alat dan deskripsi. Claude mencari KEDUA bidang
2. Uji pola Anda: `import re; re.search(r"your_pattern", "tool_name")`
3. Ingat pencarian peka huruf besar-kecil secara default (gunakan `(?i)` untuk tidak peka huruf besar-kecil)
4. Claude menggunakan pola luas seperti `".*weather.*"` bukan kecocokan tepat

**Tip:** Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemampuan penemuan

</section>

## Caching prompt

Untuk cara `defer_loading` menjaga caching prompt, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

Sistem secara otomatis memperluas blok `tool_reference` di seluruh riwayat percakapan lengkap, sehingga Claude dapat menggunakan kembali alat yang ditemukan dalam giliran berikutnya tanpa pencarian ulang.

## Streaming

Dengan streaming diaktifkan, Anda akan menerima acara pencarian alat sebagai bagian dari aliran:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "tool_search_tool_regex"}}

// Search query streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"query\":\"weather\"}"}}

// Pause while search executes

// Search results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "tool_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "tool_search_tool_search_result", "tool_references": [{"type": "tool_reference", "tool_name": "get_weather"}]}}}

// Claude continues with discovered tools
```

## Permintaan batch

Anda dapat menyertakan alat pencarian alat dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Operasi pencarian alat melalui Messages Batches API dihargai sama dengan operasi dalam permintaan Messages API reguler.

## Retensi data

Pencarian alat sisi server (alat `tool_search`) mengindeks dan menyimpan data katalog alat (nama alat, deskripsi, dan metadata argumen) di luar respons API segera; data katalog ini disimpan sesuai dengan kebijakan retensi standar Anthropic. Implementasi pencarian alat sisi klien khusus yang menggunakan Messages API standar sepenuhnya memenuhi syarat ZDR.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Batas dan praktik terbaik

### Batas

- **Alat maksimal:** 10.000 alat dalam katalog Anda
- **Hasil pencarian:** Mengembalikan 3-5 alat paling relevan per pencarian
- **Panjang pola:** Maksimal 200 karakter untuk pola regex
- **Dukungan model:** [Claude Mythos Preview](https://anthropic.com/glasswing), Sonnet 4.0+, Opus 4.0+ saja (tidak ada Haiku)

### Kapan menggunakan pencarian alat

**Kasus penggunaan yang baik:**

- 10+ alat tersedia di sistem Anda
- Definisi alat mengonsumsi >10k token
- Mengalami masalah akurasi pemilihan alat dengan set alat besar
- Membangun sistem bertenaga MCP dengan beberapa server (200+ alat)
- Perpustakaan alat berkembang seiring waktu

**Kapan pemanggilan alat tradisional mungkin lebih baik:**

- Kurang dari 10 alat total
- Semua alat sering digunakan dalam setiap permintaan
- Definisi alat sangat kecil (\<100 token total)

### Tips optimasi

- Pertahankan 3-5 alat yang paling sering digunakan sebagai non-deferred
- Tulis nama dan deskripsi alat yang jelas dan deskriptif
- Gunakan penamaan konsisten dalam nama alat: awali dengan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga kueri pencarian secara alami menampilkan grup alat yang tepat
- Gunakan kata kunci semantik dalam deskripsi yang cocok dengan cara pengguna mendeskripsikan tugas
- Tambahkan bagian system prompt yang mendeskripsikan kategori alat yang tersedia: "Anda dapat mencari alat untuk berinteraksi dengan Slack, GitHub, dan Jira"
- Pantau alat mana yang Claude temukan untuk menyempurnakan deskripsi

## Penggunaan

Penggunaan alat pencarian alat dilacak dalam objek penggunaan respons:

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

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Referensi alat" icon="list" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Katalog alat lengkap dengan kompatibilitas model dan parameter.
  </Card>
  <Card title="Konektor MCP" icon="plug" href="/docs/id/agents-and-tools/mcp-connector">
    Konfigurasi toolset MCP dengan pemuatan yang ditangguhkan.
  </Card>
  <Card title="Caching prompt" icon="bolt" href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Gabungkan pencarian alat dengan definisi alat yang di-cache.
  </Card>
  <Card title="Tentukan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Panduan langkah demi langkah untuk mendefinisikan alat.
  </Card>
</CardGroup>