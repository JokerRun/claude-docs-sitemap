---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 35c599b562cb58c8ef14ae2739bf620c2daae8e452b4942795b3580fc1f65919
---

---
title: Mode cepat (pratinjau riset)
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
description: Dapatkan token output per detik hingga 2,5x lebih tinggi dari model Claude Opus yang didukung.
---

Mode cepat (fast mode) memberikan token output per detik hingga 2,5x lebih tinggi dari Claude Opus 5 dan Claude Opus 4.8 dengan harga premium. Atur `speed: "fast"` dengan header beta `fast-mode-2026-02-01` pada permintaan Anda untuk ikut serta.

<Note>
  Mode cepat sedang dalam pratinjau riset. Hubungi manajer akun Anda untuk meminta akses. Jika Anda tidak memiliki manajer akun, [bergabunglah dengan daftar tunggu](https://claude.com/fast-mode) untuk mode cepat.
</Note>

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

## Model yang didukung

Mode cepat didukung pada model-model berikut:

* Claude Opus 5 (claude-opus-5)
* Claude Opus 4.8 (claude-opus-4-8)

<Note>
  Mode cepat untuk Claude Opus 5 dan Claude Opus 4.8 tersedia sebagai pratinjau riset hanya di Claude API, termasuk [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview). Mode ini tidak tersedia di Amazon Bedrock, Claude Platform on AWS, Google Cloud, atau Microsoft Foundry.
</Note>

<Note>
  Mode cepat tidak tersedia pada Claude Opus 4.7. Permintaan ke `claude-opus-4-7` dengan `speed: "fast"` mengembalikan error; tidak seperti Claude Opus 4.6 (lihat catatan berikut), permintaan tidak beralih kembali ke kecepatan standar. Model itu sendiri tetap tersedia pada kecepatan standar. Untuk terus menggunakan mode cepat, migrasikan ke [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-47) atau Claude Opus 4.8.
</Note>

<Note>
  Mode cepat tidak tersedia pada Claude Opus 4.6. Permintaan ke `claude-opus-4-6` dengan `speed: "fast"` tidak mengembalikan error: permintaan tersebut berjalan pada kecepatan standar dan ditagih dengan [tarif standar](https://platform.claude.com/docs/id/about-claude/pricing) alih-alih tarif premium mode cepat, dan respons melaporkan [`usage.speed: "standard"`](https://platform.claude.com/docs/id/build-with-claude/fast-mode#checking-which-speed-was-used). Untuk terus menggunakan mode cepat, migrasikan ke [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-46) atau Claude Opus 4.8.
</Note>

## Cara kerja mode cepat

Mode cepat menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

* Token output per detik hingga 2,5x lebih tinggi dibandingkan kecepatan standar
* Manfaat kecepatan berfokus pada "output tokens per second" (token output per detik), atau OTPS, bukan "time to first token" (waktu hingga token pertama), atau TTFT
* Bobot dan perilaku model yang sama (bukan model yang berbeda)
* Kompatibel dengan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming), di mana peningkatan OTPS paling terlihat

## Penggunaan dasar

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fast-mode-2026-02-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
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
    --transform 'content.#(type=="text").text' \
    --raw-output <<'YAML'
  model: claude-opus-5
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
      model="claude-opus-5",
      max_tokens=4096,
      speed="fast",
      betas=["fast-mode-2026-02-01"],
      messages=[
          {"role": "user", "content": "Refactor this module to use dependency injection"}
      ],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5",
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
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Speed = Speed.Fast,
      Betas = ["fast-mode-2026-02-01"],
      Messages = [
          new() { Role = Role.User, Content = "Refactor this module to use dependency injection" }
      ],
  });

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
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
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(4096L)
                  .speed(MessageCreateParams.Speed.FAST)
                  .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                  .addUserMessage("Refactor this module to use dependency injection")
                  .build());

  response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 4096,
      speed: 'fast',
      betas: ['fast-mode-2026-02-01'],
      messages: [
          ['role' => 'user', 'content' => 'Refactor this module to use dependency injection'],
      ],
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    speed: "fast",
    betas: ["fast-mode-2026-02-01"],
    messages: [{role: "user", content: "Refactor this module to use dependency injection"}]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Harga

