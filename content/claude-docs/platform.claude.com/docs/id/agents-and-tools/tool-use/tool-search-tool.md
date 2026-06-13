---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 45250a9db811e066dc83cbb07f169041d0597ec7c8bd3e16a292bb11784578a8
---

# Alat pencarian alat

---

Alat pencarian alat memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuatnya secara dinamis sesuai kebutuhan. Alih-alih memuat semua definisi alat ke dalam "context window" (jendela konteks) di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan hanya memuat alat yang dibutuhkannya.

Pendekatan ini menyelesaikan dua masalah yang dengan cepat menjadi semakin parah seiring bertambahnya skala pustaka alat:

- **Pembengkakan konteks:** Definisi alat dengan cepat menghabiskan anggaran konteks Anda. Pengaturan multi-server yang umum (GitHub, Slack, Sentry, Grafana, Splunk) dapat menghabiskan ~55k token dalam definisi sebelum Claude melakukan pekerjaan apa pun. Pencarian alat biasanya mengurangi ini lebih dari 85%, hanya memuat 3–5 alat yang benar-benar dibutuhkan Claude untuk permintaan tertentu.
- **Akurasi pemilihan alat:** Kemampuan Claude untuk memilih alat yang tepat menurun secara signifikan setelah Anda melebihi 30–50 alat yang tersedia. Dengan menampilkan sekumpulan alat relevan yang terfokus sesuai kebutuhan, pencarian alat menjaga akurasi pemilihan tetap tinggi bahkan di antara ribuan alat.

<Tip>
Untuk latar belakang tentang tantangan penskalaan yang diselesaikan oleh pencarian alat, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai kebutuhan pada pencarian alat juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Meskipun ini disediakan sebagai alat sisi server, Anda juga dapat mengimplementasikan fungsionalitas pencarian alat sisi klien Anda sendiri. Lihat [Implementasi pencarian alat kustom](#implementasi-pencarian-alat-kustom) untuk detailnya.

<Note>
Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA).
</Note>

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

<Warning>
  Di Amazon Bedrock, pencarian alat sisi server hanya tersedia melalui
  [InvokeModel
  API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html),
  bukan Converse API.
</Warning>

<Note>
Di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), pencarian alat sisi server bekerja secara identik dengan Claude API. Claude Platform on AWS menggunakan Anthropic Messages API secara langsung, sehingga tidak ada perbedaan antara InvokeModel atau Converse.
</Note>

## Cara kerja pencarian alat \{#how-tool-search-works}

Ada dua varian pencarian alat:

- **Regex** (`tool_search_tool_regex_20251119`): Claude menyusun pola regex untuk mencari alat
- **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat

Ketika Anda mengaktifkan alat pencarian alat:

