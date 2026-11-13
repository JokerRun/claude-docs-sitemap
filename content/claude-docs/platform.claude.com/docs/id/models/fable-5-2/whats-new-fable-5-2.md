---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 39b555022a3237b0577f272dc84594476521fe6ce845667071b0a1252c3f4f55
---

---
title: Yang baru di Claude Fable 5.2
url: https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2
description: Perubahan yang merusak kompatibilitas, dukungan fitur, harga, dan ketersediaan untuk Claude Fable 5.2 dan Claude Mythos 5.2, dibandingkan dengan Claude Fable 5.1 dan Claude Mythos 5.1.
---

Claude Fable 5.2 dirancang untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang. Untuk sebagian besar beban kerja, mulailah dengan model Claude Opus terbaru (lihat [Memilih model yang tepat](https://platform.claude.com/docs/id/about-claude/models/choosing-a-model)), dan beralihlah ke Claude Fable 5.2 ketika eval Anda pada model Claude Opus dengan effort yang lebih tinggi masih belum memenuhi kebutuhan Anda.

Empat perubahan dari Claude Fable 5.1 dapat merusak kode Anda:

* [Pemeriksaan prefiks yang gagal mengembalikan error 400](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#editing-earlier-turns-invalidates-thinking-blocks).
* [Hanya Claude Fable 5.2 dan Claude Mythos 5.2 yang membaca blok thinking Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#thinking-blocks-are-tied-to-the-model-that-produced-them).
* Alat lama [`computer_20251124` untuk computer use mengembalikan error](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#computer-20251124-is-not-supported) di setiap platform kecuali Amazon Bedrock.
* Dengan alat advisor, executor Claude Fable 5.2 [memerlukan advisor Claude Fable 5.2 atau Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#advisor-tool-pairs).

## Model

| Model             | ID Claude API     | Deskripsi                                                          | Ketersediaan                                                                                                                                                     |
| ----------------- | ----------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5.2  | claude-fable-5-2  | Untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang | Semua pelanggan di Claude API (untuk platform lain, lihat [Ketersediaan](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#availability)) |
| Claude Mythos 5.2 | claude-mythos-5-2 | Kemampuan yang sama dengan Claude Fable 5.2                        | Organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842)        |

Claude Fable 5.2 dan Claude Mythos 5.2 memiliki spesifikasi yang sama berikut:

* **Jendela konteks dan output:** [“context window” (jendela konteks) sebesar 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (default dan maksimum) dan maksimum 128k token output.
* **Thinking:** [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.
* **Tokenizer:** tokenizer yang diperkenalkan bersama Claude Opus 4.7. Lihat [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting#token-counts-on-claude-fable-5).

Untuk semua model saat ini, lihat [Ikhtisar model](https://platform.claude.com/docs/id/models/overview).

## Perubahan yang merusak kompatibilitas

### Mengedit giliran sebelumnya membatalkan blok thinking

Pada Claude Fable 5.2 dan Claude Mythos 5.2, permintaan yang gagal dalam pemeriksaan prefiks API mendapatkan [error 400](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch). Pemeriksaan prefiks menguji apakah ada sesuatu sebelum blok thinking yang telah berubah sejak model menghasilkannya. Pemeriksaan prefiks ini mencakup prompt `system`, `tools`, dan setiap pesan sebelumnya (lihat [Apa yang harus tetap sama, dan mengapa](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check)). Pesan error tersebut menyatakan `The block is bound to a different conversation`.

Tidak ada yang berubah bagi Anda jika Claude Code, claude.ai, [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), atau [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) yang membangun permintaan Anda.

Jika kode Anda sendiri yang membangun permintaan Anda, tidak ada yang berubah bagi Anda juga, selama semua hal berikut benar:

* Kode Anda menjaga `system` dan `tools` tetap sama selama seluruh percakapan.
* Kode Anda hanya menambahkan ke `messages`. Kode tersebut tidak pernah mengubah, menyusun ulang, atau menghapus pesan sebelumnya.
* Kode Anda [mengirim kembali setiap giliran asisten persis seperti yang dikembalikan API](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#append-assistant-turns-exactly-as-returned): setiap blok, dalam urutan yang sama.
* Kode Anda tidak melakukan satu pun hal yang dicantumkan di [Jika kode Anda mengubah prompt sistem, alat, atau riwayat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-to-check).

Jika tidak, uji kode Anda sebelum Anda beralih:

* **Kode pada Claude Fable 5.1:** Ikuti [bagian pemeriksaan prefiks](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide#fable-5-2-preserved-thinking) dalam panduan migrasi.
* **Kode pada Claude Mythos 5.1:** Ikuti [Migrasi ke Claude Mythos 5.2 dari Claude Mythos 5.1](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide#migrating-from-claude-mythos-5-1-to-claude-mythos-5-2).

Untuk apa yang dianggap sebagai pengeditan, lihat [Apa yang dihitung sebagai perubahan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-counts-as-an-edit). Untuk melakukan setiap perubahan tanpa pengeditan, lihat [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions).

Untuk tidak menyertakan blok thinking yang terpengaruh dan melanjutkan tanpa error 400, kirim header beta `thinking-binding-controls-2026-08-01` dan atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"`. Respons kemudian mencantumkan setiap blok yang tidak disertakan dalam array `input_transformations` tingkat atas. Perlakukan `"drop_block"` sebagai solusi sementara selagi Anda memperbaiki pengeditan, karena [tidak menyertakan blok dapat meningkatkan token output](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation#drop-block-cost).

### Hanya Claude Fable 5.2 dan Claude Mythos 5.2 yang membaca blok thinking Claude Fable 5.2

Setiap blok thinking mencatat model mana yang menghasilkannya, dan sebuah model hanya membaca bloknya sendiri dan beberapa blok dari model lain. Di Claude API dan Claude Models on Google Cloud (Google managed), Claude Fable 5.2 dan Claude Mythos 5.2 membaca blok thinking satu sama lain. Di platform tersebut, keduanya juga membaca blok dari Claude Opus 5.5, Claude Sonnet 5.5, Claude Haiku 5.5, Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5, Claude Fable 5, dan Claude Mythos 5. Keduanya juga membaca blok dari [model Claude Opus, Claude Sonnet, dan Claude Haiku sebelumnya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#earlier-models). Tidak ada model lain yang membaca blok mereka.

* **Beralih ke Claude Fable 5.2 atau Claude Mythos 5.2** dari salah satu model tersebut mempertahankan penalaran percakapan di Claude API dan Claude Models on Google Cloud (Google managed). Begitu pula berpindah antara Claude Fable 5.2 dan Claude Mythos 5.2.
* **Beralih dari Claude Fable 5.2 atau Claude Mythos 5.2 ke model lain mana pun** menghilangkan penalaran mereka untuk giliran yang berjalan di sana. Hal ini mencakup Claude Opus 5.5, Claude Fable 5.1, Claude Mythos 5.1, dan model fallback Claude Fable 5.2 (Claude Opus 4.8 dan Claude Opus 5).

Ketika permintaan membawa blok yang tidak dapat dibaca oleh model saat ini, API tidak menyertakan blok tersebut sebelum model menerimanya. Permintaan berhasil, dan blok yang tidak disertakan tidak ditagih. Dengan header beta `thinking-binding-controls-2026-08-01`, respons mencantumkan blok yang tidak disertakan tersebut dalam `input_transformations`. Lihat [Beralih model dan kembali lagi](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

### Gunakan toolset computer use alih-alih `computer_20251124`

Claude Fable 5.1 menerima [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) baik sebagai toolset `computer_toolset_20260801` maupun, dengan header beta `computer-use-2025-11-24`, sebagai alat `computer_20251124` yang lama. Claude Fable 5.2 dan Claude Mythos 5.2 mendukung computer use melalui toolset. Permintaan ke salah satu model yang mendeklarasikan alat `computer_20251124` mengembalikan 400 `invalid_request_error` di setiap platform kecuali Amazon Bedrock. Di sana, kedua model menerima alat lama: dengan InvokeModel API, kirim `computer-use-2025-11-24` dalam array `anthropic_beta` di badan permintaan.

Untuk memindahkan integrasi yang ada, ikuti [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

### Executor Claude Fable 5.2 memerlukan advisor Claude Fable 5.2 atau Claude Mythos 5.2

Dengan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool), yang masih dalam tahap beta, advisor harus setidaknya sama mampunya dengan executor. Executor Claude Fable 5.2 atau Claude Mythos 5.2 hanya menerima Claude Fable 5.2 atau Claude Mythos 5.2 sebagai advisornya. Advisor lain, termasuk Claude Fable 5.1 dan Claude Mythos 5.1, mengembalikan 400 `invalid_request_error`.

Jika Anda menggunakan alat advisor dan memindahkan executor ke salah satu model ini, atur `model` dalam definisi alat advisor ke `claude-fable-5-2` atau `claude-mythos-5-2` dalam perubahan yang sama. Mengubah `model` advisor merupakan pengeditan pada `tools`, jadi lakukan perubahan tersebut di percakapan baru. Permintaan yang mengirim kembali blok thinking sebelumnya setelah perubahan gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#editing-earlier-turns-invalidates-thinking-blocks) dan mengembalikan error 400, kecuali Anda mengatur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"` (beta, header `thinking-binding-controls-2026-08-01`). Untuk mempertahankan executor Anda saat ini dan hanya mengubah advisor, atur `model` advisor ke `claude-fable-5-2`: setiap model executor menerimanya. Advisor Claude Fable 5.2 mengembalikan sarannya dalam bentuk terenkripsi, jadi jika kode Anda membaca teks saran, lihat [Varian hasil](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#result-variants). Lihat juga [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility).

## Thinking dan pilihan alat

Dua aturan Messages API berlaku untuk setiap permintaan Claude Fable 5.2. Keduanya bukan perubahan jika Anda berasal dari Claude Fable 5.1, Claude Mythos 5.1, atau Claude Opus 5.5. Dari Claude Fable 5 atau Claude Mythos 5, tempat adaptive thinking sudah selalu aktif, hanya aturan penggunaan alat paksa yang merupakan perubahan yang merusak kompatibilitas. Dari Claude Opus 5 atau model Claude Opus sebelumnya, keduanya merupakan perubahan yang merusak kompatibilitas. [Panduan migrasi Claude Fable 5.2 dan Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide) membahas setiap jalur.

* **Adaptive thinking selalu aktif.** `thinking: {"type": "enabled"}` dengan `budget_tokens` dan `thinking: {"type": "disabled"}` sama-sama mengembalikan error 400. Hilangkan `thinking` atau kirim `{"type": "adaptive"}`, dan gunakan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.
* **“Forced tool use” (penggunaan alat paksa) tidak didukung.** `tool_choice` yang diatur ke `{"type": "any"}` atau `{"type": "tool", "name": "..."}` mengembalikan 400 `invalid_request_error`. Untuk JSON yang valid sesuai skema, pertahankan `tool_choice: {"type": "auto"}` dan atur `strict: true` dengan [penggunaan alat ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use), atau gunakan [output JSON](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#usage). Dalam organisasi dengan [“customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan)](https://platform.claude.com/docs/id/manage-claude/cmek), [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) tidak tersedia untuk Claude Fable 5.2 atau Claude Mythos 5.2. Hal itu mencakup penggunaan alat ketat dan output JSON. Di sana, hilangkan `strict` dan validasi input alat di kode Anda.

## Dukungan fitur

Claude Fable 5.2 mendukung fitur API berikut, di antara fitur lainnya:

* **Effort:** kelima [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort#effort-levels): `low`, `medium`, `high`, `xhigh`, dan `max`. Default API adalah `high`. Mulailah dari sana, karena sebagian besar peningkatan kemampuan sudah ada pada `high`. Naikkan ke `xhigh` untuk pekerjaan coding dan agentik jangka panjang Anda yang paling sulit, tempat Anda telah mengukur adanya peningkatan. Simpan `max` untuk mengukur batas kemampuan model dan untuk tugas langka ketika waktu dan token tidak menjadi masalah. Lihat [Tingkat effort yang direkomendasikan untuk Claude Fable 5.2](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-fable-5-2).
* **Compaction sesuai permintaan (beta):** dengan header beta `compact-2026-09-04`, Anda memilih kapan mengganti giliran lama dengan ringkasan. Lihat [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand).
* **Perubahan alat di tengah percakapan (beta):** Anda menambahkan atau menghapus alat dalam pesan `role: "system"` alih-alih mengedit `tools`. Di Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed), dan Microsoft Foundry, kirim header beta `inline-tools-2026-09-15`. Header `mid-conversation-tool-changes-2026-07-01` berfungsi untuk perubahan yang menyebut alat berdasarkan referensi, pada platform yang dicantumkan di [Pesan sistem dan perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Lihat [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes).
* **Computer use:** melalui toolset `computer_toolset_20260801`. Alat `computer_20251124` yang lama mengembalikan error 400 di setiap platform kecuali Amazon Bedrock. Di sana, Claude Fable 5.2 dan Claude Mythos 5.2 juga menerima alat lama tersebut. Lihat [perubahan computer use yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#computer-20251124-is-not-supported) dan [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool).

Compaction sesuai permintaan dan perubahan alat di tengah percakapan membantu Anda menjaga riwayat tetap “append-only” (hanya ditambahkan), yang diwajibkan oleh [pemeriksaan prefiks](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#editing-earlier-turns-invalidates-thinking-blocks). Lihat halaman masing-masing fitur untuk ketersediaan model dan platform.

[Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) tersedia untuk Claude Fable 5.2 dalam permintaan Messages API di Claude API, [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), dan [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Claude in Microsoft Foundry, mode cepat tersedia untuk deployment yang di-hosting di Anthropic, dengan ID modelnya sendiri, `claude-fable-5-2-fast`.

Mode cepat juga tersedia untuk Claude Mythos 5.2 dalam permintaan Messages API di Claude API. [Ketersediaan mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode#feature-availability) mencantumkan setiap platform tempat Claude Mythos 5.2 memiliki mode cepat.

### Blok thinking tetap berada di akun yang menghasilkannya

Blok thinking yang dihasilkan Claude Fable 5.2 dan Claude Mythos 5.2 hanya berfungsi di akun yang menghasilkannya, atau di akun yang ditautkan dengannya. Ketika akun lain mengirim salah satu blok ini, API tidak menyertakan blok tersebut sebelum model menerimanya, dan permintaan berhasil. Di Claude API dan Claude Models on Google Cloud (Google managed), dengan header beta `thinking-binding-controls-2026-08-01`, respons mencantumkan setiap blok yang tidak disertakan dalam `input_transformations` dengan `reason: "organization_binding_mismatch"`. Lihat [Akun dan platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking) di Pemikiran yang dipertahankan.

## Perbedaan perilaku

Beberapa perilaku Claude Fable 5.2 muncul tanpa perubahan kode apa pun. Periksalah saat Anda memindahkan prompt. Untuk panduan masing-masing, lihat [Prompting Claude Fable 5.2](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2):

* **Baris prompt yang meminta thinking lebih sedikit tidak menghentikan model dari thinking pada effort `medium` ke atas.** Claude Fable 5.1 biasanya mengikuti baris seperti “jawab langsung tanpa berpikir panjang.” Dalam pengujian Anthropic, baris seperti itu tidak menghentikan Claude Fable 5.2 dari thinking pada `medium` ke atas. Pada `high` ke atas, model berpikir sebelum hampir setiap balasan. Jika permintaan yang mudah memakan waktu terlalu lama atau biaya terlalu besar, gunakan tingkat effort yang lebih rendah untuk giliran tersebut. Lihat [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort).
* **Sebuah giliran dapat berakhir sebelum pekerjaan selesai.** Pada tugas panjang dan multilangkah, model terkadang mengakhiri giliran dengan daftar hal yang tersisa, tawaran untuk melanjutkan, atau berhenti pada hambatan biasa. Hal ini lebih sering terjadi pada effort `low` dan `medium`. Lihat [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#finish-the-whole-task).
* **Apa yang dikatakan prompt tentang kepemilikan kode itu penting.** Dalam pengujian Anthropic pada tugas coding kecil, ketika prompt tidak menyebutkan siapa pemilik kode, model cenderung menambah struktur yang ada dan melaporkan masalah di sekitarnya alih-alih memperbaikinya. Lihat [Nyatakan siapa pemilik kode](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#say-who-owns-the-code).
* **Rangkaian panjang panggilan alat dapat berlangsung dengan sedikit teks yang terlihat oleh pengguna.** Model mungkin juga melakukan panggilan alat pertamanya tanpa mengatakan apa yang akan dilakukannya. Lihat [Jaga agar pengguna tetap mendapat informasi selama giliran yang panjang](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-users-informed-during-long-turns).
* **Seberapa banyak model mendelegasikan ke subagen bergantung pada harness dan tugas Anda.** Dalam produk coding agentik yang prompt-nya mengundang delegasi, model mendelegasikan dengan mudah. Subagen dapat menyumbang porsi besar biaya sebuah sesi. Lihat [Tetapkan ekspektasi untuk subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#set-expectations-for-subagents).
* **Model mengikuti aturan gaya dengan ketat.** Batas keras pada panjang kalimat dapat membuat prosa model terputus-putus. Lihat [Tinjau prompt dan harness yang dirancang untuk model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#review-instructions-written-for-earlier-models).

## Penolakan, fallback, dan penagihan

Claude Fable 5.2 menjalankan pengklasifikasi keamanan, dan semua yang ada di [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) berlaku.

* **Penolakan:** permintaan yang ditolak mengembalikan HTTP 200 dengan `stop_reason: "refusal"` dan objek [`stop_details`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) yang menyebutkan area kebijakan yang terpicu.
* **Fallback:** coba ulang permintaan yang ditolak di model lain dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), [middleware SDK](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback), atau mekanisme coba ulang Anda sendiri. Fallback sisi server masih dalam tahap beta di Claude API dan Claude Models on Google Cloud (Anthropic managed). Dengan fallback sisi server, `fallbacks: "default"` mencoba ulang permintaan yang ditolak pada model yang direkomendasikan Anthropic untuk kategori tersebut. Untuk kategori tanpa fallback yang direkomendasikan, seperti `reasoning_extraction`, penolakan tetap berlaku. Target fallback yang diizinkan untuk Claude Fable 5.2 adalah Claude Opus 4.8 dan Claude Opus 5.
* **Penagihan:** apakah penolakan yang terjadi sebelum output apa pun ditagih bergantung pada kategori penolakannya, dan penolakan tersebut tetap dihitung terhadap batas laju Anda. Lihat [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed). [Kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit) mengembalikan biaya caching prompt akibat berpindah model.

## Harga

Claude Fable 5.2 dan Claude Mythos 5.2 memiliki harga yang sama berikut, dalam USD:

| Input dasar | Penulisan cache 5m | Penulisan cache 1h | Pembacaan cache | Output     |
| ----------- | ------------------ | ------------------ | --------------- | ---------- |
| $8 / MTok   | $10 / MTok         | $16 / MTok         | $0,20 / MTok    | $40 / MTok |

Input dan output lebih murah dibandingkan pada Claude Fable 5.1 dan Claude Mythos 5.1. Claude Fable 5.1 dan Claude Mythos 5.1 berharga $10 USD per juta token input dan $50 USD per juta token output. Pembacaan cache (hit dan refresh) berharga 0,025 kali harga input dasar, pengali yang sama seperti pada model-model tersebut. [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) berharga $4 USD per juta token input dan $20 USD per juta token output. [Mode cepat](https://platform.claude.com/docs/id/build-with-claude/fast-mode) untuk Claude Fable 5.2 dan Claude Mythos 5.2 berharga $16 USD per juta token input dan $80 USD per juta token output. Lihat [Harga mode cepat](https://platform.claude.com/docs/id/about-claude/pricing#fast-mode-pricing). Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga residensi data dan alat.

## Ketersediaan

Claude Fable 5.2 tersedia di:

* **Claude API:** semua pelanggan, sebagai `claude-fable-5-2`
* **AWS:** [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), sebagai `claude-fable-5-2`
* **Amazon Bedrock:** `global.anthropic.claude-fable-5-2` atau `us.anthropic.claude-fable-5-2`, hanya di [endpoint `bedrock-runtime`](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids)
* **Google Cloud:** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), sebagai `claude-fable-5-2`, dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), sebagai `claude-fable-5-2`
* **Microsoft Foundry:** [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-fable-5-2`, di infrastruktur Anthropic (lihat [Opsi hosting](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#hosting-options))

Claude Mythos 5.2 hanya tersedia untuk organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Model ini tersedia di:

* **Claude API:** sebagai `claude-mythos-5-2`
* **Amazon Bedrock:** `global.anthropic.claude-mythos-5-2` atau `us.anthropic.claude-mythos-5-2`, hanya di [endpoint `bedrock-runtime`](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids)
* **Google Cloud:** [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), sebagai `claude-mythos-5-2`, dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), sebagai `claude-mythos-5-2`
* **Microsoft Foundry:** [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), sebagai `claude-mythos-5-2`, di infrastruktur Anthropic

Untuk meminta akses, daftarlah ke program yang mencakup kasus penggunaan Anda, atau hubungi tim akun Anda.

Claude Fable 5.2 dan Claude Mythos 5.2 memerlukan retensi data 30 hari dan tidak tersedia dengan zero data retention kecuali diizinkan secara tegas oleh Anthropic. Keduanya merupakan [Covered Models](https://support.claude.com/en/articles/15425695). Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

## Migrasi dari Claude Fable 5.1

Untuk bermigrasi dari Claude Fable 5.1, perbarui ID model Anda:

<CodeGroup exclude="shell">
  <CodeGroupItem language="cURL">
    Atur field `model` di badan permintaan ke `claude-fable-5-2`.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Atur flag `--model` ke `claude-fable-5-2`.
  </CodeGroupItem>

  ```python Python
  model = "claude-fable-5-1"  # Before
  model = "claude-fable-5-2"  # After
  ```

  ```typescript TypeScript
  let model = "claude-fable-5-1"; // Before
  model = "claude-fable-5-2"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeFable5_1; // Before
  model = Model.ClaudeFable5_2; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeFable5_1 // Before
  model = anthropic.ModelClaudeFable5_2  // After
  ```

  ```java Java
  Model model = Model.CLAUDE_FABLE_5_1; // Before
  model = Model.CLAUDE_FABLE_5_2; // After
  ```

  ```php PHP
  $model = Model::CLAUDE_FABLE_5_1; // Before
  $model = Model::CLAUDE_FABLE_5_2; // After
  ```

  ```ruby Ruby
  model = Anthropic::Model::CLAUDE_FABLE_5_1 # Before
  model = Anthropic::Model::CLAUDE_FABLE_5_2 # After
  ```
</CodeGroup>

Kemudian tinjau item-item berikut:

1. **Periksa apakah kode Anda mengedit riwayat.** Jika kode Anda membangun array `messages` sendiri, jalankan pengujian di [bagian pemeriksaan prefiks](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide#fable-5-2-preserved-thinking) panduan migrasi.
2. **Periksa peralihan model.** Jika router atau fallback memindahkan percakapan antar model, perkirakan bahwa setiap model kecuali Claude Mythos 5.2 tidak akan menyertakan blok thinking Claude Fable 5.2, termasuk Claude Fable 5.1 dan Claude Opus 5.5. Lihat [Hanya Claude Fable 5.2 dan Claude Mythos 5.2 yang membaca blok thinking Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#thinking-blocks-are-tied-to-the-model-that-produced-them).
3. **Pindahkan computer use ke toolset.** Jika Anda menggunakan alat `computer_20251124` di mana pun selain Amazon Bedrock, Claude Fable 5.2 mengembalikan error 400 untuk alat tersebut. Deklarasikan `computer_toolset_20260801` sebagai gantinya. Untuk perubahannya sendiri, lihat [Gunakan toolset computer use alih-alih `computer_20251124`](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#computer-20251124-is-not-supported).
4. **Perbarui advisor.** Jika Anda menggunakan alat advisor dengan Claude Fable 5.2 sebagai executor, atur `model` advisor ke `claude-fable-5-2` atau `claude-mythos-5-2`. Lihat [Executor Claude Fable 5.2 memerlukan advisor Claude Fable 5.2 atau Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#advisor-tool-pairs).
5. **Jalankan ulang eval Anda.** Sertakan sapuan effort yang dimulai dari default, `high`. Lihat [Tingkat effort yang direkomendasikan untuk Claude Fable 5.2](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-fable-5-2).

Lihat [panduan migrasi Claude Fable 5.2 dan Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide) untuk instruksi langkah demi langkah, termasuk dari Claude Mythos 5.1 dan dari model Claude Opus. Untuk pola prompting khusus model, lihat [Prompting Claude Fable 5.2](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/models/overview">
    Spesifikasi dan harga untuk setiap model Claude saat ini.
  </Card>

  <Card title="Panduan migrasi" icon="code" href="https://platform.claude.com/docs/id/models/fable-5-2/migration-guide">
    Pindahkan kode dari Claude Fable 5.1, Claude Mythos 5.1, dan model Claude Opus ke Claude Fable 5.2 atau Claude Mythos 5.2.
  </Card>

  <Card title="Prompting Claude Fable 5.2" icon="terminal" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2">
    Pola prompting khusus untuk Claude Fable 5.2.
  </Card>
</CardGroup>
