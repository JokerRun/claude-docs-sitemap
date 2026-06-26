---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: aaa524122114afd8599d6c41a465b9436f37433389a5437b82a05e3b54805b7d
---

# Stop reason dan fallback

Pelajari arti setiap nilai stop_reason dan cara menangani pemotongan, penggunaan alat, giliran yang dijeda, dan penolakan dalam aplikasi Anda.

---

Setiap respons Messages API menyertakan field `stop_reason` yang memberi tahu Anda mengapa Claude berhenti menghasilkan. Periksa field ini untuk memutuskan apakah akan menggunakan respons apa adanya, melanjutkan percakapan, mencoba ulang, atau beralih ke model lain.

Untuk skema respons lengkap, lihat [referensi Messages API](/docs/id/api/messages/create).

## Referensi cepat \{#quick-reference}

| Nilai | Kapan terjadi | Apa yang harus dilakukan |
| --- | --- | --- |
| [`end_turn`](#end-turn) | Claude menyelesaikan responsnya secara alami. | Gunakan respons tersebut. |
| [`max_tokens`](#max-tokens) | Respons mencapai batas `max_tokens` Anda. | Naikkan `max_tokens` atau [lanjutkan respons](#ensuring-complete-responses). |
| [`stop_sequence`](#stop-sequence) | Claude mengeluarkan salah satu `stop_sequences` Anda. | Baca `stop_sequence` untuk melihat mana yang terpicu. |
| [`tool_use`](#tool-use) | Claude sedang memanggil alat. | Jalankan alat tersebut dan kembalikan hasilnya. |
| [`pause_turn`](#pause-turn) | Loop alat server mencapai batas iterasinya. | Kirim kembali konten asisten untuk melanjutkan. |
| [`refusal`](#refusal) | Claude menolak untuk merespons. | Baca `stop_details` dan [coba ulang pada model fallback](/docs/id/build-with-claude/refusals-and-fallback). |
| [`model_context_window_exceeded`](#model-context-window-exceeded) | Respons memenuhi jendela konteks model. | Perlakukan respons sebagai terpotong. |

## Field stop_reason \{#the-stop-reason-field}

Field `stop_reason` adalah bagian dari setiap respons Messages API yang berhasil. Tidak seperti error, yang menunjukkan kegagalan dalam memproses permintaan Anda, `stop_reason` memberi tahu Anda mengapa Claude menyelesaikan pembuatan responsnya.

```json Example response
{
  "id": "msg_01234",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here's the answer to your question..."
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

## Nilai stop reason \{#stop-reason-values}

### end_turn \{#end-turn}
Stop reason yang paling umum. Menunjukkan Claude menyelesaikan responsnya secara alami.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | jq 'if .stop_reason == "end_turn" then .content[0].text else . end'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello!"}' \
  --format json | jq 'if .stop_reason == "end_turn" then .content[0].text else . end'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
if response.stop_reason == "end_turn":
    # Proses respons lengkap
    print(response.content[0].text)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
});

if (response.stop_reason === "end_turn") {
  // Proses respons lengkap
  const block = response.content[0];
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

```csharp C# hidelines={1..4}
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }]
});

if (response.StopReason == "end_turn")
{
    // Proses respons lengkap
    if (response.Content[0].TryPickText(out var textBlock))
    {
        Console.WriteLine(textBlock.Text);
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "end_turn" {
		// Proses respons lengkap
		if block, ok := response.Content[0].AsAny().(anthropic.TextBlock); ok {
			fmt.Println(block.Text)
		}
	}
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addUserMessage("Hello!")
            .build()
    );

    if (response.stopReason().map(StopReason.END_TURN::equals).orElse(false)) {
        // Proses respons lengkap
        response.content().get(0).text().ifPresent(block -> IO.println(block.text()));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello!']],
    model: 'claude-opus-4-8',
);

if ($response->stopReason === 'end_turn') {
    // Proses respons lengkap
    echo $response->content[0]->text, PHP_EOL;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
)

if response.stop_reason == :end_turn
  # Proses respons lengkap
  puts response.content.first.text
end
```
</CodeGroup>

<section title="Respons kosong dengan end_turn">

Terkadang Claude mengembalikan respons kosong (tepat 2-3 token tanpa konten) dengan `stop_reason: "end_turn"`. Ini biasanya terjadi ketika Claude menafsirkan bahwa giliran asisten sudah selesai, terutama setelah hasil alat.

**Penyebab umum:**
- Menambahkan blok teks segera setelah hasil alat (Claude belajar untuk mengharapkan pengguna selalu menyisipkan teks setelah hasil alat, sehingga ia mengakhiri gilirannya untuk mengikuti pola tersebut)
- Mengirim kembali respons Claude yang sudah selesai tanpa menambahkan apa pun (Claude sudah memutuskan bahwa ia selesai, jadi ia akan tetap selesai)

**Cara mencegah respons kosong:**

<CodeGroup>

```python Python nocheck
# SALAH: Menambahkan teks langsung setelah tool_result
messages = [
    {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
    {
        "role": "assistant",
        "content": [
            {
                "type": "tool_use",
                "id": "toolu_123",
                "name": "calculator",
                "input": {"operation": "add", "a": 1234, "b": 5678},
            }
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "toolu_123", "content": "6912"},
            {
                "type": "text",
                "text": "Here's the result",  # Don't add text after tool_result
            },
        ],
    },
]

# BENAR: Kirim hasil alat secara langsung tanpa teks tambahan
messages = [
    {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
    {
        "role": "assistant",
        "content": [
            {
                "type": "tool_use",
                "id": "toolu_123",
                "name": "calculator",
                "input": {"operation": "add", "a": 1234, "b": 5678},
            }
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "toolu_123", "content": "6912"}
        ],
    },  # Just the tool_result, no additional text
]
```

```typescript TypeScript nocheck
// SALAH: Menambahkan teks langsung setelah tool_result
let messages: Anthropic.MessageParam[] = [
  { role: "user", content: "Calculate the sum of 1234 and 5678" },
  {
    role: "assistant",
    content: [
      {
        type: "tool_use",
        id: "toolu_123",
        name: "calculator",
        input: { operation: "add", a: 1234, b: 5678 }
      }
    ]
  },
  {
    role: "user",
    content: [
      { type: "tool_result", tool_use_id: "toolu_123", content: "6912" },
      { type: "text", text: "Here's the result" } // Don't add text after tool_result
    ]
  }
];

// BENAR: Kirim hasil alat secara langsung tanpa teks tambahan
messages = [
  { role: "user", content: "Calculate the sum of 1234 and 5678" },
  {
    role: "assistant",
    content: [
      {
        type: "tool_use",
        id: "toolu_123",
        name: "calculator",
        input: { operation: "add", a: 1234, b: 5678 }
      }
    ]
  },
  {
    role: "user",
    // Hanya tool_result, tanpa teks tambahan
    content: [{ type: "tool_result", tool_use_id: "toolu_123", content: "6912" }]
  }
];
```

```csharp C# nocheck
using System.Text.Json;
using Anthropic.Models.Messages;

var input = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
    """{"operation":"add","a":1234,"b":5678}"""
)!;

// SALAH: Menambahkan teks langsung setelah tool_result
List<MessageParam> messages =
[
    new() { Role = Role.User, Content = "Calculate the sum of 1234 and 5678" },
    new()
    {
        Role = Role.Assistant,
        Content = new List<ContentBlockParam>
        {
            new ToolUseBlockParam { ID = "toolu_123", Name = "calculator", Input = input }
        }
    },
    new()
    {
        Role = Role.User,
        Content = new List<ContentBlockParam>
        {
            new ToolResultBlockParam { ToolUseID = "toolu_123", Content = "6912" },
            new TextBlockParam { Text = "Here's the result" } // Don't add text after tool_result
        }
    }
];

// BENAR: Kirim hasil alat langsung tanpa teks tambahan
messages =
[
    new() { Role = Role.User, Content = "Calculate the sum of 1234 and 5678" },
    new()
    {
        Role = Role.Assistant,
        Content = new List<ContentBlockParam>
        {
            new ToolUseBlockParam { ID = "toolu_123", Name = "calculator", Input = input }
        }
    },
    new()
    {
        Role = Role.User,
        // Hanya tool_result, tanpa teks tambahan
        Content = new List<ContentBlockParam>
        {
            new ToolResultBlockParam { ToolUseID = "toolu_123", Content = "6912" }
        }
    }
];
```

```go Go nocheck hidelines={1..5,-2..-1}
package main

import "github.com/anthropics/anthropic-sdk-go"

func main() {
	input := map[string]any{"operation": "add", "a": 1234, "b": 5678}

	// SALAH: Menambahkan teks langsung setelah tool_result
	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock("Calculate the sum of 1234 and 5678")),
		anthropic.NewAssistantMessage(
			anthropic.NewToolUseBlock("toolu_123", input, "calculator"),
		),
		anthropic.NewUserMessage(
			anthropic.NewToolResultBlock("toolu_123", "6912", false),
			anthropic.NewTextBlock("Here's the result"), // Don't add text after tool_result
		),
	}

	// BENAR: Kirim hasil alat secara langsung tanpa teks tambahan
	messages = []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock("Calculate the sum of 1234 and 5678")),
		anthropic.NewAssistantMessage(
			anthropic.NewToolUseBlock("toolu_123", input, "calculator"),
		),
		// Hanya tool_result, tanpa teks tambahan
		anthropic.NewUserMessage(
			anthropic.NewToolResultBlock("toolu_123", "6912", false),
		),
	}
	_ = messages
}
```

```java Java nocheck
ToolUseBlockParam toolUse = ToolUseBlockParam.builder()
    .id("toolu_123")
    .name("calculator")
    .input(ToolUseBlockParam.Input.builder()
        .putAdditionalProperty("operation", JsonValue.from("add"))
        .putAdditionalProperty("a", JsonValue.from(1234))
        .putAdditionalProperty("b", JsonValue.from(5678))
        .build())
    .build();

// SALAH: Menambahkan teks langsung setelah tool_result
List<MessageParam> messages = List.of(
    MessageParam.builder().role(MessageParam.Role.USER)
        .content("Calculate the sum of 1234 and 5678").build(),
    MessageParam.builder().role(MessageParam.Role.ASSISTANT)
        .contentOfBlockParams(List.of(ContentBlockParam.ofToolUse(toolUse))).build(),
    MessageParam.builder().role(MessageParam.Role.USER)
        .contentOfBlockParams(List.of(
            ContentBlockParam.ofToolResult(
                ToolResultBlockParam.builder().toolUseId("toolu_123").content("6912").build()),
            // Jangan tambahkan teks setelah tool_result
            ContentBlockParam.ofText(TextBlockParam.builder().text("Here's the result").build())
        )).build()
);

