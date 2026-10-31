---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 809cf96dd95b1069595587d3548012a511d30e57be976036ac01a67cabc981ab
---

---
title: Effort
url: https://platform.claude.com/docs/id/build-with-claude/effort
description: Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara ketelitian respons dan efisiensi token.
featureMetadata:
  status: stable
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
  supportedPlatforms:
    Claude API: stable
    Claude Platform on AWS: stable
    Amazon Bedrock: stable
    Amazon Bedrock (InvokeModel): stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

**Dukungan API**: Penggunaan berbeda menurut produk.

* **Messages API**: Selalu aktif. Atur `output_config.effort` pada permintaan. Tanpa nilai, level default model yang berlaku.
* **Managed Agents**: Selalu aktif. Atur `effort` pada objek model agen, atau dalam override model sesi. Tanpa nilai, Managed Agents mengisi default model.

Parameter effort memungkinkan Anda mengendalikan berapa banyak token yang dihabiskan Claude saat merespons permintaan. Anda dapat menyeimbangkan antara ketelitian respons dan efisiensi token dengan satu model. Parameter effort tingkat atas tersedia di semua model yang didukung tanpa memerlukan beta header. [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) masih dalam tahap beta.

<Tip>
  Untuk mempelajari bagaimana effort berinteraksi dengan pemikiran dan kontrol mana yang sebaiknya digunakan, lihat [Pemikiran dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-effort). Jika pemikiran adaptif tersedia, effort adalah cara yang direkomendasikan untuk mengendalikan kedalaman pemikiran.
</Tip>

## Mengatur tingkat effort

