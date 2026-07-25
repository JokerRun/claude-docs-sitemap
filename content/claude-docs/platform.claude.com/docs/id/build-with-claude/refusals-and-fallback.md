---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 98368dfcc2bbaf9d99ee29513fe912c1b33c3e5b5c39b0d7a3117b3974d5fbfc
---

# Penolakan dan fallback

Bagaimana Claude Fable 5 dan Claude Opus 5 mengembalikan penolakan classifier dan cara mencoba ulang permintaan yang ditolak pada model fallback.

---

Claude Fable 5 dan Claude Opus 5 menyertakan safety classifier (pengklasifikasi keamanan) yang dapat menolak sebuah permintaan. Ketika itu terjadi, Anda menerima respons normal, bukan error, dengan `stop_reason: "refusal"`. Anda biasanya masih bisa mendapatkan jawaban dengan mengirimkan permintaan yang sama ke model Claude lain. Halaman ini menunjukkan cara mengenali penolakan dan cara menyiapkan percobaan ulang tersebut.

Baca halaman ini ketika Anda membangun di atas Claude Fable 5 atau Claude Opus 5 dan ingin permintaan yang ditolak dialihkan ke model lain secara otomatis. Halaman ini juga berlaku ketika Anda baru saja melihat `"refusal"` dalam sebuah respons dan ingin tahu apa yang harus dilakukan selanjutnya.

Halaman terkait:

* [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons): daftar lengkap nilai `stop_reason`.
* [Kredit fallback](/docs/id/build-with-claude/fallback-credit): bagaimana permintaan yang ditolak ditagih, dan cara menghindari membayar dua kali untuk caching prompt pada percobaan ulang.
* [Middleware SDK](/docs/id/cli-sdks-libraries/middleware): helper SDK yang membungkus semua ini.
* [Cookbook fallback dan penagihan](https://platform.claude.com/cookbook/fable-5-fallback-billing-guide): contoh lengkap dari awal hingga akhir.

Penyiapan paling sederhana, dalam beta di Claude API: atur `fallbacks` ke `"default"`, dan API mencoba ulang permintaan yang ditolak pada model fallback yang direkomendasikan Anthropic untuk kategori penolakannya. Untuk kategori tanpa fallback yang direkomendasikan, penolakan tetap berlaku.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": "default",
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.model'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks default \
    --beta server-side-fallback-2026-07-01 \
    --transform model --raw-output
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks="default",
      betas=["server-side-fallback-2026-07-01"],
  )
  print(response.model)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: "default",
    betas: ["server-side-fallback-2026-07-01"]
  });
  console.log(response.model);
  ```

  ```csharp C#
  AnthropicClient client = new();

  BetaMessage response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = new Default(),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  Console.WriteLine(response.Model.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: anthropic.BetaFallbacksParamOfDefault(),
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Model)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .fallbacksDefault()
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
      .build());

  IO.println(response.model().asString());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      fallbacks: 'default',
      betas: ['server-side-fallback-2026-07-01'],
  );

  echo $response->model, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: :default,
    betas: ["server-side-fallback-2026-07-01"]
  )

  puts response.model
  ```
</CodeGroup>

Bagian-bagian berikut membahas apa yang terkandung dalam respons penolakan, kapan menggunakan fallback sisi server atau sisi klien, dan bagaimana masing-masing ditagih.

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
* **`explanation`:** deskripsi yang dapat dibaca manusia. Teksnya tidak stabil, jadi tampilkan alih-alih mem-parsing-nya.
* Kedua field bernilai `null` ketika penolakan tidak terpetakan ke kategori bernama. Nilai `null` tersebut adalah nilai normal dan permanen, bukan placeholder.
* `stop_details` sendiri bernilai `null` untuk setiap stop reason selain `refusal`.

| `category`               | Artinya                                                                                                                                                                                                                                               |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"cyber"`                | Permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau exploit. Pekerjaan keamanan siber yang tidak berbahaya juga dapat memicu kategori ini.                                                                                  |
| `"bio"`                  | Permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya. Pekerjaan ilmu hayati yang bermanfaat juga dapat memicu kategori ini.                                                                                      |
| `"frontier_llm"`         | Permintaan dapat membantu pengembangan model AI pesaing, yang dibatasi berdasarkan [ketentuan komersial Anthropic](https://www.anthropic.com/legal/commercial-terms). Pekerjaan machine learning yang tidak berbahaya juga dapat memicu kategori ini. |
| `"reasoning_extraction"` | Permintaan meminta model untuk mereproduksi penalaran internalnya dalam teks respons. Untuk mendapatkan penalaran dalam bentuk terstruktur, gunakan [adaptive thinking](/docs/id/build-with-claude/thinking).                                         |
| `"general_harms"`        | Permintaan dapat terkait dengan area yang ditentukan sebagai berbahaya. Pekerjaan yang tidak berbahaya terkadang dapat memicu kategori ini.                                                                                                           |

Penolakan dapat tiba sebelum output apa pun, atau di tengah stream setelah output parsial. Dalam kedua kasus, perlakukan output parsial apa pun sebagai tidak lengkap dan buang.

<Note>
  **Bagaimana penolakan ditagih:** Anda tidak ditagih untuk penolakan yang tiba sebelum output apa pun. `content` kosong, dan jumlah token muncul di `usage` tetapi tidak dikenakan biaya. Permintaan tersebut tetap dihitung terhadap batas laju Anda. Penolakan di tengah stream menagih token input dan output yang sudah di-stream dengan tarif normal.
</Note>

## Memilih pendekatan fallback

Ada tiga cara untuk mencoba ulang permintaan yang ditolak pada model lain. Pilihan yang tepat bergantung pada di mana Anda berjalan dan seberapa banyak kontrol yang Anda butuhkan.

| Situasi Anda                                   | Gunakan                                                                                     | Alasan                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Claude API, penyiapan paling sederhana         | [Fallback sisi server](#server-side-fallback)                                               | Satu permintaan, satu respons. API menangani percobaan ulang.            |
| Platform apa pun, menggunakan SDK Anthropic    | [Middleware SDK](#client-side-fallback)                                                     | Konfigurasikan sekali di klien. Percobaan ulang terjadi secara otomatis. |
| HTTP mentah atau logika percobaan ulang kustom | Percobaan ulang manual dengan [kredit fallback](/docs/id/build-with-claude/fallback-credit) | Kontrol penuh. Kredit fallback menjaga biaya tetap rendah.               |

Fallback sisi server dan middleware SDK menerapkan kredit fallback untuk Anda. Anda hanya memerlukan halaman [Kredit fallback](/docs/id/build-with-claude/fallback-credit) ketika Anda membangun percobaan ulang sendiri.

## Fallback sisi server

Fallback sisi server mencoba ulang permintaan yang ditolak di dalam satu panggilan API. Dalam mode default, ketika model utama menolak dan kategori penolakan memiliki fallback yang direkomendasikan, API menjalankan permintaan yang sama pada model yang direkomendasikan Anthropic untuk kategori tersebut. Anda juga dapat menyebutkan hingga tiga model fallback Anda sendiri (di bawah). Dengan cara apa pun, Anda mendapatkan kembali satu respons yang menyebutkan model yang menjawab, sehingga pengguna Anda mendapatkan jawaban dalam satu perjalanan bolak-balik.

<Note>
  Fallback sisi server dalam beta di Claude API. Parameter `fallbacks` tidak didukung pada [Message Batches API](/docs/id/build-with-claude/batch-processing) (item batch yang menyertakannya kembali sebagai hasil error) dan tidak tersedia di Amazon Bedrock, Google Cloud, atau Microsoft Foundry. Pada platform tersebut, gunakan [fallback sisi klien dengan middleware SDK](#client-side-fallback) sebagai gantinya.
</Note>

### Membuat permintaan

Atur parameter `fallbacks` ke string `"default"` dan kirim header beta `server-side-fallback-2026-07-01`. API kemudian menerapkan perutean default yang ditentukan server untuk model yang diminta, yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan yang dilaporkan classifier, sehingga permintaan yang ditolak dilayani tanpa Anda perlu memelihara daftar model saat rekomendasi berubah.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": "default",
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' |
    jq -c '{
      stop_reason,
      model,
      # Entri fallback_message di usage.iterations berarti model fallback telah berjalan;
      # padukan dengan stop_reason untuk memastikan bahwa fallback yang melayani respons.
      served_by_fallback: (
        any(.usage.iterations[]?; .type == "fallback_message")
        and .stop_reason != "refusal"
      )
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks default \
    --beta server-side-fallback-2026-07-01 \
    --format json |
    jq -c '{
      stop_reason,
      model,
      # Entri fallback_message di usage.iterations berarti model fallback telah berjalan;
      # padukan dengan stop_reason untuk memastikan bahwa fallback yang melayani respons tersebut.
      served_by_fallback: (
        any(.usage.iterations[]?; .type == "fallback_message")
        and .stop_reason != "refusal"
      )
    }'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks="default",
      betas=["server-side-fallback-2026-07-01"],
  )

  # Entri fallback_message di usage.iterations berarti model fallback telah berjalan;
  # padukan dengan stop_reason untuk memastikan bahwa fallback yang melayani respons.
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
    fallbacks: "default",
    betas: ["server-side-fallback-2026-07-01"]
  });

  // Entri fallback_message di usage.iterations berarti model fallback telah dijalankan;
  // padukan dengan stop_reason untuk memastikan fallback yang melayani respons.
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
          Fallbacks = new Default(),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  // Entri fallback_message di usage.iterations menandakan model fallback telah berjalan;
  // padukan dengan stop_reason untuk memastikan fallback yang melayani respons tersebut.
  bool fallbackRan = (response.Usage.Iterations ?? []).Any(iteration =>
      iteration.TryPickBetaFallbackMessageIterationUsage(out _)
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
  	Fallbacks: anthropic.BetaFallbacksParamOfDefault(),
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
  })
  if err != nil {
  	panic(err)
  }

  // Entri fallback_message di usage.iterations menandakan model fallback telah dijalankan;
  // padukan dengan stop_reason untuk memastikan fallback yang melayani respons.
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
          .fallbacksDefault()
          .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
          .build()
  );

  // Entri penggunaan fallback_message berarti model fallback yang menghasilkan
  // respons; stop reason refusal berarti tidak ada model yang melayaninya.
  List<BetaUsage.Iteration> iterations =
      response.usage().iterations().orElse(List.of());
  boolean servedByFallback =
      iterations.stream().anyMatch(BetaUsage.Iteration::isFallbackMessage)
          && response.stopReason().filter(BetaStopReason.REFUSAL::equals).isEmpty();

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
      fallbacks: 'default',
      betas: ['server-side-fallback-2026-07-01'],
  );

  // Entri fallback_message di usage.iterations berarti model fallback telah berjalan;
  // padukan dengan stop_reason untuk memastikan fallback tersebut yang melayani respons.
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
    fallbacks: :default,
    betas: ["server-side-fallback-2026-07-01"]
  )

  # Entri fallback_message di usage.iterations berarti model fallback telah berjalan;
  # padukan dengan stop_reason untuk memastikan bahwa fallback yang melayani respons tersebut.
  iterations = response.usage.iterations || []
  served_by_fallback = iterations.any? { it.type == :fallback_message } &&
    response.stop_reason != :refusal

  stop_reason = response.stop_reason
  model = response.model
  puts JSON.generate({stop_reason:, model:, served_by_fallback:})
  ```
</CodeGroup>

Anthropic menetapkan pengamanan untuk setiap model secara individual dan untuk setiap kategori kebijakan, sesuai dengan kemampuan model: bergantung pada kategorinya, permintaan yang ditandai dapat dialihkan ke model yang kurang mampu atau ditolak. Mode `"default"` mengkodekan rekomendasi per-model, per-kategori ini untuk Anda, sehingga permintaan yang ditolak dicoba ulang pada model yang direkomendasikan Anthropic untuk kategori tersebut. Fallback terlihat dengan cara apa pun: respons menyebutkan model yang melayaninya, dan blok konten `fallback` menandai peralihan.

Perutean diterapkan di sisi server dan tidak dipublikasikan per model pada [Models API](/docs/id/api/models/list). Untuk melihat model mana yang melayani permintaan yang ditolak, periksa field `model` tingkat atas pada respons dan cari entri `fallback_message` di `usage.iterations`, seperti yang dilakukan contoh-contoh di halaman ini.

Hanya penolakan safety classifier yang memicu fallback. Batas laju, kelebihan beban, atau error server pada model yang diminta dikembalikan kepada Anda apa adanya.

<Note>
  Header beta harus membawa tepat tanggal `2026-07-01`, yang mendukung baik `"default"` maupun bentuk daftar eksplisit di bawah, atau `2026-06-01`, yang hanya menerima bentuk daftar eksplisit. Di bawah nilai `server-side-fallback-*` lainnya, parameter `fallbacks` ditolak dengan error 400. Jika Anda membangun berdasarkan pratinjau awal fitur ini, perbarui header beta serta bentuk permintaan dan respons secara bersamaan ke yang ada di halaman ini.
</Note>

### Menyebutkan model fallback Anda sendiri

Alih-alih perutean default, Anda dapat mengatur `fallbacks` ke daftar hingga tiga model. Ketika model yang diminta menolak, API menjalankan model berikutnya dalam rantai pada permintaan yang sama. Gunakan bentuk ini ketika Anda ingin mengontrol secara tepat model mana yang melayani permintaan yang ditolak, seperti menetapkan model yang telah dikualifikasi oleh aplikasi Anda.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.model'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-07-01 \
    --transform model --raw-output
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-07-01"],
  )
  print(response.model)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-07-01"]
  });
  console.log(response.model);
  ```

  ```csharp C#
  AnthropicClient client = new();

  BetaMessage response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = new([new(Messages::Model.ClaudeOpus4_8)]),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  Console.WriteLine(response.Model.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: anthropic.BetaFallbacksParamUnion{
  		OfBetaFallbackArray: []anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Model)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .fallbacksOfFallbackParams(List.of(BetaFallbackParam.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .build()))
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
      .build());

  IO.println(response.model().asString());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-07-01'],
  );

  echo $response->model, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-07-01"]
  )

  puts response.model
  ```
