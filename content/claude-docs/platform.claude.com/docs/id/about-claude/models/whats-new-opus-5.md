---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-opus-5
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: a675ab8e131bf032b200daf9dc0f8c7d117671cd2d149cdd978b60bdfda79784
---

# Apa yang baru di Claude Opus 5

Ikhtisar fitur baru dan perubahan perilaku di Claude Opus 5.

---

Claude Opus 5 adalah peningkatan besar dibandingkan Claude Opus 4.8, dengan peningkatan terbesar pada penalaran mendalam, tugas agentik dan jangka panjang, serta penskalaan komputasi saat pengujian (test-time compute scaling). Halaman ini merangkum semua hal baru di Claude Opus 5, termasuk thinking yang aktif secara default, perubahan alat di tengah percakapan, dan perubahan yang bersifat breaking terkait kapan thinking dapat dinonaktifkan.

## Model baru

| Model         | ID model API    | Deskripsi                                                       |
| ------------- | --------------- | --------------------------------------------------------------- |
| Claude Opus 5 | `claude-opus-5` | Untuk pengkodean agentik yang kompleks dan pekerjaan enterprise |

Claude Opus 5 memiliki [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) (1M token adalah nilai default sekaligus maksimum; tidak ada varian konteks yang lebih kecil), maksimum 128k token output, dan [thinking](/docs/id/build-with-claude/thinking) yang aktif secara default.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Fitur baru

### Perubahan alat di tengah percakapan (beta)

Anda dapat menambah atau menghapus alat di antara giliran percakapan sambil mempertahankan cache prompt, alih-alih mengirim ulang daftar alat yang tetap selama sesi berlangsung. Perubahan alat di tengah percakapan masih dalam tahap beta: sertakan header beta `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda. Lihat [Perubahan alat di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) untuk cara penggunaannya.

### Mode fallback default

Parameter `fallbacks` mendukung mode baru `"default"`, yang menerapkan model fallback yang direkomendasikan Anthropic berdasarkan kategori penolakan, alih-alih daftar model yang Anda kelola sendiri. Seluruh parameter `fallbacks` masih dalam tahap beta. Gunakan header beta `server-side-fallback-2026-07-01`, yang mendukung mode `"default"` maupun daftar model eksplisit (header `server-side-fallback-2026-06-01` yang lebih lama hanya menerima daftar eksplisit). Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback).

### Minimum cache prompt yang lebih rendah

Panjang prompt minimum yang dapat di-cache pada Claude Opus 5 adalah 512 token, turun dari 1.024 token pada Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache pada Claude Opus 4.8 kini dapat membuat entri cache tanpa perubahan kode. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk nilai minimum per model.

### Mode cepat

[Mode cepat](/docs/id/build-with-claude/fast-mode) (pratinjau riset) tersedia untuk Claude Opus 5 hanya di Claude API; saat ini tidak tersedia di Amazon Bedrock, Google Cloud, atau Microsoft Foundry. Mode cepat untuk Claude Opus 5 dihargai $10 per juta token input dan $50 per juta token output. Lihat [Mode cepat](/docs/id/build-with-claude/fast-mode) untuk akses, model yang didukung, dan harga.

## Perubahan perilaku

### Thinking aktif secara default

Pada Claude Opus 4.8, permintaan berjalan tanpa thinking kecuali Anda menyetel `thinking: {"type": "adaptive"}`. Pada Claude Opus 5, permintaan yang sama berjalan dengan [thinking](/docs/id/build-with-claude/thinking) aktif: model memutuskan kapan dan seberapa banyak berpikir pada setiap giliran, dan [parameter effort](/docs/id/build-with-claude/effort) menjadi kontrol untuk kedalaman berpikir. Nilai pada wire tidak berubah; `thinking: {"type": "adaptive"}` tetap valid dan setara dengan default.

Karena `max_tokens` adalah batas keras untuk total output (thinking ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa thinking pada Claude Opus 4.8.

API tetap menyediakan opsi untuk menonaktifkan thinking, dengan tunduk pada pembatasan effort di bawah ini.

### Effort lebih berpengaruh

Claude Opus 5 mengubah [effort](/docs/id/build-with-claude/effort) tambahan menjadi hasil yang lebih baik secara lebih andal dibandingkan model Opus sebelumnya, sehingga tingkat effort yang Anda pilih memiliki bobot yang lebih besar. Seluruh tingkatan tersedia: `low`, `medium`, `high`, `xhigh`, dan `max`, dengan `max` sebagai tingkat tertinggi untuk penalaran sedalam mungkin. Mulailah dari default, `high`, dan sesuaikan ke arah mana pun berdasarkan evaluasi Anda: turunkan jika kualitas tetap terjaga untuk menghemat token dan latensi, atau naikkan untuk pekerjaan yang paling menuntut. Saat berjalan pada effort `xhigh` atau `max`, setel `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat.

