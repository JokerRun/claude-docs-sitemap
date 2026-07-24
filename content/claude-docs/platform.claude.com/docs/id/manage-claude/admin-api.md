---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 5008f30d42560e3e5a79b14a3e3075c915a6a0f6a2381cebcb68b9871e2910aa
---

# Admin API

Kelola anggota organisasi, workspace, undangan, dan kunci API secara terprogram dengan Admin API, menggunakan kunci Admin API atau token OAuth `org:admin`.

---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

[Admin API](/docs/id/api/admin) memungkinkan Anda mengelola sumber daya organisasi Anda secara terprogram, termasuk anggota organisasi, workspace, dan kunci API. Ini memberikan kontrol terprogram atas tugas-tugas administratif yang jika tidak akan memerlukan konfigurasi manual di [Claude Console](/).

<Check>
  **Admin API memerlukan akses khusus**

  Admin API menerima dua kredensial:

  * **Kunci Admin API** (dimulai dengan `sk-ant-admin...`) yang dikirim di header `x-api-key`. Hanya anggota organisasi dengan peran admin yang dapat membuatnya. Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys).
  * **Token bearer OAuth** dengan cakupan `org:admin` yang dikirim di header `authorization: Bearer`. Hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperolehnya. Lihat [Memperoleh token bearer OAuth](#oauth-bearer-token).
</Check>

<Note>
  **Claude Enterprise:** Organisasi Claude Enterprise (claude.ai) juga menggunakan Admin API, dengan kunci API bercakupan yang dibuat di claude.ai. Dari endpoint di halaman ini, hanya anggota dan undangan yang tersedia untuk mereka (dalam beta), bersama dengan endpoint khusus Claude Enterprise: grup dan pembacaan peran kustom (beta), serta [batas pengeluaran](/docs/id/manage-claude/spend-limits-api). Lihat [Manajemen pengguna](/docs/id/manage-claude/user-management) untuk Claude Enterprise.
</Note>

<Note>
  **Claude Platform di AWS:** Sebagian besar Admin API tidak tersedia di Claude Platform di AWS. Endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) tersedia. Endpoint lainnya termasuk anggota organisasi, anggota workspace, undangan, kunci API, laporan penggunaan, laporan biaya, dan laporan batas laju tidak tersedia. Lihat [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) untuk detailnya.
</Note>

## Autentikasi

