---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-sessions
fetched_at: 2026-09-24T02:21:35.920672Z
sha256: 42c6515a6ae0ae93d0052c2399cef96fcd7369930d156d5a1176bdafb0a2c39c
---

---
title: Mengambil transkrip sesi
url: https://platform.claude.com/docs/id/manage-claude/compliance-sessions
description: Daftarkan sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Claude Cowork dan Claude Code, dan ambil transkripnya melalui Compliance API.
---

<Note>
  Endpoint di halaman ini hanya tersedia untuk organisasi Claude Enterprise. Endpoint sesi lokal dan sesi jarak jauh sudah stabil untuk sesi Cowork dan Claude Code. Cakupan untuk sesi Claude Science, Claude for Microsoft 365, dan Claude in Chrome masih dalam tahap beta. Endpoint ini menggunakan Compliance Access Key dan "scope" (cakupan) `read:compliance_user_data` yang sama dengan [endpoint chat, file, dan proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data). Anda tidak memerlukan kunci, cakupan, pengaturan, atau pembaruan klien baru. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Cakupan yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key.

  **Prasyarat:** Tidak ada prasyarat untuk mendaftarkan sesi di seluruh organisasi. Untuk memfilter daftar sesi jarak jauh (sesi di cloud) ke pengguna tertentu, Anda memerlukan ID pengguna dari [Daftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Daftar sesi lokal tidak memiliki filter pengguna.
</Check>

Endpoint di halaman ini menyediakan transkrip sesi yang dijalankan pengguna di organisasi Claude Enterprise Anda dalam aplikasi dan agen Claude kepada peninjau kepatuhan. Saat ini, cakupannya meliputi Cowork, Claude Code, Claude Science, Claude for Microsoft 365, dan Claude in Chrome. Setiap sesi adalah satu percakapan dengan Claude. Transkripnya berisi urutan prompt pengguna, respons asisten, serta panggilan dan hasil alat dalam percakapan tersebut. Endpoint ini mendukung ekspor "electronic discovery" (penemuan elektronik), atau eDiscovery, dan penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP.

Compliance API mengelompokkan sesi ke dalam dua keluarga endpoint berdasarkan lokasi sesi dijalankan. Endpoint "local session" (sesi lokal) mencakup sesi di mesin pengguna. Endpoint "remote session" (sesi jarak jauh) mencakup sesi yang berjalan di cloud dalam lingkungan yang dikelola Anthropic. Kedua keluarga bersifat hanya-baca, dan keduanya tidak dapat diakses dengan kunci Admin API (`sk-ant-admin01-...`). Panggilan yang diautentikasi dengan kunci Admin API akan mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Tabel berikut memetakan setiap produk dan lokasi menjalankannya ke keluarga endpoint yang mengembalikan sesinya, beserta nilai `product_surface` yang mengidentifikasi sesi tersebut dalam respons. Produk baru akan ditambahkan ke tabel ini seiring perluasan cakupan.

| Produk dan lokasi menjalankannya                                                                                                         | Keluarga endpoint                                                | `product_surface`                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cowork di Claude Desktop, berjalan di mesin pengguna                                                                                     | Endpoint sesi lokal (`/v1/compliance/apps/sessions/local`)       | `cowork`                                                                                                                                                       |
| Claude Code di terminal, di Claude Desktop, atau di ekstensi IDE, berjalan di mesin pengguna                                             | Endpoint sesi lokal                                              | `claude_code`                                                                                                                                                  |
| Aplikasi desktop Claude Science, berjalan di mesin pengguna                                                                              | Endpoint sesi lokal                                              | `claude_science`                                                                                                                                               |
| Claude for Microsoft 365 (add-in Claude untuk Excel, PowerPoint, Word, dan Outlook), berjalan di aplikasi desktop atau web Microsoft 365 | Endpoint sesi lokal                                              | `office_agents/excel`, `office_agents/powerpoint`, `office_agents/word`, atau `office_agents/outlook` (`office_agents` jika aplikasinya tidak teridentifikasi) |
| Claude in Chrome (chat bawaan ekstensi browser), berjalan di mesin pengguna                                                              | Endpoint sesi lokal                                              | `claude_in_chrome`                                                                                                                                             |
| Sesi Cowork yang dimulai di claude.ai web atau seluler, berjalan di cloud dalam lingkungan yang dikelola Anthropic                       | Endpoint sesi jarak jauh (`/v1/compliance/apps/sessions/remote`) | `cowork_remote`                                                                                                                                                |

Penangkapan sesi lokal bergantung pada aktifnya Compliance API untuk organisasi Anda, dan hanya berlaku selama pengguna masuk dengan akun Claude Enterprise mereka. Endpoint sesi tidak mengembalikan hal-hal berikut:

* Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, atau yang dijalankan melalui platform cloud pihak ketiga seperti Amazon Bedrock, Google Cloud, atau Microsoft Foundry.
* [Sesi cloud Claude Code](https://code.claude.com/docs/id/claude-code-on-the-web), yang berjalan di infrastruktur cloud, bukan di mesin pengguna. Meskipun sama-sama berjalan di cloud, sesi cloud ini bukan sesi jarak jauh. Endpoint sesi jarak jauh hanya mengembalikan sesi Cowork.
* Sesi lokal di organisasi yang mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness). Tidak ada data sesi lokal yang ditangkap, sehingga endpoint sesi lokal tidak mengembalikan sesi apa pun untuk organisasi tersebut.
* Sesi lokal yang dikenai ["zero data retention" (retensi data nol), atau ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope). Sesi ini dikecualikan dari hasil daftar, dan endpoint retrieve serta messages mengembalikan 404 untuk sesi tersebut.

Anthropic merekomendasikan Compliance API untuk mengambil konten sesi. Tabel berikut membandingkan [sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) dan [sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) dengan alternatif berbasis OpenTelemetry yang tersedia untuk Cowork dan Claude Code, yaitu [logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan [pemantauan Claude Code](https://code.claude.com/docs/id/monitoring-usage).

|                                                              | Sesi lokal (di mesin pengguna)                                                                                                                                               | Sesi jarak jauh (di cloud)                                                                                                                                                   | Logging OpenTelemetry                                                                                                                    |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Pengiriman                                                   | Pull: kueri dan ekspor melalui HTTPS                                                                                                                                         | Pull: kueri dan ekspor melalui HTTPS                                                                                                                                         | Push: di-stream ke kolektor OTLP Anda                                                                                                    |
| Penyiapan                                                    | Menggunakan Compliance Access Key yang sudah Anda miliki                                                                                                                     | Menggunakan Compliance Access Key yang sudah Anda miliki                                                                                                                     | Admin mengonfigurasi endpoint OTLP dan pengaturan penangkapan konten                                                                     |
| Infrastruktur                                                | Di-host oleh Anthropic                                                                                                                                                       | Di-host oleh Anthropic                                                                                                                                                       | Anda menjalankan kolektor dan penyimpanan sendiri                                                                                        |
| Prefiks ID                                                   | `clls_`                                                                                                                                                                      | `cse_`                                                                                                                                                                       | N/A                                                                                                                                      |
| Nilai `product_surface`                                      | `cowork`, `claude_code`, `claude_science`, `claude_in_chrome`, dan nilai yang diawali `office_agents`                                                                        | `cowork_remote`                                                                                                                                                              | N/A                                                                                                                                      |
| Retensi                                                      | 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda jika periode terbatas telah ditetapkan; disimpan oleh Anthropic                               | 6 tahun, kecuali pengguna menghapus sesi lebih awal; disimpan oleh Anthropic                                                                                                 | Infrastruktur Anda, kebijakan Anda                                                                                                       |
| Prompt pengguna dan respons asisten                          | Ya                                                                                                                                                                           | Ya                                                                                                                                                                           | Ya, bergantung pada pengaturan penangkapan konten                                                                                        |
| Input alat                                                   | Dipotong menjadi 10.000 byte per input secara default; hingga sekitar 1 MiB jika diminta                                                                                     | Dipotong menjadi 10.000 byte per input secara default; hingga sekitar 1 MiB jika diminta                                                                                     | Ringkasan yang dipotong                                                                                                                  |
| Konten hasil alat                                            | Setiap entri teks dipotong menjadi 10.000 byte secara default; hingga sekitar 1 MiB jika diminta                                                                             | Setiap entri teks dipotong menjadi 10.000 byte secara default; hingga sekitar 1 MiB jika diminta                                                                             | Metadata seperti ukuran dan status keberhasilan; Claude Code juga dapat menangkap konten melalui pengaturan opsional dengan batas ukuran |
| Isi file                                                     | Ya, melalui panggilan alat dalam transkrip (hanya teks; konten lain muncul sebagai placeholder)                                                                              | Ya, melalui panggilan alat dalam transkrip (hanya teks; konten lain dihilangkan)                                                                                             | Path file; Claude Code juga dapat menangkap isi file melalui pengaturan opsional dengan batas ukuran                                     |
| Metadata host dan perangkat (jenis terminal, path workspace) | Tidak                                                                                                                                                                        | Tidak                                                                                                                                                                        | Ya                                                                                                                                       |
| Penggunaan token dan biaya                                   | Tidak; tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api) | Tidak; tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api) | Ya                                                                                                                                       |

## Sesi di mesin pengguna (sesi lokal)

Sesi lokal berjalan di mesin pengguna selama mereka masuk dengan akun Claude Enterprise. Saat ini, sesi lokal mencakup Cowork di Claude Desktop, Claude Code (di terminal, di Claude Desktop, atau di ekstensi IDE), aplikasi desktop Claude Science, Claude for Microsoft 365 (di Excel, PowerPoint, Word, dan Outlook), serta ekstensi browser Claude in Chrome.

Compliance API menyediakan sesi lokal melalui tiga endpoint:

* `GET /v1/compliance/apps/sessions/local` mendaftarkan metadata sesi.
* `GET /v1/compliance/apps/sessions/local/{session_id}` mengambil metadata satu sesi.
* `GET /v1/compliance/apps/sessions/local/{session_id}/messages` mengembalikan transkrip satu sesi.

Ketiganya memerlukan cakupan `read:compliance_user_data` dan hanya dihitung terhadap "rate limit" (batas laju) Compliance API bersama. Ketiganya tidak dikenai anggaran permintaan kedua yang berlaku untuk endpoint sesi jarak jauh. Lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests).