// BENAR: Kirim hasil alat langsung tanpa teks tambahan
messages = List.of(
    MessageParam.builder().role(MessageParam.Role.USER)
        .content("Calculate the sum of 1234 and 5678").build(),
    MessageParam.builder().role(MessageParam.Role.ASSISTANT)
        .contentOfBlockParams(List.of(ContentBlockParam.ofToolUse(toolUse))).build(),
    // Hanya tool_result, tanpa teks tambahan
    MessageParam.builder().role(MessageParam.Role.USER)
        .contentOfBlockParams(List.of(
            ContentBlockParam.ofToolResult(
                ToolResultBlockParam.builder().toolUseId("toolu_123").content("6912").build())
        )).build()
);
```

```php PHP nocheck
// SALAH: Menambahkan teks langsung setelah tool_result
$messages = [
    ['role' => 'user', 'content' => 'Calculate the sum of 1234 and 5678'],
    [
        'role' => 'assistant',
        'content' => [
            [
                'type' => 'tool_use',
                'id' => 'toolu_123',
                'name' => 'calculator',
                'input' => ['operation' => 'add', 'a' => 1234, 'b' => 5678],
            ],
        ],
    ],
    [
        'role' => 'user',
        'content' => [
            ['type' => 'tool_result', 'tool_use_id' => 'toolu_123', 'content' => '6912'],
            // Jangan tambahkan teks setelah tool_result
            ['type' => 'text', 'text' => "Here's the result"],
        ],
    ],
];

// BENAR: Kirim hasil alat langsung tanpa teks tambahan
$messages = [
    ['role' => 'user', 'content' => 'Calculate the sum of 1234 and 5678'],
    [
        'role' => 'assistant',
        'content' => [
            [
                'type' => 'tool_use',
                'id' => 'toolu_123',
                'name' => 'calculator',
                'input' => ['operation' => 'add', 'a' => 1234, 'b' => 5678],
            ],
        ],
    ],
    [
        'role' => 'user',
        // Hanya tool_result, tanpa teks tambahan
        'content' => [
            ['type' => 'tool_result', 'tool_use_id' => 'toolu_123', 'content' => '6912'],
        ],
    ],
];
```

```ruby Ruby nocheck
# SALAH: Menambahkan teks langsung setelah tool_result
messages = [
  { role: "user", content: "Calculate the sum of 1234 and 5678" },
  {
    role: "assistant",
    content: [
      {
        type: "tool_use",
        id: "toolu_123",
        name: "calculator",
        input: { operation: "add", a: 1234, b: 5678 }
      }
    ]
  },
  {
    role: "user",
    content: [
      { type: "tool_result", tool_use_id: "toolu_123", content: "6912" },
      # Jangan tambahkan teks setelah tool_result
      { type: "text", text: "Here's the result" }
    ]
  }
]

# BENAR: Kirim hasil alat langsung tanpa teks tambahan
messages = [
  { role: "user", content: "Calculate the sum of 1234 and 5678" },
  {
    role: "assistant",
    content: [
      {
        type: "tool_use",
        id: "toolu_123",
        name: "calculator",
        input: { operation: "add", a: 1234, b: 5678 }
      }
    ]
  },
  {
    role: "user",
    # Hanya tool_result, tanpa teks tambahan
    content: [
      { type: "tool_result", tool_use_id: "toolu_123", content: "6912" }
    ]
  }
]
```
</CodeGroup>

Jika Anda masih mendapatkan respons kosong setelah memperbaiki struktur pesan, tambahkan prompt lanjutan dalam pesan pengguna baru daripada mencoba ulang dengan respons kosong:

<CodeGroup>

```python Python nocheck
def handle_empty_response(client, messages):
    response = client.messages.create(
        model="claude-opus-4-8", max_tokens=1024, messages=messages
    )

    # Periksa apakah respons kosong
    if response.stop_reason == "end_turn" and not response.content:
        # SALAH: Jangan hanya mencoba ulang dengan respons kosong
        # Ini tidak akan berhasil karena Claude sudah memutuskan bahwa ia selesai

        # BENAR: Tambahkan prompt lanjutan dalam pesan pengguna BARU
        messages.append({"role": "user", "content": "Please continue"})

        response = client.messages.create(
            model="claude-opus-4-8", max_tokens=1024, messages=messages
        )

    return response
```

```typescript TypeScript nocheck
async function handleEmptyResponse(
  client: Anthropic,
  messages: Anthropic.MessageParam[]
): Promise<Anthropic.Message> {
  let response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages
  });

  // Periksa apakah respons kosong
  if (response.stop_reason === "end_turn" && response.content.length === 0) {
    // SALAH: Jangan hanya mencoba ulang dengan respons kosong
    // Ini tidak akan berhasil karena Claude sudah memutuskan bahwa ia selesai

    // BENAR: Tambahkan prompt lanjutan dalam pesan pengguna BARU
    messages.push({ role: "user", content: "Please continue" });

    response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages
    });
  }

  return response;
}
```

```csharp C# nocheck
static async Task<Message> HandleEmptyResponse(AnthropicClient client, List<MessageParam> messages)
{
    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages = messages
    });

    // Periksa apakah respons kosong
    if (response.StopReason == "end_turn" && response.Content.Count == 0)
    {
        // BENAR: Tambahkan prompt lanjutan dalam pesan user BARU
        messages.Add(new() { Role = Role.User, Content = "Please continue" });

        response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1024,
            Messages = messages
        });
    }

    return response;
}
```

```go Go nocheck hidelines={1..8}
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
)

func handleEmptyResponse(client anthropic.Client, messages []anthropic.MessageParam) (*anthropic.Message, error) {
	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages:  messages,
	})
	if err != nil {
		return nil, err
	}

	// Periksa apakah respons kosong
	if response.StopReason == "end_turn" && len(response.Content) == 0 {
		// BENAR: Tambahkan prompt lanjutan dalam pesan user BARU
		messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Please continue")))

		response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 1024,
			Messages:  messages,
		})
		if err != nil {
			return nil, err
		}
	}

	return response, nil
}
```

```java Java nocheck
static Message handleEmptyResponse(AnthropicClient client, List<MessageParam> messages) {
    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .messages(messages)
            .build()
    );

    // Periksa apakah respons kosong
    boolean isEndTurn = response.stopReason().map(StopReason.END_TURN::equals).orElse(false);
    if (isEndTurn && response.content().isEmpty()) {
        // BENAR: Tambahkan prompt lanjutan dalam pesan user BARU
        List<MessageParam> extended = new ArrayList<>(messages);
        extended.add(MessageParam.builder()
            .role(MessageParam.Role.USER)
            .content("Please continue")
            .build());

        response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024L)
                .messages(extended)
                .build()
        );
    }

    return response;
}
```

```php PHP nocheck
function handle_empty_response(Client $client, array $messages)
{
    $response = $client->messages->create(
        maxTokens: 1024,
        messages: $messages,
        model: 'claude-opus-4-8',
    );

    // Periksa apakah respons kosong
    if ($response->stopReason === 'end_turn' && count($response->content) === 0) {
        // BENAR: Tambahkan prompt lanjutan dalam pesan pengguna BARU
        $messages[] = ['role' => 'user', 'content' => 'Please continue'];

        $response = $client->messages->create(
            maxTokens: 1024,
            messages: $messages,
            model: 'claude-opus-4-8',
        );
    }

    return $response;
}
```

```ruby Ruby nocheck
def handle_empty_response(client, messages)
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: messages
  )

  # Periksa apakah respons kosong
  if response.stop_reason == :end_turn && response.content.empty?
    # BENAR: Tambahkan prompt lanjutan dalam pesan pengguna BARU
    messages << { role: "user", content: "Please continue" }

    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages
    )
  end

  response
end
```
</CodeGroup>

**Praktik terbaik:**
1. **Jangan pernah menambahkan blok teks segera setelah hasil alat:** Ini mengajarkan Claude untuk mengharapkan input pengguna setelah setiap penggunaan alat.
2. **Jangan mencoba ulang respons kosong tanpa modifikasi:** Mengirim kembali respons kosong tidak akan membantu.
3. **Gunakan prompt lanjutan sebagai upaya terakhir:** Hanya jika perbaikan ini tidak menyelesaikan masalah.

</section>

### max_tokens \{#max-tokens}
Claude berhenti karena mencapai batas `max_tokens` yang ditentukan dalam permintaan Anda.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Explain quantum physics"}]
  }' | jq '.stop_reason'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 10 \
  --message '{role: user, content: "Explain quantum physics"}' \
  --format json | jq '.stop_reason'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
# Permintaan dengan token terbatas
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum physics"}],
)

if response.stop_reason == "max_tokens":
    # Respons terpotong
    print("Response was cut off at token limit")
    # Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Permintaan dengan token terbatas
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 10,
  messages: [{ role: "user", content: "Explain quantum physics" }]
});

if (response.stop_reason === "max_tokens") {
  // Respons terpotong
  console.log("Response was cut off at token limit");
  // Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
}
```

```csharp C# hidelines={1..4}
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

// Permintaan dengan token terbatas
var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 10,
    Messages = [new() { Role = Role.User, Content = "Explain quantum physics" }]
});

if (response.StopReason == "max_tokens")
{
    // Respons terpotong
    Console.WriteLine("Response was cut off at token limit");
    // Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
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

	// Permintaan dengan token terbatas
	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 10,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Explain quantum physics")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "max_tokens" {
		// Respons terpotong
		fmt.Println("Response was cut off at token limit")
		// Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
	}
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Permintaan dengan token terbatas
    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(10L)
            .addUserMessage("Explain quantum physics")
            .build()
    );

    if (response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
        // Respons terpotong
        IO.println("Response was cut off at token limit");
        // Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

// Permintaan dengan token terbatas
$response = $client->messages->create(
    maxTokens: 10,
    messages: [['role' => 'user', 'content' => 'Explain quantum physics']],
    model: 'claude-opus-4-8',
);

if ($response->stopReason === 'max_tokens') {
    // Respons terpotong
    echo 'Response was cut off at token limit', PHP_EOL;
    // Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Permintaan dengan token terbatas
response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 10,
  messages: [{ role: "user", content: "Explain quantum physics" }]
)

if response.stop_reason == :max_tokens
  # Respons terpotong
  puts "Response was cut off at token limit"
  # Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
end
```
</CodeGroup>

<section title="Blok tool use yang tidak lengkap">

