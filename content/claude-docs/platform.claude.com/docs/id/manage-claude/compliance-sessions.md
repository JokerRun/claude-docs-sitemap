---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-sessions
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 4338a9d15dbc7d1ef94cdc2773b4cc5d28cf1731a9a30b4b915fc723767a678b
---

---
title: Mengambil transkrip sesi
url: https://platform.claude.com/docs/id/manage-claude/compliance-sessions
description: Daftarkan sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Claude Cowork dan Claude Code, dan ambil transkripnya melalui Compliance API.
---

<Note>
  Endpoint di halaman ini hanya tersedia untuk organisasi Claude Enterprise dan masih dalam versi beta. Endpoint ini bekerja dengan Compliance Access Key dan scope `read:compliance_user_data` yang sama seperti [endpoint chat, file, dan proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data); tidak diperlukan kunci, scope, pengaturan, atau pembaruan klien baru. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key.

  **Prasyarat:** Tidak ada untuk mendaftarkan sesi di seluruh organisasi. Untuk memfilter daftar sesi remote (sesi di cloud) ke pengguna tertentu, Anda memerlukan ID pengguna dari [Daftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users); daftar sesi lokal tidak memiliki filter pengguna.
</Check>

Endpoint di halaman ini mengekspos transkrip sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude (saat ini, Cowork dan Claude Code) dari organisasi Claude Enterprise Anda kepada peninjau kepatuhan. Setiap sesi adalah satu percakapan dengan Claude; transkripnya adalah urutan prompt pengguna, respons asisten, serta pemanggilan alat dan hasilnya dalam percakapan tersebut. Endpoint ini mendukung ekspor "eDiscovery" (penemuan elektronik) dan penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP.

Compliance API mengelompokkan sesi ke dalam dua keluarga endpoint berdasarkan tempat sesi tersebut berjalan: endpoint sesi lokal untuk sesi di mesin pengguna, dan endpoint sesi remote untuk sesi yang berjalan di cloud dalam lingkungan yang dikelola Anthropic. Kedua keluarga bersifat read-only, dan tidak satu pun tersedia untuk kunci Admin API (`sk-ant-admin01-...`): panggilan yang diautentikasi dengan kunci Admin API mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Tabel berikut memetakan setiap produk, dan tempat produk tersebut berjalan, ke keluarga endpoint yang mengembalikan sesinya serta nilai `product_surface` yang mengidentifikasinya dalam respons. Produk ditambahkan ke tabel ini seiring bertambahnya cakupan.

| Produk dan tempat berjalannya                                                                                     | Keluarga endpoint                                            | `product_surface` |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------- |
| Cowork di Claude Desktop, berjalan di mesin pengguna                                                              | Endpoint sesi lokal (`/v1/compliance/apps/sessions/local`)   | `cowork`          |
| Claude Code di terminal, di Claude Desktop, atau di ekstensi IDE, berjalan di mesin pengguna                      | Endpoint sesi lokal                                          | `claude_code`     |
| Sesi Cowork yang dimulai di claude.ai web atau mobile, berjalan di cloud dalam lingkungan yang dikelola Anthropic | Endpoint sesi remote (`/v1/compliance/apps/sessions/remote`) | `cowork_remote`   |

Perekaman sesi lokal terikat pada diaktifkannya Compliance API untuk organisasi Anda dan berlaku selama pengguna masuk dengan akun Claude Enterprise mereka. Endpoint sesi tidak mengembalikan hal-hal berikut:

* Sesi Claude Code yang diautentikasi dengan kunci API Claude Console, atau dijalankan melalui platform cloud pihak ketiga seperti Amazon Bedrock, Google Cloud, atau Microsoft Foundry.
* Claude Code di web. Produk ini juga berjalan di cloud dalam lingkungan yang dikelola Anthropic, tetapi bukan merupakan sesi remote; endpoint sesi remote hanya mengembalikan sesi Cowork.
* Sesi lokal di organisasi yang mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness). Tidak ada data sesi lokal yang direkam, sehingga endpoint sesi lokal tidak mengembalikan sesi apa pun untuk organisasi tersebut.
* Sesi lokal yang tunduk pada [zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope). Sesi ini dikecualikan dari hasil daftar, dan endpoint retrieve serta messages mengembalikan 404 untuk sesi tersebut.

