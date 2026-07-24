---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: ba3cf4769be1211cb1a0119715785638383b92d896e8ca25d0c1cf67b36d8d56
---

# Effort

Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Parameter effort memungkinkan Anda mengontrol berapa banyak token yang digunakan Claude saat merespons permintaan. Anda dapat menyeimbangkan antara ketelitian respons dan efisiensi token dengan satu model. Parameter effort tersedia di semua model yang didukung tanpa memerlukan header beta.

<Note>
  Parameter effort didukung oleh Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, dan Claude Opus 4.5.
</Note>

<Tip>
  Untuk Claude Opus 4.6 dan Sonnet 4.6, effort menggantikan `budget_tokens` sebagai cara yang direkomendasikan untuk mengontrol kedalaman pemikiran. Kombinasikan effort dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) untuk pengalaman terbaik. Meskipun `budget_tokens` masih diterima pada Opus 4.6 dan Sonnet 4.6, parameter ini sudah usang (deprecated) dan akan dihapus pada rilis model mendatang. Pada effort `high` (default) dan `max`, Claude hampir selalu berpikir. Pada tingkat effort yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana.
</Tip>

## Cara kerja effort

Secara default, Claude menggunakan effort tinggi, menghabiskan token sebanyak yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi mutlak, atau menurunkannya agar lebih hemat dalam penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima sedikit penurunan kemampuan.

<Tip>
  Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan tidak menyertakan parameter `effort` sama sekali.
</Tip>

Parameter effort memengaruhi **semua token** dalam respons, termasuk:

* Respons teks dan penjelasan
* Pemanggilan alat dan argumen fungsi
* Pemikiran diperpanjang (saat diaktifkan)

Pendekatan ini memiliki dua keuntungan utama:

1. Tidak memerlukan pemikiran untuk diaktifkan.
2. Dapat memengaruhi semua pengeluaran token termasuk pemanggilan alat. Misalnya, effort yang lebih rendah berarti Claude melakukan lebih sedikit pemanggilan alat. Ini memberikan tingkat kontrol yang jauh lebih besar atas efisiensi.

### Tingkat effort

| Tingkat  | Deskripsi                                                                                                                                                                                                                   | Kasus penggunaan umum                                                                                     |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum mutlak tanpa batasan pengeluaran token. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. | Tugas yang memerlukan penalaran terdalam dan analisis paling menyeluruh                                   |
| `xhigh`  | Kemampuan diperluas untuk pekerjaan jangka panjang. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5.                                                                   | Tugas agentik dan pemrograman yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter.                                                                                                                                                                   | Penalaran kompleks, masalah pemrograman yang sulit, tugas agentik                                         |
| `medium` | Pendekatan seimbang dengan penghematan token moderat.                                                                                                                                                                       | Tugas agentik yang memerlukan keseimbangan antara kecepatan, biaya, dan kinerja                           |
| `low`    | Paling efisien. Penghematan token signifikan dengan sedikit pengurangan kemampuan.                                                                                                                                          | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagen         |

<Note>
  Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude tetap akan berpikir pada masalah yang cukup sulit, tetapi akan berpikir lebih sedikit dibandingkan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

### Tingkat effort yang direkomendasikan untuk Claude Sonnet 5

Claude Sonnet 5 secara default menggunakan effort `high`.

