---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 9d51c72e7a45f9e5a2820ec8a0a9e4e8a1545df6b27181b18c1cbe17200638aa
---

---
title: Yang baru di Claude Sonnet 5.5
url: https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5
description: "Apa yang berubah saat Anda beralih dari Claude Sonnet 5 ke Claude Sonnet 5.5: perubahan yang merusak kompatibilitas, dukungan fitur, perbedaan perilaku, harga, dan ketersediaan."
---

Claude Sonnet 5.5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan. Lima "breaking change" (perubahan yang merusak kompatibilitas) memengaruhi kode yang sudah berjalan di Claude Sonnet 5:

* [Matikan pemikiran di awal dengan `between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking).
* [Penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#forced-tool-use-is-not-supported).
* [Blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them).
* [Di Claude API dan Google Cloud, alat computer use `computer_20251124` yang lebih lama tidak diterima](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#computer-20251124-is-not-supported).
* [Alat advisor menolak Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5 sebagai advisor](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#advisor-tool-pairings).

Satu perubahan lagi mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara pemanggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#text-between-tool-calls). Aplikasi yang melakukan streaming teks tersebut kepada penggunanya akan menjadi senyap di antara pemanggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks, atau mematikan pemikiran di awal dengan `between_tools`.

## Model baru

| Model             | ID Claude API     | Deskripsi                                         |
| ----------------- | ----------------- | ------------------------------------------------- |
| Claude Sonnet 5.5 | claude-sonnet-5-5 | Kombinasi terbaik antara kecepatan dan kecerdasan |

["Adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) mengontrol kedalaman pemikiran. Nilai default-nya di Claude API adalah `high`. Tokenizer-nya sama dengan milik Claude Sonnet 5, sehingga teks yang sama menghasilkan jumlah token yang sama. Untuk "context window" (jendela konteks), batas output, batas pengetahuan, dan harga, lihat [halaman model Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview).

Untuk semua model saat ini, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Matikan pemikiran di awal dengan `between_tools`

Untuk mematikan pemikiran di awal pada Claude Sonnet 5.5, kirim `thinking: {"type": "between_tools"}` alih-alih `"disabled"`. Ini adalah pengaturan pemikiran terendah pada model ini. Pengaturan ini tersedia di setiap platform yang menawarkan Claude Sonnet 5.5. Pengaturan ini tidak memerlukan beta header. [Pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) singkat yang ditulis model di antara pemanggilan alat tetap dikembalikan sebagai blok `thinking` beserta teks ringkasannya. Kirimkan kembali blok-blok tersebut tanpa perubahan bersama sisa giliran asisten. Blok pembaruan progres yang Anda kirim kembali memberikan model catatan lengkap yang ditulisnya, bukan ringkasannya. Jika permintaan Anda tidak menggunakan alat, respons hanya berisi teks, seperti halnya `disabled` pada Claude Sonnet 5.

Pada Claude Sonnet 5.5, permintaan yang mengirim `thinking: {"type": "disabled"}` mengembalikan 400 `invalid_request_error` yang pesannya mengarahkan ke `between_tools`.

`between_tools` diterima pada effort `low`, `medium`, dan `high`. Pada effort `xhigh` atau `max`, permintaan dengan `between_tools` mengembalikan error 400. Untuk berjalan pada `xhigh` atau `max`, gunakan pemikiran adaptif: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`, yang setara. Dengan `between_tools`, effort tidak dapat berubah di tengah percakapan: `output_config.effort` [per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) yang berbeda dari level yang sedang berlaku mengembalikan error 400. Untuk memvariasikan effort per giliran, gunakan pemikiran adaptif.

`between_tools` tidak menerima field lain: `display`, `budget_tokens`, atau `block_binding` yang dikirim bersamanya mengembalikan error 400. Anggaran pemikiran manual (`thinking: {"type": "enabled", "budget_tokens": N}`) mengembalikan error 400. Lihat [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) dan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking) di panduan migrasi.

### Penggunaan alat paksa tidak didukung

