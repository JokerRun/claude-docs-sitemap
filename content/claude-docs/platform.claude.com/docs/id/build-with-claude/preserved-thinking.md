---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: b8d0485e5404b398d69c400f43494d8080e20eb9688398cb5677a561e0167d1f
---

---
title: Pemikiran yang dipertahankan
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
description: Pemikiran yang dipertahankan memungkinkan model menggunakan blok pemikiran dari giliran sebelumnya hanya jika model tersebut atau model sebelumnya yang menghasilkannya dan tidak ada yang berubah sebelum blok tersebut.
---

"Preserved thinking" (pemikiran yang dipertahankan) adalah properti model Claude yang lebih baru yang melindungi dari "distillation" (distilasi). Properti ini menentukan apakah model dapat menggunakan "thinking block" (blok pemikiran) yang Anda kirim kembali dari giliran sebelumnya. Mulai dari Claude Fable 5.1, ketika blok `thinking` atau `redacted_thinking` dikirim kembali dalam sebuah permintaan, API memeriksa `signature` blok tersebut untuk dua hal:

* **Model adalah model yang menghasilkan blok tersebut, atau model yang lebih baru.** Sebuah model membaca blok pemikirannya sendiri dan blok pemikiran dari model-model sebelumnya. Claude Fable 5.1 membaca blok dari Claude Opus 5, tetapi Claude Opus 5 tidak dapat membaca blok dari Claude Fable 5.1. Jika model saat ini tidak dapat membaca sebuah blok, API membuangnya dari permintaan tersebut tanpa error. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).
* **Tidak ada yang berubah sebelum blok pemikiran.** "System prompt" (prompt sistem) `system` tingkat atas, `tools`, dan `messages` sebelum blok tersebut adalah "prefix" (prefiks)-nya. Jika prefiks berbeda dari yang Anda kirim saat blok tersebut dihasilkan, blok tersebut dan setiap blok pemikiran setelahnya menjadi tidak valid, dan API menolak permintaan dengan error 400 atau membuang blok yang tidak valid, sesuai pilihan Anda. Lihat [Menjaga prefiks tetap tidak berubah](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#prefix-check).

Pemeriksaan model berlaku untuk setiap akun. API memberlakukan pemeriksaan prefiks secara default untuk akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC. Pada akun yang lebih lama, API memberlakukan pemeriksaan prefiks hanya pada permintaan yang menetapkan `thinking.block_binding.prefix_mismatch_behavior`. **Model-model berikutnya akan memberlakukan pemeriksaan prefiks untuk semua akun**, jadi jadikan integrasi Anda "append-only" (hanya-tambah) sekarang.

## Siapa yang perlu mengubah sesuatu

Tidak ada yang berubah bagi Anda jika Claude Code, claude.ai, Claude Managed Agents, atau Claude Agent SDK yang menyusun permintaan Anda, atau jika kode Anda menjaga `system` dan `tools` tetap selama satu sesi dan hanya pernah menambahkan ke `messages`. Claude Mythos 5.1 dan model sebelum Claude Fable 5.1 tidak menjalankan pemeriksaan prefiks. Jika Anda tidak pernah mengirim kembali blok pemikiran, pemeriksaan prefiks tidak memiliki apa pun untuk ditolak, dan model tidak mendapatkan penalaran sebelumnya sama sekali.

Periksa integrasi Anda jika, di antara dua permintaan dalam satu percakapan, integrasi tersebut melakukan salah satu hal berikut. Setiap item menautkan ke apa yang harus dilakukan sebagai gantinya:

* [Menyusun ulang prompt `system`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions): tanggal, flag mode, instruksi proyek yang dibaca ulang, atau plugin atau server "Model Context Protocol", atau MCP, yang terhubung setelah giliran pertama
* [Merender ulang konteks dalam pesan pengguna pertama](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#changing-context)
* [Menghapus atau memperpendek "tool result" (hasil alat) lama, atau meng-encode ulang gambar lama](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming)
* [Meringkas atau membuang giliran lama di klien](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#custom-compaction-on-the-client) dan mempertahankan giliran terbaru beserta pemikirannya
* [Menambahkan, menghapus, atau mengedit entri di `tools`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#tool-changes)
* [Menambahkan pengingat ke giliran pengguna](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) lalu menghapus atau menulis ulangnya nanti
* [Membuang beberapa blok `thinking` dan mempertahankan blok yang lebih baru](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#append-assistant-turns-exactly-as-returned), atau menghapusnya lalu [mengembalikannya nanti](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#prefix-check)
* [Menyusun ulang sesi tersimpan dari template](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#faq) alih-alih memutar ulang apa yang telah dikirimnya

Pada akun yang lebih lama, tidak satu pun dari hal ini menghasilkan error kecuali permintaan menetapkan `prefix_mismatch_behavior`, sehingga eksekusi tanpa error dengan kunci Anda sendiri tidak menunjukkan apakah kode Anda terdampak. Jika orang menjalankan alat Anda dengan "API key" (kunci API) mereka sendiri, mereka yang memiliki akun lebih baru akan mendapatkan error 400 sebelum Anda. [Tetapkan `prefix_mismatch_behavior` dalam pengujian Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted) untuk melihat apa yang mereka lihat.

## Beralih model di tengah percakapan

Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok pemikiran yang dihasilkan oleh satu sama lain dan oleh model Claude sebelumnya. Tidak ada model sebelumnya yang membaca blok pemikiran dari Claude Fable 5.1 atau Claude Mythos 5.1.

* **Percakapan yang naik ke Claude Fable 5.1 mempertahankan penalarannya.** Blok pemikiran model sebelumnya tetap dapat dibaca, sehingga model berpikir seperti biasa sejak giliran pertama setelah peralihan.
* **Percakapan yang turun ke model sebelumnya kehilangan penalaran Claude Fable 5.1 untuk permintaan tersebut.** Ini terjadi ketika router mengirim giliran ke model yang lebih murah, setelah [fallback penolakan classifier](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback), atau selama [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback). API menghapus blok yang tidak dapat dibaca sebelum prompt mencapai model. Blok tersebut tidak ditagih dan tidak dihitung dalam `input_tokens`.

Tetap kirim riwayat lengkap pada setiap permintaan, termasuk blok pemikiran, dan biarkan API membuang apa yang tidak dapat dibaca oleh model saat ini. API tidak pernah mengedit array `messages` Anda, sehingga blok yang dibuang tetap ada dalam riwayat Anda. Ketika riwayat yang sama kembali ke Claude Fable 5.1, bloknya dapat dibaca lagi, bersama dengan pemikiran model sebelumnya. Penalaran hilang selamanya hanya jika klien Anda sendiri yang menghapus blok tersebut, misalnya harness yang menghapus pemikiran saat peralihan model atau menyusun ulang riwayat dari apa yang digunakan setiap model.

![Animasi: beralih ke Claude Opus melewati pemikiran Claude Fable 5.1 untuk giliran tersebut; saat beralih kembali, semuanya dibaca lagi](https://platform.claude.com/docs/images/preserved-thinking-model-switch.gif)

Dengan [beta header](https://platform.claude.com/docs/id/api/beta-headers) (header beta) `thinking-binding-controls-2026-08-01`, respons mencantumkan setiap blok yang dibuang dalam array `input_transformations` tingkat atas dengan `reason: "model_binding_mismatch"`:

```json
{
  "input_transformations": [
    {
      "type": "thinking_dropped",
      "path": "messages.3.content.0",
      "reason": "model_binding_mismatch"
    }
  ]
}
```

Tanpa header tersebut, pembuangan terjadi secara diam-diam. Entri ini bukan bug dalam integrasi Anda, dan `prefix_mismatch_behavior` tidak berpengaruh padanya: blok yang tidak dapat dibaca oleh model saat ini selalu dibuang.

## Menjaga prefiks tetap tidak berubah

Pada Claude Fable 5.1, blok pemikiran tetap valid hanya selama semua yang Anda kirim sebelumnya tidak berubah pada permintaan berikutnya. Prefiks yang diperiksa memiliki tiga bagian:

* Prompt `system` tingkat atas
* Kumpulan `tools`
* Setiap `message` sebelum blok tersebut

Catatan: Dengan [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) (pemadatan) sisi server, prefiks yang diperiksa dimulai dari blok compaction terbaru.

Parameter permintaan di luar ketiga field tersebut, seperti `effort`, `max_tokens`, `output_config`, `tool_choice`, dan `metadata`, bukan bagian dari pemeriksaan prefiks, begitu pula penanda `cache_control`. [Apa yang dihitung sebagai edit](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#what-counts-as-an-edit) memuat daftar lengkapnya.

Blok pemikiran sebelumnya tidak termasuk dalam prefiks, tetapi setiap blok pemikiran mencatat blok pemikiran mana yang mendahuluinya, lintas giliran. Anda dapat menghapus blok pemikiran dari awal riwayat (yang terlama terlebih dahulu), dari akhir, atau semuanya. Yang gagal adalah celah: blok pemikiran yang Anda pertahankan harus berupa rangkaian tak terputus dari urutan aslinya, sehingga menghapus satu blok dari tengah membuat blok pemikiran setelahnya tidak valid. Setelah Anda menghapus sebuah blok, biarkan tetap dihapus. Mengembalikannya membuat blok pemikiran yang dihasilkan selama blok itu tidak ada menjadi tidak valid.

Jaga `system` dan `tools` tetap selama sesi dan perlakukan `messages` sebagai append-only. Disiplin yang sama menjaga prefiks tetap stabil untuk "prompt caching" ([caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)): edit yang membuat pemikiran tidak valid adalah edit yang sama yang memulai ulang cache.

### Apa yang dilakukan API dengan blok yang tidak valid

Anda memilihnya dengan `thinking.block_binding.prefix_mismatch_behavior`:

* **`"error"` (default):** API menolak permintaan dengan 400 `invalid_request_error` yang menyebutkan blok pertama yang gagal.
* **`"drop_block"`:** API membuang setiap blok yang gagal dan setiap blok pemikiran setelahnya, dan permintaan berhasil. Blok yang dibuang tidak ditagih. Model menjawab giliran tersebut tanpa menggunakan penalaran dari blok yang dibuang, dan cache prompt dimulai ulang pada titik edit. Respons mencantumkan setiap blok yang dibuang dalam `input_transformations` (pada event `message_start` saat streaming) dengan `reason: "prefix_binding_mismatch"`.

`"drop_block"` menjaga permintaan tetap berhasil tetapi tidak memperbaiki edit tersebut. Hitung respons di setiap sesi yang `input_transformations`-nya memiliki entri `prefix_binding_mismatch`, dan buat peringatan untuknya. Di Message Batches API, item yang tidak menetapkan field tersebut akan membuang blok yang gagal alih-alih menghasilkan error, jadi tetapkan `"error"` secara eksplisit di sana jika Anda ingin item batch gagal.

Field tersebut dan array `input_transformations` sama-sama memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01`. [Tetapkan perilaku ketidakcocokan dan baca `input_transformations`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#preserved-thinking-controls) menunjukkan permintaan tersebut di setiap "software development kit" (kit pengembangan perangkat lunak), atau SDK.

Pesan 400 dimulai dengan:

```text wrap
messages.1.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

Jika permintaan tidak mengirim header beta, pesan berlanjut:

```text wrap
That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.
```

Pesan tersebut biasanya diakhiri dengan kalimat yang menyebutkan apa yang berubah, misalnya bahwa prompt `system` atau daftar `tools` berbeda dari saat blok dibuat. [Pemecahan masalah pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-block-signature) menjelaskan apa saja yang dapat disebutkan oleh kalimat tersebut.

Signature yang dirusak atau tidak dapat didekripsi adalah kegagalan yang berbeda. Kegagalan ini selalu mengembalikan 400 (``Invalid `signature` in `thinking` block`` tanpa kalimat tentang percakapan), dan `prefix_mismatch_behavior` tidak berlaku untuknya.

#### Menangani error dalam kode

Ini adalah 400 `invalid_request_error` yang ditunjukkan sebelumnya di bagian ini. Jangan mengirim ulang body yang sama: body tersebut akan gagal dengan cara yang sama setiap kali. Coba ulang sekali dengan header beta dan `prefix_mismatch_behavior: "drop_block"`, dan simpan pilihan tersebut bersama sesi sehingga setiap permintaan berikutnya juga mengirimkannya, termasuk setelah restart. Jika Anda tidak dapat mengirim header beta, hapus setiap blok `thinking` dan `redacted_thinking` dari riwayat sekali, biarkan tetap dihapus, dan lanjutkan. Kemudian perbaiki edit yang menyebabkan ketidakcocokan tersebut.

### Tetapkan perilaku ketidakcocokan dan baca `input_transformations`

[Header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01` menambahkan:

* Array `input_transformations` tingkat atas pada setiap respons
* Objek `block_binding` pada konfigurasi `thinking`, yang satu-satunya field-nya adalah `prefix_mismatch_behavior`

`block_binding` diterima bersama `thinking.type: "adaptive"` dan `thinking.type: "enabled"`. Mengirimkannya tanpa header beta mengembalikan error 400 yang pesannya diakhiri dengan `block_binding: Extra inputs are not permitted`. Model yang tidak menjalankan pemeriksaan prefiks menerima objek tersebut dan hanya melaporkan pembuangan dari pemeriksaan model, sehingga satu body permintaan berfungsi di berbagai model. Referensi API menyebut pemeriksaan prefiks sebagai pemeriksaan percakapan.

Permintaan berikut memilih untuk membuang alih-alih menolak. Pada giliran pertama tidak ada yang perlu diputar ulang, sehingga `input_transformations` dikembalikan kosong:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5-1",
      "max_tokens": 16000,
      "thinking": {
        "type": "adaptive",
        "block_binding": {
          "prefix_mismatch_behavior": "drop_block"
        }
      },
      "messages": [
        {
          "role": "user",
          "content": "What is the greatest common divisor of 1071 and 462?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta thinking-binding-controls-2026-08-01 \
    --transform '{content.#(type=="text")#.text,input_transformations}' \
    --format yaml <<'YAML'
  model: claude-fable-5-1
  max_tokens: 16000
  thinking:
    type: adaptive
    block_binding:
      prefix_mismatch_behavior: drop_block
  messages:
    - role: user
      content: What is the greatest common divisor of 1071 and 462?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5-1",
      max_tokens=16000,
      thinking={
          "type": "adaptive",
          "block_binding": {"prefix_mismatch_behavior": "drop_block"},
      },
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
      betas=["thinking-binding-controls-2026-08-01"],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)

  print(f"Input transformations: {len(response.input_transformations or [])}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5-1",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      block_binding: { prefix_mismatch_behavior: "drop_block" }
    },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ],
    betas: ["thinking-binding-controls-2026-08-01"]
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  console.log(`Input transformations: ${response.input_transformations?.length ?? 0}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(
      new()
      {
          Model = "claude-fable-5-1",
          MaxTokens = 16000,
          Thinking = new BetaThinkingConfigAdaptive
          {
              BlockBinding = new()
              {
                  PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.DropBlock,
              },
          },
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "What is the greatest common divisor of 1071 and 462?",
              },
          ],
          Betas = [AnthropicBeta.ThinkingBindingControls2026_08_01],
      }
  );

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  Console.WriteLine($"Input transformations: {response.InputTransformations?.Count ?? 0}");
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-fable-5-1",
  	MaxTokens: 16000,
  	Thinking: anthropic.BetaThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{
  			BlockBinding: anthropic.BetaThinkingBlockBindingParam{
  				PrefixMismatchBehavior: anthropic.BetaThinkingPrefixMismatchBehaviorDropBlock,
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaThinkingBindingControls2026_08_01},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  fmt.Printf("Input transformations: %d\n", len(response.InputTransformations))
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-fable-5-1")
          .maxTokens(16000L)
          .addBeta(AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01)
          .thinking(BetaThinkingConfigAdaptive.builder()
              .blockBinding(BetaThinkingBlockBinding.builder()
                  .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.DROP_BLOCK)
                  .build())
              .build())
          .addUserMessage("What is the greatest common divisor of 1071 and 462?")
          .build();

      BetaMessage response = client.beta().messages().create(params);

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
      IO.println("Input transformations: "
          + response.inputTransformations().map(List::size).orElse(0));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
  use Anthropic\Client;

  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5-1',
      maxTokens: 16000,
      thinking: BetaThinkingConfigAdaptive::with(
          blockBinding: BetaThinkingBlockBinding::with(
              prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::DROP_BLOCK,
          ),
      ),
      messages: [
          ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?'],
      ],
      betas: [AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }

  echo 'Input transformations: ', count($response->inputTransformations ?? []), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5-1",
    max_tokens: 16_000,
    thinking: {
      type: "adaptive",
      block_binding: {prefix_mismatch_behavior: "drop_block"}
    },
    messages: [
      {role: "user", content: "What is the greatest common divisor of 1071 and 462?"}
    ],
    betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end

  puts "Input transformations: #{response.input_transformations&.length || 0}"
  ```
</CodeGroup>

```text Output wrap
The greatest common divisor of 1071 and 462 is 21.
Input transformations: 0
```

Dengan header beta, setiap respons dari model yang mendukung pemikiran membawa `input_transformations`. Array ini kosong ketika tidak ada yang dibuang. Setiap entri memiliki `type: "thinking_dropped"`, `path` dari blok yang dibuang (misalnya `messages.1.content.0`), dan `reason` berupa `prefix_binding_mismatch` atau `model_binding_mismatch` (lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models)). Abaikan entri yang `type` atau `reason`-nya tidak Anda kenali, karena pemeriksaan di masa mendatang akan menambahkan nilai baru.

Saat [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming), array tersebut tiba pada objek `message` dalam event `message_start`. Setelah fallback sisi server di tengah stream, event `message_delta` terakhir membawanya lagi dengan entri dari model yang melayani. Dalam [message batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), item yang bloknya gagal dalam pemeriksaan prefiks dengan `"error"` eksplisit diselesaikan sebagai `errored`, sedangkan item yang tidak menetapkan field tersebut akan membuang blok yang gagal. Endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) menjalankan pemeriksaan prefiks yang sama dan mengembalikan 400 yang sama.

### Kapan API memberlakukan pemeriksaan

Pemeriksaan prefiks berjalan pada Claude Fable 5.1 untuk akun baru.

* **Akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC:** API memeriksa permintaan Claude Fable 5.1 dan menerapkan `"error"` kecuali Anda menetapkan `"drop_block"`. Definisi akun baru yang sama berlaku untuk Claude API dan platform cloud.
* **Akun yang lebih lama:** API memeriksa permintaan yang menetapkan `prefix_mismatch_behavior`. Parameter ini mengikutsertakan permintaan, sehingga Anda dapat melihat apa yang dilihat akun baru tanpa membuatnya.
* **Model-model berikutnya:** setiap akun, pada setiap permintaan.

Untuk mengetahui di grup mana akun Anda berada, ambil percakapan Claude Fable 5.1 yang berisi blok pemikiran, ubah sesuatu sebelum blok tersebut, dan kirimkan ke Claude Fable 5.1 tanpa header beta atau field `block_binding`. Respons 400 yang menyebutkan header tersebut berarti pemeriksaan diberlakukan secara default pada akun Anda.

### Apa yang dihitung sebagai edit

Setiap baris membandingkan dua permintaan yang berurutan:

| Perubahan di antara permintaan                                                                                                                                                                             | Blok pemikiran berikutnya                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Menambahkan pesan di akhir                                                                                                                                                                                 | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| Menambahkan alat dengan `defer_loading: true` yang belum direferensikan oleh apa pun                                                                                                                       | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| Menghapus blok `thinking` dari awal riwayat, dari akhir, atau semuanya                                                                                                                                     | Valid (model kehilangan penalaran tersebut)                                                                                                                                                                                                                                                                                                                                                                          |
| Mengubah parameter permintaan apa pun di luar `system`, `tools`, dan `messages` (`effort`, `max_tokens`, `output_config`, `tool_choice`, `metadata`, `thinking.display`, dan seterusnya)                   | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| Menambahkan, memindahkan, atau menghapus penanda `cache_control`                                                                                                                                           | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| URL bertanda tangan yang berotasi dan mengembalikan byte yang sama                                                                                                                                         | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| Compaction atau "context editing" (pengeditan konteks) sisi server menghapus atau mengganti konten                                                                                                         | Valid (pemeriksaan membandingkan apa yang Anda kirim, bukan salinan yang diedit server)                                                                                                                                                                                                                                                                                                                              |
| [Turn-scoped system message](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) (pesan sistem cakupan giliran) yang sudah dibersihkan dan dibiarkan di tempatnya | Valid                                                                                                                                                                                                                                                                                                                                                                                                                |
| Mengedit, mengurutkan ulang, atau menghapus pesan `user`, `assistant`, atau `system` sebelumnya                                                                                                            | Tidak valid, kecuali ketika blok bertanda tangan dari [on-demand compaction](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming) (compaction sesuai permintaan) menggantikan pesan yang diringkasnya, dengan ketentuan dalam [Compaction yang mempertahankan bagian akhir](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#keep-tail-compaction) |
| Merender ulang konteks yang Anda taruh di pesan pengguna pertama dengan nilai yang berubah                                                                                                                 | Tidak valid untuk setiap blok pemikiran                                                                                                                                                                                                                                                                                                                                                                              |
| Menghapus atau memperpendek `tool_result` sebelumnya, meng-encode ulang gambar sebelumnya, atau mengubah input `tool_use` sebelumnya                                                                       | Tidak valid untuk setiap blok pemikiran berikutnya                                                                                                                                                                                                                                                                                                                                                                   |
| Menambahkan blok teks ke giliran pengguna sebelumnya, atau menghapus blok yang Anda tambahkan terakhir kali                                                                                                | Tidak valid                                                                                                                                                                                                                                                                                                                                                                                                          |
| Mengubah string atau blok `system` tingkat atas                                                                                                                                                            | Tidak valid                                                                                                                                                                                                                                                                                                                                                                                                          |
| Menambahkan, menghapus, mengganti nama, atau mengedit alat di `tools`                                                                                                                                      | Tidak valid                                                                                                                                                                                                                                                                                                                                                                                                          |
| Menghapus blok `thinking` dari tengah riwayat dan mempertahankan blok yang lebih baru                                                                                                                      | Tidak valid untuk setiap blok pemikiran berikutnya                                                                                                                                                                                                                                                                                                                                                                   |
| Mengembalikan blok `thinking` yang Anda hapus pada permintaan sebelumnya                                                                                                                                   | Tidak valid untuk blok pemikiran yang dihasilkan selama blok itu tidak ada                                                                                                                                                                                                                                                                                                                                           |
| URL gambar atau dokumen yang mengembalikan byte berbeda pada permintaan berikutnya                                                                                                                         | Tidak valid                                                                                                                                                                                                                                                                                                                                                                                                          |
| Pesan cakupan giliran yang sama dihapus atau diubah kata-katanya pada permintaan berikutnya                                                                                                                | Tidak valid                                                                                                                                                                                                                                                                                                                                                                                                          |

### Periksa apakah kode Anda mengedit prefiks

Pertama, bandingkan (diff) apa yang Anda kirim. Tangkap body permintaan yang dikirim integrasi Anda selama beberapa giliran normal, termasuk compaction atau perubahan alat. Untuk setiap pasangan permintaan yang berurutan, bandingkan `system`, `tools`, dan `messages` yang sama-sama dimiliki keduanya. Semuanya harus identik hingga giliran yang baru ditambahkan.

Kemudian konfirmasikan terhadap API. Tambahkan header beta `thinking-binding-controls-2026-08-01`, tetapkan `prefix_mismatch_behavior` ke `"drop_block"`, dan jalankan sesi multi-giliran normal melalui integrasi Anda pada claude-fable-5-1. Contoh berikut menjalankan dua giliran sebagaimana seharusnya integrasi Anda bekerja: `messages` hanya bertambah, setiap giliran asisten dikirim kembali persis seperti yang dikembalikan API, termasuk blok `thinking`, dan `block_binding` ditetapkan pada setiap permintaan. Setelah setiap giliran, contoh ini mencetak jumlah blok `thinking` dalam respons dan jumlah blok yang dibuang:

<CodeGroup>
  ```bash cURL
  # Menghitung blok thinking dalam respons dan blok yang dihapus oleh API
  COUNTS='"thinking blocks: \([.content[] | select(.type == "thinking")] | length), " +
    "dropped: \(.input_transformations | length)"'

  FIRST=$(curl -s https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
    -d '{
      "model": "claude-fable-5-1",
      "max_tokens": 16000,
      "thinking": {
        "type": "adaptive",
        "block_binding": { "prefix_mismatch_behavior": "drop_block" }
      },
      "messages": [
        {
          "role": "user",
          "content": "How many positive integers below 500 have exactly 6 positive divisors?"
        }
      ]
    }')
  echo "$FIRST" | jq -r "$COUNTS"

  # Giliran 2: giliran asisten dikirim kembali persis seperti yang dikembalikan, lalu pesan pengguna berikutnya
  MESSAGES=$(jq -n --argjson first "$FIRST" '[
    {
      role: "user",
      content: "How many positive integers below 500 have exactly 6 positive divisors?"
    },
    { role: "assistant", content: $first.content },
    { role: "user", content: "How many of those are odd?" }
  ]')

  jq -n --argjson messages "$MESSAGES" '{
    model: "claude-fable-5-1",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      block_binding: { prefix_mismatch_behavior: "drop_block" }
    },
    messages: $messages
  }' | curl -s https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
    -d @- | jq -r "$COUNTS"
  ```

  ```bash CLI
  # Menghitung blok thinking dalam respons dan blok yang dibuang oleh API
  COUNTS='"thinking blocks: \([.content[] | select(.type == "thinking")] | length), " +
    "dropped: \(.input_transformations | length)"'

  FIRST=$(ant beta:messages create --beta thinking-binding-controls-2026-08-01 \
    --format json <<'YAML'
  model: claude-fable-5-1
  max_tokens: 16000
  thinking:
    type: adaptive
    block_binding:
      prefix_mismatch_behavior: drop_block
  messages:
    - role: user
      content: How many positive integers below 500 have exactly 6 positive divisors?
  YAML
  )
  echo "$FIRST" | jq -r "$COUNTS"

  # Giliran 2: giliran asisten dikirim kembali persis seperti yang dikembalikan, lalu pesan pengguna berikutnya
  ant beta:messages create --beta thinking-binding-controls-2026-08-01 \
    --format json <<YAML | jq -r "$COUNTS"
  model: claude-fable-5-1
  max_tokens: 16000
  thinking:
    type: adaptive
    block_binding:
      prefix_mismatch_behavior: drop_block
  messages:
    - role: user
      content: How many positive integers below 500 have exactly 6 positive divisors?
    - role: assistant
      content: $(echo "$FIRST" | jq -c .content)
    - role: user
      content: How many of those are odd?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  user_turns = [
      "How many positive integers below 500 have exactly 6 positive divisors?",
      "How many of those are odd?",
  ]

  # messages bertambah di setiap giliran: tiap giliran assistant dikirim kembali persis seperti yang dikembalikan
  messages = []
  for user_turn in user_turns:
      messages.append({"role": "user", "content": user_turn})
      response = client.beta.messages.create(
          model="claude-fable-5-1",
          max_tokens=16000,
          thinking={
              "type": "adaptive",
              "block_binding": {"prefix_mismatch_behavior": "drop_block"},
          },
          messages=messages,
          betas=["thinking-binding-controls-2026-08-01"],
      )
      messages.append({"role": "assistant", "content": response.content})
      thinking_blocks = sum(block.type == "thinking" for block in response.content)
      dropped = len(response.input_transformations or [])
      print(f"thinking blocks: {thinking_blocks}, dropped: {dropped}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const userTurns = [
    "How many positive integers below 500 have exactly 6 positive divisors?",
    "How many of those are odd?"
  ];

  // messages bertambah di setiap giliran: tiap giliran asisten dikirim kembali persis seperti yang dikembalikan
  const messages: Anthropic.Beta.BetaMessageParam[] = [];
  for (const userTurn of userTurns) {
    messages.push({ role: "user", content: userTurn });
    const response = await client.beta.messages.create({
      model: "claude-fable-5-1",
      max_tokens: 16000,
      thinking: {
        type: "adaptive",
        block_binding: { prefix_mismatch_behavior: "drop_block" }
      },
      messages,
      betas: ["thinking-binding-controls-2026-08-01"]
    });
    messages.push({ role: "assistant", content: response.content });
    const thinkingBlocks = response.content.filter((block) => block.type === "thinking");
    const dropped = response.input_transformations ?? [];
    console.log(`thinking blocks: ${thinkingBlocks.length}, dropped: ${dropped.length}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  string[] userTurns =
  [
      "How many positive integers below 500 have exactly 6 positive divisors?",
      "How many of those are odd?",
  ];

  // messages bertambah di setiap giliran: tiap giliran assistant dikirim kembali persis seperti yang dikembalikan
  List<BetaMessageParam> messages = [];
  foreach (var userTurn in userTurns)
  {
      messages.Add(new() { Role = Role.User, Content = userTurn });
      var response = await client.Beta.Messages.Create(
          new()
          {
              Model = "claude-fable-5-1",
              MaxTokens = 16000,
              Thinking = new BetaThinkingConfigAdaptive
              {
                  BlockBinding = new()
                  {
                      PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.DropBlock,
                  },
              },
              Messages = messages,
              Betas = [AnthropicBeta.ThinkingBindingControls2026_08_01],
          }
      );
      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      });
      var thinkingBlocks = response.Content.Count(block => block.TryPickThinking(out _));
      var dropped = response.InputTransformations?.Count ?? 0;
      Console.WriteLine($"thinking blocks: {thinkingBlocks}, dropped: {dropped}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  userTurns := []string{
  	"How many positive integers below 500 have exactly 6 positive divisors?",
  	"How many of those are odd?",
  }

  // messages bertambah di setiap giliran: tiap giliran assistant dikirim kembali persis seperti yang dikembalikan
  messages := []anthropic.BetaMessageParam{}
  for _, userTurn := range userTurns {
  	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(userTurn)))
  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     "claude-fable-5-1",
  		MaxTokens: 16000,
  		Thinking: anthropic.BetaThinkingConfigParamUnion{
  			OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{
  				BlockBinding: anthropic.BetaThinkingBlockBindingParam{
  					PrefixMismatchBehavior: anthropic.BetaThinkingPrefixMismatchBehaviorDropBlock,
  				},
  			},
  		},
  		Messages: messages,
  		Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaThinkingBindingControls2026_08_01},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	messages = append(messages, response.ToParam())
  	thinkingBlocks := 0
  	for _, block := range response.Content {
  		if block.Type == "thinking" {
  			thinkingBlocks++
  		}
  	}
  	fmt.Printf("thinking blocks: %d, dropped: %d\n", thinkingBlocks, len(response.InputTransformations))
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaContentBlock;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      List<String> userTurns = List.of(
          "How many positive integers below 500 have exactly 6 positive divisors?",
          "How many of those are odd?");

      // Daftar pesan builder bertambah di setiap giliran: tiap giliran asisten dikirim kembali persis seperti yang dikembalikan
      MessageCreateParams.Builder conversation = MessageCreateParams.builder()
          .model("claude-fable-5-1")
          .maxTokens(16000L)
          .thinking(BetaThinkingConfigAdaptive.builder()
              .blockBinding(BetaThinkingBlockBinding.builder()
                  .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.DROP_BLOCK)
                  .build())
              .build())
          .addBeta(AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01);

      for (String userTurn : userTurns) {
          conversation.addUserMessage(userTurn);
          BetaMessage response = client.beta().messages().create(conversation.build());
          conversation.addMessage(response);
          long thinkingBlocks = response.content().stream()
              .filter(BetaContentBlock::isThinking)
              .count();
          int dropped = response.inputTransformations().map(List::size).orElse(0);
          IO.println("thinking blocks: " + thinkingBlocks + ", dropped: " + dropped);
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
  use Anthropic\Client;

  $client = new Client();

  $userTurns = [
      'How many positive integers below 500 have exactly 6 positive divisors?',
      'How many of those are odd?',
  ];

  // $messages bertambah di setiap giliran: tiap giliran asisten dikirim kembali persis seperti yang dikembalikan
  $messages = [];
  foreach ($userTurns as $userTurn) {
      $messages[] = ['role' => 'user', 'content' => $userTurn];
      $response = $client->beta->messages->create(
          model: 'claude-fable-5-1',
          maxTokens: 16000,
          thinking: BetaThinkingConfigAdaptive::with(
              blockBinding: BetaThinkingBlockBinding::with(
                  prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::DROP_BLOCK,
              ),
          ),
          messages: $messages,
          betas: [AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
      );
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $thinkingBlocks = array_filter($response->content, fn ($block) => $block->type === 'thinking');
      $dropped = $response->inputTransformations ?? [];
      echo 'thinking blocks: ', count($thinkingBlocks), ', dropped: ', count($dropped), PHP_EOL;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_turns = [
    "How many positive integers below 500 have exactly 6 positive divisors?",
    "How many of those are odd?"
  ]

  # messages bertambah di setiap giliran: tiap giliran asisten dikirim kembali persis seperti yang dikembalikan
  messages = []
  user_turns.each do |user_turn|
    messages << {role: "user", content: user_turn}
    response = client.beta.messages.create(
      model: "claude-fable-5-1",
      max_tokens: 16_000,
      thinking: {
        type: "adaptive",
        block_binding: {prefix_mismatch_behavior: "drop_block"}
      },
      messages: messages,
      betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01]
    )
    messages << {role: "assistant", content: response.content}
    thinking_blocks = response.content.count { |block| block.type == :thinking }
    dropped = (response.input_transformations || []).length
    puts "thinking blocks: #{thinking_blocks}, dropped: #{dropped}"
  end
  ```
</CodeGroup>

```text Output wrap
thinking blocks: 1, dropped: 0
thinking blocks: 1, dropped: 0
```

Tidak ada giliran yang membuang blok karena tidak ada yang berubah sebelumnya. Periksa bahwa respons pertama berisi blok `thinking`. Dengan "adaptive thinking" (pemikiran adaptif), beberapa respons tidak memilikinya. Jika tidak ada respons dalam sesi yang memilikinya, tidak ada yang perlu diperiksa dan jumlah yang dibuang adalah 0 apa pun yang Anda ubah, jadi jalankan contoh tersebut lagi.

Catat `input_transformations` pada setiap giliran integrasi Anda sendiri. Ketika API membuang sebuah blok, entrinya terlihat seperti berikut:

```json
{
  "input_transformations": [
    {
      "type": "thinking_dropped",
      "path": "messages.1.content.0",
      "reason": "prefix_binding_mismatch"
    }
  ]
}
```

* **Kosong pada setiap giliran dalam sesi yang berisi blok `thinking`:** integrasi Anda menjaga prefiks tetap utuh.
* **`reason: "prefix_binding_mismatch"`:** sesuatu sebelum blok di `path` berubah sejak permintaan sebelumnya. Bandingkan `system`, `tools`, dan `messages` hingga giliran tersebut untuk menemukannya, atau kirim ulang permintaan dengan `"error"`: 400 biasanya diakhiri dengan kalimat yang menyebutkan apa yang berubah. Kemudian temukan pengganti yang sesuai di [Melakukan perubahan tanpa mengedit prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#replace-prefix-edits).
* **`reason: "model_binding_mismatch"`:** percakapan berpindah ke model yang tidak dapat membaca blok model sebelumnya. Ini bukan edit prefiks. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

Untuk melihat kegagalan secara sengaja, kirim giliran ketiga dari contoh sebelumnya dan tambahkan prompt `system` hanya pada permintaan tersebut, sehingga berbeda dari dua permintaan pertama, yang tidak memilikinya. Dengan `"drop_block"`, jumlah yang dibuang tidak lagi 0: respons memiliki satu entri untuk setiap blok pemikiran dalam riwayat, masing-masing dengan `reason: "prefix_binding_mismatch"`. Dengan `"error"`, permintaan mengembalikan 400 yang dijelaskan di [Apa yang dilakukan API dengan blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior), dan kalimat terakhirnya menyebutkan prompt `system`. Di tab cURL dan "command-line interface" (antarmuka baris perintah), atau CLI, hapus filter `jq` untuk melihat body error. Jika jumlahnya masih 0, tidak ada yang perlu diperiksa: pastikan bahwa modelnya adalah claude-fable-5-1, bahwa permintaan menetapkan `block_binding`, bahwa riwayat yang Anda kirim berisi blok `thinking`, dan bahwa dua permintaan pertama tidak memiliki prompt `system`.

Dua giliran biasa jarang menunjukkan masalah. Jalankan sesi melalui setiap skenario berikut, dengan `"error"` ditetapkan sehingga regresi menggagalkan "continuous integration" (integrasi berkelanjutan), atau CI, Anda:

* Compaction atau pemangkasan sisi klien yang pertama
* Alat, plugin, atau server MCP yang terhubung setelah giliran pertama
* Perubahan mode atau instruksi
* Loop alat yang panjang, jika Anda menambahkan pengingat atau memperpendek hasil alat lama
* Peralihan ke model lain dan kembali lagi
* Penyimpanan, restart, dan melanjutkan sesi pada tanggal berikutnya

## Melakukan perubahan tanpa mengedit prefiks

Setiap edit prefiks yang umum memiliki pengganti yang memberikan informasi yang sama kepada model dan membiarkan byte sebelumnya tidak berubah, sehingga pemikiran berikutnya tetap valid. Temukan edit yang dilakukan kode Anda saat ini di kolom pertama:

| Alih-alih                                                                                                                       | Gunakan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Header beta                                                               |
| ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Menyusun ulang prompt `system` tingkat atas                                                                                     | [Mid-conversation system message](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions) (pesan sistem di tengah percakapan)                                                                                                                                                                                                                                                                                                                                                                   | Tidak ada                                                                 |
| Merender ulang konteks dalam pesan pengguna pertama Anda (lingkungan, tanggal, memori, instruksi proyek) pada setiap permintaan | Render sekali dan kirim ulang tanpa perubahan. Ketika sesuatu berubah, [taruh versi baru di giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#changing-context)                                                                                                                                                                                                                                                                                                                            | Tidak ada                                                                 |
| Menghapus atau memperpendek konten `tool_result` lama, atau meng-encode ulang gambar lama, secara langsung di tempatnya         | Perpendek hasil alat atau perkecil resolusi gambar sebelum pertama kali Anda mengirimkannya, bukan setelahnya. Untuk menghapus hasil lama nanti, [pangkas konteks di server](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming) dengan `clear_tool_uses_20250919`                                                                                                                                                                                                                      | `context-management-2025-06-27`                                           |
| Menyisipkan pengingat dan menghapusnya pada permintaan berikutnya                                                               | [Pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) (`clear_at: "next_user_message"`)                                                                                                                                                                                                                                                                                                                                                                      | `mid-conversation-system-clear-at-2026-08-21`                             |
| Menambahkan atau menghapus entri di `tools`                                                                                     | [Blok `tool_addition` dan `tool_removal`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#tool-changes)                                                                                                                                                                                                                                                                                                                                                                                                   | `mid-conversation-tool-changes-2026-07-01`                                |
| Mengubah `output_config.effort` tingkat atas (memulai ulang cache, tidak memengaruhi pemikiran)                                 | [`output_config` per pesan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#effort-changes)                                                                                                                                                                                                                                                                                                                                                                                                               | `mid-conversation-output-config-2026-07-01`                               |
| Membuang atau meringkas giliran lama di klien                                                                                   | [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming) untuk mempertahankan giliran terbaru beserta pemikirannya, [compaction atau pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming) sisi server lainnya, atau [compaction sisi klien](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#custom-compaction-on-the-client) yang tidak mempertahankan pemikiran usang | `compact-2026-09-04` (tidak tersedia di Amazon Bedrock atau Google Cloud) |
| URL gambar atau dokumen yang byte-nya berubah di antara permintaan                                                              | [`file_id` dari Files API](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#files-by-id), atau base64                                                                                                                                                                                                                                                                                                                                                                                                      | Tidak ada                                                                 |

Semua ini mengasumsikan Anda [mengirim kembali giliran asisten persis seperti yang dikembalikan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#append-assistant-turns-exactly-as-returned). Pesan sistem di tengah percakapan, pesan sistem cakupan giliran, dan perubahan alat tidak tersedia di setiap model: [Pesan sistem dan perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) mencantumkan model yang menerimanya. Jika kode Anda melayani beberapa model, tetap edit prompt `system` tingkat atas untuk model yang tidak menerimanya.

Untuk menggunakan beberapa beta dalam satu permintaan, gabungkan nilainya dalam satu header `anthropic-beta`. Nama beta sama di Amazon Bedrock dan Google Cloud di mana pun beta tersebut tersedia di sana (lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers)):

```text wrap
anthropic-beta: thinking-binding-controls-2026-08-01,mid-conversation-system-clear-at-2026-08-21,mid-conversation-tool-changes-2026-07-01
```

### Kirim kembali giliran asisten persis seperti yang dikembalikan

Simpan array `content` dari setiap respons dan kirim kembali tanpa perubahan sebagai giliran asisten: setiap jenis blok, dalam urutan saat diterima, termasuk blok `thinking` yang field `thinking`-nya kosong. Serializer yang membuang jenis blok yang tidak dikenal, membuang field kosong, atau mengurutkan ulang blok akan mengedit prefiks untuk setiap giliran berikutnya.

Pada Claude Fable 5.1, field `thinking` kosong secara default dan `signature` membawa penalaran, sehingga serializer yang melewati blok kosong akan menghapus pemikiran. Jika serializer menghapus semuanya, tidak ada yang gagal dan model kehilangan penalaran sebelumnya pada setiap giliran. Jika Anda mem-parsing stream sendiri, pertahankan blok tersebut bahkan ketika tidak ada teks pemikiran yang tiba: blok dibuka, menerima `signature`-nya dalam event `signature_delta`, lalu ditutup. Blok yang dikirim kembali dengan `signature` kosong akan gagal.

### Menambahkan instruksi dengan pesan sistem di tengah percakapan

Beberapa harness menyusun ulang prompt `system` tingkat atas pada setiap permintaan untuk membawa waktu saat ini, anggaran token, flag mode, atau konteks proyek yang baru ditemukan. Hal itu membuat setiap blok pemikiran dalam percakapan menjadi tidak valid. Sebagai gantinya, bekukan `system` di awal sesi. Ketika sesuatu berubah, tambahkan [pesan `role: "system"`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) pada titik di `messages` tempat perubahan tersebut mulai berlaku:

```json
{
  "role": "system",
  "content": "The user switched the workspace to read-only mode. Do not write files until told otherwise."
}
```

Model memperlakukan pesan ini dengan otoritas prompt sistem, dan semua yang ada sebelumnya tetap tidak berubah. Dalam loop alat, tempatkan pesan setelah pesan pengguna `tool_result`, jangan pernah di antara `tool_use` asisten dan `tool_result`-nya (lihat [Batasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Setelah dikirim, pesan tersebut menjadi bagian dari prefiks untuk pemikiran berikutnya: biarkan di tempatnya pada permintaan berikutnya.

### Menaruh konteks yang berubah di giliran terbaru

Beberapa harness menaruh blok lingkungan di pesan pengguna pertama (direktori kerja, branch, tanggal, memori, instruksi proyek) dan merendernya lagi pada setiap permintaan. Ketika nilai apa pun berubah, `messages[0]` berubah, dan setiap blok pemikiran dalam percakapan menjadi tidak valid. Render blok tersebut sekali dan kirim ulang apa adanya. Ketika sebuah nilai berubah, sampaikan di giliran terbaru: tambahkan blok teks ke pesan pengguna yang akan Anda kirim, atau tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions) jika perubahan tersebut berasal dari Anda sebagai operator.

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "Environment update: the current branch is now release-2."
    },
    { "type": "text", "text": "Run the tests again." }
  ]
}
```

Setelah dikirim, blok teks tersebut menjadi bagian dari prefiks untuk pemikiran berikutnya: biarkan di tempatnya pada permintaan berikutnya.

### Kirim pengingat per giliran sebagai pesan sistem bercakupan giliran

Edit prefiks yang umum adalah dorongan per giliran: baris seperti "request independent reads together" atau "you haven't updated the user in a while" yang ditambahkan kode Anda setelah setiap batch hasil alat. Agar pengingat tidak menumpuk, kirim setiap dorongan sebagai [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dengan `clear_at: "next_user_message"`, yang ditempatkan setelah pesan pengguna `tool_result`. `clear_at` memerlukan header beta `mid-conversation-system-clear-at-2026-08-21`. Array `messages` berikut adalah permintaan setelah dua panggilan alat beserta hasilnya. `messages[3]` adalah dorongan dari permintaan sebelumnya, yang dibiarkan di tempatnya, dan `messages[6]` adalah salinan untuk permintaan ini:

```json
[
  { "role": "user", "content": "Fix the failing test." },
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "", "signature": "..." },
      {
        "type": "tool_use",
        "id": "toolu_01",
        "name": "read_file",
        "input": { "path": "tests/test_auth.py" }
      }
    ]
  },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "toolu_01", "content": "..." }]
  },
  {
    "role": "system",
    "clear_at": "next_user_message",
    "content": "Request every independent read in one turn."
  },
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "", "signature": "..." },
      {
        "type": "tool_use",
        "id": "toolu_02",
        "name": "read_file",
        "input": { "path": "src/auth.py" }
      }
    ]
  },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "toolu_02", "content": "..." }]
  },
  {
    "role": "system",
    "clear_at": "next_user_message",
    "content": "Request every independent read in one turn."
  }
]
```

Pesan pengguna yang hanya berisi blok `tool_result` dihitung sebagai "next user message", sehingga `messages[3]` sudah dibersihkan. Pesan tersebut tidak menambahkan apa pun pada apa yang dilihat model dan tidak memakan token input, tetapi karena masih ada dalam array, pemikiran di `messages[4]` tetap valid. `messages[6]` adalah salinan yang dilihat model pada giliran ini. Pada permintaan berikutnya, pertahankan keduanya di tempatnya dan tambahkan salinan baru setelah pesan `tool_result` berikutnya.

### Menambahkan atau menghapus alat dengan `tool_addition` dan `tool_removal`

Mengedit array `tools` di tengah sesi membuat blok pemikiran yang dipertahankan menjadi tidak valid. Sebagai gantinya, deklarasikan setiap alat yang mungkin dibutuhkan sesi di `tools` pada permintaan pertama dan jangan pernah mengubah array tersebut. Untuk mengubah alat mana yang dapat digunakan model mulai dari titik tertentu, tambahkan pesan `role: "system"` yang membawa blok `tool_removal` atau `tool_addition`. Ini adalah [perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) dan memerlukan header beta `mid-conversation-tool-changes-2026-07-01`. Misalnya, untuk menarik alat berbahaya setelah peralihan mode:

```json
{
  "role": "system",
  "content": [
    { "type": "tool_removal", "tool": { "type": "tool_reference", "name": "delete_branch" } },
    { "type": "text", "text": "Branch deletion is disabled for the rest of this session." }
  ]
}
```

Untuk menawarkan alat di kemudian hari, deklarasikan alat tersebut di `tools` dengan `defer_loading: true` agar model tidak melihatnya pada awalnya. Ketika alat tersebut tersedia, tambahkan blok `tool_addition`:

```json
{
  "role": "system",
  "content": [
    { "type": "tool_addition", "tool": { "type": "tool_reference", "name": "deploy" } },
    { "type": "text", "text": "Authentication succeeded. Deployment is now available." }
  ]
}
```

Terkadang Anda tidak dapat mendeklarasikan alat di awal karena Anda belum mengetahui skemanya. Server MCP yang ditemukan saat runtime adalah kasus yang umum. Tambahkan alat tersebut ke `tools` dengan `defer_loading: true`, lalu tawarkan dengan blok `tool_addition`. Menambahkan alat yang ditangguhkan itu aman: pemeriksaan prefiks mengabaikan alat yang ditangguhkan hingga blok `tool_addition` mereferensikannya, sehingga pemikiran sebelumnya tetap valid. Menambahkan alat tanpa `defer_loading: true` mengubah prefiks dan membuat pemikiran sebelumnya tidak valid.

Pesan `role: "system"` yang membawa blok-blok ini menjadi bagian dari prefiks untuk pemikiran berikutnya. Biarkan pesan tersebut di tempatnya pada permintaan berikutnya.

### Mengubah effort dengan `output_config` per pesan

Mengubah `output_config.effort` tingkat atas di antara permintaan tidak membuat pemikiran menjadi tidak valid, karena "effort" (tingkat upaya) bukan bagian dari prefiks. Namun, mengubah effort tingkat atas memang memulai ulang cache prompt. Pada Claude Fable 5.1, gunakan [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) sebagai gantinya: tambahkan pesan `role: "system"` dengan `content` kosong dan level yang baru. Ini memerlukan header beta `mid-conversation-output-config-2026-07-01`.

```json
{ "role": "system", "content": [], "output_config": { "effort": "low" } }
```

Level baru berlaku mulai giliran `user` berikutnya. Setelah dikirim, pesan tersebut menjadi bagian dari `messages` dan karenanya bagian dari prefiks untuk pemikiran berikutnya: biarkan di tempatnya pada permintaan berikutnya, dan tambahkan pesan lain untuk mengubah effort lagi.

### Memangkas konteks di server

Edit prefiks umum lainnya adalah pemangkasan sisi klien: membuang atau meringkas giliran terlama dan mempertahankan giliran terbaru secara verbatim. Blok pemikiran dari giliran yang dipertahankan dihasilkan saat riwayat yang dihapus masih ada, sehingga blok tersebut gagal dalam pemeriksaan. Padanan sisi server tidak dihitung sebagai edit, karena pemeriksaan membandingkan percakapan sebagaimana yang Anda kirim:

* [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) meringkas giliran lama menjadi blok compaction ketika konteks mendekati ambang batas yang Anda tetapkan, dan prefiks yang diperiksa dimulai ulang dari blok tersebut. [Parameter `instructions`](https://platform.claude.com/docs/id/build-with-claude/compaction#custom-summarization-instructions)-nya menerima prompt peringkasan Anda sendiri, seperti "pertahankan setiap ticker, ukuran posisi, dan asumsi yang dinyatakan". [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction#compact-on-demand-with-the-compaction-parameter) (beta) mengembalikan ringkasan dari permintaan terpisah, yang dapat [berjalan di latar belakang](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#background-compaction). Kirim `"compaction": {"type": "summarize"}` dalam body permintaan, dan respons akan membawa satu blok `compaction`, yang berisi ringkasan dan signature, alih-alih balasan. Compaction sesuai permintaan tersedia di Claude API tetapi tidak di Amazon Bedrock atau Google Cloud, dan memerlukan header beta `compact-2026-09-04` pada permintaan ringkasan dan pada setiap permintaan berikutnya yang membawa blok tersebut. Anda mengirim blok tersebut sebagai pengganti pesan yang diringkasnya. Pemeriksaan menerima pertukaran tersebut, sehingga giliran yang Anda pertahankan dapat tetap valid beserta pemikirannya, dengan ketentuan dalam [Compaction yang mempertahankan bagian akhir](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#keep-tail-compaction).
* [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) menghapus hasil alat lama atau blok pemikiran lama berdasarkan aturan, yang terlama terlebih dahulu. Strateginya adalah `clear_tool_uses_20250919` dan `clear_thinking_20251015`.

### Lakukan compaction di sisi klien

Anda tetap dapat melakukan "compaction" (pemadatan) di sisi klien. Jika Anda menulis ringkasannya sendiri, jangan kirim kembali blok thinking yang dihasilkan sebelum penulisan ulang. Jika API yang menulisnya dengan compaction sesuai permintaan, [Compaction keep-tail](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#keep-tail-compaction) menjelaskan kapan thinking yang dipertahankan tetap valid.

#### Compaction sederhana (direkomendasikan)

Ketika percakapan menjadi terlalu panjang, ringkas seluruh sesi menjadi satu pesan pengguna dan kirim hanya pesan tersebut beserta instruksi berikutnya. Tidak ada bagian sebelumnya yang diputar ulang, sehingga tidak ada thinking tersisa yang dapat gagal dalam pemeriksaan, dan model bernalar dari awal berdasarkan ringkasan.

![Simple compaction (compaction sederhana): permintaan 4 mengirim riwayat lengkap dengan thinking pada setiap giliran asisten; permintaan 5 mengirim satu pesan pengguna yang berisi ringkasan giliran 1 hingga 4 beserta instruksi berikutnya, sehingga tidak ada thinking sebelumnya yang dikirim dan tidak ada yang diperiksa](https://platform.claude.com/docs/images/preserved-thinking-simple-compaction.svg)

```json
[
  {
    "role": "user",
    "content": "<summary of the session so far>\n\n<the next instruction>"
  }
]
```

Model Claude dilatih pada tugas jangka panjang dengan skema ini, dan untuk sebagian besar beban kerja, skema ini berkinerja baik.

#### Compaction keep-tail

Compaction keep-tail meringkas giliran-giliran lama dan mempertahankan giliran terbaru secara verbatim, sehingga model tetap melihat beberapa pertukaran terakhir kata demi kata. Jika Anda menulis ringkasannya sendiri, cara ini melanggar aturan: giliran asisten yang dipertahankan masih membawa blok thinking yang dihasilkan ketika yang mendahuluinya adalah giliran asli, bukan ringkasan. Blok-blok tersebut gagal.

Untuk mempertahankan thinking tersebut, minta API menulis ringkasan dengan [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming). Kirim hanya giliran-giliran lama dalam permintaan dengan parameter `compaction` dan header beta `compact-2026-09-04`. Kemudian kirim blok bertanda tangan yang dikembalikannya sebagai pengganti giliran-giliran tersebut, diikuti oleh giliran yang dipertahankan persis seperti yang dikembalikan. Thinking yang dipertahankan tetap valid selama semua kondisi berikut terpenuhi:

* Permintaan compaction berjalan pada model dengan "preserved thinking" (pemikiran yang dipertahankan). Model yang digunakan percakapan itu sendiri adalah pilihan yang paling sederhana.
* Giliran yang dipertahankan langsung mengikuti pesan yang diringkas, dan pesan pertama yang dipertahankan bukan pesan yang akan digabungkan API ke pesan terakhir yang diringkas: pesan dengan peran yang sama, atau pesan `role: "system"`.
* `system` dan `tools` non-deferred Anda cocok dengan permintaan compaction.

Cara paling sederhana untuk memenuhi kondisi kedua adalah melakukan compaction tepat pada `messages` dari permintaan yang sudah Anda buat. Pesan sistem di tengah percakapan yang berada di dalam giliran yang diringkas juga ikut diringkas, sehingga instruksi dan perubahan alatnya berhenti berlaku setelah penukaran. Agar salah satunya tetap berlaku, nyatakan kembali dalam pesan `role: "system"` tepat setelah giliran `user` baru pertama yang mengikuti giliran yang dipertahankan. Pesan sistem yang ditempatkan di antara blok dan giliran yang dipertahankan akan merusak thinking pada giliran tersebut.

Sisa bagian ini membahas ringkasan yang Anda tulis sendiri.

![Keep-tail compaction (compaction keep-tail): riwayat diganti dengan ringkasan giliran 1 dan 2 diikuti giliran 3 hingga 5 secara verbatim; thinking pada giliran asisten 3 dan 4 dihasilkan setelah giliran asli, bukan ringkasan, sehingga gagal; permintaan yang sama yang dikirim dengan prefix\_mismatch\_behavior drop\_block berhasil, API membuang kedua blok tersebut dan mencantumkannya di input\_transformations](https://platform.claude.com/docs/images/preserved-thinking-keep-tail-compaction.svg)

Perbaikan: pertahankan giliran persis seperti adanya dan kirim `prefix_mismatch_behavior: "drop_block"`. API membuang blok thinking yang usang, model membaca blok `text` dan `tool_use` dari giliran yang dipertahankan, dan permintaan berhasil.

Teruskan riwayat yang telah dipadatkan sebagai `messages` dan atur `block_binding` pada konfigurasi `thinking`. Dalam contoh berikut, `compacted_messages` adalah array yang dihasilkan oleh langkah compaction Anda: pesan ringkasan diikuti oleh giliran yang dipertahankan persis seperti yang dikembalikan API, termasuk blok `thinking`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
    -d "{
      \"model\": \"claude-fable-5-1\",
      \"max_tokens\": 16000,
      \"thinking\": {
        \"type\": \"adaptive\",
        \"block_binding\": { \"prefix_mismatch_behavior\": \"drop_block\" }
      },
      \"messages\": $COMPACTED_MESSAGES
    }"
  ```

  ```bash CLI
  ant beta:messages create --beta thinking-binding-controls-2026-08-01 <<YAML
  model: claude-fable-5-1
  max_tokens: 16000
  thinking:
    type: adaptive
    block_binding:
      prefix_mismatch_behavior: drop_block
  messages: $COMPACTED_MESSAGES
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # compacted_messages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  response = client.beta.messages.create(
      model="claude-fable-5-1",
      max_tokens=16000,
      thinking={
          "type": "adaptive",
          "block_binding": {"prefix_mismatch_behavior": "drop_block"},
      },
      messages=compacted_messages,
      betas=["thinking-binding-controls-2026-08-01"],
  )

  print(response.input_transformations)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // compactedMessages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  const response = await client.beta.messages.create({
    model: "claude-fable-5-1",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      block_binding: { prefix_mismatch_behavior: "drop_block" }
    },
    messages: compactedMessages,
    betas: ["thinking-binding-controls-2026-08-01"]
  });

  console.log(response.input_transformations);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // compactedMessages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  var response = await client.Beta.Messages.Create(
      new()
      {
          Model = "claude-fable-5-1",
          MaxTokens = 16000,
          Thinking = new BetaThinkingConfigAdaptive
          {
              BlockBinding = new()
              {
                  PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.DropBlock,
              },
          },
          Messages = compactedMessages,
          Betas = [AnthropicBeta.ThinkingBindingControls2026_08_01],
      }
  );

  Console.WriteLine(response.InputTransformations?.Count ?? 0);
  ```

  ```go Go
  client := anthropic.NewClient()

  // compactedMessages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-fable-5-1",
  	MaxTokens: 16000,
  	Thinking: anthropic.BetaThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{
  			BlockBinding: anthropic.BetaThinkingBlockBindingParam{
  				PrefixMismatchBehavior: anthropic.BetaThinkingPrefixMismatchBehaviorDropBlock,
  			},
  		},
  	},
  	Messages: compactedMessages,
  	Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaThinkingBindingControls2026_08_01},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(len(response.InputTransformations))
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // compactedMessages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-fable-5-1")
          .maxTokens(16000L)
          .thinking(BetaThinkingConfigAdaptive.builder()
              .blockBinding(BetaThinkingBlockBinding.builder()
                  .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.DROP_BLOCK)
                  .build())
              .build())
          .messages(compactedMessages)
          .addBeta(AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01)
          .build();

      BetaMessage response = client.beta().messages().create(params);

      IO.println(response.inputTransformations());
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
  use Anthropic\Client;

  $client = new Client();

  // $compactedMessages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  $response = $client->beta->messages->create(
      model: 'claude-fable-5-1',
      maxTokens: 16000,
      thinking: BetaThinkingConfigAdaptive::with(
          blockBinding: BetaThinkingBlockBinding::with(
              prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::DROP_BLOCK,
          ),
      ),
      messages: $compactedMessages,
      betas: [AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
  );

  var_dump($response->inputTransformations);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # compacted_messages: pesan ringkasan, lalu giliran yang dipertahankan sesuai yang dikembalikan
  response = client.beta.messages.create(
    model: "claude-fable-5-1",
    max_tokens: 16_000,
    thinking: {
      type: "adaptive",
      block_binding: {prefix_mismatch_behavior: "drop_block"}
    },
    messages: compacted_messages,
    betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01]
  )

  puts response.input_transformations
  ```
