---
source: platform
url: https://platform.claude.com/docs/id/about-claude/pricing
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: d8c3a35ecdc6e8127768066c21ab1a137ba24695d0d633e6e375e47de5ef53bb
---

# Harga

Pelajari struktur harga Anthropic untuk model dan fitur

---

Halaman ini menyediakan informasi harga terperinci untuk model dan fitur Anthropic. Semua harga dalam USD.

Untuk informasi harga terkini, kunjungi [claude.com/pricing](https://claude.com/pricing).

## Harga model

Tabel berikut menunjukkan harga untuk semua model Claude:

| Model                                                                                                          | Token Input Dasar | Penulisan Cache 5m | Penulisan Cache 1j | Cache Hit & Refresh | Token Output |
| -------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------ | ------------------ | ------------------- | ------------ |
| Claude Fable 5                                                                                                 | $10 / MTok        | $12,50 / MTok      | $20 / MTok         | $1 / MTok           | $50 / MTok   |
| Claude Mythos 5 ([ketersediaan terbatas](https://anthropic.com/glasswing))                                     | $10 / MTok        | $12,50 / MTok      | $20 / MTok         | $1 / MTok           | $50 / MTok   |
| Claude Opus 4.8                                                                                                | $5 / MTok         | $6,25 / MTok       | $10 / MTok         | $0,50 / MTok        | $25 / MTok   |
| Claude Opus 4.7                                                                                                | $5 / MTok         | $6,25 / MTok       | $10 / MTok         | $0,50 / MTok        | $25 / MTok   |
| Claude Opus 4.6                                                                                                | $5 / MTok         | $6,25 / MTok       | $10 / MTok         | $0,50 / MTok        | $25 / MTok   |
| Claude Opus 4.5                                                                                                | $5 / MTok         | $6,25 / MTok       | $10 / MTok         | $0,50 / MTok        | $25 / MTok   |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations))                             | $15 / MTok        | $18,75 / MTok      | $30 / MTok         | $1,50 / MTok        | $75 / MTok   |
| Claude Opus 4 ([dihentikan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations))                | $15 / MTok        | $18,75 / MTok      | $30 / MTok         | $1,50 / MTok        | $75 / MTok   |
| Claude Sonnet 5 [hingga 31 Agustus 2026](/docs/id/about-claude/pricing#claude-sonnet-5-introductory-pricing)   | $2 / MTok         | $2,50 / MTok       | $4 / MTok          | $0,20 / MTok        | $10 / MTok   |
| Claude Sonnet 5 mulai 1 September 2026                                                                         | $3 / MTok         | $3,75 / MTok       | $6 / MTok          | $0,30 / MTok        | $15 / MTok   |
| Claude Sonnet 4.6                                                                                              | $3 / MTok         | $3,75 / MTok       | $6 / MTok          | $0,30 / MTok        | $15 / MTok   |
| Claude Sonnet 4.5                                                                                              | $3 / MTok         | $3,75 / MTok       | $6 / MTok          | $0,30 / MTok        | $15 / MTok   |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations))  | $3 / MTok         | $3,75 / MTok       | $6 / MTok          | $0,30 / MTok        | $15 / MTok   |
| Claude Haiku 4.5                                                                                               | $1 / MTok         | $1,25 / MTok       | $2 / MTok          | $0,10 / MTok        | $5 / MTok    |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | $0,80 / MTok      | $1 / MTok          | $1,60 / MTok       | $0,08 / MTok        | $4 / MTok    |

<Note id="claude-sonnet-5-introductory-pricing">
  Harga perkenalan sebesar $2/$10 per juta token input/output berlaku hingga 31 Agustus 2026, setelah itu harga standar sebesar $3/$15 per juta token input/output akan berlaku.
</Note>

