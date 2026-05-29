---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-05-29T03:17:00.216417Z
sha256: e64bfe281f1cf2ea4579a0d9989dab3ee2acda9217e0a1bd4a9401062f577fc1
---

# Membangun dengan extended thinking

Pelajari cara menggunakan extended thinking untuk meningkatkan kemampuan penalaran Claude dalam tugas-tugas kompleks

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Extended thinking memberikan Claude kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, sambil memberikan tingkat transparansi yang berbeda-beda ke dalam proses pemikiran langkah demi langkah sebelum memberikan jawaban akhirnya.

<Note>
Untuk Claude Opus 4.7 dan model yang lebih baru, gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dengan [parameter effort](/docs/id/build-with-claude/effort). Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak lagi didukung pada Claude Opus 4.7 atau model yang lebih baru dan mengembalikan error 400. Untuk Claude Opus 4.6 dan Claude Sonnet 4.6, adaptive thinking juga direkomendasikan; konfigurasi manual masih berfungsi pada model-model ini tetapi sudah usang dan akan dihapus dalam rilis model di masa depan.
</Note>

## Model yang didukung

Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) didukung pada semua model Claude saat ini **kecuali Claude Opus 4.7 dan model yang lebih baru**, di mana ini tidak lagi diterima dan mengembalikan error 400. Beberapa model memiliki perilaku khusus mode:

- **Claude Opus 4.7 (`claude-opus-4-7`) dan model yang lebih baru:** extended thinking manual tidak lagi didukung. Gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya.
- **[Claude Mythos Preview](https://anthropic.com/glasswing):** [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah default; `thinking: {type: "enabled", budget_tokens: N}` juga diterima. `thinking: {type: "disabled"}` tidak didukung, dan `display` default ke `"omitted"` daripada mengembalikan konten thinking. Lewatkan `display: "summarized"` untuk menerima ringkasan.
- **Claude Opus 4.6 (`claude-opus-4-6`):** [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) direkomendasikan; mode manual (`type: "enabled"`) sudah usang tetapi masih berfungsi.
- **Claude Sonnet 4.6 (`claude-sonnet-4-6`):** [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) direkomendasikan; mode manual (`type: "enabled"`) dengan [mode interleaved](#interleaved-thinking) sudah usang tetapi masih berfungsi.

<Note>
Perilaku API berbeda di seluruh model Claude Sonnet 3.7 dan Claude 4, tetapi bentuk API tetap sama persis.

Untuk informasi lebih lanjut, lihat [Perbedaan dalam thinking di seluruh versi model](#differences-in-thinking-across-model-versions).
</Note>

## Cara kerja extended thinking

Ketika extended thinking diaktifkan, Claude membuat blok konten `thinking` di mana ia mengeluarkan penalaran internalnya. Claude menggabungkan wawasan dari penalaran ini sebelum menyusun respons akhir.

Respons API mencakup blok konten `thinking`, diikuti oleh blok konten `text`.

Berikut adalah contoh format respons default:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

Untuk informasi lebih lanjut tentang format respons extended thinking, lihat [Referensi Messages API](/docs/id/api/messages/create).

## Cara menggunakan extended thinking

Berikut adalah contoh penggunaan extended thinking dalam Messages API:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
    },
    "messages": [
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        }
    ]
}'
```

```bash CLI
ant messages create \
  --transform content --format yaml \
    --model claude-sonnet-4-6 \
    --max-tokens 16000 \
    --thinking '{type: enabled, budget_tokens: 10000}' \
    --message '{role: user, content: Are there an infinite number of prime numbers such that n mod 4 == 3?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?",
        }
    ],
)

# The response contains summarized thinking blocks and text blocks
for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking summary: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [
    {
      role: "user",
      content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }
  ]
});

