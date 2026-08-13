---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 6dc1793191012a91662b7075df393aa72647ee82227d2436ad8c0fe0b5234a92
---

---
title: Mencantumkan organisasi, pengguna, peran, grup, dan pengaturan
url: https://platform.claude.com/docs/id/manage-claude/compliance-org-data
description: Enumerasi organisasi di bawah organisasi induk Anda (pengguna, peran, dan grup mereka) dan baca pengaturan efektif setiap organisasi melalui Compliance API.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_org_data` pada Compliance Access Key. Endpoint pengguna dan anggota grup memerlukan `read:compliance_user_data` sebagai gantinya.

  Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai adalah satu-satunya jenis kunci yang diterima; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Panggilan yang diautentikasi dengan kunci Admin API (`sk-ant-admin01-...`) mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).
</Check>

Endpoint pada halaman ini mengekspos sisi direktori dari organisasi Claude Enterprise: organisasi yang tertaut, pengguna di masing-masing organisasi, peran yang didefinisikan pada masing-masing organisasi, serta grup "role-based access control" (kontrol akses berbasis peran), atau RBAC, maupun grup yang disediakan melalui SCIM (System for Cross-domain Identity Management) beserta anggotanya. Gunakan endpoint ini untuk mengisi daftar pengguna eDiscovery, membangun dasbor pelaporan, dan merekonsiliasi keanggotaan grup terhadap sistem catatan eksternal. Compliance Access Key yang mencakup organisasi induk mengembalikan data dari setiap organisasi tertaut di bawahnya, sehingga satu kunci menjangkau seluruh pohon. [Endpoint pengaturan efektif](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#get-effective-organization-settings) melengkapi direktori: endpoint ini mengembalikan pengaturan privasi data, keamanan, dan kapabilitas yang benar-benar berlaku untuk satu organisasi.

## Mencantumkan organisasi

Endpoint [List organizations](https://platform.claude.com/docs/id/api/compliance/organizations/list) mengembalikan setiap organisasi di bawah induk tempat kunci tersebut terikat.

Panggilan berikut mencantumkan setiap organisasi di bawah induk Anda. Responsnya adalah array `data` berisi record organisasi yang diurutkan berdasarkan `created_at` secara menaik, ditambah `has_more` dan `next_page` untuk paginasi. Ketika `has_more` bernilai `true`, kirimkan kembali token `next_page` yang dikembalikan tanpa perubahan sebagai parameter kueri `page` pada permintaan Anda berikutnya. Lihat [List organizations](https://platform.claude.com/docs/id/api/compliance/organizations/list) di referensi API untuk nilai default dan rentang parameter `limit` dan `page`.

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

| Field                | Lokasi                                                                                                                                                                                                                                                                                                                                                                                                                                         | Hubungan dengan `uuid`                                                                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{org_uuid}`         | Parameter path pada endpoint per-organisasi di halaman ini                                                                                                                                                                                                                                                                                                                                                                                     | Nilai yang sama                                                                                                                                                        |
| `organization_uuid`  | Record Activity Feed, chat, project, dan session                                                                                                                                                                                                                                                                                                                                                                                               | Nilai yang sama; gabungkan langsung pada kedua field ini                                                                                                               |
| `organization_id`    | Record Activity Feed, chat, dan project                                                                                                                                                                                                                                                                                                                                                                                                        | Organisasi yang sama, dengan prefiks `org_`. Tidak digunakan lagi pada record chat dan project; gunakan `organization_uuid` sebagai gantinya.                          |
| `organization_ids[]` | Filter pada [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages), dan [Mengambil sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions) (daftar sesi lokal tidak memiliki filter organisasi) | Menerima `uuid` atau bentuk dengan prefiks `org_`                                                                                                                      |
| `organization_id`    | Respons [Pengaturan organisasi efektif](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#get-effective-organization-settings)                                                                                                                                                                                                                                                                                             | Nilai yang sama, UUID polos; respons ini **tidak** menggunakan bentuk dengan prefiks `org_` yang dibawa `organization_id` pada record Activity Feed, chat, dan project |

Sebagian besar API Anthropic lainnya menggunakan bentuk dengan prefiks `org_`.

Untuk melacak perubahan keanggotaan organisasi dari waktu ke waktu, cantumkan ulang endpoint ini secara berkala, dengan mengikuti token `next_page` melalui setiap halaman pada setiap iterasi. Activity Feed juga menampilkan peristiwa keanggotaan melalui jenis aktivitas `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, dan `org_join_proposal_decided`; lihat [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

## Mencantumkan pengguna organisasi

Endpoint [List organization users](https://platform.claude.com/docs/id/api/compliance/organizations/users/list) mengembalikan daftar record pengguna yang dipaginasi untuk satu organisasi.

Endpoint ini memerlukan `read:compliance_user_data`, bukan `read:compliance_org_data`. Buat Compliance Access Key dengan kedua scope tersebut jika Anda bermaksud menggunakannya untuk enumerasi direktori; jika tidak, panggilan akan mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Lihat [List organization users](https://platform.claude.com/docs/id/api/compliance/organizations/users/list) di referensi API untuk nilai default dan rentang parameter kueri `limit` dan `page`.

Hasil diurutkan berdasarkan tanggal bergabung ke organisasi secara menaik. Tidak seperti kursor `before_id`/`after_id` pada Activity Feed (lihat [Mempaginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)), endpoint direktori melakukan paginasi dengan token `next_page`: ketika `has_more` bernilai `true`, kirimkan kembali `next_page` tanpa perubahan sebagai parameter kueri `page` pada permintaan berikutnya.

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

ID pengguna yang dikembalikan di sini adalah pengidentifikasi `user_...` yang sama yang diterima oleh filter `actor_ids[]` pada [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dan filter `user_ids[]` pada [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) dan [Mengambil sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions); [daftar sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) tidak memiliki filter pengguna, jadi atribusikan sesi lokal berdasarkan `user.id` pada setiap objek sesi. Field `organization_role` membawa tingkat keanggotaan bawaan pengguna dalam organisasi yang dicantumkan (salah satu dari `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, atau `user`), sebuah sumbu yang independen dari penetapan peran RBAC kustom apa pun yang dikembalikan oleh [Mencantumkan peran](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-roles). Alur eDiscovery yang umum mencantumkan pengguna untuk satu atau beberapa organisasi, memfilternya terhadap catatan eksternal Anda sendiri, dan memasukkan ID yang dihasilkan ke dalam kueri chat dan project.

