---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: 9a9a93b99d5aaaa81fdbad529b581ed122aa39786771506cca916110fff86ec6
---

---
title: Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed
description: Aktifkan Enterprise Frontier Safeguards untuk sebuah workspace di Claude Models on Google Cloud (Anthropic managed), lalu pilih penyimpanan dan kuncinya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Untuk menyiapkan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS), buka Claude Console dari Google Cloud console. EFS berlaku untuk setiap permintaan ke setiap model di workspace tempat Anda mengaktifkannya. Untuk memutuskan workspace mana yang sebaiknya menggunakannya, lihat [Rencanakan penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#plan-your-setup).

Penyiapan terdiri dari tiga bagian:

1. Tambahkan sumber daya cloud: bucket penyimpanan dan kunci enkripsi Anda.
2. Aktifkan EFS untuk sebuah workspace.
3. Periksa penyiapan Anda.

## Rencanakan penyiapan Anda

Rencanakan penyiapan Anda terlebih dahulu, karena Anda tidak dapat membatalkan beberapa pilihan.

Pertama, tentukan [workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) mana yang menggunakan Enterprise Frontier Safeguards. Untuk menggunakan EFS hanya untuk sebagian lalu lintas, gunakan workspace terpisah. Default Workspace tidak dapat menggunakan EFS.

Jika organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR), gunakan workspace baru untuk EFS, dan pilih kartu **Enterprise Frontier Safeguards** saat Anda membuatnya. Di Claude Console, Anda tidak dapat memilih kartu tersebut untuk workspace yang sudah ada pada **Legacy ZDR**.

Terakhir, jawab pertanyaan-pertanyaan berikut:

