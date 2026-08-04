---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
fetched_at: 2026-08-04T03:08:17.915636Z
sha256: 438ceb162987c482a9bc76a98d940252ce84d56ab331fc698a1e431212e843c9
---

# FAQ Compliance API

Jawaban atas pertanyaan umum tentang akses, cakupan, retensi, dan integrasi Compliance API.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

## Akses dan cakupan

<AccordionGroup>
  <Accordion title="Mengapa organisasi induk saya tidak muncul di Claude Console saat membuat Admin API key?">
    Ini memang diharapkan. Organisasi induk Claude Enterprise memusatkan identitas di semua organisasi yang tertaut; organisasi induk tidak membawa beban kerja, dan tidak muncul di Claude Console sama sekali. Claude Console hanya menampilkan organisasi Claude Console yang tertaut di bawah organisasi induk.

    Untuk memanggil Compliance API, Anda membuat salah satu dari dua jenis kunci berikut:

    * **Untuk akses Compliance API penuh ([Activity Feed](/docs/id/manage-claude/compliance-activity-feed) ditambah chat, file, proyek, sesi remote Cowork, pengguna, metadata organisasi, dan pengaturan organisasi),** pemilik utama organisasi induk (atau pemilik organisasi, untuk kunci yang dibatasi hanya pada organisasinya sendiri) membuat [Compliance Access Key](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) di claude.ai.
    * **Untuk akses Activity Feed saja,** admin organisasi di organisasi Claude Console Anda membuat [Admin API key](/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) di Claude Console. Compliance API harus sudah diaktifkan untuk organisasi tersebut, dan admin harus membuat Admin API key setelah pengaktifan agar kunci tersebut membawa cakupan `read:compliance_activities`.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan kunci Claude API reguler saya dengan Compliance API?">
    Tidak. Kunci Claude API (`sk-ant-api03-...`) mengautentikasi panggilan ke model Claude pada Claude API; kunci tersebut tidak mengautentikasi panggilan ke `/v1/compliance/*`. Compliance API hanya menerima Compliance Access Key (`sk-ant-api01-...`) dan Admin API key (`sk-ant-admin01-...`). Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk pemetaan lengkapnya.
  </Accordion>

  <Accordion title="Mengapa Admin API key saya mengembalikan 403 pada endpoint chat atau file?">
    Admin API key membawa cakupan tetap `read:compliance_activities`, yang hanya mengotorisasi Activity Feed. Setiap endpoint Compliance API lainnya memerlukan cakupan yang hanya dapat dibawa oleh Compliance Access Key yang dibuat di claude.ai. Memanggil endpoint konten atau direktori dengan Admin API key mengembalikan 403 yang menyebutkan cakupan yang diperlukan oleh keluarga endpoint tersebut: `read:compliance_user_data` untuk chat, file, proyek, lampiran proyek, sesi remote, pengguna, dan anggota grup, serta `read:compliance_org_data` untuk organisasi, peran, grup, dan pengaturan organisasi efektif. Misalnya, menampilkan daftar chat mengembalikan respons berikut.

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

    Untuk mengambil isi pesan dan konten file, gunakan endpoint chat, pesan, dan file dengan Compliance Access Key yang membawa `read:compliance_user_data`; kunci dan cakupan yang sama mengambil transkrip sesi Cowork melalui [endpoint sesi remote](/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions). Endpoint tersebut hanya melayani konten claude.ai; beban kerja Claude Console dan Claude API mengekspos peristiwa administratif dan sumber daya melalui Activity Feed tetapi tidak mengekspos teks prompt atau respons model melalui Compliance API.
  </Accordion>

  <Accordion title="Apakah sesi Cowork muncul di Compliance API?">
    Ya. Sesi Cowork yang dimulai di claude.ai web atau seluler tersedia melalui endpoint sesi remote: `GET /v1/compliance/apps/sessions/remote` menampilkan daftar metadata sesi, dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip sesi (prompt pengguna, respons asisten, serta panggilan alat dan hasilnya). Kedua endpoint menggunakan Compliance Access Key Anda yang sudah ada dengan `read:compliance_user_data`; tidak diperlukan kunci atau cakupan baru. Lihat [Mengambil sesi remote](/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions).

    Endpoint sesi remote masih dalam tahap beta dan tidak memerlukan pengaktifan tambahan.
  </Accordion>

  <Accordion title="Apa saja yang disertakan dalam transkrip sesi remote untuk Cowork?">
    | Data                                 | Disertakan | Catatan                                                                                                                                                                       |
    | ------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Prompt pengguna                      | Ya         | Dikembalikan sebagai blok `text`.                                                                                                                                             |
    | Respons asisten                      | Ya         | Hanya output teks.                                                                                                                                                            |
    | Panggilan alat dan hasilnya          | Ya         | Input `tool_use` dan teks `tool_result`, dipotong hingga 10.000 byte per blok secara default (hingga sekitar 1 MiB per blok berdasarkan permintaan).                          |
    | Konten file dan nama file            | Ya         | Muncul dalam transkrip melalui input dan output panggilan alat.                                                                                                               |
    | Artifacts                            | Ya         | Konten yang dihasilkan muncul di dalam input panggilan alat dalam transkrip.                                                                                                  |
    | Skills                               | Ya         | Konten skill muncul dalam transkrip.                                                                                                                                          |
    | Metadata sesi                        | Ya         | Pemilik, status, stempel waktu, dan `product_surface`, dari endpoint daftar.                                                                                                  |
    | Gambar dan konten non-teks lainnya   | Tidak      | Blok non-teks dihilangkan; byte file mentah tidak pernah dikembalikan.                                                                                                        |
    | Penggunaan token, biaya, dan latensi | Tidak      | Gunakan [pencatatan OpenTelemetry](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) untuk telemetri penggunaan dan kinerja. |

    Lihat [Mengambil sesi remote](/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions) untuk endpoint dan parameternya.
  </Accordion>

  <Accordion title="Bagaimana perbandingan cakupan sesi remote dengan pencatatan OpenTelemetry (OTEL) untuk Cowork?">
    [Pencatatan OpenTelemetry (OTEL) Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan endpoint sesi remote saling tumpang tindih tetapi menjawab kebutuhan yang berbeda: OTEL mengalirkan peristiwa ke infrastruktur yang Anda jalankan, sedangkan Compliance API memungkinkan Anda mengambil transkrip lengkap dari Anthropic setelah kejadian.

    |                                                       | Sesi remote Compliance API                                          | Pencatatan OpenTelemetry                                             |
    | ----------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
    | Pengiriman                                            | Pull: kueri dan ekspor melalui HTTPS                                | Push: dialirkan ke kolektor OTLP Anda                                |
    | Penyiapan                                             | Sederhana; bekerja dengan Compliance Access Key Anda yang sudah ada | Admin mengonfigurasi endpoint OTLP dan pengaturan penangkapan konten |
    | Infrastruktur                                         | Dihosting oleh Anthropic                                            | Anda menjalankan kolektor dan penyimpanan                            |
    | Retensi                                               | 6 tahun, disimpan oleh Anthropic                                    | Infrastruktur Anda, kebijakan Anda                                   |
    | Prompt pengguna dan respons asisten                   | Ya                                                                  | Ya, saat penangkapan konten diaktifkan                               |
    | Input alat                                            | Lengkap, hingga sekitar 1 MiB per blok berdasarkan permintaan       | Ringkasan yang dipotong                                              |
    | Konten hasil alat                                     | Ya                                                                  | Tidak; hanya metadata, seperti ukuran dan keberhasilan               |
    | Konten file                                           | Ya, melalui panggilan alat dalam transkrip                          | Tidak; hanya jalur file                                              |
    | Metadata mesin host (jenis terminal, jalur workspace) | Tidak                                                               | Ya                                                                   |

    Keduanya berbagi pengidentifikasi organisasi dan pengguna, sehingga Anda dapat menggabungkan peristiwa OTEL dengan catatan Compliance API.
  </Accordion>

  <Accordion title="Apakah konten yang dihapus dapat dipulihkan melalui Compliance API?">
    Tidak. Penghapusan yang dilakukan melalui Compliance API bersifat langsung, permanen, dan tidak dapat dipulihkan. Chat yang dihapus pengguna melalui claude.ai dihapus secara lunak (soft-delete): chat tersebut tetap terlihat melalui Compliance API dengan `deleted_at` terisi hingga jendela retensi organisasi Anda berakhir atau Anda menghapusnya secara permanen melalui API ini. Ambil konten apa pun yang perlu Anda simpan (untuk penahanan hukum atau pengarsipan) sebelum mengeluarkan permintaan `DELETE`.
  </Accordion>

  <Accordion title="Apa yang tidak ditangkap oleh Compliance API?">
    Compliance API memiliki batasan cakupan yang diketahui: Activity Feed mencatat peristiwa sumber daya tetapi bukan teks prompt atau respons, beban kerja Claude Console dan Claude API sama sekali tidak mengekspos konten pesan, dan konten yang dihapus oleh kebijakan retensi Anda atau oleh penghapusan permanen tidak dapat dipulihkan. Untuk batasan cakupan lengkap dan kontrak pengiriman, lihat [Jaminan pengiriman dan kelengkapan](/docs/id/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).
  </Accordion>
</AccordionGroup>

## Integrasi dan paginasi

<AccordionGroup>
  <Accordion title="Bagaimana cara mengorelasikan catatan Compliance API dengan SIEM saya?">
    Gabungkan catatan `Activity` ke SIEM Anda pada `actor.user_id`, `actor.email_address`, `actor.ip_address`, dan `created_at`. Lihat [Merancang integrasi kepatuhan Anda](/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem) untuk tabel kunci penggabungan dan pola konsumsi.
  </Accordion>

  <Accordion title="Dapatkah satu pelanggan memiliki beberapa organisasi di bawah satu induk?">
    Ya. Organisasi induk Claude Enterprise dapat memiliki banyak organisasi tertaut, termasuk campuran organisasi claude.ai dan organisasi Claude Console (misalnya, organisasi Claude Console produksi dan staging yang terpisah). Identitas, SSO, dan SCIM dibagikan di seluruh induk; penagihan, anggota, proyek, dan kunci API tetap terpisah untuk setiap organisasi. Pengaktifan Compliance API terjadi di tingkat organisasi induk dan berlaku ke semua organisasi tertaut, dan Compliance Access Key yang mencakup organisasi induk dan membawa `read:compliance_org_data` dapat menampilkan setiap organisasi di bawah induk melalui `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Apakah aktivitas dikembalikan secara berurutan, dan bagaimana cara mendeteksi ketika saya telah mencapai waktu nyata?">
    Aktivitas dikembalikan dari yang terbaru terlebih dahulu, dengan kesamaan pada `created_at` dipecahkan berdasarkan ID aktivitas. Untuk mengejar ketertinggalan, telusuri halaman ke depan dengan `before_id` hingga `has_more` bernilai `false`; `first_id` dari respons terakhir tersebut adalah kursor baru Anda dan Anda telah mencapai waktu saat ini. Loop lengkapnya, termasuk backfill awal dan kondisi keamanan pada persistensi kursor, ada di [Pembacaan inkremental berbasis kursor](/docs/id/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="Bagaimana cara mendapatkan sandbox untuk menguji Compliance API?">
    Siapkan organisasi sandbox Claude Enterprise yang tertaut ke organisasi Claude Console di bawah induk yang sama. Ini memungkinkan sandbox menguji baik Activity Feed (melalui Admin API key) maupun endpoint chat, file, proyek, dan sesi (melalui Compliance Access Key).

    1. **Sediakan organisasi Claude Enterprise.** Hubungi perwakilan Anthropic Anda untuk menyiapkan organisasi sandbox Claude Enterprise. Pada organisasi Claude Enterprise yang sudah ada, pemilik utama dapat [mengaktifkan Compliance API langsung di claude.ai](/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Buat organisasi Claude Console.** Buat sendiri organisasi Claude Console di `platform.claude.com` menggunakan alamat email yang sama.
    3. **Tautkan kedua organisasi.** Masuk sebagai pemilik utama organisasi Claude Enterprise, buka [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), dan gunakan **Merge Organizations** untuk menautkan keduanya di bawah induk bersama.

    Setelah tertaut, ikuti [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access) untuk membuat kunci dan mulai melakukan kueri. Organisasi pengujian menggunakan proses pengaktifan yang sama dengan organisasi produksi.
  </Accordion>
</AccordionGroup>
