---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 622f9ec63ff994320003efe17b44fa68e31c43c1c0fe7d8e6c91de873777667e
---

# Menangani stop reason

Pelajari cara menangani nilai stop_reason yang berbeda dalam respons Messages API Claude, termasuk end_turn, max_tokens, tool_use, pause_turn, dan refusal.

---

Saat Anda membuat permintaan ke Messages API, respons Claude menyertakan field `stop_reason` yang menunjukkan mengapa model berhenti menghasilkan responsnya. Memahami nilai-nilai ini sangat penting untuk membangun aplikasi yang andal yang menangani berbagai jenis respons dengan tepat.

Untuk detail tentang `stop_reason` dalam respons API, lihat [referensi Messages API](/docs/id/api/messages/create).

## Field stop_reason

Field `stop_reason` adalah bagian dari setiap respons Messages API yang berhasil. Tidak seperti error, yang menunjukkan kegagalan dalam memproses permintaan Anda, `stop_reason` memberi tahu Anda mengapa Claude berhasil menyelesaikan pembuatan responsnya.

```json Contoh respons
{
  "id": "msg_01234",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Berikut jawaban atas pertanyaan Anda..."
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

## Nilai stop reason

### end_turn
Stop reason yang paling umum. Menunjukkan Claude menyelesaikan responsnya secara alami.

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

#### Respons kosong dengan end_turn

Terkadang Claude mengembalikan respons kosong (tepat 2-3 token tanpa konten) dengan `stop_reason: "end_turn"`. Ini biasanya terjadi ketika Claude menginterpretasikan bahwa giliran asisten telah selesai, terutama setelah hasil tool.

**Penyebab umum:**
- Menambahkan blok teks segera setelah hasil tool (Claude belajar untuk mengharapkan pengguna selalu menyisipkan teks setelah hasil tool, sehingga ia mengakhiri gilirannya untuk mengikuti pola)
- Mengirim kembali respons Claude yang sudah selesai tanpa menambahkan apa pun (Claude sudah memutuskan bahwa ia selesai, sehingga ia akan tetap selesai)

**Cara mencegah respons kosong:**

```python nocheck
# SALAH: Menambahkan teks segera setelah tool_result
messages = [
    {"role": "user", "content": "Hitung jumlah 1234 dan 5678"},
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
                "text": "Berikut hasilnya",  # Jangan tambahkan teks setelah tool_result
            },
        ],
    },
]

# BENAR: Kirim hasil tool langsung tanpa teks tambahan
messages = [
    {"role": "user", "content": "Hitung jumlah 1234 dan 5678"},
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
    },  # Hanya tool_result, tanpa teks tambahan
]


# Jika Anda masih mendapatkan respons kosong setelah memperbaiki hal di atas:
def handle_empty_response(client, messages):
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=1024, messages=messages
    )

    # Periksa apakah respons kosong
    if response.stop_reason == "end_turn" and not response.content:
        # SALAH: Jangan hanya mencoba ulang dengan respons kosong
        # Ini tidak akan berhasil karena Claude sudah memutuskan bahwa ia selesai

        # BENAR: Tambahkan prompt kelanjutan dalam pesan pengguna BARU
        messages.append({"role": "user", "content": "Silakan lanjutkan"})

        response = client.messages.create(
            model="claude-opus-4-6", max_tokens=1024, messages=messages
        )

    return response
```

**Praktik terbaik:**
1. **Jangan pernah menambahkan blok teks segera setelah hasil tool** - Ini mengajarkan Claude untuk mengharapkan input pengguna setelah setiap penggunaan tool
2. **Jangan mencoba ulang respons kosong tanpa modifikasi** - Sekadar mengirim kembali respons kosong tidak akan membantu
3. **Gunakan prompt kelanjutan sebagai upaya terakhir** - Hanya jika perbaikan di atas tidak menyelesaikan masalah

### max_tokens
Claude berhenti karena mencapai batas `max_tokens` yang ditentukan dalam permintaan Anda.

```python Python
# Permintaan dengan token terbatas
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=10,
    messages=[{"role": "user", "content": "Jelaskan fisika kuantum"}],
)

if response.stop_reason == "max_tokens":
    # Respons terpotong
    print("Respons terpotong pada batas token")
    # Pertimbangkan untuk membuat permintaan lain untuk melanjutkan
