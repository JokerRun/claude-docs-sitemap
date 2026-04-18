---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: b6a1d485348ca437f542fe4499c23eb410d4c7f06cbd36db3930d568ed9526f7
---

# Alat pencarian web

Alat pencarian web memberikan Claude akses langsung ke konten web real-time untuk menjawab pertanyaan dengan informasi terkini.

---

Alat pencarian web memberikan Claude akses langsung ke konten web real-time, memungkinkannya menjawab pertanyaan dengan informasi terkini di luar cutoff pengetahuannya. Respons mencakup kutipan untuk sumber yang diambil dari hasil pencarian.

Versi alat pencarian web terbaru (`web_search_20260209`) mendukung **penyaringan dinamis** dengan [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. Claude dapat menulis dan menjalankan kode untuk menyaring hasil pencarian sebelum mencapai jendela konteks, hanya menyimpan informasi yang relevan dan membuang sisanya. Ini menghasilkan respons yang lebih akurat sambil mengurangi konsumsi token. Versi alat sebelumnya (`web_search_20250305`) tetap tersedia tanpa penyaringan dinamis.

<Note>
Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), pencarian web didukung di Claude API, Microsoft Foundry, dan Google Vertex AI. Pencarian web tidak tersedia untuk Mythos Preview di Amazon Bedrock.
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

Untuk dukungan model, lihat [Tool reference](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja pencarian web

Ketika Anda menambahkan alat pencarian web ke permintaan API Anda:

1. Claude memutuskan kapan harus mencari berdasarkan prompt.
2. API menjalankan pencarian dan memberikan Claude dengan hasilnya. Proses ini dapat berulang beberapa kali selama satu permintaan.
3. Di akhir gilirannya, Claude memberikan respons akhir dengan sumber yang dikutip.

### Penyaringan dinamis

Pencarian web adalah tugas yang intensif token. Dengan pencarian web dasar, Claude perlu menarik hasil pencarian ke dalam konteks, mengambil HTML lengkap dari beberapa situs web, dan bernalar atas semuanya sebelum sampai pada jawaban. Seringkali, banyak konten ini tidak relevan, yang dapat menurunkan kualitas respons.

Dengan versi alat `web_search_20260209`, Claude dapat menulis dan menjalankan kode untuk memproses ulang hasil kueri. Alih-alih bernalar atas file HTML lengkap, Claude secara dinamis menyaring hasil pencarian sebelum memuatnya ke dalam konteks, hanya menyimpan apa yang relevan dan membuang sisanya.

Penyaringan dinamis sangat efektif untuk:
- Pencarian melalui dokumentasi teknis
- Tinjauan literatur dan verifikasi kutipan
- Penelitian teknis
- Grounding respons dan verifikasi

<Note>
Penyaringan dinamis memerlukan [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan. Alat pencarian web yang ditingkatkan tersedia di Claude API dan Microsoft Azure. Di Google Vertex AI, alat pencarian web dasar (tanpa penyaringan dinamis) tersedia.
</Note>

Untuk mengaktifkan penyaringan dinamis, gunakan versi alat `web_search_20260209`:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
            }
        ],
        "tools": [{
            "type": "web_search_20260209",
            "name": "web_search"
        }]
    }'
```

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-7
max_tokens: 4096
messages:
  - role: user
    content: >-
      Search for the current prices of AAPL and GOOGL, then calculate
      which has a better P/E ratio.
tools:
  - type: web_search_20260209
    name: web_search
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.",
        }
    ],
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
)
print(response)
```

```typescript TypeScript nocheck hidelines={1..5,-3..-1}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const response = await anthropic.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
      }
    ],
    tools: [{ type: "web_search_20260209", name: "web_search" }]
  });

  console.log(response);
}

main().catch(console.error);
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
            MaxTokens = 4096,
            Messages = [new() { Role = Role.User, Content = "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio." }],
            Tools = [new ToolUnion(new WebSearchTool20260209())]
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
		MaxTokens: 4096,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfWebSearchTool20260209: &anthropic.WebSearchTool20260209Param{}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..5,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebSearchTool20260209;

public class WebSearchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(4096L)
            .addUserMessage("Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.")
            .addTool(WebSearchTool20260209.builder().build())
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

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio.'],
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'type' => 'web_search_20260209',
            'name' => 'web_search',
        ],
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  messages: [
    { role: "user", content: "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio." }
  ],
  tools: [{
    type: "web_search_20260209",
    name: "web_search"
  }]
)
puts message
```
</CodeGroup>

