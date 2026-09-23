---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: c5cda1a0834803820df693cdd66e57eee72cffb1fb483a41c827b8404f061088
---

---
title: Compaction dan pemikiran yang dipertahankan
url: https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks
description: Kapan blok thinking dalam giliran yang dipertahankan setelah compaction sesuai permintaan tetap valid pada model dengan pemikiran yang dipertahankan, dan cara memeriksanya.
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

Lewati halaman ini kecuali Anda mengirim "thinking blocks" (blok pemikiran) kembali ke model dengan ["preserved thinking" (pemikiran yang dipertahankan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan mempertahankan giliran setelah blok "compaction" (pemadatan). "Kept turns" (giliran yang dipertahankan) adalah giliran yang mengikuti blok tersebut: giliran terbaru yang Anda keluarkan dari permintaan compaction, seperti dalam [Compaction yang mempertahankan giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/compaction-keep-recent-turns), atau giliran yang tiba saat ringkasan sedang ditulis, seperti dalam [Compaction di latar belakang](https://platform.claude.com/docs/id/build-with-claude/compaction-background).

Model dengan pemikiran yang dipertahankan memeriksa blok thinking sebelumnya terhadap percakapan yang menghasilkannya. Ringkasan menggantikan sebagian percakapan tersebut, tetapi pemeriksaan menerima pertukaran itu ketika API yang menulis ringkasannya, sehingga thinking dalam giliran yang dipertahankan dapat tetap valid.

## Syarat agar thinking yang dipertahankan tetap valid

Blok thinking dalam giliran yang dipertahankan tetap valid selama semua hal berikut terpenuhi:

* **Permintaan compaction berjalan pada model dengan pemikiran yang dipertahankan.** Syarat ini mencakup setiap permintaan compaction sejak blok thinking dihasilkan, bukan hanya yang terbaru. Salah satu cara untuk memenuhinya adalah mengirim setiap permintaan compaction ke model yang digunakan oleh percakapan.
* **Giliran yang dipertahankan langsung mengikuti pesan yang diringkas, dan Anda mengirimnya tanpa perubahan.** Kirim setiap pesan yang dipertahankan persis seperti yang ada dalam riwayat Anda. Jangan melewatkan atau menambahkan pesan di antara pesan terakhir yang diringkas dan pesan pertama yang dipertahankan. Pesan pertama yang dipertahankan juga harus memiliki peran yang berbeda dari pesan terakhir yang diringkas, dan tidak boleh berupa pesan `role: "system"` di tengah percakapan. Jika tidak, API akan menggabungkannya ke dalam pesan terakhir yang diringkas. Salah satu cara untuk mendapatkan pesan pertama yang dipertahankan dengan benar adalah melakukan compaction tepat pada `messages` dari permintaan yang sudah Anda kirim. Giliran yang dipertahankan kemudian dimulai dengan balasan Claude terhadap permintaan tersebut.
* **`system` dan `tools` yang tidak ditandai `defer_loading: true` tidak berubah.** Keduanya sama pada permintaan compaction seperti pada permintaan yang menghasilkan thinking yang dipertahankan, dan tetap sama pada permintaan-permintaan berikutnya. [Mengubah prompt sistem atau alat](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#change-the-system-prompt-or-tools) menjelaskan cara mengubahnya dengan aman.

Jika suatu syarat tidak terpenuhi, tidak ada yang gagal saat Anda melakukan compaction, dan API tetap menerima blok tersebut pada permintaan berikutnya. Kegagalan muncul pada permintaan berikutnya yang pertama kali mengirim thinking yang dipertahankan di tempat API memberlakukan pemeriksaan: error 400 secara default, atau blok thinking dibuang jika permintaan menetapkan `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Di Message Batches API, item yang tidak menetapkan field tersebut tidak gagal. Di tempat pemeriksaan berlaku secara default, API justru membuang blok tersebut. [Apa yang dilakukan API dengan blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior) menjelaskan kedua hasil tersebut, dan [Kapan API memberlakukan pemeriksaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#enforcement) menyebutkan permintaan mana yang diperiksa.

## Melakukan compaction lagi tanpa merusak thinking yang lebih lama

Anda dapat [melakukan compaction lagi](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-again) dan mempertahankan giliran: blok baru mencakup ringkasan lama dan setiap pesan yang mengikutinya dalam permintaan compaction, dan setiap giliran yang Anda keluarkan dari permintaan tersebut menjadi giliran yang dipertahankan dari blok baru.

Syarat pertama dari [syarat untuk thinking yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid) memperhitungkan setiap compaction sejak blok thinking dihasilkan, sehingga giliran yang Anda pertahankan melalui dua compaction mengharuskan keduanya telah berjalan pada model dengan pemikiran yang dipertahankan.

Compaction yang terjadi sebelum blok thinking dihasilkan tidak diperhitungkan terhadap blok tersebut. Thinking yang dihasilkan setelah sebuah blok terpasang akan terikat pada blok tersebut, dan tetap valid melalui compaction berikutnya yang memenuhi syarat.

## Mengubah prompt sistem atau alat

Permintaan berikutnya dapat menggunakan `system` yang berbeda, `tools` yang berbeda, atau model yang berbeda dari permintaan compaction, dan API tetap menerima blok tersebut. Perubahan seperti itu dapat membuat thinking dalam giliran yang dipertahankan menjadi tidak valid, tetapi tidak memiliki efek lain.

Untuk mengubah `system` atau `tools` tanpa membuat thinking yang dipertahankan menjadi tidak valid, lakukan compaction pada seluruh percakapan terlebih dahulu, sehingga tidak ada giliran yang dipertahankan. Kemudian ubah keduanya pada permintaan berikutnya.

Untuk menambahkan instruksi atau mengubah alat yang tersedia tanpa menyentuh `system` atau `tools`, tambahkan perubahan tersebut ke `messages`, seperti yang dijelaskan dalam [Melakukan perubahan tanpa mengedit prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#replace-prefix-edits).

Pesan sistem di tengah percakapan yang berada di dalam giliran yang diringkas juga ikut diringkas, sehingga instruksi teks di dalamnya berhenti berlaku setelah pertukaran. Agar salah satunya tetap berlaku, nyatakan kembali dalam pesan `role: "system"` tepat setelah giliran `user` baru pertama yang mengikuti giliran yang dipertahankan. Perubahan alat di dalam giliran tersebut terbawa dengan sendirinya ketika permintaan compaction juga membawa `inline-tools-2026-09-15`: blok yang dikembalikan mencatat efek bersihnya dalam field `tool_changes`, jadi kirim kembali blok tersebut tanpa modifikasi. Jika blok tidak memiliki field `tool_changes`, nyatakan kembali perubahan alat tersebut dengan cara yang sama. Pesan sistem yang ditempatkan di antara blok dan giliran yang dipertahankan akan merusak thinking di dalam giliran tersebut.

## Memeriksa bahwa thinking yang dipertahankan tetap valid

Respons compaction tidak menyatakan apakah thinking yang dipertahankan tetap valid. Permintaan pertama setelah pertukaranlah yang menyatakannya. Untuk memeriksanya dalam pengujian Anda:

1. Lakukan percakapan singkat dengan thinking diaktifkan. Gunakan model tempat API menjalankan pemeriksaan (lihat [Kapan API memberlakukan pemeriksaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#enforcement)), dan gunakan model tersebut untuk setiap langkah, karena model yang tidak dapat membaca blok thinking akan membuangnya tanpa error.
2. Lakukan compaction pada giliran yang lebih lama, dan pertahankan setidaknya satu giliran yang berisi blok thinking.
3. Kirim permintaan berikutnya, dengan blok terlebih dahulu, lalu giliran yang dipertahankan, lalu pesan `user` baru, dan dengan `thinking.block_binding.prefix_mismatch_behavior` ditetapkan ke `"error"`.
4. Baca hasilnya. Respons 200 yang array `input_transformations`-nya kosong berarti tidak ada blok thinking yang gagal dalam pemeriksaan atau dibuang. Error 400 yang menyatakan bahwa blok terikat pada percakapan yang berbeda berarti ada yang gagal. Pesan tersebut dimulai dengan path dari blok pertama yang gagal, dan [Apa yang dilakukan API dengan blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior) menampilkannya secara lengkap.

Field `prefix_mismatch_behavior` memerlukan header beta `thinking-binding-controls-2026-08-01` selain [header beta `compact-2026-09-04`](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary). Menetapkan field tersebut juga mengikutsertakan permintaan ke dalam pemeriksaan pada akun yang pemeriksaannya tidak aktif secara default.

Program berikut menjalankan keempat langkah tersebut. Program ini mencetak berapa banyak blok thinking yang ada dalam giliran yang dipertahankan dan berapa banyak entri yang dimiliki `input_transformations`; tidak adanya entri berarti thinking yang dipertahankan tetap valid:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.types.beta import BetaMessageParam, BetaThinkingConfigParam

  client = anthropic.Anthropic()

  # Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim balik terhadap percakapan.
  MODEL = "claude-fable-5-1"
  BETAS = ["compact-2026-09-04", "thinking-binding-controls-2026-08-01"]
  SYSTEM = "You help plan a recipe app's release. Keep answers short."
  # Dengan "error", blok thinking yang gagal pemeriksaan membuat permintaan gagal dengan kode 400.
  THINKING: BetaThinkingConfigParam = {
      "type": "adaptive",
      "block_binding": {"prefix_mismatch_behavior": "error"},
  }

  # 1. Lakukan percakapan singkat dengan thinking aktif.
  history: list[BetaMessageParam] = [
      {"role": "user", "content": "What are the main entities in the app's data model?"}
  ]
  first = client.beta.messages.create(
      model=MODEL,
      max_tokens=8192,
      system=SYSTEM,
      betas=BETAS,
      thinking=THINKING,
      messages=history,
  )
  history += [
      {"role": "assistant", "content": first.content},
      {
          "role": "user",
          "content": "Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?",
      },
  ]
  second = client.beta.messages.create(
      model=MODEL,
      max_tokens=8192,
      system=SYSTEM,
      betas=BETAS,
      thinking=THINKING,
      messages=history,
  )
  history.append({"role": "assistant", "content": second.content})
  thinking_blocks = sum(block.type == "thinking" for block in second.content)
  print(f"Thinking blocks in the kept turn: {thinking_blocks}")

  # 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  summary = client.beta.messages.create(
      model=MODEL,
      max_tokens=4096,
      system=SYSTEM,
      betas=BETAS,
      thinking=THINKING,
      messages=history[:2],
      compaction={"type": "summarize"},
  )
  if summary.stop_reason != "compaction":
      raise SystemExit(f"No summary: {summary.stop_reason}")

  # 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
  history = [
      {"role": "assistant", "content": summary.content},
      *history[2:],
      {"role": "user", "content": "Which day should the release go out?"},
  ]
  third = client.beta.messages.create(
      model=MODEL,
      max_tokens=8192,
      system=SYSTEM,
      betas=BETAS,
      thinking=THINKING,
      messages=history,
  )

  # 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap berlaku.
  print(f"Dropped thinking blocks: {len(third.input_transformations)}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim balik terhadap percakapan.
  const model: Anthropic.Model = "claude-fable-5-1";
  const betas: Anthropic.Beta.AnthropicBeta[] = [
    "compact-2026-09-04",
    "thinking-binding-controls-2026-08-01"
  ];
  const systemPrompt = "You help plan a recipe app's release. Keep answers short.";
  // Dengan "error", blok thinking yang gagal dalam pemeriksaan membuat permintaan gagal dengan kode 400.
  const thinking: Anthropic.Beta.Messages.BetaThinkingConfigParam = {
    type: "adaptive",
    block_binding: { prefix_mismatch_behavior: "error" }
  };

  // 1. Lakukan percakapan singkat dengan thinking aktif.
  let history: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "What are the main entities in the app's data model?" }
  ];
  const first = await client.beta.messages.create({
    model,
    max_tokens: 8192,
    system: systemPrompt,
    betas,
    thinking,
    messages: history
  });
  history.push(
    { role: "assistant", content: first.content },
    {
      role: "user",
      content:
        "Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?"
    }
  );
  const second = await client.beta.messages.create({
    model,
    max_tokens: 8192,
    system: systemPrompt,
    betas,
    thinking,
    messages: history
  });
  history.push({ role: "assistant", content: second.content });
  const thinkingBlocks = second.content.filter((block) => block.type === "thinking").length;
  console.log(`Thinking blocks in the kept turn: ${thinkingBlocks}`);

  // 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  const summary = await client.beta.messages.create({
    model,
    max_tokens: 4096,
    system: systemPrompt,
    betas,
    thinking,
    messages: history.slice(0, 2),
    compaction: { type: "summarize" }
  });
  if (summary.stop_reason !== "compaction") {
    throw new Error(`No summary: ${summary.stop_reason}`);
  }

  // 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
  history = [
    { role: "assistant", content: summary.content },
    ...history.slice(2),
    { role: "user", content: "Which day should the release go out?" }
  ];
  const third = await client.beta.messages.create({
    model,
    max_tokens: 8192,
    system: systemPrompt,
    betas,
    thinking,
    messages: history
  });

  // 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap valid.
  console.log(`Dropped thinking blocks: ${third.input_transformations?.length ?? 0}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  const Model ModelId = Model.ClaudeFable5_1;
  AnthropicBeta[] betas = [AnthropicBeta.Compact2026_09_04, AnthropicBeta.ThinkingBindingControls2026_08_01];
  const string SystemPrompt = "You help plan a recipe app's release. Keep answers short.";
  // Dengan "error", blok thinking yang gagal dalam pemeriksaan membuat permintaan gagal dengan kode 400.
  BetaThinkingConfigAdaptive thinking = new()
  {
      BlockBinding = new() { PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.Error },
  };

  // 1. Lakukan percakapan singkat dengan thinking diaktifkan.
  List<BetaMessageParam> history =
  [
      new() { Role = Role.User, Content = "What are the main entities in the app's data model?" },
  ];
  var first = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = ModelId,
      MaxTokens = 8192,
      System = SystemPrompt,
      Betas = [.. betas],
      Thinking = thinking,
      Messages = history,
  });
  history.AddRange(
  [
      new()
      {
          Role = Role.Assistant,
          Content = first.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      },
      new()
      {
          Role = Role.User,
          Content = "Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?",
      },
  ]);
  var second = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = ModelId,
      MaxTokens = 8192,
      System = SystemPrompt,
      Betas = [.. betas],
      Thinking = thinking,
      Messages = history,
  });
  history.Add(new()
  {
      Role = Role.Assistant,
      Content = second.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
  });
  var thinkingBlocks = second.Content.Count(block => block.TryPickThinking(out _));
  Console.WriteLine($"Thinking blocks in the kept turn: {thinkingBlocks}");

  // 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  var summary = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = ModelId,
      MaxTokens = 4096,
      System = SystemPrompt,
      Betas = [.. betas],
      Thinking = thinking,
      Messages = history[..2],
      Compaction = new BetaCompactionConfig(), // type defaults to "summarize"
  });
  if (summary.StopReason != BetaStopReason.Compaction)
  {
      throw new InvalidOperationException($"No summary: {summary.StopReason?.Raw()}");
  }

  // 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
  history =
  [
      new()
      {
          Role = Role.Assistant,
          Content = summary.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      },
      .. history[2..],
      new() { Role = Role.User, Content = "Which day should the release go out?" },
  ];
  var third = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = ModelId,
      MaxTokens = 8192,
      System = SystemPrompt,
      Betas = [.. betas],
      Thinking = thinking,
      Messages = history,
  });

  // 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap valid.
  Console.WriteLine($"Dropped thinking blocks: {third.InputTransformations?.Count ?? 0}");
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim balik terhadap percakapan.
  const model = anthropic.ModelClaudeFable5_1
  betas := []anthropic.AnthropicBeta{
  	anthropic.AnthropicBetaCompact2026_09_04,
  	anthropic.AnthropicBetaThinkingBindingControls2026_08_01,
  }
  system := []anthropic.BetaTextBlockParam{{Text: "You help plan a recipe app's release. Keep answers short."}}
  // Dengan "error", blok thinking yang gagal dalam pemeriksaan membuat permintaan gagal dengan 400.
  thinking := anthropic.BetaThinkingConfigParamUnion{
  	OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{
  		BlockBinding: anthropic.BetaThinkingBlockBindingParam{
  			PrefixMismatchBehavior: anthropic.BetaThinkingPrefixMismatchBehaviorError,
  		},
  	},
  }

  // 1. Lakukan percakapan singkat dengan thinking aktif.
  history := []anthropic.BetaMessageParam{
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What are the main entities in the app's data model?")),
  }
  first, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     model,
  	MaxTokens: 8192,
  	System:    system,
  	Betas:     betas,
  	Thinking:  thinking,
  	Messages:  history,
  })
  if err != nil {
  	log.Fatal(err)
  }
  history = append(history,
  	first.ToParam(),
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?")),
  )
  second, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     model,
  	MaxTokens: 8192,
  	System:    system,
  	Betas:     betas,
  	Thinking:  thinking,
  	Messages:  history,
  })
  if err != nil {
  	log.Fatal(err)
  }
  history = append(history, second.ToParam())
  thinkingBlocks := 0
  for _, block := range second.Content {
  	if _, ok := block.AsAny().(anthropic.BetaThinkingBlock); ok {
  		thinkingBlocks++
  	}
  }
  fmt.Printf("Thinking blocks in the kept turn: %d\n", thinkingBlocks)

  // 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  summary, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     model,
  	MaxTokens: 4096,
  	System:    system,
  	Betas:     betas,
  	Thinking:  thinking,
  	Messages:  history[:2],
  	Compaction: anthropic.BetaCompactionConfigUnionParam{
  		OfSummarize: &anthropic.BetaSummarizeCompactionParam{},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  if summary.StopReason != anthropic.BetaStopReasonCompaction {
  	log.Fatalf("No summary: %s", summary.StopReason)
  }

  // 3. Letakkan blok di depan giliran yang dipertahankan lalu ajukan pertanyaan berikutnya.
  history = slices.Concat(
  	[]anthropic.BetaMessageParam{summary.ToParam()},
  	history[2:],
  	[]anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Which day should the release go out?"))},
  )
  third, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     model,
  	MaxTokens: 8192,
  	System:    system,
  	Betas:     betas,
  	Thinking:  thinking,
  	Messages:  history,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap valid.
  fmt.Printf("Dropped thinking blocks: %d\n", len(third.InputTransformations))
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaCompactionConfig;
  import com.anthropic.models.beta.messages.BetaContentBlock;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  static final Model MODEL = Model.CLAUDE_FABLE_5_1;
  static final List<AnthropicBeta> BETAS = List.of(
      AnthropicBeta.COMPACT_2026_09_04,
      AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01
  );
  static final String SYSTEM = "You help plan a recipe app's release. Keep answers short.";
  // Dengan "error", blok thinking yang gagal dalam pemeriksaan membuat permintaan gagal dengan kode 400.
  static final BetaThinkingConfigAdaptive THINKING = BetaThinkingConfigAdaptive.builder()
      .blockBinding(BetaThinkingBlockBinding.builder()
          .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.ERROR)
          .build())
      .build();

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      // 1. Lakukan percakapan singkat dengan thinking aktif.
      var history = new ArrayList<BetaMessageParam>();
      history.add(BetaMessageParam.builder()
          .role(BetaMessageParam.Role.USER)
          .content("What are the main entities in the app's data model?")
          .build());
      var firstParams = MessageCreateParams.builder()
          .model(MODEL)
          .maxTokens(8192)
          .system(SYSTEM)
          .betas(BETAS)
          .thinking(THINKING)
          .messages(history)
          .build();
      var first = client.beta().messages().create(firstParams);
      history.add(first.toParam());
      history.add(BetaMessageParam.builder()
          .role(BetaMessageParam.Role.USER)
          .content("Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?")
          .build());
      var secondParams = MessageCreateParams.builder()
          .model(MODEL)
          .maxTokens(8192)
          .system(SYSTEM)
          .betas(BETAS)
          .thinking(THINKING)
          .messages(history)
          .build();
      var second = client.beta().messages().create(secondParams);
      history.add(second.toParam());
      long thinkingBlocks = second.content().stream().filter(BetaContentBlock::isThinking).count();
      IO.println("Thinking blocks in the kept turn: " + thinkingBlocks);

      // 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
      var firstTurn = history.subList(0, 2);
      var summaryParams = MessageCreateParams.builder()
          .model(MODEL)
          .maxTokens(4096)
          .system(SYSTEM)
          .betas(BETAS)
          .thinking(THINKING)
          .messages(firstTurn)
          .compaction(BetaCompactionConfig.builder().build()) // type defaults to "summarize"
          .build();
      var summary = client.beta().messages().create(summaryParams);
      if (!summary.stopReason().map(BetaStopReason.COMPACTION::equals).orElse(false)) {
          throw new IllegalStateException("No summary: " + summary.stopReason().orElseThrow());
      }

      // 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
      firstTurn.clear();
      history.addFirst(summary.toParam());
      history.add(BetaMessageParam.builder()
          .role(BetaMessageParam.Role.USER)
          .content("Which day should the release go out?")
          .build());
      var thirdParams = MessageCreateParams.builder()
          .model(MODEL)
          .maxTokens(8192)
          .system(SYSTEM)
          .betas(BETAS)
          .thinking(THINKING)
          .messages(history)
          .build();
      var third = client.beta().messages().create(thirdParams);

      // 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap valid.
      IO.println("Dropped thinking blocks: " + third.inputTransformations().map(List::size).orElse(0));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaCompactionConfig;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Beta\Messages\BetaMessageParam\Role;
  use Anthropic\Beta\Messages\BetaStopReason;
  use Anthropic\Beta\Messages\BetaThinkingBlock;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;

  $client = new Client();

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  const MODEL = Model::CLAUDE_FABLE_5_1;
  const BETAS = [AnthropicBeta::COMPACT_2026_09_04, AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01];
  const SYSTEM = "You help plan a recipe app's release. Keep answers short.";
  // Dengan "error", blok thinking yang gagal dalam pemeriksaan membuat permintaan gagal dengan kode 400.
  $thinking = BetaThinkingConfigAdaptive::with(
      blockBinding: BetaThinkingBlockBinding::with(
          prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::ERROR,
      ),
  );

  // 1. Lakukan percakapan singkat dengan thinking aktif.
  $history = [
      BetaMessageParam::with(role: Role::USER, content: "What are the main entities in the app's data model?"),
  ];
  $first = $client->beta->messages->create(
      model: MODEL,
      maxTokens: 8192,
      system: SYSTEM,
      betas: BETAS,
      thinking: $thinking,
      messages: $history,
  );
  $history[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $first->content);
  $history[] = BetaMessageParam::with(
      role: Role::USER,
      content: 'Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?',
  );
  $second = $client->beta->messages->create(
      model: MODEL,
      maxTokens: 8192,
      system: SYSTEM,
      betas: BETAS,
      thinking: $thinking,
      messages: $history,
  );
  $history[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $second->content);
  $thinkingBlocks = count(array_filter($second->content, fn ($block) => $block instanceof BetaThinkingBlock));
  printf("Thinking blocks in the kept turn: %d\n", $thinkingBlocks);

  // 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  $summary = $client->beta->messages->create(
      model: MODEL,
      maxTokens: 4096,
      system: SYSTEM,
      betas: BETAS,
      thinking: $thinking,
      messages: array_slice($history, 0, 2),
      compaction: new BetaCompactionConfig(), // type defaults to 'summarize'
  );
  if ($summary->stopReason !== BetaStopReason::COMPACTION->value) {
      throw new RuntimeException("No summary: {$summary->stopReason}");
  }

  // 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
  $history = [
      BetaMessageParam::with(role: Role::ASSISTANT, content: $summary->content),
      ...array_slice($history, 2),
      BetaMessageParam::with(role: Role::USER, content: 'Which day should the release go out?'),
  ];
  $third = $client->beta->messages->create(
      model: MODEL,
      maxTokens: 8192,
      system: SYSTEM,
      betas: BETAS,
      thinking: $thinking,
      messages: $history,
  );

  // 4. Respons 200 tanpa blok yang dibuang berarti thinking yang dipertahankan tetap valid.
  printf("Dropped thinking blocks: %d\n", count($third->inputTransformations));
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Claude Fable 5.1 adalah model pertama yang memeriksa pemikiran yang dikirim kembali terhadap percakapan.
  MODEL = Anthropic::Model::CLAUDE_FABLE_5_1
  BETAS = [
    Anthropic::AnthropicBeta::COMPACT_2026_09_04,
    Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01
  ]
  SYSTEM = "You help plan a recipe app's release. Keep answers short."
  # Dengan "error", blok pemikiran yang gagal dalam pemeriksaan membuat permintaan gagal dengan kode 400.
  THINKING = Anthropic::Beta::BetaThinkingConfigAdaptive.new(
    block_binding: Anthropic::Beta::BetaThinkingBlockBinding.new(
      prefix_mismatch_behavior: Anthropic::Beta::BetaThinkingPrefixMismatchBehavior::ERROR
    )
  )

  # 1. Lakukan percakapan singkat dengan pemikiran diaktifkan.
  history = [{ role: "user", content: "What are the main entities in the app's data model?" }]
  first = client.beta.messages.create(
    model: MODEL,
    max_tokens: 8192,
    system_: SYSTEM,
    betas: BETAS,
    thinking: THINKING,
    messages: history
  )
  history += [
    { role: "assistant", content: first.content },
    {
      role: "user",
      content: "Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?"
    }
  ]
  second = client.beta.messages.create(
    model: MODEL,
    max_tokens: 8192,
    system_: SYSTEM,
    betas: BETAS,
    thinking: THINKING,
    messages: history
  )
  history << { role: "assistant", content: second.content }
  thinking_blocks = second.content.count { it.is_a?(Anthropic::Beta::BetaThinkingBlock) }
  puts "Thinking blocks in the kept turn: #{thinking_blocks}"

  # 2. Ringkas giliran pertama. Giliran kedua tidak disertakan dalam permintaan.
  summary = client.beta.messages.create(
    model: MODEL,
    max_tokens: 4096,
    system_: SYSTEM,
    betas: BETAS,
    thinking: THINKING,
    messages: history.first(2),
    compaction: { type: "summarize" }
  )
  abort "No summary: #{summary.stop_reason}" unless summary.stop_reason == :compaction

  # 3. Letakkan blok di depan giliran yang dipertahankan, lalu ajukan pertanyaan berikutnya.
  history = [
    { role: "assistant", content: summary.content },
    *history.drop(2),
    { role: "user", content: "Which day should the release go out?" }
  ]
  third = client.beta.messages.create(
    model: MODEL,
    max_tokens: 8192,
    system_: SYSTEM,
    betas: BETAS,
    thinking: THINKING,
    messages: history
  )

  # 4. Respons 200 tanpa blok yang dibuang berarti pemikiran yang dipertahankan tetap valid.
  puts "Dropped thinking blocks: #{third.input_transformations.length}"
  ```
</CodeGroup>

```text Output wrap
Thinking blocks in the kept turn: 1
Dropped thinking blocks: 0
```

Di produksi, `"drop_block"` membuat permintaan tetap berhasil ketika suatu syarat tidak terpenuhi, dan melaporkan setiap blok yang dibuang dalam `input_transformations` dengan `reason: "prefix_binding_mismatch"`. Entri yang `path`-nya berada dalam giliran yang dipertahankan berarti thinking pada giliran tersebut tidak lagi valid. [Apa yang dilakukan API dengan blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior) menjelaskan apa yang dibuang dan cara memasang peringatan untuknya.