```

#### Blok penggunaan tool yang tidak lengkap

Jika respons Claude terpotong karena mencapai batas `max_tokens`, dan respons yang terpotong berisi blok penggunaan tool yang tidak lengkap, Anda perlu mencoba ulang permintaan dengan nilai `max_tokens` yang lebih tinggi untuk mendapatkan penggunaan tool yang lengkap.

<CodeGroup>

```bash CLI nocheck
RESPONSE=$(ant messages create --max-tokens 1024 \
  --format jsonl < request.yaml)

# Periksa apakah respons terpotong di tengah penggunaan tool
STOP_REASON=$(jq -r '.stop_reason' <<<"$RESPONSE")
LAST_TYPE=$(jq -r '.content[-1].type' <<<"$RESPONSE")
if [ "$STOP_REASON" = "max_tokens" ] && [ "$LAST_TYPE" = "tool_use" ]; then
  # Coba ulang dengan max_tokens yang lebih tinggi
  ant messages create --max-tokens 4096 < request.yaml
fi
```

```python Python nocheck hidelines={1..8}
import anthropic

client = anthropic.Anthropic()
tools: list[dict] = []
messages: list[dict] = []
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024, tools=tools, messages=messages
)
# Periksa apakah respons terpotong selama penggunaan tool
if response.stop_reason == "max_tokens":
    # Periksa apakah blok konten terakhir adalah tool_use yang tidak lengkap
    last_block = response.content[-1]
    if last_block.type == "tool_use":
        # Kirim permintaan dengan max_tokens yang lebih tinggi
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,  # Batas yang ditingkatkan
            messages=messages,
            tools=tools,
        )
```

```typescript TypeScript nocheck
// Periksa apakah respons terpotong selama penggunaan tool
if (response.stop_reason === "max_tokens") {
  // Periksa apakah blok konten terakhir adalah tool_use yang tidak lengkap
  const lastBlock = response.content[response.content.length - 1];
  if (lastBlock.type === "tool_use") {
    // Kirim permintaan dengan max_tokens yang lebih tinggi
    response = await client.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 4096, // Batas yang ditingkatkan
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
            Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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
				Model:     anthropic.ModelClaudeOpus4_6,
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
Message response = client.messages().create(MessageCreateParams.builder().model(Model.CLAUDE_OPUS_4_6).maxTokens(1024L).addUserMessage("test").build());
// Periksa apakah respons terpotong selama penggunaan tool
if (response.stopReason().isPresent() && response.stopReason().get().equals(StopReason.MAX_TOKENS)) {
    ContentBlock lastBlock = response.content().get(response.content().size() - 1);
    if (lastBlock.toolUse().isPresent()) {
        // Kirim permintaan dengan max_tokens yang lebih tinggi
        response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_6)
                .maxTokens(4096L) // Batas yang ditingkatkan
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
    model: 'claude-opus-4-6',
    tools: $tools,
);

if ($response->stopReason === 'max_tokens') {
    $lastBlock = end($response->content);
    if ($lastBlock->type === 'tool_use') {
        $response = $client->messages->create(
            maxTokens: 4096,
            messages: $messages,
            model: 'claude-opus-4-6',
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
    description: "Dapatkan cuaca saat ini di lokasi tertentu",
    input_schema: { type: "object", properties: { location: { type: "string" } }, required: ["location"] }
  }
]
messages = [
  { role: "user", content: "Bagaimana cuaca di San Francisco?" }
]

response = client.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: messages,
  tools: tools
)

if response.stop_reason == :max_tokens
  last_block = response.content.last
  if last_block.type == :tool_use
    response = client.messages.create(
      model: "claude-opus-4-6",
      max_tokens: 4096,
      messages: messages,
      tools: tools
    )
  end
end
```
</CodeGroup>

### stop_sequence
Claude menemukan salah satu urutan stop kustom Anda.

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Buat teks hingga Anda mengatakan END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Berhenti pada urutan: {response.stop_sequence}")
```

### tool_use
Claude memanggil sebuah tool dan mengharapkan Anda untuk mengeksekusinya.

<Note>
Untuk sebagian besar implementasi penggunaan tool, kami merekomendasikan menggunakan [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) yang secara otomatis menangani eksekusi tool, pemformatan hasil, dan manajemen percakapan.
</Note>

```python Python nocheck
from anthropic import Anthropic

client = Anthropic()
weather_tool = {
    "name": "get_weather",
    "description": "Dapatkan cuaca saat ini di lokasi tertentu",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "Kota dan negara bagian"},
        },
        "required": ["location"],
    },
}


def execute_tool(name, tool_input):
    """Eksekusi sebuah tool dan kembalikan hasilnya."""
    return f"Cuaca di {tool_input.get('location', 'tidak diketahui')}: 72°F"


response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "Bagaimana cuacanya?"}],
)

if response.stop_reason == "tool_use":
    # Ekstrak dan eksekusi tool
    for content in response.content:
        if content.type == "tool_use":
            result = execute_tool(content.name, content.input)
            # Kembalikan hasil ke Claude untuk respons akhir
```

### pause_turn
Dikembalikan ketika loop sampling sisi server mencapai batas iterasinya saat mengeksekusi [server tools](/docs/id/agents-and-tools/tool-use/server-tools) seperti pencarian web atau pengambilan web. Batas default adalah 10 iterasi per permintaan.

Ketika ini terjadi, respons mungkin berisi blok `server_tool_use` tanpa `server_tool_result` yang sesuai. Untuk membiarkan Claude menyelesaikan pemrosesan, lanjutkan percakapan dengan mengirim kembali respons apa adanya.

```python Python nocheck
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Cari berita AI terbaru"}],
)

if response.stop_reason == "pause_turn":
    # Lanjutkan percakapan dengan mengirim kembali respons
    messages = [
        {"role": "user", "content": original_query},
        {"role": "assistant", "content": response.content},
    ]
    continuation = client.messages.create(
        model="claude-opus-4-6",
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
```

<Note>
Aplikasi Anda harus menangani `pause_turn` dalam loop agen mana pun yang menggunakan server tools. Cukup tambahkan respons asisten ke array pesan Anda dan buat permintaan API lain untuk membiarkan Claude melanjutkan.
</Note>

### refusal
Claude menolak untuk menghasilkan respons karena masalah keamanan.

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "[Permintaan tidak aman]"}],
)

