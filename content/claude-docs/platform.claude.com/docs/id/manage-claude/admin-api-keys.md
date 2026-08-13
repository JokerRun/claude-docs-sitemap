---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api-keys
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 43cdd2e20b344415ab6150a3af0347d5099fafad3a7df0ef0a0e8664a6eef113
---

---
title: Membuat kunci Admin API
url: https://platform.claude.com/docs/id/manage-claude/admin-api-keys
description: Buat kunci Admin API untuk organisasi Claude Console atau Claude Enterprise Anda.
---

Kunci Admin API mengautentikasi setiap API di bagian **Admin** dari panduan ini: [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), [Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api), [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), [Spend Limits API](https://platform.claude.com/docs/id/manage-claude/spend-limits-api), [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api), dan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api). Anda tidak memerlukan kunci terpisah untuk setiap API. Satu-satunya pengecualian adalah endpoint service-account, federation-issuer, dan federation-rule pada Admin API, yang hanya menerima OAuth bearer token dengan scope `org:admin`. Lihat [Mendapatkan OAuth bearer token](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token).

Tempat Anda membuat kunci bergantung pada produk Claude yang digunakan organisasi Anda.

## Kunci mana yang Anda butuhkan?

| Organisasi Anda                                             | Buat kunci di                                                                             | Prefiks kunci        | Siapa yang dapat membuatnya                                                                                                                                                                      | Berfungsi dengan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Console** (Claude Platform, `platform.claude.com`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | `sk-ant-admin01-...` | Anggota organisasi dengan peran **admin**                                                                                                                                                        | [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api), [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api), [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api), dan [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dari Compliance API                                                                                                                |
| **Claude Enterprise** (`claude.ai`)                         | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | `sk-ant-api01-...`   | **Primary owner** dari organisasi induk (semua organisasi yang tertaut). **Organization owner** dapat membuat kunci yang hanya membawa scope Compliance API, terbatas pada organisasinya sendiri | [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) (endpoint member, invite, dan group dari Admin API, dalam versi beta), [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api), dan [Spend Limits API](https://platform.claude.com/docs/id/manage-claude/spend-limits-api), sesuai dengan [scope](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key) yang Anda pilih |

Kunci yang dibuat di satu organisasi tidak dapat digunakan untuk mengelola organisasi lain. Jika perusahaan Anda menggunakan Claude Console dan Claude Enterprise, buat satu kunci di masing-masing.

## Membuat kunci untuk organisasi Claude Console

<Steps>
  <Step title="Masuk sebagai admin organisasi">
    Hanya anggota organisasi dengan peran **admin** yang dapat membuat kunci Admin API. Lihat [Peran dan izin organisasi](https://platform.claude.com/docs/id/manage-claude/admin-api#organization-roles-and-permissions).
  </Step>

  <Step title="Buka pengaturan Admin keys">
    Buka [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama, pilih [masa berlaku kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration), lalu klik **Create**. Kunci Claude Console tidak memiliki scope yang dapat dipilih; setiap kunci membawa akses penuh ke semua endpoint yang menerima kunci Admin API (endpoint service-account dan federation yang disebutkan di bagian atas halaman ini tidak menerima kunci Admin API).
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-admin01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Membuat kunci untuk organisasi Claude Enterprise

<Steps>
  <Step title="Masuk sebagai primary owner atau organization owner">
    **Primary owner** dari organisasi induk Claude Enterprise dapat membuat kunci yang dapat mengakses setiap organisasi yang tertaut, atau kunci yang dibatasi untuk satu organisasi. **Organization owner** dapat membuat kunci dengan scope Compliance API saja, terbatas pada organisasinya sendiri.
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Klik + Create key">
    Beri nama kunci dan pilih scope yang Anda butuhkan dari [tabel scope](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key). Primary owner dapat menggabungkan scope dari API yang berbeda (misalnya, `read:analytics` dan `read:spend_limits`) pada satu kunci.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Memilih scope untuk kunci Claude Enterprise

Saat Anda membuat kunci Claude Enterprise, pilih setiap scope yang diperlukan oleh API yang akan Anda panggil. Scope ditetapkan saat pembuatan; untuk menambahkan scope di kemudian hari, buat kunci baru.

| Untuk memanggil...                                                                                                                                                                                                                                                        | Pilih scope ini               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) Admin API: menampilkan daftar dan mencari anggota serta undangan; membaca peran kustom dan izinnya                                                                                | `read:members`                |
| [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) Admin API: mengubah peran anggota, menghapus anggota, membuat dan membatalkan undangan                                                                                            | `write:members`               |
| [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) Admin API: membaca grup dan anggotanya                                                                                                                                            | `read:rbac_groups`            |
| [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) Admin API: membuat, mengganti nama, dan menghapus grup; menambah dan menghapus anggota grup; menetapkan grup saat pembuatan undangan                                              | `write:rbac_groups`           |
| [Spend Limits API](https://platform.claude.com/docs/id/manage-claude/spend-limits-api): membaca batas pengeluaran efektif anggota dan permintaan kenaikan                                                                                                                 | `read:spend_limits`           |
| [Spend Limits API](https://platform.claude.com/docs/id/manage-claude/spend-limits-api): menetapkan atau menghapus batas pengeluaran per pengguna; menyetujui atau menolak permintaan kenaikan                                                                             | `write:spend_limits`          |
| [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api): laporan keterlibatan, adopsi, biaya, dan penggunaan                                                                                                                   | `read:analytics`              |
| [Activity Feed Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed): peristiwa aktivitas di seluruh organisasi                                                                                                                     | `read:compliance_activities`  |
| [Endpoint konten Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-content-data): membaca obrolan, file, proyek, transkrip sesi Cowork dan Claude Code, serta pengguna                                                                         | `read:compliance_user_data`   |
| [Endpoint konten Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-content-data): menghapus obrolan, file, dan proyek                                                                                                                          | `delete:compliance_user_data` |
| [Endpoint organisasi Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-org-data): membaca metadata organisasi dan pengaturan efektif                                                                                                           | `read:compliance_org_data`    |
| Endpoint baca [manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) Admin API dan setiap endpoint baca Compliance API, dengan satu scope read-only (untuk integrasi audit keamanan; tidak termasuk Spend Limits API atau Analytics API) | `read:org_audit`              |

Compliance API dan Analytics API harus diaktifkan untuk organisasi Anda sebelum kunci dengan scope tersebut dapat digunakan. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dan [Mendapatkan akses ke Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

## Menggunakan kunci

Kirimkan kunci di header `x-api-key` pada setiap permintaan. Lihat dokumentasi masing-masing API untuk contoh permintaan lengkap.

Panggilan yang melebihi scope kunci akan mengembalikan `403 Forbidden` dengan pesan yang mencantumkan scope yang dimiliki kunci dan scope yang dibutuhkan endpoint.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Admin API" href="https://platform.claude.com/docs/id/manage-claude/admin-api">
    Kelola anggota organisasi, workspace, dan kunci API.
  </Card>

  <Card title="Spend Limits API" href="https://platform.claude.com/docs/id/manage-claude/spend-limits-api">
    Tetapkan batas pengeluaran per anggota dan tinjau permintaan kenaikan untuk organisasi Claude Enterprise Anda.
  </Card>

  <Card title="Analytics API" href="https://platform.claude.com/docs/id/manage-claude/analytics-api">
    Buat laporan tentang produktivitas Claude Code atau keterlibatan dan adopsi Claude Enterprise.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-api">
    Audit aktivitas dan ambil atau hapus konten pengguna di seluruh organisasi Anda.
  </Card>
</CardGroup>
