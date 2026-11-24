---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: b9f68462d889ecf6cf0c3f86257ef14b2c8da26736a785134293140f003a0974
---

---
title: Menyiapkan Enterprise Frontier Safeguards di Claude Platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console
description: Aktifkan Enterprise Frontier Safeguards untuk workspace Claude Platform lalu pilih penyimpanan dan kuncinya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Anda menyiapkan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS) di Claude Console. EFS berlaku untuk setiap permintaan ke setiap model dalam [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) tempat Anda mengaktifkannya. Untuk menentukan workspace mana yang sebaiknya menggunakannya, lihat [Rencanakan penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#plan-your-setup).

Penyiapan terdiri dari lima bagian:

1. Dapatkan akses.
2. Tambahkan sumber daya cloud: bucket penyimpanan dan kunci enkripsi Anda.
3. Aktifkan EFS untuk workspace.
4. Secara opsional, tetapkan kebijakan untuk workspace baru.
5. Periksa penyiapan Anda.

## Rencanakan penyiapan Anda

Rencanakan penyiapan Anda terlebih dahulu, karena Anda tidak dapat membatalkan beberapa pilihan.

Pertama, tentukan [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) mana yang menggunakan Enterprise Frontier Safeguards. Di Claude Platform, EFS mencakup [setiap permintaan ke setiap model dalam sebuah workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview#workspace-scope). Untuk menggunakan EFS hanya untuk sebagian lalu lintas, gunakan workspace terpisah. Workspace default tidak dapat menggunakan EFS.

Jika organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR), gunakan workspace baru untuk EFS, dan pilih kartu **Enterprise Frontier Safeguards** saat Anda membuatnya. Di Claude Console, Anda tidak dapat memilih kartu tersebut untuk workspace yang sudah ada pada **Legacy ZDR**.

Kemudian, periksa langkah mana yang dapat Anda batalkan dan apa lagi yang diubah oleh setiap langkah. Hanya [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys) yang bersifat opsional.

| Langkah | Dapatkah Anda membatalkannya? | Apa lagi yang diubahnya |
| ----- | ----- | ----- |
| Mendapatkan akses untuk sebuah organisasi | Tidak dapat Anda lakukan sendiri. Anda tidak dapat menonaktifkan [Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) setelah aktif. Untuk menghapus akses organisasi Anda, hubungi tim akun Anthropic Anda. | Mengaktifkan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) untuk organisasi Anda (lihat [Terima ketentuan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access)). Di Claude Platform, [Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) juga menjadi aktif setelah Anda mengonfigurasi workspace Anda. Mendapatkan akses tidak mengaktifkan EFS untuk workspace mana pun. |
| [Melampirkan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) | Tidak. Ini permanen. | Menonaktifkan beberapa fitur. Lihat [apa yang berubah dengan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed). |
| Menggunakan [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) | Sebagian. Anda dapat [mengganti atau berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket), tetapi berhenti menggunakannya akan mengeluarkan workspace dari EFS. | Memerlukan [Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) oleh Anthropic dalam keadaan nonaktif, sehingga orang-orang di organisasi Anda harus meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#where-cases-arrive). Rencanakan untuk menggunakan bucket tersebut dengan [hanya satu organisasi Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#before-you-begin). |

Terakhir, jawab pertanyaan-pertanyaan berikut:

