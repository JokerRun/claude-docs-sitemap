---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 2e1648d3c68d0e1b9047cb018ea75ec3337ad59dfc37acb547432fb574525471
---

---
title: Admin API
url: https://platform.claude.com/docs/id/manage-claude/admin-api
description: Kelola anggota organisasi, workspace, undangan, dan kunci API secara terprogram dengan Admin API, menggunakan kunci Admin API atau token OAuth `org:admin`.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

[Admin API](https://platform.claude.com/docs/id/api/admin) memungkinkan Anda mengelola sumber daya organisasi Anda secara terprogram, termasuk anggota organisasi, workspace, dan kunci API. Ini memberikan kontrol terprogram atas tugas-tugas administratif yang jika tidak akan memerlukan konfigurasi manual di [Claude Console](https://platform.claude.com/).

<Check>
  **Admin API memerlukan akses khusus**

  Admin API menerima dua kredensial:

  * **Kunci Admin API** (diawali dengan `sk-ant-admin...`) yang dikirim dalam header `x-api-key`. Hanya anggota organisasi dengan peran admin yang dapat membuatnya. Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).
  * **Token bearer OAuth** dengan cakupan `org:admin` yang dikirim dalam header `authorization: Bearer`. Hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperolehnya. Lihat [Memperoleh token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token).
</Check>

<Note>
  **Claude Enterprise:** Organisasi Claude Enterprise (claude.ai) juga menggunakan Admin API, dengan kunci API bercakupan yang dibuat di claude.ai. Dari endpoint di halaman ini, hanya endpoint anggota dan undangan yang tersedia bagi mereka, di samping endpoint khusus Claude Enterprise: pembacaan grup dan peran kustom, serta [batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api). Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) untuk Claude Enterprise.
</Note>

<Note>
  **Claude Platform on AWS:** Sebagian besar Admin API tidak tersedia di Claude Platform on AWS. Endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) tersedia. Endpoint lain termasuk anggota organisasi, anggota workspace, undangan, kunci API, laporan penggunaan, laporan biaya, dan laporan batas laju tidak tersedia. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk detailnya.
</Note>

## Autentikasi

