---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 35383a2dfe3da3220256a0936a056c85f74c9c08c0f7cddf9768ffb25ea5af71
---

---
title: Cara kerja penggunaan alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works
description: Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat alih-alih prosa.
---

Halaman ini menjelaskan konsep di balik "tool use" (penggunaan alat): di mana alat berjalan, bagaimana loop agentik bekerja, dan kapan penggunaan alat merupakan pendekatan yang tepat. Untuk panduan praktis, mulailah dengan tutorial [Membangun agen yang menggunakan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent) atau panduan [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools).

## Kontrak penggunaan alat

Penggunaan alat adalah kontrak antara aplikasi Anda dan model. Anda menentukan operasi apa yang tersedia dan bentuk input serta outputnya; Claude menentukan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda (atau server Anthropic) menjalankan operasi tersebut, dan hasilnya mengalir kembali ke dalam percakapan.

Kontrak ini membuat model berperilaku kurang seperti generator teks dan lebih seperti fungsi yang Anda panggil. Engineer dengan pengalaman API klasik dapat mengintegrasikan penggunaan alat dengan cara yang sama seperti antarmuka bertipe lainnya: definisikan skema, tangani callback, kembalikan hasil. Perbedaannya adalah pemanggil di sisi lain adalah model bahasa yang memilih fungsi mana yang akan dipanggil berdasarkan percakapan.

## Di mana alat berjalan

Sumbu utama yang membedakan alat adalah di mana kode dieksekusi. Setiap alat termasuk dalam salah satu dari tiga kelompok, dan kelompok tersebut menentukan apa yang menjadi tanggung jawab aplikasi Anda.

### Alat yang didefinisikan pengguna (dieksekusi klien)

Anda menulis skema, Anda mengeksekusi kode, Anda mengembalikan hasil. Ini adalah kasus yang paling umum: sebagian besar lalu lintas penggunaan alat adalah [alat yang didefinisikan pengguna](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools) yang memanggil logika khusus aplikasi.

Ketika Claude memanggil salah satu alat Anda, respons API berisi blok `tool_use` dengan nama alat dan objek JSON berisi argumen. Aplikasi Anda mengekstrak argumen tersebut, menjalankan operasi (kueri database, panggilan HTTP, penulisan file, apa pun yang dilakukan alat tersebut), dan mengirim outputnya kembali dalam blok `tool_result` pada permintaan berikutnya. Claude tidak pernah melihat implementasi Anda; Claude hanya melihat skema yang Anda berikan dan hasil yang Anda kembalikan.

### Alat berskema Anthropic (dieksekusi klien)

Untuk beberapa operasi umum (mengelola memori scratchpad, menjalankan perintah shell, mengedit file, mengendalikan desktop atau browser), Anthropic menerbitkan skema alat dan aplikasi Anda menangani eksekusinya. Alat dalam kategori ini adalah [`memory`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool), [`bash`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool), [`text_editor`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool), [`computer`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), dan [`browser`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool).

Model eksekusinya identik dengan alat yang didefinisikan pengguna: respons berisi blok `tool_use`, kode Anda menjalankan operasi, dan Anda mengirim kembali `tool_result`. Alasan menggunakan alat berskema Anthropic alih-alih mendefinisikan padanan Anda sendiri adalah karena skema ini sudah dilatihkan ke dalam model. Claude telah dioptimalkan pada ribuan trajektori sukses yang menggunakan tanda tangan alat yang persis sama ini, sehingga Claude memanggilnya dengan lebih andal dan pulih dari kesalahan dengan lebih baik dibandingkan dengan alat kustom yang melakukan hal yang sama. Skema tersebut adalah antarmuka yang sudah diharapkan oleh model.

### Alat yang dieksekusi server

Untuk [`web_search`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool), [`web_fetch`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), [`code_execution`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), dan [`tool_search`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), Anthropic yang menjalankan kodenya. Anda mengaktifkan alat dalam permintaan Anda dan server menangani semua hal lainnya. Anda tidak pernah menyusun blok `tool_result` untuk alat-alat ini. Ketika sebuah giliran hanya memanggil [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools), loop sisi server mengeksekusi operasi dan mengumpankan outputnya kembali ke model sebelum respons sampai kepada Anda, kecuali jika loop berhenti sebelum selesai, paling sering karena loop tersebut dijeda.

