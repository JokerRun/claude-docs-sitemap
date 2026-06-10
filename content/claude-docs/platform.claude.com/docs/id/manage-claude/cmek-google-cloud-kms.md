---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 36616e364bf084ac96f5a1d0a9d569ed429d5b29166536e580e9f1b9c4fbbe55
---

# Mengonfigurasi Google Cloud KMS untuk CMEK

Gunakan Google Cloud KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.

---

```bash title="Configure with the /claude-api skill in Claude Code"
claude "/claude-api help me configure a customer-managed encryption key with Google Cloud KMS"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci Google Cloud KMS sebagai "customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau [CMEK](/docs/id/manage-claude/cmek), untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat \{#prerequisites}

- Proyek Google Cloud dengan penagihan yang diaktifkan.
- Cloud KMS API diaktifkan (`cloudkms.googleapis.com`).
- Izin untuk membuat key ring dan kunci KMS, serta untuk mengatur kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau yang setara).
- Kunci Admin API Anthropic untuk organisasi Anda.
- [`gcloud` CLI](https://cloud.google.com/cli) terinstal dan terautentikasi.
- **Data Access audit logs** Cloud KMS diaktifkan untuk proyek tersebut (IAM & Admin > Audit Logs > Cloud Key Management Service, dengan `DATA_READ` dan `DATA_WRITE`). Log ini nonaktif secara default; tanpa log ini, operasi enkripsi dan dekripsi Anthropic tidak menghasilkan entri apa pun di Cloud Logging.

## Email akun layanan Anthropic \{#anthropic-service-account-email}

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan akun layanan Anthropic sebuah kunci yang dapat digunakan untuk mengenkripsi data. Email akun layanan untuk CMEK Anthropic adalah:

```text
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

<Warning>
  Gunakan hanya email akun layanan yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

<Note>
  **Domain restricted sharing:** Jika proyek Anda berada di bawah organisasi Google Cloud yang menerapkan `constraints/iam.allowedPolicyMemberDomains`, binding IAM di bawah ini akan ditolak karena akun layanan Anthropic berada di luar organisasi Anda. Anda memerlukan pengecualian tingkat proyek pada batasan tersebut, atau menambahkan ID pelanggan Cloud Identity milik Anthropic (format `C0xxxxxxxx`) ke daftar yang diizinkan. Hubungi Anthropic untuk mendapatkan ID pelanggan jika diperlukan.
</Note>

## Penyiapan kunci enkripsi \{#encryption-key-setup}

<Steps>
  <Step title="Buat atau pilih key ring">
    Lewati langkah ini jika Anda sudah memiliki key ring yang dapat digunakan kembali. Key ring bersifat regional. Pilih lokasi AS dengan satu region seperti `us-east5` yang sesuai dengan geografi Anthropic yang sedang Anda konfigurasi. Lokasi multi-region seperti `us` dan `global` tidak didukung.

    ```bash
    gcloud kms keyrings create <your-keyring-name> \
      --project=<your-project-id> \
      --location=<region>
    ```
  </Step>

  <Step title="Buat kunci kripto">
    Buat kunci simetris dengan tujuan `ENCRYPT_DECRYPT`. Perlindungan HSM sangat direkomendasikan: kunci HSM Cloud KMS telah divalidasi FIPS 140-2 Level 3, dan selisih biayanya dibandingkan kunci perangkat lunak tergolong kecil.

    ```bash
    gcloud kms keys create <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --purpose=encryption \
      --protection-level=hsm
    ```

    Untuk perlindungan perangkat lunak, hilangkan `--protection-level=hsm`. Tidak ada hal lain dalam panduan ini yang berubah.

    Anda juga dapat membuat kunci dari Google Cloud Console. Buka key ring, klik **Create key**, pilih **Generated key**, atur tujuan dan algoritma ke symmetric encrypt and decrypt, lalu pilih **HSM** di bagian protection level.

    <Frame caption="Buat kunci symmetric encrypt/decrypt yang dilindungi HSM.">
      ![Halaman Create key Google Cloud KMS dengan tingkat perlindungan HSM dan tujuan Symmetric encrypt/decrypt.](/docs/images/cmek/gcp-create-key.png)
    </Frame>
  </Step>

  <Step title="Berikan akses kunci kepada akun layanan Anthropic">
    Dua binding IAM tingkat kunci diperlukan. Keduanya dicakupkan ke satu kunci kripto saja, bukan ke seluruh proyek atau seluruh key ring.

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

    Dari Console, pilih kunci tersebut, buka panel **Permissions**, klik **Grant access**, lalu tambahkan akun layanan dengan kedua peran Cloud KMS CryptoKey Encrypter/Decrypter dan Cloud KMS Viewer. Pastikan Anda berada di halaman permissions milik kunci tersebut, bukan key ring atau proyek, sehingga pemberian akses dicakupkan hanya ke kunci ini.

    <Frame caption="Berikan kedua peran kepada akun layanan Anthropic, dicakupkan ke kunci tersebut.">
      ![Dialog Grant access Google Cloud yang menambahkan akun layanan Anthropic dengan peran Cloud KMS CryptoKey Encrypter/Decrypter dan Cloud KMS Viewer.](/docs/images/cmek/gcp-grant-access.png)
    </Frame>
  </Step>

  <Step title="Catat nama resource lengkap kunci">
    Anda meneruskan nama ini ke Anthropic saat mendaftarkan kunci. Formatnya adalah:

    ```text
    projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>
    ```

    Ambil dengan perintah:

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

  <Step title="Daftarkan kunci ke Anthropic">
    Buat konfigurasi kunci eksternal melalui Admin API, menggunakan nama resource dari langkah sebelumnya.

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
    Picu proses enkripsi dan dekripsi bolak-balik terhadap kunci Anda.

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

    - **VPC Service Controls:** jika perimeter layanan melindungi Cloud KMS di proyek Anda, tambahkan Anthropic ke access level pada perimeter tersebut (atau kecualikan proyek kunci) agar Anthropic dapat menjangkau kunci tersebut.
    - **Domain restricted sharing:** kebijakan organisasi `constraints/iam.allowedPolicyMemberDomains` dapat menghapus binding akun layanan Anthropic (lihat catatan di atas). Pastikan binding tersebut ada dengan `gcloud kms keys get-iam-policy <your-key-name> --project=<your-project-id> --location=<region> --keyring=<your-keyring-name>`.
    - **Versi kunci yang dinonaktifkan atau dihancurkan:** pastikan versi utama kunci diaktifkan, dan tidak dinonaktifkan, dijadwalkan untuk dihancurkan, atau sudah dihancurkan.
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

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `google` dengan resource `google_kms_key_ring`, `google_kms_crypto_key`, dan `google_kms_crypto_key_iam_member`.