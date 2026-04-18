---
source: platform
url: https://platform.claude.com/docs/id/api/overview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 6f35a6368e2d1668eb24c5b3cfbb45767708dbd75f997c64139aac577cbcbc62
---

# Ikhtisar API

Pelajari tentang Claude API, termasuk autentikasi, SDK klien, dan endpoint yang tersedia.

---

Claude API adalah API RESTful di `https://api.anthropic.com` yang menyediakan akses terprogram ke model Claude dan Claude Managed Agents.

<Note>
**Baru mengenal Claude?** Untuk akses model langsung, mulai dengan [Memulai](/docs/id/get-started) dan [Bekerja dengan Messages](/docs/id/build-with-claude/working-with-messages). Untuk infrastruktur agen terkelola, lihat [Claude Managed Agents quickstart](/docs/id/managed-agents/quickstart).
</Note>

## Prasyarat

Untuk menggunakan Claude API, Anda memerlukan:

- Akun [Claude Console](https://platform.claude.com)
- [Kunci API](/settings/keys)

Untuk instruksi pengaturan langkah demi langkah, lihat [Memulai](/docs/id/get-started).

## API yang Tersedia

Claude API mencakup API berikut:

**Ketersediaan Umum:**
- **[Messages API](/docs/id/api/messages/create)**: Kirim pesan ke Claude untuk interaksi percakapan (`POST /v1/messages`)
- **[Message Batches API](/docs/id/api/creating-message-batches)**: Proses volume besar permintaan Messages secara asinkron dengan pengurangan biaya 50% (`POST /v1/messages/batches`)
- **[Token Counting API](/docs/id/api/messages-count-tokens)**: Hitung token dalam pesan sebelum mengirim untuk mengelola biaya dan batas laju (`POST /v1/messages/count_tokens`)
- **[Models API](/docs/id/api/models-list)**: Daftar model Claude yang tersedia dan detailnya (`GET /v1/models`)

**Beta:**
- **[Files API](/docs/id/api/files-create)**: Unggah dan kelola file untuk digunakan di berbagai panggilan API (`POST /v1/files`, `GET /v1/files`)
- **[Skills API](/docs/id/api/skills/create-skill)**: Buat dan kelola keterampilan agen kustom (`POST /v1/skills`, `GET /v1/skills`)
- **[Agents API](/docs/id/managed-agents/agent-setup)**: Tentukan konfigurasi agen yang dapat digunakan kembali dan berversi untuk Claude Managed Agents (`POST /v1/agents`, `GET /v1/agents`)
- **[Sessions API](/docs/id/managed-agents/sessions)**: Jalankan sesi agen stateful dalam kontainer cloud terkelola (`POST /v1/sessions`, `GET /v1/sessions/{id}/stream`)
- **[Environments API](/docs/id/managed-agents/environments)**: Konfigurasikan template kontainer untuk sesi agen (`POST /v1/environments`, `GET /v1/environments`)

Untuk referensi API lengkap dengan semua endpoint, parameter, dan skema respons, jelajahi halaman referensi API yang tercantum dalam navigasi. Untuk mengakses fitur beta, lihat [Beta headers](/docs/id/api/beta-headers).

## Autentikasi

Semua permintaan ke Claude API harus menyertakan header ini:

| Header | Nilai | Diperlukan |
|--------|-------|----------|
| `x-api-key` | Kunci API Anda dari Console | Ya |
| `anthropic-version` | Versi API (misalnya, `2023-06-01`) | Ya |
| `content-type` | `application/json` | Ya |

Jika Anda menggunakan [Client SDKs](#client-sdks), SDK akan mengirim header ini secara otomatis. Untuk detail versioning API, lihat [API versions](/docs/id/api/versioning).

### Mendapatkan Kunci API

API tersedia melalui [Console](https://platform.claude.com/) web. Anda dapat menggunakan [Workbench](https://platform.claude.com/workbench) untuk mencoba API di browser dan kemudian menghasilkan kunci API di [Account Settings](https://platform.claude.com/settings/keys). Gunakan [workspaces](https://platform.claude.com/settings/workspaces) untuk membagi kunci API Anda dan [mengontrol pengeluaran](/docs/id/api/rate-limits) berdasarkan kasus penggunaan.

## Client SDKs

Anthropic menyediakan SDK resmi yang menyederhanakan integrasi API dengan menangani autentikasi, pemformatan permintaan, penanganan kesalahan, dan banyak lagi.

**Manfaat**:
- Manajemen header otomatis (x-api-key, anthropic-version, content-type)
- Penanganan permintaan dan respons yang aman tipe
- Logika retry bawaan dan penanganan kesalahan
- Dukungan streaming
- Timeout permintaan dan manajemen koneksi

Untuk daftar SDK klien dan instruksi instalasi masing-masing, lihat [Client SDKs](/docs/id/api/client-sdks).

## Ketersediaan di platform mitra

Claude tersedia melalui Claude API langsung dan melalui platform mitra. Pilih berdasarkan infrastruktur, persyaratan kepatuhan, dan preferensi harga Anda.

### Claude API

- **Akses langsung** ke model dan fitur terbaru terlebih dahulu
- **Penagihan dan dukungan Anthropic**
- **Terbaik untuk**: Integrasi baru, akses fitur penuh, hubungan langsung dengan Anthropic

### API Platform Pihak Ketiga

Akses Claude melalui AWS, Google Cloud, atau Microsoft Azure:
- **Terintegrasi** dengan penagihan dan IAM penyedia cloud
- **Mungkin memiliki penundaan fitur** atau perbedaan dari API langsung
- **Terbaik untuk**: Komitmen cloud yang ada, persyaratan kepatuhan khusus, penagihan cloud terpadu

| Platform | Penyedia | Dokumentasi |
|----------|----------|---------------|
| Amazon Bedrock | AWS | [Claude on Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock) |
| Vertex AI | Google Cloud | [Claude on Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai) |
| Azure AI | Microsoft Azure | [Claude on Azure AI](/docs/id/build-with-claude/claude-in-microsoft-foundry) |

<Note>
Claude Managed Agents hanya tersedia melalui Claude API langsung. Untuk ketersediaan fitur di seluruh platform, lihat [Features overview](/docs/id/build-with-claude/overview).
</Note>

## Format Permintaan dan Respons

### Batas ukuran permintaan

| Endpoint | Ukuran permintaan maksimum |
| --- | --- |
| Messages, Token Counting | 32 MB |
| [Batch API](/docs/id/build-with-claude/batch-processing) | 256 MB |
| [Files API](/docs/id/build-with-claude/files) | 500 MB |
| Sessions, Agents, Environments | 32 MB |

Jika Anda melampaui batas ini, Anda akan menerima kesalahan 413 `request_too_large`.

<Note>
Platform pihak ketiga memiliki batas ukuran permintaan mereka sendiri: Vertex AI membatasi permintaan hingga 30 MB, dan Amazon Bedrock membatasi permintaan hingga 20 MB. Konsultasikan dokumentasi platform Anda untuk nilai saat ini.
</Note>

### Header Respons

Claude API menyertakan header berikut dalam setiap respons:

- `request-id`: Pengidentifikasi unik global untuk permintaan
- `anthropic-organization-id`: ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan

## Batas Laju dan Ketersediaan

### Batas Laju

API memberlakukan batas laju dan batas pengeluaran untuk mencegah penyalahgunaan dan mengelola kapasitas. Batas diatur ke dalam tingkat penggunaan yang meningkat secara otomatis saat Anda menggunakan API. Setiap tingkat memiliki:

- **Batas pengeluaran**: Biaya bulanan maksimum untuk penggunaan API
- **Batas laju**: Jumlah maksimum permintaan per menit (RPM) dan token per menit (TPM)

Anda dapat melihat batas organisasi Anda saat ini di [Console](/settings/limits). Untuk batas yang lebih tinggi atau Priority Tier (tingkat layanan yang ditingkatkan dengan pengeluaran berkomitmen), hubungi penjualan melalui Console.

Untuk informasi terperinci tentang batas, tingkat, dan algoritma token bucket yang digunakan untuk pembatasan laju, lihat [Rate limits](/docs/id/api/rate-limits).

### Ketersediaan

Claude API tersedia di [banyak negara dan wilayah](/docs/id/api/supported-regions) di seluruh dunia. Periksa halaman wilayah yang didukung untuk mengonfirmasi ketersediaan di lokasi Anda.

## Langkah Berikutnya

<CardGroup cols={2}>
  <Card title="Messages API reference" icon="book" href="/docs/id/api/messages/create">
    Spesifikasi API lengkap untuk interaksi model langsung
  </Card>
  <Card title="Claude Managed Agents reference" icon="brain" href="/docs/id/managed-agents/sessions">
    Endpoint Agents, Sessions, dan Environments
  </Card>
  <Card title="Client SDKs" icon="code" href="/docs/id/api/client-sdks">
    Python, TypeScript, Java, Go, C#, Ruby, dan PHP
  </Card>
  <Card title="Rate limits" icon="gauge" href="/docs/id/api/rate-limits">
    Tingkat penggunaan, batas pengeluaran, dan algoritma token bucket
  </Card>
</CardGroup>