Claude Sonnet 5.5 tidak mendukung "forced tool use" (penggunaan alat paksa). `tool_choice` yang diatur ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan 400 `invalid_request_error`:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` didukung. Pemeriksaan yang sama berlaku untuk endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting). Untuk input alat yang valid sesuai skema, pertahankan `tool_choice: {"type": "auto"}` dan atur `strict: true` dengan [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau pindahkan skema ke [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs). Agar model memanggil alat alih-alih membalas dengan teks, sebutkan dalam prompt kapan alat tersebut berlaku. Panduan migrasi menunjukkan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#forced-tool-use).

### Blok pemikiran terikat pada model dan percakapan

Setiap blok pemikiran mencatat model mana yang menghasilkannya. Setiap model membaca bloknya sendiri dan hanya blok dari sebagian model lain. Claude Sonnet 5.5 membaca blok pemikiran dari Claude Sonnet 5, Claude Opus 4.8, Claude Haiku 4.5, dan model-model sebelumnya, tetapi tidak dari Claude Opus 5, Claude Opus 5.5, atau model Claude Fable maupun Claude Mythos mana pun. Di Claude API dan Google Cloud, Claude Opus 5.5 membaca blok pemikiran Claude Sonnet 5.5; tidak ada model lain yang melakukannya.

Jadi, percakapan yang berpindah dari Claude Sonnet 5 ke Claude Sonnet 5.5, atau dari Claude Sonnet 5.5 naik ke Claude Opus 5.5 di Claude API dan Google Cloud, mempertahankan penalarannya, dan perpindahan lain apa pun dari Claude Sonnet 5.5 menjalankan giliran setelah peralihan tanpa penalaran tersebut. Ketika permintaan membawa blok yang tidak dapat dibaca oleh model target, API membuangnya sebelum model melihatnya: permintaan berhasil, dan blok yang dibuang tidak ditagih. Dengan beta header `thinking-binding-controls-2026-08-01`, pembuangan tersebut dilaporkan dalam array `input_transformations` tingkat atas. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

API juga memeriksa apakah ada sesuatu sebelum blok pemikiran Claude Sonnet 5.5 yang telah berubah sejak blok tersebut dihasilkan: prompt `system`, `tools`, atau pesan sebelumnya. API memberlakukan pemeriksaan tersebut secara default untuk akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC, di Claude API, Amazon Bedrock, dan Google Cloud. Pada akun-akun tersebut, permintaan yang memutar ulang blok setelah perubahan semacam itu mengembalikan error 400. Untuk membuang blok yang terpengaruh sebagai gantinya, kirim beta header `thinking-binding-controls-2026-08-01` dan atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Pada akun yang lebih lama, mengatur field tersebut ke salah satu nilai akan mengikutsertakan permintaan. `block_binding` hanya berfungsi dengan `thinking: {"type": "adaptive"}`. Dengan `between_tools`, pertahankan riwayat hanya-tambah (append-only), atau hapus blok pemikiran mulai dari giliran yang diedit dan seterusnya.

Pertahankan percakapan hanya-tambah agar pemeriksaan tidak pernah gagal: ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih melakukan pengeditan. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan [catatan tentang perubahan ini](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-blocks) di panduan migrasi.

### Alat computer use `computer_20251124` tidak didukung di Claude API dan Google Cloud

Di Claude API dan Google Cloud, Claude Sonnet 5.5 mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) hanya melalui toolset `computer_toolset_20260801`. Permintaan yang mendeklarasikan alat `computer_20251124` yang lebih lama mengembalikan 400 `invalid_request_error`. Di Claude API, pesan tersebut menyebutkan tipe yang ditolak, lalu mencantumkan tipe alat yang diterima model. Pesan tersebut diawali dengan:

```text wrap
'claude-sonnet-5-5' does not support tool types: computer_20251124.
```

Di Amazon Bedrock, Claude Sonnet 5.5 menerima alat `computer_20251124` yang lebih lama.

Untuk memindahkan integrasi yang sudah ada di Claude API atau Google Cloud, ikuti [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124), yang menunjukkan permintaan sebelum dan sesudah. Hapus beta header, ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`, dan perbarui loop agen Anda untuk blok `tool_use` anggota, aksi batch, dan `toolset_name` pada hasil. Toolset ini tersedia di Claude API dan Google Cloud. Untuk platform lain, lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use. Integrasi yang sudah menggunakan toolset, serta [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool), tidak memerlukan perubahan.

### Beberapa pasangan alat advisor tidak didukung