Jika sesi lokal tidak tersedia untuk organisasi induk Anda, ketiga endpoint mengembalikan 404 dengan pesan `Local sessions are not available.` (lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found)). Selama daftar sesi atau konten yang ditangkap untuk sementara tidak tersedia, ketiganya mengembalikan 503 (lihat [Sesi lokal untuk sementara tidak tersedia](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable)).

Untuk sesi lokal, Anthropic mencatat setiap percakapan di sisi server saat permintaannya mencapai Claude API. Tidak ada yang dipasang di perangkat, dan tidak ada data yang dikumpulkan selain permintaan yang memang sudah dikirim klien ke Claude API. Transkrip sesi lokal menunjukkan apa yang diminta dari Claude dan apa yang dikembalikannya, bukan apa yang terjadi di perangkat. Aktivitas file dan jaringan hanya terlihat melalui panggilan alat dan hasil alat dalam transkrip. Aktivitas yang tidak pernah mencapai API tidak ditangkap, misalnya file lokal yang tidak pernah dikirim oleh sesi.

Di organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek), transkrip sesi lokal dienkripsi dengan kunci tersebut dan dikembalikan seperti biasa. Jika kunci itu tidak dapat digunakan, endpoint messages mengembalikan [503 Service Unavailable](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable) untuk halaman yang terdampak, bukan konten transkrip. Hal ini terjadi, misalnya, karena Anda menonaktifkan atau mencabut kunci, atau karena kunci tidak dapat dijangkau. Pesan-pesan tersebut tidak pernah dilaporkan sebagai `not_captured` (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript)). Mencantumkan sesi dan mengambil metadata sesi tidak terpengaruh.

