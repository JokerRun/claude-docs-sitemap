---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: 4d8a7f2670f0ad94238d27a9cf9e32ce57671a9546bbc019ffd0e02cd6db6ef6
---

---
title: Pemecahan masalah penggunaan alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
description: Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.
---

Temukan gejala atau kesalahan yang Anda lihat, lalu terapkan perbaikan yang tercantum untuknya.

## Claude memanggil alat yang salah

| Gejala                                                   | Kemungkinan penyebab                               | Perbaikan                                                                                                                                                                                                      |
| -------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude memanggil alat A padahal Anda menginginkan alat B | Deskripsi ambigu                                   | Pertajam deskripsi. Bedakan alat berdasarkan KAPAN menggunakannya, bukan hanya APA yang dilakukannya. Lihat [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools). |
| Claude tidak pernah memanggil alat Anda                  | Tabrakan nama alat atau skema yang terlalu generik | Periksa nama duplikat di seluruh daftar alat Anda. Tambahkan `input_examples` agar penggunaan yang dimaksud menjadi konkret.                                                                                   |
| Claude memanggil dengan tipe parameter yang salah        | Skema ambigu                                       | Tambahkan `strict: true` (jika skema Anda berada dalam subset yang didukung) atau tambahkan `input_examples`.                                                                                                  |

## Claude mengarang parameter alat

| Gejala                                    | Kemungkinan penyebab                            | Perbaikan                                                                                                                                                    |
| ----------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Parameter yang tidak ada dalam skema Anda | Model menghasilkan berlebihan tanpa mode strict | Tambahkan `strict: true` jika skema Anda berada dalam [subset yang didukung](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). |
| Nilai parameter di luar enum Anda         | Mode strict tidak ada atau enum terlalu besar   | Perkecil enum atau tambahkan `input_examples` yang menunjukkan pilihan yang valid.                                                                           |

## Pemanggilan alat paralel tidak berfungsi

| Gejala                                                                 | Kemungkinan penyebab                   | Perbaikan                                                                                                                                                                                              |
| ---------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Claude memanggil alat secara berurutan padahal paralel akan lebih baik | Pemformatan riwayat pesan              | Kirim beberapa blok `tool_result` dalam SATU pesan pengguna, bukan satu per giliran. Lihat [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `disable_parallel_tool_use` tampaknya diabaikan                        | Diatur terlalu lambat dalam percakapan | Atur pada permintaan yang mengembalikan `tool_use`. Mengaturnya pada permintaan selanjutnya tidak berpengaruh pada pemanggilan alat sebelumnya.                                                        |

## Cache terus menjadi tidak valid

| Gejala                                              | Kemungkinan penyebab                                                                         | Perbaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setiap permintaan adalah cache miss                 | `tool_choice`, konfigurasi thinking, atau `output_config.effort` bervariasi antar permintaan | Jaga `tool_choice` tetap stabil atau tempatkan breakpoint `cache_control` sebelum titik variasi; pertahankan konfigurasi thinking dan tingkat effort konstan selama masa hidup percakapan yang di-cache. Lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching) dan [Thinking dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching). |
| Menambahkan alat di tengah percakapan merusak cache | Alat ditambahkan di awal array tools                                                         | Deklarasikan alat dengan `defer_loading: true` sejak permintaan pertama dan biarkan pencarian alat memuatnya secara inline, alih-alih menambahkannya ke array di kemudian waktu.                                                                                                                                                                                                                                                                                                  |

## Kesalahan pada saat permintaan

Kolom Kesalahan menampilkan sebagian dari setiap pesan, dan `...` mewakili teks yang bervariasi.

