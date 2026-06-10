---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 85490d87d430e8bb562f669b1c1e655ab79a616c171cf1f3b4ab82713eacb951
---

# Alat web fetch

Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.

---

Alat web fetch memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.

Versi alat web fetch terbaru (`web_fetch_20260209`) mendukung **dynamic filtering** (pemfilteran dinamis) dengan Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6. Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum masuk ke jendela konteks, hanya menyimpan informasi yang relevan dan membuang sisanya. Hal ini mengurangi konsumsi token sambil mempertahankan kualitas respons. Versi alat sebelumnya (`web_fetch_20250910`) tetap tersedia tanpa pemfilteran dinamis.

<Note>
Untuk [Claude Mythos Preview](https://anthropic.com/glasswing), web fetch tersedia di Claude API dan Microsoft Foundry. Saat ini belum tersedia untuk Mythos Preview di Amazon Bedrock atau Vertex AI.
</Note>

<Note>
Gunakan [formulir umpan balik](https://forms.gle/NhWcgmkcvPCMmPE86) untuk memberikan masukan tentang kualitas respons model, API itu sendiri, atau kualitas dokumentasi.
</Note>

Untuk kelayakan Zero Data Retention dan solusi `allowed_callers`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#zdr-and-allowed-callers).

<Warning>
Mengaktifkan alat web fetch di lingkungan tempat Claude memproses input yang tidak tepercaya bersama dengan data sensitif menimbulkan risiko eksfiltrasi data. Hanya gunakan alat ini di lingkungan tepercaya atau saat menangani data yang tidak sensitif.

Untuk meminimalkan risiko eksfiltrasi, Claude tidak diizinkan untuk membuat URL secara dinamis. Claude hanya dapat mengambil URL yang telah disediakan secara eksplisit oleh pengguna atau yang berasal dari hasil web search atau web fetch sebelumnya. Namun, masih ada risiko residual yang harus dipertimbangkan dengan cermat saat menggunakan alat ini.

Jika eksfiltrasi data menjadi kekhawatiran, pertimbangkan untuk:
- Menonaktifkan alat web fetch sepenuhnya
- Menggunakan parameter `max_uses` untuk membatasi jumlah permintaan
- Menggunakan parameter `allowed_domains` untuk membatasi ke domain yang diketahui aman
</Warning>

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Cara kerja web fetch \{#how-web-fetch-works}

Saat Anda menambahkan alat web fetch ke permintaan API Anda:

1. Claude memutuskan kapan harus mengambil konten berdasarkan prompt dan URL yang tersedia.
2. API mengambil konten teks lengkap dari URL yang ditentukan.
3. Untuk PDF, ekstraksi teks otomatis dilakukan.
4. Claude menganalisis konten yang diambil dan memberikan respons dengan kutipan opsional.

<Note>
Alat web fetch saat ini tidak mendukung situs web yang dirender secara dinamis dengan JavaScript.
</Note>

### Kapan Claude melakukan fetch \{#when-claude-fetches}

Claude melakukan fetch ketika permintaan mengarah ke halaman atau dokumen tertentu:

- Sebuah URL disediakan dalam percakapan (atau hasil alat sebelumnya)
- Pengguna menyebutkan sumber daya tertentu (artikel tertentu, README, halaman harga, atau bagian dokumentasi) tanpa URL, dan [alat web search](/docs/id/agents-and-tools/tool-use/web-search-tool) juga diaktifkan sehingga Claude dapat menemukannya terlebih dahulu (lihat [Gabungan search dan fetch](#combined-search-and-fetch))

Claude **tidak** melakukan fetch untuk pertanyaan pengetahuan umum atau pertanyaan terbuka yang tidak merujuk ke halaman tertentu. "Ringkas artikel ini: `<url>`" memicu fetch; "apa praktik terbaik untuk desain REST API?" dijawab secara langsung.

### Pemfilteran dinamis \{#dynamic-filtering}

Mengambil halaman web dan PDF secara penuh dapat dengan cepat menghabiskan token, terutama ketika hanya informasi tertentu yang dibutuhkan dari dokumen besar. Dengan versi alat `web_fetch_20260209`, Claude dapat menulis dan mengeksekusi kode untuk memfilter konten yang diambil sebelum memuatnya ke dalam konteks.

Pemfilteran dinamis ini sangat berguna untuk:
- Mengekstrak bagian tertentu dari dokumen panjang
- Memproses data terstruktur dari halaman web
- Memfilter informasi relevan dari PDF
- Mengurangi biaya token saat bekerja dengan dokumen besar

<Note>
Pemfilteran dinamis memerlukan [alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan. Alat web fetch (dengan dan tanpa pemfilteran dinamis) tersedia di Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Saat ini belum tersedia di Amazon Bedrock atau Vertex AI.
</Note>

Untuk mengaktifkan pemfilteran dinamis, gunakan versi alat `web_fetch_20260209`:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
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
model: claude-opus-4-8
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
    model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 4096,
    Messages = [new() { Role = Role.User, Content = "Fetch the content at https://example.com/research-paper and extract the key findings." }],
    Tools = [new ToolUnion(new WebFetchTool20260209())]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
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

```java Java hidelines={1..5}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebFetchTool20260209;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(4096L)
        .addUserMessage("Fetch the content at https://example.com/research-paper and extract the key findings.")
        .addTool(WebFetchTool20260209.builder().build())
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Fetch the content at https://example.com/research-paper and extract the key findings.']
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

## Cara menggunakan web fetch \{#how-to-use-web-fetch}

Sediakan alat web fetch dalam permintaan API Anda:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
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
  --model claude-opus-4-8 \
  --max-tokens 1024 \
  --message '{role: user, content: "Please analyze the content at https://example.com/article"}' \
  --tool '{type: web_fetch_20250910, name: web_fetch, max_uses: 5}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Please analyze the content at https://example.com/article" }],
    Tools = [new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 })]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message);
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

```java Java hidelines={1..5}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.WebFetchTool20250910;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024L)
        .addUserMessage("Please analyze the content at https://example.com/article")
        .addTool(WebFetchTool20250910.builder()
            .maxUses(5L)
            .build())
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Please analyze the content at https://example.com/article']
    ],
    model: 'claude-opus-4-8',
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
  model: "claude-opus-4-8",
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

### Definisi alat \{#tool-definition}

Alat web fetch mendukung parameter berikut:

```json JSON
{
  "type": "web_fetch_20250910",
  "name": "web_fetch",

  // Optional: Limit the number of fetches per request
  "max_uses": 10,

  // Optional: Only fetch from these domains
  "allowed_domains": ["example.com", "docs.example.com"],

  // Optional: Never fetch from these domains
  "blocked_domains": ["private.example.com"],

  // Optional: Enable citations for fetched content
  "citations": {
    "enabled": true
  },

  // Optional: Maximum content length in tokens
  "max_content_tokens": 100000
}
```

#### Max uses \{#max-uses}

Parameter `max_uses` membatasi jumlah web fetch yang dilakukan. Jika Claude mencoba melakukan fetch lebih banyak dari yang diizinkan, `web_fetch_tool_result` akan berupa error dengan kode error `max_uses_exceeded`. Saat ini tidak ada batas default.

#### Pemfilteran domain \{#domain-filtering}

Untuk pemfilteran domain dengan `allowed_domains` dan `blocked_domains`, lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#domain-filtering).

#### Batas konten \{#content-limits}

Parameter `max_content_tokens` membatasi jumlah konten yang disertakan dalam konteks. Jika konten yang diambil melebihi batas ini, alat akan memotongnya. Ini membantu mengontrol penggunaan token saat mengambil dokumen besar.

<Note>
Batas parameter `max_content_tokens` bersifat perkiraan. Jumlah token input aktual yang digunakan dapat bervariasi dalam jumlah kecil.
</Note>

#### Kutipan \{#citations}

Tidak seperti web search di mana kutipan selalu diaktifkan, kutipan bersifat opsional untuk web fetch. Atur `"citations": {"enabled": true}` untuk memungkinkan Claude mengutip bagian tertentu dari dokumen yang diambil.

<Note>
Saat menampilkan output API secara langsung kepada pengguna akhir, kutipan harus disertakan ke sumber aslinya. Jika Anda melakukan modifikasi pada output API, termasuk dengan memproses ulang dan/atau menggabungkannya dengan materi Anda sendiri sebelum menampilkannya kepada pengguna akhir, tampilkan kutipan sebagaimana mestinya berdasarkan konsultasi dengan tim hukum Anda.
</Note>

### Respons \{#response}

Berikut adalah contoh struktur respons:

```json Output
{
  "role": "assistant",
  "content": [
    // 1. Claude's decision to fetch
    {
      "type": "text",
      "text": "I'll fetch the content from the article to analyze it."
    },
    // 2. The fetch request
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01234567890abcdef",
      "name": "web_fetch",
      "input": {
        "url": "https://example.com/article"
      }
    },
    // 3. Fetch results
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
    // 4. Claude's analysis with citations (if enabled)
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

#### Hasil fetch \{#fetch-results}

Hasil fetch mencakup:

- `url`: URL yang diambil
- `content`: Blok dokumen yang berisi konten yang diambil
- `retrieved_at`: Stempel waktu saat konten diambil

<Note>
Alat web fetch menyimpan hasil dalam cache untuk meningkatkan performa dan mengurangi permintaan yang berlebihan. Konten yang dikembalikan mungkin tidak selalu mencerminkan versi terbaru yang tersedia di URL tersebut. Perilaku cache dikelola secara otomatis dan dapat berubah seiring waktu untuk mengoptimalkan berbagai jenis konten dan pola penggunaan.
</Note>

Untuk dokumen PDF, konten dikembalikan sebagai data yang dikodekan dalam base64:

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

#### Error \{#errors}

Ketika alat web fetch mengalami error, Claude API mengembalikan respons 200 (sukses) dengan error yang direpresentasikan dalam body respons:

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

Berikut adalah kode error yang mungkin terjadi:

- `invalid_input`: Format URL tidak valid
- `url_too_long`: URL melebihi panjang maksimum (250 karakter)
- `url_not_allowed`: URL diblokir oleh aturan pemfilteran domain dan pembatasan model
- `url_not_accessible`: Gagal mengambil konten (error HTTP)
- `too_many_requests`: Batas laju terlampaui
- `unsupported_content_type`: Jenis konten tidak didukung (hanya teks dan PDF)
- `max_uses_exceeded`: Penggunaan maksimum alat web fetch terlampaui
- `unavailable`: Terjadi error internal

## Validasi URL \{#url-validation}

Untuk alasan keamanan, alat web fetch hanya dapat mengambil URL yang sebelumnya telah muncul dalam konteks percakapan. Ini mencakup:

- URL dalam pesan pengguna
- URL dalam hasil alat sisi klien
- URL dari hasil web search atau web fetch sebelumnya

Alat ini tidak dapat mengambil URL sembarang yang dihasilkan Claude atau URL dari alat server berbasis kontainer (Code Execution, Bash, dll.).

## Gabungan search dan fetch \{#combined-search-and-fetch}

Web fetch bekerja secara mulus dengan web search untuk pengumpulan informasi yang komprehensif:

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
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
print(response)
```

Dalam alur kerja ini, Claude akan:
1. Menggunakan web search untuk menemukan artikel yang relevan
2. Memilih hasil yang paling menjanjikan
3. Menggunakan web fetch untuk mengambil konten lengkap
4. Memberikan analisis terperinci dengan kutipan

Ketika alat web search dan web fetch keduanya diaktifkan, dan pengguna menyebutkan halaman atau dokumen tertentu tanpa memberikan URL (misalnya, "baca README dari repositori anthropics/anthropic-sdk-python"), Claude menggunakan web search untuk menemukannya, lalu melakukan fetch pada hasilnya.

## Caching prompt \{#prompt-caching}

Untuk melakukan cache definisi alat di seluruh giliran, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

## Streaming \{#streaming}

Dengan streaming diaktifkan, event fetch menjadi bagian dari stream dengan jeda selama pengambilan konten:

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

## Permintaan batch \{#batch-requests}

Anda dapat menyertakan alat web fetch dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing). Panggilan alat web fetch melalui Messages Batches API dikenakan harga yang sama dengan permintaan Messages API reguler.

## Penggunaan dan harga \{#usage-and-pricing}

Penggunaan web fetch **tidak dikenakan biaya tambahan** di luar biaya token standar:

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

Alat web fetch tersedia di Claude API **tanpa biaya tambahan**. Anda hanya membayar biaya token standar untuk konten yang diambil dan menjadi bagian dari konteks percakapan Anda.

Untuk melindungi dari pengambilan konten berukuran besar secara tidak sengaja yang akan menghabiskan token secara berlebihan, gunakan parameter `max_content_tokens` untuk menetapkan batas yang sesuai berdasarkan kasus penggunaan dan pertimbangan anggaran Anda.

Contoh penggunaan token untuk konten umum:
- Halaman web rata-rata (10&nbsp;kB): ~2.500 token
- Halaman dokumentasi besar (100&nbsp;kB): ~25.000 token
- PDF makalah penelitian (500&nbsp;kB): ~125.000 token

## Langkah selanjutnya \{#next-steps}

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/server-tools" title="Alat server">
    Mekanisme bersama untuk alat yang dieksekusi Anthropic.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori semua alat yang disediakan Anthropic.
  </Card>
</CardGroup>