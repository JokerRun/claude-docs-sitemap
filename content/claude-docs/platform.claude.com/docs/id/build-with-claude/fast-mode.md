---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 09d8b87bb2cb375c106445548dd3797f19311ad10140e55123a067f8b4d75b5e
---

---
title: Mode cepat
url: https://platform.claude.com/docs/id/build-with-claude/fast-mode
description: Dapatkan token output per detik hingga 2,5x lebih tinggi dari model Claude yang didukung.
featureMetadata:
  betaHeader: fast-mode-2026-02-01
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan.
  supportedModels:
    - claude-opus-5-5
    - claude-opus-5
    - claude-opus-4-8
  supportedPlatforms:
    Claude API: stable
    Claude Models on Google Cloud (Anthropic managed): stable
    Microsoft Foundry (hosted on Azure): stable
  details:
    - Mode cepat pada Claude Opus 5 dan Claude Opus 4.8 berada dalam pratinjau riset dan memerlukan header beta `fast-mode-2026-02-01`.
---

**Dukungan API**: Penggunaan berbeda menurut produk.

* **Messages API**: Atur `speed: "fast"` pada permintaan.
* **Managed Agents**: Atur `speed` pada objek model agen, misalnya `{"id": "claude-opus-5-5", "speed": "fast"}`.

“Fast mode” (mode cepat) menghasilkan token output per detik hingga 2,5x lebih tinggi dengan harga premium. Atur `speed: "fast"` pada permintaan Anda untuk ikut serta. Mode cepat tersedia di Claude Opus 5.5 dan dalam pratinjau riset di Claude Opus 5 serta Claude Opus 4.8.

## Cara kerja mode cepat

Mode cepat menjalankan model yang sama dengan konfigurasi inferensi yang lebih cepat. Tidak ada perubahan pada kecerdasan atau kemampuan.

* Token output per detik hingga 2,5x lebih tinggi dibandingkan dengan kecepatan standar
* Manfaat kecepatan berfokus pada “output tokens per second” (token output per detik), atau OTPS, bukan “time to first token” (waktu hingga token pertama), atau TTFT
* Kompatibel dengan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming), di mana peningkatan OTPS paling terlihat

## Penggunaan dasar

