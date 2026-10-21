---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws
fetched_at: 2026-10-21T02:21:05.363362Z
sha256: ca40c5e961f856714a5aecc0c826c558777fb70516745061e785738157a3b1f8
---

---
title: Menyiapkan CMEK di Claude Platform on AWS
url: https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws
description: Gunakan kunci AWS KMS sebagai kunci enkripsi yang dikelola pelanggan di Claude Platform on AWS.
---

Panduan ini menunjukkan cara menggunakan kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Untuk Claude Platform atau Claude Enterprise, ikuti [Konfigurasikan AWS KMS untuk CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms) sebagai gantinya.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Akun AWS yang menghosting organisasi Claude Platform on AWS Anda, dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).

* Untuk membuat kunci dari baris perintah, [AWS CLI](https://aws.amazon.com/cli/) terpasang dan terautentikasi.

* Peran **Admin** di Claude Console untuk Claude Platform on AWS. Lihat [Menggunakan Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console).

* Izin berikut untuk principal IAM yang Anda gunakan untuk masuk ke Claude Console:

  * **Masuk:** `aws-external-anthropic:AssumeConsole`
  * **Mendaftarkan kunci:** `aws-external-anthropic:RegisterKey`
  * **Melihat kunci terdaftar:** `aws-external-anthropic:ListKeys` dan `aws-external-anthropic:GetKey`
  * **Melampirkan kunci:** `aws-external-anthropic:UpdateWorkspace` atau `aws-external-anthropic:CreateWorkspace`, ditambah `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci tersebut
  * **Memilih kunci dari daftar (opsional):** `kms:ListKeys` dan `kms:DescribeKey`

  `aws-external-anthropic:RegisterKey`, `aws-external-anthropic:ListKeys`, `aws-external-anthropic:GetKey`, dan `aws-external-anthropic:CreateWorkspace` memiliki cakupan akun. Berikan izin tersebut pada `Resource: "*"`. Lihat [Tindakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys).

## Service principal AWS untuk Anthropic

Kebijakan kunci dalam panduan ini memberikan akses ke kunci Anda kepada "service principal" (principal layanan) AWS berikut:

```text wrap
aws-external-anthropic.amazonaws.com
```

<Warning>
  Gunakan hanya nama principal layanan yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

### Menyiapkan kebijakan kunci

Salin kebijakan ini ke editor teks:

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

Kondisi `EncryptionContext` bersifat opsional. Kondisi ini membatasi kunci hanya untuk workspace yang Anda cantumkan. Untuk menghapusnya, hapus blok `Condition` dari pernyataan `AllowClaudePlatformOnAWSCrypto`.

Jika Anda mempertahankan kondisi tersebut, tambahkan ID compartment setiap workspace sebelum Anda melampirkan kunci ke workspace tersebut. Untuk workspace baru:

1. Buat workspace tanpa kunci.
2. Tambahkan ID compartment-nya ke kebijakan.
3. Lampirkan kunci.

Jika Anda menambahkan kondisi tersebut nanti, cantumkan ID compartment dari setiap workspace yang sudah dilampiri kunci tersebut.

Untuk membatasi kebijakan kunci lebih lanjut, lihat [kondisi `aws:SourceArn` opsional](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#source-arn-condition).

Ganti placeholder:

* **`<AWS_ACCOUNT_ID>`:** [ID akun AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/console-account-id.html) Anda. Untuk menampilkannya dengan AWS CLI, jalankan `aws sts get-caller-identity --query Account --output text`.
* **`<COMPARTMENT_UUID>`:** ID compartment dari workspace tempat Anda melampirkan kunci

<Note>
  **Menemukan ID compartment Anda:** Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) (`platform.claude.com/settings/privacy`). Pilih workspace dari menu dropdown di bagian atas halaman. ID tersebut berada di bawah **Encryption key**, di kolom **Compartment ID**. Anda juga dapat membaca kolom `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve).
</Note>

### Membuat kunci

Buat kunci di akun AWS yang menghosting organisasi Claude Platform on AWS Anda, di region yang sama dengan workspace.

