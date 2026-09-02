---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 6fa45c5f1d3e3f20086b4b4fa5d0b5959587371852a85b7e0c5b01b8ff457b7e
---

---
title: Effort
url: https://platform.claude.com/docs/id/build-with-claude/effort
description: Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): eligible (excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))
- Supported models: `claude-fable-5-1`, `claude-mythos-5-1`, `claude-fable-5`, `claude-mythos-5`, `claude-mythos-preview`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5-20251101`, `claude-sonnet-5`, `claude-sonnet-4-6`
- Platforms: Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud, Microsoft Foundry

Parameter effort (upaya) memungkinkan Anda mengendalikan berapa banyak token yang dihabiskan Claude saat merespons permintaan. Anda dapat menyeimbangkan antara ketelitian respons dan efisiensi token dengan satu model. Parameter effort tingkat atas tersedia di semua model yang didukung tanpa memerlukan header beta. [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) masih dalam versi beta.

<Tip>
  Untuk mempelajari bagaimana effort berinteraksi dengan thinking (pemikiran) dan kontrol mana yang sebaiknya digunakan, lihat [Thinking dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-effort). Jika adaptive thinking (pemikiran adaptif) tersedia, effort adalah cara yang direkomendasikan untuk mengendalikan kedalaman pemikiran.
</Tip>

## Mengatur tingkat effort

Atur `output_config.effort` pada permintaan. Contoh berikut menjalankan satu permintaan dengan effort `medium` dan mencetak teks respons.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "messages": [{
        "role": "user",
        "content": "Analyze the trade-offs between microservices and monolithic architectures"
      }],
      "output_config": {
        "effort": "medium"
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 4096 \
    --output-config '{effort: medium}' \
    --message '{role: user, content: "Analyze the trade-offs between microservices and monolithic architectures"}' \
    --transform 'content.#(type=="text").text' \
    --raw-output
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Analyze the trade-offs between microservices and monolithic architectures",
          }
      ],
      output_config={"effort": "medium"},
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Analyze the trade-offs between microservices and monolithic architectures"
      }
    ],
    output_config: {
      effort: "medium"
    }
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 4096,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Analyze the trade-offs between microservices and monolithic architectures"
          }
      ],
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Medium
      }
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the trade-offs between microservices and monolithic architectures")),
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMedium,
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
  import com.anthropic.models.messages.OutputConfig;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
          .outputConfig(OutputConfig.builder()
              .effort(OutputConfig.Effort.MEDIUM)
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
      ],
      model: 'claude-opus-5',
      outputConfig: ['effort' => 'medium'],
  );

  foreach ($message->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
    ],
    output_config: {
      effort: "medium"
    }
  )

  message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Cara kerja effort

Secara default, Claude menggunakan effort high, menghabiskan token sebanyak yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi secara mutlak, atau menurunkannya agar lebih hemat dalam penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima sedikit penurunan kemampuan.

<Tip>
  Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan tidak menyertakan parameter `effort` sama sekali.
</Tip>

Parameter effort memengaruhi **semua token** dalam respons, termasuk:

* Respons teks dan penjelasan
* Pemanggilan alat dan argumen fungsi
* Thinking (saat aktif)

Karena effort berlaku untuk setiap token output, parameter ini berfungsi baik thinking diaktifkan maupun tidak. Effort yang lebih rendah juga berarti pemanggilan alat yang lebih sedikit dan lebih ringkas.

### Tingkat effort

| Tingkat  | Deskripsi                                                                                                                                                                                                                                                                     | Kasus penggunaan umum                                                                                |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum mutlak tanpa batasan pengeluaran token. Tersedia di Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. | Tugas yang memerlukan penalaran sedalam mungkin dan analisis paling menyeluruh                       |
| `xhigh`  | Kemampuan diperluas untuk pekerjaan berjangka panjang. Tersedia di Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5.                                                                | Tugas agentic dan coding yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter.                                                                                                                                                                                                                     | Penalaran kompleks, masalah coding yang sulit, tugas agentic                                         |
| `medium` | Pendekatan seimbang dengan penghematan token moderat.                                                                                                                                                                                                                         | Tugas agentic yang memerlukan keseimbangan antara kecepatan, biaya, dan performa                     |
| `low`    | Paling efisien. Penghematan token signifikan dengan sedikit penurunan kemampuan.                                                                                                                                                                                              | Tugas lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagen         |

Tidak semua model yang mendukung `max` juga mendukung `xhigh`.

<Note>
  Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude tetap berpikir untuk masalah yang cukup sulit, tetapi berpikir lebih sedikit dibandingkan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

Rekomendasi per model berikut ini menggantikan tabel ini jika terdapat perbedaan.

### Tingkat effort yang direkomendasikan untuk Claude Fable 5.1

Claude Fable 5.1 mendukung kelima tingkat effort. **Mulailah dengan `high`, nilai default.** Naikkan ke `xhigh` atau `max` untuk pekerjaan agentic dan coding yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin atau yang sensitif terhadap latensi setelah evaluasi Anda menunjukkan kualitas tetap terjaga. Pada `high` dan di atasnya, atur `max_tokens` yang besar. Ini adalah batas keras untuk total output (thinking ditambah teks respons). Rekomendasi yang sama berlaku untuk Claude Mythos 5.1. Lihat [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels).

Claude Fable 5.1 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt.

### Tingkat effort yang direkomendasikan untuk Claude Fable 5

Effort adalah kontrol utama untuk menyeimbangkan kecerdasan, latensi, dan biaya pada Claude Fable 5. **Mulailah dengan `high`, nilai default, untuk sebagian besar tugas**, gunakan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 tetap berkinerja baik dan sering kali melampaui performa `xhigh` pada model sebelumnya. Pada `high` dan `xhigh`, atur `max_tokens` yang besar. Ini adalah batas keras untuk total output (thinking ditambah teks respons). Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

Kurangi effort jika suatu tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan interaktif. Rekomendasi yang sama berlaku untuk Claude Mythos 5. Untuk panduan lebih lengkap, lihat [Prompting Claude Fable 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

### Tingkat effort yang direkomendasikan untuk Claude Opus 5

Claude Opus 5 mendukung kelima tingkat effort. **Mulailah dengan `high`, nilai default**, dan sesuaikan berdasarkan evaluasi Anda: naikkan ke `xhigh` untuk pekerjaan coding dan agentic yang berat, atau ke `max` ketika suatu tugas membenarkan pengeluaran token tanpa batasan, dan gunakan `low` serta `medium` secara leluasa sebagai kontrol utama Anda untuk biaya token dan waktu respons di mana pun evaluasi Anda menunjukkan kualitas tetap terjaga. Jika Anda membawa pengaturan effort dari model sebelumnya, jalankan sweep effort baru pada evaluasi Anda daripada menggunakannya kembali.

Effort mengendalikan volume thinking, bukan panjang respons yang terlihat: pada Claude Opus 5, mengubah effort tidak secara andal memperpendek respons, jadi [gunakan prompt untuk mengatur panjang](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) sebagai gantinya.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda. Nilai yang Anda berikan menggantikan default.

Pada Claude Opus 5, thinking tidak dapat dinonaktifkan pada effort `xhigh` atau `max`: permintaan yang mengatur `thinking: {"type": "disabled"}` pada tingkat tersebut mengembalikan error 400. Lihat [Effort dengan thinking](https://platform.claude.com/docs/id/build-with-claude/effort#effort-with-thinking).

Saat menjalankan Claude Opus 5 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikannya dari sana adalah default yang wajar.

Claude Opus 5 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.8

Panduan untuk Claude Opus 4.7 juga berlaku untuk Claude Opus 4.8. **Mulailah dengan `xhigh` untuk kasus penggunaan coding dan agentic**, gunakan `high` untuk sebagian besar beban kerja lain yang sensitif terhadap kecerdasan, dan turunkan ke `medium` atau `low` hanya ketika Anda telah mengukur bahwa tingkat yang lebih rendah tetap menjaga kualitas pada evaluasi Anda.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda. Nilai yang Anda berikan menggantikan default.

Saat menjalankan Claude Opus 4.8 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikannya dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.7

**Mulailah dengan `xhigh` untuk kasus penggunaan coding dan agentic**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap kecerdasan. Turunkan ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naikkan ke `max` hanya ketika evaluasi Anda menunjukkan ruang peningkatan yang terukur pada `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit. Nilai yang Anda berikan menggantikan default.

