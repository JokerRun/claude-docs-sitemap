---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 53bdc0db0cb8ef4fbe25917203331aea6e1802876bf68454dbacaedc88d4b474
---

---
title: Pemikiran yang dipertahankan
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking
description: Memodifikasi percakapan kini menghasilkan error atau blok yang dibuang; cara memeriksa apakah integrasi Anda melakukan hal itu dan cara bermigrasi.
---

Pada Claude Fable 5.1, mengubah giliran sebelumnya dalam percakapan (prompt `system`, `tools`, atau pesan apa pun yang lebih awal) memengaruhi respons API. Secara default, hal ini membuat API menolak permintaan dengan error, kecuali Anda memilih agar blok thinking yang terdampak dibuang dari apa yang dilihat model (`prefix_mismatch_behavior: "drop_block"`). Pemeriksaan ini diberlakukan secara default untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC. Detail lebih lanjut ada di *[Cara kerjanya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#how-it-works)* dan *[Siapa yang terdampak](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#who-is-affected).*

Saat Anda mengirim kembali sebuah blok, API menggunakan `signature`-nya untuk memeriksa bahwa percakapan sebelumnya tidak berubah dan bahwa model saat ini dapat membaca blok tersebut. Pemeriksaan ini ada agar penalaran yang dihasilkan di bawah satu set instruksi tidak dapat diputar ulang di bawah set instruksi lain yang berpotensi bersifat adversarial.

API menyediakan alternatif kelas satu untuk memodifikasi percakapan seiring berjalannya, yang mencakup sebagian besar kasus penggunaan untuk pengeditan transkrip: [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) untuk instruksi baru, [pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) untuk pengingat per giliran, [perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) untuk menambah dan menghapus alat, dan [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) untuk menyesuaikan kedalaman pemikiran per giliran. Sisa halaman ini membahas cara mengetahui apakah integrasi Anda terdampak dan cara memigrasikan pola harness umum ke fitur-fitur ini. Sebagai manfaat tambahan, menjaga segala sesuatu sebelum setiap blok thinking tidak berubah byte demi byte juga menjaga prefiks tetap stabil untuk "prompt caching" ([caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)).

Apakah Anda perlu melakukan sesuatu bergantung pada apa yang mengelola riwayat percakapan Anda:

* **Anda menggunakan produk atau SDK resmi Claude:** Claude Code, claude.ai, [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), atau [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview). Semua ini menjaga prefiks tetap utuh untuk Anda.

* **Anda memanggil Messages API secara langsung**, dari loop agen Anda sendiri atau pengaturan lainnya. Anda harus memeriksa kode Anda dan memastikan bahwa array `messages` diperlakukan sebagai append-only (hanya-tambah). Pola umum berikut mengedit prefiks dan membatalkan validitas thinking setelah pengeditan tersebut:

  * Memangkas atau membuang giliran yang lebih lama
  * Merangkum giliran yang lebih lama di sisi klien dan mempertahankan giliran terbaru
  * Menyisipkan pengingat ke giliran yang lebih awal dan menghapusnya pada permintaan berikutnya
  * Membangun ulang prompt `system` pada setiap permintaan (waktu saat ini, anggaran token, flag mode)
  * Menambah atau menghapus entri dalam `tools` di tengah sesi

## Cara kerjanya

Untuk permintaan baru, API memeriksa:

* **Modelnya sama atau lebih baru.** Sebuah blok dapat dibaca oleh model yang menghasilkannya dan oleh model yang lebih baru, bukan oleh model yang lebih lama. Percakapan yang berpindah ke model yang lebih baru mempertahankan penalarannya. Percakapan yang berpindah ke model yang lebih lama gagal dalam pemeriksaan model untuk blok-blok tersebut, dan API membuangnya untuk permintaan itu. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-for-model) untuk daftar persis per model.
* **Tidak ada yang berubah sebelum blok tersebut.** Prompt `system` tingkat atas, set alat dalam `tools`, dan setiap pesan sebelum blok tersebut. Dengan compaction sisi server, prefiks yang diperiksa dimulai dari [blok compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) terbaru.
* **Rantai blok thinking sebelumnya tidak terputus.** Blok `thinking` dan `redacted_thinking` yang lebih awal bukan bagian dari prefiks, tetapi setiap blok thinking mencatat blok sebelumnya, lintas giliran. Anda dapat menghapus blok thinking dari bagian depan riwayat. Menghapus satu dari tengah membatalkan validitas setiap blok thinking setelahnya.