</CodeGroup>

Respons membawa giliran asisten baru seperti biasa, ditambah satu entri `input_transformations` untuk setiap blok yang dibuang. Untuk riwayat dalam diagram, itu adalah thinking pada giliran asisten 3 dan 4:

```json
{
  "input_transformations": [
    {
      "type": "thinking_dropped",
      "path": "messages.2.content.0",
      "reason": "prefix_binding_mismatch"
    },
    {
      "type": "thinking_dropped",
      "path": "messages.4.content.0",
      "reason": "prefix_binding_mismatch"
    }
  ]
}
```

Terus kirim `"drop_block"` pada permintaan berikutnya selama kedua giliran tersebut masih berada dalam riwayat. Thinking yang dihasilkan model mulai dari permintaan ini dan seterusnya mengikuti ringkasan dan tetap valid. Jika Anda lebih memilih untuk tidak bergantung pada header beta, alternatifnya adalah menghapus sendiri blok `thinking` dan `redacted_thinking` dari giliran asisten yang dipertahankan saat Anda membangun riwayat yang dipadatkan.

#### Compaction latar belakang (async)

Compaction latar belakang membangun ringkasan di luar jalur kritis sementara percakapan terus berlanjut, lalu menukarnya beberapa permintaan kemudian. Minta API menulis ringkasan dengan [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming):

