---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
fetched_at: 2026-09-03T02:44:34.856042Z
sha256: f6bba6a1bae60a97ea392fe74f1cff4469f3aa476b7b657b96f09ece73cfbbd5
---

---
title: Prompting Claude Fable 5.1
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
description: Perbedaan perilaku dan pola prompting untuk Claude Fable 5.1 dan Claude Mythos 5.1, mencakup effort, pembaruan progres, batching panggilan alat, riwayat percakapan, gaya penulisan, pemformatan, penyelesaian tugas, ringkasan compaction, cakupan dan cakupan pengujian, pemicuan pencarian, false positive safeguard, pengeditan file, output panjang, subagen, dan vision.
---

Untuk kemampuan model, perubahan API, harga, dan ketersediaan, lihat [Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1). Untuk teknik yang berlaku di seluruh model Claude, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Prompt Claude Fable 5 Anda yang sudah ada seharusnya berkinerja baik pada Claude Fable 5.1 tanpa perubahan, tetapi ada beberapa perbedaan perilaku yang perlu diketahui. Mulailah dengan bagian yang sesuai dengan apa yang Anda amati:

* Tidak yakin tingkat effort mana yang harus dijalankan, atau latensi dan biaya lebih tinggi daripada yang dibutuhkan tugas: [Pertimbangkan semua tingkat effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels)
* Sedikit atau tidak ada teks di antara panggilan alat: [Minta pembaruan progres yang ditujukan kepada pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates)
* Satu panggilan alat per giliran dalam loop agen: [Batch panggilan alat independen dalam loop agen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops)
* Permintaan gagal dengan `bound to a different conversation`, atau harness Anda mengedit giliran sebelumnya di antara permintaan: [Jaga riwayat percakapan agar hanya ditambahkan (append-only)](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)
* Prosa terlalu panjang dan padat: [Kepadatan tulisan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density)
* Balasan chat memiliki struktur yang lebih sedikit daripada yang dibutuhkan konten: [Pemformatan dalam chat](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#formatting-in-chat)
* Ringkasan mereproduksi kata-kata sumber tanpa menandainya sebagai kutipan: [Mengutip sumber yang diambil](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#quoting-retrieved-sources)
* Giliran berakhir sebelum pekerjaan selesai, atau model meminta izin untuk pekerjaan yang sudah Anda minta: [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#finish-the-whole-task)
* Ringkasan compaction sisi klien menghilangkan batasan, keputusan, atau detail persis: [Beri tahu model apa yang harus dipertahankan dalam ringkasan compaction](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#tell-the-model-what-to-preserve-in-compaction-summaries)
* Perbaikan atau ekstensi yang tidak diminta, atau lebih banyak file pengujian yang di-commit daripada yang dibutuhkan tugas: [Batasi perubahan dan pengujian pada apa yang diminta tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-changes-and-tests-to-what-the-task-asks-for)
* Menjawab dari memori alih-alih mencari pada effort rendah: [Pemicuan pencarian pada effort rendah](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort)
* Permintaan coding yang tidak berbahaya mengembalikan `stop_reason: "refusal"`: [Kurangi false positive safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#reduce-safeguard-false-positives)
* Seluruh file ditulis ulang untuk perubahan kecil: [Utamakan pengeditan terarah daripada penulisan ulang seluruh file](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#prefer-targeted-edits-over-whole-file-rewrites)
* Hasil kerja panjang pada effort `xhigh` atau `max` memakan waktu lama atau mencapai `max_tokens`: [Sisakan ruang untuk output panjang pada effort xhigh dan max](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#leave-room-for-long-outputs-at-xhigh-and-max-effort)
* Agen utama menganggur saat subagen berjalan: [Biarkan agen utama terus bekerja saat subagen berjalan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#let-the-lead-agent-keep-working-while-subagents-run)
* Jawaban tentang bagan dan gambar padat melewatkan detail: [Berikan alat untuk crop dan zoom pada pekerjaan vision](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#give-vision-work-tools-to-crop-and-zoom)

<Note>
  Kedua model menjalankan classifier keamanan dan dapat mengembalikan `stop_reason: "refusal"`. Lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing) dan [Kurangi false positive safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#reduce-safeguard-false-positives).
</Note>

## Pertimbangkan semua tingkat effort

Mulailah pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) default, `high`, lalu uji tingkat lainnya (`low`, `medium`, `xhigh`, dan `max`) terhadap eval Anda sendiri. Effort adalah kontrol utama untuk menyeimbangkan kecerdasan, "latency" (latensi), dan biaya pada Claude Fable 5.1. Jalankan ulang sweep tersebut meskipun Anda sudah pernah menjalankannya pada Claude Fable 5: nama tingkat effort tidak berkorespondensi dengan jumlah pemikiran yang sama di seluruh model.

Peningkatan kemampuan Claude Fable 5.1 dibandingkan Claude Fable 5 muncul di seluruh tingkat effort dan paling besar pada pengaturan yang lebih tinggi. Pada `medium`, hasilnya kira-kira sesuai dengan Claude Fable 5 dengan biaya lebih rendah, jadi turunkan ke `medium` atau `low` di mana eval Anda menunjukkan kualitas tetap terjaga. Pada `low`, Claude Fable 5.1 sering kompetitif dengan model Claude Opus dan Claude Sonnet dalam biaya per tugas sambil mencetak skor lebih tinggi, jadi sertakan model ini dalam perbandingan di mana pun Anda sebaliknya akan menjalankan model yang lebih kecil pada tingkat effort yang lebih tinggi.

Dua perilaku khusus effort memiliki bagiannya sendiri: pada `low`, Claude Fable 5.1 lebih jarang memanggil alat pencarian dan pengambilan (lihat [Pemicuan pencarian pada effort rendah](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort)), dan pada `xhigh` dan `max` model dapat berpikir lebih lama sebelum menulis hasil kerja yang panjang (lihat [Sisakan ruang untuk output panjang pada effort xhigh dan max](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#leave-room-for-long-outputs-at-xhigh-and-max-effort)).

## Minta pembaruan progres yang ditujukan kepada pengguna

Claude Fable 5.1 dapat menulis lebih sedikit pembaruan yang ditujukan kepada pengguna selama giliran pemanggilan alat yang panjang dibandingkan Claude Fable 5, terutama pada effort yang lebih tinggi dan dalam rantai alat yang lebih panjang. Pengguna melihat agen diam selama beberapa menit, atau pesan akhir yang hanya mencakup langkah terakhir alih-alih seluruh tugas.

Pertama, periksa apakah klien Anda menerima pembaruan progres sama sekali. Catatan singkat model di antara panggilan alat, apa yang baru saja ditemukannya dan apa yang akan dilakukannya selanjutnya, dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates), dan blok tersebut kosong di bawah `thinking.display` default yaitu `"omitted"`. Atur `display: "updates"` (beta, header `thinking-display-updates-2026-08-18`) dan render setiap blok `thinking` yang tidak kosong sebagai baris status, atau atur `"summarized"` untuk menerimanya bersama dengan penalaran yang diringkas. Jika Anda tidak memintanya, pembaruan model mungkin memang tidak sampai ke pengguna Anda.

Kedua, audit prompt Anda untuk instruksi yang menekan narasi. Beberapa model sebelumnya sangat bersemangat memberikan pembaruan saat bekerja, yang menyebabkan munculnya baris "system prompt" (prompt sistem) seperti "simpan semua temuan untuk respons akhir." Hapus baris seperti itu sebelum menambahkan apa pun.

Jika Anda masih menginginkan lebih banyak pembaruan, misalnya saat pair programming atau dalam pekerjaan human-in-the-loop lainnya, tambahkan baris prompt sistem singkat yang menyatakan kapan Anda menginginkan teks yang ditujukan kepada pengguna dari model dan apa yang harus dimuat setiap pembaruan:

```text wrap
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

Jika produk Anda menciutkan atau menyembunyikan output alat, beri tahu model. Jika tidak, model mungkin menjalankan perintah untuk "menunjukkan" kepada pengguna output yang tidak pernah ditampilkan UI Anda. Sampaikan catatan tersebut dalam [pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: "next_user_message"`, beta):

```text wrap
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

## Batch panggilan alat independen dalam loop agen

Claude Fable 5.1 biasanya mengeluarkan panggilan alat paralel seperti yang diharapkan: ketika sebuah permintaan menyebutkan beberapa hal untuk diambil, model mengeluarkan panggilan tersebut secara paralel. Pengecualiannya adalah loop coding dan computer-use di mana panggilan independen berikutnya tersirat dari tugas alih-alih diminta secara eksplisit (agen coding kustom, harness bash-dan-editor, computer use): di sana model mungkin mengeluarkannya satu per giliran. Ini tidak memengaruhi kualitas jawaban, tetapi setiap giliran tambahan memakan token, satu round trip, dan waktu nyata. Dorongan satu kalimat di akhir permintaan saat ini mengatasinya:

```text wrap
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

Setiap kali Anda mengirim hasil alat kembali, tambahkan kalimat itu setelah pesan pengguna tersebut sebagai [pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages): entri `role: "system"` dalam `messages` dengan `clear_at: "next_user_message"`. Setelah pesan pengguna berikutnya ada, API menghapus salinan sebelumnya, sehingga model hanya membaca yang terbaru. Pesan sistem cakupan giliran berada dalam beta dan memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-system-clear-at-2026-08-21`. Tanpa beta, tempatkan kalimat tersebut dalam blok teks setelah blok `tool_result` dalam pesan pengguna yang sama.

Tambahkan salinan baru setiap giliran dan biarkan salinan sebelumnya di tempatnya, byte demi byte. Salinan tersebut tetap berada dalam array, tetapi setelah dibersihkan model tidak melihatnya dan tidak memakan token input. Menghapus atau menulis ulangnya merupakan pengeditan terhadap giliran sebelumnya: hal itu memulai ulang [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) dari titik tersebut dan membatalkan blok thinking yang muncul setelahnya (lihat [Jaga riwayat percakapan agar hanya ditambahkan (append-only)](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)).

Loop berikut menunjukkan penempatan ini. Setiap giliran asisten dikembalikan persis seperti yang diterima, setiap giliran pengguna hanya membawa hasil alat, dan salinan baru dorongan dengan cakupan giliran mengikutinya.

<CodeGroup exclude="shell">
  ```python Python
  import anthropic
  from anthropic.types.beta import (
      BetaMessageParam,
      BetaToolParam,
      BetaToolResultBlockParam,
  )

  client = anthropic.Anthropic()

  BATCH_NUDGE = (
      "First privately list what you need next; then request every item "
      "that doesn't depend on another's result in this one response."
  )
  # In-memory files stand in for a working directory so the sample runs anywhere.
  FILES = {
      "pyproject.toml": """\
  [project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  """,
      "README.md": """\
  # demo

  A small demo project. Run `demo --help` for usage.
  """,
  }
  tools: list[BetaToolParam] = [
      {
          "name": "read_file",
          "description": "Read a UTF-8 text file from the working directory.",
          "input_schema": {
              "type": "object",
              "properties": {"path": {"type": "string"}},
              "required": ["path"],
          },
      }
  ]
  messages: list[BetaMessageParam] = [
      {"role": "user", "content": "Summarize pyproject.toml and README.md."}
  ]

  while True:
      response = client.beta.messages.create(
          model="claude-fable-5-1",
          max_tokens=16000,
          betas=["mid-conversation-system-clear-at-2026-08-21"],
          tools=tools,
          messages=messages,
      )
      # Append the assistant turn exactly as returned, thinking blocks included.
      messages.append({"role": "assistant", "content": response.content})
      if response.stop_reason != "tool_use":
          break
      tool_results: list[BetaToolResultBlockParam] = []
      for block in response.content:
          if block.type == "tool_use":
              raw_path = block.input.get("path")
              path = raw_path if isinstance(raw_path, str) else ""
              if path in FILES:
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": FILES[path],
                      }
                  )
              else:
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": f"File not found: {path}",
                          "is_error": True,
                      }
                  )
      # Send the tool results as the user turn, then a fresh copy of the nudge as a
      # turn-scoped system message. Leave earlier copies in place: the API clears them,
      # so the model sees only the newest one.
      messages.append({"role": "user", "content": tool_results})
      messages.append(
          {"role": "system", "content": BATCH_NUDGE, "clear_at": "next_user_message"}
      )

  print(next((block.text for block in response.content if block.type == "text"), ""))
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const BATCH_NUDGE =
    "First privately list what you need next; then request every item " +
    "that doesn't depend on another's result in this one response.";
  // In-memory files stand in for a working directory so the sample runs anywhere.
  const FILES = new Map<string, string>([
    [
      "pyproject.toml",
      `[project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  `,
    ],
    [
      "README.md",
      `# demo

  A small demo project. Run \`demo --help\` for usage.
  `,
    ],
  ]);
  const tools: Anthropic.Beta.Messages.BetaTool[] = [
    {
      name: "read_file",
      description: "Read a UTF-8 text file from the working directory.",
      input_schema: {
        type: "object",
        properties: { path: { type: "string" } },
        required: ["path"],
      },
    },
  ];
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Summarize pyproject.toml and README.md." },
  ];

  let response: Anthropic.Beta.Messages.BetaMessage;
  while (true) {
    response = await client.beta.messages.create({
      model: "claude-fable-5-1",
      max_tokens: 16000,
      betas: ["mid-conversation-system-clear-at-2026-08-21"],
      tools,
      messages,
    });
    // Append the assistant turn exactly as returned, thinking blocks included.
    messages.push({ role: "assistant", content: response.content });
    if (response.stop_reason !== "tool_use") {
      break;
    }
    const toolResults: Anthropic.Beta.Messages.BetaToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type !== "tool_use") {
        continue;
      }
      const { input } = block;
      const path =
        typeof input === "object" &&
        input !== null &&
        "path" in input &&
        typeof input.path === "string"
          ? input.path
          : "";
      const text = FILES.get(path);
      if (text === undefined) {
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: `File not found: ${path}`,
          is_error: true,
        });
        continue;
      }
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        content: text,
      });
    }
    // Send the tool results as the user turn, then a fresh copy of the nudge as a
    // turn-scoped system message. Leave earlier copies in place: the API clears them,
    // so the model sees only the newest one.
    messages.push({ role: "user", content: toolResults });
    messages.push({
      role: "system",
      content: BATCH_NUDGE,
      clear_at: "next_user_message",
    });
  }

  const finalText = response.content.find((block) => block.type === "text");
  console.log(finalText?.text ?? "");
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  AnthropicClient client = new();

  const string BatchNudge =
      "First privately list what you need next; then request every item "
      + "that doesn't depend on another's result in this one response.";

  // In-memory files stand in for a working directory so the sample runs anywhere.
  Dictionary<string, string> files = new()
  {
      ["pyproject.toml"] = """
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          """,
      ["README.md"] = """
          # demo

          A small demo project. Run `demo --help` for usage.
          """,
  };

  List<BetaToolUnion> tools =
  [
      new BetaTool
      {
          Name = "read_file",
          Description = "Read a UTF-8 text file from the working directory.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["path"] = JsonSerializer.SerializeToElement(new { type = "string" }),
              },
              Required = ["path"],
          },
      },
  ];

  List<BetaMessageParam> messages =
  [
      new() { Role = Role.User, Content = "Summarize pyproject.toml and README.md." },
  ];

  BetaMessage response;
  while (true)
  {
      response = await client.Beta.Messages.Create(new MessageCreateParams
      {
          Model = "claude-fable-5-1",
          MaxTokens = 16000,
          Betas = ["mid-conversation-system-clear-at-2026-08-21"],
          Tools = tools,
          Messages = messages,
      });
      // Append the assistant turn exactly as returned, thinking blocks included.
      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      });
      if (response.StopReason != BetaStopReason.ToolUse)
      {
          break;
      }
      List<BetaContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              var path = toolUse.Input.TryGetValue("path", out var pathValue)
                  && pathValue.ValueKind == JsonValueKind.String
                  ? pathValue.GetString()!
                  : "";
              if (files.TryGetValue(path, out var fileText))
              {
                  toolResults.Add(new BetaToolResultBlockParam { ToolUseID = toolUse.ID, Content = fileText });
              }
              else
              {
                  toolResults.Add(new BetaToolResultBlockParam
                  {
                      ToolUseID = toolUse.ID,
                      Content = $"File not found: {path}",
                      IsError = true,
                  });
              }
          }
      }
      // Send the tool results as the user turn, then a fresh copy of the nudge as a
      // turn-scoped system message. Leave earlier copies in place: the API clears them,
      // so the model sees only the newest one.
      messages.Add(new() { Role = Role.User, Content = toolResults });
      messages.Add(new()
      {
          Role = Role.System,
          Content = BatchNudge,
          ClearAt = ClearAt.NextUserMessage,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
          break;
      }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  const batchNudge = "First privately list what you need next; then request every item " +
  	"that doesn't depend on another's result in this one response."

  // In-memory files stand in for a working directory so the sample runs anywhere.
  var files = map[string]string{
  	"pyproject.toml": `[project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  `,
  	"README.md": `# demo

  A small demo project. Run "demo --help" for usage.
  `,
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.BetaToolUnionParam{
  		{OfTool: &anthropic.BetaToolParam{
  			Name:        "read_file",
  			Description: anthropic.String("Read a UTF-8 text file from the working directory."),
  			InputSchema: anthropic.BetaToolInputSchemaParam{
  				Properties: map[string]any{
  					"path": map[string]any{"type": "string"},
  				},
  				Required: []string{"path"},
  			},
  		}},
  	}
  	messages := []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize pyproject.toml and README.md.")),
  	}

  	var response *anthropic.BetaMessage
  	for {
  		var err error
  		response, err = client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  			Model:     "claude-fable-5-1",
  			MaxTokens: 16000,
  			Betas:     []anthropic.AnthropicBeta{"mid-conversation-system-clear-at-2026-08-21"},
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		// Append the assistant turn exactly as returned, thinking blocks included.
  		messages = append(messages, response.ToParam())
  		if response.StopReason != anthropic.BetaStopReasonToolUse {
  			break
  		}
  		var toolResults []anthropic.BetaContentBlockParamUnion
  		for _, block := range response.Content {
  			toolUse, ok := block.AsAny().(anthropic.BetaToolUseBlock)
  			if !ok {
  				continue
  			}
  			var input struct {
  				Path string `json:"path"`
  			}
  			// A missing or non-string path leaves input.Path empty, which takes the error-result branch.
  			if err := json.Unmarshal([]byte(toolUse.JSON.Input.Raw()), &input); err != nil {
  				input.Path = ""
  			}
  			text, found := files[input.Path]
  			if !found {
  				text = "File not found: " + input.Path
  			}
  			toolResults = append(toolResults, anthropic.NewBetaToolResultBlock(toolUse.ID, text, !found))
  		}
  		// Send the tool results as the user turn, then a fresh copy of the nudge as a
  		// turn-scoped system message. Leave earlier copies in place: the API clears them,
  		// so the model sees only the newest one.
  		messages = append(messages, anthropic.NewBetaUserMessage(toolResults...))
  		messages = append(messages, anthropic.BetaMessageParam{
  			Role:    anthropic.BetaMessageParamRoleSystem,
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock(batchNudge)},
  			ClearAt: anthropic.BetaMessageParamClearAtNextUserMessage,
  		})
  	}

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  			fmt.Println(textBlock.Text)
  			break
  		}
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.BetaTool.InputSchema;
  import com.anthropic.models.beta.messages.BetaToolResultBlockParam;
  import com.anthropic.models.beta.messages.BetaToolUseBlock;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  static final String BATCH_NUDGE =
      "First privately list what you need next; then request every item "
          + "that doesn't depend on another's result in this one response.";

  // In-memory files stand in for a working directory so the sample runs anywhere.
  static final Map<String, String> FILES = Map.of(
      "pyproject.toml", """
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          """,
      "README.md", """
          # demo

          A small demo project. Run `demo --help` for usage.
          """);

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaTool readFileTool = BetaTool.builder()
          .name("read_file")
          .description("Read a UTF-8 text file from the working directory.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of("path", Map.of("type", "string"))))
              .required(List.of("path"))
              .build())
          .build();
      List<BetaMessageParam> messages = new ArrayList<>();
      messages.add(BetaMessageParam.builder()
          .role(BetaMessageParam.Role.USER)
          .content("Summarize pyproject.toml and README.md.")
          .build());

      BetaMessage response;
      while (true) {
          response = client.beta().messages().create(MessageCreateParams.builder()
              .model("claude-fable-5-1")
              .maxTokens(16000)
              .addBeta("mid-conversation-system-clear-at-2026-08-21")
              .addTool(readFileTool)
              .messages(messages)
              .build());
          // Append the assistant turn exactly as returned, thinking blocks included.
          messages.add(response.toParam());
          boolean requestedTools = response.stopReason()
              .map(BetaStopReason.TOOL_USE::equals)
              .orElse(false);
          if (!requestedTools) {
              break;
          }
          List<BetaToolUseBlock> toolUses = response.content().stream()
              .flatMap(block -> block.toolUse().stream())
              .toList();
          List<BetaContentBlockParam> toolResults = new ArrayList<>();
          for (BetaToolUseBlock toolUse : toolUses) {
              Map<String, JsonValue> input =
                  (Map<String, JsonValue>) toolUse._input().asObject().orElseThrow();
              JsonValue pathValue = input.get("path");
              String path = pathValue != null && pathValue.asString().isPresent()
                  ? pathValue.asStringOrThrow()
                  : "";
              String fileText = FILES.get(path);
              BetaToolResultBlockParam.Builder result = BetaToolResultBlockParam.builder()
                  .toolUseId(toolUse.id());
              if (fileText != null) {
                  result.content(fileText);
              } else {
                  result.content("File not found: " + path).isError(true);
              }
              toolResults.add(BetaContentBlockParam.ofToolResult(result.build()));
          }
          // Send the tool results as the user turn, then a fresh copy of the nudge as a
          // turn-scoped system message. Leave earlier copies in place: the API clears them,
          // so the model sees only the newest one.
          messages.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .contentOfBetaContentBlockParams(toolResults)
              .build());
          messages.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.SYSTEM)
              .content(BATCH_NUDGE)
              .clearAt(BetaMessageParam.ClearAt.NEXT_USER_MESSAGE)
              .build());
      }

      String finalText = response.content().stream()
          .flatMap(block -> block.text().stream())
          .map(textBlock -> textBlock.text())
          .findFirst()
          .orElse("");
      IO.println(finalText);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Messages\BetaStopReason;
  use Anthropic\Client;

  $client = new Client();

  const BATCH_NUDGE = 'First privately list what you need next; then request every item '
      . "that doesn't depend on another's result in this one response.";
  // In-memory files stand in for a working directory so the sample runs anywhere.
  const FILES = [
      'pyproject.toml' => <<<'TOML'
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          TOML,
      'README.md' => <<<'MD'
          # demo

          A small demo project. Run `demo --help` for usage.
          MD,
  ];
  $tools = [
      [
          'name' => 'read_file',
          'description' => 'Read a UTF-8 text file from the working directory.',
          'input_schema' => [
              'type' => 'object',
              'properties' => ['path' => ['type' => 'string']],
              'required' => ['path'],
          ],
      ],
  ];
  $messages = [
      ['role' => 'user', 'content' => 'Summarize pyproject.toml and README.md.'],
  ];

  while (true) {
      $response = $client->beta->messages->create(
          model: 'claude-fable-5-1',
          maxTokens: 16000,
          betas: ['mid-conversation-system-clear-at-2026-08-21'],
          tools: $tools,
          messages: $messages,
      );
      // Append the assistant turn exactly as returned, thinking blocks included.
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      if ($response->stopReason !== BetaStopReason::TOOL_USE->value) {
          break;
      }
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $path = is_string($block->input['path'] ?? null) ? $block->input['path'] : '';
              if (array_key_exists($path, FILES)) {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => FILES[$path],
                  ];
              } else {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => "File not found: {$path}",
                      'is_error' => true,
                  ];
              }
          }
      }
      // Send the tool results as the user turn, then a fresh copy of the nudge as a
      // turn-scoped system message. Leave earlier copies in place: the API clears them,
      // so the model sees only the newest one.
      $messages[] = ['role' => 'user', 'content' => $toolResults];
      $messages[] = [
          'role' => 'system',
          'content' => BATCH_NUDGE,
          'clear_at' => 'next_user_message',
      ];
  }

  $textBlock = array_find($response->content, fn ($block) => $block->type === 'text');
  echo $textBlock?->text ?? '', PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  BATCH_NUDGE =
    "First privately list what you need next; then request every item " \
    "that doesn't depend on another's result in this one response."
  # File dalam memori menggantikan direktori kerja agar contoh ini dapat dijalankan di mana saja.
  FILES = {
    "pyproject.toml" => <<~TOML,
      [project]
      name = "demo"
      version = "0.1.0"
      description = "Demo project for the batching example"
    TOML
    "README.md" => <<~MD
      # demo

      A small demo project. Run `demo --help` for usage.
    MD
  }
  tools = [
    {
      name: "read_file",
      description: "Read a UTF-8 text file from the working directory.",
      input_schema: {
        type: "object",
        properties: {path: {type: "string"}},
        required: ["path"]
      }
    }
  ]
  messages = [{role: "user", content: "Summarize pyproject.toml and README.md."}]

  response = nil
  loop do
    response = client.beta.messages.create(
      model: "claude-fable-5-1",
      max_tokens: 16000,
      betas: ["mid-conversation-system-clear-at-2026-08-21"],
      tools: tools,
      messages: messages
    )
    # Tambahkan giliran asisten persis seperti yang dikembalikan, termasuk blok thinking.
    messages << {role: "assistant", content: response.content}
    break unless response.stop_reason == :tool_use

    tool_results = response.content.filter_map do |block|
      next unless block.type == :tool_use

      path = block.input[:path]
      if FILES.key?(path)
        {type: "tool_result", tool_use_id: block.id, content: FILES[path]}
      else
        {
          type: "tool_result",
          tool_use_id: block.id,
          content: "File not found: #{path}",
          is_error: true
        }
      end
    end
    # Kirim hasil alat sebagai giliran pengguna, lalu salinan baru dorongan sebagai
    # pesan sistem cakupan giliran. Biarkan salinan sebelumnya tetap ada: API menghapusnya,
    # sehingga model hanya melihat salinan yang terbaru.
    messages << {role: "user", content: tool_results}
    messages << {role: "system", content: BATCH_NUDGE, clear_at: "next_user_message"}
  end

  puts response.content.find { it.type == :text }&.text
  ```
</CodeGroup>

## Jaga riwayat percakapan agar hanya ditambahkan (append-only)

Tambahkan setiap giliran asisten ke riwayat persis seperti yang dikembalikan API, termasuk blok thinking, dan jangan mengedit giliran sebelumnya di antara permintaan. Untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, blok thinking Claude Fable 5.1 valid [hanya dalam percakapan persis yang menghasilkannya](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation): permintaan yang memutar ulang blok thinking setelah prefiksnya (prompt sistem, daftar alat, atau pesan sebelumnya mana pun) berubah akan mengembalikan 400, atau menghilangkan blok yang terdampak jika Anda mengatur `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta, header `thinking-binding-controls-2026-08-01`). Model mendatang diperkirakan akan menerapkan pemeriksaan ini untuk semua akun, jadi adopsi pola ini sekarang meskipun pemeriksaan ini belum diberlakukan untuk akun Anda saat ini.

