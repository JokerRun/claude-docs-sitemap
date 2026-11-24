---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: 0413e3d15d536ca265cb9db0ef95354de9707e108bfe5512e9b67a591be280d4
---

---
title: Enterprise Frontier Safeguards
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview
description: Zero Data Retention (ZDR) bagi organisasi yang memenuhi syarat yang menggunakan model Claude yang paling mumpuni, dengan data keselamatan tersegel di akun cloud Anda sendiri.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Enterprise Frontier Safeguards (EFS) adalah [Zero Data Retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) bagi organisasi yang memenuhi syarat yang menggunakan [model Claude yang paling mumpuni](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements), seperti Claude Fable 5.1. Anthropic tidak menyimpan prompt dan respons Anda. Data keselamatan tersegel ditulis ke penyimpanan milik Anda. EFS memerlukan bucket Anda sendiri. Workspace yang menggunakan [penyimpanan yang dikelola Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) tidak menggunakan EFS, karena Anthropic menyimpan salinan terenkripsi dari prompt dan respons workspace tersebut.

Gunakan EFS saat Anda menginginkan model Claude yang paling mumpuni, tetapi perlu menyimpan data keselamatan tersegel Anda di akun cloud Anda sendiri. Dengan EFS, orang-orang di organisasi Anda, bukan peninjau di Anthropic, yang meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases). EFS mencakup keduanya:

* [Penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage): Bucket yang menerima data keselamatan tersegel Anda (prompt, respons, dan penalaran model, yang dienkripsi dalam format Anthropic). Tim Anda tidak dapat membaca data keselamatan tersegel, bahkan di bucket Anda sendiri.
* [Tim Anda meninjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases): Anthropic Human Review selalu nonaktif, sehingga tim Anda sendiri yang meninjau kasus yang ditandai yang ditemukan oleh pemantauan keselamatan otomatis.

<Frame>
  ![Perbandingan EFS, Anthropic managed, dan Legacy ZDR. Enterprise Data Controls mencakup peninjauan dan kunci pada Anthropic managed.](https://platform.claude.com/docs/id/images/efs-how-it-works-enterprise-data-controls.svg)
</Frame>

Anthropic tidak mengenakan biaya untuk EFS, dan EFS tidak mengubah perilaku model, harga API, atau batas laju. Penyedia cloud Anda menagih Anda untuk penyimpanan tersebut seperti biasa, termasuk operasi baca, operasi tulis, dan data egress.

EFS mencakup permintaan ke Messages API dalam workspace yang dikonfigurasi untuk EFS, apa pun modelnya. EFS tidak mencakup data yang disimpan oleh fitur Claude Platform untuk penggunaannya sendiri, bahkan dalam permintaan Messages API, seperti container eksekusi kode, unggahan Files API, hasil Batch API, dan sesi Claude Managed Agents. Lihat [Data dan retensi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#data-and-retention) di FAQ.

## Di Claude Platform, EFS berlaku untuk seluruh workspace

Setelah EFS mulai berlaku untuk sebuah workspace, EFS berlaku untuk setiap permintaan ke setiap model dalam workspace tersebut, termasuk model yang tidak memerlukan retensi data.

Untuk menggunakan EFS hanya bagi sebagian lalu lintas, gunakan workspace yang terpisah. [Kunci API](https://platform.claude.com/docs/id/manage-claude/workspaces#api-keys-and-resource-scoping) atau ID workspace yang Anda kirim menentukan kartu mana yang digunakan oleh sebuah permintaan. Workspace baru membiarkan workspace Anda yang sudah ada beserta kunci API-nya tetap seperti semula.

## Enterprise Data Controls

Di Claude Platform, menerima [ketentuan EFS dan Enterprise Data Controls](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access) memberi Anda keduanya. Dengan Enterprise Data Controls, Anda dapat [menggunakan kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys) atau [menonaktifkan Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review) pada penyimpanan yang dikelola Anthropic. Dengan salah satunya, [Access Transparency](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#check-access-transparency) aktif untuk organisasi Anda.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Siapkan penyimpanan milik pelanggan" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage">
    Simpan data keselamatan tersegel Anda di penyimpanan di akun cloud Anda sendiri.
  </Card>

  <Card title="Tinjau Safety Cases" icon="file" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases">
    Terima, selidiki, dan tanggapi Safety Cases yang dikirimkan Anthropic.
  </Card>

  <Card title="Gunakan kunci yang dikelola pelanggan" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys">
    Enkripsi data Anda dengan kunci yang Anda simpan di layanan manajemen kunci Anda sendiri, dengan EFS atau dengan penyimpanan yang dikelola Anthropic.
  </Card>
</CardGroup>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Panduan penyiapan" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console">
    Dapatkan akses dan siapkan EFS di platform yang Anda gunakan.
  </Card>

  <Card title="FAQ Enterprise Frontier Safeguards" icon="book" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq">
    Jawaban atas pertanyaan umum tentang EFS.
  </Card>
</CardGroup>
