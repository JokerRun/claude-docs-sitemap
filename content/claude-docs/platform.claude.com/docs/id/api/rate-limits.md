---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 860a59165177a6cfc4b0145d46a0d2035aacdc2f211d45c9c5f92f76e8c14449
---

# Batas laju

Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan pada seberapa banyak sebuah organisasi dapat menggunakan Claude API.

---

<Note>
  **[Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws):** Batas laju pada halaman ini berlaku untuk Claude Platform di AWS. Penagihan dan batas pengeluaran berbeda: batas pengeluaran tidak tersedia, dan penagihan dilakukan melalui AWS Marketplace (bukan pembelian kredit Anthropic). Organisasi di Claude Platform di AWS ditempatkan pada tier Start dan tidak berpindah antar tier penggunaan secara otomatis. Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda. Konfigurasi batas laju per-workspace dan [fast mode](/docs/id/build-with-claude/fast-mode) tidak tersedia di Claude Platform di AWS.
</Note>

Ada dua jenis batasan:

1. **Batas pengeluaran** menetapkan biaya bulanan maksimum yang dapat ditanggung sebuah organisasi untuk penggunaan API.
2. **Batas laju** (rate limit) menetapkan jumlah maksimum permintaan API yang dapat dibuat sebuah organisasi selama periode waktu yang ditentukan.

API memberlakukan batasan yang dikonfigurasi oleh layanan di tingkat organisasi, tetapi Anda juga dapat menetapkan batasan yang dapat dikonfigurasi pengguna untuk workspace organisasi Anda.

## Tentang batas laju

