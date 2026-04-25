---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 5ed9e48c18223817f4edc1202a40b0ad145458a6d91ce570f049574e77e07cf8
---

# Alat server

Bekerja dengan alat yang dieksekusi Anthropic: blok server_tool_use, kelanjutan pause_turn, dan penyaringan domain.

---

Halaman ini mencakup mekanika bersama alat yang dieksekusi server: blok `server_tool_use`, kelanjutan `pause_turn`, pertimbangan ZDR, dan penyaringan domain. Untuk alat individual, lihat [referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Blok server_tool_use

Blok `server_tool_use` muncul dalam respons Claude ketika alat yang dieksekusi server berjalan. Bidang `id` menggunakan awalan `srvtoolu_` untuk membedakannya dari panggilan alat klien:

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_01A2B3C4D5E6F7G8H9",
  "name": "web_search",
  "input": { "query": "latest quantum computing breakthroughs" }
}
```

API mengeksekusi alat secara internal. Anda melihat panggilan dan hasilnya dalam respons, tetapi Anda tidak menangani eksekusi. Tidak seperti blok `tool_use` klien, Anda tidak perlu merespons dengan `tool_result`. Blok hasil muncul segera setelah blok `server_tool_use` dalam giliran asisten yang sama.

## Loop sisi server dan pause_turn

Saat menggunakan alat server seperti pencarian web, API dapat mengembalikan alasan penghentian `pause_turn`, menunjukkan bahwa API telah menjeda giliran yang berjalan lama.

Berikut cara menangani alasan penghentian `pause_turn`:

<CodeGroup>
```python Python hidelines={1..4}
import anthropic

client = anthropic.Anthropic()

# Initial request with web search
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        }
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
)

# Check if the response has pause_turn stop reason
if response.stop_reason == "pause_turn":
    # Continue the conversation with the paused content
    messages = [
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        },
        {"role": "assistant", "content": response.content},
    ]

    # Send the continuation request
    continuation = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
    )

    print(continuation)
else:
    print(response)
```

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  // Initial request with web search
  const response = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  });

  // Check if the response has pause_turn stop reason
  if (response.stop_reason === "pause_turn") {
    // Continue the conversation with the paused content
    const messages: Anthropic.MessageParam[] = [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      { role: "assistant", content: response.content }
    ];

    // Send the continuation request
    const continuation = await client.messages.create({
      model: "claude-opus-4-7",
      max_tokens: 1024,
      messages: messages,
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 10
        }
      ]
    });

    console.log(continuation);
  } else {
    console.log(response);
  }
}

main().catch(console.error);
```

```csharp C#
using Anthropic;
using Anthropic.Models.Messages;
using System;
using System.Linq;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-opus-4-7",
            MaxTokens = 1024,
            Messages = [
                new() {
                    Role = Role.User,
                    Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
                }
            ],
            Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 10 })]
        };

        var response = await client.Messages.Create(parameters);

        if (response.StopReason == "pause_turn")
        {
            var continuationParams = new MessageCreateParams
            {
                Model = "claude-opus-4-7",
                MaxTokens = 1024,
                Messages = [
                    new() {
                        Role = Role.User,
                        Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
                    },
                    new() {
                        Role = Role.Assistant,
                        Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
                    }
                ],
                Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 10 })]
            };

            var continuation = await client.Messages.Create(continuationParams);
            Console.WriteLine(continuation);
        }
        else
        {
            Console.WriteLine(response);
        }
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

	webSearchTool := []anthropic.ToolUnionParam{
		{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
			MaxUses: anthropic.Int(10),
		}},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
		},
		Tools: webSearchTool,
	})
	if err != nil {
		log.Fatal(err)
	}

	if response.StopReason == "pause_turn" {
		// Convert response content to param types for the assistant message
		var contentParams []anthropic.ContentBlockParamUnion
		for _, block := range response.Content {
			contentParams = append(contentParams, block.ToParam())
		}

		continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_7,
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{
				anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
				anthropic.NewAssistantMessage(contentParams...),
			},
			Tools: webSearchTool,
		})
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(continuation)
	} else {
		fmt.Println(response)
	}
}
```

