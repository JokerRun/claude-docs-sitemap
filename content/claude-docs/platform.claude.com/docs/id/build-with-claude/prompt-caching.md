---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-caching
fetched_at: 2026-04-17T03:11:44.711743Z
sha256: bebb78ece06e019d102d5b25ca8af7cbf65e5b746aec351d457388c3a127b10c
---

# Prompt caching

Optimalkan penggunaan API Anda dengan memungkinkan melanjutkan dari awalan spesifik dalam prompt Anda. Ini secara signifikan mengurangi waktu pemrosesan dan biaya untuk tugas berulang atau prompt dengan elemen konsisten.

---

Prompt caching mengoptimalkan penggunaan API Anda dengan memungkinkan melanjutkan dari awalan spesifik dalam prompt Anda. Ini secara signifikan mengurangi waktu pemrosesan dan biaya untuk tugas berulang atau prompt dengan elemen konsisten.

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Ada dua cara untuk mengaktifkan prompt caching:

- **[Automatic caching](#automatic-caching)**: Tambahkan satu bidang `cache_control` di tingkat atas permintaan Anda. Sistem secara otomatis menerapkan breakpoint cache ke blok yang dapat di-cache terakhir dan memindahkannya maju seiring percakapan berkembang. Terbaik untuk percakapan multi-turn di mana riwayat pesan yang berkembang harus di-cache secara otomatis.
- **[Explicit cache breakpoints](#explicit-cache-breakpoints)**: Tempatkan `cache_control` langsung pada blok konten individual untuk kontrol yang lebih halus atas apa yang di-cache.

Cara paling sederhana untuk memulai adalah dengan automatic caching:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
  model: "claude-opus-4-6",
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

```csharp C# hidelines={1..9,-2..}
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
            Model = Model.ClaudeOpus4_6,
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
		Model:        anthropic.ModelClaudeOpus4_6,
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
        .model(Model.CLAUDE_OPUS_4_6)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "Analyze the major themes in 'Pride and Prejudice'."]
    ],
    model: 'claude-opus-4-6',
    cacheControl: CacheControlEphemeral::with(),
    system: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
);
echo json_encode($response->usage);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-6",
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

Dengan automatic caching, sistem mem-cache semua konten hingga dan termasuk blok yang dapat di-cache terakhir. Pada permintaan berikutnya dengan awalan yang sama, konten yang di-cache digunakan kembali secara otomatis.

---

## Cara kerja prompt caching

Ketika Anda mengirim permintaan dengan prompt caching diaktifkan:

1. Sistem memeriksa apakah awalan prompt, hingga breakpoint cache yang ditentukan, sudah di-cache dari kueri baru-baru ini.
2. Jika ditemukan, sistem menggunakan versi yang di-cache, mengurangi waktu pemrosesan dan biaya.
3. Jika tidak, sistem memproses prompt lengkap dan mem-cache awalan setelah respons dimulai.

Ini sangat berguna untuk:
- Prompt dengan banyak contoh
- Jumlah besar konteks atau informasi latar belakang
- Tugas berulang dengan instruksi konsisten
- Percakapan multi-turn yang panjang

Secara default, cache memiliki masa pakai 5 menit. Cache disegarkan tanpa biaya tambahan setiap kali konten yang di-cache digunakan.

<Note>
Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

Untuk informasi lebih lanjut, lihat [durasi cache 1 jam](#1-hour-cache-duration).
</Note>

<Tip>
  **Prompt caching mem-cache awalan penuh**

Prompt caching mereferensikan seluruh prompt - `tools`, `system`, dan `messages` (dalam urutan itu) hingga dan termasuk blok yang ditunjuk dengan `cache_control`.

</Tip>

---

## Harga

Prompt caching memperkenalkan struktur harga baru. Tabel di bawah menunjukkan harga per juta token untuk setiap model yang didukung:

| Model             | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------------------|-------------------|-----------------|-----------------|----------------------|---------------|
| Claude Opus 4.7     | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.6     | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.5   | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.1   | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Opus 4     | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Sonnet 4.6   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4.5   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Haiku 4.5  | $1 / MTok         | $1.25 / MTok    | $2 / MTok       | $0.10 / MTok | $5 / MTok     |
| Claude Haiku 3.5  | $0.80 / MTok      | $1 / MTok       | $1.6 / MTok     | $0.08 / MTok | $4 / MTok     |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))    | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Haiku 3    | $0.25 / MTok      | $0.30 / MTok    | $0.50 / MTok    | $0.03 / MTok | $1.25 / MTok  |

<Note>
Tabel di atas mencerminkan pengganda harga berikut untuk prompt caching:
- Token penulisan cache 5 menit adalah 1,25 kali harga token input dasar
- Token penulisan cache 1 jam adalah 2 kali harga token input dasar
- Token pembacaan cache adalah 0,1 kali harga token input dasar

Pengganda ini ditumpuk dengan pengubah harga lainnya seperti diskon Batch API dan residensi data. Lihat [pricing](/docs/id/about-claude/pricing) untuk detail lengkap.
</Note>

---

## Model yang didukung

Prompt caching (baik automatic maupun explicit) didukung pada semua [model Claude aktif](/docs/id/about-claude/models/overview).

---

## Automatic caching

Automatic caching adalah cara paling sederhana untuk mengaktifkan prompt caching. Alih-alih menempatkan `cache_control` pada blok konten individual, tambahkan satu bidang `cache_control` di tingkat atas badan permintaan Anda. Sistem secara otomatis menerapkan breakpoint cache ke blok yang dapat di-cache terakhir.

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
  model: "claude-opus-4-6",
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

```csharp C# hidelines={1..9,-2..}
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
            Model = Model.ClaudeOpus4_6,
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
		Model:        anthropic.ModelClaudeOpus4_6,
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
                .model(Model.CLAUDE_OPUS_4_6)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'My name is Alex. I work on machine learning.'],
        ['role' => 'assistant', 'content' => 'Nice to meet you, Alex! How can I help with your ML work today?'],
        ['role' => 'user', 'content' => 'What did I say I work on?'],
    ],
    model: 'claude-opus-4-6',
    cacheControl: CacheControlEphemeral::with(),
    system: 'You are a helpful assistant that remembers our conversation.',
);
echo json_encode($response->usage);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-opus-4-6",
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

### Cara kerja automatic caching dalam percakapan multi-turn

Dengan automatic caching, titik cache bergerak maju secara otomatis seiring percakapan berkembang. Setiap permintaan baru mem-cache semuanya hingga blok yang dapat di-cache terakhir, dan konten sebelumnya dibaca dari cache.

