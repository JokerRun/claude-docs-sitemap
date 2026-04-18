---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/how-tool-use-works
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 5721d1be8455a610ac6033d630c4d81f2d43acc8a8de83e28c5b9a5ec3989f98
---

# Cara kerja penggunaan alat

Pahami loop penggunaan alat, di mana alat dijalankan, dan kapan menggunakan alat daripada prosa.

---

Halaman ini menjelaskan konsep di balik penggunaan alat: di mana alat berjalan, bagaimana loop agentic bekerja, dan kapan penggunaan alat adalah pendekatan yang tepat. Untuk panduan praktis, mulai dengan [tutorial](/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent) atau [panduan implementasi](/docs/id/agents-and-tools/tool-use/define-tools).

## Kontrak penggunaan alat

Penggunaan alat adalah kontrak antara aplikasi Anda dan model. Anda menentukan operasi apa yang tersedia dan bentuk input serta output mereka; Claude memutuskan kapan dan bagaimana memanggilnya. Model tidak pernah menjalankan apa pun dengan sendirinya. Model mengeluarkan permintaan terstruktur, kode Anda (atau server Anthropic) menjalankan operasi, dan hasilnya mengalir kembali ke percakapan.

Kontrak ini membuat model berperilaku kurang seperti generator teks dan lebih seperti fungsi yang Anda panggil. Insinyur dengan pengalaman API klasik dapat mengintegrasikan penggunaan alat dengan cara yang sama seperti antarmuka yang diketik lainnya: tentukan skema, tangani callback, kembalikan hasil. Perbedaannya adalah bahwa pemanggil di sisi lain adalah model bahasa yang memilih fungsi mana yang akan dipanggil berdasarkan percakapan.

## Di mana alat berjalan

Sumbu utama di mana alat berbeda adalah di mana kode dijalankan. Setiap alat termasuk dalam salah satu dari tiga kategori, dan kategori menentukan apa yang bertanggung jawab untuk aplikasi Anda.

### Alat yang ditentukan pengguna (dijalankan klien)

Anda menulis skema, Anda menjalankan kode, Anda mengembalikan hasilnya. Ini adalah acara utama: sebagian besar lalu lintas penggunaan alat adalah alat yang ditentukan pengguna yang memanggil logika khusus aplikasi.

Ketika Claude memutuskan untuk menggunakan salah satu alat Anda, respons API berisi blok `tool_use` dengan nama alat dan objek JSON argumen. Aplikasi Anda mengekstrak argumen tersebut, menjalankan operasi (kueri database, panggilan HTTP, penulisan file, apa pun yang dilakukan alat), dan mengirim output kembali dalam blok `tool_result` pada permintaan berikutnya. Claude tidak pernah melihat implementasi Anda; itu hanya melihat skema yang Anda berikan dan hasil yang Anda kembalikan.

### Alat skema Anthropic (dijalankan klien)

Untuk beberapa operasi umum (menjalankan perintah shell, mengedit file, mengontrol browser, mengelola memori scratchpad), Anthropic menerbitkan skema alat dan aplikasi Anda menangani eksekusi. Alat dalam kategori ini adalah `bash`, `text_editor`, `computer`, dan `memory`.

Model eksekusi identik dengan alat yang ditentukan pengguna: respons berisi blok `tool_use`, kode Anda menjalankan operasi, dan Anda mengirim kembali `tool_result`. Alasan untuk menggunakan alat skema Anthropic daripada mendefinisikan yang setara adalah bahwa skema ini dilatih. Claude telah dioptimalkan pada ribuan lintasan sukses yang menggunakan tanda tangan alat yang tepat ini, jadi itu memanggilnya lebih andal dan pulih dari kesalahan dengan lebih elegan daripada yang akan dilakukan dengan alat khusus yang melakukan hal yang sama. Skema adalah antarmuka yang sudah diharapkan model.

### Alat yang dijalankan server

Untuk `web_search`, `web_fetch`, `code_execution`, dan `tool_search`, Anthropic menjalankan kode. Anda mengaktifkan alat dalam permintaan Anda dan server menangani semuanya yang lain. Anda tidak pernah membuat blok `tool_result` untuk alat ini karena loop sisi server menjalankan operasi dan memberi makan output kembali ke model sebelum respons mencapai Anda.

Respons yang Anda terima berisi blok `server_tool_use` yang menunjukkan apa yang berjalan dan apa yang kembali, tetapi pada saat Anda melihatnya, eksekusi sudah selesai. Pekerjaan aplikasi Anda adalah mengaktifkan alat dan membaca jawaban akhir, bukan berpartisipasi dalam loop eksekusi.

## Loop agentic (alat klien)

Alat yang dijalankan klien (baik yang ditentukan pengguna maupun skema Anthropic) memerlukan aplikasi Anda untuk menjalankan loop. Model tidak dapat menjalankan kode Anda, jadi setiap panggilan alat adalah perjalanan bolak-balik: model bertanya, Anda menjalankan, Anda melaporkan kembali, model melanjutkan.