Anthropic merekomendasikan Compliance API untuk mengambil konten sesi Cowork dan Claude Code. Tabel berikut membandingkan [sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) dan [sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) dengan alternatif berbasis OpenTelemetry, yaitu [logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage).

|                                                              | Sesi lokal (di mesin pengguna)                                                                                                                                               | Sesi remote (di cloud)                                                                                                                                                       | Logging OpenTelemetry                                                                                                                |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Pengiriman                                                   | Pull: kueri dan ekspor melalui HTTPS                                                                                                                                         | Pull: kueri dan ekspor melalui HTTPS                                                                                                                                         | Push: di-streaming ke kolektor OTLP Anda                                                                                             |
| Penyiapan                                                    | Berfungsi dengan Compliance Access Key Anda yang sudah ada                                                                                                                   | Berfungsi dengan Compliance Access Key Anda yang sudah ada                                                                                                                   | Admin mengonfigurasi endpoint OTLP dan pengaturan penangkapan konten                                                                 |
| Infrastruktur                                                | Di-hosting oleh Anthropic                                                                                                                                                    | Di-hosting oleh Anthropic                                                                                                                                                    | Anda menjalankan kolektor dan penyimpanan                                                                                            |
| Prefiks ID                                                   | `clls_`                                                                                                                                                                      | `cse_`                                                                                                                                                                       | N/A                                                                                                                                  |
| Nilai `product_surface`                                      | `cowork`, `claude_code`                                                                                                                                                      | `cowork_remote`                                                                                                                                                              | N/A                                                                                                                                  |
| Retensi                                                      | 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda jika periode terbatas ditetapkan; disimpan oleh Anthropic                                     | 6 tahun, disimpan oleh Anthropic                                                                                                                                             | Infrastruktur Anda, kebijakan Anda                                                                                                   |
| Prompt pengguna dan respons asisten                          | Ya                                                                                                                                                                           | Ya                                                                                                                                                                           | Ya, tergantung pengaturan penangkapan konten                                                                                         |
| Input alat                                                   | Dipotong hingga 10.000 byte per input secara default; hingga sekitar 1 MiB atas permintaan                                                                                   | Dipotong hingga 10.000 byte per input secara default; hingga sekitar 1 MiB atas permintaan                                                                                   | Ringkasan yang dipotong                                                                                                              |
| Konten hasil alat                                            | Setiap entri teks dipotong hingga 10.000 byte secara default; hingga sekitar 1 MiB atas permintaan                                                                           | Setiap entri teks dipotong hingga 10.000 byte secara default; hingga sekitar 1 MiB atas permintaan                                                                           | Metadata seperti ukuran dan keberhasilan; Claude Code juga dapat menangkap konten dengan pengaturan opsional yang dibatasi ukurannya |
| Konten file                                                  | Ya, melalui pemanggilan alat dalam transkrip (hanya teks; konten lain muncul sebagai placeholder)                                                                            | Ya, melalui pemanggilan alat dalam transkrip (hanya teks; konten lain dihilangkan)                                                                                           | Path file; Claude Code juga dapat menangkap konten dengan pengaturan opsional yang dibatasi ukurannya                                |
| Metadata host dan perangkat (jenis terminal, path workspace) | Tidak                                                                                                                                                                        | Tidak                                                                                                                                                                        | Ya                                                                                                                                   |
| Penggunaan token dan biaya                                   | Tidak; tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api) | Tidak; tersedia melalui [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api) | Ya                                                                                                                                   |

## Sesi di mesin pengguna (sesi lokal)

Sesi lokal berjalan di mesin pengguna selama mereka masuk dengan akun Claude Enterprise mereka: saat ini, Cowork di Claude Desktop, dan Claude Code di terminal, di Claude Desktop, atau di ekstensi IDE.

