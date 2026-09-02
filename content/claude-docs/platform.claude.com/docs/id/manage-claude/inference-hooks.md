---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: fcaea5aa712c230e9ecf2cf5444bb69eb7f082144b923709d7db1f80eded5e26
---

---
title: Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
description: Kirim setiap prompt yang diatur ke server keamanan AI organisasi Anda untuk mendapatkan putusan izinkan atau tolak sebelum inferensi berjalan.
---

<Note>
  Inference hooks masih dalam versi beta dan tersedia untuk organisasi Claude Enterprise. Mengonfigurasinya memerlukan izin `organization:manage` di claude.ai, yang dimiliki oleh peran bawaan Admin, Owner, dan Primary owner; lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).
</Note>

"Inference hooks" (kait inferensi) memungkinkan organisasi Claude Enterprise merutekan setiap prompt yang diatur melalui server keamanan AI, yaitu layanan HTTPS yang dioperasikan oleh organisasi atau vendor keamanannya, sebelum inferensi berjalan. Ketika pengguna mengirimkan prompt, Anthropic mengirim transkrip percakapan ke server keamanan AI Anda dan menunggu putusan izinkan atau tolak; permintaan yang ditolak tidak pernah mencapai model. Tim keamanan dan kepatuhan menggunakan Inference hooks untuk menegakkan kebijakan data secara inline, dan developer membangun server keamanan AI yang mengevaluasi setiap permintaan.

Karena hook berjalan di server Anthropic, setelah permintaan meninggalkan klien dan sebelum model berjalan, hook ini berlaku untuk setiap permintaan yang diatur secara seragam, tanpa perlu menginstal atau menerapkan apa pun di perangkat pengguna.

Saat ini satu-satunya event hook adalah `prompt`, yang dipicu sekali per permintaan inferensi yang diatur, sebelum inferensi dimulai. Penegakan di sisi respons direncanakan sebagai event berikutnya.

***

## Cara kerja Inference hooks

