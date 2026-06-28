---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/analytics-api
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: cfda885d8ea5c0c1c218b1686845690d9e2898d7fad99f2067d0bf293e289dab
---

# API Analitik

Pahami API analitik dan kunci API mana yang dibutuhkan organisasi Anda, lalu sediakan akses ke metrik produktivitas Claude Code atau data keterlibatan dan adopsi Claude Enterprise.

---

Anthropic menyediakan dua API analitik, dan API mana yang Anda gunakan bergantung pada produk Claude mana yang dikelola organisasi Anda:

* **Claude Code Analytics API** melaporkan metrik produktivitas Claude Code harian untuk organisasi yang menggunakan Claude Platform. API ini merupakan bagian dari [Admin API](/docs/id/manage-claude/admin-api) dan menggunakan kunci Admin API.
* **Claude Enterprise Analytics API** melaporkan data keterlibatan, adopsi, dan biaya di seluruh organisasi untuk berbagai produk Claude (chat, projects, Claude Code, dan lainnya) bagi organisasi Claude Enterprise. API ini menggunakan kunci Analytics API yang dibuat di claude.ai.

Kedua API menggunakan jenis kunci yang berbeda, dibuat di tempat yang berbeda oleh peran yang berbeda. Halaman ini menjelaskan API mana yang sesuai dengan organisasi Anda dan cara membuat kunci yang tepat.

## API mana yang Anda butuhkan?

