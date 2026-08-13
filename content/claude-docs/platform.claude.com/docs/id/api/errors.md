---
source: platform
url: https://platform.claude.com/docs/id/api/errors
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: d83800af65256a7127e2f0cffb406abe94d86740919a10723a2acc669157ca7c
---

---
title: Error API Claude
url: https://platform.claude.com/docs/id/api/errors
description: Pahami kode status HTTP, bentuk respons error, dan ID permintaan yang dikembalikan oleh Claude API, serta tangani error dengan exception bertipe dari SDK.
---

## Error HTTP

API mengikuti format kode error HTTP yang dapat diprediksi:

* 400 - `invalid_request_error`: Ada masalah dengan format atau konten permintaan Anda. Tipe error ini juga dapat digunakan untuk kode status 4XX lainnya yang tidak tercantum di bagian ini.

* 401 - `authentication_error`: Ada masalah dengan kunci API Anda (misalnya, formatnya salah, dicabut, atau kedaluwarsa; lihat [Kedaluwarsa kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration)). Pada Claude Platform di AWS, ini juga dapat menunjukkan masalah dengan kredensial AWS atau tanda tangan SigV4 Anda.

* 402 - `billing_error`: Ada masalah dengan informasi penagihan atau pembayaran Anda. Periksa detail pembayaran Anda di [Claude Console](https://platform.claude.com), atau di AWS Marketplace jika Anda menggunakan Claude Platform di AWS.

* 403 - `permission_error`: Kunci API Anda tidak memiliki izin untuk menggunakan sumber daya yang ditentukan. Periksa pengaturan akses dan workspace organisasi Anda di [Claude Console](https://platform.claude.com).

* 404 - `not_found_error`: Sumber daya yang diminta tidak ditemukan. Periksa jalur endpoint dan ID sumber daya apa pun di URL permintaan.

* 409 - `conflict_error`: Permintaan bertentangan dengan status sumber daya saat ini. Misalnya, sumber daya dimodifikasi secara bersamaan, atau nilai yang harus unik sudah digunakan. Selesaikan konflik tersebut, lalu coba lagi permintaannya.

* 413 - `request_too_large`: Permintaan melebihi jumlah byte maksimum yang diizinkan. Lihat [Batas ukuran permintaan](https://platform.claude.com/docs/id/api/errors#request-size-limits) untuk maksimum per endpoint.

* 429 - `rate_limit_error`: Akun Anda telah mencapai batas laju (rate limit).

* 500 - `api_error`: Terjadi error tak terduga di dalam sistem internal Anthropic. Coba lagi permintaan dengan exponential backoff; jika error berlanjut, hubungi dukungan dengan menyertakan [ID permintaan](https://platform.claude.com/docs/id/api/errors#request-id).

* 504 - `timeout_error`: Permintaan kehabisan waktu saat diproses. Pertimbangkan untuk menggunakan [streaming Messages API](https://platform.claude.com/docs/id/build-with-claude/streaming) untuk permintaan yang berjalan lama. Lihat [Permintaan panjang](https://platform.claude.com/docs/id/api/errors#long-requests) untuk opsi lainnya.

* 529 - `overloaded_error`: API sedang kelebihan beban untuk sementara.

  <Warning>
    Error 529 dapat terjadi ketika API mengalami lalu lintas tinggi dari semua pengguna.

    Dalam kasus yang jarang terjadi, jika organisasi Anda mengalami peningkatan penggunaan yang tajam, Anda mungkin melihat error 429 karena batas akselerasi pada API. Untuk menghindari batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
  </Warning>

SDK resmi secara otomatis mencoba ulang kegagalan sementara (seperti error koneksi, batas laju, dan error server 5xx) dengan exponential backoff, dua kali secara default, dengan menghormati header `retry-after` jika ada. Setiap klien SDK menerima opsi maximum-retries untuk mengonfigurasi atau menonaktifkan perilaku ini.

Saat menerima respons [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) melalui server-sent events (SSE), error dapat terjadi setelah API mengembalikan respons 200. Dalam kasus tersebut, penanganan error tidak mengikuti mekanisme standar ini. Lihat [Event error](https://platform.claude.com/docs/id/build-with-claude/streaming#error-events) untuk bentuk error di tengah stream.

## Batas ukuran permintaan

API memberlakukan batas ukuran permintaan:

| Tipe endpoint                                                                       | Ukuran permintaan maksimum |
| ----------------------------------------------------------------------------------- | -------------------------- |
| Messages API                                                                        | 32 MB                      |
| Token Counting API                                                                  | 32 MB                      |
| [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) | 256 MB                     |
| [Files API](https://platform.claude.com/docs/id/build-with-claude/files)            | 500 MB                     |

Jika Anda melebihi batas ini, Anda akan menerima error 413 `request_too_large`. Pada Claude API langsung, Cloudflare mengembalikan error ini sebelum permintaan mencapai server API.

## Bentuk error

API selalu mengembalikan error sebagai JSON, dengan objek `error` tingkat atas yang selalu menyertakan nilai `type` dan `message`. Respons juga menyertakan field `request_id` untuk memudahkan pelacakan dan debugging. Contohnya:

```json JSON
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "The requested resource could not be found."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

Sesuai dengan kebijakan [versioning](https://platform.claude.com/docs/id/api/versioning), nilai-nilai di dalam objek ini dapat bertambah, dan ada kemungkinan nilai `type` akan bertambah seiring waktu.

## Tipe error SDK

SDK resmi memunculkan exception bertipe untuk error-error ini alih-alih mengembalikan JSON mentah, dan nama kelas serta namespace-nya berbeda menurut bahasa. Misalnya, 404 muncul sebagai `anthropic.NotFoundError` di Python, `Anthropic::Errors::NotFoundError` di Ruby, `com.anthropic.errors.NotFoundException` di Java, dan sebagai nilai tunggal `*anthropic.Error` (bercabang berdasarkan `StatusCode`) di Go. Tangkap kelas bertipe dari SDK alih-alih mencocokkan string pesan error, dengan menangani kelas yang paling spesifik terlebih dahulu. Setiap halaman SDK mendokumentasikan hierarki exception lengkapnya:

* [Python](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python#handling-errors) · [TypeScript](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/typescript#handling-errors) · [C#](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/csharp#error-handling) · [Go](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#error-handling) · [Java](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/java#error-handling) · [PHP](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/php#error-handling) · [Ruby](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/ruby#handling-errors)

## ID permintaan

Setiap respons API menyertakan header `request-id` yang unik. Header ini berisi nilai seperti `req_018EeWyXxfu5pfWkrYcMdjWG`. Pengidentifikasi yang sama muncul sebagai field `request_id` di [badan respons error](https://platform.claude.com/docs/id/api/errors#error-shapes). Saat menghubungi dukungan tentang permintaan tertentu, sertakan ID ini untuk membantu menyelesaikan masalah Anda dengan cepat.

Pada [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), respons menyertakan dua ID permintaan: ID permintaan AWS (`x-amzn-requestid`, utama, terindeks di CloudTrail) dan ID permintaan Anthropic (`request-id`, sekunder). Gunakan ID permintaan AWS untuk pencarian di CloudTrail dan ID permintaan Anthropic untuk tiket dukungan Anthropic.

SDK Python dan TypeScript mengekspos ID permintaan sebagai properti `_request_id` pada objek respons tingkat atas. SDK C#, Go, Java, dan PHP mengeksposnya melalui accessor raw-response mereka, yang juga memungkinkan Anda membaca header respons lainnya. Pada Claude Platform di AWS, gunakan accessor raw-response untuk membaca ID permintaan AWS (`x-amzn-requestid`) juga:

<CodeGroup>
  ```bash cURL
  # Cetak header respons (termasuk request-id); abaikan body-nya
  curl -sS -D - -o /dev/null https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  # Header request-id dicetak ke stderr dengan --debug:
  ant --debug messages create \
    --model claude-sonnet-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"Request ID: {message._request_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  console.log("Request ID:", message._request_id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.WithRawResponse.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }]
  });
  Console.WriteLine($"Request ID: {response.RequestID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  var response *http.Response
  message, err := client.Messages.New(
  	context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeSonnet5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	},
  	option.WithResponseInto(&response),
  )
  if err != nil {
  	panic(err)
  }

  fmt.Println("Request ID:", response.Header.Get("request-id"))
  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponseFor;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      HttpResponseFor<Message> response = client.messages().withRawResponse().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build()
      );

      IO.println("Request ID: " + response.requestId().orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->raw->create([
      'model' => 'claude-sonnet-5',
      'maxTokens' => 1024,
      'messages' => [['role' => 'user', 'content' => 'Hello, Claude']],
  ]);
  echo 'Request ID: ' . $response->getHeaderLine('request-id') . "\n";
  ```

  ```ruby Ruby
  # Mengakses header respons mentah saat ini belum didukung di SDK Ruby.
  # Untuk membaca header request-id, gunakan salah satu contoh SDK lainnya.
  ```

  ```python Python (Claude Platform on AWS)
  from anthropic import AnthropicAWS

  client = AnthropicAWS(aws_region="us-west-2")

  response = client.messages.with_raw_response.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(f"AWS request ID: {response.headers.get('x-amzn-requestid')}")
  message = response.parse()
  print(f"Anthropic request ID: {message._request_id}")
  ```

  ```typescript TypeScript (Claude Platform on AWS)
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws({ awsRegion: "us-west-2" });

  const { response: raw, request_id } = await client.messages
    .create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    })
    .withResponse();
  console.log("AWS request ID:", raw.headers.get("x-amzn-requestid"));
  console.log("Anthropic request ID:", request_id);
  ```
</CodeGroup>

Untuk contoh request-ID Claude Platform di AWS dalam bahasa lain, lihat [ID Permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#request-ids).

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan [streaming Messages API](https://platform.claude.com/docs/id/build-with-claude/streaming) atau [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create) untuk permintaan yang berjalan lama, terutama yang lebih dari 10 menit.
</Warning>

Hindari menetapkan nilai `max_tokens` yang besar tanpa menggunakan [streaming Messages API](https://platform.claude.com/docs/id/build-with-claude/streaming) atau [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create):

* Beberapa jaringan mungkin memutuskan koneksi yang idle setelah periode waktu yang bervariasi, yang dapat menyebabkan permintaan gagal atau kehabisan waktu tanpa menerima respons dari Anthropic.
* Keandalan jaringan berbeda-beda. [Message Batches API](https://platform.claude.com/docs/id/api/messages/batches/create) dapat membantu Anda mengelola risiko masalah jaringan dengan memungkinkan Anda melakukan polling untuk hasil alih-alih memerlukan koneksi jaringan yang tidak terputus.

Jika Anda membangun integrasi API langsung, menetapkan [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) dapat mengurangi dampak timeout koneksi idle pada beberapa jaringan.

[SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) memvalidasi bahwa permintaan Messages API non-streaming Anda tidak diperkirakan melebihi timeout 10 menit. SDK juga menetapkan opsi socket untuk TCP keep-alive.

Jika Anda tidak perlu memproses event secara bertahap, SDK dapat mengonsumsi stream untuk Anda dan mengembalikan objek `Message` lengkap, identik dengan apa yang dikembalikan oleh panggilan non-streaming:

<CodeGroup>
  ```bash cURL
  # Output SSE mentah mengharuskan penanganan event; tidak ada cara satu perintah
  # untuk mengakumulasi pesan akhir dengan curl. Gunakan contoh SDK sebagai gantinya.
  ```

  ```bash CLI
  # CLI melakukan streaming event; --format jsonl mengeluarkan satu event per baris
  ant messages create --stream --format jsonl <<'YAML'
  model: claude-sonnet-5
  max_tokens: 128000
  messages:
    - role: user
      content: Write a detailed analysis...
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=128000,
      messages=[{"role": "user", "content": "Write a detailed analysis..."}],
      model="claude-sonnet-5",
  ) as stream:
      message = stream.get_final_message()

  print(next(block.text for block in message.content if block.type == "text"))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }],
    model: "claude-sonnet-5"
  });

  const message = await stream.finalMessage();
  const textBlock = message.content.find((block) => block.type === "text");
  if (textBlock && textBlock.type === "text") {
    console.log(textBlock.text);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 128000,
      Messages = [new() { Role = Role.User, Content = "Write a detailed analysis..." }]
  };

  var message = await client.Messages.CreateStreaming(parameters).Aggregate();
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 128000,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a detailed analysis...")),
  	},
  })

  message := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := message.Accumulate(event); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.MessageAccumulator;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5)
          .maxTokens(128000L)
          .addUserMessage("Write a detailed analysis...")
          .build();

      MessageAccumulator accumulator = MessageAccumulator.create();
      try (var streamResponse = client.messages().createStreaming(params)) {
          streamResponse.stream().forEach(accumulator::accumulate);
      }

      Message message = accumulator.message();
      message.content().stream()
              .filter(ContentBlock::isText)
              .findFirst()
              .flatMap(ContentBlock::text)
              .ifPresent(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Lib\Streaming\MessageAccumulator;

  $client = new Client();

  $stream = $client->messages->createStream(
      model: 'claude-sonnet-5',
      maxTokens: 128000,
      messages: [['role' => 'user', 'content' => 'Write a detailed analysis...']],
  );

  $accumulator = MessageAccumulator::forMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
  }

  echo array_find($accumulator->message()->content, static fn ($block): bool => $block->type === 'text')->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.stream(
    model: "claude-sonnet-5",
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }]
  ).accumulated_message

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