1. Pengguna mengirimkan prompt pada permukaan yang diatur.
2. Anthropic mengirim HTTPS `POST` ke endpoint server keamanan AI yang dikonfigurasi organisasi Anda. Body permintaan membawa transkrip percakapan, dan setiap permintaan ditandatangani sesuai spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/) setelah organisasi Anda membuat signing secret-nya, sehingga server Anda dapat memverifikasi bahwa permintaan tersebut berasal dari Anthropic.
3. Server keamanan AI Anda mengevaluasi konten dan merespons dengan putusan dalam batas waktu putusan yang dikonfigurasi organisasi Anda (5 detik secara default).
4. Pada `allow`, inferensi berjalan seperti biasa. Pada `deny`, permintaan ditolak dan pengguna melihat pesan diblokir-oleh-kebijakan yang disusun dari dua bagian: alasan per permintaan yang diberikan server keamanan AI Anda dalam field `deny_reason` pada putusan, diikuti pesan tetap yang dikonfigurasi administrator Anda (misalnya, siapa yang harus dihubungi atau di mana meminta pengecualian). Jika administrator Anda belum mengonfigurasinya, pesan default bawaan mengarahkan pengguna untuk menghubungi mereka. Setiap penolakan juga dicatat dalam [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda.

Diagram berikut menelusuri satu contoh (permintaan Cowork di mana Claude juga memanggil alat O365) untuk mengilustrasikan bagian mana dari alur yang dikaitkan dengan hook. Titik-titik yang dikaitkan adalah langkah 1 dan 5 pada diagram, tempat prompt tiba dan hasil alat (tool result) dikembalikan; masing-masing menghasilkan pertukaran validasi dengan server keamanan AI (AI security server) Anda yang ditunjukkan pada langkah 2 dan 6.

![Diagram alur: server keamanan AI (AI security server) memvalidasi prompt dan hasil alat (tool result) sebelum inferensi berjalan](https://platform.claude.com/docs/images/inference-hooks-flow.svg)

Putusan adalah objek JSON kecil: `{"action": "allow"}` membiarkan permintaan berjalan, dan deny membawa alasan yang ditampilkan kepada pengguna. Untuk skema putusan lengkap, lihat [Mengembalikan putusan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#return-a-verdict).

Server keamanan AI Anda melihat apa yang dilihat pengguna: teks transkrip, pemanggilan alat dan hasilnya, serta teks yang diekstrak dari lampiran. Server tidak pernah menerima byte mentah file atau gambar, prompt sistem, atau konteks internal Anthropic. Anthropic tidak menyimpan konten prompt atau respons sebagai bagian dari Inference hooks; Anthropic hanya mencatat metadata tentang aktivitas hook, seperti putusan, stempel waktu, dan pengidentifikasi permintaan.

Jika server keamanan AI Anda tidak dapat dijangkau, mengembalikan error, atau tidak merespons dalam batas waktu, pengaturan penanganan kegagalan organisasi Anda menentukan hasilnya: memblokir permintaan, atau mengizinkannya berjalan tanpa inspeksi.

Penegakan dapat diluncurkan sesuai kecepatan Anda, sehingga tidak ada yang harus diblokir pada hari pertama: shadow mode mengamati putusan pada lalu lintas langsung tanpa memblokir apa pun, persentase peluncuran menginspeksi sebagian permintaan yang dipilih, dan pengecualian membebaskan anggota peran tertentu sepenuhnya. Lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).

Untuk skema permintaan dan respons lengkap, verifikasi tanda tangan, dan detail operasional, lihat [Mengembangkan integrasi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

***

## Kasus penggunaan

* **Data loss prevention (pencegahan kehilangan data), atau DLP.** Teruskan transkrip ke pemindai DLP Anda dan tolak prompt yang membawa materi yang diatur regulasi atau diklasifikasikan. Ini adalah penerapan yang paling umum.
* **Pengarsipan transkrip real-time.** Arsipkan setiap transkrip saat tiba dan selalu kembalikan `allow`, sebagai alternatif berbasis push untuk polling [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api).
* **Telemetri prompt.** Ukur bagaimana organisasi Anda menggunakan Claude, pada saat penggunaan.
* **Mesin kebijakan.** Tegakkan aturan Anda sendiri sebelum inferensi: allowlist model, pembatasan berlingkup proyek, atau kontrol jam kerja.

***

## Keterbatasan saat ini

* Lampiran direpresentasikan oleh metadata dan teks yang diekstrak. Byte mentah file dan gambar tidak pernah dikirim, sehingga konten yang hanya berupa gambar (misalnya, tangkapan layar dokumen) tidak diinspeksi.
* Putusan berupa izinkan atau tolak. Menulis ulang atau menyunting (redacting) prompt tidak didukung.
* Organisasi platform (akses API melalui Claude Platform) berada di luar cakupan.

***

## Ketersediaan

Inference hooks tersedia untuk organisasi Claude Enterprise. Mengonfigurasinya memerlukan izin `organization:manage`, yang dimiliki oleh peran bawaan Admin, Owner, dan Primary owner, serta peran kustom apa pun yang diberi izin tersebut.

Satu hook mengatur percakapan di seluruh claude.ai, Cowork, dan sesi Claude Code dalam organisasi Claude Enterprise Anda, baik yang berjalan di web, di aplikasi desktop, maupun di CLI. Inference hooks tidak tersedia di Amazon Bedrock atau Google Cloud.

Permintaan yang diatur adalah permintaan inferensi di balik percakapan pengguna. Permintaan tambahan, seperti pembuatan judul percakapan, tidak dikirim ke endpoint Anda, dan prompt sistem serta definisi alat tidak pernah disertakan dalam apa yang dikirim. Mode suara tidak tercakup.

***

## Inference hooks versus Compliance API

Kedua fitur melayani tim keamanan, hukum, dan kepatuhan di organisasi Claude Enterprise.

|                    | Inference hooks                                                         | Compliance API                                                                               |
| ------------------ | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Kapan bertindak    | Inline, sebelum inferensi berjalan                                      | Setelah kejadian                                                                             |
| Apa yang dilakukan | Mengizinkan atau menolak setiap permintaan yang diatur secara real time | Mengambil aktivitas, chat, file, proyek, transkrip sesi, dan pengguna untuk audit dan ekspor |
| Arah               | Anthropic memanggil server keamanan AI Anda                             | Anda memanggil API Anthropic                                                                 |

Gunakan Inference hooks untuk menghentikan permintaan sebelum mencapai model, dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) untuk mengaudit apa yang terjadi setelahnya.

***

## Di bagian ini

<CardGroup>
  <Card href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration" title="Mengonfigurasi Inference hooks">
    Izinkan Inference hooks untuk organisasi Anda, siapkan dan uji server keamanan AI Anda, pilih penanganan kegagalan, dan tegakkan putusan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint" title="Mengembangkan integrasi Inference hooks">
    Skema permintaan dan putusan, verifikasi tanda tangan, semantik operasional, dan pola integrasi untuk membangun server keamanan AI.
  </Card>
</CardGroup>