| API                                 | Jenis kunci                            | Dibuat di                                                                                 | Siapa yang dapat membuatnya | Cakupan                                                                                                                                                                       |
| ----------------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code Analytics API**       | Kunci Admin API (`sk-ant-admin01-...`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | Admin organisasi            | Metrik Claude Code harian per pengguna: sesi, baris kode, commit, pull request, penerimaan alat, dan estimasi biaya berdasarkan model                                         |
| **Claude Enterprise Analytics API** | Kunci Analytics API                    | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Primary owner               | Keterlibatan dan adopsi di seluruh organisasi (aktivitas pengguna, ringkasan pengguna aktif, penggunaan project, skill, dan connector), ditambah laporan biaya dan penggunaan |

Jenis kunci ini tidak dapat dipertukarkan: kunci Admin API tidak dapat memanggil Claude Enterprise Analytics API, dan kunci Analytics API tidak dapat memanggil Admin API. Kedua API muncul di bawah [referensi Admin API](/docs/id/api/admin), tetapi keduanya adalah API terpisah dengan jenis kunci terpisah. Jika organisasi Anda menggunakan Claude Platform dan Claude Enterprise, Anda dapat menyediakan kedua kunci dan menggunakan masing-masing API untuk datanya sendiri.

<Note>
  Mencari data penggunaan dan biaya API alih-alih analitik produk? Lihat [Usage and Cost API](/docs/id/manage-claude/usage-cost-api), yang menjelaskan jalur yang tepat untuk organisasi Claude Console maupun Claude Enterprise.
</Note>

<Note>
  Jika Anda ingin melihat data keterlibatan dan adopsi di dalam produk alih-alih secara terprogram, gunakan [dasbor Analytics](https://claude.ai/analytics/activity) di claude.ai. Untuk kasus penggunaan tata kelola dan audit (tindakan pengguna individual, peristiwa aktivitas mentah, konten percakapan), lihat [Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

## Mendapatkan akses ke Claude Code Analytics API

Claude Code Analytics API tersedia untuk setiap organisasi yang memiliki akses ke [Admin API](/docs/id/manage-claude/admin-api), dan gratis untuk digunakan.

<Steps>
  <Step title="Buat kunci Admin API">
    Ikuti langkah-langkah di [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization).
  </Step>

  <Step title="Panggil API">
    Kirimkan kunci tersebut di header `x-api-key`:

    ```bash
    curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?starting_at=2025-09-08" \
      --header "anthropic-version: 2023-06-01" \
      --header "x-api-key: $ADMIN_API_KEY"
    ```
  </Step>
</Steps>

Untuk metrik yang tersedia, parameter permintaan, dan skema respons, lihat [panduan Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api) dan [referensi API](/docs/id/api/admin/usage_report/retrieve_claude_code).

## Mendapatkan akses ke Claude Enterprise Analytics API

Claude Enterprise Analytics API tersedia untuk organisasi Claude Enterprise. Data keterlibatan dan adopsi tersedia di semua paket Enterprise. Endpoint biaya dan penggunaan berlaku untuk paket Enterprise berbasis penggunaan; untuk paket Enterprise berbasis seat, endpoint tersebut hanya mencerminkan kredit penggunaan.

<Steps>
  <Step title="Masuk sebagai primary owner">
    Hanya primary owner organisasi yang dapat mengaktifkan akses API dan membuat kunci Analytics API.
  </Step>

  <Step title="Aktifkan akses API dan buat kunci">
    Buka [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) dan aktifkan akses API publik, lalu buat kunci Analytics API. Kunci memiliki scope `read:analytics`. Salin secret yang ditampilkan dan simpan di secrets manager Anda.
  </Step>

  <Step title="Panggil API">
    Kirimkan kunci tersebut di header `x-api-key`. Endpoint berada di bawah `https://api.anthropic.com/v1/organizations/analytics/`. Untuk contoh permintaan, parameter, dan skema respons, lihat [referensi Claude Enterprise Analytics API](/docs/id/api/admin/analytics).
  </Step>
</Steps>

Claude Enterprise Analytics API menyediakan:

* **Aktivitas pengguna:** metrik harian per pengguna di seluruh chat (percakapan, pesan, project, file, artifact), Claude Code (sesi, commit, pull request, baris kode, tindakan alat), dan produk Claude lainnya
* **Ringkasan aktivitas:** pengguna aktif harian, mingguan, dan bulanan di tingkat organisasi, jumlah seat, dan undangan yang tertunda
* **Penggunaan project, skill, dan connector:** rincian adopsi untuk project chat, skill, dan connector
* **Laporan biaya dan penggunaan:** penggunaan token dan biaya per pengguna serta tingkat organisasi dari waktu ke waktu (paket Enterprise berbasis penggunaan)

Untuk detail endpoint, parameter, dan skema respons, lihat [referensi Claude Enterprise Analytics API](/docs/id/api/admin/analytics). Bagian berikut membahas kesegaran data, definisi metrik, dan panduan operasional yang berlaku di seluruh endpoint tersebut.

## Ketersediaan dan kesegaran data

Data Claude Enterprise Analytics API tersedia untuk tanggal pada atau setelah 1 Januari 2026.

**Endpoint keterlibatan dan adopsi** (aktivitas pengguna, ringkasan, project, skill, connector) mengembalikan snapshot per hari untuk tanggal yang Anda tentukan. Data untuk hari tertentu diagregasi pada pukul 10UTC hari berikutnya dan tersedia untuk dikueri tiga hari setelah agregasi. Jika data tidak tersedia dalam jangka waktu tersebut, biasanya ini menunjukkan kegagalan pipeline data di sisi Anthropic; hubungi dukungan jika kesenjangan tersebut berlanjut.

**Endpoint biaya dan penggunaan** mengikuti model kesegaran yang berbeda. Data biasanya tersedia dalam waktu empat jam setelah penggunaan yang mendasarinya, tetapi dapat memakan waktu hingga 24 jam. Nilai untuk tanggal tertentu dapat direvisi hingga 30 hari seiring datangnya peristiwa yang terlambat dan berjalannya rekonsiliasi. Untuk total setingkat faktur, kueri tanggal setidaknya 30 hari ke belakang.

<Note>
  Respons biaya dan penggunaan menyertakan timestamp `data_refreshed_at`. Ketika `ending_at` dihilangkan (defaultnya adalah waktu saat ini), respons menyertakan ekor data setelah `data_refreshed_at` yang belum lengkap. Untuk hasil yang stabil di seluruh panggilan berulang, atur `ending_at` ke nilai pada atau sebelum `data_refreshed_at` yang dikembalikan sebelumnya.
</Note>

## Bagaimana metrik didefinisikan

**Pengguna aktif.** Seorang pengguna dihitung sebagai aktif untuk suatu hari jika salah satu dari kondisi berikut terpenuhi: mereka mengirim setidaknya satu pesan chat di Claude, mereka memiliki setidaknya satu sesi Claude Code (lokal atau remote) yang terkait dengan organisasi Claude Enterprise Anda yang mencakup penggunaan alat atau aktivitas git, atau mereka memiliki setidaknya satu sesi Cowork dengan penggunaan alat atau aktivitas pesan.

**Blok metrik per produk.** Objek metrik per produk (misalnya, metrik Office Agent atau Cowork pada record aktivitas pengguna) selalu ada di setiap record. Organisasi tanpa penggunaan produk tersebut akan melihat nilai nol semua, bukan `null`.

**Nama connector.** Nama connector dinormalisasi di seluruh sumber. Misalnya, `Atlassian MCP server`, `mcp-atlassian`, dan `atlassian_MCP` semuanya muncul sebagai `atlassian` di endpoint penggunaan connector.

## Bekerja dengan API

**Kursor paginasi terikat pada kueri yang menerbitkannya.** Pada endpoint biaya dan penggunaan, jangan mengubah parameter kueri di tengah urutan: jika Anda mengubah `products[]`, `group_by[]`, `order_by`, rentang tanggal, atau filter apa pun dan meneruskan kursor lama, permintaan akan mengembalikan error 400. Untuk mengubah parameter, mulai ulang dari halaman pertama tanpa kursor.

**Parameter list menggunakan notasi kurung siku.** Ulangi parameter untuk setiap nilai, misalnya `products[]=chat&products[]=claude_code`.

**Field jumlah adalah string desimal dalam sen.** Jumlah mata uang dikembalikan sebagai string desimal seperti `"41280.000000"` (yang mewakili $412,80). Untuk mengonversi ke dolar, parse sebagai desimal dan bagi dengan 100. Hindari parsing floating-point biner untuk nilai yang mungkin melebihi beberapa juta dolar.

**Batas laju berlaku di tingkat organisasi**, bukan per kunci, dengan default 60 permintaan per menit di seluruh endpoint dalam API ini. Jika itu tidak cukup untuk kasus penggunaan Anda, hubungi tim akun Anthropic Anda untuk mendiskusikan penyesuaian batas tersebut.

## Keterbatasan yang diketahui

Jika organisasi Anda menggunakan Claude Code melalui Amazon Bedrock, Claude Enterprise Analytics API tidak mengembalikan aktivitas Claude Code untuk penggunaan tersebut.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Claude Code Analytics API" href="/docs/id/manage-claude/claude-code-analytics-api">
    Lacak sesi Claude Code, perubahan kode, dan penggunaan alat dengan kunci Admin API.
  </Card>

  <Card title="Usage and Cost API" href="/docs/id/manage-claude/usage-cost-api">
    Lacak penggunaan token API dan biaya untuk organisasi Anda.
  </Card>

  <Card title="Referensi Claude Enterprise Analytics API" href="/docs/id/api/admin/analytics">
    Referensi endpoint untuk data keterlibatan, adopsi, dan biaya.
  </Card>

  <Card title="Mendapatkan akses ke Compliance API" href="/docs/id/manage-claude/compliance-api-access">
    Data audit dan kepatuhan menggunakan jenis kuncinya sendiri.
  </Card>
</CardGroup>
