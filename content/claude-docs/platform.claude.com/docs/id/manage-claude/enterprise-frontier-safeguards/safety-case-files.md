---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: 974cb05dc7b5d18cecdaf8cbf2d931dd530327ca97d83a26f4eaa45ec12b81cd
---

---
title: File Safety Case
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files
description: File yang ditulis Anthropic ke bucket kasus Anda, serta file respons yang ditulis kembali oleh tim Anda.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Halaman ini menjelaskan file Safety Case dan transkrip di [bucket kasus](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) Anda beserta format masing-masing. Anda memilih bucket tersebut di bawah **Safety Case and Transcript storage**. Untuk menyiapkan bucket tersebut, lihat [Menyiapkan penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage). Untuk mempelajari cara tim Anda meninjau dan menanggapi Safety Case, lihat [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases).

Safety Case meminta tim Anda untuk menyelidiki sekumpulan pesan. Cara kerjanya seperti ini:

1. Anthropic menulis Safety Case ke bucket Anda sebagai file JSON, dengan file transkrip untuk setiap pesan yang salinannya dimiliki Anthropic.
2. Tim Anda melakukan penyelidikan dan menulis file respons ke bucket yang sama.
3. Anthropic menutup Safety Case tersebut.

Anthropic juga dapat menulis Safety Notices tentang Safety Cases Anda.

Beberapa detail bergantung pada penyedia penyimpanan Anda:

* **Amazon S3:** Path, izin, dan pengaturan kedaluwarsa di halaman ini berlaku untuk Amazon S3.
* **Google Cloud Storage:** Di bucket yang terhubung di Claude Console, setiap path diawali dengan folder yang dinamai sesuai ID organisasi Anthropic Anda (lihat [Menggunakan bucket Cloud Storage Anda di workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace)).

## Isi bucket