Jika respons Claude terpotong karena mencapai batas `max_tokens`, dan respons yang terpotong berisi blok tool use yang tidak lengkap, Anda perlu mencoba ulang permintaan dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan tool use yang lengkap.

<CodeGroup>

```bash CLI nocheck
RESPONSE=$(ant messages create --max-tokens 1024 \
  --format jsonl < request.yaml)

# Periksa apakah respons terpotong di tengah penggunaan alat
STOP_REASON=$(jq -r '.stop_reason' <<<"$RESPONSE")
LAST_TYPE=$(jq -r '.content[-1].type' <<<"$RESPONSE")
if [ "$STOP_REASON" = "max_tokens" ] && [ "$LAST_TYPE" = "tool_use" ]; then
  # Coba lagi dengan max_tokens yang lebih tinggi
  ant messages create --max-tokens 4096 < request.yaml
fi
```

```python Python nocheck hidelines={1..18}
import anthropic

client = anthropic.Anthropic()
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    }
]
messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]
response = client.messages.create(
    model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages
)
# Periksa apakah respons terpotong selama penggunaan alat
if response.stop_reason == "max_tokens":
    # Periksa apakah blok konten terakhir adalah tool_use yang tidak lengkap
    last_block = response.content[-1]
    if last_block.type == "tool_use":
        # Kirim permintaan dengan max_tokens yang lebih tinggi
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,  # Increased limit
            messages=messages,
            tools=tools,
        )
```

```typescript TypeScript nocheck
// Periksa apakah respons terpotong selama penggunaan alat
if (response.stop_reason === "max_tokens") {
  // Periksa apakah blok konten terakhir adalah tool_use yang tidak lengkap
  const lastBlock = response.content[response.content.length - 1];
  if (lastBlock.type === "tool_use") {
    // Kirim permintaan dengan max_tokens yang lebih tinggi
    response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096, // Increased limit
      messages: messages,
      tools: tools
    });
  }
}
```

```csharp C# nocheck
using System.Linq;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = messages,
    Tools = tools
};

var response = await client.Messages.Create(parameters);

if (response.StopReason == "max_tokens")
{
    var lastBlock = response.Content.Last();
    if (lastBlock.TryPickToolUse(out _))
    {
        response = await client.Messages.Create(parameters with { MaxTokens = 4096 });
    }
}
```

```go Go hidelines={1..15,-3..-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	tools := []anthropic.ToolUnionParam{}
	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock("test"))}
	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages:  messages,
		Tools:     tools,
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "max_tokens" {
		lastBlock := response.Content[len(response.Content)-1]
		switch lastBlock.AsAny().(type) {
		case anthropic.ToolUseBlock:
			response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
				Model:     anthropic.ModelClaudeOpus4_8,
				MaxTokens: 4096,
				Messages:  messages,
				Tools:     tools,
			})
			if err != nil {
				log.Fatal(err)
			}
		}
	}

	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..14}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.MessageParam;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.ToolUnion;
import java.util.List;
AnthropicClient client = AnthropicOkHttpClient.fromEnv();
List<MessageParam> messages = List.of();
List<ToolUnion> tools = List.of();
Message response = client.messages().create(MessageCreateParams.builder().model(Model.CLAUDE_OPUS_4_8).maxTokens(1024L).addUserMessage("test").build());
// Periksa apakah respons terpotong selama penggunaan alat
if (response.stopReason().isPresent() && response.stopReason().get().equals(StopReason.MAX_TOKENS)) {
    ContentBlock lastBlock = response.content().get(response.content().size() - 1);
    if (lastBlock.toolUse().isPresent()) {
        // Kirim permintaan dengan max_tokens yang lebih tinggi
        response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(4096L) // Increased limit
                .messages(messages)
                .tools(tools)
                .build()
        );
    }
}
```

```php PHP hidelines={1..6} nocheck
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: $messages,
    model: 'claude-opus-4-8',
    tools: $tools,
);

if ($response->stopReason === 'max_tokens') {
    $lastBlock = end($response->content);
    if ($lastBlock->type === 'tool_use') {
        $response = $client->messages->create(
            maxTokens: 4096,
            messages: $messages,
            model: 'claude-opus-4-8',
            tools: $tools,
        );
    }
}
```

```ruby Ruby hidelines={1..15}
require "anthropic"

client = Anthropic::Client.new

tools = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: { type: "object", properties: { location: { type: "string" } }, required: ["location"] }
  }
]
messages = [
  { role: "user", content: "What's the weather in San Francisco?" }
]

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: messages,
  tools: tools
)

if response.stop_reason == :max_tokens
  last_block = response.content.last
  if last_block.type == :tool_use
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages,
      tools: tools
    )
  end
end
```
</CodeGroup>

</section>

### stop_sequence \{#stop-sequence}
Claude menemukan salah satu stop sequence kustom Anda.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "stop_sequences": ["END", "STOP"],
    "messages": [{"role": "user", "content": "Generate text until you say END"}]
  }' | jq '{stop_reason, stop_sequence}'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --stop-sequence END --stop-sequence STOP \
  --message '{role: user, content: "Generate text until you say END"}' \
  --format json | jq '{stop_reason, stop_sequence}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  stop_sequences: ["END", "STOP"],
  messages: [{ role: "user", content: "Generate text until you say END" }]
});

if (response.stop_reason === "stop_sequence") {
  console.log(`Stopped at sequence: ${response.stop_sequence}`);
}
```

```csharp C# hidelines={1..4}
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    StopSequences = ["END", "STOP"],
    Messages = [new() { Role = Role.User, Content = "Generate text until you say END" }]
});

if (response.StopReason == "stop_sequence")
{
    Console.WriteLine($"Stopped at sequence: {response.StopSequence}");
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
		Model:         anthropic.ModelClaudeOpus4_8,
		MaxTokens:     1024,
		StopSequences: []string{"END", "STOP"},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Generate text until you say END")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "stop_sequence" {
		fmt.Printf("Stopped at sequence: %s\n", response.StopSequence)
	}
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addStopSequence("END")
            .addStopSequence("STOP")
            .addUserMessage("Generate text until you say END")
            .build()
    );

    if (response.stopReason().map(StopReason.STOP_SEQUENCE::equals).orElse(false)) {
        IO.println("Stopped at sequence: " + response.stopSequence().orElse(""));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Generate text until you say END']],
    model: 'claude-opus-4-8',
    stopSequences: ['END', 'STOP'],
);

if ($response->stopReason === 'stop_sequence') {
    echo "Stopped at sequence: {$response->stopSequence}", PHP_EOL;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  stop_sequences: ["END", "STOP"],
  messages: [{ role: "user", content: "Generate text until you say END" }]
)

if response.stop_reason == :stop_sequence
  puts "Stopped at sequence: #{response.stop_sequence}"
end
```
</CodeGroup>

### tool_use \{#tool-use}
Claude sedang memanggil alat dan mengharapkan Anda untuk mengeksekusinya.

<Note>
Untuk sebagian besar implementasi penggunaan alat, gunakan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner), yang secara otomatis menangani eksekusi alat, pemformatan hasil, dan manajemen percakapan.
</Note>

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "tools": [{
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string", "description": "City and state"}},
        "required": ["location"]
      }
    }],
    "messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]
  }' | jq '.stop_reason, (.content[] | select(.type == "tool_use"))'
```

```bash CLI
ant messages create --format json <<'YAML' | jq '.stop_reason, (.content[] | select(.type == "tool_use"))'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content: What is the weather in San Francisco?
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location: {type: string, description: City and state}
      required: [location]
YAML
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"},
        },
        "required": ["location"],
    },
}


def execute_tool(name, tool_input):
    """Execute a tool and return the result."""
    return f"Weather in {tool_input.get('location', 'unknown')}: 72°F"


response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What is the weather in San Francisco?"}],
)

if response.stop_reason == "tool_use":
    # Ekstrak dan jalankan alat
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            # Kembalikan hasil ke Claude untuk respons akhir
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const weatherTool: Anthropic.Tool = {
  name: "get_weather",
  description: "Get the current weather in a given location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string", description: "City and state" }
    },
    required: ["location"]
  }
};

function executeTool(name: string, input: Record<string, string>): string {
  return `Weather in ${input.location ?? "unknown"}: 72°F`;
}

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [weatherTool],
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }]
});

if (response.stop_reason === "tool_use") {
  // Ekstrak dan jalankan alat
  for (const block of response.content) {
    if (block.type === "tool_use") {
      const result = executeTool(block.name, block.input as Record<string, string>);
      // Kembalikan hasil ke Claude untuk respons akhir
    }
  }
}
```

```csharp C# nocheck hidelines={1..7}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var weatherTool = new Tool
{
    Name = "get_weather",
    Description = "Get the current weather in a given location",
    InputSchema = new InputSchema
    {
        Properties = new Dictionary<string, JsonElement>
        {
            ["location"] = JsonSerializer.SerializeToElement(
                new { type = "string", description = "City and state" }
            ),
        },
        Required = ["location"]
    }
};

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Tools = [weatherTool],
    Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco?" }]
});

if (response.StopReason == "tool_use")
{
    // Ekstrak dan jalankan alat
    foreach (var block in response.Content)
    {
        if (block.TryPickToolUse(out var toolUse))
        {
            // Jalankan toolUse.Name dengan toolUse.Input dan kembalikan hasilnya ke Claude
        }
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	weatherTool := anthropic.ToolParam{
		Name:        "get_weather",
		Description: anthropic.String("Get the current weather in a given location"),
		InputSchema: anthropic.ToolInputSchemaParam{
			Properties: map[string]any{
				"location": map[string]string{"type": "string", "description": "City and state"},
			},
			Required: []string{"location"},
		},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools:     []anthropic.ToolUnionParam{{OfTool: &weatherTool}},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "tool_use" {
		// Ekstrak dan jalankan alat
		for _, block := range response.Content {
			if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
				fmt.Println(toolUse.Name, toolUse.Input)
				// Kembalikan hasil ke Claude untuk respons akhir
			}
		}
	}
}
```

