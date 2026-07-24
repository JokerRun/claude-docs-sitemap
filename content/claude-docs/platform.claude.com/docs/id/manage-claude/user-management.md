---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-management
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: b460c7dff4a7a3051ccf71c54ecfc9536a119deb5a25715a23c788e1f95689c9
---

# Manajemen pengguna

Kelola orang-orang di organisasi Claude Enterprise Anda dengan Admin API: daftar anggota dan ubah peran, kirim dan tarik undangan, kelola grup, dan baca peran kustom.

---

Halaman ini membahas pengelolaan orang-orang di organisasi **Claude Enterprise** (claude.ai) Anda secara terprogram, menggunakan [Admin API](/docs/id/api/admin): mendaftar anggota dan mencarinya berdasarkan alamat email, mengubah peran anggota, menghapus anggota, mengirim dan menarik undangan, mengelola grup perusahaan Anda dan keanggotaannya, serta membaca peran kustom organisasi Anda. Untuk organisasi Claude Console (Claude Platform), lihat [panduan Admin API untuk Claude Console](/docs/id/manage-claude/admin-api).

<Note>
  **Endpoint di halaman ini berada dalam tahap beta untuk organisasi Claude Enterprise.** Beta diaktifkan untuk semua organisasi Claude Enterprise. Permintaan grup dan peran kustom harus menyertakan [header beta](/docs/id/api/beta-headers) `anthropic-beta: ce-user-management-2026-07-13`; permintaan tanpa header tersebut mengembalikan 404. Permintaan anggota dan undangan tidak memerlukan header beta.
</Note>

## Endpoint mana yang dapat digunakan organisasi Anda?

Admin API adalah satu set endpoint di bawah `https://api.anthropic.com/v1/organizations/`. Organisasi Claude Console dan Claude Enterprise melakukan autentikasi dengan [kunci yang berbeda](/docs/id/manage-claude/admin-api-keys) dan masing-masing memiliki akses ke subset endpoint yang berbeda:

| Endpoint                                                                                                                                                                                                                                                                                                 | Claude Console (Claude Platform)                              | Claude Enterprise (claude.ai)      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------- |
| [Anggota](#anggota) dan [undangan](#undangan)                                                                                                                                                                                                                                                            | Tersedia; lihat [Admin API](/docs/id/manage-claude/admin-api) | **Beta** (halaman ini)             |
| [Grup](#grup)                                                                                                                                                                                                                                                                                            | Tidak tersedia                                                | **Beta** (halaman ini)             |
| [Peran kustom](#peran-kustom)                                                                                                                                                                                                                                                                            | Tidak tersedia                                                | **Beta**, hanya-baca (halaman ini) |
| [Batas pengeluaran](/docs/id/manage-claude/spend-limits-api)                                                                                                                                                                                                                                             | Tidak tersedia                                                | Tersedia                           |
| [Workspaces](/docs/id/manage-claude/workspaces), [kunci API](/docs/id/manage-claude/admin-api#api-keys), [laporan penggunaan dan biaya](/docs/id/manage-claude/usage-cost-api), [batas laju](/docs/id/manage-claude/rate-limits-api), dan endpoint [Admin API](/docs/id/manage-claude/admin-api) lainnya | Tersedia                                                      | Tidak tersedia                     |

Anggota dan undangan menggunakan endpoint yang sama untuk kedua jenis organisasi; halaman ini mendokumentasikan perilakunya untuk Claude Enterprise, termasuk [peran organisasi](#peran-organisasi) Claude Enterprise. Endpoint grup dan peran kustom hanya ada untuk Claude Enterprise.

<Check>
  **Diperlukan kunci Admin API dengan cakupan**

  Endpoint ini memerlukan kunci Admin API dengan cakupan `read:members` (endpoint `GET` anggota dan undangan, serta semua endpoint peran kustom; tidak ada cakupan peran terpisah), cakupan `write:members` (endpoint `POST` dan `DELETE` anggota dan undangan), cakupan `read:rbac_groups` (endpoint `GET` grup), atau cakupan `write:rbac_groups` (endpoint `POST` dan `DELETE` grup). Kunci yang membawa cakupan `read:org_audit` (cakupan hanya-baca untuk integrasi audit keamanan) juga dapat memanggil setiap endpoint `GET` di halaman ini dan endpoint baca [Compliance API](/docs/id/manage-claude/compliance-api). Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana pemilik utama Anda membuatnya dan cakupan mana yang harus dipilih. Sertakan kunci di header `x-api-key` pada setiap permintaan. Permintaan anggota dan undangan juga memerlukan header `anthropic-version: 2023-06-01`, seperti yang ditunjukkan dalam contoh; permintaan grup dan peran kustom tidak memerlukannya, dan sebagai gantinya memerlukan header `anthropic-beta` yang dijelaskan dalam catatan sebelumnya.
</Check>

## Ikhtisar

Halaman ini membahas lima sumber daya:

| Sumber daya      | Endpoint                                                                                                                                                                                                                  | Digunakan untuk                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Anggota**      | `GET /v1/organizations/users` `GET /v1/organizations/users/{user_id}` `POST /v1/organizations/users/{user_id}` `DELETE /v1/organizations/users/{user_id}`                                                                 | Mendaftar anggota organisasi atau mencari satu anggota berdasarkan email; mengubah peran anggota; menghapus anggota.             |
| **Undangan**     | `POST /v1/organizations/invites` `GET /v1/organizations/invites` `GET /v1/organizations/invites/{invite_id}` `DELETE /v1/organizations/invites/{invite_id}`                                                               | Mengundang seseorang ke organisasi, melacak status undangan, dan menariknya sebelum diterima.                                    |
| **Grup**         | `GET /v1/organizations/rbac_groups` `GET /v1/organizations/rbac_groups/{group_id}` `POST /v1/organizations/rbac_groups` `POST /v1/organizations/rbac_groups/{group_id}` `DELETE /v1/organizations/rbac_groups/{group_id}` | Membaca grup perusahaan Anda dan peran kustom yang melekat pada masing-masing grup; membuat, mengganti nama, dan menghapus grup. |
| **Anggota grup** | `GET /v1/organizations/rbac_groups/{group_id}/members` `POST /v1/organizations/rbac_groups/{group_id}/members` `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`                                        | Membaca anggota grup; menambah dan menghapus anggota.                                                                            |
| **Peran kustom** | `GET /v1/organizations/rbac_roles` `GET /v1/organizations/rbac_roles/{role_id}` `GET /v1/organizations/rbac_roles/{role_id}/permissions`                                                                                  | Membaca peran kustom organisasi Anda dan izin yang diberikan oleh setiap peran.                                                  |

Peran kustom dan keterkaitannya dengan grup dikelola di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings); API dapat membacanya tetapi tidak dapat mengubahnya.

## Mulai cepat

Daftar anggota organisasi, yang terbaru terlebih dahulu:

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

| Peran              | Arti                                                                               |
| ------------------ | ---------------------------------------------------------------------------------- |
| `user`             | Anggota standar.                                                                   |
| `managed`          | Anggota yang izinnya diberikan melalui peran kustom yang melekat pada grup mereka. |
| `owner`            | Pemilik organisasi.                                                                |
| `membership_admin` | Anggota yang dapat mengelola anggota organisasi.                                   |
| `primary_owner`    | Pemilik utama organisasi. Hanya ada tepat satu.                                    |

API hanya dapat menetapkan peran `user` dan `managed`, pada pembuatan undangan dan pada pembaruan peran. Peran administratif (`owner`, `membership_admin`, dan `primary_owner`) ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat dimodifikasi atau dihapus melalui API ini.

### Anggota dan undangan

Seseorang menjadi anggota dengan menerima undangan (atau melalui single sign-on organisasi Anda, jika dikonfigurasi). Membuat undangan akan mengirimkan email undangan; undangan kemudian terbaca sebagai `pending` hingga penerima menerimanya (`accepted`) atau `expires_at` yang ditetapkan server terlewati (`expired`). Hanya undangan `pending` yang dapat ditarik. Untuk mengubah alamat email atau peran undangan yang tertunda, tarik undangan tersebut dan buat yang baru.

Jika paket organisasi Anda mengambil anggota dari kumpulan kursi yang dibeli dalam jumlah terbatas, undangan yang tertunda akan menggunakan satu kursi. Endpoint pembuatan undangan tidak menerima parameter kursi atau tingkatan: kursi ditetapkan secara otomatis dari tingkatan terendah yang memiliki ketersediaan. Membuat undangan ketika tidak ada kursi yang tersedia akan gagal dengan error 400, bukan membeli kursi. Menarik undangan, membiarkannya kedaluwarsa, atau menghapus anggota nantinya akan mengembalikan kursi ke kumpulan.

### Grup dan peran

Grup menghubungkan anggota ke peran kustom (role-based access control, yaitu `rbac` dalam jalur endpoint dan nama cakupan). Grup dimiliki oleh perusahaan Anda secara keseluruhan (organisasi induk bersama dengan setiap organisasi di bawahnya), bukan oleh satu organisasi, sehingga cakupan grup (`read:rbac_groups` dan `write:rbac_groups`) memerlukan kunci yang dibuat untuk semua organisasi yang tertaut. Setiap grup memiliki `source_type`: `direct` untuk grup yang dibuat di claude.ai, `scim` untuk grup yang disediakan oleh penyedia identitas Anda. Bidang `roles` grup mencantumkan ID peran kustom yang melekat padanya; selesaikan menjadi nama dan izin dengan [endpoint peran kustom](#peran-kustom), dengan catatan bahwa katalog peran bersifat per-organisasi sementara grup bersifat seluruh perusahaan, sehingga mengambil peran yang dimiliki organisasi lain dari perusahaan Anda mengembalikan 404 untuk kunci Anda. Bidang ini bernilai `null` (bukan `[]`) ketika data peran sementara tidak tersedia, jadi coba lagi untuk membedakan pembacaan yang terdegradasi dari grup tanpa peran.

## Batas laju

Endpoint Admin API berbagi batas per-organisasi sebesar **100 permintaan per menit**; pembuatan undangan memiliki batasnya sendiri sebesar **1.200 permintaan per jam**. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi

Daftar anggota dan undangan menggunakan paginasi berbasis ID: berikan `limit` (default 20, maksimum 1000) ditambah paling banyak satu dari `before_id` atau `after_id`, dan lakukan paginasi menggunakan bidang `first_id` dan `last_id` dari setiap respons hingga `has_more` bernilai `false`. Daftar grup dan peran kustom menggunakan **kursor buram (opaque cursor)**: nilai `next_page` dari respons diteruskan tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, hingga `next_page` bernilai `null`.

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Errors](/docs/id/api/errors).

## Anggota

### Mendaftar anggota

`GET /v1/organizations/users` mengembalikan anggota organisasi, yang paling baru ditambahkan terlebih dahulu. Filter berdasarkan `email` untuk mencari anggota tertentu; pencocokan tidak peka huruf besar-kecil dan menoleransi varian umum dari alamat yang sama (misalnya, `jane+hiring@example.com` cocok dengan `jane@example.com`). Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List users](/docs/id/api/admin/users/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users?email=jane@example.com" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mendapatkan anggota

`GET /v1/organizations/users/{user_id}` mengembalikan satu anggota berdasarkan ID. Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get user](/docs/id/api/admin/users/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mengubah peran anggota

`POST /v1/organizations/users/{user_id}` menetapkan peran anggota menjadi `user` atau `managed`. Anggota yang memegang peran administratif (`owner`, `membership_admin`, atau `primary_owner`) tidak dapat diubah melalui endpoint ini, dan peran administratif tidak dapat ditetapkan; keduanya mengembalikan 400 dan dikelola di pengaturan organisasi claude.ai. Jika penyedia identitas organisasi Anda mengelola peran (SSO lanjutan atau penyediaan SCIM lanjutan), pembaruan peran mengembalikan 400. Memerlukan cakupan `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Update user](/docs/id/api/admin/users/update) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"role": "managed"}'
```

### Menghapus anggota

`DELETE /v1/organizations/users/{user_id}` menghapus anggota dari organisasi, mengembalikan kursi yang dibeli yang mereka tempati ke kumpulan organisasi. Anggota yang memegang peran administratif tidak dapat dihapus melalui endpoint ini, dan jika penyedia identitas Anda mengelola keanggotaan (SCIM), penghapusan mengembalikan 400. Memerlukan cakupan `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Remove user](/docs/id/api/admin/users/delete) di referensi API.

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

`POST /v1/organizations/invites` mengirimkan email undangan dan mengembalikan undangan dengan `expires_at` yang ditetapkan server. `role` harus berupa `user` atau `managed`. Jika undangan yang tertunda sudah ada untuk alamat email tersebut, atau alamat tersebut sudah dimiliki oleh seorang anggota, permintaan mengembalikan 400 dengan menyebutkan sumber daya yang sudah ada. Organisasi yang penyedia identitasnya menyediakan pengguna secara otomatis (JIT atau SCIM) tidak dapat membuat undangan melalui API. Memerlukan cakupan `write:members`.

Pada paket yang mengambil anggota dari kumpulan kursi terbatas, undangan secara otomatis mengambil kursi dari tingkatan terendah yang memiliki ketersediaan; API tidak menerima parameter tingkatan. Jika tidak ada kursi yang tersedia, permintaan gagal dengan error 400, bukan membeli kursi. Tambahkan kursi melalui manajemen paket organisasi dan coba lagi.

Bidang opsional `rbac_group_ids` mencantumkan grup (berdasarkan ID berawalan `rbac_group_`) yang akan ditetapkan kepada anggota saat mereka menerima undangan. Memberikan `rbac_group_ids` yang tidak kosong juga mengharuskan kunci membawa cakupan `write:rbac_groups`, karena penetapan grup dapat memberikan izin yang melekat pada peran grup tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [Create invite](/docs/id/api/admin/invites/create) di referensi API.

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

`GET /v1/organizations/invites` mengembalikan undangan organisasi, yang terbaru terlebih dahulu, di seluruh status `pending`, `accepted`, dan `expired`; tidak ada filter status. Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List invites](/docs/id/api/admin/invites/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Mendapatkan undangan

`GET /v1/organizations/invites/{invite_id}` mengembalikan satu undangan berdasarkan ID. Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get invite](/docs/id/api/admin/invites/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Menarik undangan

`DELETE /v1/organizations/invites/{invite_id}` menarik undangan `pending`, menonaktifkan tautan di email undangan. Menarik undangan `accepted` mengembalikan 400 (hapus anggota sebagai gantinya); menarik undangan `expired` mengembalikan 400. Memerlukan cakupan `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete invite](/docs/id/api/admin/invites/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## Grup

Grup yang dibuat perusahaan Anda secara langsung, di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau melalui API ini (`source_type: "direct"`), mendukung setiap endpoint di bagian ini. Grup yang disediakan oleh penyedia identitas Anda (`source_type: "scim"`) dapat dibaca tetapi tidak dapat dimodifikasi: mengganti nama atau menghapus grup SCIM, atau mengubah keanggotaannya, mengembalikan 400, karena penyedia identitas Anda yang memilikinya. Setiap permintaan grup harus menyertakan header `anthropic-beta: ce-user-management-2026-07-13`, seperti yang ditunjukkan dalam contoh; permintaan tanpa header tersebut mengembalikan 404. Tidak seperti permintaan anggota dan undangan, permintaan grup tidak memerlukan header `anthropic-version`.

### Mendaftar grup

`GET /v1/organizations/rbac_groups` mengembalikan grup perusahaan Anda, termasuk grup yang dikelola penyedia identitas (`scim`). Memerlukan cakupan `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [List groups](/docs/id/api/admin/rbac_groups/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
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

`GET /v1/organizations/rbac_groups/{group_id}` mengembalikan satu grup berdasarkan ID. Memerlukan cakupan `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Get group](/docs/id/api/admin/rbac_groups/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
```

### Membuat grup

`POST /v1/organizations/rbac_groups` membuat grup dengan `name` yang diberikan (1–255 karakter) dan tanpa peran atau anggota. Memerlukan cakupan `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Create group](/docs/id/api/admin/rbac_groups/create) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13" \
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

`POST /v1/organizations/rbac_groups/{group_id}` memperbarui grup. `name` adalah satu-satunya bidang yang dapat diubah oleh endpoint ini. Memerlukan cakupan `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Update group](/docs/id/api/admin/rbac_groups/update) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13" \
  -d '{"name": "Platform Engineering"}'
```

### Menghapus grup

`DELETE /v1/organizations/rbac_groups/{group_id}` menghapus grup. Anggotanya tetap menjadi anggota organisasi mereka, tetapi mereka kehilangan izin dari peran yang melekat padanya, dan [batas pengeluaran](/docs/id/manage-claude/spend-limits-api) grup, jika ada, berhenti berlaku bagi mereka. Memerlukan cakupan `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete group](/docs/id/api/admin/rbac_groups/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
```

```json
{
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "type": "rbac_group_deleted"
}
```

### Mendaftar anggota grup

`GET /v1/organizations/rbac_groups/{group_id}/members` mengembalikan anggota grup (masing-masing dengan `user_id` dan email mereka), yang paling lama terlebih dahulu. Hanya anggota saat ini dari organisasi perusahaan Anda yang dikembalikan, sehingga sebuah halaman mungkin berisi lebih sedikit dari `limit` entri sementara `has_more` bernilai `true`. Memerlukan cakupan `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [List group members](/docs/id/api/admin/rbac_groups/members/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members?limit=100" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
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

`POST /v1/organizations/rbac_groups/{group_id}/members` menambahkan anggota organisasi ke grup berdasarkan `user_id`. Pengguna harus sudah menjadi anggota dari salah satu organisasi perusahaan Anda (jika tidak, permintaan mengembalikan 404), dan menambahkan seseorang yang sudah ada di grup mengembalikan 400. Untuk grup `scim`, keanggotaan dikelola di penyedia identitas Anda dan permintaan ini mengembalikan 400. Untuk menetapkan grup kepada seseorang yang belum bergabung, gunakan `rbac_group_ids` pada [pembuatan undangan](#membuat-undangan) sebagai gantinya. Memerlukan cakupan `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Add group member](/docs/id/api/admin/rbac_groups/members/create) di referensi API.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13" \
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

`DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}` menghapus anggota dari grup; mereka tetap menjadi anggota organisasi mereka. Permintaan mengembalikan 404 jika pengguna bukan anggota grup, dan 400 untuk grup `scim`, yang keanggotaannya dikelola di penyedia identitas Anda. Memerlukan cakupan `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Remove group member](/docs/id/api/admin/rbac_groups/members/delete) di referensi API.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
```

```json
{
  "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "type": "rbac_group_member_deleted"
}
```

## Peran kustom

Peran kustom bersifat hanya-baca melalui API: endpoint ini mengkatalogkan peran kustom organisasi Anda (yang didefinisikan di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau disediakan oleh Anthropic) dan izin yang diberikan oleh setiap peran. Pembacaan peran kustom menggunakan cakupan `read:members` (tidak ada cakupan peran terpisah) dan bekerja dengan kunci tingkat organisasi: tidak seperti endpoint grup, endpoint ini tidak memerlukan kunci yang dibuat untuk semua organisasi yang tertaut, dan katalog yang dikembalikan adalah milik organisasi Anda sendiri. Permintaan peran kustom, seperti permintaan grup, harus menyertakan header `anthropic-beta: ce-user-management-2026-07-13`; permintaan tanpa header tersebut mengembalikan 404.

### Mendaftar peran

`GET /v1/organizations/rbac_roles` mengembalikan peran kustom organisasi Anda. Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [List roles](/docs/id/api/admin/rbac_roles/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
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

`GET /v1/organizations/rbac_roles/{role_id}` mengembalikan satu peran berdasarkan ID. Memerlukan cakupan `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Get role](/docs/id/api/admin/rbac_roles/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
```

### Mendaftar izin peran

`GET /v1/organizations/rbac_roles/{role_id}/permissions` mengembalikan izin peran. Setiap izin memasangkan `resource` (apa yang menjadi cakupannya: fitur produk organisasi, alat konektor, cakupan OAuth konektor, satu konektor, atau setiap konektor) dengan `action` (apa yang diberikannya pada sumber daya tersebut). Baris untuk fitur yang tidak diaktifkan untuk organisasi Anda dihilangkan, sehingga sebuah halaman mungkin berisi lebih sedikit dari `limit` baris sementara `has_more` bernilai `true`. Memerlukan cakupan `read:members`.

Dua nilai `action` memerlukan perhatian khusus: izin `organization` yang tindakannya adalah `capability_access_all` (setiap fitur produk) atau `capability_access_all_ga` (setiap fitur produk yang tersedia secara umum) adalah pemberian menyeluruh (yang tidak mencakup akses model maupun izin panel admin berawalan `permission_`) dan dicantumkan sebagai satu baris tunggal tersebut, bukan diperluas. Saat Anda menghitung apa yang diberikan oleh suatu peran, perlakukan baris menyeluruh sebagai mencakup semua yang dijelaskan oleh variannya, bukan hanya fitur yang disebutkan di baris lain.

Untuk detail parameter lengkap dan skema respons, lihat [List role permissions](/docs/id/api/admin/rbac_roles/permissions/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv/permissions?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-beta: ce-user-management-2026-07-13"
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

2. Hapus mereka dengan `DELETE /v1/organizations/users/{user_id}`, menggunakan `id` dari respons. Kursi mereka, jika ada, kembali ke kumpulan.

3. Jika orang tersebut belum bergabung, pencarian tidak mengembalikan anggota; daftar undangan dan tarik undangan `pending` mereka sebagai gantinya.

### Mengaudit keanggotaan grup

1. Daftar grup dan catat `id`, `name`, dan `roles` setiap grup.

2. Untuk setiap grup yang membawa peran sensitif, telusuri halaman `GET /v1/organizations/rbac_groups/{group_id}/members` dan bandingkan email anggota dengan daftar penyedia identitas Anda.

3. Hapus anggota yang seharusnya tidak lagi berada di grup dengan `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`. Untuk grup `scim`, lakukan perubahan di penyedia identitas Anda sebagai gantinya.

## Pertanyaan yang sering diajukan

### Apakah ini API yang berbeda dari Admin API?

Tidak. Endpoint anggota dan undangan adalah endpoint `/v1/organizations/` yang sama yang digunakan oleh organisasi Claude Console; halaman ini mendokumentasikan perilakunya untuk Claude Enterprise. Endpoint grup dan peran kustom adalah bagian dari API yang sama dan hanya ada untuk organisasi Claude Enterprise. [Tabel ketersediaan](#endpoint-mana-yang-dapat-digunakan-organisasi-anda) menunjukkan endpoint mana yang dapat dipanggil oleh setiap jenis organisasi.

### Dapatkah saya menetapkan peran owner atau membership admin melalui API?

Tidak. API hanya menetapkan `user` dan `managed`, pada pembuatan undangan dan pembaruan peran. Peran administratif ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat dimodifikasi atau dihapus melalui API.

### Dapatkah saya membuat atau memodifikasi grup melalui API?

Ya, dengan cakupan `write:rbac_groups`: membuat, mengganti nama, dan menghapus grup, serta menambah atau menghapus anggotanya. Dua hal yang tidak dapat diubah oleh API: grup yang disediakan oleh penyedia identitas Anda (`source_type: "scim"`), yang nama dan keanggotaannya dimiliki oleh penyedia identitas, dan peran kustom, yang dikelola di pengaturan organisasi claude.ai (API [membacanya](#peran-kustom)).

### Apakah undangan yang belum diterima menggunakan kursi?

Pada paket dengan kumpulan kursi terbatas, ya: undangan `pending` menahan satu kursi. Menarik undangan atau membiarkannya kedaluwarsa akan membebaskan kursi tersebut. Pada paket tanpa kumpulan kursi, undangan tidak menggunakan apa pun.

### Organisasi saya menggunakan single sign-on. Operasi mana yang berfungsi?

Jika penyedia identitas Anda menyediakan pengguna secara otomatis (JIT atau SCIM), pembuatan undangan mengembalikan 400. Jika penyedia identitas mengelola peran (SSO lanjutan atau penyediaan SCIM lanjutan), pembaruan peran mengembalikan 400. Jika penyedia identitas mengelola keanggotaan (penyediaan SCIM), penghapusan anggota mengembalikan 400. Pembacaan berfungsi dalam semua kasus.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Membuat kunci Admin API" href="/docs/id/manage-claude/admin-api-keys">
    Di mana pemilik utama Anda membuat kunci dengan cakupan dan cakupan mana yang harus dipilih.
  </Card>

  <Card title="Compliance API" href="/docs/id/manage-claude/compliance-org-data">
    Baca organisasi, pengguna, peran, grup, dan pengaturan untuk audit dan eDiscovery.
  </Card>

  <Card title="API Analitik" href="/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan dan biaya per-pengguna dan berdasarkan rentang waktu untuk Claude Enterprise.
  </Card>

  <Card title="API Batas Pengeluaran" href="/docs/id/manage-claude/spend-limits-api">
    Tetapkan batas pengeluaran per-anggota dan tinjau permintaan kenaikan.
  </Card>
</CardGroup>
