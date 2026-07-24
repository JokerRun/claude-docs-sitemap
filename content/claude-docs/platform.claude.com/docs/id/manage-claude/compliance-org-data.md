---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 47564fbcc97cd6315c4663ffd7860d7cb2dbd1aefd4d371f0cc1f88babef4cc3
---

# Daftar organisasi, pengguna, peran, grup, dan pengaturan

Enumerasi organisasi di bawah organisasi induk Anda (pengguna, peran, dan grupnya) dan baca pengaturan efektif setiap organisasi melalui Compliance API.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_org_data` pada Compliance Access Key. Endpoint pengguna dan anggota grup memerlukan `read:compliance_user_data` sebagai gantinya.

  Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai adalah satu-satunya jenis kunci yang diterima; lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Panggilan yang diautentikasi dengan kunci Admin API (`sk-ant-admin01-...`) mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).
</Check>

Endpoint pada halaman ini mengekspos sisi direktori dari organisasi Claude Enterprise: organisasi yang tertaut, pengguna di masing-masing organisasi, peran yang didefinisikan pada masing-masing, dan grup "role-based access control" (kontrol akses berbasis peran), atau RBAC, atau grup yang disediakan melalui "SCIM (System for Cross-domain Identity Management)" beserta anggotanya. Gunakan endpoint ini untuk menyemai daftar pengguna eDiscovery, membangun dasbor pelaporan, dan merekonsiliasi keanggotaan grup terhadap sistem pencatatan eksternal. Compliance Access Key yang mencakup organisasi induk mengembalikan data dari setiap organisasi tertaut di bawahnya, sehingga satu kunci menjangkau seluruh pohon. [Endpoint effective-settings](#get-effective-organization-settings) melengkapi direktori: endpoint ini mengembalikan pengaturan privasi data, keamanan, dan kapabilitas yang benar-benar berlaku untuk satu organisasi.

## Daftar organisasi

Endpoint [List organizations](/docs/id/api/compliance/organizations/list) mengembalikan setiap organisasi di bawah induk tempat kunci terikat.

Panggilan berikut mencantumkan setiap organisasi di bawah induk Anda. Responsnya adalah array `data` berisi rekaman organisasi yang diurutkan berdasarkan `created_at` secara menaik, ditambah `has_more` dan `next_page` untuk paginasi. Ketika `has_more` bernilai `true`, kirimkan kembali token `next_page` yang dikembalikan tanpa perubahan sebagai parameter kueri `page` pada permintaan berikutnya. Lihat [List organizations](/docs/id/api/compliance/organizations/list) di referensi API untuk nilai default dan rentang parameter `limit` dan `page`.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/organizations" \
    -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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
  ],
  "has_more": false,
  "next_page": null
}
```

Field `uuid` adalah pengidentifikasi kanonis untuk pencarian lanjutan. Tabel berikut memetakannya ke pengidentifikasi organisasi lainnya di seluruh Compliance API:

| Field                | Lokasi                                                                                                                                                                                            | Hubungan dengan `uuid`                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{org_uuid}`         | Parameter path pada endpoint per-organisasi di halaman ini                                                                                                                                        | Nilai yang sama                                                                                                                                                   |
| `organization_uuid`  | Rekaman Activity Feed, chat, dan proyek                                                                                                                                                           | Nilai yang sama; gabungkan kedua field ini secara langsung                                                                                                        |
| `organization_id`    | Rekaman Activity Feed, chat, dan proyek                                                                                                                                                           | Organisasi yang sama, dengan awalan `org_`. Tidak digunakan lagi pada rekaman chat dan proyek; gunakan `organization_uuid` sebagai gantinya.                      |
| `organization_ids[]` | Filter pada [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dan [Mengambil chat dan pesan](/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) | Menerima `uuid` atau bentuk berawalan `org_`                                                                                                                      |
| `organization_id`    | Respons [Effective organization settings](#get-effective-organization-settings)                                                                                                                   | Nilai yang sama, UUID polos; respons ini **tidak** menggunakan bentuk berawalan `org_` yang dibawa `organization_id` pada rekaman Activity Feed, chat, dan proyek |

Sebagian besar API Anthropic lainnya menggunakan bentuk berawalan `org_`.

Untuk melacak perubahan keanggotaan organisasi dari waktu ke waktu, panggil ulang endpoint ini secara berkala, mengikuti token `next_page` melalui setiap halaman pada setiap putaran. Activity Feed juga menampilkan peristiwa keanggotaan melalui jenis aktivitas `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, dan `org_join_proposal_decided`; lihat [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

## Daftar pengguna organisasi

Endpoint [List organization users](/docs/id/api/compliance/organizations/users/list) mengembalikan daftar berpaginasi berisi rekaman pengguna untuk satu organisasi.

Endpoint ini memerlukan `read:compliance_user_data`, bukan `read:compliance_org_data`. Buat Compliance Access Key dengan kedua scope tersebut jika Anda bermaksud menggunakannya untuk enumerasi direktori; jika tidak, panggilan akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Lihat [List organization users](/docs/id/api/compliance/organizations/users/list) di referensi API untuk nilai default dan rentang parameter kueri `limit` dan `page`.

Hasil diurutkan berdasarkan tanggal bergabung ke organisasi secara menaik. Berbeda dengan kursor `before_id`/`after_id` pada Activity Feed (lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results)), endpoint direktori melakukan paginasi dengan token `next_page`: ketika `has_more` bernilai `true`, kirimkan kembali `next_page` tanpa perubahan sebagai parameter kueri `page` pada permintaan berikutnya.