Compliance API mengekspos sesi lokal melalui tiga endpoint: `GET /v1/compliance/apps/sessions/local` mendaftarkan metadata sesi, `GET /v1/compliance/apps/sessions/local/{session_id}` mengambil metadata satu sesi, dan `GET /v1/compliance/apps/sessions/local/{session_id}/messages` mengembalikan transkrip satu sesi. Ketiganya memerlukan scope `read:compliance_user_data` dan hanya dihitung terhadap "rate limit" (batas laju) Compliance API bersama; ketiganya tidak tunduk pada anggaran permintaan kedua yang berlaku untuk endpoint sesi remote. Lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests). Jika sesi lokal tidak tersedia untuk organisasi induk Anda, ketiga endpoint mengembalikan 404 dengan pesan `Local sessions are not available.` (lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found)); sementara daftar sesi atau konten yang direkam tidak tersedia untuk sementara, endpoint tersebut mengembalikan 503 (lihat [Sesi lokal tidak tersedia untuk sementara](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable)).

Untuk sesi lokal, Anthropic merekam setiap percakapan di sisi server saat permintaannya mencapai Claude API; tidak ada yang diinstal di perangkat, dan tidak ada yang dikumpulkan di luar permintaan yang sudah dikirim klien ke Claude API. Transkrip sesi lokal menunjukkan apa yang diminta untuk dilakukan Claude dan apa yang dikembalikannya, bukan apa yang terjadi di perangkat. Aktivitas file dan jaringan hanya terlihat melalui pemanggilan alat dan hasil alat dalam transkrip, sehingga aktivitas yang tidak pernah mencapai API (misalnya, file lokal yang tidak pernah dikirim oleh sesi) tidak direkam.

Di organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek), sesi lokal didaftarkan dan dapat diambil seperti biasa, tetapi konten transkrip saat ini tidak dikembalikan; setiap pesan dikembalikan dengan kontennya ditandai tidak tersedia (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript) untuk cara pesan tersebut ditandai).

