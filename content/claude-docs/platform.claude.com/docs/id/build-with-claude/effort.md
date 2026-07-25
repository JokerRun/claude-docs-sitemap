---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 7019b4817d2cc5705b01a0765c384bf7cc28ff4cea965f8a305443c67ea320c2
---

# Effort

Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Parameter effort memungkinkan Anda mengontrol berapa banyak token yang digunakan Claude saat merespons permintaan. Anda dapat menyeimbangkan antara ketelitian respons dan efisiensi token dengan satu model. Parameter effort tersedia pada model-model berikut tanpa memerlukan header beta.

<Note>
  Parameter effort didukung oleh Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 5, Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, dan Claude Opus 4.5.
</Note>

<Tip>
  Untuk mengetahui bagaimana effort berinteraksi dengan thinking dan kontrol mana yang harus digunakan, lihat [Thinking dan effort](/docs/id/build-with-claude/thinking#thinking-and-effort). Di mana adaptive thinking tersedia, effort adalah cara yang direkomendasikan untuk mengontrol kedalaman thinking.
</Tip>

## Cara kerja effort

Secara default, Claude menggunakan effort tinggi, menghabiskan token sebanyak yang diperlukan untuk hasil yang sangat baik. Anda dapat menaikkan level effort ke `max` untuk kemampuan tertinggi secara absolut, atau menurunkannya agar lebih konservatif dalam penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima sedikit pengurangan kemampuan.

<Tip>
  Mengatur `effort` ke `"high"` menghasilkan perilaku yang persis sama dengan menghilangkan parameter `effort` sepenuhnya.
</Tip>

Parameter effort memengaruhi **semua token** dalam respons, termasuk:

* Respons teks dan penjelasan
* Pemanggilan alat dan argumen fungsi
* Thinking (saat aktif)

Pendekatan ini memiliki dua keuntungan utama:

1. Tidak memerlukan thinking untuk diaktifkan.
2. Dapat memengaruhi semua pengeluaran token termasuk pemanggilan alat. Misalnya, effort yang lebih rendah berarti Claude melakukan lebih sedikit pemanggilan alat. Ini memberikan tingkat kontrol yang jauh lebih besar atas efisiensi.

### Level effort

| Level    | Deskripsi                                                                                                                                                                                                                                        | Kasus penggunaan umum                                                                                |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum absolut tanpa batasan pada pengeluaran token. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6. | Tugas yang memerlukan penalaran terdalam dan analisis paling menyeluruh                              |
| `xhigh`  | Kemampuan yang diperluas untuk pekerjaan jangka panjang. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5.                                                                    | Tugas agentik dan coding yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Kemampuan tinggi. Setara dengan tidak mengatur parameter.                                                                                                                                                                                        | Penalaran kompleks, masalah coding yang sulit, tugas agentik                                         |
| `medium` | Pendekatan seimbang dengan penghematan token moderat.                                                                                                                                                                                            | Tugas agentik yang memerlukan keseimbangan antara kecepatan, biaya, dan kinerja                      |
| `low`    | Paling efisien. Penghematan token signifikan dengan sedikit pengurangan kemampuan.                                                                                                                                                               | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagen    |

`xhigh` adalah level yang lebih baru; beberapa model yang mendukung `max` tidak mendukung `xhigh`.

<Note>
  Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada level effort yang lebih rendah, Claude masih akan berpikir pada masalah yang cukup sulit, tetapi akan berpikir lebih sedikit dibandingkan pada level effort yang lebih tinggi untuk masalah yang sama.
</Note>

### Level effort yang direkomendasikan untuk Claude Sonnet 5

Claude Sonnet 5 secara default menggunakan effort `high` pada Claude API dan Claude Code.

* **Effort high (default):** Cocok untuk penalaran kompleks, coding, dan tugas agentik di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort xhigh:** Untuk tugas coding dan agentik yang paling sulit. Lihat [Prompting Claude Sonnet 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5#calibrating-effort-and-thinking-depth).
* **Effort medium:** Penurunan hemat biaya dari default. Sebanding dengan Claude Sonnet 4.6 pada effort high.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana waktu penyelesaian yang lebih cepat diprioritaskan.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi secara absolut tanpa batasan pada pengeluaran token.

### Level effort yang direkomendasikan untuk Claude Sonnet 4.6

Sonnet 4.6 secara default menggunakan effort `high`. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

* **Effort medium** (default yang direkomendasikan): Keseimbangan terbaik antara kecepatan, biaya, dan kinerja untuk sebagian besar aplikasi. Cocok untuk agentic coding, alur kerja yang banyak menggunakan alat, dan pembuatan kode.
* **Effort low:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana waktu penyelesaian yang lebih cepat diprioritaskan.
* **Effort high:** Untuk penalaran kompleks dan tugas di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi secara absolut tanpa batasan pada pengeluaran token.

### Level effort yang direkomendasikan untuk Claude Opus 4.7

**Mulai dengan `xhigh` untuk kasus penggunaan coding dan agentik**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap kecerdasan. Turunkan ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naikkan ke `max` hanya ketika evaluasi Anda menunjukkan ruang peningkatan yang terukur pada `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit; nilai yang Anda berikan menggantikan default.

| Effort   | Panduan untuk Claude Opus 4.7                                                                                                                                                                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `low`    | Efisien, tetapi paling baik untuk tugas pendek dan terbatas. Pasangkan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian.                                                                                                                                                          |
| `medium` | Pilihan langsung untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya.                                                                                                                                                                                                  |
| `high`   | Kasus penggunaan lanjutan yang masih memerlukan keseimbangan antara kecerdasan dan konsumsi token. Ini sering kali merupakan keseimbangan terbaik antara kualitas dan efisiensi token.                                                                                                                          |
| `xhigh`  | Titik awal yang direkomendasikan untuk pekerjaan coding dan agentik, serta untuk tugas eksploratif seperti pemanggilan alat berulang, pencarian web terperinci, dan pencarian basis pengetahuan. Perkirakan penggunaan token yang jauh lebih tinggi daripada `high`.                                            |
| `max`    | Simpan untuk masalah yang benar-benar di garis depan. Pada sebagian besar beban kerja, `max` menambahkan biaya signifikan untuk peningkatan kualitas yang relatif kecil, dan pada beberapa tugas structured-output atau tugas yang kurang sensitif terhadap kecerdasan, hal ini dapat menyebabkan overthinking. |

Claude Opus 4.7 juga mematuhi level effort lebih ketat daripada Claude Opus 4.6, terutama pada `low` dan `medium`. Pada level effort yang lebih rendah, model membatasi pekerjaannya pada apa yang diminta daripada melakukan lebih dari yang diminta. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort daripada mengakalinya dengan prompt. Jika Anda harus menjaga effort tetap rendah demi latensi, tambahkan panduan yang terarah seperti "Tugas ini melibatkan penalaran multilangkah. Pikirkan dengan cermat sebelum merespons."

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Level effort yang direkomendasikan untuk Claude Opus 4.8

Panduan untuk Claude Opus 4.7 juga berlaku untuk Claude Opus 4.8. **Mulai dengan `xhigh` untuk kasus penggunaan coding dan agentik**, gunakan `high` untuk sebagian besar beban kerja lain yang sensitif terhadap kecerdasan, dan turunkan ke `medium` atau `low` hanya ketika Anda telah mengukur bahwa level yang lebih rendah mempertahankan kualitas pada evaluasi Anda.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan level yang berbeda; nilai yang Anda berikan menggantikan default.

Saat menjalankan Claude Opus 4.8 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Level effort yang direkomendasikan untuk Claude Opus 5

Claude Opus 5 mendukung kelima level effort. **Mulai dengan `high`, yaitu default**, dan sesuaikan berdasarkan evaluasi Anda: naikkan ke `xhigh` untuk pekerjaan coding dan agentik yang menuntut, atau ke `max` ketika suatu tugas membenarkan pengeluaran token tanpa batasan, dan gunakan `low` dan `medium` secara leluasa sebagai kontrol utama Anda untuk biaya token dan waktu respons di mana pun evaluasi Anda menunjukkan kualitas tetap terjaga. Jika Anda membawa pengaturan effort dari model sebelumnya, jalankan pengujian effort yang baru pada evaluasi Anda daripada menggunakannya kembali.

Effort mengontrol volume thinking, bukan panjang respons yang terlihat: pada Claude Opus 5, mengubah effort tidak secara andal memperpendek respons, jadi [gunakan prompt untuk mengatur panjang](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) sebagai gantinya.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan level yang berbeda; nilai yang Anda berikan menggantikan default.

Pada Claude Opus 5, thinking tidak dapat dinonaktifkan pada effort `xhigh` atau `max`: permintaan yang mengatur `thinking: {"type": "disabled"}` pada level tersebut mengembalikan error 400. Lihat [Effort dengan thinking](#effort-with-thinking).

Saat menjalankan Claude Opus 5 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

### Level effort yang direkomendasikan untuk Claude Fable 5

Effort adalah kontrol utama untuk menyeimbangkan kecerdasan, latensi, dan biaya pada Claude Fable 5. **Mulai dengan `high`, yaitu default, untuk sebagian besar tugas**, gunakan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 masih berkinerja baik dan sering kali melampaui kinerja `xhigh` pada model sebelumnya. Pada `high` dan `xhigh`, atur `max_tokens` yang besar: ini adalah batas keras pada total output, thinking ditambah teks respons. Lihat [Kontrol biaya](/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

Kurangi effort jika suatu tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan lebih interaktif. Rekomendasi yang sama berlaku untuk Claude Mythos 5. Untuk panduan yang lebih lengkap, lihat [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Penggunaan dasar

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
    --transform 'content.#(type=="text").text' \
    --raw-output <<'YAML'
  model: claude-opus-5
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

## Kapan menyesuaikan parameter effort

* Gunakan **effort max** ketika Anda membutuhkan kemampuan tertinggi secara absolut tanpa batasan: penalaran paling menyeluruh dan analisis terdalam. Tersedia pada Claude 4.6 dan model yang lebih baru serta Claude Mythos Preview.
* Gunakan **effort xhigh** untuk coding lanjutan dan pekerjaan agentik kompleks yang memerlukan eksplorasi yang diperluas, seperti pemanggilan alat berulang dan pencarian terperinci. Tersedia pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5.
* Gunakan **effort high** (default) untuk penalaran kompleks, analisis bernuansa, masalah coding yang sulit, atau tugas apa pun di mana kualitas lebih penting daripada kecepatan atau biaya.
* Gunakan **effort medium** sebagai opsi seimbang ketika Anda menginginkan kinerja yang solid tanpa pengeluaran token penuh dari effort high.
* Gunakan **effort low** ketika Anda mengoptimalkan kecepatan (karena Claude menjawab dengan lebih sedikit token) atau biaya. Misalnya, tugas klasifikasi sederhana, pencarian cepat, atau kasus penggunaan bervolume tinggi di mana peningkatan kualitas marginal tidak membenarkan latensi atau pengeluaran tambahan.

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort memengaruhi baik penjelasan di sekitar pemanggilan alat maupun pemanggilan alat itu sendiri. Level effort yang lebih rendah cenderung:

* Menggabungkan beberapa operasi menjadi lebih sedikit pemanggilan alat
* Melakukan lebih sedikit pemanggilan alat
* Langsung melanjutkan ke tindakan tanpa pembukaan
* Menggunakan pesan konfirmasi singkat setelah selesai

Level effort yang lebih tinggi mungkin:

* Melakukan lebih banyak pemanggilan alat
* Menjelaskan rencana sebelum mengambil tindakan
* Memberikan ringkasan perubahan yang terperinci
* Menyertakan komentar kode yang lebih komprehensif

## Effort dengan thinking

Parameter `thinking` mengontrol apakah Claude berpikir dalam [blok pemikiran](/docs/id/build-with-claude/thinking) sebelum menjawab; parameter `effort` mengontrol seberapa banyak upaya yang Claude curahkan untuk keseluruhan respons, yang dalam mode adaptif mencakup seberapa sering dan seberapa dalam Claude berpikir. Jangan meneruskan `adaptive` sebagai nilai `effort`: `adaptive` adalah mode berpikir, bukan tingkat effort.

Pada level effort yang lebih tinggi, Claude berpikir pada sebagian besar permintaan dan dengan durasi yang lebih panjang; pada level yang lebih rendah, Claude dapat melewati thinking sepenuhnya untuk masalah yang lebih sederhana. Lihat [Thinking dan effort](/docs/id/build-with-claude/thinking#thinking-and-effort) untuk panduan lengkap tentang bagaimana kedua kontrol tersebut bekerja bersama.

Pada Claude Opus 4.5, satu-satunya model khusus extended-thinking yang mendukung effort, effort bekerja bersama [`budget_tokens`](/docs/id/build-with-claude/extended-thinking): atur level effort untuk tugas Anda, lalu atur anggaran token thinking berdasarkan seberapa dalam penalaran yang dibutuhkan tugas tersebut.

Untuk ketersediaan thinking per model, lihat [tabel konfigurasi per model](/docs/id/build-with-claude/thinking-troubleshooting#supported-models). Effort bekerja dengan atau tanpa thinking; lihat [Cara kerja effort](#how-effort-works).

## Mengubah effort di tengah percakapan

`output_config.effort` adalah pengaturan tingkat permintaan: setiap permintaan membawa nilainya sendiri, jadi untuk menjalankan bagian selanjutnya dari percakapan pada level effort yang berbeda, atur nilai baru pada permintaan berikutnya. Level effort berlaku untuk seluruh permintaan. Karena effort membentuk prompt yang dirender, mengubahnya di antara permintaan tidak mempertahankan prefiks yang di-cache dari giliran sebelumnya; jika Anda mengandalkan [caching prompt](/docs/id/build-with-claude/prompt-caching) di sepanjang sesi yang panjang, pilih level effort di awal dan pertahankan tetap konstan.

## Praktik terbaik

1. **Atur effort secara eksplisit:** API secara default menggunakan `high`, tetapi titik awal yang tepat bergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugas bersifat sederhana, effort low dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak level effort bervariasi menurut jenis tugas. Evaluasi kinerja pada kasus penggunaan spesifik Anda sebelum melakukan deployment.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin cukup dengan effort low sementara agentic coding dan penalaran kompleks mendapat manfaat dari effort high. Lihat poin berikutnya sebelum memvariasikannya dalam satu percakapan.
5. **Pertahankan effort tetap konstan dalam percakapan yang di-cache:** Mengubah nilai effort di antara permintaan membatalkan [caching prompt](/docs/id/build-with-claude/prompt-caching), jadi variasikan effort antar beban kerja daripada dalam percakapan yang mengandalkan cache hit. Lihat [Thinking dan caching prompt](/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

## Langkah selanjutnya

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token yang bersifat anjuran untuk seluruh loop agentik guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.
  </Card>

  <Card title="Mengarahkan thinking" icon="compass" href="/docs/id/build-with-claude/thinking-steering-and-cost">
    Pahami adaptive thinking, di mana Claude memutuskan kapan dan seberapa banyak berpikir, dan arahkan dengan effort dan prompting.
  </Card>

  <Card title="Thinking" icon="brain" href="/docs/id/build-with-claude/thinking">
    Pahami cara kerja thinking, kapan Claude berpikir secara default, dan bagaimana thinking berinteraksi dengan effort.
  </Card>
</CardGroup>
