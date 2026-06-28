---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: d156a316a89083022abe24aa200a58c90cac8103d88fb49bd26c8f169aacd07f
---

# Penolakan dan fallback

Bagaimana Claude Fable 5 mengembalikan penolakan dari classifier dan cara mencoba ulang permintaan yang ditolak pada model fallback.

---

Claude Fable 5 menyertakan "safety classifiers" (pengklasifikasi keamanan) yang dapat menolak sebuah permintaan. Ketika itu terjadi, Anda menerima respons normal, bukan error, dengan `stop_reason: "refusal"`. Anda biasanya masih bisa mendapatkan jawaban dengan mengirimkan permintaan yang sama ke model Claude lain. Halaman ini menunjukkan cara mengenali penolakan dan cara menyiapkan percobaan ulang tersebut.

Baca halaman ini ketika Anda membangun di atas Claude Fable 5 dan ingin permintaan yang ditolak diteruskan ke model lain secara otomatis. Halaman ini juga berlaku ketika Anda baru saja melihat `"refusal"` dalam sebuah respons dan ingin tahu apa yang harus dilakukan selanjutnya.

Halaman terkait:

* [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons): daftar lengkap nilai `stop_reason`.
* [Kredit fallback](/docs/id/build-with-claude/fallback-credit): bagaimana permintaan yang ditolak ditagih, dan cara menghindari membayar dua kali untuk caching prompt pada percobaan ulang.
* [Middleware SDK](/docs/id/cli-sdks-libraries/middleware): helper SDK yang membungkus semua ini.
* [Cookbook fallback dan penagihan](https://platform.claude.com/cookbook/fable-5-fallback-billing-guide): contoh lengkap dari awal hingga akhir.

Pengaturan paling sederhana: sebutkan model fallback pada permintaan, dan API akan menangani percobaan ulangnya.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallback '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-06-01
  ```

  ```python Python
  client = Anthropic()

  client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-06-01"],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-06-01"]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = [new(Messages::Model.ClaudeOpus4_8)],
          Betas = [AnthropicBeta.ServerSideFallback2026_06_01],
      }
  );
  ```

  ```go Go
  client := anthropic.NewClient()

  client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: []anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_06_01},
  })
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .addFallback(BetaFallbackParam.builder().model(Model.CLAUDE_OPUS_4_8).build())
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_06_01)
      .build());
  ```

  ```php PHP
  $client = new Client();

  $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-fable-5',
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-06-01'],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-06-01"]
  )
  ```
</CodeGroup>

Bagian-bagian di bawah ini membahas apa yang terkandung dalam respons penolakan, kapan menggunakan fallback sisi server atau sisi klien, dan bagaimana masing-masing ditagih.

## Seperti apa bentuk penolakan

Penolakan adalah respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`:

```json
{
  "id": "msg_01XFUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-fable-5",
  "content": [],
  "stop_reason": "refusal",
  "stop_details": {
    "type": "refusal",
    "category": "cyber",
    "explanation": "This request was declined because it could enable cyber harm."
  },
  "usage": {
    "input_tokens": 412,
    "output_tokens": 0
  }
}
```

Objek `stop_details` menjelaskan penolakan tersebut:

* **`category`:** menyebutkan area kebijakan yang memicu classifier.
* **`explanation`:** deskripsi yang dapat dibaca manusia. Teksnya tidak stabil, jadi tampilkan saja alih-alih mem-parsing-nya.
* Kedua field bernilai `null` ketika penolakan tidak dipetakan ke kategori yang memiliki nama. Nilai `null` tersebut adalah nilai normal dan permanen, bukan placeholder.
* `stop_details` itu sendiri bernilai `null` untuk setiap stop reason selain `refusal`.