Endpoint list mengembalikan metadata sesi, tanpa konten transkrip, untuk setiap organisasi tertaut yang dapat dibaca kunci Anda. Tidak seperti daftar sesi remote, endpoint ini tidak memiliki filter organisasi atau pengguna: batasi hasil berdasarkan waktu dengan parameter `created_at.gte` dan `created_at.lt`. Keduanya menerima timestamp RFC 3339 dengan offset UTC yang wajib, dan ketika keduanya diberikan, `created_at.lt` harus benar-benar setelah `created_at.gte` atau permintaan mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Filter waktu ketiga, `updated_at.gte`, membatasi berdasarkan aktivitas terakhir alih-alih yang pertama: filter ini mengembalikan sesi yang panggilan inferensi terakhirnya berada pada atau setelah waktu yang diberikan dan dapat digabungkan dengan filter `created_at` tanpa mengubah urutan atau paginasi. Gunakan filter ini untuk melakukan polling sesi yang aktif sejak eksekusi sebelumnya, seperti dijelaskan nanti di bagian ini. Sesi dan pesan baru muncul dalam hasil setelah penundaan pemrosesan singkat, biasanya dalam hitungan menit; sesi yang tidak ada segera setelah dimulai belum tentu tidak direkam. Permintaan berikut mendaftarkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
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

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at`, dengan nilai yang sama diurutkan dalam urutan tetap di sisi server, dan dibatasi hingga `limit` hasil per respons (default 100, maks 500). Endpoint ini hanya melakukan paginasi maju dengan token `page` dan `next_page` (lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)): teruskan nilai `next_page` dari respons sebagai parameter query `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`. Respons tidak memiliki field `has_more`. Selesaikan penelusuran daftar dalam 24 jam sejak memulainya; kursor daftar yang lebih lama masih diterima tetapi dievaluasi ulang terhadap batas retensi saat ini, sehingga sesi yang aktivitas tertua yang masih disimpannya akan segera melewati periode retensi dapat terlewati.

Dalam setiap objek sesi, `user.id` selalu terisi dan tetap ada setelah penghapusan akun; `user.email_address` bernilai `null` ketika akun pengguna telah dihapus atau pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca kunci Anda. `workspace_id` bernilai `null` ketika sesi tidak terkait dengan workspace. Sesi lokal berkorespondensi dengan satu ID sesi klien: memulai percakapan baru di klien, atau menghapus konteksnya, memulai catatan sesi baru. Perlakukan nilai `id` sebagai string opaque; formatnya dapat berubah tanpa pemberitahuan.

Sesi lokal memiliki `updated_at` tetapi tidak memiliki `status`: sesi lokal tidak memiliki status siklus hidup di sisi server, dan visibilitasnya diatur oleh retensi. Sesi lokal direkam sebagai rangkaian panggilan Claude API (panggilan inferensi) yang dibuat klien selama sesi, dan retensi berlaku untuk setiap panggilan yang direkam secara individual. `created_at` adalah timestamp panggilan tertua yang masih disimpan dari sesi tersebut dan `updated_at` adalah timestamp panggilan terakhirnya, keduanya UTC. Saat panggilan yang lebih lama melewati periode retensi, `created_at` bergeser maju sesuai dengan itu, dan setelah setiap panggilan dalam sesi telah kedaluwarsa, sesi tidak lagi dikembalikan; `updated_at` melacak panggilan terbaru dan tidak terpengaruh hingga saat itu. Karena `created_at` dapat bergeser antar-eksekusi, lakukan deduplikasi berdasarkan `id` ketika Anda menelusuri ulang daftar dari waktu ke waktu. Untuk menjaga transkrip tetap mutakhir saat sesi mendapatkan pesan baru, lakukan polling dengan filter `updated_at.gte`, dengan jendela berurutan yang saling tumpang tindih. Pada endpoint list, `updated_at` adalah batas bawah: untuk sesi yang masih aktif pada batas halaman atau batas jendela `created_at.lt`, nilainya dapat sesaat tertinggal dari aktivitas terakhir sesi yang sebenarnya, dan panggilan baru hanya dapat dikueri setelah penundaan pemrosesan singkat yang disebutkan sebelumnya. Karena ketertinggalan itu, pada setiap eksekusi tetapkan `updated_at.gte` beberapa menit sebelum waktu mulai eksekusi sebelumnya, bukan tepat pada waktu eksekusi sebelumnya. Batas yang ditetapkan tepat pada waktu sebelumnya secara diam-diam dan permanen menghilangkan sesi yang panggilan terakhirnya masih diindeks pada saat itu, karena setelah batas bergerak melewati panggilan tersebut, tidak ada eksekusi berikutnya yang mengembalikannya. Lakukan deduplikasi sesi yang dikembalikan berdasarkan `id`, ambil ulang transkripnya, dan lakukan deduplikasi pesan berdasarkan `id`. Mengambil sesi, atau pesannya, selalu mencerminkan secara tepat panggilan terbaru yang masih disimpan, sehingga proses rekonsiliasi berkala atas jendela yang lebih lama dapat menjadi pengaman tambahan sebagai alternatif dari memperlebar tumpang tindih.

Daftar ini dibangun dari metadata aktivitas sesi, sehingga dapat mencakup sesi yang konten transkripnya tidak direkam, misalnya sesi yang berjalan sebelum perekaman dimulai untuk organisasi Anda (sejauh yang diizinkan periode retensi Anda); transkrip sesi semacam itu mengembalikan setiap pesan dengan kontennya ditandai tidak tersedia (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript)).

Konten sesi lokal yang direkam disimpan selama 6 tahun sejak perekaman secara default. Jika organisasi yang menjalankan sesi telah menetapkan periode retensi percakapan kustom yang terbatas di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), periode tersebut yang berlaku, baik lebih pendek maupun lebih panjang dari default; ketika organisasi memiliki lebih dari satu periode retensi kustom yang dikonfigurasi, periode terpendek yang berlaku. Perubahan pada pengaturan tersebut berlaku dengan dua cara berbeda: endpoint berhenti mengembalikan aktivitas yang lebih lama dari periode organisasi saat ini segera setelah pengaturan berubah, sedangkan setiap pesan yang direkam disimpan selama periode yang berlaku saat pesan tersebut direkam, sehingga memperpanjang periode di kemudian hari tidak memulihkan konten yang sudah kedaluwarsa.

Untuk mengambil metadata satu sesi secara langsung, teruskan ID-nya ke `GET /v1/compliance/apps/sessions/local/{session_id}`. Responsnya adalah objek sesi yang sama dengan yang dikembalikan endpoint list, tanpa envelope dan tanpa konten transkrip. ID sesi yang salah format mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Satu [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) mencakup empat kasus yang tidak dibedakan oleh respons: sesi tidak berada di organisasi yang dapat dibaca kunci Anda (termasuk sesi di bawah organisasi induk lain), sesi tidak ada, zero data retention berlaku untuknya, atau setiap panggilan di dalamnya telah melewati retensi.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi: `cowork` untuk sesi Cowork yang berjalan di mesin pengguna di Claude Desktop, dan `claude_code` untuk sesi Claude Code. Nilai baru muncul seiring bertambahnya cakupan.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan handler Anda, sehingga integrasi Anda tetap berfungsi saat product surface baru dirilis.
</Note>

### Mengambil transkrip sesi lokal

Endpoint messages mengembalikan transkrip sesi, yang direkonstruksi dari panggilan Claude API yang direkam: prompt pengguna, teks asisten, pemanggilan alat, dan bagian teks dari hasil alat, semuanya dikembalikan sebagaimana dikirim kecuali pemotongan ukuran. Tidak ada yang menyamarkan URL, kredensial, atau data pribadi dalam konten tersebut, jadi perlakukan transkrip sebagai data sensitif. Transkrip menghilangkan atau mengganti hal-hal berikut:

* Blok thinking tidak pernah disertakan.
* "System prompt" (prompt sistem) dari permintaan tidak pernah dikembalikan. Pesan penanda bertuliskan `[system prompt content not shown]` menggantikannya (biasanya sekali per sesi; sesi tanpa konten yang direkam tidak memiliki penanda).
* Definisi alat dan konfigurasi server MCP bukan bagian dari transkrip.
* Gambar, PDF, dan blok biner atau terstruktur lainnya tidak dikembalikan. Masing-masing muncul sebagai blok `text` bertuliskan `[<block type> content not shown]` (misalnya, `[image content not shown]`) dengan `truncated` diatur ke `true`. Item non-teks di dalam hasil alat diganti dengan satu entri `[N non-text item(s) not shown]`, dan `truncated` pada blok hasil alat bernilai `true`.
* Metadata sitasi pada blok `text` dihilangkan, dan blok yang terpengaruh memiliki `truncated` diatur ke `true`.

File instruksi proyek seperti `CLAUDE.md` muncul sebagai konten role user biasa. Konten skill muncul ketika klien mengirimkannya sebagai konten pesan dan tidak dibedakan dari teks pengguna lainnya. Untuk ringkasan cakupan, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention); untuk tabel yang membandingkan sesi lokal dengan sesi remote dan logging OpenTelemetry, lihat pengantar halaman ini.

```bash cURL
session_id="clls_01HxKpLmNoPqRsTuVwXyZaBc"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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
      "model": "claude-opus-5",
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
      "model": "claude-opus-5",
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

