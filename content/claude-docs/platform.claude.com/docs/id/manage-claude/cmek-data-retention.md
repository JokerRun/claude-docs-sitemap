---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-data-retention
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 42d0ca09ea05fd097761d6d79a290a803df9c271109a8abffd3dc56f909a7350
---

---
title: CMEK, retensi data, dan ZDR
url: https://platform.claude.com/docs/id/manage-claude/cmek-data-retention
description: Mengapa workspace dengan kunci menyimpan data, apa artinya bagi ZDR, dan apa yang dapat dipreservasi Anthropic di luar kunci Anda.
---

Di Claude Platform, "customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan), atau CMEK, dan [retensi data nol (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) tidak dapat berbagi workspace. Di Claude Enterprise, organisasi dapat menggunakan CMEK dan ZDR bersama-sama, tetapi organisasi tersebut kemudian [tidak dapat mengaktifkan artifact](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

## Kunci memerlukan workspace yang menyimpan data

CMEK mengenkripsi data yang disimpan, sedangkan dengan ZDR di Claude Platform, Anthropic tidak menyimpan prompt atau respons Anda. Jadi, Anda hanya dapat melampirkan kunci ke workspace dengan **Standard data retention** (30 hari).

Setelah Anda melampirkan kunci, Anda tidak dapat menonaktifkan retensi data untuk workspace tersebut. Untuk kembali ke ZDR, buat workspace baru dan pindahkan lalu lintas Anda ke sana.

## Dalam organisasi ZDR

Organisasi ZDR di Claude Platform dapat menggunakan CMEK. Anda mengalihkan satu workspace ke **Standard data retention**, menyetujui ketentuan retensi data, dan melampirkan kunci Anda ke workspace tersebut. Workspace yang Anda alihkan tidak boleh berupa workspace default, yang retensinya mengikuti retensi organisasi. Workspace Anda yang lain tetap menggunakan ZDR.

[Pilih halaman penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up) dan ikuti langkah melampirkan di halaman tersebut.

## Preservasi terbatas di luar kunci Anda

Dalam tiga kasus sempit, Anthropic dapat mempreservasi catatan tertentu dengan enkripsi yang dikelola Anthropic:

* Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A)
* Risiko mendesak atas bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang segera terjadi)
* Pelanggaran Bagian D.4 dari [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan yang setara dalam perjanjian lain yang berlaku antara pelanggan dengan Anthropic

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservasi memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) Anthropic. Untuk setiap kejadian preservasi, peristiwa [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) yang sesuai dibuat dengan kode alasan yang menyampaikan tujuan preservasi tersebut. Lihat [preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keselamatan disimpan dengan enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci. Ini adalah catatan yang diturunkan dari pemindaian keselamatan otomatis Anthropic, seperti pengidentifikasi pola dan indikator kecocokan, bukan konten percakapan.