Lihat [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail lebih lanjut.

## Error validasi umum

### Prefill tidak didukung

Model Claude 4.6 dan yang lebih baru serta [Claude Mythos Preview](https://anthropic.com/glasswing) tidak mendukung prefilling pesan assistant. Mengirim permintaan dengan pesan assistant terakhir yang sudah di-prefill ke salah satu model ini mengembalikan error 400 `invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "This model does not support assistant message prefill. The conversation must end with a user message."
  }
}
```

Sebagai gantinya, gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) pada model yang mendukungnya, instruksi prompt sistem, atau [`output_config.format`](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-outputs).

### Blok thinking tidak dapat dimodifikasi

Jika pesan assistant terbaru berisi blok `thinking` atau `redacted_thinking` yang diedit, diurutkan ulang, disaring, atau direkonstruksi sebelum dikirim kembali ke API, permintaan mengembalikan error 400 `invalid_request_error`. Pesan error dimulai dengan posisi blok yang bermasalah (misalnya, `messages.1.content.0`) dan berisi:

```text wrap
`thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified. These blocks must remain as they were in the original response.
```

Dengan penggunaan alat (tool use), setiap blok `thinking` dan `redacted_thinking` dari giliran assistant harus dikirim kembali persis seperti yang diterima, termasuk blok yang field `thinking`-nya kosong. Kirim kembali blok thinking tanpa perubahan, dan jika aplikasi Anda menyaring blok konten berdasarkan tipe sebelum mengirim ulang, sertakan baik `thinking` maupun `redacted_thinking`. Lihat [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified), [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks), dan [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

### Extended thinking tidak didukung

Model Claude 4.7 dan yang lebih baru telah menghapus "extended thinking" (pemikiran diperpanjang). Mengirim `thinking: {"type": "enabled"}` ke salah satu model ini mengembalikan error 400 `invalid_request_error`:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Sebagai gantinya, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). [Migrasi ke adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) menunjukkan pemetaan parameter, dan [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-enabled) membahas perbaikan berdasarkan gejala.

