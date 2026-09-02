---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-latency
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 56a5deeee05b03dcab744f223dd5294937aae2212d18c506e3a4e46a3164bff9
---

---
title: Mengurangi latensi
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-latency
description: Kurangi latensi respons Claude dengan memilih model yang lebih cepat seperti Claude Haiku 4.5, memangkas token prompt dan output, serta melakukan streaming respons.
---

"Latency" (latensi) mengacu pada waktu yang diperlukan model untuk memproses prompt dan menghasilkan output. Latensi dapat dipengaruhi oleh berbagai faktor, seperti ukuran model, kompleksitas prompt, serta infrastruktur dasar yang mendukung model dan titik interaksi.

<Note>
  Selalu lebih baik untuk terlebih dahulu merancang prompt yang berfungsi dengan baik tanpa batasan model atau prompt, lalu mencoba strategi pengurangan latensi setelahnya. Mencoba mengurangi latensi terlalu dini dapat menghalangi Anda menemukan seperti apa kinerja terbaik itu.
</Note>

***

## Cara mengukur latensi

Saat membahas latensi, Anda mungkin menemukan beberapa istilah dan ukuran:

* **Latensi dasar (baseline latency):** Ini adalah waktu yang dibutuhkan model untuk memproses prompt dan menghasilkan respons, tanpa mempertimbangkan token input dan output per detik. Ini memberikan gambaran umum tentang kecepatan model.
* **"Time to first token" (waktu hingga token pertama), atau TTFT:** Metrik ini mengukur waktu yang diperlukan model untuk menghasilkan token pertama dari respons, sejak prompt dikirim. Ini sangat relevan ketika Anda menggunakan streaming (lebih lanjut tentang itu nanti) dan ingin memberikan pengalaman yang responsif kepada pengguna Anda.

