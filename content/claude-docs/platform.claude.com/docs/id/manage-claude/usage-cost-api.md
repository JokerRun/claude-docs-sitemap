---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/usage-cost-api
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 0c858b409551d12714a2bd367d3de2145fd77e870889e35215229003f7aee932
---

# API Penggunaan dan Biaya

Akses data penggunaan dan biaya API organisasi Anda secara terprogram dengan Usage & Cost Admin API.

---

<Tip>
**Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

Usage & Cost Admin API menyediakan akses terprogram dan terperinci ke data historis penggunaan dan biaya API untuk organisasi Anda. Data ini serupa dengan informasi yang tersedia di halaman [Usage](/usage) dan [Cost](/cost) pada Claude Console.

API ini memungkinkan Anda untuk memantau, menganalisis, dan mengoptimalkan implementasi Claude Anda dengan lebih baik:

* **Pelacakan Penggunaan yang Akurat:** Dapatkan jumlah token dan pola penggunaan yang presisi alih-alih hanya mengandalkan penghitungan token dari respons
* **Rekonsiliasi Biaya:** Cocokkan catatan internal dengan penagihan Anthropic untuk tim keuangan dan akuntansi
* **Performa dan peningkatan produk:** Pantau performa produk sambil mengukur apakah perubahan pada sistem telah meningkatkannya, atau siapkan pemberitahuan (alerting)
* **Optimasi [Batas laju](/docs/id/api/rate-limits) dan [Priority Tier](/docs/id/api/service-tiers#get-started-with-priority-tier):** Optimalkan fitur seperti [caching prompt](/docs/id/build-with-claude/prompt-caching) atau prompt tertentu untuk memaksimalkan kapasitas yang dialokasikan, atau beli kapasitas khusus.
* **Analisis Lanjutan:** Lakukan analisis data yang lebih mendalam daripada yang tersedia di Console

<Check>
  **Kunci Admin API diperlukan**

  API ini merupakan bagian dari [Admin API](/docs/id/manage-claude/admin-api). Endpoint ini memerlukan kunci Admin API (dimulai dengan `sk-ant-admin...`) yang berbeda dari kunci API standar. Hanya anggota organisasi dengan peran admin yang dapat membuat kunci Admin API melalui [Claude Console](/settings/admin-keys).
</Check>

<Note>
**Claude Platform di AWS:** Endpoint API Penggunaan dan Biaya terprogram saat ini tidak tersedia. Lihat data penggunaan dan biaya di halaman **Usage** dan **Cost** pada Claude Console sebagai gantinya.
</Note>

## Solusi mitra \{#partner-solutions}

Platform observabilitas terkemuka menawarkan integrasi siap pakai untuk memantau penggunaan dan biaya API Claude Anda, tanpa perlu menulis kode kustom. Integrasi ini menyediakan dasbor, pemberitahuan, dan analitik untuk membantu Anda mengelola penggunaan API secara efektif.

<CardGroup cols={3}>
  <Card title="CloudZero" icon="chart" href="https://docs.cloudzero.com/docs/connections-anthropic">
    Platform intelijen cloud untuk melacak dan memperkirakan biaya
  </Card>
  <Card title="Datadog" icon="chart" href="https://docs.datadoghq.com/integrations/anthropic/">
    Observabilitas LLM dengan pelacakan dan pemantauan otomatis
  </Card>
  <Card title="Grafana Cloud" icon="chart" href="https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-anthropic/">
    Integrasi tanpa agen untuk observabilitas LLM yang mudah dengan dasbor dan pemberitahuan siap pakai
  </Card>
  <Card title="Honeycomb" icon="polygon" href="https://docs.honeycomb.io/integrations/anthropic-usage-monitoring/">
    Kueri dan visualisasi tingkat lanjut melalui OpenTelemetry
  </Card>
  <Card title="Vantage" icon="chart" href="https://docs.vantage.sh/connecting_anthropic">
    Platform FinOps untuk observabilitas biaya & penggunaan LLM
  </Card>
</CardGroup>

## Mulai cepat \{#quick-start}

Dapatkan penggunaan harian organisasi Anda selama 7 hari terakhir:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-08T00:00:00Z&\
ending_at=2025-01-15T00:00:00Z&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Tip>
  **Atur header User-Agent untuk integrasi**

  Jika Anda membangun integrasi, atur header User-Agent Anda untuk membantu kami memahami pola penggunaan:
  ```text
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Usage API \{#usage-api}

Lacak konsumsi token di seluruh organisasi Anda dengan rincian terperinci berdasarkan model, workspace, dan tingkat layanan menggunakan endpoint `/v1/organizations/usage_report/messages`.

### Konsep utama \{#key-concepts}

- **Time buckets** (wadah waktu): Agregasikan data penggunaan dalam interval tetap (`1m`, `1h`, atau `1d`)
- **Pelacakan token**: Ukur token input yang tidak di-cache, input yang di-cache, pembuatan cache, dan token output
- **Pemfilteran & pengelompokan**: Filter berdasarkan kunci API, workspace, model, tingkat layanan, jendela konteks, [residensi data](/docs/id/manage-claude/data-residency), atau kecepatan (beta), dan kelompokkan hasil berdasarkan dimensi-dimensi ini
- **Penggunaan alat server**: Lacak penggunaan alat sisi server seperti pencarian web

Untuk detail parameter lengkap dan skema respons, lihat [referensi Usage API](/docs/id/api/admin-api/usage-cost/get-messages-usage-report).

### Contoh dasar \{#basic-examples}

#### Penggunaan harian berdasarkan model \{#daily-usage-by-model}

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

#### Penggunaan per jam dengan pemfilteran \{#hourly-usage-with-filtering}

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-15T00:00:00Z&\
ending_at=2025-01-15T23:59:59Z&\
models[]=claude-opus-4-8&\
service_tiers[]=batch&\
context_window[]=0-200k&\
bucket_width=1h" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

#### Filter penggunaan berdasarkan kunci API dan workspace \{#filter-usage-by-api-keys-and-workspaces}

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
api_key_ids[]=apikey_01Rj2N8SVvo6BePZj99NhmiT&\
api_key_ids[]=apikey_01ABC123DEF456GHI789JKL&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
workspace_ids[]=wrkspc_01XYZ789ABC123DEF456MNO&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Tip>
Untuk mengambil ID kunci API organisasi Anda, gunakan endpoint [List API Keys](/docs/id/api/admin-api/apikeys/list-api-keys).

Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](/docs/id/api/admin-api/workspaces/list-workspaces), atau temukan ID workspace organisasi Anda di Claude Console.
</Tip>

#### Residensi data \{#data-residency}

Lacak [kontrol residensi data](/docs/id/manage-claude/data-residency) Anda dengan mengelompokkan dan memfilter penggunaan menggunakan dimensi `inference_geo`. Ini berguna untuk memverifikasi perutean geografis di seluruh organisasi Anda.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
group_by[]=inference_geo&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Anda juga dapat memfilter ke geo tertentu. Nilai yang valid adalah `global`, `us`, dan `not_available`:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
inference_geos[]=us&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Note>
Model yang dirilis sebelum Februari 2026 (sebelum Claude Opus 4.6 dan Claude Sonnet 4.6) tidak mendukung parameter permintaan `inference_geo`, sehingga laporan penggunaannya mengembalikan `"not_available"` untuk dimensi ini. Anda dapat menggunakan `not_available` sebagai nilai filter di `inference_geos[]` untuk menargetkan model-model tersebut.
</Note>

#### Fast mode (pratinjau riset) \{#fast-mode-research-preview}

Lacak penggunaan [fast mode](/docs/id/build-with-claude/fast-mode) dengan mengelompokkan dan memfilter menggunakan dimensi `speed`. Ini berguna untuk memantau penggunaan mode standar vs. fast mode.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
group_by[]=speed&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "anthropic-beta: fast-mode-2026-02-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Anda juga dapat memfilter ke kecepatan tertentu. Nilai yang valid adalah `standard` dan `fast`:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
speeds[]=fast&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "anthropic-beta: fast-mode-2026-02-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Note>
Baik filter `speeds[]` maupun nilai group_by `speed` memerlukan header beta `fast-mode-2026-02-01`.
</Note>

### Batas granularitas waktu \{#time-granularity-limits}

| Granularitas | Batas Default | Batas Maksimum | Kasus Penggunaan |
|-------------|---------------|---------------|----------|
| `1m` | 60 bucket | 1440 bucket | Pemantauan real-time |
| `1h` | 24 bucket | 168 bucket | Pola harian |
| `1d` | 7 bucket | 31 bucket | Laporan mingguan/bulanan |

## Cost API \{#cost-api}

Ambil rincian biaya tingkat layanan dalam USD dengan endpoint `/v1/organizations/cost_report`.

### Konsep utama \{#key-concepts-2}

- **Mata uang**: Semua biaya dalam USD, dilaporkan sebagai string desimal dalam unit terkecil (sen)
- **Jenis biaya**: Lacak biaya penggunaan token, pencarian web, dan eksekusi kode
- **Pengelompokan**: Kelompokkan biaya berdasarkan workspace atau deskripsi untuk rincian terperinci. Saat mengelompokkan berdasarkan `description`, respons menyertakan field yang telah diurai seperti `model` dan `inference_geo`
- **Time buckets**: Hanya granularitas harian (`1d`)

Untuk detail parameter lengkap dan skema respons, lihat [referensi Cost API](/docs/id/api/admin-api/usage-cost/get-cost-report).

<Warning>
  Biaya Priority Tier menggunakan model penagihan yang berbeda dan tidak disertakan dalam endpoint biaya. Lacak penggunaan Priority Tier melalui endpoint penggunaan sebagai gantinya.
</Warning>

### Contoh dasar \{#basic-example}

```bash cURL
curl "https://api.anthropic.com/v1/organizations/cost_report?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
group_by[]=workspace_id&\
group_by[]=description" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Paginasi \{#pagination}

Kedua endpoint mendukung paginasi untuk dataset besar:

1. Buat permintaan awal Anda
2. Jika `has_more` bernilai `true`, gunakan nilai `next_page` dalam permintaan Anda berikutnya
3. Lanjutkan hingga `has_more` bernilai `false`

```bash cURL
# Permintaan pertama
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
limit=7" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Respons mencakup: "has_more": true, "next_page": "page_xyz..."

# Permintaan berikutnya dengan paginasi
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
limit=7&\
page=page_xyz..." \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Kasus penggunaan umum \{#common-use-cases}

Jelajahi implementasi terperinci di [Claude Cookbook](https://platform.claude.com/cookbooks):

- **Laporan penggunaan harian**: Lacak tren konsumsi token
- **Atribusi biaya**: Alokasikan pengeluaran berdasarkan workspace untuk chargeback
- **Efisiensi cache**: Ukur dan optimalkan caching prompt
- **Pemantauan anggaran**: Siapkan pemberitahuan untuk ambang batas pengeluaran
- **Ekspor CSV**: Hasilkan laporan untuk tim keuangan

## Pertanyaan yang sering diajukan \{#frequently-asked-questions}

### Seberapa baru datanya? \{#how-fresh-is-the-data}
Data penggunaan dan biaya biasanya muncul dalam waktu 5 menit setelah permintaan API selesai, meskipun penundaan terkadang bisa lebih lama.

### Berapa frekuensi polling yang direkomendasikan? \{#whats-the-recommended-polling-frequency}
API mendukung polling satu kali per menit untuk penggunaan berkelanjutan. Untuk lonjakan singkat (misalnya, mengunduh data yang dipaginasi), polling yang lebih sering dapat diterima. Cache hasil untuk dasbor yang memerlukan pembaruan sering.

### Bagaimana cara melacak penggunaan eksekusi kode? \{#how-do-i-track-code-execution-usage}
Biaya eksekusi kode muncul di endpoint biaya yang dikelompokkan di bawah `Code Execution Usage` pada field deskripsi. Eksekusi kode tidak disertakan dalam endpoint penggunaan.

### Bagaimana cara melacak penggunaan Priority Tier? \{#how-do-i-track-priority-tier-usage}
Filter atau kelompokkan berdasarkan `service_tier` di endpoint penggunaan dan cari nilai `priority`. Biaya Priority Tier tidak tersedia di endpoint biaya.

### Apa yang terjadi dengan penggunaan Workbench? \{#what-happens-with-workbench-usage}
Penggunaan API dari Workbench tidak dikaitkan dengan kunci API, sehingga `api_key_id` akan bernilai `null` bahkan saat mengelompokkan berdasarkan dimensi tersebut.

### Bagaimana workspace default direpresentasikan? \{#how-is-the-default-workspace-represented}
Penggunaan dan biaya yang diatribusikan ke workspace default memiliki nilai `null` untuk `workspace_id`.

### Bagaimana cara mendapatkan rincian biaya per pengguna untuk Claude Code? \{#how-do-i-get-per-user-cost-breakdowns-for-claude-code}

Gunakan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api), yang menyediakan estimasi biaya per pengguna dan metrik produktivitas tanpa keterbatasan performa dalam merinci biaya berdasarkan banyak kunci API. Untuk penggunaan API umum dengan banyak kunci, gunakan [Usage API](#usage-api) untuk melacak konsumsi token sebagai proksi biaya.

## Lihat juga \{#see-also}
API Penggunaan dan Biaya dapat digunakan untuk membantu Anda memberikan pengalaman yang lebih baik bagi pengguna Anda, membantu Anda mengelola biaya, dan menjaga batas laju Anda. Pelajari lebih lanjut tentang beberapa fitur lainnya ini:

- [Admin API](/docs/id/manage-claude/admin-api)
- [Referensi Admin API](/docs/id/api/admin)
- [Harga](/docs/id/about-claude/pricing)
- [Caching prompt](/docs/id/build-with-claude/prompt-caching) - Optimalkan biaya dengan caching
- [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) - Diskon 50% untuk permintaan batch
- [Batas laju](/docs/id/api/rate-limits) - Pahami tingkatan penggunaan
- [Rate Limits API](/docs/id/manage-claude/rate-limits-api) - Baca batas laju yang telah dikonfigurasi
- [Residensi data](/docs/id/manage-claude/data-residency) - Kontrol geografi inferensi