| Permintaan | Konten | Perilaku Cache |
|---------|---------|----------------|
| Permintaan 1 | Sistem <br/> + User(1) + Asst(1) <br/> + **User(2)** ◀ cache | Semuanya ditulis ke cache |
| Permintaan 2 | Sistem <br/> + User(1) + Asst(1) <br/> + User(2) + Asst(2) <br/> + **User(3)** ◀ cache | Sistem melalui User(2) dibaca dari cache; <br/> Asst(2) + User(3) ditulis ke cache |
| Permintaan 3 | Sistem <br/> + User(1) + Asst(1) <br/> + User(2) + Asst(2) <br/> + User(3) + Asst(3) <br/> + **User(4)** ◀ cache | Sistem melalui User(3) dibaca dari cache; <br/> Asst(3) + User(4) ditulis ke cache |

Breakpoint cache secara otomatis bergerak ke blok yang dapat di-cache terakhir dalam setiap permintaan, jadi Anda tidak perlu memperbarui penanda `cache_control` apa pun seiring percakapan berkembang.

### Dukungan TTL

Secara default, automatic caching menggunakan TTL 5 menit. Anda dapat menentukan TTL 1 jam dengan harga 2x token input dasar:

```json
{ "cache_control": { "type": "ephemeral", "ttl": "1h" } }
```

### Menggabungkan dengan caching tingkat blok

