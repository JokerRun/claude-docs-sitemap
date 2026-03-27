---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/overview
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: 9d9da8f7805c0018e6c1382470ae702e74e3ad9eebdd3763dbb1c7aa57314d19
---

# Ikhtisar fitur

Jelajahi fitur dan kemampuan canggih Claude.

---

Permukaan API Claude diorganisasikan ke dalam lima area:

- **Kemampuan model:** Kendalikan cara Claude bernalar dan memformat respons.
- **Alat:** Biarkan Claude mengambil tindakan di web atau di lingkungan Anda.
- **Infrastruktur alat:** Menangani penemuan dan orkestrasi dalam skala besar.
- **Manajemen konteks:** Menjaga sesi yang berjalan lama tetap efisien.
- **File dan aset:** Kelola dokumen dan data yang Anda berikan kepada Claude.

Jika Anda baru, mulailah dengan [kemampuan model](#model-capabilities) dan [alat](#tools). Kembali ke bagian lain saat Anda siap untuk mengoptimalkan biaya, latensi, atau skala.

## Kemampuan model

Cara untuk mengarahkan Claude dan output langsung Claude, termasuk format respons, kedalaman penalaran, dan modalitas input.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Jendela konteks](/docs/id/build-with-claude/context-windows) | Hingga 1 juta token untuk memproses dokumen besar, basis kode yang luas, dan percakapan panjang. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) | Biarkan Claude secara dinamis memutuskan kapan dan seberapa banyak untuk berpikir. Mode pemikiran yang direkomendasikan untuk Opus 4.6. Gunakan parameter effort untuk mengontrol kedalaman pemikiran. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) | Proses volume permintaan yang besar secara asinkron untuk penghematan biaya. Kirim batch dengan jumlah kueri yang besar per batch. Panggilan Batch API biayanya 50% lebih murah dari panggilan API standar. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi /> |
| [Kutipan](/docs/id/build-with-claude/citations) | Dasarkan respons Claude pada dokumen sumber. Dengan Citations, Claude dapat memberikan referensi terperinci ke kalimat dan bagian yang tepat yang digunakannya untuk menghasilkan respons, menghasilkan output yang lebih dapat diverifikasi dan tepercaya. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Residensi data](/docs/id/build-with-claude/data-residency) | Kendalikan di mana inferensi model berjalan menggunakan kontrol geografis. Tentukan perutean `"global"` atau `"us"` per permintaan melalui parameter `inference_geo`. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi /> |
| [Effort](/docs/id/build-with-claude/effort) | Kendalikan berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara kelengkapan respons dan efisiensi token. Didukung pada Opus 4.6 dan Opus 4.5. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemikiran diperluas](/docs/id/build-with-claude/extended-thinking) | Kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, memberikan transparansi ke dalam proses berpikir langkah demi langkah Claude sebelum memberikan jawaban akhirnya. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Dukungan PDF](/docs/id/build-with-claude/pdf-support) | Proses dan analisis konten teks dan visual dari dokumen PDF. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Hasil pencarian](/docs/id/build-with-claude/search-results) | Aktifkan kutipan alami untuk aplikasi RAG dengan menyediakan hasil pencarian dengan atribusi sumber yang tepat. Capai kutipan berkualitas pencarian web untuk basis pengetahuan dan alat kustom. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Output terstruktur](/docs/id/build-with-claude/structured-outputs) | Jamin kesesuaian skema dengan dua pendekatan: output JSON untuk respons data terstruktur, dan penggunaan alat ketat untuk input alat yang divalidasi. | [Sebagian](/docs/id/build-with-claude/structured-outputs#data-retention)* | <PlatformAvailability claudeApi bedrock azureAiBeta /> |

## Alat

Alat bawaan yang dipanggil Claude melalui `tool_use`. Alat sisi server dijalankan oleh platform; alat sisi klien diimplementasikan dan dieksekusi oleh Anda.

### Alat sisi server

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) | Jalankan kode di lingkungan sandbox untuk analisis data lanjutan, perhitungan, dan pemrosesan file. Gratis saat digunakan dengan pencarian web atau pengambilan web. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | Ambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan untuk analisis mendalam. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) | Perkuat pengetahuan komprehensif Claude dengan data terkini dan nyata dari seluruh web. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi vertexAi azureAiBeta /> |