Respons menyematkan envelope `session` di samping array `data` yang dipaginasi. Catatan pertama dalam contoh ini adalah penanda yang menggantikan prompt sistem dari permintaan; `provenance`-nya dijelaskan nanti di bagian ini. Pada endpoint ini `user.email_address` selalu `null`: endpoint messages tidak me-resolve alamat email, sehingga `null` di sini tidak berarti akun pengguna telah dihapus. Untuk mengatribusikan sesi ke alamat email, gabungkan `user.id` dengan [endpoint list](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) atau endpoint retrieve (`GET /v1/compliance/apps/sessions/local/{session_id}`).

Pesan dikembalikan dari yang terlama lebih dulu secara default; teruskan `order=desc` untuk membalik urutan. Paginasi menggunakan skema `page`/`next_page` yang sama dengan endpoint list, dengan default `limit` 100 dan maks 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai batas ukurannya, sehingga halaman dengan pesan kurang dari `limit` tidak berarti Anda telah mencapai akhir; teruslah melakukan paginasi hingga `next_page` bernilai `null`. Kursor halaman terikat pada sesi dan urutan sortir tempat kursor tersebut diterbitkan, dan kursor suatu penelusuran kedaluwarsa 24 jam setelah halaman pertamanya: kursor yang kedaluwarsa mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) yang memberi tahu Anda untuk memulai ulang tanpa parameter `page`, dan penelusuran yang dimulai ulang mencerminkan batas retensi saat ini. Kursor yang diterbitkan untuk sesi atau `order` yang berbeda juga mengembalikan 400, sebagai kursor tidak valid.