Lakukan autentikasi dengan salah satu kredensial. Kunci Admin API mencakup sebagian besar endpoint; endpoint service-account, federation-issuer, dan federation-rule hanya menerima token OAuth `org:admin`. Contoh berikut memanggil [endpoint info organisasi](https://platform.claude.com/docs/id/manage-claude/admin-api#accessing-organization-info) dengan kedua cara.

### Token bearer OAuth

Login dengan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) menggunakan profil khusus, dengan meminta cakupan `org:admin` (lihat [Akses admin](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor token bearer. Profil khusus menjaga agar perintah rutin Anda tidak berjalan dengan akses yang ditingkatkan:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_OAUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek; jika permintaan mulai mengembalikan 401, jalankan ulang perintah `export`, yang akan menyegarkan token secara otomatis.

Panggil Admin API dengan token yang telah diekspor:

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Token `org:admin` memberikan akses ke seluruh organisasi, terlepas dari workspace tempat profil yang mendasarinya atau [aturan federasi](https://platform.claude.com/docs/id/manage-claude/admin-api#federation-rules) terikat.

Untuk CI dan beban kerja non-interaktif lainnya, terbitkan token dengan Workload Identity Federation alih-alih login secara interaktif. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#workload-ci-and-automation).

### Kunci Admin API

Untuk membuat kunci Admin API bagi jenis organisasi Anda, lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Cara kerja Admin API

Saat Anda menggunakan Admin API:

1. Anda membuat permintaan menggunakan salah satu kredensial dari bagian [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication)

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

Terdapat lima peran tingkat organisasi. Lihat detail lebih lanjut di artikel [Peran dan izin API Console](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions).

| Peran              | Izin                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------- |
| user               | Dapat menggunakan Playground                                                             |
| claude\_code\_user | Dapat menggunakan Playground dan [Claude Code](https://code.claude.com/docs/en/overview) |
| developer          | Dapat menggunakan Playground dan mengelola kunci API                                     |
| billing            | Dapat menggunakan Playground dan mengelola detail penagihan                              |
| admin              | Dapat melakukan semua hal di atas, ditambah mengelola pengguna                           |

Owner dan primary owner organisasi memiliki semua izin admin dan juga dapat mengelola admin. Semua rujukan ke peran admin di halaman ini juga berlaku untuk owner dan primary owner.

## Konsep utama

### Anggota organisasi

Anda dapat menampilkan daftar [anggota organisasi](https://platform.claude.com/docs/id/api/admin-api/users/get-user), memperbarui peran anggota, dan menghapus anggota.

<CodeGroup>
  ```bash cURL
  # Daftar anggota organisasi
  curl "https://api.anthropic.com/v1/organizations/users?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Perbarui peran anggota
  curl "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{"role": "developer"}'

  # Hapus anggota
  curl --request DELETE "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Undangan organisasi

Anda dapat mengundang pengguna ke organisasi dan mengelola [undangan](https://platform.claude.com/docs/id/api/admin-api/invites/get-invite) tersebut.

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

### Workspace

Untuk panduan lengkap tentang workspace, termasuk contoh Console dan API, lihat [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces).

### Anggota workspace

Kelola [akses pengguna ke workspace tertentu](https://platform.claude.com/docs/id/api/admin-api/workspace_members/get-workspace-member):

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

### Kunci API

Pantau dan kelola [kunci API](https://platform.claude.com/docs/id/api/admin/api_keys/list). Setiap kunci dalam respons menyertakan timestamp `expires_at` (`null` untuk kunci tanpa [kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration)):

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

### Service account

Buat dan kelola service account (`svac_...`), identitas non-manusia yang diperankan oleh token [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Kunci Admin API tidak diterima pada endpoint service-account, federation-issuer, atau federation-rule; gunakan token OAuth `org:admin`. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#service-accounts).

### Federation issuer

Daftarkan penyedia identitas OIDC (`fdis_...`) yang tokennya dapat menyatakan identitas beban kerja untuk organisasi Anda. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-issuers).

### Federation rule

Kelola aturan (`fdrl_...`) yang memetakan token issuer ke service account dan cakupan. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-rules).

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

Endpoint ini berguna untuk menentukan secara terprogram organisasi mana yang memiliki suatu kunci Admin API.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Info Organisasi](https://platform.claude.com/docs/id/api/admin-api/organization/get-me).

## Laporan penggunaan dan biaya

Lacak penggunaan dan biaya organisasi Anda dengan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api).

## Analitik Claude Code

Pantau produktivitas developer dan adopsi Claude Code dengan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api).

## Batas laju

Baca "rate limit" (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Compliance API

Ambil data audit dan aktivitas untuk organisasi Anda dengan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Kunci Admin API hanya dapat membaca Activity Feed; untuk akses penuh, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

## Praktik terbaik

Untuk menggunakan Admin API secara efektif:

* Gunakan nama dan deskripsi yang bermakna untuk workspace dan kunci API
* Terapkan penanganan error yang tepat untuk operasi yang gagal
* Audit peran dan izin anggota secara berkala
* Bersihkan workspace yang tidak digunakan dan undangan yang kedaluwarsa
* Pantau penggunaan kunci API, audit [`expires_at`](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) setiap kunci, dan rotasi kunci secara berkala

## FAQ

<AccordionGroup>
  <Accordion title="Izin apa yang diperlukan untuk menggunakan Admin API?">
    Admin API menerima kunci Admin API (diawali dengan `sk-ant-admin`) atau token bearer OAuth dengan cakupan `org:admin`. Hanya anggota organisasi dengan peran admin yang dapat membuat kunci Admin API, dan hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperoleh token `org:admin`. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication).
  </Accordion>

  <Accordion title="Dapatkah saya membuat kunci API baru melalui Admin API?">
    Tidak, kunci API baru hanya dapat dibuat melalui Claude Console demi alasan keamanan. Admin API hanya dapat mengelola kunci API yang sudah ada.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API saat menghapus pengguna?">
    Kunci API tetap dalam keadaannya saat ini karena cakupannya adalah organisasi, bukan pengguna individual.
  </Accordion>

  <Accordion title="Dapatkah admin organisasi dihapus melalui API?">
    Tidak, anggota organisasi dengan peran admin tidak dapat dihapus melalui API demi alasan keamanan.
  </Accordion>

  <Accordion title="Berapa lama undangan organisasi berlaku?">
    Undangan organisasi kedaluwarsa setelah 21 hari. Saat ini tidak ada cara untuk mengubah periode kedaluwarsa ini.
  </Accordion>
</AccordionGroup>

Untuk pertanyaan khusus workspace, lihat [FAQ Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#faq).