Permintaan ini menaikkan effort sampai ke `max`:

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
  # max_tokens 64k dapat melebihi batas waktu non-streaming; lakukan streaming pada event-nya.
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

Thinking [aktif secara default](#thinking-on-by-default) pada Claude Opus 5, sehingga field `thinking` tidak diperlukan.

### Menonaktifkan thinking memerlukan effort `high` atau lebih rendah

Pada Claude Opus 5, `thinking: {"type": "disabled"}` hanya diterima ketika tingkat effort adalah `high` atau lebih rendah. Menyetel `thinking: {"type": "disabled"}` dengan effort `xhigh` atau `max` akan mengembalikan error 400. Ini adalah perilaku yang tersedia secara umum pada Claude Opus 5 dan seterusnya, diberlakukan pada setiap permintaan, dan merupakan perubahan yang bersifat breaking dari Claude Opus 4.8, di mana menonaktifkan thinking tidak bergantung pada tingkat effort. Jika saat ini Anda menonaktifkan thinking pada tingkat effort tinggi, pertahankan thinking dalam keadaan nonaktif dan setel effort ke `high` atau lebih rendah, atau pertahankan tingkat effort dan hapus field `thinking`.

Dengan thinking dinonaktifkan, Claude Opus 5 terkadang dapat menuliskan pemanggilan alat ke dalam output teksnya alih-alih mengeluarkan blok `tool_use`, atau menyertakan tag XML internal dalam respons yang terlihat. Jika memungkinkan, biarkan thinking tetap aktif dan kendalikan biaya token dengan tingkat effort yang lebih rendah; untuk integrasi yang harus menonaktifkan thinking, lihat [Menjalankan dengan thinking dinonaktifkan](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi melalui prompting.

### Perbedaan perilaku model

Di luar perubahan API di atas, Claude Opus 5 berperilaku berbeda dari Claude Opus 4.8 dalam hal-hal yang mungkin Anda perhatikan tanpa mengubah kode apa pun. Respons default yang ditujukan kepada pengguna dan hasil tulisan menjadi lebih panjang. Dalam sesi agentik, model lebih sering menarasikan kemajuannya kepada pengguna. Dalam kerangka kerja multi-agen, model lebih mudah mendelegasikan ke subagen. Model juga memverifikasi pekerjaannya sendiri tanpa diminta, jadi hapus instruksi verifikasi yang dibawa dari model sebelumnya ("sertakan langkah verifikasi akhir," "gunakan subagen untuk memverifikasi"); instruksi tersebut menyebabkan verifikasi berlebihan pada Claude Opus 5. Untuk pola prompting yang menyetel masing-masing perilaku ini, lihat [Prompting Claude Opus 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5).

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, Claude Opus 5 merupakan peningkatan besar, bukan peningkatan inkremental, dan menghadirkan kecerdasan terdepan dengan setengah biaya Claude Fable 5. Peningkatan terbesar ada pada:

* **Penalaran mendalam**, mempertahankan analisis multilangkah di sepanjang rantai masalah yang panjang.
* **Pengkodean agentik dan tugas jangka panjang**, tetap fokus pada tugas di sepanjang loop penggunaan alat yang panjang dan menyelesaikan fitur multi-file, refactor yang lebih besar, dan pekerjaan fitur end-to-end tanpa meninggalkan stub atau placeholder.
* **Penskalaan komputasi saat pengujian**, mengubah effort tambahan (hingga tingkat `max`) menjadi hasil yang lebih baik.
* **Efisiensi pada tingkat effort yang lebih rendah**, dengan [effort](/docs/id/build-with-claude/effort) `low` dan `medium` menghasilkan kualitas yang kuat dengan hanya sebagian kecil dari token dan latensi pengaturan yang lebih tinggi.
* **Tinjauan kode dan pencarian bug**, menemukan bug nyata dengan tingkat keberhasilan tinggi per lintasan dengan sedikit positif palsu, dan tetap akurat pada tingkat effort yang lebih rendah.
* **Visi**, memahami grafik, dokumen, dan diagram serta mereplikasi visual UI dan frontend, paling kuat ketika diberi alat untuk menganalisis, memotong, dan memverifikasi pekerjaannya secara iteratif.
* **Pekerjaan konteks panjang**, dengan [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) sebagai default sekaligus maksimum, serta kepatuhan instruksi, pemanggilan alat, dan penalaran yang konsisten di sepanjang jendela tersebut.
* **Tugas perkantoran dan dokumen**, menghasilkan dan mengedit spreadsheet multi-sheet yang kompleks dengan formula yang tidak sepele, serta menghasilkan deck slide yang terstruktur dengan baik.
* **Koordinasi multi-agen**, menjalankan tim subagen dengan pola penulis-verifikator yang efektif dan sedikit kasus agen yang saling menimpa pekerjaan satu sama lain.

Untuk pola prompting yang memaksimalkan kemampuan-kemampuan ini, lihat [Prompting Claude Opus 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#capability-improvements).

## Harga

Claude Opus 5 dihargai $5 per juta token input dan $25 per juta token output, tidak berubah dari Claude Opus 4.8.

Lihat [Harga](/docs/id/about-claude/pricing) untuk harga lengkap, termasuk pemrosesan batch, caching prompt, dan tarif mode cepat.

## Ketersediaan

Claude Opus 5 tersedia di:

* **Claude API:** tersedia untuk semua pelanggan, sebagai `claude-opus-5`.
* **AWS:** tersedia melalui [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-opus-5`. Claude Opus 5 juga dapat dijangkau melalui API `InvokeModel` pada `bedrock-runtime`, yang dilayani oleh infrastruktur yang sama; integrasi [Claude on Amazon Bedrock (legacy)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) tidak menyertakannya dalam tabel ID model berversi ARN.
* **Google Cloud:** tersedia melalui [Claude on Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), sebagai `claude-opus-5`.
* **Microsoft Foundry:** tersedia melalui [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

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

Kemudian tinjau dua [perubahan perilaku](#behavior-changes): thinking aktif secara default, dan menonaktifkan thinking dengan effort `xhigh` atau `max` mengembalikan error 400. Lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5) untuk instruksi langkah demi langkah.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="/docs/id/about-claude/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Prompting Claude Opus 5" icon="terminal" href="/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5">
    Perbedaan perilaku dan pola prompting yang spesifik untuk Claude Opus 5.
  </Card>

  <Card title="Effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Thinking" icon="brain" href="/docs/id/build-with-claude/thinking">
    Cara kerja thinking ketika aktif secara default, dan kapan dapat dinonaktifkan.
  </Card>

  <Card title="Anggaran tugas" icon="database" href="/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token sebagai acuan untuk mengatur ritme pekerjaannya.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="/docs/id/about-claude/models/migration-guide">
    Panduan untuk bermigrasi ke model Claude terbaru dari versi Claude sebelumnya.
  </Card>

  <Card title="Mode cepat" icon="bolt" href="/docs/id/build-with-claude/fast-mode">
    Dapatkan token output per detik yang lebih tinggi dari model Claude Opus dengan harga premium.
  </Card>
</CardGroup>