<AccordionGroup>
  <Accordion title="Di mana seharusnya bucket saya berada, dan berapa biayanya?">
    Pilih akun cloud dan region untuk bucket Anda sebelum Anda memulai:

    * **Google Cloud Storage:** Lihat [apa yang diperlukan oleh bucket dan proyeknya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-before-you-begin) serta [region yang didukung](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#supported-regions).

    Anthropic tidak mengenakan biaya untuk EFS, tetapi penyedia cloud Anda akan menagih Anda untuk penyimpanan, pembacaan, penulisan, dan operasi kunci, ditambah transfer jaringan yang berlaku. Anthropic membaca dan menulis bucket Anda dari region milik Anthropic sendiri, yang dapat memengaruhi biaya transfer jaringan Anda.
  </Accordion>

  <Accordion title="Siapa di tim saya yang perlu dilibatkan?">
    Untuk menyiapkan EFS dan meninjau Safety Cases setelahnya, Anda memerlukan orang-orang berikut:

    | Siapa | Apa yang mereka lakukan |
    | ----- | ----- |
    | Admin cloud | Menjalankan file penyiapan dari Claude Console yang membuat bucket dan kunci serta memberikan akses kepada Anthropic, untuk [Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket). |
    | Admin organisasi | Di Claude Console, menghubungkan bucket, mengaktifkan EFS untuk setiap workspace, dan melampirkan kunci apa pun. |
    | Peninjau Anda | [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). |
  </Accordion>
</AccordionGroup>

## Sebelum Anda memulai

Untuk menyiapkan Enterprise Frontier Safeguards, Anda memerlukan hal-hal berikut:

* [`roles/claude.admin`](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console) pada proyek Google Cloud yang organisasinya akan menggunakan EFS.
* [Akses ke EFS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#what-getting-access-changes) untuk organisasi Anda, dari tim akun Anthropic Anda. Mendapatkan akses dapat mengubah pengaturan yang tidak dapat Anda kembalikan.
* Untuk menggunakan kunci Anda sendiri: [kunci yang dikelola pelanggan diaktifkan](https://platform.claude.com/docs/id/manage-claude/cmek#availability) untuk organisasi Anda.

## Apa yang berubah saat Anda mendapatkan akses

<Warning>
  Menerima ketentuan akan mengaktifkan Compliance API untuk organisasi Anda, dan untuk organisasi lain mana pun yang memenuhi syarat yang terhubung ke profil [Verification Portal](https://portal.anthropic.com) Anda.
</Warning>

Menerima ketentuan juga memungkinkan Admin Organisasi untuk menonaktifkan Anthropic Human Review. Jika tim akun Anthropic Anda telah memberikan akses kepada organisasi Anda, lewati bagian ini.

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

## 1. Tambahkan sumber daya cloud

Untuk membuka Claude Console, buka [Claude Platform](https://console.cloud.google.com/agent-platform/claude-platform) di Google Cloud console dan pilih proyek Anda. Kemudian, pilih **Anthropic managed** lalu klik **Open Claude Console**. Lakukan ini sebelum Anda mengikuti tautan di halaman ini ke Claude Console. Setiap tautan terbuka di organisasi Anthropic tempat browser Anda masuk. Untuk memeriksa organisasi tempat Anda berada, buka **Pengaturan** > **Organisasi**. **Google Cloud project number** harus menampilkan nomor proyek Anda, bukan ID-nya. Jika halaman tidak memiliki baris tersebut, kemungkinan Anda berada di organisasi lain.

Untuk menggunakan EFS, Anda memerlukan bucket Anda sendiri. Kunci enkripsi Anda sendiri bersifat opsional. Tanpa kunci tersebut, sebuah workspace menggunakan kunci yang dikelola Anthropic. Untuk menambahkan bucket dan kunci Anda, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console dan pilih **Organisasi** di bagian atas halaman.

Untuk menggunakan kunci Anda sendiri, buat [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms) di Google Cloud KMS, lalu daftarkan ke Anthropic di bawah **Encryption keys**. Ikuti tab **Claude Platform** dan berhenti sebelum **Lampirkan kunci ke workspace**. Gunakan kunci yang berbeda dari kunci milik bucket Anda sendiri, yang Anda buat bersama bucket tersebut.

Untuk menyiapkan bucket Anda untuk penyimpanan milik pelanggan, gunakan bucket baru khusus untuk organisasi ini saja. Jika organisasi ini sudah memiliki bucket, Anda dapat menggunakan bucket tersebut. Ikuti [Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#google-cloud-storage) sampai akhir [Buat dan uji bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#gcs-create-the-bucket).

Cloud Audit Logs tidak mencatat beberapa perubahan yang Anda buat di halaman Retensi data. Perubahan tersebut adalah perubahan terhadap tujuan penyimpanan, kebijakan untuk workspace baru, serta penyimpanan, kunci, atau Anthropic Human Review sebuah workspace.

## 2. Aktifkan EFS untuk sebuah workspace

Untuk mengaktifkan Enterprise Frontier Safeguards, buat sebuah workspace. Kemudian, pilih kartu **Enterprise Frontier Safeguards** dan penyimpanan Anda, tambahkan kunci Anda sendiri jika Anda menggunakannya, dan simpan satu kali.

<Steps>
  <Step title="Buat workspace">
    Buat workspace baru untuk EFS di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces), meskipun Anda sudah memiliki workspace. Default Workspace tidak dapat menggunakan EFS.

    * **Jika Anda dapat memilih kartu Enterprise Frontier Safeguards:** Anda dapat mengaktifkan EFS saat membuat workspace. Pertama, baca sisa bagian ini. Kemudian, pilih kartu tersebut, bucket Anda di bawah kedua pengaturan penyimpanan, dan kunci Anda jika Anda menggunakannya. Buat workspace tersebut lalu lanjutkan ke [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#check-your-setup).
    * **Jika tidak, dan organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR):** Jangan buat workspace tersebut. Periksa bahwa bucket Anda lolos **Test setup**. Jika lolos, hubungi tim akun Anthropic Anda.
    * **Jika tidak:** Buat workspace tersebut dan lanjutkan ke langkah berikutnya.

    Jangan kirim permintaan ke workspace tersebut hingga Anda mencapai [Periksa penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#check-your-setup).
  </Step>

  <Step title="Pilih Enterprise Frontier Safeguards">
    Buka halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console. Di bagian atas halaman, beralihlah dari **Organisasi** ke workspace yang Anda buat untuk EFS. Kemudian, pilih kartu **Enterprise Frontier Safeguards**. Tetaplah di halaman ini untuk langkah-langkah selanjutnya, dan jangan simpan hingga langkah terakhir.

    Jika Anda tidak dapat memilih kartu tersebut, periksa bahwa bucket Anda lolos **Test setup**. Jika lolos, hubungi tim akun Anthropic Anda.
  </Step>

  <Step title="Pilih penyimpanan Anda">
    Pilih bucket Anda di bawah **Sealed Safety Data storage**. Kemudian, pilih bucket yang sama di bawah **Safety Case and Transcript storage**. Jika Anda tidak memilih bucket di bawah **Safety Case and Transcript storage**, proses menyimpan Anda gagal.

    <Warning>
      Setelah sebuah workspace menggunakan bucket Anda, bucket tersebut terikat ke organisasi ini, dan Anda tidak dapat menghapus tujuan penyimpanannya. Anggaplah keterikatan tersebut bersifat permanen.
    </Warning>

    Sebelum Anda menyimpan, baca [Menggunakan bucket Cloud Storage Anda di sebuah workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#gcs-use-your-bucket-in-a-workspace).

    Untuk berpindah ke bucket lain, tanyakan terlebih dahulu kepada tim akun Anthropic Anda.

    Jika Claude Console tidak menampilkan **Safety Case and Transcript storage**, hubungi tim akun Anthropic Anda sebelum Anda menyimpan. Jika Claude Console menolak bucket Anda, hubungi mereka sebelum Anda menghubungkan bucket lain. Setelah Anda menyimpan bucket di bawah **Safety Case and Transcript storage**, Anda tidak dapat mengosongkan pengaturan tersebut selama workspace menggunakan EFS.

    <Warning>
      Pastikan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) aktif sebelum Anda mengirim permintaan, dan biarkan tetap aktif. Permintaan yang Anda kirim saat API tersebut nonaktif mungkin tidak memiliki transkrip, bahkan setelah Anda mengaktifkannya. Di tab lain, temukan tombol **Compliance API** di halaman [Kepatuhan](https://platform.claude.com/settings/security).
    </Warning>
  </Step>

  <Step title="Pasang kunci yang dikelola pelanggan">
    Untuk mengenkripsi data Anda menggunakan kunci Anda sendiri, pilih kunci tersebut di bawah **Encryption key**. Memasang kunci bersifat permanen, jadi baca [batasan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek#what-you-commit-to) sebelum Anda menyimpan atau membuat workspace.
  </Step>

  <Step title="Simpan">
    Saat Anda menyimpan atau membuat workspace dengan bucket Anda, Claude Console menonaktifkan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) untuk workspace tersebut. Dengan EFS, Anthropic Human Review selalu nonaktif. Setelah perubahan tersebut berlaku, [tim kecil yang terspesialisasi di Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#who-at-anthropic-can-access-your-data) tidak lagi meninjau prompt dan respons baru workspace tersebut. Sejak saat itu, meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) adalah tugas tim Anda. [Pantau bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#set-up-alerts), karena tenggat 7 hari untuk merespons dimulai saat Anthropic mengirimkan sebuah Safety Case.
  </Step>
</Steps>

## 3. Periksa penyiapan Anda

<Warning>
  Hingga [pemilihan bucket Anda berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#confirm-that-objects-arrive), data keselamatan tersegel mungkin masuk ke penyimpanan yang dikelola Anthropic, meskipun organisasi Anda memiliki perjanjian Legacy Zero Data Retention (ZDR). Hingga saat itu, kirim hanya permintaan pengujian tanpa data sensitif ke workspace ini.
</Warning>

Kirim permintaan pengujian ke workspace. Gunakan [ID workspace baru](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) dalam permintaan ini, dan di setiap permintaan selanjutnya yang harus dicakup oleh EFS. Kemudian, [pastikan objek tiba](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#confirm-that-objects-arrive) di bucket Anda. Objek-objek ini adalah data keselamatan tersegel dan tidak menunjukkan bahwa transkrip atau Safety Cases tiba.

Jangan kirim apa pun selain permintaan pengujian hingga 10 menit setelah objek baru pertama tiba di bawah `safeguards-data/slab/` di folder organisasi Anda di dalam bucket. Hingga saat itu, tetap arahkan lalu lintas Anda ke workspace yang sudah ada. Jika workspace lain sudah mengirim data ke bucket ini, objek baru tidak menunjukkan bahwa perubahan ini telah berlaku. Dalam hal tersebut, tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas nyata.

Di halaman [Ruang kerja](https://platform.claude.com/settings/workspaces), pilih workspace tersebut dan periksa bahwa **Cases, transcripts** di bawah **Data retention** menampilkan bucket Anda. Jika baris tersebut tidak ada atau menampilkan hal lain, hubungi tim akun Anthropic Anda sebelum Anda mengirim lalu lintas nyata.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Jika kunci Anda berhenti berfungsi" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-your-key-stops-working">
    Apa yang terjadi pada permintaan, dan apa yang harus dilakukan.
  </Card>

  <Card title="Jika bucket Anda berhenti berfungsi" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#gcs-if-your-bucket-stops-working">
    Apa yang terjadi pada data Anda, dan cara memulihkan bucket Anda.
  </Card>

  <Card title="Berhenti menggunakan bucket Anda" icon="sliders" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage?cloud=gcp#gcs-stop-using-your-bucket">
    Pertahankan data Anda saat Anda berhenti menggunakan bucket Anda.
  </Card>
</CardGroup>
