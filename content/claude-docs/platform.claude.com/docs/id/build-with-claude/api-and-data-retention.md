---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/api-and-data-retention
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: cb0200d6b6f0440385142a6c9c48e683e57a2d1b3b457796925f13dfcc85e984
---

# API dan retensi data

Pelajari tentang cara API Anthropic dan fitur-fitur terkait menyimpan data, termasuk informasi tentang API dan fitur mana yang memenuhi syarat untuk zero data retention ("ZDR").

---

<Note>
Informasi tentang kebijakan retensi standar Anthropic tercantum dalam [kebijakan retensi data komersial Anthropic](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

Ketika pengguna menggunakan endpoint API dengan zero data retention (ZDR), data pelanggan yang dikirimkan melalui endpoint tersebut tidak disimpan saat tidak aktif setelah respons API dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan. Tunduk pada pengecualian ini, saat menggunakan endpoint yang mendukung ZDR, data pelanggan diproses secara real time dan segera dibuang, tanpa pencatatan atau penyimpanan non-ephemeral dari prompt atau output.
</Note>

## Pendekatan kami terhadap retensi data

API dan fitur yang berbeda memiliki kebutuhan penyimpanan dan retensi yang berbeda. Jika suatu API atau fitur tidak memerlukan penyimpanan prompt atau respons pelanggan, API atau fitur tersebut mungkin memenuhi syarat untuk ZDR. Jika suatu API atau fitur memang memerlukan penyimpanan prompt atau respons pelanggan, Anthropic merancang untuk jejak retensi sekecil mungkin. Untuk fitur-fitur ini:

- Data yang disimpan tidak pernah digunakan untuk pelatihan model tanpa izin eksplisit Anda.
- Hanya yang secara teknis diperlukan agar API dan fitur berfungsi yang disimpan. Konten percakapan (prompt Anda dan output Claude) tidak pernah disimpan kecuali disebutkan secara eksplisit.
- Data dihapus pada TTL praktis terpendek, dan Anthropic bertujuan untuk memberi pelanggan kendali atas berapa lama data disimpan. Apa yang disimpan, dan durasi retensi di mana TTL tertentu berlaku, didokumentasikan di halaman setiap fitur.

Dalam [tabel kelayakan ZDR](#zdr-eligibility-by-feature), beberapa fitur ditandai "Ya (berkualifikasi)" di kolom yang memenuhi syarat ZDR. Jika organisasi Anda memiliki pengaturan ZDR, Anda dapat menggunakan fitur-fitur ini dengan keyakinan bahwa apa yang disimpan Anthropic bersifat terbatas dan diperlukan untuk kinerja optimal.

## Cakupan zero data retention (ZDR)

**Apa yang dicakup ZDR**

- **API Claude tertentu:** ZDR berlaku untuk API Messages dan Token Counting Claude
- **Claude Code:** ZDR berlaku saat digunakan dengan kunci API organisasi Komersial atau melalui Claude Enterprise (lihat [dokumentasi ZDR Claude Code](https://code.claude.com/docs/en/zero-data-retention))

**Apa yang TIDAK dicakup ZDR**

- **Console dan Workbench:** Penggunaan apa pun di Console atau Workbench
- **Produk konsumen Claude:** Paket Claude Free, Pro, atau Max, termasuk saat pelanggan pada paket tersebut menggunakan aplikasi web, desktop, atau mobile Claude atau Claude Code
- **Claude Teams dan Claude Enterprise:** Antarmuka produk Claude Teams dan Claude Enterprise **tidak memenuhi syarat ZDR**, kecuali untuk Claude Code saat digunakan melalui Claude Enterprise dengan ZDR yang diaktifkan untuk organisasi. Untuk antarmuka produk lainnya, hanya kunci API organisasi Komersial yang memenuhi syarat untuk ZDR.
- **Integrasi pihak ketiga:** Data yang diproses oleh situs web, alat, atau integrasi pihak ketiga lainnya **tidak memenuhi syarat ZDR**, meskipun beberapa mungkin memiliki penawaran serupa. Saat menggunakan layanan eksternal bersamaan dengan Claude API, pastikan untuk meninjau praktik penanganan data layanan tersebut.

<Note>
Untuk informasi terbaru tentang produk dan fitur mana yang memenuhi syarat ZDR, lihat ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kelayakan ZDR berdasarkan fitur

| Fitur | Endpoint | Memenuhi syarat ZDR | Detail retensi data |
| ------- | -------- | ---------- | --------------------- |
| [Messages API](/docs/id/build-with-claude/working-with-messages) | `/v1/messages` | Ya | Panggilan API standar untuk menghasilkan respons Claude. |
| [Penghitungan token](/docs/id/build-with-claude/token-counting) | `/v1/messages/count_tokens` | Ya | Hitung token sebelum mengirim permintaan. |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) | `/v1/messages` (dengan alat `web_search`) | Ya<sup>1</sup> | Hasil pencarian web real-time dikembalikan dalam respons API. |
| [Pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | `/v1/messages` (dengan alat `web_fetch`) | Ya<sup>1</sup> <sup>2</sup> | Konten web yang diambil dikembalikan dalam respons API. |
| [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) | `/v1/messages` (dengan alat `memory`) | Ya | Penyimpanan memori sisi klien di mana Anda mengontrol retensi data. |
| [Manajemen konteks (pemadatan)](/docs/id/build-with-claude/compaction) | `/v1/messages` (dengan `context_management`) | Ya | Hasil pemadatan sisi server dikembalikan/diputar-balikkan secara stateless melalui respons API. |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing) | `/v1/messages` (dengan `context_management`) | Ya | Pengeditan konteks (penghapusan penggunaan alat + penghapusan pemikiran) diterapkan secara real time. |
| [Mode cepat](/docs/id/build-with-claude/fast-mode) | `/v1/messages` (dengan `speed: "fast"`) | Ya | Endpoint Messages API yang sama dengan inferensi lebih cepat. ZDR berlaku terlepas dari pengaturan kecepatan. |
| [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) | `/v1/messages` | Ya | Pemrosesan konteks yang diperluas menggunakan Messages API standar. |
| [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) | `/v1/messages` | Ya | Kedalaman pemikiran dinamis menggunakan Messages API standar. |
| [Kutipan](/docs/id/build-with-claude/citations) | `/v1/messages` | Ya | Atribusi sumber menggunakan Messages API standar. |
| [Residensi data](/docs/id/build-with-claude/data-residency) | `/v1/messages` (dengan `inference_geo`) | Ya | Perutean geografis menggunakan Messages API standar. |
| [Upaya](/docs/id/build-with-claude/effort) | `/v1/messages` (dengan `effort`) | Ya | Kontrol efisiensi token menggunakan Messages API standar. |
| [Pemikiran diperluas](/docs/id/build-with-claude/extended-thinking) | `/v1/messages` (dengan `thinking`) | Ya | Penalaran langkah demi langkah menggunakan Messages API standar. |
| [Dukungan PDF](/docs/id/build-with-claude/pdf-support) | `/v1/messages` | Ya | Pemrosesan dokumen PDF menggunakan Messages API standar. |
| [Hasil pencarian](/docs/id/build-with-claude/search-results) | `/v1/messages` (dengan sumber `search_results`) | Ya | Dukungan kutipan RAG menggunakan Messages API standar. |
| [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool) | `/v1/messages` (dengan alat `bash`) | Ya | Alat sisi klien yang dieksekusi di lingkungan Anda. |
| [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) | `/v1/messages` (dengan alat `text_editor`) | Ya | Alat sisi klien yang dieksekusi di lingkungan Anda. |
| [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | `/v1/messages` (dengan alat `computer`) | Ya | Alat sisi klien di mana tangkapan layar dan file diambil dan disimpan di lingkungan Anda, bukan oleh Anthropic. Lihat [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool#data-retention). |
| [Streaming alat berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages` | Ya | Parameter alat streaming menggunakan Messages API standar. |
| [Caching prompt](/docs/id/build-with-claude/prompt-caching) | `/v1/messages` | Ya | Prompt Anda dan output Claude tidak disimpan. Representasi cache KV dan hash kriptografis disimpan dalam memori untuk TTL cache dan segera dihapus setelah kedaluwarsa. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#data-retention). |
| [Output terstruktur](/docs/id/build-with-claude/structured-outputs) | `/v1/messages` | Ya (berkualifikasi) | Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang di-cache, hingga 24 jam sejak terakhir digunakan. Lihat [Output terstruktur](/docs/id/build-with-claude/structured-outputs#data-retention). |
| [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool) | `/v1/messages` (dengan alat `tool_search`) | Ya (berkualifikasi) | Hanya data katalog alat (nama, deskripsi, metadata argumen) yang disimpan di sisi server. Lihat [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool#data-retention). |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) | `/v1/messages/batches` | Tidak | Retensi 29 hari; penyimpanan asinkron diperlukan. Lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing#data-retention). |
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) | `/v1/messages` (dengan alat `code_execution`) | Tidak | Data kontainer disimpan hingga 30 hari. Lihat [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#data-retention). |
| [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | `/v1/messages` (dengan alat `code_execution`) | Tidak | Dibangun di atas kontainer eksekusi kode; data disimpan hingga 30 hari. Lihat [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling#data-retention). |
| [Files API](/docs/id/build-with-claude/files) | `/v1/files` | Tidak | File disimpan hingga dihapus secara eksplisit. Lihat [Files API](/docs/id/build-with-claude/files#data-retention). |
| [Keterampilan agen](/docs/id/agents-and-tools/agent-skills/overview) | `/v1/messages` (dengan `skills`) / `/v1/skills` | Tidak | Data keterampilan disimpan sesuai kebijakan standar. Lihat [Keterampilan agen](/docs/id/agents-and-tools/agent-skills/overview#data-retention). |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector) | `/v1/messages` (dengan `mcp_servers`) | Tidak | Data disimpan sesuai kebijakan standar. Lihat [Konektor MCP](/docs/id/agents-and-tools/mcp-connector#data-retention). |

<sup>1</sup> [Pemfilteran dinamis](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering-with-opus-4-6-and-sonnet-4-6) tidak memenuhi syarat ZDR.

<sup>2</sup> Meskipun pengambilan web memenuhi syarat ZDR, penerbit situs web dapat menyimpan data permintaan (seperti URL yang diambil dan metadata permintaan) sesuai kebijakan mereka sendiri.

## Batasan dan pengecualian

### CORS tidak didukung

**Cross-Origin Resource Sharing (CORS)** tidak didukung untuk organisasi dengan pengaturan ZDR. Jika Anda perlu melakukan panggilan API dari aplikasi berbasis browser, Anda harus:

- Menggunakan server proxy backend untuk melakukan panggilan API atas nama front end Anda
- Mengimplementasikan penanganan CORS Anda sendiri di server proxy
- Tidak pernah mengekspos kunci API secara langsung di JavaScript browser

### Retensi data untuk pelanggaran kebijakan dan di mana diwajibkan oleh hukum

Bahkan dengan pengaturan ZDR yang berlaku, Anthropic dapat menyimpan data jika diwajibkan oleh hukum atau untuk memerangi pelanggaran Kebijakan Penggunaan dan penggunaan berbahaya platform Anthropic. Akibatnya, jika obrolan atau sesi ditandai karena pelanggaran tersebut, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

<section title="Bagaimana cara mengetahui apakah organisasi saya memiliki pengaturan ZDR?">

Periksa ketentuan kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR yang berlaku.

</section>

<section title="Dapatkah saya menggunakan fitur yang memenuhi syarat ZDR (berkualifikasi) di bawah pengaturan ZDR saya?">

Ya. Fitur-fitur ini menyimpan sekumpulan data teknis yang minimal dan terdokumentasi, bukan prompt Anda atau output Claude. Lihat [Pendekatan kami terhadap retensi data](#our-approach-to-data-retention) untuk komitmen yang mengatur fitur-fitur ini.

</section>

<Accordion title={'Apa yang terjadi jika saya menggunakan fitur yang ditandai "Tidak"?'}>
Fitur yang ditandai "Tidak" pada dasarnya bersifat stateful: Batch API menyimpan pekerjaan Anda, Files API menyimpan file Anda, dan eksekusi kode berjalan dalam kontainer persisten. Data untuk fitur-fitur ini disimpan sesuai kebijakan yang didokumentasikan fitur tersebut. Menggunakannya adalah pilihan untuk keluar dari pengaturan ZDR Anda untuk data tertentu tersebut.
</Accordion>

<section title="Dapatkah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?">

Hubungi perwakilan akun Anthropic Anda untuk mendiskusikan opsi penghapusan untuk fitur non-ZDR.

</section>

<section title="Apakah ini berlaku untuk Claude di AWS Bedrock atau Vertex AI?">

Tidak, hanya Claude API yang memenuhi syarat untuk ZDR. Untuk penerapan Claude di AWS Bedrock atau Vertex AI, lihat kebijakan retensi data platform tersebut.

</section>

<section title="Apakah Claude Code memenuhi syarat untuk ZDR?">

Claude Code memenuhi syarat untuk ZDR melalui dua jalur:

- **Kunci API:** Claude Code yang digunakan dengan kunci API bayar sesuai penggunaan dari organisasi Komersial
- **Claude Enterprise:** Claude Code yang digunakan melalui Claude Enterprise dengan ZDR yang diaktifkan untuk organisasi

ZDR diaktifkan berdasarkan per-organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anda. ZDR tidak secara otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama.

Selain itu, jika Anda mengaktifkan pencatatan metrik di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat disimpan.

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
- [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)
- [Files API](/docs/id/api/files-create)
- [Sesi Agent SDK](/docs/id/agent-sdk/sessions)
- [Caching prompt](/docs/id/build-with-claude/prompt-caching)