// The response contains summarized thinking blocks and text blocks
for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`\nThinking summary: ${block.thinking}`);
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
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
            Messages = [
                new() {
                    Role = Role.User,
                    Content = "Are there an infinite number of prime numbers such that n mod 4 == 3?"
                }
            ]
        };

        var message = await client.Messages.Create(parameters);

        foreach (var block in message.Content)
        {
            if (block.TryPickThinking(out ThinkingBlock? thinking))
            {
                Console.WriteLine($"\nThinking summary: {thinking.Thinking}");
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
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 16000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Are there an infinite number of prime numbers such that n mod 4 == 3?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	for _, block := range response.Content {
		switch v := block.AsAny().(type) {
		case anthropic.ThinkingBlock:
			fmt.Printf("\nThinking summary: %s", v.Thinking)
		case anthropic.TextBlock:
			fmt.Printf("\nResponse: %s", v.Text)
		}
	}
}
```

```java Java hidelines={1..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;

public class ExtendedThinkingExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(16000L)
            .enabledThinking(10000L)
            .addUserMessage("Are there an infinite number of prime numbers such that n mod 4 == 3?")
            .build();

        Message response = client.messages().create(params);

        response.content().forEach(block -> {
            block.thinking().ifPresent(thinkingBlock ->
                System.out.println("\nThinking summary: " + thinkingBlock.thinking())
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
            'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?'
        ]
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
);

foreach ($message->content as $block) {
    if ($block->type === 'thinking') {
        echo "\nThinking summary: " . $block->thinking;
    } elseif ($block->type === 'text') {
        echo "\nResponse: " . $block->text;
    }
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [
    {
      role: "user",
      content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    }
  ]
)

message.content.each do |block|
  case block.type
  when :thinking
    puts "\nThinking summary: #{block.thinking}"
  when :text
    puts "\nResponse: #{block.text}"
  end
end
```

</CodeGroup>

Untuk mengaktifkan extended thinking, tambahkan objek `thinking`, dengan parameter `type` diatur ke `enabled` dan `budget_tokens` ke anggaran token yang ditentukan untuk extended thinking. Untuk Claude Opus 4.6 dan Claude Sonnet 4.6, gunakan `type: "adaptive"` sebagai gantinya. Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) untuk detail. Meskipun `type: "enabled"` dengan `budget_tokens` masih berfungsi pada model-model ini, ini sudah usang dan akan dihapus dalam rilis di masa depan.

Parameter `budget_tokens` menentukan jumlah maksimum token yang diizinkan Claude gunakan untuk proses penalaran internalnya. Dalam model Claude 4 dan yang lebih baru, batas ini berlaku untuk token thinking penuh, dan bukan untuk [output ringkasan](#summarized-thinking). Anggaran yang lebih besar dapat meningkatkan kualitas respons dengan memungkinkan analisis yang lebih menyeluruh untuk masalah kompleks, meskipun Claude mungkin tidak menggunakan seluruh anggaran yang dialokasikan, terutama pada rentang di atas 32k.

<Warning>
`budget_tokens` adalah [usang](/docs/id/build-with-claude/overview#feature-availability) pada Claude Opus 4.6 dan Claude Sonnet 4.6 dan akan dihapus dalam rilis model di masa depan. Gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking sebagai gantinya.
</Warning>

<Note>
[Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, dan Claude Opus 4.6 mendukung hingga 128k token output. Claude Sonnet 4.6 dan Claude Haiku 4.5 mendukung hingga 64k. Lihat [gambaran umum model](/docs/id/about-claude/models/overview) untuk batas pada model legacy. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), [beta header](/docs/id/api/beta-headers) `output-300k-2026-03-24` menaikkan batas output ke 300k untuk Opus 4.7, Opus 4.6, dan Sonnet 4.6.
</Note>

`budget_tokens` harus diatur ke nilai yang kurang dari `max_tokens`. Namun, ketika menggunakan [interleaved thinking dengan tools](#interleaved-thinking), Anda dapat melampaui batas ini karena batas token menjadi seluruh jendela konteks Anda.

### Summarized thinking

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude's full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse. This is the default behavior on Claude 4 models when the `display` field on the thinking configuration is unset or set to `"summarized"`. On Claude Opus 4.8, Claude Opus 4.7, and [Claude Mythos Preview](https://anthropic.com/glasswing), `display` defaults to `"omitted"` instead, so you must set `display: "summarized"` explicitly to receive summarized thinking.

Here are some important considerations for summarized thinking:

- You're charged for the full thinking tokens generated by the original request, not the summary tokens.
- The billed output token count will **not match** the count of tokens you see in the response.
- On Claude 4 models, the first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes. [Claude Mythos Preview](https://anthropic.com/glasswing) summarizes from the first token, so its thinking blocks do not show this verbose preamble.
- As Anthropic seeks to improve the extended thinking feature, summarization behavior is subject to change.
- Summarization preserves the key ideas of Claude's thinking process with minimal added latency, enabling a streamable user experience.
- Summarization is processed by a different model than the one you target in your requests. The thinking model does not see the summarized output.

<Note>
In rare cases where you need access to full thinking output for Claude 4 models, [contact Anthropic sales](mailto:sales@anthropic.com).
</Note>

### Mengontrol tampilan thinking

The `display` field on the thinking configuration controls how thinking content is returned in API responses. It accepts two values:

- `"summarized"`: Thinking blocks contain summarized thinking text. See [Summarized thinking](#summarized-thinking) for details. This is the default on Claude Opus 4.6, Claude Sonnet 4.6, and earlier Claude 4 models.
- `"omitted"`: Thinking blocks are returned with an empty `thinking` field. The `signature` field still carries the encrypted full thinking for multi-turn continuity (see [Thinking encryption](#thinking-encryption)). This is the default on Claude Opus 4.8, Claude Opus 4.7, and [Claude Mythos Preview](https://anthropic.com/glasswing).

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
Pada [Claude Mythos Preview](https://anthropic.com/glasswing), `display` default ke `"omitted"`. Contoh-contoh di bagian ini melewatkan `display` secara eksplisit sehingga mereka berlaku untuk semua model, tetapi pada Mythos Preview Anda dapat membiarkannya tidak diatur dan menerima perilaku yang sama. Untuk menerima summarized thinking pada Mythos Preview, atur `display: "summarized"` secara eksplisit.
</Note>

Pipeline otomatis yang tidak pernah menampilkan konten thinking kepada pengguna akhir dapat melewati overhead menerima token thinking melalui wire. Aplikasi yang sensitif terhadap latensi mendapatkan kualitas penalaran yang sama tanpa menunggu teks thinking untuk streaming sebelum respons akhir dimulai.

<Tabs>
<Tab title="Shell">
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16000,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000,
        "display": "omitted"
    },
    "messages": [
        {
            "role": "user",
            "content": "What is 27 * 453?"
        }
    ]
}'
```
</Tab>

<Tab title="CLI">
```bash CLI
ant messages create \
  --model claude-sonnet-4-6 \
  --max-tokens 16000 \
  --transform content --format yaml \
    --thinking '{type: enabled, budget_tokens: 10000, display: omitted}' \
    --message '{role: user, content: "What is 27 * 453?"}'
```
</Tab>

<Tab title="Python">
```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000,
        "display": "omitted",
    },
    messages=[
        {"role": "user", "content": "What is 27 * 453?"},
    ],
)

for block in response.content:
    if block.type == "thinking":
        if block.thinking:
            print(f"Thinking: {block.thinking}")
        else:
            print("Thinking: [omitted]")
    elif block.type == "text":
        print(f"Response: {block.text}")
```
</Tab>

<Tab title="TypeScript">
<Note>
Tipe SDK TypeScript belum menyertakan `display`. Penegasan tipe melewatkannya pada runtime; SDK meneruskan parameter yang tidak dikenal ke API.
</Note>
```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000,
    display: "omitted"
  },
  messages: [
    {
      role: "user",
      content: "What is 27 * 453?"
    }
  ]
} as unknown as Anthropic.MessageCreateParamsNonStreaming);

for (const block of response.content) {
  if (block.type === "thinking") {
    if (block.thinking) {
      console.log(`Thinking: ${block.thinking}`);
    } else {
      console.log("Thinking: [omitted]");
    }
  } else if (block.type === "text") {
    console.log(`Response: ${block.text}`);
  }
}
```
</Tab>

<Tab title="C#">
<Note>
Dukungan SDK asli untuk field `display` akan segera hadir. Sampai saat itu, Anda dapat menggunakan permintaan HTTP langsung:
</Note>
```csharp C# hidelines={1..10,-2..-1}
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        var client = new HttpClient();
        client.DefaultRequestHeaders.Add("x-api-key", Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY"));
        client.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");

        var body = """
        {
            "model": "claude-sonnet-4-6",
            "max_tokens": 16000,
            "thinking": {
                "type": "enabled",
                "budget_tokens": 10000,
                "display": "omitted"
            },
            "messages": [
                {"role": "user", "content": "What is 27 * 453?"}
            ]
        }
        """;

        var response = await client.PostAsync(
            "https://api.anthropic.com/v1/messages",
            new StringContent(body, Encoding.UTF8, "application/json"));

        var json = await response.Content.ReadAsStringAsync();
        var doc = JsonDocument.Parse(json);
        foreach (var block in doc.RootElement.GetProperty("content").EnumerateArray())
        {
            var type = block.GetProperty("type").GetString();
            if (type == "thinking")
            {
                var thinking = block.GetProperty("thinking").GetString();
                Console.WriteLine($"Thinking: {(string.IsNullOrEmpty(thinking) ? "[omitted]" : thinking)}");
            }
            else if (type == "text")
            {
                Console.WriteLine($"Response: {block.GetProperty("text").GetString()}");
            }
        }
    }
}
```
</Tab>

<Tab title="Go">
<Note>
Dukungan SDK asli untuk field `display` akan segera hadir. Sampai saat itu, Anda dapat menggunakan permintaan HTTP langsung:
</Note>
```go Go hidelines={1..12,-1}
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	body := []byte(`{
		"model": "claude-sonnet-4-6",
		"max_tokens": 16000,
		"thinking": {
			"type": "enabled",
			"budget_tokens": 10000,
			"display": "omitted"
		},
		"messages": [
			{"role": "user", "content": "What is 27 * 453?"}
		]
	}`)

	req, _ := http.NewRequest("POST", "https://api.anthropic.com/v1/messages", bytes.NewBuffer(body))
	req.Header.Set("x-api-key", os.Getenv("ANTHROPIC_API_KEY"))
	req.Header.Set("anthropic-version", "2023-06-01")
	req.Header.Set("content-type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	respBody, _ := io.ReadAll(resp.Body)

	var result map[string]any
	json.Unmarshal(respBody, &result)
	for _, block := range result["content"].([]any) {
		b := block.(map[string]any)
		if b["type"] == "thinking" {
			thinking := b["thinking"].(string)
			if thinking == "" {
				fmt.Println("Thinking: [omitted]")
			} else {
				fmt.Println("Thinking:", thinking)
			}
		} else if b["type"] == "text" {
			fmt.Println("Response:", b["text"])
		}
	}
}
```
</Tab>

<Tab title="Java">
<Note>
Dukungan SDK asli untuk field `display` akan segera hadir. Sampai saat itu, Anda dapat menggunakan permintaan HTTP langsung:
</Note>
```java Java hidelines={1..9,-2..-1}
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.JSONArray;
import org.json.JSONObject;

public class ThinkingDisplay {
    public static void main(String[] args) throws Exception {
        String body = """
            {
                "model": "claude-sonnet-4-6",
                "max_tokens": 16000,
                "thinking": {
                    "type": "enabled",
                    "budget_tokens": 10000,
                    "display": "omitted"
                },
                "messages": [
                    {"role": "user", "content": "What is 27 * 453?"}
                ]
            }
            """;

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.anthropic.com/v1/messages"))
            .header("x-api-key", System.getenv("ANTHROPIC_API_KEY"))
            .header("anthropic-version", "2023-06-01")
            .header("content-type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();

        HttpResponse<String> response = HttpClient.newHttpClient()
            .send(request, HttpResponse.BodyHandlers.ofString());

        JSONObject json = new JSONObject(response.body());
        JSONArray content = json.getJSONArray("content");
        for (int i = 0; i < content.length(); i++) {
            JSONObject block = content.getJSONObject(i);
            String type = block.getString("type");
            if (type.equals("thinking")) {
                String thinking = block.getString("thinking");
                System.out.println("Thinking: " + (thinking.isEmpty() ? "[omitted]" : thinking));
            } else if (type.equals("text")) {
                System.out.println("Response: " + block.getString("text"));
            }
        }
    }
}
```
</Tab>

<Tab title="PHP">
<Note>
Dukungan SDK asli untuk field `display` akan segera hadir. Sampai saat itu, Anda dapat menggunakan permintaan HTTP langsung:
</Note>
```php PHP hidelines={1..2}
<?php

$body = json_encode([
    "model" => "claude-sonnet-4-6",
    "max_tokens" => 16000,
    "thinking" => [
        "type" => "enabled",
        "budget_tokens" => 10000,
        "display" => "omitted",
    ],
    "messages" => [
        ["role" => "user", "content" => "What is 27 * 453?"],
    ],
]);

$ch = curl_init("https://api.anthropic.com/v1/messages");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "x-api-key: " . getenv("ANTHROPIC_API_KEY"),
    "anthropic-version: 2023-06-01",
    "content-type: application/json",
]);

$response = json_decode(curl_exec($ch), true);
curl_close($ch);

foreach ($response["content"] as $block) {
    if ($block["type"] === "thinking") {
        $thinking = $block["thinking"];
        echo "Thinking: " . ($thinking === "" ? "[omitted]" : $thinking) . "\n";
    } elseif ($block["type"] === "text") {
        echo "Response: " . $block["text"] . "\n";
    }
}
```
</Tab>

<Tab title="Ruby">
<Note>
Dukungan SDK asli untuk field `display` akan segera hadir. Sampai saat itu, Anda dapat menggunakan permintaan HTTP langsung:
</Note>
```ruby Ruby
require "net/http"
require "json"
require "uri"

uri = URI("https://api.anthropic.com/v1/messages")
body = {
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000,
    display: "omitted"
  },
  messages: [
    { role: "user", content: "What is 27 * 453?" }
  ]
}

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
request = Net::HTTP::Post.new(uri)
request["x-api-key"] = ENV["ANTHROPIC_API_KEY"]
request["anthropic-version"] = "2023-06-01"
request["content-type"] = "application/json"
request.body = body.to_json

response = JSON.parse(http.request(request).body)
response["content"].each do |block|
  if block["type"] == "thinking"
    thinking = block["thinking"]
    puts "Thinking: #{thinking.empty? ? '[omitted]' : thinking}"
  elsif block["type"] == "text"
    puts "Response: #{block['text']}"
  end
end
```
</Tab>
</Tabs>

Ketika `display: "omitted"` diatur, respons berisi blok `thinking` dengan field `thinking` kosong:

```json Output
{
  "content": [
    {
      "type": "thinking",
      "thinking": "",
      "signature": "EosnCkYICxIMMb3LzNrMu..."
    },
    {
      "type": "text",
      "text": "The answer is 12,231."
    }
  ]
}
```

Ketika streaming dengan `display: "omitted"`, tidak ada event `thinking_delta` yang dipancarkan; lihat [Streaming thinking](#streaming-thinking) di bawah untuk urutan event.

### Streaming pemikiran

Anda dapat melakukan streaming respons pemikiran yang diperluas menggunakan [server-sent events (SSE)](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents).

Ketika streaming diaktifkan untuk pemikiran yang diperluas, Anda menerima konten pemikiran melalui acara `thinking_delta`.

Ketika `display: "omitted"` diatur, tidak ada acara `thinking_delta` yang dipancarkan. Lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display).

Untuk dokumentasi lebih lanjut tentang streaming melalui Messages API, lihat [Streaming Messages](/docs/id/build-with-claude/streaming).

Berikut adalah cara menangani streaming dengan pemikiran:

<CodeGroup tryInConsole={{ userPrompt: "What is the greatest common divisor of 1071 and 462?", thinkingBudgetTokens: 16000 }}>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16000,
    "stream": true,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
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
  --model claude-sonnet-4-6 \
  --max-tokens 16000 \
  --thinking '{type: enabled, budget_tokens: 10000}' \
  --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[
        {
            "role": "user",
            "content": "What is the greatest common divisor of 1071 and 462?",
        }
    ],
) as stream:
    thinking_started = False
    response_started = False

    for event in stream:
        if event.type == "content_block_start":
            print(f"\nStarting {event.content_block.type} block...")
            # Reset flags for each new block
            thinking_started = False
            response_started = False
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                if not thinking_started:
                    print("Thinking: ", end="", flush=True)
                    thinking_started = True
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                if not response_started:
                    print("Response: ", end="", flush=True)
                    response_started = True
                print(event.delta.text, end="", flush=True)
        elif event.type == "content_block_stop":
            print("\nBlock complete.")
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = await client.messages.stream({
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [
    {
      role: "user",
      content: "What is the greatest common divisor of 1071 and 462?"
    }
  ]
});

let thinkingStarted = false;
let responseStarted = false;

for await (const event of stream) {
  if (event.type === "content_block_start") {
    console.log(`\nStarting ${event.content_block.type} block...`);
    // Reset flags for each new block
    thinkingStarted = false;
    responseStarted = false;
  } else if (event.type === "content_block_delta") {
    if (event.delta.type === "thinking_delta") {
      if (!thinkingStarted) {
        process.stdout.write("Thinking: ");
        thinkingStarted = true;
      }
      process.stdout.write(event.delta.thinking);
    } else if (event.delta.type === "text_delta") {
      if (!responseStarted) {
        process.stdout.write("Response: ");
        responseStarted = true;
      }
      process.stdout.write(event.delta.text);
    }
  } else if (event.type === "content_block_stop") {
    console.log("\nBlock complete.");
  }
}
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main()
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
            Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
        };

        bool thinkingStarted = false;
        bool responseStarted = false;

        await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
        {
            if (streamEvent.TryPickContentBlockStart(out var blockStart))
            {
                Console.WriteLine($"\nStarting {blockStart.ContentBlock.Type} block...");
                thinkingStarted = false;
                responseStarted = false;
            }
            else if (streamEvent.TryPickContentBlockDelta(out var blockDelta))
            {
                if (blockDelta.Delta.TryPickThinking(out var thinkingDelta))
                {
                    if (!thinkingStarted)
                    {
                        Console.Write("Thinking: ");
                        thinkingStarted = true;
                    }
                    Console.Write(thinkingDelta.Thinking);
                }
                else if (blockDelta.Delta.TryPickText(out var textDelta))
                {
                    if (!responseStarted)
                    {
                        Console.Write("Response: ");
                        responseStarted = true;
                    }
                    Console.Write(textDelta.Text);
                }
            }
            else if (streamEvent.TryPickContentBlockStop(out _))
            {
                Console.WriteLine("\nBlock complete.");
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

	stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 16000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
		},
	})

	thinkingStarted := false
	responseStarted := false

	for stream.Next() {
		event := stream.Current()
		switch eventVariant := event.AsAny().(type) {
		case anthropic.ContentBlockStartEvent:
			fmt.Printf("\nStarting %s block...\n", eventVariant.ContentBlock.Type)
			thinkingStarted = false
			responseStarted = false
		case anthropic.ContentBlockDeltaEvent:
			switch deltaVariant := eventVariant.Delta.AsAny().(type) {
			case anthropic.ThinkingDelta:
				if !thinkingStarted {
					fmt.Print("Thinking: ")
					thinkingStarted = true
				}
				fmt.Print(deltaVariant.Thinking)
			case anthropic.TextDelta:
				if !responseStarted {
					fmt.Print("Response: ")
					responseStarted = true
				}
				fmt.Print(deltaVariant.Text)
			}
		case anthropic.ContentBlockStopEvent:
			fmt.Println("\nBlock complete.")
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
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(16000L)
            .enabledThinking(10000L)
            .addUserMessage("What is the greatest common divisor of 1071 and 462?")
            .build();

        try (var streamResponse = client.messages().createStreaming(params)) {
            streamResponse.stream().forEach(event -> {
                event.contentBlockStart().ifPresent(startEvent ->
                    System.out.println("\nStarting block...")
                );
                event.contentBlockDelta().ifPresent(deltaEvent -> {
                    deltaEvent.delta().thinking().ifPresent(td ->
                        System.out.print(td.thinking())
                    );
                    deltaEvent.delta().text().ifPresent(td ->
                        System.out.print(td.text())
                    );
                });
                event.contentBlockStop().ifPresent(stopEvent ->
                    System.out.println("\nBlock complete.")
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

$thinkingStarted = false;
$responseStarted = false;

$stream = $client->messages->createStream(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
);

foreach ($stream as $event) {
    if ($event->type === 'content_block_start') {
        echo "\nStarting {$event->contentBlock->type} block...\n";
        $thinkingStarted = false;
        $responseStarted = false;
    } elseif ($event->type === 'content_block_delta') {
        if ($event->delta->type === 'thinking_delta') {
            if (!$thinkingStarted) {
                echo "Thinking: ";
                $thinkingStarted = true;
            }
            echo $event->delta->thinking;
        } elseif ($event->delta->type === 'text_delta') {
            if (!$responseStarted) {
                echo "Response: ";
                $responseStarted = true;
            }
            echo $event->delta->text;
        }
    } elseif ($event->type === 'content_block_stop') {
        echo "\nBlock complete.\n";
    }
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

thinking_started = false
response_started = false

stream = client.messages.stream(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  messages: [
    { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
  ]
)

stream.each do |event|
  case event.type
  when :content_block_start
    puts "\nStarting #{event.content_block.type} block..."
    thinking_started = false
    response_started = false
  when :content_block_delta
    if event.delta.type == :thinking_delta
      unless thinking_started
        print "Thinking: "
        thinking_started = true
      end
      print event.delta.thinking
    elsif event.delta.type == :text_delta
      unless response_started
        print "Response: "
        response_started = true
      end
      print event.delta.text
    end
  when :content_block_stop
    puts "\nBlock complete."
  end
end
```

</CodeGroup>

Contoh output streaming:
```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-sonnet-4-6", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21\n147 = 7 × 21 + 0\n\nSo GCD(1071, 462) = 21"}}

// Additional thinking deltas...

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

// Additional text deltas...

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

Ketika `display: "omitted"` diatur, blok pemikiran terbuka, satu `signature_delta` tiba, dan blok ditutup tanpa acara `thinking_delta` apa pun. Streaming teks dimulai segera setelah:

```sse Output
event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"thinking","thinking":"","signature":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"signature_delta","signature":"EosnCkYICxIMMb3LzNrMu..."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"text","text":""}}
```

<Note>
Saat menggunakan streaming dengan pemikiran yang diaktifkan, Anda mungkin memperhatikan bahwa teks kadang-kadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token demi token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten pemikiran.

Sistem streaming perlu memproses konten dalam batch untuk kinerja optimal, yang dapat menghasilkan pola pengiriman "chunky" ini, dengan kemungkinan penundaan antara acara streaming. Anthropic terus bekerja untuk meningkatkan pengalaman ini, dengan pembaruan di masa depan berfokus pada membuat konten pemikiran melakukan streaming dengan lebih lancar.
</Note>

## Pemikiran yang diperluas dengan penggunaan alat

Pemikiran yang diperluas dapat digunakan bersama dengan [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude untuk bernalar melalui pemilihan alat dan pemrosesan hasil.

Saat menggunakan pemikiran yang diperluas dengan penggunaan alat, perhatikan batasan berikut:

1. **Batasan pilihan alat**: Penggunaan alat dengan pemikiran hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` akan menghasilkan kesalahan karena opsi ini memaksa penggunaan alat, yang tidak kompatibel dengan pemikiran yang diperluas.

2. **Melestarikan blok pemikiran**: Selama penggunaan alat, Anda harus melewatkan blok `thinking` kembali ke API untuk pesan asisten terakhir. Sertakan blok yang tidak dimodifikasi sepenuhnya kembali ke API untuk mempertahankan kontinuitas penalaran.

### Mengalihkan mode pemikiran dalam percakapan

Anda tidak dapat mengalihkan pemikiran di tengah giliran asisten, termasuk selama loop penggunaan alat. Seluruh giliran asisten harus beroperasi dalam satu mode pemikiran:

- **Jika pemikiran diaktifkan**, giliran asisten akhir harus dimulai dengan blok pemikiran.
- **Jika pemikiran dinonaktifkan**, giliran asisten akhir tidak boleh berisi blok pemikiran apa pun

Dari perspektif model, **loop penggunaan alat adalah bagian dari giliran asisten**. Giliran asisten tidak selesai sampai Claude menyelesaikan respons penuhnya, yang mungkin mencakup beberapa panggilan alat dan hasil.

Sebagai contoh, urutan ini semuanya adalah bagian dari **satu giliran asisten**:
```text
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Meskipun ada beberapa pesan API, loop penggunaan alat secara konseptual adalah bagian dari satu respons asisten yang berkelanjutan.

#### Degradasi pemikiran yang elegan

Ketika konflik pemikiran pertengahan giliran terjadi (seperti mengalihkan pemikiran aktif atau nonaktif selama loop penggunaan alat), API secara otomatis menonaktifkan pemikiran untuk permintaan tersebut. Untuk mempertahankan kualitas model dan tetap pada distribusi, API dapat:

- Menghapus blok pemikiran dari percakapan ketika mereka akan membuat struktur giliran yang tidak valid
- Menonaktifkan pemikiran untuk permintaan saat ini ketika riwayat percakapan tidak kompatibel dengan pemikiran yang diaktifkan

Ini berarti bahwa mencoba mengalihkan pemikiran pertengahan giliran tidak akan menyebabkan kesalahan, tetapi pemikiran akan diam-diam dinonaktifkan untuk permintaan tersebut. Untuk mengonfirmasi apakah pemikiran aktif, periksa kehadiran blok `thinking` dalam respons.

#### Panduan praktis

**Praktik terbaik**: Rencanakan strategi pemikiran Anda di awal setiap giliran daripada mencoba mengalihkan pertengahan giliran.

**Contoh: Mengalihkan pemikiran setelah menyelesaikan giliran**
```text
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Dengan menyelesaikan giliran asisten sebelum mengalihkan pemikiran, Anda memastikan bahwa pemikiran benar-benar diaktifkan untuk permintaan baru.

<Note>
Mengalihkan mode pemikiran juga membatalkan penyimpanan cache prompt untuk riwayat pesan. Untuk detail lebih lanjut, lihat bagian [Extended thinking dengan penyimpanan cache prompt](#extended-thinking-with-prompt-caching).
</Note>

<section title="Contoh: Meneruskan blok pemikiran dengan hasil alat">

Berikut adalah contoh praktis yang menunjukkan cara mempertahankan blok pemikiran saat memberikan hasil alat:

<CodeGroup>
```bash CLI
ant messages create --transform content <<'YAML'
model: claude-sonnet-4-6
max_tokens: 16000
thinking:
  type: enabled
  budget_tokens: 10000
tools:
  - name: get_weather
    description: Get current weather for a location
    input_schema:
      type: object
      properties:
        location:
          type: string
      required:
        - location
messages:
  - role: user
    content: "What's the weather in Paris?"
YAML
```

```python Python
weather_tool = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
}

# First request - Claude responds with thinking and tool request
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
```

```typescript TypeScript
const weatherTool: Anthropic.Tool = {
  name: "get_weather",
  description: "Get current weather for a location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string" }
    },
    required: ["location"]
  }
};

// First request - Claude responds with thinking and tool request
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weatherTool],
  messages: [{ role: "user", content: "What's the weather in Paris?" }]
});
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

        var weatherTool = new ToolUnion(new Tool()
        {
            Name = "get_weather",
            Description = "Get current weather for a location",
            InputSchema = new InputSchema()
            {
                Properties = new Dictionary<string, JsonElement>
                {
                    ["location"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                },
                Required = ["location"],
            },
        });

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
            Tools = [weatherTool],
            Messages = [new() { Role = Role.User, Content = "What's the weather in Paris?" }]
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

	weatherTool := anthropic.ToolUnionParam{
		OfTool: &anthropic.ToolParam{
			Name:        "get_weather",
			Description: anthropic.String("Get current weather for a location"),
			InputSchema: anthropic.ToolInputSchemaParam{
				Properties: map[string]any{
					"location": map[string]any{
						"type": "string",
					},
				},
				Required: []string{"location"},
			},
		},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 16000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
		Tools:     []anthropic.ToolUnionParam{weatherTool},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..12,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.core.JsonValue;
import java.util.List;
import java.util.Map;

public class ExtendedThinkingWithTools {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(16000L)
            .enabledThinking(10000L)
            .addTool(Tool.builder()
                .name("get_weather")
                .description("Get current weather for a location")
                .inputSchema(Tool.InputSchema.builder()
                    .properties(JsonValue.from(Map.of(
                        "location", Map.of("type", "string")
                    )))
                    .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                    .build())
                .build())
            .addUserMessage("What's the weather in Paris?")
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$weatherTool = [
    'name' => 'get_weather',
    'description' => 'Get current weather for a location',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'location' => ['type' => 'string']
        ],
        'required' => ['location']
    ]
];

$message = $client->messages->create(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => "What's the weather in Paris?"]
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
    tools: [$weatherTool],
);
echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

