---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/api-and-data-retention
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 7512523ee55308cba99f148c87b310f75a8c838d638ae4db2af4ddefc7ca9be0
---

# Retensi API dan data

Pelajari tentang bagaimana API Anthropic dan fitur terkait mempertahankan data, termasuk informasi tentang retensi data nol (ZDR) dan akses API siap HIPAA.

---

<Note>
Informasi tentang kebijakan retensi standar Anthropic dijelaskan dalam [kebijakan retensi data komersial Anthropic](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

Anthropic menawarkan dua pengaturan penanganan data untuk Claude API:
- **Retensi data nol (ZDR):** Data pelanggan tidak disimpan saat istirahat setelah respons API dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan.
- **Kesiapan HIPAA:** Untuk organisasi yang menangani informasi kesehatan yang dilindungi (PHI), Anthropic menawarkan akses API siap HIPAA dengan Perjanjian Mitra Bisnis (BAA) yang ditandatangani. Lihat [Kesiapan HIPAA](#hipaa-readiness).
</Note>

## Pendekatan Anthropic terhadap retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan dan retensi yang berbeda. Jika API atau fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, mungkin memenuhi syarat untuk ZDR. Jika API atau fitur harus menyimpan prompt atau respons pelanggan, Anthropic merancang jejak retensi sekecil mungkin. Untuk fitur-fitur ini:

- Data yang dipertahankan tidak pernah digunakan untuk pelatihan model tanpa izin eksplisit Anda.
- Hanya apa yang secara teknis diperlukan untuk API dan fitur bekerja yang dipertahankan. Konten percakapan (prompt Anda dan output Claude) tidak pernah dipertahankan kecuali jika secara eksplisit dicatat.
- Data dihapus pada TTL terpendek yang praktis, dan Anthropic bertujuan untuk memberikan pelanggan kontrol atas berapa lama data dipertahankan. Apa yang disimpan, dan durasi retensi di mana TTL tertentu berlaku, didokumentasikan di halaman setiap fitur.

Dalam [tabel kelayakan fitur](#feature-eligibility), beberapa fitur ditandai "Ya (qualified)" di kolom ZDR eligible. Jika organisasi Anda memiliki pengaturan ZDR, Anda dapat menggunakan fitur-fitur ini dengan percaya diri bahwa apa yang Anthropic pertahankan sempit dan diperlukan untuk kinerja optimal.

## Cakupan retensi data nol (ZDR)

**Apa yang dicakup ZDR**

- **API Claude tertentu:** ZDR berlaku untuk Claude Messages dan Token Counting APIs
- **Claude Code:** ZDR berlaku saat digunakan dengan kunci API organisasi Komersial atau melalui Claude Enterprise (lihat [dokumentasi Claude Code ZDR](https://code.claude.com/docs/en/zero-data-retention))

**Apa yang TIDAK dicakup ZDR**

- **Console dan Workbench:** Penggunaan apa pun di Console atau Workbench
- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max, termasuk ketika pelanggan di paket tersebut menggunakan aplikasi web, desktop, atau mobile Claude atau Claude Code
- **Claude Teams dan Claude Enterprise:** Antarmuka produk Claude Teams dan Claude Enterprise **tidak memenuhi syarat ZDR**, kecuali untuk Claude Code saat digunakan melalui Claude Enterprise dengan ZDR diaktifkan untuk organisasi. Untuk antarmuka produk lainnya, hanya kunci API organisasi Komersial yang memenuhi syarat untuk ZDR.
- **Integrasi pihak ketiga:** Data yang diproses oleh situs web pihak ketiga, alat, atau integrasi lainnya **tidak memenuhi syarat ZDR**, meskipun beberapa mungkin memiliki penawaran serupa. Saat menggunakan layanan eksternal bersama dengan Claude API, pastikan untuk meninjau praktik penanganan data layanan tersebut.

<Note>
Untuk informasi terbaru tentang produk dan fitur mana yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kesiapan HIPAA

Claude API mendukung integrasi siap HIPAA untuk organisasi yang menangani informasi kesehatan yang dilindungi (PHI). Dengan BAA yang ditandatangani dan organisasi yang diaktifkan HIPAA, Anda dapat menggunakan fitur API yang didukung untuk memproses PHI sambil mendukung kepatuhan HIPAA organisasi Anda.

Sebelumnya, organisasi yang memerlukan kesiapan HIPAA untuk Claude API perlu mengaktifkan ZDR. Akses API siap HIPAA menghilangkan persyaratan ini dan memberikan fondasi bagi Anthropic untuk secara progresif mengaktifkan fitur tambahan saat diaudit untuk kesiapan HIPAA.

<Note>
Halaman ini mencakup kesiapan HIPAA untuk Claude API. Untuk Panduan Implementasi HIPAA lengkap yang mencakup Claude Enterprise, Claude Code, dan persyaratan konfigurasi, lihat [Pusat Kepercayaan Anthropic](https://trust.anthropic.com/resources).
</Note>

### Memulai

Untuk menyiapkan akses API siap HIPAA:

<Steps>
<Step title="Menandatangani Perjanjian Mitra Bisnis">
Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk menandatangani BAA yang mencakup penggunaan API.
</Step>
<Step title="Menyediakan organisasi yang diaktifkan HIPAA">
Anthropic menyediakan organisasi khusus dengan kontrol kesiapan HIPAA diaktifkan. Organisasi ini secara otomatis memberlakukan pembatasan fitur, memblokir permintaan API yang menggunakan fitur yang tidak memenuhi syarat.
</Step>
<Step title="Membangun dengan fitur yang memenuhi syarat">
Gunakan [tabel kelayakan fitur](#feature-eligibility) untuk mengonfirmasi fitur mana yang didukung. Tinjau [panduan penanganan PHI](#phi-handling-guidelines) untuk fitur yang memerlukan pembatasan khusus tentang di mana PHI dapat muncul. Untuk persyaratan konfigurasi dan kepatuhan terperinci, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).
</Step>
</Steps>

<Warning>
Kesiapan HIPAA diberlakukan di tingkat organisasi. Jika Anda memerlukan akses API siap HIPAA dan tujuan umum, gunakan organisasi terpisah untuk masing-masing.
</Warning>

### Cakupan kesiapan HIPAA

**Apa yang dicakup kesiapan HIPAA**

- **Claude API:** Kesiapan HIPAA berlaku untuk Claude API (`api.anthropic.com`) untuk fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](#feature-eligibility).

**Apa yang TIDAK dicakup kesiapan HIPAA**

- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max
- **Console dan Workbench:** Penggunaan melalui antarmuka Claude Console
- **Platform pihak ketiga:** Claude di AWS Bedrock atau Google Cloud Vertex AI (lihat dokumentasi kepatuhan platform tersebut)
- **Integrasi pihak ketiga:** Data yang diproses oleh alat eksternal atau layanan yang terhubung ke aplikasi Anda
- **Claude Code:** Claude Code tidak tercakup dalam kesiapan HIPAA
- **Fitur beta:** Fitur dalam beta umumnya tidak tercakup dalam BAA kecuali secara eksplisit tercantum sebagai memenuhi syarat dalam [tabel kelayakan fitur](#feature-eligibility)

### Panduan penanganan PHI

Informasi kesehatan yang dilindungi (PHI) mencakup informasi kesehatan yang dapat diidentifikasi secara individual. Dalam konteks Claude API, PHI biasanya muncul dalam:

- Konten pesan (prompt dan respons dari Claude)
- File terlampir (gambar, PDF)
- Nama file dan metadata yang terkait dengan konten pesan

Bidang berikut tidak diharapkan mengandung PHI di bawah BAA: nama ruang kerja, informasi pengguna (nama, email, nomor telepon), data penagihan, dan tiket dukungan.

#### Pembatasan definisi skema dan alat

Saat menggunakan [output terstruktur](/docs/id/build-with-claude/structured-outputs) atau alat dengan `strict: true`, API mengompilasi skema JSON menjadi tata bahasa yang di-cache secara terpisah dari konten pesan. Skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons.

**Jangan sertakan PHI dalam definisi skema JSON.** Pembatasan ini berlaku untuk:

- Nama properti skema
- nilai `enum`
- nilai `const`
- ekspresi reguler `pattern`

Informasi khusus pasien hanya boleh muncul dalam konten pesan, di mana dilindungi di bawah perlindungan HIPAA.

### Penanganan kesalahan HIPAA

BAA yang ditandatangani Anda adalah sumber kebenaran resmi untuk fitur mana yang tercakup. API juga memberlakukan pembatasan ini secara otomatis: ketika organisasi yang diaktifkan HIPAA mengirim permintaan yang mencakup fitur yang tidak memenuhi syarat, API mengembalikan kesalahan `400` untuk mencegah penggunaan fitur yang tidak tercakup oleh BAA Anda secara tidak sengaja:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

Pesan kesalahan mencantumkan fitur yang tidak memenuhi syarat yang terdeteksi dalam permintaan. Hapus fitur-fitur ini dari permintaan Anda dan coba lagi.

## Kelayakan fitur

Tabel berikut mencantumkan fitur Claude API mana yang memenuhi syarat untuk pengaturan ZDR dan kesiapan HIPAA. Untuk organisasi yang diaktifkan HIPAA, fitur yang ditandai "Tidak" di kolom HIPAA secara otomatis diblokir, dan permintaan yang mencakupnya mengembalikan kesalahan `400`.

| Fitur | Endpoint | ZDR eligible | HIPAA eligible | Detail |
| ------- | -------- | ------------ | -------------- | ------- |
| [Messages API](/docs/id/build-with-claude/working-with-messages) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Panggilan API standar untuk menghasilkan respons Claude. |
| [Token counting](/docs/id/build-with-claude/token-counting) | `/v1/messages/count_tokens` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Hitung token sebelum mengirim permintaan. |
| [Web search](/docs/id/agents-and-tools/tool-use/web-search-tool) | `/v1/messages` (dengan alat `web_search`) | <Eligible>Ya</Eligible><sup>1</sup> | <Eligible>Ya</Eligible><sup>1</sup> | Hasil pencarian web real-time dikembalikan dalam respons API. |
| [Web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | `/v1/messages` (dengan alat `web_fetch`) | <Eligible>Ya</Eligible><sup>1</sup> <sup>2</sup> | <Eligible status="no">Tidak</Eligible> | Konten web yang diambil dikembalikan dalam respons API. |
| [Advisor tool](/docs/id/agents-and-tools/tool-use/advisor-tool) | `/v1/messages` (dengan alat `advisor`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Output model Advisor dikembalikan dalam respons API; tidak ada yang disimpan di server setelah respons. |
| [Memory tool](/docs/id/agents-and-tools/tool-use/memory-tool) | `/v1/messages` (dengan alat `memory`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Penyimpanan memori sisi klien di mana Anda mengontrol retensi data. |
| [Context management (compaction)](/docs/id/build-with-claude/compaction) | `/v1/messages` (dengan `context_management`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Hasil pemadatan sisi server dikembalikan/diputar ulang tanpa status melalui respons API. |
| [Context editing](/docs/id/build-with-claude/context-editing) | `/v1/messages` (dengan `context_management`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Pengeditan konteks (pembersihan penggunaan alat + pembersihan pemikiran) diterapkan secara real-time. |
| [Fast mode](/docs/id/build-with-claude/fast-mode) | `/v1/messages` (dengan `speed: "fast"`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan. |
| [1M token context window](/docs/id/build-with-claude/context-windows) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Pemrosesan konteks yang diperluas menggunakan Messages API standar. |
| [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Kedalaman pemikiran dinamis menggunakan Messages API standar. |
| [Citations](/docs/id/build-with-claude/citations) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Atribusi sumber menggunakan Messages API standar. |
| [Data residency](/docs/id/build-with-claude/data-residency) | `/v1/messages` (dengan `inference_geo`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Perutean geografis menggunakan Messages API standar. |
| [Effort](/docs/id/build-with-claude/effort) | `/v1/messages` (dengan `effort`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Kontrol efisiensi token menggunakan Messages API standar. |
| [Extended thinking](/docs/id/build-with-claude/extended-thinking) | `/v1/messages` (dengan `thinking`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Penalaran langkah demi langkah menggunakan Messages API standar. |
| [PDF support](/docs/id/build-with-claude/pdf-support) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Pemrosesan dokumen PDF menggunakan Messages API standar. Kelayakan HIPAA berlaku untuk PDF yang dikirim inline melalui Messages API, bukan melalui Files API. |
| [Search results](/docs/id/build-with-claude/search-results) | `/v1/messages` (dengan sumber `search_results`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Dukungan sitasi RAG menggunakan Messages API standar. |
| [Bash tool](/docs/id/agents-and-tools/tool-use/bash-tool) | `/v1/messages` (dengan alat `bash`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Alat sisi klien dijalankan di lingkungan Anda. |
| [Text editor tool](/docs/id/agents-and-tools/tool-use/text-editor-tool) | `/v1/messages` (dengan alat `text_editor`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Alat sisi klien dijalankan di lingkungan Anda. |
| [Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) | `/v1/messages` (dengan alat `computer`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Alat sisi klien di mana tangkapan layar dan file ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Lihat [Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention). |
| [Fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Parameter alat streaming menggunakan Messages API standar. |
| [Prompt caching](/docs/id/build-with-claude/prompt-caching) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Prompt Anda dan output Claude tidak disimpan. Representasi cache KV dan hash kriptografi disimpan dalam memori untuk TTL cache dan dihapus dengan cepat setelah kedaluwarsa. Lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching#data-retention). |
| [Structured outputs](/docs/id/build-with-claude/structured-outputs) | `/v1/messages` | <Eligible status="qualified">Ya (qualified)</Eligible> | <Eligible>Ya</Eligible><sup>3</sup> | Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang di-cache, hingga 24 jam sejak penggunaan terakhir. Ini juga mencakup [strict tool use](/docs/id/agents-and-tools/tool-use/strict-tool-use) (`strict: true` pada alat), yang menggunakan pipeline tata bahasa yang sama. Lihat [Structured outputs](/docs/id/build-with-claude/structured-outputs#data-retention). |
| [Tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool) | `/v1/messages` (dengan alat `tool_search`) | <Eligible status="qualified">Ya (qualified)</Eligible> | <Eligible status="no">Tidak</Eligible> | Hanya data katalog alat (nama, deskripsi, metadata argumen) yang disimpan di server. Lihat [Tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool#data-retention). |
| [Batch processing](/docs/id/build-with-claude/batch-processing) | `/v1/messages/batches` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Retensi 29 hari; penyimpanan async diperlukan. Lihat [Batch processing](/docs/id/build-with-claude/batch-processing#data-retention). |
| [Code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool) | `/v1/messages` (dengan alat `code_execution`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data kontainer dipertahankan hingga 30 hari. Lihat [Code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention). |
| [Programmatic tool calling](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | `/v1/messages` (dengan alat `code_execution`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Dibangun di atas kontainer eksekusi kode; data dipertahankan hingga 30 hari. Lihat [Programmatic tool calling](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention). |
| [Files API](/docs/id/build-with-claude/files) | `/v1/files` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | File dipertahankan hingga secara eksplisit dihapus. Lihat [Files API](/docs/id/build-with-claude/files#data-retention). |
| [Agent skills](/docs/id/agents-and-tools/agent-skills/overview) | `/v1/messages` (dengan `skills`) / `/v1/skills` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data keterampilan dipertahankan per kebijakan standar. Lihat [Agent skills](/docs/id/agents-and-tools/agent-skills/overview#data-retention). |
| [MCP connector](/docs/id/agents-and-tools/mcp-connector) | `/v1/messages` (dengan `mcp_servers`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data dipertahankan per kebijakan standar. Lihat [MCP connector](/docs/id/agents-and-tools/mcp-connector#data-retention). |

<sup>1</sup> [Dynamic filtering](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) tidak memenuhi syarat untuk ZDR atau HIPAA.

<sup>2</sup> Meskipun web fetch memenuhi syarat ZDR, penerbit situs web dapat mempertahankan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai dengan kebijakan mereka sendiri.

<sup>3</sup> PHI tidak boleh disertakan dalam definisi skema JSON. Lihat [panduan penanganan PHI](#phi-handling-guidelines).

## Batasan dan pengecualian

### CORS tidak didukung untuk ZDR

**Cross-Origin Resource Sharing (CORS)** tidak didukung untuk organisasi dengan pengaturan ZDR. Jika Anda perlu membuat panggilan API dari aplikasi berbasis browser, Anda harus:

- Gunakan server proxy backend untuk membuat panggilan API atas nama front end Anda
- Implementasikan penanganan CORS Anda sendiri di server proxy
- Jangan pernah mengekspos kunci API langsung di JavaScript browser

### Retensi data untuk pelanggaran kebijakan dan jika diperlukan oleh hukum

Bahkan dengan pengaturan ZDR atau HIPAA yang ada, Anthropic dapat mempertahankan data jika diperlukan oleh hukum atau untuk memerangi pelanggaran Kebijakan Penggunaan dan penggunaan jahat platform Anthropic. Akibatnya, jika obrolan atau sesi ditandai untuk pelanggaran seperti itu, Anthropic dapat mempertahankan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<section title="Bagaimana cara saya tahu jika organisasi saya memiliki pengaturan ZDR?">

Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR.

</section>

<section title="Bisakah saya menggunakan fitur ZDR-eligible (qualified) di bawah pengaturan ZDR saya?">

Ya. Fitur-fitur ini mempertahankan set data teknis minimal yang terdokumentasi, bukan prompt atau output Claude Anda. Lihat [Pendekatan Anthropic terhadap retensi data](#anthropics-approach-to-data-retention) untuk komitmen yang mengatur fitur-fitur ini.

</section>

<Accordion title={'Apa yang terjadi jika saya menggunakan fitur yang ditandai "Tidak" di bawah ZDR?'}>
Fitur yang ditandai "Tidak" untuk ZDR secara fundamental stateful: Batch API menyimpan pekerjaan Anda, Files API menyimpan file Anda, dan eksekusi kode berjalan di kontainer persisten. Data untuk fitur-fitur ini dipertahankan sesuai dengan kebijakan terdokumentasi fitur. Menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data spesifik itu.
</Accordion>

<section title="Bisakah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">

Hubungi perwakilan akun Anthropic Anda untuk membahas opsi penghapusan untuk fitur non-ZDR.

</section>

<section title="Bagaimana kesiapan HIPAA berbeda dari ZDR?">

ZDR mencegah data pelanggan disimpan saat istirahat setelah respons API dikembalikan. Kesiapan HIPAA melibatkan serangkaian perlindungan privasi dan keamanan yang lebih luas yang melindungi PHI sepanjang siklus hidupnya, termasuk enkripsi, kontrol akses, dan pencatatan audit. Akses API siap HIPAA memberikan fondasi untuk secara progresif mengaktifkan lebih banyak fitur karena data dapat dipertahankan dengan perlindungan yang tepat daripada memerlukan penghapusan segera.

</section>

<section title="Apakah saya masih memerlukan ZDR jika saya memiliki kesiapan HIPAA?">

Tidak. Akses API siap HIPAA dirancang sebagai alternatif untuk ZDR bagi organisasi yang menangani PHI. Dengan kesiapan HIPAA diaktifkan, Anda mendapatkan akses ke fitur API yang didukung sambil mempertahankan perlindungan privasi dan keamanan yang HIPAA perlukan.

</section>

<section title="Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat di bawah HIPAA?">

API mengembalikan kesalahan `400` dengan tipe `invalid_request_error`. Pesan kesalahan mengidentifikasi fitur mana yang tidak tersedia. Hapus fitur yang tidak memenuhi syarat dari permintaan Anda dan coba lagi.

</section>

<section title="Bisakah saya menggunakan organisasi yang sama untuk beban kerja HIPAA dan non-HIPAA?">

Tidak. Kesiapan HIPAA diberlakukan di tingkat organisasi dan secara otomatis memblokir semua fitur yang tidak memenuhi syarat. Gunakan organisasi terpisah untuk beban kerja yang tidak memerlukan kesiapan HIPAA.

</section>

<section title="Bagaimana cara saya meminta akses API siap HIPAA?">

Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk membahas akses API siap HIPAA dan menandatangani Perjanjian Mitra Bisnis.

</section>

<section title="Apakah ini berlaku untuk Claude di AWS Bedrock atau Vertex AI?">

Tidak, hanya Claude API yang memenuhi syarat untuk ZDR dan kesiapan HIPAA. Untuk penerapan Claude di AWS Bedrock atau Vertex AI, lihat kebijakan retensi data dan kepatuhan platform tersebut.

</section>

<section title="Apakah Claude Code memenuhi syarat untuk ZDR?">

Claude Code memenuhi syarat untuk ZDR melalui dua jalur:

- **Kunci API:** Claude Code digunakan dengan kunci API bayar sesuai penggunaan dari organisasi Komersial
- **Claude Enterprise:** Claude Code digunakan melalui Claude Enterprise dengan ZDR diaktifkan untuk organisasi

ZDR diaktifkan berdasarkan per-organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda. ZDR tidak secara otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

Selain itu, jika Anda memiliki pencatatan metrik diaktifkan di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat dipertahankan.

Untuk detail lengkap tentang ZDR untuk Claude Code di Claude Enterprise, termasuk fitur yang dinonaktifkan dan cara meminta pengaktifan, lihat [dokumentasi Claude Code ZDR](https://code.claude.com/docs/en/zero-data-retention).

</section>

<section title="Apakah Claude for Excel mendukung ZDR?">

Tidak, Claude for Excel saat ini tidak memenuhi syarat ZDR.

</section>

<section title="Bagaimana cara saya meminta ZDR?">

Untuk meminta pengaturan ZDR, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).

</section>

## Sumber daya terkait

- [Kebijakan Privasi](https://www.anthropic.com/legal/privacy)
- [Structured outputs](/docs/id/build-with-claude/structured-outputs)
- [Prompt caching](/docs/id/build-with-claude/prompt-caching)
- [Batch processing](/docs/id/build-with-claude/batch-processing)
- [Files API](/docs/id/api/files-create)
- [Trust Center](https://trust.anthropic.com/resources)