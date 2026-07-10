---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api-access
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 58cfd427c8b13b91c0f07e3182a1452e53ffe554c8a9278a35b70c4939481967
---

# Menyiapkan Compliance API

Aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin terbatas) atau kunci Admin API, dan pelajari mana yang harus digunakan.

---

<Note>
  Organisasi Claude Enterprise memiliki akses layanan mandiri ke API lengkap. Organisasi Claude Console diaktifkan berdasarkan permintaan; hubungi tim akun Anda. Halaman ini menjelaskan cara mengaktifkan Compliance API dan membuat kunci API.
</Note>

<Check>
  **Peran yang diperlukan:** admin organisasi (Claude Console), atau pemilik utama atau pemilik organisasi (claude.ai).
</Check>

Compliance API menggunakan dua jenis kunci, dan kunci mana yang Anda buat bergantung pada produk Claude mana yang digunakan organisasi Anda. Pemilik utama dan pemilik organisasi membuat Compliance Access Key di claude.ai; kunci ini membuka akses ke seluruh Compliance API. Kunci milik pemilik utama dapat mencakup setiap organisasi di bawah organisasi induk; kunci milik pemilik organisasi hanya mencakup organisasinya sendiri. Admin organisasi membuat kunci Admin API di Claude Console; kunci ini hanya membuka akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

## Kunci mana yang Anda butuhkan?

