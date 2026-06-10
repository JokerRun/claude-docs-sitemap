---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/adaptive-thinking
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: c37e5c7296313b0af16dd60439e431e8670a18a1102637a632a477a543fcea84
---

# Pemikiran adaptif

Biarkan Claude secara dinamis menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang dengan mode pemikiran adaptif.

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Pemikiran adaptif adalah cara yang direkomendasikan untuk menggunakan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dengan Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. Pada Claude Fable 5 dan [Claude Mythos 5](https://anthropic.com/glasswing), pemikiran selalu diaktifkan dan tidak dapat dinonaktifkan; pemikiran adaptif adalah satu-satunya mode pemikiran. Pada [Claude Mythos Preview](https://anthropic.com/glasswing), pemikiran adaptif adalah mode default dan diterapkan secara otomatis setiap kali `thinking` tidak disetel. Alih-alih menetapkan anggaran token pemikiran secara manual, pemikiran adaptif memungkinkan Claude secara dinamis menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang berdasarkan kompleksitas setiap permintaan. Pada Claude Opus 4.8 dan Claude Opus 4.7, pemikiran adaptif adalah **satu-satunya** mode pemikiran yang didukung; `thinking: {type: "enabled", budget_tokens: N}` manual tidak lagi diterima.

<Tip>
Pemikiran adaptif dapat menghasilkan performa yang lebih baik daripada pemikiran diperpanjang dengan `budget_tokens` tetap untuk banyak beban kerja, terutama tugas bimodal dan alur kerja agentik jangka panjang. Tidak diperlukan header beta.

Jika beban kerja Anda memerlukan latensi yang dapat diprediksi atau kontrol yang presisi atas biaya pemikiran, pemikiran diperpanjang dengan `budget_tokens` masih berfungsi pada Claude Opus 4.6 dan Claude Sonnet 4.6 tetapi sudah tidak digunakan lagi (deprecated) dan tidak lagi direkomendasikan. Lihat peringatan di bawah.
</Tip>

## Model yang didukung \{#supported-models}

Pemikiran adaptif didukung pada model-model berikut:

- Claude Fable 5 (`claude-fable-5`) dan Claude Mythos 5 (`claude-mythos-5`), pemikiran adaptif selalu aktif; `thinking: {type: "disabled"}` tidak didukung
- Claude Mythos Preview (claude-mythos-preview), pemikiran adaptif adalah default; `thinking: {type: "disabled"}` tidak didukung
- Claude Opus 4.8 (claude-opus-4-8), pemikiran adaptif adalah satu-satunya mode pemikiran yang didukung. Pemikiran nonaktif kecuali Anda secara eksplisit menetapkan `thinking: {type: "adaptive"}` dalam permintaan Anda; `thinking: {type: "enabled"}` manual ditolak dengan error 400.
- Claude Opus 4.7 (claude-opus-4-7), pemikiran adaptif adalah satu-satunya mode pemikiran yang didukung. Pemikiran nonaktif kecuali Anda secara eksplisit menetapkan `thinking: {type: "adaptive"}` dalam permintaan Anda; `thinking: {type: "enabled"}` manual ditolak dengan error 400.
- Claude Opus 4.6 (claude-opus-4-6)
- Claude Sonnet 4.6 (claude-sonnet-4-6)

<Warning>
`thinking.type: "enabled"` dan `budget_tokens` sudah [**tidak digunakan lagi (deprecated)**](/docs/id/build-with-claude/overview#feature-availability) pada Opus 4.6 dan Sonnet 4.6 dan akan dihapus dalam rilis model mendatang. Gunakan `thinking.type: "adaptive"` dengan parameter `effort` sebagai gantinya. Konfigurasi `budget_tokens` yang ada masih berfungsi tetapi tidak lagi direkomendasikan; rencanakan untuk bermigrasi.

Model yang lebih lama (Sonnet 4.5, Opus 4.5, dll.) tidak mendukung pemikiran adaptif dan memerlukan `thinking.type: "enabled"` dengan `budget_tokens`.
</Warning>

## Cara kerja pemikiran adaptif \{#how-adaptive-thinking-works}

Dalam mode adaptif, pemikiran bersifat opsional bagi model. Claude mengevaluasi kompleksitas setiap permintaan dan menentukan apakah dan seberapa banyak menggunakan pemikiran diperpanjang. Pada tingkat effort default (`high`), Claude hampir selalu berpikir. Pada tingkat effort yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana.

Pemikiran adaptif juga secara otomatis mengaktifkan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) (pemikiran berselang). Ini berarti Claude dapat berpikir di antara pemanggilan alat, menjadikannya sangat efektif untuk alur kerja agentik.

## Cara menggunakan pemikiran adaptif \{#how-to-use-adaptive-thinking}

Setel `thinking.type` ke `"adaptive"` dalam permintaan API Anda:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 16000,
    "thinking": {
        "type": "adaptive"
    },
    "messages": [
        {
            "role": "user",
            "content": "Explain why the sum of two even numbers is always even."
        }
    ]
}'
```

```bash CLI nocheck
ant messages create \
  --model claude-opus-4-8 \
  --max-tokens 16000 \
  --thinking '{type: adaptive}' \
  --message '{role: user, content: Explain why the sum of two even numbers is always even.}' \
  --transform content --format jsonl |
  jq -r '
    if   .type == "thinking" then "\nThinking: \(.thinking)"
    elif .type == "text"     then "\nResponse: \(.text)"
    else empty end'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[
        {
            "role": "user",
            "content": "Explain why the sum of two even numbers is always even.",
        }
    ],
)

