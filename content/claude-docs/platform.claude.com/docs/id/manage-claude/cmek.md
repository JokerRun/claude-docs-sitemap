---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 9f1037156ddd88243b993e4b8dbc86c62eb09a1e091404d3f3696f89e9b01d19
---

# Kunci enkripsi yang dikelola pelanggan

Enkripsi data workspace Claude saat disimpan dengan kunci yang Anda kendalikan.

---

```bash Learn more with the /claude-api skill in Claude Code
claude "/claude-api tell me about customer-managed encryption keys"
```

"Customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK, memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) milik Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat disimpan (at rest). Anda mempertahankan kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Penggunaan CMEK bersifat opsional. Organisasi yang memenuhi syarat dapat **memilih untuk mengaktifkan** penggunaan kunci enkripsi yang dikelola pelanggan sebagai pengganti enkripsi default yang disediakan Anthropic. Untuk mengaktifkan CMEK, hubungi tim akun Anthropic Anda.

<Accordion title="Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan" className="!border-warning-200 bg-warning-900 text-warning-000 [&_button:hover]:bg-warning-200/10">
  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data Anda yang dilindungi CMEK secara permanen. Jika Anda tidak yakin tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  * **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau materi kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  * **Verifikasi pengidentifikasi bersifat wajib:** Memberikan akses kunci kepada principal yang salah atau dipalsukan dapat mengekspos data Anda kepada pihak yang tidak berwenang. Selalu verifikasi pengidentifikasi Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Accordion>

## Cara kerjanya

