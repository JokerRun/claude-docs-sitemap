---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 1a311a7ec471c397591395102481830236b34701c0bd3fe0d6e1f8fd8b7d4b52
---

# Penolakan streaming

Deteksi dan tangani stop reason penolakan dalam respons streaming, dan coba ulang permintaan yang ditolak pada model cadangan.

---

Mulai dari model Claude 4, respons streaming dari API Claude mengembalikan **`stop_reason`: `"refusal"`** ketika pengklasifikasi streaming melakukan intervensi untuk menangani potensi pelanggaran kebijakan. Fitur keamanan ini membantu menjaga kepatuhan konten selama streaming real-time.

<Tip>
Halaman ini membahas bagaimana penolakan muncul dalam respons streaming. Untuk setiap nilai `stop_reason` dan cara menanganinya, lihat [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons). Untuk mencoba ulang permintaan yang ditolak pada model Claude lain, lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback).
</Tip>

## Format respons API \{#api-response-format}

Ketika pengklasifikasi streaming mendeteksi konten yang melanggar kebijakan Anthropic, API mengembalikan respons ini:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello.."
    }
  ],
  "stop_reason": "refusal"
}
```

<Warning>
Tidak ada pesan penolakan tambahan yang disertakan. Anda harus menangani respons tersebut dan menyediakan pesan yang sesuai untuk ditampilkan kepada pengguna.
</Warning>

## Reset konteks setelah penolakan \{#reset-context-after-refusal}

Ketika Anda menerima **`stop_reason`: `refusal`**, Anda harus mereset konteks percakapan sebelum melanjutkan. Anda dapat menghapus atau menyusun ulang giliran yang memicu penolakan, atau menghapus seluruh riwayat percakapan. Mencoba melanjutkan tanpa mereset akan menghasilkan penolakan yang berkelanjutan.

<Note>
Metrik penggunaan tetap disediakan dalam respons, bahkan ketika respons ditolak.

Ketika penolakan tiba sebelum Claude menghasilkan output apa pun, Anda tidak ditagih untuk permintaan tersebut pada API Claude, dan jumlah penggunaan dalam respons tersebut hanya bersifat informasional. Ketika Claude menghasilkan output sebelum penolakan, Anda ditagih untuk permintaan tersebut.
</Note>

<Tip>
Mereset konteks bukan satu-satunya cara untuk memulihkan. Anda juga dapat mencoba ulang permintaan yang ditolak pada model Claude yang berbeda, dan halaman [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) menunjukkan cara menyiapkannya dengan fallback sisi server, middleware SDK, atau percobaan ulang manual.
</Tip>

## Panduan implementasi \{#implementation-guide}

Berikut cara mendeteksi dan menangani penolakan streaming dalam aplikasi Anda:

<CodeGroup>
```bash cURL
# Lakukan streaming permintaan dan periksa penolakan
response=$(curl -N https://api.anthropic.com/v1/messages \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --data '{
    "model": "claude-opus-4-8",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 1024,
    "stream": true
  }')

# Periksa penolakan dalam stream
if echo "$response" | grep -q '"stop_reason":"refusal"'; then
  echo "Response refused - resetting conversation context"
  # Atur ulang status percakapan Anda di sini
fi
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()
messages = []


def reset_conversation():
    """Reset conversation context after refusal"""
    global messages
    messages = []
    print("Conversation reset due to refusal")


try:
    with client.messages.stream(
        max_tokens=1024,
        messages=messages + [{"role": "user", "content": "Hello"}],
        model="claude-opus-4-8",
    ) as stream:
        for event in stream:
            # Periksa penolakan dalam delta pesan
            if event.type == "message_delta":
                if event.delta.stop_reason == "refusal":
                    reset_conversation()
                    break
except Exception as e:
    print(f"Error: {e}")
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
let messages: any[] = [];

function resetConversation() {
  // Reset konteks percakapan setelah penolakan
  messages = [];
  console.log("Conversation reset due to refusal");
}