| Prefiks | Isinya | Siapa yang membutuhkannya | Kedaluwarsa setelah |
| ----- | ----- | ----- | ----- |
| `review-cases/` | Satu [file Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#safety-case-file) untuk setiap Safety Case | Tim triase dan peninjau, untuk dibaca | 2.555 hari (sekitar 7 tahun) secara default |
| `review-notices/` | [Safety Notices](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#notice) yang ditulis Anthropic sebagai file, masing-masing satu file | Tim triase dan peninjau, untuk dibaca | 2.555 hari secara default |
| `transcripts/flagged/` | [Transkrip](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#transcript) dari setiap pesan dalam Safety Case | Peninjau, untuk dibaca | Hingga 30 hari |
| `review-responses/` | [File respons](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file) Anda untuk setiap Safety Case | Peninjau, untuk ditulis | 2.555 hari secara default |

Anthropic merekomendasikan pemisahan akses berdasarkan prefiks, sehingga orang yang melakukan triase peringatan tidak melihat prompt dan respons. Setiap peran membutuhkan izin berikut:

* **Untuk membaca:** Seseorang membutuhkan `s3:GetObject` pada prefiks, `s3:ListBucket` pada bucket, dan `kms:Decrypt` pada kunci bucket. Batasi `s3:ListBucket` ke prefiks dengan kondisi `s3:prefix`. Bagian lain dari `transcripts/` dapat berisi permintaan yang tidak menghasilkan Safety Case.
* **Untuk menulis respons:** Peninjau juga membutuhkan `s3:PutObject` pada `review-responses/*` dan `kms:GenerateDataKey` pada kunci.

Untuk menyimpan Safety Cases, Safety Notices, atau respons lebih lama dari default, atur `ReviewExpiryDays` (CloudFormation) atau `review_expiry_days` (Terraform) saat Anda men-deploy [file penyiapan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#template-reference). Setelah salah satu file ini kedaluwarsa, diganti, atau dihapus, file tersebut tetap ada sebagai versi nonkini (noncurrent version) hingga jumlah hari tersebut.

Jangan mengedit aturan siklus hidup bucket secara langsung. Bucket yang tidak memiliki aturan yang diwajibkan, atau yang menambahkan aturan kedaluwarsa, akan gagal dalam **Test setup** atau pemeriksaan berikutnya. Transkrip kedaluwarsa setelah paling lama 30 hari, jadi salin transkrip yang Anda butuhkan lebih lama ke penyimpanan lain.

## Peringatan untuk file baru

Siapkan peringatan untuk setiap file Safety Case dan file Safety Notice baru, sehingga tim Anda dapat merespons dengan cepat.

### Amazon S3

Ada dua cara untuk mendapatkan peringatan tanpa mengubah bucket:

* **Membuat daftar sesuai jadwal.** Jalankan tugas berulang yang membuat daftar `review-cases/` dan `review-notices/` dengan `ListObjectsV2`. Minta tugas tersebut membandingkan setiap daftar dengan daftar dari eksekusi sebelumnya, dan memberikan peringatan untuk setiap objek baru.
* **Mencocokkan penulisan di AWS CloudTrail.** [Aktifkan data event CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#cloudtrail) untuk kedua prefiks tersebut, dan cocokkan `PutObject` serta `CompleteMultipartUpload` dalam aturan Amazon EventBridge.

Anthropic tidak merekomendasikan untuk mengubah pengaturan notifikasi bucket itu sendiri untuk mendapatkan peringatan. File penyiapan meminta Anda untuk tidak mengedit konfigurasi bucket setelah Anda men-deploy-nya, kecuali untuk mengatur `ReviewExpiryDays`.

Anthropic dapat menimpa file Safety Case, misalnya saat Safety Case ditutup, sehingga aturan Amazon EventBridge dapat mencocokkan file yang sama lebih dari sekali. Baca `status` di dalam file.

### Google Cloud Storage

Di bucket Google Cloud Storage, `review-cases/` dan `review-notices/` berada di dalam folder yang dinamai sesuai ID organisasi Anthropic Anda. Buat daftar `<organization ID>/review-cases/` dan `<organization ID>/review-notices/` sesuai jadwal dengan metode `Objects: list` dari JSON API, dan berikan peringatan untuk setiap objek baru.

## File Safety Case

Saat Anthropic mengirimkan Safety Case baru kepada Anda, Anthropic menulisnya ke `review-cases/<id>.json` dalam format berikut:

```json
{
  "schema_version": 1,
  "id": "rvc_01Hq3Zt8KpWv5NcR2yLbXs7D",
  "status": { "type": "open" },
  "created_at": "2026-11-23T18:42:07Z",
  "updated_at": "2026-11-23T18:42:07Z",
  "workspace_id": "wrkspc_01AbCdEfGhJkLmNpQrStUvWx",
  "policy_categories": ["cyber"],
  "enforcement_action": null,
  "transcripts": [
    {
      "item_id": "msg_01XFDUDYJgAACzvnptvVoYEL",
      "object_key": "transcripts/flagged/4da8b33b-8235-3151-ffb5-1e5cc2230505/MESSAGE_SOURCE_PUBLIC_API_SAMPLING_CALL-msg_01XFDUDYJgAACzvnptvVoYEL.json"
    }
  ],
  "derived_data_object_keys": []
}
```

| Field | Isinya |
| ----- | ----- |
| `schema_version` | Versi format. Versi berikutnya dapat menambahkan field. |
| `id` | ID Safety Case, yang diawali dengan `rvc_`. ID ini menjadi nama file ini dan file respons Anda, dan [API Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api) menggunakan ID yang sama. |
| `status.type` | `open` atau `closed` |
| `status.reason` | Hanya ada di file yang ditutup. `null` jika Anthropic tidak memberikan alasan. Jika tidak, berupa objek yang `type`-nya menyatakan alasan Safety Case ditutup. Tabel berikutnya mencantumkan nilai-nilainya. |
| `created_at` | Waktu Anthropic mengirimkan Safety Case, dalam UTC. Tenggat 7 hari kalender untuk merespons dihitung sejak waktu ini. |
| `updated_at` | Waktu terakhir Anthropic memperbarui file ini, dalam UTC |
| `workspace_id` | ID workspace yang mengirimkan pesan, atau `null` jika pesan tidak menyebutkan workspace. ID diawali dengan `wrkspc_`. |
| `policy_categories` | Jenis risiko yang ditemukan oleh pemantauan keselamatan otomatis, seperti `cyber` atau `bio`. Anthropic dapat menambahkan nilai, jadi arahkan nilai yang tidak Anda kenal ke antrean default Anda. |
| `enforcement_action` | Objek yang `type`-nya menyebutkan tindakan yang diambil Anthropic sebelum mengirimkan Safety Case, atau `null`. Berikan peringatan untuk nilai apa pun selain `null`. |
| `transcripts[].item_id` | ID pesan: `id` dari respons Messages API |
| `transcripts[].user_profile_id` | Profil pengguna yang mengirimkan pesan. Anthropic dapat menghilangkan kunci JSON ini, meskipun Anda mengirimkan profil pengguna. |
| `transcripts[].object_key` | Lokasi transkrip pesan di bucket Anda, atau `null` jika Anthropic tidak menyimpan salinan. Objek juga bisa tidak ada. Folder dalam kunci objek ini adalah UUID workspace (bukan ID `wrkspc_`-nya), atau `default` jika pesan tidak menyebutkan workspace. |
| `derived_data_object_keys` | Kunci objek dari file tambahan apa pun yang ditambahkan Anthropic tentang Safety Case. Daftar kosong jika tidak ada. |

`status.reason.type` memiliki nilai-nilai berikut:

| `status.reason.type` | Artinya |
| ----- | ----- |
| `responded` | Anthropic telah menerima respons Anda. |
| `window_ended` | Tidak ada respons valid dalam 7 hari kalender sejak `created_at`. |
| `ended_by_anthropic` | Anthropic mengakhiri Safety Case sebelum 7 hari kalender berakhir. |

Anthropic dapat menambahkan nilai.

Jangan memindahkan atau mengedit file ini, dan jangan menghapusnya selama `status.type`-nya masih `open`. Anthropic memperbaruinya di tempat, misalnya saat Safety Case ditutup. Jika Anthropic tidak dapat menemukan file yang valid, Anthropic tidak menulis file yang ditutup.

## Transkrip

Transkrip adalah salinan yang dapat dibaca dari satu pesan: prompt Anda dan respons Claude. File Safety Case memberikan lokasi setiap transkrip di `object_key`. Setiap transkrip adalah objek JSON dengan field berikut:

| Field | Isinya |
| ----- | ----- |
| `id` | ID pesan |
| `request`, `response` | Pesan, dalam format Messages API. `request` menyertakan parameter [`metadata`](https://platform.claude.com/docs/id/api/messages/create#create.metadata) yang Anda kirimkan, yang berisi `user_id`. `response` dapat bernilai `null`. |
| `request_time` | Waktu Anthropic mencatat pesan |
| `organization_uuid`, `workspace_uuid` | Organisasi dan workspace yang mengirimkannya. `workspace_uuid` adalah UUID workspace, bukan ID `wrkspc_`-nya, dan bernilai `null` jika pesan tidak menyebutkan workspace. |
| `source` | Asal pesan |
| `schema_version` | Versi format |

Transkrip bukan salinan persis dari pesan. Anthropic menyamarkan token server MCP dan menghapus blok thinking, dan gambar atau dokumen dapat muncul sebagai placeholder.

## Safety Notice

Safety Notice adalah pesan dari Anthropic tentang satu atau lebih Safety Cases Anda, atau tentang organisasi Anda secara keseluruhan. Safety Notice dapat berupa permintaan untuk merespons, peringatan, atau pertanyaan. Anthropic tidak menulis setiap Safety Notice sebagai file, tetapi API Safety Cases mencantumkan semuanya (lihat [Polling untuk Safety Notices](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll-for-notices)). File Safety Notice berada di `review-notices/<id>.json`, dan Anthropic tidak pernah mengubahnya:

```json
{
  "schema_version": 1,
  "id": "rvn_01Jt5Yw2MnQx8VbK4zRcHd6F",
  "case_ids": ["rvc_01Hq3Zt8KpWv5NcR2yLbXs7D"],
  "kind": { "type": "response_requested" },
  "created_at": "2026-11-27T18:00:00Z",
  "message": "Anthropic has found no valid response to the Case in case_ids. Review the Case and write your response file before the time in respond_by. If you wrote a valid response file in the last hour, ignore this notice.",
  "respond_by": "2026-11-30T18:42:07Z"
}
```

| Field | Isinya |
| ----- | ----- |
| `id` | ID Safety Notice, yang diawali dengan `rvn_`. ID ini menjadi nama file ini. |
| `case_ids` | `id` dari setiap Safety Case yang dibahas dalam Safety Notice. Daftar kosong berarti organisasi Anda secara keseluruhan. |
| `kind.type` | `response_requested`, `warning`, atau `question` |
| `message` | Teks permintaan, peringatan, atau pertanyaan, hingga 2.000 karakter. Teks ini tidak pernah mengutip transkrip. |
| `respond_by` | Waktu Anthropic meminta jawaban, atau `null`. Ini tidak memperpanjang tenggat 7 hari kalender untuk menanggapi Safety Case. |

Untuk menjawab `response_requested`, tulis file respons Anda. Untuk menjawab pertanyaan, hubungi tim akun Anthropic Anda.

## File respons

File respons memberi tahu Anthropic bahwa tim Anda telah menyelidiki Safety Case, dan apa yang ditemukannya. File ini adalah cara Anda menanggapi Safety Case tanpa [API Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api). Tulis ke `review-responses/<case_id>.json`, atau `<organization ID>/review-responses/<case_id>.json` di Google Cloud Storage:

```json
{
  "schema_version": 1,
  "case_id": "rvc_01Hq3Zt8KpWv5NcR2yLbXs7D",
  "submitted_at": "2026-11-25T16:02:10Z",
  "determination": "violation",
  "policy_categories": ["cyber"],
  "verdicts": [
    {
      "item_id": "msg_01XFDUDYJgAACzvnptvVoYEL",
      "determination": "violation",
      "policy_category": "cyber"
    }
  ]
}
```

| Field | Yang dikirim |
| ----- | ----- |
| `schema_version` | Versi skema respons Anda. Satu-satunya nilai yang diterima adalah angka `1`. |
| `case_id` | `id` Safety Case, sama dengan yang ada di nama file |
| `submitted_at` | Waktu Anda merespons, sebagai waktu ISO 8601 dengan offset, seperti `Z` |
| `determination` | `violation` atau `no_violation`, untuk Safety Case secara keseluruhan |
| `policy_categories` | Dengan `violation`, satu hingga empat kategori yang Anda konfirmasi. Gunakan nilai dari `policy_categories` milik Safety Case itu sendiri, atau `other` jika tidak ada yang sesuai. Dengan `no_violation`, hilangkan field ini atau kirimkan daftar kosong. |
| `verdicts` | Opsional, dan tidak pernah `null`. Untuk menilai pesan secara terpisah, berikan daftar dengan satu entri untuk setiap pesan yang Anda nilai. Setiap entri memiliki `item_id`, `determination`, dan, dengan `violation`, `policy_category` opsional. Daftar ini tidak harus mencakup setiap pesan. |

### Aturan untuk file yang valid

Anthropic tidak memberi tahu Anda jika file tidak valid, jadi periksa file Anda berdasarkan aturan berikut:

* File berada di `review-responses/<case_id>.json` (di Google Cloud Storage, `<organization ID>/review-responses/<case_id>.json`), dengan ID yang sama seperti field `case_id`-nya. Gunakan `id` Safety Case, yang diawali dengan `rvc_`.
* File memiliki field `schema_version`, `case_id`, `submitted_at`, dan `determination`, dan tidak ada field yang tidak ada dalam tabel.
* `policy_categories` memiliki satu hingga empat nilai dengan `violation` dan tidak ada nilai dengan `no_violation`, dan tidak ada nilai yang muncul dua kali. Tidak ada `item_id` yang muncul dua kali dalam `verdicts`.
* Setiap kategori adalah nilai yang dapat dimiliki Safety Case, seperti `cyber` atau `other`.
* Setiap `item_id` dalam `verdicts` ada di dalam Safety Case.
* File berupa JSON biasa berukuran paling banyak 256 kB, tanpa byte order mark dan tanpa kunci ganda. Windows PowerShell 5.1 menambahkan byte order mark, yang membuat file tidak valid, sehingga Anthropic memperlakukannya sebagai tidak ada respons.
* File menggunakan enkripsi default bucket Anda.

Anthropic menghitung respons valid pertama yang dibacanya, dan Anda tidak dapat mengubahnya setelah itu. Sampai saat itu, Anda dapat mengganti file tersebut.

Sebelum Anda mengubah atau menghapus [bucket data keselamatan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) atau bucket kasus milik workspace, tanggapi Safety Cases yang masih terbuka di workspace tersebut dan tunggu hingga semuanya ditutup. Jika Anda mengubah atau menghapus bucket terlebih dahulu, Anthropic mungkin tidak membaca file respons Anda.

### Mengapa Safety Case tetap terbuka

Anthropic memeriksa `review-responses/` sesuai jadwal, jadi berikan waktu satu hari. File valid yang Anda tulis dalam 7 hari kalender tetap dihitung, meskipun Anthropic membacanya kemudian. Jika `status.type` masih `open` satu hari setelah Anda menulis file, periksa file Anda berdasarkan [Aturan untuk file yang valid](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file-rules) dan ganti file tersebut.

Saat Anthropic membaca respons yang valid, Anthropic menulis ulang file Safety Case dengan `status.type` diatur ke `closed`. Baca `status.reason` di file tersebut:

* **`status.reason.type` bernilai `responded`:** Ini mengonfirmasi bahwa Anthropic telah menerima respons Anda.
* **`status.reason` bernilai `null`:** Ini dapat terjadi meskipun Anthropic telah menerima respons Anda. Di Claude Platform, baca Safety Case melalui [API Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api), yang selalu memberikan alasan.

Safety Case yang sudah ditutup tidak dibuka kembali, dan Anthropic mengabaikan file respons yang ditulis setelah Safety Case ditutup.
