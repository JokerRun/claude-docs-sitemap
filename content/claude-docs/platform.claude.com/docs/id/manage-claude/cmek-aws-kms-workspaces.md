---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: fbaf730ecc4e889b7a782bff8dd78d1ebba8d524b147ea26d8f48c07f470443a
---

---
title: Membatasi kunci AWS KMS ke workspace tertentu
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces
description: Tambahkan kondisi kebijakan kunci yang menyebutkan workspace yang diizinkan menggunakan kunci AWS KMS Anda.
---

[Kebijakan kunci dari penyiapan](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) mengizinkan setiap workspace di organisasi Anda menggunakan kunci tersebut. Dengan kondisi opsional ini, workspace yang tidak tercantum tidak dapat menggunakannya.

Tambahkan [ID kompartemen](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#what-one-key-protects) sebuah workspace ke kebijakan sebelum Anda [melampirkan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#register-the-key-with-anthropic) ke workspace tersebut. Untuk workspace baru, itu berarti membuatnya tanpa kunci.

## Salin ID kompartemen workspace

Di Claude Console, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) dan pilih workspace dari menu dropdown di bagian atas. Salin **ID Kompartemen** di bawah **Kunci enkripsi**. Endpoint [Dapatkan Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve) mengembalikannya sebagai `compartment_id`.

Organisasi Claude Enterprise memiliki satu ID kompartemen. Salin dari kunci Anda di bawah **Kunci enkripsi** di [claude.ai > Pengaturan organisasi > Data dan privasi](https://claude.ai/admin-settings/data-privacy-controls).

## Tambahkan kondisi ke kebijakan kunci

Ganti pernyataan `AllowAnthropicCMEKCrypto` dengan pernyataan ini. Isi ID organisasi Anthropic Anda dan ID kompartemen setiap workspace yang menggunakan kunci tersebut. Kunci yang sudah melindungi data [memerlukan satu pernyataan lagi](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#existing-data).

```json
{
  "Sid": "AllowAnthropicCMEKCrypto",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
  },
  "Action": ["kms:Encrypt", "kms:Decrypt"],
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "kms:EncryptionContext:anthropic:org_uuid": ["<ORGANIZATION_UUID>"]
    },
    "StringEqualsIfExists": {
      "kms:EncryptionContext:anthropic:compartment_uuid": ["<COMPARTMENT_UUID>"]
    }
  }
}
```

## Ganti kebijakan kunci pada kunci yang sudah ada

1. Di [konsol AWS KMS](https://console.aws.amazon.com/kms), buka kunci tersebut dan klik tab **Key policy**.
2. Jika Anda melihat **Switch to policy view**, klik opsi tersebut.
3. Klik **Edit**.
4. Ganti JSON dengan kebijakan kunci Anda.
5. Klik **Save changes**.