Setiap pesan memiliki `role` (`user` atau `assistant`) dan array `content` berisi blok `text`, `tool_use`, dan `tool_result`. Pesan juga memiliki `model`: pada giliran asisten yang direkam dari Claude API, ini adalah model yang melayani giliran tersebut, dan bernilai `null` pada pesan pengguna dan pada pesan asisten mana pun yang `provenance`-nya diisi, karena riwayat yang dinyatakan klien dan penanda sintetis tidak dihasilkan oleh model dan model yang melayani tidak diketahui untuk konten yang tidak tersedia. Blok `text` memiliki `text` dan `truncated`. Blok `tool_use` memiliki `id`, `name`, `input`, dan `truncated`, di mana `input` adalah string berenkode JSON, bukan objek. Blok `tool_result` memiliki `tool_use_id`, `name`, `is_error`, array `content` berisi entri `text`, dan `truncated`. Pemanggilan dan hasil alat MCP, serta sebagian besar pemanggilan dan hasil server tool, dinormalisasi ke dalam bentuk `tool_use` dan `tool_result` yang sama ini; jenis blok lainnya muncul sebagai placeholder `[<block type> content not shown]`. `id` pesan stabil selama giliran tersebut masih disimpan. Setiap pesan yang direkonstruksi dari panggilan inferensi yang sama memiliki timestamp panggilan tersebut, sehingga pesan berurutan sering berbagi nilai `created_at`; pertahankan urutan yang dikembalikan alih-alih mengurutkan ulang berdasarkan timestamp.

Setiap pesan juga memiliki field `provenance` yang menjelaskan bagaimana kontennya direkam. `provenance` bernilai `null` untuk konten terverifikasi yang direkam oleh Claude API, yang merupakan kasus umum. Jika tidak, field ini adalah objek yang `type`-nya menandai pengecualian:

* `content_unavailable` berarti konten tidak dapat dikembalikan. Array `content` kosong, dan `provenance.reason` menyatakan alasannya. `not_captured` berarti tidak ada konten yang tersedia untuk giliran tersebut; ini tidak membuktikan bahwa tidak ada catatan yang disimpan, karena konten yang ditahan oleh kebijakan akses di sisi penyimpanan dilaporkan dengan alasan yang sama (misalnya, di organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek#disabled-or-modified)), dan giliran individual dalam sesi yang selebihnya direkam dapat tidak tersedia karena alasan penanganan data lainnya dan memiliki alasan yang sama. `client_aborted` berarti klien menutup koneksi atau membatalkan permintaan sebelum respons selesai, sehingga respons giliran tersebut tidak direkam; output parsial apa pun yang sudah di-streaming ke klien tidak disertakan, dan alasan ini hanya berlaku untuk giliran role assistant. `cmek_key_revoked` dicadangkan untuk konten yang dienkripsi dengan kunci yang dikelola pelanggan milik organisasi Anda ketika kunci tersebut tidak tersedia (misalnya, dicabut); alasan ini saat ini tidak dikembalikan, jadi tangani untuk kompatibilitas ke depan. `retention_elapsed` berarti konten telah melewati retensi. `oversize` berarti satu pesan melebihi batas ukuran per pesan; pesan tetap dikembalikan, dengan array `content` kosong.
* `client_asserted` menandai pesan asisten yang diberikan klien sebagai riwayat percakapan dan yang tidak dapat dicocokkan dengan respons yang direkam; kepengarangannya tidak terverifikasi.
* `synthetic_marker` menandai catatan yang dihasilkan oleh endpoint itu sendiri, seperti penanda yang menggantikan prompt sistem. Ketika klien menulis ulang atau memadatkan riwayat percakapannya di tengah sesi (misalnya, setelah pemadatan konteks), transkrip menyisipkan pesan penanda pada titik tersebut dan melanjutkan dengan konten baru yang dikirim klien; ketika organisasi Anda memiliki periode retensi terbatas, riwayat yang ditulis ulang itu sendiri ditahan (penanda kedua mencatat hal ini) dan hanya giliran pengguna terbaru dan yang mengikutinya yang ditampilkan.

Pesan penanda dan pesan client-asserted dimulai dengan blok `text` penjelasan dalam kurung siku yang ditandai `truncated: true`, misalnya `[system prompt content not shown]`. Perlakukan catatan ini sebagai ada tetapi tidak tersedia atau tidak terverifikasi, bukan hilang, dan toleransi tipe dan alasan `provenance` yang tidak dikenali.

Dua parameter membatasi berapa byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default 10.000 byte. Teruskan `-1` untuk maksimum server (sekitar 1 MiB per string); `0` mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request), dan nilai di atas maksimum dijepit ke nilai tersebut. String yang terpotong oleh salah satu batas dipotong pada batas karakter dan ditambahkan sufiks in-band (misalnya, `…[truncated; pass tool_result_max_bytes=-1 for the server max]`), dan bloknya memiliki `"truncated": true`. `input` `tool_use` yang terpotong karenanya bukan lagi JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batasnya dan ambil ulang). Blok bertipe `text` selalu dibatasi pada maksimum server yang sama sekitar 1 MiB; tidak ada parameter yang menaikkannya, dan blok `text` pada batas tersebut juga memiliki `"truncated": true`.