Bentuk kanonik adalah loop `while` yang dikunci pada `stop_reason`:

1. Kirim permintaan dengan array `tools` Anda dan pesan pengguna.
2. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`.
3. Jalankan setiap alat. Format output sebagai blok `tool_result`.
4. Kirim permintaan baru yang berisi pesan asli, respons asisten, dan pesan pengguna dengan blok `tool_result`.
5. Ulangi dari langkah 2 sementara `stop_reason` adalah `"tool_use"`.

Dalam praktiknya ini berbunyi: sementara `stop_reason == "tool_use"`, jalankan alat dan lanjutkan percakapan. Loop keluar pada alasan berhenti lainnya (`"end_turn"`, `"max_tokens"`, `"stop_sequence"`, atau `"refusal"`), yang berarti Claude telah menghasilkan jawaban akhir atau berhenti karena alasan lain yang harus ditangani aplikasi Anda.

Untuk mekanika membangun permintaan, menangani panggilan alat paralel, dan memformat hasil, lihat [Tangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Loop sisi server

Alat yang dijalankan server menjalankan loop mereka sendiri di dalam infrastruktur Anthropic. Satu permintaan dari aplikasi Anda mungkin memicu beberapa pencarian web atau eksekusi kode sebelum respons kembali. Model mencari, membaca hasil, memutuskan untuk mencari lagi, dan melakukan iterasi sampai memiliki apa yang dibutuhkan, semuanya tanpa aplikasi Anda berpartisipasi.

Loop internal ini memiliki batas iterasi. Jika model masih melakukan iterasi ketika mencapai batas, respons kembali dengan `stop_reason: "pause_turn"` daripada `"end_turn"`. Giliran yang dijeda berarti pekerjaan belum selesai; kirim ulang percakapan (termasuk respons yang dijeda) untuk membiarkan model melanjutkan dari tempat ia berhenti. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) untuk pola kelanjutan.

## Kapan menggunakan alat (dan kapan tidak)

Penggunaan alat cocok ketika tugas memerlukan sesuatu yang tidak dapat dilakukan model hanya dari teks:

- **Tindakan dengan efek samping.** Mengirim email, menulis file, memperbarui catatan. Model dapat mendeskripsikan tindakan ini, tetapi hanya alat yang dapat melaksanakannya.
- **Data segar atau eksternal.** Harga saat ini, cuaca hari ini, isi database. Apa pun di luar data pelatihan atau spesifik untuk sistem Anda memerlukan alat untuk mengambilnya.
- **Output terstruktur dengan bentuk terjamin.** Ketika Anda memerlukan objek JSON dengan bidang tertentu daripada prosa yang kebetulan berisi informasi, skema alat memberlakukan bentuk.
- **Memanggil ke sistem yang ada.** Database, API internal, sistem file. Penggunaan alat adalah jembatan antara permintaan bahasa alami dan sistem yang memenuhinya.

Tanda bahwa Anda harus menggunakan alat: jika Anda menulis regex untuk mengekstrak keputusan dari output model, keputusan itu seharusnya telah menjadi panggilan alat. Mengurai teks bentuk bebas untuk memulihkan niat terstruktur adalah tanda bahwa struktur milik skema.

Penggunaan alat tidak cocok ketika:

- Model dapat menjawab dari pelatihan saja. Ringkasan, terjemahan, dan pertanyaan pengetahuan umum tidak memerlukan putaran alat.
- Interaksi adalah Q&A satu kali tanpa efek samping. Jika tidak ada yang dijalankan, tidak ada yang dapat dilakukan alat.
- Latensi pemanggilan alat akan mendominasi respons sepele. Setiap panggilan alat setidaknya satu putaran ekstra; untuk tugas ringan overhead dapat melebihi pekerjaan.

## Memilih antara pendekatan

| Pendekatan | Kapan menggunakannya | Apa yang diharapkan | Pelajari lebih lanjut |
| --- | --- | --- | --- |
| Alat klien yang ditentukan pengguna | Logika bisnis khusus, API internal, data proprietary | Anda menangani eksekusi dan loop agentic | [Tentukan alat](/docs/id/agents-and-tools/tool-use/define-tools) |
| Alat klien skema Anthropic | Operasi dev standar (bash, pengeditan file, kontrol browser) | Anda menangani eksekusi; Claude memanggil alat dengan andal karena skema dilatih | [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference) |
| Alat yang dijalankan server | Pencarian web, sandbox kode, pengambilan web | Anthropic menangani eksekusi; Anda mendapatkan hasil secara langsung | [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) |

## Langkah berikutnya

<CardGroup>
  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Bangun agen yang menggunakan alat">
    Bangun agen langkah demi langkah dari satu panggilan alat hingga produksi.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/define-tools" title="Tentukan alat">
    Spesifikasi skema, deskripsi, dan tool_choice.
  </Card>
  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat">
    Direktori alat yang disediakan Anthropic.
  </Card>
</CardGroup>