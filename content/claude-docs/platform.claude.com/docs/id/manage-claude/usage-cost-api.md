---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/usage-cost-api
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 2716d997ee9be1659b3d741c63429926696c24450c9f24d4e2525eb4c1df962c
---

# API Penggunaan dan Biaya

Akses data penggunaan dan biaya API organisasi Anda secara terprogram dengan Usage & Cost Admin API.

---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, atur organisasi Anda di **Console → Settings → Organization**.
</Tip>

Usage & Cost Admin API menyediakan akses terprogram dan granular ke data historis penggunaan dan biaya API untuk organisasi Anda. Data ini serupa dengan informasi yang tersedia di halaman [Usage](/usage) dan [Cost](/cost) pada Claude Console.

API ini memungkinkan Anda untuk memantau, menganalisis, dan mengoptimalkan implementasi Claude Anda dengan lebih baik:

* **Pelacakan Penggunaan yang Akurat:** Dapatkan jumlah token dan pola penggunaan yang presisi alih-alih hanya mengandalkan penghitungan token dari respons
* **Rekonsiliasi Biaya:** Cocokkan catatan internal dengan penagihan Anthropic untuk tim keuangan dan akuntansi
* **Performa dan peningkatan produk:** Pantau performa produk sambil mengukur apakah perubahan pada sistem telah meningkatkannya, atau siapkan pemberitahuan (alerting)
* **Optimasi [Batas laju](/docs/id/api/rate-limits) dan [Priority Tier](/docs/id/api/service-tiers#get-started-with-priority-tier):** Optimalkan fitur seperti [caching prompt](/docs/id/build-with-claude/prompt-caching) atau prompt tertentu untuk memaksimalkan kapasitas yang dialokasikan, atau beli kapasitas khusus.
* **Analisis Lanjutan:** Lakukan analisis data yang lebih mendalam daripada yang tersedia di Console

<Check>
  **Kunci Admin API diperlukan.** Endpoint ini memerlukan kunci Admin API, yang berbeda dari kunci API Claude standar. Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys) untuk mengetahui tempat membuatnya sesuai jenis organisasi Anda dan cakupan mana yang harus dipilih.
</Check>

