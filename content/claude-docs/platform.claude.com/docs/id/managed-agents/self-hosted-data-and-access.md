---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: f6c33b852a7d1031483fb9b06b1fb529d37c9fa68b34f63e1da4f553def083bb
---

---
title: Data dan akses dalam Claude Managed Agents yang di-host sendiri
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access
description: Apa yang dikirim oleh Claude Managed Agents yang di-host sendiri ke luar jaringan Anda, ke mana log, trace, dan metriknya dikirim, berapa lama data disimpan, siapa yang dapat menjangkau server, dan cara memisahkan tenant.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Dengan [Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted), Anda menjalankan server, database-nya, dan sandbox tempat worker menjalankan alat shell dan file milik agen. Halaman ini menjawab pertanyaan-pertanyaan dalam tinjauan keamanan. Penyedia inferensi server adalah layanan yang menjawab panggilan modelnya. Server terhubung ke Anthropic hanya ketika penyedia tersebut adalah Claude API. Anthropic tidak memiliki akses jarak jauh ke server atau lognya.

## Apa yang keluar dari jaringan Anda

### Setiap koneksi yang dibuat server

Server hanya terhubung ke tujuan-tujuan berikut:

* Penyedia inferensi Anda
* Database server
* Layanan-layanan yang menerbitkan kredensial server untuk panggilan model, jika server memperoleh kredensial tersebut dari suatu layanan
* Layanan penyedia cloud untuk mencantumkan model, jika penyedia inferensi Anda mencantumkan modelnya pada layanan terpisah
* Server MCP yang Anda izinkan
* Host Git yang Anda izinkan, untuk repositori yang digunakan sesi
* Collector OpenTelemetry, jika Anda mengonfigurasinya
* Penyedia identitas yang Anda cantumkan untuk single sign-on, jika Anda mengonfigurasinya
* Pengelola rahasia atau layanan manajemen kunci, jika Anda mengonfigurasinya
* Layanan yang menerbitkan kredensial server untuk pengelola rahasia atau layanan manajemen kunci tersebut
* Layanan lain apa pun yang Anda konfigurasi untuk dipanggil oleh server

Penyedia inferensi default adalah Claude API. Jika Anda mengonfigurasi penyedia inferensi lain, panggilan model dikirim ke sana sebagai gantinya. Server terhubung ke Anthropic hanya ketika Claude API menjadi penyedia inferensinya.

Jika penyedia inferensi menyediakan alat pencarian web dan pengambilan web, penyedia tersebut yang menjalankannya. Server tidak membuat koneksi sendiri untuk alat-alat tersebut. Alat-alat tersebut nonaktif sampai Anda mengaktifkannya di pengaturan server.

