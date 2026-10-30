---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 765712f22266aa7efd10386bef44865bfd6664de77fd46706d0de341d6253c94
---

---
title: Yang baru di Claude Fable 5.1
url: https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1
description: Ikhtisar fitur baru, perubahan yang merusak kompatibilitas, dan peningkatan kemampuan di Claude Fable 5.1 dan Claude Mythos 5.1.
---

Claude Fable 5.1 memperluas Claude Fable 5 dengan harga input dan output yang sama, dengan pembacaan cache seperempat biayanya, serta menghadirkan kemampuan yang lebih kuat untuk agentic coding jangka panjang, riset multilangkah, serta pekerjaan dokumen, spreadsheet, dan slide. Untuk sebagian besar beban kerja, mulailah dengan Claude Opus 5.5 (lihat [Memilih model](https://platform.claude.com/docs/id/about-claude/models/choosing-a-model)). Gunakan Claude Fable 5.1 untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang, atau ketika eval Anda pada Claude Opus 5.5 dengan effort yang lebih tinggi masih belum memadai. Claude Mythos 5.1 menawarkan kemampuan yang sama hanya kepada organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842).

Jika Anda sudah memanggil Claude Fable 5, ada tiga perubahan yang merusak kompatibilitas: [penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#forced-tool-use-is-not-supported), [hanya Claude Fable 5.1 dan Claude Mythos 5.1 yang dapat membaca blok thinking Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#thinking-blocks-are-tied-to-the-model-that-produced-them), dan [mengedit giliran sebelumnya membuat blok thinking tidak valid](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#editing-earlier-turns-invalidates-thinking-blocks). Lima bersifat tambahan: [effort per pesan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#change-effort-mid-conversation-beta) (beta), [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#turn-scoped-system-messages-beta) (beta), [pembaruan progres yang dapat dibaca di antara panggilan alat](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#progress-updates-between-tool-calls-beta) (`display: "updates"`, beta), [harga pembacaan cache yang lebih rendah](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#pricing), dan [provenans konten](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#content-provenance).

## Model

| Model             | ID Claude API     | Deskripsi                                                                                     | Ketersediaan                                                                                                                                              |
| ----------------- | ----------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5.1  | claude-fable-5-1  | Penerus Claude Fable 5, untuk agentic coding jangka panjang, pekerjaan pengetahuan, dan riset | Semua pelanggan, di Claude API dan platform mitra                                                                                                         |
| Claude Mythos 5.1 | claude-mythos-5-1 | Kemampuan yang sama dengan Claude Fable 5.1. Penerus Claude Mythos 5.                         | Organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842) |

Claude Fable 5.1 dan Claude Mythos 5.1 memiliki spesifikasi dan harga yang sama:

* **Jendela konteks dan output:** “context window” (jendela konteks) [1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (default dan maksimum) dengan harga per token standar di seluruh jendela, dan maksimum 128k token output.
* **Thinking:** [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.
* **Harga:** sama dengan Claude Fable 5, kecuali [harga pembacaan cache yang lebih rendah](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#pricing).
* **Tokenizer:** sama dengan Claude Fable 5 (diperkenalkan bersama Claude Opus 4.7). Dibandingkan dengan model yang lebih lama dari Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Lihat [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

Untuk semua model saat ini, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Penggunaan alat paksa tidak didukung

Claude Fable 5.1 dan Claude Mythos 5.1 tidak mendukung “forced tool use” (penggunaan alat paksa). `tool_choice` yang diatur ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan 400 `invalid_request_error`:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` tidak berubah. Validasi yang sama berlaku untuk endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

Thinking selalu aktif untuk model-model ini, dan panggilan alat paksa akan melewatinya. Model akan menuliskan proses pengerjaannya ke dalam argumen alat, yang menurunkan kualitas argumen. Untuk JSON yang valid sesuai skema, pertahankan `tool_choice: {"type": "auto"}` dan atur `strict: true` dengan [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau pindahkan skema ke [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs). Agar model memanggil alat alih-alih membalas dengan teks, nyatakan dalam prompt kapan alat tersebut berlaku (misalnya, “Use the `get_weather` tool to answer”). Claude Fable 5.1 mengikuti instruksi alat yang eksplisit dengan andal.

### Hanya Claude Fable 5.1 dan Claude Mythos 5.1 yang membaca blok thinking Claude Fable 5.1

Setiap blok thinking mencatat model mana yang menghasilkannya. Claude Fable 5.1 membaca blok thinking model sebelumnya, tetapi hanya Claude Fable 5.1 dan Claude Mythos 5.1 yang membaca blok thinking Claude Fable 5.1. Percakapan yang berpindah ke Claude Fable 5.1 (dari Claude Opus 5, Claude Fable 5, atau model Claude sebelumnya) mempertahankan penalarannya. Percakapan yang berpindah dari Claude Fable 5.1 ke model lain kehilangan penalaran tersebut untuk giliran yang berjalan di sana.

Ketika permintaan membawa blok yang tidak dapat dibaca oleh model target (misalnya router atau fallback yang berganti model di tengah percakapan), API membuang blok tersebut sebelum model melihatnya. Blok yang dibuang tidak dihitung dalam `input_tokens` dan tidak ditagih. Dengan header beta `thinking-binding-controls-2026-08-01`, pembuangan dilaporkan dalam array `input_transformations` tingkat atas. Tanpa header tersebut, pembuangan terjadi secara diam-diam. Lihat [Berganti model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

### Mengedit giliran sebelumnya membuat blok thinking tidak valid

Pada Claude Fable 5.1 dan Claude Mythos 5.1, blok thinking yang Anda kirim kembali hanya tetap valid selama semua yang ada sebelumnya tidak berubah: prompt `system`, `tools`, dan setiap pesan sebelumnya. Claude Code, claude.ai, [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), dan [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) menjaga riwayat tersebut tetap utuh untuk Anda. Jika kode Anda membangun array `messages` sendiri, periksa terlebih dahulu sebelum Anda bermigrasi: [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) menjelaskan pemeriksaan prefiks dan cara mengganti setiap pengeditan.

Untuk menjaga pemikiran tetap valid sepanjang sesi yang panjang, perlakukan percakapan sebagai append-only (hanya dapat ditambahkan). Tambahkan instruksi dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Jika suatu instruksi hanya berlaku untuk satu giliran, gunakan [pesan sistem yang dibatasi pada satu giliran](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#turn-scoped-system-messages-beta) sebagai gantinya. Ubah alat dengan [perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) alih-alih mengedit `system` atau `tools`. Pangkas konteks dengan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) sisi server atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction), yang tidak dihitung sebagai pengeditan. Pola-pola ini juga menjaga [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) tetap hangat. Untuk mengetahui apakah integrasi Anda mengedit riwayat, jalankan [pemeriksaan tiga langkah](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-check-integration) dari panduan migrasi.

Perubahan berikut membatalkan setiap blok pemikiran berikutnya:

* Mengedit, mengurutkan ulang, atau menghapus giliran sebelumnya sambil mempertahankan giliran setelahnya.
* Menyisipkan teks per permintaan ke giliran sebelumnya (pengingat atau baris status) yang Anda hapus pada permintaan berikutnya.
* Membangun ulang prompt `system` tingkat atas atau array `tools` di antara permintaan dalam percakapan yang sama.
* Menggunakan URL gambar atau dokumen yang menyajikan byte berbeda pada permintaan berikutnya (pemeriksaan prefiks mencakup byte, bukan URL, sehingga URL bertanda tangan yang berganti-ganti untuk file yang sama tidak menjadi masalah)
* Menghapus blok thinking dari tengah riwayat sambil mempertahankan blok-blok setelahnya

Perubahan berikut menjaga blok-blok berikutnya tetap valid:

* Menghapus blok thinking tertua (dari awal riwayat), yang terbaru (dari akhir), atau semuanya
* Membiarkan compaction sisi server atau pengeditan konteks memangkas riwayat
* Memindahkan penanda `cache_control`
* Mengubah `effort` di antara permintaan

Ketika sebuah permintaan mengirimkan kembali blok yang tidak valid, `thinking.block_binding.prefix_mismatch_behavior` (header beta `thinking-binding-controls-2026-08-01`) menentukan apa yang terjadi. `"error"` menolak permintaan dengan error 400 yang pesannya berbunyi `The block is bound to a different conversation`. `"drop_block"` membuang blok tersebut beserta setiap blok thinking setelahnya, dan permintaan berhasil. Respons mencantumkan setiap pembuangan dalam `input_transformations` dengan `reason: "prefix_binding_mismatch"`. Ketika sebuah permintaan tidak mengatur field tersebut, API mengembalikan error 400 pada Claude Mythos 5.1. Pada Claude Fable 5.1, API mengembalikan error tersebut untuk akun yang dibuat pada atau setelah 31 Agustus 2026. [Ketika `prefix_mismatch_behavior` tidak diatur](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#enforcement) memuat tabel lengkapnya.

## Fitur baru

### Mengubah effort di tengah percakapan (beta)

Di Claude Fable 5.1 Anda dapat mengubah tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) di tengah percakapan tanpa membuat cache prompt tidak valid. Naikkan untuk langkah yang sulit dan turunkan untuk langkah rutin. Effort per pesan masih dalam beta: sertakan header beta `mid-conversation-output-config-2026-07-01`. Claude Fable 5.1 dan Claude Mythos 5.1 mendukungnya di Claude API, Claude Models on Google Cloud (Google managed), dan Amazon Bedrock. Untuk menggunakannya dengan Claude Fable 5.1 melalui [InvokeModel API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) Amazon Bedrock, kirim nilai tersebut dalam array `anthropic_beta` di body permintaan. Untuk model lain yang mendukungnya dan platform untuk masing-masing, lihat [Mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#changing-effort-mid-conversation).

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
  ant beta:messages create --beta mid-conversation-output-config-2026-07-01 <<'YAML'
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
  		{
  			Role:    anthropic.BetaMessageParamRoleAssistant,
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
  		},
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
    model: "claude-fable-5-1",
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

Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) untuk detailnya.

### Pesan sistem berlingkup giliran (beta)

[Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dapat dibatasi lingkupnya ke satu giliran. Atur `clear_at: "next_user_message"` pada pesan `role: "system"` dan teksnya membawa otoritas prompt sistem untuk giliran saat ini, lalu berhenti dirender setelah ada pesan `user` berikutnya. Pesan tetap berada di `messages` dan Anda terus mengirimkannya kembali apa adanya, sehingga tidak ada yang berubah di bagian awal percakapan. [Cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) tetap cocok, [blok thinking berikutnya tetap valid](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation), dan pesan yang sudah dibersihkan tidak memakan token input. Gunakan untuk pengingat per giliran dalam loop alat (“check your inbox before running more code”, “the user can’t see that tool output”) alih-alih menyisipkan teks ke riwayat dan menghapusnya pada permintaan berikutnya. Pesan sistem berlingkup giliran masih dalam beta: sertakan header beta `mid-conversation-system-clear-at-2026-08-21`. Lihat [Pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages).

```json
{
  "role": "system",
  "clear_at": "next_user_message",
  "content": "Results have landed in your inbox. Check it before running more code."
}
```

### Pembaruan progres di antara panggilan alat (beta)

Seperti Claude Fable 5, Claude Fable 5.1 menulis pembaruan progres singkat di antara panggilan alat tentang apa yang ditemukannya dan apa yang akan dilakukannya selanjutnya, meskipun jumlahnya lebih sedikit (lihat [Perubahan dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#changed-from-claude-fable-5)). Setiap pembaruan tiba sebagai blok `thinking` tersendiri tepat sebelum panggilan alat. Dengan `thinking.display` default `"omitted"`, blok-blok tersebut dikembalikan kosong, seperti penalaran, sehingga giliran agentik yang panjang dapat terlihat diam bagi pengguna Anda. Yang baru adalah opsi `display: "updates"`: atur dengan header beta `thinking-display-updates-2026-08-18` untuk menerima pembaruan progres sebagai teks sementara penalaran tetap tersembunyi. Setiap blok `thinking` dengan teks yang tidak kosong kemudian merupakan baris status yang dapat Anda tampilkan kepada pengguna. `"summarized"` juga mengembalikannya, bercampur dengan penalaran yang diringkas. Lihat [Pembaruan progres di antara panggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).

### Provenans konten

Teks yang dihasilkan oleh Claude Fable 5.1 dan Claude Mythos 5.1 membawa watermark teks statistik Anthropic di setiap platform tempat model tersedia. File gambar, video, dan audio yang didukung yang dihasilkan Claude (misalnya melalui [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)) membawa Content Credentials [C2PA](https://c2pa.org/) yang ditandatangani ketika Anda mengambilnya melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files) di Claude API.

Watermark tidak mengubah makna, kualitas, atau keterbacaan output. Watermark tidak menambahkan token atau karakter tersembunyi, tidak membawa informasi tentang Anda atau organisasi Anda, dan tidak memerlukan perubahan pada permintaan atau respons Anda. Untuk latar belakang, lihat [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) dan [How Claude’s text watermark works](https://www.anthropic.com/news/claude-text-watermark).

## Perbedaan perilaku

### Perubahan dari Claude Fable 5

Claude Fable 5.1 berbeda dari Claude Fable 5 dalam beberapa hal yang muncul tanpa perubahan kode apa pun. Masing-masing memiliki perbaikan prompting di [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1):

* **Pemanggilan alat paralel lebih bervariasi.** Claude Fable 5.1 mungkin mengeluarkan satu panggilan alat per giliran di mana Claude Fable 5 menggabungkan beberapa. Hal ini muncul dalam loop agen panjang di mana pembacaan independen berikutnya hanya tersirat: agen coding kustom, harness bash-dan-editor, computer use. Giliran tambahan memakan token, round trip, dan waktu nyata tetapi tidak menurunkan kualitas jawaban. Permintaan yang menyebutkan beberapa hal untuk diambil tetap berjalan secara paralel. Tambahkan instruksi batching satu baris dari [Batch independent tool calls in agent loops](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops).
* **Lebih sedikit pembaruan progres selama eksekusi alat yang panjang.** Model menulis lebih sedikit teks yang ditujukan kepada pengguna di antara panggilan alat, terutama pada effort yang lebih tinggi. Atur `thinking.display` ke `"updates"` (beta) untuk menerima [pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) yang memang ditulisnya, dan hapus baris prompt apa pun yang menyuruhnya menahan temuan untuk respons akhir. Jika UI Anda bergantung pada narasi, mintalah secara eksplisit baris pembuka, pembaruan berkala, dan rekap penutup. Lihat [Ask for user-facing progress updates](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates).
* **Lebih sering menjawab dari ingatan pada effort `low`.** Pada tingkat effort terendah, model lebih jarang memanggil alat pencarian atau pengambilan. Naikkan effort untuk giliran yang membutuhkan informasi terbaru, termasuk [di tengah percakapan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#change-effort-mid-conversation-beta), atau tambahkan dorongan verifikasi dari [Search triggering at low effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort).
* **Prosa lebih padat di beberapa tempat.** Dalam beberapa kasus prosanya lebih padat daripada Claude Fable 5, dengan kalimat yang lebih panjang dan lebih sedikit jeda paragraf. Lihat [Writing density](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density).
* **Lebih sedikit pemformatan dalam chat.** Model menggunakan huruf tebal, header, dan daftar lebih sedikit daripada model Claude sebelumnya, sehingga aturan anti-pemformatan yang ditulis untuk model-model tersebut dapat menekan struktur yang dibutuhkan konten. Lihat [Formatting in chat](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#formatting-in-chat).
* **Kutipan tanpa tanda dalam ringkasan.** Saat meringkas dokumen, model lebih cenderung mereproduksi bagian dari sumber tanpa menandainya sebagai kutipan. Lihat [Quoting retrieved sources](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#quoting-retrieved-sources).
* **Penulisan ulang seluruh file untuk perubahan kecil.** Saat mengedit file teks, model lebih cenderung menulis ulang seluruh file daripada melakukan edit yang terarah. Hasilnya biasanya sama, tetapi penulisan ulang memakan lebih banyak token output dan waktu. Lihat [Prefer targeted edits over whole-file rewrites](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#prefer-targeted-edits-over-whole-file-rewrites).

### Tidak berubah dari Claude Fable 5

Perilaku Messages API berikut dibawa dari Claude Fable 5 tanpa perubahan:

* Adaptive thinking selalu aktif. `thinking: {"type": "enabled"}` dengan `budget_tokens` dan `thinking: {"type": "disabled"}` keduanya mengembalikan error 400. Hilangkan `thinking` atau kirim `{"type": "adaptive"}`.
* `thinking.display` default ke `"omitted"`. `"summarized"` tersedia, dan chain of thought mentah tidak pernah dikembalikan.
* Penalaran di antara panggilan alat muncul dalam blok thinking alih-alih teks, dan [interleaved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) berjalan otomatis tanpa header beta.
* Prefill respons asisten mengembalikan error 400.
* Mengatur `temperature`, `top_p`, atau `top_k` mengembalikan error 400.
* Panjang prompt minimum yang dapat di-cache adalah 512 token.
* [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dan perubahan alat didukung.

## Peningkatan kemampuan

Claude Fable 5.1 meningkat dibandingkan Claude Fable 5, dan selisihnya paling besar pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih tinggi. Peningkatan terkonsentrasi di enam area:

* **Agentic coding dalam sesi panjang**, termasuk fitur multi-file, refactor dan migrasi besar, debugging, dan code review di seluruh sesi yang berjalan berjam-jam.
* **Pekerjaan pengetahuan dengan dokumen, spreadsheet, dan slide**, membawa analisis dari pertanyaan pertama hingga dokumen jadi, spreadsheet dengan formula aktif, atau slide deck yang dibangun dari halaman kosong.
* **Riset dan pencarian**, dengan akurasi lebih tinggi pada riset web multilangkah dan tugas deep-research yang menindaklanjuti apa yang ditemukan.
* **Vision**, membaca grafik padat, laporan keuangan, dan tabel bersarang dalam PDF, termasuk dengan alat crop-and-zoom pada grafik.
* **Pekerjaan konteks panjang**, bernalar dan menghubungkan detail di seluruh [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows).
* **Computer use**, mengoperasikan browser dan aplikasi desktop dengan lebih andal serta pulih dari langkah yang gagal.

Performa multibahasa setara dengan Claude Fable 5.

## Penolakan, fallback, dan penagihan

Claude Fable 5.1 menyertakan classifier keamanan yang mencakup kategori `stop_details` yang sama dengan Claude Fable 5, dan semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku. Model ini dapat mengembalikan `stop_reason: "refusal"`, jadi tangani penolakan dan konfigurasikan fallback.

* **Penolakan:** permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakan yang terpicu.
* **Fallback:** coba ulang permintaan yang ditolak pada model lain dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback), atau mekanisme coba ulang Anda sendiri. `fallbacks: "default"` (beta) mencoba ulang permintaan yang ditolak pada model yang direkomendasikan Anthropic untuk kategori tersebut. Target fallback yang diizinkan untuk Claude Fable 5.1 adalah Claude Opus 4.8 dan Claude Opus 5.
* **Penagihan:** penolakan yang tiba sebelum output apa pun ditagih jika berada dalam kategori dengan volume false positive yang rendah, untuk menggagalkan upaya mengakali pengamanan Anthropic dalam skala besar ([Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed)). Sebelum 24 September 2026, penolakan ini tidak ditagih. Penolakan di tengah stream menagih token input dan output yang sudah di-stream dengan tarif normal. Untuk Claude Fable 5.1, [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit) mengembalikan biaya cache prompt akibat berganti model.

## Harga

Claude Fable 5.1 dan Claude Mythos 5.1 memiliki harga yang sama dengan Claude Fable 5, kecuali untuk pembacaan cache (harga dalam USD):

| Input dasar | Penulisan cache 5m | Penulisan cache 1h | Pembacaan cache | Output     |
| ----------- | ------------------ | ------------------ | --------------- | ---------- |
| $10 / MTok  | $12,50 / MTok      | $20 / MTok         | $0,25 / MTok    | $50 / MTok |

Pembacaan cache (hit dan refresh) berbiaya 0,025 kali harga input dasar pada model-model ini, dibandingkan dengan 0,05 pada Claude Opus 5.5 dan Claude Sonnet 5.5, dan 0,1 pada model Claude lainnya. Sesi agentik panjang yang membaca ulang prefiks yang di-cache membayar seperempat tarif Claude Fable 5. Penulisan cache dan [panjang prompt minimum yang dapat di-cache sebesar 512 token](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) tidak berubah.

[Batch processing](https://platform.claude.com/docs/id/build-with-claude/batch-processing) berbiaya $5 USD per juta token input dan $25 USD per juta token output. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga residensi data dan alat.

## Ketersediaan

Claude Fable 5.1 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-fable-5-1`.
* **AWS:** [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-fable-5-1`, dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-fable-5-1`.
* **Google Cloud:** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), sebagai `claude-fable-5-1`, dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), sebagai `claude-fable-5-1`.
* **Microsoft Foundry:** [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), di infrastruktur Anthropic.

Claude Mythos 5.1 hanya tersedia untuk organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Untuk meminta akses, daftarlah ke program yang mencakup kasus penggunaan Anda, atau hubungi tim akun Anthropic, AWS, atau Google Cloud Anda.

Claude Fable 5.1 dan Claude Mythos 5.1 memiliki retensi data 30 hari dan tidak tersedia di bawah zero data retention kecuali diizinkan secara tegas oleh Anthropic. Keduanya merupakan [Covered Models](https://support.claude.com/en/articles/15425695), seperti Claude Fable 5 dan Claude Mythos 5. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

## Migrasi dari Claude Fable 5

Untuk bermigrasi dari Claude Fable 5, perbarui ID model Anda:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-fable-5"  # Before
  model = "claude-fable-5-1"  # After
  ```

  ```typescript TypeScript
  let model = "claude-fable-5"; // Before
  model = "claude-fable-5-1"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeFable5; // Before
  model = Model.ClaudeFable5_1; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeFable5  // Before
  model = anthropic.ModelClaudeFable5_1 // After
  ```

  ```java Java
  Model model = Model.CLAUDE_FABLE_5; // Before
  model = Model.CLAUDE_FABLE_5_1; // After
  ```

  ```php PHP
  $model = 'claude-fable-5'; // Before
  $model = 'claude-fable-5-1'; // After
  ```

  ```ruby Ruby
  model = "claude-fable-5" # Before
  model = "claude-fable-5-1" # After
  ```
</CodeGroup>

Kemudian tinjau item-item berikut:

1. Hapus `tool_choice` bertipe `any` atau `tool`. Pindahkan penegakan skema ke [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) dengan `tool_choice: {"type": "auto"}` atau ke [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).
2. Kirim kembali blok thinking tanpa perubahan dan jaga riwayat tetap append-only. Jika kode Anda membangun array `messages` sendiri, jalankan [pemeriksaan tiga langkah](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-check-integration) dari panduan migrasi. Pindahkan pengingat per giliran yang Anda sisipkan dan hapus ke [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#turn-scoped-system-messages-beta), dan pindahkan perubahan `system` dan `tools` ke pesan sistem di tengah percakapan. Pangkas konteks di sisi server, atau hapus blok thinking dari giliran yang Anda bawa melintasi ringkasan sisi klien. Kemudian atur [`prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking-controls) pada setiap permintaan produksi dan pantau `input_transformations`.
3. Setel ulang effort dari default (`high`), dan pertimbangkan [mengubahnya di tengah percakapan](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#change-effort-mid-conversation-beta) alih-alih mempertahankan satu tingkat untuk seluruh sesi.
4. Dalam loop agen, perhatikan satu panggilan alat per giliran di mana Claude Fable 5 menggabungkan beberapa, dan tambahkan catatan per giliran dari [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
5. Jalankan ulang eval Anda. Penanganan penolakan, fallback, kredit fallback, dan tokenizer dibawa tanpa perubahan. Pembacaan cache lebih murah (lihat [Harga](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#pricing)), dan perilaku default berbeda dalam hal-hal yang tercantum di [Perubahan dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#changed-from-claude-fable-5).

Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide) untuk instruksi langkah demi langkah, termasuk dari Claude Opus 5 dan model sebelumnya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan harga untuk setiap model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/fable-5-1/migration-guide">
    Bermigrasi dari Claude Fable 5, Claude Opus 5, dan model sebelumnya.
  </Card>

  <Card title="Prompting Claude Fable 5.1" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1">
    Pola prompting khusus untuk Claude Fable 5.1.
  </Card>
</CardGroup>