```java Java nocheck hidelines={1..12,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.Tool;
import java.util.List;
import java.util.Map;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Tool weatherTool = Tool.builder()
        .name("get_weather")
        .description("Get the current weather in a given location")
        .inputSchema(Tool.InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "location", Map.of("type", "string", "description", "City and state")
            )))
            .putAdditionalProperty("required", JsonValue.from(List.of("location")))
            .build())
        .build();

    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addTool(weatherTool)
            .addUserMessage("What is the weather in San Francisco?")
            .build()
    );

    if (response.stopReason().map(StopReason.TOOL_USE::equals).orElse(false)) {
        // Ekstrak dan jalankan alat
        for (ContentBlock block : response.content()) {
            block.toolUse().ifPresent(toolUse -> {
                // Jalankan toolUse.name() dengan toolUse.input() dan kembalikan hasilnya ke Claude
            });
        }
    }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$weatherTool = [
    'name' => 'get_weather',
    'description' => 'Get the current weather in a given location',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'location' => ['type' => 'string', 'description' => 'City and state'],
        ],
        'required' => ['location'],
    ],
];

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'What is the weather in San Francisco?']],
    model: 'claude-opus-4-8',
    tools: [$weatherTool],
);

if ($response->stopReason === 'tool_use') {
    // Ekstrak dan jalankan alat
    foreach ($response->content as $block) {
        if ($block->type === 'tool_use') {
            // Jalankan $block->name dengan $block->input dan kembalikan hasilnya ke Claude
        }
    }
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

weather_tool = {
  name: "get_weather",
  description: "Get the current weather in a given location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string", description: "City and state" }
    },
    required: ["location"]
  }
}

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [weather_tool],
  messages: [{ role: "user", content: "What is the weather in San Francisco?" }]
)

if response.stop_reason == :tool_use
  # Ekstrak dan jalankan alat
  response.content.each do |block|
    next unless block.type == :tool_use
    # Jalankan block.name dengan block.input dan kembalikan hasilnya ke Claude
  end
end
```
</CodeGroup>

### pause_turn \{#pause-turn}
Dikembalikan ketika loop sampling sisi server mencapai batas iterasinya saat mengeksekusi [alat server](/docs/id/agents-and-tools/tool-use/server-tools) seperti web search atau web fetch. Batas default adalah 10 iterasi per permintaan.

Ketika ini terjadi, respons mungkin berisi blok `server_tool_use` tanpa `server_tool_result` yang sesuai. Untuk membiarkan Claude menyelesaikan pemrosesan, lanjutkan percakapan dengan mengirim kembali respons apa adanya.

<CodeGroup>
```bash cURL
# SDK menangani kelanjutan secara langsung. Dengan cURL, periksa stop_reason
# pada respons dan kirim ulang POST dengan konten asisten ditambahkan.
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 4096,
    "tools": [{"type": "web_search_20250305", "name": "web_search"}],
    "messages": [{"role": "user", "content": "Search for latest AI news"}]
  }' | jq '{stop_reason, content}'
```

```bash CLI
# Periksa stop_reason; jika nilainya pause_turn, jalankan ulang dengan respons
# asisten yang ditambahkan ke --message.
ant messages create --format json <<'YAML' | jq '{stop_reason, content}'
model: claude-opus-4-8
max_tokens: 4096
tools:
  - {type: web_search_20250305, name: web_search}
messages:
  - {role: user, content: "Search for latest AI news"}
YAML
```

```python Python nocheck
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Search for latest AI news"}],
)

if response.stop_reason == "pause_turn":
    # Lanjutkan percakapan dengan mengirim kembali respons tersebut
    messages = [
        {"role": "user", "content": "Search for latest AI news"},
        {"role": "assistant", "content": response.content},
    ]
    continuation = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
```

```typescript TypeScript nocheck
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 4096,
  tools: [{ type: "web_search_20250305", name: "web_search" }],
  messages: [{ role: "user", content: "Search for latest AI news" }]
});

if (response.stop_reason === "pause_turn") {
  // Lanjutkan percakapan dengan mengirim kembali respons tersebut
  const continuation = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    tools: [{ type: "web_search_20250305", name: "web_search" }],
    messages: [
      { role: "user", content: "Search for latest AI news" },
      { role: "assistant", content: response.content }
    ]
  });
}
```

```csharp C# nocheck
List<ToolUnion> tools = [new ToolUnion(new WebSearchTool20250305())];
MessageParam userMessage = new() { Role = Role.User, Content = "Search for latest AI news" };

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 4096,
    Tools = tools,
    Messages = [userMessage]
});

if (response.StopReason == "pause_turn")
{
    // Lanjutkan percakapan dengan mengirim kembali respons tersebut
    var continuation = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 4096,
        Tools = tools,
        Messages =
        [
            userMessage,
            new()
            {
                Role = Role.Assistant,
                Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
            }
        ]
    });
}
```

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	tools := []anthropic.ToolUnionParam{
		{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{}},
	}
	userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock("Search for latest AI news"))

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 4096,
		Tools:     tools,
		Messages:  []anthropic.MessageParam{userMessage},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "pause_turn" {
		// Lanjutkan percakapan dengan mengirim kembali respons tersebut
		var contentParams []anthropic.ContentBlockParamUnion
		for _, block := range response.Content {
			contentParams = append(contentParams, block.ToParam())
		}
		continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 4096,
			Tools:     tools,
			Messages:  []anthropic.MessageParam{userMessage, anthropic.NewAssistantMessage(contentParams...)},
		})
		if err != nil {
			log.Fatal(err)
		}
		_ = continuation
	}
}
```

```java Java nocheck
Message response = client.messages().create(
    MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(4096L)
        .addTool(WebSearchTool20250305.builder().build())
        .addUserMessage("Search for latest AI news")
        .build()
);

if (response.stopReason().map(StopReason.PAUSE_TURN::equals).orElse(false)) {
    // Lanjutkan percakapan dengan mengirim kembali respons tersebut
    Message continuation = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(4096L)
            .addTool(WebSearchTool20250305.builder().build())
            .addUserMessage("Search for latest AI news")
            .addMessage(response)
            .build()
    );
}
```

```php PHP nocheck
$tools = [['type' => 'web_search_20250305', 'name' => 'web_search']];
$userMessage = ['role' => 'user', 'content' => 'Search for latest AI news'];

$response = $client->messages->create(
    maxTokens: 4096,
    messages: [$userMessage],
    model: 'claude-opus-4-8',
    tools: $tools,
);

if ($response->stopReason === 'pause_turn') {
    // Lanjutkan percakapan dengan mengirim kembali respons tersebut
    $continuation = $client->messages->create(
        maxTokens: 4096,
        messages: [
            $userMessage,
            ['role' => 'assistant', 'content' => $response->content],
        ],
        model: 'claude-opus-4-8',
        tools: $tools,
    );
}
```

```ruby Ruby nocheck
tools = [{ type: "web_search_20250305", name: "web_search" }]
user_message = { role: "user", content: "Search for latest AI news" }

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 4096,
  tools: tools,
  messages: [user_message]
)

if response.stop_reason == :pause_turn
  # Lanjutkan percakapan dengan mengirim kembali respons tersebut
  continuation = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    tools: tools,
    messages: [user_message, { role: "assistant", content: response.content }]
  )
end
```
</CodeGroup>

<Note>
Aplikasi Anda harus menangani `pause_turn` dalam setiap loop agen yang menggunakan alat server. Tambahkan respons asisten ke array pesan Anda dan buat permintaan API lain untuk membiarkan Claude melanjutkan.
</Note>

### refusal \{#refusal}
Claude menolak untuk menghasilkan respons. Pada Claude Fable 5, pengklasifikasi keamanan mengembalikan stop reason ini sebagai respons HTTP 200 normal, bukan error.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "[Unsafe request]"}]
  }' | jq '{stop_reason, stop_details}'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "[Unsafe request]"}' \
  --format json | jq '{stop_reason, stop_details}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "[Unsafe request]"}],
)

if response.stop_reason == "refusal":
    # Claude menolak untuk merespons
    print("Claude was unable to process this request")
    # Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "[Unsafe request]" }]
});

if (response.stop_reason === "refusal") {
  // Claude menolak untuk merespons
  console.log("Claude was unable to process this request");
  // Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
}
```

```csharp C# hidelines={1..4}
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var response = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "[Unsafe request]" }]
});

if (response.StopReason == "refusal")
{
    // Claude menolak untuk merespons
    Console.WriteLine("Claude was unable to process this request");
    // Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("[Unsafe request]")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "refusal" {
		// Claude menolak untuk merespons
		fmt.Println("Claude was unable to process this request")
		// Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
	}
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Message response = client.messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addUserMessage("[Unsafe request]")
            .build()
    );

    if (response.stopReason().map(StopReason.REFUSAL::equals).orElse(false)) {
        // Claude menolak untuk merespons
        IO.println("Claude was unable to process this request");
        // Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => '[Unsafe request]']],
    model: 'claude-opus-4-8',
);

if ($response->stopReason === 'refusal') {
    // Claude menolak untuk merespons
    echo 'Claude was unable to process this request', PHP_EOL;
    // Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "[Unsafe request]" }]
)

if response.stop_reason == :refusal
  # Claude menolak untuk merespons
  puts "Claude was unable to process this request"
  # Pertimbangkan untuk menyusun ulang atau memodifikasi permintaan
end
```
</CodeGroup>

<Tip>
Jika Anda sering menemukan stop reason `refusal` saat menggunakan Claude Sonnet 4.5 atau Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)), Anda dapat mencoba memperbarui panggilan API Anda untuk menggunakan Haiku 4.5 (`claude-haiku-4-5-20251001`), yang memiliki batasan penggunaan yang berbeda. Pelajari lebih lanjut tentang [memahami filter keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

Pada penolakan, objek `stop_details` mengidentifikasi kategori kebijakan yang memicunya. Kategori dan bentuk respons penolakan lengkap dibahas di [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response). `stop_details` bernilai `null` untuk semua stop reason selain `refusal`.

Permintaan yang ditolak pada Claude Fable 5 biasanya dapat dilayani dengan mencoba ulang pada model Claude lain, dan [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) menunjukkan cara menyiapkan percobaan ulang tersebut, di sisi server atau di klien Anda. [Kredit fallback](/docs/id/build-with-claude/fallback-credit) membahas cara menghindari membayar biaya cache prompt dua kali ketika Anda membangun percobaan ulang sendiri.

### model_context_window_exceeded \{#model-context-window-exceeded}
Claude berhenti karena mencapai batas jendela konteks model. Ini memungkinkan Anda meminta token maksimum yang mungkin tanpa mengetahui ukuran input yang tepat.

<Note>
Stop reason ini saat ini hanya diketik dalam namespace `beta` SDK, sehingga contoh berikut memanggil `client.beta.messages` dan menggunakan tipe dengan prefiks `Beta`. Pada Sonnet 4.5 dan model yang lebih baru, API mengembalikan nilai ini tanpa header beta. Untuk model sebelumnya, tambahkan header beta `model-context-window-exceeded-2025-08-26` untuk mengaktifkannya.
</Note>

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 20000,
    "messages": [{"role": "user", "content": "Large input that uses most of context window..."}]
  }' | jq '.stop_reason'
