---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: d80884de1b2c7fb68d4327fb57974044221e7bde373c70b0d1af38294649676d
---

---
title: Pemikiran diperpanjang
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
description: Konfigurasikan pemikiran diperpanjang manual dengan anggaran budget_tokens tetap pada model Claude yang mendukungnya, dan migrasikan ke pemikiran adaptif.
---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

<Warning>
  Extended thinking (pemikiran diperpanjang) (`thinking.type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated) pada model Claude 4.6 (permintaan yang menggunakannya masih berhasil). Model Claude 4.7 dan yang lebih baru tidak mendukungnya dan menolak permintaan yang menggunakannya, dengan mengembalikan error 400. Pada model Claude 4.5 dan yang lebih lama yang mendukung thinking, pemikiran diperpanjang adalah satu-satunya mode thinking yang tersedia. Claude Mythos Preview mendukung kedua mode. Jika kedua mode tersedia, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) sebagai gantinya.

  Lihat [Migrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) untuk beralih ke pemikiran adaptif. Jika model Anda hanya mendukung pemikiran diperpanjang, halaman ini menjelaskan konfigurasi yang didukung; tidak ada perubahan yang diperlukan sampai Anda beralih ke model yang lebih baru.
</Warning>

<Note>
  Jika permintaan gagal dengan error 400 yang pesannya dimulai dengan `"thinking.type.enabled" is not supported`, model Anda menggunakan pemikiran adaptif. Lihat [Pemecahan masalah pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-enabled), atau langsung ke [Migrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking).
</Note>

"Extended thinking" (pemikiran diperpanjang) dalam mode manual memberi Anda kontrol langsung atas seberapa banyak Claude berpikir. Anda menetapkan anggaran token pemikiran pada setiap permintaan dengan `thinking: {type: "enabled", budget_tokens: N}`, dan Claude berpikir sesuai anggaran tersebut sebelum mulai menghasilkan jawaban akhirnya. Mode manual tetap berguna ketika beban kerja Anda memerlukan "latency" (latensi) yang dapat diprediksi atau kontrol yang presisi atas biaya pemikiran. Halaman ini membahas cara menetapkan dan menyetel anggaran, bagaimana mode manual berinteraksi dengan pemikiran berselang dan caching prompt, serta cara bermigrasi ke pemikiran adaptif.

Untuk cara kerja pemikiran itu sendiri, termasuk blok pemikiran dan bentuk respons, parameter `display`, streaming, pemikiran dengan penggunaan alat, dan enkripsi, lihat [ikhtisar pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking).

## Model yang didukung

Ketersediaan pemikiran diperpanjang per model, termasuk model di mana pemikiran diperpanjang adalah satu-satunya mode, tercantum dalam [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models).

## Cara menggunakan pemikiran diperpanjang

Berikut adalah contoh penggunaan pemikiran diperpanjang dalam Messages API:

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
    --transform content --format yaml <<'YAML'
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
    if (block.type === "thinking") {
      console.log(`\nThinking summary: ${block.thinking}`);
    } else if (block.type === "text") {
      console.log(`\nResponse: ${block.text}`);
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
      echo match ($block->type) {
          'thinking' => "\nThinking summary: {$block->thinking}",
          'text' => "\nResponse: {$block->text}",
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
    in {type: :thinking, thinking:}
      puts "\nThinking summary: #{thinking}"
    in {type: :text, text:}
      puts "\nResponse: #{text}"
    else
    end
  end
  ```
</CodeGroup>

Untuk mengaktifkan pemikiran diperpanjang manual, tambahkan objek `thinking` dengan `type` diatur ke `enabled` dan nilai `budget_tokens`.

Parameter `budget_tokens` menetapkan target untuk berapa banyak token yang dapat digunakan Claude untuk proses penalaran internalnya. Anggaran yang lebih besar dapat meningkatkan kualitas respons dengan memungkinkan analisis yang lebih menyeluruh untuk masalah yang kompleks.

## Aturan dan penyetelan anggaran

`budget_tokens` harus memenuhi batasan berikut:

* **Minimum 1.024 token.** API menolak nilai yang lebih kecil.
* **Kurang dari `max_tokens`.** Token pemikiran dihitung terhadap batas `max_tokens` untuk giliran tersebut, sehingga anggaran harus menyisakan ruang untuk respons akhir. Satu-satunya pengecualian adalah [pemikiran berselang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#interleaved-thinking), di mana `budget_tokens` dapat melebihi `max_tokens` karena anggaran mencakup semua blok pemikiran dalam satu giliran asisten.
* **Tanpa pre-warming cache.** Karena `budget_tokens` harus kurang dari `max_tokens`, pemikiran diperpanjang tidak dapat dikombinasikan dengan `max_tokens: 0` ([pre-warming cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache)).

Anggaran adalah target, bukan batas ketat. Penggunaan token aktual bervariasi sesuai tugas, dan Claude mungkin berhenti bernalar jauh sebelum anggaran habis; `max_tokens` tetap menjadi batas keras pada total output.

Pada Claude Opus 4.5, satu-satunya model khusus pemikiran diperpanjang yang mendukung [effort](https://platform.claude.com/docs/id/build-with-claude/effort), effort membentuk respons keseluruhan sementara `budget_tokens` menetapkan kedalaman pemikiran; atur keduanya.

Untuk menyetel anggaran:

* Sesuaikan titik awal dengan tugas. Untuk tugas sederhana, mulai di dekat minimum 1.024 token dan tingkatkan secara bertahap untuk menemukan rentang optimal untuk kasus penggunaan Anda. Untuk tugas kompleks, mulai dengan anggaran yang lebih besar yaitu 16.000 token atau lebih dan sesuaikan dengan kebutuhan latensi dan kualitas Anda. Anggaran yang lebih tinggi memungkinkan penalaran yang lebih komprehensif, dengan hasil yang semakin berkurang tergantung pada tugas, dan dengan biaya peningkatan latensi. Untuk tugas kritis, uji pengaturan yang berbeda untuk menemukan keseimbangan yang tepat.
* Untuk anggaran pemikiran di atas 32k, gunakan [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Mendorong model untuk berpikir melebihi 32k token menghasilkan permintaan yang berjalan lama yang dapat mencapai batas waktu sistem dan batas koneksi terbuka.

Untuk melacak berapa biaya aktual dari suatu anggaran, pantau field `usage.output_tokens_details.thinking_tokens` dalam respons, yang melaporkan berapa banyak dari token output yang ditagih merupakan penalaran internal. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir.

Ketika Anda siap untuk beralih dari anggaran manual, lihat [Migrasi ke pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking).

## Pemikiran berselang dalam mode manual

"Interleaved thinking" (pemikiran berselang) memungkinkan Claude berpikir di antara panggilan alat dalam satu giliran asisten, bernalar tentang setiap hasil alat sebelum memutuskan apa yang harus dilakukan selanjutnya. Untuk konsep, struktur giliran, dan bagaimana perilakunya pada model pemikiran adaptif, lihat [pemikiran berselang](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) dalam ikhtisar pemikiran. Bagian ini membahas cara mengaktifkannya ketika Anda menggunakan pemikiran manual `type: "enabled"`.

Pada Claude Opus 4.5, Claude Sonnet 4.5, dan model Claude 4 sebelumnya (Claude Opus 4.1, Claude Opus 4, dan Claude Sonnet 4), tambahkan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda.

Generasi 4.6 terbagi dalam mode manual:

* **Claude Sonnet 4.6**: header beta dengan `type: "enabled"` manual masih berfungsi tetapi sudah usang (deprecated). Lebih baik gunakan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking), yang menyelang secara otomatis tanpa header.
* **Claude Opus 4.6**: mode manual tidak memiliki pemikiran berselang sama sekali. Hanya mode adaptifnya yang menyelang, jadi beralihlah ke `thinking: {type: "adaptive"}` jika Anda memerlukan penalaran di antara panggilan alat pada model ini.

Claude Haiku 4.5 tidak mendukung pemikiran berselang. Pada Claude API, header beta diterima tetapi diabaikan.

Dua pertimbangan lain untuk pemikiran berselang dalam mode manual:

* `budget_tokens` dapat melebihi `max_tokens` di sini; [aturan anggaran](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning) menjelaskan pengecualian ini.
* Pemikiran berselang hanya didukung untuk [alat yang digunakan melalui Messages API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

Cara platform memperlakukan header beta berbeda-beda. Claude API dan [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) menerima `interleaved-thinking-2025-05-14` pada model apa pun dan mengabaikannya jika tidak didukung. Penerimaan tidak sama dengan efek: pada model yang menolak `type: "enabled"` (4.7 dan yang lebih baru) atau tidak memiliki penyelangan mode manual (Claude Opus 4.6), header tidak memiliki efek mode manual; pemikiran adaptif menyelang secara otomatis di sana.

Platform yang dioperasikan mitra ([Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)) juga menerima header pada model apa pun tanpa mengembalikan error, dan mengabaikannya pada model yang tidak mendukung pemikiran berselang.

## Struktur giliran dalam mode manual

Aturan umum struktur giliran, termasuk loop penggunaan alat satu giliran, penanganan konflik di tengah giliran, dan pengalihan pemikiran antar giliran, ada di [Pemikiran dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use).

Mode manual menambahkan satu persyaratan: giliran asisten terakhir dari permintaan dengan pemikiran aktif harus dimulai dengan blok pemikiran ([pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) menghilangkan persyaratan tersebut). Mengubah konfigurasi pemikiran antar giliran juga membatalkan caching prompt; lihat bagian berikut.

## Caching prompt dalam mode manual

Mode manual menambahkan satu aturan di atas perilaku caching yang netral mode yang dijelaskan dalam [pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching): mengubah `budget_tokens` antar permintaan membatalkan breakpoint cache, sama seperti beralih mode pemikiran, karena nilai anggaran dirender ke dalam prompt. Breakpoint tingkat pesan selalu gagal setelah perubahan anggaran; apakah breakpoint alat dan prompt sistem juga gagal tergantung pada di mana model merender konfigurasi.

Dalam praktiknya, pilih anggaran dan pertahankan stabil selama masa percakapan yang di-cache. Menjalankan percakapan multi-giliran dengan caching tingkat pesan pada Claude Sonnet 4.6 dan mengubah anggaran pada permintaan ketiga dari 4.000 menjadi 8.000 token menunjukkan pembatalan secara langsung:

```text Output wrap
First request - establishing cache
First response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 17, output_tokens: 700 }

Second request - same thinking parameters (cache hit expected)
Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 1370, input_tokens: 303, output_tokens: 874 }

Third request - different thinking budget (cache miss expected)
Third response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 747, output_tokens: 619 }
```

Permintaan ketiga membuat ulang cache (`cache_creation_input_tokens=1370`, `cache_read_input_tokens=0`) karena anggaran berubah antar permintaan. Untuk versi yang dapat dijalankan dari eksperimen yang sama dalam mode adaptif, di mana tingkat effort memainkan peran cache yang dimainkan `budget_tokens` di sini, lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#prompt-caching) di halaman pengarahan.

## Mekanisme bersama

Sebagian besar perilaku pemikiran bersifat netral mode dan didokumentasikan sekali di halaman [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking). Semua yang ada di sana juga berlaku dalam mode manual:

* [Mengontrol tampilan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display)
* [Streaming pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#streaming-thinking)
* [Pemikiran dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use), termasuk [mempertahankan blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)
* [Pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching)
* [Pemikiran dan jendela konteks](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-the-context-window)
* [Enkripsi pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-encryption)
* [Harga](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#pricing) (di halaman [Mengarahkan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost))

## Migrasi ke pemikiran adaptif

Jika model Anda hanya mendukung pemikiran diperpanjang (Claude Sonnet 4.5, Claude Opus 4.5, Claude Haiku 4.5, dan model Claude 4 sebelumnya), tidak ada tindakan yang diperlukan sekarang: pemikiran adaptif tidak tersedia di sana, dan `type: "adaptive"` [mengembalikan error 400](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-type-adaptive). Pertahankan `budget_tokens` sampai Anda beralih ke model yang mendukung pemikiran adaptif, lalu terapkan pemetaan berikut.

Anda perlu bermigrasi dari `type: "enabled"` jika:

* Anda menggunakan Claude Opus 4.6 atau Claude Sonnet 4.6, di mana `budget_tokens` sudah usang (deprecated).
* Anda beralih ke Claude Opus 4.7, Claude Opus 4.8, Claude Opus 5, Claude Sonnet 5, Claude Fable 5, atau Claude Mythos 5, di mana `type: "enabled"` mengembalikan error 400.

Pemetaannya sederhana: hapus `budget_tokens`, atur `thinking: {type: "adaptive"}`, dan kontrol kedalaman penalaran dengan `output_config: {effort: ...}` alih-alih anggaran token.

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

`effort: "high"` sesuai dengan default API; ini muncul di sini hanya untuk menunjukkan di mana kontrol kedalaman sekarang berada, dan menghilangkannya menghasilkan perilaku yang identik.

Harapkan perbedaan perilaku, bukan hanya perubahan sintaks. Dengan anggaran tetap, Claude berpikir pada setiap permintaan. Dengan pemikiran adaptif, Claude memutuskan apakah dan seberapa banyak berpikir pada setiap permintaan, dan pada pengaturan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah, Claude mungkin melewatkan pemikiran sepenuhnya pada input yang mudah. Anda juga dapat menghapus header beta `interleaved-thinking-2025-05-14` setelah bermigrasi: pemikiran adaptif menyelang secara otomatis, dan Claude API mengabaikan header pada model-model ini. Pelestarian blok pemikiran juga berubah: Claude Opus 4.5 dan model bernomor 4.6 dan lebih tinggi mempertahankan blok pemikiran giliran sebelumnya dalam konteks dan menagihnya sebagai input, sedangkan Claude Sonnet 4.5, Claude Haiku 4.5, dan model sebelumnya menghapusnya; lihat [pelestarian blok pemikiran berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model).

Beralih mode adalah perubahan konfigurasi pemikiran, sehingga permintaan pertama setelah peralihan membatalkan breakpoint cache, seperti yang dijelaskan dalam [Caching prompt dalam mode manual](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching).

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
    Pertahankan blok pemikiran dan kelola pemikiran di seluruh panggilan alat dan giliran.
  </Card>
</CardGroup>
