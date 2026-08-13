---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: e8c93c40af147aae45a7bf07b68759372e1a8db8c909450ba9eab535c0bc5579
---

---
title: Batas laju
url: https://platform.claude.com/docs/id/api/rate-limits
description: Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan mengenai seberapa banyak sebuah organisasi dapat menggunakan Claude API.
---

<Note>
  **[Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas laju pada halaman ini berlaku untuk Claude Platform di AWS, tetapi penagihan dan pengelolaan batas berbeda. Penagihan dilakukan melalui AWS Marketplace (bukan pembelian kredit Anthropic). Organisasi di Claude Platform di AWS ditempatkan pada tier Start dan tidak berpindah antar tier penggunaan secara otomatis. Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com); alur **Request rate limit increase** tidak tersedia. Konfigurasi batas laju per-workspace dan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) tidak tersedia di Claude Platform di AWS. Untuk detailnya, lihat [Batas laju dan kuota di Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

Ada dua jenis batas:

1. **Spend limits** (batas pengeluaran) menetapkan biaya bulanan maksimum yang dapat dikeluarkan organisasi untuk penggunaan API.
2. **Rate limits** (batas laju) menetapkan jumlah maksimum permintaan API yang dapat dibuat organisasi dalam periode waktu tertentu.

API menerapkan batas yang dikonfigurasi layanan pada tingkat organisasi, tetapi Anda juga dapat menetapkan batas yang dapat dikonfigurasi pengguna untuk workspace organisasi Anda.

## Tentang batas laju

* Batas dirancang untuk mencegah penyalahgunaan API, sambil meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batas ditentukan berdasarkan **usage tier** (tingkat penggunaan). Organisasi ditempatkan pada sebuah tier secara otomatis berdasarkan riwayat penggunaan dan status akun, dan dapat berpindah ke tier yang lebih tinggi seiring waktu saat mereka menggunakan API.
* Organisasi baru dan organisasi dengan riwayat penggunaan terbatas mungkin memulai di tier Evaluation, dengan batas di bawah batas standar yang ditampilkan di halaman ini sementara riwayat akun sedang dibangun. Batas awal ini adalah bagian dari cara Anthropic mencegah penipuan dan penyalahgunaan, dan batas tersebut meningkat secara otomatis seiring organisasi Anda membangun riwayat penggunaan.
* Batas ditetapkan pada tingkat organisasi. Anda dapat melihat tier organisasi Anda dan batas saat ini di halaman [Rate limits](https://platform.claude.com/settings/limits) di [Claude Console](https://platform.claude.com/).
* Anda mungkin mencapai batas laju dalam interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) mungkin diterapkan sebagai 1 permintaan per detik. Lonjakan singkat permintaan dapat melebihi batas dan memicu error batas laju.
* Batas berikut adalah batas standar untuk setiap tier. Jika Anda memerlukan batas yang lebih tinggi, lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus diisi ulang hingga batas maksimum Anda, alih-alih direset pada interval tetap.
* Semua batas yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan minimum yang dijamin. Batas ini dimaksudkan untuk mengurangi pengeluaran berlebih yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

<Note>
  **[Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas pengeluaran bekerja secara berbeda di Claude Platform di AWS. Lihat [Batas pengeluaran di Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits) untuk mengetahui bagaimana batas pengeluaran dan batas pengeluaran yang ditetapkan sendiri berlaku untuk organisasi Anda.
</Note>

Masing-masing tier Start, Build, dan Scale memiliki batas pengeluaran bulanan, yaitu jumlah maksimum yang dapat dibelanjakan organisasi Anda pada API setiap bulan kalender. Setelah Anda mencapai batas pengeluaran tier Anda, penggunaan API dijeda hingga bulan berikutnya kecuali Anda meminta batas yang lebih tinggi. Anda dapat melihat batas pengeluaran bulanan organisasi Anda dan menetapkan batas Anda sendiri di halaman [Billing](https://platform.claude.com/settings/billing).

| Tier penggunaan | Batas pengeluaran bulanan |
| --------------- | ------------------------- |
| Start           | $500 USD                  |
| Build           | $1.000 USD                |
| Scale           | $200.000 USD              |

Organisasi pada tier Custom tidak memiliki batas pengeluaran bulanan; batas diatur bersama tim akun mereka.

Anda juga dapat menetapkan batas pengeluaran Anda sendiri di bawah batas tier Anda untuk mengontrol biaya:

<Steps>
  <Step title="Buka halaman Billing">
    Buka [Settings > Billing](https://platform.claude.com/settings/billing) di Claude Console.
  </Step>

  <Step title="Buka editor batas pengeluaran">
    Di bagian **Spend limits**, klik **Adjust limit** (atau **Set limit** jika belum ada batas yang ditetapkan).
  </Step>

  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas pengeluaran Anda tidak boleh melebihi batas tier Anda saat ini.
  </Step>
</Steps>

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model. Jika Anda melebihi salah satu batas laju, Anda akan mendapatkan [error 429](https://platform.claude.com/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui, beserta header `retry-after` yang menunjukkan berapa lama harus menunggu.

<Note>
  Anda mungkin juga mengalami error 429 karena batas akselerasi pada API jika organisasi Anda mengalami peningkatan penggunaan yang tajam. Untuk menghindari mencapai batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
</Note>

### ITPM yang memperhitungkan cache

Banyak penyedia API menggunakan batas gabungan "tokens per minute" (TPM) yang mungkin mencakup semua token, baik yang di-cache maupun tidak, input maupun output. **Untuk sebagian besar model Claude, hanya token input yang tidak di-cache yang dihitung terhadap batas laju ITPM Anda.** Ini adalah keunggulan utama yang membuat batas laju secara efektif lebih tinggi daripada yang mungkin terlihat pada awalnya.

Batas laju ITPM diestimasi pada awal setiap permintaan, dan estimasi tersebut disesuaikan selama permintaan untuk mencerminkan jumlah token input aktual yang digunakan.

Berikut yang dihitung terhadap ITPM:

* `input_tokens` (token setelah breakpoint cache terakhir) ✓ **Dihitung terhadap ITPM**
* `cache_creation_input_tokens` (token yang sedang ditulis ke cache) ✓ **Dihitung terhadap ITPM**
* `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung terhadap ITPM** untuk sebagian besar model

<Note>
  Field `input_tokens` hanya mewakili token yang muncul **setelah breakpoint cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

  ```text wrap
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen 200k token yang di-cache dan pertanyaan pengguna 50 token, Anda akan melihat `input_tokens: 50` meskipun total input adalah 200.050 token.

  Untuk tujuan batas laju pada sebagian besar model, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung terhadap batas ITPM Anda, menjadikan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) cara yang efektif untuk meningkatkan throughput efektif Anda.
</Note>

**Contoh:** Dengan batas ITPM 2.000.000 dan tingkat cache hit 80%, Anda dapat secara efektif memproses 10.000.000 total token input per menit (2 juta tidak di-cache + 8 juta di-cache), karena token yang di-cache tidak dihitung terhadap batas laju Anda.

<Note>
  Claude Haiku 3.5 (ditandai dengan † dalam tabel batas laju berikut) juga menghitung `cache_read_input_tokens` terhadap batas laju ITPM.

  Untuk semua model tanpa penanda †, token input yang di-cache tidak dihitung terhadap batas laju dan ditagih dengan tarif yang lebih rendah (10% dari harga token input dasar). Ini berarti Anda dapat mencapai throughput efektif yang jauh lebih tinggi dengan menggunakan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).
</Note>

<Tip>
  **Maksimalkan batas laju Anda dengan caching prompt**

  Lihat [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk panduan tentang meningkatkan throughput efektif dengan melakukan caching pada konten yang berulang seperti:

  * Instruksi dan prompt sistem
  * Dokumen konteks yang besar
  * Definisi alat
  * Riwayat percakapan

  Dengan caching yang efektif, Anda dapat secara dramatis meningkatkan throughput aktual Anda tanpa meningkatkan batas laju Anda. Pantau tingkat cache hit Anda di [halaman Usage](https://platform.claude.com/usage) untuk mengoptimalkan strategi caching Anda.
</Tip>

Batas laju OTPM dievaluasi secara real-time saat token output dihasilkan, hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak diperhitungkan dalam perhitungan batas laju OTPM, sehingga tidak ada kerugian batas laju dalam menetapkan nilai `max_tokens` yang lebih tinggi.

Batas laju diterapkan secara terpisah untuk setiap model; oleh karena itu Anda dapat menggunakan model yang berbeda hingga batas masing-masing secara bersamaan. Anda dapat memeriksa batas laju dan perilaku Anda saat ini di halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console, atau membaca batas yang dikonfigurasi secara terprogram dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

<Note>
  Batas laju saat ini dibagi di semua nilai `inference_geo`. Permintaan dengan `inference_geo: "us"` dan `inference_geo: "global"` mengambil dari pool batas laju yang sama.
</Note>

<Tabs>
  <Tab title="Tier Start">
    | Model                                                                                                                                     | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                                            | 1.000                               | 500.000                               | 100.000                                |
    | Claude Opus 5                                                                                                                             | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Opus 4.x\*                                                                                                                         | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 5                                                                                                                           | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 4.x\*\*                                                                                                                     | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 4.5                                                                                                                          | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 1.000                               | 100.000†                              | 20.000                                 |
  </Tab>

  <Tab title="Tier Build">
    | Model                                                                                                                                     | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                                            | 2.000                               | 1.500.000                             | 300.000                                |
    | Claude Opus 5                                                                                                                             | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Opus 4.x\*                                                                                                                         | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 5                                                                                                                           | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 4.x\*\*                                                                                                                     | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 4.5                                                                                                                          | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 2.000                               | 200.000†                              | 40.000                                 |
  </Tab>

  <Tab title="Tier Scale">
    | Model                                                                                                                                     | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                                            | 4.000                               | 4.000.000                             | 800.000                                |
    | Claude Opus 5                                                                                                                             | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Opus 4.x\*                                                                                                                         | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 5                                                                                                                           | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 4.x\*\*                                                                                                                     | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 4.5                                                                                                                          | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 4.000                               | 400.000†                              | 80.000                                 |
  </Tab>

  <Tab title="Tier Custom">
    Jika Anda memerlukan batas yang lebih tinggi dari tier Scale, hubungi tim penjualan melalui halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console.
  </Tab>
</Tabs>

*\* Batas laju Opus adalah batas total yang berlaku untuk lalu lintas gabungan di Claude Opus 4.8, Opus 4.7, Opus 4.6, dan Opus 4.5. Claude Opus 5 memiliki batas laju terpisah dan bukan bagian dari bucket gabungan ini.*

*\*\* Batas laju Sonnet 4.x adalah batas total yang berlaku untuk lalu lintas gabungan di Sonnet 4.6 dan Sonnet 4.5. Claude Sonnet 5 memiliki batas laju terpisah dan bukan bagian dari bucket gabungan ini.*

*† Batas menghitung `cache_read_input_tokens` terhadap penggunaan ITPM.*

### Message Batches API

Message Batches API memiliki serangkaian batas laju sendiri yang dibagi di semua model. Ini termasuk batas permintaan per menit (RPM) untuk semua endpoint API dan batas jumlah permintaan batch yang dapat berada dalam antrean pemrosesan pada saat yang sama. "Permintaan batch" di sini mengacu pada bagian dari Message Batch. Anda dapat membuat Message Batch yang berisi ribuan permintaan batch, yang masing-masing dihitung terhadap batas ini. Permintaan batch dianggap sebagai bagian dari antrean pemrosesan ketika belum berhasil diproses oleh model.

<Tabs>
  <Tab title="Tier Start">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 1.000                               | 200.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tier Build">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 2.000                               | 300.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tier Scale">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 4.000                               | 500.000                                            | 100.000                             |
  </Tab>

  <Tab title="Tier Custom">
    Jika Anda memerlukan batas yang lebih tinggi dari tier Scale, hubungi tim penjualan melalui halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console.
  </Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dibatasi lajunya per organisasi. Batas ini terpisah dari batas laju Messages API di atas.

| Operasi                                                           | Batas                      |
| ----------------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (misalnya, agents, sessions, dan environments) | 300 permintaan per menit   |
| Endpoint pembacaan (misalnya, retrieve, list, dan stream)         | 1.200 permintaan per menit |

### Batas laju fast mode

Saat menggunakan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) dengan `speed: "fast"` pada Claude Opus 5 atau Opus 4.8, batas laju khusus berlaku yang terpisah dari batas laju Opus standar. Ketika batas laju fast mode terlampaui, API mengembalikan error `429` dengan header `retry-after`. Fast mode tidak tersedia pada Claude Opus 4.7 (permintaan mengembalikan error) atau Claude Opus 4.6 (permintaan ke `claude-opus-4-6` dengan `speed: "fast"` berjalan pada kecepatan standar). Lihat [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

Respons menyertakan header `anthropic-fast-*` yang menunjukkan status batas laju fast mode Anda. Lihat [Batas laju fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Usage](https://platform.claude.com/usage) di [Claude Console](https://platform.claude.com/).

Selain menyediakan grafik token dan permintaan, halaman Usage menyediakan dua grafik batas laju terpisah. Gunakan grafik ini untuk melihat ruang yang Anda miliki untuk berkembang, mengidentifikasi kapan Anda mungkin mencapai penggunaan puncak, memahami batas laju apa yang perlu diminta, dan mempelajari cara meningkatkan tingkat caching Anda. Grafik memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya, per model):

* Grafik **Rate Limit - Input Tokens** mencakup:

  * Token input maksimum per menit yang tidak di-cache per jam
  * Batas laju token input per menit Anda saat ini
  * Tingkat cache untuk token input Anda (yaitu, persentase token input yang dibaca dari cache)

* Grafik **Rate Limit - Output Tokens** mencakup:

  * Token output maksimum per menit per jam
  * Batas laju token output per menit Anda saat ini

## Meminta batas yang lebih tinggi

Untuk meminta batas laju yang lebih tinggi atau batas pengeluaran bulanan yang lebih tinggi, gunakan **Request rate limit increase** di halaman [Rate limits](https://platform.claude.com/settings/limits).

<Note>
  Tim dukungan juga dapat menaikkan batas. Untuk kebutuhan mendesak, hubungi [dukungan Anthropic](https://support.claude.com).
</Note>

<Note>
  **[Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Alur **Request rate limit increase** tidak tersedia. Hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com), dan sertakan model yang perlu dinaikkan, token input dan output puncak per menit Anda untuk setiap model, dan kira-kira berapa bagian dari input Anda yang merupakan konteks yang di-cache atau berulang. Lihat [Batas laju dan kuota di Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

## Menetapkan batas yang lebih rendah untuk Workspace

Untuk informasi lebih lanjut tentang workspace, lihat [Workspaces](https://platform.claude.com/docs/id/manage-claude/workspaces).

Untuk melindungi Workspace di Organisasi Anda dari potensi penggunaan berlebih, Anda dapat menetapkan batas pengeluaran dan batas laju kustom per Workspace.

Contoh: Jika batas Organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda mungkin membatasi satu Workspace menjadi 30.000 token input per menit. Ini melindungi Workspace lain dari potensi penggunaan berlebih dan memastikan distribusi sumber daya yang lebih adil di seluruh Organisasi Anda. Token per menit yang tersisa dan tidak terpakai (atau lebih, jika Workspace tersebut tidak menggunakan batasnya) kemudian tersedia untuk digunakan oleh Workspace lain.

Catatan:

* Anda tidak dapat menetapkan batas pada Workspace default.
* Jika tidak ditetapkan, batas Workspace mengikuti batas Organisasi.
* Batas Workspace ditetapkan per jenis pembatas (seperti permintaan per menit, token input per menit, atau token output per menit).
* Batas tingkat Organisasi selalu berlaku, bahkan jika jumlah batas Workspace melebihinya.

Untuk membaca batas laju organisasi dan workspace Anda saat ini secara terprogram, gunakan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Header respons

Respons API menyertakan header yang menunjukkan batas laju yang diterapkan, penggunaan saat ini, dan kapan batas akan direset.

Header berikut dikembalikan:

| Header                                        | Deskripsi                                                                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `retry-after`                                 | Jumlah detik yang harus ditunggu hingga Anda dapat mencoba kembali permintaan. Percobaan ulang yang lebih awal akan gagal.            |
| `anthropic-ratelimit-requests-limit`          | Jumlah maksimum permintaan yang diizinkan dalam periode batas laju apa pun.                                                           |
| `anthropic-ratelimit-requests-remaining`      | Jumlah permintaan yang tersisa sebelum dibatasi lajunya.                                                                              |
| `anthropic-ratelimit-requests-reset`          | Waktu ketika batas laju permintaan akan terisi penuh kembali, disediakan dalam format RFC 3339.                                       |
| `anthropic-ratelimit-tokens-limit`            | Jumlah maksimum token yang diizinkan dalam periode batas laju apa pun.                                                                |
| `anthropic-ratelimit-tokens-remaining`        | Jumlah token yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                   |
| `anthropic-ratelimit-tokens-reset`            | Waktu ketika batas laju token akan terisi penuh kembali, disediakan dalam format RFC 3339.                                            |
| `anthropic-ratelimit-input-tokens-limit`      | Jumlah maksimum token input yang diizinkan dalam periode batas laju apa pun.                                                          |
| `anthropic-ratelimit-input-tokens-remaining`  | Jumlah token input yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                             |
| `anthropic-ratelimit-input-tokens-reset`      | Waktu ketika batas laju token input akan terisi penuh kembali, disediakan dalam format RFC 3339.                                      |
| `anthropic-ratelimit-output-tokens-limit`     | Jumlah maksimum token output yang diizinkan dalam periode batas laju apa pun.                                                         |
| `anthropic-ratelimit-output-tokens-remaining` | Jumlah token output yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                            |
| `anthropic-ratelimit-output-tokens-reset`     | Waktu ketika batas laju token output akan terisi penuh kembali, disediakan dalam format RFC 3339.                                     |
| `anthropic-priority-input-tokens-limit`       | Jumlah maksimum token input Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                      |
| `anthropic-priority-input-tokens-remaining`   | Jumlah token input Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)         |
| `anthropic-priority-input-tokens-reset`       | Waktu ketika batas laju token input Priority Tier akan terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)  |
| `anthropic-priority-output-tokens-limit`      | Jumlah maksimum token output Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                     |
| `anthropic-priority-output-tokens-remaining`  | Jumlah token output Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)        |
| `anthropic-priority-output-tokens-reset`      | Waktu ketika batas laju token output Priority Tier akan terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier) |

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas paling ketat yang saat ini berlaku. Misalnya, jika Anda telah melebihi batas token per menit Workspace, header akan berisi nilai batas laju token per menit Workspace. Jika batas Workspace tidak berlaku, header akan mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Pendekatan ini memastikan bahwa Anda memiliki visibilitas terhadap batasan yang paling relevan pada penggunaan API Anda saat ini.
