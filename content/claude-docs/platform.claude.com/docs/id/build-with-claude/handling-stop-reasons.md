---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 930f5d8dfc1bc40085eb591eb6a47a8f18f4d01e768483e8a99cd0b91956dc62
---

# Stop reason dan fallback

Field stop_reason, arti setiap nilainya, dan di mana menangani penolakan dan fallback.

---

Saat Anda membuat permintaan ke Messages API, respons Claude menyertakan field `stop_reason` yang menunjukkan mengapa model berhenti menghasilkan responsnya. Memahami nilai-nilai ini sangat penting untuk membangun aplikasi yang tangguh yang menangani berbagai jenis respons dengan tepat.

Untuk detail tentang `stop_reason` dalam respons API, lihat [referensi Messages API](/docs/id/api/messages/create).

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
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

## Nilai stop reason \{#stop-reason-values}

### end_turn \{#end-turn}
Stop reason yang paling umum. Menunjukkan bahwa Claude menyelesaikan responsnya secara alami.

```python Python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
if response.stop_reason == "end_turn":
    # Proses respons lengkap
    print(response.content[0].text)
```

#### Respons kosong dengan end_turn \{#empty-responses-with-end-turn}

Terkadang Claude mengembalikan respons kosong (tepat 2-3 token tanpa konten) dengan `stop_reason: "end_turn"`. Ini biasanya terjadi ketika Claude menafsirkan bahwa giliran asisten sudah selesai, terutama setelah hasil alat.

**Penyebab umum:**
- Menambahkan blok teks langsung setelah hasil alat (Claude belajar untuk mengharapkan pengguna selalu menyisipkan teks setelah hasil alat, sehingga Claude mengakhiri gilirannya untuk mengikuti pola tersebut)
- Mengirim kembali respons Claude yang sudah selesai tanpa menambahkan apa pun (Claude sudah memutuskan bahwa ia selesai, jadi ia akan tetap selesai)

**Cara mencegah respons kosong:**

```python nocheck
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


# Jika Anda masih mendapatkan respons kosong setelah memperbaiki struktur pesan:
def handle_empty_response(client, messages):
    response = client.messages.create(
        model="claude-opus-4-8", max_tokens=1024, messages=messages
    )

    # Periksa apakah respons kosong
    if response.stop_reason == "end_turn" and not response.content:
        # SALAH: Jangan hanya mencoba ulang dengan respons kosong tersebut
        # Ini tidak akan berhasil karena Claude sudah memutuskan bahwa ia selesai

        # BENAR: Tambahkan prompt lanjutan dalam pesan user yang BARU
        messages.append({"role": "user", "content": "Please continue"})

        response = client.messages.create(
            model="claude-opus-4-8", max_tokens=1024, messages=messages
        )

    return response
```

**Praktik terbaik:**
1. **Jangan pernah menambahkan blok teks langsung setelah hasil alat** - Ini mengajarkan Claude untuk mengharapkan input pengguna setelah setiap penggunaan alat
2. **Jangan mencoba ulang respons kosong tanpa modifikasi** - Sekadar mengirim kembali respons kosong tidak akan membantu
3. **Gunakan prompt lanjutan sebagai upaya terakhir** - Hanya jika perbaikan di atas tidak menyelesaikan masalah

### max_tokens \{#max-tokens}
Claude berhenti karena mencapai batas `max_tokens` yang ditentukan dalam permintaan Anda.

```python Python
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

#### Blok tool use yang tidak lengkap \{#incomplete-tool-use-blocks}

Jika respons Claude terpotong karena mencapai batas `max_tokens`, dan respons yang terpotong tersebut berisi blok tool use yang tidak lengkap, Anda perlu mencoba ulang permintaan dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan tool use yang lengkap.

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

```python Python nocheck hidelines={1..8}
import anthropic

client = anthropic.Anthropic()
tools: list[dict] = []
messages: list[dict] = []
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
    if (lastBlock.Type == "tool_use")
    {
        parameters.MaxTokens = 4096;
        response = await client.Messages.Create(parameters);
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

### stop_sequence \{#stop-sequence}
Claude menemukan salah satu stop sequence kustom Anda.

```python Python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")
```

### tool_use \{#tool-use}
Claude memanggil sebuah alat dan mengharapkan Anda untuk mengeksekusinya.

<Note>
Untuk sebagian besar implementasi penggunaan alat, gunakan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner), yang secara otomatis menangani eksekusi alat, pemformatan hasil, dan manajemen percakapan.
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
    # Ekstrak dan jalankan alat
    for content in response.content:
        if content.type == "tool_use":
            result = execute_tool(content.name, content.input)
            # Kembalikan hasil ke Claude untuk respons akhir
```

### pause_turn \{#pause-turn}
Dikembalikan ketika loop sampling sisi server mencapai batas iterasinya saat mengeksekusi [server tools](/docs/id/agents-and-tools/tool-use/server-tools) seperti web search atau web fetch. Batas default adalah 10 iterasi per permintaan.

Ketika ini terjadi, respons mungkin berisi blok `server_tool_use` tanpa `server_tool_result` yang sesuai. Untuk membiarkan Claude menyelesaikan pemrosesan, lanjutkan percakapan dengan mengirim kembali respons apa adanya.

```python Python nocheck
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Search for latest AI news"}],
)

if response.stop_reason == "pause_turn":
    # Lanjutkan percakapan dengan mengirim kembali respons tersebut
    messages = [
        {"role": "user", "content": original_query},
        {"role": "assistant", "content": response.content},
    ]
    continuation = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
