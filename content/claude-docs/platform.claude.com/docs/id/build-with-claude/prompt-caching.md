---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-caching
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 0d47b02efc0f8dcf6125305172566c3bcbb416208f5a5425fb14bd25d7cf76f2
---

# Caching prompt

---

Caching prompt mengoptimalkan penggunaan API Anda dengan memungkinkan melanjutkan dari prefiks tertentu dalam prompt Anda. Hal ini secara signifikan mengurangi waktu pemrosesan dan biaya untuk tugas berulang atau prompt dengan elemen yang konsisten.

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Ada dua cara untuk mengaktifkan caching prompt:

- **[Caching otomatis](#automatic-caching)**: Tambahkan satu field `cache_control` di tingkat atas permintaan Anda. Sistem secara otomatis menerapkan breakpoint cache ke blok terakhir yang dapat di-cache dan memindahkannya ke depan seiring percakapan berkembang. Paling cocok untuk percakapan multi-giliran di mana riwayat pesan yang terus bertambah harus di-cache secara otomatis.
- **[Breakpoint cache eksplisit](#explicit-cache-breakpoints)**: Tempatkan `cache_control` langsung pada blok konten individual untuk kontrol yang lebih detail atas apa yang di-cache.

Cara paling sederhana untuk memulai adalah dengan caching otomatis:

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the major themes in Pride and Prejudice."
      }
    ]
  }'
```

```bash CLI
ant messages create --transform usage <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
cache_control:
  type: ephemeral
system: >-
  You are an AI assistant tasked with analyzing literary works. Your goal is
  to provide insightful commentary on themes, characters, and writing style.
messages:
  - role: user
    content: Analyze the major themes in Pride and Prejudice.
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},
    system="You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
    messages=[
        {
            "role": "user",
            "content": "Analyze the major themes in 'Pride and Prejudice'.",
        }
    ],
)
print(response.usage.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" },
  system:
    "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
  messages: [
    {
      role: "user",
      content: "Analyze the major themes in 'Pride and Prejudice'."
    }
  ]
});
console.log(response.usage);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    CacheControl = new CacheControlEphemeral(),
    System = "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "Analyze the major themes in 'Pride and Prejudice'."
        }
    ]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message.Usage);
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
		Model:        anthropic.ModelClaudeOpus4_8,
		MaxTokens:    1024,
		CacheControl: anthropic.NewCacheControlEphemeralParam(),
		System: []anthropic.TextBlockParam{
			{Text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style."},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the major themes in 'Pride and Prejudice'.")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Usage)
}
```

```java Java hidelines={1..2,4..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class PromptCachingExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .maxTokens(1024)
        .cacheControl(CacheControlEphemeral.builder().build())
        .system("You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.")
        .addUserMessage("Analyze the major themes in 'Pride and Prejudice'.")
        .build();

    Message message = client.messages().create(params);
    System.out.println(message.usage());
  }
}
```

```php PHP hidelines={1..3,5}
<?php

use Anthropic\Client;
use Anthropic\Messages\CacheControlEphemeral;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "Analyze the major themes in 'Pride and Prejudice'."]
    ],
    model: 'claude-opus-4-8',
    cacheControl: CacheControlEphemeral::with(),
    system: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
);
echo json_encode($response->usage);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: {type: "ephemeral"},
  system: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
  messages: [
    {
      role: "user",
      content: "Analyze the major themes in 'Pride and Prejudice'."
    }
  ]
)
puts response.usage
```
</CodeGroup>

Dengan caching otomatis, sistem meng-cache semua konten hingga dan termasuk blok terakhir yang dapat di-cache. Pada permintaan berikutnya dengan prefiks yang sama, konten yang di-cache digunakan kembali secara otomatis.

---

## Cara kerja caching prompt \{#how-prompt-caching-works}

Ketika Anda mengirim permintaan dengan caching prompt diaktifkan:

1. Sistem memeriksa apakah prefiks prompt, hingga breakpoint cache yang ditentukan, sudah di-cache dari kueri terbaru.
2. Jika ditemukan, sistem menggunakan versi yang di-cache, mengurangi waktu pemrosesan dan biaya.
3. Jika tidak, sistem memproses prompt lengkap dan meng-cache prefiks setelah respons dimulai.

Ini sangat berguna untuk:
- Prompt dengan banyak contoh
- Konteks atau informasi latar belakang dalam jumlah besar
- Tugas berulang dengan instruksi yang konsisten
- Percakapan multi-giliran yang panjang

Secara default, cache memiliki masa hidup 5 menit. Cache diperbarui tanpa biaya tambahan setiap kali konten yang di-cache digunakan.

<Note>
Jika Anda merasa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

Untuk informasi lebih lanjut, lihat [Durasi cache 1 jam](#1-hour-cache-duration).
</Note>

<Tip>
  **Caching prompt meng-cache seluruh prefiks**

Caching prompt mereferensikan seluruh prompt - `tools`, `system`, dan `messages` (dalam urutan tersebut) hingga dan termasuk blok yang ditandai dengan `cache_control`.

</Tip>

---

## Harga \{#pricing}

Caching prompt memperkenalkan struktur harga baru. Tabel di bawah ini menunjukkan harga per juta token untuk setiap model yang didukung:

| Model             | Token Input Dasar | Penulisan Cache 5m | Penulisan Cache 1j | Cache Hit & Refresh | Token Output |
|-------------------|-------------------|-----------------|-----------------|----------------------|---------------|
| Claude Fable 5      | $10 / MTok        | $12,50 / MTok   | $20 / MTok      | $1 / MTok | $50 / MTok    |
| Claude Mythos 5 ([ketersediaan terbatas](https://anthropic.com/glasswing)) | $10 / MTok        | $12,50 / MTok   | $20 / MTok      | $1 / MTok | $50 / MTok    |
| Claude Opus 4.8     | $5 / MTok         | $6,25 / MTok    | $10 / MTok      | $0,50 / MTok | $25 / MTok    |
| Claude Opus 4.7     | $5 / MTok         | $6,25 / MTok    | $10 / MTok      | $0,50 / MTok | $25 / MTok    |
| Claude Opus 4.6     | $5 / MTok         | $6,25 / MTok    | $10 / MTok      | $0,50 / MTok | $25 / MTok    |
| Claude Opus 4.5   | $5 / MTok         | $6,25 / MTok    | $10 / MTok      | $0,50 / MTok | $25 / MTok    |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) | $15 / MTok        | $18,75 / MTok   | $30 / MTok      | $1,50 / MTok | $75 / MTok    |
| Claude Opus 4 ([dihentikan, kecuali di Vertex AI](/docs/id/about-claude/model-deprecations)) | $15 / MTok        | $18,75 / MTok   | $30 / MTok      | $1,50 / MTok | $75 / MTok    |
| Claude Sonnet 4.6   | $3 / MTok         | $3,75 / MTok    | $6 / MTok       | $0,30 / MTok | $15 / MTok    |
| Claude Sonnet 4.5   | $3 / MTok         | $3,75 / MTok    | $6 / MTok       | $0,30 / MTok | $15 / MTok    |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) | $3 / MTok         | $3,75 / MTok    | $6 / MTok       | $0,30 / MTok | $15 / MTok    |
| Claude Haiku 4.5  | $1 / MTok         | $1,25 / MTok    | $2 / MTok       | $0,10 / MTok | $5 / MTok     |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) | $0,80 / MTok      | $1 / MTok       | $1,60 / MTok     | $0,08 / MTok | $4 / MTok     |

<Note>
Tabel di atas mencerminkan pengali harga berikut untuk caching prompt:
- Token penulisan cache 5 menit adalah 1,25 kali harga token input dasar
- Token penulisan cache 1 jam adalah 2 kali harga token input dasar
- Token pembacaan cache adalah 0,1 kali harga token input dasar

Pengali ini dapat digabungkan dengan pengubah harga lainnya seperti diskon Batch API dan residensi data. Lihat [harga](/docs/id/about-claude/pricing) untuk detail lengkap.
</Note>

---

## Model yang didukung \{#supported-models}

Caching prompt (baik otomatis maupun eksplisit) didukung pada semua [model Claude yang aktif](/docs/id/about-claude/models/overview).

---

## Caching otomatis \{#automatic-caching}

Caching otomatis adalah cara paling sederhana untuk mengaktifkan caching prompt. Alih-alih menempatkan `cache_control` pada blok konten individual, tambahkan satu field `cache_control` di tingkat atas body permintaan Anda. Sistem secara otomatis menerapkan breakpoint cache ke blok terakhir yang dapat di-cache.

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are a helpful assistant that remembers our conversation.",
    "messages": [
      {"role": "user", "content": "My name is Alex. I work on machine learning."},
      {"role": "assistant", "content": "Nice to meet you, Alex! How can I help with your ML work today?"},
      {"role": "user", "content": "What did I say I work on?"}
    ]
  }'
```

```bash CLI
ant messages create --transform usage <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
cache_control:
  type: ephemeral
system: You are a helpful assistant that remembers our conversation.
messages:
  - role: user
    content: My name is Alex. I work on machine learning.
  - role: assistant
    content: Nice to meet you, Alex! How can I help with your ML work today?
  - role: user
    content: What did I say I work on?
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},
    system="You are a helpful assistant that remembers our conversation.",
    messages=[
        {"role": "user", "content": "My name is Alex. I work on machine learning."},
        {
            "role": "assistant",
            "content": "Nice to meet you, Alex! How can I help with your ML work today?",
        },
        {"role": "user", "content": "What did I say I work on?"},
    ],
)
print(response.usage.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" },
  system: "You are a helpful assistant that remembers our conversation.",
  messages: [
    { role: "user", content: "My name is Alex. I work on machine learning." },
    {
      role: "assistant",
      content: "Nice to meet you, Alex! How can I help with your ML work today?"
    },
    { role: "user", content: "What did I say I work on?" }
  ]
});
console.log(response.usage);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    CacheControl = new CacheControlEphemeral(),
    System = "You are a helpful assistant that remembers our conversation.",
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "My name is Alex. I work on machine learning."
        },
        new()
        {
            Role = Role.Assistant,
            Content = "Nice to meet you, Alex! How can I help with your ML work today?"
        },
        new()
        {
            Role = Role.User,
            Content = "What did I say I work on?"
        }
    ]
};

var message = await client.Messages.Create(parameters);
Console.WriteLine(message.Usage);
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
		Model:        anthropic.ModelClaudeOpus4_8,
		MaxTokens:    1024,
		CacheControl: anthropic.NewCacheControlEphemeralParam(),
		System: []anthropic.TextBlockParam{
			{Text: "You are a helpful assistant that remembers our conversation."},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("My name is Alex. I work on machine learning.")),
			anthropic.NewAssistantMessage(anthropic.NewTextBlock("Nice to meet you, Alex! How can I help with your ML work today?")),
			anthropic.NewUserMessage(anthropic.NewTextBlock("What did I say I work on?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Usage)
}
```

```java Java hidelines={1..2,4..10,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class AutomaticCachingExample {

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024)
                .cacheControl(CacheControlEphemeral.builder().build())
                .system("You are a helpful assistant that remembers our conversation.")
                .addUserMessage("My name is Alex. I work on machine learning.")
                .addAssistantMessage("Nice to meet you, Alex! How can I help with your ML work today?")
                .addUserMessage("What did I say I work on?")
                .build();

        Message message = client.messages().create(params);
        System.out.println(message.usage());
    }
}
```

