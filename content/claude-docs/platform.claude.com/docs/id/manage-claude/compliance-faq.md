---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: c22052275a4394438a86c360078a24527d38c60d11a299fdc7961f34f4767c46
---

---
title: FAQ Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
description: Jawaban atas pertanyaan umum tentang akses Compliance API, cakupan, retensi, dan integrasi.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

## Akses dan cakupan

<AccordionGroup>
  <Accordion title="Siapa yang dapat mengaktifkan Compliance API?">
    Untuk organisasi Claude Enterprise, pemilik utama mengaktifkan Compliance API di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), dan pengaktifan tersebut diturunkan dari organisasi induk ke setiap organisasi yang tertaut. Untuk organisasi Claude Console mandiri yang memenuhi syarat (organisasi tanpa organisasi induk), admin organisasi mengaktifkannya di [Claude Console > Settings > Security](https://platform.claude.com/settings/security). Organisasi Claude Console yang tertaut ke organisasi induk tidak mengaktifkan Compliance API sendiri; pengaktifan dilakukan dari organisasi induk. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) untuk langkah-langkahnya.
  </Accordion>

  <Accordion title="Dapatkah saya menonaktifkan Compliance API setelah mengaktifkannya di Claude Console?">
    Ya. Untuk organisasi Claude Console mandiri, admin organisasi dapat menonaktifkan toggle **Compliance API** di [Claude Console > Settings > Security](https://platform.claude.com/settings/security), tempat yang sama dengan tempat mengaktifkannya. Selama Compliance API nonaktif, tidak ada peristiwa aktivitas yang direkam untuk organisasi Anda, sehingga [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) tidak menerima peristiwa baru. Jika organisasi Anda terdaftar dalam [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency), menonaktifkan Compliance API juga menghentikan pengiriman peristiwa Access Transparency. Aktivitas yang tidak direkam selama Compliance API nonaktif tidak dapat dipulihkan di kemudian hari. Mengaktifkan kembali Compliance API akan melanjutkan perekaman sejak titik tersebut; aktivitas yang sudah direkam sebelumnya tidak dihapus.
  </Accordion>

  <Accordion title="Apakah menonaktifkan Compliance API menghapus peristiwa yang sudah direkam?">
    Tidak. Menonaktifkan Compliance API menghentikan perekaman peristiwa aktivitas baru, tetapi tidak menghapus peristiwa yang sudah direkam saat Compliance API aktif. Perekaman dilanjutkan sejak titik Compliance API diaktifkan kembali.
  </Accordion>

  <Accordion title="Apakah penonaktifan Compliance API di Claude Console direkam di suatu tempat?">
    Ya. Ketika Compliance API dinonaktifkan (atau diaktifkan kembali) di Claude Console, perubahan tersebut direkam sebagai aktivitas pembaruan pengaturan organisasi di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), sehingga jejak audit Anda menunjukkan siapa yang mengubah pengaturan dan kapan. Aktivitas ini merupakan pengecualian dari penghentian perekaman: penonaktifan tetap direkam meskipun tidak ada aktivitas lain yang direkam selama Compliance API nonaktif.
  </Accordion>

  <Accordion title="Mengapa organisasi induk saya tidak muncul di Claude Console saat membuat kunci Admin API?">
    Ini memang perilaku yang diharapkan. Organisasi induk Claude Enterprise memusatkan identitas di seluruh organisasi yang tertaut; organisasi induk tidak menjalankan beban kerja, dan tidak muncul di Claude Console sama sekali. Claude Console hanya menampilkan organisasi Claude Console yang tertaut di bawah organisasi induk.

    Untuk memanggil Compliance API, Anda membuat salah satu dari dua jenis kunci berikut:

    * **Untuk akses Compliance API penuh ([Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) ditambah obrolan, file, proyek, sesi, pengguna, metadata organisasi, dan pengaturan organisasi),** pemilik utama organisasi induk (atau pemilik organisasi, untuk kunci yang dibatasi hanya pada organisasi mereka sendiri) membuat [Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) di claude.ai.
    * **Untuk akses Activity Feed saja,** admin organisasi di organisasi Claude Console Anda membuat [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) di Claude Console. Compliance API harus sudah diaktifkan untuk organisasi tersebut, dan admin harus membuat kunci Admin API saat Compliance API aktif agar kunci tersebut membawa cakupan `read:compliance_activities`.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan kunci Claude API reguler saya dengan Compliance API?">
    Tidak. Kunci Claude API (`sk-ant-api03-...`) mengautentikasi panggilan ke model Claude pada Claude API; kunci tersebut tidak mengautentikasi panggilan ke `/v1/compliance/*`. Compliance API hanya menerima Compliance Access Key (`sk-ant-api01-...`) dan kunci Admin API (`sk-ant-admin01-...`). Lihat [Kunci mana yang Anda butuhkan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk pemetaan lengkapnya.
  </Accordion>

  <Accordion title="Mengapa kunci Admin API saya mengembalikan 403 pada endpoint obrolan atau file?">
    Kunci Admin API membawa cakupan tetap `read:compliance_activities`, yang hanya mengotorisasi Activity Feed. Setiap endpoint Compliance API lainnya memerlukan cakupan yang hanya dapat dibawa oleh Compliance Access Key yang dibuat di claude.ai. Memanggil endpoint konten atau direktori dengan kunci Admin API mengembalikan 403 yang menyebutkan cakupan yang diperlukan oleh keluarga endpoint tersebut: `read:compliance_user_data` untuk obrolan, file, proyek, lampiran proyek, sesi, pengguna, dan anggota grup, serta `read:compliance_org_data` untuk organisasi, peran, grup, dan pengaturan organisasi efektif. Misalnya, mencantumkan obrolan mengembalikan respons berikut.

    ```json Response
    {
      "error": {
        "type": "permission_error",
        "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
      }
    }
    ```

    Untuk mengakses endpoint konten, pemilik utama organisasi induk Anda (atau pemilik organisasi, untuk organisasi mereka sendiri saja) harus [membuat Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_user_data` (dan `delete:compliance_user_data` untuk penghapusan), atau `read:compliance_org_data` untuk endpoint organisasi, peran, grup, dan pengaturan efektif. Lihat [Menangani kesalahan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog lengkap per endpoint.
  </Accordion>
</AccordionGroup>

## Cakupan data dan retensi

<AccordionGroup>
  <Accordion title="Seberapa jauh ke belakang Activity Feed menyimpan data?">
    Activity Feed menyimpan 6 tahun aktivitas organisasi, dan peristiwa baru dapat dikueri dalam waktu 1 menit setelah terjadi. Retensi Activity Feed tidak bergantung pada kebijakan retensi konten organisasi Anda: konten obrolan, file, dan proyek mengikuti aturan retensi yang dikonfigurasi untuk organisasi Anda (tidak terbatas secara default).
  </Accordion>

  <Accordion title="Apakah Activity Feed menyertakan konten prompt atau pesan?">
    Tidak. Activity Feed merekam siapa melakukan apa dan kapan (autentikasi, pembuatan obrolan, unggahan file, perubahan proyek, tindakan administratif, dan peristiwa sumber daya serupa), tetapi tidak merekam teks prompt atau respons model di dalam obrolan atau pesan.

    Untuk mengambil isi pesan dan konten file, gunakan endpoint obrolan, pesan, dan file dengan Compliance Access Key yang membawa `read:compliance_user_data`. Kunci dan cakupan yang sama mengambil transkrip sesi Cowork melalui [endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) dan [endpoint sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions), serta transkrip sesi Claude Code melalui endpoint sesi lokal. Endpoint ini hanya melayani konten Claude Enterprise; beban kerja Claude Console, dan beban kerja Claude API yang diautentikasi dengan kunci API, mengekspos peristiwa administratif dan sumber daya melalui Activity Feed tetapi tidak mengekspos teks prompt atau respons model melalui Compliance API.
  </Accordion>

  <Accordion title="Apakah sesi Cowork dan Claude Code muncul di Compliance API?">
    Ya. Sesi Cowork yang berjalan di mesin pengguna dalam Claude Desktop, dan sesi Claude Code di terminal, di Claude Desktop, atau di ekstensi IDE, direkam selama pengguna masuk dengan akun Claude Enterprise mereka dan tersedia melalui [endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions). Sesi Cowork yang dimulai di claude.ai web atau seluler, yang berjalan di lingkungan cloud yang dikelola Anthropic, tersedia melalui [endpoint sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions). Setiap keluarga memiliki endpoint daftar yang mengembalikan metadata sesi dan endpoint pesan yang mengembalikan transkrip sesi (prompt pengguna, respons asisten, serta panggilan dan hasil alat); keluarga lokal menambahkan endpoint yang mengambil metadata satu sesi. Semua endpoint ini menggunakan Compliance Access Key Anda yang sudah ada dengan `read:compliance_user_data`; tidak diperlukan kunci atau cakupan baru.

    Sesi lokal direkam saat permintaannya mencapai Claude API, sehingga tidak ada yang diinstal di perangkat, dan aktivitas di perangkat yang tidak pernah mencapai API tidak direkam. Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, sesi Claude Code yang dijalankan melalui platform cloud pihak ketiga (Amazon Bedrock, Google Cloud, atau Microsoft Foundry), dan Claude Code di web tidak direkam. Claude Code di web berjalan di lingkungan cloud yang dikelola Anthropic tetapi juga bukan sesi jarak jauh; endpoint sesi jarak jauh hanya mengembalikan sesi Cowork. Organisasi dengan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness) yang diaktifkan tidak mendapatkan data sesi lokal, dan sesi yang menerapkan [zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) dikecualikan.

    Endpoint sesi lokal dan jarak jauh masih dalam tahap beta.
  </Accordion>

  <Accordion title="Apa yang disertakan dalam transkrip sesi Cowork dan Claude Code?">
    Transkrip sesi lokal menunjukkan apa yang diminta kepada Claude dan apa yang dikembalikannya, bukan apa yang terjadi di perangkat.

    | Data                                 | Sesi lokal (Cowork dan Claude Code di mesin pengguna)                                                                                                                                                                                                                     | Sesi jarak jauh (Cowork di claude.ai web dan seluler)                                                                                                                              |
    | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Prompt pengguna                      | Ya; dikembalikan sebagai blok `text`.                                                                                                                                                                                                                                     | Ya; dikembalikan sebagai blok `text`.                                                                                                                                              |
    | Respons asisten                      | Ya; hanya output teks.                                                                                                                                                                                                                                                    | Ya; hanya output teks.                                                                                                                                                             |
    | Panggilan dan hasil alat             | Ya; input `tool_use` dan teks `tool_result`, dipotong hingga 10.000 byte per blok secara default (hingga sekitar 1 MiB per blok berdasarkan permintaan).                                                                                                                  | Ya; input `tool_use` dan teks `tool_result`, dipotong hingga 10.000 byte per blok secara default (hingga sekitar 1 MiB per blok berdasarkan permintaan).                           |
    | Konten file dan nama file            | Ya; teks yang dibaca Claude melalui alat muncul dalam transkrip, dengan pemotongan yang sama. Gambar, PDF, dan konten biner atau terstruktur lainnya hanya muncul sebagai blok `text` placeholder. Nama file muncul dalam input dan output panggilan alat.                | Ya; konten file dan nama file muncul dalam transkrip melalui input dan output panggilan alat (hanya teks; konten lain dihilangkan).                                                |
    | Artifacts                            | Ya; konten yang dihasilkan muncul di dalam input panggilan alat dalam transkrip.                                                                                                                                                                                          | Ya; konten yang dihasilkan muncul di dalam input panggilan alat dalam transkrip.                                                                                                   |
    | Skill                                | Ya; konten skill muncul ketika klien mengirimkannya sebagai konten pesan, dan tidak dibedakan dari teks pengguna lainnya.                                                                                                                                                 | Ya; konten skill muncul dalam transkrip.                                                                                                                                           |
    | Metadata sesi                        | Ya; pemilik (`user.id` dan alamat email), organisasi, workspace, `product_surface`, dan `created_at`, dari endpoint daftar dan ambil. Sesi lokal tidak membawa `status` atau `updated_at`.                                                                                | Ya; pemilik, organisasi, status, stempel waktu, dan `product_surface`, dari endpoint daftar.                                                                                       |
    | Blok pemikiran                       | Tidak.                                                                                                                                                                                                                                                                    | Tidak.                                                                                                                                                                             |
    | Gambar dan konten non-teks lainnya   | Tidak; setiap gambar, PDF, atau blok biner atau terstruktur lainnya muncul sebagai blok `text` placeholder (misalnya, `[image content not shown]`) dengan `truncated` disetel ke `true`. Byte file mentah tidak pernah dikembalikan.                                      | Tidak; blok non-teks dihilangkan, dan byte file mentah tidak pernah dikembalikan.                                                                                                  |
    | Penggunaan token, biaya, dan latensi | Tidak; gunakan [logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) atau [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage) untuk telemetri penggunaan dan performa. | Tidak; gunakan [logging OpenTelemetry](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) untuk telemetri penggunaan dan performa. |

    Lihat [Mengambil sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) dan [Mengambil sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions) untuk endpoint dan parameternya.
  </Accordion>

  <Accordion title="Bagaimana perbandingan cakupan sesi dengan logging OpenTelemetry (OTEL) untuk Cowork dan Claude Code?">
    [Logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage) tumpang tindih dengan endpoint sesi tetapi menjawab kebutuhan yang berbeda: OTEL mengalirkan telemetri per peristiwa ke infrastruktur yang Anda jalankan saat aktivitas terjadi, sedangkan Compliance API memungkinkan Anda mengambil transkrip per sesi yang disimpan dari Anthropic setelah kejadian.

    |                                                               | Sesi lokal Cowork dan Claude Code                                                                                                         | Sesi jarak jauh Cowork                                                                                    | Logging OpenTelemetry                                                                                                                |
    | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
    | Pengiriman                                                    | Pull: kueri dan ekspor melalui HTTPS                                                                                                      | Pull: kueri dan ekspor melalui HTTPS                                                                      | Push: dialirkan ke kolektor OTLP Anda                                                                                                |
    | Penyiapan                                                     | Berfungsi dengan Compliance Access Key Anda yang sudah ada                                                                                | Berfungsi dengan Compliance Access Key Anda yang sudah ada                                                | Admin mengonfigurasi endpoint OTLP dan pengaturan penangkapan konten                                                                 |
    | Infrastruktur                                                 | Dihosting Anthropic                                                                                                                       | Dihosting Anthropic                                                                                       | Anda menjalankan kolektor dan penyimpanan                                                                                            |
    | Retensi                                                       | 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda, jika periode terbatas ditetapkan; disimpan oleh Anthropic | 6 tahun, disimpan oleh Anthropic                                                                          | Infrastruktur Anda, kebijakan Anda                                                                                                   |
    | Prompt pengguna dan respons asisten                           | Ya                                                                                                                                        | Ya                                                                                                        | Ya, tergantung pada pengaturan penangkapan konten                                                                                    |
    | Input alat                                                    | Dipotong hingga 10.000 byte per blok secara default; hingga sekitar 1 MiB per blok berdasarkan permintaan                                 | Dipotong hingga 10.000 byte per blok secara default; hingga sekitar 1 MiB per blok berdasarkan permintaan | Ringkasan yang dipotong                                                                                                              |
    | Konten hasil alat                                             | Dipotong hingga 10.000 byte per blok secara default; hingga sekitar 1 MiB per blok berdasarkan permintaan                                 | Dipotong hingga 10.000 byte per blok secara default; hingga sekitar 1 MiB per blok berdasarkan permintaan | Metadata seperti ukuran dan keberhasilan; Claude Code juga dapat menangkap konten dengan pengaturan opsional yang dibatasi ukurannya |
    | Konten file                                                   | Ya, melalui panggilan alat transkrip (hanya teks; konten lain muncul sebagai placeholder)                                                 | Ya, melalui panggilan alat transkrip (hanya teks; konten lain dihilangkan)                                | Jalur file; Claude Code juga dapat menangkap konten dengan pengaturan opsional yang dibatasi ukurannya                               |
    | Metadata host dan perangkat (jenis terminal, jalur workspace) | Tidak                                                                                                                                     | Tidak                                                                                                     | Ya                                                                                                                                   |
    | Penggunaan token dan biaya                                    | Tidak                                                                                                                                     | Tidak                                                                                                     | Ya                                                                                                                                   |

    Peristiwa OTEL dan catatan Compliance API berbagi pengidentifikasi organisasi dan pengguna, sehingga Anda dapat menggabungkannya.
  </Accordion>

  <Accordion title="Apakah konten yang dihapus dapat dipulihkan melalui Compliance API?">
    Tidak. Penghapusan yang dilakukan melalui Compliance API bersifat langsung, permanen, dan tidak dapat dipulihkan. Obrolan yang dihapus pengguna melalui claude.ai dihapus secara lunak (soft-deleted): obrolan tersebut tetap terlihat melalui Compliance API dengan `deleted_at` terisi hingga jendela retensi organisasi Anda berakhir atau Anda menghapusnya secara permanen melalui API ini. Ambil konten apa pun yang perlu Anda simpan (untuk penahanan hukum atau pengarsipan) sebelum mengirimkan permintaan `DELETE`.
  </Accordion>

  <Accordion title="Apa yang tidak direkam oleh Compliance API?">
    Compliance API memiliki batasan cakupan yang diketahui: Activity Feed merekam peristiwa sumber daya tetapi bukan teks prompt atau respons, beban kerja Claude Console dan Claude API yang diautentikasi dengan kunci API tidak mengekspos konten pesan sama sekali, dan konten yang dihapus oleh kebijakan retensi Anda atau oleh penghapusan permanen tidak dapat dipulihkan. Untuk batasan cakupan lengkap dan kontrak pengiriman, lihat [Jaminan pengiriman dan kelengkapan](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).

    Transkrip sesi Cowork dan Claude Code memiliki batasan tersendiri. Sesi lokal hanya direkam saat permintaannya mencapai Claude API, sehingga aktivitas di perangkat yang tidak pernah mencapai API tidak direkam. Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, sesi Claude Code yang dijalankan melalui platform cloud pihak ketiga (Amazon Bedrock, Google Cloud, atau Microsoft Foundry), dan Claude Code di web juga tidak direkam; organisasi dengan kesiapan HIPAA yang diaktifkan tidak mendapatkan data sesi lokal; dan sesi yang menerapkan zero data retention dikecualikan. Tidak ada transkrip sesi, baik lokal maupun jarak jauh, yang menyertakan blok pemikiran atau definisi alat. Organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek) melihat metadata sesi lokal tetapi tidak melihat konten transkrip.
  </Accordion>
</AccordionGroup>

## Integrasi dan paginasi

<AccordionGroup>
  <Accordion title="Bagaimana cara mengorelasikan catatan Compliance API dengan SIEM saya?">
    Gabungkan catatan `Activity` ke SIEM Anda berdasarkan `actor.user_id`, `actor.email_address`, `actor.ip_address`, dan `created_at`. Lihat [Merancang integrasi kepatuhan Anda](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem) untuk tabel kunci gabungan dan pola konsumsi.
  </Accordion>

  <Accordion title="Dapatkah satu pelanggan memiliki beberapa organisasi di bawah satu induk?">
    Ya. Organisasi induk Claude Enterprise dapat memiliki banyak organisasi tertaut, termasuk campuran organisasi claude.ai dan organisasi Claude Console (misalnya, organisasi Claude Console produksi dan staging yang terpisah). Identitas, SSO, dan SCIM dibagikan di seluruh induk; penagihan, anggota, proyek, dan kunci API tetap terpisah untuk setiap organisasi. Pengaktifan Compliance API terjadi di tingkat organisasi induk dan diturunkan ke semua organisasi tertaut, dan Compliance Access Key yang mencakup organisasi induk dan membawa `read:compliance_org_data` dapat mengenumerasi setiap organisasi di bawah induk melalui `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Apakah aktivitas dikembalikan secara berurutan, dan bagaimana cara mendeteksi bahwa saya telah mengejar waktu nyata?">
    Aktivitas dikembalikan dari yang terbaru terlebih dahulu, dengan nilai `created_at` yang sama diurutkan berdasarkan ID aktivitas. Untuk mengejar ketertinggalan, telusuri halaman ke depan berdasarkan `before_id` hingga `has_more` bernilai `false`; `first_id` dari respons terakhir tersebut adalah kursor baru Anda dan Anda telah mencapai waktu sekarang. Loop lengkap, termasuk pengisian ulang awal dan kondisi keamanan pada persistensi kursor, ada di [Pembacaan inkremental berbasis kursor](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="Bagaimana cara mendapatkan sandbox untuk menguji Compliance API?">
    Untuk menguji hanya [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), Anda tidak memerlukan organisasi Claude Enterprise: admin organisasi dapat [mengaktifkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) pada organisasi uji Claude Console mandiri yang memenuhi syarat dan mengkueri feed dengan kunci Admin API baru. Jika bagian **Compliance API** tidak terlihat di pengaturan Security organisasi tersebut, organisasi tersebut tidak memenuhi syarat untuk pengaktifan mandiri.

    Untuk menguji setiap endpoint, siapkan organisasi sandbox Claude Enterprise yang tertaut ke organisasi Claude Console di bawah induk yang sama. Ini memungkinkan sandbox menguji Activity Feed (melalui kunci Admin API) dan endpoint obrolan, file, proyek, serta sesi (melalui Compliance Access Key).

    1. **Sediakan organisasi Claude Enterprise.** Hubungi perwakilan Anthropic Anda untuk menyiapkan organisasi sandbox Claude Enterprise. Pada organisasi Claude Enterprise yang sudah ada, pemilik utama dapat [mengaktifkan Compliance API langsung di claude.ai](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Buat organisasi Claude Console.** Buat sendiri organisasi Claude Console di `platform.claude.com` menggunakan alamat email yang sama.
    3. **Tautkan kedua organisasi.** Masuk sebagai pemilik utama organisasi Claude Enterprise, buka [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), dan gunakan **Merge Organizations** untuk menautkan keduanya di bawah induk bersama.

    Setelah tertaut, ikuti [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk membuat kunci dan mulai mengkueri. Organisasi uji menggunakan proses pengaktifan yang sama dengan organisasi produksi.
  </Accordion>
</AccordionGroup>
