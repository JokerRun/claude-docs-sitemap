---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 4f092ffd3690ac5ad2f54e37253a1ce34556d673462ee1bbdd78fad208e23186
---

---
title: Kunci enkripsi yang dikelola pelanggan
url: https://platform.claude.com/docs/id/manage-claude/cmek
description: Gunakan kunci yang Anda pegang di cloud Anda sendiri untuk mengenkripsi data yang disimpan oleh Claude.
---

Tanyakan Claude Code tentang fitur ini

```text
/claude-api ceritakan tentang kunci enkripsi yang dikelola pelanggan
```

Dengan "customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan), atau CMEK, Anda membuat kunci di AWS KMS, Google Cloud KMS, atau Azure Key Vault milik Anda sendiri. Anthropic menggunakannya untuk mengenkripsi data tertentu saat diam (at rest). Kunci tersebut tetap berada di bawah kendali Anda, sehingga Anda dapat merotasinya, mengaudit penggunaannya, dan mencabut akses Anthropic.

## Pilih halaman penyiapan Anda

Pilih layanan yang menyimpan kunci Anda. Claude Platform on AWS, yang juga menggunakan AWS KMS, memiliki halamannya sendiri.

<CardGroup cols={2}>
  <Card title="AWS KMS" href="https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms">
    Untuk Claude Platform dan Claude Enterprise.
  </Card>

  <Card title="Google Cloud KMS" href="https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms">
    Untuk Claude Platform dan Claude Enterprise.
  </Card>

  <Card title="Azure Key Vault" href="https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault">
    Untuk Claude Platform dan Claude Enterprise.
  </Card>

  <Card title="Claude Platform on AWS" href="https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws">
    Untuk organisasi yang sidebar Claude Console-nya menampilkan **Account managed by AWS**.
  </Card>
</CardGroup>

Di Claude Platform, Anda juga dapat menambahkan dan melampirkan kunci Anda [dengan Admin API](https://platform.claude.com/docs/id/manage-claude/cmek-admin-api).

## Pahami CMEK sebelum Anda menyiapkannya

Produk yang Anda gunakan menentukan apa yang dienkripsi oleh kunci Anda, apa yang tetap berada di bawah kunci Anthropic, dan fitur mana yang dinonaktifkan atau berubah.

<CardGroup cols={2}>
  <Card title="Cara kerja CMEK" href="https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works">
    Bagaimana kunci Anda melindungi data, kapan kunci tersebut mulai berlaku, dan apa yang dapat Anda lihat.
  </Card>

  <Card title="CMEK, retensi data, dan ZDR" href="https://platform.claude.com/docs/id/manage-claude/cmek-data-retention">
    Menggunakan kunci dengan tanpa retensi data (ZDR), dan apa yang dapat dipreservasi oleh Anthropic di luar kunci Anda.
  </Card>

  <Card title="Apa yang dicakup CMEK di Claude Platform" href="https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform">
    Cari fitur atau jenis data.
  </Card>

  <Card title="Apa yang dicakup CMEK di Claude Enterprise" href="https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise">
    Cari fitur, dan lihat apa yang akan diperhatikan oleh pengguna Anda.
  </Card>
</CardGroup>

## Apa yang Anda sepakati

* Setelah Anda melampirkan kunci, Anda [tidak dapat melepas atau menggantinya](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does).
* Kunci Anda hanya melindungi data yang ditulis [setelah kunci tersebut mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).
* Jika kunci Anda dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya. [Selama kunci dinonaktifkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#restore-access), Claude tidak dapat membaca data tersebut.
* Di Claude Platform, workspace yang memiliki kunci [wajib menerapkan retensi data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention).

## Siapa yang dapat menggunakan CMEK

CMEK bersifat opsional. Untuk mengaktifkannya bagi organisasi yang memenuhi syarat, hubungi tim akun Anthropic Anda. Anda memerlukan salah satu peran berikut untuk menyiapkannya:

* Claude Platform: Organization Admin
* Claude Platform on AWS: Admin
* Claude Enterprise: Owner atau Primary Owner

## Setelah penyiapan

* [Apa yang terjadi saat Anda merotasi, menonaktifkan, atau menghapus kunci enkripsi Anda](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle)
* [Memecahkan masalah CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting)