<Note>
  MTok = Juta token. Kolom "Base Input Tokens" menunjukkan harga input standar, kolom "5m Cache Writes", "1h Cache Writes", dan "Cache Hits & Refreshes" khusus untuk [prompt caching](#prompt-caching), dan "Output Tokens" menunjukkan harga output. Lihat [harga prompt caching](#prompt-caching) untuk penjelasan tentang kolom cache dan pengali harga.
</Note>

<Note>
  Claude Opus 4.7 dan model Opus yang lebih baru, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, dan Claude Sonnet 5 menggunakan tokenizer yang lebih baru yang berkontribusi pada peningkatan kinerja mereka pada berbagai tugas. Tokenizer ini menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Claude Sonnet 4.6 dan model sebelumnya menggunakan tokenizer sebelumnya.
</Note>

Untuk harga Claude Platform on AWS, lihat [harga Claude Platform on AWS](#claude-platform-on-aws-pricing).

## Harga platform cloud

Bagian ini mencakup platform cloud yang dioperasikan mitra, di mana penyedia cloud menagih Anda. Untuk platform cloud yang dioperasikan Anthropic yang ditagih melalui marketplace, lihat [harga Claude Platform on AWS](#claude-platform-on-aws-pricing) dan [harga Claude in Microsoft Foundry](#claude-in-microsoft-foundry-pricing).

Model Claude tersedia di [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai). Untuk harga resmi, kunjungi:

* [Harga Amazon Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Harga Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models)

<Note>
  **Harga endpoint regional dan multi-region untuk model Claude 4.5 dan seterusnya**

  Mulai dari Claude Sonnet 4.5, Haiku 4.5, dan Opus 4.5:

  * **Bedrock** menawarkan dua jenis endpoint: endpoint global (perutean dinamis untuk ketersediaan maksimum) dan endpoint regional (perutean data terjamin melalui wilayah geografis tertentu).
  * **Google Cloud** menawarkan tiga jenis endpoint: endpoint global, endpoint multi-region (perutean dinamis dalam suatu area geografis), dan endpoint regional.

  Endpoint regional dan multi-region menyertakan premi 10% dibandingkan endpoint global. Claude API (pihak pertama) bersifat global secara default; untuk opsi dan harga residensi data pihak pertama, lihat [Harga residensi data](#data-residency-pricing).

  **Cakupan:** Struktur harga ini berlaku untuk Claude Sonnet 4.5, Haiku 4.5, Opus 4.5, dan semua model mendatang. Model sebelumnya (Claude Opus 4.1 (tidak digunakan lagi) dan rilis sebelumnya) mempertahankan harga yang sudah ada.

  Untuk detail implementasi dan contoh kode:

  * [Endpoint global vs regional Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock#regions) untuk Opus 4.7, Haiku 4.5, dan model yang lebih baru, atau [integrasi lama](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#global-vs-regional-endpoints) untuk semua model lain di Bedrock
  * [Endpoint global, multi-region, dan regional Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai#global-multi-region-and-regional-endpoints)
</Note>

## Harga Claude Platform on AWS

[Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) menagih melalui AWS Marketplace menggunakan Claude Consumption Units (CCU). Anthropic menghitung penggunaan token Anda dalam USD dengan tarif standar per-model, per-fitur, menerapkan diskon yang dinegosiasikan, mengonversi hasilnya ke CCU dengan tarif $0,01 per CCU, dan melaporkan jumlah CCU ke AWS Marketplace setiap jam. Tagihan AWS Anda menampilkan satu item baris CCU.

| Konsep                | Detail                                                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Unit penagihan**    | Claude Consumption Unit (CCU)                                                                                                                                                         |
| **Harga CCU**         | $0,01 per CCU (tetap; diskon berlaku pada konversi token-ke-CCU, bukan pada harga CCU)                                                                                                |
| **Konversi**          | Penggunaan token dihitung dalam USD dengan tarif standar per-model, per-fitur (sama dengan [harga Claude API](#model-pricing)), kemudian dikonversi ke CCU dengan tarif $0,01 per CCU |
| **Siklus penagihan**  | Pengukuran per jam ke AWS Marketplace; faktur bulanan                                                                                                                                 |
| **Model pembayaran**  | Hanya tunggakan (pascabayar); tidak ada kredit prabayar                                                                                                                               |
| **Diskon**            | Diterapkan sebagai lebih sedikit CCU yang diukur                                                                                                                                      |
| **Pajak**             | Pengukuran sebelum pajak; AWS Marketplace menangani pajak                                                                                                                             |
| **Visibilitas biaya** | Rincian real-time di Claude Console (akses melalui AWS Console); AWS Cost Explorer menampilkan CCU teragregasi                                                                        |

<Note>
  **Claude Consumption Units.** Jika Pelanggan mengakses Layanan melalui Platform Marketplace tertentu (misalnya, Claude Platform on AWS), penggunaan akan ditagih dalam Claude Consumption Units ("CCU") alih-alih per MTok. CCU adalah satuan ukur yang digunakan semata-mata untuk penagihan Platform Marketplace. Seratus (100) CCU mewakili $1,00 USD biaya yang terutang untuk Layanan, dihitung dengan harga yang berlaku di [claude.com/pricing#api](https://claude.com/pricing#api), setelah penerapan diskon apa pun.
</Note>

### Geografi inferensi

Untuk Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, penggunaan `inference_geo: "us"` menerapkan pengali harga 1,1x. `inference_geo: "global"` (default) menggunakan harga standar. Lihat [Residensi data](/docs/id/manage-claude/data-residency) untuk detailnya.

### Penawaran privat

Saat Anda mendaftar di halaman layanan **Claude Platform on AWS** di AWS Console, AWS Console mencari penawaran privat apa pun yang terkait dengan akun Anda dan meminta Anda untuk menerimanya di AWS Marketplace. Hubungi perwakilan akun Anthropic Anda untuk ketentuan penawaran privat.

<Note>
  Jika Anda memiliki penawaran privat Amazon Bedrock yang sudah ada, hubungi perwakilan akun Anthropic atau AWS Anda sebelum memulai dengan Claude Platform on AWS untuk memastikan diskon Anda diterapkan dengan benar. Diskon tidak dapat diterapkan secara retroaktif pada penggunaan yang terjadi sebelum penawaran privat Anda diterima.
</Note>

## Harga Claude in Microsoft Foundry

[Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) menagih melalui Azure Marketplace menggunakan Claude Consumption Units (CCU). Anthropic menghitung penggunaan token Anda dalam USD dengan tarif standar per-model, per-fitur, menerapkan diskon yang dinegosiasikan, mengonversi hasilnya ke CCU dengan tarif $0,01 per CCU, dan melaporkan jumlah CCU ke Azure Marketplace setiap jam. Tagihan Azure Anda menampilkan satu item baris CCU.

| Konsep                | Detail                                                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Unit penagihan**    | Claude Consumption Unit (CCU)                                                                                                                                                         |
| **Harga CCU**         | $0,01 per CCU (tetap; diskon berlaku pada konversi token-ke-CCU, bukan pada harga CCU)                                                                                                |
| **Konversi**          | Penggunaan token dihitung dalam USD dengan tarif standar per-model, per-fitur (sama dengan [harga Claude API](#model-pricing)), kemudian dikonversi ke CCU dengan tarif $0,01 per CCU |
| **Siklus penagihan**  | Pengukuran per jam ke Azure Marketplace; faktur bulanan                                                                                                                               |
| **Model pembayaran**  | Hanya tunggakan (pascabayar); tidak ada kredit prabayar                                                                                                                               |
| **Diskon**            | Diterapkan sebagai lebih sedikit CCU yang diukur                                                                                                                                      |
| **Pajak**             | Pengukuran sebelum pajak; Azure Marketplace menangani pajak                                                                                                                           |
| **Visibilitas biaya** | Azure Cost Management menampilkan CCU teragregasi                                                                                                                                     |

<Note>
  **Claude Consumption Units.** Jika Pelanggan mengakses Layanan melalui Platform Marketplace tertentu (misalnya, Claude Platform on AWS, Claude in Microsoft Foundry), penggunaan akan ditagih dalam Claude Consumption Units ("CCU") alih-alih per MTok. CCU adalah satuan ukur yang digunakan semata-mata untuk penagihan Platform Marketplace. Seratus (100) CCU mewakili $1,00 USD biaya yang terutang untuk Layanan, dihitung dengan harga yang berlaku di [claude.com/pricing#api](https://claude.com/pricing#api), setelah penerapan diskon apa pun.
</Note>

### Geografi inferensi

Deployment yang dihosting di Azure dapat menggunakan jenis deployment US Data Zone Standard, yang menjaga inferensi tetap di dalam Amerika Serikat. Ini setara dengan `inference_geo: "us"` pada Claude API dan menerapkan pengali harga 1,1x yang sama. Lihat [Residensi data](/docs/id/manage-claude/data-residency) untuk detailnya.

## Harga khusus fitur

### Prompt caching

"Prompt caching" (caching prompt) mengurangi biaya dan latensi dengan menggunakan kembali bagian prompt Anda yang telah diproses sebelumnya di seluruh panggilan API. Alih-alih memproses ulang prompt sistem, dokumen, atau riwayat percakapan besar yang sama pada setiap permintaan, API membaca dari cache dengan sebagian kecil dari harga input standar.

Ada dua cara untuk mengaktifkan caching prompt:

* **Caching otomatis:** Tambahkan satu field `cache_control` di tingkat atas permintaan Anda. Sistem secara otomatis mengelola breakpoint cache seiring percakapan berkembang. Ini adalah titik awal yang direkomendasikan untuk sebagian besar kasus penggunaan.
* **Breakpoint cache eksplisit:** Tempatkan `cache_control` langsung pada blok konten individual untuk kontrol terperinci atas apa yang di-cache.

Caching prompt menggunakan pengali harga berikut relatif terhadap tarif token input dasar:

| Operasi cache           | Pengali                 | Durasi                                       |
| ----------------------- | ----------------------- | -------------------------------------------- |
| Penulisan cache 5 menit | 1,25x harga input dasar | Cache berlaku selama 5 menit                 |
| Penulisan cache 1 jam   | 2x harga input dasar    | Cache berlaku selama 1 jam                   |
| Pembacaan cache (hit)   | 0,1x harga input dasar  | Durasi yang sama dengan penulisan sebelumnya |

Token penulisan cache dikenakan biaya saat konten pertama kali disimpan. Token pembacaan cache dikenakan biaya saat permintaan berikutnya mengambil konten yang di-cache. Cache hit berbiaya 10% dari harga input standar, yang berarti caching menjadi menguntungkan setelah hanya satu pembacaan cache untuk durasi 5 menit (penulisan 1,25x), atau setelah dua pembacaan cache untuk durasi 1 jam (penulisan 2x).

Pengali ini dapat digabungkan dengan pengubah harga lainnya, termasuk diskon Batch API dan residensi data.

Untuk detail implementasi, model yang didukung, dan contoh kode, lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching).

### Harga residensi data

Untuk Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, menentukan inferensi khusus AS melalui parameter `inference_geo` dikenakan pengali 1,1x pada semua kategori harga token, termasuk token input, token output, penulisan cache, dan pembacaan cache. Perutean global (default) menggunakan harga standar.

Ini berlaku untuk Claude API (pihak pertama) dan Claude Platform on AWS. Pada Claude in Microsoft Foundry, pengali 1,1x yang sama berlaku untuk deployment yang menggunakan jenis deployment US Data Zone Standard (lihat [Geografi inferensi](#foundry-inference-geography)). Platform yang dioperasikan mitra (Bedrock dan Google Cloud) memiliki harga regional independen. Lihat [Bedrock](https://aws.amazon.com/bedrock/pricing/) dan [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models) untuk detailnya. Model sebelumnya tidak mendukung parameter `inference_geo` dan selalu menggunakan harga standar; permintaan yang menyertakan parameter tersebut pada model-model ini mengembalikan error 400.

Untuk informasi lebih lanjut, lihat [Residensi data](/docs/id/manage-claude/data-residency).

### Harga fast mode

[Fast mode](/docs/id/build-with-claude/fast-mode), dalam pratinjau riset, menyediakan output yang jauh lebih cepat untuk Claude Opus 4.8 dan Claude Opus 4.7 dengan harga premium. Harga fast mode berlaku di seluruh jendela konteks penuh, termasuk permintaan di atas 200k token input. Fast mode tidak tersedia di Claude Platform on AWS.

| Model           | Input      | Output      |
| --------------- | ---------- | ----------- |
| Claude Opus 4.8 | $10 / MTok | $50 / MTok  |
| Claude Opus 4.7 | $30 / MTok | $150 / MTok |

Fast mode untuk Claude Opus 4.7 tidak digunakan lagi dan akan dihapus pada 24 Juli 2026. Per 29 Juni 2026, fast mode tidak tersedia pada Claude Opus 4.6: permintaan ke `claude-opus-4-6` dengan `speed: "fast"` berjalan dengan kecepatan standar dan ditagih dengan tarif standar. Lihat [Fast mode](/docs/id/build-with-claude/fast-mode#supported-models).

Harga fast mode dapat digabungkan dengan pengubah harga lainnya:

* [Pengali prompt caching](#prompt-caching) berlaku di atas harga fast mode
* Pengali [residensi data](/docs/id/manage-claude/data-residency) berlaku di atas harga fast mode

Fast mode tidak tersedia dengan [Batch API](#batch-processing).

Untuk informasi lebih lanjut, lihat [Fast mode](/docs/id/build-with-claude/fast-mode).

### Pemrosesan batch

Batch API memungkinkan pemrosesan asinkron untuk volume permintaan yang besar dengan diskon 50% pada token input dan output.

| Model                                                                                                          | Input batch  | Output batch  |
| -------------------------------------------------------------------------------------------------------------- | ------------ | ------------- |
| Claude Fable 5                                                                                                 | $5 / MTok    | $25 / MTok    |
| Claude Mythos 5 ([ketersediaan terbatas](https://anthropic.com/glasswing))                                     | $5 / MTok    | $25 / MTok    |
| Claude Opus 4.8                                                                                                | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.7                                                                                                | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.6                                                                                                | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.5                                                                                                | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations))                             | $7.50 / MTok | $37.50 / MTok |
| Claude Opus 4 ([dihentikan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations))                | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 5 [hingga 31 Agustus 2026](/docs/id/about-claude/pricing#claude-sonnet-5-introductory-pricing)   | $1 / MTok    | $5 / MTok     |
| Claude Sonnet 5 mulai 1 September 2026                                                                         | $1.50 / MTok | $7.50 / MTok  |
| Claude Sonnet 4.6                                                                                              | $1.50 / MTok | $7.50 / MTok  |
| Claude Sonnet 4.5                                                                                              | $1.50 / MTok | $7.50 / MTok  |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations))  | $1.50 / MTok | $7.50 / MTok  |
| Claude Haiku 4.5                                                                                               | $0.50 / MTok | $2.50 / MTok  |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | $0.40 / MTok | $2 / MTok     |

Untuk informasi lebih lanjut tentang pemrosesan batch, lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing).

### Harga konteks panjang

Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5, dan Sonnet 4.6 menyertakan [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) penuh dengan harga standar. (Permintaan 900k token ditagih dengan tarif per-token yang sama dengan permintaan 9k token.) Diskon caching prompt dan pemrosesan batch berlaku dengan tarif standar di seluruh jendela konteks penuh.

### Harga penggunaan alat

Permintaan penggunaan alat dikenakan biaya berdasarkan:

1. Jumlah total token input yang dikirim ke model (termasuk dalam parameter `tools`)
2. Jumlah token output yang dihasilkan
3. Untuk alat sisi server, biaya tambahan berbasis penggunaan (misalnya, pencarian web dikenakan biaya per pencarian yang dilakukan)

Alat sisi klien dikenakan biaya yang sama seperti permintaan API Claude lainnya, sedangkan alat sisi server dapat dikenakan biaya tambahan berdasarkan penggunaan spesifiknya.

Token tambahan dari penggunaan alat berasal dari:

* Parameter `tools` dalam permintaan API (nama alat, deskripsi, dan skema)
* Blok konten `tool_use` dalam permintaan dan respons API
* Blok konten `tool_result` dalam permintaan API

Ketika Anda menggunakan `tools`, API juga secara otomatis menyertakan prompt sistem khusus untuk model yang mengaktifkan penggunaan alat. Jumlah token penggunaan alat yang diperlukan untuk setiap model tercantum di bawah ini (tidak termasuk token tambahan yang tercantum di atas). Perhatikan bahwa tabel ini mengasumsikan setidaknya 1 alat disediakan. Jika tidak ada `tools` yang disediakan, maka pilihan alat `none` menggunakan 0 token prompt sistem tambahan.

| Model                                                                                                          | Pilihan alat                   | Jumlah token prompt sistem penggunaan alat |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------ |
| Claude Opus 4.8                                                                                                | `auto`, `none`***`any`, `tool` | 290 token***410 token                      |
| Claude Opus 4.7                                                                                                | `auto`, `none`***`any`, `tool` | 675 token***804 token                      |
| Claude Opus 4.6                                                                                                | `auto`, `none`***`any`, `tool` | 497 token***589 token                      |
| Claude Opus 4.5                                                                                                | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations))                             | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Opus 4 ([dihentikan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations))                | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Sonnet 5                                                                                                | `auto`, `none`***`any`, `tool` | 354 token***474 token                      |
| Claude Sonnet 4.6                                                                                              | `auto`, `none`***`any`, `tool` | 497 token***589 token                      |
| Claude Sonnet 4.5                                                                                              | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations))  | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Haiku 4.5                                                                                               | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | `auto`, `none`***`any`, `tool` | 264 token***355 token                      |

Jumlah token ini ditambahkan ke token input dan output normal Anda untuk menghitung total biaya permintaan.

Untuk harga per-model terkini, lihat bagian [harga model](#model-pricing).

Untuk informasi lebih lanjut tentang implementasi penggunaan alat dan praktik terbaik, lihat [Penggunaan alat](/docs/id/agents-and-tools/tool-use/overview).

### Harga alat spesifik

#### Alat bash

Definisi alat bash menambahkan token input berikut ke permintaan Anda. Ini merupakan tambahan dari [prompt sistem penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) per-model yang berlaku setiap kali ada alat apa pun yang digunakan.

| Model                                                    | Token input tambahan |
| -------------------------------------------------------- | -------------------- |
| Claude Opus 4.7 dan Claude Opus 4.8                      | 325 token            |
| Claude Opus 4.6, Claude Sonnet 4.6, dan versi sebelumnya | 244 token            |

Token tambahan dikonsumsi oleh:

* Output perintah (stdout/stderr)
* Pesan kesalahan
* Konten file berukuran besar

Lihat [harga penggunaan alat](#tool-use-pricing) untuk detail harga lengkap.

#### Alat eksekusi kode

**Code execution gratis ketika digunakan bersama web search atau web fetch.** Ketika `web_search_20260209` (atau versi lebih baru) atau `web_fetch_20260209` (atau versi lebih baru) disertakan dalam permintaan API Anda, tidak ada biaya tambahan untuk panggilan alat code execution selain biaya token input dan output standar.

Ketika digunakan tanpa alat-alat tersebut, code execution ditagih berdasarkan waktu eksekusi, yang dilacak secara terpisah dari penggunaan token:

* Waktu eksekusi memiliki minimum 5 menit
* Setiap organisasi menerima **1.550 jam gratis** penggunaan per bulan
* Penggunaan tambahan di luar 1.550 jam ditagih sebesar **$0,05 per jam, per kontainer**
* Jika file disertakan dalam permintaan, waktu eksekusi tetap ditagih meskipun alat tidak dipanggil, karena file dimuat terlebih dahulu ke dalam kontainer

Penggunaan code execution dilacak dalam respons:

```json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
}
```

#### Alat editor teks

Alat editor teks menggunakan struktur harga yang sama dengan alat lain yang digunakan bersama Claude. Alat ini mengikuti harga token input dan output standar berdasarkan model Claude yang Anda gunakan.

Selain token dasar, token input tambahan berikut diperlukan untuk alat editor teks:

| Alat                                | Token input tambahan |
| ----------------------------------- | -------------------- |
| `text_editor_20250429` (Claude 4.x) | 700 token            |

Lihat [harga penggunaan alat](#tool-use-pricing) untuk detail harga lengkap.

#### Alat pencarian web

Penggunaan pencarian web dikenakan biaya sebagai tambahan dari penggunaan token:

```json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 6039,
    "cache_read_input_tokens": 7123,
    "cache_creation_input_tokens": 7345,
    "server_tool_use": {
      "web_search_requests": 1
    }
  }
}
```

Pencarian web tersedia di API Claude dengan harga **$10 per 1.000 pencarian**, ditambah biaya token standar untuk konten yang dihasilkan dari pencarian. Hasil pencarian web yang diambil sepanjang percakapan dihitung sebagai token input, baik dalam iterasi pencarian yang dijalankan selama satu giliran maupun dalam giliran percakapan berikutnya.

Setiap pencarian web dihitung sebagai satu penggunaan, terlepas dari jumlah hasil yang dikembalikan. Jika terjadi kesalahan selama pencarian web, pencarian web tersebut tidak akan ditagih.

#### Alat pengambilan web

Penggunaan web fetch **tidak dikenakan biaya tambahan** di luar biaya token standar:

```json
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```

Alat web fetch tersedia di Claude API **tanpa biaya tambahan**. Anda hanya membayar biaya token standar untuk konten yang diambil dan menjadi bagian dari konteks percakapan Anda.

Untuk melindungi dari pengambilan konten berukuran besar secara tidak sengaja yang akan menghabiskan token secara berlebihan, gunakan parameter `max_content_tokens` untuk menetapkan batas yang sesuai berdasarkan kasus penggunaan dan pertimbangan anggaran Anda.

Contoh penggunaan token untuk konten umum:

* Halaman web rata-rata (10 kB): \~2.500 token
* Halaman dokumentasi besar (100 kB): \~25.000 token
* PDF makalah penelitian (500 kB): \~125.000 token

#### Alat penggunaan komputer

Computer use mengikuti [harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat computer use:

**Overhead prompt sistem**: Beta computer use menambahkan 466-499 token ke prompt sistem

**Penggunaan token alat computer use**:

| Model            | Token input per definisi alat |
| ---------------- | ----------------------------- |
| Model Claude 4.x | 735 token                     |

**Konsumsi token tambahan**:

* Gambar tangkapan layar (lihat [Harga Vision](/docs/id/build-with-claude/vision))
* Hasil eksekusi alat yang dikembalikan ke Claude

<Note>
  Jika Anda juga menggunakan alat bash atau text editor bersamaan dengan computer use, alat-alat tersebut memiliki biaya token tersendiri sebagaimana didokumentasikan di halaman masing-masing.
</Note>

## Harga Claude Managed Agents

[Claude Managed Agents](/docs/id/managed-agents/overview) ditagih berdasarkan dua dimensi: token dan runtime sesi.

### Token

Semua token yang dikonsumsi oleh sesi Claude Managed Agents ditagih dengan tarif yang ditunjukkan di [Harga model](#model-pricing). Pengali [prompt caching](#prompt-caching) berlaku secara identik. Pencarian web yang dipicu di dalam sesi dikenakan biaya standar $10 per 1.000 pencarian. Pada [Claude Platform on AWS](#claude-platform-on-aws-pricing), biaya token dan runtime sesi dikonversi ke Claude Consumption Units dengan tarif standar.

Pengubah Messages API berikut **tidak** berlaku untuk sesi Claude Managed Agents:

| Pengubah                                          | Mengapa tidak berlaku                                        |
| ------------------------------------------------- | ------------------------------------------------------------ |
| [Diskon Batch API](#batch-processing)             | Sesi bersifat stateful dan interaktif. Tidak ada mode batch. |
| [Premi fast mode](#fast-mode-pricing)             | Kecepatan inferensi dikelola oleh runtime.                   |
| [Pengali residensi data](#data-residency-pricing) | `inference_geo` adalah field permintaan Messages API.        |
| [Harga platform cloud](#cloud-platform-pricing)   | Tidak tersedia di platform cloud yang dioperasikan mitra.    |

### Runtime sesi

| SKU          | Tarif              | Pengukuran              |
| ------------ | ------------------ | ----------------------- |
| Runtime sesi | $0,08 per jam-sesi | Durasi status `running` |

Runtime diukur hingga milidetik dan hanya terakumulasi saat status sesi adalah `running`. Waktu yang dihabiskan dalam status `idle` (menunggu pesan Anda berikutnya atau konfirmasi alat), `rescheduling`, atau `terminated` tidak dihitung dalam runtime.

<Note>
  Runtime sesi menggantikan model penagihan jam-kontainer [Code Execution](#code-execution-tool) saat menggunakan Claude Managed Agents. Anda tidak ditagih secara terpisah untuk jam kontainer di atas runtime sesi.
</Note>

### Contoh perhitungan

Sesi coding satu jam menggunakan Claude Opus 4.8 yang mengonsumsi 50.000 token input dan 15.000 token output:

| Item baris   | Perhitungan              | Biaya      |
| ------------ | ------------------------ | ---------- |
| Token input  | 50.000 × $5 / 1.000.000  | $0,25      |
| Token output | 15.000 × $25 / 1.000.000 | $0,375     |
| Runtime sesi | 1,0 jam × $0,08          | $0,08      |
| **Total**    |                          | **$0,705** |

Jika caching prompt aktif dan 40.000 dari token input adalah pembacaan cache:

| Item baris              | Perhitungan                   | Biaya      |
| ----------------------- | ----------------------------- | ---------- |
| Token input tanpa cache | 10.000 × $5 / 1.000.000       | $0,05      |
| Token pembacaan cache   | 40.000 × $5 × 0,1 / 1.000.000 | $0,02      |
| Token output            | 15.000 × $25 / 1.000.000      | $0,375     |
| Runtime sesi            | 1,0 jam × $0,08               | $0,08      |
| **Total**               |                               | **$0,525** |

<Note>
  Contoh perhitungan untuk memproses 10.000 tiket dukungan:

  * Rata-rata \~3.700 token per percakapan
  * Menggunakan Claude Haiku 4.5 dengan $1/MTok input, $5/MTok output
  * Total biaya: \~$37,00 per 10.000 tiket
</Note>

Untuk panduan terperinci tentang perhitungan ini, lihat [panduan agen dukungan pelanggan](/docs/id/about-claude/use-case-guides/customer-support-chat).

## Pertimbangan harga tambahan

### Strategi optimasi biaya

Saat membangun agen dengan Claude:

1. **Gunakan model yang sesuai:** Pilih Haiku untuk tugas sederhana, Sonnet untuk sebagian besar beban kerja produksi, dan Opus untuk penalaran yang paling kompleks
2. **Implementasikan caching prompt:** Kurangi biaya untuk konteks yang berulang
3. **Operasi batch:** Gunakan Batch API untuk tugas yang tidak sensitif terhadap waktu
4. **Pantau pola penggunaan:** Lacak konsumsi token untuk mengidentifikasi peluang optimasi

<Tip>
  Untuk aplikasi agen bervolume tinggi, hubungi [tim penjualan enterprise](https://claude.com/contact-sales) untuk pengaturan harga khusus.
</Tip>

### Batas laju

"Rate limit" (batas laju) bervariasi berdasarkan tingkat penggunaan dan memengaruhi berapa banyak permintaan yang dapat Anda buat:

* **Tingkat Start:** Batas tingkat awal untuk memulai
* **Tingkat Build:** Batas yang ditingkatkan untuk aplikasi yang berkembang
* **Tingkat Scale:** Batas standar tertinggi untuk beban kerja produksi

Untuk informasi batas laju terperinci, lihat [Batas laju](/docs/id/api/rate-limits).

Untuk batas di luar tingkat Scale atau pengaturan harga khusus, [hubungi tim penjualan](https://claude.com/contact-sales).

### Diskon volume

Diskon volume mungkin tersedia untuk pengguna bervolume tinggi. Ini dinegosiasikan berdasarkan kasus per kasus.

* Tingkat penggunaan standar menggunakan harga yang ditunjukkan di [Harga model](#model-pricing)
* Pelanggan enterprise dapat [menghubungi penjualan](mailto:sales@anthropic.com) untuk harga khusus
* Diskon akademik dan riset mungkin tersedia

### Harga enterprise

Untuk pelanggan enterprise dengan kebutuhan spesifik:

* Batas laju khusus
* Diskon volume
* Dukungan khusus
* Ketentuan khusus

Hubungi tim penjualan di [sales@anthropic.com](mailto:sales@anthropic.com) atau melalui [Claude Console](/settings/limits) untuk mendiskusikan opsi harga enterprise.

## Penagihan dan pembayaran

* Penagihan didasarkan pada penggunaan bulanan aktual
* Semua pembayaran dalam USD
* Opsi kartu kredit dan faktur tersedia
* Pelacakan penggunaan tersedia di [Claude Console](/)

## Pertanyaan yang sering diajukan

**Bagaimana penggunaan token dihitung?**

Token adalah potongan teks yang diproses oleh model. Sebagai perkiraan kasar, 1 token kira-kira setara dengan 4 karakter atau 0,75 kata dalam bahasa Inggris. Jumlah pastinya bervariasi berdasarkan bahasa dan jenis konten.

**Apakah ada tingkat gratis atau uji coba?**

Pengguna baru menerima sejumlah kecil kredit gratis untuk menguji API. [Hubungi penjualan](mailto:sales@anthropic.com) untuk informasi tentang uji coba yang diperpanjang untuk evaluasi enterprise.

**Bagaimana diskon digabungkan?**

Diskon Batch API dan caching prompt dapat digabungkan. Misalnya, menggunakan kedua fitur bersama-sama memberikan penghematan biaya yang signifikan dibandingkan dengan panggilan API standar. Lihat [harga prompt caching](#prompt-caching) untuk cara pengali berinteraksi.

**Metode pembayaran apa yang diterima?**

Kartu kredit utama diterima untuk akun standar. Pelanggan enterprise dapat mengatur faktur dan metode pembayaran lainnya.

Untuk pertanyaan tambahan tentang harga, hubungi [support@anthropic.com](mailto:support@anthropic.com).