### Adaptive thinking tidak didukung

Model yang hanya mendukung pemikiran diperpanjang (model Claude 4.5 dan yang lebih lama) menolak `thinking: {"type": "adaptive"}` dengan error 400 `invalid_request_error`:

```text wrap
adaptive thinking is not supported on this model
```

Gunakan `thinking: {"type": "enabled", "budget_tokens": N}` pada model-model ini; lihat [Extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) untuk konfigurasinya dan [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-adaptive) untuk perbaikan berdasarkan gejala.

### Thinking tidak dapat dinonaktifkan

Pada Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), dan [Claude Mythos Preview](https://anthropic.com/glasswing), thinking selalu aktif. Mengirim `thinking: {"type": "disabled"}` ke salah satu model ini mengembalikan error 400 `invalid_request_error`:

```text wrap
"thinking.type.disabled" is not supported for this model. Thinking defaults to adaptive mode when not specified; use "thinking.type.enabled" with "budget_tokens" for extended thinking.
```

Pada Claude Fable 5 dan Claude Mythos 5, saran dari pesan error itu sendiri yaitu `"thinking.type.enabled"` juga ditolak. Hilangkan parameter `thinking` dan permintaan akan berjalan dengan adaptive thinking. Untuk menjaga konten thinking tidak muncul di respons tanpa mematikan thinking, tetapkan `display: "omitted"` pada konfigurasi thinking. Lihat [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-disabled).

### Outbound web identity federation dinonaktifkan (Claude Platform di AWS)

Jika setiap permintaan ke [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) mengembalikan `"Outbound web identity federation is disabled for your account"`, jalankan `aws iam enable-outbound-web-identity-federation` sekali per akun AWS. Lihat [Mengaktifkan outbound web identity federation](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#enable-outbound-web-identity-federation) untuk detailnya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Memicu routine melalui API" icon="play" href="https://platform.claude.com/docs/id/api/claude-code/routines-fire">
    Mulai sesi routine Claude Code sesuai permintaan dengan mengirim permintaan POST yang terautentikasi.
  </Card>

  <Card title="Batas laju" icon="gauge" href="https://platform.claude.com/docs/id/api/rate-limits">
    Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan pada seberapa banyak sebuah organisasi dapat menggunakan Claude API.
  </Card>

  <Card title="Streaming pesan" icon="lightning" href="https://platform.claude.com/docs/id/build-with-claude/streaming">
    Lakukan streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>
