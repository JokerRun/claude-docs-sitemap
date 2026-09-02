---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 9cbfd6f6555502a53f063e1bf49905a39e217875f93df1428b263a56814e43af
---

---
title: Apa yang baru di Claude Opus 5
url: https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5
description: Ikhtisar fitur baru dan perubahan perilaku di Claude Opus 5.
---

Claude Opus 5 adalah peningkatan lompatan besar dibandingkan Claude Opus 4.8, dengan kemajuan terbesar dalam penalaran mendalam, tugas agentik dan berjangka panjang, serta penskalaan komputasi saat pengujian (test-time compute scaling). Halaman ini merangkum semua yang baru di Claude Opus 5, termasuk perubahan alat di tengah percakapan dan dua perubahan yang merusak kompatibilitas (breaking changes) untuk kode yang berjalan di Claude Opus 4.8: thinking aktif secara default, dan thinking hanya dapat dinonaktifkan pada effort `high` atau lebih rendah.

## Model baru

| Model         | ID model API    | Deskripsi                                                      |
| ------------- | --------------- | -------------------------------------------------------------- |
| Claude Opus 5 | `claude-opus-5` | Untuk pengodean agentik yang kompleks dan pekerjaan enterprise |

Claude Opus 5 memiliki ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (1M token adalah default sekaligus maksimum; tidak ada varian konteks yang lebih kecil), 128k token output maksimum, dan [thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default. [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Fitur baru

### Perubahan alat di tengah percakapan (beta)

Anda dapat menambahkan atau menghapus alat di antara giliran percakapan sambil mempertahankan cache prompt, alih-alih mengirim ulang daftar alat tetap selama masa sesi. Perubahan alat di tengah percakapan berada dalam tahap beta: sertakan header beta `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda. Lihat [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) untuk penggunaannya.

### Mode fallback default

Parameter `fallbacks` mendukung mode `"default"` baru, yang menerapkan model fallback yang direkomendasikan Anthropic berdasarkan kategori penolakan alih-alih daftar model yang Anda kelola sendiri. Seluruh parameter `fallbacks` berada dalam tahap beta. Gunakan header beta `server-side-fallback-2026-07-01`, yang mendukung mode `"default"` maupun daftar model eksplisit (header `server-side-fallback-2026-06-01` yang lebih lama hanya menerima daftar eksplisit). Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

### Batas minimum cache prompt yang lebih rendah

Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, turun dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 kini dapat membuat entri cache tanpa perubahan kode. Lihat ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk batas minimum per model.

### Fast mode

[Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) tersedia untuk Claude Opus 5 hanya di Claude API; saat ini tidak tersedia di Amazon Bedrock, Claude Platform on AWS, Google Cloud, atau Microsoft Foundry. Fast mode untuk Claude Opus 5 dihargai $10 USD per juta token input dan $50 USD per juta token output. Lihat [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk akses, model yang didukung, dan harga.

## Perubahan perilaku

### Thinking aktif secara default

Di Claude Opus 4.8, permintaan berjalan tanpa thinking kecuali Anda menetapkan `thinking: {"type": "adaptive"}`. Di Claude Opus 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default: model memutuskan kapan dan seberapa banyak berpikir pada setiap giliran, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol untuk kedalaman thinking. Nilai wire tidak berubah; `thinking: {"type": "adaptive"}` tetap valid dan setara dengan default.

Ini adalah breaking change untuk kode yang berjalan tanpa thinking di Claude Opus 4.8. Respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, yang dikembalikan dengan field `thinking` kosong pada default `display: "omitted"`, sehingga kode yang membaca `content[0].text` atau memperlakukan blok konten pertama yang di-streaming sebagai teks harus memilih blok konten berdasarkan field `type`-nya. Loop penggunaan alat harus mengirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi bersama hasil alatnya; lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

Token thinking ditagih sebagai token output dan dihitung terhadap `max_tokens`, batas keras pada total output (thinking ditambah teks respons), jadi tinjau kembali `max_tokens` dan tetapkan ulang baseline biaya untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8.

API tetap menyediakan opsi untuk menonaktifkan thinking, dengan tunduk pada [pembatasan effort](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5#disabling-thinking-requires-effort-high-or-below) untuk menonaktifkannya.

### Effort menjadi lebih penting

Claude Opus 5 mengubah [effort](https://platform.claude.com/docs/id/build-with-claude/effort) tambahan menjadi hasil yang lebih baik secara lebih andal dibandingkan model Opus sebelumnya, sehingga tingkat effort yang Anda pilih memiliki bobot lebih besar. Seluruh jenjang tersedia: `low`, `medium`, `high`, `xhigh`, dan `max`, dengan `max` sebagai tingkat teratas untuk penalaran sedalam mungkin. Mulailah dari default, `high`, dan sesuaikan ke arah mana pun berdasarkan evaluasi Anda: turunkan jika kualitas tetap terjaga untuk menghemat token dan latensi, atau naikkan untuk pekerjaan yang paling menuntut. Saat berjalan pada effort `xhigh` atau `max`, tetapkan `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat.

Permintaan ini menaikkan effort hingga `max`:

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
  # max_tokens 64k dapat melampaui batas waktu non-streaming; lakukan streaming pada event.
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

Thinking [aktif secara default](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5#thinking-on-by-default) di Claude Opus 5, sehingga field `thinking` tidak diperlukan.

### Menonaktifkan thinking memerlukan effort `high` atau lebih rendah

Di Claude Opus 5, `thinking: {"type": "disabled"}` hanya diterima ketika tingkat effort adalah `high` atau lebih rendah. Menetapkan `thinking: {"type": "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Aturan ini diberlakukan pada setiap permintaan ke Claude Opus 5 dan model yang lebih baru. Ini adalah breaking change dari Claude Opus 4.8, di mana menonaktifkan thinking tidak bergantung pada tingkat effort. Jika permintaan Claude Opus 4.8 Anda menonaktifkan thinking pada effort `xhigh` atau `max`, pertahankan thinking nonaktif dan tetapkan effort ke `high` atau lebih rendah, atau pertahankan tingkat effort dan hapus field `thinking`.

Dengan thinking dinonaktifkan, Claude Opus 5 sesekali dapat menulis pemanggilan alat ke dalam output teksnya alih-alih mengeluarkan blok `tool_use`, atau menyertakan tag XML internal dalam respons yang terlihat. Jika memungkinkan, biarkan thinking tetap aktif dan kendalikan biaya token dengan tingkat effort yang lebih rendah; untuk integrasi yang harus tetap menonaktifkan thinking, lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi prompting.

### Perbedaan perilaku model

Di luar perubahan API ini, Claude Opus 5 berperilaku berbeda dari Claude Opus 4.8 dengan cara yang mungkin Anda perhatikan tanpa mengubah kode apa pun. Respons default yang ditujukan kepada pengguna dan hasil kerja tertulis menjadi lebih panjang. Dalam sesi agentik, model lebih sering menarasikan kemajuannya kepada pengguna. Dalam kerangka kerja multi-agen, model lebih mudah mendelegasikan ke subagen. Model juga memverifikasi pekerjaannya sendiri tanpa diminta, jadi hapus instruksi verifikasi yang terbawa dari model sebelumnya ("sertakan langkah verifikasi akhir," "gunakan subagen untuk memverifikasi"); instruksi tersebut menyebabkan verifikasi berlebihan di Claude Opus 5. Untuk pola prompting yang menyesuaikan masing-masing perilaku ini, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5).

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, Claude Opus 5 adalah peningkatan lompatan besar, bukan peningkatan bertahap, dan menghadirkan kecerdasan terdepan dengan setengah biaya [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5). Kemajuan terbesar ada pada:

* **Penalaran mendalam**, mempertahankan analisis multilangkah di sepanjang rantai masalah yang panjang.
* **Pengodean agentik dan tugas berjangka panjang**, tetap fokus pada tugas di sepanjang loop penggunaan alat yang panjang dan menyelesaikan fitur multi-file, refactor yang lebih besar, serta pekerjaan fitur end-to-end tanpa meninggalkan stub atau placeholder.
* **Penskalaan komputasi saat pengujian**, mengubah effort tambahan (hingga tingkat `max`) menjadi hasil yang lebih baik.
* **Efisiensi pada tingkat effort yang lebih rendah**, dengan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `low` dan `medium` menghasilkan kualitas yang kuat dengan sebagian kecil token dan latensi dari pengaturan yang lebih tinggi.
* **Tinjauan kode dan pencarian bug**, menemukan bug nyata dengan tingkat tinggi per pass dengan sedikit positif palsu, dan tetap akurat pada tingkat effort yang lebih rendah.
* **Visi**, memahami bagan, dokumen, dan diagram serta mereplikasi visual UI dan frontend, paling kuat ketika diberi alat untuk menganalisis, memotong, dan memverifikasi pekerjaannya secara iteratif.
* **Pekerjaan konteks panjang**, dengan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) sebagai default sekaligus maksimum, serta kepatuhan instruksi, pemanggilan alat, dan penalaran yang konsisten di seluruh jendela.
* **Tugas perkantoran dan dokumen**, menghasilkan dan mengedit spreadsheet multi-sheet yang kompleks dengan formula yang tidak sederhana, serta menghasilkan slide deck yang terstruktur dengan baik.
* **Koordinasi multi-agen**, menjalankan tim subagen dengan pola penulis-pemverifikasi yang efektif dan sedikit kasus agen yang menimpa pekerjaan satu sama lain.

Untuk pola prompting yang memaksimalkan kemampuan ini, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#capability-improvements).

## Harga

Claude Opus 5 dihargai $5 USD per juta token input dan $25 USD per juta token output, tidak berubah dari Claude Opus 4.8. Karena thinking aktif secara default dan token thinking ditagih sebagai token output, beban kerja yang berjalan tanpa thinking di Claude Opus 4.8 dapat menghasilkan lebih banyak token output per permintaan dengan tarif per token yang sama; lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga lengkap, termasuk tarif pemrosesan batch, caching prompt, dan fast mode.

## Ketersediaan

Claude Opus 5 tersedia di:

* **Claude API:** tersedia untuk semua pelanggan, sebagai `claude-opus-5`.
* **AWS:** tersedia melalui [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-opus-5`, dan melalui [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Di Amazon Bedrock, Claude Opus 5 juga dapat dijangkau melalui API `InvokeModel` pada `bedrock-runtime`, yang dilayani oleh infrastruktur yang sama; integrasi [Claude di Amazon Bedrock (legacy)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) tidak menyertakannya dalam tabel ID model berversi ARN.
* **Google Cloud:** tersedia melalui [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), sebagai `claude-opus-5`.
* **Microsoft Foundry:** tersedia melalui [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

Claude Opus 4.8 tetap tersedia di semua platform ini.

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

Kemudian tinjau dua breaking change di bawah [Perubahan perilaku](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5#behavior-changes): thinking aktif secara default (respons dapat dimulai dengan blok `thinking`, jadi pilih blok konten berdasarkan `type`), dan menonaktifkan thinking dengan effort `xhigh` atau `max` mengembalikan error 400. Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5) untuk instruksi langkah demi langkah dan daftar periksa lengkap.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Prompting Claude Opus 5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5">
    Perbedaan perilaku dan pola prompting khusus untuk Claude Opus 5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja thinking ketika aktif secara default, dan kapan dapat dinonaktifkan.
  </Card>

  <Card title="Anggaran tugas" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token sebagai acuan untuk mengatur laju pekerjaannya.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/about-claude/models/migration-guide">
    Panduan untuk bermigrasi ke model Claude terbaru dari versi Claude sebelumnya.
  </Card>

  <Card title="Fast mode" icon="bolt" href="https://platform.claude.com/docs/id/build-with-claude/fast-mode">
    Dapatkan token output per detik yang lebih tinggi dari model Claude Opus dengan harga premium.
  </Card>
</CardGroup>