for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  messages: [
    {
      role: "user",
      content: "Explain why the sum of two even numbers is always even."
    }
  ]
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`\nThinking: ${block.thinking}`);
  } else if (block.type === "text") {
    console.log(`\nResponse: ${block.text}`);
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
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigAdaptive(),
            Messages = [
                new() {
                    Role = Role.User,
                    Content = "Explain why the sum of two even numbers is always even."
                }
            ]
        };

        var message = await client.Messages.Create(parameters);

        foreach (var block in message.Content)
        {
            if (block.TryPickThinking(out ThinkingBlock? thinking))
            {
                Console.WriteLine($"\nThinking: {thinking.Thinking}");
            }
            else if (block.TryPickText(out TextBlock? text))
            {
                Console.WriteLine($"\nResponse: {text.Text}");
            }
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 16000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Explain why the sum of two even numbers is always even.")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	for _, block := range response.Content {
		switch v := block.AsAny().(type) {
		case anthropic.ThinkingBlock:
			fmt.Printf("\nThinking: %s", v.Thinking)
		case anthropic.TextBlock:
			fmt.Printf("\nResponse: %s", v.Text)
		}
	}
}
```

```java Java hidelines={1..5,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ThinkingConfigAdaptive;

public class ExtendedThinkingExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(16000L)
            .thinking(ThinkingConfigAdaptive.builder().build())
            .addUserMessage("Explain why the sum of two even numbers is always even.")
            .build();

        Message response = client.messages().create(params);

        response.content().forEach(block -> {
            block.thinking().ifPresent(thinkingBlock ->
                System.out.println("\nThinking: " + thinkingBlock.thinking())
            );
            block.text().ifPresent(textBlock ->
                System.out.println("\nResponse: " + textBlock.text())
            );
        });
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 16000,
    messages: [
        [
            'role' => 'user',
            'content' => 'Explain why the sum of two even numbers is always even.'
        ]
    ],
    model: 'claude-opus-4-8',
    thinking: ['type' => 'adaptive'],
);

foreach ($message->content as $block) {
    if ($block->type === 'thinking') {
        echo "\nThinking: " . $block->thinking;
    } elseif ($block->type === 'text') {
        echo "\nResponse: " . $block->text;
    }
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  messages: [
    {
      role: "user",
      content: "Explain why the sum of two even numbers is always even."
    }
  ]
)

message.content.each do |block|
  case block.type
  when :thinking
    puts "\nThinking: #{block.thinking}"
  when :text
    puts "\nResponse: #{block.text}"
  end