Konten transkrip mematuhi periode retensi yang dijelaskan di bawah [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Ketika awal sesi telah melewatinya, transkrip dimulai dengan satu placeholder `content_unavailable` dengan `reason` bernilai `retention_elapsed`, dan pesan yang masih disimpan mengikutinya. Ketika setiap panggilan dalam sesi telah kedaluwarsa, endpoint messages mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found), seperti halnya untuk sesi di organisasi yang tidak dapat dibaca kunci Anda, sesi yang tidak ada, dan sesi yang tunduk pada zero data retention. ID sesi yang salah format mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request).

## Sesi di cloud (sesi remote)

Sesi Cowork yang dimulai di claude.ai web atau mobile berjalan di cloud dalam lingkungan yang dikelola Anthropic. Compliance API mengekspos sesi remote ini melalui dua endpoint: `GET /v1/compliance/apps/sessions/remote` mendaftarkan metadata sesi, dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi. Keduanya memerlukan scope `read:compliance_user_data`, dan keduanya dihitung terhadap batas laju Compliance API bersama ditambah anggaran permintaan kedua yang khusus untuk endpoint ini; lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests).

Endpoint list secara default memiliki cakupan seluruh organisasi: hilangkan `organization_ids[]` untuk menyertakan setiap organisasi claude.ai yang dapat dibaca kunci Anda, atau teruskan hingga 500 nilai untuk mempersempit cakupan. Untuk membatasi daftar ke pengguna tertentu, teruskan 1–10 nilai `user_ids[]` (dapatkan ID dari [Daftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)); filter ini mencocokkan pengguna pemilik sesi, sehingga sesi milik agen dikecualikan setiap kali `user_ids[]` diatur. Batasi hasil berdasarkan waktu dengan parameter rentang `created_at` (`gte`, `gt`, `lt`, `lte`, dalam format RFC 3339). Tidak ada filter `updated_at`. Permintaan berikut mendaftarkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
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

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at` dan dibatasi hingga `limit` hasil per respons (default 100, maks 500). Endpoint ini melakukan paginasi dengan token `page` dan `next_page` (lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)): teruskan nilai `next_page` dari respons sebagai parameter query `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`.

Sebuah sesi dimiliki oleh pengguna atau agen, tidak pernah keduanya. Untuk sesi milik pengguna, `user` memuat ID dan alamat email pemilik (`email_address` bernilai `null` ketika pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca kunci Anda) dan `agent_id` bernilai `null`. Untuk sesi milik agen (misalnya, tugas terjadwal), `user` bernilai `null`, `agent_id` memuat ID agen (prefiks `cagt_`), dan `started_by_user` mengidentifikasi manusia yang memulai eksekusi, misalnya dengan memulai tugas terjadwal; pada sesi milik pengguna, `started_by_user` bernilai `null`.

`claude_project_id` adalah ID [proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-projects-and-attachments) claude.ai tempat sesi berada (prefiks `claude_proj_`), atau `null` ketika sesi tidak berada dalam proyek.

`status` adalah salah satu dari `pending`, `active`, `paused`, `archived`, atau `failed`. Sebuah sesi berstatus `pending` selama sedang diprovisikan; sesi `pending` belum memiliki transkrip, dan endpoint messages mengembalikan 404 untuknya hingga provisi selesai. Sesi yang telah dihapus tidak pernah dikembalikan.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi. Endpoint ini saat ini hanya mengembalikan sesi dengan `product_surface` bernilai `cowork_remote`: sesi Cowork yang dimulai di claude.ai web atau mobile.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `status` dan `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan handler Anda, sehingga integrasi Anda tetap berfungsi saat status dan product surface baru dirilis.
</Note>

