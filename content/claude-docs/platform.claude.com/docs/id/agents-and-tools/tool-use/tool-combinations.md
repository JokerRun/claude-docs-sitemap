---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-combinations
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 11ebd059970ed28000f88d0112239d8c1cb2b33307fd3c8223c88c9c88aa1b48
---

# Kombinasi alat

Pasangan alat Anthropic yang umum digunakan untuk agen riset, agen pengodean, dan agen yang berjalan lama.

---

Alat yang disediakan Anthropic dirancang untuk bekerja bersama. Pola agen yang umum memasangkan alat-alat yang mencakup tahapan alur kerja yang saling melengkapi: satu alat mengumpulkan atau menemukan, alat lainnya memproses atau bertindak. Kombinasi di bawah ini adalah titik awal, bukan aturan baku. Padukan sesuai kebutuhan tugas Anda.

Setiap cuplikan hanya menampilkan array `tools`. Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk bentuk permintaan lengkapnya.

## Agen riset: web\_search + code\_execution

Pencarian menemukan sumber; eksekusi kode menganalisis dan menyintesis. Claude mencari data, lalu menulis Python untuk memproses, mentabulasi, atau memvisualisasikannya. Pasangan ini cocok untuk pertanyaan yang memerlukan informasi terkini sekaligus komputasi nontrivial atas informasi tersebut, seperti "bandingkan pendapatan kuartal ini di antara lima penyedia cloud teratas."

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "code_execution_20250825", "name": "code_execution" }
  ]
}
```

Alurnya biasanya adalah mencari, lalu mengeksekusi, lalu opsional mencari lagi jika langkah pertama mengungkap adanya kekurangan. Eksekusi kode berjalan di sisi server, jadi tidak ada sandbox sisi klien yang perlu dikelola.

## Agen pengodean: text\_editor + bash

Editor teks membaca dan memodifikasi file; bash menjalankan pengujian dan perintah build. Ini adalah siklus pengembangan perangkat lunak yang kanonis: periksa kode, buat perubahan, jalankan pengujian, ulangi. Kedua alat dieksekusi di sisi klien, sehingga aplikasi Anda mengontrol file dan perintah mana yang dapat diakses.

```json
{
  "tools": [
    { "type": "text_editor_20250728", "name": "str_replace_based_edit_tool" },
    { "type": "bash_20250124", "name": "bash" }
  ]
}
```

Pasangkan ini dengan direktori kerja yang dibatasi dan daftar izin perintah jika agen beroperasi pada kode yang tidak tepercaya. Lihat [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool) untuk kontrak eksekusinya.

## Kutip-lalu-ambil: web\_search + web\_fetch

Pencarian memunculkan URL kandidat; fetch mengambil konten halaman lengkap untuk URL yang relevan. Ini menghindari pengambilan semua konten di awal. Claude menjalankan pencarian, memeriksa cuplikannya, memilih dua atau tiga hasil yang benar-benar terlihat relevan, dan hanya mengambil yang itu saja.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

Pasangan ini berguna ketika jawaban berada dalam konten panjang (halaman dokumentasi, artikel, spesifikasi) yang tidak dapat sepenuhnya ditangkap oleh cuplikan pencarian. Fetch menarik halaman lengkap sehingga Claude dapat mengutip bagian-bagian tertentu.

## Agen yang berjalan lama: memory + rangkaian alat apa pun

Memory mempertahankan state di seluruh percakapan; alat-alat lainnya melakukan pekerjaannya. Tambahkan memory ke agen mana pun yang perlu mengingat sesi sebelumnya, seperti agen dukungan yang mengingat masalah pelanggan sebelumnya atau asisten proyek yang melacak keputusan yang dibuat minggu lalu.

```json
{
  "tools": [{ "type": "memory_20250818", "name": "memory" }]
}
```

Tambahkan alat-alat Anda yang lain bersama `memory` dalam array yang sama.

Memory bersifat ortogonal terhadap rangkaian alat Anda lainnya. Memory tidak mengubah cara alat lain berperilaku; memory memberi Claude tempat untuk mencatat dan kemudian mengambil kembali fakta-fakta yang seharusnya hilang ketika jendela konteks direset. Lihat [Alat memory](/docs/id/agents-and-tools/tool-use/memory-tool) untuk model penyimpanannya.

## Semua dalam satu: computer\_use

Alat computer use mencakup sebagian besar alat lainnya dengan mengoperasikan desktop penuh. Claude melihat tangkapan layar dan mengeluarkan aksi mouse dan keyboard, yang berarti Claude dapat menjalankan aplikasi apa pun yang dapat dijalankan manusia. Gunakan ini ketika tugas memerlukan interaksi GUI arbitrer yang tidak dapat dijangkau oleh alat yang lebih spesifik: perangkat lunak lama tanpa API, langkah verifikasi visual, atau alur kerja yang mencakup beberapa aplikasi desktop.

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

Computer use adalah opsi paling umum dan juga paling lambat, karena setiap aksi memerlukan perjalanan bolak-balik tangkapan layar. Utamakan alat yang lebih spesifik jika sudah mencakup kasus penggunaan Anda, dan gunakan computer use ketika tidak ada yang lain yang cocok. Lihat [Alat computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) untuk penyiapan sandbox.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Katalog lengkap alat yang disediakan Anthropic dengan string tipe dan parameter.
  </Card>

  <Card title="Ikhtisar penggunaan alat" icon="map" href="/docs/id/agents-and-tools/tool-use/overview">
    Cara kerja penggunaan alat dan kapan menggunakan alat Anthropic versus mendefinisikan alat Anda sendiri.
  </Card>
</CardGroup>
