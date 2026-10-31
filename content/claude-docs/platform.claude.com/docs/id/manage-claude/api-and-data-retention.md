---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/api-and-data-retention
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 6085ce067d9b4a952ebca4a9927137d9d06e698803f5d3551762d72a7587aa3c
---

---
title: API dan retensi data
url: https://platform.claude.com/docs/id/manage-claude/api-and-data-retention
description: Pelajari bagaimana API Anthropic dan fitur-fitur terkait menyimpan data, termasuk informasi tentang zero data retention (ZDR) dan akses API yang siap HIPAA.
---

Halaman ini mencakup Claude API (`api.anthropic.com`), Claude Platform on AWS, [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), dan [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), di mana Anthropic adalah pemroses data. Di Amazon Bedrock dan Claude Models on Google Cloud (Google managed), penyedia cloud adalah pemroses data; lihat dokumentasi retensi data dan kepatuhan platform tersebut untuk kontrol yang setara.

Anthropic menawarkan dua pengaturan penanganan data untuk Claude API: [“zero data retention” (retensi data nol), atau ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) dan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness). [Tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) mencantumkan fitur API mana yang dicakup oleh setiap pengaturan. Untuk kebijakan retensi standar Anthropic di luar pengaturan ini, lihat [kebijakan retensi data komersial](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

## Bagaimana Anthropic menangani retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan yang berbeda. Jika suatu fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, fitur tersebut mungkin memenuhi syarat untuk ZDR. Jika suatu fitur memang harus menyimpan data, Anthropic merancangnya dengan jejak retensi sekecil mungkin berdasarkan komitmen berikut:

* Data yang disimpan tidak pernah digunakan untuk pelatihan model tanpa izin tegas dari Anda.
* Hanya data yang secara teknis diperlukan agar fitur berfungsi yang disimpan. Konten percakapan (prompt Anda dan output Claude) tidak disimpan secara default; pengecualiannya adalah [Covered Models](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements), yang memerlukan retensi 30 hari.
* Data yang disimpan dihapus berdasarkan “time to live” (masa berlaku), atau TTL, sesingkat mungkin secara praktis, dan Anthropic berupaya memberikan kendali kepada pelanggan atas berapa lama data disimpan. Apa yang disimpan, dan durasi retensi jika TTL tertentu berlaku, didokumentasikan di halaman masing-masing fitur.

Beberapa model retensi berada di luar pengaturan ZDR dan HIPAA yang dijelaskan di halaman ini. Data yang dapat diakses melalui [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) mengikuti model retensinya sendiri. [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) menyimpan data selama 6 tahun. Konten obrolan, file, dan proyek dari claude.ai mengikuti kebijakan retensi organisasi Anda yang diatur di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), kecuali pengguna menghapusnya lebih awal. [Transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) (dari sesi di mesin pengguna, dalam aplikasi seperti Cowork dan Claude Code) disimpan selama 6 tahun secara default, atau selama periode retensi percakapan kustom organisasi Anda jika periode terbatas ditetapkan (pengaturan claude.ai yang sama). [Transkrip sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) (Cowork di cloud) disimpan selama 6 tahun, kecuali pengguna menghapus sesi tersebut lebih awal. Compliance API tidak merekam sesi lokal yang memberlakukan ZDR. Untuk organisasi yang mengaktifkan kesiapan HIPAA, Compliance API hanya merekam sesi lokal Cowork dan Claude Code serta menyimpan transkripnya selama 30 hari.

## Zero data retention (ZDR)

Dalam pengaturan ZDR, Anthropic tidak menyimpan prompt atau respons pelanggan saat tidak aktif (at rest) setelah respons API dikembalikan. Untuk meminta ZDR bagi organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales). ZDR diaktifkan per organisasi; setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda, dan pengaktifan tidak otomatis berlaku untuk organisasi lain di bawah akun yang sama.

### Apa yang dicakup ZDR