Endpoint list mengembalikan metadata sesi, tanpa konten transkrip, untuk setiap organisasi tertaut yang dapat dibaca oleh kunci Anda. Berbeda dengan daftar sesi jarak jauh, endpoint ini tidak memiliki filter organisasi atau pengguna. Batasi hasil berdasarkan waktu dengan parameter `created_at.gte` dan `created_at.lt`. Keduanya menerima timestamp RFC 3339 dengan offset UTC wajib. Jika keduanya diberikan, `created_at.lt` harus lebih lambat daripada `created_at.gte`. Jika tidak, permintaan mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request).

Filter waktu ketiga, `updated_at.gte`, membatasi hasil berdasarkan aktivitas terakhir, bukan aktivitas pertama. Filter ini mengembalikan sesi yang panggilan inferensi terakhirnya terjadi pada atau setelah waktu yang diberikan. Filter ini dapat digabungkan dengan filter `created_at` tanpa mengubah urutan atau paginasi. Gunakan filter ini untuk melakukan polling sesi yang aktif sejak proses sebelumnya, seperti dijelaskan nanti di bagian ini.

Sesi dan pesan baru muncul dalam hasil setelah jeda pemrosesan singkat, biasanya dalam hitungan menit. Jadi, sesi yang belum muncul tepat setelah dimulai belum tentu tidak tertangkap. Permintaan berikut mendaftarkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data-urlencode "created_at.gte=2026-07-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "type": "compliance_local_session",
      "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
      "user": {
        "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
        "email_address": "engineer@example.com"
      },
      "product_surface": "cowork",
      "created_at": "2026-07-09T14:02:11Z",
      "updated_at": "2026-07-09T14:02:38Z"
    },
    {
      "type": "compliance_local_session",
      "id": "clls_01HyLqMnOpQrStUvWxYzAbCd",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": null,
      "user": {
        "id": "user_01HqRsTuVwXyZaBcDeFgHiJk",
        "email_address": null
      },
      "product_surface": "claude_code",
      "created_at": "2026-07-08T09:15:43Z",
      "updated_at": "2026-07-08T09:52:10Z"
    }
  ],
  "next_page": "page_AAEfQx7mPdLkq9Rt2VwHbZk"
}
```

Hasil diurutkan secara kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at`. Sesi dengan nilai yang sama diurutkan menurut urutan tetap di sisi server. Setiap respons berisi paling banyak `limit` hasil (default 100, maksimum 500).

Endpoint ini hanya melakukan paginasi maju dengan token `page` dan `next_page` (lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)). Kirimkan nilai `next_page` dari respons sebagai parameter kueri `page` pada permintaan berikutnya, dan berhenti saat `next_page` bernilai `null`. Respons tidak memiliki field `has_more`.

Selesaikan penelusuran daftar dalam 24 jam sejak dimulai. Kursor daftar yang lebih lama masih diterima, tetapi dievaluasi ulang terhadap batas retensi saat ini. Akibatnya, sesi yang aktivitas tertua yang masih disimpannya hampir melewati periode retensi dapat terlewat.

Di setiap objek sesi, `user.id` selalu terisi dan tetap ada meskipun akun dihapus. `user.email_address` bernilai `null` jika akun pengguna telah dihapus atau pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca oleh kunci Anda. `workspace_id` bernilai `null` jika sesi tidak dikaitkan dengan workspace.

Satu sesi lokal sesuai dengan satu ID sesi klien. Memulai percakapan baru di klien, atau menghapus konteksnya, akan membuat catatan sesi baru. Untuk Claude Science, daftar juga dapat mencakup sesi terpisah untuk pekerjaan latar belakang aplikasi itu sendiri, misalnya pemberian nama percakapan. Pada versi aplikasi yang lebih baru, pekerjaan ini juga mencakup jalur peninjau dan delegasinya. Pada versi aplikasi yang lebih lama, sebagian pekerjaan latar belakang tersebut muncul sebagai pesan tambahan di dalam transkrip percakapan itu sendiri. Percakapan Claude Science yang berlanjut melewati beberapa pembaruan aplikasi akan muncul sebagai dua sesi. Perilaku ini memang diharapkan. Perlakukan nilai `id` sebagai string buram, karena formatnya dapat berubah tanpa pemberitahuan.

Untuk Claude for Microsoft 365, penghapusan percakapan di add-in hanya terjadi di sisi klien, sehingga tidak tercermin di API. Sesi lokal tidak memiliki field `deleted_at`, dan sesi tetap terdaftar hingga dihapus oleh retensi.

