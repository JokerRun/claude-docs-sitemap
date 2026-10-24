---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: d78b1c6336e807b24a98691262e1cbaee6cc38617f928875a23260ee877a70bf
---

---
title: Apa yang terjadi saat Anda merotasi, menonaktifkan, atau menghapus kunci enkripsi Anda
url: https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle
description: Apa dampak setiap tindakan pada kunci Anda terhadap data Anda, seberapa cepat dampaknya terjadi, dan apakah Anda dapat membatalkannya.
---

Dengan "customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan), atau CMEK, kunci Anda berada di "key management service" (layanan manajemen kunci), atau KMS, milik Anda, dan Claude menyimpan catatan yang merujuk ke kunci tersebut. Menghapus kunci dan menghapus catatannya adalah dua tindakan yang berbeda.

## Apa yang dilakukan setiap tindakan

<Frame>
  ![Status kunci: melampirkan bersifat satu arah, kunci yang dinonaktifkan dapat diaktifkan kembali, dan Anthropic tidak dapat memulihkan data setelah kunci dihapus.](https://platform.claude.com/docs/id/images/cmek/key-states.svg)
</Frame>

| Tindakan                                                                            | Apa yang terjadi                                                                                                                                                                                                                                                                                                                                                        | Dapatkah Anda membatalkannya?                                                                                                                                               |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lampirkan kunci ke workspace (di Claude Enterprise, tambahkan ke organisasi)        | Kunci Anda melindungi data yang ditulis [setelah kunci tersebut mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect). Di Claude Platform, melampirkan kunci juga mengunci [pengaturan retensi data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention) workspace tersebut. | Tidak. Kunci tidak dapat dilepas atau diganti.                                                                                                                              |
| Rotasi material kunci di dalam kunci yang sama                                      | Anda merotasinya di KMS Anda, sesuai jadwal Anda sendiri. Rotasi tidak memerlukan tindakan apa pun di Claude.                                                                                                                                                                                                                                                           | Tidak ada yang perlu dibatalkan. Biarkan versi kunci sebelumnya tetap aktif.                                                                                                |
| Nonaktifkan kunci, atau cabut akses Anthropic ke kunci Anda                         | Perubahan dapat memerlukan waktu hingga 1 jam untuk diterapkan, dan permintaan yang sedang berjalan selama jam tersebut mungkin masih berhasil. Setelah itu, Claude tidak dapat membaca atau menulis data yang dilindungi kunci tersebut, dan permintaan gagal.                                                                                                         | Aktifkan kembali kunci atau pulihkan akses Anthropic ke kunci Anda. [Ada dua batasan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#restore-access). |
| Hapus kunci di KMS Anda, jadwalkan penghapusannya, atau musnahkan material kuncinya | Anthropic tidak dapat memulihkan data yang dilindungi kunci tersebut.                                                                                                                                                                                                                                                                                                   | Tidak oleh Anthropic. Anthropic tidak menyimpan salinan kunci Anda.                                                                                                         |
| Hapus catatan kunci di Claude (**Delete encryption key** di Claude Console)         | Anda hanya dapat melakukan ini selama tidak ada workspace, termasuk workspace yang diarsipkan, yang menggunakan kunci tersebut.                                                                                                                                                                                                                                         | Tidak.                                                                                                                                                                      |

## Apa dampak menonaktifkan kunci, dan apa yang kembali

Selama kunci dinonaktifkan, permintaan Messages API di workspace yang menggunakan kunci tersebut mengembalikan [error 400 dengan kode `cmek_key_disabled`](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cmek-key-disabled).

Mengaktifkan kembali kunci, atau memulihkan akses Anthropic ke kunci Anda, akan mengembalikan akses ke data yang dilindungi kunci tersebut. Ada dua batasan. Permintaan yang gagal selama kunci dinonaktifkan tidak dicoba ulang. Menonaktifkan kunci tidak menjeda periode retensi.

## Jika Anthropic tidak dapat menjangkau kunci Anda

Permintaan yang menyimpan data di bawah kunci Anda akan gagal selama Anthropic tidak dapat menjangkau kunci Anda, misalnya saat terjadi gangguan pada KMS Anda. Di Claude Enterprise, permintaan ini mencakup pesan di chat dan di mode suara.

Di Messages API, permintaan ini mengembalikan error 503 dengan kode `cmek_key_unreachable`, dan Anda dapat mencobanya ulang. Message Batches API mencobanya ulang untuk Anda hingga kunci Anda tersedia atau batch kedaluwarsa.

## Mengganti kunci atau berhenti menggunakan CMEK

Workspace atau organisasi tidak dapat beralih ke kunci lain atau kembali tanpa kunci. Di Claude Platform, Anda dapat membuat workspace baru dengan kunci lain, atau tanpa kunci, lalu memindahkan lalu lintas Anda ke workspace tersebut. Di Claude Enterprise, tidak ada cara untuk mengganti kunci atau berhenti menggunakan CMEK di dalam organisasi.
