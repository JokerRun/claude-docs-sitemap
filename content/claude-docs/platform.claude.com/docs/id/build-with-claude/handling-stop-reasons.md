---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 56e3ea872330309874a2f96f2cdb56b084dc33633cfa84fdc2c74650b08f32ab
---

# Menangani alasan penghentian

Pelajari cara menangani nilai stop_reason dalam respons Messages API untuk membangun aplikasi yang lebih robust.

---

Ketika Anda membuat permintaan ke Messages API, respons Claude mencakup bidang `stop_reason` yang menunjukkan mengapa model berhenti menghasilkan responsnya. Memahami nilai-nilai ini sangat penting untuk membangun aplikasi yang robust yang menangani berbagai jenis respons dengan tepat.

Untuk detail tentang `stop_reason` dalam respons API, lihat [referensi Messages API](/docs/id/api/messages/create).

## Bidang stop_reason

Bidang `stop_reason` adalah bagian dari setiap respons Messages API yang berhasil. Tidak seperti kesalahan, yang menunjukkan kegagalan dalam memproses permintaan Anda, `stop_reason` memberi tahu Anda mengapa Claude berhasil menyelesaikan pembuatan responsnya.

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
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

## Nilai stop_reason

### end_turn
Alasan penghentian yang paling umum. Menunjukkan Claude menyelesaikan responsnya secara alami.

```python Python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
if response.stop_reason == "end_turn":
    # Process the complete response
    print(response.content[0].text)
```

#### Respons kosong dengan end_turn

Kadang-kadang Claude mengembalikan respons kosong (tepat 2-3 token tanpa konten) dengan `stop_reason: "end_turn"`. Ini biasanya terjadi ketika Claude menginterpretasikan bahwa giliran asisten sudah selesai, terutama setelah hasil alat.

**Penyebab umum:**
- Menambahkan blok teks segera setelah hasil alat (Claude belajar untuk mengharapkan pengguna selalu menyisipkan teks setelah hasil alat, jadi ia mengakhiri gilirannya untuk mengikuti pola)
- Mengirim kembali respons Claude yang sudah selesai tanpa menambahkan apa pun (Claude sudah memutuskan bahwa itu selesai, jadi itu akan tetap selesai)

**Cara mencegah respons kosong:**

```python nocheck
# INCORRECT: Adding text immediately after tool_result
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

# CORRECT: Send tool results directly without additional text
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


# If you still get empty responses after fixing the above:
def handle_empty_response(client, messages):
    response = client.messages.create(
        model="claude-opus-4-7", max_tokens=1024, messages=messages
    )

    # Check if response is empty
    if response.stop_reason == "end_turn" and not response.content:
        # INCORRECT: Don't just retry with the empty response
        # This won't work because Claude already decided it's done

        # CORRECT: Add a continuation prompt in a NEW user message
        messages.append({"role": "user", "content": "Please continue"})

        response = client.messages.create(
            model="claude-opus-4-7", max_tokens=1024, messages=messages
        )

    return response
```

**Praktik terbaik:**
1. **Jangan pernah menambahkan blok teks segera setelah hasil alat** - Ini mengajarkan Claude untuk mengharapkan input pengguna setelah setiap penggunaan alat
2. **Jangan coba lagi respons kosong tanpa modifikasi** - Hanya mengirim kembali respons kosong tidak akan membantu
3. **Gunakan prompt lanjutan sebagai pilihan terakhir** - Hanya jika perbaikan di atas tidak menyelesaikan masalah

### max_tokens
Claude berhenti karena mencapai batas `max_tokens` yang ditentukan dalam permintaan Anda.

```python Python
# Request with limited tokens
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum physics"}],
)

if response.stop_reason == "max_tokens":
    # Response was truncated
    print("Response was cut off at token limit")
    # Consider making another request to continue
```

#### Blok penggunaan alat yang tidak lengkap

Jika respons Claude terpotong karena mencapai batas `max_tokens`, dan respons yang terpotong berisi blok penggunaan alat yang tidak lengkap, Anda perlu mencoba ulang permintaan dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan penggunaan alat lengkap.

<CodeGroup>

