---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: f6bbd2668c756e5391776231d8a7e5aa14f57edd4143942804c8b1516f6133b3
---

# Pemecahan masalah penggunaan alat

Perbaiki kesalahan penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.

---

Tabel gejala-ke-perbaikan untuk kesalahan penggunaan alat yang paling umum. Setiap perbaikan merujuk silang ke halaman yang memiliki fitur tersebut.

## Claude memanggil alat yang salah \{#claude-calls-the-wrong-tool}

| Gejala | Kemungkinan penyebab | Perbaikan |
|---|---|---|
| Claude memanggil alat A padahal Anda menginginkan alat B | Ambiguitas deskripsi | Pertajam deskripsi. Bedakan alat berdasarkan KAPAN menggunakannya, bukan hanya APA yang dilakukannya. Lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools). |
| Claude tidak pernah memanggil alat Anda | Tabrakan nama alat atau skema yang terlalu generik | Periksa nama duplikat di seluruh daftar alat Anda. Tambahkan `input_examples` untuk membuat penggunaan yang dimaksud menjadi konkret. |
| Claude memanggil dengan tipe parameter yang salah | Model menebak-nebak skema yang ambigu | Tambahkan `strict: true` (jika skema Anda berada dalam subset yang didukung) atau tambahkan `input_examples`. |

## Claude mengarang parameter alat \{#claude-invents-tool-parameters}

| Gejala | Kemungkinan penyebab | Perbaikan |
|---|---|---|
| Parameter yang tidak ada dalam skema Anda | Model menghasilkan berlebihan tanpa mode strict | Tambahkan `strict: true` jika skema Anda berada dalam [subset yang didukung](/docs/id/agents-and-tools/tool-use/strict-tool-use). |
| Nilai parameter di luar enum Anda | Mode strict tidak ada atau enum terlalu besar | Perkecil enum atau tambahkan `input_examples` yang menunjukkan pilihan yang valid. |

## Pemanggilan alat paralel tidak berfungsi \{#parallel-tool-calls-dont-work}

| Gejala | Kemungkinan penyebab | Perbaikan |
|---|---|---|
| Claude memanggil alat secara berurutan padahal paralel akan lebih baik | Pemformatan riwayat pesan | Kirim beberapa blok `tool_result` dalam SATU pesan user, bukan satu per giliran. Lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `disable_parallel_tool_use` tampaknya diabaikan | Diatur terlalu terlambat dalam percakapan | Harus diatur pada permintaan yang mengembalikan `tool_use`. Mengaturnya pada permintaan berikutnya tidak berpengaruh pada pemanggilan alat sebelumnya. |

## Cache terus terinvalidasi \{#cache-keeps-invalidating}

| Gejala | Kemungkinan penyebab | Perbaikan |
|---|---|---|
| Setiap permintaan adalah cache miss | `tool_choice` bervariasi antar permintaan | Jaga agar `tool_choice` tetap stabil atau tempatkan breakpoint `cache_control` sebelum titik variasi. Lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching). |
| Menambahkan alat di tengah percakapan merusak cache | Alat ditambahkan di awal array tools | Gunakan `defer_loading: true` dengan tool search untuk menambahkan alat secara inline alih-alih memodifikasi bagian awal array. |

## Kesalahan pada waktu permintaan \{#errors-at-request-time}

| Kesalahan | Penyebab | Perbaikan |
|---|---|---|
| `tool_use ids were found without tool_result blocks immediately after` | `tool_result` tidak ada untuk beberapa id `tool_use`, atau `tool_result` bukan blok konten pertama dalam pesan user | Kembalikan satu `tool_result` untuk setiap blok `tool_use` dalam respons assistant. Letakkan blok `tool_result` sebelum teks apa pun. Lihat [Menangani pemanggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) dan [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use). |
| `Input schema is not compatible with strict mode: string patterns are not supported` | Menggunakan `pattern` dengan `strict: true` | Hapus pattern atau hilangkan `strict: true`. Kata kunci `pattern` belum termasuk dalam subset JSON Schema yang didukung. |
| `All tools have defer_loading: true` | Tidak ada alat yang terlihat oleh model | Setidaknya satu alat harus dimuat segera. Alat tool search itu sendiri tidak boleh memiliki `defer_loading: true`. |

## Claude menandai hasil alat sebagai prompt injection \{#claude-flags-tool-results-as-prompt-injection}

| Gejala | Kemungkinan penyebab | Perbaikan |
|---|---|---|
| Claude menolak untuk bertindak berdasarkan hasil alat, atau meminta pengguna untuk mengonfirmasi instruksi yang berasal darinya | Instruksi Anda sendiri dikirimkan di dalam konten `tool_result` | Claude dilatih untuk memperlakukan instruksi di dalam hasil alat sebagai konten pihak ketiga yang berpotensi tidak tepercaya. Pindahkan instruksi Anda keluar dari hasil alat: kirim instruksi tersebut dalam giliran `user` setelah blok `tool_result`, atau (pada Claude Opus 4.8 dan yang lebih baru) dalam [pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages). Batasi hasil alat hanya pada datanya saja. Lihat [Mitigasi jailbreak dan prompt injection](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection). |

## Perbedaan escaping JSON (Opus 4.6+) \{#json-escaping-differences-opus-4-6}

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| Perbandingan string pada input alat gagal dengan model yang lebih baru | Escaping Unicode dan forward-slash berbeda antar versi model | Parse dengan `json.loads()` atau `JSON.parse()`. Jangan pernah melakukan pencocokan string mentah pada input yang diserialisasi. |

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={3}>
  <Card title="Mendefinisikan alat" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>
  <Card title="Menangani pemanggilan alat" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Jalankan alat dan kembalikan hasil dalam format pesan yang diperlukan.
  </Card>
  <Card title="Referensi alat" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori lengkap alat skema Anthropic dan string versinya.
  </Card>
</CardGroup>