1. Kirim percakapan sejauh ini dalam permintaan terpisah dengan parameter `compaction` dan header beta `compact-2026-09-04`.
2. Terus bekerja pada riwayat lengkap selama permintaan tersebut berjalan.
3. Pada permintaan pertama setelah blok tiba, kirim blok tersebut sebagai pengganti pesan-pesan yang dimuat dalam permintaan compaction, diikuti oleh setiap giliran yang ditambahkan sejak saat itu.

Thinking yang dihasilkan selama ringkasan sedang dibangun tetap valid dengan kondisi yang sama seperti pada [Compaction keep-tail](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#keep-tail-compaction).

Ringkasan yang Anda bangun sendiri melanggar aturan dengan cara yang sama seperti keep-tail, hanya saja tertunda: setiap giliran asisten yang dihasilkan selama ringkasan sedang dibangun membawa thinking yang mendahului penukaran, dan semuanya gagal begitu ringkasan diterapkan. Jika Anda menggunakannya, perlakukan penukaran seperti keep-tail dan kirim `"drop_block"` sejak penukaran dan seterusnya, atau lakukan compaction secara sinkron.

#### Pola yang tidak berfungsi dengan preserved thinking

* **Memotong giliran dari bagian tengah.** Menghapus giliran individual membuat setiap blok thinking setelahnya menjadi tidak valid, dan tidak ada skema compaction yang dapat menghindarinya. Jika Anda memotong giliran untuk mengubah instruksi, tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions) sebagai gantinya. Untuk menghapus hasil alat lama atau thinking lama secara selektif, gunakan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) di sisi server.
* **Melakukan compaction di tengah putaran alat.** Jangan lakukan compaction di antara `tool_use` pada giliran asisten dan `tool_result` yang menjawabnya. Kirim kembali giliran asisten tersebut dengan thinking-nya utuh agar model menyelesaikan putaran tersebut dengan penalarannya. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

