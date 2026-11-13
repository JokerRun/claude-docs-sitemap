---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 1f42e6434ccbe8175df3073ba07e5528f4e1761921667aea81955a64210b2049
---

---
title: Security posture di Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview
description: Pahami apa yang diungkapkan Compliance API tentang halaman Security posture (Security Center) di claude.ai, dan dari mana harus memulai.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Halaman **Security posture** di **Pengaturan organisasi** claude.ai membandingkan pengaturan Claude organisasi Anda dengan kontrol keamanan yang direkomendasikan Anthropic. Melalui Compliance API, alat keamanan Anda dapat membaca perubahan yang dicatat halaman tersebut. Alat tersebut juga dapat membaca hasil saat ini. Security posture melaporkan pengaturan Anda dan tidak mengubahnya. Item sidebar-nya adalah **Security posture**, dan halaman yang dibukanya berjudul **Security Center**.

## Pilih jalur Anda

Untuk memasukkan perubahan di halaman ke sistem security information and event management (SIEM) Anda, mulailah dengan [Mengirim peristiwa Security posture ke SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events). Jika Anda sudah menyerap seluruh Activity Feed, Anda sudah memilikinya; periksa dua hal di bagian [Jika Anda sudah menyerap seluruh feed](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events#if-you-already-ingest-the-full-feed).

* Untuk memberikan peringatan atas perubahan berisiko, lihat [Mendeteksi perubahan pada Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes).
* Untuk menormalkan ke Open Cybersecurity Schema Framework (OCSF), lihat [Memetakan peristiwa Security posture ke OCSF](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/ocsf-mapping).
* Untuk menemukan siapa yang menerima risiko mana, kapan, dan sampai kapan, lihat [Referensi peristiwa Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference); untuk risiko yang berlaku, lihat [Hasil saat ini](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#current-results).

Untuk bekerja dengan hasil saat ini dari endpoint, gunakan halaman-halaman berikut:

* Untuk dasbor, lihat [Referensi hasil Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference).
* Untuk memverifikasi peristiwa yang tersimpan, lihat [Mencocokkan peristiwa Security posture yang tersimpan dengan hasil saat ini](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/check-events-against-results).
* Jika endpoint dan halaman tidak sesuai, lihat [Bagaimana atestasi ditampilkan dalam respons](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#how-an-attestation-shows-in-the-response).

Untuk memahami datanya, baca terus.

## Apa yang dievaluasi Security posture

Security posture mengevaluasi daftar kontrol, dan memberikan hasil untuk masing-masing kontrol.

### Kontrol

Kontrol adalah satu pengaturan atau praktik yang direkomendasikan, seperti single sign-on. Setiap kontrol memiliki nama tampilan dan pengidentifikasi. Pengidentifikasi tersebut sama untuk setiap organisasi. Kontrol juga dapat memiliki nilai saat ini (`current_value`) dan nilai yang direkomendasikan (`desired_state`). Ada tiga jenis kontrol:

| Jenis                    | Apa yang menentukan hasilnya                                                                                                      | Contoh                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Kontrol otomatis         | Pemeriksaan otomatis atas nilai saat ini terhadap nilai yang direkomendasikan, kecuali ada atestasi yang berlaku.                 | `sso_enabled`              |
| Kontrol manual           | Seseorang, karena Anthropic tidak dapat membaca pengaturan tersebut, misalnya ketika pengaturan itu berada di konsol vendor lain. | `oauth_conditional_access` |
| Kontrol khusus informasi | Tidak ada: tidak ada nilai yang direkomendasikan, sehingga kontrol dilaporkan dan tidak diberi hasil.                             | `allowed_invite_domains`   |

### Atestasi

Atestasi adalah pernyataan tercatat dari seseorang tentang posisi organisasi terhadap suatu kontrol; atestasi bukan hasil pemeriksaan. Sebagian besar kontrol dapat memiliki atestasi, termasuk kontrol otomatis, apa pun hasil pemeriksaannya. Atestasi memiliki salah satu dari tiga nilai:

* Selesai (`completed`): kontrol sudah diterapkan.
* Risiko diterima (`accepted_risk`): kontrol tidak diterapkan, dan organisasi menerima risikonya.
* Gagal (`control_failed`): kontrol tidak diterapkan.

Seseorang yang dapat melakukan atestasi melakukannya di halaman. API membaca atestasi dan tidak dapat membuatnya. Halaman dapat mengajukan pertanyaan ketika seseorang melakukan atestasi, dan terkadang mewajibkan jawaban. Halaman menyimpan jawaban tersebut bersama atestasi sebagai [komentar](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#what-anthropic-stores-when-someone-attests) atestasi tersebut, paling banyak 2.000 karakter. Aktivitas di Activity Feed tidak pernah menyertakan komentar tersebut atau menunjukkan bahwa komentar tersebut ada. Endpoint juga tidak mengembalikan komentar.

### Hasil

Setiap kontrol memiliki salah satu dari empat hasil.

| Hasil                             | Arti                                                                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Lulus (`passed`)                  | Memenuhi nilai yang direkomendasikan, atau atestasi Selesai atau Risiko diterima sedang berlaku.                                          |
| Gagal (`failed`)                  | Tidak memenuhi nilai yang direkomendasikan, atau diatestasi sebagai Gagal (`control_failed`).                                             |
| Belum diatestasi (`not_attested`) | Kontrol manual tanpa atestasi yang berlaku.                                                                                               |
| Deskriptif (`descriptive`)        | Tidak diberi hasil, bahkan ketika diatestasi; mencakup kontrol khusus informasi serta kontrol yang tidak relevan atau tidak dapat dibaca. |

Risiko diterima yang berlaku dihitung sebagai Lulus pada kontrol otomatis atau manual, meskipun kontrol tersebut tidak diterapkan. Dalam respons, kontrol otomatis yang [diatestasi sebagai Selesai selama pemeriksaannya tidak berhasil](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#how-an-attestation-shows-in-the-response) bernilai `failed`.

### Apa yang membuat atestasi berhenti berlaku

Atestasi tetap berlaku sampai salah satu dari tiga hal berikut terjadi:

* Seseorang mencabut atau mengubahnya.
* Tanggal berakhirnya (`review_date`) tiba. Orang yang melakukan atestasi memilih 90 hari atau tanpa tanggal berakhir.
* Pada kontrol otomatis atau kontrol khusus informasi, nilai saat ini berubah, atau, untuk risiko diterima pada beberapa kontrol otomatis, pemeriksaan otomatis berhasil.

Tanpa atestasi yang berlaku, hasil kontrol otomatis mengikuti pemeriksaannya, dan kontrol manual bernilai Belum diatestasi.

## Perubahan dari waktu ke waktu: Activity Feed

Activity Feed menjawab apa yang berubah, kapan, dan siapa yang mengubahnya. Feed mencatat aktivitas ketika seseorang melakukan atestasi pada kontrol, mengubah atestasi, atau mencabutnya, dan terkadang ketika atestasi berhenti berlaku secara otomatis.

Judul halaman-halaman ini menyebut aktivitas tersebut sebagai peristiwa. Membacanya memerlukan scope `read:compliance_activities` atau `read:org_audit`. [Referensi peristiwa Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference) mencantumkan field-nya. Untuk mengumpulkannya, lihat [Mengirim peristiwa Security posture ke SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events).

## Hasil saat ini: endpoint

Endpoint menjawab apa hasil suatu kontrol pada saat permintaan dibuat. Gunakan endpoint untuk membuat laporan di seluruh organisasi di bawah [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api#how-the-compliance-api-works) Anda. Setiap panggilan membaca satu organisasi dan tidak mengembalikan riwayat. Untuk setiap kontrol yang dicantumkannya, respons memberikan `id`, `display_name`, dan hasilnya dalam `rating`, menggunakan pengidentifikasi dalam [tabel hasil](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#results).

Memanggilnya memerlukan scope `read:compliance_org_data` atau `read:org_audit`.

Halaman, endpoint, dan feed tidak selalu menampilkan hal yang sama, karena respons tidak menyertakan sebagian kontrol dan sebagian atestasi. Lihat [Bagaimana atestasi ditampilkan dalam respons](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#how-an-attestation-shows-in-the-response) dan [Mencocokkan peristiwa Security posture yang tersimpan dengan hasil saat ini](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/check-events-against-results).

## Ketersediaan

Security posture masih dalam tahap beta.

**Jika organisasi Anda menggunakan Claude Enterprise, Security posture tersedia untuknya, dan organisasi induknya telah mengaktifkan Compliance API,** Activity Feed mencatat aktivitas atestasi untuk organisasi tersebut, dan endpoint mengembalikan hasil organisasi Anda.

Anda juga memerlukan Compliance Access Key dengan scope yang sesuai. Halaman-halaman ini mengasumsikan Anda telah membaca [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) dan [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

**Jika organisasi Anda menggunakan paket lain, atau merupakan organisasi Claude Console,** Activity Feed tidak mencatat aktivitas Security posture untuknya, dan endpoint mengembalikan 404.

**Jika halaman Security posture telah dinonaktifkan untuk organisasi Anda,** endpoint mengembalikan 404 untuk organisasi Anda hingga halaman tersebut diaktifkan. Bahkan kunci untuk organisasi induk pun mendapatkan 404 tersebut.

Untuk beberapa organisasi, endpoint mengembalikan 404 meskipun ketiga kondisi tersebut terpenuhi dan halaman tidak dinonaktifkan.

## Siapa yang dapat melihat siapa yang melakukan atestasi

Setiap aktivitas atestasi yang disebabkan oleh seseorang mencatat ID pengguna orang tersebut, alamat emailnya pada saat itu, serta alamat IP dan user agent permintaan. Kunci mana pun yang mencakup organisasi dan memiliki `read:compliance_activities` atau `read:org_audit` dapat membacanya, bahkan setelah orang tersebut meninggalkan organisasi atau akunnya telah dihapus. Menghapus organisasi tidak menghapus aktivitas-aktivitas ini dari Activity Feed, yang menyimpan aktivitas selama 6 tahun. Kunci milik organisasi itu sendiri berhenti berfungsi saat organisasi tersebut dihapus.

Kunci mana pun yang memiliki `read:compliance_org_data` dan `read:compliance_user_data` sekaligus, atau `read:org_audit`, dapat membaca, di `attested_by` pada endpoint, ID pengguna orang yang melakukan atestasi, jika endpoint mengembalikannya, bahkan untuk atestasi yang dibuat sebelum Anda memiliki akses.

Nilai-nilai ini adalah data pribadi; salinan Anda tetap ada lebih lama daripada keanggotaan orang tersebut. Sebelum Anda mengumpulkan data ini, beri tahu orang-orang yang melakukan atestasi.

## Apa yang disimpan Anthropic saat seseorang melakukan atestasi

Anthropic menyimpan satu atestasi per kontrol, termasuk nilainya, kapan atestasi tersebut dibuat, tanggal berakhir jika ada, dan akun orang yang melakukan atestasi. Melakukan atestasi lagi akan menggantikannya.

Anthropic tetap menyimpan atestasi setelah tanggal berakhirnya tiba atau setelah atestasi tersebut [berhenti berlaku secara otomatis](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#what-ends-an-attestation), sampai seseorang mencabutnya atau Anthropic menghapusnya saat menghapus organisasi. Jika akun orang yang melakukan atestasi dihapus, Anthropic tetap menyimpan atestasi tersebut, yang tidak lagi menyebutkan siapa yang melakukan atestasi. Aktivitas apa pun di Activity Feed yang disebabkan oleh orang ini tetap menyebutkan orang tersebut. Mencabut atau mengganti atestasi tersebut tidak menghapus apa pun dari Activity Feed (lihat [Siapa yang dapat melihat siapa yang melakukan atestasi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#who-can-see-who-attested)).

[Kunci enkripsi yang dikelola pelanggan (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek), [zero data retention (ZDR) untuk Claude Code](https://code.claude.com/docs/en/zero-data-retention), dan [paket Enterprise siap HIPAA](https://support.claude.com/en/articles/13296973-hipaa-ready-enterprise-plans) tidak mengubah apa yang disimpan Anthropic dari kontrol, nilai, tanggal, dan akun suatu atestasi. Tidak satu pun dari ketiganya memperpendek berapa lama Anthropic menyimpan keempatnya. CMEK tidak mengenkripsi keempat bagian tersebut.

Komentar suatu atestasi adalah jawaban atas pertanyaan yang dapat diajukan halaman Security posture ketika seseorang melakukan atestasi. Anthropic menyimpan komentar suatu atestasi sampai seseorang mencabut atestasi tersebut atau Anthropic menghapus komentar tersebut saat menghapus organisasi. Melakukan atestasi lagi dapat menggantikan atau menghapus komentar tersebut. Periode retensi percakapan kustom tidak memperpendek berapa lama Anthropic menyimpan atestasi atau komentar tersebut. Aktivitas di Activity Feed tidak pernah menyertakan komentar tersebut (lihat [Apa yang tidak dicatat oleh feed](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#what-the-feed-does-not-record)).

Beberapa organisasi tidak dapat menyimpan komentar bersama atestasi karena pengaturan penanganan datanya, seperti CMEK atau ZDR. Untuk organisasi tersebut, halaman Security posture tidak menampilkan kotak komentar dan tidak meminta jawaban ketika seseorang melakukan atestasi. Jika suatu organisasi telah menyimpan komentar sebelum pengaturan tersebut berlaku untuknya, komentar tersebut tetap tersimpan bersama atestasinya. Halaman Security posture tidak menampilkan komentar tersebut. Mencabut atestasi akan menghapus komentar tersebut.

Selama Security posture tidak tersedia untuk suatu organisasi, Anthropic tetap menyimpan atestasi dan komentar organisasi tersebut. Selama waktu itu, tidak seorang pun dapat melihat atau mencabutnya di halaman Security posture.
