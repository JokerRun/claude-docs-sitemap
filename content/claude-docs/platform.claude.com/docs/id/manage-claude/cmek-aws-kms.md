---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: ff808d1ebc21b975203a098193db2b434c57773dc7d0be29b7a59a57d61957d4
---

---
title: Mengonfigurasi AWS KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
description: Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with AWS KMS"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (kunci enkripsi yang dikelola pelanggan), atau CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Akun AWS dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Kunci API Admin Anthropic untuk organisasi Anda.
* [AWS CLI](https://aws.amazon.com/cli/) yang telah terinstal dan terautentikasi.

## Amazon Resource Name (ARN) untuk Anthropic

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan IAM role milik Anthropic sebuah kunci KMS yang dapat digunakannya untuk mengenkripsi data. ARN untuk CMEK Anthropic adalah:

```text wrap
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat kunci KMS dengan kebijakan kunci lintas akun">
    Kebijakan kunci memberikan akses lintas akun kepada IAM role milik Anthropic. Tiga pernyataan diperlukan:

    1. **Admin root akun:** pola KMS standar. Akun Anda tetap memegang kendali admin penuh.
    2. **Enkripsi dan dekripsi Anthropic:** tindakan `kms:Encrypt` dan `kms:Decrypt`, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda ("envelope encryption" (enkripsi amplop)).
    3. **Describe Anthropic:** pembacaan metadata yang dilakukan Anthropic saat startup. Izin ini diberikan secara terpisah karena `DescribeKey` tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada tindakan ini akan selalu menolak.

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
                \"kms:EncryptionContext:anthropic:compartment_uuid\": [
                  \"00000000-0000-0000-0000-000000000000\",
                  \"<compartment-uuid>\"
                ]
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

    Kondisi `EncryptionContext` direkomendasikan tetapi opsional. Anthropic selalu menyertakan compartment ID workspace Anda dalam konteks enkripsi, sehingga ciphertext terikat secara kriptografis ke compartment tersebut dalam kondisi apa pun. Menambahkan kondisi ini memberikan "defense-in-depth" (pertahanan berlapis) di lapisan IAM. Untuk memulai tanpanya, hilangkan blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan tambahkan nanti dengan `kms:PutKeyPolicy`.

    <Note>
      **Menemukan compartment ID Anda:** Lokasi compartment ID Anda berbeda antara Claude Platform dan Claude Enterprise. Lihat tab **Claude Platform** dan **Claude Enterprise** di bawah **Daftarkan kunci ke Anthropic**.
    </Note>

    Anda juga dapat membuat kunci dari AWS Console. Pilih kunci simetris dengan penggunaan kunci encrypt and decrypt, kunci single-region, dan asal material kunci KMS. Wizard Create-key menetapkan kebijakan kunci pada langkah **Review**: Jika Anda menambahkan ID akun Anthropic `915198916910` di bawah izin penggunaan kunci di sana, kebijakan yang dihasilkan memberikan tindakan yang lebih luas kepada seluruh akun Anthropic (seperti `kms:ReEncrypt*` dan `kms:GenerateDataKey*`) tanpa kondisi `EncryptionContext`, dan validasi tetap akan berhasil terhadapnya. Untuk menghindari kunci yang terlalu permisif, selesaikan wizard hanya dengan izin administratif, lalu buka tab **Key policy** pada kunci tersebut dan ganti JSON-nya dengan kebijakan yang dibatasi pada role seperti yang ditunjukkan sebelumnya (tiga pernyataan yang dibatasi pada role `anthropic-cmek-client-us`, dengan kondisi `EncryptionContext`).

    <Frame caption="Configure key (konfigurasi kunci): symmetric (simetris), encrypt and decrypt (enkripsi dan dekripsi), single-region key (kunci satu region).">
      ![Wizard Create key AWS KMS pada langkah Configure key, dengan tipe kunci Symmetric, penggunaan kunci Encrypt and decrypt, dan Single-Region key dipilih.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
    </Frame>

    <Frame caption="Tambahkan alias dan deskripsi untuk kunci.">
      ![Langkah Add labels AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
    </Frame>

    <Frame caption="Define key administrative permissions (tentukan izin administratif kunci) (opsional). Akun Anda tetap memegang kendali admin penuh.">
      ![Langkah Define key administrative permissions AWS KMS yang mencantumkan IAM role yang dapat mengelola kunci.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
    </Frame>

    <Frame caption="Jangan tambahkan ID akun Anthropic di sini. Langkah wizard ini menghasilkan kebijakan yang terlalu permisif. Biarkan usage permissions (izin penggunaan) kosong dan edit JSON Key policy (kebijakan kunci) setelah pembuatan (lihat kebijakan kunci sebelumnya).">
      ![Langkah Define key usage permissions AWS KMS dengan ID akun Anthropic dimasukkan di bawah Other AWS accounts.](https://platform.claude.com/docs/images/cmek/aws-usage-permissions.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Note>
      **Menemukan compartment ID Anda:** Setiap workspace memiliki compartment ID yang membatasi cakupan data CMEK-nya. Temukan di Claude Console di bawah **Workspace > Security > Encryption keys** (kolom **Compartment ID**), atau baca kolom `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/admin-api/workspaces/get-workspace). Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci sebelumnya.

      Validasi kunci selalu mengirimkan UUID compartment yang seluruhnya nol (`00000000-0000-0000-0000-000000000000`) sebagai konteks enkripsi, karena validasi berjalan sebelum kunci dilampirkan ke workspace mana pun. Lalu lintas langsung mengirimkan compartment ID dari setiap workspace yang dilampirkan.

      Setiap kondisi `EncryptionContext` harus mengizinkan nilai seluruhnya nol ditambah compartment ID dari setiap workspace tempat kunci dilampirkan. Validasi juga berjalan kembali setiap kali penyiapan kunci dijalankan ulang, jadi pertahankan entri seluruhnya nol secara permanen.

      Untuk melampirkan kunci ke workspace tambahan, tambahkan compartment ID workspace tersebut ke kondisi dengan `kms:PutKeyPolicy` sebelum melampirkan.
    </Note>

    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API.

        <Note>
          Untuk organisasi di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), endpoint kunci eksternal belum tersedia. Sebagai gantinya, daftarkan, validasi, dan lampirkan kunci Anda di Claude Console.
        </Note>

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
              "kms_arn": "<key-arn-from-create-key-step>",
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
        Picu proses bolak-balik enkripsi dan dekripsi terhadap kunci Anda.

        ```bash
        curl -sS -X POST https://api.anthropic.com/v1/organizations/external_keys/ekey_<id>/validate \
          -H "x-api-key: <anthropic-admin-api-key>" \
          -H "anthropic-version: 2023-06-01" \
          -H "content-type: application/json" \
          -d '{}'
        ```

        Respons yang berhasil terlihat seperti ini:

        ```json
        { "type": "external_key_validation", "status": "success", "error": null }
        ```

        Jika validasi gagal, penyebab umumnya adalah:

        * **Ketidakcocokan konteks enkripsi:** Validasi gagal sementara lalu lintas data berfungsi (atau sebaliknya) dengan `AccessDeniedException` yang tidak jelas ketika kondisi `kms:EncryptionContext:anthropic:compartment_uuid` hanya mengizinkan salah satu dari dua nilai yang dikirim Anthropic. Validasi mengirimkan UUID seluruhnya nol (`00000000-0000-0000-0000-000000000000`); lalu lintas langsung mengirimkan compartment ID workspace yang dilampirkan. Pastikan kondisi mencantumkan keduanya. Untuk mengesampingkan kondisi ini sepenuhnya, hapus sementara blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan validasi ulang.
        * **Resource control policies (RCP):** Jika organisasi AWS Anda memiliki RCP yang menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan organisasi Anda, RCP tersebut memblokir role lintas akun Anthropic. RCP memerlukan pengecualian untuk kunci ini atau untuk ARN role Anthropic. Service control policies tidak berlaku di sini, karena tidak dievaluasi untuk principal eksternal yang memanggil melalui kebijakan berbasis sumber daya.
        * **Akses diberikan melalui IAM alih-alih kebijakan kunci:** Akses KMS lintas akun harus diberikan dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Periksa dengan `aws kms get-key-policy --key-id <id> --policy-name default`.
        * **Ketidakcocokan region:** Pastikan region kunci adalah region tempat Anthropic beroperasi untuk tingkat geo yang Anda konfigurasikan.
      </Step>

      <Step title="Lampirkan kunci ke workspace">
        Setelah kunci divalidasi, lampirkan ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan waktu [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

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
  </Tab>

  <Tab title="Claude Enterprise">
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **AWS** dan klik **Continue**, lalu tempelkan Key ARN dari langkah sebelumnya dan klik **Add**. Anthropic memvalidasi kunci dengan proses bolak-balik enkripsi dan dekripsi. Setelah kunci ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK sejak saat itu.

    Langkah detail kunci dalam alur ini menampilkan **Compartment ID** organisasi Anda dengan tombol salin. Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci (lihat langkah Buat kunci KMS di bawah Penyiapan kunci enkripsi); Anda dapat membuka alur ini untuk menyalin ID sebelum membuat kunci. Setelah penyiapan, ID tetap terlihat pada kunci di bawah **Encryption keys**.

    Di Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `aws` dengan resource `aws_kms_key` dan `aws_kms_alias`.