Sesi lokal memiliki `updated_at`, tetapi tidak memiliki `status`. Sesi lokal tidak memiliki status siklus hidup di sisi server, dan visibilitasnya diatur oleh retensi. Sesi lokal ditangkap sebagai rangkaian panggilan Claude API (panggilan inferensi) yang dilakukan klien selama sesi, dan retensi berlaku untuk setiap panggilan yang ditangkap secara terpisah.

`created_at` adalah timestamp panggilan tertua yang masih disimpan dalam sesi, dan `updated_at` adalah timestamp panggilan terakhirnya. Keduanya dalam UTC. Saat panggilan yang lebih lama melewati periode retensi, `created_at` ikut bergeser maju. Setelah semua panggilan dalam sesi melewati periode retensi, sesi tidak lagi dikembalikan. `updated_at` mengikuti panggilan terbaru dan tidak terpengaruh hingga saat itu. Karena `created_at` dapat bergeser di antara proses, lakukan deduplikasi berdasarkan `id` saat Anda menelusuri ulang daftar dari waktu ke waktu.

Agar transkrip tetap mutakhir saat sesi mendapatkan pesan baru, lakukan polling dengan filter `updated_at.gte` menggunakan jendela waktu berurutan yang saling tumpang tindih. Pada endpoint list, `updated_at` adalah batas bawah. Untuk sesi yang masih aktif di batas halaman atau batas jendela `created_at.lt`, nilainya dapat sesaat tertinggal dari aktivitas terakhir sesi yang sebenarnya. Selain itu, panggilan baru hanya dapat dikueri setelah jeda pemrosesan singkat yang disebutkan sebelumnya.

Karena keterlambatan tersebut, atur `updated_at.gte` pada setiap proses beberapa menit sebelum waktu mulai proses sebelumnya, bukan tepat pada waktu proses sebelumnya. Jika batas diatur tepat pada waktu sebelumnya, sesi yang panggilan terakhirnya masih diindeks pada saat itu akan hilang secara diam-diam dan permanen. Setelah batas bergeser melewati panggilan tersebut, tidak ada proses berikutnya yang akan mengembalikannya.

Lakukan deduplikasi sesi yang dikembalikan berdasarkan `id`, ambil ulang transkripnya, lalu lakukan deduplikasi pesan berdasarkan `id`. Pengambilan sesi atau pesannya selalu mencerminkan panggilan terbaru yang masih disimpan secara tepat. Karena itu, proses rekonsiliasi berkala atas jendela waktu yang lebih lama merupakan alternatif yang lebih menyeluruh daripada memperlebar tumpang tindih.

Daftar dibangun dari metadata aktivitas sesi, sehingga dapat mencakup sesi yang konten transkripnya tidak ditangkap. Contohnya adalah sesi yang berjalan sebelum penangkapan dimulai untuk organisasi Anda, sejauh yang diizinkan periode retensi Anda. Transkrip sesi semacam itu mengembalikan setiap pesan dengan konten yang ditandai tidak tersedia (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript)).

Konten sesi lokal yang ditangkap disimpan selama 6 tahun sejak penangkapan secara default. Organisasi yang menjalankan sesi mungkin telah menetapkan periode retensi percakapan kustom yang terbatas di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). Dalam hal ini, periode tersebut yang berlaku, baik lebih pendek maupun lebih panjang dari default. Jika organisasi mengonfigurasi lebih dari satu periode retensi kustom, periode terpendek yang berlaku.

Perubahan pada pengaturan tersebut berlaku dengan dua cara berbeda. Endpoint langsung berhenti mengembalikan aktivitas yang lebih lama dari periode organisasi saat ini begitu pengaturan diubah. Sementara itu, setiap pesan yang ditangkap disimpan sesuai periode yang berlaku saat pesan tersebut ditangkap. Jadi, memperpanjang periode di kemudian hari tidak akan memulihkan konten yang sudah kedaluwarsa.

Untuk mengambil metadata satu sesi secara langsung, kirimkan ID-nya ke `GET /v1/compliance/apps/sessions/local/{session_id}`. Responsnya adalah objek sesi yang sama dengan yang dikembalikan endpoint list, tanpa envelope dan tanpa konten transkrip. ID sesi yang formatnya salah mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request).

Satu respons [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) mencakup empat kasus yang tidak dibedakan oleh respons:

* Sesi tidak berada di organisasi yang dapat dibaca oleh kunci Anda, termasuk sesi di bawah organisasi induk lain.
* Sesi tidak ada.
* Sesi dikenai retensi data nol.
* Semua panggilan dalam sesi telah melewati periode retensi.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi:

* `cowork`: Cowork di Claude Desktop pada mesin pengguna.
* `claude_code`: Claude Code.
* `claude_science`: Claude Science.
* `claude_in_chrome`: chat bawaan ekstensi browser Claude in Chrome.
* `office_agents/excel`, `office_agents/powerpoint`, `office_agents/word`, atau `office_agents/outlook`: Claude for Microsoft 365, per aplikasi. Nilainya hanya `office_agents` jika aplikasinya tidak teridentifikasi.

Nilai baru akan muncul seiring perluasan cakupan.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan handler Anda. Dengan begitu, integrasi Anda tetap berfungsi saat permukaan produk baru dirilis.
</Note>

### Mengambil transkrip sesi lokal

