---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: b152ef30e0834a28ab4ac72cc13b03aad9623c178f7a2ca745007478f959f562
---

# Pemecahan masalah penggunaan alat

Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.

---

Tabel gejala-ke-perbaikan untuk kesalahan penggunaan alat yang paling umum. Setiap perbaikan merujuk silang ke halaman yang memiliki fitur tersebut.

## Claude memanggil alat yang salah

| Gejala | Penyebab yang mungkin | Perbaikan |
|---|---|---|
| Claude memanggil alat A ketika Anda menginginkan alat B | Ambiguitas deskripsi | Tajamkan deskripsi. Bedakan alat berdasarkan KAPAN menggunakannya, bukan hanya APA yang mereka lakukan. Lihat [Define tools](/docs/id/agents-and-tools/tool-use/define-tools). |
| Claude tidak pernah memanggil alat Anda | Tabrakan nama alat atau skema yang terlalu umum | Periksa nama duplikat di seluruh daftar alat Anda. Tambahkan `input_examples` untuk membuat penggunaan yang dimaksud konkret. |
| Claude memanggil dengan tipe parameter yang salah | Model menebak-nebak pada skema yang ambigu | Tambahkan `strict: true` (jika skema Anda berada dalam subset yang didukung) atau tambahkan `input_examples`. |

## Claude menciptakan parameter alat

| Gejala | Penyebab yang mungkin | Perbaikan |
|---|---|---|
| Parameter yang tidak ada dalam skema Anda | Generasi berlebihan model tanpa mode ketat | Tambahkan `strict: true` jika skema Anda berada dalam [subset yang didukung](/docs/id/agents-and-tools/tool-use/strict-tool-use). |
| Nilai parameter di luar enum Anda | Mode ketat yang hilang atau enum yang terlalu besar | Kurangi enum atau tambahkan `input_examples` yang menunjukkan pilihan yang valid. |

## Panggilan alat paralel tidak berfungsi

| Gejala | Penyebab yang mungkin | Perbaikan |
|---|---|---|
| Claude memanggil alat secara berurutan ketika paralel akan lebih baik | Pemformatan riwayat pesan | Kirim beberapa blok `tool_result` dalam SATU pesan pengguna, bukan satu per giliran. Lihat [Parallel tool use](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `disable_parallel_tool_use` tampaknya diabaikan | Ditetapkan terlalu lambat dalam percakapan | Harus ditetapkan pada permintaan yang mengembalikan `tool_use`. Menetapkannya pada permintaan yang lebih lambat tidak berpengaruh pada panggilan alat sebelumnya. |

## Cache terus tidak valid

| Gejala | Penyebab yang mungkin | Perbaikan |
|---|---|---|
| Setiap permintaan adalah cache miss | `tool_choice` bervariasi antar permintaan | Jaga `tool_choice` tetap stabil atau tempatkan titik putus `cache_control` sebelum titik variasi. Lihat [Tool use with prompt caching](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching). |
| Menambahkan alat di tengah percakapan memecahkan cache | Alat ditambahkan di awal array alat | Gunakan `defer_loading: true` dengan pencarian alat untuk menambahkan alat secara inline alih-alih memodifikasi kepala array. |

## Kesalahan pada waktu permintaan

| Kesalahan | Penyebab | Perbaikan |
|---|---|---|
| `tool_use ids were found without tool_result blocks immediately after` | `tool_result` yang hilang untuk beberapa id `tool_use`, atau `tool_result` bukan blok konten pertama dalam pesan pengguna | Kembalikan satu `tool_result` untuk setiap blok `tool_use` dalam respons asisten. Letakkan blok `tool_result` sebelum teks apa pun. Lihat [Handle tool calls](/docs/id/agents-and-tools/tool-use/handle-tool-calls) dan [Parallel tool use](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `Input schema is not compatible with strict mode: string patterns are not supported` | Menggunakan `pattern` dengan `strict: true` | Hapus pola atau lepaskan `strict: true`. Kata kunci `pattern` belum ada dalam subset JSON Schema yang didukung. |
| `All tools have defer_loading: true` | Tidak ada alat yang terlihat oleh model | Setidaknya satu alat harus dimuat segera. Alat pencarian alat itu sendiri tidak boleh pernah memiliki `defer_loading: true`. |

## Perbedaan pelarian JSON (Opus 4.6+)

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| Perbandingan string pada input alat gagal dengan model yang lebih baru | Pelarian Unicode dan garis miring depan berbeda antar versi model | Parsing dengan `json.loads()` atau `JSON.parse()`. Jangan pernah melakukan pencocokan string mentah pada input yang diserialisasi. |

## Langkah berikutnya

<CardGroup cols={3}>
  <Card title="Define tools" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>
  <Card title="Handle tool calls" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diperlukan.
  </Card>
  <Card title="Tool reference" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat skema Anthropic dan string versi mereka.
  </Card>
</CardGroup>