```bash CLI nocheck
RESPONSE=$(ant messages create --max-tokens 1024 \
  --format jsonl < request.yaml)

# Check if the response was truncated mid tool use
STOP_REASON=$(jq -r '.stop_reason' <<<"$RESPONSE")
LAST_TYPE=$(jq -r '.content[-1].type' <<<"$RESPONSE")
if [ "$STOP_REASON" = "max_tokens" ] && [ "$LAST_TYPE" = "tool_use" ]; then
  # Retry with a higher max_tokens
  ant messages create --max-tokens 4096 < request.yaml
fi
```

```python Python nocheck hidelines={1..8}
import anthropic

client = anthropic.Anthropic()
tools: list[dict] = []
messages: list[dict] = []
response = client.messages.create(
    model="claude-opus-4-7", max_tokens=1024, tools=tools, messages=messages
)
# Check if response was truncated during tool use
if response.stop_reason == "max_tokens":
    # Check if the last content block is an incomplete tool_use
    last_block = response.content[-1]
    if last_block.type == "tool_use":
        # Send the request with higher max_tokens
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,  # Increased limit
            messages=messages,
            tools=tools,
        )
```

```typescript TypeScript nocheck
// Check if response was truncated during tool use
if (response.stop_reason === "max_tokens") {
  // Check if the last content block is an incomplete tool_use
  const lastBlock = response.content[response.content.length - 1];
  if (lastBlock.type === "tool_use") {
    // Send the request with higher max_tokens
    response = await client.messages.create({
      model: "claude-opus-4-7",
      max_tokens: 4096, // Increased limit
      messages: messages,
      tools: tools
    });
  }
}
```

```csharp C# nocheck
using System;
using System.Linq;
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
            MaxTokens = 1024,
            Messages = messages,
            Tools = tools
        };

        var response = await client.Messages.Create(parameters);

        if (response.StopReason == "max_tokens")
        {
            var lastBlock = response.Content.Last();
            if (lastBlock.Type == "tool_use")
            {
                parameters.MaxTokens = 4096;
                response = await client.Messages.Create(parameters);
            }
        }
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
				Model:     anthropic.ModelClaudeOpus4_7,
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

```java Java nocheck hidelines={1..13}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ContentBlock;
import java.util.List;
import com.anthropic.models.messages.StopReason;
AnthropicClient client = AnthropicOkHttpClient.fromEnv();
List<MessageCreateParams.Message> messages = List.of();
List<Tool> tools = List.of();
Message response = client.messages().create(MessageCreateParams.builder().model(Model.CLAUDE_OPUS_4_7).maxTokens(1024L).addUserMessage("test").build());
// Check if response was truncated during tool use
if (response.stopReason().isPresent() && response.stopReason().get().equals(StopReason.MAX_TOKENS)) {
    ContentBlock lastBlock = response.content().get(response.content().size() - 1);
    if (lastBlock.toolUse().isPresent()) {
        // Send the request with higher max_tokens
        response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_7)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->create(
    maxTokens: 1024,
    messages: $messages,
    model: 'claude-opus-4-7',
    tools: $tools,
);

if ($response->stopReason === 'max_tokens') {
    $lastBlock = end($response->content);
    if ($lastBlock->type === 'tool_use') {
        $response = $client->messages->create(
            maxTokens: 4096,
            messages: $messages,
            model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: messages,
  tools: tools
)

if response.stop_reason == :max_tokens
  last_block = response.content.last
  if last_block.type == :tool_use
    response = client.messages.create(
      model: "claude-opus-4-7",
      max_tokens: 4096,
      messages: messages,
      tools: tools
    )
  end
end
```
</CodeGroup>

### stop_sequence
Claude menemukan salah satu urutan penghentian kustom Anda.

```python Python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")
```

### tool_use
Claude memanggil alat dan mengharapkan Anda untuk menjalankannya.

<Note>
Untuk sebagian besar implementasi penggunaan alat, kami merekomendasikan menggunakan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) yang secara otomatis menangani eksekusi alat, pemformatan hasil, dan manajemen percakapan.
</Note>

```python Python nocheck
from anthropic import Anthropic

client = Anthropic()
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
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather?"}],
)

if response.stop_reason == "tool_use":
    # Extract and execute the tool
    for content in response.content:
        if content.type == "tool_use":
            result = execute_tool(content.name, content.input)
            # Return result to Claude for final response
```

### pause_turn
Dikembalikan ketika loop sampling sisi server mencapai batas iterasinya saat menjalankan [server tools](/docs/id/agents-and-tools/tool-use/server-tools) seperti pencarian web atau pengambilan web. Batas default adalah 10 iterasi per permintaan.

Ketika ini terjadi, respons mungkin berisi blok `server_tool_use` tanpa `server_tool_result` yang sesuai. Untuk membiarkan Claude menyelesaikan pemrosesan, lanjutkan percakapan dengan mengirim respons kembali apa adanya.

```python Python nocheck
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Search for latest AI news"}],
)

if response.stop_reason == "pause_turn":
    # Continue the conversation by sending the response back
    messages = [
        {"role": "user", "content": original_query},
        {"role": "assistant", "content": response.content},
    ]
    continuation = client.messages.create(
        model="claude-opus-4-7",
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
```

<Note>
Aplikasi Anda harus menangani `pause_turn` dalam loop agen apa pun yang menggunakan server tools. Cukup tambahkan respons asisten ke array pesan Anda dan buat permintaan API lain untuk membiarkan Claude melanjutkan.
</Note>

### refusal
Claude menolak untuk menghasilkan respons karena kekhawatiran keselamatan.

```python Python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "[Unsafe request]"}],
)