```php PHP hidelines={1..3,5}
<?php

use Anthropic\Client;
use Anthropic\Messages\CacheControlEphemeral;

$client = new Client();

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'My name is Alex. I work on machine learning.'],
        ['role' => 'assistant', 'content' => 'Nice to meet you, Alex! How can I help with your ML work today?'],
        ['role' => 'user', 'content' => 'What did I say I work on?'],
    ],
    model: 'claude-opus-4-8',
    cacheControl: CacheControlEphemeral::with(),
    system: 'You are a helpful assistant that remembers our conversation.',
);
echo json_encode($response->usage);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: {type: "ephemeral"},
  system: "You are a helpful assistant that remembers our conversation.",
  messages: [
    {role: "user", content: "My name is Alex. I work on machine learning."},
    {role: "assistant", content: "Nice to meet you, Alex! How can I help with your ML work today?"},
    {role: "user", content: "What did I say I work on?"}
  ]
)
puts response.usage
```
</CodeGroup>

### Cara kerja caching otomatis dalam percakapan multi-giliran \{#how-automatic-caching-works-in-multi-turn-conversations}

Dengan caching otomatis, titik cache bergerak maju secara otomatis seiring percakapan berkembang. Setiap permintaan baru meng-cache semuanya hingga blok terakhir yang dapat di-cache, dan konten sebelumnya dibaca dari cache.

| Permintaan | Konten | Perilaku cache |
|---------|---------|----------------|
| Permintaan 1 | System <br/> + User(1) + Asst(1) <br/> + **User(2)** ◀ cache | Semuanya ditulis ke cache |
| Permintaan 2 | System <br/> + User(1) + Asst(1) <br/> + User(2) + Asst(2) <br/> + **User(3)** ◀ cache | System hingga User(2) dibaca dari cache; <br/> Asst(2) + User(3) ditulis ke cache |
| Permintaan 3 | System <br/> + User(1) + Asst(1) <br/> + User(2) + Asst(2) <br/> + User(3) + Asst(3) <br/> + **User(4)** ◀ cache | System hingga User(3) dibaca dari cache; <br/> Asst(3) + User(4) ditulis ke cache |

Breakpoint cache secara otomatis berpindah ke blok terakhir yang dapat di-cache dalam setiap permintaan, sehingga Anda tidak perlu memperbarui penanda `cache_control` apa pun seiring percakapan berkembang.

### Dukungan TTL \{#ttl-support}

Secara default, caching otomatis menggunakan TTL 5 menit. Anda dapat menentukan TTL 1 jam dengan harga 2x harga token input dasar:

```json
{ "cache_control": { "type": "ephemeral", "ttl": "1h" } }
```

### Menggabungkan dengan caching tingkat blok \{#combining-with-block-level-caching}

Caching otomatis kompatibel dengan [breakpoint cache eksplisit](#explicit-cache-breakpoints). Ketika digunakan bersama, breakpoint cache otomatis menggunakan salah satu dari 4 slot breakpoint yang tersedia.

Ini memungkinkan Anda menggabungkan kedua pendekatan. Misalnya, gunakan breakpoint eksplisit untuk meng-cache prompt sistem Anda, sementara caching otomatis menangani percakapan:

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 1024,
  "cache_control": { "type": "ephemeral" },
  "system": [
    {
      "type": "text",
      "text": "You are a helpful assistant.",
      "cache_control": { "type": "ephemeral" }
    }
  ],
  "messages": [{ "role": "user", "content": "What are the key terms?" }]
}
```

### Apa yang tetap sama \{#what-stays-the-same}

Caching otomatis menggunakan infrastruktur caching dasar yang sama. Harga, ambang batas token minimum, persyaratan urutan konteks, dan jendela lookback 20 blok semuanya berlaku sama seperti dengan breakpoint eksplisit.

### Kasus khusus \{#edge-cases}

- Jika blok terakhir sudah memiliki `cache_control` eksplisit dengan TTL yang sama, caching otomatis tidak melakukan apa-apa.
- Jika blok terakhir memiliki `cache_control` eksplisit dengan TTL yang berbeda, API mengembalikan error 400.
- Jika 4 breakpoint tingkat blok eksplisit sudah ada, API mengembalikan error 400 (tidak ada slot tersisa untuk caching otomatis).
- Jika blok terakhir tidak memenuhi syarat sebagai target breakpoint cache otomatis, sistem secara diam-diam berjalan mundur untuk menemukan blok terdekat yang memenuhi syarat. Jika tidak ada yang ditemukan, caching dilewati.

<Note>
Caching otomatis tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) (beta). Bedrock dan Vertex AI tidak mendukung caching otomatis.
</Note>

---

## Breakpoint cache eksplisit \{#explicit-cache-breakpoints}

Untuk kontrol lebih atas caching, Anda dapat menempatkan `cache_control` langsung pada blok konten individual. Ini berguna ketika Anda perlu meng-cache bagian berbeda yang berubah pada frekuensi berbeda, atau memerlukan kontrol detail atas apa yang di-cache.

### Menyusun prompt Anda \{#structuring-your-prompt}

Tempatkan konten statis (definisi alat, instruksi sistem, konteks, contoh) di awal prompt Anda. Tandai akhir konten yang dapat digunakan kembali untuk caching menggunakan parameter `cache_control`.

Prefiks cache dibuat dalam urutan berikut: `tools`, `system`, lalu `messages`. Urutan ini membentuk hierarki di mana setiap tingkat dibangun di atas tingkat sebelumnya.

#### Cara kerja pemeriksaan prefiks otomatis \{#how-automatic-prefix-checking-works}

Anda dapat menggunakan hanya satu breakpoint cache di akhir konten statis Anda, dan sistem akan secara otomatis menemukan prefiks terpanjang yang sudah ditulis ke cache oleh permintaan sebelumnya. Memahami cara kerjanya membantu Anda mengoptimalkan strategi caching Anda.

**Tiga prinsip inti:**

1. **Penulisan cache hanya terjadi di breakpoint Anda.** Menandai blok dengan `cache_control` menulis tepat satu entri cache: hash dari prefiks yang berakhir di blok tersebut. Sistem tidak menulis entri untuk posisi mana pun yang lebih awal. Karena hash bersifat kumulatif, mencakup semuanya hingga dan termasuk breakpoint, mengubah blok mana pun di atau sebelum breakpoint menghasilkan hash yang berbeda pada permintaan berikutnya.

2. **Pembacaan cache melihat ke belakang untuk entri yang ditulis oleh permintaan sebelumnya.** Pada setiap permintaan, sistem menghitung hash prefiks di breakpoint Anda dan memeriksa entri cache yang cocok. Jika tidak ada, sistem berjalan mundur satu blok pada satu waktu, memeriksa apakah hash prefiks di setiap posisi sebelumnya cocok dengan sesuatu yang sudah ada di cache. Sistem mencari penulisan sebelumnya, bukan konten yang stabil.

3. **Jendela lookback adalah 20 blok.** Sistem memeriksa paling banyak 20 posisi per breakpoint, menghitung breakpoint itu sendiri sebagai yang pertama. Jika sistem tidak menemukan entri yang cocok dalam jendela tersebut, pemeriksaan berhenti (atau dilanjutkan dari breakpoint eksplisit berikutnya, jika ada).

**Contoh: Lookback dalam percakapan yang berkembang**

Anda menambahkan blok baru setiap giliran dan mengatur `cache_control` pada blok terakhir dari setiap permintaan:

- **Giliran 1:** 10 blok, breakpoint pada blok 10. Tidak ada entri cache sebelumnya. Sistem menulis entri di blok 10.
- **Giliran 2:** 15 blok, breakpoint pada blok 15. Blok 15 tidak memiliki entri, jadi sistem berjalan mundur ke blok 10 dan menemukan entri giliran-1. Cache hit di blok 10; sistem hanya memproses blok 11 hingga 15 secara baru dan menulis entri baru di blok 15.
- **Giliran 3:** 35 blok, breakpoint pada blok 35. Sistem memeriksa 20 posisi (blok 35 hingga 16) dan tidak menemukan apa pun. Entri giliran-2 di blok 15 berada satu posisi di luar jendela, jadi tidak ada cache hit. Menambahkan breakpoint kedua di blok 15 memulai jendela lookback kedua di sana, yang menemukan entri giliran-2.

**Kesalahan umum: Breakpoint pada konten yang berubah setiap permintaan**

Prompt Anda memiliki konteks sistem statis yang besar (blok 1 hingga 5) diikuti oleh blok per-permintaan yang berisi timestamp dan pesan pengguna (blok 6). Anda mengatur `cache_control` pada blok 6:

- **Permintaan 1:** Penulisan cache di blok 6. Hash mencakup timestamp.
- **Permintaan 2:** Timestamp berbeda, jadi hash prefiks di blok 6 berbeda. Lookback berjalan melalui blok 5, 4, 3, 2, dan 1, tetapi sistem tidak pernah menulis entri di posisi mana pun tersebut. Tidak ada cache hit. Anda membayar untuk penulisan cache baru pada setiap permintaan dan tidak pernah mendapatkan pembacaan.

Lookback tidak menemukan konten stabil di belakang breakpoint Anda dan meng-cache-nya. Lookback menemukan entri yang sudah ditulis oleh permintaan sebelumnya, dan penulisan hanya terjadi di breakpoint. Pindahkan `cache_control` ke blok 5, blok terakhir yang tetap sama di seluruh permintaan, dan setiap permintaan berikutnya membaca prefiks yang di-cache. [Caching otomatis](#automatic-caching) mengalami jebakan yang sama: caching otomatis menempatkan breakpoint pada blok terakhir yang dapat di-cache, yang dalam struktur ini adalah blok yang berubah setiap permintaan, jadi gunakan breakpoint eksplisit pada blok 5 sebagai gantinya.

**Poin penting:** Tempatkan `cache_control` pada blok terakhir yang prefiksnya identik di seluruh permintaan yang ingin Anda bagikan cache-nya. Dalam percakapan yang berkembang, blok terakhir berfungsi selama setiap giliran menambahkan kurang dari 20 blok: konten sebelumnya tidak pernah berubah, jadi lookback permintaan berikutnya menemukan penulisan sebelumnya. Untuk prompt dengan sufiks yang bervariasi (timestamp, konteks per-permintaan, pesan masuk), tempatkan breakpoint di akhir prefiks statis, bukan pada blok yang bervariasi.

#### Kapan menggunakan beberapa breakpoint \{#when-to-use-multiple-breakpoints}

Anda dapat mendefinisikan hingga 4 breakpoint cache jika Anda ingin:
- Meng-cache bagian berbeda yang berubah pada frekuensi berbeda (misalnya, alat jarang berubah, tetapi konteks diperbarui setiap hari)
- Memiliki kontrol lebih atas apa yang di-cache
- Memastikan cache hit ketika percakapan yang berkembang mendorong breakpoint Anda 20 blok atau lebih melewati penulisan cache terakhir

<Note>
**Batasan penting:** Lookback hanya dapat menemukan entri yang sudah ditulis oleh permintaan sebelumnya. Jika percakapan yang berkembang mendorong breakpoint Anda 20 blok atau lebih melewati penulisan terakhir, jendela lookback melewatkannya. Tambahkan breakpoint kedua lebih dekat ke posisi tersebut sejak awal sehingga penulisan terakumulasi di sana sebelum Anda membutuhkannya.
</Note>

### Memahami biaya breakpoint cache \{#understanding-cache-breakpoint-costs}

**Breakpoint cache itu sendiri tidak menambah biaya apa pun.** Anda hanya dikenakan biaya untuk:
- **Penulisan cache**: Ketika konten baru ditulis ke cache (25% lebih mahal dari token input dasar untuk TTL 5 menit)
- **Pembacaan cache**: Ketika konten yang di-cache digunakan (10% dari harga token input dasar)
- **Token input reguler**: Untuk konten apa pun yang tidak di-cache

Menambahkan lebih banyak breakpoint `cache_control` tidak meningkatkan biaya Anda - Anda tetap membayar jumlah yang sama berdasarkan konten apa yang sebenarnya di-cache dan dibaca. Breakpoint hanya memberi Anda kontrol atas bagian mana yang dapat di-cache secara independen.

---

## Strategi dan pertimbangan caching \{#caching-strategies-and-considerations}

### Batasan cache \{#cache-limitations}

Di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) (beta), panjang prompt minimum yang dapat di-cache adalah:

- 512 token untuk Claude Fable 5 dan [Claude Mythos 5](https://anthropic.com/glasswing)
- 2.048 token untuk [Claude Mythos Preview](https://anthropic.com/glasswing) dan Claude Opus 4.7
- 4.096 token untuk Claude Opus 4.6 dan Claude Opus 4.5
- 1.024 token untuk Claude Opus 4.8, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)), Claude Opus 4 ([dihentikan, kecuali di Vertex AI](/docs/id/about-claude/model-deprecations)), dan Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations))
- 4.096 token untuk Claude Haiku 4.5
- 2.048 token untuk Claude Haiku 3.5 ([dihentikan, kecuali di Vertex AI](/docs/id/about-claude/model-deprecations))

Ketersediaan model bervariasi menurut platform, begitu pula minimum untuk model yang baru dirilis: di [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), panjang prompt minimum yang dapat di-cache untuk Claude Fable 5 dan Claude Mythos 5 adalah 1.024 token.

Prompt yang lebih pendek tidak dapat di-cache, bahkan jika ditandai dengan `cache_control`. Permintaan apa pun untuk meng-cache kurang dari jumlah token ini akan diproses tanpa caching, dan tidak ada error yang dikembalikan. Untuk memverifikasi apakah prompt di-cache, periksa [field](/docs/id/build-with-claude/prompt-caching#tracking-cache-performance) usage respons: jika `cache_creation_input_tokens` dan `cache_read_input_tokens` keduanya 0, prompt tidak di-cache (kemungkinan karena tidak memenuhi persyaratan panjang minimum).

Jika prompt Anda sedikit di bawah minimum untuk model dan platform Anda, memperluas konten yang di-cache untuk mencapai ambang batas sering kali bermanfaat. Pembacaan cache jauh lebih murah daripada token input yang tidak di-cache, jadi mencapai minimum dapat mengurangi biaya untuk prompt yang sering digunakan kembali.

<Note>
[Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) adalah platform yang dioperasikan AWS. Di Bedrock, lihat [dokumentasi caching prompt Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) untuk minimum per-model, perilaku kegagalan, dan nama field usage yang berlaku.
</Note>

Untuk permintaan bersamaan, perhatikan bahwa entri cache hanya tersedia setelah respons pertama dimulai. Jika Anda memerlukan cache hit untuk permintaan paralel, tunggu respons pertama sebelum mengirim permintaan berikutnya.

Saat ini, "ephemeral" adalah satu-satunya tipe cache yang didukung, yang secara default memiliki masa hidup 5 menit.

### Apa yang dapat di-cache \{#what-can-be-cached}
Sebagian besar blok dalam permintaan dapat di-cache. Ini termasuk:

- Alat: Definisi alat dalam array `tools`
- Pesan sistem: Blok konten dalam array `system`
- Pesan teks: Blok konten dalam array `messages.content`, untuk giliran user dan assistant
- Gambar & Dokumen: Blok konten dalam array `messages.content`, dalam giliran user
- Penggunaan alat dan hasil alat: Blok konten dalam array `messages.content`, dalam giliran user dan assistant

Setiap elemen ini dapat di-cache, baik secara otomatis atau dengan menandainya dengan `cache_control`.

### Apa yang tidak dapat di-cache \{#what-cannot-be-cached}
Meskipun sebagian besar blok permintaan dapat di-cache, ada beberapa pengecualian:

- Blok thinking tidak dapat di-cache secara langsung dengan `cache_control`. Namun, blok thinking DAPAT di-cache bersama konten lain ketika muncul dalam giliran assistant sebelumnya. Ketika di-cache dengan cara ini, blok tersebut DIHITUNG sebagai token input ketika dibaca dari cache.
- Blok sub-konten (seperti [sitasi](/docs/id/build-with-claude/citations)) itu sendiri tidak dapat di-cache secara langsung. Sebagai gantinya, cache blok tingkat atas.

    Dalam kasus sitasi, blok konten dokumen tingkat atas yang berfungsi sebagai materi sumber untuk sitasi dapat di-cache. Ini memungkinkan Anda menggunakan caching prompt dengan sitasi secara efektif dengan meng-cache dokumen yang akan direferensikan oleh sitasi.
- Blok teks kosong tidak dapat di-cache.

### Apa yang membatalkan cache \{#what-invalidates-the-cache}

Modifikasi pada konten yang di-cache dapat membatalkan sebagian atau seluruh cache.

Seperti dijelaskan dalam [Menyusun prompt Anda](#structuring-your-prompt), cache mengikuti hierarki: `tools` → `system` → `messages`. Perubahan di setiap tingkat membatalkan tingkat tersebut dan semua tingkat berikutnya.

Tabel berikut menunjukkan bagian cache mana yang dibatalkan oleh berbagai jenis perubahan. ✘ menunjukkan bahwa cache dibatalkan, sedangkan ✓ menunjukkan bahwa cache tetap valid.

| Apa yang berubah | Cache tools | Cache system | Cache messages | Dampak |
|------------|------------------|---------------|----------------|-------------|
| **Definisi alat** | ✘ | ✘ | ✘ | Memodifikasi definisi alat (nama, deskripsi, parameter) membatalkan seluruh cache |
| **Toggle pencarian web** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan pencarian web memodifikasi prompt sistem |
| **Toggle sitasi** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan sitasi memodifikasi prompt sistem |
| **Pengaturan kecepatan** | ✓ | ✘ | ✘ | Beralih antara [`speed: "fast"` dan kecepatan standar](/docs/id/build-with-claude/fast-mode) membatalkan cache system dan message |
| **Tool choice** | ✓ | ✓ | ✘ | Perubahan pada parameter `tool_choice` hanya memengaruhi blok message |
| **Gambar** | ✓ | ✓ | ✘ | Menambah/menghapus gambar di mana pun dalam prompt memengaruhi blok message |
| **Parameter thinking** | ✓ | ✓ | ✘ | Perubahan pada pengaturan pemikiran diperpanjang (aktifkan/nonaktifkan, budget) memengaruhi blok message |
| **Hasil non-alat yang diteruskan ke permintaan pemikiran diperpanjang** | ✓ | ✓ | Spesifik model | Pada Opus 4.5+ dan Sonnet 4.6+, blok thinking dipertahankan secara default, sehingga cache tetap valid (✓). Pada model Opus/Sonnet sebelumnya dan semua model Haiku, semua blok thinking yang sebelumnya di-cache dihapus dari konteks, dan pesan apa pun yang mengikuti blok thinking tersebut dihapus dari cache (✘). Untuk detail lebih lanjut, lihat [Caching dengan blok thinking](#caching-with-thinking-blocks). |

<Note>
Pada Claude Opus 4.8, Anda dapat menambahkan instruksi sistem baru di tengah percakapan tanpa membatalkan cache system atau message. Tambahkan pesan `{"role": "system"}` ke `messages` alih-alih mengedit field `system` tingkat atas, sehingga prefiks yang di-cache tetap tidak berubah. Lihat [Pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages).
</Note>

### Melacak performa cache \{#tracking-cache-performance}

Pantau performa cache menggunakan field respons API ini, dalam `usage` di respons (atau event `message_start` jika menggunakan [streaming](/docs/id/build-with-claude/streaming)):

- `cache_creation_input_tokens`: Jumlah token yang ditulis ke cache saat membuat entri baru.
- `cache_read_input_tokens`: Jumlah token yang diambil dari cache untuk permintaan ini.
- `input_tokens`: Jumlah token input yang tidak dibaca dari atau digunakan untuk membuat cache (yaitu, token setelah breakpoint cache terakhir).

<Note>
**Memahami rincian token**

Field `input_tokens` hanya mewakili token yang datang **setelah breakpoint cache terakhir** dalam permintaan Anda - bukan semua token input yang Anda kirim.

Untuk menghitung total token input:
```text
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

