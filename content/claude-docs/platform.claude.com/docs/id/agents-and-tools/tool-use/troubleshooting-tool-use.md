---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 8b1c8448f5897aaf001933744ba7db855537b7de236ac3f6cbf47621bb946459
---

---
title: Pemecahan masalah penggunaan alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
description: Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.
---

Tabel gejala-ke-perbaikan untuk kesalahan "tool use" (penggunaan alat) yang paling umum. Setiap perbaikan merujuk silang ke halaman yang membahas fitur tersebut.

## Claude memanggil alat yang salah

| Gejala                                                   | Kemungkinan penyebab                               | Perbaikan                                                                                                                                                                                                      |
| -------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude memanggil alat A padahal Anda menginginkan alat B | Deskripsi ambigu                                   | Pertajam deskripsi. Bedakan alat berdasarkan KAPAN menggunakannya, bukan hanya APA yang dilakukannya. Lihat [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools). |
| Claude tidak pernah memanggil alat Anda                  | Tabrakan nama alat atau skema yang terlalu generik | Periksa nama duplikat di seluruh daftar alat Anda. Tambahkan `input_examples` untuk membuat penggunaan yang dimaksud menjadi konkret.                                                                          |
| Claude memanggil dengan tipe parameter yang salah        | Model menebak skema yang ambigu                    | Tambahkan `strict: true` (jika skema Anda berada dalam subset yang didukung) atau tambahkan `input_examples`.                                                                                                  |

## Claude mengarang parameter alat

| Gejala                                    | Kemungkinan penyebab                            | Perbaikan                                                                                                                                                    |
| ----------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Parameter yang tidak ada dalam skema Anda | Model menghasilkan berlebihan tanpa mode strict | Tambahkan `strict: true` jika skema Anda berada dalam [subset yang didukung](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). |
| Nilai parameter di luar enum Anda         | Mode strict tidak ada atau enum terlalu besar   | Perkecil enum atau tambahkan `input_examples` yang menunjukkan pilihan yang valid.                                                                           |

## Pemanggilan alat paralel tidak berfungsi

| Gejala                                                                 | Kemungkinan penyebab                   | Perbaikan                                                                                                                                                                                              |
| ---------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Claude memanggil alat secara berurutan padahal paralel akan lebih baik | Pemformatan riwayat pesan              | Kirim beberapa blok `tool_result` dalam SATU pesan pengguna, bukan satu per giliran. Lihat [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `disable_parallel_tool_use` tampak diabaikan                           | Diatur terlalu lambat dalam percakapan | Harus diatur pada permintaan yang mengembalikan `tool_use`. Mengaturnya pada permintaan berikutnya tidak berpengaruh pada pemanggilan alat sebelumnya.                                                 |

## Cache terus menjadi tidak valid

| Gejala                                              | Kemungkinan penyebab                                                                         | Perbaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setiap permintaan adalah cache miss                 | `tool_choice`, konfigurasi thinking, atau `output_config.effort` bervariasi antar permintaan | Jaga `tool_choice` tetap stabil atau tempatkan breakpoint `cache_control` sebelum titik variasi; pertahankan konfigurasi thinking dan tingkat effort konstan selama masa hidup percakapan yang di-cache. Lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching) dan [Thinking dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching). |
| Menambahkan alat di tengah percakapan merusak cache | Alat ditambahkan di awal array tools                                                         | Gunakan `defer_loading: true` dengan tool search untuk menambahkan alat secara inline alih-alih memodifikasi bagian awal array.                                                                                                                                                                                                                                                                                                                                                   |

## Kesalahan pada saat permintaan

