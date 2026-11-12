---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/multilingual-support
fetched_at: 2026-11-12T02:13:38.637181Z
sha256: 5a0b07c75c2c67ef8b036591486e6f60ca927648ce7b3a898d2e170dccec58b9
---

---
title: Dukungan multibahasa
url: https://platform.claude.com/docs/id/build-with-claude/multilingual-support
description: Claude unggul dalam tugas-tugas di berbagai bahasa, mempertahankan kinerja lintas bahasa yang kuat relatif terhadap bahasa Inggris.
featureMetadata:
  status: stable
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
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
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: stable
    Amazon Bedrock: stable
    Amazon Bedrock (bedrock-runtime): stable
    Claude Platform on AWS: stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

## Ikhtisar

Claude menunjukkan kemampuan multibahasa yang tangguh, dengan kinerja yang sangat kuat dalam tugas “zero-shot” (tanpa contoh) di berbagai bahasa.

Claude mampu bekerja dalam banyak bahasa di luar yang diuji dalam tabel berikut. Ujilah dengan bahasa apa pun yang relevan dengan kasus penggunaan spesifik Anda.

## Data kinerja

Tabel berikut menunjukkan skor zero-shot untuk model Claude pada [Global-MMLU](https://arxiv.org/abs/2412.03304), yang memperluas set pengujian [“Massive Multitask Language Understanding” (Pemahaman Bahasa Multitugas Masif), atau MMLU](https://en.wikipedia.org/wiki/MMLU) ke 42 bahasa. Setiap skor merupakan persentase dari skor bahasa Inggris model yang sama:

| Bahasa               | Claude Fable 5.2 | Claude Opus 5.5 | Claude Sonnet 5.5 | Claude Haiku 5.5 |
| -------------------- | ---------------- | --------------- | ----------------- | ---------------- |
| Inggris              | 100%             | 100%            | 100%              | 100%             |
| Spanyol              | 99,8%            | 99,3%           | 99,0%             | 98,1%            |
| Portugis (Brasil)    | 99,4%            | 99,2%           | 98,7%             | 98,1%            |
| Italia               | 99,5%            | 99,2%           | 98,4%             | 97,7%            |
| Prancis              | 99,6%            | 99,3%           | 98,7%             | 97,7%            |
| Indonesia            | 99,4%            | 99,1%           | 98,6%             | 97,1%            |
| Jerman               | 99,5%            | 99,1%           | 98,5%             | 97,4%            |
| Arab                 | 99,6%            | 99,3%           | 98,3%             | 96,6%            |
| Tionghoa (Sederhana) | 99,6%            | 99,3%           | 98,5%             | 97,7%            |
| Korea                | 99,6%            | 99,1%           | 98,3%             | 97,0%            |
| Jepang               | 99,5%            | 99,2%           | 98,4%             | 97,4%            |
| Hindi                | 99,4%            | 99,2%           | 98,5%             | 96,6%            |
| Bengali              | 99,2%            | 98,6%           | 97,2%             | 95,4%            |
| Swahili              | 99,2%            | 98,3%           | 96,9%             | 94,0%            |
| Yoruba               | 98,5%            | 96,3%           | 93,6%             | 87,0%            |

Semua skor menggunakan [“adaptive thinking” (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) pada [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) `max`. Skor tidak mencakup pertanyaan yang diblokir oleh “safety classifier” (pengklasifikasi keamanan) atau yang tidak terjawab. Untuk setiap skor dalam tabel, paling banyak 1,7 persen pertanyaan dikecualikan.

<Note>
  Gunakan tabel ini untuk membandingkan bahasa dalam satu model, bukan untuk memeringkat model. Perbedaan kurang dari sekitar 1 poin persentase masih berada dalam batas noise pengukuran.
</Note>

***

## Menetapkan bahasa respons

Claude menyimpulkan bahasa respons dari percakapan, tetapi untuk aplikasi produksi Anda sebaiknya menyatakan bahasa target secara eksplisit. Tempat paling andal untuk melakukannya adalah “system prompt” (prompt sistem), yang menjaga instruksi tetap stabil di setiap giliran percakapan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "system": "Always respond in French, regardless of the language the user writes in.",
      "messages": [
        {"role": "user", "content": "How do I reset my password?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --system "Always respond in French, regardless of the language the user writes in." \
    --message '{role: user, content: "How do I reset my password?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      system="Always respond in French, regardless of the language the user writes in.",
      messages=[{"role": "user", "content": "How do I reset my password?"}],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      System = "Always respond in French, regardless of the language the user writes in.",
      Messages = [new UserMessageParam { Content = "How do I reset my password?" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
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
      .model(Model.CLAUDE_OPUS_5_5)
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
      model: Model::CLAUDE_OPUS_5_5,
      system: 'Always respond in French, regardless of the language the user writes in.',
  );

  echo json_encode($message->content, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

1. **Berikan konteks bahasa yang jelas:** Meskipun Claude dapat mendeteksi bahasa target secara otomatis, menyatakan secara eksplisit bahasa input dan output yang Anda inginkan akan meningkatkan keandalan. Untuk kefasihan yang lebih baik, Anda dapat meminta Claude menggunakan “tuturan idiomatis seolah-olah ia adalah penutur asli.”
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
    Bangun chatbot dukungan pelanggan. Satu chatbot dapat melayani pelanggan dalam banyak bahasa.
  </Card>

  <Card title="Ikhtisar model" icon="table" href="https://platform.claude.com/docs/id/models/overview">
    Bandingkan tingkatan model untuk menyeimbangkan kualitas multibahasa dengan biaya dan latensi.
  </Card>

  <Card title="Tentukan kriteria keberhasilan dan bangun evaluasi" icon="scales" href="https://platform.claude.com/docs/id/test-and-evaluate/develop-tests">
    Terapkan metode evaluasi umum untuk mengukur kualitas output dalam setiap bahasa yang Anda dukung.
  </Card>
</CardGroup>

## Ketersediaan

Dukungan multibahasa tersedia di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Selalu aktif

| Status   | Platform cloud                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Selalu aktif

| Status   | Platform cloud                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| Tersedia | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |
