---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 6e07c813ff413a7917f8b40acd7ea4cdee7d70707fdab4023f4c484a431efe3c
---

# Mengonfigurasi AWS KMS untuk CMEK

Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.

---

```bash title="Configure with the /claude-api skill in Claude Code"
claude "/claude-api help me configure a customer-managed encryption key with AWS KMS"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai "customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau [CMEK](/docs/id/manage-claude/cmek), untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat \{#prerequisites}

- Akun AWS dengan izin untuk membuat kunci KMS dan mengatur kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
- Kunci Admin API Anthropic untuk organisasi Anda.
- [AWS CLI](https://aws.amazon.com/cli/) yang sudah terinstal dan terautentikasi.

## Amazon Resource Name (ARN) untuk Anthropic \{#amazon-resource-name-arn-for-anthropic}

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan IAM role milik Anthropic sebuah kunci KMS yang dapat digunakan untuk mengenkripsi data. ARN untuk CMEK Anthropic adalah:

```text
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi \{#encryption-key-setup}

<Steps>
  <Step title="Buat kunci KMS dengan kebijakan kunci lintas akun">
    Kebijakan kunci memberikan akses lintas akun kepada IAM role milik Anthropic. Tiga pernyataan diperlukan:

    1. **Account root admin:** pola KMS standar. Akun Anda tetap memegang kontrol admin penuh.
    2. **Anthropic encrypt and decrypt:** tindakan `kms:Encrypt` dan `kms:Decrypt`, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda (envelope encryption).
    3. **Anthropic describe:** pembacaan metadata yang dilakukan Anthropic saat startup. Ini diberikan secara terpisah karena `DescribeKey` tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada tindakan ini akan selalu menolak.

    ```bash
    export YOUR_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

    aws kms create-key \
      --region <region> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [
          {
            \"Sid\": \"AccountRootAdmin\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::${YOUR_ACCOUNT}:root\"},
            \"Action\": \"kms:*\",
            \"Resource\": \"*\"
          },
          {
            \"Sid\": \"AllowAnthropicCMEKCrypto\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::915198916910:role/anthropic-cmek-client-us\"},
            \"Action\": [\"kms:Encrypt\", \"kms:Decrypt\"],
            \"Resource\": \"*\",
            \"Condition\": {
              \"StringEquals\": {
                \"kms:EncryptionContext:anthropic:compartment_uuid\": \"<compartment-uuid>\"
              }
            }
          },
          {
            \"Sid\": \"AllowAnthropicCMEKDescribe\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::915198916910:role/anthropic-cmek-client-us\"},
            \"Action\": \"kms:DescribeKey\",
            \"Resource\": \"*\"
          }
        ]
      }"
    ```

    Catat `KeyMetadata.Arn` dari output. Anda memerlukannya saat mendaftarkan kunci pada langkah berikutnya.

    Kondisi `EncryptionContext` direkomendasikan tetapi bersifat opsional. Anthropic selalu menyertakan compartment ID workspace Anda dalam encryption context, sehingga ciphertext secara kriptografis terikat ke compartment tersebut terlepas dari kondisi ini. Menambahkan kondisi ini memberikan pertahanan berlapis (defense-in-depth) di lapisan IAM. Untuk memulai tanpa kondisi ini, hilangkan blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan tambahkan nanti dengan `kms:PutKeyPolicy`.

    <Note>
      **Menemukan compartment ID Anda:** Setiap workspace memiliki compartment ID yang membatasi cakupan data CMEK-nya. Temukan di Claude Console pada **Workspace > Security > Encryption keys** (kolom **Compartment ID**), atau baca kolom `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](/docs/id/api/admin-api/workspaces/get-workspace). Substitusikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci di atas. Anthropic juga mengirimkannya sebagai encryption context saat memvalidasi kunci, sehingga nilai kondisi harus cocok agar validasi berhasil.
    </Note>

    Anda juga dapat membuat kunci dari AWS Console. Pilih kunci simetris dengan penggunaan kunci encrypt and decrypt, kunci single-region, dan asal materi kunci KMS. Wizard Create-key menetapkan kebijakan kunci pada langkah **Review**: jika Anda menambahkan ID akun Anthropic `915198916910` di bawah key usage permissions di sana, kebijakan yang dihasilkan memberikan seluruh akun Anthropic tindakan yang lebih luas (seperti `kms:ReEncrypt*` dan `kms:GenerateDataKey*`) tanpa kondisi `EncryptionContext`, dan validasi tetap akan berhasil terhadapnya. Untuk menghindari meninggalkan kunci dengan izin berlebihan, selesaikan wizard hanya dengan izin administratif, lalu buka tab **Key policy** pada kunci tersebut dan ganti JSON dengan kebijakan yang dibatasi ke role seperti yang ditunjukkan di atas (tiga pernyataan yang dibatasi ke role `anthropic-cmek-client-us`, dengan kondisi `EncryptionContext`).

    <Frame caption="Configure key (konfigurasi kunci): symmetric, encrypt and decrypt, single-region key.">
      ![Wizard Create key AWS KMS pada langkah Configure key, dengan tipe kunci Symmetric, penggunaan kunci Encrypt and decrypt, dan Single-Region key dipilih.](/docs/images/cmek/aws-configure-key.png)
    </Frame>

    <Frame caption="Tambahkan alias dan deskripsi untuk kunci.">
      ![Langkah Add labels AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](/docs/images/cmek/aws-add-labels.png)
    </Frame>

    <Frame caption="Define key administrative permissions (tentukan izin administratif kunci) — opsional. Akun Anda tetap memegang kontrol admin penuh.">
      ![Langkah Define key administrative permissions AWS KMS yang mencantumkan IAM role yang dapat mengelola kunci.](/docs/images/cmek/aws-admin-permissions.png)
    </Frame>

    <Frame caption="Jangan tambahkan ID akun Anthropic di sini. Langkah wizard ini menghasilkan kebijakan dengan izin berlebihan. Biarkan usage permissions kosong dan edit JSON Key policy setelah pembuatan (lihat di atas).">
      ![Langkah Define key usage permissions AWS KMS ditampilkan sebagai anti-pola: menambahkan ID akun Anthropic 915198916910 di bawah Other AWS accounts di sini menghasilkan kebijakan dengan izin berlebihan. Lewati langkah ini dan biarkan kosong.](/docs/images/cmek/aws-usage-permissions.png)
    </Frame>
  </Step>

  <Step title="Daftarkan kunci ke Anthropic">
    Buat konfigurasi kunci eksternal melalui Admin API.

    ```bash
    curl -sS https://api.anthropic.com/v1/organizations/external_keys \
      -H "x-api-key: <anthropic-admin-api-key>" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d '{
        "display_name": "<friendly-name>",
        "geo": "us",
        "provider_config": {
          "type": "aws",
          "kms_arn": "<key-arn-from-step-1>",
          "role_arn": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
        }
      }'
    ```

    Respons berisi ID kunci eksternal:

    ```json
    {
      "type": "external_key",
      "id": "ekey_<id>",
      "display_name": "<friendly-name>"
    }
    ```
  </Step>

  <Step title="Validasi kunci">
    Picu proses encrypt dan decrypt bolak-balik terhadap kunci Anda.

    ```bash
    curl -sS -X POST https://api.anthropic.com/v1/organizations/external_keys/ekey_<id>/validate \
      -H "x-api-key: <anthropic-admin-api-key>" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" -d '{}'
    ```

    Respons yang berhasil terlihat seperti ini:

    ```json
    { "type": "external_key_validation", "status": "success", "error": null }
    ```

    Jika validasi gagal, penyebab umumnya adalah:

    - **Ketidakcocokan encryption context:** jika Anda mempertahankan kondisi `EncryptionContext` dalam kebijakan kunci, pastikan Anda telah mengganti `<compartment-uuid>` dengan compartment ID workspace Anda yang sebenarnya (lihat langkah 1). Nilai yang salah atau belum disubstitusi membuat KMS mengembalikan `AccessDeniedException` yang tidak jelas. Untuk mengesampingkan kemungkinan ini, hapus sementara blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan validasi ulang.
    - **Resource control policies (RCP):** jika organisasi AWS Anda memiliki RCP yang menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan org Anda, RCP tersebut memblokir role lintas akun milik Anthropic. RCP memerlukan pengecualian untuk kunci ini atau untuk ARN role Anthropic. Service control policies tidak berlaku di sini, karena tidak dievaluasi untuk principal eksternal yang memanggil melalui kebijakan berbasis sumber daya.
    - **Akses diberikan melalui IAM alih-alih kebijakan kunci:** akses KMS lintas akun harus diberikan dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Periksa dengan `aws kms get-key-policy --key-id <id> --policy-name default`.
    - **Ketidakcocokan region:** pastikan region kunci adalah salah satu region tempat Anthropic beroperasi untuk tingkat geo yang Anda konfigurasikan.
  </Step>

  <Step title="Lampirkan kunci ke workspace">
    ```bash
    curl -sS -X POST https://api.anthropic.com/v1/organizations/workspaces/<workspace-id> \
      -H "x-api-key: <anthropic-admin-api-key>" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d '{
        "external_key_id": "ekey_<id>"
      }'
    ```
  </Step>
</Steps>

## Terraform \{#terraform}

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `aws` dengan sumber daya `aws_kms_key` dan `aws_kms_alias`.