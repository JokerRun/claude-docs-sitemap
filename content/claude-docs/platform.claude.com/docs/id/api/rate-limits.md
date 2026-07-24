---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 0cbb6bac161b47595a0b76f17b6d030f726b596470979736d6af94c15bc1dd6c
---

# Batas laju

Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan pada seberapa banyak sebuah organisasi dapat menggunakan Claude API.

---

<Note>
  **[Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws):** "Rate limit" (batas laju) pada halaman ini berlaku untuk Claude Platform on AWS, tetapi penagihan dan pengelolaan batas berbeda. Penagihan dilakukan melalui AWS Marketplace (bukan pembelian kredit Anthropic). Organisasi di Claude Platform on AWS ditempatkan pada tier Start dan tidak berpindah antar tier penggunaan secara otomatis. Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com); alur **Request rate limit increase** tidak tersedia. Batas pengeluaran diatur di [Settings > Billing](/settings/billing) alih-alih **Settings > Limits**. Konfigurasi batas laju per-workspace dan [fast mode](/docs/id/build-with-claude/fast-mode) tidak tersedia di Claude Platform on AWS. Untuk detailnya, lihat [Batas laju dan kuota di Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

Ada dua jenis batasan:

1. **Batas pengeluaran** menetapkan biaya bulanan maksimum yang dapat dikeluarkan sebuah organisasi untuk penggunaan API.
2. **Batas laju** menetapkan jumlah maksimum permintaan API yang dapat dibuat sebuah organisasi selama periode waktu yang ditentukan.

API memberlakukan batasan yang dikonfigurasi oleh layanan di tingkat organisasi, tetapi Anda juga dapat menetapkan batasan yang dapat dikonfigurasi pengguna untuk workspace organisasi Anda.

## Tentang batas laju

* Batasan dirancang untuk mencegah penyalahgunaan API, sambil meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batasan ditentukan oleh **tier penggunaan**. Organisasi ditempatkan pada sebuah tier secara otomatis berdasarkan riwayat penggunaan dan status akun, dan dapat berpindah ke tier yang lebih tinggi seiring waktu saat mereka menggunakan API.
* Organisasi baru dan organisasi dengan riwayat penggunaan terbatas mungkin memulai dengan batasan di bawah batasan standar yang ditampilkan pada halaman ini sementara riwayat akun dibangun. Batasan awal ini adalah bagian dari cara kami mencegah penipuan dan penyalahgunaan, dan batasan tersebut meningkat secara otomatis seiring organisasi Anda membangun riwayat penggunaan.
* Batasan ditetapkan di tingkat organisasi. Anda dapat melihat tier dan batasan saat ini organisasi Anda di halaman [Limits](/settings/limits) di [Claude Console](/).
* Anda mungkin mencapai batas laju dalam interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) mungkin diberlakukan sebagai 1 permintaan per detik. Lonjakan permintaan singkat dapat melebihi batas dan memicu kesalahan batas laju.
* Batasan berikut adalah batasan standar untuk setiap tier. Jika Anda memerlukan batasan yang lebih tinggi, lihat [Meminta batasan yang lebih tinggi](#requesting-higher-limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus diisi ulang hingga batas maksimum Anda, alih-alih direset pada interval tetap.
* Semua batasan yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan jaminan minimum. Batasan ini dimaksudkan untuk mengurangi pengeluaran berlebih yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

<Note>
  **[Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws):** Batas pengeluaran bekerja secara berbeda di Claude Platform on AWS. Atur batas pengeluaran di [Settings > Billing](/settings/billing) alih-alih **Settings > Limits**. Lihat [Batas pengeluaran di Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws#spend-limits) untuk mengetahui bagaimana batas atas pengeluaran dan batas pengeluaran yang ditetapkan sendiri berlaku untuk organisasi Anda.
</Note>

Masing-masing tier Start, Build, dan Scale memiliki batas atas pengeluaran bulanan, yaitu jumlah maksimum yang dapat dibelanjakan organisasi Anda pada API setiap bulan kalender. Setelah Anda mencapai batas atas pengeluaran tier Anda, penggunaan API dijeda hingga bulan berikutnya kecuali Anda meminta batas yang lebih tinggi. Anda dapat melihat batas atas pengeluaran bulanan organisasi Anda di halaman [Limits](/settings/limits).

| Tier penggunaan | Batas atas pengeluaran bulanan |
| --------------- | ------------------------------ |
| Start           | $500 USD                       |
| Build           | $1,000 USD                     |
| Scale           | $200,000 USD                   |

Organisasi pada tier Custom tidak memiliki batas atas pengeluaran bulanan; batasan diatur bersama tim akun mereka.

Anda juga dapat menetapkan batas pengeluaran Anda sendiri di bawah batas atas tier Anda untuk mengendalikan biaya:

<Steps>
  <Step title="Buka halaman Limits">
    Buka [Settings > Limits](/settings/limits) di Claude Console.
  </Step>

  <Step title="Buka editor batas pengeluaran">
    Di bagian **Spend limits**, klik **Change Limit** (atau **Set spend limit** jika belum ada batas yang ditetapkan).
  </Step>

  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas pengeluaran Anda tidak dapat melebihi batas atas tier Anda saat ini.
  </Step>
</Steps>

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model. Jika Anda melebihi salah satu batas laju, Anda akan mendapatkan [kesalahan 429](/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui, bersama dengan header `retry-after` yang menunjukkan berapa lama harus menunggu.

<Note>
  Anda juga mungkin mengalami kesalahan 429 karena batas akselerasi pada API jika organisasi Anda mengalami peningkatan penggunaan yang tajam. Untuk menghindari mencapai batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
</Note>

### ITPM yang sadar cache

Banyak penyedia API menggunakan batas gabungan "token per menit" (TPM) yang mungkin mencakup semua token, baik yang di-cache maupun tidak, input dan output. **Untuk sebagian besar model Claude, hanya token input yang tidak di-cache yang dihitung terhadap batas laju ITPM Anda.** Ini adalah keunggulan utama yang membuat batas laju secara efektif lebih tinggi daripada yang mungkin terlihat pada awalnya.

Batas laju ITPM diestimasi pada awal setiap permintaan, dan estimasi tersebut disesuaikan selama permintaan untuk mencerminkan jumlah token input aktual yang digunakan.

Berikut adalah yang dihitung terhadap ITPM:

* `input_tokens` (token setelah breakpoint cache terakhir) ✓ **Dihitung terhadap ITPM**
* `cache_creation_input_tokens` (token yang sedang ditulis ke cache) ✓ **Dihitung terhadap ITPM**
* `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung terhadap ITPM** untuk sebagian besar model

<Note>
  Field `input_tokens` hanya mewakili token yang muncul **setelah breakpoint cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

  ```text wrap
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen yang di-cache sebesar 200k token dan pertanyaan pengguna sebesar 50 token, Anda akan melihat `input_tokens: 50` meskipun total inputnya adalah 200.050 token.

  Untuk tujuan batas laju pada sebagian besar model, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung terhadap batas ITPM Anda, menjadikan [caching prompt](/docs/id/build-with-claude/prompt-caching) cara yang efektif untuk meningkatkan throughput efektif Anda.
</Note>

**Contoh:** Dengan batas ITPM 2.000.000 dan tingkat cache hit 80%, Anda dapat secara efektif memproses 10.000.000 total token input per menit (2 juta tidak di-cache + 8 juta di-cache), karena token yang di-cache tidak dihitung terhadap batas laju Anda.

<Note>
  Claude Haiku 3.5 (ditandai dengan † pada tabel batas laju berikut) juga menghitung `cache_read_input_tokens` terhadap batas laju ITPM.

  Untuk semua model tanpa penanda †, token input yang di-cache tidak dihitung terhadap batas laju dan ditagih dengan tarif yang lebih rendah (10% dari harga token input dasar). Ini berarti Anda dapat mencapai throughput efektif yang jauh lebih tinggi dengan menggunakan [caching prompt](/docs/id/build-with-claude/prompt-caching).
</Note>

<Tip>
  **Maksimalkan batas laju Anda dengan caching prompt**

  Lihat [caching prompt](/docs/id/build-with-claude/prompt-caching) untuk panduan tentang meningkatkan throughput efektif dengan melakukan caching pada konten yang berulang seperti:

  * Instruksi sistem dan prompt
  * Dokumen konteks yang besar
  * Definisi alat
  * Riwayat percakapan

  Dengan caching yang efektif, Anda dapat meningkatkan throughput aktual Anda secara dramatis tanpa meningkatkan batas laju Anda. Pantau tingkat cache hit Anda di [halaman Usage](/usage) untuk mengoptimalkan strategi caching Anda.
</Tip>

Batas laju OTPM dievaluasi secara real time saat token output dihasilkan, hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak diperhitungkan dalam perhitungan batas laju OTPM, sehingga tidak ada kerugian batas laju dalam menetapkan nilai `max_tokens` yang lebih tinggi.

Batas laju diterapkan secara terpisah untuk setiap model; oleh karena itu Anda dapat menggunakan model yang berbeda hingga batas masing-masing secara bersamaan. Anda dapat memeriksa batas laju dan perilaku Anda saat ini di halaman [Limits](/settings/limits) di Claude Console, atau membaca batasan yang dikonfigurasi secara terprogram dengan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

<Note>
  Batas laju saat ini dibagikan di semua nilai `inference_geo`. Permintaan dengan `inference_geo: "us"` dan `inference_geo: "global"` mengambil dari pool batas laju yang sama.
</Note>

<Tabs>
  <Tab title="Tier Start">
    | Model                                                                                                            | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                   | 1,000                               | 500,000                               | 100,000                                |
    | Claude Opus 4.x\*                                                                                                | 1,000                               | 2,000,000                             | 400,000                                |
    | Claude Sonnet 5                                                                                                  | 1,000                               | 2,000,000                             | 400,000                                |
    | Claude Sonnet 4.x\*\*                                                                                            | 1,000                               | 2,000,000                             | 400,000                                |
    | Claude Haiku 4.5                                                                                                 | 1,000                               | 2,000,000                             | 400,000                                |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | 1,000                               | 100,000†                              | 20,000                                 |
  </Tab>

  <Tab title="Tier Build">
    | Model                                                                                                            | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                   | 2,000                               | 1,500,000                             | 300,000                                |
    | Claude Opus 4.x\*                                                                                                | 5,000                               | 5,000,000                             | 1,000,000                              |
    | Claude Sonnet 5                                                                                                  | 5,000                               | 5,000,000                             | 1,000,000                              |
    | Claude Sonnet 4.x\*\*                                                                                            | 5,000                               | 5,000,000                             | 1,000,000                              |
    | Claude Haiku 4.5                                                                                                 | 5,000                               | 5,000,000                             | 1,000,000                              |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | 2,000                               | 200,000†                              | 40,000                                 |
  </Tab>

  <Tab title="Tier Scale">
    | Model                                                                                                            | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5                                                                                                   | 4,000                               | 4,000,000                             | 800,000                                |
    | Claude Opus 4.x\*                                                                                                | 10,000                              | 10,000,000                            | 2,000,000                              |
    | Claude Sonnet 5                                                                                                  | 10,000                              | 10,000,000                            | 2,000,000                              |
    | Claude Sonnet 4.x\*\*                                                                                            | 10,000                              | 10,000,000                            | 2,000,000                              |
    | Claude Haiku 4.5                                                                                                 | 10,000                              | 10,000,000                            | 2,000,000                              |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | 4,000                               | 400,000†                              | 80,000                                 |
  </Tab>

  <Tab title="Tier Custom">
    Jika Anda memerlukan batasan yang lebih tinggi dari tier Scale, hubungi tim penjualan melalui halaman [Limits](/settings/limits) di Claude Console.
  </Tab>
</Tabs>

*\* - Batas laju Opus adalah batas total yang berlaku untuk gabungan lalu lintas di Claude Opus 4.8, Opus 4.7, Opus 4.6, dan Opus 4.5.*

*\*\* - Batas laju Sonnet 4.x adalah batas total yang berlaku untuk gabungan lalu lintas di Sonnet 4.6 dan Sonnet 4.5. Claude Sonnet 5 memiliki batas laju terpisah dan bukan bagian dari bucket gabungan ini.*

*† - Batas menghitung `cache_read_input_tokens` terhadap penggunaan ITPM.*

### Message Batches API

Message Batches API memiliki serangkaian batas laju tersendiri yang dibagikan di semua model. Ini mencakup batas permintaan per menit (RPM) untuk semua endpoint API dan batas jumlah permintaan batch yang dapat berada dalam antrean pemrosesan pada saat yang sama. "Permintaan batch" di sini mengacu pada bagian dari sebuah Message Batch. Anda dapat membuat Message Batch yang berisi ribuan permintaan batch, yang masing-masing dihitung terhadap batas ini. Sebuah permintaan batch dianggap sebagai bagian dari antrean pemrosesan ketika belum berhasil diproses oleh model.

<Tabs>
  <Tab title="Tier Start">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 1,000                               | 200,000                                            | 100,000                             |
  </Tab>

  <Tab title="Tier Build">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 2,000                               | 300,000                                            | 100,000                             |
  </Tab>

  <Tab title="Tier Scale">
    | Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrean pemrosesan | Permintaan batch maksimum per batch |
    | ----------------------------------- | -------------------------------------------------- | ----------------------------------- |
    | 4,000                               | 500,000                                            | 100,000                             |
  </Tab>

  <Tab title="Tier Custom">
    Jika Anda memerlukan batasan yang lebih tinggi dari tier Scale, hubungi tim penjualan melalui halaman [Limits](/settings/limits) di Claude Console.
  </Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](/docs/id/managed-agents/overview) dibatasi lajunya per organisasi. Batasan ini terpisah dari batas laju Messages API di atas.

| Operasi                                                   | Batas                      |
| --------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (misalnya, agen, sesi, dan lingkungan) | 300 permintaan per menit   |
| Endpoint pembacaan (misalnya, retrieve, list, dan stream) | 1.200 permintaan per menit |

### Batas laju fast mode

Saat menggunakan [fast mode](/docs/id/build-with-claude/fast-mode) (pratinjau riset) dengan `speed: "fast"` pada Claude Opus 4.8 atau Opus 4.7, batas laju khusus berlaku yang terpisah dari batas laju Opus standar. Ketika batas laju fast mode terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after`. Fast mode tidak tersedia di Claude Opus 4.6: permintaan ke `claude-opus-4-6` dengan `speed: "fast"` berjalan pada kecepatan standar. Lihat [Fast mode](/docs/id/build-with-claude/fast-mode#supported-models).

Respons menyertakan header `anthropic-fast-*` yang menunjukkan status batas laju fast mode Anda. Lihat [Batas laju fast mode](/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Usage](/usage) di [Claude Console](/).

Selain menyediakan grafik token dan permintaan, halaman Usage menyediakan dua grafik batas laju terpisah. Gunakan grafik ini untuk melihat ruang yang Anda miliki untuk bertumbuh, mengidentifikasi kapan Anda mungkin mencapai penggunaan puncak, memahami batas laju apa yang perlu diminta, dan mempelajari cara meningkatkan tingkat caching Anda. Grafik tersebut memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya, per model):

* Grafik **Rate Limit - Input Tokens** mencakup:

  * Token input tidak di-cache maksimum per jam per menit
  * Batas laju token input per menit Anda saat ini
  * Tingkat cache untuk token input Anda (yaitu, persentase token input yang dibaca dari cache)

* Grafik **Rate Limit - Output Tokens** mencakup:

  * Token output maksimum per jam per menit
  * Batas laju token output per menit Anda saat ini

## Meminta batasan yang lebih tinggi

Untuk meminta batas laju yang lebih tinggi atau batas atas pengeluaran bulanan yang lebih tinggi, gunakan **Request rate limit increase** di halaman [Limits](/settings/limits).

<Note>
  Tim dukungan juga dapat menaikkan batasan. Untuk kebutuhan mendesak, hubungi [dukungan Anthropic](https://support.claude.com).
</Note>

<Note>
  **[Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws):** Alur **Request rate limit increase** tidak tersedia. Hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com), dan sertakan model yang perlu Anda naikkan, token input dan output puncak Anda per menit untuk setiap model, dan perkiraan berapa bagian dari input Anda yang merupakan konteks yang di-cache atau berulang. Lihat [Batas laju dan kuota di Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

## Menetapkan batasan yang lebih rendah untuk Workspace

Untuk informasi lebih lanjut tentang workspace, lihat [Workspaces](/docs/id/manage-claude/workspaces).

Untuk melindungi Workspace di Organisasi Anda dari potensi penggunaan berlebih, Anda dapat menetapkan batas pengeluaran dan batas laju kustom per Workspace.

Contoh: Jika batas Organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda dapat membatasi satu Workspace menjadi 30.000 token input per menit. Ini melindungi Workspace lain dari potensi penggunaan berlebih dan memastikan distribusi sumber daya yang lebih adil di seluruh Organisasi Anda. Sisa token per menit yang tidak digunakan (atau lebih, jika Workspace tersebut tidak menggunakan batasnya) kemudian tersedia untuk digunakan oleh Workspace lain.

Catatan:

* Anda tidak dapat menetapkan batasan pada Workspace default.
* Jika tidak ditetapkan, batasan Workspace sama dengan batasan Organisasi.
* Batasan Workspace ditetapkan per jenis pembatas (seperti permintaan per menit, token input per menit, atau token output per menit).
* Batasan di seluruh Organisasi selalu berlaku, bahkan jika jumlah batasan Workspace melebihinya.

Untuk membaca batas laju organisasi dan workspace Anda saat ini secara terprogram, gunakan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

## Header respons

Respons API menyertakan header yang menunjukkan batas laju yang diberlakukan, penggunaan saat ini, dan kapan batas akan direset.

Header berikut dikembalikan:

| Header                                        | Deskripsi                                                                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `retry-after`                                 | Jumlah detik yang harus ditunggu sebelum Anda dapat mencoba kembali permintaan. Percobaan ulang yang lebih awal akan gagal.           |
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

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas paling ketat yang saat ini berlaku. Misalnya, jika Anda telah melampaui batas token per menit Workspace, header akan berisi nilai batas laju token per menit Workspace. Jika batasan Workspace tidak berlaku, header akan mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Pendekatan ini memastikan bahwa Anda memiliki visibilitas terhadap kendala yang paling relevan pada penggunaan API Anda saat ini.