### Mengambil transkrip sesi remote

Endpoint messages mengembalikan transkrip sesi: prompt pengguna, respons asisten, serta pemanggilan alat dan hasilnya. Blok thinking dan gambar tidak disertakan. Untuk ringkasan cakupan, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention); untuk tabel yang membandingkan sesi remote dengan sesi lokal dan logging OpenTelemetry Cowork, lihat pengantar halaman ini.

```bash cURL
session_id="cse_01WpQrStUvXyZaBcDeFgHjK6"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
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

Respons menyematkan envelope `session` di samping array `data` yang dipaginasi. Pada endpoint ini envelope selalu memiliki `user.email_address`, `started_by_user`, dan `claude_project_id` diatur ke `null`; dapatkan nilai-nilai tersebut dari endpoint list.

Pesan dikembalikan dari yang terlama lebih dulu secara default; teruskan `order=desc` untuk membalik urutan. Paginasi menggunakan skema `page`/`next_page` yang sama dengan endpoint list, dengan default `limit` 100 dan maks 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai batas ukurannya, sehingga halaman dengan pesan kurang dari `limit` tidak berarti Anda telah mencapai akhir; teruslah melakukan paginasi hingga `next_page` bernilai `null`.

Setiap pesan memiliki `role` (`user` atau `assistant`) dan array `content` berisi blok `text`, `tool_use`, dan `tool_result`. Nilai `created_at` pesan adalah timestamp commit: pesan berurutan dapat berbagi timestamp atau sedikit terbalik, jadi pertahankan urutan yang dikembalikan daripada mengurutkan ulang berdasarkan `created_at`. Pada sesi milik agen, `sent_by_user_id` mencatat pengguna yang mengirim pesan pengguna tertentu ketika dapat diatribusikan; nilainya `null` jika tidak, termasuk pada semua pesan asisten. Ketika konten pesan tidak dapat dikembalikan sama sekali (misalnya, melebihi batas ukuran), pesan memiliki `content_unavailable` diatur ke `true`.

Dua parameter membatasi berapa byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default 10.000 byte. Teruskan `-1` untuk maksimum server (sekitar 1 MiB per string); `0` mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Blok yang terpotong oleh salah satu batas memiliki `"truncated": true`, dan input `tool_use` yang terpotong bukan lagi JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batasnya dan ambil ulang).

Endpoint messages mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) untuk sesi `pending`, sesi yang tidak ada atau telah dihapus, dan sesi di organisasi yang tidak dapat dibaca kunci Anda.

## Retensi dan penghapusan

Endpoint sesi bersifat read-only; sesi lokal dan remote tidak dapat dihapus melalui Compliance API. Transkrip sesi lokal disimpan selama 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda jika periode terbatas ditetapkan, seperti dijelaskan di bawah [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Transkrip sesi remote disimpan selama 6 tahun. Untuk mengetahui bagaimana periode ini berdampingan dengan pengaturan retensi Anthropic lainnya, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengambil dan menghapus chat, file, dan proyek" href="https://platform.claude.com/docs/id/manage-claude/compliance-content-data">
    Akses konten chat claude.ai, lampiran file, dan proyek dengan Compliance Access Key yang sama.
  </Card>

  <Card title="FAQ Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention">
    Ringkasan field demi field tentang apa yang disertakan dalam transkrip sesi, dan pertanyaan umum lainnya.
  </Card>

  <Card title="Menangani error Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-errors">
    Payload error verbatim dan perbaikan untuk masing-masing.
  </Card>

  <Card title="Referensi API" href="https://platform.claude.com/docs/id/api/compliance/apps">
    Path endpoint, parameter, dan skema respons untuk Compliance API.
  </Card>
</CardGroup>
