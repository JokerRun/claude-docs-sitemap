---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 26685319503454324bedb21e735a64d5622b4d250cb6d82a0f8698c5b5a34c75
---

---
title: Pemecahan masalah thinking
url: https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting
description: "Diagnosis dan perbaiki kegagalan thinking yang paling umum: error 400 konfigurasi, blok thinking kosong atau hilang, penghentian max_tokens, dan cache miss."
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Halaman ini membahas kegagalan paling umum saat mengonfigurasi thinking atau melakukan round-trip blok thinking (mengirim kembali blok thinking yang dikembalikan dalam permintaan berikutnya). Bagian pertama memetakan setiap model ke konfigurasi thinking yang didukungnya dan yang ditolaknya; bagian-bagian setelahnya masing-masing dimulai dari gejala yang Anda amati, sehingga Anda dapat mencocokkan pesan error atau respons yang tidak terduga langsung dengan penyebab dan perbaikannya. Untuk mempelajari cara kerja thinking, lihat ikhtisar [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking).

## Dukungan thinking, default, dan konfigurasi yang ditolak per model

Sebagian besar error konfigurasi thinking adalah ketidakcocokan antara nilai `thinking.type` dalam permintaan dan apa yang didukung model. Pada sebagian besar model, thinking berjalan sebagai `thinking: {type: "adaptive"}`, dan banyak model mengaktifkannya secara default. Beberapa model yang lebih lama justru menggunakan ["extended thinking" (pemikiran diperpanjang)](https://platform.claude.com/docs/id/build-with-claude/extended-thinking), mode manual lama yang dikonfigurasi sebagai `thinking: {type: "enabled", budget_tokens: N}`.

"Extended thinking" (pemikiran diperpanjang) (`thinking.type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated) pada model Claude 4.6 (permintaan yang menggunakannya masih berhasil). Claude 4.7 dan model yang lebih baru tidak mendukungnya dan menolak permintaan yang menggunakannya, dengan mengembalikan error 400. Pada Claude 4.5 dan model sebelumnya yang mendukung thinking, pemikiran diperpanjang adalah satu-satunya mode thinking yang tersedia. Claude Mythos Preview mendukung kedua mode tersebut. Jika kedua mode tersedia, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) sebagai gantinya.

Tabel ini mencantumkan apa yang didukung setiap model, nilai default-nya, dan nilai `thinking.type` mana yang ditolaknya dengan error 400; nilai apa pun yang tidak tercantum sebagai ditolak akan diterima. Hanya Claude Sonnet 5.5 yang menerima `"between_tools"`, dan model ini menerima nilai tersebut sebagai pengganti `"disabled"`.

| Model                 | Jenis thinking                 | Default      | Ditolak dengan 400         |
| --------------------- | ------------------------------ | ------------ | -------------------------- |
| Claude Fable 5.1      | Hanya adaptif                  | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos 5.1     | Hanya adaptif                  | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Fable 5        | Hanya adaptif                  | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos 5       | Hanya adaptif                  | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos Preview | Adaptif, diperpanjang          | Selalu aktif | `"disabled"`               |
| Claude Opus 5.5       | Hanya adaptif                  | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Opus 5         | Hanya adaptif                  | Aktif        | `"enabled"`, `"disabled"`2 |
| Claude Opus 4.8       | Hanya adaptif                  | Nonaktif     | `"enabled"`                |
| Claude Opus 4.7       | Hanya adaptif                  | Nonaktif     | `"enabled"`                |
| Claude Sonnet 5.5     | Adaptif, `between_tools`3      | Aktif        | `"enabled"`, `"disabled"`  |
| Claude Sonnet 5       | Hanya adaptif                  | Aktif        | `"enabled"`                |
| Claude Haiku 5.5      | Hanya adaptif                  | Aktif        | `"enabled"`, `"disabled"`2 |
| Claude Opus 4.6       | Adaptif, diperpanjang (usang)1 | Nonaktif     | Tidak ada                  |
| Claude Sonnet 4.6     | Adaptif, diperpanjang (usang)1 | Nonaktif     | Tidak ada                  |
| Claude Opus 4.5       | Hanya diperpanjang             | Nonaktif     | `"adaptive"`               |
| Claude Haiku 4.5      | Hanya diperpanjang             | Nonaktif     | `"adaptive"`               |
| Claude Sonnet 4.5     | Hanya diperpanjang             | Nonaktif     | `"adaptive"`               |

*1 `enabled` dan `budget_tokens` masih berfungsi pada model-model ini tetapi sudah usang; gunakan adaptive thinking sebagai gantinya.*\
*2 Claude Opus 5 dan Claude Haiku 5.5 menerima `"disabled"` pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah; menggabungkannya dengan effort `xhigh` atau `max` mengembalikan error 400. Pada Claude Opus 5, pembatasan ini diberlakukan pada setiap permintaan. Pada Claude Haiku 5.5, effort per pesan yang berbeda dari level yang sedang berlaku juga mengembalikan error 400.*\
*3 Claude Sonnet 5.5 menerima `"between_tools"` pada effort `high` atau lebih rendah. Menggabungkannya dengan effort `xhigh` atau `max` mengembalikan error 400, begitu pula effort per pesan yang berbeda dari level yang sedang berlaku.*

Model yang ditandai `Selalu aktif` tidak dapat menonaktifkan thinking. Model yang ditandai `Aktif` menggunakan thinking secara default. Claude Opus 5, Claude Sonnet 5, dan Claude Haiku 5.5 menerima `thinking: {type: "disabled"}`. Pada Claude Sonnet 5.5, kirim `thinking: {type: "between_tools"}` untuk menonaktifkan thinking di awal.

Model Claude 4 yang lebih lama (Claude Opus 4.1, Claude Sonnet 4, dan Claude Opus 4) hanya mendukung pemikiran diperpanjang. Lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations) untuk ketersediaannya. Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, dan Claude Mythos 5 tidak tersedia di bawah [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) kecuali diizinkan secara tegas oleh Anthropic.

## Error 400 menyatakan `"thinking.type.enabled"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Ini terjadi karena model yang Anda minta telah menghapus extended thinking (lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations)).

Ubah permintaan ke `thinking: {type: "adaptive"}` dan arahkan kedalaman thinking dengan `effort` alih-alih `budget_tokens`. [Migrasi ke adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) memandu Anda melalui konversinya.

## Error 400 setelah mengirim `thinking: {type: "disabled"}`

Permintaan gagal dengan error 400. Pada Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Opus 5.5, dan Claude Mythos 5, pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Pada Claude Mythos Preview, satu-satunya model di antara model-model ini yang menerima pemikiran diperpanjang, pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Thinking defaults to adaptive mode when not specified; use "thinking.type.enabled" with "budget_tokens" for extended thinking.
```

Hal ini terjadi karena thinking selalu aktif untuk semua model ini (lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations)).

Hilangkan parameter `thinking`; model-model ini berpikir tanpa konfigurasi apa pun. Jika tujuan Anda adalah menjaga teks thinking agar tidak muncul dalam respons, gunakan `display: "omitted"` alih-alih menonaktifkan thinking; lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

Error 400 pada `"disabled"` juga dapat terjadi pada Claude Opus 5 dan Claude Haiku 5.5, yang menerima `thinking: {type: "disabled"}` hanya pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah: menggabungkannya dengan effort `xhigh` atau `max` akan ditolak. Turunkan level effort, atau atur `thinking` ke `{"type": "adaptive"}`.

Pada Claude Sonnet 5.5, `thinking: {type: "disabled"}` mengembalikan error 400 di setiap level effort. Pesannya berbunyi:

```text wrap
To turn thinking off on this model, send "thinking": {"type": "between_tools"} instead of {"type": "disabled"}. The model does not think before responding. The short updates it writes between tool calls come back as thinking blocks.
```

Untuk menonaktifkan thinking di awal pada Claude Sonnet 5.5, kirim `thinking: {type: "between_tools"}` sebagai gantinya, pada effort `high` atau lebih rendah.

## Error 400 menyatakan `"thinking.type.between_tools"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.between_tools" is not supported for this model.
```

Hal ini terjadi karena hanya Claude Sonnet 5.5 yang menerima `thinking: {type: "between_tools"}` (lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations)).

Kirim `between_tools` hanya ke Claude Sonnet 5.5. Pada model lain, hilangkan `thinking` atau gunakan nilai `thinking.type` yang tidak tercantum sebagai ditolak dalam tabel.

## Error 400 menyatakan level effort tidak didukung saat thinking dinonaktifkan

Pada Claude Sonnet 5.5, permintaan dengan `thinking: {type: "between_tools"}` pada effort `xhigh` atau `max` gagal dengan error 400 yang pesannya berbunyi:

```text wrap
output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.
```

Hal ini terjadi karena Claude Sonnet 5.5 menerima `between_tools` hanya pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Pesan tersebut menyatakan thinking dinonaktifkan karena `between_tools` tidak memiliki thinking di awal, meskipun permintaan tidak mengirim `"disabled"`. Pesan tersebut menyebutkan level yang dikirim oleh permintaan.

Turunkan effort ke `high` atau lebih rendah. Untuk berjalan pada `xhigh` atau `max`, gunakan adaptive thinking: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`. Itulah yang dimaksud pesan tersebut dengan "enable thinking". Claude Sonnet 5.5 menolak `"enabled"` dengan error 400.

Claude Haiku 5.5 mengembalikan pesan yang sama ketika permintaan mengirim `thinking: {type: "disabled"}` pada effort `xhigh` atau `max`. Model ini menerima `"disabled"` hanya pada `high` atau lebih rendah. Turunkan effort, atau atur `thinking` ke `{"type": "adaptive"}`.

## Error 400 menyatakan effort tidak dapat berubah saat thinking dinonaktifkan

Pada Claude Sonnet 5.5, permintaan dengan `thinking: {type: "between_tools"}` yang [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta)-nya mengubah level gagal dengan error 400 yang pesannya berbunyi:

```text wrap
messages.N: output_config.effort 'low' differs from the 'high' in effect before it; effort cannot change when thinking is disabled on this model. Use effort 'high', or enable thinking.
```

Pesan tersebut menyatakan thinking dinonaktifkan karena `between_tools` tidak memiliki thinking di awal. Dengan `between_tools`, effort tidak dapat berubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari level yang sedang berlaku mengembalikan error 400. `messages.N` adalah posisi pesan yang menetapkan level baru.

Claude Haiku 5.5 mengembalikan pesan yang sama untuk perubahan effort per pesan saat `thinking: {type: "disabled"}` diatur.

Hapus effort per pesan tersebut, atau atur ke level yang sedang berlaku. Untuk memvariasikan effort per giliran, gunakan adaptive thinking, yang merupakan maksud pesan tersebut dengan "enable thinking".

Claude Haiku 5.5 mengembalikan pesan yang sama ketika permintaan dengan `thinking: {type: "disabled"}` menetapkan effort per pesan yang berbeda dari level yang sedang berlaku. Hapus effort per pesan tersebut, atau atur `thinking` ke `{"type": "adaptive"}` untuk memvariasikan effort per giliran.

## Error 400 menyatakan adaptive thinking tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
adaptive thinking is not supported on this model
```

Ini terjadi karena model hanya mendukung extended thinking (lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations)).

Gunakan `thinking: {type: "enabled", budget_tokens: N}` sebagai gantinya; lihat [Extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) untuk konfigurasinya.

## Error 400 menyatakan blok thinking tidak dapat dimodifikasi

Permintaan yang mengembalikan hasil alat gagal dengan 400 `invalid_request_error` yang pesannya berisi:

```text wrap
`thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified
```

Dalam percakapan multi-giliran dan penggunaan alat, Anda mengirim pesan asisten sebelumnya, termasuk blok `thinking` dan `redacted_thinking`-nya, kembali ke API, dan API memverifikasi bahwa blok tersebut tiba tanpa modifikasi. Error ini terjadi ketika pesan asisten yang Anda kirim kembali berbeda dari yang dikembalikan API, paling sering karena kode Anda memfilter blok konten berdasarkan tipe dan membuang blok `redacted_thinking`, atau membangun ulang pesan asisten alih-alih menggemakannya kembali.

Gemakan kembali giliran asisten secara verbatim, termasuk blok thinking. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks) untuk aturannya, dan contoh round trip lengkap di [Thinking dalam alur kerja alat dan multi-giliran](https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows#two-turn-tool-use-round-trip) untuk kode yang benar di setiap SDK.

## Error 400 menyatakan signature blok thinking tidak valid

Permintaan ke Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, atau Claude Haiku 5.5 yang memutar ulang blok thinking sebelumnya gagal dengan error 400 `invalid_request_error` yang pesannya berbunyi:

```text wrap
messages.{i}.content.{j}: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

Jika permintaan tidak mengirim header beta `thinking-binding-controls-2026-08-01`, pesan tersebut menambahkan ``That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.``

Pesan tersebut biasanya diakhiri dengan kalimat yang menyebutkan apa yang berubah: prompt `system`, daftar `tools`, pesan atau blok pertama yang berbeda, konten yang hilang atau baru, atau blok thinking sebelumnya yang hilang atau tidak berurutan. Kalimat tersebut ditujukan untuk manusia dan log. Kata-katanya dapat berubah, jadi jangan mencocokkannya di dalam kode.

Jika pesan berhenti setelah ``Invalid `signature` in `thinking` block``, signature itu sendiri tidak terverifikasi: signature terpotong, diubah, atau dikirim kembali dalam keadaan kosong, dan `prefix_mismatch_behavior` tidak berlaku. Teks thinking yang diedit mengembalikan error yang berbeda. Lihat [Error 400 menyatakan blok thinking tidak dapat dimodifikasi](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified).

Pada Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5, API menerima blok thinking yang diputar ulang hanya selama prompt `system`, `tools`, dan pesan-pesan yang mendahuluinya tidak berubah. Lihat [Menjaga prefiks tetap tidak berubah](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#prefix-check). Error ini berarti ada sesuatu yang lebih awal dalam percakapan yang berubah di antara permintaan: giliran yang diedit, diurutkan ulang, atau dihapus, pengingat per giliran yang disisipkan lalu kemudian dihapus, prompt `system` atau array `tools` yang dibangun ulang, atau compaction sisi klien yang mempertahankan giliran terbaru beserta thinking-nya apa adanya. Pemeriksaan ini diberlakukan untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, dan untuk setiap permintaan yang menetapkan `thinking.block_binding.prefix_mismatch_behavior`. [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server dan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) tidak pernah memicunya.

Untuk memperbaikinya, jaga riwayat agar hanya ditambahkan (append-only): kirim kembali giliran sebelumnya persis seperti yang dikirim dan diterima, tambahkan instruksi dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih mengedit `system` atau `tools`, dan biarkan [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server melakukan pemangkasan apa pun. Mencoba ulang body permintaan yang sama tidak menghilangkan error. Untuk melanjutkan permintaan ini tanpa penalaran yang tidak valid, kirim header beta `thinking-binding-controls-2026-08-01` dan atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Sebagai alternatif, hapus setiap blok `thinking` dan `redacted_thinking` dari riwayat (minimal blok yang disebutkan dan setiap blok setelahnya, dalam giliran tersebut dan semua giliran berikutnya), biarkan blok lain di setiap giliran tetap di tempatnya, dan coba ulang sekali. Pada Claude Sonnet 5.5 dan Claude Haiku 5.5, `block_binding` hanya berfungsi dengan `thinking: {"type": "adaptive"}`. Dengan `between_tools` pada Claude Sonnet 5.5, atau `thinking: {"type": "disabled"}` pada Claude Haiku 5.5, jaga riwayat agar append-only, atau hapus blok thinking mulai dari giliran yang diedit dan seterusnya.

Blok dari model yang tidak dapat dibaca oleh model target tidak pernah menghasilkan error ini: API membuangnya dan, di bawah header beta, melaporkannya dalam `input_transformations`.

## Field thinking kosong dalam respons

Respons berisi blok `thinking`, tetapi field `thinking`-nya adalah string kosong dan hanya field `signature` yang terisi.

Ini terjadi karena `display` secara default bernilai `"omitted"` pada model yang lebih baru, yang mengembalikan blok thinking tanpa teksnya.

Tetapkan `display: "summarized"` dalam konfigurasi thinking Anda untuk menerima teks thinking yang diringkas. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk default per model. Jika Anda hanya menginginkan baris status singkat yang ditulis beberapa model di antara pemanggilan alat, dan bukan penalarannya, tetapkan `display: "updates"` (beta) sebagai gantinya. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).

Blok yang field `thinking`-nya kosong tetap lengkap, karena `signature` menyimpan penalarannya. Kirim kembali blok tersebut bersama gilirannya seperti blok lainnya. Lihat [Kirim kembali giliran asisten persis seperti yang dikembalikan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#append-assistant-turns-exactly-as-returned).

## Tidak ada blok thinking yang muncul pada beberapa giliran

Beberapa respons tidak berisi blok `thinking` sama sekali, meskipun thinking telah dikonfigurasi.

Ini normal dalam mode adaptive: Claude melewatkan thinking pada permintaan yang dinilainya cukup sederhana untuk dijawab secara langsung.

Jika Anda ingin thinking lebih sering atau lebih mendalam, naikkan `effort` atau arahkan dengan prompting; lihat [Mengarahkan seberapa sering Claude berpikir](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior).

`tool_choice` yang dipaksakan (`{"type": "any"}` atau alat yang disebutkan namanya) juga tidak mengembalikan blok `thinking`: respons dimulai dengan pemanggilan alat. Agar model dapat berpikir sebelum memanggil alat, gunakan `tool_choice: {"type": "auto"}` dan sebutkan dalam prompt kapan harus menggunakan alat tersebut.

## Pemanggilan alat atau tag XML muncul dalam output teks

Respons sesekali menulis pemanggilan alat ke dalam teksnya alih-alih menghasilkan blok `tool_use`, atau menyertakan `<thinking>` atau tag XML internal lainnya dalam teks yang terlihat. Pemanggilan alat yang bocor tidak pernah dijalankan, dan dalam loop agentik teks yang bocor tetap berada dalam riwayat percakapan, sehingga giliran berikutnya juga terpengaruh.

Ini terjadi pada Claude Opus 5 ketika thinking dinonaktifkan, paling umum pada beban kerja yang banyak menggunakan alat seperti pencarian. Aturan prompt sistem yang menginstruksikan model untuk tidak berpikir atau tidak bernalar meningkatkan kebocoran tag.

Aktifkan kembali thinking (default) dan gunakan level `effort` yang lebih rendah untuk mengontrol biaya token sebagai gantinya. Jika integrasi Anda harus tetap menonaktifkan thinking, terapkan mitigasi prompting di [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled).

## Respons berhenti dengan `stop_reason: "max_tokens"`

Respons berakhir dengan `stop_reason: "max_tokens"`, sering kali dengan blok teks yang terpotong atau hilang.

Ini terjadi karena token thinking dihitung terhadap `max_tokens`, sehingga proses thinking yang panjang dapat menghabiskan anggaran sebelum respons teks selesai.

Naikkan `max_tokens` untuk menyisakan ruang bagi thinking dan teks, atau turunkan `effort` agar Claude menghabiskan lebih sedikit untuk thinking; lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control) dan [Thinking dan jendela konteks](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-the-context-window).

## Cache hit menurun setelah mengubah pengaturan thinking

`cache_read_input_tokens` turun menjadi nol pada permintaan yang sebelumnya mengenai cache.

Ini terjadi karena konfigurasi thinking dan level effort (atau defaultnya) merupakan bagian dari prefiks prompt yang di-cache, sehingga mengubah salah satunya memulai prefiks baru: beralih mode thinking, mengubah nilai effort, dan mengubah `budget_tokens` semuanya menginvalidasi breakpoint cache pesan, dan juga dapat menginvalidasi breakpoint alat dan prompt sistem, tergantung di mana model merender konfigurasi tersebut.

Jaga agar konfigurasi thinking dan level effort tetap konstan di seluruh permintaan yang berbagi percakapan; menetapkan parameter secara eksplisit ke nilai defaultnya setara dengan menghilangkannya dan tidak menginvalidasi. Lihat [Thinking dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

## Menetapkan effort tidak mengubah thinking

Anda mengubah `effort` tetapi frekuensi atau kedalaman thinking tetap sama.

Ini terjadi karena effort adalah tuas thinking utama hanya dalam mode adaptive. Pada model yang hanya mendukung extended thinking, kedalaman thinking ditetapkan oleh `budget_tokens`.

Sesuaikan `budget_tokens` pada model-model tersebut, atau periksa mode mana yang dijalankan model Anda; lihat [Thinking dan effort](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-effort). Pada Claude Opus 4.5, satu-satunya model khusus extended thinking yang mendukung effort, effort berpadu dengan anggaran; lihat [Aturan dan penyetelan anggaran](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Ikhtisar: apa itu thinking, cara mengonfigurasinya, dan bagaimana interaksinya dengan alat, caching, dan streaming.
  </Card>

  <Card title="Error" icon="book" href="https://platform.claude.com/docs/id/api/errors">
    Referensi error lengkap, termasuk error 400 konfigurasi thinking dengan pesan server persisnya.
  </Card>

  <Card title="Migrasi ke adaptive thinking" icon="arrow-right" href="https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking">
    Konversi permintaan `budget_tokens` ke adaptive thinking dengan effort.
  </Card>
</CardGroup>