if response.stop_reason == "refusal":
    # Claude declined to respond
    print("Claude was unable to process this request")
    # Consider rephrasing or modifying the request
```

<Tip>
Jika Anda sering mengalami alasan penghentian `refusal` saat menggunakan Claude Sonnet 4.5 atau Opus 4.1, Anda dapat mencoba memperbarui panggilan API Anda untuk menggunakan Haiku 4.5 (`claude-haiku-4-5-20251001`), yang memiliki batasan penggunaan yang berbeda. Pelajari lebih lanjut tentang [memahami filter keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

<Note>
Untuk mempelajari lebih lanjut tentang penolakan yang dipicu oleh filter keamanan API untuk Claude Sonnet 4.5, lihat [Memahami Filter Keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Note>

### model_context_window_exceeded
Claude berhenti karena mencapai batas jendela konteks model. Ini memungkinkan Anda untuk meminta token maksimal yang mungkin tanpa mengetahui ukuran input yang tepat.

```python Python nocheck
# Request with maximum tokens to get as much as possible
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,  # Practical non-streaming ceiling (Opus 4.7 supports 128K with streaming)
    messages=[
        {"role": "user", "content": "Large input that uses most of context window..."}
    ],
)

if response.stop_reason == "model_context_window_exceeded":
    # Response hit context window limit before max_tokens
    print("Response reached model's context window limit")
    # The response is still valid but was limited by context window
```

<Note>
Alasan penghentian ini tersedia secara default di Sonnet 4.5 dan model yang lebih baru. Untuk model sebelumnya, gunakan header beta `model-context-window-exceeded-2025-08-26` untuk mengaktifkan perilaku ini.
</Note>

## Praktik terbaik untuk menangani alasan penghentian

### 1. Selalu periksa stop_reason

Jadikan kebiasaan untuk memeriksa `stop_reason` dalam logika penanganan respons Anda:

```python nocheck
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
        # Handle end_turn and other cases
        return response.content[0].text
```

### 2. Tangani respons yang terpotong dengan baik

Ketika respons terpotong karena batas token atau jendela konteks:

```python nocheck
def handle_truncated_response(response):
    if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
        # Option 1: Warn the user about the specific limit
        if response.stop_reason == "max_tokens":
            message = "[Response truncated due to max_tokens limit]"
        else:
            message = "[Response truncated due to context window limit]"
        return f"{response.content[0].text}\n\n{message}"

        # Option 2: Continue generation
        messages = [
            {"role": "user", "content": original_prompt},
            {"role": "assistant", "content": response.content[0].text},
        ]
        continuation = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            messages=messages + [{"role": "user", "content": "Please continue"}],
        )
        return response.content[0].text + continuation.content[0].text