if response.stop_reason == "refusal":
    # Claude menolak untuk merespons
    print("Claude tidak dapat memproses permintaan ini")
    # Pertimbangkan untuk memparafrasekan atau memodifikasi permintaan
```

<Tip>
Jika Anda sering menemukan stop reason `refusal` saat menggunakan Claude Sonnet 4.5 atau Opus 4.1, Anda dapat mencoba memperbarui panggilan API Anda untuk menggunakan Sonnet 4 (`claude-sonnet-4-20250514`), yang memiliki pembatasan penggunaan yang berbeda. Pelajari lebih lanjut tentang [memahami filter keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

<Note>
Untuk mempelajari lebih lanjut tentang penolakan yang dipicu oleh filter keamanan API untuk Claude Sonnet 4.5, lihat [Memahami Filter Keamanan API Sonnet 4.5](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Note>

### model_context_window_exceeded
Claude berhenti karena mencapai batas jendela konteks model. Ini memungkinkan Anda untuk meminta token maksimum yang mungkin tanpa mengetahui ukuran input yang tepat.

```python Python nocheck
# Permintaan dengan token maksimum untuk mendapatkan sebanyak mungkin
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,  # Batas non-streaming praktis (Opus 4.6 mendukung 128K dengan streaming)
    messages=[
        {"role": "user", "content": "Input besar yang menggunakan sebagian besar jendela konteks..."}
    ],
)

if response.stop_reason == "model_context_window_exceeded":
    # Respons mencapai batas jendela konteks model sebelum max_tokens
    print("Respons mencapai batas jendela konteks model")
    # Respons masih valid tetapi dibatasi oleh jendela konteks
```

<Note>
Stop reason ini tersedia secara default di Sonnet 4.5 dan model yang lebih baru. Untuk model yang lebih lama, gunakan header beta `model-context-window-exceeded-2025-08-26` untuk mengaktifkan perilaku ini.
</Note>

## Praktik terbaik untuk menangani stop reason

### 1. Selalu periksa stop_reason

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

### 2. Tangani respons yang terpotong dengan baik

Ketika respons terpotong karena batas token atau jendela konteks:

```python nocheck
def handle_truncated_response(response):
    if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
        # Opsi 1: Beri tahu pengguna tentang batas spesifik
        if response.stop_reason == "max_tokens":
            message = "[Respons terpotong karena batas max_tokens]"
        else:
            message = "[Respons terpotong karena batas jendela konteks]"
        return f"{response.content[0].text}\n\n{message}"

        # Opsi 2: Lanjutkan pembuatan
        messages = [
            {"role": "user", "content": original_prompt},
            {"role": "assistant", "content": response.content[0].text},
        ]
        continuation = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=messages + [{"role": "user", "content": "Silakan lanjutkan"}],
        )
        return response.content[0].text + continuation.content[0].text
