---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 56f569fead329d7b247ba3e1c25b8009ab71b717fe0a5d1a3b75a5e44068ec2c
---

# Pemanggilan alat secara terprogram

Memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram dalam kontainer eksekusi kode, mengurangi latensi dan konsumsi token untuk alur kerja multi-alat.

---

Pemanggilan alat secara terprogram memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram dalam kontainer [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), daripada memerlukan putaran bolak-balik melalui model untuk setiap pemanggilan alat. Ini mengurangi latensi untuk alur kerja multi-alat dan mengurangi konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum mencapai jendela konteks model. Pada tolok ukur pencarian agentic seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji penelitian web multi-langkah dan pengambilan informasi kompleks, menambahkan pemanggilan alat secara terprogram di atas alat pencarian dasar adalah faktor kunci yang sepenuhnya membuka kinerja agen.

Perbedaannya berkembang pesat dalam alur kerja nyata. Pertimbangkan memeriksa kepatuhan anggaran di 20 karyawan: pendekatan tradisional memerlukan 20 putaran model terpisah, menarik ribuan item baris pengeluaran ke dalam konteks sepanjang jalan. Dengan pemanggilan alat secara terprogram, satu skrip menjalankan semua 20 pencarian, memfilter hasilnya, dan mengembalikan hanya karyawan yang melampaui batas mereka, menyusutkan apa yang perlu Claude pikirkan dari ratusan kilobyte menjadi beberapa baris.

