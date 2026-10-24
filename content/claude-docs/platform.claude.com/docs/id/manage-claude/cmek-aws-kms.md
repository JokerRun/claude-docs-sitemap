---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: d764cfddfa028852d6a2fd33c5e2b4e3aae14dd5473fc61ae192187cb3f8e665
---

---
title: Menyiapkan CMEK dengan AWS KMS
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
description: Buat kunci AWS KMS, berikan Anthropic akses ke kunci tersebut, dan gunakan kunci itu di Claude Platform atau Claude Enterprise.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan AWS KMS
```

Jika sidebar Claude Console Anda menampilkan **Account managed by AWS**, ikuti [Menyiapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws) sebagai gantinya.

## Sebelum Anda mulai

Di Claude:

* Kunci enkripsi yang dikelola pelanggan (CMEK) telah [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/cmek#availability).
* Anda memiliki ID organisasi Anthropic Anda, yaitu UUID tanpa awalan `org_`. Salin ID tersebut dari [Organization](https://platform.claude.com/settings/organization) di Claude Console, atau dari **Organization settings > Organization and access** di claude.ai. Siapa pun yang membuat kunci memerlukannya.
* Anda adalah Organization Admin di Claude Platform, atau Owner atau Primary Owner di Claude Enterprise.
* Di Claude Platform, Anda memiliki workspace yang [menyimpan data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention), idealnya workspace baru, karena [data yang sudah ada tetap berada di bawah kunci milik Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).
* Di Claude Enterprise, Anda mengetahui [fitur mana yang dinonaktifkan atau berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

Di AWS:

* Anda dapat membuat kunci AWS KMS dan menetapkan kebijakan kuncinya (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Setiap pembatasan IP pada akses AWS KMS mengizinkan [alamat IP keluar Anthropic](https://platform.claude.com/docs/id/api/ip-addresses#outbound-ip-addresses).

## Di AWS: buat kunci

Setelah **Verify** atau **Add** gagal, lihat [perbaikan untuk AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#aws-kms).

### Tulis kebijakan kunci

Kebijakan ini memberikan peran IAM Anthropic akses ke kunci Anda. Gunakan hanya ARN peran yang dipublikasikan di halaman ini, jangan pernah ARN yang dikirim melalui email atau chat. Salin kebijakan ke editor teks:

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
        }
      }
    },
    {
      "Sid": "AllowAnthropicCMEKDescribe",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
      },
      "Action": "kms:DescribeKey",
      "Resource": "*"
    }
  ]
}
```

Ganti `<AWS_ACCOUNT_ID>` dengan [ID akun AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/console-account-id.html) Anda dan `<ORGANIZATION_UUID>` dengan [ID organisasi Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#prerequisites) Anda. Pertahankan kondisi `kms:EncryptionContext:anthropic:org_uuid`, jika tidak, verifikasi akan gagal.

Anda juga dapat [membatasi kunci ke workspace tertentu](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces) dengan mencantumkan ID kompartemen workspace tersebut. Jika Anda mengganti kebijakan pada kunci yang sudah melindungi data Claude, [tambahkan satu pernyataan kebijakan lagi](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#existing-data).

### Buat kunci

Anda dapat membuat kunci di region komersial AWS mana pun. Untuk latensi terendah, gunakan `us-east-2`.

Untuk menggunakan kunci yang sudah Anda miliki di AWS KMS, [ganti kebijakan kuncinya](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces#replace-the-key-policy).

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

Setiap pemeriksaan kunci di Claude menambahkan empat error access-denied yang memang diharapkan ke CloudTrail. Anda dapat [menyaringnya](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cloudtrail).

## Di Claude: tambahkan dan lampirkan kunci

Untuk membuat skrip bagian ini di Claude Platform, [gunakan Admin API](https://platform.claude.com/docs/id/manage-claude/cmek-admin-api) sebagai gantinya.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Di Claude Console, buka [Encryption keys](https://platform.claude.com/settings/privacy#encryption-keys) di halaman Data retention. Jika bagian tersebut tidak ada, pilih **Organization** dari menu dropdown di bagian atas.
      </Step>

      <Step title="Tambahkan kunci">
        Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name**, pilih **AWS KMS**, lalu klik **Continue**.
      </Step>

      <Step title="Masukkan ARN kunci">
        Periksa bahwa [kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) Anda berisi **Organization ID for the key policy** yang ditampilkan di kotak dialog. Tempelkan ARN kunci ke **KMS key ARN** lalu klik **Add**.
      </Step>

      <Step title="Verifikasi kunci">
        Di daftar **Encryption keys**, klik **Verify** di samping kunci. **Connected** muncul saat pemeriksaan berhasil. Jika yang muncul justru **Connection failed**, lihat [Memecahkan masalah CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting).
      </Step>

      <Step title="Lampirkan kunci ke workspace">
        <Warning>
          Melampirkan kunci [tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Anda tidak dapat melepasnya dari workspace atau menggantinya. Jika kunci dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya.
        </Warning>

        1. Di bagian atas halaman Data retention, pilih workspace dari menu dropdown.
        2. Di bawah **Encryption key**, pilih kunci lalu klik **Save**.
        3. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Confirm**.

        Anda akan melihat **Workspace settings updated.** Setelah kunci [mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), audit log penyedia cloud Anda menampilkan panggilan Anthropic ke kunci tersebut.

        Dalam [organisasi ZDR](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#zdr-organizations), setelah Anda memilih workspace, pilih **Standard data retention** agar **Encryption key** muncul. Setelah Anda mengklik **Save**, klik **Accept** pada ketentuan retensi data.
      </Step>
    </Steps>
  </Tab>

  <Tab title="Claude Enterprise">
    Di Claude Enterprise, CMEK berlaku untuk seluruh organisasi, dan Anda hanya dapat menambahkan satu kunci.

    <Warning>
      Menambahkan kunci [tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Anda tidak dapat melepasnya dari organisasi atau menggantinya. Jika kunci tersebut dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya.
    </Warning>

    Menambahkan kunci tersebut [menonaktifkan atau mengubah beberapa fitur](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed) untuk setiap pengguna. Untuk mencoba CMEK terlebih dahulu, gunakan organisasi terpisah.

    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Buka [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) dan temukan **Encryption keys**.
      </Step>

      <Step title="Tambahkan kunci">
        Klik **Add key**. Masukkan **Display name** dan pilih **AWS KMS**. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Continue**.
      </Step>

      <Step title="Masukkan ARN kunci">
        Periksa bahwa [kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) Anda berisi **Organization ID for the key policy** yang ditampilkan di kotak dialog. Tempelkan ARN kunci ke **KMS key ARN** lalu klik **Add**.
      </Step>

      <Step title="Konfirmasi bahwa kunci telah ditambahkan">
        Pemeriksaan dapat memakan waktu hingga 30 detik. Saat **Encryption key configured.** muncul, klik **Done**. Jika yang muncul justru **The encryption key couldn’t be added.**, [temukan penyebabnya dan coba lagi](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#claude-ai-add-fails).

        Kunci Anda melindungi data yang ditulis sejak saat itu. Beri tahu pengguna Anda [fitur mana yang berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).
      </Step>
    </Steps>
  </Tab>
</Tabs>
