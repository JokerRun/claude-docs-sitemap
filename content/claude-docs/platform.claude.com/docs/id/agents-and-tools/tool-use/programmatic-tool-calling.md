---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 85acbdc19e1af8b07e3dd7f1135f1e239320f1af074056b870714dfd5ad9ec7a
---

# Pemanggilan alat secara terprogram

---

Pemanggilan alat secara terprogram memungkinkan Claude menulis kode yang memanggil alat Anda secara terprogram di dalam kontainer [code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool), alih-alih memerlukan perjalanan bolak-balik melalui model untuk setiap pemanggilan alat. Hal ini mengurangi "latency" (latensi) untuk alur kerja multi-alat dan menurunkan konsumsi token dengan memungkinkan Claude memfilter atau memproses data sebelum data tersebut mencapai "context window" (jendela konteks) model. Pada tolok ukur pencarian agentik seperti [BrowseComp](https://arxiv.org/abs/2504.12516) dan [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), yang menguji riset web multi-langkah dan pengambilan informasi kompleks, menambahkan pemanggilan alat secara terprogram di atas alat pencarian dasar meningkatkan kinerja rata-rata sebesar 11% sambil menggunakan 24% lebih sedikit token input (lihat [Improved web search with dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)).

Perbedaannya bertambah cepat dalam alur kerja nyata. Pertimbangkan pemeriksaan kepatuhan anggaran di 20 karyawan: pendekatan tradisional memerlukan 20 perjalanan bolak-balik model yang terpisah, menarik ribuan item baris pengeluaran ke dalam konteks di sepanjang prosesnya. Dengan pemanggilan alat secara terprogram, satu skrip menjalankan semua 20 pencarian, memfilter hasilnya, dan hanya mengembalikan karyawan yang melebihi batas mereka, menyusutkan apa yang perlu dipikirkan Claude dari ratusan kilobyte menjadi hanya beberapa baris.

<Tip>
Untuk pembahasan lebih mendalam tentang biaya inferensi dan konteks yang diatasi oleh pemanggilan alat secara terprogram, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

<Note>
Fitur ini memerlukan alat code execution untuk diaktifkan.
</Note>

<Note>
Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Kompatibilitas model \{#model-compatibility}

Pemanggilan alat secara terprogram memerlukan `code_execution_20260120`, yang didukung pada model-model berikut:

| Model |
|-------|
| Claude Fable 5 (claude-fable-5) |
| Claude Mythos 5 (claude-mythos-5) |
| Claude Opus 4.8 (claude-opus-4-8) |
| Claude Opus 4.7 (claude-opus-4-7) |
| Claude Opus 4.6 (claude-opus-4-6) |
| Claude Sonnet 4.6 (claude-sonnet-4-6) |
| Claude Opus 4.5 (claude-opus-4-5-20251101) |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) |

Untuk matriks versi alat code execution lengkap, lihat [tabel kompatibilitas model alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility). Pemanggilan alat secara terprogram tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Saat ini fitur ini tidak tersedia di Amazon Bedrock atau Vertex AI.

## Mulai cepat \{#quick-start}

Berikut adalah contoh di mana Claude secara terprogram melakukan kueri ke database beberapa kali dan mengagregasi hasilnya:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
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

```typescript TypeScript hidelines={1..5,-3..-1}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.messages.create({
    model: "claude-opus-4-8",
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

```csharp C# hidelines={1..13,-2..}
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
            Model = Model.ClaudeOpus4_8,
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
		Model:     anthropic.ModelClaudeOpus4_8,
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
            .model("claude-opus-4-8")
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

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue'],
    ],
    model: 'claude-opus-4-8',
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

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
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

## Cara kerja pemanggilan alat secara terprogram \{#how-programmatic-tool-calling-works}

Ketika Anda mengonfigurasi sebuah alat agar dapat dipanggil dari code execution dan Claude memutuskan untuk menggunakan alat tersebut:

1. Claude menulis kode Python yang memanggil alat sebagai fungsi, yang berpotensi mencakup beberapa pemanggilan alat dan logika pra/pasca-pemrosesan
2. Claude menjalankan kode ini dalam kontainer sandbox melalui code execution
3. Ketika fungsi alat dipanggil, code execution dijeda dan API mengembalikan blok `tool_use`
4. Anda menyediakan hasil alat, dan code execution dilanjutkan (hasil antara tidak dimuat ke dalam jendela konteks Claude)
5. Setelah semua code execution selesai, Claude menerima output akhir dan melanjutkan pengerjaan tugas

