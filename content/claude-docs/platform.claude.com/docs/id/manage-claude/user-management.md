---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-management
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: a97b8e4031de4d323352b13f713126055ae8a1e3c37f851d6f2c9d21af5f063f
---

---
title: Manajemen pengguna
url: https://platform.claude.com/docs/id/manage-claude/user-management
description: "Kelola orang-orang di organisasi Claude Enterprise Anda dengan Admin API: daftar anggota dan ubah peran, kirim dan tarik undangan, kelola grup, dan baca peran kustom."
---

Halaman ini membahas pengelolaan orang-orang di organisasi **Claude Enterprise** (claude.ai) Anda secara terprogram, menggunakan [Admin API](https://platform.claude.com/docs/id/api/admin): mendaftar anggota dan mencarinya berdasarkan alamat email, mengubah peran anggota, menghapus anggota, mengirim dan menarik undangan, mengelola grup enterprise Anda beserta keanggotaannya, dan membaca peran kustom organisasi Anda. Untuk organisasi Claude Console (Claude Platform), lihat [panduan Admin API untuk Claude Console](https://platform.claude.com/docs/id/manage-claude/admin-api).

<Note>
  Permintaan grup dan peran kustom tidak memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `anthropic-beta: ce-user-management-2026-07-13`. Permintaan yang masih mengirimkannya tetap diterima dan berperilaku identik.
</Note>

## Endpoint mana yang dapat digunakan organisasi Anda?

Admin API adalah satu set endpoint di bawah `https://api.anthropic.com/v1/organizations/`. Organisasi Claude Console dan Claude Enterprise melakukan autentikasi dengan [kunci yang berbeda](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) dan masing-masing memiliki akses ke subset endpoint yang berbeda:

| Endpoint                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Claude Console (Claude Platform)                                                                 | Claude Enterprise (claude.ai)      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ---------------------------------- |
| [Anggota](https://platform.claude.com/docs/id/manage-claude/user-management#members) dan [undangan](https://platform.claude.com/docs/id/manage-claude/user-management#invites)                                                                                                                                                                                                                                                                               | Tersedia; lihat [panduan Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) | Tersedia (halaman ini)             |
| [Grup](https://platform.claude.com/docs/id/manage-claude/user-management#groups)                                                                                                                                                                                                                                                                                                                                                                             | Tidak tersedia                                                                                   | Tersedia (halaman ini)             |
| [Peran kustom](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles)                                                                                                                                                                                                                                                                                                                                                               | Tidak tersedia                                                                                   | Tersedia, hanya-baca (halaman ini) |
| [Batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api)                                                                                                                                                                                                                                                                                                                                                                      | Tidak tersedia                                                                                   | Tersedia                           |
| [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces), [kunci API](https://platform.claude.com/docs/id/manage-claude/admin-api#api-keys), [laporan penggunaan dan biaya](https://platform.claude.com/docs/id/manage-claude/usage-cost-api), [batas laju](https://platform.claude.com/docs/id/manage-claude/rate-limits-api), dan endpoint lainnya dalam [panduan Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) | Tersedia                                                                                         | Tidak tersedia                     |

Anggota dan undangan adalah endpoint yang sama untuk kedua jenis organisasi; halaman ini mendokumentasikan perilakunya pada Claude Enterprise, termasuk [peran organisasi](https://platform.claude.com/docs/id/manage-claude/user-management#organization-roles) Claude Enterprise. Endpoint grup dan peran kustom hanya ada untuk Claude Enterprise.

<Check>
  **Diperlukan kunci Admin API dengan scope**

  Endpoint ini memerlukan kunci Admin API dengan scope `read:members` (endpoint `GET` anggota dan undangan, serta semua endpoint peran kustom; tidak ada scope peran terpisah), scope `write:members` (endpoint `POST` dan `DELETE` anggota dan undangan), scope `read:rbac_groups` (endpoint `GET` grup), atau scope `write:rbac_groups` (endpoint `POST` dan `DELETE` grup). Kunci yang membawa scope `read:org_audit` (scope hanya-baca untuk integrasi audit keamanan) juga dapat memanggil setiap endpoint `GET` di halaman ini dan endpoint baca [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana primary owner Anda membuatnya dan scope mana yang harus dipilih. Sertakan kunci tersebut dalam header `x-api-key` pada setiap permintaan. Permintaan anggota dan undangan juga memerlukan header `anthropic-version: 2023-06-01`, seperti ditunjukkan dalam contoh; permintaan grup dan peran kustom tidak memerlukannya.
</Check>

## Ikhtisar

Halaman ini membahas lima sumber daya:

| Sumber daya      | Endpoint                                                                                                                                                                                                                  | Digunakan untuk                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Anggota**      | `GET /v1/organizations/users` `GET /v1/organizations/users/{user_id}` `POST /v1/organizations/users/{user_id}` `DELETE /v1/organizations/users/{user_id}`                                                                 | Mendaftar anggota organisasi atau mencari satu anggota berdasarkan email; mengubah peran anggota; menghapus anggota.          |
| **Undangan**     | `POST /v1/organizations/invites` `GET /v1/organizations/invites` `GET /v1/organizations/invites/{invite_id}` `DELETE /v1/organizations/invites/{invite_id}`                                                               | Mengundang seseorang ke organisasi, melacak status undangan, dan menariknya sebelum diterima.                                 |
| **Grup**         | `GET /v1/organizations/rbac_groups` `GET /v1/organizations/rbac_groups/{group_id}` `POST /v1/organizations/rbac_groups` `POST /v1/organizations/rbac_groups/{group_id}` `DELETE /v1/organizations/rbac_groups/{group_id}` | Membaca grup enterprise Anda dan peran kustom yang terlampir pada masing-masing; membuat, mengganti nama, dan menghapus grup. |
| **Anggota grup** | `GET /v1/organizations/rbac_groups/{group_id}/members` `POST /v1/organizations/rbac_groups/{group_id}/members` `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`                                        | Membaca anggota grup; menambah dan menghapus anggota.                                                                         |
| **Peran kustom** | `GET /v1/organizations/rbac_roles` `GET /v1/organizations/rbac_roles/{role_id}` `GET /v1/organizations/rbac_roles/{role_id}/permissions`                                                                                  | Membaca peran kustom organisasi Anda dan izin yang diberikan setiap peran.                                                    |

Peran kustom dan pelampirannya ke grup dikelola di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings); API membacanya tetapi tidak dapat mengubahnya.

## Mulai cepat

Daftar anggota organisasi, yang terbaru lebih dulu:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

```json
{
  "data": [
    {
      "type": "user",
      "id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "name": "Jane Smith",
      "role": "user",
      "added_at": "2026-06-12T09:14:03Z"
    }
  ],
  "has_more": false,
  "first_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "last_id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

## Konsep utama

### Peran organisasi

Setiap anggota memiliki tepat satu peran organisasi. Pembacaan mengembalikan peran anggota sebagai salah satu dari lima nilai:

| Peran              | Arti                                                                             |
| ------------------ | -------------------------------------------------------------------------------- |
| `user`             | Anggota standar.                                                                 |
| `managed`          | Anggota yang izinnya diberikan melalui peran kustom yang terlampir pada grupnya. |
| `owner`            | Pemilik organisasi.                                                              |
| `membership_admin` | Anggota yang dapat mengelola anggota organisasi.                                 |
| `primary_owner`    | Pemilik utama organisasi. Hanya ada tepat satu.                                  |

API hanya dapat menetapkan peran `user` dan `managed`, pada pembuatan undangan dan pada pembaruan peran. Peran administratif (`owner`, `membership_admin`, dan `primary_owner`) ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat diubah atau dihapus melalui API ini.

### Anggota dan undangan

Seseorang menjadi anggota dengan menerima undangan (atau melalui single sign-on organisasi Anda, jika dikonfigurasi). Membuat undangan akan mengirim email undangan; undangan tersebut kemudian terbaca sebagai `pending` hingga penerima menerimanya (`accepted`) atau `expires_at` yang ditetapkan server terlewati (`expired`). Hanya undangan `pending` yang dapat ditarik. Untuk mengubah alamat email atau peran undangan yang masih pending, tarik undangan tersebut dan buat yang baru.

Jika paket organisasi Anda mengambil anggota dari kumpulan seat terbatas yang telah dibeli, undangan pending menggunakan satu seat. Endpoint pembuatan undangan tidak menerima parameter seat atau tier: seat ditetapkan secara otomatis dari tier terendah yang masih tersedia. Membuat undangan ketika tidak ada seat yang kosong akan gagal dengan error 400, bukan membeli seat. Menarik undangan, membiarkannya kedaluwarsa, atau menghapus anggota di kemudian hari akan mengembalikan seat ke kumpulan.

### Grup dan peran

Grup menghubungkan anggota ke peran kustom ("role-based access control" (kontrol akses berbasis peran), atau RBAC, yaitu `rbac` dalam path endpoint dan nama scope). Grup dimiliki oleh enterprise Anda secara keseluruhan (organisasi induk bersama setiap organisasi di bawahnya), bukan oleh satu organisasi, sehingga scope grup (`read:rbac_groups` dan `write:rbac_groups`) memerlukan kunci yang dibuat untuk semua organisasi tertaut. Setiap grup membawa `source_type`: `direct` untuk grup yang dibuat di claude.ai, `scim` untuk grup yang diprovisikan oleh penyedia identitas Anda. Field `roles` pada grup mencantumkan ID peran kustom yang terlampir padanya; uraikan menjadi nama dan izin dengan [endpoint peran kustom](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles), dengan catatan bahwa katalog peran bersifat per-organisasi sementara grup berlaku di seluruh enterprise, sehingga mengambil peran yang dimiliki organisasi lain dalam enterprise Anda akan mengembalikan 404 untuk kunci Anda. Field ini bernilai `null` (bukan `[]`) ketika data peran sementara tidak tersedia, jadi coba lagi untuk membedakan pembacaan yang terdegradasi dari grup yang tidak memiliki peran.

## Batas laju

Endpoint Admin API berbagi batas per-organisasi sebesar **100 permintaan per menit**; pembuatan undangan memiliki batasnya sendiri sebesar **1.200 permintaan per jam**. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi

Daftar anggota dan undangan menggunakan paginasi berbasis ID: sertakan `limit` (default 20, maks 1000) ditambah paling banyak satu dari `before_id` atau `after_id`, dan lakukan paginasi menggunakan field `first_id` dan `last_id` dari setiap respons hingga `has_more` bernilai `false`. Daftar grup dan peran kustom menggunakan **kursor opak**: nilai `next_page` dari respons diteruskan tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, hingga `next_page` bernilai `null`.

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Error](https://platform.claude.com/docs/id/api/errors).

## Anggota

### Mendaftar anggota

`GET /v1/organizations/users` mengembalikan anggota organisasi, yang paling baru ditambahkan lebih dulu. Filter berdasarkan `email` untuk mencari anggota tertentu; pencocokan tidak peka huruf besar-kecil dan mentoleransi varian umum dari alamat yang sama (misalnya, `jane+hiring@example.com` cocok dengan `jane@example.com`). Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List users](https://platform.claude.com/docs/id/api/admin/users/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users?email=jane@example.com" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mendapatkan anggota

`GET /v1/organizations/users/{user_id}` mengembalikan satu anggota berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get user](https://platform.claude.com/docs/id/api/admin/users/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mengubah peran anggota

`POST /v1/organizations/users/{user_id}` menetapkan peran anggota menjadi `user` atau `managed`. Anggota yang memegang peran administratif (`owner`, `membership_admin`, atau `primary_owner`) tidak dapat diubah melalui endpoint ini, dan peran administratif tidak dapat ditetapkan; keduanya mengembalikan 400 dan dikelola di pengaturan organisasi claude.ai. Jika penyedia identitas organisasi Anda mengelola peran (SSO lanjutan atau provisi SCIM lanjutan), pembaruan peran mengembalikan 400. Memerlukan scope `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Update user](https://platform.claude.com/docs/id/api/admin/users/update) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"role": "managed"}'
```

### Menghapus anggota

`DELETE /v1/organizations/users/{user_id}` menghapus anggota dari organisasi, mengembalikan seat yang telah dibeli yang mereka tempati ke kumpulan organisasi. Anggota yang memegang peran administratif tidak dapat dihapus melalui endpoint ini, dan jika penyedia identitas Anda mengelola keanggotaan (SCIM), penghapusan mengembalikan 400. Memerlukan scope `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Remove user](https://platform.claude.com/docs/id/api/admin/users/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

```json
{
  "type": "user_deleted",
  "id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

## Undangan

### Membuat undangan

`POST /v1/organizations/invites` mengirim email undangan dan mengembalikan undangan dengan `expires_at` yang ditetapkan server. `role` harus `user` atau `managed`. Jika undangan pending sudah ada untuk alamat email tersebut, atau alamat tersebut sudah dimiliki oleh seorang anggota, permintaan mengembalikan 400 yang menyebutkan sumber daya yang sudah ada. Organisasi yang penyedia identitasnya memprovisikan pengguna secara otomatis (JIT atau SCIM) tidak dapat membuat undangan melalui API. Memerlukan scope `write:members`.

Pada paket yang mengambil anggota dari kumpulan seat terbatas, undangan secara otomatis mengambil seat dari tier terendah yang masih tersedia; API tidak menerima parameter tier. Jika tidak ada seat yang kosong, permintaan gagal dengan error 400, bukan membeli seat. Tambahkan seat melalui manajemen paket organisasi dan coba lagi.

Field opsional `rbac_group_ids` mencantumkan grup (berdasarkan ID berawalan `rbac_group_`) yang akan ditetapkan kepada anggota ketika mereka menerima undangan. Menyertakan `rbac_group_ids` yang tidak kosong juga mengharuskan kunci membawa scope `write:rbac_groups`, karena penetapan grup dapat memberikan izin yang terlampir pada peran grup tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [Create invite](https://platform.claude.com/docs/id/api/admin/invites/create) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/invites" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "email": "newhire@example.com",
    "role": "managed",
    "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
  }'
```

```json
{
  "type": "invite",
  "id": "invite_01QrStUvWxYzAbCdEfGhIj",
  "email": "newhire@example.com",
  "role": "managed",
  "invited_at": "2026-07-06T16:20:11Z",
  "expires_at": "2026-07-27T16:20:11Z",
  "accepted_at": null,
  "status": "pending",
  "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
}
```

### Mendaftar undangan

`GET /v1/organizations/invites` mengembalikan undangan organisasi, yang terbaru lebih dulu, mencakup status `pending`, `accepted`, dan `expired`; tidak ada filter status. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List invites](https://platform.claude.com/docs/id/api/admin/invites/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mendapatkan undangan

`GET /v1/organizations/invites/{invite_id}` mengembalikan satu undangan berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get invite](https://platform.claude.com/docs/id/api/admin/invites/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Menarik undangan

`DELETE /v1/organizations/invites/{invite_id}` menarik undangan `pending`, menonaktifkan tautan dalam email undangan. Menarik undangan `accepted` mengembalikan 400 (hapus anggotanya sebagai gantinya); menarik undangan `expired` mengembalikan 400. Memerlukan scope `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete invite](https://platform.claude.com/docs/id/api/admin/invites/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## Grup

Grup yang dibuat langsung oleh enterprise Anda, di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau melalui API ini (`source_type: "direct"`), mendukung setiap endpoint di bagian ini. Grup yang diprovisikan oleh penyedia identitas Anda (`source_type: "scim"`) dapat dibaca tetapi tidak dapat diubah: mengganti nama atau menghapus grup SCIM, atau mengubah keanggotaannya, mengembalikan 400, karena penyedia identitas Anda yang memilikinya. Berbeda dengan permintaan anggota dan undangan, permintaan grup tidak memerlukan header `anthropic-version`.

### Mendaftar grup

`GET /v1/organizations/rbac_groups` mengembalikan grup enterprise Anda, termasuk grup yang dikelola penyedia identitas (`scim`). Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [List groups](https://platform.claude.com/docs/id/api/admin/rbac_groups/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_group",
      "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "name": "Engineering",
      "source_type": "direct",
      "roles": ["rbac_role_01CdEfGhIjKlMnOpQrStUv"],
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Mendapatkan grup

`GET /v1/organizations/rbac_groups/{group_id}` mengembalikan satu grup berdasarkan ID. Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Get group](https://platform.claude.com/docs/id/api/admin/rbac_groups/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Membuat grup

`POST /v1/organizations/rbac_groups` membuat grup dengan `name` yang diberikan (1–255 karakter) tanpa peran atau anggota. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Create group](https://platform.claude.com/docs/id/api/admin/rbac_groups/create) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"name": "Engineering"}'
```

```json
{
  "type": "rbac_group",
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "name": "Engineering",
  "source_type": "direct",
  "roles": [],
  "created_at": "2026-07-09T18:00:00Z",
  "updated_at": "2026-07-09T18:00:00Z"
}
```

### Mengganti nama grup

`POST /v1/organizations/rbac_groups/{group_id}` memperbarui grup. `name` adalah satu-satunya field yang dapat diubah endpoint ini. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Update group](https://platform.claude.com/docs/id/api/admin/rbac_groups/update) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"name": "Platform Engineering"}'
```

### Menghapus grup

`DELETE /v1/organizations/rbac_groups/{group_id}` menghapus grup. Anggotanya tetap menjadi anggota organisasi mereka, tetapi kehilangan izin dari peran yang terlampir pada grup tersebut, dan [batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api) grup, jika ada, berhenti berlaku bagi mereka. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete group](https://platform.claude.com/docs/id/api/admin/rbac_groups/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "type": "rbac_group_deleted"
}
```

### Mendaftar anggota grup

`GET /v1/organizations/rbac_groups/{group_id}/members` mengembalikan anggota grup (masing-masing dengan `user_id` dan email mereka), yang terlama lebih dulu. Hanya anggota saat ini dari organisasi enterprise Anda yang dikembalikan, sehingga satu halaman mungkin berisi kurang dari `limit` entri sementara `has_more` bernilai `true`. Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [List group members](https://platform.claude.com/docs/id/api/admin/rbac_groups/members/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members?limit=100" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_group_member",
      "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "created_at": "2026-04-07T12:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Menambahkan anggota ke grup

`POST /v1/organizations/rbac_groups/{group_id}/members` menambahkan anggota organisasi ke grup berdasarkan `user_id`. Pengguna tersebut harus sudah menjadi anggota salah satu organisasi enterprise Anda (jika tidak, permintaan mengembalikan 404), dan menambahkan seseorang yang sudah ada di grup mengembalikan 400. Untuk grup `scim`, keanggotaan dikelola di penyedia identitas Anda dan permintaan ini mengembalikan 400. Untuk menetapkan grup kepada seseorang yang belum bergabung, gunakan `rbac_group_ids` pada [pembuatan undangan](https://platform.claude.com/docs/id/manage-claude/user-management#create-an-invite). Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Add group member](https://platform.claude.com/docs/id/api/admin/rbac_groups/members/create) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"user_id": "user_01AbCdEfGhIjKlMnOpQrSt"}'
```

```json
{
  "type": "rbac_group_member",
  "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "email": "jane@example.com",
  "created_at": "2026-07-09T18:00:00Z"
}
```

### Menghapus anggota dari grup

`DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}` menghapus anggota dari grup; mereka tetap menjadi anggota organisasi mereka. Permintaan mengembalikan 404 jika pengguna bukan anggota grup, dan 400 untuk grup `scim`, yang keanggotaannya dikelola di penyedia identitas Anda. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Remove group member](https://platform.claude.com/docs/id/api/admin/rbac_groups/members/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "type": "rbac_group_member_deleted"
}
```

## Peran kustom

Peran kustom bersifat hanya-baca melalui API: endpoint ini mengatalogkan peran kustom organisasi Anda (yang didefinisikan di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau diprovisikan oleh Anthropic) dan izin yang diberikan setiap peran. Pembacaan peran kustom menggunakan scope `read:members` (tidak ada scope peran terpisah) dan berfungsi dengan kunci tingkat organisasi: berbeda dengan endpoint grup, endpoint ini tidak memerlukan kunci yang dibuat untuk semua organisasi tertaut, dan katalog yang dikembalikan adalah milik organisasi Anda sendiri.

### Mendaftar peran

`GET /v1/organizations/rbac_roles` mengembalikan peran kustom organisasi Anda. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List roles](https://platform.claude.com/docs/id/api/admin/rbac_roles/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_role",
      "id": "rbac_role_01CdEfGhIjKlMnOpQrStUv",
      "name": "Engineering base",
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Mendapatkan peran

`GET /v1/organizations/rbac_roles/{role_id}` mengembalikan satu peran berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get role](https://platform.claude.com/docs/id/api/admin/rbac_roles/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Mendaftar izin peran

`GET /v1/organizations/rbac_roles/{role_id}/permissions` mengembalikan izin peran. Setiap izin memasangkan `resource` (apa yang menjadi sasarannya: fitur produk organisasi, alat konektor, scope OAuth konektor, satu konektor, atau setiap konektor) dengan `action` (apa yang diberikannya pada sumber daya tersebut). Baris untuk fitur yang tidak diaktifkan bagi organisasi Anda dihilangkan, sehingga satu halaman mungkin berisi kurang dari `limit` baris sementara `has_more` bernilai `true`. Memerlukan scope `read:members`.

Dua nilai `action` memerlukan perhatian khusus: izin `organization` yang action-nya `capability_access_all` (setiap fitur produk) atau `capability_access_all_ga` (setiap fitur produk stabil, yaitu setiap fitur yang tidak berlabel beta atau research preview) adalah pemberian menyeluruh (yang tidak mencakup akses model maupun izin panel admin berawalan `permission_`) dan dicantumkan sebagai satu baris tersebut, bukan diperluas. Ketika Anda menghitung apa yang diberikan suatu peran, perlakukan baris menyeluruh sebagai mencakup semua yang dijelaskan variannya, bukan hanya fitur yang disebutkan di baris lain.

Untuk detail parameter lengkap dan skema respons, lihat [List role permissions](https://platform.claude.com/docs/id/api/admin/rbac_roles/permissions/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv/permissions?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "organization",
        "organization_id": "12345678-1234-5678-1234-567812345678"
      },
      "action": "capability_access_all_ga"
    },
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "connector_tool",
        "connector_id": "mcpsrv_01WxYzAbCdEfGhIjKlMnOp",
        "tool_name": "search_tickets"
      },
      "action": "use"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Contoh alur kerja

### Offboarding karyawan yang keluar

1. Cari anggota berdasarkan email:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/users?email=departing@example.com" \
     -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     -H "anthropic-version: 2023-06-01"
   ```

2. Hapus mereka dengan `DELETE /v1/organizations/users/{user_id}`, menggunakan `id` dari respons. Seat mereka, jika ada, kembali ke kumpulan.

3. Jika orang tersebut belum bergabung, pencarian tidak mengembalikan anggota; daftar undangan dan tarik undangan `pending` mereka sebagai gantinya.

### Mengaudit keanggotaan grup

1. Daftar grup dan catat `id`, `name`, dan `roles` setiap grup.

2. Untuk setiap grup yang membawa peran sensitif, lakukan paginasi melalui `GET /v1/organizations/rbac_groups/{group_id}/members` dan bandingkan email anggota dengan daftar di penyedia identitas Anda.

3. Hapus anggota yang seharusnya tidak lagi berada di grup dengan `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`. Untuk grup `scim`, lakukan perubahan di penyedia identitas Anda.

## Pertanyaan yang sering diajukan

### Apakah ini API yang berbeda dari Admin API?

Tidak. Endpoint anggota dan undangan adalah endpoint `/v1/organizations/` yang sama dengan yang digunakan organisasi Claude Console; halaman ini mendokumentasikan perilakunya pada Claude Enterprise. Endpoint grup dan peran kustom adalah bagian dari API yang sama dan hanya ada untuk organisasi Claude Enterprise. [Tabel ketersediaan](https://platform.claude.com/docs/id/manage-claude/user-management#which-endpoints-can-your-organization-use) menunjukkan endpoint mana yang dapat dipanggil setiap jenis organisasi.

### Dapatkah saya menetapkan peran owner atau membership admin melalui API?

Tidak. API hanya menetapkan `user` dan `managed`, pada pembuatan undangan dan pembaruan peran. Peran administratif ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat diubah atau dihapus melalui API.

### Dapatkah saya membuat atau mengubah grup melalui API?

Ya, dengan scope `write:rbac_groups`: membuat, mengganti nama, dan menghapus grup, serta menambah atau menghapus anggotanya. Dua hal yang tidak dapat diubah API: grup yang diprovisikan oleh penyedia identitas Anda (`source_type: "scim"`), yang nama dan keanggotaannya dimiliki oleh penyedia identitas, dan peran kustom, yang dikelola di pengaturan organisasi claude.ai (API [membacanya](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles)).

### Apakah undangan yang belum diterima menggunakan seat?

Pada paket dengan kumpulan seat terbatas, ya: undangan `pending` menahan satu seat. Menarik undangan atau membiarkannya kedaluwarsa membebaskan seat tersebut. Pada paket tanpa kumpulan seat, undangan tidak menggunakan apa pun.

### Organisasi saya menggunakan single sign-on. Operasi mana yang berfungsi?

Jika penyedia identitas Anda memprovisikan pengguna secara otomatis (JIT atau SCIM), pembuatan undangan mengembalikan 400. Jika penyedia identitas mengelola peran (SSO lanjutan atau provisi SCIM lanjutan), pembaruan peran mengembalikan 400. Jika penyedia identitas mengelola keanggotaan (provisi SCIM), penghapusan anggota mengembalikan 400. Pembacaan tetap berfungsi dalam semua kasus.

### Apa yang terjadi pada kunci Admin API ketika orang yang membuatnya keluar?

Kunci tetap berfungsi. Kunci Admin API memiliki scope pada organisasi, bukan pada pengguna individu, dan kunci yang dibuat di claude.ai tidak kedaluwarsa. Menghapus pembuatnya dari organisasi atau mendeprovisikannya melalui penyedia identitas Anda mengakhiri akses mereka sendiri, tetapi tidak mengakhiri kunci yang mereka buat. Menurunkan peran mereka juga tidak mengubah kunci: setiap kunci tetap aktif dengan scope aslinya. Ketika Anda melakukan offboarding seseorang yang membuat kunci Admin API, hapus kunci tersebut di bagian **Keys** pada [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan buat penggantinya.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Membuat kunci Admin API" href="https://platform.claude.com/docs/id/manage-claude/admin-api-keys">
    Di mana primary owner Anda membuat kunci dengan scope dan scope mana yang harus dipilih.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-api">
    Audit aktivitas dan ambil atau hapus konten pengguna di seluruh organisasi Anda.
  </Card>

  <Card title="Analytics API" href="https://platform.claude.com/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan dan biaya per pengguna dan per rentang waktu untuk Claude Enterprise.
  </Card>

  <Card title="Spend Limits API" href="https://platform.claude.com/docs/id/manage-claude/spend-limits-api">
    Tetapkan batas pengeluaran per anggota dan tinjau permintaan kenaikan.
  </Card>
</CardGroup>