<AccordionGroup>
  <Accordion title="Di mana seharusnya bucket saya berada, dan berapa biayanya?">
    Pilih akun cloud dan region untuk bucket Anda sebelum Anda memulai:

    * **Amazon S3:** Lihat [Buat dan hubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles) serta [region AWS yang didukung](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket). Anthropic merekomendasikan `us-east-2`.
    * **Google Cloud Storage:** Lihat [apa yang diperlukan oleh bucket dan proyeknya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-before-you-begin) serta [region yang didukung](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#supported-regions).

    Jika organisasi AWS Anda memblokir akun luar dengan kebijakan kontrol sumber daya (RCP), mintalah sejak awal [pengecualian untuk akun AWS Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic).

    Anthropic tidak mengenakan biaya untuk EFS, tetapi penyedia cloud Anda akan menagih Anda untuk penyimpanan, pembacaan, penulisan, dan operasi kunci, ditambah transfer jaringan yang berlaku. Anthropic membaca dan menulis bucket Anda dari region milik Anthropic sendiri, yang dapat memengaruhi biaya transfer jaringan Anda.
  </Accordion>

  <Accordion title="Siapa di tim saya yang perlu dilibatkan?">
    Untuk menyiapkan EFS dan meninjau Safety Cases setelahnya, Anda memerlukan orang-orang berikut:

    | Siapa | Apa yang mereka lakukan |
    | ----- | ----- |
    | Admin cloud | Menjalankan file penyiapan dari Claude Console yang membuat bucket dan kunci serta memberikan akses kepada Anthropic, untuk [Amazon S3](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles) atau [Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket). |
    | Admin organisasi | Di Claude Console, menghubungkan bucket, mengaktifkan EFS untuk setiap workspace, dan melampirkan kunci apa pun. |
    | Peninjau Anda | [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). |
  </Accordion>
</AccordionGroup>

## Sebelum Anda memulai

Untuk menyiapkan Enterprise Frontier Safeguards, Anda memerlukan hal-hal berikut:

* Peran Admin organisasi di Claude Console.

## 1. Dapatkan akses

Untuk mendapatkan akses di Claude Platform, seorang Admin organisasi menerima ketentuan untuk organisasi Anda. Menerima ketentuan juga memungkinkan Admin organisasi untuk menonaktifkan Anthropic Human Review. Jika tim akun Anthropic Anda telah memberikan akses kepada organisasi Anda, lewati bagian ini.

<Warning>
  Menerima ketentuan akan mengaktifkan Compliance API untuk organisasi Anda, dan untuk organisasi lain mana pun yang memenuhi syarat yang terhubung ke profil [Verification Portal](https://portal.anthropic.com) Anda.
</Warning>

### Apa yang berubah saat Anda mendapatkan akses

Hanya organisasi yang memenuhi syarat yang dapat memperoleh Enterprise Frontier Safeguards. Untuk meminta akses, hubungi tim akun Anthropic Anda. Jika Anda tidak memiliki tim akun, lengkapi [formulir permintaan Enterprise Frontier Safeguards](https://claude.com/form/enterprise-frontier-safeguards). EFS saat ini hanya tersedia untuk penggunaan internal organisasi Anda. Jika organisasi Anda mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness), organisasi tersebut tidak dapat memperoleh EFS. Anda tidak dapat menggabungkan EFS dengan beberapa program akses Anthropic, jadi beri tahu tim akun Anthropic Anda program mana yang digunakan oleh organisasi-organisasi Anda.

Menerima ketentuan mengubah lebih dari sekadar workspace yang Anda rencanakan untuk digunakan. Bacalah perubahan utama berikut sebelum Anda menerima:

<AccordionGroup>
  <Accordion title="Anda tidak dapat menonaktifkan Access Transparency setelah aktif">
    [Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) mencatat akses personel Anthropic ke [data yang dicakupnya](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers). Kapan fitur ini menjadi aktif bergantung pada tempat Anda menggunakan Claude:

    * Di Claude Platform, fitur ini menjadi aktif saat pertama kali Anda mulai menghubungkan bucket, melampirkan kunci yang dikelola pelanggan, atau menonaktifkan Anthropic Human Review. Jika sebuah workspace sudah memiliki kunci, bucket, atau Anthropic Human Review dalam keadaan nonaktif, Access Transparency menjadi aktif saat Anda mendapatkan akses.
    * Di Claude Models on Google Cloud (Anthropic managed) atau Claude Platform on AWS, fitur ini menjadi aktif saat Anda mendapatkan akses.

    Setelah aktif, fitur ini aktif untuk setiap workspace di organisasi tersebut. Jika organisasi Claude Console lain di bawah [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) yang sama memiliki Access Transparency, saat ini atau nanti, Anda juga tidak dapat menonaktifkannya di organisasi tersebut. Organisasi yang terhubung ke profil Verification Portal Anda, saat ini atau di kemudian hari, juga dapat memperoleh Access Transparency. Untuk mengetahui organisasi mana saja yang memiliki Access Transparency, tanyakan kepada tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Compliance API menjadi aktif dan mulai mencatat aktivitas">
    Jika salah satu dari organisasi tersebut memiliki [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need), hal ini terjadi di setiap organisasi di bawah organisasi induk tersebut, bahkan jika seseorang telah menonaktifkan Compliance API. Jika orang-orang masuk ke aplikasi seperti Claude Code dan Cowork dengan paket langganan Claude, Compliance API juga menyimpan transkrip sesi.
  </Accordion>

  <Accordion title="Anthropic dapat menyalin data ke penyimpanan Anda">
    Mendapatkan akses juga berarti bahwa workspace yang dikonfigurasi untuk menyimpan data, baik di penyimpanan yang dikelola Anthropic maupun di bucket Anda sendiri, dapat menyimpan salinan permintaan dan respons API Anda. Tim Anda hanya dapat membaca salinan jika Anda menghubungkan **Safety Case and Transcript storage** atau jika Anthropic [menandainya untuk Anda tinjau](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). Mengonfigurasi ulang pengaturan workspace atau organisasi di kemudian hari tidak menghapus salinan yang sudah disimpan.
  </Accordion>
</AccordionGroup>

### Terima ketentuan

Untuk menerima ketentuan, buka halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console dan klik **Accept terms** pada kartu **Enterprise Frontier Safeguards**. Jika Anda tidak melihat **Accept terms** di sana, masuk ke [Verification Portal](https://portal.anthropic.com), pilih organisasi Anda, lalu klik **Accept terms**.

Mintalah akses kepada tim akun Anthropic Anda jika Anda tidak dapat masuk ke Verification Portal atau juga tidak melihat **Accept terms** di sana. Jika Anda tidak memiliki tim akun, lengkapi [formulir permintaan Enterprise Frontier Safeguards](https://claude.com/form/enterprise-frontier-safeguards).

Jika organisasi Anda memiliki akses, halaman [Program](https://platform.claude.com/settings/programs) menampilkan **Enterprise Frontier Safeguards** dengan tombol **Configure**.

## 2. Tambahkan sumber daya cloud

Untuk menggunakan Enterprise Frontier Safeguards, Anda memerlukan bucket Anda sendiri. Kunci enkripsi Anda sendiri bersifat opsional. Tanpa kunci tersebut, workspace menggunakan kunci yang dikelola Anthropic. Untuk menambahkan bucket dan kunci Anda, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console dan pilih **Organisasi** di bagian atas halaman.

Untuk menggunakan kunci Anda sendiri, buat [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys) di layanan manajemen kunci Anda sendiri, lalu daftarkan kunci tersebut ke Anthropic di bawah **Kunci enkripsi**.

Untuk menyiapkan bucket Anda sebagai [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage), ikuti langkah-langkah untuk penyedia cloud Anda:

* **Amazon S3:** Ikuti [Menyiapkan penyimpanan milik pelanggan di Amazon S3](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#amazon-s3) hingga akhir [Membuat dan menghubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles).
* **Google Cloud Storage:** Ikuti [Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#google-cloud-storage) hingga akhir [Membuat dan menguji bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket).

Bucket Anda dapat digunakan oleh workspace setelah **Test setup** lulus.

## 3. Aktifkan EFS untuk workspace

Untuk mengaktifkan Enterprise Frontier Safeguards untuk workspace, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console. Pilih **Enterprise Frontier Safeguards** untuk workspace terlebih dahulu, lalu penyimpanan Anda, lalu kunci Anda sendiri jika Anda menginginkannya, lalu simpan.

Dengan EFS, Anthropic Human Review selalu nonaktif, sehingga organisasi Anda bertanggung jawab untuk meninjau setiap [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) yang dikirim Anthropic kepada Anda. Saat Anda menyimpan, Claude Console menonaktifkan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) untuk workspace tersebut.

Tentukan siapa di tim Anda yang meninjau Safety Cases. Untuk mempelajari bagaimana Safety Cases sampai ke tim Anda, lihat [Mendapatkan Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#prepare).

<Steps>
  <Step title="Pilih Enterprise Frontier Safeguards">
    Jika organisasi Anda memiliki pengaturan Legacy Zero Data Retention (ZDR), Anda perlu membuat workspace baru untuk menggunakan EFS. Claude Console menandai kartu **Enterprise Frontier Safeguards** sebagai **Ineligible** untuk workspace yang sudah ada pada **Legacy ZDR**. Untuk menggunakan EFS, pilih kartu tersebut saat Anda membuat workspace baru. Pertahankan lalu lintas Anda pada workspace lama hingga Anda menyelesaikan [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#check-your-setup).

    Untuk memilih kartu tersebut saat Anda membuat workspace, baca terlebih dahulu sisa bagian ini. Kemudian, buat workspace di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces) dan pilih **Enterprise Frontier Safeguards**, penyimpanan Anda, dan kunci Anda jika Anda menggunakannya. Kemudian, lanjutkan ke [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#check-your-setup).

    Jika Anda tidak dapat memilih bucket Anda saat membuat workspace, pastikan bucket tersebut telah lulus **Test setup**. Jika itu tidak membantu, atau Claude Console tidak menyelesaikan pembuatan workspace, hubungi tim akun Anthropic Anda.

    Untuk memilih kartu tersebut untuk workspace yang sudah Anda miliki, beralihlah dari **Organisasi** ke workspace tersebut di bagian atas halaman [Retensi data](https://platform.claude.com/settings/privacy). Anda tidak dapat memilih **Enterprise Frontier Safeguards** untuk workspace default, yang selalu mengikuti pengaturan retensi data organisasi Anda.

    Kemudian, pilih kartu **Enterprise Frontier Safeguards**.
  </Step>

  <Step title="Pilih penyimpanan Anda">
    <Warning>
      Hingga [pilihan bucket Anda berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take), data keselamatan tersegel mungkin dikirim ke penyimpanan yang dikelola Anthropic, bahkan dari workspace baru, dan bahkan jika organisasi Anda memiliki pengaturan Legacy ZDR. Kirim hanya permintaan uji tanpa data sensitif ke workspace ini hingga 10 menit setelah objek baru pertama masuk ke `slab/` atau `safeguards-data/slab/` di bucket Anda.
    </Warning>

    Pilih bucket Anda di bawah **Sealed Safety Data storage**. Claude Console tidak dapat membuat workspace dengan **Enterprise Frontier Safeguards** tanpa bucket. Secara opsional, pilih bucket tersebut di bawah **Safety Case and Transcript storage** juga, sekarang atau nanti. Workspace memiliki dua pengaturan penyimpanan:

    * **Sealed Safety Data storage:** Menetapkan ke mana Anthropic mengirim [data keselamatan tersegel](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored): prompt, respons, dan penalaran model, yang dienkripsi dalam format Anthropic. Tim Anda tidak dapat membaca data keselamatan tersegel, bahkan di bucket milik Anda sendiri.
    * **Safety Case and Transcript storage:** Menetapkan ke mana Anthropic mengirim transkrip dan Safety Cases untuk dibaca tim Anda. Untuk menerimanya di bucket Anda, lihat [Transkrip dan Safety Cases di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket).

    Jika Anda membiarkan **Safety Case and Transcript storage** pada **Not copied to your storage**, tim Anda mendapatkan Safety Cases hanya jika organisasi Anda memiliki [akses ke Safety Cases API](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#get-access).

    Setelah workspace menggunakan bucket Anda, bucket tersebut terikat ke organisasi ini. Anggap keterikatan tersebut bersifat permanen. Untuk bucket Google Cloud Storage, baca juga [Menggunakan bucket Cloud Storage Anda di workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace) sebelum Anda menyimpan.

    <Warning>
      Pastikan Compliance API aktif sebelum Anda mengirim permintaan, dan biarkan tetap aktif. Permintaan yang Anda kirim saat Compliance API nonaktif tidak memiliki transkrip, sehingga tim Anda tidak dapat meninjaunya nanti. Untuk menemukan pengaturan tersebut, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).
    </Warning>
  </Step>

  <Step title="Lampirkan kunci yang dikelola pelanggan">
    Untuk mengenkripsi data Anda dengan kunci Anda sendiri, pilih kunci tersebut di bawah **Kunci enkripsi**. Anda dapat memilih kunci setelah Anda [membuat dan mendaftarkannya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key). Melampirkan kunci bersifat permanen, jadi baca [batasan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek#what-you-commit-to) sebelum Anda menyimpan.

    Pada workspace yang sudah melayani lalu lintas, kunci dapat memerlukan waktu hingga satu hari untuk berlaku setelah Anda menyimpan.

    Kunci juga menonaktifkan beberapa fitur. Lihat [apa yang berubah dengan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed).
  </Step>
</Steps>

## 4. Tetapkan kebijakan untuk workspace baru

Secara opsional, Anda dapat menetapkan kebijakan tingkat organisasi agar workspace baru menggunakan kontrol EFS. Dengan kebijakan, Anda memilih pengaturan untuk workspace baru. Anda dapat mewajibkan agar [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) aktif atau nonaktif (di bawah **Who reviews flagged cases?**), mewajibkan penyimpanan milik pelanggan atau kunci yang dikelola pelanggan, atau menyebutkan bucket atau kunci tertentu.

[Daftarkan kunci](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#add-cloud-resources) atau [tambahkan bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage) sebelum Anda mewajibkannya, atau tidak ada yang dapat membuat workspace yang menyimpan data keselamatan tersegel.

Untuk menetapkan atau mengubah kebijakan, pilih **Organisasi** di bagian atas halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console, lalu temukan **Policy for new workspaces**.

Kebijakan ini berlaku untuk workspace baru dan tidak mengubah workspace yang sudah ada. Untuk mengubah workspace yang sudah ada, lihat [Aktifkan EFS untuk workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#turn-on-efs-for-a-workspace). Jika permintaan untuk membuat atau mengubah workspace melanggar kebijakan, Anthropic menolaknya.

## 5. Periksa penyiapan Anda

Kirim permintaan uji tanpa data sensitif ke workspace. Objek baru muncul di `slab/` atau `safeguards-data/slab/` di bucket yang Anda pilih di bawah **Sealed Safety Data storage**, setelah [pilihan bucket Anda berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Tunggu 10 menit setelah objek baru pertama sebelum Anda mengirim lalu lintas sungguhan. Jika workspace lain sudah mengirim data ke bucket ini, objek baru tidak menunjukkan bahwa perubahan ini telah berlaku, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan.

## Periksa siapa yang mengakses bucket dan kunci Anda

Untuk melihat siapa yang mengakses bucket Amazon S3 dan kunci yang dikelola pelanggan milik Anda, periksa log Anda sendiri. Jika Anda menemukan pemanggil lain, hubungi tim akun Anthropic Anda.

* **Bucket Amazon S3:** Buka **Event history** di AWS CloudTrail di `us-east-2`, meskipun bucket Anda berada di region lain. Setiap panggilan `AssumeRole` ke peran IAM yang dibuat oleh penyiapan Anda harus berasal dari akun AWS Anthropic yang disebutkan dalam file penyiapan Anda. File penyiapan Claude Console menyebutkan akun `804820989669`. Untuk juga mencatat pembacaan, penulisan, dan penghapusan objek, lihat [Panggilan Anthropic di AWS CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#cloudtrail).
* **Kunci yang dikelola pelanggan:** Setelah [kunci Anda berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), log audit kunci Anda menampilkan panggilan dari Anthropic, tetapi tidak satu panggilan untuk setiap permintaan. Setiap panggilan di luar tim Anda harus berasal dari identitas yang disebutkan oleh [halaman penyiapan untuk layanan kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up). Di AWS CloudTrail, identitas tersebut menampilkan `userIdentity.accountId` `915198916910` dan `userIdentity.principalId` yang diakhiri dengan `:anthropic-cmek`.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Tinjau Safety Cases" icon="file" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases">
    Terima, selidiki, dan tanggapi Safety Cases yang dikirim Anthropic.
  </Card>

  <Card title="Jika kunci Anda berhenti berfungsi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working">
    Apa yang terjadi pada permintaan, dan apa yang harus dilakukan.
  </Card>

  <Card title="Jika bucket Anda berhenti berfungsi" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working">
    Apa yang terjadi pada data Anda, dan cara melakukan pemulihan.
  </Card>

  <Card title="Mengubah atau berhenti menggunakan bucket Anda" icon="sliders" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket">
    Pindah ke bucket baru atau keluarkan workspace dari EFS.
  </Card>
</CardGroup>
