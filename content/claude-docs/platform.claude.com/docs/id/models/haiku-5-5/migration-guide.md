---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: d6767419db8b67d5984dc7c46ba0480f67c9898d5dd0f0d81a287fe3c9f98ba9
---

---
title: Panduan migrasi Claude Haiku 5.5
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
description: Beralih ke Claude Haiku 5.5 dari Claude Haiku 4.5 dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Haiku 5.5 mencakup ID model baru, setiap perubahan yang merusak kompatibilitas beserta permintaan sebelum dan sesudahnya, serta daftar periksa migrasi.
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

Panduan ini membahas pemindahan kode yang memanggil Claude Haiku 4.5 ke Claude Haiku 5.5. Untuk beralih ke model Sonnet atau Opus, lihat [Upgrade antar versi model](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Untuk mengetahui berapa lama Claude Haiku 4.5 tetap tersedia, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

## Daftar periksa migrasi

Setiap item adalah satu perubahan yang perlu dilakukan pada kode yang memanggil Claude Haiku 4.5.

1. Ganti ID model dengan ID Claude Haiku 5.5 untuk platform Anda. Lihat [Gunakan ID model Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#use-the-claude-haiku-5-5-model-id).
2. Hitung ulang prompt Anda, dan tinjau kembali batas `max_tokens` serta estimasi biaya, karena teks yang sama dihitung sebagai lebih banyak token. Lihat [Hitung ulang token](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#recount-tokens).
3. Jika permintaan Anda mengirim `thinking: {"type": "enabled", "budget_tokens": N}`, ubah `thinking` menjadi `{"type": "adaptive"}`. Lihat [Konfigurasikan thinking](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
4. Jika kode Anda membaca blok konten pertama sebagai jawaban, pilih blok berdasarkan `type` sebagai gantinya. Lihat [Konfigurasikan thinking](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
5. Hapus `temperature`, `top_p`, dan `top_k` dari permintaan Anda. Lihat [Hapus parameter sampling](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#remove-sampling-parameters).
6. Jika permintaan Anda mengakhiri `messages` dengan giliran asisten agar dilanjutkan oleh model, akhiri dengan giliran pengguna sebagai gantinya. Lihat [Ganti prefill asisten](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replace-assistant-prefill).
7. Jika Anda menggunakan computer use di Claude API atau Google Cloud, pindahkan dari `computer_20250124` ke toolset `computer_toolset_20260801`. Lihat [Pindahkan computer use ke toolset](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#computer-use-toolset).
8. Jika Anda memutar ulang percakapan yang tersimpan melalui akun yang berbeda, putar ulang setiap percakapan melalui akun yang menghasilkannya. Lihat [Putar ulang blok thinking melalui akun yang menghasilkannya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replay-thinking-blocks-through-the-producing-account).
9. Jika kode Anda mengubah `system`, `tools`, atau `messages` sebelumnya di antara permintaan dalam satu percakapan dan mengirim kembali blok thinking, pertahankan percakapan bersifat append-only (hanya ditambahkan). Lihat [Pertahankan giliran sebelumnya tidak berubah](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#keep-earlier-turns-unchanged).
10. Tangani `stop_reason: "refusal"`. Claude Haiku 5.5 menjalankan pengklasifikasi keamanan yang dapat menolak permintaan, dan tidak memiliki fallback di sisi server. Lihat [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#safeguard-refusals).

Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) pada Claude Haiku 4.5, rencanakan kapasitas secara terpisah: Priority Tier tidak didukung pada Claude Haiku 5.5.

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
* Estimasi biaya yang dibuat dari jumlah token Claude Haiku 4.5 perlu dihitung ulang dengan jumlah token dan [harga](https://platform.claude.com/docs/id/about-claude/pricing) Claude Haiku 5.5.

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

Secara default, Claude Haiku 5.5 mengembalikan setiap blok `thinking` dengan field `thinking` kosong dan hanya `signature`, sedangkan Claude Haiku 4.5 mengembalikan thinking yang diringkas. Untuk menerima thinking yang diringkas, atur `thinking: {"type": "adaptive", "display": "summarized"}`.

Claude Haiku 5.5 menerima `tool_choice` yang dipaksakan (`any` atau alat bernama), tetapi respons dimulai dengan pemanggilan alat dan tidak memiliki blok `thinking`. Agar model dapat berpikir sebelum memanggil alat, gunakan `tool_choice: {"type": "auto"}` dan sebutkan dalam prompt kapan harus menggunakan alat tersebut.

## Hapus parameter sampling

Claude Haiku 4.5 menerima `temperature`, `top_p`, dan `top_k`. Pada Claude Haiku 5.5, hilangkan ketiganya dan gunakan prompting untuk mengarahkan perilaku model sebagai gantinya. Jika permintaan menyertakan `temperature`, nilainya harus `1`. Jika menyertakan `top_p`, nilainya harus `0.99`, yaitu nilai default-nya. Nilai `temperature` atau `top_p` lainnya mengembalikan error 400, termasuk `top_p` bernilai `1`. Begitu pula nilai `top_k` apa pun, dan begitu pula permintaan yang menyertakan `temperature` dan `top_p` sekaligus.

## Ganti prefill asisten

"Prefill" (pengisian awal) adalah giliran asisten terakhir dalam `messages` yang dilanjutkan oleh model. Claude Haiku 4.5 menerimanya ketika thinking nonaktif. Claude Haiku 5.5 menolaknya dengan error 400, bahkan ketika thinking dinonaktifkan. Akhiri `messages` dengan giliran pengguna, dan ganti setiap prefill sesuai dengan tujuannya:

* **Format output:** gunakan ["structured outputs" (output terstruktur)](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), atau alat dengan field enum untuk klasifikasi. Pada Claude di Amazon Bedrock, yang tidak mendukung output terstruktur, gunakan alat.
* **Pembukaan:** minta jawaban langsung dalam prompt sistem.
* **Kelanjutan:** pindahkan ke pesan pengguna, misalnya "Respons Anda sebelumnya terputus dan berakhir dengan `[previous_response]`. Lanjutkan dari bagian terakhir."
* **Pengingat konteks:** letakkan di giliran pengguna.

## Pindahkan computer use ke toolset

Claude Haiku 4.5 mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) melalui alat `computer_20250124`, dengan header beta `computer-use-2025-01-24`. Di Claude API dan Google Cloud, Claude Haiku 5.5 mendukung computer use hanya melalui toolset `computer_toolset_20260801`, dan permintaan yang mendeklarasikan `computer_20250124` mengembalikan error 400.

Untuk memindahkan integrasi, hapus header beta `computer-use-2025-01-24` dan ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`. Kemudian lakukan perubahan permintaan dan loop agen lainnya di [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124): lakukan dispatch berdasarkan `name` dan `toolset_name` dari setiap blok `tool_use` anggota, bukan berdasarkan `input.action`, tangani setiap blok tersebut dalam satu giliran, dan sertakan kembali `toolset_name` pada hasil. Zoom aktif secara default di toolset; jika lingkungan Anda tidak mengimplementasikannya, tambahkan `"configs": {"zoom": {"enabled": false}}`. Jika Anda mengirim header beta `fine-grained-tool-streaming-2025-05-14`, hapus header tersebut. Bersama entri toolset, header itu mengembalikan error 400. Untuk platform lain, lihat bagian [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility) pada alat computer use.

Di Claude API dan Google Cloud, Claude Haiku 5.5 juga mendukung [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) untuk tugas di dalam halaman web. Claude Haiku 4.5 tidak mendukungnya.

## Putar ulang blok thinking melalui akun yang menghasilkannya

Blok thinking dari Claude Haiku 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya. Ketika akun lain mengirim salah satu blok ini, API membuang blok tersebut sebelum model melihatnya, dan permintaan berhasil tanpa penalaran tersebut. Hal ini memengaruhi kode yang menyimpan percakapan dan memutarnya ulang melalui akun yang berbeda, misalnya layanan yang melayani beberapa pelanggan dari satu penyimpanan percakapan. Putar ulang setiap percakapan melalui akun yang menghasilkannya. Lihat [Blok pemikiran tetap berada di akun yang menghasilkannya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

## Pertahankan giliran sebelumnya tidak berubah

Blok thinking Claude Haiku 5.5 tetap valid hanya selama semua yang dikirim sebelumnya tidak berubah: permintaan yang mengirim kembali blok thinking setelah ada perubahan pada `system`, `tools`, atau `messages` sebelumnya mengembalikan error 400. Claude Haiku 4.5 tidak menjalankan pemeriksaan ini. Pertahankan percakapan bersifat append-only. Pada akun yang dibuat sebelum 31 Agustus 2026, 00:00 UTC, error hanya muncul pada permintaan yang mengatur `thinking.block_binding.prefix_mismatch_behavior`. Untuk perubahan yang memicu error dan apa yang harus dilakukan sebagai gantinya, lihat [Siapa yang perlu mengubah sesuatu](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#who-is-affected).
