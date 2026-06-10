---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: d0b3aeb6f85fb46115c5dc6561b93fde5aab3c74500b0837455a2319259b7095
---

# Membuat daftar organisasi, pengguna, peran, dan grup

Enumerasi organisasi di bawah organisasi induk Anda, beserta pengguna, peran, dan grupnya melalui Compliance API.

---

<Note>
  Compliance API diaktifkan berdasarkan permintaan. Organisasi Claude Enterprise memiliki akses ke API lengkap; organisasi Claude Console hanya memiliki akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_org_data` pada Compliance Access Key. Endpoint pengguna dan anggota grup memerlukan `read:compliance_user_data` sebagai gantinya.

  Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai adalah satu-satunya jenis kunci yang diterima; lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Panggilan yang diautentikasi dengan kunci Admin API (`sk-ant-admin01-...`) akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).
</Check>

Endpoint pada halaman ini mengekspos sisi direktori dari organisasi Claude Enterprise: organisasi yang tertaut, pengguna di setiap organisasi, peran yang didefinisikan pada masing-masing, serta grup berbasis "role-based access control" (kontrol akses berbasis peran), atau RBAC, maupun grup yang disediakan melalui "System for Cross-domain Identity Management" (Sistem untuk Manajemen Identitas Lintas Domain), atau SCIM, beserta anggotanya. Gunakan endpoint ini untuk menyiapkan daftar pengguna eDiscovery, membangun dasbor pelaporan, dan merekonsiliasi keanggotaan grup dengan sistem catatan eksternal. Compliance Access Key terikat pada organisasi induk dan mengembalikan data dari setiap organisasi tertaut di bawahnya, sehingga satu kunci dapat menjangkau seluruh pohon organisasi.

## Membuat daftar organisasi \{#list-organizations}

Endpoint [List organizations](/docs/id/api/compliance/organizations/list) mengembalikan setiap organisasi di bawah organisasi induk tempat kunci tersebut terikat.

Panggilan berikut membuat daftar setiap organisasi di bawah organisasi induk Anda. Responsnya berupa satu array `data` berisi record organisasi yang diurutkan berdasarkan `created_at` secara menaik. Endpoint ini mengembalikan hingga 1.000 organisasi dalam satu panggilan; jika pohon organisasi Anda melebihi jumlah tersebut, endpoint akan mengembalikan [error 500](/docs/id/manage-claude/compliance-errors#500-internal-server-error).

<CodeGroup>
```bash cURL nocheck
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "name": "Acme Engineering",
      "created_at": "2025-06-01T10:00:00Z"
    },
    {
      "uuid": "5a1b2c3d-4e5f-6789-abcd-ef0123456789",
      "name": "Acme Legal",
      "created_at": "2025-07-15T14:30:00Z"
    }
  ]
}
```

Field `uuid` adalah pengidentifikasi kanonis untuk pencarian selanjutnya. Tabel berikut memetakannya ke pengidentifikasi organisasi lainnya di seluruh Compliance API:

| Field                | Lokasi                                                                                                                                                                                                  | Hubungan dengan `uuid`                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| `{org_uuid}`         | Parameter path pada endpoint per-organisasi di halaman ini                                                                                                                                              | Nilai yang sama                                   |
| `organization_uuid`  | Record Activity Feed, chat, dan proyek                                                                                                                                                               | Nilai yang sama; gabungkan langsung pada kedua field ini |
| `organization_id`    | Record Activity Feed, chat, dan proyek                                                                                                                                                               | Organisasi yang sama, dengan prefiks `org_`. Sudah tidak digunakan lagi (deprecated) pada record chat dan proyek; gunakan `organization_uuid` sebagai gantinya. |
| `organization_ids[]` | Filter pada [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dan [Mengambil chat dan pesan](/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) | Menerima `uuid` atau bentuk dengan prefiks `org_`   |

Sebagian besar API Anthropic lainnya menggunakan bentuk dengan prefiks `org_`.

Jika pohon organisasi Anda melebihi batas 1.000 organisasi, hubungi dukungan Anthropic. Untuk melacak perubahan keanggotaan organisasi dari waktu ke waktu, panggil ulang endpoint ini secara berkala. Activity Feed juga menampilkan peristiwa keanggotaan melalui tipe aktivitas `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, dan `org_join_proposal_decided`; lihat [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

## Membuat daftar pengguna organisasi \{#list-organization-users}

Endpoint [List organization users](/docs/id/api/compliance/organizations/users/list) mengembalikan daftar record pengguna yang dipaginasi untuk satu organisasi.

Endpoint ini memerlukan `read:compliance_user_data`, bukan `read:compliance_org_data`. Buat Compliance Access Key dengan kedua scope tersebut jika Anda bermaksud menggunakannya untuk enumerasi direktori; jika tidak, panggilan akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Lihat [List organization users](/docs/id/api/compliance/organizations/users/list) di referensi API untuk nilai default dan rentang parameter kueri `limit` dan `page`.

Hasil diurutkan berdasarkan tanggal bergabung ke organisasi secara menaik. Berbeda dengan kursor `before_id`/`after_id` pada Activity Feed (lihat [Memaginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results)), endpoint direktori melakukan paginasi dengan token `next_page`: ketika `has_more` bernilai `true`, teruskan kembali `next_page` tanpa perubahan sebagai parameter kueri `page` pada permintaan berikutnya.

<CodeGroup>
```bash cURL nocheck
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/users" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "limit=500"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "full_name": "Priya Sharma",
      "email": "priya@example.com",
      "organization_role": "admin",
      "created_at": "2025-06-01T10:00:00Z"
    }
  ],
  "has_more": true,
  "next_page": "page_8aW5kZXgicG9zaXRpb25fdG9rZW5fOTE0"
}
```

ID pengguna yang dikembalikan di sini adalah pengidentifikasi `user_...` yang sama dengan yang diterima oleh filter `actor_ids[]` pada [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dan filter `user_ids[]` pada [Mengambil chat dan pesan](/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages). Field `organization_role` berisi tingkat keanggotaan bawaan pengguna dalam organisasi yang terdaftar (salah satu dari `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, atau `user`), sebuah sumbu yang independen dari penetapan peran RBAC kustom apa pun yang dikembalikan oleh [Membuat daftar peran](#list-roles). Alur eDiscovery yang umum membuat daftar pengguna untuk satu atau beberapa organisasi, memfilternya terhadap catatan eksternal Anda sendiri, lalu memasukkan ID yang dihasilkan ke dalam kueri chat dan proyek.

Seorang pengguna hanya muncul di sini selama mereka masih menjadi anggota aktif organisasi. Pengguna yang telah dihapus akan langsung dihilangkan dari daftar. Aktivitas historis mereka tetap dapat dikueri melalui Activity Feed selama jendela retensi penuh, diindeks dengan ID `user_...` yang sama.

## Membuat daftar peran \{#list-roles}

Endpoint [List Compliance Roles](/docs/id/api/compliance/organizations/roles/list) mengembalikan daftar record peran yang dipaginasi yang didefinisikan pada satu organisasi, dan [Get Compliance Role](/docs/id/api/compliance/organizations/roles/retrieve) mengembalikan satu peran berdasarkan ID.

Kedua endpoint peran memerlukan `read:compliance_org_data`. Endpoint daftar menerima parameter `limit` dan `page` yang sama seperti [Membuat daftar pengguna organisasi](#list-organization-users).

<CodeGroup>
```bash cURL nocheck
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/${org_uuid}/roles" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "rbac_role_01N2pQrS8tUvWxYz5AbCdEfGh",
      "name": "Compliance Reviewer",
      "description": "Read-only access to chat and project content for legal review.",
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

Lihat skema respons [List Compliance Roles](/docs/id/api/compliance/organizations/roles/list) untuk bentuk lengkap record peran. Untuk membuat daftar izin yang saat ini diberikan kepada suatu peran, gunakan [List Compliance Role Permissions](/docs/id/api/compliance/organizations/roles/permissions/list). Untuk mengaudit penetapan peran historis dan perubahan izin, kueri tipe aktivitas RBAC (misalnya, `rbac_role_assigned` dan `rbac_role_permission_added`) melalui Activity Feed; lihat [Memfilter aktivitas](/docs/id/manage-claude/compliance-activity-feed#filter-activities).

## Membuat daftar grup dan anggota \{#list-groups-and-members}

Endpoint [List Compliance Groups](/docs/id/api/compliance/groups/list) mengembalikan daftar grup RBAC dan grup yang disediakan melalui SCIM yang dipaginasi, dan [Get Compliance Group](/docs/id/api/compliance/groups/retrieve) mengembalikan satu grup berdasarkan ID. Endpoint [List Compliance Group Members](/docs/id/api/compliance/groups/members/list) mengembalikan anggota dari satu grup.

Endpoint daftar dan pengambilan grup memerlukan `read:compliance_org_data`. Endpoint anggota memerlukan `read:compliance_user_data`. Buat kunci dengan kedua scope tersebut untuk menelusuri grup secara menyeluruh. Kedua endpoint daftar menerima parameter `limit` dan `page` yang sama seperti [Membuat daftar pengguna organisasi](#list-organization-users).

Lihat skema respons [List Compliance Groups](/docs/id/api/compliance/groups/list) untuk bentuk lengkap record grup. Array `roles` berisi daftar ID peran yang ditetapkan ke grup, yang cocok dengan ID dari [Membuat daftar peran](#list-roles). `source_type` adalah pembeda antara grup yang dibuat secara manual melalui claude.ai (`direct`) dan grup yang disinkronkan dari penyedia identitas eksternal melalui SCIM (`scim`).

Buat daftar grup, lalu untuk setiap grup buat daftar anggotanya:

<CodeGroup>
```bash cURL nocheck
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/groups" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK",
      "name": "Engineering",
      "description": "Engineering team members",
      "source_type": "scim",
      "roles": ["rbac_role_01N2pQrS8tUvWxYz5AbCdEfGh"],
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

Untuk setiap ID grup, buat daftar anggotanya:

<CodeGroup>
```bash cURL nocheck
group_id="rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/groups/$group_id/members" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "user_id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "email": "priya@example.com",
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

Lihat skema respons [List Compliance Group Members](/docs/id/api/compliance/groups/members/list) untuk bentuk lengkap record anggota. Field `user_id` adalah pengidentifikasi `user_...` yang sama dengan yang diterima oleh Activity Feed dan daftar chat. Untuk mendapatkan nama lengkap anggota, cari melalui daftar pengguna organisasi.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Referensi API organisasi Compliance" href="/docs/id/api/compliance/organizations">
    Skema permintaan dan respons lengkap untuk setiap endpoint organisasi, pengguna, peran, dan grup.
  </Card>
  <Card title="Menangani error Compliance API" href="/docs/id/manage-claude/compliance-errors">
    Payload error secara verbatim dan cara memperbaiki masing-masing.
  </Card>
</CardGroup>