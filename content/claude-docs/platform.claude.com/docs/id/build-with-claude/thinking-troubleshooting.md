---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: c177eea6c2c2aec15c8b99fe83b866b9fbbe7c2b78007994fc36f1f0e3bc33c8
---

# Pemecahan masalah thinking

Diagnosis dan perbaiki kegagalan thinking yang paling umum: error konfigurasi 400, blok thinking kosong atau hilang, berhenti karena max_tokens, dan cache miss.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Halaman ini membahas kegagalan paling umum saat mengonfigurasi thinking atau melakukan round-trip blok thinking (mengirim kembali blok thinking yang dikembalikan dalam permintaan berikutnya). Bagian pertama memetakan setiap model ke konfigurasi thinking yang didukungnya dan yang ditolaknya; bagian-bagian setelahnya masing-masing dimulai dari gejala yang Anda amati, sehingga Anda dapat mencocokkan pesan error atau respons yang tidak terduga langsung ke penyebab dan perbaikannya. Untuk cara kerja thinking, lihat ikhtisar [Thinking](/docs/id/build-with-claude/thinking).

## Konfigurasi yang ditolak setiap model

Sebagian besar error konfigurasi thinking adalah ketidakcocokan antara nilai `thinking.type` dalam permintaan dan apa yang didukung model. Pada model saat ini, thinking berjalan sebagai `thinking: {type: "adaptive"}`, dan pada model terbaru thinking aktif secara default. Beberapa model sebelumnya menggunakan [extended thinking](/docs/id/build-with-claude/extended-thinking) (pemikiran diperpanjang), mode manual lama yang dikonfigurasi sebagai `thinking: {type: "enabled", budget_tokens: N}`.

