---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/console
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 88391832b607ca075dd1c7628e1ff24cd883f9a4530d48af5dc0971b6c885cf7
---

---
title: Gunakan konsol di server Anda
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/console
description: Siapkan proses masuk untuk konsol di server Claude Managed Agents yang di-host sendiri, lalu buat agen dan jalankan sesi di browser.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Konsol di server Anda adalah halaman web yang disajikan oleh server Claude Managed Agents yang di-host sendiri pada alamat yang sama dengan API-nya. Di dalamnya, Anda membuat agen, menjalankan sesi, dan mengelola environment, credential vault, memory store, dan skill, tanpa SDK atau CLI.

Ini bukan Claude Console di platform.claude.com. Konsol ini hanya menampilkan apa yang ada di server Anda.

## Siapkan proses masuk

Administrator menyiapkan proses masuk satu kali. Untuk mencoba konsol di satu mesin saja, ikuti [Coba konsol di server Anda](https://platform.claude.com/docs/id/managed-agents/self-hosted/quickstart#try-the-console-on-your-server), yang menggunakan penyedia proses masuk tiruan dari rilis tersebut.

<Steps>
  <Step title="Siapkan single sign-on dan login terminal">
    Ikuti [Single sign-on](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#single-sign-on), termasuk [Mengizinkan developer login dari terminal](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#let-developers-log-in-from-a-terminal). Konsol memasukkan pengguna melalui aplikasi yang Anda daftarkan untuk login terminal. Konsol memeriksa setiap token terhadap entri pertama `audiences` dalam entri issuer, jadi cantumkan audience aplikasi tersebut terlebih dahulu.
  </Step>

  <Step title="Sajikan konsol melalui HTTPS">
    Tempatkan proxy yang melakukan terminasi TLS di depan port 8400. [Tempatkan TLS di depan server](https://platform.claude.com/docs/id/managed-agents/self-hosted/kubernetes#put-tls-in-front-of-the-server) mencantumkan apa yang harus dilakukan proxy. Melalui HTTP biasa, proses masuk hanya berfungsi di `localhost` atau `127.0.0.1`.
  </Step>

  <Step title="Tambahkan alamat konsol ke aplikasi">
    Di penyedia identitas Anda, tambahkan alamat HTTPS server Anda sebagai redirect URI kedua dari aplikasi tersebut, dengan garis miring di akhir: `https://cma.example.com/`. Izinkan juga origin-nya, `https://cma.example.com`, untuk permintaan lintas origin (CORS).
  </Step>
</Steps>

Untuk memeriksa penyiapan, [buka konsol](https://platform.claude.com/docs/id/managed-agents/self-hosted/console#open-the-console) dan masuk.

## Buka konsol

Jika aplikasi Anda memanggil `https://cma.example.com`, buka `https://cma.example.com/` di browser, lalu klik **Continue with SSO**.

Anda masuk melalui penyedia identitas Anda. Konsol tidak menerima kunci API server. Jika konsol menyatakan bahwa proses masuk belum disiapkan di server ini, administrator perlu [menyiapkan proses masuk](https://platform.claude.com/docs/id/managed-agents/self-hosted/console#set-up-sign-in).

## Jalankan agen dari konsol

Alat bawaan agen kosong, seperti `bash`, berjalan di worker, jadi pilih environment yang sedang di-polling oleh worker. [Apa yang berjalan di mana](https://platform.claude.com/docs/id/managed-agents/self-hosted#what-runs-where) menjelaskan apa itu worker. Tanpa worker, panggilan alat pertama akan menunggu hingga ada worker yang menjalankannya. Administrator membuat environment, dan mereka dapat melihat worker suatu environment di tab **Workers**-nya.

<Steps>
  <Step title="Buat agen">
    Di sidebar, pilih **Agents**, lalu klik **Create agent**. Pilih titik awal, seperti **Blank agent**, lalu masukkan nama.

    Klik **Create agent**. Halaman agen akan terbuka.
  </Step>

  <Step title="Mulai sesi">
    Di halaman agen, klik **Start session**. Pilih environment, lalu klik **Create session**. Halaman sesi akan terbuka.
  </Step>

  <Step title="Kirim pesan">
    Masukkan pesan di kotak di bagian bawah halaman, lalu kirimkan. Halaman diperbarui saat agen bekerja. Jika suatu panggilan alat menunggu Anda, kartunya menampilkan **Approve** dan **Deny**.
  </Step>
</Steps>

Selama suatu panggilan alat menunggu Anda, lencana sesi menunjukkan **Idle**.

Untuk membuka sesi lain, seperti sesi yang dimulai oleh aplikasi melalui API, pilih **Sessions** di sidebar, lalu pilih sesi tersebut.

## Siapa melihat apa

Peran Anda menentukan apa yang ditampilkan konsol, sama seperti di API:

* **Administrator** melihat dan mengubah semua hal di server.
* **Orang dengan peran `developer` atau `user`** melihat setiap environment. Dari agen, sesi, vault, memory store, dan skill, mereka hanya melihat apa yang mereka buat dengan akun masuk mereka sendiri.

Agen atau sesi yang dibuat dengan kunci API server, seperti yang ada di quickstart, hanya terlihat oleh administrator. Untuk tabel lengkapnya, lihat [Apa yang dapat dilakukan setiap peran](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#what-each-role-can-do).

## Nonaktifkan konsol

Server menyajikan konsol secara default. Untuk menonaktifkannya, atur `console.serve: false` di [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go), lalu mulai ulang server. Server kemudian berhenti menyajikan konsol. Agen dan sesi tetap berfungsi melalui API.

## Langkah selanjutnya

* [Panggil API di server yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted/call-the-api): Lakukan pekerjaan yang sama dari kode Anda atau CLI `ant`.
* [Data dan akses di Claude Managed Agents yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#who-can-reach-the-server): Lihat siapa yang dapat menjangkau server dan konsolnya.
