---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 31e25196e11bebac7d65ce2b08d65cf3bebb1d846fdf67c0754208c01eb34663
---

---
title: Apa yang baru di Claude Opus 5
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5
description: Ikhtisar fitur baru dan perubahan perilaku di Claude Opus 5.
---

Claude Opus 5 merupakan peningkatan signifikan dibandingkan Claude Opus 4.8, dengan peningkatan terbesar pada penalaran mendalam, tugas agentik dan jangka panjang, serta penskalaan komputasi saat pengujian. Halaman ini merangkum semua hal baru di Claude Opus 5, termasuk pemikiran yang aktif secara default, perubahan alat di tengah percakapan, dan perubahan yang bersifat breaking terkait kapan pemikiran dapat dinonaktifkan.

## Model baru

| Model         | ID model API    | Deskripsi                                                      |
| ------------- | --------------- | -------------------------------------------------------------- |
| Claude Opus 5 | `claude-opus-5` | Untuk pengodean agentik yang kompleks dan pekerjaan enterprise |

Claude Opus 5 memiliki [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (1 juta token adalah nilai default sekaligus maksimum; tidak ada varian konteks yang lebih kecil), output maksimum 128 ribu token, dan [pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview).

## Fitur baru

### Perubahan alat di tengah percakapan (beta)

Anda dapat menambahkan atau menghapus alat di antara giliran percakapan sambil mempertahankan cache prompt, alih-alih mengirim ulang daftar alat yang tetap selama masa sesi. Perubahan alat di tengah percakapan masih dalam tahap beta: sertakan header beta `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda. Lihat [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) untuk cara penggunaannya.

### Mode fallback default

Parameter `fallbacks` mendukung mode `"default"` baru, yang menerapkan model fallback yang direkomendasikan Anthropic berdasarkan kategori penolakan, alih-alih daftar model yang Anda kelola sendiri. Seluruh parameter `fallbacks` masih dalam tahap beta. Gunakan header beta `server-side-fallback-2026-07-01`, yang mendukung mode `"default"` maupun daftar model eksplisit (header `server-side-fallback-2026-06-01` sebelumnya hanya menerima daftar eksplisit). Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

### Minimum cache prompt yang lebih rendah

Panjang prompt minimum yang dapat di-cache pada Claude Opus 5 adalah 512 token, turun dari 1.024 token pada Claude Opus 4.8. Prompt yang sebelumnya terlalu pendek untuk di-cache pada Claude Opus 4.8 kini dapat membuat entri cache tanpa perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk nilai minimum per model.

### Mode cepat

[Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) tersedia untuk Claude Opus 5 hanya pada Claude API; saat ini tidak tersedia di Amazon Bedrock, Google Cloud, atau Microsoft Foundry. Mode cepat untuk Claude Opus 5 dihargai $10 USD per juta token input dan $50 USD per juta token output. Lihat [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk akses, model yang didukung, dan harga.

## Perubahan perilaku

### Pemikiran aktif secara default

Pada Claude Opus 4.8, permintaan berjalan tanpa pemikiran kecuali Anda mengatur `thinking: {"type": "adaptive"}`. Pada Claude Opus 5, permintaan yang sama berjalan dengan [pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif: model memutuskan kapan dan seberapa banyak berpikir pada setiap giliran, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol untuk kedalaman pemikiran. Nilai wire tidak berubah; `thinking: {"type": "adaptive"}` tetap valid dan setara dengan default.

Karena `max_tokens` adalah batas keras pada total output (pemikiran ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang berjalan tanpa pemikiran pada Claude Opus 4.8.

API tetap menyediakan opsi untuk menonaktifkan pemikiran, dengan tunduk pada batasan effort di bawah ini.

### Effort menjadi lebih penting

Claude Opus 5 mengonversi [effort](https://platform.claude.com/docs/id/build-with-claude/effort) tambahan menjadi hasil yang lebih baik secara lebih andal dibandingkan model Opus sebelumnya, sehingga tingkat effort yang Anda pilih memiliki bobot lebih besar. Seluruh tingkatan tersedia: `low`, `medium`, `high`, `xhigh`, dan `max`, dengan `max` sebagai tingkat tertinggi untuk penalaran sedalam mungkin. Mulailah dari default, `high`, dan sesuaikan ke salah satu arah berdasarkan evaluasi Anda: turunkan jika kualitas tetap terjaga untuk menghemat token dan latensi, atau naikkan untuk pekerjaan yang paling menuntut. Saat berjalan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat.

Permintaan ini menaikkan effort hingga ke `max`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 64000,
      "stream": true,
      "output_config": {
        "effort": "max"
      },
      "messages": [
        {
          "role": "user",
          "content": "Explain why the sum of two even numbers is always even."
        }
      ]
    }'
  ```

  ```bash CLI
  # max_tokens 64k dapat melebihi batas waktu non-streaming; lakukan streaming event.
  ant messages create --stream --format jsonl <<'YAML'
  model: claude-opus-5
  max_tokens: 64000
  output_config:
    effort: max
  messages:
    - role: user
      content: Explain why the sum of two even numbers is always even.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-5",
      max_tokens=64000,
      output_config={"effort": "max"},
      messages=[
          {
              "role": "user",
              "content": "Explain why the sum of two even numbers is always even.",
          }
      ],
  ) as stream:
      response = stream.get_final_message()

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-5",
    max_tokens: 64000,
    output_config: {
      effort: "max"
    },
    messages: [
      {
        role: "user",
        content: "Explain why the sum of two even numbers is always even."
      }
    ]
  });

  const response = await stream.finalMessage();
  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 64000,
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Max
      },
      Messages = [new() { Role = Role.User, Content = "Explain why the sum of two even numbers is always even." }]
  };

  var response = await client.Messages.CreateStreaming(parameters).Aggregate();
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 64000,
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMax,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Explain why the sum of two even numbers is always even.")),
  	},
  })

  response := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := response.Accumulate(event); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(64000L)
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.MAX)
          .build())
      .addUserMessage("Explain why the sum of two even numbers is always even.")
      .build();

  MessageAccumulator accumulator = MessageAccumulator.create();
  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(accumulator::accumulate);
  }

  Message response = accumulator.message();
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 64000,
      messages: [
          ['role' => 'user', 'content' => 'Explain why the sum of two even numbers is always even.']
      ],
      model: Model::CLAUDE_OPUS_5,
      outputConfig: ['effort' => Effort::MAX],
  );

  $accumulator = MessageAccumulator::forMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
  }

  echo $accumulator->message();
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.stream(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 64000,
    output_config: {
      effort: :max
    },
    messages: [
      { role: "user", content: "Explain why the sum of two even numbers is always even." }
    ]
  ).accumulated_message

  puts response
  ```
</CodeGroup>

Pemikiran [aktif secara default](https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5#thinking-on-by-default) pada Claude Opus 5, sehingga field `thinking` tidak diperlukan.

### Menonaktifkan pemikiran memerlukan effort `high` atau lebih rendah

Pada Claude Opus 5, `thinking: {"type": "disabled"}` hanya diterima ketika tingkat effort adalah `high` atau lebih rendah. Mengatur `thinking: {"type": "disabled"}` dengan effort `xhigh` atau `max` akan mengembalikan error 400. Ini adalah perilaku yang tersedia secara umum pada Claude Opus 5 dan seterusnya, diterapkan pada setiap permintaan, dan merupakan perubahan yang bersifat breaking dari Claude Opus 4.8, di mana menonaktifkan pemikiran tidak bergantung pada tingkat effort. Jika saat ini Anda menonaktifkan pemikiran pada tingkat effort tinggi, pilih salah satu: tetap nonaktifkan pemikiran dan atur effort ke `high` atau lebih rendah, atau pertahankan tingkat effort dan hapus field `thinking`.

Dengan pemikiran dinonaktifkan, Claude Opus 5 terkadang dapat menulis pemanggilan alat ke dalam output teksnya alih-alih mengeluarkan blok `tool_use`, atau menyertakan tag XML internal dalam respons yang terlihat. Jika memungkinkan, biarkan pemikiran tetap aktif dan kendalikan biaya token dengan tingkat effort yang lebih rendah; untuk integrasi yang harus tetap menonaktifkan pemikiran, lihat [Menjalankan dengan pemikiran dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi melalui prompting.

### Perbedaan perilaku model

Di luar perubahan API di atas, Claude Opus 5 berperilaku berbeda dari Claude Opus 4.8 dalam cara-cara yang mungkin Anda perhatikan tanpa mengubah kode apa pun. Respons default yang ditampilkan kepada pengguna dan hasil tertulis cenderung lebih panjang. Dalam sesi agentik, model lebih sering menarasikan progresnya kepada pengguna. Dalam kerangka kerja multi-agen, model lebih mudah mendelegasikan ke subagen. Model juga memverifikasi pekerjaannya sendiri tanpa diminta, jadi hapus instruksi verifikasi yang dibawa dari model sebelumnya ("sertakan langkah verifikasi akhir," "gunakan subagen untuk memverifikasi"); instruksi tersebut menyebabkan verifikasi berlebihan pada Claude Opus 5. Untuk pola prompting yang menyesuaikan masing-masing perilaku ini, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5).

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, Claude Opus 5 merupakan peningkatan signifikan, bukan sekadar inkremental, dan menghadirkan kecerdasan terdepan dengan setengah biaya Claude Fable 5. Peningkatan terbesar terdapat pada:

* **Penalaran mendalam**, mempertahankan analisis multi-langkah di sepanjang rantai masalah yang panjang.
* **Pengodean agentik dan tugas jangka panjang**, tetap fokus pada tugas di sepanjang loop penggunaan alat yang diperpanjang dan menyelesaikan fitur multi-file, refaktor yang lebih besar, serta pekerjaan fitur end-to-end tanpa meninggalkan stub atau placeholder.
* **Penskalaan komputasi saat pengujian**, mengonversi effort tambahan (hingga tingkat `max`) menjadi hasil yang lebih baik.
* **Efisiensi pada tingkat effort yang lebih rendah**, dengan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `low` dan `medium` menghasilkan kualitas yang kuat dengan sebagian kecil token dan latensi dibandingkan pengaturan yang lebih tinggi.
* **Tinjauan kode dan pencarian bug**, menemukan bug nyata dengan tingkat keberhasilan tinggi per pemeriksaan dengan sedikit false positive, dan tetap akurat pada tingkat effort yang lebih rendah.
* **Visi**, memahami grafik, dokumen, dan diagram serta mereplikasi visual UI dan frontend, paling kuat ketika diberi alat untuk menganalisis, memotong, dan memverifikasi pekerjaannya secara iteratif.
* **Pekerjaan konteks panjang**, dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) sebagai default sekaligus maksimum, serta kepatuhan instruksi, pemanggilan alat, dan penalaran yang konsisten di sepanjang jendela tersebut.
* **Tugas perkantoran dan dokumen**, menghasilkan dan mengedit spreadsheet multi-sheet yang kompleks dengan rumus non-trivial, serta menghasilkan slide deck yang terstruktur dengan baik.
* **Koordinasi multi-agen**, menjalankan tim subagen dengan pola penulis-verifikator yang efektif dan sedikit kasus agen yang saling menimpa pekerjaan satu sama lain.

Untuk pola prompting yang memaksimalkan kemampuan-kemampuan ini, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#capability-improvements).

## Harga

Claude Opus 5 dihargai $5 USD per juta token input dan $25 USD per juta token output, tidak berubah dari Claude Opus 4.8.

Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga lengkap, termasuk pemrosesan batch, caching prompt, dan tarif mode cepat.

## Ketersediaan

Claude Opus 5 tersedia di:

* **Claude API:** tersedia untuk semua pelanggan, sebagai `claude-opus-5`.
* **AWS:** tersedia melalui [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-opus-5`. Claude Opus 5 juga dapat diakses melalui API `InvokeModel` pada `bedrock-runtime`, dilayani oleh infrastruktur yang sama; integrasi [Claude di Amazon Bedrock (legacy)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) tidak menyertakannya dalam tabel ID model berversi ARN.
* **Google Cloud:** tersedia melalui [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), sebagai `claude-opus-5`.
* **Microsoft Foundry:** tersedia melalui [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

Claude Opus 4.8 tetap tersedia di semua platform tersebut.

## Panduan migrasi

Untuk bermigrasi dari Claude Opus 4.8, perbarui ID model Anda:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-opus-4-8"  # Before
  model = "claude-opus-5"  # After
  ```

  ```typescript TypeScript
  let model = "claude-opus-4-8"; // Before
  model = "claude-opus-5"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeOpus4_8; // Before
  model = Model.ClaudeOpus5; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeOpus4_8 // Before
  model = anthropic.ModelClaudeOpus5    // After
  ```

  ```java Java
  Model model = Model.CLAUDE_OPUS_4_8; // Before
  model = Model.CLAUDE_OPUS_5; // After
  ```

  ```php PHP
  $model = Model::CLAUDE_OPUS_4_8; // Before
  $model = Model::CLAUDE_OPUS_5; // After
  ```

  ```ruby Ruby
  model = Anthropic::Model::CLAUDE_OPUS_4_8 # Before
  model = Anthropic::Model::CLAUDE_OPUS_5 # After
  ```
</CodeGroup>

Kemudian tinjau dua [perubahan perilaku](https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5#behavior-changes): pemikiran aktif secara default, dan menonaktifkan pemikiran dengan effort `xhigh` atau `max` akan mengembalikan error 400. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5) untuk instruksi langkah demi langkah.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/about-claude/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Prompting Claude Opus 5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5">
    Perbedaan perilaku dan pola prompting khusus untuk Claude Opus 5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Pemikiran" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran saat aktif secara default, dan kapan dapat dinonaktifkan.
  </Card>

  <Card title="Anggaran tugas" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token sebagai panduan untuk mengatur ritme kerjanya.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/about-claude/models/migration-guide">
    Panduan untuk bermigrasi ke model Claude terbaru dari versi Claude sebelumnya.
  </Card>

  <Card title="Mode cepat" icon="bolt" href="https://platform.claude.com/docs/id/build-with-claude/fast-mode">
    Dapatkan token output per detik yang lebih tinggi dari model Claude Opus dengan harga premium.
  </Card>
</CardGroup>