## Cara menggunakan pencarian web

<Note>
Administrator organisasi Anda harus mengaktifkan pencarian web di [Claude Console](/settings/privacy).
</Note>

Sediakan alat pencarian web dalam permintaan API Anda:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "What is the weather in NYC?"
            }
        ],
        "tools": [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }]
    }'
```

```bash CLI
ant messages create \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --message '{role: user, content: What is the weather in NYC?}' \
  --tool '{type: web_search_20250305, name: web_search, max_uses: 5}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
)
print(response)
```

```typescript TypeScript hidelines={1..5,-3..-1}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in NYC?"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 5
      }
    ]
  });

  console.log(response);
}

main().catch(console.error);
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
            MaxTokens = 1024,
            Messages = [new() { Role = Role.User, Content = "What's the weather in NYC?" }],
            Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 5 })]
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
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in NYC?")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
				MaxUses: anthropic.Int(5),
			}},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..5,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebSearchTool20250305;

public class WebSearchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(1024L)
            .addUserMessage("What's the weather in NYC?")
            .addTool(WebSearchTool20250305.builder()
                .maxUses(5L)
                .build())
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

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "What's the weather in NYC?"],
    ],
    model: 'claude-opus-4-7',
    tools: [
        [
            'type' => 'web_search_20250305',
            'name' => 'web_search',
            'max_uses' => 5,
        ],
    ],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What's the weather in NYC?" }
  ],
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 5
  }]
)
puts message
```
</CodeGroup>

### Definisi alat

Alat pencarian web mendukung parameter berikut:

```json JSON
{
  "type": "web_search_20250305",
  "name": "web_search",

  // Opsional: Batasi jumlah pencarian per permintaan
  "max_uses": 5,

  // Opsional: Hanya sertakan hasil dari domain ini
  "allowed_domains": ["example.com", "trusteddomain.org"],

  // Opsional: Jangan pernah sertakan hasil dari domain ini
  "blocked_domains": ["untrustedsource.com"],

  // Opsional: Lokalisasi hasil pencarian
  "user_location": {
    "type": "approximate",
    "city": "San Francisco",
    "region": "California",
    "country": "US",
    "timezone": "America/Los_Angeles"
  }
}
```

#### Max uses

Parameter `max_uses` membatasi jumlah pencarian yang dilakukan. Jika Claude mencoba lebih banyak pencarian daripada yang diizinkan, `web_search_tool_result` adalah kesalahan dengan kode kesalahan `max_uses_exceeded`.

#### Penyaringan domain

Untuk penyaringan domain dengan `allowed_domains` dan `blocked_domains`, lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

#### Lokalisasi

Parameter `user_location` memungkinkan Anda untuk melokalisasi hasil pencarian berdasarkan lokasi pengguna.

- `type`: Jenis lokasi (harus `approximate`)
- `city`: Nama kota
- `region`: Wilayah atau negara bagian
- `country`: Negara
- `timezone`: [ID zona waktu IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Respons

Berikut adalah contoh struktur respons:

```json Output
{
  "role": "assistant",
  "content": [
    // 1. Keputusan Claude untuk mencari
    {
      "type": "text",
      "text": "I'll search for when Claude Shannon was born."
    },
    // 2. Kueri pencarian yang digunakan
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "name": "web_search",
      "input": {
        "query": "claude shannon birth date"
      }
    },
    // 3. Hasil pencarian
    {
      "type": "web_search_tool_result",
      "tool_use_id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "content": [
        {
          "type": "web_search_result",
          "url": "https://en.wikipedia.org/wiki/Claude_Shannon",
          "title": "Claude Shannon - Wikipedia",
          "encrypted_content": "EqgfCioIARgBIiQ3YTAwMjY1Mi1mZjM5LTQ1NGUtODgxNC1kNjNjNTk1ZWI3Y...",
          "page_age": "April 30, 2025"
        }
      ]
    },
    {
      "text": "Based on the search results, ",
      "type": "text"
    },
    // 4. Respons Claude dengan kutipan
    {
      "text": "Claude Shannon was born on April 30, 1916, in Petoskey, Michigan",
      "type": "text",
      "citations": [
        {
          "type": "web_search_result_location",
          "url": "https://en.wikipedia.org/wiki/Claude_Shannon",
          "title": "Claude Shannon - Wikipedia",
          "encrypted_index": "Eo8BCioIAhgBIiQyYjQ0OWJmZi1lNm..",
          "cited_text": "Claude Elwood Shannon (April 30, 1916 – February 24, 2001) was an American mathematician, electrical engineer, computer scientist, cryptographer and i..."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 6039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_search_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

#### Hasil pencarian

Hasil pencarian mencakup:

- `url`: URL halaman sumber
- `title`: Judul halaman sumber
- `page_age`: Kapan situs terakhir diperbarui
- `encrypted_content`: Konten terenkripsi yang harus diteruskan kembali dalam percakapan multi-turn untuk kutipan

#### Kutipan

Kutipan selalu diaktifkan untuk pencarian web, dan setiap `web_search_result_location` mencakup:

- `url`: URL sumber yang dikutip
- `title`: Judul sumber yang dikutip
- `encrypted_index`: Referensi yang harus diteruskan kembali untuk percakapan multi-turn.
- `cited_text`: Hingga 150 karakter konten yang dikutip

Bidang kutipan pencarian web `cited_text`, `title`, dan `url` tidak dihitung terhadap penggunaan token input atau output.

<Note>
  Saat menampilkan output API secara langsung kepada pengguna akhir, kutipan harus disertakan ke sumber asli. Jika Anda membuat modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan kutipan sesuai kebutuhan berdasarkan konsultasi dengan tim hukum Anda.
</Note>

#### Kesalahan

Ketika alat pencarian web mengalami kesalahan (seperti mencapai batas laju), Claude API masih mengembalikan respons 200 (sukses). Kesalahan direpresentasikan dalam badan respons menggunakan struktur berikut:

```json Output
{
  "type": "web_search_tool_result",
  "tool_use_id": "servertoolu_a93jad",
  "content": {
    "type": "web_search_tool_result_error",
    "error_code": "max_uses_exceeded"
  }
}
```

Ini adalah kode kesalahan yang mungkin:

- `too_many_requests`: Batas laju terlampaui
- `invalid_input`: Parameter kueri pencarian tidak valid
- `max_uses_exceeded`: Penggunaan alat pencarian web maksimal terlampaui
- `query_too_long`: Kueri melebihi panjang maksimal
- `unavailable`: Kesalahan internal terjadi

#### Alasan penghentian `pause_turn`

Untuk melanjutkan setelah alasan penghentian `pause_turn`, lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn).

## Prompt caching

Untuk caching definisi alat di seluruh turn, lihat [Tool use with prompt caching](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Dengan streaming diaktifkan, Anda akan menerima peristiwa pencarian sebagai bagian dari aliran. Akan ada jeda saat pencarian dijalankan:

```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Keputusan Claude untuk mencari

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_search"}}

// Kueri pencarian dialirkan
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"query\":\"latest quantum computing breakthroughs 2025\"}"}}

// Jeda saat pencarian dijalankan

// Hasil pencarian dialirkan
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": [{"type": "web_search_result", "title": "Quantum Computing Breakthroughs in 2025", "url": "https://example.com"}]}}

// Respons Claude dengan kutipan (dihilangkan dalam contoh ini)
```

## Permintaan batch

Anda dapat menyertakan alat pencarian web dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat pencarian web melalui Messages Batches API dihargai sama dengan yang ada dalam permintaan Messages API reguler.

## Penggunaan dan harga

Web search usage is charged in addition to token usage:

```json
"usage": {
  "input_tokens": 105,
  "output_tokens": 6039,
  "cache_read_input_tokens": 7123,
  "cache_creation_input_tokens": 7345,
  "server_tool_use": {
    "web_search_requests": 1
  }
}
```

Web search is available on the Claude API for **$10 per 1,000 searches**, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/server-tools" title="Server tools">
    Mekanik bersama untuk alat yang dijalankan Anthropic.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Tool reference">
    Direktori semua alat yang disediakan Anthropic.
  </Card>
</CardGroup>