| Kesalahan                                                              | Penyebab                                                                                                                                                               | Perbaikan                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tool_use ids were found without tool_result blocks immediately after` | `tool_result` tidak ada untuk beberapa ID `tool_use`, atau `tool_result` bukan blok konten pertama dalam pesan pengguna                                                | Kembalikan satu `tool_result` untuk setiap blok `tool_use` dalam respons asisten. Letakkan blok `tool_result` sebelum teks apa pun. Lihat [Menangani pemanggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls) dan [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `was found without a corresponding ... block`                          | Permintaan lanjutan mencegah alat server yang sedang menunggu untuk dijalankan                                                                                         | Lihat [Pemanggilan alat server tidak memiliki blok hasil](https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use#a-server-tool-call-has-no-result-block).                                                                                                                                                                               |
| `Unsupported regex feature in pattern field: ...`                      | Sebuah `pattern` alat strict menggunakan fitur regex yang tidak dapat dikompilasi oleh mode strict, seperti backreference, batas kata, atau rentang `{n,m}` yang besar | Sederhanakan pola tersebut. Lihat [Batasan JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations).                                                                                                                                                                                                              |
| `Invalid regex in pattern field: ...`                                  | Sebuah `pattern` alat strict memiliki lookahead, lookbehind, atau kesalahan sintaksis                                                                                  | Hapus lookahead atau lookbehind apa pun dan perbaiki kesalahan sintaksis apa pun. Lihat [Batasan JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations).                                                                                                                                                        |
| `All tools have defer_loading: true`                                   | Tidak ada alat yang terlihat oleh model                                                                                                                                | Setidaknya satu alat harus dimuat segera. Alat pencarian alat itu sendiri tidak boleh memiliki `defer_loading: true`.                                                                                                                                                                                                                                                   |

### Pemanggilan alat server tidak memiliki blok hasil

Sebuah [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) masih menunggu untuk dijalankan ketika blok `server_tool_use` atau `mcp_tool_use`-nya tidak memiliki blok hasil. Kesalahan `was found without a corresponding ... block` berarti permintaan lanjutan mencegah alat yang sedang menunggu tersebut dijalankan. Pesan kesalahan dan `stop_reason` sebelumnya menunjukkan alasannya. Gunakan kasus pertama yang cocok:

* **Pesan diakhiri dengan ``but no `<name>` tool was provided`` atau `is not available after the last message`:** Di sini, `<name>` adalah nama alat, seperti `web_search`. Permintaan tidak lagi mendefinisikan alat tersebut. Kirim array `tools` yang sama seperti sebelumnya, dan `mcp_servers` yang sama untuk alat MCP.
* **`stop_reason` sebelumnya adalah `tool_use`:** Pesan pengguna Anda memiliki konten setelah blok `tool_result`. Kirim hanya blok `tool_result`, satu untuk setiap blok `tool_use` klien.
* **`stop_reason` sebelumnya adalah `pause_turn`:** Anda menambahkan pesan pengguna. Hapus pesan tersebut agar permintaan diakhiri dengan respons yang dijeda sebagai pesan `assistant`.

Untuk langkah lengkapnya, lihat [Ketika alat server masih menunggu](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#when-a-server-tool-is-still-waiting) dan [alasan berhenti `pause_turn`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#pause-turn).

## Kesalahan: blok thinking tidak dapat dimodifikasi

Jika sebuah permintaan gagal dengan 400 `invalid_request_error` yang pesannya berisi `` `thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified `` saat melanjutkan percakapan setelah pemanggilan alat, aplikasi Anda mengubah blok thinking asisten sebelum mengirimkannya kembali. Kirim seluruh pesan asisten kembali tanpa perubahan, lalu tambahkan `tool_result` Anda.

Lihat [Blok thinking tidak dapat dimodifikasi](https://platform.claude.com/docs/id/api/errors#thinking-blocks-cannot-be-modified) untuk kesalahan lengkap dan langkah perbaikannya.

## Claude menandai hasil alat sebagai injeksi prompt

| Gejala                                                                                                              | Kemungkinan penyebab                                            | Perbaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude menolak bertindak berdasarkan hasil alat, atau meminta pengguna mengonfirmasi instruksi yang berasal darinya | Instruksi Anda sendiri dikirimkan di dalam konten `tool_result` | Claude dilatih untuk memperlakukan instruksi di dalam hasil alat sebagai konten pihak ketiga yang berpotensi tidak tepercaya. Pindahkan instruksi Anda keluar dari hasil alat: kirimkan dalam giliran `user` setelah blok `tool_result`, atau, pada model yang didukung, dalam [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Jaga agar hasil alat hanya berisi data. Lihat [Memitigasi jailbreak dan prompt injection](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection). |

## Perbedaan escaping JSON antar versi model

| Gejala                                                                 | Penyebab                                                    | Perbaikan                                                                                                                        |
| ---------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Perbandingan string pada input alat gagal dengan model yang lebih baru | Escaping Unicode dan garis miring berbeda antar versi model | Parse dengan `json.loads()` atau `JSON.parse()`. Jangan pernah melakukan pencocokan string mentah pada input yang diserialisasi. |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Mendefinisikan alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>

  <Card title="Menangani pemanggilan alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diperlukan.
  </Card>

  <Card title="Referensi alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat yang disediakan Anthropic dan string versinya.
  </Card>
</CardGroup>
