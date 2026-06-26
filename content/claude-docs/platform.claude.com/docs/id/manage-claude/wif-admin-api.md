---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-admin-api
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 14abb0c619f5cdde2ec1c053231388fa68561b6ccf529e61c7f8a007de3f7b4e
---

# Mengelola WIF dengan Admin API

Buat dan kelola akun layanan, issuer, dan aturan Workload Identity Federation secara terprogram untuk alur kerja infrastructure-as-code dan CI.

---

Admin API memungkinkan Anda membuat dan mengelola sumber daya [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) secara terprogram: akun layanan, federation issuer, dan federation rule. Gunakan API ini untuk menyimpan konfigurasi federasi Anda dalam infrastructure as code, menyediakannya dari CI, dan mereproduksinya di berbagai organisasi alih-alih mengklik satu per satu melalui Claude Console. Endpoint ini berbagi prefiks path `/v1/organizations` dengan bagian lain dari [Admin API](/docs/id/manage-claude/admin-api).

## Prasyarat \{#prerequisites}

Setiap permintaan di halaman ini diautentikasi dengan OAuth bearer token yang membawa scope `org:admin`. Scope ini hanya diberikan kepada anggota organisasi dengan peran admin, owner, atau primary owner, dan memberikan akses ke seluruh organisasi: binding workspace apa pun akan diabaikan. Ada dua cara untuk mendapatkan token, dan keduanya membawa izin yang berbeda: token dari login Anda sendiri bertindak sebagai pengguna, sedangkan token terfederasi bertindak sebagai akun layanan dan tidak dapat melakukan semua operasi di halaman ini.