### Alat sisi klien

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Bash](/docs/id/agents-and-tools/tool-use/bash-tool) | Jalankan perintah dan skrip bash untuk berinteraksi dengan shell sistem dan melakukan operasi baris perintah. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | Kendalikan antarmuka komputer dengan mengambil tangkapan layar dan mengeluarkan perintah mouse dan keyboard. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Memori](/docs/id/agents-and-tools/tool-use/memory-tool) | Aktifkan Claude untuk menyimpan dan mengambil informasi di seluruh percakapan. Bangun basis pengetahuan dari waktu ke waktu, pertahankan konteks proyek, dan belajar dari interaksi sebelumnya. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) | Buat dan edit file teks dengan antarmuka editor teks bawaan untuk tugas manipulasi file. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## Infrastruktur alat

Infrastruktur yang mendukung penemuan, orkestrasi, dan penskalaan penggunaan alat.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) | Perluas kemampuan Claude dengan Skills. Gunakan Skills bawaan (PowerPoint, Excel, Word, PDF) atau buat Skills kustom dengan instruksi dan skrip. Skills menggunakan pengungkapan progresif untuk mengelola konteks secara efisien. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |
| [Streaming alat berbutir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | Stream parameter penggunaan alat tanpa buffering/validasi JSON, mengurangi latensi untuk menerima parameter besar. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector) | Hubungkan ke server [MCP](/docs/id/mcp) jarak jauh langsung dari Messages API tanpa klien MCP terpisah. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |
| [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | Aktifkan Claude untuk memanggil alat Anda secara terprogram dari dalam container eksekusi kode, mengurangi latensi dan konsumsi token untuk alur kerja multi-alat. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool) | Skalakan ke ribuan alat dengan menemukan dan memuat alat secara dinamis sesuai permintaan menggunakan pencarian berbasis regex, mengoptimalkan penggunaan konteks dan meningkatkan akurasi pemilihan alat. | [Sebagian](/docs/id/agents-and-tools/tool-use/tool-search-tool#data-retention) | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## Manajemen konteks

Infrastruktur untuk mengontrol dan mengoptimalkan jendela konteks Claude.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Kompaksi](/docs/id/build-with-claude/compaction) | Ringkasan konteks sisi server untuk percakapan yang berjalan lama. Ketika konteks mendekati batas jendela, API secara otomatis meringkas bagian percakapan sebelumnya. Didukung pada Opus 4.6 dan Sonnet 4.6. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing) | Kelola konteks percakapan secara otomatis dengan strategi yang dapat dikonfigurasi. Mendukung penghapusan hasil alat saat mendekati batas token dan pengelolaan blok pemikiran dalam percakapan pemikiran diperluas. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Caching prompt otomatis](/docs/id/build-with-claude/prompt-caching#automatic-caching) | Sederhanakan caching prompt ke satu parameter API. Sistem secara otomatis menyimpan cache blok yang dapat di-cache terakhir dalam permintaan Anda, memindahkan titik cache ke depan seiring percakapan berkembang. | [Sebagian](/docs/id/build-with-claude/prompt-caching#data-retention)* | <PlatformAvailability claudeApi azureAiBeta /> |
| [Caching prompt (5 menit)](/docs/id/build-with-claude/prompt-caching) | Berikan Claude lebih banyak pengetahuan latar belakang dan contoh output untuk mengurangi biaya dan latensi. | [Sebagian](/docs/id/build-with-claude/prompt-caching#data-retention)* | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Caching prompt (1 jam)](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) | Durasi cache 1 jam yang diperpanjang untuk konteks yang kurang sering diakses tetapi penting, melengkapi cache standar 5 menit. | [Sebagian](/docs/id/build-with-claude/prompt-caching#data-retention)* | <PlatformAvailability claudeApi vertexAi azureAiBeta /> |
| [Penghitungan token](/docs/id/api/messages-count-tokens) | Penghitungan token memungkinkan Anda menentukan jumlah token dalam pesan sebelum mengirimkannya ke Claude, membantu Anda membuat keputusan yang tepat tentang prompt dan penggunaan Anda. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## File dan aset

Kelola file dan aset untuk digunakan dengan Claude.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Files API](/docs/id/build-with-claude/files) | Unggah dan kelola file untuk digunakan dengan Claude tanpa mengunggah ulang konten dengan setiap permintaan. Mendukung PDF, gambar, dan file teks. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |

\* **Caching prompt:** Menyimpan representasi cache KV dan hash kriptografis (bukan teks mentah) selama 5 atau 60 menit. **Output terstruktur:** Skema JSON di-cache hingga 24 jam sejak penggunaan terakhir; prompt dan respons adalah ZDR. Lihat [detail ZDR](/docs/id/build-with-claude/api-and-data-retention#zdr-eligibility-by-product-feature).