| `category`               | Artinya                                                                                                                                                                                                                                               |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"cyber"`                | Permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau eksploit. Pekerjaan keamanan siber yang tidak berbahaya juga dapat memicu kategori ini.                                                                                 |
| `"bio"`                  | Permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya. Pekerjaan ilmu hayati yang bermanfaat juga dapat memicu kategori ini.                                                                                      |
| `"frontier_llm"`         | Permintaan dapat membantu pengembangan model AI pesaing, yang dibatasi berdasarkan [ketentuan komersial Anthropic](https://www.anthropic.com/legal/commercial-terms). Pekerjaan machine learning yang tidak berbahaya juga dapat memicu kategori ini. |
| `"reasoning_extraction"` | Permintaan meminta model untuk mereproduksi penalaran internalnya dalam teks respons. Untuk mendapatkan penalaran dalam bentuk terstruktur, gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).                                |

Penolakan dapat tiba sebelum ada output apa pun, atau di tengah stream setelah output parsial. Dalam kedua kasus tersebut, perlakukan output parsial apa pun sebagai tidak lengkap dan buang.

<Note>
  **Bagaimana penolakan ditagih:** Anda tidak ditagih untuk penolakan yang tiba sebelum ada output apa pun. `content` kosong, jumlah token muncul di `usage` tetapi tidak dikenakan biaya, dan permintaan tidak dihitung terhadap batas laju. Penolakan di tengah stream menagih token input dan output yang sudah di-stream dengan tarif normal.
</Note>

## Memilih pendekatan fallback

Ada tiga cara untuk mencoba ulang permintaan yang ditolak pada model lain. Pilihan yang tepat bergantung pada di mana Anda menjalankannya dan seberapa banyak kontrol yang Anda butuhkan.

| Situasi Anda                                                        | Gunakan                                                                                     | Alasan                                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Claude API atau Claude Platform di AWS, pengaturan paling sederhana | [Fallback sisi server](#server-side-fallback)                                               | Satu permintaan, satu respons. API menangani percobaan ulang.         |
| Platform apa pun, dengan SDK TypeScript, Python, Go, Java, atau C#  | [Middleware SDK](#client-side-fallback)                                                     | Konfigurasi sekali di klien. Percobaan ulang terjadi secara otomatis. |
| Ruby, PHP, HTTP mentah, atau logika percobaan ulang kustom          | Percobaan ulang manual dengan [kredit fallback](/docs/id/build-with-claude/fallback-credit) | Kontrol penuh. Kredit fallback menjaga biaya tetap rendah.            |

Fallback sisi server dan middleware SDK menerapkan kredit fallback untuk Anda. Anda hanya memerlukan halaman [Kredit fallback](/docs/id/build-with-claude/fallback-credit) ketika Anda membangun percobaan ulang sendiri.

## Fallback sisi server

Fallback sisi server mencoba ulang permintaan yang ditolak di dalam satu panggilan API. Anda menyebutkan hingga tiga model fallback, dan ketika Claude Fable 5 menolak, API menjalankan model berikutnya dalam rantai pada permintaan yang sama. Anda mendapatkan kembali satu respons yang menyebutkan model yang menjawab, sehingga pengguna Anda mendapatkan jawaban dalam satu kali bolak-balik.

<Note>
  Fallback sisi server masih dalam tahap beta di Claude API dan Claude Platform di AWS. Parameter `fallbacks` ditolak pada [Message Batches API](/docs/id/build-with-claude/batch-processing) dan tidak tersedia di Amazon Bedrock, Vertex AI, atau Microsoft Foundry. Pada platform-platform tersebut, gunakan [middleware SDK](#client-side-fallback) sebagai gantinya.
</Note>

### Membuat permintaan

Sebutkan model fallback dalam parameter `fallbacks` dan kirim header beta `server-side-fallback-2026-06-01`.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -c '{stop_reason, model}'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallback '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-06-01 \
    --format json |
    jq -c '{stop_reason, model}'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-06-01"],
  )

  # Entri fallback_message di usage.iterations berarti model fallback dijalankan;
  # pasangkan dengan stop_reason untuk memastikan fallback yang melayani respons.
  fallback_ran = any(
      iteration.type == "fallback_message"
      for iteration in response.usage.iterations or []
  )
  served_by_fallback = fallback_ran and response.stop_reason != "refusal"

  print(
      json.dumps(
          {
              "stop_reason": response.stop_reason,
              "model": response.model,
              "served_by_fallback": served_by_fallback,
          }
      )
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-06-01"]
  });

  // Entri fallback_message dalam usage.iterations berarti model fallback dijalankan;
  // pasangkan dengan stop_reason untuk memastikan fallback yang melayani respons.
  const { stop_reason, model, usage } = response;
  const servedByFallback =
    (usage.iterations ?? []).some((entry) => entry.type === "fallback_message") &&
    stop_reason !== "refusal";

  console.log(
    JSON.stringify({
      stop_reason,
      model,
      served_by_fallback: servedByFallback
    })
  );
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages =
          [
              new() { Content = "Hello, Claude", Role = Role.User },
          ],
          Fallbacks = [new(Messages::Model.ClaudeOpus4_8)],
          Betas = [AnthropicBeta.ServerSideFallback2026_06_01],
      }
  );

  // Entri fallback_message dalam usage.iterations berarti model fallback telah berjalan;
  // pasangkan dengan stop_reason untuk memastikan fallback yang melayani respons.
  bool fallbackRan = (response.Usage.Iterations ?? []).Any(iteration =>
      iteration.TryPickFallbackMessageIterationUsage(out _)
  );
  bool servedByFallback =
      fallbackRan && response.StopReason?.Value() != BetaStopReason.Refusal;

  Console.WriteLine(
      JsonSerializer.Serialize(
          new
          {
              stop_reason = response.StopReason?.Raw(),
              model = response.Model.Raw(),
              served_by_fallback = servedByFallback,
          }
      )
  );
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: []anthropic.BetaFallbackParam{
  		{Model: anthropic.ModelClaudeOpus4_8},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_06_01},
  })
  if err != nil {
  	panic(err)
  }

  // Entri fallback_message di usage.iterations berarti model fallback dijalankan;
  // padukan dengan stop_reason untuk memastikan fallback yang menyajikan respons.
  fallbackRan := slices.ContainsFunc(
  	response.Usage.Iterations,
  	func(iteration anthropic.BetaIterationsUsageItemUnion) bool {
  		_, isFallback := iteration.AsAny().(anthropic.BetaFallbackMessageIterationUsage)
  		return isFallback
  	},
  )
  servedByFallback := fallbackRan && response.StopReason != anthropic.BetaStopReasonRefusal

  summary, err := json.Marshal(struct {
  	StopReason       anthropic.BetaStopReason `json:"stop_reason"`
  	Model            anthropic.Model          `json:"model"`
  	ServedByFallback bool                     `json:"served_by_fallback"`
  }{response.StopReason, response.Model, servedByFallback})
  if err != nil {
  	panic(err)
  }
  fmt.Println(string(summary))
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_FABLE_5)
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .addFallback(BetaFallbackParam.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .build())
          .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_06_01)
          .build()
  );

  // Entri usage fallback_message berarti model fallback yang menghasilkan
  // respons; stop reason refusal berarti tidak ada model yang melayaninya.
  List<BetaUsage.BetaIterationsUsageItems> iterations =
      response.usage().iterations().orElse(List.of());
  boolean servedByFallback =
      iterations.stream().anyMatch(BetaUsage.BetaIterationsUsageItems::isFallbackMessage)
          && !response.stopReason().map(BetaStopReason.REFUSAL::equals).orElse(false);

  IO.println("""
      {"stop_reason":"%s","model":"%s","served_by_fallback":%b}\
      """.formatted(
          response.stopReason().map(BetaStopReason::asString).orElse("null"),
          response.model().asString(),
          servedByFallback));
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-fable-5',
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-06-01'],
  );

  // Entri fallback_message di usage.iterations berarti model fallback dijalankan;
  // padukan dengan stop_reason untuk memastikan fallback yang memberikan respons.
  $iterations = $response->usage->iterations ?? [];
  $servedByFallback = array_any($iterations, fn($entry) => $entry->type === 'fallback_message')
      && $response->stopReason !== 'refusal';

  echo json_encode([
      'stop_reason' => $response->stopReason,
      'model' => $response->model,
      'served_by_fallback' => $servedByFallback,
  ]), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-06-01"]
  )

  # Entri fallback_message dalam usage.iterations berarti model fallback dijalankan;
  # pasangkan dengan stop_reason untuk memastikan fallback yang melayani respons.
  iterations = response.usage.iterations || []
  served_by_fallback = iterations.any? { it.type == :fallback_message } &&
    response.stop_reason != :refusal

  stop_reason = response.stop_reason
  model = response.model
  puts JSON.generate({stop_reason:, model:, served_by_fallback:})
  ```