<Tip>
Untuk melihat lebih dalam biaya inferensi dan konteks yang ditangani oleh pemanggilan alat secara terprogram, lihat [Penggunaan alat tingkat lanjut](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
Fitur ini memerlukan alat eksekusi kode untuk diaktifkan.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Kompatibilitas model

Pemanggilan alat secara terprogram memerlukan `code_execution_20260120`, yang didukung pada model berikut:

| Model |
|-------|
| Claude Opus 4.7 (`claude-opus-4-7`) |
| Claude Opus 4.6 (`claude-opus-4-6`) |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`) |
| Claude Opus 4.5 (`claude-opus-4-5-20251101`) |
| Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) |

Untuk matriks versi alat eksekusi kode lengkap, lihat [tabel kompatibilitas model alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility). Pemanggilan alat secara terprogram tersedia melalui Claude API dan Microsoft Foundry.

## Mulai cepat

Berikut adalah contoh sederhana di mana Claude secara terprogram menanyakan database beberapa kali dan mengagregasi hasil:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
    model: "claude-opus-4-7",
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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model("claude-opus-4-7")
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
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

## Cara kerja pemanggilan alat secara terprogram

Ketika Anda mengonfigurasi alat untuk dapat dipanggil dari eksekusi kode dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat sebagai fungsi, yang berpotensi mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini dalam kontainer bersandal melalui eksekusi kode
3. Ketika fungsi alat dipanggil, eksekusi kode dijeda dan API mengembalikan blok `tool_use`
4. Anda memberikan hasil alat, dan eksekusi kode berlanjut (hasil perantara tidak dimuat ke jendela konteks Claude)
5. Setelah semua eksekusi kode selesai, Claude menerima output akhir dan melanjutkan pekerjaan pada tugas

Pendekatan ini sangat berguna untuk:
- **Pemrosesan data besar:** Memfilter atau mengagregasi hasil alat sebelum mencapai konteks Claude
- **Alur kerja multi-langkah:** Hemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa sampling Claude di antara pemanggilan alat
- **Logika bersyarat:** Buat keputusan berdasarkan hasil alat perantara

<Note>
Alat khusus dikonversi ke fungsi Python asinkron untuk mendukung pemanggilan alat paralel. Ketika Claude menulis kode yang memanggil alat Anda, ia menggunakan `await` (misalnya, `result = await query_database("<sql>")`) dan secara otomatis menyertakan fungsi pembungkus asinkron yang sesuai.

Pembungkus asinkron dihilangkan dari contoh kode dalam dokumentasi ini untuk kejelasan.
</Note>

## Konsep inti

### Bidang `allowed_callers`

Bidang `allowed_callers` menentukan konteks mana yang dapat memanggil alat:

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
Pilih `["direct"]` atau `["code_execution_20260120"]` untuk setiap alat daripada mengaktifkan keduanya, karena ini memberikan panduan yang lebih jelas kepada Claude tentang cara terbaik menggunakan alat.
</Tip>

### Bidang `caller` dalam respons

Setiap blok penggunaan alat mencakup bidang `caller` yang menunjukkan cara ia dipanggil:

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

**Pemanggilan terprogram:**
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

`tool_id` mereferensikan alat eksekusi kode yang membuat pemanggilan terprogram.

### Siklus hidup kontainer

Pemanggilan alat secara terprogram menggunakan kontainer yang sama dengan eksekusi kode:

- **Pembuatan kontainer:** Kontainer baru dibuat untuk setiap sesi kecuali Anda menggunakan kembali yang sudah ada
- **Kedaluwarsa:** Kontainer memiliki masa hidup maksimal 30 hari dan dibersihkan setelah 4,5 menit waktu henti
- **ID kontainer:** Dikembalikan dalam respons melalui bidang `container`
- **Penggunaan kembali:** Teruskan ID kontainer untuk mempertahankan status di seluruh permintaan

<Warning>
Ketika alat dipanggil secara terprogram dan kontainer menunggu hasil alat Anda, Anda harus merespons sebelum kontainer kedaluwarsa. Pantau bidang `expires_at`. Jika kontainer kedaluwarsa, Claude dapat memperlakukan pemanggilan alat sebagai waktu habis dan mencoba lagi.
</Warning>

## Alur kerja contoh

Berikut adalah cara alur pemanggilan alat secara terprogram yang lengkap bekerja:

### Langkah 1: Permintaan awal

Kirim permintaan dengan eksekusi kode dan alat yang memungkinkan pemanggilan terprogram. Untuk mengaktifkan pemanggilan terprogram, tambahkan bidang `allowed_callers` ke definisi alat Anda.

<Note>
Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude mencoba untuk mendeserialisasi dan memproses hasilnya dalam kode. Semakin detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara terprogram.
</Note>

Bentuk permintaan identik dengan contoh [Mulai cepat](#mulai-cepat): sertakan `code_execution` dalam daftar alat Anda, tambahkan `allowed_callers: ["code_execution_20260120"]` ke alat apa pun yang ingin Anda panggil Claude dari kode, dan kirim pesan pengguna Anda.

### Langkah 2: Respons API dengan pemanggilan alat

Claude menulis kode yang memanggil alat Anda. API berhenti dan mengembalikan:

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

### Langkah 3: Berikan hasil alat

Sertakan riwayat percakapan lengkap ditambah hasil alat Anda:

<CodeGroup>

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model(Model.CLAUDE_OPUS_4_7)
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
    model: 'claude-opus-4-7',
    container: 'container_xyz789',
    tools: [],
);

echo $message;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
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

### Langkah 4: Panggilan alat berikutnya atau penyelesaian

Eksekusi kode berlanjut dan memproses hasilnya. Jika panggilan alat tambahan diperlukan, ulangi Langkah 3 sampai semua panggilan alat terpenuhi.

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
- Mengurangi putaran model dari N (satu per wilayah) menjadi 1
- Memproses set hasil besar secara terprogram sebelum kembali ke Claude
- Menghemat token dengan hanya mengembalikan kesimpulan yang diagregasi alih-alih data mentah

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

### Pemilihan alat bersyarat

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

### Penyaringan data

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

### Panggilan alat terprogram

Ketika eksekusi kode memanggil alat:

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

### Penanganan hasil alat

Hasil alat Anda dilewatkan kembali ke kode yang sedang berjalan:

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

Ketika semua panggilan alat terpenuhi dan kode selesai:

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

## Penanganan kesalahan

### Kesalahan umum

| Kesalahan | Deskripsi | Solusi |
|-------|-------------|----------|
| `invalid_tool_input` | Input alat tidak sesuai dengan skema | Validasi input_schema alat Anda |
| `tool_not_allowed` | Alat tidak mengizinkan tipe pemanggil yang diminta | Periksa `allowed_callers` mencakup konteks yang tepat |
| `missing_beta_header` | Header beta yang diperlukan tidak disediakan (Bedrock dan Vertex AI saja; pemanggilan alat terprogram adalah GA di API Claude pihak pertama) | Tambahkan header beta yang diperlukan ke permintaan Anda |

### Kedaluwarsa kontainer selama panggilan alat

Jika alat Anda membutuhkan waktu terlalu lama untuk merespons, eksekusi kode menerima `TimeoutError`. Claude melihat ini di stderr dan biasanya mencoba lagi:

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

Untuk mencegah waktu habis:
- Pantau bidang `expires_at` dalam respons
- Implementasikan waktu habis untuk eksekusi alat Anda
- Pertimbangkan untuk memecah operasi panjang menjadi potongan yang lebih kecil

### Kesalahan eksekusi alat

Jika alat Anda mengembalikan kesalahan:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_abc123",
  "content": "Error: Query timeout - table lock exceeded 30 seconds"
}
```

Kode Claude menerima kesalahan ini dan dapat menanganinya dengan tepat.

## Batasan dan keterbatasan

### Ketidakcocokan fitur

- **Output terstruktur:** Alat dengan `strict: true` tidak didukung dengan pemanggilan terprogram
- **Pilihan alat:** Anda tidak dapat memaksa pemanggilan terprogram dari alat tertentu melalui `tool_choice`
- **Penggunaan alat paralel:** `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Pembatasan alat

Alat berikut saat ini tidak dapat dipanggil secara terprogram, tetapi dukungan dapat ditambahkan di rilis mendatang:

- Alat yang disediakan oleh [konektor MCP](/docs/id/agents-and-tools/mcp-connector)

### Pembatasan pemformatan pesan

Saat merespons panggilan alat terprogram, ada persyaratan pemformatan yang ketat:

**Respons hanya hasil alat:** Jika ada panggilan alat terprogram yang tertunda menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil alat.

Tidak valid - Tidak dapat menyertakan teks saat merespons panggilan alat terprogram:

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

Valid - Hanya hasil alat saat merespons panggilan alat terprogram:

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

Pembatasan ini hanya berlaku saat merespons panggilan alat terprogram (eksekusi kode). Untuk panggilan alat sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil alat.

### Batas laju

Panggilan alat terprogram tunduk pada batas laju yang sama dengan panggilan alat biasa. Setiap panggilan alat dari eksekusi kode dihitung sebagai invokasi terpisah.

### Validasi hasil alat sebelum digunakan

Saat mengimplementasikan alat yang ditentukan pengguna yang akan dipanggil secara terprogram:

- **Hasil alat dikembalikan sebagai string:** Mereka dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang dapat diproses oleh lingkungan eksekusi.
- **Validasi hasil alat eksternal:** Jika alat Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan ditafsirkan atau dieksekusi sebagai kode.

## Efisiensi token

Pemanggilan alat terprogram dapat secara signifikan mengurangi konsumsi token:

- **Hasil alat dari panggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir
- **Pemrosesan perantara terjadi dalam kode** - penyaringan, agregasi, dll. tidak menggunakan token model
- **Beberapa panggilan alat dalam satu eksekusi kode** - mengurangi overhead dibandingkan dengan putaran model terpisah

Misalnya, memanggil 10 alat secara langsung menggunakan ~10x token dari memanggilan mereka secara terprogram dan mengembalikan ringkasan.

## Penggunaan dan harga

Pemanggilan alat terprogram menggunakan harga yang sama dengan eksekusi kode. Lihat [harga eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detail.

<Note>
Penghitungan token untuk panggilan alat terprogram: Hasil alat dari invokasi terprogram tidak dihitung terhadap penggunaan token input/output Anda. Hanya hasil eksekusi kode akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik

### Desain alat

- **Berikan deskripsi output yang terperinci:** Karena Claude mendeserialisasi hasil alat dalam kode, dokumentasikan dengan jelas formatnya (struktur JSON, tipe bidang, dll.)
- **Kembalikan data terstruktur:** Format JSON atau format yang mudah diurai lainnya paling baik untuk pemrosesan terprogram
- **Jaga respons tetap ringkas:** Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram

**Kasus penggunaan yang baik:**
- Memproses kumpulan data besar di mana Anda hanya memerlukan agregat atau ringkasan
- Alur kerja multi-langkah dengan 3+ panggilan alat yang bergantung
- Operasi yang memerlukan penyaringan, pengurutan, atau transformasi hasil alat
- Tugas di mana data perantara tidak boleh mempengaruhi penalaran Claude
- Operasi paralel di banyak item (misalnya, memeriksa 50 titik akhir)

**Kasus penggunaan yang kurang ideal:**
- Panggilan alat tunggal dengan respons sederhana
- Alat yang memerlukan umpan balik pengguna segera
- Operasi yang sangat cepat di mana overhead eksekusi kode akan mengungguli manfaatnya

### Optimasi kinerja

- **Gunakan kembali kontainer** saat membuat beberapa permintaan terkait untuk mempertahankan status
- **Operasi serupa batch** dalam satu eksekusi kode jika memungkinkan

## Pemecahan masalah

### Masalah umum

**Kesalahan "Tool not allowed"**
- Verifikasi definisi alat Anda mencakup `"allowed_callers": ["code_execution_20260120"]`

**Kedaluwarsa kontainer**
- Pastikan Anda merespons panggilan alat sebelum kontainer idle habis (4,5 menit tidak aktif; maksimum keras 30 hari)
- Pantau bidang `expires_at` dalam respons
- Pertimbangkan untuk mengimplementasikan eksekusi alat yang lebih cepat

**Hasil alat tidak diurai dengan benar**
- Pastikan alat Anda mengembalikan data string yang dapat dideserialkan Claude
- Berikan dokumentasi format output yang jelas dalam deskripsi alat Anda

### Tips debugging

1. **Catat semua panggilan alat dan hasil** untuk melacak alur
2. **Periksa bidang `caller`** untuk mengkonfirmasi invokasi terprogram
3. **Pantau ID kontainer** untuk memastikan penggunaan kembali yang tepat
4. **Uji alat secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan alat terprogram berfungsi

Pelatihan Claude mencakup paparan luas terhadap kode, menjadikannya efektif dalam penalaran melalui dan pemanggilan fungsi rantai. Ketika alat disajikan sebagai fungsi yang dapat dipanggil dalam lingkungan eksekusi kode, Claude dapat memanfaatkan kekuatan ini untuk:

- **Alasan secara alami tentang komposisi alat:** Operasi rantai dan menangani dependensi senatural menulis kode Python apa pun
- **Proses hasil besar secara efisien:** Saring hasil alat besar, ekstrak hanya data yang relevan, atau tulis hasil perantara ke file sebelum mengembalikan ringkasan ke jendela konteks
- **Kurangi latensi secara signifikan:** Hilangkan overhead pengambilan sampel ulang Claude antara setiap panggilan alat dalam alur kerja multi-langkah

Pendekatan ini memungkinkan alur kerja yang tidak praktis dengan penggunaan alat tradisional (seperti memproses file lebih dari 1M token) dengan memungkinkan Claude bekerja dengan data secara terprogram daripada memuat semuanya ke dalam konteks percakapan.

## Implementasi alternatif

Pemanggilan alat terprogram adalah pola yang dapat digeneralisasi yang dapat diimplementasikan di luar eksekusi kode terkelola Anthropic. Berikut adalah gambaran umum pendekatan:

### Eksekusi langsung sisi klien

Berikan Claude dengan alat eksekusi kode dan jelaskan fungsi apa yang tersedia di lingkungan itu. Ketika Claude memanggil alat dengan kode, aplikasi Anda menjalankannya secara lokal di mana fungsi-fungsi itu didefinisikan.

**Keuntungan:**
- Sederhana untuk diimplementasikan dengan re-architecting minimal
- Kontrol penuh atas lingkungan dan instruksi

**Kerugian:**
- Menjalankan kode yang tidak terpercaya di luar sandbox
- Invokasi alat dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat dengan aman menjalankan kode arbitrer, Anda menginginkan solusi sederhana, dan penawaran terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi sandbox yang dikelola sendiri

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan dalam kontainer sandbox dengan pembatasan keamanan (misalnya, tidak ada egress jaringan). Jika alat Anda memerlukan sumber daya eksternal, Anda akan memerlukan protokol untuk menjalankan panggilan alat di luar sandbox.

**Keuntungan:**
- Pemanggilan alat terprogram yang aman di infrastruktur Anda sendiri
- Kontrol penuh atas lingkungan eksekusi

**Kerugian:**
- Kompleks untuk dibangun dan dipertahankan
- Memerlukan pengelolaan infrastruktur dan komunikasi antar proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai dengan persyaratan Anda.

### Eksekusi terkelola Anthropic

Pemanggilan alat terprogram Anthropic adalah versi terkelola dari eksekusi sandbox dengan lingkungan Python yang berpendapat disesuaikan untuk Claude. Anthropic menangani manajemen kontainer, eksekusi kode, dan komunikasi invokasi alat yang aman.

**Keuntungan:**
- Aman dan aman secara default
- Mudah diaktifkan dengan konfigurasi minimal
- Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API.

## Retensi data

Pemanggilan alat terprogram dibangun di atas infrastruktur eksekusi kode dan menggunakan kontainer sandbox yang sama. Data kontainer, termasuk artefak eksekusi dan output, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/build-with-claude/api-and-data-retention).

## Fitur terkait

<CardGroup cols={2}>
  <Card title="Code Execution Tool" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Pelajari tentang kemampuan eksekusi kode yang mendasari yang mendukung pemanggilan alat terprogram.
  </Card>
  <Card title="Tool Use Overview" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Pahami dasar-dasar penggunaan alat dengan Claude.
  </Card>
  <Card title="Define tools" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Panduan langkah demi langkah untuk mendefinisikan alat.
  </Card>
</CardGroup>