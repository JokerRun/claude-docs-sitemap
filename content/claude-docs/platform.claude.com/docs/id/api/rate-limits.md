---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 1f42c09f8217c1816c9b729b089fc84c0704f52a64c8a14f98f26997d43cffd9
---

---
title: Batas laju
url: https://platform.claude.com/docs/id/api/rate-limits
description: Untuk memitigasi penyalahgunaan dan mengelola kapasitas pada API, terdapat batasan mengenai seberapa banyak sebuah organisasi dapat menggunakan Claude API.
---

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas laju pada halaman ini berlaku untuk Claude Platform on AWS, tetapi penagihan dan pengelolaan batasnya berbeda. Penagihan dilakukan melalui AWS Marketplace (bukan pembelian kredit Anthropic). Organisasi di Claude Platform on AWS ditempatkan pada tingkat Start dan tidak berpindah antar tingkat penggunaan secara otomatis. Untuk meminta batas yang lebih tinggi, hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com); alur **Request rate limit increase** tidak tersedia. Konfigurasi batas laju per workspace dan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) tidak tersedia di Claude Platform on AWS. Untuk detailnya, lihat [Batas laju dan kuota di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

Ada dua jenis batas:

1. **Batas pengeluaran** ("spend limits") menetapkan biaya bulanan maksimum yang dapat dikeluarkan sebuah organisasi untuk penggunaan API.
2. **Batas laju** ("rate limits") menetapkan jumlah maksimum permintaan API yang dapat dibuat sebuah organisasi dalam periode waktu tertentu.

API memberlakukan batas yang dikonfigurasi oleh layanan di tingkat organisasi, tetapi Anda juga dapat menetapkan batas yang dapat dikonfigurasi pengguna untuk workspace organisasi Anda.

## Tentang batas laju

* Batas dirancang untuk mencegah penyalahgunaan API, sekaligus meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batas ditentukan berdasarkan **tingkat penggunaan** ("usage tier"). Organisasi ditempatkan pada suatu tingkat secara otomatis berdasarkan riwayat penggunaan dan status akun, serta dapat berpindah ke tingkat yang lebih tinggi seiring waktu saat mereka menggunakan API.
* Organisasi baru dan organisasi dengan riwayat penggunaan terbatas mungkin memulai di tingkat Evaluation, dengan batas di bawah batas standar yang ditampilkan di halaman ini selagi riwayat akun dibangun. Batas awal ini merupakan bagian dari cara Anthropic mencegah penipuan dan penyalahgunaan, dan batas tersebut meningkat secara otomatis seiring organisasi Anda membangun riwayat penggunaan.
* Batas ditetapkan di tingkat organisasi. Anda dapat melihat tingkat dan batas organisasi Anda saat ini di halaman [Rate limits](https://platform.claude.com/settings/limits) di [Claude Console](https://platform.claude.com/).
* Anda mungkin mencapai batas laju dalam interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) mungkin diberlakukan sebagai 1 permintaan per detik. Lonjakan permintaan singkat dapat melampaui batas dan memicu error batas laju.
* Batas berikut adalah batas standar untuk setiap tingkat. Jika Anda memerlukan batas yang lebih tinggi, lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus diisi ulang hingga batas maksimum Anda, bukan direset pada interval tetap.
* Semua batas yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan minimum yang dijamin. Batas ini dimaksudkan untuk mengurangi pengeluaran berlebih yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Batas pengeluaran bulanan yang sama berlaku, dan permintaan berhenti pada batas tersebut dengan cara yang sama. Penagihan dan kenaikan tingkat bekerja secara berbeda; lihat [Batas pengeluaran di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#spend-limits).
</Note>

Masing-masing tingkat Start, Build, dan Scale memiliki batas pengeluaran bulanan ("monthly spend cap"), yaitu jumlah maksimum yang dapat dibelanjakan organisasi Anda pada API setiap bulan kalender. Anda dapat melihat batas pengeluaran bulanan organisasi Anda dan menetapkan batas Anda sendiri di halaman [Billing](https://platform.claude.com/settings/billing).

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

* Tipe error-nya adalah `rate_limit_error`, sama seperti untuk batas laju, tetapi responsnya tidak memiliki header `retry-after`. Percobaan ulang, termasuk percobaan ulang otomatis dari SDK, akan gagal hingga akses dilanjutkan.
* Pada Messages API, `error.details.error_code` bernilai `enforced_spend_limit_reached`. Gunakan nilai ini untuk membedakan respons ini dari batas laju.
* Berpindah ke tingkat yang lebih tinggi akan memulihkan akses; lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).

### Menetapkan batas pengeluaran Anda sendiri

Anda juga dapat menetapkan batas pengeluaran Anda sendiri di bawah batas tingkat Anda untuk mengendalikan biaya:

<Steps>
  <Step title="Buka halaman Billing">
    Buka [Settings > Billing](https://platform.claude.com/settings/billing) di Claude Console.
  </Step>

  <Step title="Buka editor batas pengeluaran">
    Di bagian **Spend limits**, klik **Adjust limit** (atau **Set limit** jika belum ada batas yang ditetapkan).
  </Step>

  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas pengeluaran Anda tidak dapat melebihi batas tingkat Anda saat ini.
  </Step>
</Steps>

Ketika penggunaan mencapai batas pengeluaran yang Anda tetapkan, permintaan mengembalikan HTTP 400 dengan tipe error `invalid_request_error`. Pesannya diawali dengan `You have reached your specified API usage limits`, atau `You have reached your specified workspace API usage limits` untuk batas workspace, dan menyatakan kapan akses dilanjutkan. Naikkan atau hapus batas tersebut untuk memulihkan akses lebih cepat.

Batas pada [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace) diperiksa secara terpisah: permintaan Claude Code yang melampaui batas workspace tersebut dapat menerima 429 yang membawa header `retry-after`.

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model. Jika Anda melampaui salah satu batas laju, Anda akan mendapatkan [error 429](https://platform.claude.com/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui, beserta header `retry-after` yang menunjukkan berapa lama harus menunggu.

<Note>
  Anda mungkin juga menemui error 429 karena batas akselerasi pada API jika organisasi Anda mengalami peningkatan penggunaan yang tajam. Untuk menghindari batas akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
</Note>

### ITPM yang sadar cache

Banyak penyedia API menggunakan batas gabungan "tokens per minute" (token per menit), atau TPM, yang mungkin mencakup semua token, baik yang di-cache maupun tidak, input maupun output. **Untuk sebagian besar model Claude, hanya token input yang tidak di-cache yang dihitung terhadap batas laju ITPM Anda.** Ini adalah keunggulan utama yang membuat batas laju secara efektif lebih tinggi daripada yang terlihat pada awalnya.

Batas laju ITPM diestimasi di awal setiap permintaan, dan estimasi tersebut disesuaikan selama permintaan berlangsung untuk mencerminkan jumlah token input aktual yang digunakan.

Berikut yang dihitung terhadap ITPM:

* `input_tokens` (token setelah breakpoint cache terakhir) ✓ **Dihitung terhadap ITPM**
* `cache_creation_input_tokens` (token yang sedang ditulis ke cache) ✓ **Dihitung terhadap ITPM**
* `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung terhadap ITPM** untuk sebagian besar model

<Note>
  Field `input_tokens` hanya mewakili token yang muncul **setelah breakpoint cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

  ```text wrap
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen yang di-cache sebesar 200k token dan pertanyaan pengguna sebesar 50 token, Anda akan melihat `input_tokens: 50` meskipun total inputnya adalah 200.050 token.

  Untuk keperluan batas laju pada sebagian besar model, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung terhadap batas ITPM Anda, sehingga [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) menjadi cara yang efektif untuk meningkatkan throughput efektif Anda.
</Note>

**Contoh:** Dengan batas 2.000.000 ITPM dan tingkat cache hit 80%, Anda dapat secara efektif memproses 10.000.000 total token input per menit (2 juta tidak di-cache + 8 juta di-cache), karena token yang di-cache tidak dihitung terhadap batas laju Anda.

<Note>
  Claude Haiku 3.5 (ditandai dengan catatan kaki 4 dalam tabel batas laju berikut) juga menghitung `cache_read_input_tokens` terhadap batas laju ITPM.

  Untuk semua model lainnya, token input yang di-cache tidak dihitung terhadap batas laju dan ditagih dengan [tarif pembacaan cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pricing), sebagian kecil dari harga input dasar. Ini berarti Anda dapat mencapai throughput efektif yang jauh lebih tinggi dengan menggunakan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).
</Note>

Untuk memaksimalkan batas laju Anda, cache konten yang berulang seperti instruksi sistem dan prompt, dokumen konteks besar, definisi alat, dan riwayat percakapan; lihat [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk panduan. Dengan caching yang efektif, Anda dapat meningkatkan throughput aktual Anda secara substansial tanpa menaikkan batas laju Anda. Pantau tingkat cache hit Anda di [halaman Usage](https://platform.claude.com/usage) untuk menyempurnakan strategi caching Anda.

Batas laju OTPM dievaluasi secara real time saat token output dihasilkan, hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak diperhitungkan dalam kalkulasi batas laju OTPM, sehingga tidak ada kerugian batas laju dalam menetapkan nilai `max_tokens` yang lebih tinggi.

Batas laju diterapkan secara terpisah untuk setiap model; oleh karena itu Anda dapat menggunakan model yang berbeda hingga batas masing-masing secara bersamaan. Anda dapat memeriksa batas laju dan perilaku Anda saat ini di halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console, atau membaca batas yang dikonfigurasi secara terprogram dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

<Note>
  Batas laju saat ini dibagi bersama di semua nilai `inference_geo`. Permintaan dengan `inference_geo: "us"` dan `inference_geo: "global"` mengambil dari pool batas laju yang sama.
</Note>

<Tabs>
  <Tab title="Tingkat Start">
    | Model                                                                                                                                       | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.x1                                                                                                                           | 1.000                               | 500.000                               | 100.000                                |
    | Claude Opus 5                                                                                                                               | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Opus 4.x2                                                                                                                            | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 5                                                                                                                             | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Sonnet 4.x3                                                                                                                          | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 4.5                                                                                                                            | 1.000                               | 2.000.000                             | 400.000                                |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 1.000                               | 100.0004                              | 20.000                                 |
  </Tab>

  <Tab title="Tingkat Build">
    | Model                                                                                                                                       | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.x1                                                                                                                           | 2.000                               | 1.500.000                             | 300.000                                |
    | Claude Opus 5                                                                                                                               | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Opus 4.x2                                                                                                                            | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 5                                                                                                                             | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Sonnet 4.x3                                                                                                                          | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 4.5                                                                                                                            | 5.000                               | 5.000.000                             | 1.000.000                              |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 2.000                               | 200.0004                              | 40.000                                 |
  </Tab>

  <Tab title="Tingkat Scale">
    | Model                                                                                                                                       | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
    | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------- | -------------------------------------- |
    | Claude Fable 5.x1                                                                                                                           | 4.000                               | 4.000.000                             | 800.000                                |
    | Claude Opus 5                                                                                                                               | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Opus 4.x2                                                                                                                            | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 5                                                                                                                             | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Sonnet 4.x3                                                                                                                          | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 4.5                                                                                                                            | 10.000                              | 10.000.000                            | 2.000.000                              |
    | Claude Haiku 3.5 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | 4.000                               | 400.0004                              | 80.000                                 |
  </Tab>

  <Tab title="Tingkat Custom">
    Jika Anda memerlukan batas yang lebih tinggi daripada tingkat Scale, hubungi tim penjualan melalui halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console.
  </Tab>
</Tabs>

*1 Batas laju Fable adalah batas total yang berlaku untuk lalu lintas gabungan di Claude Fable 5.1 dan Claude Fable 5. Claude Mythos 5.1 dan Claude Mythos 5 berbagi batas gabungan terpisah dengan ketentuan yang sama.*

*2 Batas laju Opus adalah batas total yang berlaku untuk lalu lintas gabungan di Claude Opus 4.8, Opus 4.7, Opus 4.6, dan Opus 4.5. Claude Opus 5 memiliki batas laju terpisah dan bukan bagian dari bucket gabungan ini.*

*3 Batas laju Sonnet 4.x adalah batas total yang berlaku untuk lalu lintas gabungan di Sonnet 4.6 dan Sonnet 4.5. Claude Sonnet 5 memiliki batas laju terpisah dan bukan bagian dari bucket gabungan ini.*

*4 Batas ini menghitung `cache_read_input_tokens` terhadap penggunaan ITPM.*

### Message Batches API

Message Batches API memiliki serangkaian batas lajunya sendiri yang dibagi bersama di semua model. Ini mencakup batas permintaan per menit (RPM) untuk semua endpoint API dan batas jumlah permintaan batch yang dapat berada dalam antrean pemrosesan pada waktu yang sama. "Permintaan batch" di sini mengacu pada bagian dari sebuah Message Batch. Anda dapat membuat Message Batch yang berisi ribuan permintaan batch, yang masing-masing dihitung terhadap batas ini. Sebuah permintaan batch dianggap sebagai bagian dari antrean pemrosesan ketika belum berhasil diproses oleh model.

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
    Jika Anda memerlukan batas yang lebih tinggi daripada tingkat Scale, hubungi tim penjualan melalui halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console.
  </Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dibatasi lajunya per organisasi. Batas ini terpisah dari batas laju Messages API di atas.

| Operasi                                                   | Batas                      |
| --------------------------------------------------------- | -------------------------- |
| Endpoint pembuatan (misalnya, agen, sesi, dan lingkungan) | 300 permintaan per menit   |
| Endpoint pembacaan (misalnya, retrieve, list, dan stream) | 1.200 permintaan per menit |

### Files API

Permintaan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) memiliki batas per organisasinya sendiri, yang dibagi bersama di seluruh operasi upload, list, retrieve, download, dan delete serta terpisah dari batas Messages API yang dijelaskan sebelumnya di halaman ini. Lihat [batas laju Files API](https://platform.claude.com/docs/id/build-with-claude/files#rate-limits) untuk nilai saat ini.

### Batas laju fast mode

Saat menggunakan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) dengan `speed: "fast"` pada Claude Opus 5 atau Opus 4.8, berlaku batas laju khusus yang terpisah dari batas laju Opus standar. Ketika batas laju fast mode terlampaui, API mengembalikan error `429` dengan header `retry-after`. Fast mode tidak tersedia pada Claude Opus 4.7 (permintaan mengembalikan error) atau Claude Opus 4.6 (permintaan ke `claude-opus-4-6` dengan `speed: "fast"` berjalan pada kecepatan standar). Lihat [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

Respons menyertakan header `anthropic-fast-*` yang menunjukkan status batas laju fast mode Anda. Lihat [Batas laju fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Usage](https://platform.claude.com/usage) di [Claude Console](https://platform.claude.com/).

Selain menyediakan grafik token dan permintaan, halaman Usage menyediakan dua grafik batas laju terpisah. Gunakan grafik ini untuk melihat ruang yang Anda miliki untuk berkembang, mengidentifikasi kapan Anda mungkin mencapai penggunaan puncak, memahami batas laju apa yang perlu diminta, dan mempelajari cara meningkatkan tingkat caching Anda. Grafik tersebut memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya, per model):

* Grafik **Rate Limit - Input Tokens** mencakup:

  * Maksimum per jam dari token input yang tidak di-cache per menit
  * Batas laju token input per menit Anda saat ini
  * Tingkat cache untuk token input Anda (yaitu, persentase token input yang dibaca dari cache)

* Grafik **Rate Limit - Output Tokens** mencakup:

  * Maksimum per jam dari token output per menit
  * Batas laju token output per menit Anda saat ini

## Meminta batas yang lebih tinggi

Untuk meminta batas laju yang lebih tinggi atau batas pengeluaran bulanan yang lebih tinggi, gunakan **Request rate limit increase** di halaman [Rate limits](https://platform.claude.com/settings/limits). Dukungan Anthropic juga dapat menaikkan batas; untuk kebutuhan mendesak, hubungi [dukungan Anthropic](https://support.claude.com).

<Note>
  **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Alur **Request rate limit increase** tidak tersedia. Hubungi perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com), dan sertakan model yang perlu dinaikkan batasnya, token input dan output puncak per menit Anda untuk setiap model, dan kira-kira berapa bagian dari input Anda yang di-cache atau merupakan konteks berulang. Lihat [Batas laju dan kuota di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).
</Note>

## Menetapkan batas yang lebih rendah untuk Workspace

Untuk informasi lebih lanjut tentang workspace, lihat [Workspaces](https://platform.claude.com/docs/id/manage-claude/workspaces).

Untuk melindungi Workspace di Organisasi Anda dari potensi penggunaan berlebih, Anda dapat menetapkan batas pengeluaran dan batas laju kustom per Workspace.

Contoh: Jika batas Organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda dapat membatasi satu Workspace hingga 30.000 token input per menit. Ini melindungi Workspace lain dari potensi penggunaan berlebih dan memastikan distribusi sumber daya yang lebih merata di seluruh Organisasi Anda. Sisa token per menit yang tidak terpakai (atau lebih, jika Workspace tersebut tidak menggunakan batasnya) kemudian tersedia untuk digunakan oleh Workspace lain.

Catatan:

* Anda tidak dapat menetapkan batas pada Workspace default.
* Jika tidak ditetapkan, batas Workspace sama dengan batas Organisasi.
* Batas Workspace ditetapkan per jenis pembatas (seperti permintaan per menit, token input per menit, atau token output per menit).
* Batas tingkat Organisasi selalu berlaku, meskipun jumlah batas Workspace lebih besar.

Untuk membaca batas laju organisasi dan workspace Anda saat ini secara terprogram, gunakan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Header respons

Respons API menyertakan header yang menunjukkan batas laju yang diberlakukan, penggunaan saat ini, dan kapan batas akan direset.

Header berikut dikembalikan:

| Header                                        | Deskripsi                                                                                                                                                                                                                                                                                    |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `retry-after`                                 | Jumlah detik yang harus ditunggu hingga Anda dapat mencoba ulang permintaan. Percobaan ulang yang lebih awal akan gagal. Tidak dikirim bersama 429 batas pengeluaran (lihat [Mencapai batas pengeluaran Anda](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap)). |
| `anthropic-ratelimit-requests-limit`          | Jumlah maksimum permintaan yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                  |
| `anthropic-ratelimit-requests-remaining`      | Jumlah permintaan yang tersisa sebelum dibatasi lajunya.                                                                                                                                                                                                                                     |
| `anthropic-ratelimit-requests-reset`          | Waktu ketika batas laju permintaan akan terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                              |
| `anthropic-ratelimit-tokens-limit`            | Jumlah maksimum token yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                       |
| `anthropic-ratelimit-tokens-remaining`        | Jumlah token yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                          |
| `anthropic-ratelimit-tokens-reset`            | Waktu ketika batas laju token akan terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                                   |
| `anthropic-ratelimit-input-tokens-limit`      | Jumlah maksimum token input yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                 |
| `anthropic-ratelimit-input-tokens-remaining`  | Jumlah token input yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                    |
| `anthropic-ratelimit-input-tokens-reset`      | Waktu ketika batas laju token input akan terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                             |
| `anthropic-ratelimit-output-tokens-limit`     | Jumlah maksimum token output yang diizinkan dalam periode batas laju apa pun.                                                                                                                                                                                                                |
| `anthropic-ratelimit-output-tokens-remaining` | Jumlah token output yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya.                                                                                                                                                                                                   |
| `anthropic-ratelimit-output-tokens-reset`     | Waktu ketika batas laju token output akan terisi penuh kembali, disediakan dalam format RFC 3339.                                                                                                                                                                                            |
| `anthropic-priority-input-tokens-limit`       | Jumlah maksimum token input Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                                                                                                                                                             |
| `anthropic-priority-input-tokens-remaining`   | Jumlah token input Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)                                                                                                                                                                |
| `anthropic-priority-input-tokens-reset`       | Waktu ketika batas laju token input Priority Tier akan terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)                                                                                                                                                         |
| `anthropic-priority-output-tokens-limit`      | Jumlah maksimum token output Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                                                                                                                                                            |
| `anthropic-priority-output-tokens-remaining`  | Jumlah token output Priority Tier yang tersisa (dibulatkan ke ribuan terdekat) sebelum dibatasi lajunya. (Hanya Priority Tier)                                                                                                                                                               |
| `anthropic-priority-output-tokens-reset`      | Waktu ketika batas laju token output Priority Tier akan terisi penuh kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)                                                                                                                                                        |

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas paling ketat yang sedang berlaku. Misalnya, jika Anda telah melampaui batas token per menit Workspace, header akan berisi nilai batas laju token per menit Workspace. Jika batas Workspace tidak berlaku, header akan mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Pendekatan ini memastikan Anda memiliki visibilitas terhadap kendala yang paling relevan pada penggunaan API Anda saat ini. Untuk melihat Workspace mana yang diperhitungkan untuk suatu permintaan, baca [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) `anthropic-workspace-id`, yang membawa ID Workspace yang menjadi tujuan resolusi kunci API atau token akses Anda.
