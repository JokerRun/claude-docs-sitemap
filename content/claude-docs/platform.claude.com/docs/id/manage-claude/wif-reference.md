---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
fetched_at: 2026-11-14T02:12:32.675862Z
sha256: deadeff95daa0f3a1ef32a1e683a1556638302084c00359ff621866924b0a513
---

---
title: Referensi WIF
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
description: Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error untuk Workload Identity Federation.
---

Halaman ini mengumpulkan permukaan konfigurasi, batasan validasi, dan pemetaan error untuk [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) (WIF). Untuk panduan penyiapan langkah demi langkah, lihat [Penyedia identitas](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers).

## Permintaan pertukaran token

`POST /v1/oauth/token` menerima body JSON menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). SDK membangun permintaan ini untuk Anda dari [variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables).

| Field                | Wajib       | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`         | Ya          | Selalu `urn:ietf:params:oauth:grant-type:jwt-bearer`.                                                                                                                                                                                                                                                                                                                                                                            |
| `assertion`          | Ya          | JWT OIDC yang diterbitkan oleh penyedia identitas Anda.                                                                                                                                                                                                                                                                                                                                                                          |
| `federation_rule_id` | Ya          | ID bertag (`fdrl_...`) dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                                                                                                                                                |
| `organization_id`    | Ya          | UUID organisasi Anthropic Anda.                                                                                                                                                                                                                                                                                                                                                                                                  |
| `service_account_id` | Tidak       | ID bertag (`svac_...`) dari akun layanan target aturan. Aturan, bukan field ini, yang menentukan akun mana yang diwakili oleh token. Jika Anda mengirim field ini, nilainya harus berupa ID akun tersebut.                                                                                                                                                                                                                       |
| `workspace_id`       | Kondisional | ID bertag (`wrkspc_...`) dari workspace yang menjadi cakupan token yang dicetak. Wajib ketika aturan diaktifkan untuk semua workspace atau untuk lebih dari satu workspace. Jika dihilangkan, server memilih satu-satunya workspace yang diaktifkan untuk aturan tersebut. Literal `default` juga berfungsi untuk workspace default organisasi tetapi sudah usang (deprecated). Gunakan ID `wrkspc_...` dari workspace tersebut. |

## Respons pertukaran token

`POST /v1/oauth/token` mengembalikan respons token OAuth 2.0 standar ([RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1)):

| Field          | Tipe    | Deskripsi                                                                                                           |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| `access_token` | string  | Token Anthropic berumur pendek, dengan awalan `sk-ant-oat01-...`. Teruskan sebagai `Authorization: Bearer <token>`. |
| `token_type`   | string  | Selalu `Bearer`.                                                                                                    |
| `expires_in`   | integer | Jumlah detik hingga token kedaluwarsa.                                                                              |
| `scope`        | string  | Scope OAuth yang diberikan oleh aturan yang cocok.                                                                  |

## Variabel lingkungan

SDK membaca variabel-variabel ini untuk melakukan pertukaran token terfederasi tanpa argumen konstruktor.

| Variabel                        | Wajib                                       | Deskripsi                                                                                                                                                                                                                                                                           |
| ------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_FEDERATION_RULE_ID`  | Ya                                          | ID bertag (`fdrl_...`) dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                   |
| `ANTHROPIC_ORGANIZATION_ID`     | Ya                                          | UUID organisasi Anthropic Anda. Temukan di halaman [Organisasi](https://platform.claude.com/settings/organization) di Claude Console.                                                                                                                                               |
| `ANTHROPIC_IDENTITY_TOKEN_FILE` | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | Path sistem file ke JWT yang diterbitkan oleh “identity provider” (penyedia identitas), atau IdP, Anda. SDK membaca ulang file ini pada setiap pertukaran sehingga token terproyeksi yang berotasi di disk selalu terkini. Contohnya adalah `/var/run/secrets/anthropic.com/token`. |
| `ANTHROPIC_IDENTITY_TOKEN`      | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | JWT literal sebagai string. Gunakan ketika platform Anda menyuntikkan token sebagai variabel lingkungan, bukan file. Contohnya adalah `eyJhbGciOiJSUzI1NiIs...`.                                                                                                                    |
| `ANTHROPIC_SERVICE_ACCOUNT_ID`  | Tidak                                       | ID bertag (`svac_...`) dari akun layanan target aturan. Aturan, bukan variabel ini, yang menentukan akun mana yang diwakili oleh token. Jika Anda mengatur variabel ini, nilainya harus berupa ID akun tersebut.                                                                    |
| `ANTHROPIC_WORKSPACE_ID`        | Kondisional                                 | ID bertag (`wrkspc_...`) dari workspace yang menjadi cakupan token yang dicetak. Wajib ketika aturan federasi diaktifkan untuk semua workspace atau untuk lebih dari satu workspace. Opsional ketika aturan terikat pada satu workspace.                                            |
| `ANTHROPIC_PROFILE`             | Tidak                                       | Nama [profil konfigurasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) yang akan dimuat. Lebih diutamakan daripada variabel lingkungan federasi dalam tabel ini. Contohnya adalah `staging-profile`.                                 |

Jalur federasi langsung melalui variabel lingkungan hanya aktif ketika `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, dan salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` semuanya diatur. SDK juga membaca `ANTHROPIC_WORKSPACE_ID`, tetapi jalur ini aktif dengan atau tanpa variabel tersebut.

Pertukaran mencakupkan token yang dicetak ke workspace yang disebutkan oleh `ANTHROPIC_WORKSPACE_ID`, sehingga berpindah workspace memerlukan pertukaran baru. Tanpa profil, CLI `ant` tidak meneruskan variabel ini ke pertukaran. Dengan CLI `ant`, atur `workspace_id` dalam profil federasi dan atur `ANTHROPIC_PROFILE` ke nama profil tersebut. `ANTHROPIC_WORKSPACE_ID` juga menerima literal `default` untuk workspace default, tetapi bentuk tersebut sudah usang. Gunakan ID `wrkspc_...` dari workspace tersebut.

<Warning>
  Variabel yang diatur ke string kosong dapat menempati slotnya dalam rantai prioritas kredensial. Hapus (unset) variabel kredensial yang tidak digunakan alih-alih mengosongkannya.
</Warning>

### Prioritas kredensial

SDK menyelesaikan kredensial dalam urutan ini. Sumber pertama yang menghasilkan kredensial yang menang.

| Urutan | Sumber                                                              | Catatan                                                                                                                             |
| ------ | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1      | Argumen konstruktor (kunci API, token autentikasi, atau kredensial) | Selalu mengesampingkan semua yang lain.                                                                                             |
| 2      | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN`                     | Sepenuhnya mengesampingkan federasi. Hapus variabel ini saat bermigrasi dari kunci API.                                             |
| 3      | `ANTHROPIC_PROFILE`                                                 | Memuat `<config_dir>/configs/<name>.json`. Jika profil bernama tidak ada, SDK melaporkan error alih-alih mencoba sumber berikutnya. |
| 4      | Variabel lingkungan federasi                                        | `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID` + `ANTHROPIC_IDENTITY_TOKEN[_FILE]`.                                   |
| 5      | Profil aktif                                                        | Diselesaikan dari `<config_dir>/active_config`, dengan fallback ke profil bernama `default`.                                        |

Di CLI `ant`, pengaturan untuk [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication) berada di urutan prioritas setelah variabel lingkungan federasi dan sebelum profil aktif. Pengaturan tersebut adalah proyek, ID workspace, dan lokasi. Anda mengaturnya dengan flag `--google-cloud-*` atau variabel `ANTHROPIC_GOOGLE_CLOUD_*`. CLI menggunakan pengaturan ini ketika salah satu di antaranya diatur. Dengan pengaturan ini, CLI mendapatkan kredensialnya dari Google Application Default Credentials.

Ketika profil dimuat, variabel lingkungan mengisi field apa pun yang dihilangkan oleh profil tetapi tidak pernah mengesampingkan field yang diatur secara eksplisit oleh profil. Misalnya, `ANTHROPIC_WORKSPACE_ID` mengisi `workspace_id` hanya ketika profil aktif tidak mengaturnya.

## File konfigurasi profil

Profil adalah file konfigurasi bernama yang dibaca oleh SDK dan CLI `ant`. Profil memungkinkan Anda menyertakan parameter federasi bersama image container Anda atau beralih antar lingkungan tanpa mengubah kode.

### Direktori konfigurasi

SDK menemukan direktori konfigurasi dalam urutan ini:

1. `$ANTHROPIC_CONFIG_DIR`
2. `~/.config/anthropic` di Linux dan macOS
3. `%APPDATA%\Anthropic` di Windows

### Profil aktif

Nama profil aktif diselesaikan dalam urutan ini:

1. `$ANTHROPIC_PROFILE`
2. Isi dari `<config_dir>/active_config` (file satu baris yang ditulis oleh `ant profile activate <name>`)
3. Nama literal `default`

Claude Code dan Claude Agent SDK mengikuti urutan resolusi yang sama, sehingga profil federasi yang dikonfigurasi di sini juga mengautentikasi alat-alat tersebut tanpa penyiapan tambahan.

### Tata letak file

| Path                                      | Isi                                                                                                  | Sensitivitas                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `<config_dir>/configs/<profile>.json`     | `version`, blok `authentication`, `organization_id`, `workspace_id`, dan `base_url`.                 | Bukan rahasia. Aman untuk di-commit atau dimasukkan ke dalam image. |
| `<config_dir>/credentials/<profile>.json` | `version`, `access_token` yang di-cache, `expires_at`, dan (untuk login interaktif) `refresh_token`. | Rahasia. SDK menulis file ini dengan mode `0600`.                   |

File konfigurasi dan file kredensial sama-sama memiliki field string `version` tingkat atas dalam format `major.minor`, seperti `"1.0"`. SDK menulis field ini secara otomatis. Jika Anda menghilangkan field ini saat menulis konfigurasi secara manual, SDK akan memperlakukan file tersebut sebagai versi saat ini.

### Contoh profil federasi

```json configs/production.json
{
  "version": "1.0",
  "authentication": {
    "type": "oidc_federation",
    "federation_rule_id": "fdrl_...",
    "service_account_id": "svac_...",
    "identity_token": {
      "source": "file",
      "path": "/var/run/secrets/anthropic.com/token"
    }
  },
  "organization_id": "00000000-0000-0000-0000-000000000000",
  "workspace_id": "wrkspc_...",
  "base_url": "https://api.anthropic.com"
}
```

Jika Anda menghilangkan `authentication.identity_token`, SDK beralih ke `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` dari lingkungan.

## Scope OAuth

`oauth_scope` yang Anda atur pada aturan federasi menentukan endpoint Claude API mana yang dapat dipanggil oleh token akses yang dicetak.

| Scope                      | Memberikan akses ke                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer`      | Semua endpoint Claude API non-administratif di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models/list), [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) beserta sesinya, [Files](https://platform.claude.com/docs/id/build-with-claude/files), dan [Skills](https://platform.claude.com/docs/id/build-with-claude/skills-guide). Ini sesuai dengan akses yang dimiliki kunci API workspace di workspace yang sama. |
| `workspace:inference`      | Endpoint inferensi di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models/list), dan [endpoint chat yang kompatibel dengan OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk). Gunakan ini untuk workload yang hanya perlu memanggil Claude dan tidak pernah perlu mengelola Files, Skills, atau sumber daya lainnya.                                                                                            |
| `workspace:manage_tunnels` | [API tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api): membuat, mencantumkan, dan mendapatkan tunnel, mendaftarkan dan mengarsipkan sertifikat CA, menampilkan dan merotasi token tunnel, serta mengarsipkan tunnel. Jendela modal pembuatan tunnel di Console mengunci scope ini ketika Anda membuat aturan darinya.                                                                                                                                                                                                           |
| `org:admin`                | Akses penuh ke [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) (anggota organisasi, undangan, workspace, kunci API, dan lainnya). Token OAuth `org:admin` hanya dapat membuat atau memodifikasi aturan dengan scope `workspace:developer` atau `workspace:inference`. Token tersebut tidak dapat memperbarui issuer yang mendukung aturan dengan scope lain. Lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).                                                                       |

