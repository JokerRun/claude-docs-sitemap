---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 321e0a046e23d2baac8f9fa6b197d326b307ea896b100559712ea362502ce8fd
---

# Kunci enkripsi yang dikelola pelanggan

Enkripsi data workspace Claude saat tidak aktif dengan kunci yang Anda kendalikan.

---

```bash title="Learn more with the /claude-api skill in Claude Code"
claude "/claude-api tell me about customer-managed encryption keys"
```

"Customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK, memungkinkan Anda menyediakan kunci enkripsi di [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), atau [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) milik Anda sendiri dan meminta Anthropic menggunakannya untuk mengenkripsi data workspace tertentu saat tidak aktif (at rest). Anda tetap memegang kendali penuh atas kunci tersebut, termasuk rotasi, audit, dan pencabutan, dan operasi kunci yang dilakukan Anthropic terhadap kunci Anda dicatat dalam log audit penyedia cloud Anda.

Organisasi dapat **memilih untuk ikut serta** menggunakan kunci enkripsi yang dikelola pelanggan alih-alih enkripsi default yang disediakan Anthropic.

<Accordion
  title="Mengaktifkan CMEK bersifat permanen dan dapat menyebabkan kehilangan data yang tidak dapat dipulihkan"
 
>
  Mengaktifkan CMEK bersifat permanen. Anthropic tidak menyimpan salinan kunci Anda, sehingga kesalahan konfigurasi atau kehilangan kunci dapat menghancurkan data Anda yang dilindungi CMEK secara permanen. Jika Anda tidak yakin tentang langkah apa pun, hubungi perwakilan Anthropic Anda sebelum menerapkan perubahan.

  - **Kehilangan data permanen:** Jika kunci enkripsi Anda dihapus, dijadwalkan untuk dihapus, atau materi kuncinya dihancurkan, Anthropic tidak dapat memulihkan data Anda.
  - **Verifikasi pengidentifikasi bersifat wajib:** Memberikan akses kunci kepada principal yang salah atau dipalsukan dapat mengekspos data Anda kepada pihak yang tidak berwenang. Selalu verifikasi pengidentifikasi Anthropic terhadap identitas produksi yang dipublikasikan di setiap panduan konfigurasi.
</Accordion>

## Cara kerjanya \{#how-it-works}

CMEK dilampirkan per workspace. Hanya admin yang dapat mengonfigurasinya. CMEK melindungi data yang ditulis setelah kunci diaktifkan. Data yang sudah ada (obrolan, file, dan sesi sebelumnya) tetap dienkripsi dengan kunci yang dikelola Anthropic dan tidak dienkripsi ulang dengan kunci Anda.

Peristiwa konfigurasi admin CMEK muncul di [Activity Feed Compliance API](/docs/id/manage-claude/compliance-activity-feed). Operasi kunci yang dilakukan Anthropic terhadap kunci Anda (seperti wrapping dan unwrapping kunci data) tidak muncul di Compliance API; operasi tersebut muncul di log audit penyedia cloud Anda.

## Prasyarat \{#prerequisites}

- Akses Cloud Admin di akun, proyek, atau langganan yang akan menampung kunci enkripsi.
- Peran Organization Admin di Anthropic Console (atau Owner / Primary Owner).

## Ketersediaan dan region \{#availability-and-regions}

CMEK saat ini hanya tersedia di region AS, dan semua operasi enkripsi diproses di region AS. Kunci multi-region dan residensi kunci di UE belum didukung.

