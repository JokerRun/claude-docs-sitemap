---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 5b67bdac59e8e6649591f5d77404ec1d38f359792bebc715a602bde48d3195c4
---

---
title: Panduan migrasi Claude Haiku 5.5
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
description: Beralih ke Claude Haiku 5.5 dari model Haiku sebelumnya dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Haiku 5.5 mencakup ID model baru, pengaturan yang mengembalikan error, perubahan thinking, dan daftar periksa untuk setiap model awal.
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-haiku-5-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Panduan ini membahas pemindahan kode yang memanggil Claude Haiku 4.5 ke Claude Haiku 5.5. Untuk kode yang memanggil Claude Haiku 3.5 atau Claude Haiku 3, lakukan juga perubahan di [Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#migrating-from-haiku-35). Untuk beralih ke model Sonnet atau Opus, lihat [Upgrade antar versi model](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Untuk mengetahui berapa lama Claude Haiku 4.5 tetap tersedia, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

## Daftar periksa migrasi berdasarkan model awal

Telusuri grup-grup berikut dari atas ke bawah dan berhenti setelah grup yang menyebutkan model Anda saat ini. Jika Anda menggunakan Claude Haiku 4.5, grup pertama adalah seluruh daftarnya. Setiap item adalah satu perubahan yang perlu dilakukan dalam kode Anda.

### Setiap model awal

1. Ganti ID model dengan ID Claude Haiku 5.5 untuk platform Anda. Lihat [Gunakan ID model Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#use-the-claude-haiku-5-5-model-id).
2. Hitung ulang prompt Anda, dan tinjau kembali batas `max_tokens` serta estimasi biaya, karena teks yang sama dihitung sebagai lebih banyak token dan gambar besar dihitung sebagai lebih banyak token visual. Lihat [Hitung ulang token](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#recount-tokens).
3. Jika permintaan Anda mengirim `thinking: {"type": "enabled", "budget_tokens": N}`, ubah `thinking` menjadi `{"type": "adaptive"}`. Lihat [Konfigurasikan thinking](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
4. Jika kode Anda membaca blok konten pertama sebagai jawaban, pilih blok berdasarkan `type` sebagai gantinya. Lihat [Konfigurasikan thinking](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
5. Hapus `temperature`, `top_p`, dan `top_k` dari permintaan Anda. Lihat [Hapus parameter sampling](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#remove-sampling-parameters).
6. Jika permintaan Anda mengakhiri `messages` dengan giliran asisten agar dilanjutkan oleh model, akhiri dengan giliran pengguna sebagai gantinya. Lihat [Ganti prefill asisten](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replace-assistant-prefill).
7. Jika Anda menggunakan computer use, ganti `computer_20250124`: di Claude API dan Google Cloud, dengan toolset `computer_toolset_20260801`; di Amazon Bedrock, dengan `computer_20251124` dan beta header `computer-use-2025-11-24`. Lihat [Pindahkan computer use ke toolset](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#computer-use-toolset).
8. Jika Anda memutar ulang percakapan yang tersimpan melalui akun yang berbeda, putar ulang setiap percakapan melalui akun yang menghasilkannya. Lihat [Putar ulang blok thinking melalui akun yang menghasilkannya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replay-thinking-blocks-through-the-producing-account).
9. Jika kode Anda mengubah `system`, `tools`, atau `messages` sebelumnya di antara permintaan dalam satu percakapan dan mengirim kembali blok thinking, pertahankan percakapan bersifat append-only (hanya ditambahkan). Lihat [Pertahankan giliran sebelumnya tidak berubah](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#keep-earlier-turns-unchanged).
10. Tangani `stop_reason: "refusal"`. Claude Haiku 5.5 menjalankan pengklasifikasi keamanan yang dapat menolak permintaan, dan tidak memiliki fallback di sisi server. Lihat [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#safeguard-refusals).
11. Jika Anda menggunakan ["structured outputs" (output terstruktur)](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (`output_config.format` atau alat `strict: true`) di Amazon Bedrock, jelaskan format dalam prompt atau gunakan alat tanpa `strict`, dan validasi output dalam kode Anda. Output terstruktur tidak tersedia untuk Claude Haiku 5.5 di Amazon Bedrock.

Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) pada Claude Haiku 4.5, rencanakan kapasitas secara terpisah: Priority Tier tidak didukung pada Claude Haiku 5.5.

### Claude Haiku 3.5 atau sebelumnya

1. Ganti ID model Claude Haiku 3.5 atau Claude Haiku 3 dengan ID Claude Haiku 5.5 untuk platform Anda. Lihat [Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#migrating-from-haiku-35).
2. Jika Anda menggunakan alat lama `code_execution_20250522`, pindahkan ke `code_execution_20250825` atau yang lebih baru.
3. Jika Anda menggunakan alat text editor, pindahkan ke `text_editor_20250728`.
4. Tangani alasan berhenti `refusal` dan `model_context_window_exceeded`.
5. Jika kode Anda mencocokkan parameter string pemanggilan alat secara persis, perhitungkan adanya baris baru di akhir (trailing newline).
6. Tinjau prompt Anda.

## Gunakan ID model Claude Haiku 5.5

Ganti ID model Claude Haiku 4.5 dengan ID Claude Haiku 5.5 untuk platform Anda.

| Platform               | Claude Haiku 4.5                                    | Claude Haiku 5.5             |
| ---------------------- | --------------------------------------------------- | ---------------------------- |
| Claude API             | `claude-haiku-4-5-20251001` atau `claude-haiku-4-5` | `claude-haiku-5-5`           |
| Amazon Bedrock         | `anthropic.claude-haiku-4-5`                        | `anthropic.claude-haiku-5-5` |
| Claude Platform on AWS | `claude-haiku-4-5`                                  | `claude-haiku-5-5`           |
| Google Cloud           | `claude-haiku-4-5@20251001`                         | `claude-haiku-5-5`           |
| Microsoft Foundry      | `claude-haiku-4-5`                                  | `claude-haiku-5-5`           |

`claude-haiku-5-5` adalah ID model tetap tanpa akhiran tanggal dan tanpa alias terpisah.

## Hitung ulang token

Claude Haiku 5.5 menggunakan "tokenizer" (pemecah token) baru yang sama dengan Claude 4.7 dan model-model setelahnya. Seperti semua model yang menggunakan tokenizer ini, teks input yang sama menghasilkan sekitar 30% lebih banyak token pada Claude Haiku 5.5 dibandingkan pada Claude Haiku 4.5. Peningkatan pastinya bergantung pada konten. Permintaan, respons, dan event streaming tetap memiliki bentuk yang sama. Yang berubah adalah apa pun yang Anda ukur atau anggarkan dalam token:

* Field `usage` dan hasil [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) lebih tinggi untuk teks yang sama.
* Sejumlah token tertentu memuat lebih sedikit teks.
* Batas `max_tokens` yang disetel untuk Claude Haiku 4.5 dapat memotong output yang setara.
* Estimasi biaya yang dibuat dari jumlah token Claude Haiku 4.5 perlu dihitung ulang dengan jumlah token dan [harga](https://platform.claude.com/docs/id/about-claude/pricing) Claude Haiku 5.5, termasuk harganya yang lebih tinggi untuk prompt panjang. Lihat [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing).

Gambar besar juga dapat memakan lebih banyak token. Claude Haiku 5.5 menggunakan tingkat gambar resolusi tinggi, yang memperkecil gambar di atas 2.576 piksel pada sisi terpanjang atau 4.784 token visual. Claude Haiku 4.5 dan model Haiku sebelumnya menggunakan tingkat standar, yang memperkecil gambar di atas 1.568 piksel pada sisi terpanjang atau 1.568 token visual. Gambar berukuran 2.000 kali 1.500 piksel memakan sekitar 2,5 kali lebih banyak token visual pada Claude Haiku 5.5 dibandingkan pada Claude Haiku 4.5. Lihat [Resolusi dan biaya token](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size).

Hitung prompt Anda dengan `model` diatur ke `claude-haiku-5-5` alih-alih menggunakan kembali jumlah yang diukur pada Claude Haiku 4.5.

## Konfigurasikan thinking

Claude Haiku 5.5 mengonfigurasi thinking secara berbeda dari Claude Haiku 4.5. Nilai `thinking` berupa `{"type": "enabled", "budget_tokens": N}` mengembalikan error 400, sehingga permintaan yang mengirimkannya memerlukan nilai `thinking` yang baru.

Sebelumnya, permintaan ke Claude Haiku 4.5 mengatur `thinking` ke `enabled` dengan anggaran token:

```json
{
  "model": "claude-haiku-4-5",
  "max_tokens": 16000,
  "thinking": { "type": "enabled", "budget_tokens": 8000 },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Sesudahnya, permintaan yang sama ke Claude Haiku 5.5 menggunakan "adaptive thinking" (pemikiran adaptif). Nilai `thinking` berubah, dan `output_config.effort` mengatur seberapa banyak model berpikir:

```json
{
  "model": "claude-haiku-5-5",
  "max_tokens": 16000,
  "thinking": { "type": "adaptive" },
  "output_config": { "effort": "medium" },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Pemikiran adaptif aktif secara default, sehingga respons dapat diawali dengan satu atau lebih blok `thinking` bahkan ketika permintaan tidak mengatur `thinking`. Biarkan `thinking` tidak diatur atau atur ke `{"type": "adaptive"}`, dan gunakan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai pengendali: ketika Claude Haiku 4.5 berjalan tanpa thinking, atau dengan anggaran kecil untuk menghemat token, pilih tingkat effort yang lebih rendah. Pada tingkat yang lebih rendah, model berpikir lebih sedikit, dan dapat melewati thinking sepenuhnya pada permintaan yang lebih sederhana. Untuk panduan prompting, lihat [Gunakan effort untuk mengontrol thinking](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#use-effort-to-control-thinking). Pilih blok konten berdasarkan field `type`-nya, bukan berdasarkan posisi, dan kirim kembali blok `thinking` tanpa modifikasi bersama hasil alat.

Token thinking dihitung terhadap `max_tokens`, sehingga permintaan dengan `max_tokens` kecil dapat berhenti dengan `stop_reason: "max_tokens"` setelah blok `thinking` dan sebelum teks apa pun. Jika Anda mengatur `max_tokens` kecil untuk Claude Haiku 4.5, naikkan nilainya untuk memberi ruang bagi thinking, atau pilih tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah.

Blok thinking dari giliran asisten sebelumnya tetap berada dalam konteks dan dihitung sebagai token input, sedangkan Claude Haiku 4.5 hanya menyimpan milik giliran terakhir. Oleh karena itu, percakapan multi-giliran membawa lebih banyak token input daripada yang dapat dijelaskan oleh perubahan tokenizer saja. Untuk menghapus blok yang lebih lama, gunakan [pembersihan blok thinking](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing). Lihat [Preservasi blok pemikiran berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model).

Secara default, Claude Haiku 5.5 mengembalikan setiap blok `thinking` dengan field `thinking` kosong dan hanya `signature`, sedangkan Claude Haiku 4.5 mengembalikan thinking yang diringkas. Untuk menerima thinking yang diringkas, atur `thinking: {"type": "adaptive", "display": "summarized"}`.

Claude Haiku 5.5 menerima `tool_choice` yang dipaksakan (`any` atau alat bernama), tetapi respons dimulai dengan pemanggilan alat dan tidak memiliki blok `thinking`. Agar model dapat berpikir sebelum memanggil alat, gunakan `tool_choice: {"type": "auto"}` dan sebutkan dalam prompt kapan harus menggunakan alat tersebut.

Claude Haiku 5.5 membaca blok thinking dari Claude Sonnet 5, Claude Opus 4.8, Claude Haiku 4.5, dan model sebelumnya, sehingga percakapan yang Anda alihkan dari Claude Haiku 4.5 ke Claude Haiku 5.5 tetap mempertahankan penalarannya. Model ini tidak membaca blok dari Claude Opus 5, Claude Opus 5.5, Claude Sonnet 5.5, atau model Claude Fable maupun Claude Mythos mana pun; API membuang blok tersebut tanpa error. Di Claude API dan Google Cloud, Claude Opus 5.5 dan Claude Sonnet 5.5 membaca blok dari Claude Haiku 5.5. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

## Hapus parameter sampling

Claude Haiku 4.5 menerima `temperature`, `top_p`, dan `top_k`. Pada Claude Haiku 5.5, hilangkan ketiganya dan gunakan prompting untuk mengarahkan perilaku model sebagai gantinya. Jika permintaan menyertakan `temperature`, nilainya harus `1`. Jika menyertakan `top_p`, nilainya harus `0.99`, yaitu nilai default-nya. Nilai `temperature` atau `top_p` lainnya mengembalikan error 400, termasuk `top_p` bernilai `1`. Begitu pula nilai `top_k` apa pun, dan begitu pula permintaan yang menyertakan `temperature` dan `top_p` sekaligus.

## Ganti prefill asisten

"Prefill" (pengisian awal) adalah giliran asisten terakhir dalam `messages` yang dilanjutkan oleh model. Claude Haiku 4.5 menerimanya ketika thinking nonaktif. Claude Haiku 5.5 menolaknya dengan error 400, bahkan ketika thinking dinonaktifkan. Akhiri `messages` dengan giliran pengguna, dan ganti setiap prefill sesuai dengan tujuannya:

* **Format output:** gunakan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), atau alat dengan field enum untuk klasifikasi. Di Amazon Bedrock, output terstruktur tidak tersedia untuk Claude Haiku 5.5. Di sana, jelaskan format dalam prompt atau gunakan alat tanpa `strict`, dan validasi output dalam kode Anda.
* **Pembukaan:** minta jawaban langsung dalam prompt sistem.
* **Kelanjutan:** pindahkan ke pesan pengguna, misalnya "Respons Anda sebelumnya terputus dan berakhir dengan `[previous_response]`. Lanjutkan dari bagian terakhir."
* **Pengingat konteks:** letakkan di giliran pengguna.

## Pindahkan computer use ke toolset

Claude Haiku 4.5 mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) melalui alat `computer_20250124`, dengan beta header `computer-use-2025-01-24`. Di Claude API dan Google Cloud, Claude Haiku 5.5 mendukung computer use hanya melalui toolset `computer_toolset_20260801`, dan permintaan yang mendeklarasikan `computer_20250124` mengembalikan error 400. Di Amazon Bedrock, Claude Haiku 5.5 juga tidak menerima `computer_20250124`; gunakan versi alat `computer_20251124` dengan beta header `computer-use-2025-11-24`.

Untuk memindahkan integrasi ke toolset, hapus beta header `computer-use-2025-01-24` dan ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`. Kemudian lakukan perubahan permintaan dan agent loop lainnya di [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124): lakukan dispatch berdasarkan `name` dan `toolset_name` dari setiap blok `tool_use` anggota, bukan berdasarkan `input.action`, tangani setiap blok tersebut dalam satu giliran, dan sertakan kembali `toolset_name` pada hasil. Zoom aktif secara default di toolset; jika lingkungan Anda tidak mengimplementasikannya, tambahkan `"configs": {"zoom": {"enabled": false}}`. Jika Anda mengirim beta header `fine-grained-tool-streaming-2025-05-14`, hapus header tersebut. Jika digunakan bersama entri toolset, header itu mengembalikan error 400. Untuk platform lain, lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use.

Di Claude API dan Google Cloud, Claude Haiku 5.5 juga mendukung [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) untuk tugas di dalam halaman web. Claude Haiku 4.5 tidak mendukungnya.

## Putar ulang blok thinking melalui akun yang menghasilkannya

Blok thinking dari Claude Haiku 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya. Ketika akun lain mengirim salah satu blok ini, API membuang blok tersebut sebelum model melihatnya, dan permintaan berhasil tanpa penalaran tersebut. Hal ini memengaruhi kode yang menyimpan percakapan dan memutarnya ulang melalui akun yang berbeda, misalnya layanan yang melayani beberapa pelanggan dari satu penyimpanan percakapan. Putar ulang setiap percakapan melalui akun yang menghasilkannya. Lihat [Blok pemikiran tetap berada di akun yang menghasilkannya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

## Pertahankan giliran sebelumnya tidak berubah

Blok thinking Claude Haiku 5.5 tetap valid hanya selama semua yang dikirim sebelumnya tidak berubah: permintaan yang mengirim kembali blok thinking setelah ada perubahan pada `system`, `tools`, atau `messages` sebelumnya mengembalikan error 400. Claude Haiku 4.5 tidak menjalankan pemeriksaan ini. Pertahankan percakapan bersifat append-only. Pada akun yang dibuat sebelum 31 Agustus 2026, 00:00 UTC, error hanya muncul pada permintaan yang mengatur `thinking.block_binding.prefix_mismatch_behavior`. Untuk perubahan yang memicu error dan apa yang harus dilakukan sebagai gantinya, lihat [Siapa yang perlu mengubah sesuatu](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#who-is-affected).

## Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya

Claude Haiku 3.5 telah dipensiunkan di Claude API dan Amazon Bedrock, dan Claude Haiku 3 telah dipensiunkan di Claude API dan Google Cloud. Permintaan ke model yang telah dipensiunkan akan gagal. Google Cloud mencantumkan Claude Haiku 3.5 sebagai model yang dihentikan (deprecated) dan hanya tersedia untuk pelanggan yang sudah ada. Lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

Dari model mana pun di antara keduanya, terapkan terlebih dahulu setiap bagian sebelumnya, lalu perubahan berikut:

* **ID model:** Ganti `claude-3-5-haiku-20241022`, aliasnya `claude-3-5-haiku-latest`, atau `claude-3-haiku-20240307` dengan `claude-haiku-5-5`. Di Google Cloud, ganti `claude-3-5-haiku@20241022` dengan `claude-haiku-5-5`. Di Amazon Bedrock, gunakan ID Claude Haiku 5.5 dari [Gunakan ID model Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#use-the-claude-haiku-5-5-model-id).
* **Eksekusi kode:** Claude Haiku 5.5 menerima `code_execution_20250825` dan versi yang lebih baru. Jika Anda menggunakan `code_execution_20250522` lama yang hanya mendukung Python, pindahkan ke salah satunya. Lihat [Upgrade ke versi alat terbaru](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version).
* **Text editor:** Jika Anda menggunakan alat text editor, pindahkan ke `text_editor_20250728` (nama alat `str_replace_based_edit_tool`), yang tidak memiliki perintah `undo_edit`. Lihat [Alat text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool).
* **Alasan berhenti:** Tangani `refusal` dan `model_context_window_exceeded`. Lihat [Menangani alasan berhenti](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* **Baris baru di akhir:** Claude 4.5 dan model yang lebih baru mempertahankan baris baru di akhir pada parameter string pemanggilan alat. Jika kode Anda mencocokkan string tersebut secara persis, perhitungkan keberadaannya.
* **Prompt:** Claude 4 dan model yang lebih baru memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau prompt Anda berdasarkan [Prompting Claude Haiku 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) dan [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).