Atur `output_config.effort` pada permintaan. Contoh berikut menjalankan satu permintaan dengan effort `medium`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
    --model claude-opus-5-5 \
    --max-tokens 4096 \
    --output-config '{effort: medium}' \
    --message '{role: user, content: "Analyze the trade-offs between microservices and monolithic architectures"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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

  const textBlock = response.content.find((block) => block.type === "text");
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [
          new UserMessageParam
          {
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
  	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
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
      model: 'claude-opus-5-5',
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
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

Sebagian besar model Claude secara default menggunakan effort tinggi, menghabiskan token sebanyak yang diperlukan untuk hasil yang sangat baik; Claude Opus 5.5 dan Claude Haiku 5.5 secara default menggunakan medium. Anda dapat menaikkan tingkat effort ke `max` untuk kemampuan tertinggi mutlak, atau menurunkannya agar lebih hemat dalam penggunaan token, mengoptimalkan kecepatan dan biaya sambil menerima sedikit penurunan kemampuan.

<Tip>
  Mengatur `effort` ke nilai default model (`"medium"` pada Claude Opus 5.5 dan Claude Haiku 5.5, `"high"` pada model lain) menghasilkan perilaku yang persis sama dengan menghilangkan parameter `effort` sepenuhnya.
</Tip>

Parameter effort memengaruhi **semua token** dalam respons, termasuk:

* Respons teks dan penjelasan
* Pemanggilan alat dan argumen fungsi
* Pemikiran (saat aktif)

Karena effort berlaku untuk setiap token output, effort berfungsi dengan atau tanpa pemikiran. Effort yang lebih rendah juga berarti pemanggilan alat yang lebih sedikit dan lebih ringkas.

### Tingkat effort

| Tingkat  | Deskripsi                                                                                                                                                                                                                                                                                                                                | Kasus penggunaan umum                                                                                |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `max`    | Kemampuan maksimum mutlak tanpa batasan pada pengeluaran token. Tersedia di Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, dan Claude Haiku 5.5. | Tugas yang memerlukan penalaran sedalam mungkin dan analisis paling menyeluruh                       |
| `xhigh`  | Kemampuan yang diperluas untuk pekerjaan jangka panjang. Tersedia di Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5.5, Claude Sonnet 5, dan Claude Haiku 5.5.                                                                   | Tugas agentik dan coding yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan |
| `high`   | Menghabiskan token sebanyak yang dibutuhkan tugas untuk hasil yang sangat baik. Default pada setiap model yang mendukung effort kecuali Claude Opus 5.5 dan Claude Haiku 5.5.                                                                                                                                                            | Penalaran kompleks, masalah coding yang sulit, tugas agentik                                         |
| `medium` | Pendekatan seimbang dengan penghematan token moderat. Default pada Claude Opus 5.5 dan Claude Haiku 5.5.                                                                                                                                                                                                                                 | Tugas agentik yang memerlukan keseimbangan kecepatan, biaya, dan performa                            |
| `low`    | Paling efisien. Penghematan token signifikan dengan sedikit penurunan kemampuan.                                                                                                                                                                                                                                                         | Tugas yang lebih sederhana yang membutuhkan kecepatan terbaik dan biaya terendah, seperti subagen    |

Tidak setiap model yang mendukung `max` mendukung `xhigh`.

<Note>
  Effort adalah sinyal perilaku, bukan anggaran token yang ketat. Pada tingkat effort yang lebih rendah, Claude tetap berpikir pada masalah yang cukup sulit, tetapi berpikir lebih sedikit dibandingkan pada tingkat effort yang lebih tinggi untuk masalah yang sama.
</Note>

Rekomendasi per model berikut menggantikan tabel ini jika terdapat perbedaan.

## Tingkat effort yang direkomendasikan

**[Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview) & [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview)** — *For demanding reasoning and long-horizon agentic work*

Claude Fable 5.1 mendukung kelima tingkat effort. **Mulailah dengan `high`, yang merupakan default.** Naikkan ke `xhigh` atau `max` untuk pekerjaan agentik dan coding yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin atau yang sensitif terhadap latensi setelah evaluasi Anda menunjukkan kualitas tetap terjaga. Pada `high` ke atas, atur `max_tokens` yang besar. Ini adalah batas keras pada total output (pemikiran ditambah teks respons).

Claude Fable 5.1 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt.

See also: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels)

**[Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)** — *For long-running agentic coding and knowledge work*

Claude Opus 5.5 mendukung kelima tingkat effort, dan `medium` adalah default-nya (Claude Opus 5 dan model Opus sebelumnya secara default menggunakan `high`, sehingga permintaan yang menghilangkan `effort` berjalan satu tingkat lebih rendah dibandingkan pada Claude Opus 5). Pemikiran adaptif selalu aktif dan tidak dapat dimatikan, sehingga effort adalah kontrol utama untuk seberapa banyak model bernalar dan berapa biaya suatu permintaan. Jalankan sweep effort pada evaluasi Anda sendiri alih-alih membawa pengaturan dari model sebelumnya, dan atur `max_tokens` yang besar pada tingkat yang lebih tinggi: ini adalah batas keras pada total output (pemikiran ditambah teks respons). Permintaan yang mengatur `thinking: {"type": "disabled"}` mengembalikan error 400 pada setiap tingkat effort. Claude Opus 5.5 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt.

See also: [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

**[Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview)** — *The best combination of speed and intelligence*

Claude Sonnet 5.5 mendukung kelima tingkat effort, dan `high` adalah default pada Claude API. Tingkatnya dikalibrasi ulang, sehingga suatu tingkat tidak menghasilkan jumlah pemikiran yang sama dengan tingkat yang sama pada Claude Sonnet 5. Jalankan sweep effort baru pada evaluasi Anda alih-alih membawa pengaturan yang Anda gunakan pada Claude Sonnet 5. Mulailah dengan `high` kecuali beban kerja Anda bersifat agentik atau sensitif terhadap latensi. Untuk coding agentik dan penggunaan alat multilangkah, mulailah dengan `medium` untuk tugas yang terdefinisi dengan baik dan beralih ke `high` untuk tugas yang lebih sulit atau lebih panjang. Untuk chat dan pekerjaan lain yang sensitif terhadap latensi, mulailah dengan `medium` atau `low`. Gunakan `xhigh` atau `max` hanya jika evaluasi Anda menunjukkan peningkatan kualitas. Atur `max_tokens` dengan ruang untuk pemikiran dan balasan. Pemikiran dihitung terhadap `max_tokens` bahkan ketika konten pemikiran tidak dikembalikan. Untuk coding agentik, atur `max_tokens` ke 128.000, nilai maksimum model, dan lakukan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) pada respons.

Untuk mematikan pemikiran di awal, kirim `thinking: {"type": "between_tools"}` alih-alih `"disabled"`. Ini adalah pengaturan pemikiran terendah pada Claude Sonnet 5.5, dan berfungsi pada effort `low`, `medium`, dan `high`. Pada `xhigh` atau `max`, permintaan dengan pengaturan ini mengembalikan error 400, jadi gunakan pemikiran adaptif pada tingkat tersebut: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`. Lihat [Menjalankan tanpa pemikiran di awal](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking).

Claude Sonnet 5.5 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt. Dengan `between_tools`, effort tidak dapat diubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari tingkat yang berlaku mengembalikan error 400. Untuk memvariasikan effort di setiap giliran, gunakan pemikiran adaptif.

See also: [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#calibrate-effort)

**[Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)** — *For high-volume, latency-sensitive tasks such as classification, extraction, and routing*

Claude Haiku 5.5 mendukung kelima tingkat effort, dan `medium` adalah default-nya. Effort adalah kontrol utama untuk seberapa banyak model berpikir, dan dengan itu kualitas, latensi, dan biaya. **Mulailah dengan `medium`** untuk sebagian besar pekerjaan, termasuk coding agentik. Gunakan `low`, tingkat termurah dan tercepat, untuk chat, tugas alat singkat, dan permintaan sederhana bervolume tinggi. Dalam prompt agen yang panjang, model lebih mungkin melewatkan pencarian, berhenti lebih awal, atau melewatkan pemeriksaan pada `low`. Gunakan `high` untuk pekerjaan berbasis pengetahuan, tugas agen yang lebih panjang, dan kepatuhan instruksi yang ketat. Gunakan `xhigh` atau `max` hanya jika evaluasi Anda menunjukkan peningkatan kualitas, dan bandingkan dengan Claude Sonnet 5.5 dalam hal performa, biaya, dan kecepatan. Pemikiran aktif secara default dan dihitung terhadap `max_tokens`, jadi sisakan ruang untuknya.

Untuk mendapatkan pemikiran yang lebih sedikit, turunkan tingkat effort. Anda juga dapat mengirim `thinking: {"type": "disabled"}` pada effort `high` atau di bawahnya. Pada `xhigh` atau `max`, ini mengembalikan error 400, jadi gunakan pemikiran adaptif di sana: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`.

Pada Claude API dan Claude Models on Google Cloud (Google managed), Claude Haiku 5.5 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt. Dengan `thinking: {"type": "disabled"}`, effort tidak dapat diubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari tingkat yang berlaku mengembalikan error 400. Untuk memvariasikan effort di setiap giliran, gunakan pemikiran adaptif.

See also: [Prompting Claude Haiku 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#use-effort-to-control-thinking)

**[Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview) & [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview)**

Effort adalah kontrol utama untuk menyeimbangkan kecerdasan, latensi, dan biaya pada Claude Fable 5. **Mulailah dengan `high`, yang merupakan default, untuk sebagian besar tugas**, gunakan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan, dan turunkan ke `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 tetap berkinerja baik dan sering melampaui performa `xhigh` pada model sebelumnya. Pada `high` dan `xhigh`, atur `max_tokens` yang besar. Ini adalah batas keras pada total output (pemikiran ditambah teks respons). Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

Kurangi effort jika suatu tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan lebih interaktif.

See also: [Prompting Claude Fable 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5)

**[Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview)**

Claude Opus 5 mendukung kelima tingkat effort. **Mulailah dengan `high`, yang merupakan default**, dan sesuaikan berdasarkan evaluasi Anda: naikkan ke `xhigh` untuk pekerjaan coding dan agentik yang menuntut, atau ke `max` ketika suatu tugas membenarkan pengeluaran token tanpa batasan. Gunakan `low` dan `medium` secara leluasa sebagai kontrol utama Anda untuk biaya token dan waktu respons di mana pun evaluasi Anda menunjukkan kualitas tetap terjaga. Jika Anda membawa pengaturan effort dari model sebelumnya, jalankan sweep effort baru pada evaluasi Anda alih-alih menggunakannya kembali.

Effort mengendalikan volume pemikiran, bukan panjang respons yang terlihat: pada Claude Opus 5, mengubah effort tidak secara andal memperpendek respons, jadi [gunakan prompt untuk mengatur panjang](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) sebagai gantinya.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda. Nilai yang Anda berikan menggantikan default.

Pada Claude Opus 5, pemikiran tidak dapat dinonaktifkan pada effort `xhigh` atau `max`: permintaan yang mengatur `thinking: {"type": "disabled"}` pada tingkat tersebut mengembalikan error 400. Lihat [Effort dengan pemikiran](https://platform.claude.com/docs/id/build-with-claude/effort#effort-with-thinking).

Saat menjalankan Claude Opus 5 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

Claude Opus 5 juga mendukung [mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) dengan `output_config` per pesan, yang mempertahankan cache prompt. Effort per pesan tidak tersedia untuk Claude Opus 5 di Amazon Bedrock.

See also: [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5)

**[Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview)**

Panduan untuk Claude Opus 4.7 juga berlaku untuk Claude Opus 4.8. **Mulailah dengan `xhigh` untuk kasus penggunaan coding dan agentik**, gunakan `high` untuk sebagian besar beban kerja lain yang sensitif terhadap kecerdasan, dan turunkan ke `medium` atau `low` hanya ketika Anda telah mengukur bahwa tingkat yang lebih rendah mempertahankan kualitas pada evaluasi Anda.

Default API adalah `high`. Atur `effort` secara eksplisit untuk menggunakan tingkat yang berbeda. Nilai yang Anda berikan menggantikan default.

Saat menjalankan Claude Opus 4.8 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

See also: [Prompting Claude Opus 4.8](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)

**[Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview)**

**Mulailah dengan `xhigh` untuk kasus penggunaan coding dan agentik**, dan gunakan `high` sebagai minimum untuk sebagian besar beban kerja yang sensitif terhadap kecerdasan. Turunkan ke `medium` untuk beban kerja yang sensitif terhadap biaya, atau naikkan ke `max` hanya ketika evaluasi Anda menunjukkan ruang peningkatan yang terukur pada `xhigh`.

Default API adalah `high`. Untuk menggunakan `xhigh`, atur `effort` secara eksplisit. Nilai yang Anda berikan menggantikan default.

* **Effort rendah:** Efisien, tetapi paling baik untuk tugas singkat dengan cakupan terbatas. Pasangkan `low` dengan daftar periksa eksplisit jika tugas Anda memiliki beberapa bagian.
* **Effort sedang:** Pengaturan untuk alur kerja rata-rata di mana Anda menginginkan hasil yang baik sambil mengurangi biaya.
* **Effort tinggi:** Kasus penggunaan lanjutan yang tetap membutuhkan keseimbangan antara kecerdasan dan konsumsi token. Ini sering kali merupakan keseimbangan terbaik antara kualitas dan efisiensi token.
* **Effort xhigh:** Titik awal yang direkomendasikan untuk pekerjaan coding dan agentik, serta untuk tugas eksploratif seperti pemanggilan alat berulang, pencarian web terperinci, dan pencarian basis pengetahuan. Harapkan penggunaan token yang jauh lebih tinggi daripada `high`.
* **Effort max:** Simpan untuk masalah di garis depan. Pada sebagian besar beban kerja, `max` menambah biaya signifikan untuk peningkatan kualitas yang relatif kecil, dan pada beberapa tugas structured-output atau yang kurang sensitif terhadap kecerdasan, hal ini dapat menyebabkan overthinking.

Claude Opus 4.7 juga mematuhi tingkat effort dengan lebih ketat dibandingkan Claude Opus 4.6, terutama pada `low` dan `medium`. Pada tingkat effort yang lebih rendah, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks dengan Claude Opus 4.7, naikkan effort alih-alih mengakalinya dengan prompt. Jika Anda harus menjaga effort tetap rendah karena latensi, tambahkan panduan yang terarah seperti “This task involves multistep reasoning. Think carefully before responding.”

Saat menjalankan Claude Opus 4.7 pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alat. Memulai dari 64k token dan menyesuaikan dari sana adalah default yang wajar.

See also: [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)

**[Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview)**

Claude Sonnet 5 secara default menggunakan effort `high` pada Claude API dan Claude Code.

* **Effort tinggi (default):** Cocok untuk penalaran kompleks, coding, dan tugas agentik di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort xhigh:** Untuk tugas coding dan agentik yang paling sulit.
* **Effort sedang:** Penurunan dari default untuk menghemat biaya. Sebanding dengan Claude Sonnet 4.6 pada effort tinggi.
* **Effort rendah:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana penyelesaian yang lebih cepat diprioritaskan.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi mutlak tanpa batasan pada pengeluaran token.

See also: [Prompting Claude Sonnet 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5#calibrating-effort-and-thinking-depth)

**[Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview)**

Sonnet 4.6 secara default menggunakan effort `high`. Atur effort secara eksplisit saat menggunakan Sonnet 4.6 untuk menghindari latensi yang tidak terduga:

* **Effort sedang (default yang direkomendasikan):** Keseimbangan terbaik antara kecepatan, biaya, dan performa untuk sebagian besar aplikasi. Cocok untuk coding agentik, alur kerja yang banyak menggunakan alat, dan pembuatan kode.
* **Effort rendah:** Untuk beban kerja bervolume tinggi atau sensitif terhadap latensi. Cocok untuk chat dan kasus penggunaan non-coding di mana penyelesaian yang lebih cepat diprioritaskan.
* **Effort tinggi:** Untuk penalaran kompleks dan tugas di mana kualitas lebih penting daripada kecepatan atau biaya.
* **Effort max:** Untuk tugas yang memerlukan kemampuan tertinggi mutlak tanpa batasan pada pengeluaran token.

See also: [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)

## Effort dengan penggunaan alat

Saat menggunakan alat, parameter effort memengaruhi baik penjelasan seputar pemanggilan alat maupun pemanggilan alat itu sendiri. Tingkat effort yang lebih rendah cenderung:

* Menggabungkan beberapa operasi ke dalam lebih sedikit pemanggilan alat
* Melakukan lebih sedikit pemanggilan alat
* Langsung melanjutkan ke tindakan tanpa pembukaan
* Menggunakan pesan konfirmasi yang ringkas setelah selesai

Tingkat effort yang lebih tinggi mungkin:

* Melakukan lebih banyak pemanggilan alat
* Menjelaskan rencana sebelum mengambil tindakan
* Memberikan ringkasan perubahan yang terperinci
* Menyertakan komentar kode yang lebih komprehensif

## Effort dengan pemikiran

Parameter `thinking` mengontrol apakah Claude berpikir dalam [blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) sebelum menjawab; parameter `effort` mengontrol seberapa banyak upaya yang Claude curahkan untuk keseluruhan respons, yang dalam mode adaptif mencakup seberapa sering dan seberapa dalam Claude berpikir. Jangan berikan `adaptive` sebagai nilai `effort`: `adaptive` adalah mode berpikir, bukan tingkat upaya.

Pada tingkat effort yang lebih tinggi, Claude lebih mudah berpikir dan dengan durasi yang lebih panjang. Dalam loop penggunaan alat, permintaan lanjutan yang hanya memproses hasil alat tetap dapat melewatkan pemikiran pada tingkat apa pun. Pada tingkat yang lebih rendah, Claude dapat melewatkan pemikiran sepenuhnya untuk masalah yang lebih sederhana. Lihat [Pemikiran dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-effort) untuk panduan lengkap tentang bagaimana kedua kontrol ini bekerja bersama.

Pada Claude Opus 4.5, satu-satunya model khusus pemikiran diperpanjang yang mendukung effort, effort bekerja bersama [`budget_tokens`](https://platform.claude.com/docs/id/build-with-claude/extended-thinking): atur tingkat effort untuk tugas Anda, lalu atur anggaran token pemikiran berdasarkan seberapa dalam penalaran yang dibutuhkan tugas tersebut.

Untuk ketersediaan pemikiran per model, lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models). Effort berfungsi dengan atau tanpa pemikiran. Lihat [Cara kerja effort](https://platform.claude.com/docs/id/build-with-claude/effort#how-effort-works).

## Mengubah effort di tengah percakapan

Anda dapat menjalankan giliran selanjutnya dari suatu percakapan pada tingkat effort yang berbeda dengan dua cara. Pada Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, dan Claude Haiku 5.5, gunakan perubahan effort per pesan, yang mempertahankan cache prompt. Pada model lain, atur nilai tingkat atas yang baru pada permintaan berikutnya, yang memulai ulang cache.

### Effort per pesan (beta)

Effort per pesan masih dalam tahap beta. Pada Claude API dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), fitur ini tersedia di Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, dan Claude Haiku 5.5. Pada [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), fitur ini tersedia di Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5.5. Fitur ini memerlukan [beta header](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-output-config-2026-07-01`. Dengan [InvokeModel API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) Amazon Bedrock, fitur ini tersedia di Claude Fable 5.1 dan Claude Opus 5.5, dan Anda mengirim nilai tersebut dalam array `anthropic_beta` di body permintaan sebagai gantinya.

Tanpa nilai beta, `output_config` per pesan mengembalikan error 400: `messages.N.output_config: Extra inputs are not permitted`, di mana `N` adalah indeks pesan `system` dalam `messages`. Dengan nilai beta, model tanpa effort per pesan, termasuk Claude Fable 5, mengembalikan error 400: `output_config.effort requires a model that supports per-turn effort; this model does not`. Pada Amazon Bedrock, model-model tersebut dan Claude Opus 5 mengembalikan error `Extra inputs are not permitted` sebagai gantinya. Pada Claude Sonnet 5.5 dengan `thinking: {"type": "between_tools"}` dan pada Claude Haiku 5.5 dengan `thinking: {"type": "disabled"}`, effort tidak dapat diubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari tingkat yang berlaku mengembalikan error 400. Untuk memvariasikan effort di setiap giliran, gunakan pemikiran adaptif.

Tambahkan pesan `role: "system"` dengan `content` kosong dan tingkat baru di `output_config.effort`. Jika ditempatkan langsung setelah giliran `user` dengan input baru, pesan ini mengatur tingkat untuk balasan Claude pada giliran tersebut. Jika ditempatkan di tempat lain, seperti di antara giliran `assistant` dan giliran `user` berikutnya seperti pada contoh berikut, pesan ini berlaku mulai dari giliran `user` berikutnya dengan input baru. Giliran `user` yang hanya berisi blok `tool_result` tidak dihitung sebagai input baru, sehingga perubahan yang ditempatkan setelahnya dalam loop penggunaan alat menunggu giliran `user` berikutnya dengan input baru. Tingkat baru kemudian berlaku hingga pesan berikutnya mengubahnya. Semua yang ada sebelum pesan tersebut tidak berubah, sehingga prefix yang di-cache tetap cocok.

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
  ant beta:messages create \
    --beta mid-conversation-output-config-2026-07-01 <<'YAML'
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
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeFable5_1,
      MaxTokens = 4096,
      OutputConfig = new() { Effort = Effort.High },
      Messages =
      [
          new BetaUserMessageParam { Content = "Plan a migration from SQLite to PostgreSQL in three short steps." },
          new BetaAssistantMessageParam { Content = "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          new BetaSystemMessageParam
          {
              Content = new([]),
              OutputConfig = new() { Effort = BetaSystemMessageOutputConfigEffort.Low },
          },
          new BetaUserMessageParam { Content = "Summarize the plan in one sentence." },
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
  	Model:     anthropic.ModelClaudeFable5_1,
  	MaxTokens: 4096,
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortHigh,
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Plan a migration from SQLite to PostgreSQL in three short steps.")),
  		{OfAssistant: &anthropic.BetaAssistantMessageParam{
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
  		}},
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
  import com.anthropic.models.beta.messages.BetaOutputConfig;
  import com.anthropic.models.beta.messages.BetaSystemMessageOutputConfig;
  import com.anthropic.models.beta.messages.BetaSystemMessageParam;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_FABLE_5_1)
          .maxTokens(4096L)
          .addBeta(AnthropicBeta.MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01)
          .outputConfig(BetaOutputConfig.builder()
              .effort(BetaOutputConfig.Effort.HIGH)
              .build())
          .addUserMessage("Plan a migration from SQLite to PostgreSQL in three short steps.")
          .addAssistantMessage("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          .addMessage(BetaSystemMessageParam.builder()
              .contentOfBlocks(List.of())
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
    model: Anthropic::Model::CLAUDE_FABLE_5_1,
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

Utamakan bentuk ini dibandingkan mengubah nilai tingkat atas di antara permintaan. Perubahan tingkat atas memulai ulang cache dan, pada Claude Fable 5.1, juga mengarahkan model dengan kurang andal: balasan sebelumnya ditulis pada tingkat sebelumnya, dan model cenderung tetap konsisten dengannya.

### Effort tingkat atas pada permintaan berikutnya

`output_config.effort` tingkat atas berlaku untuk seluruh permintaan. Untuk menjalankan bagian selanjutnya dari suatu percakapan pada tingkat yang berbeda, atur nilai baru pada permintaan berikutnya. Karena effort tingkat atas membentuk prompt yang di-render, mengubahnya di antara permintaan tidak mempertahankan prefix yang di-cache dari giliran sebelumnya. Jika Anda mengandalkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) di sepanjang sesi yang panjang dan model Anda tidak mendukung effort per pesan, pilih tingkat effort di awal dan pertahankan agar tetap konstan.

## Praktik terbaik

1. **Atur effort secara eksplisit:** API secara default menggunakan `high` (`medium` pada Claude Opus 5.5 dan Claude Haiku 5.5), tetapi titik awal yang tepat bergantung pada model dan beban kerja Anda.
2. **Gunakan low untuk tugas yang sensitif terhadap kecepatan atau sederhana:** Ketika latensi penting atau tugas bersifat langsung, effort rendah dapat secara signifikan mengurangi waktu respons dan biaya.
3. **Uji kasus penggunaan Anda:** Dampak tingkat effort bervariasi menurut jenis tugas. Evaluasi performa pada kasus penggunaan spesifik Anda sebelum melakukan deployment.
4. **Pertimbangkan effort dinamis:** Sesuaikan effort berdasarkan kompleksitas tugas. Kueri sederhana mungkin memerlukan effort rendah, sedangkan coding agentik dan penalaran kompleks mendapat manfaat dari effort tinggi. Lihat poin berikutnya sebelum memvariasikannya dalam satu percakapan.
5. **Pertahankan effort tingkat atas tetap konstan dalam percakapan yang di-cache:** Mengubah nilai effort tingkat atas di antara permintaan membatalkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), jadi variasikan di seluruh beban kerja alih-alih dalam percakapan yang mengandalkan cache hit. Pada model yang mendukungnya, gunakan [perubahan effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) sebagai gantinya, yang mempertahankan cache. Lihat [Pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

## Langkah selanjutnya

<CardGroup>
  <Card title="Anggaran tugas" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan Claude anggaran token bersifat anjuran untuk seluruh loop agentik guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.
  </Card>

  <Card title="Mengarahkan thinking" icon="compass" href="https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost">
    Pahami pemikiran adaptif, di mana Claude menentukan kapan dan seberapa banyak berpikir, dan arahkan dengan effort dan prompting.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Pahami cara kerja pemikiran, kapan Claude berpikir secara default, dan bagaimana pemikiran berinteraksi dengan effort.
  </Card>
</CardGroup>

## Ketersediaan

Effort tersedia di model tertentu dan layak untuk retensi data nol dan kesiapan HIPAA.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Selalu aktif
* Penggunaan: Atur `output_config.effort` pada permintaan. Tanpa nilai, level default model yang berlaku.

| Status   | Platform cloud                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview), [Claude Opus 4.5](https://platform.claude.com/docs/id/models/opus-4-5/overview) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Selalu aktif
* Penggunaan: Atur `effort` pada objek model agen, atau dalam override model sesi. Tanpa nilai, Managed Agents mengisi default model.

| Status   | Platform cloud                                                                                                     | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview), [Claude Opus 4.5](https://platform.claude.com/docs/id/models/opus-4-5/overview) |

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                 | HIPAA |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements)) | Layak |

Endpoint yang berlaku:

* `/v1/messages` dengan `effort`