Automatic caching kompatibel dengan [explicit cache breakpoints](#explicit-cache-breakpoints). Ketika digunakan bersama, breakpoint cache otomatis menggunakan salah satu dari 4 slot breakpoint yang tersedia.

Ini memungkinkan Anda menggabungkan kedua pendekatan. Misalnya, gunakan breakpoint eksplisit untuk mem-cache prompt sistem dan alat Anda secara independen, sementara automatic caching menangani percakapan:

```json
{
  "model": "claude-opus-4-6",
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

### Apa yang tetap sama

Automatic caching menggunakan infrastruktur caching yang sama. Harga, ambang token minimum, persyaratan pengurutan konteks, dan jendela lookback 20-blok semuanya berlaku sama seperti dengan breakpoint eksplisit.

### Kasus tepi

- Jika blok terakhir sudah memiliki `cache_control` eksplisit dengan TTL yang sama, automatic caching adalah no-op.
- Jika blok terakhir memiliki `cache_control` eksplisit dengan TTL yang berbeda, API mengembalikan kesalahan 400.
- Jika 4 breakpoint tingkat blok eksplisit sudah ada, API mengembalikan kesalahan 400 (tidak ada slot tersisa untuk automatic caching).
- Jika blok terakhir tidak memenuhi syarat sebagai target breakpoint cache otomatis, sistem diam-diam berjalan mundur untuk menemukan blok yang memenuhi syarat terdekat. Jika tidak ada yang ditemukan, caching dilewati.

<Note>
Automatic caching tersedia di Claude API dan Azure AI Foundry (preview). Dukungan untuk Amazon Bedrock dan Google Vertex AI akan datang kemudian.
</Note>

---

## Explicit cache breakpoints

Untuk kontrol lebih besar atas caching, Anda dapat menempatkan `cache_control` langsung pada blok konten individual. Ini berguna ketika Anda perlu mem-cache bagian berbeda yang berubah pada frekuensi berbeda, atau memerlukan kontrol yang lebih halus atas apa yang di-cache.

### Menyusun prompt Anda

Tempatkan konten statis (definisi alat, instruksi sistem, konteks, contoh) di awal prompt Anda. Tandai akhir konten yang dapat digunakan kembali untuk caching menggunakan parameter `cache_control`.

Awalan cache dibuat dalam urutan berikut: `tools`, `system`, kemudian `messages`. Urutan ini membentuk hierarki di mana setiap level dibangun di atas yang sebelumnya.

#### Cara kerja pemeriksaan awalan otomatis

Anda dapat menggunakan hanya satu breakpoint cache di akhir konten statis Anda, dan sistem akan secara otomatis menemukan awalan terpanjang yang telah ditulis permintaan sebelumnya ke cache. Memahami cara kerjanya membantu Anda mengoptimalkan strategi caching Anda.

**Tiga prinsip inti:**

1. **Cache writes terjadi hanya pada breakpoint Anda.** Menandai blok dengan `cache_control` menulis tepat satu entri cache: hash dari awalan yang berakhir pada blok itu. Sistem tidak menulis entri untuk posisi apa pun sebelumnya. Karena hash bersifat kumulatif, mencakup semuanya hingga dan termasuk breakpoint, mengubah blok apa pun pada atau sebelum breakpoint menghasilkan hash berbeda pada permintaan berikutnya.

2. **Cache reads mencari mundur untuk entri yang ditulis permintaan sebelumnya.** Pada setiap permintaan, sistem menghitung hash awalan pada breakpoint Anda dan memeriksa entri cache yang cocok. Jika tidak ada, sistem berjalan mundur satu blok pada satu waktu, memeriksa apakah hash awalan pada setiap posisi sebelumnya cocok dengan sesuatu yang sudah ada di cache. Sistem mencari penulisan sebelumnya, bukan konten stabil.

3. **Jendela lookback adalah 20 blok.** Sistem memeriksa paling banyak 20 posisi per breakpoint, menghitung breakpoint itu sendiri sebagai yang pertama. Jika sistem tidak menemukan entri yang cocok dalam jendela itu, pemeriksaan berhenti (atau dilanjutkan dari breakpoint eksplisit berikutnya, jika ada).

**Contoh: Lookback dalam percakapan yang berkembang**

Anda menambahkan blok baru setiap giliran dan menetapkan `cache_control` pada blok terakhir setiap permintaan:

- **Giliran 1:** 10 blok, breakpoint pada blok 10. Tidak ada entri cache sebelumnya. Sistem menulis entri pada blok 10.
- **Giliran 2:** 15 blok, breakpoint pada blok 15. Blok 15 tidak memiliki entri, jadi sistem berjalan mundur ke blok 10 dan menemukan entri giliran-1. Cache hit pada blok 10; sistem hanya memproses blok 11 hingga 15 segar dan menulis entri baru pada blok 15.
- **Giliran 3:** 35 blok, breakpoint pada blok 35. Sistem memeriksa 20 posisi (blok 35 hingga 16) dan tidak menemukan apa pun. Entri giliran-2 pada blok 15 adalah satu posisi di luar jendela, jadi tidak ada cache hit. Menambahkan breakpoint kedua pada blok 15 memulai jendela lookback kedua di sana, yang menemukan entri giliran-2.

**Kesalahan umum: Breakpoint pada konten yang berubah setiap permintaan**

Prompt Anda memiliki konteks sistem statis besar (blok 1 hingga 5) diikuti oleh blok per-permintaan yang berisi stempel waktu dan pesan pengguna (blok 6). Anda menetapkan `cache_control` pada blok 6:

- **Permintaan 1:** Cache write pada blok 6. Hash mencakup stempel waktu.
- **Permintaan 2:** Stempel waktu berbeda, jadi hash awalan pada blok 6 berbeda. Lookback berjalan melalui blok 5, 4, 3, 2, dan 1, tetapi sistem tidak pernah menulis entri pada posisi apa pun. Tidak ada cache hit. Anda membayar untuk cache write segar pada setiap permintaan dan tidak pernah mendapatkan pembacaan.

Lookback tidak menemukan konten stabil di belakang breakpoint Anda dan mem-cachenya. Lookback menemukan entri yang telah ditulis permintaan sebelumnya, dan penulisan hanya terjadi pada breakpoint. Pindahkan `cache_control` ke blok 5, blok terakhir yang tetap sama di seluruh permintaan, dan setiap permintaan berikutnya membaca awalan yang di-cache. [Automatic caching](#automatic-caching) mengalami perangkap yang sama: menempatkan breakpoint pada blok yang dapat di-cache terakhir, yang dalam struktur ini adalah yang berubah setiap permintaan, jadi gunakan breakpoint eksplisit pada blok 5 sebagai gantinya.

**Takeaway kunci:** Tempatkan `cache_control` pada blok terakhir yang awalannya identik di seluruh permintaan yang ingin Anda bagikan cache. Dalam percakapan yang berkembang, blok terakhir berfungsi selama setiap giliran menambahkan lebih sedikit dari 20 blok: konten sebelumnya tidak pernah berubah, jadi lookback permintaan berikutnya menemukan penulisan sebelumnya. Untuk prompt dengan akhiran yang bervariasi (stempel waktu, konteks per-permintaan, pesan masuk), tempatkan breakpoint di akhir awalan statis, bukan pada blok yang bervariasi.

#### Kapan menggunakan beberapa breakpoint

Anda dapat menentukan hingga 4 breakpoint cache jika Anda ingin:
- Mem-cache bagian berbeda yang berubah pada frekuensi berbeda (misalnya, alat jarang berubah, tetapi konteks diperbarui setiap hari)
- Memiliki kontrol lebih besar atas apa yang di-cache
- Memastikan cache hit ketika percakapan yang berkembang mendorong breakpoint Anda 20 atau lebih blok melampaui penulisan cache terakhir

<Note>
**Batasan penting:** Lookback hanya dapat menemukan entri yang telah ditulis permintaan sebelumnya. Jika percakapan yang berkembang mendorong breakpoint Anda 20 atau lebih blok melampaui penulisan terakhir, jendela lookback melewatkannya. Tambahkan breakpoint kedua lebih dekat ke posisi itu dari awal sehingga penulisan terakumulasi di sana sebelum Anda membutuhkannya.
</Note>

### Memahami biaya breakpoint cache

**Breakpoint cache itu sendiri tidak menambah biaya apa pun.** Anda hanya dikenakan biaya untuk:
- **Cache writes**: Ketika konten baru ditulis ke cache (25% lebih banyak dari token input dasar untuk TTL 5 menit)
- **Cache reads**: Ketika konten yang di-cache digunakan (10% dari harga token input dasar)
- **Token input reguler**: Untuk konten yang tidak di-cache apa pun

Menambahkan lebih banyak breakpoint `cache_control` tidak meningkatkan biaya Anda - Anda masih membayar jumlah yang sama berdasarkan konten apa yang benar-benar di-cache dan dibaca. Breakpoint hanya memberi Anda kontrol atas bagian mana yang dapat di-cache secara independen.

---

## Strategi caching dan pertimbangan

### Batasan cache
Panjang prompt yang dapat di-cache minimum adalah:
- 4096 token untuk [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.6, dan Claude Opus 4.5
- 2048 token untuk Claude Sonnet 4.6
- 1024 token untuk Claude Sonnet 4.5, Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4, dan Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))
- 4096 token untuk Claude Haiku 4.5
- 2048 token untuk Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations)) dan Claude Haiku 3

Prompt yang lebih pendek tidak dapat di-cache, bahkan jika ditandai dengan `cache_control`. Permintaan apa pun untuk mem-cache lebih sedikit dari jumlah token ini akan diproses tanpa caching, dan tidak ada kesalahan yang dikembalikan. Untuk memverifikasi apakah prompt di-cache, periksa bidang penggunaan respons [fields](/docs/id/build-with-claude/prompt-caching#tracking-cache-performance): jika `cache_creation_input_tokens` dan `cache_read_input_tokens` keduanya 0, prompt tidak di-cache (kemungkinan karena tidak memenuhi persyaratan panjang minimum).

Jika prompt Anda jatuh sedikit di bawah minimum untuk model yang Anda gunakan, memperluas konten yang di-cache untuk mencapai ambang batas sering kali bermanfaat. Cache reads biaya jauh lebih sedikit daripada token input yang tidak di-cache, jadi mencapai minimum dapat mengurangi biaya untuk prompt yang sering digunakan kembali.

Untuk permintaan bersamaan, perhatikan bahwa entri cache hanya tersedia setelah respons pertama dimulai. Jika Anda memerlukan cache hits untuk permintaan paralel, tunggu respons pertama sebelum mengirim permintaan berikutnya.

Saat ini, "ephemeral" adalah satu-satunya jenis cache yang didukung, yang secara default memiliki masa pakai 5 menit.

### Apa yang dapat di-cache
Sebagian besar blok dalam permintaan dapat di-cache. Ini termasuk:

- Tools: Definisi alat dalam array `tools`
- Pesan sistem: Blok konten dalam array `system`
- Pesan teks: Blok konten dalam array `messages.content`, untuk giliran pengguna dan asisten
- Gambar & Dokumen: Blok konten dalam array `messages.content`, dalam giliran pengguna
- Penggunaan alat dan hasil alat: Blok konten dalam array `messages.content`, dalam giliran pengguna dan asisten

Setiap elemen ini dapat di-cache, baik secara otomatis maupun dengan menandainya dengan `cache_control`.

### Apa yang tidak dapat di-cache
Meskipun sebagian besar blok permintaan dapat di-cache, ada beberapa pengecualian:

- Blok thinking tidak dapat di-cache langsung dengan `cache_control`. Namun, blok thinking DAPAT di-cache bersama konten lain ketika muncul dalam giliran asisten sebelumnya. Ketika di-cache dengan cara ini, mereka MELAKUKAN perhitungan sebagai token input ketika dibaca dari cache.
- Blok sub-konten (seperti [citations](/docs/id/build-with-claude/citations)) itu sendiri tidak dapat di-cache langsung. Sebaliknya, cache blok tingkat atas.

    Dalam kasus kutipan, blok konten dokumen tingkat atas yang berfungsi sebagai materi sumber untuk kutipan dapat di-cache. Ini memungkinkan Anda menggunakan prompt caching dengan kutipan secara efektif dengan mem-cache dokumen yang akan direferensikan kutipan.
- Blok teks kosong tidak dapat di-cache.

### Apa yang membatalkan cache

Modifikasi konten yang di-cache dapat membatalkan beberapa atau semua cache.

Seperti dijelaskan dalam [Menyusun prompt Anda](#structuring-your-prompt), cache mengikuti hierarki: `tools` → `system` → `messages`. Perubahan pada setiap level membatalkan level itu dan semua level berikutnya.

Tabel berikut menunjukkan bagian cache mana yang dibatalkan oleh berbagai jenis perubahan. ✘ menunjukkan bahwa cache dibatalkan, sementara ✓ menunjukkan bahwa cache tetap valid.

| Apa yang berubah | Cache Tools | Cache Sistem | Cache Pesan | Dampak |
|------------|------------------|---------------|----------------|-------------|
| **Definisi alat** | ✘ | ✘ | ✘ | Memodifikasi definisi alat (nama, deskripsi, parameter) membatalkan seluruh cache |
| **Toggle pencarian web** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan pencarian web memodifikasi prompt sistem |
| **Toggle kutipan** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan kutipan memodifikasi prompt sistem |
| **Pengaturan kecepatan** | ✓ | ✘ | ✘ | Beralih antara [`speed: "fast"` dan kecepatan standar](/docs/id/build-with-claude/fast-mode) membatalkan cache sistem dan pesan |
| **Pilihan alat** | ✓ | ✓ | ✘ | Perubahan pada parameter `tool_choice` hanya mempengaruhi blok pesan |
| **Gambar** | ✓ | ✓ | ✘ | Menambahkan/menghapus gambar di mana pun dalam prompt mempengaruhi blok pesan |
| **Parameter thinking** | ✓ | ✓ | ✘ | Perubahan pada pengaturan extended thinking (aktifkan/nonaktifkan, anggaran) mempengaruhi blok pesan |
| **Hasil non-alat yang dilewatkan ke permintaan extended thinking** | ✓ | ✓ | ✘ | Ketika hasil non-alat dilewatkan dalam permintaan sementara extended thinking diaktifkan, semua blok thinking yang di-cache sebelumnya dilepas dari konteks, dan pesan apa pun dalam konteks yang mengikuti blok thinking itu dihapus dari cache. Untuk detail lebih lanjut, lihat [Caching dengan thinking blocks](#caching-with-thinking-blocks). |

### Melacak kinerja cache

Pantau kinerja cache menggunakan bidang respons API ini, dalam `usage` dalam respons (atau acara `message_start` jika [streaming](/docs/id/build-with-claude/streaming)):

- `cache_creation_input_tokens`: Jumlah token yang ditulis ke cache saat membuat entri baru.
- `cache_read_input_tokens`: Jumlah token yang diambil dari cache untuk permintaan ini.
- `input_tokens`: Jumlah token input yang tidak dibaca dari atau digunakan untuk membuat cache (yaitu, token setelah breakpoint cache terakhir).

<Note>
**Memahami rincian token**

Bidang `input_tokens` mewakili hanya token yang datang **setelah breakpoint cache terakhir** dalam permintaan Anda - bukan semua token input yang Anda kirim.

Untuk menghitung total token input:
```text
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

**Penjelasan spasial:**
- `cache_read_input_tokens` = token sebelum breakpoint sudah di-cache (pembacaan)
- `cache_creation_input_tokens` = token sebelum breakpoint sedang di-cache sekarang (penulisan)
- `input_tokens` = token setelah breakpoint terakhir Anda (tidak memenuhi syarat untuk cache)

**Contoh:** Jika Anda memiliki permintaan dengan 100.000 token konten yang di-cache (dibaca dari cache), 0 token konten baru yang di-cache, dan 50 token dalam pesan pengguna Anda (setelah breakpoint cache):
- `cache_read_input_tokens`: 100.000
- `cache_creation_input_tokens`: 0
- `input_tokens`: 50
- **Total token input yang diproses**: 100.050 token

Ini penting untuk memahami biaya dan batas laju, karena `input_tokens` biasanya akan jauh lebih kecil dari total input Anda saat menggunakan caching secara efektif.
</Note>

### Caching dengan thinking blocks

Saat menggunakan [extended thinking](/docs/id/build-with-claude/extended-thinking) dengan prompt caching, thinking blocks memiliki perilaku khusus:

**Automatic caching bersama konten lainnya**: Meskipun thinking blocks tidak dapat secara eksplisit ditandai dengan `cache_control`, mereka di-cache sebagai bagian dari konten permintaan ketika Anda membuat panggilan API berikutnya dengan hasil tool. Ini biasanya terjadi selama penggunaan tool ketika Anda melewatkan thinking blocks kembali untuk melanjutkan percakapan.

**Input token counting**: Ketika thinking blocks dibaca dari cache, mereka dihitung sebagai input tokens dalam metrik penggunaan Anda. Ini penting untuk perhitungan biaya dan anggaran token.

**Cache invalidation patterns**:
- Cache tetap valid ketika hanya hasil tool yang disediakan sebagai pesan pengguna
- Cache menjadi tidak valid ketika konten pengguna non-tool-result ditambahkan, menyebabkan semua thinking blocks sebelumnya dihapus
- Perilaku caching ini terjadi bahkan tanpa penanda `cache_control` eksplisit

Untuk detail lebih lanjut tentang cache invalidation, lihat [What invalidates the cache](#what-invalidates-the-cache).

**Contoh dengan tool use**:
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
# Non-tool-result user block causes all thinking blocks to be ignored
# This request is processed as if thinking blocks were never present
```

Ketika blok pengguna non-tool-result disertakan, itu menunjuk loop asisten baru dan semua thinking blocks sebelumnya dihapus dari konteks.

Untuk informasi lebih detail, lihat [dokumentasi extended thinking](/docs/id/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior).

### Cache storage and sharing

<Warning>
Mulai 5 Februari 2026, prompt caching akan menggunakan isolasi tingkat workspace alih-alih isolasi tingkat organisasi. Cache akan diisolasi per workspace, memastikan pemisahan data antara workspace dalam organisasi yang sama. Perubahan ini berlaku untuk Claude API dan Azure AI Foundry (preview); Amazon Bedrock dan Google Vertex AI akan mempertahankan isolasi cache tingkat organisasi. Jika Anda menggunakan beberapa workspace, tinjau strategi caching Anda untuk memperhitungkan perubahan ini.
</Warning>

- **Organization Isolation**: Cache diisolasi antara organisasi. Organisasi yang berbeda tidak pernah berbagi cache, bahkan jika mereka menggunakan prompt yang identik.

- **Exact Matching**: Cache hits memerlukan segmen prompt yang 100% identik, termasuk semua teks dan gambar hingga dan termasuk blok yang ditandai dengan cache control.

- **Output Token Generation**: Prompt caching tidak memiliki efek pada pembuatan output token. Respons yang Anda terima akan identik dengan apa yang akan Anda dapatkan jika prompt caching tidak digunakan.

### Best practices untuk effective caching

Untuk mengoptimalkan kinerja prompt caching:

- Mulai dengan [automatic caching](#automatic-caching) untuk percakapan multi-turn. Ini menangani manajemen breakpoint secara otomatis.
- Gunakan [explicit block-level breakpoints](#explicit-cache-breakpoints) ketika Anda perlu cache bagian berbeda dengan frekuensi perubahan yang berbeda.
- Cache konten stabil dan dapat digunakan kembali seperti instruksi sistem, informasi latar belakang, konteks besar, atau definisi tool yang sering digunakan.
- Tempatkan konten cache di awal prompt untuk kinerja terbaik.
- Gunakan cache breakpoints secara strategis untuk memisahkan bagian prefix yang dapat di-cache berbeda.
- Tempatkan breakpoint pada blok terakhir yang tetap identik di seluruh permintaan. Untuk prompt dengan prefix statis dan suffix yang bervariasi (timestamps, konteks per-permintaan, pesan masuk), itu adalah akhir dari prefix, bukan blok yang bervariasi.
- Secara teratur analisis cache hit rates dan sesuaikan strategi Anda sesuai kebutuhan.

### Optimizing untuk different use cases

Sesuaikan strategi prompt caching Anda dengan skenario Anda:

- Conversational agents: Kurangi biaya dan latensi untuk percakapan yang diperpanjang, terutama yang memiliki instruksi panjang atau dokumen yang diunggah.
- Coding assistants: Tingkatkan autocomplete dan codebase Q&A dengan menjaga bagian relevan atau versi ringkasan codebase dalam prompt.
- Large document processing: Gabungkan materi bentuk panjang lengkap termasuk gambar dalam prompt Anda tanpa meningkatkan latensi respons.
- Detailed instruction sets: Bagikan daftar instruksi, prosedur, dan contoh yang luas untuk menyempurnakan respons Claude. Developer sering menyertakan satu atau dua contoh dalam prompt, tetapi dengan prompt caching Anda dapat mendapatkan kinerja yang lebih baik dengan menyertakan 20+ contoh beragam jawaban berkualitas tinggi.
- Agentic tool use: Tingkatkan kinerja untuk skenario yang melibatkan beberapa panggilan tool dan perubahan kode iteratif, di mana setiap langkah biasanya memerlukan panggilan API baru.
- Talk to books, papers, documentation, podcast transcripts, dan konten longform lainnya: Hidupkan basis pengetahuan apa pun dengan menyematkan seluruh dokumen ke dalam prompt, dan membiarkan pengguna mengajukan pertanyaan padanya.

### Troubleshooting common issues

Jika mengalami perilaku yang tidak terduga:

- Pastikan bagian cache identik di seluruh panggilan. Untuk breakpoint eksplisit, verifikasi bahwa penanda `cache_control` berada di lokasi yang sama
- Periksa bahwa panggilan dilakukan dalam cache lifetime (5 menit secara default)
- Verifikasi bahwa `tool_choice` dan penggunaan gambar tetap konsisten antara panggilan
- Validasi bahwa Anda melakukan cache setidaknya jumlah token minimum untuk model yang Anda gunakan (lihat [Cache limitations](#cache-limitations)). Kegagalan caching berbasis panjang bersifat senyap: permintaan berhasil tetapi `cache_creation_input_tokens` dan `cache_read_input_tokens` akan menjadi 0
- Konfirmasi breakpoint Anda berada pada blok yang tetap identik di seluruh permintaan. Cache writes terjadi hanya pada breakpoint, dan jika blok itu berubah (timestamps, konteks per-permintaan, pesan masuk), hash prefix tidak pernah cocok. Lookback tidak menemukan konten stabil di belakang breakpoint; itu hanya menemukan entri yang diminta sebelumnya ditulis pada breakpoint mereka sendiri
- Verifikasi bahwa kunci dalam blok konten `tool_use` Anda memiliki urutan yang stabil karena beberapa bahasa (misalnya, Swift, Go) mengacakkan urutan kunci selama konversi JSON, merusak cache

<Note>
Perubahan pada `tool_choice` atau kehadiran/ketiadaan gambar di mana pun dalam prompt akan membatalkan cache, memerlukan entri cache baru untuk dibuat. Untuk detail lebih lanjut tentang cache invalidation, lihat [What invalidates the cache](#what-invalidates-the-cache).
</Note>

---
## 1-hour cache duration

Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

Untuk menggunakan cache yang diperpanjang, sertakan `ttl` dalam definisi `cache_control` seperti ini:
```json hidelines={1,-1}
{
  "cache_control": {
    "type": "ephemeral",
    "ttl": "1h"
  }
}
```

Respons akan mencakup informasi cache terperinci seperti berikut:
```json Output
{
  "usage": {
    "input_tokens": 2048,
    "cache_read_input_tokens": 1800,
    "cache_creation_input_tokens": 248,
    "output_tokens": 503,

    "cache_creation": {
      "ephemeral_5m_input_tokens": 456,
      "ephemeral_1h_input_tokens": 100
    }
  }
}
```

Perhatikan bahwa field `cache_creation_input_tokens` saat ini sama dengan jumlah nilai dalam objek `cache_creation`.

### When to use the 1-hour cache

Jika Anda memiliki prompt yang digunakan dengan ritme teratur (yaitu, prompt sistem yang digunakan lebih sering dari setiap 5 menit), terus gunakan cache 5 menit, karena ini akan terus disegarkan tanpa biaya tambahan.

Cache 1 jam paling baik digunakan dalam skenario berikut:
- Ketika Anda memiliki prompt yang kemungkinan digunakan kurang sering dari 5 menit, tetapi lebih sering dari setiap jam. Misalnya, ketika side-agent agentic akan memakan waktu lebih dari 5 menit, atau ketika menyimpan percakapan obrolan panjang dengan pengguna dan Anda umumnya mengharapkan bahwa pengguna mungkin tidak merespons dalam 5 menit berikutnya.
- Ketika latensi penting dan prompt tindak lanjut Anda dapat dikirim di luar 5 menit.
- Ketika Anda ingin meningkatkan utilisasi rate limit Anda, karena cache hits tidak dikurangkan terhadap rate limit Anda.

<Note>
Cache 5 menit dan 1 jam berperilaku sama sehubungan dengan latensi. Anda umumnya akan melihat waktu-ke-token-pertama yang ditingkatkan untuk dokumen panjang.
</Note>

### Mixing different TTLs

Anda dapat menggunakan kontrol cache 1 jam dan 5 menit dalam permintaan yang sama, tetapi dengan batasan penting: Entri cache dengan TTL lebih lama harus muncul sebelum TTL lebih pendek (yaitu, entri cache 1 jam harus muncul sebelum entri cache 5 menit apa pun).

Saat mencampur TTL, API menentukan tiga lokasi penagihan dalam prompt Anda:
1. Position `A`: Jumlah token pada cache hit tertinggi (atau 0 jika tidak ada hits).
2. Position `B`: Jumlah token pada blok `cache_control` 1 jam tertinggi setelah `A` (atau sama dengan `A` jika tidak ada).
3. Position `C`: Jumlah token pada blok `cache_control` terakhir.

<Note>
Jika `B` dan/atau `C` lebih besar dari `A`, mereka harus menjadi cache misses, karena `A` adalah cache hit tertinggi.
</Note>

Anda akan dikenakan biaya untuk:
1. Cache read tokens untuk `A`.
2. 1-hour cache write tokens untuk `(B - A)`.
3. 5-minute cache write tokens untuk `(C - B)`.

Berikut adalah 3 contoh. Ini menggambarkan input tokens dari 3 permintaan, masing-masing memiliki cache hits dan cache misses yang berbeda. Masing-masing memiliki penagihan yang dihitung berbeda, ditunjukkan dalam kotak berwarna, sebagai hasilnya.
![Mixing TTLs Diagram](/docs/images/prompt-cache-mixed-ttl.svg)

---

## Contoh prompt caching

Untuk membantu Anda memulai dengan prompt caching, [prompt caching cookbook](https://platform.claude.com/cookbook/misc-prompt-caching) menyediakan contoh terperinci dan praktik terbaik.

Cuplikan kode berikut menampilkan berbagai pola prompt caching. Contoh-contoh ini menunjukkan cara mengimplementasikan caching dalam skenario berbeda, membantu Anda memahami aplikasi praktis dari fitur ini:

<section title="Contoh caching konteks besar">

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
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
print(response.model_dump_json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
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

```csharp C# hidelines={1..10,-2..}
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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
	fmt.Printf("%+v\n", response)
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
      .model(Model.CLAUDE_OPUS_4_6)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => 'What are the key terms and conditions in this agreement?'
        ]
    ],
    model: 'claude-opus-4-6',
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
  model: "claude-opus-4-6",
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
Contoh ini menunjukkan penggunaan prompt caching dasar, melakukan caching pada teks lengkap perjanjian hukum sebagai awalan sambil menjaga instruksi pengguna tidak di-cache.

