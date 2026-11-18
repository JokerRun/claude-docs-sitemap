---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review
fetched_at: 2026-11-18T02:14:00.973041Z
sha256: cc219b3c0bc0db4de2246dcb2627837afffa4b23c188cc51ee1b69715ef0c22c
---

---
title: Pengujian dan peninjauan aplikasi
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review
description: Bagaimana aplikasi Linked billing yang baru keluar dari tahap pengujian dan terbuka bagi pelanggan Anda, dan apa yang terjadi ketika Anda mengubah aplikasi yang aktif.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Fitur ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Dengan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections), pelanggan menautkan organisasi Claude mereka ke aplikasi OAuth Anda. Aplikasi Linked billing yang baru dimulai dalam tahap pengujian, di mana hanya “test users” (pengguna uji) yang Anda tentukan yang dapat menautkan organisasi mereka ke aplikasi tersebut. Untuk membuka aplikasi bagi pelanggan Anda, Anda memublikasikannya, lalu Anthropic meninjaunya.

Jika organisasi Anda menggunakan penagihan berbasis faktur, Anthropic tidak meninjau aplikasi Anda. Lihat [Penagihan berbasis faktur](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#invoiced-billing).

Aplikasi dianggap aktif ketika Anthropic telah menyetujuinya atau ketika Anda telah memublikasikannya dengan penagihan berbasis faktur. Setiap [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#eligible-customers-and-endpoints) dapat menautkan organisasinya ke aplikasi yang aktif, dan tautan yang dibuat oleh pengguna uji aplikasi tersebut tetap ada. Pada halaman aplikasi OAuth di Claude Console, status aplikasi yang aktif tertulis **Active**.

Sampai aplikasi aktif, Console menampilkan salah satu status berikut untuk aplikasi tersebut:

| Status           | Artinya                                                                               |
| ---------------- | ------------------------------------------------------------------------------------- |
| **Testing**      | Anda belum memublikasikan aplikasi.                                                   |
| **In review**    | Anthropic sedang meninjau aplikasi atau perubahan yang Anda buat saat aplikasi aktif. |
| **Not approved** | Anthropic telah meninjau aplikasi atau perubahan tersebut dan tidak menyetujuinya.    |

Aplikasi yang kembali ke peninjauan setelah suatu perubahan belum aktif kembali sampai Anthropic menyetujui perubahan tersebut. Setiap aplikasi Linked billing memiliki status dan pengguna ujinya sendiri. Lihat catatan di [Langkah 1: Buat aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#step-1-create-the-app) dalam panduan Linked billing.

## Sebelum memulai

Selesaikan [Proses penyiapan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#setup-process) dalam panduan Linked billing.

## Mengelola pengguna uji

### Menambahkan pengguna uji

1. Buka halaman aplikasi dari [halaman aplikasi OAuth](https://platform.claude.com/settings/oauth-apps) di Console.
2. Pada tab **Settings**, buka daftar **Test users** di bawah **Who can link**.
3. Masukkan alamat email akun Claude pengguna uji, lalu klik **Add**. Ulangi untuk setiap pengguna uji.
4. Klik **Save changes**.

Setelah Anda menyimpan, orang-orang dalam daftar dapat menautkan organisasi mereka ke aplikasi Anda. Sampai aplikasi Anda aktif, halaman persetujuan Claude, tempat seseorang menyetujui tautan, menolak orang lain. Untuk mengetahui apa yang kemudian diterima aplikasi Anda, lihat [Redirect URI Anda menerima `error=access_denied`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#access-denied) dalam panduan Linked billing.

**Who can link** tetap pada **Test users only** selama aplikasi belum aktif, dan Anda tidak dapat mengubahnya. Daftar ini dapat menampung hingga 10 pengguna uji. Setiap alamat harus sama persis dengan alamat akun, tetapi huruf besar-kecil tidak berpengaruh. Alamat dengan plus tag, seperti `name+test@example.com`, dihitung sebagai alamat yang berbeda dari `name@example.com`.

### Menautkan organisasi pengguna uji

Pengguna uji menautkan organisasinya dari aplikasi Anda dan menyetujui tautan pada halaman yang digunakan pelanggan Anda. Mereka memerlukan peran Admin atau Billing di organisasi tersebut. Langkah-langkahnya adalah Langkah 4 hingga 8 dalam panduan Linked billing. [Menguji sebagai pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#test-as-a-customer) dalam panduan tersebut memandu Anda melalui langkah-langkah itu dan menjelaskan cara memeriksa bahwa tautan telah dibuat.

Untuk menguji aplikasi sendiri, tambahkan alamat email Anda sendiri ke daftar. Organisasi yang memiliki aplikasi tidak dapat menautkan ke aplikasi tersebut, jadi gunakan organisasi Claude kedua milik Anda.

Setelah pengguna uji menautkan organisasinya, [kirim permintaan yang Anda tagihkan ke organisasi tersebut](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#step-3-update-calls-to-claude) untuk mencoba aplikasi Anda. Pengujian menggunakan uang sungguhan. Anthropic menagih organisasi setiap pengguna uji untuk permintaan yang Anda tagihkan kepadanya, sama seperti untuk pelanggan mana pun.

Sampai aplikasi Anda aktif, setiap tautan baru memerlukan “spend cap” (batas atas pengeluaran) bulanan sebesar $50 USD atau kurang. Untuk aturan batas atas tersebut, lihat [Selama aplikasi Anda dalam tahap pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#while-your-app-is-in-testing) dalam panduan.

### Menghapus pengguna uji

Penghapusan pengguna uji berlaku seketika. Penghapusan ini mengakhiri setiap tautan ke aplikasi Anda yang telah disetujui oleh orang tersebut. Setelah tautan berakhir, Claude API menolak permintaan yang Anda tagihkan ke organisasi tersebut. Lihat [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors).

1. Jika tab **Settings** memiliki perubahan yang belum disimpan, klik **Save changes** atau **Discard**. Sampai Anda melakukannya, Console tidak mengizinkan Anda menghapus pengguna uji yang telah disimpan.
2. Hapus alamat pengguna uji dari daftar **Test users**.
3. Ketika Console memintanya, klik **Remove** untuk mengonfirmasi. Anda tidak perlu mengklik **Save changes**.

## Memublikasikan aplikasi

Proses publikasi dapat meminta Anda membuktikan bahwa Anda mengendalikan domain aplikasi Anda, dengan menambahkan record DNS. Anthropic kemudian meninjau aplikasi tersebut. Perubahan DNS memerlukan waktu, jadi mulailah sebelum Anda membutuhkan pelanggan untuk menautkan.

Sebelum memublikasikan, periksa hal-hal berikut:

* Autentikasi klien telah disiapkan. Anda tidak dapat memublikasikan aplikasi sampai autentikasi klien disiapkan.
* Aplikasi Anda memiliki halaman beranda, yang Anda tetapkan pada tab **Appearance**.
* Anda dapat mengubah record DNS dari domain halaman beranda.
* Setiap redirect URI berada di domain halaman beranda atau salah satu subdomainnya.

Untuk mengetahui apa yang dianggap sebagai domain halaman beranda dan pengecualiannya, lihat [Aturan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#domain-rules).

Ikuti langkah-langkah berikut untuk memublikasikan aplikasi:

1. Pada halaman aplikasi di Console, klik **Publish app**. Sebuah kotak dialog akan terbuka.
2. Jika kotak dialog menampilkan **Prove your domain**, tambahkan record DNS TXT yang diberikannya di tempat Anda mengelola DNS untuk domain Anda. Jika tidak, lanjutkan ke langkah 5.
3. Klik **Check**. Jika domain masih menampilkan **Not proven yet**, lihat [Jika Anda tidak dapat membuktikan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#if-you-cant-prove-the-domain).
4. Ketika domain menampilkan **Proven**, klik **Continue**.
5. Jika kotak dialog menampilkan kotak centang untuk menerima Linked Billing Terms, pilih kotak tersebut. Lalu, klik **Publish app** di kotak dialog untuk mengonfirmasi.

Selama Anthropic meninjau aplikasi, statusnya adalah **In review**. Untuk hasil-hasilnya, lihat [Peninjauan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#the-review).

### Jika Anda tidak dapat membuktikan domain

* **Domain masih menampilkan Not proven yet:** Perubahan DNS dapat memerlukan waktu hingga 48 jam untuk berlaku. Anda dapat menutup kotak dialog dan kembali nanti. Jika Anda sedang memublikasikan, klik **Publish app** lagi. Jika Anda sedang mengubah aplikasi yang aktif, lakukan pengeditan yang sama lagi, dan Console memberi Anda record yang sama sampai record tersebut kedaluwarsa.
* **Check menyatakan bahwa record telah kedaluwarsa:** Record DNS berlaku selama 30 hari sejak Console pertama kali menampilkannya. Setelah itu, klik **Get a new record** dan tambahkan record baru tersebut. Domain yang menampilkan **Proven** tetap terbukti.
* **Kotak dialog menampilkan pesan sebagai ganti record:** Misalnya, pesan tersebut dapat menyatakan bahwa organisasi Anda sudah memiliki 20 nama domain. Anda tidak dapat melanjutkan sampai hal tersebut terselesaikan. Jika Anda memerlukan bantuan, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support).

### Aturan domain

Domain adalah hostname tanpa awalan `www.`, dan domain Anda adalah domain halaman beranda Anda. Misalnya, domain dari halaman beranda di `https://www.example.com` adalah `example.com`. Domain yang telah terbukti mencakup domain itu sendiri dan subdomainnya.

* **Domain bersama:** Domain bersama milik layanan hosting tidak memenuhi syarat, jadi gunakan domain milik Anda sendiri.
* **Redirect URI lokal:** Redirect URI pada `localhost`, `127.0.0.1`, atau `[::1]` tidak harus berada di domain halaman beranda.
* **Subdomain sejajar:** Jika halaman beranda Anda berada di `app.example.com`, domain Anda adalah subdomain tersebut, dan domain itu tidak mencakup redirect URI di `auth.example.com`. Salah satu cara untuk menggunakan keduanya adalah dengan meletakkan halaman beranda Anda di `example.com`, yang mencakup keduanya.
* **Domain yang telah dibuktikan oleh organisasi Anda:** Organisasi Anda mungkin telah membuktikan suatu domain sebelumnya, misalnya untuk aplikasi lain. Jika domain tersebut mencakup halaman beranda Anda dan setiap redirect URI yang tidak lokal, kotak dialog melewati **Prove your domain**. Redirect URI kemudian tidak harus berada di domain halaman beranda. Misalnya, dengan `example.com` telah terbukti, halaman beranda dan redirect URI dapat berada di subdomain yang berbeda dari domain tersebut.

## Peninjauan

Ketika peninjauan selesai, halaman aplikasi di Console menampilkan hasilnya:

* **Anthropic menyetujui aplikasi:** Aplikasi menjadi aktif. **Who can link** kemudian menampilkan **Any Claude user** tanpa langkah apa pun dari Anda, dan Console menyembunyikan daftar **Test users**.
* **Anthropic tidak menyetujui aplikasi:** Status aplikasi berubah menjadi **Not approved**.

Selama peninjauan dan setelah hasil **Not approved**, pengguna uji Anda tetap mempertahankan tautan mereka, dan Anda masih dapat menambahkan dan menghapus pengguna uji.

### Jika aplikasi tidak disetujui

Anda tidak dapat memublikasikan aplikasi lagi sendiri. Untuk menanyakan keputusan tersebut, [hubungi dukungan](https://support.claude.com/en/articles/9015913-how-to-get-support). Anda masih dapat [mengubah aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#change-an-app-that-isnt-live), tetapi perubahan tidak memulai peninjauan baru.

## Mengubah aplikasi yang aktif

Perubahan pada nama, logo, halaman beranda, atau redirect URI aplikasi yang aktif mengirimkan aplikasi tersebut kembali ke peninjauan. Sampai Anthropic menyetujui perubahan tersebut, hanya pengguna uji Anda yang dapat menautkan organisasi mereka ke aplikasi. Lihat [Sampai Anthropic menyetujui perubahan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#until-anthropic-approves-the-change). Perubahan lain, seperti izin atau autentikasi klien, tidak mengirimkan aplikasi kembali ke peninjauan.

Ikuti langkah-langkah berikut untuk mengubah nama, halaman beranda, atau redirect URI:

1. Ubah aplikasi pada tab **Appearance** (nama dan halaman beranda) atau tab **Settings** (redirect URI).

2. Klik **Save changes**. Sebuah kotak dialog akan terbuka sebelum apa pun disimpan.

3. Jika kotak dialog menampilkan **Prove your domain**, buktikan setiap domain yang disebutkannya:

   1. Tambahkan record DNS TXT untuk domain tersebut. Lalu, klik **Check**. Jika domain masih menampilkan **Not proven yet**, lihat [Jika Anda tidak dapat membuktikan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#if-you-cant-prove-the-domain).
   2. Ketika domain menampilkan **Proven**, klik **Next domain** jika masih ada domain lain. Jika tidak, klik **Continue**.

4. Klik **Save and send to review**.

Console kemudian menyimpan perubahan, dan perubahan langsung berlaku tanpa menunggu peninjauan. Selama Anthropic meninjau perubahan, status aplikasi adalah **In review**.

Untuk mengubah logo, pilih atau hapus logo pada tab **Appearance**. Kotak dialog langsung terbuka. Klik **Send to review**. Jika Anda membatalkan, logo tidak berubah.

Untuk mengubah aplikasi lagi selama statusnya **In review** atau **Not approved**, lihat [Mengubah aplikasi yang belum aktif](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#change-an-app-that-isnt-live).

### Ketika Console meminta Anda membuktikan domain

Console hanya meminta jika Anda mengubah halaman beranda atau redirect URI. Console juga memeriksa halaman beranda dan redirect URI yang tidak Anda ubah, sehingga kotak dialog dapat menyebutkan domain-domain tersebut juga. Console hanya menyebutkan domain yang tidak tercakup oleh domain terbukti mana pun milik organisasi Anda. Console tidak memeriksa redirect URI lokal, tetapi perubahan pada salah satunya tetap mengirimkan aplikasi kembali ke peninjauan.

Setelah suatu perubahan, redirect URI dapat berada di domain selain domain halaman beranda jika organisasi Anda membuktikan masing-masing domain tersebut.

### Sampai Anthropic menyetujui perubahan

Aturan-aturan berikut berlaku sejak Anda mengirim perubahan ke peninjauan:

* **Pelanggan yang sudah menautkan:** Organisasi mereka tetap tertaut, dan permintaan yang Anda tagihkan kepada mereka tetap berfungsi. Pelanggan yang membatalkan tautan tidak dapat menautkan kembali, kecuali orang yang menautkan ada dalam daftar **Test users**.
* **Tautan baru:** Pengaturan **Who can link** kembali ke **Test users only**. Console menampilkan daftar **Test users** lagi, berisi orang-orang yang sebelumnya ada di dalamnya.
* **Pengguna uji:** Anda dapat menambahkan dan menghapus orang dalam daftar. Menghapus seseorang juga mengakhiri tautan yang mereka buat ke organisasi pelanggan saat aplikasi aktif. Lihat [Menghapus pengguna uji](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#remove-a-test-user).
* **Batas atas pengeluaran organisasi yang tertaut:** Organisasi yang tertaut mempertahankan pengaturan [batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#spend-caps) saat ini, meskipun batas atasnya di atas $50 USD atau tidak memiliki batas atas. Pengaturan yang diubahnya harus mengikuti aturan dalam [Selama aplikasi Anda dalam tahap pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#while-your-app-is-in-testing).

### Ketika peninjauan perubahan selesai

Peninjauan berakhir dengan salah satu dari dua cara berikut:

* **Anthropic menyetujui perubahan:** Aplikasi aktif kembali. Setiap pelanggan yang memenuhi syarat dapat menautkan, Console menyembunyikan daftar **Test users**, dan aturan batas atas untuk aplikasi yang belum aktif tidak berlaku lagi.
* **Anthropic tidak menyetujui perubahan:** Status aplikasi berubah menjadi **Not approved**. Perubahan tetap berlaku, dan aturan dalam [Sampai Anthropic menyetujui perubahan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#until-anthropic-approves-the-change) masih berlaku. Lihat [Jika aplikasi tidak disetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#if-the-app-isnt-approved).

## Mengubah aplikasi yang belum aktif

Ikuti langkah-langkah berikut selama status aplikasi adalah **Testing**, **In review**, atau **Not approved**:

1. Ubah aplikasi pada tab **Appearance** (nama, logo, dan halaman beranda) atau tab **Settings** (redirect URI).
2. Klik **Save changes**. Perubahan logo tersimpan ketika Anda memilih atau menghapus logo.

Tidak ada kotak dialog yang meminta Anda mengonfirmasi, dan perubahan tidak mengubah status aplikasi.

Ketika Anda menyimpan perubahan pada halaman beranda atau redirect URI, Console hanya memeriksa domain selama statusnya **In review**. Aplikasi dalam tahap pengujian menjalani pemeriksaan domain saat Anda memublikasikannya. Selama peninjauan, halaman beranda aplikasi yang diubah dan setiap redirect URI yang tidak lokal harus berada di domain yang telah dibuktikan oleh organisasi Anda. Jika tidak, Console menolak perubahan tersebut, dan tidak meminta Anda membuktikan domain. Untuk pindah ke domain yang belum terbukti, tunggu hingga peninjauan selesai.

## Penagihan berbasis faktur

Dengan penagihan berbasis faktur, Anthropic menagih organisasi yang memiliki aplikasi Anda melalui faktur untuk penggunaan API-nya, dan organisasi tersebut tidak membeli kredit prabayar. Aplikasi Anda tetap dimulai dalam tahap pengujian, dan aturan untuk pengguna uji serta batas atas pengeluaran tetap berlaku. Setelah itu, ada tiga hal yang berbeda:

* **[Memublikasikan aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#publish-the-app):** Pada halaman aplikasi, klik **Publish app**. Lalu, klik **Publish app** di kotak dialog untuk mengonfirmasi. Anthropic tidak meninjau aplikasi, sehingga aplikasi langsung aktif begitu Anda memublikasikannya.
* **Halaman beranda dan domain:** Anda tidak membuktikan domain apa pun, sehingga kotak dialog melewati **Prove your domain**. Aplikasi Anda tidak memerlukan halaman beranda untuk dipublikasikan, dan aturan redirect URI di bagian [Memublikasikan aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#publish-the-app) tidak berlaku. Autentikasi klien tetap harus disiapkan terlebih dahulu.
* **[Mengubah aplikasi yang aktif](https://platform.claude.com/docs/id/manage-claude/oauth-apps/app-review#change-a-live-app):** Console menyimpan perubahan ketika Anda mengklik **Save changes** atau ketika Anda memilih atau menghapus logo. Console tidak meminta Anda membuktikan domain atau mengonfirmasi, dan tidak ada peninjauan setelahnya.
