---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 572ee501e9969949f4c32fe67efd59c9b8fde40da2385b7c297ae873f50b54a3
---

---
title: Apa yang dilihat pelanggan Anda
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see
description: "Jelaskan Linked billing kepada pelanggan Anda: halaman persetujuan, batas atas pengeluaran mereka untuk aplikasi Anda, cara koneksi berakhir, dan email yang mereka terima."
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

Dengan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing), pelanggan Anda menyetujui aplikasi Anda, menetapkan [batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps) apa pun untuknya, dan membatalkan tautannya di halaman Anthropic, bukan di produk Anda. Anthropic juga mengirimi mereka email. Tim produk dan dukungan Anda dapat menggunakan halaman ini untuk menjelaskan Linked billing kepada pelanggan. Engineer Anda dapat menggunakannya untuk merencanakan hal-hal yang tidak dapat dilihat oleh aplikasi Anda.

## Cara kerjanya

Misalnya, seorang Admin di Acme menyetujui aplikasi Anda di halaman persetujuan Claude dan menetapkan “spend cap” (batas atas pengeluaran) bulanan sebesar $200 USD untuknya. Kemudian, Acme dapat mengubah batas tersebut atau membatalkan tautan aplikasi Anda di halaman [Linked platforms](https://platform.claude.com/linked-platforms) miliknya. Anthropic mengirim email kepada anggota Admin dan Billing Acme ketika koneksi dibuat dan ketika Acme membatalkan tautan aplikasi Anda. Anthropic juga mengirim email kepada mereka ketika pengeluaran mencapai 80 persen dari batas.

### Menyetujui aplikasi Anda

Halaman persetujuan berada di `auth.claude.com`. Halaman ini menggunakan akun Claude mana pun yang sedang masuk di browser dan hanya menawarkan organisasi Claude milik akun tersebut. Orang yang menyetujui memerlukan peran Admin atau Billing di organisasi yang mereka tautkan. Setiap layar menampilkan nama aplikasi Anda dan memiliki tombol **Cancel**:

| Layar | Apa yang dilakukan orang tersebut |
| ----- | ----- |
| **Select an organization** | Memilih organisasi Claude yang akan ditautkan (hanya muncul jika mereka memiliki pilihan) |
| **How billing works** | Membaca bahwa organisasi membayar penggunaan ini dengan tarifnya sendiri dan mengklik **Continue** |
| **Set a monthly spend limit** | Memasukkan batas atas pengeluaran aplikasi Anda dalam dolar AS bulat atau mengklik **Continue without a limit** dan mengonfirmasi |
| Layar terakhir | Meninjau apa yang dapat dilakukan aplikasi Anda, termasuk batasnya, dan mengklik **Link and authorize** |

Pada layar **Set a monthly spend limit**, kolom jumlah dimulai dalam keadaan kosong. **Continue without a limit** tidak menyimpan batas baru. Batas yang sebelumnya disimpan pelanggan untuk aplikasi Anda tetap berlaku. Jika tidak ada, [batas default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps) mereka yang berlaku. Sampai aplikasi Anda aktif, aturan lain berlaku: lihat [Batas atas selama pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing).

Setelah **Link and authorize**, browser kembali ke aplikasi Anda tanpa layar konfirmasi.

Dalam kasus-kasus berikut, persetujuan berlangsung secara berbeda:

* **Akun yang salah sedang masuk:** Misalnya, orang tersebut mungkin masuk dengan akun pribadi, bukan akun kerja. Halaman menampilkan akun mana yang sedang masuk dan memungkinkan orang tersebut beralih. Aplikasi Anda tidak dapat memilih akun: parameter OpenID Connect `prompt=select_account` dan `login_hint` tidak mengubahnya. Halaman juga dapat meminta orang yang sudah masuk untuk masuk lagi.
* **Akun tidak termasuk dalam organisasi Claude Platform mana pun:** Halaman menawarkan **Set up Claude Platform**, yang membuka Claude Console untuk membuat organisasi lalu kembali ke persetujuan. Sampai organisasi tersebut menyiapkan penagihan, permintaan yang ditagihkan kepadanya akan mendapatkan [`user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-not-billable).
* **Orang tersebut tidak memiliki organisasi yang dapat mereka tautkan:** Mereka tidak memiliki peran Admin atau Billing di organisasi Claude mana pun yang [memenuhi syarat untuk ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers), sehingga halaman tidak memiliki organisasi untuk ditawarkan. Jika mereka kembali ke aplikasi Anda, aplikasi menerima error `access_denied`. Untuk penyebab lainnya, lihat [`access_denied` di Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#access-denied).
* **Orang tersebut mengklik Cancel:** Tidak ada koneksi yang dibuat. Saat browser kembali, aplikasi Anda menerima `access_denied`.

### Setelah penautan

Koneksi dimiliki oleh seluruh organisasi Claude pelanggan, bukan oleh orang yang menyetujuinya, sehingga koneksi tetap ada jika orang tersebut keluar. Pelanggan mengelolanya di halaman [Linked platforms](https://platform.claude.com/linked-platforms) di Claude Console mereka. Di sana, anggota dengan peran Admin atau Billing dapat melihat biaya aplikasi Anda bulan ini. Mereka juga dapat menetapkan batas atas pengeluaran untuknya. Untuk membatalkan tautannya, mereka mengklik aplikasi Anda, lalu **Unlink**, dan mengonfirmasi di kotak dialog.

Koneksi berakhir dengan cara-cara berikut, dan beberapa di antaranya mengirim email kepada anggota Admin dan Billing pelanggan:

| Cara koneksi berakhir | Email kepada pelanggan |
| ----- | ----- |
| Pelanggan membatalkan tautan aplikasi Anda | Ya, tanpa menyebutkan siapa yang membatalkan tautannya |
| Back end Anda mengakhiri koneksi melalui API | Ya |
| Admin organisasi Anda membatalkan tautan pelanggan di Console | Tidak |
| Back end Anda [menggunakan ulang refresh token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails) lebih dari 30 detik setelah penggunaan pertamanya | Tidak |
| Anda menghapus pengguna uji yang menyetujuinya dari daftar **Test users** aplikasi Anda | Tidak |
| Pelanggan menyetujui lagi dengan scope lain, yang menggantikan koneksi dengan yang baru, sehingga pelanggan tetap tertaut | Tidak |
| Anda [menghapus aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#delete-the-app), yang mengakhiri setiap koneksi sekaligus | Tidak |

Jika aplikasi Anda masih ada dan tidak ada koneksi baru yang menggantikan koneksi yang berakhir, permintaan yang ditagihkan kepada pelanggan tersebut biasanya ditolak dalam waktu sekitar 10 detik. Error-nya adalah [`user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized). Permintaan dengan token akses dari koneksi yang berakhir dapat menerima [`401 authentication_error`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#authentication-error) sebagai gantinya. Profil mereka menampilkan **Unlinked** di halaman User profiles Anda, dan Anda dapat [menautkan mereka lagi dengan profil yang sama](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

### Batas atas pengeluaran

Batas atas pengeluaran aplikasi Anda adalah jumlah dalam dolar AS yang membatasi apa yang dapat ditagihkan aplikasi Anda kepada pelanggan setiap bulan. Halaman persetujuan menyebutnya monthly spend limit. Dua pengaturan lain mudah tertukar dengannya:

* **Monthly spend limit organisasi:** Ini membatasi seluruh penggunaan organisasi dan ditetapkan di bawah [Spend limits](https://platform.claude.com/settings/billing#spend-limits). Batas aplikasi Anda bisa lebih tinggi darinya.
* **Batas default pelanggan:** Ini berlaku sepenuhnya untuk setiap aplikasi tertaut yang tidak memiliki batasnya sendiri.

Batas aplikasi Anda atau batas organisasi dapat menolak permintaan yang Anda tagihkan kepada pelanggan, dengan error [`linked_organization_spend_limit_reached`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#linked-organization-spend-limit-reached). Begitu pula kurangnya [kredit yang dapat membayar](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#which-credits-can-pay). Error tersebut tidak menyebutkan yang mana. Batas aplikasi Anda bekerja dengan cara ini:

* Penolakan berlangsung hingga pukul 00:00 UTC pada hari pertama bulan berikutnya atau hingga pelanggan menaikkan atau menghapus batasnya.
* Batas menghitung biaya token dan biaya pencarian web dengan harga daftar, sebelum diskon yang dinegosiasikan. Oleh karena itu, tagihan pelanggan dapat berbeda dari yang dihitung oleh batas, dan pelanggan dengan diskon dapat mencapai batas sebelum tagihan mereka mencapainya.
* Permintaan yang melewati batas tetap dilayani, dan permintaan yang sudah berjalan akan selesai. Oleh karena itu, totalnya dapat berakhir di atas batas, dan lebih jauh lagi ketika banyak permintaan berjalan bersamaan.
* Perubahan batas memerlukan sekitar satu menit untuk berlaku. Batas terkecil adalah $0 USD, yang menolak setiap permintaan. Console menerima dolar bulat dan tidak memiliki batas maksimum praktis setelah aplikasi Anda aktif.
* Anthropic mengirim email kepada anggota Admin dan Billing pelanggan pada 80 persen dari batas dan lagi saat mencapai batas, kecuali untuk batas $0 USD.

Di halaman Linked platforms, anggota dengan peran Admin atau Billing mengelola batas:

* **Menetapkan atau mengubah batas aplikasi Anda:** Klik aplikasi Anda, lalu **Set spend cap** atau **Edit spend cap**.
* **Menetapkan batas default:** Di bawah **Default spend cap**, klik **Set default** atau **Edit**.
* **Menghapus batas aplikasi Anda:** Klik aplikasi Anda, **Edit spend cap**, lalu **Remove cap**. Aplikasi Anda kemudian menggunakan batas default atau tidak memiliki batas.

### Email

Anthropic mengirim email kepada pelanggan pada waktu-waktu berikut:

* Ketika penautan selesai
* Ketika koneksi berakhir dengan salah satu [cara yang mengirim email](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#after-linking)
* Pada [80 persen dari batas dan saat mencapai batas](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps)

Email tentang penautan dan pembatalan tautan menautkan ke halaman Linked platforms pelanggan. Beberapa organisasi tidak menerima email sama sekali. Apakah penautan mengirim email bergantung pada penukaran kode:

| Peristiwa | Email kepada pelanggan |
| ----- | ----- |
| Back end Anda menukarkan kode setelah pelanggan menyetujui | Ya |
| Pelanggan menyetujui, tetapi back end Anda tidak pernah menukarkan kode | Tidak |
| Pelanggan menyetujui lagi saat masih tertaut | Tidak |

## Tentukan cara menjaga pelanggan tetap mendapat informasi

Aplikasi Anda tidak dapat melihat sebagian dari apa yang dilihat pelanggan, jadi rencanakan apa yang disampaikan produk Anda kepada mereka:

* **Pembatalan tautan:** Anthropic tidak memberi tahu Anda ketika pelanggan membatalkan tautan: Anda tidak mendapatkan event webhook maupun email. [Tentukan seberapa sering memeriksa](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#decide-how-often-to-check-link-status) apakah pelanggan masih tertaut.
* **Batas:** Anda tidak dapat melihat batas pelanggan atau berapa banyak yang telah mereka gunakan. Ketika permintaan ditolak dengan `linked_organization_spend_limit_reached`, minta pelanggan untuk memeriksa batas mereka untuk aplikasi Anda, **Monthly spend limit** organisasi mereka, dan kredit mereka.
* **Email:** Anthropic tidak menjamin bahwa email dikirim atau diterima. Beri tahu pelanggan sendiri setiap kali Anda membatalkan tautan mereka, dan jangan mengandalkan email untuk memberi tahu mereka bahwa mereka sudah tertaut.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Tombol Link your Claude organization" icon="code" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-button">
    HTML, CSS, warna, dan logo tombol
  </Card>

  <Card title="Tautkan dan tagih pelanggan" icon="link" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer">
    Tautkan pelanggan dan tagihkan permintaan kepada mereka, dimulai dengan pelanggan uji
  </Card>
</CardGroup>
