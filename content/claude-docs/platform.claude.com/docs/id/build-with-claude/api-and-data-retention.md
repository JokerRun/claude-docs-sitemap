---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/api-and-data-retention
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: b24315503ee7dde9b7fef507083effc354bc32b550ae214c5257d2e0224a97e0
---

# API dan retensi data

Pelajari tentang bagaimana API Anthropic dan fitur-fitur terkait menyimpan data, termasuk informasi tentang zero data retention (ZDR) dan akses API siap-HIPAA.

---

<Note>
Informasi tentang kebijakan retensi standar Anthropic tercantum dalam [kebijakan retensi data komersial Anthropic](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

Anthropic menawarkan dua pengaturan penanganan data untuk Claude API:
- **Zero data retention (ZDR):** Data pelanggan tidak disimpan saat tidak aktif setelah respons API dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan.
- **Kesiapan HIPAA:** Untuk organisasi yang menangani informasi kesehatan yang dilindungi (PHI), Anthropic menawarkan akses API siap-HIPAA dengan Business Associate Agreement (BAA) yang ditandatangani. Lihat [kesiapan HIPAA](#hipaa-readiness).
</Note>

## Pendekatan Anthropic terhadap retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan dan retensi yang berbeda. Jika suatu API atau fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, maka mungkin memenuhi syarat untuk ZDR. Jika suatu API atau fitur secara inheren memerlukan penyimpanan prompt atau respons pelanggan, Anthropic merancang untuk jejak retensi sekecil mungkin. Untuk fitur-fitur ini:

- Data yang dipertahankan tidak pernah digunakan untuk pelatihan model tanpa izin eksplisit Anda.
- Hanya yang secara teknis diperlukan agar API dan fitur berfungsi yang dipertahankan. Konten percakapan (prompt Anda dan output Claude) tidak pernah dipertahankan kecuali disebutkan secara eksplisit.
- Data dihapus pada TTL terpendek yang praktis, dan Anthropic bertujuan memberi pelanggan kontrol atas berapa lama data dipertahankan. Apa yang disimpan, dan durasi retensi di mana TTL tertentu berlaku, didokumentasikan di halaman setiap fitur.

Dalam [tabel kelayakan fitur](#feature-eligibility), beberapa fitur ditandai "Ya (berkualifikasi)" di kolom yang memenuhi syarat ZDR. Jika organisasi Anda memiliki pengaturan ZDR, Anda dapat menggunakan fitur-fitur ini dengan keyakinan bahwa apa yang dipertahankan Anthropic bersifat terbatas dan diperlukan untuk kinerja optimal.

## Cakupan zero data retention (ZDR)

**Apa yang dicakup ZDR**

- **API Claude tertentu:** ZDR berlaku untuk API Messages dan Token Counting Claude
- **Claude Code:** ZDR berlaku saat digunakan dengan kunci API organisasi Komersial atau melalui Claude Enterprise (lihat [dokumen ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention))

**Apa yang TIDAK dicakup ZDR**

- **Console dan Workbench:** Penggunaan apa pun di Console atau Workbench
- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max, termasuk saat pelanggan pada paket tersebut menggunakan aplikasi web, desktop, atau mobile Claude atau Claude Code
- **Claude Teams dan Claude Enterprise:** Antarmuka produk Claude Teams dan Claude Enterprise **tidak memenuhi syarat ZDR**, kecuali untuk Claude Code saat digunakan melalui Claude Enterprise dengan ZDR diaktifkan untuk organisasi. Untuk antarmuka produk lainnya, hanya kunci API organisasi Komersial yang memenuhi syarat untuk ZDR.
- **Integrasi pihak ketiga:** Data yang diproses oleh situs web, alat, atau integrasi pihak ketiga lainnya **tidak memenuhi syarat ZDR**, meskipun beberapa mungkin memiliki penawaran serupa. Saat menggunakan layanan eksternal bersamaan dengan Claude API, pastikan untuk meninjau praktik penanganan data layanan tersebut.

<Note>
Untuk informasi terbaru tentang produk dan fitur mana yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kesiapan HIPAA

Claude API mendukung integrasi siap-HIPAA untuk organisasi yang menangani informasi kesehatan yang dilindungi (PHI). Dengan BAA yang ditandatangani dan organisasi yang diaktifkan HIPAA, Anda dapat menggunakan fitur API yang didukung untuk memproses PHI sambil mendukung kepatuhan HIPAA organisasi Anda.

Sebelumnya, organisasi yang memerlukan kesiapan HIPAA untuk Claude API perlu mengaktifkan ZDR. Akses API siap-HIPAA menghapus persyaratan ini dan memberikan fondasi bagi Anthropic untuk secara progresif mengaktifkan fitur tambahan saat diaudit untuk kesiapan HIPAA.

<Note>
Halaman ini mencakup kesiapan HIPAA untuk Claude API. Untuk Panduan Implementasi HIPAA lengkap yang mencakup Claude Enterprise, Claude Code, dan persyaratan konfigurasi, lihat [Anthropic Trust Center](https://trust.anthropic.com/resources).
</Note>

### Memulai

Untuk menyiapkan akses API siap-HIPAA:

<Steps>
<Step title="Tandatangani Business Associate Agreement">
Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk menandatangani BAA yang mencakup penggunaan API.
</Step>
<Step title="Provisikan organisasi yang diaktifkan HIPAA">
Anthropic menyediakan organisasi khusus dengan kontrol kesiapan HIPAA yang diaktifkan. Organisasi ini secara otomatis memberlakukan pembatasan fitur, memblokir permintaan API yang menggunakan fitur yang tidak memenuhi syarat.
</Step>
<Step title="Bangun dengan fitur yang memenuhi syarat">
Gunakan [tabel kelayakan fitur](#feature-eligibility) untuk mengonfirmasi fitur mana yang didukung. Tinjau [panduan penanganan PHI](#phi-handling-guidelines) untuk fitur yang memerlukan pembatasan khusus tentang di mana PHI dapat muncul. Untuk persyaratan konfigurasi dan kepatuhan terperinci, lihat [Panduan Implementasi HIPAA](https://trust.anthropic.com/resources).
</Step>
</Steps>

<Warning>
Kesiapan HIPAA diberlakukan di tingkat organisasi. Jika Anda memerlukan akses API siap-HIPAA dan tujuan umum, gunakan organisasi terpisah untuk masing-masing.
</Warning>

### Cakupan kesiapan HIPAA

**Apa yang dicakup kesiapan HIPAA**

- **Claude API:** Kesiapan HIPAA berlaku untuk Claude API (`api.anthropic.com`) untuk fitur yang memenuhi syarat yang tercantum dalam [tabel kelayakan fitur](#feature-eligibility).

**Apa yang TIDAK dicakup kesiapan HIPAA**

- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max
- **Console dan Workbench:** Penggunaan melalui antarmuka Claude Console
- **Platform pihak ketiga:** Claude di AWS Bedrock atau Google Cloud Vertex AI (lihat dokumentasi kepatuhan platform tersebut)
- **Integrasi pihak ketiga:** Data yang diproses oleh alat atau layanan eksternal yang terhubung ke aplikasi Anda
- **Claude Code:** Claude Code tidak dicakup dalam kesiapan HIPAA
- **Fitur beta:** Fitur dalam beta umumnya tidak dicakup dalam BAA kecuali secara eksplisit tercantum sebagai memenuhi syarat dalam [tabel kelayakan fitur](#feature-eligibility)

### Panduan penanganan PHI

Informasi kesehatan yang dilindungi (PHI) mencakup informasi kesehatan yang dapat diidentifikasi secara individual. Dalam konteks Claude API, PHI biasanya muncul dalam:

- Konten pesan (prompt dan respons dari Claude)
- File terlampir (gambar, PDF)
- Nama file dan metadata yang terkait dengan konten pesan

Bidang-bidang berikut tidak diharapkan mengandung PHI berdasarkan BAA: nama ruang kerja, informasi pengguna (nama, email, nomor telepon), data penagihan, dan tiket dukungan.

#### Pembatasan skema dan definisi alat

Saat menggunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau alat dengan `strict: true`, API mengompilasi skema JSON ke dalam tata bahasa yang di-cache secara terpisah dari konten pesan. Skema yang di-cache ini tidak mendapatkan perlindungan PHI yang sama seperti prompt dan respons.

**Jangan sertakan PHI dalam definisi skema JSON.** Pembatasan ini berlaku untuk:

- Nama properti skema
- Nilai `enum`
- Nilai `const`
- Ekspresi reguler `pattern`

Informasi spesifik pasien hanya boleh muncul dalam konten pesan, di mana informasi tersebut dilindungi di bawah perlindungan HIPAA.

### Penanganan kesalahan HIPAA

BAA yang Anda tandatangani adalah sumber kebenaran resmi untuk fitur mana yang dicakup. API juga memberlakukan pembatasan ini secara otomatis: ketika organisasi yang diaktifkan HIPAA mengirimkan permintaan yang menyertakan fitur yang tidak memenuhi syarat, API mengembalikan kesalahan `400` untuk mencegah penggunaan fitur yang tidak dicakup oleh BAA Anda secara tidak sengaja:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

Pesan kesalahan mencantumkan fitur yang tidak memenuhi syarat yang terdeteksi dalam permintaan. Hapus fitur yang tidak memenuhi syarat dari permintaan Anda dan coba lagi.

## Kelayakan fitur

Tabel berikut mencantumkan fitur Claude API mana yang memenuhi syarat untuk pengaturan ZDR dan kesiapan HIPAA. Untuk organisasi yang diaktifkan HIPAA, fitur yang ditandai "Tidak" di kolom HIPAA diblokir secara otomatis, dan permintaan yang menyertakannya mengembalikan kesalahan `400`.

| Fitur | Endpoint | Memenuhi syarat ZDR | Memenuhi syarat HIPAA | Detail |
| ----- | -------- | ------------------- | --------------------- | ------ |
| [Messages API](/docs/id/build-with-claude/working-with-messages) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Panggilan API standar untuk menghasilkan respons Claude. |
| [Penghitungan token](/docs/id/build-with-claude/token-counting) | `/v1/messages/count_tokens` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Hitung token sebelum mengirim permintaan. |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) | `/v1/messages` (dengan alat `web_search`) | <Eligible>Ya</Eligible><sup>1</sup> | <Eligible>Ya</Eligible><sup>1</sup> | Hasil pencarian web real-time dikembalikan dalam respons API. |
| [Pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | `/v1/messages` (dengan alat `web_fetch`) | <Eligible>Ya</Eligible><sup>1</sup> <sup>2</sup> | <Eligible status="no">Tidak</Eligible> | Konten web yang diambil dikembalikan dalam respons API. |
| [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) | `/v1/messages` (dengan alat `memory`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Penyimpanan memori sisi klien di mana Anda mengontrol retensi data. |
| [Manajemen konteks (pemadatan)](/docs/id/build-with-claude/compaction) | `/v1/messages` (dengan `context_management`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Hasil pemadatan sisi server dikembalikan/diputar-balikkan secara stateless melalui respons API. |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing) | `/v1/messages` (dengan `context_management`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Pengeditan konteks (pembersihan penggunaan alat + pembersihan pemikiran) diterapkan secara real time. |
| [Mode cepat](/docs/id/build-with-claude/fast-mode) | `/v1/messages` (dengan `speed: "fast"`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan. |
| [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Pemrosesan konteks yang diperluas menggunakan Messages API standar. |
| [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Kedalaman pemikiran dinamis menggunakan Messages API standar. |
| [Kutipan](/docs/id/build-with-claude/citations) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Atribusi sumber menggunakan Messages API standar. |
| [Residensi data](/docs/id/build-with-claude/data-residency) | `/v1/messages` (dengan `inference_geo`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Perutean geografis menggunakan Messages API standar. |
| [Upaya](/docs/id/build-with-claude/effort) | `/v1/messages` (dengan `effort`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Kontrol efisiensi token menggunakan Messages API standar. |
| [Pemikiran diperluas](/docs/id/build-with-claude/extended-thinking) | `/v1/messages` (dengan `thinking`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Penalaran langkah demi langkah menggunakan Messages API standar. |
| [Dukungan PDF](/docs/id/build-with-claude/pdf-support) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Pemrosesan dokumen PDF menggunakan Messages API standar. Kelayakan HIPAA berlaku untuk PDF yang dikirim secara inline melalui Messages API, bukan melalui Files API. |
| [Hasil pencarian](/docs/id/build-with-claude/search-results) | `/v1/messages` (dengan sumber `search_results`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Dukungan kutipan RAG menggunakan Messages API standar. |
| [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool) | `/v1/messages` (dengan alat `bash`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Alat sisi klien yang dieksekusi di lingkungan Anda. |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) | `/v1/messages` (dengan alat `text_editor`) | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Alat sisi klien yang dieksekusi di lingkungan Anda. |
| [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | `/v1/messages` (dengan alat `computer`) | <Eligible>Ya</Eligible> | <Eligible status="no">Tidak</Eligible> | Alat sisi klien di mana tangkapan layar dan file diambil dan disimpan di lingkungan Anda, bukan oleh Anthropic. Lihat [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention). |
| [Streaming alat berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Parameter alat streaming menggunakan Messages API standar. |
| [Caching prompt](/docs/id/build-with-claude/prompt-caching) | `/v1/messages` | <Eligible>Ya</Eligible> | <Eligible>Ya</Eligible> | Prompt Anda dan output Claude tidak disimpan. Representasi cache KV dan hash kriptografi disimpan dalam memori untuk TTL cache dan segera dihapus setelah kedaluwarsa. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#data-retention). |
| [Structured outputs](/docs/id/build-with-claude/structured-outputs) | `/v1/messages` | <Eligible status="qualified">Ya (berkualifikasi)</Eligible> | <Eligible>Ya</Eligible><sup>3</sup> | Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang di-cache, hingga 24 jam sejak terakhir digunakan. Ini juga mencakup [penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use) (`strict: true` pada alat), yang menggunakan pipeline tata bahasa yang sama. Lihat [Structured outputs](/docs/id/build-with-claude/structured-outputs#data-retention). |
| [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool) | `/v1/messages` (dengan alat `tool_search`) | <Eligible status="qualified">Ya (berkualifikasi)</Eligible> | <Eligible status="no">Tidak</Eligible> | Hanya data katalog alat (nama, deskripsi, metadata argumen) yang disimpan di sisi server. Lihat [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool#data-retention). |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) | `/v1/messages/batches` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Retensi 29 hari; penyimpanan async diperlukan. Lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing#data-retention). |
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) | `/v1/messages` (dengan alat `code_execution`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data kontainer dipertahankan hingga 30 hari. Lihat [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention). |
| [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | `/v1/messages` (dengan alat `code_execution`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Dibangun di atas kontainer eksekusi kode; data dipertahankan hingga 30 hari. Lihat [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention). |
| [Files API](/docs/id/build-with-claude/files) | `/v1/files` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | File dipertahankan hingga dihapus secara eksplisit. Lihat [Files API](/docs/id/build-with-claude/files#data-retention). |
| [Keterampilan agen](/docs/id/agents-and-tools/agent-skills/overview) | `/v1/messages` (dengan `skills`) / `/v1/skills` | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data keterampilan dipertahankan sesuai kebijakan standar. Lihat [Keterampilan agen](/docs/id/agents-and-tools/agent-skills/overview#data-retention). |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector) | `/v1/messages` (dengan `mcp_servers`) | <Eligible status="no">Tidak</Eligible> | <Eligible status="no">Tidak</Eligible> | Data dipertahankan sesuai kebijakan standar. Lihat [Konektor MCP](/docs/id/agents-and-tools/mcp-connector#data-retention). |

<sup>1</sup> [Pemfilteran dinamis](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) tidak memenuhi syarat untuk ZDR atau HIPAA.

<sup>2</sup> Meskipun pengambilan web memenuhi syarat ZDR, penerbit situs web dapat menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri.

<sup>3</sup> PHI tidak boleh disertakan dalam definisi skema JSON. Lihat [panduan penanganan PHI](#phi-handling-guidelines).

## Batasan dan pengecualian

### CORS tidak didukung untuk ZDR

**Cross-Origin Resource Sharing (CORS)** tidak didukung untuk organisasi dengan pengaturan ZDR. Jika Anda perlu melakukan panggilan API dari aplikasi berbasis browser, Anda harus:

- Menggunakan server proxy backend untuk melakukan panggilan API atas nama front end Anda
- Mengimplementasikan penanganan CORS Anda sendiri di server proxy
- Tidak pernah mengekspos kunci API secara langsung dalam JavaScript browser

### Retensi data untuk pelanggaran kebijakan dan jika diwajibkan oleh hukum

Bahkan dengan pengaturan ZDR atau HIPAA yang berlaku, Anthropic dapat menyimpan data jika diwajibkan oleh hukum atau untuk memerangi pelanggaran Kebijakan Penggunaan dan penggunaan berbahaya platform Anthropic. Akibatnya, jika obrolan atau sesi ditandai untuk pelanggaran tersebut, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<section title="Bagaimana cara mengetahui apakah organisasi saya memiliki pengaturan ZDR?">

Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR yang berlaku.

</section>

<section title="Dapatkah saya menggunakan fitur yang memenuhi syarat ZDR (berkualifikasi) berdasarkan pengaturan ZDR saya?">

Ya. Fitur-fitur ini menyimpan sekumpulan data teknis yang minimal dan terdokumentasi, bukan prompt Anda atau output Claude. Lihat [Pendekatan Anthropic terhadap retensi data](#anthropics-approach-to-data-retention) untuk komitmen yang mengatur fitur-fitur ini.

</section>

<Accordion title={'Apa yang terjadi jika saya menggunakan fitur yang ditandai "Tidak" berdasarkan ZDR?'}>
Fitur yang ditandai "Tidak" untuk ZDR pada dasarnya bersifat stateful: Batch API menyimpan pekerjaan Anda, Files API menyimpan file Anda, dan eksekusi kode berjalan dalam kontainer persisten. Data untuk fitur-fitur ini dipertahankan sesuai kebijakan yang didokumentasikan fitur tersebut. Menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data tertentu tersebut.
</Accordion>

<section title="Dapatkah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">

Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan opsi penghapusan untuk fitur non-ZDR.

</section>

<section title="Bagaimana kesiapan HIPAA berbeda dari ZDR?">

ZDR mencegah data pelanggan disimpan saat tidak aktif setelah respons API dikembalikan. Kesiapan HIPAA melibatkan serangkaian perlindungan privasi dan keamanan yang lebih luas yang melindungi PHI sepanjang siklus hidupnya, termasuk enkripsi, kontrol akses, dan pencatatan audit. Akses API siap-HIPAA memberikan fondasi untuk secara progresif mengaktifkan lebih banyak fitur karena data dapat dipertahankan dengan perlindungan yang tepat daripada memerlukan penghapusan segera.

</section>

<section title="Apakah saya masih memerlukan ZDR jika saya memiliki kesiapan HIPAA?">

Tidak. Akses API siap-HIPAA dirancang sebagai alternatif ZDR untuk organisasi yang menangani PHI. Dengan kesiapan HIPAA yang diaktifkan, Anda mendapatkan akses ke fitur API yang didukung sambil mempertahankan perlindungan privasi dan keamanan yang diperlukan HIPAA.

</section>

<section title="Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat berdasarkan HIPAA?">

API mengembalikan kesalahan `400` dengan tipe `invalid_request_error`. Pesan kesalahan mengidentifikasi fitur mana yang tidak tersedia. Hapus fitur yang tidak memenuhi syarat dari permintaan Anda dan coba lagi.

</section>

<section title="Dapatkah saya menggunakan organisasi yang sama untuk beban kerja HIPAA dan non-HIPAA?">

Tidak. Kesiapan HIPAA diberlakukan di tingkat organisasi dan secara otomatis memblokir semua fitur yang tidak memenuhi syarat. Gunakan organisasi terpisah untuk beban kerja yang tidak memerlukan kesiapan HIPAA.

</section>

<section title="Bagaimana cara meminta akses API siap-HIPAA?">

Hubungi [tim penjualan Anthropic](https://claude.com/contact-sales) untuk mendiskusikan akses API siap-HIPAA dan menandatangani Business Associate Agreement.

</section>

<section title="Apakah ini berlaku untuk Claude di AWS Bedrock atau Vertex AI?">

Tidak, hanya Claude API yang memenuhi syarat untuk ZDR dan kesiapan HIPAA. Untuk penerapan Claude di AWS Bedrock atau Vertex AI, lihat kebijakan retensi data dan kepatuhan platform tersebut.

</section>

<section title="Apakah Claude Code memenuhi syarat untuk ZDR?">

Claude Code memenuhi syarat untuk ZDR melalui dua jalur:

- **Kunci API:** Claude Code yang digunakan dengan kunci API bayar sesuai penggunaan dari organisasi Komersial
- **Claude Enterprise:** Claude Code yang digunakan melalui Claude Enterprise dengan ZDR diaktifkan untuk organisasi

ZDR diaktifkan berdasarkan per-organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda. ZDR tidak secara otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

Selain itu, jika Anda mengaktifkan pencatatan metrik di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat dipertahankan.

Untuk detail lengkap tentang ZDR untuk Claude Code di Claude Enterprise, termasuk fitur yang dinonaktifkan dan cara meminta pengaktifan, lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention).

</section>

<section title="Apakah Claude for Excel mendukung ZDR?">

Tidak, Claude for Excel saat ini tidak memenuhi syarat ZDR.

</section>

<section title="Bagaimana cara meminta ZDR?">

Untuk meminta pengaturan ZDR, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).

</section>

## Sumber daya terkait

- [Kebijakan Privasi](https://www.anthropic.com/legal/privacy)
- [Structured outputs](/docs/id/build-with-claude/structured-outputs)
- [Caching prompt](/docs/id/build-with-claude/prompt-caching)
- [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)
- [Files API](/docs/id/api/files-create)
- [Trust Center](https://trust.anthropic.com/resources)