---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-combinations
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: d4e26d71f60d6fe86e43f4f8a3a147e7d5ea553664110c0219ef2b334b0ad05e
---

# Kombinasi alat

Pasangan alat Anthropic yang umum untuk agen riset, agen coding, dan agen yang berjalan lama.

---

Alat-alat yang disediakan Anthropic dirancang untuk bekerja bersama. Pola agen yang umum memasangkan alat-alat yang mencakup tahapan alur kerja yang saling melengkapi: satu alat mengumpulkan atau menemukan, alat lainnya memproses atau bertindak. Kombinasi di bawah ini adalah titik awal, bukan aturan baku. Padukan sesuai kebutuhan tugas Anda.

Setiap cuplikan hanya menampilkan array `tools`. Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk bentuk permintaan lengkapnya.

## Agen riset: web\_search + code\_execution

Pencarian menemukan sumber; eksekusi kode menganalisis dan menyintesis. Claude mencari data, lalu menulis Python untuk memproses, menabulasi, atau memvisualisasikannya. Pasangan ini cocok untuk pertanyaan yang membutuhkan informasi terkini sekaligus komputasi yang tidak sepele atas informasi tersebut, seperti "bandingkan pendapatan kuartal ini di antara lima penyedia cloud teratas."

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "code_execution_20260521", "name": "code_execution" }
  ]
}
```

Alurnya biasanya adalah mencari, lalu mengeksekusi, kemudian secara opsional mencari lagi jika tahap pertama menemukan celah. Eksekusi kode berjalan di sisi server, sehingga tidak ada sandbox sisi klien yang perlu dikelola.

## Agen coding: text\_editor + bash

Editor teks membaca dan memodifikasi file; bash menjalankan pengujian dan perintah build. Ini adalah siklus pengembangan perangkat lunak yang kanonis: periksa kode, lakukan pengeditan, jalankan pengujian, ulangi. Kedua alat dieksekusi di sisi klien, sehingga aplikasi Anda mengontrol file dan perintah mana yang dapat diakses.

```json
{
  "tools": [
    { "type": "text_editor_20250728", "name": "str_replace_based_edit_tool" },
    { "type": "bash_20250124", "name": "bash" }
  ]
}
```

Pasangkan ini dengan direktori kerja yang dibatasi dan daftar perintah yang diizinkan (allowlist) jika agen beroperasi pada kode yang tidak tepercaya. Lihat [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [Alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) untuk kontrak eksekusinya.

## Kutip-lalu-ambil: web\_search + web\_fetch

Pencarian memunculkan URL kandidat; fetch mengambil konten halaman lengkap untuk yang relevan. Ini menghindari pengambilan semuanya di awal. Claude menjalankan pencarian, memeriksa cuplikannya, memilih dua atau tiga hasil yang benar-benar terlihat relevan, dan hanya mengambil yang itu saja.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

Pasangan ini berguna ketika jawabannya berada dalam konten berbentuk panjang (halaman dokumentasi, artikel, spesifikasi) yang tidak dapat ditangkap sepenuhnya oleh cuplikan pencarian. Fetch menarik halaman lengkap sehingga Claude dapat mengutip bagian-bagian tertentu.

## Agen yang berjalan lama: memory + toolset apa pun

Memory mempertahankan state di seluruh percakapan; alat-alat lainnya melakukan pekerjaannya. Tambahkan memory ke agen mana pun yang perlu mengingat sesi sebelumnya, seperti agen dukungan yang mengingat masalah pelanggan sebelumnya atau asisten proyek yang melacak keputusan yang dibuat minggu lalu.

```json
{
  "tools": [{ "type": "memory_20250818", "name": "memory" }]
}
```

Tambahkan alat-alat Anda yang lain bersama `memory` dalam array yang sama.

Memory bersifat ortogonal terhadap toolset Anda yang lain. Memory tidak mengubah cara alat lain berperilaku; memory memberi Claude tempat untuk mencatat dan kemudian mengambil kembali fakta-fakta yang jika tidak akan hilang ketika jendela konteks direset. Lihat [Alat memory](/docs/id/agents-and-tools/tool-use/memory-tool) untuk model penyimpanannya.

## Semua-dalam-satu: computer\_use

Alat computer use mencakup sebagian besar alat lainnya dengan mengoperasikan desktop penuh. Claude melihat tangkapan layar dan mengeluarkan aksi mouse dan keyboard, yang berarti Claude dapat menjalankan aplikasi apa pun yang bisa dijalankan manusia. Gunakan ini ketika tugas memerlukan interaksi GUI sembarang yang tidak dapat dijangkau oleh alat yang lebih spesifik: perangkat lunak lawas tanpa API, langkah verifikasi visual, atau alur kerja yang mencakup beberapa aplikasi desktop.

```json
{
  "tools": [
    {
      "type": "computer_20250124",
      "name": "computer",
      "display_width_px": 1280,
      "display_height_px": 800
    }
  ]
}
```

Computer use adalah opsi yang paling umum dan juga yang paling lambat, karena setiap aksi memerlukan perjalanan bolak-balik tangkapan layar. Utamakan alat yang lebih sempit ketika alat tersebut mencakup kasus penggunaan Anda, dan gunakan computer use ketika tidak ada yang lain yang cocok. Lihat [Alat computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) untuk penyiapan sandbox-nya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Katalog lengkap alat yang disediakan Anthropic beserta string tipe dan parameternya.
  </Card>

  <Card title="Ikhtisar penggunaan alat" icon="map" href="/docs/id/agents-and-tools/tool-use/overview">
    Cara kerja penggunaan alat dan kapan menggunakan alat Anthropic versus mendefinisikan alat Anda sendiri.
  </Card>
</CardGroup>
