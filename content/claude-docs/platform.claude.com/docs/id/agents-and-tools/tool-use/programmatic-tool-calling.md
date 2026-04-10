---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 0fb86ea21f92e62d083fe4ced57caaf0f752dead526fb8d5f789cc936e40da22
---

# Pemanggilan alat secara programatik

Pelajari cara Claude memanggil alat secara programatik dalam container eksekusi kode untuk mengurangi latensi dan konsumsi token.

---

Pemanggilan alat secara programatik memungkinkan Claude menulis kode yang memanggil alat Anda secara programatik dalam container [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), daripada memerlukan perjalanan bolak-balik melalui model untuk setiap pemanggilan alat. Ini mengurangi latensi untuk alur kerja multi-alat dan mengurangi konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum mencapai jendela konteks model. Pada benchmark pencarian agentic seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji penelitian web multi-langkah dan pengambilan informasi yang kompleks, menambahkan pemanggilan alat secara programatik di atas alat pencarian dasar adalah faktor kunci yang sepenuhnya membuka kinerja agen.

Perbedaannya bertambah cepat dalam alur kerja nyata. Pertimbangkan pemeriksaan kepatuhan anggaran di 20 karyawan: pendekatan tradisional memerlukan 20 perjalanan bolak-balik model yang terpisah, menarik ribuan item baris pengeluaran ke dalam konteks di sepanjang jalan. Dengan pemanggilan alat secara programatik, satu skrip menjalankan semua 20 pencarian, memfilter hasilnya, dan hanya mengembalikan karyawan yang melebihi batas mereka, menyusutkan apa yang perlu dipertimbangkan Claude dari ratusan kilobyte menjadi beberapa baris.

<Tip>
Untuk melihat lebih dalam biaya inferensi dan konteks yang ditangani oleh pemanggilan alat secara programatik, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
Fitur ini memerlukan alat eksekusi kode untuk diaktifkan.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Kompatibilitas model

Untuk detail kompatibilitas model dan versi alat, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference). Pemanggilan alat secara programatik tersedia melalui Claude API dan Microsoft Foundry.

## Mulai cepat

Berikut adalah contoh sederhana di mana Claude secara programatik mengkueri database beberapa kali dan mengagregasi hasilnya:

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

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: >-
      Query sales data for the West, East, and Central regions, then
      tell me which region had the highest revenue
tools:
  - type: code_execution_20260120
    name: code_execution
  - name: query_database
    description: >-
      Execute a SQL query against the sales database. Returns a list
      of rows as JSON objects.
    input_schema:
      type: object
      properties:
        sql:
          type: string
          description: SQL query to execute
      required:
        - sql
    allowed_callers:
      - code_execution_20260120