**Penjelasan spasial:**
- `cache_read_input_tokens` = token sebelum breakpoint yang sudah di-cache (pembacaan)
- `cache_creation_input_tokens` = token sebelum breakpoint yang sedang di-cache sekarang (penulisan)
- `input_tokens` = token setelah breakpoint terakhir Anda (tidak memenuhi syarat untuk cache)

**Contoh:** Jika Anda memiliki permintaan dengan 100.000 token konten yang di-cache (dibaca dari cache), 0 token konten baru yang sedang di-cache, dan 50 token dalam pesan pengguna Anda (setelah breakpoint cache):
- `cache_read_input_tokens`: 100.000
- `cache_creation_input_tokens`: 0
- `input_tokens`: 50
- **Total token input yang diproses**: 100.050 token

Ini penting untuk memahami biaya dan batas laju, karena `input_tokens` biasanya akan jauh lebih kecil dari total input Anda ketika menggunakan caching secara efektif.
</Note>

### Caching dengan blok thinking \{#caching-with-thinking-blocks}

Ketika menggunakan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dengan caching prompt, blok thinking memiliki perilaku khusus:

**Caching otomatis bersama konten lain**: Meskipun blok thinking tidak dapat secara eksplisit ditandai dengan `cache_control`, blok tersebut di-cache sebagai bagian dari konten permintaan ketika Anda membuat panggilan API berikutnya dengan hasil alat. Ini umumnya terjadi selama penggunaan alat ketika Anda meneruskan blok thinking kembali untuk melanjutkan percakapan.

**Penghitungan token input**: Ketika blok thinking dibaca dari cache, blok tersebut dihitung sebagai token input dalam metrik penggunaan Anda. Ini penting untuk perhitungan biaya dan penganggaran token.

**Pola pembatalan cache**:
- Cache tetap valid ketika hanya hasil alat yang disediakan sebagai pesan pengguna
- Pada Opus 4.5+ dan Sonnet 4.6+, blok thinking dipertahankan secara default bahkan ketika konten pengguna non-hasil-alat ditambahkan, sehingga cache tetap valid
- Pada model Opus/Sonnet sebelumnya dan semua model Haiku, cache dibatalkan ketika konten pengguna non-hasil-alat ditambahkan, menyebabkan semua blok thinking sebelumnya dihapus dari konteks
- Perilaku caching ini terjadi bahkan tanpa penanda `cache_control` eksplisit

Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).

**Contoh dengan penggunaan alat**:
```text
Request 1: User: "What's the weather in Paris?"
Response: [thinking_block_1] + [tool_use block 1]

Request 2:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
Response: [thinking_block_2] + [text block 2]
# Request 2 caches its request content (not the response)
# The cache includes: user message, thinking_block_1, tool_use block 1, and tool_result_1

Request 3:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
# On earlier Opus/Sonnet and all Haiku models, non-tool-result user block causes prior thinking blocks to be stripped; on Opus 4.5+/Sonnet 4.6+ they are kept
```

Pada model Opus/Sonnet sebelumnya dan semua model Haiku, semua blok thinking sebelumnya dihapus dari konteks pada titik ini. Pada Opus 4.5+ dan Sonnet 4.6+, blok thinking sebelumnya dipertahankan secara default dan tetap menjadi bagian dari prefiks yang di-cache.

Untuk informasi lebih detail, lihat [dokumentasi pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior).

### Penyimpanan dan berbagi cache \{#cache-storage-and-sharing}

