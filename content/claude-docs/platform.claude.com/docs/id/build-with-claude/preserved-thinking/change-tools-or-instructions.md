---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 2e41c68bfd0abb895feb852f30bf49ad38d0a8ba4a905227970bb5a61e02cc1f
---

---
title: Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks
url: https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions
description: Kirim instruksi, alat, pengingat, atau ringkasan, lanjutkan percakapan yang tersimpan, atau teruskan permintaan orang lain, sehingga Claude mempertahankan pemikiran sebelumnya.
featureMetadata:
  status: stable
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-opus-5-5
    - claude-sonnet-5-5
    - claude-haiku-5-5
  supportedPlatforms:
    Claude API: stable
    Amazon Bedrock: stable
    Amazon Bedrock (bedrock-runtime): stable
    Claude Platform on AWS: stable
    Claude Models on Google Cloud (Anthropic managed): stable
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

Untuk memperbarui alat, instruksi, atau konteks lain, biarkan semua yang sudah Anda kirim seperti semula, dan tambahkan pembaruan di bagian akhir, tempat pembaruan itu tetap berada. Pada model dengan “preserved thinking” (pemikiran yang dipertahankan), mengubah apa yang sudah Anda kirim dapat membuat pemikiran setelahnya tidak valid, dan [permintaan dapat gagal](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#outcomes).

Model dengan “preserved thinking” (Pemikiran yang dipertahankan) adalah Claude Fable 5.2, Claude Mythos 5.2, Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5.

## Kirim kembali giliran asisten persis apa adanya

Kirim kembali seluruh array `content` dari setiap respons, secara berurutan, termasuk “thinking blocks” (blok pemikiran) yang teksnya kosong. Blok dengan teks kosong itu lengkap, karena `signature`-nya menyimpan penalaran dalam bentuk terenkripsi. Giliran yang berisi [blok `fallback`](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#continuing-the-conversation) memiliki aturannya sendiri.

[Serializer, filter, dan parser stream](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#append-assistant-turns-exactly-as-returned-details) dapat merusak hal ini.

## Ubah instruksi

Jaga `system` tetap sama di setiap permintaan. Letakkan instruksi Anda sendiri dalam pesan `role: "system"` di bagian akhir, dan kirim pesan itu hanya ketika ada yang berubah. Claude memperlakukannya sebagai instruksi dari Anda, sang operator. Biarkan pesan itu selama sisa percakapan, karena menghapus atau mengubah kata-katanya nanti membuat pemikiran setelahnya tidak valid. [Kata-kata pengguna Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#user-words) memiliki aturannya sendiri.

Pengingat yang harus menyertai setiap giliran itu berbeda: [kirim pengingat yang membersihkan dirinya sendiri](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#per-turn-reminders).

Pesan sistem ditempatkan setelah pesan pengguna terbaru, bahkan pesan yang berisi [hasil alat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#new-instructions-details). Pesan sistem dengan blok teks atau blok alat mendapatkan error 400 tepat setelah giliran Claude atau tepat sebelum pesan pengguna. Jadi, ketika giliran Claude adalah yang terakhir, tunggu hingga pesan pengguna berikutnya sudah ada.

Pesan sistem tidak menjamin bahwa Claude mengikuti sebuah instruksi, jadi terapkan batasan seperti mode hanya-baca dalam kode yang menjalankan alat Anda. Beberapa model [tidak menerima pesan sistem](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages).

## Teks yang dapat diedit orang lain

Tanyakan apakah pengguna Anda akan mengharapkan Claude memercayai sebuah file, seperti `AGENTS.md` atau `CLAUDE.md` yang dapat diedit orang lain, atau memori yang tersimpan. Jika tidak, kirim teksnya hanya dalam blok `tool_result`, termasuk versi pertamanya. Untuk alasannya, lihat [Injeksi prompt tidak langsung](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection).

Jangan letakkan teks seperti itu dalam pesan sistem atau dalam teks pesan pengguna, dan dalam percakapan baru, jangan letakkan teks itu di `system`.

Saat Anda memuat file seperti itu atau file itu berubah, minta Claude membacanya dengan alat, dan jangan sertakan teksnya. Atau, setelah pesan pengguna berikutnya, tambahkan sendiri panggilan alat dan hasilnya: pesan `assistant` dengan blok `tool_use`, lalu pesan `user` yang blok `tool_result`-nya berisi teks tersebut. Untuk langkah-langkahnya, lihat [Tulis sendiri panggilan alat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#write-the-tool-call).

File yang diharapkan pengguna Anda untuk diikuti Claude dapat diletakkan dalam pesan pengguna. File instruksi yang hanya Anda kendalikan dapat diletakkan dalam pesan sistem: muat sekali, lalu tambahkan setiap versi yang diperbarui.

## Perbarui tanggal, file, atau konteks lain

Susun `system` dan pesan pertama sekali saja, lalu kirimkan tanpa perubahan di setiap permintaan.

Letakkan nilai yang diperbarui dalam blok teksnya sendiri di pesan pengguna yang akan Anda kirim, [setelah hasil alat apa pun](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#user-words):

```json
{
  "role": "user",
  "content": [
    { "type": "text", "text": "Environment update: the current branch is now release-2." },
    { "type": "text", "text": "Run the tests again." }
  ]
}
```

Nyatakan nilai itu hanya ketika berubah, dan biarkan tetap di sana.

Simpan konteks apa pun yang ditambahkan kode Anda ke sebuah pesan bersama pesan tersebut. Jika tidak, permintaan berikutnya mengirim sesuatu yang berbeda sebelum pemikiran yang sama.

## Tambah, hapus, atau nonaktifkan alat

Jaga `tools` tetap sama di setiap permintaan. Menambahkan, mengubah, atau menghapus alat di sana, selain [alat yang ditangguhkan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#deferred-tools), membuat pemikiran yang sudah ada dalam percakapan tidak valid, karena `tools` berada sebelum semuanya. Satu kalimat yang diubah kata-katanya dalam sebuah deskripsi sudah cukup untuk itu.

Untuk menambah atau menghapus alat, tambahkan pesan sistem dengan blok `tool_addition` atau `tool_removal` dan [beta header untuk kasus Anda](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#tool-changes-details). Lakukan hal yang sama saat server MCP atau plugin terhubung.

Untuk menonaktifkan alat pada satu permintaan, atur `tool_choice: {"type": "none"}`, dan biarkan `tools` seperti semula.

## Pangkas atau ringkas giliran lama

Untuk mempertahankan giliran terbaru beserta pemikirannya, biarkan API menulis ringkasan dengan [“compaction” (pemadatan) sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand#request-a-summary), sesuai [syarat untuk thinking yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid). Mulai `messages` dengan blok compaction yang dikembalikannya, dan hapus pesan-pesan yang diringkasnya.

Jika kode Anda sendiri yang menulis ringkasan, atau memotong giliran lama tanpa ringkasan, [hapus pemikiran giliran yang dipertahankan atau kirim `"drop_block"`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#server-side-trimming-details). Setiap pemotongan baru membuat pemikiran giliran yang dipertahankan tidak valid lagi, jadi jarang-jaranglah memotong, dalam langkah yang besar. Untuk membersihkan hasil alat lama sebagai gantinya, [gunakan “context editing” (pengeditan konteks)](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#clear-old-content).

## Simpan, lanjutkan, atau fork percakapan

Simpan apa yang Anda kirim dan apa yang Anda terima, lalu kirim persis itu. Percakapan yang dilanjutkan adalah permintaan berikutnya yang biasa: `system`, `tools`, dan `messages` sebelumnya harus memiliki nilai yang dimilikinya dulu. Untuk fork, letakkan instruksi cabang tersebut dalam pesan pengguna baru pertamanya, atau dalam pesan sistem setelahnya. Pemikiran tidak dapat dipindahkan ke percakapan dengan riwayat yang berbeda: mulailah percakapan itu dari sebuah ringkasan sebagai gantinya.

Rilis yang mengubah prompt sistem atau alat Anda merupakan perubahan dalam percakapan yang sudah berjalan. Perbaikan yang membuat kode Anda “append-only” (hanya menambahkan) juga bisa merupakan perubahan seperti itu. Terus kirimkan ke setiap percakapan yang sedang berjalan `system` dan `tools` dari permintaan sukses terakhirnya, karena pemikiran terbarunya dihasilkan setelah versi tersebut. Kembali ke versi sebelumnya akan membuat pemikiran itu tidak valid.

Gunakan `system` dan `tools` yang diperbarui dalam percakapan baru. Jika rilis menghapus alat atau mengubah instruksi demi keamanan, terapkan juga ke percakapan yang sedang berjalan. Tambahkan [blok `tool_removal`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#tool-changes) atau [pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#new-instructions).

## Hapus rahasia, data pribadi, atau teks yang diinjeksi

Keamanan dan privasi lebih diutamakan daripada menjaga pemikiran tetap valid. Jika sebuah pesan berisi rahasia atau data pribadi yang harus Anda hapus, hapus teks tersebut. Hapus juga dari setiap pesan dan ringkasan yang mengulanginya.

Untuk hasil alat yang berisi instruksi yang diinjeksi, ganti kontennya dengan catatan singkat seperti “Removed.” Pertahankan blok `tool_result` itu sendiri, karena `tool_use`-nya membutuhkannya. Jika [blok compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) berisi teks tersebut, hapus blok itu, dan mulai dari ringkasan Anda sendiri.

Lalu hapus setiap blok `thinking` dan `redacted_thinking` setelah tempat pertama teks itu muncul. Jika teks itu ada di `system` atau `tools`, berarti semuanya. Setiap blok dapat mengulangi teks tersebut, dan Anda tidak dapat membaca atau mengedit isinya. Mengirim `"drop_block"` tidak cukup di sini, karena itu membiarkan blok-blok tersebut tetap ada dalam riwayat yang Anda simpan. Percakapan berlanjut tanpa penalaran itu.

Setelah hasil yang diinjeksi, giliran-giliran berikutnya mungkin sudah bertindak berdasarkan hasil itu. Periksa panggilan alat yang dibuat sejak saat itu, dan batalkan apa yang perlu Anda batalkan.

## Detail teknis

### Cara kode mengubah giliran asisten

* Serializer tidak menyertakan tipe blok yang tidak dikenalinya, atau mengubah urutan, menggabungkan, atau memisahkan blok. Hal itu mengubah apa yang ada sebelum setiap blok berikutnya.
* Kode melewati blok pemikiran yang tampak kosong. Jika kode melewati semuanya, Claude kehilangan penalaran tersebut. Jika kode hanya melewati sebagian, celahnya membuat pemikiran setelahnya tidak valid.
* Parser stream buatan Anda sendiri tidak menyertakan blok pemikiran yang tidak mendapatkan teks. Helper stream SDK mempertahankannya.

### Tidak menyertakan pemikiran

Claude kehilangan penalaran yang tidak Anda sertakan. Yang tidak Anda sertakan boleh blok yang paling lama, yang paling baru, atau semuanya, tetapi jangan ada yang di antaranya. Setiap blok mencatat blok yang mendahuluinya saat blok itu dihasilkan, sehingga celah membuat blok-blok setelahnya tidak valid. Blok pemikiran yang tidak dipisahkan oleh blok lain dalam satu giliran diperiksa bersama-sama, jadi yang tidak disertakan harus semuanya atau tidak sama sekali. Setelah sebuah blok tidak disertakan, tetap jangan sertakan blok itu.

Selama panggilan alat masih terbuka, [kirim kembali pemikiran giliran tersebut](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks), sehingga Claude menyelesaikan putaran itu dengan penalarannya.

### Instruksi Anda dalam loop alat

Pesan-pesan disusun dalam urutan ini:

```json
[
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "", "signature": "..." },
      {
        "type": "tool_use",
        "id": "toolu_01",
        "name": "run_tests",
        "input": { "path": "tests/" }
      }
    ]
  },
  {
    "role": "user",
    "content": [
      { "type": "tool_result", "tool_use_id": "toolu_01", "content": "2 failed, 48 passed" }
    ]
  },
  {
    "role": "system",
    "content": "Plan mode is off. You can edit files."
  }
]
```

### Tulis sendiri panggilan alat

Deklarasikan alat yang membaca file pada permintaan pertama, atau [tambahkan nanti dalam pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#tool-changes), dan minta kode Anda menjawab panggilan Claude ke alat itu. Setelah pesan pengguna berikutnya, tambahkan pesan `assistant` dengan blok `tool_use` untuk alat tersebut. Langsung setelahnya, tambahkan pesan `user` yang blok `tool_result`-nya memiliki `tool_use_id` yang cocok dan berisi teks file tersebut. Claude menjawab setelah itu:

```json
[
  { "role": "user", "content": "Run the tests again." },
  {
    "role": "assistant",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_app_agents_md_1",
        "name": "read_file",
        "input": { "path": "AGENTS.md" }
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "tool_result",
        "tool_use_id": "toolu_app_agents_md_1",
        "content": "The file's text"
      }
    ]
  }
]
```

Biarkan keduanya tetap di tempatnya, dan tambahkan pasangan baru, dengan `id` baru, untuk setiap versi baru.

### Kata-kata pengguna Anda, dan nilai yang diperbarui, dalam loop alat

Jika Anda meneruskan apa yang diketik pengguna Anda saat Claude sedang bekerja, tambahkan sebelum Anda mengirim pesan pengguna yang membawa blok `tool_result`. Jadikan itu blok teks setelah `tool_result` terakhir.

Nilai yang berasal dari Anda dapat diletakkan dalam pesan sistem sebagai gantinya. Setelah hasil alat, Claude Sonnet 5.5 dan Claude Haiku 5.5 dapat mengabaikan kata-kata pengguna dalam pesan sistem sebagai prompt injection. Claude Sonnet 5.5 dapat melakukan hal yang sama terhadap instruksi dan pengingat Anda sendiri jika itu muncul setelah setiap hasil alat.

Pesan pengguna dengan hasil alat harus hanya berisi blok `tool_result` ketika giliran tersebut juga memanggil [“server tool” (alat server)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls) yang belum memiliki hasil, atau menggunakan programmatic tool calling. Dalam hal itu, tambahkan teks ke pesan pengguna berikutnya.

### Model yang tidak menerima pesan sistem

Di Claude API, setiap model dengan pemikiran yang dipertahankan menerima pesan sistem. Untuk model yang tidak menerimanya, lihat [Ketika model tidak menerima pesan sistem](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#unchosen-switches-details).

### Kirim pengingat untuk satu giliran

Kirim pengingat sebagai [pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages): atur `clear_at: "next_user_message"`, dan kirim beta header `mid-conversation-system-clear-at-2026-08-21`. Pesan itu diletakkan setelah pesan pengguna yang membawa blok `tool_result`:

```json
{
  "role": "system",
  "clear_at": "next_user_message",
  "content": "Run the linter before you report that a task is done."
}
```

Pada pesan pengguna berikutnya, bahkan yang hanya berisi blok `tool_result`, API membersihkannya, sehingga Claude berhenti membacanya. Pada Claude Sonnet 5.5, [jangan kirim pengingat setelah setiap hasil alat](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#user-words). Simpan setiap pengingat dalam `messages` Anda, sudah dibersihkan atau belum, kecuali pengingat itu [berisi sesuatu yang harus Anda hapus](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#remove-sensitive-content). Menghapus atau mengubah kata-kata salah satunya membuat pemikiran setelahnya tidak valid.

Tanpa header tersebut, kirim pesan sistem biasa dan biarkan tetap di tempatnya. Pesan itu tidak pernah dibersihkan, sehingga pengingat menumpuk. Pada model yang tidak menerima pesan sistem, gunakan blok teks dalam pesan pengguna.

### Blok dan beta header mana yang dibutuhkan perubahan alat

Untuk platform yang menerima setiap header, lihat [Pesan sistem dan perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages).

* **Jika Anda mengetahui semua alat sejak awal:** Deklarasikan semuanya pada permintaan pertama, dengan `defer_loading: true` pada alat yang Anda tawarkan nanti. Lalu sebutkan nama alat tersebut dalam blok `tool_addition` atau `tool_removal` dari pesan sistem. Beta header: `inline-tools-2026-09-15` atau `mid-conversation-tool-changes-2026-07-01`.
* **Jika Anda baru mengetahui sebuah alat nanti, atau memiliki alat yang skemanya berubah:** Definisikan alat tersebut dalam blok `tool_addition` dari pesan sistem. Beta header: `inline-tools-2026-09-15`.
* **Jika Anda baru mengetahui sebuah alat nanti, pada platform tanpa header `inline-tools-2026-09-15`:** Tambahkan alat tersebut ke akhir `tools` dengan `defer_loading: true`, yang tidak terhitung sebagai perubahan, lalu tawarkan berdasarkan namanya. Beta header: `mid-conversation-tool-changes-2026-07-01`.
* **Jika Anda menghubungkan server MCP melalui MCP connector belakangan, di Claude API:** Definisikan `mcp_toolset`-nya dalam blok `tool_addition`. Beta header: `inline-tools-2026-09-15` dan `mcp-client-2026-09-15`.

Jika daftar alat server MCP dapat berubah, lihat [Sematkan daftar alat server MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#pin-mcp-tool-list).

Pesan sistem ini menawarkan alat yang telah dideklarasikan berdasarkan namanya dan mendefinisikan alat lain, yang membutuhkan `inline-tools-2026-09-15`:

```json
{
  "role": "system",
  "content": [
    {
      "type": "tool_addition",
      "tool": { "type": "tool_reference", "name": "search_tickets" }
    },
    {
      "type": "tool_addition",
      "tool": {
        "type": "tool_definition",
        "definition": {
          "name": "get_weather",
          "description": "Get the current weather in a city.",
          "input_schema": {
            "type": "object",
            "properties": { "city": { "type": "string" } },
            "required": ["city"]
          }
        }
      }
    }
  ]
}
```

### Alat dengan `defer_loading`, dan error 400 yang menyebutkannya

Alat dengan `defer_loading: true` tetap berada di luar konteks Claude dan pemeriksaan prefiks hingga sebuah pesan atau hasil pencarian alat merujuk ke alat itu. Hingga saat itu, menambahkan, memperbarui, atau menghapusnya tidak terhitung sebagai perubahan. Setelahnya, hal itu terhitung sebagai perubahan. Mengaktifkan atau menonaktifkan `defer_loading` juga terhitung sebagai mengubah `tools`.

Deklarasikan setidaknya satu alat yang tidak ditangguhkan, atau permintaan dapat mendapatkan error 400 yang menyebutkan `defer_loading`.

### Persingkat atau bersihkan hasil dan gambar lama

Persingkat atau perkecil resolusi hasil alat atau gambar sebelum Anda mengirimkannya pertama kali. Jika kode Anda membersihkan, mempersingkat, atau meng-encode ulang sesuatu yang sudah dikirimnya, pemikiran setelahnya menjadi tidak valid. Untuk membersihkan hasil alat lama nanti, termasuk gambar apa pun di dalamnya, gunakan pengeditan konteks. Kirim `context_management` dengan edit bertipe `clear_tool_uses_20250919`, dan beta header `context-management-2025-06-27`. Untuk permintaan lengkap dan opsinya, lihat [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing#tool-result-clearing).

### File yang Anda kirim melalui URL

Untuk file melalui URL, API membandingkan byte yang diambilnya. Jadi ketika URL bertanda tangan kedaluwarsa, URL baru untuk file yang sama tidak menjadi masalah. Jika konten di balik URL dapat berubah, kirim `file_id` atau base64 sejak permintaan pertama.

### Jika kode Anda sendiri meringkas atau memotong giliran lama

Setelah ringkasan atau pemotongan Anda sendiri, pemikiran giliran yang dipertahankan gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check), karena pesan-pesan yang diikutinya sudah tidak ada. Hapus pemikiran itu, atau [kirim `"drop_block"`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls). Claude tetap membaca giliran tersebut tanpa pemikiran itu.

### Library, proxy, dan gateway

Jika permintaan orang lain melewati kode Anda, penulisan ulang yang Anda lakukan mengubah riwayat mereka, dan mereka mungkin tidak dapat melihat atau memperbaiki perubahan tersebut. Jangan sembunyikan error 400. Jika Anda melakukan pemulihan untuk pemanggil, beri tahu mereka, karena riwayat mereka masih berisi perubahan tersebut.

* Teruskan nilai `anthropic-beta` dan `thinking.block_binding` sebagaimana dikirim. Jika gateway Anda hanya mengizinkan field yang dikenal, tambahkan `thinking.block_binding` dan nilai header `thinking-binding-controls-2026-08-01`, atau pengguna Anda tidak dapat memilih `"drop_block"`.
* Jangan menghapus beta header lalu meneruskan setting tersebut. Permintaan seperti itu mendapatkan error 400.
* Kembalikan blok pemikiran yang teksnya kosong, dan array `input_transformations`, kepada pemanggil.
* Biarkan pesan `role: "system"` di tempatnya. Memindahkannya ke `system` membuat pemikiran yang sudah ada dalam percakapan tidak valid.
* Uji dengan [`prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#preserved-thinking-controls) diatur ke `"error"`, yang memberikan error pada setiap model dengan pemikiran yang dipertahankan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemikiran yang dipertahankan" icon="book" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking">
    Apa itu pemikiran yang dipertahankan, blok pemikiran terikat pada apa, serta beralih model atau akun.
  </Card>

  <Card title="Perbaiki blok pemikiran yang terikat ke percakapan lain" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation">
    Pulihkan percakapan yang gagal, dan lihat biaya tidak menyertakan pemikiran.
  </Card>

  <Card title="Pesan sistem dan perubahan alat di tengah percakapan" icon="message" href="https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages">
    Di mana pesan sistem dan perubahan alat ditempatkan, serta model dan platform mana yang menerimanya.
  </Card>
</CardGroup>
