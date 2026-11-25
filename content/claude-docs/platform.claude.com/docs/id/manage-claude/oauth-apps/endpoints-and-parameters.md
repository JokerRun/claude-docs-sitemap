---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 654579c5dad031e241cb06e64215ffc067d3e889a4a5e028a87cdf8511acbccf
---

---
title: Endpoint dan parameter OAuth
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters
description: Endpoint, parameter, scope, token OAuth, masa berlaku, dan error dari Claude Platform OAuth, sesuai urutan penggunaannya dalam sebuah permintaan.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Sesuai urutan permintaan, halaman ini mencantumkan nilai-nilai yang digunakan oleh permintaan [Claude Platform OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview), lalu [istilah yang digunakan di halaman-halaman ini](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#terms).

## Endpoint

| Endpoint | URL |
| ----- | ----- |
| “Authorization endpoint” (endpoint otorisasi; halaman persetujuan) | `https://auth.claude.com/oauth/authorize` |
| Endpoint “pushed authorization request” (permintaan otorisasi yang didorong), atau PAR | `https://auth.claude.com/v1/oauth/par` |
| “Token endpoint” (endpoint token) | `https://auth.claude.com/v1/oauth/token` |
| “Revocation endpoint” (endpoint pencabutan) | `https://auth.claude.com/v1/oauth/revoke` |
| Claude API ([profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) dan permintaan yang menagih pelanggan) | `https://api.anthropic.com` |

## Autentikasi klien

`auth.claude.com` mengautentikasi aplikasi Anda dengan variasi metode `private_key_jwt` ([RFC 7523](https://www.rfc-editor.org/rfc/rfc7523)). Penyedia identitas Anda, bukan aplikasi Anda, yang menerbitkan dan menandatangani “client assertion” (asersi klien). `iss`-nya adalah penerbit penyedia identitas Anda. `aud`-nya adalah audiens yang dikonfigurasi untuk aplikasi Anda, bukan client ID Anda atau URL lengkap endpoint. `auth.claude.com` memeriksanya terhadap kunci yang terdaftar untuk penerbit tersebut dan pengaturan aplikasi Anda.

Kirim parameter ini di body setiap permintaan `POST` ke endpoint PAR, token, dan pencabutan.

| Parameter | Nilai |
| ----- | ----- |
| `client_id` | Client ID aplikasi OAuth Anda, wajib bahkan ketika menggunakan client assertion |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` |
| `client_assertion` | JWT dari penyedia identitas Anda dengan klaim yang tercantum di [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-assertion-claims) |

Aturan berikut berlaku untuk setiap permintaan:

* **Body:** Dapat berupa JSON atau form-encoded (`application/x-www-form-urlencoded`). Atur header `Content-Type` agar sesuai.
* **Query string:** `auth.claude.com` menolak kredensial di query string URL.
* **HTTP Basic:** Jangan kirim header `Authorization` HTTP Basic. `auth.claude.com` tidak membaca kredensial darinya, dan endpoint PAR dapat menolak permintaan yang memilikinya.

### Klaim client assertion

Client assertion harus berisi klaim berikut. Nilai yang harus dicocokkan ada di [pengaturan autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication) aplikasi Anda.

| Klaim | Persyaratan |
| ----- | ----- |
| `iss` | URL penerbit penyedia identitas Anda, persis seperti yang didaftarkan melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) |
| `sub` | Subjek back end Anda. Jika pengaturan aplikasi Anda memiliki pola subjek, subjek harus cocok dengannya. |
| `aud` | Tepat satu audiens: nilai di pengaturan aplikasi Anda, bukan URL lengkap endpoint yang Anda panggil |
| `iat` | Waktu penyedia identitas Anda menerbitkan JWT |
| `exp` | Waktu kedaluwarsa, tidak lebih dari [masa berlaku maksimum](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification) penerbit Anda setelah `iat` (1 jam secara default) |

Header dan tanda tangan client assertion juga harus memenuhi aturan berikut:

* **Algoritma:** `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, atau `PS512`, daftar yang sama seperti di [referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification). `auth.claude.com` menolak algoritma lain, termasuk algoritma HMAC (`HS256`, `HS384`, `HS512`) dan `none`.
* **Key ID:** `kid` di header harus menyebutkan kunci di JWKS Anda. Jika kunci tersebut mendeklarasikan `alg`, itu harus algoritma yang menandatangani asersi.
* **JWKS Anda:** Setiap kunci penandatanganan harus memiliki `kid`. Kunci tanpa `kid` membuat seluruh set tidak dapat digunakan.

Payload asersi terlihat seperti ini. `aud`-nya adalah **Expected audience** milik aplikasi Anda sendiri, dari tab **Client authentication** aplikasi:

```json
{
  "iss": "https://idp.example.com",
  "sub": "workload:prod:claude-integration-backend",
  "aud": "https://auth.claude.com",
  "iat": 1791230000,
  "exp": 1791230300
}
```

`auth.claude.com` menerima JWT apa pun dari penyedia identitas Anda yang cocok dengan pola subjek dan kondisi klaim aplikasi Anda. Untuk mempersempitnya, lihat [Siapkan autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication).

## Permintaan otorisasi

Untuk membangun alur persetujuan yang menggunakan nilai-nilai ini, lihat [Mengarahkan pelanggan untuk memberikan persetujuan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#send-them-to-approve).

### Parameter permintaan otorisasi

Kirim parameter ini beserta parameter di [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-authentication) ke endpoint PAR.

| Parameter | Deskripsi |
| ----- | ----- |
| `response_type` | Nilai `code` |
| `client_id` | Client ID aplikasi OAuth Anda |
| `redirect_uri` | URI yang persis cocok dengan redirect URI yang terdaftar, hingga 2.048 karakter |
| `scope` | `billing:attribution` atau `billing:attribution offline_access`. Lihat [apa yang diizinkan setiap scope](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#scopes). |
| `state` | Nilai acak sekali pakai, hingga 2.048 karakter, yang Anda periksa pada callback |
| `code_challenge` | `BASE64URL(SHA256(code_verifier))` tanpa padding, dengan `code_verifier` sepanjang 43 hingga 128 karakter |
| `code_challenge_method` | Nilai `S256` |
| `connection_type` | Nilai `organization_shared`. Seorang administrator menyetujui koneksi untuk seluruh organisasi. |
| `connection_auth_target` | Nilai `platform`. Permintaan koneksi diarahkan ke pemilik aplikasi OAuth. |
| `user_profile_id` | ID profil pengguna di organisasi Anda yang mewakili pelanggan dan tidak diarsipkan |

Endpoint PAR mengembalikan HTTP 201 dengan `request_uri` dan `expires_in`. Kemudian, arahkan browser orang tersebut ke endpoint otorisasi hanya dengan dua parameter ini:

| Parameter | Nilai |
| ----- | ----- |
| `client_id` | Client ID aplikasi OAuth Anda |
| `request_uri` | Nilai yang dikembalikan oleh endpoint PAR |

Setelah orang tersebut menyetujui, `auth.claude.com` mengarahkan browser ke `redirect_uri` Anda dengan parameter query berikut:

| Parameter | Nilai |
| ----- | ----- |
| `code` | Kode otorisasi untuk ditukarkan di endpoint token |
| `state` | Nilai `state` yang Anda kirim. Periksa apakah cocok. |
| `iss` | `https://identity.anthropic.com/users`, yang berbeda dari host endpoint. Periksa apakah ada dan cocok. |

### Scope

| Scope | Deskripsi |
| ----- | ----- |
| `billing:attribution` | Koneksi yang memungkinkan Anda menagih organisasi Claude pelanggan untuk permintaan Claude API yang Anda buat atas arahan pelanggan. Kirim sendiri atau bersama `offline_access`. |
| `offline_access` | Juga memberikan refresh token kepada aplikasi Anda. Pada koneksi penagihan, kirim hanya bersama `billing:attribution`. |
| `org:billing_attribution` | Tidak digunakan lagi: gunakan `billing:attribution`. Lihat [Jika Anda masih menggunakan scope usang](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-still-use-the-deprecated-scope). |

### Aturan redirect URI

* Setiap `redirect_uri` harus persis cocok dengan URI yang terdaftar di aplikasi Anda. Tidak ada pencocokan wildcard atau prefiks. Satu-satunya pengecualian adalah URI pengembangan lokal yang didaftarkan dengan tanda bintang sebagai port, seperti `http://localhost:*/callback`, yang cocok dengan port apa pun.
* Setiap redirect URI harus menggunakan HTTPS dan tidak boleh berisi fragmen. URI pengembangan lokal di `localhost`, `127.0.0.1`, atau `[::1]` boleh menggunakan HTTP.
* Anda dapat mendaftarkan hingga 10 redirect URI untuk setiap aplikasi.
* `auth.claude.com` mengirim error ke redirect URI Anda hanya jika `redirect_uri` cocok dengan URI yang terdaftar. Untuk `redirect_uri` lainnya, browser tidak dialihkan.

## Token OAuth

### Permintaan dan respons token

Untuk menukarkan kode, kirim parameter ini ke [endpoint token](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#endpoints):

| Parameter | Nilai |
| ----- | ----- |
| `grant_type` | `authorization_code` |
| `code` | Kode dari callback |
| `redirect_uri` | `redirect_uri` yang sama dengan yang Anda kirim di permintaan otorisasi |
| `code_verifier` | Code verifier PKCE |
| `client_id`, `client_assertion_type`, `client_assertion` | Seperti di [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-authentication) |

Untuk menyegarkan, kirim `grant_type` yang diatur ke `refresh_token`, `refresh_token`, dan parameter di [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-authentication). Setiap refresh token hanya berfungsi sekali, dan koneksi penagihan memiliki aturannya sendiri: lihat bagian berikutnya dan [Jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails).

### Token OAuth untuk koneksi penagihan

Untuk koneksi `billing:attribution`, penyegaran tidak boleh mengirim parameter `scope`. Kedua grant mengembalikan field berikut:

| Field respons | Nilai |
| ----- | ----- |
| `access_token` | Token akses koneksi |
| `token_type` | `Bearer` |
| `expires_in` | Detik hingga token akses kedaluwarsa, paling lama `3600` |
| `scope` | Selalu `workspace:inference`, bukan scope yang Anda minta |
| `connection_id` | ID koneksi, misalnya `ocon_01HV9Z`. Hanya grant `authorization_code` yang mengembalikannya. |
| `refresh_token` | Dikembalikan hanya jika pelanggan menyetujui `offline_access`. Penyegaran mengembalikan yang baru, yang menggantikan yang Anda kirim. |
| `refresh_token_expires_in` | Detik hingga `refresh_token` kedaluwarsa. Tidak disertakan jika tidak ada `refresh_token`. |

Token akses mengautentikasi sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#terms) aplikasi Anda, di [workspace default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace) aplikasi, yang oleh API disebut sebagai pengaturan `connection_token_workspace_id`. Pada `/v1/messages` dan `/v1/chat/completions`, permintaan dengan token tersebut ditagihkan ke pelanggan koneksi tersebut. Token ini hanya berfungsi pada endpoint yang tercantum di [Panggil Claude dengan token akses pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#call-claude-with-a-token), dan endpoint lain menolaknya. Cara menggunakan, menyegarkan, dan memulihkan token ini ada di [Gunakan kredensial terpisah untuk setiap pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer).

Setiap peristiwa berikut mencabut token koneksi `billing:attribution`, termasuk token akses saat ini:

* Pelanggan atau Anda membatalkan tautan.
* Pelanggan menyetujui permintaan otorisasi baru dengan scope berbeda untuk profil pengguna yang sama, dan Anda menukarkan kodenya. Koneksi baru menggantikan koneksi sebelumnya.
* Workspace tempat token berjalan diarsipkan.
* Refresh token yang telah digantikan oleh penyegaran dikirim lagi lebih dari 30 detik kemudian.
* Anda mencabut salah satu token koneksi di [endpoint pencabutan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#revocation).

### Masa berlaku

| Item | Masa berlaku |
| ----- | ----- |
| `request_uri` dari endpoint PAR | 10 menit, sekali pakai |
| Kode otorisasi | 5 menit, sekali pakai |
| `access_token` | Hingga 1 jam |
| `refresh_token` | Hingga 1 tahun sejak penukaran kode. Penyegaran tidak memperpanjangnya. |

Jika respons memberikan `expires_in` atau `refresh_token_expires_in`, baca masa berlaku dari nilai tersebut, bukan dari tabel ini.

### Pencabutan

Kirim permintaan pencabutan ke endpoint pencabutan, `https://auth.claude.com/v1/oauth/revoke`. Selain token, endpoint ini menerima ID koneksi dan ID profil pengguna. Untuk membatalkan tautan pelanggan atau menautkannya lagi, lihat [Kelola pelanggan tertaut](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers). Kirim parameter di [Autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-authentication) dan tepat satu dari berikut:

| Parameter | Apa yang diakhirinya |
| ----- | ----- |
| `connection_id` | Salah satu koneksi aplikasi Anda, diberikan sebagai ID `ocon_` |
| `user_profile_id` | Semua koneksi aplikasi Anda pada satu profil pengguna, diberikan sebagai ID `uprof_` |
| `token` | Koneksi tempat token akses atau refresh token berasal, dan semua token koneksi tersebut |

Token akses dari koneksi yang disetujui dengan scope `org:billing_attribution` yang tidak digunakan lagi merupakan pengecualian: mengirimnya hanya mengakhiri token tersebut. Untuk mengakhiri koneksi itu, kirim `connection_id` atau `user_profile_id`.

`auth.claude.com` menerima `token_type_hint` dan mengabaikannya.

Endpoint mengembalikan HTTP 200 dan ID koneksi yang diakhiri oleh permintaan:

```json
{
  "revoked_connection_ids": ["ocon_01HV9Z"]
}
```

Daftar kosong dalam salah satu kasus berikut, dan respons tidak menyebutkan yang mana:

* Token atau ID tidak dikenal atau milik aplikasi lain.
* Koneksi sudah berakhir.
* Permintaan mengakhiri token tetapi tidak mengakhiri koneksi.

Setelah koneksi berakhir, Claude API menolak permintaan yang menagih pelanggan tersebut dengan `user_profile_billing_not_authorized`, dan token koneksi berhenti berfungsi. Token akses dari koneksi yang disetujui dengan scope yang tidak digunakan lagi mungkin tetap berfungsi hingga kedaluwarsa.

## Error protokol

### Error pada redirect

`auth.claude.com` mengembalikan error sebagai parameter query `error`, `error_description`, `state`, dan `iss` pada redirect URI Anda. Ini adalah error OAuth 2.0 standar ([RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)), kecuali `user_profile_already_linked`.

| Error | Kapan |
| ----- | ----- |
| `access_denied` | Orang tersebut menolak atau tidak dapat menyetujui permintaan ini. Lihat [`access_denied`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#access-denied). |
| `server_error` | `auth.claude.com` gagal memproses permintaan. Minta orang tersebut untuk mencoba lagi. |
| `user_profile_already_linked` | Organisasi pelanggan sudah ditautkan ke aplikasi Anda melalui profil pengguna lain, atau profil pengguna sudah ditautkan ke aplikasi Anda melalui organisasi lain. Lihat [`user_profile_already_linked`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-already-linked). |

Jika `request_uri` telah kedaluwarsa atau sudah digunakan, `auth.claude.com` menampilkan halaman error dan tidak mengalihkan browser. Mulai lagi dengan pushed authorization request baru.

### Error dari endpoint PAR dan token

Endpoint ini mengembalikan body JSON dengan `error` dan `error_description`.

| Error | Kapan |
| ----- | ----- |
| `invalid_request` | Parameter wajib tidak ada atau tidak valid, seperti `state` yang tidak ada, challenge PKCE yang tidak ada, atau `user_profile_id` yang bukan profil pengguna aktif di organisasi Anda |
| `invalid_client` | Client ID tidak dikenal, atau client assertion gagal dalam pemeriksaan di [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-assertion-claims). **Client authentication history** aplikasi Anda di Claude Console menunjukkan pemeriksaan mana yang gagal. |
| `invalid_scope` | Scope tidak diizinkan untuk aplikasi ini, penyegaran koneksi penagihan mengirim parameter `scope`, atau `billing:attribution` telah dihapus dari aplikasi Anda. Dalam kasus terakhir, penukaran kode juga menghabiskan kode. |
| `invalid_grant` | Saat penukaran kode: kode telah kedaluwarsa atau sudah digunakan, orang yang menyetujui telah keluar dari akunnya, atau kode tidak cocok dengan `redirect_uri` atau `code_verifier`. Ketidakcocokan menghabiskan kode. |
| `invalid_grant` | Saat penukaran kode: pelanggan menyetujui lagi dengan scope yang sama sementara koneksinya memiliki refresh token. Lihat [Jika pelanggan memberikan persetujuan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-a-customer-approves-again). |
| `invalid_grant` | Saat penyegaran: lihat [Jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails) |
| `unauthorized_client` | Aplikasi Anda tidak disiapkan untuk permintaan ini. Error ini tidak menghabiskan kode dan tidak mencabut refresh token. Lihat [`unauthorized_client`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#code-exchange-unauthorized-client) atau, untuk penyegaran, [Jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails). |
| `user_profile_already_linked` | Dari endpoint token: antara persetujuan dan penukaran, profil atau organisasi ditautkan dengan cara lain |

Beberapa respons datang dalam format lain, yang mungkin bukan JSON. Hal itu terjadi ketika `auth.claude.com` menerapkan “rate limit” (batas laju) pada permintaan atau mengalami gangguan. Hal itu juga terjadi untuk `grant_type` yang tidak dikenal atau parameter yang terlalu panjang. Tangani respons tanpa `error` berupa string berdasarkan statusnya, menggunakan baris pertama yang sesuai:

| Status | Apa yang harus dilakukan |
| ----- | ----- |
| Status apa pun, saat penyegaran | Ikuti [Jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails). |
| `501` | Anthropic telah menonaktifkan endpoint. Jangan coba lagi. |
| `429` atau `5xx` | Coba lagi dengan backoff, dan tunggu setidaknya selama yang disebutkan header `retry-after` mana pun. Kirim setiap percobaan ulang dari kode Anda sendiri: percobaan ulang otomatis klien HTTP mungkin tidak berjalan untuk respons semacam itu. |
| Status lainnya | Anggap sebagai kesalahan dalam permintaan. |

### Error dari endpoint pencabutan

Untuk sebagian besar penolakan, endpoint pencabutan mengembalikan HTTP 400 dan body JSON dengan `error` dan `error_description`.

| Error | Kapan |
| ----- | ----- |
| `invalid_request` | Parameter tidak ada atau tidak valid: tidak ada atau lebih dari satu dari `token`, `connection_id`, dan `user_profile_id`, ID yang salah format, atau kredensial di query string URL |
| `invalid_request` | Profil pengguna memiliki terlalu banyak koneksi untuk satu permintaan. Permintaan itu mungkin telah mengakhiri sebagian, jadi akhiri sisanya dengan masing-masing `connection_id`. |
| `invalid_client` | `auth.claude.com` tidak dapat mengautentikasi aplikasi Anda. Periksa client assertion Anda terhadap [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-assertion-claims). **Client authentication history** aplikasi Anda tidak mencatat endpoint ini. |
| `unauthorized_client` | Aplikasi Anda tidak disiapkan untuk permintaan ini. Hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) atau tim akun Anthropic Anda jika Anda memilikinya. |

Penolakan lainnya hanya membawa status, dan body-nya mungkin bukan JSON. Jika body tersebut berupa JSON, `error`-nya adalah objek, bukan string:

| Status | Kapan | Apa yang harus dilakukan |
| ----- | ----- | ----- |
| `400` | Parameter lebih panjang dari batasnya | Perbaiki permintaan. Jangan coba lagi. |
| `429` | Terlalu banyak permintaan gagal berasal dari alamat IP Anda | Coba lagi dengan backoff. |
| `500` | `auth.claude.com` gagal memproses permintaan | Coba lagi dengan backoff. Jika terus terjadi, hubungi dukungan atau tim akun Anda. |
| `501` | Anthropic telah menonaktifkan endpoint | Jangan coba lagi. Hubungi dukungan atau tim akun Anda. |
| `503` | Permintaan tidak selesai, dan apa pun yang telah diakhirinya tetap berakhir | Coba lagi dengan backoff. Gunakan parameter yang sama dan client assertion baru. |

Percobaan ulang setelah `503` menyelesaikan sisanya, dan daftarnya tidak menyertakan koneksi yang diakhiri oleh permintaan sebelumnya. Dengan `connection_id`, coba lagi kapan saja. Dengan `user_profile_id`, coba lagi dalam satu hari. Setelah satu hari, percobaan ulang tetap mengakhiri koneksi aktif. Percobaan ulang tidak mencabut sisa dari koneksi yang diakhiri oleh permintaan yang gagal, seperti token OAuth-nya. Untuk mencabutnya, kirim setiap `connection_id` yang tersimpan.

### Error penagihan

Error Claude API untuk permintaan yang menagih pelanggan atau yang menggunakan token akses pelanggan ada di [Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#while-billing).

## Standar

| Standar | Di mana berlaku |
| ----- | ----- |
| [OAuth 2.0 (RFC 6749)](https://www.rfc-editor.org/rfc/rfc6749) | Alur kode otorisasi, endpoint token, dan respons error |
| [PKCE (RFC 7636)](https://www.rfc-editor.org/rfc/rfc7636) | Wajib dengan `S256` pada setiap permintaan otorisasi |
| [Pushed authorization requests (RFC 9126)](https://www.rfc-editor.org/rfc/rfc9126) | Wajib untuk Linked billing |
| [Authorization server issuer identification (RFC 9207)](https://www.rfc-editor.org/rfc/rfc9207) | Parameter `iss` pada setiap redirect ke aplikasi Anda |
| [Token revocation (RFC 7009)](https://www.rfc-editor.org/rfc/rfc7009) | Endpoint pencabutan, yang juga menerima ID koneksi dan ID profil pengguna |
| [JWT client authentication (RFC 7523)](https://www.rfc-editor.org/rfc/rfc7523) | Autentikasi klien di endpoint PAR, token, dan pencabutan |

## Istilah yang digunakan di halaman-halaman ini

Makna berikut hanya berlaku untuk Claude Platform OAuth.

| Istilah | Makna |
| ----- | ----- |
| Organisasi Claude | Akun organisasi dengan Anthropic. Perusahaan Anda memilikinya, begitu pula setiap pelanggan yang menautkan organisasinya untuk penagihan. |
| Administrator | Anggota organisasi Claude dengan peran Admin atau Billing |
| Aplikasi OAuth | Pendaftaran di organisasi Claude Anda yang mengidentifikasi produk Anda ke `auth.claude.com`. Aplikasi ini memiliki client ID, nama, logo, beranda, dan redirect URI. |
| Penyedia identitas | Layanan di infrastruktur Anda sendiri yang menandatangani JWT berumur pendek untuk back end Anda dan memublikasikan kunci publiknya sebagai JSON Web Key Set (JWKS). Layanan ini tidak pernah Anthropic. |
| Client assertion | JWT berumur pendek yang ditandatangani oleh penyedia identitas Anda dan dikirim oleh back end Anda untuk mengautentikasi aplikasi OAuth Anda |
| Pushed authorization request (PAR) | Permintaan di mana back end Anda mengirim parameter otorisasi ke `auth.claude.com` dan mendapatkan `request_uri` untuk digunakan dalam redirect browser |
| Workload Identity Federation | Fitur Claude Console tempat organisasi Anda mendaftarkan penyedia identitas Anda sehingga Anthropic menerima JWT yang ditandatangani dengan kunci Anda |
| Profil pengguna | Catatan di organisasi Claude Anda sendiri yang mewakili salah satu pelanggan Anda |
| Koneksi | Catatan yang mengikat organisasi Claude pelanggan ke salah satu profil pengguna Anda, dibuat ketika pelanggan menautkan aplikasi Anda. ID-nya diawali dengan `ocon_`. |
| Akun layanan | Akun non-manusia di organisasi Claude Anda. Akun layanan operator aplikasi Anda adalah akun yang digunakan back end Anda untuk mengautentikasi guna menagih pelanggan. |
| Token OAuth koneksi | Token akses yang dikembalikan `auth.claude.com` untuk sebuah koneksi dan refresh token yang dikembalikannya dengan `offline_access`. Token akses hanya dapat menagih pelanggan koneksi tersebut. |
