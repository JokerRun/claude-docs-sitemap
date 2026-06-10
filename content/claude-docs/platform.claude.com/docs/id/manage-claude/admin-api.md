---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: f65b833d6c4edba89ec3adfb2c44f790920858dcca04d073dd3a6b0320c2a8e8
---

# Admin API

---

<Tip>
**Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

[Admin API](/docs/id/api/admin) memungkinkan Anda mengelola sumber daya organisasi Anda secara terprogram, termasuk anggota organisasi, workspace, dan kunci API. Ini memberikan kontrol terprogram atas tugas-tugas administratif yang jika tidak akan memerlukan konfigurasi manual di [Claude Console](/).

<Check>
  **Admin API memerlukan akses khusus**

  Admin API memerlukan kunci Admin API khusus (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Hanya anggota organisasi dengan peran admin yang dapat menyediakan kunci Admin API melalui Claude Console.
</Check>

<Note>
**Claude Platform di AWS:** Sebagian besar Admin API tidak tersedia di Claude Platform di AWS. Endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) tersedia. Endpoint lainnya termasuk anggota organisasi, anggota workspace, undangan, kunci API, laporan penggunaan, laporan biaya, dan laporan batas laju tidak tersedia. Lihat [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) untuk detailnya.
</Note>

## Cara kerja Admin API \{#how-the-admin-api-works}

Saat Anda menggunakan Admin API:

1. Anda membuat permintaan menggunakan kunci Admin API Anda di header `x-api-key`
2. API memungkinkan Anda mengelola:
   - Anggota organisasi dan peran mereka
   - Undangan anggota organisasi
   - Workspace dan anggotanya
   - Kunci API

Ini berguna untuk:
- Mengotomatiskan onboarding/offboarding pengguna
- Mengelola akses workspace secara terprogram
- Memantau dan mengelola penggunaan kunci API

## Peran dan izin organisasi \{#organization-roles-and-permissions}

Ada lima peran tingkat organisasi. Lihat detail lebih lanjut di artikel [Peran dan izin API Console](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions).

| Peran | Izin |
|------|-------------|
| user | Dapat menggunakan Workbench |
| claude_code_user | Dapat menggunakan Workbench dan [Claude Code](https://code.claude.com/docs/en/overview) |
| developer | Dapat menggunakan Workbench dan mengelola kunci API |
| billing | Dapat menggunakan Workbench dan mengelola detail penagihan |
| admin | Dapat melakukan semua hal di atas, ditambah mengelola pengguna |

## Konsep utama \{#key-concepts}

### Anggota Organisasi \{#organization-members}

Anda dapat membuat daftar [anggota organisasi](/docs/id/api/admin-api/users/get-user), memperbarui peran anggota, dan menghapus anggota.

<CodeGroup>
```bash cURL
# Menampilkan daftar anggota organisasi
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

### Undangan Organisasi \{#organization-invites}

Anda dapat mengundang pengguna ke organisasi dan mengelola [undangan](/docs/id/api/admin-api/invites/get-invite) tersebut.

<CodeGroup>

```bash cURL
# Buat undangan
curl --request POST "https://api.anthropic.com/v1/organizations/invites" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "email": "newuser@domain.com",
    "role": "developer"
  }'

# Daftar undangan
curl "https://api.anthropic.com/v1/organizations/invites?limit=10" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Hapus undangan
curl --request DELETE "https://api.anthropic.com/v1/organizations/invites/{invite_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

</CodeGroup>

### Workspace \{#workspaces}

Untuk panduan komprehensif tentang workspace, termasuk contoh Console dan API, lihat [Workspace](/docs/id/manage-claude/workspaces).

### Anggota Workspace \{#workspace-members}

Kelola [akses pengguna ke workspace tertentu](/docs/id/api/admin-api/workspace_members/get-workspace-member):

<CodeGroup>

```bash cURL
# Tambahkan anggota ke workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "user_id": "user_xxx",
    "workspace_role": "workspace_developer"
  }'

# Daftar anggota workspace
curl "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members?limit=10" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Perbarui peran anggota
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "workspace_role": "workspace_admin"
  }'

# Hapus anggota dari workspace
curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

</CodeGroup>

### Kunci API \{#api-keys}

Pantau dan kelola [kunci API](/docs/id/api/admin-api/apikeys/get-api-key):

<CodeGroup>

```bash cURL
# Daftar kunci API
curl "https://api.anthropic.com/v1/organizations/api_keys?limit=10&status=active&workspace_id=wrkspc_xxx" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Perbarui kunci API
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

## Mengakses info organisasi \{#accessing-organization-info}

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

Endpoint ini berguna untuk menentukan secara terprogram organisasi mana yang terkait dengan kunci Admin API.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Organization Info API](/docs/id/api/admin-api/organization/get-me).

## Laporan penggunaan dan biaya \{#usage-and-cost-reports}

Lacak penggunaan dan biaya organisasi Anda dengan [Usage and Cost API](/docs/id/manage-claude/usage-cost-api).

## Analitik Claude Code \{#claude-code-analytics}

Pantau produktivitas developer dan adopsi Claude Code dengan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api).

## Batas laju \{#rate-limits}

Baca batas laju yang dikonfigurasi untuk organisasi Anda dan workspace-nya dengan [Rate Limits API](/docs/id/manage-claude/rate-limits-api).

## Compliance API \{#compliance-api}

Ambil data audit dan aktivitas untuk organisasi Anda dengan [Compliance API](/docs/id/manage-claude/compliance-api). Kunci Admin API hanya dapat membaca Activity Feed; untuk akses penuh, lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).

## Praktik terbaik \{#best-practices}

Untuk menggunakan Admin API secara efektif:

- Gunakan nama dan deskripsi yang bermakna untuk workspace dan kunci API
- Terapkan penanganan kesalahan yang tepat untuk operasi yang gagal
- Audit peran dan izin anggota secara berkala
- Bersihkan workspace yang tidak digunakan dan undangan yang kedaluwarsa
- Pantau penggunaan kunci API dan rotasi kunci secara berkala

## FAQ \{#faq}

<section title="Izin apa yang diperlukan untuk menggunakan Admin API?">

Hanya anggota organisasi dengan peran admin yang dapat menggunakan Admin API. Mereka juga harus memiliki kunci Admin API khusus (dimulai dengan `sk-ant-admin`).

</section>

<section title="Bisakah saya membuat kunci API baru melalui Admin API?">

Tidak, kunci API baru hanya dapat dibuat melalui Claude Console untuk alasan keamanan. Admin API hanya dapat mengelola kunci API yang sudah ada.

</section>

<section title="Apa yang terjadi pada kunci API saat menghapus pengguna?">

Kunci API tetap dalam kondisi saat ini karena cakupannya adalah Organisasi, bukan pengguna individu.

</section>

<section title="Bisakah admin organisasi dihapus melalui API?">

Tidak, anggota organisasi dengan peran admin tidak dapat dihapus melalui API untuk alasan keamanan.

</section>

<section title="Berapa lama undangan organisasi berlaku?">

Undangan organisasi kedaluwarsa setelah 21 hari. Saat ini tidak ada cara untuk mengubah periode kedaluwarsa ini.

</section>

Untuk pertanyaan khusus workspace, lihat [FAQ Workspace](/docs/id/manage-claude/workspaces#faq).