Extended thinking (pemikiran diperpanjang) (`thinking.type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated) pada model Claude 4.6 (permintaan yang menggunakannya masih berhasil). Model Claude 4.7 dan yang lebih baru tidak mendukungnya dan menolak permintaan yang menggunakannya, dengan mengembalikan error 400. Pada model Claude 4.5 dan yang lebih lama yang mendukung thinking, pemikiran diperpanjang adalah satu-satunya mode thinking yang tersedia. Claude Mythos Preview mendukung kedua mode. Jika kedua mode tersedia, gunakan [adaptive thinking](/docs/id/build-with-claude/thinking) sebagai gantinya.

Tabel ini mencantumkan apa yang didukung setiap model, apa defaultnya, dan nilai `thinking.type` mana yang ditolaknya dengan error 400; nilai apa pun yang tidak tercantum sebagai ditolak akan diterima.

| Model                        | Tipe thinking                    | Default      | Ditolak dengan 400         |
| ---------------------------- | -------------------------------- | ------------ | -------------------------- |
| Claude Fable 5               | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos 5              | Hanya adaptive                   | Selalu aktif | `"enabled"`, `"disabled"`  |
| Claude Mythos Preview        | Adaptive, extended               | Selalu aktif | `"disabled"`               |
| Claude Opus 5                | Hanya adaptive                   | Aktif        | `"enabled"`, `"disabled"`2 |
| Claude Opus 4.8              | Hanya adaptive                   | Nonaktif     | `"enabled"`                |
| Claude Opus 4.7              | Hanya adaptive                   | Nonaktif     | `"enabled"`                |
| Claude Sonnet 5              | Hanya adaptive                   | Aktif        | `"enabled"`                |
| Claude Opus 4.6              | Adaptive, extended (deprecated)1 | Nonaktif     | Tidak ada                  |
| Claude Sonnet 4.6            | Adaptive, extended (deprecated)1 | Nonaktif     | Tidak ada                  |
| Claude Opus 4.5              | Hanya extended                   | Nonaktif     | `"adaptive"`               |
| Claude Haiku 4.5             | Hanya extended                   | Nonaktif     | `"adaptive"`               |
| Claude Sonnet 4.5            | Hanya extended                   | Nonaktif     | `"adaptive"`               |
| Claude Opus 4.1 (deprecated) | Hanya extended                   | Nonaktif     | `"adaptive"`               |

*1 `enabled` dan `budget_tokens` masih berfungsi pada model-model ini tetapi sudah deprecated; gunakan adaptive thinking sebagai gantinya.*\
*2 Claude Opus 5 menerima `"disabled"` pada [effort](/docs/id/build-with-claude/effort) `high` atau di bawahnya; menggabungkannya dengan effort `xhigh` atau `max` mengembalikan error 400. Pembatasan ini berlaku untuk Claude Opus 5 dan model-model setelahnya dan diberlakukan pada setiap permintaan.*

Model yang ditandai `Selalu aktif` tidak dapat menonaktifkan thinking. Model yang ditandai `Aktif` secara default melakukan thinking tetapi menerima `thinking: {type: "disabled"}`.

Model Claude 4 yang lebih awal (Claude Sonnet 4 dan Claude Opus 4) hanya mendukung extended thinking; lihat [deprecation model](/docs/id/about-claude/model-deprecations) untuk ketersediaannya. Claude Fable 5 dan Claude Mythos 5 tidak tersedia di bawah [zero data retention](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

## Error 400 menyatakan `"thinking.type.enabled"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Ini terjadi karena model yang Anda minta telah menghapus extended thinking (lihat [Konfigurasi yang ditolak setiap model](#rejected-configurations)).

Alihkan permintaan ke `thinking: {type: "adaptive"}` dan kendalikan kedalaman thinking dengan `effort` alih-alih `budget_tokens`. [Migrasi ke adaptive thinking](/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking) memandu proses konversinya.

## Error 400 menyatakan `"thinking.type.disabled"` tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
"thinking.type.disabled" is not supported for this model. Thinking defaults to adaptive mode when not specified; use "thinking.type.enabled" with "budget_tokens" for extended thinking.
```

Ini terjadi pada model di mana thinking selalu aktif: Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview menolak `"disabled"`. Pada Claude Fable 5 dan Claude Mythos 5, saran dalam teks error untuk menggunakan `"thinking.type.enabled"` juga tidak berlaku: model-model tersebut juga menolaknya.

Hilangkan parameter `thinking`; model-model ini melakukan thinking tanpa konfigurasi apa pun. Jika tujuan Anda adalah menjaga teks thinking agar tidak muncul dalam respons, gunakan `display: "omitted"` alih-alih menonaktifkan thinking; lihat [Mengontrol tampilan thinking](/docs/id/build-with-claude/thinking#controlling-thinking-display).

Error 400 pada `"disabled"` juga dapat terjadi pada Claude Opus 5, yang menerima `thinking: {type: "disabled"}` hanya pada [effort](/docs/id/build-with-claude/effort) `high` atau di bawahnya: menggabungkannya dengan effort `xhigh` atau `max` akan ditolak. Turunkan tingkat effort, atau biarkan thinking tetap aktif.

## Error 400 menyatakan adaptive thinking tidak didukung

Permintaan gagal dengan error 400 yang pesannya berbunyi:

```text wrap
adaptive thinking is not supported on this model
```

Ini terjadi karena model hanya mendukung extended thinking (lihat [Konfigurasi yang ditolak setiap model](#rejected-configurations)).

Gunakan `thinking: {type: "enabled", budget_tokens: N}` sebagai gantinya; lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking) untuk konfigurasinya.

## Error 400 menyatakan blok thinking tidak dapat dimodifikasi

Permintaan yang mengembalikan hasil alat gagal dengan 400 `invalid_request_error` yang pesannya berisi:

```text wrap
`thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified
```

Dalam percakapan multi-giliran dan penggunaan alat, Anda mengirim pesan assistant sebelumnya, termasuk blok `thinking` dan `redacted_thinking`-nya, kembali ke API, dan API memverifikasi bahwa pesan tersebut tiba tanpa modifikasi. Error ini terjadi ketika pesan assistant yang Anda kirim kembali berbeda dari yang dikembalikan API, paling sering karena kode Anda memfilter blok konten berdasarkan tipe dan membuang blok `redacted_thinking`, atau membangun ulang pesan assistant alih-alih menggemakannya kembali.

Gemakan kembali giliran assistant secara verbatim, termasuk blok thinking-nya. Lihat [Mempertahankan blok thinking](/docs/id/build-with-claude/thinking#preserving-thinking-blocks) untuk aturannya, dan contoh round trip yang dikerjakan di [Thinking dalam alur kerja alat dan multi-giliran](/docs/id/build-with-claude/thinking-tool-workflows#two-turn-tool-use-round-trip) untuk kode yang benar di setiap SDK.

## Field thinking kosong dalam respons

Respons berisi blok `thinking`, tetapi field `thinking`-nya berupa string kosong dan hanya field `signature` yang terisi.

Ini terjadi karena `display` secara default bernilai `"omitted"` pada model yang lebih baru, yang mengembalikan blok thinking tanpa teksnya.

Atur `display: "summarized"` dalam konfigurasi thinking Anda untuk menerima teks thinking yang diringkas; lihat [Mengontrol tampilan thinking](/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk default per model.

## Tidak ada blok thinking yang muncul pada beberapa giliran

Beberapa respons sama sekali tidak berisi blok `thinking`, meskipun thinking sudah dikonfigurasi.

Ini normal dalam mode adaptive: Claude melewatkan thinking pada permintaan yang dinilainya cukup sederhana untuk dijawab langsung.

Jika Anda ingin thinking lebih sering atau lebih dalam, naikkan `effort` atau arahkan dengan prompting; lihat [Mengarahkan seberapa sering Claude berpikir](/docs/id/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior).

## Panggilan alat atau tag XML muncul dalam output teks

Sebuah respons kadang-kadang menuliskan panggilan alat ke dalam teksnya alih-alih mengeluarkan blok `tool_use`, atau menyertakan `<thinking>` atau tag XML internal lainnya dalam teks yang terlihat. Panggilan alat yang bocor tidak pernah dijalankan, dan dalam loop agentik teks yang bocor tetap berada dalam riwayat percakapan, sehingga giliran-giliran berikutnya juga terpengaruh.

Ini terjadi pada Claude Opus 5 ketika thinking dinonaktifkan, paling umum pada beban kerja yang banyak menggunakan alat seperti pencarian. Aturan prompt sistem yang menginstruksikan model untuk tidak berpikir atau tidak bernalar meningkatkan kebocoran tag.

Aktifkan kembali thinking (default) dan gunakan tingkat `effort` yang lebih rendah untuk mengontrol biaya token sebagai gantinya. Jika integrasi Anda harus tetap menonaktifkan thinking, terapkan mitigasi prompting di [Menjalankan dengan thinking dinonaktifkan](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled).

## Respons berhenti dengan `stop_reason: "max_tokens"`

Respons berakhir dengan `stop_reason: "max_tokens"`, sering kali dengan blok teks yang terpotong atau hilang.

Ini terjadi karena token thinking dihitung terhadap `max_tokens`, sehingga proses thinking yang panjang dapat menghabiskan anggaran sebelum respons teks selesai.

Naikkan `max_tokens` untuk menyisakan ruang bagi thinking dan teks, atau turunkan `effort` agar Claude menghabiskan lebih sedikit untuk thinking; lihat [Kontrol biaya](/docs/id/build-with-claude/thinking-steering-and-cost#cost-control) dan [Thinking dan jendela konteks](/docs/id/build-with-claude/thinking#thinking-and-the-context-window).

## Cache hit turun setelah mengubah pengaturan thinking

`cache_read_input_tokens` turun menjadi nol pada permintaan yang sebelumnya mengenai cache.

Ini terjadi karena konfigurasi thinking dan tingkat effort (atau defaultnya) adalah bagian dari prefiks prompt yang di-cache, sehingga mengubah salah satunya memulai prefiks baru: beralih mode thinking, mengubah nilai effort, dan mengubah `budget_tokens` semuanya membatalkan breakpoint cache pesan, dan juga dapat membatalkan breakpoint alat dan prompt sistem, tergantung di mana model merender konfigurasinya.

Jaga konfigurasi thinking dan tingkat effort tetap konstan di seluruh permintaan yang berbagi percakapan; mengatur parameter secara eksplisit ke nilai defaultnya setara dengan menghilangkannya dan tidak membatalkan cache. Lihat [Thinking dan caching prompt](/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

## Mengatur effort tidak mengubah thinking

Anda mengubah `effort` tetapi frekuensi atau kedalaman thinking tetap sama.

Ini terjadi karena effort adalah tuas utama thinking hanya dalam mode adaptive. Pada model yang hanya mendukung extended thinking, kedalaman thinking diatur oleh `budget_tokens`.

Sesuaikan `budget_tokens` pada model-model tersebut, atau periksa mode mana yang dijalankan model Anda; lihat [Thinking dan effort](/docs/id/build-with-claude/thinking#thinking-and-effort). Pada Claude Opus 4.5, satu-satunya model yang hanya mendukung extended thinking dan mendukung effort, effort berkomposisi dengan anggaran; lihat [Aturan anggaran dan penyetelan](/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Thinking" icon="brain" href="/docs/id/build-with-claude/thinking">
    Ikhtisar: apa itu thinking, cara mengonfigurasinya, dan bagaimana interaksinya dengan alat, caching, dan streaming.
  </Card>

  <Card title="Error" icon="book" href="/docs/id/api/errors">
    Referensi error lengkap, termasuk error 400 konfigurasi thinking dengan pesan server persisnya.
  </Card>

  <Card title="Migrasi ke adaptive thinking" icon="arrow-right" href="/docs/id/build-with-claude/extended-thinking#migrating-to-adaptive-thinking">
    Konversi permintaan `budget_tokens` ke adaptive thinking dengan effort.
  </Card>
</CardGroup>
