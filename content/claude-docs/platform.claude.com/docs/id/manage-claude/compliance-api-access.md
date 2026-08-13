---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api-access
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 1907e3a50745310f1c596d95d4037de2d850d89b7832318355cebea33ddabb7d
---

---
title: Menyiapkan Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-api-access
description: Aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin bercakupan) atau kunci Admin API, dan pelajari mana yang harus digunakan.
---

<Note>
  Organisasi Claude Enterprise dan organisasi Claude Console mandiri yang memenuhi syarat memiliki akses swalayan ke Compliance API. Halaman ini menjelaskan cara mengaktifkan Compliance API untuk organisasi Anda dan membuat kunci API.
</Note>

<Check>
  **Peran yang diperlukan:** organization admin (Claude Console), atau primary owner atau organization owner (claude.ai).
</Check>

Compliance API menggunakan dua jenis kunci, dan kunci mana yang Anda buat bergantung pada produk Claude yang digunakan organisasi Anda. Primary owner dan organization owner membuat Compliance Access Key di claude.ai; kunci ini membuka akses ke seluruh Compliance API. Kunci milik primary owner dapat mencakup setiap organisasi di bawah organisasi induk; kunci milik organization owner hanya mencakup organisasi mereka sendiri. Organization admin membuat kunci Admin API di Claude Console; kunci ini hanya membuka akses ke [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

## Kunci mana yang Anda butuhkan?

| Jenis kunci                                    | Dibuat di                                                                                 | Digunakan untuk                                                                                                             | Berfungsi dengan Compliance API? |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Compliance Access Key** (`sk-ant-api01-...`) | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Activity Feed, obrolan, file, proyek, sesi Cowork dan Claude Code, pengguna, metadata organisasi, dan pengaturan organisasi | Ya (semua endpoint)              |
| **Kunci Admin API** (`sk-ant-admin01-...`)     | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) dan Activity Feed Compliance API                   | Hanya Activity Feed              |
| **Kunci Analytics API**                        | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Claude Enterprise Analytics API (lihat [Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api))    | Tidak                            |
| **Kunci Claude API** (`sk-ant-api03-...`)      | [Claude Console > Settings > API keys](https://platform.claude.com/settings/keys)         | Memanggil model Claude melalui [Claude API](https://platform.claude.com/docs/id/api/overview)                               | Tidak                            |

Tenant Claude Enterprise memiliki satu **organisasi induk** yang memusatkan identitas, SSO, dan SCIM untuk setiap organisasi beban kerja di bawahnya. Organisasi beban kerja ini adalah **organisasi tertaut** dari induk tersebut.

<Warning>
  **Organisasi induk Claude Enterprise tidak muncul di Claude Console (`platform.claude.com`).** Induk tidak membawa beban kerja, tidak memiliki kunci Claude API, dan tidak memiliki kunci Admin API. Buat Compliance Access Key di **Organization settings** claude.ai, bukan di Claude Console.
</Warning>

## Menyiapkan Compliance API

Penyiapan adalah satu alur: aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key di claude.ai. Organisasi Claude Console sebagai gantinya [membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) setelah pengaktifan; kunci Admin API hanya menjangkau [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

<Warning>
  Compliance Access Key dengan `read:compliance_user_data` dapat membaca setiap obrolan, file, proyek, dan transkrip sesi Cowork dan Claude Code di setiap organisasi tertaut, termasuk konten yang belum dilihat oleh primary owner. Kunci dengan `delete:compliance_user_data` dapat menghapus obrolan, file, dan proyek secara permanen. Perlakukan Compliance Access Key seperti kredensial database produksi: simpan di secrets manager, jangan pernah di source control atau konfigurasi SIEM forwarder.
</Warning>

<Steps>
  <Step title="Aktifkan Compliance API">
    Tempat Anda mengaktifkan Compliance API bergantung pada bagaimana organisasi Anda disiapkan:

    * **Organisasi Claude Enterprise:** Primary owner mengaktifkan Compliance API di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Pengaktifan terjadi di tingkat organisasi induk dan diturunkan ke setiap organisasi tertaut, baik claude.ai maupun Claude Console.
    * **Organisasi Claude Console mandiri:** Organization admin mengaktifkan toggle **Compliance API** di [Claude Console > Settings > Security](https://platform.claude.com/settings/security). Pengaktifan bersifat swalayan untuk organisasi yang memenuhi syarat, dan perubahan berlaku segera. Jika bagian **Compliance API** tidak terlihat, Anda tidak memiliki peran admin, organisasi Anda tertaut ke organisasi induk (Compliance API diaktifkan dari organisasi induk sebagai gantinya), atau organisasi Anda tidak memenuhi syarat untuk pengaktifan swalayan; hubungi tim akun Anda atau [dukungan Anthropic](https://support.claude.com) jika Anda tidak yakin mana yang berlaku.
    * **Organisasi Claude Console yang tertaut ke organisasi induk:** Tidak ada yang perlu diaktifkan di Claude Console. Minta primary owner organisasi induk Anda untuk mengaktifkan Compliance API di claude.ai, atau hubungi tim akun Anda.

    <Warning>
      **Menonaktifkan Compliance API menghentikan perekaman aktivitas.** Organization admin dapat menonaktifkan Compliance API kapan saja dengan toggle **Compliance API** yang sama yang digunakan untuk mengaktifkannya. Selama Compliance API nonaktif, tidak ada peristiwa aktivitas yang direkam untuk organisasi Anda, sehingga [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) tidak menerima peristiwa baru. Jika organisasi Anda terdaftar di [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency), menonaktifkan Compliance API juga menghentikan pengiriman peristiwa Access Transparency. Aktivitas yang tidak direkam selama Compliance API nonaktif tidak dapat dipulihkan nanti. Mengaktifkan kembali Compliance API melanjutkan perekaman dari titik tersebut ke depan; aktivitas yang sudah direkam tidak dihapus. Untuk organisasi Claude Enterprise, pengaturan Compliance API di claude.ai juga mengatur penangkapan transkrip sesi Cowork dan Claude Code untuk endpoint sesi lokal (sesi yang berjalan di mesin pengguna): penangkapan dimulai ketika Compliance API diaktifkan dan berhenti selama nonaktif, dan konten transkrip dari sesi yang berjalan selama nonaktif tidak ditangkap dan tidak dapat dipulihkan nanti.
    </Warning>

    Organisasi Claude Console mandiri menggunakan kunci Admin API alih-alih Compliance Access Key: setelah pengaktifan, lewati langkah-langkah yang tersisa dan [buat kunci Admin API baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) sebagai gantinya. Langkah-langkah yang tersisa menyediakan Compliance Access Key, yang hanya tersedia untuk organisasi yang merupakan bagian dari tenant Claude Enterprise.
  </Step>

  <Step title="Tentukan cakupan kunci">
    Akses kunci ditetapkan saat kunci dibuat. Tentukan organisasi mana yang dicakup oleh kunci:

    * Kunci untuk **organisasi induk** dapat mengakses setiap organisasi di bawah organisasi induk.
    * Kunci untuk **satu organisasi** hanya dapat mengakses organisasi tersebut.
  </Step>

  <Step title="Masuk dengan peran yang sesuai">
    Masuk ke claude.ai. Primary owner organisasi induk dapat membuat kunci dengan salah satu cakupan. Organization owner hanya dapat membuat kunci yang dibatasi untuk organisasi mereka sendiri.

    Jika halaman **API** yang dijelaskan di langkah berikutnya tidak terlihat, atau cakupan compliance tidak tersedia saat membuat kunci, berarti peran Anda tidak dapat membuat Compliance Access Key, atau Compliance API belum diaktifkan untuk organisasi Anda (kembali ke langkah pertama).
  </Step>

  <Step title="Buka pengaturan API">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan temukan bagian **Keys**.
  </Step>

  <Step title="Buat kunci">
    Klik **Create key**, beri nama kunci, dan pilih satu atau beberapa cakupan dari tabel berikut. Klik **Create**.

    | Cakupan                       | Memberikan                                                                                                                                                                                                                |
    | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `read:compliance_activities`  | Membaca Activity Feed. Kunci yang mencakup organisasi induk membaca peristiwa untuk organisasi induk dan semua organisasi tertaut.                                                                                        |
    | `read:compliance_user_data`   | Membaca obrolan pengguna, pesan, file, proyek, sesi Cowork dan Claude Code beserta transkripnya, pengguna organisasi, dan anggota grup                                                                                    |
    | `delete:compliance_user_data` | Menghapus obrolan, file, dan proyek pengguna                                                                                                                                                                              |
    | `read:compliance_org_data`    | Membaca metadata organisasi (nama, jenis, peran, dan grup) serta pengaturan efektif yang berlaku untuk organisasi di bawah organisasi induk. Daftar pengguna dan keanggotaan grup memerlukan `read:compliance_user_data`. |

    Pilih set cakupan terkecil yang dibutuhkan integrasi Anda:

    * Pipeline audit yang hanya membaca Activity Feed hanya membutuhkan `read:compliance_activities`.
    * Alat eDiscovery yang membaca obrolan dan file tetapi tidak pernah menghapusnya tidak membutuhkan `delete:compliance_user_data`.
    * Jika alur kerja Anda membaca sekaligus menghapus, gunakan **dua kunci** dengan cakupan terpisah sehingga kunci baca yang bocor tidak dapat menghapus data.

    Cakupan Compliance Access Key tidak dapat diubah setelah dibuat. Untuk mengubah cakupan, buat kunci baru dengan cakupan yang Anda inginkan, lalu hapus kunci lama.
  </Step>

  <Step title="Salin dan simpan secret">
    Salin secret key yang ditampilkan (dimulai dengan `sk-ant-api01-`) dan simpan di secrets manager Anda. Secret lengkap hanya ditampilkan satu kali.
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
  Compliance API harus sudah [diaktifkan untuk organisasi Claude Console Anda](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) sebelum kunci Admin API dapat memanggil Activity Feed.
</Note>

Ikuti langkah-langkah di [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization), lalu tetapkan kunci sebagai variabel lingkungan:

```bash
export ANTHROPIC_ADMIN_KEY=sk-ant-admin01-...
```

Nama variabel yang berbeda mencegah kunci Admin API menimpa Compliance Access Key jika Anda menyediakan keduanya. Contoh cURL dalam panduan ini membaca kunci dari `$ANTHROPIC_COMPLIANCE_ACCESS_KEY`; ganti dengan `$ANTHROPIC_ADMIN_KEY` saat memanggil [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dengan kunci Admin API.

Kunci Admin API membawa cakupan `read:compliance_activities` hanya jika Compliance API telah diaktifkan untuk organisasi pada saat kunci dibuat; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api). Kunci ini tidak dapat diberikan cakupan Compliance API lainnya, sehingga panggilan ke endpoint apa pun selain Activity Feed mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Untuk peran kunci yang sama dalam mengelola organisasi Claude Console Anda, lihat [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api).

## Memeriksa cakupan kunci Anda

Untuk memeriksa cakupan pada kunci yang sudah Anda miliki, gunakan salah satu sinyal berikut.

* **Prefiks kunci.** `sk-ant-admin01-` adalah kunci Admin API (hanya membawa `read:compliance_activities`, tergantung pada waktu pengaktifan di bagian sebelumnya). `sk-ant-api01-` adalah Compliance Access Key; cakupannya adalah subset yang Anda pilih saat pembuatan.
* **UI Pengaturan.** Buka bagian **Keys** di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), atau bagian **Admin keys** di [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys), dan baca kolom **Scopes** untuk kunci tersebut.
* **Respons error.** Panggilan yang melebihi cakupan kunci mengembalikan 403 dengan pesan dalam format `Missing required scopes. Got: [<scopes the key carries>] Needed: [<scopes the endpoint requires>]`. Lihat [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog error lengkap.

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

Kursor paginasi yang disimpan sebelum rotasi tetap valid: kursor dicakupkan ke organisasi, bukan ke kunci.

Jika Compliance Access Key bocor, hapus segera, audit [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) untuk aktivitas `compliance_api_accessed` oleh kunci yang disusupi, dan rotasi kredensial hilir apa pun yang dapat dijangkau oleh kunci yang bocor. Berikan `activity_types[]=compliance_api_accessed` untuk membatasi cakupan kueri, lalu di klien Anda, pertahankan aktivitas yang `actor.type`-nya adalah `api_actor` dan `actor.api_key_id`-nya cocok dengan kunci yang disusupi; lihat [Memahami objek Activity](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object) untuk skema actor.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Mengkueri Activity Feed" href="https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed">
    Baca peristiwa aktivitas di seluruh organisasi dengan kunci apa pun yang memiliki `read:compliance_activities`.
  </Card>

  <Card title="Mengambil dan menghapus obrolan, file, proyek, dan sesi" href="https://platform.claude.com/docs/id/manage-claude/compliance-content-data">
    Gunakan Compliance Access Key dengan `read:compliance_user_data` untuk mengambil konten Claude Enterprise, termasuk transkrip sesi Cowork dan Claude Code, dan `delete:compliance_user_data` untuk menghapus obrolan, file, dan proyek.
  </Card>
</CardGroup>
