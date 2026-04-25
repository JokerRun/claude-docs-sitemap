---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-combinations
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 1ea5d967a123ecba3e9757506d910397eb3268ca4fdfeedbebbc58351c3faaaa
---

# Kombinasi alat

Pasangan alat Anthropic yang umum untuk agen penelitian, agen pengkodean, dan agen yang berjalan lama.

---

Alat yang disediakan Anthropic dirancang untuk bekerja bersama. Pola agen umum memasangkan alat yang mencakup tahap-tahap komplementer dari alur kerja: satu alat mengumpulkan atau menemukan, alat lain memproses atau bertindak. Kombinasi di bawah ini adalah titik awal, bukan preskripsi. Campurkan mereka agar sesuai dengan tugas Anda.

Setiap cuplikan hanya menunjukkan larik `tools`. Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk bentuk permintaan lengkap.

## Agen penelitian: web_search + code_execution

Pencarian menemukan sumber; eksekusi kode menganalisis dan mensintesis. Claude mencari data, kemudian menulis Python untuk memproses, membuat tabel, atau memvisualisasikannya. Pasangan ini cocok untuk pertanyaan yang memerlukan informasi terkini dan komputasi nontrivial atas informasi tersebut, seperti "bandingkan pendapatan kuartal ini di seluruh lima penyedia cloud teratas."

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "code_execution_20250825", "name": "code_execution" }
  ]
}
```

Alurnya biasanya pencarian, kemudian eksekusi, kemudian secara opsional pencarian lagi jika lintasan pertama mengungkapkan celah. Eksekusi kode berjalan di sisi server, jadi tidak ada sandbox sisi klien yang perlu dikelola.

## Agen pengkodean: text_editor + bash

Editor teks membaca dan memodifikasi file; bash menjalankan tes dan perintah build. Ini adalah loop pengembangan perangkat lunak kanonik: periksa kode, buat edit, jalankan tes, ulangi. Kedua alat dieksekusi klien, jadi aplikasi Anda mengontrol file dan perintah mana yang dapat diakses.

```json
{
  "tools": [
    { "type": "text_editor_20250728", "name": "str_replace_based_edit_tool" },
    { "type": "bash_20250124", "name": "bash" }
  ]
}
```

Pasangkan ini dengan direktori kerja terbatas dan daftar perintah yang diizinkan jika agen beroperasi pada kode yang tidak terpercaya. Lihat [Alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [Alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool) untuk kontrak eksekusi.

## Kutip-kemudian-ambil: web_search + web_fetch

Pencarian mengungkapkan URL kandidat; ambil mengambil konten halaman lengkap untuk yang relevan. Ini menghindari pengambilan semuanya di muka. Claude menjalankan pencarian, memeriksa cuplikan, memilih dua atau tiga hasil yang benar-benar terlihat relevan, dan hanya mengambil yang tersebut.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

Pasangan ini berguna ketika jawaban hidup dalam konten bentuk panjang (halaman dokumentasi, artikel, spesifikasi) yang cuplikan pencarian tidak dapat sepenuhnya menangkap. Ambil menarik halaman lengkap sehingga Claude dapat mengutip bagian tertentu.

## Agen yang berjalan lama: memory + any toolset

Memori bertahan keadaan di seluruh percakapan; alat lainnya melakukan pekerjaan. Tambahkan memori ke agen apa pun yang perlu mengingat sesi sebelumnya, seperti agen dukungan yang mengingat masalah pelanggan sebelumnya atau asisten proyek yang melacak keputusan yang dibuat minggu lalu.

```json
{
  "tools": [{ "type": "memory_20250818", "name": "memory" }]
}
```

Tambahkan alat lain Anda bersama `memory` dalam larik yang sama.

Memori ortogonal terhadap sisa perangkat alat Anda. Ini tidak mengubah cara alat lain berperilaku; ini memberi Claude tempat untuk menuliskan dan kemudian mengambil fakta yang sebaliknya akan hilang ketika jendela konteks direset. Lihat [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) untuk model penyimpanan.

## Semua-dalam-satu: computer_use

Alat penggunaan komputer menggabungkan sebagian besar alat lainnya dengan mengoperasikan desktop lengkap. Claude melihat tangkapan layar dan mengeluarkan tindakan mouse dan keyboard, yang berarti dapat mendorong aplikasi apa pun yang dapat didorong manusia. Gunakan ini ketika tugas memerlukan interaksi GUI arbitrer yang tidak dapat dijangkau alat yang lebih spesifik: perangkat lunak warisan tanpa API, langkah verifikasi visual, atau alur kerja yang mencakup beberapa aplikasi desktop.

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

Penggunaan komputer adalah opsi yang paling umum dan juga yang paling lambat, karena setiap tindakan memerlukan putaran tangkapan layar. Lebih suka alat yang lebih sempit ketika mereka mencakup kasus penggunaan Anda, dan gunakan penggunaan komputer ketika tidak ada yang cocok. Lihat [Alat penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) untuk penyiapan sandbox.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Referensi alat"
    icon="book"
    href="/docs/id/agents-and-tools/tool-use/tool-reference"
  >
    Katalog lengkap alat yang disediakan Anthropic dengan string tipe dan parameter.
  </Card>
  <Card
    title="Ikhtisar penggunaan alat"
    icon="map"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Cara penggunaan alat bekerja dan kapan menggunakan alat Anthropic versus menentukan milik Anda sendiri.
  </Card>
</CardGroup>