| Effort   | Panduan untuk Claude Opus 4.7                                                                                                                                                                                                                                                |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `low`    | Efisien, tetapi paling cocok untuk tugas singkat dengan cakupan terbatas. Padukan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian.                                                                                                            |
| `medium` | Pengganti langsung untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya.                                                                                                                                                             |
| `high`   | Kasus penggunaan lanjutan yang masih memerlukan keseimbangan antara kecerdasan dan konsumsi token. Ini sering kali merupakan keseimbangan terbaik antara kualitas dan efisiensi token.                                                                                       |
| `xhigh`  | Titik awal yang direkomendasikan untuk pekerjaan coding dan agentic, serta untuk tugas eksploratif seperti pemanggilan alat berulang, pencarian web mendetail, dan pencarian basis pengetahuan. Perkirakan penggunaan token yang jauh lebih tinggi daripada `high`.          |
| `max`    | Simpan untuk masalah frontier. Pada sebagian besar beban kerja, `max` menambah biaya signifikan untuk peningkatan kualitas yang relatif kecil, dan pada beberapa tugas output terstruktur atau yang kurang sensitif terhadap kecerdasan, ini dapat menyebabkan overthinking. |

Claude Opus 4.7 juga mematuhi tingkat effort dengan lebih ketat daripada Claude Opus 4.6, terutama pada `low` dan `medium`. Pada tingkat effort yang lebih rendah, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort daripada mengatasinya dengan prompt. Jika Anda harus menjaga effort tetap rendah demi latensi, tambahkan panduan terarah seperti "This task involves multistep reasoning. Think carefully before responding."

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikannya dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Sonnet 5

