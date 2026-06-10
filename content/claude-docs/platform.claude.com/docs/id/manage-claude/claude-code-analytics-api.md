---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 22f40c276e3c1c2a89e6f4ffaee48faecfe7bacffaeb49c676703cb669a7c5aa
---

# Claude Code Analytics API

Akses analitik penggunaan Claude Code dan metrik produktivitas organisasi Anda secara terprogram dengan Claude Code Analytics Admin API.

---

<Tip>
**Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

Claude Code Analytics Admin API menyediakan akses terprogram ke metrik penggunaan harian yang diagregasi untuk pengguna Claude Code, memungkinkan organisasi menganalisis produktivitas developer dan membangun dashboard kustom. API ini menjembatani kesenjangan antara [dashboard Analytics](/claude-code) dasar dan integrasi OpenTelemetry yang kompleks.

API ini memungkinkan Anda untuk memantau, menganalisis, dan mengoptimalkan adopsi Claude Code dengan lebih baik:

* **Analisis produktivitas developer:** Lacak sesi, baris kode yang ditambahkan/dihapus, commit, dan pull request yang dibuat menggunakan Claude Code
* **Metrik penggunaan alat:** Pantau tingkat penerimaan dan penolakan untuk berbagai alat Claude Code (Edit, MultiEdit, Write, NotebookEdit)
* **Analisis biaya:** Lihat estimasi biaya dan penggunaan token yang dirinci berdasarkan model Claude
* **Pelaporan kustom:** Ekspor data untuk membangun dashboard eksekutif dan laporan untuk tim manajemen
* **Justifikasi penggunaan:** Sediakan metrik untuk menjustifikasi dan memperluas adopsi Claude Code secara internal

