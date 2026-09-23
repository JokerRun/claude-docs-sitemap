---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction-keep-recent-turns
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: b91c57790b1aa67aa3bfacb6f3bea565d9906e77f12492c30f3113bb97520559
---

---
title: Compaction yang mempertahankan giliran terbaru
url: https://platform.claude.com/docs/id/build-with-claude/compaction-keep-recent-turns
description: Ringkas giliran-giliran lama dalam percakapan dengan compaction sesuai permintaan, lalu kirim giliran-giliran terbaru setelah ringkasan, kata demi kata.
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

"Keep-tail compaction" (compaction yang mempertahankan ekor percakapan) mempertahankan beberapa giliran terakhir dari sebuah percakapan kata demi kata setelah ringkasan. Fitur ini mengubah dua hal dalam [loop compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-in-a-loop): pesan mana yang masuk ke dalam permintaan compaction, dan apa yang Anda kirim setelah blok. Semua yang ada di [Melanjutkan dari ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#continue-from-the-summary) tetap berlaku tanpa perubahan.

## Memilih giliran yang dipertahankan

Tidak ada parameter yang menentukan giliran mana yang dipertahankan. Anda memilih titik potong dalam riwayat Anda: pesan-pesan sebelum titik tersebut masuk ke dalam permintaan compaction, dan pesan-pesan mulai dari titik tersebut dan seterusnya dipertahankan.

Giliran yang dipertahankan dikirim kembali ke Claude dengan panjang penuh, sehingga semakin banyak yang Anda pertahankan, semakin sedikit ruang yang dibebaskan oleh compaction.

Letakkan titik potong di tempat yang tidak menyisakan panggilan alat yang masih terbuka, dengan setiap panggilan alat dan hasilnya berada di sisi yang sama. Jika pesan-pesan yang Anda kirim diakhiri dengan giliran `assistant` yang panggilan alatnya belum memiliki hasil, API akan menolak permintaan compaction tersebut.

## Melakukan compaction pada giliran-giliran lama dan mengirim sisanya setelah blok

Untuk mempertahankan ekor berupa giliran-giliran terbaru kata demi kata, jangan sertakan giliran-giliran tersebut dalam permintaan compaction. API meringkas setiap pesan yang dikirimkan kepadanya, jadi kirim hanya giliran-giliran lama, lalu letakkan blok di depan giliran-giliran yang Anda pertahankan.

Kirim giliran yang dipertahankan persis seperti yang ada di riwayat Anda, termasuk "thinking blocks" (blok pemikiran). Kedua permintaan membawa header beta, seperti pada [Meminta ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary).

Dalam contoh berikut, riwayat berisi dua giliran, dan titik potong mempertahankan giliran kedua. Permintaan compaction membawa giliran pertama:

```json
{
  "model": "claude-opus-5-5",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": "I am building a recipe app. Help me name the main entities in the data model."
    },
    {
      "role": "assistant",
      "content": "Start with Recipe, Ingredient, and Step. Add a RecipeIngredient entry that holds the quantity and unit for each ingredient in a recipe."
    }
  ],
  "compaction": { "type": "summarize" }
}
```

Permintaan berikutnya mengirim blok yang dikembalikan terlebih dahulu, lalu giliran yang dipertahankan persis seperti aslinya, kemudian pesan `user` yang baru. [Melanjutkan dari ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#continue-from-the-summary) menunjukkan permintaan yang dimulai dengan sebuah blok.

Program berikut adalah loop dari [Compaction dalam loop](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-in-a-loop), yang diubah untuk mempertahankan dua giliran terakhir. Baris yang disorot menunjukkan bagian yang berbeda dari loop tersebut.

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.types.beta import BetaMessageParam

  client = anthropic.Anthropic()

  # Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini dibuat rendah agar percakapan singkat pun dipadatkan.
  COMPACT_AT_TOKENS = 2500
  SYSTEM = "You help design a recipe app's data model. Keep answers short."
  KEEP_TURNS = 2

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
      if conversation_tokens > COMPACT_AT_TOKENS and KEEP_TURNS < turn < len(QUESTIONS):
          # Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten,
          # sehingga giliran yang dipertahankan diawali dengan pesan pengguna.
          split = -2 * KEEP_TURNS
          older, recent = history[:split], history[split:]
          summary = client.beta.messages.create(
              model="claude-opus-5-5",
              max_tokens=4096,
              system=SYSTEM,
              betas=["compact-2026-09-04"],
              messages=older,
              compaction={"type": "summarize"},
          )
          if summary.stop_reason == "compaction":
              history = [{"role": "assistant", "content": summary.content}, *recent]
              print(f"Kept {len(recent) // 2} turns after the block")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  const compactAtTokens = 2500;
  const systemPrompt = "You help design a recipe app's data model. Keep answers short.";
  const keepTurns = 2;

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

    // Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
    const conversationTokens = response.usage.input_tokens + response.usage.output_tokens;
    if (conversationTokens > compactAtTokens && turn > keepTurns && turn < questions.length) {
      // Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
      const older = history.slice(0, -2 * keepTurns);
      const recent = history.slice(-2 * keepTurns);
      const summary = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 4096,
        system: systemPrompt,
        betas: ["compact-2026-09-04"],
        messages: older,
        compaction: { type: "summarize" }
      });
      if (summary.stop_reason === "compaction") {
        history = [{ role: "assistant", content: summary.content }, ...recent];
        console.log(`Kept ${recent.length / 2} turns after the block`);
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
  const int KeepTurns = 2;

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

      // Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
      var conversationTokens = response.Usage.InputTokens + response.Usage.OutputTokens;
      if (conversationTokens > CompactAtTokens && turn > KeepTurns && turn < questions.Length)
      {
          // Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
          var older = history[..^(2 * KeepTurns)];
          var recent = history[^(2 * KeepTurns)..];
          var summary = await client.Beta.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus5_5,
              MaxTokens = 4096,
              System = SystemPrompt,
              Betas = [AnthropicBeta.Compact2026_09_04],
              Messages = older,
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
                  .. recent,
              ];
              Console.WriteLine($"Kept {recent.Count / 2} turns after the block");
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
  const keepTurns = 2

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
  	if conversationTokens > compactAtTokens && turn > keepTurns && turn < len(questions) {
  		// Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
  		split := len(history) - 2*keepTurns
  		older, recent := history[:split], history[split:]
  		summary, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 4096,
  			System:    system,
  			Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
  			Messages:  older,
  			Compaction: anthropic.BetaCompactionConfigUnionParam{
  				OfSummarize: &anthropic.BetaSummarizeCompactionParam{},
  			},
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		if summary.StopReason == anthropic.BetaStopReasonCompaction {
  			history = slices.Replace(history, 0, split, summary.ToParam())
  			fmt.Printf("Kept %d turns after the block\n", len(recent)/2)
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
  static final int KEEP_TURNS = 2;

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

          // Permintaan berikutnya juga mengirim balasan ini, jadi ikut hitung.
          long conversationTokens = response.usage().inputTokens() + response.usage().outputTokens();
          if (conversationTokens > COMPACT_AT_TOKENS && turn > KEEP_TURNS && turn < questions.size()) {
              // Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
              var older = history.subList(0, history.size() - 2 * KEEP_TURNS);
              var summaryParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(4096)
                  .system(SYSTEM)
                  .addBeta(AnthropicBeta.COMPACT_2026_09_04)
                  .messages(older)
                  .compaction(BetaCompactionConfig.builder().build()) // type defaults to "summarize"
                  .build();
              var summary = client.beta().messages().create(summaryParams);
              if (summary.stopReason().map(BetaStopReason.COMPACTION::equals).orElse(false)) {
                  older.clear();
                  history.addFirst(summary.toParam());
                  IO.println("Kept " + (history.size() - 1) / 2 + " turns after the block");
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

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  const COMPACT_AT_TOKENS = 2500;
  const SYSTEM = "You help design a recipe app's data model. Keep answers short.";
  const KEEP_TURNS = 2;

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

      // Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
      $conversationTokens = $response->usage->inputTokens + $response->usage->outputTokens;
      if ($conversationTokens > COMPACT_AT_TOKENS && $turn > KEEP_TURNS && $turn < count($questions)) {
          // Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
          $older = array_slice($history, 0, -2 * KEEP_TURNS);
          $recent = array_slice($history, -2 * KEEP_TURNS);
          $summary = $client->beta->messages->create(
              model: Model::CLAUDE_OPUS_5_5,
              maxTokens: 4096,
              system: SYSTEM,
              betas: [AnthropicBeta::COMPACT_2026_09_04],
              messages: $older,
              compaction: new BetaCompactionConfig(), // type defaults to 'summarize'
          );
          if ($summary->stopReason === BetaStopReason::COMPACTION->value) {
              $history = [BetaMessageParam::with(role: Role::ASSISTANT, content: $summary->content), ...$recent];
              printf("Kept %d turns after the block\n", intdiv(count($recent), 2));
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini dibuat rendah agar percakapan singkat pun dipadatkan.
  COMPACT_AT_TOKENS = 2500
  SYSTEM = "You help design a recipe app's data model. Keep answers short."
  KEEP_TURNS = 2

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
    if conversation_tokens > COMPACT_AT_TOKENS && turn > KEEP_TURNS && turn < questions.length
      # Satu giliran terdiri dari satu pesan pengguna dan satu balasan asisten, jadi giliran yang disimpan diawali pesan pengguna.
      older, recent = history[...-2 * KEEP_TURNS], history.last(2 * KEEP_TURNS)
      summary = client.beta.messages.create(
        model: Anthropic::Model::CLAUDE_OPUS_5_5,
        max_tokens: 4096,
        system_: SYSTEM,
        betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
        messages: older,
        compaction: { type: "summarize" }
      )
      if summary.stop_reason == :compaction
        history = [{ role: "assistant", content: summary.content }, *recent]
        puts "Kept #{recent.length / 2} turns after the block"
      end
    end
  end
  ```
</CodeGroup>

* **Memilih titik potong:** Program mempertahankan dua giliran terakhir, di mana satu giliran adalah satu pesan `user` beserta balasannya. Program membagi riwayat pada posisi empat pesan dari akhir, sehingga giliran yang dipertahankan dimulai dengan pesan `user`.
* **Menentukan kapan melakukan compaction:** Pemeriksaan ukuran juga mensyaratkan bahwa percakapan memiliki lebih banyak giliran daripada yang dipertahankan program, sehingga bagian lama tidak pernah kosong.
* **Permintaan compaction:** Sementara loop mengirim seluruh riwayat, versi ini hanya mengirim pesan-pesan lama.
* **Penukaran:** Sementara loop mengganti seluruh riwayat dengan pesan yang dikembalikan, riwayat baru pada versi ini adalah pesan yang dikembalikan diikuti oleh giliran-giliran yang dipertahankan.

Pemeriksaan `stop_reason` dan setiap permintaan setelah penukaran tidak berubah dari loop tersebut.

## Menjaga validitas thinking dalam giliran yang dipertahankan

Jika Anda mengirim kembali blok thinking pada model dengan ["preserved thinking" (pemikiran yang dipertahankan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking), thinking dalam giliran yang dipertahankan hanya tetap valid selama [syarat agar thinking yang dipertahankan tetap valid](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid) terpenuhi, dan salah satu syarat tersebut membatasi di mana titik potong dapat diletakkan.

Titik potong program, yaitu di antara sebuah balasan dan pesan `user` berikutnya, memenuhi syarat tersebut. Begitu pula titik potong di akhir permintaan yang sudah Anda buat: lakukan compaction tepat pada `messages` dari permintaan tersebut, dan pertahankan semua yang telah ditambahkan ke riwayat Anda sejak saat itu.
