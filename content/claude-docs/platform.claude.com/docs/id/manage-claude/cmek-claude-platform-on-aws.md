---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 182d2e98a262de11dd38ac0f4c396112f9b38538903ccedafa5ec9026db31a27
---

---
title: Menyiapkan CMEK di Claude Platform on AWS
url: https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws
description: Buat kunci AWS KMS di akun AWS Anda dan lampirkan ke workspace di Claude Platform on AWS.
---

Jika sidebar Claude Console Anda tidak menampilkan **Account managed by AWS**, ikuti [Menyiapkan CMEK dengan AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms) sebagai gantinya.

## Sebelum Anda memulai

* "Customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan), atau CMEK, telah [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/cmek#availability).

* Di akun AWS yang menjadi host organisasi Anda, Anda dapat membuat kunci AWS KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).

* Anda memiliki peran **Admin** di [Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console).

* Principal IAM yang Anda gunakan untuk masuk memiliki izin berikut:

  * Masuk: `aws-external-anthropic:AssumeConsole`
  * Menambahkan kunci: `aws-external-anthropic:RegisterKey`
  * Melihat kunci: `aws-external-anthropic:ListKeys` dan `aws-external-anthropic:GetKey`
  * Melampirkan kunci: `aws-external-anthropic:UpdateWorkspace` atau `aws-external-anthropic:CreateWorkspace`, ditambah `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci tersebut
  * Memilih kunci dari daftar (opsional): `kms:ListKeys` dan `kms:DescribeKey`

  Untuk membatasi cakupannya, lihat [tindakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys).

* Anda memiliki workspace tanpa kunci yang dilampirkan, idealnya workspace baru, karena [data yang sudah ada tetap berada di bawah kunci Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect). Kebijakan kunci mencantumkan ID kompartemen workspace tersebut.

Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) dan pilih workspace dari menu dropdown di bagian atas. Salin **Compartment ID** di bawah **Encryption key**. Endpoint [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve) mengembalikannya sebagai `compartment_id`.

## Di AWS: buat kunci

### Tulis kebijakan kunci

Kebijakan ini memberikan akses ke kunci Anda kepada service principal AWS `aws-external-anthropic.amazonaws.com`. Gunakan hanya nama yang dipublikasikan di halaman ini, jangan pernah nama yang dikirim melalui email atau chat. Salin kebijakan ini ke editor teks:

```json key-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AccountRootAdmin",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:root"
      },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "AllowClaudePlatformOnAWSCrypto",
      "Effect": "Allow",
      "Principal": {
        "Service": "aws-external-anthropic.amazonaws.com"
      },
      "Action": ["kms:Encrypt", "kms:Decrypt", "kms:GenerateDataKey"],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "kms:EncryptionContext:anthropic:compartment_uuid": ["<COMPARTMENT_UUID>"]
        }
      }
    },
    {
      "Sid": "AllowClaudePlatformOnAWSDescribe",
      "Effect": "Allow",
      "Principal": {
        "Service": "aws-external-anthropic.amazonaws.com"
      },
      "Action": "kms:DescribeKey",
      "Resource": "*"
    }
  ]
}
```

Ganti `<AWS_ACCOUNT_ID>` dengan [ID akun AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/console-account-id.html) Anda dan `<COMPARTMENT_UUID>` dengan [ID kompartemen](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#prerequisites).

Kondisi `EncryptionContext` yang opsional membatasi kunci ke workspace yang Anda cantumkan. Sebelum Anda melampirkan kunci ke workspace lain, tambahkan ID kompartemen workspace tersebut dan [ganti kebijakan pada kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces#replace-the-key-policy). Untuk tidak menggunakan kondisi tersebut, hapus blok `Condition` dari pernyataan `AllowClaudePlatformOnAWSCrypto`. Jika Anda menambahkan kondisi tersebut nanti, cantumkan setiap workspace yang sudah dilampiri kunci tersebut.

Untuk mempersempit akses lebih lanjut, gunakan kebijakan kunci, bukan pembatasan berbasis IP. Tambahkan kondisi `aws:SourceArn` ke kedua pernyataan service principal. Kondisi berikut mengizinkan setiap workspace di akun AWS Anda:

```text wrap
"ArnLike": {"aws:SourceArn": "arn:aws:aws-external-anthropic:*:<AWS_ACCOUNT_ID>:workspace/*"}
```

Untuk workspace tertentu, cantumkan [ARN workspace](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#service-details) lengkapnya sebagai gantinya, dalam bentuk ini:

```text wrap
arn:aws:aws-external-anthropic:<REGION>:<AWS_ACCOUNT_ID>:workspace/<WORKSPACE_ID>
```

### Buat kunci

Buat kunci di akun AWS yang menjadi host organisasi Anda, di region yang sama dengan workspace.

<Tabs>
  <Tab title="AWS Console">
    <Steps>
      <Step title="Buka wizard Create key">
        Buka [konsol AWS KMS](https://console.aws.amazon.com/kms) dan beralihlah ke region untuk kunci tersebut. Buka **Customer managed keys** lalu klik **Create key**.
      </Step>

      <Step title="Configure key">
        Pastikan opsi-opsi berikut dipilih:

        * **Key type:** Symmetric
        * **Key usage:** Encrypt and decrypt
        * **Advanced options > Key material origin:** KMS
        * **Advanced options > Regionality:** Single-Region key

        Klik **Next**.

        <Frame caption="Kunci Symmetric, Encrypt and decrypt, Single-Region key.">
          ![Langkah Configure key di AWS KMS dengan tipe kunci Symmetric, penggunaan kunci Encrypt and decrypt, dan Single-Region key dipilih.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
        </Frame>
      </Step>

      <Step title="Add labels">
        Masukkan **Alias** untuk kunci tersebut, misalnya `anthropic-cmek`. Klik **Next**.

        <Frame caption="Alias untuk kunci tersebut.">
          ![Langkah Add labels di AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
        </Frame>
      </Step>

      <Step title="Define key administrative permissions">
        Jangan pilih administrator kunci apa pun. Kebijakan kunci Anda sudah memberikan kontrol admin penuh kepada akun AWS Anda. Klik **Next**.

        <Frame caption="Biarkan administrator kunci kosong.">
          ![Langkah Define key administrative permissions di AWS KMS yang menampilkan daftar peran IAM yang dapat mengelola kunci tersebut.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
        </Frame>
      </Step>

      <Step title="Define key usage permissions">
        Jangan pilih pengguna kunci apa pun, dan jangan tambahkan apa pun di bawah **Other AWS accounts**. Kebijakan kunci Anda sudah memberikan akses yang diperlukan. Klik **Next**.
      </Step>

      <Step title="Edit key policy">
        Klik **Edit**. Ganti seluruh kebijakan dengan kebijakan kunci Anda, lalu klik **Next**.
      </Step>

      <Step title="Review">
        Klik **Finish**.
      </Step>

      <Step title="Salin ARN kunci">
        Di **Customer managed keys**, buka kunci baru tersebut dan salin ARN-nya. Siapa pun yang menambahkan kunci di Claude memerlukannya.
      </Step>
    </Steps>
  </Tab>

  <Tab title="AWS CLI">
    Simpan kebijakan kunci Anda sebagai `key-policy.json`, lalu buat kuncinya. Ganti `<REGION>` dengan region kunci tersebut.

    ```bash
    aws kms create-key \
      --region <REGION> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy file://key-policy.json
    ```

    Salin `KeyMetadata.Arn` dari output. Siapa pun yang menambahkan kunci di Claude memerlukan ARN tersebut.
  </Tab>
</Tabs>

## Di Claude: tambahkan dan lampirkan kunci

Masuk ke Claude Console melalui AWS. Untuk membuat skrip bagian ini sebagai gantinya, gunakan endpoint yang tercantum di [tindakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys).

<Steps>
  <Step title="Buka pengaturan kunci enkripsi">
    Di Claude Console, buka [Encryption keys](https://platform.claude.com/settings/privacy#encryption-keys) di halaman Data retention. Jika bagian tersebut tidak ada, pilih **Organization** dari menu dropdown di bagian atas.
  </Step>

  <Step title="Tambahkan kunci">
    Di bawah **Encryption keys**, klik **Add key** dan masukkan **Display name**.
  </Step>

  <Step title="Masukkan ARN kunci">
    Di **KMS key ARN**, pilih kunci Anda. Jika tidak tercantum, klik **Enter ARN manually** dan tempelkan ARN-nya. Anthropic menolak ARN alias dan kunci multi-Region. Klik **Add**.
  </Step>

  <Step title="Lampirkan kunci ke workspace">
    <Warning>
      Melampirkan kunci [tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Anda tidak dapat melepasnya dari workspace atau menggantinya. Jika kunci dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya.
    </Warning>

    1. Di bagian atas halaman Data retention, pilih workspace dari menu dropdown.
    2. Di bawah **Encryption key**, pilih kunci lalu klik **Save**.
    3. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Confirm**.

    Anda akan melihat **Workspace settings updated.** Setelah kunci [mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), CloudTrail mencatat panggilan ke kunci Anda.

    Proses melampirkan memeriksa kunci dengan satu panggilan enkripsi dan satu panggilan dekripsi, sehingga masalah kebijakan kunci akan terlihat di sini. Jika Anda mendapatkan error akses KMS, lihat [penyebab dan perbaikannya](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#claude-platform-on-aws).
  </Step>
</Steps>