<Warning>
Per 5 Februari 2026, caching prompt menggunakan isolasi tingkat [workspace](/docs/id/manage-claude/workspaces) alih-alih isolasi tingkat organisasi. Cache diisolasi per workspace, memastikan pemisahan data antar workspace dalam organisasi yang sama. Ini berlaku untuk Claude API, Claude Platform on AWS, dan Microsoft Foundry (beta); Bedrock dan Vertex AI mempertahankan isolasi cache tingkat organisasi. Jika Anda menggunakan beberapa workspace, tinjau strategi caching Anda untuk memperhitungkan perbedaan ini.
</Warning>

- **Isolasi organisasi dan workspace:** Cache diisolasi antar organisasi. Organisasi yang berbeda tidak pernah berbagi cache, bahkan jika mereka menggunakan prompt yang identik. Per 5 Februari 2026, cache juga diisolasi per workspace dalam organisasi di Claude API, Claude Platform on AWS, dan Microsoft Foundry (beta); Bedrock dan Vertex AI terus menggunakan isolasi tingkat organisasi saja.

- **Pencocokan persis:** Cache hit memerlukan segmen prompt yang 100% identik, termasuk semua teks dan gambar hingga dan termasuk blok yang ditandai dengan cache control.

- **Pembuatan token output:** Caching prompt tidak berpengaruh pada pembuatan token output. Respons yang Anda terima identik dengan apa yang akan Anda dapatkan jika caching prompt tidak digunakan.

### Praktik terbaik untuk caching yang efektif \{#best-practices-for-effective-caching}

Untuk mengoptimalkan performa caching prompt:

- Mulai dengan [caching otomatis](#automatic-caching) untuk percakapan multi-giliran. Caching otomatis menangani manajemen breakpoint secara otomatis.
- Gunakan [breakpoint tingkat blok eksplisit](#explicit-cache-breakpoints) ketika Anda perlu meng-cache bagian berbeda dengan frekuensi perubahan berbeda.
- Cache konten yang stabil dan dapat digunakan kembali seperti instruksi sistem, informasi latar belakang, konteks besar, atau definisi alat yang sering digunakan.
- Tempatkan konten yang di-cache di awal prompt untuk performa terbaik.
- Gunakan breakpoint cache secara strategis untuk memisahkan bagian prefiks yang dapat di-cache yang berbeda.
- Tempatkan breakpoint pada blok terakhir yang tetap identik di seluruh permintaan. Untuk prompt dengan prefiks statis dan sufiks yang bervariasi (timestamp, konteks per-permintaan, pesan masuk), itu adalah akhir dari prefiks, bukan blok yang bervariasi.
- Analisis tingkat cache hit secara teratur dan sesuaikan strategi Anda sesuai kebutuhan.

### Mengoptimalkan untuk kasus penggunaan yang berbeda \{#optimizing-for-different-use-cases}

Sesuaikan strategi caching prompt Anda dengan skenario Anda:

- Agen percakapan: Kurangi biaya dan latensi untuk percakapan yang diperpanjang, terutama yang memiliki instruksi panjang atau dokumen yang diunggah.
- Asisten coding: Tingkatkan autocomplete dan tanya jawab codebase dengan menyimpan bagian yang relevan atau versi ringkasan dari codebase dalam prompt.
- Pemrosesan dokumen besar: Sertakan materi panjang lengkap termasuk gambar dalam prompt Anda tanpa meningkatkan latensi respons.
- Set instruksi terperinci: Bagikan daftar instruksi, prosedur, dan contoh yang ekstensif untuk menyempurnakan respons Claude. Developer sering menyertakan satu atau dua contoh dalam prompt, tetapi dengan caching prompt Anda bisa mendapatkan performa yang lebih baik dengan menyertakan 20+ contoh beragam dari jawaban berkualitas tinggi.
- Penggunaan alat agentic: Tingkatkan performa untuk skenario yang melibatkan beberapa panggilan alat dan perubahan kode iteratif, di mana setiap langkah biasanya memerlukan panggilan API baru.
- Berbicara dengan buku, makalah, dokumentasi, transkrip podcast, dan konten panjang lainnya: Hidupkan basis pengetahuan apa pun dengan menyematkan seluruh dokumen ke dalam prompt, dan membiarkan pengguna mengajukan pertanyaan kepadanya.

### Memecahkan masalah umum \{#troubleshooting-common-issues}

Jika mengalami perilaku yang tidak terduga:

<Tip>
[Diagnostik cache](/docs/id/build-with-claude/cache-diagnostics) (beta) membuat API membandingkan permintaan berturut-turut dan melaporkan dengan tepat di mana prefiks prompt menyimpang, yang secara otomatis menangani banyak langkah dalam daftar ini.
</Tip>

- Pastikan bagian yang di-cache identik di seluruh panggilan. Untuk breakpoint eksplisit, verifikasi bahwa penanda `cache_control` berada di lokasi yang sama
- Periksa bahwa panggilan dilakukan dalam masa hidup cache (5 menit secara default)
- Verifikasi bahwa `tool_choice` dan penggunaan gambar tetap konsisten antar panggilan
- Validasi bahwa Anda meng-cache setidaknya jumlah token minimum untuk model dan platform Anda (lihat [Batasan cache](#cache-limitations))
- Konfirmasi breakpoint Anda berada pada blok yang tetap identik di seluruh permintaan. Penulisan cache hanya terjadi di breakpoint, dan jika blok tersebut berubah (timestamp, konteks per-permintaan, pesan masuk), hash prefiks tidak pernah cocok. Lookback tidak menemukan konten stabil di belakang breakpoint; lookback hanya menemukan entri yang ditulis oleh permintaan sebelumnya di breakpoint mereka sendiri
- Verifikasi bahwa kunci dalam blok konten `tool_use` Anda memiliki urutan yang stabil karena beberapa bahasa (misalnya, Swift, Go) mengacak urutan kunci selama konversi JSON, yang merusak cache
- Gunakan [diagnostik cache](/docs/id/build-with-claude/cache-diagnostics) agar API membandingkan permintaan berturut-turut dan melaporkan bagian prompt mana yang menyimpang

<Note>
Perubahan pada `tool_choice` atau ada/tidaknya gambar di mana pun dalam prompt akan membatalkan cache, mengharuskan entri cache baru dibuat. Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).
</Note>

---
## Durasi cache 1 jam \{#1-hour-cache-duration}

Jika Anda merasa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

<Note>
Durasi cache 1 jam tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Amazon Bedrock (legacy)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) (beta).
</Note>

Untuk menggunakan cache yang diperpanjang, sertakan `ttl` dalam definisi `cache_control` seperti ini:
```json hidelines={1,-1}
{
  "cache_control": {
    "type": "ephemeral",
    "ttl": "1h"
  }
}
```

Respons akan menyertakan informasi cache terperinci seperti berikut:
```json Output
{
  "usage": {
    "input_tokens": 2048,
    "cache_read_input_tokens": 1800,
    "cache_creation_input_tokens": 248,
    "output_tokens": 503,

    "cache_creation": {
      "ephemeral_5m_input_tokens": 148,
      "ephemeral_1h_input_tokens": 100
    }
  }
}
```

Perhatikan bahwa field `cache_creation_input_tokens` saat ini sama dengan jumlah nilai dalam objek `cache_creation`.

Jika Anda melihat penulisan `ephemeral_5m_input_tokens` yang tidak Anda minta saat menggunakan alat server seperti pencarian web, lihat [panduan ini tentang caching prompt dan penggunaan alat](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#server-tool-results-are-cached-automatically).

### Kapan menggunakan cache 1 jam \{#when-to-use-the-1-hour-cache}

Jika Anda memiliki prompt yang digunakan pada irama reguler (yaitu, prompt sistem yang digunakan lebih sering dari setiap 5 menit), terus gunakan cache 5 menit, karena ini akan terus diperbarui tanpa biaya tambahan.

Cache 1 jam paling baik digunakan dalam skenario berikut:
- Ketika Anda memiliki prompt yang kemungkinan digunakan kurang sering dari 5 menit, tetapi lebih sering dari setiap jam. Misalnya, ketika side-agent agentic akan memakan waktu lebih dari 5 menit, atau ketika menyimpan percakapan chat panjang dengan pengguna dan Anda umumnya mengharapkan pengguna tersebut mungkin tidak merespons dalam 5 menit berikutnya.
- Ketika latensi penting dan prompt lanjutan Anda mungkin dikirim setelah 5 menit.
- Ketika Anda ingin meningkatkan pemanfaatan batas laju Anda, karena cache hit tidak dikurangi dari batas laju Anda.

<Note>
Cache 5 menit dan 1 jam berperilaku sama sehubungan dengan latensi. Anda umumnya akan melihat peningkatan time-to-first-token untuk dokumen panjang.
</Note>

### Mencampur TTL yang berbeda \{#mixing-different-ttls}

Anda dapat menggunakan kontrol cache 1 jam dan 5 menit dalam permintaan yang sama, tetapi dengan batasan penting: Entri cache dengan TTL lebih panjang harus muncul sebelum TTL yang lebih pendek (yaitu, entri cache 1 jam harus muncul sebelum entri cache 5 menit mana pun).

Ketika mencampur TTL, API menentukan tiga lokasi penagihan dalam prompt Anda:
1. Posisi `A`: Jumlah token pada cache hit tertinggi (atau 0 jika tidak ada hit).
2. Posisi `B`: Jumlah token pada blok `cache_control` 1 jam tertinggi setelah `A` (atau sama dengan `A` jika tidak ada).
3. Posisi `C`: Jumlah token pada blok `cache_control` terakhir.

<Note>
Jika `B` dan/atau `C` lebih besar dari `A`, keduanya pasti merupakan cache miss, karena `A` adalah cache hit tertinggi.
</Note>

Anda akan dikenakan biaya untuk:
1. Token pembacaan cache untuk `A`.
2. Token penulisan cache 1 jam untuk `(B - A)`.
3. Token penulisan cache 5 menit untuk `(C - B)`.

Berikut adalah 3 contoh. Ini menggambarkan token input dari 3 permintaan, yang masing-masing memiliki cache hit dan cache miss yang berbeda. Masing-masing memiliki harga terhitung yang berbeda, ditunjukkan dalam kotak berwarna, sebagai hasilnya.
![Diagram Mencampur TTL](/docs/images/prompt-cache-mixed-ttl.svg)

---
## Pre-warming cache \{#pre-warming-the-cache}

Pre-warming cache memungkinkan Anda memuat prompt sistem atau definisi alat Anda ke dalam cache prompt sebelum pengguna memicu permintaan nyata. Ini menghilangkan penalti latensi cache-miss pada interaksi pengguna pertama, mengurangi "time-to-first-token" (waktu ke token pertama), atau TTFT, untuk aplikasi yang sensitif terhadap latensi.

### Cara kerjanya \{#how-it-works}

Atur `max_tokens: 0` dalam permintaan Anda. API membaca prompt Anda ke dalam model dan menulis cache di breakpoint `cache_control` mana pun, lalu segera kembali tanpa menghasilkan output apa pun. Respons memiliki array `content` kosong, `stop_reason: "max_tokens"`, dan blok `usage` yang terisi penuh.

Tempatkan breakpoint `cache_control` pada blok terakhir yang dibagikan dengan permintaan lanjutan (biasanya prompt sistem atau definisi alat Anda), bukan pada pesan pengguna placeholder. Jika tidak, entri cache dikunci ke placeholder dan permintaan lanjutan tidak akan mengenainya. Ini berarti menggunakan [breakpoint cache eksplisit](#explicit-cache-breakpoints) daripada [caching otomatis](#automatic-caching), karena caching otomatis menempatkan breakpoint pada blok terakhir, yang di sini adalah placeholder. Pesan pengguna placeholder dapat berupa string apa pun dengan konten non-whitespace (contoh di sini menggunakan `"warmup"`); kontennya dibaca ke dalam model tetapi tidak pernah dijawab.

<Note>
Permintaan pre-warm dikenakan biaya **penulisan cache** jika prefiks belum di-cache, sama seperti permintaan lainnya. Periksa `usage.cache_creation_input_tokens` dalam respons untuk mengonfirmasi penulisan terjadi. Nol token output yang ditagih.
</Note>

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 0,
    "system": [
      {
        "type": "text",
        "text": "You are an expert software engineer with deep knowledge of distributed systems...",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    "messages": [{"role": "user", "content": "warmup"}]
  }'
```

```bash CLI
ant messages create \
  --transform '{stop_reason,content,usage}' --format yaml <<'YAML'
model: claude-opus-4-8
max_tokens: 0
system:
  - type: text
    text: >-
      You are an expert software engineer with deep knowledge of
      distributed systems...
    cache_control:
      type: ephemeral
messages:
  - role: user
    content: warmup
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Jalankan ini sebelum pengguna datang untuk menghangatkan cache prompt sistem bersama.
prewarm = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=0,
    system=[
        {
            "type": "text",
            "text": "You are an expert software engineer with deep knowledge of distributed systems...",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "warmup"}],
)
print(prewarm.stop_reason)  # "max_tokens"
print(prewarm.content)  # []
print(prewarm.usage)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Jalankan ini sebelum pengguna datang untuk menghangatkan cache prompt sistem bersama.
const prewarm = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 0,
  system: [
    {
      type: "text",
      text: "You are an expert software engineer with deep knowledge of distributed systems...",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [{ role: "user", content: "warmup" }]
});
console.log(prewarm.stop_reason); // "max_tokens"
console.log(prewarm.content); // []
console.log(prewarm.usage);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var prewarm = await client.Messages.Create(
    new()
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 0,
        System = new(
            [
                new TextBlockParam
                {
                    Text = "You are an expert software engineer with deep knowledge of distributed systems...",
                    CacheControl = new(),
                },
            ]
        ),
        Messages = [new() { Role = Role.User, Content = "warmup" }],
    }
);

Console.WriteLine(prewarm.StopReason?.Raw()); // "max_tokens"
Console.WriteLine(prewarm.Content.Count); // 0
Console.WriteLine(prewarm.Usage);
```

```go Go hidelines={1..10,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	prewarm, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 0,
		System: []anthropic.TextBlockParam{
			{
				Text:         "You are an expert software engineer with deep knowledge of distributed systems...",
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("warmup")),
		},
	})
	if err != nil {
		panic(err)
	}

	fmt.Println(prewarm.StopReason) // "max_tokens"
	fmt.Println(prewarm.Content)    // []
	fmt.Println(prewarm.Usage.RawJSON())
}
```

```java Java hidelines={1..9,-1..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Message prewarm = client.messages().create(MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(0)
            .systemOfTextBlockParams(List.of(TextBlockParam.builder()
                    .text("You are an expert software engineer with deep knowledge of distributed systems...")
                    .cacheControl(CacheControlEphemeral.builder().build())
                    .build()))
            .addUserMessage("warmup")
            .build());

    IO.println(prewarm.stopReason()); // Optional[max_tokens]
    IO.println(prewarm.content());    // []
    IO.println(prewarm.usage());
}
```

```php PHP hidelines={1..5}
<?php

use Anthropic\Client;
use Anthropic\Messages\Model;

$client = new Client();

$prewarm = $client->messages->create(
    model: Model::CLAUDE_OPUS_4_8,
    maxTokens: 0,
    system: [
        [
            'type' => 'text',
            'text' => 'You are an expert software engineer with deep knowledge of distributed systems...',
            'cache_control' => ['type' => 'ephemeral'],
        ],
    ],
    messages: [['role' => 'user', 'content' => 'warmup']],
);

echo $prewarm->stopReason->value, PHP_EOL; // "max_tokens"
echo json_encode($prewarm->content), PHP_EOL; // []
echo json_encode($prewarm->usage), PHP_EOL;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

prewarm = client.messages.create(
  model: Anthropic::Model::CLAUDE_OPUS_4_8,
  max_tokens: 0,
  system_: [
    {
      type: "text",
      text: "You are an expert software engineer with deep knowledge of distributed systems...",
      cache_control: {type: "ephemeral"}
    }
  ],
  messages: [{role: "user", content: "warmup"}]
)

puts prewarm.stop_reason # :max_tokens
puts prewarm.content # []
puts prewarm.usage
```

</CodeGroup>

API mengembalikan array `content` kosong:

```json Output
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [],
  "model": "claude-opus-4-8",
  "stop_reason": "max_tokens",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 8,
    "cache_creation_input_tokens": 5120,
    "cache_read_input_tokens": 0,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 5120,
      "ephemeral_1h_input_tokens": 0
    },
    "iterations": [
      {
        "input_tokens": 8,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 5120,
        "cache_creation": {
          "ephemeral_5m_input_tokens": 5120,
          "ephemeral_1h_input_tokens": 0
        },
        "type": "message"
      }
    ],
    "output_tokens": 0,
    "service_tier": "standard",
    "inference_geo": "global"
  }
}
```

### Pola penggunaan umum \{#typical-usage-pattern}

Jalankan permintaan pre-warm ketika aplikasi Anda dimulai (atau pada interval terjadwal), lalu kirim permintaan pengguna nyata setelah pre-warm selesai:

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": "You are an expert software engineer with deep knowledge of distributed systems...",
        "cache_control": {"type": "ephemeral"},
    }
]


def prewarm_cache() -> None:
    """Call this at application startup or on a scheduled interval."""
    client.messages.create(
        model="claude-opus-4-8",
        max_tokens=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": "warmup"}],
    )


def respond(user_message: str) -> anthropic.types.Message:
    """The real user request; benefits from a warm cache."""
    return client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )


# Panaskan cache sebelum lalu lintas pengguna tiba.
prewarm_cache()

# Kemudian, saat pengguna mengirim pesan, prefiks prompt sistem sudah di-cache.
response = respond("How do I implement a binary search tree?")
print(response.content[0].text)
```