| Kesalahan                                                              | Penyebab                                                                                                                                                                                                                                                                                                                                                                                                        | Perbaikan                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tool_use ids were found without tool_result blocks immediately after` | `tool_result` tidak ada untuk beberapa id `tool_use`, atau `tool_result` bukan blok konten pertama dalam pesan pengguna                                                                                                                                                                                                                                                                                         | Kembalikan satu `tool_result` untuk setiap blok `tool_use` dalam respons asisten. Letakkan blok `tool_result` sebelum teks apa pun. Lihat [Menangani pemanggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls) dan [Penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `was found without a corresponding <name>_tool_result block`           | Giliran asisten sebelumnya memiliki blok `server_tool_use` tanpa blok hasil (paling sering, Claude memanggilnya bersamaan dengan alat klien), dan pesan pengguna berikutnya dari Anda mengakhiri giliran tersebut (misalnya, dengan teks setelah blok `tool_result`) atau permintaan lanjutan tidak lagi mendefinisikan alat server tersebut (pesan kemudian diakhiri dengan `but no <name> tool was provided`) | Kirim pesan pengguna yang hanya berisi blok `tool_result` untuk id `tool_use` klien dan pertahankan array `tools` yang sama. Lihat [Alasan berhenti dan fallback](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#tool-use).                                                                                                                |
| `Unsupported regex feature in pattern field: ...`                      | Sebuah `pattern` dalam `input_schema` alat strict menggunakan fitur regex yang tidak dapat dikompilasi oleh mode strict, seperti backreference, lookaround, word boundary, atau rentang `{n,m}` yang besar                                                                                                                                                                                                      | Sederhanakan pattern tersebut. Pattern berjangkar dengan quantifier dasar, kelas karakter, dan grup didukung; lihat [Keterbatasan JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations).                                                                                                                       |
| `All tools have defer_loading: true`                                   | Tidak ada alat yang terlihat oleh model                                                                                                                                                                                                                                                                                                                                                                         | Setidaknya satu alat harus dimuat segera. Alat tool search itu sendiri tidak boleh memiliki `defer_loading: true`.                                                                                                                                                                                                                                                      |

## Kesalahan: blok thinking tidak dapat dimodifikasi

Jika sebuah permintaan gagal dengan 400 `invalid_request_error` yang pesannya berisi `` `thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified `` saat melanjutkan percakapan setelah pemanggilan alat, aplikasi Anda mengubah blok thinking asisten sebelum mengirimkannya kembali. Kirim kembali seluruh pesan asisten tanpa perubahan, lalu tambahkan `tool_result` Anda.

Lihat [Blok thinking tidak dapat dimodifikasi](https://platform.claude.com/docs/id/api/errors#thinking-blocks-cannot-be-modified) untuk kesalahan lengkap dan langkah-langkah perbaikannya.

## Claude menandai hasil alat sebagai prompt injection

| Gejala                                                                                                              | Kemungkinan penyebab                                            | Perbaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude menolak bertindak berdasarkan hasil alat, atau meminta pengguna mengonfirmasi instruksi yang berasal darinya | Instruksi Anda sendiri dikirimkan di dalam konten `tool_result` | Claude dilatih untuk memperlakukan instruksi di dalam hasil alat sebagai konten pihak ketiga yang berpotensi tidak tepercaya. Pindahkan instruksi Anda keluar dari hasil alat: kirimkan dalam giliran `user` setelah blok `tool_result`, atau, pada model yang didukung, dalam [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Jaga agar hasil alat hanya berisi data. Lihat [Memitigasi jailbreak dan prompt injection](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection). |

## Perbedaan escaping JSON (Opus 4.6+)

| Gejala                                                                 | Penyebab                                                    | Perbaikan                                                                                                                        |
| ---------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Perbandingan string pada input alat gagal dengan model yang lebih baru | Escaping Unicode dan garis miring berbeda antar versi model | Parse dengan `json.loads()` atau `JSON.parse()`. Jangan pernah melakukan pencocokan string mentah pada input yang diserialisasi. |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Mendefinisikan alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>

  <Card title="Menangani pemanggilan alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diwajibkan.
  </Card>

  <Card title="Referensi alat" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat berskema Anthropic dan string versinya.
  </Card>
</CardGroup>
