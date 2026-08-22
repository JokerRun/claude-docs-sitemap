---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: bfd183bb1ff794ac77cb22017aec976c315fcc9163c16ec5710485cd5a4d6b34
---

---
title: Kunci enkripsi yang dikelola pelanggan
url: https://platform.claude.com/docs/id/manage-claude/cmek
description: Enkripsi data workspace Claude saat disimpan (at rest) dengan kunci yang Anda kendalikan.
---

```bash Learn more with the /claude-api skill in Claude Code
claude "/claude-api tell me about customer-managed encryption keys"
```

"Customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK, memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) milik Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat disimpan (at rest). Anda tetap memegang kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Penggunaan CMEK bersifat opsional. Organisasi yang memenuhi syarat dapat **memilih untuk ikut serta (opt in)** menggunakan kunci enkripsi yang dikelola pelanggan sebagai pengganti enkripsi default yang disediakan Anthropic. Untuk mengaktifkan CMEK, hubungi tim akun Anthropic Anda.

<Warning>
  **Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan**

  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data Anda yang dilindungi CMEK secara permanen. Jika Anda ragu tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  * **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau materi kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  * **Verifikasi pengenal bersifat wajib:** Memberikan akses kunci kepada principal yang salah atau dipalsukan dapat mengekspos data Anda kepada pihak yang tidak berwenang. Selalu verifikasi pengenal Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Cara kerjanya

Hanya Organization Admin (di Claude Platform) atau Owner dan Primary Owner (di Claude Enterprise) yang dapat mengonfigurasi CMEK. Di Claude Platform, CMEK dicakup per workspace dan dikonfigurasi dengan Admin API. Di Claude Enterprise, CMEK dicakup per organisasi dan dikonfigurasi di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). Di kedua produk, CMEK melindungi data yang ditulis setelah kunci Anda berlaku. Data yang sudah ada (chat, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Di Claude Platform, Anthropic merekomendasikan untuk melampirkan kunci Anda ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Jika Anda melampirkan kunci ke workspace yang sudah menerima permintaan, kunci Anda dapat memerlukan waktu hingga satu hari untuk berlaku. Data yang ditulis sebelum itu, seperti data yang sudah ada, dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang.

Peristiwa konfigurasi CMEK muncul di [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti membungkus dan membuka bungkus kunci data) tidak muncul di Compliance API; operasi tersebut muncul di log audit penyedia cloud Anda.

Anthropic memanggil layanan manajemen kunci Anda dari rentang IP publik standarnya. Jika Anda membatasi akses ke layanan manajemen kunci Anda berdasarkan IP, izinkan alamat yang tercantum di [Alamat IP](https://platform.claude.com/docs/id/api/ip-addresses).

## Prasyarat

* Izin untuk membuat kunci enkripsi dan mengelola akses kunci di akun, proyek, atau subscription yang akan menampung kunci enkripsi.
* Peran Organization Admin di Claude Console pada Claude Platform, atau peran Owner atau Primary Owner pada Claude Enterprise.
* Konfigurasi retensi data: CMEK diizinkan dengan [Zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) untuk Claude Platform maupun Claude Enterprise.

## Ketersediaan dan region

CMEK saat ini hanya tersedia di region AS, dan semua operasi enkripsi diproses di region AS.

Di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di Claude Console; endpoint API `external_keys` saat ini tidak tersedia di Claude Platform on AWS. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.

Untuk latensi minimal, pilih region yang dekat dengan infrastruktur AS milik Anthropic:

| Penyedia     | Region yang direkomendasikan |
| ------------ | ---------------------------- |
| AWS          | `us-east-2`                  |
| Google Cloud | `us-central1`, `us-east5`    |
| Azure        | `northcentralus`, `eastus2`  |

## Apa yang dilindungi CMEK

Cakupan CMEK bergantung pada produk yang Anda gunakan.

### Dienkripsi dengan kunci CMEK

**Claude Platform**

* Konten pesan, file dan lampiran (baik lampiran inline yang dikirim bersama permintaan maupun unggahan Files API), serta konfigurasi MCP dan alat.
* Data [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), termasuk konfigurasi agen, environment, webhook, serta sesi dan peristiwanya.

**Claude Enterprise**

* Konten chat, termasuk skill, plugin, dan artifact.
* Lampiran chat dan lampiran proyek.
* Claude Code di CLI, termasuk konten pesan.
* Cowork di Claude Desktop.
* Agen Office.
* Claude in Chrome.

Di kedua produk, backup dan snapshot mewarisi kunci tersebut.

### Dinonaktifkan atau dimodifikasi

Beberapa fitur dimatikan atau dimodifikasi secara substansial ketika CMEK diaktifkan. Daftar ini tidak lengkap; tinjau bersama tim Anda sebelum mengaktifkan CMEK.

**Claude Platform**

* Playground di Claude Console dinonaktifkan.
* Bagian Compliance API yang mengembalikan konten mentah, seperti prompt, respons, dan file, dinonaktifkan.
* Fitur beta dan research preview lainnya mungkin tidak dicakup oleh CMEK.

**Claude Enterprise**

* Pencarian riwayat percakapan dinonaktifkan. Judul percakapan dienkripsi, sehingga pencarian berdasarkan judul atau konten tidak mengembalikan hasil.
* Pencarian di sejumlah besar file menjadi lebih lambat.
* Analitik tertentu mengalami penurunan: analitik admin untuk skill dan konektor claude.ai (di claude.ai/analytics/usage dan melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api)), laporan cerdas Claude (di claude.ai/analytics/insights), dan metrik kontribusi Claude Code (di claude.ai/analytics/claude-code).
* Ekspor log audit dinonaktifkan.
* Signed URL untuk pertukaran file sementara dinonaktifkan. URL ini mendukung ekspor data organisasi di claude.ai dan alur file Claude Code Remote seperti pembaruan screenshot.
* [Transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) Compliance API (Cowork dan Claude Code di mesin pengguna) saat ini tidak mengembalikan konten pesan. Metadata sesi dicantumkan seperti biasa, dan endpoint pesan sesi lokal (`GET /v1/compliance/apps/sessions/local/{session_id}/messages`) mengembalikan setiap pesan dengan kontennya ditandai tidak tersedia; lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript) untuk bentuk responsnya.

