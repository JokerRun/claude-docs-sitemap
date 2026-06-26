---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 08855bf63db9835b039185adc6fc6f31b333884213856fd57f1be2da18f71de1
---

# Fast mode (pratinjau riset)

Dapatkan hingga 2,5x lebih banyak token output per detik dari model Claude Opus.

---

Fast mode menghasilkan hingga 2,5x lebih banyak token output per detik dari Claude Opus 4.8, Claude Opus 4.7, dan Claude Opus 4.6 dengan harga premium. Tetapkan `speed: "fast"` bersama header beta `fast-mode-2026-02-01` pada permintaan Anda untuk mengaktifkannya.

<Note>
Fast mode berada dalam tahap pratinjau riset. Hubungi manajer akun Anda untuk meminta akses. Jika Anda tidak memiliki manajer akun, [bergabunglah dengan daftar tunggu](https://claude.com/fast-mode) untuk fast mode.
</Note>

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Model yang didukung \{#supported-models}

Fast mode didukung pada model berikut:

- Claude Opus 4.8 (claude-opus-4-8)
- Claude Opus 4.7 (claude-opus-4-7)
- Claude Opus 4.6 (claude-opus-4-6)

<Note>
Fast mode untuk Claude Opus 4.8 diluncurkan sebagai pratinjau riset hanya di Claude API, termasuk [Claude Managed Agents](/docs/id/managed-agents/overview). Fitur ini tidak tersedia di platform pihak ketiga, termasuk Vertex AI, Amazon Bedrock, dan Microsoft Foundry.
</Note>

<Warning>
Fast mode untuk Claude Opus 4.6 tidak digunakan lagi (deprecated) sejak peluncuran Claude Opus 4.8 dan akan dihapus sekitar 30 hari setelahnya. Setelah dihapus, permintaan ke `claude-opus-4-6` dengan `speed: "fast"` akan kembali ke kecepatan standar dengan harga standar alih-alih mengembalikan error. Migrasikan ke fast mode untuk Claude Opus 4.8 atau Claude Opus 4.7 untuk mempertahankan peningkatan kecepatan.
</Warning>

## Cara kerja fast mode \{#how-fast-mode-works}

Fast mode menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

- Hingga 2,5x lebih banyak token output per detik dibandingkan kecepatan standar
- Manfaat kecepatan berfokus pada "output tokens per second" (token output per detik), atau OTPS, bukan "time to first token" (waktu hingga token pertama), atau TTFT
- Bobot dan perilaku model yang sama (bukan model yang berbeda)
- Kompatibel dengan [streaming](/docs/id/build-with-claude/streaming), di mana peningkatan OTPS paling terlihat

## Penggunaan dasar \{#basic-usage}

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: fast-mode-2026-02-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
        "max_tokens": 4096,
        "speed": "fast",
        "messages": [{
            "role": "user",
            "content": "Refactor this module to use dependency injection"
        }]
    }'
```

```bash CLI
ant beta:messages create \
  --beta fast-mode-2026-02-01 \
  --transform 'content.0.text' \
  --raw-output <<'YAML'
model: claude-opus-4-8
max_tokens: 4096
speed: fast
messages:
  - role: user
    content: Refactor this module to use dependency injection
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[
        {"role": "user", "content": "Refactor this module to use dependency injection"}
    ],
)

print(response.content[0].text)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 4096,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [
    {
      role: "user",
      content: "Refactor this module to use dependency injection"
    }
  ]
});

const textBlock = response.content.find(
  (block): block is Anthropic.Beta.Messages.BetaTextBlock => block.type === "text"
);
console.log(textBlock?.text);
```

```csharp C# hidelines={1..5}
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-8",
    MaxTokens = 4096,
    Speed = Speed.Fast,
    Betas = ["fast-mode-2026-02-01"],
    Messages = [
        new() { Role = Role.User, Content = "Refactor this module to use dependency injection" }
    ],
});

