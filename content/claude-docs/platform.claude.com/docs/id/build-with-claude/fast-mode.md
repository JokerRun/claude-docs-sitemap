---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 99c1a06e81e8b00f5dc057329768120863126758cbfdf133a1a956e7c7c1e5cd
---

# Mode cepat (pratinjau penelitian)

Kecepatan output lebih tinggi untuk Claude Opus 4.6, memberikan pembuatan token yang jauh lebih cepat untuk alur kerja yang sensitif terhadap latensi dan agentic.

---

Mode cepat menyediakan pembuatan token output yang jauh lebih cepat untuk Claude Opus 4.6. Dengan mengatur `speed: "fast"` dalam permintaan API Anda, Anda mendapatkan hingga 2,5x token output per detik yang lebih tinggi dari model yang sama dengan harga premium.

<Note>
Mode cepat saat ini dalam pratinjau penelitian. [Bergabunglah dengan daftar tunggu](https://claude.com/fast-mode) untuk meminta akses. Ketersediaan terbatas saat kami mengumpulkan umpan balik.
</Note>

## Model yang didukung

Mode cepat didukung pada model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`)

## Cara kerja mode cepat

Mode cepat menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

- Hingga 2,5x token output per detik yang lebih tinggi dibandingkan dengan kecepatan standar
- Manfaat kecepatan berfokus pada token output per detik (OTPS), bukan waktu ke token pertama (TTFT)
- Bobot model dan perilaku yang sama (bukan model yang berbeda)

## Penggunaan dasar

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: fast-mode-2026-02-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "speed": "fast",
        "messages": [{
            "role": "user",
            "content": "Refactor this module to use dependency injection"
        }]
    }'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[
        {"role": "user", "content": "Refactor this module to use dependency injection"}
    ],
)

print(response.content[0].text)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{
    role: "user",
    content: "Refactor this module to use dependency injection"
  }]
});

console.log(response.content[0].text);
```

</CodeGroup>

## Harga

Mode cepat dihargai pada 6x tarif Opus standar untuk prompt ≤200K token, dan 12x tarif Opus standar untuk prompt > 200K token. Tabel berikut menunjukkan harga untuk Claude Opus 4.6 dengan mode cepat:

| Jendela konteks | Input | Output |
|:---------------|:------|:-------|
| ≤ 200K token input | $30 / MTok | $150 / MTok |
| > 200K token input | $60 / MTok | $225 / MTok |

Harga mode cepat ditumpuk dengan pengubah harga lainnya:

- [Pengganda prompt caching](/docs/id/about-claude/pricing#model-pricing) berlaku di atas harga mode cepat
- [Residensi data](/docs/id/build-with-claude/data-residency) pengganda berlaku di atas harga mode cepat

Untuk detail harga lengkap, lihat [halaman harga](/docs/id/about-claude/pricing#fast-mode-pricing).

## Batas laju

Mode cepat memiliki batas laju khusus yang terpisah dari batas laju Opus standar. Tidak seperti kecepatan standar, yang memiliki batas terpisah untuk ≤200K dan >200K token input, mode cepat menggunakan batas laju tunggal yang mencakup rentang konteks penuh. Ketika batas laju mode cepat Anda terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Respons mencakup header yang menunjukkan status batas laju mode cepat Anda:

| Header | Deskripsi |
|:-------|:------------|
| `anthropic-fast-input-tokens-limit` | Token input mode cepat maksimum per menit |
| `anthropic-fast-input-tokens-remaining` | Token input mode cepat yang tersisa |
| `anthropic-fast-input-tokens-reset` | Waktu ketika batas token input mode cepat direset |
| `anthropic-fast-output-tokens-limit` | Token output mode cepat maksimum per menit |
| `anthropic-fast-output-tokens-remaining` | Token output mode cepat yang tersisa |
| `anthropic-fast-output-tokens-reset` | Waktu ketika batas token output mode cepat direset |

Untuk batas laju khusus tingkat, lihat [halaman batas laju](/docs/id/api/rate-limits).

## Memeriksa kecepatan mana yang digunakan

Objek `usage` respons mencakup bidang `speed` yang menunjukkan kecepatan mana yang digunakan, baik `"fast"` atau `"standard"`:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: fast-mode-2026-02-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 1024,
        "speed": "fast",
        "messages": [{"role": "user", "content": "Hello"}]
    }'

{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  ...
  "usage": {
    "input_tokens": 523,
    "output_tokens": 1842,
    "speed": "fast"
  }
}
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.usage.speed)  # "fast" or "standard"
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{ role: "user", content: "Hello" }]
});

console.log(response.usage.speed); // "fast" or "standard"
```

```ruby Ruby
response = anthropic.beta.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 1024,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{ role: "user", content: "Hello" }]
)

puts(response.usage.speed)  # "fast" or "standard"
```
</CodeGroup>

Untuk melacak penggunaan mode cepat dan biaya di seluruh organisasi Anda, lihat [API Penggunaan dan Biaya](/docs/id/build-with-claude/usage-cost-api).

## Percobaan ulang dan fallback

### Percobaan ulang otomatis

Ketika batas laju mode cepat terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after`. SDK Anthropic secara otomatis mencoba ulang permintaan ini hingga 2 kali secara default (dapat dikonfigurasi melalui `max_retries`), menunggu penundaan yang ditentukan server sebelum setiap percobaan ulang. Karena mode cepat menggunakan pengisian ulang token berkelanjutan, penundaan `retry-after` biasanya singkat dan permintaan berhasil setelah kapasitas tersedia.

### Jatuh kembali ke kecepatan standar

