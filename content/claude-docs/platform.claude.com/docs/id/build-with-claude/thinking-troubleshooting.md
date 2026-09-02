---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 886920e61b9b87a38259db3d6d078547e87fd5694881f78654fdfe6bf04059eb
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

Sebagian besar error konfigurasi thinking adalah ketidakcocokan antara nilai `thinking.type` dalam permintaan dan apa yang didukung model. Pada sebagian besar model, thinking berjalan sebagai `thinking: {type: "adaptive"}`, dan banyak model mengaktifkannya secara default. Beberapa model sebelumnya justru menggunakan [extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) (pemikiran diperpanjang), mode manual lama yang dikonfigurasi sebagai `thinking: {type: "enabled", budget_tokens: N}`.

"Extended thinking" (pemikiran diperpanjang) (`thinking.type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated) pada model Claude 4.6 (permintaan yang menggunakannya masih berhasil). Claude 4.7 dan model yang lebih baru tidak mendukungnya dan menolak permintaan yang menggunakannya, dengan mengembalikan error 400. Pada Claude 4.5 dan model sebelumnya yang mendukung thinking, pemikiran diperpanjang adalah satu-satunya mode thinking yang tersedia. Claude Mythos Preview mendukung kedua mode tersebut. Jika kedua mode tersedia, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) sebagai gantinya.

Tabel ini mencantumkan apa yang didukung setiap model, apa defaultnya, dan nilai `thinking.type` mana yang ditolaknya dengan error 400; nilai apa pun yang tidak tercantum sebagai ditolak akan diterima.

| Model                 | Tipe thinking                    | Default      | Ditolak dengan 400         |
| --------------------- | -------------------------------- | ------------ | -------------------------- |
| Claude Fable 5.1      | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos 5.1     | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Fable 5        | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos 5       | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos Preview | Adaptive, extended               | Selalu aktif | `"disabled"`               |
| Claude Opus 5         | Hanya adaptive                   | Aktif        | `"enabled"`, `"disabled"`2 |
| Claude Opus 4.8       | Hanya adaptive                   | Nonaktif     | `"enabled"`                |
| Claude Opus 4.7       | Hanya adaptive                   | Nonaktif     | `"enabled"`                |
| Claude Sonnet 5       | Hanya adaptive                   | Aktif        | `"enabled"`                |
| Claude Opus 4.6       | Adaptive, extended (deprecated)1 | Nonaktif     | Tidak ada                  |
| Claude Sonnet 4.6     | Adaptive, extended (deprecated)1 | Nonaktif     | Tidak ada                  |
| Claude Opus 4.5       | Hanya extended                   | Nonaktif     | `"adaptive"`               |
| Claude Haiku 4.5      | Hanya extended                   | Nonaktif     | `"adaptive"`               |
| Claude Sonnet 4.5     | Hanya extended                   | Nonaktif     | `"adaptive"`               |

*1 `enabled` dan `budget_tokens` masih berfungsi pada model-model ini tetapi sudah deprecated; gunakan adaptive thinking sebagai gantinya.*\
*2 Claude Opus 5 menerima `"disabled"` pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah; menggabungkannya dengan effort `xhigh` atau `max` mengembalikan error 400. Pembatasan ini berlaku untuk Claude Opus 5 dan model yang lebih baru serta diberlakukan pada setiap permintaan.*

Model yang ditandai `Selalu aktif` tidak dapat menonaktifkan thinking. Model yang ditandai `Aktif` secara default menggunakan thinking tetapi menerima `thinking: {type: "disabled"}`.

Model Claude 4 sebelumnya (Claude Opus 4.1, Claude Sonnet 4, dan Claude Opus 4) hanya mendukung extended thinking. Lihat [Deprecation model](https://platform.claude.com/docs/id/about-claude/model-deprecations) untuk ketersediaannya. Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, dan Claude Mythos 5 tidak tersedia di bawah [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) kecuali diizinkan secara tegas oleh Anthropic.

## Error 400 menyatakan `"thinking.type.enabled"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Ini terjadi karena model yang Anda minta telah menghapus extended thinking (lihat [tabel konfigurasi per model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations)).

Ubah permintaan ke `thinking: {type: "adaptive"}` dan arahkan kedalaman thinking dengan `effort` alih-alih `budget_tokens`. [Migrasi ke adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) memandu Anda melalui konversinya.

## Error 400 menyatakan `"thinking.type.disabled"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Thinking defaults to adaptive mode when not specified; use "thinking.type.enabled" with "budget_tokens" for extended thinking.
```

Ini terjadi pada model yang thinking-nya selalu aktif: Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview menolak `"disabled"`. Semua model ini kecuali Claude Mythos Preview juga menolak `"thinking.type.enabled"` yang disarankan oleh teks error.

Hilangkan parameter `thinking`; model-model ini berpikir tanpa konfigurasi apa pun. Jika tujuan Anda adalah agar teks thinking tidak muncul dalam respons, gunakan `display: "omitted"` alih-alih menonaktifkan thinking; lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

Error 400 pada `"disabled"` juga dapat terjadi pada Claude Opus 5, yang menerima `thinking: {type: "disabled"}` hanya pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah: menggabungkannya dengan effort `xhigh` atau `max` akan ditolak. Turunkan level effort, atau biarkan thinking tetap aktif.

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

Permintaan ke Claude Fable 5.1 yang memutar ulang blok thinking sebelumnya gagal dengan 400 `invalid_request_error` yang pesannya berbunyi:

```text wrap
messages.{i}.content.{j}: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

Jika permintaan tidak mengirim header beta `thinking-binding-controls-2026-08-01`, pesan tersebut menambahkan ``That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.`` Pesan tersebut juga dapat diakhiri dengan kalimat yang menyebutkan pesan pertama yang berubah. Jika pesan tidak memiliki klausa alasan sama sekali, konten blok tersebut telah dimodifikasi. Lihat [Error 400 menyatakan blok thinking tidak dapat dimodifikasi](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified).

Pada Claude Fable 5.1, API menerima blok thinking yang diputar ulang [hanya selama prompt `system`, `tools`, dan pesan yang mendahuluinya tidak berubah](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation). Error ini berarti sesuatu yang lebih awal dalam percakapan berubah di antara permintaan: giliran yang diedit, diurutkan ulang, atau dihapus, pengingat per giliran yang disisipkan lalu dihapus, prompt `system` atau array `tools` yang dibangun ulang, atau compaction sisi klien yang mempertahankan giliran terbaru dan thinking-nya secara verbatim. Pemeriksaan ini diberlakukan untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, dan untuk setiap permintaan yang menetapkan `thinking.block_binding.prefix_mismatch_behavior`. [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server dan [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) tidak pernah memicunya.

Untuk memperbaikinya, jaga agar riwayat bersifat append-only: kirim kembali giliran sebelumnya persis seperti yang dikirim dan diterima, tambahkan instruksi dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) alih-alih mengedit `system` atau `tools`, dan biarkan [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server melakukan pemangkasan apa pun. Mencoba ulang body permintaan yang sama tidak menghilangkan error. Untuk melanjutkan permintaan ini tanpa penalaran yang telah diinvalidasi, kirim header beta `thinking-binding-controls-2026-08-01` dan tetapkan `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Sebagai alternatif, hapus setiap blok `thinking` dan `redacted_thinking` dari riwayat (minimal blok yang disebutkan dan setiap blok setelahnya, dalam giliran tersebut dan semua giliran berikutnya), biarkan blok lain di setiap giliran tetap di tempatnya, dan coba ulang sekali.

Blok dari model yang tidak dapat dibaca oleh model target tidak pernah menghasilkan error ini: API membuangnya dan, di bawah header beta, melaporkannya dalam `input_transformations`.

## Field thinking kosong dalam respons

Respons berisi blok `thinking`, tetapi field `thinking`-nya adalah string kosong dan hanya field `signature` yang terisi.

Ini terjadi karena `display` secara default bernilai `"omitted"` pada model yang lebih baru, yang mengembalikan blok thinking tanpa teksnya.

Tetapkan `display: "summarized"` dalam konfigurasi thinking Anda untuk menerima teks thinking yang diringkas. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk default per model. Jika Anda hanya menginginkan baris status singkat yang ditulis beberapa model di antara pemanggilan alat, dan bukan penalarannya, tetapkan `display: "updates"` (beta) sebagai gantinya. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).

## Tidak ada blok thinking yang muncul pada beberapa giliran

Beberapa respons tidak berisi blok `thinking` sama sekali, meskipun thinking telah dikonfigurasi.

Ini normal dalam mode adaptive: Claude melewatkan thinking pada permintaan yang dinilainya cukup sederhana untuk dijawab secara langsung.

Jika Anda ingin thinking lebih sering atau lebih mendalam, naikkan `effort` atau arahkan dengan prompting; lihat [Mengarahkan seberapa sering Claude berpikir](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior).

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
