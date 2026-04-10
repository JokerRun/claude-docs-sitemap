---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 23187ddd43cdb71224cf111b5144e936226037eef4d96c4a91ec09270c7f3e48
---

# Mode cepat (beta: pratinjau penelitian)

Kecepatan keluaran lebih tinggi untuk Claude Opus 4.6, memberikan pembuatan token yang jauh lebih cepat untuk alur kerja yang sensitif terhadap latensi dan agentic.

---

Mode cepat menyediakan pembuatan token keluaran yang jauh lebih cepat untuk Claude Opus 4.6. Dengan mengatur `speed: "fast"` dalam permintaan API Anda, Anda mendapatkan hingga 2,5x token keluaran per detik yang lebih tinggi dari model yang sama dengan harga premium.

<Note>
Mode cepat sedang dalam beta (pratinjau penelitian). [Bergabunglah dengan daftar tunggu](https://claude.com/fast-mode) untuk meminta akses. Ketersediaan terbatas saat Anthropic mengumpulkan umpan balik.
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Model yang didukung

Mode cepat didukung pada model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`)

## Cara kerja mode cepat

Mode cepat menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

- Hingga 2,5x token keluaran per detik yang lebih tinggi dibandingkan dengan kecepatan standar
- Manfaat kecepatan berfokus pada token keluaran per detik (OTPS), bukan waktu ke token pertama (TTFT)
- Bobot dan perilaku model yang sama (bukan model yang berbeda)

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

```bash CLI
ant beta:messages create \
  --beta fast-mode-2026-02-01 \
  --transform 'content.0.text' --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
speed: fast
messages:
  - role: user
    content: Refactor this module to use dependency injection
YAML
```

```python Python nocheck hidelines={1..2}
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

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
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
    Model = "claude-opus-4-6",
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class FastModeExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        BetaMessage response = client.beta().messages().create(
                MessageCreateParams.builder()
                        .model(Model.CLAUDE_OPUS_4_6)
                        .maxTokens(4096L)
                        .speed(MessageCreateParams.Speed.FAST)
                        .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                        .addUserMessage("Refactor this module to use dependency injection")
                        .build());

        System.out.println(response.content().get(0).text().get().text());
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->beta->messages->create(
    model: 'claude-opus-4-6',
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
  model: "claude-opus-4-6",
  max_tokens: 4096,
  speed: "fast",
  betas: ["fast-mode-2026-02-01"],
  messages: [{role: "user", content: "Refactor this module to use dependency injection"}]
)

puts response.content[0].text
```

</CodeGroup>

## Harga

Mode cepat dihargai pada 6x tarif Opus standar di seluruh jendela konteks, termasuk permintaan di atas 200k token input. Tabel berikut menunjukkan harga untuk Claude Opus 4.6 dengan mode cepat:

| Input | Output |
|:------|:-------|
| $30 / MTok | $150 / MTok |

Harga mode cepat ditumpuk dengan pengubah harga lainnya:

- [Pengganda caching prompt](/docs/id/about-claude/pricing#model-pricing) berlaku di atas harga mode cepat
- [Residensi data](/docs/id/build-with-claude/data-residency) pengganda berlaku di atas harga mode cepat

Untuk detail harga lengkap, lihat [halaman harga](/docs/id/about-claude/pricing#fast-mode-pricing).

## Batas laju

Mode cepat memiliki batas laju khusus yang terpisah dari batas laju Opus standar. Ketika batas laju mode cepat Anda terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Respons mencakup header yang menunjukkan status batas laju mode cepat Anda:

| Header | Deskripsi |
|:-------|:----------|
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
```

```bash CLI
ant beta:messages create --beta fast-mode-2026-02-01 \
  --transform usage.speed --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
speed: fast
messages:
  - role: user
    content: Hello
YAML
```

```python Python nocheck
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

```csharp C# hidelines={1..5}
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-6",
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class FastModeUsage {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_6)
                .maxTokens(1024L)
                .speed(MessageCreateParams.Speed.FAST)
                .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                .addUserMessage("Hello")
                .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response.usage().speed());  // "fast" or "standard"
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->beta->messages->create(
    model: 'claude-opus-4-6',
    maxTokens: 1024,
    speed: 'fast',
    betas: ['fast-mode-2026-02-01'],
    messages: [['role' => 'user', 'content' => 'Hello']],
);

echo $response->usage->speed;  // "fast" or "standard"
```

```ruby Ruby nocheck
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