</CodeGroup>

Beberapa aturan berlaku untuk daftar `fallbacks`:

* Entri dicoba secara berurutan. Setiap entri harus berbeda dari entri lainnya dan dari model yang diminta.
* Setiap entri harus merupakan salah satu target yang diizinkan untuk model yang diminta. Dengan header beta diatur, daftar tersebut dipublikasikan sebagai `allowed_fallback_models` pada entri model di [Models API](/docs/id/api/models/list).
* Setiap entri menyebutkan sebuah `model` dan dapat menimpa `max_tokens` dan `thinking` hanya untuk percobaan tersebut.
* Permintaan harus valid sebagai permintaan langsung ke setiap model yang disebutkan. Jika model fallback tidak mendukung fitur yang digunakan permintaan, API menolak permintaan tersebut di awal.
* Hanya penolakan dari safety classifier yang memicu fallback. Batas laju, overload, atau error server pada model yang diminta dikembalikan kepada Anda apa adanya.

<Note>
  Header beta harus membawa tanggal persis `2026-06-01`. Di bawah nilai `server-side-fallback-*` lainnya, parameter `fallbacks` ditolak dengan error 400. Jika Anda membangun berdasarkan pratinjau fitur ini yang lebih awal, perbarui header beta serta bentuk permintaan dan respons secara bersamaan ke yang ada di halaman ini.
</Note>

### Apa yang terkandung dalam respons

Respons terlihat seperti pesan lainnya, dengan dua tambahan:

* Field `model` tingkat atas melaporkan model yang menghasilkan pesan yang dikembalikan, baik itu model yang diminta maupun fallback.

* Blok konten `fallback` menandai setiap titik dalam `content` di mana output satu model beralih ke model berikutnya: `{"type": "fallback", "from": {"model": ...}, "to": {"model": ...}}`.

  * `from.model` menggemakan string model yang Anda kirim ketika hop yang menolak adalah model yang diminta.
  * `to.model` selalu merupakan ID yang telah di-resolve dari model yang melanjutkan.