Untuk pemahaman yang lebih mendalam tentang istilah-istilah ini, lihat [glosarium](https://platform.claude.com/docs/id/about-claude/glossary).

***

## Cara mengurangi latensi

### 1. Pilih model yang tepat

Salah satu cara paling langsung untuk mengurangi latensi adalah memilih model yang sesuai untuk kasus penggunaan Anda. Anthropic menawarkan [berbagai model](https://platform.claude.com/docs/id/models/overview) dengan kemampuan dan karakteristik kinerja yang berbeda. Pertimbangkan kebutuhan spesifik Anda dan pilih model yang paling sesuai dengan kebutuhan Anda dalam hal kecepatan dan kualitas output.

Untuk aplikasi yang mengutamakan kecepatan, **Claude Haiku 4.5** menawarkan waktu respons tercepat sambil tetap mempertahankan kecerdasan yang tinggi:

<CodeGroup>
  ```bash cURL
  # Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-haiku-4-5",
      "max_tokens": 100,
      "messages": [{"role": "user", "content": "Summarize this customer feedback in 2 sentences: [feedback text]"}]
    }'
  ```

  ```bash CLI
  # Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  ant messages create \
    --model claude-haiku-4-5 \
    --max-tokens 100 \
    --message '{"role": "user", "content": "Summarize this customer feedback in 2 sentences: [feedback text]"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  message = client.messages.create(
      model="claude-haiku-4-5",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Summarize this customer feedback in 2 sentences: [feedback text]",
          }
      ],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  const message = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Summarize this customer feedback in 2 sentences: [feedback text]"
      }
    ]
  });
  const textBlock = message.content.find((block) => block.type === "text");
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeHaiku4_5,
      MaxTokens = 100,
      Messages = [
          new()
          {
              Role = Role.User,
              Content = "Summarize this customer feedback in 2 sentences: [feedback text]"
          }
      ]
  };
  var message = await client.Messages.Create(parameters);
  message.Content[0].TryPickText(out var textBlock);
  Console.WriteLine(textBlock?.Text);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeHaiku4_5,
  	MaxTokens: 100,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize this customer feedback in 2 sentences: [feedback text]")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_HAIKU_4_5)
      .maxTokens(100L)
      .addUserMessage("Summarize this customer feedback in 2 sentences: [feedback text]")
      .build();
  Message message = client.messages().create(params);
  IO.println(message.content().get(0).text().map(TextBlock::text).orElse(""));
  ```

  ```php PHP
  $client = new Client();

  // Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  $message = $client->messages->create(
      maxTokens: 100,
      messages: [['role' => 'user', 'content' => 'Summarize this customer feedback in 2 sentences: [feedback text]']],
      model: 'claude-haiku-4-5',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Untuk aplikasi yang sensitif terhadap waktu, gunakan Claude Haiku 4.5
  message = client.messages.create(
    model: "claude-haiku-4-5",
    max_tokens: 100,
    messages: [{ role: "user", content: "Summarize this customer feedback in 2 sentences: [feedback text]" }]
  )
  puts message.content.first.text
  ```
</CodeGroup>

Untuk detail lebih lanjut tentang metrik model, lihat halaman [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

### 2. Optimalkan panjang prompt dan output

Minimalkan jumlah token baik dalam prompt input Anda maupun output yang diharapkan, sambil tetap mempertahankan kinerja yang tinggi. Semakin sedikit token yang harus diproses dan dihasilkan model, semakin cepat responsnya.

Berikut beberapa tips untuk membantu Anda mengoptimalkan prompt dan output Anda:

* **Jelas tetapi ringkas:** Usahakan menyampaikan maksud Anda dengan jelas dan ringkas dalam prompt. Hindari detail yang tidak perlu atau informasi yang berlebihan, sambil tetap mengingat bahwa [Claude tidak memiliki konteks](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#be-clear-and-direct) tentang kasus penggunaan Anda dan mungkin tidak membuat lompatan logika yang dimaksud jika instruksinya tidak jelas.
* **Minta respons yang lebih pendek:** Minta Claude secara langsung untuk bersikap ringkas. Jika Claude menghasilkan output dengan panjang yang tidak diinginkan, minta Claude untuk [mengurangi sifat cerewetnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#be-clear-and-direct).
  <Tip>
    Karena cara LLM menghitung 

    [token](https://platform.claude.com/docs/id/about-claude/glossary#tokens)

     alih-alih kata, meminta jumlah kata yang tepat atau batas jumlah kata bukanlah strategi yang seefektif meminta batas jumlah paragraf atau kalimat.
  </Tip>
* **Tetapkan batas output yang sesuai:** Gunakan parameter `max_tokens` untuk menetapkan batas keras pada panjang maksimum respons yang dihasilkan. Ini mencegah Claude menghasilkan output yang terlalu panjang.
  <Note>
    Ketika respons mencapai 

    `max_tokens`

     token, respons akan terpotong, mungkin di tengah kalimat atau di tengah kata, sehingga ini adalah teknik kasar yang mungkin memerlukan pasca-pemrosesan dan biasanya paling sesuai untuk respons pilihan ganda atau jawaban singkat di mana jawabannya muncul tepat di awal.
  </Note>
* **Bereksperimen dengan temperature:** [Parameter](https://platform.claude.com/docs/id/api/messages/create) `temperature` mengontrol keacakan output. Nilai yang lebih rendah (misalnya, 0,2) terkadang dapat menghasilkan respons yang lebih terfokus dan lebih pendek, sedangkan nilai yang lebih tinggi (misalnya, 0,8) mungkin menghasilkan output yang lebih beragam tetapi berpotensi lebih panjang.

Menemukan keseimbangan yang tepat antara kejelasan prompt, kualitas output, dan jumlah token mungkin memerlukan beberapa eksperimen.

### 3. Lakukan streaming respons

Streaming adalah fitur yang memungkinkan model mulai mengirimkan responsnya sebelum output lengkap selesai. Ini dapat secara signifikan meningkatkan responsivitas yang dirasakan dari aplikasi Anda, karena pengguna dapat melihat output model secara real time.

Dengan streaming diaktifkan, Anda dapat memproses output model saat output tersebut tiba, memperbarui antarmuka pengguna Anda atau melakukan tugas lain secara paralel.

Kunjungi [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming) untuk mempelajari cara mengimplementasikan streaming untuk kasus penggunaan Anda.

***

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengurangi halusinasi" icon="shield" href="https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations">
    Minimalkan halusinasi dalam output Claude dengan mengizinkan ketidakpastian, mendasarkan respons pada kutipan langsung, dan memverifikasi klaim dengan sitasi.
  </Card>

  <Card title="Streaming pesan" icon="bolt" href="https://platform.claude.com/docs/id/build-with-claude/streaming">
    Lakukan streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.
  </Card>
</CardGroup>
