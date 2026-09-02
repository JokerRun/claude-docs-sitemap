---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/access-transparency
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d2579500ecac8f8d060f7d859c692bc7a21067f65981b4b2b480a8639d401fe7
---

---
title: Access Transparency
url: https://platform.claude.com/docs/id/manage-claude/access-transparency
description: Terima catatan audit atas akses manusia terhadap data organisasi Anda oleh personel Anthropic melalui Compliance API.
---

Pelajari bagaimana "Access Transparency" (Transparansi Akses) membuat catatan atas akses manusia terhadap data organisasi Anda oleh personel Anthropic, apa saja yang dicakupnya, dan cara menerima event melalui Compliance API.

<Note>
  Ketika Access Transparency diaktifkan untuk organisasi Anda:

  * Setiap kali seorang karyawan Anthropic melihat data Anda yang disimpan (lihat [konten yang dicakup](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers)), sebuah aktivitas `anthropic_access` ditulis ke [Activity Feed Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) Anda.
  * Akses hanya terjadi untuk peninjauan keamanan atau respons insiden. Lihat [Kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes).

  Access Transparency tersedia bagi pelanggan yang memenuhi syarat berdasarkan permintaan dan tidak bersifat swalayan. Untuk kelayakan, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Cara kerja Access Transparency

Personel Anthropic mengakses konten pelanggan hanya dalam kondisi yang telah ditetapkan. Access Transparency dirancang untuk membuat akses tersebut terlihat oleh Anda. Rancangan ini bertumpu pada prinsip-prinsip berikut:

* **Akses manusia hanya terjadi berdasarkan kode alasan yang dipublikasikan.**
* **Setiap kali manusia melihat konten Anda yang dicakup, hal itu dicatat.** Perangkat internal Anthropic yang dapat menjangkau konten Anda yang dicakup telah diinstrumentasi untuk memancarkan event pada setiap tampilan.
* **Event merepresentasikan akses manusia, bukan pemrosesan otomatis.** Sistem keamanan otomatis Anthropic memproses konten Anda dalam pipeline yang diamankan tanpa akses manusia interaktif; pemrosesan tersebut tidak menghasilkan event `anthropic_access`. Satu-satunya event yang dapat dipicu oleh pemrosesan otomatis adalah catatan preservasi `cmek_preserve` (lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation)).
* **Event tiba di feed Anda yang sudah ada.** Aktivitas dapat diakses melalui [Activity Feed Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) Anda. Kredensial, audit, ekspor, dan integrasi SIEM yang sudah ada untuk Compliance API akan tetap berlaku.

## Apa yang dicakup Access Transparency

