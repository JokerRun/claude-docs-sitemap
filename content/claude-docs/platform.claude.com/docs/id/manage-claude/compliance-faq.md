---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 1db39634d27f7586f7df6c23d3d144de20877cdeb70c9a8e129248f6bd10babb
---

# FAQ Compliance API

Jawaban atas pertanyaan umum tentang akses, cakupan, retensi, dan integrasi Compliance API.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

## Akses dan cakupan

<AccordionGroup>
  <Accordion title="Mengapa organisasi induk saya tidak muncul di Claude Console saat membuat kunci Admin API?">
    Ini memang diharapkan. Organisasi induk Claude Enterprise memusatkan identitas di seluruh organisasi yang tertaut; organisasi induk tidak membawa beban kerja, dan tidak muncul sama sekali di Claude Console. Claude Console hanya menampilkan organisasi Claude Console yang tertaut di bawah organisasi induk.

    Untuk memanggil Compliance API, Anda membuat salah satu dari dua jenis kunci berikut:

    * **Untuk akses penuh Compliance API ([Activity Feed](/docs/id/manage-claude/compliance-activity-feed) ditambah chat, file, proyek, pengguna, metadata organisasi, dan pengaturan organisasi),** pemilik utama organisasi induk (atau pemilik organisasi, untuk kunci yang dibatasi hanya pada organisasinya sendiri) membuat [Compliance Access Key](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) di claude.ai.
    * **Untuk akses Activity Feed saja,** admin organisasi di organisasi Claude Console Anda membuat [kunci Admin API](/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) di Claude Console. Compliance API harus sudah diaktifkan untuk organisasi tersebut, dan admin harus membuat kunci Admin API setelah pengaktifan agar kunci tersebut membawa cakupan `read:compliance_activities`.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan kunci Claude API biasa saya dengan Compliance API?">
    Tidak. Kunci Claude API (`sk-ant-api03-...`) mengautentikasi panggilan ke model Claude pada Claude API; kunci tersebut tidak mengautentikasi panggilan ke `/v1/compliance/*`. Compliance API hanya menerima Compliance Access Key (`sk-ant-api01-...`) dan kunci Admin API (`sk-ant-admin01-...`). Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk pemetaan lengkapnya.
  </Accordion>

  <Accordion title="Mengapa kunci Admin API saya mengembalikan 403 pada endpoint chat atau file?">
    Kunci Admin API membawa cakupan tetap `read:compliance_activities`, yang hanya mengotorisasi Activity Feed. Setiap endpoint Compliance API lainnya memerlukan cakupan yang hanya dapat dibawa oleh Compliance Access Key yang dibuat di claude.ai. Memanggil endpoint konten atau direktori dengan kunci Admin API mengembalikan 403 yang menyebutkan cakupan yang diperlukan oleh keluarga endpoint tersebut: `read:compliance_user_data` untuk chat, file, proyek, lampiran proyek, pengguna, dan anggota grup, serta `read:compliance_org_data` untuk organisasi, peran, grup, dan pengaturan organisasi efektif. Misalnya, menampilkan daftar chat mengembalikan respons berikut.

    ```json Response
    {
      "error": {
        "type": "permission_error",
        "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
      }
    }
    ```

    Untuk mengakses endpoint konten, pemilik utama organisasi induk Anda (atau pemilik organisasi, hanya untuk organisasinya sendiri) harus [membuat Compliance Access Key](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_user_data` (dan `delete:compliance_user_data` untuk penghapusan), atau `read:compliance_org_data` untuk endpoint organisasi, peran, grup, dan pengaturan efektif. Lihat [Menangani kesalahan Compliance API](/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog lengkap per endpoint.
  </Accordion>
</AccordionGroup>

## Cakupan data dan retensi

<AccordionGroup>
  <Accordion title="Seberapa jauh ke belakang Activity Feed menyimpan data?">
    Activity Feed menyimpan 6 tahun aktivitas organisasi, dan peristiwa baru dapat dikueri dalam waktu 1 menit setelah terjadi. Retensi Activity Feed tidak bergantung pada kebijakan retensi konten organisasi Anda: konten chat, file, dan proyek mengikuti aturan retensi yang dikonfigurasi untuk organisasi Anda (tanpa batas waktu secara default).
  </Accordion>

  <Accordion title="Apakah Activity Feed menyertakan konten prompt atau pesan?">
    Tidak. Activity Feed mencatat siapa melakukan apa dan kapan (autentikasi, pembuatan chat, unggahan file, perubahan proyek, tindakan administratif, dan peristiwa sumber daya serupa), tetapi tidak menangkap teks prompt atau respons model di dalam chat atau pesan.

    Untuk mengambil isi pesan dan konten file, gunakan endpoint chat, pesan, dan file dengan Compliance Access Key yang membawa `read:compliance_user_data`. Endpoint tersebut hanya menyajikan konten claude.ai; beban kerja Claude Console dan Claude API mengekspos peristiwa administratif dan sumber daya melalui Activity Feed tetapi tidak mengekspos teks prompt atau respons model melalui Compliance API.
  </Accordion>

  <Accordion title="Apakah konten yang dihapus dapat dipulihkan melalui Compliance API?">
    Tidak. Penghapusan yang dilakukan melalui Compliance API bersifat langsung, permanen, dan tidak dapat dipulihkan. Chat yang dihapus pengguna melalui claude.ai dihapus secara lunak (soft-deleted): chat tersebut tetap terlihat melalui Compliance API dengan `deleted_at` terisi hingga jendela retensi organisasi Anda berakhir atau Anda menghapusnya secara permanen melalui API ini. Tarik konten apa pun yang perlu Anda simpan (untuk penahanan hukum atau pengarsipan) sebelum mengeluarkan permintaan `DELETE`.
  </Accordion>

  <Accordion title="Apa yang tidak ditangkap oleh Compliance API?">
    Compliance API memiliki batasan cakupan yang diketahui: Activity Feed mencatat peristiwa sumber daya tetapi tidak mencatat teks prompt atau respons, beban kerja Claude Console dan Claude API sama sekali tidak mengekspos konten pesan, dan konten yang dihapus oleh kebijakan retensi Anda atau oleh penghapusan permanen tidak dapat dipulihkan. Untuk batasan cakupan lengkap dan kontrak pengiriman, lihat [Jaminan pengiriman dan kelengkapan](/docs/id/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).
  </Accordion>
</AccordionGroup>

## Integrasi dan paginasi

<AccordionGroup>
  <Accordion title="Bagaimana cara mengorelasikan catatan Compliance API dengan SIEM saya?">
    Gabungkan catatan `Activity` ke SIEM Anda pada `actor.user_id`, `actor.email_address`, `actor.ip_address`, dan `created_at`. Lihat [Merancang integrasi kepatuhan Anda](/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem) untuk tabel kunci penggabungan dan pola konsumsi.
  </Accordion>

  <Accordion title="Dapatkah satu pelanggan memiliki beberapa organisasi di bawah satu induk?">
    Ya. Organisasi induk Claude Enterprise dapat memiliki banyak organisasi tertaut, termasuk campuran organisasi claude.ai dan organisasi Claude Console (misalnya, organisasi Claude Console produksi dan staging yang terpisah). Identitas, SSO, dan SCIM dibagikan di seluruh organisasi induk; penagihan, anggota, proyek, dan kunci API tetap terpisah untuk setiap organisasi. Pengaktifan Compliance API terjadi di tingkat organisasi induk dan berlaku ke semua organisasi tertaut, dan Compliance Access Key yang mencakup organisasi induk serta membawa `read:compliance_org_data` dapat menampilkan setiap organisasi di bawah induk melalui `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Apakah aktivitas dikembalikan secara berurutan, dan bagaimana cara mendeteksi ketika saya telah mencapai waktu nyata?">
    Aktivitas dikembalikan dari yang terbaru terlebih dahulu, dengan kesamaan pada `created_at` dipecahkan berdasarkan ID aktivitas. Untuk mengejar ketertinggalan, telusuri halaman ke depan dengan `before_id` hingga `has_more` bernilai `false`; `first_id` dari respons terakhir tersebut adalah kursor baru Anda dan Anda telah mencapai saat ini. Loop lengkapnya, termasuk backfill awal dan kondisi keamanan pada persistensi kursor, ada di [Pembacaan inkremental berbasis kursor](/docs/id/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="Bagaimana cara mendapatkan sandbox untuk menguji Compliance API?">
    Siapkan organisasi sandbox Claude Enterprise yang tertaut ke organisasi Claude Console di bawah induk yang sama. Ini memungkinkan sandbox menguji baik Activity Feed (melalui kunci Admin API) maupun endpoint chat, file, dan proyek (melalui Compliance Access Key).

    1. **Sediakan organisasi Claude Enterprise.** Hubungi perwakilan Anthropic Anda untuk menyiapkan organisasi sandbox Claude Enterprise. Pada organisasi Claude Enterprise yang sudah ada, pemilik utama dapat [mengaktifkan Compliance API langsung di claude.ai](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Buat organisasi Claude Console.** Buat sendiri organisasi Claude Console di `platform.claude.com` menggunakan alamat email yang sama.
    3. **Tautkan kedua organisasi.** Masuk sebagai pemilik utama organisasi Claude Enterprise, buka [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), dan gunakan **Merge Organizations** untuk menautkan keduanya di bawah induk bersama.

    Setelah tertaut, ikuti [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access) untuk membuat kunci dan mulai melakukan kueri. Organisasi pengujian menggunakan proses pengaktifan yang sama dengan organisasi produksi.
  </Accordion>
</AccordionGroup>