Hanya admin yang dapat mengonfigurasi CMEK. Pada Claude Platform, CMEK dicakup per workspace dan dikonfigurasi dengan Admin API. Pada Claude Enterprise, CMEK dicakup per organisasi dan dikonfigurasi di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). Pada kedua produk, CMEK melindungi data yang ditulis setelah kunci diaktifkan. Data yang sudah ada (chat, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Peristiwa konfigurasi admin CMEK muncul di [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti wrapping dan unwrapping kunci data) tidak muncul di Compliance API; operasi tersebut muncul di log audit penyedia cloud Anda.

Anthropic memanggil layanan manajemen kunci Anda dari rentang IP publik standarnya. Jika Anda membatasi akses ke layanan manajemen kunci Anda berdasarkan IP, izinkan alamat yang tercantum di [Alamat IP](/docs/id/api/ip-addresses).

## Prasyarat

* Akses Cloud Admin di akun, proyek, atau langganan yang akan menampung kunci enkripsi.
* Peran admin di organisasi Anthropic Anda: peran Organization Admin di Claude Console pada Claude Platform, atau peran Owner atau Primary Owner pada Claude Enterprise.
* [Zero data retention (ZDR)](/docs/id/manage-claude/api-and-data-retention) dinonaktifkan untuk organisasi Anda.

## Ketersediaan dan region

CMEK saat ini hanya tersedia di region AS, dan semua operasi enkripsi diproses di region AS. Kunci multi-region dan residensi kunci UE belum didukung.

Pada [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di Claude Console; endpoint API `external_keys` saat ini tidak tersedia di Claude Platform on AWS. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.

Untuk latensi minimal, pilih region yang dekat dengan infrastruktur AS Anthropic:

| Penyedia     | Region yang direkomendasikan |
| ------------ | ---------------------------- |
| AWS          | `us-east-2`                  |
| Google Cloud | `us-central1`, `us-east5`    |
| Azure        | `northcentralus`, `eastus2`  |

## Apa yang dilindungi CMEK

Apa yang dicakup CMEK bergantung pada produk yang Anda gunakan.

### Dienkripsi

**Claude Platform**

* Konten pesan, file dan lampiran (baik lampiran inline yang dikirim bersama permintaan maupun unggahan Files API), serta konfigurasi MCP dan alat.

**Claude Enterprise**

* Konten chat, termasuk skill, plugin, dan artifact.
* Lampiran chat dan lampiran proyek.
* Claude Code pada CLI, termasuk konten pesan.
* Cowork di Claude Desktop.
* Agen Office.

Pada kedua produk, backup dan snapshot mewarisi kunci tersebut.

### Dinonaktifkan atau dimodifikasi

Beberapa fitur dinonaktifkan atau dimodifikasi secara substansial ketika CMEK diaktifkan. Daftar ini tidak lengkap; tinjau bersama tim Anda sebelum mengaktifkan CMEK.

**Claude Platform**

* Workbench di Claude Console dinonaktifkan.
* Bagian dari Compliance API yang mengembalikan konten mentah, seperti prompt, respons, dan file, dinonaktifkan.
* Fitur beta dan pratinjau riset mungkin tidak dicakup oleh CMEK. Ini termasuk Claude Managed Agents, fitur beta yang dinonaktifkan secara keseluruhan, termasuk memori agen dan agent dreaming.

**Claude Enterprise**

* Pencarian riwayat percakapan dinonaktifkan. Judul percakapan dienkripsi, sehingga pencarian berdasarkan judul atau konten tidak mengembalikan hasil.
* Pencarian di sejumlah besar file menjadi lebih lambat.
* Analytics API dan analitik dalam produk mengalami penurunan. Beberapa tampilan dan laporan penggunaan mungkin tidak lengkap.
* Ekspor log audit dinonaktifkan.
* Signed URL untuk pertukaran file sementara dinonaktifkan. Ini mendukung ekspor data admin claude.ai dan alur file Claude Code Remote seperti pembaruan tangkapan layar.
* Preferensi pribadi dinonaktifkan untuk pengguna yang termasuk dalam organisasi yang dilindungi CMEK, di semua organisasi di bawah induk yang sama. Pengguna yang tidak termasuk dalam organisasi yang dilindungi CMEK masih dapat menggunakannya di semua organisasi.

### Tidak dienkripsi

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di Settings.

**Claude Platform**

* Data yang tidak dalam keadaan disimpan (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
* Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan bahkan jika kunci dicabut.

**Claude Enterprise**

* Claude Code Desktop, Claude Code di web, dan Claude in Slack. Anthropic merekomendasikan untuk menonaktifkan salah satu dari ini yang tidak sesuai untuk kasus penggunaan Anda di konsol admin.
* Fitur beta dan pratinjau riset mungkin tidak dicakup oleh CMEK dan dapat rusak di organisasi CMEK, misalnya Claude Security dan Claude Design.
* Ekspor data sesuai permintaan di bawah Settings > Privacy.

Pada kedua produk, data akun untuk pengguna di organisasi Anda (seperti nama, alamat email, dan foto profil) tidak dienkripsi dengan kunci Anda.

### Dukungan fitur

API dan alat Claude Platform berikut menyimpan data saat disimpan (at rest) dengan kunci Anda ketika CMEK diaktifkan:

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

## Penyimpanan terbatas di luar kunci Anda

Dalam tiga kasus terbatas, Anthropic dapat menyimpan catatan tertentu di bawah enkripsi yang dikelola Anthropic:

* Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A).
* Risiko mendesak akan bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang akan segera terjadi).
* Pelanggaran Bagian D.4 dari [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan setara dalam perjanjian lain yang berlaku antara pelanggan dengan Anthropic.

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), penyimpanan memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi Anthropic untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data). Untuk setiap instans penyimpanan, peristiwa [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) yang sesuai dihasilkan dengan kode alasan yang menyampaikan tujuan penyimpanan tersebut. Lihat [Penyimpanan konten CMEK](/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keamanan (catatan yang diturunkan dari pemindaian keamanan otomatis Anthropic, seperti pengidentifikasi pola dan indikator kecocokan, bukan konten percakapan) disimpan di bawah enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci.

## Batasan

* **Tindakan yang tidak dapat dibatalkan:** Setelah kunci dilampirkan ke workspace, kunci tersebut tidak dapat dilepas atau ditukar. Merotasi materi kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan migrasi data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur untuk kembali.
* **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci diaktifkan.
* **Latensi:** Operasi yang melakukan wrap atau unwrap kunci data melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latensi pada tindakan yang membaca atau menulis data saat disimpan.
* **Penundaan pencabutan:** Pencabutan kunci dapat memakan waktu hingga satu jam (TTL cache). Permintaan yang sudah berjalan selama jendela waktu tersebut mungkin tetap berhasil.
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
