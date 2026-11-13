---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: b0b53806d0c41c1e3c7c49a097f1db02eff9dada16b4d0e9970730092747bf0b
---

---
title: Compaction dan pemikiran yang dipertahankan
url: https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks
description: Kapan thinking dalam giliran yang dipertahankan setelah compaction, atau setelah ringkasan atau pemotongan Anda sendiri, tetap valid pada model dengan pemikiran yang dipertahankan, dan cara memeriksanya.
featureMetadata:
  status: beta
  betaHeader: compact-2026-09-04
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
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Google managed): beta
    Microsoft Foundry: beta
---

Lewati halaman ini kecuali Anda mengirim “thinking blocks” (blok pemikiran) kembali ke model dengan [“preserved thinking” (pemikiran yang dipertahankan)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan mempertahankan giliran setelah blok “compaction” (pemadatan), atau setelah ringkasan atau pemotongan Anda sendiri. “Kept turns” (giliran yang dipertahankan) adalah giliran yang mengikuti blok tersebut. Giliran tersebut adalah giliran terbaru yang Anda keluarkan dari permintaan compaction, seperti dalam [Compaction yang mempertahankan giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/compaction-keep-recent-turns), atau giliran yang tiba saat API sedang menulis ringkasan, seperti dalam [Compaction di latar belakang](https://platform.claude.com/docs/id/build-with-claude/compaction-background).

Model dengan pemikiran yang dipertahankan memeriksa blok thinking sebelumnya terhadap percakapan yang menghasilkannya. Ringkasan menggantikan sebagian percakapan tersebut, tetapi [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) menerima pertukaran itu ketika API yang menulis ringkasannya, sehingga thinking dalam giliran yang dipertahankan dapat tetap valid.

## Syarat agar thinking yang dipertahankan tetap valid

Blok thinking dalam giliran yang dipertahankan tetap valid selama semua hal berikut terpenuhi:

* **Permintaan compaction berjalan pada model dengan pemikiran yang dipertahankan.** Syarat ini mencakup setiap permintaan compaction sejak blok thinking dihasilkan, bukan hanya yang terbaru. Salah satu cara untuk memenuhinya adalah mengirim setiap permintaan compaction ke model yang digunakan oleh percakapan.
* **Giliran yang dipertahankan langsung mengikuti pesan yang diringkas, dan Anda mengirimnya tanpa perubahan.** Kirim setiap pesan yang dipertahankan persis seperti yang ada dalam riwayat Anda, dan jangan kirim lagi pesan yang sudah diringkas. Jangan melewatkan atau menambahkan pesan di antara pesan terakhir yang diringkas dan pesan pertama yang dipertahankan. Pesan pertama yang dipertahankan juga harus memiliki peran yang berbeda dari pesan terakhir yang diringkas, dan tidak boleh berupa pesan `role: "system"` di tengah percakapan. Jika tidak, API akan menggabungkannya ke dalam pesan terakhir yang diringkas. Salah satu cara untuk mendapatkan pesan pertama yang dipertahankan dengan benar adalah melakukan compaction tepat pada `messages` dari permintaan yang sudah Anda kirim. Giliran yang dipertahankan kemudian dimulai dengan balasan Claude terhadap permintaan tersebut.
* **`system` dan `tools` tidak berubah.** Keduanya sama pada permintaan compaction seperti pada permintaan yang menghasilkan thinking yang dipertahankan, dan tetap sama pada permintaan-permintaan berikutnya. Pengecualiannya adalah alat yang ditandai `defer_loading: true` yang belum direferensikan oleh apa pun. Untuk mengubahnya dengan aman, lihat [Mengubah prompt sistem atau alat](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#change-the-system-prompt-or-tools).

Jika suatu kondisi tidak terpenuhi, API tetap menerima blok compaction pada permintaan berikutnya. Yang gagal adalah thinking yang dipertahankan, pada permintaan berikutnya yang pertama kali mengirimkannya. Permintaan compaction menjalankan pemeriksaan prefiks pada blok thinking yang dibawanya, sehingga `system` atau `tools` yang berubah, atau pesan yang diedit, juga dapat membuat permintaan tersebut gagal. Untuk apa yang terjadi saat itu, lihat [Atur `prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls).

## Melakukan compaction lagi tanpa merusak thinking yang lebih lama

Anda dapat [melakukan compaction lagi](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#compact-again) dan mempertahankan giliran: blok baru mencakup ringkasan lama dan setiap pesan yang mengikutinya dalam permintaan compaction, dan setiap giliran yang Anda keluarkan dari permintaan tersebut menjadi giliran yang dipertahankan dari blok baru.

Agar thinking suatu giliran tetap valid melalui dua compaction, keduanya harus telah berjalan pada model dengan pemikiran yang dipertahankan.

Compaction yang terjadi sebelum blok thinking dihasilkan tidak diperhitungkan terhadap blok tersebut. Thinking yang dihasilkan setelah sebuah blok terpasang akan terikat pada blok tersebut, dan tetap valid melalui compaction berikutnya yang memenuhi syarat.

## Mengubah prompt sistem atau alat

Permintaan berikutnya dapat menggunakan `system`, `tools`, atau model lain yang mendukung compaction sesuai permintaan, dan API tetap menerima blok tersebut. Perubahan tersebut dapat membuat thinking yang dipertahankan menjadi tidak valid.

Untuk mengubah `system` atau `tools` tanpa membuat thinking yang dipertahankan menjadi tidak valid, lakukan compaction pada seluruh percakapan terlebih dahulu, sehingga tidak ada giliran yang dipertahankan. Kemudian ubah keduanya pada permintaan berikutnya.

Untuk menambahkan instruksi atau mengubah alat yang tersedia tanpa menyentuh `system` atau `tools`, tambahkan perubahan tersebut ke `messages`, seperti yang dijelaskan dalam [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions).

Giliran yang diringkas dapat mencakup pesan sistem di tengah percakapan, yaitu entri `role: "system"` dalam `messages`. Pesan-pesan tersebut ikut diringkas bersama bagian lainnya, sehingga instruksi teks dan level [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort-per-message) di dalamnya berhenti berlaku (lihat [Batasan dan interaksi dengan fitur lain](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#how-it-fits-with-the-rest-of-the-api)). Perubahan alat di dalamnya dapat terbawa:

1. Kirim header beta `inline-tools-2026-09-15` pada permintaan compaction. Blok yang dikembalikan kemudian mencatat perubahan tersebut dalam field `tool_changes`.
2. Kirim kembali blok tersebut tanpa modifikasi. API kemudian menerapkan perubahan yang tercatat pada setiap permintaan yang menyertakan blok tersebut. Jika field tersebut tidak ada, API menerima blok tersebut tetapi tidak menerapkan apa pun, jadi nyatakan kembali perubahan tersebut.
3. Kirim header yang sama pada setiap permintaan yang menyertakan blok tersebut.

Anda dapat menyatakan kembali instruksi, level effort, atau perubahan alat. Letakkan dalam pesan `role: "system"` tepat setelah pesan `user` baru pada permintaan Anda berikutnya. `messages` permintaan tersebut kemudian berjalan dengan urutan ini:

1. Blok compaction.
2. Giliran yang dipertahankan, jika ada.
3. Pesan `user` Anda.
4. Pesan `role: "system"`.

Pada permintaan berikutnya, biarkan entri-entri tersebut apa adanya, dan tambahkan giliran baru setelah pesan sistem. Jangan letakkan pesan sistem sebelum atau di antara giliran yang dipertahankan, karena di posisi itu pesan sistem membuat setiap blok thinking yang dipertahankan setelahnya menjadi tidak valid.

## Ketika kode Anda yang menulis ringkasan

Bagian ini berlaku di mana pun [pemeriksaan prefiks berjalan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#enforcement), dengan atau tanpa compaction sesuai permintaan.

Jika kode Anda yang menulis ringkasan, thinking dalam giliran yang Anda pertahankan setelahnya gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), karena ringkasan Anda menggantikan pesan-pesan yang mendahului thinking tersebut. Untuk mempertahankan thinking tersebut, biarkan API yang menulis ringkasannya.

Hal yang sama berlaku untuk giliran yang Anda pertahankan dengan [menjeda setelah compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#pausing-after-compaction) pada ambang token, giliran yang dihasilkan Claude saat kode Anda meringkas di latar belakang, dan giliran setelah pemotongan.

Hapus blok `thinking` dan [`redacted_thinking`](https://platform.claude.com/docs/id/build-with-claude/thinking#redacted-thinking-blocks) dari giliran tersebut dan pertahankan blok lainnya, atau kirim [`"drop_block"`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls) pada setiap permintaan yang menyertakannya. Apa pun caranya, Claude membaca giliran tersebut tanpa thinking itu, dan [token output dapat meningkat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost).

Jika Anda hanya mengirim ringkasan Anda dan instruksi berikutnya, sebagai satu pesan user, tidak ada thinking sebelumnya yang dikirim, dan thinking berikutnya valid.

## Memeriksa bahwa thinking yang dipertahankan tetap valid

Respons compaction tidak menyatakan apakah thinking yang dipertahankan tetap valid. Permintaan pertama setelah pertukaranlah yang menyatakannya. Untuk memeriksanya dalam pengujian Anda:

1. Lakukan percakapan singkat dengan thinking diaktifkan. Gunakan [model yang menjalankan pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#enforcement), dan gunakan model tersebut untuk setiap langkah, karena model yang tidak dapat membaca blok thinking akan tidak menyertakannya tanpa error.
2. Lakukan compaction pada giliran yang lebih lama, dan pertahankan setidaknya satu giliran yang berisi blok thinking.
3. Kirim permintaan berikutnya, dengan blok terlebih dahulu, lalu giliran yang dipertahankan, lalu pesan `user` baru, dan dengan `thinking.block_binding.prefix_mismatch_behavior` ditetapkan ke `"error"`.
4. Baca hasilnya. Respons 200 yang array `input_transformations`-nya kosong berarti tidak ada blok thinking yang gagal dalam pemeriksaan prefiks atau tidak disertakan. [Error 400](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch) yang menyatakan “the block is bound to a different conversation” berarti ada blok yang gagal dalam pemeriksaan prefiks. Pesan tersebut dimulai dengan path dari blok pertama yang gagal dalam pemeriksaan prefiks, sebagaimana ditunjukkan dalam [Kesalahan: The block is bound to a different conversation](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#prefix-mismatch-error).

Pengaturan `prefix_mismatch_behavior` memerlukan header beta `thinking-binding-controls-2026-08-01` selain [header beta `compact-2026-09-04`](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary).

Program berikut menjalankan keempat langkah tersebut. Program ini mencetak berapa banyak blok thinking yang ada dalam giliran yang dipertahankan dan berapa banyak entri yang dimiliki `input_transformations`; tidak adanya entri berarti thinking yang dipertahankan tetap valid:

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan logika yang lebih banyak daripada satu perintah shell. Gunakan Anthropic SDK untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan logika yang lebih banyak daripada satu perintah shell. Gunakan Anthropic SDK untuk menjalankannya.
  </CodeGroupItem>

  ```python Python
  from anthropic.types.beta import BetaMessageParam, BetaThinkingConfigParam

  client = anthropic.Anthropic()

  # Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  MODEL = "claude-fable-5-1"
  BETAS = ["compact-2026-09-04", "thinking-binding-controls-2026-08-01"]
  SYSTEM = "You help plan a recipe app's release. Keep answers short."
  # Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan 400.
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

  # 3. Letakkan blok di depan giliran yang dipertahankan lalu ajukan pertanyaan berikutnya.
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

  # 4. Respons 200 tanpa blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
  print(f"Dropped thinking blocks: {len(third.input_transformations or [])}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  const model: Anthropic.Model = "claude-fable-5-1";
  const betas: Anthropic.Beta.AnthropicBeta[] = [
    "compact-2026-09-04",
    "thinking-binding-controls-2026-08-01"
  ];
  const systemPrompt = "You help plan a recipe app's release. Keep answers short.";
  // Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan kode 400.
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

  // 4. Respons 200 tanpa ada blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
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
  // Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan kode 400.
  BetaThinkingConfigAdaptive thinking = new()
  {
      BlockBinding = new() { PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.Error },
  };

  // 1. Lakukan percakapan singkat dengan thinking diaktifkan.
  List<BetaMessageParam> history =
  [
      new BetaUserMessageParam { Content = "What are the main entities in the app's data model?" },
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
      new BetaAssistantMessageParam
      {
          Content = first.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      },
      new BetaUserMessageParam
      {
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
  history.Add(new BetaAssistantMessageParam
  {
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
      new BetaAssistantMessageParam
      {
          Content = summary.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      },
      .. history[2..],
      new BetaUserMessageParam { Content = "Which day should the release go out?" },
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

  // 4. Respons 200 tanpa blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
  Console.WriteLine($"Dropped thinking blocks: {third.InputTransformations?.Count ?? 0}");
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  // Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  const model = anthropic.ModelClaudeFable5_1
  betas := []anthropic.AnthropicBeta{
  	anthropic.AnthropicBetaCompact2026_09_04,
  	anthropic.AnthropicBetaThinkingBindingControls2026_08_01,
  }
  system := []anthropic.BetaTextBlockParam{{Text: "You help plan a recipe app's release. Keep answers short."}}
  // Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan 400.
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

  // 4. Respons 200 tanpa blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
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
  // Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan kode 400.
  static final BetaThinkingConfigAdaptive THINKING = BetaThinkingConfigAdaptive.builder()
      .blockBinding(BetaThinkingBlockBinding.builder()
          .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.ERROR)
          .build())
      .build();

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      // 1. Lakukan percakapan singkat dengan thinking aktif.
      var history = new ArrayList<BetaMessageParam>();
      history.add(BetaMessageParam.ofUser("What are the main entities in the app's data model?"));
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
      history.add(BetaMessageParam.ofUser(
          "Testing starts on Tuesday, March 3, 2026, takes 10 weekdays, and pauses on March 9 and March 16. On which date does it end?"));
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
      history.add(BetaMessageParam.ofUser("Which day should the release go out?"));
      var thirdParams = MessageCreateParams.builder()
          .model(MODEL)
          .maxTokens(8192)
          .system(SYSTEM)
          .betas(BETAS)
          .thinking(THINKING)
          .messages(history)
          .build();
      var third = client.beta().messages().create(thirdParams);

      // 4. Respons 200 tanpa blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
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
  // Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan 400.
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
      throw new \RuntimeException("No summary: {$summary->stopReason}");
  }

  // 3. Letakkan blok di depan giliran yang dipertahankan dan ajukan pertanyaan berikutnya.
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

  // 4. Respons 200 tanpa ada blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
  printf("Dropped thinking blocks: %d\n", count($third->inputTransformations ?? []));
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Claude Fable 5.1 adalah model pertama yang memeriksa thinking yang dikirim kembali terhadap percakapan.
  MODEL = Anthropic::Model::CLAUDE_FABLE_5_1
  BETAS = [
    Anthropic::AnthropicBeta::COMPACT_2026_09_04,
    Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01
  ]
  SYSTEM = "You help plan a recipe app's release. Keep answers short."
  # Dengan "error", blok pemikiran yang gagal dalam pemeriksaan prefiks membuat permintaan gagal dengan 400.
  THINKING = Anthropic::Beta::BetaThinkingConfigAdaptive.new(
    block_binding: Anthropic::Beta::BetaThinkingBlockBinding.new(
      prefix_mismatch_behavior: Anthropic::Beta::BetaThinkingPrefixMismatchBehavior::ERROR
    )
  )

  # 1. Lakukan percakapan singkat dengan thinking aktif.
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

  # 3. Letakkan blok di depan giliran yang dipertahankan dan ajukan pertanyaan berikutnya.
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

  # 4. Respons 200 tanpa blok yang tidak disertakan berarti thinking yang dipertahankan tetap valid.
  puts "Dropped thinking blocks: #{(third.input_transformations || []).length}"
  ```
</CodeGroup>

```text Output wrap
Thinking blocks in the kept turn: 1
Dropped thinking blocks: 0
```

Di lingkungan produksi, `"drop_block"` menjaga agar permintaan tetap berhasil ketika suatu kondisi tidak terpenuhi, dan respons mencantumkan setiap blok yang tidak disertakan dalam `input_transformations` dengan `reason: "prefix_binding_mismatch"`. Entri yang `path`-nya berada dalam giliran yang dipertahankan berarti suatu kondisi tidak terpenuhi untuk thinking pada giliran tersebut. Untuk cara membuat peringatan atas entri-entri tersebut, lihat [Pantau produksi, dan temukan penalaran yang hilang tanpa error](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#monitor). Pada Claude Sonnet 5.5 dan Claude Haiku 5.5, `block_binding` hanya berfungsi dengan `thinking: {"type": "adaptive"}`. Dengan pengaturan thinking lainnya pada model-model tersebut, pastikan setiap kondisi terpenuhi, atau hapus blok `thinking` dan `redacted_thinking` dari giliran yang dipertahankan.

## Ketersediaan

Compaction dan pemikiran yang dipertahankan dalam versi beta di model tertentu.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status | Platform cloud                                                                                                                                                                                                                                                                                                                                                                   | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `compact-2026-09-04`
