---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5
fetched_at: 2026-09-25T02:20:28.349481Z
sha256: d55cc7d9507265f5c03821503c2d5c06088975b77929f7be41e1968fe67138ef
---

---
title: Yang baru di Claude Opus 5.5
url: https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5
description: Ikhtisar perubahan yang merusak kompatibilitas, dukungan fitur, dan perbedaan perilaku di Claude Opus 5.5.
---

Claude Opus 5.5 dibangun untuk agentic coding dan pekerjaan pengetahuan yang berjalan lama, dengan harga $4 / $20 USD per juta token input / output. Empat "breaking changes" (perubahan yang merusak kompatibilitas) memengaruhi kode yang sudah berjalan di Claude Opus 5: [thinking tidak dapat dinonaktifkan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled), [penggunaan alat paksa mengembalikan error](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#forced-tool-use-is-not-supported), [blok thinking terikat pada model dan percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them), dan, di Claude API dan Google Cloud, [alat computer use `computer_20251124` yang lebih lama tidak diterima](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported). Tiga yang pertama juga berlaku di Claude Fable 5.1. Satu perubahan lain mengubah bentuk respons tanpa menggagalkan permintaan apa pun: [teks di antara panggilan alat dikembalikan dalam blok `thinking`](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#text-between-tool-calls) yang teksnya kosong pada pengaturan `display` default. Aplikasi yang melakukan streaming teks tersebut ke penggunanya sebagai pembaruan progres akan menjadi senyap di antara panggilan alat hingga aplikasi tersebut menetapkan nilai `display` yang mengembalikan teks.

## Model baru

| Model           | ID Claude API   | Deskripsi                                                         |
| --------------- | --------------- | ----------------------------------------------------------------- |
| Claude Opus 5.5 | claude-opus-5-5 | Untuk agentic coding dan pekerjaan pengetahuan yang berjalan lama |

["Adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) mengontrol kedalaman thinking; nilai default-nya pada model ini adalah `medium`. Untuk "context window" (jendela konteks), batas output, batas pengetahuan, dan harga, lihat [halaman model Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview); untuk semua model saat ini, lihat [ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Thinking tidak dapat dinonaktifkan

Di Claude Opus 5, "thinking" (pemikiran) aktif secara default dan `thinking: {"type": "disabled"}` diterima pada effort `high` atau lebih rendah. Di Claude Opus 5.5, thinking selalu aktif: permintaan yang menetapkan `thinking: {"type": "disabled"}`, atau anggaran manual dengan `thinking: {"type": "enabled", "budget_tokens": N}`, mengembalikan 400 `invalid_request_error`. Hilangkan field `thinking`, atau kirim `thinking: {"type": "adaptive"}`, yang setara. Tidak ada header beta yang terlibat.

Pesan error-nya adalah:

```text wrap
"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

[Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol untuk kedalaman thinking, "latency" (latensi), dan biaya: turunkan nilainya di tempat Anda sebelumnya menonaktifkan thinking; [Mengoptimalkan biaya dan kecerdasan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort) memuat hasil terukur untuk memilih level. Karena setiap respons dapat diawali dengan satu atau lebih blok `thinking` (dikembalikan dengan field `thinking` kosong pada default `display: "omitted"`), pilih blok konten berdasarkan field `type`-nya, bukan berdasarkan posisi, dan kirimkan kembali blok `thinking` tanpa modifikasi dalam loop penggunaan alat. Kode yang sudah berjalan di Claude Opus 5 dengan thinking aktif tidak memerlukan perubahan. Lihat [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) dan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-cant-be-disabled) di panduan migrasi.

### Penggunaan alat paksa tidak didukung

Claude Opus 5.5 tidak mendukung "forced tool use" (penggunaan alat paksa). `tool_choice` yang ditetapkan ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan 400 `invalid_request_error`:

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

`tool_choice: {"type": "auto"}` (default) dan `{"type": "none"}` didukung, dan validasi yang sama berlaku untuk endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting). Untuk JSON yang valid sesuai skema, pertahankan `tool_choice: {"type": "auto"}` dan tetapkan `strict: true` dengan [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau pindahkan skema ke [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs). Agar model memanggil alat alih-alih membalas dengan teks, sebutkan dalam prompt kapan alat tersebut berlaku. Panduan migrasi menunjukkan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#forced-tool-use).

### Blok thinking terikat pada model dan percakapan

Setiap blok thinking mencatat model mana yang menghasilkannya, dan setiap model membaca bloknya sendiri serta hanya sebagian blok dari model lain. Claude Opus 5.5 membaca blok thinking dari Claude Opus 5 dan model Opus, Sonnet, dan Haiku yang lebih lama, tetapi tidak dari model Claude Fable atau Claude Mythos. Di Claude API, Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok thinking dari Claude Opus 5.5; tidak ada model lain yang melakukannya. Percakapan yang berpindah dari Claude Opus 5 ke Claude Opus 5.5, atau dari Claude Opus 5.5 naik ke Claude Fable 5.1 atau Claude Mythos 5.1 di Claude API, mempertahankan penalarannya. Percakapan yang berpindah dari Claude Opus 5.5 ke model apa pun selain kedua model tersebut, atau ke Claude Opus 5.5 dari model Claude Fable atau Claude Mythos, menjalankan giliran setelah perpindahan tanpa penalaran model sebelumnya. Ketika sebuah permintaan membawa blok yang tidak dapat dibaca oleh model target, API membuangnya sebelum model melihatnya: permintaan berhasil, dan blok yang dibuang tidak ditagih. Dengan header beta `thinking-binding-controls-2026-08-01`, pembuangan tersebut dilaporkan dalam array `input_transformations` tingkat atas. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

API juga memeriksa apakah ada sesuatu sebelum blok thinking Claude Opus 5.5 (prompt `system`, `tools`, atau pesan sebelumnya) yang telah berubah sejak blok tersebut dihasilkan. Seperti di Claude Fable 5.1, API memberlakukan pemeriksaan tersebut secara default untuk akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC, di Claude API dan di platform cloud. Pada akun tersebut, permintaan yang memutar ulang blok setelah perubahan semacam itu mengembalikan error 400. Untuk membuang blok yang terdampak sebagai gantinya, kirim header beta `thinking-binding-controls-2026-08-01` dan tetapkan `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Pada akun yang lebih lama, menetapkan field tersebut ke salah satu nilai akan mengikutsertakan permintaan dalam pemberlakuan pemeriksaan tersebut. Pertahankan percakapan agar hanya ditambahkan (append-only) sehingga masalah ini tidak pernah muncul: ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih dengan pengeditan. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) dan [catatan tentang perubahan ini](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#thinking-blocks) di panduan migrasi.

### Alat computer use `computer_20251124` tidak didukung di Claude API dan Google Cloud

Claude Opus 5 menerima [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) baik sebagai toolset `computer_toolset_20260801` maupun, dengan header beta `computer-use-2025-11-24`, sebagai alat `computer_20251124` yang lebih lama. Di Claude API dan Google Cloud, Claude Opus 5.5 hanya mendukung toolset: permintaan yang mendeklarasikan alat `computer_20251124` mengembalikan 400 `invalid_request_error`. Pesan tersebut menyebutkan tipe yang ditolak, lalu mencantumkan tipe alat yang diterima model (termasuk `computer_toolset_20260801`) setelah `Did you mean one of`; pesan tersebut diawali dengan:

```text wrap
'claude-opus-5-5' does not support tool types: computer_20251124.
```

Untuk memindahkan integrasi yang sudah ada di Claude API atau Google Cloud, ikuti [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124): hapus header beta, ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`, dan perbarui loop agen Anda untuk blok `tool_use` anggota, aksi batch, dan `toolset_name` pada hasil. Di Amazon Bedrock, alat `computer_20251124` yang lebih lama tetap berfungsi di Claude Opus 5.5 seperti di Claude Opus 5, sehingga tidak diperlukan perubahan di sana. Untuk platform lain, lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use. Integrasi yang sudah menggunakan toolset, serta [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool), tidak memerlukan perubahan. Panduan migrasi menunjukkan permintaan [sebelum dan sesudah](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#computer-use-toolset).

## Dukungan fitur

Claude Opus 5.5 mendukung [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta), [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) dengan prompt minimum yang dapat di-cache sebesar 512 token, [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Di Claude API dan Google Cloud, computer use memerlukan toolset `computer_toolset_20260801` (lihat [perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#computer-20251124-is-not-supported)). Lihat halaman masing-masing fitur untuk ketersediaan model.

### Mode cepat

[Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) tersedia untuk Claude Opus 5.5 hanya di Claude API; mode ini tidak tersedia di Amazon Bedrock, Claude Platform on AWS, Google Cloud, atau Microsoft Foundry. Tetapkan `speed: "fast"` dengan header beta `fast-mode-2026-02-01`. Lihat [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk akses, model yang didukung, dan harga.

### Mendefinisikan alat dalam pesan (beta)

Dengan header beta `inline-tools-2026-09-15`, blok `tool_addition` dalam pesan sistem di tengah percakapan dapat membawa definisi alat lengkap alih-alih referensi, sehingga Anda dapat menambahkan alat, mengubah skemanya, atau memindahkan alat server ke versi yang lebih baru di tengah percakapan tanpa mengedit `tools` dan tanpa kehilangan cache prompt. Ini berfungsi di setiap model yang mendukung perubahan alat di tengah percakapan, termasuk Claude Opus 5.5. Lihat [Mendefinisikan alat dalam pesan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta).

### Compaction sesuai permintaan (beta)

Dengan header beta `compact-2026-09-04`, permintaan yang mengirimkan parameter `compaction` tingkat atas mengembalikan blok `compaction` bertanda tangan yang merangkum seluruh percakapan, yang kemudian Anda kirimkan di urutan pertama sebagai pengganti pesan-pesan yang dirangkum. Fitur ini tersedia di model yang mendukung compaction, termasuk Claude Opus 5.5. Anda memilih kapan melakukan compaction, permintaan dapat berjalan di latar belakang, dan blok thinking dalam giliran yang Anda pertahankan dapat tetap valid setelah penggantian (dengan kondisi yang dijelaskan di [Compaction dan pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid)), yang penting di Claude Opus 5.5 karena [blok thinking-nya terikat pada percakapan](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-blocks-are-tied-to-the-model-that-produced-them). Lihat [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) untuk ketersediaan platform dan alur permintaan lengkap.

## Perbedaan perilaku

Claude Opus 5.5 berbeda dari Claude Opus 5 dalam beberapa hal yang muncul tanpa perubahan kode apa pun. Masing-masing memiliki panduan di [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5):

* **Effort default adalah `medium`.** Permintaan yang tidak menyertakan `effort` berjalan pada `medium`; di Claude Opus 5 permintaan tersebut berjalan pada `high`. Tetapkan `effort` secara eksplisit dan jalankan ulang sweep Anda; lihat [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#calibrate-effort).
* **Lebih banyak thinking per giliran pada level effort tertentu.** Pada pengaturan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang sama, model cenderung berpikir lebih banyak per giliran dibandingkan Claude Opus 5, terutama pada `xhigh` dan `max`. Jalankan ulang sweep effort Anda alih-alih membawa pengaturan lama, dan sisakan ruang di `max_tokens` untuk thinking. Lihat [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#calibrate-effort).
* **Teks di antara panggilan alat dikembalikan dalam blok thinking.** Catatan singkat yang ditulis model di antara panggilan alat tiba sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) alih-alih blok `text`, sehingga pada default `display: "omitted"` aplikasi yang melakukan streaming catatan tersebut ke penggunanya menjadi senyap di antara panggilan alat, tanpa error. [Panduan migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls) memuat perbaikan untuk menerimanya, dan [Pembaruan progres untuk pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#user-facing-progress-updates) membahas cara meminta lebih banyak pembaruan tersebut.
* **Lebih banyak kategori safeguard.** Model menjalankan pengklasifikasi keamanan biologi selain pengklasifikasi keamanan siber, dan permintaan yang mendorong model untuk mereproduksi penalaran internalnya dalam teks respons dapat ditolak dengan kategori `reasoning_extraction`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#refusals-and-fallback) dan [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#safeguard-refusals).
* **Pembacaan grafik, diagram, dan tangkapan layar yang lebih tajam.** Model membaca nilai dari grafik padat dan visual yang bergantung pada tata letak dengan jauh lebih presisi tanpa alat, sehingga solusi vision di sisi prompt yang dibuat untuk model sebelumnya mungkin tidak lagi diperlukan; alat gambar tetap menambah akurasi pada input yang paling padat. Lihat [Alat untuk input visual yang kompleks](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#tools-for-complex-visual-inputs).

Jika integrasi Claude Opus 5 Anda berjalan dengan thinking dinonaktifkan, lihat [Prompt yang ditulis untuk thinking yang dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#prompts-written-for-thinking-disabled) bersama dengan [perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5#thinking-cant-be-disabled). Untuk peningkatan kemampuan dalam agentic coding dan tinjauan kode, pekerjaan pengetahuan, komunikasi, input visual, dan computer use, lihat [Kemampuan yang relevan untuk prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#capability-improvements).

## Penolakan dan fallback

Claude Opus 5.5 dilengkapi dengan pengklasifikasi keamanan, dan semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku. Permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakan, jadi tangani penolakan dan konfigurasikan fallback: coba ulang di model lain dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (`fallbacks: "default"`, dalam beta, mencoba ulang di model yang direkomendasikan Anthropic untuk kategori tersebut), [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback), atau mekanisme coba ulang Anda sendiri. Apakah penolakan yang tiba sebelum output apa pun ditagih bergantung pada kategori penolakannya, dan penolakan tersebut tetap dihitung terhadap "rate limit" (batas laju) Anda dalam kedua kasus; lihat [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).

## Harga

Claude Opus 5.5 berharga $4 USD per juta token input dan $20 USD per juta token output, lebih rendah dari $5 dan $25 pada Claude Opus 5, dengan penulisan cache 5 menit seharga $5, penulisan cache 1 jam seharga $8, dan pembacaan cache seharga $0,20 per juta token (0,05x harga input dasar). [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) setengah harga: $2 dan $10. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk residensi data dan harga alat.

## Ketersediaan

Claude Opus 5.5 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-opus-5-5`.
* **AWS:** [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), sebagai `anthropic.claude-opus-5-5`, dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-opus-5-5`.
* **Google Cloud:** [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), sebagai `claude-opus-5-5`.
* **Microsoft Foundry:** [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-opus-5-5`.

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

Kemudian hapus pengaturan `thinking: {"type": "disabled"}` atau `thinking: {"type": "enabled", ...}` apa pun dan pilih level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai gantinya. Ganti tipe `tool_choice` `any` dan `tool` dengan `auto` ditambah [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). Jika Anda menggunakan computer use melalui `computer_20251124` di Claude API atau Google Cloud, [pindah ke toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Jika antarmuka Anda menampilkan teks di antara panggilan alat, tetapkan juga `thinking.display`; lihat [Teks di antara panggilan alat dikembalikan dalam blok thinking](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#text-between-tool-calls). Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide) untuk instruksi langkah demi langkah dari Claude Opus 5 dan model yang lebih lama, serta daftar periksa lengkap.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/opus-5-5/migration-guide">
    Pindahkan kode dari Claude Opus 5 dan model yang lebih lama ke Claude Opus 5.5.
  </Card>

  <Card title="Prompting Claude Opus 5.5" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5">
    Perbedaan perilaku dan pola prompting yang khusus untuk Claude Opus 5.5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude saat merespons, dari low hingga max.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Cara kerja adaptive thinking dan cara blok thinking dipertahankan.
  </Card>

  <Card title="Penolakan dan fallback" icon="shield" href="https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback">
    Tangani `stop_reason: "refusal"` dan coba ulang di model lain.
  </Card>
</CardGroup>
