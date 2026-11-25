---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: ef5d44e697bf183843c5e10696faeef31ff786308df07c353aa8fd4598d84f57
---

---
title: Menggunakan kunci yang dikelola pelanggan
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys
description: Enkripsi data Anda menggunakan kunci yang Anda simpan di layanan manajemen kunci milik Anda sendiri.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Dengan “customer-managed key” (kunci yang dikelola pelanggan), atau CMEK, Anthropic mengenkripsi data Anda menggunakan kunci yang Anda simpan di layanan manajemen kunci milik Anda sendiri: AWS KMS, Google Cloud KMS, atau Azure Key Vault. Dalam waktu sekitar satu jam setelah [menonaktifkan kunci Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#revoke-your-key), Anthropic tidak dapat lagi mendekripsi data yang dilindungi oleh kunci Anda.

Di Claude Console, Anda melampirkan kunci Anda ke setiap [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) yang menggunakannya, dan mendapatkan akses melalui [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS) atau [Enterprise Data Controls](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview#enterprise-data-controls).

## Sebelum Anda melampirkan kunci

Anda harus menjadi Admin organisasi untuk melampirkan kunci.

Organisasi Anda juga memerlukan akses ke kunci yang dikelola pelanggan. Untuk mendapatkan akses dengan EFS, ikuti bagian “Dapatkan akses” di [Menyiapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access). Untuk mendapatkan akses tanpa EFS, hubungi tim akun Anthropic Anda, seperti yang dijelaskan di [Siapa yang dapat menggunakan CMEK](https://platform.claude.com/docs/id/manage-claude/cmek#availability).

Melampirkan kunci pertama Anda akan mengaktifkan [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#access-transparency-with-customer-managed-keys) untuk seluruh organisasi Anda, kecuali jika sudah aktif. Anda tidak dapat menonaktifkannya. Dengan Access Transparency aktif, organisasi Anda tidak dapat [memanggil Claude API langsung dari browser](https://platform.claude.com/docs/id/manage-claude/authentication#browser-based-applications).

Kunci menonaktifkan beberapa fitur, dan [melampirkan kunci bersifat permanen](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key), jadi Anthropic menyarankan untuk membaca bagian-bagian berikut dari panduan kunci enkripsi yang dikelola pelanggan terlebih dahulu:

* [Apa yang berubah dengan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed): fitur-fitur yang dinonaktifkan oleh kunci.
* [Apa yang dicakup kunci](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#encrypted-with-your-key): apa yang dienkripsi oleh kunci Anda.
* [Apa arti mencabut kunci](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does): apa yang terjadi jika Anda mencabut atau menonaktifkan kunci Anda. Menghapus kunci Anda tidak dapat dibatalkan.

### Jika Anda menggunakan penyimpanan milik pelanggan

Workspace yang menggunakan penyimpanan milik pelanggan sekaligus kunci yang dikelola pelanggan memiliki dua kunci yang terpisah:

| Kunci | Tempat dibuat | Fungsinya |
| ----- | ----- | ----- |
| Kunci bucket Anda | Bersama bucket Anda, saat Anda [membuat bucket dan peran](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles) | Mengenkripsi bucket Anda. |
| Kunci yang dikelola pelanggan milik Anda | Di layanan manajemen kunci Anda, mengikuti panduan di bagian selanjutnya halaman ini | Mengenkripsi data Anda. Ini adalah kunci yang Anda lampirkan ke workspace. |

Jangan gunakan kunci yang sama untuk keduanya. Kunci mana yang mengenkripsi isi bucket Anda bergantung pada jenis datanya:

* **Data keselamatan tersegel:** Anthropic mengenkripsi konten dengan kunci yang dikelola pelanggan milik Anda sebelum menuliskannya ke bucket Anda, dan layanan penyimpanan Anda mengenkripsi objek yang disimpan sekali lagi dengan kunci bucket Anda. Setelah kunci yang dikelola pelanggan milik Anda berhenti berfungsi, Anthropic tidak dapat mendekripsi konten yang disimpan tersebut, apa pun yang terjadi pada kunci bucket Anda.
* **Transkrip dan Safety Cases:** Hanya kunci bucket Anda yang mengenkripsinya.

## Melampirkan kunci yang dikelola pelanggan

<Warning>
  Melampirkan kunci bersifat permanen. Anda tidak dapat melepas kunci atau menggantinya dengan kunci lain. Rotasi material kunci di dalam kunci yang sama didukung. Di Claude Platform, workspace tidak dapat beralih ke **Legacy ZDR**, dan Anda membuat workspace baru untuk menggunakan kunci lain.
</Warning>

<Steps>
  <Step title="Buat dan daftarkan kunci Anda">
    Ikuti panduan untuk layanan manajemen kunci Anda untuk membuat kunci dan mendaftarkannya ke Anthropic, lalu kembali ke sini untuk melampirkannya.

    * [AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms)
    * [Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms)
    * [Azure Key Vault](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault)
  </Step>

  <Step title="Lampirkan kunci Anda">
    Lampirkan kunci Anda sebelum workspace melayani lalu lintas, karena pada workspace yang sudah melayani lalu lintas, kunci dapat memerlukan waktu hingga satu hari untuk berlaku.

    Jika workspace akan menggunakan penyimpanan milik pelanggan, terlebih dahulu [hubungkan tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) ke organisasi Anda di bawah **Storage destinations**. Jika workspace menggunakan EFS, ikuti langkah-langkah di [Menyiapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console).

    Untuk melampirkan kunci Anda, ikuti langkah-langkah berikut untuk setiap workspace yang akan menggunakannya:

    1. Buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console dan pilih workspace di bagian atas.
    2. Pilih kunci Anda di bawah **Kunci enkripsi** dan simpan.

    Jika workspace menggunakan penyimpanan yang dikelola Anthropic, tidak ada lagi yang perlu dilakukan.

    Untuk menyiapkan kunci di Claude Platform on AWS, ikuti langkah-langkah di [Menyiapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws).

    Untuk menyiapkan kunci di Claude Models on Google Cloud (Anthropic managed), [buka Claude Console](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#before-you-begin) dari konsol Google Cloud. Kemudian, ikuti langkah-langkah untuk kunci Anda sendiri di [Menambahkan sumber daya cloud](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#add-cloud-resources). Anda memerlukan `roles/claude.admin`, bukan Admin organisasi. Anda tidak memerlukan bucket untuk menggunakan kunci.
  </Step>
</Steps>

## Mencabut kunci Anda

Di Claude Platform, setelah kunci Anda [berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), permintaan ke workspace mulai gagal hingga satu jam setelah Anda mencabut atau menonaktifkannya. Dalam waktu sekitar satu jam setelah menonaktifkan kunci Anda, Anthropic tidak dapat lagi mendekripsi data yang dilindungi oleh kunci Anda. Sejumlah kecil catatan [tetap berada di luar kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#limited-preservation-outside-your-key). Mencabut atau menonaktifkan kunci Anda tidak menghapus data atau membatalkan pembacaan yang sudah terjadi.

Sebelum Anda mencabut kunci Anda, baca [apa arti mencabut dan apa yang tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Untuk apa yang terjadi pada permintaan Anda dan siapa yang diberi tahu, lihat [Jika kunci Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working).

## Jika kunci Anda berhenti berfungsi

Tabel berikut menunjukkan apa yang terjadi di Claude Platform ketika workspace tidak dapat menggunakan kunci Anda, dan apa yang harus dilakukan.

| Peristiwa | Permintaan | Data Anda | Siapa yang diberi tahu | Apa yang harus dilakukan |
| ----- | ----- | ----- | ----- | ----- |
| Kunci Anda dicabut atau dinonaktifkan | Jika kunci Anda sudah berlaku, permintaan dapat tetap berhasil hingga satu jam. Setelah itu, permintaan ke workspace gagal. | Setelah kunci Anda berhenti berfungsi, Anthropic tidak dapat mendekripsi apa yang dilindungi oleh kunci Anda hingga Anda mengaktifkan kembali kunci Anda atau memulihkan akses Anthropic ke kunci tersebut. Menghapus kunci Anda tidak dapat dibatalkan. | Anthropic biasanya mengirim email kepada anggota organisasi Anda yang dapat mengelola kunci enkripsi. Di Claude Models on Google Cloud (Anthropic managed) dan Claude Platform on AWS, Anthropic justru biasanya mengirim email kepada orang yang menyelesaikan penyiapan organisasi Anda, bukan kepada anggota tersebut. | Aktifkan kembali kunci Anda, atau pulihkan akses Anthropic ke kunci tersebut. Permintaan yang gagal sementara itu tidak dicoba ulang, dan periode retensi tetap berjalan. Lihat [apa yang kembali saat Anda mengaktifkan kembali kunci](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#restore-access). |
| Layanan manajemen kunci Anda tidak dapat dijangkau | Dapat tetap berhasil hingga satu jam. Setelah itu, permintaan ke workspace gagal. Di Messages API, permintaan tersebut mengembalikan [error 503 dengan kode `cmek_key_unreachable`](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#unreachable-key), dan Anda dapat mencobanya ulang. Message Batches API mencobanya ulang untuk Anda hingga kunci Anda tersedia atau batch kedaluwarsa. | Apa yang sudah disimpan tidak berubah. Setelah kunci Anda berhenti berfungsi, Anthropic tidak dapat mendekripsi apa yang dilindungi oleh kunci Anda hingga layanan manajemen kunci Anda dapat dijangkau kembali. Catatan yang tidak dapat dienkripsi oleh Anthropic selama gangguan tidak disimpan. | Tidak ada. | Pulihkan akses ke layanan manajemen kunci Anda. |

Jika workspace juga menggunakan penyimpanan milik pelanggan, lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working).

## Merotasi atau mengganti kunci Anda

Anda dapat merotasi material kunci di dalam kunci yang sama tanpa mengubah apa pun di Claude Console.

Di Claude Platform, untuk menggunakan kunci yang berbeda, buat workspace baru dengan kunci baru dan pindahkan lalu lintas Anda ke sana, karena [melampirkan kunci bersifat permanen](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Menyiapkan Enterprise Frontier Safeguards di Claude Platform" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console">
    Untuk workspace yang menggunakan EFS, lampirkan kunci Anda, lalu periksa penyiapan Anda.
  </Card>

  <Card title="Menyiapkan penyimpanan milik pelanggan" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage">
    Simpan data keselamatan tersegel Anda di penyimpanan dalam akun cloud milik Anda sendiri.
  </Card>

  <Card title="Kunci enkripsi yang dikelola pelanggan" icon="book" href="https://platform.claude.com/docs/id/manage-claude/cmek">
    Apa yang dicakup kunci, apa yang dinonaktifkannya, dan apa arti mencabutnya.
  </Card>
</CardGroup>
