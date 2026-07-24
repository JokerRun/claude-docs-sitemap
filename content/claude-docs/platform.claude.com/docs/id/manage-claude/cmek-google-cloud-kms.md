---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 4ee407386390d6d31567f25cca586009d02b8e7a22a19ff074deb57dc24944e0
---

# Mengonfigurasi Google Cloud KMS untuk CMEK

Gunakan Google Cloud KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.

---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Google Cloud KMS"
```

Panduan ini menjelaskan cara mengonfigurasi kunci Google Cloud KMS sebagai [customer-managed encryption key (kunci enkripsi yang dikelola pelanggan), atau CMEK](/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Proyek Google Cloud dengan penagihan yang diaktifkan.
* Cloud KMS API yang diaktifkan (`cloudkms.googleapis.com`).
* Izin untuk membuat key ring dan kunci KMS, serta untuk menetapkan kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau yang setara).
* Kunci Admin API Anthropic untuk organisasi Anda.
* [`gcloud` CLI](https://cloud.google.com/cli) yang sudah terpasang dan terautentikasi.
* **Data Access audit logs** Cloud KMS yang diaktifkan untuk proyek tersebut (IAM & Admin > Audit Logs > Cloud Key Management Service, dengan `DATA_READ` dan `DATA_WRITE`). Ini nonaktif secara default; tanpanya, operasi enkripsi dan dekripsi Anthropic tidak menghasilkan entri apa pun di Cloud Logging.

## Email akun layanan Anthropic

Agar Anthropic menggunakan kunci enkripsi Anda, Anda harus memberikan akun layanan Anthropic sebuah kunci yang dapat digunakannya untuk mengenkripsi data. Email akun layanan untuk Anthropic CMEK adalah:

```text wrap
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

<Warning>
  Gunakan hanya email akun layanan yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

<Note>
  **Domain restricted sharing:** Jika proyek Anda berada di bawah organisasi Google Cloud yang memberlakukan `constraints/iam.allowedPolicyMemberDomains`, binding IAM berikut akan ditolak karena akun layanan Anthropic berada di luar organisasi Anda. Anda memerlukan pengecualian tingkat proyek pada constraint tersebut, atau menambahkan ID pelanggan Cloud Identity Anthropic (format `C0xxxxxxxx`) ke daftar yang diizinkan. Hubungi Anthropic untuk mendapatkan ID pelanggan jika diperlukan.
