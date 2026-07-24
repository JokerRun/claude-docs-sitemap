---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: a33f8846405dc470b00d053ae2292efaeb0610a0f9e9f18609a93a5add589d8a
---

# Mengonfigurasi AWS KMS untuk CMEK

Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.

---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with AWS KMS"
```

Panduan ini menjelaskan cara mengonfigurasi kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (kunci enkripsi yang dikelola pelanggan), atau CMEK](/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Akun AWS dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Kunci Admin API Anthropic untuk organisasi Anda.
* [AWS CLI](https://aws.amazon.com/cli/) yang sudah terpasang dan terautentikasi.

## Amazon Resource Name (ARN) untuk Anthropic

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan kunci KMS kepada IAM role Anthropic yang dapat digunakan untuk mengenkripsi data. ARN untuk Anthropic CMEK adalah:

```text wrap
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat kunci KMS dengan kebijakan kunci lintas akun">
    Kebijakan kunci memberikan akses lintas akun kepada IAM role Anthropic. Tiga pernyataan diperlukan:

    1. **Account root admin:** pola KMS standar. Akun Anda mempertahankan kontrol admin penuh.
    2. **Anthropic encrypt and decrypt:** aksi `kms:Encrypt` dan `kms:Decrypt`, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda (envelope encryption).
    3. **Anthropic describe:** pembacaan metadata yang dilakukan Anthropic saat startup. Ini diberikan secara terpisah karena `DescribeKey` tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada aksi ini akan selalu menolak.

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

    Kondisi `EncryptionContext` direkomendasikan tetapi opsional. Anthropic selalu menyertakan compartment ID workspace Anda dalam encryption context, sehingga ciphertext terikat secara kriptografis ke compartment tersebut terlepas dari kondisi ini. Menambahkan kondisi memberikan pertahanan berlapis (defense-in-depth) pada lapisan IAM. Untuk memulai tanpa kondisi tersebut, hilangkan blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan tambahkan nanti dengan `kms:PutKeyPolicy`.

    <Note>
      **Menemukan compartment ID Anda:** Lokasi untuk menemukan compartment ID Anda berbeda antara Claude Platform dan Claude Enterprise. Lihat tab **Claude Platform** dan **Claude Enterprise** di bawah **Daftarkan kunci ke Anthropic**.
    </Note>

    Anda juga dapat membuat kunci dari AWS Console. Pilih kunci simetris dengan penggunaan kunci encrypt dan decrypt, kunci single-region, dan asal materi kunci KMS. Wizard Create-key menerapkan kebijakan kunci pada langkah **Review**-nya: Jika Anda menambahkan ID akun Anthropic `915198916910` di bawah izin penggunaan kunci di sana, kebijakan yang dihasilkan memberikan aksi yang lebih luas kepada seluruh akun Anthropic (seperti `kms:ReEncrypt*` dan `kms:GenerateDataKey*`) tanpa kondisi `EncryptionContext`, dan validasi tetap akan berhasil terhadapnya. Untuk menghindari meninggalkan kunci dengan izin berlebihan, selesaikan wizard hanya dengan izin administratif, lalu buka tab **Key policy** pada kunci tersebut dan ganti JSON dengan kebijakan yang dibatasi pada role seperti yang ditunjukkan sebelumnya (tiga pernyataan yang dibatasi pada role `anthropic-cmek-client-us`, dengan kondisi `EncryptionContext`).

    <Frame caption="Configure key (konfigurasi kunci): symmetric, encrypt and decrypt, single-region key.">
      ![AWS KMS Create key wizard on the Configure key step, with Symmetric key type, Encrypt and decrypt key usage, and Single-Region key selected.](/docs/images/cmek/aws-configure-key.png)
    </Frame>

    <Frame caption="Add labels (tambahkan label): alias dan deskripsi untuk kunci.">
      ![AWS KMS Add labels step with an alias of anthropic-cmek and a description of Anthropic CMEK.](/docs/images/cmek/aws-add-labels.png)
    </Frame>

    <Frame caption="Define key administrative permissions (tentukan izin administratif kunci) (opsional). Akun Anda mempertahankan kontrol admin penuh.">
      ![AWS KMS Define key administrative permissions step listing IAM roles that can administer the key.](/docs/images/cmek/aws-admin-permissions.png)
    </Frame>

    <Frame caption="Jangan tambahkan ID akun Anthropic di sini. Langkah wizard ini menghasilkan kebijakan dengan izin berlebihan. Biarkan usage permissions (izin penggunaan) kosong dan edit JSON Key policy setelah pembuatan (lihat kebijakan kunci sebelumnya).">
      ![AWS KMS Define key usage permissions step with Anthropic's account ID entered under Other AWS accounts.](/docs/images/cmek/aws-usage-permissions.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Note>
      **Menemukan compartment ID Anda:** Setiap workspace memiliki compartment ID yang membatasi cakupan data CMEK-nya. Temukan di Claude Console di bawah **Workspace > Security > Encryption keys** (bidang **Compartment ID**), atau baca bidang `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](/docs/id/api/admin-api/workspaces/get-workspace). Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci sebelumnya.

      Validasi kunci selalu mengirimkan compartment UUID yang seluruhnya nol (`00000000-0000-0000-0000-000000000000`) sebagai encryption context, karena validasi berjalan sebelum kunci dilampirkan ke workspace mana pun. Lalu lintas langsung mengirimkan compartment ID dari setiap workspace yang dilampirkan.

      Setiap kondisi `EncryptionContext` harus mengizinkan nilai seluruhnya nol ditambah compartment ID dari setiap workspace tempat kunci dilampirkan. Validasi juga berjalan kembali setiap kali penyiapan kunci dijalankan ulang, jadi pertahankan entri seluruhnya nol secara permanen.

      Untuk melampirkan kunci ke workspace tambahan, tambahkan compartment ID workspace tersebut ke kondisi dengan `kms:PutKeyPolicy` sebelum melampirkan.
    </Note>

    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API.

        <Note>
          Untuk organisasi di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), endpoint kunci eksternal belum tersedia. Sebagai gantinya, daftarkan, validasi, dan lampirkan kunci Anda di Claude Console.
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
        Picu proses encrypt dan decrypt bolak-balik terhadap kunci Anda.

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

        * **Ketidakcocokan encryption context:** Validasi gagal sementara lalu lintas data berfungsi (atau sebaliknya) dengan `AccessDeniedException` yang tidak jelas ketika kondisi `kms:EncryptionContext:anthropic:compartment_uuid` hanya mengizinkan salah satu dari dua nilai yang dikirim Anthropic. Validasi mengirimkan UUID seluruhnya nol (`00000000-0000-0000-0000-000000000000`); lalu lintas langsung mengirimkan compartment ID dari workspace yang dilampirkan. Pastikan kondisi mencantumkan keduanya. Untuk sepenuhnya mengesampingkan kondisi tersebut, hapus sementara blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan validasi ulang.
        * **Resource control policies (RCPs):** Jika organisasi AWS Anda memiliki RCP yang menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan organisasi Anda, RCP tersebut memblokir role lintas akun Anthropic. RCP memerlukan pengecualian untuk kunci ini atau untuk ARN role Anthropic. Service control policies tidak berlaku di sini, karena tidak dievaluasi untuk principal eksternal yang memanggil melalui kebijakan berbasis sumber daya.
        * **Akses diberikan melalui IAM alih-alih kebijakan kunci:** Akses KMS lintas akun harus diberikan dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Periksa dengan `aws kms get-key-policy --key-id <id> --policy-name default`.
        * **Ketidakcocokan region:** Pastikan region kunci adalah salah satu region tempat Anthropic beroperasi untuk tingkat geo yang Anda konfigurasikan.
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
  </Tab>

  <Tab title="Claude Enterprise">
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **AWS** dan klik **Continue**, lalu tempel Key ARN dari langkah sebelumnya dan klik **Add**. Anthropic memvalidasi kunci dengan proses encrypt dan decrypt bolak-balik. Setelah ditampilkan sebagai terverifikasi, organisasi Anda terlindungi oleh CMEK sejak saat itu.

    Langkah detail kunci dari alur ini menampilkan **Compartment ID** organisasi Anda dengan tombol salin. Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci (lihat langkah Buat kunci KMS di bawah Penyiapan kunci enkripsi); Anda dapat membuka alur untuk menyalin ID sebelum membuat kunci. Setelah penyiapan, ID tetap terlihat pada kunci di bawah **Encryption keys**.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `aws` dengan sumber daya `aws_kms_key` dan `aws_kms_alias`.
