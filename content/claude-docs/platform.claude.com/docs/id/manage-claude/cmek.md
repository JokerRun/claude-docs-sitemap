---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 5b27cd829a4f656c92478f6ecb311c45bef0d87d314f180cba5ad245b57232dd
---

# Kunci enkripsi yang dikelola pelanggan

Enkripsi data workspace Claude saat tidak aktif dengan kunci yang Anda kendalikan.

---

```bash title="Learn more with the /claude-api skill in Claude Code"
claude "/claude-api tell me about customer-managed encryption keys"
```

"Customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK, memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) milik Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat tidak aktif (at rest). Anda mempertahankan kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Penggunaan CMEK bersifat opsional. Organisasi yang memenuhi syarat dapat **memilih untuk ikut serta** menggunakan kunci enkripsi yang dikelola pelanggan alih-alih enkripsi default yang disediakan Anthropic. Untuk mengaktifkan CMEK, hubungi tim akun Anthropic Anda.

<Accordion
  title="Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan"
 
>
  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data yang dilindungi CMEK secara permanen. Jika Anda tidak yakin tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  - **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau materi kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  - **Verifikasi pengidentifikasi bersifat wajib:** Memberikan akses kunci ke principal yang salah atau dipalsukan dapat mengekspos data Anda ke pihak yang tidak berwenang. Selalu verifikasi pengidentifikasi Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Accordion>

## Cara kerjanya \{#how-it-works}

