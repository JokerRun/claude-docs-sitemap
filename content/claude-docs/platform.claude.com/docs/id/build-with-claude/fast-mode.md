---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 4f232d6d079a17a431b08af05ccb47178f814d69337d4157f98afdc148c8d864
---

# Mode cepat (pratinjau riset)

Dapatkan hingga 2,5x lebih banyak token output per detik dari model Claude Opus yang didukung.

---

Mode cepat (fast mode) menghasilkan hingga 2,5x lebih banyak token output per detik dari Claude Opus 4.8 dan Claude Opus 4.7 dengan harga premium. Atur `speed: "fast"` dengan header beta `fast-mode-2026-02-01` pada permintaan Anda untuk ikut serta.

<Note>
  Mode cepat berada dalam pratinjau riset. Hubungi manajer akun Anda untuk meminta akses. Jika Anda tidak memiliki manajer akun, [bergabunglah dengan daftar tunggu](https://claude.com/fast-mode) untuk mode cepat.
</Note>

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Model yang didukung

Mode cepat didukung pada model-model berikut:

* Claude Opus 4.8 (claude-opus-4-8)
* Claude Opus 4.7 (claude-opus-4-7)

<Note>
  Mode cepat untuk Claude Opus 4.8 diluncurkan sebagai pratinjau riset hanya di Claude API, termasuk [Claude Managed Agents](/docs/id/managed-agents/overview). Mode ini tidak tersedia di Amazon Bedrock, Google Cloud, atau Microsoft Foundry.
</Note>

<Warning>
  Mode cepat untuk Claude Opus 4.7 tidak digunakan lagi (deprecated) sejak 25 Juni 2026, dan akan dihapus pada 24 Juli 2026. Setelah penghapusan, permintaan ke `claude-opus-4-7` dengan `speed: "fast"` akan mengembalikan error; tidak seperti Claude Opus 4.6 (lihat catatan berikut), Claude Opus 4.7 tidak beralih kembali ke kecepatan standar. Model itu sendiri tetap tersedia pada kecepatan standar. Untuk terus menggunakan mode cepat, migrasikan ke Claude Opus 4.8.
</Warning>

<Note>
  Sejak 29 Juni 2026, mode cepat tidak tersedia di Claude Opus 4.6. Permintaan ke `claude-opus-4-6` dengan `speed: "fast"` tidak mengembalikan error: permintaan tersebut berjalan pada kecepatan standar dan ditagih dengan [tarif standar](/docs/id/about-claude/pricing) alih-alih tarif premium mode cepat, dan respons melaporkan [`usage.speed: "standard"`](#checking-which-speed-was-used). Untuk terus menggunakan mode cepat, migrasikan ke [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide).
</Note>

## Cara kerja mode cepat

Mode cepat menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

* Hingga 2,5x lebih banyak token output per detik dibandingkan dengan kecepatan standar
* Manfaat kecepatan berfokus pada "output tokens per second" (token output per detik), atau OTPS, bukan "time to first token" (waktu hingga token pertama), atau TTFT
* Bobot dan perilaku model yang sama (bukan model yang berbeda)
* Kompatibel dengan [streaming](/docs/id/build-with-claude/streaming), di mana peningkatan OTPS paling terlihat

## Penggunaan dasar

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fast-mode-2026-02-01" \
    -H "content-type: application/json" \
    -d '{
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

  ```python Python
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

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
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
  ```

  ```php PHP
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

  ```ruby Ruby
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

## Harga

Mode cepat dihargai dengan pengali per model atas tarif standar di seluruh jendela konteks, termasuk permintaan dengan lebih dari 200k token input. Tabel berikut menunjukkan harga mode cepat untuk setiap model yang didukung:

| Model           | Input          | Output          |
| --------------- | -------------- | --------------- |
| Claude Opus 4.8 | $10 USD / MTok | $50 USD / MTok  |
| Claude Opus 4.7 | $30 USD / MTok | $150 USD / MTok |

Harga mode cepat digabungkan dengan pengubah harga lainnya:

* [Pengali caching prompt](/docs/id/about-claude/pricing#prompt-caching) berlaku di atas harga mode cepat
* Pengali [residensi data](/docs/id/manage-claude/data-residency) berlaku di atas harga mode cepat

Untuk detail harga lengkap, lihat halaman [Harga](/docs/id/about-claude/pricing#fast-mode-pricing).

## Batas laju

Mode cepat memiliki batas laju (rate limit) khusus yang terpisah dari batas laju Opus standar. Ketika batas laju mode cepat Anda terlampaui, API mengembalikan error `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Respons menyertakan header yang menunjukkan status batas laju mode cepat Anda:

| Header                                   | Deskripsi                                          |
| ---------------------------------------- | -------------------------------------------------- |
| `anthropic-fast-input-tokens-limit`      | Maksimum token input mode cepat per menit          |
| `anthropic-fast-input-tokens-remaining`  | Sisa token input mode cepat                        |
| `anthropic-fast-input-tokens-reset`      | Waktu ketika batas token input mode cepat direset  |
| `anthropic-fast-output-tokens-limit`     | Maksimum token output mode cepat per menit         |
| `anthropic-fast-output-tokens-remaining` | Sisa token output mode cepat                       |
| `anthropic-fast-output-tokens-reset`     | Waktu ketika batas token output mode cepat direset |

Untuk batas laju spesifik per tingkat, lihat halaman [Batas laju](/docs/id/api/rate-limits).

## Memeriksa kecepatan yang digunakan

Objek `usage` pada respons menyertakan field `speed` yang menunjukkan kecepatan mana yang digunakan, baik `"fast"` atau `"standard"`. Pada model yang didukung, mode cepat tidak secara diam-diam beralih kembali ke kecepatan standar saat terkena batas laju atau keterbatasan kapasitas (Anda akan mendapatkan `429` atau `529` sebagai gantinya), jadi ketika Anda meminta `speed: "fast"` pada Claude Opus 4.8 atau Claude Opus 4.7, `usage.speed` adalah `"fast"`. Pada Claude Opus 4.6, di mana mode cepat [tidak tersedia](#supported-models), permintaan dengan `speed: "fast"` berjalan pada kecepatan standar dan mengembalikan `usage.speed: "standard"`. Periksa field ini untuk mengonfirmasi kecepatan mana yang melayani suatu permintaan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fast-mode-2026-02-01" \
    -H "content-type: application/json" \
    -d '{
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

  ```python Python
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

  ```typescript TypeScript
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

  ```csharp C#
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

  ```go Go
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
  ```

  ```java Java
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
  ```

  ```php PHP
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

  ```ruby Ruby
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

```json Output
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
// ...
  "usage": {
    "input_tokens": 8,
    "output_tokens": 12,
    "speed": "fast"
  }
}
```

Untuk melacak penggunaan dan biaya mode cepat di seluruh organisasi Anda, lihat [Usage and Cost API](/docs/id/manage-claude/usage-cost-api).

## Percobaan ulang dan fallback

### Percobaan ulang otomatis

Ketika batas laju mode cepat terlampaui, API mengembalikan error `429` dengan header `retry-after`. SDK Anthropic secara otomatis mencoba ulang permintaan ini hingga 2 kali secara default (dapat dikonfigurasi dengan `max_retries`), menunggu penundaan yang ditentukan server sebelum setiap percobaan ulang. Karena mode cepat menggunakan pengisian ulang token secara berkelanjutan, penundaan `retry-after` biasanya singkat dan permintaan berhasil begitu kapasitas tersedia.

### Beralih kembali ke kecepatan standar

<Note>
  Bagian ini membahas fallback sisi klien yang bersifat opt-in ketika mode cepat terkena batas laju. Ini terpisah dari perilaku pada [Claude Opus 4.6](#supported-models), di mana mode cepat tidak tersedia dan permintaan berjalan pada kecepatan standar secara otomatis.
</Note>

Jika Anda lebih memilih untuk beralih kembali ke kecepatan standar daripada menunggu kapasitas mode cepat, tangkap error batas laju dan coba ulang tanpa `speed: "fast"`. Atur `max_retries` ke `0` pada permintaan cepat awal untuk melewati percobaan ulang otomatis dan langsung gagal pada error batas laju.

<Note>
  Beralih kembali dari kecepatan cepat ke standar akan mengakibatkan [cache prompt](/docs/id/build-with-claude/prompt-caching) tidak ditemukan (miss). Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
</Note>

Karena mengatur `max_retries` ke `0` juga menonaktifkan percobaan ulang untuk error sementara lainnya (overloaded, internal server error), contoh berikut mengirim ulang permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup exclude="shell:cURL">
  ```bash CLI
  # `ant` mencoba ulang 429/5xx secara otomatis dan tidak memiliki override max_retries
  # per permintaan, sehingga pada 429 mode cepat, fallback berjalan setelah
  # percobaan ulang bawaan habis. --transform-error menampilkan error.type untuk percabangan.
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

  ```python Python
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

  ```typescript TypeScript
  const client = new Anthropic();

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
  ```

  ```csharp C#
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

  ```go Go
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
  			Speed: anthropic.BetaMessageNewParamsSpeedFast,
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

  ```java Java
  import com.anthropic.errors.InternalServerException;
  import com.anthropic.errors.RateLimitException;
  // ...
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

  ```php PHP
  use Anthropic\Core\Exceptions\APIConnectionException;
  use Anthropic\Core\Exceptions\InternalServerException;
  use Anthropic\Core\Exceptions\RateLimitException;
  use Anthropic\RequestOptions;
  // ...
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

  ```ruby Ruby
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

## Pertimbangan

* **Caching prompt:** Beralih antara kecepatan cepat dan standar membatalkan cache prompt. Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
* **Model yang didukung:** Mode cepat didukung pada Claude Opus 4.8 dan Claude Opus 4.7 (mode cepat tidak digunakan lagi; penghapusan pada 24 Juli 2026, dengan model itu sendiri tidak terpengaruh). Pada Claude Opus 4.6, permintaan dengan `speed: "fast"` tidak mengembalikan error: permintaan tersebut berjalan pada kecepatan standar dan ditagih dengan tarif standar. Pada model lainnya, mengirim `speed: "fast"` mengembalikan error.
* **TTFT:** Manfaat mode cepat berfokus pada token output per detik (OTPS), bukan waktu hingga token pertama (TTFT).
* **Batch API:** Mode cepat tidak tersedia dengan [Batch API](/docs/id/build-with-claude/batch-processing).
* **Priority Tier:** Mode cepat tidak tersedia dengan komitmen [Priority Tier](/docs/id/api/service-tiers).
* **Claude Platform di AWS:** Mode cepat saat ini tidak tersedia di [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Output terstruktur" icon="code-brackets" href="/docs/id/build-with-claude/structured-outputs">
    Dapatkan hasil JSON yang tervalidasi dari alur kerja agen.
  </Card>

  <Card title="Harga" icon="calculator" href="/docs/id/about-claude/pricing#fast-mode-pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>

  <Card title="Effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.
  </Card>

  <Card title="Streaming pesan" icon="arrow-right" href="/docs/id/build-with-claude/streaming">
    Lakukan streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>