Untuk memeriksa lalu lintas server, bandingkan log proxy egress atau firewall Anda dengan daftar ini. Permintaan server ke Claude API membawa header `User-Agent`. Lihat [Field yang menyebutkan perangkat lunak server](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#fields-that-name-the-server-software).

### Apa yang dapat dijangkau worker

Daftar tujuan ini hanya mencakup server. [Egress gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#environment-variable-credentials), jika Anda menjalankannya, terhubung ke host yang Anda cantumkan untuknya, dan mengirimkan kepada host tersebut nilai kredensial yang Anda simpan untuknya. Worker terpisah. Worker memiliki akses jaringan apa pun yang Anda izinkan untuk container, VM, atau sandbox lain tempat worker berjalan. Setiap perintah yang dijalankan agen melalui worker memiliki akses jaringan yang sama.

### Apa yang dikirim server ke penyedia inferensinya

Setiap panggilan model membawa percakapan sejauh ini, termasuk prompt, input alat, dan hasil alat.

Ketika Claude API menjadi penyedia inferensi, setiap panggilan model juga membawa hingga tiga header. Header tersebut berisi ID yang dihasilkan oleh server Anda:

| Header                                    | Isinya                                        |
| ----------------------------------------- | --------------------------------------------- |
| `anthropic-managed-agents-session-id`     | ID sesi yang dilayani oleh panggilan tersebut |
| `anthropic-managed-agents-agent-id`       | ID agen dari sesi tersebut                    |
| `anthropic-managed-agents-environment-id` | ID environment dari sesi tersebut             |

Sebuah ID tidak berisi nama maupun konten, tetapi ID tersebut mengodekan waktu saat server Anda membuatnya. Dengan header ini, Anthropic dapat mengatribusikan penggunaan ke sesi, agen, atau environment. Tidak ada pengaturan yang dapat menonaktifkannya. Jika `ANTHROPIC_BASE_URL` menunjuk ke proxy atau gateway, header tersebut dikirim ke sana. Di bawah penyedia inferensi lain mana pun, server tidak pernah mengirimkannya.

Ketika Claude API menjadi penyedia inferensi, server juga memeriksa ke Claude API bahwa kredensialnya untuk panggilan model valid. Server memeriksanya saat startup lalu setiap 60 detik, kecuali Anda mengubah `health.check_interval`. Pemeriksaan ini tidak menjalankan inferensi, dan tidak membawa satu pun dari ketiga header tersebut.

### Field yang menyebutkan perangkat lunak server

Setiap permintaan ke Claude API memiliki header `User-Agent` yang menyebutkan perangkat lunak server dan versinya. Header itu sendiri tidak mengidentifikasi deployment Anda. Seperti pada setiap permintaan Claude API, kunci API mengidentifikasi organisasi Anda. Anthropic dapat menggunakan header tersebut untuk menghitung penggunaan Managed Agents yang di-host sendiri.

Panggilan model juga dapat membawa label `cma-server`, di badan permintaan sebagai `metadata.user_id`. Label tersebut sama di setiap server, sehingga label itu sendiri tidak mengidentifikasi deployment Anda, pengguna Anda, atau sesi Anda. Ketika sebuah panggilan mencapai Anthropic, Anthropic dapat menggunakan label tersebut untuk menghitung penggunaan Managed Agents yang di-host sendiri, bahkan jika proxy telah menghapus header `User-Agent`.

Apakah sebuah panggilan membawa label tersebut bergantung pada tujuan panggilan:

* **Server mengirimkan label pada panggilan berikut:** panggilan ke Claude API, ke Microsoft Foundry, dan ke model gateway yang menerima permintaan yang sama seperti Claude API.
* **Server tidak pernah mengirimkan `metadata.user_id` pada panggilan berikut:** panggilan ke Amazon Bedrock, ke Claude Models on Google Cloud (Google managed), dan ke model gateway yang menggunakan format permintaan lain.

Jika model gateway atau proxy meneruskan panggilan ke penyedia lain, `metadata.user_id` dapat ikut terkirim bersamanya. Pada panggilan yang membawa `metadata.user_id`, proxy atau gateway milik Anda sendiri harus menerimanya di badan permintaan. Jika proxy atau gateway tersebut menolak field itu, setiap panggilan model akan gagal.

## Ke mana log, trace, dan metrik dikirim

Server menulis log-nya ke standard error. Ketika Anda menjalankan server di bawah Docker, Kubernetes, atau pengelola layanan, sistem tersebut mengumpulkan log dari standard error.

Server tidak merekam trace atau metrik apa pun sampai Anda mengaktifkannya dengan variabel lingkungan OpenTelemetry standar. Server mengirimkannya hanya ke tujuan yang ditunjuk oleh variabel tersebut. Endpoint Prometheus juga dapat mengekspos metrik. Lihat [Tempat server mendengarkan](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#where-the-server-listens).

## Berapa lama data disimpan

Pipeline log Anda, collector Anda, dan backend tracing Anda yang menentukan berapa lama log, trace, dan metrik disimpan. Server tidak menyimpan file log dan tidak menyimpan trace atau metrik apa pun.

Server menyimpan semua hal lainnya, seperti agen, sesi, dan riwayat sesi, di database Anda. Jika Anda tidak menyiapkan database, yang merupakan default, server menyimpan data tersebut di memori, dan restart akan menghapusnya. Jika Anda mengonfigurasi pengelola rahasia, server menyimpan rahasia setiap [kredensial vault](https://platform.claude.com/docs/id/managed-agents/vaults) baru di sana sebagai gantinya, bukan di database. Rahasia yang disimpannya sebelumnya tetap berada di database.

Sesi dan riwayatnya tetap tersimpan di database Anda sampai Anda menghapusnya. Server tidak menghapus sesi karena usianya, baik diarsipkan maupun tidak. Menghapus sesi melalui API akan menghapus sesi tersebut beserta riwayatnya dari database Anda, meskipun server tetap menyimpan ID sesi tersebut. Server dapat menolak penghapusan saat sesi sedang berjalan. Penghapusan tersebut tidak menjangkau salinan di tempat lain, seperti cadangan database, log dan trace yang diekspor, atau apa yang ditulis agen ke [memory store](https://platform.claude.com/docs/id/managed-agents/memory). Di Kubernetes, penghapusan tersebut juga membiarkan volume `/workspace` milik sesi tetap ada, sebagaimana dijelaskan di [Membebaskan volume sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#free-a-sessions-volume).

Apa yang dikirim server ke model, dan apa yang dikembalikan model, tunduk pada perjanjian organisasi Anda dengan penyedia yang melayani model tersebut. Ketentuan retensi data dalam perjanjian tersebut berlaku. Ketika Claude API yang melayani model, perjanjian dan pengaturan retensi data yang dimiliki organisasi Anda dengan Anthropic yang berlaku. Jika organisasi Anda memiliki pengaturan [zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope), pengaturan tersebut mencakup panggilan model ini dengan cara yang sama seperti panggilan Messages API lainnya.

Halaman API dan retensi data mencantumkan Claude Managed Agents sebagai [tidak tercakup oleh ZDR](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#what-zdr-does-not-cover). Hal ini karena, ketika Anthropic yang menjalankan layanan tersebut, Anthropic menyimpan transkrip sesi hingga Anda menghapusnya. Siapa yang menyimpan transkrip tersebut bergantung pada siapa yang menjalankan layanan:

* **Anthropic yang menjalankannya:** Anthropic yang menyimpannya. Dengan [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), Anda hanya meng-host sandbox, dan Anthropic yang menjalankan sisanya.
* **Anda yang menjalankannya, dengan Managed Agents yang di-host sendiri:** Anda sendiri yang menyimpannya.

## Siapa yang dapat menjangkau server

Anthropic tidak memiliki akses jarak jauh ke server atau lognya. Aplikasi dan worker Anda terhubung ke server. Server tidak pernah terhubung ke worker.

### Kredensial yang diterima server

Anthropic tidak menerbitkan satu pun kredensial yang diterima server, dan tidak menyimpan satu pun darinya. Setiap kredensial yang diterima server adalah salah satu dari berikut ini:

* Kredensial yang Anda atur atau buat
* Kredensial yang diterbitkan oleh penyedia identitas Anda
* Kredensial yang dibuat oleh server itu sendiri, seperti token yang diberikannya kepada worker bersama setiap bagian pekerjaan

### Tempat server mendengarkan

Server menerima permintaan API pada satu alamat dan port. Server membuka dua listener lagi, masing-masing hanya jika Anda mengaktifkannya.

| Listener                                                                                                                                               | Aktif secara default                                                                                                                                         | Alamat default                                                                                                         | Apa yang dimintanya                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Permintaan API                                                                                                                                         | Ya                                                                                                                                                           | `127.0.0.1:8400`, yang hanya dapat dijangkau oleh mesin yang sama. Untuk mengubah alamat dan port, atur `server.addr`. | Lihat [Kredensial yang diterima server](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#credentials-that-the-server-accepts).         |
| [Konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/console), sebuah halaman web                                    | Ya. Untuk berhenti menyajikannya, lihat [Menonaktifkan konsol](https://platform.claude.com/docs/id/managed-agents/self-hosted/console#turn-off-the-console). | Alamat dan port yang sama dengan permintaan API                                                                        | Tidak ada untuk memuat halaman, bagi siapa pun yang dapat menjangkaunya. Untuk melakukan apa pun di konsol, seseorang harus sign in melalui penyedia identitas Anda. |
| Endpoint metrik Prometheus                                                                                                                             | Tidak                                                                                                                                                        | `localhost:9464`, yang hanya dapat dijangkau oleh mesin yang sama                                                      | Tidak ada kredensial                                                                                                                                                 |
| Listener server untuk [egress gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#environment-variable-credentials) | Tidak                                                                                                                                                        | Port 8410 pada setiap interface                                                                                        | Kunci gateway                                                                                                                                                        |

Detail lebih lanjut tentang dua listener terakhir:

* **Endpoint metrik Prometheus:** Endpoint ini tidak meminta kredensial, sehingga siapa yang dapat menjangkaunya bergantung pada tempat endpoint tersebut mendengarkan. Jika Anda mengatur `OTEL_METRICS_EXPORTER` ke `prometheus` dan tidak mengatur alamat, endpoint mendengarkan pada alamat default. Jika Anda mengaktifkannya melalui Helm chart server, endpoint mendengarkan pada port 9464 di setiap pod server. Apa pun yang memiliki rute ke alamat pod kemudian dapat menjangkaunya, kecuali NetworkPolicy memblokir lalu lintas tersebut.
* **Listener untuk egress gateway:** Egress gateway adalah proxy opsional antara sandbox Anda dan internet. Server mendengarkan gateway pada port terpisah. Listener ini menggunakan HTTP biasa, dan jawabannya membawa nilai kredensial yang tersimpan. Stack Compose dan Helm chart server hanya mengizinkan gateway untuk menjangkaunya. Jika Anda menjalankan server dengan cara lain, lakukan hal yang sama.

Stack Docker Compose memublikasikan port 8400 pada alamat loopback host Docker, `127.0.0.1`. Jalankan Docker Engine 28.3.3 atau yang lebih baru. Pada beberapa rilis sebelumnya, mesin di jaringan lokal host dapat menjangkau port yang dipublikasikan pada loopback. Untuk memublikasikan port pada alamat lain, atur `CMA_PUBLISH_ADDRESS` di `.env`.

## Multitenancy

Setiap deployment melayani satu tenant pada satu tingkat kepercayaan. Environment dalam satu deployment tidak memisahkan tingkat kepercayaan. Kunci API server menjangkau setiap environment. Setiap pemanggil yang memiliki role dapat menjalankan sesi di setiap environment, dengan jaringan dan file apa pun yang dapat dijangkau oleh worker environment tersebut.

| Yang dipisahkan                                | Lakukan ini                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tenant                                         | Berikan setiap tenant deployment-nya sendiri, dengan database, kunci API server, dan worker-nya sendiri.                                                                                                                                                                                                                                                                                                         |
| Beban kerja dengan tingkat kepercayaan berbeda | Berikan setiap tingkat kepercayaan deployment-nya sendiri, yang disiapkan seperti untuk tenant. Contohnya adalah kode tepercaya dan tidak tepercaya, atau worker yang menjangkau sistem yang hanya boleh digunakan oleh sebagian pemanggil.                                                                                                                                                                      |
| Pemanggil dalam satu deployment                | Aktifkan [single sign-on](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#single-sign-on), petakan grup ke role `developer` atau `user`, dan simpan kunci API server untuk administrator. [Apa yang dapat dilakukan setiap peran](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#what-each-role-can-do) menunjukkan apa yang dilihat oleh pemanggil tersebut. |

### Pengelola rahasia, single sign-on, dan model gateway

Jika deployment Anda menggunakan salah satu layanan ini, pisahkan juga deployment tersebut di sana:

* **Pengelola rahasia:** Pisahkan rahasia setiap deployment, sebagaimana dalam [batasan pengelola rahasia](https://platform.claude.com/docs/id/managed-agents/self-hosted/agent-identity#limits).
* **Single sign-on:** Berikan setiap deployment entri `audiences` yang tidak dicantumkan oleh deployment lain mana pun, sehingga deployment tersebut menolak token deployment lain. Di deployment setiap tingkat kepercayaan, berikan role hanya kepada pemanggil yang diizinkan pada tingkat tersebut, dan jangan atur `default_role`.
* **[Model gateway](https://platform.claude.com/docs/id/managed-agents/self-hosted/inference-provider#model-gateway):** Untuk membedakan deployment-deployment tersebut, berikan masing-masing nilainya sendiri untuk header seperti `x-tenant-id` di bawah `inference.headers`.

### Apa yang tidak dibatasi oleh role

Role hanya membatasi permintaan yang dibuat pemanggil dengan token miliknya sendiri. Kode yang dijalankan agen dapat memanggil server dengan kredensial apa pun yang disimpan sandbox-nya. [Kunci environment](https://platform.claude.com/docs/id/managed-agents/self-hosted#the-three-credentials) dapat membaca event dan mengirimkan hasil alat di setiap sesi di environment-nya. Jadi, jalankan setiap sesi di sandbox-nya sendiri, dan jauhkan kunci environment dari sandbox tersebut. Stack di [Memulai dengan Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart) dan [Menerapkan di Kubernetes](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes) melakukan hal ini.
