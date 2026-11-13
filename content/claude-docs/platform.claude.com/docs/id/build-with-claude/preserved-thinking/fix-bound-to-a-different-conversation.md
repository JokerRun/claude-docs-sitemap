---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: a971e230960231151b6dcce83d904febd6df8f96932e456bfb5c735ca752d7a2
---

---
title: Perbaiki blok pemikiran yang terikat ke percakapan lain
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation
description: Lanjutkan kembali percakapan setelah error 400 yang menyatakan bahwa blok pemikiran terikat ke percakapan lain, temukan apa yang diubah kode Anda, dan uji bahwa perubahan itu sudah hilang.
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

Mengirim permintaan yang sama lagi tidak akan berhasil, karena riwayat Anda masih memuat apa yang diubah oleh kode Anda. Kirim `"drop_block"` sesuai langkah [Hentikan error sekarang](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#prefix-mismatch-error). Perbaikan jangka panjangnya adalah membuat kode Anda [“append-only” (hanya menambah di akhir)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check).

## Kesalahan: The block is bound to a different conversation

“Thinking block” (blok pemikiran) tersebut gagal dalam “prefix check” ([pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check)): sesuatu sebelum blok itu berubah setelah Claude menghasilkannya (lihat [Apa yang dihitung sebagai perubahan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-counts-as-an-edit)), atau sebuah blok pemikiran di antara blok-blok lain tidak disertakan atau dipindahkan. Error-nya terlihat seperti ini, dan dapat berlanjut dengan [menyebutkan apa yang berubah](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#prefix-mismatch-error-details):

```text wrap
messages.1.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

“A different conversation” berarti konten yang berbeda sebelum blok tersebut: [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) tidak membandingkan sesi atau pengguna. Pesan error menyuruh Anda menghapus blok tersebut, tetapi [menghapus hanya blok itu tidak cukup](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#remove-by-hand). [Error lain](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#similar-errors) dapat terlihat mirip.

Jika aplikasi tersebut bukan milik Anda, mulailah percakapan baru dan beri tahu pengelolanya. Jika Anda [menghapus rahasia, data pribadi, atau teks yang disisipkan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#remove-sensitive-content), atau permintaan Anda [menonaktifkan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#turning-thinking-off), [hapus pemikiran secara manual](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#remove-by-hand) alih-alih melakukan langkah 1.

<Steps>
  <Step title="Hentikan error sekarang">
    Atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`, dan kirim “beta header” ([header beta](https://platform.claude.com/docs/id/api/beta-headers#beta-features-on-other-platforms)) `anthropic-beta: thinking-binding-controls-2026-08-01`. Lakukan ini pada setiap permintaan berikutnya dalam percakapan, karena API tidak menyimpan pengaturan tersebut di antara permintaan. Percakapan yang tersimpan masih memuat perubahan itu, bahkan setelah Anda memperbaiki kode Anda, jadi simpan pengaturan tersebut bersama percakapan itu. Atur `type` ke `"adaptive"`, seperti yang ditunjukkan:

    ```json
    {
      "thinking": {
        "type": "adaptive",
        "block_binding": {
          "prefix_mismatch_behavior": "drop_block"
        }
      }
    }
    ```

    Di SDK, panggil metode Messages beta dan teruskan nilai header-nya, seperti yang dilakukan [program pengujian](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#how-to-tell-whether-your-integration-is-impacted-details). Jika error [masih meminta header](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#setting-not-received), header tersebut tidak sampai.

    Cara itu menghentikan error dengan tidak menyertakan pemikiran yang tidak valid dalam permintaan, tetapi [dapat menambah biaya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost) serta dapat memengaruhi kualitas output dan “latency” (latensi). Permintaan berikutnya berhasil, dan array `input_transformations`-nya mencantumkan setiap blok yang tidak disertakan API dalam permintaan tersebut.

    Jika permintaan Anda tidak mengatur parameter `thinking`, menambahkannya tidak mengubah hal lain, karena [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes) berpikir secara adaptif secara default.
  </Step>

  <Step title="Perbaikan jangka panjang">
    Jadikan integrasi Anda append-only:

    1. Temukan perubahannya. Error dapat menyebutkannya. Untuk menemukan di mana kode Anda membuatnya, jalankan `claude update`, lalu jalankan `/claude-api preserved-thinking-migration` di Claude Code di repositori kode Anda. Atau [cari secara manual](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#find-the-change-details).
    2. Berhenti membuat perubahan tersebut, atau percakapan baru juga dapat mengalami error. [Kirim pembaruan di bagian akhir sebagai gantinya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions).
    3. Terus kirimkan ke setiap percakapan yang sedang berjalan `system` dan `tools` dari [permintaan terakhirnya yang berhasil](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#saved-sessions).
  </Step>
</Steps>

Jika perubahan itu baru saja dilakukan, Anda dapat membatalkannya sebagai gantinya: kembalikan apa yang diubah kode Anda. Pemikiran dari sebelum perubahan menjadi valid kembali. Pemikiran yang dihasilkan sejak saat itu gagal dalam pemeriksaan prefiks, jadi hapus pemikiran tersebut atau terus kirim `"drop_block"`.

## Biaya tidak menyertakan pemikiran

Claude dapat menghabiskan lebih banyak token output untuk menyusun penalaran yang tidak dapat lagi dibacanya. Tidak menyertakan blok-blok tersebut juga membuat cache prompt tidak valid mulai dari blok pertama yang tidak disertakan dan seterusnya.

Ketika sesuatu berubah di setiap giliran, setiap giliran kehilangan pemikiran dari giliran-giliran sebelumnya, sehingga peningkatan tersebut berulang. Jalankan evaluasi (evals) pada beban kerja Anda sendiri sebelum Anda mengandalkan `"drop_block"`.

<Frame>
  ![Empat permintaan setelah sebuah perubahan: yang pertama ditolak; tiga berikutnya tidak menyertakan pemikiran lama dan mempertahankan setiap blok baru](https://platform.claude.com/docs/id/images/preserved-thinking-drop-block-loss.svg)
</Frame>

Gunakan `"drop_block"` untuk menjaga percakapan yang sudah ada tetap berjalan selama percakapan tersebut masih memuat perubahan yang sedang Anda perbaiki, dan untuk tindakan tidak menyertakan blok yang direncanakan, seperti [setelah ringkasan Anda sendiri](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#own-summary). Jangan biarkan pengaturan ini tetap aktif untuk menyembunyikan perubahan yang terus dibuat kode Anda. Anda dapat [berhenti mengirimkannya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost-details) setelah blok yang tidak valid sudah keluar dari riwayat.

## Temukan apa yang diubah kode Anda

Perubahan berada sebelum blok pertama yang disebutkan API. Error 400 dapat menyebutkan apa yang berubah, seperti `system`, `tools`, blok pemikiran yang hilang, atau pesan pertama yang berbeda. Jika tidak ada error, atau error-nya tidak menyebutkannya, [mulailah dari apa yang Anda miliki](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#find-the-change-details), seperti entri `prefix_binding_mismatch` atau token output yang lebih banyak.

## Uji kode Anda terhadap kegagalan pemeriksaan prefiks

Anda dapat memercayai sebuah pengujian setelah Anda melihatnya gagal. Pertama, melalui kode Anda sendiri, jalankan sesi yang membuat Claude berpikir, dan ubah sesuatu dengan sengaja. Kirim `"drop_block"` untuk langkah ini, sehingga respons mencantumkan setiap blok yang tidak valid alih-alih berhenti di blok pertama, seperti yang ditunjukkan oleh [lima langkah dan sebuah program](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#how-to-tell-whether-your-integration-is-impacted-details).

Kemudian hapus perubahan itu, dan jalankan sesi nyata Anda. Pada setiap permintaan, kirim header beta `thinking-binding-controls-2026-08-01`, dan atur [`prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls) ke `"error"`, sehingga perubahan yang dibuat kode Anda dalam sesi tersebut menggagalkan build dengan error 400.

Uji sesi yang melakukan compaction, menambahkan alat belakangan, mengubah instruksi, [beralih model](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models), atau dilanjutkan kembali: giliran biasa tidak menjangkau kode tersebut.

Proses yang bersih tidak memiliki entri `prefix_binding_mismatch` dan tidak ada error. Proses tersebut hanya menunjukkan bahwa blok yang diperiksanya valid, dalam sesi yang Anda jalankan. Proses tersebut tidak membuktikan apa pun jika:

* sesi tidak memiliki blok pemikiran
* kode Anda menghapus semua pemikiran, atau model tidak memiliki pemikiran yang dipertahankan
* Anda tidak mengirim header beta, dan [model mungkin meloloskan blok yang gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes) tanpa error

## Pantau produksi, dan temukan penalaran yang hilang tanpa error

Catat setiap error 400, dan [tangani dalam kode](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#handle-the-error-in-code) agar percakapan tetap berlanjut. Jika Anda justru tidak menyertakan `prefix_mismatch_behavior` dalam permintaan, [pantau lalu lintas produksi](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#watch-production-traffic) untuk pemikiran yang gagal dalam pemeriksaan prefiks yang sampai ke Claude.

Penalaran dapat hilang tanpa error melalui `"drop_block"`, item batch, peralihan model, perpindahan ke [akun lain](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking), atau kode yang tidak mengirim kembali pemikiran apa pun. Dengan header beta, masing-masing meninggalkan entri kecuali yang terakhir. Untuk yang terakhir itu, periksa bahwa permintaan Anda memuat blok `thinking`.

## Detail teknis

### Apa lagi yang dapat disebutkan pesan error

Pesan error selanjutnya menyebutkan apa yang berubah, jika API dapat mengetahuinya, seperti `system`, `tools`, pesan atau blok pertama yang berbeda, konten yang hilang atau baru, atau blok pemikiran sebelumnya yang hilang atau tidak berurutan. Susunan kata kalimat itu dapat berubah, jadi jangan melakukan pencocokan terhadapnya. Jika permintaan tidak memiliki header beta, pesan error menambahkan kalimat ini:

```text wrap
That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.
```

### Error masih meminta header, atau menyatakan `Extra inputs are not permitted`

Jika error masih meminta header, header tersebut tidak sampai ke API: proxy atau library mungkin telah menghapusnya. Error yang berbeda, yang diakhiri dengan `block_binding: Extra inputs are not permitted`, berarti hal yang sama, atau bahwa pemikiran dinonaktifkan.

### Hapus pemikiran yang tidak valid secara manual

Gunakan cara ini ketika Anda tidak dapat mengirim pengaturan tersebut, atau dalam salah satu kasus berikut:

* Setelah Anda menghapus rahasia, data pribadi, atau teks yang disisipkan, karena `"drop_block"` membiarkan pemikiran tetap ada di riwayat tersimpan Anda.
* Ketika pemikiran dinonaktifkan (`"disabled"` atau `"between_tools"`), karena `"drop_block"` memerlukan `"adaptive"`, yang akan mengaktifkan pemikiran dan menambah token output.

1. Hapus blok yang disebutkan error, serta setiap blok `thinking` dan [`redacted_thinking`](https://platform.claude.com/docs/id/build-with-claude/thinking#redacted-thinking-blocks) setelahnya, atau error yang sama kemudian akan menyebutkan blok tidak valid berikutnya. Namun, jika riwayat Anda memuat pesan `role: "system"`, atau dua pesan dengan peran yang sama secara berturut-turut, hapus setiap blok `thinking` dan `redacted_thinking`. Error menghitung pesan semacam itu sebagai bagian dari pesan sebelumnya, sehingga posisi yang disebutkannya dapat lebih rendah daripada indeks dalam array Anda. `path` dari entri `input_transformations` menghitung setiap pesan secara terpisah.
2. Pertahankan setiap blok lainnya, dan kirim permintaan lagi. Jangan kembalikan blok yang telah dihapus.

### Error yang terlihat seperti ini

Error berikut tidak menyatakan bahwa blok terikat ke percakapan lain, dan mengatur `prefix_mismatch_behavior` mungkin tidak menghilangkannya:

* Pesan yang berhenti setelah “Invalid `signature` in `thinking` block”, menyatakan “cannot be modified”, atau tentang `budget_tokens`: [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting)
* Pesan tentang `temperature` atau balasan yang diisi sebelumnya: [Batasan dan kompatibilitas fitur](https://platform.claude.com/docs/id/build-with-claude/thinking#limits-and-feature-compatibility)

### Kapan Anda dapat berhenti mengirim `"drop_block"`

Untuk berhenti mengirim `"drop_block"`, hapus blok yang tidak disertakannya dalam permintaan dan pertahankan pemikiran yang dihasilkan sejak saat itu. Jika tidak ada hal lain yang berubah, percakapan kemudian lolos dengan `"error"`.

### Tangani error dalam kode

Untuk menangani error dalam kode, kirim header beta dan `"error"` pada setiap permintaan, sehingga kegagalan pemeriksaan prefiks menjadi error 400 di setiap model. Ketika error itu muncul, alihkan hanya percakapan tersebut ke `"drop_block"` untuk setiap permintaan berikutnya, simpan pilihan itu bersama percakapan tersebut, kirim lagi satu kali, dan catat error-nya. Jika error yang sama muncul kembali, pengaturan tersebut tidak sampai ke API: lihat [Error masih meminta header, atau menyatakan `Extra inputs are not permitted`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#setting-not-received).

Kode Anda harus mengenali error ini dari field `message`-nya, sebagai pengecualian dari saran umum untuk tidak mencocokkan teks error. Setiap error 400 memiliki tipe `invalid_request_error`, dan error ini tidak memiliki `error.details.error_code`. Cocokkan hanya pada “The block is bound to a different conversation”, karena sisa pesannya dapat berubah.

### Anda tidak mendapatkan error, atau error-nya tidak menyebutkan apa yang berubah

* **Error 400, dan tidak menyebutkan perubahan apa pun:** Bandingkan sendiri permintaan-permintaannya. Salah satu penyebabnya adalah blok compaction yang dikirim tanpa menghapus pesan-pesan yang diringkasnya.

* **Entri `prefix_binding_mismatch`:** Bandingkan `system`, `tools`, dan `messages` hingga `path` entri pertama dengan percakapan sebagaimana adanya saat blok tersebut dihasilkan. Jika setiap blok tercantum, mulailah dengan `system` dan `tools`.

  Jika tidak ada yang berbeda, cari [URL gambar atau dokumen yang kontennya berubah](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#files-by-id), daftar alat server MCP yang berubah (lihat [Sematkan daftar alat server MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#pin-mcp-tool-list)), atau blok pemikiran yang tidak disertakan, dipindahkan, atau dikembalikan. Tanpa log permintaan, kirim permintaan lagi dengan `"error"`, dan baca kalimat yang menyatakan apa yang berbeda, jika ada.

* **Proxy atau library yang bukan milik Anda, berada di antaranya:** Bandingkan apa yang dikirimnya dengan apa yang Anda kirim, dan arahkan pengelolanya ke [Library, proxy, dan gateway](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#libraries-proxies-gateways).

* **Hanya dugaan, dan tidak ada Claude Code:** Rekam body permintaan dari sebuah percakapan, yang memiliki compaction atau perubahan alat. Bandingkan masing-masing dengan yang sebelumnya, tanpa menyertakan giliran-giliran barunya.

### Lima langkah untuk pengujian yang dapat gagal, dan program yang menjalankannya

1. Dalam kode Anda sendiri, kirim header beta dan `"drop_block"` pada setiap permintaan dari sebuah sesi, ke [model dengan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes).
2. Gunakan prompt yang membuat Claude berpikir, dan periksa bahwa respons pertama memiliki blok `thinking`. Dengan pemikiran adaptif, Claude dapat melewatkan pemikiran pada prompt yang mudah.
3. Gagalkan pengujian hanya pada entri `input_transformations` yang alasannya adalah `prefix_binding_mismatch`. Pengujian yang mengharapkan array kosong juga gagal setelah peralihan model, karena entri dengan `model_binding_mismatch` atau `organization_binding_mismatch` memang diharapkan pada saat itu.
4. Ubah sesuatu dengan sengaja, seperti menambahkan prompt `system` hanya pada permintaan ketiga.
5. Periksa bahwa `input_transformations` mencantumkan blok pemikiran yang berada setelah perubahan. Jika tidak mencantumkan apa pun, periksa bahwa riwayat memuat blok pemikiran.

Program ini melakukan langkah 1, 2, 4, dan 5. Program ini mencetak berapa banyak blok pemikiran dan entri `input_transformations` yang dimiliki setiap respons, lalu setiap entri, yang merupakan hal yang diperiksa oleh langkah 3:

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan lebih banyak logika daripada satu perintah shell. Gunakan [Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan lebih banyak logika daripada satu perintah shell. Gunakan [Anthropic SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) untuk menjalankannya.
  </CodeGroupItem>

  ```python Python
  client = anthropic.Anthropic()

  user_turns = [
      "How many positive integers below 500 have exactly 6 positive divisors?",
      "How many have exactly 8?",
      "How many have exactly 10?",
  ]

  messages = []
  for turn, user_turn in enumerate(user_turns, start=1):
      messages.append({"role": "user", "content": user_turn})
      response = client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=16000,
          thinking={
              "type": "adaptive",
              "block_binding": {"prefix_mismatch_behavior": "drop_block"},
          },
          # Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
          system="Answer briefly." if turn == len(user_turns) else anthropic.omit,
          messages=messages,
          betas=["thinking-binding-controls-2026-08-01"],
      )
      messages.append({"role": "assistant", "content": response.content})
      thinking_blocks = sum(block.type == "thinking" for block in response.content)
      entries = response.input_transformations or []
      print(f"thinking blocks: {thinking_blocks}, entries: {len(entries)}")
      for entry in entries:
          if entry.type == "thinking_dropped":
              print(entry.type, entry.path, entry.reason)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const userTurns = [
    "How many positive integers below 500 have exactly 6 positive divisors?",
    "How many have exactly 8?",
    "How many have exactly 10?"
  ];

  const messages: Anthropic.Beta.BetaMessageParam[] = [];
  for (const [turnIndex, userTurn] of userTurns.entries()) {
    messages.push({ role: "user", content: userTurn });
    const response = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 16000,
      thinking: {
        type: "adaptive",
        block_binding: { prefix_mismatch_behavior: "drop_block" }
      },
      // Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
      system: turnIndex === userTurns.length - 1 ? "Answer briefly." : undefined,
      messages,
      betas: ["thinking-binding-controls-2026-08-01"]
    });
    messages.push({ role: "assistant", content: response.content });
    const thinkingBlocks = response.content.filter((block) => block.type === "thinking");
    const entries = response.input_transformations ?? [];
    console.log(`thinking blocks: ${thinkingBlocks.length}, entries: ${entries.length}`);
    for (const entry of entries) {
      if (entry.type === "thinking_dropped") {
        console.log(entry.type, entry.path, entry.reason);
      }
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  string[] userTurns =
  [
      "How many positive integers below 500 have exactly 6 positive divisors?",
      "How many have exactly 8?",
      "How many have exactly 10?",
  ];

  List<BetaMessageParam> messages = [];
  foreach (var (turnIndex, userTurn) in userTurns.Index())
  {
      messages.Add(new BetaUserMessageParam { Content = userTurn });
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
              // Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
              System = turnIndex == userTurns.Length - 1 ? new("Answer briefly.") : null,
              Messages = messages,
              Betas = [AnthropicBeta.ThinkingBindingControls2026_08_01],
          }
      );
      messages.Add(new BetaAssistantMessageParam
      {
          Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      });
      var thinkingBlocks = response.Content.Count(block => block.TryPickThinking(out _));
      var entries = response.InputTransformations ?? [];
      Console.WriteLine($"thinking blocks: {thinkingBlocks}, entries: {entries.Count}");
      foreach (var entry in entries)
      {
          if (entry.TryPickThinkingDropped(out var dropped))
          {
              Console.WriteLine($"{dropped.Type} {dropped.Path} {dropped.Reason.Raw()}");
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  userTurns := []string{
  	"How many positive integers below 500 have exactly 6 positive divisors?",
  	"How many have exactly 8?",
  	"How many have exactly 10?",
  }

  messages := []anthropic.BetaMessageParam{}
  for turnIndex, userTurn := range userTurns {
  	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(userTurn)))
  	// Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
  	var system []anthropic.BetaTextBlockParam
  	if turnIndex == len(userTurns)-1 {
  		system = []anthropic.BetaTextBlockParam{{Text: "Answer briefly."}}
  	}
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
  		System:   system,
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
  	fmt.Printf("thinking blocks: %d, entries: %d\n", thinkingBlocks, len(response.InputTransformations))
  	for _, entry := range response.InputTransformations {
  		if entry.Type == "thinking_dropped" {
  			fmt.Println(entry.Type, entry.Path, entry.Reason)
  		}
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaContentBlock;
  import com.anthropic.models.beta.messages.BetaInputTransformation;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      List<String> userTurns = List.of(
          "How many positive integers below 500 have exactly 6 positive divisors?",
          "How many have exactly 8?",
          "How many have exactly 10?");

      MessageCreateParams.Builder conversation = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(16000L)
          .thinking(BetaThinkingConfigAdaptive.builder()
              .blockBinding(BetaThinkingBlockBinding.builder()
                  .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.DROP_BLOCK)
                  .build())
              .build())
          .addBeta(AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01);

      for (int turnIndex = 0; turnIndex < userTurns.size(); turnIndex++) {
          if (turnIndex == userTurns.size() - 1) {
              // Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
              conversation.system("Answer briefly.");
          }
          conversation.addUserMessage(userTurns.get(turnIndex));
          BetaMessage response = client.beta().messages().create(conversation.build());
          conversation.addMessage(response);
          long thinkingBlocks = response.content().stream()
              .filter(BetaContentBlock::isThinking)
              .count();
          List<BetaInputTransformation> entries = response.inputTransformations().orElse(List.of());
          IO.println("thinking blocks: " + thinkingBlocks + ", entries: " + entries.size());
          for (BetaInputTransformation entry : entries) {
              entry.thinkingDropped().ifPresent(dropped ->
                  IO.println(entry.type() + " " + dropped.path() + " " + dropped.reason()));
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaThinkingBlock;
  use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
  use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
  use Anthropic\Beta\Messages\BetaThinkingDroppedInputTransformation;
  use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
  use Anthropic\Client;
  use Anthropic\Messages\Model;

  $client = new Client();

  $userTurns = [
      'How many positive integers below 500 have exactly 6 positive divisors?',
      'How many have exactly 8?',
      'How many have exactly 10?',
  ];

  $messages = [];
  foreach ($userTurns as $turnIndex => $userTurn) {
      $messages[] = ['role' => 'user', 'content' => $userTurn];
      $response = $client->beta->messages->create(
          model: Model::CLAUDE_OPUS_5_5,
          maxTokens: 16000,
          thinking: BetaThinkingConfigAdaptive::with(
              blockBinding: BetaThinkingBlockBinding::with(
                  prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::DROP_BLOCK,
              ),
          ),
          // Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
          system: $turnIndex === array_key_last($userTurns) ? 'Answer briefly.' : null,
          messages: $messages,
          betas: [AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
      );
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $thinkingBlocks = array_filter(
          $response->content,
          fn ($block) => $block instanceof BetaThinkingBlock,
      );
      $entries = $response->inputTransformations ?? [];
      echo 'thinking blocks: ', count($thinkingBlocks), ', entries: ', count($entries), PHP_EOL;
      foreach ($entries as $entry) {
          if ($entry instanceof BetaThinkingDroppedInputTransformation) {
              echo $entry->type, ' ', $entry->path, ' ', $entry->reason, PHP_EOL;
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_turns = [
    "How many positive integers below 500 have exactly 6 positive divisors?",
    "How many have exactly 8?",
    "How many have exactly 10?"
  ]

  messages = []
  user_turns.each_with_index do |user_turn, turn_index|
    messages << { role: "user", content: user_turn }
    # Hanya permintaan terakhir yang menambahkan prompt sistem, yang sengaja mengubah prefiks
    system_param = (turn_index == user_turns.length - 1) ? { system_: "Answer briefly." } : {}
    response = client.beta.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 16_000,
      thinking: {
        type: "adaptive",
        block_binding: { prefix_mismatch_behavior: "drop_block" }
      },
      messages: messages,
      betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
      **system_param
    )
    messages << { role: "assistant", content: response.content }
    thinking_blocks = response.content.count { |block| block.is_a?(Anthropic::Beta::BetaThinkingBlock) }
    entries = response.input_transformations || []
    puts "thinking blocks: #{thinking_blocks}, entries: #{entries.length}"
    entries.each do |entry|
      if entry.is_a?(Anthropic::Beta::BetaThinkingDroppedInputTransformation)
        puts "#{entry.type} #{entry.path} #{entry.reason}"
      end
    end
  end
  ```
</CodeGroup>

```text Output wrap
thinking blocks: 1, entries: 0
thinking blocks: 1, entries: 0
thinking blocks: 1, entries: 2
thinking_dropped messages.1.content.0 prefix_binding_mismatch
thinking_dropped messages.3.content.0 prefix_binding_mismatch
```

Dengan `"error"` sebagai pengganti `"drop_block"`, permintaan ketiga mendapatkan [error 400](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#prefix-mismatch-error).

### Arti setiap entri `input_transformations`, dan mana yang perlu Anda perbaiki

Dengan header beta, respons dari model yang mendukung pemikiran memiliki array `input_transformations` di samping `usage`. Array ini kosong ketika tidak ada blok yang tidak disertakan dan tidak ada blok tidak valid yang diloloskan. Saat Anda melakukan “streaming” (streaming), array ini berada di `message` dari event `message_start`; setelah fallback di tengah stream, event `message_delta` terakhir membawa array yang berlaku. Tidak seperti posisi pada error, `path` selalu merupakan posisi blok sebagaimana Anda mengirimkannya:

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

`type` dan `reason` setiap entri, beserta artinya:

* **`thinking_dropped`, `prefix_binding_mismatch`:** Apa yang ada sebelum blok ini bukan lagi yang dicatatnya. Perlu Anda perbaiki: [Temukan apa yang diubah kode Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#find-the-change).
* **`thinking_mismatch_allowed`, `prefix_binding_mismatch`:** Sama seperti di atas, tetapi Claude membaca blok tersebut tanpa perubahan, dan blok tersebut ditagih. Entri ini hanya muncul jika pengaturan tersebut tidak disertakan dalam permintaan, pada [beberapa model](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes). Perlu Anda perbaiki.
* **`thinking_dropped`, `model_binding_mismatch`:** Model ini tidak dapat membaca blok dari model yang menghasilkannya. Bukan untuk Anda perbaiki: [terus kirim seluruh percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).
* **`thinking_dropped`, `organization_binding_mismatch`:** Akun lain yang menghasilkan blok tersebut, sehingga [API tidak menyertakannya dalam permintaan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking). Bukan untuk Anda perbaiki.

Abaikan entri yang `type` atau `reason`-nya tidak Anda kenali.

### Batch dan penghitungan token

* **[Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing):** Item yang tidak menyertakan `prefix_mismatch_behavior` tidak pernah mendapatkan error 400. API tidak menyertakan blok yang tidak valid dalam permintaan, atau, pada [beberapa model](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes), dapat meloloskannya. Item yang mengatur `"error"` diselesaikan sebagai `errored` ketika sebuah blok gagal dalam pemeriksaan prefiks. `block_binding` ditempatkan di `params.thinking` milik item tersebut.
* **[Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting):** Di Claude API, penghitungan token dapat mengembalikan error 400 yang sama, dan menerima `prefix_mismatch_behavior` dengan header yang sama. Penghitungan token tidak memasukkan blok yang tidak disertakan ke dalam hitungan, dan tidak mengembalikan `input_transformations`.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks" icon="edit" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions">
    Apa yang harus dikirim sebagai ganti setiap perubahan yang dibuat kode Anda pada sebuah percakapan.
  </Card>

  <Card title="Pemikiran yang dipertahankan" icon="book" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking">
    Apa itu pemikiran yang dipertahankan, ke apa sebuah blok pemikiran terikat, serta beralih model atau akun.
  </Card>

  <Card title="Pemecahan masalah thinking" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting">
    Perbaikan untuk error pemikiran lainnya, seperti signature yang tidak dapat diverifikasi.
  </Card>
</CardGroup>