Autentikasi dengan salah satu kredensial. Kunci Admin API mencakup sebagian besar endpoint; endpoint service-account, federation-issuer, dan federation-rule hanya menerima token OAuth `org:admin`. Contoh berikut memanggil [endpoint info organisasi](#accessing-organization-info) dengan kedua cara.

### Token bearer OAuth

Masuk dengan [CLI `ant`](/docs/id/cli-sdks-libraries/cli/quickstart) di bawah profil khusus, dengan meminta cakupan `org:admin` (lihat [Akses admin](/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor token bearer. Profil khusus menjaga perintah rutin Anda agar tidak berjalan dengan akses yang ditingkatkan:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_OAUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek; jika permintaan mulai mengembalikan 401, jalankan kembali perintah `export`, yang akan menyegarkan token secara otomatis.

Panggil Admin API dengan token yang telah diekspor:

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Token `org:admin` memberikan akses ke seluruh organisasi, terlepas dari workspace tempat profil yang mendasarinya atau [aturan federasi](#federation-rules) terikat.

Untuk CI dan beban kerja non-interaktif lainnya, buat token dengan Workload Identity Federation alih-alih masuk secara interaktif. Lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api#workload-ci-and-automation).

### Kunci Admin API

Untuk membuat kunci Admin API untuk jenis organisasi Anda, lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys).

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Cara kerja Admin API

Saat Anda menggunakan Admin API:

1. Anda membuat permintaan menggunakan salah satu kredensial dari bagian [Autentikasi](#authentication)

2. API memungkinkan Anda mengelola:

   * Anggota organisasi dan peran mereka
   * Undangan anggota organisasi
   * Workspace dan anggotanya
   * Kunci API
   * Service account, federation issuer, dan federation rule (endpoint ini memerlukan token OAuth `org:admin`; kunci Admin API tidak diterima)

Ini berguna untuk:

* Mengotomatiskan onboarding/offboarding pengguna
* Mengelola akses workspace secara terprogram
* Memantau dan mengelola penggunaan kunci API

## Peran dan izin organisasi

Ada lima peran tingkat organisasi. Lihat detail lebih lanjut di artikel [API Console roles and permissions](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions).

| Peran              | Izin                                                                                    |
| ------------------ | --------------------------------------------------------------------------------------- |
| user               | Dapat menggunakan Workbench                                                             |
| claude\_code\_user | Dapat menggunakan Workbench dan [Claude Code](https://code.claude.com/docs/en/overview) |
| developer          | Dapat menggunakan Workbench dan mengelola kunci API                                     |
| billing            | Dapat menggunakan Workbench dan mengelola detail penagihan                              |
| admin              | Dapat melakukan semua hal di atas, ditambah mengelola pengguna                          |

Owner dan primary owner organisasi memiliki semua izin admin dan juga dapat mengelola admin. Semua referensi ke peran admin di halaman ini juga berlaku untuk owner dan primary owner.

## Konsep utama

### Anggota organisasi

Anda dapat membuat daftar [anggota organisasi](/docs/id/api/admin-api/users/get-user), memperbarui peran anggota, dan menghapus anggota.

<CodeGroup>
  ```bash cURL
  # Mencantumkan anggota organisasi
  curl "https://api.anthropic.com/v1/organizations/users?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Memperbarui peran anggota
  curl "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{"role": "developer"}'

  # Menghapus anggota
  curl --request DELETE "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Undangan organisasi

Anda dapat mengundang pengguna ke organisasi dan mengelola [undangan](/docs/id/api/admin-api/invites/get-invite) tersebut.

<CodeGroup>
  ```bash cURL
  # Membuat undangan
  curl --request POST "https://api.anthropic.com/v1/organizations/invites" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "email": "newuser@domain.com",
      "role": "developer"
    }'

  # Menampilkan daftar undangan
  curl "https://api.anthropic.com/v1/organizations/invites?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Menghapus undangan
  curl --request DELETE "https://api.anthropic.com/v1/organizations/invites/{invite_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Workspace

Untuk panduan komprehensif tentang workspace, termasuk contoh Console dan API, lihat [Workspace](/docs/id/manage-claude/workspaces).

### Anggota workspace

Kelola [akses pengguna ke workspace tertentu](/docs/id/api/admin-api/workspace_members/get-workspace-member):

<CodeGroup>
  ```bash cURL
  # Menambahkan anggota ke workspace
  curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "user_id": "user_xxx",
      "workspace_role": "workspace_developer"
    }'

  # Menampilkan daftar anggota workspace
  curl "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Memperbarui peran anggota
  curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "workspace_role": "workspace_admin"
    }'

  # Menghapus anggota dari workspace
  curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Kunci API

Pantau dan kelola [kunci API](/docs/id/api/admin/api_keys/list). Setiap kunci dalam respons menyertakan timestamp `expires_at`-nya (`null` untuk kunci tanpa [kedaluwarsa](/docs/id/manage-claude/authentication#key-expiration)):

<CodeGroup>
  ```bash cURL
  # Mencantumkan kunci API
  curl "https://api.anthropic.com/v1/organizations/api_keys?limit=10&status=active&workspace_id=wrkspc_xxx" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Memperbarui kunci API
  curl --request POST "https://api.anthropic.com/v1/organizations/api_keys/{api_key_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "status": "inactive",
      "name": "New Key Name"
    }'
  ```
</CodeGroup>

### Service account

Buat dan kelola service account (`svac_...`), identitas non-manusia yang diwakili oleh token [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation). Kunci Admin API tidak diterima pada endpoint service-account, federation-issuer, atau federation-rule; gunakan token OAuth `org:admin`. Lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api#service-accounts).

### Federation issuer

Daftarkan penyedia identitas OIDC (`fdis_...`) yang tokennya dapat menegaskan identitas beban kerja untuk organisasi Anda. Lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api#federation-issuers).

### Federation rule

Kelola aturan (`fdrl_...`) yang memetakan token issuer ke service account dan cakupan. Lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api#federation-rules).

## Mengakses info organisasi

Dapatkan informasi tentang organisasi Anda secara terprogram dengan endpoint `/v1/organizations/me`.

Sebagai contoh:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "type": "organization",
  "name": "Organization Name"
}
```

Endpoint ini berguna untuk menentukan secara terprogram organisasi mana yang memiliki kunci Admin API tertentu.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Organization Info API](/docs/id/api/admin-api/organization/get-me).

## Laporan penggunaan dan biaya

Lacak penggunaan dan biaya organisasi Anda dengan [Usage and Cost API](/docs/id/manage-claude/usage-cost-api).

## Analitik Claude Code

Pantau produktivitas developer dan adopsi Claude Code dengan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api).

## Batas laju

Baca "rate limit" (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya dengan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

## Compliance API

Ambil data audit dan aktivitas untuk organisasi Anda dengan [Compliance API](/docs/id/manage-claude/compliance-api). Kunci Admin API hanya dapat membaca Activity Feed; untuk akses penuh, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).

## Praktik terbaik

Untuk menggunakan Admin API secara efektif:

* Gunakan nama dan deskripsi yang bermakna untuk workspace dan kunci API
* Terapkan penanganan kesalahan yang tepat untuk operasi yang gagal
* Audit peran dan izin anggota secara berkala
* Bersihkan workspace yang tidak digunakan dan undangan yang kedaluwarsa
* Pantau penggunaan kunci API, audit [`expires_at`](/docs/id/manage-claude/authentication#key-expiration) setiap kunci, dan rotasi kunci secara berkala

## FAQ

<AccordionGroup>
  <Accordion title="Izin apa yang diperlukan untuk menggunakan Admin API?">
    Admin API menerima kunci Admin API (dimulai dengan `sk-ant-admin`) atau token bearer OAuth dengan cakupan `org:admin`. Hanya anggota organisasi dengan peran admin yang dapat membuat kunci Admin API, dan hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperoleh token `org:admin`. Lihat [Autentikasi](#authentication).
  </Accordion>

  <Accordion title="Dapatkah saya membuat kunci API baru melalui Admin API?">
    Tidak, kunci API baru hanya dapat dibuat melalui Claude Console untuk alasan keamanan. Admin API hanya dapat mengelola kunci API yang sudah ada.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API saat menghapus pengguna?">
    Kunci API tetap dalam keadaan saat ini karena kunci tersebut terikat pada organisasi, bukan pada pengguna individu.
  </Accordion>

  <Accordion title="Dapatkah admin organisasi dihapus melalui API?">
    Tidak, anggota organisasi dengan peran admin tidak dapat dihapus melalui API untuk alasan keamanan.
  </Accordion>

  <Accordion title="Berapa lama undangan organisasi berlaku?">
    Undangan organisasi kedaluwarsa setelah 21 hari. Saat ini tidak ada cara untuk mengubah periode kedaluwarsa ini.
  </Accordion>
</AccordionGroup>

Untuk pertanyaan khusus workspace, lihat [FAQ Workspace](/docs/id/manage-claude/workspaces#faq).