**Interaktif (terminal Anda):** Login dengan [CLI `ant`](/docs/id/cli-sdks-libraries/cli/quickstart) menggunakan profil khusus, dengan meminta scope `org:admin` (lihat [Akses admin](/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor bearer token:

```bash CLI nocheck
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_OAUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek; jika permintaan mulai mengembalikan 401, jalankan kembali perintah ekspor (perintah ini menyegarkan token secara otomatis).

**Workload (CI dan otomatisasi):** Buat federation rule dengan `oauth_scope: org:admin` yang menargetkan akun layanan dengan `organization_role` bernilai `admin`. Aturan itu sendiri harus dibuat di Claude Console: memberikan akses admin organisasi kepada sebuah workload adalah tindakan manusia yang disengaja, bukan sesuatu yang dapat di-bootstrap sendiri oleh otomatisasi. Bagian berikutnya memandu Anda melalui penyiapan sekali-per-organisasi ini.

## Bootstrap workload untuk mengelola WIF \{#bootstrap-a-workload-to-manage-wif}

Satu aturan yang dibuat di Console sudah cukup untuk menempatkan sisa konfigurasi federasi Anda di bawah infrastructure as code: berikan scope `org:admin` kepada satu workload tepercaya, dan biarkan workload tersebut mengelola federation issuer dan setiap federation rule dengan scope workspace melalui API ini.

<Steps>
  <Step title="Buat aturan org:admin di Console">
    Di Claude Console, buka **Settings → Workload identity** dan pilih **Connect workload** untuk membuat satu federation rule bagi workload otomatisasi Anda, misalnya workflow GitHub Actions di repositori infrastruktur Anda. Di bawah **Advanced rule options**, atur OAuth scope aturan ke `org:admin`: wizard kemudian membuat akun layanan baru dengan peran organisasi Admin (atau meminta Anda memilih akun layanan admin yang sudah ada sebagai target).

    <Warning>
      Cocokkan aturan dengan satu identitas workload yang persis, bukan pola yang luas. `subject_prefix` adalah pencocokan persis kecuali diakhiri dengan `*`. Untuk GitHub Actions, pin subject ke branch yang dilindungi, seperti `repo:my-org/my-repo:ref:refs/heads/main`. Wildcard di akhir seperti `repo:my-org/my-repo:*` juga mencocokkan run `pull_request`, termasuk run yang dipicu dari fork, sehingga siapa pun yang dapat membuka pull request terhadap repositori tersebut dapat mencetak token `org:admin`. Lihat [Membatasi workflow mana yang dapat mengautentikasi](/docs/id/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate).
    </Warning>
  </Step>

  <Step title="Tukarkan identity token workload">
    Saat runtime, workload menukarkan JWT dari identity provider-nya dengan bearer token `org:admin` berumur pendek menggunakan [token exchange](/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload) yang sama seperti workload terfederasi lainnya.
  </Step>

  <Step title="Kelola issuer dan aturan dengan scope workspace melalui API">
    Dengan token yang dicetak di `ANTHROPIC_OAUTH_TOKEN`, workload membuat dan mengelola konfigurasi federasi Anda menggunakan endpoint di halaman ini.
  </Step>
</Steps>

Untuk operasi yang dapat dan tidak dapat dilakukan oleh token yang dicetak workload, lihat [Izin dan batasan](#permissions-and-constraints). Jika Anda sudah membuat issuer, akun layanan, atau aturan dengan wizard Connect workload, daftarkan semuanya dengan endpoint berikut dan impor ke dalam state infrastructure-as-code Anda alih-alih membuatnya ulang.

## Autentikasi \{#authentication}

Semua endpoint berada di bawah `https://api.anthropic.com/v1/organizations/`. Setiap permintaan ke endpoint federasi dan akun layanan memerlukan header versi API dan bearer token:

```bash cURL nocheck
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Kunci Admin API tidak diterima pada endpoint ini; contoh `x-api-key` di halaman Admin API tidak berlaku di sini.

## Akun layanan \{#service-accounts}

[Akun layanan](/docs/id/manage-claude/workload-identity-federation#service-accounts) (`svac_...`) adalah identitas non-manusia yang diwakili oleh token terfederasi. Atur `organization_role` ke `developer`.

```bash cURL nocheck
# Membuat akun layanan
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "inference-worker",
    "organization_role": "developer"
  }'

# Menampilkan daftar akun layanan
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts?limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Mengarsipkan akun layanan
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/service_accounts/svac_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Endpoint create mengembalikan akun layanan baru:

```json
{
  "id": "svac_...",
  "name": "inference-worker",
  "organization_role": "developer",
  "created_at": "...",
  "type": "service_account",
  "...": "..."
}
```

Untuk membaca atau memperbarui satu akun layanan, gunakan `GET` dan `POST` pada `/v1/organizations/service_accounts/{service_account_id}`. Akun layanan harus menjadi anggota workspace sebelum token terfederasi dapat bertindak di dalamnya. Setiap akun layanan memiliki keanggotaan implisit di workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain dengan `GET`, `POST`, dan `DELETE` pada `/v1/organizations/service_accounts/{service_account_id}/workspaces`, di mana `DELETE` menargetkan `.../workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Service accounts](/docs/id/api/admin/service_accounts).

## Federation issuer \{#federation-issuers}

[Federation issuer](/docs/id/manage-claude/workload-identity-federation#federation-issuers) (`fdis_...`) mendaftarkan identity provider OIDC ke organisasi Anda. Field `jwks` adalah discriminated union yang mengontrol bagaimana Anthropic mengambil signing key dari provider:

| Nilai `jwks`                          | Kapan digunakan                                                                  |
| ------------------------------------- | -------------------------------------------------------------------------------- |
| `{"type": "discovery"}`               | Provider menyajikan `/.well-known/openid-configuration` di URL issuer.           |
| `{"type": "explicit_url", "url": "..."}` | Menunjuk langsung ke endpoint JWKS.                                            |
| `{"type": "inline", "keys": [...]}`   | Unggah key set untuk provider yang tidak dapat dijangkau dari internet publik.   |

```bash cURL nocheck
# Daftarkan issuer (GitHub Actions, dengan penemuan JWKS)
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "github-actions",
    "issuer_url": "https://token.actions.githubusercontent.com",
    "jwks": {"type": "discovery"}
  }'

# Tampilkan daftar issuer
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers?limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Arsipkan issuer
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/federation_issuers/fdis_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Untuk membaca atau memperbarui satu issuer, gunakan `GET` dan `POST` pada `/v1/organizations/federation_issuers/{issuer_id}`. Pemanggil OAuth tidak dapat memperbarui issuer yang mendukung aturan dengan `oauth_scope` selain `workspace:developer` atau `workspace:inference`; lihat [Izin dan batasan](#permissions-and-constraints).

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Federation issuers](/docs/id/api/admin/federation_issuers).

## Federation rule \{#federation-rules}

