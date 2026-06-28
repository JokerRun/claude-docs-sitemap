---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/api-and-data-retention
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 2618f24c5a24bdcd0c8ced402b4173143b50dac21c0ff17f3fae7b6a3bb326e1
---

# API dan retensi data

Pelajari bagaimana API Anthropic dan fitur terkait menyimpan data, termasuk informasi tentang zero data retention (ZDR) dan akses API yang siap HIPAA.

---

<Note>
  Informasi tentang kebijakan retensi standar Anthropic tercantum dalam [kebijakan retensi data komersial Anthropic](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

  Anthropic menawarkan dua pengaturan penanganan data untuk Claude API:

  * **Zero data retention (ZDR):** Data pelanggan tidak disimpan dalam keadaan diam setelah respons API dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan.
  * **Kesiapan HIPAA:** Untuk organisasi yang menangani protected health information (PHI), Anthropic menawarkan akses API yang siap HIPAA dengan Business Associate Agreement (BAA) yang ditandatangani. Lihat [Kesiapan HIPAA](#hipaa-readiness).
</Note>

## Pendekatan Anthropic terhadap retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan dan retensi yang berbeda. Jika suatu API atau fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, API atau fitur tersebut mungkin memenuhi syarat untuk ZDR. Jika suatu API atau fitur memang memerlukan penyimpanan prompt atau respons pelanggan, Anthropic merancangnya dengan jejak retensi sekecil mungkin. Untuk fitur-fitur ini:

* Data yang disimpan tidak pernah digunakan untuk pelatihan model tanpa izin eksplisit Anda.
* Hanya data yang secara teknis diperlukan agar API dan fitur dapat berfungsi yang disimpan. Konten percakapan (prompt Anda dan output Claude) tidak disimpan secara default. Model tertentu memerlukan retensi data 30 hari; lihat [Persyaratan retensi data khusus model](#model-specific-data-retention-requirements).
* Data dihapus dengan TTL sesingkat mungkin secara praktis, dan Anthropic berupaya memberikan kontrol kepada pelanggan atas berapa lama data disimpan. Apa yang disimpan, dan durasi retensi ketika TTL tertentu berlaku, didokumentasikan di halaman masing-masing fitur.

Data yang dapat diakses melalui [Compliance API](/docs/id/manage-claude/compliance-api) mengikuti model retensinya sendiri. [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) menyimpan data selama 6 tahun. Konten chat, file, dan proyek dari claude.ai mengikuti kebijakan retensi organisasi Anda, yang diatur di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls).

Dalam [tabel kelayakan fitur](#feature-eligibility), beberapa fitur ditandai "Ya (dengan kualifikasi)" di kolom kelayakan ZDR. Jika organisasi Anda memiliki pengaturan ZDR, Anda dapat menggunakan fitur-fitur ini dengan keyakinan bahwa apa yang disimpan Anthropic bersifat terbatas dan diperlukan untuk kinerja optimal.

## Cakupan zero data retention (ZDR)

<Warning>
  Claude Fable 5 dan Claude Mythos 5 tidak tersedia di bawah ZDR; lihat [Persyaratan retensi data khusus model](#model-specific-data-retention-requirements).
</Warning>

**Apa yang dicakup ZDR**

* **API Claude tertentu:** ZDR berlaku untuk Claude Messages API dan Token Counting API.
* **Claude Code:** ZDR berlaku ketika digunakan dengan kunci API organisasi Komersial atau melalui Claude Enterprise (lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention))

**Apa yang TIDAK dicakup ZDR**

* **Console dan Workbench:** Penggunaan apa pun di Console atau Workbench
* **Claude Managed Agents:** Claude Managed Agents adalah sumber daya yang bersifat stateful. Anda dapat menghapus transkrip sesi, tetapi tidak ada penghapusan otomatis.
* **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max, termasuk ketika pelanggan pada paket tersebut menggunakan aplikasi web, desktop, atau seluler Claude, atau Claude Code
* **Claude Teams dan Claude Enterprise:** Antarmuka produk Claude Teams dan Claude Enterprise **tidak memenuhi syarat ZDR**, kecuali untuk Claude Code ketika digunakan melalui Claude Enterprise dengan ZDR yang diaktifkan untuk organisasi tersebut. Untuk antarmuka produk lainnya, hanya kunci API organisasi Komersial yang memenuhi syarat untuk ZDR.
* **Integrasi pihak ketiga:** Data yang diproses oleh situs web, alat, atau integrasi pihak ketiga lainnya **tidak memenuhi syarat ZDR**, meskipun beberapa mungkin memiliki penawaran serupa. Saat menggunakan layanan eksternal bersama dengan Claude API, pastikan untuk meninjau praktik penanganan data layanan tersebut.

<Note>
  Untuk informasi terbaru tentang produk dan fitur apa saja yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Persyaratan retensi data khusus model

Claude Fable 5 dan Claude Mythos 5 ditetapkan sebagai [Covered Models](https://support.claude.com/en/articles/15425695) dan memerlukan retensi data 30 hari. Zero data retention tidak tersedia untuk Claude Fable 5 atau Claude Mythos 5. Permintaan ke salah satu model tersebut dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini akan mengembalikan `400 invalid_request_error`.

Persyaratan ini berlaku pada Claude API. Untuk Claude Fable 5 di Amazon Bedrock, Vertex AI, dan Microsoft Foundry, persyaratan retensi data ditetapkan oleh masing-masing platform.

Organisasi dengan pengaturan ZDR dapat mengonfigurasi retensi data di tingkat workspace di [Claude Console > Settings > Workspaces](https://platform.claude.com/settings/workspaces): buka tab **Privacy controls** pada suatu workspace dan aktifkan retensi data 30 hari untuk workspace tersebut. Ini membuat Claude Fable 5 dan Claude Mythos 5 tersedia di workspace yang ditentukan sementara workspace lain dalam organisasi tetap menggunakan zero data retention. Workspace tanpa pengaturan khusus akan mengikuti default organisasi.

## Kesiapan HIPAA

Claude API mendukung integrasi yang siap HIPAA untuk organisasi yang menangani protected health information (PHI). Dengan BAA yang ditandatangani dan organisasi yang mengaktifkan HIPAA, Anda dapat menggunakan fitur API yang didukung untuk memproses PHI sambil mendukung kepatuhan HIPAA organisasi Anda.

Sebelumnya, organisasi yang memerlukan kesiapan HIPAA untuk Claude API perlu mengaktifkan ZDR. Akses API yang siap HIPAA menghilangkan persyaratan ini dan menyediakan fondasi bagi Anthropic untuk secara bertahap mengaktifkan fitur tambahan seiring fitur-fitur tersebut diaudit untuk kesiapan HIPAA.

<Note>
  Halaman ini membahas kesiapan HIPAA untuk Claude API. Untuk Panduan Implementasi HIPAA lengkap yang mencakup Claude Enterprise dan persyaratan konfigurasi, lihat [Anthropic Trust Center](https://trust.anthropic.com/resources).
</Note>

### Memulai

Untuk menyiapkan akses API yang siap HIPAA:

<Steps>
  <Step title="Tanda tangani Business Associate Agreement">
    Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk menandatangani BAA yang mencakup penggunaan API.
  </Step>

  <Step title="Sediakan organisasi yang mengaktifkan HIPAA">
    Anthropic menyediakan organisasi khusus dengan kontrol kesiapan HIPAA yang diaktifkan. Organisasi ini secara otomatis menerapkan pembatasan fitur, memblokir permintaan API yang menggunakan fitur yang tidak memenuhi syarat.
  </Step>

  <Step title="Bangun dengan fitur yang memenuhi syarat">
    Gunakan [tabel kelayakan fitur](#feature-eligibility) untuk mengonfirmasi fitur mana yang didukung. Tinjau [pedoman penanganan PHI](#phi-handling-guidelines) untuk fitur yang memerlukan pembatasan khusus tentang di mana PHI dapat muncul. Untuk persyaratan konfigurasi dan kepatuhan yang terperinci, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).
  </Step>
</Steps>

<Warning>
  Kesiapan HIPAA diterapkan di tingkat organisasi. Jika Anda memerlukan akses API yang siap HIPAA dan akses API untuk tujuan umum, gunakan organisasi terpisah untuk masing-masing.
</Warning>

### Cakupan kesiapan HIPAA

**Apa yang dicakup kesiapan HIPAA**

* **Claude API:** Kesiapan HIPAA berlaku untuk Claude API (`api.anthropic.com`) untuk fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](#feature-eligibility).

**Apa yang TIDAK dicakup kesiapan HIPAA**

* **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max
* **Console dan Workbench:** Penggunaan melalui antarmuka Claude Console
* **Platform yang dioperasikan mitra:** Amazon Bedrock atau Vertex AI (lihat dokumentasi kepatuhan platform tersebut)
* **Claude Platform di AWS dan Microsoft Foundry:** Kesiapan HIPAA tidak tersedia
* **Integrasi pihak ketiga:** Data yang diproses oleh alat atau layanan eksternal yang terhubung ke aplikasi Anda
* **Claude Code:** Claude Code tidak dicakup dalam kesiapan HIPAA
* **Fitur beta:** Fitur dalam tahap beta umumnya tidak dicakup dalam BAA kecuali secara eksplisit tercantum sebagai memenuhi syarat dalam [tabel kelayakan fitur](#feature-eligibility)

### Pedoman penanganan PHI

Protected health information (PHI) mencakup informasi kesehatan apa pun yang dapat diidentifikasi secara individual. Dalam konteks Claude API, PHI biasanya muncul dalam:

* Konten pesan (prompt dan respons dari Claude)
* File terlampir (gambar, PDF)
* Nama file dan metadata yang terkait dengan konten pesan

Bidang berikut tidak diharapkan mengandung PHI berdasarkan BAA: nama workspace, informasi pengguna (nama, email, nomor telepon), data penagihan, dan tiket dukungan.

#### Pembatasan skema dan definisi alat

Saat menggunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau alat dengan `strict: true`, API mengompilasi skema JSON menjadi grammar yang di-cache secara terpisah dari konten pesan. Skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons.

**Jangan sertakan PHI dalam definisi skema JSON.** Pembatasan ini berlaku untuk:

* Nama properti skema
* Nilai `enum`
* Nilai `const`
* Ekspresi reguler `pattern`

Informasi spesifik pasien hanya boleh muncul dalam konten pesan, di mana informasi tersebut dilindungi di bawah pengamanan HIPAA.

### Penanganan error HIPAA

BAA yang Anda tanda tangani adalah sumber kebenaran resmi untuk fitur mana yang dicakup. API juga menerapkan pembatasan ini secara otomatis: ketika organisasi yang mengaktifkan HIPAA mengirim permintaan yang menyertakan fitur yang tidak memenuhi syarat, API mengembalikan error `400` untuk mencegah penggunaan fitur yang tidak dicakup oleh BAA Anda secara tidak sengaja:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

Pesan error mencantumkan fitur yang tidak memenuhi syarat yang terdeteksi dalam permintaan. Hapus fitur-fitur ini dari permintaan Anda dan coba lagi.

## Kelayakan fitur

Tabel berikut mencantumkan fitur Claude API mana yang memenuhi syarat untuk pengaturan ZDR dan kesiapan HIPAA. Untuk organisasi yang mengaktifkan HIPAA, fitur yang ditandai "Tidak" di kolom HIPAA diblokir secara otomatis, dan permintaan yang menyertakannya akan mengembalikan error `400`.

| Fitur                                                                                       | Endpoint                                         | Memenuhi syarat ZDR                                             | Memenuhi syarat HIPAA                  | Detail                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Messages API](/docs/id/build-with-claude/working-with-messages)                            | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Panggilan API standar untuk menghasilkan respons Claude.                                                                                                                                                                                                                                                                                                                          |
| [Penghitungan token](/docs/id/build-with-claude/token-counting)                             | `/v1/messages/count_tokens`                      | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Hitung token sebelum mengirim permintaan.                                                                                                                                                                                                                                                                                                                                         |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool)                         | `/v1/messages` (dengan alat `web_search`)        | <Eligible>Ya</Eligible>1                                        | <Eligible>Ya</Eligible>1               | Hasil pencarian web real-time dikembalikan dalam respons API.                                                                                                                                                                                                                                                                                                                     |
| [Web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool)                              | `/v1/messages` (dengan alat `web_fetch`)         | <Eligible>Ya</Eligible>1 2                                      | <Eligible status="no">Tidak</Eligible> | Konten web yang diambil dikembalikan dalam respons API.                                                                                                                                                                                                                                                                                                                           |
| [Alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool)                             | `/v1/messages` (dengan alat `advisor`)           | <Eligible>Ya</Eligible>                                         | <Eligible status="no">Tidak</Eligible> | Output model advisor dikembalikan dalam respons API; tidak ada yang disimpan di sisi server setelah respons.                                                                                                                                                                                                                                                                      |
| [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool)                               | `/v1/messages` (dengan alat `memory`)            | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Penyimpanan memori sisi klien di mana Anda mengontrol retensi data.                                                                                                                                                                                                                                                                                                               |
| [Manajemen konteks (compaction)](/docs/id/build-with-claude/compaction)                     | `/v1/messages` (dengan `context_management`)     | <Eligible>Ya</Eligible>                                         | <Eligible status="no">Tidak</Eligible> | Hasil compaction sisi server dikembalikan/dikirim bolak-balik secara stateless melalui respons API.                                                                                                                                                                                                                                                                               |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing)                            | `/v1/messages` (dengan `context_management`)     | <Eligible>Ya</Eligible>                                         | <Eligible status="no">Tidak</Eligible> | Pengeditan konteks (pembersihan tool use + pembersihan thinking) diterapkan secara real time.                                                                                                                                                                                                                                                                                     |
| [Mode cepat](/docs/id/build-with-claude/fast-mode)                                          | `/v1/messages` (dengan `speed: "fast"`)          | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan.                                                                                                                                                                                                                                                                     |
| [Jendela konteks 1 juta token](/docs/id/build-with-claude/context-windows)                  | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Pemrosesan konteks yang diperluas menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                               |
| [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking)                           | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Kedalaman pemikiran dinamis menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                     |
| [Sitasi](/docs/id/build-with-claude/citations)                                              | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Atribusi sumber menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                                 |
| [Residensi data](/docs/id/manage-claude/data-residency)                                     | `/v1/messages` (dengan `inference_geo`)          | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Perutean geografis menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                              |
| [Effort](/docs/id/build-with-claude/effort)                                                 | `/v1/messages` (dengan `effort`)                 | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Kontrol efisiensi token menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                         |
| [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking)                      | `/v1/messages` (dengan `thinking`)               | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Penalaran langkah demi langkah menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                  |
| [Dukungan PDF](/docs/id/build-with-claude/pdf-support)                                      | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Pemrosesan dokumen PDF menggunakan Messages API standar. Kelayakan HIPAA berlaku untuk PDF yang dikirim secara inline melalui Messages API, bukan melalui Files API.                                                                                                                                                                                                              |
| [Hasil pencarian](/docs/id/build-with-claude/search-results)                                | `/v1/messages` (dengan sumber `search_results`)  | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Dukungan sitasi RAG menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                             |
| [Alat bash](/docs/id/agents-and-tools/tool-use/bash-tool)                                   | `/v1/messages` (dengan alat `bash`)              | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Alat sisi klien yang dieksekusi di lingkungan Anda.                                                                                                                                                                                                                                                                                                                               |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool)                     | `/v1/messages` (dengan alat `text_editor`)       | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Alat sisi klien yang dieksekusi di lingkungan Anda.                                                                                                                                                                                                                                                                                                                               |
| [Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool)                        | `/v1/messages` (dengan alat `computer`)          | <Eligible>Ya</Eligible>                                         | <Eligible status="no">Tidak</Eligible> | Alat sisi klien di mana tangkapan layar dan file ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Lihat [Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention).                                                                                                                                                                      |
| [Streaming alat terperinci](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Streaming parameter alat menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                        |
| [Caching prompt](/docs/id/build-with-claude/prompt-caching)                                 | `/v1/messages`                                   | <Eligible>Ya</Eligible>                                         | <Eligible>Ya</Eligible>                | Prompt Anda dan output Claude tidak disimpan. Representasi KV cache dan hash kriptografis disimpan dalam memori selama TTL cache dan segera dihapus setelah kedaluwarsa. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#data-retention).                                                                                                                        |
| [Structured outputs](/docs/id/build-with-claude/structured-outputs)                         | `/v1/messages`                                   | <Eligible status="qualified">Ya (dengan kualifikasi)</Eligible> | <Eligible>Ya</Eligible>3               | Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang di-cache, hingga 24 jam sejak penggunaan terakhir. Ini juga mencakup [strict tool use](/docs/id/agents-and-tools/tool-use/strict-tool-use) (`strict: true` pada alat), yang menggunakan pipeline grammar yang sama. Lihat [Structured outputs](/docs/id/build-with-claude/structured-outputs#data-retention). |
| [Diagnostik cache](/docs/id/build-with-claude/cache-diagnostics)                            | `/v1/messages` (dengan `diagnostics`)            | <Eligible status="qualified">Ya (dengan kualifikasi)</Eligible> | <Eligible status="no">Tidak</Eligible> | Prompt Anda dan output Claude tidak disimpan. Sidik jari berupa hash kriptografis dan estimasi jumlah token disimpan sebentar untuk memungkinkan perbandingan dengan permintaan berikutnya. Lihat [Diagnostik cache](/docs/id/build-with-claude/cache-diagnostics#data-retention).                                                                                                |
| [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)                       | `/v1/messages` (dengan alat `tool_search`)       | <Eligible>Ya</Eligible>                                         | <Eligible status="no">Tidak</Eligible> | Pencarian alat menggunakan Messages API standar.                                                                                                                                                                                                                                                                                                                                  |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)                             | `/v1/messages/batches`                           | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Retensi 29 hari; penyimpanan async diperlukan. Lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing#data-retention).                                                                                                                                                                                                                                              |
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)                     | `/v1/messages` (dengan alat `code_execution`)    | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Data kontainer disimpan hingga 30 hari. Lihat [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention).                                                                                                                                                                                                                                             |
| [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | `/v1/messages` (dengan alat `code_execution`)    | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Dibangun di atas kontainer eksekusi kode; data disimpan hingga 30 hari. Lihat [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention).                                                                                                                                                                                         |
| [Files API](/docs/id/build-with-claude/files)                                               | `/v1/files`                                      | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | File disimpan hingga dihapus secara eksplisit. Lihat [Files API](/docs/id/build-with-claude/files#data-retention).                                                                                                                                                                                                                                                                |
| [Agent skills](/docs/id/agents-and-tools/agent-skills/overview)                             | `/v1/messages` (dengan `skills`) / `/v1/skills`  | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Data skill disimpan sesuai kebijakan standar. Lihat [Agent skills](/docs/id/agents-and-tools/agent-skills/overview#data-retention).                                                                                                                                                                                                                                               |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector)                                     | `/v1/messages` (dengan `mcp_servers`)            | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Data disimpan sesuai kebijakan standar. Lihat [Konektor MCP](/docs/id/agents-and-tools/mcp-connector#data-retention).                                                                                                                                                                                                                                                             |
| [Claude Managed Agents](/docs/id/managed-agents/overview)                                   | `/v1/agents`, `/v1/sessions`, `/v1/environments` | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Sesi adalah sumber daya stateful; transkrip tetap ada hingga Anda menghapusnya. Berlaku untuk semua sub-fitur Managed Agents, termasuk [Self-hosted sandboxes](/docs/id/managed-agents/self-hosted-sandboxes).                                                                                                                                                                    |
| [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview)                               | `/v1/organizations/tunnels`                      | <Eligible status="no">Tidak</Eligible>                          | <Eligible status="no">Tidak</Eligible> | Pratinjau riset. Lihat [Keamanan MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/security) untuk batasan aliran data dan detail subprosesor.                                                                                                                                                                                                                                   |

1 [Pemfilteran dinamis](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) tidak memenuhi syarat untuk ZDR atau HIPAA.

2 Meskipun web fetch memenuhi syarat ZDR, penerbit situs web dapat menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai dengan kebijakan mereka sendiri.

3 PHI tidak boleh disertakan dalam definisi skema JSON. Lihat [Pedoman penanganan PHI](#phi-handling-guidelines).

## Batasan dan pengecualian

### CORS tidak didukung untuk ZDR

**Cross-Origin Resource Sharing (CORS)** tidak didukung untuk organisasi dengan pengaturan ZDR. Jika Anda perlu melakukan panggilan API dari aplikasi berbasis browser, Anda harus:

* Menggunakan server proxy backend untuk melakukan panggilan API atas nama front end Anda
* Mengimplementasikan penanganan CORS Anda sendiri di server proxy
* Jangan pernah mengekspos kunci API secara langsung di JavaScript browser

### Retensi data untuk pelanggaran kebijakan dan jika diwajibkan oleh hukum

Bahkan dengan pengaturan ZDR atau HIPAA yang berlaku, Anthropic dapat menyimpan data jika diwajibkan oleh hukum atau untuk memerangi pelanggaran Kebijakan Penggunaan dan penggunaan berbahaya terhadap platform Anthropic. Akibatnya, jika suatu chat atau sesi ditandai karena pelanggaran tersebut, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Bagaimana saya tahu apakah organisasi saya memiliki pengaturan ZDR?">
    Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan fitur yang memenuhi syarat ZDR (dengan kualifikasi) di bawah pengaturan ZDR saya?">
    Ya. Fitur-fitur ini menyimpan sekumpulan data teknis yang minimal dan terdokumentasi, bukan prompt Anda atau output Claude. Lihat [Pendekatan Anthropic terhadap retensi data](#anthropics-approach-to-data-retention) untuk komitmen yang mengatur fitur-fitur ini.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang ditandai &#x22;Tidak&#x22; di bawah ZDR?">
    Fitur yang ditandai "Tidak" untuk ZDR pada dasarnya bersifat stateful: Batch API menyimpan pekerjaan Anda, Files API menyimpan file Anda, dan eksekusi kode berjalan dalam kontainer persisten. Data untuk fitur-fitur ini disimpan sesuai kebijakan yang didokumentasikan untuk fitur tersebut. Menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data spesifik tersebut.
  </Accordion>

  <Accordion title="Dapatkah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">
    Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan opsi penghapusan untuk fitur non-ZDR.
  </Accordion>

  <Accordion title="Apa perbedaan kesiapan HIPAA dengan ZDR?">
    ZDR mencegah data pelanggan disimpan dalam keadaan diam setelah respons API dikembalikan. Kesiapan HIPAA melibatkan serangkaian pengamanan privasi dan keamanan yang lebih luas yang melindungi PHI sepanjang siklus hidupnya, termasuk enkripsi, kontrol akses, dan pencatatan audit. Akses API yang siap HIPAA menyediakan fondasi untuk secara bertahap mengaktifkan lebih banyak fitur karena data dapat disimpan dengan pengamanan yang tepat alih-alih memerlukan penghapusan segera.
  </Accordion>

  <Accordion title="Apakah saya masih memerlukan ZDR jika saya memiliki kesiapan HIPAA?">
    Tidak. Akses API yang siap HIPAA dirancang sebagai alternatif untuk ZDR bagi organisasi yang menangani PHI. Dengan kesiapan HIPAA yang diaktifkan, Anda mendapatkan akses ke fitur API yang didukung sambil mempertahankan perlindungan privasi dan keamanan yang diwajibkan HIPAA.
  </Accordion>

  <Accordion title="Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat di bawah HIPAA?">
    API mengembalikan error `400` dengan tipe `invalid_request_error`. Pesan error mengidentifikasi fitur mana yang tidak tersedia. Hapus fitur yang tidak memenuhi syarat dari permintaan Anda dan coba lagi.
  </Accordion>

  <Accordion title="Dapatkah saya menggunakan organisasi yang sama untuk beban kerja HIPAA dan non-HIPAA?">
    Tidak. Kesiapan HIPAA diterapkan di tingkat organisasi dan secara otomatis memblokir semua fitur yang tidak memenuhi syarat. Gunakan organisasi terpisah untuk beban kerja yang tidak memerlukan kesiapan HIPAA.
  </Accordion>

  <Accordion title="Bagaimana cara meminta akses API yang siap HIPAA?">
    Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk mendiskusikan akses API yang siap HIPAA dan menandatangani Business Associate Agreement.
  </Accordion>

  <Accordion title="Apakah ini berlaku untuk Amazon Bedrock atau Vertex AI?">
    Tidak. Pengaturan ZDR dan HIPAA yang dijelaskan di halaman ini berlaku untuk Claude API, di mana Anthropic adalah pemroses data. Di Bedrock dan Vertex AI, penyedia cloud adalah pemroses data; lihat kebijakan retensi data dan kepatuhan platform tersebut untuk kontrol setara mereka.
  </Accordion>

  <Accordion title="Apakah Claude Platform di AWS memenuhi syarat untuk ZDR atau kesiapan HIPAA?">
    Claude Platform di AWS mengikuti kebijakan retensi data yang sama dengan Claude API pihak pertama. ZDR tersedia berdasarkan permintaan; hubungi perwakilan akun Anthropic Anda untuk mengaktifkannya. Kesiapan HIPAA tidak tersedia di Claude Platform di AWS. Lihat [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) untuk detailnya.
  </Accordion>

  <Accordion title="Apakah Claude Code memenuhi syarat untuk ZDR?">
    Claude Code memenuhi syarat untuk ZDR melalui dua jalur:

    * **Kunci API:** Claude Code yang digunakan dengan kunci API bayar sesuai pemakaian dari organisasi Komersial
    * **Claude Enterprise:** Claude Code yang digunakan melalui Claude Enterprise dengan ZDR yang diaktifkan untuk organisasi tersebut

    ZDR diaktifkan per organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda. ZDR tidak secara otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

    Selain itu, jika Anda mengaktifkan pencatatan metrik di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat disimpan.

    Untuk detail lengkap tentang ZDR untuk Claude Code di Claude Enterprise, termasuk fitur yang dinonaktifkan dan cara meminta pengaktifan, lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention).
  </Accordion>

  <Accordion title="Apakah Claude for Excel mendukung ZDR?">
    Tidak, Claude for Excel saat ini tidak memenuhi syarat ZDR.
  </Accordion>

  <Accordion title="Bagaimana cara meminta ZDR?">
    Untuk meminta pengaturan ZDR, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Kebijakan Privasi](https://www.anthropic.com/legal/privacy)
* [Structured outputs](/docs/id/build-with-claude/structured-outputs)
* [Caching prompt](/docs/id/build-with-claude/prompt-caching)
* [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)
* [Files API](/docs/id/api/files-create)
* [Trust Center](https://trust.anthropic.com/resources)
