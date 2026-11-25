---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: deb039a67214c8676cff3f813538bede61e95aa45a0ee09d77ceee0e35a9e628
---

---
title: Siapkan aplikasi Anda untuk Linked billing
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app
description: Daftarkan produk Anda sebagai aplikasi OAuth di Claude Console dan berikan back end Anda identitas yang dapat menagih pelanggan Anda dengan Linked billing.
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

Dengan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing), pelanggan Anda membayar penggunaan Claude di produk Anda melalui organisasi Claude mereka sendiri. Sebelum pelanggan mana pun dapat menautkan, Anda menyiapkan aplikasi Anda satu kali di Claude Console.

Setelah selesai, aplikasi Anda memiliki client ID, [autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication), [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account), dan [workspace default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace). Anda juga telah memilih [apakah akan mendapatkan refresh token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#choose-whether-to-get-refresh-tokens). Bagian akhir halaman ini membahas perubahan pada aplikasi yang sudah digunakan pelanggan.

## Sebelum Anda memulai

* **Peran Admin:** Anda memerlukan peran Admin di organisasi Claude Anda untuk setiap langkah di halaman ini.
* **Penyedia identitas untuk back end Anda:** Back end Anda membuktikan identitasnya dengan token berumur pendek dari penyedia identitas Anda sendiri, melalui “Workload Identity Federation” (federasi identitas beban kerja).
* **Organisasi yang ditagih langsung oleh Anthropic:** Organisasi Anda harus membayar Anthropic secara langsung untuk penggunaan API-nya, melalui kredit prabayar atau penagihan berbasis faktur. Organisasi yang ditagih melalui marketplace cloud tidak dapat menagih pelanggan dengan cara ini.

Jika penyedia identitas Anda tidak termasuk dalam [penyedia identitas](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers), Anda dapat mendaftarkan penyedia OpenID Connect apa pun sebagai [federation issuer](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#federation-issuers).

## Buat aplikasi

Aplikasi adalah pendaftaran produk Anda di Anthropic. Aplikasi ini mengaitkan redirect URI Anda, yaitu alamat di produk Anda yang menerima browser setelah pelanggan memberikan persetujuan, dengan client ID.

1. Di halaman [OAuth apps](https://platform.claude.com/settings/oauth-apps) di Console, klik **Create**.

2. Masukkan nama aplikasi dan redirect URI Anda.

   * **Nama:** Pelanggan melihatnya saat memberikan persetujuan, jadi awali dengan nama produk Anda, seperti “Example Analytics for Claude”. Nama tidak boleh diawali dengan “Claude” atau “Anthropic” atau yang mirip dengannya, dan tidak boleh menempatkan “official” di sebelah salah satunya.
   * **Redirect URI:** Alamat harus mengikuti [aturan redirect URI](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#redirect-uri-rules).

3. Di bawah **What the app can do**, pastikan **Bill and link to organizations** dipilih. Ini memberikan aplikasi scope `billing:attribution`, yang memungkinkannya menagih pelanggan Anda.

4. Pilih kotak centang **I accept Linked Billing Terms on behalf of** organisasi Anda dan klik **Continue**. Ketentuan tersebut adalah [Linked Billing Beta Terms](https://www.anthropic.com/legal/linked-billing-terms).

5. Saat kotak dialog meminta autentikasi klien, klik **Skip for now**. Console membuat aplikasi, dan Anda menyiapkan autentikasi klien di bagian berikutnya. Hingga saat itu, halaman aplikasi memperingatkan bahwa aplikasi tidak dapat melakukan autentikasi.

6. Salin **Client ID** di bagian atas halaman aplikasi. Client ID diawali dengan `clid_`. Setiap permintaan ke `auth.claude.com`, server otorisasi Anthropic, membawanya, termasuk pengalihan yang mengirim pelanggan ke halaman persetujuan. Client ID bersifat publik.

7. Di tab **Appearance**, masukkan halaman beranda Anda dan klik **Save changes**.

8. Unggah logo Anda, berupa file PNG atau JPEG persegi, 256 hingga 2.048 piksel per sisi dan maksimal 2 MB. Logo langsung tersimpan. Tanpa logo, pelanggan melihat inisial aplikasi Anda.

Aplikasi baru dimulai dalam mode pengujian. Hingga aplikasi aktif, hanya orang-orang di daftar **Test users**-nya yang dapat menautkannya: lihat [Publikasikan aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#publish-the-app).

## Siapkan autentikasi klien

Back end Anda membuktikan bahwa permintaan ke `auth.claude.com` berasal dari aplikasi Anda dengan “client assertion” (asersi klien): JWT berumur pendek yang diterbitkan oleh penyedia identitas Anda untuk back end Anda. Anthropic tidak menerbitkan client secret untuk aplikasi OAuth. Untuk menyiapkan autentikasi klien:

1. Pada tab **Client authentication** aplikasi, pilih **Identity provider** Anda, yaitu penerbit yang menandatangani token back end Anda, seperti AWS, Google Cloud, atau Kubernetes. Untuk menambahkannya, klik **Register a new issuer**, isi detailnya, lalu klik **Register**, atau lihat [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation).
2. Atur **Subject pattern** yang harus dicocokkan oleh klaim `sub` pada token back end Anda, atau atur kondisi klaim di bawah **Advanced match options**. `auth.claude.com` menerima token apa pun dari penyedia identitas Anda yang cocok dengan pola atau kondisi tersebut, jadi buatlah sesempit yang dimungkinkan oleh back end Anda. Untuk sintaks pola, lihat [Semantik pencocokan aturan](https://platform.claude.com/docs/id/manage-claude/wif-reference#rule-matching-semantics).
3. Klik **Save**. Tab tersebut kemudian menampilkan **Expected audience**.
4. Pastikan penyedia identitas Anda menerbitkan client assertion untuk back end Anda dengan audiens tersebut secara persis pada klaim `aud`. Jaga agar masa berlakunya singkat, dalam batas [masa berlaku maksimum](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification) penerbit Anda, yaitu 1 jam secara default: siapa pun yang mencegat client assertion dapat menggunakannya hingga kedaluwarsa.

Untuk setiap klaim yang harus dimuat oleh client assertion, lihat [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-assertion-claims).

## Berikan identitas untuk back end Anda

Back end Anda memanggil Claude API sebagai akun layanan, yaitu akun non-manusia di organisasi Claude Anda. Akun yang Anda pilih sebagai operator aplikasi adalah satu-satunya akun yang dapat menagih pelanggan tertaut Anda. Akun ini menagih dengan salah satu dari dua cara:

* Dengan kredensialnya sendiri, dengan menyebutkan [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) pelanggan
* Melalui [token akses OAuth milik pelanggan sendiri](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer), yang dihitung sebagai akun tersebut dan hanya dapat menagih pelanggan itu

### Pilih akun layanan operator

Akun layanan melakukan autentikasi dengan aturan federasinya sendiri, yang terpisah dari autentikasi klien. Autentikasi klien membuktikan bahwa permintaan ke `auth.claude.com` berasal dari aplikasi Anda. Aturan federasi memungkinkan back end Anda memanggil Claude API sebagai akun layanan.

1. [Buat akun layanan dan aturan federasinya](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#set-up-federation).

   * **Akun tersendiri:** Gunakan akun layanan yang bukan operator aplikasi lain, karena setiap aplikasi memerlukan akunnya sendiri.
   * **Scope aturan:** Pertahankan scope default, `workspace:developer`, yang diperlukan back end Anda untuk membuat profil pengguna, memeriksa apakah pelanggan tertaut, dan membatalkan tautan mereka. Jangan tambahkan `org:admin`, yang mencakup seluruh Admin API.
   * **Audiens aturan:** Jika Anda membiarkannya kosong, biasanya nilainya berbeda dari **Expected audience** aplikasi Anda, sehingga Anda memerlukan dua JWT: lihat [saat kedua audiens berbeda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-the-audiences-differ).

2. Di tab **Client authentication** aplikasi, di bawah **Operator service account**, pilih akun layanan dan klik **Save**.

<Warning>
  Setelah pelanggan tertaut, mengubah atau mengarsipkan akun layanan operator dapat menghentikan sebagian atau seluruh penagihan sebagai aplikasi Anda.
</Warning>

Perubahan menghentikan token OAuth pelanggan dari melakukan penagihan, dan pengarsipan menghentikan semua penagihan sebagai aplikasi Anda. Untuk memulihkan dari keduanya, lihat [Jika Anda mengubah akun layanan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-change-the-service-account).

### Pilih workspace default

Permintaan yang menggunakan token akses milik pelanggan sendiri berjalan di satu workspace organisasi Anda, yaitu workspace default aplikasi. Setiap aplikasi baru memerlukannya, meskipun Anda tidak pernah menggunakan token tersebut. Pada langkah terakhir penautan, back end Anda menukar kode sekali pakai dengan koneksi ke organisasi pelanggan. Tanpa workspace default, penukaran tersebut gagal dengan `unauthorized_client`. Penolakan itu tidak menghabiskan kode, sehingga Anda dapat mengatur workspace dan mengirim kode yang sama lagi dalam batas 5 menitnya.

Pengaturan ini muncul setelah akun layanan operator disimpan:

1. Di tab **Client authentication** aplikasi, di bawah akun layanan operator, temukan **Default workspace for platform auth mode OAuth tokens** (pengaturan `connection_token_workspace_id` aplikasi) dan klik **Choose workspace**.
2. Pilih workspace yang tidak diarsipkan dan yang akun layanannya menjadi anggota, lalu klik **Save**. Setiap akun layanan adalah anggota workspace bawaan organisasi Anda yang bernama **Default**, sehingga Anda selalu dapat memilih workspace tersebut.

<Warning>
  Setelah pelanggan tertaut, jangan arsipkan workspace default aplikasi: pengarsipan mencabut setiap token OAuth yang berjalan di dalamnya, dan tindakan ini tidak dapat dibatalkan.
</Warning>

Untuk menggunakan workspace lain, ikuti [Jika Anda pindah ke workspace lain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-move-to-another-workspace).

## Pilih apakah akan mendapatkan refresh token

Setiap koneksi memberi Anda token akses untuk pelanggannya, yang hanya dapat menagih pelanggan tersebut dan kedaluwarsa dalam 1 jam. Refresh token mendapatkan token akses baru tanpa meminta persetujuan pelanggan lagi. Yang menentukan adalah cara back end Anda melakukan penagihan:

* **Hanya dengan kredensial akun layanan operator sendiri:** Biarkan **Offline access** nonaktif.
* **Dengan token akses milik pelanggan sendiri:** Aktifkan **Offline access**. Anda menagih dengan cara ini jika kode yang tidak sepenuhnya Anda kendalikan memanggil Claude untuk pelanggan, seperti agen di dalam sandbox. Anda juga menagih dengan cara ini jika Anda ingin setiap permintaan yang ditagih menggunakan token akses milik pelanggan sendiri.

Untuk mendapatkan refresh token, buka tab **Permissions** aplikasi dan aktifkan **Offline access**, yang memungkinkan Anda meminta scope `offline_access`. Kemudian, mintalah `billing:attribution offline_access` saat Anda [mengirim setiap pelanggan untuk memberikan persetujuan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve). Aktifkan sebelum pelanggan Anda menautkan. Jika Anda mengaktifkannya nanti, setiap pelanggan tertaut harus [memberikan persetujuan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#implementation-details) untuk memberi Anda refresh token. Anda tidak perlu membatalkan tautan mereka terlebih dahulu.

Jika tab **Permissions** juga mencantumkan scope usang `org:billing_attribution`, menghapusnya tidak dapat dibatalkan: lihat [Jika Anda masih menggunakan scope usang](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-still-use-the-deprecated-scope).

## Periksa hasilnya

Di halaman aplikasi di Console, periksa hal-hal berikut:

* Halaman tidak menampilkan peringatan bahwa aplikasi tidak dapat melakukan autentikasi.
* Tab **Client authentication** menampilkan penyedia identitas Anda dan **Expected audience**-nya.
* Tab yang sama menampilkan akun layanan operator Anda dan workspace default aplikasi.
* Tab **Permissions** menampilkan `billing:attribution` dalam keadaan aktif di bawah **Billing**.
* Jika Anda memilih refresh token, tab **Permissions** juga menampilkan **Offline access** dalam keadaan aktif.

Perubahan yang disimpan dapat memerlukan beberapa menit untuk mencapai `auth.claude.com`. Tunggu beberapa menit setelah perubahan terakhir Anda sebelum menautkan pelanggan.

## Putuskan apakah akan menggunakan aplikasi uji terpisah

Aplikasi baru dimulai dalam mode pengujian, sehingga Anda dapat mencoba penautan dengan aplikasi produksi Anda dan pengguna ujinya. Anda juga dapat mendaftarkan aplikasi terpisah untuk pengujian. Setiap aplikasi memiliki koneksi, pengguna uji, status, dan akun layanan operatornya sendiri.

<Warning>
  Pertahankan Linked billing pada satu aplikasi produksi selama Anda menawarkannya: koneksi pelanggan hanya berfungsi dengan aplikasi yang mereka tautkan.
</Warning>

## Aturan dan kasus khusus

Kasus-kasus ini muncul saat Anda mengubah aplikasi yang sudah digunakan pelanggan atau saat aplikasi Anda masih menggunakan scope usang. Dua istilah berulang kali muncul:

* **Memberikan persetujuan lagi:** Kirim pelanggan melalui persetujuan yang sama seperti saat pertama kali mereka menautkan. Gunakan profil pengguna mereka yang sudah ada, dan jangan batalkan tautan mereka terlebih dahulu.
* **Menautkan lagi:** Ikuti [Menautkan pelanggan kembali](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again), yang membahas setiap kasus.

### Jika Anda mengubah scope

Untuk memberi pelanggan tertaut refresh token:

1. Aktifkan **Offline access** di tab **Permissions**.
2. Minta pelanggan memberikan persetujuan lagi, dengan meminta scope `billing:attribution offline_access`.
3. Ganti ID koneksi yang tersimpan dengan yang baru yang dikembalikan oleh penukaran kode.

Jika pushed authorization request meminta scope yang tidak dimiliki aplikasi, `auth.claude.com` menolaknya dengan `invalid_scope`. Server juga menolak permintaan yang dikirim dalam beberapa menit setelah Anda mengubah scope aplikasi, sebelum perubahan mencapainya: tunggu dan kirim lagi.

### Jika Anda mengubah akun layanan

Setelah Anda mengubah atau mengarsipkan akun layanan operator, `auth.claude.com` menolak setiap penyegaran token yang masih berfungsi dengan `unauthorized_client`. Token yang sudah dicabut atau kedaluwarsa mendapatkan `invalid_grant` setelah perubahan dan dapat mendapatkan salah satu dari kedua error setelah pengarsipan.

**Jika Anda mengubahnya:**

| Permintaan | Hasil |
| ----- | ----- |
| Dengan token akses pelanggan yang Anda pegang atau sebagai akun layanan sebelumnya | Berhenti menagih pelanggan tidak lama setelah perubahan |
| Sebagai akun layanan operator baru | Masih dapat menagih pelanggan tertaut Anda kecuali Anda [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#turn-off-operator-only-authentication), yang membuat hanya token akses milik pelanggan sendiri yang dapat menagih |

Untuk memulihkan, pastikan back end Anda melakukan autentikasi sebagai akun layanan operator baru. Akun tersebut harus menjadi anggota workspace default aplikasi. Kemudian, tautkan lagi setiap pelanggan yang tokennya Anda gunakan. Pelanggan yang hanya Anda tagih sebagai akun layanan operator tidak memerlukan tindakan lain.

**Jika Anda mengarsipkannya:** Tidak ada yang dapat menagih sebagai aplikasi Anda, dan `auth.claude.com` menolak setiap penukaran kode, hingga aplikasi memiliki akun layanan operator baru. Console menyatakan bahwa akun layanan tersebut tidak ada lagi dan menampilkan tombol **Delete app**, tetapi Anda tidak perlu menghapus aplikasi. Jika workspace default aplikasi juga diarsipkan, Console tidak dapat memilih akun layanan baru: hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support).

Seseorang dengan peran Admin atau Billing di setiap pelanggan harus menautkan lagi, jadi sepakati waktunya dengan mereka terlebih dahulu. Kemudian:

1. [Batalkan tautan setiap pelanggan tertaut di Console](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer). Endpoint pembatalan tautan tidak dapat melakukan ini, karena memerlukan akun yang telah diarsipkan.
2. Buat [akun layanan operator lain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) beserta aturan federasinya. Akun tersebut harus menjadi anggota workspace default aplikasi.
3. Di tab **Client authentication** aplikasi, klik **Change** di bawah **Operator service account**. Pilih akun layanan baru dan klik **Change service account**.
4. Pastikan back end Anda melakukan autentikasi sebagai akun layanan baru, dan tunggu beberapa menit.
5. Minta setiap pelanggan menautkan lagi dengan profil pengguna mereka yang sudah ada, lalu simpan ID koneksi dan token OAuth baru untuk menggantikan yang sebelumnya.

### Jika Anda pindah ke workspace lain

Permintaan dengan token akses milik pelanggan sendiri berjalan di workspace default aplikasi. Untuk pindah ke workspace lain, ikuti langkah-langkah ini secara berurutan. Jangan arsipkan workspace sebelumnya sebelum langkah 6: pengarsipan mencabut token OAuth pelanggannya.

1. Pastikan akun layanan operator adalah anggota workspace baru.
2. Di tab **Client authentication** aplikasi, klik **Change workspace**, pilih workspace baru, dan klik **Save**.
3. Tunggu beberapa menit hingga perubahan mencapai `auth.claude.com`. Penyegaran selama masa tunggu dapat mengembalikan token yang masih berjalan di workspace sebelumnya.
4. Segarkan token OAuth setiap pelanggan yang memiliki refresh token.
5. Minta setiap pelanggan tanpa refresh token memberikan persetujuan lagi dengan scope yang sama.
6. Jika Anda tidak lagi memerlukan workspace sebelumnya, arsipkan.

Jika Anda mengarsipkan workspace sebelumnya terlalu cepat, segera hentikan penyegaran untuk pelanggannya. Yang terjadi selanjutnya:

| Kapan | Pelanggan dengan refresh token | Pelanggan tanpa refresh token |
| ----- | ----- | ----- |
| Sebelum Anda memilih workspace default baru | Penyegaran mendapatkan `invalid_grant` | Token akses berhenti berfungsi dalam beberapa menit |
| Setelah Anda memilihnya | Penyegaran mengakhiri koneksi | Tetap tertaut |

Setelah Anda memilih workspace default baru, tautkan lagi setiap pelanggan yang memiliki refresh token, dan minta setiap pelanggan tanpa refresh token memberikan persetujuan lagi.

### Jika Anda masih menggunakan scope usang

Aplikasi yang dibuat sebelum `billing:attribution` ada dapat memiliki scope usang `org:billing_attribution`. Pelanggan yang hanya menyetujui scope tersebut tidak mendapatkan token miliknya sendiri, sehingga Anda hanya menagih mereka sebagai akun layanan operator:

* Penukaran kode mengembalikan `access_token`, tetapi itu bukan token akses milik pelanggan sendiri. Jangan gunakan sebagai token akses pelanggan.
* Penagihan mereka berhenti saat koneksi mereka berakhir atau saat Anda [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#turn-off-operator-only-authentication).

Dua aturan berlaku untuk scope usang:

* **Kirim secara terpisah:** Dengan `billing:attribution` atau `offline_access`, pushed authorization request mendapatkan `invalid_scope`.
* **Menghapusnya bersifat final:** Jika Anda menghapus `org:billing_attribution` di tab **Permissions**, Anda tidak dapat menambahkannya kembali.

Untuk memberi pelanggan seperti itu token miliknya sendiri:

1. Di tab **Permissions** aplikasi, aktifkan `billing:attribution` di bawah **Billing** dan aktifkan **Offline access**.
2. Pastikan aplikasi memiliki [workspace default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace).
3. Minta pelanggan memberikan persetujuan lagi, dengan meminta `billing:attribution offline_access`.

## Langkah selanjutnya

<CardGroup cols={1}>
  <Card title="Tombol Link your Claude organization" icon="link" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-button">
    Tombol yang mengirim pelanggan dari produk Anda untuk menyetujui aplikasi Anda
  </Card>
</CardGroup>
