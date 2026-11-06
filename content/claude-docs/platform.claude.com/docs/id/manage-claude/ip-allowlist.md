---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/ip-allowlist
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: b87fe1fd27c007b21d5314ac2d5e8f1a4c66cd2dfef79710ab1108d735fa8234
---

---
title: Allowlist IP
url: https://platform.claude.com/docs/id/manage-claude/ip-allowlist
description: Amankan organisasi Anda dengan membatasi akses hanya untuk alamat IP tertentu yang Anda percayai.
featureMetadata:
  status: beta
---

“IP allowlisting” (daftar izin IP) melindungi organisasi Anda dengan hanya mengizinkan [permintaan yang dicakup](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#where-the-allowlist-applies) berasal dari rentang IP tertentu. Artinya, jika kunci API bocor, penyerang akan jauh lebih sulit menggunakan kunci tersebut. Hal ini dapat mencegah kebocoran data dan mengurangi kemungkinan Anda ditagih atas penggunaan yang menyalahgunakan.

Allowlist membatasi di mana sebuah kunci dapat digunakan, tetapi bukan berapa lama. Anda juga sebaiknya menetapkan [masa kedaluwarsa kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) yang singkat, atau beralih ke [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) agar berhenti menggunakan kunci statis. Ini lebih aman daripada hanya mengandalkan allowlist.

<Note>
  IP allowlisting tersedia dalam beta berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Note>

## Cara kerjanya

Admin atau pemilik organisasi menyiapkan daftar rentang IP di pengaturan. Daftar rentang ini mencakup seluruh organisasi Anda. Untuk setiap permintaan yang dicakup, Anthropic membandingkan alamat IP publik asal permintaan dengan daftar Anda, dan menolaknya jika tidak diizinkan.

* **Permintaan API** ke [endpoint yang dicakup](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#where-the-allowlist-applies) dari alamat di luar daftar akan ditolak. Misalnya, Messages API mengembalikan 403 `permission_error` dengan pesan `Your IP address isn't in this organization's allowed range.`
* **Orang** yang terhubung dari alamat yang tidak diizinkan melihat halaman berjudul **Your current network can’t access this organization**. Admin organisasi juga diblokir, tetapi Anda dapat secara opsional [memberi admin jalan untuk masuk kembali](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#avoid-locking-yourself-out) guna menghindari terkunci, dan dalam hal ini mereka hanya dapat mengakses pengaturan allowlist.

## Organisasi Claude Platform

### Di mana allowlist berlaku

* **Claude Console:** Akses UI dibatasi.
* **Endpoint Claude API berikut:** [Messages](https://platform.claude.com/docs/id/api/messages), [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Token Counting](https://platform.claude.com/docs/id/build-with-claude/token-counting), [Models](https://platform.claude.com/docs/id/api/models/list), [Files](https://platform.claude.com/docs/id/build-with-claude/files), dan [Skills](https://platform.claude.com/docs/id/build-with-claude/skills-guide), dengan kunci API atau token Workload Identity Federation.
* **Endpoint Claude Managed Agents berikut:** [Agents](https://platform.claude.com/docs/id/managed-agents/agent-setup), [Sessions](https://platform.claude.com/docs/id/managed-agents/sessions), [Environments](https://platform.claude.com/docs/id/managed-agents/environments), [Vaults](https://platform.claude.com/docs/id/managed-agents/vaults), dan [Memory stores](https://platform.claude.com/docs/id/managed-agents/memory), dengan kunci API atau token Workload Identity Federation.
* **API organisasi berikut:** [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), dengan [kunci yang hanya mencakup organisasi ini](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#which-key-do-you-need).

Lihat juga [Keterbatasan](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#limitations).

## Organisasi Claude Enterprise

Organisasi Claude Enterprise memiliki IP allowlist sendiri, yang hanya mengizinkan akses ke [aplikasi yang dicakupnya](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#apps-that-the-allowlist-covers) dari rentang IP tertentu. Artinya, jika kredensial masuk seorang pengguna dicuri, penyerang akan jauh lebih sulit menggunakannya. Daftar ini mencakup seluruh organisasi Anda, termasuk pemilik. Pemilik dan pemilik utama dapat menyiapkannya. Sebelum Anda [mengaktifkan allowlist](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#turn-on-the-allowlist), baca [Hindari mengunci diri Anda sendiri](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#avoid-locking-yourself-out).

### Aplikasi yang dicakup allowlist

Pengguna di luar daftar kehilangan akses ke organisasi Anda di:

* Claude di browser, aplikasi desktop, dan aplikasi seluler
* [Claude Code](https://code.claude.com/docs/id/overview), saat pengguna masuk dengan akun Claude mereka
* Claude in Chrome, [add-in Office](https://claude.com/docs/office-agents/overview), [Cowork](https://claude.com/docs/cowork/overview), dan Remote Tools

Ini mencakup konektor dan artifact di aplikasi-aplikasi tersebut, kecuali artifact yang dibagikan pengguna ke luar organisasi. Untuk Claude Science, lihat [Identity and access di kontrol admin Claude Science](https://claude.com/docs/claude-science/admin-controls#identity-and-access).

Allowlist juga mencakup [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), dengan [kunci yang hanya mencakup organisasi ini](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#which-key-do-you-need).

Lihat juga [Keterbatasan](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#limitations).

### Apa yang dapat diharapkan pengguna

Di web dan di aplikasi desktop, pengguna yang diblokir melihat halaman berjudul **Your current network can’t access this organization**. Pemilik juga diblokir, tetapi Anda dapat secara opsional [memberi pemilik jalan untuk masuk kembali](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#avoid-locking-yourself-out) guna menghindari terkunci, dan dalam hal ini mereka hanya dapat mengakses pengaturan allowlist. Di Claude Code, pengguna yang diblokir melihat error API 403 dengan pesan `Your IP address isn't in this organization's allowed range.`

* **Akun lain:** Pengguna yang diblokir tetap dapat masuk dan menggunakan organisasi lain atau akun pribadi.
* **Pengguna jarak jauh:** Ponsel yang menggunakan data seluler, Wi-Fi rumah, dan laptop di luar VPN akan diblokir sampai terhubung melalui jaringan yang tercantum.
* **Proxy:** Beberapa fitur terhubung melalui `bridge.claudeusercontent.com`: Claude in Chrome, Cowork, Remote Tools, dan [bekerja lintas aplikasi](https://claude.com/docs/office-agents/work-across-apps) di add-in Office. Jika proxy Anda mengirimkan host tersebut keluar melalui alamat yang berbeda dari `claude.ai` dan `api.anthropic.com`, cantumkan juga alamat itu.

## Keterbatasan

* **Claude Platform:** Allowlist mencakup permintaan ke endpoint [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), bukan agen itu sendiri. Allowlist tidak berlaku untuk jaringan apa pun di runtime Claude Managed Agents. Allowlist tidak berlaku untuk [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview), atau [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).
* **Claude Enterprise:** Claude Design, Claude in Slack, dan Claude Academy tidak dicakup. Jika Claude sedang mengerjakan tugas dalam sebuah chat saat pengguna diblokir, tugas tersebut dapat berlanjut hingga 24 jam. Pengguna tidak dapat membuka atau mengontrol chat tersebut dari luar daftar.

## Mengaktifkan allowlist

<Steps>
  <Step title="Aktifkan toggle">
    Buka halaman pengaturan organisasi Anda:

    * **Claude Platform:** Halaman [Identitas dan akses](https://platform.claude.com/settings/identity) di Claude Console
    * **Claude Enterprise:** [claude.ai > Pengaturan organisasi > Organisasi dan Akses](https://claude.ai/admin-settings/organization#ip-allowlist)

    Aktifkan toggle **IP allowlist**. Tidak ada yang berubah sampai Anda menyimpan.
  </Step>

  <Step title="Tambahkan rentang Anda dan simpan">
    Klik **Tambahkan entri** (Claude Console) atau **Tambahkan rentang IP** (claude.ai), masukkan satu atau beberapa alamat atau rentang yang dipisahkan dengan koma, lalu tekan Enter. Cantumkan setiap jaringan tempat server, CI, dan pengguna Anda terhubung, termasuk jaringan yang sedang Anda gunakan untuk terhubung. Anthropic menyarankan untuk memastikan kotak centang **Izinkan admin mengakses halaman pengaturan ini dari alamat IP mana pun** (Claude Console) atau **Izinkan pemilik mengakses halaman pengaturan ini dari alamat IP mana pun** (claude.ai) dipilih guna [menghindari terkunci](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#avoid-locking-yourself-out). Lalu klik **Simpan** dan konfirmasi.
  </Step>

  <Step title="Periksa lalu lintas Anda">
    Perubahan dapat memerlukan waktu hingga 15 menit untuk diterapkan. Pantau aplikasi Anda untuk respons 403 `permission_error`, termasuk job yang hanya berjalan harian atau mingguan, dan tambahkan alamat apa pun yang terlewat. Di organisasi Claude Enterprise, minta pengguna di setiap jaringan untuk mengonfirmasi bahwa mereka masih dapat membuka Claude. Di sana, perubahan dapat memerlukan waktu lebih lama untuk menjangkau koneksi yang sudah terbuka, add-in Office, dan Remote Tools.
  </Step>
</Steps>

### Format entri

* **Format:** Anda dapat memasukkan alamat IPv4 atau IPv6 ke allowlist. Setiap entri dapat berupa alamat tunggal (`203.0.113.5`) atau rentang CIDR (`203.0.113.0/24`, `2001:db8::/32`) yang tidak lebih luas dari `/8` untuk IPv4 atau `/32` untuk IPv6. Daftar dapat memuat hingga 1.000 entri.
* **Hanya alamat publik:** Cantumkan alamat tempat lalu lintas Anda keluar dari jaringan Anda, bukan rentang privat seperti `10.0.0.0/8`. Jika Anda menambahkan alamat proxy bersama, perhatikan bahwa penyerang yang memiliki kunci yang bocor atau kredensial masuk yang dicuri berpotensi dapat menggunakannya melalui proxy tersebut.

## Hindari mengunci diri Anda sendiri

Saat Anda menyimpan, halaman pengaturan memeriksa alamat Anda saat ini terhadap daftar untuk memastikan Anda tidak akan mengunci diri sendiri. Namun, halaman tersebut tidak memeriksa server Anda, rekan tim Anda, atau alamat yang mungkin Anda gunakan untuk terhubung besok.

* **Pastikan untuk mencantumkan setiap jaringan terlebih dahulu:** Sertakan pusat data, sistem CI, kantor, VPN, proxy, dan worker dari [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) apa pun, beserta alamat IPv4 dan IPv6 publiknya. Perhatikan bahwa alamat rumah dan seluler sering kali dapat berubah tanpa pemberitahuan.
* **Sisakan jalan untuk masuk kembali:** Anthropic menyarankan untuk memilih kotak centang **Izinkan admin mengakses halaman pengaturan ini dari alamat IP mana pun** (Claude Console) atau **Izinkan pemilik mengakses halaman pengaturan ini dari alamat IP mana pun** (claude.ai). Dengan begitu, admin (pemilik di claude.ai) dapat memperbaiki daftar dari mana saja. Kekurangannya adalah penyerang yang menyusupi sesi seorang admin atau pemilik dapat memperbarui allowlist dari lokasi jarak jauh. Jika Anda [menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk organisasi Anda, [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed)-nya mencatat perubahan pada allowlist, sehingga Anda dapat mengauditnya.

### Jika Anda terkunci

Di organisasi Claude Enterprise, admin tidak dapat mengubah daftar, sehingga “admin atau pemilik” dalam langkah-langkah ini berarti pemilik atau pemilik utama.

1. **Hubungkan kembali dari jaringan yang tercantum:** Hubungkan ke jaringan kantor atau VPN Anda, lalu klik **Try again**. Jika tidak ada tombol **Try again**, muat ulang halaman.
2. **Minta bantuan admin atau pemilik lain:** Admin atau pemilik yang berada di jaringan yang tercantum dapat menambahkan alamat Anda.
3. **Perbaiki daftar dari lokasi Anda:** Jika Anda adalah admin atau pemilik dan kotak centang di bawah [Sisakan jalan untuk masuk kembali](https://platform.claude.com/docs/id/manage-claude/ip-allowlist#avoid-locking-yourself-out) dipilih, buka Claude Console atau Claude di browser dan klik **Buka daftar IP yang diizinkan**, atau buka halaman [Identitas dan akses](https://platform.claude.com/settings/identity) ([Organisasi dan Akses](https://claude.ai/admin-settings/organization#ip-allowlist) di claude.ai). Klik **Tambahkan** untuk menambahkan alamat Anda saat ini, atau nonaktifkan allowlist, lalu klik **Simpan** dan konfirmasi. Akses dapat memerlukan waktu hingga 15 menit untuk pulih.
4. **Hubungi Anthropic:** Jika tidak ada admin atau pemilik yang dapat mengakses halaman tersebut, minta [dukungan Anthropic](https://support.claude.com) untuk menonaktifkan allowlist.
