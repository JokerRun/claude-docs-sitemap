---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 63d247e5d3ae4a08bc8545f5c550e0b6e1598a23c8f26700f1453be5e32dd57c
---

---
title: Uji dan publikasikan aplikasi Anda
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish
description: Tambahkan pengguna uji, publikasikan aplikasi Linked billing Anda agar setiap pelanggan yang memenuhi syarat dapat menautkannya, dan ubah aplikasi setelah pelanggan bergantung padanya.
featureMetadata:
  status: beta
  betaHeader: user-profiles-billing-2026-10-01
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API:
      availability: beta
      note: Hanya permintaan yang mengirim `billing_policy` yang memerlukan header beta.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Aplikasi [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing) yang baru dimulai dalam tahap pengujian, di mana hanya [pengguna uji](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#manage-test-users) yang Anda tentukan yang dapat menautkan organisasi mereka ke aplikasi tersebut. Untuk membukanya bagi pelanggan Anda, Anda membuktikan domain Anda dan [memublikasikan aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#publish-the-app), lalu Anthropic meninjaunya. Halaman ini juga membahas cara [batas atas pengeluaran bekerja selama Anda menguji](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing) serta cara mengubah atau menghapus aplikasi.

Halaman [OAuth apps](https://platform.claude.com/settings/oauth-apps) di Claude Console menampilkan status setiap aplikasi:

| Status | Artinya |
| ----- | ----- |
| **Testing** | Anda belum memublikasikan aplikasi |
| **In review** | Anthropic sedang meninjau aplikasi atau perubahan padanya |
| **Not approved** | Anthropic telah meninjau aplikasi atau perubahan tersebut dan tidak menyetujuinya |
| **Active** | Aplikasi sudah aktif: setiap [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers) dapat menautkannya |

Jika Anthropic menagih organisasi Anda melalui faktur untuk penggunaan API-nya, aplikasi Anda melewati peninjauan: lihat [Jika organisasi Anda menggunakan penagihan melalui faktur](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#with-invoiced-billing).

## Sebelum Anda memulai

Anda memerlukan peran Admin di organisasi Anda dan aplikasi yang sudah [disiapkan untuk Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app).

## Kelola pengguna uji

Hingga aplikasi Anda aktif, pengaturan **Who can link**-nya bertuliskan **Test users only**, dan Anda tidak dapat mengubahnya. Hanya orang-orang dalam daftar **Test users** yang dapat menautkan organisasi mereka ke aplikasi tersebut, dan setiap aplikasi memiliki daftarnya sendiri. Halaman persetujuan menolak orang lain, dan jika mereka kembali ke aplikasi Anda, aplikasi Anda menerima [`access_denied`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#access-denied). Setiap orang yang menautkan saat aplikasi belum aktif harus menetapkan batas atas pengeluaran bulanan sebesar $50 USD atau kurang: lihat [Batas atas selama pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing).

### Tambahkan pengguna uji

Pengujian menggunakan uang sungguhan: Anthropic menagih organisasi setiap pengguna uji untuk permintaan yang Anda tagihkan kepadanya, sama seperti pelanggan lainnya. Pengguna uji [menautkan organisasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer) tempat mereka memiliki peran Admin atau Billing. Organisasi tersebut tidak boleh organisasi yang memiliki aplikasi. Untuk menguji aplikasi sendiri, tambahkan alamat Anda sendiri dan tautkan organisasi Claude kedua milik Anda.

1. Buka aplikasi dari halaman [OAuth apps](https://platform.claude.com/settings/oauth-apps) di Console.
2. Pada tab **Settings**, temukan daftar **Test users** di bawah **Who can link**.
3. Masukkan alamat email akun Claude milik pengguna uji dan klik **Add**. Ulangi untuk setiap pengguna uji.
4. Klik **Save changes**.

Daftar ini memiliki aturan berikut:

* Daftar ini dapat memuat hingga 10 orang.
* Alamat harus sama persis dengan alamat akun, tetapi huruf besar/kecil tidak berpengaruh. `name+test@example.com` adalah alamat yang berbeda dari `name@example.com`.

### Hapus pengguna uji

<Warning>
  Menghapus pengguna uji akan mengakhiri setiap koneksi ke aplikasi Anda yang telah mereka setujui.
</Warning>

Selama peninjauan perubahan pada aplikasi yang aktif, hal ini dapat mencakup koneksi ke organisasi pelanggan. Permintaan baru yang menagih organisasi tersebut biasanya berhenti dalam sekitar 10 detik dan ditolak dengan [`user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized). Permintaan dengan token akses dari koneksi yang telah berakhir dapat menerima [`401 authentication_error`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#authentication-error) sebagai gantinya. Untuk menghapus seseorang:

1. Jika tab **Settings** memiliki perubahan yang belum disimpan, klik **Save changes** atau **Discard**. Console tidak mengizinkan Anda menghapus pengguna uji yang telah disimpan sampai Anda melakukannya.
2. Hapus alamat orang tersebut dari daftar **Test users**.
3. Saat Console meminta, klik **Remove**. Anda tidak perlu mengklik **Save changes**.

## Publikasikan aplikasi

Publikasi dapat meminta Anda menambahkan catatan DNS yang membuktikan bahwa Anda mengendalikan domain aplikasi Anda. Perubahan DNS dapat memerlukan waktu hingga 48 jam untuk berlaku, jadi publikasikan jauh sebelum Anda membutuhkan pelanggan untuk menautkan. Sebelum Anda memublikasikan, periksa hal-hal berikut:

* [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication) sudah disiapkan. Anda tidak dapat memublikasikan sampai autentikasi klien disiapkan.
* Aplikasi memiliki beranda, yang diatur pada tab **Appearance**-nya, di domain milik Anda sendiri. Domain bersama dari layanan hosting tidak memenuhi syarat.
* Anda dapat mengubah catatan DNS dari domain beranda.
* Setiap redirect URI berada pada hostname beranda, tanpa awalan `www.`, atau subdomainnya. Untuk pengecualiannya, lihat [Aturan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#domain-rules).

Untuk memublikasikan aplikasi:

1. Simpan setiap perubahan yang belum disimpan pada tab-tab aplikasi, karena Console tidak mengizinkan Anda memublikasikan sampai Anda melakukannya. Kemudian, klik **Publish app** di halaman aplikasi.
2. Jika kotak dialog menampilkan **Prove your domain**, tambahkan catatan DNS TXT yang diberikannya, di tempat Anda mengelola DNS untuk domain Anda. Kemudian, klik **Check**. Jika domain tidak bertuliskan **Proven**, lihat [Jika Anda tidak dapat membuktikan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#if-you-cant-prove-the-domain). Saat bertuliskan **Proven**, klik **Continue**.
3. Jika kotak dialog menampilkan kotak centang untuk menerima Linked Billing Terms, centang kotak tersebut. Ketentuan tersebut adalah [Linked Billing Beta Terms](https://www.anthropic.com/legal/linked-billing-terms).
4. Klik **Publish app** di kotak dialog.

Status aplikasi kemudian menjadi **In review**. Selama peninjauan dan setelah hasil **Not approved**, pengguna uji Anda tetap mempertahankan koneksi mereka, dan Anda masih dapat menambahkan serta menghapus pengguna uji. Saat peninjauan selesai, halaman aplikasi menampilkan hasilnya, dan Anthropic biasanya mengirimkannya melalui email kepada orang yang memublikasikan aplikasi:

* **Approved:** Aplikasi aktif, dan statusnya di halaman OAuth apps bertuliskan **Active**. **Who can link** bertuliskan **Any Claude user**, Console menyembunyikan daftar **Test users**, dan koneksi pengguna uji tetap ada.
* **Not approved:** Anda tidak dapat memublikasikan aplikasi lagi sendiri: lihat [Jika aplikasi tidak disetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#if-the-app-isnt-approved).

Dengan penagihan melalui faktur, Anthropic tidak meninjau aplikasi Anda: lihat [Jika organisasi Anda menggunakan penagihan melalui faktur](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#with-invoiced-billing).

## Ubah aplikasi yang aktif

<Warning>
  Mengubah nama, logo, beranda, atau redirect URI aplikasi yang aktif membatasi koneksi baru hanya untuk pengguna uji hingga Anthropic menyetujui perubahan tersebut.
</Warning>

Hingga Anthropic menyetujui perubahan tersebut:

* Pelanggan yang sudah menautkan tetap tertaut, dan permintaan yang Anda tagihkan kepada mereka tetap berfungsi.
* Pelanggan yang membatalkan tautan hanya dapat menautkan lagi melalui orang yang ada dalam daftar **Test users**.
* Perubahan pada batas mengikuti [Batas atas selama pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing).

Jika Anthropic menolak perubahan tersebut, pembatasan tetap berlaku: lihat [Jika aplikasi tidak disetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#if-the-app-isnt-approved). Untuk aturan lainnya, lihat [Saat perubahan sedang ditinjau atau tidak disetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#while-a-change-is-in-review).

Perubahan berlaku segera setelah Console menyimpannya, sehingga pelanggan melihatnya sebelum peninjauan selesai. Perubahan pada izin aplikasi atau autentikasi klien tidak memulai peninjauan, dan dengan [penagihan melalui faktur](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#with-invoiced-billing), tidak ada perubahan yang memulai peninjauan.

Untuk mengubah nama, beranda, atau redirect URI:

1. Ubah aplikasi pada tab **Appearance**-nya (nama dan beranda) atau tab **Settings**-nya (redirect URI).
2. Klik **Save changes**. Kotak dialog terbuka sebelum apa pun disimpan.
3. Jika kotak dialog menampilkan **Prove your domain**, buktikan setiap domain yang disebutkannya, satu per satu. Untuk masing-masing, tambahkan catatan DNS TXT-nya, klik **Check**, dan saat bertuliskan **Proven**, klik **Next domain** atau **Continue**. Untuk domain mana yang disebutkannya, lihat [Aturan domain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#domain-rules).
4. Klik **Save and send**, yang menyimpan perubahan dan mengirimkannya untuk ditinjau.

Untuk mengubah logo, unggah atau hapus logo pada tab **Appearance**, lalu klik **Send to review** di kotak dialog yang terbuka. Jika Anda membatalkan, logo tidak berubah.

Selama Anthropic meninjau perubahan, status aplikasi bertuliskan **In review**. Saat peninjauan selesai, Anthropic biasanya mengirimkan hasilnya melalui email kepada orang yang menyimpan perubahan.

## Ubah aplikasi yang sedang dalam pengujian atau peninjauan

Ikuti bagian ini saat status aplikasi adalah **Testing**, **In review**, atau **Not approved**. Ini termasuk aplikasi aktif yang perubahannya sedang ditinjau. Ubah aplikasi pada tab **Appearance**-nya (nama, logo, dan beranda) atau tab **Settings**-nya (redirect URI), lalu klik **Save changes**. Perubahan logo tersimpan saat Anda mengunggah atau menghapus logo.

Tidak ada kotak dialog yang meminta Anda untuk mengonfirmasi, dan status tidak berubah. Selama peninjauan, perubahan tersebut menggantikan apa yang ditinjau Anthropic dengan aplikasi sebagaimana yang Anda edit.

Console memeriksa domain yang telah dibuktikan untuk aplikasi dalam pengujian hanya saat Anda memublikasikan. Saat status adalah **In review**, beranda dan setiap redirect URI yang bukan lokal harus sudah berada pada domain organisasi Anda yang telah dibuktikan. Jika tidak, Console menolak perubahan dan tidak meminta Anda membuktikan domain. Untuk pindah ke domain yang belum dibuktikan, tunggu hingga peninjauan selesai.

## Hapus aplikasi

<Warning>
  Menghapus aplikasi membatalkan tautan setiap pelanggan dan tidak dapat dibatalkan.
</Warning>

Permintaan yang menagih pelanggan ditolak, setiap token OAuth dicabut, dan client ID berhenti berfungsi. Anthropic tidak mengirim email kepada pelanggan Anda, jadi beri tahu mereka terlebih dahulu. Untuk menghapus aplikasi:

1. Pada tab **Settings** aplikasi, simpan atau buang setiap perubahan yang belum disimpan.
2. Di bawah **Danger zone**, klik **Delete app** dan konfirmasikan dengan **Delete app**. Menu baris aplikasi di halaman [OAuth apps](https://platform.claude.com/settings/oauth-apps) juga memiliki **Delete**.

Untuk menawarkan Linked billing lagi, buat aplikasi baru, dan minta setiap pelanggan menautkannya. Aplikasi baru dimulai dalam tahap pengujian dengan client ID baru, dan batas atas pengeluaran pelanggan tidak terbawa.

## Aturan dan kasus khusus

Bagian selanjutnya dari halaman ini membahas aturan di balik publikasi dan perubahan aplikasi. Bagian ini juga membahas kasus seperti domain yang tidak dapat dibuktikan.

### Aturan domain

Domain adalah hostname tanpa awalan `www.`, sehingga beranda di `https://www.example.com` memiliki domain `example.com`. Domain Anda adalah domain beranda Anda. Domain yang telah dibuktikan mencakup dirinya sendiri dan subdomainnya, dan tetap terbukti.

* **Redirect URI lokal:** Redirect URI pada `localhost`, `127.0.0.1`, atau `[::1]` tidak harus berada pada domain beranda.
* **Subdomain setingkat:** Beranda pada `app.example.com` tidak mencakup redirect URI pada `auth.example.com`. Tempatkan beranda pada `example.com` untuk mencakup keduanya.
* **Domain yang sudah dibuktikan oleh organisasi Anda:** Jika domain tersebut mencakup beranda dan setiap redirect URI yang bukan lokal, publikasi melewati **Prove your domain**. Redirect URI kemudian tidak harus berada pada domain beranda.

Saat Anda mengubah aplikasi yang aktif, Console meminta Anda membuktikan domain hanya jika Anda mengubah beranda atau redirect URI. Console kemudian memeriksa setiap domain aplikasi, baik yang diubah maupun tidak, dan menyebutkan setiap domain yang tidak dicakup oleh domain terbukti milik organisasi Anda. Setelah perubahan seperti itu, redirect URI dapat berada pada domain selain domain beranda, jika organisasi Anda membuktikan masing-masing domain tersebut. Console tidak memeriksa redirect URI lokal, tetapi mengubahnya tetap mengirim aplikasi untuk ditinjau.

### Jika Anda tidak dapat membuktikan domain

* **Domain masih bertuliskan Not proven:** Perubahan DNS belum berlaku. Tutup kotak dialog dan kembali lagi nanti. Jika Anda sedang memublikasikan, klik **Publish app** lagi. Jika Anda sedang mengubah aplikasi yang aktif, lakukan pengeditan yang sama lagi: Console memberi Anda catatan yang sama hingga catatan tersebut kedaluwarsa.
* **Check menyatakan bahwa catatan telah kedaluwarsa:** Catatan berlaku selama 30 hari sejak Console pertama kali menampilkannya. Klik **Get a new record** dan tambahkan catatan baru tersebut.
* **Kotak dialog menampilkan pesan sebagai pengganti catatan:** Pesan tersebut mungkin menyatakan, misalnya, bahwa organisasi Anda sudah memiliki 20 nama domain. Anda tidak dapat melanjutkan sampai hal tersebut diselesaikan. Untuk bantuan, hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support).

### Jika aplikasi tidak disetujui

Anda tidak dapat memublikasikan aplikasi lagi sendiri, dan perubahan tidak memulai peninjauan baru. Untuk meminta peninjauan lain, hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support). Setelah perubahan pada aplikasi aktif ditolak, perubahan tersebut tetap berlaku, dan koneksi baru tetap terbatas pada pengguna uji Anda.

### Saat perubahan sedang ditinjau atau tidak disetujui

Sejak Anda mengirim perubahan aplikasi aktif untuk ditinjau hingga Anthropic menyetujuinya:

* **Koneksi baru:** **Who can link** kembali menjadi **Test users only**. Console menampilkan daftar **Test users** lagi dengan orang-orang yang sebelumnya ada di dalamnya.
* **Pengguna uji:** Anda dapat menambahkan dan menghapus orang.
* **Batas yang sudah ditetapkan:** Organisasi yang tertaut mempertahankan pengaturan batasnya, bahkan di atas $50 USD atau tanpa batas.

Saat peninjauan selesai, salah satu dari hal berikut terjadi:

* **Approved:** Aplikasi aktif kembali. Setiap pelanggan yang memenuhi syarat dapat menautkan, Console menyembunyikan daftar **Test users**, dan aturan batas pengujian berhenti berlaku.
* **Not approved:** Status berubah menjadi **Not approved**, dan aturan ini tetap berlaku.

### Batas atas selama pengujian

Batas atas pengeluaran pelanggan untuk aplikasi Anda membatasi jumlah yang dapat Anda tagihkan kepada mereka setiap bulan. Halaman persetujuan menyebutnya batas pengeluaran bulanan. Aturan ini berlaku untuk orang yang menautkan serta anggota Admin dan Billing pelanggan di Console:

| Pengaturan batas | Saat aplikasi dalam pengujian, dalam peninjauan, atau tidak disetujui | Saat aplikasi aktif |
| ----- | ----- | ----- |
| Batas atas pengeluaran di halaman persetujuan | Wajib, $50 USD atau kurang | Opsional |
| Kolom jumlah di halaman persetujuan | Dimulai dari $50 USD | Dimulai kosong |
| **Continue without a limit** | Tidak ditawarkan | Ditawarkan |
| Menghapus batas di Console | Tidak dapat dilakukan | Dapat dilakukan |
| Batas terbesar yang dapat mereka tetapkan | $50 USD | Tidak ada batas maksimum praktis |

Setelah aplikasi aktif, batas yang disimpan pelanggan saat aplikasi dalam pengujian tetap berlaku. Pelanggan kemudian dapat menaikkan atau menghapusnya. Untuk aturan lain tentang batas, lihat [Batas atas pengeluaran di halaman Apa yang dilihat pelanggan Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps).

### Jika organisasi Anda menggunakan penagihan melalui faktur

Dengan penagihan melalui faktur, Anthropic menagih organisasi Anda melalui faktur untuk penggunaan API-nya, dan organisasi Anda tidak membeli kredit prabayar. Aplikasi Anda tetap dimulai dalam tahap pengujian, dan aturan untuk pengguna uji serta batas tetap berlaku. Setelah itu, ada tiga hal yang berbeda:

* Untuk memublikasikan, klik **Publish app** lalu klik **Publish app** di kotak dialog. Anthropic tidak meninjau aplikasi, sehingga aplikasi aktif segera setelah Anda memublikasikannya.
* Anda tidak perlu membuktikan domain, dan aplikasi tidak memerlukan beranda untuk dipublikasikan. Aturan untuk redirect URI tidak berlaku. Autentikasi klien tetap harus disiapkan terlebih dahulu.
* Perubahan pada aplikasi aktif tersimpan saat Anda mengklik **Save changes** atau saat Anda mengunggah atau menghapus logo. Tidak ada pemeriksaan domain, konfirmasi, atau peninjauan setelahnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kelola pelanggan tertaut" icon="list" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers">
    Lihat penggunaan, periksa apakah pelanggan tertaut, dan batalkan tautan atau tautkan mereka kembali
  </Card>

  <Card title="Gunakan kredensial terpisah untuk setiap pelanggan" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer">
    Batasi kredensial untuk satu pelanggan, untuk produk single-tenant dan sandbox
  </Card>
</CardGroup>
