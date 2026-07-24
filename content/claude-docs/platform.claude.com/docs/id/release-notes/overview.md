---
source: platform
url: https://platform.claude.com/docs/id/release-notes/overview
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: d36840ffa2985a02f08c11f4997d25c7fa0eeb492a6f49d3978c111243a73df4
---

# Catatan rilis Claude Platform

Pembaruan untuk Claude Platform, termasuk Claude API, SDK klien, dan Claude Console.

---

<Tip>
  Untuk catatan rilis tentang Claude Apps, lihat [Catatan rilis untuk Claude Apps di Claude Help Center](https://support.claude.com/en/articles/12138966-release-notes).

  Untuk pembaruan pada Claude Code, lihat [CHANGELOG.md lengkap](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) di repositori `claude-code`.
</Tip>

### 22 Juli 2026

* Anda sekarang dapat mengatur tingkat `effort` pada konfigurasi model agen Claude Managed Agents. Teruskan `effort` di dalam objek `model` saat Anda [membuat agen](/docs/id/managed-agents/agent-setup#create-an-agent). Lihat [Tingkat effort](/docs/id/build-with-claude/effort#effort-levels) untuk mengetahui fungsi setiap tingkat.
* Webhook untuk Claude Managed Agents sekarang mencakup siklus hidup environment dan memory store: empat tipe event `environment.*` dan tiga tipe event `memory_store.*`. Anda dapat bereaksi terhadap perubahan siklus hidup environment dan memory store tanpa polling. Lihat tab Environment events dan Memory store events di [Berlangganan webhook](/docs/id/managed-agents/webhooks#supported-event-types).
* Saat membuat sesi Claude Managed Agents, Anda sekarang dapat [mengisinya dengan event awal](/docs/id/managed-agents/sessions#seed-the-session-with-initial-events). Teruskan `initial_events` pada `POST /v1/sessions` dengan hingga 50 event `user.message` dan `user.define_outcome`. Daftar yang tidak kosong memulai loop agen dalam panggilan yang sama, sehingga Anda tidak memerlukan permintaan send-events terpisah untuk memulai pekerjaan.
* Field `version` sekarang opsional saat [memperbarui agen Claude Managed Agents](/docs/id/managed-agents/agent-setup#update-an-agent). Sediakan field ini untuk optimistic concurrency (ketidakcocokan mengembalikan error 409), atau hilangkan untuk menerapkan pembaruan tanpa syarat. Lihat [Semantik pembaruan](/docs/id/managed-agents/agent-setup#update-semantics).
* Stream event thread sesi Claude Managed Agents sekarang mendukung [event delta](/docs/id/managed-agents/events-and-streaming#event-deltas). `GET /v1/sessions/{session_id}/threads/{thread_id}/stream` menerima parameter kueri `event_deltas[]` yang sama dengan stream tingkat sesi, sehingga Anda dapat melihat pratinjau teks subagen saat model menghasilkannya. Sebuah koneksi hanya menampilkan pratinjau thread yang sedang dibacanya. Lihat [Pratinjau event thread sesi](/docs/id/managed-agents/events-and-streaming#preview-session-thread-events).

### 17 Juli 2026

* **Workbench** lama ([platform.claude.com/workbench](https://platform.claude.com/workbench)) di Claude Console akan dihentikan dengan akses berakhir pada 17 Agustus 2026. Prompt tersimpan, variabel, dan eval tidak didukung di [Workbench](https://platform.claude.com/playground) yang diperbarui. Anda dapat mengekspor data apa pun yang ingin Anda simpan dari banner dan di bawah **Organizational Settings** Anda. Untuk informasi lebih lanjut, lihat [Bagaimana cara menggunakan Workbench?](https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench) di Claude Help Center.
* API alat prompt eksperimental untuk menghasilkan, meningkatkan, dan membuat templat prompt (`/v1/experimental/generate_prompt`, `/v1/experimental/improve_prompt`, dan `/v1/experimental/templatize_prompt`) akan dipensiunkan bersama dengan Workbench pada 17 Agustus 2026. Setelah penghapusan, permintaan ke endpoint ini akan mengembalikan error.

### 15 Juli 2026

* [Pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages) tersedia di Claude Fable 5, Claude Mythos 5, dan Claude Opus 4.8, pada Claude API, [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai). Tidak diperlukan header beta. Ini mengoreksi catatan ketersediaan sebelumnya.

### 14 Juli 2026

* Anda sekarang dapat mengelola orang-orang di organisasi **Claude Enterprise** (claude.ai) Anda dengan [Admin API](/docs/id/api/admin), dalam versi beta untuk semua organisasi Claude Enterprise: mencantumkan anggota dan mencarinya berdasarkan alamat email, mengubah peran anggota, menghapus anggota, mengirim dan menarik undangan, mengelola grup dan keanggotaannya, serta membaca peran kustom. Permintaan grup dan peran kustom memerlukan header beta `anthropic-beta: ce-user-management-2026-07-13`; permintaan anggota dan undangan tidak memerlukan header beta. Kunci Admin API dengan cakupan `read:org_audit` juga dapat memanggil setiap endpoint `GET` manajemen pengguna. Lihat [Manajemen pengguna](/docs/id/manage-claude/user-management).

### 10 Juli 2026

* [Dreams](/docs/id/managed-agents/dreams) (pratinjau riset) sekarang mendukung Claude Fable 5 dan Claude Sonnet 5. Lihat [Model yang didukung](/docs/id/managed-agents/dreams#limits).
* Kami telah memperluas dokumentasi [Access Transparency](/docs/id/manage-claude/access-transparency) untuk event `cmek_preserve` dengan contoh filter, contoh payload event, dan dua kode alasan preservasi (`policy_violation_investigation`, `csae_report`). Dokumentasi sekarang juga mengklarifikasi bahwa event preservasi ditulis baik preservasi dimulai oleh peninjau manusia maupun oleh pipeline keamanan otomatis. Lihat [Preservasi konten CMEK](/docs/id/manage-claude/access-transparency#cmek-content-preservation).

### 8 Juli 2026

* Anda sekarang dapat mengatur masa kedaluwarsa saat membuat kunci API (API key) atau kunci Admin API di [Claude Console](https://platform.claude.com/settings/keys). Pilih preset, durasi kustom, atau **Never**. Untuk kunci dengan masa pakai setidaknya 7 hari, Anthropic mengirim email kepada pembuatnya sebelum kedaluwarsa. Kunci yang sudah ada tidak terpengaruh. Admin API melaporkan masa kedaluwarsa setiap kunci di field [`expires_at`](/docs/id/api/admin/api_keys/list). Lihat [Autentikasi](/docs/id/manage-claude/authentication#key-expiration).

### 2 Juli 2026

* Kami telah menambahkan header beta `agent-memory-2026-07-22`, yang mengubah perilaku [pencantuman memori](/docs/id/managed-agents/memory#list-memories) (`GET /v1/memory_stores/{memory_store_id}/memories`): hasil dikembalikan dalam urutan stabil yang ditentukan server dan parameter `order_by` serta `order` diabaikan; `depth` hanya menerima `0`, `1`, atau dihilangkan (nilai lain mengembalikan error `400`); dan `path_prefix` harus diakhiri dengan `/` dan mencocokkan segmen path utuh alih-alih substring. Kursor halaman yang diterbitkan tanpa header ini tidak valid dengannya, jadi mulai ulang dari halaman pertama saat Anda mengadopsinya. Pada endpoint memory store, `agent-memory-2026-07-22` menggantikan `managed-agents-2026-04-01`; mengirim keduanya mengembalikan error `400`. Pada 22 Juli 2026, header `managed-agents-2026-04-01` mengadopsi perilaku daftar yang sama. Lihat [Header beta](/docs/id/api/beta-headers#endpoint-specific-headers).
* SDK Python (0.116.0), TypeScript (0.110.0), Go (1.56.0), Java (2.48.0), Ruby (1.55.0), PHP (0.36.0), C# (12.35.0), dan CLI (1.16.0) sekarang mengirim `agent-memory-2026-07-22` pada semua panggilan memory store alih-alih `managed-agents-2026-04-01`. Jika kode Anda meneruskan `betas` secara eksplisit pada panggilan memory store, ganti `managed-agents-2026-04-01` dengan `agent-memory-2026-07-22` di sana alih-alih menambahkan nilai kedua.

### 1 Juli 2026

* Kami telah memulihkan akses ke Claude Fable 5 dan Claude Mythos 5. Lihat [pernyataan kami](https://www.anthropic.com/news/redeploying-fable-5) untuk informasi lebih lanjut.

### 30 Juni 2026

* Kami telah meluncurkan **Claude Sonnet 5** (`claude-sonnet-5`), generasi berikutnya dari keluarga model Sonnet kami, dengan harga perkenalan $2 / $10 per MTok hingga 31 Agustus 2026 (standar $3 / $15 setelahnya). Claude Sonnet 5 mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), maksimum 128k token output, dan rangkaian alat serta fitur platform yang sama dengan Claude Sonnet 4.6, kecuali [Priority Tier](/docs/id/api/service-tiers#supported-models), yang tidak tersedia di Claude Sonnet 5. Tiga perubahan perilaku berlaku saat bermigrasi: [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) sekarang aktif secara default; extended thinking (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) dihapus dan mengembalikan error 400 (fitur ini telah ditandai usang di Sonnet 4.6); dan mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default mengembalikan error 400. Claude Sonnet 5 juga menggunakan tokenizer baru yang menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Lihat [Apa yang baru di Claude Sonnet 5](/docs/id/about-claude/models/whats-new-sonnet-5) untuk detail dan panduan migrasi. Untuk perbedaan perilaku dan pola prompting khusus model, lihat [Prompting Claude Sonnet 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5).
* Stream event sesi Claude Managed Agents sekarang mendukung [event delta](/docs/id/managed-agents/events-and-streaming#event-deltas). Ikut serta dengan parameter kueri `event_deltas[]` pada `GET /v1/sessions/{session_id}/events/stream`. Event `event_start` dan `event_delta` menampilkan pratinjau teks pesan agen saat dihasilkan, sebelum event `agent.message` lengkap tiba.
* [Pencantuman sesi](/docs/id/managed-agents/session-operations#listing-sessions) untuk Claude Managed Agents sekarang mendukung paginasi mundur. `GET /v1/sessions` mengembalikan kursor `prev_page` bersama `next_page`; teruskan sebagai parameter `page` untuk kembali ke halaman sebelumnya. Lihat [Paginasi](/docs/id/api/overview#pagination).
* Saat membuat sesi Claude Managed Agents, Anda sekarang dapat [menimpa konfigurasi agen untuk sesi tersebut](/docs/id/managed-agents/sessions#override-agent-configuration-for-a-session). Teruskan `agent` dengan `type: "agent_with_overrides"` untuk mengganti model, prompt sistem, alat, server MCP, atau skill untuk satu sesi. Agen itu sendiri tidak berubah.
* Vault Claude Managed Agents sekarang mendukung pengaturan `injection_location` pada [kredensial variabel lingkungan](/docs/id/managed-agents/vaults#add-a-credential) (tab Environment variable). Pengaturan ini mengontrol apakah nilai kredensial disubstitusikan, saat egress, ke dalam header permintaan keluar agen, body permintaan, atau keduanya.
* Webhook untuk Claude Managed Agents sekarang mencakup siklus hidup agen, deployment, dan deployment run. Anda dapat bereaksi terhadap versi agen yang baru dipublikasikan, deployment yang dijeda, atau scheduled run yang gagal tanpa polling. Lihat tab Agent events, Deployment events, dan Deployment run events di [Berlangganan webhook](/docs/id/managed-agents/webhooks#supported-event-types).

### 29 Juni 2026

* Kami telah menghapus [mode cepat](/docs/id/build-with-claude/fast-mode) (fast mode) untuk Claude Opus 4.6. Permintaan ke `claude-opus-4-6` dengan `speed: "fast"` tidak lagi berjalan dengan kecepatan cepat atau harga premium: permintaan tersebut berjalan dengan kecepatan standar, ditagih dengan tarif standar, dan tidak mengembalikan error. Field `usage.speed` pada respons melaporkan kecepatan yang digunakan. Untuk terus menggunakan mode cepat, migrasikan ke [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide). Baca selengkapnya di [Mode cepat](/docs/id/build-with-claude/fast-mode#supported-models).

### 26 Juni 2026

* Kami telah menaikkan [batas laju](/docs/id/api/rate-limits) (rate limit) di seluruh Claude API. Batas laju Claude Sonnet dan Claude Haiku sekarang setara dengan Claude Opus di setiap tingkat penggunaan, dan tingkat penggunaan telah dikonsolidasikan menjadi tiga: Start, Build, dan Scale. Sebagian besar organisasi berpindah ke tingkat yang lebih tinggi, tidak ada organisasi yang menerima batas lebih rendah dari sebelumnya, dan tidak diperlukan tindakan apa pun. Anda dapat melihat tingkat dan batas Anda saat ini di [Claude Console](/settings/limits).

### 25 Juni 2026

* Kami telah menandai [mode cepat](/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.7 sebagai usang (deprecated), dengan penghapusan pada 24 Juli 2026. Setelah penghapusan, permintaan ke `claude-opus-4-7` dengan `speed: "fast"` akan mengembalikan error. Migrasikan ke mode cepat untuk Claude Opus 4.8. Baca selengkapnya di [Mode cepat](/docs/id/build-with-claude/fast-mode#supported-models).

### 22 Juni 2026

* **MCP tunnels** (pratinjau riset): API manajemen berpindah dari `/v1/organizations/tunnels` pada Admin API ke `/v1/tunnels` pada Claude API. Permukaan baru menggunakan header `anthropic-beta: mcp-tunnels-2026-06-22` dan cakupan WIF `workspace:manage_tunnels`. Permukaan sebelumnya tetap tersedia selama jendela migrasi. Lihat [referensi Tunnels API](/docs/id/api/beta/tunnels).

### 18 Juni 2026

* SDK Python, TypeScript, Go, Java, Ruby, PHP, dan C# sekarang menyertakan dukungan untuk `code_execution_20260120`, versi [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) yang menambahkan persistensi state REPL dan merupakan versi minimum untuk [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling). Untuk mengadopsinya, atur `type` alat ke `code_execution_20260120`; tidak diperlukan header beta. Versi ini tersedia di Claude Fable 5, Claude Mythos 5, Claude Opus 4.5 dan yang lebih baru, serta Claude Sonnet 4.5 dan yang lebih baru; lihat [tabel kompatibilitas model](/docs/id/agents-and-tools/tool-use/code-execution-tool#model-compatibility).

### 15 Juni 2026

* Kami telah memensiunkan model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`). Semua permintaan ke model-model ini sekarang akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) dan [Claude Opus 4.8](/docs/id/about-claude/models/overview#latest-models-comparison) secara berurutan. Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 11 Juni 2026

* [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) sekarang mendukung `code_execution_20260521`, yang mengungkapkan batas waktu eksekusi 90 detik per sel dalam deskripsi alat sehingga Claude dapat menganggarkan sel yang berjalan lama. Tidak diperlukan header beta.
* [Alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) dan [alat pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool) sekarang mendukung `web_search_20260318` dan `web_fetch_20260318`, menambahkan parameter `response_inclusion` untuk menghapus blok hasil yang telah dikonsumsi dari respons API untuk alur kerja agentik. Tidak diperlukan header beta.

### 10 Juni 2026

* Endpoint `GET /v1/environments/{id}/work`, yang mencantumkan pekerjaan tertunda untuk [sandbox yang dihosting sendiri](/docs/id/managed-agents/self-hosted-sandboxes), sekarang tersedia di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Aksi IAM untuk Claude Platform on AWS](/docs/id/api/claude-platform-on-aws-iam-actions) untuk aksi `GetEnvironment` yang mengotorisasinya.

### 9 Juni 2026

* Kami telah meluncurkan **Claude Fable 5** (`claude-fable-5`), model paling mumpuni yang kami rilis secara luas, bersama **Claude Mythos 5** (`claude-mythos-5`) untuk peserta Project Glasswing. Kedua model mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) secara default, maksimum 128k token output, dan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) yang selalu aktif. Lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) untuk kemampuan, perubahan API, dan ketersediaan.
* Claude Fable 5 dan Claude Mythos 5 menggunakan tokenizer yang diperkenalkan dengan Claude Opus 4.7. Dibandingkan dengan model sebelum Claude Opus 4.7, teks yang sama menghasilkan sekitar 30% lebih banyak token. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting#token-counts-on-claude-fable-5) dengan `model: "claude-fable-5"` untuk mengukur prompt Anda dengan tokenizer baru.
* Claude Fable 5 menjalankan pengklasifikasi keamanan pada permintaan dan selama pembuatan respons. Ketika pengklasifikasi menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"`. Anda tidak ditagih untuk permintaan yang ditolak sebelum output apa pun dihasilkan. Parameter `fallbacks` yang bersifat opt-in (dalam versi beta di Claude API dan Claude Platform on AWS; tidak didukung di Message Batches API) menjalankan ulang permintaan yang ditolak pada model lain, ditagih dengan tarif model fallback. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).
* Field [`stop_details.category`](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan sekarang menyertakan `"reasoning_extraction"` di Claude Fable 5, yang dikembalikan ketika permintaan diblokir berdasarkan pembatasan Ketentuan Layanan Anthropic tentang rekayasa balik atau duplikasi output model. Kategori `"cyber"` dan `"bio"` yang sudah ada tidak berubah. Tidak diperlukan header beta.
* Di Claude Fable 5 dan Claude Mythos 5, [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) adalah satu-satunya mode berpikir: `thinking: {"type": "disabled"}` tidak didukung, dan anggaran pemikiran diperpanjang manual serta prefill asisten tidak didukung (keduanya mengembalikan error 400). Lihat [Migrasi dari Claude Mythos Preview ke Claude Mythos 5](/docs/id/about-claude/models/migration-guide#migrating-from-claude-mythos-preview).
* Di Claude Fable 5 dan Claude Mythos 5, `thinking.display` secara default bernilai `"omitted"`, sama seperti Claude Opus 4.8, Claude Opus 4.7, dan Claude Mythos Preview; atur `display: "summarized"` untuk menerima ringkasan pemikiran yang dapat dibaca. Rantai pemikiran mentah tidak pernah dikembalikan; teruskan kembali blok pemikiran tanpa perubahan dalam percakapan multi-giliran pada model yang sama. Lihat [Output pemikiran di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Claude Fable 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah retensi data nol. Lihat [Persyaratan retensi data khusus model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Claude Managed Agents sekarang mendukung [deployment terjadwal](/docs/id/managed-agents/scheduled-deployments), memungkinkan Anda menjalankan sesi pada jadwal cron tanpa mengelola scheduler Anda sendiri.
* Vault Claude Managed Agents sekarang mendukung [kredensial variabel lingkungan](/docs/id/managed-agents/vaults#add-a-credential), sehingga Anda dapat menyuntikkan rahasia secara aman ke dalam sandbox agen untuk CLI, SDK, dan layanan lain yang mengautentikasi melalui variabel lingkungan.
* Event webhook `session.thread_*` sekarang menyertakan field `session_thread_id` yang mengidentifikasi thread multiagen yang memicu event tersebut.
* Kami telah merilis [paket Swift](/docs/id/cli-sdks-libraries/libraries/apple-foundation-models) dalam versi beta yang menambahkan Claude sebagai `LanguageModel` sisi server dalam framework Foundation Models milik Apple. Panggil Claude melalui API `LanguageModelSession` yang sama dengan model on-device Apple di iOS 27, macOS 27, visionOS 27, dan watchOS 27 (beta).

### 5 Juni 2026

* Kami mengumumkan penghentian dukungan (deprecation) model Claude Opus 4.1 (`claude-opus-4-1-20250805`), dengan pemensiunan di Claude API dijadwalkan pada 5 Agustus 2026. Kami merekomendasikan migrasi ke [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47). Baca selengkapnya di [penghentian dukungan model](/docs/id/about-claude/model-deprecations).

### 2 Juni 2026

* [Alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool) sekarang mendukung parameter `max_tokens` untuk membatasi output model advisor per panggilan, mengurangi latensi dan biaya token output untuk beban kerja yang tidak memerlukan respons advisor dengan panjang penuh. Atur `tools[].max_tokens` pada definisi alat advisor; lihat [Membatasi output advisor](/docs/id/agents-and-tools/tool-use/advisor-tool#capping-advisor-output).
* Di Claude API, Anda tidak lagi ditagih untuk sebuah permintaan ketika permintaan tersebut mengembalikan `stop_reason: "refusal"` tanpa Claude menghasilkan output apa pun. Lihat [Penolakan streaming](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) untuk mendeteksi dan menangani penolakan.

### 29 Mei 2026

* [Webhook](/docs/id/managed-agents/webhooks) Claude Managed Agents, [orkestrasi multiagen](/docs/id/managed-agents/multiagent-orchestration), dan [sandbox yang dihosting sendiri](/docs/id/managed-agents/self-hosted-sandboxes) sekarang tersedia di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws). Lihat [Aksi IAM untuk Claude Platform on AWS](/docs/id/api/claude-platform-on-aws-iam-actions) untuk aksi IAM baru dan kebijakan terkelola `AnthropicSelfHostedEnvironmentAccess`.

### 28 Mei 2026

* Kami telah meluncurkan **Claude Opus 4.8** (claude-opus-4-8), model paling mumpuni kami yang tersedia secara umum. Claude Opus 4.8 mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) secara default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry, maksimum 128k token output, dan rangkaian alat serta fitur platform yang sama dengan Claude Opus 4.7. Lihat [Apa yang baru di Claude Opus 4.8](/docs/id/about-claude/models/whats-new-claude-4-8) untuk peningkatan kemampuan, fitur baru, dan panduan migrasi.
* Kami telah meluncurkan [pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages). Di Claude Opus 4.8, Anda dapat mengirim pesan `role: "system"` setelah giliran pengguna (tunduk pada [aturan penempatan](/docs/id/build-with-claude/mid-conversation-system-messages#limitations)) dalam array `messages`, mempertahankan cache hit prompt ketika instruksi berubah selama sesi yang berjalan lama. Tidak diperlukan header beta.
* Field [`stop_details`](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada respons penolakan sekarang didokumentasikan secara publik; field ini mengembalikan `category` (`cyber`, `bio`, atau `null`) dan `explanation` yang dapat dibaca manusia, sehingga aplikasi Anda dapat mengarahkan kelas penolakan yang berbeda ke langkah berikutnya yang tepat. Tidak diperlukan header beta.
* Di Claude Opus 4.8, [parameter effort](/docs/id/build-with-claude/effort) secara default bernilai `high` di semua permukaan, termasuk Claude Code dan Messages API.
* Di Claude Opus 4.8, panjang prompt minimum yang dapat di-cache untuk [caching prompt](/docs/id/build-with-claude/prompt-caching) adalah 1.024 token, lebih rendah daripada di Claude Opus 4.7.
* Dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) diaktifkan, Claude Opus 4.8 memicu penalaran hanya ketika sebuah giliran membutuhkannya, mengurangi token pemikiran yang terbuang dibandingkan dengan Claude Opus 4.7 pada tingkat effort yang sama.
* Claude Opus 4.8 mendukung [input gambar resolusi tinggi](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga 2576 piksel pada sisi panjang), sama seperti Claude Opus 4.7.
* [Anggaran tugas](/docs/id/build-with-claude/task-budgets) sekarang mendukung Claude Opus 4.8.
* [Alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool) sekarang mendukung Claude Opus 4.8.
* [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) sekarang mendukung Claude Opus 4.8.
* [Mode cepat](/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.8 tersedia sebagai pratinjau riset hanya di Claude API.
* Mengatur parameter sampling `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 4.8, sama seperti di Claude Opus 4.7. Lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide) untuk detailnya.
* Di Claude Code, kami telah memperluas mode Auto ke lebih banyak pengguna untuk tugas yang berjalan lama. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, pengguna paket Max sekarang secara default menggunakan [mode cepat](/docs/id/build-with-claude/fast-mode) di Claude Opus 4.8. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Di Claude Code, Workflows tersedia sebagai pratinjau riset, memungkinkan Anda mendefinisikan dan menjalankan rencana agentik multilangkah. Lihat [dokumentasi Claude Code](https://code.claude.com/docs).
* Kami telah menandai [mode cepat](/docs/id/build-with-claude/fast-mode) untuk Claude Opus 4.6 sebagai usang (deprecated), dengan penghapusan sekitar 30 hari setelah peluncuran. Migrasikan ke mode cepat untuk Claude Opus 4.8 atau Claude Opus 4.7. Baca selengkapnya di [Mode cepat](/docs/id/build-with-claude/fast-mode#supported-models).
* Untuk pembaruan pada claude.ai, Cowork, Claude for Microsoft 365, dan aplikasi Claude lainnya dalam rilis ini, lihat [catatan rilis untuk Claude Apps](https://support.claude.com/en/articles/12138966-release-notes).

### 27 Mei 2026

* Respons Messages API sekarang menyertakan [`usage.output_tokens_details.thinking_tokens`](/docs/id/build-with-claude/extended-thinking#working-with-thinking-budgets), yang melaporkan berapa banyak dari token output yang ditagih merupakan pemikiran diperpanjang. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir. Tidak diperlukan header beta.

### 19 Mei 2026

* [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) sekarang tersedia sebagai pratinjau riset, sehingga Anda dapat terhubung ke server MCP di jaringan privat Anda.
* Sandbox yang dihosting sendiri sekarang tersedia untuk Claude Managed Agents, sebagai alternatif untuk menjalankan eksekusi alat di infrastruktur Anthropic. Lihat [Sandbox yang dihosting sendiri](/docs/id/managed-agents/self-hosted-sandboxes).
* Dengan Claude Managed Agents, Anda sekarang dapat memperbarui konfigurasi server MCP dan alat agen yang terkait dengan sesi aktif.
* Dengan Claude Managed Agents, output besar dari `agent_toolset` dan alat MCP yang melebihi 100K karakter (sekitar 25K token) sekarang secara otomatis dialihkan ke sebuah file di sandbox. Model menerima pratinjau terpotong dengan path file dan dapat membaca konten lengkapnya dari sana.

### 18 Mei 2026

* [Alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) sekarang mengembalikan data pengajuan SEC yang lebih kaya, memudahkan untuk melandaskan agen riset keuangan, analisis laba, dan alur kerja uji tuntas pada sumber primer dengan sitasi.

### 13 Mei 2026

* Kami telah meluncurkan [diagnostik cache](/docs/id/build-with-claude/cache-diagnostics) dalam versi beta publik. Teruskan `diagnostics.previous_message_id` pada permintaan Messages dan API melaporkan `cache_miss_reason` yang menjelaskan di mana prefiks cache prompt menyimpang dari giliran sebelumnya. Sertakan header beta `cache-diagnosis-2026-04-07` dalam permintaan Anda.

### 12 Mei 2026

* [Mode cepat](/docs/id/build-with-claude/fast-mode) (pratinjau riset) sekarang mendukung Claude Opus 4.7. Atur `speed: "fast"` dengan `model: "claude-opus-4-7"` dan header beta `fast-mode-2026-02-01` untuk pembuatan token output yang jauh lebih cepat dengan harga premium. Harga, batas laju, dan akses sama dengan mode cepat Opus 4.6; pelanggan yang tertarik dapat bergabung dengan [daftar tunggu](https://claude.com/fast-mode).

### 11 Mei 2026

* Kami telah meluncurkan **Claude Platform on AWS**, menghadirkan Claude API ke infrastruktur yang dikelola Anthropic yang dapat diakses melalui AWS, dengan penagihan AWS dan autentikasi IAM. Akses Messages API lengkap, Files API, Message Batches API, Claude Managed Agents, Agent Skills, eksekusi kode, dan penggunaan alat melalui endpoint AWS native. Pelajari lebih lanjut di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws).

### 6 Mei 2026

* [Orkestrasi multiagen](/docs/id/managed-agents/multiagent-orchestration) dan [Outcomes](/docs/id/managed-agents/define-outcomes) sekarang dalam versi beta publik di bawah header beta standar `managed-agents-2026-04-01`.
* Penyegaran latar belakang kredensial vault Claude Managed Agents sekarang didukung untuk kredensial `mcp_oauth`. Lihat [Autentikasi dengan vault](/docs/id/managed-agents/vaults).
* Webhook untuk Claude Managed Agents sekarang didukung. Tipe event webhook mencakup event siklus hidup sesi dan vault. Lihat [Berlangganan webhook](/docs/id/managed-agents/webhooks).
* Opsi pemfilteran dan pengurutan tambahan sekarang didukung untuk Claude Managed Agents. Sesi dapat difilter berdasarkan status, dan event dapat difilter berdasarkan tipe. Event sekarang dapat difilter berdasarkan waktu pembuatan.
* [Dreams](/docs/id/managed-agents/dreams) untuk Claude Managed Agents sekarang tersedia sebagai pratinjau riset. Sebuah dream membaca memory store yang ada bersama transkrip sesi sebelumnya dan menghasilkan memory store output yang direorganisasi dengan duplikat digabungkan, entri usang diganti, dan wawasan baru dimunculkan. Endpoint dream dibatasi oleh header beta `dreaming-2026-04-21`. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.

### 4 Mei 2026

* [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) sekarang tersedia secara umum. Autentikasi beban kerja ke Claude API dengan token OIDC berumur pendek dari penyedia identitas Anda sendiri (AWS IAM, Google Cloud, GitHub Actions, Kubernetes, Microsoft Entra ID, Okta, SPIFFE, dan lainnya) alih-alih kunci API statis berumur panjang. Konfigurasikan issuer dan aturan federasi di Claude Console, dan SDK menangani pertukaran serta penyegaran token secara otomatis. Lihat [Autentikasi](/docs/id/manage-claude/authentication).

### 30 April 2026

* Kami telah memensiunkan beta jendela konteks 1M token (`context-1m-2025-08-07`) untuk Claude Sonnet 4.5 dan Claude Sonnet 4. Header beta sekarang tidak berpengaruh pada model-model ini, dan permintaan yang melebihi jendela konteks standar 200k token mengembalikan error. Untuk menggunakan jendela konteks 1M, migrasikan ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) atau [Claude Opus 4.6](/docs/id/about-claude/models/overview#latest-models-comparison), di mana fitur ini tersedia secara umum dengan harga standar tanpa memerlukan header beta.

### 29 April 2026

* Kami telah merilis [skill Claude API](/docs/id/agents-and-tools/agent-skills/claude-api-skill), sebuah [Agent Skill](/docs/id/agents-and-tools/agent-skills/overview) open-source yang memberi Claude materi referensi terkini untuk membangun di atas Messages API dan Claude Managed Agents dalam 8 bahasa. Skill ini dibundel dengan Claude Code dan tersedia di [repositori skill Anthropic](https://github.com/anthropics/skills/tree/main/skills/claude-api).

### 24 April 2026

* Kami telah merilis [Rate Limits API](/docs/id/manage-claude/rate-limits-api), memungkinkan administrator untuk mengkueri batas laju yang dikonfigurasi untuk organisasi dan workspace mereka secara terprogram.

### 23 April 2026

* Memori untuk Claude Managed Agents sekarang dalam versi beta publik di bawah header standar `managed-agents-2026-04-01`. Lihat [Menggunakan memori agen](/docs/id/managed-agents/memory) untuk panduan integrasi lengkap.

### 20 April 2026

* Kami telah memensiunkan model Claude Haiku 3 (`claude-3-haiku-20240307`). Semua permintaan ke model ini sekarang akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Haiku 4.5](/docs/id/about-claude/models/overview#latest-models-comparison).

### 16 April 2026

* Kami telah meluncurkan [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), model paling mumpuni kami yang tersedia secara umum untuk penalaran kompleks dan pengkodean agentik, dengan harga yang sama $5 / $25 per MTok seperti Opus 4.6. Lihat [Apa yang baru di Claude Opus 4.7](/docs/id/about-claude/models/whats-new-claude-4-7) untuk peningkatan kemampuan, fitur baru, dan tokenizer yang diperbarui. Opus 4.7 menyertakan perubahan API yang merusak kompatibilitas dibandingkan Opus 4.6; lihat [Migrasi ke Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-46) sebelum meningkatkan.
* [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) sekarang terbuka untuk semua pelanggan Amazon Bedrock. Claude Opus 4.7 dan Claude Haiku 4.5 tersedia secara mandiri dari konsol Bedrock melalui endpoint Messages API di `/anthropic/v1/messages`, di 27 region AWS dengan endpoint global dan regional.
* Kami telah meluncurkan [anggaran tugas](/docs/id/build-with-claude/task-budgets) dalam versi beta di Claude Opus 4.7. Berikan Claude anggaran token yang bersifat anjuran untuk satu loop agentik penuh (pemikiran, panggilan alat, hasil alat, dan output) dan model melihat hitungan mundur yang berjalan, menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan dengan baik saat anggaran terpakai. Sertakan header beta `task-budgets-2026-03-13` dalam permintaan Anda.
* Claude Opus 4.7 mendukung [input gambar resolusi tinggi](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7), menaikkan resolusi gambar maksimum dari 1568 menjadi 2576 piksel pada sisi panjang untuk kinerja yang lebih baik pada penggunaan komputer, pemahaman tangkapan layar, dan analisis dokumen. Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta; gambar dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya.
* Kami telah menambahkan tingkat [effort](/docs/id/build-with-claude/effort) `xhigh` di Claude Opus 4.7. `xhigh` berada di antara `high` dan `max` dan disetel untuk tugas agentik dan pengkodean yang berjalan lama (lebih dari 30 menit) dengan anggaran token dalam jutaan. Tidak diperlukan header beta.

### 14 April 2026

* Kami mengumumkan penghentian dukungan (deprecation) model Claude Sonnet 4 (`claude-sonnet-4-20250514`) dan model Claude Opus 4 (`claude-opus-4-20250514`), dengan pemensiunan di Claude API dijadwalkan pada 15 Juni 2026. Kami merekomendasikan migrasi ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) dan [Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47) secara berurutan. Baca selengkapnya di [penghentian dukungan model](/docs/id/about-claude/model-deprecations).

### 9 April 2026

* Kami telah meluncurkan [alat advisor](/docs/id/agents-and-tools/tool-use/advisor-tool) dalam versi beta publik. Pasangkan model eksekutor yang lebih cepat dengan model advisor berintelegensi lebih tinggi yang memberikan panduan strategis di tengah pembuatan, sehingga beban kerja agentik berhorizon panjang mendekati kualitas advisor saja sementara sebagian besar pembuatan token terjadi dengan tarif model eksekutor. Sertakan header beta `advisor-tool-2026-03-01` dalam permintaan Anda.

### 8 April 2026

* Kami telah meluncurkan **Claude Managed Agents** dalam beta publik, sebuah harness agen yang dikelola sepenuhnya untuk menjalankan Claude sebagai agen otonom dengan sandboxing yang aman, alat bawaan, dan streaming server-sent event. Buat agen, konfigurasikan container, dan jalankan sesi melalui API. Semua endpoint memerlukan header beta `managed-agents-2026-04-01`. Pelajari lebih lanjut di [Ikhtisar Claude Managed Agents](/docs/id/managed-agents/overview).
* Kami telah meluncurkan **CLI `ant`**, sebuah klien command-line untuk Claude API yang memungkinkan interaksi lebih cepat dengan Claude API, integrasi native dengan Claude Code, dan versioning sumber daya API dalam file YAML. Pelajari lebih lanjut di [Quickstart CLI](/docs/id/cli-sdks-libraries/cli/quickstart).

### 7 April 2026

* Kami mengumumkan [Claude Mythos Preview](https://anthropic.com/glasswing) tersedia sebagai pratinjau riset terbatas untuk pekerjaan keamanan siber defensif sebagai bagian dari [Project Glasswing](https://anthropic.com/glasswing). Akses hanya melalui undangan.
* [Messages API](/docs/id/api/messages) kini tersedia di Amazon Bedrock sebagai pratinjau riset. Endpoint Claude in Amazon Bedrock yang baru di `/anthropic/v1/messages` menggunakan bentuk permintaan yang sama dengan Claude API pihak pertama dan berjalan di infrastruktur yang dikelola AWS tanpa akses operator. Tersedia di `us-east-1`; hubungi account executive Anthropic Anda untuk meminta akses. Pelajari lebih lanjut di [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock).

### 30 Maret 2026

* Kami telah menaikkan batas `max_tokens` menjadi 300k pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta) untuk Claude Opus 4.6 dan Sonnet 4.6. Sertakan header beta `output-300k-2026-03-24` untuk menghasilkan output single-turn yang lebih panjang untuk konten bentuk panjang, data terstruktur, dan tugas pembuatan kode berskala besar.
* Kami akan menghentikan beta jendela konteks 1M token untuk Claude Sonnet 4.5 dan Claude Sonnet 4 pada **30 April 2026**. Setelah tanggal tersebut, header beta `context-1m-2025-08-07` tidak akan berpengaruh pada model-model ini, dan permintaan yang melebihi jendela konteks standar 200k token akan mengembalikan error. Untuk terus menggunakan jendela konteks 1M, migrasikan ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) atau [Claude Opus 4.6](/docs/id/about-claude/models/overview#latest-models-comparison), yang mendukung jendela konteks 1M token penuh dengan harga standar tanpa memerlukan header beta.

### 18 Maret 2026

* Kami telah menambahkan field kemampuan model ke [Models API](/docs/id/api/models/list). `GET /v1/models` dan `GET /v1/models/{model_id}` kini mengembalikan `max_input_tokens`, `max_tokens`, dan objek `capabilities`. Kueri API untuk mengetahui apa yang didukung oleh setiap model.

### 16 Maret 2026

* Kami telah meluncurkan field `display` untuk pemikiran diperpanjang, memungkinkan Anda menghilangkan konten pemikiran dari respons untuk streaming yang lebih cepat. Atur `thinking.display: "omitted"` untuk menerima blok thinking dengan field `thinking` kosong dan `signature` yang dipertahankan untuk kontinuitas multi-turn. Penagihan tidak berubah. Pelajari lebih lanjut di [Mengontrol tampilan thinking](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display).

### 13 Maret 2026

* [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) kini tersedia secara umum untuk Claude Opus 4.6 dan Sonnet 4.6 dengan harga standar. Permintaan di atas 200k token bekerja secara otomatis untuk model-model ini tanpa memerlukan header beta. Jendela konteks 1M token tetap dalam beta untuk Claude Sonnet 4.5 dan Sonnet 4.
* Kami telah menghapus batas laju khusus 1M untuk semua model yang didukung. Batas akun standar Anda kini berlaku di semua panjang konteks.
* Kami telah menaikkan batas media dari 100 menjadi 600 gambar atau halaman PDF per permintaan saat menggunakan jendela konteks 1M token.

### 19 Februari 2026

* Kami telah meluncurkan **automatic caching** untuk Messages API. Tambahkan satu field `cache_control` ke body permintaan Anda dan sistem secara otomatis melakukan cache pada blok terakhir yang dapat di-cache, memindahkan titik cache ke depan seiring percakapan berkembang. Tidak diperlukan pengelolaan breakpoint manual. Bekerja berdampingan dengan kontrol cache tingkat blok yang sudah ada untuk optimasi yang lebih terperinci. Tersedia di Claude API dan Microsoft Foundry (pratinjau). Pelajari lebih lanjut di [Caching prompt](/docs/id/build-with-claude/prompt-caching#automatic-caching).
* Kami telah menghentikan model Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`) dan model Claude Haiku 3.5 (`claude-3-5-haiku-20241022`). Semua permintaan ke model-model ini kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Sonnet 4.6](/docs/id/about-claude/models/overview#latest-models-comparison) dan [Claude Haiku 4.5](/docs/id/about-claude/models/overview#latest-models-comparison) secara berurutan. Peneliti dapat meminta akses berkelanjutan melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).
* Kami mengumumkan deprekasi model Claude Haiku 3 (`claude-3-haiku-20240307`), dengan penghentian dijadwalkan pada 20 April 2026. Kami merekomendasikan migrasi ke [Claude Haiku 4.5](/docs/id/about-claude/models/overview#latest-models-comparison). Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).

### 17 Februari 2026

* Kami telah meluncurkan [Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6), model seimbang terbaru kami yang menggabungkan kecepatan dan kecerdasan untuk tugas sehari-hari. Sonnet 4.6 memberikan kinerja pencarian agentik yang lebih baik sambil mengonsumsi lebih sedikit token. Sonnet 4.6 mendukung [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) dan [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) (beta). Lihat [Model & Harga](/docs/id/about-claude/models) untuk detailnya.
* [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) API kini **gratis saat digunakan dengan web search atau web fetch**. Eksekusi kode dalam sandbox meningkatkan kemampuan model dan efisiensi token. Lihat [detail harga](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk penggunaan mandiri.
* [Alat web search](/docs/id/agents-and-tools/tool-use/web-search-tool) dan [programmatic tool calling](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) kini tersedia secara umum (tidak memerlukan header beta). Web search dan web fetch kini mendukung [dynamic filtering](/docs/id/agents-and-tools/tool-use/web-search-tool#dynamic-filtering), yang menggunakan eksekusi kode untuk memfilter hasil sebelum mencapai jendela konteks demi kinerja yang lebih baik dan biaya token yang lebih rendah.
* [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), [alat web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), [alat tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool), [contoh penggunaan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples), dan [alat memory](/docs/id/agents-and-tools/tool-use/memory-tool) kini tersedia secara umum (tidak memerlukan header beta).

### 7 Februari 2026

* Kami telah meluncurkan [fast mode](/docs/id/build-with-claude/fast-mode) dalam pratinjau riset untuk Opus 4.6, memberikan pembuatan token output yang jauh lebih cepat melalui parameter `speed`. Fast mode hingga 2,5x lebih cepat dengan harga premium. Pelanggan yang tertarik dapat bergabung dengan [daftar tunggu](https://claude.com/fast-mode).

### 5 Februari 2026

* Kami telah meluncurkan [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), model paling cerdas kami untuk tugas agentik yang kompleks dan pekerjaan jangka panjang. Opus 4.6 merekomendasikan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`); thinking manual (`type: "enabled"` dengan `budget_tokens`) sudah dideprekasi. Opus 4.6 tidak mendukung prefilling pesan assistant. Pelajari lebih lanjut di [Apa yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6).
* [Parameter effort](/docs/id/build-with-claude/effort) kini tersedia secara umum (tidak memerlukan header beta) dan mendukung Claude Opus 4.6. Effort menggantikan `budget_tokens` untuk mengontrol kedalaman thinking pada model-model baru.
* Kami telah meluncurkan [compaction API](/docs/id/build-with-claude/compaction) dalam beta, menyediakan ringkasan konteks sisi server untuk percakapan yang secara efektif tak terbatas. Tersedia di Opus 4.6.
* Kami telah memperkenalkan [kontrol residensi data](/docs/id/manage-claude/data-residency), memungkinkan Anda menentukan di mana inferensi model berjalan dengan parameter `inference_geo`. Inferensi khusus AS tersedia dengan harga 1,1x untuk model yang dirilis setelah 1 Februari 2026.
* [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) kini tersedia dalam beta untuk Claude Opus 4.6, selain Sonnet 4.5 dan Sonnet 4. [Harga konteks panjang](/docs/id/about-claude/pricing#long-context-pricing) berlaku untuk permintaan yang melebihi 200k token input.
* [Fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) kini tersedia secara umum di semua model dan platform (tidak memerlukan header beta).

### 29 Januari 2026

* [Structured outputs](/docs/id/build-with-claude/structured-outputs) kini tersedia secara umum di Claude API untuk Claude Sonnet 4.5, Claude Opus 4.5, dan Claude Haiku 4.5. GA mencakup dukungan skema yang diperluas, latensi kompilasi grammar yang lebih baik, dan jalur integrasi yang disederhanakan tanpa memerlukan header beta. Parameter `output_format` telah dipindahkan ke `output_config.format`. Pengguna beta yang sudah ada dapat terus menggunakan header beta selama periode transisi. Structured outputs tetap dalam beta publik di Amazon Bedrock dan Microsoft Foundry.

### 12 Januari 2026

* `console.anthropic.com` kini dialihkan ke `platform.claude.com`. Claude Console telah pindah ke rumah barunya sebagai bagian dari konsolidasi merek Claude kami. Bookmark dan tautan yang sudah ada akan terus berfungsi melalui pengalihan otomatis. Untuk detail lebih lanjut, lihat [pengumuman 16 September 2025](#september-16-2025).

### 5 Januari 2026

* Kami telah menghentikan model Claude Opus 3 (`claude-3-opus-20240229`). Semua permintaan ke model ini kini akan mengembalikan error. Kami merekomendasikan untuk meningkatkan ke [Claude Opus 4.5](/docs/id/about-claude/models/overview#latest-models-comparison), yang menawarkan kecerdasan yang jauh lebih baik dengan sepertiga biaya. Peneliti dapat meminta akses berkelanjutan ke Claude Opus 3 di API melalui [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### 19 Desember 2025

* Kami mengumumkan deprekasi model Claude Haiku 3.5. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).

### 4 Desember 2025

* [Structured outputs](/docs/id/build-with-claude/structured-outputs) kini mendukung Claude Haiku 4.5.

### 24 November 2025

* Kami telah meluncurkan [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5), model paling cerdas kami yang menggabungkan kemampuan maksimum dengan kinerja praktis. Ideal untuk tugas khusus yang kompleks, rekayasa perangkat lunak profesional, dan agen tingkat lanjut. Menghadirkan peningkatan signifikan dalam vision, coding, dan computer use dengan harga yang lebih terjangkau dibandingkan model Opus sebelumnya. Pelajari lebih lanjut di [Ikhtisar model](/docs/id/about-claude/models).
* Kami telah meluncurkan [programmatic tool calling](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) dalam beta publik, memungkinkan Claude memanggil alat dari dalam eksekusi kode untuk mengurangi latensi dan penggunaan token dalam alur kerja multi-alat.
* Kami telah meluncurkan [alat tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool) dalam beta publik, memungkinkan Claude menemukan dan memuat alat secara dinamis sesuai permintaan dari katalog alat yang besar.
* Kami telah meluncurkan [parameter effort](/docs/id/build-with-claude/effort) dalam beta publik untuk Claude Opus 4.5, memungkinkan Anda mengontrol penggunaan token dengan menyeimbangkan antara ketelitian respons dan efisiensi.
* Kami telah menambahkan [client-side compaction](/docs/id/build-with-claude/context-editing#client-side-compaction-sdk) ke SDK Python dan TypeScript kami, yang secara otomatis mengelola konteks percakapan melalui ringkasan saat menggunakan `tool_runner`.

### 21 November 2025

* Blok konten hasil pencarian kini tersedia secara umum di Amazon Bedrock. Pelajari lebih lanjut di [Hasil pencarian](/docs/id/build-with-claude/search-results).

### 19 November 2025

* Kami telah meluncurkan **platform dokumentasi baru** di [platform.claude.com/docs](https://platform.claude.com/docs). Dokumentasi kami kini berada berdampingan dengan Claude Console, memberikan pengalaman pengembang yang terpadu. Situs dokumentasi sebelumnya di docs.claude.com akan dialihkan ke lokasi baru.

### 18 November 2025

* Kami telah meluncurkan **Claude in Microsoft Foundry**, menghadirkan model Claude kepada pelanggan Azure dengan penagihan Azure dan autentikasi OAuth. Akses Messages API lengkap termasuk pemikiran diperpanjang, caching prompt (5 menit dan 1 jam), dukungan PDF, Files API, Agent Skills, dan penggunaan alat. Pelajari lebih lanjut di [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

### 14 November 2025

* Kami telah meluncurkan [structured outputs](/docs/id/build-with-claude/structured-outputs) dalam beta publik, memberikan jaminan kesesuaian skema untuk respons Claude. Gunakan output JSON untuk respons data terstruktur atau strict tool use untuk input alat yang tervalidasi. Tersedia untuk Claude Sonnet 4.5 dan Claude Opus 4.1. Untuk mengaktifkannya, gunakan header beta `structured-outputs-2025-11-13`.

### 28 Oktober 2025

* Kami mengumumkan deprekasi model Claude Sonnet 3.7. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).
* Kami telah menghentikan model Claude Sonnet 3.5. Semua permintaan ke model-model ini kini akan mengembalikan error.
* Kami telah memperluas context editing dengan pembersihan blok thinking (`clear_thinking_20251015`), memungkinkan pengelolaan otomatis blok thinking. Pelajari lebih lanjut di [Context editing](/docs/id/build-with-claude/context-editing).

### 16 Oktober 2025

* Kami telah meluncurkan [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (beta `skills-2025-10-02`), cara baru untuk memperluas kemampuan Claude. Skills adalah folder terorganisir berisi instruksi, skrip, dan sumber daya yang dimuat Claude secara dinamis untuk melakukan tugas khusus. Rilis awal mencakup:

  * **Skills yang dikelola Anthropic**: Skills siap pakai untuk bekerja dengan file PowerPoint (.pptx), Excel (.xlsx), Word (.docx), dan PDF
  * **Skills kustom**: Unggah Skills Anda sendiri melalui Skills API (endpoint `/v1/skills`) untuk mengemas keahlian domain dan alur kerja organisasi
  * Skills memerlukan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk diaktifkan
  * Pelajari lebih lanjut di [Agent Skills](/docs/id/agents-and-tools/agent-skills/overview) dan [Referensi API](/docs/id/api/skills/create-skill)

### 15 Oktober 2025

* Kami telah meluncurkan [Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5), model Haiku tercepat dan paling cerdas kami dengan kinerja mendekati frontier. Ideal untuk aplikasi real-time, pemrosesan volume tinggi, dan deployment yang sensitif terhadap biaya yang memerlukan penalaran yang kuat. Pelajari lebih lanjut di [Ikhtisar model](/docs/id/about-claude/models).

### 29 September 2025

* Kami telah meluncurkan [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), model terbaik kami untuk agen kompleks dan coding, dengan kecerdasan tertinggi di sebagian besar tugas. Pelajari lebih lanjut di [ikhtisar model](/docs/id/about-claude/models/overview).
* Kami telah memperkenalkan [harga endpoint global](/docs/id/about-claude/pricing#cloud-platform-pricing) untuk Amazon Bedrock dan Vertex AI. Harga Claude API (1P) tidak terpengaruh.
* Kami telah memperkenalkan stop reason baru `model_context_window_exceeded` yang memungkinkan Anda meminta token maksimum yang mungkin tanpa menghitung ukuran input. Pelajari lebih lanjut di [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).
* Kami telah meluncurkan alat memory dalam beta, memungkinkan Claude menyimpan dan merujuk informasi di seluruh percakapan. Pelajari lebih lanjut di [Alat memory](/docs/id/agents-and-tools/tool-use/memory-tool).
* Kami telah meluncurkan context editing dalam beta, menyediakan strategi untuk mengelola konteks percakapan secara otomatis. Rilis awal mendukung pembersihan hasil dan panggilan alat yang lebih lama saat mendekati batas token. Pelajari lebih lanjut di [Context editing](/docs/id/build-with-claude/context-editing).

### 17 September 2025

* Kami telah meluncurkan tool helpers dalam beta untuk SDK Python dan TypeScript, menyederhanakan pembuatan dan eksekusi alat dengan validasi input yang type-safe dan tool runner untuk penanganan alat otomatis dalam percakapan. Untuk detailnya, lihat dokumentasi untuk [SDK Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md) dan [SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers).

### 16 September 2025

* Kami telah menyatukan penawaran pengembang kami di bawah merek Claude. Anda akan melihat penamaan dan URL yang diperbarui di seluruh platform dan dokumentasi kami, tetapi **antarmuka pengembang kami akan tetap sama**. Berikut beberapa perubahan penting:

  * Claude Console ([console.anthropic.com](https://console.anthropic.com)) → Claude Console ([platform.claude.com](https://platform.claude.com)). Console akan tersedia di kedua URL hingga 12 Januari 2026. Setelah tanggal tersebut, [console.anthropic.com](https://console.anthropic.com) akan secara otomatis dialihkan ke [platform.claude.com](https://platform.claude.com).
  * Anthropic Docs ([docs.anthropic.com](https://docs.anthropic.com)) → Claude Docs ([docs.claude.com](https://docs.claude.com))
  * Anthropic Help Center ([support.anthropic.com](https://support.anthropic.com)) → Claude Help Center ([support.claude.com](https://support.claude.com))
  * Endpoint API, header, variabel lingkungan, dan SDK tetap sama. Integrasi Anda yang sudah ada akan terus berfungsi tanpa perubahan apa pun.

### 10 September 2025

* Kami telah meluncurkan alat web fetch dalam beta, memungkinkan Claude mengambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan. Pelajari lebih lanjut di [Alat web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool).
* Kami telah meluncurkan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api), memungkinkan organisasi mengakses metrik penggunaan agregat harian untuk Claude Code secara terprogram, termasuk metrik produktivitas, statistik penggunaan alat, dan data biaya.

### 8 September 2025

* Kami meluncurkan versi beta dari [SDK C#](https://github.com/anthropics/anthropic-sdk-csharp).

### 5 September 2025

* Kami telah meluncurkan [grafik batas laju](/docs/id/api/rate-limits#monitoring-your-rate-limits-in-the-console) di halaman [Usage](https://console.anthropic.com/settings/usage) Console, memungkinkan Anda memantau penggunaan batas laju API dan tingkat caching Anda dari waktu ke waktu.

### 3 September 2025

* Kami telah meluncurkan dukungan untuk dokumen yang dapat dikutip dalam hasil alat sisi klien. Pelajari lebih lanjut di [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

### 2 September 2025

* Kami telah meluncurkan v2 dari [Alat Eksekusi Kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, menggantikan alat asli yang hanya mendukung Python dengan eksekusi perintah Bash dan kemampuan manipulasi file langsung, termasuk menulis kode dalam bahasa lain.

### 27 Agustus 2025

* Kami meluncurkan versi beta dari [SDK PHP](https://github.com/anthropics/anthropic-sdk-php).

### 26 Agustus 2025

* Kami telah meningkatkan batas laju pada [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) untuk Claude Sonnet 4 di Claude API.
* Jendela konteks 1M token kini tersedia di Vertex AI. Untuk informasi lebih lanjut, lihat [Claude di Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai).

### 19 Agustus 2025

* Request ID kini disertakan langsung dalam body respons error bersama header `request-id` yang sudah ada. Pelajari lebih lanjut di [Error](/docs/id/api/errors#error-shapes).

### 18 Agustus 2025

* Kami telah merilis [Usage & Cost API](/docs/id/manage-claude/usage-cost-api), memungkinkan administrator memantau data penggunaan dan biaya organisasi mereka secara terprogram.
* Kami telah menambahkan endpoint baru ke Admin API untuk mengambil informasi organisasi. Untuk detailnya, lihat [Referensi Organization Info Admin API](/docs/id/api/admin-api/organization/get-me).

### 13 Agustus 2025

* Kami mengumumkan deprekasi model Claude Sonnet 3.5 (`claude-3-5-sonnet-20240620` dan `claude-3-5-sonnet-20241022`). Model-model ini akan dihentikan pada 28 Oktober 2025. Kami merekomendasikan migrasi ke Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) untuk kinerja dan kemampuan yang lebih baik. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).
* Durasi cache 1 jam untuk caching prompt kini tersedia secara umum. Anda kini dapat menggunakan TTL cache yang diperpanjang tanpa header beta. Pelajari lebih lanjut di [Caching prompt](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration).

### 12 Agustus 2025

* Kami telah meluncurkan dukungan beta untuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) di Claude Sonnet 4 pada Claude API dan Amazon Bedrock.

### 11 Agustus 2025

* Beberapa pelanggan mungkin mengalami [error](/docs/id/api/errors) 429 (`rate_limit_error`) setelah peningkatan tajam dalam penggunaan API karena batas akselerasi pada API. Sebelumnya, error 529 (`overloaded_error`) akan terjadi dalam skenario serupa.

### 8 Agustus 2025

* Blok konten hasil pencarian kini tersedia secara umum di Claude API dan Vertex AI. Fitur ini memungkinkan sitasi alami untuk aplikasi RAG dengan atribusi sumber yang tepat. Header beta `search-results-2025-06-09` tidak lagi diperlukan. Pelajari lebih lanjut di [Hasil pencarian](/docs/id/build-with-claude/search-results).

### 5 Agustus 2025

* Kami telah meluncurkan [Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1), pembaruan inkremental untuk Claude Opus 4 dengan kemampuan yang ditingkatkan dan peningkatan kinerja.\* Pelajari lebih lanjut di [Ikhtisar model](/docs/id/about-claude/models).

*\* - Opus 4.1 tidak mengizinkan parameter `temperature` dan `top_p` ditentukan bersamaan. Harap gunakan hanya salah satu.*

### 28 Juli 2025

* Kami telah merilis `text_editor_20250728`, alat text editor yang diperbarui yang memperbaiki beberapa masalah dari versi sebelumnya dan menambahkan parameter opsional `max_characters` yang memungkinkan Anda mengontrol panjang pemotongan saat melihat file besar.

### 24 Juli 2025

* Kami telah meningkatkan [batas laju](/docs/id/api/rate-limits) untuk Claude Opus 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan menskalakan dengan Claude. Untuk pelanggan dengan [batas laju usage tier 1-4](/docs/id/api/rate-limits#rate-limits), perubahan ini berlaku segera untuk akun Anda - tidak diperlukan tindakan apa pun.

### 21 Juli 2025

* Kami telah menghentikan model Claude 2.0, Claude 2.1, dan Claude Sonnet 3. Semua permintaan ke model-model ini kini akan mengembalikan error. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).

### 17 Juli 2025

* Kami telah meningkatkan [batas laju](/docs/id/api/rate-limits) untuk Claude Sonnet 4 di Claude API untuk memberi Anda lebih banyak kapasitas untuk membangun dan menskalakan dengan Claude. Untuk pelanggan dengan [batas laju usage tier 1-4](/docs/id/api/rate-limits#rate-limits), perubahan ini berlaku segera untuk akun Anda - tidak diperlukan tindakan apa pun.

### 3 Juli 2025

* Kami telah meluncurkan blok konten hasil pencarian dalam beta, memungkinkan sitasi alami untuk aplikasi RAG. Alat kini dapat mengembalikan hasil pencarian dengan atribusi sumber yang tepat, dan Claude akan secara otomatis mengutip sumber-sumber ini dalam responsnya - menyamai kualitas sitasi web search. Ini menghilangkan kebutuhan akan solusi alternatif dokumen dalam aplikasi basis pengetahuan kustom. Pelajari lebih lanjut di [Hasil pencarian](/docs/id/build-with-claude/search-results). Untuk mengaktifkan fitur ini, gunakan header beta `search-results-2025-06-09`.

### 30 Juni 2025

* Kami mengumumkan deprekasi model Claude Opus 3. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).

### 23 Juni 2025

* Pengguna Console dengan peran Developer kini dapat mengakses halaman [Cost](https://console.anthropic.com/settings/cost). Sebelumnya, peran Developer mengizinkan akses ke halaman [Usage](https://console.anthropic.com/settings/usage), tetapi tidak ke halaman Cost.

### 11 Juni 2025

* Kami telah meluncurkan [fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) dalam beta publik, fitur yang memungkinkan Claude melakukan streaming parameter penggunaan alat tanpa buffering / validasi JSON. Untuk mengaktifkan fine-grained tool streaming, gunakan [header beta](/docs/id/api/beta-headers) `fine-grained-tool-streaming-2025-05-14`.

### 22 Mei 2025

* Kami telah meluncurkan [Claude Opus 4 dan Claude Sonnet 4](https://www.anthropic.com/news/claude-4), model terbaru kami dengan kemampuan pemikiran diperpanjang. Pelajari lebih lanjut di [Ikhtisar model](/docs/id/about-claude/models).
* Perilaku default [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) pada model Claude 4 mengembalikan ringkasan dari proses thinking lengkap Claude, dengan thinking lengkap dienkripsi dan dikembalikan dalam field `signature` dari output blok `thinking`.
* Kami telah meluncurkan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) dalam beta publik, fitur yang memungkinkan Claude berpikir di antara panggilan alat. Untuk mengaktifkan interleaved thinking, gunakan [header beta](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14`.
* Kami telah meluncurkan [Files API](/docs/id/build-with-claude/files) dalam beta publik, memungkinkan Anda mengunggah file dan merujuknya di Messages API dan alat eksekusi kode.
* Kami telah meluncurkan [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) dalam beta publik, alat yang memungkinkan Claude mengeksekusi kode Python dalam lingkungan sandbox yang aman.
* Kami telah meluncurkan [konektor MCP](/docs/id/agents-and-tools/mcp-connector) dalam beta publik, fitur yang memungkinkan Anda terhubung ke server MCP jarak jauh langsung dari Messages API.
* Untuk meningkatkan kualitas jawaban dan mengurangi error alat, kami telah mengubah nilai default untuk parameter [nucleus sampling](https://en.wikipedia.org/wiki/Top-p_sampling) `top_p` di Messages API dari 0,999 menjadi 0,99 untuk semua model. Untuk mengembalikan perubahan ini, atur `top_p` ke 0,999. Selain itu, saat pemikiran diperpanjang diaktifkan, Anda kini dapat mengatur `top_p` ke nilai antara 0,95 dan 1.
* Kami telah memindahkan [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami dari beta ke GA.
* Kami telah menyertakan granularitas tingkat menit dan jam ke halaman [Usage](https://console.anthropic.com/settings/usage) di Console bersama dengan tingkat error 429 di halaman Usage.

### 21 Mei 2025

* Kami telah memindahkan [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby) kami dari beta ke GA.

### 7 Mei 2025

* Kami telah meluncurkan alat web search di API, memungkinkan Claude mengakses informasi terkini dari web. Pelajari lebih lanjut di [Alat web search](/docs/id/agents-and-tools/tool-use/web-search-tool).

### 1 Mei 2025

* Cache control kini harus ditentukan langsung di blok `content` induk dari `tool_result` dan `document.source`. Untuk kompatibilitas mundur, jika cache control terdeteksi pada blok terakhir di `tool_result.content` atau `document.source.content`, cache control akan secara otomatis diterapkan ke blok induk sebagai gantinya. Cache control pada blok lain di dalam `tool_result.content` dan `document.source.content` akan menghasilkan error validasi.

### 9 April 2025

* Kami meluncurkan versi beta dari [SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby).

### 31 Maret 2025

* Kami telah memindahkan [SDK Java](https://github.com/anthropics/anthropic-sdk-java) kami dari beta ke GA.
* Kami telah memindahkan [SDK Go](https://github.com/anthropics/anthropic-sdk-go) kami dari alpha ke beta.

### 27 Februari 2025

* Kami telah menambahkan blok sumber URL untuk gambar dan PDF di Messages API. Anda kini dapat merujuk gambar dan PDF langsung melalui URL alih-alih harus meng-encode-nya dalam base64. Pelajari lebih lanjut di [Vision](/docs/id/build-with-claude/vision) dan [Dukungan PDF](/docs/id/build-with-claude/pdf-support).
* Kami telah menambahkan dukungan untuk opsi `none` pada parameter `tool_choice` di Messages API yang mencegah Claude memanggil alat apa pun. Selain itu, Anda tidak lagi diharuskan menyediakan `tools` apa pun saat menyertakan blok `tool_use` dan `tool_result`.
* Kami telah meluncurkan endpoint API yang kompatibel dengan OpenAI, memungkinkan Anda menguji model Claude hanya dengan mengubah kunci API, base URL, dan nama model di integrasi OpenAI yang sudah ada. Lapisan kompatibilitas ini mendukung fungsionalitas inti chat completions. Pelajari lebih lanjut di [Kompatibilitas SDK OpenAI](/docs/id/cli-sdks-libraries/libraries/openai-sdk).

### 24 Februari 2025

* Kami telah meluncurkan [Claude Sonnet 3.7](https://www.anthropic.com/news/claude-3-7-sonnet), model paling cerdas kami saat itu. Claude Sonnet 3.7 dapat menghasilkan respons hampir instan atau menunjukkan pemikiran diperpanjangnya langkah demi langkah. Satu model, dua cara berpikir. Pelajari lebih lanjut tentang semua model Claude di [Ikhtisar model](/docs/id/about-claude/models).

* Kami telah menambahkan dukungan vision ke Claude Haiku 3.5, memungkinkan model menganalisis dan memahami gambar.

* Kami telah merilis implementasi penggunaan alat yang hemat token, meningkatkan kinerja keseluruhan saat menggunakan alat dengan Claude. Pelajari lebih lanjut di [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

* Kami telah mengubah temperature default di [Console](https://console.anthropic.com/workbench) untuk prompt baru dari 0 menjadi 1 agar konsisten dengan temperature default di API. Prompt yang sudah tersimpan tidak berubah.

* Kami telah merilis versi terbaru dari alat kami yang memisahkan alat text edit dan bash dari prompt sistem computer use:

  * `bash_20250124`: Fungsionalitas sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `text_editor_20250124`: Fungsionalitas sama dengan versi sebelumnya tetapi independen dari computer use. Tidak memerlukan header beta.
  * `computer_20250124`: Alat computer use yang diperbarui dengan opsi perintah baru termasuk "hold\_key", "left\_mouse\_down", "left\_mouse\_up", "scroll", "triple\_click", dan "wait". Alat ini memerlukan header anthropic-beta "computer-use-2025-01-24". Pelajari lebih lanjut di [Penggunaan alat dengan Claude](/docs/id/agents-and-tools/tool-use/overview).

### 10 Februari 2025

* Kami telah menambahkan header respons `anthropic-organization-id` ke semua respons API. Header ini memberikan ID organisasi yang terkait dengan kunci API yang digunakan dalam permintaan.

### 31 Januari 2025

* Kami telah memindahkan [SDK Java](https://github.com/anthropics/anthropic-sdk-java) kami dari alpha ke beta.

### 23 Januari 2025

* Kami telah meluncurkan kemampuan sitasi di API, memungkinkan Claude memberikan atribusi sumber untuk informasi. Pelajari lebih lanjut di [Sitasi](/docs/id/build-with-claude/citations).
* Kami telah menambahkan dukungan untuk dokumen teks biasa dan dokumen konten kustom di Messages API.

### 21 Januari 2025

* Kami mengumumkan deprekasi model Claude 2, Claude 2.1, dan Claude Sonnet 3. Baca lebih lanjut di [Deprekasi model](/docs/id/about-claude/model-deprecations).

### 15 Januari 2025

* Kami telah memperbarui [caching prompt](/docs/id/build-with-claude/prompt-caching) agar lebih mudah digunakan. Kini, saat Anda menetapkan breakpoint cache, kami akan secara otomatis membaca dari prefix ter-cache terpanjang Anda sebelumnya.
* Anda kini dapat menempatkan kata-kata di mulut Claude saat menggunakan alat.

### 10 Januari 2025

* Kami telah mengoptimalkan dukungan untuk [caching prompt di Message Batches API](/docs/id/build-with-claude/batch-processing#using-prompt-caching-with-message-batches) untuk meningkatkan tingkat cache hit.

### 19 Desember 2024

* Kami telah menambahkan dukungan untuk [endpoint delete](/docs/id/api/deleting-message-batches) di Message Batches API.

### 17 Desember 2024

Fitur-fitur berikut kini tersedia secara umum di Claude API:

* [Models API](/docs/id/api/models/list): Kueri model yang tersedia, validasi ID model, dan resolusi [alias model](/docs/id/about-claude/models#model-names) ke ID model kanoniknya.
* [Message Batches API](/docs/id/build-with-claude/batch-processing): Proses batch pesan dalam jumlah besar secara asinkron dengan 50% dari biaya API standar.
* [Token counting API](/docs/id/build-with-claude/token-counting): Hitung jumlah token untuk Messages sebelum mengirimkannya ke Claude.
* [Prompt Caching](/docs/id/build-with-claude/prompt-caching): Kurangi biaya hingga 90% dan latensi hingga 80% dengan melakukan caching dan menggunakan kembali konten prompt.
* [Dukungan PDF](/docs/id/build-with-claude/pdf-support): Proses PDF untuk menganalisis konten teks dan visual dalam dokumen.

Kami juga merilis SDK resmi baru:

* [SDK Java](https://github.com/anthropics/anthropic-sdk-java) (alpha)
* [SDK Go](https://github.com/anthropics/anthropic-sdk-go) (alpha)

### 4 Desember 2024

* Kami telah menambahkan kemampuan untuk mengelompokkan berdasarkan kunci API di halaman [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) di [Developer Console](https://console.anthropic.com).
* Kami telah menambahkan dua kolom baru **Last used at** dan **Cost** serta kemampuan untuk mengurutkan berdasarkan kolom apa pun di halaman [API keys](https://console.anthropic.com/settings/keys) di [Developer Console](https://console.anthropic.com).

### 21 November 2024

* Kami telah merilis [Admin API](/docs/id/manage-claude/admin-api), memungkinkan pengguna mengelola sumber daya organisasi mereka secara terprogram.

### 20 November 2024

* Kami telah memperbarui batas laju (rate limit) untuk Messages API. Kami telah mengganti batas laju token per menit dengan batas laju token input dan output per menit yang baru. Baca selengkapnya di [Batas laju](/docs/id/api/rate-limits).
* Kami telah menambahkan dukungan untuk [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) di [Workbench](https://console.anthropic.com/workbench).

### 13 November 2024

* Kami telah menambahkan dukungan PDF untuk semua model Claude Sonnet 3.5. Baca selengkapnya di [Dukungan PDF](/docs/id/build-with-claude/pdf-support).

### 6 November 2024

* Kami telah menghentikan model Claude 1 dan Instant. Baca selengkapnya di [Penghentian model](/docs/id/about-claude/model-deprecations).

### 4 November 2024

* [Claude Haiku 3.5](https://www.anthropic.com/claude/haiku) sekarang tersedia di Claude API sebagai model khusus teks.

### 1 November 2024

* Kami telah menambahkan dukungan PDF untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca selengkapnya di [Dukungan PDF](/docs/id/build-with-claude/pdf-support).
* Kami juga telah menambahkan penghitungan token, yang memungkinkan Anda menentukan jumlah total token dalam sebuah Message sebelum mengirimkannya ke Claude. Baca selengkapnya di [Penghitungan token](/docs/id/build-with-claude/token-counting).

### 22 Oktober 2024

* Kami telah menambahkan alat computer use yang didefinisikan oleh Anthropic ke API kami untuk digunakan dengan Claude Sonnet 3.5 yang baru. Baca selengkapnya di [Alat computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool).
* Claude Sonnet 3.5, model kami yang paling cerdas sejauh ini, baru saja mendapatkan peningkatan dan sekarang tersedia di Claude API. Baca selengkapnya di [dokumentasi Claude Sonnet](https://www.anthropic.com/claude/sonnet).

### 8 Oktober 2024

* Message Batches API sekarang tersedia dalam versi beta. Proses batch kueri dalam jumlah besar secara asinkron di Claude API dengan biaya 50% lebih murah. Baca selengkapnya di [Pemrosesan batch](/docs/id/build-with-claude/batch-processing).
* Kami telah melonggarkan pembatasan pada urutan giliran `user`/`assistant` di Messages API kami. Pesan `user`/`assistant` yang berurutan akan digabungkan menjadi satu pesan alih-alih menghasilkan error, dan kami tidak lagi mengharuskan pesan input pertama berupa pesan `user`.
* Kami telah menghentikan paket Build dan Scale demi rangkaian fitur standar (sebelumnya disebut sebagai Build), bersama dengan fitur tambahan yang tersedia melalui tim penjualan. Baca selengkapnya di [informasi harga API kami](https://claude.com/platform/api).

### 3 Oktober 2024

* Kami telah menambahkan kemampuan untuk menonaktifkan penggunaan alat paralel di API. Atur `disable_parallel_tool_use: true` di bidang `tool_choice` untuk memastikan bahwa Claude menggunakan paling banyak satu alat. Baca selengkapnya di [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use).

### 10 September 2024

* Kami telah menambahkan Workspaces ke [Developer Console](https://console.anthropic.com). Workspaces memungkinkan Anda mengatur batas pengeluaran atau batas laju kustom, mengelompokkan kunci API, melacak penggunaan berdasarkan proyek, dan mengontrol akses dengan peran pengguna. Baca selengkapnya di [postingan blog kami](https://www.anthropic.com/news/workspaces).

### 4 September 2024

* Kami mengumumkan penghentian model Claude 1. Baca selengkapnya di [Penghentian model](/docs/id/about-claude/model-deprecations).

### 22 Agustus 2024

* Kami telah menambahkan dukungan untuk penggunaan SDK di browser dengan mengembalikan header CORS dalam respons API. Atur `dangerouslyAllowBrowser: true` pada instansiasi SDK untuk mengaktifkan fitur ini.

### 19 Agustus 2024

* Kami telah memindahkan output 8.192 token dari beta ke ketersediaan umum untuk Claude Sonnet 3.5.

### 14 Agustus 2024

* [Caching prompt](/docs/id/build-with-claude/prompt-caching) sekarang tersedia sebagai fitur beta di Claude API. Simpan dalam cache dan gunakan kembali prompt untuk mengurangi latensi hingga 80% dan biaya hingga 90%.

### 15 Juli 2024

* Hasilkan output hingga 8.192 token dari Claude Sonnet 3.5 dengan header baru `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15`.

### 9 Juli 2024

* Hasilkan kasus uji untuk prompt Anda secara otomatis menggunakan Claude di [Developer Console](https://console.anthropic.com).
* Bandingkan output dari prompt yang berbeda secara berdampingan dalam mode perbandingan output baru di [Developer Console](https://console.anthropic.com).

### 27 Juni 2024

* Lihat penggunaan API dan penagihan yang dirinci berdasarkan jumlah dolar, jumlah token, dan kunci API di tab [Usage](https://console.anthropic.com/settings/usage) dan [Cost](https://console.anthropic.com/settings/cost) yang baru di [Developer Console](https://console.anthropic.com).
* Lihat batas laju API Anda saat ini di tab [Rate Limits](https://console.anthropic.com/settings/limits) yang baru di [Developer Console](https://console.anthropic.com).

### 20 Juni 2024

* [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet), model kami yang paling cerdas sejauh ini, sekarang tersedia secara umum di Claude API, Amazon Bedrock, dan Vertex AI.

### 30 Mei 2024

* [Penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) sekarang tersedia secara umum di Claude API, Amazon Bedrock, dan Vertex AI.

### 10 Mei 2024

* Alat pembuat prompt kami sekarang tersedia di [Developer Console](https://console.anthropic.com). Prompt Generator memudahkan Anda memandu Claude untuk menghasilkan prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda. Baca selengkapnya di [postingan blog kami](https://www.anthropic.com/news/prompt-generator).