Organisasi Claude Enterprise menggunakan kunci Analytics API dengan API yang berbeda; lihat [API mana yang Anda butuhkan?](#which-api-do-you-need).

<Note>
  **Claude Platform di AWS:** Endpoint terprogram Usage and Cost API saat ini tidak tersedia. Lihat data penggunaan dan biaya di halaman **Usage** dan **Cost** di Claude Console sebagai gantinya.
</Note>

## API mana yang Anda butuhkan?

Anthropic menyediakan pelaporan biaya dan penggunaan melalui dua API, tergantung pada produk Claude mana yang dikelola organisasi Anda:

| Organisasi Anda                  | API                                                                                           | Jenis kunci                            |
| -------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------- |
| Claude Console (Claude Platform) | Usage and Cost Admin API yang dijelaskan di halaman ini                                       | Kunci Admin API (`sk-ant-admin01-...`) |
| Claude Enterprise (claude.ai)    | Endpoint biaya dan penggunaan [Claude Enterprise Analytics API](/docs/id/api/admin/analytics) | Kunci Analytics API                    |

Organisasi induk Claude Enterprise tidak muncul di Claude Console dan tidak memiliki kunci Admin API, sehingga bagi mereka kunci Analytics API adalah satu-satunya jalur untuk mengakses data ini. Lihat [Analytics API](/docs/id/manage-claude/analytics-api) untuk cara membuat setiap jenis kunci dan paket mana yang berlaku untuk data biaya Claude Enterprise.

## Solusi mitra

Platform observabilitas terkemuka menawarkan integrasi siap pakai untuk memantau penggunaan dan biaya Claude API Anda, tanpa menulis kode kustom. Integrasi ini menyediakan dasbor, pemberitahuan, dan analitik untuk membantu Anda mengelola penggunaan API secara efektif.

<CardGroup cols={3}>
  <Card title="CloudZero" icon="chart" href="https://docs.cloudzero.com/docs/connections-anthropic">
    Platform intelijen cloud untuk melacak dan memperkirakan biaya
  </Card>

  <Card title="Datadog" icon="chart" href="https://docs.datadoghq.com/integrations/anthropic/">
    Observabilitas LLM dengan pelacakan dan pemantauan otomatis
  </Card>

  <Card title="Grafana Cloud" icon="chart" href="https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-anthropic/">
    Integrasi tanpa agen untuk observabilitas LLM yang mudah dengan dasbor dan peringatan siap pakai
  </Card>

  <Card title="Honeycomb" icon="polygon" href="https://docs.honeycomb.io/integrations/anthropic-usage-monitoring/">
    Kueri dan visualisasi tingkat lanjut melalui OpenTelemetry
  </Card>

  <Card title="Vantage" icon="chart" href="https://docs.vantage.sh/connecting_anthropic">
    Platform FinOps untuk observabilitas biaya & penggunaan LLM
  </Card>
</CardGroup>

## Mulai cepat

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

  ```text wrap
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Usage API

Lacak konsumsi token di seluruh organisasi Anda dengan rincian detail berdasarkan model, workspace, dan tingkat layanan menggunakan endpoint `/v1/organizations/usage_report/messages`.

### Konsep utama

* **Time buckets** (keranjang waktu): Agregasi data penggunaan dalam interval tetap (`1m`, `1h`, atau `1d`)
* **Pelacakan token**: Mengukur token input yang tidak di-cache, input yang di-cache, pembuatan cache, dan token output
* **Pemfilteran & pengelompokan**: Filter berdasarkan kunci API, workspace, model, tingkat layanan, jendela konteks, [residensi data](/docs/id/manage-claude/data-residency), atau kecepatan (beta), dan kelompokkan hasil berdasarkan dimensi-dimensi ini
* **Penggunaan alat server**: Lacak penggunaan alat sisi server seperti pencarian web

Untuk detail parameter lengkap dan skema respons, lihat [referensi Usage API](/docs/id/api/admin-api/usage-cost/get-messages-usage-report).

### Contoh dasar

#### Penggunaan harian berdasarkan model

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
group_by[]=model&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

#### Penggunaan per jam dengan pemfilteran

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

#### Filter penggunaan berdasarkan kunci API dan workspace

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

#### Residensi data

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

#### Fast mode (pratinjau riset)

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
  Baik filter `speeds[]` maupun nilai group\_by `speed` memerlukan header beta `fast-mode-2026-02-01`.
</Note>

### Batas granularitas waktu

| Granularitas | Batas Default | Batas Maksimum | Kasus Penggunaan         |
| ------------ | ------------- | -------------- | ------------------------ |
| `1m`         | 60 bucket     | 1440 bucket    | Pemantauan real-time     |
| `1h`         | 24 bucket     | 168 bucket     | Pola harian              |
| `1d`         | 7 bucket      | 31 bucket      | Laporan mingguan/bulanan |

## Cost API

Ambil rincian biaya tingkat layanan dalam USD dengan endpoint `/v1/organizations/cost_report`.

### Konsep utama

* **Mata uang**: Semua biaya dalam USD, dilaporkan sebagai string desimal dalam unit terkecil (sen)
* **Jenis biaya**: Lacak biaya penggunaan token, pencarian web, dan eksekusi kode
* **Pengelompokan**: Kelompokkan biaya berdasarkan workspace atau deskripsi untuk rincian detail. Saat mengelompokkan berdasarkan `description`, respons menyertakan field yang telah diurai seperti `model` dan `inference_geo`
* **Time buckets**: Hanya granularitas harian (`1d`)

Untuk detail parameter lengkap dan skema respons, lihat [referensi Cost API](/docs/id/api/admin-api/usage-cost/get-cost-report).

<Warning>
  Biaya Priority Tier menggunakan model penagihan yang berbeda dan tidak disertakan dalam endpoint biaya. Lacak penggunaan Priority Tier melalui endpoint penggunaan sebagai gantinya.
</Warning>

### Contoh dasar

```bash cURL
curl "https://api.anthropic.com/v1/organizations/cost_report?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
group_by[]=workspace_id&\
group_by[]=description" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Paginasi

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

## Kasus penggunaan umum

Jelajahi implementasi detail di [Claude Cookbook](https://platform.claude.com/cookbooks):

* **Laporan penggunaan harian**: Lacak tren konsumsi token
* **Atribusi biaya**: Alokasikan pengeluaran berdasarkan workspace untuk chargeback
* **Efisiensi cache**: Ukur dan optimalkan caching prompt
* **Pemantauan anggaran**: Siapkan peringatan untuk ambang batas pengeluaran
* **Ekspor CSV**: Hasilkan laporan untuk tim keuangan

## Pertanyaan yang sering diajukan

### Seberapa baru datanya?

Data penggunaan dan biaya biasanya muncul dalam 5 menit setelah permintaan API selesai, meskipun penundaan terkadang bisa lebih lama.

### Berapa frekuensi polling yang direkomendasikan?

API mendukung polling sekali per menit untuk penggunaan berkelanjutan. Untuk lonjakan singkat (misalnya, mengunduh data yang dipaginasi), polling yang lebih sering dapat diterima. Cache hasil untuk dasbor yang memerlukan pembaruan sering.

### Bagaimana cara melacak penggunaan eksekusi kode?

Biaya eksekusi kode muncul di endpoint biaya yang dikelompokkan di bawah `Code Execution Usage` dalam field deskripsi. Eksekusi kode tidak disertakan dalam endpoint penggunaan.

### Bagaimana cara melacak penggunaan Priority Tier?

Filter atau kelompokkan berdasarkan `service_tier` di endpoint penggunaan dan cari nilai `priority`. Biaya Priority Tier tidak tersedia di endpoint biaya.

### Apa yang terjadi dengan penggunaan Workbench?

Penggunaan API dari Workbench tidak terkait dengan kunci API, sehingga `api_key_id` akan bernilai `null` bahkan saat mengelompokkan berdasarkan dimensi tersebut.

### Bagaimana workspace default direpresentasikan?

Penggunaan dan biaya yang diatribusikan ke workspace default memiliki nilai `null` untuk `workspace_id`.

### Bagaimana cara mendapatkan rincian biaya per pengguna untuk Claude Code?

Gunakan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api), yang menyediakan estimasi biaya per pengguna dan metrik produktivitas tanpa keterbatasan performa dari merinci biaya berdasarkan banyak kunci API. Untuk penggunaan API umum dengan banyak kunci, gunakan [Usage API](#usage-api) untuk melacak konsumsi token sebagai proksi biaya.

## Lihat juga

Usage and Cost API dapat digunakan untuk membantu Anda memberikan pengalaman yang lebih baik bagi pengguna Anda, membantu Anda mengelola biaya, dan menjaga batas laju Anda. Pelajari lebih lanjut tentang beberapa fitur lainnya ini:

* [Admin API](/docs/id/manage-claude/admin-api)
* [Referensi Admin API](/docs/id/api/admin)
* [Analytics API](/docs/id/manage-claude/analytics-api) - API analitik dan jenis kunci mana yang dibutuhkan organisasi Anda
* [Harga](/docs/id/about-claude/pricing)
* [Caching prompt](/docs/id/build-with-claude/prompt-caching) - Optimalkan biaya dengan caching
* [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) - Diskon 50% untuk permintaan batch
* [Batas laju](/docs/id/api/rate-limits) - Pahami tingkatan penggunaan
* [Rate Limits API](/docs/id/manage-claude/rate-limits-api) - Baca batas laju yang dikonfigurasi untuk Anda
* [Residensi data](/docs/id/manage-claude/data-residency) - Kontrol geografi inferensi
