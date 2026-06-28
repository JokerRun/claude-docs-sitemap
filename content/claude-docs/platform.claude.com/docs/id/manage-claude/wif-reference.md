---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-reference
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: ab0ff1fdea6f012d1c9e27971b02bb6760be46d9aa6a0a0ad89424b80c7f5716
---

# Referensi WIF

Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi kesalahan untuk Workload Identity Federation.

---

Halaman ini mengumpulkan permukaan konfigurasi, batasan validasi, dan pemetaan kesalahan untuk [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation). Untuk panduan penyiapan, lihat [panduan penyedia](/docs/id/manage-claude/workload-identity-federation#identity-providers).

## Permintaan pertukaran token

`POST /v1/oauth/token` menerima body JSON menggunakan grant `jwt-bearer` dari [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). SDK membangun permintaan ini untuk Anda dari [variabel lingkungan](#environment-variables); contoh cURL pada setiap panduan penyedia menunjukkan body mentahnya.

| Field                | Wajib       | Deskripsi                                                                                                                                                                                                                                                                                                       |
| -------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`         | Ya          | Selalu `urn:ietf:params:oauth:grant-type:jwt-bearer`.                                                                                                                                                                                                                                                           |
| `assertion`          | Ya          | JWT OIDC yang diterbitkan oleh penyedia identitas Anda.                                                                                                                                                                                                                                                         |
| `federation_rule_id` | Ya          | ID bertag (`fdrl_...`) dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                               |
| `organization_id`    | Ya          | UUID organisasi Anthropic Anda.                                                                                                                                                                                                                                                                                 |
| `service_account_id` | Ya          | ID bertag (`svac_...`) dari akun layanan target.                                                                                                                                                                                                                                                                |
| `workspace_id`       | Kondisional | ID bertag (`wrkspc_...`) dari workspace tempat token yang diterbitkan akan dicakupkan, atau literal `default` untuk workspace default organisasi. Wajib ketika aturan diaktifkan untuk lebih dari satu workspace. Jika dihilangkan, server memilih satu-satunya workspace yang diaktifkan pada aturan tersebut. |

## Respons pertukaran token

`POST /v1/oauth/token` mengembalikan respons token OAuth 2.0 standar ([RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1)):

| Field          | Tipe    | Deskripsi                                                                                                            |
| -------------- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| `access_token` | string  | Token Anthropic berumur pendek, dengan prefiks `sk-ant-oat01-...`. Kirimkan sebagai `Authorization: Bearer <token>`. |
| `token_type`   | string  | Selalu `Bearer`.                                                                                                     |
| `expires_in`   | integer | Jumlah detik hingga token kedaluwarsa.                                                                               |
| `scope`        | string  | Scope OAuth yang diberikan oleh aturan yang cocok.                                                                   |

## Variabel lingkungan

SDK membaca variabel-variabel ini untuk melakukan pertukaran token terfederasi tanpa argumen konstruktor.

| Variabel                        | Wajib                                       | Deskripsi                                                                                                                                                                                                                                                                                                                                                    | Contoh                                 |
| ------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| `ANTHROPIC_FEDERATION_RULE_ID`  | Ya                                          | ID bertag dari aturan federasi yang akan dievaluasi.                                                                                                                                                                                                                                                                                                         | `fdrl_...`                             |
| `ANTHROPIC_ORGANIZATION_ID`     | Ya                                          | UUID organisasi Anthropic Anda. Temukan di Claude Console pada **Settings > Organization**.                                                                                                                                                                                                                                                                  | `00000000-0000-0000-0000-000000000000` |
| `ANTHROPIC_IDENTITY_TOKEN_FILE` | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | Path filesystem ke JWT yang diterbitkan oleh "identity provider" (penyedia identitas), atau IdP, Anda. SDK membaca ulang file ini pada setiap pertukaran sehingga token yang diproyeksikan dan dirotasi di disk selalu terkini.                                                                                                                              | `/var/run/secrets/anthropic.com/token` |
| `ANTHROPIC_IDENTITY_TOKEN`      | Salah satu dari `_TOKEN_FILE` atau `_TOKEN` | JWT literal sebagai string. Gunakan ketika platform Anda menyuntikkan token sebagai variabel lingkungan alih-alih file.                                                                                                                                                                                                                                      | `eyJhbGciOiJSUzI1NiIs...`              |
| `ANTHROPIC_SERVICE_ACCOUNT_ID`  | Ya                                          | ID bertag dari akun layanan Anthropic target yang akan diwakili oleh access token yang diterbitkan.                                                                                                                                                                                                                                                          | `svac_...`                             |
| `ANTHROPIC_WORKSPACE_ID`        | Kondisional                                 | ID bertag dari workspace tempat token yang diterbitkan akan dicakupkan, atau literal `default`. Wajib ketika aturan federasi diaktifkan untuk lebih dari satu workspace; opsional ketika aturan terikat pada satu workspace. Token yang diterbitkan dicakupkan ke workspace ini pada saat pertukaran, sehingga beralih workspace memerlukan pertukaran baru. | `wrkspc_...`                           |
| `ANTHROPIC_PROFILE`             | Tidak                                       | Nama [profil konfigurasi](#profile-configuration-file) yang akan dimuat. Lebih diutamakan daripada variabel lingkungan federasi dalam tabel ini.                                                                                                                                                                                                             | `staging-profile`                      |

Jalur federasi melalui variabel lingkungan langsung hanya aktif ketika `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan salah satu dari `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` semuanya diatur. `ANTHROPIC_WORKSPACE_ID` dibaca bersamaan tetapi tidak menjadi syarat aktivasi.

<Warning>
  Variabel yang diatur ke string kosong tetap menempati slotnya dalam rantai prioritas kredensial. Jika `ANTHROPIC_API_KEY=""` diekspor, SDK memilih jalur kunci API dengan kunci kosong alih-alih jatuh ke federasi. Hapus (unset) variabel kredensial yang tidak digunakan alih-alih mengosongkannya.
</Warning>

### Prioritas kredensial

SDK menyelesaikan kredensial dalam urutan ini. Sumber pertama yang menghasilkan kredensial akan menang.

| Urutan | Sumber                                                          | Catatan                                                                                                                            |
| ------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1      | Argumen konstruktor (`api_key=`, `auth_token=`, `credentials=`) | Selalu mengesampingkan yang lainnya.                                                                                               |
| 2      | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN`                 | Membayangi federasi sepenuhnya. Hapus variabel ini saat bermigrasi dari kunci API.                                                 |
| 3      | `ANTHROPIC_PROFILE`                                             | Memuat `<config_dir>/configs/<name>.json`. Profil bernama yang tidak ditemukan adalah kesalahan, bukan fall-through.               |
| 4      | Variabel lingkungan federasi                                    | `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID` + `ANTHROPIC_SERVICE_ACCOUNT_ID` + `ANTHROPIC_IDENTITY_TOKEN[_FILE]`. |
| 5      | Profil aktif                                                    | Diselesaikan dari `<config_dir>/active_config`, dengan fallback ke profil bernama `default`.                                       |

Ketika sebuah profil dimuat, variabel lingkungan mengisi field apa pun yang dihilangkan oleh profil tetapi tidak pernah menimpa field yang diatur secara eksplisit oleh profil. Misalnya, `ANTHROPIC_WORKSPACE_ID` mengisi `workspace_id` hanya ketika profil aktif tidak mengaturnya.

## File konfigurasi profil

Profil adalah file konfigurasi bernama yang dibaca oleh SDK dan CLI `ant`. Profil memungkinkan Anda mengirimkan parameter federasi bersama image container Anda atau beralih antar lingkungan tanpa mengubah kode.

### Direktori konfigurasi

SDK menemukan direktori konfigurasi dalam urutan ini:

1. `$ANTHROPIC_CONFIG_DIR`
2. `~/.config/anthropic` pada Linux dan macOS
3. `%APPDATA%\Anthropic` pada Windows

### Profil aktif

Nama profil aktif diselesaikan dalam urutan ini:

1. `$ANTHROPIC_PROFILE`
2. Isi dari `<config_dir>/active_config` (file satu baris yang ditulis oleh `ant profile activate <name>`)
3. Nama literal `default`

Claude Code dan Claude Agent SDK mengikuti urutan resolusi yang sama ini, sehingga profil federasi yang dikonfigurasi di sini juga mengautentikasi alat-alat tersebut tanpa penyiapan tambahan.

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

Jika `authentication.identity_token` dihilangkan, SDK akan jatuh kembali ke `ANTHROPIC_IDENTITY_TOKEN_FILE` atau `ANTHROPIC_IDENTITY_TOKEN` dari lingkungan.

## Scope OAuth

`oauth_scope` yang Anda atur pada aturan federasi menentukan endpoint Claude API mana yang dapat dipanggil oleh access token yang diterbitkan.

| Scope                 | Memberikan akses ke                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer` | Semua endpoint Claude API non-administratif di workspace aturan: [Messages](/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](/docs/id/api/models-list), [Managed Agents](/docs/id/managed-agents/overview) dan sesinya, [Files](/docs/id/build-with-claude/files), dan [Skills](/docs/id/build-with-claude/skills-guide). Ini setara dengan akses yang dimiliki kunci API yang diterbitkan untuk workspace yang sama. |
| `workspace:inference` | Endpoint inferensi di workspace aturan: [Messages](/docs/id/api/messages) (termasuk streaming dan penghitungan token), [Models](/docs/id/api/models-list), dan [endpoint chat yang kompatibel dengan OpenAI](/docs/id/cli-sdks-libraries/libraries/openai-sdk). Gunakan ini untuk beban kerja yang hanya perlu memanggil Claude dan tidak pernah perlu mengelola Files, Skills, atau sumber daya lainnya.                                         |
| `org:manage_tunnels`  | [API tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api): mendaftar dan mendapatkan tunnel, mendaftarkan dan mengarsipkan sertifikat CA, mengungkap dan merotasi token tunnel, serta mengarsipkan tunnel. Modal create-tunnel di Console mengunci scope ini ketika Anda membuat aturan dari sana.                                                                                                                            |
| `org:admin`           | Akses penuh ke [Admin API](/docs/id/manage-claude/admin-api) (anggota organisasi, undangan, workspace, kunci API, dan lainnya). Token OAuth `org:admin` hanya dapat membuat atau memodifikasi aturan yang dicakupkan ke `workspace:developer` atau `workspace:inference`, dan tidak dapat memperbarui issuer yang mendukung aturan dengan scope lain; lihat [batasan](/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).          |

Permintaan ke endpoint di luar scope token mengembalikan HTTP 403. Scope yang lebih terperinci (per sumber daya, atau baca versus tulis) saat ini tidak tersedia.

### Batas izin

`oauth_scope` pada aturan federasi adalah batas atas: token yang diterbitkan tidak pernah dapat melampauinya. `organization_role` akun layanan target (`developer` atau `admin`) menentukan scope mana yang dapat diberikan, sehingga aturan yang memberikan `org:admin` harus menargetkan akun layanan dengan `organization_role=admin`. Izin efektif adalah irisan dari scope aturan dan peran akun layanan.

| `oauth_scope` aturan  | `organization_role` akun layanan | Izin efektif                                                                                                                                                                                                        |
| --------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer` | `admin`                          | Akses Claude API hanya di workspace aturan. Scope membatasi token di bawah peran.                                                                                                                                   |
| `org:admin`           | `admin`                          | Akses Admin API penuh (anggota organisasi, undangan, workspace, kunci API, dan lainnya), dikurangi pengecualian pemanggil OAuth; lihat [batasan](/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). |

## Aturan validasi

Anthropic menerapkan batasan-batasan ini ketika Anda membuat atau memperbarui issuer dan aturan, serta saat memverifikasi JWT yang masuk pada waktu pertukaran.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Service accounts](/docs/id/api/admin/service_accounts), [referensi API Federation issuers](/docs/id/api/admin/federation_issuers), dan [referensi API Federation rules](/docs/id/api/admin/federation_rules).

### Field sumber daya

| Field                                        | Batasan                                                                                                                                                                                                                                                                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name` pada issuer, aturan, dan akun layanan | Harus cocok dengan `^[a-z0-9-]+$`, panjang 1 hingga 255 karakter.                                                                                                                                                                                                                                                        |
| `workspace_id`                               | Wajib saat pembuatan kecuali `applies_to_all_workspaces` bernilai true. Workspace (`wrkspc_...`) yang kuota, penagihan, dan batas lajunya berlaku untuk token yang diterbitkan di bawah aturan ini. Harus berupa workspace dalam organisasi yang sama, dan akun layanan target harus menjadi anggota workspace tersebut. |
| `applies_to_all_workspaces`                  | Boolean. Atur `true` untuk mengaktifkan aturan di setiap workspace dalam organisasi alih-alih menyebutkan satu; salah satu dari ini atau `workspace_id` wajib saat pembuatan.                                                                                                                                            |
| `token_lifetime_seconds`                     | Integer antara `60` dan `86400` (1 menit hingga 24 jam). Default `3600`. Nilai di luar rentang ini ditolak pada waktu permintaan. Lihat [Masa hidup dan penyegaran token](/docs/id/manage-claude/workload-identity-federation#token-lifetime-and-refresh).                                                               |

### Field URL

Field `issuer_url`, `jwks.discovery_base`, dan `jwks.url` divalidasi:

| Batasan | Detail                                                                                                                       |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Skema   | Harus `https`.                                                                                                               |
| Port    | Harus `443` (eksplisit atau default).                                                                                        |
| Host    | Harus berupa nama host DNS publik untuk penyedia OIDC Anda. Harus me-resolve ke alamat IP publik; literal IP tidak diterima. |

Kegagalan validasi URL mengembalikan `400 invalid_request_error` dengan nama field sebagai prefiks pada pesan kesalahan (misalnya, `issuer_url: url must use https scheme`).

<Note>
  Batasan URL hanya berlaku untuk URL yang dihubungi oleh Anthropic. Dalam mode JWKS `explicit_url` dan `inline`, serta dalam mode `discovery` ketika `jwks.discovery_base` diatur, `issuer_url` dibandingkan dengan klaim `iss` JWT sebagai string dan tidak pernah diambil, sehingga dapat mereferensikan hostname internal atau port non-standar.
</Note>

### Verifikasi JWT

| Batasan                   | Detail                                                                                                                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ukuran maksimum           | JWT `assertion` harus paling banyak 16 KiB.                                                                                                                                              |
| Algoritma penandatanganan | Hanya algoritma asimetris (keluarga RSA dan ECDSA: ES256, ES384, ES512, RS256, RS384, RS512, PS256, PS384, PS512) yang diterima. HMAC (`HS256`, `HS384`, `HS512`) dan `none` ditolak.    |
| Key ID                    | Header JWT harus membawa `kid` yang cocok dengan kunci dalam JWKS issuer. Token tanpa `kid` ditolak.                                                                                     |
| Klaim wajib               | `sub` harus ada. `iat` harus ada dan tidak di masa depan. `exp` harus ada dan di masa depan.                                                                                             |
| Masa hidup maksimum       | Masa hidup token (`exp` dikurangi `iat`) tidak boleh melebihi maksimum yang dikonfigurasi pada issuer (1 jam secara default, dapat dikonfigurasi untuk setiap issuer di Claude Console). |
| Toleransi waktu           | Toleransi 30 detik diterapkan pada `exp`, `nbf`, dan `iat`.                                                                                                                              |

## Semantik pencocokan aturan

Blok `match` pada aturan federasi menentukan apakah JWT yang masuk diterima. Semua field yang terisi dievaluasi dengan semantik AND: JWT harus memenuhi setiap matcher yang terisi. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur; blok `match` yang hanya berisi `audience` (atau tanpa matcher sama sekali) ditolak. Ini melindungi dari aturan yang akan menerima setiap token dari suatu issuer.

| Matcher          | Tipe                 | Semantik                                                                                                                                                                                                                                        |
| ---------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subject_prefix` | string               | Pencocokan persis terhadap klaim `sub` JWT. Tanda `*` di akhir menjadikannya pencocokan prefiks (nilai `sub` harus dimulai dengan karakter sebelum `*`). Peka huruf besar-kecil.                                                                |
| `audience`       | string               | Klaim `aud` JWT harus berisi string persis ini. Ketika `aud` adalah array, elemen mana pun yang cocok persis memenuhi pemeriksaan.                                                                                                              |
| `claims`         | map\<string, string> | Setiap kunci adalah nama klaim tingkat atas dan setiap nilai adalah nilai string persis yang diperlukan. Untuk klaim bersarang, numerik, boolean, atau kompleks seperti list dan map, gunakan `condition` dengan ekspresi CEL sebagai gantinya. |
| `condition`      | string (CEL)         | Ekspresi [CEL](https://cel.dev/) yang harus dievaluasi menjadi `true`.                                                                                                                                                                          |

### Lingkungan evaluasi CEL

Ekspresi `condition` memiliki akses ke satu variabel:

| Variabel | Tipe | Isi                                                                                                  |
| -------- | ---- | ---------------------------------------------------------------------------------------------------- |
| `claims` | map  | Kumpulan klaim JWT lengkap yang telah didekode. Objek bersarang dapat diakses sebagai map bersarang. |

Contoh:

```text wrap
claims.sub.startsWith("repo:acme-corp/") && claims.ref in ["refs/heads/main", "refs/heads/release"]
```

<Warning>
  Kondisi CEL adalah batas keamanan. Ekspresi yang dievaluasi menjadi `true` untuk lebih banyak input daripada yang dimaksudkan memberikan akses yang lebih luas daripada yang dimaksudkan. Utamakan matcher statis ketika matcher tersebut dapat mengekspresikan batasan Anda.
</Warning>

## Kesalahan

### Kesalahan pertukaran token

`POST /v1/oauth/token` mengembalikan kesalahan dalam [bentuk kesalahan API](/docs/id/api/errors) standar. SDK membungkus kegagalan pertukaran dalam `FederationExchangeError` bertipe (atau padanan bahasanya) yang mengekspos status HTTP, body respons, dan `request_id`.

| Status | Kesalahan         | Penyebab                                                                                                                           | Resolusi                                                                                                                                                                                                                                                                                         |
| ------ | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 400    | `invalid_request` | `federation_rule_id` memiliki format yang salah atau field permintaan yang wajib tidak ada.                                        | Verifikasi ID `fdrl_` dan bahwa body permintaan menyertakan semua field yang wajib.                                                                                                                                                                                                              |
| 400    | `invalid_request` | `workspace_id_required`: aturan federasi diaktifkan untuk lebih dari satu workspace dan permintaan menghilangkan `workspace_id`.   | Atur `ANTHROPIC_WORKSPACE_ID` (atau field body `workspace_id` pada permintaan mentah) ke ID `wrkspc_...` yang Anda inginkan sebagai cakupan token. Lihat [Permintaan pertukaran token](#token-exchange-request).                                                                                 |
| 400    | `invalid_grant`   | Klaim `iss` JWT tidak sama persis dengan `issuer_url` yang terdaftar.                                                              | Bandingkan byte demi byte, termasuk garis miring di akhir dan skema: `jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' <<< "$JWT"`.                                                                                                                      |
| 400    | `invalid_grant`   | Pengambilan JWKS gagal, JWKS sudah usang, atau JWT ditandatangani dengan kunci yang tidak ada dalam JWKS.                          | Untuk mode `inline`, perbarui issuer dengan kunci yang telah dirotasi. Untuk `discovery` dan `explicit_url`, konfirmasi bahwa endpoint JWKS dapat dijangkau pada port 443; jika issuer baru saja merotasi kunci penandatanganannya, lihat [Rotasi kunci dan caching](#key-rotation-and-caching). |
| 400    | `invalid_grant`   | Klaim `exp` JWT berada di masa lalu (melampaui jendela toleransi 30 detik).                                                        | Konfirmasi bahwa penyedia identitas Anda memproyeksikan token baru dan SDK membaca ulang file token.                                                                                                                                                                                             |
| 400    | `invalid_grant`   | JWT telah diverifikasi tetapi klaimnya tidak memenuhi blok `match` aturan.                                                         | Dekode JWT dan bandingkan setiap klaim dengan aturan. `subject_prefix` peka huruf besar-kecil. `audience` memerlukan pencocokan elemen yang persis.                                                                                                                                              |
| 400    | `invalid_grant`   | `federation_rule_id` tidak ada, telah diarsipkan, atau JWT tidak diotorisasi untuknya (dikonsolidasikan untuk mencegah enumerasi). | Konfirmasi ID aturan di Claude Console dan bahwa aturan belum diarsipkan.                                                                                                                                                                                                                        |

Semua kegagalan `invalid_grant` mengembalikan HTTP 400; penyebab spesifiknya hanya dicatat di sisi server dan tidak diekspos dalam respons.

### Kegagalan umum di sisi SDK

| Gejala                                                                   | Penyebab                                                                                                                                                                                          | Resolusi                                                                   |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| SDK melaporkan "no credentials" alih-alih melakukan pertukaran           | Salah satu dari `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, atau `ANTHROPIC_IDENTITY_TOKEN[_FILE]` tidak diatur dan tidak ada profil yang aktif. | Atur keempat variabel tersebut, atau konfigurasikan profil.                |
| SDK mengautentikasi dengan kunci API alih-alih melakukan federasi        | `ANTHROPIC_API_KEY` atau `ANTHROPIC_AUTH_TOKEN` diatur dan memenangkan prioritas.                                                                                                                 | Hapus variabel kunci atau token tersebut.                                  |
| `FileNotFoundError` pada permintaan pertama                              | Path di `ANTHROPIC_IDENTITY_TOKEN_FILE` tidak ada. SDK membuka file secara lazy pada waktu pertukaran.                                                                                            | Konfirmasi bahwa volume projected-token telah di-mount dan path-nya cocok. |
| Pertukaran token berhasil tetapi permintaan Claude API mengembalikan 403 | Scope token yang diterbitkan tidak memberikan akses ke endpoint tersebut.                                                                                                                         | Periksa `oauth_scope` aturan terhadap [Scope OAuth](#oauth-scopes).        |
| Autentikasi gagal dengan kredensial kosong                               | Variabel lingkungan kredensial diekspor tetapi diatur ke string kosong. Nilai kosong tetap memenangkan slot prioritasnya.                                                                         | Hapus variabel dengan `unset VAR` alih-alih `VAR=""`.                      |

## Memecahkan masalah pertukaran yang gagal

Respons `400 invalid_grant` sengaja dibuat tidak transparan; penyebab spesifiknya hanya dicatat di sisi server.

<Tip>
  Mulailah dengan [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console. Upaya pertukaran terbaru menampilkan issuer dan aturan yang dievaluasi, klaim JWT yang diperiksa, dan langkah validasi mana yang gagal, yang biasanya mempersingkat pemeriksaan berikut.
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
    Klaim `iss` yang didekode harus sama dengan `issuer_url` yang terdaftar byte demi byte, termasuk skema, port, dan garis miring di akhir. Ketidakcocokan pada satu karakter saja menggagalkan verifikasi.
  </Step>

  <Step title="Periksa aud cocok dengan aturan">
    Klaim `aud` yang didekode harus berisi nilai `audience` aturan sebagai pencocokan persis. Ketika `aud` adalah array, satu elemen harus cocok persis.
  </Step>

  <Step title="Periksa sub dan setiap entri claims">
    Bandingkan `sub` dengan `subject_prefix` aturan (peka huruf besar-kecil; `*` di akhir adalah pencocokan prefiks, selain itu adalah pencocokan persis). Bandingkan setiap kunci dalam map `claims` aturan dengan klaim tingkat atas yang bernama sama.
  </Step>

  <Step title="Periksa exp, nbf, dan iat">
    `exp` harus di masa depan dan `nbf`/`iat` harus di masa lalu, dalam jendela toleransi 30 detik. Jika jam host beban kerja telah bergeser, token yang sebenarnya valid akan ditolak.
  </Step>

  <Step title="Periksa keterjangkauan JWKS">
    Untuk mode `discovery`, ambil `<jwks.discovery_base or issuer_url>/.well-known/openid-configuration` melalui HTTPS publik pada port 443 dan konfirmasi bahwa `jwks_uri` dapat di-resolve. Untuk `explicit_url`, ambil URL JWKS secara langsung. Untuk `inline`, konfirmasi bahwa kunci penandatanganan issuer belum dirotasi sejak Anda mendaftarkan kunci-kunci tersebut.

    Jika issuer merotasi kunci penandatanganannya dan segera mulai menandatangani dengannya, pertukaran dapat gagal hingga satu menit sementara cache JWKS Anthropic disegarkan. Lihat [Rotasi kunci dan caching](#key-rotation-and-caching).
  </Step>
</Steps>

## Mode sumber JWKS

Ketika Anda mendaftarkan issuer federasi, field `jwks` mengontrol bagaimana Anthropic memperoleh kunci publik yang digunakan untuk memverifikasi tanda tangan JWT dari issuer tersebut. Ini adalah discriminated union yang dikunci pada `type`:

| `jwks.type`           | Bentuk `jwks`                                                                                                                                        | Perilaku                                                                                                                                                                                                      | Gunakan ketika                                                                                                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery` (default) | `{ "type": "discovery", "discovery_base": "https://..." }` (`discovery_base` bersifat opsional; atur ketika URL discovery berbeda dari `issuer_url`) | Anthropic mengambil `<discovery_base or issuer_url>/.well-known/openid-configuration`, membaca `jwks_uri` dari dokumen discovery, dan mengambil JWKS dari sana.                                               | IdP Anda menyajikan dokumen discovery OIDC standar di internet publik. Sebagian besar penyedia terkelola (EKS, GKE, Cloud Run, GitHub Actions, Entra ID) mendukung ini. |
| `explicit_url`        | `{ "type": "explicit_url", "url": "https://..." }`                                                                                                   | Anthropic mengambil JWKS langsung dari `url`. `issuer_url` hanya digunakan untuk perbandingan string terhadap klaim `iss` JWT dan tidak pernah dihubungi.                                                     | IdP Anda tidak menyajikan dokumen discovery, atau discovery hanya internal tetapi JWKS dapat dijangkau secara publik.                                                   |
| `inline`              | `{ "type": "inline", "keys": [...] }`                                                                                                                | Anda menyediakan array objek JWK secara inline (array `keys` dari dokumen JWKS, bukan objek pembungkusnya). Anthropic tidak membuat permintaan keluar. `issuer_url` hanya digunakan untuk perbandingan `iss`. | Lingkungan air-gapped, klaster Kubernetes yang dikelola sendiri dengan URL issuer internal klaster, atau ketika Anda menginginkan kontrol eksplisit atas rotasi kunci.  |

Discriminated union membuat field pendamping saling eksklusif secara konstruksi. Baik `discovery` maupun `explicit_url` juga menerima string `ca_cert_pem` opsional untuk issuer yang menyajikan TLS dari CA privat.

### Rotasi kunci dan caching

Dalam mode `discovery` dan `explicit_url`, Anthropic meng-cache JWKS yang diambil. Jika penyedia identitas Anda memublikasikan kunci penandatanganan baru dan segera mulai menandatangani token dengannya, pertukaran yang menyajikan token tersebut dapat gagal dengan kesalahan tanda tangan hingga satu menit sementara cache disegarkan.

Untuk menghindari jendela ini, publikasikan kunci penandatanganan baru di JWKS setidaknya 15 menit sebelum penyedia identitas Anda mulai menandatangani token dengannya, dan pertahankan kunci yang digantikan di JWKS hingga token yang ditandatanganinya telah kedaluwarsa. Penyedia identitas terkelola biasanya mengikuti disiplin ini dengan sendirinya. Jika Anda mengoperasikan issuer Anda sendiri (klaster Kubernetes yang dikelola sendiri, penyedia discovery OIDC SPIRE, atau server otorisasi kustom Okta dengan kadens rotasi yang dikonfigurasi), konfirmasi bahwa kebijakan rotasi Anda memublikasikan kunci baru sebelum penggunaan pertama.

<Warning>
  Dalam mode `inline` tidak ada penyegaran kunci otomatis. Ketika penyedia identitas Anda merotasi kunci penandatanganannya, Anda harus memperbarui konfigurasi issuer dengan JWKS baru atau semua pertukaran token akan gagal verifikasi tanda tangan.
</Warning>
