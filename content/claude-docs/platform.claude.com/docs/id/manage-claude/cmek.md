---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e472361edd92bc0bec1d43b205427d0a975b175af8f62ba5e76e3be141d53f57
---

# Kunci enkripsi yang dikelola pelanggan

Enkripsi data workspace Claude saat tidak aktif dengan kunci yang Anda kendalikan.

---

```bash Learn more with the /claude-api skill in Claude Code
claude "/claude-api tell me about customer-managed encryption keys"
```

"Customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK, memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) milik Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat tidak aktif (at rest). Anda mempertahankan kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Penggunaan CMEK bersifat opsional. Organisasi yang memenuhi syarat dapat **memilih untuk ikut serta** menggunakan kunci enkripsi yang dikelola pelanggan alih-alih enkripsi default yang disediakan Anthropic. Untuk mengaktifkan CMEK, hubungi tim akun Anthropic Anda.

<Warning>
  **Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan**

  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data yang dilindungi CMEK Anda secara permanen. Jika Anda tidak yakin tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  * **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau materi kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  * **Verifikasi identifier wajib dilakukan:** Memberikan akses kunci kepada principal yang salah atau dipalsukan dapat mengekspos data Anda kepada pihak yang tidak berwenang. Selalu verifikasi identifier Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi. Jangan pernah mempercayai identifier yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Cara kerjanya

