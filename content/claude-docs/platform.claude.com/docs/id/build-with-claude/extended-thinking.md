---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-09-29T02:22:52.185218Z
sha256: d2d256e5f727dd78de72b671c8f4b8707553abeff9b5117db26e4142384e9577
---

---
title: Pemikiran diperpanjang
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
description: Konfigurasikan pemikiran diperpanjang manual dengan anggaran budget_tokens tetap pada model Claude yang mendukungnya, lalu bermigrasi ke pemikiran adaptif.
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

<Warning>
  "Extended thinking" (pemikiran diperpanjang) (`thinking.type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated) pada model Claude 4.6 (permintaan yang menggunakannya masih berhasil). Claude 4.7 dan model yang lebih baru tidak mendukungnya dan menolak permintaan yang menggunakannya, dengan mengembalikan error 400. Pada Claude 4.5 dan model sebelumnya yang mendukung thinking, pemikiran diperpanjang adalah satu-satunya mode thinking yang tersedia. Claude Mythos Preview mendukung kedua mode tersebut. Jika kedua mode tersedia, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) sebagai gantinya.

  Lihat [Bermigrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) untuk beralih ke pemikiran adaptif. Jika model Anda hanya mendukung pemikiran diperpanjang, halaman ini menjelaskan konfigurasi yang didukung. Anda tidak perlu mengubah apa pun sampai Anda beralih ke model yang lebih baru.
</Warning>

<Note>
  Jika permintaan gagal dengan error 400 yang pesannya diawali dengan `"thinking.type.enabled" is not supported`, berarti model Anda menggunakan pemikiran adaptif. Lihat [Pemecahan masalah pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-enabled), atau langsung ke [Bermigrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking).
</Note>

"Extended thinking" (pemikiran diperpanjang) dalam mode manual memberi Anda kendali langsung atas seberapa banyak Claude berpikir. Anda menetapkan anggaran token pemikiran pada setiap permintaan dengan `thinking: {type: "enabled", budget_tokens: N}`, dan Claude berpikir dalam batas anggaran tersebut sebelum mulai menyusun jawaban akhirnya. Mode manual tetap berguna ketika beban kerja Anda memerlukan "latency" (latensi) yang dapat diprediksi atau kendali yang presisi atas biaya pemikiran. Halaman ini membahas cara menetapkan dan menyetel anggaran, interaksi mode manual dengan "interleaved thinking" (pemikiran berselang-seling) dan "prompt caching" (caching prompt), serta cara bermigrasi ke "adaptive thinking" (pemikiran adaptif).

Untuk mempelajari cara kerja pemikiran itu sendiri, termasuk blok pemikiran dan bentuk respons, parameter `display`, streaming, pemikiran dengan "tool use" (penggunaan alat), dan enkripsi, lihat [ikhtisar pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking).

## Model yang didukung

Ketersediaan pemikiran diperpanjang untuk setiap model, termasuk model yang hanya mendukung mode pemikiran diperpanjang, tercantum dalam [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models).

## Cara menggunakan pemikiran diperpanjang

Berikut adalah contoh penggunaan pemikiran diperpanjang di Messages API:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
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
    --format yaml <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  messages:
    - role: user
      content: Are there an infinite number of prime numbers such that n mod 4 == 3?
  YAML
  ```

  ```python Python
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
      match block.type:
          case "thinking":
              print(f"\nThinking summary: {block.thinking}")
          case "text":
              print(f"\nResponse: {block.text}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000,
    },
    messages: [
      {
        role: "user",
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?",
      },
    ],
  });

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  for (const block of response.content) {
    switch (block.type) {
      case "thinking":
        console.log(`\nThinking summary: ${block.thinking}`);
        break;
      case "text":
        console.log(`\nResponse: ${block.text}`);
        break;
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Are there an infinite number of prime numbers such that n mod 4 == 3?",
          },
      ],
  });

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  foreach (var block in response.Content)
  {
      if (block.TryPickThinking(out var thinking))
      {
          Console.WriteLine($"\nThinking summary: {thinking.Thinking}");
      }
      else if (block.TryPickText(out var text))
      {
          Console.WriteLine($"\nResponse: {text.Text}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
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

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  for _, block := range response.Content {
  	switch block := block.AsAny().(type) {
  	case anthropic.ThinkingBlock:
  		fmt.Printf("\nThinking summary: %s", block.Thinking)
  	case anthropic.TextBlock:
  		fmt.Printf("\nResponse: %s", block.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(16_000)
          .enabledThinking(10_000)
          .addUserMessage("Are there an infinite number of prime numbers such that n mod 4 == 3?")
          .build();

      var response = client.messages().create(params);

      // Respons berisi blok pemikiran yang diringkas dan blok teks
      for (var block : response.content()) {
          block.thinking().ifPresent(thinkingBlock ->
              IO.println("\nThinking summary: " + thinkingBlock.thinking())
          );
          block.text().ifPresent(textBlock ->
              IO.println("\nResponse: " + textBlock.text())
          );
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 16000,
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
      messages: [
          [
              'role' => 'user',
              'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?',
          ],
      ],
  );

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  foreach ($response->content as $block) {
      echo match (true) {
          $block instanceof \Anthropic\Messages\ThinkingBlock => "\nThinking summary: {$block->thinking}",
          $block instanceof \Anthropic\Messages\TextBlock => "\nResponse: {$block->text}",
          default => '',
      };
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 16_000,
    thinking: {
      type: :enabled,
      budget_tokens: 10_000
    },
    messages: [
      {
        role: :user,
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      }
    ]
  )

  # Respons berisi blok pemikiran yang diringkas dan blok teks
  response.content.each do |block|
    case block
    when Anthropic::Models::ThinkingBlock
      puts "\nThinking summary: #{block.thinking}"
    when Anthropic::Models::TextBlock
      puts "\nResponse: #{block.text}"
    end
  end
  ```
</CodeGroup>

Untuk mengaktifkan pemikiran diperpanjang manual, tambahkan objek `thinking` dengan `type` bernilai `enabled` beserta nilai `budget_tokens`.

Parameter `budget_tokens` menetapkan target jumlah token yang dapat digunakan Claude untuk proses penalaran internalnya. Anggaran yang lebih besar dapat meningkatkan kualitas respons karena memungkinkan analisis yang lebih menyeluruh untuk masalah yang kompleks.

## Aturan dan penyetelan anggaran

`budget_tokens` harus memenuhi batasan berikut:

* **Minimal 1.024 token.** API menolak nilai yang lebih kecil.
* **Kurang dari `max_tokens`.** Token pemikiran dihitung dalam batas `max_tokens` untuk giliran tersebut, sehingga anggaran harus menyisakan ruang untuk respons akhir. Satu-satunya pengecualian adalah [pemikiran berselang-seling](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#interleaved-thinking). Di sana, `budget_tokens` boleh melebihi `max_tokens` karena anggaran tersebut mencakup semua blok pemikiran dalam satu giliran asisten.
* **Tanpa pre-warming cache.** Karena `budget_tokens` harus kurang dari `max_tokens`, pemikiran diperpanjang tidak dapat digabungkan dengan `max_tokens: 0` ([pre-warming cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache)).

Anggaran ini adalah target, bukan batas yang ketat. Penggunaan token yang sebenarnya bervariasi sesuai tugas, dan Claude dapat berhenti bernalar jauh sebelum anggaran habis. `max_tokens` tetap menjadi batas mutlak untuk total output.

Pada Claude Opus 4.5, satu-satunya model khusus pemikiran diperpanjang yang mendukung [effort](https://platform.claude.com/docs/id/build-with-claude/effort), effort membentuk respons secara keseluruhan, sedangkan `budget_tokens` menetapkan kedalaman pemikiran. Tetapkan keduanya.

Untuk menyetel anggaran:

* Sesuaikan titik awal dengan tugasnya. Untuk tugas sederhana, mulailah di sekitar batas minimum 1.024 token, lalu naikkan secara bertahap untuk menemukan rentang optimal bagi kasus penggunaan Anda. Untuk tugas kompleks, mulailah dengan anggaran yang lebih besar, yaitu 16.000 token atau lebih, lalu sesuaikan dengan kebutuhan latensi dan kualitas Anda. Anggaran yang lebih tinggi memungkinkan penalaran yang lebih komprehensif, tetapi manfaat tambahannya makin berkurang tergantung tugasnya, dan latensinya meningkat. Untuk tugas penting, uji berbagai pengaturan untuk menemukan keseimbangan yang tepat.
* Untuk anggaran pemikiran di atas 32k, gunakan [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Mendorong model berpikir melebihi 32k token menghasilkan permintaan yang berjalan lama, yang dapat terkena timeout sistem dan batas koneksi terbuka.

Untuk melacak biaya sebenarnya dari suatu anggaran, pantau field `usage.output_tokens_details.thinking_tokens` dalam respons. Field ini melaporkan berapa banyak token output yang ditagih yang merupakan penalaran internal. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir.

Jika Anda siap meninggalkan anggaran manual, lihat [Bermigrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking).

## Pemikiran berselang-seling dalam mode manual

Pemikiran berselang-seling memungkinkan Claude berpikir di antara pemanggilan alat dalam satu giliran asisten, sehingga Claude dapat menalar setiap hasil alat sebelum memutuskan langkah berikutnya. Untuk konsepnya, struktur giliran, dan perilakunya pada model pemikiran adaptif, lihat [pemikiran berselang-seling](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) di ikhtisar pemikiran. Bagian ini membahas cara mengaktifkannya saat Anda menggunakan pemikiran manual `type: "enabled"`.

Pada Claude Opus 4.5, Claude Sonnet 4.5, dan model Claude 4 yang lebih lama, tambahkan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda.

Generasi 4.6 berperilaku berbeda dalam mode manual:

* **Claude Sonnet 4.6**: header beta dengan `type: "enabled"` manual masih berfungsi, tetapi sudah deprecated. Sebaiknya gunakan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking), yang berselang-seling secara otomatis tanpa header.
* **Claude Opus 4.6**: mode manual sama sekali tidak mendukung pemikiran berselang-seling. Hanya mode adaptifnya yang berselang-seling, jadi beralihlah ke `thinking: {type: "adaptive"}` jika Anda memerlukan penalaran di antara pemanggilan alat pada model ini.

Claude Haiku 4.5 tidak mendukung pemikiran berselang-seling. Di Claude API, header beta diterima tetapi diabaikan.

Ada dua pertimbangan lain untuk pemikiran berselang-seling dalam mode manual:

* `budget_tokens` boleh melebihi `max_tokens` di sini. [Aturan anggaran](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning) menjelaskan pengecualian ini.
* Pemikiran berselang-seling hanya didukung untuk [alat yang digunakan melalui Messages API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

Setiap platform memperlakukan header beta secara berbeda. Claude API dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) menerima `interleaved-thinking-2025-05-14` pada model apa pun dan mengabaikannya jika tidak didukung. Namun, header yang diterima belum tentu berpengaruh. Pada model yang menolak `type: "enabled"` (4.7 dan yang lebih baru) atau yang tidak mendukung pemikiran berselang-seling dalam mode manual (Claude Opus 4.6), header tersebut tidak berpengaruh pada mode manual. Pada model-model tersebut, pemikiran adaptif berselang-seling secara otomatis.

Platform yang dioperasikan mitra ([Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)) juga menerima header tersebut pada model apa pun tanpa mengembalikan error, dan mengabaikannya pada model yang tidak mendukung pemikiran berselang-seling.

## Struktur giliran dalam mode manual

Aturan umum struktur giliran, termasuk loop penggunaan alat dalam satu giliran, penanganan konflik di tengah giliran, dan pengaktifan atau penonaktifan pemikiran di antara giliran, dijelaskan di [Pemikiran dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use).

Mode manual menambahkan satu persyaratan: giliran asisten terakhir dari permintaan dengan pemikiran aktif harus diawali dengan blok pemikiran. [Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) tidak memiliki persyaratan ini. Mengubah konfigurasi pemikiran di antara giliran juga membatalkan caching prompt. Lihat bagian berikut.

## Caching prompt dalam mode manual

Mode manual menambahkan satu aturan di atas perilaku caching yang berlaku untuk semua mode, seperti dijelaskan di [pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching). Mengubah `budget_tokens` di antara permintaan membatalkan breakpoint cache, sama seperti beralih mode pemikiran, karena nilai anggaran dirender ke dalam prompt. Breakpoint tingkat pesan selalu meleset setelah anggaran berubah. Apakah breakpoint alat dan prompt sistem juga meleset bergantung pada tempat model merender konfigurasi tersebut.

Dalam praktiknya, pilih satu anggaran dan pertahankan selama percakapan yang di-cache berlangsung. Contoh berikut menunjukkan pembatalan cache secara langsung: percakapan multi-giliran dengan caching tingkat pesan dijalankan pada Claude Sonnet 4.6, lalu anggaran pada permintaan ketiga diubah dari 4.000 menjadi 8.000 token:

```text Output wrap
First request - establishing cache
First response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 17, output_tokens: 700 }

Second request - same thinking parameters (cache hit expected)
Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 1370, input_tokens: 303, output_tokens: 874 }

Third request - different thinking budget (cache miss expected)
Third response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 747, output_tokens: 619 }
```

Permintaan ketiga membuat ulang cache (`cache_creation_input_tokens=1370`, `cache_read_input_tokens=0`) karena anggaran berubah di antara permintaan. Untuk versi yang dapat dijalankan dari eksperimen yang sama dalam mode adaptif, di mana tingkat effort memainkan peran cache yang dimainkan `budget_tokens` di sini, lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#prompt-caching) di halaman pengarahan.

## Mekanisme bersama

Sebagian besar perilaku pemikiran berlaku untuk semua mode dan didokumentasikan satu kali di halaman [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking). Semua yang ada di sana juga berlaku dalam mode manual:

* [Mengontrol tampilan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display)
* [Streaming pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#streaming-thinking)
* [Pemikiran dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use), termasuk [mempertahankan blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)
* [Pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching)
* [Pemikiran dan "context window" (jendela konteks)](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-the-context-window)
* [Enkripsi pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-encryption)
* [Harga](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#pricing) (di halaman [Mengarahkan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost))

## Bermigrasi ke pemikiran adaptif

Jika model Anda hanya mendukung pemikiran diperpanjang (Claude Sonnet 4.5, Claude Opus 4.5, Claude Haiku 4.5, dan model Claude 4 yang lebih lama), Anda tidak perlu melakukan apa pun sekarang. Pemikiran adaptif tidak tersedia pada model tersebut, dan `type: "adaptive"` [mengembalikan error 400](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-adaptive). Tetap gunakan `budget_tokens` sampai Anda beralih ke model yang mendukung pemikiran adaptif, lalu terapkan pemetaan berikut.

Anda perlu bermigrasi dari `type: "enabled"` jika:

* Anda menggunakan Claude Opus 4.6 atau Claude Sonnet 4.6, yang `budget_tokens`-nya sudah deprecated.
* Anda menggunakan Claude 4.7 atau model yang lebih baru, seperti Claude Opus 5.5, Claude Sonnet 5, Claude Sonnet 5.5, atau Claude Fable 5.1, yang mengembalikan error 400 untuk `type: "enabled"`.

Pemetaannya sederhana: hapus `budget_tokens`, tetapkan `thinking: {type: "adaptive"}`, lalu kendalikan kedalaman penalaran dengan `output_config: {effort: ...}` sebagai pengganti anggaran token.

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```

menjadi:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 16000,
  "thinking": {
    "type": "adaptive"
  },
  "output_config": {
    "effort": "high"
  }
}
```

`effort: "high"` sama dengan nilai default API. Nilai ini dicantumkan di sini hanya untuk menunjukkan letak kontrol kedalaman yang baru, dan menghilangkannya menghasilkan perilaku yang identik.

Perubahan ini bukan sekadar perubahan sintaks, karena perilakunya juga berbeda. Dengan anggaran tetap, Claude berpikir pada setiap permintaan. Dengan pemikiran adaptif, Claude memutuskan apakah perlu berpikir dan seberapa banyak pada setiap permintaan. Pada pengaturan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah, Claude mungkin sama sekali tidak berpikir untuk input yang mudah.

Setelah bermigrasi, Anda juga dapat menghapus header beta `interleaved-thinking-2025-05-14`. Pemikiran adaptif berselang-seling secara otomatis, dan Claude API mengabaikan header tersebut pada model-model ini.

Penyimpanan blok pemikiran juga berubah. Claude Opus 4.5 dan model bernomor 4.6 ke atas menyimpan blok pemikiran dari giliran sebelumnya dalam konteks dan menagihnya sebagai input. Sebaliknya, Claude Sonnet 4.5, Claude Haiku 4.5, dan model yang lebih lama menghapusnya. Lihat [penyimpanan blok pemikiran per model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model).

Beralih mode termasuk perubahan konfigurasi pemikiran, sehingga permintaan pertama setelah peralihan membatalkan breakpoint cache, seperti dijelaskan di [Caching prompt dalam mode manual](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching).

Untuk panduan lengkap, lihat [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking), [effort](https://platform.claude.com/docs/id/build-with-claude/effort), dan [panduan migrasi model](https://platform.claude.com/docs/id/about-claude/models/migration-guide).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Pemikiran" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Pelajari cara kerja pemikiran: blok, tampilan, streaming, dan penggunaan alat.
  </Card>

  <Card title="Mengarahkan pemikiran" icon="compass" href="https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost">
    Biarkan Claude memutuskan kapan dan seberapa banyak berpikir pada setiap permintaan.
  </Card>

  <Card title="Pemikiran dalam alur kerja alat dan multi-giliran" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows">
    Pertahankan blok pemikiran dan kelola pemikiran di seluruh pemanggilan alat dan giliran.
  </Card>
</CardGroup>
