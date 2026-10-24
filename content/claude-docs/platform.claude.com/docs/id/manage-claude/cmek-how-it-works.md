---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 5c1e91547d45b90c01ebd496f0277c3ae008184de0d0d004d7950177c07837de
---

---
title: Cara kerja CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works
description: Bagaimana kunci Anda melindungi data yang tersimpan, apa yang dicakup oleh satu kunci, kapan kunci tersebut mulai berlaku, dan apa yang dapat Anda lihat.
---

## Kunci Anda membungkus kunci yang mengenkripsi data Anda

Anthropic mengenkripsi data Anda yang tersimpan dengan kunci data. Dengan "customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan), atau CMEK, kunci Anda mengenkripsi, atau membungkus, kunci data tersebut. Ini adalah enkripsi amplop (envelope encryption). Untuk menulis atau membaca data, Anthropic meminta "key management service" (layanan manajemen kunci), atau KMS, Anda untuk membungkus atau membuka bungkus sebuah kunci data.

Kunci data berpindah antara Anthropic dan cloud Anda. Kunci Anda tidak pernah meninggalkan KMS Anda. Data Anda tidak pernah dikirim ke sana.

<Frame>
  ![Kunci Anda tetap berada di KMS cloud Anda dan membungkus kunci data milik Anthropic, yang mengenkripsi data Anda. Cloud Anda dapat mencatat setiap panggilan.](https://platform.claude.com/docs/id/images/cmek/key-wrapping.svg)
</Frame>

Anthropic tidak menyimpan salinan kunci Anda, sehingga tanpa kunci tersebut, Claude [tidak dapat membaca data yang dilindunginya](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle).

## Apa yang dilindungi oleh satu kunci

Di Claude Platform dan Claude Platform on AWS, sebuah kunci melindungi sebuah workspace, dan satu kunci dapat melayani beberapa workspace. Di Claude Enterprise, sebuah kunci melindungi seluruh organisasi, yang hanya dapat memiliki satu kunci. [Data mana yang dilindungi oleh kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek#what-cmek-protects) bergantung pada produk Anda.

Di Claude Platform dan Claude Enterprise, kunci Anda memuat ID organisasi Anthropic Anda, yang mengaitkan kunci tersebut dengan organisasi Anda. Bergantung pada KMS Anda, ID tersebut dimasukkan ke dalam kondisi kebijakan kunci, label, atau tag. Kunci tanpa ID tersebut gagal dalam verifikasi. Kunci yang dibagikan antar-organisasi memuat setiap ID.

Kebijakan kunci AWS KMS dapat [menyebutkan workspace](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces) berdasarkan ID kompartemennya. ID kompartemen adalah UUID yang diberikan Anthropic kepada setiap workspace untuk enkripsi, bukan ID workspace yang diawali dengan `wrkspc_`.

## Tempat kunci Anda berada

Kunci Anda berada di AWS KMS, Google Cloud KMS, atau Azure Key Vault. Penyedia Anda mungkin mengenakan biaya untuk kunci tersebut.

Di Claude Platform dan Claude Enterprise, Anthropic memproses semua operasi enkripsi di region AS. Kunci Anda dapat berada di luar AS, dengan konsekuensi berupa tambahan latensi. [Setiap halaman penyiapan](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up) menyebutkan region dengan latensi terendah.

## Kapan kunci Anda mulai berlaku

Kunci Anda hanya melindungi data yang ditulis setelah kunci tersebut mulai berlaku. Data yang sudah ada (obrolan, file, dan sesi sebelumnya) tetap berada di bawah kunci milik Anthropic dan tidak dienkripsi ulang.

Di Claude Platform dan Claude Platform on AWS, kunci yang dilampirkan ke sebuah workspace sebelum permintaan pertamanya mulai berlaku pada permintaan tersebut. Pada workspace yang sedang digunakan, kunci Anda dapat memerlukan waktu hingga satu hari untuk mulai berlaku, dan data yang ditulis selama itu tetap berada di bawah kunci milik Anthropic. Itulah sebabnya Anthropic merekomendasikan workspace baru.

## Apa yang dapat Anda lihat

Log audit cloud Anda dapat mencatat setiap operasi yang dilakukan Anthropic dengan kunci Anda. Jika Anda harus mengaktifkan pencatatan tersebut, halaman penyiapan Anda mencantumkannya sebagai prasyarat. Di AWS CloudTrail, beberapa entri merupakan [error yang diharapkan](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cloudtrail).

Perubahan pada konfigurasi CMEK Anda muncul di [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Operasi kunci tidak muncul di sana.

## Latensi dan standar

Setiap operasi membungkus atau membuka bungkus merupakan perjalanan pulang-pergi ke KMS Anda, yang dapat menambah sedikit latensi pada pembacaan dan penulisan data yang tersimpan. Untuk standar kriptografi seperti FIPS, lihat whitepaper CMEK di [Trust Center](https://trust.anthropic.com/resources).

Selanjutnya, baca [apa yang dilakukan setiap tindakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does).