Hanya Organization Admin (di Claude Platform) atau Owner dan Primary Owner (di Claude Enterprise) yang dapat mengonfigurasi CMEK. Di Claude Platform, CMEK dicakup per workspace dan dikonfigurasi dengan Admin API. Di Claude Enterprise, CMEK dicakup per organisasi dan dikonfigurasi di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). Pada kedua produk, CMEK melindungi data yang ditulis setelah kunci diaktifkan. Data yang sudah ada (chat, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Peristiwa konfigurasi CMEK muncul di [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti wrapping dan unwrapping kunci data) tidak muncul di Compliance API; operasi tersebut muncul di log audit penyedia cloud Anda.

Anthropic memanggil layanan manajemen kunci Anda dari rentang IP publik standarnya. Jika Anda membatasi akses ke layanan manajemen kunci Anda berdasarkan IP, izinkan alamat yang tercantum di [alamat IP](/docs/id/api/ip-addresses).

## Prasyarat

* Izin untuk membuat kunci enkripsi dan mengelola akses kunci di akun, proyek, atau langganan yang akan menjadi host kunci enkripsi.
* Peran Organization Admin di Claude Console pada Claude Platform, atau peran Owner atau Primary Owner pada Claude Enterprise.
* Konfigurasi retensi data: CMEK diizinkan dengan [Zero data retention (ZDR)](/docs/id/manage-claude/api-and-data-retention) untuk Claude Platform maupun Claude Enterprise.

## Ketersediaan dan region

CMEK saat ini hanya tersedia di region AS, dan semua operasi enkripsi diproses di region AS.

Pada [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di Claude Console; endpoint API `external_keys` saat ini tidak tersedia di Claude Platform on AWS. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.

Untuk "latency" (latensi) minimal, pilih region yang dekat dengan infrastruktur AS milik Anthropic:

| Penyedia     | Region yang direkomendasikan |
| ------------ | ---------------------------- |
| AWS          | `us-east-2`                  |
| Google Cloud | `us-central1`, `us-east5`    |
| Azure        | `northcentralus`, `eastus2`  |

## Apa yang dilindungi CMEK

Cakupan CMEK bergantung pada produk yang Anda gunakan.

### Dienkripsi

**Claude Platform**

* Konten pesan, file dan lampiran (baik lampiran inline yang dikirim dengan permintaan maupun unggahan Files API), serta konfigurasi MCP dan alat.

**Claude Enterprise**

* Konten chat, termasuk skill, plugin, dan artifacts.
* Lampiran chat dan lampiran proyek.
* Claude Code di CLI, termasuk konten pesan.
* Cowork di Claude Desktop.
* Office agents.
* Claude in Chrome.

Pada kedua produk, backup dan snapshot mewarisi kunci tersebut.

### Dinonaktifkan atau dimodifikasi

Beberapa fitur dimatikan atau dimodifikasi secara substansial ketika CMEK diaktifkan. Daftar ini tidak lengkap; tinjau bersama tim Anda sebelum mengaktifkan CMEK.

**Claude Platform**

* Workbench di Claude Console dinonaktifkan.
* Bagian dari Compliance API yang mengembalikan konten mentah, seperti prompt, respons, dan file, dinonaktifkan.
* Fitur beta dan pratinjau riset mungkin tidak tercakup oleh CMEK. Ini termasuk Claude Managed Agents, fitur beta yang dinonaktifkan secara keseluruhan, termasuk agent memory dan agent dreaming.

**Claude Enterprise**

* Pencarian riwayat percakapan dinonaktifkan. Judul percakapan dienkripsi, sehingga pencarian berdasarkan judul atau konten tidak mengembalikan hasil.
* Pencarian di sejumlah besar file menjadi lebih lambat.
* Analytics API dan analitik dalam produk mengalami penurunan. Beberapa tampilan penggunaan dan laporan mungkin tidak lengkap.
* Ekspor log audit dinonaktifkan.
* Signed URL untuk pertukaran file sementara dinonaktifkan. Ini mendukung ekspor data organisasi di claude.ai dan alur file Claude Code Remote seperti pembaruan tangkapan layar.
* Preferensi pribadi dinonaktifkan untuk pengguna yang termasuk dalam organisasi yang dilindungi CMEK, di semua organisasi di bawah induk yang sama. Pengguna yang tidak termasuk dalam organisasi yang dilindungi CMEK masih dapat menggunakannya di semua organisasi.

### Tidak dienkripsi

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di **Settings**.

**Claude Platform**

* Data yang tidak dalam keadaan at rest (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
* Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan bahkan jika kunci dicabut.

**Claude Enterprise**

* Claude Code Desktop, Claude Code di web, dan Claude in Slack. Anthropic merekomendasikan untuk menonaktifkan fitur-fitur ini yang tidak sesuai untuk kasus penggunaan Anda di konsol admin.
* Fitur beta dan pratinjau riset mungkin tidak tercakup oleh CMEK dan dapat rusak di organisasi CMEK, misalnya Claude Security dan Claude Design.
* Ekspor data on-demand di bawah **Settings** > **Privacy**.

Pada kedua produk, data akun untuk pengguna di organisasi Anda (seperti nama, alamat email, dan foto profil) tidak dienkripsi dengan kunci Anda.

### Dukungan fitur

API dan alat Claude Platform berikut menyimpan data at rest dengan kunci Anda ketika CMEK diaktifkan:

| API           | Alat dan fitur                                                    |
| ------------- | ----------------------------------------------------------------- |
| Messages      | Web search                                                        |
| Models        | Web fetch                                                         |
| Files         | Code execution                                                    |
| Batch         | Bash tool                                                         |
| Skills        | Text editor tool                                                  |
| User profiles | MCP connector                                                     |
|               | Structured outputs (hanya Claude Sonnet 4.6 dan Claude Haiku 4.5) |
|               | Advisor tool                                                      |
|               | Computer use                                                      |
|               | Context management                                                |

## Preservasi terbatas di luar kunci Anda

Dalam tiga kasus yang sempit, Anthropic dapat mempertahankan catatan tertentu dengan enkripsi yang dikelola Anthropic:

* Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A).
* Risiko mendesak akan bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang akan segera terjadi).
* Pelanggaran terhadap Bagian D.4 dari [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan setara dalam perjanjian lain yang berlaku antara pelanggan dan Anthropic.

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservasi memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi Anthropic untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data). Untuk setiap instans preservasi, peristiwa [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) yang sesuai dihasilkan dengan kode alasan yang menyampaikan tujuan preservasi tersebut. Lihat [preservasi konten CMEK](/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keamanan (catatan yang berasal dari pemindaian keamanan otomatis Anthropic, seperti identifier pola dan indikator kecocokan, bukan konten percakapan) disimpan dengan enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci.

## Batasan

* **Tindakan yang tidak dapat dibatalkan:** Setelah kunci dilampirkan ke workspace, kunci tersebut tidak dapat dilepas atau ditukar. Di Claude Platform, melampirkan kunci juga mengunci pengaturan retensi data workspace: Anda tidak dapat mematikan retensi data 30 hari untuk workspace tersebut, dan kembali ke zero data retention memerlukan pembuatan workspace baru dan memindahkan lalu lintas Anda ke sana. Merotasi materi kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan migrasi data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur pemulihan.
* **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci diaktifkan.
* **Latency:** Operasi yang melakukan wrap atau unwrap kunci data melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latency pada tindakan yang membaca atau menulis data at rest.
* **Penundaan pencabutan:** Pencabutan kunci dapat memakan waktu hingga 1 jam (TTL cache). Permintaan yang sudah berjalan selama jendela waktu tersebut mungkin tetap berhasil.
* **Biaya KMS:** CMEK memerlukan kunci di layanan manajemen kunci pihak ketiga (AWS KMS, Google Cloud KMS, atau Azure Key Vault), yang dapat menimbulkan biaya terpisah yang ditagih oleh penyedia KMS Anda.

## Konfigurasikan penyedia Anda

Ikuti panduan untuk layanan manajemen kunci yang Anda gunakan.

<CardGroup cols={3}>
  <Card href="/docs/id/manage-claude/cmek-aws-kms" title="AWS KMS">
    Buat kunci AWS KMS dengan kebijakan kunci lintas akun, lalu daftarkan dan validasi.
  </Card>

  <Card href="/docs/id/manage-claude/cmek-google-cloud-kms" title="Google Cloud KMS">
    Buat crypto key Cloud KMS, berikan akses ke service account Anthropic, lalu daftarkan.
  </Card>

  <Card href="/docs/id/manage-claude/cmek-azure-key-vault" title="Azure Key Vault">
    Buat kunci RSA, berikan akses ke service principal Anthropic, lalu daftarkan dan validasi.
  </Card>
</CardGroup>
