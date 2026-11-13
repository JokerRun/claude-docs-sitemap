---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: fd13b1209dcd55d5db060489ef238b57963f081b74b7a04f4cca35bb9eb526c1
---

---
title: Yang baru di Claude Sonnet 5.5
url: https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5
description: "Apa yang berubah saat Anda beralih dari Claude Sonnet 5 ke Claude Sonnet 5.5: perubahan yang merusak kompatibilitas, dukungan fitur, perbedaan perilaku, harga, dan ketersediaan."
---

Claude Sonnet 5.5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan. Lima perubahan yang dapat merusak kompatibilitas dapat memengaruhi kode yang sudah berjalan di Claude Sonnet 5:

* [Matikan pemikiran di awal dengan `between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking).
* [Penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#forced-tool-use-is-not-supported).
* [Blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them).
* [Beberapa versi alat penggunaan komputer tidak didukung](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#computer-20251124-is-not-supported).
* [Alat advisor menolak empat model sebagai advisor](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#advisor-tool-pairings): Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, dan Claude Haiku 5.5.

Satu perubahan lagi mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara pemanggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#text-between-tool-calls). Aplikasi yang melakukan streaming teks tersebut ke penggunanya akan menjadi senyap di antara pemanggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks, atau mematikan pemikiran di awal dengan `between_tools`.

## Model baru

| Model             | ID Claude API     | Deskripsi                                         |
| ----------------- | ----------------- | ------------------------------------------------- |
| Claude Sonnet 5.5 | claude-sonnet-5-5 | Kombinasi terbaik antara kecepatan dan kecerdasan |

[Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) aktif secara default, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) mengontrol kedalaman pemikiran. Nilai default-nya di Claude API adalah `high`. Tokenizer-nya sama dengan milik Claude Sonnet 5, sehingga teks yang sama menghasilkan jumlah token yang sama. Untuk jendela konteks, batas output, batas pengetahuan, dan harga, lihat halaman model [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview).

Untuk semua model saat ini, lihat [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Matikan pemikiran di awal dengan `between_tools`

Untuk mematikan pemikiran di awal pada Claude Sonnet 5.5, kirim `thinking: {"type": "between_tools"}` alih-alih `"disabled"`. Ini adalah pengaturan pemikiran terendah pada model ini. Pengaturan ini tersedia di setiap platform yang menawarkan Claude Sonnet 5.5. [Pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) singkat yang ditulis model di antara pemanggilan alat tetap dikembalikan sebagai blok `thinking` beserta teks ringkasannya. Kirimkan kembali blok-blok tersebut tanpa perubahan bersama sisa giliran asisten. Blok pembaruan progres yang Anda kirim kembali memberi model catatan lengkap yang ditulisnya, bukan ringkasannya. Jika permintaan Anda tidak menggunakan alat, respons hanya berisi teks, seperti halnya `disabled` pada Claude Sonnet 5.

Pada Claude Sonnet 5.5, permintaan yang mengirim `thinking: {"type": "disabled"}` mengembalikan `invalid_request_error` 400 yang pesannya mengarah ke `between_tools`.

`between_tools` diterima pada effort `low`, `medium`, dan `high`. Pada effort `xhigh` atau `max`, permintaan dengan `between_tools` mengembalikan error 400. Untuk berjalan pada `xhigh` atau `max`, gunakan pemikiran adaptif: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`, yang setara. Dengan `between_tools`, effort tidak dapat berubah di tengah percakapan: `output_config.effort` [per pesan](https://platform.claude.com/docs/id/build-with-claude/effort-per-message) yang berbeda dari level yang berlaku akan mengembalikan error 400. Untuk memvariasikan effort di setiap giliran, gunakan pemikiran adaptif.

`between_tools` tidak menerima field lain: `display`, `budget_tokens`, atau `block_binding` yang dikirim bersamanya mengembalikan error 400. Anggaran pemikiran manual (`thinking: {"type": "enabled", "budget_tokens": N}`) mengembalikan error 400. Lihat [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) dan [Matikan pemikiran di awal](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking) dalam panduan migrasi.

### Penggunaan alat paksa tidak didukung

Claude Sonnet 5.5 tidak mendukung penggunaan alat paksa (“forced tool use”). `tool_choice` yang disetel ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan `invalid_request_error` 400:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` didukung. Pemeriksaan yang sama berlaku untuk endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting). Untuk input alat yang valid terhadap skema, pertahankan `tool_choice: {"type": "auto"}` dan setel `strict: true` dengan [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau pindahkan skema ke [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs). Agar model memanggil alat alih-alih membalas dengan teks, sebutkan dalam prompt kapan alat tersebut berlaku. [Penggunaan alat yang dipaksakan tidak didukung](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#forced-tool-use) dalam panduan migrasi menunjukkan kondisi sebelum dan sesudahnya.

### Blok pemikiran terikat pada model dan percakapan

Setiap blok pemikiran mencatat model mana yang menghasilkannya. Percakapan yang berpindah model hanya mempertahankan penalaran sebelumnya jika model yang menjadi tujuan perpindahan dapat membaca blok pemikiran model sebelumnya:

| Perpindahan                                                                                                                        | Mempertahankan penalarannya                                                |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Ke Claude Sonnet 5.5, dari Claude Sonnet 5 atau sebelumnya, Claude Opus 4.8 atau sebelumnya, atau Claude Haiku 4.5 atau sebelumnya | Ya                                                                         |
| Ke Claude Sonnet 5.5, dari Claude Haiku 5.5                                                                                        | Ya, hanya di Claude API dan Claude Models on Google Cloud (Google managed) |
| Ke Claude Sonnet 5.5, dari model lain apa pun                                                                                      | Tidak                                                                      |
| Dari Claude Sonnet 5.5, ke Claude Opus 5.5, Claude Fable 5.2, atau Claude Mythos 5.2                                               | Ya, hanya di Claude API dan Claude Models on Google Cloud (Google managed) |
| Dari Claude Sonnet 5.5, ke model lain apa pun                                                                                      | Tidak                                                                      |

Ketika permintaan membawa blok yang tidak dapat dibaca oleh model target, API tidak menyertakan blok tersebut sebelum model menerimanya. Permintaan berhasil, dan blok yang tidak disertakan tidak ditagih. Dengan header beta `thinking-binding-controls-2026-08-01`, API melaporkan blok yang tidak disertakan tersebut dalam array `input_transformations` tingkat atas. Lihat [Beralih model dan kembali lagi](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models). Untuk peralihan yang tidak melibatkan Claude Sonnet 5.5, lihat [Peralihan model mana yang mempertahankan penalaran di Claude API](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#which-model-switches-keep-reasoning).

API juga memeriksa apakah ada sesuatu sebelum blok pemikiran Claude Sonnet 5.5 yang telah berubah sejak model menghasilkan blok tersebut. “Prefix check” (pemeriksaan prefiks) ini mencakup prompt `system`, `tools`, dan setiap pesan sebelumnya. Pertahankan percakapan tetap “append-only” (hanya ditambahkan): ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), bukan dengan pengeditan.

Gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) mungkin menghasilkan atau mungkin tidak menghasilkan [error 400](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch). Untuk mengidentifikasi dan menangani kedua kasus tersebut, lihat [Pemeriksaan prefiks pada blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks).

Pemeriksaan prefiks berjalan di Claude API dan di [beberapa platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#feature-availability).

Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan [catatan tentang blok pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-blocks) dalam panduan migrasi.

### Beberapa versi alat penggunaan komputer tidak didukung

Claude Sonnet 5.5 mendukung [penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) melalui toolset `computer_toolset_20260801`. Di Amazon Bedrock, Claude Sonnet 5.5 juga menerima alat `computer_20251124` dengan header beta `computer-use-2025-11-24`. Claude Sonnet 5.5 mengembalikan error 400 untuk versi alat penggunaan komputer apa pun yang tidak diterimanya, seperti `computer_20251124` di Claude API. Pesan `invalid_request_error` dari Claude API menyebutkan tipe yang ditolak dan, setelah `Did you mean one of`, mencantumkan tipe alat yang diterima model. Pesan tersebut diawali dengan:

```text wrap
'claude-sonnet-5-5' does not support tool types: computer_20251124.
```

Integrasi yang menggunakan toolset tidak memerlukan perubahan. Untuk memindahkan integrasi `computer_20251124` ke toolset, ikuti [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124), yang menunjukkan permintaan sebelum dan sesudahnya. Hapus header beta dan ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`. Kemudian perbarui loop agen Anda untuk blok `tool_use` anggota, aksi batch, dan `toolset_name` pada hasil.

### Beberapa pasangan alat advisor tidak didukung

[Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) sedang dalam beta. Executor Claude Sonnet 5.5 hanya menerima advisor berikut:

* Claude Mythos 5.2 dan Claude Fable 5.2
* Claude Mythos 5.1 dan Claude Fable 5.1
* Claude Mythos 5 dan Claude Fable 5
* Claude Opus 5.5 dan Claude Opus 5
* Claude Sonnet 5.5 itu sendiri

Advisor Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, dan Claude Haiku 5.5 berfungsi dengan executor Claude Sonnet 5. Dengan executor Claude Sonnet 5.5, mereka mengembalikan `invalid_request_error` 400. Setiap advisor yang diterima Claude Sonnet 5.5 mengembalikan sarannya dalam bentuk terenkripsi, sebagai blok `advisor_redacted_result`. Jadi klien Anda tidak dapat membaca teks saran tersebut. Lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility) dan [Varian hasil](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#result-variants) alat advisor.

## Dukungan fitur

Claude Sonnet 5.5 mendukung fitur-fitur berikut:

* [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort-per-message), yang sedang dalam beta
* [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages)
* [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes), yang sedang dalam beta
* “Prompt caching” ([caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)), dengan prompt minimum yang dapat di-cache sebesar 512 token
* [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)
* [Vision](https://platform.claude.com/docs/id/build-with-claude/vision)
* Alat sisi server dan sisi klien (lihat [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview))

Claude Sonnet 5 tidak mendukung effort per pesan, pesan sistem di tengah percakapan, atau perubahan alat di tengah percakapan. Pada Claude Sonnet 5, prompt minimum yang dapat di-cache adalah 1.024 token. Lihat halaman masing-masing fitur untuk ketersediaan model.

### Lakukan compaction sesuai permintaan (beta)

Dengan header beta `compact-2026-09-04`, permintaan yang mengirim parameter `compaction` tingkat atas mengembalikan blok `compaction` bertanda tangan yang merangkum pesan-pesan dalam permintaan tersebut. Dalam permintaan berikutnya, blok tersebut ditempatkan pertama di `messages`, menggantikan pesan-pesan yang dirangkumnya. Anda memilih kapan melakukan compaction dan giliran mana yang dipertahankan setelah blok tersebut. Pada Claude Sonnet 5.5, blok pemikiran di giliran yang dipertahankan dapat tetap valid setelah compaction. Untuk syarat-syaratnya, lihat [Compaction dan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid). Lihat [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) untuk ketersediaan platform dan alur permintaan lengkap.

### Mendefinisikan alat dalam pesan (beta)

Dengan header beta `inline-tools-2026-09-15`, blok `tool_addition` dalam pesan sistem di tengah percakapan dapat membawa definisi alat lengkap alih-alih referensi. Anda dapat menambahkan alat, mengubah skemanya, atau memindahkan alat server ke versi yang lebih baru di tengah percakapan tanpa mengedit `tools` dan tanpa kehilangan cache prompt. Lihat [Mendefinisikan alat dalam pesan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta).

### Blok pemikiran tetap berada pada akun yang menghasilkannya

Blok pemikiran yang dihasilkan Claude Sonnet 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang tertaut dengannya. Ketika akun lain mengirim salah satu blok ini, API tidak menyertakan blok tersebut sebelum model menerimanya, dan permintaan berhasil. Blok dari Claude Haiku 5.5, Claude Fable 5.2, dan Claude Mythos 5.2 mengikuti aturan yang sama.

Di Claude API dan Claude Models on Google Cloud (Google managed), Anda dapat melihat blok mana yang tidak disertakan. Kirim header beta `thinking-binding-controls-2026-08-01`, dan respons mencantumkan setiap blok yang tidak disertakan dalam `input_transformations` dengan `reason: "organization_binding_mismatch"`. Lihat [Akun dan platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

## Perbedaan perilaku

Untuk panduan tentang masing-masing hal berikut, lihat [Prompting untuk Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5). Claude Sonnet 5.5 berbeda dari Claude Sonnet 5 dalam hal-hal berikut, yang muncul tanpa perubahan kode apa pun:

* **Level effort dikalibrasi ulang.** Level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) tidak menghasilkan jumlah pemikiran yang sama seperti pada Claude Sonnet 5. Jalankan ulang pengujian effort Anda alih-alih membawa pengaturan sebelumnya. Mulailah pada `high` kecuali beban kerja Anda bersifat agentik atau sensitif terhadap latensi. Untuk coding agentik dan penggunaan alat multilangkah, mulailah pada `medium` untuk tugas yang terdefinisi dengan baik dan beralih ke `high` untuk tugas yang lebih sulit atau lebih panjang. Untuk chat dan pekerjaan lain yang sensitif terhadap latensi, mulailah pada `medium` atau `low`.
* **Teks di antara pemanggilan alat dikembalikan dalam blok pemikiran.** Di antara pemanggilan alat, catatan yang lebih panjang dari satu atau dua kalimat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates). Komentar yang lebih pendek tetap berupa `text`. Pada default `display: "omitted"`, teks blok pembaruan progres kosong, sehingga aplikasi yang melakukan streaming catatan tersebut ke penggunanya menjadi senyap di antara pemanggilan alat, tanpa error. Jika Anda [mematikan pemikiran di awal dengan `between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#turn-off-up-front-thinking), teks tersebut kembali. Untuk menerimanya, lihat [Teks di antara pemanggilan alat dikembalikan dalam blok pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls) dalam panduan migrasi.
* **Kategori safeguard.** Safeguard model dapat menolak permintaan dalam lima [kategori `stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response). `"cyber"` berarti permintaan tersebut dapat memungkinkan bahaya siber. `"bio"` berarti permintaan tersebut dapat memungkinkan bahaya biologis. `"frontier_llm"` berarti permintaan tersebut dapat membantu pengembangan model AI pesaing. `"reasoning_extraction"` berarti permintaan tersebut meminta model mereproduksi penalaran internalnya dalam teks respons. `"general_harms"` berarti permintaan tersebut termasuk dalam area kebijakan penggunaan lainnya. Lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#refusals-fallback-and-billing).

## Penolakan, fallback, dan penagihan

Semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku untuk Claude Sonnet 5.5. Permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakan.

Tangani penolakan dalam kode Anda, dan konfigurasikan fallback. Dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (`fallbacks: "default"`), permintaan yang ditolak dalam kategori `"cyber"` atau `"frontier_llm"` dijalankan lagi pada Claude Sonnet 5. Permintaan yang ditolak dalam kategori `"bio"`, `"reasoning_extraction"`, atau `"general_harms"` tidak dicoba ulang. Fallback sisi server sedang dalam beta di Claude API dan di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed). Anda juga dapat menggunakan [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) atau mekanisme coba ulang Anda sendiri.

Penolakan yang terjadi sebelum output apa pun ditagih dalam beberapa kategori penolakan dan tidak ditagih dalam kategori lainnya. Bagaimanapun juga, penolakan tersebut tetap dihitung terhadap batas laju Anda. Lihat [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).

## Harga

Claude Sonnet 5.5 memiliki harga yang sama dengan Claude Sonnet 5, kecuali untuk pembacaan cache prompt, yang biayanya $0,10 USD per juta token, setengah dari tarif Claude Sonnet 5. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk daftar lengkap, residensi data, dan harga alat.

## Ketersediaan

Claude Sonnet 5.5 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-sonnet-5-5`
* **AWS:** [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-sonnet-5-5`, dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-sonnet-5-5`
* **Google Cloud:** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), sebagai `claude-sonnet-5-5`, dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), sebagai `claude-sonnet-5-5`
* **Microsoft Foundry:** [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-sonnet-5-5`

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

1. Jika kode Anda mematikan pemikiran dengan `disabled`, kirimkan `between_tools` sebagai gantinya, pada effort `high` atau di bawahnya.
2. Ganti tipe `tool_choice` `any` dan `tool` dengan `auto` ditambah [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use).
3. Pertahankan percakapan tetap append-only (hanya ditambahkan). Permintaan yang memutar ulang blok pemikiran Claude Sonnet 5.5 setelah pengeditan riwayat sebelumnya dapat mengembalikan error 400. Lihat [Blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them).
4. Jika Anda menggunakan alat penggunaan komputer melalui `computer_20251124`, [pindahlah ke toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Di Amazon Bedrock, `computer_20251124` juga berfungsi.
5. Jika Anda menggunakan alat advisor dengan advisor Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, atau Claude Haiku 5.5, [beralihlah ke advisor yang diterima Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#advisor-tool-pairings).
6. Jika antarmuka Anda menampilkan teks di antara pemanggilan alat, atur `thinking.display` saat Anda menggunakan pemikiran adaptif. Dengan `between_tools`, teks dikembalikan tanpa pengaturan tersebut. Lihat [Teks di antara pemanggilan alat dikembalikan dalam blok pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls).

[Panduan migrasi Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide) berisi instruksi langkah demi langkah dari Claude Sonnet 5 dan model-model sebelumnya, serta daftar periksa lengkap.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi lengkap dan harga untuk semua model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide">
    Pindahkan kode dari Claude Sonnet 5 dan model-model sebelumnya ke Claude Sonnet 5.5.
  </Card>

  <Card title="Prompting untuk Claude Sonnet 5.5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Sonnet 5.5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Pemikiran" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif dan cara blok pemikiran dipertahankan.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani `stop_reason: "refusal"` dan coba ulang pada model lain.
  </Card>
</CardGroup>