```java Java hidelines={1..4,7..8,-1..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.WebSearchTool20250305;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model("claude-opus-4-7")
        .maxTokens(1024L)
        .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
        .addTool(WebSearchTool20250305.builder()
            .maxUses(10L)
            .build())
        .build();

    Message response = client.messages().create(params);

    if (response.stopReason().isPresent()
            && response.stopReason().get().equals(StopReason.PAUSE_TURN)) {
        MessageCreateParams continuationParams = MessageCreateParams.builder()
            .model("claude-opus-4-7")
            .maxTokens(1024L)
            .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
            .addMessage(response)
            .addTool(WebSearchTool20250305.builder()
                .maxUses(10L)
                .build())
            .build();

        Message continuation = client.messages().create(continuationParams);
        IO.println(continuation);
    } else {
        IO.println(response);
    }
}
```

```php PHP hidelines={1..6}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
        ]
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'type' => 'web_search_20250305',
            'name' => 'web_search',
            'max_uses' => 10
        ]
    ],
);

if ($response->stopReason === 'pause_turn') {
    $messages = [
        [
            'role' => 'user',
            'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
        ],
        [
            'role' => 'assistant',
            'content' => $response->content
        ]
    ];

    $continuation = $client->messages->create(
        maxTokens: 1024,
        messages: $messages,
        model: 'claude-opus-4-7',
        tools: [
            [
                'type' => 'web_search_20250305',
                'name' => 'web_search',
                'max_uses' => 10
            ]
        ],
    );

    echo $continuation;
} else {
    echo $response;
}
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content:
        "Search for comprehensive information about quantum computing breakthroughs in 2025"
    }
  ],
  tools: [
    {
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 10
    }
  ]
)

if response.stop_reason == :pause_turn
  messages = [
    {
      role: "user",
      content: "Search for comprehensive information about quantum computing breakthroughs in 2025"
    },
    {
      role: "assistant",
      content: response.content
    }
  ]

  continuation = client.messages.create(
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: messages,
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  )

  puts continuation
else
  puts response
end
```
</CodeGroup>

Saat menangani `pause_turn`:
- **Lanjutkan percakapan:** Teruskan respons yang dijeda kembali apa adanya dalam permintaan berikutnya untuk membiarkan Claude melanjutkan gilirannya
- **Modifikasi jika diperlukan:** Anda dapat secara opsional memodifikasi konten sebelum melanjutkan jika Anda ingin mengganggu atau mengalihkan percakapan
- **Pertahankan status alat:** Sertakan alat yang sama dalam permintaan kelanjutan untuk mempertahankan fungsionalitas

## ZDR dan allowed_callers

Versi dasar pencarian web (`web_search_20250305`) dan pengambilan web (`web_fetch_20250910`) memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/zero-data-retention).

Versi `_20260209` dengan penyaringan dinamis **bukan** memenuhi syarat ZDR secara default karena penyaringan dinamis bergantung pada eksekusi kode secara internal.

Untuk menggunakan alat server `_20260209` dengan ZDR, nonaktifkan penyaringan dinamis dengan menetapkan `"allowed_callers": ["direct"]` pada alat:

```json
{
  "type": "web_search_20260209",
  "name": "web_search",
  "allowed_callers": ["direct"]
}
```

Ini membatasi alat hanya untuk pemanggilan langsung, melewati langkah eksekusi kode internal.

<Note>
Meskipun alat pengambilan web itu sendiri memenuhi syarat ZDR, penerbit situs web dapat mempertahankan parameter apa pun yang diteruskan ke URL jika Claude mengambil konten dari situs mereka.
</Note>

## Penyaringan domain

Alat server yang mengakses web menerima parameter `allowed_domains` dan `blocked_domains` untuk mengontrol domain mana yang dapat dijangkau Claude.