```json Output hidelines={5..8}
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [{ "type": "text", "text": "Hello!" }],
  "model": "claude-opus-4-6",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 523,
    "output_tokens": 1842,
    "speed": "fast"
  }
}
```

Untuk melacak penggunaan mode cepat dan biaya di seluruh organisasi Anda, lihat [API Penggunaan dan Biaya](/docs/id/build-with-claude/usage-cost-api).

## Percobaan ulang dan fallback

### Percobaan ulang otomatis

Ketika batas laju mode cepat terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after`. SDK Anthropic secara otomatis mencoba ulang permintaan ini hingga 2 kali secara default (dapat dikonfigurasi melalui `max_retries`), menunggu penundaan yang ditentukan server sebelum setiap percobaan ulang. Karena mode cepat menggunakan pengisian ulang token berkelanjutan, penundaan `retry-after` biasanya singkat dan permintaan berhasil setelah kapasitas tersedia.

### Jatuh kembali ke kecepatan standar

Jika Anda lebih suka jatuh kembali ke kecepatan standar daripada menunggu kapasitas mode cepat, tangkap kesalahan batas laju dan coba ulang tanpa `speed: "fast"`. Atur `max_retries` ke `0` pada permintaan cepat awal untuk melewati percobaan ulang otomatis dan gagal segera pada kesalahan batas laju.

<Note>
Jatuh kembali dari kecepatan cepat ke standar akan menghasilkan [cache prompt](/docs/id/build-with-claude/prompt-caching) miss. Permintaan pada kecepatan berbeda tidak berbagi awalan yang di-cache.
</Note>

Karena mengatur `max_retries` ke `0` juga menonaktifkan percobaan ulang untuk kesalahan transien lainnya (kelebihan beban, kesalahan server internal), contoh di bawah mengeluarkan kembali permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup>
```bash CLI
# `ant` retries 429/5xx automatically and has no per-request max_retries
# override, so on a fast-mode 429 the fallback runs after the built-in
# retries exhaust. --transform-error surfaces error.type for branching.
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
model: claude-opus-4-6
max_tokens: 1024
messages:
  - role: user
    content: Hello
YAML
)
```

```python Python nocheck hidelines={1..2}
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
      model: "claude-opus-4-6",
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
            ? client.WithOptions(o => o with { MaxRetries = retries })
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
        Model = "claude-opus-4-6",
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
			Model:     anthropic.ModelClaudeOpus4_6,
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

```java Java hidelines={1..2,5..11,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.errors.InternalServerException;
import com.anthropic.errors.RateLimitException;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import java.util.Optional;

public class FastModeFallback {
    // Disable SDK auto-retry so the fallback logic below handles it
    static AnthropicClient client =
            AnthropicOkHttpClient.builder().fromEnv().maxRetries(0).build();

    static BetaMessage createMessageWithFastFallback(
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

    public static void main(String[] args) {
        BetaMessage message = createMessageWithFastFallback(
                MessageCreateParams.builder()
                        .model(Model.CLAUDE_OPUS_4_6)
                        .maxTokens(1024L)
                        .addUserMessage("Hello")
                        .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                        .speed(MessageCreateParams.Speed.FAST)
                        .build(),
                3);
    }
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
        'model' => 'claude-opus-4-6',
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

- **Caching prompt:** Beralih antara kecepatan cepat dan standar membatalkan cache prompt. Permintaan pada kecepatan berbeda tidak berbagi awalan yang di-cache.
- **Model yang didukung:** Mode cepat saat ini didukung hanya pada Opus 4.6. Mengirim `speed: "fast"` dengan model yang tidak didukung mengembalikan kesalahan.
- **TTFT:** Manfaat mode cepat berfokus pada token keluaran per detik (OTPS), bukan waktu ke token pertama (TTFT).
- **Batch API:** Mode cepat tidak tersedia dengan [Batch API](/docs/id/build-with-claude/batch-processing).
- **Priority Tier:** Mode cepat tidak tersedia dengan [Priority Tier](/docs/id/api/service-tiers).

## Langkah berikutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="/docs/id/about-claude/pricing#fast-mode-pricing">
    Lihat informasi harga mode cepat yang terperinci.
  </Card>
  <Card title="Batas laju" icon="gauge" href="/docs/id/api/rate-limits">
    Periksa tingkat batas laju untuk mode cepat.
  </Card>
  <Card title="Parameter usaha" icon="sliders" href="/docs/id/build-with-claude/effort">
    Kontrol penggunaan token dengan parameter usaha.
  </Card>
</CardGroup>