Untuk permintaan pertama:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: Jumlah token dalam seluruh pesan sistem, termasuk dokumen hukum
- `cache_read_input_tokens`: 0 (tidak ada cache hit pada permintaan pertama)

Untuk permintaan berikutnya dalam masa hidup cache:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: 0 (tidak ada pembuatan cache baru)
- `cache_read_input_tokens`: Jumlah token dalam seluruh pesan sistem yang di-cache

</section>

<section title="Caching definisi alat">

Definisi alat dapat di-cache dengan menempatkan `cache_control` pada alat terakhir dalam array `tools` Anda. Semua alat yang didefinisikan sebelum dan termasuk alat tersebut di-cache sebagai satu awalan.

```json
{
  "model": "claude-opus-4-6",
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

Pada permintaan pertama, `cache_creation_input_tokens` mencerminkan jumlah token dari semua definisi alat. Pada permintaan berikutnya dalam masa hidup cache, token-token tersebut muncul di bawah `cache_read_input_tokens` sebagai gantinya.

Untuk interaksi terperinci antara definisi alat, `defer_loading`, dan invalidasi cache, lihat [Tool use with prompt caching](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

</section>

<section title="Melanjutkan percakapan multi-turn">

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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
    model="claude-opus-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        # ...long conversation so far
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
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "...long system prompt",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    // ...long conversation so far
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
    Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

    // Create ephemeral system prompt
    TextBlockParam systemPrompt = TextBlockParam.builder()
      .text("...long system prompt")
      .cacheControl(CacheControlEphemeral.builder().build())
      .build();

    // Create message params
    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      .systemOfTextBlockParams(List.of(systemPrompt))
      // First user message (without cache control)
      .addUserMessage("Hello, can you tell me more about the solar system?")
      // Assistant response
      .addAssistantMessage(
        "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
      )
      // Second user message (with cache control)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
    model: 'claude-opus-4-6',
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
  model: "claude-opus-4-6",
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

Contoh ini menunjukkan cara menggunakan prompt caching dalam percakapan multi-turn.

Selama setiap giliran, blok terakhir dari pesan terakhir ditandai dengan `cache_control` sehingga percakapan dapat di-cache secara bertahap. Sistem akan secara otomatis mencari dan menggunakan urutan blok yang paling lama di-cache sebelumnya untuk pesan lanjutan. Artinya, blok yang sebelumnya ditandai dengan blok `cache_control` kemudian tidak ditandai dengan ini, tetapi mereka masih akan dianggap sebagai cache hit (dan juga cache refresh!) jika mereka terkena dalam 5 menit.

Selain itu, perhatikan bahwa parameter `cache_control` ditempatkan pada pesan sistem. Ini untuk memastikan bahwa jika ini dihapus dari cache (setelah tidak digunakan selama lebih dari 5 menit), itu akan ditambahkan kembali ke cache pada permintaan berikutnya.

Pendekatan ini berguna untuk mempertahankan konteks dalam percakapan yang sedang berlangsung tanpa berulang kali memproses informasi yang sama.

Ketika ini diatur dengan benar, Anda harus melihat hal berikut dalam respons penggunaan setiap permintaan:
- `input_tokens`: Jumlah token dalam pesan pengguna baru (akan minimal)
- `cache_creation_input_tokens`: Jumlah token dalam giliran asisten dan pengguna baru
- `cache_read_input_tokens`: Jumlah token dalam percakapan hingga giliran sebelumnya

</section>

<section title="Menyatukannya semua: Beberapa titik henti cache">

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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

      # Instructions
      - Always search for relevant documents before answering
      - Provide citations for your sources
      - Be objective and accurate in your responses
      - If multiple documents contain relevant information, synthesize them
      - Acknowledge when information is not available in the knowledge base
    cache_control:
      type: ephemeral
  - type: text
    text: |-
      # Knowledge Base Context

      Here are the relevant documents for this conversation:

      ## Document 1: Solar System Overview
      The solar system consists of the Sun and all objects that orbit it...

      ## Document 2: Planetary Characteristics
      Each planet has unique features. Mercury is the smallest planet...

      ## Document 3: Mars Exploration
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
    model="claude-opus-4-6",
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
  model: "claude-opus-4-6",
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

```csharp C# hidelines={1..11,-2..}
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

    // Search tool schema
    InputSchema searchSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("query", Map.of("type", "string", "description", "Search query"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("query")))
      .build();

    // Get document tool schema
    InputSchema getDocSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("doc_id", Map.of("type", "string", "description", "Document ID"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("doc_id")))
      .build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      // Tools with cache control on the last one
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
      // System prompts with cache control on instructions and context separately
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
      // Conversation history
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
    model: 'claude-opus-4-6',
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

echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
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

Contoh komprehensif ini menunjukkan cara menggunakan semua 4 titik henti cache yang tersedia untuk mengoptimalkan bagian berbeda dari prompt Anda:

1. **Cache alat** (titik henti cache 1): Parameter `cache_control` pada definisi alat terakhir melakukan cache pada semua definisi alat.

2. **Cache instruksi yang dapat digunakan kembali** (titik henti cache 2): Instruksi statis dalam prompt sistem di-cache secara terpisah. Instruksi-instruksi ini jarang berubah antar permintaan.

3. **Cache konteks RAG** (titik henti cache 3): Dokumen basis pengetahuan di-cache secara independen, memungkinkan Anda memperbarui dokumen RAG tanpa membatalkan cache alat atau instruksi.

4. **Cache riwayat percakapan** (titik henti cache 4): Respons asisten ditandai dengan `cache_control` untuk mengaktifkan caching bertahap dari percakapan saat berkembang.

Pendekatan ini memberikan fleksibilitas maksimal:
- Jika Anda hanya memperbarui pesan pengguna terakhir, semua empat segmen cache digunakan kembali
- Jika Anda memperbarui dokumen RAG tetapi menjaga alat dan instruksi yang sama, dua segmen cache pertama digunakan kembali
- Jika Anda mengubah percakapan tetapi menjaga alat, instruksi, dan dokumen yang sama, tiga segmen pertama digunakan kembali
- Setiap titik henti cache dapat dibatalkan secara independen berdasarkan apa yang berubah dalam aplikasi Anda

