---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 71e21081778584dcbc9b866e76c9bb4a969c3e87fbeafed4765c98124930ffc1
---

---
title: Referensi WIF
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
description: Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error untuk Workload Identity Federation.
---

Halaman ini mengumpulkan permukaan konfigurasi, batasan validasi, dan pemetaan error untuk [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Untuk panduan langkah demi langkah penyiapan, lihat [panduan penyedia](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers).

## Permintaan pertukaran token

`POST /v1/oauth/token` menerima body JSON menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). SDK membangun permintaan ini untuk Anda dari [variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables); contoh cURL di setiap panduan penyedia menunjukkan body mentahnya.

| Field                | Wajib       | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`         | Ya          | Selalu `urn:ietf:params:oauth:grant-type:jwt-bearer`.                                                                                                                                                                                                                                                                                                                                                 |
| `assertion`          | Ya          | JWT OIDC yang diterbitkan oleh penyedia identitas Anda.                                                                                                                                                                                                                                                                                                                                               |
| `federation_rule_id` | Ya          | ID bertag (`fdrl_...`) dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                                                                                                                     |
| `organization_id`    | Ya          | UUID organisasi Anthropic Anda.                                                                                                                                                                                                                                                                                                                                                                       |
| `service_account_id` | Ya          | ID bertag (`svac_...`) dari akun layanan target.                                                                                                                                                                                                                                                                                                                                                      |
| `workspace_id`       | Kondisional | ID bertag (`wrkspc_...`) dari workspace yang menjadi cakupan token yang dicetak. Wajib ketika aturan diaktifkan untuk lebih dari satu workspace. Jika dihilangkan, server memilih satu-satunya workspace yang diaktifkan untuk aturan tersebut. Literal `default` juga berfungsi untuk Default Workspace organisasi tetapi sudah usang (deprecated); gunakan ID `wrkspc_...` dari workspace tersebut. |

## Respons pertukaran token

`POST /v1/oauth/token` mengembalikan respons token OAuth 2.0 standar ([RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1)):

| Field          | Tipe    | Deskripsi                                                                                                           |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| `access_token` | string  | Token Anthropic berumur pendek, dengan awalan `sk-ant-oat01-...`. Teruskan sebagai `Authorization: Bearer <token>`. |
| `token_type`   | string  | Selalu `Bearer`.                                                                                                    |
| `expires_in`   | integer | Detik hingga token kedaluwarsa.                                                                                     |
| `scope`        | string  | Cakupan OAuth yang diberikan oleh aturan yang cocok.                                                                |

## Variabel lingkungan

SDK membaca variabel-variabel ini untuk melakukan pertukaran token terfederasi tanpa argumen konstruktor.

| Variabel                        | Wajib                                       | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                              | Contoh                                 |
| ------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `ANTHROPIC_FEDERATION_RULE_ID`  | Ya                                          | ID bertag dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                                                                                                                                                                   | `fdrl_...`                             |
| `ANTHROPIC_ORGANIZATION_ID`     | Ya                                          | UUID organisasi Anthropic Anda. Temukan di Claude Console pada **Settings > Organization**.                                                                                                                                                                                                                                                                                                                                            | `00000000-0000-0000-0000-000000000000` |
| `ANTHROPIC_IDENTITY_TOKEN_FILE` | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | Path sistem file ke JWT yang diterbitkan oleh penyedia identitas (IdP) Anda. SDK membaca ulang file ini pada setiap pertukaran sehingga token terproyeksi yang berotasi di disk selalu terkini.                                                                                                                                                                                                                                        | `/var/run/secrets/anthropic.com/token` |
| `ANTHROPIC_IDENTITY_TOKEN`      | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | JWT literal sebagai string. Gunakan ketika platform Anda menyuntikkan token sebagai variabel lingkungan, bukan sebagai file.                                                                                                                                                                                                                                                                                                           | `eyJhbGciOiJSUzI1NiIs...`              |
| `ANTHROPIC_SERVICE_ACCOUNT_ID`  | Ya                                          | ID bertag dari akun layanan Anthropic target yang diwakili oleh token akses yang diterbitkan.                                                                                                                                                                                                                                                                                                                                          | `svac_...`                             |
| `ANTHROPIC_WORKSPACE_ID`        | Kondisional                                 | ID bertag dari workspace yang menjadi cakupan token yang dicetak. Wajib ketika aturan federasi diaktifkan untuk lebih dari satu workspace; opsional ketika aturan terikat pada satu workspace. Token yang dicetak dicakupkan ke workspace ini pada saat pertukaran, sehingga berpindah workspace memerlukan pertukaran baru. Literal `default` juga berfungsi untuk Default Workspace tetapi sudah usang; gunakan ID `wrkspc_...`-nya. | `wrkspc_...`                           |
| `ANTHROPIC_PROFILE`             | Tidak                                       | Nama [profil konfigurasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) yang akan dimuat. Lebih diutamakan daripada variabel lingkungan federasi dalam tabel ini.                                                                                                                                                                                                                        | `staging-profile`                      |

Jalur federasi variabel-lingkungan langsung diaktifkan hanya ketika `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` semuanya diatur. `ANTHROPIC_WORKSPACE_ID` dibaca bersamaan tetapi tidak mengatur aktivasi.

<Warning>
  Variabel yang diatur ke string kosong tetap menempati slotnya dalam rantai prioritas kredensial. Jika `ANTHROPIC_API_KEY=""` diekspor, SDK memilih jalur kunci-API dengan kunci kosong alih-alih jatuh ke federasi. Batalkan pengaturan variabel kredensial yang tidak digunakan alih-alih mengosongkannya.
</Warning>

### Prioritas kredensial

SDK menyelesaikan kredensial dalam urutan ini. Sumber pertama yang menghasilkan kredensial menang.

| Urutan | Sumber                                                          | Catatan                                                                                                                            |
| ------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1      | Argumen konstruktor (`api_key=`, `auth_token=`, `credentials=`) | Selalu menimpa segala sesuatu yang lain.                                                                                           |
| 2      | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN`                 | Membayangi federasi sepenuhnya. Batalkan pengaturan ini saat bermigrasi dari kunci API.                                            |
| 3      | `ANTHROPIC_PROFILE`                                             | Memuat `<config_dir>/configs/<name>.json`. Profil bernama yang hilang adalah error, bukan fall-through.                            |
| 4      | Variabel lingkungan federasi                                    | `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID` + `ANTHROPIC_SERVICE_ACCOUNT_ID` + `ANTHROPIC_IDENTITY_TOKEN[_FILE]`. |
| 5      | Profil aktif                                                    | Diselesaikan dari `<config_dir>/active_config`, jatuh kembali ke profil bernama `default`.                                         |