Console.WriteLine(response);
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	anthropic "github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 4096,
		Speed:     anthropic.BetaMessageNewParamsSpeedFast,
		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Refactor this module to use dependency injection")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content[0].AsText().Text)
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    BetaMessage response = client.beta().messages().create(
            MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_8)
                    .maxTokens(4096L)
                    .speed(MessageCreateParams.Speed.FAST)
                    .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                    .addUserMessage("Refactor this module to use dependency injection")
                    .build());

    IO.println(response.content().get(0).text().get().text());
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->beta->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 4096,
    speed: 'fast',
    betas: ['fast-mode-2026-02-01'],
    messages: [
        ['role' => 'user', 'content' => 'Refactor this module to use dependency injection'],
    ],
);

echo $response->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 4096,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{role: "user", content: "Refactor this module to use dependency injection"}]
)

puts response.content[0].text
```

</CodeGroup>

## Harga \{#pricing}

Fast mode dihargai dengan pengali per model atas tarif standar di seluruh jendela konteks, termasuk permintaan dengan lebih dari 200k token input. Tabel berikut menunjukkan harga fast mode untuk setiap model yang didukung:

| Model | Input | Output |
|:------|:------|:-------|
| Claude Opus 4.8 | $10 / MTok | $50 / MTok |
| Claude Opus 4.7 / Claude Opus 4.6 | $30 / MTok | $150 / MTok |

Harga fast mode berlaku kumulatif dengan pengubah harga lainnya:

- [Pengali caching prompt](/docs/id/about-claude/pricing#prompt-caching) berlaku di atas harga fast mode
- Pengali [residensi data](/docs/id/manage-claude/data-residency) berlaku di atas harga fast mode

Untuk detail harga lengkap, lihat [halaman harga](/docs/id/about-claude/pricing#fast-mode-pricing).

## Batas laju \{#rate-limits}

Fast mode memiliki batas laju khusus yang terpisah dari batas laju Opus standar. Ketika batas laju fast mode Anda terlampaui, API mengembalikan error `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Respons menyertakan header yang menunjukkan status batas laju fast mode Anda:

| Header | Deskripsi |
|:-------|:------------|
| `anthropic-fast-input-tokens-limit` | Token input fast mode maksimum per menit |
| `anthropic-fast-input-tokens-remaining` | Token input fast mode yang tersisa |
| `anthropic-fast-input-tokens-reset` | Waktu ketika batas token input fast mode direset |
| `anthropic-fast-output-tokens-limit` | Token output fast mode maksimum per menit |
| `anthropic-fast-output-tokens-remaining` | Token output fast mode yang tersisa |
| `anthropic-fast-output-tokens-reset` | Waktu ketika batas token output fast mode direset |

Untuk batas laju spesifik per tier, lihat [halaman batas laju](/docs/id/api/rate-limits).

## Memeriksa kecepatan mana yang digunakan \{#checking-which-speed-was-used}

Objek `usage` dalam respons menyertakan field `speed` yang menunjukkan kecepatan mana yang digunakan, baik `"fast"` atau `"standard"`. Fast mode tidak secara diam-diam kembali ke kecepatan standar saat terjadi batas laju atau masalah kapasitas (Anda akan mendapatkan `429` atau `529` sebagai gantinya), jadi ketika Anda meminta `speed: "fast"` pada model yang didukung, `usage.speed` adalah `"fast"`.

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: fast-mode-2026-02-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-8",
        "max_tokens": 1024,
        "speed": "fast",
        "messages": [{"role": "user", "content": "Hello"}]
    }'
```

```bash CLI
ant beta:messages create \
  --beta fast-mode-2026-02-01 \
  --transform usage.speed \
  --raw-output <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
speed: fast
messages:
  - role: user
    content: Hello
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.usage.speed)  # "fast" or "standard"
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{ role: "user", content: "Hello" }]
});

