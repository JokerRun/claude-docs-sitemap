---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 1a64537df2db62dad985345da7ed50afec92c039441813bd8da90a0863445ed3
---

# Claude Code Analytics API

Akses analitik penggunaan Claude Code dan metrik produktivitas organisasi Anda secara terprogram dengan Claude Code Analytics Admin API.

---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

Claude Code Analytics Admin API menyediakan akses terprogram ke metrik penggunaan agregat harian untuk pengguna Claude Code, memungkinkan organisasi menganalisis produktivitas pengembang dan membangun dasbor kustom. API ini memberikan detail lebih banyak daripada [dasbor Analytics](/claude-code) dasar tanpa kompleksitas integrasi OpenTelemetry.

API ini memungkinkan Anda untuk memantau, menganalisis, dan mengoptimalkan adopsi Claude Code Anda dengan lebih baik:

* **Analisis produktivitas pengembang:** Lacak sesi, baris kode yang ditambahkan/dihapus, commit, dan pull request yang dibuat menggunakan Claude Code
* **Metrik penggunaan alat:** Pantau tingkat penerimaan dan penolakan untuk berbagai alat Claude Code (Edit, MultiEdit, Write, NotebookEdit)
* **Analisis biaya:** Lihat estimasi biaya dan penggunaan token yang dirinci berdasarkan model Claude
* **Pelaporan kustom:** Ekspor data untuk membangun dasbor eksekutif dan laporan untuk tim manajemen
* **Justifikasi penggunaan:** Sediakan metrik untuk menjustifikasi dan memperluas adopsi Claude Code secara internal

<Check>
  **Kunci Admin API diperlukan.** Endpoint ini memerlukan kunci Admin API, yang berbeda dari kunci API Claude standar. Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys) untuk mengetahui tempat membuatnya sesuai jenis organisasi Anda dan cakupan mana yang harus dipilih.
</Check>

<Note>
  **Claude Platform on AWS:** Claude Code Analytics API saat ini tidak tersedia. Sebagai gantinya, lihat penggunaan Claude Code di halaman **Usage** di Claude Console.
</Note>

<Note>
  **Organisasi Claude Enterprise:** Aktivitas Claude Code untuk pengguna claude.ai dilaporkan oleh Claude Enterprise Analytics API, yang menggunakan kunci Analytics API alih-alih kunci Admin API. Lihat [Analytics APIs](/docs/id/manage-claude/analytics-api) untuk mengetahui API dan jenis kunci mana yang dibutuhkan organisasi Anda.
</Note>

## Mulai cepat

Dapatkan analitik Claude Code organisasi Anda untuk hari tertentu:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
limit=20" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ADMIN_API_KEY"
```

<Tip>
  **Atur header User-Agent untuk integrasi**

  Jika Anda membangun integrasi, atur header User-Agent Anda untuk membantu kami memahami pola penggunaan:

  ```text wrap
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Claude Code Analytics API

Lacak penggunaan Claude Code, metrik produktivitas, dan aktivitas pengembang di seluruh organisasi Anda dengan endpoint `/v1/organizations/usage_report/claude_code`.

### Konsep utama

* **Agregasi harian:** Mengembalikan metrik untuk satu hari yang ditentukan oleh parameter `starting_at`
* **Data tingkat pengguna:** Setiap record mewakili aktivitas satu pengguna untuk hari yang ditentukan
* **Metrik produktivitas:** Lacak sesi, baris kode, commit, pull request, dan penggunaan alat
* **Data token dan biaya:** Pantau penggunaan dan estimasi biaya yang dirinci berdasarkan model Claude
* **Paginasi berbasis kursor:** Tangani dataset besar dengan paginasi yang stabil menggunakan kursor opaque
* **Kesegaran data:** Metrik tersedia dengan penundaan hingga 1 jam untuk konsistensi

Untuk detail parameter lengkap dan skema respons, lihat [referensi Claude Code Analytics API](/docs/id/api/admin/usage_report/retrieve_claude_code).

### Contoh dasar

#### Dapatkan analitik untuk hari tertentu

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ADMIN_API_KEY"
```

#### Dapatkan analitik dengan paginasi

```bash cURL
# Permintaan pertama
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
limit=20" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ADMIN_API_KEY"