* Batasan dirancang untuk mencegah penyalahgunaan API, sambil meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batasan ditentukan oleh **tier penggunaan**. Organisasi Anda ditempatkan pada sebuah tier secara otomatis dan dapat berpindah ke tier yang lebih tinggi seiring waktu saat Anda menggunakan API.
* Batasan ditetapkan di tingkat organisasi. Anda dapat melihat tier organisasi Anda dan batasan saat ini di halaman [Limits](/settings/limits) di [Claude Console](/).
* Anda mungkin mencapai batas laju dalam interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) mungkin diberlakukan sebagai 1 permintaan per detik. Lonjakan permintaan singkat dapat melebihi batas dan memicu kesalahan batas laju.
* Batasan berikut adalah batasan standar untuk setiap tier. Jika Anda memerlukan batasan yang lebih tinggi, lihat [Meminta batas yang lebih tinggi](#requesting-higher-limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus diisi ulang hingga batas maksimum Anda, bukan direset pada interval tetap.
* Semua batasan yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan jaminan minimum. Batasan ini dimaksudkan untuk mengurangi pengeluaran berlebih yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

Masing-masing tier Start, Build, dan Scale memiliki batas pengeluaran bulanan, yaitu jumlah maksimum yang dapat dibelanjakan organisasi Anda pada API setiap bulan kalender. Setelah Anda mencapai batas pengeluaran tier Anda, penggunaan API dijeda hingga bulan berikutnya kecuali Anda meminta batas yang lebih tinggi. Anda dapat melihat batas pengeluaran bulanan organisasi Anda di halaman [Limits](/settings/limits).

| Tier penggunaan | Batas pengeluaran bulanan |
| --------------- | ------------------------- |
| Start           | $500                      |
| Build           | $1,000                    |
| Scale           | $200,000                  |

Organisasi pada tier Custom tidak memiliki batas pengeluaran bulanan; batasan diatur bersama tim akun mereka.

Anda juga dapat menetapkan batas pengeluaran Anda sendiri di bawah batas tier Anda untuk mengendalikan biaya:

<Steps>
  <Step title="Buka halaman Limits">
    Buka [Settings > Limits](/settings/limits) di Claude Console.
  </Step>

  <Step title="Buka editor batas pengeluaran">
    Di bagian **Spend limits**, klik **Change Limit** (atau **Set spend limit** jika belum ada batas yang ditetapkan).
  </Step>

  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas pengeluaran Anda tidak dapat melebihi batas tier Anda saat ini.
  </Step>
</Steps>

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model. Jika Anda melebihi salah satu batas laju, Anda akan mendapatkan [kesalahan 429](/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui, bersama dengan header `retry-after` yang menunjukkan berapa lama harus menunggu.

<Note>
  Anda juga mungkin mengalami kesalahan 429 karena batas akselerasi pada API jika organisasi Anda mengalami peningkatan penggunaan yang tajam. Untuk menghindari batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
</Note>

### ITPM yang sadar cache

Banyak penyedia API menggunakan batas gabungan "token per menit" (TPM) yang dapat mencakup semua token, baik yang di-cache maupun tidak, input dan output. **Untuk sebagian besar model Claude, hanya token input yang tidak di-cache yang dihitung terhadap batas laju ITPM Anda.** Ini adalah keunggulan utama yang membuat batas laju secara efektif lebih tinggi daripada yang mungkin terlihat pada awalnya.

Batas laju ITPM diperkirakan pada awal setiap permintaan, dan perkiraan tersebut disesuaikan selama permintaan untuk mencerminkan jumlah token input aktual yang digunakan.

Berikut adalah yang dihitung terhadap ITPM:

* `input_tokens` (token setelah breakpoint cache terakhir) ✓ **Dihitung terhadap ITPM**
* `cache_creation_input_tokens` (token yang sedang ditulis ke cache) ✓ **Dihitung terhadap ITPM**
* `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung terhadap ITPM** untuk sebagian besar model

<Note>
  Field `input_tokens` hanya mewakili token yang muncul **setelah breakpoint cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

  ```text wrap
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen yang di-cache sebesar 200k token dan pertanyaan pengguna sebesar 50 token, Anda akan melihat `input_tokens: 50` meskipun total input adalah 200.050 token.

  Untuk keperluan batas laju pada sebagian besar model, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung terhadap batas ITPM Anda, menjadikan [caching prompt](/docs/id/build-with-claude/prompt-caching) cara yang efektif untuk meningkatkan throughput efektif Anda.
</Note>

**Contoh**: Dengan batas ITPM 2.000.000 dan tingkat cache hit 80%, Anda secara efektif dapat memproses 10.000.000 total token input per menit (2 juta tidak di-cache + 8 juta di-cache), karena token yang di-cache tidak dihitung terhadap batas laju Anda.

<Note>
  Claude Haiku 3.5 (ditandai dengan † pada tabel batas laju berikut) juga menghitung `cache_read_input_tokens` terhadap batas laju ITPM.

  Untuk semua model tanpa penanda †, token input yang di-cache tidak dihitung terhadap batas laju dan ditagih dengan tarif yang lebih rendah (10% dari harga token input dasar). Ini berarti Anda dapat mencapai throughput efektif yang jauh lebih tinggi dengan menggunakan [caching prompt](/docs/id/build-with-claude/prompt-caching).
</Note>

<Tip>
  **Maksimalkan batas laju Anda dengan caching prompt**

  Untuk memaksimalkan batas laju Anda, gunakan [caching prompt](/docs/id/build-with-claude/prompt-caching) untuk konten yang berulang seperti:

  * Instruksi sistem dan prompt
  * Dokumen konteks yang besar
  * Definisi alat
  * Riwayat percakapan

  Dengan caching yang efektif, Anda dapat meningkatkan throughput aktual Anda secara dramatis tanpa meningkatkan batas laju Anda. Pantau tingkat cache hit Anda di [halaman Usage](/usage) untuk mengoptimalkan strategi caching Anda.
</Tip>

Batas laju OTPM dievaluasi secara real time saat token output dihasilkan, hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak diperhitungkan dalam perhitungan batas laju OTPM, sehingga tidak ada kerugian batas laju dalam menetapkan nilai `max_tokens` yang lebih tinggi.

Batas laju diterapkan secara terpisah untuk setiap model; oleh karena itu Anda dapat menggunakan model yang berbeda hingga batas masing-masing secara bersamaan. Anda dapat memeriksa batas laju dan perilaku Anda saat ini di [Claude Console](/settings/limits), atau membaca batasan yang dikonfigurasi secara terprogram dengan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

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
    Jika Anda memerlukan batasan yang lebih tinggi dari tier Scale, hubungi bagian penjualan melalui [Claude Console](/settings/limits).
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
    Jika Anda memerlukan batasan yang lebih tinggi dari tier Scale, hubungi bagian penjualan melalui [Claude Console](/settings/limits).
  </Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](/docs/id/managed-agents/overview) dibatasi lajunya per organisasi. Batasan ini terpisah dari batas laju Messages API di atas.

| Operasi                                                   | Batas                      |
| --------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (misalnya, agen, sesi, dan lingkungan) | 300 permintaan per menit   |
| Endpoint pembacaan (misalnya, retrieve, list, dan stream) | 1.200 permintaan per menit |

### Batas laju fast mode

Saat menggunakan [fast mode](/docs/id/build-with-claude/fast-mode) (pratinjau riset) dengan `speed: "fast"` pada Claude Opus 4.8 atau Opus 4.7, batas laju khusus berlaku yang terpisah dari batas laju Opus standar. Ketika batas laju fast mode terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after`. Fast mode tidak tersedia pada Claude Opus 4.6: permintaan ke `claude-opus-4-6` dengan `speed: "fast"` berjalan pada kecepatan standar. Lihat [Fast mode](/docs/id/build-with-claude/fast-mode#supported-models).

Respons menyertakan header `anthropic-fast-*` yang menunjukkan status batas laju fast mode Anda. Lihat [Fast mode](/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Usage](/usage) di [Claude Console](/).

Selain menyediakan grafik token dan permintaan, halaman Usage menyediakan dua grafik batas laju terpisah. Gunakan grafik ini untuk melihat ruang yang Anda miliki untuk berkembang, kapan Anda mungkin mencapai penggunaan puncak, lebih memahami batas laju apa yang perlu diminta, atau bagaimana Anda dapat meningkatkan tingkat caching Anda. Grafik ini memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya, per model):

* Grafik **Rate Limit - Input Tokens** mencakup:

  * Token input tidak di-cache maksimum per jam per menit
  * Batas laju token input per menit Anda saat ini
  * Tingkat cache untuk token input Anda (yaitu, persentase token input yang dibaca dari cache)

* Grafik **Rate Limit - Output Tokens** mencakup:

  * Token output maksimum per jam per menit
  * Batas laju token output per menit Anda saat ini

## Meminta batas yang lebih tinggi

Untuk meminta batas laju yang lebih tinggi atau batas pengeluaran bulanan yang lebih tinggi, gunakan **Request rate limit increase** di halaman [Limits](/settings/limits).

<Note>
  Tim dukungan juga dapat menaikkan batasan. Untuk kebutuhan mendesak, hubungi [dukungan](https://support.claude.com).
</Note>

## Menetapkan batas yang lebih rendah untuk Workspace

Untuk informasi lebih lanjut tentang workspace, lihat [Workspaces](/docs/id/manage-claude/workspaces).

Untuk melindungi Workspace di Organisasi Anda dari potensi penggunaan berlebih, Anda dapat menetapkan batas pengeluaran dan batas laju kustom per Workspace.

Contoh: Jika batas Organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda dapat membatasi satu Workspace menjadi 30.000 token input per menit. Ini melindungi Workspace lain dari potensi penggunaan berlebih dan memastikan distribusi sumber daya yang lebih adil di seluruh Organisasi Anda. Sisa token per menit yang tidak digunakan (atau lebih, jika Workspace tersebut tidak menggunakan batasnya) kemudian tersedia untuk digunakan oleh Workspace lain.

Catatan:

* Anda tidak dapat menetapkan batasan pada Workspace default.
* Jika tidak ditetapkan, batas Workspace sama dengan batas Organisasi.
* Batas Workspace ditetapkan per jenis pembatas (seperti permintaan per menit, token input per menit, atau token output per menit).
* Batas di seluruh Organisasi selalu berlaku, bahkan jika jumlah batas Workspace melebihinya.

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

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas paling ketat yang saat ini berlaku. Misalnya, jika Anda telah melampaui batas token per menit Workspace, header akan berisi nilai batas laju token per menit Workspace. Jika batas Workspace tidak berlaku, header akan mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Pendekatan ini memastikan bahwa Anda memiliki visibilitas terhadap kendala yang paling relevan pada penggunaan API Anda saat ini.
