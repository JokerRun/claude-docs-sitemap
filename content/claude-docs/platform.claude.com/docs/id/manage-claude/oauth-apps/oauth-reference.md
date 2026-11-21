---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference
fetched_at: 2026-11-21T02:12:50.066053Z
sha256: 1a4ac8bbfe18a1292f484e07c508af56f823309dab4cb1ca0b7c00c729b543a3
---

---
title: Referensi OAuth
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference
description: Endpoint, autentikasi klien, parameter permintaan, scope, respons token, pencabutan, masa berlaku, aturan URI pengalihan, dan error.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Halaman ini mengumpulkan endpoint, parameter, aturan validasi, dan pemetaan error untuk [Claude Platform OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview). Untuk panduan langkah demi langkah, lihat [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections).

## Endpoint

| Endpoint | URL |
| ----- | ----- |
| Endpoint otorisasi (halaman masuk dan persetujuan) | `https://auth.claude.com/oauth/authorize` |
| Endpoint “pushed authorization request” (permintaan otorisasi yang didorong), atau PAR | `https://auth.claude.com/v1/oauth/par` |
| Endpoint token | `https://auth.claude.com/v1/oauth/token` |
| Endpoint pencabutan | `https://auth.claude.com/v1/oauth/revoke` |
| Claude API (profil pengguna dan permintaan yang menagih pelanggan) | `https://api.anthropic.com` |

## Autentikasi klien

