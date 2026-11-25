---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 03e39c8658137b833c7e6daf1c1a2b80857fdcf1464133bfef607b8d9513fa40
---

---
title: Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws
description: Aktifkan Enterprise Frontier Safeguards untuk workspace Claude Platform on AWS, lalu pilih pengaturan penyimpanan dan kuncinya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Anda menyiapkan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS) di Claude Console, yang Anda buka dari AWS Console. EFS berlaku untuk setiap permintaan ke setiap model dalam workspace tempat Anda mengaktifkannya. Untuk menentukan workspace mana yang sebaiknya menggunakannya, lihat [Rencanakan penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#plan-your-setup).

Penyiapan terdiri dari tiga bagian:

1. Tambahkan sumber daya cloud: bucket penyimpanan dan kunci enkripsi Anda.
2. Aktifkan EFS untuk workspace.
3. Periksa penyiapan Anda.

## Rencanakan penyiapan Anda

Rencanakan penyiapan Anda terlebih dahulu, karena Anda tidak dapat membatalkan beberapa pilihan.

Pertama, tentukan [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) mana yang menggunakan Enterprise Frontier Safeguards. Untuk menggunakan EFS hanya untuk sebagian lalu lintas, gunakan workspace terpisah. Workspace default tidak dapat menggunakan EFS.

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

    Jika organisasi AWS Anda memblokir akun luar dengan kebijakan kontrol sumber daya (RCP), mintalah sejak awal [pengecualian untuk akun AWS Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic).

    Anthropic tidak mengenakan biaya untuk EFS, tetapi penyedia cloud Anda akan menagih Anda untuk penyimpanan, pembacaan, penulisan, dan operasi kunci, ditambah transfer jaringan yang berlaku. Anthropic membaca dan menulis bucket Anda dari region milik Anthropic sendiri, yang dapat memengaruhi biaya transfer jaringan Anda.
  </Accordion>

  <Accordion title="Siapa di tim saya yang perlu dilibatkan?">
    Untuk menyiapkan EFS dan meninjau Safety Cases setelahnya, Anda memerlukan orang-orang berikut:

    | Siapa | Apa yang mereka lakukan |
    | ----- | ----- |
    | Admin cloud | Menjalankan file penyiapan dari Claude Console yang membuat bucket dan kunci serta memberikan akses kepada Anthropic, untuk [Amazon S3](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles). |
    | Admin organisasi | Di Claude Console, menghubungkan bucket, mengaktifkan EFS untuk setiap workspace, dan melampirkan kunci apa pun. |
    | Peninjau Anda | [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). |
  </Accordion>
</AccordionGroup>

## Sebelum Anda memulai

Untuk menyiapkan Enterprise Frontier Safeguards, Anda memerlukan hal-hal berikut:

* Peran Admin di Claude Console. Untuk mendapatkan peran tersebut, buka halaman layanan **Claude Platform on AWS** di AWS Console, pilih **Admin**, dan klik **Sign in**. Masuklah dengan cara ini sebelum Anda mengikuti tautan di halaman ini ke Claude Console. Setiap tautan terbuka di organisasi Anthropic tempat browser Anda masuk.
* [Akses ke EFS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#what-getting-access-changes) untuk organisasi Anda.
* [Izin IAM](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#iam-permissions) untuk IAM principal Anda.

Gunakan workspace baru untuk EFS, meskipun Anda sudah memiliki workspace. Anthropic merekomendasikan agar Anda menetapkan **AWS region** workspace tersebut ke `us-east-2` untuk menghindari biaya transfer jaringan, tetapi ini tidak wajib. Anda tidak dapat mengubah region nanti.

Jika organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR), ikuti langkah-langkah berikut:

1. [Tambahkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#add-cloud-resources), pastikan bucket tersebut lulus **Test setup**, lalu kembali ke daftar ini.
2. Baca [Aktifkan EFS untuk workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#turn-on-efs-for-a-workspace).
3. Buat workspace di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces). Saat Anda membuatnya, pilih kartu **Enterprise Frontier Safeguards** dan bucket Anda di bawah kedua pengaturan penyimpanan. Jika Anda tidak dapat memilih kartu tersebut atau bucket Anda, atau Claude Console tidak selesai membuat workspace, hubungi tim akun Anthropic Anda.
4. Untuk menggunakan kunci Anda sendiri, [buat dan daftarkan kunci tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#add-cloud-resources), lalu lampirkan di halaman [Retensi data](https://platform.claude.com/settings/privacy) workspace.
5. Lanjutkan ke [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#check-your-setup).

Jika tidak, sebelum Anda memulai, buat workspace di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces), dan jangan pilih kartu **Enterprise Frontier Safeguards**. Kartu tersebut memerlukan bucket Anda, yang Anda tambahkan setelah Anda membuat workspace. Jangan kirim permintaan apa pun ke workspace hingga Anda [mengaktifkan EFS untuknya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#turn-on-efs-for-a-workspace).

## Apa yang berubah saat Anda mendapatkan akses

<Warning>
  Menerima ketentuan akan mengaktifkan Compliance API untuk organisasi Anda, dan untuk organisasi lain mana pun yang memenuhi syarat yang terhubung ke profil [Verification Portal](https://portal.anthropic.com) Anda.
</Warning>

Menerima ketentuan juga memungkinkan Admin organisasi untuk menonaktifkan Anthropic Human Review. Jika tim akun Anthropic Anda telah memberikan akses kepada organisasi Anda, lewati bagian ini.

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

Untuk menerima ketentuan, buka halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console dan klik **Accept terms** pada kartu **Enterprise Frontier Safeguards**. Jika Anda tidak melihat **Accept terms** di sana, klik **Open Verification Portal** di halaman yang sama, lalu klik **Accept terms** di Verification Portal.

Mintalah akses kepada tim akun Anthropic Anda jika Anda tidak dapat membuka Verification Portal atau juga tidak melihat **Accept terms** di sana. Jika Anda tidak memiliki tim akun, lengkapi [formulir permintaan Enterprise Frontier Safeguards](https://claude.com/form/enterprise-frontier-safeguards).

## 1. Tambahkan sumber daya cloud

Untuk menggunakan Enterprise Frontier Safeguards, Anda memerlukan bucket Anda sendiri. Kunci enkripsi Anda sendiri bersifat opsional. Tanpa kunci tersebut, workspace menggunakan kunci yang dikelola Anthropic. Untuk menambahkan bucket dan kunci Anda, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console dan pilih **Organisasi** di bagian atas halaman.

Untuk menggunakan kunci Anda sendiri, buat [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws) di AWS KMS, di region workspace, lalu daftarkan kunci tersebut ke Anthropic di bawah **Kunci enkripsi**. Contoh kebijakan kunci di panduan yang ditautkan memerlukan ID kompartemen workspace, jadi buat workspace terlebih dahulu.

Untuk menyiapkan bucket Anda untuk [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=aws), baca [apa yang diperlukan bucket dan akun AWS-nya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=aws#before-you-begin), lalu [buat dan hubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=aws#create-the-bucket-and-roles). Di Claude Console, dialog **Connect storage** mengisi **AWS account ID** dengan ID akun AWS tempat Anda mendaftar. Untuk membuat bucket Anda di akun AWS yang berbeda, ubah ID tersebut. Workspace dapat menggunakan bucket Anda setelah **Test setup** lulus.

## 2. Aktifkan EFS untuk workspace

Untuk mengaktifkan Enterprise Frontier Safeguards untuk workspace, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console. Untuk workspace tersebut, pilih **Enterprise Frontier Safeguards** dan penyimpanan Anda, tambahkan kunci Anda sendiri jika Anda menginginkannya, lalu simpan satu kali.

<Steps>
  <Step title="Pilih Enterprise Frontier Safeguards">
    Jika organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR), Anda perlu membuat workspace baru untuk menggunakan EFS. Claude Console menandai kartu **Enterprise Frontier Safeguards** sebagai **Ineligible** untuk workspace yang sudah ada yang menggunakan **Legacy ZDR**. Untuk menggunakan EFS, pilih kartu tersebut saat Anda membuat workspace, seperti yang dijelaskan di [Sebelum Anda memulai](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#before-you-begin). Biarkan lalu lintas Anda tetap di workspace yang sudah ada hingga Anda menyelesaikan [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#check-your-setup).

    Jika tidak, di bagian atas halaman, beralihlah dari **Organisasi** ke workspace yang Anda buat untuk EFS. Kemudian, pilih kartu **Enterprise Frontier Safeguards**.

    Jika Claude Console menandai kartu tersebut **Ineligible**, tooltip pada lencana tersebut menjelaskan alasannya dan apa yang harus dilakukan. Jika Claude Console menyembunyikan kartu tersebut, hubungi tim akun Anthropic Anda.

    Tetap di halaman ini untuk langkah-langkah selanjutnya, dan jangan menyimpan hingga langkah terakhir.
  </Step>

  <Step title="Pilih penyimpanan Anda">
    <Warning>
      Hingga [pilihan bucket Anda berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=aws#how-long-changes-take), data keselamatan tersegel mungkin dikirim ke penyimpanan yang dikelola Anthropic, bahkan dari workspace baru, dan bahkan jika organisasi Anda memiliki perjanjian Legacy ZDR. Kirim hanya permintaan uji tanpa data sensitif ke workspace ini hingga 10 menit setelah objek baru pertama tiba di bawah `slab/` atau `safeguards-data/slab/` di bucket Anda.
    </Warning>

    Pilih bucket Anda di bawah kedua pengaturan penyimpanan workspace:

    * **Sealed Safety Data storage:** Menetapkan ke mana Anthropic mengirim [data keselamatan tersegel](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage?cloud=aws#what-is-stored): prompt, respons, dan penalaran model, yang dienkripsi dalam format Anthropic. Tim Anda tidak dapat membaca data keselamatan tersegel, bahkan di bucket milik Anda sendiri.
    * **Safety Case and Transcript storage:** Menetapkan ke mana Anthropic mengirim transkrip dan [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) untuk dibaca tim Anda.

    Pilih bucket Anda di bawah **Safety Case and Transcript storage** meskipun Claude Console menandai pengaturan tersebut sebagai opsional. EFS mewajibkan bucket di sana. Jika Anda membiarkan pengaturan tersebut kosong, tindakan simpan Anda mungkin gagal atau membiarkan Anthropic Human Review tetap aktif.

    Perhatikan hal-hal berikut saat Anda memilih bucket Anda:

    * Jika Claude Console tidak menampilkan **Safety Case and Transcript storage**, hubungi tim akun Anthropic Anda sebelum Anda menyimpan. Jika Claude Console menolak bucket Anda, hubungi tim akun Anthropic Anda sebelum Anda menghubungkan bucket lain.
    * Setelah Anda menyimpan bucket di bawah **Safety Case and Transcript storage**, Anda tidak dapat mengosongkan pengaturan tersebut selama workspace menggunakan EFS. Untuk [pindah ke bucket lain](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-your-bucket), tanyakan terlebih dahulu kepada tim akun Anthropic Anda.
    * Jika bucket Anda berhenti berfungsi, beri tahu tim akun Anthropic Anda segera setelah Anda menyadarinya. Anthropic tidak dapat menulis data ke bucket Anda selama kegagalan tersebut. Sekitar 1 hari setelah data tersebut dikirim, Anthropic menghapus data apa pun yang belum dipulihkan. Lihat [Jika bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working).

    Setelah workspace menggunakan bucket Anda, bucket tersebut terikat ke organisasi ini, dan Anda tidak dapat menghapus tujuan penyimpanannya. Anggap keterikatan tersebut bersifat permanen.

    <Warning>
      Pastikan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) aktif sebelum Anda mengirim permintaan, dan biarkan tetap aktif. Permintaan yang Anda kirim saat API tersebut nonaktif mungkin tidak memiliki transkrip, bahkan setelah Anda mengaktifkannya. Di tab lain, temukan tombol **Compliance API** di halaman [Kepatuhan](https://platform.claude.com/settings/security).
    </Warning>
  </Step>

  <Step title="Lampirkan kunci yang dikelola pelanggan">
    Untuk mengenkripsi data Anda dengan kunci Anda sendiri, pilih kunci tersebut di bawah **Kunci enkripsi**. Anda dapat memilih kunci setelah Anda [membuat dan mendaftarkannya](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws). Melampirkan kunci bersifat permanen, jadi baca [batasan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek#what-you-commit-to) sebelum Anda menyimpan.

    Kunci juga menonaktifkan beberapa fitur. Lihat [apa yang berubah dengan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed).
  </Step>

  <Step title="Simpan">
    Saat Anda menyimpan, Claude Console menonaktifkan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) untuk workspace tersebut. Dengan EFS, Anthropic Human Review selalu nonaktif. Setelah perubahan itu berlaku, [tim kecil yang terspesialisasi di Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#who-at-anthropic-can-access-your-data) tidak lagi meninjau prompt dan respons baru dari workspace. Sejak saat itu, meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) menjadi tugas tim Anda.
  </Step>
</Steps>

## 3. Periksa penyiapan Anda

Kirim permintaan uji tanpa data sensitif ke workspace. Objek baru muncul di bawah `slab/` atau `safeguards-data/slab/` di bucket yang Anda pilih di bawah **Sealed Safety Data storage**, setelah [pilihan bucket Anda berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=aws#how-long-changes-take). Tunggu 10 menit setelah objek baru pertama sebelum Anda mengirim lalu lintas sungguhan. Jika workspace lain sudah mengirim data ke bucket ini, objek baru tidak menunjukkan bahwa perubahan ini telah berlaku, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan.

Di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces), pilih workspace dan pastikan **Cases, transcripts** di bawah **Data retention** menampilkan bucket yang Anda pilih di bawah **Safety Case and Transcript storage**. Jika nilai tersebut tidak ada atau menampilkan bucket lain, hubungi tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan. Jika nilai tersebut menampilkan **Not copied to your storage**, pilih bucket Anda di bawah **Safety Case and Transcript storage** di halaman [Retensi data](https://platform.claude.com/settings/privacy) workspace, lalu klik **Save**.

## Periksa siapa yang mengakses bucket dan kunci Anda

Untuk melihat siapa yang mengakses bucket Amazon S3 dan kunci yang dikelola pelanggan milik Anda, periksa log Anda sendiri. Jika Anda menemukan pemanggil lain, hubungi tim akun Anthropic Anda.

* **Bucket Amazon S3:** Buka **Event history** di AWS CloudTrail di `us-east-2`, meskipun bucket Anda berada di region lain. Setiap panggilan `AssumeRole` ke peran IAM yang dibuat oleh penyiapan Anda harus berasal dari akun AWS Anthropic yang disebutkan dalam file penyiapan Anda. File penyiapan Claude Console menyebutkan akun `804820989669`. Untuk juga mencatat pembacaan, penulisan, dan penghapusan objek, lihat [Panggilan Anthropic di AWS CloudTrail](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage?cloud=aws#cloudtrail).
* **Kunci yang dikelola pelanggan:** Setelah [kunci Anda berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), CloudTrail menampilkan panggilan `Encrypt` atau `Decrypt` pada kunci Anda, tetapi tidak satu untuk setiap permintaan. Setiap panggilan dari luar tim Anda seharusnya menampilkan `userIdentity.invokedBy` `aws-external-anthropic.amazonaws.com`, yaitu service principal AWS yang diizinkan oleh kebijakan kunci Anda.

## Izin IAM

IAM principal yang Anda gunakan untuk masuk memerlukan izin untuk menyiapkan penyimpanan. Kebijakan `AnthropicFullAccess` menyertakannya. Dalam kebijakan Anda sendiri, izinkan tindakan `aws-external-anthropic` berikut pada `Resource: "*"`:

* `RegisterAccountExternalStorage`: Menghubungkan tujuan penyimpanan.
* `ActivateAccountExternalStorage`: Menjalankan **Test setup**.
* `GetAccountExternalStorage`: Melihat tujuan penyimpanan.
* `ListAccountExternalStorages`: Menampilkan daftar tujuan penyimpanan Anda.
* `UpdateAccountExternalStorage`: Mengubah nama tampilan tujuan penyimpanan.
* `DeregisterAccountExternalStorage`: Menghapus tujuan penyimpanan. Ini tidak menghapus bucket S3 Anda.
* `GetAccountPrograms`: Melihat apa yang telah disetujui Anthropic untuk organisasi Anda.
* `GetAccountWorkspacePolicy`: Melihat kebijakan organisasi Anda untuk workspace baru.
* `UpdateAccountWorkspacePolicy`: Mengubah kebijakan organisasi Anda untuk workspace baru.
* `UpdateComplianceSettings`: Mengubah pengaturan Compliance API.

Izinkan tindakan ini meskipun [Tindakan IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) tidak mencantumkannya. Halaman tersebut mencantumkan tindakan lain yang Anda perlukan di bagian 1 dan 2:

* `AssumeConsole`
* `CreateWorkspace`
* `ListWorkspaces`
* `GetWorkspace`
* `UpdateWorkspace`
* `RegisterKey`
* `ListKeys`
* `GetKey`

IAM principal Anda juga memerlukan dua tindakan AWS STS: `sts:GetWebIdentityToken` dan `sts:TagGetWebIdentityToken`. Kebijakan `AnthropicFullAccess` menyertakan keduanya. Jika Anda menggunakan kebijakan Anda sendiri, berikan kedua tindakan tersebut seperti yang ditunjukkan di [Kebijakan IAM](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#iam-policies).

Untuk melampirkan kunci, Anda juga memerlukan [izin KMS untuk kunci tersebut](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#prerequisites).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Jika kunci Anda berhenti berfungsi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working">
    Apa yang terjadi pada permintaan, dan apa yang harus dilakukan.
  </Card>

  <Card title="Jika bucket Anda berhenti berfungsi" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working">
    Apa yang terjadi pada data Anda, dan cara memulihkannya.
  </Card>

  <Card title="Mengubah atau berhenti menggunakan bucket Anda" icon="sliders" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket">
    Pindah ke bucket baru atau keluarkan workspace dari EFS.
  </Card>
</CardGroup>