Mode cepat dihargai dengan pengali terhadap tarif standar di seluruh jendela konteks (context window), termasuk permintaan dengan lebih dari 200k token input. Tabel berikut menunjukkan harga mode cepat untuk model yang didukung:

| Model                           | Input          | Output         |
| ------------------------------- | -------------- | -------------- |
| Claude Opus 5 / Claude Opus 4.8 | $10 USD / MTok | $50 USD / MTok |

Harga mode cepat bertumpuk dengan pengubah harga lainnya:

* [Pengali caching prompt](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching) berlaku di atas harga mode cepat
* Pengali [residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) berlaku di atas harga mode cepat

Untuk detail harga lengkap, lihat halaman [Harga](https://platform.claude.com/docs/id/about-claude/pricing#fast-mode-pricing).

## Batas laju

Mode cepat memiliki batas laju (rate limit) khusus yang terpisah dari batas laju Opus standar. Ketika batas laju mode cepat Anda terlampaui, API mengembalikan error `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Respons menyertakan header yang menunjukkan status batas laju mode cepat Anda:

| Header                                   | Deskripsi                                          |
| ---------------------------------------- | -------------------------------------------------- |
| `anthropic-fast-input-tokens-limit`      | Token input mode cepat maksimum per menit          |
| `anthropic-fast-input-tokens-remaining`  | Token input mode cepat yang tersisa                |
| `anthropic-fast-input-tokens-reset`      | Waktu ketika batas token input mode cepat direset  |
| `anthropic-fast-output-tokens-limit`     | Token output mode cepat maksimum per menit         |
| `anthropic-fast-output-tokens-remaining` | Token output mode cepat yang tersisa               |
| `anthropic-fast-output-tokens-reset`     | Waktu ketika batas token output mode cepat direset |

Untuk batas laju spesifik per tingkat, lihat halaman [Batas laju](https://platform.claude.com/docs/id/api/rate-limits).

## Memeriksa kecepatan mana yang digunakan

Objek `usage` pada respons menyertakan field `speed` yang menunjukkan kecepatan mana yang digunakan, baik `"fast"` maupun `"standard"`. Meminta `speed: "fast"` pada [model yang tidak mendukung mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models) mengembalikan error, begitu pula jika melampaui batas laju atau kapasitas mode cepat (`429` atau `529`). Ketika permintaan dengan `speed: "fast"` berhasil, `usage.speed` bernilai `"fast"`. Jika Anda menggunakan Claude Opus 4.6 dan meminta mode cepat, perilakunya unik. Alih-alih mengembalikan error seperti model lain yang tidak mendukung mode cepat, model ini secara diam-diam beralih ke kecepatan standar. Meskipun tidak ada error pada Opus 4.6, field `speed` secara akurat menampilkan `"standard"`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fast-mode-2026-02-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
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
  model: claude-opus-5
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
      model="claude-opus-5",
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
    model: "claude-opus-5",
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
      Model = "claude-opus-5",
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
  	Model:     anthropic.ModelClaudeOpus5,
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
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .speed(MessageCreateParams.Speed.FAST)
          .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
          .addUserMessage("Hello")
          .build();

  BetaMessage response = client.beta().messages().create(params);
  IO.println(response.usage().speed().orElseThrow());  // "fast" or "standard"
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
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
    model: "claude-opus-5",
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

Untuk melacak penggunaan dan biaya mode cepat di seluruh organisasi Anda, lihat [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api).

## Percobaan ulang dan fallback

### Percobaan ulang otomatis

Ketika batas laju mode cepat terlampaui, API mengembalikan error `429` dengan header `retry-after`. SDK Anthropic secara otomatis mencoba ulang permintaan ini hingga 2 kali secara default (dapat dikonfigurasi dengan `max_retries`), menunggu jeda yang ditentukan server sebelum setiap percobaan ulang. Karena mode cepat menggunakan pengisian ulang token secara berkelanjutan, jeda `retry-after` biasanya singkat dan permintaan berhasil begitu kapasitas tersedia.

### Beralih kembali ke kecepatan standar

<Note>
  Bagian ini membahas fallback sisi klien yang bersifat opt-in ketika mode cepat terkena batas laju. Ini terpisah dari perilaku pada [Claude Opus 4.6](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models), di mana mode cepat tidak tersedia dan permintaan berjalan pada kecepatan standar secara otomatis.
</Note>

Jika Anda lebih memilih beralih kembali ke kecepatan standar daripada menunggu kapasitas mode cepat, tangkap error batas laju dan coba ulang tanpa `speed: "fast"`. Atur `max_retries` ke `0` pada permintaan cepat awal untuk melewati percobaan ulang otomatis dan langsung gagal pada error batas laju.

<Note>
  Beralih dari kecepatan cepat ke standar akan mengakibatkan [prompt cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) miss. Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
</Note>

Karena mengatur `max_retries` ke `0` juga menonaktifkan percobaan ulang untuk error sementara lainnya (overloaded, internal server error), contoh-contoh berikut mengirim ulang permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup exclude="shell:cURL">
  ```bash CLI
  # `ant` mencoba ulang 429/5xx secara otomatis dan tidak memiliki override max_retries
  # per permintaan, jadi pada 429 mode cepat, fallback berjalan setelah percobaan ulang
  # bawaan habis. --transform-error menampilkan error.type untuk percabangan.
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
  model: claude-opus-5
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
      model="claude-opus-5",
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
    params: Anthropic.Beta.MessageCreateParamsNonStreaming,
    requestOptions?: Anthropic.RequestOptions,
    maxAttempts: number = 3
  ): Promise<Anthropic.Beta.Messages.BetaMessage> {
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
          return createMessageWithFastFallback(params, undefined, maxAttempts - 1);
        }
      }
      throw e;
    }
  }

  const message = await createMessageWithFastFallback(
    {
      model: "claude-opus-5",
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
          Model = "claude-opus-5",
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
  			Model:     anthropic.ModelClaudeOpus5,
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
                      .model(Model.CLAUDE_OPUS_5)
                      .maxTokens(1024L)
                      .addUserMessage("Hello")
                      .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                      .speed(MessageCreateParams.Speed.FAST)
                      .build(),
              3);
      message.content().stream()
              .flatMap(block -> block.text().stream())
              .forEach(textBlock -> IO.println(textBlock.text()));
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
          'model' => 'claude-opus-5',
          'maxTokens' => 1024,
          'messages' => [['role' => 'user', 'content' => 'Hello']],
          'betas' => ['fast-mode-2026-02-01'],
          'speed' => 'fast',
      ],
      RequestOptions::with(maxRetries: 0),
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

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
    client,
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
    betas: ["fast-mode-2026-02-01"],
    speed: "fast",
    request_options: { max_retries: 0 }
  )
  ```
</CodeGroup>

## Pertimbangan

* **Caching prompt:** Beralih antara kecepatan cepat dan standar membatalkan prompt cache. Permintaan pada kecepatan yang berbeda tidak berbagi prefiks yang di-cache.
* **Model yang didukung:** Mode cepat didukung pada Claude Opus 5 dan Claude Opus 4.8. Lihat [Model yang didukung](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).
* **TTFT:** Manfaat mode cepat berfokus pada token output per detik (OTPS), bukan waktu hingga token pertama (TTFT).
* **Batch API:** Mode cepat tidak tersedia dengan [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing).
* **Priority Tier:** Mode cepat tidak tersedia dengan komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers).
* **Claude Platform on AWS:** Mode cepat saat ini tidak tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Output terstruktur" icon="code-brackets" href="https://platform.claude.com/docs/id/build-with-claude/structured-outputs">
    Dapatkan hasil JSON yang tervalidasi dari alur kerja agen.
  </Card>

  <Card title="Harga" icon="calculator" href="https://platform.claude.com/docs/id/about-claude/pricing#fast-mode-pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.
  </Card>

  <Card title="Streaming pesan" icon="arrow-right" href="https://platform.claude.com/docs/id/build-with-claude/streaming">
    Lakukan streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>
