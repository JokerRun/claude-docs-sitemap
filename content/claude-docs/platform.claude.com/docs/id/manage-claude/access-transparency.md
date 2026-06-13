---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/access-transparency
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 35deb4f830f1ab9f8388609b0a4853ea8521126aa5a4958e491fa3298f3fd672
---

# Access Transparency

Terima catatan audit akses manusia ke data organisasi Anda oleh personel Anthropic melalui Compliance API.

---

Pelajari bagaimana Access Transparency membuat catatan akses manusia ke data organisasi Anda oleh personel Anthropic, apa saja yang dicakupnya, dan cara menerima event melalui Compliance API.

<Note>
  Ketika Access Transparency diaktifkan untuk organisasi Anda:

  - Setiap tampilan manusia terhadap data Anda yang disimpan (lihat [konten yang dicakup](#apa-yang-dicakup-access-transparency)) oleh karyawan Anthropic akan menulis aktivitas `anthropic_access` ke [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) Anda.
  - Akses hanya terjadi untuk tinjauan keamanan atau respons insiden. Lihat [Kode alasan](#kode-alasan).

  Access Transparency tersedia untuk pelanggan yang memenuhi syarat berdasarkan permintaan dan tidak bersifat swalayan. Untuk kelayakan, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Cara kerja Access Transparency \{#how-access-transparency-works}

Personel Anthropic mengakses konten pelanggan hanya dalam kondisi yang telah ditentukan. Access Transparency dirancang untuk membuat akses tersebut terlihat oleh Anda. Desain ini didasarkan pada prinsip-prinsip berikut:

- **Akses manusia hanya terjadi di bawah kode alasan yang dipublikasikan.**
- **Tampilan manusia terhadap konten Anda yang dicakup akan dicatat.** Perangkat internal Anthropic yang dapat menjangkau konten Anda yang dicakup telah diinstrumentasi untuk mengeluarkan event pada setiap tampilan.
- **Event merepresentasikan akses manusia, bukan pemrosesan otomatis.** Sistem keamanan otomatis Anthropic memproses konten Anda dalam pipeline yang diamankan tanpa akses manusia interaktif; pemrosesan tersebut tidak menulis ke feed ini.
- **Event tiba di feed Anda yang sudah ada.** Aktivitas dapat diakses melalui [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) Anda. Kredensial, audit, ekspor, dan integrasi SIEM yang sudah ada untuk Compliance API akan tetap berlaku.

## Apa yang dicakup Access Transparency \{#what-access-transparency-covers}

- **Konten yang dicakup:** Access Transparency mencakup konten prompt dan respons yang dikirim melalui Claude Messages API atau sesi Claude Code. [Dokumentasi ZDR umum](/docs/id/manage-claude/api-and-data-retention) Anthropic dan [dokumentasi ZDR untuk Claude Code](https://code.claude.com/docs/en/zero-data-retention) menjelaskan API dan fitur mana yang dicakup oleh ZDR. API dan fitur yang sama juga dicakup oleh Access Transparency.
- **Tampilan manual oleh personel Anthropic:** Tampilan manual terhadap konten Anda yang dicakup oleh peninjau Anthropic menghasilkan event.

## Apa yang tidak dicakup Access Transparency \{#what-access-transparency-does-not-cover}

- **Pemrosesan otomatis:** Penyajian model, pengklasifikasi keamanan, dan pipeline deteksi penyalahgunaan memproses konten Anda sebagai bagian dari operasi normal dan tidak menghasilkan event.
- **Aktivitas organisasi Anda sendiri:** Panggilan API, tindakan admin, dan pembacaan Compliance API Anda dicakup oleh tipe event [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) standar.
- **Claude for Enterprise dan Claude Apps:** Kursi claude.ai Enterprise, Claude for Work, Cowork, dan Claude in Chrome tidak dicakup.
- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max.
- **Platform yang dioperasikan mitra:** Amazon Bedrock dan Vertex AI; lihat kontrol transparansi platform tersebut.
- **Apa pun yang tidak dicakup ZDR:** Produk yang tidak dicakup oleh ZDR (misalnya, Files API, aplikasi stateful yang di-host Anthropic, dan Batch API) tidak dicakup oleh Access Transparency. Lihat [dokumentasi ZDR](https://code.claude.com/docs/en/zero-data-retention#what-zdr-does-not-cover) untuk detail tambahan.

## Memulai \{#getting-started}

Untuk mengaktifkan Access Transparency:

<Steps>
  <Step title="Minta Access Transparency">
    Hubungi perwakilan akun Anthropic Anda.
  </Step>
  <Step title="Anthropic meninjau kelayakan">
    Anthropic mengonfirmasi bahwa organisasi Anda memenuhi kriteria kelayakan dan mengaktifkan kemampuan ini di tingkat organisasi.
  </Step>
  <Step title="Terima event melalui Compliance API">
    Aktivitas `anthropic_access` muncul di Activity Feed Anda yang sudah ada di bawah Compliance Access Key Anda yang sudah ada; tidak diperlukan endpoint atau kredensial baru.
  </Step>
</Steps>

Access Transparency diaktifkan di tingkat organisasi dan mencakup semua workspace. Pendaftaran per-workspace saat ini tidak tersedia.

## Menerima event Access Transparency \{#receiving-access-transparency-events}

Event Access Transparency dikirimkan sebagai tipe aktivitas `anthropic_access` pada Compliance API Activity Feed. Filter dengan `activity_types[]`:

```bash nocheck
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --data-urlencode "activity_types[]=anthropic_access" \
  --data-urlencode "limit=50" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Paginasi, pemfilteran rentang tanggal (`created_at.gte` / `.lt`), dan envelope respons (`has_more`, `first_id`, `last_id`) digunakan bersama dengan bagian lain dari Activity Feed. Lihat [Melakukan kueri pada Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

Setiap aktivitas `anthropic_access` membawa field Activity standar ditambah yang berikut:

| Field | Tipe | Deskripsi |
| :---- | :---- | :---- |
| `id` | string | Pengidentifikasi unik untuk aktivitas ini |
| `accessed_at` | string RFC 3339 | Kapan akses terjadi. Mungkin lebih awal dari saat aktivitas menjadi terlihat di feed Anda |
| `created_at` | string RFC 3339 | Kapan aktivitas menjadi terlihat di feed Anda |
| `actor` | object | Selalu `{ "type": "anthropic_actor", "email_address": null }`. Identitas karyawan individu tidak diungkapkan |
| `accessor_department` | string | Tim Anthropic yang melakukan akses (misalnya, `Safeguards`) |
| `reason_code` | enum | Lihat [Kode alasan](#kode-alasan) |
| `resource_details.type` | enum | Tipe sumber daya, saat ini hanya `message`. Dapat diperluas untuk tipe sumber daya di masa mendatang |
| `resource_details.id` | string atau null | Pengidentifikasi konten yang diakses |
| `resource_details.parent` | string atau null | Pengidentifikasi induk konten, misalnya ID percakapan yang berisi pesan. Saat ini `null` atau dihilangkan hingga sumber daya dengan induk didukung |
| `organization_id` | string | Organisasi tempat konten tersebut berada. Format ID bertag (`org_...`) |
| `organization_uuid` | string | Organisasi tempat konten tersebut berada. Format UUID |
| `workspace_id` | string atau null | Workspace tempat konten tersebut berada |

Contoh pesan JSON:

```json
{
  "id": "activity_013b013744txqZtFHLUaRqLr",
  "type": "anthropic_access",
  "created_at": "2026-06-08T17:12:09.812446Z",
  "accessed_at": "2026-06-08T17:12:06.478035Z",
  "organization_id": "org_0910d9133038914eta7i3vt",
  "actor": { "type": "anthropic_actor", "email_address": null },
  "resource_details": { "type": "message", "id": "msg_1234ABCD" },
  "accessor_department": "Safeguards",
  "reason_code": "safety_review",
  "organization_uuid": "5b236db4-3fb4-4bf3-a560-b5e266038a15"
}
```

## Kode alasan \{#reason-codes}

Kumpulan kode alasan bersifat tertutup. Anthropic akan memperbarui halaman ini jika memperkenalkan kode baru.

| Kode | Arti |
| :---- | :---- |
| `safety_review` | Konten dilihat sebagai bagian dari investigasi kebijakan penggunaan atau keamanan |
| `incident_response` | Konten dilihat saat menyelidiki insiden yang memengaruhi organisasi Anda |

## Preservasi konten CMEK \{#cmek-content-preservation}

Dalam kasus yang jarang terjadi, Anthropic mempreservasi konten tertentu melampaui jendela retensi standar (misalnya, ketika tinjauan keamanan mengonfirmasi konten yang sangat berbahaya yang harus disimpan untuk investigasi yang sedang berlangsung). Preservasi itu sendiri merupakan tindakan yang dicatat dan terlihat oleh pelanggan:

- **Event preservasi ditulis ke feed Anda.** Ketika konten dipreservasi, event dengan tipe `cmek_preserve` ditulis ke Compliance API Activity Feed Anda, membawa kode alasan dari kumpulan tertutup yang sama dan field yang sama seperti event akses.
- **Preservasi mengikuti tinjauan.** Event preservasi selalu mengikuti event `anthropic_access`, karena preservasi diinisiasi dari tinjauan manusia.
- **Untuk organisasi CMEK, preservasi adalah pergerakan kunci yang terlihat.** Konten yang dipreservasi dienkripsi ulang di luar kunci yang dikelola pelanggan Anda sehingga investigasi dapat berlanjut secara independen dari kunci Anda. Event preservasi adalah catatan Anda bahwa hal ini terjadi. Semua konten lain yang disimpan tetap berada di bawah kunci Anda.

## Kelayakan permukaan \{#surface-eligibility}

Tabel berikut mencantumkan permukaan mana yang dicakup oleh Access Transparency. Cakupan berarti akses manusia ke konten dari permukaan tersebut menghasilkan event `anthropic_access`.

| Permukaan | Dicakup | Detail |
| :---- | :---- | :---- |
| Claude API (`api.anthropic.com`) | Ya | Prompt, completion, dan data yang disematkan langsung dalam input API |
| Claude Code (menggunakan kunci API) | Ya | Lalu lintas API dari Claude Code dicakup sebagai lalu lintas Claude API |
| Claude Platform di AWS | Ya | Claude Platform di AWS menghasilkan event Access Transparency dalam Compliance API (bukan AWS CloudTrail) |
| Claude API (`api.anthropic.com`) (Batch, Files) | Tidak | Claude API Batch dan Files API tidak dicakup, sama seperti tidak dicakup oleh ZDR |
| Claude for Enterprise (kursi claude.ai) | Tidak | Tidak dicakup |
| Claude for Work | Tidak | Tidak dicakup |
| Claude Free, Pro, Max | Tidak | Paket konsumen tidak memenuhi syarat |
| Anthropic Workbench | Tidak | Workbench menyimpan data di penyimpanan data yang tidak dicakup oleh Access Transparency |
| Microsoft Foundry | Tidak | Tidak tersedia |
| Amazon Bedrock, Vertex AI | Tidak | Platform yang dioperasikan mitra; lihat kontrol transparansi platform tersebut |

## Batasan dan pengecualian \{#limitations-and-exclusions}

### Waktu cakupan \{#coverage-timing}

Access Transparency berlaku sejak saat diaktifkan untuk organisasi Anda. Konten yang sudah ada dalam jendela retensi Anda pada saat pengaktifan mungkin juga menghasilkan event ketika diakses, tetapi Anthropic tidak menjamin cakupan untuk konten yang ditulis sebelum pengaktifan. Perlakukan tanggal pengaktifan Anda sebagai awal cakupan yang dapat diandalkan. Mungkin ada penundaan hingga dua jam antara pengaktifan Access Transparency dan konten Anda mulai dicakup.

### Waktu notifikasi \{#notification-timing}

Event `anthropic_access` dikirimkan ke feed Compliance API Anda dalam waktu dua hari kerja sejak akses yang dicatatnya. Feed ini tidak boleh diperlakukan sebagai saluran peringatan real-time, dan timestamp `accessed_at` mencerminkan kapan akses terjadi, yang mungkin hingga dua hari kerja sebelum aktivitas menjadi terlihat di feed Anda. Field `created_at` mencerminkan waktu event menjadi terlihat.

### Pemrosesan otomatis tidak dicatat \{#automated-processing-is-not-logged}

Access Transparency hanya mencatat akses manusia. Sistem keamanan otomatis dan pengklasifikasi Anthropic terus memproses konten Anda sebagai bagian dari operasi normal, dan pemrosesan tersebut tidak menghasilkan event `anthropic_access`. Feed yang kosong berarti tidak ada manusia di Anthropic yang telah melihat konten Anda; itu tidak berarti konten Anda tidak diproses oleh sistem otomatis.

### Access Transparency tidak mengubah apa yang dapat diakses Anthropic \{#access-transparency-does-not-change-what-anthropic-can-access}

Access Transparency mencatat akses; tidak memberikan atau membatasinya. Tujuan yang memungkinkan personel Anthropic mengakses konten Anda diatur oleh perjanjian Anda dengan Anthropic dan [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup), dan tetap sama terlepas dari apakah Access Transparency diaktifkan atau tidak.

### Log penggunaan kunci CMEK bukan catatan per-pembacaan \{#cmek-key-use-logs-are-not-a-per-read-record}

Untuk organisasi yang juga mengaktifkan CMEK, log audit KMS cloud Anda (CloudTrail, Cloud Audit Logs, atau Azure Monitor) mencatat penggunaan kunci Anda oleh Anthropic. Karena kunci di-cache untuk periode singkat selama operasi, pembacaan manusia individual tidak selalu menghasilkan entri dekripsi KMS yang berbeda. Gunakan feed Access Transparency sebagai catatan per-akses; log KMS Anda secara independen mengonfirmasi pola penggunaan kunci.

## Pertanyaan yang sering diajukan \{#frequently-asked-questions}

<section title="Bagaimana saya tahu jika organisasi saya telah mengaktifkan Access Transparency?">

  Hubungi perwakilan akun Anthropic Anda.

</section>

<section title="Apakah saya akan melihat event setiap kali pengklasifikasi keamanan berjalan pada lalu lintas saya?">

  Tidak. Pemrosesan otomatis tidak menghasilkan event Access Transparency. Anda hanya akan melihat event jika peninjau manusia kemudian melihat konten tersebut.

</section>

<section title="Kami adalah platform yang menyajikan Claude kepada pengguna akhir kami sendiri. Bisakah kami mengaktifkan Access Transparency?">

  Access Transparency tidak tersedia untuk deployment platform. Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan kasus penggunaan Anda.

</section>

<section title="Apakah saya akan melihat event untuk akses yang terjadi sebelum kami mendaftar, atau untuk data lama kami?">

  Access Transparency tidak dijamin bersifat retroaktif. Ini mencakup akses manusia ke konten yang ditulis ke Claude API pada atau setelah tanggal pendaftaran Anda. Anda mungkin melihat event untuk akses ke konten yang ditulis sebelum pendaftaran.

</section>

<section title="Seberapa cepat setelah akses saya akan melihat event?">

  Dalam waktu dua hari kerja sejak akses. Konfigurasikan peringatan SIEM atau ekspor terjadwal apa pun dengan jendela lookback yang sesuai daripada mengasumsikan kedatangan real-time.

</section>

<section title="Bagaimana saya tahu permintaan mana yang dirujuk oleh event anthropic_access?">

  Gunakan field `resource_details.id`. Field ini berisi ID pesan yang sama (`msg_...`) yang dikembalikan oleh [Messages API](/docs/id/api/messages/create) di field `id` pada setiap body respons. Agar ini berguna, catat `id` di sistem Anda sendiri bersama dengan metadata internal Anda, seperti aplikasi, pengguna akhir, atau percakapan yang menghasilkan permintaan tersebut. Ketika event tiba, gabungkan `resource_details.id`-nya dengan log Anda untuk mengidentifikasi dengan tepat permintaan mana yang dilihat.

</section>

<section title="Bisakah saya mengaktifkan Access Transparency untuk satu workspace saja?">

  Access Transparency diaktifkan di tingkat organisasi dan mencakup semua workspace.

</section>

<section title="Bagaimana hubungan Access Transparency dengan CMEK?">

  Keduanya independen. Dengan CMEK, preservasi keamanan di luar kunci Anda mengeluarkan event `cmek_preserve` terpisah pada feed yang sama. Lihat [CMEK](/docs/id/manage-claude/cmek).

</section>

<section title="Bagaimana cara meminta Access Transparency?">

  Hubungi perwakilan akun Anthropic Anda.

</section>

## Sumber daya terkait \{#related-resources}

- [Ikhtisar Compliance API](/docs/id/manage-claude/compliance-api)
- [Activity Feed](/docs/id/manage-claude/compliance-activity-feed)
- [API dan retensi data](/docs/id/manage-claude/api-and-data-retention)
- [Customer-Managed Encryption Keys (CMEK)](/docs/id/manage-claude/cmek)
- [Penggunaan data Claude Code](https://code.claude.com/docs/en/data-usage)
- [Trust Center](https://trust.anthropic.com/resources)