Pada penolakan sebelum ada output apa pun, blok `fallback` adalah blok konten pertama:

```json
{
  "id": "msg_01XFUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-4-8",
  "content": [
    {
      "type": "fallback",
      "from": { "model": "claude-fable-5" },
      "to": { "model": "claude-opus-4-8" }
    },
    { "type": "text", "text": "Hi! How can I help you today?" }
  ],
  "stop_reason": "end_turn",
  "stop_details": null,
  "usage": {
    "input_tokens": 412,
    "output_tokens": 264,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "iterations": [
      {
        "type": "message",
        "model": "claude-fable-5",
        "input_tokens": 535,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0
      },
      {
        "type": "fallback_message",
        "model": "claude-opus-4-8",
        "input_tokens": 412,
        "output_tokens": 264,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0
      }
    ]
  }
}
```

Array `usage.iterations` mencatat setiap percobaan. Model yang menolak muncul sebagai entri `message` biasa, dan model yang melayani giliran tersebut muncul sebagai entri `fallback_message`. Jika setiap model dalam rantai menolak, responsnya adalah penolakan dari model terakhir, dengan entri `message` untuk setiap hop sebelumnya dan entri `fallback_message` untuk yang terakhir.

### Melanjutkan percakapan

Pada giliran berikutnya, kirim kembali konten asisten sebagaimana Anda menerimanya. Setelah fallback di tengah output, `content` dapat menyertakan tipe blok yang dihasilkan model yang menolak sebelum serah terima; tabel di bawah ini membahas mana yang harus dipertahankan dan mana yang harus dibuang ketika Anda menggemakan giliran tersebut.

