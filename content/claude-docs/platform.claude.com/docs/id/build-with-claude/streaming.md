---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/streaming
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 0a7620f56355e46a1471a533cf75a9aa602fa90f5eb15c641d85b02099f559e7
---

# Pesan Streaming

Pelajari cara melakukan streaming respons pesan secara inkremental menggunakan server-sent events (SSE).

---

Saat membuat Pesan, Anda dapat mengatur `"stream": true` untuk melakukan streaming respons secara inkremental menggunakan [server-sent events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents) (SSE).

## Streaming dengan SDK

[Python](https://github.com/anthropics/anthropic-sdk-python) dan [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript) SDK menawarkan berbagai cara untuk streaming. [PHP](https://github.com/anthropics/anthropic-sdk-php) SDK menyediakan streaming melalui `createStream()`. Python SDK memungkinkan aliran sinkron dan asinkron. Lihat dokumentasi di setiap SDK untuk detail lebih lanjut.

<CodeGroup>
    ```bash CLI
    ant messages create --stream --format jsonl \
      --model claude-opus-4-7 \
      --max-tokens 1024 \
      --message '{role: user, content: "Hello"}' \
      | while IFS= read -r event; do
          [[ $event == *'"text_delta"'* ]] || continue
          text=${event#*'"text":"'}
          printf '%b' "${text%\"*}"
        done
    ```

    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()

    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-opus-4-7",
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    ```

    ```typescript TypeScript hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const client = new Anthropic();

    await client.messages
      .stream({
        messages: [{ role: "user", content: "Hello" }],
        model: "claude-opus-4-7",
        max_tokens: 1024
      })
      .on("text", (text) => {
        console.log(text);
      });
    ```

    ```csharp C#
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
                Messages = [new() { Role = Role.User, Content = "Hello" }]
            };

            await foreach (var msg in client.Messages.CreateStreaming(parameters))
            {
                Console.Write(msg);
            }
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
    		Model:     anthropic.ModelClaudeOpus4_7,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
    		},
    	})

    	for stream.Next() {
    		event := stream.Current()
    		switch eventVariant := event.AsAny().(type) {
    		case anthropic.ContentBlockDeltaEvent:
    			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
    			case anthropic.TextDelta:
    				fmt.Print(deltaVariant.Text)
    			}
    		}
    	}
    	if err := stream.Err(); err != nil {
    		log.Fatal(err)
    	}
    }
    ```

    ```java Java hidelines={1..6,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;

    public class StreamingExample {
        public static void main(String[] args) {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            MessageCreateParams params = MessageCreateParams.builder()
                .model("claude-opus-4-7")
                .maxTokens(1024L)
                .addUserMessage("Hello")
                .build();

            try (var streamResponse = client.messages().createStreaming(params)) {
                streamResponse.stream().forEach(event -> {
                    event.contentBlockDelta().ifPresent(deltaEvent ->
                        deltaEvent.delta().text().ifPresent(td ->
                            System.out.print(td.text())
                        )
                    );
                });
            }
        }
    }
    ```

    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

    $stream = $client->messages->createStream(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Hello']
        ],
        model: 'claude-opus-4-7',
    );

    foreach ($stream as $message) {
        echo $message;
    }
    ```

    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    stream = client.messages.stream(
      model: "claude-opus-4-7",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello" }]
    )

    stream.text.each { |text| print(text) }
    ```
</CodeGroup>

## Dapatkan pesan akhir tanpa menangani acara

Jika Anda tidak perlu memproses teks saat tiba, SDK menyediakan cara untuk menggunakan streaming di balik layar sambil mengembalikan objek `Message` lengkap, identik dengan apa yang dikembalikan `.create()`. Ini sangat berguna untuk permintaan dengan nilai `max_tokens` besar, di mana SDK memerlukan streaming untuk menghindari timeout HTTP.

<CodeGroup>
    ```bash CLI
    # CLI ant dengan flag --stream mengeluarkan satu acara per baris dan tidak
    # mengumpulkan ke Pesan akhir. Untuk generasi panjang, streaming
    # acara mentah:
    ant messages create --stream --format jsonl <<'YAML'
    model: claude-opus-4-7
    max_tokens: 128000
    messages:
      - role: user
        content: Write a detailed analysis...
    YAML
    ```

    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()

    with client.messages.stream(
        max_tokens=128000,
        messages=[{"role": "user", "content": "Write a detailed analysis..."}],
        model="claude-opus-4-7",
    ) as stream:
        message = stream.get_final_message()

    print(message.content[0].text)
    ```

    ```typescript TypeScript hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const client = new Anthropic();

    const stream = client.messages.stream({
      max_tokens: 128000,
      messages: [{ role: "user", content: "Write a detailed analysis..." }],
      model: "claude-opus-4-7"
    });

    const message = await stream.finalMessage();
    const textBlock = message.content.find((block) => block.type === "text");
    if (textBlock && textBlock.type === "text") {
      console.log(textBlock.text);
    }
    ```

    
    ```csharp C# nocheck
    using System;
    using System.Threading.Tasks;
    using Anthropic;
    using Anthropic.Models.Messages;

    class Program
    {
        static async Task Main()
        {
            AnthropicClient client = new();

            var parameters = new MessageCreateParams
            {
                Model = Model.ClaudeOpus4_7,
                MaxTokens = 128000,
                Messages = [new() { Role = Role.User, Content = "Write a detailed analysis..." }]
            };

            var fullText = "";
            await foreach (var msg in client.Messages.CreateStreaming(parameters))
            {
                fullText += msg;
            }

            Console.WriteLine(fullText);
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
    		Model:     anthropic.ModelClaudeOpus4_7,
    		MaxTokens: 128000,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Write a detailed analysis...")),
    		},
    	})

    	message := anthropic.Message{}
    	for stream.Next() {
    		event := stream.Current()
    		if err := message.Accumulate(event); err != nil {
    			log.Fatal(err)
    		}
    	}
    	if err := stream.Err(); err != nil {
    		log.Fatal(err)
    	}

    	fmt.Println(message.Content[0].Text)
    }
    ```

    ```java Java hidelines={1..2,4..9,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.helpers.MessageAccumulator;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;
    import com.anthropic.models.messages.Model;

    public class StreamingExample {
        public static void main(String[] args) {
            AnthropicClient client = AnthropicOkHttpClient.fromEnv();

            MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_7)
                .maxTokens(128000L)
                .addUserMessage("Write a detailed analysis...")
                .build();

            MessageAccumulator accumulator = MessageAccumulator.create();
            try (var streamResponse = client.messages().createStreaming(params)) {
                streamResponse.stream().forEach(accumulator::accumulate);
            }

            Message message = accumulator.message();
            message.content().get(0).text().ifPresent(tb -> System.out.println(tb.text()));
        }
    }
    ```

    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

    $stream = $client->messages->createStream(
        maxTokens: 128000,
        messages: [
            ['role' => 'user', 'content' => 'Write a detailed analysis...']
        ],
        model: 'claude-opus-4-7',
    );

    $fullText = '';
    foreach ($stream as $event) {
        if ($event->type === 'content_block_delta') {
            $fullText .= $event->delta->text;
        }
    }

    echo $fullText;
    ```

    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    message = client.messages.stream(
      model: "claude-opus-4-7",
      max_tokens: 128000,
      messages: [{ role: "user", content: "Write a detailed analysis..." }]
    ).accumulated_message

    puts message.content.first.text
    ```
</CodeGroup>

Panggilan `.stream()` menjaga koneksi HTTP tetap aktif dengan server-sent events, kemudian `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) mengumpulkan semua acara dan mengembalikan objek `Message` lengkap. Di Go, Anda memanggil `message.Accumulate(event)` di dalam loop streaming untuk membangun `Message` lengkap yang sama. Di Java, gunakan `MessageAccumulator.create()` dan panggil `accumulator.accumulate(event)` pada setiap acara. Di Ruby, panggil `.accumulated_message` pada streaming. Di SDK PHP, Anda mengulangi acara streaming secara manual untuk mengumpulkan respons.

## Jenis acara

Setiap server-sent event mencakup jenis acara bernama dan data JSON terkait. Setiap acara menggunakan nama acara SSE (misalnya `event: message_stop`), dan menyertakan `type` acara yang cocok dalam datanya.

Setiap streaming menggunakan alur acara berikut:

1. `message_start`: berisi objek `Message` dengan `content` kosong.
2. Serangkaian blok konten, masing-masing memiliki acara `content_block_start`, satu atau lebih acara `content_block_delta`, dan acara `content_block_stop`. Setiap blok konten memiliki `index` yang sesuai dengan indeksnya dalam array `content` Pesan akhir.
3. Satu atau lebih acara `message_delta`, menunjukkan perubahan tingkat atas pada objek `Message` akhir.
4. Acara `message_stop` akhir.

  <Warning>
  Jumlah token yang ditampilkan di bidang `usage` acara `message_delta` adalah *kumulatif*.
  </Warning>

### Acara ping

Aliran acara juga dapat mencakup sejumlah acara `ping`.

### Acara kesalahan

API mungkin kadang-kadang mengirim [kesalahan](/docs/id/api/errors) dalam aliran acara. Misalnya, selama periode penggunaan tinggi, Anda mungkin menerima `overloaded_error`, yang biasanya sesuai dengan HTTP 529 dalam konteks non-streaming:

```sse Contoh kesalahan
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

### Acara lainnya

Sesuai dengan [kebijakan versioning](/docs/id/api/versioning), jenis acara baru dapat ditambahkan, dan kode Anda harus menangani jenis acara yang tidak dikenal dengan baik.

## Jenis delta blok konten

Setiap acara `content_block_delta` berisi `delta` dari jenis yang memperbarui blok `content` pada `index` tertentu.

### Delta teks

Delta blok konten `text` terlihat seperti:
```sse Delta teks
event: content_block_delta
data: {"type": "content_block_delta","index": 0,"delta": {"type": "text_delta", "text": "ello frien"}}
```

### Delta JSON input

Delta untuk blok konten `tool_use` sesuai dengan pembaruan untuk bidang `input` blok. Untuk mendukung granularitas maksimal, delta adalah _string JSON parsial_, sedangkan `tool_use.input` akhir selalu merupakan _objek_.

Anda dapat mengumpulkan delta string dan mengurai JSON setelah menerima acara `content_block_stop`, dengan menggunakan perpustakaan seperti [Pydantic](https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing) untuk melakukan parsing JSON parsial, atau dengan menggunakan [SDK](/docs/id/api/client-sdks), yang menyediakan pembantu untuk mengakses nilai inkremental yang diurai.

Delta blok konten `tool_use` terlihat seperti:
```sse Delta JSON input
event: content_block_delta
data: {"type": "content_block_delta","index": 1,"delta": {"type": "input_json_delta","partial_json": "{\"location\": \"San Fra"}}
```
Catatan: Model saat ini hanya mendukung pemancarannya satu properti kunci dan nilai lengkap dari `input` pada satu waktu. Dengan demikian, saat menggunakan alat, mungkin ada penundaan antara acara streaming saat model sedang bekerja. Setelah kunci dan nilai `input` dikumpulkan, mereka dipancarkan sebagai beberapa acara `content_block_delta` dengan json parsial yang dipotong sehingga format dapat secara otomatis mendukung granularitas lebih halus di model masa depan.

### Delta pemikiran

Saat menggunakan [extended thinking](/docs/id/build-with-claude/extended-thinking#streaming-thinking) dengan streaming diaktifkan, Anda akan menerima konten pemikiran melalui acara `thinking_delta`. Delta ini sesuai dengan bidang `thinking` dari blok konten `thinking`.

Untuk konten pemikiran, acara `signature_delta` khusus dikirim tepat sebelum acara `content_block_stop`. Tanda tangan ini digunakan untuk memverifikasi integritas blok pemikiran.

Ketika `display: "omitted"` diatur pada konfigurasi pemikiran, tidak ada acara `thinking_delta` yang dikirim. Blok pemikiran terbuka, menerima `signature_delta` tunggal, dan ditutup. Lihat [Mengontrol tampilan pemikiran](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display).

Delta pemikiran khas terlihat seperti:
```sse Delta pemikiran
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}
```

Delta tanda tangan terlihat seperti:
```sse Delta tanda tangan
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}
```

## Respons aliran HTTP lengkap

Gunakan [SDK klien](/docs/id/api/client-sdks) saat menggunakan mode streaming. Namun, jika Anda membangun integrasi API langsung, Anda perlu menangani acara ini sendiri.

Respons streaming terdiri dari:
1. Acara `message_start`
2. Berpotensi beberapa blok konten, masing-masing berisi:
    - Acara `content_block_start`
    - Berpotensi beberapa acara `content_block_delta`
    - Acara `content_block_stop`
3. Acara `message_delta`
4. Acara `message_stop`

Mungkin ada acara `ping` yang tersebar di seluruh respons juga. Lihat [Jenis acara](#event-types) untuk detail lebih lanjut tentang formatnya.

### Permintaan streaming dasar

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --data \
'{
  "model": "claude-opus-4-7",
  "messages": [{"role": "user", "content": "Hello"}],
  "max_tokens": 256,
  "stream": true
}'
```

```bash CLI
ant messages create --stream --format jsonl \
  --model claude-opus-4-7 \
  --max-tokens 256 \
  --message '{role: user, content: Hello}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-7",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=256,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-opus-4-7",
  messages: [{ role: "user", content: "Hello" }],
  max_tokens: 256
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

```csharp C#
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
            MaxTokens = 256,
            Messages = [new() { Role = Role.User, Content = "Hello" }]
        };

        await foreach (var msg in client.Messages.CreateStreaming(parameters))
        {
            Console.Write(msg);
        }
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
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 256,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
		},
	})

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockDeltaEvent:
			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
			case anthropic.TextDelta:
				fmt.Print(deltaVariant.Text)
			}
		}
	}
	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class StreamingExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(256L)
            .addUserMessage("Hello")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                event.contentBlockDelta().ifPresent(deltaEvent ->
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    )
                );
            });
        }
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$stream = $client->messages->createStream(
    maxTokens: 256,
    messages: [
        ['role' => 'user', 'content' => 'Hello']
    ],
    model: 'claude-opus-4-7',
);

foreach ($stream as $message) {
    echo $message;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

stream = client.messages.stream(
  model: "claude-opus-4-7",
  messages: [{ role: "user", content: "Hello" }],
  max_tokens: 256
)

stream.text.each { |text| print(text) }
```
</CodeGroup>

```sse Respons
event: message_start
data: {"type": "message_start", "message": {"id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-7", "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "!"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence":null}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}

```

### Permintaan streaming dengan penggunaan alat

<Tip>
Penggunaan alat mendukung [streaming butir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) untuk nilai parameter. Aktifkan per alat dengan `eager_input_streaming`.
</Tip>

Permintaan ini meminta Claude untuk menggunakan alat untuk melaporkan cuaca.

<CodeGroup>
```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-7",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "tool_choice": {"type": "any"},
      "messages": [
        {
          "role": "user",
          "content": "What is the weather like in San Francisco?"
        }
      ],
      "stream": true
    }'
```

```bash CLI
ant messages create --stream --format jsonl <<'YAML'
model: claude-opus-4-7
max_tokens: 1024
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      required:
        - location
tool_choice:
  type: any
messages:
  - role: user
    content: What is the weather like in San Francisco?
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    }
]

with client.messages.stream(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[
        {"role": "user", "content": "What is the weather like in San Francisco?"}
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  }
];

const stream = client.messages.stream({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: tools,
  tool_choice: { type: "any" },
  messages: [
    {
      role: "user",
      content: "What is the weather like in San Francisco?"
    }
  ]
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
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
            MaxTokens = 1024,
            Tools = [
                new ToolUnion(new Tool()
                {
                    Name = "get_weather",
                    Description = "Get the current weather in a given location",
                    InputSchema = new InputSchema()
                    {
                        Properties = new Dictionary<string, JsonElement>
                        {
                            ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                        },
                        Required = ["location"],
                    },
                }),
            ],
            ToolChoice = new ToolChoiceAny(),
            Messages = [
                new() { Role = Role.User, Content = "What is the weather like in San Francisco?" }
            ]
        };

        await foreach (var msg in client.Messages.CreateStreaming(parameters))
        {
            Console.Write(msg);
        }
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
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:        "get_weather",
				Description: anthropic.String("Get the current weather in a given location"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"location": map[string]any{
							"type":        "string",
							"description": "The city and state, e.g. San Francisco, CA",
						},
					},
					Required: []string{"location"},
				},
			}},
		},
		ToolChoice: anthropic.ToolChoiceUnionParam{OfAny: &anthropic.ToolChoiceAnyParam{}},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather like in San Francisco?")),
		},
	})

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockDeltaEvent:
			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
			case anthropic.TextDelta:
				fmt.Print(deltaVariant.Text)
			}
		}
	}
	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ToolChoice;
import com.anthropic.models.messages.ToolChoiceAny;
import com.anthropic.models.messages.Tool;
import com.anthropic.core.JsonValue;
import java.util.Map;
import java.util.List;

public class StreamingToolUse {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(1024L)
            .addTool(Tool.builder()
                .name("get_weather")
                .description("Get the current weather in a given location")
                .inputSchema(Tool.InputSchema.builder()
                    .properties(JsonValue.from(Map.of(
                        "location", Map.of(
                            "type", "string",
                            "description", "The city and state, e.g. San Francisco, CA"
                        )
                    )))
                    .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                    .build())
                .build())
            .toolChoice(ToolChoice.ofAny(ToolChoiceAny.builder().build()))
            .addUserMessage("What is the weather like in San Francisco?")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                event.contentBlockDelta().ifPresent(deltaEvent ->
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    )
                );
            });
        }
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$stream = $client->messages->createStream(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather like in San Francisco?']
    ],
    model: 'claude-opus-4-7',
    toolChoice: ['type' => 'any'],
    tools: [
        [
            'name' => 'get_weather',
            'description' => 'Get the current weather in a given location',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'location' => [
                        'type' => 'string',
                        'description' => 'The city and state, e.g. San Francisco, CA'
                    ]
                ],
                'required' => ['location']
            ]
        ]
    ],
);

foreach ($stream as $message) {
    echo $message;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

tools = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  }
]

stream = client.messages.stream(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: tools,
  tool_choice: { type: "any" },
  messages: [
    { role: "user", content: "What is the weather like in San Francisco?" }
  ]
)

stream.text.each { |text| print(text) }
```
</CodeGroup>

```sse Response
event: message_start
data: {"type":"message_start","message":{"id":"msg_014p7gG3wDgGV9EUtLvnow3U","type":"message","role":"assistant","model":"claude-opus-4-7","stop_sequence":null,"usage":{"input_tokens":472,"output_tokens":2},"content":[],"stop_reason":null}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Okay"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" let"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"'s"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" for"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" Francisco"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" CA"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":":"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"tool_use","id":"toolu_01T1x1fJ34qAmk2tNTrN7Up6","name":"get_weather","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"location\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" Francisc"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"o,"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" CA\""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" "}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"\"unit\": \"fah"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"renheit\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"tool_use","stop_sequence":null},"usage":{"output_tokens":89}}

event: message_stop
data: {"type":"message_stop"}
```

### Permintaan streaming dengan pemikiran yang diperluas

Permintaan ini mengaktifkan pemikiran yang diperluas dengan streaming untuk melihat penalaran langkah demi langkah Claude.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-7",
    "max_tokens": 20000,
    "stream": true,
    "thinking": {
        "type": "adaptive",
        "display": "summarized"
    },
    "messages": [
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?"
        }
    ]
}'
```

```bash CLI
ant messages create --stream --format jsonl \
  --model claude-opus-4-7 \
  --max-tokens 20000 \
  --thinking '{type: adaptive, display: summarized}' \
  --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-7",
    max_tokens=20000,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?",
        }
    ],
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-opus-4-7",
  max_tokens: 20000,
  thinking: { type: "adaptive", display: "summarized" },
  messages: [
    {
      role: "user",
      content: "What is the greatest common divisor of 1071 and 462?"
    }
  ]
});