Blok yang gagal dalam pemeriksaan model selalu dibuang. Untuk ketidakcocokan prefiks, Anda memilih apa yang terjadi dengan `thinking.block_binding.prefix_mismatch_behavior`, yang memerlukan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01`:

* `"drop_block"`: API menghapus blok tersebut dan setiap blok thinking setelahnya dalam percakapan, dan permintaan berhasil. Blok yang dibuang tidak ditagih. Respons mencantumkannya dalam array `input_transformations` tingkat atas (pada event `message_start` saat streaming).
* `"error"`: API menolak permintaan dengan 400 `invalid_request_error` yang menyebutkan blok pertama yang gagal.

Default-nya adalah `"error"`. Header tersebut memungkinkan Anda mengatur field ini dan menambahkan `input_transformations` ke respons.

## Siapa yang terdampak

Claude Fable 5.1. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking) untuk daftar model.

Pada Claude Fable 5.1, API memberlakukan pemeriksaan ini untuk akun baru. Akun baru adalah akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC. Definisi yang sama berlaku pada Claude API dan pada platform cloud. Model-model selanjutnya akan memberlakukan pemeriksaan ini untuk semua pengguna.

Permintaan yang mengatur `prefix_mismatch_behavior` ikut serta dalam pemberlakuan terlepas dari usia akun, dan inilah cara Anda menguji dari akun yang lebih lama. Untuk memeriksa apakah akun Anda diberlakukan secara default, kirim permintaan yang mengedit riwayat tanpa header beta: respons 400 yang menyebutkan header tersebut berarti diberlakukan.

<Note>
  Jika Anda memelihara alat atau framework yang dijalankan orang dengan kunci API mereka sendiri, pengguna Anda pada akun baru akan terkena pemeriksaan ini sebelum Anda: kunci Anda sendiri kemungkinan berada pada akun yang lebih lama. Uji dengan `prefix_mismatch_behavior` yang diatur agar Anda melihat apa yang akan mereka lihat.
</Note>

## Cara mengetahui apakah integrasi Anda terdampak

Tangkap body permintaan persis yang dikirim integrasi Anda selama beberapa giliran normal, termasuk compaction atau perubahan alat jika produk Anda melakukannya. Untuk setiap pasangan permintaan berurutan, bandingkan `system`, `tools`, dan bagian `messages` yang sama. Semuanya harus identik byte demi byte hingga giliran yang baru ditambahkan.

Kemudian konfirmasikan terhadap API. Dengan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01` dan `claude-fable-5-1`, atur `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"` dan jalankan sesi multi-giliran normal melalui integrasi Anda. Permintaan ini adalah giliran kedua dari sesi semacam itu, yang mengirim kembali giliran asisten dari respons pertama persis seperti yang diterima:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
  -d '{
    "model": "claude-fable-5-1",
    "max_tokens": 16000,
    "thinking": {
      "type": "adaptive",
      "block_binding": { "prefix_mismatch_behavior": "drop_block" }
    },
    "system": "You are a coding agent.",
    "messages": [
      { "role": "user", "content": "Fix the failing test." },
      {
        "role": "assistant",
        "content": [
          { "type": "thinking", "thinking": "", "signature": "EqQBCkYIBxgCKkD..." },
          { "type": "text", "text": "I need to see the test first. Which file is it in?" }
        ]
      },
      { "role": "user", "content": "tests/test_auth.py" }
    ]
  }'