weather_tool = {
  name: "get_weather",
  description: "Get current weather for a location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string" }
    },
    required: ["location"]
  }
}

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weather_tool],
  messages: [
    { role: "user", content: "What's the weather in Paris?" }
  ]
)
puts message
```

</CodeGroup>

Respons API mencakup blok pemikiran, teks, dan tool_use:

```json Output
{
  "content": [
    {
      "type": "thinking",
      "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
      "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5TILnCrrUXoKiiNBZW9P+nr8XSj1zuZzAl4egiCCpQNvfyUuFFJP5CncdYZEQPPmLxYsNrcs...."
    },
    {
      "type": "text",
      "text": "I can help you get the current weather information for Paris. Let me check that for you"
    },
    {
      "type": "tool_use",
      "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
      "name": "get_weather",
      "input": {
        "location": "Paris"
      }
    }
  ]
}
```

Sekarang mari kita lanjutkan percakapan dan gunakan alat

<CodeGroup>
```bash CLI
# First turn: capture the assistant content array (thinking + tool_use,
# with signatures intact) as compact JSON.
ASSISTANT_CONTENT=$(ant messages create \
  --transform content <<'YAML'
model: claude-sonnet-4-6
max_tokens: 16000
thinking:
  type: enabled
  budget_tokens: 10000
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state
      required: [location]
messages:
  - role: user
    content: What's the weather in Paris?
YAML
)

TOOL_USE_ID=$(printf '%s' "$ASSISTANT_CONTENT" \
  | grep -o 'toolu_[A-Za-z0-9]*')

# Second turn: pass the captured blocks back as the assistant message.
# The thinking block MUST accompany the tool_use block.
ant messages create <<YAML
model: claude-sonnet-4-6
max_tokens: 16000
thinking:
  type: enabled
  budget_tokens: 10000
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state
      required: [location]
messages:
  - role: user
    content: What's the weather in Paris?
  - role: assistant
    content: $ASSISTANT_CONTENT
  - role: user
    content:
      - type: tool_result
        tool_use_id: $TOOL_USE_ID
        content: "Current temperature: 88°F"
YAML
```

```python Python hidelines={1}
import anthropic
from typing import Any

client = anthropic.Anthropic()
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "The city and state"}
        },
        "required": ["location"],
    },
}
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
# Extract thinking block and tool use block
thinking_block = next(
    (block for block in response.content if block.type == "thinking"), None
)
tool_use_block = next(
    (block for block in response.content if block.type == "tool_use"), None
)

# Call your actual weather API, here is where your actual API call would go
# Let's pretend this is what we get back
weather_data = {"temperature": 88}