Untuk permintaan pertama:
- `input_tokens`: Token dalam pesan pengguna terakhir
- `cache_creation_input_tokens`: Token dalam semua segmen yang di-cache (alat + instruksi + dokumen RAG + riwayat percakapan)
- `cache_read_input_tokens`: 0 (tidak ada cache hit)

Untuk permintaan berikutnya dengan hanya pesan pengguna baru:
- `input_tokens`: Token dalam pesan pengguna baru saja
- `cache_creation_input_tokens`: Token baru apa pun yang ditambahkan ke riwayat percakapan
- `cache_read_input_tokens`: Semua token yang sebelumnya di-cache (alat + instruksi + dokumen RAG + percakapan sebelumnya)

Pola ini sangat kuat untuk:
- Aplikasi RAG dengan konteks dokumen besar
- Sistem agen yang menggunakan beberapa alat
- Percakapan yang berjalan lama yang perlu mempertahankan konteks
- Aplikasi yang perlu mengoptimalkan bagian berbeda dari prompt secara independen

</section>

## Retensi data

Prompt caching (baik otomatis maupun eksplisit) memenuhi syarat ZDR. Anthropic tidak menyimpan teks mentah dari prompt Anda atau respons Claude.

Representasi cache KV (key-value) dan hash kriptografi dari konten yang di-cache disimpan hanya dalam memori dan tidak disimpan saat istirahat. Entri cache memiliki masa hidup minimum 5 menit (standar) atau 60 menit (diperpanjang), setelah itu akan segera, meskipun tidak langsung, dihapus. Entri cache terisolasi antar organisasi.

