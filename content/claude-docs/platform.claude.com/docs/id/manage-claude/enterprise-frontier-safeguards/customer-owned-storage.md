---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 54494148fb6c515af5c9abf30ed55971e90e960e822cfc5baed32bb3964cea0e
---

---
title: Penyimpanan milik pelanggan
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage
description: Simpan data di sebuah bucket di akun cloud Anda sendiri.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

<Where cloud="aws" label="Claude Platform on AWS">

Dengan Enterprise Frontier Safeguards (EFS), Anda membawa penyimpanan Anda sendiri dan menyimpan data Anda sendiri, di bawah kebijakan akses dan pencatatan audit Anda sendiri. Anthropic segera menghapus prompt dan respons setelah respons terkait dihasilkan dan semuanya ditulis ke bucket Anda. Anda menyediakan penyimpanan untuk:

</Where>

<Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">

Penyimpanan milik pelanggan menyimpan data sebuah workspace di sebuah bucket di akun cloud Anda sendiri, bukan di penyimpanan yang dikelola Anthropic. Enterprise Frontier Safeguards (EFS) mewajibkannya untuk data keselamatan tersegel. Untuk transkrip dan Safety Cases, penyimpanan ini wajib di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed). Tiga kategori data dapat masuk ke bucket Anda:

</Where>

<Where cloud="claude" label="Claude Platform">

Penyimpanan milik pelanggan menyimpan data keselamatan tersegel dan transkrip sebuah workspace di sebuah bucket di akun cloud Anda sendiri, bukan di penyimpanan yang dikelola Anthropic. Enterprise Frontier Safeguards (EFS) mewajibkannya untuk data keselamatan tersegel. Untuk transkrip dan Safety Cases, penyimpanan ini opsional di Claude Platform. Tiga kategori data dapat masuk ke bucket Anda:

</Where>

* **[Data keselamatan tersegel](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored):** Prompt, respons, dan penalaran model, dienkripsi dalam format Anthropic.
* **Transkrip:** Salinan prompt dan respons yang dapat dibaca, untuk dibaca oleh tim Anda.
* **Safety Correspondence:** Safety Cases, Safety Notices, dan Safety Case Responses Anda. Tidak pernah berisi prompt dan respons. Tim Anda meninjau Safety Cases seperti yang dijelaskan di [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases).