* **Claude Messages API dan Token Counting API:** ZDR berlaku untuk endpoint ini bagi fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility). Fitur yang menggunakan `/v1/messages` tetapi ditandai “Tidak” dalam tabel (seperti eksekusi kode) tidak tercakup.
* **Claude Code dengan kunci API:** ZDR berlaku ketika Claude Code digunakan dengan kunci API dari organisasi Komersial (organisasi di bawah Ketentuan Layanan Komersial Anthropic, berbeda dari akun Claude konsumen). Jika pencatatan metrik diaktifkan di Claude Code, data produktivitas seperti statistik penggunaan dikecualikan dari ZDR dan dapat disimpan. Claude Code di Claude Enterprise tidak tercakup oleh pengaturan ini dan memiliki penawaran ZDR tersendiri; lihat [Apa yang tidak dicakup ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#what-zdr-does-not-cover).
* **Claude Platform on AWS:** [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya.
* **Claude Models on Google Cloud (Anthropic managed):** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya.

### Apa yang tidak dicakup ZDR

* **Claude Console:** Setiap penggunaan di Claude Console, termasuk playground.
* **Claude Managed Agents:** Claude Managed Agents adalah sumber daya stateful; transkrip sesi tetap tersimpan hingga Anda menghapusnya.
* **Produk konsumen Claude:** Paket Claude Free, Pro, Max, dan Ultra, termasuk ketika pelanggan pada paket tersebut menggunakan aplikasi web, desktop, atau seluler Claude atau Claude Code.
* **Antarmuka produk Claude Teams dan Claude Enterprise:** Antarmuka ini tidak memenuhi syarat ZDR. Satu-satunya pengecualian adalah Claude Code di Claude Enterprise, yang memiliki penawaran ZDR tersendiri, terpisah dari pengaturan ZDR yang dijelaskan di halaman ini. Penawaran tersebut hanya tersedia untuk akun yang memenuhi syarat di Claude Enterprise dan memerlukan pengaktifan terpisah oleh Anthropic. Lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention), yang hanya berlaku untuk organisasi Claude Enterprise.
* **Claude for Excel:** Saat ini tidak memenuhi syarat ZDR.
* **Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, dan Claude Mythos 5:** Model-model ini memerlukan retensi data 30 hari dan tidak tersedia di bawah ZDR kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* **Integrasi pihak ketiga:** Data yang diproses oleh situs web, alat, atau integrasi pihak ketiga lainnya tidak tercakup, meskipun beberapa mungkin memiliki penawaran serupa. Tinjau praktik penanganan data dari setiap layanan.
* **Cross-Origin Resource Sharing (CORS):** CORS tidak didukung untuk organisasi dengan pengaturan ZDR. Untuk melakukan panggilan API dari aplikasi berbasis browser, arahkan permintaan melalui server proxy backend. Lihat [panduan keamanan API](https://platform.claude.com/docs/id/api/overview) untuk pola proxy dan penanganan kunci API.
* **Konten yang ditandai dan penahanan hukum:** Lihat [Retensi terlepas dari pengaturan](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#retention-regardless-of-arrangement).

<Note>
  Untuk informasi terbaru tentang produk dan fitur mana yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kesiapan HIPAA

Claude API mendukung integrasi yang siap HIPAA untuk organisasi yang menangani “protected health information” (informasi kesehatan yang dilindungi), atau PHI. Dengan BAA yang telah ditandatangani dan organisasi yang mengaktifkan HIPAA, Anda dapat menggunakan fitur API yang didukung untuk memproses PHI sambil mendukung kepatuhan HIPAA organisasi Anda. Organisasi yang memenuhi syarat dapat meninjau dan menandatangani BAA serta mengaktifkan kesiapan HIPAA langsung dari Claude Console. Kesiapan HIPAA menerapkan serangkaian perlindungan privasi dan keamanan yang lebih luas daripada ZDR (enkripsi, kontrol akses, dan pencatatan audit yang melindungi PHI sepanjang siklus hidupnya) alih-alih mewajibkan penghapusan segera. Jika organisasi Anda menangani PHI, kesiapan HIPAA adalah pengaturan yang harus digunakan; Anda tidak memerlukan ZDR juga. Lihat [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) untuk fitur mana yang dicakup oleh setiap pengaturan.

<Note>
  Halaman ini membahas kesiapan HIPAA untuk Claude API. Untuk Panduan Implementasi HIPAA lengkap yang mencakup Claude Enterprise dan persyaratan konfigurasi, lihat [Anthropic Trust Center](https://trust.anthropic.com/resources).
</Note>

### Apa yang dicakup kesiapan HIPAA

* **Claude API:** Kesiapan HIPAA berlaku untuk Claude API (`api.anthropic.com`) bagi fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
* **Claude in Microsoft Foundry:** [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) (Hosted on Anthropic atau Hosted on Azure) adalah layanan yang memenuhi syarat bagi pelanggan yang memiliki BAA dengan Anthropic serta konfigurasi HIPAA yang diaktifkan pada langganan Azure. Minta konfigurasi HIPAA melalui tim akun Anthropic Anda. Untuk persyaratan dan fitur yang tercakup, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).

### Apa yang tidak dicakup kesiapan HIPAA

* **Produk konsumen Claude:** Paket Claude Free, Pro, Max, dan Ultra.
* **Claude Console:** Penggunaan melalui antarmuka Claude Console (mengaktifkan kesiapan HIPAA dari pengaturan Console didukung; memproses PHI melalui Console tidak tercakup).
* **Platform yang dioperasikan mitra:** Amazon Bedrock dan Google Cloud’s Agent Platform. Lihat dokumentasi kepatuhan platform tersebut.
* **Claude Platform on AWS:** Kesiapan HIPAA tidak tersedia di Claude Platform on AWS.
* **Integrasi pihak ketiga:** Data yang diproses oleh alat atau layanan eksternal yang terhubung ke aplikasi Anda.
* **Claude Code:** Claude Code tidak tercakup dalam kesiapan HIPAA.
* **Fitur beta:** Fitur dalam tahap beta umumnya tidak tercakup dalam BAA kecuali secara eksplisit dicantumkan sebagai memenuhi syarat dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
* **Konten yang ditandai dan penahanan hukum:** Lihat [Retensi terlepas dari pengaturan](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#retention-regardless-of-arrangement).

### Panduan penanganan PHI

Informasi kesehatan yang dilindungi (PHI) mencakup setiap informasi kesehatan yang dapat mengidentifikasi individu. Dalam konteks Claude API, PHI biasanya muncul dalam konten pesan (prompt dan respons Claude), file lampiran (gambar, PDF), serta nama file atau metadata yang terkait dengan konten pesan. Kolom-kolom berikut tidak diharapkan berisi PHI berdasarkan BAA: nama workspace, informasi pengguna (nama, email, nomor telepon), data penagihan, dan tiket dukungan.

Saat menggunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau alat dengan `strict: true`, API mengompilasi skema JSON menjadi grammar yang di-cache secara terpisah dari konten pesan. Skema yang di-cache ini tidak menerima perlindungan PHI yang sama dengan prompt dan respons. **Jangan sertakan PHI dalam definisi skema JSON.** Pembatasan ini berlaku untuk nama properti skema, nilai `enum`, nilai `const`, dan ekspresi reguler `pattern`. Informasi spesifik pasien sebaiknya hanya muncul dalam konten pesan, tempat informasi tersebut dilindungi oleh perlindungan HIPAA.

### Penanganan error HIPAA

BAA yang telah Anda tandatangani adalah sumber kebenaran resmi untuk fitur mana yang tercakup. API juga memberlakukan pembatasan ini secara otomatis. Ketika organisasi yang mengaktifkan HIPAA mengirim permintaan yang menyertakan fitur yang tidak memenuhi syarat, API mengembalikan error `400` untuk mencegah penggunaan fitur yang tidak tercakup oleh BAA Anda secara tidak sengaja:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

Pesan error mencantumkan fitur tidak memenuhi syarat yang terdeteksi dalam permintaan; hapus fitur tersebut dan coba lagi. Frasa “without Zero Data Retention” adalah kata-kata API itu sendiri dan tidak mengubah penyelesaiannya. Alat sisi klien yang kolom Detailnya dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) menyatakan tidak diblokir akan diterima tetapi tetap berada di luar kesiapan HIPAA.

### Memulai dengan kesiapan HIPAA

Ada dua cara untuk menyiapkan akses API yang siap HIPAA. Sebagian besar organisasi dapat mengaktifkannya langsung di Claude Console dengan BAA standar Anthropic; organisasi yang memerlukan BAA hasil negosiasi sebaiknya bekerja sama dengan tim akun mereka.

#### Aktifkan di Console (BAA standar)

<Steps>
  <Step title="Buka pengaturan retensi data organisasi Anda">
    Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) (`platform.claude.com/settings/privacy`). Admin organisasi dengan izin pengelolaan HIPAA akan melihat kartu **HIPAA compliance** di sana. Jika Anda tidak melihat kartu tersebut, pilih **Organization** dari menu dropdown di bagian atas halaman. Jika organisasi Anda memenuhi syarat tetapi Anda masih tidak melihat opsi untuk mengaktifkan, minta admin organisasi untuk menyelesaikan langkah-langkah ini.
  </Step>

  <Step title="Tinjau dan tandatangani BAA">
    Unduh Business Associate Agreement dan Panduan Implementasi HIPAA, lalu terima perjanjian tersebut sebagai perwakilan hukum resmi organisasi Anda. Setiap langkah menjadi tersedia setelah Anda mengunduh dokumen sebelumnya, dan pengaktifan Anda terikat pada versi BAA persis yang Anda unduh.
  </Step>

  <Step title="Pengaktifan langsung berlaku">
    Kontrol kesiapan HIPAA diterapkan pada organisasi Anda segera setelah Anda menerimanya. Setelah kesiapan HIPAA diaktifkan untuk organisasi Anda, konfigurasinya bersifat permanen dan tidak dapat dinonaktifkan oleh administrator. API secara otomatis memberlakukan pembatasan fitur, dengan mengembalikan error untuk permintaan yang menggunakan fitur yang tidak memenuhi syarat. Lihat [Penanganan error HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-error-handling) untuk error tersebut dan pengecualian alat sisi klien.
  </Step>
</Steps>

#### Hubungi tim penjualan (BAA kustom)

Jika organisasi Anda memerlukan BAA hasil negosiasi atau kustom, atau jika pengaktifan mandiri tidak tersedia untuk organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales). Anthropic akan menandatangani BAA dan mengaktifkan kesiapan HIPAA untuk organisasi Anda.

#### Bangun dengan fitur yang memenuhi syarat

Jalur mana pun yang Anda gunakan, pastikan fitur mana yang didukung dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) dan tinjau [panduan penanganan PHI](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#phi-handling-guidelines) untuk fitur yang membatasi di mana PHI dapat muncul. Untuk persyaratan konfigurasi dan kepatuhan yang mendetail, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).

<Warning>
  Kesiapan HIPAA diberlakukan di tingkat organisasi. Jika Anda memerlukan akses API yang siap HIPAA sekaligus akses API untuk keperluan umum, gunakan organisasi terpisah untuk masing-masing.
</Warning>

## Persyaratan retensi data khusus model

Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, dan Claude Mythos 5 ditetapkan sebagai Covered Models (lihat [artikel dukungan Covered Models](https://support.claude.com/en/articles/15425695)) dan memerlukan retensi data 30 hari; oleh karena itu ZDR tidak tersedia untuk model mana pun di antaranya kecuali diizinkan secara tegas oleh Anthropic. Di Claude API, permintaan ke Claude Fable 5 dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini akan mengembalikan `400 invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "In order to access this model, your organization or workspace must have data retention enabled."
  }
}
```

Persyaratan retensi data 30 hari berlaku di mana pun Covered Models ditawarkan. Di Claude API (termasuk Claude Platform on AWS), Anthropic menangani data yang disimpan. Di Amazon Bedrock dan Google Cloud’s Agent Platform, data yang disimpan tetap berada di dalam lingkungan penyedia cloud Anda; tinjau dokumentasi setiap platform untuk langkah-langkah pengaktifan.

### Aktifkan retensi 30 hari untuk workspace

Organisasi dengan pengaturan ZDR dapat menyediakan model-model ini di workspace tertentu dengan mengaktifkan retensi 30 hari hanya untuk workspace tersebut. Workspace lain dalam organisasi tetap menggunakan retensi data nol. Default Workspace selalu mengikuti pengaturan organisasi, jadi gunakan workspace lain.

<Steps>
  <Step title="Buka pengaturan retensi data workspace">
    Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) (`platform.claude.com/settings/privacy`) dan pilih workspace dari menu dropdown di bagian atas halaman.
  </Step>

  <Step title="Aktifkan retensi data 30 hari">
    Pilih **Standard data retention** (retensi 30 hari) dan klik **Save**. Kotak dialog konfirmasi kemudian meminta Anda untuk meninjau dan menerima ketentuan yang berlaku untuk retensi data bagi workspace tersebut. Retensi data baru aktif untuk workspace setelah Anda menerimanya.
  </Step>

  <Step title="Verifikasi">
    Permintaan ke Covered Models dari workspace ini sekarang berhasil. Workspace tanpa pengaturan override tetap mengikuti default organisasi.
  </Step>
</Steps>

## Kelayakan fitur

Tabel berikut mencantumkan fitur Claude API mana yang memenuhi syarat untuk pengaturan ZDR dan kesiapan HIPAA. Tabel-tabel ini membagi fitur dengan cara yang sama seperti [Ikhtisar fitur](https://platform.claude.com/docs/id/build-with-claude/overview).

Setiap kolom kelayakan menggunakan tiga nilai:

* **Ya:** Fitur sepenuhnya memenuhi syarat dalam pengaturan tersebut. Untuk ZDR, “Ya” juga mengasumsikan bahwa Anda menggunakan model yang tidak memerlukan retensi data 30 hari; [Covered Models](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) tidak tersedia di bawah ZDR terlepas dari kelayakan fitur.
* **Ya (bersyarat):** Prompt Anda dan output Claude tidak disimpan, tetapi artefak teknis terbatas (disebutkan di kolom Detail) disimpan sebentar agar fitur dapat berfungsi. Lihat [Bagaimana Anthropic menangani retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#how-anthropic-approaches-data-retention) untuk komitmen yang mengatur fitur-fitur ini.
* **Tidak:** Fitur tidak memenuhi syarat. Dalam kesiapan HIPAA, API memblokir permintaan yang menyertakan fitur “Tidak” dan mengembalikan error `400`, kecuali kolom Detail fitur tersebut menyatakan sebaliknya. Dalam ZDR, API **tidak** memblokir fitur-fitur ini; menggunakan salah satunya berarti memilih untuk keluar dari pengaturan ZDR Anda untuk data tertentu tersebut, dan kebijakan retensi yang didokumentasikan untuk fitur itu sendiri yang berlaku. Fitur yang ditandai “Tidak” untuk ZDR biasanya bersifat stateful (menyimpan job, file, atau status container), itulah sebabnya fitur tersebut tidak dapat memiliki retensi nol.

### Fitur platform

Fitur yang terkait dengan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) dan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview). Beberapa hanya tersedia di salah satunya. Tabel ini memberikan kelayakan setiap fitur di Messages API. Di Claude Managed Agents, tidak ada fitur yang memenuhi syarat untuk ZDR atau kesiapan HIPAA; lihat baris Claude Managed Agents di bawah [Fitur Managed Agents](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#managed-agents-features).

| Fitur                                                                                                                          | Endpoint                                           | Layak ZDR      | Layak HIPAA | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :----------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- | :------------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool)                                     | `/v1/messages` dengan alat `advisor`               | Ya             | Tidak       | Output model advisor dikembalikan dalam respons API; tidak ada yang disimpan di sisi server setelah respons.                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview)                                     | `/v1/skills`, `/v1/messages` dengan `skills`       | Tidak          | Tidak       | Data skill disimpan sesuai kebijakan standar. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview#data-retention)                                                                                                                                                                                                                                                                                                                                                                                                        |
| [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)                                     | `/v1/messages/batches`                             | Tidak          | Tidak       | Retensi 29 hari; penyimpanan asinkron diperlukan. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/batch-processing#data-retention)                                                                                                                                                                                                                                                                                                                                                                                                        |
| [Alat penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool)                      | `/v1/messages` dengan toolset `browser`            | Ya             | Tidak       | Alat sisi klien. Anthropic tidak menjalankan tindakan browser atau menyimpan konten halaman di luar penanganan API standar. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#data-retention) Tidak tercakup dalam kesiapan HIPAA; permintaan yang menyertakan alat penggunaan browser tidak diblokir.                                                                                                                                                                                                             |
| [Kutipan](https://platform.claude.com/docs/id/build-with-claude/citations)                                                     | `/v1/messages`                                     | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool)                    | `/v1/messages` dengan toolset atau alat `computer` | Ya             | Ya          | Alat sisi klien tempat screenshot dan file diambil dan disimpan di environment Anda, bukan oleh Anthropic. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention)                                                                                                                                                                                                                                                                                                                                      |
| [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency)                                             | `/v1/messages` dengan `inference_geo`              | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Effort](https://platform.claude.com/docs/id/build-with-claude/effort)                                                         | `/v1/messages` dengan `effort`                     | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode)                                                  | `/v1/messages` dengan `speed: "fast"`              | Ya             | Ya          | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Files API](https://platform.claude.com/docs/id/build-with-claude/files)                                                       | `/v1/files`                                        | Tidak          | Tidak       | File disimpan hingga dihapus secara eksplisit atau mencapai masa kedaluwarsa yang dikonfigurasi. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/files#data-retention)                                                                                                                                                                                                                                                                                                                                                                    |
| [Konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector)                                             | `/v1/messages` dengan `mcp_servers`                | Tidak          | Tidak       | Data disimpan sesuai kebijakan standar. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#data-retention)                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview)                                        | `/v1/tunnels`                                      | Tidak          | Tidak       | Research preview. Halaman keamanan Tunnel MCP menjelaskan batas aliran data dan detail subprosesor. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security)                                                                                                                                                                                                                                                                                                                                                                  |
| [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages)    | `/v1/messages` dengan pesan `role: "system"`       | Ya             | Ya          | Kapabilitas bentuk permintaan dari Messages API; pesan sistem di tengah percakapan mengalir melalui jalur inferensi standar dan tidak ada yang disimpan di sisi server setelah respons.                                                                                                                                                                                                                                                                                                                                                                                 |
| [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)                                              | `/v1/messages`                                     | Ya             | Ya          | Kelayakan HIPAA berlaku untuk PDF yang dikirim secara inline melalui Messages API, bukan melalui Files API.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Pemanggilan alat secara programatik](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | `/v1/messages` dengan alat `code_execution`        | Tidak          | Tidak       | Dibangun di atas kontainer eksekusi kode; data disimpan hingga 30 hari. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention)                                                                                                                                                                                                                                                                                                                                                                 |
| [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)                                         | `/v1/messages`                                     | Ya             | Ya          | Prompt Anda dan output Claude tidak disimpan. Representasi cache KV dan hash kriptografis disimpan di memori selama TTL cache dan segera dihapus setelah kedaluwarsa. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#data-retention)                                                                                                                                                                                                                                                                                      |
| ↳ [Diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics)                                  | `/v1/messages` dengan `diagnostics`                | Ya (bersyarat) | Tidak       | Prompt Anda dan output Claude tidak disimpan. Fingerprint berupa hash kriptografis dan estimasi jumlah token disimpan sebentar untuk memungkinkan perbandingan dengan permintaan berikutnya. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#data-retention)                                                                                                                                                                                                                                                            |
| [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results)                                        | `/v1/messages` dengan sumber `search_results`      | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs)                                 | `/v1/messages`                                     | Ya (bersyarat) | Ya          | Prompt Anda dan output Claude tidak disimpan. Hanya JSON schema yang di-cache, hingga 24 jam sejak terakhir digunakan. Ini juga mencakup penggunaan alat ketat (`strict: true` pada alat), yang menggunakan pipeline grammar yang sama. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#data-retention) PHI tidak boleh disertakan dalam definisi JSON schema; lihat panduan penanganan PHI. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#phi-handling-guidelines) |
| [Pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking)                                                    | `/v1/messages` dengan `thinking`                   | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ↳ [Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost)                        | `/v1/messages`                                     | Ya             | Ya          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Compaction ambang batas](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold)                          | `/v1/messages` dengan `context_management`         | Ya             | Tidak       | Hasil compaction sisi server dikembalikan dan dikirim bolak-balik secara stateless melalui respons API.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting)                                     | `/v1/messages/count_tokens`                        | Ya             | Ya          | Hitung token sebelum mengirim permintaan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [Alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)                          | `/v1/messages` dengan alat `tool_search`           | Ya             | Tidak       | Alat sisi server yang dijalankan oleh Anthropic; definisi alat dalam permintaan dicari di memori per panggilan dan tidak ada yang disimpan setelah respons.                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)                                 | `/v1/messages` dengan alat `web_fetch`             | Ya             | Tidak       | Konten web yang diambil dikembalikan dalam respons API. Pemfilteran dinamis untuk web fetch tidak memenuhi syarat kelayakan ZDR atau HIPAA. Penerbit situs web mungkin menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri.                                                                                                                                                                                                                                                                                    |
| [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)                            | `/v1/messages` dengan alat `web_search`            | Ya             | Ya          | Hasil pencarian web real-time dikembalikan dalam respons API. Pemfilteran dinamis untuk pencarian web tidak memenuhi syarat kelayakan ZDR atau HIPAA.                                                                                                                                                                                                                                                                                                                                                                                                                   |

### Fitur Messages API

| Fitur                                                                                                                    | Endpoint                                    | Layak ZDR | Layak HIPAA | Detail                                                                                                                                                            |
| :----------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :-------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)                                     | `/v1/messages` dengan alat `bash`           | Ya        | Ya          | Alat sisi klien yang dijalankan di environment Anda.                                                                                                              |
| [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)                  | `/v1/messages` dengan alat `code_execution` | Tidak     | Tidak       | Data kontainer disimpan hingga 30 hari. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention) |
| [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing)                              | `/v1/messages` dengan `context_management`  | Ya        | Tidak       | Edit konteks (penghapusan penggunaan alat dan penghapusan pemikiran) diterapkan secara real time.                                                                 |
| [Streaming alat fine-grained](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages`                              | Ya        | Ya          |                                                                                                                                                                   |
| [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)                                 | `/v1/messages` dengan alat `memory`         | Ya        | Ya          | Penyimpanan memori sisi klien tempat Anda mengontrol retensi data.                                                                                                |
| [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)                              | `/v1/messages`                              | Ya        | Ya          | Panggilan API standar untuk menghasilkan respons Claude.                                                                                                          |
| [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)                       | `/v1/messages` dengan alat `text_editor`    | Ya        | Ya          | Alat sisi klien yang dijalankan di environment Anda.                                                                                                              |

### Fitur Managed Agents

| Fitur                                                                                | Endpoint                                         | Layak ZDR | Layak HIPAA | Detail                                                                                                                                                                    |
| :----------------------------------------------------------------------------------- | :----------------------------------------------- | :-------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) | `/v1/agents`, `/v1/sessions`, `/v1/environments` | Tidak     | Tidak       | Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri. |

