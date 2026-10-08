---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 9a5380942cd4dd687ce606f133a459cf56032afe5ac8ed25b84cd78219882e4e
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

Ada tiga status penegakan: **off** (**Enforce verdicts** nonaktif: server keamanan AI Anda tidak pernah dihubungi dan prompt tidak diperiksa), **shadow** (**Enforce verdicts** aktif dengan **Mode** diatur ke **Shadow mode**: server keamanan AI Anda menerima prompt dan mengembalikan putusan, dan tidak ada yang diblokir), dan **enforcing** (**Enforce verdicts** aktif dengan **Mode** diatur ke **Allow the request** atau **Block the request**: putusan tolak akan memblokir permintaan). Langkah-langkah berikut membawa konfigurasi baru dari off ke enforcing.

<Steps>
  <Step title="Izinkan Inference hooks untuk organisasi Anda">
    Buka claude.ai > **Organization settings** > **Data and privacy** dan temukan bagian **Inference hooks**. Aktifkan **Allow for your organization**.

    Mengaktifkan ini akan membuka halaman pengaturan Inference hooks dan selalu memaksa **Enforce verdicts** nonaktif, sehingga mengizinkan fitur ini tidak pernah memulai pemeriksaan dengan sendirinya: bahkan konfigurasi yang sebelumnya memiliki penegakan aktif tetap tidak diperiksa hingga Anda mengaktifkan kembali **Enforce verdicts** pada langkah terakhir.
  </Step>

  <Step title="Buka halaman pengaturan Inference hooks">
    Masih di **Data and privacy**, buka bagian **Inference hooks** untuk mencapai halaman pengaturan Inference hooks. Halaman ini berada di bawah Data and privacy alih-alih sebagai entri tersendiri di navigasi pengaturan, sehingga breadcrumb-nya berbunyi **Data and privacy / Inference hooks**. Hingga Anda menyimpan endpoint, halaman ini memperingatkan bahwa prompt belum diperiksa, dan **Enforce verdicts** tetap nonaktif dengan lencana **Requires endpoint**.
  </Step>

  <Step title="Konfigurasikan endpoint Anda">
    Klik **Configure** untuk membuka dialog **Set up endpoint** dan masukkan **Endpoint URL**: URL `https://` yang menerima permintaan putusan. Hanya URL `https://` yang diterima.

    Dialog ini tidak meminta hal lain pada tahap ini: header permintaan kustom ada di langkah 5, dan penanganan kegagalan di langkah 6. Klik **Next** untuk menyimpan. Setelah endpoint disimpan, tombol tersebut berbunyi **Edit**.
  </Step>

  <Step title="Simpan signing secret Anda">
    Penyimpanan pertama menghasilkan webhook signing secret Anda dan menampilkannya satu kali. Salin dan simpan dengan aman sebelum mengklik **Next**: secret tidak dapat diambil kembali nanti, hanya dapat [dirotasi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#rotate-your-signing-secret).

    Server keamanan AI Anda menggunakan secret ini untuk memverifikasi tanda tangan pada setiap permintaan yang diterimanya, termasuk uji koneksi pada langkah berikutnya. Untuk prosedur verifikasi, lihat [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature).
  </Step>

  <Step title="Tambahkan header permintaan dan uji koneksi">
    Mengklik **Next** pada dialog signing secret akan membuka kembali dialog endpoint, kini dengan dua kontrol tambahan:

    * **Custom request headers:** hingga 16 header statis yang dikirim bersama setiap permintaan putusan agar server keamanan AI Anda dapat mengautentikasi pemanggil. Nilai header disimpan dalam keadaan terenkripsi dan tidak pernah ditampilkan lagi; setelah disimpan, hanya nama header yang ditampilkan. Karena nilainya hanya dapat ditulis, menyimpan perubahan apa pun pada header mengharuskan Anda memasukkan ulang setiap nilai. Mengubah URL endpoint akan menghapus semua nilai header yang tersimpan sehingga kredensial Anda tidak pernah dikirim ke tujuan baru; masukkan ulang nilai tersebut setelah perubahan URL. Nama header harus menggunakan karakter token HTTP standar dengan `-` alih-alih `_`, dan tidak boleh bertabrakan dengan nama yang dicadangkan (header pembingkaian permintaan seperti `Content-*` dan `Host`, header proxy dan cookie, header alamat klien seperti `X-Forwarded-*`, header tanda tangan `webhook-*`, dan prefiks `X-Anthropic-*`). Nilai harus berupa ASCII yang dapat dicetak.
    * **Test connection:** Claude mengirimkan prompt uji sintetis ke URL dan header yang saat ini ada di formulir, bukan nilai yang tersimpan, jadi masukkan ulang nilai header yang tersimpan sebelum menguji. Jika berhasil, hasilnya melaporkan apakah server keamanan AI Anda mengembalikan putusan izinkan atau tolak untuk prompt uji tersebut, yang akan mengungkap default tolak-semua sebelum Anda mulai menegakkan.

    Klik **Save** untuk menyimpan header yang Anda masukkan.

    Hasil kegagalan yang umum:

    | Hasil                      | Yang perlu diperiksa                                                                                                                                               |
    | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | URL ditolak                | URL gagal dalam pemeriksaan struktural. Gunakan URL `https://` pada port 443.                                                                                      |
    | IP privat atau internal    | Host URL adalah alamat IP privat atau internal, alamat IPv6, atau `localhost`. Gunakan host yang dapat dirutekan secara publik.                                    |
    | Timeout                    | Server keamanan AI tidak mengembalikan putusan dalam batas waktu.                                                                                                  |
    | Kesalahan transport        | Resolusi DNS, TLS handshake, atau koneksi gagal, atau hostname di-resolve ke alamat privat.                                                                        |
    | Status non-200             | Server keamanan AI merespons dengan status selain 200. Putusan harus dikembalikan sebagai HTTP 200; pengalihan tidak diikuti dan dihitung sebagai kegagalan.       |
    | Respons tidak dapat diurai | Server keamanan AI merespons, tetapi body-nya bukan putusan yang valid.                                                                                            |
    | Signing secret diperlukan  | Organisasi Anda tidak memiliki signing secret, sehingga uji akan dikirim tanpa tanda tangan. Klik **Generate secret** di bawah **Request signing**, lalu uji lagi. |
  </Step>

  <Step title="Pilih penanganan kegagalan dan batas waktu">
    Di bawah **Failure handling**, atur **Mode** untuk memilih apa yang terjadi saat server keamanan AI tidak dapat dijangkau atau putusan melewati batas waktu:

    * **Block the request:** hentikan inferensi ketika server keamanan AI Anda tidak dapat memberikan putusan ("fail closed", gagal tertutup).
    * **Allow the request:** biarkan permintaan diteruskan ke model tanpa pemeriksaan ("fail open", gagal terbuka).

    Opsi ketiga pada dropdown, **Shadow mode**, adalah alat peluncuran, bukan kebijakan kegagalan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Kemudian atur **Prompt verdict timeout (ms)**: 1 hingga 10.000ms, dengan default 5.000ms. Anggaran waktu ini mencakup seluruh pertukaran, dan putusan yang lebih lambat dihitung sebagai server yang tidak dapat dijangkau, jadi atur nilai terendah yang dapat dipenuhi server Anda secara andal.

    Perubahan di bagian ini tersimpan saat Anda membuatnya. Pada penyimpanan pertama, default-nya adalah **Allow the request** dan 5.000ms.
  </Step>

  <Step title="Pilih persentase peluncuran">
    Di bawah **Rollout**, atur **Requests inspected (%)** untuk menjalankan pemeriksaan pada sebagian persentase permintaan selama Anda menyiapkan server keamanan AI Anda. Nilainya berkisar dari 0 hingga 100: 100 memeriksa semuanya, dan 0 menonaktifkan pemeriksaan.

    Setiap permintaan diundi satu kali untuk seluruh giliran percakapannya, sehingga satu percakapan dapat diperiksa sebagian di berbagai giliran. Permintaan di luar persentase sampel diteruskan tanpa pemeriksaan, bahkan ketika penanganan kegagalan diatur ke **Block the request**.
  </Step>

  <Step title="Aktifkan Enforce verdicts">
    Untuk mengevaluasi putusan terhadap lalu lintas langsung tanpa memblokir siapa pun pada awalnya, atur **Mode** ke **Shadow mode** (langkah 6) sebelum mengaktifkan penegakan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Aktifkan **Enforce verdicts** untuk membuat Claude bergantung pada putusan server keamanan AI Anda untuk setiap prompt yang diatur, lalu konfirmasikan di dialog, yang menyatakan kembali pilihan penanganan kegagalan Anda. Tunggu sekitar satu menit agar perubahan mencapai setiap server Anthropic; permintaan yang sedang berjalan diselesaikan dengan pengaturan lama. Menonaktifkannya akan menghentikan pengiriman prompt ke server keamanan AI Anda, juga dalam waktu sekitar satu menit; konfigurasi Anda tetap disimpan.

    **Validate tool calls**, di bawah **Enforce verdicts**, juga mengirimkan panggilan alat dalam setiap respons Claude ke server keamanan AI Anda dan menunggu putusannya sebelum panggilan alat tersebut dijalankan; lihat [Frame tool call](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#the-tool-call-frame). Opsi ini aktif secara default pada konfigurasi baru. Opsi ini tidak berpengaruh selama **Enforce verdicts** nonaktif, dan perubahan padanya memerlukan sekitar satu menit untuk mencapai setiap server Anthropic, sama seperti **Enforce verdicts**.
  </Step>
</Steps>

## Shadow mode

Shadow mode menjalankan hook Anda terhadap lalu lintas langsung tanpa memblokir apa pun. Server keamanan AI Anda menerima prompt yang diatur dan mengembalikan putusan persis seperti saat menegakkan, tetapi tidak ada yang diblokir: setiap permintaan diteruskan ke model, bahkan ketika server Anda menolaknya atau tidak dapat dijangkau, dan pengguna akhir tidak melihat apa pun. Gunakan mode ini untuk menyetel kebijakan Anda terhadap lalu lintas nyata organisasi Anda sebelum mulai menegakkan. Dengan **Validate tool calls** aktif, server Anda juga menerima frame tool call dalam shadow mode, dan tidak ada panggilan alat yang diblokir.

Untuk menggunakan shadow mode, atur **Mode** ke **Shadow mode** di bawah **Failure handling**, lalu aktifkan **Enforce verdicts** agar prompt mengalir ke server keamanan AI Anda. Selama aktif, halaman pengaturan menampilkan lencana **Shadow mode — not blocking**. Untuk keluar dari shadow mode, atur **Mode** kembali ke **Allow the request** atau **Block the request**; putusan ditegakkan kembali setelah penegakan aktif.

## Pengecualian

Di bawah **Exclusions**, pilih peran yang anggotanya tidak dicakup oleh Inference hooks: prompt mereka tidak pernah dikirim ke server keamanan AI Anda. Hanya peran kustom yang dibuat organisasi Anda yang dapat dikecualikan; peran bawaan tidak ditawarkan. Pilih peran tersebut di pemilih peran, yang placeholder-nya berbunyi **Select roles to exclude**, dan kelola siapa yang memegang setiap peran dari halaman admin peran (**Manage roles**); mengubah pengecualian memerlukan izin manajemen identitas. Daftar ini kosong secara default, dan tanpa peran yang dikecualikan, setiap permintaan yang diatur akan diperiksa.

Pengecualian berlaku untuk sesi interaktif pengguna. Perubahan pada daftar pengecualian dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda sebagai perubahan izin peran (`rbac_role_permission_added` dan `rbac_role_permission_removed`).

## Pesan kustom untuk prompt yang diblokir

Di bawah **Custom blocked prompt message**, Anda dapat mengatur teks kustom hingga 500 karakter. Teks ini ditambahkan ke pesan kesalahan yang dilihat pengguna akhir ketika server keamanan AI Anda menolak permintaan, biasanya berisi siapa yang harus dihubungi atau di mana mengajukan pengecualian.

Pesan akhir terdiri dari `deny_reason` per permintaan dari server keamanan AI Anda (jika ada), satu baris kosong, lalu teks ini. Jika tidak ada teks kustom yang dikonfigurasi, pesan default bawaan akan mengarahkan pengguna untuk menghubungi administrator mereka. Anda juga dapat menonaktifkan pesan tambahan ini sepenuhnya sehingga pengguna hanya melihat `deny_reason`.

## Memantau server keamanan AI Anda

Area kesehatan endpoint pada halaman pengaturan Inference hooks menampilkan:

* **Endpoint status:** Healthy, Tripped, Not enforcing, atau Not configured sebelum endpoint disimpan.
* **Failures per minute:** kegagalan webhook selama dua menit terakhir, dirata-ratakan.
* **Block rate:** penolakan sebagai proporsi dari putusan server keamanan AI Anda, ditampilkan selama persentase peluncuran di bawah 100.
* **Circuit breaker tripped:** kapan breaker terakhir kali terpicu, jika pernah.
* **Recent errors:** setiap entri menunjukkan kapan kegagalan terjadi, jenis kesalahan, dan kategori. Kategorinya adalah `webhook_error` untuk masalah pada endpoint Anda atau koneksi ke endpoint tersebut, atau `relay_error` untuk kegagalan di dalam sistem Anthropic. Entri tidak pernah menyertakan konten permintaan atau URL endpoint Anda. Daftar ini menyimpan 10 kegagalan terbaru dan dikosongkan satu jam setelah kegagalan terakhir.

Jenis kesalahan di **Recent errors** berarti:

| Kesalahan yang ditampilkan                           | Artinya                                                                                                                                                                                                                                                              | Dihitung untuk circuit breaker |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `DlpWebhookTimeoutError` · `webhook_error`           | Server keamanan AI Anda tidak mengembalikan putusan dalam **Prompt verdict timeout (ms)** yang Anda atur.                                                                                                                                                            | Ya                             |
| `DlpWebhookStatusError` · `webhook_error`            | Server keamanan AI Anda menjawab dengan status HTTP selain 200, seperti pengalihan.                                                                                                                                                                                  | Ya                             |
| `DlpWebhookResponseError` · `webhook_error`          | Server keamanan AI Anda menjawab 200, tetapi body-nya bukan putusan yang valid atau lebih besar dari 64 KiB.                                                                                                                                                         | Ya                             |
| `DlpWebhookTransportError` · `webhook_error`         | Koneksi gagal atau terputus sebelum jawaban lengkap tiba: misalnya, hostname tidak dapat di-resolve atau di-resolve ke alamat privat, koneksi ditolak atau di-reset, atau TLS handshake gagal. Masalah jaringan di sisi Anthropic juga dapat muncul dengan cara ini. | Tidak                          |
| `DlpWebhookDisallowedAddressError` · `webhook_error` | Host URL endpoint adalah alamat IP privat atau internal, alamat IPv6, atau `localhost`. Hostname yang di-resolve ke alamat seperti itu ditampilkan sebagai kesalahan transport.                                                                                      | Ya                             |
| `DlpWebhookBlockedError` · `webhook_error`           | URL endpoint bukan URL `https://` pada port 443, atau tidak dapat diurai, sehingga tidak ada permintaan yang dikirim.                                                                                                                                                | Tidak                          |
| `DlpWebhookRelayError` · `relay_error`               | Kegagalan terjadi di dalam sistem Anthropic, dan server keamanan AI Anda biasanya tidak dihubungi.                                                                                                                                                                   | Tidak                          |

Dalam shadow mode, tidak ada kesalahan yang dihitung untuk circuit breaker.

Panel ini bersifat upaya terbaik (best-effort): jika Anthropic tidak dapat membaca penghitung, panel menampilkan nol kegagalan dan tidak ada kesalahan alih-alih menampilkan kesalahannya sendiri, sehingga panel yang tampak sehat bukanlah bukti tersendiri bahwa server keamanan AI Anda sehat. **Failures per minute** menghitung setiap kegagalan, termasuk kesalahan jaringan dan DNS yang tidak pernah memicu circuit breaker, sehingga nilainya bisa tinggi sementara **Circuit breaker tripped** tetap kosong.

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

Aktivitas Inference hooks dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda: perubahan konfigurasi, penolakan, pemicuan circuit breaker, dan permintaan yang diteruskan tanpa pemeriksaan karena tidak ada putusan yang dapat diperoleh. Jenis terakhir tersebut hanya dicatat selama **Enforce verdicts** aktif dan **Mode** adalah **Allow the request**. Alasannya adalah `endpoint_timeout`, `endpoint_error` untuk masalah lain apa pun saat memanggil server keamanan AI Anda, atau `internal_error` untuk kegagalan di sisi Anthropic. Di bawah **Block the request** atau **Shadow mode**, permintaan yang gagal tidak dicatat secara individual. Pemulihan otomatis circuit breaker tidak dicatat dalam mode apa pun. Selama circuit breaker terpicu, tidak ada aktivitas Inference hooks per permintaan yang dicatat; aktivitas pemicuan adalah catatan feed untuk rentang waktu tersebut. Catatan penolakan membawa pengidentifikasi yang memungkinkan Anda menggabungkan setiap penolakan dengan catatan yang sesuai di sistem Anda sendiri.

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