<Where bucket="s3" label="Amazon S3">Anda membuat bucket Amazon S3 tersebut, sebuah kunci enkripsi, dan peran-peran di akun cloud Anda sendiri. Kunci tersebut mengenkripsi bucket, dan peran-peran tersebut memberi Anthropic akses ke bucket itu.</Where> <Where bucket="gcs" label="Google Cloud Storage">Anda membuat bucket Google Cloud Storage tersebut, sebuah kunci enkripsi, peran kustom, dan pemberian izin (grant) kepada akun-akun Anthropic di akun cloud Anda sendiri. Kunci tersebut mengenkripsi bucket, dan pemberian izin tersebut memberi Anthropic akses ke bucket itu.</Where> <Where bucket="s3" label="Amazon S3">Log akun Anda mencatat setiap kali Anthropic mengambil alih salah satu peran Anda (lihat [Panggilan Anthropic di AWS CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#cloudtrail)).</Where> Anda dapat menghapus akses Anthropic. Untuk data keselamatan tersegel, permintaan di workspace yang terdampak kemudian dapat ditolak hingga akses dipulihkan. <Where bucket="s3" label="Amazon S3">Untuk menghapusnya, ikuti langkah-langkah di [Berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#stop-using-your-bucket) secara berurutan.</Where> <Where bucket="gcs" label="Google Cloud Storage">Untuk menghapusnya, ikuti langkah-langkah di [Berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-stop-using-your-bucket) secara berurutan.</Where>

Anthropic tidak mengenakan biaya untuk penyimpanan milik pelanggan, tetapi penyedia cloud Anda menagih Anda untuk penyimpanan, pembacaan, penulisan, dan operasi kunci, ditambah transfer jaringan apa pun yang berlaku.

<CardGroup cols={3}>
  <Where cloud="aws" label="Claude Platform on AWS">

  <Card title="Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws">
    Aktifkan Enterprise Frontier Safeguards untuk sebuah workspace dan pilih penyimpanan serta kuncinya.
  </Card>

  </Where>

  <Where cloud="claude" label="Claude Platform">

  <Where bucket="s3" label="Amazon S3">

  <Card title="Menyiapkan penyimpanan milik pelanggan" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage">
    Buat bucket Anda, kuncinya, dan peran-perannya, lalu hubungkan semuanya di Claude Console.
  </Card>

  </Where>

  <Where bucket="gcs" label="Google Cloud Storage">

  <Card title="Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#google-cloud-storage">
    Buat bucket Anda, kuncinya, dan peran-perannya, lalu hubungkan semuanya di Claude Console.
  </Card>

  </Where>

  </Where>

  <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">

  <Card title="Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed">
    Aktifkan Enterprise Frontier Safeguards untuk sebuah workspace dan pilih penyimpanan serta kuncinya.
  </Card>

  </Where>

  <Where bucket="s3" label="Amazon S3">

  <Card title="Mengelola penyimpanan milik pelanggan" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage">
    Periksa status bucket Anda, perbaiki bucket yang berhenti berfungsi, dan ubah atau berhenti menggunakannya.
  </Card>

  </Where>

  <Where bucket="gcs" label="Google Cloud Storage">

  <Card title="Jika bucket Anda berhenti berfungsi" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-if-your-bucket-stops-working">
    Perbaiki bucket yang berhenti berfungsi, atau berhenti menggunakannya.
  </Card>

  </Where>

  <Where bucket="s3" label="Amazon S3">

  <Where cloud="claude" label="Claude Platform">

  <Card title="Menyiapkan penyimpanan milik pelanggan dengan Admin API" icon="code" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?method=api">
    Buat skrip untuk bagian Claude Console dengan Admin API, tempat External Storage adalah catatan Anthropic tentang bucket Anda.
  </Card>

  </Where>

  </Where>
</CardGroup>

## Apa yang disimpan, dan di mana

Ketiga kategori data berbeda dalam hal siapa yang dapat membacanya dan apa yang terjadi jika Anthropic tidak dapat menulis ke bucket Anda. <Where cloud="claude" label="Claude Platform"><Where bucket="s3" label="Amazon S3">[Transkrip dan Safety Cases di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket) menjelaskan bucket mana yang dapat menerima transkrip dan Safety Cases.</Where> <Where bucket="gcs" label="Google Cloud Storage">[Gunakan bucket Cloud Storage Anda di ruang kerja](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace) menjelaskan cara memilih bucket Anda untuk transkrip dan Safety Cases.</Where></Where> <Where cloud="aws" label="Claude Platform on AWS">EFS juga mewajibkan bucket Anda untuk transkrip dan Safety Cases.</Where> <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">EFS juga mewajibkan bucket Anda untuk transkrip dan Safety Cases.</Where>

| Kategori data | Siapa yang dapat membacanya | Jika Anthropic tidak dapat menulis ke bucket Anda |
| ----- | ----- | ----- |
| Data keselamatan tersegel: prompt, respons, dan penalaran model, dienkripsi dalam format Anthropic. | Tim Anda tidak dapat membacanya, bahkan di penyimpanan yang Anda miliki. Data ini ditujukan untuk pemantauan keselamatan otomatis. Untuk detailnya, lihat [Kapan pemantauan keselamatan otomatis mengakses data Anda?](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#who-at-anthropic-can-access-your-data) | <Where bucket="s3" label="Amazon S3">Permintaan ke workspace tetap berjalan selama [masa tenggang hingga 24 jam](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working). Setelah itu, Anthropic mungkin menolaknya. Anthropic mencoba ulang penulisan selama waktu yang terbatas dan tidak mengirim data tersebut ke penyimpanan yang dikelola Anthropic sebagai gantinya. Beri tahu tim akun Anthropic Anda segera setelah Anda menyadari adanya kegagalan, karena Anthropic menghapus data yang belum sampai ke bucket Anda. Di Claude Platform, Anthropic menghapus data tersebut sekitar 72 jam setelah permintaan. Di platform lain mana pun, hal itu dapat terjadi paling cepat sekitar satu hari setelah permintaan.</Where> <Where bucket="gcs" label="Google Cloud Storage">Permintaan ke workspace tetap berjalan selama masa tenggang hingga 24 jam. Setelah itu, Anthropic mungkin menolaknya. Anthropic mencoba ulang penulisan yang gagal. Pulihkan bucket Anda dalam waktu sekitar 46 jam setelah permintaan dan pertahankan setiap workspace di bucket tersebut, atau Anda dapat kehilangan data tersebut. Anthropic berhenti mencoba ulang paling lambat sekitar 72 jam setelah permintaan, lalu menghapus data tersebut. Tidak ada yang dapat memulihkan data tersebut, dan data itu tidak dikirim ke penyimpanan yang dikelola Anthropic. Beri tahu tim akun Anthropic Anda segera setelah Anda menyadari adanya kegagalan. Lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-if-your-bucket-stops-working).</Where> |
| Transkrip prompt dan respons Anda. Transkrip mungkin mencakup permintaan yang tidak pernah menghasilkan Safety Case, jadi rencanakan siapa yang dapat membaca bucket Anda. | Tim Anda. Anthropic menulisnya dalam bentuk yang dapat dibaca oleh tim Anda. | <Where cloud="claude aws" label="Claude Platform or Claude Platform on AWS">Kegagalan penyimpanan ini saja tidak memblokir permintaan.</Where> Anda tidak menerima transkrip atau Safety Cases di sana selama Anthropic tidak dapat menulis ke penyimpanan tersebut. |
| Safety Correspondence: Safety Cases, Safety Notices, dan Safety Case Responses Anda. | Tim Anda, dan Anthropic (lihat paragraf setelah tabel ini). | Sama seperti untuk transkrip. |

Safety Cases, Safety Notices, dan Safety Case Responses Anda (secara bersama-sama, Safety Correspondence) tidak pernah berisi prompt atau respons Anda. Sebuah Safety Case berisi pengenal dan detail, seperti status, stempel waktu, kategori kebijakan, tindakan penegakan apa pun yang diambil, dan referensi ke transkrip terkait. <Where bucket="s3" label="Amazon S3">Anthropic dapat membaca Safety Cases dan Safety Case Responses Anda di bucket Anda melalui [peran peninjauan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-roles), tetapi identitasnya tidak dapat membaca transkrip Anda atau menulis maupun mengubah Safety Case Responses Anda.</Where> <Where bucket="gcs" label="Google Cloud Storage">Anthropic dapat membaca Safety Cases dan Safety Case Responses Anda di bucket Anda, tetapi identitasnya tidak dapat membaca transkrip Anda atau menulis maupun mengubah Safety Case Responses Anda.</Where> Ke mana pun Safety Cases Anda dikirim, Anthropic juga menyimpan catatan Safety Correspondence, yang dapat dibaca oleh personel Anthropic yang berwenang. Catatan tersebut tidak berisi prompt atau respons.

### Dua pengaturan penyimpanan

Sebuah workspace yang menggunakan kartu **Enterprise Frontier Safeguards** memiliki dua pengaturan penyimpanan:

* **Sealed Safety Data storage** menentukan ke mana Anthropic mengirim data keselamatan tersegel. Pengaturan ini wajib, dan hanya menawarkan penyimpanan milik Anda sendiri.
* **Safety Case and Transcript storage** menentukan ke mana Anthropic mengirim transkrip dan Safety Cases. <Where cloud="claude" label="Claude Platform">Pengaturan ini opsional. Tanpa bucket di bawahnya, tim Anda hanya mendapatkan Safety Cases jika organisasi Anda memiliki [akses ke Safety Cases API](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#get-access). **Not copied to your storage** berarti Anthropic tidak menyalinnya ke penyimpanan Anda. <Where bucket="s3" label="Amazon S3">Jika bucket di bawah **Sealed Safety Data storage** [dapat menerimanya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket), Anda juga dapat memilihnya, saat pertama kali menyimpan atau nanti.</Where> <Where bucket="gcs" label="Google Cloud Storage">Jika halaman Data retention menampilkan pengaturan tersebut, Anda dapat memilih bucket yang sama saat pertama kali menyimpan atau nanti. Lihat [Gunakan bucket Cloud Storage Anda di ruang kerja](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace).</Where></Where> <Where cloud="aws" label="Claude Platform on AWS">EFS mewajibkannya. Lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws). **Not copied to your storage** berarti Anthropic tidak menyalinnya ke penyimpanan Anda.</Where> <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">EFS mewajibkannya. Lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed). **Not copied to your storage** berarti Anthropic tidak menyalinnya ke penyimpanan Anda.</Where>

Transkrip dan Safety Cases dikirim ke bucket yang sama, dan Anda tidak dapat memilih salah satunya tanpa yang lain.

### Berapa lama data keselamatan tersegel disimpan

<Where cloud="claude" label="Claude Platform">

Data keselamatan tersegel tetap berada di bucket Anda selama jumlah hari yang terbatas setelah Anda mengirim permintaan. Waktu tersebut adalah periode retensi, dan lamanya hingga 28 hari.

</Where>

<Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">

Data keselamatan tersegel tetap berada di bucket Anda selama jumlah hari yang terbatas setelah Anda mengirim permintaan. Waktu tersebut adalah periode retensi, dan lamanya hingga 28 hari.

</Where>

<Where cloud="aws" label="Claude Platform on AWS">

Periode retensi untuk data keselamatan tersegel adalah hingga 28 hari setelah Anda mengirim permintaan.

</Where>

<Where bucket="gcs" label="Google Cloud Storage">

Aturan siklus hidup milik bucket Anda sendiri menghapus setiap objek data keselamatan tersegel setelah berumur 28 hari dan menghapusnya secara permanen paling cepat satu hari kemudian.

</Where>

<Where bucket="s3" label="Amazon S3">

<Where cloud="claude" label="Claude Platform">

Anthropic menghapus sebuah objek dari bucket Anda setelah semua isinya melewati periode retensi. Anda tidak perlu menyiapkan pembersihan apa pun. [Versi lama dan beberapa objek disimpan lebih lama](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-removes-data).

</Where>

</Where>
