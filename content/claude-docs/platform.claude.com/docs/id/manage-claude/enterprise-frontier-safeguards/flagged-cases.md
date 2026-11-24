---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: 9cb5fbc62f5ea011aa7f752f58f22f665f785b68ecc9bcd3d6118233ef904fb0
---

---
title: Tinjau Safety Cases
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases
description: Cara tim Anda menerima, menyelidiki, dan menanggapi Safety Cases yang dikirimkan Anthropic, serta tempat mendapatkan bantuan.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Pemantauan keselamatan otomatis memeriksa prompt dan respons Anda untuk mencari tanda-tanda penyalahgunaan serius, seperti upaya mengembangkan kemampuan siber ofensif atau biologis. Enterprise Frontier Safeguards mengharuskan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) dinonaktifkan. Saat fitur tersebut nonaktif, potensi pelanggaran Kebijakan Penggunaan Anthropic yang ditemukan pemantauan keselamatan otomatis dapat menjadi Safety Case untuk ditinjau oleh tim Anda sendiri. Anthropic memperkirakan Safety Cases akan jarang terjadi bagi sebagian besar organisasi.

## Cara kerja peninjauan Safety Case

1. **[Anthropic mengirimkan Safety Case kepada Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#where-cases-arrive).**
2. **[Anda meninjaunya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#read-a-case)** untuk melihat pesan mana yang dicakupnya dan jenis risiko apa yang dilaporkannya.
3. **[Anda menyelidiki](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#investigate)**, dengan log Anda sendiri dan transkrip.
4. **[Anda menanggapi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#respond-to-a-case)** untuk mengonfirmasi bahwa Anda telah menyelidikinya.
5. **[Anthropic menutup Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#after-you-respond).**

## Mendapatkan Safety Cases

Safety Cases dapat sampai kepada Anda dengan dua cara: sebagai file di penyimpanan Anda sendiri dan melalui API.

Di Claude Platform, biarkan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) tetap aktif. Permintaan yang Anda kirim saat API tersebut nonaktif tidak memiliki transkrip baik di [bucket kasus](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) Anda maupun melalui API Safety Cases. Tanpa bucket kasus, Anda juga tidak mendapatkan Safety Cases selama API tersebut nonaktif.

### Di penyimpanan Anda sendiri

Anthropic menulis Safety Cases dan transkrip yang dapat dibaca ke [bucket di akun cloud Anda sendiri](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored). Untuk memilih salah satunya:

1. Baca [Transkrip dan Safety Cases di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket) sebelum Anda memilih bucket. Tidak setiap bucket Amazon S3 dapat menerima Safety Cases.
2. Untuk setiap workspace, pilih bucket tersebut di bawah **Safety Case and Transcript storage** di Claude Console.

Saat Anthropic mengirimkan Safety Case kepada Anda, Anthropic menambahkan [file Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files) ke penyimpanan Anda.

Ada dua batasan yang berlaku:

* Anda hanya mendapatkan file Safety Case untuk workspace yang memiliki [bucket data keselamatan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) (lihat [Menyiapkan penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage)). Bucket tersebut menyimpan data keselamatan tersegel, yang tidak dapat dibaca oleh tim Anda. Anda memilihnya di bawah **Sealed Safety Data storage**, yang merupakan pengaturan yang terpisah dari **Safety Case and Transcript storage**.
* Di Claude Platform, Anda juga hanya mendapatkan file Safety Case untuk pesan yang Anda kirim setelah workspace mulai menggunakan bucket data keselamatannya.

### Melalui API

[API Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api) menyajikan Safety Cases yang sama melalui HTTP. API ini memungkinkan Anda membaca dan menanggapi Safety Cases. API ini hanya tersedia di Claude Platform. API ini sedang dalam beta.

Apakah Anda juga memerlukan bucket kasus bergantung pada platform Anda:

* **Claude Platform:** Anda juga dapat memilih bucket kasus untuk setiap workspace di bawah **Safety Case and Transcript storage**. Tanpa bucket tersebut, Anda tidak mendapatkan Safety Cases untuk pesan dengan profil pengguna.
* **Claude Models on Google Cloud (Anthropic managed) dan Claude Platform on AWS:** Safety Cases hanya dapat sampai ke tim Anda melalui bucket kasus. Pantau bucket tersebut, karena 7 hari untuk menanggapi dimulai saat Anthropic mengirimkan Safety Case.

### Cara mengetahui kapan Safety Case dibuat

Anthropic tidak memberi tahu Anda secara otomatis saat membuat Safety Case. Pantau penyimpanan Anda atau [lakukan polling ke API](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll) untuk Safety Cases, agar Anda dapat menanggapi dengan cepat. Lihat [Peringatan untuk file baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#alerts) untuk cara-cara mengirim peringatan ke SIEM atau sistem tiket Anda berdasarkan pembaruan penyimpanan.

## Meninjau Safety Case

### Isi Safety Case

Setiap Safety Case mencakup:

* ID-nya
* Kategori kebijakan, seperti `cyber` atau `bio`
* ID setiap pesan, dan lokasi transkripnya
* Workspace yang mengirim pesan tersebut, dan terkadang profil pengguna yang mengirimnya

Di bucket Anda, Safety Case berupa file JSON. [File Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#safety-case-file) menjelaskan field-field-nya.

Melalui API, [tampilkan daftar Safety Cases Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll), lalu [baca setiap pesan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#read-a-message). API juga mengembalikan pengguna atau kunci API yang dicatat Anthropic untuk sebuah pesan.

### Menyelidiki Safety Case

Sebagian besar Safety Cases berujung pada salah satu dari empat hasil:

| Apa yang Anda temukan | Apa yang harus dilakukan |
| ----- | ----- |
| **Pekerjaan yang diotorisasi.** Misalnya, red team Anda menjalankan uji penetrasi di bawah Cyber Verification Program. | Konfirmasikan dengan tim yang memiliki pekerjaan tersebut. Tanggapi dengan `no_violation`. |
| **Karyawan atau pengguna yang bertindak atas kemauannya sendiri, melanggar kebijakan.** Mereka melanggar kebijakan Anda atau Kebijakan Penggunaan Anthropic tanpa persetujuan organisasi Anda. | Cabut akses mereka dan ikuti proses Anda sendiri. Tanggapi dengan `violation`. |
| **Pengguna eksternal atau kredensial yang dicuri.** | Blokir pengguna tersebut atau rotasi kuncinya. Tanggapi dengan `violation`. |
| **Positif palsu.** Pemantauan keselamatan otomatis salah membaca maksud atau kontennya. | Tidak ada yang perlu diperbaiki. Tanggapi dengan `no_violation`. |

Siapa yang Anda libatkan, termasuk HR, bagian hukum, atau manajer, bergantung pada proses Anda sendiri.

<Note>
  Berhati-hatilah saat Anda memasukkan transkrip ini ke Claude atau model AI lain. Transkrip tersebut dapat memicu Safety Case lain.
</Note>

## Menanggapi Safety Case

Tanggapi dalam 7 hari kalender sejak `created_at` Safety Case, yaitu waktu saat Anthropic mengirimkannya. Dengan menanggapi, Anda mengonfirmasi bahwa Anda telah menyelidiki dan mengidentifikasi penyebabnya dan, jika terjadi pelanggaran, telah mengambil langkah untuk memastikan hal itu tidak terulang.

Safety Case Response Anda menyatakan apakah Anda menemukan pelanggaran. Anda tidak perlu membagikan nama, bukti, atau transkrip kepada Anthropic. Informasi apa pun yang Anda pilih untuk dibagikan kepada Anthropic sebagai bagian dari tanggapan Anda menjadi bagian dari Safety Case. Tanggapan menutup Safety Case, sehingga Anda tidak dapat mengubahnya atau menambahkan apa pun ke dalamnya nanti.

Anda dapat menanggapi dengan salah satu dari dua cara. Gunakan salah satunya untuk setiap Safety Case, karena Anthropic menghitung tanggapan pertama.

### Opsi 1: Menulis file respons

Tulis [file respons](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file) ke bucket yang menyimpan Safety Cases Anda. Path-nya bergantung pada penyedia penyimpanan Anda:

* **Amazon S3:** `review-responses/<case_id>.json`
* **Bucket Google Cloud Storage yang terhubung di Claude Console:** `<organization ID>/review-responses/<case_id>.json`

Periksa file tersebut berdasarkan [Aturan untuk file yang valid](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file-rules), karena hanya file yang valid yang dihitung.

### Opsi 2: Menanggapi melalui API

Kirim satu permintaan untuk [menanggapi Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#respond).

### Setelah Anda menanggapi

Saat Anthropic membaca tanggapan yang valid, Anthropic menutup Safety Case. Alasan penutupan `responded` mengonfirmasi bahwa Anthropic telah menerima tanggapan Anda. Melalui API, Safety Case langsung ditutup. Jika Safety Case masih terbuka sehari setelah Anda menulis file, lihat [Mengapa Safety Case tetap terbuka](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#still-open).

Jika Anthropic memerlukan informasi lebih lanjut dari Anda mengenai tanggapan Anda, Anthropic mengirimkan Safety Notice (lihat [Polling untuk Safety Notices](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll-for-notices)), atau tim akun Anthropic Anda akan menghubungi Anda.

## Jika Anthropic mengambil tindakan

Enterprise Frontier Safeguards tidak mengubah [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup) Anthropic atau standar penegakannya. Anthropic hanya melakukan penegakan untuk bahaya yang jelas dan disengaja.

### Jika Anda tidak menanggapi

Menanggapi dengan segera dapat membantu menjaga akun Anda tetap dalam status baik. Jika 7 hari kalender berlalu tanpa tanggapan yang valid, Anthropic menutup Safety Case. Jika Safety Case tetap tidak ditanggapi, Anthropic dapat menangguhkan akses.

### Jika Anthropic menangguhkan akses

Dalam kasus langka ketika pemantauan keselamatan otomatis menemukan bahaya yang jelas dan disengaja, Anthropic dapat menangguhkan akses untuk membatasi bahaya lebih lanjut selagi Anda menyelidiki. Penangguhan dapat sesempit satu pengguna atau profil pengguna. Safety Case dapat menyebutkan profil pengguna jika Anda mengirimkannya. Untuk meminta akses dipulihkan, hubungi tim akun Anthropic Anda. Jika Safety Case masih terbuka, tanggapi juga Safety Case tersebut. Selama seluruh organisasi Anda ditangguhkan, API Safety Cases menolak kunci Anda.

## Praktik terbaik

* **Catat ID pesan.** Untuk melacak pesan hingga ke pengirimnya, Anthropic menyarankan untuk mencatat `id` (`msg_...`) dari setiap respons Messages API bersama ID pengguna Anda sendiri. Sering kali masuk akal untuk memulai ini sejak awal, karena log Anda hanya mencakup permintaan sejak saat itu. Anda juga dapat menetapkan `metadata.user_id` ke ID buram, yang akan muncul kembali di transkrip.
* **Simpan transkrip yang Anda perlukan.** Transkrip memiliki masa kedaluwarsa (lihat [Isi bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#whats-in-the-bucket)).

## Menghubungi untuk mendapatkan bantuan

Tim akun Anthropic Anda adalah kontak Anda untuk Safety Cases. Sebutkan ID Safety Case agar Anthropic dapat menemukan Safety Case yang tepat. Anda tidak perlu mengutip atau memberikan transkrip.

Tanpa Anthropic Human Review, orang-orang di Anthropic yang menangani Safety Case hanya melihat detail terbatas, seperti ID-nya, kategorinya, dan tindakan apa pun yang diusulkan. Mereka tidak dapat membaca transkrip Anda.

* **Anda memerlukan lebih banyak waktu:** Beri tahu tim akun Anthropic Anda sebelum 7 hari berakhir. Safety Case tetap ditutup tepat waktu.
* **Anda menganggap Safety Case keliru:** Tanggapi dengan `no_violation`.

## Pertanyaan dan pemecahan masalah

<AccordionGroup>
  <Accordion title="Apakah tim Anda memerlukan cakupan 24/7?">
    Anthropic tidak meminta cakupan 24/7 untuk Safety Cases. Anthropic memperkirakan Safety Cases jarang terjadi, dan Anda memiliki waktu beberapa hari, bukan beberapa jam, untuk menanggapi. Kirim peringatan ke antrean yang diperiksa seseorang setiap hari kerja.
  </Accordion>

  <Accordion title="Dapatkah Anda menguji prosesnya sebelum Safety Case sungguhan masuk?">
    Tanyakan kepada tim akun Anthropic Anda apakah Safety Case uji tersedia untuk organisasi Anda.
  </Accordion>

  <Accordion title="Apakah Anthropic mengirimkan webhook untuk Safety Cases?">
    Tidak. Sebagai gantinya, [pantau bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#set-up-alerts) atau [lakukan polling ke API Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll).
  </Accordion>

  <Accordion title="Siapa yang meninjau saat Anthropic Human Review aktif?">
    Tim kecil yang terspesialisasi di Anthropic dapat meninjau apa yang ditemukan oleh pemantauan keselamatan otomatis. Anda dapat membiarkan Anthropic Human Review tetap aktif hanya untuk workspace yang menggunakan penyimpanan yang dikelola Anthropic. Enterprise Frontier Safeguards mengharuskannya dinonaktifkan.
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Periksa penyiapan Anda" icon="check" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#check-your-setup">
    Di Claude Platform, pastikan bahwa penyiapan Anda berfungsi sebelum Anda memulai penggunaan produksi.
  </Card>

  <Card title="Siapkan penyimpanan milik pelanggan" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage">
    Simpan data keselamatan tersegel Anda di penyimpanan dalam akun cloud Anda sendiri.
  </Card>

  <Card title="Human Review dan Access Transparency" icon="shield" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency">
    Lihat siapa di Anthropic yang meninjau data Anda, dan catatan apa yang Anda dapatkan.
  </Card>
</CardGroup>
