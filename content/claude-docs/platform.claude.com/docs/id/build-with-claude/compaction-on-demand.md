---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: 2433132266a7a00609b749705da36a50ec0394a5e2d3333a67e6b9b19d27850e
---

---
title: Compaction sesuai permintaan
url: https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand
description: Minta Claude meringkas percakapan pada saat yang dipilih aplikasi Anda, lalu lanjutkan dari ringkasan tersebut.
featureMetadata:
  status: beta
  betaHeader: compact-2026-09-04
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-5
    - claude-sonnet-4-6
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Amazon Bedrock: not available
    Google Cloud: beta
    Microsoft Foundry: beta
---

Dengan "on-demand compaction" (pemadatan sesuai permintaan), aplikasi Anda yang menentukan kapan percakapan diringkas: Anda mengirim satu permintaan dengan parameter `compaction`, dan Claude mengembalikan ringkasan sebagai pengganti balasan.

## Cara kerja compaction sesuai permintaan

Permintaan compaction terpisah dari giliran percakapan Anda. Anda mengirim percakapan apa adanya dengan parameter `compaction`, dan respons berisi satu blok `compaction`. Blok tersebut memuat ringkasan sebagai teks yang dapat Anda baca, serta sebuah tanda tangan (signature). Kirimkan blok itu dalam permintaan berikutnya persis seperti saat diterima.

Sejak saat itu, blok tersebut menggantikan pesan-pesan yang diringkasnya. Blok ditempatkan pertama di `messages`, pesan-pesan yang diringkas dihapus, dan giliran Anda berikutnya menyusul setelahnya. Claude melihat ringkasan di tempat pesan-pesan tersebut sebelumnya berada.

