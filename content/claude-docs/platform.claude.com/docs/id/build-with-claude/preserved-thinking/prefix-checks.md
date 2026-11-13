---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 30439295aa18bb818d381140600d7d84b3ae8c55fa497dfa29c207bdfb671a9a
---

---
title: Pemeriksaan prefiks pada blok pemikiran
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks
description: Apa yang dibandingkan oleh pemeriksaan prefiks, model mana yang menjalankannya, apa yang terjadi ketika sebuah permintaan gagal dalam pemeriksaan prefiks, dan cara menangani error 400 serta kasus tanpa error.
featureMetadata:
  status: stable
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-opus-5-5
    - claude-sonnet-5-5
    - claude-haiku-5-5
  supportedPlatforms:
    Claude API: stable
    Amazon Bedrock: stable
    Amazon Bedrock (bedrock-runtime): stable
    Claude Platform on AWS: stable
    Claude Models on Google Cloud (Anthropic managed): stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

Setiap permintaan yang mengirimkan kembali “thinking blocks” (blok pemikiran) ke [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes) menjalani “prefix check” (pemeriksaan prefiks). Pemeriksaan prefiks gagal jika `system`, `tools`, atau pesan sebelumnya berubah setelah Claude menghasilkan sebuah blok. Pemeriksaan prefiks juga gagal jika sebuah blok pemikiran yang berada di antara blok lainnya dihilangkan atau dipindahkan.

