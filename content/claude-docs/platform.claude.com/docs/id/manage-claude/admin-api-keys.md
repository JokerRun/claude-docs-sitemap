---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api-keys
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 05073d46bdee094346d169b518a2b4583b33f9e5b5b4516888c1122997767eb7
---

# Membuat kunci API Admin

Buat kunci API Admin untuk organisasi Claude Console atau Claude Enterprise Anda.

---

Kunci API Admin mengautentikasi setiap API di bagian **Admin** dari panduan ini: [Admin API](/docs/id/manage-claude/admin-api), [Analytics API](/docs/id/manage-claude/analytics-api), [Compliance API](/docs/id/manage-claude/compliance-api), [Spend Limits API](/docs/id/manage-claude/spend-limits-api), [Usage and Cost API](/docs/id/manage-claude/usage-cost-api), dan [Rate Limits API](/docs/id/manage-claude/rate-limits-api). Anda tidak memerlukan kunci terpisah untuk setiap API. Satu-satunya pengecualian adalah endpoint service-account, federation-issuer, dan federation-rule pada Admin API, yang hanya menerima token bearer OAuth dengan cakupan `org:admin`. Lihat [Mendapatkan token bearer OAuth](/docs/id/manage-claude/admin-api#oauth-bearer-token).

Tempat Anda membuat kunci bergantung pada produk Claude mana yang digunakan organisasi Anda.

## Kunci mana yang Anda butuhkan?

| Organisasi Anda                                             | Buat kunci di                                                                             | Awalan kunci         | Siapa yang dapat membuatnya                                                                                                                                                                                | Berfungsi dengan                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Console** (Claude Platform, `platform.claude.com`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | `sk-ant-admin01-...` | Anggota organisasi dengan peran **admin**                                                                                                                                                                  | [Admin API](/docs/id/manage-claude/admin-api), [Usage and Cost API](/docs/id/manage-claude/usage-cost-api), [Rate Limits API](/docs/id/manage-claude/rate-limits-api), [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api), dan [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) pada Compliance API                                                                             |
| **Claude Enterprise** (`claude.ai`)                         | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | `sk-ant-api01-...`   | **Primary owner** dari organisasi induk (semua organisasi yang tertaut). Seorang **organization owner** dapat membuat kunci yang hanya membawa cakupan Compliance API, terbatas pada organisasinya sendiri | [Manajemen pengguna](/docs/id/manage-claude/user-management) (endpoint member, invite, dan group pada Admin API, dalam versi beta), [Compliance API](/docs/id/manage-claude/compliance-api), [Claude Enterprise Analytics API](/docs/id/manage-claude/analytics-api), dan [Spend Limits API](/docs/id/manage-claude/spend-limits-api), sesuai dengan [cakupan](#choose-scopes-for-a-claude-enterprise-key) yang Anda pilih |

Kunci yang dibuat di satu organisasi tidak dapat digunakan untuk mengelola organisasi yang berbeda. Jika perusahaan Anda menggunakan Claude Console dan Claude Enterprise, buat satu kunci di masing-masing.

## Membuat kunci untuk organisasi Claude Console

<Steps>
  <Step title="Masuk sebagai admin organisasi">
    Hanya anggota organisasi dengan peran **admin** yang dapat membuat kunci API Admin. Lihat [Peran dan izin organisasi](/docs/id/manage-claude/admin-api#organization-roles-and-permissions).
  </Step>

  <Step title="Buka pengaturan Admin keys">
    Buka [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama, pilih [masa berlaku kunci](/docs/id/manage-claude/authentication#key-expiration), lalu klik **Create**. Kunci Claude Console tidak memiliki cakupan yang dapat dipilih; setiap kunci membawa akses penuh ke semua endpoint yang menerima kunci API Admin (endpoint service-account dan federation yang disebutkan di bagian atas halaman ini tidak menerima kunci API Admin).
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-admin01-`) dan simpan di pengelola secret Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Membuat kunci untuk organisasi Claude Enterprise

<Steps>
  <Step title="Masuk sebagai primary owner atau organization owner">
    **Primary owner** dari organisasi induk Claude Enterprise dapat membuat kunci yang dapat mengakses setiap organisasi yang tertaut, atau kunci yang terbatas pada satu organisasi. Seorang **organization owner** dapat membuat kunci dengan cakupan Compliance API saja, terbatas pada organisasinya sendiri.
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Klik + Create key">
    Beri nama kunci dan pilih cakupan yang Anda butuhkan dari [tabel cakupan](#choose-scopes-for-a-claude-enterprise-key). Primary owner dapat menggabungkan cakupan dari API yang berbeda (misalnya, `read:analytics` dan `read:spend_limits`) pada satu kunci.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di pengelola secret Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Memilih cakupan untuk kunci Claude Enterprise

Saat Anda membuat kunci Claude Enterprise, pilih setiap cakupan yang dibutuhkan oleh API yang akan Anda panggil. Cakupan bersifat tetap saat pembuatan; untuk menambahkan cakupan di kemudian hari, buat kunci baru.

| Untuk memanggil...                                                                                                                                                                                                                            | Pilih cakupan ini             |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| [Manajemen pengguna](/docs/id/manage-claude/user-management) Admin API: menampilkan daftar dan mencari anggota serta undangan; membaca peran kustom dan izinnya                                                                               | `read:members`                |
| [Manajemen pengguna](/docs/id/manage-claude/user-management) Admin API: mengubah peran anggota, menghapus anggota, membuat dan menarik undangan                                                                                               | `write:members`               |
| [Manajemen pengguna](/docs/id/manage-claude/user-management) Admin API: membaca grup dan anggotanya                                                                                                                                           | `read:rbac_groups`            |
| [Manajemen pengguna](/docs/id/manage-claude/user-management) Admin API: membuat, mengganti nama, dan menghapus grup; menambah dan menghapus anggota grup; menetapkan grup saat pembuatan undangan                                             | `write:rbac_groups`           |
| [Spend Limits API](/docs/id/manage-claude/spend-limits-api): membaca batas pengeluaran efektif anggota dan permintaan kenaikan                                                                                                                | `read:spend_limits`           |
| [Spend Limits API](/docs/id/manage-claude/spend-limits-api): menetapkan atau menghapus batas pengeluaran per pengguna; menyetujui atau menolak permintaan kenaikan                                                                            | `write:spend_limits`          |
| [Claude Enterprise Analytics API](/docs/id/manage-claude/analytics-api): laporan keterlibatan, adopsi, biaya, dan penggunaan                                                                                                                  | `read:analytics`              |
| [Activity Feed Compliance API](/docs/id/manage-claude/compliance-activity-feed): peristiwa aktivitas di seluruh organisasi                                                                                                                    | `read:compliance_activities`  |
| [Endpoint konten Compliance API](/docs/id/manage-claude/compliance-content-data): membaca chat, file, proyek, dan pengguna                                                                                                                    | `read:compliance_user_data`   |
| [Endpoint konten Compliance API](/docs/id/manage-claude/compliance-content-data): menghapus chat, file, dan proyek                                                                                                                            | `delete:compliance_user_data` |
| [Endpoint organisasi Compliance API](/docs/id/manage-claude/compliance-org-data): membaca metadata organisasi dan pengaturan efektif                                                                                                          | `read:compliance_org_data`    |
| Endpoint baca [manajemen pengguna](/docs/id/manage-claude/user-management) Admin API dan setiap endpoint baca Compliance API, dengan satu cakupan hanya-baca (untuk integrasi audit keamanan; tidak termasuk Spend Limits atau Analytics API) | `read:org_audit`              |

Compliance API dan Analytics API harus diaktifkan untuk organisasi Anda sebelum kunci dengan cakupan tersebut dapat digunakan. Lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dan [Mendapatkan akses ke Claude Enterprise Analytics API](/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

## Menggunakan kunci

Sertakan kunci di header `x-api-key` pada setiap permintaan. Lihat dokumentasi masing-masing API untuk contoh permintaan lengkap.

Panggilan yang melebihi cakupan kunci akan mengembalikan `403 Forbidden` dengan pesan yang mencantumkan cakupan yang dimiliki kunci dan cakupan yang dibutuhkan endpoint.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Admin API" href="/docs/id/manage-claude/admin-api">
    Kelola anggota organisasi, workspace, dan kunci API.
  </Card>

  <Card title="Spend Limits API" href="/docs/id/manage-claude/spend-limits-api">
    Tetapkan batas pengeluaran per anggota dan tinjau permintaan kenaikan untuk organisasi Claude Enterprise Anda.
  </Card>

  <Card title="Analytics API" href="/docs/id/manage-claude/analytics-api">
    Buat laporan tentang produktivitas Claude Code atau keterlibatan dan adopsi Claude Enterprise.
  </Card>

  <Card title="Compliance API" href="/docs/id/manage-claude/compliance-api">
    Audit aktivitas serta ambil atau hapus konten pengguna di seluruh organisasi Anda.
  </Card>
</CardGroup>