Seorang pengguna hanya muncul di sini selama mereka adalah anggota aktif dari organisasi tersebut. Pengguna yang dihapus langsung dihilangkan dari daftar. Aktivitas historis mereka tetap dapat dikueri melalui Activity Feed selama jendela retensi penuh, diindeks dengan ID `user_...` yang sama.

## Mencantumkan peran

Endpoint [List Compliance Roles](https://platform.claude.com/docs/id/api/compliance/organizations/roles/list) mengembalikan daftar record peran yang dipaginasi yang didefinisikan pada satu organisasi, dan [Get Compliance Role](https://platform.claude.com/docs/id/api/compliance/organizations/roles/retrieve) mengembalikan satu peran berdasarkan ID.

Kedua endpoint peran memerlukan `read:compliance_org_data`. Endpoint daftar menerima parameter `limit` dan `page` yang sama seperti [endpoint pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users).

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

Lihat skema respons [List Compliance Roles](https://platform.claude.com/docs/id/api/compliance/organizations/roles/list) untuk bentuk lengkap record peran. Untuk mencantumkan izin yang saat ini diberikan kepada suatu peran, gunakan [List Compliance Role Permissions](https://platform.claude.com/docs/id/api/compliance/organizations/roles/permissions/list). Untuk mengaudit penetapan peran historis dan perubahan izin, kueri jenis aktivitas RBAC (misalnya, `rbac_role_assigned` dan `rbac_role_permission_added`) melalui Activity Feed; lihat [Memfilter aktivitas](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#filter-activities).

## Mencantumkan grup dan anggota

Endpoint [List Compliance Groups](https://platform.claude.com/docs/id/api/compliance/groups/list) mengembalikan daftar grup RBAC dan grup yang disediakan melalui SCIM yang dipaginasi, dan [Get Compliance Group](https://platform.claude.com/docs/id/api/compliance/groups/retrieve) mengembalikan satu grup berdasarkan ID. Endpoint [List Compliance Group Members](https://platform.claude.com/docs/id/api/compliance/groups/members/list) mengembalikan anggota dari satu grup.

Endpoint daftar dan pengambilan grup memerlukan `read:compliance_org_data`. Endpoint anggota memerlukan `read:compliance_user_data`. Buat kunci dengan kedua scope tersebut untuk menelusuri grup dari awal hingga akhir. Kedua endpoint daftar menerima parameter `limit` dan `page` yang sama seperti [endpoint pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users).

Lihat skema respons [List Compliance Groups](https://platform.claude.com/docs/id/api/compliance/groups/list) untuk bentuk lengkap record grup. Array `roles` mencantumkan ID peran yang ditetapkan ke grup, yang cocok dengan ID dari [Mencantumkan peran](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-roles). `source_type` adalah pembeda antara grup yang dibuat secara manual melalui claude.ai (`direct`) dan grup yang disinkronkan dari penyedia identitas eksternal melalui SCIM (`scim`).

Cantumkan grup, lalu untuk setiap grup cantumkan anggotanya:

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

Untuk setiap ID grup, cantumkan anggotanya:

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

Lihat skema respons [List Compliance Group Members](https://platform.claude.com/docs/id/api/compliance/groups/members/list) untuk bentuk lengkap record anggota. Field `user_id` adalah pengidentifikasi `user_...` yang sama yang diterima oleh Activity Feed, daftar chat, dan daftar sesi jarak jauh; field ini juga cocok dengan `user.id` pada objek sesi lokal dan pada objek sesi jarak jauh yang dimiliki pengguna (sesi jarak jauh yang dimiliki agen membawa ID manusia di `started_by_user.id` sebagai gantinya). Untuk mendapatkan nama lengkap anggota, cari melalui daftar pengguna organisasi.

## Mendapatkan pengaturan organisasi efektif

Endpoint [Get effective organization settings](https://platform.claude.com/docs/id/api/compliance/organizations/settings/retrieve) mengembalikan pengaturan yang berlaku untuk satu organisasi di bawah induk Anda: keadaan yang diberlakukan setelah pembatasan regulasi (seperti HIPAA), aturan ketersediaan fitur, default jenis organisasi, dan dependensi antar-fitur diterapkan, yang dapat berbeda dari apa yang dikonfigurasi oleh administrator. Gunakan endpoint ini untuk membuktikan bahwa jendela retensi, redaksi konten, penegakan single sign-on, daftar izin IP, dan kontrol durasi sesi sesuai dengan baseline yang Anda dokumentasikan, tanpa akses Console administrator.

Endpoint ini memerlukan `read:compliance_org_data`; kunci tanpa scope tersebut mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden). Target harus merupakan salah satu organisasi tertaut dari induk: organisasi induk itu sendiri bukan target yang valid. Organisasi yang tidak dikenal, ID organisasi yang bukan UUID valid, organisasi di luar pohon induk Anda, dan organisasi induk yang belum memiliki akses ke endpoint ini semuanya mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) yang sama, sehingga 404 tidak mengungkapkan apakah suatu organisasi ada. Endpoint pengaturan diaktifkan per organisasi induk secara terpisah dari bagian Compliance API lainnya; jika setiap permintaan mengembalikan 404, hubungi perwakilan Anthropic Anda.

<Note>
  Sebelum 30 Juni 2026, endpoint ini memerlukan scope terpisah `read:compliance_org_settings`. Scope tersebut telah dihentikan: scope tersebut tidak dapat lagi dipilih atau diberikan saat membuat kunci, dan kunci yang hanya membawa scope yang dihentikan tersebut mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden). Buat Compliance Access Key baru dengan `read:compliance_org_data` sebagai gantinya.
</Note>

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/settings" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Responsnya adalah daftar baris pengaturan bertipe, dan baris mana yang muncul bervariasi menurut organisasi: pengaturan yang tidak dapat diubah oleh administrator organisasi, karena dikendalikan oleh kebijakan Anthropic atau tidak tersedia untuk organisasi tersebut, dihilangkan dari daftar. Perlakukan baris yang hilang sebagai "tidak dapat dikontrol oleh administrator organisasi ini", bukan sebagai "nonaktif". Contoh singkat berikut menunjukkan tiga dari baris yang dapat dimuat dalam respons:

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

Setiap baris membawa `name`, `type`, dan `value`; field `type` (`boolean`, `integer`, `string_list`, `provisioning_mode`, atau `data_retention`) memberi tahu Anda bentuk dari `value`. Daftar lengkap nama pengaturan, dan skema `value` untuk setiap tipe, ada di [Get effective organization settings](https://platform.claude.com/docs/id/api/compliance/organizations/settings/retrieve) di referensi API.

Array `api_keys` mencantumkan setiap Compliance Access Key yang dikonfigurasi untuk organisasi induk Anda, sehingga daftar yang sama dikembalikan terlepas dari organisasi tertaut mana yang Anda kueri. Setiap entri membawa `type` kunci (`compliance_api_key`), `id`, `name`, `scopes`, flag `is_active`, timestamp `created_at` dan `expires_at`, serta `created_by_id` (ID pengguna yang membuat kunci; dapat bernilai `null`). Nilai rahasia kunci tidak pernah dikembalikan. Kunci yang dinonaktifkan disertakan dengan `is_active: false` sehingga Anda dapat meninjau kunci yang sebelumnya memiliki akses, dan kunci yang hanya membawa scope `read:compliance_org_settings` yang telah dihentikan tetap ada dalam daftar untuk visibilitas audit dan pembersihan meskipun scope tersebut tidak lagi memberikan akses.

`organization_id` tingkat atas adalah UUID polos organisasi: nilai yang sama dengan `uuid` dalam daftar organisasi, bukan bentuk dengan prefiks `org_` yang dibawa `organization_id` pada record Activity Feed, chat, dan project (lihat [tabel pengidentifikasi organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organizations)).

Baris mencerminkan keadaan yang diberlakukan, bukan konfigurasi yang terakhir disimpan: misalnya, `sso_provisioning_mode` melaporkan mode SCIM yang dikonfigurasi hanya selama sinkronisasi direktori diaktifkan, `ip_allowlist_enabled` bernilai `true` hanya selama daftar izin aktif dan memiliki setidaknya satu rentang aktif, dan `code_execution_network_egress_enabled` bernilai `false` setiap kali eksekusi kode dinonaktifkan.

Respons mencerminkan keadaan pada waktu pembacaan; tidak ada yang di-snapshot. Perubahan pada sebagian besar pengaturan ini muncul sebagai peristiwa di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed); gunakan endpoint ini untuk keadaan terselesaikan saat ini dan gunakan feed untuk mengaudit siapa yang mengubah apa, dan kapan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API organisasi Compliance" href="https://platform.claude.com/docs/id/api/compliance/organizations">
    Skema permintaan dan respons lengkap untuk setiap endpoint organisasi, pengguna, peran, grup, dan pengaturan.
  </Card>

  <Card title="Menangani error Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-errors">
    Payload error secara verbatim dan perbaikan untuk masing-masing.
  </Card>
</CardGroup>