Perlu diingat bahwa TTL cache tetap berlaku. Untuk cache 5 menit default, kirim permintaan pre-warm baru setidaknya setiap 5 menit untuk menjaga cache tetap hangat. Untuk jeda yang lebih lama antar permintaan pengguna, gunakan [durasi cache 1 jam](#1-hour-cache-duration) sebagai gantinya.

### Batasan \{#limitations}

Permintaan dengan `max_tokens: 0` akan ditolak dengan `invalid_request_error` jika salah satu dari hal berikut diatur, karena masing-masing menyiratkan output yang tidak dapat dihasilkan oleh anggaran nol token:

- `stream: true`
- [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) (`thinking.type: "enabled"`)
- [Output terstruktur](/docs/id/build-with-claude/structured-outputs) (`output_config.format`)
- `tool_choice` berupa `{"type": "tool", ...}` atau `{"type": "any"}`

`max_tokens: 0` juga ditolak di dalam permintaan [Message Batches](/docs/id/build-with-claude/batch-processing). Pre-warming menargetkan time-to-first-token, yang tidak berlaku untuk pemrosesan batch, dan entri cache yang ditulis selama pemrosesan batch kemungkinan besar akan kedaluwarsa sebelum permintaan lanjutan dijalankan.

### Menggantikan solusi sementara max_tokens=1 \{#replacing-the-max-tokens-1-workaround}

Sebelum `max_tokens: 0` tersedia, beberapa aplikasi menggunakan panggilan warm-up `max_tokens: 1` untuk mencapai efek yang sama. Pendekatan `max_tokens: 0` lebih disarankan: tidak ada output yang dihasilkan, sehingga tidak ada balasan satu token yang perlu dibuang, tidak ada token output yang ditagih, dan maksud dari permintaan tersebut tidak ambigu.

---
## Contoh caching prompt \{#prompt-caching-examples}

Untuk membantu Anda memulai dengan caching prompt, [prompt caching cookbook](https://platform.claude.com/cookbook/misc-prompt-caching) menyediakan contoh terperinci dan praktik terbaik.

Cuplikan kode berikut menampilkan berbagai pola caching prompt. Contoh-contoh ini mendemonstrasikan cara mengimplementasikan caching dalam berbagai skenario, membantu Anda memahami penerapan praktis dari fitur ini:

<section title="Contoh caching konteks besar">

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "system": [
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents."
        },
        {
            "type": "text",
            "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "What are the key terms and conditions in this agreement?"
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
system:
  - type: text
    text: You are an AI assistant tasked with analyzing legal documents.
  - type: text
    text: >-
      Here is the full text of a complex legal agreement:
      [Insert full text of a 50-page legal agreement here]
    cache_control:
      type: ephemeral
messages:
  - role: user
    content: What are the key terms and conditions in this agreement?
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents.",
        },
        {
            "type": "text",
            "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "What are the key terms and conditions in this agreement?",
        }
    ],
)
print(response.usage.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an AI assistant tasked with analyzing legal documents."
    },
    {
      type: "text",
      text: "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "What are the key terms and conditions in this agreement?"
    }
  ]
});
console.log(response);
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new()
{
    ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
};

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    System = new MessageCreateParamsSystem(new List<TextBlockParam>
    {
        new TextBlockParam()
        {
            Text = "You are an AI assistant tasked with analyzing legal documents.",
        },
        new TextBlockParam()
        {
            Text = "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            CacheControl = new CacheControlEphemeral(),
        },
    }),
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "What are the key terms and conditions in this agreement?"
        }
    ]
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
		System: []anthropic.TextBlockParam{
			{
				Text: "You are an AI assistant tasked with analyzing legal documents.",
			},
			{
				Text:         "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What are the key terms and conditions in this agreement?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Usage)
}
```

```java Java hidelines={1..2,4..12,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class LegalDocumentAnalysisExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .systemOfTextBlockParams(
        List.of(
          TextBlockParam.builder()
            .text("You are an AI assistant tasked with analyzing legal documents.")
            .build(),
          TextBlockParam.builder()
            .text(
              "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        )
      )
      .addUserMessage("What are the key terms and conditions in this agreement?")
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'What are the key terms and conditions in this agreement?'
        ]
    ],
    model: 'claude-opus-4-8',
    system: [
        [
            'type' => 'text',
            'text' => 'You are an AI assistant tasked with analyzing legal documents.'
        ],
        [
            'type' => 'text',
            'text' => 'Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]',
            'cache_control' => ['type' => 'ephemeral']
        ]
    ],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an AI assistant tasked with analyzing legal documents."
    },
    {
      type: "text",
      text: "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "What are the key terms and conditions in this agreement?"
    }
  ]
)
puts message
```
</CodeGroup>
Contoh ini mendemonstrasikan penggunaan dasar caching prompt, dengan melakukan caching pada teks lengkap perjanjian hukum sebagai prefiks sambil membiarkan instruksi pengguna tidak di-cache.

Untuk permintaan pertama:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: Jumlah token dalam seluruh pesan sistem, termasuk dokumen hukum
- `cache_read_input_tokens`: 0 (tidak ada cache hit pada permintaan pertama)

Untuk permintaan berikutnya dalam masa aktif cache:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: 0 (tidak ada pembuatan cache baru)
- `cache_read_input_tokens`: Jumlah token dalam seluruh pesan sistem yang di-cache

</section>

<section title="Caching definisi alat">

Definisi alat dapat di-cache dengan menempatkan `cache_control` pada alat terakhir dalam array `tools` Anda. Semua alat yang didefinisikan sebelum dan termasuk alat tersebut di-cache sebagai satu prefiks.

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "input_schema": {
        "type": "object",
        "properties": { "location": { "type": "string" } },
        "required": ["location"]
      }
    },
    {
      "name": "get_time",
      "description": "Get the current time in a given time zone",
      "input_schema": {
        "type": "object",
        "properties": { "timezone": { "type": "string" } },
        "required": ["timezone"]
      },
      "cache_control": { "type": "ephemeral" }
    }
  ],
  "messages": [{ "role": "user", "content": "What is the weather and time in New York?" }]
}
```

