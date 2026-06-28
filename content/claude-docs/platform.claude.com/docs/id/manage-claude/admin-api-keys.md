---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api-keys
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 340a70d351a57c0afa70d9d8f890b169e6d999a821a8abbc5861d1e4bb724be4
---

# Membuat kunci Admin API

Buat kunci Admin API untuk organisasi Claude Console atau Claude Enterprise Anda.

---

Setiap API di bagian **Admin** dari panduan ini ([Admin API](/docs/id/manage-claude/admin-api), [Analytics API](/docs/id/manage-claude/analytics-api), [Compliance API](/docs/id/manage-claude/compliance-api), [Spend Limits API](/docs/id/manage-claude/spend-limits-api), [Usage and Cost API](/docs/id/manage-claude/usage-cost-api), dan [Rate Limits API](/docs/id/manage-claude/rate-limits-api)) diautentikasi dengan kunci Admin API. Anda tidak memerlukan kunci terpisah untuk setiap API.

Tempat Anda membuat kunci bergantung pada produk Claude yang digunakan organisasi Anda.

## Kunci mana yang Anda butuhkan?

| Organisasi Anda                                             | Buat kunci di                                                                             | Prefiks kunci        | Siapa yang dapat membuatnya                  | Berfungsi dengan                                                                                                                                                                                                                                                                                                                               |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Console** (Claude Platform, `platform.claude.com`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | `sk-ant-admin01-...` | Anggota organisasi dengan peran **admin**    | [Admin API](/docs/id/manage-claude/admin-api), [Usage and Cost API](/docs/id/manage-claude/usage-cost-api), [Rate Limits API](/docs/id/manage-claude/rate-limits-api), [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api), dan [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dari Compliance API |
| **Claude Enterprise** (`claude.ai`)                         | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | `sk-ant-api01-...`   | **Primary owner** (pemilik utama) organisasi | [Compliance API](/docs/id/manage-claude/compliance-api), [Claude Enterprise Analytics API](/docs/id/manage-claude/analytics-api), dan [Spend Limits API](/docs/id/manage-claude/spend-limits-api), sesuai dengan [scope](#choose-scopes-for-a-claude-enterprise-key) yang Anda pilih                                                           |

Kunci yang dibuat di satu organisasi tidak dapat digunakan untuk mengelola organisasi yang berbeda. Jika perusahaan Anda menggunakan Claude Console dan Claude Enterprise, buat satu kunci di masing-masing.

## Membuat kunci untuk organisasi Claude Console

<Steps>
  <Step title="Masuk sebagai admin organisasi">
    Hanya anggota organisasi dengan peran **admin** yang dapat membuat kunci Admin API. Lihat [Peran dan izin organisasi](/docs/id/manage-claude/admin-api#organization-roles-and-permissions).
  </Step>

  <Step title="Buka pengaturan Admin keys">
    Buka [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama, lalu klik **Create**. Kunci Claude Console tidak memiliki scope yang dapat dipilih; setiap kunci memiliki akses Admin API penuh.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-admin01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Membuat kunci untuk organisasi Claude Enterprise

<Steps>
  <Step title="Masuk sebagai primary owner">
    Hanya **primary owner** (pemilik utama) dari organisasi induk Claude Enterprise yang dapat membuat kunci ini.
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Klik + Create key">
    Beri nama kunci dan pilih scope yang Anda butuhkan dari [tabel scope](#choose-scopes-for-a-claude-enterprise-key). Anda dapat menggabungkan scope dari API yang berbeda (misalnya, `read:analytics` dan `read:spend_limits`) pada satu kunci.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>
</Steps>

## Memilih scope untuk kunci Claude Enterprise

Saat Anda membuat kunci Claude Enterprise, pilih setiap scope yang diperlukan oleh API yang akan Anda panggil. Scope bersifat tetap saat pembuatan; untuk menambahkan scope di kemudian hari, buat kunci baru.

| Untuk memanggil...                                                                                                                                                  | Pilih scope ini                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Spend Limits API](/docs/id/manage-claude/spend-limits-api): membaca batas pengeluaran efektif anggota dan permintaan peningkatan                                   | `read:spend_limits`                                        |
| [Spend Limits API](/docs/id/manage-claude/spend-limits-api): mengatur atau menghapus batas pengeluaran per pengguna; menyetujui atau menolak permintaan peningkatan | `write:spend_limits`                                       |
| [Claude Enterprise Analytics API](/docs/id/manage-claude/analytics-api): laporan keterlibatan, adopsi, biaya, dan penggunaan                                        | `read:analytics`                                           |
| [Compliance API Activity Feed](/docs/id/manage-claude/compliance-activity-feed): peristiwa aktivitas di seluruh organisasi                                          | `read:compliance_activities`                               |
| [Endpoint konten Compliance API](/docs/id/manage-claude/compliance-content-data): membaca obrolan, file, proyek, dan pengguna                                       | `read:compliance_user_data`                                |
| [Endpoint konten Compliance API](/docs/id/manage-claude/compliance-content-data): menghapus obrolan, file, dan proyek                                               | `delete:compliance_user_data`                              |
| [Endpoint organisasi Compliance API](/docs/id/manage-claude/compliance-org-data): membaca metadata dan pengaturan organisasi                                        | `read:compliance_org_data`, `read:compliance_org_settings` |

Compliance API dan Analytics API harus diaktifkan untuk organisasi Anda sebelum kunci dengan scope tersebut dapat digunakan. Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access#request-compliance-api-access) dan [Analytics API](/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

## Menggunakan kunci

Sertakan kunci di header `x-api-key` pada setiap permintaan. Lihat dokumentasi masing-masing API untuk contoh permintaan lengkap.

Panggilan yang melebihi scope kunci akan mengembalikan `403 Forbidden` dengan pesan yang mencantumkan scope yang dimiliki kunci dan scope yang dibutuhkan endpoint.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Admin API" href="/docs/id/manage-claude/admin-api">
    Kelola anggota organisasi, workspace, dan kunci API.
  </Card>

  <Card title="Spend Limits API" href="/docs/id/manage-claude/spend-limits-api">
    Atur batas pengeluaran per anggota dan tinjau permintaan peningkatan untuk organisasi Claude Enterprise Anda.
  </Card>

  <Card title="Analytics API" href="/docs/id/manage-claude/analytics-api">
    Buat laporan tentang produktivitas Claude Code atau keterlibatan dan adopsi Claude Enterprise.
  </Card>

  <Card title="Compliance API" href="/docs/id/manage-claude/compliance-api">
    Audit aktivitas dan ambil atau hapus konten pengguna di seluruh organisasi Anda.
  </Card>
</CardGroup>
