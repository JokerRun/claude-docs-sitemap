---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 27a283e90f1097da21b23005f668a7ff6371063e7bfafff10654e8ed6d3ba311
---

---
title: Membatasi kunci AWS KMS ke workspace tertentu
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces
description: Tambahkan kondisi kebijakan kunci yang menyebutkan workspace yang diizinkan menggunakan kunci AWS KMS Anda.
---

[Kebijakan kunci dari penyiapan](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) mengizinkan setiap workspace di organisasi Anda menggunakan kunci tersebut. Dengan kondisi opsional ini, workspace yang tidak tercantum tidak dapat menggunakannya.

Tambahkan [ID kompartemen](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#what-one-key-protects) sebuah workspace ke kebijakan sebelum Anda [melampirkan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#register-the-key-with-anthropic) ke workspace tersebut. Untuk workspace baru, itu berarti membuatnya tanpa kunci.

## Salin ID kompartemen workspace

Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) dan pilih workspace dari menu dropdown di bagian atas. Salin **Compartment ID** di bawah **Encryption key**. Endpoint [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve) mengembalikannya sebagai `compartment_id`.

Organisasi Claude Enterprise memiliki satu ID kompartemen. Salin dari kunci Anda di bawah **Encryption keys** di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls).

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