Endpoint messages mengembalikan transkrip sesi yang direkonstruksi dari panggilan Claude API yang ditangkap. Transkrip ini mencakup prompt pengguna, teks asisten, panggilan alat, dan bagian teks dari hasil alat. Semuanya dikembalikan persis seperti saat dikirim, kecuali untuk pemotongan ukuran. Tidak ada penyamaran URL, kredensial, atau data pribadi dalam konten tersebut, jadi perlakukan transkrip sebagai data sensitif. Transkrip menghilangkan atau mengganti hal-hal berikut:

* Blok thinking tidak pernah disertakan.
* "System prompt" (prompt sistem) dari permintaan tidak pernah dikembalikan. Sebagai gantinya, muncul pesan penanda bertuliskan `[system prompt content not shown]` (biasanya sekali per sesi; sesi tanpa konten yang ditangkap tidak memiliki penanda ini).
* Definisi alat dan konfigurasi server "Model Context Protocol", atau MCP, tidak termasuk dalam transkrip.
* Gambar, PDF, dan blok biner atau terstruktur lainnya tidak dikembalikan. Masing-masing muncul sebagai blok `text` bertuliskan `[<block type> content not shown]` (misalnya, `[image content not shown]`) dengan `truncated` bernilai `true`. Item non-teks di dalam hasil alat, seperti hasil [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) atau output [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), diganti dengan satu entri `[N non-text item(s) not shown]`, dan `truncated` pada blok hasil alat tersebut bernilai `true`. Panggilan alat yang terkait, beserta kueri pencarian atau kode dalam `input`-nya, tetap dikembalikan.
* Metadata sitasi pada blok `text` dihilangkan, misalnya sitasi sumber pada jawaban yang menggunakan hasil pencarian web. Teksnya tetap dikembalikan, dan blok tersebut memiliki `truncated` bernilai `true`.

File instruksi proyek seperti `CLAUDE.md` muncul sebagai konten biasa dengan peran pengguna. Konten skill muncul jika klien mengirimkannya sebagai konten pesan, dan tidak dibedakan dari teks pengguna lainnya. Untuk ringkasan cakupan, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention). Untuk tabel perbandingan sesi lokal dengan sesi jarak jauh dan logging OpenTelemetry, lihat bagian pendahuluan halaman ini.

```bash cURL
session_id="clls_01HxKpLmNoPqRsTuVwXyZaBc"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json Response
{
  "session": {
    "type": "compliance_local_session",
    "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
    "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
    "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
    "user": {
      "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
      "email_address": null
    },
    "product_surface": "cowork",
    "created_at": "2026-07-09T14:02:11Z",
    "updated_at": "2026-07-09T14:02:38Z"
  },
  "data": [
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBa",
      "role": "user",
      "model": null,
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": {
        "type": "synthetic_marker"
      },
      "content": [
        {
          "type": "text",
          "text": "[system prompt content not shown]",
          "truncated": true
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBc",
      "role": "user",
      "model": null,
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "Fix the failing test in tests/auth_test.py",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBd",
      "role": "assistant",
      "model": "claude-opus-5-5",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "I'll read the test file first.",
          "truncated": false
        },
        {
          "type": "tool_use",
          "id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "input": "{\"file_path\":\"tests/auth_test.py\"}",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBe",
      "role": "user",
      "model": null,
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "is_error": false,
          "content": [
            {
              "type": "text",
              "text": "def test_login_expiry():\n    ..."
            }
          ],
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBf",
      "role": "assistant",
      "model": "claude-opus-5-5",
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "The test was asserting on a stale expiry timestamp. I've updated it.",
          "truncated": false
        }
      ]
    }
  ],
  "next_page": null
}
```

Respons menyertakan envelope `session` di samping array `data` yang dipaginasi. Catatan pertama dalam contoh ini adalah penanda yang menggantikan prompt sistem dari permintaan. `provenance`-nya dijelaskan nanti di bagian ini. Pada endpoint ini, `user.email_address` selalu bernilai `null` karena endpoint messages tidak me-resolve alamat email. Jadi, nilai `null` di sini tidak berarti akun pengguna telah dihapus. Untuk mengaitkan sesi dengan alamat email, cocokkan `user.id` dengan data dari [endpoint list](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) atau endpoint retrieve (`GET /v1/compliance/apps/sessions/local/{session_id}`).

Secara default, pesan dikembalikan mulai dari yang terlama. Teruskan `order=desc` untuk membalik urutannya. Paginasi menggunakan skema `page`/`next_page` yang sama dengan endpoint list, dengan `limit` default 100 dan maksimum 1.000. Halaman dapat berakhir lebih awal jika respons mencapai batas ukurannya. Jadi, halaman yang berisi pesan lebih sedikit dari `limit` tidak berarti Anda telah mencapai akhir. Teruskan paginasi hingga `next_page` bernilai `null`. Kursor halaman terikat pada sesi dan urutan pengurutan saat kursor diterbitkan. Kursor dari suatu penelusuran kedaluwarsa 24 jam setelah halaman pertamanya. Kursor yang kedaluwarsa mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) yang meminta Anda memulai ulang tanpa parameter `page`, dan penelusuran yang dimulai ulang akan mengikuti batas retensi saat ini. Kursor yang diterbitkan untuk sesi atau `order` yang berbeda juga mengembalikan 400 karena dianggap tidak valid.

Setiap pesan memiliki `role` (`user` atau `assistant`) dan array `content` yang berisi blok `text`, `tool_use`, dan `tool_result`. Setiap pesan juga memiliki `model`. Pada giliran asisten yang ditangkap dari Claude API, nilainya adalah model yang melayani giliran tersebut. Nilainya `null` pada pesan pengguna dan pada pesan asisten yang `provenance`-nya terisi. Alasannya, riwayat yang dinyatakan klien dan penanda sintetis tidak dihasilkan oleh model, sedangkan model yang melayani konten yang tidak tersedia tidak diketahui.