Ketika profil dimuat, variabel lingkungan mengisi field apa pun yang dihilangkan profil tetapi tidak pernah menimpa field yang diatur profil secara eksplisit. Misalnya, `ANTHROPIC_WORKSPACE_ID` mengisi `workspace_id` hanya ketika profil aktif tidak mengaturnya.

## File konfigurasi profil

Profil adalah file konfigurasi bernama yang dibaca oleh SDK dan CLI `ant`. Profil memungkinkan Anda mengirimkan parameter federasi dengan image kontainer Anda atau beralih antar lingkungan tanpa mengubah kode.

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

Claude Code dan Claude Agent SDK menghormati urutan penyelesaian yang sama ini, sehingga profil federasi yang dikonfigurasi di sini juga mengautentikasi alat-alat tersebut tanpa penyiapan tambahan.

### Tata letak file

| Path                                      | Isi                                                                                                  | Sensitivitas                                                      |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `<config_dir>/configs/<profile>.json`     | `version`, blok `authentication`, `organization_id`, `workspace_id`, dan `base_url`.                 | Non-rahasia. Aman untuk di-commit atau dimasukkan ke dalam image. |
| `<config_dir>/credentials/<profile>.json` | `version`, `access_token` yang di-cache, `expires_at`, dan (untuk login interaktif) `refresh_token`. | Rahasia. Ditulis oleh SDK dengan mode `0600`.                     |