Pada permintaan pertama, `cache_creation_input_tokens` mencerminkan jumlah token dari semua definisi alat. Pada permintaan berikutnya dalam masa aktif cache, token tersebut muncul di bawah `cache_read_input_tokens` sebagai gantinya.

Untuk interaksi terperinci antara definisi alat, `defer_loading`, dan invalidasi cache, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

</section>

<section title="Melanjutkan percakapan multi-giliran">

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "system": [
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, can you tell me more about the solar system?"
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Good to know."
                },
                {
                    "type": "text",
                    "text": "Tell me more about Mars.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
system:
  - type: text
    text: "...long system prompt"
    cache_control:
      type: ephemeral
messages:
  - role: user
    content:
      - type: text
        text: Hello, can you tell me more about the solar system?
  - role: assistant
    content: >-
      Certainly! The solar system is the collection of celestial bodies that
      orbit our Sun. It consists of eight planets, numerous moons, asteroids,
      comets, and other objects. The planets, in order from closest to farthest
      from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus,
      and Neptune. Each planet has its own unique characteristics and features.
      Is there a specific aspect of the solar system you would like to know
      more about?
  - role: user
    content:
      - type: text
        text: Good to know.
      - type: text
        text: Tell me more about Mars.
        cache_control:
          type: ephemeral
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        # ...percakapan panjang sejauh ini
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, can you tell me more about the solar system?",
                }
            ],
        },
        {
            "role": "assistant",
            "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Good to know."},
                {
                    "type": "text",
                    "text": "Tell me more about Mars.",
                    "cache_control": {"type": "ephemeral"},
                },
            ],
        },
    ],
)
print(response.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "...long system prompt",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    // ...percakapan panjang sejauh ini
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Hello, can you tell me more about the solar system?"
        }
      ]
    },
    {
      role: "assistant",
      content:
        "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?"
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Good to know."
        },
        {
          type: "text",
          text: "Tell me more about Mars.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
});
console.log(response);
```

```csharp C# hidelines={1..6}
using Anthropic;
using Anthropic.Models.Messages;
using System.Collections.Generic;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    System = new MessageCreateParamsSystem(new List<TextBlockParam>
    {
        new TextBlockParam()
        {
            Text = "...long system prompt",
            CacheControl = new CacheControlEphemeral(),
        },
    }),
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = new MessageParamContent(new List<ContentBlockParam>
            {
                new ContentBlockParam(new TextBlockParam("Hello, can you tell me more about the solar system?")),
            }),
        },
        new()
        {
            Role = Role.Assistant,
            Content = "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
        },
        new()
        {
            Role = Role.User,
            Content = new MessageParamContent(new List<ContentBlockParam>
            {
                new ContentBlockParam(new TextBlockParam("Good to know.")),
                new ContentBlockParam(new TextBlockParam()
                {
                    Text = "Tell me more about Mars.",
                    CacheControl = new CacheControlEphemeral(),
                }),
            })
        }
    ]
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
		System: []anthropic.TextBlockParam{
			{
				Text:         "...long system prompt",
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, can you tell me more about the solar system?")),
			anthropic.NewAssistantMessage(anthropic.NewTextBlock("Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?")),
			{
				Role: anthropic.MessageParamRoleUser,
				Content: []anthropic.ContentBlockParamUnion{
					anthropic.NewTextBlock("Good to know."),
					{OfText: &anthropic.TextBlockParam{
						Text:         "Tell me more about Mars.",
						CacheControl: anthropic.NewCacheControlEphemeralParam(),
					}},
				},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..2,4..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class ConversationWithCacheControlExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Buat prompt sistem sementara
    TextBlockParam systemPrompt = TextBlockParam.builder()
      .text("...long system prompt")
      .cacheControl(CacheControlEphemeral.builder().build())
      .build();

    // Buat parameter pesan
    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .systemOfTextBlockParams(List.of(systemPrompt))
      // Pesan pengguna pertama (tanpa cache control)
      .addUserMessage("Hello, can you tell me more about the solar system?")
      // Respons asisten
      .addAssistantMessage(
        "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
      )
      // Pesan pengguna kedua (dengan cache control)
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(TextBlockParam.builder().text("Good to know.").build()),
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text("Tell me more about Mars.")
              .cacheControl(CacheControlEphemeral.builder().build())
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'Hello, can you tell me more about the solar system?'
                ]
            ]
        ],
        [
            'role' => 'assistant',
            'content' => "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
        ],
        [
            'role' => 'user',
            'content' => [
                ['type' => 'text', 'text' => 'Good to know.'],
                [
                    'type' => 'text',
                    'text' => 'Tell me more about Mars.',
                    'cache_control' => ['type' => 'ephemeral']
                ]
            ]
        ]
    ],
    model: 'claude-opus-4-8',
    system: [
        [
            'type' => 'text',
            'text' => '...long system prompt',
            'cache_control' => ['type' => 'ephemeral']
        ]
    ],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "...long system prompt",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Hello, can you tell me more about the solar system?"
        }
      ]
    },
    {
      role: "assistant",
      content: "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
    },
    {
      role: "user",
      content: [
        { type: "text", text: "Good to know." },
        {
          type: "text",
          text: "Tell me more about Mars.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
)
puts message
```
</CodeGroup>

Contoh ini mendemonstrasikan cara menggunakan caching prompt dalam percakapan multi-giliran.

Pada setiap giliran, blok terakhir dari pesan terakhir ditandai dengan `cache_control` sehingga percakapan dapat di-cache secara inkremental. Sistem akan secara otomatis mencari dan menggunakan urutan blok terpanjang yang sebelumnya di-cache untuk pesan lanjutan. Artinya, blok yang sebelumnya ditandai dengan blok `cache_control` kemudian tidak lagi ditandai dengan ini, tetapi blok tersebut akan tetap dianggap sebagai cache hit (dan juga cache refresh!) jika diakses dalam waktu 5 menit.

Selain itu, perhatikan bahwa parameter `cache_control` ditempatkan pada pesan sistem. Ini untuk memastikan bahwa jika pesan tersebut dikeluarkan dari cache (setelah tidak digunakan selama lebih dari 5 menit), pesan tersebut akan ditambahkan kembali ke cache pada permintaan berikutnya.

Pendekatan ini berguna untuk mempertahankan konteks dalam percakapan yang sedang berlangsung tanpa memproses informasi yang sama berulang kali.

Ketika ini diatur dengan benar, Anda akan melihat hal berikut dalam respons usage dari setiap permintaan:
- `input_tokens`: Jumlah token dalam pesan pengguna baru (akan minimal)
- `cache_creation_input_tokens`: Jumlah token dalam giliran asisten dan pengguna yang baru
- `cache_read_input_tokens`: Jumlah token dalam percakapan hingga giliran sebelumnya

</section>

<section title="Menggabungkan semuanya: Beberapa cache breakpoint">

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "tools": [
        {
            "name": "search_documents",
            "description": "Search through the knowledge base",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_document",
            "description": "Retrieve a specific document by ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Document ID"
                    }
                },
                "required": ["doc_id"]
            },
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "system": [
        {
            "type": "text",
            "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "Can you search for information about Mars rovers?"
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_1",
                    "name": "search_documents",
                    "input": {"query": "Mars rovers"}
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "tool_1",
                    "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Yes, please tell me about the Perseverance rover specifically.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
tools:
  - name: search_documents
    description: Search through the knowledge base
    input_schema:
      type: object
      properties:
        query:
          type: string
          description: Search query
      required: [query]
  - name: get_document
    description: Retrieve a specific document by ID
    input_schema:
      type: object
      properties:
        doc_id:
          type: string
          description: Document ID
      required: [doc_id]
    cache_control:
      type: ephemeral
system:
  - type: text
    text: |-
      You are a helpful research assistant with access to a document knowledge base.

      # Instruksi
      - Always search for relevant documents before answering
      - Provide citations for your sources
      - Be objective and accurate in your responses
      - If multiple documents contain relevant information, synthesize them
      - Acknowledge when information is not available in the knowledge base
    cache_control:
      type: ephemeral
  - type: text
    text: |-
      # Konteks Basis Pengetahuan

      Here are the relevant documents for this conversation:

      ## Dokumen 1: Gambaran Umum Tata Surya
      The solar system consists of the Sun and all objects that orbit it...

      ## Dokumen 2: Karakteristik Planet
      Each planet has unique features. Mercury is the smallest planet...

      ## Dokumen 3: Eksplorasi Mars
      Mars has been a target of exploration for decades...

      [Additional documents...]
    cache_control:
      type: ephemeral
messages:
  - role: user
    content: Can you search for information about Mars rovers?
  - role: assistant
    content:
      - type: tool_use
        id: tool_1
        name: search_documents
        input:
          query: Mars rovers
  - role: user
    content:
      - type: tool_result
        tool_use_id: tool_1
        content: >-
          Found 3 relevant documents: Document 3 (Mars Exploration),
          Document 7 (Rover Technology), Document 9 (Mission History)
  - role: assistant
    content:
      - type: text
        text: >-
          I found 3 relevant documents about Mars rovers. Let me get more
          details from the Mars Exploration document.
  - role: user
    content:
      - type: text
        text: Yes, please tell me about the Perseverance rover specifically.
        cache_control:
          type: ephemeral
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[
        {
            "name": "search_documents",
            "description": "Search through the knowledge base",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_document",
            "description": "Retrieve a specific document by ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "string", "description": "Document ID"}
                },
                "required": ["doc_id"],
            },
            "cache_control": {"type": "ephemeral"},
        },
    ],
    system=[
        {
            "type": "text",
            "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "Can you search for information about Mars rovers?",
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_1",
                    "name": "search_documents",
                    "input": {"query": "Mars rovers"},
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "tool_1",
                    "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Yes, please tell me about the Perseverance rover specifically.",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
    ],
)
print(response.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      name: "search_documents",
      description: "Search through the knowledge base",
      input_schema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Search query"
          }
        },
        required: ["query"]
      }
    },
    {
      name: "get_document",
      description: "Retrieve a specific document by ID",
      input_schema: {
        type: "object",
        properties: {
          doc_id: {
            type: "string",
            description: "Document ID"
          }
        },
        required: ["doc_id"]
      },
      cache_control: { type: "ephemeral" }
    }
  ],
  system: [
    {
      type: "text",
      text: "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
      cache_control: { type: "ephemeral" }
    },
    {
      type: "text",
      text: "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "Can you search for information about Mars rovers?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "tool_use",
          id: "tool_1",
          name: "search_documents",
          input: { query: "Mars rovers" }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "tool_1",
          content:
            "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
        }
      ]
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Yes, please tell me about the Perseverance rover specifically.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
});
console.log(response);
```

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new()
{
    ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
};

var parameters = new MessageCreateParams
{
    Model = Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Tools =
    [
        new ToolUnion(new Tool()
        {
            Name = "search_documents",
            Description = "Search through the knowledge base",
            InputSchema = new InputSchema()
            {
                Properties = new Dictionary<string, JsonElement>
                {
                    ["query"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Search query" }),
                },
                Required = ["query"],
            },
        }),
        new ToolUnion(new Tool()
        {
            Name = "get_document",
            Description = "Retrieve a specific document by ID",
            InputSchema = new InputSchema()
            {
                Properties = new Dictionary<string, JsonElement>
                {
                    ["doc_id"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Document ID" }),
                },
                Required = ["doc_id"],
            },
            CacheControl = new CacheControlEphemeral(),
        }),
    ],
    System = new MessageCreateParamsSystem(new List<TextBlockParam>
    {
        new TextBlockParam()
        {
            Text = "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            CacheControl = new CacheControlEphemeral(),
        },
        new TextBlockParam()
        {
            Text = "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            CacheControl = new CacheControlEphemeral(),
        },
    }),
    Messages =
    [
        new() { Role = Role.User, Content = "Can you search for information about Mars rovers?" },
        new()
        {
            Role = Role.Assistant,
            Content = new MessageParamContent(new List<ContentBlockParam>
            {
                new ContentBlockParam(new ToolUseBlockParam()
                {
                    ID = "tool_1",
                    Name = "search_documents",
                    Input = new Dictionary<string, JsonElement>
                    {
                        ["query"] = JsonSerializer.SerializeToElement("Mars rovers"),
                    },
                }),
            }),
        },
        new()
        {
            Role = Role.User,
            Content = new MessageParamContent(new List<ContentBlockParam>
            {
                new ContentBlockParam(new ToolResultBlockParam()
                {
                    ToolUseID = "tool_1",
                    Content = "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)",
                }),
            }),
        },
        new()
        {
            Role = Role.Assistant,
            Content = "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.",
        },
        new()
        {
            Role = Role.User,
            Content = new MessageParamContent(new List<ContentBlockParam>
            {
                new ContentBlockParam(new TextBlockParam()
                {
                    Text = "Yes, please tell me about the Perseverance rover specifically.",
                    CacheControl = new CacheControlEphemeral(),
                }),
            }),
        },
    ]
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
		Tools: []anthropic.ToolUnionParam{
			{OfTool: &anthropic.ToolParam{
				Name:        "search_documents",
				Description: anthropic.String("Search through the knowledge base"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"query": map[string]any{
							"type":        "string",
							"description": "Search query",
						},
					},
					Required: []string{"query"},
				},
			}},
			{OfTool: &anthropic.ToolParam{
				Name:        "get_document",
				Description: anthropic.String("Retrieve a specific document by ID"),
				InputSchema: anthropic.ToolInputSchemaParam{
					Properties: map[string]any{
						"doc_id": map[string]any{
							"type":        "string",
							"description": "Document ID",
						},
					},
					Required: []string{"doc_id"},
				},
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			}},
		},
		System: []anthropic.TextBlockParam{
			{
				Text:         "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			},
			{
				Text:         "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Can you search for information about Mars rovers?")),
			anthropic.NewAssistantMessage(anthropic.NewToolUseBlock(
				"tool_1",
				map[string]any{"query": "Mars rovers"},
				"search_documents",
			)),
			anthropic.NewUserMessage(anthropic.NewToolResultBlock(
				"tool_1",
				"Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)",
				false,
			)),
			anthropic.NewAssistantMessage(anthropic.NewTextBlock("I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.")),
			{
				Role: anthropic.MessageParamRoleUser,
				Content: []anthropic.ContentBlockParamUnion{
					{OfText: &anthropic.TextBlockParam{
						Text:         "Yes, please tell me about the Perseverance rover specifically.",
						CacheControl: anthropic.NewCacheControlEphemeralParam(),
					}},
				},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..3,5..19,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlockParam;
import java.util.List;
import java.util.Map;

public class MultipleCacheBreakpointsExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Skema alat pencarian
    InputSchema searchSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("query", Map.of("type", "string", "description", "Search query"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("query")))
      .build();

    // Skema alat pengambilan dokumen
    InputSchema getDocSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("doc_id", Map.of("type", "string", "description", "Document ID"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("doc_id")))
      .build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      // Alat dengan cache control pada yang terakhir
      .addTool(
        Tool.builder()
          .name("search_documents")
          .description("Search through the knowledge base")
          .inputSchema(searchSchema)
          .build()
      )
      .addTool(
        Tool.builder()
          .name("get_document")
          .description("Retrieve a specific document by ID")
          .inputSchema(getDocSchema)
          .cacheControl(CacheControlEphemeral.builder().build())
          .build()
      )
      // Prompt sistem dengan cache control pada instruksi dan konteks secara terpisah
      .systemOfTextBlockParams(
        List.of(
          TextBlockParam.builder()
            .text(
              "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build(),
          TextBlockParam.builder()
            .text(
              "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        )
      )
      // Riwayat percakapan
      .addUserMessage("Can you search for information about Mars rovers?")
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofToolUse(
            ToolUseBlockParam.builder()
              .id("tool_1")
              .name("search_documents")
              .input(JsonValue.from(Map.of("query", "Mars rovers")))
              .build()
          )
        )
      )
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofToolResult(
            ToolResultBlockParam.builder()
              .toolUseId("tool_1")
              .content(
                "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
              )
              .build()
          )
        )
      )
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text(
                "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
              )
              .build()
          )
        )
      )
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text("Yes, please tell me about the Perseverance rover specifically.")
              .cacheControl(CacheControlEphemeral.builder().build())
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'Can you search for information about Mars rovers?'
        ],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'tool_use',
                    'id' => 'tool_1',
                    'name' => 'search_documents',
                    'input' => ['query' => 'Mars rovers']
                ]
            ]
        ],
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'tool_result',
                    'tool_use_id' => 'tool_1',
                    'content' => 'Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)'
                ]
            ]
        ],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.'
                ]
            ]
        ],
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'Yes, please tell me about the Perseverance rover specifically.',
                    'cache_control' => ['type' => 'ephemeral']
                ]
            ]
        ]
    ],
    model: 'claude-opus-4-8',
    system: [
        [
            'type' => 'text',
            'text' => "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            'cache_control' => ['type' => 'ephemeral']
        ],
        [
            'type' => 'text',
            'text' => "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            'cache_control' => ['type' => 'ephemeral']
        ]
    ],
    tools: [
        [
            'name' => 'search_documents',
            'description' => 'Search through the knowledge base',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'query' => [
                        'type' => 'string',
                        'description' => 'Search query'
                    ]
                ],
                'required' => ['query']
            ]
        ],
        [
            'name' => 'get_document',
            'description' => 'Retrieve a specific document by ID',
            'input_schema' => [
                'type' => 'object',
                'properties' => [
                    'doc_id' => [
                        'type' => 'string',
                        'description' => 'Document ID'
                    ]
                ],
                'required' => ['doc_id']
            ],
            'cache_control' => ['type' => 'ephemeral']
        ]
    ],
);

