---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-data-retention
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 004a17c840415268666e9967e1a47b916255af717001edd040b9973907b14990
---

---
title: CMEK, retensi data, dan ZDR
url: https://platform.claude.com/docs/id/manage-claude/cmek-data-retention
description: Mengapa workspace dengan kunci menyimpan data, apa artinya bagi ZDR, dan apa yang dapat dipreservasi Anthropic di luar kunci Anda.
---

Di Claude Platform, “customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK, dan [retensi data nol lama (Legacy ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) tidak dapat berbagi workspace. Di Claude Enterprise, organisasi dapat menggunakan CMEK dan ZDR Claude Code bersama-sama, tetapi organisasi tersebut kemudian [tidak dapat mengaktifkan Claude Docs atau Claude Sheets](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

Namun, di Claude Platform, Anda dapat melampirkan kunci ke workspace yang menggunakan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS). EFS adalah ZDR, dan data keselamatan tersegel milik workspace tersebut ditulis ke penyimpanan milik Anda. EFS dalam tahap beta. Untuk langkah-langkahnya, lihat [Melampirkan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) di panduan EFS.

## Kunci memerlukan workspace yang menyimpan data

CMEK mengenkripsi data yang disimpan, sedangkan dengan Legacy ZDR di Claude Platform, Anthropic tidak menyimpan prompt atau respons Anda. Dengan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS), Anthropic mengenkripsi data keselamatan tersegel Anda dengan kunci Anda sebelum menuliskannya ke bucket Anda. Jadi, Anda hanya dapat melampirkan kunci ke workspace dengan **Retensi data standar** (30 hari) atau workspace yang menggunakan EFS.

Setelah Anda melampirkan kunci, Anda tidak dapat menonaktifkan retensi data untuk workspace tersebut. Untuk kembali memiliki workspace yang tidak menyimpan data, buat workspace baru dan pindahkan lalu lintas Anda ke sana.

## Dalam organisasi Legacy ZDR

Organisasi Legacy ZDR di Claude Platform dapat menggunakan CMEK. Anda mengalihkan satu workspace ke **Retensi data standar**, menyetujui ketentuan retensi data, dan melampirkan kunci Anda ke workspace tersebut. Workspace yang Anda alihkan tidak boleh berupa workspace default, yang retensinya mengikuti retensi organisasi. Workspace Anda yang lain tetap menggunakan Legacy ZDR.

[Pilih halaman penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up) dan ikuti langkah melampirkan di halaman tersebut.

## Preservasi terbatas di luar kunci Anda

Dalam tiga kasus sempit, Anthropic dapat mempreservasi catatan tertentu dengan enkripsi yang dikelola Anthropic:

* Ketika Anthropic diwajibkan oleh hukum untuk menyimpan catatan (misalnya, materi yang dilaporkan ke NCMEC berdasarkan 18 U.S.C. § 2258A)
* Risiko mendesak atas bahaya serius (misalnya, pengembangan senjata CBRNE, serangan siber ofensif, atau ancaman kekerasan yang segera terjadi)
* Pelanggaran Bagian D.4 dari [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) Anthropic atau ketentuan yang setara dalam perjanjian lain yang berlaku antara pelanggan dengan Anthropic

Di luar [penyaringan CSAM](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservasi memerlukan keputusan eksplisit dari peninjau manusia dan mengikuti [kebijakan retensi untuk data komersial](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) Anthropic. Untuk setiap kejadian preservasi, peristiwa [Activity Feed Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) yang sesuai dibuat dengan kode alasan yang menyampaikan tujuan preservasi tersebut. Lihat [preservasi konten CMEK](https://platform.claude.com/docs/id/manage-claude/access-transparency#cmek-content-preservation) untuk detailnya. Metadata penyaringan keselamatan disimpan dengan enkripsi yang dikelola Anthropic dan tetap dapat dibaca setelah pencabutan kunci. Ini adalah catatan yang diturunkan dari pemindaian keselamatan otomatis Anthropic, seperti pengidentifikasi pola dan indikator kecocokan, bukan konten percakapan.
