---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 2e89d34a4550fa936a3b4e9f6f00981f63f6bbaa669324daed0c5b3d48d97a31
---

# Pemecahan masalah penggunaan alat

Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.

---

Tabel gejala-ke-perbaikan untuk kesalahan penggunaan alat yang paling umum. Setiap perbaikan merujuk silang ke halaman yang memiliki fitur tersebut.

## Claude memanggil alat yang salah

| Gejala                                                   | Kemungkinan penyebab                               | Perbaikan                                                                                                                                                                           |
| -------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude memanggil alat A padahal Anda menginginkan alat B | Ambiguitas deskripsi                               | Pertajam deskripsi. Bedakan alat berdasarkan KAPAN menggunakannya, bukan hanya APA yang dilakukannya. Lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools). |
| Claude tidak pernah memanggil alat Anda                  | Tabrakan nama alat atau skema yang terlalu generik | Periksa nama duplikat di seluruh daftar alat Anda. Tambahkan `input_examples` untuk membuat penggunaan yang dimaksud menjadi konkret.                                               |
| Claude memanggil dengan tipe parameter yang salah        | Model menebak pada skema yang ambigu               | Tambahkan `strict: true` (jika skema Anda berada dalam subset yang didukung) atau tambahkan `input_examples`.                                                                       |

## Claude mengarang parameter alat

| Gejala                                    | Kemungkinan penyebab                            | Perbaikan                                                                                                                         |
| ----------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Parameter yang tidak ada dalam skema Anda | Model menghasilkan berlebihan tanpa mode strict | Tambahkan `strict: true` jika skema Anda berada dalam [subset yang didukung](/docs/id/agents-and-tools/tool-use/strict-tool-use). |
| Nilai parameter di luar enum Anda         | Mode strict tidak ada atau enum terlalu besar   | Perkecil enum atau tambahkan `input_examples` yang menunjukkan pilihan yang valid.                                                |

## Panggilan alat paralel tidak berfungsi

| Gejala                                                                 | Kemungkinan penyebab                      | Perbaikan                                                                                                                                                                   |
| ---------------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude memanggil alat secara berurutan padahal paralel akan lebih baik | Pemformatan riwayat pesan                 | Kirim beberapa blok `tool_result` dalam SATU pesan pengguna, bukan satu per giliran. Lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `disable_parallel_tool_use` tampaknya diabaikan                        | Diatur terlalu terlambat dalam percakapan | Harus diatur pada permintaan yang mengembalikan `tool_use`. Mengaturnya pada permintaan berikutnya tidak berpengaruh pada panggilan alat sebelumnya.                        |

## Cache terus tidak valid

| Gejala                                              | Kemungkinan penyebab                      | Perbaikan                                                                                                                                                                                                        |
| --------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setiap permintaan adalah cache miss                 | `tool_choice` bervariasi antar permintaan | Jaga `tool_choice` tetap stabil atau tempatkan breakpoint `cache_control` sebelum titik variasi. Lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching). |
| Menambahkan alat di tengah percakapan merusak cache | Alat ditambahkan di awal array tools      | Gunakan `defer_loading: true` dengan pencarian alat untuk menambahkan alat secara inline alih-alih memodifikasi bagian awal array.                                                                               |

## Kesalahan saat permintaan

| Kesalahan                                                                            | Penyebab                                                                                                                                                                                                                                                                                                                                                                                                   | Perbaikan                                                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tool_use ids were found without tool_result blocks immediately after`               | `tool_result` tidak ada untuk beberapa id `tool_use`, atau `tool_result` bukan blok konten pertama dalam pesan pengguna                                                                                                                                                                                                                                                                                    | Kembalikan satu `tool_result` untuk setiap blok `tool_use` dalam respons asisten. Tempatkan blok `tool_result` sebelum teks apa pun. Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) dan [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `was found without a corresponding <name>_tool_result block`                         | Giliran asisten sebelumnya memiliki blok `server_tool_use` tanpa blok hasil (paling sering, Claude memanggilnya bersamaan dengan alat klien), dan pesan pengguna Anda berikutnya mengakhiri giliran tersebut (misalnya, dengan teks setelah blok `tool_result`) atau permintaan lanjutan tidak lagi mendefinisikan alat server tersebut (pesan kemudian berakhir dengan `but no <name> tool was provided`) | Kirim pesan pengguna yang hanya berisi blok `tool_result` untuk id `tool_use` klien dan pertahankan array `tools` yang sama. Lihat [Alasan berhenti dan fallback](/docs/id/build-with-claude/handling-stop-reasons#tool-use).                                                                                    |
| `Input schema is not compatible with strict mode: string patterns are not supported` | Menggunakan `pattern` dengan `strict: true`                                                                                                                                                                                                                                                                                                                                                                | Hapus pattern atau hilangkan `strict: true`. Kata kunci `pattern` belum termasuk dalam subset JSON Schema yang didukung.                                                                                                                                                                                         |
| `All tools have defer_loading: true`                                                 | Tidak ada alat yang terlihat oleh model                                                                                                                                                                                                                                                                                                                                                                    | Setidaknya satu alat harus dimuat segera. Alat pencarian alat itu sendiri tidak boleh memiliki `defer_loading: true`.                                                                                                                                                                                            |

## Kesalahan: blok thinking tidak dapat dimodifikasi

Jika permintaan gagal dengan 400 `invalid_request_error` yang pesannya berisi `` `thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified `` saat melanjutkan percakapan setelah panggilan alat, aplikasi Anda mengubah blok thinking asisten sebelum mengirimkannya kembali. Kirim kembali seluruh pesan asisten tanpa perubahan, lalu tambahkan `tool_result` Anda.

Lihat [Blok thinking tidak dapat dimodifikasi](/docs/id/api/errors#thinking-blocks-cannot-be-modified) untuk kesalahan lengkap dan langkah perbaikannya.

## Claude menandai hasil alat sebagai prompt injection

| Gejala                                                                                                             | Kemungkinan penyebab                                            | Perbaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude menolak bertindak atas hasil alat, atau meminta pengguna untuk mengonfirmasi instruksi yang berasal darinya | Instruksi Anda sendiri dikirimkan di dalam konten `tool_result` | Claude dilatih untuk memperlakukan instruksi di dalam hasil alat sebagai konten pihak ketiga yang berpotensi tidak tepercaya. Pindahkan instruksi Anda keluar dari hasil alat: kirimkan dalam giliran `user` setelah blok `tool_result`, atau, pada model yang didukung, dalam [pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages). Jaga hasil alat hanya berisi data. Lihat [Mitigasi jailbreak dan prompt injection](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection). |

## Perbedaan escaping JSON (Opus 4.6+)

| Gejala                                                                 | Penyebab                                                    | Perbaikan                                                                                                                        |
| ---------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Perbandingan string pada input alat gagal dengan model yang lebih baru | Escaping Unicode dan garis miring berbeda antar versi model | Parse dengan `json.loads()` atau `JSON.parse()`. Jangan pernah melakukan pencocokan string mentah pada input yang diserialisasi. |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Mendefinisikan alat" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>

  <Card title="Menangani panggilan alat" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diperlukan.
  </Card>

  <Card title="Referensi alat" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat skema-Anthropic dan string versinya.
  </Card>
</CardGroup>
