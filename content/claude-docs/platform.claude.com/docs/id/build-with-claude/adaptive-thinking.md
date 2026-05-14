---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/adaptive-thinking
fetched_at: 2026-05-14T03:14:07.437614Z
sha256: f9c276016a1f1807a54040c532edd35255b342bde2e28e0def4d012d4cc0a9e9
---

# Pemikiran adaptif

Biarkan Claude secara dinamis menentukan kapan dan berapa banyak menggunakan pemikiran yang diperluas dengan mode pemikiran adaptif.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Pemikiran adaptif adalah cara yang direkomendasikan untuk menggunakan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) dengan Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6, dan merupakan mode default pada [Claude Mythos Preview](https://anthropic.com/glasswing) (di mana ia secara otomatis diterapkan kapan pun `thinking` tidak diatur). Alih-alih secara manual menetapkan anggaran token pemikiran, pemikiran adaptif memungkinkan Claude secara dinamis menentukan kapan dan berapa banyak menggunakan pemikiran yang diperluas berdasarkan kompleksitas setiap permintaan. Pada Claude Opus 4.7, pemikiran adaptif adalah **satu-satunya** mode pemikiran yang didukung; manual `thinking: {type: "enabled", budget_tokens: N}` tidak lagi diterima.

<Tip>
Pemikiran adaptif dapat menghasilkan kinerja yang lebih baik daripada pemikiran yang diperluas dengan `budget_tokens` tetap untuk banyak beban kerja, terutama tugas bimodal dan alur kerja agentic jangka panjang. Tidak ada header beta yang diperlukan.

Jika beban kerja Anda memerlukan latensi yang dapat diprediksi atau kontrol presisi atas biaya pemikiran, pemikiran yang diperluas dengan `budget_tokens` masih berfungsi pada Claude Opus 4.6 dan Claude Sonnet 4.6 tetapi sudah usang dan tidak lagi direkomendasikan. Lihat peringatan di bawah.
</Tip>

## Model yang didukung

Pemikiran adaptif didukung pada model berikut:

- Claude Mythos Preview (`claude-mythos-preview`), pemikiran adaptif adalah default; `thinking: {type: "disabled"}` tidak didukung
- Claude Opus 4.7 (`claude-opus-4-7`), pemikiran adaptif adalah satu-satunya mode pemikiran yang didukung. Pemikiran dimatikan kecuali Anda secara eksplisit menetapkan `thinking: {type: "adaptive"}` dalam permintaan Anda; manual `thinking: {type: "enabled"}` ditolak dengan kesalahan 400.
- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)