### Referensikan file berdasarkan ID, bukan berdasarkan URL yang kontennya berubah

Untuk blok `image` atau `document` dengan sumber `url`, pemeriksaan mencakup byte yang diambil, bukan string URL. URL yang kontennya berubah membuat thinking berikutnya tidak valid: misalnya endpoint "tangkapan layar terbaru", atau dokumen yang diedit seseorang di antara giliran. URL bertanda tangan yang berganti-ganti untuk file yang sama tidak menimbulkan masalah. Untuk konten yang Anda referensikan di beberapa giliran, unggah sekali dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan gunakan `file_id`, atau kirim dalam base64.

### Library, proxy, dan gateway

Library, proxy, atau gateway berada di antara riwayat milik pihak lain dan API, sehingga penulisan ulang yang dilakukannya dihitung sebagai edit, dan penggunanya tidak dapat melihat atau memperbaikinya.

* **Teruskan apa yang tidak Anda kenali.** Teruskan nilai `anthropic-beta` dan `thinking.block_binding` dari pemanggil tanpa perubahan, dan kembalikan `input_transformations` kepada mereka. Skema opsi yang menolak key yang tidak dikenal akan menghalangi pengguna Anda memilih `"drop_block"`.
* **Biarkan pesan `role: "system"` di tempat pemanggil meletakkannya.** Memindahkannya ke field `system` tingkat atas akan mengubah `system` pada permintaan tersebut dan membuat setiap blok thinking dalam percakapan menjadi tidak valid.
* **Untuk menonaktifkan penggunaan alat pada suatu permintaan, kirim `tool_choice: {"type": "none"}`.** Jangan hapus `tools`.
* **Jangan sembunyikan error 400.** Jika kode Anda menangkapnya, menghapus thinking, dan mencoba ulang atas nama pemanggil, catat bahwa hal itu dilakukan: riwayat mereka tetap teredit, dan model kehilangan penalaran sebelumnya pada setiap permintaan berikutnya.

