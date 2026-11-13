---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: e2220aefe787f9606b0eea5499a549533db940ba52174e64fa9bd467dfc1e155
---

---
title: Batas laju
url: https://platform.claude.com/docs/id/api/rate-limits
description: Untuk memitigasi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan mengenai seberapa banyak sebuah organisasi dapat menggunakan Claude API.
---

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas laju di halaman ini berlaku untuk Claude Platform on AWS, tetapi penagihan dan pengelolaan batasnya berbeda. Penagihan dilakukan melalui AWS Marketplace (bukan pembelian kredit Anthropic). Organisasi di Claude Platform on AWS ditempatkan pada tingkat Start dan dapat berpindah ke tingkat yang lebih tinggi secara otomatis seiring mereka membangun riwayat faktur AWS Marketplace yang telah dibayar. Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com); alur **Minta kenaikan tingkat** tidak tersedia. Konfigurasi batas laju per workspace dan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (mode cepat) tidak tersedia di Claude Platform on AWS. Untuk detailnya, lihat [Batas laju dan kuota di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

Ada dua jenis batas:

1. **Batas pengeluaran** (“spend limits”) menetapkan biaya bulanan maksimum yang dapat dikeluarkan sebuah organisasi untuk penggunaan API.
2. **Batas laju** (“rate limits”) menetapkan jumlah maksimum permintaan API yang dapat dibuat sebuah organisasi dalam periode waktu tertentu.

API menerapkan batas yang dikonfigurasi oleh layanan di tingkat organisasi, tetapi Anda juga dapat menetapkan batas yang dapat dikonfigurasi pengguna untuk workspace organisasi Anda.

## Tentang batas laju

* Batas dirancang untuk mencegah penyalahgunaan API, sekaligus meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batas ditentukan berdasarkan **tingkat penggunaan** (“usage tier”). Organisasi ditempatkan pada suatu tingkat secara otomatis berdasarkan riwayat penggunaan dan status akun, serta dapat berpindah ke tingkat yang lebih tinggi seiring waktu saat mereka menggunakan API.
* Organisasi baru dan organisasi dengan riwayat penggunaan terbatas mungkin memulai di tingkat Evaluation, dengan batas di bawah batas standar yang ditampilkan di halaman ini selagi riwayat akun dibangun. Batas awal ini merupakan bagian dari cara Anthropic mencegah penipuan dan penyalahgunaan, dan batas tersebut meningkat secara otomatis seiring organisasi Anda membangun riwayat penggunaan.
* Batas ditetapkan di tingkat organisasi. Anda dapat melihat tingkat dan batas organisasi Anda saat ini di halaman [Batas laju](https://platform.claude.com/usage/limits) (`platform.claude.com/usage/limits`) di [Claude Console](https://platform.claude.com/).
* Anda mungkin mencapai batas laju dalam interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) mungkin diberlakukan sebagai 1 permintaan per detik. Lonjakan permintaan singkat dapat melampaui batas dan memicu error batas laju.
* Batas berikut adalah batas standar untuk setiap tingkat. Jika Anda memerlukan batas yang lebih tinggi, lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus diisi ulang hingga batas maksimum Anda, bukan direset pada interval tetap.
* Semua batas yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan minimum yang dijamin. Batas ini dimaksudkan untuk mengurangi pengeluaran berlebih yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas pengeluaran bulanan yang sama berlaku, dan permintaan berhenti pada batas tersebut dengan cara yang sama. Penagihan dan kenaikan tingkat bekerja secara berbeda; lihat [Batas pengeluaran di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits).
</Note>

Masing-masing tingkat Start, Build, dan Scale memiliki batas pengeluaran bulanan (“monthly spend cap”). Batas ini adalah jumlah maksimum yang dapat dibelanjakan organisasi Anda untuk API setiap bulan kalender. Anda dapat melihat batas pengeluaran bulanan organisasi Anda dan menetapkan batas Anda sendiri di [Batas pengeluaran di Claude Console](https://platform.claude.com/settings/spend-limits) (`platform.claude.com/settings/spend-limits`).

| Tingkat penggunaan | Batas pengeluaran bulanan |
| ------------------ | ------------------------- |
| Start              | $500 USD                  |
| Build              | $1.000 USD                |
| Scale              | $200.000 USD              |

Organisasi pada tingkat Custom tidak memiliki batas pengeluaran bulanan; batasnya diatur bersama tim akun mereka.

### Mencapai batas pengeluaran Anda

Setelah Anda mencapai batas pengeluaran tingkat Anda, penggunaan API dijeda hingga pukul 00:00 UTC pada hari pertama bulan berikutnya, kecuali Anda meminta batas yang lebih tinggi lebih awal. Selama penggunaan dijeda, permintaan API mengembalikan HTTP 429:

```json
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "You have reached your API usage limits: your organization has crossed its monthly API usage threshold, set based on your organization's API tier. You will regain access on 2026-09-01 at 00:00 UTC.",
    "details": { "error_code": "enforced_spend_limit_reached" }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

* Tipe error-nya adalah `rate_limit_error`, sama seperti untuk batas laju, tetapi respons tidak memiliki header `retry-after`. Mencoba ulang, termasuk percobaan ulang otomatis SDK, akan gagal hingga akses dipulihkan.
* Pada Messages API, `error.details.error_code` bernilai `enforced_spend_limit_reached`. Gunakan ini untuk membedakan respons ini dari batas laju.
* Berpindah ke tingkat yang lebih tinggi memulihkan akses; lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).

### Menetapkan batas pengeluaran Anda sendiri

Anda juga dapat menetapkan batas pengeluaran Anda sendiri di bawah batas tingkat Anda untuk mengendalikan biaya:

<Steps>
  <Step title="Buka batas pengeluaran Anda">
    Buka [Batas pengeluaran di Claude Console](https://platform.claude.com/settings/spend-limits) (`platform.claude.com/settings/spend-limits`).
  </Step>

  <Step title="Buka editor batas pengeluaran">
    Di samping **Batas pengeluaran bulanan** organisasi Anda, klik **Sesuaikan batas** atau **Tetapkan batas**.
  </Step>

  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas pengeluaran Anda tidak dapat melebihi batas tingkat Anda saat ini.
  </Step>
</Steps>

Ketika penggunaan mencapai batas pengeluaran yang Anda tetapkan, permintaan mengembalikan HTTP 400 dengan jenis error `invalid_request_error`. Pesannya diawali dengan `You have reached your specified API usage limits`, atau `You have reached your specified workspace API usage limits` untuk batas workspace, dan menyebutkan kapan akses dipulihkan. Naikkan atau hapus batas tersebut untuk memulihkan akses lebih cepat.

Batas pada [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace) diperiksa secara terpisah: permintaan Claude Code yang melampaui batas workspace tersebut justru dapat menerima 429 yang membawa header `retry-after`.

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model. Jika Anda melebihi salah satu batas laju, Anda mendapatkan [error 429](https://platform.claude.com/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui. Ketika respons memiliki header `retry-after`, tunggu selama jumlah detik tersebut sebelum mencoba ulang.

<Note>
  Peningkatan penggunaan yang tajam juga dapat menyebabkan error 429. Lihat [Batas ramp](https://platform.claude.com/docs/id/api/rate-limits#ramp-limits).
</Note>

### ITPM yang sadar cache

**Batas laju ITPM default API hanya menghitung token input yang tidak di-cache.** Hal ini membuat batas laju secara efektif lebih tinggi daripada yang mungkin terlihat pada awalnya.

Batas laju ITPM diperkirakan di awal setiap permintaan, dan perkiraan tersebut disesuaikan selama permintaan untuk mencerminkan jumlah token input aktual yang digunakan.

Berikut yang dihitung terhadap ITPM:

* `input_tokens` (token setelah breakpoint cache terakhir) ✓ **Dihitung terhadap ITPM**
* `cache_creation_input_tokens` (token yang sedang ditulis ke cache) ✓ **Dihitung terhadap ITPM**
* `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung terhadap ITPM**

<Note>
  Field `input_tokens` hanya mewakili token yang muncul **setelah breakpoint cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

  ```text wrap
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen yang di-cache sebesar 200 ribu token dan pertanyaan pengguna sebesar 50 token, Anda akan melihat `input_tokens: 50` meskipun total inputnya adalah 200.050 token.

  Untuk keperluan batas laju, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung terhadap batas ITPM Anda, menjadikan [“prompt caching” (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) cara yang efektif untuk meningkatkan throughput Anda.
</Note>

**Contoh:** Dengan batas ITPM 2.000.000 dan tingkat cache hit 80 persen, Anda secara efektif dapat memproses total 10.000.000 token input per menit (2 juta tidak di-cache + 8 juta di-cache), karena token yang di-cache tidak dihitung terhadap batas laju Anda. Token yang di-cache tersebut ditagih dengan [tarif baca cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pricing), sebagian kecil dari harga input dasar.

Untuk mendapatkan throughput tertinggi dalam batas laju Anda, cache konten yang berulang seperti instruksi sistem dan prompt, dokumen konteks besar, definisi alat, dan riwayat percakapan; lihat [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk panduan. Dengan caching yang efektif, Anda dapat meningkatkan throughput aktual Anda secara substansial tanpa menaikkan batas laju Anda. Pantau tingkat cache hit Anda di halaman [Penggunaan](https://platform.claude.com/usage) di Claude Console untuk menyempurnakan strategi caching Anda.

Batas laju OTPM dievaluasi secara real time saat token output dihasilkan, dengan hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak diperhitungkan dalam kalkulasi batas laju OTPM, sehingga tidak ada kerugian terkait batas laju jika menetapkan nilai `max_tokens` yang lebih tinggi.

Setiap baris dalam tabel berikut memiliki batas RPM, ITPM, dan OTPM tersendiri. Beberapa baris mencakup beberapa model yang berbagi satu batas; lihat catatan setelah tabel. Anda dapat memeriksa “rate limit” (batas laju) dan perilaku Anda saat ini di halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console, atau membaca batas yang dikonfigurasi dan menetapkan batas workspace secara terprogram dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

<Note>
  Batas laju dibagikan di semua nilai `inference_geo`. Permintaan dengan `inference_geo: "us"` dan `inference_geo: "global"` mengambil dari kumpulan batas laju yang sama.
</Note>

<Tabs>
  <Tab title="Tingkat Start">
    | Model                                           | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.2                                | 4.000                               | 500.000                               | 100.000                                |
    | Claude Fable 5.1 dan Claude Fable 5<sup>1</sup> | 4.000                               | 500.000                               | 100.000                                |
    | Claude Opus 5.5                                 | 4.000                               | 2.000.000                             | 400.000                                |
    | Claude Opus 5                                   | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Opus 4.x<sup>2</sup>                     | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 5.5                               | 4.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 5                                 | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 4.x<sup>3</sup>                   | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 5.5                                | 4.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 4.5                                | 1.000                               | 2.000.000                             | 400.000                                |
  </Tab>

  <Tab title="Tingkat Build">
    | Model                                           | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.2                                | 10.000                              | 1.500.000                             | 300.000                                |
    | Claude Fable 5.1 dan Claude Fable 5<sup>1</sup> | 10.000                              | 1.500.000                             | 300.000                                |
    | Claude Opus 5.5                                 | 10.000                              | 5.000.000                             | 1.000.000                              |
    | Claude Opus 5                                   | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Opus 4.x<sup>2</sup>                     | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 5.5                               | 10.000                              | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 5                                 | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 4.x<sup>3</sup>                   | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 5.5                                | 10.000                              | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 4.5                                | 5.000                               | 5.000.000                             | 1.000.000                              |
  </Tab>

  <Tab title="Tingkat Scale">
    | Model                                           | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.2                                | 13.000                              | 4.000.000                             | 800.000                                |
    | Claude Fable 5.1 dan Claude Fable 5<sup>1</sup> | 13.000                              | 4.000.000                             | 800.000                                |
    | Claude Opus 5.5                                 | 13.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Opus 5                                   | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Opus 4.x<sup>2</sup>                     | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 5.5                               | 13.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 5                                 | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 4.x<sup>3</sup>                   | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 5.5                                | 13.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 4.5                                | 10.000                              | 10.000.000                            | 2.000.000                              |
  </Tab>

  <Tab title="Tingkat Custom">
    Jika Anda memerlukan batas yang lebih tinggi dari tingkat Scale, hubungi tim penjualan melalui halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console.
  </Tab>
</Tabs>

*<sup>1 Batas laju Fable adalah batas total yang berlaku untuk lalu lintas gabungan di Claude Fable 5.1 dan Claude Fable 5. Claude Fable 5.2 memiliki batas laju terpisah dan bukan bagian dari kelompok gabungan ini. Claude Mythos 5.2, Claude Mythos 5.1, dan Claude Mythos 5 berbagi batas gabungan terpisah.</sup>*

*<sup>2 Batas laju Opus adalah batas total yang berlaku untuk lalu lintas gabungan di Claude Opus 4.8, Opus 4.7, Opus 4.6, dan Opus 4.5. Claude Opus 5.5 dan Claude Opus 5 masing-masing memiliki batas laju terpisah dan bukan bagian dari kelompok gabungan ini.</sup>*

*<sup>3 Batas laju Sonnet 4.x adalah batas total yang berlaku untuk lalu lintas gabungan di Sonnet 4.6 dan Sonnet 4.5 (tidak digunakan lagi; lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations)). Claude Sonnet 5.5 dan Claude Sonnet 5 masing-masing memiliki batas laju terpisah dan bukan bagian dari kelompok gabungan ini.</sup>*

### Batas ramp

“Ramp limit” (batas ramp) membatasi seberapa cepat penggunaan token organisasi Anda pada suatu model dapat bertumbuh. Setelah peningkatan penggunaan yang tajam, permintaan dapat mengembalikan error 429 meskipun Anda masih berada di bawah batas laju ITPM dan OTPM Anda. Lonjakan permintaan dalam beberapa detik juga dapat dihitung sebagai peningkatan yang tajam.

Batas ramp Anda adalah penggunaan per menit tertinggi organisasi Anda untuk model tersebut dalam waktu belakangan ini, ditambah satu langkah. Setiap menit Anda dapat naik hingga satu langkah di atas puncak tersebut, sehingga batas meningkat seiring bertumbuhnya penggunaan Anda yang berhasil. Batas berhenti naik pada batas laju Anda. Setelah periode penggunaan yang lebih rendah, batas ramp turun kembali. Batas tidak pernah turun di bawah jumlah awal, bahkan jika Anda belum menggunakan model tersebut baru-baru ini.

* Batas ramp dapat berlaku untuk model apa pun.
* Token input dan token output dihitung secara terpisah.
* Penggunaan [mode cepat](https://platform.claude.com/docs/id/api/rate-limits#fast-mode-rate-limits) memiliki batas ramp tersendiri, terpisah dari penggunaan standar model yang sama.
* Seperti pada [ITPM yang sadar cache](https://platform.claude.com/docs/id/api/rate-limits#cache-aware-itpm), token yang dibaca dari cache tidak dihitung terhadap batas ramp. Token input yang tidak di-cache dan token yang ditulis ke cache dihitung.
* Langkah dan jumlah awal bervariasi menurut model dan dapat berubah. Pesan error biasanya menyebutkan batas ramp Anda saat ini, langkahnya, dan batas laju Anda.
* Tipe error-nya adalah `rate_limit_error`, sama seperti untuk batas laju. Pada Messages API, `error.details.error_code` bernilai `ramp_limit_exceeded`. Gunakan ini untuk membedakan respons ini dari batas laju.
* [Message Batches API](https://platform.claude.com/docs/id/api/rate-limits#message-batches-api) tidak dikenai batas ramp.

Jika Anda mendapatkan 429 dari batas ramp:

* Tunggu setidaknya selama jumlah detik di header `retry-after` sebelum mencoba ulang.
* Pertahankan lalu lintas Anda pada tingkat di mana permintaan berhasil, lalu tingkatkan paling banyak satu langkah per menit.
* Mulai pekerjaan terjadwal atau massal pada laju yang rendah dan sebarkan permintaan secara merata, alih-alih mengirim semuanya sekaligus.

### Message Batches API

Message Batches API memiliki set batas lajunya sendiri, yang dibagikan di semua model. Ini mencakup batas permintaan per menit (RPM) untuk semua endpoint API dan batas jumlah permintaan batch yang dapat berada dalam antrean pemrosesan pada saat yang sama. “Permintaan batch” di sini mengacu pada bagian dari sebuah Message Batch. Anda dapat membuat Message Batch yang berisi ribuan permintaan batch, yang masing-masing dihitung terhadap batas ini. Sebuah permintaan batch tetap berada dalam antrean pemrosesan hingga model berhasil memprosesnya.

<Tabs>
  <Tab title="Tingkat Start">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 1.000                               | 200.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tingkat Build">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 2.000                               | 300.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tingkat Scale">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 4.000                               | 500.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tingkat Custom">
    Jika Anda memerlukan batas yang lebih tinggi dari tingkat Scale, hubungi tim penjualan melalui halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console.
  </Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dibatasi lajunya untuk setiap organisasi. Batas ini terpisah dari batas laju Messages API yang dijelaskan sebelumnya di halaman ini.

| Operasi                                                        | Batas                      |
| -------------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (misalnya, agen, sesi, dan lingkungan)      | 300 permintaan per menit   |
| Endpoint pembacaan (misalnya, pengambilan, daftar, dan stream) | 1.200 permintaan per menit |

### Files API

Permintaan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) memiliki batas per organisasinya sendiri, yang dibagi bersama di seluruh operasi unggah, daftar, pengambilan, unduh, dan penghapusan serta terpisah dari batas Messages API yang dijelaskan sebelumnya di halaman ini. Lihat [batas laju Files API](https://platform.claude.com/docs/id/build-with-claude/files#rate-limits) untuk nilai saat ini.

### Batas laju mode cepat

Saat Anda menggunakan [mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) dengan `speed: "fast"`, berlaku batas laju khusus yang terpisah dari batas laju standar. Batas ini berlaku pada Claude Fable 5.2, Claude Mythos 5.2, Claude Opus 5.5, Claude Opus 5, dan Claude Opus 4.8. Mode cepat berada dalam pratinjau riset untuk Claude Opus 5 dan usang (deprecated) untuk Claude Opus 4.8.

Claude Fable 5.2, Claude Mythos 5.2, dan Claude Opus 5.5 memiliki batas laju mode cepat default. Batas default tersebut berlaku di tingkat Start, Build, dan Scale. Anda tidak perlu meminta akses mode cepat untuk model-model ini. Organisasi di tingkat Evaluation dapat menggunakan mode cepat dengan model-model ini setelah mereka berpindah ke tingkat Start, Build, atau Scale.

Untuk melihat batas laju mode cepat Anda, buka halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console. Ketika Anda melampaui batas laju mode cepat Anda, API mengembalikan error `429` dengan header `retry-after`.

Respons menyertakan header `anthropic-fast-*` yang menunjukkan status batas laju mode cepat Anda. Lihat [Batas laju mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Penggunaan](https://platform.claude.com/usage) di [Claude Console](https://platform.claude.com/).

Selain menyediakan grafik token dan permintaan, halaman **Penggunaan** menyediakan dua grafik batas laju terpisah. Gunakan grafik ini untuk melihat ruang yang Anda miliki untuk berkembang, mengidentifikasi kapan Anda mungkin mencapai puncak penggunaan, memahami batas laju apa yang perlu diminta, dan mempelajari cara meningkatkan tingkat caching Anda. Grafik tersebut memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya, untuk setiap model):

* Grafik **Rate Limit - Input Tokens** mencakup:

  * Maksimum per jam dari token input yang tidak di-cache per menit
  * Batas laju token input per menit Anda saat ini
  * Tingkat cache untuk token input Anda (yaitu, persentase token input yang dibaca dari cache)

* Grafik **Rate Limit - Output Tokens** mencakup:

  * Maksimum per jam dari token output per menit
  * Batas laju token output per menit Anda saat ini

## Meminta batas yang lebih tinggi

Untuk meminta batas laju yang lebih tinggi atau batas pengeluaran bulanan yang lebih tinggi, gunakan **Minta kenaikan tingkat** di halaman [Batas laju](https://platform.claude.com/usage/limits) di Claude Console. Dukungan Anthropic juga dapat menaikkan batas; untuk kebutuhan mendesak, hubungi [dukungan Anthropic](https://support.claude.com).

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Alur **Minta kenaikan tingkat** tidak tersedia. Hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com), dan sertakan model yang perlu dinaikkan batasnya, token input dan output puncak per menit untuk setiap model, serta perkiraan porsi input Anda yang merupakan konteks yang di-cache atau berulang. Lihat [Batas laju dan kuota di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

## Menetapkan batas yang lebih rendah untuk workspace

Untuk informasi lebih lanjut tentang workspace, lihat [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces).

Untuk melindungi workspace di organisasi Anda dari potensi penggunaan berlebih, Anda dapat menetapkan batas pengeluaran dan batas laju khusus untuk setiap workspace.

Contoh: Jika batas organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda dapat membatasi satu workspace hingga 30.000 token input per menit. Ini melindungi workspace lain dari potensi penggunaan berlebih dan membagi sumber daya secara lebih merata di seluruh organisasi Anda. Sisa 10.000 token input per menit, ditambah bagian mana pun dari 30.000 yang tidak digunakan oleh workspace tersebut, tetap tersedia untuk workspace lain.

Catatan:

* Anda tidak dapat menetapkan batas pengeluaran pada workspace default.
* Jika tidak ditetapkan, batas workspace sama dengan batas organisasi.
* Batas workspace ditetapkan untuk setiap jenis pembatas (seperti permintaan per menit, token input per menit, atau token output per menit).
* Batas tingkat organisasi selalu berlaku, meskipun jumlah batas workspace lebih besar.

Untuk membaca batas laju organisasi dan workspace Anda saat ini atau menetapkan batas laju workspace secara terprogram, gunakan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Header respons

Respons API menyertakan header yang menunjukkan batas laju yang diberlakukan, penggunaan saat ini, dan kapan batas direset.

Header berikut dikembalikan:

| Header                                        | Deskripsi                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `retry-after`                                 | Jumlah detik yang harus ditunggu hingga Anda dapat mencoba ulang permintaan. Percobaan ulang yang lebih awal mungkin gagal. Tidak semua 429 membawa header ini; 429 batas pengeluaran tidak pernah membawanya (lihat [Mencapai batas pengeluaran Anda](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap)). |
| `anthropic-ratelimit-requests-limit`          | Jumlah maksimum permintaan yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                                                           |
| `anthropic-ratelimit-requests-remaining`      | Jumlah permintaan yang tersisa sebelum dibatasi lajunya.                                                                                                                                                                                                                                                                              |
| `anthropic-ratelimit-requests-reset`          | Waktu ketika batas laju permintaan terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                                                                            |
| `anthropic-ratelimit-tokens-limit`            | Jumlah maksimum token yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                                                                |
| `anthropic-ratelimit-tokens-remaining`        | Jumlah token yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                                                                   |
| `anthropic-ratelimit-tokens-reset`            | Waktu ketika batas laju token terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                                                                                 |
| `anthropic-ratelimit-input-tokens-limit`      | Jumlah maksimum token input yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                                                          |
| `anthropic-ratelimit-input-tokens-remaining`  | Jumlah token input yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                                                             |
| `anthropic-ratelimit-input-tokens-reset`      | Waktu ketika batas laju token input terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                                                                           |
| `anthropic-ratelimit-output-tokens-limit`     | Jumlah maksimum token output yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                                                         |
| `anthropic-ratelimit-output-tokens-remaining` | Jumlah token output yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                                                            |
| `anthropic-ratelimit-output-tokens-reset`     | Waktu ketika batas laju token output terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                                                                          |
| `anthropic-priority-input-tokens-limit`       | Jumlah maksimum token input Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                                                                                                                                                                                                      |
| `anthropic-priority-input-tokens-remaining`   | Jumlah token input Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)                                                                                                                                                                                                         |
| `anthropic-priority-input-tokens-reset`       | Waktu ketika batas laju token input Priority Tier terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)                                                                                                                                                                                                       |
| `anthropic-priority-output-tokens-limit`      | Jumlah maksimum token output Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                                                                                                                                                                                                     |
| `anthropic-priority-output-tokens-remaining`  | Jumlah token output Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)                                                                                                                                                                                                        |
| `anthropic-priority-output-tokens-reset`      | Waktu ketika batas laju token output Priority Tier terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)                                                                                                                                                                                                      |

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas paling ketat yang sedang berlaku. Misalnya, jika Anda telah melampaui batas token per menit workspace, header berisi nilai batas laju token per menit workspace. Jika batas workspace tidak berlaku, header mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Untuk melihat workspace mana yang diperhitungkan untuk suatu permintaan, baca [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) `anthropic-workspace-id`, yang membawa ID workspace yang menjadi tujuan resolusi kunci API atau token akses Anda.
