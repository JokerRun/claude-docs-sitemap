---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api-access
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: 2a485a6c6a44bf37f878447a5268dc5752ab724925787e3bae5077c1b967bba8
---

# Mendapatkan akses ke Compliance API

Minta akses Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin bercakupan) atau kunci Admin API, dan pelajari mana yang harus digunakan.

---

<Note>
  Organisasi Claude Enterprise memiliki akses swalayan ke API lengkap. Organisasi Claude Console diaktifkan berdasarkan permintaan; hubungi tim akun Anda. Halaman ini menjelaskan cara meminta akses dan membuat kunci API.
</Note>

<Check>
  **Peran yang diperlukan:** admin organisasi (Claude Console) atau pemilik utama (claude.ai).
</Check>

Compliance API menggunakan dua jenis kunci, dan kunci mana yang Anda buat bergantung pada produk Claude mana yang digunakan organisasi Anda. Pemilik utama membuat Compliance Access Key di claude.ai; kunci ini membuka akses ke seluruh Compliance API. Admin organisasi membuat kunci Admin API di Claude Console; kunci ini hanya membuka akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

## Kunci mana yang Anda butuhkan? \{#which-key-do-you-need}

| Jenis kunci                                    | Dibuat di                               | Digunakan untuk                                                                                                | Berfungsi dengan Compliance API? |
| ---------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **Compliance Access Key** (`sk-ant-api01-...`) | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)  | Activity Feed, obrolan, file, proyek, pengguna, metadata organisasi, dan pengaturan organisasi                 | Ya (semua endpoint)            |
| **Kunci Admin API** (`sk-ant-admin01-...`)           | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys)  | [Admin API](/docs/id/manage-claude/admin-api) dan Activity Feed dari Compliance API  | Hanya Activity Feed             |
| **Kunci Analytics API**                          | [claude.ai > Analytics > API keys](https://claude.ai/analytics/api-keys)        | [Claude Enterprise Analytics API](https://support.claude.com/en/articles/13694757-claude-enterprise-analytics-api-access-engagement-and-adoption-data)                                                                            | Tidak                             |
| **Kunci Claude API** (`sk-ant-api03-...`)        | [Claude Console > Settings > API keys](https://platform.claude.com/settings/keys)    | Memanggil model Claude melalui [Claude API](/docs/id/api/overview)                                          | Tidak                             |

Tenant Claude Enterprise memiliki satu **organisasi induk** yang memusatkan identitas, SSO, dan SCIM untuk setiap organisasi beban kerja di bawahnya. Organisasi beban kerja ini adalah **organisasi tertaut** dari induk tersebut.

<Warning>
  **Organisasi induk Claude Enterprise tidak muncul di Claude Console (`platform.claude.com`).** Induk tidak membawa beban kerja, tidak memiliki kunci Claude API, dan tidak memiliki kunci Admin API. Buat Compliance Access Key di **Organization settings** claude.ai, bukan di Claude Console.
</Warning>

## Meminta akses Compliance API \{#request-compliance-api-access}

Pemilik utama Claude Enterprise dapat mengaktifkan Compliance API langsung di claude.ai. Organisasi Claude Console harus menghubungi tim akun mereka untuk meminta akses. Dalam kedua kasus, pengaktifan terjadi di tingkat organisasi induk dan diturunkan ke setiap organisasi tertaut, baik claude.ai maupun Claude Console. Apa yang berubah setelah pengaktifan bergantung pada produk Claude mana yang digunakan organisasi Anda.

### Setelah pengaktifan: organisasi claude.ai \{#after-enablement-claude-ai-organizations}

Setelah Compliance API diaktifkan untuk organisasi induk Anda, pemilik utama dapat [membuat Compliance Access Key](#create-a-compliance-access-key) dari bagian **Keys** di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access).

### Setelah pengaktifan: organisasi Claude Console \{#after-enablement-claude-console-organizations}

Setelah Anthropic mengaktifkan Compliance API untuk organisasi induk Anda, kunci Admin API yang dibuat sejak saat itu membawa cakupan `read:compliance_activities`. Kunci Admin API yang dibuat sebelum pengaktifan tetap berfungsi dengan Admin API, tetapi memanggil Activity Feed dengan kunci tersebut akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden); [buat kunci Admin API baru](#create-an-admin-api-key) untuk mendapatkan cakupan tersebut.

## Membuat Compliance Access Key \{#create-a-compliance-access-key}

<Note>
  Compliance API harus sudah [diaktifkan untuk organisasi induk claude.ai Anda](#request-compliance-api-access) sebelum Compliance Access Key dapat dibuat.
</Note>

<Warning>
  Compliance Access Key dengan `read:compliance_user_data` dapat membaca setiap obrolan,
  file, dan proyek di setiap organisasi tertaut, termasuk konten yang belum
  dilihat oleh pemilik utama. Kunci dengan `delete:compliance_user_data` dapat menghapus
  konten tersebut secara permanen. Perlakukan Compliance Access Key seperti kredensial
  database produksi: simpan di pengelola rahasia (secrets manager), jangan pernah di kontrol sumber atau
  konfigurasi forwarder SIEM.
</Warning>

<Steps>
  <Step title="Masuk sebagai pemilik utama">
    Hanya pemilik utama dari organisasi induk yang dapat membuat Compliance Access Key. Jika halaman **API** yang dijelaskan di langkah berikutnya tidak terlihat, atau cakupan kepatuhan tidak tersedia saat membuat kunci, berarti Anda bukan pemilik utama, atau Compliance API belum diaktifkan untuk organisasi Anda (lihat [Meminta akses Compliance API](#request-compliance-api-access)).
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama kunci tersebut, dan pilih satu atau beberapa cakupan dari tabel berikut. Klik **Create**.

    | Cakupan                        | Memberikan                                                                      |
    | ------------------------------ | ------------------------------------------------------------------------------- |
    | `read:compliance_activities`   | Membaca Activity Feed untuk organisasi induk dan semua organisasi tertaut |
    | `read:compliance_user_data`    | Membaca obrolan pengguna, pesan, file, proyek, pengguna organisasi, dan anggota grup |
    | `delete:compliance_user_data`  | Menghapus obrolan, file, dan proyek pengguna                                          |
    | `read:compliance_org_data`     | Membaca metadata organisasi (nama, jenis, peran, dan grup). Daftar pengguna dan keanggotaan grup memerlukan `read:compliance_user_data`. |
    | `read:compliance_org_settings` | Membaca pengaturan efektif yang berlaku untuk organisasi di bawah organisasi induk                                                  |

    Pilih set cakupan terkecil yang dibutuhkan integrasi Anda:

    - Pipeline audit yang hanya membaca Activity Feed hanya memerlukan `read:compliance_activities`.
    - Alat eDiscovery yang membaca obrolan dan file tetapi tidak pernah menghapusnya tidak memerlukan `delete:compliance_user_data`.
    - Jika alur kerja Anda membaca sekaligus menghapus, gunakan **dua kunci** dengan cakupan terpisah sehingga kunci baca yang bocor tidak dapat menghapus data.

    Cakupan Compliance Access Key tidak dapat diubah setelah dibuat. Untuk mengubah cakupan, buat kunci baru dengan cakupan yang Anda inginkan, lalu hapus kunci lama.
  </Step>

  <Step title="Salin dan simpan rahasia">
    Salin kunci rahasia yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di pengelola rahasia Anda. Rahasia lengkap hanya ditampilkan satu kali.
  </Step>

  <Step title="Ekspor kunci untuk contoh dalam panduan ini">
    Tetapkan kunci sebagai variabel lingkungan sehingga contoh shell dalam panduan ini dapat membacanya:

    ```bash
    export ANTHROPIC_COMPLIANCE_ACCESS_KEY=sk-ant-api01-...
    ```
  </Step>
</Steps>

## Membuat kunci Admin API \{#create-an-admin-api-key}

<Note>
  Compliance API harus sudah [diaktifkan untuk organisasi Claude Console Anda](#request-compliance-api-access) sebelum kunci Admin API dapat memanggil Activity Feed.
</Note>

<Steps>
  <Step title="Masuk sebagai admin organisasi">
    Hanya anggota organisasi dengan peran **admin** yang dapat membuat kunci Admin API. Lihat [Peran dan izin organisasi](/docs/id/manage-claude/admin-api#organization-roles-and-permissions) untuk daftar peran lengkap.
  </Step>

  <Step title="Buka pengaturan Admin keys">
    Buka [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama kunci tersebut, dan klik **Create**.
  </Step>

  <Step title="Salin dan simpan rahasia">
    Salin kunci rahasia yang ditampilkan (dimulai dengan `sk-ant-admin01-`) dan simpan di pengelola rahasia Anda. Rahasia lengkap hanya ditampilkan satu kali.
  </Step>

  <Step title="Ekspor kunci untuk digunakan dengan Activity Feed">
    Tetapkan kunci sebagai variabel lingkungan:

    ```bash
    export ANTHROPIC_ADMIN_KEY=sk-ant-admin01-...
    ```

    Nama variabel yang berbeda mencegah kunci Admin API menimpa Compliance Access Key jika Anda menyediakan keduanya. Contoh cURL dalam panduan ini membaca kunci dari `$ANTHROPIC_COMPLIANCE_ACCESS_KEY`; ganti dengan `$ANTHROPIC_ADMIN_KEY` saat memanggil [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dengan kunci Admin API.
  </Step>
</Steps>

Kunci Admin API membawa cakupan `read:compliance_activities` hanya jika Compliance API telah diaktifkan untuk organisasi sebelum kunci tersebut dibuat; lihat [Setelah pengaktifan: organisasi Claude Console](#after-enablement-claude-console-organizations). Kunci ini tidak dapat diberikan cakupan Compliance API lainnya, sehingga panggilan ke endpoint apa pun selain Activity Feed akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Untuk peran kunci yang sama dalam mengelola organisasi Claude Console Anda, lihat [Admin API](/docs/id/manage-claude/admin-api).

## Memeriksa cakupan kunci Anda \{#check-your-keys-scopes}

Untuk memeriksa cakupan pada kunci yang sudah Anda miliki, gunakan salah satu sinyal berikut.

- **Prefiks kunci.** `sk-ant-admin01-` adalah kunci Admin API (hanya membawa `read:compliance_activities`, tergantung pada waktu pengaktifan di bagian sebelumnya). `sk-ant-api01-` adalah Compliance Access Key; cakupannya adalah subset yang Anda pilih saat pembuatan.
- **UI Pengaturan.** Buka bagian **Keys** di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), atau bagian **Admin keys** di [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys), dan baca kolom **Scopes** untuk kunci tersebut.
- **Respons kesalahan.** Panggilan yang melebihi cakupan kunci akan mengembalikan 403 dengan pesan dalam format `Missing required scopes. Got: [<scopes the key carries>] Needed: [<scopes the endpoint requires>]`. Lihat [Menangani kesalahan Compliance API](/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog kesalahan lengkap.

```json
{
  "error": {
    "type": "permission_error",
    "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
  }
}
```

## Mengelola dan merotasi kunci \{#manage-and-rotate-keys}

Hapus Compliance Access Key dari tabel **Keys** yang sama tempat Anda membuatnya: buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Hapus kunci Admin API dari [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).

Penghapusan kunci berlaku pada permintaan berikutnya: tidak ada masa tenggang. Compliance Access Key tidak kedaluwarsa dengan sendirinya.

Untuk merotasi kunci tanpa gangguan layanan:

1. Buat kunci baru dengan cakupan yang sama.
2. Perbarui integrasi Anda untuk menggunakan kunci baru.
3. Verifikasi bahwa integrasi berhasil dengan kunci baru.
4. Hapus kunci lama.

Kursor paginasi yang disimpan sebelum rotasi tetap valid: kursor dicakupkan ke organisasi, bukan ke kunci.

Jika Compliance Access Key bocor, hapus segera, audit [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) untuk aktivitas `compliance_api_accessed` oleh kunci yang disusupi, dan rotasi kredensial hilir apa pun yang dapat dijangkau oleh kunci yang bocor. Berikan `activity_types[]=compliance_api_accessed` untuk membatasi cakupan kueri, lalu di klien Anda, simpan aktivitas yang `actor.type`-nya adalah `api_actor` dan `actor.api_key_id`-nya cocok dengan kunci yang disusupi; lihat [Memahami objek Activity](/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object) untuk skema actor.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Mengkueri Activity Feed" href="/docs/id/manage-claude/compliance-activity-feed">
    Baca peristiwa aktivitas di seluruh organisasi dengan kunci apa pun yang memiliki `read:compliance_activities`.
  </Card>
  <Card title="Mengambil dan menghapus obrolan, file, dan proyek" href="/docs/id/manage-claude/compliance-content-data">
    Gunakan Compliance Access Key dengan `read:compliance_user_data` untuk mengambil konten claude.ai, dan `delete:compliance_user_data` untuk menghapusnya.
  </Card>
</CardGroup>