</CodeGroup>

Beberapa aturan berlaku untuk daftar `fallbacks`:

* Entri dicoba secara berurutan. Masing-masing harus berbeda dari entri lainnya dan dari model yang diminta.
* Setiap entri harus merupakan salah satu target yang diizinkan untuk model yang diminta. Dengan header beta diatur, daftar tersebut dipublikasikan sebagai `allowed_fallback_models` pada entri model di [Models API](/docs/id/api/models/list).
* Setiap entri menyebutkan `model` dan dapat menimpa `max_tokens`, `thinking`, `output_config`, dan `speed` hanya untuk percobaan tersebut.
* Permintaan harus valid sebagai permintaan langsung ke setiap model yang disebutkan. Jika model fallback tidak mendukung fitur yang digunakan permintaan, API menolak permintaan di awal.
* Seperti pada mode default, hanya penolakan safety classifier yang memicu fallback. Batas laju, kelebihan beban, atau error server pada model yang diminta dikembalikan kepada Anda apa adanya.

Bentuk daftar eksplisit juga berfungsi di bawah header beta `server-side-fallback-2026-06-01`; mode `"default"` tidak.

Respons memiliki bentuk yang sama dalam kedua mode: model yang melayani giliran muncul di field `model` tingkat atas, blok konten `fallback` menandai peralihan, dan `usage.iterations` mencatat setiap percobaan.