```

### 3. Implementasikan logika percobaan ulang untuk pause_turn

Saat menggunakan [server tools](/docs/id/agents-and-tools/tool-use/server-tools), API mungkin mengembalikan `pause_turn` jika loop sampling sisi server mencapai batas iterasinya (default 10). Tangani ini dengan melanjutkan percakapan:

```python nocheck
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
            model="claude-opus-4-7", messages=messages, tools=tools
        )

        if response.stop_reason != "pause_turn":
            # Claude finished processing - return the final response
            return response

        # pause_turn: replace the full message list to maintain alternating roles
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.content},
        ]

    # Reached max continuations - return the last response
    return response
```

## Alasan penghentian vs. kesalahan

Penting untuk membedakan antara nilai `stop_reason` dan kesalahan aktual:

### Alasan penghentian (respons berhasil)
- Bagian dari badan respons
- Menunjukkan mengapa pembuatan berhenti secara normal
- Respons berisi konten yang valid

### Kesalahan (permintaan gagal)
- Kode status HTTP 4xx atau 5xx
- Menunjukkan kegagalan pemrosesan permintaan
- Respons berisi detail kesalahan

```python Python
import anthropic
from anthropic import Anthropic

client = Anthropic()

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}],
    )

    # Handle successful response with stop_reason
    if response.stop_reason == "max_tokens":
        print("Response was truncated")

except anthropic.APIError as e:
    # Handle actual errors
    if e.status_code == 429:
        print("Rate limit exceeded")
    elif e.status_code == 500:
        print("Server error")
```

## Pertimbangan streaming

Saat menggunakan streaming, `stop_reason` adalah:
- `null` dalam acara `message_start` awal
- Disediakan dalam acara `message_delta`
- Tidak disediakan dalam acara lain apa pun

```python Python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
) as stream:
    for event in stream:
        if event.type == "message_delta":
            stop_reason = event.delta.stop_reason
            if stop_reason:
                print(f"Stream ended with: {stop_reason}")
```

## Pola umum

### Menangani alur kerja penggunaan alat

<Tip>
**Lebih sederhana dengan tool runner**: Contoh di bawah menunjukkan penanganan alat manual. Untuk sebagian besar kasus penggunaan, [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) secara otomatis menangani eksekusi alat dengan jauh lebih sedikit kode.
</Tip>

```python nocheck
def complete_tool_workflow(client, user_query, tools):
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-7", messages=messages, tools=tools
        )

        if response.stop_reason == "tool_use":
            # Execute tools and continue
            tool_results = execute_tools(response.content)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Final response
            return response
```

### Memastikan respons lengkap

```python nocheck
def get_complete_response(client, prompt, max_attempts=3):
    messages = [{"role": "user", "content": prompt}]
    full_response = ""

    for _ in range(max_attempts):
        response = client.messages.create(
            model="claude-opus-4-7", messages=messages, max_tokens=4096
        )

        full_response += response.content[0].text

        if response.stop_reason != "max_tokens":
            break

        # Continue from where it left off
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_response},
            {"role": "user", "content": "Please continue from where you left off."},
        ]

    return full_response
```

### Mendapatkan token maksimal tanpa mengetahui ukuran input

Dengan alasan penghentian `model_context_window_exceeded`, Anda dapat meminta token maksimal yang mungkin tanpa menghitung jumlah token input:

```python nocheck
def get_max_possible_tokens(client, prompt):
    """
    Get as many tokens as possible within the model's context window
    without needing to calculate input token count
    """
    response = client.messages.create(
        model="claude-opus-4-7",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=64000,  # Practical non-streaming ceiling (Opus 4.7 supports 128K with streaming)
    )

    if response.stop_reason == "model_context_window_exceeded":
        # Got the maximum possible tokens given input size
        print(
            f"Generated {response.usage.output_tokens} tokens (context limit reached)"
        )
    elif response.stop_reason == "max_tokens":
        # Got exactly the requested tokens
        print(f"Generated {response.usage.output_tokens} tokens (max_tokens reached)")
    else:
        # Natural completion
        print(f"Generated {response.usage.output_tokens} tokens (natural completion)")

    return response.content[0].text
```

Dengan menangani nilai `stop_reason` dengan benar, Anda dapat membangun aplikasi yang lebih robust yang menangani skenario respons yang berbeda dengan baik dan memberikan pengalaman pengguna yang lebih baik.