for await (const event of stream) {
  if (event.type === "content_block_delta") {
    if (event.delta.type === "thinking_delta") {
      process.stdout.write(event.delta.thinking);
    } else if (event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}
```

```csharp C#
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_6,
    MaxTokens = 20000,
    Thinking = new ThinkingConfigEnabled(budgetTokens: 16000),
    Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
};

await foreach (var msg in client.Messages.CreateStreaming(parameters))
{
    Console.Write(msg);
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
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(16000),
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
		},
	})

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockDeltaEvent:
			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
			case anthropic.ThinkingDelta:
				fmt.Print(deltaVariant.Thinking)
			case anthropic.TextDelta:
				fmt.Print(deltaVariant.Text)
			}
		}
	}
	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..7,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class ExtendedThinkingStreaming {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(20000L)
            .enabledThinking(16000L)
            .addUserMessage("What is the greatest common divisor of 1071 and 462?")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                event.contentBlockDelta().ifPresent(deltaEvent -> {
                    deltaEvent.delta().thinking().ifPresent(td ->
                        System.out.print(td.thinking())
                    );
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    );
                });
            });
        }
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$stream = $client->messages->createStream(
    maxTokens: 20000,
    messages: [
        ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
    ],
    model: 'claude-opus-4-7',
    thinking: ['type' => 'adaptive', 'display' => 'summarized'],
);

