---
source: platform
url: https://platform.claude.com/docs/id/release-notes/overview
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 992c83154276027ded39c5f1c58d4521b1f41efac79e9453d567e56ca82c4f88
---

---
title: Catatan rilis Claude Platform
url: https://platform.claude.com/docs/id/release-notes/overview
description: Pembaruan pada Claude Platform, termasuk Claude API, SDK klien, dan Claude Console.
---

Catatan rilis Claude Platform mencantumkan perubahan pada Claude API, SDK klien, dan Claude Console, dengan urutan terbaru lebih dulu.

<Tip>
  Untuk catatan rilis Claude Apps, lihat [Catatan rilis untuk Claude Apps di Pusat Bantuan Claude](https://support.claude.com/en/articles/12138966-release-notes).

  Untuk pembaruan Claude Code, lihat [CHANGELOG.md lengkap](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) di repositori `claude-code`.
</Tip>

### 1 September 2026

* Kami telah meluncurkan **Claude Fable 5.1** (`claude-fable-5-1`), penerus Claude Fable 5 untuk pengodean agentik yang berjalan lama, pekerjaan berbasis pengetahuan, dan riset, bersama **Claude Mythos 5.1** (`claude-mythos-5-1`) untuk peserta Project Glasswing. Kedua model mendukung ["context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, output maksimum 128k token, dan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif, dengan harga $10 / $50 USD per MTok, sama dengan Claude Fable 5, dengan pembacaan cache diturunkan menjadi $0,25 per MTok. Claude Fable 5.1 tersedia di Claude API, [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Lihat [Yang baru di Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) untuk kemampuan, perubahan API, dan panduan migrasi.
* Pembacaan cache prompt pada Claude Fable 5.1 dan Claude Mythos 5.1 berbiaya $0,25 USD per juta token: 0,025x harga input dasar, dibandingkan dengan 0,1x pada model lain. Penulisan cache tidak berubah. Lihat [Harga caching prompt](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching).
* Pada Claude Fable 5.1 dan Claude Mythos 5.1, tipe `tool_choice` `any` dan `tool` tidak didukung dan mengembalikan error 400. `auto` dan `none` tidak berubah. Untuk menjamin input alat yang sesuai skema, gunakan [strict tool use (penggunaan alat ketat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) atau [structured outputs (output terstruktur)](https://platform.claude.com/docs/id/build-with-claude/structured-outputs).
* Blok thinking yang dihasilkan oleh Claude Fable 5.1 dan Claude Mythos 5.1 hanya dipertahankan untuk model yang menghasilkannya atau model yang lebih baru: model sebelumnya tidak dapat membacanya, dan API membuang blok yang diputar ulang ke model sebelumnya. Claude Fable 5.1 menerima blok thinking dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude sebelumnya. Pada Claude Fable 5.1, API juga [memeriksa bahwa tidak ada yang berubah sebelum sebuah blok](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation): untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, memutar ulang sebuah blok setelah prompt `system`, `tools`, atau pesan sebelumnya berubah akan mengembalikan error 400. Dengan header beta `thinking-binding-controls-2026-08-01`, blok yang dibuang dilaporkan dalam field respons `input_transformations`, dan `thinking.block_binding.prefix_mismatch_behavior` memilih antara menolak dan membuang blok yang riwayatnya berubah. Lihat [Thinking yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking).
* Perubahan effort per pesan tersedia dalam beta pada Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5 di Claude API. Tambahkan pesan `role: "system"` dengan `output_config.effort` di dalam `messages` untuk mengubah effort pada giliran berikutnya sambil mempertahankan cache prompt. Sertakan header beta `mid-conversation-output-config-2026-07-01` dalam permintaan Anda. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).
* [Pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) tersedia dalam beta (header `mid-conversation-system-clear-at-2026-08-21`). Atur `clear_at: "next_user_message"` pada pesan `role: "system"` di tengah percakapan dan pesan tersebut hanya dirender untuk giliran saat ini, lalu tetap berada dalam riwayat tanpa biaya token. Pengingat per giliran tidak menumpuk dan tidak membatalkan cache prompt atau blok thinking berikutnya.
* `thinking.display` menerima nilai ketiga, `"updates"`, dalam beta (header `thinking-display-updates-2026-08-18`). Penalaran dikembalikan dengan field `thinking` kosong, seperti pada `"omitted"`, dan pembaruan progres singkat yang ditulis Claude Fable 5.1, Claude Mythos 5.1, dan Claude Fable 5 di antara pemanggilan alat dikembalikan sebagai teks, paling banyak satu blok `thinking` sebelum pemanggilan alat. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).
* Teks yang dihasilkan oleh Claude Fable 5.1 dan Claude Mythos 5.1 membawa watermark teks Anthropic, dan file gambar serta video yang didukung yang dihasilkan Claude melalui [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) membawa C2PA Content Credentials saat Anda mengambilnya melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files) di Claude API. Penandaan ini tidak memerlukan perubahan pada permintaan atau penanganan respons Anda.
* Seperti Claude Fable 5, kedua model memerlukan retensi data 30 hari dan tidak tersedia dengan zero data retention kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

### 27 Agustus 2026

* Pada Python SDK 1.2.0, TypeScript SDK 0.122.0, Go SDK 1.68.0, Java SDK 2.59.0, Ruby SDK 1.67.0, dan C# SDK 12.44.0, `client.beta.files` dan `client.beta.skills` tidak lagi mengirim header beta `files-api-2025-04-14` dan `skills-2025-10-02` serta mengembalikan bentuk yang sama dengan `client.files` dan `client.skills`. Dengan perubahan ini, `client.beta.skills.delete()` menghapus sebuah Skill beserta semua versinya, dan tipe Messages beta `BetaSkill` (referensi Skill container) diubah namanya menjadi `BetaContainerSkill`. Permintaan yang masih mengirim header beta tetap menerima bentuk beta. Lihat [Migrasi dari `files-api-2025-04-14`](https://platform.claude.com/docs/id/build-with-claude/files#migrate-from-files-api-2025-04-14) dan [Migrasi dari `skills-2025-10-02`](https://platform.claude.com/docs/id/build-with-claude/skills-guide#migrate-from-skills-2025-10-02).

- Anda kini dapat membuat **kunci personal** dan **kunci akun layanan** di Claude Console. Kunci ini bertindak sebagai Anda atau sebagai [akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts), dengan izin yang sama, dan berhenti berfungsi ketika akun yang tertaut dihapus dari organisasi. Ini memungkinkan admin organisasi melacak penggunaan setiap akun dengan lebih mudah, dan memastikan penggunaan kunci sah. Kunci API ini dapat dibatasi cakupannya ke workspace tertentu atau [berfungsi pada endpoint admin dan di seluruh workspace mana pun](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) yang dapat diakses akun tersebut. Kunci API workspace tetap didukung sebagai opsi legacy. Lihat [Kunci API](https://platform.claude.com/docs/id/manage-claude/authentication#api-keys) untuk informasi lebih lanjut.

### 26 Agustus 2026

* Endpoint sesi [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) telah keluar dari beta untuk sesi Cowork dan Claude Code. Lihat [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions).
* Endpoint sesi lokal [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini juga mengembalikan transkrip sesi Claude Science (nilai `product_surface` `claude_science`) dan sesi Claude for Microsoft 365 di Excel, PowerPoint, Word, dan Outlook (nilai `product_surface` yang diawali `office_agents`), dalam beta untuk organisasi Claude Enterprise, dengan Compliance Access Key Anda yang sudah ada dan cakupan `read:compliance_user_data`. Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).

- [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) kini tersedia di CLI `ant` dan SDK Python, TypeScript, C#, Go, Java, PHP, dan Ruby di bawah `client.beta.organization`. Cakupannya meliputi info organisasi, anggota, undangan, workspace dan anggota workspace, kunci API, batas laju, akun layanan, issuer dan aturan workload identity federation, serta kunci enkripsi yang dikelola pelanggan. Laporan penggunaan dan biaya serta endpoint manajemen pengguna dan analitik Claude Enterprise tetap hanya tersedia melalui curl. CLI dan SDK membaca kunci Admin API dari `ANTHROPIC_API_KEY` atau token OAuth `org:admin` dari `ANTHROPIC_AUTH_TOKEN`.

### 20 Agustus 2026

* Kami telah merilis **v1.0 dari [Python SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/python)**. Lapisan HTTP SDK berpindah dari `httpx` ke [httpx2](https://httpx2.pydantic.dev), sebuah fork yang terpelihara dan kompatibel secara API: bangun objek `http_client`, `Timeout`, dan transport kustom dari `httpx2` (helper `DefaultHttpxClient` tidak berubah), dan panggil `httpx2.alias_httpx()` saat startup jika Anda mengandalkan library tracing atau mocking yang mem-patch `httpx`. v1.0 memerlukan Python 3.10 atau lebih baru dan menghapus permukaan yang sudah lama deprecated, termasuk Text Completions API legacy, parameter `temperature`, `top_p`, dan `top_k` pada metode Messages, serta `compaction_control` sisi klien pada tool runner. Pada klien async, hasil `.with_raw_response` kini memerlukan `await response.parse()`, dan `AnthropicBedrock` kini memunculkan error ketika tidak ada region AWS yang dikonfigurasi alih-alih menggunakan default `us-east-1`. Lihat [panduan migrasi v1](https://github.com/anthropics/anthropic-sdk-python/blob/main/MIGRATION.md) untuk setiap perubahan dengan cuplikan sebelum-dan-sesudah.
* Toolset [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`computer_toolset_20260801` dan `browser_toolset_20260801`) kini tersedia di [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai) untuk Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, dan Claude Opus 4.8. Permintaan menggunakan entri `tools` yang sama seperti di Claude API.

### 19 Agustus 2026

* [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) telah keluar dari beta di Claude API sebagai toolset `computer_toolset_20260801`: tanpa header beta, aksi batch (beberapa aksi dalam satu giliran), `zoom` diaktifkan secara default, dan konfigurasi per anggota melalui `configs`. Versi beta sebelumnya tetap tersedia. Meng-upgrade integrasi yang sudah ada mengubah bentuk permintaan dan penanganan alat; lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).
* Kami telah meluncurkan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`), sebuah toolset klien untuk mengendalikan browser yang di-host oleh aplikasi Anda. Alat ini bekerja di dalam viewport browser alih-alih seluruh desktop, membaca halaman itu sendiri (pohon aksesibilitas, elemen, formulir, dan tabnya) serta menambahkan referensi elemen, input formulir, manajemen tab, pelaporan unduhan, dan unggah file opt-in di atas kendali screenshot-dan-klik.
* Kedua toolset tersedia untuk Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, dan Claude Opus 4.8 di Claude API.
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files) telah keluar dari beta di Claude API. Permintaan ke endpoint `/v1/files`, dan permintaan Messages API yang mereferensikan file yang diunggah, tidak lagi memerlukan header beta `files-api-2025-04-14`. Permintaan yang dikirim tanpa header menggunakan format respons saat ini: [kedaluwarsa file](https://platform.claude.com/docs/id/build-with-claude/files#file-expiration) (atur `expires_in_seconds` saat Anda mengunggah file; objek file melaporkan `expires_at`), serta [paginasi](https://platform.claude.com/docs/id/api/overview#pagination) `page` dan `next_page` ditambah filter `ids[]` saat Anda [mencantumkan file](https://platform.claude.com/docs/id/build-with-claude/files#list-files). Permintaan `/v1/files` yang masih mengirim header beta tetap berfungsi dan mengembalikan format respons sebelumnya. Untuk memindahkan integrasi yang sudah ada dari header tersebut, lihat [Migrasi dari `files-api-2025-04-14`](https://platform.claude.com/docs/id/build-with-claude/files#migrate-from-files-api-2025-04-14).
* [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan Skills API (`/v1/skills`) telah keluar dari beta di Claude API. Permintaan tidak lagi memerlukan header beta `skills-2025-10-02`, termasuk permintaan Messages API yang memuat Skills melalui parameter `container`. Permintaan yang masih mengirim header tersebut tetap berfungsi tanpa perubahan. Lihat [Menggunakan Agent Skills dengan API](https://platform.claude.com/docs/id/build-with-claude/skills-guide). Untuk memindahkan integrasi yang sudah ada dari header tersebut, lihat [Migrasi dari `skills-2025-10-02`](https://platform.claude.com/docs/id/build-with-claude/skills-guide#migrate-from-skills-2025-10-02).
* Endpoint manajemen pengguna [Admin API](https://platform.claude.com/docs/id/api/admin) untuk organisasi **Claude Enterprise** (claude.ai) (anggota, undangan, grup, dan peran kustom) telah keluar dari beta. Header `anthropic-beta: ce-user-management-2026-07-13` tidak lagi diperlukan pada permintaan grup dan peran kustom; permintaan yang masih mengirimnya diterima tanpa perubahan. Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management).
* Anda kini dapat membatasi situs mana yang dapat dijangkau oleh alat `web_search` dan `web_fetch` milik agen Claude Managed Agents. Atur `allowed_domains` atau `blocked_domains` pada entri alat tersebut dalam array `configs` `agent_toolset_20260401`; `web_fetch` juga menerima `max_content_tokens` dan `web_search` menerima `user_location`. Setiap entri `configs` diidentifikasi oleh `name`-nya dan diberi tipe oleh `type` opsional, dan permintaan yang hanya meneruskan `name`, `enabled`, dan `permission_policy` tetap berfungsi; pada SDK bertipe, entri `configs` menjadi tipe per alat. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools#restrict-web-search-and-web-fetch-domains).
* Sesi Claude Managed Agents yang berjalan di [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) kini dapat melampirkan [memory store](https://platform.claude.com/docs/id/managed-agents/memory). Worker SDK Python, TypeScript, dan Go mengunduh setiap store yang dilampirkan ke dalam sandbox pada `mount_path`-nya dan menyinkronkan perubahan agen kembali ke store. Lihat [Menggunakan memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores).
* Penampil sesi di Claude Console telah didesain ulang dengan minimap timeline, transkrip yang dikelompokkan berdasarkan permintaan model, dan panel Inspector untuk detail dan biaya sesi, event mentah, statistik per alat, sumber daya yang di-mount, dan aktivitas per thread. Lihat [Observabilitas Console](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#console-observability).

### 18 Agustus 2026

* Workbench kini menjadi [**playground**](https://platform.claude.com/playground) di Claude Console. Playground mendukung setiap parameter Messages API dan menyertakan template yang mendemonstrasikan fitur API seperti eksekusi kode dan web search. Playground menampilkan permintaan SDK lengkap dan respons API untuk setiap eksekusi, untuk membantu Anda memahami API dan membangun dengannya. Untuk informasi lebih lanjut, lihat [Pusat Bantuan Claude](https://support.claude.com/en/articles/8606378-how-do-i-use-playground) atau coba di [platform.claude.com/playground](https://platform.claude.com/playground).

### 11 Agustus 2026

* [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini mengembalikan transkrip sesi Cowork dan Claude Code yang berjalan di mesin pengguna Anda, dalam beta untuk organisasi Claude Enterprise. `GET /v1/compliance/apps/sessions/local` mencantumkan sesi di seluruh organisasi Anda, `GET /v1/compliance/apps/sessions/local/{session_id}` mengambil metadata satu sesi, dan `GET /v1/compliance/apps/sessions/local/{session_id}/messages` mengembalikan transkripnya, semuanya dengan Compliance Access Key Anda yang sudah ada dan cakupan `read:compliance_user_data`. Lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions).
* Kami telah menambahkan header respons `anthropic-workspace-id` ke Claude API. Header ini membawa ID berawalan `wrkspc_` dari workspace yang menjadi tujuan resolusi kunci API atau token akses permintaan, termasuk Default Workspace organisasi Anda. Lihat [Mengidentifikasi workspace di balik respons API](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response).

### 10 Agustus 2026

* Harga perkenalan untuk **Claude Sonnet 5** ($2 / $10 per MTok) kini menjadi harga standar: kenaikan yang sebelumnya dijadwalkan menjadi $3 / $15 per MTok pada 1 September 2026 tidak akan terjadi. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing).

### 7 Agustus 2026

* Anda kini dapat menetapkan anggaran pada sesi Claude Managed Agents: batas keras pada pengeluaran sesi, dengan harga sesuai tarif daftar publik. Sesi yang mencapai anggarannya dijeda dengan stop reason `budget_reached` alih-alih memulai permintaan model baru; mengubah atau menghapus anggaran akan melanjutkannya. Deployment menerima anggaran yang sama dan menerapkannya ke setiap sesi yang dimulainya. Lihat [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets).
* Anda kini dapat memberi sesi Claude Managed Agents sebuah advisor: model yang setidaknya sama mampunya dengan model agen itu sendiri yang dapat dikonsultasikan oleh thread utama sesi di tengah giliran untuk panduan strategis. Konfigurasikan sebagai entri `{"type": "advisor"}` dalam roster multiagen agen, dengan menyebutkan `model` yang akan dikonsultasikan. Lihat [Memberi sesi sebuah advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor).
* Anda kini dapat mengontrol di mana inferensi model berjalan untuk agen Claude Managed Agents. Atur `inference_geo` di dalam objek `model` saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo), atau [timpa untuk satu sesi](https://platform.claude.com/docs/id/managed-agents/sessions#pin-the-inference-geo-for-a-session). Lihat [Residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency) untuk geo yang tersedia dan harganya.
* Sesi Claude Managed Agents kini dapat [memuat skill dari repositori GitHub](https://platform.claude.com/docs/id/managed-agents/skills#load-skills-from-a-github-repository). Saat sebuah sesi [me-mount repositori](https://platform.claude.com/docs/id/managed-agents/github), skill apa pun di direktori root `.claude/skills`-nya ditemukan secara otomatis saat sesi dimulai dan tersedia bagi agen untuk sesi tersebut.

### 5 Agustus 2026

* **Inference hooks** kini tersedia dalam beta untuk organisasi Claude Enterprise. Arahkan Claude ke server keamanan AI organisasi Anda, dan setiap prompt yang diatur di seluruh claude.ai, Cowork, dan Claude Code ditahan untuk menunggu putusan izinkan atau tolak dari server sebelum inferensi dilanjutkan. Permintaan ditandatangani, penanganan kegagalan dapat dikonfigurasi, dan setiap penolakan dicatat dalam [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) kepatuhan. Lihat [Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks).
* Kami telah memensiunkan model Claude Opus 4.1 (`claude-opus-4-1-20250805`). Semua permintaan ke model ini di Claude API kini akan mengembalikan error. Kami merekomendasikan upgrade ke [Claude Opus 5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 3 Agustus 2026

* [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) kini mengembalikan transkrip sesi Cowork yang dimulai di claude.ai web atau mobile, dalam beta untuk organisasi Claude Enterprise. `GET /v1/compliance/apps/sessions/remote` mencantumkan sesi dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi, menggunakan Compliance Access Key Anda yang sudah ada dengan cakupan `read:compliance_user_data`. Lihat [Sesi di cloud](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions).

### 1 Agustus 2026

* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) (pratinjau riset) kini mendukung Claude Opus 5. Lihat [Model yang didukung](https://platform.claude.com/docs/id/managed-agents/dreams#limits).

### 24 Juli 2026

* Kami telah meluncurkan **Claude Opus 5** (`claude-opus-5`), peningkatan besar dibandingkan Claude Opus 4.8. Claude Opus 5 mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (baik default maupun maksimum), output maksimum 128k token, dan [thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, dengan harga $5 / $25 USD per MTok, harga yang sama dengan Claude Opus 4.8. Model ini tersedia di Claude API, [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Lihat [Yang baru di Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5) untuk fitur baru, perubahan perilaku, dan panduan migrasi, serta [ikhtisar model](https://platform.claude.com/docs/id/models/overview) untuk spesifikasi lengkap.
* Pada Claude Opus 5, menonaktifkan thinking hanya diizinkan pada effort `high` atau lebih rendah: `thinking: {"type": "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, sebuah perubahan yang merusak kompatibilitas dari Claude Opus 4.8. Lihat [Yang baru di Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5#behavior-changes).
* [Effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol utama untuk mengarahkan Claude Opus 5: model ini mendukung seluruh jenjang (`low`, `medium`, `high`, `xhigh`, `max`), dengan `max` untuk pekerjaan yang kritis terhadap kemampuan.
* Perubahan alat di tengah percakapan kini tersedia dalam beta pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 5: tambahkan atau hapus alat di antara giliran percakapan sambil mempertahankan cache prompt. Sertakan header beta `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda.
* Parameter `fallbacks` kini mendukung mode `"default"`, yang menerapkan model fallback yang direkomendasikan Anthropic berdasarkan kategori penolakan. Fallback sisi server tersedia dalam beta, dan mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Kami telah menghapus [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.7. Permintaan ke `claude-opus-4-7` dengan `speed: "fast"` kini mengembalikan error; tidak seperti Claude Opus 4.6, permintaan tersebut tidak beralih ke kecepatan standar. Claude Opus 4.7 sendiri tetap tersedia pada kecepatan standar. Untuk terus menggunakan fast mode, migrasikan ke [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-47) atau Claude Opus 4.8. Baca lebih lanjut di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 22 Juli 2026

* Anda kini dapat menetapkan level `effort` pada konfigurasi model agen Claude Managed Agents. Teruskan `effort` di dalam objek `model` saat Anda [membuat agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#create-an-agent). Lihat [Level effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels) untuk mengetahui fungsi setiap level.
* Webhook untuk Claude Managed Agents kini mencakup siklus hidup environment dan memory store: empat tipe event `environment.*` dan tiga tipe event `memory_store.*`. Anda dapat bereaksi terhadap perubahan siklus hidup environment dan memory store tanpa polling. Lihat tab Environment events dan Memory store events di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types).
* Saat membuat sesi Claude Managed Agents, Anda kini dapat [mengisinya dengan event awal](https://platform.claude.com/docs/id/managed-agents/sessions#seed-the-session-with-initial-events). Teruskan `initial_events` pada `POST /v1/sessions` dengan hingga 50 event `user.message` dan `user.define_outcome`. Daftar yang tidak kosong memulai loop agen dalam panggilan yang sama, sehingga Anda tidak memerlukan permintaan send-events terpisah untuk memulai pekerjaan.
* Field `version` kini opsional saat [memperbarui agen Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-an-agent). Sertakan untuk optimistic concurrency (ketidakcocokan mengembalikan error 409), atau hilangkan untuk menerapkan pembaruan tanpa syarat. Lihat [Semantik pembaruan](https://platform.claude.com/docs/id/managed-agents/agent-setup#update-semantics).
* Stream event thread sesi Claude Managed Agents kini mendukung [delta event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas). `GET /v1/sessions/{session_id}/threads/{thread_id}/stream` menerima parameter query `event_deltas[]` yang sama dengan stream tingkat sesi, sehingga Anda dapat melihat pratinjau teks subagen saat model menghasilkannya. Sebuah koneksi hanya mempratinjau thread yang sedang dibacanya. Lihat [Pratinjau event thread sesi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#preview-session-thread-events).

### 17 Juli 2026

* **Workbench** legacy ([platform.claude.com/workbench](https://platform.claude.com/workbench)) di Claude Console akan dihentikan dengan akses berakhir pada 17 Agustus 2026. Prompt tersimpan, variabel, dan eval tidak didukung di [Workbench](https://platform.claude.com/playground) yang diperbarui. Anda dapat mengekspor data apa pun yang ingin Anda simpan dari banner dan di bawah **Organizational Settings** Anda. Untuk informasi lebih lanjut, lihat [Bagaimana cara menggunakan Workbench?](https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench) di Pusat Bantuan Claude.
* API alat prompt eksperimental untuk menghasilkan, memperbaiki, dan membuat template prompt (`/v1/experimental/generate_prompt`, `/v1/experimental/improve_prompt`, dan `/v1/experimental/templatize_prompt`) akan dipensiunkan bersama Workbench pada 17 Agustus 2026. Setelah penghapusan, permintaan ke endpoint ini akan mengembalikan error.

### 15 Juli 2026

* [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) tersedia pada Claude Fable 5, Claude Mythos 5, dan Claude Opus 4.8, di Claude API, [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai). Tidak diperlukan header beta. Ini mengoreksi catatan ketersediaan sebelumnya.

### 14 Juli 2026

* Anda kini dapat mengelola orang-orang di organisasi **Claude Enterprise** (claude.ai) Anda dengan [Admin API](https://platform.claude.com/docs/id/api/admin), dalam beta untuk semua organisasi Claude Enterprise: mencantumkan anggota dan mencarinya berdasarkan alamat email, mengubah peran anggota, menghapus anggota, mengirim dan menarik undangan, mengelola grup dan keanggotaannya, serta membaca peran kustom. Permintaan grup dan peran kustom memerlukan header beta `anthropic-beta: ce-user-management-2026-07-13`; permintaan anggota dan undangan tidak memerlukan header beta. Kunci Admin API dengan cakupan `read:org_audit` juga dapat memanggil setiap endpoint `GET` manajemen pengguna. Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management).

### 10 Juli 2026

* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) (pratinjau riset) kini mendukung Claude Fable 5 dan Claude Sonnet 5. Lihat [Model yang didukung](https://platform.claude.com/docs/id/managed-agents/dreams#limits).
* Kami telah memperluas dokumentasi [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency) tentang event `cmek_preserve` dengan contoh filter, contoh payload event, dan dua kode alasan preservasi (`policy_violation_investigation`, `csae_report`). Dokumentasi kini juga memperjelas bahwa event preservasi ditulis baik preservasi tersebut diprakarsai oleh peninjau manusia maupun pipeline keamanan otomatis. Lihat [Preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation).

### 8 Juli 2026

* Anda kini dapat menetapkan kedaluwarsa saat membuat kunci API atau kunci Admin API di [Claude Console](https://platform.claude.com/settings/keys). Pilih preset, durasi kustom, atau **Never**. Untuk kunci dengan masa berlaku setidaknya 7 hari, Anthropic mengirim email kepada pembuatnya sebelum kedaluwarsa. Kunci yang sudah ada tidak terpengaruh. Admin API melaporkan kedaluwarsa setiap kunci dalam field [`expires_at`](https://platform.claude.com/docs/id/api/admin/api_keys/list). Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration).

### 2 Juli 2026

* Kami telah menambahkan header beta `agent-memory-2026-07-22`, yang mengubah perilaku [pencantuman memori](https://platform.claude.com/docs/id/managed-agents/memory#list-memories) (`GET /v1/memory_stores/{memory_store_id}/memories`): hasil dikembalikan dalam urutan stabil yang ditentukan server dan parameter `order_by` serta `order` diabaikan; `depth` hanya menerima `0`, `1`, atau dihilangkan (nilai lain mengembalikan error `400`); dan `path_prefix` harus diakhiri dengan `/` serta mencocokkan segmen path utuh alih-alih substring. Kursor halaman yang diterbitkan tanpa header tersebut tidak valid dengannya, jadi mulai ulang dari halaman pertama saat Anda mengadopsinya. Pada endpoint memory store, `agent-memory-2026-07-22` menggantikan `managed-agents-2026-04-01`; mengirim keduanya mengembalikan error `400`. Pada 22 Juli 2026, header `managed-agents-2026-04-01` mengadopsi perilaku pencantuman yang sama. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
* SDK Python (0.116.0), TypeScript (0.110.0), Go (1.56.0), Java (2.48.0), Ruby (1.55.0), PHP (0.36.0), C# (12.35.0), dan CLI (1.16.0) kini mengirim `agent-memory-2026-07-22` pada semua panggilan memory store alih-alih `managed-agents-2026-04-01`. Jika kode Anda meneruskan `betas` secara eksplisit pada panggilan memory store, ganti `managed-agents-2026-04-01` dengan `agent-memory-2026-07-22` di sana alih-alih menambahkan nilai kedua.

### 1 Juli 2026

* Kami telah memulihkan akses ke Claude Fable 5 dan Claude Mythos 5. Lihat [pernyataan kami](https://www.anthropic.com/news/redeploying-fable-5) untuk informasi lebih lanjut.

### 30 Juni 2026

* Kami telah meluncurkan **Claude Sonnet 5** (`claude-sonnet-5`), generasi berikutnya dari keluarga model Sonnet kami, dengan harga perkenalan $2 / $10 per MTok (dijadikan harga standar pada 10 Agustus 2026). Claude Sonnet 5 mendukung ["context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows), 128k token output maksimum, serta rangkaian alat dan fitur platform yang sama dengan Claude Sonnet 4.6, kecuali [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), yang tidak tersedia di Claude Sonnet 5. Tiga perubahan perilaku berlaku saat bermigrasi: [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) kini aktif secara default; "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) dihapus dan mengembalikan error 400 (fitur ini sudah dideprekasi pada Sonnet 4.6); dan mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default akan mengembalikan error 400. Claude Sonnet 5 juga menggunakan tokenizer baru yang menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Lihat [Yang baru di Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/whats-new-sonnet-5) untuk detail dan panduan migrasi. Untuk perbedaan perilaku dan pola prompting khusus model, lihat [Prompting Claude Sonnet 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5).
* Stream event sesi Claude Managed Agents kini mendukung [event delta](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#event-deltas). Aktifkan dengan parameter query `event_deltas[]` pada `GET /v1/sessions/{session_id}/events/stream`. Event `event_start` dan `event_delta` menampilkan pratinjau teks pesan agen saat sedang dihasilkan, sebelum event `agent.message` lengkap tiba.
* [Mendaftar sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#listing-sessions) untuk Claude Managed Agents kini mendukung paginasi mundur. `GET /v1/sessions` mengembalikan kursor `prev_page` bersama `next_page`; teruskan sebagai parameter `page` untuk kembali ke halaman sebelumnya. Lihat [Paginasi](https://platform.claude.com/docs/id/api/overview#pagination).
* Saat membuat sesi Claude Managed Agents, Anda kini dapat [menimpa konfigurasi agen untuk sesi tersebut](https://platform.claude.com/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session). Teruskan `agent` dengan `type: "agent_with_overrides"` untuk mengganti model, prompt sistem, alat, server MCP, atau skill untuk satu sesi. Agen itu sendiri tidak berubah.
* Vault Claude Managed Agents kini mendukung pengaturan `injection_location` pada [kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential) (tab Environment variable). Pengaturan ini mengontrol apakah nilai kredensial disubstitusikan, saat egress, ke dalam header permintaan keluar agen, body permintaan, atau keduanya.
* Webhook untuk Claude Managed Agents kini mencakup siklus hidup agen, deployment, dan deployment run. Anda dapat bereaksi terhadap versi agen yang baru dipublikasikan, deployment yang dijeda, atau run terjadwal yang gagal tanpa polling. Lihat tab Agent events, Deployment events, dan Deployment run events di [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks#supported-event-types).

### 29 Juni 2026

* Kami telah menghapus [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.6. Permintaan ke `claude-opus-4-6` dengan `speed: "fast"` tidak lagi berjalan pada kecepatan fast atau harga premium: permintaan tersebut berjalan pada kecepatan standar, ditagih dengan tarif standar, dan tidak mengembalikan error. Field `usage.speed` pada respons melaporkan kecepatan yang digunakan. Untuk terus menggunakan fast mode, migrasikan ke [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 26 Juni 2026

* Kami telah menaikkan ["rate limits" (batas laju)](https://platform.claude.com/docs/id/api/rate-limits) di seluruh Claude API. Batas laju Claude Sonnet dan Claude Haiku kini setara dengan Claude Opus di setiap tingkat penggunaan, dan tingkat penggunaan telah dikonsolidasikan menjadi tiga: Start, Build, dan Scale. Sebagian besar organisasi berpindah ke tingkat yang lebih tinggi, tidak ada organisasi yang menerima batas lebih rendah dari sebelumnya, dan tidak ada tindakan yang diperlukan. Anda dapat melihat tingkat dan batas Anda saat ini di [Claude Console](https://platform.claude.com/settings/limits).

### 25 Juni 2026

* Kami telah mendeprekasi [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.7, dengan penghapusan pada 24 Juli 2026. Setelah penghapusan, permintaan ke `claude-opus-4-7` dengan `speed: "fast"` akan mengembalikan error. Migrasikan ke fast mode untuk Claude Opus 4.8. Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).

### 22 Juni 2026

* **MCP tunnels** (pratinjau riset): API manajemen dipindahkan dari `/v1/organizations/tunnels` pada Admin API ke `/v1/tunnels` pada Claude API. Surface baru ini menggunakan header `anthropic-beta: mcp-tunnels-2026-06-22` dan scope WIF `workspace:manage_tunnels`. Surface sebelumnya tetap tersedia selama periode migrasi. Lihat [referensi Tunnels API](https://platform.claude.com/docs/id/api/beta/tunnels).

### 18 Juni 2026

* SDK Python, TypeScript, Go, Java, Ruby, PHP, dan C# kini menyertakan dukungan untuk `code_execution_20260120`, versi [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) yang menambahkan persistensi state REPL dan merupakan versi minimum untuk [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling). Untuk mengadopsinya, atur `type` alat ke `code_execution_20260120`; tidak diperlukan header beta. Tersedia di Claude Fable 5, Claude Mythos 5, Claude Opus 4.5 dan yang lebih baru, serta Claude Sonnet 4.5 dan yang lebih baru; lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#compatibility) pada alat eksekusi kode.

### 15 Juni 2026

* Kami telah memensiunkan model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`). Semua permintaan ke model-model ini pada Claude API kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Opus 4.8](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) masing-masing. Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 11 Juni 2026

* [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) kini mendukung `code_execution_20260521`, yang mengungkapkan batas waktu eksekusi 90 detik per sel dalam deskripsi alat sehingga Claude dapat menganggarkan sel yang berjalan lama. Tidak diperlukan header beta.
* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) kini mendukung `web_search_20260318` dan `web_fetch_20260318`, menambahkan parameter `response_inclusion` untuk menghilangkan blok hasil yang telah dikonsumsi dari respons API untuk alur kerja agentik. Tidak diperlukan header beta.

### 10 Juni 2026

* Endpoint `GET /v1/environments/{id}/work`, yang mendaftar pekerjaan tertunda untuk [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) untuk aksi `GetEnvironment` yang mengotorisasinya.

### 9 Juni 2026

* Kami telah meluncurkan **Claude Fable 5** (`claude-fable-5`), model kami yang paling mumpuni yang dirilis secara luas, bersama **Claude Mythos 5** (`claude-mythos-5`) untuk peserta Project Glasswing. Kedua model mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, 128k token output maksimum, dan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) untuk kemampuan, perubahan API, dan ketersediaan.
* Claude Fable 5 dan Claude Mythos 5 menggunakan tokenizer yang diperkenalkan bersama Claude Opus 4.7. Dibandingkan dengan model sebelum Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Gunakan [API penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting#token-counts-on-claude-fable-5) dengan `model: "claude-fable-5"` untuk mengukur prompt Anda dengan tokenizer baru.
* Claude Fable 5 menjalankan classifier keamanan pada permintaan dan selama pembuatan respons. Ketika classifier menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"`. Anda tidak ditagih untuk permintaan yang ditolak sebelum output apa pun dihasilkan. Parameter `fallbacks` opsional (dalam beta di Claude API dan Claude Platform on AWS; tidak didukung di Message Batches API) menjalankan ulang permintaan yang ditolak pada model lain, ditagih dengan tarif model fallback. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* Field [`stop_details.category`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan kini menyertakan `"reasoning_extraction"` di Claude Fable 5, dikembalikan ketika permintaan diblokir berdasarkan pembatasan Ketentuan Layanan Anthropic terkait rekayasa balik atau duplikasi output model. Kategori `"cyber"` dan `"bio"` yang sudah ada tidak berubah. Tidak diperlukan header beta.
* Pada Claude Fable 5 dan Claude Mythos 5, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) adalah satu-satunya mode thinking: `thinking: {"type": "disabled"}` tidak didukung, dan anggaran pemikiran diperpanjang manual serta prefill asisten tidak didukung (keduanya mengembalikan error 400). Lihat [Bermigrasi dari Claude Mythos Preview ke Claude Mythos 5](https://platform.claude.com/docs/id/models/fable-5/migration-guide#migrating-from-claude-mythos-preview).
* Pada Claude Fable 5 dan Claude Mythos 5, `thinking.display` secara default bernilai `"omitted"`, sama seperti Claude Opus 4.8, Claude Opus 4.7, dan Claude Mythos Preview; atur `display: "summarized"` untuk menerima ringkasan thinking yang dapat dibaca. Rantai pemikiran mentah tidak pernah dikembalikan; teruskan kembali blok thinking tanpa perubahan dalam percakapan multi-giliran pada model yang sama. Lihat [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Claude Fable 5 memerlukan retensi data 30 hari dan tidak tersedia dengan zero data retention. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Claude Managed Agents kini mendukung [deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments), memungkinkan Anda menjalankan sesi dengan jadwal cron tanpa mengelola scheduler Anda sendiri.
* Vault Claude Managed Agents kini mendukung [kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential), sehingga Anda dapat menyuntikkan secret dengan aman ke dalam sandbox agen untuk CLI, SDK, dan layanan lain yang melakukan autentikasi melalui variabel lingkungan.
* [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) (`GET /v1/compliance/activities`) kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#compliance) untuk aksi `ListComplianceActivities` yang mengotorisasinya.
* Event webhook `session.thread_*` kini menyertakan field `session_thread_id` yang mengidentifikasi thread multiagen yang memicu event tersebut.
* Kami telah merilis [paket Swift](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/apple-foundation-models) dalam beta yang menambahkan Claude sebagai `LanguageModel` sisi server dalam framework Foundation Models milik Apple. Panggil Claude melalui API `LanguageModelSession` yang sama dengan model on-device Apple di iOS 27, macOS 27, visionOS 27, dan watchOS 27 (beta).

### 5 Juni 2026

* Kami mengumumkan deprekasi model Claude Opus 4.1 (`claude-opus-4-1-20250805`), dengan pemensiunan di Claude API dijadwalkan pada 5 Agustus 2026. Kami merekomendasikan untuk bermigrasi ke [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Deprekasi model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 2 Juni 2026

* [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) kini mendukung parameter `max_tokens` untuk membatasi output model advisor per panggilan, mengurangi latensi dan biaya token output untuk beban kerja yang tidak memerlukan respons advisor dengan panjang penuh. Atur `tools[].max_tokens` pada definisi alat advisor; lihat [Membatasi output advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#capping-advisor-output).
* Di Claude API, Anda tidak lagi ditagih untuk permintaan ketika permintaan tersebut mengembalikan `stop_reason: "refusal"` tanpa Claude menghasilkan output apa pun. Lihat [Penolakan streaming](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) untuk mendeteksi dan menangani penolakan.

### 29 Mei 2026

* [Webhook](https://platform.claude.com/docs/id/managed-agents/webhooks), [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), dan [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) Claude Managed Agents kini tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Aksi IAM untuk Claude Platform on AWS](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions) untuk aksi IAM baru dan managed policy `AnthropicSelfHostedEnvironmentAccess`.

### 28 Mei 2026

* Kami telah meluncurkan **Claude Opus 4.8** (claude-opus-4-8), model kami yang paling mumpuni yang dirilis secara luas. Claude Opus 4.8 mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry, 128k token output maksimum, serta rangkaian alat dan fitur platform yang sama dengan Claude Opus 4.7. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) untuk pengaturan dasar, fitur, dan panduan migrasi.
* Kami telah meluncurkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Pada Claude Opus 4.8, Anda dapat mengirim pesan `role: "system"` setelah giliran pengguna (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)) dalam array `messages`, mempertahankan cache hit prompt ketika instruksi berubah selama sesi yang berjalan lama. Tidak diperlukan header beta.
* Field [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan kini didokumentasikan secara publik; field ini mengembalikan `category` (`cyber`, `bio`, atau `null`) dan `explanation` yang dapat dibaca manusia, sehingga aplikasi Anda dapat mengarahkan berbagai kelas penolakan ke langkah berikutnya yang tepat. Tidak diperlukan header beta.
* Pada Claude Opus 4.8, [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) secara default bernilai `high` di semua surface, termasuk Claude Code dan Messages API.
* Pada Claude Opus 4.8, panjang prompt minimum yang dapat di-cache untuk ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) adalah 1.024 token, lebih rendah daripada Claude Opus 4.7.
* Dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) diaktifkan, Claude Opus 4.8 memicu penalaran hanya ketika suatu giliran membutuhkannya, mengurangi token thinking yang terbuang dibandingkan Claude Opus 4.7 pada tingkat effort yang sama.
* Claude Opus 4.8 mendukung [input gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga 2576 piksel pada sisi panjang), sama seperti Claude Opus 4.7.
* [Task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) kini mendukung Claude Opus 4.8.
* [Alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) kini mendukung Claude Opus 4.8.
* [Computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) kini mendukung Claude Opus 4.8.
* [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.8 tersedia sebagai pratinjau riset hanya di Claude API.
* Mengatur parameter sampling `temperature`, `top_p`, atau `top_k` ke nilai non-default akan mengembalikan error 400 pada Claude Opus 4.8, sama seperti pada Claude Opus 4.7. Lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) untuk detail.
* Di Claude Code, kami telah memperluas Auto mode ke lebih banyak pengguna untuk tugas yang berjalan lama. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, pengguna paket Max kini secara default menggunakan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) pada Claude Opus 4.8. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, Workflows tersedia sebagai pratinjau riset, memungkinkan Anda mendefinisikan dan menjalankan rencana agentik multilangkah. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Kami telah mendeprekasi [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.6, dengan penghapusan sekitar 30 hari setelah peluncuran. Migrasikan ke fast mode untuk Claude Opus 4.8 atau Claude Opus 4.7. Baca selengkapnya di [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode#supported-models).
* Untuk pembaruan pada claude.ai, Cowork, Claude for Microsoft 365, dan aplikasi Claude lainnya dalam rilis ini, lihat [catatan rilis untuk Claude Apps](https://support.claude.com/en/articles/12138966-release-notes).

### 27 Mei 2026

* Respons Messages API kini menyertakan [`usage.output_tokens_details.thinking_tokens`](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning), yang melaporkan berapa banyak token output yang ditagih merupakan pemikiran diperpanjang. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir. Tidak diperlukan header beta.

### 19 Mei 2026

* [MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) kini tersedia sebagai pratinjau riset, sehingga Anda dapat terhubung ke server MCP di jaringan privat Anda.
* Sandbox self-hosted kini tersedia untuk Claude Managed Agents, sebagai alternatif untuk menjalankan eksekusi alat di infrastruktur Anthropic. Lihat [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes).
* Dengan Claude Managed Agents, Anda kini dapat memperbarui konfigurasi server MCP dan alat agen yang terkait dengan sesi aktif.
* Dengan Claude Managed Agents, output besar dari `agent_toolset` dan alat MCP yang melebihi 100K karakter (sekitar 25K token) kini secara otomatis dialihkan ke file di sandbox. Model menerima pratinjau terpotong beserta path file dan dapat membaca konten lengkapnya dari sana.

### 18 Mei 2026

* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) kini mengembalikan data pengajuan SEC yang lebih kaya, memudahkan agen riset keuangan, analisis laporan laba, dan alur kerja uji tuntas untuk berlandaskan pada sumber primer dengan sitasi.

### 13 Mei 2026

* Kami telah meluncurkan [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) dalam beta publik. Teruskan `diagnostics.previous_message_id` pada permintaan Messages dan API akan melaporkan `cache_miss_reason` yang menjelaskan di mana prefiks cache prompt menyimpang dari giliran sebelumnya. Sertakan header beta `cache-diagnosis-2026-04-07` dalam permintaan Anda.

### 12 Mei 2026

* [Fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset) kini mendukung Claude Opus 4.7. Atur `speed: "fast"` dengan `model: "claude-opus-4-7"` dan header beta `fast-mode-2026-02-01` untuk pembuatan token output yang jauh lebih cepat dengan harga premium. Harga, batas laju, dan akses sama dengan fast mode Opus 4.6; pelanggan yang berminat dapat bergabung dengan [daftar tunggu](https://claude.com/fast-mode).

### 11 Mei 2026

* Kami telah meluncurkan **Claude Platform on AWS**, menghadirkan Claude API ke infrastruktur yang dikelola Anthropic dan dapat diakses melalui AWS, dengan penagihan AWS dan autentikasi IAM. Akses Messages API, Files API, Message Batches API, Claude Managed Agents, Agent Skills, eksekusi kode, dan penggunaan alat secara lengkap melalui endpoint AWS native. Pelajari lebih lanjut di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).

### 6 Mei 2026

* [Orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) dan [Outcomes](https://platform.claude.com/docs/id/managed-agents/define-outcomes) kini dalam beta publik di bawah header beta standar `managed-agents-2026-04-01`.
* Refresh latar belakang kredensial vault Claude Managed Agents kini didukung untuk kredensial `mcp_oauth`. Lihat [Autentikasi dengan vault](https://platform.claude.com/docs/id/managed-agents/vaults).
* Webhook untuk Claude Managed Agents kini didukung. Tipe event webhook mencakup event siklus hidup sesi dan vault. Lihat [Berlangganan webhook](https://platform.claude.com/docs/id/managed-agents/webhooks).
* Opsi pemfilteran dan pengurutan tambahan kini didukung untuk Claude Managed Agents. Sesi dapat difilter berdasarkan status, dan event dapat difilter berdasarkan tipe. Event kini dapat difilter berdasarkan waktu pembuatan.
* [Dreams](https://platform.claude.com/docs/id/managed-agents/dreams) untuk Claude Managed Agents kini tersedia sebagai pratinjau riset. Sebuah dream membaca memory store yang ada bersama transkrip sesi sebelumnya dan menghasilkan memory store output yang telah ditata ulang dengan duplikat digabungkan, entri usang diganti, dan wawasan baru dimunculkan. Endpoint dream dibatasi oleh header beta `dreaming-2026-04-21`. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.

### 4 Mei 2026

* Kami telah meluncurkan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Autentikasi beban kerja ke Claude API dengan token OIDC berumur pendek dari penyedia identitas Anda sendiri (AWS IAM, Google Cloud, GitHub Actions, Kubernetes, Microsoft Entra ID, Okta, SPIFFE, dan lainnya) alih-alih "API key" (kunci API) statis berumur panjang. Konfigurasikan issuer dan aturan federasi di Claude Console, dan SDK akan menangani pertukaran dan refresh token secara otomatis. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

### 30 April 2026

* Kami telah memensiunkan beta jendela konteks 1 juta token (`context-1m-2025-08-07`) untuk Claude Sonnet 4.5 dan Claude Sonnet 4. Header beta tersebut kini tidak berpengaruh pada model-model ini, dan permintaan yang melebihi jendela konteks standar 200k token akan mengembalikan error. Untuk menggunakan jendela konteks 1 juta token, migrasikan ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) atau [Claude Opus 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison), di mana fitur ini sudah termasuk dengan harga standar tanpa memerlukan header beta.

### 29 April 2026

* Kami telah merilis [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill), sebuah [Agent Skill](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) open-source yang memberi Claude materi referensi terkini untuk membangun di atas Messages API dan Claude Managed Agents dalam 8 bahasa. Skill ini dibundel dengan Claude Code dan tersedia di [repositori skills Anthropic](https://github.com/anthropics/skills/tree/main/skills/claude-api).

### 24 April 2026

* Kami telah merilis [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api), yang memungkinkan administrator untuk secara terprogram mengkueri batas laju yang dikonfigurasi untuk organisasi dan workspace mereka.

### 23 April 2026

* Memory untuk Claude Managed Agents kini dalam beta publik di bawah header standar `managed-agents-2026-04-01`. Lihat [Menggunakan memory agen](https://platform.claude.com/docs/id/managed-agents/memory) untuk panduan integrasi lengkap.

### 20 April 2026

* Kami telah memensiunkan model Claude Haiku 3 (`claude-3-haiku-20240307`). Semua permintaan ke model ini kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison).

### 16 April 2026

* Kami telah meluncurkan [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), model kami yang paling mumpuni yang dirilis secara luas untuk penalaran kompleks dan coding agentik, dengan harga $5 / $25 per MTok yang sama dengan Opus 4.6. Lihat [Yang baru di Claude Opus 4.7](https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-7) untuk peningkatan kemampuan, fitur baru, dan tokenizer yang diperbarui. Opus 4.7 menyertakan perubahan API yang tidak kompatibel dibandingkan Opus 4.6; lihat [panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide) sebelum meningkatkan.
* [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) kini terbuka untuk semua pelanggan Amazon Bedrock. Claude Opus 4.7 dan Claude Haiku 4.5 tersedia secara self-serve dari konsol Bedrock melalui endpoint Messages API di `/anthropic/v1/messages`, di 27 region AWS dengan endpoint global dan regional.
* Kami telah meluncurkan [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) dalam beta pada Claude Opus 4.7. Berikan Claude anggaran token bersifat saran untuk satu loop agentik penuh (thinking, panggilan alat, hasil alat, dan output) dan model akan melihat hitungan mundur berjalan, menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikannya dengan baik saat anggaran terpakai. Sertakan header beta `task-budgets-2026-03-13` dalam permintaan Anda.
* Claude Opus 4.7 mendukung [input gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7), menaikkan resolusi gambar maksimum dari 1568 menjadi 2576 piksel pada sisi panjang untuk peningkatan performa pada computer use, pemahaman tangkapan layar, dan analisis dokumen. Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta; gambar dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya.
* Kami telah menambahkan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `xhigh` pada Claude Opus 4.7. `xhigh` berada di antara `high` dan `max` dan disetel untuk tugas agentik dan coding yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan. Tidak diperlukan header beta.

### 14 April 2026

* Kami mengumumkan deprekasi model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`), dengan pemensiunan di Claude API dijadwalkan pada 15 Juni 2026. Kami merekomendasikan untuk bermigrasi ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Opus 4.8](https://platform.claude.com/docs/id/about-claude/models/migration-guide) masing-masing. Baca selengkapnya di [Deprekasi model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 9 April 2026

* Kami telah meluncurkan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) dalam beta publik. Pasangkan model executor yang lebih cepat dengan model advisor berkecerdasan lebih tinggi yang memberikan panduan strategis di tengah pembuatan respons, sehingga beban kerja agentik berjangka panjang mendekati kualitas advisor-solo sementara sebagian besar pembuatan token terjadi dengan tarif model executor. Sertakan header beta `advisor-tool-2026-03-01` dalam permintaan Anda.

### 8 April 2026

* Kami telah meluncurkan **Claude Managed Agents** dalam beta publik, sebuah harness agen yang dikelola sepenuhnya untuk menjalankan Claude sebagai agen otonom dengan sandboxing aman, alat bawaan, dan streaming server-sent event. Buat agen, konfigurasikan container, dan jalankan sesi melalui API. Semua endpoint memerlukan header beta `managed-agents-2026-04-01`. Pelajari lebih lanjut di [Ikhtisar Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview).
* Kami telah meluncurkan **CLI `ant`**, klien baris perintah untuk Claude API yang memungkinkan interaksi lebih cepat dengan Claude API, integrasi native dengan Claude Code, dan pembuatan versi sumber daya API dalam file YAML. Pelajari lebih lanjut di [quickstart CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart).

### 7 April 2026

* Kami mengumumkan [Claude Mythos Preview](https://anthropic.com/glasswing) tersedia sebagai pratinjau riset terbatas untuk pekerjaan keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya melalui undangan.
* [Messages API](https://platform.claude.com/docs/id/api/messages) kini tersedia di Amazon Bedrock sebagai pratinjau riset. Endpoint Claude in Amazon Bedrock baru di `/anthropic/v1/messages` menggunakan bentuk permintaan yang sama dengan Claude API pihak pertama dan berjalan di infrastruktur yang dikelola AWS tanpa akses operator. Tersedia di `us-east-1`; hubungi account executive Anthropic Anda untuk meminta akses. Pelajari lebih lanjut di [Claude in Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock).

### 30 Maret 2026

* Kami telah menaikkan batas `max_tokens` menjadi 300k pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta) untuk Claude Opus 4.6 dan Sonnet 4.6. Sertakan header beta `output-300k-2026-03-24` untuk menghasilkan output satu giliran yang lebih panjang untuk konten berformat panjang, data terstruktur, dan tugas pembuatan kode berskala besar.
* Kami akan memensiunkan beta jendela konteks 1 juta token untuk Claude Sonnet 4.5 dan Claude Sonnet 4 pada **30 April 2026**. Setelah tanggal tersebut, header beta `context-1m-2025-08-07` tidak akan berpengaruh pada model-model ini, dan permintaan yang melebihi jendela konteks standar 200k token akan mengembalikan error. Untuk terus menggunakan jendela konteks 1 juta token, migrasikan ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) atau [Claude Opus 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison), yang mendukung jendela konteks 1 juta token penuh dengan harga standar tanpa memerlukan header beta.

### 18 Maret 2026

* Kami telah menambahkan field kemampuan model ke [Models API](https://platform.claude.com/docs/id/api/models/list). `GET /v1/models` dan `GET /v1/models/{model_id}` kini mengembalikan `max_input_tokens`, `max_tokens`, dan objek `capabilities`. Kueri API untuk mengetahui apa yang didukung setiap model.

### 16 Maret 2026

* Kami telah meluncurkan field `display` untuk pemikiran diperpanjang, memungkinkan Anda menghilangkan konten thinking dari respons untuk streaming yang lebih cepat. Atur `thinking.display: "omitted"` untuk menerima blok thinking dengan field `thinking` kosong dan `signature` dipertahankan untuk kontinuitas multi-giliran. Penagihan tidak berubah. Pelajari lebih lanjut di [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

### 13 Maret 2026

* [Jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) telah keluar dari beta untuk Claude Opus 4.6 dan Sonnet 4.6, dengan harga standar. Permintaan di atas 200k token berfungsi secara otomatis untuk model-model ini tanpa memerlukan header beta. Jendela konteks 1 juta token tetap dalam beta untuk Claude Sonnet 4.5 dan Sonnet 4.
* Kami telah menghapus batas laju khusus 1M untuk semua model yang didukung. Batas akun standar Anda kini berlaku di setiap panjang konteks.
* Kami telah menaikkan batas media dari 100 menjadi 600 gambar atau halaman PDF per permintaan saat menggunakan jendela konteks 1 juta token.

### 19 Februari 2026

* Kami telah meluncurkan **caching otomatis** untuk Messages API. Tambahkan satu field `cache_control` ke body permintaan Anda dan sistem akan secara otomatis meng-cache blok terakhir yang dapat di-cache, memajukan titik cache seiring percakapan bertambah. Tidak diperlukan manajemen breakpoint manual. Berfungsi bersama kontrol cache tingkat blok yang sudah ada untuk optimasi yang lebih terperinci. Tersedia di Claude API dan Microsoft Foundry (pratinjau). Pelajari lebih lanjut di [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching).
* Kami telah memensiunkan model Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) dan model Claude Haiku 3.5 (`claude-3-5-haiku-20241022`). Semua permintaan ke Claude Sonnet 3.7 kini akan mengembalikan error. Permintaan ke Claude Haiku 3.5 di Claude API kini akan mengembalikan error; model ini tetap tersedia di Amazon Bedrock dan Google Cloud. Kami merekomendasikan untuk meningkatkan ke [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) dan [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison) masing-masing. Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).
* Kami mengumumkan deprekasi model Claude Haiku 3 (`claude-3-haiku-20240307`), dengan pemensiunan dijadwalkan pada 20 April 2026. Kami merekomendasikan untuk bermigrasi ke [Claude Haiku 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison). Baca selengkapnya di [Deprekasi model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 17 Februari 2026

* Kami telah meluncurkan [Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6), model seimbang terbaru kami yang menggabungkan kecepatan dan kecerdasan untuk tugas sehari-hari. Sonnet 4.6 memberikan performa pencarian agentik yang lebih baik sambil mengonsumsi lebih sedikit token. Sonnet 4.6 mendukung [pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) dan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (beta). Lihat [Model & Harga](https://platform.claude.com/docs/id/about-claude/models) untuk detail.
* [Eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) API kini **gratis saat digunakan bersama pencarian web atau web fetch**. Eksekusi kode dalam sandbox meningkatkan kemampuan model dan efisiensi token. Lihat [detail harga](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk penggunaan mandiri.
* [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) dan [pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) tersedia tanpa memerlukan header beta. Pencarian web dan web fetch kini mendukung [pemfilteran dinamis](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering), yang menggunakan eksekusi kode untuk memfilter hasil sebelum mencapai jendela konteks demi performa yang lebih baik dan biaya token yang lebih rendah.
* [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), [alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), [contoh penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples), dan [alat memory](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool) tidak lagi memerlukan header beta.

### 7 Februari 2026

* Kami telah meluncurkan [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (mode cepat) dalam pratinjau riset untuk Opus 4.6, yang menyediakan pembuatan token output yang jauh lebih cepat melalui parameter `speed`. Fast mode hingga 2,5x lebih cepat dengan harga premium. Pelanggan yang berminat dapat bergabung dalam [daftar tunggu](https://claude.com/fast-mode).

### 5 Februari 2026

* Kami telah meluncurkan [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), model kami yang paling cerdas untuk tugas agentik yang kompleks dan pekerjaan berjangka panjang. Opus 4.6 merekomendasikan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) (`thinking: {type: "adaptive"}`); pemikiran manual (`type: "enabled"` dengan `budget_tokens`) sudah tidak direkomendasikan lagi (deprecated). Opus 4.6 tidak mendukung prefilling pesan asisten. Pelajari lebih lanjut di [Yang baru di Claude 4.6](https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-6).
* [Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) tidak lagi memerlukan header beta dan kini mendukung Claude Opus 4.6. Effort menggantikan `budget_tokens` untuk mengontrol kedalaman pemikiran pada model-model baru.
* Kami telah meluncurkan [API compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) (pemadatan) dalam versi beta, yang menyediakan peringkasan konteks di sisi server untuk percakapan yang secara efektif tak terbatas. Tersedia di Opus 4.6.
* Kami telah memperkenalkan [kontrol residensi data](https://platform.claude.com/docs/id/manage-claude/data-residency), yang memungkinkan Anda menentukan di mana inferensi model dijalankan dengan parameter `inference_geo`. Inferensi khusus AS tersedia dengan harga 1,1x untuk model yang dirilis setelah 1 Februari 2026.
* ["Context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) kini tersedia dalam versi beta untuk Claude Opus 4.6, selain Sonnet 4.5 dan Sonnet 4. [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing) berlaku untuk permintaan yang melebihi 200 ribu token input.
* [Fine-grained tool streaming](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) (streaming alat berbutir halus) tidak lagi memerlukan header beta pada model atau platform apa pun.

### 29 Januari 2026

* [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (output terstruktur) telah keluar dari versi beta di Claude API untuk Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. Rilis ini mencakup dukungan skema yang diperluas, latensi kompilasi grammar yang lebih baik, dan jalur integrasi yang disederhanakan tanpa memerlukan header beta. Parameter `output_format` telah dipindahkan ke `output_config.format`. Pengguna beta yang sudah ada dapat terus menggunakan header beta selama masa transisi. Structured outputs tetap dalam beta publik di Amazon Bedrock dan Microsoft Foundry.

### 12 Januari 2026

* `console.anthropic.com` kini dialihkan ke `platform.claude.com`. Claude Console telah pindah ke rumah barunya sebagai bagian dari konsolidasi merek Claude kami. Bookmark dan tautan yang sudah ada akan tetap berfungsi melalui pengalihan otomatis. Untuk detail lebih lanjut, lihat [pengumuman 16 September 2025](https://platform.claude.com/docs/id/release-notes/overview#september-16-2025).

### 5 Januari 2026

* Kami telah menghentikan model Claude Opus 3 (`claude-3-opus-20240229`). Semua permintaan ke model ini kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Opus 4.5](https://platform.claude.com/docs/id/models/overview#latest-models-comparison), yang menawarkan kecerdasan yang jauh lebih baik dengan sepertiga biayanya. Peneliti dapat meminta akses berkelanjutan ke Claude Opus 3 di API melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 19 Desember 2025

* Kami mengumumkan penghentian (deprecation) model Claude Haiku 3.5. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 4 Desember 2025

* [Structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) kini mendukung Claude Haiku 4.5.

### 24 November 2025

* Kami telah meluncurkan [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5), model kami yang paling cerdas yang menggabungkan kemampuan maksimum dengan performa praktis. Ideal untuk tugas khusus yang kompleks, rekayasa perangkat lunak profesional, dan agen tingkat lanjut. Menghadirkan peningkatan signifikan dalam vision, coding, dan computer use dengan harga yang lebih terjangkau dibandingkan model Opus sebelumnya. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models).
* Kami telah meluncurkan [programmatic tool calling](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) (pemanggilan alat secara programatik) dalam beta publik, yang memungkinkan Claude memanggil alat dari dalam eksekusi kode untuk mengurangi latensi dan penggunaan token dalam alur kerja multi-alat.
* Kami telah meluncurkan [tool search tool](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) (alat pencarian alat) dalam beta publik, yang memungkinkan Claude menemukan dan memuat alat secara dinamis sesuai permintaan dari katalog alat yang besar.
* Kami telah meluncurkan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) dalam beta publik untuk Claude Opus 4.5, yang memungkinkan Anda mengontrol penggunaan token dengan menyeimbangkan antara ketelitian respons dan efisiensi.
* Kami telah menambahkan [client-side compaction](https://platform.claude.com/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) (pemadatan di sisi klien) ke SDK Python dan TypeScript kami, yang secara otomatis mengelola konteks percakapan melalui peringkasan saat menggunakan `tool_runner`.

### 21 November 2025

* Blok konten hasil pencarian kini tersedia di Amazon Bedrock tanpa memerlukan header beta. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results).

### 19 November 2025

* Kami telah meluncurkan **platform dokumentasi baru** di [platform.claude.com/docs](https://platform.claude.com/docs). Dokumentasi kami kini berada berdampingan dengan Claude Console, memberikan pengalaman developer yang terpadu. Situs dokumentasi sebelumnya di docs.claude.com akan dialihkan ke lokasi baru.

### 18 November 2025

* Kami telah meluncurkan **Claude di Microsoft Foundry**, menghadirkan model Claude bagi pelanggan Azure dengan penagihan Azure dan autentikasi OAuth. Akses Messages API lengkap termasuk "extended thinking" (pemikiran diperpanjang), "prompt caching" (caching prompt) (5 menit dan 1 jam), dukungan PDF, Files API, Agent Skills, dan "tool use" (penggunaan alat). Pelajari lebih lanjut di [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

### 14 November 2025

* Kami telah meluncurkan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) dalam beta publik, yang memberikan jaminan kesesuaian skema untuk respons Claude. Gunakan output JSON untuk respons data terstruktur atau penggunaan alat ketat (strict tool use) untuk input alat yang tervalidasi. Tersedia untuk Claude Sonnet 4.5 dan Claude Opus 4.1. Untuk mengaktifkannya, gunakan header beta `structured-outputs-2025-11-13`.

### 28 Oktober 2025

* Kami mengumumkan penghentian model Claude Sonnet 3.7. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).
* Kami telah menghentikan model-model Claude Sonnet 3.5. Semua permintaan ke model-model ini kini akan mengembalikan error.
* Kami telah memperluas context editing dengan pembersihan blok thinking (`clear_thinking_20251015`), yang memungkinkan pengelolaan otomatis blok thinking. Pelajari lebih lanjut di [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing).

### 16 Oktober 2025

* Kami telah meluncurkan [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (beta `skills-2025-10-02`), cara baru untuk memperluas kemampuan Claude. Skills adalah folder terorganisir berisi instruksi, skrip, dan sumber daya yang dimuat Claude secara dinamis untuk melakukan tugas khusus. Rilis awal mencakup:

  * **Skills yang dikelola Anthropic**: Skills siap pakai untuk bekerja dengan file PowerPoint (.pptx), Excel (.xlsx), Word (.docx), dan PDF
  * **Skills Kustom**: Unggah Skills Anda sendiri melalui Skills API (endpoint `/v1/skills`) untuk mengemas keahlian domain dan alur kerja organisasi
  * Skills memerlukan [alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan
  * Pelajari lebih lanjut di [Agent Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview) dan [referensi API](https://platform.claude.com/docs/id/api/skills/create)

### 15 Oktober 2025

* Kami telah meluncurkan [Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5), model Haiku kami yang tercepat dan paling cerdas dengan performa mendekati frontier. Ideal untuk aplikasi real-time, pemrosesan volume tinggi, dan deployment yang sensitif terhadap biaya yang memerlukan penalaran yang kuat. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models).

### 29 September 2025

* Kami telah meluncurkan [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), model terbaik kami untuk agen kompleks dan coding, dengan kecerdasan tertinggi di sebagian besar tugas. Pelajari lebih lanjut di [ikhtisar model](https://platform.claude.com/docs/id/models/overview).
* Kami telah memperkenalkan [harga endpoint global](https://platform.claude.com/docs/id/about-claude/pricing#cloud-platform-pricing) untuk Amazon Bedrock dan Vertex AI. Harga Claude API (1P) tidak terpengaruh.
* Kami telah memperkenalkan stop reason baru `model_context_window_exceeded` yang memungkinkan Anda meminta token maksimum yang dimungkinkan tanpa menghitung ukuran input. Pelajari lebih lanjut di [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* Kami telah meluncurkan alat memori dalam versi beta, yang memungkinkan Claude menyimpan dan merujuk informasi lintas percakapan. Pelajari lebih lanjut di [Alat memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool).
* Kami telah meluncurkan context editing dalam versi beta, yang menyediakan strategi untuk mengelola konteks percakapan secara otomatis. Rilis awal mendukung pembersihan hasil dan panggilan alat yang lebih lama saat mendekati batas token. Pelajari lebih lanjut di [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing).

### 17 September 2025

* Kami telah meluncurkan tool helpers dalam versi beta untuk SDK Python dan TypeScript, yang menyederhanakan pembuatan dan eksekusi alat dengan validasi input yang type-safe dan tool runner untuk penanganan alat otomatis dalam percakapan. Untuk detailnya, lihat dokumentasi untuk [SDK Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md) dan [SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers).

### 16 September 2025

* Kami telah menyatukan penawaran developer kami di bawah merek Claude. Anda akan melihat penamaan dan URL yang diperbarui di seluruh platform dan dokumentasi kami, tetapi **antarmuka developer kami akan tetap sama**. Berikut beberapa perubahan penting:

  * Claude Console ([console.anthropic.com](https://console.anthropic.com)) → Claude Console ([platform.claude.com](https://platform.claude.com)). Console akan tersedia di kedua URL hingga 12 Januari 2026. Setelah tanggal tersebut, [console.anthropic.com](https://console.anthropic.com) akan secara otomatis dialihkan ke [platform.claude.com](https://platform.claude.com).
  * Anthropic Docs ([docs.anthropic.com](https://docs.anthropic.com)) → Claude Docs ([docs.claude.com](https://docs.claude.com))
  * Anthropic Help Center ([support.anthropic.com](https://support.anthropic.com)) → Claude Help Center ([support.claude.com](https://support.claude.com))
  * Endpoint API, header, variabel lingkungan, dan SDK tetap sama. Integrasi Anda yang sudah ada akan terus berfungsi tanpa perubahan apa pun.

### 10 September 2025

* Kami telah meluncurkan alat web fetch dalam versi beta, yang memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan. Pelajari lebih lanjut di [Alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool).
* Kami telah meluncurkan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api), yang memungkinkan organisasi mengakses metrik penggunaan harian teragregasi untuk Claude Code secara programatik, termasuk metrik produktivitas, statistik penggunaan alat, dan data biaya.

### 8 September 2025

* Kami meluncurkan versi beta dari [SDK C#](https://github.com/anthropics/anthropic-sdk-csharp).

### 5 September 2025

* Kami telah meluncurkan [grafik "rate limit" (batas laju)](https://platform.claude.com/docs/id/api/rate-limits#monitoring-your-rate-limits-in-the-console) di halaman [Usage](https://console.anthropic.com/settings/usage) Console, yang memungkinkan Anda memantau penggunaan batas laju API dan tingkat caching Anda dari waktu ke waktu.

### 3 September 2025

* Kami telah meluncurkan dukungan untuk dokumen yang dapat dikutip dalam hasil alat di sisi klien. Pelajari lebih lanjut di [Menangani panggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls).

### 2 September 2025

* Kami telah meluncurkan v2 dari [Alat Eksekusi Kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, menggantikan alat asli yang hanya mendukung Python dengan eksekusi perintah Bash dan kemampuan manipulasi file langsung, termasuk menulis kode dalam bahasa lain.

### 27 Agustus 2025

* Kami meluncurkan versi beta dari [SDK PHP](https://github.com/anthropics/anthropic-sdk-php).

### 26 Agustus 2025

* Kami telah meningkatkan batas laju pada [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) untuk Claude Sonnet 4 di Claude API.
* Jendela konteks 1 juta token kini tersedia di Vertex AI. Untuk informasi lebih lanjut, lihat [Claude di Vertex AI](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai).

### 19 Agustus 2025

* Request ID kini disertakan langsung dalam body respons error di samping header `request-id` yang sudah ada. Pelajari lebih lanjut di [Error](https://platform.claude.com/docs/id/api/errors#error-shapes).

### 18 Agustus 2025

* Kami telah merilis [Usage & Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api), yang memungkinkan administrator memantau data penggunaan dan biaya organisasi mereka secara programatik.
* Kami telah menambahkan endpoint baru ke Admin API untuk mengambil informasi organisasi. Untuk detailnya, lihat [referensi Admin API Info Organisasi](https://platform.claude.com/docs/id/api/admin-api/organization/get-me).

### 13 Agustus 2025

* Kami mengumumkan penghentian model-model Claude Sonnet 3.5 (`claude-3-5-sonnet-20240620` dan `claude-3-5-sonnet-20241022`). Model-model ini akan dihentikan pada 28 Oktober 2025. Kami merekomendasikan migrasi ke Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) untuk performa dan kemampuan yang lebih baik. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).
* Durasi cache 1 jam untuk caching prompt tidak lagi memerlukan header beta. Pelajari lebih lanjut di [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration).

### 12 Agustus 2025

* Kami telah meluncurkan dukungan beta untuk [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) di Claude Sonnet 4 pada Claude API dan Amazon Bedrock.

### 11 Agustus 2025

* Beberapa pelanggan mungkin mengalami [error](https://platform.claude.com/docs/id/api/errors) 429 (`rate_limit_error`) setelah peningkatan tajam dalam penggunaan API karena batas akselerasi pada API. Sebelumnya, error 529 (`overloaded_error`) akan terjadi dalam skenario serupa.

### 8 Agustus 2025

* Blok konten hasil pencarian telah keluar dari versi beta di Claude API dan Vertex AI. Fitur ini memungkinkan kutipan alami untuk aplikasi RAG dengan atribusi sumber yang tepat. Header beta `search-results-2025-06-09` tidak lagi diperlukan. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results).

### 5 Agustus 2025

* Kami telah meluncurkan [Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1), pembaruan inkremental untuk Claude Opus 4 dengan kemampuan yang ditingkatkan dan perbaikan performa.\* Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models).

*\*Opus 4.1 tidak mengizinkan parameter `temperature` dan `top_p` ditentukan secara bersamaan. Harap gunakan salah satu saja.*

### 28 Juli 2025

* Kami telah merilis `text_editor_20250728`, alat editor teks yang diperbarui yang memperbaiki beberapa masalah dari versi sebelumnya dan menambahkan parameter opsional `max_characters` yang memungkinkan Anda mengontrol panjang pemotongan saat melihat file besar.

### 24 Juli 2025

* Kami telah meningkatkan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk Claude Opus 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan berkembang bersama Claude. Untuk pelanggan dengan [batas laju tingkat penggunaan 1-4](https://platform.claude.com/docs/id/api/rate-limits#rate-limits), perubahan ini langsung berlaku pada akun Anda - tidak perlu tindakan apa pun.

### 21 Juli 2025

* Kami telah menghentikan model Claude 2.0, Claude 2.1, dan Claude Sonnet 3. Semua permintaan ke model-model ini kini akan mengembalikan error. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 17 Juli 2025

* Kami telah meningkatkan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk Claude Sonnet 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan berkembang bersama Claude. Untuk pelanggan dengan [batas laju tingkat penggunaan 1-4](https://platform.claude.com/docs/id/api/rate-limits#rate-limits), perubahan ini langsung berlaku pada akun Anda - tidak perlu tindakan apa pun.

### 3 Juli 2025

* Kami telah meluncurkan blok konten hasil pencarian dalam versi beta, yang memungkinkan kutipan alami untuk aplikasi RAG. Alat kini dapat mengembalikan hasil pencarian dengan atribusi sumber yang tepat, dan Claude akan secara otomatis mengutip sumber-sumber ini dalam responsnya - menyamai kualitas kutipan pencarian web. Ini menghilangkan kebutuhan akan solusi sementara berbasis dokumen dalam aplikasi basis pengetahuan kustom. Pelajari lebih lanjut di [Hasil pencarian](https://platform.claude.com/docs/id/build-with-claude/search-results). Untuk mengaktifkan fitur ini, gunakan header beta `search-results-2025-06-09`.

### 30 Juni 2025

* Kami mengumumkan penghentian model Claude Opus 3. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 23 Juni 2025

* Pengguna Console dengan peran Developer kini dapat mengakses halaman [Cost](https://console.anthropic.com/settings/cost). Sebelumnya, peran Developer mengizinkan akses ke halaman [Usage](https://console.anthropic.com/settings/usage), tetapi tidak ke halaman Cost.

### 11 Juni 2025

* Kami telah meluncurkan [fine-grained tool streaming](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) dalam beta publik, fitur yang memungkinkan Claude melakukan streaming parameter penggunaan alat tanpa buffering / validasi JSON. Untuk mengaktifkan fine-grained tool streaming, gunakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `fine-grained-tool-streaming-2025-05-14`.

### 22 Mei 2025

* Kami telah meluncurkan [Claude Opus 4 dan Claude Sonnet 4](https://www.anthropic.com/news/claude-4), model terbaru kami dengan kemampuan pemikiran diperpanjang. Pelajari lebih lanjut di [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models).
* Perilaku default [pemikiran diperpanjang](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) pada model Claude 4 mengembalikan ringkasan dari proses pemikiran lengkap Claude, dengan pemikiran lengkap dienkripsi dan dikembalikan dalam field `signature` pada output blok `thinking`.
* Kami telah meluncurkan [interleaved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) (pemikiran berselang-seling) dalam beta publik, fitur yang memungkinkan Claude berpikir di antara panggilan alat. Untuk mengaktifkan interleaved thinking, gunakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14`.
* Kami telah meluncurkan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dalam beta publik, yang memungkinkan Anda mengunggah file dan mereferensikannya di Messages API dan alat eksekusi kode.
* Kami telah meluncurkan [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, alat yang memungkinkan Claude mengeksekusi kode Python dalam lingkungan sandbox yang aman.
* Kami telah meluncurkan [MCP connector](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) dalam beta publik, fitur yang memungkinkan Anda terhubung ke server MCP jarak jauh langsung dari Messages API.
* Untuk meningkatkan kualitas jawaban dan mengurangi error alat, kami telah mengubah nilai default untuk parameter [nucleus sampling](https://en.wikipedia.org/wiki/Top-p_sampling) `top_p` di Messages API dari 0,999 menjadi 0,99 untuk semua model. Untuk mengembalikan perubahan ini, atur `top_p` ke 0,999. Selain itu, saat pemikiran diperpanjang diaktifkan, Anda kini dapat mengatur `top_p` ke nilai antara 0,95 dan 1.
* [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami telah berpindah dari beta ke rilis stabil pertamanya.
* Kami telah menyertakan granularitas tingkat menit dan jam pada halaman [Usage](https://console.anthropic.com/settings/usage) Console bersama dengan tingkat error 429 di halaman Usage.

### 21 Mei 2025

* [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby) kami telah berpindah dari beta ke rilis stabil pertamanya.

### 7 Mei 2025

* Kami telah meluncurkan alat pencarian web di API, yang memungkinkan Claude mengakses informasi terkini dari web. Pelajari lebih lanjut di [Alat pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool).

### 1 Mei 2025

* Cache control kini harus ditentukan langsung di blok `content` induk dari `tool_result` dan `document.source`. Untuk kompatibilitas mundur, jika cache control terdeteksi pada blok terakhir di `tool_result.content` atau `document.source.content`, cache control tersebut akan secara otomatis diterapkan ke blok induk. Cache control pada blok lain mana pun di dalam `tool_result.content` dan `document.source.content` akan menghasilkan error validasi.

### 9 April 2025

* Kami meluncurkan versi beta dari [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby).

### 31 Maret 2025

* [SDK Java](https://github.com/anthropics/anthropic-sdk-java) kami telah berpindah dari beta ke rilis stabil pertamanya.
* Kami telah memindahkan [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami dari alpha ke beta.

### 27 Februari 2025

* Kami telah menambahkan blok sumber URL untuk gambar dan PDF di Messages API. Anda kini dapat mereferensikan gambar dan PDF langsung melalui URL alih-alih harus mengenkodenya dengan base64. Pelajari lebih lanjut di [Vision](https://platform.claude.com/docs/id/build-with-claude/vision) dan [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).
* Kami telah menambahkan dukungan untuk opsi `none` pada parameter `tool_choice` di Messages API yang mencegah Claude memanggil alat apa pun. Selain itu, Anda tidak lagi diwajibkan menyediakan `tools` apa pun saat menyertakan blok `tool_use` dan `tool_result`.
* Kami telah meluncurkan endpoint API yang kompatibel dengan OpenAI, yang memungkinkan Anda menguji model Claude hanya dengan mengubah kunci API, base URL, dan nama model Anda di integrasi OpenAI yang sudah ada. Lapisan kompatibilitas ini mendukung fungsionalitas inti chat completions. Pelajari lebih lanjut di [Kompatibilitas SDK OpenAI](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk).

### 24 Februari 2025

* Kami telah meluncurkan [Claude Sonnet 3.7](https://www.anthropic.com/news/claude-3-7-sonnet), model kami yang paling cerdas sejauh ini. Claude Sonnet 3.7 dapat menghasilkan respons hampir instan atau menunjukkan pemikiran diperpanjangnya langkah demi langkah. Satu model, dua cara berpikir. Pelajari lebih lanjut tentang semua model Claude di [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models).

* Kami telah menambahkan dukungan vision ke Claude Haiku 3.5, yang memungkinkan model menganalisis dan memahami gambar.

* Kami telah merilis implementasi penggunaan alat yang hemat token, yang meningkatkan performa keseluruhan saat menggunakan alat dengan Claude. Pelajari lebih lanjut di [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

* Kami telah mengubah temperature default di [Console](https://console.anthropic.com/workbench) untuk prompt baru dari 0 menjadi 1 agar konsisten dengan temperature default di API. Prompt tersimpan yang sudah ada tidak berubah.

* Kami telah merilis versi terbaru dari alat-alat kami yang memisahkan alat text edit dan bash dari "system prompt" (prompt sistem) computer use:

  * `bash_20250124`: Fungsionalitas yang sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `text_editor_20250124`: Fungsionalitas yang sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `computer_20250124`: Alat computer use yang diperbarui dengan opsi perintah baru termasuk "hold\_key", "left\_mouse\_down", "left\_mouse\_up", "scroll", "triple\_click", dan "wait". Alat ini memerlukan header anthropic-beta "computer-use-2025-01-24". Pelajari lebih lanjut di [Penggunaan alat dengan Claude](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

### 10 Februari 2025

* Kami telah menambahkan header respons `anthropic-organization-id` ke semua respons API. Header ini menyediakan ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan.

### 31 Januari 2025

* Kami telah memindahkan [SDK Java](https://github.com/anthropics/anthropic-sdk-java) kami dari alpha ke beta.

### 23 Januari 2025

* Kami telah meluncurkan kemampuan kutipan (citations) di API, yang memungkinkan Claude memberikan atribusi sumber untuk informasi. Pelajari lebih lanjut di [Kutipan](https://platform.claude.com/docs/id/build-with-claude/citations).
* Kami telah menambahkan dukungan untuk dokumen teks biasa dan dokumen konten kustom di Messages API.

### 21 Januari 2025

* Kami mengumumkan penghentian model Claude 2, Claude 2.1, dan Claude Sonnet 3. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 15 Januari 2025

* Kami telah memperbarui [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) agar lebih mudah digunakan. Kini, saat Anda menetapkan breakpoint cache, kami akan secara otomatis membaca dari prefiks terpanjang Anda yang telah di-cache sebelumnya.
* Anda kini dapat menaruh kata-kata di mulut Claude saat menggunakan alat.

### 10 Januari 2025

* Kami telah mengoptimalkan dukungan untuk [caching prompt di Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#using-prompt-caching-with-message-batches) untuk meningkatkan tingkat cache hit.

### 19 Desember 2024

* Kami telah menambahkan dukungan untuk [endpoint delete](https://platform.claude.com/docs/id/api/deleting-message-batches) di Message Batches API.

### 17 Desember 2024

Fitur-fitur berikut kini tersedia di Claude API tanpa header beta:

* [Models API](https://platform.claude.com/docs/id/api/models/list): Kueri model yang tersedia, validasi ID model, dan resolusi [alias model](https://platform.claude.com/docs/id/models/overview) ke ID model kanonisnya.
* [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing): Proses batch pesan dalam jumlah besar secara asinkron dengan 50% dari biaya API standar.
* [Token counting API](https://platform.claude.com/docs/id/build-with-claude/token-counting): Hitung jumlah token untuk Messages sebelum mengirimkannya ke Claude.
* [Caching Prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching): Kurangi biaya hingga 90% dan latensi hingga 80% dengan melakukan caching dan menggunakan kembali konten prompt.
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support): Proses PDF untuk menganalisis konten teks maupun visual di dalam dokumen.

Kami juga merilis SDK resmi baru:

* [SDK Java](https://github.com/anthropics/anthropic-sdk-java) (alpha)
* [SDK Go](https://github.com/anthropics/anthropic-sdk-go) (alpha)

### 4 Desember 2024

* Kami telah menambahkan kemampuan untuk mengelompokkan berdasarkan kunci API di halaman [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) di [Developer Console](https://console.anthropic.com).
* Kami telah menambahkan dua kolom baru **Last used at** dan **Cost** serta kemampuan untuk mengurutkan berdasarkan kolom apa pun di halaman [API keys](https://console.anthropic.com/settings/keys) di [Developer Console](https://console.anthropic.com).

### 21 November 2024

* Kami telah merilis [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), yang memungkinkan pengguna mengelola sumber daya organisasi mereka secara programatik.

### 20 November 2024

* Kami telah memperbarui batas laju kami untuk Messages API. Kami telah mengganti batas laju token per menit dengan batas laju token input dan output per menit yang baru. Baca lebih lanjut di [Batas laju](https://platform.claude.com/docs/id/api/rate-limits).
* Kami telah menambahkan dukungan untuk [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) di [Workbench](https://console.anthropic.com/workbench).

### 13 November 2024

* Kami telah menambahkan dukungan PDF untuk semua model Claude Sonnet 3.5. Baca lebih lanjut di [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).

### 6 November 2024

* Kami telah menghentikan model Claude 1 dan Instant. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 4 November 2024

* [Claude Haiku 3.5](https://www.anthropic.com/claude/haiku) kini tersedia di Claude API sebagai model khusus teks.

### 1 November 2024

* Kami telah menambahkan dukungan PDF untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca lebih lanjut di [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support).
* Kami juga telah menambahkan penghitungan token, yang memungkinkan Anda menentukan jumlah total token dalam sebuah Message sebelum mengirimkannya ke Claude. Baca lebih lanjut di [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

### 22 Oktober 2024

* Kami telah menambahkan alat computer use yang didefinisikan Anthropic ke API kami untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca lebih lanjut di [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool).
* Claude Sonnet 3.5, model kami yang paling cerdas sejauh ini, baru saja mendapatkan peningkatan dan kini tersedia di Claude API. Baca lebih lanjut di [dokumentasi Claude Sonnet](https://www.anthropic.com/claude/sonnet).

### 8 Oktober 2024

* Message Batches API kini tersedia dalam versi beta. Proses batch kueri dalam jumlah besar secara asinkron di Claude API dengan biaya 50% lebih rendah. Baca lebih lanjut di [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing).
* Kami telah melonggarkan pembatasan pada urutan giliran `user`/`assistant` di Messages API kami. Pesan `user`/`assistant` yang berurutan akan digabungkan menjadi satu pesan alih-alih menghasilkan error, dan kami tidak lagi mewajibkan pesan input pertama berupa pesan `user`.
* Kami telah menghentikan paket Build dan Scale dan menggantinya dengan rangkaian fitur standar (sebelumnya disebut Build), bersama dengan fitur tambahan yang tersedia melalui tim penjualan. Baca lebih lanjut di [informasi harga API](https://claude.com/platform/api) kami.

### 3 Oktober 2024

* Kami telah menambahkan kemampuan untuk menonaktifkan penggunaan alat paralel di API. Atur `disable_parallel_tool_use: true` di field `tool_choice` untuk memastikan Claude menggunakan paling banyak satu alat. Baca lebih lanjut di [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use).

### 10 September 2024

* Kami telah menambahkan Workspaces ke [Developer Console](https://console.anthropic.com). Workspaces memungkinkan Anda menetapkan batas pengeluaran atau batas laju kustom, mengelompokkan kunci API, melacak penggunaan per proyek, dan mengontrol akses dengan peran pengguna. Baca lebih lanjut di [postingan blog](https://www.anthropic.com/news/workspaces) kami.

### 4 September 2024

* Kami mengumumkan penghentian model-model Claude 1. Baca lebih lanjut di [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### 22 Agustus 2024

* Kami telah menambahkan dukungan untuk penggunaan SDK di browser dengan mengembalikan header CORS dalam respons API. Atur `dangerouslyAllowBrowser: true` dalam instansiasi SDK untuk mengaktifkan fitur ini.

### 19 Agustus 2024

* Output 8.192 token pada Claude Sonnet 3.5 telah keluar dari versi beta dan tidak lagi memerlukan header `max-tokens-3-5-sonnet-2024-07-15`.

### 14 Agustus 2024

* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) kini tersedia sebagai fitur beta di Claude API. Lakukan caching dan gunakan kembali prompt untuk mengurangi latensi hingga 80% dan biaya hingga 90%.

### 15 Juli 2024

* Hasilkan output hingga 8.192 token dari Claude Sonnet 3.5 dengan header baru `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15`.

### 9 Juli 2024

* Hasilkan kasus uji secara otomatis untuk prompt Anda menggunakan Claude di [Developer Console](https://console.anthropic.com).
* Bandingkan output dari prompt yang berbeda secara berdampingan dalam mode perbandingan output baru di [Developer Console](https://console.anthropic.com).

### 27 Juni 2024

* Lihat penggunaan dan penagihan API yang dirinci berdasarkan jumlah dolar, jumlah token, dan kunci API di tab [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) baru di [Developer Console](https://console.anthropic.com).
* Lihat batas laju API Anda saat ini di tab [Rate Limits](https://console.anthropic.com/settings/limits) baru di [Developer Console](https://console.anthropic.com).

### 20 Juni 2024

* [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet), model kami yang paling cerdas sejauh ini, kini tersedia di Claude API, Amazon Bedrock, dan Vertex AI.

### 30 Mei 2024

* [Penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) telah keluar dari versi beta di Claude API, Amazon Bedrock, dan Vertex AI, tanpa memerlukan header beta.

### 10 Mei 2024

* Alat prompt generator kami kini tersedia di [Developer Console](https://console.anthropic.com). Prompt Generator memudahkan Anda memandu Claude untuk menghasilkan prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda. Baca lebih lanjut di [postingan blog](https://www.anthropic.com/news/prompt-generator) kami.