Blok `text` berisi `text` dan `truncated`. Blok `tool_use` berisi `id`, `name`, `input`, dan `truncated`, dengan `input` berupa string yang dienkode JSON, bukan objek. Blok `tool_result` berisi `tool_use_id`, `name`, `is_error`, array `content` yang berisi entri `text`, dan `truncated`. Panggilan dan hasil alat MCP, serta sebagian besar panggilan dan hasil alat server, dinormalisasi ke dalam bentuk `tool_use` dan `tool_result` yang sama. Jenis blok lainnya muncul sebagai placeholder `[<block type> content not shown]`. `id` pesan tetap stabil selama giliran tersebut masih disimpan. Semua pesan yang direkonstruksi dari panggilan inferensi yang sama memiliki timestamp panggilan tersebut, sehingga pesan yang berurutan sering kali memiliki nilai `created_at` yang sama. Pertahankan urutan yang dikembalikan dan jangan mengurutkan ulang berdasarkan timestamp.

Setiap pesan juga memiliki field `provenance` yang menjelaskan cara kontennya ditangkap. Pada kasus umum, yaitu konten terverifikasi yang ditangkap oleh Claude API, `provenance` bernilai `null`. Jika tidak, nilainya berupa objek dengan `type` yang menunjukkan jenis pengecualiannya:

* `content_unavailable` berarti konten tidak dapat dikembalikan. Array `content` kosong, dan `provenance.reason` menjelaskan alasannya:

  * `not_captured` berarti tidak ada konten yang tersedia untuk giliran tersebut. Alasan ini tidak membuktikan bahwa tidak ada catatan yang disimpan. Konten yang ditahan dari Compliance API oleh kebijakan penanganan data Anthropic juga dilaporkan dengan alasan yang sama. Hal yang sama berlaku untuk giliran tertentu yang tidak tersedia karena alasan tersebut, meskipun bagian lain sesinya berhasil ditangkap. Satu-satunya pengecualian adalah kunci yang dikelola pelanggan yang tidak dapat digunakan, yang mengembalikan [503 Service Unavailable](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable).
  * `client_aborted` berarti klien menutup koneksi atau membatalkan permintaan sebelum respons selesai, sehingga respons untuk giliran tersebut tidak ditangkap. Output parsial yang sudah di-stream ke klien tidak disertakan, dan alasan ini hanya berlaku untuk giliran dengan peran asisten.
  * `cmek_key_revoked` dicadangkan untuk konten yang dienkripsi dengan kunci yang dikelola pelanggan milik organisasi Anda ketika kunci tersebut tidak tersedia (misalnya, dicabut). Saat ini alasan ini tidak dikembalikan karena kunci yang tidak dapat digunakan menghasilkan 503. Namun, tetap tangani alasan ini demi kompatibilitas ke depan.
  * `retention_elapsed` berarti konten telah melewati periode retensi.
  * `oversize` berarti satu pesan melebihi batas ukuran per pesan. Pesan tersebut tetap dikembalikan, tetapi dengan array `content` yang kosong.

* `client_asserted` menandai pesan asisten yang diberikan klien sebagai riwayat percakapan tetapi tidak dapat dicocokkan dengan respons yang ditangkap. Kepengarangan pesan ini tidak terverifikasi.

* `synthetic_marker` menandai catatan yang dibuat oleh endpoint itu sendiri, seperti penanda yang menggantikan prompt sistem. Jika klien menulis ulang atau memadatkan riwayat percakapannya di tengah sesi (misalnya, setelah pemadatan konteks), transkrip menyisipkan pesan penanda pada titik tersebut, lalu melanjutkan dengan konten baru yang dikirim klien. Jika organisasi Anda memiliki periode retensi terbatas dan konten baru tersebut mencakup pesan asisten, transkrip menahan konten baru hingga dan termasuk pesan asisten terakhirnya (penanda kedua mencatat hal ini). Setelah itu, transkrip hanya menampilkan pesan pengguna setelah titik tersebut, diikuti oleh sisa sesi.

Pesan penanda dan pesan yang dinyatakan klien diawali dengan blok `text` berisi penjelasan dalam tanda kurung siku yang ditandai `truncated: true`, misalnya `[system prompt content not shown]`. Perlakukan catatan ini sebagai catatan yang ada tetapi tidak tersedia atau tidak terverifikasi, bukan sebagai catatan yang hilang. Pastikan juga integrasi Anda dapat menangani jenis dan alasan `provenance` yang tidak dikenali.

Dua parameter membatasi jumlah byte yang dikembalikan dari setiap blok alat: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, masing-masing dengan default 10.000 byte. Teruskan `-1` untuk menggunakan maksimum server (sekitar 1 MiB per string). Nilai `0` mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request), dan nilai di atas maksimum akan diturunkan ke nilai maksimum tersebut. String yang terpotong oleh salah satu batas ini dipotong pada batas karakter dan diberi akhiran in-band (misalnya, `…[truncated; pass tool_result_max_bytes=-1 for the server max]`), dan bloknya memiliki `"truncated": true`. Karena itu, `input` `tool_use` yang terpotong bukan lagi JSON yang valid. Parse input alat hanya dari blok yang tidak terpotong, atau naikkan batasnya lalu ambil ulang. Blok bertipe `text` selalu dibatasi pada maksimum server yang sama, yaitu sekitar 1 MiB. Tidak ada parameter untuk menaikkan batas ini, dan blok `text` yang mencapai batas tersebut juga memiliki `"truncated": true`.