Pendekatan ini sangat berguna untuk:
- **Pemrosesan data besar:** Memfilter atau mengagregasi hasil alat sebelum mencapai konteks Claude
- **Alur kerja multi-langkah:** Menghemat token dan latensi dengan memanggil alat secara serial atau dalam loop tanpa melakukan sampling Claude di antara pemanggilan alat
- **Logika kondisional:** Membuat keputusan berdasarkan hasil alat antara

<Note>
Alat kustom dikonversi menjadi fungsi Python async untuk mendukung pemanggilan alat paralel. Ketika Claude menulis kode yang memanggil alat Anda, Claude menggunakan `await` (misalnya, `result = await query_database("<sql>")`) dan secara otomatis menyertakan fungsi pembungkus async yang sesuai.

Pembungkus async dihilangkan dari contoh kode dalam dokumentasi ini untuk kejelasan.
</Note>

## Konsep inti \{#core-concepts}

### Field `allowed_callers` \{#the-allowed-callers-field}

Field `allowed_callers` menentukan konteks mana yang dapat memanggil sebuah alat:

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
- `["direct"]` - Claude diarahkan untuk memanggil alat ini secara langsung (default jika dihilangkan)
- `["code_execution_20260120"]` - Claude diarahkan untuk memanggil alat ini hanya dari dalam code execution
- `["direct", "code_execution_20260120"]` - Claude dapat memanggil alat ini secara langsung atau dari dalam code execution

<Tip>
Pilih salah satu antara `["direct"]` atau `["code_execution_20260120"]` untuk setiap alat daripada mengaktifkan keduanya, karena ini memberikan panduan yang lebih jelas kepada Claude tentang cara terbaik menggunakan alat tersebut.
</Tip>

<Note>
`allowed_callers` mengontrol bagaimana alat disajikan kepada Claude dan divalidasi terhadap `tool_choice`, tetapi ini bukan pemblokiran keras di tingkat API terhadap pemanggilan langsung. Claude diarahkan dengan kuat untuk menghormatinya, tetapi klien Anda tetap harus siap menangani `tool_use` langsung untuk alat apa pun yang didefinisikannya. Jangan mengandalkan `allowed_callers` sebagai batas keamanan.
</Note>

### Field `caller` dalam respons \{#the-caller-field-in-responses}

Setiap blok tool use menyertakan field `caller` yang menunjukkan bagaimana alat tersebut dipanggil:

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

`tool_id` merujuk ke alat code execution yang melakukan pemanggilan terprogram.

### Siklus hidup kontainer \{#container-lifecycle}

Pemanggilan alat secara terprogram menggunakan kontainer yang sama dengan code execution:

- **Pembuatan kontainer:** Kontainer baru dibuat untuk setiap permintaan kecuali Anda menggunakan kembali kontainer yang sudah ada
- **Kedaluwarsa:** Kontainer memiliki masa hidup maksimum 30 hari dan dibersihkan setelah 4,5 menit waktu idle
- **ID Kontainer:** Dikembalikan dalam respons di field `container`
- **Penggunaan kembali:** Teruskan ID kontainer untuk mempertahankan state di seluruh permintaan

<Warning>
Ketika sebuah alat dipanggil secara terprogram dan kontainer sedang menunggu hasil alat Anda, Anda harus merespons sebelum kontainer kedaluwarsa. Pantau field `expires_at`. Jika kontainer kedaluwarsa, Claude mungkin memperlakukan pemanggilan alat sebagai timeout dan mencobanya kembali.
</Warning>

## Contoh alur kerja \{#example-workflow}

Berikut cara kerja alur pemanggilan alat secara terprogram yang lengkap:

### Langkah 1: Permintaan awal \{#step-1-initial-request}

Kirim permintaan dengan code execution dan alat yang mengizinkan pemanggilan terprogram. Untuk mengaktifkan pemanggilan terprogram, tambahkan field `allowed_callers` ke definisi alat Anda.

<Note>
Berikan deskripsi terperinci tentang format output alat Anda dalam deskripsi alat. Jika Anda menentukan bahwa alat mengembalikan JSON, Claude akan mencoba melakukan deserialisasi dan memproses hasilnya dalam kode. Semakin banyak detail yang Anda berikan tentang skema output, semakin baik Claude dapat menangani respons secara terprogram.
</Note>