Gagal dalam pemeriksaan prefiks mungkin menghasilkan error 400 dan mungkin juga tidak, [tergantung pada modelnya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), jadi [tangani kedua kasus](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#handle-either-outcome).

## Siapa yang terpengaruh oleh pemeriksaan prefiks

Anda tidak perlu mengubah apa pun jika salah satu dari hal berikut benar:

* Claude Code, claude.ai, atau Claude Managed Agents mengelola riwayat percakapan Anda.
* Claude Agent SDK mengelola riwayat tersebut, dan prompt sistem yang Anda berikan kepada SDK tetap sama.
* Kode Anda mengikuti [tiga kebiasaan integrasi append-only](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), dan tidak ada yang menulis ulang permintaannya di tengah jalan.
* Anda tidak memanggil [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes) mana pun.

Jika permintaan Anda melewati sebuah library, proxy, atau gateway, [bandingkan apa yang dikirimkannya dengan apa yang Anda kirim](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#find-the-change-details). Jika Anda menjalankan salah satunya, lihat [Library, proxy, dan gateway](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#libraries-proxies-gateways) untuk mengetahui apa yang harus diteruskan.

## Apa yang harus tetap sama, dan mengapa

Jadikan integrasi Anda “append-only” (hanya menambahkan di akhir). Tiga kebiasaan mewujudkannya:

1. Kirim kembali setiap giliran asisten persis seperti yang dikembalikan oleh API, termasuk blok pemikiran yang teksnya kosong.
2. Bangun `system` dan `tools` satu kali untuk setiap percakapan, dan kirim salinan tersebut setiap kali.
3. Letakkan setiap pembaruan dalam pesan baru di bagian akhir, dan biarkan tetap di sana.

Penalaran setiap blok pemikiran berkaitan persis dengan apa yang ada sebelumnya: `system`, `tools`, dan setiap pesan sebelumnya. Konten tersebut adalah *prefiks* blok itu, dan itulah yang dibandingkan oleh [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check-details).

Pemeriksaan prefiks mirip dengan caching prompt, bedanya sebuah perubahan membuat pemikiran setelahnya tidak valid, alih-alih hanya tidak mengenai cache.

Ambil contoh aplikasi yang menaruh tanggal hari ini di prompt sistemnya. Pada tengah malam tanggal berubah, begitu pula prefiks dari pemikiran yang sudah ada dalam percakapan. Pemikiran itu menjadi tidak valid, dan permintaan berikutnya dapat gagal. Aplikasi append-only mempertahankan prompt sistem seperti semula, dan menyatakan tanggal baru dalam [sebuah pesan di bagian akhir](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#changing-context).

<Frame>
  ![Pembaruan di bagian akhir membuat semua pemikiran tetap valid; perubahan pada giliran 2, atau pada system, membuat pemikiran setelahnya tidak valid](https://platform.claude.com/docs/id/images/preserved-thinking-add-or-change.svg)
</Frame>

Sebuah perubahan hanya membuat pemikiran yang sudah ada setelahnya menjadi tidak valid. Pemikiran sebelum perubahan itu dan pemikiran yang dihasilkan Claude sesudahnya tetap valid.

## Jika kode Anda mengubah prompt sistem, alat, atau riwayat

| Jika kode Anda…                                                                                                     | Apa yang harus dilakukan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Membangun ulang prompt sistem dengan tanggal, sebuah mode, atau file instruksi                                      | Berhenti mengubah `system`. [Tambahkan instruksi Anda sendiri sebagai pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#new-instructions), yaitu entri `role: "system"` di `messages`, dan [nyatakan nilai baru di giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#changing-context). Untuk teks yang dapat diedit orang lain, lihat [Teks yang dapat diedit orang lain](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#untrusted-text) sebagai gantinya. |
| Menambahkan, menghapus, atau mengubah kata-kata sebuah alat, atau mendapatkan alat baru ketika server MCP terhubung | Berhenti mengubah `tools`, dan [tambahkan atau hapus alat dalam pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#tool-changes).                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Memangkas, menciutkan, atau meringkas giliran lama, dan mempertahankan giliran terbaru tanpa perubahan              | [Biarkan API yang menulis ringkasan, atau hapus pemikiran dari giliran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#server-side-trimming).                                                                                                                                                                                                                                                                                                                                                                                                                                   |

Penyebab lain, seperti melewatkan blok pemikiran yang teksnya kosong atau membangun ulang percakapan yang tersimpan, memiliki perbaikannya sendiri: lihat [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions). Untuk menemukan penyebab Anda, [minta agen memeriksa kode Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#hand-to-an-agent).

## Apa yang dilakukan setiap model ketika pemeriksaan prefiks gagal

Di Claude API dan [beberapa platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#feature-availability), hasil dari gagal dalam pemeriksaan prefiks ketika permintaan tidak menyertakan [`prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls) bergantung pada modelnya:

| Model dengan pemikiran yang dipertahankan | Hasil                                                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5.2                          | Error 400                                                                                                                          |
| Claude Mythos 5.2                         | Error 400                                                                                                                          |
| Claude Mythos 5.1                         | Error 400                                                                                                                          |
| Claude Fable 5.1                          | [Kemungkinan error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#possible-400-error) |
| Claude Opus 5.5                           | [Kemungkinan error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#possible-400-error) |
| Claude Sonnet 5.5                         | [Kemungkinan error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#possible-400-error) |
| Claude Haiku 5.5                          | [Kemungkinan error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#possible-400-error) |

Jika tabel menyebutkan “Kemungkinan error 400,” ada dua kasus: permintaan yang gagal dalam pemeriksaan prefiks mungkin mendapatkan error 400 atau tidak mendapatkan error. Ketika tidak ada error yang dikembalikan, blok yang gagal dalam pemeriksaan prefiks sampai ke model. Claude membacanya seperti input lainnya, Anda ditagih untuk blok-blok tersebut, dan Claude bekerja berdasarkan penalaran tentang konten yang sejak itu telah berubah.

Pada model-model tersebut, Anda dapat [memeriksa kasus mana yang didapatkan sebuah permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#check-which-case), tetapi [tangani kedua kasus](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#handle-either-outcome).

<Tip>
  Kode yang mengikuti [tiga kebiasaan integrasi append-only](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) tidak menyebabkan kegagalan dalam pemeriksaan prefiks.
</Tip>

[Item Message Batches](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#batches) yang tidak menyertakan `prefix_mismatch_behavior` tidak mendapatkan error, dan API dapat tidak menyertakan blok yang gagal dalam pemeriksaan prefiks.

## Tangani kedua kasus

Untuk mendapatkan satu hasil yang sama pada setiap permintaan, jadikan integrasi Anda append-only atau atur `prefix_mismatch_behavior`. Jika tidak, kode Anda harus menangani kedua perilaku.

* **Append-only:** dengan [tiga kebiasaan tersebut](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), kode Anda tidak membuat permintaan gagal dalam pemeriksaan prefiks.
* **Pengaturan:** dengan `"error"` pada setiap permintaan, setiap kegagalan menjadi error 400, dan Anda [menangkapnya dalam kode](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#handle-the-error-in-code).
* **Kedua perilaku:** jika Anda tidak menyertakan pengaturan tersebut, tangkap error 400, dan [pantau pemikiran yang gagal dalam pemeriksaan prefiks dan sampai ke Claude](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#watch-production-traffic).

Setelah error 400, kirim `"drop_block"` pada permintaan-permintaan berikutnya dalam percakapan itu untuk memulihkannya. Ini memiliki biaya: lihat [Biaya tidak menyertakan pemikiran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost). Jangan mengirimkannya pada semua percakapan Anda untuk menyembunyikan error.

## Detail teknis

### Cara kerja pemeriksaan prefiks

Model dengan pemikiran yang dipertahankan merekam sidik jari dari prefiks setiap blok pemikiran di dalam `signature` blok tersebut. Referensi API menyebut pemeriksaan prefiks sebagai pemeriksaan percakapan, dan error 400 menyatakan bahwa blok yang gagal dalam pemeriksaan prefiks `is bound to a different conversation`.

### Model mana yang menjalankan pemeriksaan prefiks

Pemeriksaan prefiks berjalan di Claude API dan di [beberapa platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#feature-availability). Pemeriksaan prefiks memeriksa blok pemikiran yang dihasilkan oleh [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), pada permintaan ke salah satu model tersebut. Di Claude API, model lain, seperti Claude Opus 5, tidak menjalankannya, dan pemeriksaan prefiks tidak mencakup blok dari model-model tersebut.

### Apa yang dihitung sebagai perubahan

* **Setiap blok diperiksa terhadap rekamannya sendiri.** API membandingkan apa yang ada sebelum sebuah blok dalam permintaan ini dengan apa yang direkam oleh signature-nya ketika Claude menghasilkannya. Permintaan terakhir Anda tidak berperan. Pemeriksaan prefiks hanya melihat konten, bukan sesi, ID, atau pengguna. Konten yang sama dalam permintaan baru atau dalam fork lolos pemeriksaan prefiks.
* **Pemeriksaan prefiks membandingkan apa yang Anda kirim, bukan apa yang dibaca Claude.** [Compaction pada ambang batas token](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold) dan pengeditan konteks hanya mengubah apa yang dibaca Claude, sehingga tidak pernah dihitung. Setelah blok compaction ambang, API hanya membandingkan pesan-pesan mulai dari blok itu dan seterusnya, ditambah `system` dan `tools`. Compaction sesuai permintaan memiliki syaratnya sendiri: lihat [Syarat agar thinking yang dipertahankan tetap valid](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid). Untuk file yang dikirim melalui URL dan, di Claude API, [daftar alat MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#pin-mcp-tool-list), API membandingkan apa yang diambilnya sebagai gantinya.
* **Pemikiran yang Anda kirim harus berupa rangkaian yang tidak terputus.** Blok pemikiran tidak dibandingkan sebagai konten. Tetapi setiap blok yang Anda kirim, selain yang pertama, harus memiliki blok pemikiran sebelumnya yang sama seperti ketika Claude menghasilkannya. Jadi Anda dapat [menghilangkan yang paling lama, yang paling baru, atau semuanya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#leave-out-thinking), tetapi tidak satu blok yang berada di antaranya.

Sebuah perubahan bisa sekecil satu kata dalam deskripsi alat. Mengubah, menyisipkan, memindahkan, atau menghapus pesan sebelumnya dihitung sebagai perubahan, apa pun perannya. Begitu pula mengubah teks sebelum blok pemikiran di dalam pesannya sendiri.

### Apa yang tidak dihitung

| Ini tidak dihitung                                                                                    | Karena                                                                                    |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `model`, `effort`, `max_tokens`, `tool_choice`, `metadata`, `thinking.display`, dan parameter lainnya | Hanya `system`, `tools`, dan pesan yang dibandingkan                                      |
| Format JSON atau urutan kunci                                                                         | API membandingkan JSON yang telah di-parse, bukan teksnya                                 |
| Penanda `cache_control`                                                                               | Penanda ini menyatakan di mana harus melakukan cache, dan bukan konten yang dibaca Claude |
| Alat dengan `defer_loading: true` yang belum dirujuk oleh apa pun                                     | Alat tersebut tidak berada dalam konteks Claude sampai ada sesuatu yang merujuknya        |

### Atur `prefix_mismatch_behavior`

[Beta header](https://platform.claude.com/docs/id/api/beta-headers#beta-features-on-other-platforms) `thinking-binding-controls-2026-08-01` menambahkan pengaturan `thinking.block_binding.prefix_mismatch_behavior` dan array `input_transformations` pada respons.

| Nilai                         | Jika sebuah blok gagal dalam pemeriksaan prefiks                                                                                                                                                                                                                                                                |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"error"`                     | API menolak permintaan dengan error 400 yang menyebutkan blok tidak valid pertama                                                                                                                                                                                                                               |
| `"drop_block"`                | API tidak menyertakan blok yang tidak valid, dan permintaan berhasil. Anda tidak ditagih untuk blok tersebut, tetapi [tidak menyertakannya dapat menimbulkan biaya lebih besar](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost) |
| Tidak disertakan, atau `null` | [Tergantung pada modelnya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes)                                                                                                                                                                                     |

Blok yang gagal dalam pemeriksaan prefiks tetap tidak valid pada setiap permintaan berikutnya yang mengirimkannya, selama perubahan tersebut masih ada. Pengaturan ini berlaku pada satu permintaan yang membawanya. Dengan pemikiran dinonaktifkan (`"disabled"` atau `"between_tools"`), mengirimkannya menghasilkan error 400 pada setiap model.

Permintaan berikut mengatur `prefix_mismatch_behavior` ke `"drop_block"`. Pada giliran pertama tidak ada pemikiran yang perlu dikirim kembali, sehingga `input_transformations` dikembalikan dalam keadaan kosong:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
  ant beta:messages create --beta thinking-binding-controls-2026-08-01 <<'YAML'
  model: claude-opus-5-5
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
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus5_5,
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
              new BetaUserMessageParam
              {
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
  	Model:     anthropic.ModelClaudeOpus5_5,
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
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
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
  use Anthropic\Beta\Messages\BetaTextBlock;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
  use Anthropic\Client;
  use Anthropic\Messages\Model;

  $client = new Client();

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
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
      if ($block instanceof BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }

  echo 'Input transformations: ', count($response->inputTransformations ?? []), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 16_000,
    thinking: {
      type: "adaptive",
      block_binding: { prefix_mismatch_behavior: "drop_block" }
    },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ],
    betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01]
  )

  response.content.each do |block|
    puts block.text if block.is_a?(Anthropic::Beta::BetaTextBlock)
  end

  puts "Input transformations: #{response.input_transformations&.length || 0}"
  ```
</CodeGroup>

### Pantau lalu lintas produksi

Tanpa menyertakan `prefix_mismatch_behavior`, permintaan yang gagal dalam pemeriksaan prefiks mungkin tidak mendapatkan error pada [beberapa model](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes). Blok pemikiran yang gagal dalam pemeriksaan prefiks kemudian sampai ke model. Untuk menemukan blok-blok tersebut dalam lalu lintas produksi, kirim beta header `thinking-binding-controls-2026-08-01`, jangan sertakan pengaturan tersebut, dan catat array `input_transformations` dari setiap respons. Header tersebut menambahkan array itu dan tidak mengubah apa yang diterima model.

Setiap blok tersebut mendapatkan entri `thinking_mismatch_allowed` sendiri dalam array itu. Satu entri terlihat seperti ini:

```json
{
  "input_transformations": [
    {
      "type": "thinking_mismatch_allowed",
      "path": "messages.1.content.0",
      "reason": "prefix_binding_mismatch"
    }
  ]
}
```

Untuk menemukan perubahannya, lihat [Temukan apa yang diubah kode Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#find-the-change).

### Periksa kasus mana yang Anda dapatkan

Pada [beberapa model](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), permintaan yang gagal dalam pemeriksaan prefiks mungkin mendapatkan error 400 atau tidak mendapatkan error. Pengujian ini menunjukkan mana yang didapatkan sebuah permintaan:

1. Ambil percakapan yang berisi blok pemikiran dari salah satu model tersebut. Ubah atau tambahkan prompt sistem (`system`). Blok tersebut kemudian gagal dalam pemeriksaan prefiks, karena prompt sistem berubah setelah Claude menghasilkan blok tersebut.
2. Kirimkan ke model yang sama dengan beta header `thinking-binding-controls-2026-08-01`, dan jangan sertakan `prefix_mismatch_behavior`.

Responsnya adalah salah satu dari berikut:

* **[Error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#prefix-mismatch-error) yang menyatakan `bound to a different conversation`:** Permintaan mendapatkan error 400.
* **Respons 200 yang array `input_transformations`-nya memiliki entri `thinking_mismatch_allowed`:** Permintaan tidak mendapatkan error. Setiap entri menyebutkan blok pemikiran yang gagal dalam pemeriksaan prefiks dan sampai ke Claude.
* **Respons 200 yang array `input_transformations`-nya kosong:** Tidak ada blok yang gagal dalam pemeriksaan prefiks, sehingga pengujian tidak menunjukkan apa pun. Pastikan percakapan tersebut berisi blok pemikiran dari model itu.

Hasilnya menggambarkan satu permintaan tersebut dan tidak menjanjikan apa pun tentang permintaan berikutnya, jadi tulis kode Anda untuk [menangani kedua kasus](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#handle-either-outcome).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks" icon="edit" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions">
    Apa yang harus dikirim sebagai pengganti setiap perubahan yang dibuat kode Anda pada sebuah percakapan.
  </Card>

  <Card title="Perbaiki blok pemikiran yang terikat ke percakapan lain" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation">
    Pulihkan percakapan yang gagal dalam pemeriksaan prefiks, temukan apa yang diubah kode Anda, dan uji bahwa perubahan itu sudah hilang.
  </Card>

  <Card title="Pemikiran yang dipertahankan" icon="book" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking">
    Apa itu pemikiran yang dipertahankan, pada apa sebuah blok pemikiran terikat, serta beralih model atau akun.
  </Card>
</CardGroup>