Claude Sonnet 5 menggunakan effort `high` secara default pada Claude API dan Claude Code.

* **Effort high (default):** Cocok untuk penalaran kompleks, coding, dan tugas agentic di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort xhigh:** Untuk tugas coding dan agentic yang paling sulit. Lihat [Prompting Claude Sonnet 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5#calibrating-effort-and-thinking-depth).
* **Effort medium:** Penurunan yang menghemat biaya dari default. Sebanding dengan Claude Sonnet 4.6 pada effort high.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana waktu penyelesaian yang lebih cepat diprioritaskan.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi secara mutlak tanpa batasan pengeluaran token.

### Tingkat effort yang direkomendasikan untuk Claude Sonnet 4.6

Sonnet 4.6 menggunakan effort `high` secara default. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

* **Effort medium** (default yang direkomendasikan): Keseimbangan terbaik antara kecepatan, biaya, dan performa untuk sebagian besar aplikasi. Cocok untuk agentic coding, alur kerja yang banyak menggunakan alat, dan pembuatan kode.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana waktu penyelesaian yang lebih cepat diprioritaskan.
* **Effort high:** Untuk penalaran kompleks dan tugas di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi secara mutlak tanpa batasan pengeluaran token.

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort memengaruhi baik penjelasan di sekitar pemanggilan alat maupun pemanggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

* Menggabungkan beberapa operasi menjadi lebih sedikit pemanggilan alat
* Melakukan lebih sedikit pemanggilan alat
* Langsung bertindak tanpa pendahuluan
* Menggunakan pesan konfirmasi ringkas setelah selesai

Tingkat effort yang lebih tinggi mungkin:

* Melakukan lebih banyak pemanggilan alat
* Menjelaskan rencana sebelum bertindak
* Memberikan ringkasan perubahan yang mendetail
* Menyertakan komentar kode yang lebih komprehensif

## Effort dengan thinking

Parameter `thinking` mengontrol apakah Claude berpikir dalam [blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) sebelum menjawab; parameter `effort` mengontrol seberapa banyak upaya yang Claude curahkan untuk keseluruhan respons, yang dalam mode adaptif mencakup seberapa sering dan seberapa dalam Claude berpikir. Jangan berikan `adaptive` sebagai nilai `effort`: `adaptive` adalah mode berpikir, bukan tingkat upaya.

Pada tingkat effort yang lebih tinggi, Claude berpikir pada sebagian besar permintaan dan dengan lebih panjang. Pada tingkat yang lebih rendah, Claude dapat melewatkan thinking sepenuhnya untuk masalah yang lebih sederhana. Lihat [Thinking dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-effort) untuk panduan lengkap tentang bagaimana kedua kontrol ini bekerja bersama.

Pada Claude Opus 4.5, satu-satunya model khusus pemikiran diperpanjang yang mendukung effort, parameter ini bekerja berdampingan dengan [`budget_tokens`](https://platform.claude.com/docs/id/build-with-claude/extended-thinking): atur tingkat effort untuk tugas Anda, lalu atur anggaran token thinking berdasarkan seberapa dalam penalaran yang dibutuhkan tugas tersebut.

Untuk ketersediaan thinking per model, lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models). Effort berfungsi dengan atau tanpa thinking. Lihat [Cara kerja effort](https://platform.claude.com/docs/id/build-with-claude/effort#how-effort-works).

## Mengubah effort di tengah percakapan

Anda dapat menjalankan giliran percakapan selanjutnya pada tingkat effort yang berbeda dengan dua cara. Pada Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5, gunakan perubahan effort per pesan, yang mempertahankan cache prompt. Pada model lain, atur nilai tingkat atas baru pada permintaan berikutnya, yang memulai cache dari awal.

### Effort per pesan (beta)

Effort per pesan masih dalam versi beta dan memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-output-config-2026-07-01`. Model tanpa effort per pesan, termasuk Claude Fable 5, mengembalikan error 400: `output_config.effort requires a model that supports per-turn effort; this model does not`.

Tambahkan pesan `role: "system"` dengan `content` kosong dan tingkat baru di `output_config.effort`. Tingkat baru berlaku mulai giliran `user` berikutnya dan bertahan hingga pesan selanjutnya mengubahnya. Semua yang ada sebelum pesan tersebut tidak berubah, sehingga prefiks yang di-cache tetap cocok.

Contoh berikut dimulai pada `high`, lalu turun ke `low` untuk tindak lanjut rutin:

<CodeGroup>
  ```bash cURL
  # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mid-conversation-output-config-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5-1",
      "max_tokens": 4096,
      "output_config": {"effort": "high"},
      "messages": [
        {"role": "user", "content": "Plan a migration from SQLite to PostgreSQL in three short steps."},
        {"role": "assistant", "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."},
        {"role": "system", "content": [], "output_config": {"effort": "low"}},
        {"role": "user", "content": "Summarize the plan in one sentence."}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta mid-conversation-output-config-2026-07-01 \
    --transform 'content.#(type=="text").text' --raw-output <<'YAML'
  model: claude-fable-5-1
  max_tokens: 4096
  output_config:
    effort: high
  messages:
    - role: user
      content: Plan a migration from SQLite to PostgreSQL in three short steps.
    - role: assistant
      content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
    # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
    - role: system
      content: []
      output_config:
        effort: low
    - role: user
      content: Summarize the plan in one sentence.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5-1",
      max_tokens=4096,
      output_config={"effort": "high"},
      messages=[
          {
              "role": "user",
              "content": "Plan a migration from SQLite to PostgreSQL in three short steps.",
          },
          {
              "role": "assistant",
              "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.",
          },
          # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          {"role": "system", "content": [], "output_config": {"effort": "low"}},
          {"role": "user", "content": "Summarize the plan in one sentence."},
      ],
      betas=["mid-conversation-output-config-2026-07-01"],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5-1",
    max_tokens: 4096,
    output_config: { effort: "high" },
    messages: [
      {
        role: "user",
        content: "Plan a migration from SQLite to PostgreSQL in three short steps."
      },
      {
        role: "assistant",
        content:
          "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
      },
      // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
      { role: "system", content: [], output_config: { effort: "low" } },
      { role: "user", content: "Summarize the plan in one sentence." }
    ],
    betas: ["mid-conversation-output-config-2026-07-01"]
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = "claude-fable-5-1",
      MaxTokens = 4096,
      OutputConfig = new() { Effort = Effort.High },
      Messages =
      [
          new() { Role = Role.User, Content = "Plan a migration from SQLite to PostgreSQL in three short steps." },
          new() { Role = Role.Assistant, Content = "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          new()
          {
              Role = Role.System,
              Content = new([]),
              OutputConfig = new() { Effort = BetaSystemMessageOutputConfigEffort.Low },
          },
          new() { Role = Role.User, Content = "Summarize the plan in one sentence." },
      ],
      Betas = [AnthropicBeta.MidConversationOutputConfig2026_07_01],
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

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     "claude-fable-5-1",
  	MaxTokens: 4096,
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortHigh,
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Plan a migration from SQLite to PostgreSQL in three short steps.")),
  		{
  			Role:    anthropic.BetaMessageParamRoleAssistant,
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
  		},
  		// Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
  		anthropic.NewBetaSystemMessage(anthropic.BetaSystemMessageOutputConfigParam{
  			Effort: anthropic.BetaSystemMessageOutputConfigEffortLow,
  		}),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize the plan in one sentence.")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaMidConversationOutputConfig2026_07_01},
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
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaOutputConfig;
  import com.anthropic.models.beta.messages.BetaSystemMessageOutputConfig;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-fable-5-1")
          .maxTokens(4096L)
          .addBeta(AnthropicBeta.MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01)
          .outputConfig(BetaOutputConfig.builder()
              .effort(BetaOutputConfig.Effort.HIGH)
              .build())
          .addUserMessage("Plan a migration from SQLite to PostgreSQL in three short steps.")
          .addAssistantMessage("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          .addMessage(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.SYSTEM)
              .contentOfBetaContentBlockParams(List.of())
              .outputConfig(BetaSystemMessageOutputConfig.builder()
                  .effort(BetaSystemMessageOutputConfig.Effort.LOW)
                  .build())
              .build())
          .addUserMessage("Summarize the plan in one sentence.")
          .build();

      BetaMessage response = client.beta().messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Beta\Messages\BetaOutputConfig;
  use Anthropic\Beta\Messages\BetaSystemMessageOutputConfig;
  use Anthropic\Client;

  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5-1',
      maxTokens: 4096,
      outputConfig: BetaOutputConfig::with(effort: 'high'),
      messages: [
          BetaMessageParam::with(role: 'user', content: 'Plan a migration from SQLite to PostgreSQL in three short steps.'),
          BetaMessageParam::with(role: 'assistant', content: '1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.'),
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          BetaMessageParam::with(
              role: 'system',
              content: [],
              outputConfig: BetaSystemMessageOutputConfig::with(effort: 'low'),
          ),
          BetaMessageParam::with(role: 'user', content: 'Summarize the plan in one sentence.'),
      ],
      betas: [AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01],
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
    model: "claude-fable-5-1",
    max_tokens: 4096,
    output_config: {effort: :high},
    messages: [
      {role: "user", content: "Plan a migration from SQLite to PostgreSQL in three short steps."},
      {role: "assistant", content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."},
      # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
      {role: "system", content: [], output_config: {effort: :low}},
      {role: "user", content: "Summarize the plan in one sentence."}
    ],
    betas: [Anthropic::AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

Pesan sistem yang hanya berisi effort tidak membawa teks, sehingga [aturan penempatan untuk pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations) tidak berlaku. Pesan ini dapat muncul di mana saja dalam `messages`, termasuk sebagai entri pertama atau di antara giliran `assistant` dan giliran `user` berikutnya. Nilainya adalah nama tingkat (`low`, `medium`, `high`, `xhigh`, dan `max`).

Pada Claude Fable 5.1, utamakan bentuk ini daripada mengubah nilai tingkat atas di antara permintaan. Perubahan tingkat atas memulai ulang cache dan juga mengarahkan model dengan kurang andal: balasan sebelumnya ditulis pada tingkat sebelumnya, dan model cenderung tetap konsisten dengan balasan tersebut.

### Effort tingkat atas pada permintaan berikutnya

`output_config.effort` tingkat atas berlaku untuk seluruh permintaan. Untuk menjalankan bagian percakapan selanjutnya pada tingkat yang berbeda, atur nilai baru pada permintaan berikutnya. Karena effort tingkat atas membentuk prompt yang dirender, mengubahnya di antara permintaan tidak mempertahankan prefiks yang di-cache dari giliran sebelumnya. Jika Anda mengandalkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) sepanjang sesi yang panjang dan model Anda tidak mendukung effort per pesan, pilih tingkat effort di awal dan pertahankan agar tetap konstan.

## Praktik terbaik

1. **Atur effort secara eksplisit:** API menggunakan `high` secara default, tetapi titik awal yang tepat bergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugasnya sederhana, effort low dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak tingkat effort bervariasi menurut jenis tugas. Evaluasi performa pada kasus penggunaan spesifik Anda sebelum melakukan deployment.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin cukup dengan effort low sementara agentic coding dan penalaran kompleks mendapat manfaat dari effort high. Lihat butir berikutnya sebelum memvariasikannya dalam satu percakapan.
5. **Pertahankan effort tingkat atas konstan dalam percakapan yang di-cache:** Mengubah nilai effort tingkat atas di antara permintaan membatalkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), jadi variasikan di antara beban kerja alih-alih di dalam percakapan yang mengandalkan cache hit. Pada model yang mendukungnya, gunakan [perubahan effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) sebagai gantinya, yang mempertahankan cache. Lihat [Thinking dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

## Langkah selanjutnya

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token yang bersifat saran untuk seluruh loop agentic guna membantu model mengatur dirinya sendiri pada tugas agentic yang panjang.
  </Card>

  <Card title="Mengarahkan thinking" icon="compass" href="https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost">
    Pahami adaptive thinking, di mana Claude memutuskan kapan dan seberapa banyak berpikir, dan arahkan dengan effort serta prompting.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Pahami cara kerja thinking, kapan Claude berpikir secara default, dan bagaimana thinking berinteraksi dengan effort.
  </Card>
</CardGroup>