```

Setiap respons kemudian membawa array `input_transformations` tingkat atas. Catat dalam log pada setiap giliran:

```json
{
  "input_transformations": [
    {
      "type": "thinking_dropped",
      "path": "messages.1.content.0",
      "reason": "prefix_binding_mismatch"
    }
  ]
}
```

* **Kosong pada setiap giliran:** integrasi Anda menjaga riwayat tetap utuh.
* **`reason: "prefix_binding_mismatch"`:** sesuatu sebelum blok di `path` berubah antara permintaan ini dan permintaan sebelumnya. Lakukan diff pada `system`, `tools`, dan `messages` hingga giliran tersebut untuk menemukannya.
* **`reason: "model_binding_mismatch"`:** percakapan berpindah ke model yang tidak dapat membaca blok dari model sebelumnya (router, fallback). Bukan bug dalam integrasi Anda. Tetap kirim blok-blok tersebut dan biarkan API membuang apa yang tidak dapat dibaca model saat ini.

Ini berfungsi dari akun mana pun, karena mengatur field tersebut membuat permintaan ikut serta dalam pemberlakuan. Untuk gagal secara eksplisit di CI, atur `"error"`. Respons 400 dimulai dengan:

```text wrap
messages.1.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

Tanpa header beta pada permintaan, pesan berlanjut: ``That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.`` Pesan biasanya diakhiri dengan kalimat yang menyebutkan apa yang berubah, misalnya bahwa prompt `system` atau daftar `tools` berbeda dari saat blok tersebut dibuat.

Lihat [Pemecahan masalah thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-block-signature) untuk setiap varian error ini.

## Apa yang dihitung sebagai pengeditan

Antara dua permintaan berurutan:

| Perubahan antar permintaan                                                                                                                                                       | Blok thinking selanjutnya                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Menambahkan pesan di akhir                                                                                                                                                       | Valid                                                                                   |
| Menambahkan alat dengan `defer_loading: true` yang belum direferensikan oleh apa pun                                                                                             | Valid                                                                                   |
| Menghapus blok `thinking` dari awal riwayat (setiap blok thinking sebelum titik tertentu)                                                                                        | Valid                                                                                   |
| Mengubah parameter permintaan apa pun di luar `system`, `tools`, dan `messages` (`max_tokens`, `output_config`, `tool_choice`, `metadata`, dan seterusnya)                       | Valid                                                                                   |
| Menambah, memindahkan, atau menghapus penanda `cache_control`                                                                                                                    | Valid                                                                                   |
| Signed URL yang berotasi yang mengembalikan byte yang sama                                                                                                                       | Valid                                                                                   |
| Compaction sisi server atau context editing menghapus atau mengganti konten                                                                                                      | Valid (pemeriksaan membandingkan apa yang Anda kirim, bukan salinan yang diedit server) |
| [Pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) yang sudah dibersihkan dan dibiarkan di tempatnya | Valid                                                                                   |
| Mengedit, mengurutkan ulang, atau menghapus pesan `user`, `assistant`, atau `system` yang lebih awal                                                                             | Tidak valid                                                                             |
| Menambahkan blok teks ke giliran user yang lebih awal, atau menghapus yang Anda tambahkan terakhir kali                                                                          | Tidak valid                                                                             |
| Mengubah string atau blok `system` tingkat atas                                                                                                                                  | Tidak valid                                                                             |
| Menambah, menghapus, mengganti nama, atau mengedit alat dalam `tools`                                                                                                            | Tidak valid                                                                             |
| Menghapus blok `thinking` dari tengah riwayat dan mempertahankan yang setelahnya                                                                                                 | Tidak valid untuk setiap blok thinking setelahnya                                       |
| URL gambar atau dokumen yang mengembalikan byte berbeda pada permintaan berikutnya                                                                                               | Tidak valid                                                                             |
| Pesan bercakupan giliran yang sama dihapus atau diubah kata-katanya pada permintaan selanjutnya                                                                                  | Tidak valid                                                                             |

## Perbarui integrasi Anda

Setiap pola menggantikan satu jenis pengeditan riwayat dengan fitur API yang memiliki efek yang sama pada model tanpa mengubah byte yang lebih awal.

### Tambahkan giliran asisten persis seperti yang dikembalikan

