---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/overview
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 0171980ecd2c06cab370a4df3da61f67abbfee0f93a4c0ac54fe34687841cdf1
---

# Ikhtisar fitur

Jelajahi fitur dan kemampuan Claude yang canggih.

---

Permukaan API Claude diorganisir menjadi lima area:

- **Kemampuan model:** Kontrol cara Claude bernalar dan memformat respons.
- **Tools:** Biarkan Claude mengambil tindakan di web atau di lingkungan Anda.
- **Infrastruktur tool:** Menangani penemuan dan orkestrasi dalam skala besar.
- **Manajemen konteks:** Menjaga sesi yang berjalan lama tetap efisien.
- **File dan aset:** Kelola dokumen dan data yang Anda berikan kepada Claude.

Jika Anda baru, mulai dengan [kemampuan model](#model-capabilities) dan [tools](#tools). Kembali ke bagian lain ketika Anda siap untuk mengoptimalkan biaya, latensi, atau skala.

## Ketersediaan fitur

Fitur di Claude Platform diberi salah satu klasifikasi ketersediaan berikut per platform (ditampilkan di kolom Ketersediaan dari setiap tabel di bawah). Tidak semua fitur melewati setiap tahap. Fitur dapat memasuki pada klasifikasi apa pun dan dapat melewati tahap.

| Klasifikasi | Deskripsi |
|----------------|-------------|
| **Beta**<sup>*</sup> | Fitur pratinjau yang digunakan untuk mengumpulkan umpan balik dan melakukan iterasi pada kasus penggunaan yang kurang matang. Ketersediaan mungkin terbatas, termasuk melalui persyaratan pendaftaran atau daftar tunggu, dan mungkin tidak diumumkan secara publik. <br/><br/> Fitur dapat berubah secara signifikan atau dihentikan berdasarkan umpan balik. Tidak dijamin untuk penggunaan produksi yang berkelanjutan. Perubahan yang merusak dimungkinkan dengan pemberitahuan, dan beberapa batasan khusus platform mungkin berlaku. Fitur Beta memiliki [header beta](/docs/id/api/beta-headers). |
| **Tersedia secara umum (GA)** | Fitur stabil, sepenuhnya didukung, dan direkomendasikan untuk penggunaan produksi. Seharusnya tidak memiliki header beta atau indikator lain bahwa fitur berada dalam status pratinjau. Dicakup oleh jaminan [versioning](/docs/id/api/versioning) API standar. |
| **Tidak direkomendasikan** | Fitur masih berfungsi tetapi tidak lagi direkomendasikan. Jalur migrasi dan jadwal penghapusan disediakan. |
| **Pensiun** | Fitur tidak lagi tersedia. |

_<sup>*</sup> Dapat membawa qualifier yang menunjukkan ketersediaan yang lebih sempit atau batasan tambahan (misalnya, "beta: research preview"). Lihat halaman fitur untuk detail._

## Kemampuan model

Cara untuk mengarahkan Claude dan output langsung Claude, termasuk format respons, kedalaman penalaran, dan modalitas input.

<Tip>
Anda dapat menemukan kemampuan model mana yang didukung secara terprogram. [Models API](/docs/id/api/models/list) mengembalikan `max_input_tokens`, `max_tokens`, dan objek `capabilities` untuk setiap model yang tersedia.
</Tip>

| Fitur | Deskripsi | Retensi Data Nol (ZDR) | Ketersediaan |
|---------|-----------|----|--------------|
| [Jendela konteks](/docs/id/build-with-claude/context-windows) | Hingga 1M token untuk memproses dokumen besar, basis kode yang luas, dan percakapan panjang. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) | Biarkan Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir. Mode pemikiran yang direkomendasikan untuk Opus 4.7. Gunakan parameter effort untuk mengontrol kedalaman pemikiran. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing) | Proses volume besar permintaan secara asinkron untuk penghematan biaya. Kirim batch dengan jumlah besar kueri per batch. Panggilan API Batch berharga 50% lebih murah daripada panggilan API standar. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi /> |
| [Kutipan](/docs/id/build-with-claude/citations) | Dasarkan respons Claude pada dokumen sumber. Dengan Kutipan, Claude dapat memberikan referensi terperinci ke kalimat dan bagian yang tepat yang digunakannya untuk menghasilkan respons, menghasilkan output yang lebih dapat diverifikasi dan dapat dipercaya. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Residensi data](/docs/id/build-with-claude/data-residency) | Kontrol di mana inferensi model berjalan menggunakan kontrol geografis. Tentukan `"global"` atau `"us"` routing per permintaan melalui parameter `inference_geo`. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi /> |
| [Effort](/docs/id/build-with-claude/effort) | Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menukar antara kelengkapan respons dan efisiensi token. Didukung pada Opus 4.7, Opus 4.6, dan Opus 4.5. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) | Kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, memberikan transparansi ke dalam proses pemikiran langkah demi langkah Claude sebelum memberikan jawaban akhirnya. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Dukungan PDF](/docs/id/build-with-claude/pdf-support) | Proses dan analisis konten teks dan visual dari dokumen PDF. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Hasil pencarian](/docs/id/build-with-claude/search-results) | Aktifkan kutipan alami untuk aplikasi RAG dengan menyediakan hasil pencarian dengan atribusi sumber yang tepat. Capai kutipan berkualitas pencarian web untuk basis pengetahuan dan alat khusus. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Output terstruktur](/docs/id/build-with-claude/structured-outputs) | Jamin kepatuhan skema dengan dua pendekatan: output JSON untuk respons data terstruktur, dan penggunaan tool ketat untuk input tool yang divalidasi. | [Memenuhi syarat ZDR (qualified)](/docs/id/build-with-claude/structured-outputs#data-retention)* | <PlatformAvailability claudeApi bedrock azureAiBeta /> |

## Tools

Tool bawaan yang Claude panggil melalui `tool_use`. Tool sisi server dijalankan oleh platform; tool sisi klien diimplementasikan dan dieksekusi oleh Anda.

### Tool sisi server

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Tool Advisor](/docs/id/agents-and-tools/tool-use/advisor-tool) | Pasangkan model executor yang lebih cepat dengan model advisor dengan kecerdasan lebih tinggi yang memberikan panduan strategis di tengah-tengah generasi untuk beban kerja agentic jangka panjang. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta /> |
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) | Jalankan kode di lingkungan sandbox untuk analisis data tingkat lanjut, perhitungan, dan pemrosesan file. Gratis saat digunakan dengan pencarian web atau pengambilan web. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | Ambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan untuk analisis mendalam. | Memenuhi syarat ZDR* | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) | Perkaya pengetahuan komprehensif Claude dengan data terkini dan dunia nyata dari seluruh web. | Memenuhi syarat ZDR* | <PlatformAvailability claudeApi vertexAi azureAiBeta /> |