Baik file config maupun file credentials membawa field string `version` tingkat atas dalam format `major.minor` (saat ini `"1.0"`). SDK menulis field ini secara otomatis sehingga rilis mendatang dapat mendeteksi dan memigrasikan format yang lebih lama; hilangkan saat menulis config secara manual dan SDK memperlakukan file sebagai versi saat ini.

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

Jika `authentication.identity_token` dihilangkan, SDK jatuh kembali ke `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` dari lingkungan.

## Cakupan OAuth

`oauth_scope` yang Anda atur pada aturan federasi menentukan endpoint Claude API mana yang dapat dipanggil oleh token akses yang dicetak.

| Cakupan                    | Memberikan akses ke                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer`      | Semua endpoint Claude API non-administratif di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models/list), [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dan sesi mereka, [Files](https://platform.claude.com/docs/id/build-with-claude/files), dan [Skills](https://platform.claude.com/docs/id/build-with-claude/skills-guide). Ini cocok dengan akses yang dimiliki kunci API workspace di workspace yang sama. |
| `workspace:inference`      | Endpoint inferensi di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models/list), dan [endpoint chat yang kompatibel dengan OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk). Gunakan ini untuk beban kerja yang hanya perlu memanggil Claude dan tidak pernah perlu mengelola Files, Skills, atau sumber daya lainnya.                                                                                        |
| `workspace:manage_tunnels` | [API tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api): membuat, mendaftar, dan mendapatkan tunnel, mendaftarkan dan mengarsipkan sertifikat CA, mengungkapkan dan merotasi token tunnel, dan mengarsipkan tunnel. Jendela modal create-tunnel Console mengunci cakupan ini ketika Anda membuat aturan darinya.                                                                                                                                                                                                                 |
| `org:admin`                | Akses penuh ke [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) (anggota organisasi, undangan, workspace, kunci API, dan selebihnya). Token OAuth `org:admin` hanya dapat membuat atau memodifikasi aturan yang dibatasi cakupannya ke `workspace:developer` atau `workspace:inference`, dan tidak dapat memperbarui issuer yang mendukung aturan dengan cakupan lain apa pun; lihat [batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).                                                              |

Permintaan ke endpoint di luar cakupan token mengembalikan HTTP 403. Cakupan yang lebih halus (per sumber daya, atau baca versus tulis) saat ini tidak tersedia.

### Batas izin

`oauth_scope` aturan federasi adalah batas atas: token yang dicetak tidak pernah dapat melampauinya. `organization_role` akun layanan target (`developer` atau `admin`) menentukan cakupan mana yang dapat diberikan, sehingga aturan yang memberikan `org:admin` harus menargetkan akun layanan dengan `organization_role=admin`. Izin efektif adalah irisan dari cakupan aturan dan peran akun layanan.

| `oauth_scope` aturan  | `organization_role` akun layanan | Izin efektif                                                                                                                                                                                                                                      |
| --------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer` | `admin`                          | Akses Claude API hanya di workspace aturan. Cakupan membatasi token di bawah peran.                                                                                                                                                               |
| `org:admin`           | `admin`                          | Akses penuh Admin API (anggota organisasi, undangan, workspace, kunci API, dan selebihnya), dikurangi pengecualian pemanggil OAuth; lihat [batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). |

## Aturan validasi