Pengeditan riwayat yang memicu pemeriksaan ini adalah pengeditan yang sama yang memulai ulang [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching): menyisipkan dan menghapus pengingat per giliran, meringkas giliran lama di tempat, atau mengubah prompt sistem di tengah sesi. Kirim pengingat per giliran sebagai [pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages), ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih menulis ulang `system` atau `tools`, dan biarkan [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server atau [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) melakukan pemangkasan apa pun. Jika Anda melakukan compaction di klien, bentuk paling sederhana adalah mengganti seluruh riwayat dengan satu pesan ringkasan ditambah giliran pengguna baru dan tidak memutar ulang apa pun lainnya: tidak ada blok thinking yang terbawa, sehingga tidak ada yang gagal, dan model berpikir dari awal pada percakapan yang telah di-compact (lihat [Compaction kustom di sisi klien](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#custom-compaction-on-the-client)).

Untuk menemukan pengeditan yang sudah dilakukan harness Anda, jalankan sesi dengan `prefix_mismatch_behavior: "drop_block"` dan catat `input_transformations`, seperti dijelaskan dalam [Cara mengetahui apakah integrasi Anda terdampak](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted), atau tangkap permintaan persis yang dikirimnya selama beberapa giliran normal dan konfirmasikan bahwa permintaan berurutan identik byte demi byte hingga giliran yang ditambahkan.

## Kepadatan tulisan

Tulisan Claude Fable 5.1 secara umum merupakan peningkatan dari model Claude sebelumnya, dengan lebih sedikit frasa klise dan lebih sedikit jargon yang tidak dijelaskan. Namun, dalam beberapa kasus, prosanya lebih padat daripada Claude Fable 5: kalimat lebih panjang dan lebih sedikit jeda paragraf. Instruksi yang mendefinisikan anti-pola tersebut, yaitu prosa yang dibuat-buat, membantu. Tambahkan ke pesan pengguna (lebih disukai) atau prompt sistem:

```text wrap
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

Versi singkatnya juga cenderung berhasil:

```text wrap
Please remove all mannered prose.
```

## Pemformatan dalam chat

Model sebelumnya terlalu banyak menggunakan bullet dan bold dalam chat, dan banyak prompt membawa aturan anti-pemformatan yang ditulis untuk menekannya. Claude Fable 5.1 condong ke arah sebaliknya: model ini lebih jarang menggunakan bold dan lebih kecil kemungkinannya menggunakan header, daftar, atau tanda kutip. Jika prompt Anda berisi bahasa anti-pemformatan, hapus atau ganti dengan aturan yang menyatakan kapan pemformatan tertentu sesuai, seperti berikut:

```text wrap
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

## Mengutip sumber yang diambil

Saat meringkas dokumen, Claude Fable 5.1 lebih mungkin dibandingkan Claude Fable 5 untuk mereproduksi bagian teks sumber tanpa menandainya sebagai kutipan. Untuk mengatasinya, tambahkan satu contoh lengkap respons yang benar ke prompt sistem: permintaan pengguna, responsnya, dan satu kalimat yang menjelaskan mengapa respons tersebut benar.

```text wrap
<example>
<user>look up how the Riverton Ledger and the Coast Dispatch each covered the Harbor Bridge closure and compare their reporting</user>
<response>
[web_search: Harbor Bridge closure Riverton Ledger]
[web_search: Harbor Bridge closure Coast Dispatch]
Both outlets agree on the basics: the bridge closed on March 3 after inspectors found cracked welds, and the state expects repairs to take about eight months. Where they differ is emphasis. The Ledger treats it as a local-economy story. The Dispatch frames it as a funding failure; its editorial calls the closure "entirely foreseeable." Read together, the Ledger explains who is affected now and the Dispatch explains how it came to this — neither account alone gives the whole picture.
</response>
<rationale>CORRECT: The response is organized around where the two outlets agree and differ, not as a walk through either article. Each outlet's reporting is conveyed in one or two sentences of the assistant's own indirect speech. One short marked phrase from one source; every other claim is reworded. The response is still specific and complete.</rationale>
</example>
```

Ganti dua baris `[web_search: ...]` dengan nama alat Anda sendiri, sehingga model membacanya sebagai output alat bertemplat alih-alih teks literal untuk dikeluarkan.

## Selesaikan seluruh tugas

Claude Fable 5.1 dapat mengeksekusi tugas yang sangat panjang tanpa banyak panduan tentang metodologi, terutama ketika tujuannya jelas. Namun, pada beban kerja asinkron yang kompleks, dorong model agar tidak mengakhiri gilirannya sebelum pekerjaan selesai. Tanpa dorongan tersebut, model terkadang mendeskripsikan apa yang akan dilakukannya selanjutnya alih-alih melakukannya ("Next, I'll …") atau berhenti untuk meminta izin atas langkah yang sudah dicakup permintaan awal ("Shall I apply this?"). Pengguna harus membalas "continue" atau "go ahead," yang cocok untuk pair programming dan pekerjaan human-in-the-loop lainnya tetapi tidak memanfaatkan kemampuan jangka panjang penuh model.

Dua tambahan prompt sistem bersama-sama memitigasi hal ini. Terapkan keduanya. Jika Anda perlu membatasi panjang prompt, gunakan hanya yang pertama, yang mempertahankan sebagian besar efeknya. Yang pertama memberi tahu model untuk tidak bertanya tentang pekerjaan yang sudah diminta dan untuk melaksanakan langkah berikutnya yang telah dinyatakannya:

```text wrap
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

Kalimat pembuka, yang memberi tahu model bahwa pengguna tidak sedang mengamati, membawa sebagian besar efeknya. Pertahankan seperti yang tertulis. Jika produk Anda membutuhkan model untuk berhenti demi konfirmasi tertentu, tambahkan satu kalimat setelahnya yang mencantumkannya. Blok ini juga dapat membuat model lebih kecil kemungkinannya bertanya tentang permintaan yang ambigu, jadi periksa trade-off tersebut pada tugas Anda sendiri.

Yang kedua mendefinisikan permintaan pengguna sebagai cakupan hasil kerja:

```text wrap
# Delivering work
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

## Beri tahu model apa yang harus dipertahankan dalam ringkasan compaction

Claude Fable 5.1 merespons dengan baik ketika diberi tahu secara eksplisit apa yang harus dipertahankan ringkasannya saat percakapan panjang di-compact. [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server sudah melakukan ini. Jika Anda melakukan compaction di sisi klien, gunakan instruksi peringkasan berikut:

```text wrap
Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped.
```

## Batasi perubahan dan pengujian pada apa yang diminta tugas

Ketika diminta mengimplementasikan fitur yang bersifat terbuka, Claude Fable 5.1 memberikan apa yang diminta dan terkadang lebih: model mungkin memperbaiki kode di sekitarnya, memperluas perilaku yang tidak disebutkan tugas, atau meng-commit lebih banyak file pengujian daripada yang dibutuhkan perubahan tersebut. Model merespons dengan baik terhadap instruksi eksplisit tentang apa yang harus ditinggalkan. Dengan instruksi berikut, tambahan yang tidak diminta dan kode pengujian yang di-commit berkurang secara substansial tanpa perubahan terukur pada keberhasilan tugas:

```text wrap
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

## Pemicuan pencarian pada effort rendah

Pada effort `low`, Claude Fable 5.1 lebih kecil kemungkinannya daripada Claude Fable 5 untuk memanggil alat pencarian atau pengambilan, dan lebih mungkin menjawab dari memori. Dalam beberapa kasus, perbaikan paling sederhana adalah menaikkan effort untuk giliran yang terpengaruh alih-alih seluruh percakapan. Lihat [Ubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#changing-effort-mid-conversation).

Dalam kasus lain, dorongan prompt ke arah verifikasi membantu. Dalam prompt sistem, nyatakan bahwa mengenali sebuah nama tidak sama dengan mengetahui keadaannya saat ini, dan bahwa nama seperti itu harus dicari sebagaimana pengguna menuliskannya:

```text wrap
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

## Kurangi false positive safeguard

Classifier keamanan Claude Fable 5.1 menghasilkan lebih sedikit false positive dibandingkan Claude Fable 5 saat peluncuran, dan menemukan kerentanan dalam kode sumber diizinkan. False positive masih terjadi, dan permintaan yang diblokir mengembalikan `stop_reason: "refusal"` (lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing)). Tiga situasi membuatnya lebih mungkin terjadi:

* **Frasa pemeriksaan kompilasi:** Alih-alih "Apakah program ini bisa dikompilasi tanpa error?", tanyakan "Apakah ada bug di program ini?"
* **Bahasa pemrograman yang kurang dikenal:** Berikan model konteks tentang apa bahasa tersebut dan cara kerjanya, misalnya dengan memberinya akses ke dokumentasi bahasa tersebut.
* **Base64 dalam output alat:** Alat yang mengembalikan data berenkode base64 ke dalam konteks model dapat memicu false positive, jadi menghapusnya adalah perbaikan yang direkomendasikan.

## Utamakan pengeditan terarah daripada penulisan ulang seluruh file

Jika Claude Fable 5.1 menulis ulang seluruh file untuk perubahan kecil, tambahkan instruksi berikut ke prompt sistem atau pesan pengguna pertama. Claude Fable 5.1 lebih mungkin dibandingkan Claude Fable 5 untuk menulis ulang seluruh file teks alih-alih melakukan pengeditan terarah. File yang dihasilkan biasanya sama, tetapi kecuali file tersebut pendek atau sebagian besarnya berubah, penulisan ulang memakan lebih banyak token output dan waktu. Instruksi ini mengembalikan Claude Fable 5.1 agar sejalan dengan Claude Fable 5 untuk perubahan kecil dan menengah.

```text wrap
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

## Sisakan ruang untuk output panjang pada effort xhigh dan max

Pada effort `xhigh` dan terutama `max`, Claude Fable 5.1 dapat berpikir lebih lama sebelum mulai menulis balasannya. Ketika satu permintaan meminta hasil kerja yang panjang, seperti penulisan ulang penuh dokumen yang panjang, model mungkin menyusun sebagian besar hasil kerja tersebut dalam thinking-nya lalu menuliskannya lagi sebagai balasan, yang berarti waktu tunggu lebih lama dan lebih banyak token output. Pendekatan paling sederhana adalah menjalankan permintaan seperti ini pada `high`, titik awal yang direkomendasikan, dan beralih ke `xhigh` atau `max` hanya di mana Anda telah mengukur peningkatan kualitas (lihat [Pertimbangkan semua tingkat effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels)). Jika Anda menjalankannya pada `xhigh` atau `max`:

* Atur `max_tokens` untuk menyisakan ruang bagi thinking dan balasan, bukan hanya panjang balasan yang Anda harapkan.
* Tambahkan catatan berikut di akhir pesan pengguna. Catatan ini membuat thinking jauh lebih pendek pada permintaan prosa dan kode. Ganti `[max_tokens]` dengan nilai `max_tokens` aktual permintaan, misalnya 64.000.

```text wrap
Everything Claude produces in one reply, including any reasoning or drafting it does before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so Claude doesn't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, Claude spends extra effort on understanding the request, checking the inputs Claude's answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. If Claude plans well then it should not need to draft its output multiple times (and Claude is pretty good at planning, so this should not be an issue).
```

## Biarkan agen utama terus bekerja saat subagen berjalan

Jika agen coding Anda mengizinkan Claude Fable 5.1 mendelegasikan pekerjaan ke subagen, jangan paksa agen utama untuk berhenti dan menunggu masing-masing subagen. Pada tugas coding, membiarkan agen utama melanjutkan saat subagen berjalan menurunkan rata-rata waktu penyelesaian dengan kualitas, penggunaan token, dan biaya yang serupa. Untuk menyiapkannya:

* Buat alat yang memulai subagen langsung kembali (return) tanpa menunggu hasilnya.
* Teruskan hasil setiap subagen kembali ke agen utama dalam pesan `user` berikutnya setelah siap.
* Berikan agen utama alat terpisah yang dapat dipanggilnya ketika ingin menunggu hasil.

Model masih sering memilih untuk menunggu. Penghematan waktu berasal dari run di mana model melanjutkan pekerjaan lain.

## Berikan alat untuk crop dan zoom pada pekerjaan vision

Claude Fable 5.1 memiliki kemampuan vision yang lebih baik secara bawaan, dan pada input visual yang kompleks seperti bagan yang padat, model melakukan pekerjaan terbaiknya ketika dapat menganalisis, meng-crop, dan memverifikasi secara visual apa yang dilihatnya secara iteratif. Untuk mendapatkan manfaat penuh, jalankan model sebagai agen dengan akses ke container yang menyimpan gambar atau video mentah dan memiliki library pemrosesan gambar dasar (seperti PIL dan OpenCV) yang sudah terinstal. Jika menjalankan container terlalu membebani, alat pemotongan gambar saja sudah memberikan sebagian besar peningkatannya: alat yang mengembalikan wilayah gambar yang dipilih, di-crop dan diperbesar, memungkinkan model memeriksa detail tertentu secara lebih mendalam dan menskalakan komputasi test-time dengan token gambar. [Resep alat crop](https://platform.claude.com/cookbook/multimodal-crop-tool) memiliki definisi yang berfungsi.
