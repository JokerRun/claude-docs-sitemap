---
source: platform
url: https://platform.claude.com/docs/id/release-notes/overview
fetched_at: 2026-10-02T02:24:19.323378Z
sha256: f2052eeb6266acfb8ed93995640bf013e78df4d071dddd08e1e1fdc9c5bb3e81
---

---
title: Catatan rilis Claude Platform
url: https://platform.claude.com/docs/id/release-notes/overview
description: Pembaruan untuk Claude Platform, termasuk Claude API, SDK klien, dan Claude Console.
---

Catatan rilis Claude Platform mencantumkan perubahan pada Claude API, SDK klien, dan Claude Console, dengan yang terbaru lebih dulu.

<Tip>
  Untuk catatan rilis tentang Claude Apps, lihat [Catatan rilis untuk Claude Apps di Claude Help Center](https://support.claude.com/en/articles/12138966-release-notes).

  Untuk pembaruan Claude Code, lihat [CHANGELOG.md lengkap](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) di repositori `claude-code`.
</Tip>

### 28 September 2026

* Kami telah meluncurkan **Claude Sonnet 5.5** (`claude-sonnet-5-5`). Model ini tersedia di Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Untuk "context window" (jendela konteks), batas output, dan harganya, lihat [halaman model Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview).
* Kode yang ditulis untuk Claude Sonnet 5 dapat rusak di Claude Sonnet 5.5 dalam lima cara. Untuk menonaktifkan thinking di awal, kirim `thinking: {"type": "between_tools"}` alih-alih `"disabled"`, pada effort `high` atau lebih rendah. "Tool use" (penggunaan alat) yang dipaksakan (tipe `tool_choice` `any` dan `tool`) mengembalikan error 400. Blok thinking terikat pada model dan percakapan. Di Claude API dan Google Cloud, alat computer use `computer_20251124` yang lebih lama tidak diterima. Alat advisor menolak Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5 sebagai advisor. Lihat [Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5) untuk setiap perubahan dan [panduan migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide) untuk contoh permintaan sebelum dan sesudah. Untuk pola prompting khusus model, lihat [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5).
* Blok thinking yang dihasilkan Claude Sonnet 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya. Ketika akun lain mengirim salah satu blok ini, API membuang blok tersebut sebelum model melihatnya, dan permintaan tetap berhasil. Blok dari model sebelumnya tidak terpengaruh. Lihat [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

### 24 September 2026

* Kami melanjutkan kembali penagihan untuk penolakan (refusal) yang terjadi sebelum output apa pun ketika `stop_details.category` bernilai `"bio"`, `"frontier_llm"`, atau `"reasoning_extraction"`, yaitu kategori tempat kami mengukur volume false positive yang rendah. Penolakan di tengah stream sudah ditagih sebelumnya. Penolakan yang ditagih berdasarkan perubahan ini dikenakan biaya seperti permintaan lainnya, sesuai tarif model yang menjalankannya. Penolakan sebelum output apa pun dalam kategori lain tetap tidak ditagih, dan kredit fallback tidak berubah. Perubahan ini berlaku di semua platform. Lihat [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).
* Endpoint sesi lokal [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) telah keluar dari beta untuk sesi Claude for Microsoft 365 di Excel, PowerPoint, Word, dan Outlook (nilai `product_surface` yang diawali dengan `office_agents`). Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).
* [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dari [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) tidak lagi mengembalikan nama file, nama dokumen proyek, atau judul artifact. Field `filename` dan `title` pada aktivitas file, dokumen proyek, dan artifact kini selalu kosong atau dihilangkan, termasuk pada aktivitas yang tercatat sebelum perubahan ini. Untuk mencari nama atau judul berdasarkan ID pada aktivitas, gunakan Compliance Access Key dengan scope `read:compliance_user_data`. Lihat [Memahami objek Activity](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object).

### 23 September 2026

* [Diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) telah keluar dari beta di Claude API dan tidak lagi memerlukan beta header `cache-diagnosis-2026-04-07`. Sertakan objek `diagnostics` pada permintaan Messages untuk ikut serta; permintaan yang masih mengirim header tersebut tetap berfungsi seperti sebelumnya. Respons dari `POST /v1/messages` kini selalu menyertakan field `diagnostics`, yang bernilai `null` ketika permintaan tidak menyertakan objek `diagnostics`.

### 22 September 2026

* Kami telah meluncurkan **Claude Opus 5.5** (`claude-opus-5-5`), model untuk agentic coding dan pekerjaan pengetahuan yang berjalan lama. Model ini memiliki [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, maksimum 128k token output, dan "adaptive thinking" (pemikiran adaptif) yang [selalu aktif](https://platform.claude.com/docs/id/build-with-claude/thinking), dengan harga $4 / $20 USD per MTok (Claude Opus 5 seharga $5 / $25). Claude Opus 5.5 tersedia di Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Lihat [Yang baru di Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/whats-new-opus-5-5) untuk kemampuan, perubahan API, dan panduan migrasi.
* Pada Claude Opus 5.5, thinking tidak dapat dinonaktifkan: `thinking: {"type": "disabled"}` dan `thinking: {"type": "enabled", ...}` mengembalikan error 400. Hilangkan field `thinking` dan kendalikan kedalaman thinking dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort). Tipe `tool_choice` `any` dan `tool` juga mengembalikan error 400, seperti pada Claude Fable 5.1; gunakan `auto` dengan [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). Di Claude API dan Google Cloud, [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) pada model ini memerlukan toolset `computer_toolset_20260801` dan alat `computer_20251124` yang lebih lama mengembalikan error 400; di Amazon Bedrock, `computer_20251124` tetap berfungsi. Lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide#migrating-from-claude-opus-5).
* [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) tersedia untuk Claude Opus 5.5 di Claude API.
* Alat kini dapat didefinisikan di dalam [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta), dalam beta di Claude API dengan beta header `inline-tools-2026-09-15`. Blok `tool_addition` dapat membawa definisi lengkap alat (`tool: {"type": "tool_definition", "definition": {...}}`), sehingga Anda dapat menambahkan alat, mengubah skemanya, atau memindahkan server tool ke versi yang lebih baru tanpa mengedit `tools` atau membatalkan cache yang dibuat oleh "prompt caching" (caching prompt). Header yang sama mencakup penambahan dan penghapusan alat berdasarkan referensi. Dengan beta header `mcp-client-2026-09-15` dari konektor MCP juga, definisi tersebut dapat berupa toolset MCP, dan respons mencatat daftar alat yang diambil dari setiap server dalam blok `mcp_tool_listing`, yang mengunci daftar tersebut saat Anda mengirimkannya kembali.

### 18 September 2026

* Untuk [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics), respons terhadap permintaan yang mengirim beta header `cache-diagnosis-2026-04-07` kini selalu menyertakan field `diagnostics`. Field tersebut bernilai `null` ketika permintaan tidak menyertakan objek `diagnostics`. Sebelumnya field tersebut dihilangkan dalam kasus itu.
* Endpoint sesi lokal [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini juga mengembalikan transkrip sesi Claude in Chrome (nilai `product_surface` `claude_in_chrome`), dalam beta untuk organisasi Claude Enterprise, dengan Compliance Access Key Anda yang sudah ada dan scope `read:compliance_user_data`. Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).

### 14 September 2026

* Messages API kini dapat [memadatkan percakapan sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) di Claude API, dalam beta dengan beta header `compact-2026-09-04`. Kirim parameter tingkat atas `compaction`, dan API mengembalikan blok `compaction` bertanda tangan yang merangkum pesan yang Anda kirim. Pada permintaan berikutnya, kirim blok tersebut terlebih dahulu, sebagai pengganti pesan-pesan tersebut. Anda memilih kapan melakukan pemadatan, permintaan dapat berjalan di latar belakang, dan Anda dapat mempertahankan giliran terbaru kata demi kata setelah ringkasan. Pada model dengan preserved thinking, thinking dalam giliran yang dipertahankan tersebut dapat tetap valid.
* Dengan beta header `thinking-binding-controls-2026-08-01`, field respons `input_transformations` mendapatkan tipe entri kedua, `thinking_mismatch_allowed`. Entri ini menyebutkan blok thinking yang gagal dalam pemeriksaan prefiks pada permintaan di mana API tidak memberlakukan pemeriksaan tersebut: pada Claude Fable 5.1, misalnya, permintaan dari akun yang dibuat sebelum 31 Agustus 2026, dengan `prefix_mismatch_behavior` tidak diatur. Blok tersebut tetap mencapai model tanpa perubahan. Catat entri-entri ini untuk menemukan pengeditan riwayat dalam lalu lintas produksi sebelum Anda memilih untuk mengaktifkan penegakan. Lihat [Mengatur perilaku mismatch dan membaca `input_transformations`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#preserved-thinking-controls).

### 10 September 2026

* Kebijakan izin Claude Managed Agents kini menyertakan `auto`: server mengevaluasi setiap panggilan alat agen atau MCP dan menjalankannya, menolaknya, atau menjeda untuk menunggu persetujuan Anda. Event `agent.tool_use` dan `agent.mcp_tool_use` melaporkan bagaimana setiap panggilan dievaluasi dalam field `evaluation` di samping `evaluated_permission`. Lihat [Biarkan server mengevaluasi setiap panggilan dengan `auto`](https://platform.claude.com/docs/id/managed-agents/permission-policies#let-the-server-evaluate-each-call-with-auto).
* Versi 1.32.0 dari CLI `ant` menambahkan `ant beta:sessions connect`, yang menghubungkan terminal Anda ke sesi Claude Managed Agents. Anda dapat mengikuti sesi secara langsung, mengirim pesan, dan mengizinkan atau menolak panggilan alat yang sedang menunggu persetujuan. Berikan `--web` untuk menyajikan penampil sesi Claude Console secara lokal dan membuka sesi di sana sebagai gantinya. Lihat [Terhubung ke sesi Managed Agents dari terminal Anda](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect).

### 9 September 2026

* Untuk [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics), API kini menyimpan fingerprint permintaan hanya ketika permintaan menyertakan objek `diagnostics`. Permintaan yang hanya mengirim beta header `cache-diagnosis-2026-04-07` tetap diterima, tetapi tidak ada fingerprint yang disimpan. Giliran berikutnya yang mengarahkan `previous_message_id` ke permintaan tersebut melaporkan `previous_message_not_found`. Sertakan `diagnostics` pada setiap giliran, dengan `"previous_message_id": null` pada giliran pertama.

### 3 September 2026

* Versi 1.30.0 dari CLI `ant` menambahkan `ant apply`, yang membuat dan memperbarui agen, environment, skill, memory store, dan deployment dari file di repositori Anda. Deskripsikan setiap sumber daya dalam sebuah file, jalankan `ant apply`, dan setujui rencana yang dicetaknya. Commit lockfile `claude-lock.json` yang ditulisnya agar eksekusi berikutnya, di mesin Anda atau di CI, memperbarui sumber daya yang sama alih-alih membuat yang baru. Lihat [Mengelola sumber daya sebagai kode dengan ant apply](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply).
* Perubahan [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta), dalam beta, juga tersedia di [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai) untuk Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5, dengan beta header `mid-conversation-output-config-2026-07-01` yang sama.

### 1 September 2026

* Kami telah meluncurkan **Claude Fable 5.1** (`claude-fable-5-1`), penerus Claude Fable 5 untuk agentic coding, pekerjaan pengetahuan, dan riset yang berjalan lama, bersama dengan **Claude Mythos 5.1** (`claude-mythos-5-1`) untuk peserta Project Glasswing. Kedua model mendukung [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, maksimum 128k token output, dan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif, dengan harga $10 / $50 USD per MTok, sama seperti Claude Fable 5, dengan pembacaan cache dipangkas menjadi $0,25 per MTok. Claude Fable 5.1 tersedia di Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Lihat [Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) untuk kemampuan, perubahan API, dan panduan migrasi.
* Pembacaan cache pada caching prompt di Claude Fable 5.1 dan Claude Mythos 5.1 berbiaya $0,25 USD per juta token: 0,025x harga input dasar, dibandingkan dengan 0,1x pada model lain. Penulisan cache tidak berubah. Lihat [Harga caching prompt](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching).
* Pada Claude Fable 5.1 dan Claude Mythos 5.1, tipe `tool_choice` `any` dan `tool` tidak didukung dan mengembalikan error 400. `auto` dan `none` tidak berubah. Untuk menjamin input alat yang sesuai skema, gunakan [strict tool use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) atau [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).
* Blok thinking yang dihasilkan oleh Claude Fable 5.1 dan Claude Mythos 5.1 dipertahankan hanya untuk model yang menghasilkannya atau model yang lebih baru: model sebelumnya tidak dapat membacanya, dan API membuang blok yang diputar ulang ke model sebelumnya. Claude Fable 5.1 menerima blok thinking dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude sebelumnya. Pada Claude Fable 5.1, API juga [memeriksa bahwa tidak ada yang berubah sebelum sebuah blok](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation): untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, memutar ulang blok setelah prompt `system`, `tools`, atau pesan sebelumnya berubah akan mengembalikan error 400. Dengan beta header `thinking-binding-controls-2026-08-01`, blok yang dibuang dilaporkan dalam field respons `input_transformations`, dan `thinking.block_binding.prefix_mismatch_behavior` memilih antara menolak dan membuang blok yang riwayatnya berubah. Lihat [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking).
* Perubahan effort per pesan tersedia dalam beta pada Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5 di Claude API. Tambahkan pesan `role: "system"` dengan `output_config.effort` di dalam `messages` untuk mengubah effort pada giliran berikutnya sambil mempertahankan cache dari caching prompt. Sertakan beta header `mid-conversation-output-config-2026-07-01` dalam permintaan Anda. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).
* [Pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) tersedia dalam beta (header `mid-conversation-system-clear-at-2026-08-21`). Atur `clear_at: "next_user_message"` pada pesan `role: "system"` di tengah percakapan, dan pesan tersebut dirender hanya untuk giliran saat ini, lalu tetap berada dalam riwayat tanpa biaya token. Pengingat per giliran tidak menumpuk dan tidak membatalkan cache dari caching prompt atau blok thinking berikutnya.
* `thinking.display` menerima nilai ketiga, `"updates"`, dalam beta (header `thinking-display-updates-2026-08-18`). Penalaran dikembalikan dengan field `thinking` kosong, seperti pada `"omitted"`, dan pembaruan progres singkat yang ditulis Claude Fable 5.1, Claude Mythos 5.1, dan Claude Fable 5 di antara panggilan alat dikembalikan sebagai teks, paling banyak satu blok `thinking` sebelum panggilan alat. Lihat [Pembaruan progres di antara panggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).
* Teks yang dihasilkan oleh Claude Fable 5.1 dan Claude Mythos 5.1 membawa watermark teks Anthropic, dan file gambar, video, dan audio yang didukung yang dihasilkan Claude melalui [alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) membawa C2PA Content Credentials saat Anda mengambilnya melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files) di Claude API. Penandaan ini tidak memerlukan perubahan apa pun pada permintaan atau penanganan respons Anda.
* Seperti Claude Fable 5, kedua model memerlukan retensi data 30 hari dan tidak tersedia di bawah zero data retention kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Panduan untuk endpoint Claude Enterprise dari [Admin API](https://platform.claude.com/docs/id/api/beta/organization) ([manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) dan [batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api)), [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api), dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini menampilkan header `anthropic-version`; kirimkan header tersebut pada setiap permintaan ke endpoint ini, seperti di bagian lain Claude API. Lihat [Versi API](https://platform.claude.com/docs/id/api/versioning).

### 27 Agustus 2026

* Di Python SDK 1.2.0, TypeScript SDK 0.122.0, Go SDK 1.68.0, Java SDK 2.59.0, Ruby SDK 1.67.0, dan C# SDK 12.44.0, `client.beta.files` dan `client.beta.skills` tidak lagi mengirim beta header `files-api-2025-04-14` dan `skills-2025-10-02` dan mengembalikan bentuk yang sama seperti `client.files` dan `client.skills`. Dengan perubahan ini, `client.beta.skills.delete()` menghapus Skill beserta semua versinya, dan tipe Messages beta `BetaSkill` (referensi Skill container) diganti namanya menjadi `BetaContainerSkill`. Permintaan yang masih mengirim beta header tetap menerima bentuk beta. Lihat [Migrasi dari `files-api-2025-04-14`](https://platform.claude.com/docs/id/build-with-claude/files#migrate-from-files-api-2025-04-14) dan [Migrasi dari `skills-2025-10-02`](https://platform.claude.com/docs/id/build-with-claude/skills-guide#migrate-from-skills-2025-10-02).

- Anda kini dapat membuat **kunci pribadi** dan **kunci akun layanan** di Claude Console. Kunci ini bertindak sebagai Anda atau sebagai [akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts), dengan izin yang sama, dan berhenti berfungsi ketika akun yang terhubung dihapus dari organisasi. Hal ini memudahkan admin organisasi untuk melacak penggunaan setiap akun, dan memastikan penggunaan kunci tersebut sah. "API keys" (kunci API) ini dapat dibatasi ke workspace tertentu atau [berfungsi pada endpoint admin dan di seluruh workspace mana pun](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) yang dapat diakses akun tersebut. Kunci API workspace tetap didukung sebagai opsi lama. Lihat [Kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys) untuk informasi lebih lanjut.

### 26 Agustus 2026

* Endpoint sesi [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) telah keluar dari beta untuk sesi Cowork dan Claude Code. Lihat [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions).
* Endpoint sesi lokal [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini juga mengembalikan transkrip sesi Claude Science (nilai `product_surface` `claude_science`) dan sesi Claude for Microsoft 365 di Excel, PowerPoint, Word, dan Outlook (nilai `product_surface` yang diawali dengan `office_agents`), dalam beta untuk organisasi Claude Enterprise, dengan Compliance Access Key Anda yang sudah ada dan scope `read:compliance_user_data`. Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) kini tersedia di CLI `ant` dan SDK Python, TypeScript, C#, Go, Java, PHP, dan Ruby di bawah `client.beta.organization`. Cakupannya meliputi info organisasi, anggota, undangan, workspace dan anggota workspace, kunci API, "rate limits" (batas laju), akun layanan, penerbit dan aturan workload identity federation, serta kunci enkripsi yang dikelola pelanggan. Laporan penggunaan dan biaya serta endpoint manajemen pengguna dan analitik Claude Enterprise tetap hanya tersedia melalui curl. CLI dan SDK membaca kunci Admin API dari `ANTHROPIC_API_KEY` atau token OAuth `org:admin` dari `ANTHROPIC_AUTH_TOKEN`.

### 20 Agustus 2026

* Kami telah merilis **v1.0 dari [Python SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python)**. Lapisan HTTP SDK berpindah dari `httpx` ke [httpx2](https://httpx2.pydantic.dev), sebuah fork yang terpelihara dan kompatibel secara API: buat objek `http_client`, `Timeout`, dan transport kustom dari `httpx2` (helper `DefaultHttpxClient` tidak berubah), dan panggil `httpx2.alias_httpx()` saat startup jika Anda mengandalkan library tracing atau mocking yang mem-patch `httpx`. v1.0 memerlukan Python 3.10 atau lebih baru dan menghapus surface yang sudah lama deprecated, termasuk Text Completions API lama, parameter `temperature`, `top_p`, dan `top_k` pada metode Messages, serta `compaction_control` sisi klien pada tool runner. Pada klien async, hasil `.with_raw_response` kini memerlukan `await response.parse()`, dan `AnthropicBedrock` kini memunculkan error ketika tidak ada region AWS yang dikonfigurasi alih-alih menggunakan `us-east-1` secara default. Lihat [panduan migrasi v1](https://github.com/anthropics/anthropic-sdk-python/blob/main/MIGRATION.md) untuk setiap perubahan beserta cuplikan sebelum dan sesudah.
* Toolset [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`computer_toolset_20260801` dan `browser_toolset_20260801`) kini tersedia di [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai) untuk Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, dan Claude Opus 4.8. Permintaan menggunakan entri `tools` yang sama seperti di Claude API.

### 19 Agustus 2026

* [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) telah keluar dari beta di Claude API sebagai toolset `computer_toolset_20260801`: tanpa beta header, aksi batch (beberapa aksi dalam satu giliran), `zoom` diaktifkan secara default, dan konfigurasi per anggota melalui `configs`. Versi beta sebelumnya tetap tersedia. Meningkatkan integrasi yang ada akan mengubah bentuk permintaan dan penanganan alat; lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).
* Kami telah meluncurkan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`), toolset klien untuk mengendalikan browser yang di-host oleh aplikasi Anda. Alat ini bekerja di dalam viewport browser alih-alih seluruh desktop, membaca halaman itu sendiri (accessibility tree, elemen, formulir, dan tab-nya) serta menambahkan referensi elemen, input formulir, manajemen tab, pelaporan unduhan, dan unggah file opsional (opt-in) di atas kontrol screenshot-dan-klik.
* Kedua toolset tersedia untuk Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, dan Claude Opus 4.8 di Claude API.
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files) telah keluar dari beta di Claude API. Permintaan ke endpoint `/v1/files`, dan permintaan Messages API yang mereferensikan file yang diunggah, tidak lagi memerlukan beta header `files-api-2025-04-14`. Permintaan yang dikirim tanpa header menggunakan format respons saat ini: [kedaluwarsa file](https://platform.claude.com/docs/id/build-with-claude/files#file-expiration) (atur `expires_in_seconds` saat Anda mengunggah file; objek file melaporkan `expires_at`), serta [paginasi](https://platform.claude.com/docs/id/api/overview#pagination) `page` dan `next_page` ditambah filter `ids[]` saat Anda [mencantumkan file](https://platform.claude.com/docs/id/build-with-claude/files#list-files). Permintaan `/v1/files` yang masih mengirim beta header tetap berfungsi dan mengembalikan format respons sebelumnya. Untuk memindahkan integrasi yang ada agar tidak lagi menggunakan header tersebut, lihat [Migrasi dari `files-api-2025-04-14`](https://platform.claude.com/docs/id/build-with-claude/files#migrate-from-files-api-2025-04-14).
* [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan Skills API (`/v1/skills`) telah keluar dari beta di Claude API. Permintaan tidak lagi memerlukan beta header `skills-2025-10-02`, termasuk permintaan Messages API yang memuat Skills melalui parameter `container`. Permintaan yang masih mengirim header tersebut tetap berfungsi tanpa perubahan. Lihat [Menggunakan Agent Skills dengan API](https://platform.claude.com/docs/id/build-with-claude/skills-guide). Untuk memindahkan integrasi yang ada agar tidak lagi menggunakan header tersebut, lihat [Migrasi dari `skills-2025-10-02`](https://platform.claude.com/docs/id/build-with-claude/skills-guide#migrate-from-skills-2025-10-02).
* Endpoint manajemen pengguna [Admin API](https://platform.claude.com/docs/id/api/beta/organization) untuk organisasi **Claude Enterprise** (claude.ai) (anggota, undangan, grup, dan peran kustom) telah keluar dari beta. Header `anthropic-beta: ce-user-management-2026-07-13` tidak lagi diperlukan pada permintaan grup dan peran kustom; permintaan yang masih mengirimnya diterima tanpa perubahan. Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management).
* Anda kini dapat membatasi situs mana yang dapat dijangkau oleh alat `web_search` dan `web_fetch` milik agen Claude Managed Agents. Atur `allowed_domains` atau `blocked_domains` pada entri alat di array `configs` `agent_toolset_20260401`; `web_fetch` juga menerima `max_content_tokens` dan `web_search` menerima `user_location`. Setiap entri `configs` diidentifikasi oleh `name`-nya dan diberi tipe oleh `type` opsional, dan permintaan yang hanya meneruskan `name`, `enabled`, dan `permission_policy` tetap berfungsi; di SDK bertipe, entri `configs` menjadi tipe per alat. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).
* Sesi Claude Managed Agents yang berjalan di [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) kini dapat melampirkan [memory store](https://platform.claude.com/docs/id/managed-agents/memory). Worker SDK Python, TypeScript, dan Go mengunduh setiap store yang dilampirkan ke dalam sandbox di `mount_path`-nya dan menyinkronkan perubahan agen kembali ke store tersebut. Lihat [Menggunakan memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores).
* Penampil sesi di Claude Console telah didesain ulang dengan minimap timeline, transkrip yang dikelompokkan berdasarkan permintaan model, dan panel Inspector untuk detail dan biaya sesi, event mentah, statistik per alat, sumber daya yang di-mount, dan aktivitas per thread. Lihat [Observabilitas Console](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#console-observability).

### 18 Agustus 2026

* Workbench kini menjadi [**playground**](https://platform.claude.com/playground) di Claude Console. Playground mendukung setiap parameter Messages API dan menyertakan template yang mendemonstrasikan fitur API seperti code execution dan web search. Playground menampilkan permintaan SDK lengkap dan respons API untuk setiap eksekusi, untuk membantu Anda memahami API dan membangun dengannya. Untuk informasi lebih lanjut, lihat [Claude Help Center](https://support.claude.com/en/articles/8606378-how-do-i-use-playground) atau coba di [platform.claude.com/playground](https://platform.claude.com/playground).

### 11 Agustus 2026

* [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini mengembalikan transkrip sesi Cowork dan Claude Code yang berjalan di mesin pengguna Anda, dalam beta untuk organisasi Claude Enterprise. `GET /v1/compliance/apps/sessions/local` mencantumkan sesi di seluruh organisasi Anda, `GET /v1/compliance/apps/sessions/local/{session_id}` mengambil metadata satu sesi, dan `GET /v1/compliance/apps/sessions/local/{session_id}/messages` mengembalikan transkripnya, semuanya dengan Compliance Access Key Anda yang sudah ada dan scope `read:compliance_user_data`. Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).
* Kami telah menambahkan header respons `anthropic-workspace-id` ke Claude API. Header ini membawa ID berawalan `wrkspc_` dari workspace yang menjadi hasil resolusi kunci API atau token akses pada permintaan, termasuk Default Workspace organisasi Anda. Lihat [Mengidentifikasi workspace di balik respons API](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response).

### 10 Agustus 2026

* Harga perkenalan untuk **Claude Sonnet 5** ($2 / $10 per MTok) kini menjadi harga standar: kenaikan yang sebelumnya dijadwalkan menjadi $3 / $15 per MTok pada 1 September 2026 tidak akan terjadi. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing).

### 7 Agustus 2026

* Anda kini dapat menetapkan anggaran pada sesi Claude Managed Agents: batas keras untuk pengeluaran sesi, dihitung berdasarkan tarif daftar publik. Sesi yang mencapai anggarannya akan dijeda dengan stop reason `budget_reached` alih-alih memulai permintaan model baru; mengubah atau menghapus anggaran akan melanjutkannya. Deployment menerima anggaran yang sama dan menerapkannya ke setiap sesi yang dimulainya. Lihat [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets).
* Anda kini dapat memberikan advisor pada sesi Claude Managed Agents: model yang setidaknya sama mampunya dengan model milik agen itu sendiri, yang dapat dikonsultasikan oleh thread utama sesi di tengah giliran untuk mendapatkan panduan strategis. Konfigurasikan sebagai entri `{"type": "advisor"}` dalam roster multiagent agen, dengan menyebutkan `model` yang akan dikonsultasikan. Lihat [Memberikan advisor pada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor).
* Anda kini dapat mengontrol di mana inferensi model berjalan untuk agen Claude Managed Agents. Atur `inference_geo` di dalam objek `model` saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo), atau [menimpanya untuk satu sesi](https://platform.claude.com/docs/id/managed-agents/sessions#pin-the-inference-geo-for-a-session). Lihat [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) untuk geo yang tersedia dan harganya.
* Sesi Claude Managed Agents kini dapat [memuat skill dari repositori GitHub](https://platform.claude.com/docs/id/managed-agents/skills#load-skills-from-a-github-repository). Ketika sesi [me-mount repositori](https://platform.claude.com/docs/id/managed-agents/github), skill apa pun di direktori root `.claude/skills`-nya ditemukan secara otomatis saat sesi dimulai dan tersedia bagi agen untuk sesi tersebut.

### 5 Agustus 2026

* **Inference hooks** kini tersedia dalam beta untuk organisasi Claude Enterprise. Arahkan Claude ke server keamanan AI organisasi Anda, dan setiap prompt yang diatur di claude.ai, Cowork, dan Claude Code akan ditahan untuk menunggu putusan izinkan atau tolak dari server sebelum inferensi dilanjutkan. Permintaan ditandatangani, penanganan kegagalan dapat dikonfigurasi, dan setiap penolakan dicatat dalam [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) kepatuhan. Lihat [Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks).
* Kami telah menghentikan model Claude Opus 4.1 (`claude-opus-4-1-20250805`). Semua permintaan ke model ini di Claude API kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Opus 5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 3 Agustus 2026

* [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini mengembalikan transkrip sesi Cowork yang dimulai di claude.ai web atau seluler, dalam beta untuk organisasi Claude Enterprise. `GET /v1/compliance/apps/sessions/remote` mencantumkan sesi dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi, menggunakan Compliance Access Key Anda yang sudah ada dengan scope `read:compliance_user_data`. Lihat [Sesi di cloud](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions).

### 1 Agustus 2026

* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) (pratinjau riset) kini mendukung Claude Opus 5. Lihat [Model yang didukung](https://platform.claude.com/docs/id/managed-agents/dreams#limits).

### 24 Juli 2026

* Kami telah meluncurkan **Claude Opus 5** (`claude-opus-5`), peningkatan besar dibandingkan Claude Opus 4.8. Claude Opus 5 mendukung ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (sebagai nilai default sekaligus maksimum), maksimum 128k token output, dan ["thinking" (pemikiran)](https://platform.claude.com/docs/id/build-with-claude/thinking) yang aktif secara default. Harganya $5 / $25 USD per MTok, sama dengan Claude Opus 4.8. Model ini tersedia di Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude on Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Lihat [Yang baru di Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview) untuk fitur baru, perubahan perilaku, dan panduan migrasi, serta [ikhtisar model](https://platform.claude.com/docs/id/models/overview) untuk spesifikasi lengkap.
* Pada Claude Opus 5, thinking hanya dapat dinonaktifkan pada effort `high` atau lebih rendah. `thinking: {"type": "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Ini merupakan "breaking change" (perubahan yang merusak kompatibilitas) dari Claude Opus 4.8. Lihat [Yang baru di Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview).
* ["Effort" (upaya)](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol utama untuk mengarahkan Claude Opus 5. Model ini mendukung seluruh tingkatan (`low`, `medium`, `high`, `xhigh`, `max`), dengan `max` untuk pekerjaan yang sangat menuntut kapabilitas.
* Perubahan alat di tengah percakapan kini tersedia dalam beta di Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 5. Anda dapat menambahkan atau menghapus alat di antara giliran percakapan tanpa kehilangan prompt yang sudah di-cache oleh "prompt caching" (caching prompt). Sertakan "beta header" (header beta) `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda.
* Parameter `fallbacks` kini mendukung mode `"default"`, yang menerapkan model "fallback" (cadangan) yang direkomendasikan Anthropic berdasarkan kategori penolakan. Fallback sisi server masih dalam beta, dan mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Kami telah menghapus ["fast mode" (mode cepat)](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.7. Permintaan ke `claude-opus-4-7` dengan `speed: "fast"` kini mengembalikan error. Berbeda dengan Claude Opus 4.6, permintaan tersebut tidak dialihkan ke kecepatan standar. Claude Opus 4.7 sendiri tetap tersedia pada kecepatan standar. Untuk terus menggunakan fast mode, migrasikan ke [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview) atau Claude Opus 4.8. Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 22 Juli 2026

* Anda kini dapat menetapkan tingkat `effort` pada konfigurasi model agen Claude Managed Agents. Teruskan `effort` di dalam objek `model` saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent). Lihat [Tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels) untuk mengetahui fungsi setiap tingkat.
* "Webhooks" (webhook) untuk Claude Managed Agents kini mencakup siklus hidup environment dan memory store, yaitu empat jenis event `environment.*` dan tiga jenis event `memory_store.*`. Anda dapat merespons perubahan siklus hidup environment dan memory store tanpa "polling" (pemeriksaan berkala). Lihat tab Environment events dan Memory store events di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types).
* Saat membuat sesi Claude Managed Agents, Anda kini dapat [mengisi sesi dengan event awal](https://platform.claude.com/docs/id/managed-agents/sessions#seed-the-session-with-initial-events). Teruskan `initial_events` pada `POST /v1/sessions` dengan maksimal 50 event `user.message` dan `user.define_outcome`. Jika daftar tersebut tidak kosong, loop agen langsung dimulai dalam panggilan yang sama, sehingga Anda tidak perlu mengirim permintaan send-events terpisah untuk memulai pekerjaan.
* Field `version` kini bersifat opsional saat [memperbarui agen Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent). Sertakan field ini untuk "optimistic concurrency" (konkurensi optimistis), dengan ketidakcocokan versi mengembalikan error 409. Jika dihilangkan, pembaruan diterapkan tanpa syarat. Lihat [Semantik pembaruan](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-semantics).
* Stream event thread sesi Claude Managed Agents kini mendukung ["event deltas" (delta event)](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas). `GET /v1/sessions/{session_id}/threads/{thread_id}/stream` menerima parameter kueri `event_deltas[]` yang sama dengan stream tingkat sesi, sehingga Anda dapat melihat pratinjau teks subagen selagi model menghasilkannya. Setiap koneksi hanya menampilkan pratinjau thread yang sedang dibacanya. Lihat [Pratinjau event thread sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#preview-session-thread-events).

### 17 Juli 2026

* **Workbench** lama ([platform.claude.com/workbench](https://platform.claude.com/workbench)) di Claude Console akan dihentikan, dan aksesnya berakhir pada 17 Agustus 2026. Prompt, variabel, dan eval yang tersimpan tidak didukung di [Workbench](https://platform.claude.com/playground) versi terbaru. Anda dapat mengekspor data yang ingin disimpan melalui banner dan di bagian **Organizational Settings**. Untuk informasi lebih lanjut, lihat [Bagaimana cara menggunakan Workbench?](https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench) di Claude Help Center.
* API alat prompt eksperimental untuk membuat, menyempurnakan, dan mengubah prompt menjadi template (`/v1/experimental/generate_prompt`, `/v1/experimental/improve_prompt`, dan `/v1/experimental/templatize_prompt`) akan dihentikan bersama Workbench pada 17 Agustus 2026. Setelah dihapus, permintaan ke endpoint ini akan mengembalikan error.

### 15 Juli 2026

* [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) tersedia di Claude Fable 5, Claude Mythos 5, dan Claude Opus 4.8, melalui Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai). Header beta tidak diperlukan. Informasi ini mengoreksi catatan ketersediaan sebelumnya.

### 14 Juli 2026

* Anda kini dapat mengelola anggota organisasi **Claude Enterprise** (claude.ai) Anda dengan [Admin API](https://platform.claude.com/docs/id/api/beta/organization). Fitur ini tersedia dalam beta untuk semua organisasi Claude Enterprise dan memungkinkan Anda untuk:

  * mencantumkan anggota dan mencarinya berdasarkan alamat email,
  * mengubah peran anggota dan menghapus anggota,
  * mengirim dan menarik undangan,
  * mengelola grup beserta keanggotaannya,
  * membaca peran kustom.

  Permintaan untuk grup dan peran kustom memerlukan header beta `anthropic-beta: ce-user-management-2026-07-13`, sedangkan permintaan untuk anggota dan undangan tidak memerlukan header beta. "Admin API key" (kunci Admin API) dengan scope `read:org_audit` juga dapat memanggil semua endpoint `GET` manajemen pengguna. Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management).

### 10 Juli 2026

* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) (pratinjau riset) kini mendukung Claude Fable 5 dan Claude Sonnet 5. Lihat [Model yang didukung](https://platform.claude.com/docs/id/managed-agents/dreams#limits).
* Kami telah memperluas dokumentasi [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency) tentang event `cmek_preserve` dengan contoh filter, contoh payload event, dan dua kode alasan preservasi (`policy_violation_investigation`, `csae_report`). Dokumentasi kini juga menjelaskan bahwa event preservasi tetap dicatat, baik preservasi dimulai oleh peninjau manusia maupun oleh pipeline keamanan otomatis. Lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation).

### 8 Juli 2026

* Anda kini dapat menetapkan masa kedaluwarsa saat membuat "API key" (kunci API) atau kunci Admin API di [Claude Console](https://platform.claude.com/settings/keys). Pilih preset, durasi kustom, atau **Never**. Untuk kunci dengan masa berlaku minimal 7 hari, Anthropic akan mengirim email kepada pembuatnya sebelum kunci kedaluwarsa. Kunci yang sudah ada tidak terpengaruh. Admin API melaporkan masa kedaluwarsa setiap kunci di field [`expires_at`](https://platform.claude.com/docs/id/api/beta/organization/api_keys/list). Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration).

### 2 Juli 2026

* Kami telah menambahkan header beta `agent-memory-2026-07-22`, yang mengubah perilaku [pencantuman memori](https://platform.claude.com/docs/id/managed-agents/memory#list-memories) (`GET /v1/memory_stores/{memory_store_id}/memories`) sebagai berikut:

  * Hasil dikembalikan dalam urutan stabil yang ditentukan server, dan parameter `order_by` serta `order` diabaikan.
  * `depth` hanya menerima `0`, `1`, atau tidak disertakan. Nilai lain mengembalikan error `400`.
  * `path_prefix` harus diakhiri dengan `/` dan dicocokkan per segmen path secara utuh, bukan sebagai substring.

  Kursor halaman yang diterbitkan tanpa header ini tidak valid jika digunakan bersama header tersebut, jadi mulailah lagi dari halaman pertama saat Anda mulai menggunakannya. Pada endpoint memory store, `agent-memory-2026-07-22` menggantikan `managed-agents-2026-04-01`, dan mengirim keduanya sekaligus mengembalikan error `400`. Mulai 22 Juli 2026, header `managed-agents-2026-04-01` juga akan menerapkan perilaku pencantuman yang sama. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).

* "Software development kit" (kit pengembangan perangkat lunak), atau SDK, untuk Python (0.116.0), TypeScript (0.110.0), Go (1.56.0), Java (2.48.0), Ruby (1.55.0), PHP (0.36.0), dan C# (12.35.0), serta "command-line interface" (antarmuka baris perintah), atau CLI (1.16.0), kini mengirim `agent-memory-2026-07-22` pada semua panggilan memory store, menggantikan `managed-agents-2026-04-01`. Jika kode Anda meneruskan `betas` secara eksplisit pada panggilan memory store, ganti `managed-agents-2026-04-01` dengan `agent-memory-2026-07-22` di sana, alih-alih menambahkan nilai kedua.

### 1 Juli 2026

* Kami telah memulihkan akses ke Claude Fable 5 dan Claude Mythos 5. Lihat [pernyataan kami](https://www.anthropic.com/news/redeploying-fable-5) untuk informasi lebih lanjut.

### 30 Juni 2026

* Kami telah meluncurkan **Claude Sonnet 5** (`claude-sonnet-5`), generasi berikutnya dari keluarga model Sonnet kami, dengan harga perkenalan $2 / $10 per MTok (ditetapkan sebagai harga standar pada 10 Agustus 2026). Claude Sonnet 5 mendukung [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows), maksimum 128k token output, serta alat dan fitur platform yang sama dengan Claude Sonnet 4.6. Pengecualiannya adalah [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), yang tidak tersedia di Claude Sonnet 5.

  Ada tiga perubahan perilaku yang perlu diperhatikan saat migrasi:

  * ["Adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) kini aktif secara default.
  * "Extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) telah dihapus dan mengembalikan error 400. Fitur ini sudah berstatus deprecated (tidak digunakan lagi) di Sonnet 4.6.
  * Menetapkan "sampling parameters" (parameter sampling) (`temperature`, `top_p`, `top_k`) ke nilai non-default mengembalikan error 400.

  Claude Sonnet 5 juga menggunakan "tokenizer" (pemecah token) baru yang menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Besar peningkatannya bergantung pada konten dan karakteristik beban kerja. Lihat [Yang baru di Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5) untuk detail dan panduan migrasi. Untuk perbedaan perilaku dan pola prompting khusus model ini, lihat [Prompting Claude Sonnet 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5).

* Stream event sesi Claude Managed Agents kini mendukung [delta event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas). Aktifkan fitur ini dengan parameter kueri `event_deltas[]` pada `GET /v1/sessions/{session_id}/events/stream`. Event `event_start` dan `event_delta` menampilkan pratinjau teks pesan agen selagi dihasilkan, sebelum event `agent.message` yang lengkap tiba.

* [Pencantuman sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#listing-sessions) untuk Claude Managed Agents kini mendukung "backward pagination" (paginasi mundur). `GET /v1/sessions` mengembalikan kursor `prev_page` bersama `next_page`. Teruskan kursor tersebut sebagai parameter `page` untuk kembali ke halaman sebelumnya. Lihat [Paginasi](https://platform.claude.com/docs/id/api/overview#pagination).

* Saat membuat sesi Claude Managed Agents, Anda kini dapat [menimpa konfigurasi agen untuk sesi tersebut](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session). Teruskan `agent` dengan `type: "agent_with_overrides"` untuk mengganti model, "system prompt" (prompt sistem), alat, skill, atau server "Model Context Protocol", yaitu MCP, khusus untuk satu sesi. Konfigurasi agen itu sendiri tidak berubah.

* Vault Claude Managed Agents kini mendukung pengaturan `injection_location` pada [kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential) (tab Environment variable). Pengaturan ini menentukan di mana nilai kredensial disisipkan saat egress: ke header permintaan keluar agen, ke body permintaan, atau keduanya.

* Webhook untuk Claude Managed Agents kini mencakup siklus hidup agen, deployment, dan deployment run. Anda dapat merespons versi agen yang baru dipublikasikan, deployment yang dijeda, atau run terjadwal yang gagal tanpa polling. Lihat tab Agent events, Deployment events, dan Deployment run events di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types).

### 29 Juni 2026

* Kami telah menghapus [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.6. Permintaan ke `claude-opus-4-6` dengan `speed: "fast"` tidak lagi dijalankan dengan kecepatan tinggi atau harga premium. Permintaan tersebut kini berjalan pada kecepatan standar, ditagih dengan tarif standar, dan tidak mengembalikan error. Field `usage.speed` pada respons menunjukkan kecepatan yang digunakan. Untuk terus menggunakan fast mode, migrasikan ke [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 26 Juni 2026

* Kami telah menaikkan ["rate limits" (batas laju)](https://platform.claude.com/docs/id/api/rate-limits) di seluruh Claude API. Batas laju Claude Sonnet dan Claude Haiku kini setara dengan Claude Opus di setiap tingkat penggunaan. Tingkat penggunaan juga telah disederhanakan menjadi tiga: Start, Build, dan Scale. Sebagian besar organisasi naik ke tingkat yang lebih tinggi, tidak ada organisasi yang mendapat batas lebih rendah dari sebelumnya, dan Anda tidak perlu melakukan tindakan apa pun. Anda dapat melihat tingkat dan batas Anda saat ini di [Claude Console](https://platform.claude.com/settings/limits).

### 25 Juni 2026

* Kami telah menandai [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.7 sebagai deprecated (tidak digunakan lagi), dan fitur ini akan dihapus pada 24 Juli 2026. Setelah dihapus, permintaan ke `claude-opus-4-7` dengan `speed: "fast"` akan mengembalikan error. Migrasikan ke fast mode untuk Claude Opus 4.8. Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 22 Juni 2026

* **MCP tunnels** (pratinjau riset): API manajemen telah dipindahkan dari `/v1/organizations/tunnels` di Admin API ke `/v1/tunnels` di Claude API. Antarmuka baru ini menggunakan header `anthropic-beta: mcp-tunnels-2026-06-22` dan scope `workspace:manage_tunnels` dari "Workload Identity Federation", atau WIF. Antarmuka lama tetap tersedia selama masa migrasi. Lihat [Referensi Tunnels API](https://platform.claude.com/docs/id/api/beta/tunnels).

### 18 Juni 2026

* SDK Python, TypeScript, Go, Java, Ruby, PHP, dan C# kini mendukung `code_execution_20260120`. Versi [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) ini menambahkan persistensi status "read-eval-print loop" (loop baca-evaluasi-cetak), atau REPL, dan merupakan versi minimum untuk ["programmatic tool calling" (pemanggilan alat terprogram)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling). Untuk menggunakannya, tetapkan `type` alat ke `code_execution_20260120`. Header beta tidak diperlukan. Versi ini tersedia di Claude Fable 5, Claude Mythos 5, Claude Opus 4.5 dan yang lebih baru, serta Claude Sonnet 4.5 dan yang lebih baru. Lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#compatibility) pada alat eksekusi kode.

### 15 Juni 2026

* Kami telah menghentikan model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`). Semua permintaan ke model-model ini di Claude API kini akan mengembalikan error. Kami merekomendasikan untuk beralih ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Opus 4.8](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Peneliti dapat mengajukan akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 11 Juni 2026

* [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) kini mendukung `code_execution_20260521`. Versi ini mencantumkan batas waktu eksekusi 90 detik per sel dalam deskripsi alat, sehingga Claude dapat memperhitungkan waktu untuk sel yang berjalan lama. Header beta tidak diperlukan.
* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [alat pengambilan web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) kini mendukung `web_search_20260318` dan `web_fetch_20260318`. Versi ini menambahkan parameter `response_inclusion` untuk menghapus blok hasil yang sudah digunakan dari respons API dalam alur kerja agentik. Header beta tidak diperlukan.

### 10 Juni 2026

* Endpoint `GET /v1/environments/{id}/work`, yang mencantumkan pekerjaan tertunda untuk [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Tindakan "Identity and Access Management" (manajemen identitas dan akses), atau IAM, untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) untuk tindakan `GetEnvironment` yang memberikan otorisasi ke endpoint ini.

### 9 Juni 2026

* Kami telah meluncurkan **Claude Fable 5** (`claude-fable-5`), model paling mumpuni kami yang tersedia untuk semua pelanggan, bersama **Claude Mythos 5** (`claude-mythos-5`) untuk peserta Project Glasswing. Kedua model mendukung [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, maksimum 128k token output, dan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) untuk kapabilitas, perubahan API, dan ketersediaan.
* Claude Fable 5 dan Claude Mythos 5 menggunakan tokenizer yang diperkenalkan bersama Claude Opus 4.7. Dibandingkan model sebelum Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Besar peningkatannya bergantung pada konten dan karakteristik beban kerja. Gunakan [API penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting#token-counts-on-claude-fable-5) dengan `model: "claude-fable-5"` untuk mengukur prompt Anda dengan tokenizer baru.
* Claude Fable 5 menjalankan "safety classifiers" (pengklasifikasi keamanan) pada permintaan dan selama respons dihasilkan. Jika pengklasifikasi menolak suatu permintaan, Messages API mengembalikan `stop_reason: "refusal"`. Anda tidak ditagih untuk permintaan yang ditolak sebelum output apa pun dihasilkan. Parameter opsional `fallbacks` dapat menjalankan ulang permintaan yang ditolak pada model lain, dengan tagihan sesuai tarif model fallback tersebut. Parameter ini tersedia dalam beta di Claude API dan Claude Platform on AWS, tetapi tidak didukung di Message Batches API. Lihat [Menangani alasan berhenti](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* Field [`stop_details.category`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan kini dapat berisi `"reasoning_extraction"` di Claude Fable 5. Nilai ini dikembalikan ketika permintaan diblokir berdasarkan larangan dalam Ketentuan Layanan Anthropic terkait rekayasa balik atau penggandaan output model. Kategori `"cyber"` dan `"bio"` yang sudah ada tidak berubah. Header beta tidak diperlukan.
* Pada Claude Fable 5 dan Claude Mythos 5, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) adalah satu-satunya mode thinking. `thinking: {"type": "disabled"}` tidak didukung. Anggaran pemikiran diperpanjang manual dan "assistant prefill" (pengisian awal respons asisten) juga tidak didukung, dan keduanya mengembalikan error 400. Lihat [Migrasi dari Claude Mythos Preview ke Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/migration-guide#migrating-from-claude-mythos-preview).
* Pada Claude Fable 5 dan Claude Mythos 5, `thinking.display` bernilai default `"omitted"`, sama seperti Claude Opus 4.8, Claude Opus 4.7, dan Claude Mythos Preview. Tetapkan `display: "summarized"` untuk menerima ringkasan thinking yang mudah dibaca. "Chain of thought" (rantai pemikiran) mentah tidak pernah dikembalikan. Dalam percakapan multi-giliran pada model yang sama, kirimkan kembali blok thinking tanpa perubahan. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Claude Fable 5 memerlukan retensi data selama 30 hari dan tidak tersedia dengan "zero data retention" (retensi data nol). Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Claude Managed Agents kini mendukung [deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments), sehingga Anda dapat menjalankan sesi berdasarkan jadwal cron tanpa perlu mengelola penjadwal sendiri.
* Vault Claude Managed Agents kini mendukung [kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential). Dengan fitur ini, Anda dapat menyisipkan secret secara aman ke sandbox agen untuk CLI, SDK, dan layanan lain yang melakukan autentikasi melalui variabel lingkungan.
* [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) dari [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) (`GET /v1/compliance/activities`) kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Tindakan IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#compliance) untuk tindakan `ListComplianceActivities` yang memberikan otorisasi ke endpoint ini.
* Event webhook `session.thread_*` kini menyertakan field `session_thread_id` yang mengidentifikasi thread multiagen pemicu event tersebut.
* Kami telah merilis [paket Swift](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models) dalam beta yang menambahkan Claude sebagai `LanguageModel` sisi server dalam framework Foundation Models milik Apple. Anda dapat memanggil Claude melalui API `LanguageModelSession` yang sama dengan model on-device Apple di iOS 27, macOS 27, visionOS 27, dan watchOS 27 (beta).

### 5 Juni 2026

* Kami mengumumkan bahwa model Claude Opus 4.1 (`claude-opus-4-1-20250805`) kini berstatus deprecated, dan model ini dijadwalkan dihentikan di Claude API pada 5 Agustus 2026. Kami merekomendasikan migrasi ke [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Deprecation model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 2 Juni 2026

* [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) kini mendukung parameter `max_tokens` untuk membatasi output model advisor per panggilan. Ini mengurangi "latency" (latensi) dan biaya token output untuk beban kerja yang tidak memerlukan respons advisor secara penuh. Tetapkan `tools[].max_tokens` pada definisi alat advisor. Lihat [Membatasi output advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#capping-advisor-output).
* Di Claude API, Anda tidak lagi ditagih untuk permintaan yang mengembalikan `stop_reason: "refusal"` jika Claude belum menghasilkan output apa pun. Lihat [Penolakan saat streaming](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) untuk cara mendeteksi dan menangani penolakan.

### 29 Mei 2026

* [Webhook](https://platform.claude.com/docs/id/managed-agents/webhooks), [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), dan [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) untuk Claude Managed Agents kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Tindakan IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) untuk tindakan IAM baru dan managed policy `AnthropicSelfHostedEnvironmentAccess`.

### 28 Mei 2026

* Kami telah meluncurkan **Claude Opus 4.8** (claude-opus-4-8), model kami yang paling mumpuni. Claude Opus 4.8 mendukung [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry. Model ini juga mendukung maksimum 128k token output, serta alat dan fitur platform yang sama dengan Claude Opus 4.7. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) untuk pengaturan dasar, fitur, dan panduan migrasi.
* Kami telah meluncurkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Pada Claude Opus 4.8, Anda dapat mengirim pesan `role: "system"` setelah giliran pengguna dalam array `messages`, sesuai [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations). Dengan begitu, prompt yang sudah di-cache tetap dapat digunakan meskipun instruksi berubah selama sesi yang berjalan lama. Header beta tidak diperlukan.
* Field [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan kini didokumentasikan secara publik. Field ini mengembalikan `category` (`cyber`, `bio`, atau `null`) dan `explanation` yang mudah dibaca, sehingga aplikasi Anda dapat menangani setiap jenis penolakan dengan langkah lanjutan yang sesuai. Header beta tidak diperlukan.
* Pada Claude Opus 4.8, [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) bernilai default `high` di semua antarmuka, termasuk Claude Code dan Messages API.
* Pada Claude Opus 4.8, panjang prompt minimum yang dapat di-cache untuk [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) adalah 1.024 token, lebih rendah daripada di Claude Opus 4.7.
* Dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) diaktifkan, Claude Opus 4.8 hanya melakukan penalaran ketika suatu giliran memerlukannya. Hasilnya, token thinking yang terbuang lebih sedikit dibandingkan Claude Opus 4.7 pada tingkat effort yang sama.
* Claude Opus 4.8 mendukung [input gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga 2576 piksel pada sisi terpanjang), sama seperti Claude Opus 4.7.
* [Anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) kini mendukung Claude Opus 4.8.
* [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) kini mendukung Claude Opus 4.8.
* ["Computer use" (penggunaan komputer)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) kini mendukung Claude Opus 4.8.
* [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.8 tersedia sebagai pratinjau riset, khusus di Claude API.
* Menetapkan parameter sampling `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 4.8, sama seperti di Claude Opus 4.7. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) untuk detailnya.
* Di Claude Code, kami telah memperluas ketersediaan Auto mode ke lebih banyak pengguna untuk tugas yang berjalan lama. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, pengguna paket Max kini menggunakan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) secara default di Claude Opus 4.8. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, Workflows tersedia sebagai pratinjau riset, sehingga Anda dapat mendefinisikan dan menjalankan rencana agentik multilangkah. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Kami telah menandai [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.6 sebagai deprecated, dan fitur ini akan dihapus sekitar 30 hari setelah peluncuran. Migrasikan ke fast mode untuk Claude Opus 4.8 atau Claude Opus 4.7. Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).
* Untuk pembaruan claude.ai, Cowork, Claude for Microsoft 365, dan aplikasi Claude lainnya dalam rilis ini, lihat [catatan rilis untuk Claude Apps](https://support.claude.com/en/articles/12138966-release-notes).

### 27 Mei 2026

* Respons Messages API kini menyertakan [`usage.output_tokens_details.thinking_tokens`](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning), yang menunjukkan berapa banyak token output yang ditagih berasal dari pemikiran diperpanjang. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir. Header beta tidak diperlukan.

### 19 Mei 2026

* [MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) kini tersedia sebagai pratinjau riset, sehingga Anda dapat terhubung ke server MCP di jaringan privat Anda.
* Sandbox yang di-host sendiri kini tersedia untuk Claude Managed Agents sebagai alternatif dari menjalankan eksekusi alat di infrastruktur Anthropic. Lihat [Sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).
* Dengan Claude Managed Agents, Anda kini dapat memperbarui konfigurasi server MCP dan alat milik agen pada sesi yang sedang aktif.
* Dengan Claude Managed Agents, output besar dari `agent_toolset` dan alat MCP yang melebihi 100K karakter (sekitar 25K token) kini otomatis disimpan ke file di sandbox. Model menerima pratinjau yang dipotong beserta path file tersebut, lalu dapat membaca konten lengkapnya dari sana.

### 18 Mei 2026

* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) kini mengembalikan data dokumen pengajuan SEC yang lebih lengkap. Ini memudahkan agen riset keuangan, analisis laba, dan alur kerja uji tuntas untuk berlandaskan sumber primer yang disertai sitasi.

### 13 Mei 2026

* Kami telah meluncurkan [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) dalam beta publik. Teruskan `diagnostics.previous_message_id` pada permintaan Messages, dan API akan melaporkan `cache_miss_reason` yang menjelaskan di titik mana prefiks prompt yang di-cache berbeda dari giliran sebelumnya. Sertakan header beta `cache-diagnosis-2026-04-07` dalam permintaan Anda.

### 12 Mei 2026

* [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) kini mendukung Claude Opus 4.7. Tetapkan `speed: "fast"` dengan `model: "claude-opus-4-7"` dan header beta `fast-mode-2026-02-01` untuk menghasilkan token output jauh lebih cepat dengan harga premium. Harga, batas laju, dan aksesnya sama dengan fast mode Opus 4.6. Pelanggan yang tertarik dapat bergabung dengan [daftar tunggu](https://claude.com/fast-mode).

### 11 Mei 2026

* Kami telah meluncurkan **Claude Platform on AWS**, yang menghadirkan Claude API di infrastruktur yang dikelola Anthropic dan dapat diakses melalui AWS, dengan penagihan AWS dan autentikasi IAM. Anda dapat mengakses Messages API, Files API, Message Batches API, Claude Managed Agents, Agent Skills, eksekusi kode, dan "tool use" (penggunaan alat) secara lengkap melalui endpoint AWS native. Pelajari lebih lanjut di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).

### 6 Mei 2026

* [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) dan [Outcomes](https://platform.claude.com/docs/id/managed-agents/define-outcomes) kini tersedia dalam beta publik dengan header beta standar `managed-agents-2026-04-01`.
* Refresh otomatis di latar belakang untuk kredensial vault Claude Managed Agents kini didukung untuk kredensial `mcp_oauth`. Lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults).
* Webhook untuk Claude Managed Agents kini didukung. Jenis event webhook mencakup event siklus hidup sesi dan vault. Lihat [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks).
* Claude Managed Agents kini mendukung opsi pemfilteran dan pengurutan tambahan. Sesi dapat difilter berdasarkan status, sedangkan event dapat difilter berdasarkan jenis dan waktu pembuatan.
* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) untuk Claude Managed Agents kini tersedia sebagai pratinjau riset. Dream membaca memory store yang sudah ada beserta transkrip sesi sebelumnya, lalu menghasilkan memory store baru yang telah ditata ulang: duplikat digabungkan, entri usang diganti, dan wawasan baru dimunculkan. Endpoint dream hanya dapat diakses dengan header beta `dreaming-2026-04-21`. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.

### 4 Mei 2026

* Kami telah meluncurkan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Anda dapat mengautentikasi beban kerja ke Claude API menggunakan token "OpenID Connect", atau OIDC, berumur pendek dari penyedia identitas Anda sendiri, alih-alih kunci API statis berumur panjang. Penyedia yang didukung antara lain AWS IAM, Google Cloud, GitHub Actions, Kubernetes, Microsoft Entra ID, Okta, dan SPIFFE. Konfigurasikan issuer dan aturan federasi di Claude Console, dan SDK akan menangani pertukaran serta refresh token secara otomatis. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

### 30 April 2026

* Kami telah menghentikan beta jendela konteks 1M token (`context-1m-2025-08-07`) untuk Claude Sonnet 4.5 dan Claude Sonnet 4. Header beta tersebut kini tidak berpengaruh pada kedua model ini, dan permintaan yang melebihi jendela konteks standar 200k token akan mengembalikan error. Untuk menggunakan jendela konteks 1M, migrasikan ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) atau [Claude Opus 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Pada kedua model tersebut, fitur ini sudah termasuk dalam harga standar dan tidak memerlukan header beta.

### 29 April 2026

* Kami telah merilis [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill), sebuah [Agent Skill](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) open-source yang memberi Claude materi referensi terkini untuk membangun aplikasi dengan Messages API dan Claude Managed Agents dalam 8 bahasa. Skill ini sudah disertakan dalam Claude Code dan tersedia di [repositori skill Anthropic](https://github.com/anthropics/skills/tree/main/skills/claude-api).

### 24 April 2026

* Kami telah merilis [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api), yang memungkinkan administrator mengkueri batas laju yang dikonfigurasi untuk organisasi dan workspace mereka secara terprogram.

### 23 April 2026

* Memori untuk Claude Managed Agents kini tersedia dalam beta publik dengan header standar `managed-agents-2026-04-01`. Lihat [Menggunakan memori agen](https://platform.claude.com/docs/id/managed-agents/memory) untuk panduan integrasi lengkap.

### 20 April 2026

* Kami telah menghentikan model Claude Haiku 3 (`claude-3-haiku-20240307`). Semua permintaan ke model ini kini akan mengembalikan error. Kami merekomendasikan untuk beralih ke [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison).

### 16 April 2026

* Kami telah meluncurkan [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), model kami yang paling mumpuni untuk penalaran kompleks dan "agentic coding" (pengodean agentik), dengan harga yang sama seperti Opus 4.6, yaitu $5 / $25 per MTok. Lihat [Apa yang baru di Claude Opus 4.7](https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-7) untuk peningkatan kemampuan, fitur baru, dan tokenizer yang diperbarui. Opus 4.7 mencakup perubahan API yang bersifat breaking dibandingkan Opus 4.6; lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) sebelum melakukan upgrade.
* [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) kini terbuka untuk semua pelanggan Amazon Bedrock. Claude Opus 4.7 dan Claude Haiku 4.5 tersedia secara swalayan dari konsol Bedrock melalui endpoint Messages API di `/anthropic/v1/messages`, di 27 region AWS dengan endpoint global dan regional.
* Kami telah meluncurkan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) dalam versi beta di Claude Opus 4.7. Berikan Claude anggaran token yang bersifat anjuran untuk satu loop agentik penuh (pemikiran, pemanggilan alat, hasil alat, dan output), dan model akan melihat hitung mundur yang terus berjalan, lalu menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan baik seiring anggaran terpakai. Sertakan header beta `task-budgets-2026-03-13` dalam permintaan Anda.
* Claude Opus 4.7 mendukung [input gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7), yang menaikkan resolusi gambar maksimum dari 1568 menjadi 2576 piksel pada sisi terpanjang untuk kinerja yang lebih baik pada computer use, pemahaman tangkapan layar, dan analisis dokumen. Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta; gambar dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan pada model sebelumnya.
* Kami telah menambahkan level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `xhigh` di Claude Opus 4.7. `xhigh` berada di antara `high` dan `max` dan disetel untuk tugas agentik dan pengodean yang berjalan lama (lebih dari 30 menit) dengan anggaran token hingga jutaan. Tidak diperlukan header beta.

### 14 April 2026

* Kami mengumumkan penghentian (deprecation) model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`), dengan penonaktifan di Claude API dijadwalkan pada 15 Juni 2026. Kami menyarankan untuk bermigrasi masing-masing ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 9 April 2026

* Kami telah meluncurkan [advisor tool](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) dalam beta publik. Pasangkan model eksekutor yang lebih cepat dengan model penasihat berkecerdasan lebih tinggi yang memberikan panduan strategis di tengah proses generasi, sehingga beban kerja agentik jangka panjang mendekati kualitas model penasihat yang bekerja sendiri, sementara sebagian besar generasi token terjadi dengan tarif model eksekutor. Sertakan header beta `advisor-tool-2026-03-01` dalam permintaan Anda.

### 8 April 2026

* Kami telah meluncurkan **Claude Managed Agents** dalam beta publik, sebuah harness agen yang dikelola sepenuhnya untuk menjalankan Claude sebagai agen otonom dengan sandboxing yang aman, alat bawaan, dan streaming server-sent event. Buat agen, konfigurasikan container, dan jalankan sesi melalui API. Semua endpoint memerlukan header beta `managed-agents-2026-04-01`. Pelajari lebih lanjut di [Ikhtisar Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).
* Kami telah meluncurkan **`ant` CLI**, klien baris perintah untuk Claude API yang memungkinkan interaksi lebih cepat dengan Claude API, integrasi native dengan Claude Code, dan pembuatan versi sumber daya API dalam file YAML. Pelajari lebih lanjut di [panduan memulai cepat CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart).

### 7 April 2026

* Kami mengumumkan bahwa [Claude Mythos Preview](https://anthropic.com/glasswing) tersedia sebagai pratinjau riset terbatas untuk pekerjaan keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya melalui undangan.
* [Messages API](https://platform.claude.com/docs/id/api/messages) kini tersedia di Amazon Bedrock sebagai pratinjau riset. Endpoint baru Claude in Amazon Bedrock di `/anthropic/v1/messages` menggunakan bentuk permintaan yang sama dengan Claude API pihak pertama dan berjalan di infrastruktur yang dikelola AWS tanpa akses operator. Tersedia di `us-east-1`; hubungi account executive Anthropic Anda untuk meminta akses. Pelajari lebih lanjut di [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock).

### 30 Maret 2026

* Kami telah menaikkan batas `max_tokens` menjadi 300k di [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) untuk Claude Opus 4.6 dan Sonnet 4.6. Sertakan header beta `output-300k-2026-03-24` untuk menghasilkan output satu giliran yang lebih panjang untuk konten panjang, data terstruktur, dan tugas pembuatan kode berskala besar.
* Kami akan menghentikan beta "context window" (jendela konteks) 1M token untuk Claude Sonnet 4.5 dan Claude Sonnet 4 pada **30 April 2026**. Setelah tanggal tersebut, header beta `context-1m-2025-08-07` tidak akan berpengaruh pada model-model ini, dan permintaan yang melebihi jendela konteks standar 200k token akan mengembalikan error. Untuk terus menggunakan jendela konteks 1M, bermigrasilah ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) atau [Claude Opus 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison), yang mendukung jendela konteks 1M token penuh dengan harga standar tanpa memerlukan header beta.

### 18 Maret 2026

* Kami telah menambahkan field kemampuan model ke [Models API](https://platform.claude.com/docs/id/api/models/list). `GET /v1/models` dan `GET /v1/models/{model_id}` kini mengembalikan `max_input_tokens`, `max_tokens`, dan objek `capabilities`. Lakukan kueri ke API untuk mengetahui apa yang didukung oleh setiap model.

### 16 Maret 2026

* Kami telah meluncurkan field `display` untuk "extended thinking" (pemikiran diperpanjang), yang memungkinkan Anda menghilangkan konten pemikiran dari respons untuk streaming yang lebih cepat. Atur `thinking.display: "omitted"` untuk menerima blok pemikiran dengan field `thinking` yang kosong dan `signature` yang tetap dipertahankan untuk kesinambungan multi-giliran. Penagihan tidak berubah. Pelajari lebih lanjut di [Mengontrol tampilan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

### 13 Maret 2026

* [Jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) telah keluar dari beta untuk Claude Opus 4.6 dan Sonnet 4.6, dengan harga standar. Permintaan di atas 200k token berfungsi secara otomatis untuk model-model ini tanpa memerlukan header beta. Jendela konteks 1M token tetap dalam beta untuk Claude Sonnet 4.5 dan Sonnet 4.
* Kami telah menghapus "rate limit" (batas laju) khusus 1M untuk semua model yang didukung. Batas akun standar Anda kini berlaku di setiap panjang konteks.
* Kami telah menaikkan batas media dari 100 menjadi 600 gambar atau halaman PDF per permintaan saat menggunakan jendela konteks 1M token.

### 19 Februari 2026

* Kami telah meluncurkan **caching otomatis** untuk Messages API. Tambahkan satu field `cache_control` ke body permintaan Anda dan sistem akan secara otomatis melakukan cache pada blok terakhir yang dapat di-cache, serta memajukan titik cache seiring bertambahnya percakapan. Tidak perlu mengelola breakpoint secara manual. Berfungsi bersama kontrol cache tingkat blok yang sudah ada untuk optimasi yang lebih terperinci. Tersedia di Claude API dan Microsoft Foundry (pratinjau). Pelajari lebih lanjut di ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching).
* Kami telah menonaktifkan model Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) dan model Claude Haiku 3.5 (`claude-3-5-haiku-20241022`). Semua permintaan ke Claude Sonnet 3.7 kini akan mengembalikan error. Permintaan ke Claude Haiku 3.5 di Claude API kini akan mengembalikan error; model ini tetap tersedia di Amazon Bedrock dan Google Cloud. Kami menyarankan untuk melakukan upgrade masing-masing ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).
* Kami mengumumkan penghentian model Claude Haiku 3 (`claude-3-haiku-20240307`), dengan penonaktifan dijadwalkan pada 20 April 2026. Kami menyarankan untuk bermigrasi ke [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 17 Februari 2026

* Kami telah meluncurkan [Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6), model seimbang terbaru kami yang menggabungkan kecepatan dan kecerdasan untuk tugas sehari-hari. Sonnet 4.6 memberikan kinerja pencarian agentik yang lebih baik sambil mengonsumsi lebih sedikit token. Sonnet 4.6 mendukung [pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) dan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (beta). Lihat [Model & Harga](https://platform.claude.com/docs/id/models/overview) untuk detailnya.
* [Eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) API kini **gratis saat digunakan bersama web search atau web fetch**. Eksekusi kode dalam sandbox meningkatkan kemampuan model dan efisiensi token. Lihat [detail harga](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk penggunaan mandiri.
* [Alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) tersedia tanpa memerlukan header beta. Web search dan web fetch kini mendukung [pemfilteran dinamis](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering), yang menggunakan eksekusi kode untuk memfilter hasil sebelum mencapai jendela konteks demi kinerja yang lebih baik dan biaya token yang lebih rendah.
* [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), [alat tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), [contoh "tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples), dan [alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool) tidak lagi memerlukan header beta.

### 7 Februari 2026

* Kami telah meluncurkan [mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) dalam pratinjau riset untuk Opus 4.6, yang memberikan generasi token output yang jauh lebih cepat melalui parameter `speed`. Mode cepat hingga 2,5x lebih cepat dengan harga premium. Pelanggan yang tertarik dapat bergabung dengan [daftar tunggu](https://claude.com/fast-mode).

### 5 Februari 2026

* Kami telah meluncurkan [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), model kami yang paling cerdas untuk tugas agentik yang kompleks dan pekerjaan jangka panjang. Opus 4.6 merekomendasikan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) (`thinking: {type: "adaptive"}`); pemikiran manual (`type: "enabled"` dengan `budget_tokens`) sudah tidak digunakan lagi (deprecated). Opus 4.6 tidak mendukung prefilling pesan asisten. Pelajari lebih lanjut di [Apa yang baru di Claude 4.6](https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-6).
* [Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) tidak lagi memerlukan header beta dan kini mendukung Claude Opus 4.6. Effort menggantikan `budget_tokens` untuk mengontrol kedalaman pemikiran pada model-model baru.
* Kami telah meluncurkan [compaction API](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold) dalam beta, yang menyediakan peringkasan konteks di sisi server untuk percakapan yang secara efektif tanpa batas. Tersedia di Opus 4.6.
* Kami telah memperkenalkan [kontrol residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency), yang memungkinkan Anda menentukan lokasi inferensi model dijalankan dengan parameter `inference_geo`. Inferensi khusus AS tersedia dengan harga 1,1x untuk model yang dirilis setelah 1 Februari 2026.
* [Jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) kini tersedia dalam beta untuk Claude Opus 4.6, selain Sonnet 4.5 dan Sonnet 4. [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing) berlaku untuk permintaan yang melebihi 200k token input.
* [Streaming alat terperinci](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) tidak lagi memerlukan header beta di model atau platform mana pun.

### 29 Januari 2026

* [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) telah keluar dari beta di Claude API untuk Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Rilis ini mencakup dukungan skema yang diperluas, latensi kompilasi grammar yang lebih baik, dan jalur integrasi yang disederhanakan tanpa memerlukan header beta. Parameter `output_format` telah dipindahkan ke `output_config.format`. Pengguna beta yang sudah ada dapat terus menggunakan header beta selama masa transisi. Output terstruktur tetap dalam beta publik di Amazon Bedrock dan Microsoft Foundry.

### 12 Januari 2026

* `console.anthropic.com` kini dialihkan ke `platform.claude.com`. Claude Console telah pindah ke rumah barunya sebagai bagian dari konsolidasi merek Claude kami. Bookmark dan tautan yang sudah ada akan tetap berfungsi melalui pengalihan otomatis. Untuk detail lebih lanjut, lihat [pengumuman 16 September 2025](https://platform.claude.com/docs/id/release-notes/overview#september-16-2025).

### 5 Januari 2026

* Kami telah menonaktifkan model Claude Opus 3 (`claude-3-opus-20240229`). Semua permintaan ke model ini kini akan mengembalikan error. Kami menyarankan untuk melakukan upgrade ke [Claude Opus 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison), yang menawarkan kecerdasan yang jauh lebih baik dengan sepertiga biaya. Peneliti dapat meminta akses berkelanjutan ke Claude Opus 3 di API melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 19 Desember 2025

* Kami mengumumkan penghentian model Claude Haiku 3.5. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 4 Desember 2025

* [Output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) kini mendukung Claude Haiku 4.5.

### 24 November 2025

* Kami telah meluncurkan [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5), model kami yang paling cerdas yang menggabungkan kemampuan maksimum dengan kinerja praktis. Ideal untuk tugas khusus yang kompleks, rekayasa perangkat lunak profesional, dan agen tingkat lanjut. Menghadirkan peningkatan signifikan dalam vision, pengodean, dan computer use dengan harga yang lebih terjangkau dibandingkan model Opus sebelumnya. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).
* Kami telah meluncurkan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dalam beta publik, yang memungkinkan Claude memanggil alat dari dalam eksekusi kode untuk mengurangi latensi dan penggunaan token dalam alur kerja multi-alat.
* Kami telah meluncurkan [alat tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) dalam beta publik, yang memungkinkan Claude menemukan dan memuat alat secara dinamis sesuai kebutuhan dari katalog alat yang besar.
* Kami telah meluncurkan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) dalam beta publik untuk Claude Opus 4.5, yang memungkinkan Anda mengontrol penggunaan token dengan menyeimbangkan antara ketelitian respons dan efisiensi.
* Kami telah menambahkan [pemadatan sisi klien](https://platform.claude.com/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) ke SDK Python dan TypeScript kami, yang secara otomatis mengelola konteks percakapan melalui peringkasan saat menggunakan `tool_runner`.

### 21 November 2025

* Blok konten hasil pencarian kini tersedia di Amazon Bedrock tanpa memerlukan header beta. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results).

### 19 November 2025

* Kami telah meluncurkan **platform dokumentasi baru** di [platform.claude.com/docs](https://platform.claude.com/docs). Dokumentasi kami kini berada berdampingan dengan Claude Console, memberikan pengalaman developer yang terpadu. Situs dokumentasi sebelumnya di docs.claude.com akan dialihkan ke lokasi baru.

### 18 November 2025

* Kami telah meluncurkan **Claude in Microsoft Foundry**, yang menghadirkan model Claude kepada pelanggan Azure dengan penagihan Azure dan autentikasi OAuth. Akses Messages API secara lengkap termasuk pemikiran diperpanjang, caching prompt (5 menit dan 1 jam), dukungan PDF, Files API, Agent Skills, dan penggunaan alat. Pelajari lebih lanjut di [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

### 14 November 2025

* Kami telah meluncurkan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) dalam beta publik, yang memberikan jaminan kesesuaian skema untuk respons Claude. Gunakan output JSON untuk respons data terstruktur atau penggunaan alat yang ketat (strict) untuk input alat yang tervalidasi. Tersedia untuk Claude Sonnet 4.5 dan Claude Opus 4.1. Untuk mengaktifkannya, gunakan header beta `structured-outputs-2025-11-13`.

### 28 Oktober 2025

* Kami mengumumkan penghentian model Claude Sonnet 3.7. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).
* Kami telah menonaktifkan model-model Claude Sonnet 3.5. Semua permintaan ke model-model ini kini akan mengembalikan error.
* Kami telah memperluas pengeditan konteks dengan pembersihan blok pemikiran (`clear_thinking_20251015`), yang memungkinkan pengelolaan blok pemikiran secara otomatis. Pelajari lebih lanjut di [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing).

### 16 Oktober 2025

* Kami telah meluncurkan [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (beta `skills-2025-10-02`), cara baru untuk memperluas kemampuan Claude. Skills adalah folder terorganisir berisi instruksi, skrip, dan sumber daya yang dimuat Claude secara dinamis untuk melakukan tugas-tugas khusus. Rilis awal mencakup:

  * **Skills yang dikelola Anthropic**: Skills siap pakai untuk bekerja dengan file PowerPoint (.pptx), Excel (.xlsx), Word (.docx), dan PDF
  * **Skills kustom**: Unggah Skills Anda sendiri melalui Skills API (endpoint `/v1/skills`) untuk mengemas keahlian domain dan alur kerja organisasi
  * Skills memerlukan [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan
  * Pelajari lebih lanjut di [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan [referensi API](https://platform.claude.com/docs/id/api/skills/create)

### 15 Oktober 2025

* Kami telah meluncurkan [Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5), model Haiku kami yang tercepat dan paling cerdas dengan kinerja yang mendekati model terdepan. Ideal untuk aplikasi real-time, pemrosesan bervolume tinggi, dan deployment yang sensitif terhadap biaya yang memerlukan penalaran yang kuat. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

### 29 September 2025

* Kami telah meluncurkan [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), model terbaik kami untuk agen kompleks dan pengodean, dengan kecerdasan tertinggi di sebagian besar tugas. Pelajari lebih lanjut di [ikhtisar model](https://platform.claude.com/docs/id/models/overview).
* Kami telah memperkenalkan [harga endpoint global](https://platform.claude.com/docs/id/about-claude/pricing#cloud-platform-pricing) untuk Amazon Bedrock dan Vertex AI. Harga Claude API (1P) tidak terpengaruh.
* Kami telah memperkenalkan alasan berhenti (stop reason) baru `model_context_window_exceeded` yang memungkinkan Anda meminta token maksimum yang memungkinkan tanpa menghitung ukuran input. Pelajari lebih lanjut di [Menangani alasan berhenti](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* Kami telah meluncurkan alat memori dalam beta, yang memungkinkan Claude menyimpan dan merujuk informasi lintas percakapan. Pelajari lebih lanjut di [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool).
* Kami telah meluncurkan pengeditan konteks dalam beta, yang menyediakan strategi untuk mengelola konteks percakapan secara otomatis. Rilis awal mendukung pembersihan hasil dan pemanggilan alat yang lebih lama saat mendekati batas token. Pelajari lebih lanjut di [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing).

### 17 September 2025

* Kami telah meluncurkan tool helper dalam beta untuk SDK Python dan TypeScript, yang menyederhanakan pembuatan dan eksekusi alat dengan validasi input yang type-safe serta tool runner untuk penanganan alat secara otomatis dalam percakapan. Untuk detailnya, lihat dokumentasi untuk [SDK Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md) dan [SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers).

### 16 September 2025

* Kami telah menyatukan penawaran developer kami di bawah merek Claude. Anda akan melihat penamaan dan URL yang diperbarui di seluruh platform dan dokumentasi kami, tetapi **antarmuka developer kami akan tetap sama**. Berikut beberapa perubahan penting:

  * Claude Console ([console.anthropic.com](https://console.anthropic.com)) → Claude Console ([platform.claude.com](https://platform.claude.com)). Konsol akan tersedia di kedua URL hingga 12 Januari 2026. Setelah tanggal tersebut, [console.anthropic.com](https://console.anthropic.com) akan secara otomatis dialihkan ke [platform.claude.com](https://platform.claude.com).
  * Anthropic Docs ([docs.anthropic.com](https://docs.anthropic.com)) → Claude Docs ([docs.claude.com](https://docs.claude.com))
  * Anthropic Help Center ([support.anthropic.com](https://support.anthropic.com)) → Claude Help Center ([support.claude.com](https://support.claude.com))
  * Endpoint API, header, variabel lingkungan, dan SDK tetap sama. Integrasi Anda yang sudah ada akan terus berfungsi tanpa perubahan apa pun.

### 10 September 2025

* Kami telah meluncurkan alat web fetch dalam beta, yang memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan. Pelajari lebih lanjut di [Alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool).
* Kami telah meluncurkan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api), yang memungkinkan organisasi mengakses secara terprogram metrik penggunaan harian teragregasi untuk Claude Code, termasuk metrik produktivitas, statistik penggunaan alat, dan data biaya.

### 8 September 2025

* Kami meluncurkan versi beta dari [SDK C#](https://github.com/anthropics/anthropic-sdk-csharp).

### 5 September 2025

* Kami telah meluncurkan [grafik batas laju](https://platform.claude.com/docs/id/api/rate-limits#monitoring-your-rate-limits-in-the-console) di halaman [Usage](https://console.anthropic.com/settings/usage) Console, yang memungkinkan Anda memantau penggunaan batas laju API dan tingkat caching Anda dari waktu ke waktu.

### 3 September 2025

* Kami telah meluncurkan dukungan untuk dokumen yang dapat dikutip dalam hasil alat sisi klien. Pelajari lebih lanjut di [Menangani pemanggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls).

### 2 September 2025

* Kami telah meluncurkan v2 dari [Alat Eksekusi Kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, menggantikan alat asli yang hanya mendukung Python dengan eksekusi perintah Bash dan kemampuan manipulasi file secara langsung, termasuk menulis kode dalam bahasa lain.

### 27 Agustus 2025

* Kami meluncurkan versi beta dari [SDK PHP](https://github.com/anthropics/anthropic-sdk-php).

### 26 Agustus 2025

* Kami telah meningkatkan batas laju pada [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) untuk Claude Sonnet 4 di Claude API.
* Jendela konteks 1M token kini tersedia di Vertex AI. Untuk informasi lebih lanjut, lihat [Claude di Vertex AI](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai).

### 19 Agustus 2025

* ID permintaan kini disertakan langsung dalam body respons error bersama header `request-id` yang sudah ada. Pelajari lebih lanjut di [Error](https://platform.claude.com/docs/id/api/errors#error-shapes).

### 18 Agustus 2025

* Kami telah merilis [Usage & Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api), yang memungkinkan administrator memantau data penggunaan dan biaya organisasi mereka secara terprogram.
* Kami telah menambahkan endpoint baru ke Admin API untuk mengambil informasi organisasi. Untuk detailnya, lihat [referensi Admin API Organization Info](https://platform.claude.com/docs/id/api/beta/organization/retrieve).

### 13 Agustus 2025

* Kami mengumumkan penghentian model-model Claude Sonnet 3.5 (`claude-3-5-sonnet-20240620` dan `claude-3-5-sonnet-20241022`). Model-model ini akan dinonaktifkan pada 28 Oktober 2025. Kami menyarankan untuk bermigrasi ke Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) untuk kinerja dan kemampuan yang lebih baik. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).
* Durasi cache 1 jam untuk caching prompt tidak lagi memerlukan header beta. Pelajari lebih lanjut di [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration).

### 12 Agustus 2025

* Kami telah meluncurkan dukungan beta untuk [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) di Claude Sonnet 4 pada Claude API dan Amazon Bedrock.

### 11 Agustus 2025

* Beberapa pelanggan mungkin mengalami [error](https://platform.claude.com/docs/id/api/errors) 429 (`rate_limit_error`) setelah peningkatan tajam dalam penggunaan API karena batas akselerasi pada API. Sebelumnya, error 529 (`overloaded_error`) akan terjadi dalam skenario serupa.

### 8 Agustus 2025

* Blok konten hasil pencarian telah keluar dari beta di Claude API dan Vertex AI. Fitur ini memungkinkan kutipan alami untuk aplikasi RAG dengan atribusi sumber yang tepat. Header beta `search-results-2025-06-09` tidak lagi diperlukan. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results).

### 5 Agustus 2025

* Kami telah meluncurkan [Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1), pembaruan inkremental untuk Claude Opus 4 dengan kemampuan yang ditingkatkan dan peningkatan kinerja.\* Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

*\*Opus 4.1 tidak mengizinkan parameter `temperature` dan `top_p` ditentukan secara bersamaan. Harap gunakan salah satu saja.*

### 28 Juli 2025

* Kami telah merilis `text_editor_20250728`, alat editor teks yang diperbarui yang memperbaiki beberapa masalah dari versi sebelumnya dan menambahkan parameter opsional `max_characters` yang memungkinkan Anda mengontrol panjang pemotongan saat melihat file berukuran besar.

### 24 Juli 2025

* Kami telah meningkatkan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk Claude Opus 4 di Claude API untuk memberi Anda lebih banyak kapasitas dalam membangun dan melakukan scaling dengan Claude. Bagi pelanggan dengan [batas laju usage tier 1-4](https://platform.claude.com/docs/id/api/rate-limits#rate-limits), perubahan ini langsung berlaku untuk akun Anda - tidak perlu tindakan apa pun.

### 21 Juli 2025

* Kami telah menonaktifkan model Claude 2.0, Claude 2.1, dan Claude Sonnet 3. Semua permintaan ke model-model ini kini akan mengembalikan error. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 17 Juli 2025

* Kami telah meningkatkan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk Claude Sonnet 4 di Claude API untuk memberi Anda lebih banyak kapasitas dalam membangun dan melakukan scaling dengan Claude. Bagi pelanggan dengan [batas laju usage tier 1-4](https://platform.claude.com/docs/id/api/rate-limits#rate-limits), perubahan ini langsung berlaku untuk akun Anda - tidak perlu tindakan apa pun.

### 3 Juli 2025

* Kami telah meluncurkan blok konten hasil pencarian dalam beta, yang memungkinkan kutipan alami untuk aplikasi RAG. Alat kini dapat mengembalikan hasil pencarian dengan atribusi sumber yang tepat, dan Claude akan secara otomatis mengutip sumber-sumber ini dalam responsnya - menyamai kualitas kutipan web search. Hal ini menghilangkan kebutuhan akan solusi alternatif berbasis dokumen dalam aplikasi basis pengetahuan kustom. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results). Untuk mengaktifkan fitur ini, gunakan header beta `search-results-2025-06-09`.

### 30 Juni 2025

* Kami mengumumkan penghentian model Claude Opus 3. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 23 Juni 2025

* Pengguna Console dengan peran Developer kini dapat mengakses halaman [Cost](https://console.anthropic.com/settings/cost). Sebelumnya, peran Developer mengizinkan akses ke halaman [Usage](https://console.anthropic.com/settings/usage), tetapi tidak ke halaman Cost.

### 11 Juni 2025

* Kami telah meluncurkan [streaming alat terperinci](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) dalam beta publik, fitur yang memungkinkan Claude melakukan streaming parameter penggunaan alat tanpa buffering / validasi JSON. Untuk mengaktifkan streaming alat terperinci, gunakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `fine-grained-tool-streaming-2025-05-14`.

### 22 Mei 2025

* Kami telah meluncurkan [Claude Opus 4 dan Claude Sonnet 4](https://www.anthropic.com/news/claude-4), model terbaru kami dengan kemampuan pemikiran diperpanjang. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).
* Perilaku default [pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) pada model Claude 4 mengembalikan ringkasan dari proses pemikiran lengkap Claude, dengan pemikiran lengkap dienkripsi dan dikembalikan dalam field `signature` pada output blok `thinking`.
* Kami telah meluncurkan [pemikiran berselang-seling](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) dalam beta publik, fitur yang memungkinkan Claude berpikir di antara pemanggilan alat. Untuk mengaktifkan pemikiran berselang-seling, gunakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14`.
* Kami telah meluncurkan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dalam beta publik, yang memungkinkan Anda mengunggah file dan mereferensikannya di Messages API dan alat eksekusi kode.
* Kami telah meluncurkan [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, alat yang memungkinkan Claude mengeksekusi kode Python di lingkungan sandbox yang aman.
* Kami telah meluncurkan [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) dalam beta publik, fitur yang memungkinkan Anda terhubung ke server MCP jarak jauh langsung dari Messages API.
* Untuk meningkatkan kualitas jawaban dan mengurangi error alat, kami telah mengubah nilai default untuk parameter [nucleus sampling](https://en.wikipedia.org/wiki/Top-p_sampling) `top_p` di Messages API dari 0.999 menjadi 0.99 untuk semua model. Untuk membatalkan perubahan ini, atur `top_p` ke 0.999. Selain itu, saat pemikiran diperpanjang diaktifkan, Anda kini dapat mengatur `top_p` ke nilai antara 0.95 dan 1.
* [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami telah beralih dari beta ke rilis stabil pertamanya.
* Kami telah menambahkan granularitas tingkat menit dan jam ke halaman [Usage](https://console.anthropic.com/settings/usage) di Console, bersama dengan tingkat error 429 di halaman Usage.

### 21 Mei 2025

* [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby) kami telah beralih dari beta ke rilis stabil pertamanya.

### 7 Mei 2025

* Kami telah meluncurkan alat web search di API, yang memungkinkan Claude mengakses informasi terkini dari web. Pelajari lebih lanjut di [Alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool).

### 1 Mei 2025

* Kontrol cache kini harus ditentukan langsung di blok `content` induk dari `tool_result` dan `document.source`. Untuk kompatibilitas mundur, jika kontrol cache terdeteksi pada blok terakhir di `tool_result.content` atau `document.source.content`, kontrol tersebut akan secara otomatis diterapkan ke blok induk sebagai gantinya. Kontrol cache pada blok lain mana pun di dalam `tool_result.content` dan `document.source.content` akan menghasilkan error validasi.

### 9 April 2025

* Kami meluncurkan versi beta dari [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby).

### 31 Maret 2025

* [SDK Java](https://github.com/anthropics/anthropic-sdk-java) kami telah beralih dari beta ke rilis stabil pertamanya.
* Kami telah memindahkan [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami dari alpha ke beta.

### 27 Februari 2025

* Kami telah menambahkan blok sumber URL untuk gambar dan PDF di Messages API. Anda kini dapat mereferensikan gambar dan PDF secara langsung melalui URL alih-alih harus melakukan encoding base64. Pelajari lebih lanjut di [Vision](https://platform.claude.com/docs/id/build-with-claude/vision) dan [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).
* Kami telah menambahkan dukungan untuk opsi `none` pada parameter `tool_choice` di Messages API yang mencegah Claude memanggil alat apa pun. Selain itu, Anda tidak lagi diwajibkan menyediakan `tools` apa pun saat menyertakan blok `tool_use` dan `tool_result`.
* Kami telah meluncurkan endpoint API yang kompatibel dengan OpenAI, yang memungkinkan Anda menguji model Claude hanya dengan mengubah kunci API, base URL, dan nama model dalam integrasi OpenAI yang sudah ada. Lapisan kompatibilitas ini mendukung fungsionalitas inti chat completions. Pelajari lebih lanjut di [Kompatibilitas SDK OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk).

### 24 Februari 2025

* Kami telah meluncurkan [Claude Sonnet 3.7](https://www.anthropic.com/news/claude-3-7-sonnet), model kami yang paling cerdas sejauh ini. Claude Sonnet 3.7 dapat menghasilkan respons yang hampir instan atau menunjukkan pemikiran diperpanjangnya langkah demi langkah. Satu model, dua cara berpikir. Pelajari lebih lanjut tentang semua model Claude di [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

* Kami telah menambahkan dukungan vision ke Claude Haiku 3.5, yang memungkinkan model menganalisis dan memahami gambar.

* Kami telah merilis implementasi penggunaan alat yang hemat token, yang meningkatkan kinerja keseluruhan saat menggunakan alat dengan Claude. Pelajari lebih lanjut di [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

* Kami telah mengubah temperature default di [Console](https://console.anthropic.com/workbench) untuk prompt baru dari 0 menjadi 1 agar konsisten dengan temperature default di API. Prompt tersimpan yang sudah ada tidak berubah.

* Kami telah merilis versi terbaru dari alat-alat kami yang memisahkan alat text edit dan bash dari "system prompt" (prompt sistem) computer use:

  * `bash_20250124`: Fungsionalitas sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `text_editor_20250124`: Fungsionalitas sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `computer_20250124`: Alat computer use yang diperbarui dengan opsi perintah baru termasuk "hold\_key", "left\_mouse\_down", "left\_mouse\_up", "scroll", "triple\_click", dan "wait". Alat ini memerlukan header anthropic-beta "computer-use-2025-01-24". Pelajari lebih lanjut di [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

### 10 Februari 2025

* Kami telah menambahkan header respons `anthropic-organization-id` ke semua respons API. Header ini menyediakan ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan.

### 31 Januari 2025

* Kami telah memindahkan [Java SDK](https://github.com/anthropics/anthropic-sdk-java) kami dari alpha ke beta.

### 23 Januari 2025

* Kami telah meluncurkan kemampuan "citations" (kutipan) di API, yang memungkinkan Claude memberikan atribusi sumber untuk informasi. Pelajari lebih lanjut di [Kutipan](https://platform.claude.com/docs/id/build-with-claude/citations).
* Kami telah menambahkan dukungan untuk dokumen teks biasa dan dokumen konten kustom di Messages API.

### 21 Januari 2025

* Kami mengumumkan penghentian model Claude 2, Claude 2.1, dan Claude Sonnet 3. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 15 Januari 2025

* Kami telah memperbarui ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) agar lebih mudah digunakan. Sekarang, saat Anda menetapkan breakpoint cache, kami akan secara otomatis membaca dari prefiks terpanjang yang sebelumnya telah di-cache.
* Anda sekarang dapat menentukan awal respons Claude saat menggunakan alat.

### 10 Januari 2025

* Kami telah mengoptimalkan dukungan untuk [caching prompt di Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#using-prompt-caching-with-message-batches) untuk meningkatkan tingkat cache hit.

### 19 Desember 2024

* Kami telah menambahkan dukungan untuk [endpoint delete](https://platform.claude.com/docs/id/api/messages/batches/delete) di Message Batches API.

### 17 Desember 2024

Fitur-fitur berikut sekarang tersedia di Claude API tanpa header beta:

* [Models API](https://platform.claude.com/docs/id/api/models/list): Kueri model yang tersedia, validasi ID model, dan selesaikan [alias model](https://platform.claude.com/docs/id/models/overview) ke ID model kanoniknya.
* [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing): Proses batch pesan dalam jumlah besar secara asinkron dengan biaya 50% dari biaya API standar.
* [Token counting API](https://platform.claude.com/docs/id/build-with-claude/token-counting): Hitung jumlah token untuk Messages sebelum mengirimkannya ke Claude.
* [Caching Prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching): Kurangi biaya hingga 90% dan "latency" (latensi) hingga 80% dengan melakukan caching dan menggunakan kembali konten prompt.
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support): Proses PDF untuk menganalisis konten teks maupun visual di dalam dokumen.

Kami juga merilis SDK resmi baru:

* [Java SDK](https://github.com/anthropics/anthropic-sdk-java) (alpha)
* [Go SDK](https://github.com/anthropics/anthropic-sdk-go) (alpha)

### 4 Desember 2024

* Kami telah menambahkan kemampuan untuk mengelompokkan berdasarkan "API key" (kunci API) di halaman [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) pada [Developer Console](https://console.anthropic.com).
* Kami telah menambahkan dua kolom baru, **Last used at** dan **Cost**, serta kemampuan untuk mengurutkan berdasarkan kolom apa pun di halaman [API keys](https://console.anthropic.com/settings/keys) pada [Developer Console](https://console.anthropic.com).

### 21 November 2024

* Kami telah merilis [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), yang memungkinkan pengguna mengelola sumber daya organisasi mereka secara terprogram.

### 20 November 2024

* Kami telah memperbarui "rate limit" (batas laju) untuk Messages API. Kami telah mengganti batas laju token per menit dengan batas laju token input dan token output per menit yang baru. Baca selengkapnya di [Batas laju](https://platform.claude.com/docs/id/api/rate-limits).
* Kami telah menambahkan dukungan untuk ["tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) di [Workbench](https://console.anthropic.com/workbench).

### 13 November 2024

* Kami telah menambahkan dukungan PDF untuk semua model Claude Sonnet 3.5. Baca selengkapnya di [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).

### 6 November 2024

* Kami telah memensiunkan model Claude 1 dan Instant. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 4 November 2024

* [Claude Haiku 3.5](https://www.anthropic.com/claude/haiku) sekarang tersedia di Claude API sebagai model khusus teks.

### 1 November 2024

* Kami telah menambahkan dukungan PDF untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca selengkapnya di [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).
* Kami juga telah menambahkan penghitungan token, yang memungkinkan Anda menentukan jumlah total token dalam sebuah Message sebelum mengirimkannya ke Claude. Baca selengkapnya di [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

### 22 Oktober 2024

* Kami telah menambahkan alat computer use yang ditentukan oleh Anthropic ke API kami untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca selengkapnya di [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool).
* Claude Sonnet 3.5, model kami yang paling cerdas sejauh ini, baru saja mendapatkan peningkatan dan sekarang tersedia di Claude API. Baca selengkapnya di [dokumentasi Claude Sonnet](https://www.anthropic.com/claude/sonnet).

### 8 Oktober 2024

* Message Batches API sekarang tersedia dalam versi beta. Proses batch kueri dalam jumlah besar secara asinkron di Claude API dengan biaya 50% lebih rendah. Baca selengkapnya di [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing).
* Kami telah melonggarkan batasan pada urutan giliran `user`/`assistant` di Messages API kami. Pesan `user`/`assistant` yang berurutan akan digabungkan menjadi satu pesan alih-alih menghasilkan error, dan kami tidak lagi mengharuskan pesan input pertama berupa pesan `user`.
* Kami telah menghentikan paket Build dan Scale dan menggantinya dengan rangkaian fitur standar (sebelumnya disebut Build), beserta fitur tambahan yang tersedia melalui tim penjualan. Baca selengkapnya di [informasi harga API](https://claude.com/platform/api) kami.

### 3 Oktober 2024

* Kami telah menambahkan kemampuan untuk menonaktifkan penggunaan alat paralel di API. Tetapkan `disable_parallel_tool_use: true` di field `tool_choice` untuk memastikan bahwa Claude menggunakan paling banyak satu alat. Baca selengkapnya di [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use).

### 10 September 2024

* Kami telah menambahkan Workspaces ke [Developer Console](https://console.anthropic.com). Workspaces memungkinkan Anda menetapkan batas pengeluaran atau batas laju kustom, mengelompokkan kunci API, melacak penggunaan per proyek, dan mengontrol akses dengan peran pengguna. Baca selengkapnya di [postingan blog](https://www.anthropic.com/news/workspaces) kami.

### 4 September 2024

* Kami mengumumkan penghentian model Claude 1. Baca selengkapnya di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 22 Agustus 2024

* Kami telah menambahkan dukungan untuk penggunaan SDK di browser dengan mengembalikan header CORS dalam respons API. Tetapkan `dangerouslyAllowBrowser: true` saat instansiasi SDK untuk mengaktifkan fitur ini.

### 19 Agustus 2024

* Output 8.192 token pada Claude Sonnet 3.5 telah keluar dari beta dan tidak lagi memerlukan header `max-tokens-3-5-sonnet-2024-07-15`.

### 14 Agustus 2024

* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) sekarang tersedia sebagai fitur beta di Claude API. Lakukan caching dan gunakan kembali prompt untuk mengurangi latensi hingga 80% dan biaya hingga 90%.

### 15 Juli 2024

* Hasilkan output dengan panjang hingga 8.192 token dari Claude Sonnet 3.5 dengan header baru `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15`.

### 9 Juli 2024

* Buat kasus uji untuk prompt Anda secara otomatis menggunakan Claude di [Developer Console](https://console.anthropic.com).
* Bandingkan output dari berbagai prompt secara berdampingan dalam mode perbandingan output yang baru di [Developer Console](https://console.anthropic.com).

### 27 Juni 2024

* Lihat penggunaan API dan penagihan yang dirinci berdasarkan jumlah dolar, jumlah token, dan kunci API di tab [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) yang baru di [Developer Console](https://console.anthropic.com).
* Lihat batas laju API Anda saat ini di tab [Rate Limits](https://console.anthropic.com/settings/limits) yang baru di [Developer Console](https://console.anthropic.com).

### 20 Juni 2024

* [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet), model kami yang paling cerdas sejauh ini, sekarang tersedia di Claude API, Amazon Bedrock, dan Vertex AI.

### 30 Mei 2024

* [Penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) telah keluar dari beta di Claude API, Amazon Bedrock, dan Vertex AI, tanpa memerlukan header beta.

### 10 Mei 2024

* Alat pembuat prompt kami sekarang tersedia di [Developer Console](https://console.anthropic.com). Prompt Generator memudahkan Anda memandu Claude untuk menghasilkan prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda. Baca selengkapnya di [postingan blog](https://www.anthropic.com/news/prompt-generator) kami.