Untuk kelayakan ZDR di semua fitur, lihat [API and data retention](/docs/id/build-with-claude/api-and-data-retention).

---
## FAQ

  <section title="Apakah saya memerlukan beberapa titik cache breakpoint atau satu di akhir sudah cukup?">

    **Dalam kebanyakan kasus, satu titik cache breakpoint di akhir konten statis Anda sudah cukup.** Cache writes hanya terjadi pada blok yang Anda tandai. Tempatkan pada blok terakhir yang tetap identik di seluruh permintaan, dan setiap permintaan berikutnya membaca entri yang sama. Jika blok yang lebih baru bervariasi per permintaan (timestamp, pesan masuk), pertahankan breakpoint sebelumnya, pada blok stabil terakhir.

    Anda hanya memerlukan beberapa breakpoint jika:
    - Percakapan yang berkembang mendorong breakpoint Anda 20 atau lebih blok melampaui cache write terakhir, menempatkan entri sebelumnya di luar jendela lookback
    - Anda ingin cache bagian yang diperbarui pada frekuensi berbeda secara independen
    - Anda memerlukan kontrol eksplisit atas apa yang di-cache untuk optimasi biaya

    Contoh: Jika Anda memiliki instruksi sistem (jarang berubah) dan konteks RAG (berubah setiap hari), Anda mungkin menggunakan dua breakpoint untuk cache mereka secara terpisah.
  
</section>

  <section title="Apakah cache breakpoint menambah biaya ekstra?">

    Tidak, cache breakpoint itu sendiri gratis. Anda hanya membayar untuk:
    - Menulis konten ke cache (25% lebih dari token input dasar untuk TTL 5 menit)
    - Membaca dari cache (10% dari harga token input dasar)
    - Token input reguler untuk konten yang tidak di-cache

    Jumlah breakpoint tidak mempengaruhi harga - hanya jumlah konten yang di-cache dan dibaca yang penting.
  