Saat menggunakan filter domain:

- Domain tidak boleh menyertakan skema HTTP/HTTPS (gunakan `example.com` bukan `https://example.com`)
- Subdomain secara otomatis disertakan (`example.com` mencakup `docs.example.com`)
- Subdomain spesifik membatasi hasil hanya ke subdomain itu (`docs.example.com` mengembalikan hanya hasil dari subdomain itu, bukan dari `example.com` atau `api.example.com`)
- Subpath didukung dan cocok dengan apa pun setelah path (`example.com/blog` cocok dengan `example.com/blog/post-1`)
- Anda dapat menggunakan `allowed_domains` atau `blocked_domains`, tetapi tidak keduanya dalam permintaan yang sama

**Dukungan wildcard:**

- Hanya satu wildcard (`*`) yang diizinkan per entri domain, dan harus muncul setelah bagian domain (di path)
- Valid: `example.com/*`, `example.com/*/articles`
- Tidak valid: `*.example.com`, `ex*.com`, `example.com/*/news/*`

Format domain yang tidak valid mengembalikan kesalahan alat `invalid_tool_input`.

<Note>
Pembatasan domain tingkat permintaan harus kompatibel dengan pembatasan domain tingkat organisasi yang dikonfigurasi di Console. Domain tingkat permintaan hanya dapat membatasi domain lebih lanjut, bukan mengganti atau memperluas di luar daftar tingkat organisasi. Jika permintaan Anda menyertakan domain yang bertentangan dengan pengaturan organisasi, API mengembalikan kesalahan validasi.
</Note>

<Warning>
Waspadai bahwa karakter Unicode dalam nama domain dapat menciptakan kerentanan keamanan melalui serangan homograf, di mana karakter yang terlihat serupa dari skrip berbeda dapat melewati filter domain. Misalnya, `аmazon.com` (menggunakan 'а' Cyrillic) mungkin terlihat identik dengan `amazon.com` tetapi mewakili domain yang berbeda.

Saat mengonfigurasi daftar izin/blokir domain:
- Gunakan nama domain ASCII-only jika memungkinkan
- Pertimbangkan bahwa parser URL dapat menangani normalisasi Unicode secara berbeda
- Uji filter domain Anda dengan variasi homograf potensial
- Audit konfigurasi domain Anda secara teratur untuk karakter Unicode yang mencurigakan
</Warning>

## Penyaringan dinamis dengan eksekusi kode

Versi `_20260209` dari pencarian web dan pengambilan web menggunakan eksekusi kode secara internal untuk menerapkan filter dinamis terhadap hasil pencarian.

<Warning>
Menyertakan alat `code_execution` mandiri bersama versi `_20260209` dari alat web menciptakan dua lingkungan eksekusi, yang dapat membingungkan model. Gunakan satu atau yang lain, atau pin keduanya ke versi yang sama.
</Warning>

## Streaming acara alat server

Acara alat server streaming sebagai bagian dari aliran SSE normal. Blok `server_tool_use` dan hasilnya tiba sebagai acara `content_block_start` dan `content_block_delta`, dengan cara yang sama teks dan panggilan alat klien stream.

Lihat [Streaming](/docs/id/build-with-claude/streaming) untuk referensi acara lengkap. Halaman alat individual mendokumentasikan nama acara khusus alat di mana mereka berbeda.

## Permintaan batch

Semua alat server mendukung pemrosesan batch. Lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing).

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Pencarian web" icon="magnifying-glass" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Cari web dan kutip hasil.
  </Card>
  <Card title="Pengambilan web" icon="globe" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil konten dari URL spesifik.
  </Card>
  <Card title="Eksekusi kode" icon="terminal" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan Python dalam kontainer bersandbox.
  </Card>
  <Card title="Pencarian alat" icon="list-magnifying-glass" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Temukan dan muat alat sesuai permintaan.
  </Card>
</CardGroup>