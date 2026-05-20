---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-05-20T03:15:44.945478Z
sha256: b190f053cea116b8b229058cfcf6e04b9c60d2d21b7feb3340bbfd9759c5c4f4
---

# Alat web fetch

Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.

---

Alat web fetch memungkinkan Claude untuk mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi alat web fetch terbaru (`web_fetch_20260209`) mendukung **penyaringan dinamis** dengan [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. Claude dapat menulis dan menjalankan kode untuk menyaring konten yang diambil sebelum mencapai jendela konteks, hanya menyimpan informasi yang relevan dan membuang sisanya. Ini mengurangi konsumsi token sambil mempertahankan kualitas respons. Versi alat sebelumnya (`web_fetch_20250910`) tetap tersedia tanpa penyaringan dinamis.

<Note>
Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), web fetch didukung di Claude API dan Microsoft Foundry saja. Tidak tersedia untuk Mythos Preview di Amazon Bedrock atau Google Vertex AI.
</Note>

<Note>
Gunakan [formulir umpan balik](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan umpan balik tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

<Warning>
Mengaktifkan alat web fetch di lingkungan di mana Claude memproses input yang tidak terpercaya bersama data sensitif menimbulkan risiko eksfiltrasi data. Hanya gunakan alat ini di lingkungan terpercaya atau saat menangani data non-sensitif.

Untuk meminimalkan risiko eksfiltrasi, Claude tidak diizinkan untuk secara dinamis membangun URL. Claude hanya dapat mengambil URL yang telah secara eksplisit disediakan oleh pengguna atau yang berasal dari hasil pencarian web atau web fetch sebelumnya. Namun, masih ada risiko sisa yang harus dipertimbangkan dengan hati-hati saat menggunakan alat ini.

Jika eksfiltrasi data menjadi perhatian, pertimbangkan:
- Menonaktifkan alat web fetch sepenuhnya
- Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
- Menggunakan parameter `allowed_domains` untuk membatasi ke domain yang dikenal aman
</Warning>

Untuk dukungan model, lihat [Tool reference](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja web fetch

Saat Anda menambahkan alat web fetch ke permintaan API Anda:

1. Claude memutuskan kapan harus mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, ekstraksi teks otomatis dilakukan.
4. Claude menganalisis konten yang diambil dan memberikan respons dengan kutipan opsional.

<Note>
Alat web fetch saat ini tidak mendukung situs web yang dirender secara dinamis melalui JavaScript.
</Note>

### Penyaringan dinamis

Mengambil halaman web dan PDF lengkap dapat dengan cepat mengonsumsi token, terutama ketika hanya informasi spesifik yang diperlukan dari dokumen besar. Dengan versi alat `web_fetch_20260209`, Claude dapat menulis dan menjalankan kode untuk menyaring konten yang diambil sebelum memuatnya ke dalam konteks.

Penyaringan dinamis ini sangat berguna untuk:
- Mengekstrak bagian tertentu dari dokumen panjang
- Memproses data terstruktur dari halaman web
- Menyaring informasi yang relevan dari PDF
- Mengurangi biaya token saat bekerja dengan dokumen besar

<Note>
Penyaringan dinamis memerlukan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan. Alat web fetch (dengan dan tanpa penyaringan dinamis) tersedia di Claude API dan Microsoft Azure.
</Note>

Untuk mengaktifkan penyaringan dinamis, gunakan versi alat `web_fetch_20260209`:

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
                "content": "Fetch the content at https://example.com/research-paper and extract the key findings."
            }
        ],
        "tools": [{
            "type": "web_fetch_20260209",
            "name": "web_fetch"
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
      Fetch the content at https://example.com/research-paper
      and extract the key findings.
tools:
  - type: web_fetch_20260209
    name: web_fetch
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
            "content": "Fetch the content at https://example.com/research-paper and extract the key findings.",
        }
    ],
    tools=[{"type": "web_fetch_20260209", "name": "web_fetch"}],
)
print(response)
```

```typescript TypeScript hidelines={1..5,-3..-1}
import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