<Warning>
`thinking.type: "enabled"` dan `budget_tokens` adalah [**usang**](/docs/id/build-with-claude/overview#feature-availability) pada Opus 4.6 dan Sonnet 4.6 dan akan dihapus dalam rilis model di masa depan. Gunakan `thinking.type: "adaptive"` dengan parameter `effort` sebagai gantinya. Konfigurasi `budget_tokens` yang ada masih berfungsi tetapi tidak lagi direkomendasikan; rencanakan untuk bermigrasi.

Model yang lebih lama (Sonnet 4.5, Opus 4.5, dll.) tidak mendukung pemikiran adaptif dan memerlukan `thinking.type: "enabled"` dengan `budget_tokens`.
</Warning>

## Cara kerja pemikiran adaptif

Dalam mode adaptif, pemikiran bersifat opsional untuk model. Claude mengevaluasi kompleksitas setiap permintaan dan menentukan apakah dan berapa banyak menggunakan pemikiran yang diperluas. Pada tingkat upaya default (`high`), Claude hampir selalu berpikir. Pada tingkat upaya yang lebih rendah, Claude dapat melewati pemikiran untuk masalah yang lebih sederhana.

Pemikiran adaptif juga secara otomatis mengaktifkan [pemikiran yang disisipi](/docs/id/build-with-claude/extended-thinking#interleaved-thinking). Ini berarti Claude dapat berpikir di antara panggilan alat, menjadikannya sangat efektif untuk alur kerja agentic.

## Cara menggunakan pemikiran adaptif

Atur `thinking.type` ke `"adaptive"` dalam permintaan API Anda:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-7",
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

```bash CLI
ant messages create \
  --model claude-opus-4-7 \
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
} as unknown as Anthropic.MessageCreateParamsNonStreaming);

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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model(Model.CLAUDE_OPUS_4_7)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 16000,
    messages: [
        [
            'role' => 'user',
            'content' => 'Explain why the sum of two even numbers is always even.'
        ]
    ],
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

## Pemikiran adaptif dengan parameter upaya

Anda dapat menggabungkan pemikiran adaptif dengan [parameter upaya](/docs/id/build-with-claude/effort) untuk memandu seberapa banyak Claude berpikir. Tingkat upaya bertindak sebagai panduan lembut untuk alokasi pemikiran Claude:

| Tingkat upaya | Perilaku pemikiran |
|:-------------|:------------------|
| `max` | Claude selalu berpikir tanpa batasan pada kedalaman pemikiran. Tersedia pada Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. |
| `xhigh` | Claude selalu berpikir mendalam dengan eksplorasi yang diperluas. Tersedia pada Claude Opus 4.7. |
| `high` (default) | Claude selalu berpikir. Memberikan penalaran mendalam pada tugas yang kompleks. |
| `medium` | Claude menggunakan pemikiran moderat. Mungkin melewati pemikiran untuk pertanyaan yang sangat sederhana. |
| `low` | Claude meminimalkan pemikiran. Melewati pemikiran untuk tugas sederhana di mana kecepatan paling penting. |

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-7",
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
  --transform 'content.0.text' --format yaml <<'YAML'
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
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
} as unknown as Anthropic.MessageCreateParamsNonStreaming);

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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model(Model.CLAUDE_OPUS_4_7)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the capital of France?']
    ],
    model: 'claude-opus-4-7',
    thinking: ['type' => 'adaptive'],
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
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

## Streaming dengan pemikiran adaptif

Pemikiran adaptif bekerja dengan mulus dengan [streaming](/docs/id/build-with-claude/streaming). Blok pemikiran dialirkan melalui acara `thinking_delta` seperti mode pemikiran manual:

<CodeGroup>
```bash CLI
ant messages create --stream --format jsonl \
  --model claude-opus-4-7 \
  --max-tokens 16000 \
  --thinking '{type: adaptive}' \
  --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-4-7",
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
  model: "claude-opus-4-7",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "What is the greatest common divisor of 1071 and 462?" }]
} as unknown as Anthropic.MessageStreamParams);

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
            Model = Model.ClaudeOpus4_7,
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
		Model:     anthropic.ModelClaudeOpus4_7,
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
            .model(Model.CLAUDE_OPUS_4_7)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$stream = $client->messages->createStream(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
    ],
    model: 'claude-opus-4-7',
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
  model: "claude-opus-4-7",
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

## Pemikiran adaptif vs manual vs dinonaktifkan

| Mode | Konfigurasi | Ketersediaan | Kapan digunakan |
|:-----|:-------|:-------------|:------------|
| **Adaptif** | `thinking: {type: "adaptive"}` | Claude Mythos Preview (default), Opus 4.7 (hanya mode), Opus 4.6, Sonnet 4.6 | Claude menentukan kapan dan berapa banyak menggunakan pemikiran yang diperluas. Gunakan `effort` untuk memandu. |
| **Manual** | `thinking: {type: "enabled", budget_tokens: N}` | Semua model kecuali Claude Opus 4.7 (ditolak). Usang pada Opus 4.6 dan Sonnet 4.6 (pertimbangkan mode adaptif sebagai gantinya). | Ketika Anda memerlukan kontrol presisi atas pengeluaran token pemikiran. |
| **Dinonaktifkan** | Hilangkan parameter `thinking` atau lewatkan `{type: "disabled"}` | Semua model kecuali Claude Mythos Preview | Ketika Anda tidak memerlukan pemikiran yang diperluas dan menginginkan latensi terendah. |