Jika Anda lebih suka jatuh kembali ke kecepatan standar daripada menunggu kapasitas mode cepat, tangkap kesalahan batas laju dan coba ulang tanpa `speed: "fast"`. Atur `max_retries` ke `0` pada permintaan cepat awal untuk melewati percobaan ulang otomatis dan gagal segera pada kesalahan batas laju.

<Note>
Jatuh kembali dari cepat ke kecepatan standar akan menghasilkan [prompt cache](/docs/id/build-with-claude/prompt-caching) miss. Permintaan pada kecepatan berbeda tidak berbagi awalan yang di-cache.
</Note>

Karena mengatur `max_retries` ke `0` juga menonaktifkan percobaan ulang untuk kesalahan transien lainnya (kelebihan beban, kesalahan server internal), contoh di bawah mengeluarkan kembali permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()


def create_message_with_fast_fallback(max_retries=None, max_attempts=3, **params):
    try:
        return client.beta.messages.create(**params, max_retries=max_retries)
    except anthropic.RateLimitError:
        if params.get("speed") == "fast":
            del params["speed"]
            return create_message_with_fast_fallback(**params)
        raise
    except (
        anthropic.InternalServerError,
        anthropic.OverloadedError,
        anthropic.APIConnectionError,
    ):
        if max_attempts > 1:
            return create_message_with_fast_fallback(
                max_attempts=max_attempts - 1, **params
            )
        raise


message = create_message_with_fast_fallback(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    betas=["fast-mode-2026-02-01"],
    speed="fast",
    max_retries=0,
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function createMessageWithFastFallback(
  params: Anthropic.Beta.MessageCreateParams,
  requestOptions?: Anthropic.RequestOptions,
  maxAttempts: number = 3
): Promise<Anthropic.Beta.Message> {
  try {
    return await client.beta.messages.create(params, requestOptions);
  } catch (e) {
    if (e instanceof Anthropic.RateLimitError && params.speed === "fast") {
      const { speed, ...rest } = params;
      return createMessageWithFastFallback(rest);
    }
    if (
      e instanceof Anthropic.InternalServerError ||
      e instanceof Anthropic.APIConnectionError
    ) {
      if (maxAttempts > 1) {
        return createMessageWithFastFallback(params, requestOptions, maxAttempts - 1);
      }
    }
    throw e;
  }
}

const message = await createMessageWithFastFallback(
  {
    model: "claude-opus-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
    betas: ["fast-mode-2026-02-01"],
    speed: "fast"
  },
  { maxRetries: 0 }
);
```

```go Go
package main

import (
	"context"
	"errors"

	anthropic "github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func createMessageWithFastFallback(
	ctx context.Context,
	client *anthropic.Client,
	params anthropic.BetaMessageNewParams,
	maxAttempts int,
	opts ...option.RequestOption,
) (*anthropic.BetaMessage, error) {
	message, err := client.Beta.Messages.New(ctx, params, opts...)
	if err != nil {
		var apierr *anthropic.Error
		if errors.As(err, &apierr) && apierr.StatusCode == 429 && params.Speed != "" {
			params.Speed = ""
			return createMessageWithFastFallback(ctx, client, params, maxAttempts)
		}
		if (errors.As(err, &apierr) && apierr.StatusCode >= 500) || !errors.As(err, &apierr) {
			if maxAttempts > 1 {
				return createMessageWithFastFallback(ctx, client, params, maxAttempts-1)
			}
		}
		return nil, err
	}
	return message, nil
}
```

```ruby Ruby
require "anthropic"

anthropic = Anthropic::Client.new

def create_message_with_fast_fallback(client, request_options: {}, max_attempts: 3, **params)
  client.beta.messages.create(**params, request_options: request_options)
rescue Anthropic::Errors::RateLimitError
  raise unless params[:speed] == "fast"
  params.delete(:speed)
  create_message_with_fast_fallback(client, **params)
rescue Anthropic::Errors::InternalServerError, Anthropic::Errors::APIConnectionError
  raise unless max_attempts > 1
  create_message_with_fast_fallback(client, request_options: request_options, max_attempts: max_attempts - 1, **params)
end

message = create_message_with_fast_fallback(
  anthropic,
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
  betas: ["fast-mode-2026-02-01"],
  speed: "fast",
  request_options: { max_retries: 0 }
)
```
</CodeGroup>

## Pertimbangan

- **Prompt caching**: Beralih antara kecepatan cepat dan standar membatalkan cache prompt. Permintaan pada kecepatan berbeda tidak berbagi awalan yang di-cache.
- **Model yang didukung**: Mode cepat saat ini didukung hanya pada Opus 4.6. Mengirim `speed: "fast"` dengan model yang tidak didukung mengembalikan kesalahan.
- **TTFT**: Manfaat mode cepat berfokus pada token output per detik (OTPS), bukan waktu ke token pertama (TTFT).
- **Batch API**: Mode cepat tidak tersedia dengan [Batch API](/docs/id/build-with-claude/batch-processing).
- **Priority Tier**: Mode cepat tidak tersedia dengan [Priority Tier](/docs/id/api/service-tiers).

## Langkah berikutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="/docs/id/about-claude/pricing#fast-mode-pricing">
    Lihat informasi harga mode cepat yang terperinci.
  </Card>
  <Card title="Batas laju" icon="gauge" href="/docs/id/api/rate-limits">
    Periksa tingkat batas laju untuk mode cepat.
  </Card>
  <Card title="Parameter effort" icon="sliders" href="/docs/id/build-with-claude/effort">
    Kontrol penggunaan token dengan parameter effort.
  </Card>
</CardGroup>