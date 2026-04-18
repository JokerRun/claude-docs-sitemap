---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/administration-api
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: d5d7c57ad5e5586bfd52192bdb9a6b9b55ea4812a65e482205b91eb6f030e1b4
---

# Ikhtisar Admin API

Kelola sumber daya organisasi Anda secara terprogram dengan Admin API, termasuk anggota organisasi, ruang kerja, dan kunci API.

---

<Tip>
**The Admin API is unavailable for individual accounts.** To collaborate with teammates and add members, set up your organization in **Console → Settings → Organization**.
</Tip>

[Admin API](/docs/id/api/admin) memungkinkan Anda mengelola sumber daya organisasi secara terprogram, termasuk anggota organisasi, ruang kerja, dan kunci API. Ini memberikan kontrol terprogram atas tugas administratif yang sebaliknya memerlukan konfigurasi manual di [Claude Console](/).

<Check>
  **Admin API memerlukan akses khusus**

  Admin API memerlukan kunci Admin API khusus (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Hanya anggota organisasi dengan peran admin yang dapat menyediakan kunci Admin API melalui Claude Console.
</Check>

## Cara kerja Admin API

Saat Anda menggunakan Admin API:

1. Anda membuat permintaan menggunakan kunci Admin API Anda di header `x-api-key`
2. API memungkinkan Anda mengelola:
   - Anggota organisasi dan peran mereka
   - Undangan anggota organisasi
   - Ruang kerja dan anggota mereka
   - Kunci API

Ini berguna untuk:
- Mengotomatisasi onboarding/offboarding pengguna
- Mengelola akses ruang kerja secara terprogram
- Memantau dan mengelola penggunaan kunci API

## Peran dan izin organisasi

Ada lima peran tingkat organisasi. Lihat detail lebih lanjut di artikel [peran dan izin API Console](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions).

| Peran | Izin |
|------|-------------|
| user | Dapat menggunakan Workbench |
| claude_code_user | Dapat menggunakan Workbench dan [Claude Code](https://code.claude.com/docs/en/overview) |
| developer | Dapat menggunakan Workbench dan mengelola kunci API |
| billing | Dapat menggunakan Workbench dan mengelola detail penagihan |
| admin | Dapat melakukan semua hal di atas, plus mengelola pengguna |

## Konsep kunci

### Anggota Organisasi

Anda dapat membuat daftar [anggota organisasi](/docs/id/api/admin-api/users/get-user), memperbarui peran anggota, dan menghapus anggota.

<CodeGroup>
```bash Shell
# Daftar anggota organisasi
curl "https://api.anthropic.com/v1/organizations/users?limit=10" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Perbarui peran anggota
curl "https://api.anthropic.com/v1/organizations/users/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"role": "developer"}'

# Hapus anggota
curl --request DELETE "https://api.anthropic.com/v1/organizations/users/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

</CodeGroup>

### Undangan Organisasi

Anda dapat mengundang pengguna ke organisasi dan mengelola [undangan](/docs/id/api/admin-api/invites/get-invite) tersebut.

<CodeGroup>

```bash Shell
# Buat undangan
curl --request POST "https://api.anthropic.com/v1/organizations/invites" \
  --header "anthropic-version: 2023-06-01" \
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

### Ruang Kerja

Untuk panduan komprehensif tentang ruang kerja, termasuk contoh Console dan API, lihat [Ruang Kerja](/docs/id/build-with-claude/workspaces).

### Anggota Ruang Kerja

Kelola [akses pengguna ke ruang kerja tertentu](/docs/id/api/admin-api/workspace_members/get-workspace-member):

<CodeGroup>

```bash Shell
# Tambahkan anggota ke ruang kerja
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "user_id": "user_xxx",
    "workspace_role": "workspace_developer"
  }'

# Daftar anggota ruang kerja
curl "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members?limit=10" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Perbarui peran anggota
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "workspace_role": "workspace_admin"
  }'

# Hapus anggota dari ruang kerja
curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

</CodeGroup>

### Kunci API

Pantau dan kelola [kunci API](/docs/id/api/admin-api/apikeys/get-api-key):

<CodeGroup>

```bash Shell
# Daftar kunci API
curl "https://api.anthropic.com/v1/organizations/api_keys?limit=10&status=active&workspace_id=wrkspc_xxx" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Perbarui kunci API
curl --request POST "https://api.anthropic.com/v1/organizations/api_keys/{api_key_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "status": "inactive",
    "name": "New Key Name"
  }'
```

</CodeGroup>

## Mengakses informasi organisasi

Dapatkan informasi tentang organisasi Anda secara terprogram dengan endpoint `/v1/organizations/me`.

Sebagai contoh:

```bash
curl "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "type": "organization",
  "name": "Organization Name"
}
```

Endpoint ini berguna untuk menentukan secara terprogram organisasi mana yang dimiliki kunci Admin API.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Informasi Organisasi](/docs/id/api/admin-api/organization/get-me).

## Laporan penggunaan dan biaya

Lacak penggunaan dan biaya organisasi Anda dengan [Usage and Cost API](/docs/id/build-with-claude/usage-cost-api).

## Analitik Claude Code

Pantau produktivitas pengembang dan adopsi Claude Code dengan [Claude Code Analytics API](/docs/id/build-with-claude/claude-code-analytics-api).

## Praktik terbaik

Untuk menggunakan Admin API secara efektif:

- Gunakan nama dan deskripsi yang bermakna untuk ruang kerja dan kunci API
- Implementasikan penanganan kesalahan yang tepat untuk operasi yang gagal
- Audit peran dan izin anggota secara teratur
- Bersihkan ruang kerja yang tidak digunakan dan undangan yang kedaluwarsa
- Pantau penggunaan kunci API dan putar kunci secara berkala

## FAQ

<section title="Izin apa yang diperlukan untuk menggunakan Admin API?">

Hanya anggota organisasi dengan peran admin yang dapat menggunakan Admin API. Mereka juga harus memiliki kunci Admin API khusus (dimulai dengan `sk-ant-admin`).

</section>

<section title="Bisakah saya membuat kunci API baru melalui Admin API?">

Tidak, kunci API baru hanya dapat dibuat melalui Claude Console untuk alasan keamanan. Admin API hanya dapat mengelola kunci API yang sudah ada.

</section>

<section title="Apa yang terjadi pada kunci API saat menghapus pengguna?">

Kunci API tetap dalam keadaan saat ini karena mereka dibatasi pada Organisasi, bukan pada pengguna individual.

</section>

<section title="Bisakah admin organisasi dihapus melalui API?">

Tidak, anggota organisasi dengan peran admin tidak dapat dihapus melalui API untuk alasan keamanan.

</section>

<section title="Berapa lama undangan organisasi berlaku?">

Undangan organisasi kedaluwarsa setelah 21 hari. Saat ini tidak ada cara untuk mengubah periode kedaluwarsa ini.

</section>

Untuk pertanyaan khusus ruang kerja, lihat [FAQ Ruang Kerja](/docs/id/build-with-claude/workspaces#faq).