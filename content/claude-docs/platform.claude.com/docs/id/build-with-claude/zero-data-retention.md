---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/zero-data-retention
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 79daa5c679d6a72e1b8bbd0f7716367f80bc449d2201ed600f45d7f9592e3592
---

# Zero Data Retention (ZDR)

Pelajari tentang kebijakan Zero Data Retention (ZDR) Anthropic, termasuk endpoint API dan fitur mana yang memenuhi syarat ZDR.

---

Halaman ini menyediakan daftar endpoint API dan fitur mana yang memenuhi syarat ZDR dan mana yang tidak.

<Note>
Informasi tentang kebijakan retensi data standar Anthropic diatur dalam [kebijakan retensi data komersial Anthropic](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) dan [kebijakan retensi data konsumen](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data). 

Zero Data Retention (ZDR) adalah komitmen Anthropic untuk memastikan bahwa data pelanggan yang dikirimkan melalui endpoint API tertentu tidak disimpan setelah respons API dikembalikan kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan, seperti yang diuraikan dalam pengaturan pelanggan dengan Anthropic. Tunduk pada pengecualian ini, saat menggunakan endpoint yang diaktifkan ZDR, data Anda diproses secara real-time dan segera dibuang, tanpa pencatatan atau penyimpanan prompt atau output.
</Note>

## Batasan penting

**Apa yang dicakup ZDR**

- **API Claude tertentu**: ZDR berlaku untuk API Messages dan Token Counting Claude
- **Claude Code**: ZDR berlaku saat digunakan dengan kredensial API enterprise Anda

**Apa yang TIDAK dicakup ZDR**

- **Produk dan fitur beta**: Produk dan fitur dalam beta kecuali ditentukan lain
- **Console dan Workbench**: Penggunaan apa pun di Console atau Workbench
- **Produk konsumen Claude**: Paket Claude Free, Pro, atau Max, termasuk ketika pelanggan di paket tersebut menggunakan aplikasi web, desktop, atau mobile Claude atau Claude Code
- **Claude for Work dan Claude for Enterprise**: Antarmuka produk Claude for Work dan Claude for Enterprise tidak dicakup oleh ZDR; hanya kunci API organisasi Komersial yang memenuhi syarat
- **Integrasi pihak ketiga**: Data yang diproses oleh situs web pihak ketiga, alat, atau integrasi lainnya tidak dicakup oleh ZDR, meskipun beberapa mungkin menawarkan penawaran serupa. Saat menggunakan layanan eksternal bersama dengan Claude API, pastikan untuk meninjau praktik penanganan data layanan tersebut.

<Note>
Untuk informasi terbaru tentang produk dan fitur mana yang memenuhi syarat ZDR, silakan lihat syarat kontrak Anda atau hubungi perwakilan akun Anthropic Anda.
</Note>

## Kelayakan ZDR menurut produk/fitur

### Sepenuhnya memenuhi syarat ZDR

Endpoint API ini memproses data secara real-time:

| Fitur | Endpoint | Deskripsi |
| ------- | -------- | ----------- |
| Messages API | `/v1/messages` | Panggilan API standar untuk menghasilkan respons Claude. |
| Token Counting | `/v1/messages/count_tokens` | Hitung token sebelum mengirim permintaan. |

### Tidak memenuhi syarat ZDR

Berikut adalah daftar non-exhaustif endpoint dan fitur yang menyimpan data melampaui saat respons API dihasilkan dan **tidak dicakup oleh pengaturan ZDR**:

| Fitur | Endpoint | Kebijakan Retensi Data | Mengapa Tidak Memenuhi Syarat ZDR |
| ------- | -------- | -------------------- | -------------------------- |
| Batch API | `/v1/messages/batches` | Kebijakan standar: retensi 29 hari. Gunakan endpoint DELETE `/v1/messages/batches` untuk menghapus batch pesan kapan saja setelah pemrosesan. | Pemrosesan batch memerlukan penyimpanan respons asinkron. |
| Files API | `/v1/files` | File disimpan sampai dihapus secara eksplisit. | Fitur beta dikecualikan dari ZDR. File yang diunggah melalui Files API disimpan untuk permintaan API di masa depan. |
| Skills (Code Executor) | `/v1/skills` | Data disimpan untuk eksekusi skill. | Fitur beta dikecualikan dari ZDR. Skills menggunakan eksekusi kode di sisi server, yang menyimpan data eksekusi dan file yang diunggah melampaui respons API langsung. |
| Context Management | `/v1/messages` (dengan `context_management`) | File disimpan di server Anthropic. | Fitur beta dikecualikan dari ZDR. |

### Kasus khusus

