---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 3df8e20a5eb714d4f5e38325c4b9c1052888b0869ee946f5794e90f8c7b9b97c
---

---
title: Daftar organisasi, pengguna, peran, grup, dan pengaturan
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
description: Enumerasi organisasi di bawah organisasi induk Anda (pengguna, peran, dan grupnya) dan baca pengaturan efektif setiap organisasi melalui Compliance API.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Cakupan yang diperlukan:** `read:compliance_org_data` pada Compliance Access Key. Endpoint pengguna dan anggota grup memerlukan `read:compliance_user_data` sebagai gantinya.

  Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai adalah satu-satunya jenis kunci yang diterima; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Panggilan yang diautentikasi dengan kunci Admin API (`sk-ant-admin01-...`) mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).
</Check>

Endpoint di halaman ini mengekspos sisi direktori dari organisasi Claude Enterprise: organisasi tertautnya, pengguna di masing-masing organisasi, peran yang didefinisikan pada masing-masing, serta grup "role-based access control" (kontrol akses berbasis peran), atau RBAC, maupun grup yang disediakan melalui SCIM (System for Cross-domain Identity Management) beserta anggotanya. Gunakan endpoint ini untuk mengisi daftar pengguna eDiscovery, membangun dasbor pelaporan, dan merekonsiliasi keanggotaan grup terhadap sistem pencatatan eksternal. Compliance Access Key yang mencakup organisasi induk mengembalikan data dari setiap organisasi tertaut di bawahnya, sehingga satu kunci menjangkau seluruh pohon. [Endpoint pengaturan efektif](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#get-effective-organization-settings) melengkapi direktori: endpoint ini mengembalikan pengaturan privasi data, keamanan, dan kapabilitas yang benar-benar berlaku untuk satu organisasi.

## Daftar organisasi

Endpoint [List organizations](https://platform.claude.com/docs/id/api/compliance/organizations/list) mengembalikan setiap organisasi di bawah induk tempat kunci tersebut terikat.

Panggilan berikut mendaftar setiap organisasi di bawah induk Anda. Responsnya adalah array `data` berisi catatan organisasi yang diurutkan berdasarkan `created_at` secara menaik, ditambah `has_more` dan `next_page` untuk paginasi. Ketika `has_more` bernilai `true`, teruskan kembali token `next_page` yang dikembalikan tanpa perubahan sebagai parameter query `page` pada permintaan berikutnya. Lihat [List organizations](https://platform.claude.com/docs/id/api/compliance/organizations/list) di referensi API untuk nilai default dan rentang parameter `limit` dan `page`.

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

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

Field `uuid` adalah pengidentifikasi kanonis untuk pencarian lanjutan. Tabel berikut memetakannya ke pengidentifikasi organisasi lain di seluruh Compliance API:

| Field                | Lokasi                                                                                                                                                                                                                                                                                                                                                                                                                          | Hubungan dengan `uuid`                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{org_uuid}`         | Parameter path pada endpoint per-organisasi di halaman ini                                                                                                                                                                                                                                                                                                                                                                      | Nilai yang sama                                                                                                                                                   |
| `organization_uuid`  | Catatan Activity Feed, chat, proyek, dan sesi                                                                                                                                                                                                                                                                                                                                                                                   | Nilai yang sama; gabungkan langsung pada kedua field ini                                                                                                          |
| `organization_id`    | Catatan Activity Feed, chat, dan proyek                                                                                                                                                                                                                                                                                                                                                                                         | Organisasi yang sama, dengan awalan `org_`. Tidak lagi digunakan pada catatan chat dan proyek; gunakan `organization_uuid` sebagai gantinya.                      |
| `organization_ids[]` | Filter pada [Query Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages), dan [daftar sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) (daftar sesi lokal tidak memiliki filter organisasi) | Menerima `uuid` atau bentuk berawalan `org_`                                                                                                                      |
| `organization_id`    | Respons [Pengaturan organisasi efektif](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#get-effective-organization-settings)                                                                                                                                                                                                                                                                              | Nilai yang sama, UUID polos; respons ini **tidak** menggunakan bentuk berawalan `org_` yang dibawa `organization_id` pada catatan Activity Feed, chat, dan proyek |

Sebagian besar API Anthropic lainnya menggunakan bentuk berawalan `org_`.

Untuk melacak perubahan keanggotaan organisasi dari waktu ke waktu, daftar ulang endpoint ini secara berkala, dengan mengikuti token `next_page` melalui setiap halaman pada setiap putaran. Activity Feed juga menampilkan peristiwa keanggotaan melalui tipe aktivitas `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, dan `org_join_proposal_decided`; lihat [Query Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

## Daftar pengguna organisasi

Endpoint [List organization users](https://platform.claude.com/docs/id/api/compliance/organizations/users/list) mengembalikan daftar catatan pengguna berpaginasi untuk satu organisasi.

Endpoint ini memerlukan `read:compliance_user_data`, bukan `read:compliance_org_data`. Buat Compliance Access Key dengan kedua cakupan jika Anda bermaksud menggunakannya untuk enumerasi direktori; jika tidak, panggilan akan mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Lihat [List organization users](https://platform.claude.com/docs/id/api/compliance/organizations/users/list) di referensi API untuk nilai default dan rentang parameter query `limit` dan `page`.

Hasil diurutkan berdasarkan tanggal bergabung ke organisasi secara menaik. Berbeda dengan kursor `before_id`/`after_id` pada Activity Feed (lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)), endpoint direktori melakukan paginasi dengan token `next_page`: ketika `has_more` bernilai `true`, teruskan kembali `next_page` tanpa perubahan sebagai parameter query `page` pada permintaan berikutnya.

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/users" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "limit=500"
```

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

ID pengguna yang dikembalikan di sini adalah pengidentifikasi `user_...` yang sama dengan yang diterima oleh filter `actor_ids[]` pada [Query Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dan filter `user_ids[]` pada [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) serta [daftar sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions); [daftar sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) tidak memiliki filter pengguna, jadi atribusikan sesi lokal berdasarkan `user.id` pada setiap objek sesi. Field `organization_role` membawa tingkat keanggotaan bawaan pengguna dalam organisasi yang didaftar (salah satu dari `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, atau `user`), sebuah sumbu yang independen dari penugasan peran RBAC kustom apa pun yang dikembalikan oleh [Daftar peran](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-roles). Alur eDiscovery yang umum mendaftar pengguna untuk satu atau lebih organisasi, memfilternya terhadap catatan eksternal Anda sendiri, dan memasukkan ID yang dihasilkan ke dalam query chat dan proyek.

Seorang pengguna hanya muncul di sini selama mereka menjadi anggota aktif organisasi. Pengguna yang dihapus langsung dikeluarkan dari daftar. Aktivitas historis mereka tetap dapat di-query melalui Activity Feed selama jendela retensi penuh, diindeks dengan ID `user_...` yang sama.

## Daftar peran

Endpoint [List Compliance Roles](https://platform.claude.com/docs/id/api/compliance/organizations/roles/list) mengembalikan daftar catatan peran berpaginasi yang didefinisikan pada satu organisasi, dan [Get Compliance Role](https://platform.claude.com/docs/id/api/compliance/organizations/roles/retrieve) mengembalikan satu peran berdasarkan ID.

Kedua endpoint peran memerlukan `read:compliance_org_data`. Endpoint daftar menerima parameter `limit` dan `page` yang sama dengan [endpoint pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users).

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/${org_uuid}/roles" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

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

Lihat skema respons [List Compliance Roles](https://platform.claude.com/docs/id/api/compliance/organizations/roles/list) untuk bentuk lengkap catatan peran. Untuk mendaftar izin yang saat ini diberikan kepada suatu peran, gunakan [List Compliance Role Permissions](https://platform.claude.com/docs/id/api/compliance/organizations/roles/permissions/list). Untuk mengaudit penugasan peran historis dan perubahan izin, query tipe aktivitas RBAC (misalnya, `rbac_role_assigned` dan `rbac_role_permission_added`) melalui Activity Feed; lihat [Memfilter aktivitas](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#filter-activities).

## Daftar grup dan anggota

Endpoint [List Compliance Groups](https://platform.claude.com/docs/id/api/compliance/groups/list) mengembalikan daftar berpaginasi grup RBAC dan grup yang disediakan melalui SCIM, dan [Get Compliance Group](https://platform.claude.com/docs/id/api/compliance/groups/retrieve) mengembalikan satu grup berdasarkan ID. Endpoint [List Compliance Group Members](https://platform.claude.com/docs/id/api/compliance/groups/members/list) mengembalikan anggota dari satu grup.

Endpoint daftar dan pengambilan grup memerlukan `read:compliance_org_data`. Endpoint anggota memerlukan `read:compliance_user_data`. Buat kunci dengan kedua cakupan untuk menelusuri grup dari ujung ke ujung. Kedua endpoint daftar menerima parameter `limit` dan `page` yang sama dengan [endpoint pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users).

Lihat skema respons [List Compliance Groups](https://platform.claude.com/docs/id/api/compliance/groups/list) untuk bentuk lengkap catatan grup. Array `roles` mendaftar ID peran yang ditugaskan ke grup, sesuai dengan ID dari [Daftar peran](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-roles). `source_type` adalah pembeda antara grup yang dibuat secara manual melalui claude.ai (`direct`) dan grup yang disinkronkan dari penyedia identitas eksternal melalui SCIM (`scim`).

Daftar grup, lalu untuk setiap grup daftar anggotanya:

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/groups" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

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

Untuk setiap ID grup, daftar anggotanya:

```bash cURL
group_id="rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/groups/$group_id/members" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

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

Lihat skema respons [List Compliance Group Members](https://platform.claude.com/docs/id/api/compliance/groups/members/list) untuk bentuk lengkap catatan anggota. Field `user_id` adalah pengidentifikasi `user_...` yang sama dengan yang diterima Activity Feed, daftar chat, dan daftar sesi remote; field ini juga cocok dengan `user.id` pada objek sesi lokal dan pada objek sesi remote milik pengguna (sesi remote milik agen membawa ID manusianya di `started_by_user.id` sebagai gantinya). Untuk mendapatkan nama lengkap anggota, cari melalui daftar pengguna organisasi.

## Mendapatkan pengaturan organisasi efektif

Endpoint [Get effective organization settings](https://platform.claude.com/docs/id/api/compliance/organizations/settings/retrieve) mengembalikan pengaturan yang berlaku untuk satu organisasi di bawah induk Anda: status yang ditegakkan setelah pembatasan regulasi (seperti HIPAA), aturan ketersediaan fitur, default tipe organisasi, dan dependensi antarfitur diterapkan, yang dapat berbeda dari apa yang dikonfigurasi administrator. Gunakan endpoint ini untuk membuktikan bahwa jendela retensi, redaksi konten, penegakan single sign-on, allowlist IP, dan kontrol durasi sesi sesuai dengan baseline terdokumentasi Anda, tanpa akses Console administrator.

Endpoint ini memerlukan `read:compliance_org_data`; kunci tanpa cakupan tersebut mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden). Target harus merupakan salah satu organisasi tertaut milik induk: organisasi induk itu sendiri bukan target yang valid. Organisasi yang tidak dikenal, ID organisasi yang bukan UUID valid, organisasi di luar pohon induk Anda, dan organisasi induk yang belum memiliki akses ke endpoint ini semuanya mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) yang sama, sehingga 404 tidak mengungkapkan apakah suatu organisasi ada. Endpoint pengaturan diaktifkan per organisasi induk secara terpisah dari bagian Compliance API lainnya; jika setiap permintaan mengembalikan 404, hubungi perwakilan Anthropic Anda.

<Note>
  Sebelum 30 Juni 2026, endpoint ini memerlukan cakupan terpisah `read:compliance_org_settings`. Cakupan tersebut telah dipensiunkan: cakupan ini tidak dapat lagi dipilih atau diberikan saat membuat kunci, dan kunci yang hanya membawa cakupan yang dipensiunkan tersebut mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden). Buat Compliance Access Key baru dengan `read:compliance_org_data` sebagai gantinya.
</Note>

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/settings" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Responsnya adalah daftar baris pengaturan bertipe, dan baris mana yang muncul bervariasi menurut organisasi: pengaturan yang tidak dapat diubah oleh administrator organisasi, karena dikendalikan oleh kebijakan Anthropic atau tidak tersedia untuk organisasi tersebut, dihilangkan dari daftar. Perlakukan baris yang tidak ada sebagai "tidak dapat dikendalikan oleh administrator organisasi ini", bukan sebagai "nonaktif". Contoh ringkas berikut menunjukkan tiga dari baris yang dapat dimuat sebuah respons:

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

Setiap baris membawa `name`, `type`, dan `value`; field `type` (`boolean`, `integer`, `string_list`, `provisioning_mode`, atau `data_retention`) memberi tahu Anda bentuk dari `value`. Daftar lengkap nama pengaturan, dan skema `value` untuk setiap tipe, terdapat di [Get effective organization settings](https://platform.claude.com/docs/id/api/compliance/organizations/settings/retrieve) di referensi API.

Array `api_keys` mendaftar setiap Compliance Access Key yang dikonfigurasi untuk organisasi induk Anda, sehingga daftar yang sama dikembalikan terlepas dari organisasi tertaut mana yang Anda query. Setiap entri membawa `type` kunci (`compliance_api_key`), `id`, `name`, `scopes`, flag `is_active`, stempel waktu `created_at` dan `expires_at`, serta `created_by_id` (ID pengguna yang membuat kunci; dapat bernilai `null`). Nilai rahasia kunci tidak pernah dikembalikan. Kunci yang dinonaktifkan disertakan dengan `is_active: false` sehingga Anda dapat meninjau kunci yang sebelumnya memiliki akses, dan kunci yang hanya membawa cakupan `read:compliance_org_settings` yang telah dipensiunkan tetap ada dalam daftar untuk visibilitas audit dan pembersihan meskipun cakupan tersebut tidak lagi memberikan akses.

`organization_id` tingkat atas adalah UUID polos organisasi: nilai yang sama dengan `uuid` dalam daftar organisasi, bukan bentuk berawalan `org_` yang dibawa `organization_id` pada catatan Activity Feed, chat, dan proyek (lihat [tabel pengidentifikasi organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organizations)).

Baris mencerminkan status yang ditegakkan, bukan konfigurasi yang terakhir disimpan: misalnya, `sso_provisioning_mode` melaporkan mode SCIM yang dikonfigurasi hanya selama sinkronisasi direktori diaktifkan, `ip_allowlist_enabled` bernilai `true` hanya selama allowlist aktif dan memiliki setidaknya satu rentang aktif, dan `code_execution_network_egress_enabled` bernilai `false` setiap kali eksekusi kode nonaktif.

Respons mencerminkan status pada saat pembacaan; tidak ada yang di-snapshot. Perubahan pada sebagian besar pengaturan ini muncul sebagai peristiwa di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed); gunakan endpoint ini untuk status terselesaikan saat ini dan feed untuk mengaudit siapa yang mengubah apa, dan kapan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API organisasi Compliance" href="https://platform.claude.com/docs/id/api/compliance/organizations">
    Skema permintaan dan respons lengkap untuk setiap endpoint organisasi, pengguna, peran, grup, dan pengaturan.
  </Card>

  <Card title="Menangani error Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-errors">
    Payload error verbatim dan perbaikan untuk masing-masing.
  </Card>
</CardGroup>