<Note>
Pemikiran adaptif tersedia pada Claude Mythos Preview, Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Pada Mythos Preview, pemikiran adaptif adalah default dan diterapkan secara otomatis kapan pun `thinking` tidak diatur. Pada Claude Opus 4.7, pemikiran adaptif adalah satu-satunya mode yang didukung dan `type: "enabled"` dengan `budget_tokens` ditolak. Model yang lebih lama hanya mendukung `type: "enabled"` dengan `budget_tokens`. Pada Opus 4.6 dan Sonnet 4.6, `type: "enabled"` dengan `budget_tokens` masih berfungsi tetapi usang.

**Ketersediaan pemikiran yang disisipi menurut mode:**
- **Mode adaptif:** Pemikiran yang disisipi secara otomatis diaktifkan pada Claude Mythos Preview, Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Pada Mythos Preview dan Opus 4.7, penalaran antar-alat selalu berada di dalam blok pemikiran.
- **Mode manual pada Sonnet 4.6:** Pemikiran yang disisipi bekerja melalui header beta `interleaved-thinking-2025-05-14`.
- **Mode manual pada Opus 4.6:** Pemikiran yang disisipi tidak tersedia. Jika alur kerja agentic Anda memerlukan pemikiran di antara panggilan alat pada Opus 4.6, gunakan mode adaptif.
</Note>

## Pertimbangan penting

### Perubahan validasi

Saat menggunakan pemikiran adaptif, giliran asisten sebelumnya tidak perlu dimulai dengan blok pemikiran. Ini lebih fleksibel daripada mode manual, di mana API memberlakukan bahwa giliran yang diaktifkan pemikiran dimulai dengan blok pemikiran.

### Caching prompt

Permintaan berturut-turut menggunakan pemikiran `adaptive` mempertahankan titik henti [cache prompt](/docs/id/build-with-claude/prompt-caching). Namun, beralih antara mode pemikiran `adaptive` dan `enabled`/`disabled` memecah titik henti cache untuk pesan. Prompt sistem dan definisi alat tetap di-cache terlepas dari perubahan mode.

### Menyetel perilaku pemikiran

Perilaku pemicu pemikiran adaptif dapat dipromptkan. Jika Claude berpikir lebih atau kurang sering daripada yang Anda inginkan, Anda dapat menambahkan panduan ke prompt sistem Anda:

```text
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality — typically for problems
that require multi-step reasoning. When in doubt, respond directly.
```

<Warning>
Mengarahkan Claude untuk berpikir lebih jarang dapat mengurangi kualitas pada tugas yang mendapat manfaat dari penalaran. Ukur dampak pada beban kerja spesifik Anda sebelum menerapkan penyesuaian berbasis prompt ke produksi. Pertimbangkan pengujian dengan [tingkat upaya](/docs/id/build-with-claude/effort) yang lebih rendah terlebih dahulu.
</Warning>

### Kontrol biaya

Gunakan `max_tokens` sebagai batas keras pada total output (pemikiran + teks respons). Parameter `effort` memberikan panduan lembut tambahan tentang berapa banyak pemikiran yang Claude alokasikan. Bersama-sama, ini memberi Anda kontrol yang efektif atas biaya.

Pada tingkat upaya `high` dan `max`, Claude mungkin berpikir lebih ekstensif dan dapat lebih mungkin menghabiskan anggaran `max_tokens`. Jika Anda mengamati `stop_reason: "max_tokens"` dalam respons, pertimbangkan untuk meningkatkan `max_tokens` untuk memberi model lebih banyak ruang, atau menurunkan tingkat upaya.

## Bekerja dengan blok pemikiran

Konsep berikut berlaku untuk semua model yang mendukung pemikiran yang diperluas, terlepas dari apakah Anda menggunakan mode adaptif atau manual.