# Second request - Include thinking block and tool result
# No new thinking blocks are generated in the response
continuation = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"},
        # notice that the thinking_block is passed in as well as the tool_use_block
        # if this is not passed in, an error is raised
        {"role": "assistant", "content": [thinking_block, tool_use_block]},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": f"Current temperature: {weather_data['temperature']}°F",
                }
            ],
        },
    ],
)
```

```typescript TypeScript nocheck
// Extract thinking block and tool use block
const thinkingBlock = response.content.find(
  (block): block is Anthropic.ThinkingBlock => block.type === "thinking"
);
const toolUseBlock = response.content.find(
  (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
);

// Call your actual weather API, here is where your actual API call would go
// Let's pretend this is what we get back
const weatherData = { temperature: 88 };

if (thinkingBlock && toolUseBlock) {
  // Second request - Include thinking block and tool result
  // No new thinking blocks are generated in the response
  const continuation = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000
    },
    tools: [weatherTool],
    messages: [
      { role: "user", content: "What's the weather in Paris?" },
      // notice that the thinkingBlock is passed in as well as the toolUseBlock
      // if this is not passed in, an error is raised
      { role: "assistant", content: [thinkingBlock, toolUseBlock] },
      {
        role: "user",
        content: [
          {
            type: "tool_result" as const,
            tool_use_id: toolUseBlock.id,
            content: `Current temperature: ${weatherData.temperature}°F`
          }
        ]
      }
    ]
  });
}
```

```csharp C# nocheck
using System;
using System.Text.Json;
using System.Linq;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var weatherTool = new ToolUnion(new Tool()
        {
            Name = "get_weather",
            Description = "Get current weather for a location",
            InputSchema = new InputSchema()
            {
                Properties = new Dictionary<string, JsonElement>
                {
                    ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
                },
                Required = ["location"],
            },
        });

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
            Tools = [weatherTool],
            Messages = [
                new() { Role = Role.User, Content = "What is the weather in Paris?" }
            ]
        };

        var response = await client.Messages.Create(parameters);

        // Extract thinking and tool_use blocks from response
        var thinkingBlock = response.Content.FirstOrDefault(b => b.TryPickThinking(out _));
        var toolUseBlock = response.Content.FirstOrDefault(b => b.TryPickToolUse(out _));

        var weatherData = new { temperature = 88 };

        // Build continuation with tool result
        var continuationParams = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 16000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
            Tools = [weatherTool],
            Messages = [
                new() { Role = Role.User, Content = "What is the weather in Paris?" },
                new() { Role = Role.Assistant, Content = response.Content },
                new() { Role = Role.User, Content = new MessageParamContent(new List<ContentBlockParam>
                {
                    new ContentBlockParam(new ToolResultBlockParam()
                    {
                        ToolUseID = toolUseBlock?.Id ?? "",
                        Content = $"Current temperature: {weatherData.temperature}\u00b0F"
                    })
                })}
            ]
        };

        var continuation = await client.Messages.Create(continuationParams);
        Console.WriteLine(continuation);
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

	weatherTool := anthropic.ToolUnionParam{
		OfTool: &anthropic.ToolParam{
			Name:        "get_weather",
			Description: anthropic.String("Get current weather for a location"),
			InputSchema: anthropic.ToolInputSchemaParam{
				Properties: map[string]any{
					"location": map[string]any{
						"type":        "string",
						"description": "City name",
					},
				},
				Required: []string{"location"},
			},
		},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 16000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
		Tools:     []anthropic.ToolUnionParam{weatherTool},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in Paris?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	var toolUseBlock anthropic.ToolUseBlock
	for _, block := range response.Content {
		switch v := block.AsAny().(type) {
		case anthropic.ToolUseBlock:
			toolUseBlock = v
		}
	}

	weatherData := map[string]int{"temperature": 88}

	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 16000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
		Tools:     []anthropic.ToolUnionParam{weatherTool},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in Paris?")),
			response.ToParam(),
			anthropic.NewUserMessage(
				anthropic.NewToolResultBlock(toolUseBlock.ID, fmt.Sprintf("Current temperature: %d°F", weatherData["temperature"]), false),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(continuation)
}
```

```java Java hidelines={1..10,13..18,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlock;
import com.anthropic.models.messages.ToolUseBlockParam;
import com.anthropic.models.messages.ThinkingBlock;
import com.anthropic.models.messages.ThinkingBlockParam;
import com.anthropic.core.JsonValue;
import java.util.List;
import java.util.Map;

public class ExtendedThinkingToolUse {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        Tool weatherTool = Tool.builder()
            .name("get_weather")
            .description("Get current weather for a location")
            .inputSchema(Tool.InputSchema.builder()
                .properties(JsonValue.from(Map.of(
                    "location", Map.of("type", "string", "description", "City name")
                )))
                .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                .build())
            .build();

        MessageCreateParams initialParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(16000L)
            .enabledThinking(10000L)
            .addTool(weatherTool)
            .addUserMessage("What is the weather in Paris?")
            .build();

        Message response = client.messages().create(initialParams);

        ThinkingBlock thinkingBlock = null;
        ToolUseBlock toolUseBlock = null;
        for (var block : response.content()) {
            if (block.thinking().isPresent()) {
                thinkingBlock = block.thinking().get();
            }
            if (block.toolUse().isPresent()) {
                toolUseBlock = block.toolUse().get();
            }
        }

        int temperature = 88;

        // Second request: pass back thinking block and tool result
        MessageCreateParams continuationParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(16000L)
            .enabledThinking(10000L)
            .addTool(weatherTool)
            .addUserMessage("What is the weather in Paris?")
            .addAssistantMessageOfBlockParams(List.of(
                ContentBlockParam.ofThinking(ThinkingBlockParam.builder()
                    .thinking(thinkingBlock.thinking())
                    .signature(thinkingBlock.signature())
                    .build()),
                ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                    .id(toolUseBlock.id())
                    .name(toolUseBlock.name())
                    .input(toolUseBlock._input())
                    .build())
            ))
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofToolResult(
                    ToolResultBlockParam.builder()
                        .toolUseId(toolUseBlock.id())
                        .content("Current temperature: " + temperature + "°F")
                        .build()
                )
            ))
            .build();

        Message continuation = client.messages().create(continuationParams);
        System.out.println(continuation);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$weatherTool = [
    'name' => 'get_weather',
    'description' => 'Get current weather for a location',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'location' => [
                'type' => 'string',
                'description' => 'City name'
            ]
        ],
        'required' => ['location']
    ]
];

$response = $client->messages->create(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather in Paris?']
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
    tools: [$weatherTool],
);

$thinkingBlock = null;
$toolUseBlock = null;
foreach ($response->content as $block) {
    if ($block->type === 'thinking') {
        $thinkingBlock = $block;
    }
    if ($block->type === 'tool_use') {
        $toolUseBlock = $block;
    }
}

$weatherData = ['temperature' => 88];

$continuation = $client->messages->create(
    maxTokens: 16000,
    messages: [
        ['role' => 'user', 'content' => 'What is the weather in Paris?'],
        ['role' => 'assistant', 'content' => [$thinkingBlock, $toolUseBlock]],
        ['role' => 'user', 'content' => [
            [
                'type' => 'tool_result',
                'tool_use_id' => $toolUseBlock->id,
                'content' => "Current temperature: {$weatherData['temperature']}°F"
            ]
        ]]
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
    tools: [$weatherTool],
);

echo $continuation;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

weather_tool = {
  name: "get_weather",
  description: "Get current weather for a location",
  input_schema: {
    type: "object",
    properties: {
      location: { type: "string", description: "City name" }
    },
    required: ["location"]
  }
}

response = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weather_tool],
  messages: [
    { role: "user", content: "What is the weather in Paris?" }
  ]
)

thinking_block = response.content.find { |block| block.type == :thinking }
tool_use_block = response.content.find { |block| block.type == :tool_use }

raise "No tool_use block found" unless tool_use_block

weather_data = { temperature: 88 }

continuation = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [weather_tool],
  messages: [
    { role: "user", content: "What is the weather in Paris?" },
    { role: "assistant", content: [thinking_block, tool_use_block] },
    { role: "user", content: [
      {
        type: "tool_result",
        tool_use_id: tool_use_block.id,
        content: "Current temperature: #{weather_data[:temperature]}°F"
      }
    ] }
  ]
)

puts continuation
```

</CodeGroup>

Respons API sekarang mencakup **hanya** teks

```json Output
{
  "content": [
    {
      "type": "text",
      "text": "Currently in Paris, the temperature is 88°F (31°C)"
    }
  ]
}
```

</section>

### Mempertahankan blok pemikiran

Selama penggunaan alat, Anda harus meneruskan blok `thinking` kembali ke API, dan Anda harus menyertakan blok lengkap yang tidak dimodifikasi kembali ke API. Ini sangat penting untuk mempertahankan aliran penalaran model dan integritas percakapan.

<Tip>
Meskipun Anda dapat menghilangkan blok `thinking` dari giliran `assistant` sebelumnya, selalu teruskan semua blok pemikiran ke API untuk percakapan multi-giliran apa pun. API:
- Secara otomatis memfilter blok pemikiran yang disediakan
- Menggunakan blok pemikiran yang relevan yang diperlukan untuk mempertahankan penalaran model
- Hanya menagih token input untuk blok yang ditampilkan ke Claude
</Tip>

<Note>
Ketika mengalihkan mode pemikiran selama percakapan, ingat bahwa seluruh giliran asisten (termasuk loop penggunaan alat) harus beroperasi dalam satu mode pemikiran. Untuk detail lebih lanjut, lihat [Mengalihkan mode pemikiran dalam percakapan](#toggling-thinking-modes-in-conversations).
</Note>

Ketika Claude memanggil alat, itu menghentikan konstruksi respons untuk menunggu informasi eksternal. Ketika hasil alat dikembalikan, Claude melanjutkan membangun respons yang ada. Ini memerlukan pemeliharaan blok pemikiran selama penggunaan alat, untuk beberapa alasan:

1. **Kontinuitas penalaran**: Blok pemikiran menangkap penalaran langkah demi langkah Claude yang menyebabkan permintaan alat. Ketika Anda memposting hasil alat, menyertakan pemikiran asli memastikan Claude dapat melanjutkan penalarannya dari tempat ia berhenti.

2. **Pemeliharaan konteks**: Meskipun hasil alat muncul sebagai pesan pengguna dalam struktur API, mereka adalah bagian dari aliran penalaran yang berkelanjutan. Mempertahankan blok pemikiran mempertahankan aliran konseptual ini di seluruh panggilan API yang berbeda. Untuk informasi lebih lanjut tentang manajemen konteks, lihat [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows).

**Penting**: Ketika memberikan blok `thinking`, seluruh urutan blok `thinking` berturut-turut harus cocok dengan output yang dihasilkan oleh model selama permintaan asli; Anda tidak dapat mengatur ulang atau memodifikasi urutan blok ini.

### Pemikiran yang disisipi

Extended thinking dengan penggunaan alat dalam model Claude 4 mendukung pemikiran yang disisipi, yang memungkinkan Claude untuk berpikir di antara panggilan alat dan membuat penalaran yang lebih canggih setelah menerima hasil alat.

Dengan pemikiran yang disisipi, Claude dapat:
- Bernalar tentang hasil panggilan alat sebelum memutuskan apa yang harus dilakukan selanjutnya
- Menghubungkan beberapa panggilan alat dengan langkah penalaran di antaranya
- Membuat keputusan yang lebih bernuansa berdasarkan hasil perantara

**Dukungan model:**
- **[Claude Mythos Preview](https://anthropic.com/glasswing)**: Pemikiran yang disisipi terjadi secara otomatis. Setiap langkah penalaran antar-alat bergerak ke blok pemikiran alih-alih teks biasa, dan blok pemikiran dipertahankan di seluruh giliran secara default. Tidak ada header beta yang diperlukan atau didukung.
- **Claude Opus 4.7**: Pemikiran yang disisipi secara otomatis diaktifkan saat menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (satu-satunya mode pemikiran yang didukung di Opus 4.7). Tidak ada header beta yang diperlukan.
- **Claude Opus 4.6**: Pemikiran yang disisipi secara otomatis diaktifkan saat menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Tidak ada header beta yang diperlukan. Header beta `interleaved-thinking-2025-05-14` **sudah usang** di Opus 4.6 dan dengan aman diabaikan jika disertakan.
- **Claude Sonnet 4.6**: Pemikiran yang disisipi secara otomatis diaktifkan saat menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (direkomendasikan). Header beta `interleaved-thinking-2025-05-14` dengan extended thinking manual (`thinking: {type: "enabled"}`) masih berfungsi tetapi sudah usang.
- **Model Claude 4 lainnya** (Opus 4.5, Opus 4.1, Opus 4 (usang), Sonnet 4.5, Sonnet 4 (usang)): Tambahkan [header beta](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda untuk mengaktifkan pemikiran yang disisipi.

Berikut adalah beberapa pertimbangan penting untuk pemikiran yang disisipi:
- Dengan pemikiran yang disisipi, `budget_tokens` dapat melebihi parameter `max_tokens`, karena mewakili anggaran total di seluruh semua blok pemikiran dalam satu giliran asisten.
- Pemikiran yang disisipi hanya didukung untuk [alat yang digunakan melalui Messages API](/docs/id/agents-and-tools/tool-use/overview).
- Panggilan langsung ke Claude API memungkinkan Anda meneruskan `interleaved-thinking-2025-05-14` dalam permintaan ke model apa pun, tanpa efek (kecuali Opus 4.7 dan Opus 4.6, di mana sudah usang dan dengan aman diabaikan).
- Di platform pihak ketiga (misalnya, [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock) dan [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)), jika Anda meneruskan `interleaved-thinking-2025-05-14` ke model apa pun selain Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5, Claude Opus 4.1, Opus 4 (usang), Sonnet 4.5, atau Sonnet 4 (usang), permintaan Anda akan gagal.

<section title="Penggunaan alat tanpa pemikiran yang disisipi">

Tanpa pemikiran yang disisipi, Claude berpikir sekali di awal giliran asisten. Respons berikutnya setelah hasil alat berlanjut tanpa blok pemikiran baru.

```text
User: "What's the total revenue if we sold 150 units at $50 each,
       and how does this compare to our average monthly revenue?"