</Note>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat atau pilih key ring">
    Lewati langkah ini jika Anda sudah memiliki key ring yang dapat digunakan kembali. Key ring bersifat regional. Pilih lokasi single-region AS seperti `us-east5` yang sesuai dengan geografi Anthropic yang Anda konfigurasikan. Lokasi multi-region seperti `us` dan `global` tidak didukung.

    ```bash
    gcloud kms keyrings create <your-keyring-name> \
      --project=<your-project-id> \
      --location=<region>
    ```
  </Step>

  <Step title="Buat crypto key">
    Buat kunci simetris dengan tujuan `ENCRYPT_DECRYPT`. Anthropic sangat merekomendasikan perlindungan HSM: kunci HSM Cloud KMS tervalidasi FIPS 140-2 Level 3, dan selisih biayanya dibandingkan kunci perangkat lunak cukup kecil.

    ```bash
    gcloud kms keys create <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --purpose=encryption \
      --protection-level=hsm
    ```

    Untuk perlindungan perangkat lunak sebagai gantinya, hilangkan `--protection-level=hsm`. Tidak ada hal lain dalam panduan ini yang berubah.

    Anda juga dapat membuat kunci dari Google Cloud Console. Buka key ring, klik **Create key**, pilih **Generated key**, atur tujuan dan algoritma ke symmetric encrypt dan decrypt, lalu pilih **HSM** di bawah protection level.

    <Frame caption="Buat kunci symmetric encrypt/decrypt yang dilindungi HSM.">
      ![Halaman Create key Google Cloud KMS dengan tingkat perlindungan HSM dan tujuan Symmetric encrypt/decrypt.](/docs/images/cmek/gcp-create-key.png)
    </Frame>
  </Step>

  <Step title="Berikan akses akun layanan Anthropic ke kunci">
    Dua binding IAM tingkat kunci diperlukan. Keduanya dibatasi pada satu crypto key, bukan seluruh proyek atau seluruh keyring.

    Encrypt dan decrypt, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda (envelope encryption):

    ```bash
    gcloud kms keys add-iam-policy-binding <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
      --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
    ```

    Viewer, untuk pembacaan metadata (`cryptoKeys.get`) yang dilakukan Anthropic saat startup untuk memvalidasi tujuan dan algoritma kunci:

    ```bash
    gcloud kms keys add-iam-policy-binding <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
      --role=roles/cloudkms.viewer
    ```

    Dari Console, pilih kunci, buka panel **Permissions**, klik **Grant access**, dan tambahkan akun layanan dengan kedua peran Cloud KMS CryptoKey Encrypter/Decrypter dan Cloud KMS Viewer. Pastikan Anda berada di halaman izin kunci, bukan key ring atau proyek, sehingga pemberian akses hanya dibatasi pada kunci ini saja.

    <Frame caption="Berikan akun layanan Anthropic kedua peran, dibatasi pada kunci.">
      ![Dialog Grant access dengan akun layanan Anthropic yang diberi peran Cloud KMS CryptoKey Encrypter/Decrypter dan Viewer.](/docs/images/cmek/gcp-grant-access.png)
    </Frame>
  </Step>

  <Step title="Catat nama resource kunci lengkap">
    Anda meneruskan ini ke Anthropic saat Anda mendaftarkan kunci. Formatnya adalah:

    ```text wrap
    projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>
    ```

    Ambil dengan:

    ```bash
    gcloud kms keys describe <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --format="value(name)"
    ```

    Dari Console, buka halaman detail kunci dan klik **Copy resource name**.

    <Frame caption="Salin nama resource lengkap kunci dari menu tindakan.">
      ![Detail key ring Google Cloud dengan tindakan Copy resource name yang disorot di menu tindakan kunci.](/docs/images/cmek/gcp-copy-resource-name.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API, menggunakan nama resource dari langkah Catat nama resource kunci lengkap di bawah Penyiapan kunci enkripsi.

        ```bash
        curl -sS https://api.anthropic.com/v1/organizations/external_keys \
          -H "x-api-key: <anthropic-admin-api-key>" \
          -H "anthropic-version: 2023-06-01" \
          -H "content-type: application/json" \
          -d '{
            "display_name": "<friendly-name>",
            "geo": "us",
            "provider_config": {
              "type": "gcp",
              "key_name": "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
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
        Picu putaran enkripsi dan dekripsi terhadap kunci Anda.

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

        * **VPC Service Controls:** jika service perimeter melindungi Cloud KMS di proyek Anda, tambahkan Anthropic ke access level pada perimeter tersebut (atau kecualikan proyek kunci) agar Anthropic dapat menjangkau kunci.
        * **Domain restricted sharing:** kebijakan organisasi `constraints/iam.allowedPolicyMemberDomains` dapat menghapus binding akun layanan Anthropic (lihat catatan sebelumnya). Konfirmasikan bahwa binding tersebut ada dengan `gcloud kms keys get-iam-policy <your-key-name> --project=<your-project-id> --location=<region> --keyring=<your-keyring-name>`.
        * **Versi kunci dinonaktifkan atau dihancurkan:** konfirmasikan bahwa versi utama kunci diaktifkan, dan tidak dinonaktifkan, dijadwalkan untuk dihancurkan, atau sudah dihancurkan.
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
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Google Cloud**, tempelkan nama resource kunci lengkap dari langkah sebelumnya, dan klik **Continue**. Anthropic memvalidasi kunci dengan putaran enkripsi dan dekripsi. Setelah ditampilkan sebagai terverifikasi, organisasi Anda terlindungi CMEK sejak saat itu.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `google` dengan resource `google_kms_key_ring`, `google_kms_crypto_key`, dan `google_kms_crypto_key_iam_member`.