### Apa yang terkandung dalam respons

Respons terlihat seperti pesan lainnya, dengan dua tambahan:

* Field `model` tingkat atas melaporkan model yang menghasilkan pesan yang dikembalikan, baik itu model yang diminta maupun fallback.

* Blok konten `fallback` menandai setiap titik dalam `content` di mana output satu model beralih ke model berikutnya: `{"type": "fallback", "from": {"model": ...}, "to": {"model": ...}}`.

  * `from.model` menggemakan string model yang Anda kirim ketika hop yang menolak adalah model yang diminta.
  * `to.model` selalu merupakan ID yang telah diselesaikan dari model yang melanjutkan.

Pada penolakan sebelum output apa pun, blok `fallback` adalah blok konten pertama. Misalnya, ketika perutean default memilih Claude Opus 4.8 untuk kategori penolakan tersebut:

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

Array `usage.iterations` mencatat setiap percobaan. Model yang menolak muncul sebagai entri `message` biasa, dan model yang melayani giliran muncul sebagai entri `fallback_message`. Jika setiap model dalam rantai menolak, responsnya adalah penolakan model terakhir, dengan entri `message` untuk setiap hop sebelumnya dan entri `fallback_message` untuk yang terakhir.

### Melanjutkan percakapan

Pada giliran berikutnya, kirim kembali konten assistant seperti yang Anda terima. Setelah fallback di tengah output, `content` dapat menyertakan tipe blok yang dihasilkan model yang menolak sebelum peralihan; tabel berikut membahas mana yang harus dipertahankan dan mana yang harus dibuang ketika Anda menggemakan giliran tersebut.