Pada [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya tersedia dengan kunci AWS KMS; kunci Google Cloud KMS dan Azure Key Vault tidak dapat didaftarkan. Buat, validasi, dan lampirkan kunci di Claude Console; endpoint API `external_keys` saat ini tidak tersedia di Claude Platform di AWS. Kunci harus berada di region AWS yang sama dengan workspace tempat kunci tersebut dilampirkan.

<Note>
  CMEK saat ini tidak didukung untuk organisasi yang mengaktifkan HIPAA. Dukungan untuk menggunakan CMEK bersama dengan HIPAA sedang direncanakan. Jika organisasi Anda mengaktifkan HIPAA, hubungi perwakilan Anthropic Anda sebelum mengonfigurasi CMEK.
</Note>

Untuk latensi minimal, pilih region yang dekat dengan infrastruktur AS milik Anthropic:

| Penyedia | Region yang direkomendasikan |
|:---------|:--------------------|
| AWS | `us-east-2` |
| Google Cloud | `us-central1`, `us-east5` |
| Azure | `northcentralus`, `eastus2` |

## Apa yang dilindungi CMEK \{#what-cmek-protects}

### Dienkripsi \{#encrypted}

- Konten pesan, termasuk lampiran file inline yang dikirim bersama permintaan, serta konfigurasi MCP dan alat.
- Cadangan dan snapshot mewarisi kunci tersebut.

### Dinonaktifkan atau dimodifikasi \{#disabled-or-modified}

Beberapa fitur dimatikan atau dimodifikasi secara substansial ketika CMEK diaktifkan:

- Memori agen terkelola dan agent dreaming dinonaktifkan.
- Fitur beta dan pratinjau riset mungkin tidak tercakup oleh CMEK.

### Tidak dienkripsi \{#not-encrypted}

Fitur-fitur ini tetap tersedia, tetapi datanya tidak dienkripsi dengan kunci Anda. Anda dapat menonaktifkan fitur apa pun yang tidak sesuai untuk kasus penggunaan Anda di Settings.

- Workbench di Console.
- Data yang tidak dalam keadaan at rest (seperti cache) dan data dengan TTL lebih pendek dari 24 jam.
- Activity Feed, log audit, dan lalu lintas jaringan telemetri seperti OTEL, sehingga pelanggan dapat mempertahankan kepatuhan meskipun kunci dicabut.

### Dukungan fitur \{#feature-support}

API, sumber daya agen terkelola, dan alat berikut menyimpan data at rest dengan kunci Anda ketika CMEK diaktifkan:

| API | Agen Terkelola | Alat dan fitur |
|:-----|:---------------|:-------------------|
| Messages | Agents | Web search |
| Models | Environments | Web fetch |
| Files | Sessions | Code execution |
| Batch | Vaults | Bash tool |
| Skills | | Text editor tool |
| User profiles | | MCP connector |
| | | Structured outputs (hanya Claude Sonnet 4.6 dan Claude Haiku 4.5) |
| | | Advisor tool |
| | | Computer use |
| | | Context management |

## Batasan \{#limitations}

- **Tindakan yang tidak dapat dibatalkan:** Setelah kunci dilampirkan ke workspace, kunci tersebut tidak dapat dilepas atau ditukar. Merotasi materi kunci dalam kunci yang sama (misalnya, rotasi otomatis AWS KMS, jadwal rotasi Cloud KMS, atau kebijakan rotasi Azure Key Vault) didukung secara transparan dan tidak memerlukan perubahan di Anthropic. Beralih ke kunci yang *berbeda* memerlukan pembuatan workspace baru dengan kunci baru dan migrasi data Anda. Mencabut atau menonaktifkan kunci membuat semua data yang dilindungi CMEK di workspace tersebut tidak dapat diakses secara permanen, tanpa jalur untuk kembali.
- **Tidak ada enkripsi retroaktif:** CMEK hanya melindungi data yang ditulis setelah kunci diaktifkan.
- **Latensi:** operasi yang melakukan wrap atau unwrap kunci data melakukan perjalanan bolak-balik ke layanan manajemen kunci Anda, yang dapat menambahkan sedikit latensi pada tindakan yang membaca atau menulis data at rest.
- **Penundaan pencabutan:** pencabutan kunci dapat memakan waktu hingga satu jam (TTL cache). Permintaan yang sudah sedang diproses selama jendela waktu tersebut mungkin tetap berhasil.

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