Simpan array `content` dari setiap respons dan kirim kembali tanpa perubahan sebagai giliran asisten, setiap tipe blok dalam urutan yang diterima, termasuk blok `thinking` yang field `thinking`-nya kosong. Jangan melakukan reserialisasi melalui tipe perantara yang membuang tipe blok yang tidak dikenal atau field kosong.

### Tambahkan instruksi dengan pesan sistem di tengah percakapan, bukan dengan mengedit `system`

Jika kode Anda membangun ulang prompt `system` tingkat atas pada setiap permintaan (waktu saat ini, anggaran token, flag mode, konteks proyek yang baru ditemukan), setiap blok thinking dalam percakapan gagal dalam pemeriksaan. Bekukan `system` di awal sesi, dan ketika sesuatu berubah, tambahkan [pesan `role: "system"`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) pada titik dalam `messages` di mana hal itu menjadi benar:

```json
{
  "role": "system",
  "content": "The user switched the workspace to read-only mode. Do not write files until told otherwise."
}
```

Model memperlakukannya dengan otoritas prompt sistem, dan segala sesuatu sebelumnya tidak berubah. Tidak diperlukan header beta pada Claude Fable 5.1. Dalam loop alat, tempatkan setelah pesan user `tool_result`, jangan pernah di antara `tool_use` asisten dan `tool_result`-nya (lihat [Keterbatasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)).

### Kirim pengingat per giliran sebagai pesan sistem bercakupan giliran

Pengeditan riwayat yang paling umum adalah dorongan per giliran: sebuah baris yang ditambahkan setelah setiap batch hasil alat ("minta pembacaan independen secara bersamaan", "Anda sudah lama tidak memberi kabar kepada pengguna") dan dihapus pada permintaan berikutnya agar pengingat tidak menumpuk. Menghapusnya adalah pengeditan tersebut.

