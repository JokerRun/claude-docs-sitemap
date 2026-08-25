---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 0916df2e7da69da202cae0cafc7b47e690ba40ea757b6305ed454efd4250aadc
---

---
title: Mengonfigurasi Inference hooks
url: https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration
description: Izinkan Inference hooks untuk organisasi Claude Enterprise Anda, hubungkan server keamanan AI Anda, dan kendalikan penegakan, penanganan kegagalan, serta peluncuran bertahap.
---

<Note>
  Inference hooks masih dalam versi beta dan tersedia untuk organisasi Claude Enterprise. Mengonfigurasinya memerlukan izin `organization:manage`, yang dimiliki oleh peran bawaan Admin, Owner, dan Primary owner, serta peran kustom apa pun yang diberi izin tersebut.
</Note>

Inference hooks mengirimkan prompt dari organisasi Anda ke server keamanan AI yang Anda pilih, dan menahan setiap permintaan untuk menunggu verdict (putusan) izinkan atau tolak sebelum Claude memprosesnya. Halaman ini memandu Anda mengaktifkan fitur ini, menghubungkan server Anda, dan mengendalikan penegakan. Untuk mengetahui apa itu Inference hooks dan kapan menggunakannya, lihat [ikhtisar Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks). Untuk membangun server keamanan AI itu sendiri, lihat [Mengembangkan integrasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

## Sebelum Anda memulai

Anda memerlukan:

* Izin `organization:manage` di claude.ai. Peran bawaan **Admin**, **Owner**, dan **Primary owner** memilikinya, begitu pula peran kustom apa pun yang telah diberi izin tersebut.
* Endpoint HTTPS server keamanan AI yang menerima permintaan verdict: URL `https://` pada port 443, pada host yang dapat dirutekan secara publik, dan dapat dijangkau tanpa pengalihan (redirect). Host reverse-tunnel (ngrok dan layanan tunnel serupa) tidak didukung: kebijakan jaringan Anthropic memblokirnya. Jangan menguji melalui tunnel; host server Anda pada domain yang Anda kendalikan. Untuk [persyaratan hosting](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#receive-a-request) selengkapnya, serta untuk membangun server dan memverifikasi permintaan yang ditandatangani, lihat [Mengembangkan integrasi Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint).

## Menyiapkan Inference hooks

Ada tiga status penegakan: **off** (**Enforce verdicts** nonaktif: server keamanan AI Anda tidak pernah dihubungi dan prompt tidak diperiksa), **shadow** (**Enforce verdicts** aktif dengan **Mode** diatur ke **Shadow mode**: server keamanan AI Anda menerima prompt dan mengembalikan verdict, dan tidak ada yang diblokir), dan **enforcing** (**Enforce verdicts** aktif dengan **Mode** diatur ke **Allow the request** atau **Block the request**: verdict tolak akan memblokir permintaan). Langkah-langkah berikut membawa konfigurasi baru dari off ke enforcing.

<Steps>
  <Step title="Izinkan Inference hooks untuk organisasi Anda">
    Buka claude.ai > **Organization settings** > **Data and privacy** dan temukan bagian **Inference hooks**. Aktifkan **Allow for your organization**.

    Mengaktifkan ini akan membuka halaman pengaturan Inference hooks dan selalu memaksa **Enforce verdicts** menjadi nonaktif, sehingga mengizinkan fitur ini tidak pernah memulai pemeriksaan dengan sendirinya: bahkan konfigurasi yang sebelumnya memiliki penegakan aktif tetap tidak diperiksa sampai Anda mengaktifkan kembali **Enforce verdicts** pada langkah terakhir.
  </Step>

  <Step title="Buka halaman pengaturan Inference hooks">
    Masih di **Data and privacy**, buka bagian **Inference hooks** untuk menuju halaman pengaturan Inference hooks. Halaman ini berada di bawah Data and privacy, bukan sebagai entri tersendiri di navigasi pengaturan, sehingga breadcrumb-nya tertulis **Data and privacy / Inference hooks**. Sampai Anda menyimpan sebuah endpoint, halaman ini memperingatkan bahwa prompt belum diperiksa, dan **Enforce verdicts** tetap nonaktif dengan lencana **Requires endpoint**.
  </Step>

  <Step title="Konfigurasikan endpoint Anda">
    Klik **Configure** untuk membuka dialog **Configure endpoint** dan isi:

    * **Endpoint URL:** URL `https://` yang menerima permintaan verdict. Hanya URL `https://` yang diterima.
    * **Custom request headers:** hingga 16 header statis yang dikirim bersama setiap permintaan verdict agar server keamanan AI Anda dapat mengautentikasi pemanggil. Nilai header disimpan terenkripsi dan tidak pernah ditampilkan lagi; setelah disimpan, hanya nama header yang ditampilkan. Karena nilainya bersifat write-only, menyimpan perubahan apa pun pada header mengharuskan Anda memasukkan ulang setiap nilai. Mengubah URL endpoint akan menghapus semua nilai header yang tersimpan sehingga kredensial Anda tidak pernah dikirim ke tujuan baru; masukkan kembali setelah perubahan URL. Nama header harus menggunakan karakter token HTTP standar dengan `-` alih-alih `_`, dan tidak boleh berbenturan dengan nama yang dicadangkan (header pembingkaian permintaan seperti `Content-*` dan `Host`, header proxy dan cookie, header alamat klien seperti `X-Forwarded-*`, header tanda tangan `webhook-*`, dan prefiks `X-Anthropic-*`). Nilai harus berupa ASCII yang dapat dicetak.

    Dialog ini hanya mencakup kedua bidang tersebut ditambah **Test connection**; dialog ini tidak menanyakan penanganan kegagalan, yang Anda pilih pada langkah 6. Setelah sebuah endpoint disimpan, tombolnya bertuliskan **Edit**.
  </Step>

  <Step title="Uji koneksi">
    Klik **Test connection**. Claude mengirimkan prompt uji sintetis ke URL dan header yang saat ini ada di formulir, bukan nilai yang tersimpan, jadi masukkan ulang nilai header yang tersimpan sebelum menguji. Jika berhasil, hasilnya melaporkan apakah server keamanan AI Anda mengembalikan verdict izinkan atau tolak untuk prompt uji tersebut, yang akan mengungkap adanya default tolak-semua sebelum Anda mulai menegakkan.

    Hasil kegagalan yang umum:

    | Hasil                      | Yang perlu diperiksa                                                                                                                                         |
    | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | URL ditolak                | URL gagal dalam pemeriksaan struktural. Gunakan URL `https://` pada port 443.                                                                                |
    | IP privat atau internal    | Host diresolusi ke alamat privat atau internal. Gunakan host yang dapat dirutekan secara publik.                                                             |
    | Timeout                    | Server keamanan AI tidak mengembalikan verdict dalam batas waktu.                                                                                            |
    | Kesalahan transport        | Resolusi DNS, handshake TLS, atau koneksi gagal.                                                                                                             |
    | Status bukan 200           | Server keamanan AI merespons dengan status selain 200. Verdict harus dikembalikan sebagai HTTP 200; pengalihan tidak diikuti dan dihitung sebagai kegagalan. |
    | Respons tidak dapat diurai | Server keamanan AI merespons, tetapi body-nya bukan verdict yang valid.                                                                                      |
  </Step>

  <Step title="Simpan dan amankan signing secret Anda">
    Simpan konfigurasi endpoint. Penyimpanan pertama menghasilkan webhook signing secret Anda dan menampilkannya satu kali. Salin dan simpan dengan aman sebelum menutup dialog: secret ini tidak dapat diambil kembali nanti, hanya dapat [dirotasi](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#rotate-your-signing-secret).

    Server keamanan AI Anda menggunakan secret ini untuk memverifikasi tanda tangan pada setiap permintaan yang diterimanya. Untuk prosedur verifikasi, lihat [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature).
  </Step>

  <Step title="Pilih penanganan kegagalan dan batas waktu">
    Di bawah **Failure handling**, atur **Mode** untuk memilih apa yang terjadi ketika server keamanan AI tidak dapat dijangkau atau verdict melewati batas waktu:

    * **Block the request:** hentikan inferensi ketika server keamanan AI Anda tidak dapat memberikan verdict (fail closed).
    * **Allow the request:** biarkan permintaan dilanjutkan ke model tanpa pemeriksaan (fail open).

    Opsi ketiga pada dropdown, **Shadow mode**, adalah alat peluncuran bertahap, bukan kebijakan kegagalan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Kemudian atur **Prompt verdict timeout (ms)**: 1 hingga 10.000 ms, dengan default 5.000 ms. Anggaran waktu ini mencakup seluruh pertukaran, dan verdict yang lebih lambat dihitung sebagai server yang tidak dapat dijangkau, jadi atur nilai terendah yang dapat dipenuhi server Anda secara andal.

    Perubahan di bagian ini disimpan saat Anda membuatnya. Pada penyimpanan pertama, default-nya adalah **Allow the request** dan 5.000 ms.
  </Step>

  <Step title="Pilih persentase peluncuran">
    Di bawah **Rollout**, atur **Requests inspected (%)** untuk menjalankan pemeriksaan pada sebagian persentase permintaan selagi Anda menyiapkan server keamanan AI Anda. Nilainya berkisar dari 0 hingga 100: 100 memeriksa semuanya, dan 0 menonaktifkan pemeriksaan.

    Setiap permintaan diundi satu kali untuk seluruh giliran percakapannya, sehingga satu percakapan dapat diperiksa sebagian di berbagai giliran. Permintaan di luar persentase sampel dilanjutkan tanpa pemeriksaan, bahkan ketika penanganan kegagalan diatur ke **Block the request**.
  </Step>

  <Step title="Aktifkan Enforce verdicts">
    Untuk mengevaluasi verdict terhadap lalu lintas langsung tanpa memblokir siapa pun pada awalnya, atur **Mode** ke **Shadow mode** (langkah 6) sebelum mengaktifkan penegakan; lihat [Shadow mode](https://platform.claude.com/docs/id/manage-claude/inference-hooks-configuration#shadow-mode).

    Aktifkan **Enforce verdicts** untuk menjadikan verdict server keamanan AI Anda sebagai gerbang bagi Claude untuk setiap prompt yang diatur, lalu konfirmasikan di dialog, yang menyatakan ulang pilihan penanganan kegagalan Anda. Beri waktu sekitar satu menit agar perubahan mencapai setiap server Anthropic; permintaan yang sedang berjalan diselesaikan dengan pengaturan lama. Menonaktifkannya menghentikan pengiriman prompt ke server keamanan AI Anda, juga dalam waktu sekitar satu menit; konfigurasi Anda tetap disimpan.
  </Step>
</Steps>

## Shadow mode

Shadow mode menjalankan hook Anda terhadap lalu lintas langsung tanpa memblokir apa pun. Server keamanan AI Anda menerima prompt yang diatur dan mengembalikan verdict persis seperti saat menegakkan, tetapi tidak ada yang diblokir: setiap permintaan dilanjutkan ke model, bahkan ketika server Anda menolaknya atau tidak dapat dijangkau, dan pengguna akhir tidak melihat apa pun. Gunakan mode ini untuk menyetel kebijakan Anda terhadap lalu lintas nyata organisasi Anda sebelum mulai menegakkan.

Untuk menggunakan shadow mode, atur **Mode** ke **Shadow mode** di bawah **Failure handling**, lalu aktifkan **Enforce verdicts** agar prompt mengalir ke server keamanan AI Anda. Selama mode ini aktif, halaman pengaturan menampilkan lencana **Shadow mode — not blocking**. Untuk keluar dari shadow mode, atur **Mode** kembali ke **Allow the request** atau **Block the request**; verdict ditegakkan kembali setelah penegakan aktif.

## Pengecualian

Di bawah **Exclusions**, pilih peran yang anggotanya tidak dicakup oleh Inference hooks: prompt mereka tidak pernah dikirim ke server keamanan AI Anda. Hanya peran kustom yang dibuat organisasi Anda yang dapat dikecualikan; peran bawaan tidak ditawarkan. Pilih peran tersebut di pemilih peran, yang placeholder-nya bertuliskan **Select roles to exclude**, dan kelola siapa yang memegang setiap peran dari halaman admin peran (**Manage roles**); mengubah pengecualian memerlukan izin manajemen identitas. Daftar ini kosong secara default, dan tanpa peran yang dikecualikan, setiap permintaan yang diatur akan diperiksa.

Pengecualian berlaku untuk sesi interaktif pengguna; lalu lintas yang diautentikasi oleh kredensial mesin selalu diperiksa. Jika Claude tidak dapat menentukan keanggotaan peran pemohon, permintaan gagal secara fail closed dengan kesalahan yang dapat dicoba ulang, alih-alih dilanjutkan tanpa pemeriksaan. Perubahan pada daftar pengecualian dicatat dalam jejak audit.

## Pesan prompt terblokir kustom

Di bawah **Custom blocked prompt message**, atur teks kustom hingga 500 karakter yang ditambahkan ke pesan kesalahan yang dilihat pengguna akhir ketika server keamanan AI Anda menolak permintaan (biasanya siapa yang harus dihubungi atau di mana meminta pengecualian). Pesan akhirnya adalah `deny_reason` per permintaan dari server keamanan AI Anda (jika ada), satu baris kosong, lalu teks ini. Tanpa teks kustom yang dikonfigurasi, default bawaan mengarahkan pengguna untuk menghubungi administrator mereka; Anda juga dapat menonaktifkan pesan tambahan ini sepenuhnya sehingga pengguna hanya melihat `deny_reason`.

## Memantau server keamanan AI Anda

Area kesehatan endpoint pada halaman pengaturan Inference hooks menampilkan:

* **Endpoint status:** Healthy, Tripped, Not enforcing, atau Not configured sebelum sebuah endpoint disimpan.
* **Failures per minute:** kegagalan webhook selama dua menit terakhir, dirata-ratakan.
* **Block rate:** penolakan sebagai bagian dari verdict server keamanan AI Anda, ditampilkan selama persentase peluncuran di bawah 100.
* **Circuit breaker tripped:** kapan circuit breaker terakhir kali terpicu, jika pernah.
* **Recent errors:** setiap entri diringkas menjadi stempel waktu, jenis kesalahan, dan alasan satu baris. Entri tidak pernah menyertakan konten permintaan atau URL endpoint Anda.

Panel ini bersifat best-effort: jika Anthropic tidak dapat membaca penghitungnya, panel menampilkan nol kegagalan dan tanpa kesalahan alih-alih menampilkan kesalahannya sendiri, sehingga panel yang tampak sehat bukan dengan sendirinya bukti bahwa server keamanan AI Anda sehat. **Failures per minute** menghitung setiap kegagalan, termasuk kesalahan jaringan dan DNS yang tidak pernah memicu circuit breaker, sehingga nilainya bisa tinggi sementara **Circuit breaker tripped** tetap kosong.

## Circuit breaker

Kegagalan webhook berkelanjutan yang disebabkan oleh server keamanan AI Anda akan memicu circuit breaker, yang menghentikan penegakan: server Anda tidak lagi dihubungi, dan pilihan **Failure handling** Anda berlaku untuk setiap permintaan yang diperiksa. Dengan **Block the request** dipilih, pengguna di organisasi Anda diblokir sampai Anda bertindak. Ketika circuit breaker terpicu, administrator juga diberi tahu di pusat notifikasi claude.ai.

Setiap pemicuan juga dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda sebagai aktivitas `inference_hooks_circuit_breaker_tripped`, sehingga tim keamanan atau vendor Anda dapat membuat peringatan atas pemicuan dari pemantauan yang sudah mereka jalankan, seperti SIEM yang menyerap feed tersebut. Satu aktivitas dicatat per pemicuan, bukan satu per permintaan yang terdampak. Pencatatan memerlukan Compliance API diaktifkan untuk organisasi Anda; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

Untuk memulihkan, perbaiki server, lalu aktifkan kembali **Enforce verdicts** untuk mereset circuit breaker.

## Merotasi signing secret Anda

Klik **Rotate secret** di bawah **Request signing** untuk mengganti signing secret Anda. Rotasi adalah peralihan seketika: secret baru dihasilkan dan ditampilkan satu kali, secret lama tidak dapat diambil kembali, dan tidak ada permintaan yang pernah ditandatangani dengan kedua secret, sehingga tidak ada periode tumpang tindih yang dapat diandalkan.

Permintaan yang ditandatangani dengan secret sebelumnya masih dapat tiba sesaat setelah rotasi; [Memverifikasi tanda tangan](https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint#verify-the-signature) membahas bagaimana server keamanan AI Anda sebaiknya menangani peralihan tersebut.

## Jejak audit

Aktivitas Inference hooks dicatat di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda: perubahan konfigurasi, penolakan, pemicuan circuit breaker, dan permintaan yang berlanjut tanpa pemeriksaan berdasarkan pengaturan penanganan kegagalan Anda. Selama circuit breaker terpicu, tidak ada aktivitas Inference hooks per permintaan yang dicatat; aktivitas pemicuan adalah catatan feed untuk jendela waktu tersebut. Catatan penolakan membawa pengidentifikasi yang memungkinkan Anda menggabungkan setiap penolakan dengan catatan yang sesuai di sistem Anda sendiri.

## Menonaktifkan Inference hooks

Ada dua tingkat nonaktif:

* **Enforce verdicts** nonaktif, di halaman pengaturan Inference hooks: dalam waktu sekitar satu menit, prompt dari organisasi Anda berhenti dikirim ke server keamanan AI Anda; permintaan yang sedang berjalan diselesaikan dengan pengaturan lama. Halaman pengaturan tetap tersedia, jadi gunakan ini untuk menjeda penegakan selagi Anda mengerjakan server keamanan AI Anda.
* **Allow for your organization** nonaktif, di pengaturan **Data and privacy**: prompt tidak lagi diperiksa, dan pengaturan Inference hooks menjadi tidak tersedia sampai Anda mengaktifkannya kembali. Konfigurasi endpoint, header kustom, dan signing secret Anda tetap disimpan dalam kedua kasus; mengaktifkannya kembali memaksa **Enforce verdicts** menjadi nonaktif, jadi aktifkan penegakan lagi ketika Anda siap.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengembangkan integrasi Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks-endpoint">
    Bangun server keamanan AI: skema permintaan dan verdict, verifikasi tanda tangan, dan semantik operasional.
  </Card>

  <Card title="Ikhtisar Inference hooks" href="https://platform.claude.com/docs/id/manage-claude/inference-hooks">
    Apa itu Inference hooks, bagaimana perjalanan bolak-balik verdict bekerja, dan apa yang dikirim ke server keamanan AI Anda.
  </Card>
</CardGroup>