Mode cepat hanya berfungsi pada model yang didukung. Lihat [Ketersediaan](https://platform.claude.com/docs/id/build-with-claude/fast-mode#feature-availability) untuk detailnya, termasuk model mana yang memerlukan header beta.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 4096,
      "speed": "fast",
      "messages": [{
        "role": "user",
        "content": "Refactor this module to use dependency injection"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 4096
  speed: fast
  messages:
    - role: user
      content: Refactor this module to use dependency injection
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      speed="fast",
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

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    speed: "fast",
    messages: [
      {
        role: "user",
        content: "Refactor this module to use dependency injection"
      }
    ]
  });

  const textBlock = response.content.find((block) => block.type === "text");
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Speed = Speed.Fast,
      Messages = [
          new UserMessageParam { Content = "Refactor this module to use dependency injection" }
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

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Speed:     anthropic.MessageNewParamsSpeedFast,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Refactor this module to use dependency injection")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .speed(MessageCreateParams.Speed.FAST)
          .addUserMessage("Refactor this module to use dependency injection")
          .build());

  response.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 4096,
      speed: 'fast',
      messages: [
          ['role' => 'user', 'content' => 'Refactor this module to use dependency injection'],
      ],
  );

  foreach ($response->content as $block) {
      if ($block instanceof \Anthropic\Messages\TextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 4096,
    speed: "fast",
    messages: [{role: "user", content: "Refactor this module to use dependency injection"}]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Batas laju

Mode cepat memiliki “rate limit” (batas laju) khusus yang terpisah dari batas laju Opus standar. Ketika batas laju mode cepat Anda terlampaui, API mengembalikan error `429` dengan header `retry-after` yang menunjukkan kapan kapasitas akan tersedia.

Claude Opus 5.5 memiliki batas laju mode cepat default pada [tingkat penggunaan](https://platform.claude.com/docs/id/api/rate-limits) Start, Build, dan Scale, sehingga Anda tidak perlu meminta akses untuk menggunakan mode cepat dengannya. Organisasi pada tingkat Evaluation dapat menggunakan mode cepat dengan Claude Opus 5.5 setelah mereka pindah ke tingkat Start, Build, atau Scale.

Respons menyertakan header yang menunjukkan status batas laju mode cepat Anda:

| Header                                   | Deskripsi                                          |
| ---------------------------------------- | -------------------------------------------------- |
| `anthropic-fast-input-tokens-limit`      | Maksimum token input mode cepat per menit          |
| `anthropic-fast-input-tokens-remaining`  | Sisa token input mode cepat                        |
| `anthropic-fast-input-tokens-reset`      | Waktu ketika batas token input mode cepat direset  |
| `anthropic-fast-output-tokens-limit`     | Maksimum token output mode cepat per menit         |
| `anthropic-fast-output-tokens-remaining` | Sisa token output mode cepat                       |
| `anthropic-fast-output-tokens-reset`     | Waktu ketika batas token output mode cepat direset |

Untuk melihat batas laju mode cepat Anda, buka halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console.

## Memeriksa kecepatan yang digunakan

Objek `usage` pada respons menyertakan field `speed` yang menunjukkan kecepatan yang digunakan, yaitu `"fast"` atau `"standard"`. Meminta `speed: "fast"` pada [model yang tidak mendukung mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode#availability-feature-support) akan mengembalikan error, begitu pula jika melampaui batas laju atau kapasitas mode cepat (`429` atau `529`). Ketika permintaan dengan `speed: "fast"` berhasil, `usage.speed` bernilai `"fast"`. Claude Opus 4.6 merupakan pengecualian: alih-alih mengembalikan error, permintaan dengan `speed: "fast"` dan header beta `fast-mode-2026-02-01` berhasil, tetapi berjalan dengan kecepatan standar. Perilaku ini tercermin dengan benar di `usage.speed`, yang menampilkan `"standard"` dalam situasi ini. Di Claude Models on Google Cloud (Anthropic managed), permintaan Claude Opus 4.6 dengan `speed: "fast"` mengembalikan error `400` bahkan dengan header tersebut.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "speed": "fast",
      "messages": [{"role": "user", "content": "Hello"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  speed: fast
  messages:
    - role: user
      content: Hello
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      speed="fast",
      messages=[{"role": "user", "content": "Hello"}],
  )

  print(response.usage.speed)  # "fast" or "standard"
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    speed: "fast",
    messages: [{ role: "user", content: "Hello" }]
  });

  console.log(response.usage.speed); // "fast" or "standard"
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Speed = Speed.Fast,
      Messages = [new UserMessageParam { Content = "Hello" }],
  });

  Console.WriteLine(response.Usage.Speed);  // "fast" or "standard"
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Speed:     anthropic.MessageNewParamsSpeedFast,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
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
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .speed(MessageCreateParams.Speed.FAST)
      .addUserMessage("Hello")
      .build();

  Message response = client.messages().create(params);
  IO.println(response.usage().speed().orElseThrow());  // "fast" or "standard"
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      speed: 'fast',
      messages: [['role' => 'user', 'content' => 'Hello']],
  );

  echo $response->usage->speed;  // "fast" or "standard"
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    speed: "fast",
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

Untuk melacak penggunaan dan biaya mode cepat di seluruh organisasi Anda, lihat [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api).

## Percobaan ulang dan fallback

### Percobaan ulang otomatis