Sebagai gantinya, kirim dorongan tersebut sebagai [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dengan `clear_at: "next_user_message"` setelah pesan user `tool_result` (header beta `mid-conversation-system-clear-at-2026-08-21`). Array `messages` ini adalah permintaan setelah dua putaran alat. `messages[3]` adalah dorongan dari permintaan sebelumnya, dibiarkan di tempatnya, dan `messages[6]` adalah salinan untuk permintaan ini:

```json
[
  { "role": "user", "content": "Fix the failing test." },
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "", "signature": "..." },
      {
        "type": "tool_use",
        "id": "toolu_01",
        "name": "read_file",
        "input": { "path": "tests/test_auth.py" }
      }
    ]
  },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "toolu_01", "content": "..." }]
  },
  {
    "role": "system",
    "clear_at": "next_user_message",
    "content": "Request every independent read in one turn."
  },
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "", "signature": "..." },
      {
        "type": "tool_use",
        "id": "toolu_02",
        "name": "read_file",
        "input": { "path": "src/auth.py" }
      }
    ]
  },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "toolu_02", "content": "..." }]
  },
  {
    "role": "system",
    "clear_at": "next_user_message",
    "content": "Request every independent read in one turn."
  }
]
```

Pesan user yang hanya berisi `tool_result` dihitung sebagai "pesan user berikutnya", sehingga `messages[3]` sudah dibersihkan: pesan itu tidak merender apa pun dan tidak memakan token input, tetapi masih ada dalam array, sehingga thinking dalam `messages[4]` tetap valid. `messages[6]` adalah apa yang dilihat model pada giliran ini. Pada permintaan selanjutnya, biarkan keduanya di tempatnya dan tambahkan salinan berikutnya setelah pesan `tool_result` berikutnya. Pesan bercakupan giliran hanya membawa `text` dan tidak menerima `cache_control`. Letakkan breakpoint cache pada giliran user sebelumnya. Lihat [Pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages).

Tanpa beta, tambahkan dorongan tersebut sebagai blok `text` setelah blok-blok `tool_result` dalam pesan user yang sama, dan biarkan salinan yang lebih awal di tempatnya. Model bertindak berdasarkan yang terbaru.

### Ubah alat dengan `tool_addition` dan `tool_removal`, bukan dengan mengedit `tools`

Jika set alat berubah di tengah sesi (sebuah alat terbuka setelah autentikasi, alat berbahaya ditarik setelah pergantian mode), jangan edit `tools`. Deklarasikan set lengkap di awal sesi dan gunakan [perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) untuk menawarkan atau menarik alat sejak titik itu (header beta `mid-conversation-tool-changes-2026-07-01`). Alat yang belum tersedia mendapat `defer_loading: true` dan blok `tool_addition` di kemudian waktu, dengan bentuk yang sama seperti `tool_removal` ini:

```json
{
  "role": "system",
  "content": [
    { "type": "tool_removal", "tool": { "type": "tool_reference", "name": "delete_branch" } },
    { "type": "text", "text": "Branch deletion is disabled for the rest of this session." }
  ]
}
```

Alat yang skemanya Anda ketahui di tengah sesi (server MCP yang ditemukan saat runtime) dapat ditambahkan ke `tools` dengan `defer_loading: true` dan ditawarkan dengan `tool_addition`. Alat deferred yang belum direferensikan bukan bagian dari prefiks, sehingga menambahkannya aman. Menambahkan alat biasa tidak aman.

### Pangkas konteks di server jika memungkinkan

Pemotongan dan perangkuman sisi klien adalah pengeditan paling umum kedua: membuang atau merangkum giliran terlama dan mempertahankan giliran terbaru secara verbatim. Blok thinking pada giliran terbaru dihasilkan saat riwayat yang Anda hapus masih ada, sehingga gagal dalam pemeriksaan. Padanan sisi server tidak dihitung sebagai pengeditan, karena pemeriksaan membandingkan percakapan sebagaimana Anda mengirimnya:

* [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) merangkum giliran yang lebih lama menjadi blok compaction ketika konteks mendekati ambang yang Anda tetapkan, dan prefiks yang diperiksa dimulai ulang dari blok tersebut. [Parameter `instructions`](https://platform.claude.com/docs/id/build-with-claude/compaction#custom-summarization-instructions)-nya menerima prompt perangkuman Anda sendiri ("pertahankan setiap ticker, ukuran posisi, dan asumsi yang dinyatakan").
* [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) membersihkan hasil alat lama (`clear_tool_uses_20250919`) atau blok thinking lama dari yang terlama terlebih dahulu (`clear_thinking_20251015`) berdasarkan aturan.

### Compaction kustom di sisi klien

Pemeriksaan ini tidak melarang compaction sisi klien. Aturannya lebih sempit: **jangan pertahankan blok thinking di belakang prefiks yang telah Anda tulis ulang.**

**Compaction sederhana** adalah bentuk yang direkomendasikan dan tidak memerlukan perubahan. Ketika percakapan menjadi terlalu panjang, rangkum menjadi satu pesan dan mulai permintaan berikutnya dengan rangkuman tersebut ditambah giliran user baru, tanpa memutar ulang giliran atau blok thinking yang lebih awal: `messages` menjadi `[{"role": "user", "content": "<summary of the session so far>\n\n<the next instruction>"}]`. Tidak ada thinking yang lebih awal yang tersisa, sehingga tidak ada yang gagal, dan model berpikir dari awal pada percakapan yang telah di-compact. Model Claude dilatih pada tugas berjangka panjang dengan skema ini, dan kinerjanya sebanding dengan skema yang lebih rumit untuk sebagian besar beban kerja. Skema ini mereset cache prompt pada titik compaction, seperti halnya compaction apa pun.

Dua bentuk umum lainnya gagal sebagaimana tertulis dan masing-masing memerlukan satu perubahan:

* **Compaction keep-tail** merangkum giliran yang lebih lama dan mempertahankan giliran terbaru secara verbatim. Blok thinking pada giliran yang dipertahankan dihasilkan terhadap riwayat lengkap, sehingga gagal di belakang rangkuman. Perbaikan: hapus `thinking` dan `redacted_thinking` dari setiap giliran asisten yang Anda bawa, dengan mempertahankan `text` dan `tool_use`, atau kirim `prefix_mismatch_behavior: "drop_block"` dan biarkan API menghapusnya.
* **Compaction latar belakang** membangun rangkuman di luar jalur kritis dan menukarnya masuk sementara percakapan berlanjut, sehingga setiap giliran yang dihasilkan selama itu memiliki thinking yang mendahului penukaran. Perbaikan: kirim `"drop_block"` pada setiap permintaan yang masih membawa blok thinking yang dihasilkan sebelum penukaran (atau hapus sendiri blok-blok tersebut; `input_transformations` pada respons pertama setelah penukaran mencantumkan persis blok mana saja), atau lakukan compaction secara sinkron.

Memotong giliran individual dari tengah transkrip membatalkan validitas segala sesuatu setelahnya, dan tidak ada bentuk sisi klien yang menghindari hal itu. Gunakan pesan sistem di tengah percakapan untuk perubahan instruksi yang Anda buat, atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) sisi server untuk penghapusan selektif.

Jangan lakukan compaction di tengah putaran alat: giliran asisten yang `tool_use`-nya masih menunggu `tool_result` harus dikirim kembali dengan thinking-nya utuh, agar model menyelesaikan putaran dengan penalarannya (lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)).