![On-demand compaction (pemadatan sesuai permintaan): permintaan yang membawa empat pesan dan parameter compaction mengembalikan satu compaction block (blok compaction) tanpa balasan; pada permintaan berikutnya blok tersebut ditempatkan pertama di messages menggantikan keempat pesan itu, diikuti oleh giliran user berikutnya](https://platform.claude.com/docs/images/compaction-on-demand-swap.svg)

## Meminta ringkasan

Kirim header beta `compact-2026-09-04` pada permintaan yang meminta ringkasan dan pada setiap permintaan berikutnya yang membawa blok bertanda tangan. Untuk memeriksa apakah suatu model mendukung compaction sesuai permintaan, panggil [Models API](https://platform.claude.com/docs/id/api/beta/models/list) dengan header beta dan baca `capabilities.compaction` dari setiap model. Anda tidak dapat menggabungkan `compaction` dengan `context_management` dalam satu permintaan.

Kirim percakapan apa adanya dengan `"compaction": {"type": "summarize"}`. API meringkas setiap pesan dalam permintaan satu kali, tidak menghasilkan balasan setelahnya, dan hanya mengembalikan blok tersebut dengan `stop_reason` `"compaction"`. Kirim prompt `system` dan `tools` yang sama dengan yang Anda gunakan untuk sisa percakapan. Peringkas membaca keduanya, dan jika Anda mempertahankan giliran setelah blok pada model dengan ["preserved thinking" (pemikiran yang dipertahankan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking), thinking dalam giliran tersebut tetap valid hanya jika `system` dan `tools` cocok. Percakapan dalam contoh ini tidak memiliki prompt `system` maupun alat, sehingga permintaan tidak mengirim keduanya:

<CodeGroup>
  ```bash cURL
  # max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-09-04" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 4096,
      "messages": [
        {"role": "user", "content": "I am building a recipe app. Help me name the main entities in the data model."},
        {"role": "assistant", "content": "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe."},
        {"role": "user", "content": "Good. Now suggest field names for Recipe."}
      ],
      "compaction": {"type": "summarize"}
    }'
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:messages create --beta compact-2026-09-04 < request.yaml
    ```

    <File filename="request.yaml">
      ```yaml
      model: claude-opus-5-5
      # max_tokens caps the whole call, including any thinking, so allow several thousand tokens.
      max_tokens: 4096
      messages:
        - role: user
          content: I am building a recipe app. Help me name the main entities in the data model.
        - role: assistant
          content: Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.
        - role: user
          content: Good. Now suggest field names for Recipe.
      compaction:
        type: summarize
      ```
    </File>
  </MultiFileExample>

  ```python Python
  from anthropic.types.beta import BetaMessageParam

  client = anthropic.Anthropic()

  history: list[BetaMessageParam] = [
      {
          "role": "user",
          "content": "I am building a recipe app. Help me name the main entities in the data model.",
      },
      {
          "role": "assistant",
          "content": "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.",
      },
      {"role": "user", "content": "Good. Now suggest field names for Recipe."},
  ]

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      # max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
      max_tokens=4096,
      betas=["compact-2026-09-04"],
      messages=history,
      compaction={"type": "summarize"},
  )
  print(f"Stop reason: {response.stop_reason}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const history: Anthropic.Beta.Messages.BetaMessageParam[] = [
    {
      role: "user",
      content: "I am building a recipe app. Help me name the main entities in the data model."
    },
    {
      role: "assistant",
      content:
        "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe."
    },
    { role: "user", content: "Good. Now suggest field names for Recipe." }
  ];

  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    // max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
    max_tokens: 4096,
    betas: ["compact-2026-09-04"],
    messages: history,
    compaction: { type: "summarize" }
  });
  console.log(`Stop reason: ${response.stop_reason}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  List<BetaMessageParam> history =
  [
      new()
      {
          Role = Role.User,
          Content = "I am building a recipe app. Help me name the main entities in the data model.",
      },
      new()
      {
          Role = Role.Assistant,
          Content = "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.",
      },
      new() { Role = Role.User, Content = "Good. Now suggest field names for Recipe." },
  ];

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      // max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
      MaxTokens = 4096,
      Betas = [AnthropicBeta.Compact2026_09_04],
      Messages = history,
      Compaction = new BetaCompactionConfig(), // type defaults to "summarize"
  });

  Console.WriteLine($"Stop reason: {response.StopReason?.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  history := []anthropic.BetaMessageParam{
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("I am building a recipe app. Help me name the main entities in the data model.")),
  	{
  		Role:    anthropic.BetaMessageParamRoleAssistant,
  		Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.")},
  	},
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Good. Now suggest field names for Recipe.")),
  }

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model: anthropic.ModelClaudeOpus5_5,
  	// max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
  	MaxTokens: 4096,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
  	Messages:  history,
  	Compaction: anthropic.BetaCompactionConfigUnionParam{
  		OfSummarize: &anthropic.BetaSummarizeCompactionParam{},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println("Stop reason:", response.StopReason)
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaCompactionConfig;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          // max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
          .maxTokens(4096)
          .addBeta(AnthropicBeta.COMPACT_2026_09_04)
          .addUserMessage("I am building a recipe app. Help me name the main entities in the data model.")
          .addAssistantMessage("Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.")
          .addUserMessage("Good. Now suggest field names for Recipe.")
          .compaction(BetaCompactionConfig.builder().build()) // type defaults to "summarize"
          .build();

      var response = client.beta().messages().create(params);
      response.stopReason().ifPresent(reason -> IO.println("Stop reason: " + reason));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaCompactionConfig;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Beta\Messages\BetaMessageParam\Role;

  $client = new Client();

  $history = [
      BetaMessageParam::with(
          role: Role::USER,
          content: 'I am building a recipe app. Help me name the main entities in the data model.',
      ),
      BetaMessageParam::with(
          role: Role::ASSISTANT,
          content: 'Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe.',
      ),
      BetaMessageParam::with(role: Role::USER, content: 'Good. Now suggest field names for Recipe.'),
  ];

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      // max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
      maxTokens: 4096,
      betas: [AnthropicBeta::COMPACT_2026_09_04],
      messages: $history,
      compaction: BetaCompactionConfig::with(), // type defaults to 'summarize'
  );

  echo "Stop reason: {$response->stopReason}", PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  history = [
    {
      role: "user",
      content: "I am building a recipe app. Help me name the main entities in the data model."
    },
    {
      role: "assistant",
      content: "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe."
    },
    { role: "user", content: "Good. Now suggest field names for Recipe." }
  ]

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    # max_tokens membatasi seluruh panggilan, termasuk proses thinking, jadi sediakan beberapa ribu token.
    max_tokens: 4096,
    betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
    messages: history,
    compaction: { type: "summarize" }
  )
  puts "Stop reason: #{response.stop_reason}"
  ```
</CodeGroup>

```json Response
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-5-5",
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation: the user is designing the data model for a recipe app. The entities agreed so far are Recipe, Ingredient, Step, and RecipeIngredient, which holds the quantity and unit. The user then asked for field names for Recipe.",
      "signature": "EuYBCkQY..."
    }
  ],
  "stop_reason": "compaction",
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "iterations": [{ "type": "compaction", "input_tokens": 144, "output_tokens": 276 }]
  }
}
```

Panggilan peringkasan menggunakan model, `system`, `tools`, pengaturan thinking, dan `max_tokens` dari permintaan. Peringkas membaca definisi alat tetapi tidak pernah menjalankan alat, dan respons tidak membawa thinking. `max_tokens` membatasi seluruh panggilan, termasuk thinking apa pun yang dilakukan model sebelum menulis ringkasan, jadi sediakan beberapa ribu token. [Menghitung penggunaan compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#understanding-usage) menunjukkan bagaimana panggilan tersebut ditagih.

Jika giliran `assistant` terakhir diakhiri dengan panggilan alat yang belum memiliki hasil, API menolak permintaan tersebut. Kirim hasil alat dari giliran itu terlebih dahulu. Selain itu, jangan sertakan `stop_sequences`, `output_config.format` untuk structured output, maupun `tool_choice` bertipe `any` atau `tool`. Parameter-parameter tersebut tidak berpengaruh apa pun pada panggilan peringkasan, dan API menolaknya. Percakapan tetap harus muat dalam "context window" (jendela konteks) model, jadi lakukan compaction sebelum percakapan melampauinya, bukan sesudahnya.

Saat Anda melakukan streaming respons, blok tiba secara utuh. Anda mendapatkan satu event `content_block_start` yang membawa blok lengkap, lalu `content_block_stop`, tanpa event `content_block_delta`. Event `ping` dapat tiba sebelum atau di antara keduanya.

## Melanjutkan dari ringkasan

Dalam riwayat Anda, ganti pesan-pesan yang Anda kirim dengan pesan assistant yang dikembalikan. Pertahankan blok `compaction` persis seperti yang dikembalikan API, termasuk `signature`-nya. Giliran apa pun yang diambil setelah Anda mengirim permintaan compaction menyusul blok tersebut tanpa perubahan, dan hal inilah yang menjadi dasar [Compaction di latar belakang](https://platform.claude.com/docs/id/build-with-claude/compaction-background). Kirim blok tersebut di urutan pertama pada setiap permintaan berikutnya, dengan header beta:

```json
{
  "model": "claude-opus-5-5",
  "max_tokens": 2048,
  "messages": [
    {
      "role": "assistant",
      "content": [
        {
          "type": "compaction",
          "content": "Summary of the conversation: the user is designing the data model for a recipe app. The entities agreed so far are Recipe, Ingredient, Step, and RecipeIngredient, which holds the quantity and unit. The user then asked for field names for Recipe.",
          "signature": "EuYBCkQY..."
        }
      ]
    },
    {
      "role": "assistant",
      "content": "For Recipe, use title, description, servings, prep_minutes, and cook_minutes. Add created_at and updated_at timestamps."
    },
    { "role": "user", "content": "Now do the same for Ingredient." }
  ]
}
```

Contoh ini melanjutkan sampel permintaan, yang berakhir pada giliran `user`; diagram menunjukkan kasus yang lebih sederhana, di mana tidak ada giliran yang diambil selama ringkasan ditulis. Di sini pesan `assistant` kedua adalah balasan untuk giliran `user` terakhir yang diringkas. Pesan itu tiba saat ringkasan sedang ditulis, sehingga tidak termasuk dalam pesan-pesan yang diringkas. Dua pesan `assistant` berturut-turut tidak menjadi masalah di sini, karena blok tetap berada di urutan pertama.

API menempatkan ringkasan di posisi blok dan meneruskan setiap pesan berikutnya ke Claude tanpa perubahan. Ikuti aturan berikut:

* Tempatkan blok di urutan pertama dalam `messages`, baik sebagai pesan `assistant` tersendiri maupun sebagai blok konten pertama dari pesan pertama, entah itu pesan `user` atau `assistant`.
* Hapus pesan-pesan yang diringkas. Jika ada yang masih tersisa di depan blok, permintaan mengembalikan error 400 (`compaction_block_misplaced`).
* Kirim tepat satu blok `compaction` per permintaan, pada setiap permintaan berikutnya.

<Warning>
  Dua kesalahan dalam penukaran ini tidak memunculkan error. Jika pesan yang diringkas masih tersisa setelah blok, API mengirimkannya lagi ke Claude. Jika permintaan berikutnya tidak menyertakan blok, Claude tidak mendapatkan ringkasan.
</Warning>

Compaction ambang batas bekerja sebaliknya: bloknya mengikuti pesan-pesan yang diringkasnya, dan API menghapus pesan-pesan tersebut untuk Anda. Lihat [Mengirimkan kembali blok compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#passing-compaction-blocks-back).

Di Python, gunakan `client.beta.messages`, seperti yang dilakukan sampel di halaman ini. Jika Anda memanggil `client.messages` dan menyerialisasi blok sendiri, gunakan `to_dict()` atau `model_dump(exclude_none=True)`: `model_dump()` biasa menambahkan `citations: null` dan `text: null` ke blok, dan API menolaknya.

Jika Anda mempertahankan giliran setelah blok dan mengirim kembali blok thinking-nya, syarat-syarat yang menjaga thinking tersebut tetap valid dijelaskan di [Compaction dan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks).

### Melakukan compaction lagi

Untuk melakukan compaction pada percakapan yang sudah diawali dengan sebuah blok, kirim `compaction` lagi. Blok baru meringkas ringkasan lama beserta semua yang ada setelahnya. Sejak saat itu, kirim hanya blok terbaru.

## Compaction dalam loop

Setelah setiap giliran, loop menjumlahkan token input dan output dari respons terakhir, karena permintaan berikutnya juga mengirim balasan tersebut. Ketika total itu melewati batas dan masih ada giliran lain yang akan datang, loop mengirim permintaan compaction dengan model dan prompt `system` yang sama, memeriksa `stop_reason`, mengganti riwayatnya dengan pesan yang dikembalikan, dan mencetak giliran yang didahului oleh compaction tersebut. Batas sampel sebesar 2.500 token sengaja dibuat rendah, agar percakapan yang singkat pun mengalami compaction. Atur batas Anda mendekati anggaran input Anda yang sebenarnya.

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.types.beta import BetaMessageParam

  client = anthropic.Anthropic()

  # Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini sengaja rendah agar percakapan singkat pun dipadatkan.
  COMPACT_AT_TOKENS = 2500
  SYSTEM = "You help design a recipe app's data model. Keep answers short."

  QUESTIONS = [
      "What are the main entities in the data model?",
      "Which fields should Recipe have?",
      "Which fields should Ingredient have?",
      "Which fields should RecipeIngredient have?",
      "Which fields should Step have?",
      "Which indexes should these tables have?",
      "Which fields should be required?",
      "Which fields should have default values?",
  ]

  history: list[BetaMessageParam] = []
  for turn, question in enumerate(QUESTIONS, start=1):
      history.append({"role": "user", "content": question})
      response = client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=8192,
          system=SYSTEM,
          betas=["compact-2026-09-04"],
          messages=history,
      )
      history.append({"role": "assistant", "content": response.content})

      # Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
      conversation_tokens = response.usage.input_tokens + response.usage.output_tokens
      if conversation_tokens > COMPACT_AT_TOKENS and turn < len(QUESTIONS):
          summary = client.beta.messages.create(
              model="claude-opus-5-5",
              max_tokens=4096,
              system=SYSTEM,
              betas=["compact-2026-09-04"],
              messages=history,
              compaction={"type": "summarize"},
          )
          if summary.stop_reason == "compaction":
              history = [{"role": "assistant", "content": summary.content}]
              print(f"Compacted before turn {turn + 1}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  const compactAtTokens = 2500;
  const systemPrompt = "You help design a recipe app's data model. Keep answers short.";

  const questions = [
    "What are the main entities in the data model?",
    "Which fields should Recipe have?",
    "Which fields should Ingredient have?",
    "Which fields should RecipeIngredient have?",
    "Which fields should Step have?",
    "Which indexes should these tables have?",
    "Which fields should be required?",
    "Which fields should have default values?"
  ];

  let history: Anthropic.Beta.Messages.BetaMessageParam[] = [];
  for (const [index, question] of questions.entries()) {
    const turn = index + 1;
    history.push({ role: "user", content: question });
    const response = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 8192,
      system: systemPrompt,
      betas: ["compact-2026-09-04"],
      messages: history
    });
    history.push({ role: "assistant", content: response.content });

    // Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
    const conversationTokens = response.usage.input_tokens + response.usage.output_tokens;
    if (conversationTokens > compactAtTokens && turn < questions.length) {
      const summary = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 4096,
        system: systemPrompt,
        betas: ["compact-2026-09-04"],
        messages: history,
        compaction: { type: "summarize" }
      });
      if (summary.stop_reason === "compaction") {
        history = [{ role: "assistant", content: summary.content }];
        console.log(`Compacted before turn ${turn + 1}`);
      }
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  const int CompactAtTokens = 2500;
  const string SystemPrompt = "You help design a recipe app's data model. Keep answers short.";

  string[] questions =
  [
      "What are the main entities in the data model?",
      "Which fields should Recipe have?",
      "Which fields should Ingredient have?",
      "Which fields should RecipeIngredient have?",
      "Which fields should Step have?",
      "Which indexes should these tables have?",
      "Which fields should be required?",
      "Which fields should have default values?",
  ];

  List<BetaMessageParam> history = [];
  foreach (var (index, question) in questions.Index())
  {
      var turn = index + 1;
      history.Add(new() { Role = Role.User, Content = question });
      var response = await client.Beta.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 8192,
          System = SystemPrompt,
          Betas = [AnthropicBeta.Compact2026_09_04],
          Messages = history,
      });
      history.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      });

      // Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung balasan tersebut.
      var conversationTokens = response.Usage.InputTokens + response.Usage.OutputTokens;
      if (conversationTokens > CompactAtTokens && turn < questions.Length)
      {
          var summary = await client.Beta.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus5_5,
              MaxTokens = 4096,
              System = SystemPrompt,
              Betas = [AnthropicBeta.Compact2026_09_04],
              Messages = history,
              Compaction = new BetaCompactionConfig(), // type defaults to "summarize"
          });
          if (summary.StopReason == BetaStopReason.Compaction)
          {
              history =
              [
                  new()
                  {
                      Role = Role.Assistant,
                      Content = summary.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
                  },
              ];
              Console.WriteLine($"Compacted before turn {turn + 1}");
          }
      }
  }
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  const compactAtTokens = 2500
  system := []anthropic.BetaTextBlockParam{{Text: "You help design a recipe app's data model. Keep answers short."}}

  questions := []string{
  	"What are the main entities in the data model?",
  	"Which fields should Recipe have?",
  	"Which fields should Ingredient have?",
  	"Which fields should RecipeIngredient have?",
  	"Which fields should Step have?",
  	"Which indexes should these tables have?",
  	"Which fields should be required?",
  	"Which fields should have default values?",
  }

  var history []anthropic.BetaMessageParam
  for i, question := range questions {
  	turn := i + 1
  	history = append(history, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(question)))
  	response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 8192,
  		System:    system,
  		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
  		Messages:  history,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	history = append(history, response.ToParam())

  	// Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
  	conversationTokens := response.Usage.InputTokens + response.Usage.OutputTokens
  	if conversationTokens > compactAtTokens && turn < len(questions) {
  		summary, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 4096,
  			System:    system,
  			Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
  			Messages:  history,
  			Compaction: anthropic.BetaCompactionConfigUnionParam{
  				OfSummarize: &anthropic.BetaSummarizeCompactionParam{},
  			},
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		if summary.StopReason == anthropic.BetaStopReasonCompaction {
  			history = []anthropic.BetaMessageParam{summary.ToParam()}
  			fmt.Printf("Compacted before turn %d\n", turn+1)
  		}
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaCompactionConfig;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  static final long COMPACT_AT_TOKENS = 2500;
  static final String SYSTEM = "You help design a recipe app's data model. Keep answers short.";

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var questions = List.of(
          "What are the main entities in the data model?",
          "Which fields should Recipe have?",
          "Which fields should Ingredient have?",
          "Which fields should RecipeIngredient have?",
          "Which fields should Step have?",
          "Which indexes should these tables have?",
          "Which fields should be required?",
          "Which fields should have default values?"
      );

      var history = new ArrayList<BetaMessageParam>();
      for (int turn = 1; turn <= questions.size(); turn++) {
          history.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .content(questions.get(turn - 1))
              .build());
          var params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(8192)
              .system(SYSTEM)
              .addBeta(AnthropicBeta.COMPACT_2026_09_04)
              .messages(history)
              .build();
          var response = client.beta().messages().create(params);
          history.add(response.toParam());

          // Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung balasan ini.
          long conversationTokens = response.usage().inputTokens() + response.usage().outputTokens();
          if (conversationTokens > COMPACT_AT_TOKENS && turn < questions.size()) {
              var summaryParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(4096)
                  .system(SYSTEM)
                  .addBeta(AnthropicBeta.COMPACT_2026_09_04)
                  .messages(history)
                  .compaction(BetaCompactionConfig.builder().build()) // type defaults to "summarize"
                  .build();
              var summary = client.beta().messages().create(summaryParams);
              if (summary.stopReason().map(BetaStopReason.COMPACTION::equals).orElse(false)) {
                  history.clear();
                  history.add(summary.toParam());
                  IO.println("Compacted before turn " + (turn + 1));
              }
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaCompactionConfig;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Beta\Messages\BetaMessageParam\Role;
  use Anthropic\Beta\Messages\BetaStopReason;

  $client = new Client();

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini dibuat rendah agar percakapan singkat pun dipadatkan.
  const COMPACT_AT_TOKENS = 2500;
  const SYSTEM = "You help design a recipe app's data model. Keep answers short.";

  $questions = [
      'What are the main entities in the data model?',
      'Which fields should Recipe have?',
      'Which fields should Ingredient have?',
      'Which fields should RecipeIngredient have?',
      'Which fields should Step have?',
      'Which indexes should these tables have?',
      'Which fields should be required?',
      'Which fields should have default values?',
  ];

  $history = [];
  foreach ($questions as $index => $question) {
      $turn = $index + 1;
      $history[] = BetaMessageParam::with(role: Role::USER, content: $question);
      $response = $client->beta->messages->create(
          model: Model::CLAUDE_OPUS_5_5,
          maxTokens: 8192,
          system: SYSTEM,
          betas: [AnthropicBeta::COMPACT_2026_09_04],
          messages: $history,
      );
      $history[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $response->content);

      // Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
      $conversationTokens = $response->usage->inputTokens + $response->usage->outputTokens;
      if ($conversationTokens > COMPACT_AT_TOKENS && $turn < count($questions)) {
          $summary = $client->beta->messages->create(
              model: Model::CLAUDE_OPUS_5_5,
              maxTokens: 4096,
              system: SYSTEM,
              betas: [AnthropicBeta::COMPACT_2026_09_04],
              messages: $history,
              compaction: new BetaCompactionConfig(), // type defaults to 'summarize'
          );
          if ($summary->stopReason === BetaStopReason::COMPACTION->value) {
              $history = [BetaMessageParam::with(role: Role::ASSISTANT, content: $summary->content)];
              printf("Compacted before turn %d\n", $turn + 1);
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini sengaja rendah agar percakapan singkat pun dipadatkan.
  COMPACT_AT_TOKENS = 2500
  SYSTEM = "You help design a recipe app's data model. Keep answers short."

  questions = [
    "What are the main entities in the data model?",
    "Which fields should Recipe have?",
    "Which fields should Ingredient have?",
    "Which fields should RecipeIngredient have?",
    "Which fields should Step have?",
    "Which indexes should these tables have?",
    "Which fields should be required?",
    "Which fields should have default values?"
  ]

  history = []
  questions.each.with_index(1) do |question, turn|
    history << { role: "user", content: question }
    response = client.beta.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 8192,
      system_: SYSTEM,
      betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
      messages: history
    )
    history << { role: "assistant", content: response.content }

    # Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
    conversation_tokens = response.usage.input_tokens + response.usage.output_tokens
    if conversation_tokens > COMPACT_AT_TOKENS && turn < questions.length
      summary = client.beta.messages.create(
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
        max_tokens: 4096,
        system_: SYSTEM,
        betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
        messages: history,
        compaction: { type: "summarize" }
      )
      if summary.stop_reason == :compaction
        history = [{ role: "assistant", content: summary.content }]
        puts "Compacted before turn #{turn + 1}"
      end
    end
  end
  ```