### Fitur lainnya

| Fitur                                                                                                                | Endpoint                                   | Layak ZDR                              | Layak HIPAA                            | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [“Context window” (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) | `/v1/messages`                             | <Eligible>Ya</Eligible>                | <Eligible>Ya</Eligible>                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Ekspor OpenTelemetry](https://platform.claude.com/docs/id/manage-claude/opentelemetry)                              | `/v1/organizations/telemetry_destinations` | <Eligible>Ya</Eligible>                | <Eligible status="no">Tidak</Eligible> | Beta. Span memiliki kelayakan ZDR yang sama dengan fitur yang menghasilkannya. Organisasi HIPAA dapat mengekspor metadata. Span SDK dikirim langsung dari lingkungan Anda ke exporter Anda. Setelah dikirim, data disimpan oleh layanan yang Anda pilih, di luar Anthropic, di bawah kontrol retensi dan akses layanan tersebut.                                                                                                                                                                                                                                                            |
| [Profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles)                                   | `/v1/user_profiles`                        | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Profil adalah metadata tentang pelanggan akhir Anda dan tidak berisi prompt atau output. Data profil yang Anda kirim disimpan sesuai kebijakan standar hingga Anda menghapus profil tersebut. Organisasi yang mengaktifkan HIPAA dapat menggunakan profil pengguna, tetapi API profil pengguna bukan layanan yang memenuhi syarat HIPAA dan PHI tidak boleh disertakan dalam data profil yang Anda kirim. Lihat [Apa isi profil dan bagaimana Anthropic menggunakannya](https://platform.claude.com/docs/id/manage-claude/user-profiles#what-a-profile-contains-and-how-anthropic-uses-it). |

## Retensi terlepas dari pengaturan

Bahkan dengan pengaturan ZDR atau HIPAA yang berlaku, Anthropic dapat menyimpan data jika diwajibkan oleh hukum atau jika data tersebut telah ditandai oleh sistem kepercayaan dan keamanan otomatis Anthropic. Akibatnya, jika suatu obrolan atau sesi ditandai, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Bagaimana saya tahu apakah organisasi saya memiliki pengaturan ZDR?">
    Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk memastikan apakah organisasi Anda memiliki pengaturan ZDR.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan fitur yang memenuhi syarat ZDR (bersyarat) dalam pengaturan ZDR saya?">
    Ya. Fitur-fitur ini menyimpan sekumpulan data teknis yang minimal dan terdokumentasi, bukan prompt Anda atau output Claude. Lihat legenda [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) untuk arti “Ya (bersyarat)” dan [Bagaimana Anthropic menangani retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#how-anthropic-approaches-data-retention) untuk komitmen yang mengatur fitur-fitur ini.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang ditandai &#x22;Tidak&#x22; di bawah ZDR?">
    Tidak ada yang memblokir permintaan tersebut. Fitur yang ditandai “Tidak” untuk ZDR pada dasarnya bersifat stateful: Batch API menyimpan job Anda, Files API menyimpan file Anda, dan eksekusi kode berjalan di container persisten. Data untuk fitur-fitur ini disimpan sesuai kebijakan yang didokumentasikan untuk fitur tersebut. Menggunakannya berarti memilih untuk keluar dari pengaturan ZDR Anda untuk data tertentu tersebut.
  </Accordion>

  <Accordion title="Dapatkah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">
    Hubungi perwakilan akun Anthropic Anda untuk membahas opsi penghapusan untuk fitur non-ZDR.
  </Accordion>

  <Accordion title="Apa perbedaan kesiapan HIPAA dengan ZDR?">
    ZDR mencegah data pelanggan disimpan saat tidak aktif (at rest) setelah respons API dikembalikan. Kesiapan HIPAA melibatkan serangkaian perlindungan privasi dan keamanan yang lebih luas yang melindungi PHI sepanjang siklus hidupnya, termasuk enkripsi, kontrol akses, dan pencatatan audit. Dalam kesiapan HIPAA, data dapat disimpan dengan perlindungan ini alih-alih mewajibkan penghapusan segera. Kedua pengaturan mencakup kumpulan fitur yang berbeda; lihat [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).
  </Accordion>

  <Accordion title="Apakah saya masih memerlukan ZDR jika saya memiliki kesiapan HIPAA?">
    Tidak. Akses API yang siap HIPAA dirancang sebagai alternatif ZDR untuk organisasi yang menangani PHI. Dengan kesiapan HIPAA diaktifkan, Anda mendapatkan akses ke fitur API yang didukung sambil mempertahankan perlindungan privasi dan keamanan yang diwajibkan oleh HIPAA.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat di bawah HIPAA?">
    API mengembalikan error `400` dengan tipe `invalid_request_error`, kecuali untuk alat sisi klien yang kolom Detailnya dalam [tabel kelayakan fitur](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) menyatakan tidak diblokir (alat tersebut diterima tetapi tetap berada di luar kesiapan HIPAA). Pesan error mengidentifikasi fitur mana yang tidak tersedia. Hapus fitur tersebut dari permintaan Anda dan coba lagi. Lihat [Penanganan error HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-error-handling).
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan organisasi yang sama untuk beban kerja HIPAA dan non-HIPAA?">
    Tidak. Kesiapan HIPAA diberlakukan di tingkat organisasi dan secara otomatis memblokir fitur yang tidak memenuhi syarat (alat sisi klien yang dicatat di kolom Detail tabel adalah pengecualiannya: alat tersebut tidak diblokir, tetapi tetap berada di luar kesiapan HIPAA). Gunakan organisasi terpisah untuk beban kerja yang tidak memerlukan kesiapan HIPAA.
  </Accordion>

  <Accordion title="Bagaimana cara meminta akses API yang siap HIPAA?">
    Organisasi yang memenuhi syarat dapat mengaktifkan kesiapan HIPAA langsung di halaman [Data retention](https://platform.claude.com/settings/privacy) (`platform.claude.com/settings/privacy`) di Claude Console dengan meninjau dan menandatangani BAA standar Anthropic; lihat [Memulai dengan kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#getting-started-with-hipaa-readiness). Jika organisasi Anda memerlukan BAA hasil negosiasi, atau pengaktifan mandiri tidak tersedia untuk organisasi Anda, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).
  </Accordion>

  <Accordion title="Apakah ini berlaku untuk Amazon Bedrock atau Google Cloud?">
    [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama, dan Anthropic adalah pemroses datanya. ZDR tersedia di sana berdasarkan permintaan. Di Amazon Bedrock dan Claude Models on Google Cloud (Google managed), penyedia cloud adalah pemroses data; lihat kebijakan retensi data dan kepatuhan platform tersebut untuk kontrol yang setara.
  </Accordion>

  <Accordion title="Apakah Claude Platform on AWS memenuhi syarat untuk ZDR atau kesiapan HIPAA?">
    Claude Platform on AWS mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya. Kesiapan HIPAA tidak tersedia di Claude Platform on AWS. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk detailnya.
  </Accordion>

  <Accordion title="Apakah Claude Code memenuhi syarat untuk ZDR?">
    Claude Code memenuhi syarat untuk ZDR melalui dua penawaran terpisah:

    * **Kunci API:** Claude Code yang digunakan dengan kunci API bayar sesuai penggunaan dari organisasi Komersial tercakup ketika organisasi tersebut memiliki pengaturan ZDR untuk Claude API, yang dijelaskan di halaman ini.
    * **Claude Enterprise:** Claude Code yang digunakan melalui Claude Enterprise tercakup oleh penawaran terpisah, yaitu ZDR untuk Claude Code di Claude Enterprise, ketika Anthropic telah mengaktifkannya untuk organisasi tersebut.

    ZDR diaktifkan berdasarkan per organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda. ZDR tidak otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

    Selain itu, jika Anda mengaktifkan pencatatan metrik di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat disimpan.

    Untuk detail lengkap tentang ZDR untuk Claude Code di Claude Enterprise, termasuk fitur yang dinonaktifkan dan cara meminta pengaktifan, lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention). Dokumentasi tersebut hanya berlaku untuk organisasi Claude Enterprise dan tidak menjelaskan pengaturan ZDR untuk Claude API.
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
* [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Referensi Files API](https://platform.claude.com/docs/id/api/files/upload)
* [Trust Center](https://trust.anthropic.com/resources)
