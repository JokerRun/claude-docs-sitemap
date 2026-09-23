---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: 4fcd513405173a2370160e68edaa24fd728b2ecd01c45e7cfb5592fce2045ded
---

---
title: Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
description: Kirim setiap prompt yang diatur ke server keamanan AI organisasi Anda untuk mendapatkan putusan izinkan atau tolak sebelum inferensi dilanjutkan.
---

<Note>
  Inference hooks masih dalam tahap beta dan tersedia untuk organisasi Claude Enterprise. Untuk mengonfigurasinya, Anda memerlukan izin `organization:manage` di claude.ai, yang hanya dimiliki oleh peran Owner dan Primary owner; lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).
</Note>

Inference hooks memungkinkan organisasi Claude Enterprise merutekan setiap prompt yang diatur melalui "AI security server" (server keamanan AI) sebelum inferensi berjalan. Server ini adalah layanan HTTPS yang dioperasikan oleh organisasi atau vendor keamanannya. Saat pengguna mengirimkan prompt, Anthropic mengirimkan transkrip percakapan ke server keamanan AI Anda dan menunggu putusan izinkan atau tolak. Permintaan yang ditolak tidak akan pernah sampai ke model. Tim keamanan dan kepatuhan menggunakan Inference hooks untuk menegakkan kebijakan data secara langsung (inline), sementara developer membangun server keamanan AI yang mengevaluasi setiap permintaan.

Hook berjalan di server Anthropic, yaitu setelah permintaan meninggalkan klien dan sebelum model berjalan. Karena itu, hook berlaku secara seragam untuk setiap permintaan yang diatur, tanpa perlu memasang atau men-deploy apa pun di perangkat pengguna.

Saat ini, satu-satunya event hook adalah `prompt`. Event ini dipicu satu kali per permintaan inferensi yang diatur, sebelum inferensi dimulai. Penegakan di sisi respons direncanakan sebagai event di kemudian hari.

***

## Cara kerja Inference hooks

1. Pengguna mengirimkan prompt pada permukaan yang diatur.

2. Anthropic mengirimkan HTTPS `POST` ke endpoint server keamanan AI yang dikonfigurasi organisasi Anda. Body permintaan berisi transkrip percakapan. Setelah organisasi Anda membuat signing secret, setiap permintaan ditandatangani sesuai spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/), sehingga server Anda dapat memverifikasi bahwa permintaan tersebut berasal dari Anthropic.

3. Server keamanan AI Anda mengevaluasi konten dan merespons dengan putusan dalam batas waktu putusan yang dikonfigurasi organisasi Anda (default 5 detik).

4. Jika putusannya `allow`, inferensi berjalan seperti biasa. Jika putusannya `deny`, permintaan ditolak dan pengguna melihat pesan diblokir-oleh-kebijakan yang tersusun dari dua bagian:

   * alasan per permintaan yang diberikan server keamanan AI Anda di field `deny_reason` pada putusan;
   * pesan tetap yang dikonfigurasi administrator Anda (misalnya, siapa yang harus dihubungi atau di mana mengajukan pengecualian). Jika administrator belum mengonfigurasinya, pesan default bawaan akan mengarahkan pengguna untuk menghubungi mereka.

   Setiap penolakan juga dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda.

Diagram berikut menelusuri satu contoh, yaitu permintaan Cowork di mana Claude juga memanggil alat O365, untuk menunjukkan bagian alur mana yang di-hook. Titik yang di-hook adalah langkah 1 dan 6 pada diagram, yaitu saat prompt tiba dan saat hasil alat kembali. Masing-masing memicu pertukaran validasi dengan server keamanan AI Anda, seperti yang ditunjukkan pada langkah 2–3 dan 7–8.