### Pemikiran yang diringkas

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude's full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse. This is the default behavior on Claude 4 models when the `display` field on the thinking configuration is unset or set to `"summarized"`. On Claude Opus 4.7 and [Claude Mythos Preview](https://anthropic.com/glasswing), `display` defaults to `"omitted"` instead, so you must set `display: "summarized"` explicitly to receive summarized thinking.

Here are some important considerations for summarized thinking:

- You're charged for the full thinking tokens generated by the original request, not the summary tokens.
- The billed output token count will **not match** the count of tokens you see in the response.
- On Claude 4 models, the first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes. [Claude Mythos Preview](https://anthropic.com/glasswing) summarizes from the first token, so its thinking blocks do not show this verbose preamble.
- As Anthropic seeks to improve the extended thinking feature, summarization behavior is subject to change.
- Summarization preserves the key ideas of Claude's thinking process with minimal added latency, enabling a streamable user experience.
- Summarization is processed by a different model than the one you target in your requests. The thinking model does not see the summarized output.

<Note>
In rare cases where you need access to full thinking output for Claude 4 models, [contact our sales team](mailto:sales@anthropic.com).
</Note>

### Mengontrol tampilan pemikiran

The `display` field on the thinking configuration controls how thinking content is returned in API responses. It accepts two values:

- `"summarized"`: Thinking blocks contain summarized thinking text. See [Summarized thinking](#summarized-thinking) for details. This is the default on Claude Opus 4.6, Claude Sonnet 4.6, and earlier Claude 4 models.
- `"omitted"`: Thinking blocks are returned with an empty `thinking` field. The `signature` field still carries the encrypted full thinking for multi-turn continuity (see [Thinking encryption](#thinking-encryption)). This is the default on Claude Opus 4.7 and [Claude Mythos Preview](https://anthropic.com/glasswing).

Setting `display: "omitted"` is useful when your application doesn't surface thinking content to users. The primary benefit is **faster time-to-first-text-token when streaming:** The server skips streaming thinking tokens entirely and delivers only the signature, so the final text response begins streaming sooner.

Here are some important considerations for omitted thinking:

- You're still charged for the full thinking tokens. Omitting reduces latency, not cost.
- If you pass thinking blocks back in multi-turn conversations, pass them unchanged. The server decrypts the `signature` to reconstruct the original thinking for prompt construction (see [Preserving thinking blocks](/docs/en/build-with-claude/extended-thinking#preserving-thinking-blocks)). Any text you place in the `thinking` field of a round-tripped omitted block is ignored.
- `display` is invalid with `thinking.type: "disabled"` (there is nothing to display).
- When using `thinking.type: "adaptive"` and the model skips thinking for a simple request, no thinking block is produced regardless of `display`.

<Note>
The `signature` field is identical whether `display` is `"summarized"` or `"omitted"`. Switching `display` values between turns in a conversation is supported.
</Note>

<Note>
Pada Claude Opus 4.7, `thinking.display` default ke `"omitted"`. Blok pemikiran masih muncul dalam aliran respons, tetapi bidang `thinking` mereka kosong kecuali Anda secara eksplisit memilih. Ini adalah perubahan senyap dari Claude Opus 4.6, di mana default adalah `"summarized"`. Untuk mengembalikan teks pemikiran yang diringkas pada Claude Opus 4.7, atur `thinking.display` ke `"summarized"` secara eksplisit:

```python
thinking = {
    "type": "adaptive",
    "display": "summarized",
}
```
</Note>

Untuk contoh kode dan perilaku streaming dengan `display: "omitted"`, lihat [Mengontrol tampilan pemikiran](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display) di halaman pemikiran yang diperluas. Contoh di sana menggunakan `type: "enabled"`; dengan pemikiran adaptif, gunakan:

```python
thinking = {"type": "adaptive", "display": "omitted"}
```

### Enkripsi pemikiran

Full thinking content is encrypted and returned in the `signature` field. This field is used to verify that thinking blocks were generated by Claude when passed back to the API.

<Note>
It is only strictly necessary to send back thinking blocks when using [tools with extended thinking](/docs/en/build-with-claude/extended-thinking#extended-thinking-with-tool-use). Otherwise you can omit thinking blocks from previous turns. If you pass them back, whether the API keeps or strips them depends on the model: Opus 4.5+ and Sonnet 4.6+ keep them in context by default; earlier Opus/Sonnet models and all Haiku models strip them. See [context editing](/docs/en/build-with-claude/context-editing) to configure this.

If sending back thinking blocks, we recommend passing everything back as you received it for consistency and to avoid potential issues.
</Note>

Here are some important considerations on thinking encryption:
- When [streaming responses](/docs/en/build-with-claude/extended-thinking#streaming-thinking), the signature is added via a `signature_delta` inside a `content_block_delta` event just before the `content_block_stop` event.
- `signature` values are significantly longer in Claude 4 models than in previous models.
- The `signature` field is an opaque field and should not be interpreted or parsed.
- `signature` values are compatible across platforms (Claude APIs, [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock), and [Vertex AI](/docs/en/build-with-claude/claude-on-vertex-ai)). Values generated on one platform will be compatible with another.

### Harga

For complete pricing information including base rates, cache writes, cache hits, and output tokens, see the [pricing page](/docs/en/about-claude/pricing).

The thinking process incurs charges for:
- Tokens used during thinking (output tokens)
- Thinking blocks from prior assistant turns kept in context: only the last turn on earlier Opus/Sonnet models and all Haiku models; all turns by default on Opus 4.5+ and Sonnet 4.6+ (input tokens)
- Standard text output tokens

<Note>
When extended thinking is enabled, a specialized system prompt is automatically included to support this feature.
</Note>

When using summarized thinking:
- **Input tokens:** Tokens in your original request (excludes thinking tokens from previous turns)
- **Output tokens (billed):** The original thinking tokens that Claude generated internally
- **Output tokens (visible):** The summarized thinking tokens you see in the response
- **No charge:** Tokens used to generate the summary

When using `display: "omitted"`:
- **Input tokens:** Tokens in your original request (same as summarized)
- **Output tokens (billed):** The original thinking tokens that Claude generated internally (same as summarized)
- **Output tokens (visible):** Zero thinking tokens (the `thinking` field is empty)

<Warning>
The billed output token count will **not** match the visible token count in the response. You are billed for the full thinking process, not the thinking content visible in the response.
</Warning>

### Topik tambahan

Halaman pemikiran yang diperluas mencakup beberapa topik secara lebih detail dengan contoh kode khusus mode:

- **[Penggunaan alat dengan pemikiran](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use)**: Aturan yang sama berlaku untuk pemikiran adaptif: pertahankan blok pemikiran di antara panggilan alat dan waspadai keterbatasan `tool_choice` ketika pemikiran aktif.
- **[Caching prompt](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching)**: Dengan pemikiran adaptif, permintaan berturut-turut menggunakan mode pemikiran yang sama mempertahankan titik henti cache. Beralih antara mode `adaptive` dan `enabled`/`disabled` memecah titik henti cache untuk pesan (prompt sistem dan definisi alat tetap di-cache).
- **[Jendela konteks](/docs/id/build-with-claude/extended-thinking#max-tokens-and-context-window-size-with-extended-thinking)**: Bagaimana token pemikiran berinteraksi dengan batas `max_tokens` dan jendela konteks.

## Langkah berikutnya

<CardGroup>
  <Card title="Extended thinking" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang pemikiran yang diperluas, termasuk mode manual, penggunaan alat, dan caching prompt.
  </Card>
  <Card title="Effort parameter" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol seberapa menyeluruh Claude merespons dengan parameter upaya.
  </Card>
</CardGroup>