</section>

  <section title="Bagaimana cara menghitung total token input dari bidang penggunaan?">

    Respons penggunaan mencakup tiga bidang token input terpisah yang bersama-sama mewakili total input Anda:

    ```text
    total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
    ```

    - `cache_read_input_tokens`: Token yang diambil dari cache (semua yang sebelum cache breakpoint yang di-cache)
    - `cache_creation_input_tokens`: Token baru yang ditulis ke cache (pada cache breakpoint)
    - `input_tokens`: Token **setelah cache breakpoint terakhir** yang tidak di-cache

    **Penting:** `input_tokens` TIDAK mewakili semua token input - hanya bagian setelah cache breakpoint terakhir Anda. Jika Anda memiliki konten cache, `input_tokens` biasanya akan jauh lebih kecil dari total input Anda.

    **Contoh:** Dengan dokumen 200k token di-cache dan pertanyaan pengguna 50 token:
    - `cache_read_input_tokens`: 200.000
    - `cache_creation_input_tokens`: 0
    - `input_tokens`: 50
    - **Total**: 200.050 token

    Rincian ini sangat penting untuk memahami biaya dan penggunaan batas laju Anda. Lihat [Tracking cache performance](#tracking-cache-performance) untuk detail lebih lanjut.
  
</section>

  <section title="Berapa lama cache berlaku?">

    Masa hidup minimum cache default (TTL) adalah 5 menit. Masa hidup ini diperbarui setiap kali konten cache digunakan.

    Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan [cache TTL 1 jam](#1-hour-cache-duration).
  
</section>

  <section title="Berapa banyak cache breakpoint yang dapat saya gunakan?">

    Anda dapat menentukan hingga 4 cache breakpoint (menggunakan parameter `cache_control`) dalam prompt Anda.
  
</section>

  <section title="Apakah prompt caching tersedia untuk semua model?">

    Prompt caching didukung pada semua [model Claude aktif](/docs/id/about-claude/models/overview).
  
</section>

  <section title="Bagaimana prompt caching bekerja dengan extended thinking?">

    Prompt sistem cache dan alat akan digunakan kembali ketika parameter thinking berubah. Namun, perubahan thinking (mengaktifkan/menonaktifkan atau perubahan anggaran) akan membatalkan prefix prompt cache sebelumnya dengan konten pesan.

    Untuk detail lebih lanjut tentang cache invalidation, lihat [What invalidates the cache](#what-invalidates-the-cache).

    Untuk lebih lanjut tentang extended thinking, termasuk interaksinya dengan tool use dan prompt caching, lihat [dokumentasi extended thinking](/docs/id/build-with-claude/extended-thinking#extended-thinking-and-prompt-caching).
  
</section>

  <section title="Bagaimana cara mengaktifkan prompt caching?">

    Cara termudah adalah menambahkan `"cache_control": {"type": "ephemeral"}` di tingkat atas badan permintaan Anda ([automatic caching](#automatic-caching)). Atau, sertakan setidaknya satu breakpoint `cache_control` pada blok konten individual ([explicit cache breakpoints](#explicit-cache-breakpoints)).
  
</section>

  <section title="Bisakah saya menggunakan prompt caching dengan fitur API lainnya?">

    Ya, prompt caching dapat digunakan bersama fitur API lainnya seperti tool use dan kemampuan vision. Namun, mengubah apakah ada gambar dalam prompt atau memodifikasi pengaturan tool use akan memutus cache.

    Untuk detail lebih lanjut tentang cache invalidation, lihat [What invalidates the cache](#what-invalidates-the-cache).
  
</section>

  <section title="Bagaimana prompt caching mempengaruhi harga?">

    Prompt caching memperkenalkan struktur harga baru di mana cache writes biaya 25% lebih dari token input dasar, sementara cache hits biaya hanya 10% dari harga token input dasar.
  
</section>

  <section title="Bisakah saya menghapus cache secara manual?">

    Saat ini, tidak ada cara untuk menghapus cache secara manual. Prefix cache secara otomatis kedaluwarsa setelah minimum 5 menit tidak aktif.
  
</section>

  <section title="Bagaimana cara melacak efektivitas strategi caching saya?">

    Anda dapat memantau kinerja cache menggunakan bidang `cache_creation_input_tokens` dan `cache_read_input_tokens` dalam respons API.
  
</section>

  <section title="Apa yang dapat memutus cache?">

    Lihat [What invalidates the cache](#what-invalidates-the-cache) untuk detail lebih lanjut tentang cache invalidation, termasuk daftar perubahan yang memerlukan pembuatan entri cache baru.
  
</section>

  <section title="Bagaimana prompt caching menangani privasi dan pemisahan data?">

Prompt caching dirancang dengan langkah-langkah privasi dan pemisahan data yang kuat:

1. Kunci cache dihasilkan menggunakan hash kriptografi dari prompt hingga titik kontrol cache. Ini berarti hanya permintaan dengan prompt identik yang dapat mengakses cache tertentu.

2. Cache khusus organisasi. Pengguna dalam organisasi yang sama dapat mengakses cache yang sama jika mereka menggunakan prompt identik, tetapi cache tidak dibagikan di seluruh organisasi yang berbeda, bahkan untuk prompt identik.

3. Mekanisme caching dirancang untuk mempertahankan integritas dan privasi setiap percakapan atau konteks unik.

4. Aman untuk menggunakan `cache_control` di mana saja dalam prompt Anda. Untuk caching menghasilkan pembacaan, tempatkan breakpoint di akhir prefix stabil: menempatkannya pada blok yang berubah setiap permintaan (seperti timestamp atau input arbitrer pengguna) menulis entri segar setiap kali dan tidak pernah hit.

Langkah-langkah ini memastikan bahwa prompt caching mempertahankan privasi dan keamanan data sambil menawarkan manfaat kinerja.

Catatan: Mulai 5 Februari 2026, cache akan terisolasi per workspace bukan per organisasi. Perubahan ini berlaku untuk Claude API dan Azure AI Foundry (preview). Lihat [Cache storage and sharing](#cache-storage-and-sharing) untuk detail.

  
</section>
  <section title="Bisakah saya menggunakan prompt caching dengan Batches API?">

    Ya, dimungkinkan untuk menggunakan prompt caching dengan permintaan [Batches API](/docs/id/build-with-claude/batch-processing) Anda. Namun, karena permintaan batch asinkron dapat diproses secara bersamaan dan dalam urutan apa pun, cache hits disediakan atas dasar best-effort.

    [Cache 1 jam](#1-hour-cache-duration) dapat membantu meningkatkan cache hits Anda. Cara paling hemat biaya untuk menggunakannya adalah sebagai berikut:
    - Kumpulkan serangkaian permintaan pesan yang memiliki prefix bersama.
    - Kirim permintaan batch dengan hanya satu permintaan yang memiliki prefix bersama ini dan blok cache 1 jam. Ini akan ditulis ke cache 1 jam.
    - Segera setelah selesai, kirimkan sisa permintaan. Anda harus memantau pekerjaan untuk mengetahui kapan selesai.

    Ini biasanya lebih baik daripada menggunakan cache 5 menit hanya karena umum untuk permintaan batch memakan waktu antara 5 menit dan 1 jam untuk diselesaikan. Anthropic sedang mempertimbangkan cara untuk meningkatkan tingkat cache hit ini dan membuat proses ini lebih mudah.
  
</section>
  <section title="Mengapa saya melihat error `AttributeError: 'Beta' object has no attribute 'prompt_caching'` di Python?">

  Error ini biasanya muncul ketika Anda telah meningkatkan SDK atau menggunakan contoh kode yang ketinggalan zaman. Prompt caching sekarang tersedia secara umum, jadi Anda tidak lagi memerlukan prefix beta. Alih-alih:
    <CodeGroup>
      
      ```python Python nocheck
      client.beta.prompt_caching.messages.create(**params)
      ```

      
      ```typescript TypeScript nocheck hidelines={1..2}
      import Anthropic from "@anthropic-ai/sdk";

      const client = new Anthropic();

      const response = await client.beta.promptCaching.messages.create({
        model: "claude-opus-4-6",
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

      $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

      $message = $client->beta->promptCaching->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Summarize the key points']
          ],
          model: 'claude-opus-4-6',
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
    </CodeGroup>
    Cukup gunakan:
    <CodeGroup>
      
      ```python Python nocheck
      client.messages.create(**params)
      ```

      ```typescript TypeScript hidelines={1..2}
      import Anthropic from "@anthropic-ai/sdk";

      const client = new Anthropic();

      const response = await client.messages.create({
        model: "claude-opus-4-6",
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

      $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Summarize the key points']
          ],
          model: 'claude-opus-4-6',
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
        model: "claude-opus-4-6",
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

  Error ini biasanya muncul ketika Anda telah meningkatkan SDK atau menggunakan contoh kode yang ketinggalan zaman. Prompt caching sekarang tersedia secara umum, jadi Anda tidak lagi memerlukan prefix beta. Alih-alih:

      ```typescript TypeScript
      client.beta.promptCaching.messages.create(/* ... */);
      ```

      Cukup gunakan:

      ```typescript
      client.messages.create(/* ... */);
      ```
  
</section>