</CodeGroup>

Pemeriksaan `stop_reason` dilakukan sebelum kode mencari blok; [Menangani ringkasan yang tidak ada atau error](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#when-no-summary-comes-back) menjelaskan alasannya. Riwayat diganti, bukan ditambahkan: pesan yang dikembalikan menggantikan setiap pesan yang dibawa permintaan, sesuai aturan di [Melanjutkan dari ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#continue-from-the-summary). Ketika tidak ada ringkasan yang dikembalikan, loop mempertahankan riwayatnya dan meminta lagi setelah giliran berikutnya.

[Tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner) SDK di Python, TypeScript, C#, Go, dan Java dapat mengirim permintaan compaction untuk Anda. Saat Anda memutuskan untuk melakukan compaction, panggil `compact_before_next_turn()` pada runner (`compactBeforeNextTurn()` di TypeScript dan Java, `CompactBeforeNextTurn()` di C# dan Go). Setelah giliran saat ini beserta panggilan alatnya selesai, runner mengirim permintaan compaction dan mengganti riwayatnya dengan pesan yang dikembalikan. Buat runner dengan beta `compact-2026-09-04`, karena runner tidak menambahkannya. Runner menyusun permintaan dari parameternya sendiri dan tidak menyertakan `context_management`. Jika parameter tersebut mencakup `stop_sequences`, `tool_choice` bertipe `any` atau `tool`, atau `output_config.format` untuk structured output, API menolak permintaan dengan error 400. [Meminta ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary) menjelaskan alasannya. Runner menolak melakukan compaction selama `context_management`-nya memiliki edit compaction, jadi gunakan satu jenis compaction saja pada sebuah runner.

### Kapan melakukan compaction

Anda dapat mengirim permintaan compaction setelah giliran mana pun yang telah selesai, sehingga kode Anda yang menentukan kapan.

Untuk memperkirakan seberapa besar permintaan berikutnya, jumlahkan `input_tokens` dan `output_tokens` dari `usage` respons terakhir, seperti yang dilakukan loop. Dengan ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#tracking-cache-performance), `input_tokens` hanya menghitung token setelah cache breakpoint terakhir, jadi tambahkan juga `cache_read_input_tokens` dan `cache_creation_input_tokens`. Anda juga dapat mengirim pesan yang sama ke endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

Bandingkan angka tersebut dengan batas yang Anda pilih, di bawah [jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows) model.

## Menulis prompt peringkasan Anda sendiri

Tanpa `instructions`, API menggunakan prompt peringkasannya sendiri. String `instructions` yang tidak kosong (hingga 16.384 karakter) menggantikan prompt tersebut sepenuhnya. Sebagai contoh:

```json
{
  "compaction": {
    "type": "summarize",
    "instructions": "Summarize this recipe app design conversation. Preserve every entity and field name agreed so far, and the user's latest open request. Do not call tools; respond with the summary text only."
  }
}
```

Peringkas membaca seluruh percakapan, termasuk thinking sebelumnya, baik dengan maupun tanpa `instructions`. Dalam `instructions` Anda, sebutkan apa yang harus dipertahankan oleh ringkasan dan minta model untuk tidak memanggil alat. Panggilan peringkasan berjalan di bawah perlindungan yang sama seperti permintaan lainnya.

## Menangani ringkasan yang tidak ada atau error

Ringkasan hanya dihasilkan ketika panggilan peringkasan berakhir secara normal dengan teks dan tanpa panggilan alat. Jika tidak, respons tetap berstatus 200 dengan `content` kosong, jadi periksa `stop_reason` sebelum Anda mencari blok. Panggilan tersebut tetap ditagih dan dilaporkan di `usage.iterations`, dengan penggunaan nol jika tidak ada panggilan yang dapat dilakukan. `stop_reason` adalah alasan berhentinya panggilan peringkasan. Dalam setiap kasus, Anda dapat melanjutkan tanpa ringkasan dan melakukan compaction nanti.

| `stop_reason`                     | Penyebab                                          | Yang harus dilakukan                                                               |
| --------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `"max_tokens"`                    | Ringkasan terpotong.                              | Kirim ulang dengan `max_tokens` yang lebih besar.                                  |
| `"model_context_window_exceeded"` | Tidak ada ruang untuk prompt peringkasan.         | Kirim ulang dengan `instructions` yang lebih pendek atau pesan yang lebih sedikit. |
| `"tool_use"`                      | Model memanggil alat alih-alih menulis ringkasan. | Kirim ulang dengan `instructions` yang meminta model untuk tidak memanggil alat.   |
| `"refusal"`                       | Permintaan ditolak.                               | Lanjutkan tanpa ringkasan.                                                         |
| `"end_turn"`                      | Panggilan tidak mengembalikan teks.               | Lanjutkan tanpa ringkasan.                                                         |

Panggilan peringkasan tunduk pada perlindungan yang sama seperti permintaan Anda yang lain. Setelah `"refusal"`, [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#refusal) mengidentifikasi kategori kebijakan yang mendasarinya.

### Error

Permintaan compaction, atau permintaan yang membawa blok, juga dapat gagal sepenuhnya. Sebagian besar error 400 memiliki pesan yang menyebutkan apa yang harus dihapus atau dikirim ulang. Beberapa juga membawa `error.details.error_code` yang diawali dengan `compaction_`. Error parameter, seperti field yang tidak dapat digabungkan dengan `compaction`, hanya membawa pesan.

| Error                                                                                                                                                                                          | Penyebab                                                                                         | Yang harus dilakukan                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 529 `overloaded_error`, `error.details.error_code` `compaction_unavailable`                                                                                                                    | Masalah server sementara saat menghasilkan blok, atau saat membaca blok yang Anda kirim kembali. | Coba ulang permintaan.                                                                                                                                                                 |
| 400 `compaction_block_misplaced`                                                                                                                                                               | Pesan yang diringkas masih tersisa di depan blok.                                                | Hapus pesan-pesan tersebut, sehingga blok berada di urutan pertama dalam `messages`.                                                                                                   |
| 400 `compaction_signature_invalid` atau `compaction_content_mismatch`                                                                                                                          | `signature` atau `content` blok diubah setelah API mengembalikannya.                             | Kirim blok persis seperti yang dikembalikan, termasuk `signature`-nya.                                                                                                                 |
| 400                                                                                                                                                                                            | Permintaan membawa lebih dari satu blok `compaction`.                                            | Kirim tepat satu, yaitu yang terbaru.                                                                                                                                                  |
| 400                                                                                                                                                                                            | Giliran `assistant` terakhir diakhiri dengan panggilan alat yang belum memiliki hasil.           | Kirim hasil alat dari giliran tersebut, lalu lakukan compaction.                                                                                                                       |
| 400 `compaction_nothing_to_summarize`                                                                                                                                                          | `messages` tidak memiliki konten `user` atau `assistant`, misalnya daftar kosong.                | Kirim setidaknya satu pesan `user` atau `assistant`.                                                                                                                                   |
| 400 pada permintaan compaction, dengan pesan yang menyatakan bahwa parameter `compaction` `requires anthropic-beta: compact-2026-09-04`                                                        | Permintaan compaction tidak menyertakan header beta.                                             | Tambahkan header beta; lihat [Meminta ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary).                                        |
| 400 pada permintaan berikutnya yang membawa blok: error validasi yang menyatakan bahwa `compaction` bukan salah satu tipe blok konten yang diharapkan. Pesan tersebut tidak menyebutkan header | Permintaan tersebut tidak menyertakan header beta.                                               | Tambahkan header beta ke setiap permintaan yang membawa blok; lihat [Meminta ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary). |
| Error validasi 400, seperti `messages.0.content.0.compaction.citations: Extra inputs are not permitted`                                                                                        | Blok dikirim kembali dengan field yang tidak dikembalikan API, seperti `citations: null`.        | Kirim blok persis seperti yang dikembalikan; lihat [Melanjutkan dari ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#continue-from-the-summary). |

## Menghitung penggunaan compaction

Panggilan peringkasan ditagih dan dikenai "rate limit" (batas laju) seperti permintaan lainnya, dan `usage.iterations` melaporkannya sebagai entri `compaction`. `input_tokens` dan `output_tokens` tingkat atas bernilai nol karena tidak ada balasan yang dihasilkan. Untuk menghitung apa yang dikonsumsi sebuah percakapan, jumlahkan seluruh `usage.iterations`, bukan field tingkat atas. Mengirim kembali blok pada permintaan berikutnya tidak menambah biaya compaction.

Anda kini memiliki loop yang berfungsi untuk melakukan compaction pada percakapan dan menangani ringkasan yang tidak ada. Dua halaman mengubah cara loop tersebut berjalan, dan Anda dapat menggabungkan keduanya: [Compaction yang mempertahankan giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/compaction-keep-recent-turns) mempertahankan giliran terakhir kata demi kata, dan [Compaction di latar belakang](https://platform.claude.com/docs/id/build-with-claude/compaction-background) memungkinkan percakapan berlanjut selama ringkasan ditulis. [Compaction dan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks) berlaku jika Anda mengirim kembali blok thinking dan melakukan salah satu dari keduanya.

## Batasan dan interaksi dengan fitur lain

* **Compaction ambang batas dan pengeditan konteks.** Anda tidak dapat mengirim `compaction` dan `context_management` dalam permintaan yang sama. Compaction ambang batas (`compact_20260112`) tidak dapat berjalan pada permintaan yang membawa blok bertanda tangan.
* **Caching prompt.** `cache_control` pada blok menempatkan breakpoint setelah ringkasan.
* **Pesan sistem dan perubahan alat di tengah percakapan.** Pesan `role: "system"` di dalam rentang yang diringkas juga ikut diringkas, sehingga instruksi teksnya tidak lagi berlaku setelah blok menggantikannya. Jika suatu instruksi masih penting, nyatakan kembali dalam pesan `role: "system"`. Kirim pesan tersebut tepat setelah giliran `user` baru Anda berikutnya, dan biarkan pesan itu tetap ada di riwayat Anda sejak saat itu. Untuk [perubahan alat](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes), dan untuk posisi pesan tersebut ketika Anda mempertahankan giliran setelah blok, lihat [Mengubah prompt sistem atau alat](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#change-the-system-prompt-or-tools).
* **Anggaran tugas.** Jangan kirim nilai `remaining` dari [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (`output_config.task_budget.remaining`) bersama `compaction` atau pada permintaan yang membawa blok. Melakukannya akan mengembalikan error 400.
* **Penghitungan token.** Endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengabaikan parameter `compaction`.
* **Konten yang tidak dapat dibawa oleh ringkasan.** Gambar, dokumen, blok `container_upload`, dan URL yang diambil di dalam pesan yang diringkas akan hilang setelah blok menggantikannya. Nyatakan ulang atau unggah ulang apa pun yang masih dibutuhkan oleh giliran berikutnya.