end
```
</CodeGroup>

## Pemikiran adaptif dengan parameter effort \{#adaptive-thinking-with-the-effort-parameter}

Anda dapat menggabungkan pemikiran adaptif dengan [parameter effort](/docs/id/build-with-claude/effort) untuk memandu seberapa banyak pemikiran yang dilakukan Claude. Tingkat effort bertindak sebagai panduan lunak untuk alokasi pemikiran Claude:

| Tingkat effort | Perilaku pemikiran |
|:-------------|:------------------|
| `max` | Claude selalu berpikir tanpa batasan pada kedalaman pemikiran. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. |
| `xhigh` | Claude selalu berpikir secara mendalam dengan eksplorasi yang diperluas. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7. |
| `high` (default) | Claude hampir selalu berpikir. Memberikan penalaran mendalam pada tugas-tugas kompleks. |
| `medium` | Claude menggunakan pemikiran moderat. Mungkin melewatkan pemikiran untuk kueri yang sangat sederhana. |
| `low` | Claude meminimalkan pemikiran. Melewatkan pemikiran untuk tugas sederhana di mana kecepatan paling penting. |

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 16000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
}'
```

```bash CLI
ant messages create \
  --transform 'content.0.text' --raw-output <<'YAML'
model: claude-opus-4-8
max_tokens: 16000
thinking:
  type: adaptive
output_config:
  effort: medium
messages:
  - role: user
    content: What is the capital of France?
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

print(response.content[0].text)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  output_config: {
    effort: "medium"
  },
  messages: [
    {
      role: "user",
      content: "What is the capital of France?"
    }
  ]
});

for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
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
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigAdaptive(),
            OutputConfig = new OutputConfig { Effort = Effort.Medium },
            Messages = [new() { Role = Role.User, Content = "What is the capital of France?" }]
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
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
		MaxTokens: 16000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
		},
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortMedium,
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the capital of France?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content[0].Text)
}
```

```java Java hidelines={1..5,8..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.OutputConfig;
import com.anthropic.models.messages.ThinkingConfigAdaptive;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(16000L)
            .thinking(ThinkingConfigAdaptive.builder().build())
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.MEDIUM)
                .build())
            .addUserMessage("What is the capital of France?")
            .build();

        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(textBlock -> System.out.println(textBlock.text()));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the capital of France?']
    ],
    model: 'claude-opus-4-8',
    thinking: ['type' => 'adaptive'],
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: {
    type: "adaptive"
  },
  output_config: {
    effort: "medium"
  },
  messages: [
    { role: "user", content: "What is the capital of France?" }
  ]
)

puts message.content.first.text
```
</CodeGroup>

## Streaming dengan pemikiran adaptif \{#streaming-with-adaptive-thinking}

Pemikiran adaptif bekerja dengan mulus bersama [streaming](/docs/id/build-with-claude/streaming). Blok pemikiran di-stream melalui event `thinking_delta` sama seperti mode pemikiran manual:

<CodeGroup>
```bash CLI
ant messages create --stream --format jsonl \
  --model claude-opus-4-8 \
  --max-tokens 16000 \
  --thinking '{type: adaptive}' \
  --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-8",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?",
        }
    ],
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print(f"\nStarting {event.content_block.type} block...")
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = await client.messages.stream({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "What is the greatest common divisor of 1071 and 462?" }]
});

for await (const event of stream) {
  if (event.type === "content_block_start") {
    console.log(`\nStarting ${event.content_block.type} block...`);
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "thinking_delta") {
      process.stdout.write(event.delta.thinking);
    } else if (event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
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
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigAdaptive(),
            Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 16000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
		},
	})

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockStartEvent:
			fmt.Printf("\nStarting %s block...\n", eventVariant.ContentBlock.Type)
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

```java Java hidelines={1..4,6..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ThinkingConfigAdaptive;

public class StreamingThinkingExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(16000L)
            .thinking(ThinkingConfigAdaptive.builder().build())
            .addUserMessage("What is the greatest common divisor of 1071 and 462?")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                if (event.contentBlockStart().isPresent()) {
                    var startEvent = event.contentBlockStart().get();
                    var block = startEvent.contentBlock();
                    if (block.isThinking()) {
                        System.out.println("\nStarting thinking block...");
                    } else if (block.isText()) {
                        System.out.println("\nStarting text block...");
                    }
                } else if (event.contentBlockDelta().isPresent()) {
                    var deltaEvent = event.contentBlockDelta().get();
                    deltaEvent.delta().thinking().ifPresent(td ->
                        System.out.print(td.thinking())
                    );
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    );
                }
            });
        }
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$stream = $client->messages->createStream(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
    ],
    model: 'claude-opus-4-8',
    thinking: ['type' => 'adaptive'],
);

