---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 63cb29de1b90220d8cea995c904e5119ac31f0ea4094bd30802cd043fd4136d9
---

# FAQ Compliance API

Jawaban atas pertanyaan umum tentang akses Compliance API, cakupan, retensi, dan integrasi.

---

<Note>
  Compliance API diaktifkan berdasarkan permintaan. Organisasi Claude Enterprise memiliki akses ke API lengkap; organisasi Claude Console hanya memiliki akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

## Akses dan cakupan \{#access-and-scopes}

<section title="Mengapa organisasi induk saya tidak muncul di Claude Console saat membuat kunci Admin API?">

  Hal ini memang diharapkan. Organisasi induk Claude Enterprise memusatkan identitas di seluruh organisasi yang tertaut; organisasi induk tidak menjalankan beban kerja, dan tidak muncul di Claude Console sama sekali. Claude Console hanya menampilkan organisasi Claude Console yang tertaut di bawah organisasi induk.

  Untuk memanggil Compliance API, Anda membuat salah satu dari dua jenis kunci berikut:

  - **Untuk akses penuh Compliance API ([Activity Feed](/docs/id/manage-claude/compliance-activity-feed) ditambah obrolan, file, proyek, pengguna, dan metadata organisasi),** pemilik utama organisasi induk membuat [Compliance Access Key](/docs/id/manage-claude/compliance-api-access#create-a-compliance-access-key) di claude.ai.
  - **Untuk akses Activity Feed saja,** admin organisasi di organisasi Claude Console Anda membuat [kunci Admin API](/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) di Claude Console. Compliance API harus sudah diaktifkan untuk organisasi tersebut, dan admin harus membuat kunci Admin API setelah pengaktifan agar kunci tersebut membawa cakupan `read:compliance_activities`.

</section>

<section title="Dapatkah saya menggunakan kunci Claude API reguler saya dengan Compliance API?">

  Tidak. Kunci Claude API (`sk-ant-api03-...`) mengautentikasi panggilan ke model Claude pada Claude API; kunci tersebut tidak mengautentikasi panggilan ke `/v1/compliance/*`. Compliance API hanya menerima Compliance Access Key (`sk-ant-api01-...`) dan kunci Admin API (`sk-ant-admin01-...`). Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk pemetaan lengkapnya.

</section>

<section title="Mengapa kunci Admin API saya mengembalikan 403 pada endpoint obrolan atau file?">

  Kunci Admin API membawa cakupan tetap `read:compliance_activities`, yang hanya mengotorisasi Activity Feed. Setiap endpoint Compliance API lainnya memerlukan cakupan yang hanya dapat dibawa oleh Compliance Access Key yang dibuat di claude.ai. Memanggil endpoint konten atau direktori dengan kunci Admin API akan mengembalikan 403 yang menyebutkan cakupan yang diperlukan oleh kelompok endpoint tersebut: `read:compliance_user_data` untuk obrolan, file, proyek, lampiran proyek, pengguna, dan anggota grup, serta `read:compliance_org_data` untuk organisasi, peran, dan grup. Sebagai contoh, mencantumkan daftar obrolan akan mengembalikan respons berikut.

  ```json Response
  {
    "error": {
      "type": "permission_error",
      "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
    }
  }
  ```

  Untuk mengakses endpoint konten, pemilik utama organisasi induk Anda harus [membuat Compliance Access Key](/docs/id/manage-claude/compliance-api-access#create-a-compliance-access-key) dengan `read:compliance_user_data` (dan `delete:compliance_user_data` untuk penghapusan), atau `read:compliance_org_data` untuk endpoint organisasi, peran, dan grup. Lihat [Menangani kesalahan Compliance API](/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog lengkap per endpoint.

</section>

## Cakupan data dan retensi \{#data-coverage-and-retention}

<section title="Seberapa jauh ke belakang Activity Feed menyimpan data?">

  Activity Feed menyimpan 6 tahun aktivitas organisasi, dan peristiwa baru dapat dikueri dalam waktu 1 menit setelah terjadi. Retensi Activity Feed tidak bergantung pada kebijakan retensi konten organisasi Anda: konten obrolan, file, dan proyek mengikuti aturan retensi yang dikonfigurasi untuk organisasi Anda (tidak terbatas secara default).

</section>

<section title="Apakah Activity Feed menyertakan konten prompt atau pesan?">

  Tidak. Activity Feed mencatat siapa melakukan apa dan kapan (autentikasi, pembuatan obrolan, unggahan file, perubahan proyek, tindakan administratif, dan peristiwa sumber daya serupa), tetapi tidak menangkap teks prompt atau respons model di dalam obrolan atau pesan.

  Untuk mengambil isi pesan dan konten file, gunakan endpoint obrolan, pesan, dan file dengan Compliance Access Key yang membawa `read:compliance_user_data`. Endpoint tersebut hanya menyajikan konten claude.ai; beban kerja Claude Console dan Claude API mengekspos peristiwa administratif dan sumber daya melalui Activity Feed tetapi tidak mengekspos teks prompt atau respons model melalui Compliance API.

</section>

<section title="Apakah konten yang dihapus dapat dipulihkan melalui Compliance API?">

  Tidak. Penghapusan yang dilakukan melalui Compliance API bersifat langsung, permanen, dan tidak dapat dipulihkan. Obrolan yang dihapus pengguna melalui claude.ai dihapus secara lunak (soft-deleted): obrolan tersebut tetap terlihat melalui Compliance API dengan `deleted_at` terisi hingga jendela retensi organisasi Anda berakhir atau Anda menghapusnya secara permanen (hard-delete) melalui API ini. Ambil konten apa pun yang perlu Anda simpan (untuk penahanan hukum atau pengarsipan) sebelum mengirimkan permintaan `DELETE`.

</section>

<section title="Apa yang tidak ditangkap oleh Compliance API?">

  Compliance API memiliki batasan cakupan yang diketahui: Activity Feed mencatat peristiwa sumber daya tetapi bukan teks prompt atau respons, beban kerja Claude Console dan Claude API tidak mengekspos konten pesan sama sekali, dan konten yang dihapus oleh kebijakan retensi Anda atau oleh penghapusan permanen (hard delete) tidak dapat dipulihkan. Untuk batasan cakupan lengkap dan kontrak pengiriman, lihat [Jaminan pengiriman dan kelengkapan](/docs/id/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).

</section>

## Integrasi dan paginasi \{#integration-and-pagination}

<section title="Bagaimana cara mengorelasikan catatan Compliance API dengan SIEM saya?">

  Gabungkan catatan `Activity` ke SIEM Anda berdasarkan `actor.user_id`, `actor.email_address`, `actor.ip_address`, dan `created_at`. Lihat [Merancang integrasi kepatuhan Anda](/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem) untuk tabel kunci penggabungan dan pola konsumsi.

</section>

<section title="Dapatkah satu pelanggan memiliki beberapa organisasi di bawah satu induk?">

  Ya. Organisasi induk Claude Enterprise dapat memiliki banyak organisasi tertaut, termasuk campuran organisasi claude.ai dan organisasi Claude Console (misalnya, organisasi Claude Console produksi dan staging yang terpisah). Identitas, SSO, dan SCIM dibagikan di seluruh induk; penagihan, anggota, proyek, dan kunci API tetap terpisah untuk setiap organisasi. Pengaktifan Compliance API terjadi di tingkat organisasi induk dan diturunkan ke semua organisasi tertaut, dan Compliance Access Key dengan `read:compliance_org_data` dapat mengenumerasi setiap organisasi di bawah induk melalui `GET /v1/compliance/organizations`.

</section>

<section title="Apakah aktivitas dikembalikan secara berurutan, dan bagaimana cara mendeteksi bahwa saya telah mengejar hingga waktu nyata?">

  Aktivitas dikembalikan dari yang terbaru terlebih dahulu, dengan nilai `created_at` yang sama diurutkan berdasarkan ID aktivitas. Untuk mengejar ketertinggalan, telusuri halaman ke depan menggunakan `before_id` hingga `has_more` bernilai `false`; `first_id` dari respons terakhir tersebut adalah kursor baru Anda dan Anda telah mencapai waktu sekarang. Loop lengkapnya, termasuk pengisian ulang awal (backfill) dan kondisi keamanan pada persistensi kursor, ada di [Pembacaan inkremental berbasis kursor](/docs/id/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).

</section>

<section title="Bagaimana cara mendapatkan sandbox untuk menguji Compliance API?">

  Siapkan organisasi sandbox Claude Enterprise yang tertaut ke organisasi Claude Console di bawah induk yang sama. Ini memungkinkan sandbox menguji Activity Feed (melalui kunci Admin API) maupun endpoint obrolan, file, dan proyek (melalui Compliance Access Key).

  1. **Sediakan organisasi Claude Enterprise.** Hubungi perwakilan Anthropic Anda untuk menyiapkan organisasi sandbox Claude Enterprise, atau untuk [meminta akses Compliance API](/docs/id/manage-claude/compliance-api-access#request-compliance-api-access) pada organisasi Claude Enterprise yang sudah ada.
  2. **Buat organisasi Claude Console.** Buat sendiri organisasi Claude Console di `platform.claude.com` menggunakan alamat email yang sama.
  3. **Tautkan kedua organisasi.** Masuk sebagai pemilik utama organisasi Claude Enterprise, buka [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), dan gunakan **Merge Organizations** untuk menautkan keduanya di bawah induk bersama.

  Setelah tertaut, ikuti [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access) untuk membuat kunci dan mulai melakukan kueri. Organisasi pengujian menggunakan proses pengaktifan yang sama dengan organisasi produksi.

</section>