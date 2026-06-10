---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 76d2834b0c6e031f0e67de8fa2091f07b3036068ba47da117e78fbbbf2fcde55
---

# Alat server

Bekerja dengan alat yang dieksekusi Anthropic: blok server_tool_use, kelanjutan pause_turn, dan pemfilteran domain.

---

Halaman ini membahas mekanisme bersama dari alat yang dieksekusi server: blok `server_tool_use`, kelanjutan `pause_turn`, pertimbangan ZDR, dan pemfilteran domain. Untuk alat individual, lihat [referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Blok server_tool_use \{#the-server-tool-use-block}

Blok `server_tool_use` muncul dalam respons Claude ketika alat yang dieksekusi server dijalankan. Field `id`-nya menggunakan prefiks `srvtoolu_` untuk membedakannya dari panggilan alat klien:

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_01A2B3C4D5E6F7G8H9",
  "name": "web_search",
  "input": { "query": "latest quantum computing breakthroughs" }
}
```

API mengeksekusi alat tersebut secara internal. Anda melihat panggilan dan hasilnya dalam respons, tetapi Anda tidak menangani eksekusinya. Tidak seperti blok `tool_use` klien, Anda tidak perlu merespons dengan `tool_result`. Blok hasil muncul segera setelah blok `server_tool_use` dalam giliran asisten yang sama.

## Loop sisi server dan pause_turn \{#the-server-side-loop-and-pause-turn}

Saat menggunakan alat server seperti pencarian web, API dapat mengembalikan stop reason `pause_turn`, yang menunjukkan bahwa API telah menjeda giliran yang berjalan lama.

Berikut cara menangani stop reason `pause_turn`:

<CodeGroup>
```python Python hidelines={1..4}
import anthropic

client = anthropic.Anthropic()

# Permintaan awal dengan pencarian web
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        }
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
)

