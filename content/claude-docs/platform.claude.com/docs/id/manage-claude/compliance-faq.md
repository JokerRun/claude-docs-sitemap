---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 85c2bbacc24287d25f850692c41d5878dd3a2238aae417067c393300dc6b2e15
---

---
title: FAQ Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-faq
description: Jawaban atas pertanyaan umum tentang akses, cakupan (scope), retensi, dan integrasi Compliance API.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

## Akses dan scope

<AccordionGroup>
  <Accordion title="Siapa yang dapat mengaktifkan Compliance API?">
    Untuk organisasi Claude Enterprise, pemilik utama (primary owner) mengaktifkan Compliance API di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), dan pengaktifan tersebut diteruskan dari organisasi induk ke setiap organisasi yang tertaut. Untuk organisasi Claude Console mandiri yang memenuhi syarat (organisasi tanpa organisasi induk), admin organisasi mengaktifkannya di [Claude Console > Settings > Security](https://platform.claude.com/settings/security). Organisasi Claude Console yang tertaut ke organisasi induk tidak mengaktifkan Compliance API sendiri; Compliance API diaktifkan dari organisasi induk. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) untuk langkah-langkahnya.
  </Accordion>

  <Accordion title="Dapatkah saya menonaktifkan Compliance API setelah mengaktifkannya di Claude Console?">
    Ya. Untuk organisasi Claude Console mandiri, admin organisasi dapat menonaktifkan toggle **Compliance API** di [Claude Console > Settings > Security](https://platform.claude.com/settings/security), tempat yang sama untuk mengaktifkannya. Selama Compliance API nonaktif, tidak ada peristiwa aktivitas yang direkam untuk organisasi Anda, sehingga [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) tidak menerima peristiwa baru. Jika organisasi Anda terdaftar dalam [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency), menonaktifkan Compliance API juga menghentikan pengiriman peristiwa Access Transparency. Aktivitas yang tidak direkam selama Compliance API nonaktif tidak dapat dipulihkan kemudian. Mengaktifkan kembali Compliance API akan melanjutkan perekaman sejak saat itu; aktivitas yang sudah direkam tidak dihapus.
  </Accordion>

  <Accordion title="Apakah menonaktifkan Compliance API menghapus peristiwa yang sudah direkam?">
    Tidak. Menonaktifkan Compliance API menghentikan perekaman peristiwa aktivitas baru, tetapi tidak menghapus peristiwa yang sudah direkam saat Compliance API aktif. Perekaman dilanjutkan sejak Compliance API diaktifkan kembali.
  </Accordion>

  <Accordion title="Apakah penonaktifan Compliance API di Claude Console direkam di suatu tempat?">
    Ya. Ketika Compliance API dinonaktifkan (atau diaktifkan kembali) di Claude Console, perubahan tersebut direkam sebagai aktivitas `org_compliance_api_settings_updated` di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), sehingga jejak audit Anda menunjukkan siapa yang mengubah pengaturan dan kapan. Aktivitas ini merupakan pengecualian dari penghentian perekaman: penonaktifan tetap direkam meskipun tidak ada aktivitas lain yang direkam selama Compliance API nonaktif.
  </Accordion>

  <Accordion title="Mengapa organisasi induk saya tidak muncul di Claude Console saat membuat Admin API key?">
    Ini memang sudah seharusnya. Organisasi induk Claude Enterprise memusatkan identitas di seluruh organisasi yang tertaut; organisasi induk tidak menjalankan beban kerja, dan sama sekali tidak muncul di Claude Console. Claude Console hanya menampilkan organisasi Claude Console yang tertaut di bawah organisasi induk.

    Untuk memanggil Compliance API, Anda membuat salah satu dari dua jenis kunci berikut:

    * **Untuk akses penuh Compliance API ([Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) ditambah chat, file, proyek, sesi, pengguna, metadata organisasi, dan pengaturan organisasi),** pemilik utama organisasi induk (atau pemilik organisasi, untuk kunci yang dibatasi hanya pada organisasinya sendiri) membuat [Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) di claude.ai.
    * **Untuk akses Activity Feed saja,** admin organisasi di organisasi Claude Console Anda membuat [Admin API key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#create-an-admin-api-key) di Claude Console. Compliance API harus sudah diaktifkan untuk organisasi tersebut, dan admin harus membuat Admin API key saat Compliance API aktif agar kunci tersebut membawa scope `read:compliance_activities`.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan kunci API Claude biasa dengan Compliance API?">
    Tidak. "API key" (kunci API) Claude (`sk-ant-api03-...`) mengautentikasi panggilan ke model Claude di Claude API; kunci tersebut tidak mengautentikasi panggilan ke `/v1/compliance/*`. Compliance API hanya menerima Compliance Access Key (`sk-ant-api01-...`) dan Admin API key (`sk-ant-admin01-...`). Lihat [Kunci mana yang Anda perlukan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk pemetaan lengkapnya.
  </Accordion>

  <Accordion title="Mengapa Admin API key saya mengembalikan 403 pada endpoint chat atau file?">
    Admin API key membawa scope tetap `read:compliance_activities`, yang hanya mengotorisasi Activity Feed. Setiap endpoint Compliance API lainnya memerlukan scope yang hanya dapat dibawa oleh Compliance Access Key yang dibuat di claude.ai. Memanggil endpoint konten atau direktori dengan Admin API key mengembalikan 403 yang menyebutkan scope yang diperlukan oleh kelompok endpoint tersebut: `read:compliance_user_data` untuk chat, file, proyek, lampiran proyek, sesi, pengguna, dan anggota grup, serta `read:compliance_org_data` untuk organisasi, peran, grup, dan pengaturan organisasi efektif. Misalnya, mencantumkan daftar chat mengembalikan respons berikut.

    ```json Response
    {
      "error": {
        "type": "permission_error",
        "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
      }
    }
    ```

    Untuk mengakses endpoint konten, pemilik utama organisasi induk Anda (atau pemilik organisasi, hanya untuk organisasinya sendiri) harus [membuat Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_user_data` (dan `delete:compliance_user_data` untuk penghapusan), atau `read:compliance_org_data` untuk endpoint organisasi, peran, grup, dan pengaturan efektif. Organisasi Claude Console mandiri (organisasi tanpa organisasi induk) tidak dapat membuat Compliance Access Key, sehingga endpoint konten tidak tersedia baginya; organisasi tersebut hanya dapat mengkueri Activity Feed. Lihat [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden) untuk katalog lengkap per endpoint.
  </Accordion>
</AccordionGroup>

## Cakupan data dan retensi

<AccordionGroup>
  <Accordion title="Seberapa jauh ke belakang jangkauan Activity Feed?">
    Activity Feed menyimpan 6 tahun aktivitas organisasi, dan peristiwa baru dapat dikueri dalam 1 menit setelah terjadi. Feed ini paling jauh menjangkau hingga saat Compliance API pertama kali diaktifkan untuk organisasi Anda: perekaman tidak bersifat retroaktif, dan aktivitas sebelum pengaktifan tidak diisi ulang (backfill). Retensi Activity Feed tidak bergantung pada kebijakan retensi konten organisasi Anda: konten chat, file, dan proyek mengikuti aturan retensi yang dikonfigurasi untuk organisasi Anda (tanpa batas waktu secara default), kecuali pengguna menghapusnya lebih awal.
  </Accordion>

  <Accordion title="Apakah Activity Feed menyertakan konten prompt atau pesan?">
    Tidak. Activity Feed merekam siapa melakukan apa dan kapan (autentikasi, pembuatan chat, unggahan file, perubahan proyek, tindakan administratif, dan peristiwa sumber daya serupa), tetapi tidak merekam teks prompt atau respons model di dalam chat atau pesan.

    Untuk mengambil isi pesan dan konten file, gunakan endpoint chat, pesan, dan file dengan Compliance Access Key yang membawa `read:compliance_user_data`. Kunci dan scope yang sama mengambil transkrip sesi di mesin pengguna (seperti sesi Cowork dan Claude Code) melalui [endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions), dan transkrip sesi Cowork di cloud melalui [endpoint sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions). Endpoint ini hanya melayani konten Claude Enterprise; beban kerja Claude Console, dan beban kerja Claude API yang diautentikasi dengan kunci API, mengekspos peristiwa administratif dan sumber daya melalui Activity Feed tetapi tidak mengekspos teks prompt atau respons model melalui Compliance API.
  </Accordion>

  <Accordion title="Apakah sesi Cowork, Claude Code, Claude Science, dan Claude for Microsoft 365 muncul di Compliance API?">
    Ya. Sesi Cowork di Claude Desktop yang berjalan di mesin pengguna, sesi Claude Code (di terminal, di Claude Desktop, atau di ekstensi IDE), sesi di aplikasi desktop Claude Science, dan sesi Claude for Microsoft 365 di Excel, PowerPoint, Word, dan Outlook direkam selama pengguna masuk dengan akun Claude Enterprise mereka dan tersedia melalui [endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Sesi Cowork yang dimulai di claude.ai web atau seluler, yang berjalan di cloud dalam lingkungan yang dikelola Anthropic, tersedia melalui [endpoint sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions). Setiap kelompok memiliki endpoint daftar yang mengembalikan metadata sesi dan endpoint pesan yang mengembalikan transkrip sesi (prompt pengguna, respons asisten, serta pemanggilan alat dan hasilnya). Kelompok lokal menambahkan endpoint ketiga yang mengambil metadata satu sesi. Semua endpoint ini menggunakan Compliance Access Key Anda yang sudah ada dengan `read:compliance_user_data`; tidak diperlukan kunci atau scope baru.

    Sesi lokal direkam saat permintaannya mencapai Claude API, sehingga tidak ada yang diinstal di perangkat, dan aktivitas di perangkat yang tidak pernah mencapai API tidak direkam. Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, sesi Claude Code yang dijalankan melalui platform cloud pihak ketiga (Amazon Bedrock, Google Cloud, atau Microsoft Foundry), dan Claude Code di web tidak direkam. Claude Code di web juga berjalan di cloud dalam lingkungan yang dikelola Anthropic, tetapi bukan merupakan sesi jarak jauh; endpoint sesi jarak jauh hanya mengembalikan sesi Cowork. Organisasi dengan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness) yang diaktifkan tidak mendapatkan data sesi lokal, dan sesi yang menerapkan [zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) dikecualikan.

    Endpoint sesi lokal dan jarak jauh sudah stabil untuk sesi Cowork dan Claude Code; cakupan sesi Claude Science dan Claude for Microsoft 365 masih dalam versi beta.
  </Accordion>

  <Accordion title="Apa saja yang termasuk dalam transkrip sesi?">
    Transkrip sesi lokal dan jarak jauh sama-sama memuat prompt pengguna, respons asisten, serta pemanggilan alat dan hasilnya. Untuk sesi lokal (di mesin pengguna), itu berarti apa yang diminta kepada Claude dan apa yang dikembalikannya, bukan apa yang terjadi di perangkat.

    | Data                                 | Sesi lokal (di mesin pengguna)                                                                                                                                                                                                                               | Sesi jarak jauh (di cloud)                                                                                                                                                                               |
    | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Prompt pengguna                      | Ya; dikembalikan sebagai blok `text`.                                                                                                                                                                                                                        | Ya; dikembalikan sebagai blok `text`.                                                                                                                                                                    |
    | Respons asisten                      | Ya; hanya output teks.                                                                                                                                                                                                                                       | Ya; hanya output teks.                                                                                                                                                                                   |
    | Pemanggilan alat dan hasilnya        | Ya; setiap input `tool_use` dan setiap entri `text` dalam `tool_result` dipotong hingga 10.000 byte secara default (hingga sekitar 1 MiB masing-masing berdasarkan permintaan).                                                                              | Ya; setiap input `tool_use` dan setiap entri `text` dalam `tool_result` dipotong hingga 10.000 byte secara default (hingga sekitar 1 MiB masing-masing berdasarkan permintaan).                          |
    | Konten file dan nama file            | Ya; teks yang dibaca Claude melalui alat muncul dalam transkrip, dengan pemotongan yang sama. Gambar, PDF, dan konten biner atau terstruktur lainnya hanya muncul sebagai blok `text` placeholder. Nama file muncul dalam input dan output pemanggilan alat. | Ya; konten file dan nama file muncul dalam transkrip melalui input dan output pemanggilan alat (hanya teks; konten lain dihilangkan).                                                                    |
    | Artifacts                            | Ya; konten yang dihasilkan muncul di dalam input pemanggilan alat dalam transkrip.                                                                                                                                                                           | Ya; konten yang dihasilkan muncul di dalam input pemanggilan alat dalam transkrip.                                                                                                                       |
    | Skills                               | Ya; konten skill muncul ketika klien mengirimkannya sebagai konten pesan, dan tidak dibedakan dari teks pengguna lainnya.                                                                                                                                    | Ya; konten skill muncul dalam transkrip.                                                                                                                                                                 |
    | Metadata sesi                        | Ya; pemilik (`user.id` dan alamat email), organisasi, workspace, `product_surface`, `created_at`, dan `updated_at`, dari endpoint daftar dan ambil. Sesi lokal tidak memiliki `status`.                                                                      | Ya; pemilik, organisasi, status, stempel waktu, dan `product_surface`, dari endpoint daftar.                                                                                                             |
    | Blok thinking                        | Tidak.                                                                                                                                                                                                                                                       | Tidak.                                                                                                                                                                                                   |
    | Gambar dan konten non-teks lainnya   | Tidak; setiap gambar, PDF, atau blok biner atau terstruktur lainnya muncul sebagai blok `text` placeholder (misalnya, `[image content not shown]`) dengan `truncated` diatur ke `true`. Byte file mentah tidak pernah dikembalikan.                          | Tidak; blok non-teks dihilangkan, dan byte file mentah tidak pernah dikembalikan.                                                                                                                        |
    | Penggunaan token, biaya, dan latensi | Tidak; penggunaan token dan biaya tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).                                                     | Tidak; penggunaan token dan biaya tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api). |

    Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) dan [Sesi di cloud](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) untuk endpoint dan parameternya.
  </Accordion>

  <Accordion title="Bagaimana perbandingan cakupan sesi dengan logging OpenTelemetry (OTEL) untuk Cowork dan Claude Code?">
    [Logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage) tumpang tindih dengan endpoint sesi tetapi menjawab kebutuhan yang berbeda: OTEL melakukan streaming telemetri per peristiwa ke infrastruktur yang Anda jalankan saat aktivitas terjadi, sedangkan Compliance API memungkinkan Anda mengambil transkrip per sesi yang disimpan dari Anthropic setelah kejadian. OTEL juga dapat merekam prompt dan respons, tetapi Anthropic merekomendasikan Compliance API untuk mengambil konten sesi Cowork dan Claude Code. Untuk tabel yang membandingkan sesi lokal, sesi jarak jauh, dan OTEL, lihat pengantar [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions).

    Peristiwa OTEL dan catatan Compliance API berbagi pengidentifikasi organisasi dan pengguna, sehingga Anda dapat menggabungkannya.
  </Accordion>

  <Accordion title="Apakah konten yang dihapus dapat dipulihkan melalui Compliance API?">
    Tidak. Penghapusan yang dilakukan melalui Compliance API bersifat langsung, permanen, dan tidak dapat dipulihkan. Konten chat yang dihapus pengguna di claude.ai juga tidak dapat dipulihkan: Compliance API tetap mengembalikan chat dan pesan-pesannya, dengan `deleted_at` terisi, tetapi tidak dengan kontennya. Ambil konten apa pun yang perlu Anda simpan (untuk legal hold atau pengarsipan) selagi masih tersedia. Lihat [Merencanakan retensi konten](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#plan-content-retention) untuk mengetahui kapan harus mengekspor konten ke arsip Anda sendiri.
  </Accordion>

  <Accordion title="Apa yang tidak direkam oleh Compliance API?">
    Compliance API memiliki batas cakupan yang diketahui: Activity Feed merekam peristiwa sumber daya tetapi bukan teks prompt atau respons, beban kerja Claude Console dan Claude API yang diautentikasi dengan kunci API tidak mengekspos konten pesan sama sekali, dan konten yang dihapus oleh kebijakan retensi Anda, dihapus oleh pengguna di claude.ai, atau dihapus permanen melalui Compliance API tidak dapat dipulihkan. Untuk batas cakupan lengkap dan kontrak pengiriman, lihat [Jaminan pengiriman dan kelengkapan](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).

    Transkrip sesi memiliki batasnya sendiri. Sesi lokal hanya direkam saat permintaannya mencapai Claude API, sehingga aktivitas di perangkat yang tidak pernah mencapai API tidak direkam. Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, sesi Claude Code yang dijalankan melalui platform cloud pihak ketiga (Amazon Bedrock, Google Cloud, atau Microsoft Foundry), dan Claude Code di web juga tidak direkam; organisasi dengan kesiapan HIPAA yang diaktifkan tidak mendapatkan data sesi lokal; dan sesi yang menerapkan zero data retention dikecualikan. Tidak ada transkrip sesi, lokal maupun jarak jauh, yang menyertakan blok thinking atau definisi alat. Organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek) menerima transkrip sesi lokal seperti biasa. Selama kunci tidak dapat digunakan, endpoint pesan mengembalikan [503 Service Unavailable](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable) alih-alih konten transkrip, dan metadata sesi tetap dicantumkan.
  </Accordion>
</AccordionGroup>

## Integrasi dan paginasi

<AccordionGroup>
  <Accordion title="Bagaimana cara mengorelasikan catatan Compliance API dengan SIEM saya?">
    Gabungkan catatan `Activity` ke SIEM Anda berdasarkan `actor.user_id`, `actor.email_address`, `actor.ip_address`, `actor.user_agent`, dan `created_at`. Lihat [Merancang integrasi kepatuhan Anda](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem) untuk tabel kunci penggabungan dan pola konsumsi.
  </Accordion>

  <Accordion title="Dapatkah satu pelanggan memiliki beberapa organisasi di bawah satu induk?">
    Ya. Organisasi induk Claude Enterprise dapat memiliki banyak organisasi tertaut, termasuk campuran organisasi claude.ai dan organisasi Claude Console (misalnya, organisasi Claude Console produksi dan staging yang terpisah). Identitas, SSO, dan SCIM dibagikan di seluruh induk; penagihan, anggota, proyek, dan kunci API tetap terpisah untuk setiap organisasi. Pengaktifan Compliance API terjadi di tingkat organisasi induk dan diteruskan ke semua organisasi tertaut, dan Compliance Access Key yang mencakup organisasi induk serta membawa `read:compliance_org_data` dapat mencantumkan setiap organisasi di bawah induk melalui `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Apakah aktivitas dikembalikan secara berurutan, dan bagaimana cara mendeteksi bahwa saya sudah mengejar waktu nyata?">
    Aktivitas dikembalikan dari yang terbaru terlebih dahulu, dengan nilai `created_at` yang sama diurutkan berdasarkan ID aktivitas. Untuk mengejar, telusuri halaman ke depan dengan `before_id` hingga `has_more` bernilai `false`; `first_id` dari respons terakhir tersebut adalah kursor baru Anda dan Anda telah mencapai saat ini. Loop lengkapnya, termasuk backfill awal dan kondisi keamanan pada persistensi kursor, terdapat di [Pembacaan inkremental berbasis kursor](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="Bagaimana cara mendapatkan sandbox untuk menguji Compliance API?">
    Untuk menguji [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) saja, Anda tidak memerlukan organisasi Claude Enterprise: admin organisasi dapat [mengaktifkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) pada organisasi uji Claude Console mandiri yang memenuhi syarat dan mengkueri feed dengan Admin API key baru. Jika bagian **Compliance API** tidak terlihat di pengaturan Security organisasi tersebut, organisasi itu tidak memenuhi syarat untuk pengaktifan mandiri.

    Untuk menguji setiap endpoint, siapkan organisasi sandbox Claude Enterprise yang tertaut ke organisasi Claude Console di bawah induk yang sama. Ini memungkinkan sandbox menguji Activity Feed (melalui Admin API key) maupun endpoint chat, file, proyek, dan sesi (melalui Compliance Access Key).

    1. **Sediakan organisasi Claude Enterprise.** Hubungi perwakilan Anthropic Anda untuk menyiapkan organisasi sandbox Claude Enterprise. Pada organisasi Claude Enterprise yang sudah ada, pemilik utama dapat [mengaktifkan Compliance API langsung di claude.ai](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Buat organisasi Claude Console.** Buat sendiri organisasi Claude Console di `platform.claude.com` menggunakan alamat email yang sama.
    3. **Tautkan kedua organisasi.** Masuk sebagai pemilik utama organisasi Claude Enterprise, buka [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), dan gunakan **Merge Organizations** untuk menautkan keduanya di bawah induk bersama.

    Setelah tertaut, ikuti [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk membuat kunci dan mulai mengkueri. Organisasi uji menggunakan proses pengaktifan yang sama dengan organisasi produksi.
  </Accordion>
</AccordionGroup>
