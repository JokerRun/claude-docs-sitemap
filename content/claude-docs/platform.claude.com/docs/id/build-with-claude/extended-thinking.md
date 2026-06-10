---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 4db7e8c0387776552115d0736e5e2e1bb647b1e90c574f8eba9b69fbbd1634c9
---

# Membangun dengan pemikiran diperpanjang

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Pemikiran diperpanjang memberikan Claude kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, sekaligus menyediakan berbagai tingkat transparansi ke dalam proses pemikiran langkah demi langkahnya sebelum memberikan jawaban akhir.

<Note>
Pada `claude-fable-5` dan `claude-mythos-5`, pemikiran diperpanjang selalu diaktifkan dan tidak dapat dinonaktifkan. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung; gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya. Pemikiran adaptif selalu aktif, dan `thinking: {type: "disabled"}` mengembalikan error.
</Note>

<Note>
Untuk Claude Opus 4.8 dan Claude Opus 4.7, atur `thinking: {type: "adaptive"}` untuk mengaktifkan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Pada kedua model tersebut, pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Dengan pemikiran adaptif, model memutuskan kapan dan seberapa banyak harus berpikir berdasarkan setiap permintaan, sehingga pemikiran hanya dipicu sesuai kebutuhan. Untuk Claude Opus 4.6 dan Claude Sonnet 4.6, pemikiran adaptif juga direkomendasikan; konfigurasi manual masih berfungsi pada model-model ini tetapi sudah tidak digunakan lagi (deprecated) dan akan dihapus pada rilis model mendatang.
</Note>

## Model yang didukung \{#supported-models}

Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) didukung pada semua model Claude saat ini **kecuali Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7**, di mana konfigurasi ini tidak diterima dan mengembalikan error 400. Beberapa model memiliki perilaku khusus mode:

- **Claude Fable 5 (`claude-fable-5`) dan Claude Mythos 5 (`claude-mythos-5`):** pemikiran diperpanjang manual tidak didukung dan mengembalikan error 400. [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) selalu aktif; gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran.
- **Claude Opus 4.8 (claude-opus-4-8):** pemikiran diperpanjang manual tidak didukung dan mengembalikan error 400. Gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya. Model menentukan apakah dan seberapa banyak menggunakan pemikiran diperpanjang berdasarkan setiap permintaan.
- **Claude Opus 4.7 (claude-opus-4-7):** pemikiran diperpanjang manual tidak lagi didukung. Gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya.
- **[Claude Mythos Preview](https://anthropic.com/glasswing):** [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) adalah default; `thinking: {type: "enabled", budget_tokens: N}` juga diterima. `thinking: {type: "disabled"}` tidak didukung, dan `display` secara default bernilai `"omitted"` alih-alih mengembalikan konten pemikiran. Berikan `display: "summarized"` untuk menerima ringkasan.
- **Claude Opus 4.6 (claude-opus-4-6):** [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) direkomendasikan; mode manual (`type: "enabled"`) sudah deprecated tetapi masih berfungsi.
- **Claude Sonnet 4.6 (claude-sonnet-4-6):** [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) direkomendasikan; mode manual (`type: "enabled"`) dengan [mode interleaved](#interleaved-thinking) sudah deprecated tetapi masih berfungsi.

<Note>
Perilaku pemikiran berbeda di antara versi model Claude. Lihat [Perbedaan pemikiran di antara versi model](#differences-in-thinking-across-model-versions) untuk detailnya.
</Note>

## Cara kerja pemikiran diperpanjang \{#how-extended-thinking-works}

Ketika pemikiran diperpanjang diaktifkan, Claude membuat blok konten `thinking` tempat ia mengeluarkan penalaran internalnya. Claude menggabungkan wawasan dari penalaran ini sebelum menyusun respons akhir.

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

Untuk informasi lebih lanjut tentang format respons pemikiran diperpanjang, lihat [Referensi Messages API](/docs/id/api/messages/create).

## Cara menggunakan pemikiran diperpanjang \{#how-to-use-extended-thinking}

Berikut adalah contoh penggunaan pemikiran diperpanjang di Messages API:

<CodeGroup>
```bash cURL
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

# Respons berisi blok pemikiran yang diringkas dan blok teks
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

// Respons berisi blok pemikiran yang diringkas dan blok teks
for (const block of response.content) {
  if (block.type === "thinking") {
    console.log(`\nThinking summary: ${block.thinking}`);
  } else if (block.type === "text") {
    console.log(`\nResponse: ${block.text}`);
  }
}
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

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
		Model:     anthropic.ModelClaudeSonnet4_6,
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

```java Java hidelines={1..7,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;

void main() {
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
            IO.println("\nThinking summary: " + thinkingBlock.thinking())
        );
        block.text().ifPresent(textBlock ->
            IO.println("\nResponse: " + textBlock.text())
        );
    });
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

Untuk mengaktifkan pemikiran diperpanjang, tambahkan objek `thinking`, dengan parameter `type` diatur ke `enabled` dan `budget_tokens` ke anggaran token yang ditentukan untuk pemikiran diperpanjang. Untuk Claude Opus 4.6 dan Claude Sonnet 4.6, gunakan `type: "adaptive"` sebagai gantinya. Lihat [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) untuk detailnya. Meskipun `type: "enabled"` dengan `budget_tokens` masih berfungsi pada model-model ini, konfigurasi tersebut sudah deprecated dan akan dihapus pada rilis mendatang.

Parameter `budget_tokens` menentukan jumlah maksimum token yang diizinkan Claude gunakan untuk proses penalaran internalnya. Batas ini berlaku untuk token pemikiran penuh, bukan untuk [output yang diringkas](#summarized-thinking). Anggaran yang lebih besar dapat meningkatkan kualitas respons dengan memungkinkan analisis yang lebih menyeluruh untuk masalah kompleks, meskipun Claude mungkin tidak menggunakan seluruh anggaran yang dialokasikan, terutama pada rentang di atas 32k.

<Warning>
`budget_tokens` sudah [deprecated](/docs/id/build-with-claude/overview#feature-availability) pada Claude Opus 4.6 dan Claude Sonnet 4.6 dan akan dihapus pada rilis model mendatang. Gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran sebagai gantinya.
</Warning>

<Note>
[Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.8, Claude Opus 4.7, dan Claude Opus 4.6 mendukung hingga 128k token output. Claude Sonnet 4.6 dan Claude Haiku 4.5 mendukung hingga 64k. Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk batas pada model lama. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), [beta header](/docs/id/api/beta-headers) `output-300k-2026-03-24` menaikkan batas output menjadi 300k untuk Claude Opus 4.8, Opus 4.7, Opus 4.6, dan Sonnet 4.6.
</Note>

`budget_tokens` harus diatur ke nilai yang lebih kecil dari `max_tokens`. Namun, saat menggunakan [pemikiran interleaved dengan alat](#interleaved-thinking), Anda dapat melebihi batas ini karena batas token menjadi seluruh jendela konteks Anda. Karena `budget_tokens` harus lebih kecil dari `max_tokens`, pemikiran diperpanjang tidak dapat dikombinasikan dengan `max_tokens: 0` ([pre-warming cache](/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache)).

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
Pada [Claude Mythos Preview](https://anthropic.com/glasswing), `display` secara default bernilai `"omitted"`. Contoh-contoh di bagian ini memberikan `display` secara eksplisit agar berlaku untuk semua model, tetapi pada Mythos Preview Anda dapat membiarkannya tidak diatur dan menerima perilaku yang sama. Untuk menerima pemikiran yang diringkas pada Mythos Preview, atur `display: "summarized"` secara eksplisit.
</Note>

Pipeline otomatis yang tidak pernah menampilkan konten pemikiran kepada pengguna akhir dapat melewati overhead menerima token pemikiran melalui jaringan. Aplikasi yang sensitif terhadap latensi mendapatkan kualitas penalaran yang sama tanpa menunggu teks pemikiran di-stream sebelum respons akhir dimulai.

<CodeGroup>
```bash cURL
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

```bash CLI
ant messages create \
  --model claude-sonnet-4-6 \
  --max-tokens 16000 \
  --transform content --format yaml \
    --thinking '{type: enabled, budget_tokens: 10000, display: omitted}' \
    --message '{role: user, content: "What is 27 * 453?"}'
```

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
});

for (const block of response.content) {
  if (block.type === "thinking") {
    if (block.thinking.length > 0) {
      console.log(`Thinking: ${block.thinking}`);
    } else {
      console.log("Thinking: [omitted]");
    }
  } else if (block.type === "text") {
    console.log(`Response: ${block.text}`);
  }
}
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

var message = await client.Messages.Create(new MessageCreateParams
{
    Model = Model.ClaudeSonnet4_6,
    MaxTokens = 16000,
    Thinking = new ThinkingConfigEnabled
    {
        BudgetTokens = 10000,
        Display = ThinkingConfigEnabledDisplay.Omitted
    },
    Messages =
    [
        new() { Role = Role.User, Content = "What is 27 * 453?" }
    ]
});

foreach (var block in message.Content)
{
    if (block.TryPickThinking(out ThinkingBlock? thinking))
    {
        Console.WriteLine(string.IsNullOrEmpty(thinking.Thinking)
            ? "Thinking: [omitted]"
            : $"Thinking: {thinking.Thinking}");
    }
    else if (block.TryPickText(out TextBlock? text))
    {
        Console.WriteLine($"Response: {text.Text}");
    }
}
```

```go Go hidelines={1..12,-1}
package main

import (
	"cmp"
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 16000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfEnabled: &anthropic.ThinkingConfigEnabledParam{
				BudgetTokens: 10000,
				Display:      anthropic.ThinkingConfigEnabledDisplayOmitted,
			},
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is 27 * 453?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	for _, block := range response.Content {
		switch v := block.AsAny().(type) {
		case anthropic.ThinkingBlock:
			fmt.Println("Thinking:", cmp.Or(v.Thinking, "[omitted]"))
		case anthropic.TextBlock:
			fmt.Println("Response:", v.Text)
		}
	}
}
```

```java Java hidelines={1..5,7}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.ThinkingConfigEnabled;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_4_6)
        .maxTokens(16000L)
        .thinking(ThinkingConfigEnabled.builder()
            .budgetTokens(10000L)
            .display(ThinkingConfigEnabled.Display.OMITTED)
            .build())
        .addUserMessage("What is 27 * 453?")
        .build();

    Message message = client.messages().create(params);

    message.content().forEach(block -> {
        block.thinking().ifPresent(thinkingBlock -> {
            if (thinkingBlock.thinking().isEmpty()) {
                IO.println("Thinking: [omitted]");
            } else {
                IO.println("Thinking: " + thinkingBlock.thinking());
            }
        });
        block.text().ifPresent(textBlock ->
            IO.println("Response: " + textBlock.text())
        );
    });
}
```

```php PHP hidelines={1..3,8}
<?php

use Anthropic\Client;
use Anthropic\Messages\TextBlock;
use Anthropic\Messages\ThinkingBlock;
use Anthropic\Messages\ThinkingConfigEnabled;
use Anthropic\Messages\ThinkingConfigEnabled\Display;

$client = new Client();

$response = $client->messages->create(
    model: 'claude-sonnet-4-6',
    maxTokens: 16000,
    thinking: ThinkingConfigEnabled::with(
        budgetTokens: 10000,
        display: Display::OMITTED,
    ),
    messages: [
        ['role' => 'user', 'content' => 'What is 27 * 453?'],
    ],
);

foreach ($response->content as $block) {
    echo match (true) {
        $block instanceof ThinkingBlock && $block->thinking === '' => "Thinking: [omitted]\n",
        $block instanceof ThinkingBlock => "Thinking: {$block->thinking}\n",
        $block instanceof TextBlock => "Response: {$block->text}\n",
        default => '',
    };
}
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16000,
  thinking: {
    type: :enabled,
    budget_tokens: 10000,
    # SDK Ruby menggunakan `display_` (underscore di akhir) untuk menghindari
    # pembayangan Kernel#display; field pada wire tetap `display`.
    display_: :omitted
  },
  messages: [{role: "user", content: "What is 27 * 453?"}]
)

response.content.each do |block|
  case block.type
  when :thinking
    puts block.thinking.empty? ? "Thinking: [omitted]" : "Thinking: #{block.thinking}"
  when :text
    puts "Response: #{block.text}"
  end
end
```
</CodeGroup>

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

Saat streaming dengan `display: "omitted"`, tidak ada event `thinking_delta` yang dipancarkan; lihat [Streaming pemikiran](#streaming-thinking) di bawah untuk urutan event.

### Streaming pemikiran \{#streaming-thinking}

Anda dapat melakukan streaming respons pemikiran diperpanjang menggunakan [server-sent events (SSE)](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents).

Ketika streaming diaktifkan untuk pemikiran diperpanjang, Anda menerima konten pemikiran melalui event `thinking_delta`.

Ketika `display: "omitted"` diatur, tidak ada event `thinking_delta` yang dipancarkan. Lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display).

Untuk dokumentasi lebih lanjut tentang streaming melalui Messages API, lihat [Streaming Messages](/docs/id/build-with-claude/streaming).

Berikut cara menangani streaming dengan pemikiran:

<CodeGroup tryInConsole={{ userPrompt: "What is the greatest common divisor of 1071 and 462?", thinkingBudgetTokens: 10000 }}>
```bash cURL
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
            # Reset flag untuk setiap blok baru
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
    // Reset flag untuk setiap blok baru
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

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Messages;

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
		Model:     anthropic.ModelClaudeSonnet4_6,
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

```java Java hidelines={1..6,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
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
                IO.println("\nStarting block...")
            );
            event.contentBlockDelta().ifPresent(deltaEvent -> {
                deltaEvent.delta().thinking().ifPresent(td ->
                    IO.print(td.thinking())
                );
                deltaEvent.delta().text().ifPresent(td ->
                    IO.print(td.text())
                );
            });
            event.contentBlockStop().ifPresent(stopEvent ->
                IO.println("\nBlock complete.")
            );
        });
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

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

Ketika `display: "omitted"` diatur, blok pemikiran terbuka, satu `signature_delta` tiba, dan blok ditutup tanpa event `thinking_delta` apa pun. Streaming teks dimulai segera setelahnya:

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
Saat menggunakan streaming dengan pemikiran diaktifkan, Anda mungkin memperhatikan bahwa teks terkadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token demi token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten pemikiran.

Sistem streaming perlu memproses konten dalam batch untuk kinerja optimal, yang dapat menghasilkan pola pengiriman "bergumpal" ini, dengan kemungkinan penundaan di antara event streaming.
</Note>

## Pemikiran diperpanjang dengan penggunaan alat \{#extended-thinking-with-tool-use}

Pemikiran diperpanjang dapat digunakan bersama [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude untuk bernalar melalui pemilihan alat dan pemrosesan hasil.

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, perhatikan batasan berikut:

1. **Batasan pilihan alat**: Penggunaan alat dengan pemikiran hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` akan menghasilkan error karena opsi-opsi ini memaksa penggunaan alat, yang tidak kompatibel dengan pemikiran diperpanjang.

2. **Mempertahankan blok pemikiran**: Selama penggunaan alat, Anda harus mengirimkan kembali blok `thinking` ke API untuk pesan asisten terakhir. Sertakan blok lengkap yang tidak dimodifikasi kembali ke API untuk menjaga kontinuitas penalaran.

### Mengalihkan mode pemikiran dalam percakapan \{#toggling-thinking-modes-in-conversations}

Anda tidak dapat mengalihkan pemikiran di tengah giliran asisten, termasuk selama loop penggunaan alat. Seluruh giliran asisten harus beroperasi dalam satu mode pemikiran:

- **Jika pemikiran diaktifkan**, giliran asisten terakhir harus dimulai dengan blok pemikiran.
- **Jika pemikiran dinonaktifkan**, giliran asisten terakhir tidak boleh berisi blok pemikiran apa pun

Dari perspektif model, **loop penggunaan alat adalah bagian dari giliran asisten**. Giliran asisten tidak selesai sampai Claude menyelesaikan respons penuhnya, yang mungkin mencakup beberapa panggilan alat dan hasil.

Misalnya, urutan ini semuanya merupakan bagian dari **satu giliran asisten**:
```text
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Meskipun ada beberapa pesan API, loop penggunaan alat secara konseptual adalah bagian dari satu respons asisten yang berkelanjutan.

#### Degradasi pemikiran secara halus \{#graceful-thinking-degradation}

Ketika konflik pemikiran di tengah giliran terjadi (seperti mengaktifkan atau menonaktifkan pemikiran selama loop penggunaan alat), API secara otomatis menonaktifkan pemikiran untuk permintaan tersebut. Untuk menjaga kualitas model dan tetap sesuai distribusi, API dapat:

- Menghapus blok pemikiran dari percakapan ketika blok tersebut akan menciptakan struktur giliran yang tidak valid
- Menonaktifkan pemikiran untuk permintaan saat ini ketika riwayat percakapan tidak kompatibel dengan pemikiran yang diaktifkan

Ini berarti bahwa mencoba mengalihkan pemikiran di tengah giliran tidak akan menyebabkan error, tetapi pemikiran akan dinonaktifkan secara diam-diam untuk permintaan tersebut. Untuk mengonfirmasi apakah pemikiran aktif, periksa keberadaan blok `thinking` dalam respons.

#### Panduan praktis \{#practical-guidance}

**Praktik terbaik**: Rencanakan strategi pemikiran Anda di awal setiap giliran daripada mencoba mengalihkannya di tengah giliran.

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
Mengalihkan mode pemikiran juga membatalkan caching prompt untuk riwayat pesan. Untuk detail lebih lanjut, lihat bagian [Pemikiran diperpanjang dengan caching prompt](#extended-thinking-with-prompt-caching).
</Note>

<section title="Contoh: Mengirimkan blok pemikiran dengan hasil alat">

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

```python Python hidelines={1}
import anthropic

client = anthropic.Anthropic()

weather_tool = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
}

# Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

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

// Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
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

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

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
		Model:     anthropic.ModelClaudeSonnet4_6,
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

```java Java hidelines={1..11,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.core.JsonValue;
import java.util.List;
import java.util.Map;

void main() {
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
                .required(List.of("location"))
                .build())
            .build())
        .addUserMessage("What's the weather in Paris?")
        .build();

    Message response = client.messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

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

Respons API mencakup blok thinking, text, dan tool_use:

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

Sekarang mari kita lanjutkan percakapan dan gunakan alat tersebut

<CodeGroup>
```bash CLI
# Giliran pertama: tangkap array konten asisten (thinking + tool_use,
# dengan signature tetap utuh) sebagai JSON ringkas.
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

# Giliran kedua: kirim kembali blok yang ditangkap sebagai pesan asisten.
# Blok thinking HARUS menyertai blok tool_use.
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
# Ekstrak blok pemikiran dan blok penggunaan alat
thinking_block = next(
    (block for block in response.content if block.type == "thinking"), None
)
tool_use_block = next(
    (block for block in response.content if block.type == "tool_use"), None
)

# Panggil API cuaca Anda yang sebenarnya, di sinilah pemanggilan API Anda yang sebenarnya akan dilakukan
# Anggap saja ini yang kita dapatkan kembali
weather_data = {"temperature": 88}

# Permintaan kedua - Sertakan blok pemikiran dan hasil alat
# Tidak ada blok pemikiran baru yang dihasilkan dalam respons
continuation = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"},
        # perhatikan bahwa thinking_block diteruskan bersama dengan tool_use_block
        # jika ini tidak diteruskan, error akan dimunculkan
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
print(continuation)
```

```typescript TypeScript nocheck
// Ekstrak blok pemikiran dan blok penggunaan alat
const thinkingBlock = response.content.find(
  (block): block is Anthropic.ThinkingBlock => block.type === "thinking"
);
const toolUseBlock = response.content.find(
  (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
);

// Panggil API cuaca Anda yang sebenarnya, di sinilah panggilan API Anda yang sebenarnya akan ditempatkan
// Anggap saja ini yang kita dapatkan kembali
const weatherData = { temperature: 88 };

if (thinkingBlock && toolUseBlock) {
  // Permintaan kedua - Sertakan blok pemikiran dan hasil alat
  // Tidak ada blok pemikiran baru yang dihasilkan dalam respons
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
      // perhatikan bahwa thinkingBlock diteruskan bersama dengan toolUseBlock
      // jika ini tidak diteruskan, error akan dimunculkan
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
  console.log(continuation);
}
```

```csharp C# hidelines={1..4}
using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

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

// Ekstrak blok tool_use untuk mendapatkan ID-nya bagi tool result
ToolUseBlock? toolUseBlock = null;
foreach (var block in response.Content)
{
    if (block.TryPickToolUse(out var toolUse))
    {
        toolUseBlock = toolUse;
    }
}

var weatherData = new { temperature = 88 };

// Bangun kelanjutan dengan tool result
var continuationParams = new MessageCreateParams
{
    Model = Model.ClaudeSonnet4_6,
    MaxTokens = 16000,
    Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
    Tools = [weatherTool],
    Messages = [
        new() { Role = Role.User, Content = "What is the weather in Paris?" },
        // response.Content menyertakan blok pemikiran; mengirimkannya kembali adalah wajib
        new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
        new() { Role = Role.User, Content = new MessageParamContent(new List<ContentBlockParam>
        {
            new ContentBlockParam(new ToolResultBlockParam()
            {
                ToolUseID = toolUseBlock?.ID ?? "",
                Content = $"Current temperature: {weatherData.temperature}°F"
            })
        })}
    ]
};

var continuation = await client.Messages.Create(continuationParams);
Console.WriteLine(continuation);
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
		Model:     anthropic.ModelClaudeSonnet4_6,
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
		Model:     anthropic.ModelClaudeSonnet4_6,
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

```java Java hidelines={1..10,13..16}
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

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Tool weatherTool = Tool.builder()
        .name("get_weather")
        .description("Get current weather for a location")
        .inputSchema(Tool.InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "location", Map.of("type", "string", "description", "City name")
            )))
            .required(List.of("location"))
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

    // Permintaan kedua: kirim kembali blok pemikiran dan hasil alat
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
    IO.println(continuation);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

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

Respons API sekarang **hanya** mencakup text

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

### Mempertahankan blok pemikiran \{#preserving-thinking-blocks}

Selama penggunaan alat, Anda harus mengirimkan kembali blok `thinking` ke API, dan Anda harus menyertakan blok lengkap yang tidak dimodifikasi kembali ke API. Ini sangat penting untuk menjaga alur penalaran model dan integritas percakapan.

<Tip>
Meskipun Anda dapat menghilangkan blok `thinking` dari giliran peran `assistant` sebelumnya, selalu kirimkan kembali semua blok pemikiran ke API untuk percakapan multi-giliran apa pun. API:
- Secara otomatis memfilter blok pemikiran yang disediakan
- Menggunakan blok pemikiran relevan yang diperlukan untuk mempertahankan penalaran model
- Hanya menagih token input untuk blok yang ditampilkan kepada Claude

Blok mana yang dipertahankan bergantung pada model. Lihat [Pemeliharaan blok pemikiran berdasarkan model](#thinking-block-preservation-in-claude-opus-45-and-later) untuk default per kelas. Untuk mengganti default, gunakan [strategi pengeditan konteks `clear_thinking_20251015`](/docs/id/build-with-claude/context-editing#thinking-block-clearing).
</Tip>

<Note>
Saat mengalihkan mode pemikiran selama percakapan, ingat bahwa seluruh giliran asisten (termasuk loop penggunaan alat) harus beroperasi dalam satu mode pemikiran. Untuk detail lebih lanjut, lihat [Mengalihkan mode pemikiran dalam percakapan](#toggling-thinking-modes-in-conversations).
</Note>

Ketika Claude memanggil alat, ia menjeda konstruksi responsnya untuk menunggu informasi eksternal. Ketika hasil alat dikembalikan, Claude melanjutkan membangun respons yang ada tersebut. Ini mengharuskan pemeliharaan blok pemikiran selama penggunaan alat, karena beberapa alasan:

1. **Kontinuitas penalaran**: Blok pemikiran menangkap penalaran langkah demi langkah Claude yang mengarah ke permintaan alat. Ketika Anda mengirimkan hasil alat, menyertakan pemikiran asli memastikan Claude dapat melanjutkan penalarannya dari tempat ia berhenti.

2. **Pemeliharaan konteks**: Meskipun hasil alat muncul sebagai pesan pengguna dalam struktur API, hasil tersebut adalah bagian dari alur penalaran yang berkelanjutan. Mempertahankan blok pemikiran menjaga alur konseptual ini di seluruh beberapa panggilan API. Untuk informasi lebih lanjut tentang manajemen konteks, lihat [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows).

**Penting**: Saat memberikan blok `thinking`, seluruh urutan blok `thinking` yang berurutan harus cocok dengan output yang dihasilkan oleh model selama permintaan asli; Anda tidak dapat mengatur ulang atau memodifikasi urutan blok-blok ini.

### Pemikiran interleaved \{#interleaved-thinking}

Pemikiran diperpanjang dengan penggunaan alat pada model Claude 4 mendukung "interleaved thinking" (pemikiran berselang), yang memungkinkan Claude untuk berpikir di antara panggilan alat dan membuat penalaran yang lebih canggih setelah menerima hasil alat.

Dengan pemikiran interleaved, Claude dapat:
- Bernalar tentang hasil panggilan alat sebelum memutuskan apa yang harus dilakukan selanjutnya
- Merangkai beberapa panggilan alat dengan langkah-langkah penalaran di antaranya
- Membuat keputusan yang lebih bernuansa berdasarkan hasil antara

**Dukungan model:**
- **Claude Opus 4.8**: Pemikiran interleaved diaktifkan secara otomatis saat menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (satu-satunya mode pemikiran yang didukung pada Claude Opus 4.8). Tidak diperlukan beta header.
- **[Claude Mythos Preview](https://anthropic.com/glasswing)**: Pemikiran interleaved terjadi secara otomatis. Setiap langkah penalaran antar-alat berpindah ke dalam blok pemikiran alih-alih teks biasa, dan blok pemikiran dipertahankan di seluruh giliran secara default. Tidak diperlukan atau didukung beta header.
- **Claude Opus 4.7**: Pemikiran interleaved diaktifkan secara otomatis saat menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (satu-satunya mode pemikiran yang didukung pada Opus 4.7). Tidak diperlukan beta header.
- **Claude Opus 4.6**: Pemikiran interleaved diaktifkan secara otomatis saat menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking). Tidak diperlukan beta header. Beta header `interleaved-thinking-2025-05-14` sudah **deprecated** pada Opus 4.6 dan diabaikan dengan aman jika disertakan.
- **Claude Sonnet 4.6**: Pemikiran interleaved diaktifkan secara otomatis saat menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (direkomendasikan). Beta header `interleaved-thinking-2025-05-14` dengan pemikiran diperpanjang manual (`thinking: {type: "enabled"}`) masih berfungsi tetapi sudah deprecated.
- **Model Claude 4 lainnya** (Opus 4.5, Opus 4.1 (deprecated), Opus 4 (deprecated), Sonnet 4.5, Sonnet 4 (deprecated)): Tambahkan [beta header](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda untuk mengaktifkan pemikiran interleaved.

Berikut adalah beberapa pertimbangan penting untuk pemikiran interleaved:
- Dengan pemikiran interleaved, `budget_tokens` dapat melebihi parameter `max_tokens`, karena mewakili total anggaran di seluruh blok pemikiran dalam satu giliran asisten.
- Pemikiran interleaved hanya didukung untuk [alat yang digunakan melalui Messages API](/docs/id/agents-and-tools/tool-use/overview).
- Claude API dan [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) menerima `interleaved-thinking-2025-05-14` dalam permintaan ke model apa pun tanpa mengembalikan error. Pada model yang tidak mendukung pemikiran interleaved, header diabaikan. Pada Claude Opus 4.8, Claude Opus 4.7, dan Claude Opus 4.6, header tersebut sudah deprecated dan diabaikan dengan aman. Pada Claude Mythos Preview, header tersebut tidak diperlukan dan diabaikan dengan aman.
- Pada platform yang dioperasikan mitra (misalnya, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)), jika Anda memberikan `interleaved-thinking-2025-05-14` ke model apa pun selain Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5, Claude Opus 4.1 (deprecated), Opus 4 (deprecated), Sonnet 4.5, atau Sonnet 4 (deprecated), permintaan Anda akan gagal.

<section title="Penggunaan alat tanpa pemikiran interleaved">

Tanpa pemikiran interleaved, Claude berpikir sekali di awal giliran asisten. Respons berikutnya setelah hasil alat berlanjut tanpa blok pemikiran baru.

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

<section title="Penggunaan alat dengan pemikiran interleaved">

Dengan pemikiran interleaved diaktifkan, Claude dapat berpikir setelah menerima setiap hasil alat, memungkinkannya untuk bernalar tentang hasil antara sebelum melanjutkan.

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

## Pemikiran diperpanjang dengan caching prompt \{#extended-thinking-with-prompt-caching}

[Caching prompt](/docs/id/build-with-claude/prompt-caching) dengan pemikiran memiliki beberapa pertimbangan penting:

<Tip>
Tugas pemikiran diperpanjang sering memakan waktu lebih dari 5 menit untuk diselesaikan. Pertimbangkan untuk menggunakan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hit di seluruh sesi pemikiran yang lebih lama dan alur kerja multi-langkah.
</Tip>

**Penghapusan konteks blok pemikiran**
- Pada model Opus/Sonnet yang lebih lama dan semua model Haiku, blok pemikiran dari giliran sebelumnya dihapus dari konteks, yang dapat memengaruhi breakpoint cache. Pada Opus 4.5+ dan Sonnet 4.6+, blok tersebut dipertahankan secara default.
- Saat melanjutkan percakapan dengan penggunaan alat, blok pemikiran di-cache dan dihitung sebagai token input saat dibaca dari cache
- Ini menciptakan trade-off: meskipun blok pemikiran tidak mengonsumsi ruang jendela konteks secara visual, blok tersebut tetap dihitung terhadap penggunaan token input Anda saat di-cache
- Jika pemikiran menjadi dinonaktifkan dan Anda mengirimkan konten pemikiran dalam giliran penggunaan alat saat ini, konten pemikiran akan dihapus dan pemikiran akan tetap dinonaktifkan untuk permintaan tersebut

**Pola pembatalan cache**
- Perubahan pada parameter pemikiran (diaktifkan/dinonaktifkan atau alokasi anggaran) membatalkan breakpoint cache pesan
- [Pemikiran interleaved](#interleaved-thinking) memperkuat pembatalan cache, karena blok pemikiran dapat terjadi di antara beberapa [panggilan alat](#extended-thinking-with-tool-use)
- Prompt sistem dan alat tetap di-cache meskipun ada perubahan parameter pemikiran atau penghapusan blok

<Note>
Pada model Opus/Sonnet yang lebih lama dan semua model Haiku, blok pemikiran dihapus untuk caching dan perhitungan konteks; pada Opus 4.5+ dan Sonnet 4.6+, blok tersebut dipertahankan secara default. Dalam kedua kasus, blok tersebut harus dipertahankan saat melanjutkan percakapan dengan [penggunaan alat](#extended-thinking-with-tool-use), terutama dengan [pemikiran interleaved](#interleaved-thinking).
</Note>

### Memahami perilaku caching blok pemikiran \{#understanding-thinking-block-caching-behavior}

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, blok pemikiran menunjukkan perilaku caching spesifik yang memengaruhi penghitungan token:

**Cara kerjanya:**

1. Caching hanya terjadi ketika Anda membuat permintaan berikutnya yang menyertakan hasil alat
2. Ketika permintaan berikutnya dibuat, riwayat percakapan sebelumnya (termasuk blok pemikiran) dapat di-cache
3. Blok pemikiran yang di-cache ini dihitung sebagai token input dalam metrik penggunaan Anda saat dibaca dari cache
4. Ketika blok pengguna non-tool-result disertakan: pada Opus 4.5+ dan Sonnet 4.6+, blok pemikiran sebelumnya dipertahankan; pada model Opus/Sonnet yang lebih lama dan semua model Haiku, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks

**Contoh alur terperinci:**

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
Permintaan 2 menulis cache dari konten permintaan (bukan respons). Cache mencakup pesan pengguna asli, blok pemikiran pertama, blok tool use, dan hasil alat.

**Permintaan 3:**
```text
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```
Untuk Opus 4.5+ dan Sonnet 4.6+, semua blok pemikiran sebelumnya dipertahankan secara default. Untuk model Opus/Sonnet yang lebih lama dan semua model Haiku, karena blok pengguna non-tool-result disertakan, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks. Permintaan ini akan diproses sama seperti:
```text
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

**Poin-poin penting:**
- Perilaku caching ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit
- Perilaku ini konsisten baik menggunakan pemikiran reguler maupun pemikiran interleaved

<section title="Caching prompt sistem (dipertahankan saat pemikiran berubah)">

<CodeGroup>
```bash CLI
# Ambil ~10 kB dari Pride and Prejudice untuk blok sistem yang di-cache
curl -s https://www.gutenberg.org/cache/epub/1342/pg1342.txt \
  | head -c 10000 > pride.txt

# Hasilkan body permintaan untuk anggaran pemikiran yang diberikan. Setelah CONTENT1
# terisi (setelah giliran pertama), balasan asisten dan pesan
# lanjutan dari pengguna ditambahkan agar percakapan bertambah panjang.
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

# Permintaan pertama (anggaran 4000): membentuk cache. Tangkap usage
# dan content sebagai dua baris jsonl agar balasan bisa diteruskan.
printf 'First request - establishing cache\n'
{
  read -r USAGE1
  read -r CONTENT1
} < <(build_body 4000 \
  | ant messages create --transform '[usage,content]' --format jsonl)
printf 'First response usage: %s\n' "$USAGE1"

# Permintaan kedua: anggaran sama, cache hit prompt sistem diharapkan.
printf '\nSecond request - same thinking parameters (cache hit expected)\n'
USAGE2=$(build_body 4000 \
  | ant messages create --transform usage --format jsonl)
printf 'Second response usage: %s\n' "$USAGE2"

# Permintaan ketiga: anggaran diubah ke 8000. Prompt sistem yang di-cache
# tetap hit; hanya caching blok pesan yang diinvalidasi.
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

    # Ambil teks
    text = soup.get_text()

    # Pecah menjadi baris-baris dan hapus spasi di awal dan akhir setiap baris
    lines = (line.strip() for line in text.splitlines())
    # Pecah multi-headline menjadi satu baris masing-masing
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Buang baris kosong
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


# Ambil konten artikel
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Gunakan teks secukupnya untuk caching (beberapa bab pertama)
LARGE_TEXT = book_content[:10000]

SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.",
    },
    {"type": "text", "text": LARGE_TEXT, "cache_control": {"type": "ephemeral"}},
]

MESSAGES = [{"role": "user", "content": "Analyze the tone of this passage."}]

# Permintaan pertama - membangun cache
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
# Permintaan kedua - parameter thinking yang sama (diharapkan cache hit)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 4000},
    system=SYSTEM_PROMPT,
    messages=MESSAGES,
)

print(f"Second response usage: {response2.usage}")

# Permintaan ketiga - parameter thinking berbeda (cache miss untuk messages)
print("\nThird request - different thinking parameters (cache miss for messages)")
response3 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000,  # Changed thinking budget
    },
    system=SYSTEM_PROMPT,  # System prompt remains cached
    messages=MESSAGES,  # Messages cache is invalidated
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

// Permintaan pertama - membuat cache
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
  content: response1.content
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
```

```csharp C# hidelines={1..4}
using System.Net.Http;
using Anthropic;
using Anthropic.Models.Messages;

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

// Permintaan pertama - membuat cache
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

messages.Add(new() { Role = Role.Assistant, Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList() });
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

// Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
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

	// Permintaan pertama - membuat cache
	fmt.Println("First request - establishing cache")
	response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

	messages = append(messages, response1.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

	// Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
	fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
	response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

	// Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
	fmt.Println("\nThird request - different thinking parameters (cache miss for messages)")
	response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
		System:    systemPrompt,
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
}
```

```java Java hidelines={1..2,4..13}
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

void main() throws Exception {
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

    // Permintaan pertama - membuat cache
    IO.println("First request - establishing cache");
    MessageCreateParams params1 = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_4_6)
        .maxTokens(20000L)
        .enabledThinking(4000L)
        .systemOfTextBlockParams(systemPrompt)
        .addUserMessage("Analyze the tone of this passage.")
        .build();

    Message response1 = client.messages().create(params1);
    IO.println("First response usage: " + response1.usage());

    // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
    IO.println("\nSecond request - same thinking parameters (cache hit expected)");
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
    IO.println("Second response usage: " + response2.usage());

    // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
    IO.println("\nThird request - different thinking parameters (cache miss for messages)");
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
    IO.println("Third response usage: " + response3.usage());
}
```

```php PHP hidelines={1..5}
<?php


use Anthropic\Client;

$client = new Client();

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

// Permintaan pertama - membuat cache
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

// Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
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

# Permintaan pertama - membuat cache
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

# Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
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
<section title="Caching pesan (dibatalkan saat pemikiran berubah)">

<CodeGroup>
```bash CLI
# Ambil ~10 kB pertama dari Pride and Prejudice untuk prefiks yang di-cache
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

# Panggilan 2: anggaran sama, percakapan diperpanjang; diharapkan cache HIT
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

# Panggilan 3: anggaran diubah menjadi 8000; cache MISS meskipun prefiks identik
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

    # Ambil teks
    text = soup.get_text()

    # Pecah menjadi baris-baris dan hapus spasi di awal dan akhir setiap baris
    lines = (line.strip() for line in text.splitlines())
    # Pecah multi-headline menjadi satu baris masing-masing
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Buang baris kosong
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


# Ambil konten artikel
book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
book_content = fetch_article_content(book_url)
# Gunakan teks secukupnya untuk caching (beberapa bab pertama)
LARGE_TEXT = book_content[:10000]

# Tanpa prompt sistem - caching di messages sebagai gantinya
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

# Permintaan pertama - membuat cache
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
# Permintaan kedua - parameter thinking yang sama (diharapkan cache hit)
print("\nSecond request - same thinking parameters (cache hit expected)")
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 4000,  # Same thinking budget
    },
    messages=MESSAGES,
)

print(f"Second response usage: {response2.usage}")

MESSAGES.append({"role": "assistant", "content": response2.content})
MESSAGES.append({"role": "user", "content": "Analyze the setting in this passage."})

# Permintaan ketiga - budget thinking berbeda (diharapkan cache miss)
print("\nThird request - different thinking budget (cache miss expected)")
response3 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000,  # Different thinking budget breaks cache
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

  // Ambil teks
  let text = $.text();

  // Bersihkan teks (pecah menjadi baris, hapus spasi kosong)
  const lines = text.split("\n").map((line) => line.trim());
  const chunks = lines.flatMap((line) => line.split("  ").map((phrase) => phrase.trim()));
  text = chunks.filter((chunk) => chunk).join("\n");

  return text;
}

const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
const bookContent = await fetchArticleContent(bookUrl);
const LARGE_TEXT = bookContent.substring(0, 10000);

// Tanpa prompt sistem - caching dilakukan di messages sebagai gantinya
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

// Permintaan pertama - membangun cache
console.log("First request - establishing cache");
const response1 = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: { type: "enabled", budget_tokens: 4000 },
  messages
});

console.log("First response usage: ", response1.usage);

messages.push(
  { role: "assistant", content: response1.content },
  { role: "user", content: "Analyze the characters in this passage." }
);

// Permintaan kedua - parameter pemikiran yang sama (diharapkan cache hit)
console.log("\nSecond request - same thinking parameters (cache hit expected)");
const response2 = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: { type: "enabled", budget_tokens: 4000 },
  messages
});

console.log("Second response usage: ", response2.usage);

messages.push(
  { role: "assistant", content: response2.content },
  { role: "user", content: "Analyze the setting in this passage." }
);

// Permintaan ketiga - anggaran pemikiran berbeda (diharapkan cache miss)
console.log("\nThird request - different thinking budget (cache miss expected)");
const response3 = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 20000,
  thinking: { type: "enabled", budget_tokens: 8000 },
  messages
});

console.log("Third response usage: ", response3.usage);
```

```csharp C# hidelines={1..4}
using System.Net.Http;
using Anthropic;
using Anthropic.Models.Messages;

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
            Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
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
            Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
        },
        new()
        {
            Role = Role.User,
            Content = "Analyze the characters in this passage."
        },
        new()
        {
            Role = Role.Assistant,
            Content = response2.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
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

static async Task<string> FetchArticleContent(string url)
{
    using HttpClient httpClient = new();
    string content = await httpClient.GetStringAsync(url);
    return content;
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

	// Tanpa prompt sistem - caching dilakukan di messages
	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(
			anthropic.ContentBlockParamUnion{OfText: &anthropic.TextBlockParam{
				Text:         largeText,
				CacheControl: anthropic.NewCacheControlEphemeralParam(),
			}},
			anthropic.NewTextBlock("Analyze the tone of this passage."),
		),
	}

	// Permintaan pertama - membuat cache
	fmt.Println("First request - establishing cache")
	response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

	messages = append(messages, response1.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

	// Permintaan kedua - parameter pemikiran sama (diharapkan cache hit)
	fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
	response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

	messages = append(messages, response2.ToParam())
	messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the setting in this passage.")))

	// Permintaan ketiga - anggaran pemikiran berbeda (diharapkan cache miss)
	fmt.Println("\nThird request - different thinking budget (cache miss expected)")
	response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 20000,
		Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
		Messages:  messages,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
}
```

```java Java hidelines={1..2,4..14}
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

void main() throws Exception {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    String bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
    String bookContent = fetchArticleContent(bookUrl);
    String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

    // Permintaan pertama - membuat cache
    IO.println("First request - establishing cache");
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
    IO.println("First response usage: " + response1.usage());

    // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
    IO.println("\nSecond request - same thinking parameters (cache hit expected)");
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
    IO.println("Second response usage: " + response2.usage());

    // Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
    IO.println("\nThird request - different thinking budget (cache miss expected)");
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
    IO.println("Third response usage: " + response3.usage());
}

String fetchArticleContent(String url) throws Exception {
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(url))
        .build();
    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    return response.body();
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

$client = new Client();

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

Contoh ini menunjukkan bahwa ketika caching diatur dalam array pesan, mengubah parameter pemikiran (budget_tokens ditingkatkan dari 4000 menjadi 8000) **membatalkan cache**. Permintaan ketiga menunjukkan tidak ada cache hit dengan `cache_creation_input_tokens=1370` dan `cache_read_input_tokens=0`, membuktikan bahwa caching berbasis pesan dibatalkan ketika parameter pemikiran berubah.

</section>

## Max tokens dan ukuran jendela konteks dengan pemikiran diperpanjang \{#max-tokens-and-context-window-size-with-extended-thinking}

`max_tokens` (yang mencakup anggaran pemikiran Anda saat pemikiran diaktifkan) diberlakukan sebagai batas ketat. Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan tersebut. Jika generasi kemudian mencapai batas jendela konteks, generasi berhenti dengan `stop_reason: "model_context_window_exceeded"`. Pada model yang lebih lama, API mengembalikan error validasi sebagai gantinya. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).

<Note>
Anda dapat membaca [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows) untuk pembahasan yang lebih mendalam.
</Note>

### Jendela konteks dengan pemikiran diperpanjang \{#the-context-window-with-extended-thinking}

Saat menghitung penggunaan jendela konteks dengan pemikiran diaktifkan, ada beberapa pertimbangan yang perlu diperhatikan:

- Pada Opus 4.5+ dan Sonnet 4.6+, blok pemikiran dari giliran sebelumnya dipertahankan dan dihitung terhadap jendela konteks Anda; pada model Opus/Sonnet yang lebih lama dan semua model Haiku, blok tersebut dihapus dan tidak dihitung
- Pemikiran giliran saat ini dihitung terhadap batas `max_tokens` Anda untuk giliran tersebut

Diagram di bawah ini menunjukkan manajemen token khusus saat pemikiran diperpanjang diaktifkan:

![Diagram jendela konteks dengan pemikiran diperpanjang](/docs/images/context-window-thinking.svg)

Jendela konteks efektif dihitung sebagai:

```text
context window =
  (current input tokens - previous thinking tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan jumlah token yang akurat untuk kasus penggunaan spesifik Anda, terutama saat bekerja dengan percakapan multi-giliran yang mencakup pemikiran.

### Jendela konteks dengan pemikiran diperpanjang dan penggunaan alat \{#the-context-window-with-extended-thinking-and-tool-use}

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, blok pemikiran harus dipertahankan secara eksplisit dan dikembalikan dengan hasil alat.

Perhitungan jendela konteks efektif untuk pemikiran diperpanjang dengan penggunaan alat menjadi:

```text
context window =
  (current input tokens + previous thinking tokens + tool use tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Diagram di bawah ini mengilustrasikan manajemen token untuk pemikiran diperpanjang dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran diperpanjang dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

### Mengelola token dengan pemikiran diperpanjang \{#managing-tokens-with-extended-thinking}

Mengingat perilaku jendela konteks dan `max_tokens` dengan pemikiran diperpanjang, Anda mungkin perlu:

- Lebih aktif memantau dan mengelola penggunaan token Anda
- Menyesuaikan nilai `max_tokens` seiring perubahan panjang prompt Anda
- Berpotensi menggunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) lebih sering
- Menyadari bahwa blok pemikiran sebelumnya tidak terakumulasi dalam jendela konteks Anda

## Enkripsi pemikiran \{#thinking-encryption}

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

## Blok pemikiran yang disunting \{#redacted-thinking-blocks}

Selain blok `thinking` reguler, API dapat mengembalikan blok `redacted_thinking`. Blok `redacted_thinking` berisi konten pemikiran terenkripsi dalam field `data`, tanpa ringkasan yang dapat dibaca:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

Field `data` bersifat opaque dan terenkripsi. Seperti field `signature` pada blok pemikiran reguler, Anda harus mengirimkan kembali blok `redacted_thinking` ke API tanpa perubahan saat melanjutkan percakapan multi-giliran dengan [alat](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).

<Tip>
Jika kode Anda memfilter blok konten berdasarkan tipe (misalnya, `block.type == "thinking"`) saat mengirim balik respons dengan penggunaan alat, sertakan juga blok `redacted_thinking`. Memfilter hanya pada `block.type == "thinking"` secara diam-diam menghilangkan blok `redacted_thinking` dan merusak protokol multi-giliran yang dijelaskan di atas.
</Tip>

<Note>
Blok `redacted_thinking` adalah tipe blok konten yang berbeda yang dikembalikan oleh API ketika bagian dari pemikiran disunting karena alasan keamanan. Ini terpisah dari opsi [`display: "omitted"`](#controlling-thinking-display), yang mengembalikan blok `thinking` reguler dengan field `thinking` kosong.
</Note>

## Perbedaan pemikiran di antara versi model \{#differences-in-thinking-across-model-versions}

Messages API menangani pemikiran secara berbeda di antara versi model Claude. Tabel berikut memberikan perbandingan ringkas:

| Fitur | Model Claude 4 (sebelum Opus 4.5) | Claude Opus 4.5 | Claude Sonnet 4.6 | Claude Opus 4.6 ([pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)) | Claude Opus 4.7 ([pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)) | Claude Opus 4.8 ([pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)) | [Claude Mythos Preview](https://anthropic.com/glasswing) ([pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)) |
|---------|-------------------------------|--------------------------|------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| **Output pemikiran** | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Mengembalikan pemikiran yang diringkas | Dihilangkan secara default; atur `display: "summarized"` untuk menerima pemikiran yang diringkas | Dihilangkan secara default; atur `display: "summarized"` untuk menerima pemikiran yang diringkas | Dihilangkan secara default; atur `display: "summarized"` untuk menerima pemikiran yang diringkas. Token pemikiran mentah tidak pernah dikembalikan. |
| **Pemikiran interleaved** | Didukung dengan beta header `interleaved-thinking-2025-05-14` | Didukung dengan beta header `interleaved-thinking-2025-05-14` | Didukung dengan beta header `interleaved-thinking-2025-05-14` atau otomatis dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) | Otomatis dengan pemikiran adaptif (beta header deprecated dan diabaikan dengan aman) | Otomatis dengan pemikiran adaptif (beta header deprecated dan diabaikan dengan aman) | Otomatis dengan pemikiran adaptif (beta header deprecated dan diabaikan dengan aman) | Otomatis dengan pemikiran adaptif (beta header tidak diperlukan dan diabaikan dengan aman). Penalaran antar-alat berpindah ke dalam blok pemikiran pada model ini. |
| **Pemeliharaan blok pemikiran** | Tidak dipertahankan di seluruh giliran | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default** | **Dipertahankan secara default.** Blok dihapus saat melanjutkan percakapan pada model yang tidak mendukung format pemikiran Mythos. |

### Pemeliharaan blok pemikiran berdasarkan model \{#thinking-block-preservation-by-model}

Apakah blok pemikiran dari giliran asisten sebelumnya dipertahankan dalam konteks secara default bergantung pada kelas model. **Opus**: Claude Opus 4.5 dan model Opus yang lebih baru mempertahankan semua blok pemikiran sebelumnya; Claude Opus 4.1 (deprecated) dan model Opus yang lebih lama hanya mempertahankan pemikiran giliran asisten terakhir. **Sonnet**: Claude Sonnet 4.6 dan model Sonnet yang lebih baru mempertahankan semua; Claude Sonnet 4.5 dan model Sonnet yang lebih lama hanya mempertahankan giliran terakhir. **Haiku**: semua model Haiku hingga Claude Haiku 4.5 hanya mempertahankan giliran terakhir. [Claude Mythos Preview](https://anthropic.com/glasswing) juga mempertahankan semua blok pemikiran sebelumnya.

**Manfaat pemeliharaan blok pemikiran:**

- **Optimasi cache**: Saat menggunakan penggunaan alat, blok pemikiran yang dipertahankan memungkinkan cache hit karena blok tersebut dikirim kembali dengan hasil alat dan di-cache secara inkremental di seluruh giliran asisten, menghasilkan penghematan token dalam alur kerja multi-langkah
- **Tidak ada dampak kecerdasan**: Mempertahankan blok pemikiran tidak memiliki efek negatif pada kinerja model

**Pertimbangan penting:**

- **Penggunaan konteks**: Percakapan panjang akan mengonsumsi lebih banyak ruang konteks karena blok pemikiran dipertahankan dalam konteks
- **Perilaku otomatis**: Ini adalah default untuk setiap model seperti yang tercantum di atas. Tidak diperlukan perubahan kode atau beta header
- **Kompatibilitas mundur**: Untuk memanfaatkan fitur ini, terus kirimkan kembali blok pemikiran yang lengkap dan tidak dimodifikasi ke API seperti yang Anda lakukan untuk penggunaan alat

<Note>
Untuk model yang lebih lama (Claude Sonnet 4.5, Opus 4.1 (deprecated), dll.), blok pemikiran dari giliran sebelumnya terus dihapus dari konteks. Perilaku yang ada yang dijelaskan di bagian [Pemikiran diperpanjang dengan caching prompt](#extended-thinking-with-prompt-caching) berlaku untuk model-model tersebut.
</Note>

## Harga \{#pricing}

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

## Praktik terbaik dan pertimbangan untuk pemikiran diperpanjang \{#best-practices-and-considerations-for-extended-thinking}

### Bekerja dengan anggaran pemikiran \{#working-with-thinking-budgets}

- **Optimasi anggaran:** Anggaran minimum adalah 1.024 token. Mulailah dari nilai minimum dan tingkatkan anggaran pemikiran secara bertahap untuk menemukan rentang optimal bagi kasus penggunaan Anda. Jumlah token yang lebih tinggi memungkinkan penalaran yang lebih komprehensif, tetapi dengan hasil yang semakin berkurang tergantung pada tugasnya. Meningkatkan anggaran dapat meningkatkan kualitas respons dengan konsekuensi peningkatan "latency" (latensi). Untuk tugas-tugas penting, uji berbagai pengaturan untuk menemukan keseimbangan optimal. Perhatikan bahwa anggaran pemikiran adalah target, bukan batas yang ketat. Penggunaan token aktual dapat bervariasi berdasarkan tugas.
- **Titik awal:** Mulailah dengan anggaran pemikiran yang lebih besar (16k+ token) untuk tugas-tugas kompleks dan sesuaikan berdasarkan kebutuhan Anda.
- **Anggaran besar:** Untuk anggaran pemikiran di atas 32k, gunakan [batch processing](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Permintaan yang mendorong model untuk berpikir di atas 32k token menyebabkan permintaan yang berjalan lama yang mungkin terbentur dengan batas waktu sistem dan batas koneksi terbuka.
- **Pelacakan penggunaan token:** Pantau penggunaan token pemikiran untuk mengoptimalkan biaya dan kinerja. Field `usage.output_tokens_details.thinking_tokens` dalam respons melaporkan berapa banyak dari token output yang ditagih merupakan penalaran internal. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir.

### Pertimbangan kinerja \{#performance-considerations}

- **Waktu respons:** Bersiaplah untuk waktu respons yang lebih lama karena pemrosesan tambahan. Menghasilkan blok pemikiran meningkatkan waktu respons secara keseluruhan.
- **Persyaratan streaming:** SDK mengharuskan streaming ketika `max_tokens` lebih besar dari 21.333 untuk menghindari timeout HTTP pada permintaan yang berjalan lama. Ini adalah validasi sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses event secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani event individual. Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detailnya. Saat streaming, bersiaplah untuk menangani blok konten pemikiran dan teks saat keduanya tiba.
- **Menghilangkan pemikiran untuk latensi:** Jika aplikasi Anda tidak menampilkan konten pemikiran, atur `display: "omitted"` pada konfigurasi pemikiran untuk mengurangi waktu hingga token teks pertama. Lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display).

### Kompatibilitas fitur \{#feature-compatibility}

- Pemikiran tidak kompatibel dengan modifikasi `temperature` atau `top_k` serta [penggunaan alat yang dipaksakan](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).
- Ketika pemikiran diaktifkan, Anda dapat mengatur `top_p` ke nilai antara 1 dan 0,95.
- Anda tidak dapat mengisi respons terlebih dahulu (pre-fill) ketika pemikiran diaktifkan.
- Perubahan pada anggaran pemikiran membatalkan prefiks prompt yang di-cache yang menyertakan pesan. Namun, prompt sistem dan definisi alat yang di-cache akan tetap berfungsi ketika parameter pemikiran berubah.

### Panduan penggunaan \{#usage-guidelines}

- **Pemilihan tugas:** Gunakan pemikiran diperpanjang untuk tugas-tugas yang sangat kompleks yang mendapat manfaat dari penalaran langkah demi langkah, seperti matematika, pemrograman, dan analisis.
- **Penanganan konteks:** Anda tidak perlu menghapus blok pemikiran sebelumnya sendiri. Pada Opus 4.5+ dan Sonnet 4.6+, API Claude menyimpan blok pemikiran dari giliran sebelumnya secara default; pada model Opus/Sonnet yang lebih lama dan semua model Haiku, API secara otomatis mengabaikannya dan blok tersebut tidak disertakan saat menghitung penggunaan konteks.
- **Rekayasa prompt:** Tinjau [tips prompting pemikiran diperpanjang](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities) jika Anda ingin memaksimalkan kemampuan pemikiran Claude.

## Langkah selanjutnya \{#next-steps}

<CardGroup>
  <Card title="Coba cookbook pemikiran diperpanjang" icon="book" href="https://platform.claude.com/cookbook/extended-thinking-extended-thinking">
    Jelajahi contoh praktis pemikiran dalam cookbook.
  </Card>
  <Card title="Tips prompting pemikiran diperpanjang" icon="code" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities">
    Pelajari praktik terbaik rekayasa prompt untuk pemikiran diperpanjang.
  </Card>
</CardGroup>