Dengan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) (beta), executor Claude Sonnet 5.5 memerlukan Claude Mythos 5.1, Claude Fable 5.1, Claude Mythos 5, Claude Fable 5, Claude Opus 5.5, atau Claude Opus 5 sebagai advisor-nya, atau Claude Sonnet 5.5 itu sendiri. Advisor Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5 berfungsi dengan executor Claude Sonnet 5, tetapi dengan executor Claude Sonnet 5.5 mereka mengembalikan 400 `invalid_request_error`. Setiap advisor yang diterima Claude Sonnet 5.5 mengembalikan sarannya dalam bentuk terenkripsi, sebagai blok `advisor_redacted_result`, sehingga klien Anda tidak dapat membaca teks saran tersebut. Lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility) dan [Varian hasil](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#result-variants) pada alat advisor.

## Dukungan fitur

Claude Sonnet 5.5 mendukung [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta), [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), [perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) (beta), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) dengan prompt minimum yang dapat di-cache sebesar 512 token, [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Effort per pesan, pesan sistem di tengah percakapan, dan perubahan alat di tengah percakapan tidak tersedia di Claude Sonnet 5, yang prompt minimum yang dapat di-cache-nya adalah 1.024 token. Di Claude API dan Google Cloud, computer use memerlukan toolset `computer_toolset_20260801` (lihat [perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#computer-20251124-is-not-supported)). Lihat halaman masing-masing fitur untuk ketersediaan model.

### Compact sesuai permintaan (beta)

Dengan beta header `compact-2026-09-04`, permintaan yang mengirim parameter `compaction` tingkat atas mengembalikan blok `compaction` bertanda tangan yang merangkum seluruh percakapan. Anda kemudian mengirim blok tersebut terlebih dahulu, menggantikan pesan-pesan yang dirangkum. Anda memilih kapan melakukan compact, dan blok pemikiran dalam giliran yang Anda pertahankan dapat tetap valid setelah penggantian, dengan ketentuan yang dijelaskan di [Compaction dan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid). Hal ini penting pada Claude Sonnet 5.5 karena [blok pemikirannya terikat pada percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them). Lihat [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) untuk ketersediaan platform dan alur permintaan lengkap.

### Definisikan alat dalam pesan (beta)

Dengan beta header `inline-tools-2026-09-15`, blok `tool_addition` dalam pesan sistem di tengah percakapan dapat membawa definisi alat lengkap alih-alih referensi. Anda dapat menambahkan alat, mengubah skemanya, atau memindahkan alat server ke versi yang lebih baru di tengah percakapan tanpa mengedit `tools` dan tanpa kehilangan cache prompt. Lihat [Definisikan alat dalam pesan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta).

### Blok pemikiran tetap berada pada akun yang menghasilkannya

Blok pemikiran yang dihasilkan Claude Sonnet 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya. Ketika akun lain mengirim salah satu blok ini, API membuang blok tersebut sebelum model melihatnya, dan permintaan berhasil. Di Claude API dan Google Cloud, dengan beta header `thinking-binding-controls-2026-08-01`, respons mencantumkan setiap blok yang dibuang dalam `input_transformations` dengan `reason: "organization_binding_mismatch"`. Blok dari model-model sebelumnya tidak terpengaruh. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

## Perbedaan perilaku

Claude Sonnet 5.5 berbeda dari Claude Sonnet 5 dalam beberapa hal yang muncul tanpa perubahan kode apa pun. [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) memiliki panduan untuk masing-masing:

* **Level effort dikalibrasi ulang.** Level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) tidak menghasilkan jumlah pemikiran yang sama seperti pada Claude Sonnet 5. Jalankan ulang pengujian effort Anda alih-alih membawa pengaturan lama. Mulailah dari `high` kecuali beban kerja Anda bersifat agentik atau sensitif terhadap "latency" (latensi). Untuk coding agentik dan penggunaan alat multilangkah, mulailah dari `medium` untuk tugas yang terdefinisi dengan baik dan naikkan ke `high` untuk tugas yang lebih sulit atau lebih panjang. Untuk chat dan pekerjaan lain yang sensitif terhadap latensi, mulailah dari `medium` atau `low`.
* **Teks di antara pemanggilan alat dikembalikan dalam blok pemikiran.** Di antara pemanggilan alat, catatan yang lebih panjang dari satu atau dua kalimat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates). Komentar yang lebih pendek tetap berupa `text`. Pada default `display: "omitted"`, teks blok pembaruan progres kosong, sehingga aplikasi yang melakukan streaming catatan tersebut kepada penggunanya menjadi senyap di antara pemanggilan alat, tanpa error. Jika Anda [mematikan pemikiran di awal dengan `between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking), teks tersebut dikembalikan. [Panduan migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls) menunjukkan cara menerimanya.
* **Kategori safeguard.** Safeguard model dapat menolak permintaan dalam lima [kategori `stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response). `"cyber"` berarti permintaan tersebut dapat memungkinkan bahaya siber. `"bio"` berarti permintaan tersebut dapat memungkinkan bahaya biologis. `"frontier_llm"` berarti permintaan tersebut dapat membantu pengembangan model AI pesaing. `"reasoning_extraction"` berarti permintaan tersebut meminta model untuk mereproduksi penalaran internalnya dalam teks respons. `"general_harms"` berarti permintaan tersebut termasuk dalam area kebijakan penggunaan lainnya. Lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#refusals-fallback-and-billing).

## Penolakan, fallback, dan penagihan

Semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku untuk Claude Sonnet 5.5. Permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakannya. Tangani penolakan dan konfigurasikan fallback. [Fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (`fallbacks: "default"`, dalam beta, di Claude API) mencoba ulang penolakan `"cyber"` dan `"frontier_llm"` pada Claude Sonnet 5. Fallback ini tidak mencoba ulang penolakan `"bio"`, `"reasoning_extraction"`, atau `"general_harms"`. Anda juga dapat menggunakan [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) atau mekanisme percobaan ulang Anda sendiri. Apakah penolakan yang terjadi sebelum output apa pun ditagih bergantung pada kategori penolakannya, dan penolakan tersebut tetap dihitung terhadap "rate limit" (batas laju) Anda. Lihat [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).

## Harga

Claude Sonnet 5.5 memiliki harga yang sama dengan Claude Sonnet 5, kecuali untuk pembacaan cache prompt, yang berbiaya $0,10 USD per juta token, setengah dari tarif Claude Sonnet 5. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk daftar lengkap, residensi data, dan harga alat.

## Ketersediaan

Claude Sonnet 5.5 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-sonnet-5-5`.
* **AWS:** [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-sonnet-5-5`, dan [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-sonnet-5-5`.
* **Google Cloud:** [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), sebagai `claude-sonnet-5-5`.
* **Microsoft Foundry:** [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-sonnet-5-5`.

## Migrasi dari Claude Sonnet 5

Perbarui ID model Anda:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-sonnet-5"  # Before
  model = "claude-sonnet-5-5"  # After
  ```

  ```typescript TypeScript
  let model = "claude-sonnet-5"; // Before
  model = "claude-sonnet-5-5"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeSonnet5; // Before
  model = Model.ClaudeSonnet5_5; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeSonnet5  // Before
  model = anthropic.ModelClaudeSonnet5_5 // After
  ```

  ```java Java
  Model model = Model.CLAUDE_SONNET_5; // Before
  model = Model.CLAUDE_SONNET_5_5; // After
  ```

  ```php PHP
  $model = Model::CLAUDE_SONNET_5; // Before
  $model = Model::CLAUDE_SONNET_5_5; // After
  ```

  ```ruby Ruby
  model = Anthropic::Model::CLAUDE_SONNET_5 # Before
  model = Anthropic::Model::CLAUDE_SONNET_5_5 # After
  ```
</CodeGroup>

Kemudian periksa enam hal:

1. Jika kode Anda mematikan pemikiran dengan `disabled`, kirim `between_tools` sebagai gantinya, pada effort `high` atau di bawahnya.
2. Ganti tipe `tool_choice` `any` dan `tool` dengan `auto` ditambah [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use).
3. Pertahankan percakapan hanya-tambah. Permintaan yang memutar ulang blok pemikiran Claude Sonnet 5.5 setelah pengeditan pada riwayat sebelumnya dapat mengembalikan error 400. Lihat [Blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them).
4. Jika Anda menggunakan computer use melalui `computer_20251124` di Claude API atau Google Cloud, [pindah ke toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).
5. Jika Anda menggunakan alat advisor dengan advisor Claude Opus 4.8, Claude Opus 4.7, atau Claude Sonnet 5, [beralihlah ke advisor yang diterima Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#advisor-tool-pairings).
6. Jika antarmuka Anda menampilkan teks di antara pemanggilan alat, atur `thinking.display` saat Anda menggunakan pemikiran adaptif. Dengan `between_tools`, teks tersebut dikembalikan tanpa pengaturan itu. Lihat [Teks di antara pemanggilan alat dikembalikan dalam blok thinking](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls).

[Panduan migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide) berisi instruksi langkah demi langkah dari Claude Sonnet 5 dan model-model sebelumnya, serta daftar periksa lengkap.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide">
    Pindahkan kode dari Claude Sonnet 5 dan model-model sebelumnya ke Claude Sonnet 5.5.
  </Card>

  <Card title="Prompting Claude Sonnet 5.5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Sonnet 5.5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif dan cara blok pemikiran dipertahankan.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani `stop_reason: "refusal"` dan coba ulang pada model lain.
  </Card>
</CardGroup>
