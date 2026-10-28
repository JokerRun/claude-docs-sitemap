---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 0fb79d815002b4019dd2a017e12f8b0bccecabc917ee97761db324a62a0f697d
---

---
title: Memecahkan masalah CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting
description: Temukan penyebab dan perbaikan untuk pesan kesalahan CMEK, verifikasi yang gagal, atau entri log yang tidak terduga.
---

**Verify** di Claude Console, **Add** di claude.ai, dan panggilan validate pada Admin API semuanya menjalankan pemeriksaan yang sama. Jika pemeriksaan gagal (**Connection failed** di Claude Console), lihat penyebabnya untuk [AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#aws-kms), [Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#google-cloud-kms), atau [Azure Key Vault](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#azure-key-vault).

Jika suatu fitur berhenti berfungsi, mungkin fitur tersebut termasuk yang dinonaktifkan oleh “customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK. Periksa [daftar Claude Platform](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-platform#turned-off-or-changed) atau [daftar Claude Enterprise](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

Jika tidak ada yang sesuai di sini, hubungi tim akun Anthropic Anda.

## Permintaan gagal setelah penyiapan

### `cmek_key_disabled`

```text wrap
Customer-managed encryption key is disabled or revoked. Re-enable the key to restore access.
```

Kesalahan 400 ini berarti layanan manajemen kunci Anda menolak panggilan Anthropic. Periksa penyebab berikut secara berurutan:

1. Kunci dinonaktifkan.
2. Akses Anthropic ke kunci Anda telah dicabut. [Halaman penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up) menunjukkan akses yang dibutuhkan Anthropic.
3. Di AWS KMS, kebijakan kunci [mencantumkan workspace](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces) tetapi tidak mencantumkan workspace ini.
4. Di AWS KMS, kondisi IP memblokir [alamat IP keluar Anthropic](https://platform.claude.com/docs/id/api/ip-addresses#outbound-ip-addresses).

Perbaiki penyebabnya. [Dua batasan berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#restore-access) saat akses pulih.

### `cmek_key_network_blocked`

```text wrap
The request to your key management service was blocked by its network access controls (for example, a KMS firewall or IP allowlist). Verify that your KMS network rules allow requests from Anthropic's published IP addresses, or contact Anthropic support if your configuration looks correct.
```

Ini adalah kesalahan 400. Kunci itu sendiri mungkin dalam kondisi baik. Izinkan [alamat IP Anthropic yang dipublikasikan](https://platform.claude.com/docs/id/api/ip-addresses) dalam aturan jaringan layanan manajemen kunci Anda.

### `cmek_key_unreachable`

```text wrap
The workspace's customer-managed encryption key could not be reached. Try again shortly. If this continues, check that the key is available in your key management service, or contact Anthropic support.
```

Kesalahan 503 ini berarti [Anthropic tidak dapat menjangkau kunci Anda](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#unreachable-key). Coba ulang permintaan tersebut.

## Verifikasi gagal: AWS KMS

| Penyebab                                           | Perbaikan                                                                                                                                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID organisasi salah                                | Kondisi `org_uuid` harus mencantumkan [ID organisasi Anthropic Anda](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#prerequisites), yaitu UUID tanpa awalan `org_`.       |
| Sebuah workspace tidak ada dalam kebijakan         | Kondisi `compartment_uuid` harus [mencantumkan ID kompartemen](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces) dari setiap workspace tempat kunci dilampirkan. |
| Akses diberikan melalui IAM, bukan kebijakan kunci | Peran Anthropic memerlukan akses di [kebijakan kunci itu sendiri](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy).                                             |

Untuk mencetak kebijakan kunci, jalankan:

```bash
aws kms get-key-policy \
  --region <REGION> \
  --key-id <KEY_ARN> \
  --policy-name default
```

### Kunci yang sudah melindungi data

Jika Anda [mengganti kebijakan pada kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces#replace-the-key-policy) yang sudah melindungi data, tambahkan pernyataan kebijakan ini agar Anthropic tetap dapat mendekripsi data tersebut. Dalam kondisinya, cantumkan ID kompartemen dari setiap workspace tempat kunci tersebut sedang atau pernah dilampirkan.

```json
{
  "Sid": "AllowAnthropicCMEKDecryptExistingData",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
  },
  "Action": "kms:Decrypt",
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "kms:EncryptionContext:anthropic:compartment_uuid": ["<COMPARTMENT_UUID>"]
    }
  }
}
```

## Verifikasi gagal: Google Cloud KMS

| Penyebab                                   | Perbaikan                                                                                                                                                                                      |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Label organisasi salah                     | Kunci memerlukan [label organisasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#organization-label), dengan ID organisasi Anthropic Anda dalam huruf kecil.        |
| Domain restricted sharing                  | Kebijakan organisasi ini memblokir pemberian akses ke akun layanan Anthropic. [Tambahkan pengecualian](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#prerequisites). |
| Versi kunci dinonaktifkan atau dimusnahkan | Versi utama kunci harus diaktifkan.                                                                                                                                                            |

Untuk memeriksa pemberian akses, jalankan:

```bash
gcloud kms keys get-iam-policy <your-key-name> \
  --project=<your-project-id> \
  --location=<region> \
  --keyring=<your-keyring-name>
```

## Verifikasi gagal: Azure Key Vault

| Penyebab                                  | Perbaikan                                                                                                                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tag organisasi salah                      | Versi kunci saat ini memerlukan [tag organisasi](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#organization-tag).                                            |
| Penetapan peran belum berlaku             | Penetapan peran baru dapat memerlukan beberapa menit. Tunggu, lalu coba lagi.                                                                                                         |
| Aturan jaringan vault memblokir Anthropic | Periksa aturan tersebut terhadap [pengaturan vault yang dibutuhkan Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#check-your-vault-configuration). |

## Melampirkan gagal di Claude Platform on AWS

Claude Platform on AWS tidak memiliki langkah **Verify**, sehingga masalah pada kunci akan terlihat saat Anda melampirkannya.

| Penyebab                       | Perbaikan                                                                                                                                                                                                                                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ketidakcocokan kebijakan kunci | Cetak kebijakan kunci dengan [perintah `get-key-policy`](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#aws-kms) dan bandingkan dengan [kebijakan di halaman penyiapan](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#prepare-the-key-policy). |
| Ketidakcocokan kondisi         | Setiap kondisi `EncryptionContext` atau `aws:SourceArn` harus menyertakan workspace ini.                                                                                                                                                                                                               |
| Status atau lokasi kunci       | Kunci harus diaktifkan, bersifat single-Region, dan berada di akun AWS serta region yang sama dengan workspace.                                                                                                                                                                                        |
| Izin tidak ada                 | Principal yang Anda gunakan untuk masuk memerlukan `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci.                                                                                                                                                                                     |

Jika melampirkan masih gagal, temukan event `kms:` yang ditolak di CloudTrail pada akun kunci. Event tersebut menunjukkan principal yang memanggil dan, untuk panggilan kriptografis, konteks enkripsinya. Perbaiki penyebabnya, lalu klik **Save** lagi.

## Melampirkan atau menambahkan kunci ditolak

### Workspace tidak menyimpan data

```text wrap
CMEK keys can only be attached to workspaces in this organization that have inference data retention enabled.
```

[Organisasi Anda menggunakan “zero data retention” (tanpa retensi data), atau ZDR](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#zdr-organizations), dan kunci memerlukan workspace yang menyimpan data. Alihkan workspace ke **Standard data retention** terlebih dahulu.

### Workspace tidak memiliki pengaturan Encryption key

Hanya [workspace yang menyimpan data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention) yang memiliki pengaturan ini, jadi pilih **Standard data retention** untuk workspace tersebut terlebih dahulu. Workspace default organisasi ZDR tidak dapat dialihkan, jadi gunakan workspace lain.

### Tidak ada bagian Encryption keys

Di Claude Console, pilih **Organization** dari menu dropdown di bagian atas halaman Data retention. Jika bagian tersebut masih tidak ada, peran Anda tidak mencakupnya atau CMEK belum diaktifkan untuk organisasi Anda. Tim akun Anthropic Anda yang mengaktifkan CMEK.

### Workspace sudah memiliki kunci

```text wrap
This workspace already has a different external key attached.
```

Kunci sebuah workspace tidak dapat diganti, jadi [buat workspace baru](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#change-keys) untuk kunci yang berbeda.

### Menambahkan kunci di claude.ai gagal

```text wrap
The encryption key couldn’t be added.
```

Pemeriksaan pada kunci Anda gagal. Temukan penyebabnya untuk [AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#aws-kms), [Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#google-cloud-kms), atau [Azure Key Vault](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#azure-key-vault). Untuk mencoba lagi, klik **Add key** lagi. Kotak dialog akan terbuka dengan detail Anda sebelumnya. Pilih kotak centang, klik **Continue**, lalu klik **Add**.

## Kesalahan yang diharapkan di CloudTrail

Di Claude Platform dan Claude Enterprise, Anthropic memeriksa kunci setiap kali Anda memverifikasinya, melampirkannya ke workspace, atau melihatnya di claude.ai. Setiap pemeriksaan menambahkan empat kesalahan access-denied yang diharapkan ke CloudTrail.

Untuk menyaringnya, cocokkan ketiga nilai berikut:

* `requestParameters.encryptionContext.associatedData`: `Y21lay12YWxpZGF0aW9u`
* `userIdentity.accountId`: `915198916910`
* `resources.ARN`: `arn:aws:kms:<REGION>:<AWS_ACCOUNT_ID>:key/<KEY_ID>`

Nilai pertama saja tidak cukup, karena pemanggil mana pun dapat menetapkannya.