```

```bash CLI
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 20000 \
  --message '{role: user, content: "Large input that uses most of context window..."}' \
  --format json | jq '.stop_reason'
```

```python Python nocheck
# Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k (Opus 4.8 supports 128k with streaming)
    messages=[
        {"role": "user", "content": "Large input that uses most of context window..."}
    ],
)

if response.stop_reason == "model_context_window_exceeded":
    # Respons mencapai batas jendela konteks sebelum max_tokens
    print("Response reached model's context window limit")
    # Respons tetap valid tetapi dibatasi oleh jendela konteks
```

```typescript TypeScript nocheck
// Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 20000,
  messages: [{ role: "user", content: "Large input that uses most of context window..." }]
});

if (response.stop_reason === "model_context_window_exceeded") {
  // Respons mencapai batas jendela konteks sebelum max_tokens
  console.log("Response reached model's context window limit");
  // Respons tetap valid tetapi dibatasi oleh jendela konteks
}
```

```csharp C# nocheck
using Anthropic.Models.Beta.Messages;
using Model = Anthropic.Models.Messages.Model;

// Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 20000,
    Messages = [new() { Role = Role.User, Content = "Large input that uses most of context window..." }]
});

if (response.StopReason?.Value() == BetaStopReason.ModelContextWindowExceeded)
{
    // Respons mencapai batas jendela konteks sebelum max_tokens
    Console.WriteLine("Response reached model's context window limit");
    // Respons tetap valid tetapi dibatasi oleh jendela konteks
}
```

```go Go nocheck hidelines={1..3,-1}
package main

func main() {
	// Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 20000,
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Large input that uses most of context window...")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == anthropic.BetaStopReasonModelContextWindowExceeded {
		// Respons mencapai batas jendela konteks sebelum max_tokens
		fmt.Println("Response reached model's context window limit")
		// Respons tetap valid tetapi dibatasi oleh jendela konteks
	}
}
```

```java Java nocheck
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaStopReason;
import com.anthropic.models.beta.messages.MessageCreateParams;

// Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
BetaMessage response = client.beta().messages().create(
    MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(20000L)
        .addUserMessage("Large input that uses most of context window...")
        .build()
);

if (response.stopReason().map(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED::equals).orElse(false)) {
    // Respons mencapai batas jendela konteks sebelum max_tokens
    IO.println("Response reached model's context window limit");
    // Respons tetap valid tetapi dibatasi oleh jendela konteks
}
```

```php PHP nocheck
// Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
$response = $client->beta->messages->create(
    maxTokens: 20000,
    messages: [['role' => 'user', 'content' => 'Large input that uses most of context window...']],
    model: 'claude-opus-4-8',
);

if ($response->stopReason === 'model_context_window_exceeded') {
    // Respons mencapai batas jendela konteks sebelum max_tokens
    echo 'Response reached model\'s context window limit', PHP_EOL;
    // Respons tetap valid tetapi dibatasi oleh jendela konteks
}
```

```ruby Ruby nocheck
# Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
response = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 20000,
  messages: [{ role: "user", content: "Large input that uses most of context window..." }]
)

if response.stop_reason == :model_context_window_exceeded
  # Respons mencapai batas jendela konteks sebelum max_tokens
  puts "Response reached model's context window limit"
  # Respons tetap valid tetapi dibatasi oleh jendela konteks
end
```
</CodeGroup>

## Praktik terbaik untuk menangani stop reason \{#best-practices-for-handling-stop-reasons}

### Selalu periksa stop_reason \{#always-check-stop-reason}

Biasakan untuk memeriksa `stop_reason` dalam logika penanganan respons Anda:

<CodeGroup>

```python Python nocheck
def handle_response(response):
    if response.stop_reason == "tool_use":
        return handle_tool_use(response)
    elif response.stop_reason == "max_tokens":
        return handle_truncation(response)
    elif response.stop_reason == "model_context_window_exceeded":
        return handle_context_limit(response)
    elif response.stop_reason == "pause_turn":
        return handle_pause(response)
    elif response.stop_reason == "refusal":
        return handle_refusal(response)
    else:
        # Tangani end_turn dan kasus lainnya
        return response.content[0].text
```

```typescript TypeScript nocheck
function handleResponse(response: Anthropic.Beta.BetaMessage): string {
  switch (response.stop_reason) {
    case "tool_use":
      return handleToolUse(response);
    case "max_tokens":
      return handleTruncation(response);
    case "model_context_window_exceeded":
      return handleContextLimit(response);
    case "pause_turn":
      return handlePause(response);
    case "refusal":
      return handleRefusal(response);
    default: {
      // Tangani end_turn dan kasus lainnya
      const block = response.content[0];
      return block.type === "text" ? block.text : "";
    }
  }
}
```

```csharp C# nocheck
static string HandleResponse(BetaMessage response)
{
    return response.StopReason?.Value() switch
    {
        BetaStopReason.ToolUse => HandleToolUse(response),
        BetaStopReason.MaxTokens => HandleTruncation(response),
        BetaStopReason.ModelContextWindowExceeded => HandleContextLimit(response),
        BetaStopReason.PauseTurn => HandlePause(response),
        BetaStopReason.Refusal => HandleRefusal(response),
        // Tangani end_turn dan kasus lainnya
        _ => response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "",
    };
}
```

```go Go nocheck hidelines={1..2}
package main

func handleResponse(response *anthropic.BetaMessage) string {
	switch response.StopReason {
	case anthropic.BetaStopReasonToolUse:
		return handleToolUse(response)
	case anthropic.BetaStopReasonMaxTokens:
		return handleTruncation(response)
	case anthropic.BetaStopReasonModelContextWindowExceeded:
		return handleContextLimit(response)
	case anthropic.BetaStopReasonPauseTurn:
		return handlePause(response)
	case anthropic.BetaStopReasonRefusal:
		return handleRefusal(response)
	default:
		// Tangani end_turn dan kasus lainnya
		if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
			return block.Text
		}
		return ""
	}
}
```

```java Java nocheck
static String handleResponse(BetaMessage response) {
    BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);
    if (reason.equals(BetaStopReason.TOOL_USE)) {
        return handleToolUse(response);
    } else if (reason.equals(BetaStopReason.MAX_TOKENS)) {
        return handleTruncation(response);
    } else if (reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
        return handleContextLimit(response);
    } else if (reason.equals(BetaStopReason.PAUSE_TURN)) {
        return handlePause(response);
    } else if (reason.equals(BetaStopReason.REFUSAL)) {
        return handleRefusal(response);
    }
    // Tangani end_turn dan kasus lainnya
    return response.content().get(0).text().map(BetaTextBlock::text).orElse("");
}
```

```php PHP nocheck
function handle_response($response): string
{
    return match ($response->stopReason) {
        'tool_use' => handle_tool_use($response),
        'max_tokens' => handle_truncation($response),
        'model_context_window_exceeded' => handle_context_limit($response),
        'pause_turn' => handle_pause($response),
        'refusal' => handle_refusal($response),
        // Tangani end_turn dan kasus lainnya
        default => $response->content[0]->text,
    };
}
```

```ruby Ruby nocheck
def handle_response(response)
  case response.stop_reason
  when :tool_use then handle_tool_use(response)
  when :max_tokens then handle_truncation(response)
  when :model_context_window_exceeded then handle_context_limit(response)
  when :pause_turn then handle_pause(response)
  when :refusal then handle_refusal(response)
  else
    # Tangani end_turn dan kasus lainnya
    response.content.first.text
  end
end
```
</CodeGroup>

### Tangani respons terpotong dengan baik \{#handle-truncated-responses-gracefully}

Ketika respons terpotong karena batas token atau jendela konteks, tambahkan pemberitahuan agar pembaca tahu bahwa output tidak lengkap. Untuk melanjutkan pembuatan dari tempat respons terhenti, lihat [Memastikan respons lengkap](#ensuring-complete-responses).

<CodeGroup>

```python Python nocheck
def handle_truncated_response(response):
    if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
        if response.stop_reason == "max_tokens":
            note = "[Response truncated due to max_tokens limit]"
        else:
            note = "[Response truncated due to context window limit]"
        return f"{response.content[0].text}\n\n{note}"
    return response.content[0].text
```

```typescript TypeScript nocheck
function handleTruncatedResponse(response: Anthropic.Beta.BetaMessage): string {
  const text = response.content[0].type === "text" ? response.content[0].text : "";

  if (
    response.stop_reason === "max_tokens" ||
    response.stop_reason === "model_context_window_exceeded"
  ) {
    const note =
      response.stop_reason === "max_tokens"
        ? "[Response truncated due to max_tokens limit]"
        : "[Response truncated due to context window limit]";
    return `${text}\n\n${note}`;
  }
  return text;
}
```

```csharp C# nocheck
static string HandleTruncatedResponse(BetaMessage response)
{
    var text = response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "";
    var reason = response.StopReason?.Value();

    if (reason is BetaStopReason.MaxTokens or BetaStopReason.ModelContextWindowExceeded)
    {
        var note = reason == BetaStopReason.MaxTokens
            ? "[Response truncated due to max_tokens limit]"
            : "[Response truncated due to context window limit]";
        return $"{text}\n\n{note}";
    }
    return text;
}
```

```go Go nocheck hidelines={1..2}
package main

func handleTruncatedResponse(response *anthropic.BetaMessage) string {
	text := ""
	if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
		text = block.Text
	}

	if response.StopReason == anthropic.BetaStopReasonMaxTokens ||
		response.StopReason == anthropic.BetaStopReasonModelContextWindowExceeded {
		note := "[Response truncated due to context window limit]"
		if response.StopReason == anthropic.BetaStopReasonMaxTokens {
			note = "[Response truncated due to max_tokens limit]"
		}
		return text + "\n\n" + note
	}
	return text
}
```

```java Java nocheck
static String handleTruncatedResponse(BetaMessage response) {
    String text = response.content().get(0).text().map(BetaTextBlock::text).orElse("");
    BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);

    if (reason.equals(BetaStopReason.MAX_TOKENS)
            || reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
        String note = reason.equals(BetaStopReason.MAX_TOKENS)
            ? "[Response truncated due to max_tokens limit]"
            : "[Response truncated due to context window limit]";
        return text + "\n\n" + note;
    }
    return text;
}
```

```php PHP nocheck
function handle_truncated_response($response): string
{
    $text = $response->content[0]->text;

    if (in_array($response->stopReason, ['max_tokens', 'model_context_window_exceeded'], true)) {
        $note = $response->stopReason === 'max_tokens'
            ? '[Response truncated due to max_tokens limit]'
            : '[Response truncated due to context window limit]';
        return "{$text}\n\n{$note}";
    }
    return $text;
}
```

```ruby Ruby nocheck
def handle_truncated_response(response)
  text = response.content.first.text

  if [:max_tokens, :model_context_window_exceeded].include?(response.stop_reason)
    note = if response.stop_reason == :max_tokens
      "[Response truncated due to max_tokens limit]"
    else
      "[Response truncated due to context window limit]"
    end
    return "#{text}\n\n#{note}"
  end
  text