* **Effort high (default):** Cocok untuk penalaran kompleks, pemrograman, dan tugas agentik di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort xhigh:** Untuk tugas pemrograman dan agentik yang paling sulit. Lihat [Prompting Claude Sonnet 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5#calibrating-effort-and-thinking-depth).
* **Effort medium:** Penurunan tingkat untuk penghematan biaya dari default. Sebanding dengan Claude Sonnet 4.6 pada effort high.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-pemrograman di mana waktu respons yang lebih cepat diprioritaskan.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi mutlak tanpa batasan pengeluaran token.

### Tingkat effort yang direkomendasikan untuk Sonnet 4.6

Sonnet 4.6 secara default menggunakan effort `high`. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

* **Effort medium** (default yang direkomendasikan): Keseimbangan terbaik antara kecepatan, biaya, dan kinerja untuk sebagian besar aplikasi. Cocok untuk pemrograman agentik, alur kerja yang banyak menggunakan alat, dan pembuatan kode.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-pemrograman di mana waktu respons yang lebih cepat diprioritaskan.
* **Effort high:** Untuk penalaran kompleks dan tugas di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi mutlak tanpa batasan pengeluaran token.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.7

**Mulailah dengan `xhigh` untuk kasus penggunaan pemrograman dan agentik**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap kecerdasan. Turunkan ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naikkan ke `max` hanya ketika evaluasi Anda menunjukkan ruang peningkatan yang terukur pada `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit; nilai yang Anda berikan akan menggantikan default.

| Effort   | Panduan untuk Claude Opus 4.7                                                                                                                                                                                                                                                                                            |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `low`    | Efisien, tetapi paling baik untuk tugas pendek dan terbatas. Pasangkan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian.                                                                                                                                                                   |
| `medium` | Pilihan langsung untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya.                                                                                                                                                                                                           |
| `high`   | Kasus penggunaan lanjutan yang masih memerlukan keseimbangan antara kecerdasan dan konsumsi token. Ini sering kali merupakan keseimbangan terbaik antara kualitas dan efisiensi token.                                                                                                                                   |
| `xhigh`  | Titik awal yang direkomendasikan untuk pekerjaan pemrograman dan agentik, serta untuk tugas eksploratif seperti pemanggilan alat berulang, pencarian web terperinci, dan pencarian basis pengetahuan. Perkirakan penggunaan token yang jauh lebih tinggi daripada `high`.                                                |
| `max`    | Cadangkan untuk masalah yang benar-benar di garis depan. Pada sebagian besar beban kerja, `max` menambah biaya signifikan untuk peningkatan kualitas yang relatif kecil, dan pada beberapa tugas output terstruktur atau tugas yang kurang sensitif terhadap kecerdasan, hal ini dapat menyebabkan pemikiran berlebihan. |

Claude Opus 4.7 juga mematuhi tingkat effort dengan lebih ketat dibandingkan Claude Opus 4.6, terutama pada `low` dan `medium`. Pada tingkat effort yang lebih rendah, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort alih-alih mengakalinya dengan prompt. Jika Anda harus mempertahankan effort rendah demi latensi, tambahkan panduan yang terarah seperti "Tugas ini melibatkan penalaran multilangkah. Pikirkan dengan cermat sebelum merespons."

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Opus 4.8

Panduan untuk Claude Opus 4.7 juga berlaku untuk Claude Opus 4.8. **Mulailah dengan `xhigh` untuk kasus penggunaan pemrograman dan agentik**, gunakan `high` untuk sebagian besar beban kerja lain yang sensitif terhadap kecerdasan, dan turunkan ke `medium` atau `low` hanya ketika Anda telah mengukur bahwa tingkat yang lebih rendah tetap mempertahankan kualitas pada evaluasi Anda.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda; nilai yang Anda berikan akan menggantikan default.

Saat menjalankan Claude Opus 4.8 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Tingkat effort yang direkomendasikan untuk Claude Fable 5

Effort adalah kontrol utama untuk menyeimbangkan kecerdasan, latensi, dan biaya pada Claude Fable 5. **Mulailah dengan `high`, yaitu default, untuk sebagian besar tugas**, gunakan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 tetap berkinerja baik dan sering kali melampaui kinerja `xhigh` pada model sebelumnya. Pada `high` dan `xhigh`, atur `max_tokens` yang besar: ini adalah batas keras pada total output, pemikiran ditambah teks respons. Lihat [Kontrol biaya](/docs/id/build-with-claude/adaptive-thinking#cost-control).

Kurangi effort jika tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan lebih interaktif. Rekomendasi yang sama berlaku untuk Claude Mythos 5. Untuk panduan yang lebih lengkap, lihat [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Penggunaan dasar

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
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
    --transform 'content.0.text' \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Analyze the trade-offs between microservices and monolithic architectures
  output_config:
    effort: medium
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Analyze the trade-offs between microservices and monolithic architectures",
          }
      ],
      output_config={"effort": "medium"},
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Analyze the trade-offs between microservices and monolithic architectures" }],
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(4096L)
      .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.MEDIUM)
          .build())
      .build();

  Message response = client.messages().create(params);
  response.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
      ],
      model: 'claude-opus-4-8',
      outputConfig: ['effort' => 'medium'],
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
    ],
    output_config: {
      effort: "medium"
    }
  )

  puts message.content.first.text
  ```
</CodeGroup>

## Kapan menyesuaikan parameter effort

* Gunakan **effort max** ketika Anda membutuhkan kemampuan tertinggi mutlak tanpa batasan: penalaran paling menyeluruh dan analisis terdalam. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6.
* Gunakan **effort xhigh** untuk pemrograman lanjutan dan pekerjaan agentik kompleks yang memerlukan eksplorasi diperpanjang, seperti pemanggilan alat berulang dan pencarian terperinci. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5.
* Gunakan **effort high** (default) untuk penalaran kompleks, analisis bernuansa, masalah pemrograman yang sulit, atau tugas apa pun di mana kualitas lebih penting daripada kecepatan atau biaya.
* Gunakan **effort medium** sebagai opsi seimbang ketika Anda menginginkan kinerja yang solid tanpa pengeluaran token penuh dari effort high.
* Gunakan **effort low** ketika Anda mengoptimalkan kecepatan (karena Claude menjawab dengan lebih sedikit token) atau biaya. Misalnya, tugas klasifikasi sederhana, pencarian cepat, atau kasus penggunaan bervolume tinggi di mana peningkatan kualitas marginal tidak sebanding dengan latensi atau pengeluaran tambahan.

<Note>
  **Mode ultracode Claude Code:** ultracode muncul di menu effort Claude Code, tetapi ini bukan tingkat effort API tambahan. Nilai-nilai yang didokumentasikan di halaman ini adalah kumpulan lengkap yang diterima API. Ultracode memasangkan tingkat effort `xhigh` dengan izin tetap bagi Claude Code untuk meluncurkan alur kerja multiagen, yang diberikan melalui [Pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages). Untuk membangun perilaku serupa dengan API, lihat [Membangun mode orkestrasi](/docs/id/build-with-claude/mid-conversation-effort-example).
</Note>

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort memengaruhi baik penjelasan seputar pemanggilan alat maupun pemanggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

* Menggabungkan beberapa operasi menjadi lebih sedikit pemanggilan alat
* Melakukan lebih sedikit pemanggilan alat
* Langsung melanjutkan ke tindakan tanpa pengantar
* Menggunakan pesan konfirmasi singkat setelah selesai

Tingkat effort yang lebih tinggi mungkin:

* Melakukan lebih banyak pemanggilan alat
* Menjelaskan rencana sebelum mengambil tindakan
* Memberikan ringkasan perubahan yang terperinci
* Menyertakan komentar kode yang lebih komprehensif

## Effort dengan pemikiran diperpanjang

Parameter effort bekerja bersama pemikiran diperpanjang. Perilakunya bergantung pada model:

* **Claude Fable 5 dan Claude Mythos 5** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking), yang selalu aktif (tidak memerlukan konfigurasi `thinking`). `thinking: {type: "disabled"}` ditolak. Effort mengontrol kedalaman pemikiran dengan cara yang sama seperti pada Opus 4.8 dan Opus 4.7.
* **Claude Opus 4.8** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Model memutuskan kapan dan seberapa banyak berpikir berdasarkan setiap permintaan, sehingga hanya memicu pemikiran saat diperlukan. Pada effort `high`, `xhigh`, dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana. Atur `thinking: {type: "adaptive"}` untuk mengaktifkan pemikiran; tanpanya, permintaan berjalan tanpa pemikiran.
* **Claude Mythos Preview** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) secara default (tidak memerlukan konfigurasi `thinking`). `thinking: {type: "disabled"}` ditolak. Effort mengontrol kedalaman pemikiran dengan cara yang sama seperti pada Opus 4.7 dan Opus 4.6.
* **Claude Opus 4.7** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak lagi didukung pada Opus 4.7; gunakan pemikiran adaptif dengan effort sebagai gantinya. Pada effort `high`, `xhigh`, dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana.
* **Claude Opus 4.6** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Meskipun `budget_tokens` masih diterima pada Opus 4.6, parameter ini sudah usang dan akan dihapus pada rilis mendatang. Pada effort `high` dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana.
* **Claude Sonnet 5** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking), yang aktif secara default (tidak memerlukan konfigurasi `thinking`), dan effort adalah kontrol yang direkomendasikan untuk kedalaman pemikiran. Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Berikan `thinking: {type: "disabled"}` untuk menonaktifkan pemikiran. Pada effort `high` (default), `xhigh`, dan `max`, Claude hampir selalu berpikir secara mendalam. Pada tingkat yang lebih rendah, Claude mungkin melewatkan pemikiran untuk masalah yang lebih sederhana.
* **Claude Sonnet 4.6** menggunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (di mana effort mengontrol kedalaman pemikiran). Pemikiran manual dengan [mode interleaved](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) (`thinking: {type: "enabled", budget_tokens: N}`) masih berfungsi tetapi sudah usang.
* **Claude Opus 4.5** menggunakan pemikiran manual (`thinking: {type: "enabled", budget_tokens: N}`), di mana effort bekerja bersama anggaran token pemikiran. Atur tingkat effort untuk tugas Anda, lalu atur anggaran token pemikiran berdasarkan kompleksitas tugas.

Parameter effort dapat digunakan dengan atau tanpa pemikiran diperpanjang diaktifkan. Saat digunakan tanpa pemikiran, parameter ini tetap mengontrol pengeluaran token keseluruhan untuk respons teks dan pemanggilan alat.

## Praktik terbaik

1. **Atur effort secara eksplisit:** API secara default menggunakan `high`, tetapi titik awal yang tepat bergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugas bersifat sederhana, effort low dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak tingkat effort bervariasi menurut jenis tugas. Evaluasi kinerja pada kasus penggunaan spesifik Anda sebelum melakukan deployment.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin cukup dengan effort low sementara pemrograman agentik dan penalaran kompleks mendapat manfaat dari effort high.

## Langkah selanjutnya

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token advisori untuk seluruh loop agentik guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Biarkan Claude secara dinamis menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang dengan mode pemikiran adaptif.
  </Card>

  <Card title="Membangun dengan pemikiran diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Berikan Claude penalaran yang ditingkatkan untuk tugas kompleks dengan anggaran pemikiran manual, penggunaan alat, dan caching prompt.
  </Card>
</CardGroup>