echo json_encode($message->usage), PHP_EOL;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      name: "search_documents",
      description: "Search through the knowledge base",
      input_schema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Search query"
          }
        },
        required: ["query"]
      }
    },
    {
      name: "get_document",
      description: "Retrieve a specific document by ID",
      input_schema: {
        type: "object",
        properties: {
          doc_id: {
            type: "string",
            description: "Document ID"
          }
        },
        required: ["doc_id"]
      },
      cache_control: { type: "ephemeral" }
    }
  ],
  system: [
    {
      type: "text",
      text: "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
      cache_control: { type: "ephemeral" }
    },
    {
      type: "text",
      text: "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "Can you search for information about Mars rovers?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "tool_use",
          id: "tool_1",
          name: "search_documents",
          input: { query: "Mars rovers" }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "tool_1",
          content: "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
        }
      ]
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Yes, please tell me about the Perseverance rover specifically.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
)
puts message
```
</CodeGroup>

Contoh komprehensif ini mendemonstrasikan cara menggunakan keempat cache breakpoint yang tersedia untuk mengoptimalkan bagian-bagian berbeda dari prompt Anda:

1. **Cache alat** (cache breakpoint 1): Parameter `cache_control` pada definisi alat terakhir melakukan caching pada semua definisi alat.

2. **Cache instruksi yang dapat digunakan kembali** (cache breakpoint 2): Instruksi statis dalam prompt sistem di-cache secara terpisah. Instruksi ini jarang berubah antar permintaan.

3. **Cache konteks RAG** (cache breakpoint 3): Dokumen basis pengetahuan di-cache secara independen, memungkinkan Anda memperbarui dokumen RAG tanpa membatalkan cache alat atau instruksi.

4. **Cache riwayat percakapan** (cache breakpoint 4): Pesan pengguna terakhir ditandai dengan `cache_control` untuk mengaktifkan caching inkremental dari percakapan seiring berjalannya waktu.

Pendekatan ini memberikan fleksibilitas maksimum:
- Jika Anda menambahkan giliran baru ke percakapan tanpa mengubah konten sebelumnya, keempat segmen cache digunakan kembali
- Jika Anda memperbarui dokumen RAG tetapi mempertahankan alat dan instruksi yang sama, dua segmen cache pertama digunakan kembali
- Jika Anda mengubah percakapan tetapi mempertahankan alat, instruksi, dan dokumen yang sama, tiga segmen pertama digunakan kembali
- Perubahan pada breakpoint mana pun membatalkan segmen tersebut dan semua yang ada setelahnya, sementara segmen cache sebelumnya tetap valid

Untuk permintaan pertama:
- `input_tokens`: Minimal (token setelah cache breakpoint terakhir, mendekati 0 dalam contoh ini)
- `cache_creation_input_tokens`: Token dalam semua segmen yang di-cache (alat + instruksi + dokumen RAG + riwayat percakapan)
- `cache_read_input_tokens`: 0 (tidak ada cache hit)

Untuk permintaan berikutnya dengan hanya pesan pengguna baru (dan breakpoint keempat dipindahkan ke pesan terakhir yang baru tersebut, seperti dalam contoh):
- `input_tokens`: Minimal (token setelah cache breakpoint terakhir, mendekati 0 dalam contoh ini)
- `cache_creation_input_tokens`: Token dalam pesan pengguna baru dan giliran asisten sebelumnya (segmen percakapan baru yang sedang di-cache)
- `cache_read_input_tokens`: Semua token yang sebelumnya di-cache (alat + instruksi + dokumen RAG + percakapan sebelumnya)

Pola ini sangat berguna untuk:
- Aplikasi RAG dengan konteks dokumen yang besar
- Sistem agen yang menggunakan banyak alat
- Percakapan jangka panjang yang perlu mempertahankan konteks
- Aplikasi yang perlu mengoptimalkan bagian-bagian berbeda dari prompt secara independen

</section>

## Retensi data \{#data-retention}

Caching prompt (baik otomatis maupun eksplisit) memenuhi syarat ZDR. Anthropic tidak menyimpan teks mentah dari prompt Anda atau respons Claude.

Representasi cache KV (key-value) dan hash kriptografis dari konten yang di-cache hanya disimpan dalam memori dan tidak disimpan secara permanen. Entri yang di-cache memiliki masa aktif minimum 5 menit (standar) atau 1 jam (diperpanjang), setelah itu entri tersebut akan segera dihapus, meskipun tidak langsung. Entri cache diisolasi antar organisasi dan, pada Claude API, Claude Platform di AWS, dan Microsoft Foundry (beta), antar workspace dalam satu organisasi.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

---
## FAQ \{#faq}

  <section title="Apakah saya memerlukan beberapa cache breakpoint atau cukup satu di akhir?">

    **Dalam sebagian besar kasus, satu cache breakpoint di akhir konten statis Anda sudah cukup.** Penulisan cache hanya terjadi pada blok yang Anda tandai. Tempatkan pada blok terakhir yang tetap identik di seluruh permintaan, dan setiap permintaan berikutnya akan membaca entri yang sama. Jika blok setelahnya bervariasi per permintaan (timestamp, pesan masuk), pertahankan breakpoint sebelum blok tersebut, pada blok stabil terakhir.

    Anda hanya memerlukan beberapa breakpoint jika:
    - Percakapan yang terus bertambah mendorong breakpoint Anda 20 blok atau lebih melewati penulisan cache terakhir, menempatkan entri sebelumnya di luar jendela lookback
    - Anda ingin melakukan caching pada bagian-bagian yang diperbarui pada frekuensi berbeda secara independen
    - Anda memerlukan kontrol eksplisit atas apa yang di-cache untuk optimasi biaya

    Contoh: Jika Anda memiliki instruksi sistem (jarang berubah) dan konteks RAG (berubah setiap hari), Anda mungkin menggunakan dua breakpoint untuk melakukan caching secara terpisah.
  
</section>

  <section title="Apakah cache breakpoint menambah biaya tambahan?">

    Tidak, cache breakpoint itu sendiri gratis. Anda hanya membayar untuk:
    - Menulis konten ke cache (25% lebih mahal dari token input dasar untuk TTL 5 menit)
    - Membaca dari cache (10% dari harga token input dasar)
    - Token input reguler untuk konten yang tidak di-cache

    Jumlah breakpoint tidak memengaruhi harga - hanya jumlah konten yang di-cache dan dibaca yang penting.
  
</section>

  <section title="Bagaimana cara menghitung total token input dari field usage?">

    Respons usage mencakup tiga field token input terpisah yang bersama-sama mewakili total input Anda:

    ```text
    total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
    ```

    - `cache_read_input_tokens`: Token yang diambil dari cache (semua yang ada sebelum cache breakpoint yang telah di-cache)
    - `cache_creation_input_tokens`: Token baru yang sedang ditulis ke cache (pada cache breakpoint)
    - `input_tokens`: Token **setelah cache breakpoint terakhir** yang tidak di-cache

    **Penting:** `input_tokens` TIDAK mewakili semua token input - hanya bagian setelah cache breakpoint terakhir Anda. Jika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil dari total input Anda.

    **Contoh:** Dengan dokumen 200k token yang di-cache dan pertanyaan pengguna 50 token:
    - `cache_read_input_tokens`: 200.000
    - `cache_creation_input_tokens`: 0
    - `input_tokens`: 50
    - **Total**: 200.050 token

    Rincian ini sangat penting untuk memahami biaya dan penggunaan batas laju Anda. Lihat [Melacak performa cache](#tracking-cache-performance) untuk detail lebih lanjut.
  
</section>

  <section title="Berapa masa aktif cache?">

    Masa aktif minimum default cache (TTL) adalah 5 menit. Masa aktif ini diperbarui setiap kali konten yang di-cache digunakan.

    Jika Anda merasa 5 menit terlalu singkat, Anthropic juga menawarkan [TTL cache 1 jam](#1-hour-cache-duration).
  
</section>

  <section title="Berapa banyak cache breakpoint yang dapat saya gunakan?">

    Anda dapat mendefinisikan hingga 4 cache breakpoint (menggunakan parameter `cache_control`) dalam prompt Anda.
  
</section>

  <section title="Apakah caching prompt tersedia untuk semua model?">

    Caching prompt didukung pada semua [model Claude yang aktif](/docs/id/about-claude/models/overview).
  
</section>

  <section title="Bagaimana caching prompt bekerja dengan pemikiran diperpanjang?">

    Prompt sistem dan alat yang di-cache akan digunakan kembali ketika parameter thinking berubah. Namun, perubahan thinking (mengaktifkan/menonaktifkan atau perubahan anggaran) akan membatalkan prefiks prompt yang sebelumnya di-cache dengan konten messages.

    Untuk detail lebih lanjut tentang invalidasi cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).

    Untuk informasi lebih lanjut tentang pemikiran diperpanjang, termasuk interaksinya dengan penggunaan alat dan caching prompt, lihat [dokumentasi pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#extended-thinking-and-prompt-caching).
  
</section>

  <section title="Bagaimana cara mengaktifkan caching prompt?">

    Cara termudah adalah menambahkan `"cache_control": {"type": "ephemeral"}` di tingkat teratas body permintaan Anda ([caching otomatis](#automatic-caching)). Sebagai alternatif, sertakan setidaknya satu breakpoint `cache_control` pada blok konten individual ([cache breakpoint eksplisit](#explicit-cache-breakpoints)).
  
</section>

  <section title="Dapatkah saya menggunakan caching prompt dengan fitur API lainnya?">

    Ya, caching prompt dapat digunakan bersama fitur API lainnya seperti penggunaan alat dan kemampuan vision. Namun, mengubah apakah ada gambar dalam prompt atau memodifikasi pengaturan penggunaan alat akan merusak cache.

    Untuk detail lebih lanjut tentang invalidasi cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).
  
</section>

  <section title="Bagaimana caching prompt memengaruhi harga?">

    Caching prompt memperkenalkan struktur harga baru di mana penulisan cache 5 menit berbiaya 25% lebih mahal dari token input dasar, penulisan cache 1 jam berbiaya 2x token input dasar, dan cache hit hanya berbiaya 10% dari harga token input dasar.
  
</section>

  <section title="Dapatkah saya menghapus cache secara manual?">

    Saat ini, tidak ada cara untuk menghapus cache secara manual. Prefiks yang di-cache secara otomatis kedaluwarsa setelah minimal 5 menit tidak aktif.
  
</section>

  <section title="Bagaimana cara melacak efektivitas strategi caching saya?">

    Anda dapat memantau performa cache menggunakan field `cache_creation_input_tokens` dan `cache_read_input_tokens` dalam respons API.
  
</section>

  <section title="Apa yang dapat merusak cache?">

    Lihat [Apa yang membatalkan cache](#what-invalidates-the-cache) untuk detail lebih lanjut tentang invalidasi cache, termasuk daftar perubahan yang memerlukan pembuatan entri cache baru.
  
</section>

  <section title="Bagaimana caching prompt menangani privasi dan pemisahan data?">

Caching prompt dirancang dengan langkah-langkah privasi dan pemisahan data yang kuat:

1. Kunci cache dihasilkan menggunakan hash kriptografis dari prompt hingga titik cache control. Ini berarti hanya permintaan dengan prompt yang identik yang dapat mengakses cache tertentu.

2. Pada Claude API, Claude Platform di AWS, dan Microsoft Foundry (beta), cache diisolasi per workspace dalam satu organisasi. Pada Bedrock dan Vertex AI, cache diisolasi per organisasi. Dalam setiap kasus, cache tidak pernah dibagikan antar organisasi, bahkan untuk prompt yang identik. Lihat [Penyimpanan dan berbagi cache](#cache-storage-and-sharing) untuk detailnya.

3. Mekanisme caching dirancang untuk menjaga integritas dan privasi setiap percakapan atau konteks yang unik.

4. Aman untuk menggunakan `cache_control` di mana saja dalam prompt Anda. Agar caching menghasilkan pembacaan, tempatkan breakpoint di akhir prefiks yang stabil: menempatkannya pada blok yang berubah setiap permintaan (seperti timestamp atau input sembarang dari pengguna) akan menulis entri baru setiap kali dan tidak pernah menghasilkan hit.

Langkah-langkah ini memastikan bahwa caching prompt menjaga privasi dan keamanan data sambil menawarkan manfaat performa.

  
</section>
  <section title="Dapatkah saya menggunakan caching prompt dengan Batches API?">

    Ya, dimungkinkan untuk menggunakan caching prompt dengan permintaan [Batches API](/docs/id/build-with-claude/batch-processing) Anda. Namun, karena permintaan batch asinkron dapat diproses secara bersamaan dan dalam urutan apa pun, cache hit disediakan berdasarkan upaya terbaik.

    [Cache 1 jam](#1-hour-cache-duration) dapat membantu meningkatkan cache hit Anda. Cara paling hemat biaya untuk menggunakannya adalah sebagai berikut:
    - Kumpulkan sekumpulan permintaan pesan yang memiliki prefiks bersama.
    - Kirim permintaan batch dengan satu permintaan yang memiliki prefiks bersama ini dan blok cache 1 jam. Ini menulis prefiks ke cache 1 jam.
    - Segera setelah ini selesai, kirim sisa permintaan. Anda harus memantau job untuk mengetahui kapan selesai.

    Ini biasanya lebih baik daripada menggunakan cache 5 menit karena permintaan batch umumnya membutuhkan waktu antara 5 menit dan 1 jam untuk selesai.
  
</section>
  <section title="Mengapa saya melihat error `AttributeError: 'Beta' object has no attribute 'prompt_caching'` di Python?">

  Error ini biasanya muncul ketika Anda telah meng-upgrade SDK Anda atau Anda menggunakan contoh kode yang sudah usang. Caching prompt tidak lagi memerlukan prefiks beta. Alih-alih:
    <CodeGroup>
      
      ```python Python nocheck
      client.beta.prompt_caching.messages.create(**params)
      ```

      
      ```typescript TypeScript nocheck hidelines={1..2}
      import Anthropic from "@anthropic-ai/sdk";

      const client = new Anthropic();

      const response = await client.beta.promptCaching.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an expert on this large document...",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [{ role: "user", content: "Summarize the key points" }]
      });

      console.log(response);
      ```

      
      ```php PHP hidelines={1..4} nocheck
      <?php

      use Anthropic\Client;

      $client = new Client();

      $message = $client->beta->promptCaching->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Summarize the key points']
          ],
          model: 'claude-opus-4-8',
          system: [
              [
                  'type' => 'text',
                  'text' => 'You are an expert on this large document...',
                  'cache_control' => ['type' => 'ephemeral']
              ]
          ],
      );

      echo $message->content[0]->text;
      ```

      
      ```ruby Ruby nocheck hidelines={1..2}
      require "anthropic"

      client = Anthropic::Client.new

      message = client.beta.prompt_caching.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an expert on this large document...",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Summarize the key points" }
        ]
      )
      puts message.content.first.text
      ```
    </CodeGroup>
    Gunakan:
    <CodeGroup>
      
      ```python Python nocheck
      client.messages.create(**params)
      ```

      ```typescript TypeScript hidelines={1..2}
      import Anthropic from "@anthropic-ai/sdk";

      const client = new Anthropic();

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an expert on this large document...",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [{ role: "user", content: "Summarize the key points" }]
      });

      console.log(response);
      ```

      ```php PHP hidelines={1..4}
      <?php

      use Anthropic\Client;

      $client = new Client();

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Summarize the key points']
          ],
          model: 'claude-opus-4-8',
          system: [
              [
                  'type' => 'text',
                  'text' => 'You are an expert on this large document...',
                  'cache_control' => ['type' => 'ephemeral']
              ]
          ],
      );

      echo $message->content[0]->text;
      ```

      ```ruby Ruby hidelines={1..2}
      require "anthropic"

      client = Anthropic::Client.new

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        system: [
          {
            type: "text",
            text: "You are an expert on this large document...",
            cache_control: { type: "ephemeral" }
          }
        ],
        messages: [
          { role: "user", content: "Summarize the key points" }
        ]
      )
      puts message.content.first.text
      ```
    </CodeGroup>
  
</section>
  <section title="Mengapa saya melihat 'TypeError: Cannot read properties of undefined (reading 'messages')'?">

  Error ini biasanya muncul ketika Anda telah meng-upgrade SDK Anda atau Anda menggunakan contoh kode yang sudah usang. Caching prompt tidak lagi memerlukan prefiks beta. Alih-alih:

      ```typescript TypeScript
      client.beta.promptCaching.messages.create(/* ... */);
      ```

      Cukup gunakan:

      ```typescript
      client.messages.create(/* ... */);
      ```
  
</section>