---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 05ed9d355f84ff13f017d7bac22c9d18aae386f083f28780e05bbc13eedec07a
---

---
title: Yang baru di Claude Opus 5.5
url: https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5
description: Ikhtisar perubahan yang merusak kompatibilitas, dukungan fitur, dan perbedaan perilaku di Claude Opus 5.5.
---

Claude Opus 5.5 dibuat untuk agentic coding dan pekerjaan berbasis pengetahuan yang berjalan lama, dengan harga $4 / $20 USD per juta token input / output. Empat “breaking changes” (perubahan yang merusak kompatibilitas) memengaruhi kode yang sudah berjalan di Claude Opus 5: [pemikiran tidak dapat dinonaktifkan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled), [forced tool use mengembalikan error](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#forced-tool-use-is-not-supported), [blok pemikiran terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them), dan, di Claude API serta Claude Models on Google Cloud (Google managed), [alat penggunaan komputer `computer_20251124` yang lebih lama tidak diterima](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported). Tiga yang pertama juga berlaku di Claude Fable 5.1. Satu perubahan lainnya mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara panggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#text-between-tool-calls) yang teksnya kosong pada pengaturan `display` default. Aplikasi yang melakukan streaming teks tersebut ke penggunanya sebagai pembaruan progres akan menjadi senyap di antara panggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks.

## Model baru

| Model           | ID Claude API   | Deskripsi                                                                  |
| --------------- | --------------- | -------------------------------------------------------------------------- |
| Claude Opus 5.5 | claude-opus-5-5 | Untuk agentic coding dan pekerjaan berbasis pengetahuan yang berjalan lama |

[Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) mengontrol kedalaman pemikiran; nilai default-nya pada model ini adalah `medium`. Untuk “context window” (jendela konteks), batas output, batas pengetahuan, dan harga, lihat [halaman model Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview); untuk semua model saat ini, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Pemikiran tidak dapat dinonaktifkan

Di Claude Opus 5, pemikiran aktif secara default dan `thinking: {"type": "disabled"}` diterima pada effort `high` atau lebih rendah. Di Claude Opus 5.5, pemikiran selalu aktif: permintaan yang menetapkan `thinking: {"type": "disabled"}`, atau anggaran manual dengan `thinking: {"type": "enabled", "budget_tokens": N}`, mengembalikan 400 `invalid_request_error`. Hilangkan field `thinking`, atau kirim `thinking: {"type": "adaptive"}`, yang setara. Tidak ada beta header yang terlibat.

Pesan error-nya adalah:

```text wrap
"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

[Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol untuk kedalaman pemikiran, latensi, dan biaya: turunkan nilainya di tempat Anda sebelumnya menonaktifkan pemikiran; [Mengoptimalkan biaya dan kecerdasan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort) berisi hasil terukur untuk memilih level. Karena setiap respons dapat diawali dengan satu atau lebih blok `thinking` (dikembalikan dengan field `thinking` kosong pada default `display: "omitted"`), pilih blok konten berdasarkan field `type`-nya, bukan berdasarkan posisi, dan kirimkan kembali blok `thinking` tanpa modifikasi dalam loop “tool use” (penggunaan alat). Kode yang sudah berjalan di Claude Opus 5 dengan pemikiran aktif tidak memerlukan perubahan. Lihat [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) dan [perbandingan sebelum dan sesudah untuk pemikiran](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-cant-be-disabled) di panduan migrasi.

### Forced tool use tidak didukung

Claude Opus 5.5 tidak mendukung “forced tool use” (penggunaan alat paksa). `tool_choice` yang ditetapkan ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan 400 `invalid_request_error`:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` didukung, dan validasi yang sama berlaku untuk endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting). Untuk JSON yang valid terhadap skema, pertahankan `tool_choice: {"type": "auto"}` dan tetapkan `strict: true` dengan [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau pindahkan skema ke [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs). Agar model memanggil alat alih-alih membalas dengan teks, sebutkan dalam prompt kapan alat tersebut berlaku. Panduan migrasi menunjukkan [perbandingan sebelum dan sesudah untuk tool choice](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#forced-tool-use).

### Blok pemikiran terikat pada model dan percakapan

Setiap “thinking block” (blok pemikiran) mencatat model mana yang menghasilkannya, dan setiap model membaca bloknya sendiri serta hanya sebagian blok dari model lain. Claude Opus 5.5 membaca blok pemikiran dari Claude Opus 5, dari model Opus, Sonnet, dan Haiku yang lebih lama, dan, di Claude API dan Claude Models on Google Cloud (Google managed), dari Claude Sonnet 5.5 dan Claude Haiku 5.5, tetapi tidak dari model Claude Fable atau Claude Mythos. Di Claude API, Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok pemikiran dari Claude Opus 5.5; tidak ada model lain yang melakukannya. Percakapan yang berpindah dari Claude Opus 5 ke Claude Opus 5.5, atau dari Claude Opus 5.5 naik ke Claude Fable 5.1 atau Claude Mythos 5.1 di Claude API, mempertahankan penalarannya. Percakapan yang berpindah dari Claude Opus 5.5 ke model apa pun selain kedua model tersebut, atau berpindah ke Claude Opus 5.5 dari model Claude Fable atau Claude Mythos, menjalankan giliran setelah peralihan tanpa penalaran model sebelumnya. Ketika sebuah permintaan membawa blok yang tidak dapat dibaca oleh model tujuan, API membuangnya sebelum model melihatnya: permintaan tetap berhasil, dan blok yang dibuang tidak ditagih. Dengan beta header `thinking-binding-controls-2026-08-01`, pembuangan tersebut dilaporkan dalam array `input_transformations` tingkat atas. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

API juga memeriksa apakah ada sesuatu sebelum blok pemikiran Claude Opus 5.5 (prompt `system`, `tools`, atau pesan sebelumnya) yang telah berubah sejak blok tersebut dihasilkan. Jaga agar percakapan bersifat append-only (hanya ditambahkan): ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih melakukan pengeditan. Permintaan yang memutar ulang sebuah blok setelah perubahan semacam itu dan membiarkan `thinking.block_binding.prefix_mismatch_behavior` tidak diatur akan mendapatkan error 400 pada akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC. Ini berlaku di Claude API dan di platform cloud. Pada akun yang dibuat sebelum tanggal tersebut, permintaan hanya mendapatkan error ketika field tersebut diatur ke `"error"`. Untuk membuang blok yang terdampak sebagai gantinya, kirim beta header `thinking-binding-controls-2026-08-01` dan atur field tersebut ke `"drop_block"`. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan [catatan tentang blok pemikiran](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-blocks) dalam panduan migrasi.

### Alat penggunaan komputer `computer_20251124` tidak didukung di Claude API dan Claude Models on Google Cloud (Google managed)

Claude Opus 5 menerima [penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) baik sebagai toolset `computer_toolset_20260801` maupun, dengan beta header `computer-use-2025-11-24`, sebagai alat `computer_20251124` yang lebih lama. Di Claude API dan Claude Models on Google Cloud (Google managed), Claude Opus 5.5 hanya mendukung toolset: permintaan yang mendeklarasikan alat `computer_20251124` mengembalikan 400 `invalid_request_error`. Pesan tersebut menyebutkan tipe yang ditolak, lalu mencantumkan tipe alat yang diterima model (termasuk `computer_toolset_20260801`) setelah `Did you mean one of`; pesan tersebut diawali dengan:

```text wrap
'claude-opus-5-5' does not support tool types: computer_20251124.
```

Untuk memindahkan integrasi yang sudah ada di Claude API atau Claude Models on Google Cloud (Google managed), ikuti [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124): hapus beta header, ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`, dan perbarui loop agen Anda untuk blok `tool_use` anggota, aksi batch, dan `toolset_name` pada hasil. Di Amazon Bedrock, alat `computer_20251124` yang lebih lama tetap berfungsi di Claude Opus 5.5 seperti di Claude Opus 5, sehingga tidak diperlukan perubahan di sana. Untuk platform lain, lihat bagian [dukungan API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#availability-feature-support) pada alat penggunaan komputer. Integrasi yang sudah menggunakan toolset, serta [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool), tidak memerlukan perubahan. Panduan migrasi menunjukkan permintaan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#computer-use-toolset).

## Dukungan fitur

Claude Opus 5.5 mendukung [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta), [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets), [“prompt caching” (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) dengan prompt minimum yang dapat di-cache sebesar 512 token, [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Di Claude API dan Claude Models on Google Cloud (Google managed), penggunaan komputer memerlukan toolset `computer_toolset_20260801` (lihat [perubahan yang merusak kompatibilitas pada penggunaan komputer](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported)). Lihat halaman masing-masing fitur untuk ketersediaan model.

### Mode cepat

[Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) tersedia untuk Claude Opus 5.5 di Claude API, di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), dan di [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) untuk deployment yang di-host di Azure. Di Claude API dan di Claude Models on Google Cloud (Anthropic managed), tetapkan `speed: "fast"` pada permintaan Anda. Claude Opus 5.5 tidak memerlukan beta header. Lihat [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk model yang didukung, “rate limit” (batas laju), dan harga.

### Mendefinisikan alat dalam pesan (beta)

Dengan beta header `inline-tools-2026-09-15`, blok `tool_addition` dalam pesan sistem di tengah percakapan dapat membawa definisi alat lengkap alih-alih referensi, sehingga Anda dapat menambahkan alat, mengubah skemanya, atau memindahkan alat server ke versi yang lebih baru di tengah percakapan tanpa mengedit `tools` dan tanpa kehilangan cache prompt. Ini berfungsi pada setiap model yang mendukung perubahan alat di tengah percakapan, termasuk Claude Opus 5.5. Lihat [Mendefinisikan alat dalam pesan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta).

### Compaction sesuai permintaan (beta)

Dengan beta header `compact-2026-09-04`, permintaan yang mengirimkan parameter `compaction` tingkat atas mengembalikan blok `compaction` bertanda tangan yang merangkum seluruh percakapan, yang kemudian Anda kirim pertama kali sebagai pengganti pesan-pesan yang dirangkum. Fitur ini tersedia pada model yang mendukung compaction, termasuk Claude Opus 5.5. Anda memilih kapan melakukan compaction, dan permintaan dapat berjalan di latar belakang. Dalam kondisi yang dijelaskan di [Compaction dan preserved thinking](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid), blok pemikiran pada giliran yang Anda pertahankan dapat tetap valid setelah penggantian. Hal ini penting di Claude Opus 5.5 karena [blok pemikirannya terikat pada percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them). Lihat [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) untuk ketersediaan platform dan alur permintaan lengkap.

## Perbedaan perilaku

Claude Opus 5.5 berbeda dari Claude Opus 5 dalam beberapa hal yang muncul tanpa perubahan kode apa pun. Masing-masing memiliki panduan di [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5):

* **Effort default adalah `medium`.** Permintaan yang tidak menyertakan `effort` berjalan pada `medium`; di Claude Opus 5 permintaan tersebut berjalan pada `high`. Tetapkan `effort` secara eksplisit dan jalankan ulang pengujian Anda; lihat [Mengkalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#calibrate-effort).
* **Lebih banyak pemikiran per giliran pada level effort tertentu.** Pada pengaturan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang sama, model cenderung berpikir lebih banyak per giliran dibandingkan Claude Opus 5, terutama pada `xhigh` dan `max`. Jalankan ulang pengujian effort Anda alih-alih membawa pengaturan lama, dan sisakan ruang di `max_tokens` untuk pemikiran. Lihat [Mengkalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#calibrate-effort).
* **Teks di antara panggilan alat dikembalikan dalam blok pemikiran.** Catatan singkat yang ditulis model di antara panggilan alat tiba sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) alih-alih blok `text`, sehingga pada default `display: "omitted"` aplikasi yang melakukan streaming catatan tersebut ke penggunanya menjadi senyap di antara panggilan alat, tanpa error. Panduan migrasi menjelaskan [cara menerima teks di antara panggilan alat](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls), dan [Pembaruan progres untuk pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#user-facing-progress-updates) membahas cara meminta lebih banyak pembaruan tersebut.
* **Lebih banyak kategori safeguard.** Model menjalankan pengklasifikasi keamanan biologi selain pengklasifikasi keamanan siber. Seperti di Claude Opus 5, permintaan yang mendorong model untuk mereproduksi penalaran internalnya dalam teks respons mungkin ditolak dengan kategori `reasoning_extraction`. Lihat [Penolakan dan fallback di Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#refusals-and-fallback) dan [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#safeguard-refusals).
* **Pembacaan grafik, diagram, dan tangkapan layar yang lebih tajam.** Model membaca nilai dari grafik padat dan visual yang bergantung pada tata letak dengan jauh lebih presisi tanpa alat, sehingga solusi vision di sisi prompt yang dibuat untuk model sebelumnya mungkin tidak lagi diperlukan; alat gambar tetap menambah akurasi pada input yang paling padat. Lihat [Alat untuk input visual yang kompleks](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#tools-for-complex-visual-inputs).

Jika integrasi Claude Opus 5 Anda berjalan dengan pemikiran dinonaktifkan, lihat [Prompt yang ditulis untuk pemikiran yang dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#prompts-written-for-thinking-disabled) bersama dengan perubahan yang merusak kompatibilitas [Pemikiran tidak dapat dinonaktifkan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled). Untuk peningkatan kemampuan dalam agentic coding dan code review, pekerjaan berbasis pengetahuan, komunikasi, input visual, dan penggunaan komputer, lihat [Kemampuan yang relevan untuk prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#capability-improvements).

## Penolakan dan fallback

Claude Opus 5.5 dilengkapi dengan pengklasifikasi keamanan, dan semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku. Permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakan, jadi tangani penolakan dan konfigurasikan fallback: coba ulang di model lain dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (`fallbacks: "default"`, dalam beta, mencoba ulang pada model yang direkomendasikan Anthropic untuk kategori tersebut), [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback), atau mekanisme percobaan ulang Anda sendiri. Apakah penolakan yang tiba sebelum output apa pun ditagih bergantung pada kategori penolakannya, dan penolakan tersebut tetap dihitung terhadap batas laju Anda dalam kedua kasus; lihat [Bagaimana penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).

## Harga

Claude Opus 5.5 berharga $4 USD per juta token input dan $20 USD per juta token output, lebih rendah dari $5 dan $25 USD pada Claude Opus 5, dengan penulisan cache 5 menit sebesar $5 USD, penulisan cache 1 jam sebesar $8 USD, dan pembacaan cache sebesar $0,20 USD per juta token (0,05x harga input dasar). [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) setengah harga: $2 dan $10 USD. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk residensi data dan harga alat.

## Ketersediaan

Claude Opus 5.5 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-opus-5-5`
* **AWS:** [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-opus-5-5`, dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-opus-5-5`
* **Google Cloud:** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), sebagai `claude-opus-5-5`, dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), sebagai `claude-opus-5-5`
* **Microsoft Foundry:** [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-opus-5-5`

## Migrasi dari Claude Opus 5

Perbarui ID model Anda:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-opus-5"  # Before
  model = "claude-opus-5-5"  # After
  ```

  ```typescript TypeScript
  let model = "claude-opus-5"; // Before
  model = "claude-opus-5-5"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeOpus5; // Before
  model = Model.ClaudeOpus5_5; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeOpus5  // Before
  model = anthropic.ModelClaudeOpus5_5 // After
  ```

  ```java Java
  Model model = Model.CLAUDE_OPUS_5; // Before
  model = Model.CLAUDE_OPUS_5_5; // After
  ```

  ```php PHP
  $model = Model::CLAUDE_OPUS_5; // Before
  $model = Model::CLAUDE_OPUS_5_5; // After
  ```

  ```ruby Ruby
  model = Anthropic::Model::CLAUDE_OPUS_5 # Before
  model = Anthropic::Model::CLAUDE_OPUS_5_5 # After
  ```
</CodeGroup>

Kemudian hapus pengaturan `thinking: {"type": "disabled"}` atau `thinking: {"type": "enabled", ...}` apa pun dan pilih level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai gantinya. Ganti tipe `tool_choice` `any` dan `tool` dengan `auto` ditambah [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). Jika Anda menggunakan alat penggunaan komputer melalui `computer_20251124` di Claude API atau Claude Models on Google Cloud (Google managed), [pindah ke toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Jika antarmuka Anda menampilkan teks di antara panggilan alat, tetapkan juga `thinking.display`; lihat [Teks di antara panggilan alat dikembalikan dalam blok pemikiran](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls). Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide) untuk instruksi langkah demi langkah dari Claude Opus 5 dan model sebelumnya, serta daftar periksa lengkap.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi lengkap dan harga untuk semua model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/opus-5-5/migration-guide">
    Pindahkan kode dari Claude Opus 5 dan model sebelumnya ke Claude Opus 5.5.
  </Card>

  <Card title="Prompting Claude Opus 5.5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Opus 5.5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja pemikiran adaptif dan cara blok pemikiran dipertahankan.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani `stop_reason: "refusal"` dan coba ulang di model lain.
  </Card>
</CardGroup>
