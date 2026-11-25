---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 3a8ac9b06478b15ab6ddb4b8c6086eed80a8790bb406c5386da409ec45cb14af
---

---
title: FAQ Enterprise Frontier Safeguards
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq
description: Jawaban singkat atas pertanyaan umum tentang Enterprise Frontier Safeguards, dengan tautan ke detailnya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Untuk menyiapkan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS), lihat [Panduan penyiapan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console).

## Data dan retensi

<AccordionGroup>
  <Accordion title="Apa itu Enterprise Frontier Safeguards (EFS)?">
    [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS) adalah “Zero Data Retention” (retensi data nol), atau ZDR, bagi organisasi yang memenuhi syarat yang menggunakan [model Claude yang paling mumpuni](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Anthropic tidak menyimpan prompt dan respons Anda. Data keselamatan tersegel ditulis ke penyimpanan milik Anda. EFS mencakup [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) sekaligus [peninjauan Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) oleh orang-orang di organisasi Anda. Workspace yang menggunakan [penyimpanan yang dikelola Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) tidak termasuk EFS, karena Anthropic menyimpan salinan terenkripsi dari prompt dan respons workspace tersebut.
  </Accordion>

  <Accordion title="Bagaimana cara saya mendapatkan akses ke EFS?">
    1. Jika halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console sudah menampilkan **Enterprise Frontier Safeguards**, lanjutkan ke langkah 2. Jika tidak, hubungi tim akun Anthropic Anda untuk meminta akses. Jika Anda tidak memiliki tim akun, lengkapi [formulir permintaan Enterprise Frontier Safeguards](https://claude.com/form/enterprise-frontier-safeguards).
    2. Setelah Anthropic mengonfirmasi bahwa organisasi Anda memenuhi syarat, seorang Admin organisasi menerima ketentuan dari halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console.
    3. Untuk menyiapkan EFS, ikuti [panduan penyiapan EFS untuk platform Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console).

    Di Amazon Bedrock, Anda mendapatkan akses melalui AWS. Lihat [Enterprise Frontier Safeguards di Amazon Bedrock](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-amazon-bedrock).
  </Accordion>

  <Accordion title="Apa perbedaan antara Enterprise Data Controls dan EFS?">
    Perbedaan utamanya adalah tempat data keselamatan tersegel Anda disimpan. Dengan EFS, data tersebut ditulis ke penyimpanan milik Anda, sehingga EFS merupakan Zero Data Retention (ZDR). Dengan [Enterprise Data Controls](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview#enterprise-data-controls), sebuah workspace tetap menggunakan penyimpanan yang dikelola Anthropic. Di Claude Platform, Anda tetap dapat [menggunakan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys) dan [menonaktifkan Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) untuk kontrol tambahan atas data Anda.
  </Accordion>

  <Accordion title="Apakah EFS hanya berlaku untuk model yang memerlukan retensi data?">
    Tidak. Di Claude Platform, EFS berlaku untuk setiap permintaan ke setiap model dalam workspace tempat Anda mengaktifkannya. Itu termasuk model yang tidak memerlukan retensi data. Satu workspace tidak dapat menggunakan EFS untuk sebagian model dan tidak untuk model lainnya. Untuk menggunakan EFS hanya untuk sebagian lalu lintas, [gunakan workspace terpisah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview#workspace-scope) dan pilih workspace berdasarkan kunci API atau ID workspace.
  </Accordion>

  <Accordion title="Apakah saya harus mengaktifkan EFS untuk seluruh organisasi saya?">
    Tidak. Di Claude Platform, mendapatkan akses ke EFS tidak mengaktifkan EFS untuk workspace mana pun. Memilih EFS untuk satu workspace tidak mengubah workspace Anda yang lain. Access Transparency merupakan pengecualian: setelah diaktifkan, fitur ini aktif untuk seluruh organisasi Anda, dan Anda tidak dapat menonaktifkannya. Lihat [Periksa Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency). Jika organisasi Anda memiliki perjanjian Legacy ZDR, workspace yang menggunakan **Legacy ZDR** tetap di sana. Untuk menggunakan EFS, buat workspace baru dan gunakan workspace tersebut sebagai pengganti workspace Legacy ZDR Anda.

    Permintaan dari workspace yang menggunakan **Legacy ZDR** ke model yang [memerlukan retensi data 30 hari](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) akan gagal dengan error 400, kecuali Anthropic telah mengizinkan organisasi Anda untuk menggunakannya di bawah Legacy ZDR. Kirim permintaan tersebut dari workspace yang menggunakan EFS atau penyimpanan yang dikelola Anthropic sebagai gantinya.
  </Accordion>

  <Accordion title="Data apa saja yang dicakup oleh EFS?">
    EFS mencakup permintaan ke Messages API di workspace yang dikonfigurasi untuk EFS, apa pun modelnya. EFS tidak mencakup data yang disimpan oleh fitur Claude Platform untuk penggunaannya sendiri, bahkan dalam permintaan Messages API, seperti container eksekusi kode, unggahan Files API, hasil Batch API, dan sesi Claude Managed Agents. Lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility) untuk setiap fitur.

    EFS berlaku sejak konfigurasi mulai berlaku. Data yang ditulis sebelumnya tetap berada di tempat data tersebut ditulis hingga kedaluwarsa.
  </Accordion>

  <Accordion title="Apakah EFS mendukung Batch API?">
    Tidak, karena [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) tidak menyimpan transkrip untuk ditinjau oleh tim Anda. Sebagai gantinya, kirim setiap permintaan secara terpisah melalui Messages API, atau kirim batch dari workspace yang tidak menggunakan EFS dan yang Anthropic Human Review-nya aktif.
  </Accordion>

  <Accordion title="Apakah EFS mendukung layanan Claude Managed Agents dari Anthropic?">
    Tidak. Setiap workspace yang menggunakan EFS memiliki [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) nonaktif. Layanan Claude Managed Agents dari Anthropic tidak menjalankan sesi atau [dreams](https://platform.claude.com/docs/id/managed-agents/dreams) di workspace yang Anthropic Human Review-nya nonaktif. Sesi yang sudah ada di workspace seperti itu akan berhenti menerima pesan baru. Untuk menjalankan sesi atau dreams, buat keduanya di workspace yang Anthropic Human Review-nya aktif.
  </Accordion>

  <Accordion title="Apakah EFS berlaku untuk lalu lintas dari sebelum saya menyiapkannya?">
    Tidak. EFS berlaku begitu penyiapan Anda mulai berlaku. Lihat [Berapa lama perubahan berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#how-long-changes-take).
  </Accordion>

  <Accordion title="Apakah Anthropic melatih model dengan data saya?">
    Anthropic tidak melatih model Claude dengan data perusahaan tanpa izin eksplisit.
  </Accordion>
</AccordionGroup>

## Akses dan peninjauan

<AccordionGroup>
  <Accordion title="Siapa di Anthropic yang meninjau data saya?">
    Pemantauan keselamatan otomatis memeriksa lalu lintas Anda, dan tidak ada orang yang melihat konten Anda pada tahap tersebut. Dengan EFS, Anthropic Human Review selalu nonaktif. Di penyimpanan yang dikelola Anthropic, dengan Anthropic Human Review aktif, tim kecil yang terspesialisasi di Anthropic dapat meninjau temuan pemantauan keselamatan otomatis. Lihat [kapan pemantauan keselamatan otomatis mengakses data Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#who-at-anthropic-can-access-your-data).
  </Accordion>

  <Accordion title="Bagaimana saya tahu jika personel Anthropic mengakses data saya?">
    Access Transparency mencatat akses ke data Anda oleh personel Anthropic, untuk semua yang [dicakup oleh Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers). Di Claude Platform, Access Transparency tidak memiliki catatan untuk data di penyimpanan milik pelanggan. Lihat [Periksa Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency).
  </Accordion>

  <Accordion title="Dapatkah saya menambahkan classifier saya sendiri?">
    Tidak. Pemantauan keselamatan otomatis milik Anthropic yang memeriksa lalu lintas Anda.
  </Accordion>
</AccordionGroup>

## Penyimpanan dan kunci

<AccordionGroup>
  <Accordion title="Penyedia cloud mana saja yang didukung oleh penyimpanan milik pelanggan?">
    Penyedia bucket Anda bergantung pada tempat Anda menggunakan Claude:

    * **Claude Platform:** Amazon S3 atau Google Cloud Storage.
    * **[Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws):** Amazon S3.
    * **[Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed):** Google Cloud Storage.

    Lihat [Menyiapkan penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) atau [Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#google-cloud-storage).
  </Accordion>

  <Accordion title="Dapatkah saya mengubah isi bucket saya?">
    Hanya untuk menulis [file tanggapan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file) tim Anda, jika bucket Anda menerima [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary). Jangan menulis apa pun selain itu ke bucket Anda, dan biarkan isi lainnya apa adanya. Untuk bucket Amazon S3, lihat [Berikan tim Anda akses ke bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#let-your-team-read-the-bucket) dan [Apa yang menghapus data dari bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-removes-data).
  </Accordion>

  <Accordion title="Dapatkah beberapa organisasi Anthropic berbagi satu akun AWS?">
    Ya. Lihat [Buat dan hubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles).

    Setiap organisasi memerlukan bucket sendiri, dengan [kunci KMS sendiri](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-you-use-your-own-bucket), dan menggunakan sebuah bucket akan [mengikatnya ke satu organisasi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#before-you-begin).
  </Accordion>

  <Accordion title="Dapatkah saya menghubungkan lebih dari satu bucket di akun AWS yang sama?">
    Ya. Setiap bucket memerlukan stack CloudFormation sendiri atau folder Terraform sendiri. Lihat [Buat dan hubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles).
  </Accordion>

  <Accordion title="Dapatkah setiap workspace menggunakan bucket-nya sendiri?">
    Di Claude Platform dan Claude Platform on AWS, ya. Pilih bucket setiap workspace di Claude Console. Untuk Google Cloud Storage, bicarakan terlebih dahulu dengan tim akun Anthropic Anda, karena [Anthropic membatasi jumlah bucket dan workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace).
  </Accordion>

  <Accordion title="Dapatkah saya menyimpan transkrip dan Safety Cases di bucket yang berbeda dari data keselamatan tersegel saya?">
    Rencanakan satu bucket untuk keduanya. Jika sebuah workspace menggunakan [**Sealed Safety Data storage** dan **Safety Case and Transcript storage**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#the-two-storage-settings) sekaligus, pilih bucket yang sama untuk keduanya. Jika Anda memilih bucket yang berbeda, bucket tersebut mungkin tidak menerima transkrip dan Safety Cases, meskipun penyimpanan pengaturan berhasil. Lihat [Transkrip dan Safety Cases di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket).
  </Accordion>

  <Accordion title="Apa yang terjadi pada data saya jika saya berhenti menggunakan penyimpanan milik pelanggan?">
    EFS memerlukan penyimpanan milik pelanggan, sehingga workspace yang berhenti menggunakannya akan keluar dari EFS. Untuk mengetahui apa yang terjadi pada data Anda dan urutan langkahnya, lihat [Ubah atau berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket).

    Setelah Anda [berhenti menggunakan sebuah bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket), [hapus tujuan penyimpanannya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#delete-a-storage-destination) jika memungkinkan. Jika tidak memungkinkan, bicarakan dengan tim akun Anthropic Anda sebelum Anda menghapus akses Anthropic ke bucket tersebut. Hal ini berlaku bahkan setelah semua isinya melewati periode retensi.
  </Accordion>

  <Accordion title="Apa yang berubah saat saya melampirkan kunci yang dikelola pelanggan?">
    [Melampirkan kunci](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) menonaktifkan beberapa fitur dan bersifat permanen. Pertama, periksa [apa yang dinonaktifkan](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed) dan baca [Sebelum Anda melampirkan kunci](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#before-you-attach-a-key).
  </Accordion>
</AccordionGroup>

## EFS di Claude Platform on AWS

Untuk menyiapkan EFS di Claude Platform on AWS, ikuti [Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws). Kunci enkripsi yang dikelola pelanggan tersedia di sana dengan AWS KMS.

## EFS di Claude Models on Google Cloud (Anthropic managed)

Untuk menyiapkan EFS di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), ikuti [Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed). Bucket Anda berada di Google Cloud Storage, dan kunci enkripsi yang dikelola pelanggan Anda berada di Google Cloud KMS. Untuk kuncinya, lihat [Menyiapkan CMEK dengan Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms).

## Jika kunci atau bucket Anda berhenti berfungsi

Di Claude Platform, jika kunci Anda dicabut atau dinonaktifkan setelah [kunci tersebut berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), permintaan dapat tetap berhasil hingga satu jam. Setelah itu, permintaan ke workspace tersebut gagal. Untuk memulihkannya, lihat [Jika kunci Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working).

Jika Anthropic tidak dapat menulis ke bucket Anda, lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working). Untuk bucket Google Cloud Storage, lihat [Jika bucket Cloud Storage Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-if-your-bucket-stops-working).

## Berapa lama perubahan berlaku

Rencanakan pemeriksaan Anda dan peralihan Anda ke produksi berdasarkan waktu-waktu berikut:

| Perubahan | Berapa lama waktunya |
| ----- | ----- |
| Workspace baru, atau workspace yang menggunakan penyimpanan yang dikelola Anthropic, [mulai menggunakan penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take) | Biasanya dalam 10 menit, tetapi dapat memakan waktu lebih lama. Setelah objek baru pertama tiba di bucket Anda, tunggu 10 menit lagi. |
| [Access Transparency mulai mencatat](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) setelah diaktifkan | Dalam 2 jam |
| Event Access Transparency tiba di Activity Feed Anda | Dalam 2 hari kerja setelah akses yang dicatatnya |
| [Kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) berlaku pada workspace yang sudah melayani lalu lintas | Hingga satu hari |
| Perubahan pada [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) diterapkan | Hingga 2 jam |

## Glosarium

| Istilah | Arti |
| ----- | ----- |
| Claude Platform | Claude API, yang disiapkan di Claude Console. |
| Pemantauan keselamatan otomatis | Sistem otomatis yang mencari pola penyalahgunaan di banyak permintaan. Dengan EFS, sistem tersebut menganalisis data yang disimpan di akun cloud Anda, dan tim Anda meninjau setiap temuan. |
| Data keselamatan tersegel | Prompt, respons, dan penalaran model, yang dienkripsi dalam format Anthropic. Tim Anda tidak dapat membacanya, bahkan di bucket Anda sendiri. Lihat [Apa yang disimpan, dan di mana](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored). |
| Transkrip | Salinan yang dapat dibaca dari sebuah prompt dan respons, untuk dibaca oleh tim Anda. |
| Safety Correspondence | Safety Cases, Safety Notices, dan Safety Case Responses Anda. Tidak pernah berisi prompt dan respons. |
| Bucket data keselamatan (Safety data bucket) | Bucket di akun cloud Anda sendiri yang digunakan sebuah workspace untuk data keselamatan tersegel. Anda memilihnya di bawah **Sealed Safety Data storage** pada halaman [Retensi data](https://platform.claude.com/settings/privacy) workspace tersebut. EFS memerlukannya. |
| Bucket kasus (Case bucket) | Bucket tempat Anthropic mengirimkan transkrip dan Safety Cases sebuah workspace, dalam bentuk yang dapat dibaca oleh tim Anda. Anda memilihnya di bawah [**Safety Case and Transcript storage**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#the-two-storage-settings). EFS memerlukannya di Claude Models on Google Cloud (Anthropic managed) dan Claude Platform on AWS. Satu bucket dapat berfungsi sebagai bucket data keselamatan sekaligus bucket kasus, jadi rencanakan untuk menggunakan satu bucket untuk keduanya. |
| Legacy ZDR | [ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) dengan pengamanan real-time tetapi tanpa pemantauan keselamatan otomatis. Anthropic tidak menyimpan prompt atau respons setelah respons API dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan. |
| Penyimpanan yang dikelola Anthropic | Penyimpanan yang dijalankan oleh Anthropic, digunakan oleh workspace pada kartu **Anthropic managed**. |
| Anthropic managed | Kartu di Claude Console untuk workspace yang menggunakan penyimpanan yang dikelola Anthropic. Kartu ini merupakan pengaturan default untuk model Claude yang [memerlukan retensi data 30 hari](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). |
| Enterprise Data Controls | Serangkaian fitur untuk workspace yang memenuhi syarat EFS yang menggunakan penyimpanan yang dikelola Anthropic alih-alih EFS. Anda dapat menggunakan kunci yang dikelola pelanggan (CMEK) dan, di Claude Platform, menonaktifkan Anthropic Human Review. Anthropic tetap menyimpan data keselamatan tersegel Anda, sehingga penyiapan ini bukan EFS dan bukan ZDR. Lihat [Enterprise Data Controls](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview#enterprise-data-controls). |
| Penyimpanan milik pelanggan | Menyimpan data keselamatan tersegel Anda di bucket dalam akun cloud Anda sendiri. Lihat [Menyiapkan penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) atau [Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#google-cloud-storage). |
| Kunci yang dikelola pelanggan | Kunci enkripsi di layanan manajemen kunci Anda sendiri yang mengenkripsi data Anda. Disebut juga CMEK. Lihat [Menggunakan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys). |
| Human Review | Disebut juga Anthropic Human Review. Di Claude Platform dengan penyimpanan yang dikelola Anthropic, jika Claude Console menampilkan pertanyaan **Who reviews flagged cases?**, **Anthropic** mengaktifkannya dan **My organization** menonaktifkannya. Saat aktif, tim kecil yang terspesialisasi di Anthropic dapat meninjau temuan pemantauan keselamatan otomatis. Dengan EFS, fitur ini selalu nonaktif. Lihat [di mana Anda dapat menonaktifkan Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review). |
| Access Transparency | Catatan, melalui Compliance API, tentang akses ke data Anda oleh personel Anthropic, untuk semua yang [dicakup oleh Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers). |
| Safety Case | Catatan yang dapat dibuka oleh Anthropic saat pemantauan keselamatan otomatis menemukan potensi pelanggaran Kebijakan Penggunaan Anthropic di workspace tanpa Anthropic Human Review. Catatan ini mencantumkan transkrip terkait berdasarkan pengidentifikasinya. [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) menjelaskan workspace mana yang menerimanya. |
| Tujuan penyimpanan (Storage destination) | Bucket yang Anda hubungkan di bawah **Storage destinations** pada halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console. Anda memilih salah satunya untuk sebuah workspace di bawah **Sealed Safety Data storage** atau **Safety Case and Transcript storage**. |
| Kunci yang dikelola Anthropic | Kunci yang digunakan Anthropic untuk mengenkripsi data Anda saat Anda tidak melampirkan kunci Anda sendiri. |

## Referensi

Untuk detail API, lihat [Kunci yang dikelola pelanggan di Admin API](https://platform.claude.com/docs/id/api/organization/external_keys), [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), dan [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency).