Bentuk permintaan identik dengan contoh [Mulai cepat](#quick-start): sertakan `code_execution` dalam daftar alat Anda, tambahkan `allowed_callers: ["code_execution_20260120"]` ke alat apa pun yang Anda ingin Claude panggil dari kode, dan kirim pesan pengguna Anda. Langkah-langkah selanjutnya dalam alur kerja ini menggunakan pesan pengguna `"Query customer purchase history from the last quarter and identify our top 5 customers by revenue"`.

### Langkah 2: Respons API dengan pemanggilan alat \{#step-2-api-response-with-tool-call}

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
    "expires_at": "2026-01-20T14:30:00Z"
  },
  "stop_reason": "tool_use"
}
```

### Langkah 3: Sediakan hasil alat \{#step-3-provide-tool-result}

Sertakan riwayat percakapan lengkap ditambah hasil alat Anda:

<CodeGroup>

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
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
            Model = Model.ClaudeOpus4_8,
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
		Model:     anthropic.ModelClaudeOpus4_8,
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
            .model(Model.CLAUDE_OPUS_4_8)
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

$client = new Client();

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
    model: 'claude-opus-4-8',
    container: 'container_xyz789',
    tools: [],
);

echo $message;
```

```ruby Ruby nocheck
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
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

### Langkah 4: Pemanggilan alat berikutnya atau penyelesaian \{#step-4-next-tool-call-or-completion}

Code execution dilanjutkan dan memproses hasilnya. Jika pemanggilan alat tambahan diperlukan, ulangi Langkah 3 hingga semua pemanggilan alat terpenuhi.

### Langkah 5: Respons akhir \{#step-5-final-response}

Setelah code execution selesai, Claude memberikan respons akhir:

```json Output
{
  "content": [
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_abc123",
      "content": {
        "type": "code_execution_result",
        "stdout": "Top 5 customers: [{'customer_id': 'C1', 'revenue': 45000}, {'customer_id': 'C2', 'revenue': 38000}, {'customer_id': 'C5', 'revenue': 32000}, {'customer_id': 'C8', 'revenue': 28500}, {'customer_id': 'C3', 'revenue': 24000}]",
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

## Pola lanjutan \{#advanced-patterns}

### Pemrosesan batch dengan loop \{#batch-processing-with-loops}

Claude dapat menulis kode yang memproses banyak item secara efisien:

```python hidelines={1..4,-1}
async def query_database(sql):
    return [{"revenue": 100}]


async def _claude_code():
    regions = ["West", "East", "Central", "North", "South"]
    results = {}
    for region in regions:
        data = await query_database(f"<sql for {region}>")
        results[region] = sum(row["revenue"] for row in data)

    # Proses hasil secara terprogram
    top_region = max(results.items(), key=lambda x: x[1])
    print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")


_ = _claude_code
```

Pola ini:
- Mengurangi perjalanan bolak-balik model dari N (satu per wilayah) menjadi 1
- Memproses kumpulan hasil yang besar secara terprogram sebelum dikembalikan ke Claude
- Menghemat token dengan hanya mengembalikan kesimpulan yang diagregasi alih-alih data mentah

### Penghentian dini \{#early-termination}

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

### Pemilihan alat kondisional \{#conditional-tool-selection}

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

### Pemfilteran data \{#data-filtering}

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

## Format respons \{#response-format}

### Pemanggilan alat terprogram \{#programmatic-tool-call}

Ketika code execution memanggil sebuah alat:

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

### Penanganan hasil alat \{#tool-result-handling}

Hasil alat Anda diteruskan kembali ke kode yang sedang berjalan:

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

### Penyelesaian code execution \{#code-execution-completion}

Ketika semua pemanggilan alat terpenuhi dan kode selesai:

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

## Penanganan error \{#error-handling}

### Error umum \{#common-errors}

| Error | Deskripsi | Solusi |
|-------|-------------|----------|
| `invalid_tool_input` | Input alat tidak cocok dengan skema | Validasi input_schema alat Anda |
| `invalid_request_error` (pada `tool_choice`) | `tool_choice` menyebutkan alat yang `allowed_callers`-nya tidak menyertakan `"direct"` | Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode |

### Kedaluwarsa kontainer selama pemanggilan alat \{#container-expiration-during-tool-call}

Jika alat Anda membutuhkan waktu terlalu lama untuk merespons, code execution menerima `TimeoutError`. Claude melihat ini di stderr dan biasanya mencoba lagi:

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
- Terapkan timeout untuk eksekusi alat Anda
- Pertimbangkan untuk memecah operasi panjang menjadi bagian-bagian yang lebih kecil

### Error eksekusi alat \{#tool-execution-errors}

Jika alat Anda mengembalikan error:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_abc123",
  "content": "Error: Query timeout - table lock exceeded 30 seconds"
}
```

Kode Claude menerima error ini dan dapat menanganinya dengan tepat.

## Batasan dan keterbatasan \{#constraints-and-limitations}

### Inkompatibilitas fitur \{#feature-incompatibilities}

- **Output terstruktur:** Alat dengan `strict: true` tidak didukung dengan pemanggilan terprogram
- **Tool choice:** Anda tidak dapat memaksa pemanggilan terprogram dari alat tertentu melalui `tool_choice`
- **Penggunaan alat paralel:** `disable_parallel_tool_use: true` tidak didukung dengan pemanggilan terprogram

### Pembatasan alat \{#tool-restrictions}

Alat-alat berikut tidak dapat dipanggil secara terprogram:

- Alat yang disediakan oleh [MCP connector](/docs/id/agents-and-tools/mcp-connector)

### Pembatasan pemformatan pesan \{#message-formatting-restrictions}

Saat merespons pemanggilan alat terprogram, terdapat persyaratan pemformatan yang ketat:

**Respons hanya hasil alat:** Jika ada pemanggilan alat terprogram yang tertunda menunggu hasil, pesan respons Anda harus berisi **hanya** blok `tool_result`. Anda tidak dapat menyertakan konten teks apa pun, bahkan setelah hasil alat.

Tidak valid - Tidak dapat menyertakan teks saat merespons pemanggilan alat terprogram:

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

Valid - Hanya hasil alat saat merespons pemanggilan alat terprogram:

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

Pembatasan ini hanya berlaku saat merespons pemanggilan alat terprogram (code execution). Untuk pemanggilan alat sisi klien biasa, Anda dapat menyertakan konten teks setelah hasil alat.

### Batas laju \{#rate-limits}

Pemanggilan alat terprogram tunduk pada batas laju yang sama dengan pemanggilan alat biasa. Setiap pemanggilan alat dari code execution dihitung sebagai pemanggilan terpisah.

### Validasi hasil alat sebelum digunakan \{#validate-tool-results-before-use}

Saat mengimplementasikan alat yang didefinisikan pengguna yang akan dipanggil secara terprogram:

- **Hasil alat dikembalikan sebagai string:** Hasil tersebut dapat berisi konten apa pun, termasuk cuplikan kode atau perintah yang dapat dieksekusi yang mungkin diproses oleh lingkungan eksekusi.
- **Validasi hasil alat eksternal:** Jika alat Anda mengembalikan data dari sumber eksternal atau menerima input pengguna, waspadai risiko injeksi kode jika output akan diinterpretasikan atau dieksekusi sebagai kode.

## Efisiensi token \{#token-efficiency}

Pemanggilan alat secara terprogram dapat secara signifikan mengurangi konsumsi token:

- **Hasil alat dari pemanggilan terprogram tidak ditambahkan ke konteks Claude** - hanya output kode akhir yang ditambahkan
- **Pemrosesan antara terjadi dalam kode** - pemfilteran, agregasi, dan transformasi lainnya tidak mengonsumsi token model
- **Beberapa pemanggilan alat dalam satu code execution** - mengurangi overhead dibandingkan dengan giliran model yang terpisah

Misalnya, memanggil 10 alat secara langsung menggunakan ~10x token dibandingkan memanggilnya secara terprogram dan mengembalikan ringkasan.

Dalam evaluasi internal Anthropic pada model Claude produksi:

- Pada tolok ukur agen manajemen proyek dengan 75 alat, mengaktifkan pemanggilan alat secara terprogram mengurangi token input yang ditagih sekitar 38% tanpa perubahan pada akurasi tugas.
- Pada [τ²-bench](https://arxiv.org/abs/2506.07982) (domain maskapai penerbangan, ritel, dan telekomunikasi), di mana setiap giliran membuat satu atau dua pemanggilan alat berurutan, pemanggilan alat secara terprogram tidak mengubah skor dan biayanya sekitar 8% lebih tinggi. Alur kerja pemanggilan tunggal berurutan tidak mendapat manfaat.
- Di seluruh lalu lintas API produksi, permintaan yang array `tools`-nya berisi 10 hingga 49 definisi alat mengalami penghematan token tipikal sebesar 20% hingga 40% dengan pemanggilan alat secara terprogram diaktifkan.

Penghematan aktual bervariasi tergantung bentuk beban kerja; lihat [Kapan menggunakan pemanggilan terprogram](#when-to-use-programmatic-calling).

## Penggunaan dan harga \{#usage-and-pricing}

Pemanggilan alat secara terprogram menggunakan harga yang sama dengan code execution. Lihat [harga code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detailnya.

<Note>
Penghitungan token untuk pemanggilan alat terprogram: Hasil alat dari pemanggilan terprogram tidak dihitung terhadap penggunaan token input/output Anda. Hanya hasil code execution akhir dan respons Claude yang dihitung.
</Note>

## Praktik terbaik \{#best-practices}

### Desain alat \{#tool-design}

- **Berikan deskripsi output yang terperinci:** Karena Claude melakukan deserialisasi hasil alat dalam kode, dokumentasikan formatnya dengan jelas (struktur JSON dan tipe field)
- **Kembalikan data terstruktur:** JSON atau format lain yang mudah di-parse bekerja paling baik untuk pemrosesan terprogram
- **Jaga respons tetap ringkas:** Kembalikan hanya data yang diperlukan untuk meminimalkan overhead pemrosesan

### Kapan menggunakan pemanggilan terprogram \{#when-to-use-programmatic-calling}

Pemanggilan alat secara terprogram menukar overhead tetap yang kecil (startup kontainer, pembuatan skrip) dengan penghematan besar pada token hasil alat dan perjalanan bolak-balik model. Apakah pertukaran itu menguntungkan tergantung pada bentuk beban kerja.

**Sangat cocok:**
- Operasi fan-out atau paralel di banyak item (misalnya, memeriksa 50 endpoint atau mencari 20 record)
- Hasil alat yang besar yang dapat difilter, diagregasi, atau diringkas sebelum mencapai konteks Claude
- Pencarian dan pengambilan agentik, di mana kueri iteratif dan pemfilteran hasil mendominasi alur kerja

**Kurang cocok:**
- Alur kerja yang sangat berurutan di mana setiap pemanggilan bergantung pada penalaran Claude atas hasil sebelumnya, karena skrip tidak dapat melewati perjalanan bolak-balik model dalam kasus tersebut
- Sejumlah kecil pemanggilan alat dengan respons kecil, terutama pada giliran pertama percakapan, di mana overhead kontainer dan skrip dapat melebihi penghematannya
- Alat yang memerlukan umpan balik pengguna segera di antara pemanggilan

Jika Anda tidak yakin, ukur token input yang ditagih dengan dan tanpa `allowed_callers` pada sampel representatif dari lalu lintas Anda sebelum mengaktifkannya secara luas.

### Optimasi kinerja \{#performance-optimization}

- **Gunakan kembali kontainer** saat membuat beberapa permintaan terkait untuk mempertahankan state
- **Kelompokkan operasi serupa** dalam satu code execution jika memungkinkan

## Pemecahan masalah \{#troubleshooting}

### Masalah umum \{#common-issues}

**`invalid_request_error` saat mengatur `tool_choice`**
- `tool_choice` tidak dapat menyebutkan alat yang `allowed_callers`-nya tidak menyertakan `"direct"`. Tambahkan `"direct"` ke `allowed_callers` alat tersebut, atau hapus alat dari `tool_choice` dan biarkan Claude memanggilnya dari kode.

**Kedaluwarsa kontainer**
- Pastikan Anda merespons pemanggilan alat sebelum kontainer menjadi idle (4,5 menit tidak aktif; maksimum keras 30 hari)
- Pantau field `expires_at` dalam respons
- Pertimbangkan untuk mengimplementasikan eksekusi alat yang lebih cepat

**Hasil alat tidak di-parse dengan benar**
- Pastikan alat Anda mengembalikan data string yang dapat dideserialisasi oleh Claude
- Berikan dokumentasi format output yang jelas dalam deskripsi alat Anda

### Tips debugging \{#debugging-tips}

1. **Catat semua pemanggilan alat dan hasilnya** untuk melacak alurnya
2. **Periksa field `caller`** untuk mengonfirmasi pemanggilan terprogram
3. **Pantau ID kontainer** untuk memastikan penggunaan kembali yang tepat
4. **Uji alat secara independen** sebelum mengaktifkan pemanggilan terprogram

## Mengapa pemanggilan alat secara terprogram berhasil \{#why-programmatic-tool-calling-works}

Pelatihan Claude mencakup paparan ekstensif terhadap kode, menjadikannya efektif dalam bernalar dan merangkai pemanggilan fungsi. Ketika alat disajikan sebagai fungsi yang dapat dipanggil dalam lingkungan code execution, Claude dapat memanfaatkan kekuatan ini untuk:

- **Bernalar secara alami tentang komposisi alat:** Merangkai operasi dan menangani dependensi sealami menulis kode Python apa pun
- **Memproses hasil besar secara efisien:** Memfilter output alat yang besar, mengekstrak hanya data yang relevan, atau menulis hasil antara ke file sebelum mengembalikan ringkasan ke jendela konteks
- **Mengurangi latensi secara signifikan:** Menghilangkan overhead sampling ulang Claude di antara setiap pemanggilan alat dalam alur kerja multi-langkah

Pendekatan ini memungkinkan alur kerja yang tidak praktis dengan penggunaan alat tradisional (seperti memproses file lebih dari 1 juta token) dengan memungkinkan Claude bekerja dengan data secara terprogram alih-alih memuat semuanya ke dalam konteks percakapan.

## Implementasi alternatif \{#alternative-implementations}

Pemanggilan alat secara terprogram adalah pola yang dapat digeneralisasi yang juga dapat diimplementasikan pada infrastruktur Anda sendiri. Berikut perbandingan pendekatannya:

### Eksekusi langsung sisi klien \{#client-side-direct-execution}

Sediakan Claude dengan alat code execution dan jelaskan fungsi apa yang tersedia di lingkungan tersebut. Ketika Claude memanggil alat dengan kode, aplikasi Anda mengeksekusinya secara lokal di mana fungsi-fungsi tersebut didefinisikan.

**Kelebihan:**
- Sederhana untuk diimplementasikan dengan re-arsitektur minimal
- Kontrol penuh atas lingkungan dan instruksi

**Kekurangan:**
- Mengeksekusi kode yang tidak tepercaya di luar sandbox
- Pemanggilan alat dapat menjadi vektor untuk injeksi kode

**Gunakan ketika:** Aplikasi Anda dapat dengan aman mengeksekusi kode arbitrer, Anda menginginkan solusi sederhana, dan penawaran terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi sandbox yang dikelola sendiri \{#self-managed-sandboxed-execution}

Pendekatan yang sama dari perspektif Claude, tetapi kode berjalan dalam kontainer sandbox dengan pembatasan keamanan (misalnya, tanpa egress jaringan). Jika alat Anda memerlukan sumber daya eksternal, Anda akan memerlukan protokol untuk mengeksekusi pemanggilan alat di luar sandbox.

**Kelebihan:**
- Pemanggilan alat terprogram yang aman pada infrastruktur Anda sendiri
- Kontrol penuh atas lingkungan eksekusi

**Kekurangan:**
- Kompleks untuk dibangun dan dipelihara
- Memerlukan pengelolaan infrastruktur dan komunikasi antar-proses

**Gunakan ketika:** Keamanan sangat penting dan solusi terkelola Anthropic tidak sesuai dengan kebutuhan Anda.

### Eksekusi yang dikelola Anthropic \{#anthropic-managed-execution}

Pemanggilan alat secara terprogram dari Anthropic adalah versi terkelola dari eksekusi sandbox dengan lingkungan Python yang telah dikonfigurasi dan disetel untuk Claude. Anthropic menangani manajemen kontainer, eksekusi kode, dan komunikasi pemanggilan alat yang aman.

**Kelebihan:**
- Aman dan terlindungi secara default
- Mudah diaktifkan dengan konfigurasi minimal
- Lingkungan dan instruksi dioptimalkan untuk Claude

Pertimbangkan untuk menggunakan solusi terkelola Anthropic jika Anda menggunakan Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), atau [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Retensi data \{#data-retention}

Pemanggilan alat secara terprogram dibangun di atas infrastruktur code execution dan menggunakan kontainer sandbox yang sama. Data kontainer, termasuk artefak eksekusi dan output, disimpan hingga 30 hari.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Fitur terkait \{#related-features}

<CardGroup cols={2}>
  <Card title="Alat code execution" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Pelajari tentang kemampuan code execution yang mendasari yang mendukung pemanggilan alat secara terprogram.
  </Card>
  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="/docs/id/agents-and-tools/tool-use/overview">
    Pahami dasar-dasar penggunaan alat dengan Claude.
  </Card>
  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Panduan langkah demi langkah untuk mendefinisikan alat.
  </Card>
</CardGroup>