---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 9adee5a035bb208257003521c1109951e9844e30a91ddc9bc5c5423f8d5f52f3
---

---
title: Kunci enkripsi yang dikelola pelanggan
url: https://platform.claude.com/docs/id/manage-claude/cmek
description: Enkripsi data workspace Claude saat istirahat dengan kunci yang Anda kendalikan.
---

```bash Learn more with the /claude-api skill in Claude Code
claude "/claude-api tell me about customer-managed encryption keys"
```

Kunci enkripsi yang dikelola pelanggan (customer-managed encryption key, atau CMEK) memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat istirahat. Anda mempertahankan kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Penggunaan CMEK bersifat opsional. Organisasi yang memenuhi syarat dapat **memilih untuk ikut serta** menggunakan kunci enkripsi yang dikelola pelanggan alih-alih enkripsi default yang disediakan Anthropic. Untuk mengaktifkan CMEK, hubungi tim akun Anthropic Anda.

<Warning>
  **Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan**

  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data yang dilindungi CMEK Anda secara permanen. Jika Anda tidak yakin tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  * **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau material kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  * **Verifikasi identifier bersifat wajib:** Memberikan akses kunci kepada principal yang salah atau dipalsukan dapat mengekspos data Anda kepada pihak yang tidak berwenang. Selalu verifikasi identifier Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi. Pada Claude Platform on AWS, identitas tersebut adalah AWS service principal yang dipublikasikan dalam [panduan AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws). Jangan pernah mempercayai identifier yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Cara kerjanya