## FAQ

<AccordionGroup>
  <Accordion title="Apakah saya memerlukan akun baru untuk menguji preserved thinking?">
    Tidak. Kirim header beta `thinking-binding-controls-2026-08-01` dan atur `thinking.block_binding.prefix_mismatch_behavior`. Mengatur field tersebut membuat permintaan itu ikut dalam penegakan aturan, terlepas dari usia akun. `"error"` menolak riwayat yang diedit dengan error 400 yang sama seperti yang diterima akun baru, dan `"drop_block"` meloloskan permintaan serta mencantumkan apa yang dibuang di `input_transformations`. Lihat [Periksa apakah kode Anda mengedit prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted).
  </Accordion>

  <Accordion title="Jika ada yang berubah sebelum blok thinking, bahkan satu deskripsi alat, apakah percakapan menjadi tidak dapat digunakan?">
    Tidak. Yang gagal adalah thinking yang sudah ada dalam riwayat setelah titik yang Anda ubah, dan Anda yang memilih apa yang terjadi padanya. Dengan `prefix_mismatch_behavior: "drop_block"`, API membuang blok-blok tersebut dan permintaan berhasil: model menjawab giliran itu tanpa penalaran tersebut, dan caching prompt dimulai ulang dari titik edit. Dengan nilai default `"error"`, API menolak permintaan dengan error 400 hingga Anda membatalkan edit atau mengirim ulang dengan `"drop_block"`. Lihat [Apa yang dilakukan API terhadap blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior). [Apa yang dihitung sebagai edit](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#what-counts-as-an-edit) mencantumkan perubahan mana yang berpengaruh.
  </Accordion>

  <Accordion title="Apakah mengubah effort atau pengaturan thinking lainnya di antara permintaan membuat thinking sebelumnya tidak valid?">
    Tidak. `output_config.effort`, `max_tokens`, dan konfigurasi `thinking` bukan bagian dari prefiks yang diperiksa, yang hanya mencakup `system`, `tools`, dan `messages`. Perubahan effort di tingkat atas membuat sebagian besar cache untuk prompt menjadi tidak valid. Pada Claude Fable 5.1, perubahan [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#effort-changes) mempertahankan cache untuk prompt dan digunakan sebagai tingkat effort baru hingga diubah lagi.
  </Accordion>

  <Accordion title="Daftar alat saya berubah di tengah sesi. Bagaimana cara menghindari percakapan menjadi tidak valid?">
    Jangan edit `tools`. Deklarasikan set lengkap di awal sesi, tandai alat yang belum tersedia dengan `defer_loading: true`, lalu tawarkan atau tarik kembali alat tersebut dengan blok `tool_addition` dan `tool_removal`. Jika Anda baru mengetahui skema suatu alat di tengah sesi, misalnya dari server MCP yang ditemukan saat runtime, Anda tetap dapat menambahkannya ke `tools` dengan `defer_loading: true` dan menawarkannya dengan cara yang sama. Hal itu aman karena alat deferred yang tidak direferensikan bukan bagian dari prefiks. Pesan `role: "system"` yang membawa blok-blok ini menjadi bagian dari prefiks untuk thinking berikutnya, jadi jangan pindahkan, ubah kata-katanya, atau hapus pesan tersebut setelahnya. Lihat [Menambah atau menghapus alat dengan `tool_addition` dan `tool_removal`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#tool-changes).
  </Accordion>

  <Accordion title="Saya melakukan compaction dengan meringkas giliran lama dan mempertahankan giliran terbaru secara verbatim. Apakah itu masih berfungsi?">
    Ya, jika API yang menulis ringkasannya. [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#server-side-trimming) (header beta `compact-2026-09-04`) meringkas giliran-giliran lama menjadi blok bertanda tangan yang Anda kirim sebagai penggantinya. Giliran terbaru mempertahankan thinking-nya dengan kondisi yang dijelaskan di [Compaction keep-tail](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#keep-tail-compaction).

    Jika Anda menulis ringkasannya sendiri, thinking pada giliran yang dipertahankan gagal dalam pemeriksaan, karena blok-blok tersebut dihasilkan berdasarkan riwayat yang Anda ganti. Hapus blok `thinking` dan `redacted_thinking` dari giliran yang Anda bawa dan pertahankan blok `text` dan `tool_use`-nya, atau kirim `prefix_mismatch_behavior: "drop_block"` dan biarkan API membuangnya. Compaction sederhana tidak meninggalkan thinking yang dapat gagal dan merupakan pendekatan yang direkomendasikan: satu pesan ringkasan ditambah giliran pengguna berikutnya, tanpa memutar ulang giliran sebelumnya. [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) dan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) di sisi server tidak dihitung sebagai edit. Lihat [Lakukan compaction di sisi klien](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#custom-compaction-on-the-client).
  </Accordion>

  <Accordion title="Bagaimana cara menangani file instruksi seperti AGENTS.md atau CLAUDE.md yang berubah di tengah sesi?">
    Muat file tersebut sekali di awal sesi dan pertahankan prompt `system` tingkat atas serta `tools` tetap. Ketika sebuah file berubah, tambahkan versi barunya pada titik tersebut di `messages` alih-alih mengedit yang asli. Gunakan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) untuk instruksi yang berasal dari Anda sebagai operator. Untuk teks file yang Anda anggap tidak tepercaya, yang tidak seharusnya memiliki otoritas prompt sistem, letakkan kontennya di giliran `user` berikutnya. Lihat [Menambahkan instruksi dengan pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions) dan [Batasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations).
  </Accordion>

  <Accordion title="Dapatkah saya melanjutkan sesi yang tersimpan nanti, setelah restart atau keesokan harinya?">
    Ya. Sesi yang dilanjutkan adalah permintaan lanjutan biasa: `system`, `tools`, dan `messages` sebelumnya harus memiliki konten yang sama dengan yang terakhir Anda kirim. Format JSON dan urutan key tidak berpengaruh; nilainya yang berpengaruh. Simpan persis apa yang Anda kirim dan terima, lalu putar ulang itu: prompt sistem yang telah dirender, definisi alat, dan setiap giliran asisten seperti yang dikembalikan. Jangan merender ulang dari input yang mungkin telah berubah sejak saat itu, seperti tanggal, file instruksi yang diperbarui, atau versi alat yang baru. Apa pun yang baru dimasukkan ke dalam pesan yang ditambahkan. Lihat [Kirim kembali giliran asisten persis seperti yang dikembalikan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#append-assistant-turns-exactly-as-returned).
  </Accordion>

  <Accordion title="Sesi yang tersimpan sekarang gagal pada setiap permintaan. Bagaimana cara membuatnya berfungsi kembali?">
    Riwayat yang tersimpan mengandung edit, sehingga memutarnya ulang tidak akan berhasil. Kirim sesi tersebut dengan `prefix_mismatch_behavior: "drop_block"` mulai sekarang, atau hapus blok `thinking` dan `redacted_thinking`-nya sekali lalu lanjutkan. Thinking yang dihasilkan model sejak titik itu tetap valid selama tidak ada yang berubah lagi sebelumnya. Kemudian temukan edit tersebut agar sesi baru tidak mengalaminya. Lihat [Menangani error dalam kode](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#handle-the-error-in-code).
  </Accordion>

  <Accordion title="Harness saya dapat merutekan giliran ke model non-Claude. Apakah giliran tersebut membuat thinking Claude sebelumnya tidak valid?">
    Tidak, asalkan giliran tersebut ditambahkan setelah riwayat yang ada dan tidak ada yang berubah sebelumnya: pesan asisten tanpa blok thinking adalah pesan tambahan seperti pesan lainnya. Kirim output model lain sebagai konten `text` dan `tool_use`.
  </Accordion>

  <Accordion title="Dapatkah saya membawa penalaran suatu percakapan ke percakapan baru?">
    Tidak ke percakapan yang berbeda. Blok thinking hanya dapat digunakan ketika mengikuti `system`, `tools`, dan `messages` yang persis sama dengan yang menghasilkannya. Cabang yang memutar ulang riwayat tersebut tanpa perubahan hingga titik percabangan mempertahankan thinking-nya. Percakapan yang dimulai dari hal lain tidak dapat menggunakannya, jadi mulailah percakapan tersebut dari ringkasan status tugas, seperti pada [compaction sederhana](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#custom-compaction-on-the-client): tujuan, keputusan yang telah dibuat, file dan hasil sejauh ini, serta langkah berikutnya.
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemecahan masalah thinking" icon="hammer" href="https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting">
    Diagnosis dan perbaiki kegagalan thinking yang paling umum: error 400 konfigurasi, blok thinking kosong atau hilang, penghentian max\_tokens, dan cache miss.
  </Card>

  <Card title="Pesan sistem dan perubahan alat di tengah percakapan" icon="messages" href="https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages">
    Ubah instruksi sistem atau ketersediaan alat di tengah percakapan tanpa membatalkan validitas prefiks yang di-cache sebelumnya.
  </Card>

  <Card title="Compaction" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/compaction">
    Compaction konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.
  </Card>

  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Cache prefiks prompt dengan `cache_control` untuk memangkas biaya dan latensi, menggunakan caching otomatis atau breakpoint eksplisit dengan TTL 5 menit atau 1 jam.
  </Card>
</CardGroup>