YAML
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

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.messages.create({
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
          type: "object" as const,
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

```csharp C#
using Anthropic;
using Anthropic.Models.Messages;
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
            MaxTokens = 4096,
            Messages = [
                new() {
                    Role = Role.User,
                    Content = "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
                }
            ],
            Tools = [
                new CodeExecutionTool20260120(),
                new ToolUnion(new Tool()
                {
                    Name = "query_database",
                    Description = "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                    InputSchema = new InputSchema()
                    {
                        Properties = new Dictionary<string, JsonElement>
                        {
                            ["sql"] = JsonSerializer.SerializeToElement(new { type = "string", description = "SQL query to execute" }),
                        },
                        Required = ["sql"],
                    },
                    AllowedCallers = ["code_execution_20260120"]
                }),
            ]
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..13,-1}
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
		MaxTokens: 4096,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
			{OfTool: &anthropic.ToolParam{
				Name:        "query_database",
				Description: anthropic.String("Execute a SQL query against the sales database. Returns a list of rows as JSON objects."),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"sql": map[string]any{
							"type":        "string",
							"description": "SQL query to execute",
						},
					},
					Required: []string{"sql"},
				},
				AllowedCallers: []string{"code_execution_20260120"},
			}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..7,9..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.CodeExecutionTool20260120;
import java.util.List;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-opus-4-6")
            .maxTokens(4096L)
            .addUserMessage("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")
            .addTool(CodeExecutionTool20260120.builder().build())
            .addTool(Tool.builder()
                .name("query_database")
                .description("Execute a SQL query against the sales database. Returns a list of rows as JSON objects.")
                .inputSchema(InputSchema.builder()
                    .properties(JsonValue.from(Map.of(
                        "sql", Map.of(
                            "type", "string",
                            "description", "SQL query to execute"
                        )
                    )))
                    .putAdditionalProperty("required", JsonValue.from(List.of("sql")))
                    .build())
                .allowedCallers(List.of(Tool.AllowedCaller.of("code_execution_20260120")))
                .build())
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue'],
    ],
    model: 'claude-opus-4-6',
    tools: [
        [
            'type' => 'code_execution_20260120',
            'name' => 'code_execution',
        ],
        [
            'name' => 'query_database',
            'description' => 'Execute a SQL query against the sales database. Returns a list of rows as JSON objects.',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'sql' => [
                        'type' => 'string',
                        'description' => 'SQL query to execute',
                    ],
                ],
                'required' => ['sql'],
            ],
            'allowed_callers' => ['code_execution_20260120'],
        ],
    ],
);

echo $message;
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
    }
  ],
  tools: [
    {
      type: "code_execution_20260120",
      name: "code_execution"
    },
    {
      name: "query_database",
      description: "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
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
)

puts message
```
</CodeGroup>

## Cara kerja pemanggilan alat secara programatik

Ketika Anda mengonfigurasi alat agar dapat dipanggil dari eksekusi kode dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat sebagai fungsi, berpotensi mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini dalam container yang terisolasi melalui eksekusi kode
3. Ketika fungsi alat dipanggil, eksekusi kode dijeda dan API mengembalikan blok `tool_use`
4. Anda menyediakan hasil alat, dan eksekusi kode berlanjut (hasil antara tidak dimuat ke dalam jendela konteks Claude)
5. Setelah semua eksekusi kode selesai, Claude menerima output akhir dan melanjutkan mengerjakan tugas

Pendekatan ini sangat berguna untuk:
- **Pemrosesan data besar:** Filter atau agregasi hasil alat sebelum mencapai konteks Claude
- **Alur kerja multi-langkah:** Hemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa mengambil sampel Claude di antara pemanggilan alat
- **Logika kondisional:** Membuat keputusan berdasarkan hasil alat antara

<Note>
Alat kustom dikonversi menjadi fungsi Python async untuk mendukung pemanggilan alat paralel. Ketika Claude menulis kode yang memanggil alat Anda, ia menggunakan `await` (misalnya, `result = await query_database("<sql>")`) dan secara otomatis menyertakan fungsi pembungkus async yang sesuai.

Fungsi pembungkus async dihilangkan dari contoh kode dalam dokumentasi ini untuk kejelasan.
</Note>

## Konsep inti

### Field `allowed_callers`

Field `allowed_callers` menentukan konteks mana yang dapat memanggil alat:

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

### Field `caller` dalam respons

Setiap blok penggunaan alat menyertakan field `caller` yang menunjukkan bagaimana alat dipanggil:

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

**Pemanggilan programatik:**
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

`tool_id` mereferensikan alat eksekusi kode yang melakukan pemanggilan programatik.

### Siklus hidup container

Pemanggilan alat secara programatik menggunakan container yang sama dengan eksekusi kode:

- **Pembuatan container:** Container baru dibuat untuk setiap sesi kecuali Anda menggunakan kembali yang sudah ada
- **Kedaluwarsa:** Container memiliki masa hidup maksimum 30 hari dan dibersihkan setelah 4,5 menit tidak aktif
- **ID container:** Dikembalikan dalam respons melalui field `container`
- **Penggunaan ulang:** Berikan ID container untuk mempertahankan status di seluruh permintaan

<Warning>
Ketika alat dipanggil secara programatik dan container menunggu hasil alat Anda, Anda harus merespons sebelum container kedaluwarsa. Pantau field `expires_at`. Jika container kedaluwarsa, Claude mungkin memperlakukan pemanggilan alat sebagai waktu habis dan mencoba lagi.
</Warning>

## Contoh alur kerja

Berikut adalah cara kerja alur pemanggilan alat secara programatik yang lengkap:

### Langkah 1: Permintaan awal

Kirim permintaan dengan eksekusi kode dan alat yang memungkinkan pemanggilan programatik. Untuk mengaktifkan pemanggilan programatik, tambahkan field `allowed_callers` ke definisi alat Anda.

<Note>
Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude mencoba melakukan deserialisasi dan memproses hasilnya dalam kode. Semakin banyak detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara programatik.
</Note>

Bentuk permintaan identik dengan contoh [Mulai cepat](#quick-start): sertakan `code_execution` dalam daftar alat Anda, tambahkan `allowed_callers: ["code_execution_20260120"]` ke alat mana pun yang ingin Anda panggil Claude dari kode, dan kirim pesan pengguna Anda.

### Langkah 2: Respons API dengan pemanggilan alat

Claude menulis kode yang memanggil alat Anda. API dijeda dan mengembalikan:

```json Output
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

### Langkah 3: Berikan hasil tool

Sertakan riwayat percakapan lengkap beserta hasil tool Anda:

<CodeGroup>

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container: container_xyz789
messages:
  - role: user
    content: >-
      Query customer purchase history from the last quarter and identify our
      top 5 customers by revenue
  - role: assistant
    content:
      - type: text
        text: I'll query the purchase history and analyze the results.
      - type: server_tool_use
        id: srvtoolu_abc123
        name: code_execution
        input:
          code: "..."
      - type: tool_use
        id: toolu_def456
        name: query_database
        input:
          sql: "<sql>"
        caller:
          type: code_execution_20260120
          tool_id: srvtoolu_abc123
  - role: user
    content:
      - type: tool_result
        tool_use_id: toolu_def456
        content: >-
          [{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2",
          "revenue": 38000}, ...]
tools: [...]
YAML
```

```python Python nocheck
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    container="container_xyz789",  # Reuse the container
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

print(response)
```

```typescript TypeScript nocheck
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  container: "container_xyz789", // Reuse the container
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
    /* ... */
  ]
});

console.log(response);
```

```csharp C# nocheck
using System;
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
            Model = Model.ClaudeOpus4_6,
            MaxTokens = 4096,
            Container = "container_xyz789",
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
                },
                new()
                {
                    Role = Role.Assistant,
                    Content = new ContentBlock[]
                    {
                        new TextBlock { Text = "I'll query the purchase history and analyze the results." },
                        new ServerToolUseBlock
                        {
                            Id = "srvtoolu_abc123",
                            Name = "code_execution",
                            Input = new { code = "..." }
                        },
                        new ToolUseBlock
                        {
                            Id = "toolu_def456",
                            Name = "query_database",
                            Input = new { sql = "<sql>" },
                            Caller = new ToolCaller
                            {
                                Type = "code_execution_20260120",
                                ToolId = "srvtoolu_abc123"
                            }
                        }
                    }
                },
                new()
                {
                    Role = Role.User,
                    Content = new ContentBlockParam[]
                    {
                        new ToolResultBlockParam
                        {
                            ToolUseID = "toolu_def456",
                            Content = "[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]"
                        }
                    }
                }
            ],
            Tools = []
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go nocheck hidelines={1..13,-1}
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
		MaxTokens: 4096,
		Container: anthropic.MessageNewParamsContainerUnion{
			OfString: anthropic.String("container_xyz789"),
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")),
			{
				Role: anthropic.MessageParamRoleAssistant,
				Content: []anthropic.ContentBlockParamUnion{
					anthropic.NewTextBlock("I'll query the purchase history and analyze the results."),
					{OfServerToolUse: &anthropic.ServerToolUseBlockParam{
						ID:    "srvtoolu_abc123",
						Name:  anthropic.ServerToolUseBlockParamNameCodeExecution,
						Input: map[string]any{"code": "..."},
					}},
					{OfToolUse: &anthropic.ToolUseBlockParam{
						ID:    "toolu_def456",
						Name:  "query_database",
						Input: map[string]any{"sql": "<sql>"},
						Caller: anthropic.ServerToolUseBlockParamCallerUnion{
							OfCodeExecution20260120: &anthropic.ServerToolCaller20260120Param{
								ToolID: "srvtoolu_abc123",
							},
						},
					}},
				},
			},
			{
				Role: anthropic.MessageParamRoleUser,
				Content: []anthropic.ContentBlockParamUnion{
					{OfToolResult: &anthropic.ToolResultBlockParam{
						ToolUseID: "toolu_def456",
						Content: []anthropic.ToolResultBlockParamContentUnion{
							{OfText: &anthropic.TextBlockParam{
								Text: `[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]`,
							}},
						},
					}},
				},
			},
		},
		Tools: []anthropic.ToolUnionParam{
			{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..3,5..8,10..17,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.CodeExecutionTool20260120;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ServerToolUseBlockParam;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlockParam;
import java.util.List;
import java.util.Map;

public class ContainerReuse {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(4096L)
            .container("container_xyz789")
            .addUserMessage("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")
            .addAssistantMessageOfBlockParams(List.of(
                ContentBlockParam.ofText(
                    TextBlockParam.builder()
                        .text("I'll query the purchase history and analyze the results.")
                        .build()),
                ContentBlockParam.ofServerToolUse(
                    ServerToolUseBlockParam.builder()
                        .id("srvtoolu_abc123")
                        .name("code_execution")
                        .input(JsonValue.from(Map.of("code", "...")))
                        .build()),
                ContentBlockParam.ofToolUse(
                    ToolUseBlockParam.builder()
                        .id("toolu_def456")
                        .name("query_database")
                        .input(JsonValue.from(Map.of("sql", "<sql>")))
                        .codeExecution20260120Caller("srvtoolu_abc123")
                        .build())
            ))
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofToolResult(
                    ToolResultBlockParam.builder()
                        .toolUseId("toolu_def456")
                        .content("[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]")
                        .build())
            ))
            .addTool(CodeExecutionTool20260120.builder().build())
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..6} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        [
            'role' => 'user',
            'content' => 'Query customer purchase history from the last quarter and identify our top 5 customers by revenue',
        ],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'text',
                    'text' => "I'll query the purchase history and analyze the results.",
                ],
                [
                    'type' => 'server_tool_use',
                    'id' => 'srvtoolu_abc123',
                    'name' => 'code_execution',
                    'input' => ['code' => '...'],
                ],
                [
                    'type' => 'tool_use',
                    'id' => 'toolu_def456',
                    'name' => 'query_database',
                    'input' => ['sql' => '<sql>'],
                    'caller' => [
                        'type' => 'code_execution_20260120',
                        'tool_id' => 'srvtoolu_abc123',
                    ],
                ],
            ],
        ],
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'tool_result',
                    'tool_use_id' => 'toolu_def456',
                    'content' => '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                ],
            ],
        ],
    ],
    model: 'claude-opus-4-6',
    container: 'container_xyz789',
    tools: [],
);

echo $message;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 4096,
  container: "container_xyz789",
  messages: [
    {
      role: "user",
      content: "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I'll query the purchase history and analyze the results."
        },
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
          content: '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
        }
      ]
    }
  ],
  tools: [
    { type: "code_execution_20260120", name: "code_execution" }
  ]
)
puts message
```
</CodeGroup>

### Langkah 4: Panggilan tool berikutnya atau penyelesaian

Eksekusi kode berlanjut dan memproses hasilnya. Jika diperlukan panggilan tool tambahan, ulangi Langkah 3 hingga semua panggilan tool terpenuhi.

### Langkah 5: Respons akhir

Setelah eksekusi kode selesai, Claude memberikan respons akhir:

```json Output
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

```python hidelines={1..4,-1}
async def query_database(sql):
    return [{"revenue": 100}]


async def _claude_code():
    regions = ["West", "East", "Central", "North", "South"]
    results = {}
    for region in regions:
        data = await query_database(f"<sql for {region}>")
        results[region] = sum(row["revenue"] for row in data)

    # Process results programmatically
    top_region = max(results.items(), key=lambda x: x[1])
    print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")


_ = _claude_code
```

Pola ini:
- Mengurangi round-trip model dari N (satu per wilayah) menjadi 1
- Memproses kumpulan hasil yang besar secara terprogram sebelum dikembalikan ke Claude
- Menghemat token dengan hanya mengembalikan kesimpulan yang diagregasi, bukan data mentah

### Penghentian awal

Claude dapat berhenti memproses segera setelah kriteria keberhasilan terpenuhi:

```python hidelines={1..4,-1}
async def check_health(ep):
    return "healthy"


async def _claude_code():
    endpoints = ["us-east", "eu-west", "apac"]
    for endpoint in endpoints:
        status = await check_health(endpoint)
        if status == "healthy":
            print(f"Found healthy endpoint: {endpoint}")
            break  # Stop early, don't check remaining


_ = _claude_code
```

### Pemilihan tool bersyarat

```python hidelines={1..15,-1}
async def get_file_info(p):
    return {"size": 500}


async def read_full_file(p):
    return "content"


async def read_file_summary(p):
    return "summary"


path = "/tmp/example.txt"


async def _claude_code():
    file_info = await get_file_info(path)
    if file_info["size"] < 10000:
        content = await read_full_file(path)
    else:
        content = await read_file_summary(path)
    print(content)


_ = _claude_code
```

### Pemfilteran data

```python hidelines={1..7,-1}
async def fetch_logs(sid):
    return ["INFO: ok", "ERROR: failed"]


server_id = "srv-01"


async def _claude_code():
    logs = await fetch_logs(server_id)
    errors = [log for log in logs if "ERROR" in log]
    print(f"Found {len(errors)} errors")
    for error in errors[-10:]:  # Only return last 10 errors
        print(error)


_ = _claude_code
```

## Format respons

### Panggilan tool terprogram

Ketika eksekusi kode memanggil sebuah tool:

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

### Penanganan hasil tool

Hasil tool Anda diteruskan kembali ke kode yang sedang berjalan:

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

Ketika semua panggilan tool terpenuhi dan kode selesai:

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
| `invalid_tool_input` | Input tool tidak sesuai dengan skema | Validasi input_schema tool Anda |
| `tool_not_allowed` | Tool tidak mengizinkan tipe caller yang diminta | Periksa `allowed_callers` menyertakan konteks yang tepat |
| `missing_beta_header` | Header beta yang diperlukan tidak disediakan (hanya Bedrock dan Vertex AI; pemanggilan tool terprogram sudah GA di Claude API pihak pertama) | Tambahkan header beta yang diperlukan ke permintaan Anda |

### Kedaluwarsa container selama panggilan tool

Jika tool Anda membutuhkan waktu terlalu lama untuk merespons, eksekusi kode menerima `TimeoutError`. Claude melihat ini di stderr dan biasanya mencoba ulang:

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
- Pantau field `expires_at` dalam respons
- Implementasikan timeout untuk eksekusi tool Anda
- Pertimbangkan untuk memecah operasi yang panjang menjadi potongan yang lebih kecil

### Error eksekusi tool

Jika tool Anda mengembalikan error:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_abc123",
  "content": "Error: Query timeout - table lock exceeded 30 seconds"
}
```

Kode Claude menerima error ini dan dapat menanganinya dengan tepat.

## Batasan dan keterbatasan

### Ketidakcocokan fitur

- **Output terstruktur:** Tool dengan `strict: true` tidak didukung dengan pemanggilan terprogram
- **Pilihan tool:** Anda tidak dapat memaksa pemanggilan terprogram tool tertentu melalui `tool_choice`
- **Penggunaan tool paralel:** `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Pembatasan tool

Tool-tool berikut saat ini tidak dapat dipanggil secara terprogram, tetapi dukungan mungkin ditambahkan di rilis mendatang:

- Tool yang disediakan oleh [konektor MCP](/docs/id/agents-and-tools/mcp-connector)

### Pembatasan format pesan

Saat merespons panggilan tool terprogram, ada persyaratan format yang ketat:

**Respons hanya hasil tool:** Jika ada panggilan tool terprogram yang menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil tool.

Tidak valid - Tidak dapat menyertakan teks saat merespons panggilan tool terprogram:

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

Valid - Hanya hasil tool saat merespons panggilan tool terprogram:

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

Pembatasan ini hanya berlaku saat merespons panggilan tool terprogram (eksekusi kode). Untuk panggilan tool sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil tool.

### Batas rate

Panggilan tool terprogram tunduk pada batas rate yang sama dengan panggilan tool biasa. Setiap panggilan tool dari eksekusi kode dihitung sebagai pemanggilan terpisah.

### Validasi hasil tool sebelum digunakan

Saat mengimplementasikan tool yang ditentukan pengguna yang akan dipanggil secara terprogram:

- **Hasil tool dikembalikan sebagai string:** Dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang mungkin diproses oleh lingkungan eksekusi.
- **Validasi hasil tool eksternal:** Jika tool Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan diinterpretasikan atau dieksekusi sebagai kode.

## Efisiensi token

Pemanggilan tool terprogram dapat secara signifikan mengurangi konsumsi token:

- **Hasil tool dari panggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir yang ditambahkan
- **Pemrosesan perantara terjadi dalam kode** - pemfilteran, agregasi, dll. tidak mengonsumsi token model
- **Beberapa panggilan tool dalam satu eksekusi kode** - mengurangi overhead dibandingkan dengan giliran model terpisah

Misalnya, memanggil 10 tool secara langsung menggunakan ~10x token dibandingkan memanggilnya secara terprogram dan mengembalikan ringkasan.

## Penggunaan dan harga

Pemanggilan tool terprogram menggunakan harga yang sama dengan eksekusi kode. Lihat [harga eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detailnya.

<Note>
Penghitungan token untuk panggilan tool terprogram: Hasil tool dari pemanggilan terprogram tidak dihitung terhadap penggunaan token input/output Anda. Hanya hasil eksekusi kode akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik

### Desain tool

- **Berikan deskripsi output yang terperinci:** Karena Claude mendeserialisasi hasil tool dalam kode, dokumentasikan format dengan jelas (struktur JSON, tipe field, dll.)
- **Kembalikan data terstruktur:** JSON atau format yang mudah diurai lainnya bekerja paling baik untuk pemrosesan terprogram
- **Jaga respons tetap ringkas:** Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram

**Kasus penggunaan yang baik:**
- Memproses kumpulan data besar di mana Anda hanya membutuhkan agregat atau ringkasan
- Alur kerja multi-langkah dengan 3+ panggilan tool yang bergantung
- Operasi yang memerlukan pemfilteran, pengurutan, atau transformasi hasil tool
- Tugas di mana data perantara tidak boleh memengaruhi penalaran Claude
- Operasi paralel di banyak item (misalnya, memeriksa 50 endpoint)

**Kasus penggunaan yang kurang ideal:**
- Panggilan tool tunggal dengan respons sederhana
- Tool yang memerlukan umpan balik pengguna segera
- Operasi yang sangat cepat di mana overhead eksekusi kode akan melebihi manfaatnya

### Optimasi performa

- **Gunakan ulang container** saat membuat beberapa permintaan terkait untuk mempertahankan status
- **Kelompokkan operasi serupa** dalam satu eksekusi kode jika memungkinkan

## Pemecahan masalah

### Masalah umum

**Error "Tool not allowed"**
- Verifikasi definisi tool Anda menyertakan `"allowed_callers": ["code_execution_20260120"]`

**Kedaluwarsa container**
- Pastikan Anda merespons panggilan tool sebelum container menjadi idle (4,5 menit tidak aktif; maksimum keras 30 hari)
- Pantau field `expires_at` dalam respons
- Pertimbangkan untuk mengimplementasikan eksekusi tool yang lebih cepat

**Hasil tool tidak diurai dengan benar**
- Pastikan tool Anda mengembalikan data string yang dapat dideserialisasi oleh Claude
- Berikan dokumentasi format output yang jelas dalam deskripsi tool Anda

### Tips debugging

1. **Catat semua panggilan tool dan hasilnya** untuk melacak alur
2. **Periksa field `caller`** untuk mengonfirmasi pemanggilan terprogram
3. **Pantau ID container** untuk memastikan penggunaan ulang yang tepat
4. **Uji tool secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan tool terprogram bekerja

Pelatihan Claude mencakup paparan ekstensif terhadap kode, membuatnya efektif dalam menalar dan merantai panggilan fungsi. Ketika tool disajikan sebagai fungsi yang dapat dipanggil dalam lingkungan eksekusi kode, Claude dapat memanfaatkan kekuatan ini untuk:

- **Menalar secara alami tentang komposisi tool:** Merantai operasi dan menangani dependensi senatural menulis kode Python apa pun
- **Memproses hasil besar secara efisien:** Memfilter output tool yang besar, mengekstrak hanya data yang relevan, atau menulis hasil perantara ke file sebelum mengembalikan ringkasan ke jendela konteks
- **Mengurangi latensi secara signifikan:** Menghilangkan overhead pengambilan sampel ulang Claude di antara setiap panggilan tool dalam alur kerja multi-langkah

Pendekatan ini memungkinkan alur kerja yang tidak praktis dengan penggunaan tool tradisional (seperti memproses file lebih dari 1 juta token) dengan memungkinkan Claude bekerja dengan data secara terprogram daripada memuat semuanya ke dalam konteks percakapan.

## Implementasi alternatif

Pemanggilan tool terprogram adalah pola yang dapat digeneralisasi yang dapat diimplementasikan di luar eksekusi kode terkelola Anthropic. Berikut adalah ikhtisar pendekatannya:

### Eksekusi langsung sisi klien

Berikan Claude tool eksekusi kode dan jelaskan fungsi apa yang tersedia di lingkungan tersebut. Ketika Claude memanggil tool dengan kode, aplikasi Anda mengeksekusinya secara lokal di mana fungsi-fungsi tersebut didefinisikan.

**Keuntungan:**
- Mudah diimplementasikan dengan perubahan arsitektur minimal
- Kontrol penuh atas lingkungan dan instruksi

**Kerugian:**
- Mengeksekusi kode yang tidak tepercaya di luar sandbox
- Pemanggilan tool dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat mengeksekusi kode arbitrer dengan aman, Anda menginginkan solusi sederhana, dan penawaran terkelola Anthropic tidak sesuai kebutuhan Anda.

### Eksekusi sandbox yang dikelola sendiri

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan dalam container sandbox dengan pembatasan keamanan (misalnya, tidak ada egress jaringan). Jika tool Anda memerlukan sumber daya eksternal, Anda memerlukan protokol untuk mengeksekusi panggilan tool di luar sandbox.

**Keuntungan:**
- Pemanggilan tool terprogram yang aman di infrastruktur Anda sendiri
- Kontrol penuh atas lingkungan eksekusi

**Kerugian:**
- Kompleks untuk dibangun dan dipelihara
- Memerlukan pengelolaan infrastruktur dan komunikasi antar-proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai kebutuhan Anda.

### Eksekusi terkelola Anthropic

Pemanggilan tool terprogram Anthropic adalah versi terkelola dari eksekusi sandbox dengan lingkungan Python yang teropini dan disetel untuk Claude. Anthropic menangani manajemen container, eksekusi kode, dan komunikasi pemanggilan tool yang aman.

**Keuntungan:**
- Aman dan terjamin secara default
- Mudah diaktifkan dengan konfigurasi minimal
- Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan untuk menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API.

## Retensi data

Pemanggilan tool terprogram dibangun di atas infrastruktur eksekusi kode dan menggunakan container sandbox yang sama. Data container, termasuk artefak dan output eksekusi, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [retensi API dan data](/docs/id/build-with-claude/api-and-data-retention).

## Fitur terkait

<CardGroup cols={2}>
  <Card title="Tool Eksekusi Kode" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Pelajari tentang kemampuan eksekusi kode yang mendasari yang mendukung pemanggilan tool terprogram.
  </Card>
  <Card title="Ikhtisar Penggunaan Tool" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Pahami dasar-dasar penggunaan tool dengan Claude.
  </Card>
  <Card title="Definisikan tool" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Panduan langkah demi langkah untuk mendefinisikan tool.
  </Card>
</CardGroup>