end
```
</CodeGroup>

### Implementasikan logika percobaan ulang untuk pause_turn \{#implement-retry-logic-for-pause-turn}

Saat menggunakan [alat server](/docs/id/agents-and-tools/tool-use/server-tools), API mungkin mengembalikan `pause_turn` jika loop sampling sisi server mencapai batas iterasinya (default 10). Tangani ini dengan melanjutkan percakapan:

<CodeGroup>

```python Python nocheck
def handle_server_tool_conversation(client, user_query, tools, max_continuations=5):
    """
    Handle server tool conversations that may require multiple continuations.

    The server runs a sampling loop when executing server tools. If the loop
    reaches its iteration limit, the API returns pause_turn. Continue the
    conversation by sending the response back to let Claude finish.
    """
    messages = [{"role": "user", "content": user_query}]

    for _ in range(max_continuations):
        response = client.messages.create(
            model="claude-opus-4-8", max_tokens=4096, messages=messages, tools=tools
        )

        if response.stop_reason != "pause_turn":
            # Claude selesai memproses - kembalikan respons akhir
            return response

        # pause_turn: ganti seluruh daftar pesan untuk menjaga peran tetap bergantian
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.content},
        ]

    # Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
    return response
```

```typescript TypeScript nocheck
async function handleServerToolConversation(
  client: Anthropic,
  userQuery: string,
  tools: Anthropic.ToolUnion[],
  maxContinuations = 5
): Promise<Anthropic.Message> {
  let messages: Anthropic.MessageParam[] = [{ role: "user", content: userQuery }];
  let response: Anthropic.Message;

  for (let i = 0; i < maxContinuations; i++) {
    response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages,
      tools
    });

    if (response.stop_reason !== "pause_turn") {
      // Claude selesai memproses - kembalikan respons akhir
      return response;
    }

    // pause_turn: ganti seluruh daftar pesan untuk menjaga peran yang bergantian
    messages = [
      { role: "user", content: userQuery },
      { role: "assistant", content: response.content }
    ];
  }

  // Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
  return response!;
}
```

```csharp C# nocheck
static async Task<Message> HandleServerToolConversation(
    AnthropicClient client,
    string userQuery,
    List<ToolUnion> tools,
    int maxContinuations = 5)
{
    List<MessageParam> messages = [new() { Role = Role.User, Content = userQuery }];
    Message response = null!;

    for (var i = 0; i < maxContinuations; i++)
    {
        response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 4096,
            Messages = messages,
            Tools = tools
        });

        if (response.StopReason != "pause_turn")
        {
            // Claude selesai memproses - kembalikan respons akhir
            return response;
        }

        // pause_turn: ganti seluruh daftar pesan untuk menjaga peran tetap bergantian
        messages =
        [
            new() { Role = Role.User, Content = userQuery },
            new()
            {
                Role = Role.Assistant,
                Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
            }
        ];
    }

    // Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
    return response;
}
```

```go Go nocheck hidelines={1..2}
package main

func handleServerToolConversation(
	client anthropic.Client,
	userQuery string,
	tools []anthropic.ToolUnionParam,
	maxContinuations int,
) (*anthropic.Message, error) {
	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery))}
	var response *anthropic.Message
	var err error

	for range maxContinuations {
		response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 4096,
			Messages:  messages,
			Tools:     tools,
		})
		if err != nil {
			return nil, err
		}

		if response.StopReason != "pause_turn" {
			// Claude selesai memproses - kembalikan respons akhir
			return response, nil
		}

		// pause_turn: ganti seluruh daftar pesan untuk menjaga peran yang berselang-seling
		var contentParams []anthropic.ContentBlockParamUnion
		for _, block := range response.Content {
			contentParams = append(contentParams, block.ToParam())
		}
		messages = []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery)),
			anthropic.NewAssistantMessage(contentParams...),
		}
	}

	// Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
	return response, nil
}
```

```java Java nocheck
static Message handleServerToolConversation(
    AnthropicClient client,
    String userQuery,
    List<Tool> tools,
    int maxContinuations
) {
    Message response = null;

    for (int i = 0; i < maxContinuations; i++) {
        // Bangun ulang params setiap iterasi agar pesan tidak terakumulasi
        MessageCreateParams.Builder params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(4096L)
            .addUserMessage(userQuery);
        tools.forEach(params::addTool);
        if (response != null) {
            params.addMessage(response);
        }

        response = client.messages().create(params.build());

        if (!response.stopReason().map(StopReason.PAUSE_TURN::equals).orElse(false)) {
            // Claude selesai memproses - kembalikan respons akhir
            return response;
        }
        // pause_turn: ulangi loop dan kirim kembali responsnya
    }

    // Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
    return response;
}
```

```php PHP nocheck
function handle_server_tool_conversation(
    Client $client,
    string $userQuery,
    array $tools,
    int $maxContinuations = 5
) {
    $messages = [['role' => 'user', 'content' => $userQuery]];
    $response = null;

    for ($i = 0; $i < $maxContinuations; $i++) {
        $response = $client->messages->create(
            maxTokens: 4096,
            messages: $messages,
            model: 'claude-opus-4-8',
            tools: $tools,
        );

        if ($response->stopReason !== 'pause_turn') {
            // Claude selesai memproses - kembalikan respons akhir
            return $response;
        }

        // pause_turn: ganti seluruh daftar pesan untuk menjaga peran yang bergantian
        $messages = [
            ['role' => 'user', 'content' => $userQuery],
            ['role' => 'assistant', 'content' => $response->content],
        ];
    }

    // Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
    return $response;
}
```

```ruby Ruby nocheck
def handle_server_tool_conversation(client, user_query, tools, max_continuations: 5)
  messages = [{ role: "user", content: user_query }]
  response = nil

  max_continuations.times do
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages,
      tools: tools
    )

    # Claude selesai memproses - kembalikan respons akhir
    return response unless response.stop_reason == :pause_turn

    # pause_turn: ganti seluruh daftar pesan untuk mempertahankan peran yang berselang-seling
    messages = [
      { role: "user", content: user_query },
      { role: "assistant", content: response.content }
    ]
  end

  # Mencapai jumlah kelanjutan maksimum - kembalikan respons terakhir
  response
end
```
</CodeGroup>

## Stop reason vs. error \{#stop-reasons-vs-errors}

Penting untuk membedakan antara nilai `stop_reason` dan error yang sebenarnya:

### Stop reason (respons berhasil) \{#stop-reasons-successful-responses}
- Bagian dari body respons
- Menunjukkan mengapa pembuatan berhenti secara normal
- Respons berisi konten yang valid

### Error (permintaan gagal) \{#errors-failed-requests}
- Kode status HTTP 4xx atau 5xx
- Menunjukkan kegagalan pemrosesan permintaan
- Respons berisi detail error

<CodeGroup>
```bash cURL
# cURL keluar dengan kode non-nol pada error HTTP dengan --fail-with-body; periksa
# $? untuk error dan stop_reason untuk respons yang berhasil.
curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | jq '.stop_reason'
```

```bash CLI
# CLI keluar dengan kode non-nol pada kesalahan API; stop_reason muncul saat berhasil.
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello!"}' \
  --format json | jq '.stop_reason'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

try:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}],
    )

    # Tangani respons yang berhasil dengan stop_reason
    if response.stop_reason == "max_tokens":
        print("Response was truncated")

except anthropic.APIStatusError as e:
    # Tangani error yang sebenarnya
    if e.status_code == 429:
        print("Rate limit exceeded")
    elif e.status_code == 500:
        print("Server error")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

try {
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });

  // Tangani respons yang berhasil dengan stop_reason
  if (response.stop_reason === "max_tokens") {
    console.log("Response was truncated");
  }
} catch (err) {
  // Tangani error yang sebenarnya
  if (err instanceof Anthropic.APIError) {
    if (err.status === 429) {
      console.log("Rate limit exceeded");
    } else if (err.status === 500) {
      console.log("Server error");
    }
  } else {
    throw err;
  }
}
```

```csharp C# hidelines={1..5}
using System;
using Anthropic;
using Anthropic.Exceptions;
using Anthropic.Models.Messages;

AnthropicClient client = new();

try
{
    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages = [new() { Role = Role.User, Content = "Hello!" }]
    });

    // Tangani respons yang berhasil dengan stop_reason
    if (response.StopReason == "max_tokens")
    {
        Console.WriteLine("Response was truncated");
    }
}
catch (AnthropicRateLimitException)
{
    // Tangani error yang sebenarnya
    Console.WriteLine("Rate limit exceeded");
}
catch (Anthropic5xxException)
{
    Console.WriteLine("Server error");
}
```

```go Go hidelines={1..12,-1}
package main

import (
	"context"
	"errors"
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
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})
	if err != nil {
		// Tangani error yang sebenarnya
		var apiErr *anthropic.Error
		if errors.As(err, &apiErr) {
			switch apiErr.StatusCode {
			case 429:
				fmt.Println("Rate limit exceeded")
			case 500:
				fmt.Println("Server error")
			}
		}
		log.Fatal(err)
	}

	// Tangani respons yang berhasil dengan stop_reason
	if response.StopReason == "max_tokens" {
		fmt.Println("Response was truncated")
	}
}
```

```java Java hidelines={1..10,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.errors.AnthropicServiceException;
import com.anthropic.errors.RateLimitException;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.StopReason;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    try {
        Message response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024L)
                .addUserMessage("Hello!")
                .build()
        );

        // Handle successful response with stop_reason
        if (response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
            IO.println("Response was truncated");
        }
    } catch (RateLimitException e) {
        // Handle actual errors
        IO.println("Rate limit exceeded");
    } catch (AnthropicServiceException e) {
        if (e.statusCode() == 500) {
            IO.println("Server error");
        }
    }
}
```

```php PHP hidelines={1..6}
<?php

use Anthropic\Client;
use Anthropic\Core\Exceptions\InternalServerException;
use Anthropic\Core\Exceptions\RateLimitException;

$client = new Client();