try {
  const stream = await client.messages.stream({
    messages: [...messages, { role: "user", content: "Hello" }],
    model: "claude-opus-4-8",
    max_tokens: 1024
  });

  for await (const event of stream) {
    // Periksa penolakan di delta pesan
    if (event.type === "message_delta" && event.delta.stop_reason === "refusal") {
      resetConversation();
      break;
    }
  }
} catch (error) {
  console.error("Error:", error);
}
```

```csharp C# nocheck
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    private static List<Message> messages = new();

    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1024,
            Messages = [new() { Role = Role.User, Content = "Hello" }]
        };

        try
        {
            await foreach (var msg in client.Messages.CreateStreaming(parameters))
            {
                if (msg.Type == "message_delta" && msg.Delta?.StopReason == "refusal")
                {
                    ResetConversation();
                    break;
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error: {e.Message}");
        }
    }

    private static void ResetConversation()
    {
        messages.Clear();
        Console.WriteLine("Conversation reset due to refusal");
    }
}
```

```go Go nocheck hidelines={1..10,17..18,-1..}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

var messages []anthropic.MessageParam

func resetConversation() {
	messages = []anthropic.MessageParam{}
	fmt.Println("Conversation reset due to refusal")
}

func main() {
	client := anthropic.NewClient()

	stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
		},
	})

streamLoop:
	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.MessageDeltaEvent:
			if eventVariant.Delta.StopReason == "refusal" {
				resetConversation()
				break streamLoop
			}
		}
	}

	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..5,9..10}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.MessageParam;
import com.anthropic.models.messages.Model;
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;
import com.anthropic.models.messages.StopReason;
import java.util.ArrayList;
import java.util.List;

List<MessageParam> messages = new ArrayList<>();

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("Hello")
        .build();

    try (StreamResponse<RawMessageStreamEvent> stream = client.messages().createStreaming(params)) {
        stream.stream().forEach(event -> {
            event.messageDelta().ifPresent(deltaEvent -> {
                deltaEvent.delta().stopReason().ifPresent(stopReason -> {
                    if (stopReason.equals(StopReason.REFUSAL)) {
                        resetConversation();
                    }
                });
            });
        });
    } catch (Exception e) {
        System.err.println("Error: " + e.getMessage());
    }
}

