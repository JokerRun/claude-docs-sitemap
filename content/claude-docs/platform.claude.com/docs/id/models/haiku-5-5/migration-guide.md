---
source: platform
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 2ce170ad534c03ed6bcbaaf99af5623a56d5d4f73735ef7b7a69586dd678b8b4
---

---
title: Panduan migrasi Claude Haiku 5.5
url: https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide
description: Beralih ke Claude Haiku 5.5 dari model Haiku sebelumnya dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Haiku 5.5 mencakup ID model baru, pengaturan yang mengembalikan error, perubahan pemikiran, dan daftar periksa untuk setiap model awal.
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

Biarkan Claude Code memigrasikan kode Anda

```text
/claude-api migrate proyek ini ke claude-haiku-5-5
```

Panduan ini membahas pemindahan kode yang memanggil Claude Haiku 4.5 ke Claude Haiku 5.5. Untuk kode yang memanggil Claude Haiku 3.5 atau Claude Haiku 3, lakukan juga perubahan di [Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#migrating-from-haiku-35). Untuk beralih ke model Sonnet atau Opus sebagai gantinya, lihat [Panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide). Untuk mengetahui berapa lama Claude Haiku 4.5 tetap tersedia, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

## Daftar periksa migrasi berdasarkan model awal

Kerjakan grup-grup ini secara berurutan dan berhenti setelah grup yang menyebutkan model Anda saat ini. Jika Anda menggunakan Claude Haiku 4.5, grup pertama adalah seluruh daftarnya. Setiap item adalah satu perubahan yang perlu dilakukan dalam kode Anda.

### Setiap model awal

1. Ganti ID model dengan ID Claude Haiku 5.5 untuk platform Anda. Lihat [Gunakan ID model Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#use-the-claude-haiku-5-5-model-id).
2. Hitung ulang prompt Anda, dan tinjau kembali batas `max_tokens` serta estimasi biaya, karena teks yang sama dihitung sebagai lebih banyak token dan gambar berukuran besar dihitung sebagai lebih banyak token visual. Lihat [Hitung ulang token](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#recount-tokens).
3. Jika permintaan Anda mengirimkan `thinking: {"type": "enabled", "budget_tokens": N}`, ubah `thinking` menjadi `{"type": "adaptive"}`. Lihat [Konfigurasikan pemikiran](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
4. Jika kode Anda membaca blok konten pertama sebagai jawaban, pilih blok berdasarkan `type` sebagai gantinya. Lihat [Konfigurasikan pemikiran](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#configure-thinking).
5. Hapus `temperature`, `top_p`, dan `top_k` dari permintaan Anda. Lihat [Hapus parameter sampling](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#remove-sampling-parameters).
6. Jika permintaan Anda mengakhiri `messages` dengan giliran asisten agar dilanjutkan oleh model, akhiri dengan giliran pengguna sebagai gantinya. Lihat [Ganti prefill asisten](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replace-assistant-prefill).
7. Jika Anda menggunakan fitur penggunaan komputer, ganti `computer_20250124` dengan toolset `computer_toolset_20260801`. Di Amazon Bedrock, `computer_20251124` juga berfungsi. Lihat [Pindahkan penggunaan komputer ke toolset](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#computer-use-toolset).
8. Jika Anda memutar ulang percakapan yang tersimpan melalui akun yang berbeda, putar ulang masing-masing melalui akun yang menghasilkannya. Lihat [Putar ulang blok pemikiran melalui akun yang menghasilkannya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#replay-thinking-blocks-through-the-producing-account).
9. Jika kode Anda mengubah `system`, `tools`, atau `messages` sebelumnya di antara permintaan dalam sebuah percakapan dan mengirimkan kembali blok pemikiran, pertahankan percakapan agar bersifat append-only (hanya ditambahkan). Lihat [Pertahankan giliran sebelumnya tidak berubah](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#keep-earlier-turns-unchanged).
10. Tangani `stop_reason: "refusal"`. Claude Haiku 5.5 menjalankan pengklasifikasi keamanan yang dapat menolak permintaan, dan model ini tidak memiliki fallback di sisi server. Lihat [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#safeguard-refusals).

Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) pada Claude Haiku 4.5, rencanakan kapasitas secara terpisah: Priority Tier tidak didukung pada Claude Haiku 5.5.

### Claude Haiku 3.5 atau sebelumnya

1. Ganti ID model Claude Haiku 3.5 atau Claude Haiku 3 dengan ID Claude Haiku 5.5 untuk platform Anda. Lihat [Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#migrating-from-haiku-35).
2. Jika Anda menggunakan alat `code_execution_20250522`, pindah ke `code_execution_20250825` atau yang lebih baru.
3. Jika Anda menggunakan alat editor teks, pindah ke `text_editor_20250728`.
4. Tangani alasan berhenti `refusal` dan `model_context_window_exceeded`.
5. Jika kode Anda mencocokkan parameter string panggilan alat secara persis, perhitungkan adanya baris baru di akhir (trailing newline).
6. Tinjau prompt Anda.

## Gunakan ID model Claude Haiku 5.5

Ganti ID model Claude Haiku 4.5 dengan ID Claude Haiku 5.5 untuk platform Anda.

| Platform                                          | Claude Haiku 4.5                                    | Claude Haiku 5.5             |
| ------------------------------------------------- | --------------------------------------------------- | ---------------------------- |
| Claude API                                        | `claude-haiku-4-5-20251001` atau `claude-haiku-4-5` | `claude-haiku-5-5`           |
| Amazon Bedrock                                    | `anthropic.claude-haiku-4-5`                        | `anthropic.claude-haiku-5-5` |
| Claude Platform on AWS                            | `claude-haiku-4-5`                                  | `claude-haiku-5-5`           |
| Claude Models on Google Cloud (Anthropic managed) | `claude-haiku-4-5-20251001`                         | `claude-haiku-5-5`           |
| Claude Models on Google Cloud (Google managed)    | `claude-haiku-4-5@20251001`                         | `claude-haiku-5-5`           |
| Microsoft Foundry                                 | `claude-haiku-4-5`                                  | `claude-haiku-5-5`           |

`claude-haiku-5-5` adalah ID model tetap tanpa akhiran tanggal dan tanpa alias terpisah.

## Hitung ulang token

Claude Haiku 5.5 menggunakan tokenizer yang sama dengan Claude 4.7 dan model yang lebih baru. Seperti semua model yang menggunakan tokenizer ini, teks input yang sama menghasilkan sekitar 30 persen lebih banyak token pada Claude Haiku 5.5 dibandingkan pada Claude Haiku 4.5. Peningkatan pastinya bergantung pada konten. Permintaan, respons, dan event streaming mempertahankan bentuk yang sama. Yang berubah adalah apa pun yang Anda ukur atau anggarkan dalam token:

* Field `usage` dan hasil [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) lebih tinggi untuk teks yang sama.
* Sejumlah token tertentu menampung lebih sedikit teks.
* Batas `max_tokens` yang disesuaikan untuk Claude Haiku 4.5 mungkin memotong output yang setara.
* Estimasi biaya yang dibuat dari jumlah token Claude Haiku 4.5 perlu dihitung ulang dengan jumlah token dan harga Claude Haiku 5.5, termasuk harga yang lebih tinggi untuk prompt panjang. Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) dan [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing).

Gambar besar juga dapat memakan lebih banyak token. Claude Haiku 5.5 menggunakan tingkat gambar resolusi tinggi, yang memperkecil gambar di atas 2.576 piksel pada sisi terpanjang atau 4.784 token visual. Claude Haiku 4.5 dan model Haiku sebelumnya menggunakan tingkat standar, yang memperkecil gambar di atas 1.568 piksel pada sisi terpanjang atau 1.568 token visual. Gambar berukuran 2.000 kali 1.500 piksel memakan sekitar 2,5 kali lebih banyak token visual pada Claude Haiku 5.5 dibandingkan pada Claude Haiku 4.5. Lihat [Resolusi dan biaya token](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size).

Hitung prompt Anda dengan `model` diatur ke `claude-haiku-5-5` alih-alih menggunakan ulang hasil hitungan yang diukur pada Claude Haiku 4.5.

## Konfigurasikan pemikiran

Claude Haiku 5.5 mengonfigurasi pemikiran secara berbeda dari Claude Haiku 4.5. Nilai `thinking` berupa `{"type": "enabled", "budget_tokens": N}` mengembalikan error 400, sehingga permintaan yang mengirimkannya memerlukan nilai `thinking` yang baru.

Sebelumnya, permintaan ke Claude Haiku 4.5 mengatur `thinking` ke `enabled` dengan anggaran token:

```json
{
  "model": "claude-haiku-4-5",
  "max_tokens": 16000,
  "thinking": { "type": "enabled", "budget_tokens": 8000 },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Sesudahnya, permintaan yang sama ke Claude Haiku 5.5 menggunakan pemikiran adaptif. Nilai `thinking` berubah, dan `output_config.effort` mengatur seberapa banyak model berpikir:

```json
{
  "model": "claude-haiku-5-5",
  "max_tokens": 16000,
  "thinking": { "type": "adaptive" },
  "output_config": { "effort": "medium" },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Pemikiran adaptif aktif secara default, sehingga respons dapat dimulai dengan satu atau lebih blok `thinking` bahkan ketika permintaan tidak mengatur `thinking`. Biarkan `thinking` tidak diatur atau atur ke `{"type": "adaptive"}`, dan gunakan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai kontrolnya: jika Claude Haiku 4.5 berjalan tanpa pemikiran, atau dengan anggaran kecil untuk menghemat token, pilih tingkat effort yang lebih rendah. Pada tingkat yang lebih rendah, model berpikir lebih sedikit, dan dapat melewati pemikiran sepenuhnya pada permintaan yang lebih sederhana. Untuk panduan prompting, lihat [Gunakan effort untuk mengontrol pemikiran](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#use-effort-to-control-thinking). Pilih blok konten berdasarkan field `type`-nya alih-alih berdasarkan posisi, dan kirim balik blok `thinking` tanpa modifikasi bersama hasil alat.

Token pemikiran dihitung terhadap `max_tokens`, sehingga permintaan dengan `max_tokens` kecil dapat berhenti dengan `stop_reason: "max_tokens"` setelah blok `thinking` dan sebelum ada teks apa pun. Jika Anda mengatur `max_tokens` kecil untuk Claude Haiku 4.5, naikkan untuk memberi ruang bagi pemikiran, atau pilih tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah.

Blok pemikiran dari giliran asisten sebelumnya tetap berada dalam konteks dan dihitung sebagai token input, sedangkan Claude Haiku 4.5 hanya mempertahankan blok dari giliran terakhir. Karena itu, percakapan multi-giliran membawa lebih banyak token input daripada yang dapat dijelaskan oleh perubahan tokenizer saja. Untuk menghapus blok yang lebih lama, gunakan [pembersihan blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing). Lihat [Preservasi blok pemikiran berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model).

Secara default, Claude Haiku 5.5 mengembalikan setiap blok `thinking` dengan field `thinking` kosong dan hanya `signature`, sedangkan Claude Haiku 4.5 mengembalikan pemikiran yang diringkas. Untuk menerima pemikiran yang diringkas, atur `thinking: {"type": "adaptive", "display": "summarized"}`.

Claude Haiku 5.5 menerima `tool_choice` yang dipaksakan (`any` atau alat bernama), tetapi respons dimulai dengan panggilan alat dan tidak memiliki blok `thinking`. Untuk membiarkan model berpikir sebelum memanggil alat, gunakan `tool_choice: {"type": "auto"}` dan sebutkan dalam prompt kapan harus menggunakan alat tersebut.

Percakapan yang Anda alihkan dari Claude Haiku 4.5 ke Claude Haiku 5.5 tetap mempertahankan penalarannya. Untuk peralihan lainnya, hal ini bergantung pada kedua model tersebut:

| Peralihan                                                                                                                         | Mempertahankan penalarannya                                                |
| --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Ke Claude Haiku 5.5, dari Claude Haiku 4.5 atau sebelumnya, Claude Sonnet 5 atau sebelumnya, atau Claude Opus 4.8 atau sebelumnya | Ya                                                                         |
| Ke Claude Haiku 5.5, dari model lain mana pun                                                                                     | Tidak. API tidak menyertakan blok pemikiran model tersebut, tanpa error.   |
| Dari Claude Haiku 5.5, ke Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.2, atau Claude Mythos 5.2                            | Ya, hanya di Claude API dan Claude Models on Google Cloud (Google managed) |
| Dari Claude Haiku 5.5, ke model lain mana pun                                                                                     | Tidak                                                                      |

Lihat [Beralih model dan kembali lagi](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models). Untuk peralihan yang tidak melibatkan Claude Haiku 5.5, lihat [Peralihan model mana yang mempertahankan penalaran di Claude API](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#which-model-switches-keep-reasoning).

## Hapus parameter sampling

Pada Claude Haiku 5.5, hilangkan `temperature`, `top_p`, dan `top_k` dan gunakan prompting untuk mengarahkan perilaku model sebagai gantinya.

## Ganti prefill asisten

Prefill adalah giliran asisten terakhir dalam `messages` yang dilanjutkan oleh model. Claude Haiku 4.5 menerimanya ketika pemikiran dinonaktifkan. Claude Haiku 5.5 menolaknya dengan error 400, bahkan ketika pemikiran dinonaktifkan. Akhiri `messages` dengan giliran pengguna, dan ganti setiap prefill sesuai dengan tujuannya:

* **Format output:** gunakan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), atau alat dengan field enum untuk klasifikasi.
* **Pembukaan:** minta jawaban langsung dalam prompt sistem.
* **Kelanjutan:** pindahkan ke pesan pengguna, misalnya “Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off.”
* **Pengingat konteks:** letakkan di giliran pengguna.

## Pindahkan penggunaan komputer ke toolset

Claude Haiku 4.5 mendukung [penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) melalui alat `computer_20250124`, dengan header beta `computer-use-2025-01-24`. Claude Haiku 5.5 mendukung penggunaan komputer melalui toolset `computer_toolset_20260801`. Permintaan ke Claude Haiku 5.5 yang mendeklarasikan `computer_20250124` akan mengembalikan error 400.

Untuk memindahkan integrasi ke toolset, jangan sertakan lagi header beta `computer-use-2025-01-24` dan ganti entri `tools` dengan `{"type": "computer_toolset_20260801"}`. Kemudian lakukan perubahan permintaan dan agent loop lainnya di [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). Lakukan dispatch berdasarkan `name` dan `toolset_name` dari setiap blok `tool_use` anggota, bukan berdasarkan `input.action`. Tangani setiap blok tersebut dalam satu giliran dan sertakan kembali `toolset_name` pada hasil. Zoom aktif secara default di toolset; jika lingkungan Anda tidak mengimplementasikannya, tambahkan `"configs": {"zoom": {"enabled": false}}`. Jika Anda mengirimkan header beta `fine-grained-tool-streaming-2025-05-14`, hapus header tersebut. Bila digunakan bersama entri toolset, header itu akan mengembalikan error 400.

Di Amazon Bedrock, Claude Haiku 5.5 juga menerima alat `computer_20251124` dengan header beta `computer-use-2025-11-24`.

Claude Haiku 5.5 mendukung [alat penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) untuk tugas-tugas di dalam halaman web. Claude Haiku 4.5 tidak mendukungnya.

## Putar ulang blok pemikiran melalui akun yang menghasilkannya

Blok pemikiran dari Claude Haiku 5.5 hanya berfungsi di akun yang menghasilkannya atau di akun yang terhubung dengannya. Ketika akun lain mengirimkan salah satu blok ini, API tidak menyertakan blok tersebut sebelum model menerimanya, dan permintaan tetap berhasil tanpa penalaran tersebut. Hal ini memengaruhi kode yang menyimpan percakapan dan memutarnya ulang melalui akun yang berbeda, misalnya layanan yang melayani beberapa pelanggan dari satu penyimpanan percakapan. Putar ulang setiap percakapan melalui akun yang menghasilkannya. Lihat [Akun dan platform cloud](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

## Pertahankan giliran sebelumnya tidak berubah

Pertahankan percakapan agar bersifat append-only (hanya ditambahkan). Blok pemikiran Claude Haiku 5.5 hanya tetap valid selama semua yang dikirim sebelumnya tidak berubah: prompt `system`, `tools`, dan setiap pesan sebelumnya.

Gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) mungkin menghasilkan atau mungkin tidak menghasilkan [error 400](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch). Untuk mengidentifikasi dan menangani kedua kasus tersebut, lihat [Pemeriksaan prefiks pada blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks).

Untuk perubahan yang memicu error dan apa yang harus dilakukan sebagai gantinya, lihat [Jika kode Anda mengubah prompt sistem, alat, atau riwayat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-to-check).

## Migrasi ke Claude Haiku 5.5 dari Claude Haiku 3.5 dan model Haiku sebelumnya

Claude Haiku 3.5 telah dipensiunkan di Claude API, Amazon Bedrock, dan Claude Models on Google Cloud (Google managed). Claude Haiku 3 telah dipensiunkan di Claude API dan Claude Models on Google Cloud (Google managed). Lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

Dari model mana pun di antara keduanya, terapkan terlebih dahulu setiap bagian sebelumnya, lalu perubahan berikut:

* **ID model:** Ganti `claude-3-5-haiku-20241022`, aliasnya `claude-3-5-haiku-latest`, atau `claude-3-haiku-20240307` dengan `claude-haiku-5-5`. Di Claude Models on Google Cloud (Google managed), ganti `claude-3-5-haiku@20241022` dengan `claude-haiku-5-5`. Di Amazon Bedrock, gunakan ID Claude Haiku 5.5 dari [Gunakan ID model Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/migration-guide#use-the-claude-haiku-5-5-model-id).
* **Eksekusi kode:** Claude Haiku 5.5 menerima `code_execution_20250825` dan versi yang lebih baru. Jika Anda menggunakan `code_execution_20250522` yang hanya mendukung Python, pindah ke salah satunya. Lihat [Upgrade ke versi alat terbaru](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version).
* **Editor teks:** Jika Anda menggunakan alat editor teks, pindah ke `text_editor_20250728` (nama alat `str_replace_based_edit_tool`), yang tidak memiliki perintah `undo_edit`. Lihat [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool).
* **Alasan berhenti:** Tangani `refusal` dan `model_context_window_exceeded`. Lihat [Alasan berhenti dan fallback](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* **Baris baru di akhir:** Claude 4.5 dan model yang lebih baru mempertahankan baris baru di akhir (trailing newline) dalam parameter string panggilan alat. Jika kode Anda mencocokkan string tersebut secara persis, perhitungkan keberadaannya.
* **Prompt:** Claude 4 dan model yang lebih baru memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan yang eksplisit. Tinjau prompt Anda berdasarkan [Menulis prompt untuk Claude Haiku 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) dan [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).