try {
    $response = $client->messages->create(
        maxTokens: 1024,
        messages: [['role' => 'user', 'content' => 'Hello!']],
        model: 'claude-opus-4-8',
    );

    // Tangani respons yang berhasil dengan stop_reason
    if ($response->stopReason === 'max_tokens') {
        echo 'Response was truncated', PHP_EOL;
    }
} catch (RateLimitException $e) {
    // Tangani error yang sebenarnya
    echo 'Rate limit exceeded', PHP_EOL;
} catch (InternalServerException $e) {
    echo 'Server error', PHP_EOL;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

begin
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  )

  # Tangani respons yang berhasil dengan stop_reason
  if response.stop_reason == :max_tokens
    puts "Response was truncated"
  end
rescue Anthropic::Errors::RateLimitError
  # Tangani error yang sebenarnya
  puts "Rate limit exceeded"
rescue Anthropic::Errors::APIStatusError => e
  puts "Server error" if e.status == 500
end
```
</CodeGroup>

## Pertimbangan streaming \{#streaming-considerations}

Saat menggunakan streaming, `stop_reason` adalah:
- `null` dalam event `message_start` awal
- Disediakan dalam event `message_delta`
- Tidak disediakan dalam event lainnya

<CodeGroup>
```bash cURL
# Event message_delta dalam stream SSE membawa stop_reason.
curl --no-buffer https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "stream": true,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

```bash CLI
# stop_reason muncul dalam event message_delta.
ant messages create --stream --format jsonl \
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello!"}' |
  jq -c 'select(.type == "message_delta") | .delta.stop_reason'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
) as stream:
    for event in stream:
        if event.type == "message_delta":
            stop_reason = event.delta.stop_reason
            if stop_reason:
                print(f"Stream ended with: {stop_reason}")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
});

for await (const event of stream) {
  if (event.type === "message_delta" && event.delta.stop_reason) {
    console.log(`Stream ended with: ${event.delta.stop_reason}`);
  }
}
```

```csharp C# hidelines={1..4}
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello!" }]
};

await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
{
    switch (streamEvent.Value)
    {
        case RawMessageDeltaEvent deltaEvent when deltaEvent.Delta.StopReason is not null:
            Console.WriteLine($"Stream ended with: {deltaEvent.Delta.StopReason}");
            break;
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

	stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
		},
	})

	// Akumulasikan event ke dalam Message akhir, yang membawa stop_reason.
	message := anthropic.Message{}
	for stream.Next() {
		if err := message.Accumulate(stream.Current()); err != nil {
			log.Fatal(err)
		}
	}
	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}

	if message.StopReason != "" {
		fmt.Printf("Stream ended with: %s\n", message.StopReason)
	}
}
```

```java Java hidelines={1..9,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.http.StreamResponse;
import com.anthropic.helpers.MessageAccumulator;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.RawMessageStreamEvent;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("Hello!")
        .build();

    // Akumulasikan event menjadi Message final, yang membawa stop_reason.
    MessageAccumulator accumulator = MessageAccumulator.create();
    try (StreamResponse<RawMessageStreamEvent> streamResponse =
            client.messages().createStreaming(params)) {
        streamResponse.stream().forEach(accumulator::accumulate);
    }

    accumulator.message().stopReason().ifPresent(stopReason ->
        IO.println("Stream ended with: " + stopReason)
    );
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\RawMessageDeltaEvent;

$client = new Client();

$stream = $client->messages->createStream(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello!']],
    model: 'claude-opus-4-8',
);

foreach ($stream as $event) {
    if ($event instanceof RawMessageDeltaEvent && $event->delta->stopReason !== null) {
        echo "Stream ended with: {$event->delta->stopReason}", PHP_EOL;
    }
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

stream = client.messages.stream(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }]
)

stream.each do |event|
  next unless event.type == :message_delta
  stop_reason = event.delta.stop_reason
  puts "Stream ended with: #{stop_reason}" if stop_reason
end
```
</CodeGroup>

## Pola umum \{#common-patterns}

### Menangani alur kerja penggunaan alat \{#handling-tool-use-workflows}

<Tip>
**Lebih sederhana dengan tool runner:** Contoh berikut menunjukkan penanganan alat secara manual. Untuk sebagian besar kasus penggunaan, [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) secara otomatis menangani eksekusi alat dengan kode yang jauh lebih sedikit.
</Tip>

<CodeGroup>

```python Python nocheck
def complete_tool_workflow(client, user_query, tools):
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-8", max_tokens=1024, messages=messages, tools=tools
        )

        if response.stop_reason == "tool_use":
            # Jalankan alat dan lanjutkan
            tool_results = execute_tools(response.content)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Respons akhir
            return response
```

```typescript TypeScript nocheck
async function completeToolWorkflow(
  client: Anthropic,
  userQuery: string,
  tools: Anthropic.ToolUnion[]
): Promise<Anthropic.Message> {
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: userQuery }];

  while (true) {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages,
      tools
    });

    if (response.stop_reason === "tool_use") {
      // Jalankan alat dan lanjutkan
      const toolResults = executeTools(response.content);
      messages.push({ role: "assistant", content: response.content });
      messages.push({ role: "user", content: toolResults });
    } else {
      // Respons akhir
      return response;
    }
  }
}
```

```csharp C# nocheck
static async Task<Message> CompleteToolWorkflow(
    AnthropicClient client,
    string userQuery,
    List<ToolUnion> tools)
{
    List<MessageParam> messages = [new() { Role = Role.User, Content = userQuery }];

    while (true)
    {
        var response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1024,
            Messages = messages,
            Tools = tools
        });

        if (response.StopReason == "tool_use")
        {
            // Jalankan alat dan lanjutkan
            var toolResults = ExecuteTools(response.Content);
            messages.Add(new()
            {
                Role = Role.Assistant,
                Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
            });
            messages.Add(new() { Role = Role.User, Content = toolResults });
        }
        else
        {
            // Respons akhir
            return response;
        }
    }
}
```

```go Go nocheck hidelines={1..2}
package main

func completeToolWorkflow(
	client anthropic.Client,
	userQuery string,
	tools []anthropic.ToolUnionParam,
) (*anthropic.Message, error) {
	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery))}

	for {
		response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 1024,
			Messages:  messages,
			Tools:     tools,
		})
		if err != nil {
			return nil, err
		}

		if response.StopReason != "tool_use" {
			// Respons akhir
			return response, nil
		}

		// Jalankan alat dan lanjutkan
		toolResults := executeTools(response.Content)
		var contentParams []anthropic.ContentBlockParamUnion
		for _, block := range response.Content {
			contentParams = append(contentParams, block.ToParam())
		}
		messages = append(messages, anthropic.NewAssistantMessage(contentParams...))
		messages = append(messages, anthropic.NewUserMessage(toolResults...))
	}
}
```

```java Java nocheck
static Message completeToolWorkflow(
    AnthropicClient client,
    String userQuery,
    List<Tool> tools
) {
    List<MessageParam> messages = new ArrayList<>();
    messages.add(MessageParam.builder().role(MessageParam.Role.USER).content(userQuery).build());

    while (true) {
        MessageCreateParams.Builder params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .messages(messages);
        tools.forEach(params::addTool);

        Message response = client.messages().create(params.build());

        if (!response.stopReason().map(StopReason.TOOL_USE::equals).orElse(false)) {
            // Final response
            return response;
        }

        // Execute tools and continue
        List<ToolResultBlockParam> toolResults = executeTools(response.content());
        messages.add(response.toParam());
        messages.add(MessageParam.builder()
            .role(MessageParam.Role.USER)
            .contentOfBlockParams(toolResults.stream().map(ContentBlockParam::ofToolResult).toList())
            .build());
    }
}
```

```php PHP nocheck
function complete_tool_workflow(Client $client, string $userQuery, array $tools)
{
    $messages = [['role' => 'user', 'content' => $userQuery]];

    while (true) {
        $response = $client->messages->create(
            maxTokens: 1024,
            messages: $messages,
            model: 'claude-opus-4-8',
            tools: $tools,
        );

        if ($response->stopReason !== 'tool_use') {
            // Respons akhir
            return $response;
        }

        // Jalankan alat dan lanjutkan
        $toolResults = execute_tools($response->content);
        $messages[] = ['role' => 'assistant', 'content' => $response->content];
        $messages[] = ['role' => 'user', 'content' => $toolResults];
    }
}
```

```ruby Ruby nocheck
def complete_tool_workflow(client, user_query, tools)
  messages = [{ role: "user", content: user_query }]

  loop do
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages,
      tools: tools
    )

    # Respons akhir
    return response unless response.stop_reason == :tool_use

    # Jalankan alat dan lanjutkan
    tool_results = execute_tools(response.content)
    messages << { role: "assistant", content: response.content }
    messages << { role: "user", content: tool_results }
  end
end
```
</CodeGroup>

### Memastikan respons lengkap \{#ensuring-complete-responses}

<CodeGroup>

```python Python nocheck
def get_complete_response(client, prompt, max_attempts=3):
    messages = [{"role": "user", "content": prompt}]
    full_response = ""

    for _ in range(max_attempts):
        response = client.messages.create(
            model="claude-opus-4-8", messages=messages, max_tokens=4096
        )

        full_response += response.content[0].text

        if response.stop_reason != "max_tokens":
            break

        # Lanjutkan dari titik terakhir berhenti
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_response},
            {"role": "user", "content": "Please continue from where you left off."},
        ]

    return full_response
```

```typescript TypeScript nocheck
async function getCompleteResponse(
  client: Anthropic,
  prompt: string,
  maxAttempts = 3
): Promise<string> {
  let messages: Anthropic.MessageParam[] = [{ role: "user", content: prompt }];
  let fullResponse = "";

  for (let i = 0; i < maxAttempts; i++) {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages
    });

    const block = response.content[0];
    fullResponse += block.type === "text" ? block.text : "";

    if (response.stop_reason !== "max_tokens") {
      break;
    }

    // Lanjutkan dari titik terakhir berhenti
    messages = [
      { role: "user", content: prompt },
      { role: "assistant", content: fullResponse },
      { role: "user", content: "Please continue from where you left off." }
    ];
  }

  return fullResponse;
}
```

```csharp C# nocheck
static async Task<string> GetCompleteResponse(AnthropicClient client, string prompt, int maxAttempts = 3)
{
    List<MessageParam> messages = [new() { Role = Role.User, Content = prompt }];
    var fullResponse = "";

    for (var i = 0; i < maxAttempts; i++)
    {
        var response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 4096,
            Messages = messages
        });

        if (response.Content[0].TryPickText(out var textBlock))
        {
            fullResponse += textBlock.Text;
        }

        if (response.StopReason != "max_tokens")
        {
            break;
        }

        // Lanjutkan dari titik terakhir berhenti
        messages =
        [
            new() { Role = Role.User, Content = prompt },
            new() { Role = Role.Assistant, Content = fullResponse },
            new() { Role = Role.User, Content = "Please continue from where you left off." }
        ];
    }

    return fullResponse;
}
```