### Referensikan file berdasarkan ID, bukan berdasarkan URL yang kontennya berubah

Untuk blok `image` atau `document` dengan sumber `url`, byte yang diambil adalah bagian dari prefiks yang diperiksa dan string URL-nya bukan. Endpoint "screenshot terbaru" atau dokumen yang diedit membatalkan validitas thinking selanjutnya. Signed URL yang berotasi untuk file yang sama tidak. Untuk konten yang Anda referensikan lintas giliran, unggah sekali dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan gunakan `file_id`, atau kirim base64.

### Tentukan apa yang terjadi saat ketidakcocokan

Setelah integrasi Anda bersifat append-only, pilih `prefix_mismatch_behavior` untuk produksi. Ini hanya mengatur ketidakcocokan prefiks. Blok yang tidak dapat dibaca model saat ini (setelah pergantian router atau [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback)) selalu dibuang, dan dilaporkan dalam `input_transformations` ketika header beta dikirim.

* **`"error"`** (default) jika ketidakcocokan prefiks hanya bisa berarti bug dalam kode Anda. Anda mengetahuinya dari respons 400 dalam pengujian, bukan dari blok yang dibuang secara diam-diam. Dalam Message Batches API, default yang tidak diatur membuang blok yang gagal alih-alih menggagalkan item batch; atur `"error"` secara eksplisit jika Anda ingin item menghasilkan error.
* **`"drop_block"`** jika Anda lebih memilih membuang blok yang terdampak daripada gagal. Catat `input_transformations` dalam log.

Jika Anda menangkap respons 400 di produksi, mencoba ulang permintaan yang sama tidak akan menyelesaikannya. Coba ulang dengan `prefix_mismatch_behavior: "drop_block"` (dan header beta), yang menghapus persis blok-blok yang gagal, termasuk yang ada dalam giliran asisten yang `tool_use`-nya masih menunggu `tool_result`-nya. Pembuangan hanya berlaku untuk permintaan itu, jadi tetap kirim `"drop_block"` (dan header beta) untuk sisa sesi. Tanpa beta, hapus setiap blok `thinking` dan `redacted_thinking` dari riwayat, dengan membiarkan blok `text` dan `tool_use` setiap giliran di tempatnya, dan coba ulang sekali. Kemudian perbaiki pengeditan yang menyebabkannya.

## Fitur API yang digunakan di halaman ini