Hanya Organization Admin (pada Claude Platform; peran Admin pada Claude Platform on AWS) atau Owner dan Primary Owner (pada Claude Enterprise) yang dapat mengonfigurasi CMEK. Pada Claude Platform, CMEK dicakup per workspace dan dikonfigurasi dengan Admin API (pada Claude Platform on AWS, di Claude Console atau melalui endpoint kunci eksternal dan workspace yang diotorisasi IAM). Pada Claude Enterprise, CMEK dicakup per organisasi dan dikonfigurasi di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). Pada kedua produk, CMEK melindungi data yang ditulis setelah kunci Anda berlaku. Data yang sudah ada (chat, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Pada Claude Platform, Anthropic merekomendasikan untuk melampirkan kunci Anda ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Jika Anda melampirkan kunci ke workspace yang sudah menerima permintaan, kunci Anda dapat memerlukan waktu hingga satu hari untuk berlaku. Data yang ditulis sebelum itu, seperti data yang sudah ada, dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang.

Peristiwa konfigurasi CMEK muncul di [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti membungkus dan membuka bungkus kunci data) tidak muncul di Compliance API; mereka muncul di log audit penyedia cloud Anda.

Anthropic memanggil layanan manajemen kunci Anda dari rentang IP publik standarnya. Jika Anda membatasi akses ke layanan manajemen kunci Anda berdasarkan IP, izinkan alamat yang tercantum di [Alamat IP](https://platform.claude.com/docs/id/api/ip-addresses). Pada Claude Platform on AWS, jangan mengandalkan pembatasan berbasis IP untuk kunci Anda; cakup akses dengan kebijakan kunci yang dijelaskan dalam [panduan AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) sebagai gantinya.

## Prasyarat

* Izin untuk membuat kunci enkripsi dan mengelola akses kunci di akun, proyek, atau langganan yang akan menampung kunci enkripsi.
* Peran Organization Admin di Claude Console pada Claude Platform (peran Admin pada Claude Platform on AWS), atau peran Owner atau Primary Owner pada Claude Enterprise.
* Konfigurasi retensi data: CMEK diizinkan dengan [Zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) untuk Claude Platform dan Claude Enterprise.

## Ketersediaan dan wilayah

Kecuali pada Claude Platform on AWS (dibahas di akhir bagian ini), CMEK saat ini hanya tersedia di wilayah AS, dan semua operasi enkripsi diproses di wilayah AS. Untuk latensi minimal, pilih wilayah yang dekat dengan infrastruktur AS Anthropic:

| Penyedia     | Wilayah yang direkomendasikan |
| ------------ | ----------------------------- |
| AWS          | `us-east-2`                   |
| Google Cloud | `us-central1`, `us-east5`     |
| Azure        | `northcentralus`, `eastus2`   |

Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Rekomendasi wilayah ini tidak berlaku di sana: kunci harus berupa kunci KMS wilayah tunggal di akun dan wilayah AWS yang sama dengan workspace tempat kunci tersebut dilampirkan, dan kebijakan kuncinya harus memberikan akses ke AWS service principal alih-alih peran IAM Anthropic; lihat [Siapkan CMEK pada Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws). Daftarkan dan lampirkan kunci di Claude Console; endpoint kunci eksternal juga tersedia pada Claude Platform on AWS, diotorisasi melalui [tindakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys). Tidak ada langkah validasi terpisah: kunci divalidasi secara implisit saat Anda melampirkannya ke workspace (panggilan lampiran melakukan putaran enkripsi/dekripsi), sehingga masalah kebijakan kunci muncul pada saat pelampiran alih-alih pada saat pendaftaran.

## Apa yang dilindungi CMEK

Apa yang dicakup CMEK bergantung pada produk mana yang Anda gunakan.

### Dienkripsi dengan kunci CMEK

**Claude Platform**

* Konten pesan, file dan lampiran (baik lampiran inline yang dikirim dengan permintaan maupun unggahan Files API), serta konfigurasi MCP dan alat.
* Data [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), termasuk konfigurasi agen, lingkungan, webhook, serta sesi dan peristiwanya.

**Claude Enterprise**

* Konten chat, termasuk skills, plugin, dan artifacts.
* Lampiran chat dan lampiran proyek.
* Claude Code di CLI, termasuk konten pesan.
* Cowork di Claude Desktop.
* [Transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) Compliance API yang ditangkap dari sesi di mesin pengguna. Jika kunci Anda tidak dapat digunakan, endpoint pesan mengembalikan [503 Service Unavailable](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable) alih-alih konten transkrip. Metadata sesi tetap dicantumkan.
* Office agents.
* Claude in Chrome.

Pada kedua produk, cadangan dan snapshot mewarisi kunci.

### Dinonaktifkan atau dimodifikasi

Beberapa fitur dimatikan atau dimodifikasi secara substansial saat CMEK diaktifkan. Daftar ini tidak lengkap; tinjau bersama tim Anda sebelum mengaktifkan CMEK.

**Claude Platform**

* Playground di Claude Console dinonaktifkan.
* Bagian dari Compliance API yang mengembalikan konten mentah, seperti prompt, respons, dan file, dinonaktifkan.
* Fitur beta dan research preview lainnya mungkin tidak dicakup oleh CMEK.

**Claude Enterprise**

* Pencarian riwayat percakapan dinonaktifkan. Judul percakapan dienkripsi, sehingga pencarian berdasarkan judul atau konten tidak mengembalikan hasil.
* [Pencarian pengetahuan proyek](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects) ("retrieval-augmented generation" (pembangkitan yang ditambah pengambilan), atau RAG) dinonaktifkan. Pengetahuan proyek dimuat langsung ke dalam konteks setiap percakapan alih-alih diindeks dan dicari. Akibatnya, sebuah proyek dapat menggunakan pengetahuan yang jauh lebih sedikit daripada yang bisa dilakukannya tanpa CMEK. Pengetahuan di luar apa yang dapat dimuat ditinggalkan dari percakapan.
* Analitik tertentu menurun: analitik admin untuk skills dan konektor claude.ai (di bawah claude.ai/analytics/usage dan melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api)), laporan cerdas Claude (di bawah claude.ai/analytics/insights), dan metrik kontribusi Claude Code (di bawah claude.ai/analytics/claude-code).
* Ekspor log audit dinonaktifkan.
* URL yang ditandatangani untuk pertukaran file sementara dinonaktifkan. Ini mendukung ekspor data organisasi di claude.ai dan alur file Claude Code Remote seperti pembaruan screenshot.

### Dienkripsi dengan kunci Anthropic

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di **Settings**.

**Claude Platform**

* Data yang tidak dalam keadaan istirahat (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
* Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan bahkan jika kunci dicabut.
* Nilai [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) Claude Managed Agents, seperti token OAuth dan client secret. Ini disimpan di bawah enkripsi yang dikelola Anthropic, bersifat write-only, dan tidak pernah dikembalikan dalam respons API.
* [Profil pengguna](https://platform.claude.com/docs/id/api/beta/user_profiles): field `name`, `external_id`, dan `metadata` disimpan di bawah enkripsi yang dikelola Anthropic, bukan kunci Anda. Jangan menyimpan data pribadi sensitif di `metadata` profil.

**Claude Enterprise**

* Claude Code Desktop, Claude Code di web, dan Claude in Slack. Anthropic merekomendasikan untuk menonaktifkan salah satu dari ini yang tidak sesuai untuk kasus penggunaan Anda di konsol admin.
* Fitur beta dan research preview mungkin tidak dicakup oleh CMEK dan dapat rusak di organisasi CMEK, misalnya, Claude Security dan Claude Design.
* Ekspor data sesuai permintaan di bawah **Settings** > **Privacy**.
* [Preferensi pribadi - bagian Instructions for Claude](https://claude.ai/new#settings/general) dan instruksi Cowork Global. Ini diatur di tingkat akun dan dibagikan di semua organisasi pengguna.

Pada kedua produk, data akun untuk pengguna di organisasi Anda (seperti nama, alamat email, dan gambar profil) tidak dienkripsi dengan kunci Anda.

### Dukungan fitur

API dan alat Claude Platform berikut menyimpan data saat istirahat di bawah kunci Anda saat CMEK diaktifkan:

| API                   | Alat dan fitur                                                                                     |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| Messages              | Web search                                                                                         |
| Models                | Web fetch                                                                                          |
| Files                 | Code execution                                                                                     |
| Batch                 | Bash tool                                                                                          |
| Skills                | Text editor tool                                                                                   |
| Claude Managed Agents | MCP connector                                                                                      |
|                       | Structured outputs (tidak tersedia untuk model Claude Fable atau Claude Mythos di organisasi CMEK) |
|                       | Advisor tool                                                                                       |
|                       | Computer use                                                                                       |
|                       | Browser use                                                                                        |
|                       | Context management                                                                                 |

## Pelestarian terbatas di luar kunci Anda

Dalam tiga kasus sempit, Anthropic dapat melestarikan catatan tertentu di bawah enkripsi yang dikelola Anthropic:

* Di mana Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A).
* Risiko mendesak dari bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang akan segera terjadi).
* Pelanggaran Bagian D.4 dari [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan setara dalam perjanjian lain pelanggan yang berlaku dengan Anthropic.

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), pelestarian memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) Anthropic. Untuk setiap instance pelestarian, peristiwa [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) yang sesuai dihasilkan dengan kode alasan yang menyampaikan tujuan pelestarian. Lihat [Pelestarian konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keamanan (catatan yang berasal dari pemindaian keamanan otomatis Anthropic, seperti pengidentifikasi pola dan indikator kecocokan, bukan konten percakapan) disimpan di bawah enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci.

## Keterbatasan

* **Tindakan yang tidak dapat dibalik:** Setelah kunci dilampirkan ke workspace, kunci tidak dapat dilepas atau ditukar. Pada Claude Platform, melampirkan kunci juga mengunci pengaturan retensi data workspace: Anda tidak dapat mematikan retensi data 30 hari untuk workspace tersebut, dan kembali ke zero data retention memerlukan pembuatan workspace baru dan memindahkan lalu lintas Anda ke sana. Merotasi material kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan memigrasikan data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur pemulihan.
* **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci Anda berlaku (lihat [Cara kerjanya](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works)).
* **Latensi:** Operasi yang membungkus atau membuka bungkus kunci data melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latensi pada tindakan yang membaca atau menulis data saat istirahat.
* **Penundaan pencabutan:** Pencabutan kunci dapat memerlukan waktu hingga 1 jam (TTL cache). Permintaan yang sudah dalam perjalanan selama jendela tersebut mungkin terus berhasil.
* **Biaya KMS:** CMEK memerlukan kunci di layanan manajemen kunci pihak ketiga (AWS KMS, Google Cloud KMS, atau Azure Key Vault), yang mungkin menimbulkan biaya terpisah yang ditagih oleh penyedia KMS Anda.
* **Telemetri Claude Code di belakang gateway:** Ketika Claude Code terhubung melalui gateway atau proxy LLM (`ANTHROPIC_BASE_URL` kustom), CMEK tidak berlaku untuk telemetri operasional Claude Code. Untuk mematikan telemetri ini, atur variabel lingkungan `DISABLE_TELEMETRY` ke `1`, seperti yang dijelaskan di bawah [Layanan telemetri](https://code.claude.com/docs/en/data-usage#telemetry-services) dalam dokumentasi Claude Code.

## Konfigurasikan penyedia Anda

Ikuti panduan untuk layanan manajemen kunci yang Anda gunakan.

<CardGroup cols={3}>
  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms" title="AWS KMS">
    Buat kunci AWS KMS dengan kebijakan kunci yang memberikan akses Anthropic, lalu daftarkan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms" title="Google Cloud KMS">
    Buat crypto key Cloud KMS, berikan akses akun layanan Anthropic, lalu daftarkan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault" title="Azure Key Vault">
    Buat kunci RSA, berikan akses service principal Anthropic, lalu daftarkan dan validasi.
  </Card>
</CardGroup>
