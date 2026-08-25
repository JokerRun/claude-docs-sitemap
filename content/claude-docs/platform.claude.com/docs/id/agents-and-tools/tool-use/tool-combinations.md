---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-combinations
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 8a1fe245cb904c930c77f64c8bfe29eccddc3ac4c615085bde787ff3a4dbf749
---

---
title: Kombinasi alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-combinations
description: Pasangan alat Anthropic yang umum untuk agen riset, agen coding, dan agen yang berjalan lama.
---

Alat yang disediakan Anthropic dirancang untuk bekerja bersama. Pola agen yang umum memasangkan alat-alat yang mencakup tahap-tahap alur kerja yang saling melengkapi: satu alat mengumpulkan atau menemukan, alat lainnya memproses atau bertindak. Kombinasi di bawah ini adalah titik awal, bukan ketentuan baku. Padukan sesuai dengan tugas Anda.

Setiap cuplikan hanya menampilkan array `tools`. Lihat [Menangani panggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk bentuk permintaan yang lengkap.

## Agen riset: web\_search + code\_execution

Pencarian menemukan sumber; eksekusi kode menganalisis dan menyintesis. Claude mencari data, lalu menulis Python untuk memproses, mentabulasi, atau memvisualisasikannya. Pasangan ini cocok untuk pertanyaan yang memerlukan informasi terkini sekaligus komputasi yang tidak sepele atas informasi tersebut, seperti "bandingkan pendapatan kuartal ini di antara lima penyedia cloud teratas."

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "code_execution_20260521", "name": "code_execution" }
  ]
}
```

Alurnya biasanya adalah cari, lalu eksekusi, lalu secara opsional cari lagi jika putaran pertama menyingkap adanya celah. Eksekusi kode berjalan di sisi server, sehingga tidak ada sandbox sisi klien yang perlu dikelola.

## Agen coding: text\_editor + bash

Editor teks membaca dan memodifikasi file; bash menjalankan pengujian dan perintah build. Ini adalah siklus pengembangan perangkat lunak yang kanonis: periksa kode, buat perubahan, jalankan pengujian, ulangi. Kedua alat dieksekusi di sisi klien, sehingga aplikasi Anda mengontrol file dan perintah mana yang dapat diakses.

```json
{
  "tools": [
    { "type": "text_editor_20250728", "name": "str_replace_based_edit_tool" },
    { "type": "bash_20250124", "name": "bash" }
  ]
}
```

Pasangkan ini dengan direktori kerja yang dibatasi dan daftar izin (allowlist) perintah jika agen beroperasi pada kode yang tidak tepercaya. Lihat [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [Alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool) untuk kontrak eksekusinya.

## Kutip-lalu-ambil: web\_search + web\_fetch

Pencarian memunculkan URL kandidat; fetch mengambil konten halaman lengkap untuk URL yang relevan. Ini menghindari pengambilan semuanya di awal. Claude menjalankan pencarian, memeriksa cuplikannya, memilih dua atau tiga hasil yang benar-benar tampak relevan, dan hanya mengambil hasil tersebut.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

Pasangan ini berguna ketika jawabannya berada dalam konten berbentuk panjang (halaman dokumentasi, artikel, spesifikasi) yang tidak dapat ditangkap sepenuhnya oleh cuplikan pencarian. Fetch menarik halaman lengkap sehingga Claude dapat mengutip bagian-bagian tertentu.

## Agen yang berjalan lama: memory + alat lain apa pun

Memory mempertahankan status di seluruh percakapan; alat-alat lainnya melakukan pekerjaannya. Tambahkan memory ke agen apa pun yang perlu mengingat sesi sebelumnya, seperti agen dukungan yang mengingat masalah pelanggan sebelumnya atau asisten proyek yang melacak keputusan yang dibuat minggu lalu.

```json
{
  "tools": [{ "type": "memory_20250818", "name": "memory" }]
}
```

Tambahkan alat-alat Anda yang lain di samping `memory` dalam array yang sama.

Memory bersifat ortogonal terhadap alat-alat Anda yang lain. Memory tidak mengubah cara alat-alat tersebut berperilaku; memory memberi Claude tempat untuk menuliskan dan kemudian mengambil kembali fakta-fakta yang jika tidak akan hilang ketika "context window" (jendela konteks) direset. Lihat [Alat memory](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool) untuk model penyimpanannya.

## Serba ada: computer\_use

Alat computer use mencakup sebagian besar alat lainnya dengan mengoperasikan desktop penuh. Claude melihat tangkapan layar dan mengeluarkan tindakan mouse dan keyboard, yang berarti Claude dapat mengendalikan aplikasi apa pun yang dapat dikendalikan manusia. Gunakan ini ketika tugas memerlukan interaksi GUI arbitrer yang tidak dapat dijangkau oleh alat yang lebih spesifik: perangkat lunak lawas tanpa API, langkah verifikasi visual, atau alur kerja yang mencakup beberapa aplikasi desktop.

```json
{
  "tools": [{ "type": "computer_toolset_20260801" }]
}
```

Entri toolset tidak memerlukan `name` atau dimensi tampilan: koordinat dinyatakan dalam ruang piksel dari tangkapan layar yang Anda kembalikan, dan Anda dapat menonaktifkan tindakan individual melalui field `configs` pada entri tersebut.

Computer use adalah opsi yang paling umum dan juga yang paling lambat, karena Claude biasanya memerlukan tangkapan layar baru setelah setiap kumpulan tindakan. Utamakan alat yang lebih sempit ketika alat tersebut mencakup kasus penggunaan Anda, dan gunakan computer use ketika tidak ada yang lain yang cocok. Jika tugas tetap berada di dalam browser web, gunakan pola agen browser di bagian berikutnya. Lihat [Alat computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) untuk penyiapan sandbox.

## Agen browser: browser\_use

Ketika seluruh tugas terjadi di dalam halaman web (mengisi formulir, membaca konten halaman, bekerja di beberapa tab), alat browser use lebih cocok daripada computer use. Aplikasi Anda mengendalikan browser yang dikontrolnya dan mengembalikan tangkapan layar atau status halaman; Claude memanggil alat anggota yang sadar-halaman seperti `read_page`, `find`, `form_input`, dan `get_page_text` di samping klik dan pengetikan, sehingga Claude dapat bertindak berdasarkan referensi elemen selain koordinat piksel.

```json
{
  "tools": [{ "type": "browser_toolset_20260801" }]
}
```

Seperti toolset computer use, entri ini tidak memerlukan `name`, dan Anda menonaktifkan alat anggota individual melalui field `configs`-nya. Lihat [Alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk kontrak eksekusinya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Katalog lengkap alat yang disediakan Anthropic dengan string tipe dan parameter.
  </Card>

  <Card title="Ikhtisar penggunaan alat" icon="map" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Cara kerja penggunaan alat dan kapan menggunakan alat Anthropic dibandingkan mendefinisikan alat Anda sendiri.
  </Card>
</CardGroup>