| Fitur                                                                                                                                                                                                                  | Apa yang digantikannya                                                                                                    | Status | Header                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------- |
| [Kontrol untuk blok yang tidak dipertahankan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking-controls) (`thinking.block_binding.prefix_mismatch_behavior`, `input_transformations`) | Memilih tolak atau buang saat ketidakcocokan prefiks, dan melihat apa yang dibuang                                        | Beta   | `thinking-binding-controls-2026-08-01`        |
| [Pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) (`role: "system"` dalam `messages`)                                                        | Membangun ulang prompt `system` tingkat atas                                                                              | Stabil | Tidak ada                                     |
| [Pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders) (`clear_at: "next_user_message"`)                                                       | Menyisipkan pengingat dan menghapusnya pada permintaan berikutnya                                                         | Beta   | `mid-conversation-system-clear-at-2026-08-21` |
| [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) (`tool_addition`, `tool_removal`)                          | Mengedit array `tools`                                                                                                    | Beta   | `mid-conversation-tool-changes-2026-07-01`    |
| [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) (`instructions` untuk prompt rangkuman kustom)                                                                                          | Perangkuman giliran lama di sisi klien                                                                                    | Beta   | `compact-2026-01-12`                          |
| [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) (`clear_tool_uses_20250919`, `clear_thinking_20251015`)                                                                       | Penghapusan hasil alat atau thinking lama di sisi klien                                                                   | Beta   | `context-management-2025-06-27`               |
| [Files API](https://platform.claude.com/docs/id/build-with-claude/files) (sumber `file_id`)                                                                                                                            | URL yang kontennya berubah antar permintaan                                                                               | Stabil | Tidak ada                                     |
| [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (`output_config.effort` pada pesan `role: "system"`)                                              | Mengubah effort tingkat atas antar permintaan (melindungi cache prompt, bukan thinking: effort bukan bagian dari prefiks) | Beta   | `mid-conversation-output-config-2026-07-01`   |

Untuk menggabungkan header dalam satu permintaan:

```text wrap
anthropic-beta: thinking-binding-controls-2026-08-01,mid-conversation-system-clear-at-2026-08-21,mid-conversation-tool-changes-2026-07-01
```

Nama beta yang sama berlaku pada Amazon Bedrock dan Google Cloud. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers) untuk cara mengirimnya dengan setiap SDK.

## Daftar periksa

* Jika produk atau SDK resmi Claude (Claude Code, claude.ai, Claude Managed Agents, Claude Agent SDK) mengelola riwayat percakapan Anda, berhenti di sini.
* Body permintaan berurutan identik byte demi byte dalam `system`, `tools`, dan prefiks `messages` yang sama.
* Sesi penuh di bawah `prefix_mismatch_behavior: "drop_block"` tidak mencatat entri `prefix_binding_mismatch` apa pun.
* Giliran asisten dikirim kembali byte demi byte seperti yang dikembalikan, termasuk semua tipe blok.
* `system` dan `tools` tingkat atas tetap untuk sesi tersebut. Perubahan masuk ke pesan `role: "system"` dan blok `tool_addition` / `tool_removal`.
* Pengingat per giliran adalah pesan sistem bercakupan giliran (atau blok teks di akhir) yang ditambahkan baru dan tidak pernah dihapus.
* Konteks dipangkas dengan compaction atau context editing, atau dengan compaction sisi klien yang tidak menyisakan blok thinking di belakang prefiks yang ditulis ulang dan tidak pernah memecah putaran alat.
* File lintas giliran berupa `file_id` atau base64, bukan URL yang dapat berubah.
* `prefix_mismatch_behavior` produksi telah diatur dan respons 400 atau entri yang dibuang dipantau.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemecahan masalah thinking" icon="hammer" href="https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting">
    Diagnosis dan perbaiki kegagalan thinking yang paling umum: error 400 konfigurasi, blok thinking kosong atau hilang, penghentian max\_tokens, dan cache miss.
  </Card>

  <Card title="Pesan sistem dan perubahan alat di tengah percakapan" icon="messages" href="https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages">
    Ubah instruksi sistem atau ketersediaan alat di tengah percakapan tanpa membatalkan validitas prefiks yang di-cache sebelumnya.
  </Card>

  <Card title="Compaction" icon="stack" href="https://platform.claude.com/docs/id/build-with-claude/compaction">
    Compaction konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.
  </Card>

  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Cache prefiks prompt dengan `cache_control` untuk memangkas biaya dan latensi, menggunakan caching otomatis atau breakpoint eksplisit dengan TTL 5 menit atau 1 jam.
  </Card>
</CardGroup>