![Diagram alur: "AI security server" (server keamanan AI) memvalidasi prompt dan "tool result" (hasil alat) sebelum inferensi dilanjutkan](https://platform.claude.com/docs/images/inference-hooks-flow.png)

Putusan berupa objek JSON kecil. `{"action": "allow"}` mengizinkan permintaan dilanjutkan, sedangkan putusan tolak menyertakan alasan yang ditampilkan kepada pengguna. Untuk skema putusan lengkap, lihat [Mengembalikan putusan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#return-a-verdict).

Server keamanan AI Anda melihat apa yang dilihat pengguna: teks transkrip, panggilan alat beserta hasilnya, dan teks yang diekstrak dari lampiran. Server ini tidak pernah menerima byte mentah file atau gambar, prompt sistem, maupun konteks internal Anthropic.

Sistem Inference hooks tidak menyimpan salinan konten prompt atau respons. Sistem ini hanya menyimpan konfigurasi hook Anda dan metadata tentang aktivitas hook, seperti putusan, stempel waktu, dan pengidentifikasi permintaan. Produk Claude yang Anda gunakan menyimpan prompt dan respons sesuai aturan retensi datanya sendiri, baik hook aktif maupun tidak. Misalnya, pesan yang diblokir hook di claude.ai tetap ada di percakapan.

Jika server keamanan AI Anda tidak dapat dijangkau, mengembalikan error, atau tidak merespons dalam batas waktu, pengaturan penanganan kegagalan organisasi Anda yang menentukan hasilnya: memblokir permintaan, atau mengizinkannya berjalan tanpa inspeksi.

Kegagalan berkelanjutan yang disebabkan oleh server Anda akan memicu "circuit breaker" (pemutus sirkuit). Dalam kondisi ini, Anthropic berhenti menghubungi server Anda dan menerapkan pengaturan penanganan kegagalan Anda ke setiap permintaan. Pemutus sirkuit akan direset secara otomatis setelah Anthropic mendeteksi bahwa server Anda kembali mengembalikan putusan. Lihat [Circuit breaker](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#circuit-breaker).

Penegakan dapat diluncurkan sesuai kecepatan Anda, sehingga tidak ada yang perlu diblokir sejak hari pertama. Tersedia tiga opsi:

* "Shadow mode" (mode bayangan) mengamati putusan pada lalu lintas langsung tanpa memblokir apa pun.
* "Rollout percentage" (persentase peluncuran) menginspeksi sebagian permintaan sesuai proporsi yang Anda pilih.
* Pengecualian membebaskan anggota peran tertentu sepenuhnya.

Lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).

Untuk skema permintaan dan respons lengkap, verifikasi tanda tangan, dan detail operasional, lihat [Mengembangkan integrasi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

***

## Kasus penggunaan

* **"Data loss prevention" (pencegahan kehilangan data), atau DLP.** Teruskan transkrip ke pemindai DLP Anda dan tolak prompt yang memuat materi yang diatur regulasi atau bersifat rahasia. Ini adalah penerapan yang paling umum.
* **Pengarsipan transkrip secara real-time.** Arsipkan setiap transkrip saat tiba dan selalu kembalikan `allow`. Cara ini menjadi alternatif berbasis push untuk polling [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api).
* **Telemetri prompt.** Ukur cara organisasi Anda menggunakan Claude, tepat pada saat penggunaan.
* **Mesin kebijakan.** Tegakkan aturan Anda sendiri sebelum inferensi, seperti allowlist model, pembatasan berbasis proyek, atau kontrol jam kerja.

***

## Keterbatasan saat ini

* Lampiran direpresentasikan oleh metadata dan teks yang diekstrak. Byte mentah file dan gambar tidak pernah dikirim, sehingga konten yang hanya berupa gambar (misalnya, tangkapan layar dokumen) tidak diinspeksi.
* Putusan hanya berupa izinkan atau tolak. Penulisan ulang atau penyuntingan (redaksi) prompt tidak didukung.
* Organisasi Platform (akses API melalui Claude Platform) berada di luar cakupan.

***

## Ketersediaan

Inference hooks tersedia untuk organisasi Claude Enterprise. Untuk mengonfigurasinya, Anda memerlukan izin `organization:manage`, yang hanya dimiliki oleh peran Owner dan Primary owner.

Satu hook mengatur percakapan di seluruh sesi claude.ai, Cowork, dan Claude Code dalam organisasi Claude Enterprise Anda, baik yang berjalan di web, di aplikasi desktop atau seluler, maupun di CLI. Inference hooks tidak tersedia di Amazon Bedrock atau Google Cloud.

Permintaan yang diatur adalah permintaan inferensi di balik percakapan pengguna. Permintaan tambahan, seperti pembuatan judul percakapan, tidak dikirim ke endpoint Anda. Prompt sistem dan definisi alat juga tidak pernah disertakan dalam data yang dikirim. Mode suara tidak tercakup.

***

## Inference hooks dibandingkan dengan Compliance API

Kedua fitur ini melayani tim keamanan, hukum, dan kepatuhan di organisasi Claude Enterprise.

|                    | Inference hooks                                                         | Compliance API                                                                               |
| ------------------ | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Kapan bertindak    | Secara inline, sebelum inferensi berjalan                               | Setelah kejadian                                                                             |
| Apa yang dilakukan | Mengizinkan atau menolak setiap permintaan yang diatur secara real-time | Mengambil aktivitas, chat, file, proyek, transkrip sesi, dan pengguna untuk audit dan ekspor |
| Arah               | Anthropic memanggil server keamanan AI Anda                             | Anda memanggil API Anthropic                                                                 |

Gunakan Inference hooks untuk menghentikan permintaan sebelum mencapai model, dan gunakan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) untuk mengaudit apa yang terjadi setelahnya.

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