<CodeGroup>
  ```bash cURL
  org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/users" \
    -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
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

ID pengguna yang dikembalikan di sini adalah pengidentifikasi `user_...` yang sama yang diterima oleh filter `actor_ids[]` pada [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dan filter `user_ids[]` pada [Mengambil chat dan pesan](/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages). Field `organization_role` membawa tingkat keanggotaan bawaan pengguna dalam organisasi yang tercantum (salah satu dari `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, atau `user`), sebuah sumbu yang independen dari penugasan peran RBAC kustom apa pun yang dikembalikan oleh [Daftar peran](#list-roles). Alur eDiscovery yang umum mencantumkan pengguna untuk satu atau beberapa organisasi, memfilternya terhadap catatan eksternal Anda sendiri, dan memasukkan ID yang dihasilkan ke dalam kueri chat dan proyek.

Seorang pengguna hanya muncul di sini selama mereka menjadi anggota aktif organisasi. Pengguna yang dihapus langsung dikeluarkan dari daftar. Aktivitas historis mereka tetap dapat dikueri melalui Activity Feed selama jendela retensi penuh, diindeks dengan ID `user_...` yang sama.

## Daftar peran

Endpoint [List Compliance Roles](/docs/id/api/compliance/organizations/roles/list) mengembalikan daftar berpaginasi berisi rekaman peran yang didefinisikan pada satu organisasi, dan [Get Compliance Role](/docs/id/api/compliance/organizations/roles/retrieve) mengembalikan satu peran berdasarkan ID.

Kedua endpoint peran memerlukan `read:compliance_org_data`. Endpoint daftar menerima parameter `limit` dan `page` yang sama dengan [endpoint pengguna organisasi](#list-organization-users).

<CodeGroup>
  ```bash cURL
  org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/organizations/${org_uuid}/roles" \
    -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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

Lihat skema respons [List Compliance Roles](/docs/id/api/compliance/organizations/roles/list) untuk bentuk lengkap rekaman peran. Untuk mencantumkan izin yang saat ini diberikan kepada suatu peran, gunakan [List Compliance Role Permissions](/docs/id/api/compliance/organizations/roles/permissions/list). Untuk mengaudit penugasan peran historis dan perubahan izin, kueri jenis aktivitas RBAC (misalnya, `rbac_role_assigned` dan `rbac_role_permission_added`) melalui Activity Feed; lihat [Memfilter aktivitas](/docs/id/manage-claude/compliance-activity-feed#filter-activities).

## Daftar grup dan anggota

Endpoint [List Compliance Groups](/docs/id/api/compliance/groups/list) mengembalikan daftar berpaginasi berisi grup RBAC dan grup yang disediakan melalui SCIM, dan [Get Compliance Group](/docs/id/api/compliance/groups/retrieve) mengembalikan satu grup berdasarkan ID. Endpoint [List Compliance Group Members](/docs/id/api/compliance/groups/members/list) mengembalikan anggota dari satu grup.

Endpoint daftar dan pengambilan grup memerlukan `read:compliance_org_data`. Endpoint anggota memerlukan `read:compliance_user_data`. Buat kunci dengan kedua scope untuk menelusuri grup dari awal hingga akhir. Kedua endpoint daftar menerima parameter `limit` dan `page` yang sama dengan [endpoint pengguna organisasi](#list-organization-users).

Lihat skema respons [List Compliance Groups](/docs/id/api/compliance/groups/list) untuk bentuk lengkap rekaman grup. Array `roles` mencantumkan ID peran yang ditugaskan ke grup, yang cocok dengan ID dari [Daftar peran](#list-roles). `source_type` adalah pembeda antara grup yang dibuat secara manual melalui claude.ai (`direct`) dan grup yang disinkronkan dari penyedia identitas eksternal melalui SCIM (`scim`).

Cantumkan grup, lalu untuk setiap grup cantumkan anggotanya:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/groups" \
    -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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

Untuk setiap ID grup, cantumkan anggotanya:

<CodeGroup>
  ```bash cURL
  group_id="rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK"

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/groups/$group_id/members" \
    -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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

Lihat skema respons [List Compliance Group Members](/docs/id/api/compliance/groups/members/list) untuk bentuk lengkap rekaman anggota. Field `user_id` adalah pengidentifikasi `user_...` yang sama yang diterima oleh Activity Feed dan daftar chat. Untuk mendapatkan nama lengkap anggota, cari melalui daftar pengguna organisasi.

## Mendapatkan pengaturan organisasi efektif

Endpoint [Get effective organization settings](/docs/id/api/compliance/organizations/settings/retrieve) mengembalikan pengaturan yang berlaku untuk satu organisasi di bawah induk Anda: keadaan yang diberlakukan setelah pembatasan regulasi (seperti HIPAA), aturan ketersediaan fitur, nilai default jenis organisasi, dan ketergantungan antar-fitur diterapkan, yang dapat berbeda dari apa yang dikonfigurasi oleh administrator. Gunakan endpoint ini untuk memastikan bahwa jendela retensi, penyuntingan konten, penegakan single sign-on, daftar IP yang diizinkan, dan kontrol durasi sesi sesuai dengan baseline terdokumentasi Anda, tanpa akses Console administrator.

Endpoint ini memerlukan `read:compliance_org_data`; kunci tanpa scope tersebut mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden). Target harus merupakan salah satu organisasi tertaut dari induk: organisasi induk itu sendiri bukan target yang valid. Organisasi yang tidak dikenal, ID organisasi yang bukan UUID valid, organisasi di luar pohon induk Anda, dan organisasi induk yang belum memiliki akses ke endpoint ini semuanya mengembalikan [404 Not Found](/docs/id/manage-claude/compliance-errors#404-not-found) yang sama, sehingga 404 tidak mengungkapkan apakah suatu organisasi ada. Endpoint pengaturan diaktifkan per organisasi induk secara terpisah dari bagian lain Compliance API; jika setiap permintaan mengembalikan 404, hubungi perwakilan Anthropic Anda.

<Note>
  Sebelum 30 Juni 2026, endpoint ini memerlukan scope terpisah `read:compliance_org_settings`. Scope tersebut telah dihentikan: scope itu tidak lagi dapat dipilih atau diberikan saat membuat kunci, dan kunci yang hanya membawa scope yang telah dihentikan tersebut mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden). Buat Compliance Access Key baru dengan `read:compliance_org_data` sebagai gantinya.
</Note>

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/settings" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Responsnya adalah daftar baris pengaturan bertipe, dan baris mana yang muncul bervariasi menurut organisasi: pengaturan yang tidak dapat diubah oleh administrator organisasi, karena dikendalikan oleh kebijakan Anthropic atau tidak tersedia untuk organisasi tersebut, dihilangkan dari daftar. Perlakukan baris yang hilang sebagai "tidak dapat dikendalikan oleh administrator organisasi ini", bukan sebagai "nonaktif". Contoh ringkas berikut menunjukkan tiga dari baris yang dapat dimuat dalam respons:

```json Response
{
  "type": "effective_organization_settings",
  "organization_id": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "settings": [
    {
      "name": "data_retention_periods",
      "type": "data_retention",
      "value": {
        "chat": {
          "type": "fixed",
          "timescale": "day",
          "duration": 90
        }
      }
    },
    {
      "name": "content_redaction_enabled",
      "type": "boolean",
      "value": true
    },
    {
      "name": "ip_allowlist_ip_ranges",
      "type": "string_list",
      "value": ["10.0.0.0/8", "203.0.113.0/24"]
    }
  ],
  "api_keys": [
    {
      "type": "compliance_api_key",
      "id": "apikey_01Hx7k2mP9nQ4rS6tU8vW0xY",
      "name": "Compliance Export Key",
      "scopes": ["read:compliance_activities", "read:compliance_org_data"],
      "is_active": true,
      "created_at": "2026-03-14T09:30:00Z",
      "created_by_id": "user_01Jz3a4bC5dE6fG7hI8jK9lM",
      "expires_at": null
    }
  ]
}
```

Setiap baris membawa `name`, `type`, dan `value`; field `type` (`boolean`, `integer`, `string_list`, `provisioning_mode`, atau `data_retention`) memberi tahu Anda bentuk dari `value`. Daftar lengkap nama pengaturan, dan skema `value` untuk setiap tipe, ada di [Get effective organization settings](/docs/id/api/compliance/organizations/settings/retrieve) di referensi API.

Array `api_keys` mencantumkan setiap Compliance Access Key yang dikonfigurasi untuk organisasi induk Anda, sehingga daftar yang sama dikembalikan terlepas dari organisasi tertaut mana yang Anda kueri. Setiap entri membawa `type` kunci (`compliance_api_key`), `id`, `name`, `scopes`, flag `is_active`, stempel waktu `created_at` dan `expires_at`, serta `created_by_id` (ID pengguna yang membuat kunci; dapat bernilai `null`). Nilai rahasia kunci tidak pernah dikembalikan. Kunci yang dinonaktifkan disertakan dengan `is_active: false` sehingga Anda dapat meninjau kunci yang sebelumnya memiliki akses, dan kunci yang hanya membawa scope `read:compliance_org_settings` yang telah dihentikan tetap ada dalam daftar untuk visibilitas audit dan pembersihan meskipun scope tersebut tidak lagi memberikan akses.

`organization_id` tingkat atas adalah UUID polos organisasi: nilai yang sama dengan `uuid` dalam daftar organisasi, bukan bentuk berawalan `org_` yang dibawa `organization_id` pada rekaman Activity Feed, chat, dan proyek (lihat [tabel pengidentifikasi organisasi](#list-organizations)).

Baris mencerminkan keadaan yang diberlakukan, bukan konfigurasi yang terakhir disimpan: misalnya, `sso_provisioning_mode` melaporkan mode SCIM yang dikonfigurasi hanya selama sinkronisasi direktori diaktifkan, `ip_allowlist_enabled` bernilai `true` hanya selama daftar yang diizinkan aktif dan memiliki setidaknya satu rentang aktif, dan `code_execution_network_egress_enabled` bernilai `false` setiap kali eksekusi kode nonaktif.

Respons mencerminkan keadaan pada saat pembacaan; tidak ada yang di-snapshot. Perubahan pada sebagian besar pengaturan ini muncul sebagai peristiwa di [Activity Feed](/docs/id/manage-claude/compliance-activity-feed); gunakan endpoint ini untuk keadaan terselesaikan saat ini dan gunakan feed untuk mengaudit siapa yang mengubah apa, dan kapan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API organisasi Compliance" href="/docs/id/api/compliance/organizations">
    Skema permintaan dan respons lengkap untuk setiap endpoint organisasi, pengguna, peran, grup, dan pengaturan.
  </Card>

  <Card title="Menangani error Compliance API" href="/docs/id/manage-claude/compliance-errors">
    Payload error verbatim dan perbaikan untuk masing-masing.
  </Card>
</CardGroup>