<Check>
  **Kunci Admin API diperlukan**

  API ini merupakan bagian dari [Admin API](/docs/id/manage-claude/admin-api). Endpoint ini memerlukan kunci Admin API (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Hanya anggota organisasi dengan peran admin yang dapat menyediakan kunci Admin API melalui [Claude Console](/settings/admin-keys).
</Check>

<Note>
**Claude Platform di AWS:** Claude Code Analytics API saat ini tidak tersedia. Lihat penggunaan Claude Code di halaman **Usage** pada Claude Console sebagai gantinya.
</Note>

## Mulai cepat \{#quick-start}

Dapatkan analitik Claude Code organisasi Anda untuk hari tertentu:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

<Tip>
  **Atur header User-Agent untuk integrasi**

  Jika Anda membangun integrasi, atur header User-Agent Anda untuk membantu kami memahami pola penggunaan:
  ```text
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Claude Code Analytics API \{#claude-code-analytics-api}

Lacak penggunaan Claude Code, metrik produktivitas, dan aktivitas developer di seluruh organisasi Anda dengan endpoint `/v1/organizations/usage_report/claude_code`.

### Konsep utama \{#key-concepts}

- **Agregasi harian**: Mengembalikan metrik untuk satu hari yang ditentukan oleh parameter `starting_at`
- **Data tingkat pengguna**: Setiap record mewakili aktivitas satu pengguna untuk hari yang ditentukan
- **Metrik produktivitas**: Lacak sesi, baris kode, commit, pull request, dan penggunaan alat
- **Data token dan biaya**: Pantau penggunaan dan estimasi biaya yang dirinci berdasarkan model Claude
- **Paginasi berbasis cursor**: Tangani dataset besar dengan paginasi yang stabil menggunakan cursor opaque
- **Kesegaran data**: Metrik tersedia dengan penundaan hingga 1 jam untuk konsistensi

Untuk detail parameter lengkap dan skema respons, lihat [referensi Claude Code Analytics API](/docs/id/api/admin-api/claude-code/get-claude-code-usage-report).

### Contoh dasar \{#basic-examples}

#### Mendapatkan analitik untuk hari tertentu \{#get-analytics-for-a-specific-day}

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

#### Mendapatkan analitik dengan paginasi \{#get-analytics-with-pagination}

```bash cURL
# Permintaan pertama
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"

# Permintaan berikutnya menggunakan kursor dari respons
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2025-09-08&\
page=page_MjAyNS0wNS0xNFQwMDowMDowMFo=" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

### Parameter permintaan \{#request-parameters}

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|----------|-------------|
| `starting_at` | string | Ya | Tanggal UTC dalam format YYYY-MM-DD; mengembalikan metrik hanya untuk satu hari ini |
| `limit` | integer | Tidak | Jumlah record per halaman (default: 20, maks: 1000) |
| `page` | string | Tidak | Token cursor opaque dari field `next_page` pada respons sebelumnya |

### Metrik yang tersedia \{#available-metrics}

Setiap record respons berisi metrik berikut untuk satu pengguna pada satu hari:

#### Dimensi \{#dimensions}
- **date**: Tanggal dalam format RFC 3339 (timestamp UTC)
- **actor**: Pengguna atau kunci API yang melakukan tindakan Claude Code (baik `user_actor` dengan `email_address` atau `api_actor` dengan `api_key_name`)
- **organization_id**: UUID organisasi
- **customer_type**: Tipe akun pelanggan (`api` untuk pelanggan API, `subscription` untuk pelanggan Pro/Team)
- **terminal_type**: Tipe terminal atau lingkungan tempat Claude Code digunakan (misalnya, `vscode`, `iTerm.app`, `tmux`)

#### Metrik inti \{#core-metrics}
- **num_sessions**: Jumlah sesi Claude Code berbeda yang diinisiasi oleh actor ini
- **lines_of_code.added**: Total jumlah baris kode yang ditambahkan di semua file oleh Claude Code
- **lines_of_code.removed**: Total jumlah baris kode yang dihapus di semua file oleh Claude Code
- **commits_by_claude_code**: Jumlah git commit yang dibuat melalui fungsionalitas commit Claude Code
- **pull_requests_by_claude_code**: Jumlah pull request yang dibuat melalui fungsionalitas PR Claude Code

#### Metrik tindakan alat \{#tool-action-metrics}
Rincian tingkat penerimaan dan penolakan tindakan alat berdasarkan tipe alat:
- **edit_tool.accepted/rejected:** Jumlah proposal alat Edit yang diterima/ditolak oleh pengguna
- **multi_edit_tool.accepted/rejected:** Jumlah proposal alat MultiEdit yang diterima/ditolak oleh pengguna
- **write_tool.accepted/rejected:** Jumlah proposal alat Write yang diterima/ditolak oleh pengguna
- **notebook_edit_tool.accepted/rejected:** Jumlah proposal alat NotebookEdit yang diterima/ditolak oleh pengguna

#### Rincian model \{#model-breakdown}
Untuk setiap model Claude yang digunakan:
- **model**: Pengidentifikasi model Claude (misalnya, `claude-opus-4-8`)
- **tokens.input/output**: Jumlah token input dan output untuk model ini
- **tokens.cache_read/cache_creation**: Penggunaan token terkait cache untuk model ini
- **estimated_cost.amount**: Estimasi biaya dalam sen USD untuk model ini
- **estimated_cost.currency**: Kode mata uang untuk jumlah biaya (saat ini selalu `USD`)

### Struktur respons \{#response-structure}

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

## Paginasi \{#pagination}

API mendukung paginasi berbasis cursor untuk organisasi dengan jumlah pengguna yang besar:

1. Buat permintaan awal Anda dengan parameter `limit` opsional
2. Jika `has_more` bernilai `true` dalam respons, gunakan nilai `next_page` dalam permintaan Anda berikutnya
3. Lanjutkan hingga `has_more` bernilai `false`

Cursor mengenkode posisi record terakhir dan memastikan paginasi yang stabil bahkan saat data baru masuk. Setiap sesi paginasi mempertahankan batas data yang konsisten untuk memastikan Anda tidak melewatkan atau menduplikasi record.

## Kasus penggunaan umum \{#common-use-cases}

- **Dashboard eksekutif**: Buat laporan tingkat tinggi yang menunjukkan dampak Claude Code pada kecepatan pengembangan
- **Perbandingan alat AI**: Ekspor metrik untuk membandingkan Claude Code dengan alat coding AI lainnya seperti Copilot dan Cursor
- **Analisis produktivitas developer**: Lacak metrik produktivitas individu dan tim dari waktu ke waktu
- **Pelacakan dan alokasi biaya**: Pantau pola pengeluaran dan alokasikan biaya berdasarkan tim atau proyek
- **Pemantauan adopsi**: Identifikasi tim dan pengguna mana yang mendapatkan nilai paling banyak dari Claude Code
- **Justifikasi ROI**: Sediakan metrik konkret untuk menjustifikasi dan memperluas adopsi Claude Code secara internal

## Pertanyaan yang sering diajukan \{#frequently-asked-questions}

### Seberapa baru data analitik ini? \{#how-fresh-is-the-analytics-data}
Data analitik Claude Code biasanya muncul dalam waktu 1 jam setelah aktivitas pengguna selesai. Untuk memastikan hasil paginasi yang konsisten, hanya data yang lebih lama dari 1 jam yang disertakan dalam respons.

### Bisakah saya mendapatkan metrik real-time? \{#can-i-get-real-time-metrics}
Tidak, API ini hanya menyediakan metrik harian yang diagregasi. Untuk pemantauan real-time, pertimbangkan untuk menggunakan [integrasi OpenTelemetry](https://code.claude.com/docs/en/monitoring-usage).

### Bagaimana pengguna diidentifikasi dalam data? \{#how-are-users-identified-in-the-data}
Pengguna diidentifikasi melalui field `actor` dengan dua cara:
- **`user_actor`:** Berisi `email_address` untuk pengguna yang mengautentikasi melalui OAuth (paling umum)
- **`api_actor`:** Berisi `api_key_name` untuk pengguna yang mengautentikasi dengan kunci API

Field `customer_type` menunjukkan apakah penggunaan berasal dari pelanggan `api` (API bayar sesuai penggunaan) atau pelanggan `subscription` (paket Pro/Team).

### Berapa periode retensi data? \{#whats-the-data-retention-period}
Data analitik Claude Code historis disimpan dan dapat diakses melalui API. Tidak ada periode penghapusan yang ditentukan untuk data ini.

### Deployment Claude Code mana yang didukung? \{#which-claude-code-deployments-are-supported}
API ini hanya melacak penggunaan Claude Code pada Claude API. Penggunaan melalui [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Claude di Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), atau [Claude di Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai) tidak disertakan.

### Berapa biaya untuk menggunakan API ini? \{#what-does-it-cost-to-use-this-api}
Claude Code Analytics API gratis digunakan untuk semua organisasi yang memiliki akses ke Admin API.

### Bagaimana cara menghitung tingkat penerimaan alat? \{#how-do-i-calculate-tool-acceptance-rates}
Tingkat penerimaan alat = `accepted / (accepted + rejected)` untuk setiap tipe alat. Misalnya, jika alat edit menunjukkan 45 diterima dan 5 ditolak, tingkat penerimaannya adalah 90%.

### Zona waktu apa yang digunakan untuk parameter tanggal? \{#what-time-zone-is-used-for-the-date-parameter}
Semua tanggal dalam UTC. Parameter `starting_at` harus dalam format YYYY-MM-DD dan mewakili tengah malam UTC untuk hari tersebut.

## Lihat juga \{#see-also}

Claude Code Analytics API membantu Anda memahami dan mengoptimalkan alur kerja pengembangan tim Anda. Pelajari lebih lanjut tentang fitur terkait:

- [Admin API](/docs/id/manage-claude/admin-api)
- [Referensi Admin API](/docs/id/api/admin)
- [Dashboard Claude Code Analytics](/claude-code)
- [Usage and Cost API](/docs/id/manage-claude/usage-cost-api) - Lacak penggunaan API di semua layanan Anthropic
- [Compliance API](/docs/id/manage-claude/compliance-api) - Ambil data audit dan aktivitas
- [Manajemen identitas dan akses](https://code.claude.com/docs/en/iam)
- [Memantau penggunaan dengan OpenTelemetry](https://code.claude.com/docs/en/monitoring-usage) untuk metrik kustom dan peringatan