| Tipe blok                                                                               | Pada giliran berikutnya                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fallback`                                                                              | Pertahankan persis di tempat kemunculannya. API menggunakan posisinya untuk memvalidasi blok thinking di sekitarnya, sehingga permintaan yang menggemakan blok thinking dari kedua sisi batas akan ditolak jika blok tersebut dihilangkan atau dipindahkan. |
| `text`                                                                                  | Pertahankan.                                                                                                                                                                                                                                                |
| Blok apa pun setelah blok `fallback` terakhir                                           | Pertahankan.                                                                                                                                                                                                                                                |
| `thinking`, `redacted_thinking`, atau `connector_text` sebelum blok `fallback` terakhir | Buang.                                                                                                                                                                                                                                                      |
| `tool_use` sisi klien sebelum blok `fallback` terakhir                                  | Buang.                                                                                                                                                                                                                                                      |
| `server_tool_use` sebelum blok `fallback` terakhir                                      | Pertahankan jika berpasangan dengan hasilnya. Buang jika tidak memiliki hasil yang cocok.                                                                                                                                                                   |

<Note>
  Blok `connector_text` membawa teks narasi yang disertakan oleh beberapa respons yang menggunakan alat di antara panggilan alat.
</Note>

### Streaming

Pada permintaan streaming, percobaan ulang terjadi pada stream yang sama, dan tidak ada yang sudah Anda terima yang dibatalkan. Apa yang Anda lihat bergantung pada kapan penolakan terjadi.

**Ketika penolakan terjadi sebelum ada output apa pun:**

* `message_start` menyebutkan model fallback, dan blok `fallback` adalah blok konten pertama.
* Karena `message_start` menunggu percobaan fallback dimulai, waktu hingga byte pertama mencakup percobaan yang ditolak.

**Ketika penolakan terjadi di tengah output:**

* Blok konten yang terbuka ditutup, dan blok `fallback` (pasangan `content_block_start` dan `content_block_stop` biasa tanpa delta) menandai batasnya.
* Model fallback melanjutkan dari output parsial. Hanya blok `text` dari output parsial yang diteruskan ke model fallback sebagai konteks; tipe blok lainnya tetap berada di `content`.
* `message_start` sudah menyebutkan model yang diminta, jadi baca model yang melayani dari `to.model` pada blok `fallback` dan dari entri `fallback_message` di `usage.iterations` pada `message_delta` terakhir.

### Respons non-streaming

Pada permintaan non-streaming, penolakan di tengah output berperilaku berbeda: respons menghilangkan output parsial dari model yang ditolak, dan model fallback menjawab dari awal. Hasilnya terlihat seperti penolakan sebelum ada output apa pun, dengan blok `fallback` di awal. Percobaan yang ditolak dan token output-nya tetap muncul di `usage.iterations`.

<Note>
  **Penolakan setelah alat server berjalan:** ketika penolakan terjadi setelah alat server (misalnya, pencarian web atau eksekusi kode) sudah dieksekusi dalam sebuah permintaan, API mengembalikan penolakan alih-alih melanjutkan ke model fallback. Jika header `fallback-credit-2026-06-01` juga diatur, penolakan tersebut membawa token kredit yang dapat ditukarkan dengan melanjutkan respons parsial, sehingga pekerjaan alat yang sudah selesai tidak hilang. Ini hanya berlaku untuk alat server yang beriterasi dalam satu permintaan. Percakapan yang menggunakan alat sisi klien melakukan fallback secara normal.
</Note>

<Accordion title="Sticky routing">
  Setelah sebuah percakapan melakukan fallback, API mencatat model mana yang melayaninya. Permintaan selanjutnya untuk percakapan tersebut yang menyertakan `fallbacks` langsung menuju model fallback tersebut, tanpa menjalankan model yang diminta. Ini menghindari pembayaran untuk percobaan yang dapat diprediksi akan ditolak lagi pada setiap giliran.

  Beberapa properti dari keputusan routing:

  * Keputusan ini disimpan selama kurang lebih satu jam dan cakupannya terbatas pada organisasi Anda.
  * Keputusan ini disimpan sebagai hash konten dari prefiks percakapan ditambah model yang melayaninya. Konten pesan itu sendiri tidak disimpan.
  * Keputusan ini bersifat best-effort, jadi kode Anda harus menangani kemungkinan model yang diminta dicoba lagi kapan saja.

  Giliran yang dilayani secara sticky tidak membawa blok konten `fallback`, karena tidak ada model yang menolak giliran tersebut. Identifikasi dari entri `fallback_message` di `usage.iterations`, tidak adanya entri `message` untuk model yang diminta, dan field `model` pada respons.

  Dalam rilis saat ini, sticky routing hanya berlaku untuk permintaan non-streaming. Permintaan streaming yang melakukan fallback tetap mencatat keputusan tersebut untuk giliran non-streaming selanjutnya.
</Accordion>

<Accordion title="Bagaimana fallback sisi server ditagih">
  Anda membayar untuk model yang benar-benar melayani permintaan. Percobaan yang menolak sebelum menghasilkan output tidak dikenakan biaya dan tidak mengonsumsi batas laju.

  Setiap percobaan ditagih secara terpisah, dengan tarif model yang menjalankannya. Array `usage.iterations` adalah catatan per-percobaan dari apa yang ditagihkan kepada Anda. Jumlah `usage` tingkat atas hanya menggambarkan percobaan yang menghasilkan pesan yang dikembalikan; token dari model yang berbeda tidak pernah dijumlahkan ke dalam satu field.

  Setiap percobaan yang berjalan dihitung terhadap batas laju modelnya sendiri. Jika model fallback terkena batas laju atau overload, percobaan fallback tidak dilakukan dan penolakan sebelumnya dikembalikan sebagai gantinya. Sesuaikan ukuran batas laju model fallback untuk volume penolakan yang Anda perkirakan, atau fallback akan terdegradasi menjadi penolakan di bawah beban tinggi.

  Ketika percobaan fallback dilewati dengan cara ini, `stop_details.recommended_model` menyebutkan model untuk dicoba ulang secara langsung. Rekomendasi tersebut adalah petunjuk, bukan jaminan, dan bernilai `null` ketika tidak ada rekomendasi yang tersedia.
</Accordion>

## Fallback sisi klien dengan middleware SDK

SDK TypeScript, Python, Go, Java, dan C# menyertakan middleware refusal-fallback. Anda mengonfigurasinya sekali pada klien dengan daftar model fallback Anda. Panggilan melalui `client.beta.messages` kemudian mencoba ulang permintaan yang ditolak secara otomatis, di platform mana pun. Middleware juga mengirimkan header beta `fallback-credit-2026-06-01` pada setiap permintaan yang ditanganinya, sehingga percobaan ulang dihargai ulang tanpa pengaturan per-permintaan.

<Note>
  Helper middleware refusal-fallback belum tersedia di SDK Ruby dan PHP. Pada SDK tersebut, implementasikan pola deteksi-dan-coba-ulang secara langsung.
</Note>

### Menyiapkannya

Teruskan middleware ke konstruktor klien, dan bagikan satu instance `BetaFallbackState` di seluruh permintaan dalam sebuah percakapan.

<CodeGroup>
  ```bash cURL
  # Middleware refusal-fallback adalah fitur SDK. Lihat
  # bagian fallback sisi server untuk pendekatan permintaan tunggal yang setara,
  # atau halaman kredit fallback untuk pola retry HTTP mentah.
  ```

  ```bash CLI
  # Middleware refusal-fallback adalah fitur SDK. Lihat
  # bagian fallback sisi server untuk pendekatan permintaan tunggal yang setara,
  # atau halaman kredit fallback untuk pola retry HTTP mentah.
  ```

  ```python Python
  # Saat terjadi penolakan, middleware mencoba ulang pada model fallback yang tercantum dan
  # secara otomatis mengirim header beta fallback-credit pada setiap permintaan yang ditanganinya.
  client = Anthropic(
      middleware=[BetaRefusalFallbackMiddleware([{"model": "claude-opus-4-8"}])],
  )

  state = BetaFallbackState()  # pins follow-ups to the model that accepted

  # Streaming: saat terjadi penolakan, middleware mencoba ulang pada model fallback dan
  # menyambungkan event-nya ke stream yang sedang terbuka.
  with (
      state,
      client.beta.messages.stream(
          max_tokens=1024,
          model="claude-fable-5",
          messages=[{"role": "user", "content": "Hello, Claude"}],
      ) as stream,
  ):
      for event in stream:
          if event.type == "text":
              print(event.text, end="", flush=True)
      final_message = stream.get_final_message()
  print(f"\nserved by: {final_message.model}")

  # Non-streaming: menggunakan kembali state membuat percakapan tetap terikat.
  with state:
      message = client.beta.messages.create(
          max_tokens=1024,
          model="claude-fable-5",
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
  print(f"served by: {message.model}")
  ```

  ```typescript TypeScript
  // Saat terjadi penolakan, middleware mencoba ulang permintaan melalui rantai fallback.
  // Middleware mengirim header beta fallback-credit pada setiap permintaan yang ditanganinya.
  const client = new Anthropic({
    middleware: [betaRefusalFallbackMiddleware([{ model: "claude-opus-4-8" }])]
  });

  // Bagikan satu state di seluruh percakapan agar permintaan lanjutan tetap
  // terikat pada model yang menerima.
  const fallbackState = new BetaFallbackState();

  // Streaming: saat terjadi penolakan, middleware menyambungkan event dari model fallback
  // ke stream yang masih terbuka.
  const stream = client.beta.messages.stream(
    {
      model: "claude-fable-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  stream.on("text", (text) => process.stdout.write(text));

  const finalMessage = await stream.finalMessage();
  console.log("\nserved by:", finalMessage.model);

  // Non-streaming: menggunakan kembali state menjaga percakapan tetap terikat pada model yang menerima.
  const message = await client.beta.messages.create(
    {
      model: "claude-fable-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  console.log("served by:", message.model);
  ```

  ```csharp C#
  // Saat terjadi penolakan, handler mencoba ulang pada model fallback yang tercantum dan
  // secara otomatis mengirim header beta fallback-credit pada setiap permintaan yang ditanganinya.
  AnthropicClient client = new()
  {
      Handlers =
      [
          new BetaRefusalFallbackHandler { Fallbacks = [new(Messages::Model.ClaudeOpus4_8)] },
      ],
  };

  // Menyematkan permintaan lanjutan yang berbagi state ini ke model yang menerima.
  BetaFallbackState fallbackState = BetaFallbackState.Create();

  MessageCreateParams parameters = new()
  {
      Model = Messages::Model.ClaudeFable5,
      MaxTokens = 1024,
      Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
  };

  // Streaming: jika stream berakhir dengan penolakan, handler menyambungkan event dari model
  // fallback ke stream yang masih terbuka.
  BetaMessageContentAggregator aggregator = new();
  using (fallbackState.Use())
  {
      var responseUpdates = client.Beta.Messages.CreateStreaming(parameters);
      await foreach (BetaRawMessageStreamEvent rawEvent in responseUpdates.CollectAsync(aggregator))
      {
          if (
              rawEvent.TryPickContentBlockDelta(out var deltaEvent)
              && deltaEvent.Delta.TryPickText(out var textDelta)
          )
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  BetaMessage streamedMessage = aggregator.Message();
  Console.WriteLine($"\nserved by: {streamedMessage.Model.Raw()}");

  // Non-streaming: menggunakan kembali state ini menjaga percakapan tetap tersemat ke model yang menerima.
  using (fallbackState.Use())
  {
      BetaMessage message = await client.Beta.Messages.Create(parameters);
      Console.WriteLine($"served by: {message.Model.Raw()}");
  }
  ```

  ```go Go
  ctx := context.Background()

  // Middleware mencoba ulang permintaan yang ditolak pada setiap model fallback secara
  // bergiliran, dan otomatis mengikutsertakan permintaan ke beta fallback-credit.
  client := anthropic.NewClient(
  	option.WithMiddleware(betafallback.BetaRefusalFallbackMiddleware(
  		[]anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	)),
  )

  // Satu state per percakapan: permintaan yang berbagi state tetap terikat ke
  // model yang menerima, jadi tindak lanjut tak pernah bertanya ulang ke model yang menolak.
  state := &betafallback.BetaFallbackState{}
  conversation := betafallback.WithBetaFallbackState(state)

  params := anthropic.BetaMessageNewParams{
  	MaxTokens: 1024,
  	Model:     anthropic.ModelClaudeFable5,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  }

  // Streaming: saat ditolak, middleware mencoba ulang di tempat, menyambungkan
  // event model fallback ke stream yang terbuka sebagai satu pesan berkelanjutan.
  stream := client.Beta.Messages.NewStreaming(ctx, params, conversation)
  var streamed anthropic.BetaMessage
  for stream.Next() {
  	event := stream.Current()
  	if err := streamed.Accumulate(event); err != nil {
  		panic(err)
  	}
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.BetaRawContentBlockDeltaEvent:
  		if textDelta, ok := eventVariant.Delta.AsAny().(anthropic.BetaTextDelta); ok {
  			fmt.Print(textDelta.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }
  fmt.Println("\nserved by:", streamed.Model)

  // Non-streaming: state bersama mengikat tindak lanjut ini ke model yang
  // melayani giliran streaming sebelumnya.
  message, err := client.Beta.Messages.New(ctx, params, conversation)
  if err != nil {
  	panic(err)
  }
  fmt.Println("served by:", message.Model)
  ```

  ```java Java
  // Interceptor mencoba ulang permintaan yang ditolak pada model fallback. Secara otomatis
  // menambahkan header beta fallback-credit ke setiap permintaan yang ditanganinya.
  AnthropicClient client = AnthropicOkHttpClient.builder()
      .fromEnv()
      .addInterceptor(BetaRefusalFallbackInterceptor.builder()
          .addFallback(Model.CLAUDE_OPUS_4_8)
          .build())
      .build();

  // Bagikan satu state di seluruh permintaan agar tindak lanjut tetap terikat ke model yang menerima.
  BetaFallbackState state = BetaFallbackState.create();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024)
      .addUserMessage("Hello, Claude")
      .build();

  // Streaming: saat penolakan, event model fallback disambungkan ke stream yang terbuka.
  BetaMessageAccumulator accumulator = BetaMessageAccumulator.create();
  try (StreamResponse<BetaRawMessageStreamEvent> streamResponse = client.beta()
          .messages()
          .createStreaming(params, RequestOptions.builder().fallbackState(state).build())) {
      streamResponse.stream()
          .peek(accumulator::accumulate)
          .forEach(event -> event.contentBlockDelta()
              .flatMap(deltaEvent -> deltaEvent.delta().text())
              .ifPresent(textDelta -> IO.print(textDelta.text())));
  }
  IO.println("\nserved by: " + accumulator.message().model().asString());

  // Non-streaming: menggunakan kembali state yang sama menjaga percakapan tetap terikat.
  BetaMessage message = client.beta()
      .messages()
      .create(params, RequestOptions.builder().fallbackState(state).build());
  IO.println("served by: " + message.model().asString());
  ```

  ```php PHP
  // Middleware refusal-fallback saat ini belum tersedia di SDK PHP.
  // Lihat bagian fallback sisi server untuk pendekatan permintaan tunggal yang setara,
  // atau halaman kredit fallback untuk pola retry yang mendasarinya.
  ```

  ```ruby Ruby
  # Middleware refusal-fallback saat ini belum tersedia di Ruby SDK.
  # Lihat bagian fallback sisi server untuk pendekatan permintaan tunggal yang setara,
  # atau halaman kredit fallback untuk pola retry yang mendasarinya.
  ```
</CodeGroup>

### Bagaimana perilakunya

* Percobaan ulang menelusuri daftar fallback Anda secara berurutan. Model fallback yang juga menolak akan meneruskan permintaan ke entri berikutnya.
* Respons penolakan asli dikembalikan hanya ketika setiap model dalam daftar telah menolak. Middleware tidak memunculkan error untuk itu.
* [Blok thinking dari Claude Fable 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) ditangani untuk Anda: middleware menghapusnya dari percobaan ulang dan mengelolanya dalam riwayat percakapan pada permintaan selanjutnya.
* Respons yang dilayani melalui middleware menyertakan blok konten `fallback` di setiap batas model, sama seperti respons fallback sisi server. Middleware mengelola blok-blok tersebut untuk Anda pada permintaan selanjutnya.
* Model yang menerima dicatat dalam `BetaFallbackState`, sehingga permintaan lanjutan yang berbagi state tersebut tetap terpaku padanya alih-alih bertanya ulang ke model yang menolak.

<Note>
  Middleware dan parameter `fallbacks` sisi server melakukan pekerjaan yang sama. Konfigurasikan salah satunya, jangan pernah keduanya pada permintaan yang sama. Untuk mengirim permintaan `fallbacks` sisi server dari aplikasi yang memasang middleware, gunakan instance klien terpisah tanpa middleware.
</Note>

<Accordion title="Menulis percobaan ulang sendiri">
  Pada Ruby, PHP, atau HTTP mentah, implementasikan pola yang dibungkus oleh middleware:

  <Steps>
    <Step title="Deteksi penolakan">
      Periksa respons untuk `stop_reason: "refusal"`.
    </Step>

    <Step title="Kirim ulang pada model fallback">
      Kirim permintaan yang sama dengan `model` diatur ke model fallback, seperti Claude Opus 4.8. Permintaan yang ditolak oleh classifier Claude Fable 5 biasanya dapat dilayani oleh model lain. Cara Anda menangani riwayat percakapan bergantung pada apakah Anda menukarkan [kredit fallback](/docs/id/build-with-claude/fallback-credit):

      * **Tidak menukarkan kredit:** Anda dapat terlebih dahulu menghapus [blok thinking dari Claude Fable 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) dari riwayat percakapan. Model lain mengabaikannya, dan menghapusnya menjaga permintaan lintas-model tetap minimal.
      * **Menukarkan kredit:** kirim body tanpa perubahan, karena penukaran memerlukan kecocokan persis.
    </Step>

    <Step title="Tetap pada model fallback">
      Untuk percakapan multi-giliran, terus gunakan model fallback untuk giliran berikutnya alih-alih beralih kembali.
    </Step>
  </Steps>

  Percobaan ulang manual menulis cache prompt model fallback dari awal, yang biayanya lebih mahal daripada membaca cache yang sudah ada. [Kredit fallback](/docs/id/build-with-claude/fallback-credit) mengembalikan biaya tersebut; tukarkan pada setiap percobaan ulang yang Anda bangun sendiri.
</Accordion>

## Penolakan dalam Message Batches

Permintaan yang ditolak dalam [Message Batch](/docs/id/build-with-claude/batch-processing) kembali sebagai `result.type: "succeeded"` dengan `stop_reason: "refusal"`. Field `stop_details` mungkin bernilai `null` pada hasil batch, jadi deteksi penolakan dengan memeriksa `stop_reason` secara langsung.

Fallback sisi server tidak tersedia untuk batch (permintaan batch yang menyertakan `fallbacks` menghasilkan hasil error per-item). Untuk mencoba ulang item batch yang ditolak:

1. Kumpulkan item yang ditolak dari hasil.
2. Hapus blok thinking Claude Fable 5 dari riwayat multi-giliran mana pun.
3. Kirim ulang pada model fallback sebagai batch baru atau sebagai permintaan langsung.

## Kesalahan umum

* **Coba ulang pada model yang berbeda.** Mengirim ulang permintaan yang ditolak ke model yang sama biasanya menghasilkan penolakan lagi. Arahkan percobaan ulang ke model fallback.
* **Anggarkan percobaan ulang per permintaan, bukan per giliran atau per sesi.** Satu giliran dapat menghasilkan beberapa penolakan, misalnya sebuah agen ditambah sub-agennya.
* **Konfigurasikan fallback pada setiap jalur permintaan.** Handler percobaan ulang, cabang pemulihan error, dan worker latar belakang semuanya membutuhkannya. Handler yang mengeluarkan ulang permintaan tanpa fallback kehilangan perlindungan justru pada permintaan yang paling mungkin membutuhkannya.
* **Berikan panggilan sub-agen fallback-nya sendiri.** Parameter `fallbacks` tidak dipropagasi ke panggilan model yang dibuat dari dalam eksekusi alat.
* **Jadikan fallback sebagai properti permintaan, bukan state ambien.** Flag bersama, nilai konfigurasi yang di-cache, atau toggle global dapat menjadi tidak sinkron dan secara diam-diam membiarkan permintaan tidak terlindungi. Ketika Anda tidak dapat memastikan fallback aktif, konfigurasikan alih-alih mengasumsikan sudah aktif.
* **Instrumentasikan penolakan sebagai sinyal tersendiri.** Penolakan adalah HTTP 200, jadi pemantauan yang dibangun berdasarkan tingkat error atau respons 5xx tidak pernah melihatnya. Pancarkan satu event per penolakan dan satu per respons yang dilayani fallback (entri `fallback_message` di `usage.iterations` menandai yang terakhir), lalu buat alert pada selisih antara kedua hitungan tersebut.
* **Bercabang berdasarkan `stop_reason`, bukan `stop_details` atau `content`.** `stop_details` bersifat informasional dan dapat bernilai `null` pada penolakan. Periksa apakah `stop_reason` sama dengan `"refusal"` secara langsung.

## Langkah selanjutnya

<CardGroup>
  <Card title="Kredit fallback" icon="scales" href="/docs/id/build-with-claude/fallback-credit">
    Hindari membayar biaya cache prompt dua kali ketika Anda membangun percobaan ulang sendiri.
  </Card>

  <Card title="Stop reason dan fallback" icon="code" href="/docs/id/build-with-claude/handling-stop-reasons">
    Setiap nilai `stop_reason` dan cara menanganinya.
  </Card>

  <Card title="Middleware SDK" icon="settings" href="/docs/id/cli-sdks-libraries/middleware">
    Cara kerja middleware SDK, termasuk helper refusal-fallback.
  </Card>

  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide">
    Pindahkan aplikasi yang sudah ada ke Claude Fable 5.
  </Card>
</CardGroup>
