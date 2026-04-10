---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 781d0b5d3828e6607c9f500e37faa5191c3ab44b7a11bac017724262135441b9
---

# Cara kerja penggunaan alat

Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat dibandingkan prosa.

---

Halaman ini menjelaskan konsep di balik penggunaan alat: di mana alat berjalan, bagaimana loop agentik bekerja, dan kapan penggunaan alat adalah pendekatan yang tepat. Untuk panduan langsung, mulailah dengan [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent) atau [panduan implementasi](/docs/id/agents-and-tools/tool-use/define-tools).

## Kontrak penggunaan alat

Penggunaan alat adalah kontrak antara aplikasi Anda dan model. Anda menentukan operasi apa yang tersedia dan bentuk input serta outputnya; Claude memutuskan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda (atau server Anthropic) menjalankan operasi, dan hasilnya mengalir kembali ke dalam percakapan.

Kontrak ini membuat model berperilaku kurang seperti generator teks dan lebih seperti fungsi yang Anda panggil. Engineer dengan pengalaman API klasik dapat mengintegrasikan penggunaan alat dengan cara yang sama seperti antarmuka bertipe lainnya: definisikan skema, tangani callback, kembalikan hasil. Perbedaannya adalah pemanggil di sisi lain adalah model bahasa yang memilih fungsi mana yang akan dipanggil berdasarkan percakapan.

## Di mana alat berjalan

Sumbu utama yang membedakan alat adalah di mana kode dieksekusi. Setiap alat masuk ke salah satu dari tiga kategori, dan kategori tersebut menentukan apa yang menjadi tanggung jawab aplikasi Anda.

### Alat yang ditentukan pengguna (dieksekusi oleh klien)

Anda menulis skema, Anda mengeksekusi kode, Anda mengembalikan hasilnya. Ini adalah acara utama: sebagian besar lalu lintas penggunaan alat adalah alat yang ditentukan pengguna yang memanggil logika khusus aplikasi.

Ketika Claude memutuskan untuk menggunakan salah satu alat Anda, respons API berisi blok `tool_use` dengan nama alat dan objek JSON berisi argumen. Aplikasi Anda mengekstrak argumen tersebut, menjalankan operasi (kueri database, panggilan HTTP, penulisan file, apa pun yang dilakukan alat), dan mengirim output kembali dalam blok `tool_result` pada permintaan berikutnya. Claude tidak pernah melihat implementasi Anda; ia hanya melihat skema yang Anda berikan dan hasil yang Anda kembalikan.

### Alat skema Anthropic (dieksekusi oleh klien)

Untuk sejumlah kecil operasi umum (menjalankan perintah shell, mengedit file, mengontrol browser, mengelola memori scratchpad), Anthropic menerbitkan skema alat dan aplikasi Anda menangani eksekusi. Alat dalam kategori ini adalah `bash`, `text_editor`, `computer`, dan `memory`.

Model eksekusi identik dengan alat yang ditentukan pengguna: respons berisi blok `tool_use`, kode Anda menjalankan operasi, dan Anda mengirim kembali `tool_result`. Alasan menggunakan alat skema Anthropic daripada mendefinisikan ekuivalen Anda sendiri adalah bahwa skema ini sudah terlatih. Claude telah dioptimalkan pada ribuan trajektori sukses yang menggunakan tanda tangan alat yang tepat ini, sehingga ia memanggilnya dengan lebih andal dan pulih dari kesalahan dengan lebih baik dibandingkan alat kustom yang melakukan hal yang sama. Skema adalah antarmuka yang sudah diharapkan oleh model.

### Alat yang dieksekusi server

Untuk `web_search`, `web_fetch`, `code_execution`, dan `tool_search`, Anthropic menjalankan kode. Anda mengaktifkan alat dalam permintaan Anda dan server menangani segalanya. Anda tidak pernah membuat blok `tool_result` untuk alat-alat ini karena loop sisi server mengeksekusi operasi dan mengumpankan output kembali ke model sebelum respons mencapai Anda.

Respons yang Anda terima berisi blok `server_tool_use` yang menunjukkan apa yang berjalan dan apa yang dikembalikan, tetapi pada saat Anda melihatnya, eksekusi sudah selesai. Tugas aplikasi Anda adalah mengaktifkan alat dan membaca jawaban akhir, bukan berpartisipasi dalam loop eksekusi.

## Loop agentik (alat klien)

Alat yang dieksekusi klien (baik yang ditentukan pengguna maupun skema Anthropic) mengharuskan aplikasi Anda untuk menjalankan loop. Model tidak dapat menjalankan kode Anda, sehingga setiap pemanggilan alat adalah perjalanan bolak-balik: model meminta, Anda mengeksekusi, Anda melaporkan kembali, model melanjutkan.

Bentuk kanonik adalah loop `while` yang dikunci pada `stop_reason`:

1. Kirim permintaan dengan array `tools` Anda dan pesan pengguna.
2. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`.
3. Eksekusi setiap alat. Format output sebagai blok `tool_result`.
4. Kirim permintaan baru yang berisi pesan asli, respons asisten, dan pesan pengguna dengan blok `tool_result`.
5. Ulangi dari langkah 2 selama `stop_reason` adalah `"tool_use"`.

Dalam praktiknya ini terbaca sebagai: selama `stop_reason == "tool_use"`, eksekusi alat dan lanjutkan percakapan. Loop keluar pada alasan berhenti lainnya (`"end_turn"`, `"max_tokens"`, `"stop_sequence"`, atau `"refusal"`), yang berarti Claude telah menghasilkan jawaban akhir atau berhenti karena alasan lain yang harus ditangani aplikasi Anda.

Untuk mekanisme membangun permintaan, menangani pemanggilan alat paralel, dan memformat hasil, lihat [Tangani pemanggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Loop sisi server

Alat yang dieksekusi server menjalankan loop mereka sendiri di dalam infrastruktur Anthropic. Satu permintaan dari aplikasi Anda mungkin memicu beberapa pencarian web atau eksekusi kode sebelum respons kembali. Model mencari, membaca hasil, memutuskan untuk mencari lagi, dan beriterasi hingga mendapatkan apa yang dibutuhkan, semuanya tanpa aplikasi Anda berpartisipasi.

Loop internal ini memiliki batas iterasi. Jika model masih beriterasi ketika mencapai batas, respons kembali dengan `stop_reason: "pause_turn"` alih-alih `"end_turn"`. Giliran yang dijeda berarti pekerjaan belum selesai; kirim ulang percakapan (termasuk respons yang dijeda) untuk membiarkan model melanjutkan dari tempat terakhir. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) untuk pola kelanjutan.

## Kapan menggunakan alat (dan kapan tidak)

Penggunaan alat cocok ketika tugas memerlukan sesuatu yang tidak dapat dilakukan model dari teks saja:

- **Tindakan dengan efek samping.** Mengirim email, menulis file, memperbarui catatan. Model dapat mendeskripsikan tindakan-tindakan ini, tetapi hanya alat yang dapat melakukannya.
- **Data segar atau eksternal.** Harga terkini, cuaca hari ini, isi database. Apa pun di luar data pelatihan atau yang spesifik untuk sistem Anda memerlukan alat untuk mengambilnya.
- **Output terstruktur dengan bentuk yang terjamin.** Ketika Anda membutuhkan objek JSON dengan bidang tertentu daripada prosa yang kebetulan berisi informasi, skema alat memaksakan bentuknya.
- **Memanggil sistem yang ada.** Database, API internal, sistem file. Penggunaan alat adalah jembatan antara permintaan bahasa alami dan sistem yang memenuhinya.

Tanda bahwa Anda harus menggunakan alat: jika Anda menulis regex untuk mengekstrak keputusan dari output model, keputusan itu seharusnya menjadi pemanggilan alat. Mengurai teks bebas untuk memulihkan maksud terstruktur adalah tanda bahwa struktur tersebut seharusnya ada dalam skema.

Penggunaan alat tidak cocok ketika:

- Model dapat menjawab dari pelatihan saja. Ringkasan, terjemahan, dan pertanyaan pengetahuan umum tidak memerlukan perjalanan bolak-balik alat.
- Interaksi adalah tanya jawab satu kali tanpa efek samping. Jika tidak ada yang perlu dieksekusi, tidak ada yang perlu dilakukan alat.
- Latensi pemanggilan alat akan mendominasi respons yang sepele. Setiap pemanggilan alat setidaknya satu perjalanan bolak-balik ekstra; untuk tugas ringan, overhead dapat melebihi pekerjaan itu sendiri.

## Memilih antara pendekatan

| Pendekatan | Kapan menggunakannya | Apa yang diharapkan | Pelajari lebih lanjut |
| --- | --- | --- | --- |
| Alat klien yang ditentukan pengguna | Logika bisnis kustom, API internal, data proprietary | Anda menangani eksekusi dan loop agentik | [Definisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) |
| Alat klien skema Anthropic | Operasi dev standar (bash, pengeditan file, kontrol browser) | Anda menangani eksekusi; Claude memanggil alat dengan andal karena skema sudah terlatih | [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference) |
| Alat yang dieksekusi server | Pencarian web, sandbox kode, pengambilan web | Anthropic menangani eksekusi; Anda mendapatkan hasil secara langsung | [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) |

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Bangun agen yang menggunakan alat">
    Bangun agen langkah demi langkah dari satu pemanggilan alat hingga produksi.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/define-tools" title="Definisikan alat">
    Spesifikasi skema, deskripsi, dan tool_choice.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori alat yang disediakan Anthropic.
  </Card>
</CardGroup>