### Dienkripsi dengan kunci Anthropic

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di **Settings**.

**Claude Platform**

* Data yang tidak dalam keadaan disimpan (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
* Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan bahkan jika kunci dicabut.
* Nilai [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) Claude Managed Agents, seperti token OAuth dan client secret. Nilai ini disimpan dengan enkripsi yang dikelola Anthropic, bersifat write-only, dan tidak pernah dikembalikan dalam respons API.
* [Profil pengguna](https://platform.claude.com/docs/id/api/beta/user_profiles): field `name`, `external_id`, dan `metadata` disimpan dengan enkripsi yang dikelola Anthropic, bukan kunci Anda. Jangan menyimpan data pribadi sensitif di `metadata` profil.

**Claude Enterprise**

* Claude Code Desktop, Claude Code di web, dan Claude di Slack. Anthropic merekomendasikan untuk menonaktifkan fitur mana pun dari ini yang tidak sesuai untuk kasus penggunaan Anda di konsol admin.
* Fitur beta dan research preview mungkin tidak dicakup oleh CMEK dan dapat rusak di organisasi CMEK, misalnya, Claude Security dan Claude Design.
* Ekspor data sesuai permintaan di **Settings** > **Privacy**.
* [Preferensi pribadi - bagian Instructions for Claude](https://claude.ai/new#settings/general). Ini diatur di tingkat akun dan dibagikan di semua organisasi pengguna.

Di kedua produk, data akun untuk pengguna di organisasi Anda (seperti nama, alamat email, dan foto profil) tidak dienkripsi dengan kunci Anda.

### Dukungan fitur

API dan alat Claude Platform berikut menyimpan data at rest dengan kunci Anda ketika CMEK diaktifkan:

| API                   | Alat dan fitur                                                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| Messages              | Web search                                                                                           |
| Models                | Web fetch                                                                                            |
| Files                 | Code execution                                                                                       |
| Batch                 | Alat Bash                                                                                            |
| Skills                | Alat text editor                                                                                     |
| Claude Managed Agents | Konektor MCP                                                                                         |
|                       | Structured outputs (tidak tersedia untuk model Claude Fable 5 atau Claude Mythos di organisasi CMEK) |
|                       | Alat Advisor                                                                                         |
|                       | Computer use                                                                                         |
|                       | Manajemen konteks                                                                                    |

## Preservasi terbatas di luar kunci Anda

Dalam tiga kasus yang sempit, Anthropic dapat mempreservasi catatan tertentu dengan enkripsi yang dikelola Anthropic:

* Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A).
* Risiko mendesak akan bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang akan segera terjadi).
* Pelanggaran Bagian D.4 dari [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan yang setara dalam perjanjian lain yang berlaku antara pelanggan dan Anthropic.

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservasi memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) Anthropic. Untuk setiap kejadian preservasi, peristiwa [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) yang sesuai dihasilkan dengan kode alasan yang menyampaikan tujuan preservasi tersebut. Lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keamanan (catatan yang diturunkan dari pemindaian keamanan otomatis Anthropic, seperti pengenal pola dan indikator kecocokan, bukan konten percakapan) disimpan dengan enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci.

## Keterbatasan

* **Tindakan yang tidak dapat dibatalkan:** Setelah kunci dilampirkan ke workspace, kunci tersebut tidak dapat dilepas atau ditukar. Di Claude Platform, melampirkan kunci juga mengunci pengaturan retensi data workspace: Anda tidak dapat mematikan retensi data 30 hari untuk workspace tersebut, dan kembali ke zero data retention memerlukan pembuatan workspace baru dan pemindahan lalu lintas Anda ke sana. Merotasi materi kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan migrasi data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur untuk membatalkannya.
* **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci Anda berlaku (lihat [Cara kerjanya](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works)).
* **Latensi:** Operasi yang membungkus atau membuka bungkus kunci data melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latensi pada tindakan yang membaca atau menulis data at rest.
* **Penundaan pencabutan:** Pencabutan kunci dapat memerlukan waktu hingga 1 jam (TTL cache). Permintaan yang sudah berjalan selama jendela waktu tersebut mungkin tetap berhasil.
* **Biaya KMS:** CMEK memerlukan kunci di layanan manajemen kunci pihak ketiga (AWS KMS, Google Cloud KMS, atau Azure Key Vault), yang dapat menimbulkan biaya terpisah yang ditagihkan oleh penyedia KMS Anda.

## Konfigurasikan penyedia Anda

Ikuti panduan untuk layanan manajemen kunci yang Anda gunakan.

<CardGroup cols={3}>
  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms" title="AWS KMS">
    Buat kunci AWS KMS dengan kebijakan kunci lintas akun, lalu daftarkan dan validasi.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms" title="Google Cloud KMS">
    Buat crypto key Cloud KMS, berikan akses kepada service account Anthropic, lalu daftarkan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault" title="Azure Key Vault">
    Buat kunci RSA, berikan akses kepada service principal Anthropic, lalu daftarkan dan validasi.
  </Card>
</CardGroup>
