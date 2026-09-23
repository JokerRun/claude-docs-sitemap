---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction-background
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: 6a121c6f46aed870272bbe38f2ae63c6142c11ea873e879d3b19f01f3bda867b
---

---
title: Compaction di latar belakang
url: https://platform.claude.com/docs/id/build-with-claude/compaction-background
description: Minta ringkasan compaction sesuai permintaan sementara percakapan berlanjut pada riwayat lengkapnya, lalu tukar blok tersebut ke dalam riwayat saat blok itu tiba.
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

"Background compaction" (pemadatan latar belakang), yang sering disebut "async compaction" (pemadatan asinkron), mengubah dua hal dalam [loop compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-in-a-loop): permintaan compaction berjalan sementara percakapan berlanjut pada riwayat lengkapnya, dan penukaran menunggu hingga blok tiba. [Melanjutkan dari ringkasan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#continue-from-the-summary) dan [Menangani ringkasan yang tidak ada atau error](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#when-no-summary-comes-back) berlaku tanpa perubahan.

## Cara kerja penukaran sementara pekerjaan berlanjut

Permintaan compaction dan blok yang dikembalikannya sama seperti dalam loop. Riwayat Anda bertambah antara saat permintaan dikirim dan saat hasilnya digunakan, dan "swap" (penukaran) harus membiarkan pertambahan tersebut tetap di tempatnya.

1. Kirim [permintaan compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary) dengan riwayat Anda sebagaimana adanya, dan catat berapa banyak pesan yang dimuatnya.
2. Selama permintaan tersebut berjalan, teruskan percakapan pada riwayat lengkap. Tambahkan setiap giliran baru, jangan mengedit apa pun yang sudah ada dalam riwayat, dan jangan memulai permintaan compaction lain hingga permintaan ini selesai ditukar atau gagal.
3. Saat respons tiba dengan `stop_reason` `"compaction"`, hapus tepat pesan-pesan yang Anda kirim dari bagian depan riwayat Anda dan letakkan pesan yang dikembalikan di tempatnya. Setiap giliran yang ditambahkan sejak langkah 1 tetap berada setelahnya.
4. Kirim riwayat yang sudah ditukar pada permintaan pertama setelah blok tiba, sehingga thinking yang dihasilkan selama ringkasan sedang ditulis tetap valid.

Sebagai contoh, jika permintaan compaction memuat pesan 1 hingga 5 dan percakapan bertambah dengan pesan 6 hingga 8 selama permintaan itu berjalan, setelah penukaran riwayat Anda adalah blok tersebut diikuti oleh pesan 6 hingga 8.

![Linimasa background compaction (pemadatan latar belakang): permintaan compaction dikirim dengan pesan 1 hingga 5 sementara percakapan berlanjut pada riwayat lengkapnya dan bertambah dengan pesan 6 hingga 8; saat blok tiba, blok tersebut menggantikan pesan 1 hingga 5 di bagian depan riwayat, dan riwayat menjadi blok tersebut diikuti oleh pesan 6 hingga 8](https://platform.claude.com/docs/images/compaction-background-timeline.svg)

Jika respons memiliki `stop_reason` lain, tidak ada ringkasan yang dihasilkan, dan hal ini dihitung sebagai kegagalan pada langkah 2. Pertahankan riwayat lengkap; [Menangani ringkasan yang tidak ada atau error](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#when-no-summary-comes-back) mencantumkan penyebabnya dan apa yang harus dilakukan untuk masing-masing.

## Meminta ringkasan di latar belakang

Permintaan compaction dihitung terhadap batas laju Anda seperti permintaan lainnya, dan selama permintaan itu berjalan, aplikasi Anda memiliki dua permintaan yang terbuka sekaligus. Percakapan terus bertambah pada riwayat lengkapnya hingga penukaran, jadi mulailah permintaan compaction selagi "context window" (jendela konteks) masih memiliki ruang untuk giliran-giliran yang tiba sementara itu.

Program berikut adalah loop dari [Compaction dalam loop](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-in-a-loop) dengan permintaan compaction dipindahkan dari jalur percakapan. Program ini tidak memiliki versi PHP, karena contohnya bergantung pada menjalankan dua permintaan sekaligus. Baris yang disorot menunjukkan di mana program ini berbeda dari loop, dan daftar berikut membahasnya sesuai urutan program menjalankannya.

<CodeGroup exclude="shell, php">
  ```python Python
  from concurrent.futures import Future, ThreadPoolExecutor

  import anthropic
  from anthropic.types.beta import BetaMessage, BetaMessageParam

  client = anthropic.Anthropic()
  executor = ThreadPoolExecutor(max_workers=1)

  # Atur ini mendekati anggaran input Anda yang sebenarnya. Di sini dibuat rendah agar percakapan singkat pun dipadatkan.
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


  def swap_in(history: list[BetaMessageParam], summary: BetaMessage, sent: int) -> None:
      if summary.stop_reason == "compaction":
          # Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan.
          # Giliran berikutnya tetap berada setelah blok tersebut.
          history[:sent] = [{"role": "assistant", "content": summary.content}]
          print(f"Swapped {sent} messages")


  history: list[BetaMessageParam] = []
  pending: Future[BetaMessage] | None = None
  sent = 0
  for turn, question in enumerate(QUESTIONS, start=1):
      if pending is not None and pending.done():
          swap_in(history, pending.result(), sent)
          pending = None

      history.append({"role": "user", "content": question})
      response = client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=8192,
          system=SYSTEM,
          betas=["compact-2026-09-04"],
          messages=history,
      )
      history.append({"role": "assistant", "content": response.content})

      # Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
      conversation_tokens = response.usage.input_tokens + response.usage.output_tokens
      if (
          conversation_tokens > COMPACT_AT_TOKENS
          and turn < len(QUESTIONS)
          and pending is None
      ):
          sent = len(history)
          pending = executor.submit(
              client.beta.messages.create,
              model="claude-opus-5-5",
              max_tokens=4096,
              system=SYSTEM,
              betas=["compact-2026-09-04"],
              messages=history.copy(),
              compaction={"type": "summarize"},
          )

  # Pasang ringkasan yang masih dalam proses sebelum Anda menyimpan
  # atau melanjutkan percakapan.
  if pending is not None:
      swap_in(history, pending.result(), sent)
  executor.shutdown()
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

  function swapIn(
    history: Anthropic.Beta.Messages.BetaMessageParam[],
    summary: Anthropic.Beta.Messages.BetaMessage,
    sent: number
  ): Anthropic.Beta.Messages.BetaMessageParam[] {
    if (summary.stop_reason !== "compaction") {
      return history;
    }
    console.log(`Swapped ${sent} messages`);
    // Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan. Giliran berikutnya tetap berada setelah blok tersebut.
    return [{ role: "assistant", content: summary.content }, ...history.slice(sent)];
  }

  let history: Anthropic.Beta.Messages.BetaMessageParam[] = [];
  let pending: Promise<Anthropic.Beta.Messages.BetaMessage> | undefined;
  let settled = false;
  let sent = 0;
  for (const [index, question] of questions.entries()) {
    const turn = index + 1;
    if (pending && settled) {
      history = swapIn(history, await pending, sent);
      pending = undefined;
      settled = false;
    }

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
    if (conversationTokens > compactAtTokens && turn < questions.length && !pending) {
      sent = history.length;
      pending = client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 4096,
        system: systemPrompt,
        betas: ["compact-2026-09-04"],
        messages: [...history],
        compaction: { type: "summarize" }
      });
      // Tandai permintaan sebagai selesai dalam kedua kasus. Menunggunya kemudian akan mengembalikan ringkasan atau melempar error.
      const markSettled = () => {
        settled = true;
      };
      pending.then(markSettled, markSettled);
    }
  }

  // Masukkan ringkasan yang masih dalam proses sebelum Anda menyimpan atau melanjutkan percakapan.
  if (pending) {
    history = swapIn(history, await pending, sent);
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

  static List<BetaMessageParam> SwapIn(List<BetaMessageParam> history, BetaMessage summary, int sent)
  {
      if (summary.StopReason != BetaStopReason.Compaction)
      {
          return history;
      }
      Console.WriteLine($"Swapped {sent} messages");
      // Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan. Giliran berikutnya tetap berada setelah blok tersebut.
      return
      [
          new()
          {
              Role = Role.Assistant,
              Content = summary.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
          },
          .. history[sent..],
      ];
  }

  List<BetaMessageParam> history = [];
  Task<BetaMessage>? pending = null;
  var sent = 0;
  foreach (var (index, question) in questions.Index())
  {
      var turn = index + 1;
      if (pending is { IsCompleted: true })
      {
          history = SwapIn(history, await pending, sent);
          pending = null;
      }

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

      // Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga balasan ini.
      var conversationTokens = response.Usage.InputTokens + response.Usage.OutputTokens;
      if (conversationTokens > CompactAtTokens && turn < questions.Length && pending is null)
      {
          sent = history.Count;
          pending = client.Beta.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus5_5,
              MaxTokens = 4096,
              System = SystemPrompt,
              Betas = [AnthropicBeta.Compact2026_09_04],
              Messages = [.. history],
              Compaction = new BetaCompactionConfig(), // type defaults to "summarize"
          });
      }
  }

  // Tukar dengan ringkasan yang masih dalam proses sebelum Anda menyimpan atau melanjutkan percakapan.
  if (pending is not null)
  {
      history = SwapIn(history, await pending, sent);
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
  var pending chan *anthropic.BetaMessage
  var sent int
  swapIn := func(summary *anthropic.BetaMessage) {
  	if summary.StopReason != anthropic.BetaStopReasonCompaction {
  		return
  	}
  	fmt.Printf("Swapped %d messages\n", sent)
  	// Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan. Giliran berikutnya tetap berada setelah blok tersebut.
  	history = slices.Replace(history, 0, sent, summary.ToParam())
  }

  for i, question := range questions {
  	turn := i + 1
  	// Menerima dari channel nil tidak pernah berhasil, jadi bagian ini dilewati jika tidak ada yang tertunda.
  	select {
  	case summary := <-pending:
  		swapIn(summary)
  		pending = nil
  	default:
  	}

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

  	// Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
  	conversationTokens := response.Usage.InputTokens + response.Usage.OutputTokens
  	if conversationTokens > compactAtTokens && turn < len(questions) && pending == nil {
  		sent = len(history)
  		pending = make(chan *anthropic.BetaMessage, 1)
  		go func(messages []anthropic.BetaMessageParam, result chan<- *anthropic.BetaMessage) {
  			summary, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  				Model:     anthropic.ModelClaudeOpus5_5,
  				MaxTokens: 4096,
  				System:    system,
  				Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
  				Messages:  messages,
  				Compaction: anthropic.BetaCompactionConfigUnionParam{
  					OfSummarize: &anthropic.BetaSummarizeCompactionParam{},
  				},
  			})
  			if err != nil {
  				log.Fatal(err)
  			}
  			result <- summary
  		}(slices.Clone(history), pending)
  	}
  }

  // Tukar dengan ringkasan yang masih dalam proses sebelum Anda menyimpan atau melanjutkan percakapan.
  if pending != nil {
  	swapIn(<-pending)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaCompactionConfig;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  // Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
  static final long COMPACT_AT_TOKENS = 2500;
  static final String SYSTEM = "You help design a recipe app's data model. Keep answers short.";

  void swapIn(List<BetaMessageParam> history, BetaMessage summary, int sent) {
      if (!summary.stopReason().map(BetaStopReason.COMPACTION::equals).orElse(false)) {
          return;
      }
      IO.println("Swapped " + sent + " messages");
      // Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan. Giliran berikutnya tetap berada setelah blok tersebut.
      history.subList(0, sent).clear();
      history.addFirst(summary.toParam());
  }

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
      CompletableFuture<BetaMessage> pending = null;
      int sent = 0;
      for (int turn = 1; turn <= questions.size(); turn++) {
          if (pending != null && pending.isDone()) {
              swapIn(history, pending.join(), sent);
              pending = null;
          }

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

          // Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga balasan ini.
          long conversationTokens = response.usage().inputTokens() + response.usage().outputTokens();
          if (conversationTokens > COMPACT_AT_TOKENS && turn < questions.size() && pending == null) {
              sent = history.size();
              var summaryParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(4096)
                  .system(SYSTEM)
                  .addBeta(AnthropicBeta.COMPACT_2026_09_04)
                  .messages(List.copyOf(history))
                  .compaction(BetaCompactionConfig.builder().build()) // type defaults to "summarize"
                  .build();
              pending = client.async().beta().messages().create(summaryParams);
          }
      }

      // Masukkan ringkasan yang masih dalam proses sebelum Anda menyimpan atau melanjutkan percakapan.
      if (pending != null) {
          swapIn(history, pending.join(), sent);
      }
      client.close();
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Atur nilai ini mendekati anggaran input Anda yang sebenarnya. Di sini nilainya rendah agar percakapan singkat pun dipadatkan.
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

  def swap_in(history, summary, sent)
    return history unless summary.stop_reason == :compaction

    puts "Swapped #{sent} messages"
    # Ganti tepat pesan-pesan yang dimuat oleh permintaan pemadatan. Giliran berikutnya tetap berada setelah blok tersebut.
    [{ role: "assistant", content: summary.content }, *history[sent..]]
  end

  history = []
  pending = nil
  sent = 0
  questions.each.with_index(1) do |question, turn|
    if pending && !pending.alive?
      history = swap_in(history, pending.value, sent)
      pending = nil
    end

    history << { role: "user", content: question }
    response = client.beta.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 8192,
      system_: SYSTEM,
      betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
      messages: history
    )
    history << { role: "assistant", content: response.content }

    # Permintaan berikutnya juga mengirim balasan ini, jadi hitung juga.
    conversation_tokens = response.usage.input_tokens + response.usage.output_tokens
    if conversation_tokens > COMPACT_AT_TOKENS && turn < questions.length && pending.nil?
      sent = history.length
      pending = Thread.new(history.dup) do |snapshot|
        client.beta.messages.create(
          model: Anthropic::Model::CLAUDE_OPUS_5_5,
          max_tokens: 4096,
          system_: SYSTEM,
          betas: [Anthropic::AnthropicBeta::COMPACT_2026_09_04],
          messages: snapshot,
          compaction: { type: "summarize" }
        )
      end
    end
  end

  # Ganti dengan ringkasan yang masih dalam proses sebelum Anda menyimpan atau melanjutkan percakapan.
  history = swap_in(history, pending.value, sent) if pending
  ```
</CodeGroup>

* **Menentukan kapan melakukan compaction:** Pemeriksaan ukuran juga mensyaratkan bahwa tidak ada permintaan compaction yang sedang tertunda.
* **Memulai permintaan:** Di tempat loop menunggu respons compaction, versi ini mencatat berapa banyak pesan yang dimuat riwayat, memulai permintaan pada salinan riwayat dengan alat konkurensi milik masing-masing bahasa, dan melanjutkan ke giliran berikutnya tanpa menunggu.
* **Memeriksa hasil:** Di awal setiap giliran, program memeriksa apakah permintaan yang tertunda sudah selesai. Jika sudah, program melakukan penukaran sebelum mengirim permintaan untuk giliran tersebut.
* **Melakukan penukaran:** Di tempat loop mengganti seluruh riwayat dengan pesan yang dikembalikan, fungsi penukaran versi ini hanya mengganti pesan-pesan yang dimuat oleh permintaan, dihitung dari bagian depan, dan mempertahankan semua yang ditambahkan sejak saat itu.
* **Mengakhiri loop:** Jika permintaan compaction masih tertunda saat loop berakhir, program menunggunya dan melakukan penukaran, sehingga ringkasan yang masih dalam perjalanan tidak hilang sebelum Anda menyimpan atau melanjutkan percakapan.

Pemeriksaan `stop_reason` tidak berubah dari loop: respons tanpa blok membiarkan riwayat seperti semula. Karena tidak ada lagi yang tertunda, program kemudian dapat memulai permintaan compaction baru.

## Menjaga thinking tetap valid selama ringkasan dibuat

Giliran yang tiba selama ringkasan sedang ditulis adalah giliran yang dipertahankan. Jika Anda mengirim kembali blok thinking pada model dengan ["preserved thinking" (pemikiran yang dipertahankan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking), thinking dalam giliran-giliran tersebut tetap valid hanya selama [syarat agar thinking yang dipertahankan tetap valid](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid) terpenuhi.
