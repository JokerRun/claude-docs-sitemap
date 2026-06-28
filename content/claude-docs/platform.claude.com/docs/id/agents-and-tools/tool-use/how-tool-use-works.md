---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 2b9732388333206fd3dc8e94182e78c4de5ede460f79bfe944a55ff2a1e10923
---

# Cara kerja penggunaan alat

Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat alih-alih prosa.

---

Halaman ini menjelaskan konsep di balik "tool use" (penggunaan alat): di mana alat dijalankan, bagaimana loop agentik bekerja, dan kapan penggunaan alat merupakan pendekatan yang tepat. Untuk panduan praktis, mulailah dengan [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent) atau [panduan implementasi](/docs/id/agents-and-tools/tool-use/define-tools).

## Kontrak penggunaan alat

Penggunaan alat adalah kontrak antara aplikasi Anda dan model. Anda menentukan operasi apa yang tersedia dan bentuk input serta output-nya; Claude memutuskan kapan dan bagaimana memanggilnya. Model tidak pernah mengeksekusi apa pun sendiri. Model mengeluarkan permintaan terstruktur, kode Anda (atau server Anthropic) menjalankan operasi tersebut, dan hasilnya mengalir kembali ke dalam percakapan.

Kontrak ini membuat model berperilaku tidak seperti generator teks, melainkan lebih seperti fungsi yang Anda panggil. Engineer dengan pengalaman API klasik dapat mengintegrasikan penggunaan alat dengan cara yang sama seperti antarmuka bertipe lainnya: definisikan skema, tangani callback, kembalikan hasil. Perbedaannya adalah pemanggil di sisi lain adalah model bahasa yang memilih fungsi mana yang akan dipanggil berdasarkan percakapan.

## Di mana alat dijalankan

Sumbu utama yang membedakan alat adalah di mana kode dieksekusi. Setiap alat termasuk dalam salah satu dari tiga kategori, dan kategori tersebut menentukan apa yang menjadi tanggung jawab aplikasi Anda.

### Alat yang didefinisikan pengguna (dieksekusi di klien)

Anda menulis skemanya, Anda mengeksekusi kodenya, Anda mengembalikan hasilnya. Ini adalah bagian utamanya: sebagian besar lalu lintas penggunaan alat adalah alat yang didefinisikan pengguna yang memanggil logika spesifik aplikasi.

Ketika Claude memutuskan untuk menggunakan salah satu alat Anda, respons API berisi blok `tool_use` dengan nama alat dan objek JSON berisi argumen. Aplikasi Anda mengekstrak argumen tersebut, menjalankan operasi (kueri database, panggilan HTTP, penulisan file, apa pun yang dilakukan alat tersebut), dan mengirimkan output kembali dalam blok `tool_result` pada permintaan berikutnya. Claude tidak pernah melihat implementasi Anda; ia hanya melihat skema yang Anda berikan dan hasil yang Anda kembalikan.

### Alat skema Anthropic (dieksekusi di klien)

Untuk beberapa operasi umum (menjalankan perintah shell, mengedit file, mengontrol browser, mengelola memori scratchpad), Anthropic menerbitkan skema alat dan aplikasi Anda menangani eksekusinya. Alat dalam kategori ini adalah `bash`, `text_editor`, `computer`, dan `memory`.

Model eksekusinya identik dengan alat yang didefinisikan pengguna: respons berisi blok `tool_use`, kode Anda menjalankan operasi, dan Anda mengirimkan kembali `tool_result`. Alasan untuk menggunakan alat skema Anthropic alih-alih mendefinisikan alat setara Anda sendiri adalah karena skema ini sudah dilatih ke dalam model. Claude telah dioptimalkan pada ribuan trajektori sukses yang menggunakan signature alat persis ini, sehingga ia memanggilnya dengan lebih andal dan pulih dari kesalahan dengan lebih baik dibandingkan dengan alat kustom yang melakukan hal yang sama. Skema tersebut adalah antarmuka yang sudah diharapkan oleh model.

### Alat yang dieksekusi di server

Untuk `web_search`, `web_fetch`, `code_execution`, dan `tool_search`, Anthropic yang menjalankan kodenya. Anda mengaktifkan alat dalam permintaan Anda dan server menangani sisanya. Anda tidak pernah membuat blok `tool_result` untuk alat-alat ini karena loop sisi server mengeksekusi operasi dan memasukkan output kembali ke model sebelum respons mencapai Anda.

Respons yang Anda terima berisi blok `server_tool_use` yang menunjukkan apa yang dijalankan dan apa yang dikembalikan, tetapi pada saat Anda melihatnya, eksekusi sudah selesai. Tugas aplikasi Anda adalah mengaktifkan alat dan membaca jawaban akhir, bukan berpartisipasi dalam loop eksekusi.

## Loop agentik (alat klien)

Alat yang dieksekusi di klien (baik yang didefinisikan pengguna maupun skema Anthropic) mengharuskan aplikasi Anda untuk menjalankan sebuah loop. Model tidak dapat menjalankan kode Anda, jadi setiap pemanggilan alat adalah perjalanan bolak-balik: model meminta, Anda mengeksekusi, Anda melaporkan kembali, model melanjutkan.

