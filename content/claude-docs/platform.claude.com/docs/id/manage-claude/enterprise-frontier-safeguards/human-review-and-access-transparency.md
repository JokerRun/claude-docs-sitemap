---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: a4b2a98328bdd2111b94e5ca434cfbc81bd7e01dcd40f8e4b908aec852e3de1d
---

---
title: Human Review dan Access Transparency
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency
description: Nonaktifkan Anthropic Human Review dan periksa catatan akses Anthropic ke data Anda.
---

<Warning>
  Enterprise Data Controls berada dalam beta di Claude Platform. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Pemantauan keselamatan otomatis Anthropic memeriksa prompt dan respons Anda, dan tim kecil khusus di Anthropic dapat meninjau temuannya. Hal ini disebut Anthropic Human Review, dan secara default aktif untuk workspace baru yang menggunakan penyimpanan yang dikelola Anthropic.

Di Claude Platform, Enterprise Data Controls memungkinkan Anda [menonaktifkan Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) pada penyimpanan yang dikelola Anthropic. [Enterprise Frontier Safeguards (EFS)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) memungkinkan Anda [menggunakan penyimpanan Anda sendiri](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage) dan [melakukan peninjauan Anda sendiri](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). Organisasi enterprise yang memenuhi syarat di Claude Platform dapat memperoleh keduanya dengan menyetujui ketentuan dari halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console. Sebelum Anda menyetujuinya, baca [Apa yang berubah saat Anda mendapatkan akses](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access).

[Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) memberi Anda catatan setiap kali seseorang di Anthropic melihat data Anda. Access Transparency tidak mencakup setiap bagian data di organisasi Anda. Lihat [apa yang tidak dicakup Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-does-not-cover).

## Kapan pemantauan keselamatan otomatis mengakses data Anda?

Tabel berikut menunjukkan bagaimana dan kapan pemantauan keselamatan otomatis dan Anthropic Human Review dapat mengakses data Anda:

| Siapa | Kapan | Catatan apa yang Anda dapatkan |
| ----- | ----- | ----- |
| Sistem pemantauan keselamatan otomatis | Setiap workspace dengan penyimpanan yang dikelola Anthropic atau Enterprise Frontier Safeguards. Tidak pada workspace dengan **Legacy ZDR**. Sistem ini memeriksa prompt dan respons Anda untuk mendeteksi penyalahgunaan. Pemeriksaan ini sepenuhnya otomatis, sehingga tidak ada orang yang melihat konten Anda pada tahap ini. | Tidak ada [event `anthropic_access`](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency). |
| Tim kecil khusus berisi peninjau yang disetujui di Anthropic | Hanya selama Anthropic Human Review aktif. Hanya tim ini yang meninjau temuan pemantauan keselamatan otomatis. Lihat [kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes) untuk jenis alasan Anthropic mengakses konten. | Sebuah event `anthropic_access` setiap kali seseorang melihat data Anda, jika akses tersebut termasuk dalam [cakupan Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers). |