console.log(response.usage.speed); // "fast" or "standard"
```

```csharp C# hidelines={1..5}
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-8",
    MaxTokens = 1024,
    Speed = Speed.Fast,
    Betas = ["fast-mode-2026-02-01"],
    Messages = [new() { Role = Role.User, Content = "Hello" }],
});

Console.WriteLine(response.Usage.Speed);  // "fast" or "standard"
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	anthropic "github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Speed:     anthropic.BetaMessageNewParamsSpeedFast,
		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Usage.Speed) // "fast" or "standard"
}
```

```java Java hidelines={1..8,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .speed(MessageCreateParams.Speed.FAST)
            .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
            .addUserMessage("Hello")
            .build();

    BetaMessage response = client.beta().messages().create(params);
    IO.println(response.usage().speed());  // "fast" or "standard"
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->beta->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    speed: 'fast',
    betas: ['fast-mode-2026-02-01'],
    messages: [['role' => 'user', 'content' => 'Hello']],
);

echo $response->usage->speed;  // "fast" or "standard"
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{ role: "user", content: "Hello" }]
)

puts(response.usage.speed)  # "fast" or "standard"
```
</CodeGroup>

```json Output hidelines={5..8}
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [{ "type": "text", "text": "Hello!" }],
  "model": "claude-opus-4-8",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 8,
    "output_tokens": 12,
    "speed": "fast"
  }
}
```

Untuk melacak penggunaan dan biaya fast mode di seluruh organisasi Anda, lihat [Usage and Cost API](/docs/id/manage-claude/usage-cost-api).

## Percobaan ulang dan fallback \{#retries-and-fallback}

### Percobaan ulang otomatis \{#automatic-retries}

Ketika batas laju fast mode terlampaui, API mengembalikan error `429` dengan header `retry-after`. SDK Anthropic secara otomatis mencoba ulang permintaan ini hingga 2 kali secara default (dapat dikonfigurasi dengan `max_retries`), menunggu selama penundaan yang ditentukan server sebelum setiap percobaan ulang. Karena fast mode menggunakan pengisian ulang token secara kontinu, penundaan `retry-after` biasanya singkat dan permintaan berhasil setelah kapasitas tersedia.

### Kembali ke kecepatan standar \{#falling-back-to-standard-speed}

Jika Anda lebih memilih untuk kembali ke kecepatan standar daripada menunggu kapasitas fast mode, tangkap error batas laju dan coba ulang tanpa `speed: "fast"`. Tetapkan `max_retries` ke `0` pada permintaan fast awal untuk melewati percobaan ulang otomatis dan langsung gagal pada error batas laju.

<Note>
Kembali dari kecepatan fast ke standar akan menghasilkan cache miss pada [caching prompt](/docs/id/build-with-claude/prompt-caching). Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
</Note>

Karena menetapkan `max_retries` ke `0` juga menonaktifkan percobaan ulang untuk error sementara lainnya (overloaded, internal server error), contoh berikut mengirim ulang permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup>
```bash CLI
# `ant` mencoba ulang 429/5xx secara otomatis dan tidak punya override max_retries per permintaan,
# jadi pada 429 mode cepat, fallback berjalan setelah percobaan ulang bawaan
# habis. --transform-error menampilkan error.type untuk percabangan.
create_message_with_fast_fallback() {
  local speed="$1" max_attempts="${2:-3}" body out
  body=${3:-$(cat)}
  out=$(
    ant beta:messages create --beta fast-mode-2026-02-01 \
      ${speed:+--speed "$speed"} \
      --transform-error error.type --format-error yaml <<<"$body" 2>/dev/null
  ) && { printf '%s\n' "$out"; return; }
  case "$out" in
    rate_limit_error)
      if [[ -n "$speed" ]]; then
        create_message_with_fast_fallback "" "$max_attempts" "$body"
        return
      fi ;;
    overloaded_error | api_error | "")
      if (( max_attempts > 1 )); then
        create_message_with_fast_fallback "$speed" $((max_attempts - 1)) "$body"
        return
      fi ;;
  esac
  printf '%s\n' "${out:-connection_error}" >&2
  return 1
}