SDK secara otomatis mencoba ulang error `429` mode cepat hingga 2 kali secara default (dapat dikonfigurasi dengan `max_retries` (typescript, php: `maxRetries`; java: `.maxRetries()`; csharp: `MaxRetries`; go: `option.WithMaxRetries()`)), dengan menunggu jeda yang ditentukan di header `retry-after` sebelum setiap percobaan ulang. Karena mode cepat menggunakan pengisian ulang token secara berkelanjutan, jeda `retry-after` biasanya singkat dan permintaan berhasil setelah kapasitas tersedia.

### Fallback ke kecepatan standar

Jika Anda lebih suka beralih ke kecepatan standar daripada menunggu kapasitas mode cepat, tangkap error batas laju dan coba ulang tanpa `speed: "fast"`. Atur `max_retries` (typescript, php: `maxRetries`; java: `.maxRetries()`; csharp: `MaxRetries`; go: `option.WithMaxRetries()`) ke `0` pada permintaan cepat awal untuk melewati percobaan ulang otomatis dan langsung gagal pada error batas laju.

<Note>
  Beralih dari kecepatan cepat ke standar mengakibatkan cache miss pada [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching). Permintaan dengan kecepatan berbeda tidak berbagi prefiks yang di-cache.
</Note>

Karena mengatur `max_retries` (typescript, php: `maxRetries`; java: `.maxRetries()`; csharp: `MaxRetries`; go: `option.WithMaxRetries()`) ke `0` juga menonaktifkan percobaan ulang untuk error sementara lainnya (overloaded, error server internal), contoh berikut mengirim ulang permintaan asli dengan percobaan ulang default untuk kasus-kasus tersebut.

<CodeGroup exclude="shell:cURL, shell:CLI">
  ```python Python
  client = anthropic.Anthropic()


  def create_message_with_fast_fallback(max_retries=0, max_attempts=3, **params):
      try:
          return client.with_options(max_retries=max_retries).messages.create(**params)
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
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello"}],
      speed="fast",
      max_retries=0,
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  async function createMessageWithFastFallback(
    params: Anthropic.MessageCreateParamsNonStreaming,
    requestOptions?: Anthropic.RequestOptions,
    maxAttempts: number = 3
  ): Promise<Anthropic.Message> {
    try {
      return await client.messages.create(params, requestOptions);
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
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello" }],
      speed: "fast"
    },
    { maxRetries: 0 }
  );
  ```

  ```csharp C#
  AnthropicClient client = new();

  async Task<Message> CreateMessageWithFastFallback(
      MessageCreateParams parameters,
      int? maxRetries = null,
      int maxAttempts = 3)
  {
      try
      {
          var requestClient = maxRetries is int retries
              ? client.WithOptions(options => options with { MaxRetries = retries })
              : client;
          return await requestClient.Messages.Create(parameters);
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
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello" }],
          Speed = Speed.Fast,
      },
      maxRetries: 0);
  ```

  ```go Go
  func createMessageWithFastFallback(
  	ctx context.Context,
  	client *anthropic.Client,
  	params anthropic.MessageNewParams,
  	maxAttempts int,
  	opts ...option.RequestOption,
  ) (*anthropic.Message, error) {
  	message, err := client.Messages.New(ctx, params, opts...)
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
  		anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 1024,
  			Messages: []anthropic.MessageParam{
  				anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
  			},
  			Speed: anthropic.MessageNewParamsSpeedFast,
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
  // Nonaktifkan auto-retry SDK agar logika fallback berikutnya yang menanganinya
  AnthropicClient client =
      AnthropicOkHttpClient.builder()
          .fromEnv()
          .maxRetries(0)
          .build();

  Message createMessageWithFastFallback(
          MessageCreateParams params, int maxAttempts) {
      try {
          return client.messages().create(params);
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
      Message message = createMessageWithFastFallback(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addUserMessage("Hello")
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
          return $client->messages->create(
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
          'model' => 'claude-opus-5-5',
          'maxTokens' => 1024,
          'messages' => [['role' => 'user', 'content' => 'Hello']],
          'speed' => 'fast',
      ],
      RequestOptions::with(maxRetries: 0),
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  def create_message_with_fast_fallback(client, request_options: {}, max_attempts: 3, **params)
    client.messages.create(**params, request_options: request_options)
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
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
    speed: "fast",
    request_options: { max_retries: 0 }
  )
  ```