Dengan [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage), sistem Anthropic menulis data keselamatan tersegel Anda ke bucket Anda dan membacanya kembali untuk menjalankan pemantauan keselamatan otomatis. Untuk bucket Amazon S3, lihat [Panggilan Anthropic di AWS CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#cloudtrail).

## Nonaktifkan Anthropic Human Review

Jika Anda telah mengonfigurasi Enterprise Frontier Safeguards untuk sebuah workspace, tim Anda sendiri mendapatkan [Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) untuk ditinjau, alih-alih tim Anthropic. Pastikan Anda telah membaca [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#where-cases-arrive) sebelum menonaktifkan Anthropic Human Review.

Layanan Claude Managed Agents dari Anthropic tidak menjalankan sesi atau [dreams](https://platform.claude.com/docs/id/managed-agents/dreams) di workspace yang Anthropic Human Review-nya nonaktif. Sesi yang sudah ada di workspace tersebut berhenti menerima pesan baru. [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) juga menolak batch baru di workspace tersebut. Untuk menjalankan sesi, dreams, atau batch, buat semuanya di workspace yang Anthropic Human Review-nya aktif.

Untuk mengonfigurasi Anthropic Human Review untuk sebuah workspace, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) sebagai Admin organisasi. Perubahan dapat memerlukan waktu hingga 2 jam untuk diterapkan. Workspace yang menggunakan Enterprise Frontier Safeguards selalu memiliki Anthropic Human Review nonaktif. Di Claude Models on Google Cloud (Anthropic managed) dan Claude Platform on AWS, menggunakan Enterprise Frontier Safeguards adalah satu-satunya cara untuk menonaktifkannya.

Anda dapat memberlakukan pengaturan Anthropic Human Review di seluruh workspace baru Anda dengan [menetapkan kebijakan workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#set-organization-defaults) di halaman [Retensi data](https://platform.claude.com/settings/privacy) organisasi Anda.

Untuk informasi lebih lanjut, lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console), [Aktifkan EFS di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#turn-on-efs-for-a-workspace), atau [Aktifkan EFS di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#turn-on-efs-for-a-workspace).

## Periksa Access Transparency

Access Transparency memberi Anda catatan setiap kali seseorang di Anthropic melihat data Anda. Catatan ini muncul sebagai event `anthropic_access` di Activity Feed Compliance API Anda. Untuk batasan tentang apa yang dicatat, lihat [cakupan Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers).

Bagi pelanggan Claude Platform yang menggunakan Enterprise Frontier Safeguards atau Enterprise Data Controls, Access Transparency menjadi aktif untuk seluruh organisasi Anda saat pertama kali Anda mulai menghubungkan bucket, memasang kunci yang dikelola pelanggan, atau menonaktifkan Anthropic Human Review. Setelah aktif, Access Transparency mulai mencatat dalam 2 jam.

Compliance API harus aktif agar Anda dapat membaca event ini.

Jika Anda menonaktifkan Compliance API, Anthropic tetap mencatat event Access Transparency, dan Anda dapat membacanya setelah Anda mengaktifkannya kembali. Aktivitas lain organisasi Anda tidak dicatat selama Compliance API nonaktif dan tidak dapat dipulihkan nanti.

Untuk membaca event Access Transparency Anda, Anda memerlukan kunci yang dapat membaca Activity Feed. Jika Anda menggunakan Claude Platform on AWS, langsung lanjut ke [Di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency-on-aws).

<Steps>
  <Step title="Buat kunci">
    [Siapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) dan buat Compliance Access Key atau kunci Admin API yang dapat membaca Activity Feed.
  </Step>

  <Step title="Baca event anthropic_access">
    Baca event `anthropic_access` dari [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) Anda.
  </Step>
</Steps>

Di Claude Platform, hasil kosong tidak menunjukkan apa pun tentang data di penyimpanan milik pelanggan, karena saat ini tidak ada catatan Access Transparency untuk data tersebut. Untuk apa yang dicatat AWS CloudTrail di akun AWS Anda tentang bucket Anda, lihat [Panggilan Anthropic di AWS CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#cloudtrail).

Berikut cara membaca hasilnya:

* **Tidak ada event `anthropic_access`:** Activity Feed Anda tidak menunjukkan akses ke data Anda oleh personel Anthropic, untuk semua hal dalam [cakupan Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers). Sebuah event dapat tiba hingga 2 hari kerja setelah akses yang dicatatnya.
* **Sebuah event `anthropic_access`:** Seseorang di Anthropic melihat data Anda. Cari alasannya di [kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes).

Untuk memverifikasi event itu sendiri, lihat [Memverifikasi event Access Transparency dengan log transparansi](https://platform.claude.com/docs/id/manage-claude/access-transparency-log).

### Di Claude Platform on AWS

Di Claude Platform on AWS, Anda [menandatangani setiap permintaan dengan kredensial AWS Anda](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#sig-v4-authentication) alih-alih menggunakan kunci Compliance API. Untuk membaca Activity Feed Anda, kirim permintaan `GET` melalui HTTPS dengan bagian-bagian berikut:

* **Host:** `aws-external-anthropic.{region}.api.aws`, dengan `{region}` adalah region salah satu workspace Anda.
* **Path:** `/v1/compliance/activities`.
* **Header:** `anthropic-version: 2023-06-01`.
* **Filter (opsional):** `activity_types%5B%5D=anthropic_access` di query string, untuk hanya mendapatkan event Access Transparency. Biarkan tanda kurung siku tetap ter-encode, jika tidak, tanda tangan tidak akan cocok.

Principal IAM Anda memerlukan action `aws-external-anthropic:ListComplianceActivities`.

Berikut cara membaca respons tersebut:

* **Sebuah daftar, bahkan yang kosong:** Compliance API aktif. Sebuah event dapat memerlukan waktu hingga 2 hari kerja untuk muncul.
* **Sebuah event `anthropic_access`:** Seseorang di Anthropic melihat data Anda. [Kode alasan](https://platform.claude.com/docs/id/manage-claude/access-transparency#reason-codes) menjelaskan alasannya.
* **Error 400, `Compliance API is not enabled for this organization`:** Compliance API nonaktif. Aktifkan dengan toggle **Compliance API**, tunggu sekitar 1 menit, lalu kirim ulang permintaan Activity Feed.

Untuk mengaktifkan Compliance API, gunakan toggle **Compliance API** di halaman [Compliance](https://platform.claude.com/settings/security) di Claude Console. Principal IAM Anda memerlukan action `aws-external-anthropic:UpdateComplianceSettings` pada `Resource: "*"`. Policy `AnthropicFullAccess` mencakup action ini.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Tinjau Safety Cases" icon="file" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases">
    Tinjau temuan pemantauan keselamatan otomatis bersama tim Anda sendiri.
  </Card>

  <Card title="Periksa penyiapan Anda" icon="check" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#check-your-setup">
    Di Claude Platform, periksa bahwa data keselamatan tersegel sampai ke bucket Anda sebelum Anda mulai menggunakannya di produksi.
  </Card>
</CardGroup>
