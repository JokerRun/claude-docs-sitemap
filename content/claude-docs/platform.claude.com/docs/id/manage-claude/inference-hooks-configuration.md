---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 06878e30f835739dde873e76f73ef5c1c8f37ef690df7db2eb38bd0fa463fbb7
---

---
title: Mengonfigurasi Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration
description: Izinkan Inference hooks untuk organisasi Claude Enterprise Anda, hubungkan server keamanan AI Anda, dan kendalikan penegakan, penanganan kegagalan, serta peluncuran bertahap.
---

<Note>
  Inference hooks masih dalam tahap beta dan tersedia untuk organisasi Claude Enterprise. Untuk mengonfigurasinya, Anda memerlukan izin `organization:manage`, yang hanya dimiliki oleh peran Owner dan Primary owner.
</Note>

Inference hooks mengirimkan prompt dari organisasi Anda ke server keamanan AI pilihan Anda. Setiap permintaan ditahan hingga server tersebut memberikan putusan izinkan atau tolak, sebelum Claude memprosesnya. Halaman ini menjelaskan cara mengaktifkan fitur ini, menghubungkan server Anda, dan mengendalikan penegakan. Untuk mempelajari apa itu Inference hooks dan kapan menggunakannya, lihat [ikhtisar Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks). Untuk membangun server keamanan AI itu sendiri, lihat [Mengembangkan integrasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

## Sebelum Anda memulai

Anda memerlukan:

* Izin `organization:manage` di claude.ai, yang hanya dimiliki oleh peran **Owner** dan **Primary owner**. Peran **Admin** tidak memilikinya.
* Endpoint HTTPS server keamanan AI yang menerima permintaan putusan. Endpoint ini harus berupa URL `https://` pada port 443, berada di host yang dapat dirutekan secara publik, dan dapat dijangkau tanpa pengalihan. Host "reverse tunnel" (terowongan balik), seperti ngrok dan layanan terowongan serupa, tidak didukung karena diblokir oleh kebijakan jaringan Anthropic. Jangan melakukan pengujian melalui terowongan; hosting server Anda di domain yang Anda kendalikan. Untuk [persyaratan hosting](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#receive-a-request) selengkapnya, serta cara membangun server dan memverifikasi permintaan yang ditandatangani, lihat [Mengembangkan integrasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

## Menyiapkan Inference hooks

Ada tiga status penegakan:

* **off** (nonaktif): **Enforce verdicts** dimatikan. Server keamanan AI Anda tidak pernah dihubungi dan prompt tidak diperiksa.
* **shadow** (bayangan): **Enforce verdicts** diaktifkan dengan **Mode** diatur ke **Shadow mode**. Server keamanan AI Anda menerima prompt dan mengembalikan putusan, tetapi tidak ada yang diblokir.
* **enforcing** (menegakkan): **Enforce verdicts** diaktifkan dengan **Mode** diatur ke **Allow the request** atau **Block the request**. Putusan tolak akan memblokir permintaan.

Langkah-langkah berikut membawa konfigurasi baru dari status off ke enforcing.

<Steps>
  <Step title="Izinkan Inference hooks untuk organisasi Anda">
    Buka claude.ai > **Organization settings** > **Data and privacy**, lalu temukan bagian **Inference hooks**. Aktifkan **Allow for your organization**.

    Mengaktifkan opsi ini akan membuka halaman pengaturan Inference hooks dan selalu memaksa **Enforce verdicts** dalam keadaan nonaktif. Dengan demikian, mengizinkan fitur ini tidak pernah memulai pemeriksaan dengan sendirinya. Bahkan konfigurasi yang sebelumnya sudah menegakkan putusan tetap tidak diperiksa hingga Anda mengaktifkan kembali **Enforce verdicts** pada langkah terakhir.
  </Step>

  <Step title="Buka halaman pengaturan Inference hooks">
    Masih di **Data and privacy**, buka bagian **Inference hooks** untuk masuk ke halaman pengaturan Inference hooks. Halaman ini berada di bawah Data and privacy, bukan sebagai entri tersendiri di navigasi pengaturan, sehingga breadcrumb-nya bertuliskan **Data and privacy / Inference hooks**. Selama Anda belum menyimpan endpoint, halaman ini menampilkan peringatan bahwa prompt belum diperiksa, dan **Enforce verdicts** tetap nonaktif dengan lencana **Requires endpoint**.
  </Step>

  <Step title="Konfigurasikan endpoint Anda">
    Klik **Configure** untuk membuka dialog **Set up endpoint**, lalu masukkan **Endpoint URL**, yaitu URL `https://` yang menerima permintaan putusan. Hanya URL `https://` yang diterima.

    Pada tahap ini, dialog tidak meminta informasi lain. Header permintaan kustom diatur pada langkah 5, dan penanganan kegagalan pada langkah 6. Klik **Next** untuk menyimpan. Setelah endpoint tersimpan, tombol tersebut berubah menjadi **Edit**.
  </Step>

  <Step title="Simpan signing secret Anda">
    Penyimpanan pertama akan membuat "signing secret" (rahasia penandatanganan) webhook Anda dan menampilkannya satu kali saja. Salin dan simpan rahasia tersebut dengan aman sebelum mengklik **Next**. Rahasia ini tidak dapat diambil kembali nanti; Anda hanya dapat [merotasinya](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#rotate-your-signing-secret).

    Server keamanan AI Anda menggunakan rahasia ini untuk memverifikasi tanda tangan pada setiap permintaan yang diterimanya, termasuk uji koneksi pada langkah berikutnya. Untuk prosedur verifikasinya, lihat [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature).
  </Step>

  <Step title="Tambahkan header permintaan dan uji koneksi">
    Mengklik **Next** pada dialog signing secret akan membuka kembali dialog endpoint, kini dengan dua kontrol tambahan:

    * **Custom request headers:** hingga 16 header statis yang dikirim bersama setiap permintaan putusan agar server keamanan AI Anda dapat mengautentikasi pemanggil.

      * Nilai header disimpan dalam keadaan terenkripsi dan tidak pernah ditampilkan lagi. Setelah disimpan, hanya nama header yang ditampilkan.
      * Karena nilainya hanya dapat ditulis, setiap perubahan pada header mengharuskan Anda memasukkan ulang semua nilai sebelum menyimpan.
      * Mengubah URL endpoint akan menghapus semua nilai header yang tersimpan agar kredensial Anda tidak pernah terkirim ke tujuan baru. Masukkan kembali nilai-nilai tersebut setelah mengubah URL.
      * Nama header harus menggunakan karakter token HTTP standar, dengan `-` alih-alih `_`. Nama header juga tidak boleh bentrok dengan nama yang dicadangkan, yaitu header pembingkaian permintaan seperti `Content-*` dan `Host`, header proxy dan cookie, header alamat klien seperti `X-Forwarded-*`, header tanda tangan `webhook-*`, serta prefiks `X-Anthropic-*`.
      * Nilai header harus berupa ASCII yang dapat dicetak.

    * **Test connection:** Claude mengirimkan prompt uji sintetis ke URL dan header yang saat ini ada di formulir, bukan nilai yang tersimpan. Karena itu, masukkan ulang nilai header yang tersimpan sebelum menguji. Jika berhasil, hasilnya menunjukkan apakah server keamanan AI Anda mengembalikan putusan izinkan atau tolak untuk prompt uji tersebut. Dengan begitu, Anda dapat mengetahui jika server Anda secara default menolak semua permintaan sebelum Anda mulai menegakkan putusan.

    Klik **Save** untuk menyimpan header yang Anda masukkan.

    Hasil kegagalan yang umum:

    | Hasil                      | Yang perlu diperiksa                                                                                                                                               |
    | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | URL ditolak                | URL gagal dalam pemeriksaan struktural. Gunakan URL `https://` pada port 443.                                                                                      |
    | IP privat atau internal    | Host di-resolve ke alamat privat atau internal. Gunakan host yang dapat dirutekan secara publik.                                                                   |
    | Timeout                    | Server keamanan AI tidak mengembalikan putusan dalam batas waktu.                                                                                                  |
    | Kesalahan transport        | Resolusi DNS, TLS handshake, atau koneksi gagal.                                                                                                                   |
    | Status selain 200          | Server keamanan AI merespons dengan status selain 200. Putusan harus dikembalikan sebagai HTTP 200; pengalihan tidak diikuti dan dihitung sebagai kegagalan.       |
    | Respons tidak dapat diurai | Server keamanan AI merespons, tetapi isi responsnya bukan putusan yang valid.                                                                                      |
    | Signing secret diperlukan  | Organisasi Anda tidak memiliki signing secret, sehingga uji akan dikirim tanpa tanda tangan. Klik **Generate secret** di bawah **Request signing**, lalu uji lagi. |
  </Step>

  <Step title="Pilih penanganan kegagalan dan batas waktu">
    Di bawah **Failure handling**, atur **Mode** untuk menentukan apa yang terjadi saat server keamanan AI tidak dapat dijangkau atau putusan melewati batas waktu:

    * **Block the request:** hentikan inferensi ketika server keamanan AI Anda tidak dapat memberikan putusan ("fail closed", gagal tertutup).
    * **Allow the request:** biarkan permintaan diteruskan ke model tanpa pemeriksaan ("fail open", gagal terbuka).

    Opsi ketiga pada dropdown, **Shadow mode**, adalah alat untuk peluncuran bertahap, bukan kebijakan kegagalan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Kemudian atur **Prompt verdict timeout (ms)** dengan nilai 1 hingga 10.000 ms (default 5.000 ms). Batas waktu ini mencakup seluruh pertukaran, dan putusan yang lebih lambat dihitung sebagai server yang tidak dapat dijangkau. Karena itu, atur nilai terendah yang dapat dipenuhi server Anda secara andal.

    Perubahan di bagian ini langsung tersimpan saat Anda membuatnya. Pada penyimpanan pertama, nilai default-nya adalah **Allow the request** dan 5.000 ms.
  </Step>

  <Step title="Pilih persentase peluncuran bertahap">
    Di bawah **Rollout**, atur **Requests inspected (%)** untuk menjalankan pemeriksaan pada sebagian persentase permintaan selama Anda menyiapkan server keamanan AI Anda. Nilainya berkisar dari 0 hingga 100: 100 memeriksa semua permintaan, dan 0 menonaktifkan pemeriksaan.

    Pengundian dilakukan satu kali untuk setiap giliran percakapan, sehingga satu percakapan dapat diperiksa sebagian di antara giliran-gilirannya. Permintaan di luar persentase sampel diteruskan tanpa pemeriksaan, bahkan ketika penanganan kegagalan diatur ke **Block the request**.
  </Step>

  <Step title="Aktifkan Enforce verdicts">
    Jika Anda ingin mengevaluasi putusan terhadap lalu lintas nyata tanpa memblokir siapa pun terlebih dahulu, atur **Mode** ke **Shadow mode** (langkah 6) sebelum mengaktifkan penegakan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Aktifkan **Enforce verdicts** agar setiap prompt yang diatur oleh Inference hooks harus menunggu putusan server keamanan AI Anda sebelum diproses Claude. Lalu konfirmasikan di dialog, yang menampilkan kembali pilihan penanganan kegagalan Anda. Perubahan ini memerlukan waktu sekitar satu menit untuk mencapai semua server Anthropic; permintaan yang sedang berjalan akan diselesaikan dengan pengaturan lama. Menonaktifkannya akan menghentikan pengiriman prompt ke server keamanan AI Anda, juga dalam waktu sekitar satu menit, dan konfigurasi Anda tetap tersimpan.
  </Step>
</Steps>

## Shadow mode

"Shadow mode" (mode bayangan) menjalankan hook Anda terhadap lalu lintas nyata tanpa memblokir apa pun. Server keamanan AI Anda menerima prompt yang diatur dan mengembalikan putusan persis seperti saat menegakkan putusan, tetapi tidak ada yang diblokir. Setiap permintaan tetap diteruskan ke model, bahkan ketika server Anda menolaknya atau tidak dapat dijangkau, dan pengguna akhir tidak melihat apa pun. Gunakan mode ini untuk menyempurnakan kebijakan Anda berdasarkan lalu lintas nyata organisasi Anda sebelum mulai menegakkan putusan.

Untuk menggunakan shadow mode, atur **Mode** ke **Shadow mode** di bawah **Failure handling**, lalu aktifkan **Enforce verdicts** agar prompt dikirim ke server keamanan AI Anda. Selama mode ini aktif, halaman pengaturan menampilkan lencana **Shadow mode — not blocking**. Untuk keluar dari shadow mode, atur **Mode** kembali ke **Allow the request** atau **Block the request**. Putusan akan kembali ditegakkan selama penegakan aktif.

## Pengecualian

Di bawah **Exclusions**, pilih peran yang anggotanya tidak dicakup oleh Inference hooks. Prompt dari anggota peran tersebut tidak pernah dikirim ke server keamanan AI Anda.

* Hanya peran kustom yang dibuat oleh organisasi Anda yang dapat dikecualikan; peran bawaan tidak tersedia sebagai pilihan.
* Pilih peran di pemilih peran, yang placeholder-nya bertuliskan **Select roles to exclude**.
* Kelola siapa yang memegang setiap peran dari halaman admin peran (**Manage roles**).
* Mengubah pengecualian memerlukan izin manajemen identitas.

Daftar ini kosong secara default. Jika tidak ada peran yang dikecualikan, setiap permintaan yang diatur akan diperiksa.

Pengecualian berlaku untuk sesi interaktif pengguna; lalu lintas yang diautentikasi dengan kredensial mesin selalu diperiksa. Perubahan pada daftar pengecualian dicatat dalam jejak audit.

## Pesan kustom untuk prompt yang diblokir

Di bawah **Custom blocked prompt message**, Anda dapat mengatur teks kustom hingga 500 karakter. Teks ini ditambahkan ke pesan kesalahan yang dilihat pengguna akhir ketika server keamanan AI Anda menolak permintaan, biasanya berisi siapa yang harus dihubungi atau di mana mengajukan pengecualian.

Pesan akhir terdiri dari `deny_reason` per permintaan dari server keamanan AI Anda (jika ada), satu baris kosong, lalu teks ini. Jika tidak ada teks kustom yang dikonfigurasi, pesan default bawaan akan mengarahkan pengguna untuk menghubungi administrator mereka. Anda juga dapat menonaktifkan pesan tambahan ini sepenuhnya sehingga pengguna hanya melihat `deny_reason`.

## Memantau server keamanan AI Anda

Area kesehatan endpoint di halaman pengaturan Inference hooks menampilkan:

* **Endpoint status:** Healthy, Tripped, atau Not enforcing. Sebelum endpoint disimpan, statusnya Not configured.
* **Failures per minute:** rata-rata kegagalan webhook selama dua menit terakhir.
* **Block rate:** penolakan sebagai proporsi dari putusan server keamanan AI Anda, ditampilkan selama persentase peluncuran bertahap di bawah 100.
* **Circuit breaker tripped:** kapan pemutus sirkuit terakhir kali terpicu, jika pernah.
* **Recent errors:** setiap entri hanya berisi stempel waktu, jenis kesalahan, dan alasan satu baris. Entri tidak pernah menyertakan konten permintaan atau URL endpoint Anda.

Panel ini bersifat upaya terbaik (best-effort). Jika Anthropic tidak dapat membaca penghitungnya, panel menampilkan nol kegagalan dan tidak ada kesalahan, alih-alih menampilkan kesalahannya sendiri. Jadi, panel yang tampak sehat belum tentu membuktikan bahwa server keamanan AI Anda sehat.

**Failures per minute** menghitung setiap kegagalan, termasuk kesalahan jaringan dan DNS yang tidak pernah memicu pemutus sirkuit. Karena itu, nilainya bisa tinggi sementara **Circuit breaker tripped** tetap kosong.

## Circuit breaker

Kegagalan webhook berkelanjutan yang disebabkan oleh server keamanan AI Anda akan memicu "circuit breaker" (pemutus sirkuit), yang menghentikan penegakan. Server Anda tidak lagi dihubungi, dan pilihan **Failure handling** Anda berlaku untuk setiap permintaan yang diperiksa. Jika **Block the request** dipilih, pengguna di organisasi Anda akan diblokir hingga pemutus sirkuit diatur ulang. Saat pemutus sirkuit terpicu, administrator juga diberi tahu melalui pusat notifikasi claude.ai.

Setiap pemicuan juga dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda sebagai aktivitas `inference_hooks_circuit_breaker_tripped`. Dengan begitu, tim keamanan atau vendor Anda dapat membuat peringatan atas pemicuan dari sistem pemantauan yang sudah mereka jalankan, seperti SIEM yang menyerap feed tersebut. Satu aktivitas dicatat per pemicuan, bukan per permintaan yang terdampak. Pencatatan ini memerlukan Compliance API yang diaktifkan untuk organisasi Anda; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

Untuk memulihkan, perbaiki server, lalu aktifkan kembali **Enforce verdicts** untuk mengatur ulang pemutus sirkuit.

Pemutus sirkuit juga dapat diatur ulang dengan sendirinya:

1. Mulai 10 menit setelah pemicuan, Anthropic memeriksa apakah server Anda telah pulih dengan mengirimkan permintaan uji di latar belakang, paling sering sekitar sekali per menit. Tidak ada permintaan pengguna yang terlibat.
2. Jika server Anda merespons dengan putusan yang valid, baik izinkan maupun tolak, pemutus sirkuit diatur ulang dan penegakan dilanjutkan.
3. Jika tidak, pemutus sirkuit tetap terpicu dan pemeriksaan terus berlanjut.

Pemulihan otomatis hanya berjalan selama pengaturan Inference hooks Anda tidak berubah sejak pemicuan. Jika Anda mengubah pengaturan Inference hooks apa pun setelah pemicuan, termasuk merotasi signing secret, pemeriksaan akan berhenti dan pemutus sirkuit tidak lagi diatur ulang dengan sendirinya. Dalam hal ini, aktifkan kembali **Enforce verdicts** setelah server Anda diperbaiki.

Pemulihan otomatis hanya berlaku untuk pemicuan. Jika Anda sendiri yang menonaktifkan **Enforce verdicts**, penegakan tetap nonaktif hingga Anda mengaktifkannya kembali.

## Merotasi signing secret Anda

Klik **Rotate secret** di bawah **Request signing** untuk mengganti signing secret Anda. Jika organisasi Anda belum memiliki rahasia, tombol yang sama bertuliskan **Generate secret** dan akan membuat rahasia pertama.

Rotasi berlaku seketika:

* Rahasia baru dibuat dan ditampilkan satu kali saja.
* Rahasia lama tidak dapat diambil kembali.
* Tidak ada permintaan yang pernah ditandatangani dengan kedua rahasia sekaligus, sehingga tidak ada periode tumpang tindih yang dapat diandalkan.

Permintaan yang ditandatangani dengan rahasia sebelumnya masih dapat tiba sesaat setelah rotasi. [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature) menjelaskan cara server keamanan AI Anda menangani peralihan ini.

## Jejak audit

Aktivitas Inference hooks dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda, meliputi:

* perubahan konfigurasi,
* penolakan,
* pemicuan pemutus sirkuit, dan
* permintaan yang diteruskan tanpa pemeriksaan berdasarkan pengaturan penanganan kegagalan Anda.

Selama pemutus sirkuit terpicu, tidak ada aktivitas Inference hooks per permintaan yang dicatat; aktivitas pemicuan menjadi catatan feed untuk periode tersebut. Catatan penolakan memuat pengidentifikasi yang memungkinkan Anda mencocokkan setiap penolakan dengan catatan terkait di sistem Anda sendiri.

## Menonaktifkan Inference hooks

Ada dua tingkat penonaktifan:

* **Enforce verdicts** dinonaktifkan, di halaman pengaturan Inference hooks: dalam waktu sekitar satu menit, prompt dari organisasi Anda berhenti dikirim ke server keamanan AI Anda. Permintaan yang sedang berjalan akan diselesaikan dengan pengaturan lama. Halaman pengaturan tetap tersedia, jadi gunakan opsi ini untuk menjeda penegakan selama Anda mengerjakan server keamanan AI Anda.
* **Allow for your organization** dinonaktifkan, di pengaturan **Data and privacy**: prompt tidak lagi diperiksa, dan pengaturan Inference hooks tidak tersedia hingga Anda mengaktifkannya kembali. Konfigurasi endpoint, header kustom, dan signing secret Anda tetap tersimpan. Mengaktifkannya kembali akan memaksa **Enforce verdicts** dalam keadaan nonaktif dan menghapus status pemutus sirkuit yang terpicu, jadi aktifkan kembali penegakan saat Anda siap.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengembangkan integrasi Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint">
    Bangun server keamanan AI: skema permintaan dan putusan, verifikasi tanda tangan, serta semantik operasional.
  </Card>

  <Card title="Ikhtisar Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks">
    Apa itu Inference hooks, cara kerja alur pertukaran putusan, dan apa saja yang dikirim ke server keamanan AI Anda.
  </Card>
</CardGroup>