Claude Science memanggil konektor (server MCP) dari kode yang dijalankannya melalui alat `repl`, bukan sebagai alat dengan nama tersendiri. Akibatnya, tidak ada blok dalam transkrip Claude Science yang dinamai sesuai konektor. Setiap panggilan konektor muncul dalam kode di dalam `input` blok `tool_use` `repl` (misalnya, panggilan `host.mcp("<server>", "<tool>", ...)`). Output konektor hanya muncul di `tool_result` yang terkait jika kode tersebut mencetaknya. Sesi Cowork dan Claude Code berbeda: keduanya memanggil setiap alat konektor dengan namanya sendiri, yaitu `mcp__<server>__<tool>`, yang menjadi `name` dari blok `tool_use`. Untuk memantau penggunaan konektor dalam sesi Claude Science, parse string `input` dan cocokkan berdasarkan kode di dalamnya, bukan berdasarkan nama alat. Teruskan `tool_use_input_max_bytes=-1` untuk sesi ini. Dengan begitu, input kode yang panjang dikembalikan hingga maksimum server dan tidak terpotong pada default 10.000 byte sebelum panggilan konektor muncul.

Konten transkrip mengikuti periode retensi yang dijelaskan di [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Jika awal sesi telah melewati periode tersebut, transkrip diawali dengan satu placeholder `content_unavailable` dengan `reason` bernilai `retention_elapsed`, diikuti oleh pesan-pesan yang masih disimpan. Jika semua panggilan dalam sesi telah melewati retensi, endpoint messages mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found). Respons yang sama juga dikembalikan untuk sesi di organisasi yang tidak dapat dibaca oleh kunci Anda, sesi yang tidak ada, dan sesi yang dikenai retensi data nol. ID sesi dengan format yang salah mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request).

## Sesi di cloud (sesi jarak jauh)

Sesi Cowork yang dimulai di claude.ai web atau seluler berjalan di cloud dalam lingkungan yang dikelola Anthropic. Compliance API mengekspos sesi jarak jauh ini melalui dua endpoint: `GET /v1/compliance/apps/sessions/remote` mendaftarkan metadata sesi, dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi. Keduanya memerlukan cakupan `read:compliance_user_data`, dan keduanya dihitung terhadap batas laju Compliance API bersama ditambah anggaran permintaan kedua yang khusus untuk endpoint ini; lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests).

Endpoint list secara default bercakupan seluruh organisasi: hilangkan `organization_ids[]` untuk menyertakan setiap organisasi claude.ai yang dapat dibaca kunci Anda, atau teruskan hingga 500 nilai untuk mempersempit cakupan. Untuk membatasi daftar ke pengguna tertentu, teruskan 1–10 nilai `user_ids[]` (dapatkan ID-nya dari [Daftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)); filter ini mencocokkan pengguna pemilik sesi, sehingga sesi milik agen dikecualikan setiap kali `user_ids[]` diatur. Batasi hasil berdasarkan waktu dengan parameter rentang `created_at` (`gte`, `gt`, `lt`, `lte`, dalam format RFC 3339). Tidak ada filter `updated_at`. Permintaan berikut mendaftarkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data-urlencode "created_at.gte=2026-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "agent_id": null,
      "started_by_user": null,
      "status": "active",
      "created_at": "2026-07-01T17:04:05Z",
      "updated_at": "2026-07-01T18:00:41Z",
      "product_surface": "cowork_remote",
      "claude_project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq"
    },
    {
      "id": "cse_01TkNpRsUvWxYzAbCdEfGhJ4",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": null,
      "agent_id": "cagt_01MnPqRsTuVwXyZaBcDeFgH8",
      "started_by_user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "status": "archived",
      "created_at": "2026-06-28T09:15:22Z",
      "updated_at": "2026-06-28T09:47:10Z",
      "product_surface": "cowork_remote",
      "claude_project_id": null
    }
  ],
  "next_page": "page_AAEfMk93cXpYdGxrZXk"
}
```

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at` dan dibatasi hingga `limit` hasil per respons (default 100, maks 500). Endpoint ini melakukan paginasi dengan token `page` dan `next_page` (lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)): teruskan nilai `next_page` dari respons sebagai parameter kueri `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`.

Sebuah sesi dimiliki oleh pengguna atau agen, tidak pernah keduanya. Untuk sesi milik pengguna, `user` memuat ID dan alamat email pemilik (`email_address` bernilai `null` ketika pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca kunci Anda) dan `agent_id` bernilai `null`. Untuk sesi milik agen (misalnya, tugas terjadwal), `user` bernilai `null`, `agent_id` memuat ID agen (prefiks `cagt_`), dan `started_by_user` mengidentifikasi manusia yang memulai run tersebut, misalnya dengan memulai tugas terjadwal; pada sesi milik pengguna, `started_by_user` bernilai `null`.

`claude_project_id` adalah ID [proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-projects-and-attachments) claude.ai tempat sesi berada (prefiks `claude_proj_`), atau `null` ketika sesi tidak berada dalam proyek.