`auth.claude.com` mengautentikasi aplikasi Anda dengan metode `private_key_jwt` ([RFC 7523](https://www.rfc-editor.org/rfc/rfc7523)). Kirim parameter-parameter ini pada setiap permintaan ke endpoint PAR, endpoint token, dan endpoint pencabutan. Jangan pernah mengirim kredensial dalam query string URL: `auth.claude.com` akan menolaknya.

| Parameter | Nilai |
| ----- | ----- |
| `client_id` | ID klien aplikasi OAuth Anda |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` |
| `client_assertion` | JWT dari penyedia identitas Anda dengan klaim dalam [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-assertion-claims) |

### Klaim client assertion

“Client assertion” (asersi klien) harus berisi semua klaim berikut, dan header-nya harus berisi `kid` dari sebuah kunci dalam JWKS Anda.

| Klaim | Persyaratan |
| ----- | ----- |
| `iss` | URL issuer penyedia identitas Anda, persis seperti yang didaftarkan melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) |
| `sub` | Nilai yang cocok dengan pola subjek dalam pengaturan autentikasi klien aplikasi Anda, jika Anda menetapkannya |
| `aud` | Tepat satu audiens: nilai dalam pengaturan autentikasi klien aplikasi Anda. `auth.claude.com` menolak asersi yang mencantumkan lebih dari satu audiens. |
| `iat` | Waktu penyedia identitas Anda menerbitkan JWT |
| `exp` | Waktu kedaluwarsa, tidak lebih dari 1 jam setelah `iat`. Gunakan masa berlaku yang lebih singkat jika memungkinkan: siapa pun yang mencegat asersi dapat menggunakannya hingga kedaluwarsa. |

Contoh payload asersi:

```json
{
  "iss": "https://idp.example.com",
  "sub": "workload:prod:claude-integration-backend",
  "aud": "YOUR_CONFIGURED_AUDIENCE",
  "iat": 1791230000,
  "exp": 1791230300
}
```

Buat pola subjek dan kondisi klaim sesempit yang dimungkinkan oleh back end Anda. `auth.claude.com` menerima JWT apa pun dari penyedia identitas Anda yang cocok dengan keduanya sebagai autentikasi untuk aplikasi Anda.

## Parameter permintaan otorisasi

Semua parameter ini wajib. Kirim semua parameter kecuali `request_uri` dalam body JSON dari pushed authorization request.

| Parameter | Deskripsi |
| ----- | ----- |
| `response_type` | Nilai `code` |
| `client_id` | ID klien aplikasi OAuth Anda |
| `redirect_uri` | URI yang persis cocok dengan URI pengalihan yang terdaftar, hingga 2.048 karakter |
| `scope` | `billing:attribution` atau `billing:attribution offline_access`. Lihat [scope penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#scopes). |
| `state` | Nilai acak sekali pakai, hingga 2.048 karakter, yang Anda periksa pada callback |
| `code_challenge` | `BASE64URL(SHA256(code_verifier))`, dengan `code_verifier` sepanjang 43 hingga 128 karakter |
| `code_challenge_method` | Nilai `S256` |
| `connection_type` | Nilai `organization_shared`. Administrator menyetujui koneksi atas nama seluruh organisasi. |
| `connection_auth_target` | Nilai `platform`. Permintaan koneksi diarahkan ke pemilik aplikasi OAuth. |
| `user_profile_id` | ID profil pengguna aktif di organisasi Anda yang mewakili pelanggan |
| `request_uri` | Nilai yang dikembalikan oleh endpoint PAR. Kirimkan ke endpoint otorisasi bersama `client_id` dan tanpa parameter lain. |

Endpoint PAR mengembalikan HTTP 201 dengan `request_uri` dan `expires_in` (600 detik).

## Scope

Minta scope berikut dalam parameter `scope`.

| Scope | Deskripsi |
| ----- | ----- |
| `offline_access` | Memberikan aplikasi refresh token yang mewakili scope lain yang diminta. Pada koneksi penagihan, kirimkan hanya bersama dengan `billing:attribution`. |
| `billing:attribution` | Koneksi yang memungkinkan Anda menagihkan permintaan Claude API yang diarahkan pelanggan untuk Anda buat ke organisasi Claude mereka. Kirimkan sendiri, atau bersama dengan `offline_access` untuk juga mendapatkan refresh token. Lihat [Token OAuth untuk koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#oauth-tokens-for-a-billing-connection). |
| `org:billing_attribution` | Tidak digunakan lagi: gunakan `billing:attribution`. |

## Permintaan token

Kirim permintaan token ke `https://auth.claude.com/v1/oauth/token` dengan body JSON.

| Parameter | Nilai |
| ----- | ----- |
| `grant_type` | `authorization_code` |
| `code` | Kode dari callback |
| `redirect_uri` | `redirect_uri` yang sama dengan yang Anda kirim dalam permintaan otorisasi |
| `code_verifier` | Code verifier PKCE |
| `client_id`, `client_assertion_type`, `client_assertion` | Seperti dalam [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-authentication) |

Untuk melakukan refresh, kirim `grant_type` yang diatur ke `refresh_token`, `refresh_token` Anda, dan parameter dalam [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-authentication).

## Token OAuth untuk koneksi penagihan

Endpoint token mengembalikan token akses koneksi. Token tersebut melakukan autentikasi sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#terms) aplikasi Anda di workspace yang disebutkan oleh pengaturan `connection_token_workspace_id` aplikasi. Pada `/v1/messages` dan `/v1/chat/completions`, permintaan dengan token akses tersebut ditagihkan ke pelanggan koneksi tersebut dan tidak ke pihak lain. Jika pelanggan juga menyetujui `offline_access`, endpoint token juga mengembalikan refresh token, dan grant `refresh_token` memperbarui kedua token. Untuk penyiapan dan panduan langkah demi langkah, lihat [Token OAuth untuk setiap koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#oauth-tokens-for-each-connection) di halaman Linked billing.

Kedua grant menggunakan parameter dalam [Permintaan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#token-request-and-response) dan [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-authentication). Refresh tidak boleh mengirim parameter `scope`. Respons token berisi field-field berikut:

| Field respons | Nilai |
| ----- | ----- |
| `access_token` | Token akses koneksi |
| `token_type` | `Bearer` |
| `expires_in` | Detik hingga token akses kedaluwarsa, paling lama `3600` |
| `scope` | Selalu `workspace:inference` |
| `connection_id` | ID koneksi, misalnya `ocon_EXAMPLE`. Simpan ID ini. Hanya grant `authorization_code` yang mengembalikannya. |
| `refresh_token` | Refresh token koneksi. Dikembalikan hanya jika pelanggan menyetujui `offline_access`. |
| `refresh_token_expires_in` | Detik hingga `refresh_token` kedaluwarsa. Tidak ada jika tidak ada `refresh_token`. |

Setiap refresh mengembalikan `access_token` baru dan `refresh_token` baru. Refresh token yang Anda kirim digantikan, dan token akses sebelumnya berhenti berfungsi dalam beberapa menit. Anda dapat mengirim refresh token yang telah digantikan satu kali lagi, dalam 30 detik setelah refresh yang menggantikannya, untuk mengulangi permintaan yang responsnya hilang. Permintaan kedua tersebut mengembalikan pasangan baru lainnya dan mencabut pasangan dari respons yang hilang: gunakan hanya pasangan terbaru. Permintaan ketiga dengan token yang telah digantikan akan mendapatkan `invalid_grant`, demikian juga permintaan kedua yang tiba setelah 30 detik tersebut. Dalam 30 detik tersebut, permintaan semacam itu tidak mencabut apa pun. Setelah 30 detik tersebut, permintaan itu mencabut setiap token koneksi dan mengakhiri koneksi. [Segarkan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#refresh-the-connection) menjelaskan aturan dan error dari refresh.

Setiap peristiwa berikut mencabut token koneksi, termasuk token akses saat ini:

* Pelanggan atau Anda membatalkan tautan.
* Pelanggan menyetujui permintaan otorisasi baru dengan scope berbeda untuk profil pengguna yang sama, dan Anda menukarkan kode dari persetujuan tersebut. Koneksi baru menggantikan koneksi sebelumnya.
* Workspace tempat token berjalan diarsipkan.

Untuk cara Claude API menagih permintaan dengan token akses koneksi, lihat [Panggil Claude dengan token akses koneksi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#call-claude-with-a-connections-access-token).

## Pencabutan

Kirim permintaan pencabutan ke `https://auth.claude.com/v1/oauth/revoke` dengan body JSON atau form-encoded. Endpoint ini mengikuti [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009) dan juga menerima ID koneksi dan ID profil pengguna.

Kirim parameter dalam [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#client-authentication) dan tepat satu parameter dari tabel ini. `aud` dari client assertion adalah nilai dalam pengaturan autentikasi klien aplikasi Anda, bukan URL pencabutan.

| Parameter | Apa yang diakhirinya |
| ----- | ----- |
| `connection_id` | Salah satu koneksi aplikasi Anda, diberikan sebagai ID `ocon_` |
| `user_profile_id` | Semua koneksi aplikasi Anda pada satu profil pengguna, diberikan sebagai ID `uprof_` |
| `token` | Koneksi tempat token akses atau refresh token tersebut berada, dan semua token koneksi tersebut |

Token akses dari koneksi yang disetujui dengan scope `org:billing_attribution` yang sudah tidak digunakan lagi merupakan pengecualian: mengirimnya hanya mengakhiri token tersebut. Untuk mengakhiri koneksi tersebut, kirim `connection_id` atau `user_profile_id`.

`auth.claude.com` menerima `token_type_hint` dan mengabaikannya.

Endpoint mengembalikan HTTP 200 dan ID koneksi yang diakhiri oleh permintaan tersebut:

```json
{
  "revoked_connection_ids": ["ocon_EXAMPLE"]
}
```

Daftar tersebut kosong dalam salah satu kasus berikut, dan respons tidak menyebutkan yang mana:

* Token atau ID tidak dikenal atau milik aplikasi lain.
* Koneksi sudah berakhir.
* Permintaan mengakhiri token tetapi tidak mengakhiri koneksi apa pun.

Setelah koneksi penagihan apa pun berakhir, Claude API menolak permintaan yang menagih pelanggan koneksi tersebut. Untuk responsnya, lihat [Error penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#billing-errors).

Setelah koneksi `billing:attribution` berakhir, token OAuth-nya berhenti berfungsi. Setelah koneksi yang disetujui dengan scope `org:billing_attribution` yang sudah tidak digunakan lagi berakhir, jangan mengandalkan token aksesnya. Token tersebut mungkin langsung berhenti berfungsi, atau tetap berfungsi hingga kedaluwarsa.

## Masa berlaku

| Item | Masa berlaku |
| ----- | ----- |
| `request_uri` dari endpoint PAR | 10 menit, sekali pakai |
| Kode otorisasi | 5 menit, sekali pakai |
| `access_token` | Hingga 1 jam |
| `refresh_token` | Hingga 1 tahun sejak pertukaran kode. Refresh tidak memperpanjangnya. |

Baca `expires_in` dan `refresh_token_expires_in` dari setiap respons alih-alih mengandalkan nilai tetap.

## Aturan URI pengalihan

* Setiap `redirect_uri` harus persis cocok dengan URI yang terdaftar pada aplikasi Anda. `auth.claude.com` tidak menggunakan pencocokan wildcard atau prefiks.
* Setiap URI pengalihan harus menggunakan HTTPS dan tidak boleh berisi fragmen. URI pengembangan lokal pada `localhost`, `127.0.0.1`, atau `[::1]` boleh menggunakan HTTP.
* URI pengembangan lokal yang didaftarkan dengan tanda bintang sebagai port, seperti `http://localhost:*/callback`, cocok dengan port apa pun.
* Anda dapat mendaftarkan hingga 10 URI pengalihan untuk setiap aplikasi.
* `auth.claude.com` mengirim error ke URI pengalihan Anda hanya jika `redirect_uri` cocok dengan URI yang terdaftar. Untuk `redirect_uri` lainnya, `auth.claude.com` tidak mengalihkan browser.

## Error

### Error pada pengalihan

`auth.claude.com` mengembalikan error sebagai parameter query `error`, `error_description`, dan `state` pada URI pengalihan Anda. Ini adalah error OAuth 2.0 standar ([RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)), kecuali `user_profile_already_linked`, yang khusus untuk Anthropic.

| Error | Kapan | Apa yang ditampilkan kepada pengguna Anda |
| ----- | ----- | ----- |
| `access_denied` | Orang tersebut menolak, atau tidak dapat menyetujui permintaan ini. Orang tersebut harus menjadi administrator organisasi Claude. | Jelaskan bahwa koneksi tidak selesai, dan jangan berasumsi bahwa orang tersebut menolak. Ikuti [Redirect URI Anda menerima `error=access_denied`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#access-denied) dalam panduan Linked billing, yang mencantumkan penyebabnya dan apa yang perlu disampaikan kepada orang tersebut. |
| `server_error` | `auth.claude.com` gagal memproses permintaan. | Minta pengguna untuk mencoba lagi. |
| `user_profile_already_linked` | Organisasi pelanggan sudah tertaut ke aplikasi Anda melalui profil pengguna yang berbeda. Setiap organisasi pelanggan dapat memiliki satu koneksi ke aplikasi Anda. `auth.claude.com` sudah meminta administrator untuk menghubungi Anda. | Jelaskan bahwa organisasi mereka sudah tertaut ke aplikasi Anda. |

Jika `request_uri` telah kedaluwarsa atau Anda sudah menggunakannya, `auth.claude.com` menampilkan halaman error dan tidak mengalihkan browser kembali ke aplikasi Anda. Mulai alur lagi dengan pushed authorization request yang baru.

### Error dari endpoint PAR dan token

Endpoint-endpoint ini mengembalikan body JSON dengan `error` dan `error_description`.

| Error | Kapan |
| ----- | ----- |
| `invalid_request` | Parameter wajib tidak ada atau tidak valid, misalnya `state` atau challenge PKCE yang tidak ada, atau `user_profile_id` yang bukan ID profil pengguna aktif di organisasi Anda. |
| `invalid_client` | `auth.claude.com` tidak dapat mengautentikasi aplikasi Anda: ID klien tidak dikenal, atau client assertion gagal diverifikasi. Periksa `iss`, `sub`, dan `aud` dari asersi terhadap pengaturan autentikasi klien aplikasi Anda, dan periksa bahwa penyedia identitas Anda menandatanganinya dengan kunci dalam JWKS Anda. |
| `invalid_scope` | Scope yang diminta tidak diizinkan untuk aplikasi ini. Refresh juga mendapatkan error ini jika mengirim parameter `scope`. Permintaan token apa pun mendapatkan error ini jika `billing:attribution` tidak lagi terdaftar untuk aplikasi Anda. Pada pertukaran kode, `billing:attribution` yang tidak ada menghabiskan kode. |
| `invalid_grant` | Kode telah kedaluwarsa, Anda sudah menggunakannya, atau kode tidak cocok dengan `redirect_uri` atau `code_verifier`. Untuk refresh, refresh token telah kedaluwarsa atau tidak lagi valid: ikuti [Segarkan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#refresh-the-connection). |
| `unauthorized_client` | Aplikasi Anda tidak disiapkan untuk permintaan ini. Periksa terlebih dahulu akun layanan operator aplikasi dan workspace-nya: lihat [Penukaran kode mengembalikan `unauthorized_client`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#code-exchange-unauthorized-client). `error_description` mungkin menyebutkan penyebabnya, misalnya workspace yang tidak ada. Penolakan ini tidak menghabiskan kode dan tidak mencabut refresh token. |
| `user_profile_already_linked` | Dari endpoint token. Profil pengguna telah tertaut ke aplikasi Anda melalui organisasi pelanggan yang berbeda, atau organisasi pelanggan telah tertaut melalui profil pengguna yang berbeda. Tautan tersebut dibuat di antara persetujuan dan permintaan ini. |

Jika `auth.claude.com` menerapkan batas laju pada permintaan atau mengalami gangguan, ia mengembalikan error dalam format berbeda, yang mungkin bukan JSON. Hal yang sama terjadi untuk `grant_type` yang tidak dikenal atau parameter yang lebih panjang dari batasnya. Coba ulang dengan backoff hanya pada respons HTTP 429 dan 5xx. Perlakukan status lainnya sebagai kesalahan dalam permintaan. Untuk refresh, ikuti [Segarkan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#refresh-the-connection) alih-alih backoff umum. Jika respons memiliki header `retry-after`, tunggu setidaknya selama waktu tersebut. Kirim permintaan berikutnya dari kode Anda sendiri. Jangan mengandalkan percobaan ulang otomatis dari library klien HTTP: percobaan ulang tersebut mungkin tidak berjalan untuk respons semacam itu. [Segarkan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#refresh-the-connection) juga menjelaskan kapan percobaan ulang aman. Refresh token yang sudah digunakan dapat mengakhiri koneksi saat Anda mengirimnya lagi.

### Error dari endpoint pencabutan

Untuk sebagian besar permintaan yang ditolak `auth.claude.com`, endpoint pencabutan mengembalikan HTTP 400 dan body JSON dengan `error` dan `error_description`.

| Error | Kapan |
| ----- | ----- |
| `invalid_request` | Parameter wajib tidak ada atau tidak valid, misalnya `client_id` yang tidak ada. Permintaan tidak mengirim satu pun dari `token`, `connection_id`, dan `user_profile_id`, atau mengirim lebih dari satu. Sebuah ID salah format, misalnya memiliki prefiks yang salah. Kredensial atau `token` berada dalam query string URL. Profil pengguna memiliki terlalu banyak koneksi untuk satu permintaan: permintaan tersebut mungkin telah mengakhiri sebagian di antaranya, jadi akhiri sisanya dengan `connection_id`. |
| `invalid_client` | `auth.claude.com` tidak dapat mengautentikasi aplikasi Anda. Untuk hal yang perlu diperiksa, lihat `invalid_client` dalam [Error dari endpoint PAR dan token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#errors-from-the-par-and-token-endpoints). |
| `unauthorized_client` | Aplikasi Anda tidak disiapkan untuk permintaan ini. Hubungi tim akun Anthropic Anda. |

Respons dalam tabel berikutnya menggunakan format berbeda, yang mungkin bukan JSON. Jika body berupa JSON, `error` adalah objek, bukan string.

| Status | Kapan | Apa yang harus dilakukan |
| ----- | ----- | ----- |
| 400 | Sebuah parameter lebih panjang dari batasnya. | Perbaiki permintaan. Jangan mencoba ulang. |
| 429 | Terlalu banyak permintaan gagal yang berasal dari alamat IP Anda. | Coba ulang dengan backoff. |
| 500 | `auth.claude.com` gagal memproses permintaan. | Coba ulang dengan backoff. Jika terus terjadi, hubungi tim akun Anthropic Anda. |
| 501 | Anthropic belum mengaktifkan endpoint ini untuk organisasi Anda. | Jangan mencoba ulang. Hubungi tim akun Anthropic Anda. |
| 503 | Permintaan tidak selesai. Apa pun yang telah diakhirinya tetap berakhir. | Coba ulang dengan backoff, dengan parameter yang sama dan client assertion baru. Percobaan ulang akan menyelesaikan sisanya, dan daftarnya tidak mencantumkan koneksi yang telah diakhiri oleh permintaan sebelumnya. Jika Anda mengirim `user_profile_id`, coba ulang dalam satu hari: setelah itu, percobaan ulang dapat mengembalikan 200 dengan daftar kosong dan tidak menyelesaikan apa pun. Percobaan ulang dengan setiap `connection_id` berfungsi kapan saja. |

### Error penagihan

Ini berlaku untuk permintaan Claude API yang mengatur `billing_policy.bill_to` ke `"user_profile"` atau yang melakukan autentikasi dengan [token akses koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#oauth-tokens-for-a-billing-connection). Claude API tidak menagih organisasi mana pun untuk permintaan yang ditolak. Tidak ada respons 402 dan 403 yang dapat dicoba ulang, kecuali penolakan `user_profile_not_billable` dalam 10 detik pertama setelah koneksi baru.

| Status | Tipe dan kode error | Kapan |
| ----- | ----- | ----- |
| 400 | `invalid_request_error` | Permintaan mengirim `billing_policy` tanpa header beta `user-profiles-billing-2026-10-01`. Atau objek `billing_policy` memiliki field yang tidak ada atau tidak valid. Dengan token akses koneksi penagihan, `bill_to` boleh dihilangkan. Atau permintaan menggunakan eksekusi kode di luar kombinasi yang diizinkan. |
| 400 | `invalid_request_error`, `user_profile_required` | `bill_to` adalah `"user_profile"`, permintaan tidak menyertakan ID profil pengguna, dan permintaan tidak melakukan autentikasi dengan token akses koneksi penagihan. |
| 400 | `invalid_request_error`, tanpa kode error | Permintaan melakukan autentikasi dengan token akses koneksi penagihan, dan mengatur `bill_to` ke `"self"` atau menyebutkan profil pengguna selain profil yang menjadi batasan token tersebut. Masing-masing dari kedua penolakan ini menyebutkan apa yang salah dalam `error.message`. |
| 401 | `authentication_error` | Permintaan melakukan autentikasi dengan token akses koneksi penagihan yang telah kedaluwarsa, yang telah digantikan oleh refresh, atau yang koneksinya telah berakhir. Pesan menyebutkan apakah token telah kedaluwarsa atau telah dicabut. Kirim permintaan lagi dengan token akses saat ini, atau tautkan pelanggan lagi jika koneksi telah berakhir. Setelah koneksi berakhir, setiap permintaan baru dengan token aksesnya dapat menerima 401 ini atau 403 `user_profile_not_billable`, tanpa urutan tetap. |
| 402 | `billing_error`, `linked_organization_spend_limit_reached` | Organisasi pelanggan telah mencapai batas pengeluaran yang ditetapkannya, baik untuk aplikasi OAuth Anda maupun untuk seluruh organisasi. Claude API mengirim kode yang sama ketika organisasi tidak memiliki kredit yang dapat membayar permintaan tersebut. Respons tidak menyebutkan yang mana. Minta pelanggan untuk memeriksa kedua batas tersebut dan saldo kreditnya. [Error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#expected-errors) untuk Linked billing menjelaskan di mana masing-masing ditetapkan dan apa yang perlu diubah. |
| 402 | `billing_error`, `linked_organization_billing_unavailable` | Anthropic saat ini tidak dapat menagih organisasi pelanggan karena masalah pada akun Anthropic milik organisasi tersebut. Kode yang sama mengakhiri balasan yang telah dimulai Claude ketika kredit organisasi tersebut habis. Minta pelanggan untuk memeriksa status penagihannya dengan Anthropic. |
| 403 | `permission_error`, tanpa kode error | Anthropic tidak menagih organisasi Anda secara langsung, sehingga tidak dapat menagih pelanggan atas nama Anda. |
| 403 | `permission_error`, `user_profile_not_billable` | Profil pengguna tidak memiliki koneksi ke organisasi pelanggan, administrator atau back end Anda mengakhiri koneksi, organisasi pelanggan tidak membayar Anthropic secara langsung untuk penggunaan API-nya (kredit prabayar dan penagihan berbasis faktur sama-sama terhitung), atau permintaan tidak diautentikasi sebagai akun layanan aplikasi Anda. Respons tidak menyebutkan yang mana. Token akses koneksi juga dapat menerimanya setelah koneksi berakhir. [Penyebab `user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#user-profile-not-billable) menjelaskan apa yang perlu diperiksa untuk masing-masing penyebab. |
| 503 | `overloaded_error` | Claude API untuk sementara tidak dapat memastikan apakah dapat menagih pelanggan. Coba ulang permintaan. Jika respons menyertakan header `retry-after`, tunggu selama waktu tersebut sebelum mencoba ulang. |

Pada `/v1/messages`, kode error ada di `error.details.error_code`. Pada `/v1/chat/completions`, `error.type` selalu `invalid_request_error`, `error.code` berisi tipe error Anthropic (misalnya `permission_error` atau `billing_error`), dan respons tidak memiliki kode error, jadi lakukan pencocokan berdasarkan status HTTP dan `error.code`.

## Standar

| Standar | Tempat berlakunya |
| ----- | ----- |
| [OAuth 2.0 (RFC 6749)](https://www.rfc-editor.org/rfc/rfc6749) | Alur kode otorisasi, endpoint token, dan respons error |
| [PKCE (RFC 7636)](https://www.rfc-editor.org/rfc/rfc7636) | Wajib dengan `S256` pada setiap permintaan otorisasi |
| [Pushed authorization requests (RFC 9126)](https://www.rfc-editor.org/rfc/rfc9126) | Wajib pada setiap permintaan otorisasi |
| [Pencabutan token (RFC 7009)](https://www.rfc-editor.org/rfc/rfc7009) | Endpoint pencabutan, yang juga menerima ID koneksi dan ID profil pengguna serta mengembalikan ID koneksi yang diakhirinya |
| [Autentikasi klien JWT (RFC 7523)](https://www.rfc-editor.org/rfc/rfc7523) | Autentikasi klien `private_key_jwt` di endpoint PAR, token, dan pencabutan, serta pertukaran token akun layanan untuk permintaan yang menagih pelanggan |

## Istilah yang digunakan di halaman-halaman ini

Arti berikut hanya berlaku untuk Claude Platform OAuth.

| Istilah | Arti |
| ----- | ----- |
| Organisasi Claude | Akun organisasi dengan Anthropic. Perusahaan Anda memilikinya, demikian juga setiap pelanggan yang menautkan organisasinya untuk penagihan. |
| Administrator | Anggota organisasi Claude dengan peran Admin atau Penagihan. |
| Aplikasi OAuth | Pendaftaran di organisasi Claude Anda yang mengidentifikasi produk Anda ke `auth.claude.com`. Aplikasi ini memiliki ID klien, nama, logo, URL beranda, dan URI pengalihan. |
| Penyedia identitas | Layanan di infrastruktur Anda sendiri yang menandatangani JWT berumur pendek untuk back end Anda dan memublikasikan kunci publiknya sebagai JSON Web Key Set (JWKS), seperti layanan identitas workload penyedia cloud Anda atau issuer Anda sendiri yang sesuai dengan OIDC. Di halaman-halaman ini, “penyedia identitas Anda” selalu berarti layanan ini, bukan Anthropic. |
| Client assertion | JWT berumur pendek yang ditandatangani oleh penyedia identitas Anda dan dikirim oleh back end Anda untuk mengautentikasi aplikasi OAuth Anda. Ini adalah metode autentikasi klien `private_key_jwt` (RFC 7523). |
| Pushed authorization request (PAR) | Permintaan di mana back end Anda mengirim parameter otorisasi langsung ke `auth.claude.com` dan menerima `request_uri` untuk digunakan dalam pengalihan browser (RFC 9126). |
| Workload Identity Federation | Fitur Claude Console yang digunakan organisasi Anda untuk mendaftarkan penyedia identitas Anda, sehingga Anthropic menerima JWT yang ditandatangani dengan kunci dalam JWKS Anda. |
| Profil pengguna | Catatan yang Anda buat di organisasi Claude Anda sendiri untuk mewakili salah satu pelanggan Anda. Koneksi penagihan menautkan profil pengguna ke organisasi Claude pelanggan. |
| Akun layanan | Akun non-manusia di organisasi Claude Anda. Aplikasi OAuth Anda ditautkan ke satu akun layanan, yaitu akun layanan operatornya. Back end Anda diautentikasi sebagai akun layanan tersebut saat mengirim permintaan yang menagih pelanggan. |
| Token OAuth koneksi | Token akses yang dikembalikan `auth.claude.com` untuk koneksi penagihan, dan refresh token yang dikembalikannya jika pelanggan juga menyetujui `offline_access`. Token akses melakukan autentikasi sebagai akun layanan operator dan hanya dapat menagih profil pengguna dari koneksi tersebut. Lihat [Token OAuth untuk koneksi penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#oauth-tokens-for-a-billing-connection). |