[Federation rule](/docs/id/manage-claude/workload-identity-federation#federation-rules) (`fdrl_...`) mengikat issuer ke akun layanan: JWT dari issuer yang memenuhi kondisi pencocokan aturan dapat mencetak token yang bertindak sebagai target aturan tersebut. `workspace_id` dalam permintaan create mengaktifkan aturan di workspace tersebut saat pembuatan; tambahkan workspace lain nanti melalui sub-resource `/federation_rules/{rule_id}/workspaces`. Salah satu dari `workspace_id` atau `applies_to_all_workspaces: true` wajib ada saat create.

```bash cURL nocheck
# Buat aturan (GitHub Actions melakukan deploy dari branch main)
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "gha-deploy",
    "issuer_id": "fdis_...",
    "match": {
      "subject_prefix": "repo:my-org/my-repo:ref:refs/heads/main",
      "claims": {"repository_owner": "my-org"}
    },
    "target": {
      "type": "service_account",
      "service_account_id": "svac_..."
    },
    "workspace_id": "wrkspc_...",
    "oauth_scope": "workspace:developer",
    "token_lifetime_seconds": 600
  }'

# Tampilkan daftar aturan, dapat difilter berdasarkan penerbit
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules?issuer_id=fdis_..." \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Arsipkan aturan
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/federation_rules/fdrl_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Endpoint list mengembalikan satu halaman aturan dan cursor untuk halaman berikutnya:

```json
{
  "data": [{ "id": "fdrl_...", "name": "gha-deploy", "...": "..." }],
  "next_page": "..."
}
```

Untuk membaca atau memperbarui satu aturan, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}`. Untuk mengelola workspace tempat aturan dapat mencetak token, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}/workspaces`, dan `DELETE` pada `/v1/organizations/federation_rules/{rule_id}/workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Federation rules](/docs/id/api/admin/federation_rules).

## Izin dan batasan \{#permissions-and-constraints}

<Note>
  - Pemanggil yang diautentikasi OAuth hanya dapat membuat atau memodifikasi aturan dengan `oauth_scope` bernilai `workspace:developer` atau `workspace:inference`. Untuk membuat atau memodifikasi aturan dengan scope lain (seperti `org:admin` atau `org:manage_tunnels`), gunakan Console.
  - Pemanggil OAuth tidak dapat memperbarui federation issuer yang mendukung aturan dengan `oauth_scope` selain `workspace:developer` atau `workspace:inference` (seperti `org:admin` atau `org:manage_tunnels`). Pertimbangkan untuk mendaftarkan issuer khusus untuk aturan bootstrap agar issuer di balik aturan dengan scope workspace tetap dapat diperbarui melalui API.
  - Kunci Admin API tidak diterima pada endpoint ini, baik untuk membaca maupun menulis; gunakan OAuth token `org:admin`.
</Note>

Aturan dengan `oauth_scope: org:admin` harus menargetkan akun layanan dengan `organization_role` bernilai `admin`. Nama resource harus cocok dengan `^[a-z0-9-]+$`, terdiri dari 1 hingga 255 karakter, dan unik dalam satu organisasi untuk setiap tipe resource; untuk batasan lengkap di tingkat field, lihat [Aturan validasi](/docs/id/manage-claude/wif-reference#validation-rules).

## Paginasi dan pengarsipan \{#pagination-and-archiving}

Endpoint list untuk akun layanan, federation issuer, dan federation rule menerima `limit` (1 hingga 100, default 20) dan cursor `page` yang diambil dari respons sebelumnya. Teruskan nilai `next_page` dari respons sebagai parameter query `page` pada permintaan berikutnya. List sub-resource rule-workspaces mengembalikan set lengkap tanpa paginasi. Resource yang diarsipkan disembunyikan dari daftar secara default; teruskan `include_archived=true` untuk menyertakannya.

Pengarsipan adalah soft delete dan bersifat idempoten: mengarsipkan resource yang sudah diarsipkan akan berhasil. Mengarsipkan issuer atau akun layanan mengembalikan `400` selama masih ada federation rule aktif yang mereferensikannya; arsipkan aturan tersebut terlebih dahulu.

## Lihat juga \{#see-also}

- [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation): konsep dan panduan penyiapan di Console
- [Referensi WIF](/docs/id/manage-claude/wif-reference): variabel lingkungan, aturan validasi, OAuth scope, dan kode error
- [Admin API](/docs/id/manage-claude/admin-api): bagian lain dari permukaan manajemen organisasi
- [Referensi Admin API](/docs/id/api/admin): skema permintaan dan respons yang dihasilkan untuk setiap endpoint Admin API