async function main() {
  const response = await anthropic.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Fetch the content at https://example.com/research-paper and extract the key findings."
      }
    ],
    tools: [{ type: "web_fetch_20260209", name: "web_fetch" }]
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
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 4096,
            Messages = [new() { Role = Role.User, Content = "Fetch the content at https://example.com/research-paper and extract the key findings." }],
            Tools = [new ToolUnion(new WebFetchTool20260209())]
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
			anthropic.NewUserMessage(anthropic.NewTextBlock("Fetch the content at https://example.com/research-paper and extract the key findings.")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfWebFetchTool20260209: &anthropic.WebFetchTool20260209Param{}},
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
import com.anthropic.models.messages.WebFetchTool20260209;

public class WebFetchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(4096L)
            .addUserMessage("Fetch the content at https://example.com/research-paper and extract the key findings.")
            .addTool(WebFetchTool20260209.builder().build())
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
        ['role' => 'user', 'content' => 'Fetch the content at https://example.com/research-paper and extract the key findings.']
    ],
    model: 'claude-opus-4-7',
    tools: [[
        'type' => 'web_fetch_20260209',
        'name' => 'web_fetch',
    ]],
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
    { role: "user", content: "Fetch the content at https://example.com/research-paper and extract the key findings." }
  ],
  tools: [{
    type: "web_fetch_20260209",
    name: "web_fetch"
  }]
)
puts message
```
</CodeGroup>

## Cara menggunakan web fetch

Sediakan alat web fetch dalam permintaan API Anda:

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
                "content": "Please analyze the content at https://example.com/article"
            }
        ],
        "tools": [{
            "type": "web_fetch_20250910",
            "name": "web_fetch",
            "max_uses": 5
        }]
    }'
```

```bash CLI
ant messages create \
  --model claude-opus-4-7 \
  --max-tokens 1024 \
  --message '{role: user, content: "Please analyze the content at https://example.com/article"}' \
  --tool '{type: web_fetch_20250910, name: web_fetch, max_uses: 5}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Please analyze the content at https://example.com/article",
        }
    ],
    tools=[{"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5}],
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
        content: "Please analyze the content at https://example.com/article"
      }
    ],
    tools: [
      {
        type: "web_fetch_20250910",
        name: "web_fetch",
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
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 1024,
            Messages = [new() { Role = Role.User, Content = "Please analyze the content at https://example.com/article" }],
            Tools = [new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 })]
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
			anthropic.NewUserMessage(anthropic.NewTextBlock("Please analyze the content at https://example.com/article")),
		},
		Tools: []anthropic.ToolUnionParam{
			{OfWebFetchTool20250910: &anthropic.WebFetchTool20250910Param{
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
import com.anthropic.models.messages.WebFetchTool20250910;

public class WebFetchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(1024L)
            .addUserMessage("Please analyze the content at https://example.com/article")
            .addTool(WebFetchTool20250910.builder()
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
        ['role' => 'user', 'content' => 'Please analyze the content at https://example.com/article']
    ],
    model: 'claude-opus-4-7',
    tools: [[
        'type' => 'web_fetch_20250910',
        'name' => 'web_fetch',
        'max_uses' => 5,
    ]],
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
    { role: "user", content: "Please analyze the content at https://example.com/article" }
  ],
  tools: [{
    type: "web_fetch_20250910",
    name: "web_fetch",
    max_uses: 5
  }]
)
puts message
```
</CodeGroup>

### Definisi alat

Alat web fetch mendukung parameter berikut:

```json JSON
{
  "type": "web_fetch_20250910",
  "name": "web_fetch",

  // Opsional: Batasi jumlah pengambilan per permintaan
  "max_uses": 10,

  // Opsional: Hanya ambil dari domain ini
  "allowed_domains": ["example.com", "docs.example.com"],

  // Opsional: Jangan pernah ambil dari domain ini
  "blocked_domains": ["private.example.com"],

  // Opsional: Aktifkan kutipan untuk konten yang diambil
  "citations": {
    "enabled": true
  },

  // Opsional: Panjang konten maksimum dalam token
  "max_content_tokens": 100000
}
```

#### Penggunaan maksimal

Parameter `max_uses` membatasi jumlah pengambilan web yang dilakukan. Jika Claude mencoba lebih banyak pengambilan daripada yang diizinkan, `web_fetch_tool_result` adalah kesalahan dengan kode kesalahan `max_uses_exceeded`. Saat ini tidak ada batas default.

#### Penyaringan domain

Untuk penyaringan domain dengan `allowed_domains` dan `blocked_domains`, lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

#### Batas konten

Parameter `max_content_tokens` membatasi jumlah konten yang disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, alat akan memotongnya. Ini membantu mengontrol penggunaan token saat mengambil dokumen besar.

<Note>
Batas parameter `max_content_tokens` bersifat perkiraan. Jumlah token input aktual yang digunakan dapat bervariasi dalam jumlah kecil.
</Note>

#### Kutipan

Tidak seperti pencarian web di mana kutipan selalu diaktifkan, kutipan bersifat opsional untuk web fetch. Atur `"citations": {"enabled": true}` untuk memungkinkan Claude mengutip bagian tertentu dari dokumen yang diambil.

<Note>
Saat menampilkan output API langsung kepada pengguna akhir, kutipan harus disertakan ke sumber asli. Jika Anda membuat modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan kutipan sesuai kebutuhan berdasarkan konsultasi dengan tim hukum Anda.
</Note>

### Respons

Berikut adalah contoh struktur respons:

```json Output
{
  "role": "assistant",
  "content": [
    // 1. Keputusan Claude untuk mengambil
    {
      "type": "text",
      "text": "I'll fetch the content from the article to analyze it."
    },
    // 2. Permintaan pengambilan
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01234567890abcdef",
      "name": "web_fetch",
      "input": {
        "url": "https://example.com/article"
      }
    },
    // 3. Hasil pengambilan
    {
      "type": "web_fetch_tool_result",
      "tool_use_id": "srvtoolu_01234567890abcdef",
      "content": {
        "type": "web_fetch_result",
        "url": "https://example.com/article",
        "content": {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "Full text content of the article..."
          },
          "title": "Article Title",
          "citations": { "enabled": true }
        },
        "retrieved_at": "2025-08-25T10:30:00Z"
      }
    },
    // 4. Analisis Claude dengan kutipan (jika diaktifkan)
    {
      "text": "Based on the article, ",
      "type": "text"
    },
    {
      "text": "the main argument presented is that artificial intelligence will transform healthcare",
      "type": "text",
      "citations": [
        {
          "type": "char_location",
          "document_index": 0,
          "document_title": "Article Title",
          "start_char_index": 1234,
          "end_char_index": 1456,
          "cited_text": "Artificial intelligence is poised to revolutionize healthcare delivery..."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

#### Hasil pengambilan

Hasil pengambilan mencakup:

- `url`: URL yang diambil
- `content`: Blok dokumen yang berisi konten yang diambil
- `retrieved_at`: Stempel waktu saat konten diambil

<Note>
Alat web fetch menyimpan hasil dalam cache untuk meningkatkan kinerja dan mengurangi permintaan yang berlebihan. Konten yang dikembalikan mungkin tidak selalu mencerminkan versi terbaru yang tersedia di URL. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan berbagai jenis konten dan pola penggunaan.
</Note>

Untuk dokumen PDF, konten dikembalikan sebagai data yang dikodekan base64:

```json Output
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_02",
  "content": {
    "type": "web_fetch_result",
    "url": "https://example.com/paper.pdf",
    "content": {
      "type": "document",
      "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": "JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmo..."
      },
      "citations": { "enabled": true }
    },
    "retrieved_at": "2025-08-25T10:30:02Z"
  }
}
```

#### Kesalahan

Ketika alat web fetch mengalami kesalahan, Claude API mengembalikan respons 200 (sukses) dengan kesalahan yang diwakili dalam badan respons:

```json Output
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_a93jad",
  "content": {
    "type": "web_fetch_tool_error",
    "error_code": "url_not_accessible"
  }
}
```

Ini adalah kode kesalahan yang mungkin:

- `invalid_input`: Format URL tidak valid
- `url_too_long`: URL melebihi panjang maksimum (250 karakter)
- `url_not_allowed`: URL diblokir oleh aturan penyaringan domain dan pembatasan model
- `url_not_accessible`: Gagal mengambil konten (kesalahan HTTP)
- `too_many_requests`: Batas laju terlampaui
- `unsupported_content_type`: Jenis konten tidak didukung (hanya teks dan PDF)
- `max_uses_exceeded`: Penggunaan alat web fetch maksimum terlampaui
- `unavailable`: Kesalahan internal terjadi

## Validasi URL

Untuk alasan keamanan, alat web fetch hanya dapat mengambil URL yang telah muncul sebelumnya dalam konteks percakapan. Ini mencakup:

- URL dalam pesan pengguna
- URL dalam hasil alat sisi klien
- URL dari hasil pencarian web atau web fetch sebelumnya

Alat tidak dapat mengambil URL arbitrer yang dihasilkan Claude atau URL dari alat server berbasis kontainer (Code Execution, Bash, dll.).

## Pencarian dan pengambilan gabungan

Web fetch bekerja dengan mulus dengan pencarian web untuk pengumpulan informasi yang komprehensif:

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Find recent articles about quantum computing and analyze the most relevant one in detail",
        }
    ],
    tools=[
        {"type": "web_search_20250305", "name": "web_search", "max_uses": 3},
        {
            "type": "web_fetch_20250910",
            "name": "web_fetch",
            "max_uses": 5,
            "citations": {"enabled": True},
        },
    ],
)
```

Dalam alur kerja ini, Claude akan:
1. Menggunakan pencarian web untuk menemukan artikel yang relevan
2. Memilih hasil yang paling menjanjikan
3. Menggunakan web fetch untuk mengambil konten lengkap
4. Memberikan analisis terperinci dengan kutipan

## Penyimpanan cache prompt

Untuk menyimpan definisi alat dalam cache di seluruh putaran, lihat [Tool use with prompt caching](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming

Dengan streaming diaktifkan, acara pengambilan adalah bagian dari aliran dengan jeda selama pengambilan konten:

```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Claude's decision to fetch

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_fetch"}}

// Fetch URL streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"url\":\"https://example.com/article\"}"}}

// Pause while fetch executes

// Fetch results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_fetch_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "web_fetch_result", "url": "https://example.com/article", "content": {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "Article content..."}}}}}

// Claude's response continues...
```

## Permintaan batch

Anda dapat menyertakan alat web fetch dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat web fetch melalui Messages Batches API memiliki harga yang sama dengan permintaan Messages API biasa.

## Penggunaan dan harga

Web fetch usage has **no additional charges** beyond standard token costs:

```json
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```

The web fetch tool is available on the Claude API at **no additional cost**. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the `max_content_tokens` parameter to set appropriate limits based on your use case and budget considerations.

Example token usage for typical content:
- Average web page (10&nbsp;kB): ~2,500 tokens
- Large documentation page (100&nbsp;kB): ~25,000 tokens
- Research paper PDF (500&nbsp;kB): ~125,000 tokens

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/server-tools" title="Server tools">
    Mekanik bersama untuk alat yang dijalankan Anthropic.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Tool reference">
    Direktori semua alat yang disediakan Anthropic.
  </Card>
</CardGroup>