foreach ($stream as $event) {
    if ($event->type === 'content_block_start') {
        echo "\nStarting {$event->contentBlock->type} block...\n";
    } elseif ($event->type === 'content_block_delta') {
        if ($event->delta->type === 'thinking_delta') {
            echo $event->delta->thinking;
        } elseif ($event->delta->type === 'text_delta') {
            echo $event->delta->text;
        }
    }
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

stream = client.messages.stream(
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  messages: [
    { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
  ]
)

stream.each do |event|
  case event
  when Anthropic::Streaming::ThinkingEvent
    print event.thinking
  when Anthropic::Streaming::TextEvent
    print event.text
  end
end
```
</CodeGroup>

## Pemikiran adaptif vs manual vs dinonaktifkan \{#adaptive-vs-manual-vs-disabled-thinking}

| Mode | Konfigurasi | Ketersediaan | Kapan digunakan |
|:-----|:-------|:-------------|:------------|
| **Adaptif** | `thinking: {type: "adaptive"}` | Claude Fable 5 (selalu aktif), Claude Mythos 5 (selalu aktif), Claude Mythos Preview (default), Claude Opus 4.8 (satu-satunya mode), Opus 4.7 (satu-satunya mode), Opus 4.6, Sonnet 4.6 | Claude menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang. Gunakan `effort` untuk memandu. |
| **Manual** | `thinking: {type: "enabled", budget_tokens: N}` | Semua model kecuali Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7 (ditolak dengan error 400). Tidak digunakan lagi (deprecated) pada Opus 4.6 dan Sonnet 4.6 (pertimbangkan mode adaptif sebagai gantinya). | Ketika Anda memerlukan kontrol presisi atas pengeluaran token pemikiran. |
| **Dinonaktifkan** | Hilangkan parameter `thinking` atau kirim `{type: "disabled"}` | Semua model kecuali Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview | Ketika Anda tidak memerlukan pemikiran diperpanjang dan menginginkan latensi terendah. |

<Note>
Pemikiran adaptif tersedia pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 4.8, Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Pada Claude Fable 5 dan Claude Mythos 5, pemikiran adaptif selalu aktif: diterapkan setiap kali `thinking` tidak disetel dan tidak dapat dinonaktifkan. Pada Mythos Preview, pemikiran adaptif adalah default dan diterapkan secara otomatis setiap kali `thinking` tidak disetel. Pada Claude Opus 4.8, pemikiran adaptif adalah satu-satunya mode yang didukung; pemikiran nonaktif kecuali Anda secara eksplisit menetapkan `thinking: {type: "adaptive"}`, dan `type: "enabled"` manual dengan `budget_tokens` ditolak dengan error 400. Pada Claude Opus 4.7, pemikiran adaptif adalah satu-satunya mode yang didukung dan `type: "enabled"` dengan `budget_tokens` ditolak. Model yang lebih lama hanya mendukung `type: "enabled"` dengan `budget_tokens`. Pada Opus 4.6 dan Sonnet 4.6, `type: "enabled"` dengan `budget_tokens` masih berfungsi tetapi sudah tidak digunakan lagi (deprecated).

**Ketersediaan interleaved thinking berdasarkan mode:**
- **Mode adaptif:** Interleaved thinking diaktifkan secara otomatis pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 4.8, Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Pada Claude Fable 5, Claude Mythos 5, Mythos Preview, Claude Opus 4.8, dan Opus 4.7, penalaran antar-alat selalu berada di dalam blok pemikiran.
- **Mode manual pada Sonnet 4.6:** Interleaved thinking bekerja melalui header beta `interleaved-thinking-2025-05-14`.
- **Mode manual pada Opus 4.6:** Interleaved thinking tidak tersedia. Jika alur kerja agentik Anda memerlukan pemikiran di antara pemanggilan alat pada Opus 4.6, gunakan mode adaptif.
</Note>

## Pertimbangan penting \{#important-considerations}

### Perubahan validasi \{#validation-changes}

Saat menggunakan pemikiran adaptif, giliran asisten sebelumnya tidak perlu dimulai dengan blok pemikiran. Ini lebih fleksibel daripada mode manual, di mana API mengharuskan giliran dengan pemikiran aktif dimulai dengan blok pemikiran.

### Caching prompt \{#prompt-caching}

Permintaan berturut-turut yang menggunakan pemikiran `adaptive` mempertahankan breakpoint [cache prompt](/docs/id/build-with-claude/prompt-caching). Namun, beralih antara mode pemikiran `adaptive` dan `enabled`/`disabled` akan merusak breakpoint cache untuk pesan. Prompt sistem dan definisi alat tetap di-cache terlepas dari perubahan mode.

### Menyetel perilaku pemikiran \{#tuning-thinking-behavior}

Perilaku pemicu pemikiran adaptif dapat diarahkan melalui prompt. Jika Claude berpikir lebih sering atau lebih jarang dari yang Anda inginkan, Anda dapat menambahkan panduan ke prompt sistem Anda:

```text
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality — typically for problems
that require multi-step reasoning. When in doubt, respond directly.
```

Untuk mendorong pemikiran sebagai gantinya, gunakan frasa seperti:

```text
This task involves multi-step reasoning. Think carefully before responding.
```

Efektivitas pengarahan dapat sensitif terhadap pilihan kata yang tepat — jika satu frasa tidak menghasilkan perilaku yang Anda inginkan, coba varian yang lebih langsung.

Anda juga dapat mengarahkan pemikiran per pesan dari giliran pengguna. Menambahkan `"Please think hard before responding."` ke pesan pengguna mendorong Claude untuk berpikir pada giliran tersebut; `"Answer directly without deliberating."` menekannya. Ini bekerja secara independen dari prompt sistem dan berguna ketika hanya beberapa permintaan dalam percakapan yang memerlukan penalaran diperpanjang.

<Warning>
Mengarahkan Claude untuk berpikir lebih jarang dapat mengurangi kualitas pada tugas yang mendapat manfaat dari penalaran. Ukur dampaknya pada beban kerja spesifik Anda sebelum menerapkan penyetelan berbasis prompt ke produksi. Pertimbangkan untuk menguji dengan [tingkat effort](/docs/id/build-with-claude/effort) yang lebih rendah terlebih dahulu.
</Warning>

### Kontrol biaya \{#cost-control}

Gunakan `max_tokens` sebagai batas keras pada total output (pemikiran + teks respons). Parameter `effort` memberikan panduan lunak tambahan tentang seberapa banyak pemikiran yang dialokasikan Claude. Bersama-sama, keduanya memberi Anda kontrol efektif atas biaya.

Pada tingkat effort `high` dan `max`, Claude mungkin berpikir lebih ekstensif dan lebih mungkin menghabiskan anggaran `max_tokens`. Jika Anda mengamati `stop_reason: "max_tokens"` dalam respons, pertimbangkan untuk meningkatkan `max_tokens` untuk memberi model lebih banyak ruang, atau menurunkan tingkat effort.

## Bekerja dengan blok pemikiran \{#working-with-thinking-blocks}

Konsep-konsep berikut berlaku untuk semua model yang mendukung pemikiran diperpanjang, terlepas dari apakah Anda menggunakan mode adaptif atau manual.

### Pemikiran yang diringkas \{#summarized-thinking}

Dengan pemikiran diperpanjang diaktifkan, Messages API untuk model Claude 4 mengembalikan ringkasan dari proses pemikiran lengkap Claude. Pemikiran yang diringkas memberikan manfaat kecerdasan penuh dari pemikiran diperpanjang, sekaligus mencegah penyalahgunaan. Ini adalah perilaku default pada model Claude 4 ketika field `display` pada konfigurasi thinking tidak disetel atau disetel ke `"summarized"`. Pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing), `display` secara default disetel ke `"omitted"`, sehingga Anda harus menyetel `display: "summarized"` secara eksplisit untuk menerima pemikiran yang diringkas.

Berikut adalah beberapa pertimbangan penting untuk pemikiran yang diringkas:

- Anda dikenakan biaya untuk token pemikiran penuh yang dihasilkan oleh permintaan asli, bukan token ringkasan.
- Jumlah token output yang ditagih **tidak akan sama** dengan jumlah token yang Anda lihat dalam respons.
- Pada model Claude 4, beberapa baris pertama dari output pemikiran lebih panjang dan rinci, memberikan penalaran mendetail yang sangat membantu untuk keperluan rekayasa prompt. [Claude Mythos Preview](https://anthropic.com/glasswing) meringkas sejak token pertama, sehingga blok pemikirannya tidak menampilkan pembukaan yang rinci ini.
- Karena Anthropic terus berupaya meningkatkan fitur pemikiran diperpanjang, perilaku peringkasan dapat berubah sewaktu-waktu.
- Peringkasan mempertahankan ide-ide kunci dari proses pemikiran Claude dengan latensi tambahan yang minimal, memungkinkan pengalaman pengguna yang dapat di-stream.
- Peringkasan diproses oleh model yang berbeda dari model yang Anda targetkan dalam permintaan Anda. Model pemikiran tidak melihat output yang diringkas.

<Note>
Dalam kasus yang jarang terjadi di mana Anda memerlukan akses ke output pemikiran penuh untuk model Claude 4, [hubungi tim penjualan Anthropic](mailto:sales@anthropic.com).
</Note>

### Mengontrol tampilan pemikiran \{#controlling-thinking-display}

Field `display` pada konfigurasi thinking mengontrol bagaimana konten thinking dikembalikan dalam respons API. Field ini menerima dua nilai:

- `"summarized"`: Blok thinking berisi teks thinking yang diringkas. Lihat [Summarized thinking](#summarized-thinking) untuk detailnya. Ini adalah nilai default pada Claude Opus 4.6, Claude Sonnet 4.6, dan model Claude 4 sebelumnya.
- `"omitted"`: Blok thinking dikembalikan dengan field `thinking` yang kosong. Field `signature` tetap membawa thinking lengkap yang terenkripsi untuk kontinuitas multi-turn (lihat [Thinking encryption](#thinking-encryption)). Ini adalah nilai default pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing).

Mengatur `display: "omitted"` berguna ketika aplikasi Anda tidak menampilkan konten thinking kepada pengguna. Manfaat utamanya adalah **time-to-first-text-token yang lebih cepat saat streaming:** Server melewati streaming token thinking sepenuhnya dan hanya mengirimkan signature, sehingga respons teks akhir mulai di-stream lebih cepat.

Berikut adalah beberapa pertimbangan penting untuk omitted thinking:

- Anda tetap dikenakan biaya untuk token thinking penuh. Menghilangkan thinking mengurangi latensi, bukan biaya.
- Jika Anda mengirimkan kembali blok thinking dalam percakapan multi-turn, kirimkan tanpa perubahan. Server mendekripsi `signature` untuk merekonstruksi thinking asli guna menyusun prompt (lihat [Preserving thinking blocks](/docs/id/build-with-claude/extended-thinking#preserving-thinking-blocks)). Teks apa pun yang Anda tempatkan di field `thinking` dari blok omitted yang dikirim ulang akan diabaikan.
- `display` tidak valid dengan `thinking.type: "disabled"` (tidak ada yang perlu ditampilkan).
- Saat menggunakan `thinking.type: "adaptive"` dan model melewati thinking untuk permintaan sederhana, tidak ada blok thinking yang dihasilkan terlepas dari nilai `display`.

<Note>
Field `signature` identik baik `display` bernilai `"summarized"` maupun `"omitted"`. Mengganti nilai `display` di antara giliran dalam sebuah percakapan didukung.
</Note>

<Note>
Pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7, `thinking.display` secara default adalah `"omitted"`. Blok pemikiran tetap muncul dalam stream respons, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, di mana default-nya adalah `"summarized"`. `display` hanya mengontrol visibilitas: pemikiran tetap terjadi dan ditagih sama di setiap pengaturan. Untuk menerima teks pemikiran yang diringkas pada model-model ini, setel `thinking.display` ke `"summarized"` secara eksplisit:

```python
thinking = {
    "type": "adaptive",
    "display": "summarized",
}
```
</Note>

Untuk contoh kode dan perilaku streaming dengan `display: "omitted"`, lihat [Mengontrol tampilan pemikiran](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display) di halaman pemikiran diperpanjang. Contoh di sana menggunakan `type: "enabled"`; dengan pemikiran adaptif, gunakan:

```python
thinking = {"type": "adaptive", "display": "omitted"}
```

### Enkripsi pemikiran \{#thinking-encryption}

Konten pemikiran lengkap dienkripsi dan dikembalikan dalam field `signature`. Field ini digunakan untuk memverifikasi bahwa blok pemikiran dihasilkan oleh Claude ketika dikirimkan kembali ke API.

<Note>
Mengirimkan kembali blok pemikiran hanya benar-benar diperlukan ketika menggunakan [alat dengan pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use). Jika tidak, Anda dapat menghilangkan blok pemikiran dari giliran sebelumnya. Jika Anda mengirimkannya kembali, apakah API menyimpan atau menghapusnya bergantung pada model: Opus 4.5+ dan Sonnet 4.6+ menyimpannya dalam konteks secara default; model Opus/Sonnet sebelumnya dan semua model Haiku menghapusnya. Lihat [pengeditan konteks](/docs/id/build-with-claude/context-editing) untuk mengonfigurasi hal ini.

Jika mengirimkan kembali blok pemikiran, kirimkan semuanya kembali persis seperti yang Anda terima demi konsistensi dan untuk menghindari potensi masalah.
</Note>

Berikut adalah beberapa pertimbangan penting tentang enkripsi pemikiran:
- Saat [melakukan streaming respons](/docs/id/build-with-claude/extended-thinking#streaming-thinking), signature ditambahkan melalui `signature_delta` di dalam event `content_block_delta` tepat sebelum event `content_block_stop`.
- Nilai `signature` secara signifikan lebih panjang pada model Claude 4 dibandingkan model sebelumnya.
- Field `signature` adalah field opaque dan tidak boleh diinterpretasikan atau di-parse.
- Nilai `signature` kompatibel di seluruh platform (API Claude, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)). Nilai yang dihasilkan di satu platform akan kompatibel dengan platform lainnya.

### Output pemikiran pada Claude Fable 5 dan Claude Mythos 5 \{#thinking-output-on-claude-fable-5-and-claude-mythos-5}

Pada Claude Fable 5 dan Claude Mythos 5, rantai pemikiran mentah tidak pernah dikembalikan. Blok pemikiran yang Anda terima adalah blok `thinking` biasa, bukan `redacted_thinking`, dan `thinking.display` bekerja sama seperti pada model lain: `"summarized"` mengembalikan ringkasan penalaran yang dapat dibaca, dan dengan `"omitted"` (default pada model-model ini), respons tetap menyertakan blok `thinking`, tetapi field `thinking` adalah string kosong. Untuk bentuk respons blok pemikiran, lihat [referensi Messages API](/docs/id/api/messages/create).

Saat melanjutkan percakapan pada model yang sama, kirim kembali setiap blok pemikiran ke API persis seperti yang diterima, termasuk blok yang field `thinking`-nya kosong. Jangan mengedit atau merekonstruksinya. Membaca teks ringkasan untuk ditampilkan tidak masalah: API menolak blok yang kontennya telah dimodifikasi, bukan blok yang telah Anda baca.

Blok pemikiran terikat pada model yang menghasilkannya. Model lain secara diam-diam mengabaikannya alih-alih menolak permintaan, tetapi blok yang diabaikan tetap menambah token input, jadi ketika Anda beralih model, misalnya setelah [fallback penolakan classifier](/docs/id/build-with-claude/refusals-and-fallback), hapus blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya. Pengecualiannya, yang dibahas dalam [Kredit fallback](/docs/id/build-with-claude/fallback-credit), adalah percobaan ulang kredit fallback (yang harus mengirim ulang body permintaan yang ditolak tanpa perubahan) dan blok `fallback` dari fallback di tengah output (yang tetap di tempat kemunculannya).

Pada Claude Fable 5, permintaan yang mencoba memancing penalaran internal model sebagai bagian dari teks respons dapat ditolak dengan `stop_details.category: "reasoning_extraction"`. Aplikasi yang memerlukan visibilitas penalaran sebaiknya membaca blok `thinking` yang dijelaskan di bagian ini alih-alih meminta penalaran dalam respons. Lihat [Kategori penolakan](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk referensi field dan panduan penanganan.

### Harga \{#pricing}

Untuk informasi harga lengkap termasuk tarif dasar, penulisan cache, cache hit, dan token output, lihat [halaman harga](/docs/id/about-claude/pricing).

Proses pemikiran dikenakan biaya untuk:
- Token yang digunakan selama pemikiran (token output)
- Blok pemikiran dari giliran asisten sebelumnya yang disimpan dalam konteks: hanya giliran terakhir pada model Opus/Sonnet yang lebih lama dan semua model Haiku; semua giliran secara default pada Opus 4.5+ dan Sonnet 4.6+ (token input)
- Token output teks standar

<Note>
Ketika pemikiran diperpanjang diaktifkan, prompt sistem khusus secara otomatis disertakan untuk mendukung fitur ini.
</Note>

Saat menggunakan pemikiran yang diringkas:
- **Token input:** Token dalam permintaan asli Anda (tidak termasuk token pemikiran dari giliran sebelumnya)
- **Token output (ditagih):** Token pemikiran asli yang dihasilkan Claude secara internal
- **Token output (terlihat):** Token pemikiran yang diringkas yang Anda lihat dalam respons
- **Tanpa biaya:** Token yang digunakan untuk menghasilkan ringkasan

Saat menggunakan `display: "omitted"`:
- **Token input:** Token dalam permintaan asli Anda (sama seperti yang diringkas)
- **Token output (ditagih):** Token pemikiran asli yang dihasilkan Claude secara internal (sama seperti yang diringkas)
- **Token output (terlihat):** Nol token pemikiran (field `thinking` kosong)

<Warning>
Jumlah token output yang ditagih **tidak** akan sama dengan jumlah token yang terlihat dalam respons. Anda ditagih untuk seluruh proses pemikiran, bukan konten pemikiran yang terlihat dalam respons.
</Warning>

Untuk melihat berapa banyak token output yang ditagih yang digunakan untuk penalaran internal, baca `usage.output_tokens_details.thinking_tokens` dalam respons. Nilai ini mencerminkan penalaran mentah yang dihasilkan model (bukan teks ringkasan yang dikembalikan dalam body) dan selalu kurang dari atau sama dengan `output_tokens`. Kurangi nilai ini dari `output_tokens` untuk memperkirakan bagian output yang bukan penalaran.

```json
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 348,
    "output_tokens_details": {
      "thinking_tokens": 312
    }
  }
}
```

`output_tokens` tetap menjadi total inklusif dan otoritatif yang digunakan untuk penagihan. `output_tokens_details` adalah rincian read-only untuk keperluan observabilitas.

### Topik tambahan \{#additional-topics}

Halaman pemikiran diperpanjang membahas beberapa topik secara lebih detail dengan contoh kode spesifik per mode:

- **[Penggunaan alat dengan pemikiran](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use)**: Aturan yang sama berlaku untuk pemikiran adaptif: pertahankan blok pemikiran di antara pemanggilan alat dan perhatikan batasan `tool_choice` saat pemikiran aktif.
- **[Caching prompt](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching)**: Dengan pemikiran adaptif, permintaan berturut-turut yang menggunakan mode pemikiran yang sama mempertahankan breakpoint cache. Beralih antara mode `adaptive` dan `enabled`/`disabled` merusak breakpoint cache untuk pesan (prompt sistem dan definisi alat tetap di-cache).
- **[Jendela konteks](/docs/id/build-with-claude/extended-thinking#max-tokens-and-context-window-size-with-extended-thinking)**: Bagaimana token pemikiran berinteraksi dengan `max_tokens` dan batas jendela konteks.

## Langkah selanjutnya \{#next-steps}

<CardGroup>
  <Card title="Pemikiran diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang pemikiran diperpanjang, termasuk mode manual, penggunaan alat, dan caching prompt.
  </Card>
  <Card title="Parameter effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol seberapa menyeluruh Claude merespons dengan parameter effort.
  </Card>
</CardGroup>