Turn 1: [thinking] "I need to calculate 150 * $50, then check the database..."
        [tool_use: calculator] { "expression": "150 * 50" }
  ↓ tool result: "7500"

Turn 2: [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
        ↑ no thinking block
  ↓ tool result: "5200"

Turn 3: [text] "The total revenue is $7,500, which is 44% above your
        average monthly revenue of $5,200."
        ↑ no thinking block
```

</section>

<section title="Penggunaan alat dengan pemikiran yang disisipi">

Dengan pemikiran yang disisipi diaktifkan, Claude dapat berpikir setelah menerima setiap hasil alat, memungkinkannya untuk bernalar tentang hasil perantara sebelum melanjutkan.

```text
User: "What's the total revenue if we sold 150 units at $50 each,
       and how does this compare to our average monthly revenue?"

Turn 1: [thinking] "I need to calculate 150 * $50 first..."
        [tool_use: calculator] { "expression": "150 * 50" }
  ↓ tool result: "7500"

Turn 2: [thinking] "Got $7,500. Now I should query the database to compare..."
        [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
        ↑ thinking after receiving calculator result
  ↓ tool result: "5200"

Turn 3: [thinking] "$7,500 vs $5,200 average - that's a 44% increase..."
        [text] "The total revenue is $7,500, which is 44% above your
        average monthly revenue of $5,200."
        ↑ thinking before final answer
```

</section>

## Pemikiran yang diperluas dengan prompt caching

[Prompt caching](/docs/id/build-with-claude/prompt-caching) dengan pemikiran memiliki beberapa pertimbangan penting:

<Tip>
Tugas pemikiran yang diperluas sering kali membutuhkan waktu lebih dari 5 menit untuk diselesaikan. Pertimbangkan untuk menggunakan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hits di seluruh sesi pemikiran yang lebih lama dan alur kerja multi-langkah.
</Tip>

**Penghapusan konteks blok pemikiran**
- Blok pemikiran dari giliran sebelumnya dihapus dari konteks, yang dapat mempengaruhi titik putus cache
- Saat melanjutkan percakapan dengan penggunaan alat, blok pemikiran di-cache dan dihitung sebagai token input saat dibaca dari cache
- Ini menciptakan pertukaran: meskipun blok pemikiran tidak mengonsumsi ruang jendela konteks secara visual, mereka tetap dihitung terhadap penggunaan token input Anda saat di-cache
- Jika pemikiran menjadi dinonaktifkan dan Anda meneruskan konten pemikiran dalam giliran penggunaan alat saat ini, konten pemikiran akan dihapus dan pemikiran akan tetap dinonaktifkan untuk permintaan tersebut

**Pola invalidasi cache**
- Perubahan pada parameter pemikiran (diaktifkan/dinonaktifkan atau alokasi anggaran) membatalkan titik putus cache pesan
- [Pemikiran yang disisipi](#interleaved-thinking) memperkuat invalidasi cache, karena blok pemikiran dapat terjadi di antara beberapa [panggilan alat](#extended-thinking-with-tool-use)
- Prompt sistem dan alat tetap di-cache meskipun ada perubahan parameter pemikiran atau penghapusan blok

<Note>
Meskipun blok pemikiran dihapus untuk caching dan perhitungan konteks, mereka harus dipertahankan saat melanjutkan percakapan dengan [penggunaan alat](#extended-thinking-with-tool-use), terutama dengan [pemikiran yang disisipi](#interleaved-thinking).
</Note>

### Memahami perilaku caching blok pemikiran

Saat menggunakan pemikiran yang diperluas dengan penggunaan alat, blok pemikiran menunjukkan perilaku caching tertentu yang mempengaruhi penghitungan token:

**Cara kerjanya:**

1. Caching hanya terjadi ketika Anda membuat permintaan berikutnya yang mencakup hasil alat
2. Ketika permintaan berikutnya dibuat, riwayat percakapan sebelumnya (termasuk blok pemikiran) dapat di-cache
3. Blok pemikiran yang di-cache ini dihitung sebagai token input dalam metrik penggunaan Anda ketika dibaca dari cache
4. Ketika blok pengguna non-hasil-alat disertakan, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks

**Alur contoh terperinci:**

**Permintaan 1:**
```text
User: "What's the weather in Paris?"
```
**Respons 1:**
```text
[thinking_block_1] + [tool_use block 1]
```

**Permintaan 2:**
```text
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
```
**Respons 2:**
```text
[thinking_block_2] + [text block 2]
```
Permintaan 2 menulis cache dari konten permintaan (bukan respons). Cache mencakup pesan pengguna asli, blok pemikiran pertama, blok penggunaan alat, dan hasil alat.

**Permintaan 3:**
```text
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```
Untuk Claude Opus 4.5 dan yang lebih baru (termasuk Claude Opus 4.6), semua blok pemikiran sebelumnya disimpan secara default. Untuk model yang lebih lama, karena blok pengguna non-hasil-alat disertakan, semua blok pemikiran sebelumnya diabaikan. Permintaan ini akan diproses sama dengan:
```text
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

**Poin-poin kunci:**
- Perilaku caching ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit
- Perilaku ini konsisten apakah menggunakan pemikiran reguler atau pemikiran yang disisipi

<section title="Caching prompt sistem (dipertahankan ketika pemikiran berubah)">

<CodeGroup>
```bash CLI
# Ambil ~10 kB Pride and Prejudice untuk blok sistem yang di-cache
curl -s https://www.gutenberg.org/cache/epub/1342/pg1342.txt \
  | head -c 10000 > pride.txt

# Emit badan permintaan untuk anggaran pemikiran yang diberikan. Setelah CONTENT1
# diisi (setelah giliran pertama), respons asisten dan pesan pengguna lanjutan
# ditambahkan sehingga percakapan berkembang.
build_body() {
  cat <<YAML
model: claude-sonnet-4-6
max_tokens: 20000
thinking:
  type: enabled
  budget_tokens: $1
system:
  - type: text
    text: >-
      You are an AI assistant that is tasked with literary analysis.
      Analyze the following text carefully.
  - type: text
    text: "@./pride.txt"
    cache_control:
      type: ephemeral
messages:
  - role: user
    content: Analyze the tone of this passage.
YAML
  if [[ -n "${CONTENT1:-}" ]]; then
    printf '  - role: assistant\n    content: %s\n' "$CONTENT1"
    printf '  - role: user\n'
    printf '    content: Analyze the characters in this passage.\n'
  fi
}

# Permintaan pertama (anggaran 4000): membangun cache. Tangkap penggunaan
# dan konten sebagai dua baris jsonl sehingga balasan dapat diteruskan.
printf 'First request - establishing cache\n'
{
  read -r USAGE1
  read -r CONTENT1
} < <(build_body 4000 \
  | ant messages create --transform '[usage,content]' --format jsonl)
printf 'First response usage: %s\n' "$USAGE1"

# Permintaan kedua: anggaran yang sama, cache prompt sistem diharapkan.
printf '\nSecond request - same thinking parameters (cache hit expected)\n'
USAGE2=$(build_body 4000 \
  | ant messages create --transform usage --format jsonl)
printf 'Second response usage: %s\n' "$USAGE2"

# Permintaan ketiga: anggaran diubah menjadi 8000. Prompt sistem yang di-cache
# masih terkena; hanya caching blok pesan yang tidak valid.
printf '\nThird request - different thinking parameters (cache miss for messages)\n'
USAGE3=$(build_body 8000 \
  | ant messages create --transform usage --format jsonl)
printf 'Third response usage: %s\n' "$USAGE3"
```

```python Python hidelines={1}
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup

client = Anthropic()


def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Hapus elemen script dan style
    for script in soup(["script", "style"]):
        script.decompose()

    # Dapatkan teks
    text = soup.get_text()

    # Pecah menjadi baris dan hapus spasi di awal dan akhir setiap baris
    lines = (line.strip() for line in text.splitlines())
    # Pecah multi-headline menjadi satu baris masing-masing
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Hapus baris kosong
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


# Ambil konten artikel
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Gunakan cukup teks untuk caching (beberapa bab pertama)
LARGE_TEXT = book_content[:10000]

SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.",
    },
    {"type": "text", "text": LARGE_TEXT, "cache_control": {"type": "ephemeral"}},
]

MESSAGES = [{"role": "user", "content": "Analyze the tone of this passage."}]

# Permintaan pertama - bangun cache
print("First request - establishing cache")
response1 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 4000},
    system=SYSTEM_PROMPT,
    messages=MESSAGES,
)

print(f"First response usage: {response1.usage}")

MESSAGES.append({"role": "assistant", "content": response1.content})
MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})
# Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 4000},
    system=SYSTEM_PROMPT,
    messages=MESSAGES,
)

print(f"Second response usage: {response2.usage}")

# Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
print("\nThird request - different thinking parameters (cache miss for messages)")
response3 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000,  # Anggaran pemikiran berubah
    },
    system=SYSTEM_PROMPT,  # Prompt sistem tetap di-cache
    messages=MESSAGES,  # Cache pesan tidak valid
)

print(f"Third response usage: {response3.usage}")
```

```typescript TypeScript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import axios from "axios";
import * as cheerio from "cheerio";

const client = new Anthropic();

async function fetchArticleContent(url: string): Promise<string> {
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);
  $("script, style").remove();
  let text = $.text();
  const lines = text.split("\n").map((line) => line.trim());
  text = lines.filter((line) => line.length > 0).join("\n");
  return text;
}

async function main(): Promise<void> {
  const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
  const bookContent = await fetchArticleContent(bookUrl);
  const LARGE_TEXT = bookContent.slice(0, 10000);

  const SYSTEM_PROMPT: Anthropic.TextBlockParam[] = [
    {
      type: "text",
      text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
    },
    {
      type: "text",
      text: LARGE_TEXT,
      cache_control: { type: "ephemeral" }
    }
  ];

  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "Analyze the tone of this passage." }
  ];

  // Permintaan pertama - bangun cache
  console.log("First request - establishing cache");
  const response1 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 4000 },
    system: SYSTEM_PROMPT,
    messages
  });

  console.log(`First response usage: ${JSON.stringify(response1.usage)}`);

  messages.push({
    role: "assistant",
    content: response1.content as Anthropic.ContentBlockParam[]
  });
  messages.push({
    role: "user",
    content: "Analyze the characters in this passage."
  });

  // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
  console.log("\nSecond request - same thinking parameters (cache hit expected)");
  const response2 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 4000 },
    system: SYSTEM_PROMPT,
    messages
  });

  console.log(`Second response usage: ${JSON.stringify(response2.usage)}`);

  // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
  console.log("\nThird request - different thinking parameters (cache miss for messages)");
  const response3 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 8000 },
    system: SYSTEM_PROMPT,
    messages
  });

  console.log(`Third response usage: ${JSON.stringify(response3.usage)}`);
}

main();
```

```csharp C# nocheck
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        // Ambil konten buku
        using var httpClient = new HttpClient();
        var bookContent = await httpClient.GetStringAsync("https://www.gutenberg.org/cache/epub/1342/pg1342.txt");
        var largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

        var systemPrompt = new MessageCreateParamsSystem(new List<TextBlockParam>
        {
            new TextBlockParam()
            {
                Text = "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
            },
            new TextBlockParam()
            {
                Text = largeText,
                CacheControl = new CacheControlEphemeral(),
            },
        });

        var messages = new List<MessageParam>
        {
            new() { Role = Role.User, Content = "Analyze the tone of this passage." }
        };

        // Permintaan pertama - bangun cache
        Console.WriteLine("First request - establishing cache");
        var parameters1 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
            System = systemPrompt,
            Messages = messages
        };

        var response1 = await client.Messages.Create(parameters1);
        Console.WriteLine($"First response usage: {response1.Usage}");

        messages.Add(new() { Role = Role.Assistant, Content = response1.Content });
        messages.Add(new() { Role = Role.User, Content = "Analyze the characters in this passage." });

        // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
        Console.WriteLine("\nSecond request - same thinking parameters (cache hit expected)");
        var parameters2 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
            System = systemPrompt,
            Messages = messages
        };

        var response2 = await client.Messages.Create(parameters2);
        Console.WriteLine($"Second response usage: {response2.Usage}");

        // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
        Console.WriteLine("\nThird request - different thinking parameters (cache miss for messages)");
        var parameters3 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 8000),
            System = systemPrompt,
            Messages = messages
        };

        var response3 = await client.Messages.Create(parameters3);
        Console.WriteLine($"Third response usage: {response3.Usage}");
    }
}
```

```go Go hidelines={1..15,-6..-1}
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Ambil konten buku
	resp, err := http.Get("https://www.gutenberg.org/cache/epub/1342/pg1342.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	largeText := string(body)
	if len(largeText) > 10000 {
		largeText = largeText[:10000]
	}

	systemPrompt := []anthropic.TextBlockParam{
		{Text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."},
		{
			Text:         largeText,
			CacheControl: anthropic.NewCacheControlEphemeralParam(),
		},
	}

	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the tone of this passage.")),
	}

	// Permintaan pertama - bangun cache
	fmt.Println("First request - establishing cache")
	response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("First response usage: %+v\n", response1.Usage)

	messages = append(messages, response1.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

	// Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
	fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
	response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Second response usage: %+v\n", response2.Usage)

	// Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
	fmt.Println("\nThird request - different thinking parameters (cache miss for messages)")
	response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Third response usage: %+v\n", response3.Usage)
}
```

```java Java hidelines={1..2,4..15,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;

public class ThinkingCacheExample {
    public static void main(String[] args) throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Ambil konten buku
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://www.gutenberg.org/cache/epub/1342/pg1342.txt"))
            .build();
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        String bookContent = response.body();
        String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

        List<TextBlockParam> systemPrompt = List.of(
            TextBlockParam.builder()
                .text("You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.")
                .build(),
            TextBlockParam.builder()
                .text(largeText)
                .cacheControl(CacheControlEphemeral.builder().build())
                .build()
        );

        // Permintaan pertama - bangun cache
        System.out.println("First request - establishing cache");
        MessageCreateParams params1 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(4000L)
            .systemOfTextBlockParams(systemPrompt)
            .addUserMessage("Analyze the tone of this passage.")
            .build();

        Message response1 = client.messages().create(params1);
        System.out.println("First response usage: " + response1.usage());

        // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
        System.out.println("\nSecond request - same thinking parameters (cache hit expected)");
        MessageCreateParams params2 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(4000L)
            .systemOfTextBlockParams(systemPrompt)
            .addUserMessage("Analyze the tone of this passage.")
            .addAssistantMessageOfBlockParams(response1.content().stream()
                .map(block -> block.toParam())
                .collect(java.util.stream.Collectors.toList()))
            .addUserMessage("Analyze the characters in this passage.")
            .build();

        Message response2 = client.messages().create(params2);
        System.out.println("Second response usage: " + response2.usage());

        // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
        System.out.println("\nThird request - different thinking parameters (cache miss for messages)");
        MessageCreateParams params3 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(8000L)
            .systemOfTextBlockParams(systemPrompt)
            .addUserMessage("Analyze the tone of this passage.")
            .addAssistantMessageOfBlockParams(response1.content().stream()
                .map(block -> block.toParam())
                .collect(java.util.stream.Collectors.toList()))
            .addUserMessage("Analyze the characters in this passage.")
            .build();

        Message response3 = client.messages().create(params3);
        System.out.println("Third response usage: " + response3.usage());
    }
}
```

```php PHP hidelines={1..5}
<?php


use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

// Ambil konten buku
$bookContent = file_get_contents("https://www.gutenberg.org/cache/epub/1342/pg1342.txt");
$largeText = substr($bookContent, 0, 10000);

$systemPrompt = [
    [
        'type' => 'text',
        'text' => 'You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.'
    ],
    [
        'type' => 'text',
        'text' => $largeText,
        'cache_control' => ['type' => 'ephemeral']
    ]
];

$messages = [
    ['role' => 'user', 'content' => 'Analyze the tone of this passage.']
];

// Permintaan pertama - bangun cache
echo "First request - establishing cache\n";
$response1 = $client->messages->create(
    maxTokens: 20000,
    messages: $messages,
    model: 'claude-sonnet-4-6',
    system: $systemPrompt,
    thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
);

echo "First response usage: " . json_encode($response1->usage) . "\n";

$messages[] = ['role' => 'assistant', 'content' => $response1->content];
$messages[] = ['role' => 'user', 'content' => 'Analyze the characters in this passage.'];

// Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
echo "\nSecond request - same thinking parameters (cache hit expected)\n";
$response2 = $client->messages->create(
    maxTokens: 20000,
    messages: $messages,
    model: 'claude-sonnet-4-6',
    system: $systemPrompt,
    thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
);

echo "Second response usage: " . json_encode($response2->usage) . "\n";

// Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
echo "\nThird request - different thinking parameters (cache miss for messages)\n";
$response3 = $client->messages->create(
    maxTokens: 20000,
    messages: $messages,
    model: 'claude-sonnet-4-6',
    system: $systemPrompt,
    thinking: ['type' => 'enabled', 'budget_tokens' => 8000],
);

echo "Third response usage: " . json_encode($response3->usage) . "\n";
```

```ruby Ruby hidelines={1}
require "anthropic"
require "net/http"
require "uri"

client = Anthropic::Client.new

# Ambil konten buku
uri = URI("https://www.gutenberg.org/cache/epub/1342/pg1342.txt")
response = Net::HTTP.get_response(uri)
book_content = response.body
large_text = book_content[0...10000]

system_prompt = [
  {
    type: "text",
    text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
  },
  {
    type: "text",
    text: large_text,
    cache_control: { type: "ephemeral" }
  }
]

messages = [
  { role: "user", content: "Analyze the tone of this passage." }
]

# Permintaan pertama - bangun cache
puts "First request - establishing cache"
response1 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  system: system_prompt,
  messages: messages
)

puts "First response usage: #{response1.usage}"

messages << { role: "assistant", content: response1.content }
messages << { role: "user", content: "Analyze the characters in this passage." }

# Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
puts "\nSecond request - same thinking parameters (cache hit expected)"
response2 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  system: system_prompt,
  messages: messages
)

puts "Second response usage: #{response2.usage}"

# Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
puts "\nThird request - different thinking parameters (cache miss for messages)"
response3 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 8000
  },
  system: system_prompt,
  messages: messages
)

puts "Third response usage: #{response3.usage}"
```

</CodeGroup>

</section>
<section title="Caching pesan (tidak valid ketika pemikiran berubah)">

<CodeGroup>
```bash CLI
# Ambil ~10 kB pertama Pride and Prejudice untuk awalan yang di-cache
curl -sL 'https://www.gutenberg.org/cache/epub/1342/pg1342.txt' \
  | head -c 10000 > book.txt

# Panggilan 1: anggaran pemikiran 4000, menulis cache
USAGE=$(ant messages create \
  --model claude-sonnet-4-6 --max-tokens 20000 \
  --transform usage <<'YAML'
thinking:
  type: enabled
  budget_tokens: 4000
messages:
  - role: user
    content:
      - type: text
        text: "@./book.txt"
        cache_control:
          type: ephemeral
      - type: text
        text: "Give a one-sentence summary of this passage."
YAML
)
printf 'Call 1 (budget 4000):\n%s\n\n' "$USAGE"

# Panggilan 2: anggaran yang sama, percakapan diperluas; harapkan cache HIT
USAGE=$(ant messages create \
  --model claude-sonnet-4-6 --max-tokens 20000 \
  --transform usage <<'YAML'
thinking:
  type: enabled
  budget_tokens: 4000
messages:
  - role: user
    content:
      - type: text
        text: "@./book.txt"
        cache_control:
          type: ephemeral
      - type: text
        text: "Give a one-sentence summary of this passage."
  - role: assistant
    content: "It opens Pride and Prejudice with the Bennet family."
  - role: user
    content: "Who is the protagonist?"
YAML
)
printf 'Call 2 (budget 4000):\n%s\n\n' "$USAGE"

# Panggilan 3: anggaran diubah menjadi 8000; cache MISS meskipun awalan identik
USAGE=$(ant messages create \
  --model claude-sonnet-4-6 --max-tokens 20000 \
  --transform usage <<'YAML'
thinking:
  type: enabled
  budget_tokens: 8000
messages:
  - role: user
    content:
      - type: text
        text: "@./book.txt"
        cache_control:
          type: ephemeral
      - type: text
        text: "Give a one-sentence summary of this passage."
  - role: assistant
    content: "It opens Pride and Prejudice with the Bennet family."
  - role: user
    content: "Who is the protagonist?"
  - role: assistant
    content: "Elizabeth Bennet is the protagonist."
  - role: user
    content: "What era is the story set in?"
YAML
)
printf 'Call 3 (budget 8000):\n%s\n' "$USAGE"
```

```python Python hidelines={1}
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup

client = Anthropic()


def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Hapus elemen script dan style
    for script in soup(["script", "style"]):
        script.decompose()

    # Dapatkan teks
    text = soup.get_text()

    # Pecah menjadi baris dan hapus spasi di awal dan akhir setiap baris
    lines = (line.strip() for line in text.splitlines())
    # Pecah multi-headline menjadi satu baris masing-masing
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Hapus baris kosong
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


# Ambil konten artikel
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Gunakan cukup teks untuk caching (beberapa bab pertama)
LARGE_TEXT = book_content[:10000]

# Tidak ada prompt sistem - caching di pesan sebagai gantinya
MESSAGES = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": LARGE_TEXT,
                "cache_control": {"type": "ephemeral"},
            },
            {"type": "text", "text": "Analyze the tone of this passage."},
        ],
    }
]

# Permintaan pertama - bangun cache
print("First request - establishing cache")
response1 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 4000},
    messages=MESSAGES,
)

print(f"First response usage: {response1.usage}")

MESSAGES.append({"role": "assistant", "content": response1.content})
MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})
# Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000,  # Anggaran pemikiran yang sama
    },
    messages=MESSAGES,
)

print(f"Second response usage: {response2.usage}")

MESSAGES.append({"role": "assistant", "content": response2.content})
MESSAGES.append({"role": "user", "content": "Analyze the setting in this passage."})

# Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
print("\nThird request - different thinking budget (cache miss expected)")
response3 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000,  # Anggaran pemikiran berbeda memecah cache
    },
    messages=MESSAGES,
)

print(f"Third response usage: {response3.usage}")
```

```typescript TypeScript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import axios from "axios";
import * as cheerio from "cheerio";

const client = new Anthropic();

async function fetchArticleContent(url: string): Promise<string> {
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);

  // Hapus elemen script dan style
  $("script, style").remove();

  // Dapatkan teks
  let text = $.text();

  // Bersihkan teks (pecah menjadi baris, hapus spasi)
  const lines = text.split("\n").map((line) => line.trim());
  const chunks = lines.flatMap((line) => line.split("  ").map((phrase) => phrase.trim()));
  text = chunks.filter((chunk) => chunk).join("\n");

  return text;
}

async function main(): Promise<void> {
  const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
  const bookContent = await fetchArticleContent(bookUrl);
  const LARGE_TEXT = bookContent.substring(0, 10000);

  // Tidak ada prompt sistem - caching di pesan sebagai gantinya
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: LARGE_TEXT,
          cache_control: { type: "ephemeral" }
        },
        {
          type: "text",
          text: "Analyze the tone of this passage."
        }
      ]
    }
  ];

  // Permintaan pertama - bangun cache
  console.log("First request - establishing cache");
  const response1 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 4000 },
    messages
  });

  console.log("First response usage: ", response1.usage);

  messages.push(
    { role: "assistant", content: response1.content as Anthropic.ContentBlockParam[] },
    { role: "user", content: "Analyze the characters in this passage." }
  );

  // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
  console.log("\nSecond request - same thinking parameters (cache hit expected)");
  const response2 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 4000 },
    messages
  });

  console.log("Second response usage: ", response2.usage);

  messages.push(
    { role: "assistant", content: response2.content as Anthropic.ContentBlockParam[] },
    { role: "user", content: "Analyze the setting in this passage." }
  );

  // Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
  console.log("\nThird request - different thinking budget (cache miss expected)");
  const response3 = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 20000,
    thinking: { type: "enabled", budget_tokens: 8000 },
    messages
  });

  console.log("Third response usage: ", response3.usage);
}

main().catch(console.error);
```

```csharp C# nocheck
using System;
using System.Net.Http;
using System.Collections.Generic;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        string bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
        string bookContent = await FetchArticleContent(bookUrl);
        string largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

        Console.WriteLine("First request - establishing cache");
        var parameters1 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = largeText,
                            CacheControl = new CacheControlEphemeral(),
                        }),
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = "Analyze the tone of this passage."
                        }),
                    })
                }
            ]
        };

        var response1 = await client.Messages.Create(parameters1);
        Console.WriteLine($"First response usage: {response1.Usage}");

        Console.WriteLine("\nSecond request - same thinking parameters (cache hit expected)");
        var parameters2 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = largeText,
                            CacheControl = new CacheControlEphemeral(),
                        }),
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = "Analyze the tone of this passage."
                        }),
                    })
                },
                new()
                {
                    Role = Role.Assistant,
                    Content = response1.Content
                },
                new()
                {
                    Role = Role.User,
                    Content = "Analyze the characters in this passage."
                }
            ]
        };

        var response2 = await client.Messages.Create(parameters2);
        Console.WriteLine($"Second response usage: {response2.Usage}");

        Console.WriteLine("\nThird request - different thinking budget (cache miss expected)");
        var parameters3 = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 20000,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 8000),
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = largeText,
                            CacheControl = new CacheControlEphemeral(),
                        }),
                        new ContentBlockParam(new TextBlockParam()
                        {
                            Text = "Analyze the tone of this passage."
                        }),
                    })
                },
                new()
                {
                    Role = Role.Assistant,
                    Content = response1.Content
                },
                new()
                {
                    Role = Role.User,
                    Content = "Analyze the characters in this passage."
                },
                new()
                {
                    Role = Role.Assistant,
                    Content = response2.Content
                },
                new()
                {
                    Role = Role.User,
                    Content = "Analyze the setting in this passage."
                }
            ]
        };

        var response3 = await client.Messages.Create(parameters3);
        Console.WriteLine($"Third response usage: {response3.Usage}");
    }

    static async Task<string> FetchArticleContent(string url)
    {
        using HttpClient httpClient = new();
        string content = await httpClient.GetStringAsync(url);
        return content;
    }
}
```

```go Go hidelines={1..41,-1}
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
)

func fetchArticleContent(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	text := string(body)
	lines := strings.Split(text, "\n")
	var cleanedLines []string
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if trimmed != "" {
			cleanedLines = append(cleanedLines, trimmed)
		}
	}

	return strings.Join(cleanedLines, "\n"), nil
}

func main() {
	client := anthropic.NewClient()

	bookURL := "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
	bookContent, err := fetchArticleContent(bookURL)
	if err != nil {
		log.Fatal(err)
	}

	largeText := bookContent
	if len(largeText) > 10000 {
		largeText = largeText[:10000]
	}

	// Tidak ada prompt sistem - caching di pesan sebagai gantinya
	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(
			anthropic.ContentBlockParamUnion{OfText: &anthropic.TextBlockParam{
				Text:         largeText,
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			}},
			anthropic.NewTextBlock("Analyze the tone of this passage."),
		),
	}

	// Permintaan pertama - bangun cache
	fmt.Println("First request - establishing cache")
	response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("First response usage: %+v\n", response1.Usage)

	messages = append(messages, response1.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

	// Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
	fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
	response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Second response usage: %+v\n", response2.Usage)

	messages = append(messages, response2.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the setting in this passage.")))

	// Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
	fmt.Println("\nThird request - different thinking budget (cache miss expected)")
	response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Third response usage: %+v\n", response3.Usage)
}
```

```java Java hidelines={1..2,4..16,94..95,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;

public class CachingThinkingExample {
    public static void main(String[] args) throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        String bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
        String bookContent = fetchArticleContent(bookUrl);
        String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

        // Permintaan pertama - membangun cache
        System.out.println("First request - establishing cache");
        MessageCreateParams params1 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(4000L)
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text(largeText)
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()),
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text("Analyze the tone of this passage.")
                    .build())
            ))
            .build();

        Message response1 = client.messages().create(params1);
        System.out.println("First response usage: " + response1.usage());

        // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
        System.out.println("\nSecond request - same thinking parameters (cache hit expected)");
        MessageCreateParams params2 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(4000L)
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text(largeText)
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()),
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text("Analyze the tone of this passage.")
                    .build())
            ))
            .addAssistantMessageOfBlockParams(response1.content().stream()
                .map(block -> block.toParam())
                .collect(java.util.stream.Collectors.toList()))
            .addUserMessage("Analyze the characters in this passage.")
            .build();

        Message response2 = client.messages().create(params2);
        System.out.println("Second response usage: " + response2.usage());

        // Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
        System.out.println("\nThird request - different thinking budget (cache miss expected)");
        MessageCreateParams params3 = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(20000L)
            .enabledThinking(8000L)
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text(largeText)
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()),
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text("Analyze the tone of this passage.")
                    .build())
            ))
            .addAssistantMessageOfBlockParams(response1.content().stream()
                .map(block -> block.toParam())
                .collect(java.util.stream.Collectors.toList()))
            .addUserMessage("Analyze the characters in this passage.")
            .addAssistantMessageOfBlockParams(response2.content().stream()
                .map(block -> block.toParam())
                .collect(java.util.stream.Collectors.toList()))
            .addUserMessage("Analyze the setting in this passage.")
            .build();

        Message response3 = client.messages().create(params3);
        System.out.println("Third response usage: " + response3.usage());
    }

    private static String fetchArticleContent(String url) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}
```

```php PHP hidelines={1..6}
<?php


use Anthropic\Client;


function fetchArticleContent($url) {
    $content = file_get_contents($url);
    $lines = explode("\n", $content);
    $cleanedLines = array_filter(array_map('trim', $lines));
    return implode("\n", $cleanedLines);
}

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
$bookContent = fetchArticleContent($bookUrl);
$largeText = substr($bookContent, 0, 10000);

echo "First request - establishing cache\n";
$response1 = $client->messages->create(
    maxTokens: 20000,
    messages: [[
        'role' => 'user',
        'content' => [
            [
                'type' => 'text',
                'text' => $largeText,
                'cache_control' => ['type' => 'ephemeral']
            ],
            [
                'type' => 'text',
                'text' => 'Analyze the tone of this passage.'
            ]
        ]
    ]],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
);

echo "First response usage: " . json_encode($response1->usage) . "\n";

echo "\nSecond request - same thinking parameters (cache hit expected)\n";
$response2 = $client->messages->create(
    maxTokens: 20000,
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'text',
                    'text' => $largeText,
                    'cache_control' => ['type' => 'ephemeral']
                ],
                [
                    'type' => 'text',
                    'text' => 'Analyze the tone of this passage.'
                ]
            ]
        ],
        [
            'role' => 'assistant',
            'content' => $response1->content
        ],
        [
            'role' => 'user',
            'content' => 'Analyze the characters in this passage.'
        ]
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
);

echo "Second response usage: " . json_encode($response2->usage) . "\n";

echo "\nThird request - different thinking budget (cache miss expected)\n";
$response3 = $client->messages->create(
    maxTokens: 20000,
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'text',
                    'text' => $largeText,
                    'cache_control' => ['type' => 'ephemeral']
                ],
                [
                    'type' => 'text',
                    'text' => 'Analyze the tone of this passage.'
                ]
            ]
        ],
        [
            'role' => 'assistant',
            'content' => $response1->content
        ],
        [
            'role' => 'user',
            'content' => 'Analyze the characters in this passage.'
        ],
        [
            'role' => 'assistant',
            'content' => $response2->content
        ],
        [
            'role' => 'user',
            'content' => 'Analyze the setting in this passage.'
        ]
    ],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 8000],
);

echo "Third response usage: " . json_encode($response3->usage) . "\n";
```

```ruby Ruby hidelines={1}
require "anthropic"
require "net/http"
require "uri"

def fetch_article_content(url)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  text = response.body

  lines = text.split("\n").map(&:strip)
  lines.reject(&:empty?).join("\n")
end

client = Anthropic::Client.new

book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
large_text = book_content[0...10000]

puts "First request - establishing cache"
response1 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  messages: [{
    role: "user",
    content: [
      {
        type: "text",
        text: large_text,
        cache_control: { type: "ephemeral" }
      },
      {
        type: "text",
        text: "Analyze the tone of this passage."
      }
    ]
  }]
)

puts "First response usage: #{response1.usage}"

puts "\nSecond request - same thinking parameters (cache hit expected)"
response2 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 4000
  },
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: large_text,
          cache_control: { type: "ephemeral" }
        },
        {
          type: "text",
          text: "Analyze the tone of this passage."
        }
      ]
    },
    {
      role: "assistant",
      content: response1.content
    },
    {
      role: "user",
      content: "Analyze the characters in this passage."
    }
  ]
)

puts "Second response usage: #{response2.usage}"

puts "\nThird request - different thinking budget (cache miss expected)"
response3 = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: {
    type: "enabled",
    budget_tokens: 8000
  },
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: large_text,
          cache_control: { type: "ephemeral" }
        },
        {
          type: "text",
          text: "Analyze the tone of this passage."
        }
      ]
    },
    {
      role: "assistant",
      content: response1.content
    },
    {
      role: "user",
      content: "Analyze the characters in this passage."
    },
    {
      role: "assistant",
      content: response2.content
    },
    {
      role: "user",
      content: "Analyze the setting in this passage."
    }
  ]
)

puts "Third response usage: #{response3.usage}"
```

</CodeGroup>

Berikut adalah output dari skrip (Anda mungkin melihat angka yang sedikit berbeda)

```text Output
First request - establishing cache
First response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 17, output_tokens: 700 }

Second request - same thinking parameters (cache hit expected)

Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 1370, input_tokens: 303, output_tokens: 874 }

Third request - different thinking budget (cache miss expected)
Third response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 747, output_tokens: 619 }
```

Contoh ini menunjukkan bahwa ketika caching diatur dalam array pesan, mengubah parameter pemikiran (budget_tokens meningkat dari 4000 menjadi 8000) **membatalkan cache**. Permintaan ketiga menunjukkan tidak ada cache hit dengan `cache_creation_input_tokens=1370` dan `cache_read_input_tokens=0`, membuktikan bahwa caching berbasis pesan tidak valid ketika parameter pemikiran berubah.

</section>

## Token maksimal dan ukuran jendela konteks dengan pemikiran yang diperluas

Dalam model Claude yang lebih lama (sebelum Claude Sonnet 3.7), jika jumlah token prompt dan `max_tokens` melebihi jendela konteks model, sistem akan secara otomatis menyesuaikan `max_tokens` agar sesuai dengan batas konteks. Ini berarti Anda dapat mengatur nilai `max_tokens` yang besar dan sistem akan secara diam-diam menguranginya sesuai kebutuhan.

Dengan model Claude 3.7 dan 4, `max_tokens` (yang mencakup anggaran pemikiran Anda ketika pemikiran diaktifkan) diberlakukan sebagai batas yang ketat. Sistem sekarang akan mengembalikan kesalahan validasi jika token prompt + `max_tokens` melebihi ukuran jendela konteks.

<Note>
Anda dapat membaca [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows) untuk penyelaman yang lebih mendalam.
</Note>

### Jendela konteks dengan pemikiran yang diperluas

Saat menghitung penggunaan jendela konteks dengan pemikiran diaktifkan, ada beberapa pertimbangan yang perlu diperhatikan:

- Blok pemikiran dari putaran sebelumnya dihapus dan tidak dihitung terhadap jendela konteks Anda
- Pemikiran putaran saat ini dihitung terhadap batas `max_tokens` untuk putaran tersebut

Diagram di bawah menunjukkan manajemen token khusus ketika pemikiran yang diperluas diaktifkan:

![Diagram jendela konteks dengan pemikiran yang diperluas](/docs/images/context-window-thinking.svg)

Jendela konteks yang efektif dihitung sebagai:

```text
context window =
  (current input tokens - previous thinking tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan penghitungan token yang akurat untuk kasus penggunaan spesifik Anda, terutama saat bekerja dengan percakapan multi-putaran yang mencakup pemikiran.

### Jendela konteks dengan pemikiran yang diperluas dan penggunaan alat

Saat menggunakan pemikiran yang diperluas dengan penggunaan alat, blok pemikiran harus secara eksplisit dipertahankan dan dikembalikan dengan hasil alat.

Perhitungan jendela konteks yang efektif untuk pemikiran yang diperluas dengan penggunaan alat menjadi:

```text
context window =
  (current input tokens + previous thinking tokens + tool use tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Diagram di bawah mengilustrasikan manajemen token untuk pemikiran yang diperluas dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran yang diperluas dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

### Mengelola token dengan pemikiran yang diperluas

Mengingat perilaku jendela konteks dan `max_tokens` dengan pemikiran yang diperluas pada model Claude 3.7 dan 4, Anda mungkin perlu:

- Memantau dan mengelola penggunaan token Anda dengan lebih aktif
- Menyesuaikan nilai `max_tokens` saat panjang prompt Anda berubah
- Berpotensi menggunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) lebih sering
- Menyadari bahwa blok pemikiran sebelumnya tidak terakumulasi dalam jendela konteks Anda

Perubahan ini telah dilakukan untuk memberikan perilaku yang lebih dapat diprediksi dan transparan, terutama karena batas token maksimal telah meningkat secara signifikan.

## Enkripsi pemikiran

Full thinking content is encrypted and returned in the `signature` field. This field is used to verify that thinking blocks were generated by Claude when passed back to the API.

<Note>
It is only strictly necessary to send back thinking blocks when using [tools with extended thinking](/docs/en/build-with-claude/extended-thinking#extended-thinking-with-tool-use). Otherwise you can omit thinking blocks from previous turns. If you pass them back, whether the API keeps or strips them depends on the model: Opus 4.5+ and Sonnet 4.6+ keep them in context by default; earlier Opus/Sonnet models and all Haiku models strip them. See [context editing](/docs/en/build-with-claude/context-editing) to configure this.

If sending back thinking blocks, pass everything back as you received it for consistency and to avoid potential issues.
</Note>

Here are some important considerations on thinking encryption:
- When [streaming responses](/docs/en/build-with-claude/extended-thinking#streaming-thinking), the signature is added via a `signature_delta` inside a `content_block_delta` event just before the `content_block_stop` event.
- `signature` values are significantly longer in Claude 4 models than in previous models.
- The `signature` field is an opaque field and should not be interpreted or parsed.
- `signature` values are compatible across platforms (Claude APIs, [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock), and [Vertex AI](/docs/en/build-with-claude/claude-on-vertex-ai)). Values generated on one platform will be compatible with another.

## Blok pemikiran yang diredaksi

Selain blok `thinking` biasa, API dapat mengembalikan blok `redacted_thinking`. Blok `redacted_thinking` berisi konten pemikiran terenkripsi dalam bidang `data`, tanpa ringkasan yang dapat dibaca:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

Bidang `data` bersifat opak dan terenkripsi. Seperti bidang `signature` pada blok pemikiran biasa, Anda harus mengirimkan blok `redacted_thinking` kembali ke API tanpa perubahan saat melanjutkan percakapan multi-putaran dengan [alat](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).

<Tip>
Jika kode Anda memfilter blok konten berdasarkan tipe (misalnya, `block.type == "thinking"`) saat mengembalikan respons dengan penggunaan alat, juga sertakan blok `redacted_thinking`. Pemfilteran hanya pada `block.type == "thinking"` secara diam-diam menghapus blok `redacted_thinking` dan merusak protokol multi-putaran yang dijelaskan di atas.
</Tip>

<Note>
Blok `redacted_thinking` adalah tipe blok konten yang berbeda yang dikembalikan oleh API ketika bagian dari pemikiran diredaksi untuk keamanan. Ini terpisah dari opsi [`display: "omitted"`](#controlling-thinking-display), yang mengembalikan blok `thinking` biasa dengan bidang `thinking` kosong.
</Note>

## Perbedaan pemikiran di seluruh versi model

Messages API menangani pemikiran secara berbeda di seluruh model Claude Sonnet 3.7 dan Claude 4, terutama dalam perilaku peringkasan.

Lihat tabel di bawah untuk perbandingan yang diringkas:

| Fitur | Claude Sonnet 3.7 | Model Claude 4 (pra-Opus 4.5) | Claude Opus 4.5 | Claude Sonnet 4.6 | Claude Opus 4.6 ([adaptive thinking](/docs/id/build-with-claude/adaptive-thinking)) | [Claude Mythos Preview](https://anthropic.com/glasswing) ([adaptive thinking](/docs/id/build-with-claude/adaptive-thinking)) |
|---------|------------------|-------------------------------|--------------------------|------------------|--------------------------|--------------------------|
| **Output Pemikiran** | Mengembalikan output pemikiran lengkap | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Dihilangkan secara default; atur `display: "summarized"` untuk menerima pemikiran yang diringkas. Token pemikiran mentah tidak pernah dikembalikan. |
| **Pemikiran yang Disisipi** | Tidak didukung | Didukung dengan header beta `interleaved-thinking-2025-05-14` | Didukung dengan header beta `interleaved-thinking-2025-05-14` | Didukung dengan header beta `interleaved-thinking-2025-05-14` atau otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) | Otomatis dengan adaptive thinking (header beta tidak didukung) | Otomatis dengan adaptive thinking (header beta tidak didukung). Penalaran antar-alat berpindah ke blok pemikiran pada model ini. |
| **Pelestarian Blok Pemikiran** | Tidak dipertahankan di seluruh putaran | Tidak dipertahankan di seluruh putaran | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default.** Blok dihapus saat melanjutkan percakapan pada model yang tidak mendukung format pemikiran Mythos. |

### Pelestarian blok pemikiran di Claude Opus 4.5 dan yang lebih baru

Dimulai dengan Claude Opus 4.5 (dan berlanjut di Claude Opus 4.6), **blok pemikiran dari putaran asisten sebelumnya dipertahankan dalam konteks model secara default**. Ini berbeda dari model yang lebih awal, yang menghapus blok pemikiran dari putaran sebelumnya.

**Manfaat pelestarian blok pemikiran:**

- **Optimasi cache**: Saat menggunakan penggunaan alat, blok pemikiran yang dipertahankan memungkinkan cache hits karena mereka dilewatkan kembali dengan hasil alat dan di-cache secara bertahap di seluruh putaran asisten, menghasilkan penghematan token dalam alur kerja multi-langkah
- **Tidak ada dampak kecerdasan**: Mempertahankan blok pemikiran tidak memiliki efek negatif pada kinerja model

**Pertimbangan penting:**

- **Penggunaan konteks**: Percakapan panjang akan mengonsumsi lebih banyak ruang konteks karena blok pemikiran dipertahankan dalam konteks
- **Perilaku otomatis**: Ini adalah perilaku default untuk model Claude Opus 4.5 dan yang lebih baru (termasuk [Claude Mythos Preview](https://anthropic.com/glasswing) dan Claude Opus 4.6). Tidak ada perubahan kode atau header beta yang diperlukan
- **Kompatibilitas mundur**: Untuk memanfaatkan fitur ini, terus lewatkan blok pemikiran lengkap yang tidak dimodifikasi kembali ke API seperti yang Anda lakukan untuk penggunaan alat

<Note>
Untuk model yang lebih awal (Claude Sonnet 4.5, Opus 4.1, dll.), blok pemikiran dari putaran sebelumnya terus dihapus dari konteks. Perilaku yang ada yang dijelaskan dalam bagian [Extended thinking with prompt caching](#extended-thinking-with-prompt-caching) berlaku untuk model tersebut.
</Note>

## Harga

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

## Praktik terbaik dan pertimbangan untuk pemikiran yang diperluas

### Bekerja dengan anggaran pemikiran

- **Optimasi anggaran:** Anggaran minimum adalah 1.024 token. Mulai dengan minimum dan tingkatkan anggaran pemikiran secara bertahap untuk menemukan rentang optimal untuk kasus penggunaan Anda. Jumlah token yang lebih tinggi memungkinkan penalaran yang lebih komprehensif tetapi dengan hasil yang semakin berkurang tergantung pada tugas. Meningkatkan anggaran dapat meningkatkan kualitas respons dengan pertukaran peningkatan latensi. Untuk tugas-tugas penting, uji pengaturan yang berbeda untuk menemukan keseimbangan optimal. Perhatikan bahwa anggaran pemikiran adalah target daripada batas yang ketat. Penggunaan token aktual dapat bervariasi berdasarkan tugas.
- **Titik awal:** Mulai dengan anggaran pemikiran yang lebih besar (16k+ token) untuk tugas-tugas kompleks dan sesuaikan berdasarkan kebutuhan Anda.
- **Anggaran besar:** Untuk anggaran pemikiran di atas 32k, gunakan [batch processing](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Permintaan yang mendorong model untuk berpikir di atas 32k token menyebabkan permintaan yang berjalan lama yang mungkin berjalan melawan batas waktu sistem dan batas koneksi terbuka.
- **Pelacakan penggunaan token:** Pantau penggunaan token pemikiran untuk mengoptimalkan biaya dan kinerja.

### Pertimbangan kinerja

- **Waktu respons:** Bersiaplah untuk waktu respons yang lebih lama karena pemrosesan tambahan. Menghasilkan blok pemikiran meningkatkan waktu respons keseluruhan.
- **Persyaratan streaming:** SDK memerlukan streaming ketika `max_tokens` lebih besar dari 21.333 untuk menghindari timeout HTTP pada permintaan yang berjalan lama. Ini adalah validasi sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses acara secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani acara individual. Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail. Saat streaming, bersiaplah untuk menangani blok konten pemikiran dan teks saat mereka tiba.
- **Menghilangkan pemikiran untuk latensi:** Jika aplikasi Anda tidak menampilkan konten pemikiran, atur `display: "omitted"` pada konfigurasi pemikiran untuk mengurangi waktu-ke-token-teks-pertama. Lihat [Controlling thinking display](#controlling-thinking-display).

### Kompatibilitas fitur

- Pemikiran tidak kompatibel dengan modifikasi `temperature` atau `top_k` serta [forced tool use](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).
- Ketika pemikiran diaktifkan, Anda dapat mengatur `top_p` ke nilai antara 1 dan 0,95.
- Anda tidak dapat mengisi respons sebelumnya ketika pemikiran diaktifkan.
- Perubahan pada anggaran pemikiran membatalkan awalan prompt yang di-cache yang mencakup pesan. Namun, prompt sistem yang di-cache dan definisi alat akan terus berfungsi ketika parameter pemikiran berubah.

### Pedoman penggunaan

- **Pemilihan tugas:** Gunakan pemikiran yang diperluas untuk tugas-tugas yang sangat kompleks yang mendapat manfaat dari penalaran langkah demi langkah, seperti matematika, pengkodean, dan analisis.
- **Penanganan konteks:** Anda tidak perlu menghapus blok pemikiran sebelumnya sendiri. Claude API secara otomatis mengabaikan blok pemikiran dari putaran sebelumnya dan mereka tidak disertakan saat menghitung penggunaan konteks.
- **Rekayasa prompt:** Tinjau [tips prompting pemikiran yang diperluas](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities) jika Anda ingin memaksimalkan kemampuan pemikiran Claude.

## Langkah berikutnya

<CardGroup>
  <Card title="Coba buku masak pemikiran yang diperluas" icon="book" href="https://platform.claude.com/cookbook/extended-thinking-extended-thinking">
    Jelajahi contoh praktis pemikiran dalam buku masak.
  </Card>
  <Card title="Tips prompting pemikiran yang diperluas" icon="code" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities">
    Pelajari praktik terbaik rekayasa prompt untuk pemikiran yang diperluas.
  </Card>
</CardGroup>