MESSAGE=$(
  create_message_with_fast_fallback fast <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content: Hello
YAML
)
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()


def create_message_with_fast_fallback(max_retries=0, max_attempts=3, **params):
    try:
        return client.with_options(max_retries=max_retries).beta.messages.create(
            **params
        )
    except anthropic.RateLimitError:
        if params.get("speed") == "fast":
            del params["speed"]
            return create_message_with_fast_fallback(max_retries=max_retries, **params)
        raise
    except (
        anthropic.APIStatusError,
        anthropic.APIConnectionError,
    ) as error:
        if isinstance(error, anthropic.APIStatusError) and error.status_code < 500:
            raise
        if max_attempts > 1:
            return create_message_with_fast_fallback(
                max_retries=max_retries, max_attempts=max_attempts - 1, **params
            )
        raise


message = create_message_with_fast_fallback(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    betas=["fast-mode-2026-02-01"],
    speed="fast",
    max_retries=0,
)
```

```typescript TypeScript hidelines={1..3,-1}
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
(async () => {
  async function createMessageWithFastFallback(
    params: Anthropic.Beta.MessageCreateParams,
    requestOptions?: Anthropic.RequestOptions,
    maxAttempts: number = 3
  ): Promise<Anthropic.Beta.Messages.BetaMessage> {
    try {
      return (await client.beta.messages.create(
        params,
        requestOptions
      )) as Anthropic.Beta.Messages.BetaMessage;
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
          return createMessageWithFastFallback(params, undefined, maxAttempts - 1);
        }
      }
      throw e;
    }
  }

  const message = await createMessageWithFastFallback(
    {
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello" }],
      betas: ["fast-mode-2026-02-01"],
      speed: "fast"
    },
    { maxRetries: 0 }
  );
})();
```

```csharp C# hidelines={1..6}
using Anthropic;
using Anthropic.Exceptions;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

async Task<BetaMessage> CreateMessageWithFastFallback(
    MessageCreateParams parameters,
    int? maxRetries = null,
    int maxAttempts = 3)
{
    try
    {
        var requestClient = maxRetries is int retries
            ? client.WithOptions(options => options with { MaxRetries = retries })
            : client;
        return await requestClient.Beta.Messages.Create(parameters);
    }
    catch (AnthropicRateLimitException)
    {
        if (parameters.Speed is not null)
        {
            return await CreateMessageWithFastFallback(
                parameters with { Speed = null });
        }
        throw;
    }
    catch (Anthropic5xxException)
    {
        if (maxAttempts > 1)
        {
            return await CreateMessageWithFastFallback(
                parameters, maxAttempts: maxAttempts - 1);
        }
        throw;
    }
}

var message = await CreateMessageWithFastFallback(
    new MessageCreateParams
    {
        Model = "claude-opus-4-8",
        MaxTokens = 1024,
        Messages = [new() { Role = Role.User, Content = "Hello" }],
        Betas = ["fast-mode-2026-02-01"],
        Speed = Speed.Fast,
    },
    maxRetries: 0);
```

```go Go hidelines={1..11}
package main

import (
	"context"
	"errors"
	"fmt"

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

func main() {
	client := anthropic.NewClient()
	message, err := createMessageWithFastFallback(
		context.TODO(),
		&client,
		anthropic.BetaMessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 1024,
			Messages: []anthropic.BetaMessageParam{
				anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
			},
			Speed: "fast",
			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
		},
		3,
		option.WithMaxRetries(0),
	)
	if err != nil {
		panic(err)
	}
	fmt.Println(message)
}
```

```java Java hidelines={1..2,5..10}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.errors.InternalServerException;
import com.anthropic.errors.RateLimitException;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import java.util.Optional;

// Nonaktifkan auto-retry SDK agar logika fallback di bawah yang menanganinya
AnthropicClient client =
        AnthropicOkHttpClient.builder().fromEnv().maxRetries(0).build();