1. Anda menyertakan alat pencarian alat (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar alat Anda.
2. Anda menyediakan semua definisi alat dengan `defer_loading: true` untuk alat yang tidak perlu dimuat segera.
3. Claude awalnya hanya melihat alat pencarian alat dan alat apa pun yang tidak ditangguhkan.
4. Ketika Claude membutuhkan alat tambahan, Claude mencari menggunakan alat pencarian alat.
5. API mengembalikan 3-5 blok `tool_reference` yang paling relevan.
6. Referensi ini secara otomatis diperluas menjadi definisi alat lengkap.
7. Claude memilih dari alat yang ditemukan dan memanggilnya.

Ini menjaga jendela konteks Anda tetap efisien sambil mempertahankan akurasi pemilihan alat yang tinggi.

## Mulai cepat \{#quick-start}

Berikut adalah contoh sederhana dengan alat yang ditangguhkan:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
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

console.log(response);
```

```csharp C# hidelines={1..5}
using System;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
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
		Model:     anthropic.ModelClaudeOpus4_8,
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

```java Java hidelines={1..8}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.ToolSearchToolRegex20251119;

void main() {
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
        .model(Model.CLAUDE_OPUS_4_8)
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
    IO.println(response);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 2048,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather in San Francisco?'],
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

## Definisi alat \{#tool-definition}

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
**Format kueri varian regex: Regex Python, BUKAN bahasa alami**

Saat menggunakan `tool_search_tool_regex_20251119`, Claude menyusun pola regex menggunakan sintaks `re.search()` Python, bukan kueri bahasa alami. Pola umum:

- `"weather"` - cocok dengan nama/deskripsi alat yang mengandung "weather"
- `"get_.*_data"` - cocok dengan alat seperti `get_user_data`, `get_weather_data`
- `"database.*query|query.*database"` - pola OR untuk fleksibilitas
- `"(?i)slack"` - pencarian tidak peka huruf besar/kecil

Panjang kueri maksimum: 200 karakter

</Warning>

<Note>
**Format kueri varian BM25: Bahasa alami**

Saat menggunakan `tool_search_tool_bm25_20251119`, Claude menggunakan kueri bahasa alami untuk mencari alat.

</Note>

### Pemuatan alat yang ditangguhkan \{#deferred-tool-loading}

Tandai alat untuk pemuatan sesuai kebutuhan dengan menambahkan `defer_loading: true`:

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

**Poin penting:**

- Alat tanpa `defer_loading` dimuat ke dalam konteks segera
- Alat dengan `defer_loading: true` hanya dimuat ketika Claude menemukannya melalui pencarian
- Alat pencarian alat itu sendiri **tidak boleh** memiliki `defer_loading: true`
- Pertahankan 3-5 alat yang paling sering digunakan sebagai alat yang tidak ditangguhkan untuk kinerja optimal

Kedua varian pencarian alat (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

**Cara kerja penangguhan secara internal:** Alat yang ditangguhkan tidak disertakan dalam prefiks prompt sistem. Ketika model menemukan alat yang ditangguhkan melalui pencarian alat, API menambahkan blok `tool_reference` secara inline dalam percakapan, lalu memperluasnya menjadi definisi alat lengkap sebelum meneruskannya ke Claude. Prefiks tidak tersentuh, sehingga caching prompt tetap terjaga. Tata bahasa untuk [strict mode](/docs/id/agents-and-tools/tool-use/strict-tool-use) (aturan yang membatasi output pemanggilan alat agar sesuai dengan skema Anda) dibangun dari keseluruhan set alat, sehingga `defer_loading` dan strict mode dapat digabungkan tanpa kompilasi ulang tata bahasa.

## Format respons \{#response-format}

Ketika Claude menggunakan alat pencarian alat, respons menyertakan tipe blok baru:

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

### Memahami respons \{#understanding-the-response}

- **`server_tool_use`:** Menunjukkan Claude sedang memanggil alat pencarian alat
- **`tool_search_tool_result`:** Berisi hasil pencarian dengan objek `tool_search_tool_search_result` bersarang
- **`tool_references`:** Array objek `tool_reference` yang menunjuk ke alat yang ditemukan
- **`tool_use`:** Claude memanggil alat yang ditemukan

Blok `tool_reference` secara otomatis diperluas menjadi definisi alat lengkap sebelum ditampilkan ke Claude. Anda tidak perlu menangani perluasan ini sendiri. Ini terjadi secara otomatis di API selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

## Integrasi MCP \{#mcp-integration}

Untuk mengonfigurasi `mcp_toolset` dengan `defer_loading`, lihat [MCP connector](/docs/id/agents-and-tools/mcp-connector).

## Implementasi pencarian alat kustom \{#custom-tool-search-implementation}

Anda dapat mengimplementasikan logika pencarian alat Anda sendiri (misalnya, menggunakan embeddings atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat kustom. Ketika Claude memanggil alat pencarian kustom Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas dengan `defer_loading: true`. Pendekatan ini memungkinkan Anda menggunakan algoritma pencarian yang lebih canggih sambil mempertahankan kompatibilitas dengan sistem pencarian alat.

<Note>
Format `tool_search_tool_result` yang ditampilkan di bagian [Format respons](#format-respons) adalah format sisi server yang digunakan secara internal oleh pencarian alat bawaan Anthropic. Untuk implementasi sisi klien kustom, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan pada contoh sebelumnya.
</Note>

Untuk contoh lengkap menggunakan embeddings, lihat [cookbook pencarian alat dengan embeddings](https://platform.claude.com/cookbooks/tool_use).

## Penanganan error \{#error-handling}

<Note>
  Alat pencarian alat tidak kompatibel dengan [contoh penggunaan
  alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples).
  Jika Anda perlu memberikan contoh penggunaan alat, gunakan pemanggilan alat
  standar tanpa pencarian alat.
</Note>

### Error HTTP (status 400) \{#http-errors-400-status}

Error ini mencegah permintaan diproses:

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

**Definisi alat tidak ada:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Tool reference 'unknown_tool' has no corresponding tool definition"
  }
}
```

### Error hasil alat (status 200) \{#tool-result-errors-200-status}

Error selama eksekusi alat mengembalikan respons 200 dengan informasi error di body:

```json JSON
{
  "type": "tool_search_tool_result",
  "tool_use_id": "srvtoolu_01ABC123",
  "content": {
    "type": "tool_search_tool_result_error",
    "error_code": "invalid_pattern"
  }
}
```

**Kode error:**

- `too_many_requests`: Batas laju terlampaui untuk operasi pencarian alat
- `invalid_pattern`: Pola regex tidak valid
- `pattern_too_long`: Pola melebihi batas 200 karakter
- `unavailable`: Layanan pencarian alat tidak tersedia untuk sementara

### Kesalahan umum \{#common-mistakes}

<section title="Error 400: Semua alat ditangguhkan">

**Penyebab:** Anda mengatur `defer_loading: true` pada SEMUA alat termasuk alat pencarian

**Perbaikan:** Hapus `defer_loading` dari alat pencarian alat:

```json
{
  "type": "tool_search_tool_regex_20251119",
  "name": "tool_search_tool_regex"
}
```

</section>

<section title="Error 400: Definisi alat tidak ada">

**Penyebab:** Sebuah `tool_reference` menunjuk ke alat yang tidak ada dalam array `tools` Anda

**Perbaikan:** Pastikan setiap alat yang dapat ditemukan memiliki definisi lengkap:

```json
{
  "name": "my_tool",
  "description": "Full description here",
  "input_schema": {
    "type": "object"
  },
  "defer_loading": true
}
```

</section>

<section title="Claude tidak menemukan alat yang diharapkan">

**Penyebab:** Nama alat, deskripsi, nama argumen, atau deskripsi argumen tidak cocok dengan pola regex

**Langkah debugging:**

1. Periksa nama alat, deskripsi, nama argumen, dan deskripsi argumen. Claude mencari semua bidang ini.
2. Uji pola Anda: `import re; re.search(r"your_pattern", "tool_name")`.
3. Ingat bahwa pencarian peka huruf besar/kecil secara default (gunakan `(?i)` untuk tidak peka huruf besar/kecil).
4. Claude menggunakan pola luas seperti `".*weather.*"` bukan pencocokan persis.

**Tip:** Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemudahan penemuan

</section>

## Caching prompt \{#prompt-caching}

Untuk mengetahui bagaimana `defer_loading` menjaga caching prompt, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

Sistem secara otomatis memperluas blok `tool_reference` di seluruh riwayat percakapan, sehingga Claude dapat menggunakan kembali alat yang ditemukan pada giliran berikutnya tanpa mencari ulang.

## Streaming \{#streaming}

Dengan streaming diaktifkan, Anda akan menerima event pencarian alat sebagai bagian dari stream:

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

## Permintaan batch \{#batch-requests}

Anda dapat menyertakan alat pencarian alat dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Operasi pencarian alat melalui Messages Batches API dikenakan harga yang sama dengan permintaan Messages API reguler.

## Batasan dan praktik terbaik \{#limits-and-best-practices}

### Batasan \{#limits}

- **Alat maksimum:** 10.000 alat dalam katalog Anda
- **Hasil pencarian:** Mengembalikan 3-5 alat paling relevan per pencarian
- **Panjang pola:** Maksimum 200 karakter untuk pola regex
- **Dukungan model:** Claude Fable 5, Claude Mythos 5, [Claude Mythos Preview](https://anthropic.com/glasswing), Sonnet 4.0+, Opus 4.0+, Haiku 4.5+

### Kapan menggunakan pencarian alat \{#when-to-use-tool-search}

**Kasus penggunaan yang cocok:**

- 10+ alat tersedia dalam sistem Anda
- Definisi alat menghabiskan >10k token
- Mengalami masalah akurasi pemilihan alat dengan set alat yang besar
- Membangun sistem berbasis MCP dengan beberapa server (200+ alat)
- Pustaka alat yang terus bertambah seiring waktu

**Kapan pemanggilan alat tradisional mungkin lebih baik:**

- Kurang dari 10 alat secara total
- Semua alat sering digunakan dalam setiap permintaan
- Definisi alat yang sangat kecil (\<100 token total)

### Tips optimasi \{#optimization-tips}

- Pertahankan 3-5 alat yang paling sering digunakan sebagai alat yang tidak ditangguhkan
- Tulis nama dan deskripsi alat yang jelas dan deskriptif
- Gunakan namespace yang konsisten dalam nama alat: beri prefiks berdasarkan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga kueri pencarian secara alami memunculkan grup alat yang tepat
- Gunakan kata kunci semantik dalam deskripsi yang sesuai dengan cara pengguna mendeskripsikan tugas
- Tambahkan bagian prompt sistem yang menjelaskan kategori alat yang tersedia: "Anda dapat mencari alat untuk berinteraksi dengan Slack, GitHub, dan Jira"
- Pantau alat mana yang ditemukan Claude untuk menyempurnakan deskripsi

## Penggunaan \{#usage}

Penggunaan alat pencarian alat dilacak dalam objek usage respons:

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

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Referensi alat" icon="list" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Katalog alat lengkap dengan kompatibilitas model dan parameter.
  </Card>
  <Card title="MCP connector" icon="plug" href="/docs/id/agents-and-tools/mcp-connector">
    Konfigurasikan toolset MCP dengan pemuatan yang ditangguhkan.
  </Card>
  <Card title="Caching prompt" icon="bolt" href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Gabungkan pencarian alat dengan definisi alat yang di-cache.
  </Card>
  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Panduan langkah demi langkah untuk mendefinisikan alat.
  </Card>
</CardGroup>