`status` adalah salah satu dari `pending`, `active`, `paused`, `archived`, atau `failed`. Sesi berstatus `pending` selama sedang disediakan; sesi `pending` belum memiliki transkrip, dan endpoint messages mengembalikan 404 untuknya hingga penyediaan selesai. Sesi yang telah dihapus tidak pernah dikembalikan.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi. Endpoint ini saat ini hanya mengembalikan sesi dengan `product_surface` bernilai `cowork_remote`: sesi Cowork yang dimulai di claude.ai web atau seluler.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `status` dan `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan handler Anda, agar integrasi Anda tetap berfungsi saat status dan product surface baru dirilis.
</Note>

### Mengambil transkrip sesi jarak jauh

Endpoint messages mengembalikan transkrip sesi: prompt pengguna, respons asisten, serta panggilan alat dan hasilnya. Blok thinking dan gambar tidak disertakan. Untuk ringkasan cakupan, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention); untuk tabel yang membandingkan sesi jarak jauh dengan sesi lokal dan logging OpenTelemetry Cowork, lihat pengantar halaman ini.

```bash cURL
session_id="cse_01WpQrStUvXyZaBcDeFgHjK6"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json Response
{
  "session": {
    "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
    "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
    "user": {
      "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "email_address": null
    },
    "agent_id": null,
    "started_by_user": null,
    "status": "active",
    "created_at": "2026-07-01T17:04:05Z",
    "updated_at": "2026-07-01T18:00:41Z",
    "product_surface": "cowork_remote",
    "claude_project_id": null
  },
  "data": [
    {
      "id": "csev_01HjKmNpQrStUvWxYzAbCdE2",
      "role": "user",
      "created_at": "2026-07-01T17:04:05Z",
      "content": [
        {
          "type": "text",
          "text": "Summarize the customer feedback in the attached spreadsheet.",
          "truncated": false
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    },
    {
      "id": "csev_01BcDeFgHjKmNpQrStUvWxY4",
      "role": "assistant",
      "created_at": "2026-07-01T17:04:06Z",
      "content": [
        {
          "type": "text",
          "text": "I'll start by reading the spreadsheet...",
          "truncated": false
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    }
  ],
  "next_page": null
}
```

Respons menyematkan envelope `session` di samping array `data` yang dipaginasi. Pada endpoint ini envelope selalu memiliki `user.email_address`, `started_by_user`, dan `claude_project_id` bernilai `null`; dapatkan nilai-nilai tersebut dari endpoint list.

Pesan dikembalikan dari yang terlama lebih dulu secara default; teruskan `order=desc` untuk membalik urutan. Paginasi menggunakan skema `page`/`next_page` yang sama dengan endpoint list, dengan `limit` default 100 dan maks 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai batas ukurannya, sehingga halaman dengan pesan kurang dari `limit` tidak berarti Anda telah mencapai akhir; teruslah melakukan paginasi hingga `next_page` bernilai `null`.

Setiap pesan memiliki `role` (`user` atau `assistant`) dan array `content` berisi blok `text`, `tool_use`, dan `tool_result`. Nilai `created_at` pesan adalah timestamp commit: pesan berurutan dapat berbagi timestamp atau sedikit terbalik, jadi pertahankan urutan yang dikembalikan alih-alih mengurutkan ulang berdasarkan `created_at`. Pada sesi milik agen, `sent_by_user_id` mencatat pengguna yang mengirim pesan pengguna tertentu ketika dapat diatribusikan; nilainya `null` jika tidak, termasuk pada semua pesan asisten. Ketika konten pesan tidak dapat dikembalikan sama sekali (misalnya, melebihi batas ukuran), pesan memiliki `content_unavailable` diatur ke `true`.

Dua parameter membatasi berapa byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default 10.000 byte. Teruskan `-1` untuk maksimum server (sekitar 1 MiB per string); `0` mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Blok yang terpotong oleh salah satu batas memiliki `"truncated": true`, dan input `tool_use` yang terpotong bukan lagi JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batasnya dan ambil ulang).

Endpoint messages mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) untuk sesi `pending`, sesi yang tidak ada atau telah dihapus, dan sesi di organisasi yang tidak dapat dibaca kunci Anda.

## Retensi dan penghapusan

Endpoint sesi bersifat hanya-baca. Sesi lokal dan jarak jauh tidak dapat dihapus melalui Compliance API. Secara default, transkrip sesi lokal disimpan selama 6 tahun, atau selama periode retensi percakapan kustom organisasi Anda jika periode terbatas telah ditetapkan, sebagaimana dijelaskan di bagian [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Transkrip sesi jarak jauh disimpan selama 6 tahun, kecuali pengguna menghapus sesi tersebut lebih awal. Setelah pengguna menghapus sebuah sesi, endpoint sesi jarak jauh tidak lagi mengembalikan sesi tersebut, dan transkripnya tidak dapat dipulihkan melalui Compliance API. Untuk mempelajari bagaimana periode-periode ini berkaitan dengan pengaturan retensi Anthropic lainnya, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengambil dan menghapus chat, file, dan proyek" href="https://platform.claude.com/docs/id/manage-claude/compliance-content-data">
    Akses konten chat claude.ai, lampiran file, dan proyek dengan Compliance Access Key yang sama.
  </Card>

  <Card title="FAQ Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention">
    Ringkasan per bidang tentang apa saja yang tercakup dalam transkrip sesi, serta pertanyaan umum lainnya.
  </Card>

  <Card title="Menangani error Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-errors">
    Payload error secara verbatim dan perbaikan untuk masing-masingnya.
  </Card>

  <Card title="Referensi API" href="https://platform.claude.com/docs/id/api/compliance/apps">
    Path endpoint, parameter, dan skema respons untuk Compliance API.
  </Card>
</CardGroup>