# Periksa apakah respons memiliki stop_reason pause_turn
if response.stop_reason == "pause_turn":
    # Lanjutkan percakapan dengan konten yang dijeda
    messages = [
        {
            "role": "user",
            "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
        },
        {"role": "assistant", "content": response.content},
    ]

    # Kirim permintaan lanjutan
    continuation = client.messages.create(
        model="claude-opus-4-8",
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
  // Permintaan awal dengan pencarian web
  const response = await client.messages.create({
    model: "claude-opus-4-8",
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

  // Periksa apakah respons memiliki stop_reason pause_turn
  if (response.stop_reason === "pause_turn") {
    // Lanjutkan percakapan dengan konten yang dijeda
    const messages: Anthropic.MessageParam[] = [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      { role: "assistant", content: response.content }
    ];

    // Kirim permintaan lanjutan
    const continuation = await client.messages.create({
      model: "claude-opus-4-8",
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
            Model = "claude-opus-4-8",
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
                Model = "claude-opus-4-8",
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
		Model:     anthropic.ModelClaudeOpus4_8,
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
		// Konversi konten respons ke tipe param untuk pesan asisten
		var contentParams []anthropic.ContentBlockParamUnion
		for _, block := range response.Content {
			contentParams = append(contentParams, block.ToParam())
		}

		continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
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
        .model("claude-opus-4-8")
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
            .model("claude-opus-4-8")
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

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
        ]
    ],
    model: 'claude-opus-4-8',
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
        model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
- **Lanjutkan percakapan:** Kirim kembali respons yang dijeda apa adanya dalam permintaan berikutnya agar Claude dapat melanjutkan gilirannya
- **Modifikasi jika diperlukan:** Anda dapat secara opsional memodifikasi konten sebelum melanjutkan jika Anda ingin menginterupsi atau mengalihkan percakapan
- **Pertahankan status alat:** Sertakan alat yang sama dalam permintaan kelanjutan untuk mempertahankan fungsionalitas

## ZDR dan allowed_callers \{#zdr-and-allowed-callers}

Versi dasar dari pencarian web (`web_search_20250305`) dan pengambilan web (`web_fetch_20250910`) memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/manage-claude/api-and-data-retention).

Versi `_20260209` dengan pemfilteran dinamis **tidak** memenuhi syarat ZDR secara default karena pemfilteran dinamis bergantung pada eksekusi kode secara internal.

Untuk menggunakan alat server `_20260209` dengan ZDR, nonaktifkan pemfilteran dinamis dengan mengatur `"allowed_callers": ["direct"]` pada alat tersebut:

```json
{
  "type": "web_search_20260209",
  "name": "web_search",
  "allowed_callers": ["direct"]
}
```

Ini membatasi alat hanya untuk pemanggilan langsung, melewati langkah eksekusi kode internal.

<Note>
Bahkan ketika pengambilan web digunakan dalam konfigurasi yang memenuhi syarat ZDR, penerbit situs web dapat menyimpan parameter apa pun yang diteruskan ke URL jika Claude mengambil konten dari situs mereka.
</Note>

## Pemfilteran domain \{#domain-filtering}

Alat server yang mengakses web menerima parameter `allowed_domains` dan `blocked_domains` untuk mengontrol domain mana yang dapat dijangkau Claude.

Saat menggunakan filter domain:

- Domain tidak boleh menyertakan skema HTTP/HTTPS (gunakan `example.com` alih-alih `https://example.com`)
- Subdomain disertakan secara otomatis (`example.com` mencakup `docs.example.com`)
- Subdomain spesifik membatasi hasil hanya ke subdomain tersebut (`docs.example.com` hanya mengembalikan hasil dari subdomain tersebut, bukan dari `example.com` atau `api.example.com`)
- Subpath didukung dan mencocokkan apa pun setelah path tersebut (`example.com/blog` cocok dengan `example.com/blog/post-1`)
- Anda dapat menggunakan `allowed_domains` atau `blocked_domains`, tetapi tidak keduanya dalam permintaan yang sama

**Dukungan wildcard:**

- Hanya satu wildcard (`*`) yang diizinkan per entri domain, dan harus muncul setelah bagian domain (di dalam path)
- Valid: `example.com/*`, `example.com/*/articles`
- Tidak valid: `*.example.com`, `ex*.com`, `example.com/*/news/*`

Format domain yang tidak valid mengembalikan error alat `invalid_tool_input`.

<Note>
Pembatasan domain tingkat permintaan harus kompatibel dengan pembatasan domain tingkat organisasi yang dikonfigurasi di Claude Console. Domain tingkat permintaan hanya dapat membatasi domain lebih lanjut, bukan menimpa atau memperluas melampaui daftar tingkat organisasi. Jika permintaan Anda menyertakan domain yang bertentangan dengan pengaturan organisasi, API mengembalikan error validasi.
</Note>

<Warning>
Perlu diketahui bahwa karakter Unicode dalam nama domain dapat menciptakan kerentanan keamanan melalui serangan homograf, di mana karakter yang secara visual mirip dari skrip yang berbeda dapat melewati filter domain. Misalnya, `аmazon.com` (menggunakan 'а' Sirilik) mungkin tampak identik dengan `amazon.com` tetapi mewakili domain yang berbeda.

Saat mengonfigurasi daftar izin/blokir domain:
- Gunakan nama domain ASCII saja jika memungkinkan
- Pertimbangkan bahwa parser URL mungkin menangani normalisasi Unicode secara berbeda
- Uji filter domain Anda dengan variasi homograf potensial
- Audit konfigurasi domain Anda secara berkala untuk karakter Unicode yang mencurigakan
</Warning>

## Pemfilteran dinamis dengan eksekusi kode \{#dynamic-filtering-with-code-execution}

Versi `_20260209` dari pencarian web dan pengambilan web menggunakan eksekusi kode secara internal untuk menerapkan filter dinamis terhadap hasil pencarian.

<Warning>
Menyertakan alat `code_execution` mandiri bersama dengan versi `_20260209` dari alat web akan menciptakan dua lingkungan eksekusi, yang dapat membingungkan model. Gunakan salah satu saja, atau sematkan keduanya ke versi yang sama.
</Warning>

## Streaming event alat server \{#streaming-server-tool-events}

Event alat server di-stream sebagai bagian dari alur SSE normal. Blok `server_tool_use` dan hasilnya tiba sebagai event `content_block_start` dan `content_block_delta`, dengan cara yang sama seperti teks dan panggilan alat klien di-stream.

Lihat [Streaming](/docs/id/build-with-claude/streaming) untuk referensi event lengkap. Halaman alat individual mendokumentasikan nama event spesifik alat jika berbeda.

## Permintaan batch \{#batch-requests}

Semua alat server mendukung pemrosesan batch. Dalam sebuah batch, loop agentik berjalan sama seperti pada permintaan sinkron, dengan batas iterasi per giliran yang lebih tinggi. Jika loop mencapai batas tersebut, respons berakhir dengan `stop_reason: "pause_turn"`; Anda dapat melanjutkannya dengan mengirimkan permintaan lanjutan berisi konten yang dikembalikan. Lihat [Alat server dan loop agentik](/docs/id/build-with-claude/batch-processing#server-tools-and-the-agentic-loop) untuk detailnya.

Beban kerja batch yang umum untuk alat server meliputi memperkaya dataset atau katalog dengan informasi yang diambil dari web, memeriksa sekumpulan besar dokumen terhadap sumber terkini, memantau daftar halaman atau topik dari waktu ke waktu, dan menjalankan kode analisis pada banyak file.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Pencarian web" icon="magnifying-glass" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Cari di web dan kutip hasilnya.
  </Card>
  <Card title="Pengambilan web" icon="globe" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil konten dari URL tertentu.
  </Card>
  <Card title="Eksekusi kode" icon="terminal" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan Python dalam kontainer sandbox.
  </Card>
  <Card title="Pencarian alat" icon="list-magnifying-glass" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Temukan dan muat alat sesuai kebutuhan.
  </Card>
</CardGroup>