BetaMessage createMessageWithFastFallback(
        MessageCreateParams params, int maxAttempts) {
    try {
        return client.beta().messages().create(params);
    } catch (RateLimitException e) {
        if (params.speed().isPresent()) {
            MessageCreateParams retryParams = params.toBuilder()
                    .speed(Optional.empty())
                    .build();
            return createMessageWithFastFallback(retryParams, maxAttempts);
        }
        throw e;
    } catch (InternalServerException e) {
        if (maxAttempts > 1) {
            return createMessageWithFastFallback(params, maxAttempts - 1);
        }
        throw e;
    }
}

void main() {
    BetaMessage message = createMessageWithFastFallback(
            MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_8)
                    .maxTokens(1024L)
                    .addUserMessage("Hello")
                    .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                    .speed(MessageCreateParams.Speed.FAST)
                    .build(),
            3);
    IO.println(message.content().get(0).text().get().text());
}
```

```php PHP hidelines={1..3,8}
<?php

use Anthropic\Client;
use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\InternalServerException;
use Anthropic\Core\Exceptions\RateLimitException;
use Anthropic\RequestOptions;

$client = new Client();

function createMessageWithFastFallback(
    Client $client,
    array $params,
    ?RequestOptions $requestOptions = null,
    int $maxAttempts = 3,
) {
    try {
        return $client->beta->messages->create(
            ...$params,
            requestOptions: $requestOptions,
        );
    } catch (RateLimitException $e) {
        if (isset($params['speed'])) {
            unset($params['speed']);
            return createMessageWithFastFallback($client, $params);
        }
        throw $e;
    } catch (InternalServerException | APIConnectionException $e) {
        if ($maxAttempts > 1) {
            return createMessageWithFastFallback(
                $client, $params, maxAttempts: $maxAttempts - 1
            );
        }
        throw $e;
    }
}

$message = createMessageWithFastFallback(
    $client,
    [
        'model' => 'claude-opus-4-8',
        'maxTokens' => 1024,
        'messages' => [['role' => 'user', 'content' => 'Hello']],
        'betas' => ['fast-mode-2026-02-01'],
        'speed' => 'fast',
    ],
    RequestOptions::with(maxRetries: 0),
);
```

```ruby Ruby nocheck hidelines={1..2}
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
  create_message_with_fast_fallback(client, max_attempts: max_attempts - 1, **params)
end

message = create_message_with_fast_fallback(
  anthropic,
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
  betas: ["fast-mode-2026-02-01"],
  speed: "fast",
  request_options: { max_retries: 0 }
)
```
</CodeGroup>

## Pertimbangan \{#considerations}

- **Caching prompt:** Beralih antara kecepatan fast dan standar membatalkan cache prompt. Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
- **Model yang didukung:** Fast mode didukung pada Claude Opus 4.8, Claude Opus 4.7, dan Claude Opus 4.6. Mengirim `speed: "fast"` dengan model yang tidak didukung akan mengembalikan error.
- **TTFT:** Manfaat fast mode berfokus pada token output per detik (OTPS), bukan waktu hingga token pertama (TTFT).
- **Batch API:** Fast mode tidak tersedia dengan [Batch API](/docs/id/build-with-claude/batch-processing).
- **Priority Tier:** Fast mode tidak tersedia dengan [Priority Tier](/docs/id/api/service-tiers).
- **Claude Platform on AWS:** Fast mode saat ini tidak tersedia di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws).

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Output terstruktur" icon="code-brackets" href="/docs/id/build-with-claude/structured-outputs">
    Dapatkan hasil JSON yang tervalidasi dari alur kerja agen.
  </Card>
  <Card title="Harga" icon="calculator" href="/docs/id/about-claude/pricing#fast-mode-pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>
  <Card title="Effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara kelengkapan respons dan efisiensi token.
  </Card>
  <Card title="Streaming pesan" icon="arrow-right" href="/docs/id/build-with-claude/streaming">
    Stream respons Messages API secara inkremental dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>