Bentuk kanonisnya adalah loop `while` yang didasarkan pada `stop_reason`:

1. Kirim permintaan dengan array `tools` Anda dan pesan pengguna.
2. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`.
3. Eksekusi setiap alat. Format output sebagai blok `tool_result`.
4. Kirim permintaan baru yang berisi pesan asli, respons asisten, dan pesan pengguna dengan blok `tool_result`.
5. Ulangi dari langkah 2 selama `stop_reason` adalah `"tool_use"`.

Dalam praktiknya, ini dibaca sebagai: selama `stop_reason == "tool_use"`, eksekusi alat dan lanjutkan percakapan. Loop keluar pada stop reason lainnya (`"end_turn"`, `"max_tokens"`, `"stop_sequence"`, atau `"refusal"`), yang berarti Claude telah menghasilkan jawaban akhir atau berhenti karena alasan lain yang harus ditangani oleh aplikasi Anda.

Untuk mekanisme membangun permintaan, menangani pemanggilan alat paralel, dan memformat hasil, lihat [Menangani pemanggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Loop sisi server

Alat yang dieksekusi di server menjalankan loop mereka sendiri di dalam infrastruktur Anthropic. Satu permintaan dari aplikasi Anda mungkin memicu beberapa pencarian web atau eksekusi kode sebelum respons dikembalikan. Model mencari, membaca hasil, memutuskan untuk mencari lagi, dan mengulangi hingga mendapatkan apa yang dibutuhkan, semuanya tanpa partisipasi aplikasi Anda.

Loop internal ini memiliki batas iterasi. Jika model masih melakukan iterasi ketika mencapai batas tersebut, respons dikembalikan dengan `stop_reason: "pause_turn"` alih-alih `"end_turn"`. Giliran yang dijeda berarti pekerjaan belum selesai; kirim ulang percakapan (termasuk respons yang dijeda) untuk membiarkan model melanjutkan dari tempat terakhirnya. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) untuk pola kelanjutan.

## Kapan menggunakan alat (dan kapan tidak)

Penggunaan alat cocok ketika tugas memerlukan sesuatu yang tidak dapat dilakukan model dari teks saja:

* **Tindakan dengan efek samping.** Mengirim email, menulis file, memperbarui record. Model dapat mendeskripsikan tindakan ini, tetapi hanya alat yang dapat melakukannya.
* **Data baru atau eksternal.** Harga terkini, cuaca hari ini, isi database. Apa pun di luar data pelatihan atau yang spesifik untuk sistem Anda memerlukan alat untuk mengambilnya.
* **Output terstruktur dengan bentuk yang terjamin.** Ketika Anda membutuhkan objek JSON dengan field tertentu alih-alih prosa yang kebetulan berisi informasi tersebut, skema alat memaksakan bentuknya.
* **Memanggil sistem yang sudah ada.** Database, API internal, sistem file. Penggunaan alat adalah jembatan antara permintaan bahasa alami dan sistem yang memenuhinya.

Tanda bahwa Anda seharusnya menggunakan alat: jika Anda menulis regex untuk mengekstrak keputusan dari output model, keputusan itu seharusnya berupa pemanggilan alat. Mem-parsing teks bebas untuk memulihkan maksud terstruktur adalah tanda bahwa struktur tersebut seharusnya ada di skema.

Penggunaan alat tidak cocok ketika:

* Model dapat menjawab dari pelatihan saja. Peringkasan, terjemahan, dan pertanyaan pengetahuan umum tidak memerlukan perjalanan bolak-balik alat.
* Interaksi adalah tanya jawab satu kali tanpa efek samping. Jika tidak ada yang perlu dieksekusi, tidak ada yang perlu dilakukan oleh alat.
* "Latency" (latensi) pemanggilan alat akan mendominasi respons yang sepele. Setiap pemanggilan alat setidaknya satu perjalanan bolak-balik tambahan; untuk tugas ringan, overhead-nya bisa melebihi pekerjaannya.

## Memilih di antara pendekatan

| Pendekatan                             | Kapan menggunakannya                                         | Apa yang diharapkan                                                                                      | Pelajari lebih lanjut                                                  |
| -------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Alat klien yang didefinisikan pengguna | Logika bisnis kustom, API internal, data proprietary         | Anda menangani eksekusi dan loop agentik                                                                 | [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) |
| Alat klien skema Anthropic             | Operasi dev standar (bash, pengeditan file, kontrol browser) | Anda menangani eksekusi; Claude memanggil alat dengan andal karena skemanya sudah dilatih ke dalam model | [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference)    |
| Alat yang dieksekusi di server         | Pencarian web, sandbox kode, pengambilan web                 | Anthropic menangani eksekusi; Anda mendapatkan hasil secara langsung                                     | [Alat server](/docs/id/agents-and-tools/tool-use/server-tools)         |

## Langkah selanjutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Membangun agen yang menggunakan alat">
    Bangun agen langkah demi langkah dari satu pemanggilan alat hingga produksi.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/define-tools" title="Mendefinisikan alat">
    Spesifikasi skema, deskripsi, dan tool\_choice.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori alat yang disediakan Anthropic.
  </Card>
</CardGroup>