foreach ($stream as $message) {
    echo $message;
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

stream = client.messages.stream(
  model: "claude-opus-4-7",
  max_tokens: 20000,
  thinking: { type: "adaptive", display: "summarized" },
  messages: [
    { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
  ]
)

stream.each do |event|
  if event.type == :content_block_delta
    if event.delta.type == :thinking_delta
      print(event.delta.thinking)
    elsif event.delta.type == :text_delta
      print(event.delta.text)
    end
  end
end
```
</CodeGroup>

```sse Response
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-7", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n147 = 7 × 21 + 0"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\nThe remainder is 0, so GCD(1071, 462) = 21."}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

### Permintaan streaming dengan penggunaan alat pencarian web

Permintaan ini meminta Claude untuk mencari web untuk informasi cuaca terkini.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-7",
    "max_tokens": 1024,
    "stream": true,
    "tools": [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in New York City today?"
        }
    ]
}'
```

```bash CLI
ant messages create --stream --format jsonl \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --tool '{type: web_search_20250305, name: web_search, max_uses: 5}' \
  --message '{role: user, content: What is the weather like in New York City today?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
    messages=[
        {"role": "user", "content": "What is the weather like in New York City today?"}
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-opus-4-7",
  max_tokens: 1024,
  tools: [{ type: "web_search_20250305", name: "web_search", max_uses: 5 }],
  messages: [{ role: "user", content: "What is the weather like in New York City today?" }]
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

```csharp C#
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_7,
    MaxTokens = 1024,
    Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 5 })],
    Messages = [new() { Role = Role.User, Content = "What is the weather like in New York City today?" }]
};

await foreach (var msg in client.Messages.CreateStreaming(parameters))
{
    Console.Write(msg);
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
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Tools: []anthropic.ToolUnionParam{
			{
				OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
					MaxUses: anthropic.Int(5),
				},
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather like in New York City today?")),
		},
	})

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockDeltaEvent:
			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
			case anthropic.TextDelta:
				fmt.Print(deltaVariant.Text)
			}
		}
	}
	if err := stream.Err(); err != nil {
		log.Fatal(err)
	}
}
```

```java Java hidelines={1..4,6..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebSearchTool20250305;

public class WebSearchStreaming {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(1024L)
            .addTool(WebSearchTool20250305.builder()
                .maxUses(5L)
                .build())
            .addUserMessage("What is the weather like in New York City today?")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                event.contentBlockDelta().ifPresent(deltaEvent ->
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    )
                );
            });
        }
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$stream = $client->messages->createStream(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather like in New York City today?']
    ],
    model: 'claude-opus-4-7',
    tools: [
        ['type' => 'web_search_20250305', 'name' => 'web_search', 'max_uses' => 5]
    ],
);

foreach ($stream as $message) {
    echo $message;
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

stream = client.messages.stream(
  model: :"claude-opus-4-7",
  max_tokens: 1024,
  tools: [
    {
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 5
    }
  ],
  messages: [
    {
      role: "user",
      content: "What is the weather like in New York City today?"
    }
  ]
)

stream.text.each { |text| print(text) }
```
</CodeGroup>

```sse Response
event: message_start
data: {"type":"message_start","message":{"id":"msg_01G...","type":"message","role":"assistant","model":"claude-opus-4-7","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":2679,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":3}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"I'll check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the current weather in New York City for you"}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"server_tool_use","id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","name":"web_search","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"query"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" NY"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"C to"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"day\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1 }

event: content_block_start
data: {"type":"content_block_start","index":2,"content_block":{"type":"web_search_tool_result","tool_use_id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","content":[{"type":"web_search_result","title":"Weather in New York City in May 2025 (New York) - detailed Weather Forecast for a month","url":"https://world-weather.info/forecast/usa/new_york/may-2025/","encrypted_content":"Ev0DCioIAxgCIiQ3NmU4ZmI4OC1k...","page_age":null},...]}}

event: content_block_stop
data: {"type":"content_block_stop","index":2}

event: content_block_start
data: {"type":"content_block_start","index":3,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"Here's the current weather information for New York"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" City:\n\n# Weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" in New York City"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"\n\n"}}

...

event: content_block_stop
data: {"type":"content_block_stop","index":17}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"input_tokens":10682,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":510,"server_tool_use":{"web_search_requests":1}}}

event: message_stop
data: {"type":"message_stop"}
```

## Pemulihan kesalahan

### Claude 4.5 dan lebih awal

Untuk model Claude 4.5 dan lebih awal, Anda dapat memulihkan permintaan streaming yang terputus karena masalah jaringan, batas waktu, atau kesalahan lainnya dengan melanjutkan dari tempat aliran terputus. Pendekatan ini menghemat Anda dari pemrosesan ulang seluruh respons.

Strategi pemulihan dasar melibatkan:

1. **Tangkap respons parsial**: Simpan semua konten yang berhasil diterima sebelum kesalahan terjadi
2. **Buat permintaan kelanjutan**: Buat permintaan API baru yang mencakup respons asisten parsial sebagai awal dari pesan asisten baru
3. **Lanjutkan streaming**: Terus menerima sisa respons dari tempat terputus

### Claude 4.6

Untuk model Claude 4.6, Anda harus menambahkan pesan pengguna yang menginstruksikan model untuk melanjutkan dari tempat terakhir. Misalnya:

```text Sample prompt
Your previous response was interrupted and ended with [previous_response]. Continue from where you left off.
```

### Praktik terbaik pemulihan kesalahan

1. **Gunakan fitur SDK**: Manfaatkan kemampuan akumulasi pesan dan penanganan kesalahan bawaan SDK
2. **Tangani jenis konten**: Ketahui bahwa pesan dapat berisi beberapa blok konten (`text`, `tool_use`, `thinking`). Blok penggunaan alat dan pemikiran yang diperluas tidak dapat dipulihkan sebagian. Anda dapat melanjutkan streaming dari blok teks paling baru.