### Tool sisi klien

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Bash](/docs/id/agents-and-tools/tool-use/bash-tool) | Jalankan perintah bash dan skrip untuk berinteraksi dengan shell sistem dan melakukan operasi baris perintah. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | Kontrol antarmuka komputer dengan mengambil tangkapan layar dan mengeluarkan perintah mouse dan keyboard. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Memori](/docs/id/agents-and-tools/tool-use/memory-tool) | Aktifkan Claude untuk menyimpan dan mengambil informasi di seluruh percakapan. Bangun basis pengetahuan seiring waktu, pertahankan konteks proyek, dan pelajari dari interaksi masa lalu. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) | Buat dan edit file teks dengan antarmuka editor teks bawaan untuk tugas manipulasi file. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## Infrastruktur tool

Infrastruktur yang mendukung penemuan, orkestrasi, dan penskalaan penggunaan tool.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) | Perluas kemampuan Claude dengan Skills. Gunakan Skills yang telah dibangun sebelumnya (PowerPoint, Excel, Word, PDF) atau buat Skills khusus dengan instruksi dan skrip. Skills menggunakan pengungkapan progresif untuk mengelola konteks secara efisien. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |
| [Streaming tool butir halus](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) | Stream parameter penggunaan tool tanpa buffering/validasi JSON, mengurangi latensi untuk menerima parameter besar. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Konektor MCP](/docs/id/agents-and-tools/mcp-connector) | Terhubung ke server [MCP](/docs/id/mcp) jarak jauh langsung dari Messages API tanpa klien MCP terpisah. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |
| [Pemanggilan tool terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) | Aktifkan Claude untuk memanggil tool Anda secara terprogram dari dalam kontainer eksekusi kode, mengurangi latensi dan konsumsi token untuk alur kerja multi-tool. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Pencarian tool](/docs/id/agents-and-tools/tool-use/tool-search-tool) | Skala ke ribuan tool dengan secara dinamis menemukan dan memuat tool sesuai permintaan menggunakan pencarian berbasis regex, mengoptimalkan penggunaan konteks dan meningkatkan akurasi pemilihan tool. | [Memenuhi syarat ZDR (qualified)](/docs/id/agents-and-tools/tool-use/tool-search-tool#data-retention)* | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## Manajemen konteks

Infrastruktur untuk mengontrol dan mengoptimalkan jendela konteks Claude.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Pemadatan](/docs/id/build-with-claude/compaction) | Ringkasan konteks sisi server untuk percakapan yang berjalan lama. Ketika konteks mendekati batas jendela, API secara otomatis merangkum bagian-bagian awal percakapan. Didukung pada Opus 4.7, Opus 4.6, dan Sonnet 4.6. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing) | Kelola konteks percakapan secara otomatis dengan strategi yang dapat dikonfigurasi. Mendukung penghapusan hasil tool saat mendekati batas token dan mengelola blok pemikiran dalam percakapan pemikiran diperpanjang. | Memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta azureAiBeta /> |
| [Penyimpanan prompt otomatis](/docs/id/build-with-claude/prompt-caching#automatic-caching) | Sederhanakan penyimpanan prompt menjadi parameter API tunggal. Sistem secara otomatis menyimpan blok yang dapat disimpan terakhir dalam permintaan Anda, memindahkan titik cache ke depan saat percakapan berkembang. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi azureAiBeta /> |
| [Penyimpanan prompt (5m)](/docs/id/build-with-claude/prompt-caching) | Berikan Claude dengan lebih banyak pengetahuan latar belakang dan contoh output untuk mengurangi biaya dan latensi. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |
| [Penyimpanan prompt (1jam)](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) | Durasi cache 1 jam yang diperpanjang untuk konteks yang kurang sering diakses tetapi penting, melengkapi cache standar 5 menit. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi vertexAi azureAiBeta /> |
| [Penghitungan token](/docs/id/api/messages-count-tokens) | Penghitungan token memungkinkan Anda menentukan jumlah token dalam pesan sebelum mengirimnya ke Claude, membantu Anda membuat keputusan berdasarkan informasi tentang prompt dan penggunaan Anda. | Memenuhi syarat ZDR | <PlatformAvailability claudeApi bedrock vertexAi azureAiBeta /> |

## File dan aset

Kelola file dan aset untuk digunakan dengan Claude.

| Fitur | Deskripsi | ZDR | Ketersediaan |
|---------|-----------|----|--------------|
| [Files API](/docs/id/build-with-claude/files) | Unggah dan kelola file untuk digunakan dengan Claude tanpa mengunggah ulang konten dengan setiap permintaan. Mendukung PDF, gambar, dan file teks. | Tidak memenuhi syarat ZDR | <PlatformAvailability claudeApiBeta azureAiBeta /> |

\* **Output terstruktur:** Prompt Anda dan output Claude tidak disimpan. Hanya skema JSON yang disimpan, hingga 24 jam sejak penggunaan terakhir. **Pencarian tool:** Hanya data katalog tool (nama, deskripsi, metadata argumen) yang disimpan di sisi server; implementasi khusus sisi klien sepenuhnya memenuhi syarat ZDR. **Pencarian web dan pengambilan web:** Memenuhi syarat ZDR kecuali ketika [penyaringan dinamis](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) diaktifkan. Lihat [detail ZDR](/docs/id/build-with-claude/api-and-data-retention#feature-eligibility).