* **Konten yang dicakup:** Access Transparency mencakup konten prompt dan respons yang dikirim melalui Claude Messages API atau sesi Claude Code. [Dokumentasi ZDR umum](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) Anthropic dan [dokumentasi ZDR untuk Claude Code](https://code.claude.com/docs/id/zero-data-retention) menjelaskan API dan fitur mana yang dicakup oleh ZDR. API dan fitur yang sama dicakup oleh Access Transparency.
* **Tampilan manual oleh personel Anthropic:** Tampilan manual atas konten Anda yang dicakup oleh peninjau Anthropic menghasilkan event.

## Apa yang tidak dicakup Access Transparency

* **Pemrosesan otomatis:** Penyajian model, pengklasifikasi keamanan, dan pipeline deteksi penyalahgunaan memproses konten Anda sebagai bagian dari operasi normal dan tidak menghasilkan event `anthropic_access`. Preservasi yang dipicu oleh pemrosesan otomatis memang menghasilkan event `cmek_preserve` (lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation)).
* **Aktivitas organisasi Anda sendiri:** Panggilan API, tindakan admin, dan pembacaan Compliance API Anda dicakup oleh tipe event [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) standar.
* **Claude for Enterprise dan Claude Apps:** Seat claude.ai Enterprise, Claude for Work, Cowork, dan Claude in Chrome tidak dicakup.
* **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max.
* **Platform yang dioperasikan mitra:** Amazon Bedrock dan Google Cloud; lihat kontrol transparansi platform tersebut.
* **Apa pun yang tidak dicakup ZDR:** Produk yang tidak dicakup oleh ZDR (misalnya, Files API, aplikasi stateful yang di-hosting Anthropic, dan Batch API) tidak dicakup oleh Access Transparency. Lihat [dokumentasi ZDR](https://code.claude.com/docs/id/zero-data-retention#what-zdr-does-not-cover) untuk detail tambahan.

## Memulai

Untuk mengaktifkan Access Transparency:

<Steps>
  <Step title="Minta Access Transparency">
    Hubungi perwakilan akun Anthropic Anda.
  </Step>

  <Step title="Anthropic meninjau kelayakan">
    Anthropic mengonfirmasi bahwa organisasi Anda memenuhi kriteria kelayakan dan mengaktifkan kapabilitas ini di tingkat organisasi.
  </Step>

  <Step title="Terima event melalui Compliance API">
    Aktivitas `anthropic_access` muncul di Activity Feed Anda yang sudah ada di bawah Compliance Access Key Anda yang sudah ada; tidak diperlukan endpoint atau kredensial baru.
  </Step>
</Steps>

Access Transparency diaktifkan di tingkat organisasi dan mencakup semua workspace. Pendaftaran per workspace saat ini tidak tersedia.

## Menerima event Access Transparency

Event Access Transparency dikirimkan sebagai tipe aktivitas `anthropic_access` pada Activity Feed Compliance API. Filter dengan `activity_types[]`:

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --data-urlencode "activity_types[]=anthropic_access" \
  --data-urlencode "limit=50" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Paginasi, pemfilteran rentang tanggal (`created_at.gte` / `.lt`), dan envelope respons (`has_more`, `first_id`, `last_id`) sama dengan bagian lain dari Activity Feed. Lihat [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

Setiap aktivitas `anthropic_access` membawa field Activity standar ditambah yang berikut:

| Field                     | Tipe             | Deskripsi                                                                                                                                              |
| ------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                      | string           | Pengidentifikasi unik untuk aktivitas ini                                                                                                              |
| `accessed_at`             | string RFC 3339  | Kapan akses terjadi. Mungkin lebih awal daripada saat aktivitas terlihat di feed Anda                                                                  |
| `created_at`              | string RFC 3339  | Kapan aktivitas menjadi terlihat di feed Anda                                                                                                          |
| `actor`                   | object           | Selalu `{ "type": "anthropic_actor", "email_address": null }`. Identitas karyawan individual tidak diungkapkan                                         |
| `accessor_department`     | string           | Tim Anthropic yang melakukan akses (misalnya, `Safeguards`)                                                                                            |
| `reason_code`             | enum             | Lihat [Kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes)                                                |
| `resource_details.type`   | enum             | Tipe resource, saat ini hanya `message`. Dapat diperluas untuk tipe resource di masa mendatang                                                         |
| `resource_details.id`     | string atau null | Pengidentifikasi konten yang diakses                                                                                                                   |
| `resource_details.parent` | string atau null | Pengidentifikasi induk konten, misalnya ID percakapan yang berisi sebuah pesan. Saat ini `null` atau dihilangkan hingga resource dengan induk didukung |
| `organization_id`         | string           | Organisasi pemilik konten. Format tagged ID (`org_...`)                                                                                                |
| `organization_uuid`       | string           | Organisasi pemilik konten. Format UUID                                                                                                                 |
| `workspace_id`            | string atau null | Workspace pemilik konten                                                                                                                               |

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

Dalam kasus yang jarang terjadi, Anthropic mempreservasi konten tertentu melampaui jendela retensi standar (misalnya, ketika peninjauan keamanan mengonfirmasi konten yang sangat berbahaya yang harus disimpan untuk investigasi yang sedang berlangsung). Preservasi itu sendiri merupakan tindakan yang dicatat dan terlihat oleh pelanggan:

* **Event preservasi ditulis ke feed Anda.** Ketika konten dipreservasi, sebuah event dengan tipe `cmek_preserve` ditulis ke Activity Feed Compliance API Anda. Event preservasi membawa field yang sama dengan event `anthropic_access`; hanya tipe event-nya yang berbeda, sehingga parser yang menangani salah satunya dapat menangani keduanya. Lihat [Kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes).
* **Event preservasi ditulis terlepas dari bagaimana preservasi tersebut dipicu.** Preservasi biasanya mengikuti peninjauan manusia atas konten, tetapi event ditulis baik preservasi dipicu oleh peninjau manusia maupun oleh pipeline keamanan otomatis: catatan tersebut mencerminkan bahwa status retensi konten Anda berubah, terlepas dari siapa yang mengubahnya.
* **Untuk organisasi CMEK, preservasi adalah perpindahan kunci yang terlihat.** Konten yang dipreservasi dienkripsi ulang di luar kunci yang dikelola pelanggan Anda sehingga investigasi dapat berlanjut secara independen dari kunci Anda. Event preservasi adalah catatan Anda bahwa hal ini terjadi. Semua konten lain yang disimpan tetap berada di bawah kunci Anda.

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
| `incident_response`              | Konten dilihat saat menginvestigasi insiden yang memengaruhi organisasi Anda      |
| `policy_violation_investigation` | Konten dipreservasi selama investigasi pelanggaran kebijakan Trust and Safety     |
| `csae_report`                    | Konten dipreservasi sebagai bukti untuk laporan keselamatan anak (CSAE)           |

## Kelayakan surface

Tabel berikut mencantumkan surface mana yang dicakup oleh Access Transparency. Cakupan berarti akses manusia terhadap konten dari surface tersebut menghasilkan event `anthropic_access`.

| Surface                                         | Dicakup | Detail                                                                                                       |
| ----------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| Claude API (`api.anthropic.com`)                | Ya      | Prompt, completion, dan data yang disematkan langsung dalam input API                                        |
| Claude Code (menggunakan kunci API)             | Ya      | Lalu lintas API dari Claude Code dicakup sebagai lalu lintas Claude API                                      |
| Claude Platform on AWS                          | Ya      | Claude Platform on AWS menghasilkan event Access Transparency di dalam Compliance API (bukan AWS CloudTrail) |
| Claude API (`api.anthropic.com`) (Batch, Files) | Tidak   | Batch API dan Files API pada Claude API tidak dicakup, sama seperti keduanya tidak dicakup oleh ZDR          |
| Claude for Enterprise (seat claude.ai)          | Tidak   | Tidak dicakup                                                                                                |
| Claude for Work                                 | Tidak   | Tidak dicakup                                                                                                |
| Claude Free, Pro, Max                           | Tidak   | Paket konsumen tidak memenuhi syarat                                                                         |
| Playground (Claude Console)                     | Tidak   | Tidak dicakup                                                                                                |
| Microsoft Foundry                               | Tidak   | Tidak tersedia                                                                                               |
| Amazon Bedrock, Google Cloud                    | Tidak   | Platform yang dioperasikan mitra; lihat kontrol transparansi platform tersebut                               |

## Batasan dan pengecualian

### Waktu cakupan

Access Transparency berlaku sejak diaktifkan untuk organisasi Anda. Konten yang sudah berada dalam jendela retensi Anda pada saat pengaktifan mungkin juga menghasilkan event ketika diakses, tetapi Anthropic tidak menjamin cakupan untuk konten yang ditulis sebelum pengaktifan. Perlakukan tanggal pengaktifan Anda sebagai awal cakupan yang andal. Mungkin terdapat penundaan hingga dua jam antara pengaktifan Access Transparency dan konten Anda mulai dicakup.

### Waktu notifikasi

Event `anthropic_access` dan `cmek_preserve` dikirimkan ke feed Compliance API Anda dalam waktu dua hari kerja sejak akses atau preservasi yang dicatatnya. Feed ini tidak boleh diperlakukan sebagai saluran peringatan real-time, dan timestamp `accessed_at` mencerminkan kapan akses terjadi, yang mungkin hingga dua hari kerja sebelum aktivitas terlihat di feed Anda. Field `created_at` mencerminkan waktu ketika event menjadi terlihat.

### Pemrosesan otomatis tidak menghasilkan event akses

Event `anthropic_access` hanya mencatat akses manusia. Sistem keamanan otomatis dan pengklasifikasi Anthropic terus memproses konten Anda sebagai bagian dari operasi normal, dan pemrosesan tersebut tidak menghasilkan event `anthropic_access`. Satu-satunya event yang dapat dipicu oleh pemrosesan otomatis adalah catatan preservasi `cmek_preserve` (lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation)). Feed yang kosong berarti tidak ada manusia di Anthropic yang telah melihat konten Anda; ini tidak berarti konten Anda tidak diproses oleh sistem otomatis.

### Access Transparency tidak mengubah apa yang dapat diakses Anthropic

Access Transparency mencatat akses; fitur ini tidak memberikan atau membatasinya. Tujuan-tujuan yang memperbolehkan personel Anthropic mengakses konten Anda diatur oleh perjanjian Anda dengan Anthropic dan [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup), dan tetap sama terlepas dari apakah Access Transparency diaktifkan atau tidak.

### Log penggunaan kunci CMEK bukan catatan per pembacaan

Untuk organisasi yang juga mengaktifkan CMEK, log audit KMS cloud Anda (CloudTrail, Cloud Audit Logs, atau Azure Monitor) mencatat penggunaan kunci Anda oleh Anthropic. Karena kunci di-cache untuk periode singkat selama operasi, satu pembacaan manusia tidak selalu menghasilkan entri dekripsi KMS yang terpisah. Gunakan feed Access Transparency sebagai catatan per akses; log KMS Anda secara independen mengonfirmasi pola penggunaan kunci.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Bagaimana saya tahu apakah organisasi saya telah mengaktifkan Access Transparency?">
    Hubungi perwakilan akun Anthropic Anda.
  </Accordion>

  <Accordion title="Apakah saya akan melihat event setiap kali pengklasifikasi keamanan berjalan pada lalu lintas saya?">
    Tidak. Pemrosesan otomatis tidak menghasilkan event `anthropic_access`; Anda hanya akan melihat event `anthropic_access` jika seorang peninjau manusia kemudian melihat konten tersebut. Secara terpisah, event `cmek_preserve` ditulis ketika konten dipreservasi, baik preservasi tersebut dipicu oleh peninjau manusia maupun pipeline keamanan otomatis.
  </Accordion>

  <Accordion title="Kami adalah platform yang menyajikan Claude kepada pengguna akhir kami sendiri. Dapatkah kami mengaktifkan Access Transparency?">
    Access Transparency tidak tersedia untuk deployment platform. Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan kasus penggunaan Anda.
  </Accordion>

  <Accordion title="Apakah saya akan melihat event untuk akses yang terjadi sebelum kami mendaftar, atau untuk data lama kami?">
    Access Transparency tidak dijamin berlaku surut. Fitur ini mencakup akses manusia terhadap konten yang ditulis ke Claude API pada atau setelah tanggal pendaftaran Anda. Anda mungkin melihat event untuk akses terhadap konten yang ditulis sebelum pendaftaran.
  </Accordion>

  <Accordion title="Seberapa cepat setelah akses saya akan melihat event-nya?">
    Dalam waktu dua hari kerja sejak akses. Konfigurasikan peringatan SIEM atau ekspor terjadwal apa pun dengan jendela lookback yang sesuai alih-alih mengasumsikan kedatangan real-time.
  </Accordion>

  <Accordion title="Bagaimana saya tahu permintaan mana yang dirujuk oleh event anthropic_access?">
    Gunakan field `resource_details.id`. Field ini berisi ID pesan yang sama (`msg_...`) yang dikembalikan oleh [Messages API](https://platform.claude.com/docs/id/api/messages/create) dalam field `id` pada setiap body respons. Agar ini berguna, catat `id` di sistem Anda sendiri bersama metadata internal Anda, seperti aplikasi, pengguna akhir, atau percakapan yang menghasilkan permintaan tersebut. Ketika sebuah event tiba, gabungkan `resource_details.id`-nya dengan log Anda untuk mengidentifikasi secara tepat permintaan mana yang dilihat.
  </Accordion>

  <Accordion title="Dapatkah saya mengaktifkan Access Transparency untuk satu workspace saja?">
    Access Transparency diaktifkan di tingkat organisasi dan mencakup semua workspace.
  </Accordion>

  <Accordion title="Bagaimana hubungan Access Transparency dengan CMEK?">
    Keduanya independen. Dengan CMEK, preservasi keamanan di luar kunci Anda memancarkan event `cmek_preserve` terpisah pada feed yang sama. Lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation) dan [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek).
  </Accordion>

  <Accordion title="Bagaimana cara meminta Access Transparency?">
    Hubungi perwakilan akun Anthropic Anda.
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Ikhtisar Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api)
* [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed)
* [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention)
* [Customer-Managed Encryption Keys (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek)
* [Penggunaan data Claude Code](https://code.claude.com/docs/id/data-usage)
* [Trust Center](https://trust.anthropic.com/resources)
