---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 896317113bf0493367a762c90486fe561c73c21cdf17f465fba539ddc868fdc1
---

---
title: Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks
description: Kirim setiap prompt yang diatur ke server keamanan AI organisasi Anda untuk mendapatkan keputusan izinkan atau tolak sebelum inferensi dilanjutkan.
---

<Note>
  Inference hooks masih dalam tahap beta dan tersedia untuk organisasi Claude Enterprise. Mengonfigurasinya memerlukan izin `organization:manage` di claude.ai, yang dimiliki oleh peran bawaan Admin, Owner, dan Primary owner; lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).
</Note>

"Inference hooks" (kait inferensi) memungkinkan organisasi Claude Enterprise merutekan setiap prompt yang diatur melalui server keamanan AI, yaitu layanan HTTPS yang dioperasikan oleh organisasi atau vendor keamanannya, sebelum inferensi dijalankan. Ketika pengguna mengirimkan prompt, Anthropic mengirimkan transkrip percakapan ke server keamanan AI Anda dan menunggu keputusan izinkan atau tolak; permintaan yang ditolak tidak akan pernah mencapai model. Tim keamanan dan kepatuhan menggunakan Inference hooks untuk menegakkan kebijakan data secara inline, dan developer membangun server keamanan AI yang mengevaluasi setiap permintaan.

Karena hook berjalan di server Anthropic, setelah permintaan meninggalkan klien dan sebelum model dijalankan, hook ini diterapkan secara seragam pada setiap permintaan yang diatur, tanpa perlu menginstal atau men-deploy apa pun di perangkat pengguna.

Saat ini satu-satunya event hook adalah `prompt`, yang dipicu satu kali per permintaan inferensi yang diatur, sebelum inferensi dimulai. Penegakan di sisi respons direncanakan sebagai event berikutnya.

***

## Cara kerja Inference hooks