Fitur-fitur ini memiliki karakteristik retensi data yang bernuansa:

#### Prompt caching

**Status**: Prompt caching adalah fitur beta yang menyimpan representasi cache KV dan hash kriptografi konten yang di-cache. Entri yang di-cache memiliki masa hidup minimal 5 atau 60 menit dan terisolasi antar organisasi. Karena Anthropic tidak menyimpan teks mentah prompt atau respons, fitur ini mungkin cocok untuk pelanggan yang memerlukan komitmen retensi data tipe ZDR.

Lihat [dokumentasi Prompt Caching](/docs/id/build-with-claude/prompt-caching#what-is-the-cache-lifetime) untuk detail.

#### Structured Outputs

**Status**: Saat menggunakan Structured Outputs dengan skema JSON, prompt dan respons diproses dengan ZDR. Namun, skema JSON itu sendiri disimpan dalam cache sementara selama hingga 24 jam untuk tujuan optimasi. Tidak ada data prompt atau respons yang disimpan.

## Batasan dan pengecualian tambahan

### CORS tidak didukung

**Cross-Origin Resource Sharing (CORS)** tidak didukung untuk organisasi dengan pengaturan ZDR. Jika Anda perlu membuat panggilan API dari aplikasi berbasis browser, Anda harus:

- Menggunakan server proxy backend untuk membuat panggilan API atas nama frontend Anda
- Menerapkan penanganan CORS Anda sendiri di server proxy
- Jangan pernah mengekspos kunci API secara langsung di JavaScript browser

### Retensi data untuk pelanggaran kebijakan dan jika diperlukan oleh hukum

Bahkan dengan pengaturan ZDR yang berlaku, Anthropic dapat menyimpan data jika diperlukan oleh hukum atau untuk memerangi pelanggaran Usage Policy dan penggunaan platform Anthropic yang berbahaya. Akibatnya, jika chat atau sesi ditandai untuk pelanggaran seperti itu, Anthropic dapat menyimpan input dan output hingga 2 tahun.

## Pertanyaan yang sering diajukan

**Bagaimana saya tahu jika organisasi saya memiliki pengaturan ZDR?**

Periksa syarat kontrak Anda atau hubungi perwakilan akun Anthropic Anda untuk mengonfirmasi apakah organisasi Anda memiliki pengaturan ZDR.

**Apa yang terjadi jika saya menggunakan fitur yang tidak memenuhi syarat ZDR ketika organisasi saya memiliki pengaturan ZDR?**

Data akan disimpan sesuai dengan kebijakan retensi standar fitur. Pastikan Anda memahami karakteristik retensi setiap fitur sebelum digunakan.

**Bisakah saya meminta penghapusan data dari fitur yang tidak memenuhi syarat ZDR?**

Hubungi perwakilan akun Anthropic Anda untuk membahas opsi penghapusan untuk fitur non-ZDR.

**Apakah ZDR berlaku untuk semua model Claude?**

ZDR berlaku untuk endpoint yang memenuhi syarat ZDR terlepas dari model Claude mana yang Anda gunakan.

**Apakah ini berlaku untuk Claude di AWS Bedrock atau Google Vertex AI?**

Tidak, hanya Claude API yang memenuhi syarat untuk ZDR. Untuk deployment Claude di AWS Bedrock atau Google Vertex AI, lihat kebijakan retensi data platform tersebut.

**Apakah Claude Code memenuhi syarat untuk ZDR?**

Kelayakan ZDR Claude Code tergantung pada cara Anda melakukan autentikasi:

- **Memenuhi syarat**: Claude Code yang digunakan dengan kunci API bayar sesuai penggunaan dari organisasi Komersial
- **Tidak memenuhi syarat**: Claude Code yang digunakan melalui OAuth (kursi premium melalui Claude for Enterprise)

Selain itu, jika Anda memiliki pencatatan metrik yang diaktifkan di Claude Code, data produktivitas (seperti statistik penggunaan) dikecualikan dari ZDR dan dapat disimpan.

**Apakah Claude for Excel mendukung ZDR?**

Tidak, Claude for Excel saat ini tidak memenuhi syarat ZDR.

**Bagaimana cara saya meminta ZDR?**

Untuk meminta pengaturan ZDR, hubungi [tim penjualan Anthropic](https://claude.com/contact-sales).

## Sumber daya terkait

- [Privacy Policy](https://www.anthropic.com/legal/privacy)
- [Batch Processing](/docs/id/build-with-claude/batch-processing)
- [Files API](/docs/id/api/files-create)
- [Agent SDK Sessions](/docs/id/agent-sdk/sessions)
- [Prompt Caching](/docs/id/build-with-claude/prompt-caching)