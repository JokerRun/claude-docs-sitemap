---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/api-and-data-retention
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: df82d3709c7d6b847c734cc238529cada0486464f8bd25e96627c1ccf2ce04e9
---

---
title: API dan retensi data
url: https://platform.claude.com/docs/id/manage-claude/api-and-data-retention
description: Pelajari bagaimana API Anthropic dan fitur-fitur terkaitnya menyimpan data, termasuk informasi tentang zero data retention (ZDR) dan akses API yang siap HIPAA.
---

Halaman ini mencakup Claude API (`api.anthropic.com`), Claude Platform on AWS, dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), di mana Anthropic bertindak sebagai pemroses data. Pada Amazon Bedrock dan Google Cloud's Agent Platform, penyedia cloud adalah pemroses data; lihat dokumentasi retensi data dan kepatuhan platform tersebut untuk kontrol yang setara.

Anthropic menawarkan dua pengaturan penanganan data untuk Claude API: ["zero data retention" (retensi data nol), atau ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) dan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness). [Tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) mencantumkan fitur API mana yang dicakup oleh masing-masing pengaturan. Untuk kebijakan retensi standar Anthropic di luar pengaturan ini, lihat [kebijakan retensi data komersial](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

## Bagaimana Anthropic mendekati retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan yang berbeda. Jika suatu fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, fitur tersebut mungkin memenuhi syarat untuk ZDR. Jika suatu fitur memang memerlukan penyimpanan, Anthropic merancangnya dengan jejak retensi sekecil mungkin berdasarkan komitmen berikut:

* Data yang disimpan tidak pernah digunakan untuk pelatihan model tanpa izin tegas dari Anda.
* Hanya yang secara teknis diperlukan agar fitur berfungsi yang disimpan. Konten percakapan (prompt Anda dan output Claude) tidak disimpan secara default; pengecualiannya adalah [Covered Models](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements), yang memerlukan retensi 30 hari.
* Data yang disimpan dihapus dalam "time to live" (masa hidup), atau TTL, terpendek yang praktis, dan Anthropic berupaya memberi pelanggan kendali atas berapa lama data disimpan. Apa yang disimpan, dan durasi retensi jika TTL tertentu berlaku, didokumentasikan di halaman masing-masing fitur.

Beberapa model retensi berada di luar pengaturan ZDR dan HIPAA yang dijelaskan di halaman ini. Data yang dapat diakses melalui [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) mengikuti model retensinya sendiri. [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) menyimpan data selama 6 tahun. Konten chat, file, dan proyek dari claude.ai mengikuti kebijakan retensi organisasi Anda yang ditetapkan di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). [Transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) (Cowork dan Claude Code di mesin pengguna) disimpan selama 6 tahun secara default, atau selama periode retensi percakapan kustom organisasi Anda jika periode terbatas ditetapkan (pengaturan claude.ai yang sama). [Transkrip sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) (Cowork di cloud) disimpan selama 6 tahun. Compliance API tidak menangkap sesi lokal yang berada di bawah ZDR, atau sesi lokal apa pun dari organisasi yang mengaktifkan kesiapan HIPAA.

## Zero data retention (ZDR)

Di bawah pengaturan ZDR, Anthropic tidak menyimpan prompt atau respons pelanggan dalam keadaan diam (at rest) setelah respons API dikembalikan. Untuk meminta ZDR bagi organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales). ZDR diaktifkan per organisasi; setiap organisasi baru memerlukan pengaktifan ZDR secara terpisah oleh tim akun Anda, dan pengaktifan tidak otomatis berlaku untuk organisasi lain di bawah akun yang sama.

### Apa yang dicakup ZDR