1. Pengguna mengirimkan prompt pada permukaan yang diatur.
2. Anthropic mengirimkan `POST` HTTPS ke endpoint server keamanan AI yang dikonfigurasi organisasi Anda. Body permintaan membawa transkrip percakapan, dan setiap permintaan ditandatangani sesuai spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/) setelah organisasi Anda menghasilkan signing secret-nya, sehingga server Anda dapat memverifikasi bahwa permintaan tersebut berasal dari Anthropic.
3. Server keamanan AI Anda mengevaluasi konten dan merespons dengan keputusan dalam batas waktu keputusan yang dikonfigurasi organisasi Anda (5 detik secara default).
4. Pada `allow`, inferensi dilanjutkan secara normal. Pada `deny`, permintaan ditolak dan pengguna melihat pesan diblokir-oleh-kebijakan yang disusun dari dua bagian: alasan per-permintaan yang disediakan server keamanan AI Anda dalam field `deny_reason` pada keputusan, diikuti oleh pesan tetap yang dikonfigurasi administrator Anda (misalnya, siapa yang harus dihubungi atau di mana meminta pengecualian). Jika administrator Anda belum mengonfigurasinya, pesan default bawaan akan mengarahkan pengguna untuk menghubungi mereka. Setiap penolakan juga dicatat dalam [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda.

Diagram berikut menelusuri satu contoh (permintaan Cowork di mana Claude juga memanggil alat O365) untuk mengilustrasikan bagian mana dari alur yang di-hook. Titik-titik yang di-hook adalah langkah 1 dan 5 pada diagram, di mana prompt tiba dan hasil alat dikembalikan; masing-masing menghasilkan pertukaran validasi dengan server keamanan AI Anda yang ditunjukkan pada langkah 2 dan 6.

![Diagram alur: server keamanan AI memvalidasi prompt dan hasil alat sebelum inferensi dilanjutkan](https://platform.claude.com/docs/images/inference-hooks-flow.svg)

Keputusan adalah objek JSON kecil: `{"action": "allow"}` membiarkan permintaan dilanjutkan, dan deny membawa alasan yang ditampilkan kepada pengguna. Untuk skema keputusan lengkap, lihat [Mengembalikan keputusan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#return-a-verdict).

Server keamanan AI Anda melihat apa yang dilihat pengguna: teks transkrip, panggilan alat dan hasilnya, serta teks yang diekstrak dari lampiran. Server tidak pernah menerima byte file atau gambar mentah, prompt sistem, atau konteks internal Anthropic.

Jika server keamanan AI Anda tidak dapat dijangkau, mengembalikan error, atau tidak merespons dalam batas waktu, pengaturan penanganan kegagalan organisasi Anda menentukan hasilnya: blokir permintaan, atau izinkan permintaan dilanjutkan tanpa inspeksi.

Penegakan dapat diluncurkan sesuai kecepatan Anda, sehingga tidak ada yang harus diblokir pada hari pertama: mode bayangan mengamati keputusan pada lalu lintas langsung tanpa memblokir apa pun, persentase peluncuran menginspeksi sebagian permintaan yang dipilih, dan pengecualian membebaskan anggota dari peran yang dipilih sepenuhnya. Lihat [Mengonfigurasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration).

Untuk skema permintaan dan respons lengkap, verifikasi tanda tangan, dan detail operasional, lihat [Mengembangkan integrasi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

***

## Kasus penggunaan

* **Data loss prevention (DLP).** Teruskan transkrip ke pemindai DLP Anda dan tolak prompt yang membawa materi yang diatur atau diklasifikasikan. Ini adalah penerapan yang paling umum.
* **Pengarsipan transkrip real-time.** Arsipkan setiap transkrip saat tiba dan selalu kembalikan `allow`, sebagai alternatif berbasis push untuk polling [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api).
* **Telemetri prompt.** Ukur bagaimana organisasi Anda menggunakan Claude, pada saat penggunaan.
* **Mesin kebijakan.** Tegakkan aturan Anda sendiri sebelum inferensi: daftar izin model, pembatasan berbasis proyek, atau kontrol jam kerja.

***

## Keterbatasan saat ini

* Lampiran direpresentasikan oleh metadata dan teks yang diekstrak. Byte file dan gambar mentah tidak pernah dikirim, sehingga konten yang hanya berupa gambar (misalnya, tangkapan layar dokumen) tidak diinspeksi.
* Keputusan hanya berupa izinkan atau tolak. Menulis ulang atau meredaksi prompt tidak didukung.
* Organisasi Platform (akses API melalui Claude Platform) berada di luar cakupan.

***

## Ketersediaan

Inference hooks tersedia untuk organisasi Claude Enterprise. Mengonfigurasinya memerlukan izin `organization:manage`, yang dimiliki oleh peran bawaan Admin, Owner, dan Primary owner, serta peran kustom apa pun yang diberikan izin tersebut.

Satu hook mengatur percakapan di seluruh claude.ai, Cowork, dan sesi Claude Code dalam organisasi Claude Enterprise Anda, baik yang berjalan di web, di aplikasi desktop, maupun di CLI. Inference hooks tidak tersedia di Amazon Bedrock atau Google Cloud.

Permintaan yang diatur adalah permintaan inferensi di balik percakapan pengguna. Permintaan tambahan, seperti pembuatan judul percakapan, tidak dikirim ke endpoint Anda, dan prompt sistem serta definisi alat tidak pernah disertakan dalam apa yang dikirim. Mode suara tidak tercakup.

***

## Inference hooks versus Compliance API

Kedua fitur ini melayani tim keamanan, hukum, dan kepatuhan di organisasi Claude Enterprise.

|                    | Inference hooks                                                         | Compliance API                                                                                                           |
| ------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Kapan bertindak    | Inline, sebelum inferensi dijalankan                                    | Setelah kejadian                                                                                                         |
| Apa yang dilakukan | Mengizinkan atau menolak setiap permintaan yang diatur secara real time | Mengambil aktivitas, obrolan, file, proyek, transkrip sesi Cowork dan Claude Code, serta pengguna untuk audit dan ekspor |
| Arah               | Anthropic memanggil server keamanan AI Anda                             | Anda memanggil API Anthropic                                                                                             |

Gunakan Inference hooks untuk menghentikan permintaan sebelum mencapai model, dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) untuk mengaudit apa yang terjadi setelahnya.

***

## Dalam bagian ini

<CardGroup>
  <Card href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration" title="Mengonfigurasi Inference hooks">
    Izinkan Inference hooks untuk organisasi Anda, siapkan dan uji server keamanan AI Anda, pilih penanganan kegagalan, dan tegakkan keputusan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint" title="Mengembangkan integrasi Inference hooks">
    Skema permintaan dan keputusan, verifikasi tanda tangan, semantik operasional, dan pola integrasi untuk membangun server keamanan AI.
  </Card>
</CardGroup>