</CodeGroup>

## Pertimbangan

* **Batch API:** Mode cepat tidak tersedia dengan [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing).
* **Priority Tier:** Mode cepat tidak tersedia dengan komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers).

## Harga

Harga mode cepat dihitung sebagai pengali dari tarif standar di seluruh “context window” (jendela konteks), termasuk permintaan dengan lebih dari 200k token input.

| Model                           | Input          | Output         |
| ------------------------------- | -------------- | -------------- |
| Claude Opus 5.5                 | $8 USD / MTok  | $40 USD / MTok |
| Claude Opus 5 / Claude Opus 4.8 | $10 USD / MTok | $50 USD / MTok |

Harga mode cepat digabungkan dengan pengubah harga lainnya:

* [Pengali caching prompt](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching) berlaku di atas harga mode cepat.
* Pengali [residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) berlaku di atas harga mode cepat.

Untuk detail harga lengkap, lihat halaman [Harga](https://platform.claude.com/docs/id/about-claude/pricing#fast-mode-pricing).

## Ketersediaan

Mode cepat tersedia atau dalam pratinjau riset di model tertentu dan layak untuk retensi data nol dan kesiapan HIPAA.

### Dukungan API

Mode cepat hanya tersedia pada model-model berikut. Jika Anda menggunakan mode cepat pada model sebelumnya, [migrasikan ke model yang mendukung mode cepat](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide).

Untuk mengakses mode cepat pada Claude Opus 5, hubungi manajer akun Anda atau [bergabunglah dengan daftar tunggu](https://claude.com/fast-mode).

<Warning>
  Mode cepat pada Claude Opus 4.8 sudah usang (deprecated) dan akan dihapus pada 30 November 2026. Setelah penghapusan, permintaan ke `claude-opus-4-8` dengan `speed: "fast"` akan mengembalikan error. Untuk terus menggunakan mode cepat, migrasikan ke Claude Opus 5.5. Lihat [Migrasi ke Claude Opus 5.5 dari Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8).
</Warning>

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia
* Penggunaan: Atur `speed: "fast"` pada permintaan.

| Status          | Platform cloud                                                                                                                                                                                                                                                                                   | Model                                                                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tersedia        | Claude API, [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Microsoft Foundry (hosted on Azure)](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)                                                                              |
| Pratinjau riset | Claude API                                                                                                                                                                                                                                                                                       | [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia
* Penggunaan: Atur `speed` pada objek model agen, misalnya `{"id": "claude-opus-5-5", "speed": "fast"}`.

| Status          | Platform cloud | Model                                                                                                                                                        |
| --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tersedia        | Claude API     | [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)                                                                              |
| Pratinjau riset | Claude API     | [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

| Header                 | Model                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fast-mode-2026-02-01` | [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview) |

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                 | HIPAA |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements)) | Layak |
| Detail | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan.                                                    | —     |

Endpoint yang berlaku:

* `/v1/messages` dengan `speed: "fast"`

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Output terstruktur" icon="code-brackets" href="https://platform.claude.com/docs/id/build-with-claude/structured-outputs">
    Dapatkan hasil JSON yang tervalidasi dari alur kerja agen.
  </Card>

  <Card title="Harga" icon="calculator" href="https://platform.claude.com/docs/id/about-claude/pricing#fast-mode-pricing">
    Pelajari struktur harga Anthropic untuk model dan fitur.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, dengan menyeimbangkan antara kelengkapan respons dan efisiensi token.
  </Card>

  <Card title="Streaming pesan" icon="arrow-right" href="https://platform.claude.com/docs/id/build-with-claude/streaming">
    Streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>