* **Claude Messages API dan Token Counting API:** ZDR berlaku untuk endpoint ini bagi fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility). Fitur yang berjalan di atas `/v1/messages` tetapi ditandai "Tidak" dalam tabel (seperti code execution) tidak dicakup.
* **Claude Code:** ZDR berlaku ketika Claude Code digunakan dengan kunci API dari organisasi Komersial (organisasi di bawah Ketentuan Layanan Komersial Anthropic, berbeda dari akun Claude konsumen) atau melalui Claude Enterprise dengan ZDR diaktifkan. Jika pencatatan metrik diaktifkan di Claude Code, data produktivitas seperti statistik penggunaan dikecualikan dari ZDR dan dapat disimpan. Lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention) untuk detail lengkap.
* **Claude Platform on AWS:** [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya.

### Apa yang tidak dicakup ZDR

* **Claude Console:** Penggunaan apa pun di Claude Console, termasuk Playground.
* **Claude Managed Agents:** Claude Managed Agents adalah sumber daya stateful; transkrip sesi tetap ada hingga Anda menghapusnya.
* **Produk konsumen Claude:** Paket Claude Free, Pro, dan Max, termasuk ketika pelanggan pada paket tersebut menggunakan aplikasi web, desktop, atau seluler Claude atau Claude Code.
* **Antarmuka produk Claude Teams dan Claude Enterprise:** Antarmuka ini tidak memenuhi syarat ZDR. Pengecualiannya adalah Claude Code yang digunakan melalui Claude Enterprise dengan ZDR diaktifkan; lihat [Apa yang dicakup ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#what-zdr-covers).
* **Claude for Excel:** Saat ini tidak memenuhi syarat ZDR.
* **Claude Fable 5 dan Claude Mythos 5:** Model ini memerlukan retensi data 30 hari dan tidak tersedia di bawah ZDR. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* **Integrasi pihak ketiga:** Data yang diproses oleh situs web, alat, atau integrasi pihak ketiga lainnya tidak dicakup, meskipun beberapa mungkin memiliki penawaran serupa. Tinjau praktik penanganan data masing-masing layanan.
* **Cross-Origin Resource Sharing (CORS):** CORS tidak didukung untuk organisasi dengan pengaturan ZDR. Untuk melakukan panggilan API dari aplikasi berbasis browser, rutekan permintaan melalui server proxy backend. Lihat [panduan keamanan API](https://platform.claude.com/docs/id/api/overview) untuk pola proxy dan penanganan kunci API.
* **Konten yang ditandai dan penahanan hukum:** Lihat [Retensi terlepas dari pengaturan](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#retention-regardless-of-arrangement).

<Note>
  Untuk informasi terkini tentang produk dan fitur mana yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kesiapan HIPAA

Claude API mendukung integrasi siap HIPAA untuk organisasi yang menangani "protected health information" (informasi kesehatan yang dilindungi), atau PHI. Dengan BAA yang ditandatangani dan organisasi yang mengaktifkan HIPAA, Anda dapat menggunakan fitur API yang didukung untuk memproses PHI sambil mendukung kepatuhan HIPAA organisasi Anda. Organisasi yang memenuhi syarat dapat meninjau dan menandatangani BAA serta mengaktifkan kesiapan HIPAA langsung dari Claude Console. Kesiapan HIPAA menerapkan serangkaian perlindungan privasi dan keamanan yang lebih luas daripada ZDR (enkripsi, kontrol akses, dan pencatatan audit yang melindungi PHI sepanjang siklus hidupnya) alih-alih mengharuskan penghapusan segera. Jika organisasi Anda menangani PHI, kesiapan HIPAA adalah pengaturan yang harus digunakan; Anda tidak perlu ZDR juga. Lihat [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) untuk fitur mana yang dicakup masing-masing pengaturan.

<Note>
  Halaman ini mencakup kesiapan HIPAA untuk Claude API. Untuk Panduan Implementasi HIPAA lengkap yang mencakup Claude Enterprise dan persyaratan konfigurasi, lihat [Anthropic Trust Center](https://trust.anthropic.com/resources).
</Note>

### Apa yang dicakup kesiapan HIPAA

* **Claude API:** Kesiapan HIPAA berlaku untuk Claude API (`api.anthropic.com`) bagi fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

### Apa yang tidak dicakup kesiapan HIPAA

* **Produk konsumen Claude:** Paket Claude Free, Pro, dan Max.
* **Claude Console:** Penggunaan melalui antarmuka Claude Console (mengaktifkan kesiapan HIPAA dari pengaturan Console didukung; memproses PHI melalui Console tidak dicakup).
* **Platform yang dioperasikan mitra:** Amazon Bedrock dan Google Cloud's Agent Platform. Lihat dokumentasi kepatuhan platform tersebut.
* **Claude Platform on AWS dan Microsoft Foundry:** Kesiapan HIPAA tidak tersedia di platform ini.
* **Integrasi pihak ketiga:** Data yang diproses oleh alat atau layanan eksternal yang terhubung ke aplikasi Anda.
* **Claude Code:** Claude Code tidak dicakup di bawah kesiapan HIPAA.
* **Fitur beta:** Fitur dalam beta umumnya tidak dicakup di bawah BAA kecuali secara eksplisit tercantum sebagai memenuhi syarat dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
* **Konten yang ditandai dan penahanan hukum:** Lihat [Retensi terlepas dari pengaturan](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#retention-regardless-of-arrangement).

### Pedoman penanganan PHI

Protected health information (PHI) mencakup informasi kesehatan apa pun yang dapat diidentifikasi secara individual. Dalam konteks Claude API, PHI biasanya muncul dalam konten pesan (prompt dan respons Claude), file terlampir (gambar, PDF), dan nama file atau metadata yang terkait dengan konten pesan. Bidang berikut tidak diharapkan berisi PHI di bawah BAA: nama workspace, informasi pengguna (nama, email, nomor telepon), data penagihan, dan tiket dukungan.

Saat menggunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau alat dengan `strict: true`, API mengompilasi skema JSON menjadi grammar yang di-cache secara terpisah dari konten pesan. Skema yang di-cache ini tidak menerima perlindungan PHI yang sama dengan prompt dan respons. **Jangan sertakan PHI dalam definisi skema JSON.** Pembatasan ini berlaku untuk nama properti skema, nilai `enum`, nilai `const`, dan ekspresi reguler `pattern`. Informasi khusus pasien hanya boleh muncul dalam konten pesan, di mana informasi tersebut dilindungi di bawah perlindungan HIPAA.

### Penanganan error HIPAA

BAA yang Anda tandatangani adalah sumber kebenaran resmi untuk fitur mana yang dicakup. API juga menegakkan pembatasan ini secara otomatis. Ketika organisasi yang mengaktifkan HIPAA mengirim permintaan yang menyertakan fitur yang tidak memenuhi syarat, API mengembalikan error `400` untuk mencegah penggunaan tidak sengaja atas fitur yang tidak dicakup oleh BAA Anda:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

Pesan error mencantumkan fitur yang tidak memenuhi syarat yang terdeteksi dalam permintaan; hapus fitur tersebut dan coba lagi. Frasa "without Zero Data Retention" adalah kata-kata API sendiri dan tidak mengubah penyelesaiannya.

### Memulai dengan kesiapan HIPAA

Ada dua cara untuk menyiapkan akses API siap HIPAA. Sebagian besar organisasi dapat mengaktifkannya langsung di Claude Console dengan BAA standar Anthropic; organisasi yang memerlukan BAA yang dinegosiasikan harus bekerja sama dengan tim akun mereka.

#### Aktifkan di Console (BAA standar)

<Steps>
  <Step title="Buka pengaturan privasi organisasi Anda">
    Di [Claude Console > Settings > Privacy](https://platform.claude.com/settings/privacy), admin organisasi dengan izin manajemen HIPAA akan melihat kartu **HIPAA compliance**. Jika organisasi Anda memenuhi syarat tetapi Anda tidak melihat opsi untuk mengaktifkan, minta admin organisasi untuk menyelesaikan langkah-langkah ini.
  </Step>

  <Step title="Tinjau dan tandatangani BAA">
    Unduh Business Associate Agreement dan Panduan Implementasi HIPAA, lalu terima perjanjian tersebut sebagai perwakilan hukum resmi organisasi Anda. Setiap langkah menjadi tersedia setelah Anda mengunduh dokumen sebelumnya, dan pengaktifan Anda terikat pada versi BAA persis yang Anda unduh.
  </Step>

  <Step title="Pengaktifan berlaku segera">
    Kontrol kesiapan HIPAA diterapkan pada organisasi Anda segera setelah Anda menerima. Setelah kesiapan HIPAA diaktifkan untuk organisasi Anda, konfigurasi tersebut bersifat permanen dan tidak dapat dinonaktifkan oleh administrator. API secara otomatis menegakkan pembatasan fitur, mengembalikan error untuk permintaan yang menggunakan fitur yang tidak memenuhi syarat. Lihat [Penanganan error HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-error-handling).
  </Step>
</Steps>

#### Hubungi penjualan (BAA kustom)

Jika organisasi Anda memerlukan BAA yang dinegosiasikan atau kustom, atau jika pengaktifan mandiri tidak tersedia untuk organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales). Anthropic akan menandatangani BAA dan mengaktifkan kesiapan HIPAA untuk organisasi Anda.

#### Bangun dengan fitur yang memenuhi syarat

Jalur mana pun yang Anda gunakan, konfirmasikan fitur mana yang didukung dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) dan tinjau [pedoman penanganan PHI](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#phi-handling-guidelines) untuk fitur yang membatasi di mana PHI dapat muncul. Untuk persyaratan konfigurasi dan kepatuhan terperinci, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).

<Warning>
  Kesiapan HIPAA ditegakkan di tingkat organisasi. Jika Anda memerlukan akses API siap HIPAA dan akses API tujuan umum, gunakan organisasi terpisah untuk masing-masing.
</Warning>

## Persyaratan retensi data khusus model

Claude Fable 5 dan Claude Mythos 5 ditetapkan sebagai Covered Models (lihat [artikel dukungan Covered Models](https://support.claude.com/en/articles/15425695)) dan memerlukan retensi data 30 hari; oleh karena itu ZDR tidak tersedia untuk kedua model tersebut. Pada Claude API, permintaan ke Claude Fable 5 dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini mengembalikan `400 invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "In order to access this model, your organization or workspace must have data retention enabled."
  }
}
```

Persyaratan retensi data 30 hari berlaku di mana pun Covered Models ditawarkan. Pada Claude API (termasuk Claude Platform on AWS), Anthropic menangani data yang disimpan. Pada Amazon Bedrock dan Google Cloud's Agent Platform, data yang disimpan tetap berada dalam lingkungan penyedia cloud Anda; tinjau dokumentasi masing-masing platform untuk langkah pengaktifan.

### Aktifkan retensi 30 hari untuk workspace

Organisasi dengan pengaturan ZDR dapat membuat Claude Fable 5 dan Claude Mythos 5 tersedia di workspace tertentu dengan mengaktifkan retensi 30 hari hanya untuk workspace tersebut. Workspace lain dalam organisasi tetap menggunakan retensi data nol.

<Steps>
  <Step title="Buka kontrol privasi workspace">
    Di [Claude Console > Settings > Workspaces](https://platform.claude.com/settings/workspaces), pilih workspace dan buka tab **Privacy controls**.
  </Step>

  <Step title="Aktifkan retensi data 30 hari">
    Aktifkan pengaturan retensi data 30 hari untuk workspace tersebut.
  </Step>

  <Step title="Verifikasi">
    Permintaan ke Claude Fable 5 dan Claude Mythos 5 dari workspace ini sekarang berhasil. Workspace tanpa override tetap mengikuti default organisasi.
  </Step>
</Steps>

## Kelayakan fitur

Tabel berikut mencantumkan fitur Claude API mana yang memenuhi syarat untuk pengaturan ZDR dan kesiapan HIPAA.

Setiap kolom kelayakan menggunakan tiga nilai:

* **Ya:** Fitur sepenuhnya memenuhi syarat di bawah pengaturan tersebut. Untuk ZDR, "Ya" juga mengasumsikan Anda menggunakan model yang tidak memerlukan retensi data 30 hari; [Covered Models](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) tidak tersedia di bawah ZDR terlepas dari kelayakan fitur.
* **Ya (bersyarat):** Prompt Anda dan output Claude tidak disimpan, tetapi artefak teknis terbatas (disebutkan di kolom Detail) disimpan sebentar agar fitur berfungsi. Lihat [Bagaimana Anthropic mendekati retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#how-anthropic-approaches-data-retention) untuk komitmen yang mengatur fitur-fitur ini.
* **Tidak:** Fitur tidak memenuhi syarat. Di bawah kesiapan HIPAA, API memblokir permintaan yang menyertakan fitur "Tidak" dan mengembalikan error `400`. Di bawah ZDR, API **tidak** memblokir fitur-fitur ini; menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data spesifik tersebut, dan kebijakan retensi terdokumentasi milik fitur itu sendiri yang berlaku. Fitur yang ditandai "Tidak" untuk ZDR biasanya bersifat stateful (menyimpan job, file, atau status container), itulah sebabnya fitur tersebut tidak dapat memiliki retensi nol.

| Fitur                                                                                                                       | Endpoint                                         | Memenuhi syarat ZDR                                    | Memenuhi syarat HIPAA                  | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows)                           | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                         | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool)                                  | `/v1/messages` (dengan alat `advisor`)           | <Eligible>Ya</Eligible>                                | <Eligible status="no">Tidak</Eligible> | Output model advisor dikembalikan dalam respons API; tidak ada yang disimpan di sisi server setelah respons.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Agent skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview)                                  | `/v1/messages` (dengan `skills`) / `/v1/skills`  | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Data skill disimpan sesuai kebijakan standar. Lihat [Agent skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)                                        | `/v1/messages` (dengan alat `bash`)              | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Alat sisi klien yang dieksekusi di lingkungan Anda.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Batch processing](https://platform.claude.com/docs/id/build-with-claude/batch-processing)                                  | `/v1/messages/batches`                           | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Retensi 29 hari; penyimpanan asinkron diperlukan. Lihat [Batch processing](https://platform.claude.com/docs/id/build-with-claude/batch-processing#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [Cache diagnostics](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics)                                | `/v1/messages` (dengan `diagnostics`)            | <Eligible status="qualified">Ya (bersyarat)</Eligible> | <Eligible status="no">Tidak</Eligible> | Prompt Anda dan output Claude tidak disimpan. Sidik jari berupa hash kriptografis dan estimasi jumlah token disimpan sebentar untuk memungkinkan perbandingan dengan permintaan berikutnya. Lihat [Cache diagnostics](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#data-retention).                                                                                                                                                                                                                                                                                                                  |
| [Citations](https://platform.claude.com/docs/id/build-with-claude/citations)                                                | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)                                        | `/v1/agents`, `/v1/sessions`, `/v1/environments` | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Sesi adalah sumber daya stateful; transkrip tetap ada hingga Anda menghapusnya. Berlaku untuk semua sub-fitur Managed Agents, termasuk [Self-hosted sandboxes](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).                                                                                                                                                                                                                                                                                                                                                                                       |
| [Code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)                         | `/v1/messages` (dengan alat `code_execution`)    | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Data container disimpan hingga 30 hari. Lihat [Code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [Computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool)                             | `/v1/messages` (dengan alat `computer`)          | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Alat sisi klien di mana tangkapan layar dan file ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Lihat [Computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention).                                                                                                                                                                                                                                                                                                                                                                                         |
| [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing)                                    | `/v1/messages` (dengan `context_management`)     | <Eligible>Ya</Eligible>                                | <Eligible status="no">Tidak</Eligible> | Pengeditan konteks (pembersihan penggunaan alat dan pembersihan thinking) diterapkan secara real time.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [Context management (compaction)](https://platform.claude.com/docs/id/build-with-claude/compaction)                         | `/v1/messages` (dengan `context_management`)     | <Eligible>Ya</Eligible>                                | <Eligible status="no">Tidak</Eligible> | Hasil compaction sisi server dikembalikan dan dikirim bolak-balik secara stateless melalui respons API.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Data residency](https://platform.claude.com/docs/id/manage-claude/data-residency)                                          | `/v1/messages` (dengan `inference_geo`)          | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                                      | `/v1/messages` (dengan `effort`)                 | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode)                                                | `/v1/messages` (dengan `speed: "fast"`)          | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [Files API](https://platform.claude.com/docs/id/build-with-claude/files)                                                    | `/v1/files`                                      | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | File disimpan hingga dihapus secara eksplisit atau mencapai masa kedaluwarsa yang dikonfigurasi. Lihat [Files API](https://platform.claude.com/docs/id/build-with-claude/files#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Fine-grained tool streaming](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming)    | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [MCP connector](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector)                                         | `/v1/messages` (dengan `mcp_servers`)            | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Data disimpan sesuai kebijakan standar. Lihat [MCP connector](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview)                                    | `/v1/tunnels`                                    | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Pratinjau riset. Lihat [keamanan MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security) untuk batas aliran data dan detail subprosesor.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [Alat memory](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)                                    | `/v1/messages` (dengan alat `memory`)            | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Penyimpanan memori sisi klien di mana Anda mengontrol retensi data.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)                                 | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Panggilan API standar untuk menghasilkan respons Claude.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) | `/v1/messages` (dengan pesan `role: "system"`)   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Kemampuan bentuk permintaan dari Messages API; pesan sistem di tengah percakapan mengalir melalui jalur inferensi standar dan tidak ada yang disimpan di sisi server setelah respons.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)                                           | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Kelayakan HIPAA berlaku untuk PDF yang dikirim inline melalui Messages API, bukan melalui Files API.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Programmatic tool calling](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)        | `/v1/messages` (dengan alat `code_execution`)    | <Eligible status="no">Tidak</Eligible>                 | <Eligible status="no">Tidak</Eligible> | Dibangun di atas container code execution; data disimpan hingga 30 hari. Lihat [Programmatic tool calling](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention).                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)                                      | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Prompt Anda dan output Claude tidak disimpan. Representasi KV cache dan hash kriptografis disimpan dalam memori selama TTL cache dan segera dihapus setelah kedaluwarsa. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#data-retention).                                                                                                                                                                                                                                                                                                                                           |
| [Search results](https://platform.claude.com/docs/id/build-with-claude/search-results)                                      | `/v1/messages` (dengan sumber `search_results`)  | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)                              | `/v1/messages`                                   | <Eligible status="qualified">Ya (bersyarat)</Eligible> | <Eligible>Ya</Eligible>                | Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang di-cache, hingga 24 jam sejak penggunaan terakhir. Ini juga mencakup [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) (`strict: true` pada alat), yang menggunakan pipeline grammar yang sama. PHI tidak boleh disertakan dalam definisi skema JSON; lihat [pedoman penanganan PHI](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#phi-handling-guidelines). Lihat [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#data-retention). |
| [Alat text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)                          | `/v1/messages` (dengan alat `text_editor`)       | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Alat sisi klien yang dieksekusi di lingkungan Anda.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                  | `/v1/messages` (dengan `thinking`)               | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting)                                      | `/v1/messages/count_tokens`                      | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Hitung token sebelum mengirim permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [Tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)                               | `/v1/messages` (dengan alat `tool_search`)       | <Eligible>Ya</Eligible>                                | <Eligible status="no">Tidak</Eligible> | Alat sisi server yang dieksekusi oleh Anthropic; definisi alat dalam permintaan dicari dalam memori per panggilan dan tidak ada yang disimpan setelah respons.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)                                   | `/v1/messages` (dengan alat `web_fetch`)         | <Eligible>Ya</Eligible>                                | <Eligible status="no">Tidak</Eligible> | Konten web yang diambil dikembalikan dalam respons API. [Dynamic filtering](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#dynamic-filtering) tidak memenuhi syarat untuk ZDR atau HIPAA. Penerbit situs web dapat menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri.                                                                                                                                                                                                                                                                  |
| [Web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)                                 | `/v1/messages` (dengan alat `web_search`)        | <Eligible>Ya</Eligible>                                | <Eligible>Ya</Eligible>                | Hasil pencarian web real-time dikembalikan dalam respons API. [Dynamic filtering](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) tidak memenuhi syarat untuk ZDR atau HIPAA.                                                                                                                                                                                                                                                                                                                                                                                                  |

## Retensi terlepas dari pengaturan

Bahkan dengan pengaturan ZDR atau HIPAA yang berlaku, Anthropic dapat menyimpan data jika diwajibkan oleh hukum atau jika data tersebut telah ditandai oleh sistem kepercayaan dan keamanan otomatis Anthropic. Akibatnya, jika suatu chat atau sesi ditandai, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Bagaimana saya tahu apakah organisasi saya memiliki pengaturan ZDR?">
    Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR yang berlaku.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan fitur yang memenuhi syarat ZDR (bersyarat) di bawah pengaturan ZDR saya?">
    Ya. Fitur-fitur ini menyimpan sekumpulan data teknis minimal yang terdokumentasi, bukan prompt Anda atau output Claude. Lihat legenda [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) untuk arti "Ya (bersyarat)" dan [Bagaimana Anthropic mendekati retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#how-anthropic-approaches-data-retention) untuk komitmen yang mengatur fitur-fitur ini.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang ditandai &#x22;Tidak&#x22; di bawah ZDR?">
    Tidak ada yang memblokir permintaan. Fitur yang ditandai "Tidak" untuk ZDR pada dasarnya bersifat stateful: Batch API menyimpan job Anda, Files API menyimpan file Anda, dan code execution berjalan di container persisten. Data untuk fitur-fitur ini disimpan sesuai kebijakan terdokumentasi fitur tersebut. Menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data spesifik tersebut.
  </Accordion>

  <Accordion title="Dapatkah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">
    Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan opsi penghapusan untuk fitur non-ZDR.
  </Accordion>

  <Accordion title="Apa perbedaan kesiapan HIPAA dengan ZDR?">
    ZDR mencegah data pelanggan disimpan dalam keadaan diam setelah respons API dikembalikan. Kesiapan HIPAA melibatkan serangkaian perlindungan privasi dan keamanan yang lebih luas yang melindungi PHI sepanjang siklus hidupnya, termasuk enkripsi, kontrol akses, dan pencatatan audit. Di bawah kesiapan HIPAA, data dapat disimpan dengan perlindungan ini alih-alih mengharuskan penghapusan segera. Kedua pengaturan mencakup kumpulan fitur yang berbeda; lihat [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
  </Accordion>

  <Accordion title="Apakah saya masih memerlukan ZDR jika saya memiliki kesiapan HIPAA?">
    Tidak. Akses API siap HIPAA dirancang sebagai alternatif ZDR untuk organisasi yang menangani PHI. Dengan kesiapan HIPAA diaktifkan, Anda mendapatkan akses ke fitur API yang didukung sambil mempertahankan perlindungan privasi dan keamanan yang diwajibkan HIPAA.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat di bawah HIPAA?">
    API mengembalikan error `400` dengan tipe `invalid_request_error`. Pesan error mengidentifikasi fitur mana yang tidak tersedia. Hapus fitur yang tidak memenuhi syarat dari permintaan Anda dan coba lagi. Lihat [Penanganan error HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-error-handling).
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan organisasi yang sama untuk beban kerja HIPAA dan non-HIPAA?">
    Tidak. Kesiapan HIPAA ditegakkan di tingkat organisasi dan secara otomatis memblokir semua fitur yang tidak memenuhi syarat. Gunakan organisasi terpisah untuk beban kerja yang tidak memerlukan kesiapan HIPAA.
  </Accordion>

  <Accordion title="Bagaimana cara meminta akses API siap HIPAA?">
    Organisasi yang memenuhi syarat dapat mengaktifkan kesiapan HIPAA langsung di [Claude Console > Settings > Privacy](https://platform.claude.com/settings/privacy) dengan meninjau dan menandatangani BAA standar Anthropic; lihat [Memulai dengan kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#getting-started-with-hipaa-readiness). Jika organisasi Anda memerlukan BAA yang dinegosiasikan, atau pengaktifan mandiri tidak tersedia untuk organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).
  </Accordion>

  <Accordion title="Apakah ini berlaku untuk Amazon Bedrock atau Google Cloud?">
    Tidak. Pengaturan ZDR dan HIPAA yang dijelaskan di halaman ini berlaku untuk Claude API, di mana Anthropic adalah pemroses data. Pada Bedrock dan Google Cloud, penyedia cloud adalah pemroses data; lihat kebijakan retensi data dan kepatuhan platform tersebut untuk kontrol yang setara.
  </Accordion>

  <Accordion title="Apakah Claude Platform on AWS memenuhi syarat untuk ZDR atau kesiapan HIPAA?">
    Claude Platform on AWS mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya. Kesiapan HIPAA tidak tersedia di Claude Platform on AWS. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk detail.
  </Accordion>

  <Accordion title="Apakah Claude Code memenuhi syarat untuk ZDR?">
    Claude Code memenuhi syarat untuk ZDR melalui dua jalur:

    * **Kunci API:** Claude Code yang digunakan dengan kunci API bayar sesuai pemakaian dari organisasi Komersial
    * **Claude Enterprise:** Claude Code yang digunakan melalui Claude Enterprise dengan ZDR diaktifkan untuk organisasi

    ZDR diaktifkan per organisasi. Setiap organisasi baru memerlukan pengaktifan ZDR secara terpisah oleh tim akun Anda. ZDR tidak otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

    Selain itu, jika Anda mengaktifkan pencatatan metrik di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat disimpan.

    Untuk detail lengkap tentang ZDR untuk Claude Code di Claude Enterprise, termasuk fitur yang dinonaktifkan dan cara meminta pengaktifan, lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention).
  </Accordion>

  <Accordion title="Apakah Claude for Excel mendukung ZDR?">
    Tidak, Claude for Excel saat ini tidak memenuhi syarat ZDR.
  </Accordion>

  <Accordion title="Bagaimana cara meminta ZDR?">
    Untuk meminta pengaturan ZDR, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Kebijakan Privasi](https://www.anthropic.com/legal/privacy)
* [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)
* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Batch processing](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Referensi Files API](https://platform.claude.com/docs/id/api/files/upload)
* [Trust Center](https://trust.anthropic.com/resources)