<Tabs>
  <Tab title="AWS Console">
    <Steps>
      <Step title="Buka wizard Create key">
        Buka [konsol AWS KMS](https://console.aws.amazon.com/kms) dan beralih ke region untuk kunci tersebut. Buka **Customer managed keys** dan klik **Create key**.
      </Step>

      <Step title="Konfigurasikan kunci">
        Pastikan opsi-opsi berikut dipilih:

        * **Key type:** Symmetric
        * **Key usage:** Encrypt and decrypt
        * **Advanced options > Key material origin:** KMS
        * **Advanced options > Regionality:** Single-Region key

        Klik **Next**.

        <Frame caption="Kunci simetris, encrypt dan decrypt, single-Region.">
          ![Wizard Create-key di AWS KMS pada langkah Configure key, dengan tipe kunci simetris, penggunaan kunci encrypt dan decrypt, dan kunci single-region dipilih.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
        </Frame>
      </Step>

      <Step title="Tambahkan label">
        Masukkan **Alias** untuk kunci tersebut, seperti `anthropic-cmek`. Klik **Next**.

        <Frame caption="Alias untuk kunci.">
          ![Langkah Add labels di AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
        </Frame>
      </Step>

      <Step title="Tentukan izin administratif kunci">
        Jangan pilih administrator kunci apa pun. Kebijakan kunci Anda sudah memberikan kontrol admin penuh kepada akun AWS Anda. Klik **Next**.

        <Frame caption="Biarkan administrator kunci kosong.">
          ![Langkah Define key administrative permissions di AWS KMS yang mencantumkan peran IAM yang dapat mengelola kunci.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
        </Frame>
      </Step>

      <Step title="Tentukan izin penggunaan kunci">
        Jangan pilih pengguna kunci apa pun, dan jangan tambahkan apa pun di bawah **Other AWS accounts**. Kebijakan kunci Anda sudah memberikan akses yang diperlukan. Klik **Next**.
      </Step>

      <Step title="Edit kebijakan kunci">
        Klik **Edit**. Ganti seluruh kebijakan dengan kebijakan kunci Anda, lalu klik **Next**.
      </Step>

      <Step title="Tinjau">
        Klik **Finish**.
      </Step>

      <Step title="Salin ARN kunci">
        Di **Customer managed keys**, buka kunci baru tersebut dan salin ARN-nya. Anda memerlukan ARN tersebut untuk mendaftarkan kunci.
      </Step>
    </Steps>

    Untuk mengganti kebijakan kunci pada kunci yang sudah ada:

    1. Buka kunci tersebut dan klik tab **Key policy**.
    2. Jika Anda melihat **Switch to policy view**, klik opsi tersebut.
    3. Klik **Edit**.
    4. Ganti JSON dengan kebijakan kunci Anda.
    5. Klik **Save changes**.
  </Tab>

  <Tab title="AWS CLI">
    Simpan kebijakan kunci Anda sebagai `key-policy.json`, lalu buat kunci. Ganti `<REGION>` dengan region kunci tersebut.

    ```bash
    aws kms create-key \
      --region <REGION> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy file://key-policy.json
    ```

    Salin `KeyMetadata.Arn` dari output. Anda memerlukannya untuk mendaftarkan kunci.
  </Tab>
</Tabs>

<Note>
  **Opsional:** Untuk membatasi kedua pernyataan service principal lebih lanjut, tambahkan kondisi `aws:SourceArn` ke masing-masing pernyataan. ARN sumber pada setiap panggilan adalah [ARN workspace](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#service-details), dalam bentuk `arn:aws:aws-external-anthropic:<REGION>:<AWS_ACCOUNT_ID>:workspace/<WORKSPACE_ID>`.

  * **Semua workspace di akun AWS Anda:** `"ArnLike": {"aws:SourceArn": "arn:aws:aws-external-anthropic:*:<AWS_ACCOUNT_ID>:workspace/*"}`
  * **Workspace tertentu:** kondisi yang sama, dengan daftar ARN workspace lengkap sebagai pengganti wildcard
</Note>

## Mendaftarkan kunci dengan Anthropic

Masuk ke Claude Console melalui AWS dengan peran Admin.

<Steps>
  <Step title="Buka pengaturan kunci enkripsi">
    Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy#encryption-keys) (`platform.claude.com/settings/privacy`). Jika Anda tidak melihat **Encryption keys**, pilih **Organization** dari menu dropdown di bagian atas halaman.
  </Step>

  <Step title="Tambahkan kunci">
    Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name**.
  </Step>

  <Step title="Masukkan ARN kunci">
    Anthropic menolak ARN alias dan kunci multi-Region.

    Di **KMS key ARN**, tempelkan ARN kunci. Jika yang muncul justru daftar kunci, pilih kunci Anda, atau klik **Enter ARN manually** lalu tempelkan ARN. Klik **Add**.
  </Step>

  <Step title="Lampirkan kunci ke workspace">
    Melampirkan kunci tidak dapat dibatalkan. Jika memungkinkan, lampirkan kunci ke workspace baru sebelum workspace tersebut menerima permintaan apa pun. Di workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

    Di halaman Data retention, pilih workspace dari menu dropdown di bagian atas halaman. Di bawah **Encryption key**, pilih kunci dan klik **Save**.
  </Step>

  <Step title="Konfirmasi perubahan">
    Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Confirm**.
  </Step>
</Steps>

Proses melampirkan akan memvalidasi kunci. Jika gagal dengan kesalahan akses KMS, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#troubleshoot-validation).

Anda juga dapat memilih kunci saat membuat workspace di Claude Console, jika kebijakan kunci Anda tidak memiliki kondisi `EncryptionContext`.

Untuk mendaftarkan dan melampirkan kunci dengan API sebagai gantinya, lihat [Tindakan IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys). API mengidentifikasi kunci berdasarkan ARN kunci KMS-nya.

## Memecahkan masalah validasi

Jika validasi gagal, penyebab umumnya adalah:

* **Ketidakcocokan kebijakan kunci:** Pastikan kebijakan kunci sesuai dengan yang ada di [Menyiapkan kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws#prepare-the-key-policy). Untuk memeriksa kebijakan kunci, jalankan `aws kms get-key-policy --region <REGION> --key-id <KEY_ARN> --policy-name default`.
* **Ketidakcocokan kondisi:** Pastikan setiap kondisi `EncryptionContext` atau `aws:SourceArn` mencakup workspace ini.
* **Status atau lokasi kunci:** Konfirmasikan bahwa kunci diaktifkan, bersifat single-Region, dan berada di akun AWS serta region yang sama dengan workspace.
* **Izin yang kurang:** Principal yang Anda gunakan untuk masuk memerlukan `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci tersebut.
* **Kebijakan organisasi:** Pastikan tidak ada service control policy atau resource control policy di organisasi AWS Anda yang memblokir service principal atau principal Anda.

Jika proses melampirkan masih gagal, temukan event `kms:` yang ditolak di CloudTrail pada akun pemilik kunci. Event tersebut menunjukkan principal pemanggil dan, untuk panggilan kriptografis, konteks enkripsinya. Setelah Anda memperbaiki penyebabnya, klik **Save** lagi.

## Terraform

Untuk membuat kunci dengan Terraform, gunakan resource `aws_kms_key` dan `aws_kms_alias` dari provider `aws`.
