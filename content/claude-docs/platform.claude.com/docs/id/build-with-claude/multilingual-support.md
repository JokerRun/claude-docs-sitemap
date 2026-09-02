---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/multilingual-support
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 0035d593abf98886c72357632c697f9d5859c8462da1bde20e9de25d1cc309de
---

---
title: Dukungan multibahasa
url: https://platform.claude.com/docs/id/build-with-claude/multilingual-support
description: Claude unggul dalam tugas-tugas di berbagai bahasa, mempertahankan kinerja lintas bahasa yang kuat relatif terhadap bahasa Inggris.
---

## Ikhtisar

Claude menunjukkan kemampuan multibahasa yang tangguh, dengan kinerja yang sangat kuat terutama dalam tugas "zero-shot" (tanpa contoh) di berbagai bahasa. Model ini mempertahankan kinerja relatif yang konsisten baik pada bahasa yang digunakan secara luas maupun bahasa dengan sumber daya yang lebih terbatas, menjadikannya pilihan yang andal untuk aplikasi multibahasa.

Claude mampu bekerja dalam banyak bahasa di luar yang diuji dalam tabel berikut. Ujilah dengan bahasa apa pun yang relevan dengan kasus penggunaan spesifik Anda.

## Data kinerja

Tabel berikut menunjukkan skor evaluasi "zero-shot chain-of-thought" (rantai pemikiran tanpa contoh) untuk model Claude di berbagai bahasa, dinyatakan sebagai persentase relatif terhadap kinerja bahasa Inggris (100%):

| Bahasa                                 | Claude Sonnet 4.51 | Claude Haiku 4.51 |
| -------------------------------------- | ------------------ | ----------------- |
| Inggris (acuan dasar, ditetapkan 100%) | 100%               | 100%              |
| Spanyol                                | 98,2%              | 96,4%             |
| Portugis (Brasil)                      | 97,8%              | 96,1%             |
| Italia                                 | 97,9%              | 96,0%             |
| Prancis                                | 97,5%              | 95,7%             |
| Indonesia                              | 97,3%              | 94,2%             |
| Jerman                                 | 97,0%              | 94,3%             |
| Arab                                   | 97,2%              | 92,5%             |
| Tionghoa (Sederhana)                   | 96,9%              | 94,2%             |
| Korea                                  | 96,7%              | 93,3%             |
| Jepang                                 | 96,8%              | 93,5%             |
| Hindi                                  | 96,7%              | 92,4%             |
| Bengali                                | 95,4%              | 90,4%             |
| Swahili                                | 91,1%              | 78,3%             |
| Yoruba                                 | 79,7%              | 52,7%             |

1 Dengan [extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) (pemikiran diperpanjang).

<Note>
  Metrik ini didasarkan pada set pengujian bahasa Inggris [MMLU (Massive Multitask Language Understanding)](https://en.wikipedia.org/wiki/MMLU) yang diterjemahkan ke dalam 14 bahasa tambahan oleh penerjemah manusia profesional, seperti yang didokumentasikan dalam [repositori simple-evals milik OpenAI](https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md). Penggunaan penerjemah manusia untuk evaluasi ini memastikan terjemahan berkualitas tinggi, yang sangat penting terutama untuk bahasa dengan sumber daya digital yang lebih sedikit.
</Note>

***

## Menetapkan bahasa respons

Claude menyimpulkan bahasa respons dari percakapan, tetapi untuk aplikasi produksi Anda sebaiknya menyatakan bahasa target secara eksplisit. Tempat paling andal untuk melakukannya adalah "system prompt" (prompt sistem), yang menjaga instruksi tetap stabil di setiap giliran percakapan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "system": "Always respond in French, regardless of the language the user writes in.",
      "messages": [
        {"role": "user", "content": "How do I reset my password?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --system "Always respond in French, regardless of the language the user writes in." \
    --message '{role: user, content: "How do I reset my password?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      system="Always respond in French, regardless of the language the user writes in.",
      messages=[{"role": "user", "content": "How do I reset my password?"}],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    system: "Always respond in French, regardless of the language the user writes in.",
    messages: [{ role: "user", content: "How do I reset my password?" }]
  });

  console.log(message.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      System = "Always respond in French, regardless of the language the user writes in.",
      Messages =
      [
          new() { Role = Role.User, Content = "How do I reset my password?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	System: []anthropic.TextBlockParam{
  		{Text: "Always respond in French, regardless of the language the user writes in."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I reset my password?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024)
      .system("Always respond in French, regardless of the language the user writes in.")
      .addUserMessage("How do I reset my password?")
      .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'How do I reset my password?']
      ],
      model: 'claude-opus-5',
      system: 'Always respond in French, regardless of the language the user writes in.',
  );

  echo json_encode($message->content, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    system: "Always respond in French, regardless of the language the user writes in.",
    messages: [
      { role: "user", content: "How do I reset my password?" }
    ]
  )

  puts message.content
  ```
</CodeGroup>

Jika aplikasi Anda memungkinkan pengguna memilih bahasa saat runtime, sisipkan pilihan tersebut ke dalam prompt sistem alih-alih mengandalkan Claude untuk menyimpulkannya dari pesan pengguna. Untuk menerjemahkan antara dua bahasa tertentu, sebutkan keduanya: `Translate the user's message from German to Korean. Respond with only the translation.`

***

## Praktik terbaik

Saat bekerja dengan konten multibahasa:

1. **Berikan konteks bahasa yang jelas:** Meskipun Claude dapat mendeteksi bahasa target secara otomatis, menyatakan bahasa input dan output yang diinginkan secara eksplisit akan meningkatkan keandalan. Untuk kefasihan yang lebih baik, Anda dapat meminta Claude untuk menggunakan "tuturan idiomatis seolah-olah ia adalah penutur asli."
2. **Gunakan aksara asli:** Kirimkan teks dalam aksara aslinya, bukan transliterasi, untuk hasil yang optimal.
3. **Pertimbangkan konteks budaya:** Komunikasi yang efektif sering kali memerlukan kesadaran budaya dan regional di luar penerjemahan semata.

Ikuti juga panduan umum dalam [Ikhtisar rekayasa prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview) untuk lebih meningkatkan kualitas output.

***

## Pertimbangan dukungan bahasa

* Claude memproses input dan menghasilkan output dalam sebagian besar bahasa dunia yang menggunakan karakter Unicode standar.
* Kinerja bervariasi menurut bahasa, dengan kemampuan yang sangat kuat terutama pada bahasa yang digunakan secara luas.
* Bahkan dalam bahasa dengan sumber daya digital yang lebih sedikit, Claude tetap mempertahankan kemampuan yang bermakna.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar rekayasa prompt" icon="edit" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/overview">
    Terapkan teknik prompting umum untuk meningkatkan kualitas output multibahasa.
  </Card>

  <Card title="Agen dukungan pelanggan" icon="headset" href="https://platform.claude.com/docs/id/about-claude/use-case-guides/customer-support-chat">
    Bangun chatbot dukungan yang dilokalkan menggunakan prompt sistem yang dibatasi bahasanya.
  </Card>

  <Card title="Ikhtisar model" icon="table" href="https://platform.claude.com/docs/id/models/overview">
    Bandingkan tingkatan model untuk menyeimbangkan kualitas multibahasa dengan biaya dan latensi.
  </Card>

  <Card title="Tentukan kriteria keberhasilan dan bangun evaluasi" icon="scales" href="https://platform.claude.com/docs/id/test-and-evaluate/develop-tests">
    Evaluasi kualitas terjemahan dan lokalisasi sebelum Anda merilis.
  </Card>
</CardGroup>
