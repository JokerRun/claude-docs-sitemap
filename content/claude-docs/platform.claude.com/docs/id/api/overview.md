---
source: platform
url: https://platform.claude.com/docs/id/api/overview
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 5e9c448cd1e39f01e3aa092ca45511fcee92f0822888dabcf9b24935515e6b3e
---

# Ikhtisar API

---

Claude API adalah RESTful API di `https://api.anthropic.com` yang menyediakan akses terprogram ke model Claude dan Claude Managed Agents.

<Note>
  **Baru mengenal Claude?** Untuk akses model langsung, mulailah dengan [Memulai](/docs/id/get-started) dan [Bekerja dengan Messages](/docs/id/build-with-claude/working-with-messages). Untuk infrastruktur agen terkelola, lihat [Panduan cepat Claude Managed Agents](/docs/id/managed-agents/quickstart).
</Note>

## Prasyarat

Untuk menggunakan Claude API, Anda memerlukan:

* [Akun Claude Console](https://platform.claude.com)
* [Kunci API](/settings/keys), atau aturan [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) yang telah dikonfigurasi

Untuk petunjuk penyiapan langkah demi langkah, lihat [Memulai](/docs/id/get-started).

## API yang tersedia

Claude API mencakup API berikut:

**Ketersediaan Umum:**

* **[Messages API](/docs/id/api/messages/create)**: Kirim pesan ke Claude untuk interaksi percakapan (`POST /v1/messages`)
* **[Message Batches API](/docs/id/api/messages/batches/create)**: Proses permintaan Messages dalam volume besar secara asinkron dengan pengurangan biaya 50% (`POST /v1/messages/batches`)
* **[Token Counting API](/docs/id/api/messages-count-tokens)**: Hitung token dalam pesan sebelum mengirim untuk mengelola biaya dan batas laju (`POST /v1/messages/count_tokens`)
* **[Models API](/docs/id/api/models/list)**: Daftar model Claude yang tersedia beserta detailnya (`GET /v1/models`)

**Beta:**

* **[Files API](/docs/id/api/beta/files/upload)**: Unggah dan kelola file untuk digunakan di berbagai panggilan API (`POST /v1/files`, `GET /v1/files`)
* **[Skills API](/docs/id/api/skills/create-skill)**: Buat dan kelola keterampilan agen kustom (`POST /v1/skills`, `GET /v1/skills`)
* **[Agents API](/docs/id/managed-agents/agent-setup)**: Definisikan konfigurasi agen yang dapat digunakan kembali dan berversi untuk Claude Managed Agents (`POST /v1/agents`, `GET /v1/agents`)
* **[Sessions API](/docs/id/managed-agents/sessions)**: Jalankan sesi agen stateful di sandbox cloud terkelola (`POST /v1/sessions`, `GET /v1/sessions/{id}/stream`)
* **[Environments API](/docs/id/managed-agents/environments)**: Konfigurasikan template sandbox untuk sesi agen (`POST /v1/environments`, `GET /v1/environments`)

Untuk referensi API lengkap dengan semua endpoint, parameter, dan skema respons, jelajahi halaman referensi API yang tercantum di navigasi. Untuk mengakses fitur beta, lihat [Header beta](/docs/id/api/beta-headers).

## Autentikasi

Untuk detail tentang kedua metode autentikasi dan kapan menggunakan masing-masing, lihat [Autentikasi](/docs/id/manage-claude/authentication). Semua permintaan ke Claude API harus menyertakan header berikut:

| Header              | Nilai                                                                                                                                                                                                        | Wajib                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| `x-api-key`         | Kunci API Anda dari Console                                                                                                                                                                                  | Salah satu dari `x-api-key` atau `Authorization` |
| `Authorization`     | `Bearer <token>`, di mana `<token>` adalah token akses berumur pendek yang diperoleh dari `POST /v1/oauth/token` melalui [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) | Salah satu dari `x-api-key` atau `Authorization` |
| `anthropic-version` | Versi API (misalnya, `2023-06-01`)                                                                                                                                                                           | Ya                                               |
| `content-type`      | `application/json`                                                                                                                                                                                           | Ya                                               |

Jika Anda menggunakan [Client SDK](#client-sdk), SDK akan mengirim header ini secara otomatis. Untuk detail versi API, lihat [Versi API](/docs/id/api/versioning).

Saat mengakses Claude melalui [platform cloud](#claude-api-vs-platform-cloud), autentikasi terintegrasi dengan sistem IAM penyedia cloud. Lihat dokumentasi khusus platform untuk jenis kredensial yang didukung, header yang diperlukan, dan opsi autentikasi.

### Mendapatkan kunci API

API tersedia melalui [Console](https://platform.claude.com/) berbasis web. Anda dapat menggunakan [Workbench](https://platform.claude.com/workbench) untuk mencoba API di browser dan kemudian membuat kunci API di [Pengaturan Akun](https://platform.claude.com/settings/keys). Gunakan [workspace](https://platform.claude.com/settings/workspaces) untuk mengelompokkan kunci API Anda dan [mengontrol pengeluaran](/docs/id/api/rate-limits) berdasarkan kasus penggunaan.

## Client SDK

Anthropic menyediakan SDK resmi yang menyederhanakan integrasi API dengan menangani autentikasi, pemformatan permintaan, penanganan kesalahan, dan lainnya.

**Manfaat:**

* Manajemen header otomatis (x-api-key, anthropic-version, content-type)
* Penanganan permintaan dan respons yang type-safe
* Logika retry dan penanganan kesalahan bawaan
* Dukungan streaming
* Timeout permintaan dan manajemen koneksi

Untuk daftar client SDK, lihat [Client SDK](/docs/id/cli-sdks-libraries/overview).

## Claude API vs platform cloud

Claude tersedia melalui Claude API langsung dan melalui platform cloud. Pilih berdasarkan infrastruktur, ketersediaan fitur, persyaratan kepatuhan, dan preferensi harga Anda.

### Claude API

* **Akses langsung** ke model dan fitur terbaru
* **Penagihan dan dukungan Anthropic**
* **Paling cocok untuk:** Integrasi baru, akses fitur penuh, hubungan langsung dengan Anthropic

### API platform cloud

Akses Claude melalui AWS, Google Cloud, atau Microsoft Azure:

* **Terintegrasi** dengan penagihan dan IAM penyedia cloud
* **Ketersediaan fitur bervariasi menurut platform:** Platform yang dioperasikan Anthropic mencakup [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry); platform yang dioperasikan mitra mencakup Amazon Bedrock dan Google Cloud. Lihat halaman masing-masing platform untuk ketersediaan dan waktu fitur.
* **Paling cocok untuk:** Komitmen cloud yang sudah ada, persyaratan kepatuhan tertentu, penagihan cloud terkonsolidasi

| Platform               | Penyedia                                 | Dokumentasi                                                                           |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------- |
| Claude Platform di AWS | AWS (dioperasikan Anthropic)             | [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)           |
| Amazon Bedrock         | AWS                                      | [Claude di Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)       |
| Agent Platform         | Google Cloud                             | [Claude di Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)              |
| Microsoft Foundry      | Microsoft Azure (dioperasikan Anthropic) | [Claude di Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) |

<Note>
  Claude Managed Agents tersedia melalui Claude API langsung dan [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws). Untuk ketersediaan fitur di seluruh platform, lihat [Ikhtisar fitur](/docs/id/build-with-claude/overview).
</Note>

## Format permintaan dan respons

### Batas ukuran permintaan

| Endpoint                                                           | Ukuran permintaan maksimum |
| ------------------------------------------------------------------ | -------------------------- |
| Messages, Token Counting                                           | 32 MB                      |
| [Message Batches API](/docs/id/build-with-claude/batch-processing) | 256 MB                     |
| [Files API](/docs/id/build-with-claude/files)                      | 500 MB                     |
| Sessions, Agents, Environments                                     | 32 MB                      |

Jika Anda melebihi batas ini, Anda akan menerima kesalahan 413 `request_too_large`.

<Note>
  Platform yang dioperasikan mitra memiliki batas ukuran permintaan mereka sendiri: Google Cloud membatasi permintaan hingga 30 MB, dan Bedrock membatasi permintaan hingga 20 MB. Claude Platform di AWS menggunakan batas yang sama dengan Claude API langsung. Konsultasikan dokumentasi platform Anda untuk nilai terkini.
</Note>

### Header respons

Claude API menyertakan header berikut di setiap respons:

* `request-id`: Pengidentifikasi unik global untuk permintaan
* `anthropic-organization-id`: ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan

<Note>
  Claude Platform di AWS menambahkan ID permintaan AWS (`x-amzn-requestid`) di samping header `request-id` standar. Lihat [ID Permintaan](/docs/id/build-with-claude/claude-platform-on-aws#request-ids) untuk pola penanganan ID ganda.
</Note>

## Paginasi

Endpoint list mengembalikan hasil dalam halaman. Sebagian besar endpoint list yang lebih baru menggunakan skema kursor `page` dan `next_page` yang dijelaskan di bagian ini. Beberapa menggunakan skema yang berbeda; lihat catatan di akhir bagian ini. Gunakan parameter kueri `limit` untuk mengontrol ukuran halaman dan parameter kueri `page` untuk mengambil halaman yang berdekatan. Setiap respons menyertakan array `data` beserta field kursor untuk menavigasi antar halaman.

| Nama        | Lokasi          | Deskripsi                                                                                                                                                                                                   |
| ----------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `limit`     | Parameter kueri | Jumlah maksimum item yang dikembalikan per halaman.                                                                                                                                                         |
| `page`      | Parameter kueri | Kursor opaque dari respons sebelumnya. Berikan nilai `next_page` atau `prev_page` di sini untuk mengambil halaman yang berdekatan.                                                                          |
| `order`     | Parameter kueri | Arah pengurutan untuk hasil (`asc` atau `desc`), pada endpoint list yang mendukung pengurutan. Kursor `page` hanya valid dengan `order` yang digunakan saat kursor tersebut dibuat.                         |
| `next_page` | Field respons   | Kursor untuk halaman berikutnya, atau `null` jika tidak ada hasil lagi.                                                                                                                                     |
| `prev_page` | Field respons   | Kursor untuk halaman sebelumnya pada endpoint yang mendukung paginasi mundur (saat ini `GET /v1/sessions`), atau `null` jika Anda berada di halaman pertama. Endpoint list lainnya menghilangkan field ini. |

Untuk kembali satu halaman, berikan `prev_page` sebagai parameter `page`. `prev_page` bernilai `null` ketika Anda berada di halaman pertama. Tidak semua endpoint list mendukung `prev_page`. Hanya `GET /v1/sessions` yang mengembalikan `prev_page`; pada endpoint list yang tidak mendukung paginasi mundur, field tersebut tidak ada dalam respons, bukan bernilai `null`. Untuk panduan permintaan, lihat [Mendaftar sesi](/docs/id/managed-agents/session-operations#listing-sessions).

Setiap SDK menyediakan iterator paginasi otomatis yang mengikuti `next_page` untuk Anda. Di Python dan TypeScript, Anda mendapatkannya dengan melakukan iterasi langsung pada hasil list. SDK lainnya menyediakan iterator melalui metode terpisah. Paginasi otomatis SDK hanya bergerak maju; untuk kembali satu halaman, baca `prev_page` dari respons dan berikan kembali sebagai parameter `page` secara manual. Lihat [client SDK](/docs/id/cli-sdks-libraries/overview) untuk detail spesifik bahasa.

<Note>
  Beberapa endpoint list menggunakan skema kursor yang berbeda. [Message Batches API](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [Models API](/docs/id/api/models/list), dan beberapa endpoint [Admin API](/docs/id/manage-claude/admin-api) menggunakan parameter kueri `after_id` dan `before_id` alih-alih `page`. Respons mereka mengembalikan `has_more`, `first_id`, dan `last_id` alih-alih `next_page`. Beberapa endpoint yang menggunakan skema `page`, seperti `GET /v1/skills`, juga mengembalikan Boolean `has_more` di samping `next_page`. Lihat halaman referensi untuk setiap endpoint untuk field paginasi yang tepat.
</Note>

## Batas laju dan ketersediaan

### Batas laju

API menerapkan batas laju dan batas pengeluaran untuk mencegah penyalahgunaan dan mengelola kapasitas. Batas diatur ke dalam tingkatan penggunaan; organisasi Anda ditempatkan pada suatu tingkatan secara otomatis dan dapat naik ke tingkatan yang lebih tinggi seiring waktu. Setiap tingkatan memiliki:

* **Batas pengeluaran**: Biaya bulanan maksimum untuk penggunaan API
* **Batas laju**: Jumlah maksimum permintaan per menit (RPM) dan token per menit (TPM)

Anda dapat melihat batas organisasi Anda saat ini di [Console](/settings/limits). Untuk batas yang lebih tinggi, gunakan **Request rate limit increase** di halaman [Limits](/settings/limits).

Untuk informasi terperinci tentang batas, tingkatan, dan algoritma token bucket yang digunakan untuk pembatasan laju, lihat [Batas laju](/docs/id/api/rate-limits).

### Ketersediaan

Claude API tersedia di [banyak negara dan wilayah](/docs/id/api/supported-regions) di seluruh dunia. Periksa halaman wilayah yang didukung untuk mengonfirmasi ketersediaan di lokasi Anda.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi Messages API" icon="book" href="/docs/id/api/messages/create">
    Spesifikasi API lengkap untuk interaksi model langsung
  </Card>

  <Card title="Referensi Claude Managed Agents" icon="brain" href="/docs/id/managed-agents/sessions">
    Endpoint Agents, Sessions, dan Environments
  </Card>

  <Card title="Client SDK" icon="code" href="/docs/id/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, dan Ruby
  </Card>

  <Card title="Batas laju" icon="gauge" href="/docs/id/api/rate-limits">
    Tingkatan penggunaan, meminta batas yang lebih tinggi, dan algoritma token bucket
  </Card>
</CardGroup>