Permintaan ke endpoint di luar scope token mengembalikan HTTP 403. Scope yang lebih terperinci (berdasarkan sumber daya, atau baca versus tulis) tidak tersedia.

### Batas izin

`oauth_scope` aturan federasi adalah batas atas: token yang dicetak tidak pernah dapat melampauinya. `organization_role` akun layanan target (`developer` atau `admin`) menentukan scope mana yang dapat diberikan oleh aturan. Aturan yang memberikan `org:admin` harus menargetkan akun layanan dengan `organization_role=admin`. Izin efektif adalah irisan dari scope aturan dan peran akun layanan.

| `oauth_scope` aturan  | `organization_role` akun layanan | Izin efektif                                                                                                                                                                                                                                                  |
| --------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer` | `admin`                          | Akses Claude API hanya di workspace aturan. Scope membatasi token di bawah peran.                                                                                                                                                                             |
| `org:admin`           | `admin`                          | Akses penuh Admin API (anggota organisasi, undangan, workspace, kunci API, dan lainnya), dikurangi pengecualian untuk pemanggil OAuth. Lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). |

## Aturan validasi

Anthropic memberlakukan batasan-batasan ini ketika Anda membuat atau memperbarui issuer dan aturan, serta ketika Anthropic memverifikasi JWT yang masuk pada saat pertukaran.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API akun layanan](https://platform.claude.com/docs/id/api/organization/service_accounts), [referensi API penerbit federasi](https://platform.claude.com/docs/id/api/organization/federation/issuers), dan [referensi API aturan federasi](https://platform.claude.com/docs/id/api/organization/federation/rules).

### Field sumber daya

| Field                                   | Batasan                                                                                                                                                                                                                                                                                                           |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` issuer, aturan, dan akun layanan | Harus cocok dengan `^[a-z0-9-]+$`, panjang 1 hingga 255 karakter.                                                                                                                                                                                                                                                 |
| `workspace_id`                          | Wajib saat pembuatan kecuali `applies_to_all_workspaces` bernilai true. Workspace (`wrkspc_...`) yang kuota, penagihan, dan batas lajunya berlaku untuk token yang dicetak di bawah aturan ini. Harus berupa workspace di organisasi yang sama, dan akun layanan target harus menjadi anggota workspace tersebut. |
| `applies_to_all_workspaces`             | Boolean. Atur `true` untuk mengaktifkan aturan di setiap workspace dalam organisasi alih-alih menyebutkan satu. Salah satu dari ini atau `workspace_id` wajib saat pembuatan.                                                                                                                                     |
| `token_lifetime_seconds`                | Integer antara `60` dan `86400` (1 menit hingga 24 jam). Default `3600`. Anthropic menolak nilai di luar rentang ini pada saat permintaan. Lihat [Masa berlaku dan pembaruan token](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#token-lifetime-and-refresh).                   |

### Field URL

Anthropic memvalidasi field `issuer_url`, `jwks.discovery_base`, dan `jwks.url`:

| Batasan | Detail                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Skema   | Harus `https`.                                                                                                                        |
| Port    | Harus `443` (eksplisit atau default).                                                                                                 |
| Host    | Harus berupa hostname DNS publik untuk penyedia OIDC Anda. Harus di-resolve ke alamat IP publik. Anthropic tidak menerima literal IP. |

Kegagalan validasi URL mengembalikan `400 invalid_request_error` dengan nama field sebagai awalan pada pesan error (misalnya, `issuer_url: url must use https scheme`).

<Note>
  Batasan URL hanya berlaku untuk URL yang dihubungi oleh Anthropic. Anthropic tidak pernah mengambil `issuer_url` dalam mode `explicit_url` dan `inline` untuk “JSON Web Key Set” (set kunci web JSON), atau JWKS, maupun dalam mode `discovery` ketika `jwks.discovery_base` diatur. Anthropic hanya membandingkan URL tersebut dengan klaim JWT `iss` sebagai string, sehingga URL tersebut dapat merujuk ke hostname internal atau port non-standar.
</Note>

### Verifikasi JWT

| Batasan                   | Detail                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ukuran maksimum           | JWT `assertion` harus berukuran paling banyak 16 KiB.                                                                                                                                                                                                                                                                                                                                                                     |
| Algoritma penandatanganan | Anthropic hanya menerima algoritma asimetris (keluarga RSA dan ECDSA: ES256, ES384, ES512, RS256, RS384, RS512, PS256, PS384, PS512). Anthropic menolak HMAC (`HS256`, `HS384`, `HS512`) dan `none`.                                                                                                                                                                                                                      |
| ID kunci                  | Header JWT harus membawa `kid` yang cocok dengan kunci di JWKS issuer. Anthropic menolak token tanpa `kid`.                                                                                                                                                                                                                                                                                                               |
| Klaim wajib               | `sub` harus ada. `iat` harus ada dan tidak berada di masa depan. `exp` harus ada dan berada di masa depan.                                                                                                                                                                                                                                                                                                                |
| Sekali pakai              | Assertion yang membawa klaim `jti` hanya dapat ditukarkan sekali untuk setiap penerbit. Anthropic menolak pertukaran berulang dengan `jti` yang sama sebagai replay. Field `check_jti` issuer (diaktifkan secara default) mengontrol pemeriksaan ini. Assertion tanpa klaim `jti` tidak tunduk padanya. Lihat [referensi API penerbit federasi](https://platform.claude.com/docs/id/api/organization/federation/issuers). |
| Masa berlaku maksimum     | Masa berlaku token (`exp` dikurangi `iat`) tidak boleh melebihi maksimum yang dikonfigurasi issuer (1 jam secara default, dapat dikonfigurasi untuk setiap issuer di Claude Console).                                                                                                                                                                                                                                     |
| Selisih jam               | Anthropic menerapkan toleransi 30 detik pada `exp`, `nbf`, dan `iat`.                                                                                                                                                                                                                                                                                                                                                     |

## Semantik pencocokan aturan

Blok `match` aturan federasi menentukan apakah Anthropic menerima JWT yang masuk. JWT harus memenuhi setiap matcher yang terisi. Atur setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition`. Anthropic menolak blok `match` yang hanya berisi `audience` atau tanpa matcher sama sekali. Ini melindungi dari aturan yang akan menerima setiap token dari suatu issuer.

| Matcher          | Tipe                 | Semantik                                                                                                                                                                                                                                                                                                   |
| ---------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subject_prefix` | string               | Pencocokan persis terhadap klaim JWT `sub`. Tanda `*` di akhir menjadikannya pencocokan awalan (nilai `sub` harus diawali dengan karakter sebelum `*`). Peka huruf besar/kecil.                                                                                                                            |
| `audience`       | string               | Klaim JWT `aud` harus berisi string persis ini. Ketika `aud` berupa array, elemen mana pun yang cocok persis memenuhi pemeriksaan.                                                                                                                                                                         |
| `claims`         | map\<string, string> | Setiap kunci adalah nama klaim tingkat atas dan setiap nilai adalah nilai string persis yang diwajibkan. Untuk klaim bersarang, numerik, boolean, atau kompleks seperti list dan map, gunakan `condition` dengan ekspresi “Common Expression Language” (bahasa ekspresi umum), atau CEL, sebagai gantinya. |
| `condition`      | string (CEL)         | Ekspresi [CEL](https://cel.dev/) yang harus dievaluasi menjadi `true`.                                                                                                                                                                                                                                     |

### Lingkungan evaluasi CEL

Ekspresi `condition` memiliki akses ke satu variabel:

| Variabel | Tipe | Isi                                                                                             |
| -------- | ---- | ----------------------------------------------------------------------------------------------- |
| `claims` | map  | Set klaim JWT lengkap yang telah didekode. Objek bersarang dapat diakses sebagai map bersarang. |

Contoh:

```text wrap
claims.sub.startsWith("repo:acme-corp/") && claims.ref in ["refs/heads/main", "refs/heads/release"]
```

<Warning>
  Kondisi CEL adalah batas keamanan. Ekspresi yang dievaluasi menjadi `true` untuk lebih banyak input daripada yang dimaksudkan akan memberikan akses yang lebih luas daripada yang dimaksudkan. Utamakan matcher statis jika matcher tersebut dapat mengekspresikan batasan Anda.
</Warning>

## Error

### Error pertukaran token

`POST /v1/oauth/token` mengembalikan error dalam [bentuk error API](https://platform.claude.com/docs/id/api/errors) standar. SDK melaporkan kegagalan pertukaran sebagai `WorkloadIdentityError` (ruby: `Anthropic::Credentials::WorkloadIdentityError`; go: `error`; java: `UnexpectedStatusCodeException`; csharp: `WorkloadIdentityException`; php: `OAuthException`), yang memberikan status HTTP dan detail error dari body respons. Kecuali di C# dan PHP, SDK juga memberikan ID permintaan: pada error, di header respons exception, atau di pesan error.

| Status | Error                   | Penyebab                                                                                                                                                                                                      | Penyelesaian                                                                                                                                                                                                                                                                                                                                                                                      |
| ------ | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | `invalid_request_error` | `federation_rule_id` salah format atau field permintaan wajib tidak ada.                                                                                                                                      | Periksa ID `fdrl_` dan pastikan body permintaan menyertakan semua field wajib.                                                                                                                                                                                                                                                                                                                    |
| 400    | `invalid_request_error` | `workspace_id` ada tetapi bukan ID `wrkspc_...` yang valid atau literal `default`.                                                                                                                            | Perbaiki nilai `workspace_id`. Pesan respons menyebutkan format yang diharapkan.                                                                                                                                                                                                                                                                                                                  |
| 401    | `authentication_error`  | Klaim JWT `iss` tidak sama persis dengan `issuer_url` yang terdaftar.                                                                                                                                         | Bandingkan byte demi byte, termasuk garis miring di akhir dan skema: `jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' <<< "$JWT"`.                                                                                                                                                                                                                       |
| 401    | `authentication_error`  | Pengambilan JWKS gagal, JWKS sudah usang, atau JWT ditandatangani dengan kunci yang tidak ada di JWKS.                                                                                                        | Untuk mode `inline`, perbarui issuer dengan kunci yang telah dirotasi. Untuk `discovery` dan `explicit_url`, pastikan endpoint JWKS dapat dijangkau di port 443. Jika issuer baru saja merotasi kunci penandatanganannya, lihat [Rotasi kunci dan caching](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching).                                             |
| 401    | `authentication_error`  | Klaim JWT `exp` berada di masa lalu (melampaui jendela skew 30 detik).                                                                                                                                        | Pastikan penyedia identitas Anda memproyeksikan token baru dan SDK membaca ulang file token.                                                                                                                                                                                                                                                                                                      |
| 401    | `authentication_error`  | JWT telah diverifikasi tetapi klaimnya tidak memenuhi blok `match` aturan.                                                                                                                                    | Dekode JWT dan bandingkan setiap klaim dengan aturan. `subject_prefix` peka huruf besar-kecil. `audience` memerlukan pencocokan elemen yang persis.                                                                                                                                                                                                                                               |
| 401    | `authentication_error`  | `federation_rule_id` tidak ada atau telah diarsipkan, atau JWT tidak diotorisasi untuknya (satu error mencakup kasus-kasus ini untuk mencegah enumerasi).                                                     | Konfirmasi ID aturan di Claude Console dan pastikan aturan belum diarsipkan.                                                                                                                                                                                                                                                                                                                      |
| 401    | `authentication_error`  | Aturan federasi diaktifkan untuk semua workspace atau untuk lebih dari satu workspace, dan permintaan tidak menyertakan `workspace_id`. Entri riwayat autentikasi menunjukkan alasan `workspace_id_required`. | Atur `ANTHROPIC_WORKSPACE_ID` (atau field body `workspace_id` pada permintaan mentah) ke ID `wrkspc_...` yang Anda inginkan sebagai cakupan token. Dengan CLI `ant`, atur `workspace_id` dalam profil federasi dan atur `ANTHROPIC_PROFILE` ke nama profil tersebut. Lihat [Permintaan pertukaran token](https://platform.claude.com/docs/id/manage-claude/wif-reference#token-exchange-request). |

Setiap penolakan assertion mengembalikan `401` `authentication_error` opak yang sama dengan pesan tetap `Authentication failed`, terlepas dari pemeriksaan mana yang gagal. Error yang dapat dibedakan akan memungkinkan pemanggil menyelidiki konfigurasi aturan. [Riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console mencatat alasan penolakan pada entri percobaan. Misalnya, riwayat menampilkan `match_subject_prefix` saat klaim `sub` tidak memenuhi `subject_prefix` aturan, atau `workspace_id_required` saat aturan mencakup beberapa workspace dan permintaan tidak menyebutkan satu pun. Permintaan yang ditolak sebelum organisasi aturan dikonfirmasi (keluarga `400 invalid_request_error` di tabel sebelumnya) tidak meninggalkan entri riwayat. Pesan responsnya menyebutkan masalahnya secara langsung. `401` tanpa entri riwayat yang cocok biasanya berarti Anthropic tidak mengenali `federation_rule_id`.

### Kegagalan umum di sisi SDK

| Gejala                                                                   | Penyebab                                                                                                                                                          | Penyelesaian                                                                                                                       |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| SDK melaporkan kredensial yang hilang alih-alih melakukan pertukaran     | Salah satu dari `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, atau `ANTHROPIC_IDENTITY_TOKEN[_FILE]` tidak diatur dan tidak ada profil yang aktif. | Atur ketiga variabel, atau konfigurasikan profil.                                                                                  |
| SDK mengautentikasi dengan kunci API alih-alih melakukan federasi        | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` diatur dan memenangkan prioritas.                                                                                 | Hapus variabel kunci atau token tersebut.                                                                                          |
| Error file tidak ditemukan pada permintaan pertama                       | Path di `ANTHROPIC_IDENTITY_TOKEN_FILE` tidak ada. SDK membuka file secara lazy pada saat pertukaran.                                                             | Pastikan volume token terproyeksi telah di-mount dan path-nya cocok.                                                               |
| Pertukaran token berhasil tetapi permintaan Claude API mengembalikan 403 | Scope token yang dicetak tidak memberikan akses ke endpoint tersebut.                                                                                             | Periksa `oauth_scope` aturan terhadap [Scope OAuth](https://platform.claude.com/docs/id/manage-claude/wif-reference#oauth-scopes). |
| Autentikasi gagal dengan kredensial kosong                               | Variabel lingkungan kredensial diekspor tetapi diatur ke string kosong. Nilai kosong dapat memenangkan slot prioritasnya.                                         | Hapus variabel dengan `unset VAR` alih-alih `VAR=""`.                                                                              |

## Memecahkan masalah pertukaran yang gagal

Respons `401` `authentication_error` sengaja dibuat buram, dan pesannya selalu `Authentication failed`. Alasan penolakan muncul di riwayat autentikasi, bukan di respons.

<Tip>
  Mulailah dengan [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console. Percobaan pertukaran terbaru menampilkan issuer dan aturan yang dievaluasi Anthropic, klaim JWT yang diperiksanya, dan langkah validasi mana yang gagal. Informasi ini biasanya membuat pemeriksaan-pemeriksaan berikut tidak diperlukan.
</Tip>

Salah satu kegagalan buram yang umum adalah assertion yang diputar ulang (replay). Assertion yang membawa klaim `jti` hanya dapat [ditukarkan sekali](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification). Workload yang mengirim ulang JWT yang sama (loop percobaan ulang, atau penyegaran yang membaca ulang token yang belum dirotasi) gagal pada pertukaran kedua. Halaman riwayat autentikasi menampilkan percobaan ini dengan alasan `jti_reused`. Untuk memperbaikinya, cetak assertion baru untuk setiap pertukaran.

Jika Anda perlu melakukan debug dari JWT itu sendiri, lakukan pemeriksaan berikut secara berurutan:

<Steps>
  <Step title="Dekode JWT">
    Dekode assertion yang Anda kirim sehingga Anda dapat membandingkan setiap klaim dengan konfigurasi issuer dan aturan Anda:

    ```bash
    jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson' <<< "$JWT"
    ```
  </Step>

  <Step title="Periksa apakah iss cocok dengan issuer">
    Klaim `iss` yang telah didekode harus sama dengan `issuer_url` yang terdaftar byte demi byte, termasuk skema, port, dan garis miring di akhir. Ketidakcocokan pada satu karakter saja akan menggagalkan verifikasi.
  </Step>

  <Step title="Periksa apakah aud cocok dengan aturan">
    Klaim `aud` yang telah didekode harus berisi nilai `audience` aturan sebagai pencocokan persis. Ketika `aud` berupa array, satu elemen harus cocok persis.
  </Step>

  <Step title="Periksa sub dan setiap entri claims">
    Bandingkan `sub` dengan `subject_prefix` aturan. Perbandingan ini peka huruf besar/kecil. Tanda `*` di akhir menjadikannya pencocokan awalan, dan selain itu adalah pencocokan persis. Bandingkan setiap kunci di map `claims` aturan dengan klaim tingkat atas yang bernama sama.
  </Step>

  <Step title="Periksa exp, nbf, dan iat">
    `exp` harus berada di masa depan dan `nbf`/`iat` harus berada di masa lalu, dalam jendela skew 30 detik. Jika jam host workload telah bergeser, Anthropic menolak token yang sebenarnya valid.
  </Step>

  <Step title="Periksa keterjangkauan JWKS">
    Untuk mode `discovery`, ambil `<jwks.discovery_base or issuer_url>/.well-known/openid-configuration` melalui HTTPS publik di port 443 dan pastikan `jwks_uri` dapat di-resolve. Untuk `explicit_url`, ambil URL JWKS secara langsung. Untuk `inline`, pastikan kunci penandatanganan issuer belum dirotasi sejak Anda mendaftarkan kunci tersebut.

    Jika issuer merotasi kunci penandatanganannya dan segera mulai menandatangani dengannya, pertukaran dapat gagal hingga satu menit selama cache JWKS Anthropic diperbarui. Lihat [Rotasi kunci dan caching](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching).
  </Step>
</Steps>

## Mode sumber JWKS

Ketika Anda mendaftarkan issuer federasi, field `jwks` mengontrol bagaimana Anthropic memperoleh kunci publik yang digunakan untuk memverifikasi tanda tangan JWT dari issuer tersebut. Field `type`-nya memilih mode sumber:

| `jwks.type`           | Bentuk `jwks`                                                                                                                              | Perilaku                                                                                                                                                                                                                  | Gunakan ketika                                                                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery` (default) | `{ "type": "discovery", "discovery_base": "https://..." }` (atur `discovery_base` opsional ketika URL discovery berbeda dari `issuer_url`) | Anthropic mengambil `<discovery_base or issuer_url>/.well-known/openid-configuration`, membaca `jwks_uri` dari dokumen discovery, dan mengambil JWKS dari sana.                                                           | IdP Anda menyajikan dokumen discovery OIDC standar di internet publik. Sebagian besar penyedia terkelola (EKS, GKE, Cloud Run, GitHub Actions, Entra ID) mendukung ini. |
| `explicit_url`        | `{ "type": "explicit_url", "url": "https://..." }`                                                                                         | Anthropic mengambil JWKS langsung dari `url`. Anthropic menggunakan `issuer_url` hanya untuk perbandingan string dengan klaim JWT `iss` dan tidak pernah menghubunginya.                                                  | IdP Anda tidak menyajikan dokumen discovery, atau discovery hanya bersifat internal tetapi JWKS dapat dijangkau secara publik.                                          |
| `inline`              | `{ "type": "inline", "keys": [...] }`                                                                                                      | Anda menyediakan array objek JWK secara inline (array `keys` dari dokumen JWKS, bukan objek pembungkusnya). Anthropic tidak membuat permintaan keluar. Anthropic menggunakan `issuer_url` hanya untuk perbandingan `iss`. | Lingkungan air-gapped, cluster Kubernetes yang dikelola sendiri dengan URL issuer internal cluster, atau ketika Anda menginginkan kontrol eksplisit atas rotasi kunci.  |

Setiap `type` menerima field pendampingnya sendiri, sehingga field-field tersebut saling eksklusif. Baik `discovery` maupun `explicit_url` juga menerima string `ca_cert_pem` opsional untuk issuer yang menyajikan TLS dari CA privat.

### Rotasi kunci dan caching

Dalam mode `discovery` dan `explicit_url`, Anthropic menyimpan cache JWKS yang diambil. Setelah penyedia identitas Anda memublikasikan kunci penandatanganan baru, pertukaran token yang ditandatangani dengannya mungkin gagal dengan error tanda tangan hingga 1 menit selama cache diperbarui.

Untuk menghindari jendela ini, terbitkan kunci penandatanganan baru di JWKS setidaknya 15 menit sebelum penyedia identitas Anda mulai menandatangani token dengannya. Pertahankan kunci yang digantikan di JWKS hingga token yang ditandatanganinya kedaluwarsa. Penyedia identitas terkelola biasanya melakukan hal ini dengan sendirinya. Jika Anda mengoperasikan issuer sendiri, pastikan kebijakan rotasi Anda menerbitkan kunci baru sebelum penggunaan pertama. Contohnya adalah klaster Kubernetes yang dikelola sendiri, penyedia discovery OIDC SPIRE, dan server otorisasi kustom Okta dengan jadwal rotasi yang dikonfigurasi.

<Warning>
  Dalam mode `inline` tidak ada penyegaran kunci otomatis. Ketika penyedia identitas Anda merotasi kunci penandatanganannya, Anda harus memperbarui konfigurasi issuer dengan JWKS baru atau semua pertukaran token gagal dalam verifikasi tanda tangan.
</Warning>