Anthropic menegakkan batasan-batasan ini ketika Anda membuat atau memperbarui issuer dan aturan, dan ketika memverifikasi JWT yang masuk pada waktu pertukaran.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Service accounts](https://platform.claude.com/docs/id/api/organization/service_accounts), [referensi API Federation issuers](https://platform.claude.com/docs/id/api/organization/federation/issuers), dan [referensi API Federation rules](https://platform.claude.com/docs/id/api/organization/federation/rules).

### Field sumber daya

| Field                                   | Batasan                                                                                                                                                                                                                                                                                                         |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` issuer, aturan, dan akun layanan | Harus cocok dengan `^[a-z0-9-]+$`, panjang 1 hingga 255 karakter.                                                                                                                                                                                                                                               |
| `workspace_id`                          | Wajib saat membuat kecuali `applies_to_all_workspaces` bernilai true. Workspace (`wrkspc_...`) yang kuota, penagihan, dan batas lajunya berlaku untuk token yang dicetak di bawah aturan ini. Harus berupa workspace di organisasi yang sama, dan akun layanan target harus menjadi anggota workspace tersebut. |
| `applies_to_all_workspaces`             | Boolean. Atur `true` untuk mengaktifkan aturan di setiap workspace dalam organisasi alih-alih menamai satu; salah satu dari ini atau `workspace_id` wajib saat membuat.                                                                                                                                         |
| `token_lifetime_seconds`                | Integer antara `60` dan `86400` (1 menit hingga 24 jam). Default `3600`. Nilai di luar rentang ini ditolak pada waktu permintaan. Lihat [Masa pakai dan penyegaran token](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#token-lifetime-and-refresh).                           |

### Field URL

Field `issuer_url`, `jwks.discovery_base`, dan `jwks.url` divalidasi:

| Batasan | Detail                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Skema   | Harus `https`.                                                                                                                 |
| Port    | Harus `443` (eksplisit atau default).                                                                                          |
| Host    | Harus berupa hostname DNS publik untuk penyedia OIDC Anda. Harus menyelesaikan ke alamat IP publik; literal IP tidak diterima. |

Kegagalan validasi URL mengembalikan `400 invalid_request_error` dengan nama field sebagai awalan pada pesan error (misalnya, `issuer_url: url must use https scheme`).

<Note>
  Batasan URL hanya berlaku untuk URL yang dihubungi Anthropic. Dalam mode JWKS `explicit_url` dan `inline`, dan dalam mode `discovery` ketika `jwks.discovery_base` diatur, `issuer_url` dibandingkan dengan klaim `iss` JWT sebagai string dan tidak pernah diambil, sehingga dapat merujuk ke hostname internal atau port non-standar.
</Note>

### Verifikasi JWT

| Batasan                   | Detail                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ukuran maksimum           | JWT `assertion` harus berukuran paling banyak 16 KiB.                                                                                                                                                                                                                                                                                                                                                |
| Algoritma penandatanganan | Hanya algoritma asimetris (keluarga RSA dan ECDSA: ES256, ES384, ES512, RS256, RS384, RS512, PS256, PS384, PS512) yang diterima. HMAC (`HS256`, `HS384`, `HS512`) dan `none` ditolak.                                                                                                                                                                                                                |
| Key ID                    | Header JWT harus membawa `kid` yang cocok dengan kunci di JWKS issuer. Token tanpa `kid` ditolak.                                                                                                                                                                                                                                                                                                    |
| Klaim wajib               | `sub` harus ada. `iat` harus ada dan tidak berada di masa depan. `exp` harus ada dan berada di masa depan.                                                                                                                                                                                                                                                                                           |
| Sekali pakai              | Assertion yang membawa klaim `jti` hanya dapat ditukar sekali per issuer: mengulangi pertukaran dengan `jti` yang sama ditolak sebagai replay. Field `check_jti` issuer (diaktifkan secara default) mengontrol pemeriksaan ini; assertion tanpa klaim `jti` tidak tunduk padanya. Lihat [referensi API Federation issuers](https://platform.claude.com/docs/id/api/organization/federation/issuers). |
| Masa berlaku maksimum     | Masa berlaku token (`exp` dikurangi `iat`) tidak boleh melebihi maksimum yang dikonfigurasi issuer (1 jam secara default, dapat dikonfigurasi untuk setiap issuer di Claude Console).                                                                                                                                                                                                                |
| Selisih jam               | Toleransi 30 detik diterapkan pada `exp`, `nbf`, dan `iat`.                                                                                                                                                                                                                                                                                                                                          |

## Semantik pencocokan aturan

Blok `match` aturan federasi menentukan apakah JWT yang masuk diterima. Semua field yang terisi dievaluasi dengan semantik AND: JWT harus memenuhi setiap matcher yang terisi. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur; blok `match` yang hanya berisi `audience` (atau tidak ada matcher sama sekali) ditolak. Ini melindungi dari aturan yang akan menerima setiap token dari issuer.

| Matcher          | Tipe                 | Semantik                                                                                                                                                                                                                                        |
| ---------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subject_prefix` | string               | Pencocokan persis terhadap klaim `sub` JWT. `*` di akhir menjadikannya pencocokan awalan (nilai `sub` harus dimulai dengan karakter sebelum `*`). Peka huruf besar-kecil.                                                                       |
| `audience`       | string               | Klaim `aud` JWT harus berisi string persis ini. Ketika `aud` adalah array, elemen apa pun yang cocok persis memenuhi pemeriksaan.                                                                                                               |
| `claims`         | map\<string, string> | Setiap kunci adalah nama klaim tingkat atas dan setiap nilai adalah nilai string persis yang diperlukan. Untuk klaim bersarang, numerik, boolean, atau kompleks seperti list dan map, gunakan `condition` dengan ekspresi CEL sebagai gantinya. |
| `condition`      | string (CEL)         | Ekspresi [CEL](https://cel.dev/) yang harus dievaluasi menjadi `true`.                                                                                                                                                                          |

### Lingkungan evaluasi CEL

Ekspresi `condition` memiliki akses ke satu variabel:

| Variabel | Tipe | Isi                                                                                     |
| -------- | ---- | --------------------------------------------------------------------------------------- |
| `claims` | map  | Set klaim JWT yang didekode penuh. Objek bersarang dapat diakses sebagai map bersarang. |

Contoh:

```text wrap
claims.sub.startsWith("repo:acme-corp/") && claims.ref in ["refs/heads/main", "refs/heads/release"]
```

<Warning>
  Kondisi CEL adalah batas keamanan. Ekspresi yang dievaluasi menjadi `true` untuk lebih banyak input daripada yang dimaksudkan memberikan akses yang lebih luas daripada yang dimaksudkan. Lebih baik gunakan matcher statis ketika mereka mengekspresikan batasan Anda.
</Warning>

## Error

### Error pertukaran token

`POST /v1/oauth/token` mengembalikan error dalam [bentuk error API](https://platform.claude.com/docs/id/api/errors) standar. SDK membungkus kegagalan pertukaran dalam `WorkloadIdentityError` (python, typescript; ruby: `Anthropic::Credentials::WorkloadIdentityError`; go: `*config.FederationExchangeError`; java: `UnexpectedStatusCodeException`; csharp: `WorkloadIdentityException`; php: `OAuthException`) bertipe yang mengekspos status HTTP, body respons, dan `request_id`.

| Status | Error                   | Penyebab                                                                                                                                                                      | Resolusi                                                                                                                                                                                                                                                                                                                                                |
| ------ | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | `invalid_request_error` | `federation_rule_id` salah bentuk atau field permintaan yang diperlukan hilang.                                                                                               | Verifikasi ID `fdrl_` dan bahwa body permintaan menyertakan semua field yang diperlukan.                                                                                                                                                                                                                                                                |
| 400    | `invalid_request_error` | `workspace_id` ada tetapi bukan ID `wrkspc_...` yang terbentuk dengan baik atau literal `default`.                                                                            | Perbaiki nilai `workspace_id`; pesan respons menamai format yang diharapkan.                                                                                                                                                                                                                                                                            |
| 401    | `authentication_error`  | Klaim `iss` JWT tidak sama persis dengan `issuer_url` yang terdaftar.                                                                                                         | Bandingkan byte demi byte, termasuk garis miring di akhir dan skema: `jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' <<< "$JWT"`.                                                                                                                                                                             |
| 401    | `authentication_error`  | Pengambilan JWKS gagal, JWKS usang, atau JWT ditandatangani dengan kunci yang tidak ada di JWKS.                                                                              | Untuk mode `inline`, perbarui issuer dengan kunci yang dirotasi. Untuk `discovery` dan `explicit_url`, konfirmasi endpoint JWKS dapat dijangkau pada port 443; jika issuer baru-baru ini merotasi kunci penandatanganannya, lihat [Rotasi dan caching kunci](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching). |
| 401    | `authentication_error`  | Klaim `exp` JWT di masa lalu (melampaui jendela skew 30 detik).                                                                                                               | Konfirmasi penyedia identitas Anda memproyeksikan token segar dan SDK membaca ulang file token.                                                                                                                                                                                                                                                         |
| 401    | `authentication_error`  | JWT diverifikasi tetapi klaimnya tidak memenuhi blok `match` aturan.                                                                                                          | Dekode JWT dan bandingkan setiap klaim terhadap aturan. `subject_prefix` peka huruf besar-kecil. `audience` memerlukan pencocokan elemen persis.                                                                                                                                                                                                        |
| 401    | `authentication_error`  | `federation_rule_id` tidak ada, diarsipkan, atau JWT tidak diotorisasi untuknya (dikonsolidasikan untuk mencegah enumerasi).                                                  | Konfirmasi ID aturan di Claude Console dan bahwa aturan belum diarsipkan.                                                                                                                                                                                                                                                                               |
| 401    | `authentication_error`  | Aturan federasi diaktifkan untuk lebih dari satu workspace dan permintaan menghilangkan `workspace_id`. Entri riwayat autentikasi menunjukkan alasan `workspace_id_required`. | Atur `ANTHROPIC_WORKSPACE_ID` (atau field body `workspace_id` pada permintaan mentah) ke ID `wrkspc_...` yang Anda inginkan untuk membatasi cakupan token. Lihat [Permintaan pertukaran token](https://platform.claude.com/docs/id/manage-claude/wif-reference#token-exchange-request).                                                                 |

Setiap penolakan assertion mengembalikan `401` `authentication_error` buram yang sama dengan pesan tetap `Authentication failed`, terlepas dari pemeriksaan mana yang gagal; error yang dapat dibedakan akan memungkinkan pemanggil menyelidiki konfigurasi aturan. Alasan penolakan dicatat pada entri percobaan di [riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history), misalnya `match_subject_prefix` ketika klaim `sub` gagal pada `subject_prefix` aturan, atau `workspace_id_required` ketika aturan mencakup beberapa workspace dan permintaan tidak menamai satu pun. Permintaan yang ditolak sebelum organisasi aturan dikuatkan (keluarga `400 invalid_request_error` di atas) tidak meninggalkan entri riwayat; pesan respons mereka menamai masalah secara langsung. `401` tanpa entri riwayat yang cocok biasanya berarti `federation_rule_id` itu sendiri tidak dikenali.

### Kegagalan umum di sisi SDK

| Gejala                                                                   | Penyebab                                                                                                                                                                                          | Resolusi                                                                                                                             |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| SDK melaporkan "no credentials" alih-alih menukar                        | Salah satu dari `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, atau `ANTHROPIC_IDENTITY_TOKEN[_FILE]` tidak diatur dan tidak ada profil yang aktif. | Atur keempat variabel, atau konfigurasikan profil.                                                                                   |
| SDK mengautentikasi dengan kunci API alih-alih berfederasi               | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` diatur dan memenangkan prioritas.                                                                                                                 | Batalkan pengaturan variabel kunci atau token.                                                                                       |
| `FileNotFoundError` pada permintaan pertama                              | Path di `ANTHROPIC_IDENTITY_TOKEN_FILE` tidak ada. SDK membuka file secara lazy pada waktu pertukaran.                                                                                            | Konfirmasi volume token yang diproyeksikan terpasang dan path cocok.                                                                 |
| Pertukaran token berhasil tetapi permintaan Claude API mengembalikan 403 | Cakupan token yang dicetak tidak memberikan akses ke endpoint tersebut.                                                                                                                           | Periksa `oauth_scope` aturan terhadap [Cakupan OAuth](https://platform.claude.com/docs/id/manage-claude/wif-reference#oauth-scopes). |
| Autentikasi gagal dengan kredensial kosong                               | Variabel lingkungan kredensial diekspor tetapi diatur ke string kosong. Nilai kosong tetap memenangkan slot prioritasnya.                                                                         | Batalkan pengaturan variabel dengan `unset VAR` alih-alih `VAR=""`.                                                                  |

## Memecahkan masalah pertukaran yang gagal

Respons `401` `authentication_error` sengaja dibuat buram dan pesannya selalu `Authentication failed`; alasan penolakan dicatat dalam riwayat autentikasi, bukan dalam respons.

<Tip>
  Mulailah dengan [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console. Percobaan pertukaran terbaru menampilkan issuer dan aturan yang dievaluasi, klaim JWT yang diperiksa, dan langkah validasi mana yang gagal, yang biasanya memotong pemeriksaan berikut.
</Tip>

Satu kegagalan buram yang umum adalah assertion yang di-replay: assertion yang membawa klaim `jti` hanya dapat [ditukar sekali](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification), sehingga beban kerja yang mengirim ulang JWT yang sama (loop retry, atau penyegaran yang membaca ulang token yang tidak dirotasi) ditolak pada pertukaran kedua. Halaman riwayat autentikasi menunjukkan percobaan ini dengan alasan `jti_reused`; perbaikannya adalah mencetak assertion segar untuk setiap pertukaran.

Jika Anda masih perlu men-debug dari JWT itu sendiri, kerjakan pemeriksaan ini secara berurutan:

<Steps>
  <Step title="Dekode JWT">
    Dekode assertion yang Anda kirim sehingga Anda dapat membandingkan setiap klaim terhadap konfigurasi issuer dan aturan Anda:

    ```bash cURL
    jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson' <<< "$JWT"
    ```
  </Step>

  <Step title="Periksa iss cocok dengan issuer">
    Klaim `iss` yang didekode harus sama dengan `issuer_url` yang terdaftar byte demi byte, termasuk skema, port, dan garis miring di akhir apa pun. Ketidakcocokan pada satu karakter menggagalkan verifikasi.
  </Step>

  <Step title="Periksa aud cocok dengan aturan">
    Klaim `aud` yang didekode harus berisi nilai `audience` aturan sebagai pencocokan persis. Ketika `aud` adalah array, satu elemen harus cocok persis.
  </Step>

  <Step title="Periksa sub dan setiap entri claims">
    Bandingkan `sub` terhadap `subject_prefix` aturan (peka huruf besar-kecil; `*` di akhir adalah pencocokan awalan, selain itu persis). Bandingkan setiap kunci dalam map `claims` aturan terhadap klaim tingkat atas dengan nama yang sama.
  </Step>

  <Step title="Periksa exp, nbf, dan iat">
    `exp` harus di masa depan dan `nbf`/`iat` harus di masa lalu, dalam jendela skew 30 detik. Jika jam host beban kerja telah bergeser, token yang sebaliknya valid ditolak.
  </Step>

  <Step title="Periksa keterjangkauan JWKS">
    Untuk mode `discovery`, ambil `<jwks.discovery_base or issuer_url>/.well-known/openid-configuration` melalui HTTPS publik pada port 443 dan konfirmasi `jwks_uri` menyelesaikan. Untuk `explicit_url`, ambil URL JWKS secara langsung. Untuk `inline`, konfirmasi kunci penandatanganan issuer belum dirotasi sejak Anda mendaftarkan kunci.

    Jika issuer merotasi kunci penandatanganannya dan segera mulai menandatangani dengannya, pertukaran dapat gagal hingga satu menit sementara cache JWKS Anthropic menyegarkan. Lihat [Rotasi dan caching kunci](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching).
  </Step>
</Steps>

## Mode sumber JWKS

Ketika Anda mendaftarkan issuer federasi, field `jwks` mengontrol bagaimana Anthropic memperoleh kunci publik yang digunakan untuk memverifikasi tanda tangan JWT dari issuer tersebut. Ini adalah union terdiskriminasi yang dikunci pada `type`:

| `jwks.type`           | Bentuk `jwks`                                                                                                                               | Perilaku                                                                                                                                                                                                   | Gunakan ketika                                                                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery` (default) | `{ "type": "discovery", "discovery_base": "https://..." }` (`discovery_base` opsional; atur ketika URL discovery berbeda dari `issuer_url`) | Anthropic mengambil `<discovery_base or issuer_url>/.well-known/openid-configuration`, membaca `jwks_uri` dari dokumen discovery, dan mengambil JWKS dari sana.                                            | IdP Anda menyajikan dokumen discovery OIDC standar di internet publik. Sebagian besar penyedia terkelola (EKS, GKE, Cloud Run, GitHub Actions, Entra ID) mendukung ini. |
| `explicit_url`        | `{ "type": "explicit_url", "url": "https://..." }`                                                                                          | Anthropic mengambil JWKS langsung dari `url`. `issuer_url` hanya digunakan untuk perbandingan string terhadap klaim `iss` JWT dan tidak pernah dihubungi.                                                  | IdP Anda tidak menyajikan dokumen discovery, atau discovery hanya internal tetapi JWKS dapat dijangkau secara publik.                                                   |
| `inline`              | `{ "type": "inline", "keys": [...] }`                                                                                                       | Anda menyediakan array objek JWK secara inline (array `keys` dari dokumen JWKS, bukan objek pembungkus). Anthropic tidak membuat permintaan keluar. `issuer_url` hanya digunakan untuk perbandingan `iss`. | Lingkungan air-gapped, cluster Kubernetes yang dikelola sendiri dengan URL issuer internal-cluster, atau ketika Anda menginginkan kontrol eksplisit atas rotasi kunci.  |

Union terdiskriminasi membuat field pendamping saling eksklusif secara konstruksi. Baik `discovery` maupun `explicit_url` juga menerima string `ca_cert_pem` opsional untuk issuer yang menyajikan TLS dari CA privat.

### Rotasi dan caching kunci

Dalam mode `discovery` dan `explicit_url`, Anthropic meng-cache JWKS yang diambil. Jika penyedia identitas Anda menerbitkan kunci penandatanganan baru dan segera mulai menandatangani token dengannya, pertukaran yang menyajikan token tersebut dapat gagal dengan error tanda tangan hingga 1 menit sementara cache menyegarkan.

Untuk menghindari jendela ini, terbitkan kunci penandatanganan baru di JWKS setidaknya 15 menit sebelum penyedia identitas Anda mulai menandatangani token dengannya, dan pertahankan kunci yang digantikan di JWKS hingga token yang ditandatanganinya kedaluwarsa. Penyedia identitas terkelola biasanya mengikuti disiplin ini sendiri. Jika Anda mengoperasikan issuer Anda sendiri (cluster Kubernetes yang dikelola sendiri, penyedia discovery OIDC SPIRE, atau server otorisasi kustom Okta dengan irama rotasi yang dikonfigurasi), konfirmasi bahwa kebijakan rotasi Anda menerbitkan kunci baru sebelum penggunaan pertama.

<Warning>
  Dalam mode `inline` tidak ada penyegaran kunci otomatis. Ketika penyedia identitas Anda merotasi kunci penandatanganannya, Anda harus memperbarui konfigurasi issuer dengan JWKS baru atau semua pertukaran token akan gagal verifikasi tanda tangan.
</Warning>