| Jenis kunci                                    | Dibuat di                                                                                 | Digunakan untuk                                                                                   | Berfungsi dengan Compliance API? |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Compliance Access Key** (`sk-ant-api01-...`) | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Activity Feed, percakapan, file, proyek, pengguna, metadata organisasi, dan pengaturan organisasi | Ya (semua endpoint)              |
| **Kunci Admin API** (`sk-ant-admin01-...`)     | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | [Admin API](/docs/id/manage-claude/admin-api) dan Activity Feed Compliance API                    | Hanya Activity Feed              |
| **Kunci Analytics API**                        | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Claude Enterprise Analytics API (lihat [Analytics APIs](/docs/id/manage-claude/analytics-api))    | Tidak                            |
| **Kunci Claude API** (`sk-ant-api03-...`)      | [Claude Console > Settings > API keys](https://platform.claude.com/settings/keys)         | Memanggil model Claude melalui [Claude API](/docs/id/api/overview)                                | Tidak                            |

Sebuah tenant Claude Enterprise memiliki satu **organisasi induk** yang memusatkan identitas, SSO, dan SCIM untuk setiap organisasi beban kerja di bawahnya. Organisasi beban kerja ini adalah **organisasi tertaut** dari organisasi induk.

<Warning>
  **Organisasi induk Claude Enterprise tidak muncul di Claude Console (`platform.claude.com`).** Organisasi induk tidak membawa beban kerja, tidak memiliki kunci Claude API, dan tidak memiliki kunci Admin API. Buat Compliance Access Key di **Organization settings** claude.ai, bukan di Claude Console.
</Warning>

## Menyiapkan Compliance API

Penyiapan adalah satu alur: aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key di claude.ai. Organisasi Claude Console sebagai gantinya [membuat kunci Admin API](#create-an-admin-api-key) setelah pengaktifan; kunci Admin API hanya menjangkau [Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

<Warning>
  Compliance Access Key dengan `read:compliance_user_data` dapat membaca setiap percakapan, file, dan proyek di setiap organisasi tertaut, termasuk konten yang belum pernah dilihat oleh pemilik utama. Kunci dengan `delete:compliance_user_data` dapat menghapus konten tersebut secara permanen. Perlakukan Compliance Access Key seperti kredensial database produksi: simpan di secrets manager, jangan pernah di source control atau konfigurasi forwarder SIEM.
</Warning>

<Steps>
  <Step title="Aktifkan Compliance API">
    Cara Anda mengaktifkan Compliance API bergantung pada produk Claude mana yang digunakan organisasi Anda. Dalam kedua kasus, pengaktifan terjadi di tingkat organisasi induk dan diteruskan ke setiap organisasi tertaut.

    * **Claude Enterprise (`claude.ai`):** Pengaktifan bersifat layanan mandiri.
    * **Claude Console (`platform.claude.com`):** Pengaktifan berdasarkan permintaan: hubungi tim akun Anthropic Anda.
  </Step>

  <Step title="Tentukan cakupan kunci">
    Akses sebuah kunci ditetapkan saat kunci tersebut dibuat. Tentukan organisasi mana yang dicakup oleh kunci:

    * Kunci untuk **organisasi induk** dapat mengakses setiap organisasi di bawah organisasi induk.
    * Kunci untuk **satu organisasi** hanya dapat mengakses organisasi tersebut.
  </Step>

  <Step title="Masuk dengan peran yang sesuai">
    Masuk ke claude.ai. Pemilik utama organisasi induk dapat membuat kunci dengan salah satu cakupan. Pemilik organisasi dapat membuat kunci yang dibatasi hanya untuk organisasinya sendiri.

    Jika halaman **API** yang dijelaskan pada langkah berikutnya tidak terlihat, atau cakupan compliance tidak tersedia saat membuat kunci, berarti peran Anda tidak dapat membuat Compliance Access Key, atau Compliance API belum diaktifkan untuk organisasi Anda (kembali ke langkah pertama).
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama kunci, dan pilih satu atau lebih cakupan dari tabel berikut. Klik **Create**.

    | Cakupan                       | Memberikan                                                                                                                                                                                                                |
    | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `read:compliance_activities`  | Membaca Activity Feed. Kunci yang mencakup organisasi induk membaca peristiwa untuk organisasi induk dan semua organisasi tertaut.                                                                                        |
    | `read:compliance_user_data`   | Membaca percakapan pengguna, pesan, file, proyek, pengguna organisasi, dan anggota grup                                                                                                                                   |
    | `delete:compliance_user_data` | Menghapus percakapan, file, dan proyek pengguna                                                                                                                                                                           |
    | `read:compliance_org_data`    | Membaca metadata organisasi (nama, jenis, peran, dan grup) serta pengaturan efektif yang berlaku untuk organisasi di bawah organisasi induk. Daftar pengguna dan keanggotaan grup memerlukan `read:compliance_user_data`. |

    Pilih set cakupan terkecil yang dibutuhkan integrasi Anda:

    * Pipeline audit yang hanya membaca Activity Feed hanya memerlukan `read:compliance_activities`.
    * Alat eDiscovery yang membaca percakapan dan file tetapi tidak pernah menghapusnya tidak memerlukan `delete:compliance_user_data`.
    * Jika alur kerja Anda membaca sekaligus menghapus, gunakan **dua kunci** dengan cakupan terpisah sehingga kunci baca yang bocor tidak dapat menghapus data.

    Cakupan Compliance Access Key tidak dapat diubah setelah pembuatan. Untuk mengubah cakupan, buat kunci baru dengan cakupan yang Anda inginkan, lalu hapus kunci lama.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin kunci rahasia yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
  </Step>

  <Step title="Ekspor kunci untuk contoh dalam panduan ini">
    Tetapkan kunci sebagai variabel lingkungan sehingga contoh shell dalam panduan ini dapat membacanya:

    ```bash
    export ANTHROPIC_COMPLIANCE_ACCESS_KEY=sk-ant-api01-...
    ```
  </Step>
</Steps>

## Membuat kunci Admin API

<Note>
  Compliance API harus sudah [diaktifkan untuk organisasi Claude Console Anda](#set-up-the-compliance-api) sebelum kunci Admin API dapat memanggil Activity Feed.
</Note>

Ikuti langkah-langkah di [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization), lalu tetapkan kunci sebagai variabel lingkungan:

```bash
export ANTHROPIC_ADMIN_KEY=sk-ant-admin01-...
```

Nama variabel yang berbeda mencegah kunci Admin API menimpa Compliance Access Key jika Anda menyediakan keduanya. Contoh cURL dalam panduan ini membaca kunci dari `$ANTHROPIC_COMPLIANCE_ACCESS_KEY`; gantikan dengan `$ANTHROPIC_ADMIN_KEY` saat memanggil [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) dengan kunci Admin API.

Kunci Admin API hanya membawa cakupan `read:compliance_activities` jika Compliance API diaktifkan untuk organisasi sebelum kunci dibuat; lihat [Menyiapkan Compliance API](#set-up-the-compliance-api). Kunci tersebut tidak dapat diberikan cakupan Compliance API lainnya, sehingga panggilan ke endpoint apa pun selain Activity Feed mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Untuk peran kunci yang sama dalam mengelola organisasi Claude Console Anda, lihat [Admin API](/docs/id/manage-claude/admin-api).

## Memeriksa cakupan kunci Anda

Untuk memeriksa cakupan pada kunci yang sudah Anda miliki, gunakan salah satu sinyal berikut.

* **Prefiks kunci.** `sk-ant-admin01-` adalah kunci Admin API (hanya membawa `read:compliance_activities`, tergantung pada waktu pengaktifan di bagian sebelumnya). `sk-ant-api01-` adalah Compliance Access Key; cakupannya adalah subset yang Anda pilih saat pembuatan.
* **UI Pengaturan.** Buka bagian **Keys** di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), atau bagian **Admin keys** di [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys), dan baca kolom **Scopes** untuk kunci tersebut.
* **Respons kesalahan.** Panggilan yang melebihi cakupan kunci mengembalikan 403 dengan pesan dalam format `Missing required scopes. Got: [<scopes the key carries>] Needed: [<scopes the endpoint requires>]`. Lihat [Menangani kesalahan Compliance API](/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog kesalahan lengkap.

```json
{
  "error": {
    "type": "permission_error",
    "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
  }
}
```

## Mengelola dan merotasi kunci

Hapus Compliance Access Key dari tabel **Keys** yang sama tempat Anda membuatnya: buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Hapus kunci Admin API dari [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).

Penghapusan kunci berlaku pada permintaan berikutnya: tidak ada masa tenggang. Compliance Access Key tidak kedaluwarsa dengan sendirinya.

Untuk merotasi kunci tanpa gangguan layanan:

1. Buat kunci baru dengan cakupan yang sama.
2. Perbarui integrasi Anda untuk menggunakan kunci baru.
3. Verifikasi bahwa integrasi berhasil dengan kunci baru.
4. Hapus kunci lama.

Kursor paginasi yang disimpan sebelum rotasi tetap valid: kursor dicakup ke organisasi, bukan ke kunci.

Jika Compliance Access Key bocor, segera hapus, audit [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) untuk aktivitas `compliance_api_accessed` oleh kunci yang terkompromi, dan rotasi kredensial hilir apa pun yang dapat dijangkau oleh kunci yang bocor. Teruskan `activity_types[]=compliance_api_accessed` untuk membatasi kueri, lalu di klien Anda, simpan aktivitas yang `actor.type`-nya adalah `api_actor` dan yang `actor.api_key_id`-nya cocok dengan kunci yang terkompromi; lihat [Memahami objek Activity](/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object) untuk skema actor.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kueri Activity Feed" href="/docs/id/manage-claude/compliance-activity-feed">
    Baca peristiwa aktivitas di seluruh organisasi dengan kunci apa pun yang memiliki `read:compliance_activities`.
  </Card>

  <Card title="Mengambil dan menghapus percakapan, file, dan proyek" href="/docs/id/manage-claude/compliance-content-data">
    Gunakan Compliance Access Key dengan `read:compliance_user_data` untuk mengambil konten claude.ai, dan `delete:compliance_user_data` untuk menghapusnya.
  </Card>
</CardGroup>