CMEK dilampirkan per workspace. Hanya admin yang dapat mengonfigurasinya. CMEK melindungi data yang ditulis setelah kunci diaktifkan. Data yang sudah ada (percakapan, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Peristiwa konfigurasi admin CMEK muncul di [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti wrapping dan unwrapping data key) tidak muncul di Compliance API; operasi tersebut muncul di log audit penyedia cloud Anda.

Anthropic memanggil layanan manajemen kunci Anda dari rentang IP publik standarnya. Jika Anda membatasi akses ke layanan manajemen kunci Anda berdasarkan IP, izinkan alamat yang tercantum di [Alamat IP](/docs/id/api/ip-addresses).

## Prasyarat \{#prerequisites}

- Akses Cloud Admin di akun, proyek, atau langganan yang akan menampung kunci enkripsi.
- Peran Organization Admin di Claude Console (atau Owner / Primary Owner).

## Ketersediaan dan region \{#availability-and-regions}

CMEK saat ini hanya tersedia di region AS, dan semua operasi enkripsi diproses di region AS. Kunci multi-region dan residensi kunci di UE belum didukung.

Pada [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di Claude Console; endpoint API `external_keys` saat ini tidak tersedia di Claude Platform on AWS. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.

<Note>
  CMEK saat ini tidak didukung untuk organisasi yang mengaktifkan HIPAA. Dukungan untuk menggunakan CMEK bersama dengan HIPAA sedang direncanakan. Jika organisasi Anda mengaktifkan HIPAA, hubungi perwakilan Anthropic Anda sebelum mengonfigurasi CMEK.
</Note>

Untuk latensi minimal, pilih region yang dekat dengan infrastruktur AS Anthropic:

| Penyedia | Region yang direkomendasikan |
|:---------|:--------------------|
| AWS | `us-east-2` |
| Google Cloud | `us-central1`, `us-east5` |
| Azure | `northcentralus`, `eastus2` |

## Apa yang dilindungi CMEK \{#what-cmek-protects}

### Dienkripsi \{#encrypted}

- Konten pesan, file dan lampiran (baik lampiran inline yang dikirim bersama permintaan maupun unggahan Files API), serta konfigurasi MCP dan alat.
- Cadangan dan snapshot mewarisi kunci tersebut.

### Dinonaktifkan atau dimodifikasi \{#disabled-or-modified}

Beberapa fitur dimatikan atau dimodifikasi secara substansial ketika CMEK diaktifkan. Daftar ini tidak lengkap; tinjau bersama tim Anda sebelum mengaktifkan CMEK.

- Workbench di Claude Console dinonaktifkan.
- Bagian dari Compliance API yang mengembalikan konten mentah, seperti prompt, respons, dan file, dinonaktifkan.
- Fitur beta dan pratinjau riset mungkin tidak tercakup oleh CMEK. Ini termasuk Claude Managed Agents, fitur beta yang dinonaktifkan secara keseluruhan, termasuk agent memory dan agent dreaming.

### Tidak dienkripsi \{#not-encrypted}

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di Settings.

- Data yang tidak dalam keadaan at rest (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
- Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan meskipun kunci dicabut.

### Dukungan fitur \{#feature-support}

API dan alat berikut menyimpan data at rest dengan kunci Anda ketika CMEK diaktifkan:

| API | Alat dan fitur |
|:-----|:-------------------|
| Messages | Web search |
| Models | Web fetch |
| Files | Code execution |
| Batch | Bash tool |
| Skills | Text editor tool |
| User profiles | MCP connector |
| | Structured outputs (hanya Claude Sonnet 4.6 dan Claude Haiku 4.5) |
| | Advisor tool |
| | Computer use |
| | Context management |

## Preservasi terbatas di luar kunci Anda \{#limited-preservation-outside-your-key}

Dalam tiga kasus terbatas, Anthropic dapat mempreservasi catatan tertentu di bawah enkripsi yang dikelola Anthropic:

- Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A).
- Risiko mendesak akan bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang akan segera terjadi).
- Pelanggaran Bagian D.4 dari [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan setara dalam perjanjian lain yang berlaku antara pelanggan dan Anthropic.

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservasi memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) Anthropic. Untuk setiap instans preservasi, peristiwa [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) yang sesuai dihasilkan dengan kode alasan yang menyampaikan tujuan preservasi tersebut. Metadata penyaringan keamanan (catatan yang berasal dari pemindaian keamanan otomatis Anthropic, seperti pengidentifikasi pola dan indikator kecocokan, bukan konten percakapan) disimpan di bawah enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci.

## Batasan \{#limitations}

- **Tindakan yang tidak dapat dibatalkan:** Setelah kunci dilampirkan ke workspace, kunci tersebut tidak dapat dilepas atau ditukar. Merotasi materi kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan migrasi data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur untuk kembali.
- **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci diaktifkan.
- **Latensi:** Operasi yang melakukan wrap atau unwrap data key melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latensi pada tindakan yang membaca atau menulis data at rest.
- **Penundaan pencabutan:** Pencabutan kunci dapat memakan waktu hingga satu jam (TTL cache). Permintaan yang sudah berjalan selama jendela waktu tersebut mungkin tetap berhasil.
- **Biaya KMS:** CMEK memerlukan kunci di layanan manajemen kunci pihak ketiga (AWS KMS, Google Cloud KMS, atau Azure Key Vault), yang dapat menimbulkan biaya terpisah yang ditagihkan oleh penyedia KMS Anda.

## Konfigurasikan penyedia Anda \{#configure-your-provider}

Ikuti panduan untuk layanan manajemen kunci yang Anda gunakan.

<CardGroup cols={3}>
  <Card href="/docs/id/manage-claude/cmek-aws-kms" title="AWS KMS">
    Buat kunci AWS KMS dengan kebijakan kunci lintas akun, lalu daftarkan dan validasi.
  </Card>
  <Card href="/docs/id/manage-claude/cmek-google-cloud-kms" title="Google Cloud KMS">
    Buat crypto key Cloud KMS, berikan akses ke akun layanan Anthropic, lalu daftarkan.
  </Card>
  <Card href="/docs/id/manage-claude/cmek-azure-key-vault" title="Azure Key Vault">
    Buat kunci RSA, berikan akses ke service principal Anthropic, lalu daftarkan dan validasi.
  </Card>
</CardGroup>