void resetConversation() {
    messages.clear();
    IO.println("Conversation reset due to refusal");
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();
$messages = [];

function resetConversation(&$messages) {
    $messages = [];
    echo "Conversation reset due to refusal\n";
}

try {
    $stream = $client->messages->createStream(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Hello']
        ],
        model: 'claude-opus-4-8',
    );

    foreach ($stream as $event) {
        if (isset($event->type) && $event->type === 'message_delta') {
            if (isset($event->delta->stopReason) && $event->delta->stopReason === 'refusal') {
                resetConversation($messages);
                break;
            }
        }
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new
messages = []

def reset_conversation(messages)
  messages.clear
  puts "Conversation reset due to refusal"
end

begin
  stream = client.messages.stream(
    model: :"claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }]
  )

  stream.each do |event|
    if event.type == :message_delta && event.delta.stop_reason == :refusal
      reset_conversation(messages)
      break
    end
  end
rescue => e
  puts "Error: #{e.message}"
end
```
</CodeGroup>

## Jenis penolakan saat ini \{#current-refusal-types}

API saat ini menangani penolakan dengan tiga cara berbeda:

| Jenis Penolakan | Format Respons | Kapan Terjadi |
|-------------|----------------|----------------|
| Penolakan pengklasifikasi streaming | **`stop_reason`: `refusal`** | Selama streaming ketika konten melanggar kebijakan |
| Validasi input API dan hak cipta | Kode error 400 | Ketika input gagal dalam pemeriksaan validasi |
| Penolakan yang dihasilkan model | Respons teks standar | Ketika model itu sendiri memutuskan untuk menolak |

<Note>
Versi API mendatang akan memperluas pola **`stop_reason`: `refusal`** untuk menyatukan penanganan penolakan di semua jenis.
</Note>

## Praktik terbaik \{#best-practices}

- **Pantau penolakan:** Sertakan pemeriksaan **`stop_reason`: `refusal`** dalam penanganan error Anda
- **Reset secara otomatis:** Implementasikan reset konteks otomatis ketika penolakan terdeteksi
- **Beralih ke model lain:** Konfigurasikan [fallback sisi server atau middleware SDK](/docs/id/build-with-claude/refusals-and-fallback) sehingga permintaan yang ditolak dicoba ulang pada model Claude lain alih-alih menampilkan penolakan kepada pengguna
- **Tukarkan kredit fallback pada percobaan ulang manual:** Jika Anda membangun percobaan ulang sendiri, teruskan token [kredit fallback](/docs/id/build-with-claude/fallback-credit) dari penolakan tersebut sehingga percobaan ulang tidak membayar biaya cache prompt dua kali
- **Sediakan pesan kustom:** Buat pesan yang ramah pengguna untuk UX yang lebih baik ketika penolakan terjadi
- **Lacak pola penolakan:** Pantau frekuensi penolakan untuk mengidentifikasi potensi masalah dengan prompt Anda

## Catatan migrasi \{#migration-notes}

Jika Anda membangun penanganan penolakan ketika fitur ini pertama kali dirilis, atau Anda menambahkannya ke integrasi yang sudah ada, periksa hal-hal berikut:

- **Penolakan adalah respons, bukan error.** Penolakan tiba sebagai respons HTTP 200 yang berhasil dengan `stop_reason`: `"refusal"`, sehingga pemantauan yang hanya dibangun berdasarkan tingkat error tidak akan menampilkannya. Lacak penolakan sebagai sinyal tersendiri.
- **Model yang lebih baru mengembalikan lebih banyak detail.** Pada Claude Fable 5, penolakan juga menyertakan objek `stop_details` yang mengidentifikasi kategori kebijakan di balik penolakan tersebut. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk bentuk respons lengkapnya.
- **Coba ulang pada model yang berbeda.** Mengirim ulang permintaan yang ditolak ke model yang sama biasanya menghasilkan penolakan lagi. Alih-alih hanya mereset konteks, coba ulang pada model cadangan dengan [fallback sisi server, middleware SDK, atau percobaan ulang manual](/docs/id/build-with-claude/refusals-and-fallback), dan tukarkan [kredit fallback](/docs/id/build-with-claude/fallback-credit) ketika Anda membangun percobaan ulang sendiri.
- **Periksa hasil batch untuk penolakan.** Permintaan yang ditolak dalam [Message Batch](/docs/id/build-with-claude/batch-processing) dikembalikan sebagai hasil yang berhasil dengan `stop_reason`: `"refusal"`, bukan sebagai hasil yang error.
- **Pusatkan penanganan pada `stop_reason`.** API terus mengonsolidasikan penanganan penolakan di sekitar `stop_reason`: `"refusal"`, jadi lakukan percabangan berdasarkan stop reason daripada berdasarkan perilaku spesifik model.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Penolakan dan fallback" icon="arrows-clockwise" href="/docs/id/build-with-claude/refusals-and-fallback">
    Coba ulang permintaan yang ditolak pada model Claude lain, di sisi server atau di klien Anda.
  </Card>
  <Card title="Stop reason dan fallback" icon="code" href="/docs/id/build-with-claude/handling-stop-reasons">
    Setiap nilai `stop_reason` dan cara menanganinya.
  </Card>
  <Card title="Pesan streaming" icon="lightning" href="/docs/id/build-with-claude/streaming">
    Stream respons dan baca `stop_reason` dari event `message_delta` saat tiba.
  </Card>
  <Card title="Dukungan multibahasa" icon="text-aa" href="/docs/id/build-with-claude/multilingual-support">
    Layani pengguna di berbagai bahasa dengan kemampuan lintas bahasa Claude.
  </Card>
</CardGroup>