```

<Note>
Aplikasi Anda harus menangani `pause_turn` dalam setiap loop agen yang menggunakan server tools. Cukup tambahkan respons asisten ke array messages Anda dan buat permintaan API lain untuk membiarkan Claude melanjutkan.
</Note>

### refusal \{#refusal}
Claude menolak untuk menghasilkan respons. Pada Claude Fable 5, pengklasifikasi keamanan mengembalikan stop reason ini sebagai respons HTTP 200 normal, bukan error.

```python Python
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

<Tip>
Jika Anda sering menemukan stop reason `refusal` saat menggunakan Claude Sonnet 4.5 atau Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)), Anda dapat mencoba memperbarui panggilan API Anda untuk menggunakan Haiku 4.5 (`claude-haiku-4-5-20251001`), yang memiliki batasan penggunaan yang berbeda. Pelajari lebih lanjut tentang [memahami filter keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

Pada penolakan, objek `stop_details` mengidentifikasi kategori kebijakan yang memicunya. Kategori-kategori tersebut dan bentuk lengkap respons penolakan dibahas di [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response). `stop_details` bernilai `null` untuk semua stop reason selain `refusal`.

Permintaan yang ditolak pada Claude Fable 5 biasanya dapat dilayani dengan mencoba ulang pada model Claude lain, dan [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) menunjukkan cara menyiapkan percobaan ulang tersebut, baik di sisi server maupun di klien Anda. [Kredit fallback](/docs/id/build-with-claude/fallback-credit) membahas cara menghindari pembayaran biaya cache prompt dua kali ketika Anda membangun percobaan ulang sendiri.

### model_context_window_exceeded \{#model-context-window-exceeded}
Claude berhenti karena mencapai batas jendela konteks model. Ini memungkinkan Anda meminta token maksimum yang mungkin tanpa mengetahui ukuran input yang tepat.

```python Python nocheck
# Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
response = client.messages.create(
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

<Note>
Stop reason ini tersedia secara default di Sonnet 4.5 dan model yang lebih baru. Untuk model sebelumnya, gunakan beta header `model-context-window-exceeded-2025-08-26` untuk mengaktifkan perilaku ini.
</Note>

## Praktik terbaik untuk menangani stop reason \{#best-practices-for-handling-stop-reasons}

### 1. Selalu periksa stop_reason \{#1-always-check-stop-reason}

Biasakan untuk memeriksa `stop_reason` dalam logika penanganan respons Anda:

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
        # Tangani end_turn dan kasus lainnya
        return response.content[0].text
```

### 2. Tangani respons yang terpotong dengan baik \{#2-handle-truncated-responses-gracefully}

Ketika respons terpotong karena batas token atau jendela konteks:

```python nocheck
def handle_truncated_response(response):
    if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
        # Opsi 1: Peringatkan pengguna tentang batas spesifik tersebut
        if response.stop_reason == "max_tokens":
            message = "[Response truncated due to max_tokens limit]"
        else:
            message = "[Response truncated due to context window limit]"
        return f"{response.content[0].text}\n\n{message}"

        # Opsi 2: Lanjutkan proses generasi
        messages = [
            {"role": "user", "content": original_prompt},
            {"role": "assistant", "content": response.content[0].text},
        ]
        continuation = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            messages=messages + [{"role": "user", "content": "Please continue"}],
        )
        return response.content[0].text + continuation.content[0].text
```

### 3. Terapkan logika percobaan ulang untuk pause_turn \{#3-implement-retry-logic-for-pause-turn}

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
            model="claude-opus-4-8", max_tokens=1024, messages=messages, tools=tools
        )

        if response.stop_reason != "pause_turn":
            # Claude selesai memproses - kembalikan respons akhir
            return response

        # pause_turn: ganti seluruh daftar pesan untuk mempertahankan peran yang bergantian
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.content},
        ]

    # Mencapai batas maksimum kelanjutan - kembalikan respons terakhir
    return response
```

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

## Pertimbangan streaming \{#streaming-considerations}

Saat menggunakan streaming, `stop_reason` adalah:
- `null` dalam event `message_start` awal
- Disediakan dalam event `message_delta`
- Tidak disediakan dalam event lainnya

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

## Pola umum \{#common-patterns}

### Menangani alur kerja penggunaan alat \{#handling-tool-use-workflows}

<Tip>
**Lebih sederhana dengan tool runner:** Contoh berikut menunjukkan penanganan alat secara manual. Untuk sebagian besar kasus penggunaan, [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) secara otomatis menangani eksekusi alat dengan kode yang jauh lebih sedikit.
</Tip>

```python nocheck
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

### Memastikan respons yang lengkap \{#ensuring-complete-responses}

```python nocheck
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

### Mendapatkan token maksimum tanpa mengetahui ukuran input \{#getting-maximum-tokens-without-knowing-input-size}

Dengan stop reason `model_context_window_exceeded`, Anda dapat meminta token maksimum yang mungkin tanpa menghitung ukuran input:

```python
def get_max_possible_tokens(client, prompt):
    """
    Get as many tokens as possible within the model's context window
    without needing to calculate input token count
    """
    response = client.messages.create(
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

Dengan menangani nilai `stop_reason` dengan benar, Anda dapat membangun aplikasi yang lebih tangguh yang menangani berbagai skenario respons dengan baik dan memberikan pengalaman pengguna yang lebih baik.