Respons yang Anda terima berisi blok `server_tool_use` yang menunjukkan apa yang dijalankan dan apa yang dikembalikan. Dalam kasus umum, eksekusi sudah selesai pada saat Anda melihatnya, dan tugas aplikasi Anda adalah mengaktifkan alat dan membaca jawaban akhir alih-alih berpartisipasi dalam loop eksekusi; pengecualian utamanya adalah loop yang dijeda ([`pause_turn`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works#the-server-side-loop)) dan giliran yang juga memanggil alat klien.

## Loop agentik (alat klien)

Alat yang dieksekusi klien (baik yang didefinisikan pengguna maupun berskema Anthropic) mengharuskan aplikasi Anda menjalankan sebuah loop. Model tidak dapat menjalankan kode Anda, sehingga setiap panggilan alat adalah satu perjalanan bolak-balik: model meminta, Anda mengeksekusi, Anda melaporkan kembali, model melanjutkan.

Bentuk kanoniknya adalah loop `while` yang bergantung pada `stop_reason`:

1. Kirim permintaan dengan array `tools` Anda dan pesan pengguna.
2. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`.
3. Eksekusi setiap alat. Format outputnya sebagai blok `tool_result`.
4. Kirim permintaan baru yang berisi pesan asli, respons asisten, dan pesan pengguna dengan blok `tool_result`.
5. Ulangi dari langkah 2 selama `stop_reason` adalah `"tool_use"`.

Dalam praktiknya ini dibaca sebagai: selama `stop_reason == "tool_use"`, eksekusi alat dan lanjutkan percakapan. Loop berakhir pada stop reason lainnya (`"end_turn"`, `"max_tokens"`, `"stop_sequence"`, atau `"refusal"`), yang berarti Claude telah menghasilkan jawaban akhir atau berhenti karena alasan lain yang harus ditangani aplikasi Anda.

Untuk mekanisme membangun permintaan, menangani panggilan alat paralel, dan memformat hasil, lihat [Menangani panggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Loop sisi server

Alat yang dieksekusi server menjalankan loop-nya sendiri di dalam infrastruktur Anthropic. Satu permintaan dari aplikasi Anda mungkin memicu beberapa pencarian web atau eksekusi kode sebelum respons kembali. Model mencari, membaca hasil, menentukan apakah perlu mencari lagi, dan beriterasi hingga mendapatkan apa yang dibutuhkan, semuanya tanpa partisipasi aplikasi Anda.

Loop internal ini memiliki batas iterasi. Jika model masih beriterasi ketika mencapai batas tersebut, respons kembali dengan `stop_reason: "pause_turn"` alih-alih `"end_turn"`. Giliran yang dijeda berarti pekerjaan belum selesai; kirim ulang percakapan (termasuk respons yang dijeda) agar model melanjutkan dari tempat ia berhenti. Lihat [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) untuk pola kelanjutannya.

Loop ini juga menyerahkan kendali kembali kepada Anda sebelum alat server berjalan jika Claude memanggil alat server tersebut dan alat klien dalam kelompok panggilan alat paralel yang sama. Respons kemudian kembali dengan `stop_reason: "tool_use"` dan blok `server_tool_use` yang belum memiliki blok hasil; API menjalankannya setelah Anda mengembalikan hasil alat klien. Lihat [Stop reason dan fallback](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#tool-use) untuk kontrak persisnya.

## Kapan menggunakan alat (dan kapan tidak)

Penggunaan alat cocok ketika tugas memerlukan sesuatu yang tidak dapat dilakukan model hanya dari teks:

* **Tindakan dengan efek samping.** Mengirim email, menulis file, memperbarui catatan. Model dapat mendeskripsikan tindakan ini, tetapi hanya alat yang dapat melakukannya.
* **Data terbaru atau eksternal.** Harga saat ini, cuaca hari ini, isi database. Apa pun di luar data pelatihan atau yang spesifik untuk sistem Anda memerlukan alat untuk mengambilnya.
* **Output terstruktur dengan bentuk yang terjamin.** Ketika Anda membutuhkan objek JSON dengan field tertentu alih-alih prosa yang kebetulan berisi informasi tersebut, skema alat menegakkan bentuknya.
* **Memanggil sistem yang sudah ada.** Database, API internal, filesystem. Penggunaan alat adalah jembatan antara permintaan bahasa alami dan sistem yang memenuhinya.

Tanda jelas bahwa Anda seharusnya menggunakan alat: jika Anda menulis regex untuk mengekstrak keputusan dari output model, keputusan itu seharusnya berupa panggilan alat. Mengurai teks bebas untuk memulihkan maksud terstruktur adalah tanda bahwa struktur tersebut seharusnya berada dalam skema.

Penggunaan alat tidak cocok ketika:

* Model dapat menjawab hanya dari pelatihan. Peringkasan, penerjemahan, dan pertanyaan pengetahuan umum tidak memerlukan perjalanan bolak-balik alat.
* Interaksinya adalah tanya jawab sekali jalan tanpa efek samping. Jika tidak ada yang perlu dieksekusi, tidak ada yang perlu dilakukan alat.
* Latensi pemanggilan alat akan mendominasi respons yang sepele. Setiap panggilan alat setidaknya satu perjalanan bolak-balik tambahan; untuk tugas ringan, overhead-nya dapat melebihi pekerjaannya.

## Memilih di antara pendekatan

| Pendekatan                             | Kapan menggunakannya                                                              | Apa yang diharapkan                                                                          | Pelajari lebih lanjut                                                                             |
| -------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Alat klien yang didefinisikan pengguna | Logika bisnis kustom, API internal, data proprietary                              | Anda menangani eksekusi dan loop agentik                                                     | [Mendefinisikan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools) |
| Alat klien berskema Anthropic          | Operasi pengembangan standar (bash, pengeditan file, kendali desktop dan browser) | Anda menangani eksekusi; Claude memanggil alat dengan andal karena skemanya sudah dilatihkan | [Referensi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference)    |
| Alat yang dieksekusi server            | Pencarian web, sandbox kode, web fetch                                            | Anthropic menangani eksekusi; Anda membaca hasilnya alih-alih menghasilkannya                | [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools)         |

## Langkah selanjutnya

<CardGroup>
  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Membangun agen yang menggunakan alat">
    Bangun agen langkah demi langkah dari satu panggilan alat hingga produksi.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools" title="Mendefinisikan alat">
    Spesifikasi skema, deskripsi, dan `tool_choice`.
  </Card>

  <Card href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori alat yang disediakan Anthropic.
  </Card>
</CardGroup>