| Tipe blok                                                                               | Pada giliran berikutnya                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fallback`                                                                              | Pertahankan tepat di tempat ia muncul. API menggunakan posisinya untuk memvalidasi blok thinking di sekitarnya, sehingga permintaan yang menggemakan blok thinking dari kedua sisi batas akan ditolak jika blok tersebut dihilangkan atau dipindahkan. |
| `text`                                                                                  | Pertahankan.                                                                                                                                                                                                                                           |
| Blok apa pun setelah blok `fallback` terakhir                                           | Pertahankan.                                                                                                                                                                                                                                           |
| `thinking`, `redacted_thinking`, atau `connector_text` sebelum blok `fallback` terakhir | Buang.                                                                                                                                                                                                                                                 |
| `tool_use` sisi klien sebelum blok `fallback` terakhir                                  | Buang.                                                                                                                                                                                                                                                 |
| `server_tool_use` sebelum blok `fallback` terakhir                                      | Pertahankan ketika dipasangkan dengan hasilnya. Buang ketika tidak memiliki hasil yang cocok.                                                                                                                                                          |

<Note>
  Blok `connector_text` membawa teks narasi yang disertakan beberapa respons penggunaan alat di antara panggilan alat.
</Note>

### Streaming

Pada permintaan streaming, percobaan ulang terjadi pada stream yang sama, dan tidak ada yang sudah Anda terima yang menjadi tidak valid. Apa yang Anda lihat bergantung pada kapan penolakan terjadi.

**Ketika penolakan terjadi sebelum output apa pun:**

* `message_start` menyebutkan model fallback, dan blok `fallback` adalah blok konten pertama.
* Karena `message_start` menunggu percobaan fallback dimulai, waktu ke byte pertama mencakup percobaan yang ditolak.

**Ketika penolakan terjadi di tengah output:**

* Blok konten yang terbuka ditutup, dan blok `fallback` (pasangan `content_block_start` dan `content_block_stop` biasa tanpa delta) menandai batasnya.
* Model fallback melanjutkan dari output parsial. Hanya blok `text` dari output parsial yang diteruskan ke model fallback sebagai konteks; tipe blok lainnya tetap berada di `content`.
* `message_start` sudah menyebutkan model yang diminta, jadi baca model yang melayani dari `to.model` pada blok `fallback` dan dari entri `fallback_message` di `usage.iterations` pada `message_delta` terakhir.

### Respons non-streaming

Pada permintaan non-streaming, penolakan di tengah output berperilaku berbeda: respons menghilangkan output parsial dari model yang menolak, dan model fallback menjawab dari awal. Hasilnya terlihat seperti penolakan sebelum output apa pun, dengan blok `fallback` di urutan pertama. Percobaan yang ditolak dan token output-nya tetap muncul di `usage.iterations`.

<Note>
  **Penolakan selama penggunaan alat:** pekerjaan alat yang telah selesai tidak menghalangi fallback. Ketika penolakan terjadi setelah alat server (misalnya, pencarian web atau eksekusi kode) selesai dieksekusi dalam sebuah permintaan, percobaan fallback tetap berjalan: hasil alat yang telah selesai terbawa, dan model fallback dapat terus memanggil alat server. Satu-satunya kasus yang tidak dicoba ulang adalah penolakan streaming yang terjadi saat blok tool-use dari tipe apa pun (alat klien, alat server, atau panggilan alat MCP) masih terbuka pada stream: penolakan tersebut dikembalikan secara langsung, dan jika header `fallback-credit-2026-07-01` diatur, penolakan tersebut tetap membawa token kredit yang dapat ditukarkan dengan melanjutkan respons parsial. Permintaan non-streaming tidak terpengaruh; API membersihkan pekerjaan parsial dan mencoba ulang sebelum merespons.
</Note>

<Accordion title="Perutean sticky">
  Setelah percakapan mengalami fallback, API mencatat model mana yang melayaninya. Permintaan berikutnya untuk percakapan tersebut yang menyertakan `fallbacks` langsung menuju model fallback tersebut, tanpa menjalankan model yang diminta. Ini menghindari pembayaran untuk percobaan yang dapat diprediksi akan ditolak lagi pada setiap giliran.

  Beberapa properti dari keputusan perutean:

  * Disimpan selama kurang lebih 1 jam dan dibatasi pada organisasi Anda.
  * Disimpan sebagai hash konten dari prefiks percakapan ditambah model yang melayaninya. Konten pesan itu sendiri tidak disimpan.
  * Bersifat best-effort, jadi kode Anda harus menangani kemungkinan model yang diminta dicoba lagi kapan saja.

  Giliran yang dilayani secara sticky tidak membawa blok konten `fallback`, karena tidak ada model yang menolak giliran tersebut. Identifikasi melalui entri `fallback_message` di `usage.iterations`, tidak adanya entri `message` untuk model yang diminta, dan field `model` pada respons.

  Perutean sticky berlaku untuk permintaan streaming maupun non-streaming. Pada permintaan streaming, keputusan perutean dibuat sebelum stream dibuka, sehingga field `model` pada event `message_start` sudah membawa ID model fallback.
</Accordion>

<Accordion title="Bagaimana fallback sisi server ditagih">
  Anda membayar untuk model yang benar-benar melayani permintaan. Percobaan yang menolak sebelum menghasilkan output tidak ditagih: token-nya dilaporkan pada entri `usage.iterations`-nya tetapi tidak dikenakan biaya. Percobaan yang ditolak tetap dihitung terhadap batas laju (lihat di bawah).

  Setiap percobaan ditagih secara terpisah, dengan tarif model yang menjalankannya. Array `usage.iterations` adalah catatan per-percobaan dari apa yang Anda bayar. Jumlah `usage` tingkat atas hanya menggambarkan percobaan yang menghasilkan pesan yang dikembalikan; token dari model yang berbeda tidak pernah dijumlahkan ke dalam satu field.

  Setiap percobaan yang berjalan dihitung terhadap batas laju modelnya sendiri. Jika model fallback terkena batas laju atau kelebihan beban, percobaan fallback tidak dilakukan dan penolakan sebelumnya dikembalikan sebagai gantinya. Sesuaikan batas laju model fallback untuk volume penolakan yang Anda perkirakan, atau fallback akan terdegradasi menjadi penolakan saat beban tinggi.

  Ketika percobaan fallback dilewati dengan cara ini, `stop_details.recommended_model` menyebutkan model untuk dicoba ulang secara langsung. Rekomendasi tersebut adalah petunjuk, bukan jaminan, dan bernilai `null` ketika tidak ada rekomendasi yang tersedia.
</Accordion>

## Fallback sisi klien dengan middleware SDK

Setiap SDK Anthropic menyertakan middleware refusal-fallback. Anda mengonfigurasinya sekali di klien dengan daftar model fallback Anda. Panggilan melalui `client.beta.messages` kemudian mencoba ulang permintaan yang ditolak secara otomatis, di platform apa pun. Middleware juga mengirimkan header beta `fallback-credit-2026-07-01` pada setiap permintaan yang ditanganinya, sehingga percobaan ulang dihargai ulang tanpa penyiapan per-permintaan.

### Menyiapkannya

Berikan middleware ke konstruktor klien, dan bagikan satu instans `BetaFallbackState` di seluruh permintaan dalam sebuah percakapan.

<CodeGroup>
  ```bash cURL
  # Middleware refusal-fallback adalah fitur SDK. Lihat bagian
  # fallback sisi server untuk pendekatan permintaan tunggal yang setara,
  # atau halaman kredit fallback untuk pola retry HTTP mentah.
  ```

  ```bash CLI
  # Middleware refusal-fallback adalah fitur SDK. Lihat bagian
  # fallback sisi server untuk pendekatan permintaan-tunggal yang setara,
  # atau halaman kredit fallback untuk pola retry HTTP mentah.
  ```

  ```python Python
  from anthropic import Anthropic, BetaFallbackState, BetaRefusalFallbackMiddleware

  # Saat terjadi penolakan, middleware mencoba ulang pada model fallback yang terdaftar dan
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
      for text in stream.text_stream:
          print(text, end="", flush=True)
      final_message = stream.get_final_message()
  print(f"\nserved by: {final_message.model}")

  # Non-streaming: menggunakan kembali state menjaga percakapan tetap terpaku (pinned).
  with state:
      message = client.beta.messages.create(
          max_tokens=1024,
          model="claude-fable-5",
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
  print(f"served by: {message.model}")
  ```

  ```typescript TypeScript
  import { BetaFallbackState, betaRefusalFallbackMiddleware } from "@anthropic-ai/sdk";

  // Saat terjadi penolakan, middleware mencoba ulang pada model fallback yang terdaftar dan
  // secara otomatis mengirim header beta fallback-credit pada setiap permintaan yang ditanganinya.
  const client = new Anthropic({
    middleware: [betaRefusalFallbackMiddleware([{ model: "claude-opus-4-8" }])]
  });

  // Bagikan satu state di sepanjang percakapan agar permintaan lanjutan tetap
  // terpaku pada model yang menerima.
  const fallbackState = new BetaFallbackState();

  // Streaming: saat terjadi penolakan, middleware mencoba ulang pada model fallback dan
  // menyambungkan event-nya ke stream yang sedang terbuka.
  const stream = client.beta.messages
    .stream(
      {
        max_tokens: 1024,
        model: "claude-fable-5",
        messages: [{ role: "user", content: "Hello, Claude" }]
      },
      { fallbackState }
    )
    .on("text", (text) => process.stdout.write(text));

  const finalMessage = await stream.finalMessage();
  console.log("\nserved by:", finalMessage.model);

  // Non-streaming: menggunakan kembali state menjaga percakapan tetap terpaku.
  const message = await client.beta.messages.create(
    {
      max_tokens: 1024,
      model: "claude-fable-5",
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  console.log("served by:", message.model);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Helpers;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  // Saat terjadi penolakan, handler mencoba ulang pada model fallback yang terdaftar dan
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

  // Streaming: jika stream berakhir dengan penolakan, handler menyambungkan event
  // dari model fallback ke stream yang masih terbuka.
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

  // Non-streaming: menggunakan kembali state menjaga percakapan tetap tersemat pada model yang menerima.
  using (fallbackState.Use())
  {
      BetaMessage message = await client.Beta.Messages.Create(parameters);
      Console.WriteLine($"served by: {message.Model.Raw()}");
  }
  ```

  ```go Go
  import (
  // ...
  	"github.com/anthropics/anthropic-sdk-go/lib/betafallback"
  // ...
  )

  func main() {
  	ctx := context.Background()

  	// Middleware mencoba ulang permintaan yang ditolak pada tiap model
  	// fallback bergiliran, dan otomatis mengikutkan permintaan ke beta fallback-credit.
  	client := anthropic.NewClient(
  		option.WithMiddleware(betafallback.BetaRefusalFallbackMiddleware(
  			[]anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  		)),
  	)

  	// Satu state per percakapan: permintaan yang memakainya tetap terkunci ke
  	// model yang menerima, sehingga lanjutan tak pernah menanyai lagi model yang menolak.
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
  	// event model fallback ke stream yang terbuka sebagai satu pesan berkesinambungan.
  	stream := client.Beta.Messages.NewStreaming(ctx, params, conversation)
  	defer stream.Close()
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

  	// Non-streaming: state bersama mengunci lanjutan ini ke model yang
  	// melayani giliran yang di-streaming.
  	message, err := client.Beta.Messages.New(ctx, params, conversation)
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println("served by:", message.Model)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.RequestOptions;
  import com.anthropic.core.http.StreamResponse;
  import com.anthropic.helpers.BetaFallbackState;
  import com.anthropic.helpers.BetaMessageAccumulator;
  import com.anthropic.helpers.BetaRefusalFallbackInterceptor;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaRawMessageStreamEvent;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      // Interceptor mencoba ulang permintaan yang ditolak pada model fallback. Interceptor secara otomatis
      // menambahkan header beta fallback-credit ke setiap permintaan yang ditanganinya.
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .fromEnv()
          .addInterceptor(BetaRefusalFallbackInterceptor.builder()
              .addFallback(Model.CLAUDE_OPUS_4_8)
              .build())
          .build();

      // Bagikan satu state di seluruh permintaan agar permintaan lanjutan tetap terikat pada model yang menerima.
      BetaFallbackState state = BetaFallbackState.create();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_FABLE_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build();

      // Streaming: saat terjadi penolakan, event dari model fallback disambungkan ke stream yang terbuka.
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
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaRawContentBlockDeltaEvent;
  use Anthropic\Beta\Messages\BetaTextDelta;
  use Anthropic\Client;
  use Anthropic\Lib\Middleware\BetaFallbackState;
  use Anthropic\Lib\Middleware\RefusalFallbackMiddleware;
  use Anthropic\Lib\Streaming\MessageAccumulator;

  // Konfigurasikan rantai fallback sekali saja. Saat terjadi penolakan, middleware mencoba ulang
  // permintaan ke model berikutnya dalam rantai dan mengirimkan header beta fallback-credit untuk Anda.
  $client = new Client(
      requestOptions: [
          'middleware' => [new RefusalFallbackMiddleware([['model' => 'claude-opus-4-8']])],
      ],
  );

  // Gunakan satu state yang sama di sepanjang percakapan agar permintaan lanjutan tetap terikat
  // pada model yang menerima.
  $state = new BetaFallbackState();

  // Streaming: saat terjadi penolakan, middleware menyambungkan event dari model fallback
  // ke stream yang masih terbuka. Model pada akumulator adalah model yang melayani.
  $stream = $client->beta->messages->createStream(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      requestOptions: ['fallbackState' => $state],
  );
  $accumulator = MessageAccumulator::forBetaMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
      if ($event instanceof BetaRawContentBlockDeltaEvent
          && $event->delta instanceof BetaTextDelta) {
          echo $event->delta->text;
      }
  }
  echo "\nserved by: {$accumulator->message()->model}\n";

  // Non-streaming: middleware yang sama. Menggunakan kembali state menjaga percakapan
  // tetap terikat pada model yang menerima.
  $message = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      requestOptions: ['fallbackState' => $state],
  );
  echo "served by: {$message->model}\n";
  ```

  ```ruby Ruby
  # Saat terjadi penolakan, middleware mencoba ulang permintaan melalui rantai fallback.
  # Middleware ini mengirimkan header beta fallback-credit pada setiap permintaan yang ditanganinya.
  client = Anthropic::Client.new(
    middleware: [Anthropic::BetaRefusalFallbackMiddleware.new([{model: "claude-opus-4-8"}])]
  )

  # Gunakan satu state yang sama di sepanjang percakapan agar permintaan lanjutan tetap
  # terikat pada model yang menerima.
  state = Anthropic::BetaFallbackState.new

  # Streaming: saat terjadi penolakan, middleware menyambungkan event dari model
  # fallback ke stream yang masih terbuka.
  stream = client.beta.messages.stream(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {fallback_state: state}
  )
  stream.text.each { print it }
  puts "\nserved by: #{stream.accumulated_message.model}"

  # Non-streaming: menggunakan kembali state menjaga percakapan tetap terikat pada model yang menerima.
  message = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {fallback_state: state}
  )
  puts "served by: #{message.model}"
  ```
</CodeGroup>

### Bagaimana perilakunya

* Percobaan ulang menelusuri daftar fallback Anda secara berurutan. Model fallback yang juga menolak meneruskan permintaan ke entri berikutnya.
* Ketika setiap model dalam daftar telah menolak, middleware mengembalikan penolakan terakhir (respons penolakan model terakhir) alih-alih memunculkan error.
* [Blok thinking dari Claude Fable 5](/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) diteruskan tanpa perubahan: setiap percobaan ulang mengirim ulang body permintaan asli Anda, dan satu-satunya blok yang dihapus middleware dari riwayat percakapan pada permintaan berikutnya adalah blok batas `fallback` yang ditambahkannya sendiri.
* Respons yang dilayani melalui middleware menyertakan blok konten `fallback` pada setiap batas model, sama seperti respons fallback sisi server. Middleware mengelola blok-blok tersebut untuk Anda pada permintaan berikutnya.
* Model yang menerima dicatat di `BetaFallbackState`, sehingga permintaan lanjutan yang berbagi state tersebut tetap terikat padanya alih-alih menanyakan kembali model yang menolak.

<Note>
  Middleware dan parameter `fallbacks` sisi server melakukan pekerjaan yang sama. Konfigurasikan salah satunya, jangan pernah keduanya pada permintaan yang sama. Untuk mengirim permintaan `fallbacks` sisi server dari aplikasi yang memasang middleware, gunakan instans klien terpisah tanpa middleware tersebut.
</Note>

<Accordion title="Menulis percobaan ulang sendiri">
  Melalui HTTP mentah atau dengan logika percobaan ulang kustom, implementasikan pola yang dibungkus oleh middleware:

  <Steps>
    <Step title="Deteksi penolakan">
      Periksa respons untuk `stop_reason: "refusal"`.
    </Step>

    <Step title="Kirim ulang pada model fallback">
      Kirim permintaan yang sama dengan `model` diatur ke model fallback, seperti Claude Opus 4.8. Permintaan yang ditolak oleh classifier Claude Fable 5 biasanya dapat dilayani oleh model lain. Cara Anda menangani riwayat percakapan bergantung pada apakah Anda menukarkan [kredit fallback](/docs/id/build-with-claude/fallback-credit):

      * **Tidak menukarkan kredit:** Anda dapat terlebih dahulu menghapus [blok thinking dari Claude Fable 5](/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) dari riwayat percakapan. Model lain mengabaikannya, dan penghapusan menjaga permintaan lintas model tetap minimal.
      * **Menukarkan kredit:** kirim body tanpa perubahan, karena penukaran memerlukan kecocokan yang persis.
    </Step>

    <Step title="Tetap pada model fallback">
      Untuk percakapan multi-giliran, terus gunakan model fallback untuk giliran berikutnya alih-alih beralih kembali.
    </Step>
  </Steps>

  Percobaan ulang manual menulis cache prompt model fallback dari awal, yang biayanya lebih besar daripada membaca cache yang sudah ada. [Kredit fallback](/docs/id/build-with-claude/fallback-credit) mengembalikan biaya tersebut; tukarkan pada setiap percobaan ulang yang Anda bangun sendiri.
</Accordion>

## Penolakan dalam Message Batches

Permintaan yang ditolak dalam [Message Batch](/docs/id/build-with-claude/batch-processing) kembali sebagai `result.type: "succeeded"` dengan `stop_reason: "refusal"`. Hasil batch membawa objek `stop_details` yang sama dengan respons sinkron, sehingga Anda dapat mendeteksi penolakan melalui `stop_reason` atau `stop_details.type`. Satu perbedaan: penolakan batch tidak menghasilkan kredit fallback, sehingga `stop_details` pada hasil batch tidak pernah menyertakan `fallback_credit_token`.

Fallback sisi server tidak tersedia untuk batch (permintaan batch yang menyertakan `fallbacks` menghasilkan hasil error per-item). Untuk mencoba ulang item batch yang ditolak:

1. Kumpulkan item yang ditolak dari hasil.
2. Hapus blok thinking Claude Fable 5 dari riwayat multi-giliran apa pun.
3. Kirim ulang pada model fallback sebagai batch baru atau sebagai permintaan langsung.

## Jebakan umum

* **Coba ulang pada model yang berbeda.** Mengirim ulang permintaan yang ditolak ke model yang sama biasanya menghasilkan penolakan lagi. Arahkan percobaan ulang ke model fallback.
* **Anggarkan percobaan ulang per permintaan, bukan per giliran atau per sesi.** Satu giliran dapat menghasilkan beberapa penolakan, misalnya sebuah agen beserta sub-agennya.
* **Konfigurasikan fallback pada setiap jalur permintaan.** Handler percobaan ulang, cabang pemulihan error, dan worker latar belakang semuanya membutuhkannya. Handler yang mengeluarkan ulang permintaan tanpa fallback kehilangan perlindungan tepat pada permintaan yang paling mungkin membutuhkannya.
* **Berikan panggilan sub-agen fallback-nya sendiri.** Parameter `fallbacks` tidak menyebar ke panggilan model yang dibuat dari dalam eksekusi alat.
* **Jadikan fallback sebagai properti permintaan, bukan state ambien.** Flag bersama, nilai konfigurasi yang di-cache, atau toggle global dapat menjadi tidak sinkron dan diam-diam membiarkan permintaan tidak terlindungi. Ketika Anda tidak dapat memastikan fallback aktif, konfigurasikan alih-alih mengasumsikannya aktif.
* **Instrumentasikan penolakan sebagai sinyal tersendiri.** Penolakan adalah HTTP 200, sehingga pemantauan yang dibangun berdasarkan tingkat error atau respons 5xx tidak pernah melihatnya. Keluarkan satu event per penolakan dan satu per respons yang dilayani fallback (entri `fallback_message` di `usage.iterations` menandai yang terakhir), lalu buat peringatan pada selisih antara kedua hitungan tersebut.
* **Bercabang berdasarkan `stop_reason` atau `stop_details.type`, bukan berdasarkan `content` atau field dalam `stop_details`.** Objek `stop_details` selalu ada pada penolakan, tetapi field `category` dan `explanation`-nya dapat bernilai `null`. Periksa `stop_reason` yang sama dengan `"refusal"` secara langsung.

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
    Pindahkan aplikasi yang ada ke Claude Fable 5.
  </Card>
</CardGroup>
