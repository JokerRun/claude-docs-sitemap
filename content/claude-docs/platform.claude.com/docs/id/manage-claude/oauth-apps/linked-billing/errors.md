---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 72840583a33fdf47c5d6e54ceba1984179f95b664c00459ef1067e884f10da66
---

---
title: Error Linked billing
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors
description: Temukan apa yang harus dilakukan untuk setiap kesalahan yang dapat dikembalikan saat menautkan atau menagih pelanggan, beserta penyebabnya dalam urutan pemeriksaan.
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

Berikut adalah kesalahan yang dikembalikan oleh `auth.claude.com` saat penautan dan oleh Claude API saat penagihan, selain [penyegaran yang gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails).

## Saat penautan

Kesalahan ini tiba di redirect URI Anda atau dari penukaran kode. Koneksi adalah catatan yang mengikat organisasi Claude milik pelanggan ke salah satu [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) Anda. Dalam setiap kasus, tidak ada koneksi yang dibuat. Untuk kesalahan OAuth standar, lihat [Endpoint dan parameter OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#errors).

### `access_denied`

Pertama, periksa aplikasi Anda: penyebab 3 dan 4 adalah tanggung jawab Anda untuk diperbaiki.

Jika bukan itu, beri tahu orang tersebut bahwa penautan tidak selesai, dan jangan berasumsi bahwa mereka menolak. Minta mereka memeriksa akun Claude mana yang mereka gunakan untuk masuk dan peran mereka di organisasi yang ingin mereka tautkan. Agar mereka dapat mencoba lagi, [arahkan mereka untuk menyetujui](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve) dengan “pushed authorization request” (permintaan otorisasi yang didorong) baru.

Untuk penyebab-penyebab ini, redirect URI Anda menerima `error=access_denied` beserta nilai `state` Anda:

1. Orang tersebut mengklik **Cancel** pada layar persetujuan.

2. Halaman persetujuan tidak memiliki organisasi untuk ditawarkan, dan orang tersebut mengklik tombol yang kembali ke aplikasi Anda. Hal itu terjadi ketika:

   * orang tersebut tidak memiliki peran Admin atau Billing di organisasi Claude mana pun
   * satu-satunya organisasi orang tersebut adalah organisasi yang memiliki aplikasi Anda
   * profil pengguna yang Anda kirim sudah ditautkan ke organisasi lain, di mana orang tersebut tidak memiliki peran Admin atau Billing
   * satu-satunya organisasi orang tersebut adalah jenis yang tidak dapat ditautkan: lihat [pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers)

3. Pengaturan **Who can link** aplikasi Anda bertuliskan “only” setelah nama organisasi Anda. Tidak ada yang dapat menautkan aplikasi seperti itu. Pada tab **Settings**-nya, pilih **Any Claude user** dan klik **Save changes**.

4. Aplikasi Anda belum aktif, orang tersebut tidak ada di daftar **Test users**-nya, dan mereka mengklik tombol yang kembali ke aplikasi Anda. [Tambahkan mereka sebagai pengguna uji](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#add-test-users), atau [publikasikan aplikasi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#publish-the-app).

Untuk penyebab-penyebab ini, `error_description` bertuliskan `the user declined the request`, sehingga tidak dapat memberi tahu Anda penyebab mana yang terjadi. Jika sebaliknya bertuliskan `the request cannot be approved for this organization`, organisasi yang dipilih orang tersebut tidak dapat menyetujui aplikasi Anda. Minta mereka memilih organisasi lain.

### `user_profile_already_linked`

Setiap organisasi pelanggan hanya dapat memiliki satu koneksi ke aplikasi Anda pada satu waktu, demikian pula setiap profil Anda. `error_description` menyebutkan mana dari dua penyebab ini yang berlaku:

1. **Organisasi sudah memiliki koneksi**, melalui profil Anda yang lain. Ini adalah penyebab yang umum, dan `error_description` diawali dengan `This organization already has an active connection`. Di [halaman User profiles](https://platform.claude.com/user-profiles) Anda, cari profil lain dari pelanggan ini yang ditampilkan sebagai **Linked**. Anthropic tidak menampilkan organisasi mana yang ditautkan ke sebuah profil, jadi konfirmasikan dengan pelanggan bahwa itu milik mereka.

   * **Anda menemukannya:** Tagih pelanggan melalui profil tersebut, atau [batalkan tautan profil tersebut](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer) dan arahkan pelanggan untuk menyetujui lagi dengan profil yang ditolak.
   * **Tidak ada profil pelanggan ini yang ditautkan:** Orang tersebut mungkin telah memilih organisasi milik pelanggan Anda yang lain. Arahkan mereka untuk menyetujui lagi, dan minta mereka memeriksa organisasi mana yang mereka pilih.

2. **Profil yang Anda kirim sudah memiliki koneksi**, ke organisasi lain. `error_description`-nya diawali dengan `This user profile already has an active connection`. Akhiri koneksi tersebut terlebih dahulu: lihat [Memindahkan pelanggan ke organisasi lain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#move-a-customer-to-another-organization).

Anda tidak dapat menangkap kesalahan ini lebih awal: pushed authorization request berhasil.

Kesalahan ini tiba di salah satu dari dua tempat:

* **Di redirect URI Anda:** Jika orang tersebut kembali ke aplikasi Anda, redirect membawa `error=user_profile_already_linked` beserta nilai `state` Anda. `auth.claude.com` telah meminta mereka menghubungi Anda dengan kode ini.
* **Dari endpoint token:** Penukaran kode mengembalikannya jika koneksi dibuat setelah persetujuan.

Kesalahan ini tidak menyebutkan profil yang memegang koneksi tersebut.

### Tidak ada redirect

Jika orang tersebut kembali ke produk Anda tanpa callback, arahkan mereka untuk menyetujui lagi dengan pushed authorization request baru. Anda tidak mendapatkan callback dan tidak dapat membedakan kasus-kasus ini:

* Orang tersebut menutup halaman persetujuan.
* `request_uri` telah kedaluwarsa. `request_uri` kedaluwarsa 10 menit setelah Anda membuatnya.
* `request_uri` sudah digunakan. Masing-masing hanya berfungsi sekali.

Dalam dua kasus terakhir, halaman persetujuan menampilkan kesalahan dan tidak mengirim browser kembali ke aplikasi Anda.

### `unauthorized_client` dari penukaran kode

Periksa penyiapan aplikasi Anda di Claude Console, perbaiki yang kurang, dan tukarkan kode yang sama lagi. Penolakan ini tidak menghabiskan kode, yang berlaku selama 5 menit.

| Pemeriksaan | `error_description` | Perbaikan |
| ----- | ----- | ----- |
| Aplikasi memiliki akun layanan operator | `the client is not registered for this grant` | [Pilih akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) |
| Aplikasi memiliki workspace default yang tidak diarsipkan | Menyebutkan masalah workspace | [Pilih workspace default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace) |
| Akun layanan operator adalah anggota workspace tersebut | Menyebutkan masalah workspace | [Pilih workspace](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace) yang akunnya menjadi anggota, seperti workspace bawaan bernama **Default** |

Perubahan yang disimpan dapat memerlukan beberapa menit untuk mencapai `auth.claude.com`, jadi jika penukaran ditolak lagi, tunggu dan coba lagi. Jika kode kedaluwarsa lebih dulu, arahkan pelanggan untuk menyetujui lagi.

Jika Console menyatakan bahwa akun layanan tidak ada lagi, lihat [Jika Anda mengubah akun layanan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-change-the-service-account). Untuk penyebab lainnya, hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) atau tim akun Anthropic Anda jika Anda memilikinya.

## Saat penagihan

Permintaan yang ditolak Claude API sebelum Claude memulai balasan tidak menagih siapa pun. Lokasi detail kesalahan bergantung pada endpoint:

| Endpoint | Lokasi kode kesalahan | Header ID permintaan |
| ----- | ----- | ----- |
| `/v1/messages` | `error.details.error_code` | `request-id` |
| `/v1/chat/completions` | Tidak dikirim | `x-request-id` |

Pada `/v1/chat/completions`, kesalahan memiliki bentuk lain:

* `error.type` adalah `invalid_request_error`.
* `error.code` berisi jenis kesalahan, seperti `billing_error`, bukan salah satu kode kesalahan di judul halaman ini.

Cocokkan berdasarkan status HTTP dan `error.code`. Dua kesalahan `402` terlihat serupa di sana, begitu pula kesalahan `403`, jadi ikuti setiap entri yang sesuai. `401` untuk token akses memiliki bentuk `/v1/messages` dan header `request-id` pada kedua endpoint.

Penolakan pada `/v1/messages` memiliki bentuk ini:

```json
{
  "type": "error",
  "error": {
    "type": "billing_error",
    "message": "...",
    "details": {
      "error_code": "linked_organization_spend_limit_reached"
    }
  }
}
```

Kesalahan `401` dan `503` di bagian selanjutnya halaman ini tidak memiliki kode kesalahan. Pada `/v1/messages`, cocokkan berdasarkan status dan `error.type`.

Di Anthropic SDK, tangkap kelas kesalahan untuk status HTTP, lalu baca kode kesalahan dari `error_code` (typescript: `errorCode`; csharp: `ErrorCode`; go: `ErrorCode()`; java: `errorCode()`; php: `getErrorCode()`)-nya. Kelas untuk `402` adalah `PaymentRequiredError` (ruby: `Anthropic::Errors::PaymentRequiredError`; java, php: `PaymentRequiredException`; csharp: `AnthropicPaymentRequiredException`; go: `*anthropic.Error`), dan kelas untuk `403` adalah `PermissionDeniedError` (ruby: `Anthropic::Errors::PermissionDeniedError`; java, php: `PermissionDeniedException`; csharp: `AnthropicForbiddenException`; go: `*anthropic.Error`).

Di luar Go, setiap kelas mencakup setiap kesalahan dengan statusnya. Go memiliki satu tipe, `*anthropic.Error`, untuk setiap status: periksa `StatusCode`-nya. Satu kode juga dapat tiba di dalam balasan yang di-stream: lihat [`linked_organization_billing_unavailable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#linked-organization-billing-unavailable).

Catat seluruh `error.message` dan ID permintaan dari setiap permintaan yang ditolak. Untuk melayani pelanggan yang ditolak dengan biaya Anda sendiri, kirim permintaan lagi [sebagai permintaan yang Anda bayar](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#you-pay), dengan `bill_to: "self"` di `billing_policy`. Kirimkan sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) Anda, bukan dengan token akses pelanggan.

Untuk `402` atau `403`, mengirim permintaan yang sama lagi tidak membantu selama penyebabnya masih ada. Detik-detik pertama koneksi baru adalah pengecualian: lihat [`user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized).

Permintaan yang sesuai dengan penyebab kedua kode `403` dapat menerima salah satu kode, misalnya kredensial yang salah untuk pelanggan yang juga belum ditautkan. Tangani kedua kode bersama-sama, dan jika penyebab satu entri tidak menjelaskan penolakan, periksa penyebab entri lainnya.

### 403 `user_profile_billing_not_authorized`

Tidak ada koneksi yang mengizinkan permintaan Anda menagih profil pengguna yang disebutkannya. Respons tidak menyebutkan alasannya. Untuk membedakan penyebab 2 hingga 4, [periksa apakah pelanggan ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status) melalui aplikasi yang Anda harapkan.

Periksa penyebab-penyebab ini secara berurutan:

1. **Permintaan Anda.** Permintaan harus menyebutkan profil pengguna yang ditautkan oleh pelanggan ini. Permintaan juga harus diautentikasi sebagai akun layanan operator dari aplikasi yang mereka gunakan untuk menautkan, atau dengan token akses koneksi tersebut. Akun layanan dari aplikasi Anda yang lain menerima kesalahan ini jika pelanggan belum menautkan melalui aplikasi tersebut. Perbaiki permintaan: koneksi baru tidak membantu.

2. **Pelanggan belum menautkan melalui aplikasi ini.** [Status koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status) bertuliskan `not_connected`. Profil yang hanya ditautkan melalui aplikasi Anda yang lain, seperti [aplikasi uji terpisah](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-run-several-apps), tidak ditautkan ke aplikasi ini. Sampai pelanggan [menautkan melalui aplikasi ini](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve), permintaan hanya dapat menagih Anda, dengan `bill_to: "self"`.

3. **Koneksi telah berakhir.** Status koneksi bertuliskan `disconnected`, dan profil ditampilkan sebagai **Unlinked** di [halaman User profiles](https://platform.claude.com/user-profiles) Anda. `last_revoked_reason.type` dari status tersebut menyebutkan alasannya. Sampai pelanggan [menautkan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again), permintaan hanya dapat menagih Anda, dengan `bill_to: "self"`.

4. **Status koneksi bertuliskan `connected`, dan permintaan tetap ditolak.**

   * **Koneksi baru:** Koneksi baru biasanya langsung berfungsi, tetapi dapat memerlukan sekitar 10 detik setelah penukaran kode. Jika koneksi masih sebaru itu, tunggu hingga sekitar 10 detik berlalu sejak penukaran lalu kirim permintaan sekali lagi.
   * **Token akses dari koneksi sebelumnya:** Token akses pelanggan hanya berfungsi untuk koneksi yang menerbitkannya. Setelah koneksi tersebut berakhir, permintaan dengan token-nya dapat menerima kesalahan ini atau [`401 authentication_error`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#authentication-error), bahkan jika pelanggan telah menautkan lagi. Gunakan token akses dari koneksi baru.
   * **Bukan keduanya:** Kirim ID permintaan yang ditolak ke [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) atau ke tim akun Anthropic Anda jika Anda memilikinya.

### 403 `user_profile_not_billable`

Temukan penyebabnya sebelum Anda meminta pelanggan menautkan lagi, karena menautkan organisasi yang sama lagi hanya dapat memperbaiki penyebab 2.

Periksa penyebab-penyebab ini secara berurutan:

1. **Kredensial permintaan Anda.** Permintaan harus diautentikasi sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) aplikasi Anda atau dengan token akses pelanggan. Kredensial lain apa pun ditolak, seperti kunci API yang tidak terikat ke akun layanan. Begitu pula akun layanan yang tidak mengoperasikan aplikasi OAuth, seperti [operator yang Anda ganti](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-change-the-service-account). Perbaiki permintaan.

2. **Autentikasi khusus operator.** Jika Anda [menonaktifkan autentikasi khusus operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#turn-off-operator-only-authentication), hanya token akses milik pelanggan sendiri yang dapat menagih mereka. Permintaan dari akun layanan Anda saja akan ditolak, meskipun pelanggan ditampilkan sebagai **Linked**.

   * **Anda memegang token akses pelanggan:** Kirim permintaan dengan token tersebut. Jika sudah kedaluwarsa, [segarkan token OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#refresh-the-tokens) terlebih dahulu.
   * **Anda tidak memegang refresh token, atau penyegaran mengembalikan `invalid_grant`:** [Tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

3. **Organisasi pelanggan.** Anda tidak dapat melihat statusnya dari sisi Anda, jadi tanyakan kepada pelanggan bagaimana organisasi mereka membayar penggunaan Claude API.

   * **Tidak memenuhi syarat:** Organisasi harus [membayar Anthropic secara langsung](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers). Beberapa organisasi yang ditagih melalui marketplace cloud dapat menautkan, lalu setiap permintaan yang Anda tagihkan kepada mereka menerima kesalahan ini.
   * **Belum ada penagihan yang disiapkan:** Organisasi baru dapat menautkan sebelum penagihannya disiapkan. Sampai saat itu, organisasi tersebut menerima kesalahan ini, bukan `402` karena kehabisan kredit. Minta pelanggan membeli kredit di [halaman Billing](https://platform.claude.com/settings/billing) mereka lalu kirim permintaan lagi. Pembelian dapat memerlukan waktu untuk diterapkan, jadi jika Anda masih menerima kesalahan ini atau [`linked_organization_spend_limit_reached`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#linked-organization-spend-limit-reached), coba lagi nanti.

4. **Sesuatu yang hanya dapat dilihat Anthropic.** Pelanggan ditampilkan sebagai **Linked**, dan permintaan Anda benar. Kirim ID permintaan yang ditolak ke [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) atau ke tim akun Anthropic Anda jika Anda memilikinya.

### 402 `linked_organization_spend_limit_reached`

Minta seseorang dengan peran Admin atau Billing di pihak pelanggan untuk memeriksa hal-hal berikut di Claude Console. Respons tidak menyebutkan mana yang berlaku:

* **Batas atas pengeluaran mereka untuk aplikasi Anda:** Di halaman aplikasi Anda di bawah [Linked platforms](https://platform.claude.com/linked-platforms), mereka dapat menetapkan atau menaikkannya. Batas yang ditetapkan di sana menggantikan batas default yang mereka tetapkan untuk semua platform tertaut.
* **Batas pengeluaran bulanan organisasi mereka:** Di bawah [Spend limits](https://platform.claude.com/settings/billing#spend-limits), mereka dapat menaikkannya.
* **Saldo kredit mereka:** Di [halaman Billing](https://platform.claude.com/settings/billing) mereka, mereka dapat membeli kredit. Pembelian dapat memerlukan waktu untuk diterapkan, sehingga permintaan segera setelahnya masih dapat menerima kesalahan ini. Jika demikian, coba lagi nanti. Beberapa kredit tidak dapat membayar permintaan ini: lihat [Kredit mana yang dapat membayar](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#which-credits-can-pay). Oleh karena itu, saldo di atas $0 USD masih dapat menerima kesalahan ini.

Selama aplikasi Anda belum aktif, batas tidak dapat melebihi $50 USD. Penolakan pada $50 USD kemudian berlangsung hingga bulan berikutnya dimulai (UTC): lihat [Batas atas selama pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing).

Organisasi yang sudah menyiapkan penagihan tetapi tidak memiliki kredit menerima kode ini. Organisasi yang penagihannya belum disiapkan menerima [`user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-not-billable).

### 402 `linked_organization_billing_unavailable`

Apa yang harus dilakukan bergantung pada kapan kesalahan tiba:

* **Sebelum balasan dimulai:** Anthropic tidak dapat menagih organisasi pelanggan, misalnya karena organisasi tersebut ditangguhkan. Respons tidak menyebutkan alasannya. Minta pelanggan memeriksa akun Claude mereka dan status penagihan mereka dengan Anthropic.
* **Setelah Claude memulai balasan:** Biasanya, kredit organisasi habis, meskipun penangguhan juga dapat memotong balasan. Minta pelanggan membeli kredit di [halaman Billing](https://platform.claude.com/settings/billing) mereka atau memeriksa akun mereka.

Permintaan yang tidak di-stream menerima HTTP `402` dalam kedua kasus, jadi ikuti keduanya. Pelanggan yang tidak memiliki kredit saat permintaan tiba akan menerima [`linked_organization_spend_limit_reached`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#linked-organization-spend-limit-reached) sebagai gantinya.

Pada balasan yang di-stream, status HTTP sudah `200` ketika balasan terpotong, dan kesalahan tiba di dalam stream:

* **Pada `/v1/messages`:** Sebagai event `error` yang `error.type`-nya adalah `billing_error` dan `error.details.error_code`-nya adalah kode ini. Kelas SDK untuk `402` tidak menangkapnya.
* **Pada `/v1/chat/completions`:** Sebagai baris `data:` terakhir yang berisi objek kesalahan OpenAI, dengan `billing_error` di `error.code` dan tanpa `[DONE]` setelahnya.

Tidak ada yang membayar balasan yang terpotong. Jika permintaan sudah menyelesaikan sebuah langkah, seperti giliran Claude sebelum pencarian web, pelanggan membayar langkah tersebut.

### 400 `user_profile_required`

Kirim ID profil pengguna pelanggan di header `anthropic-user-profile-id`. Permintaan menetapkan `bill_to: "user_profile"` tanpa header tersebut. Permintaan dengan [token akses pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#call-claude-with-a-token) tidak memerlukan header tersebut.

### 401 `authentication_error`

Kirim permintaan lagi dengan token akses terbaru pelanggan, atau [segarkan token OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#refresh-the-tokens). [Tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again) hanya jika profil mereka ditampilkan sebagai **Unlinked**, Anda tidak memegang refresh token untuk mereka, atau penyegaran mengembalikan `invalid_grant`.

Entri ini mencakup permintaan dengan token akses pelanggan yang tidak lagi berfungsi: token tersebut kedaluwarsa, digantikan oleh penyegaran, atau dicabut. Penyegaran juga mencabut token sebelumnya, jadi “revoked” di `error.message` saja tidak berarti bahwa koneksi telah berakhir. Setelah koneksi berakhir, setiap permintaan dengan token-nya dapat menerima kesalahan ini atau [`403 user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized), tanpa urutan yang tetap.

### 429 `enforced_spend_limit_reached`

[Minta batas atas pengeluaran bulanan yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits) untuk organisasi Anda, atau tunggu hingga bulan berikutnya dimulai (UTC). Mengirim permintaan lagi tidak membantu, bahkan sebagai permintaan yang Anda bayar.

Organisasi Anda telah mencapai batas atas pengeluaran bulanan untuk tingkat penggunaan Anda. Batas atas pengeluaran pelanggan untuk aplikasi Anda bukan penyebabnya, sehingga pelanggan tidak dapat memperbaikinya. Lihat [Mencapai batas pengeluaran Anda](https://platform.claude.com/docs/id/api/rate-limits#reaching-your-spend-cap).

### 503 `overloaded_error`

Coba lagi dengan backoff. Jika respons memiliki header `retry-after`, tunggu setidaknya selama itu. Claude API tidak dapat mengonfirmasi apakah dapat menagih pelanggan, sehingga tidak melayani atau menagih permintaan tersebut.

### Kesalahan lain tanpa kode

| Status dan jenis | Penyebab | Perbaikan |
| ----- | ----- | ----- |
| `400 invalid_request_error` | Header `anthropic-user-profile-id` berisi ID yang salah format atau bukan salah satu profil pengguna organisasi Anda | Kirim ID profil pengguna pelanggan |
| `400 invalid_request_error` | Permintaan mengirim `billing_policy` tanpa beta header `user-profiles-billing-2026-10-01` | Tambahkan beta header |
| `400 invalid_request_error` | `billing_policy` memiliki field yang hilang atau tidak valid | Perbaiki `billing_policy` |
| `400 invalid_request_error` | Permintaan menagih pelanggan dan menggunakan [fitur eksekusi kode yang dapat ditagih](https://platform.claude.com/docs/id/about-claude/pricing#code-execution-tool) | Kirimkan sebagai akun layanan operator Anda, ditagihkan kepada Anda |
| `invalid_request_error` dalam hasil batch `errored` | Permintaan dalam batch menagih pelanggan: lihat [Jika Anda menggunakan Message Batches](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#if-you-use-message-batches) | Kirimkan dengan penagihan kepada Anda |
| `400 invalid_request_error` | Permintaan menggunakan token akses pelanggan dan menetapkan `bill_to: "self"` | Kirim permintaan yang Anda bayar sebagai akun layanan operator Anda |
| `400 invalid_request_error` | Permintaan menggunakan token akses pelanggan dan menyebutkan profil pengguna lain | Sebutkan hanya profil pelanggan tersebut |
| `403 permission_error` | Permintaan menggunakan token akses pelanggan pada endpoint yang tidak menerimanya, seperti [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing) | Kirimkan sebagai akun layanan operator Anda |
| `403 permission_error` | Anthropic tidak menagih organisasi Anda secara langsung, sehingga tidak dapat menagih pelanggan atas nama Anda | Tagih pelanggan dari organisasi yang membayar Anthropic secara langsung |