```

### 3. Implementasikan logika percobaan ulang untuk pause_turn

Saat menggunakan [server tools](/docs/id/agents-and-tools/tool-use/server-tools), API mungkin mengembalikan `pause_turn` jika loop sampling sisi server mencapai batas iterasinya (default 10). Tangani ini dengan melanjutkan percakapan:

```python nocheck
def handle_server_tool_conversation(client, user_query, tools, max_continuations=5):
    """
    Tangani percakapan server tool yang mungkin memerlukan beberapa kelanjutan.

    Server menjalankan loop sampling saat mengeksekusi server tools. Jika loop
    mencapai batas iterasinya, API mengembalikan pause_turn. Lanjutkan
    percakapan dengan mengirim kembali respons untuk membiarkan Claude menyelesaikan.
    """
    messages = [{"role": "user", "content": user_query}]

    for _ in range(max_continuations):
        response = client.messages.create(
            model="claude-opus-4-6", messages=messages, tools=tools
        )

        if response.stop_reason != "pause_turn":
            # Claude selesai memproses - kembalikan respons akhir
            return response

        # pause_turn: ganti daftar pesan lengkap untuk mempertahankan peran bergantian
        messages = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.content},
        ]

    # Mencapai kelanjutan maksimum - kembalikan respons terakhir
    return response
```

## Stop reason vs. error

Penting untuk membedakan antara nilai `stop_reason` dan error yang sebenarnya:

### Stop reason (respons berhasil)
- Bagian dari badan respons
- Menunjukkan mengapa pembuatan berhenti secara normal
- Respons berisi konten yang valid

### Error (permintaan gagal)
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

    # Tangani respons berhasil dengan stop_reason
    if response.stop_reason == "max_tokens":
        print("Respons terpotong")

except anthropic.APIError as e:
    # Tangani error yang sebenarnya
    if e.status_code == 429:
        print("Batas rate terlampaui")
    elif e.status_code == 500:
        print("Error server")
```

## Pertimbangan streaming

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
                print(f"Stream berakhir dengan: {stop_reason}")
```

## Pola umum

### Menangani alur kerja penggunaan tool

<Tip>
**Lebih sederhana dengan tool runner**: Contoh di bawah menunjukkan penanganan tool secara manual. Untuk sebagian besar kasus penggunaan, [tool runner](/docs/id/agents-and-tools/tool-use/tool-runner) secara otomatis menangani eksekusi tool dengan kode yang jauh lebih sedikit.
</Tip>

```python nocheck
def complete_tool_workflow(client, user_query, tools):
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6", messages=messages, tools=tools
        )

        if response.stop_reason == "tool_use":
            # Eksekusi tool dan lanjutkan
            tool_results = execute_tools(response.content)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Respons akhir
            return response
```

### Memastikan respons lengkap

```python nocheck
def get_complete_response(client, prompt, max_attempts=3):
    messages = [{"role": "user", "content": prompt}]
    full_response = ""

    for _ in range(max_attempts):
        response = client.messages.create(
            model="claude-opus-4-6", messages=messages, max_tokens=4096
        )

        full_response += response.content[0].text

        if response.stop_reason != "max_tokens":
            break

        # Lanjutkan dari tempat terakhir berhenti
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_response},
            {"role": "user", "content": "Silakan lanjutkan dari tempat Anda berhenti."},
        ]

    return full_response
```

### Mendapatkan token maksimum tanpa mengetahui ukuran input

Dengan stop reason `model_context_window_exceeded`, Anda dapat meminta token maksimum yang mungkin tanpa menghitung ukuran input:

```python nocheck
def get_max_possible_tokens(client, prompt):
    """
    Dapatkan token sebanyak mungkin dalam jendela konteks model
    tanpa perlu menghitung jumlah token input
    """
    response = client.messages.create(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=64000,  # Batas non-streaming praktis (Opus 4.6 mendukung 128K dengan streaming)
    )

    if response.stop_reason == "model_context_window_exceeded":
        # Mendapatkan token maksimum yang mungkin mengingat ukuran input
        print(
            f"Menghasilkan {response.usage.output_tokens} token (batas konteks tercapai)"
        )
    elif response.stop_reason == "max_tokens":
        # Mendapatkan tepat token yang diminta
        print(f"Menghasilkan {response.usage.output_tokens} token (max_tokens tercapai)")
    else:
        # Penyelesaian alami
        print(f"Menghasilkan {response.usage.output_tokens} token (penyelesaian alami)")

    return response.content[0].text
```

Dengan menangani nilai `stop_reason` dengan benar, Anda dapat membangun aplikasi yang lebih andal yang menangani berbagai skenario respons dengan baik dan memberikan pengalaman pengguna yang lebih baik.