```go Go nocheck hidelines={1..2}
package main

func getCompleteResponse(client anthropic.Client, prompt string, maxAttempts int) (string, error) {
	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(prompt))}
	fullResponse := ""

	for range maxAttempts {
		response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 4096,
			Messages:  messages,
		})
		if err != nil {
			return "", err
		}

		if block, ok := response.Content[0].AsAny().(anthropic.TextBlock); ok {
			fullResponse += block.Text
		}

		if response.StopReason != "max_tokens" {
			break
		}

		// Lanjutkan dari titik terakhir berhenti
		messages = []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock(prompt)),
			anthropic.NewAssistantMessage(anthropic.NewTextBlock(fullResponse)),
			anthropic.NewUserMessage(anthropic.NewTextBlock("Please continue from where you left off.")),
		}
	}

	return fullResponse, nil
}
```

```java Java nocheck
static String getCompleteResponse(AnthropicClient client, String prompt, int maxAttempts) {
    List<MessageParam> messages = List.of(
        MessageParam.builder().role(MessageParam.Role.USER).content(prompt).build()
    );
    StringBuilder fullResponse = new StringBuilder();

    for (int i = 0; i < maxAttempts; i++) {
        Message response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(4096L)
                .messages(messages)
                .build()
        );

        response.content().get(0).text().ifPresent(block -> fullResponse.append(block.text()));

        if (!response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
            break;
        }

        // Lanjutkan dari titik terakhir berhenti
        messages = List.of(
            MessageParam.builder().role(MessageParam.Role.USER).content(prompt).build(),
            MessageParam.builder().role(MessageParam.Role.ASSISTANT).content(fullResponse.toString()).build(),
            MessageParam.builder().role(MessageParam.Role.USER).content("Please continue from where you left off.").build()
        );
    }

    return fullResponse.toString();
}
```

```php PHP nocheck
function get_complete_response(Client $client, string $prompt, int $maxAttempts = 3): string
{
    $messages = [['role' => 'user', 'content' => $prompt]];
    $fullResponse = '';

    for ($i = 0; $i < $maxAttempts; $i++) {
        $response = $client->messages->create(
            maxTokens: 4096,
            messages: $messages,
            model: 'claude-opus-4-8',
        );

        $fullResponse .= $response->content[0]->text;

        if ($response->stopReason !== 'max_tokens') {
            break;
        }

        // Lanjutkan dari titik terakhir berhenti
        $messages = [
            ['role' => 'user', 'content' => $prompt],
            ['role' => 'assistant', 'content' => $fullResponse],
            ['role' => 'user', 'content' => 'Please continue from where you left off.'],
        ];
    }

    return $fullResponse;
}
```

```ruby Ruby nocheck
def get_complete_response(client, prompt, max_attempts: 3)
  messages = [{ role: "user", content: prompt }]
  full_response = +""

  max_attempts.times do
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages
    )

    full_response << response.content.first.text

    break unless response.stop_reason == :max_tokens

    # Lanjutkan dari titik terakhir berhenti
    messages = [
      { role: "user", content: prompt },
      { role: "assistant", content: full_response },
      { role: "user", content: "Please continue from where you left off." }
    ]
  end

  full_response
end
```
</CodeGroup>

### Mendapatkan token maksimum tanpa mengetahui ukuran input \{#getting-maximum-tokens-without-knowing-input-size}

Dengan stop reason `model_context_window_exceeded`, Anda dapat meminta token maksimum yang mungkin tanpa menghitung ukuran input:

<CodeGroup>

```python Python nocheck
def get_max_possible_tokens(client, prompt):
    """
    Get as many tokens as possible within the model's context window
    without needing to calculate input token count
    """
    response = client.beta.messages.create(
        model="claude-opus-4-8",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k
    )

    if response.stop_reason == "model_context_window_exceeded":
        # Mendapatkan token maksimum yang mungkin berdasarkan ukuran input
        print(
            f"Generated {response.usage.output_tokens} tokens (context limit reached)"
        )
    elif response.stop_reason == "max_tokens":
        # Mendapatkan persis jumlah token yang diminta
        print(f"Generated {response.usage.output_tokens} tokens (max_tokens reached)")
    else:
        # Penyelesaian alami
        print(f"Generated {response.usage.output_tokens} tokens (natural completion)")

    return response.content[0].text
```

```typescript TypeScript nocheck
async function getMaxPossibleTokens(client: Anthropic, prompt: string): Promise<string> {
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 20000,
    messages: [{ role: "user", content: prompt }]
  });

  const tokens = response.usage.output_tokens;
  if (response.stop_reason === "model_context_window_exceeded") {
    // Mendapatkan token maksimum yang mungkin berdasarkan ukuran input
    console.log(`Generated ${tokens} tokens (context limit reached)`);
  } else if (response.stop_reason === "max_tokens") {
    // Mendapatkan persis jumlah token yang diminta
    console.log(`Generated ${tokens} tokens (max_tokens reached)`);
  } else {
    // Penyelesaian alami
    console.log(`Generated ${tokens} tokens (natural completion)`);
  }

  const block = response.content[0];
  return block.type === "text" ? block.text : "";
}
```

```csharp C# nocheck
using Anthropic.Models.Beta.Messages;
using Model = Anthropic.Models.Messages.Model;

static async Task<string> GetMaxPossibleTokens(AnthropicClient client, string prompt)
{
    var response = await client.Beta.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 20000,
        Messages = [new() { Role = Role.User, Content = prompt }]
    });

    var tokens = response.Usage.OutputTokens;
    var reason = response.StopReason?.Value();
    if (reason == BetaStopReason.ModelContextWindowExceeded)
    {
        // Mendapatkan token maksimum yang mungkin berdasarkan ukuran input
        Console.WriteLine($"Generated {tokens} tokens (context limit reached)");
    }
    else if (reason == BetaStopReason.MaxTokens)
    {
        // Mendapatkan persis jumlah token yang diminta
        Console.WriteLine($"Generated {tokens} tokens (max_tokens reached)");
    }
    else
    {
        // Penyelesaian alami
        Console.WriteLine($"Generated {tokens} tokens (natural completion)");
    }

    return response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "";
}
```

```go Go nocheck hidelines={1..2}
package main

func getMaxPossibleTokens(client anthropic.Client, prompt string) (string, error) {
	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 20000,
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(prompt)),
		},
	})
	if err != nil {
		return "", err
	}

	tokens := response.Usage.OutputTokens
	switch response.StopReason {
	case anthropic.BetaStopReasonModelContextWindowExceeded:
		// Mendapatkan token maksimum yang mungkin berdasarkan ukuran input
		fmt.Printf("Generated %d tokens (context limit reached)\n", tokens)
	case anthropic.BetaStopReasonMaxTokens:
		// Mendapatkan persis jumlah token yang diminta
		fmt.Printf("Generated %d tokens (max_tokens reached)\n", tokens)
	default:
		// Penyelesaian alami
		fmt.Printf("Generated %d tokens (natural completion)\n", tokens)
	}

	if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
		return block.Text, nil
	}
	return "", nil
}
```

```java Java nocheck
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaStopReason;
import com.anthropic.models.beta.messages.BetaTextBlock;
import com.anthropic.models.beta.messages.MessageCreateParams;

static String getMaxPossibleTokens(AnthropicClient client, String prompt) {
    BetaMessage response = client.beta().messages().create(
        MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(20000L)
            .addUserMessage(prompt)
            .build()
    );

    long tokens = response.usage().outputTokens();
    BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);
    if (reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
        // Mendapat token maksimum yang mungkin berdasarkan ukuran input
        IO.println("Generated " + tokens + " tokens (context limit reached)");
    } else if (reason.equals(BetaStopReason.MAX_TOKENS)) {
        // Mendapat persis jumlah token yang diminta
        IO.println("Generated " + tokens + " tokens (max_tokens reached)");
    } else {
        // Penyelesaian alami
        IO.println("Generated " + tokens + " tokens (natural completion)");
    }

    return response.content().get(0).text().map(BetaTextBlock::text).orElse("");
}
```

```php PHP nocheck
function get_max_possible_tokens(Client $client, string $prompt): string
{
    $response = $client->beta->messages->create(
        maxTokens: 20000,
        messages: [['role' => 'user', 'content' => $prompt]],
        model: 'claude-opus-4-8',
    );

    $tokens = $response->usage->outputTokens;
    echo match ($response->stopReason) {
        // Mendapat token maksimum yang mungkin berdasarkan ukuran input
        'model_context_window_exceeded' => "Generated {$tokens} tokens (context limit reached)",
        // Mendapat persis jumlah token yang diminta
        'max_tokens' => "Generated {$tokens} tokens (max_tokens reached)",
        // Penyelesaian alami
        default => "Generated {$tokens} tokens (natural completion)",
    }, PHP_EOL;

    return $response->content[0]->text;
}
```

```ruby Ruby nocheck
def get_max_possible_tokens(client, prompt)
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 20000,
    messages: [{ role: "user", content: prompt }]
  )

  tokens = response.usage.output_tokens
  case response.stop_reason
  when :model_context_window_exceeded
    # Mendapatkan token maksimum yang mungkin berdasarkan ukuran input
    puts "Generated #{tokens} tokens (context limit reached)"
  when :max_tokens
    # Mendapatkan persis jumlah token yang diminta
    puts "Generated #{tokens} tokens (max_tokens reached)"
  else
    # Penyelesaian alami
    puts "Generated #{tokens} tokens (natural completion)"
  end

  response.content.first.text
end
```
</CodeGroup>

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Penolakan dan fallback" icon="arrows-clockwise" href="/docs/id/build-with-claude/refusals-and-fallback">
    Coba ulang permintaan yang ditolak pada model fallback, di sisi server atau di klien Anda.
  </Card>
  <Card title="Tool Runner (SDK)" icon="wrench" href="/docs/id/agents-and-tools/tool-use/tool-runner">
    Biarkan SDK mengelola loop `tool_use`, pemformatan hasil, dan percobaan ulang untuk Anda.
  </Card>
  <Card title="Streaming pesan" icon="lightning" href="/docs/id/build-with-claude/streaming">
    Baca `stop_reason` dari event `message_delta` saat streaming.
  </Card>
  <Card title="Error" icon="info" href="/docs/id/api/errors">
    Tangani error HTTP 4xx dan 5xx, yang berbeda dari stop reason.
  </Card>
</CardGroup>