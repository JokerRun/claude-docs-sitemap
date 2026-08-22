---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: f719aab5f89a69f584de6545c69b1f3351eb3930aae36a66eaa5cd9fb8e78c5c
---

---
title: Referensi WIF
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
description: Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error untuk Workload Identity Federation.
---

Halaman ini mengumpulkan permukaan konfigurasi, batasan validasi, dan pemetaan error untuk [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Untuk panduan penyiapan langkah demi langkah, lihat [panduan penyedia](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers).

## Permintaan pertukaran token

`POST /v1/oauth/token` menerima body JSON menggunakan grant `jwt-bearer` dari [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). SDK membangun permintaan ini untuk Anda dari [variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables); contoh cURL pada setiap panduan penyedia menunjukkan body mentahnya.

| Field                | Wajib     | Deskripsi                                                                                                                                                                                                                                                                                                 |
| -------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`         | Ya        | Selalu `urn:ietf:params:oauth:grant-type:jwt-bearer`.                                                                                                                                                                                                                                                     |
| `assertion`          | Ya        | JWT OIDC yang diterbitkan oleh penyedia identitas Anda.                                                                                                                                                                                                                                                   |
| `federation_rule_id` | Ya        | ID bertag (`fdrl_...`) dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                         |
| `organization_id`    | Ya        | UUID organisasi Anthropic Anda.                                                                                                                                                                                                                                                                           |
| `service_account_id` | Ya        | ID bertag (`svac_...`) dari service account target.                                                                                                                                                                                                                                                       |
| `workspace_id`       | Bersyarat | ID bertag (`wrkspc_...`) dari workspace yang menjadi cakupan token yang dicetak, atau literal `default` untuk workspace default organisasi. Wajib ketika aturan diaktifkan untuk lebih dari satu workspace. Jika dihilangkan, server memilih satu-satunya workspace yang diaktifkan pada aturan tersebut. |

## Respons pertukaran token

`POST /v1/oauth/token` mengembalikan respons token OAuth 2.0 standar ([RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1)):

| Field          | Tipe    | Deskripsi                                                                                                            |
| -------------- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| `access_token` | string  | Token Anthropic berumur pendek, dengan prefiks `sk-ant-oat01-...`. Kirimkan sebagai `Authorization: Bearer <token>`. |
| `token_type`   | string  | Selalu `Bearer`.                                                                                                     |
| `expires_in`   | integer | Detik hingga token kedaluwarsa.                                                                                      |
| `scope`        | string  | Scope OAuth yang diberikan oleh aturan yang cocok.                                                                   |

## Variabel lingkungan

SDK membaca variabel-variabel ini untuk melakukan pertukaran token terfederasi tanpa argumen konstruktor.

| Variabel                        | Wajib                                       | Deskripsi                                                                                                                                                                                                                                                                                                                                            | Contoh                                 |
| ------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `ANTHROPIC_FEDERATION_RULE_ID`  | Ya                                          | ID bertag dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                                                                                 | `fdrl_...`                             |
| `ANTHROPIC_ORGANIZATION_ID`     | Ya                                          | UUID organisasi Anthropic Anda. Temukan di Claude Console pada **Settings > Organization**.                                                                                                                                                                                                                                                          | `00000000-0000-0000-0000-000000000000` |
| `ANTHROPIC_IDENTITY_TOKEN_FILE` | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | Path filesystem ke JWT yang diterbitkan oleh "identity provider" (penyedia identitas) Anda, atau IdP. SDK membaca ulang file ini pada setiap pertukaran sehingga token terproyeksi yang berotasi di disk selalu terkini.                                                                                                                             | `/var/run/secrets/anthropic.com/token` |
| `ANTHROPIC_IDENTITY_TOKEN`      | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | JWT literal sebagai string. Gunakan ketika platform Anda menyuntikkan token sebagai variabel lingkungan alih-alih file.                                                                                                                                                                                                                              | `eyJhbGciOiJSUzI1NiIs...`              |
| `ANTHROPIC_SERVICE_ACCOUNT_ID`  | Ya                                          | ID bertag dari service account Anthropic target yang diperankan oleh access token yang diterbitkan.                                                                                                                                                                                                                                                  | `svac_...`                             |
| `ANTHROPIC_WORKSPACE_ID`        | Bersyarat                                   | ID bertag dari workspace yang menjadi cakupan token yang dicetak, atau literal `default`. Wajib ketika aturan federasi diaktifkan untuk lebih dari satu workspace; opsional ketika aturan terikat pada satu workspace. Token yang dicetak dicakupkan ke workspace ini pada saat pertukaran, sehingga berpindah workspace memerlukan pertukaran baru. | `wrkspc_...`                           |
| `ANTHROPIC_PROFILE`             | Tidak                                       | Nama [profil konfigurasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) yang akan dimuat. Lebih diutamakan daripada variabel lingkungan federasi dalam tabel ini.                                                                                                                                      | `staging-profile`                      |

Jalur federasi variabel-lingkungan langsung hanya aktif ketika `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` semuanya disetel. `ANTHROPIC_WORKSPACE_ID` dibaca bersamaan tetapi tidak menentukan aktivasi.

<Warning>
  Variabel yang disetel ke string kosong tetap menempati slotnya dalam rantai prioritas kredensial. Jika `ANTHROPIC_API_KEY=""` diekspor, SDK memilih jalur kunci API dengan kunci kosong alih-alih meneruskan ke federasi. Hapus (unset) variabel kredensial yang tidak digunakan alih-alih mengosongkannya.
</Warning>

### Prioritas kredensial

SDK menyelesaikan kredensial dalam urutan ini. Sumber pertama yang menghasilkan kredensial yang menang.

| Urutan | Sumber                                                          | Catatan                                                                                                                            |
| ------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1      | Argumen konstruktor (`api_key=`, `auth_token=`, `credentials=`) | Selalu menimpa semua yang lain.                                                                                                    |
| 2      | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN`                 | Membayangi federasi sepenuhnya. Hapus variabel ini saat bermigrasi dari kunci API.                                                 |
| 3      | `ANTHROPIC_PROFILE`                                             | Memuat `<config_dir>/configs/<name>.json`. Profil bernama yang tidak ditemukan adalah error, bukan fall-through.                   |
| 4      | Variabel lingkungan federasi                                    | `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID` + `ANTHROPIC_SERVICE_ACCOUNT_ID` + `ANTHROPIC_IDENTITY_TOKEN[_FILE]`. |
| 5      | Profil aktif                                                    | Diselesaikan dari `<config_dir>/active_config`, dengan fallback ke profil bernama `default`.                                       |

Ketika sebuah profil dimuat, variabel lingkungan mengisi field apa pun yang dihilangkan profil tetapi tidak pernah menimpa field yang disetel profil secara eksplisit. Misalnya, `ANTHROPIC_WORKSPACE_ID` mengisi `workspace_id` hanya ketika profil aktif tidak menyetelnya.

## File konfigurasi profil

Profil adalah file konfigurasi bernama yang dibaca oleh SDK dan CLI `ant`. Profil memungkinkan Anda mengirimkan parameter federasi bersama image container Anda atau berpindah antar lingkungan tanpa mengubah kode.

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

Claude Code dan Claude Agent SDK mematuhi urutan resolusi yang sama ini, sehingga profil federasi yang dikonfigurasi di sini juga mengautentikasi alat-alat tersebut tanpa penyiapan tambahan.

### Tata letak file

| Path                                      | Isi                                                                                                  | Sensitivitas                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `<config_dir>/configs/<profile>.json`     | `version`, blok `authentication`, `organization_id`, `workspace_id`, dan `base_url`.                 | Bukan rahasia. Aman untuk di-commit atau dimasukkan ke dalam image. |
| `<config_dir>/credentials/<profile>.json` | `version`, `access_token` yang di-cache, `expires_at`, dan (untuk login interaktif) `refresh_token`. | Rahasia. Ditulis oleh SDK dengan mode `0600`.                       |

Baik file config maupun file credentials membawa field string `version` tingkat atas dalam format `major.minor` (saat ini `"1.0"`). SDK menulis field ini secara otomatis sehingga rilis mendatang dapat mendeteksi dan memigrasikan format lama; hilangkan field ini saat menulis config secara manual dan SDK akan memperlakukan file tersebut sebagai versi saat ini.

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

Jika `authentication.identity_token` dihilangkan, SDK melakukan fallback ke `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` dari lingkungan.

## Scope OAuth

`oauth_scope` yang Anda setel pada aturan federasi menentukan endpoint Claude API mana yang dapat dipanggil oleh access token yang dicetak.

| Scope                      | Memberikan akses ke                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer`      | Semua endpoint Claude API non-administratif di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models-list), [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dan sesinya, [Files](https://platform.claude.com/docs/id/build-with-claude/files), dan [Skills](https://platform.claude.com/docs/id/build-with-claude/skills-guide). Ini sama dengan akses yang dimiliki kunci API yang diterbitkan untuk workspace yang sama. |
| `workspace:inference`      | Endpoint inferensi di workspace aturan: [Messages](https://platform.claude.com/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](https://platform.claude.com/docs/id/api/models-list), dan [endpoint chat yang kompatibel dengan OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk). Gunakan ini untuk workload yang hanya perlu memanggil Claude dan tidak pernah perlu mengelola Files, Skills, atau sumber daya lainnya.                                                                                                |
| `workspace:manage_tunnels` | [API tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api): membuat, mendaftar, dan mengambil tunnel, mendaftarkan dan mengarsipkan sertifikat CA, menampilkan dan merotasi token tunnel, serta mengarsipkan tunnel. Jendela modal create-tunnel di Console mengunci scope ini ketika Anda membuat aturan darinya.                                                                                                                                                                                                                       |
| `org:admin`                | Akses penuh ke [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) (anggota organisasi, undangan, workspace, kunci API, dan lainnya). Token OAuth `org:admin` hanya dapat membuat atau memodifikasi aturan dengan scope `workspace:developer` atau `workspace:inference`, dan tidak dapat memperbarui issuer yang mendukung aturan dengan scope lain apa pun; lihat [batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).                                                                                       |

Permintaan ke endpoint di luar scope token mengembalikan HTTP 403. Scope yang lebih granular (per sumber daya, atau baca versus tulis) saat ini tidak tersedia.

### Batas izin

`oauth_scope` aturan federasi adalah batas atas: token yang dicetak tidak pernah dapat melampauinya. `organization_role` service account target (`developer` atau `admin`) menentukan scope mana yang dapat diberikan, sehingga aturan yang memberikan `org:admin` harus menargetkan service account dengan `organization_role=admin`. Izin efektif adalah irisan dari scope aturan dan peran service account.

| `oauth_scope` aturan  | `organization_role` service account | Izin efektif                                                                                                                                                                                                                                         |
| --------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer` | `admin`                             | Akses Claude API hanya di workspace aturan. Scope membatasi token di bawah peran.                                                                                                                                                                    |
| `org:admin`           | `admin`                             | Akses Admin API penuh (anggota organisasi, undangan, workspace, kunci API, dan lainnya), dikurangi pengecualian untuk pemanggil OAuth; lihat [batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). |

## Aturan validasi

Anthropic menegakkan batasan ini ketika Anda membuat atau memperbarui issuer dan aturan, serta ketika memverifikasi JWT yang masuk pada saat pertukaran.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Service accounts](https://platform.claude.com/docs/id/api/admin/service_accounts), [referensi API Federation issuers](https://platform.claude.com/docs/id/api/admin/federation_issuers), dan [referensi API Federation rules](https://platform.claude.com/docs/id/api/admin/federation_rules).

### Field sumber daya

| Field                                      | Batasan                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` issuer, aturan, dan service account | Harus cocok dengan `^[a-z0-9-]+$`, panjang 1 hingga 255 karakter.                                                                                                                                                                                                                                                    |
| `workspace_id`                             | Wajib saat pembuatan kecuali `applies_to_all_workspaces` bernilai true. Workspace (`wrkspc_...`) yang kuota, penagihan, dan batas lajunya berlaku untuk token yang dicetak di bawah aturan ini. Harus berupa workspace di organisasi yang sama, dan service account target harus menjadi anggota workspace tersebut. |
| `applies_to_all_workspaces`                | Boolean. Setel `true` untuk mengaktifkan aturan di setiap workspace dalam organisasi alih-alih menyebutkan satu; salah satu dari ini atau `workspace_id` wajib saat pembuatan.                                                                                                                                       |
| `token_lifetime_seconds`                   | Integer antara `60` dan `86400` (1 menit hingga 24 jam). Default `3600`. Nilai di luar rentang ini ditolak pada saat permintaan. Lihat [Masa berlaku token dan refresh](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#token-lifetime-and-refresh).                                  |

### Field URL

Field `issuer_url`, `jwks.discovery_base`, dan `jwks.url` divalidasi:

| Batasan | Detail                                                                                                                       |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Skema   | Harus `https`.                                                                                                               |
| Port    | Harus `443` (eksplisit atau default).                                                                                        |
| Host    | Harus berupa hostname DNS publik untuk penyedia OIDC Anda. Harus ter-resolve ke alamat IP publik; literal IP tidak diterima. |

Kegagalan validasi URL mengembalikan `400 invalid_request_error` dengan nama field sebagai prefiks pada pesan error (misalnya, `issuer_url: url must use https scheme`).

<Note>
  Batasan URL hanya berlaku untuk URL yang dihubungi Anthropic. Dalam mode JWKS `explicit_url` dan `inline`, serta dalam mode `discovery` ketika `jwks.discovery_base` disetel, `issuer_url` dibandingkan dengan klaim `iss` JWT sebagai string dan tidak pernah diambil, sehingga boleh merujuk ke hostname internal atau port non-standar.
</Note>

### Verifikasi JWT

| Batasan                   | Detail                                                                                                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ukuran maksimum           | JWT `assertion` harus berukuran paling besar 16 KiB.                                                                                                                                       |
| Algoritma penandatanganan | Hanya algoritma asimetris (keluarga RSA dan ECDSA: ES256, ES384, ES512, RS256, RS384, RS512, PS256, PS384, PS512) yang diterima. HMAC (`HS256`, `HS384`, `HS512`) dan `none` ditolak.      |
| Key ID                    | Header JWT harus membawa `kid` yang cocok dengan kunci di JWKS issuer. Token tanpa `kid` ditolak.                                                                                          |
| Klaim wajib               | `sub` harus ada. `iat` harus ada dan tidak di masa depan. `exp` harus ada dan di masa depan.                                                                                               |
| Masa berlaku maksimum     | Masa berlaku token (`exp` dikurangi `iat`) tidak boleh melebihi maksimum yang dikonfigurasi pada issuer (1 jam secara default, dapat dikonfigurasi untuk setiap issuer di Claude Console). |
| Selisih jam               | Kelonggaran 30 detik diterapkan pada `exp`, `nbf`, dan `iat`.                                                                                                                              |

## Semantik pencocokan aturan

Blok `match` aturan federasi menentukan apakah JWT yang masuk diterima. Semua field yang terisi dievaluasi dengan semantik AND: JWT harus memenuhi setiap matcher yang terisi. Setidaknya satu dari `subject_prefix`, `claims`, atau `condition` harus disetel; blok `match` yang hanya berisi `audience` (atau tanpa matcher sama sekali) ditolak. Ini mencegah aturan yang akan menerima setiap token dari sebuah issuer.

| Matcher          | Tipe                 | Semantik                                                                                                                                                                                                                                        |
| ---------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subject_prefix` | string               | Pencocokan persis terhadap klaim `sub` JWT. Tanda `*` di akhir menjadikannya pencocokan prefiks (nilai `sub` harus diawali dengan karakter sebelum `*`). Peka huruf besar/kecil.                                                                |
| `audience`       | string               | Klaim `aud` JWT harus berisi string persis ini. Ketika `aud` berupa array, elemen mana pun yang cocok persis memenuhi pemeriksaan.                                                                                                              |
| `claims`         | map\<string, string> | Setiap kunci adalah nama klaim tingkat atas dan setiap nilai adalah nilai string persis yang diwajibkan. Untuk klaim bersarang, numerik, boolean, atau kompleks seperti list dan map, gunakan `condition` dengan ekspresi CEL sebagai gantinya. |
| `condition`      | string (CEL)         | Ekspresi [CEL](https://cel.dev/) yang harus bernilai `true`.                                                                                                                                                                                    |

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
  Kondisi CEL adalah batas keamanan. Ekspresi yang bernilai `true` untuk lebih banyak input daripada yang dimaksudkan memberikan akses yang lebih luas daripada yang dimaksudkan. Utamakan matcher statis ketika matcher tersebut dapat mengekspresikan batasan Anda.
</Warning>

## Error

### Error pertukaran token

`POST /v1/oauth/token` mengembalikan error dalam [bentuk error API](https://platform.claude.com/docs/id/api/errors) standar. SDK membungkus kegagalan pertukaran dalam `FederationExchangeError` bertipe (atau padanannya di bahasa lain) yang mengekspos status HTTP, body respons, dan `request_id`.

| Status | Error                   | Penyebab                                                                                                                                                                      | Penyelesaian                                                                                                                                                                                                                                                                                                                                            |
| ------ | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | `invalid_request_error` | `federation_rule_id` salah format atau field permintaan wajib tidak ada.                                                                                                      | Verifikasi ID `fdrl_` dan bahwa body permintaan menyertakan semua field wajib.                                                                                                                                                                                                                                                                          |
| 400    | `invalid_request_error` | `workspace_id` ada tetapi bukan ID `wrkspc_...` yang terbentuk dengan benar atau literal `default`.                                                                           | Perbaiki nilai `workspace_id`; pesan respons menyebutkan format yang diharapkan.                                                                                                                                                                                                                                                                        |
| 401    | `authentication_error`  | Klaim `iss` JWT tidak sama persis dengan `issuer_url` yang terdaftar.                                                                                                         | Bandingkan byte demi byte, termasuk garis miring di akhir dan skema: `jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' <<< "$JWT"`.                                                                                                                                                                             |
| 401    | `authentication_error`  | Pengambilan JWKS gagal, JWKS usang, atau JWT ditandatangani dengan kunci yang tidak ada di JWKS.                                                                              | Untuk mode `inline`, perbarui issuer dengan kunci yang telah dirotasi. Untuk `discovery` dan `explicit_url`, pastikan endpoint JWKS dapat dijangkau pada port 443; jika issuer baru saja merotasi kunci penandatanganannya, lihat [Rotasi kunci dan caching](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching). |
| 401    | `authentication_error`  | Klaim `exp` JWT berada di masa lalu (melampaui jendela selisih 30 detik).                                                                                                     | Pastikan penyedia identitas Anda memproyeksikan token baru dan SDK membaca ulang file token.                                                                                                                                                                                                                                                            |
| 401    | `authentication_error`  | JWT terverifikasi tetapi klaimnya tidak memenuhi blok `match` aturan.                                                                                                         | Dekode JWT dan bandingkan setiap klaim dengan aturan. `subject_prefix` peka huruf besar/kecil. `audience` memerlukan pencocokan elemen persis.                                                                                                                                                                                                          |
| 401    | `authentication_error`  | `federation_rule_id` tidak ada, diarsipkan, atau JWT tidak diotorisasi untuknya (digabungkan untuk mencegah enumerasi).                                                       | Pastikan ID aturan di Claude Console dan bahwa aturan belum diarsipkan.                                                                                                                                                                                                                                                                                 |
| 401    | `authentication_error`  | Aturan federasi diaktifkan untuk lebih dari satu workspace dan permintaan menghilangkan `workspace_id`. Entri riwayat autentikasi menunjukkan alasan `workspace_id_required`. | Setel `ANTHROPIC_WORKSPACE_ID` (atau field body `workspace_id` pada permintaan mentah) ke ID `wrkspc_...` yang Anda inginkan sebagai cakupan token. Lihat [Permintaan pertukaran token](https://platform.claude.com/docs/id/manage-claude/wif-reference#token-exchange-request).                                                                        |

Setiap penolakan assertion mengembalikan `401` `authentication_error` buram yang sama dengan pesan tetap `Authentication failed`, terlepas dari pemeriksaan mana yang gagal; error yang dapat dibedakan akan memungkinkan pemanggil menyelidiki konfigurasi aturan. Alasan penolakan dicatat pada entri percobaan di [riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history), misalnya `match_subject_prefix` ketika klaim `sub` gagal memenuhi `subject_prefix` aturan, atau `workspace_id_required` ketika aturan mencakup beberapa workspace dan permintaan tidak menyebutkan satu pun. Permintaan yang ditolak sebelum organisasi aturan dikonfirmasi (keluarga `400 invalid_request_error` di atas) tidak meninggalkan entri riwayat; pesan responsnya menyebutkan masalahnya secara langsung. `401` tanpa entri riwayat yang cocok biasanya berarti `federation_rule_id` itu sendiri tidak dikenali.

### Kegagalan umum di sisi SDK

| Gejala                                                                   | Penyebab                                                                                                                                                                                           | Penyelesaian                                                                                                                       |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| SDK melaporkan "no credentials" alih-alih melakukan pertukaran           | Salah satu dari `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, atau `ANTHROPIC_IDENTITY_TOKEN[_FILE]` tidak disetel dan tidak ada profil yang aktif. | Setel keempat variabel, atau konfigurasikan profil.                                                                                |
| SDK mengautentikasi dengan kunci API alih-alih berfederasi               | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` disetel dan memenangkan prioritas.                                                                                                                 | Hapus variabel kunci atau token tersebut.                                                                                          |
| `FileNotFoundError` pada permintaan pertama                              | Path di `ANTHROPIC_IDENTITY_TOKEN_FILE` tidak ada. SDK membuka file secara lazy pada saat pertukaran.                                                                                              | Pastikan volume projected-token terpasang dan path-nya cocok.                                                                      |
| Pertukaran token berhasil tetapi permintaan Claude API mengembalikan 403 | Scope token yang dicetak tidak memberikan akses ke endpoint tersebut.                                                                                                                              | Periksa `oauth_scope` aturan terhadap [Scope OAuth](https://platform.claude.com/docs/id/manage-claude/wif-reference#oauth-scopes). |
| Autentikasi gagal dengan kredensial kosong                               | Variabel lingkungan kredensial diekspor tetapi disetel ke string kosong. Nilai kosong tetap memenangkan slot prioritasnya.                                                                         | Hapus variabel dengan `unset VAR` alih-alih `VAR=""`.                                                                              |

## Memecahkan masalah pertukaran yang gagal

Respons `401` `authentication_error` sengaja dibuat buram dan pesannya selalu `Authentication failed`; alasan penolakan dicatat di riwayat autentikasi, bukan di respons.

<Tip>
  Mulailah dengan [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console. Percobaan pertukaran terbaru menampilkan issuer dan aturan yang dievaluasi, klaim JWT yang diperiksa, dan langkah validasi mana yang gagal, yang biasanya mempersingkat pemeriksaan berikut.
</Tip>

Jika Anda masih perlu melakukan debug dari JWT itu sendiri, lakukan pemeriksaan ini secara berurutan:

<Steps>
  <Step title="Dekode JWT">
    Dekode assertion yang Anda kirim sehingga Anda dapat membandingkan setiap klaim dengan konfigurasi issuer dan aturan Anda:

    ```bash cURL
    jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson' <<< "$JWT"
    ```
  </Step>

  <Step title="Periksa iss cocok dengan issuer">
    Klaim `iss` yang didekode harus sama dengan `issuer_url` yang terdaftar byte demi byte, termasuk skema, port, dan garis miring di akhir jika ada. Ketidakcocokan pada satu karakter saja menggagalkan verifikasi.
  </Step>

  <Step title="Periksa aud cocok dengan aturan">
    Klaim `aud` yang didekode harus berisi nilai `audience` aturan sebagai pencocokan persis. Ketika `aud` berupa array, satu elemen harus cocok persis.
  </Step>

  <Step title="Periksa sub dan setiap entri claims">
    Bandingkan `sub` dengan `subject_prefix` aturan (peka huruf besar/kecil; `*` di akhir adalah pencocokan prefiks, selain itu adalah pencocokan persis). Bandingkan setiap kunci di map `claims` aturan dengan klaim tingkat atas bernama sama.
  </Step>

  <Step title="Periksa exp, nbf, dan iat">
    `exp` harus di masa depan dan `nbf`/`iat` harus di masa lalu, dalam jendela selisih 30 detik. Jika jam host workload telah bergeser, token yang sebenarnya valid akan ditolak.
  </Step>

  <Step title="Periksa keterjangkauan JWKS">
    Untuk mode `discovery`, ambil `<jwks.discovery_base or issuer_url>/.well-known/openid-configuration` melalui HTTPS publik pada port 443 dan pastikan `jwks_uri` ter-resolve. Untuk `explicit_url`, ambil URL JWKS secara langsung. Untuk `inline`, pastikan kunci penandatanganan issuer belum dirotasi sejak Anda mendaftarkan kunci tersebut.

    Jika issuer merotasi kunci penandatanganannya dan langsung mulai menandatangani dengannya, pertukaran dapat gagal hingga satu menit sementara cache JWKS Anthropic diperbarui. Lihat [Rotasi kunci dan caching](https://platform.claude.com/docs/id/manage-claude/wif-reference#key-rotation-and-caching).
  </Step>
</Steps>

## Mode sumber JWKS

Ketika Anda mendaftarkan issuer federasi, field `jwks` mengontrol bagaimana Anthropic memperoleh kunci publik yang digunakan untuk memverifikasi tanda tangan JWT dari issuer tersebut. Field ini adalah discriminated union dengan kunci `type`:

| `jwks.type`           | Bentuk `jwks`                                                                                                                                | Perilaku                                                                                                                                                                                                      | Gunakan ketika                                                                                                                                                          |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery` (default) | `{ "type": "discovery", "discovery_base": "https://..." }` (`discovery_base` opsional; setel ketika URL discovery berbeda dari `issuer_url`) | Anthropic mengambil `<discovery_base or issuer_url>/.well-known/openid-configuration`, membaca `jwks_uri` dari dokumen discovery, dan mengambil JWKS dari sana.                                               | IdP Anda menyajikan dokumen discovery OIDC standar di internet publik. Sebagian besar penyedia terkelola (EKS, GKE, Cloud Run, GitHub Actions, Entra ID) mendukung ini. |
| `explicit_url`        | `{ "type": "explicit_url", "url": "https://..." }`                                                                                           | Anthropic mengambil JWKS langsung dari `url`. `issuer_url` hanya digunakan untuk perbandingan string dengan klaim `iss` JWT dan tidak pernah dihubungi.                                                       | IdP Anda tidak menyajikan dokumen discovery, atau discovery hanya internal tetapi JWKS dapat dijangkau secara publik.                                                   |
| `inline`              | `{ "type": "inline", "keys": [...] }`                                                                                                        | Anda menyediakan array objek JWK secara inline (array `keys` dari dokumen JWKS, bukan objek pembungkusnya). Anthropic tidak membuat permintaan keluar. `issuer_url` hanya digunakan untuk perbandingan `iss`. | Lingkungan air-gapped, cluster Kubernetes yang dikelola sendiri dengan URL issuer internal cluster, atau ketika Anda menginginkan kontrol eksplisit atas rotasi kunci.  |

Discriminated union membuat field pendamping saling eksklusif secara konstruksi. Baik `discovery` maupun `explicit_url` juga menerima string `ca_cert_pem` opsional untuk issuer yang menyajikan TLS dari CA privat.

### Rotasi kunci dan caching

Dalam mode `discovery` dan `explicit_url`, Anthropic menyimpan JWKS yang diambil dalam cache. Jika penyedia identitas Anda memublikasikan kunci penandatanganan baru dan langsung mulai menandatangani token dengannya, pertukaran yang menyajikan token tersebut dapat gagal dengan error tanda tangan hingga 1 menit sementara cache diperbarui.

Untuk menghindari jendela ini, publikasikan kunci penandatanganan baru di JWKS setidaknya 15 menit sebelum penyedia identitas Anda mulai menandatangani token dengannya, dan pertahankan kunci yang digantikan di JWKS hingga token yang ditandatanganinya kedaluwarsa. Penyedia identitas terkelola biasanya mengikuti disiplin ini dengan sendirinya. Jika Anda mengoperasikan issuer sendiri (cluster Kubernetes yang dikelola sendiri, penyedia discovery OIDC SPIRE, atau authorization server kustom Okta dengan irama rotasi yang dikonfigurasi), pastikan kebijakan rotasi Anda memublikasikan kunci baru sebelum penggunaan pertama.

<Warning>
  Dalam mode `inline` tidak ada pembaruan kunci otomatis. Ketika penyedia identitas Anda merotasi kunci penandatanganannya, Anda harus memperbarui konfigurasi issuer dengan JWKS baru atau semua pertukaran token akan gagal verifikasi tanda tangan.
</Warning>