# Permintaan berikutnya menggunakan cursor dari respons
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
page=page_MjAyNS0wNS0xNFQwMDowMDowMFo=" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ADMIN_API_KEY"
```

### Parameter permintaan

| Parameter     | Tipe    | Wajib | Deskripsi                                                                           |
| ------------- | ------- | ----- | ----------------------------------------------------------------------------------- |
| `starting_at` | string  | Ya    | Tanggal UTC dalam format YYYY-MM-DD; mengembalikan metrik hanya untuk satu hari ini |
| `limit`       | integer | Tidak | Jumlah record per halaman (default: 20, maks: 1000)                                 |
| `page`        | string  | Tidak | Token kursor opaque dari field `next_page` pada respons sebelumnya                  |

### Metrik yang tersedia

Setiap record respons berisi metrik berikut untuk satu pengguna pada satu hari:

#### Dimensi

* **date:** Tanggal dalam format RFC 3339 (timestamp UTC)
* **actor:** Pengguna atau kunci API yang melakukan tindakan Claude Code (baik `user_actor` dengan `email_address` atau `api_actor` dengan `api_key_name`)
* **organization\_id:** UUID organisasi
* **customer\_type:** Jenis akun pelanggan (`api` untuk pelanggan API, `subscription` untuk pelanggan Pro/Team)
* **terminal\_type:** Jenis terminal atau lingkungan tempat Claude Code digunakan (misalnya, `vscode`, `iTerm.app`, `tmux`)

#### Metrik inti

* **num\_sessions:** Jumlah sesi Claude Code berbeda yang dimulai oleh aktor ini
* **lines\_of\_code.added:** Jumlah total baris kode yang ditambahkan di semua file oleh Claude Code
* **lines\_of\_code.removed:** Jumlah total baris kode yang dihapus di semua file oleh Claude Code
* **commits\_by\_claude\_code:** Jumlah commit git yang dibuat melalui fungsionalitas commit Claude Code
* **pull\_requests\_by\_claude\_code:** Jumlah pull request yang dibuat melalui fungsionalitas PR Claude Code

#### Metrik tindakan alat

Rincian tingkat penerimaan dan penolakan tindakan alat berdasarkan jenis alat:

* **edit\_tool.accepted/rejected:** Jumlah proposal alat Edit yang diterima/ditolak pengguna
* **multi\_edit\_tool.accepted/rejected:** Jumlah proposal alat MultiEdit yang diterima/ditolak pengguna
* **write\_tool.accepted/rejected:** Jumlah proposal alat Write yang diterima/ditolak pengguna
* **notebook\_edit\_tool.accepted/rejected:** Jumlah proposal alat NotebookEdit yang diterima/ditolak pengguna

#### Rincian model

Untuk setiap model Claude yang digunakan:

* **model:** Pengidentifikasi model Claude (misalnya, `claude-opus-4-8`)
* **tokens.input/output:** Jumlah token input dan output untuk model ini
* **tokens.cache\_read/cache\_creation:** Penggunaan token terkait cache untuk model ini
* **estimated\_cost.amount:** Estimasi biaya dalam sen USD untuk model ini
* **estimated\_cost.currency:** Kode mata uang untuk jumlah biaya (saat ini selalu `USD`)

### Struktur respons

API mengembalikan data dalam format berikut:

```json
{
  "data": [
    {
      "date": "2025-09-08T00:00:00Z",
      "actor": {
        "type": "user_actor",
        "email_address": "developer@company.com"
      },
      "organization_id": "dc9f6c26-b22c-4831-8d01-0446bada88f1",
      "customer_type": "api",
      "terminal_type": "vscode",
      "core_metrics": {
        "num_sessions": 5,
        "lines_of_code": {
          "added": 1543,
          "removed": 892
        },
        "commits_by_claude_code": 12,
        "pull_requests_by_claude_code": 2
      },
      "tool_actions": {
        "edit_tool": {
          "accepted": 45,
          "rejected": 5
        },
        "multi_edit_tool": {
          "accepted": 12,
          "rejected": 2
        },
        "write_tool": {
          "accepted": 8,
          "rejected": 1
        },
        "notebook_edit_tool": {
          "accepted": 3,
          "rejected": 0
        }
      },
      "model_breakdown": [
        {
          "model": "claude-opus-4-8",
          "tokens": {
            "input": 100000,
            "output": 35000,
            "cache_read": 10000,
            "cache_creation": 5000
          },
          "estimated_cost": {
            "currency": "USD",
            "amount": 1025
          }
        }
      ]
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Paginasi

API mendukung paginasi berbasis kursor untuk organisasi dengan jumlah pengguna yang besar:

1. Buat permintaan awal Anda dengan parameter `limit` opsional.
2. Jika `has_more` bernilai `true` dalam respons, gunakan nilai `next_page` dalam permintaan Anda berikutnya.
3. Lanjutkan hingga `has_more` bernilai `false`.

Kursor mengkodekan posisi record terakhir dan memastikan paginasi yang stabil bahkan saat data baru masuk. Setiap sesi paginasi mempertahankan batas data yang konsisten untuk memastikan Anda tidak melewatkan atau menduplikasi record.

## Kasus penggunaan umum

* **Dasbor eksekutif:** Buat laporan tingkat tinggi yang menunjukkan dampak Claude Code pada kecepatan pengembangan
* **Perbandingan alat AI:** Ekspor metrik untuk membandingkan Claude Code dengan alat pengkodean AI lainnya seperti Copilot dan Cursor
* **Analisis produktivitas pengembang:** Lacak metrik produktivitas individu dan tim dari waktu ke waktu
* **Pelacakan dan alokasi biaya:** Pantau pola pengeluaran dan alokasikan biaya berdasarkan tim atau proyek
* **Pemantauan adopsi:** Identifikasi tim dan pengguna mana yang mendapatkan nilai terbesar dari Claude Code
* **Justifikasi ROI:** Sediakan metrik konkret untuk menjustifikasi dan memperluas adopsi Claude Code secara internal

## Pertanyaan yang sering diajukan

### Seberapa segar data analitiknya?

Data analitik Claude Code biasanya muncul dalam waktu 1 jam setelah aktivitas pengguna selesai. Untuk memastikan hasil paginasi yang konsisten, hanya data yang lebih lama dari 1 jam yang disertakan dalam respons.

### Bisakah saya mendapatkan metrik real-time?

Tidak, API ini hanya menyediakan metrik agregat harian. Untuk pemantauan real-time, pertimbangkan untuk menggunakan [integrasi OpenTelemetry](https://code.claude.com/docs/id/monitoring-usage).

### Bagaimana pengguna diidentifikasi dalam data?

Pengguna diidentifikasi melalui field `actor` dengan dua cara:

* **`user_actor`:** Berisi `email_address` untuk pengguna yang mengautentikasi melalui OAuth (paling umum)
* **`api_actor`:** Berisi `api_key_name` untuk pengguna yang mengautentikasi dengan kunci API

Field `customer_type` menunjukkan apakah penggunaan berasal dari pelanggan `api` (API bayar sesuai pemakaian) atau pelanggan `subscription` (paket Pro/Team).

### Berapa lama periode retensi data?

Data historis analitik Claude Code disimpan dan dapat diakses melalui API. Tidak ada periode penghapusan yang ditentukan untuk data ini.

### Deployment Claude Code mana yang didukung?

API ini hanya melacak penggunaan Claude Code pada Claude API. Penggunaan melalui [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude on Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), atau [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) tidak disertakan.

### Berapa biaya untuk menggunakan API ini?

Claude Code Analytics API gratis digunakan untuk semua organisasi yang memiliki akses ke Admin API.

### Bagaimana cara menghitung tingkat penerimaan alat?

Tingkat penerimaan alat = `accepted / (accepted + rejected)` untuk setiap jenis alat. Misalnya, jika alat edit menunjukkan 45 diterima dan 5 ditolak, tingkat penerimaannya adalah 90%.

### Zona waktu apa yang digunakan untuk parameter tanggal?

Semua tanggal dalam UTC. Parameter `starting_at` harus dalam format YYYY-MM-DD dan merepresentasikan tengah malam UTC untuk hari tersebut.

## Lihat juga

Claude Code Analytics API membantu Anda memahami dan mengoptimalkan alur kerja pengembangan tim Anda. Pelajari lebih lanjut tentang fitur terkait:

* [Admin API](/docs/id/manage-claude/admin-api)
* [Referensi Admin API](/docs/id/api/admin)
* [Dasbor Claude Code Analytics](/claude-code)
* [Usage and Cost API](/docs/id/manage-claude/usage-cost-api) - Lacak penggunaan API di semua layanan Anthropic
* [Compliance API](/docs/id/manage-claude/compliance-api) - Ambil data audit dan aktivitas
* [Manajemen identitas dan akses](https://code.claude.com/docs/id/iam)
* [Memantau penggunaan dengan OpenTelemetry](https://code.claude.com/docs/id/monitoring-usage) untuk metrik kustom dan peringatan
