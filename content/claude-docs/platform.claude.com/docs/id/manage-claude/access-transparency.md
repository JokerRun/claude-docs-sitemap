---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/access-transparency
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: ac882f99c5a43573e02ec5be6bff872a896af05c57f5a00631600f5ba79d3f96
---

# Access Transparency

Terima catatan audit akses manusia ke data organisasi Anda oleh personel Anthropic melalui Compliance API.

---

Pelajari bagaimana Access Transparency membuat catatan akses manusia ke data organisasi Anda oleh personel Anthropic, apa saja yang dicakupnya, dan cara menerima event melalui Compliance API.

<Note>
  Ketika Access Transparency diaktifkan untuk organisasi Anda:

  * Setiap tampilan manusia atas data Anda yang disimpan (lihat [konten yang dicakup](#what-access-transparency-covers)) oleh karyawan Anthropic menulis aktivitas `anthropic_access` ke [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) Anda.
  * Akses hanya terjadi untuk tinjauan keamanan atau respons insiden. Lihat [Kode alasan](#reason-codes).

  Access Transparency tersedia untuk pelanggan yang memenuhi syarat berdasarkan permintaan dan tidak bersifat layanan mandiri. Untuk kelayakan, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Cara kerja Access Transparency

Personel Anthropic mengakses konten pelanggan hanya dalam kondisi yang telah ditentukan. Access Transparency dirancang untuk membuat akses tersebut terlihat oleh Anda. Desainnya bertumpu pada prinsip-prinsip berikut:

* **Akses manusia hanya terjadi berdasarkan kode alasan yang dipublikasikan.**
* **Tampilan manusia atas konten Anda yang dicakup akan dicatat.** Perangkat internal Anthropic yang dapat menjangkau konten Anda yang dicakup diinstrumentasi untuk memancarkan event pada setiap tampilan.
* **Event merepresentasikan akses manusia, bukan pemrosesan otomatis.** Sistem keamanan otomatis Anthropic memproses konten Anda dalam pipeline yang diamankan tanpa akses manusia interaktif; pemrosesan tersebut tidak menghasilkan event `anthropic_access`. Satu-satunya event yang dapat dimulai oleh pemrosesan otomatis adalah catatan preservasi `cmek_preserve` (lihat [Preservasi konten CMEK](#cmek-content-preservation)).
* **Event tiba di feed Anda yang sudah ada.** Aktivitas dapat diakses melalui [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed) Anda. Kredensial, audit, ekspor, dan integrasi SIEM yang sudah ada untuk Compliance API akan tetap berlaku.

## Apa yang dicakup Access Transparency

* **Konten yang dicakup:** Access Transparency mencakup konten prompt dan respons yang dikirim melalui Claude Messages API atau sesi Claude Code. [Dokumentasi ZDR umum](/docs/id/manage-claude/api-and-data-retention) Anthropic dan [dokumentasi ZDR untuk Claude Code](https://code.claude.com/docs/en/zero-data-retention) menjelaskan API dan fitur mana yang dicakup oleh ZDR. API dan fitur yang sama dicakup oleh Access Transparency.
* **Tampilan manual oleh personel Anthropic:** Tampilan manual atas konten Anda yang dicakup oleh peninjau Anthropic menghasilkan event.

## Apa yang tidak dicakup Access Transparency

* **Pemrosesan otomatis:** Penyajian model, pengklasifikasi keamanan, dan pipeline deteksi penyalahgunaan memproses konten Anda sebagai bagian dari operasi normal dan tidak menghasilkan event `anthropic_access`. Preservasi yang dimulai oleh pemrosesan otomatis memang menghasilkan event `cmek_preserve` (lihat [Preservasi konten CMEK](#cmek-content-preservation)).
* **Aktivitas organisasi Anda sendiri:** Panggilan API, tindakan admin, dan pembacaan Compliance API Anda dicakup oleh tipe event [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) standar.
* **Claude for Enterprise dan Claude Apps:** Kursi claude.ai Enterprise, Claude for Work, Cowork, dan Claude in Chrome tidak dicakup.
* **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max.
* **Platform yang dioperasikan mitra:** Amazon Bedrock dan Google Cloud; lihat kontrol transparansi platform tersebut.
* **Apa pun yang tidak dicakup ZDR:** Produk yang tidak dicakup oleh ZDR (misalnya, Files API, aplikasi stateful yang dihosting Anthropic, dan Batch API) tidak dicakup oleh Access Transparency. Lihat [dokumentasi ZDR](https://code.claude.com/docs/en/zero-data-retention#what-zdr-does-not-cover) untuk detail tambahan.

## Memulai

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

## Menerima event Access Transparency

Event Access Transparency dikirimkan sebagai tipe aktivitas `anthropic_access` pada Compliance API Activity Feed. Filter dengan `activity_types[]`:

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --data-urlencode "activity_types[]=anthropic_access" \
  --data-urlencode "limit=50" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Paginasi, pemfilteran rentang tanggal (`created_at.gte` / `.lt`), dan amplop respons (`has_more`, `first_id`, `last_id`) dibagikan dengan bagian lain dari Activity Feed. Lihat [Kueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

Setiap aktivitas `anthropic_access` membawa field Activity standar ditambah yang berikut:

| Field                     | Tipe             | Deskripsi                                                                                                                                          |
| ------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                      | string           | Pengidentifikasi unik untuk aktivitas ini                                                                                                          |
| `accessed_at`             | string RFC 3339  | Kapan akses terjadi. Mungkin lebih awal daripada saat aktivitas menjadi terlihat di feed Anda                                                      |
| `created_at`              | string RFC 3339  | Kapan aktivitas menjadi terlihat di feed Anda                                                                                                      |
| `actor`                   | object           | Selalu `{ "type": "anthropic_actor", "email_address": null }`. Identitas karyawan individu tidak diungkapkan                                       |
| `accessor_department`     | string           | Tim Anthropic yang melakukan akses (misalnya, `Safeguards`)                                                                                        |
| `reason_code`             | enum             | Lihat [Kode alasan](#reason-codes)                                                                                                                 |
| `resource_details.type`   | enum             | Tipe sumber daya, saat ini hanya `message`. Dapat diperluas untuk tipe sumber daya di masa mendatang                                               |
| `resource_details.id`     | string atau null | Pengidentifikasi konten yang diakses                                                                                                               |
| `resource_details.parent` | string atau null | Pengidentifikasi induk konten, misalnya ID percakapan yang berisi pesan. Saat ini `null` atau dihilangkan sampai sumber daya dengan induk didukung |
| `organization_id`         | string           | Organisasi pemilik konten. Format ID bertag (`org_...`)                                                                                            |
| `organization_uuid`       | string           | Organisasi pemilik konten. Format UUID                                                                                                             |
| `workspace_id`            | string atau null | Workspace pemilik konten                                                                                                                           |

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

## Preservasi konten CMEK

Dalam kasus yang jarang terjadi, Anthropic mempreservasi konten tertentu melampaui jendela retensi standar (misalnya, ketika tinjauan keamanan mengonfirmasi konten yang sangat berbahaya yang harus disimpan untuk investigasi yang sedang berlangsung). Preservasi itu sendiri adalah tindakan yang dicatat dan terlihat oleh pelanggan:

* **Event preservasi ditulis ke feed Anda.** Ketika konten dipreservasi, event dengan tipe `cmek_preserve` ditulis ke Compliance API Activity Feed Anda. Event preservasi membawa field yang sama dengan event `anthropic_access`; hanya tipe event yang berbeda, sehingga parser yang menangani salah satunya dapat menangani keduanya. Lihat [Kode alasan](#reason-codes).
* **Event preservasi ditulis terlepas dari bagaimana preservasi dimulai.** Preservasi biasanya mengikuti tinjauan manusia atas konten, tetapi event ditulis baik preservasi dimulai oleh peninjau manusia maupun oleh pipeline keamanan otomatis: catatan tersebut mencerminkan bahwa status retensi konten Anda berubah, terlepas dari siapa yang mengubahnya.
* **Untuk organisasi CMEK, preservasi adalah pergerakan kunci yang terlihat.** Konten yang dipreservasi dienkripsi ulang di luar kunci yang dikelola pelanggan Anda sehingga investigasi dapat berlanjut secara independen dari kunci Anda. Event preservasi adalah catatan Anda bahwa hal ini terjadi. Semua konten lain yang disimpan tetap berada di bawah kunci Anda.

Filter event preservasi dengan cara yang sama seperti event akses:

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --data-urlencode "activity_types[]=cmek_preserve" \
  --data-urlencode "limit=50" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Contoh pesan JSON:

```json
{
  "id": "activity_01AbCdEfGhJkMnPqRsTuVwXy",
  "type": "cmek_preserve",
  "created_at": "2026-07-02T09:41:53.204118Z",
  "accessed_at": "2026-07-02T09:41:50.118764Z",
  "organization_id": "org_0123456789abcdefghijklmn",
  "actor": { "type": "anthropic_actor", "email_address": null },
  "resource_details": { "type": "message", "id": "msg_0ExampleExampleExample" },
  "accessor_department": "Safeguards",
  "reason_code": "policy_violation_investigation",
  "organization_uuid": "00000000-1111-2222-3333-444444444444"
}
```

Untuk event preservasi, `accessed_at` mencatat kapan konten dipreservasi.

## Kode alasan

Kumpulan kode alasan bersifat tertutup. Anthropic akan memperbarui halaman ini jika memperkenalkan kode baru.

| Kode                             | Arti                                                                              |
| -------------------------------- | --------------------------------------------------------------------------------- |
| `safety_review`                  | Konten dilihat sebagai bagian dari investigasi kebijakan penggunaan atau keamanan |
| `incident_response`              | Konten dilihat saat menyelidiki insiden yang memengaruhi organisasi Anda          |
| `policy_violation_investigation` | Konten dipreservasi selama investigasi pelanggaran kebijakan Trust and Safety     |
| `csae_report`                    | Konten dipreservasi sebagai bukti untuk laporan keselamatan anak (CSAE)           |

## Kelayakan permukaan

Tabel berikut mencantumkan permukaan mana yang dicakup oleh Access Transparency. Cakupan berarti akses manusia ke konten dari permukaan tersebut menghasilkan event `anthropic_access`.

| Permukaan                                       | Dicakup | Detail                                                                                                       |
| ----------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| Claude API (`api.anthropic.com`)                | Ya      | Prompt, completion, dan data yang disematkan langsung dalam input API                                        |
| Claude Code (menggunakan kunci API)             | Ya      | Lalu lintas API dari Claude Code dicakup sebagai lalu lintas Claude API                                      |
| Claude Platform di AWS                          | Ya      | Claude Platform di AWS menghasilkan event Access Transparency di dalam Compliance API (bukan AWS CloudTrail) |
| Claude API (`api.anthropic.com`) (Batch, Files) | Tidak   | Claude API Batch dan Files API tidak dicakup, sama seperti keduanya tidak dicakup oleh ZDR                   |
| Claude for Enterprise (kursi claude.ai)         | Tidak   | Tidak dicakup                                                                                                |
| Claude for Work                                 | Tidak   | Tidak dicakup                                                                                                |
| Claude Free, Pro, Max                           | Tidak   | Paket konsumen tidak memenuhi syarat                                                                         |
| Anthropic Workbench                             | Tidak   | Workbench menyimpan data di penyimpanan data yang tidak dicakup oleh Access Transparency                     |
| Microsoft Foundry                               | Tidak   | Tidak tersedia                                                                                               |
| Amazon Bedrock, Google Cloud                    | Tidak   | Platform yang dioperasikan mitra; lihat kontrol transparansi platform tersebut                               |

## Batasan dan pengecualian

### Waktu cakupan

Access Transparency berlaku sejak diaktifkan untuk organisasi Anda. Konten yang sudah berada dalam jendela retensi Anda saat pengaktifan mungkin juga menghasilkan event saat diakses, tetapi Anthropic tidak menjamin cakupan untuk konten yang ditulis sebelum pengaktifan. Perlakukan tanggal pengaktifan Anda sebagai awal cakupan yang andal. Mungkin ada penundaan hingga dua jam antara pengaktifan Access Transparency dan konten Anda mulai dicakup.

### Waktu notifikasi

Event `anthropic_access` dan `cmek_preserve` dikirimkan ke feed Compliance API Anda dalam waktu dua hari kerja sejak akses atau preservasi yang dicatatnya. Feed ini tidak boleh diperlakukan sebagai saluran peringatan real-time, dan stempel waktu `accessed_at` mencerminkan kapan akses terjadi, yang mungkin hingga dua hari kerja sebelum aktivitas menjadi terlihat di feed Anda. Field `created_at` mencerminkan waktu event menjadi terlihat.

### Pemrosesan otomatis tidak menghasilkan event akses

Event `anthropic_access` hanya mencatat akses manusia. Sistem keamanan otomatis dan pengklasifikasi Anthropic terus memproses konten Anda sebagai bagian dari operasi normal, dan pemrosesan tersebut tidak menghasilkan event `anthropic_access`. Satu-satunya event yang dapat dimulai oleh pemrosesan otomatis adalah catatan preservasi `cmek_preserve` (lihat [Preservasi konten CMEK](#cmek-content-preservation)). Feed yang kosong berarti tidak ada manusia di Anthropic yang telah melihat konten Anda; ini tidak berarti konten Anda tidak diproses oleh sistem otomatis.

### Access Transparency tidak mengubah apa yang dapat diakses Anthropic

Access Transparency mencatat akses; ia tidak memberikan atau membatasinya. Tujuan personel Anthropic dapat mengakses konten Anda diatur oleh perjanjian Anda dengan Anthropic dan [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup), dan tetap sama terlepas dari apakah Access Transparency diaktifkan atau tidak.

### Log penggunaan kunci CMEK bukan catatan per-pembacaan

Untuk organisasi yang juga mengaktifkan CMEK, log audit KMS cloud Anda (CloudTrail, Cloud Audit Logs, atau Azure Monitor) mencatat penggunaan kunci Anda oleh Anthropic. Karena kunci di-cache untuk periode singkat selama operasi, satu pembacaan manusia individual tidak selalu menghasilkan entri dekripsi KMS yang berbeda. Gunakan feed Access Transparency sebagai catatan per-akses; log KMS Anda secara independen mengonfirmasi pola penggunaan kunci.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Bagaimana saya tahu apakah organisasi saya telah mengaktifkan Access Transparency?">
    Hubungi perwakilan akun Anthropic Anda.
  </Accordion>

  <Accordion title="Apakah saya akan melihat event setiap kali pengklasifikasi keamanan berjalan pada lalu lintas saya?">
    Tidak. Pemrosesan otomatis tidak menghasilkan event `anthropic_access`; Anda hanya akan melihat event `anthropic_access` jika peninjau manusia kemudian melihat konten tersebut. Secara terpisah, event `cmek_preserve` ditulis ketika konten dipreservasi, baik preservasi dimulai oleh peninjau manusia maupun pipeline keamanan otomatis.
  </Accordion>

  <Accordion title="Kami adalah platform yang menyajikan Claude kepada pengguna akhir kami sendiri. Bisakah kami mengaktifkan Access Transparency?">
    Access Transparency tidak tersedia untuk deployment platform. Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan kasus penggunaan Anda.
  </Accordion>

  <Accordion title="Apakah saya akan melihat event untuk akses yang terjadi sebelum kami mendaftar, atau untuk data kami yang lebih lama?">
    Access Transparency tidak dijamin bersifat retroaktif. Ia mencakup akses manusia ke konten yang ditulis ke Claude API pada atau setelah tanggal pendaftaran Anda. Anda mungkin melihat event untuk akses ke konten yang ditulis sebelum pendaftaran.
  </Accordion>

  <Accordion title="Seberapa cepat setelah akses saya akan melihat event tersebut?">
    Dalam waktu dua hari kerja sejak akses. Konfigurasikan peringatan SIEM atau ekspor terjadwal apa pun dengan jendela lookback yang sesuai alih-alih mengasumsikan kedatangan real-time.
  </Accordion>

  <Accordion title="Bagaimana saya tahu permintaan mana yang dirujuk oleh event anthropic_access?">
    Gunakan field `resource_details.id`. Field ini berisi ID pesan yang sama (`msg_...`) yang dikembalikan oleh [Messages API](/docs/id/api/messages/create) di field `id` pada setiap body respons. Agar ini berguna, catat `id` di sistem Anda sendiri bersama metadata internal Anda, seperti aplikasi, pengguna akhir, atau percakapan yang menghasilkan permintaan tersebut. Ketika event tiba, gabungkan `resource_details.id`-nya dengan log Anda untuk mengidentifikasi dengan tepat permintaan mana yang dilihat.
  </Accordion>

  <Accordion title="Bisakah saya mengaktifkan Access Transparency untuk satu workspace saja?">
    Access Transparency diaktifkan di tingkat organisasi dan mencakup semua workspace.
  </Accordion>

  <Accordion title="Bagaimana hubungan Access Transparency dengan CMEK?">
    Keduanya independen. Dengan CMEK, preservasi keamanan di luar kunci Anda memancarkan event `cmek_preserve` terpisah pada feed yang sama. Lihat [Preservasi konten CMEK](#cmek-content-preservation) dan [CMEK](/docs/id/manage-claude/cmek).
  </Accordion>

  <Accordion title="Bagaimana cara meminta Access Transparency?">
    Hubungi perwakilan akun Anthropic Anda.
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Ikhtisar Compliance API](/docs/id/manage-claude/compliance-api)
* [Activity Feed](/docs/id/manage-claude/compliance-activity-feed)
* [API dan retensi data](/docs/id/manage-claude/api-and-data-retention)
* [Customer-Managed Encryption Keys (CMEK)](/docs/id/manage-claude/cmek)
* [Penggunaan data Claude Code](https://code.claude.com/docs/en/data-usage)
* [Trust Center](https://trust.anthropic.com/resources)
