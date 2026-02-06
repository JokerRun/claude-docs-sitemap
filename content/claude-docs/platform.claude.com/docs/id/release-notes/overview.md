---
source: platform
url: https://platform.claude.com/docs/id/release-notes/overview
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 2adf4b14b25703cec1ae4763c6cb139367294e6cc6aa2d2f09a198485fbee0de
---

# Platform Pengembang Claude

Pembaruan ke Platform Pengembang Claude, termasuk Claude API, SDK klien, dan Konsol Claude.

---

<Tip>
Untuk catatan rilis tentang Claude Apps, lihat [Catatan rilis untuk Claude Apps di Pusat Bantuan Claude](https://support.claude.com/en/articles/12138966-release-notes).

Untuk pembaruan ke Claude Code, lihat [CHANGELOG.md lengkap](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) di repositori `claude-code`.
</Tip>

### 5 Februari 2026
- Kami telah meluncurkan [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), model paling cerdas kami untuk tugas-tugas agentic yang kompleks dan pekerjaan jangka panjang. Opus 4.6 merekomendasikan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`); manual thinking (`type: "enabled"` dengan `budget_tokens`) sudah tidak direkomendasikan. Opus 4.6 tidak mendukung prefilling pesan asisten. Pelajari lebih lanjut di [Apa yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6).
- Parameter [effort](/docs/id/build-with-claude/effort) sekarang tersedia secara umum (tidak memerlukan header beta) dan mendukung Claude Opus 4.6. Effort menggantikan `budget_tokens` untuk mengontrol kedalaman thinking pada model baru.
- Kami telah meluncurkan [API compaction](/docs/id/build-with-claude/compaction) dalam beta, menyediakan ringkasan konteks sisi server untuk percakapan yang efektif tak terbatas. Tersedia di Opus 4.6.
- Kami telah memperkenalkan [kontrol residensi data](/docs/id/build-with-claude/data-residency), memungkinkan Anda menentukan di mana inferensi model berjalan dengan parameter `inference_geo`. Inferensi hanya AS tersedia dengan harga 1,1x untuk model yang dirilis setelah 1 Februari 2026.
- [Jendela konteks token 1M](/docs/id/build-with-claude/context-windows#1m-token-context-window) sekarang tersedia dalam beta untuk Claude Opus 4.6, selain Sonnet 4.5 dan Sonnet 4. [Harga konteks panjang](/docs/id/about-claude/pricing#long-context-pricing) berlaku untuk permintaan yang melebihi 200K token input.
- [Fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) sekarang tersedia secara umum di semua model dan platform (tidak memerlukan header beta). Parameter `output_format` untuk [structured outputs](/docs/id/build-with-claude/structured-outputs) telah dipindahkan ke `output_config.format`.

### 29 Januari 2026
- [Structured outputs](/docs/id/build-with-claude/structured-outputs) sekarang tersedia secara umum di Claude API untuk Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. GA mencakup dukungan skema yang diperluas, latensi kompilasi grammar yang ditingkatkan, dan jalur integrasi yang disederhanakan tanpa memerlukan header beta. Parameter `output_format` telah dipindahkan ke `output_config.format`. Pengguna beta yang ada dapat terus menggunakan header beta selama periode transisi. Structured outputs tetap dalam beta publik di Amazon Bedrock dan Microsoft Foundry.

### 12 Januari 2026
- `console.anthropic.com` sekarang dialihkan ke `platform.claude.com`. Konsol Claude telah pindah ke rumah barunya sebagai bagian dari konsolidasi merek Claude kami. Bookmark dan tautan yang ada akan terus berfungsi melalui pengalihan otomatis. Untuk detail lebih lanjut, lihat [pengumuman 16 September 2025](#september-16-2025).

### 5 Januari 2026
- Kami telah menghentikan model Claude Opus 3 (`claude-3-opus-20240229`). Semua permintaan ke model ini sekarang akan mengembalikan kesalahan. Kami merekomendasikan upgrade ke [Claude Opus 4.5](/docs/id/about-claude/models/overview#latest-models-comparison), yang menawarkan peningkatan intelijen yang signifikan dengan sepertiga biayanya. Peneliti dapat meminta akses berkelanjutan ke Claude Opus 3 di API melalui [Program Akses Peneliti Eksternal](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 19 Desember 2025
- Kami mengumumkan penghentian model Claude Haiku 3.5. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 4 Desember 2025
- [Structured outputs](/docs/id/build-with-claude/structured-outputs) sekarang mendukung Claude Haiku 4.5.

### 24 November 2025
- Kami telah meluncurkan [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5), model paling cerdas kami yang menggabungkan kemampuan maksimal dengan kinerja praktis. Ideal untuk tugas-tugas khusus yang kompleks, rekayasa perangkat lunak profesional, dan agen lanjutan. Fitur peningkatan langkah-demi-langkah dalam visi, coding, dan penggunaan komputer dengan harga yang lebih terjangkau daripada model Opus sebelumnya. Pelajari lebih lanjut di dokumentasi [Models & Pricing](/docs/id/about-claude/models) kami.
- Kami telah meluncurkan [programmatic tool calling](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dalam beta publik, memungkinkan Claude memanggil alat dari dalam eksekusi kode untuk mengurangi latensi dan penggunaan token dalam alur kerja multi-alat.
- Kami telah meluncurkan [tool search tool](/docs/id/agents-and-tools/tool-use/tool-search-tool) dalam beta publik, memungkinkan Claude untuk secara dinamis menemukan dan memuat alat sesuai permintaan dari katalog alat besar.
- Kami telah meluncurkan [parameter effort](/docs/id/build-with-claude/effort) dalam beta publik untuk Claude Opus 4.5, memungkinkan Anda mengontrol penggunaan token dengan menukar antara kelengkapan respons dan efisiensi.
- Kami telah menambahkan [client-side compaction](/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) ke SDK Python dan TypeScript kami, secara otomatis mengelola konteks percakapan melalui ringkasan saat menggunakan `tool_runner`.

### 21 November 2025
- Blok konten hasil pencarian sekarang tersedia secara umum di Amazon Bedrock. Pelajari lebih lanjut di dokumentasi [search results](/docs/id/build-with-claude/search-results) kami.

### 19 November 2025
- Kami telah meluncurkan **platform dokumentasi baru** di [platform.claude.com/docs](https://platform.claude.com/docs). Dokumentasi kami sekarang hidup berdampingan dengan Konsol Claude, menyediakan pengalaman pengembang yang terpadu. Situs docs sebelumnya di docs.claude.com akan dialihkan ke lokasi baru.

### 18 November 2025
- Kami telah meluncurkan **Claude di Microsoft Foundry**, membawa model Claude ke pelanggan Azure dengan penagihan Azure dan autentikasi OAuth. Akses Messages API lengkap termasuk extended thinking, prompt caching (5-menit dan 1-jam), dukungan PDF, Files API, Agent Skills, dan penggunaan alat. Pelajari lebih lanjut di dokumentasi [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) kami.

### 14 November 2025
- Kami telah meluncurkan [structured outputs](/docs/id/build-with-claude/structured-outputs) dalam beta publik, menyediakan kepatuhan skema yang dijamin untuk respons Claude. Gunakan output JSON untuk respons data terstruktur atau penggunaan alat ketat untuk input alat yang divalidasi. Tersedia untuk Claude Sonnet 4.5 dan Claude Opus 4.1. Untuk mengaktifkan, gunakan header beta `structured-outputs-2025-11-13`.

### 28 Oktober 2025
- Kami mengumumkan penghentian model Claude Sonnet 3.7. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).
- Kami telah menghentikan model Claude Sonnet 3.5. Semua permintaan ke model ini sekarang akan mengembalikan kesalahan.
- Kami telah memperluas context editing dengan clearing thinking block (`clear_thinking_20251015`), memungkinkan manajemen otomatis thinking block. Pelajari lebih lanjut di dokumentasi [context editing](/docs/id/build-with-claude/context-editing) kami.

### 16 Oktober 2025
- Kami telah meluncurkan [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (`skills-2025-10-02` beta), cara baru untuk memperluas kemampuan Claude. Skills adalah folder terorganisir dari instruksi, skrip, dan sumber daya yang Claude muat secara dinamis untuk melakukan tugas khusus. Rilis awal mencakup:
  - **Anthropic-managed Skills**: Skills pra-bangun untuk bekerja dengan file PowerPoint (.pptx), Excel (.xlsx), Word (.docx), dan PDF
  - **Custom Skills**: Unggah Skills Anda sendiri melalui Skills API (endpoint `/v1/skills`) untuk mengemas keahlian domain dan alur kerja organisasi
  - Skills memerlukan [code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan
  - Pelajari lebih lanjut di dokumentasi [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) kami dan [referensi API](/docs/id/api/skills/create-skill)

### 15 Oktober 2025
- Kami telah meluncurkan [Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5), model Haiku tercepat dan paling cerdas kami dengan kinerja mendekati frontier. Ideal untuk aplikasi real-time, pemrosesan volume tinggi, dan deployment sensitif biaya yang memerlukan penalaran kuat. Pelajari lebih lanjut di dokumentasi [Models & Pricing](/docs/id/about-claude/models) kami.

### 29 September 2025
- Kami telah meluncurkan [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), model terbaik kami untuk agen kompleks dan coding, dengan intelijen tertinggi di sebagian besar tugas. Pelajari lebih lanjut di [models overview](/docs/id/about-claude/models/overview).
- Kami telah memperkenalkan [global endpoint pricing](/docs/id/about-claude/pricing#third-party-platform-pricing) untuk AWS Bedrock dan Google Vertex AI. Harga Claude API (1P) tidak terpengaruh.
- Kami telah memperkenalkan alasan berhenti baru `model_context_window_exceeded` yang memungkinkan Anda meminta token maksimal yang mungkin tanpa menghitung ukuran input. Pelajari lebih lanjut di dokumentasi [handling stop reasons](/docs/id/build-with-claude/handling-stop-reasons) kami.
- Kami telah meluncurkan memory tool dalam beta, memungkinkan Claude menyimpan dan berkonsultasi informasi di seluruh percakapan. Pelajari lebih lanjut di dokumentasi [memory tool](/docs/id/agents-and-tools/tool-use/memory-tool) kami.
- Kami telah meluncurkan context editing dalam beta, menyediakan strategi untuk secara otomatis mengelola konteks percakapan. Rilis awal mendukung penghapusan hasil dan panggilan alat yang lebih lama saat mendekati batas token. Pelajari lebih lanjut di dokumentasi [context editing](/docs/id/build-with-claude/context-editing) kami.

### 17 September 2025
- Kami telah meluncurkan tool helpers dalam beta untuk SDK Python dan TypeScript, menyederhanakan pembuatan dan eksekusi alat dengan validasi input yang aman tipe dan tool runner untuk penanganan alat otomatis dalam percakapan. Untuk detail, lihat dokumentasi untuk [Python SDK](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md) dan [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers).

### 16 September 2025
- Kami telah menyatukan penawaran pengembang kami di bawah merek Claude. Anda harus melihat penamaan dan URL yang diperbarui di seluruh platform dan dokumentasi kami, tetapi **antarmuka pengembang kami akan tetap sama**. Berikut adalah beberapa perubahan penting:
  - Konsol Claude ([console.anthropic.com](https://console.anthropic.com)) → Konsol Claude ([platform.claude.com](https://platform.claude.com)). Konsol akan tersedia di kedua URL hingga 12 Januari 2026. Setelah tanggal itu, [console.anthropic.com](https://console.anthropic.com) akan secara otomatis dialihkan ke [platform.claude.com](https://platform.claude.com).
  - Docs Anthropic ([docs.claude.com](https://docs.claude.com)) → Claude Docs ([docs.claude.com](https://docs.claude.com))
  - Pusat Bantuan Anthropic ([support.claude.com](https://support.claude.com)) → Pusat Bantuan Claude ([support.claude.com](https://support.claude.com))
  - Endpoint API, header, variabel lingkungan, dan SDK tetap sama. Integrasi yang ada akan terus berfungsi tanpa perubahan apa pun.

### 10 September 2025
- Kami telah meluncurkan web fetch tool dalam beta, memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan. Pelajari lebih lanjut di dokumentasi [web fetch tool](/docs/id/agents-and-tools/tool-use/web-fetch-tool) kami.
- Kami telah meluncurkan [Claude Code Analytics API](/docs/id/build-with-claude/claude-code-analytics-api), memungkinkan organisasi untuk secara terprogram mengakses metrik penggunaan harian yang diagregasi untuk Claude Code, termasuk metrik produktivitas, statistik penggunaan alat, dan data biaya.

### 8 September 2025
- Kami meluncurkan versi beta dari [C# SDK](https://github.com/anthropics/anthropic-sdk-csharp).

### 5 September 2025
- Kami telah meluncurkan [rate limit charts](/docs/id/api/rate-limits#monitoring-your-rate-limits-in-the-console) di halaman [Usage](https://console.anthropic.com/settings/usage) Konsol, memungkinkan Anda memantau penggunaan batas laju API dan tingkat caching dari waktu ke waktu.

### 3 September 2025
- Kami telah meluncurkan dukungan untuk dokumen yang dapat dikutip dalam hasil alat sisi klien. Pelajari lebih lanjut di dokumentasi [tool use](/docs/id/agents-and-tools/tool-use/implement-tool-use) kami.

### 2 September 2025
- Kami telah meluncurkan v2 dari [Code Execution Tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, menggantikan alat Python-only asli dengan eksekusi perintah Bash dan kemampuan manipulasi file langsung, termasuk menulis kode dalam bahasa lain.

### 27 Agustus 2025
- Kami meluncurkan versi beta dari [PHP SDK](https://github.com/anthropics/anthropic-sdk-php).

### 26 Agustus 2025
- Kami telah meningkatkan batas laju pada [jendela konteks token 1M](/docs/id/build-with-claude/context-windows#1m-token-context-window) untuk Claude Sonnet 4 di Claude API. Untuk informasi lebih lanjut, lihat [Long context rate limits](/docs/id/api/rate-limits#long-context-rate-limits).
- Jendela konteks token 1m sekarang tersedia di Vertex AI Google Cloud. Untuk informasi lebih lanjut, lihat [Claude di Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai).

### 19 Agustus 2025
- ID permintaan sekarang disertakan langsung dalam badan respons kesalahan bersama dengan header `request-id` yang ada. Pelajari lebih lanjut di dokumentasi [error](/docs/id/api/errors#error-shapes) kami.

### 18 Agustus 2025
- Kami telah merilis [Usage & Cost API](/docs/id/build-with-claude/usage-cost-api), memungkinkan administrator untuk secara terprogram memantau data penggunaan dan biaya organisasi mereka.
- Kami telah menambahkan endpoint baru ke Admin API untuk mengambil informasi organisasi. Untuk detail, lihat [Organization Info Admin API reference](/docs/id/api/admin-api/organization/get-me).

### 13 Agustus 2025
- Kami mengumumkan penghentian model Claude Sonnet 3.5 (`claude-3-5-sonnet-20240620` dan `claude-3-5-sonnet-20241022`). Model ini akan dihentikan pada 28 Oktober 2025. Kami merekomendasikan migrasi ke Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) untuk kinerja dan kemampuan yang ditingkatkan. Baca lebih lanjut di dokumentasi [Model deprecations](/docs/id/about-claude/model-deprecations).
- Durasi cache 1 jam untuk prompt caching sekarang tersedia secara umum. Anda sekarang dapat menggunakan TTL cache yang diperluas tanpa header beta. Pelajari lebih lanjut di dokumentasi [prompt caching](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) kami.

### 12 Agustus 2025
- Kami telah meluncurkan dukungan beta untuk [jendela konteks token 1M](/docs/id/build-with-claude/context-windows#1m-token-context-window) di Claude Sonnet 4 di Claude API dan Amazon Bedrock.

### 11 Agustus 2025
- Beberapa pelanggan mungkin mengalami 429 (`rate_limit_error`) [errors](/docs/id/api/errors) setelah peningkatan tajam dalam penggunaan API karena batas akselerasi di API. Sebelumnya, kesalahan 529 (`overloaded_error`) akan terjadi dalam skenario serupa.

### 8 Agustus 2025
- Blok konten hasil pencarian sekarang tersedia secara umum di Claude API dan Vertex AI Google Cloud. Fitur ini memungkinkan kutipan alami untuk aplikasi RAG dengan atribusi sumber yang tepat. Header beta `search-results-2025-06-09` tidak lagi diperlukan. Pelajari lebih lanjut di dokumentasi [search results](/docs/id/build-with-claude/search-results) kami.

### 5 Agustus 2025
- Kami telah meluncurkan [Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1), pembaruan inkremental ke Claude Opus 4 dengan kemampuan yang ditingkatkan dan peningkatan kinerja.<sup>*</sup> Pelajari lebih lanjut di dokumentasi [Models & Pricing](/docs/id/about-claude/models) kami.

_<sup>* - Opus 4.1 tidak memungkinkan parameter `temperature` dan `top_p` untuk ditentukan bersama-sama. Silakan gunakan hanya satu. </sup>_

### 28 Juli 2025
- Kami telah merilis `text_editor_20250728`, alat editor teks yang diperbarui yang memperbaiki beberapa masalah dari versi sebelumnya dan menambahkan parameter `max_characters` opsional yang memungkinkan Anda mengontrol panjang pemotongan saat melihat file besar.

### 24 Juli 2025
- Kami telah meningkatkan [rate limits](/docs/id/api/rate-limits) untuk Claude Opus 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan menskalakan dengan Claude. Untuk pelanggan dengan [usage tier 1-4 rate limits](/docs/id/api/rate-limits#rate-limits), perubahan ini berlaku segera ke akun Anda - tidak ada tindakan yang diperlukan.

### 21 Juli 2025
- Kami telah menghentikan model Claude 2.0, Claude 2.1, dan Claude Sonnet 3. Semua permintaan ke model ini sekarang akan mengembalikan kesalahan. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 17 Juli 2025
- Kami telah meningkatkan [rate limits](/docs/id/api/rate-limits) untuk Claude Sonnet 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan menskalakan dengan Claude. Untuk pelanggan dengan [usage tier 1-4 rate limits](/docs/id/api/rate-limits#rate-limits), perubahan ini berlaku segera ke akun Anda - tidak ada tindakan yang diperlukan.

### 3 Juli 2025
- Kami telah meluncurkan blok konten hasil pencarian dalam beta, memungkinkan kutipan alami untuk aplikasi RAG. Alat sekarang dapat mengembalikan hasil pencarian dengan atribusi sumber yang tepat, dan Claude akan secara otomatis mengutip sumber ini dalam responsnya - cocok dengan kualitas kutipan pencarian web. Ini menghilangkan kebutuhan untuk solusi dokumen dalam aplikasi basis pengetahuan khusus. Pelajari lebih lanjut di dokumentasi [search results](/docs/id/build-with-claude/search-results) kami. Untuk mengaktifkan fitur ini, gunakan header beta `search-results-2025-06-09`.

### 30 Juni 2025
- Kami mengumumkan penghentian model Claude Opus 3. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 23 Juni 2025
- Pengguna Konsol dengan peran Developer sekarang dapat mengakses halaman [Cost](https://console.anthropic.com/settings/cost). Sebelumnya, peran Developer memungkinkan akses ke halaman [Usage](https://console.anthropic.com/settings/usage), tetapi bukan halaman Cost.

### 11 Juni 2025
- Kami telah meluncurkan [fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) dalam beta publik, fitur yang memungkinkan Claude untuk melakukan streaming parameter penggunaan alat tanpa buffering / validasi JSON. Untuk mengaktifkan fine-grained tool streaming, gunakan [beta header](/docs/id/api/beta-headers) `fine-grained-tool-streaming-2025-05-14`.

### 22 Mei 2025
- Kami telah meluncurkan [Claude Opus 4 dan Claude Sonnet 4](http://www.anthropic.com/news/claude-4), model terbaru kami dengan kemampuan extended thinking. Pelajari lebih lanjut di dokumentasi [Models & Pricing](/docs/id/about-claude/models) kami.
- Perilaku default dari [extended thinking](/docs/id/build-with-claude/extended-thinking) dalam model Claude 4 mengembalikan ringkasan dari proses thinking penuh Claude, dengan thinking penuh dienkripsi dan dikembalikan di bidang `signature` dari output blok `thinking`.
- Kami telah meluncurkan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) dalam beta publik, fitur yang memungkinkan Claude untuk berpikir di antara panggilan alat. Untuk mengaktifkan interleaved thinking, gunakan [beta header](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14`.
- Kami telah meluncurkan [Files API](/docs/id/build-with-claude/files) dalam beta publik, memungkinkan Anda mengunggah file dan mereferensikannya di Messages API dan alat eksekusi kode.
- Kami telah meluncurkan [Code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, alat yang memungkinkan Claude untuk menjalankan kode Python dalam lingkungan yang aman dan terisolasi.
- Kami telah meluncurkan [MCP connector](/docs/id/agents-and-tools/mcp-connector) dalam beta publik, fitur yang memungkinkan Anda untuk terhubung ke server MCP jarak jauh langsung dari Messages API. 
- Untuk meningkatkan kualitas jawaban dan mengurangi kesalahan alat, kami telah mengubah nilai default untuk parameter `top_p` [nucleus sampling](https://en.wikipedia.org/wiki/Top-p_sampling) di Messages API dari 0.999 menjadi 0.99 untuk semua model. Untuk mengembalikan perubahan ini, atur `top_p` ke 0.999. 
    Selain itu, ketika extended thinking diaktifkan, Anda sekarang dapat mengatur `top_p` ke nilai antara 0.95 dan 1.
- Kami telah memindahkan [Go SDK](https://github.com/anthropics/anthropic-sdk-go) kami dari beta ke GA.
- Kami telah menyertakan granularitas tingkat menit dan jam ke halaman [Usage](https://console.anthropic.com/settings/usage) Konsol bersama dengan tingkat kesalahan 429 di halaman Usage.

### 21 Mei 2025
- Kami telah memindahkan [Ruby SDK](https://github.com/anthropics/anthropic-sdk-ruby) kami dari beta ke GA.

### 7 Mei 2025
- Kami telah meluncurkan web search tool di API, memungkinkan Claude mengakses informasi terkini dari web. Pelajari lebih lanjut di dokumentasi [web search tool](/docs/id/agents-and-tools/tool-use/web-search-tool) kami.

### 1 Mei 2025
- Cache control sekarang harus ditentukan langsung di blok `content` induk dari `tool_result` dan `document.source`. Untuk kompatibilitas mundur, jika cache control terdeteksi di blok terakhir dalam `tool_result.content` atau `document.source.content`, cache control akan secara otomatis diterapkan ke blok induk sebagai gantinya. Cache control pada blok lain dalam `tool_result.content` dan `document.source.content` akan menghasilkan kesalahan validasi.

### 9 April 2025
- Kami meluncurkan versi beta dari [Ruby SDK](https://github.com/anthropics/anthropic-sdk-ruby)

### 31 Maret 2025
- Kami telah memindahkan [Java SDK](https://github.com/anthropics/anthropic-sdk-java) kami dari beta ke GA.
- Kami telah memindahkan [Go SDK](https://github.com/anthropics/anthropic-sdk-go) kami dari alpha ke beta.

### 27 Februari 2025
- Kami telah menambahkan blok sumber URL untuk gambar dan PDF di Messages API. Anda sekarang dapat mereferensikan gambar dan PDF langsung melalui URL alih-alih harus mengenkode base64 mereka. Pelajari lebih lanjut di dokumentasi [vision](/docs/id/build-with-claude/vision) dan [PDF support](/docs/id/build-with-claude/pdf-support) kami.
- Kami telah menambahkan dukungan untuk opsi `none` ke parameter `tool_choice` di Messages API yang mencegah Claude memanggil alat apa pun. Selain itu, Anda tidak lagi diperlukan untuk memberikan `tools` apa pun saat menyertakan blok `tool_use` dan `tool_result`.
- Kami telah meluncurkan endpoint API yang kompatibel dengan OpenAI, memungkinkan Anda menguji model Claude dengan hanya mengubah kunci API, URL dasar, dan nama model Anda dalam integrasi OpenAI yang ada. Lapisan kompatibilitas ini mendukung fungsionalitas chat completions inti. Pelajari lebih lanjut di dokumentasi [OpenAI SDK compatibility](/docs/id/api/openai-sdk) kami.

### 24 Februari 2025
- Kami telah meluncurkan [Claude Sonnet 3.7](http://www.anthropic.com/news/claude-3-7-sonnet), model paling cerdas kami sejauh ini. Claude Sonnet 3.7 dapat menghasilkan respons instan atau menunjukkan extended thinking langkah demi langkah. Satu model, dua cara untuk berpikir. Pelajari lebih lanjut tentang semua model Claude di dokumentasi [Models & Pricing](/docs/id/about-claude/models) kami.
- Kami telah menambahkan dukungan visi ke Claude Haiku 3.5, memungkinkan model untuk menganalisis dan memahami gambar.
- Kami telah merilis implementasi penggunaan alat yang hemat token, meningkatkan kinerja keseluruhan saat menggunakan alat dengan Claude. Pelajari lebih lanjut di dokumentasi [tool use](/docs/id/agents-and-tools/tool-use/overview) kami.
- Kami telah mengubah suhu default di [Console](https://console.anthropic.com/workbench) untuk prompt baru dari 0 menjadi 1 untuk konsistensi dengan suhu default di API. Prompt yang disimpan yang ada tidak berubah.
- Kami telah merilis versi alat yang diperbarui yang memisahkan alat edit teks dan bash dari prompt sistem penggunaan komputer:
  - `bash_20250124`: Fungsionalitas yang sama dengan versi sebelumnya tetapi independen dari penggunaan komputer. Tidak memerlukan header beta.
  - `text_editor_20250124`: Fungsionalitas yang sama dengan versi sebelumnya tetapi independen dari penggunaan komputer. Tidak memerlukan header beta.
  - `computer_20250124`: Alat penggunaan komputer yang diperbarui dengan opsi perintah baru termasuk "hold_key", "left_mouse_down", "left_mouse_up", "scroll", "triple_click", dan "wait". Alat ini memerlukan header anthropic-beta "computer-use-2025-01-24".
  Pelajari lebih lanjut di dokumentasi [tool use](/docs/id/agents-and-tools/tool-use/overview) kami.

### 10 Februari 2025
- Kami telah menambahkan header respons `anthropic-organization-id` ke semua respons API. Header ini menyediakan ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan.

### 31 Januari 2025

- Kami telah memindahkan [Java SDK](https://github.com/anthropics/anthropic-sdk-java) kami dari alpha ke beta.

### 23 Januari 2025

- Kami telah meluncurkan kemampuan kutipan di API, memungkinkan Claude memberikan atribusi sumber untuk informasi. Pelajari lebih lanjut di dokumentasi [citations](/docs/id/build-with-claude/citations) kami.
- Kami telah menambahkan dukungan untuk dokumen teks biasa dan dokumen konten khusus di Messages API.

### 21 Januari 2025

- Kami mengumumkan penghentian model Claude 2, Claude 2.1, dan Claude Sonnet 3. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 15 Januari 2025

- Kami telah memperbarui [prompt caching](/docs/id/build-with-claude/prompt-caching) agar lebih mudah digunakan. Sekarang, ketika Anda menetapkan breakpoint cache, kami akan secara otomatis membaca dari awalan cache terpanjang Anda sebelumnya.
- Anda sekarang dapat memasukkan kata-kata ke mulut Claude saat menggunakan alat.

### 10 Januari 2025

- Kami telah mengoptimalkan dukungan untuk [prompt caching di Message Batches API](/docs/id/build-with-claude/batch-processing#using-prompt-caching-with-message-batches) untuk meningkatkan cache hit rate.

### 19 Desember 2024

- Kami telah menambahkan dukungan untuk [delete endpoint](/docs/id/api/deleting-message-batches) di Message Batches API

### 17 Desember 2024
Fitur berikut sekarang tersedia secara umum di Claude API:

- [Models API](/docs/id/api/models-list): Kueri model yang tersedia, validasi ID model, dan selesaikan [model aliases](/docs/id/about-claude/models#model-names) ke ID model kanonik mereka.
- [Message Batches API](/docs/id/build-with-claude/batch-processing): Proses batch besar pesan secara asinkron dengan harga 50% dari biaya API standar.
- [Token counting API](/docs/id/build-with-claude/token-counting): Hitung token untuk Messages sebelum mengirimnya ke Claude.
- [Prompt Caching](/docs/id/build-with-claude/prompt-caching): Kurangi biaya hingga 90% dan latensi hingga 80% dengan caching dan penggunaan kembali konten prompt.
- [PDF support](/docs/id/build-with-claude/pdf-support): Proses PDF untuk menganalisis konten teks dan visual dalam dokumen.

Kami juga merilis SDK resmi baru:
- [Java SDK](https://github.com/anthropics/anthropic-sdk-java) (alpha)
- [Go SDK](https://github.com/anthropics/anthropic-sdk-go) (alpha)

### 4 Desember 2024

- Kami telah menambahkan kemampuan untuk mengelompokkan berdasarkan kunci API ke halaman [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) dari [Developer Console](https://console.anthropic.com)
- Kami telah menambahkan dua kolom **Last used at** dan **Cost** baru dan kemampuan untuk mengurutkan berdasarkan kolom apa pun di halaman [API keys](https://console.anthropic.com/settings/keys) dari [Developer Console](https://console.anthropic.com)

### 21 November 2024

- Kami telah merilis [Admin API](/docs/id/build-with-claude/administration-api), memungkinkan pengguna untuk secara terprogram mengelola sumber daya organisasi mereka.

### 20 November 2024

- Kami telah memperbarui batas laju kami untuk Messages API. Kami telah menggantikan batas laju token per menit dengan batas laju token input dan output per menit yang baru. Baca lebih lanjut di [dokumentasi](/docs/id/api/rate-limits) kami.
- Kami telah menambahkan dukungan untuk [tool use](/docs/id/agents-and-tools/tool-use/overview) di [Workbench](https://console.anthropic.com/workbench).

### 13 November 2024

- Kami telah menambahkan dukungan PDF untuk semua model Claude Sonnet 3.5. Baca lebih lanjut di [dokumentasi](/docs/id/build-with-claude/pdf-support) kami.

### 6 November 2024

- Kami telah menghentikan model Claude 1 dan Instant. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 4 November 2024

- [Claude Haiku 3.5](https://www.anthropic.com/claude/haiku) sekarang tersedia di Claude API sebagai model hanya teks.

### 1 November 2024

- Kami telah menambahkan dukungan PDF untuk digunakan dengan Claude Sonnet 3.5 baru. Baca lebih lanjut di [dokumentasi](/docs/id/build-with-claude/pdf-support) kami.
- Kami juga telah menambahkan penghitungan token, yang memungkinkan Anda menentukan jumlah total token dalam Message, sebelum mengirimnya ke Claude. Baca lebih lanjut di [dokumentasi](/docs/id/build-with-claude/token-counting) kami.

### 22 Oktober 2024

- Kami telah menambahkan alat penggunaan komputer yang ditentukan Anthropic ke API kami untuk digunakan dengan Claude Sonnet 3.5 baru. Baca lebih lanjut di [dokumentasi](/docs/id/agents-and-tools/tool-use/computer-use-tool) kami.
- Claude Sonnet 3.5, model paling cerdas kami sejauh ini, baru saja mendapat upgrade dan sekarang tersedia di Claude API. Baca lebih lanjut di [dokumentasi Claude Sonnet](https://www.anthropic.com/claude/sonnet).

### 8 Oktober 2024

- Message Batches API sekarang tersedia dalam beta. Proses batch besar kueri secara asinkron di Claude API dengan biaya 50% lebih rendah. Baca lebih lanjut di [dokumentasi](/docs/id/build-with-claude/batch-processing) kami.
- Kami telah melonggarkan pembatasan pada pengurutan giliran `user`/`assistant` di Messages API kami. Pesan `user`/`assistant` berturut-turut akan digabungkan menjadi satu pesan alih-alih error, dan kami tidak lagi memerlukan pesan input pertama menjadi pesan `user`.
- Kami telah menghentikan rencana Build dan Scale mendukung suite fitur standar (sebelumnya disebut Build), bersama dengan fitur tambahan yang tersedia melalui penjualan. Baca lebih lanjut di [informasi harga API](https://claude.com/platform/api) kami.

### 3 Oktober 2024

- Kami telah menambahkan kemampuan untuk menonaktifkan penggunaan alat paralel di API. Atur `disable_parallel_tool_use: true` di bidang `tool_choice` untuk memastikan bahwa Claude menggunakan paling banyak satu alat. Baca lebih lanjut di [dokumentasi](/docs/id/agents-and-tools/tool-use/implement-tool-use#parallel-tool-use) kami.

### 10 September 2024

- Kami telah menambahkan Workspaces ke [Developer Console](https://console.anthropic.com). Workspaces memungkinkan Anda menetapkan batas pengeluaran atau laju kustom, mengelompokkan kunci API, melacak penggunaan berdasarkan proyek, dan mengontrol akses dengan peran pengguna. Baca lebih lanjut di [blog post](https://www.anthropic.com/news/workspaces) kami.

### 4 September 2024

- Kami mengumumkan penghentian model Claude 1. Baca lebih lanjut di [dokumentasi kami](/docs/id/about-claude/model-deprecations).

### 22 Agustus 2024

- Kami telah menambahkan dukungan untuk penggunaan SDK di browser dengan mengembalikan header CORS dalam respons API. Atur `dangerouslyAllowBrowser: true` dalam instansiasi SDK untuk mengaktifkan fitur ini.

### 19 Agustus 2024

- Kami telah memindahkan output token 8,192 dari beta ke ketersediaan umum untuk Claude Sonnet 3.5.

### 14 Agustus 2024

- [Prompt caching](/docs/id/build-with-claude/prompt-caching) sekarang tersedia sebagai fitur beta di Claude API. Cache dan gunakan kembali prompt untuk mengurangi latensi hingga 80% dan biaya hingga 90%.

### 15 Juli 2024

- Hasilkan output hingga 8,192 token panjang dari Claude Sonnet 3.5 dengan header `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15` baru.

### 9 Juli 2024

- Secara otomatis hasilkan kasus uji untuk prompt Anda menggunakan Claude di [Developer Console](https://console.anthropic.com).
- Bandingkan output dari prompt berbeda berdampingan dalam mode perbandingan output baru di [Developer Console](https://console.anthropic.com).

### 27 Juni 2024

- Lihat penggunaan API dan penagihan yang dipecah berdasarkan jumlah dolar, jumlah token, dan kunci API di tab [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) baru di [Developer Console](https://console.anthropic.com).
- Lihat batas laju API Anda saat ini di tab [Rate Limits](https://console.anthropic.com/settings/limits) baru di [Developer Console](https://console.anthropic.com).

### 20 Juni 2024

- [Claude Sonnet 3.5](http://anthropic.com/news/claude-3-5-sonnet), model paling cerdas kami sejauh ini, sekarang tersedia secara umum di Claude API, Amazon Bedrock, dan Google Vertex AI.

### 30 Mei 2024

- [Tool use](/docs/id/agents-and-tools/tool-use/overview) sekarang tersedia secara umum di Claude API, Amazon Bedrock, dan Google Vertex AI.

### 10 Mei 2024

- Alat prompt generator kami sekarang tersedia di [Developer Console](https://console.anthropic.com). Prompt Generator memudahkan untuk memandu Claude menghasilkan prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda. Baca lebih lanjut di [blog post](https://www.anthropic.com/news/prompt-generator) kami.