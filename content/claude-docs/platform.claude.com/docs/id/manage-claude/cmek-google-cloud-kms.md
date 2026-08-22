---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 96d552bf1bcd9924de1020b2b2a0bd26e3f85c30316ee784d03b69c8edf0c124
---

---
title: Mengonfigurasi Google Cloud KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
description: Gunakan Google Cloud KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Google Cloud KMS"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci Google Cloud KMS sebagai ["customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Proyek Google Cloud dengan penagihan yang diaktifkan.
* Cloud KMS API diaktifkan (`cloudkms.googleapis.com`).
* Izin untuk membuat key ring dan kunci KMS, serta untuk menetapkan kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau yang setara).
* Kunci API Admin Anthropic untuk organisasi Anda.
* [CLI `gcloud`](https://cloud.google.com/cli) terinstal dan terautentikasi.
* **Data Access audit logs** Cloud KMS diaktifkan untuk proyek (IAM & Admin > Audit Logs > Cloud Key Management Service, dengan `DATA_READ` dan `DATA_WRITE`). Log ini nonaktif secara default; tanpanya, operasi enkripsi dan dekripsi Anthropic tidak menghasilkan entri apa pun di Cloud Logging.

## Email service account Anthropic

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan service account Anthropic sebuah kunci yang dapat digunakannya untuk mengenkripsi data. Email service account untuk CMEK Anthropic adalah:

```text wrap
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

<Warning>
  Gunakan hanya email service account yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

<Note>
  **Domain restricted sharing:** Jika proyek Anda berada di bawah organisasi Google Cloud yang menerapkan `constraints/iam.allowedPolicyMemberDomains`, binding IAM berikut akan ditolak karena service account Anthropic berada di luar organisasi Anda. Anda memerlukan pengecualian tingkat proyek pada constraint tersebut, atau menambahkan ID pelanggan Cloud Identity Anthropic (format `C0xxxxxxxx`) ke daftar yang diizinkan. Hubungi Anthropic untuk mendapatkan ID pelanggan jika diperlukan.
</Note>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat atau pilih key ring">
    Lewati langkah ini jika Anda sudah memiliki key ring untuk digunakan kembali. Key ring bersifat regional. Pilih lokasi US region tunggal seperti `us-east5` yang sesuai dengan geografi Anthropic yang Anda konfigurasikan. Lokasi multi-region seperti `us` dan `global` tidak didukung.

    ```bash
    gcloud kms keyrings create <your-keyring-name> \
      --project=<your-project-id> \
      --location=<region>
    ```
  </Step>

  <Step title="Buat crypto key">
    Buat kunci simetris dengan tujuan `ENCRYPT_DECRYPT`. Anthropic sangat merekomendasikan perlindungan HSM: kunci HSM Cloud KMS tervalidasi FIPS 140-2 Level 3, dan selisih biayanya dibandingkan kunci perangkat lunak kecil.

    ```bash
    gcloud kms keys create <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --purpose=encryption \
      --protection-level=hsm
    ```

    Untuk perlindungan perangkat lunak sebagai gantinya, hilangkan `--protection-level=hsm`. Tidak ada hal lain dalam panduan ini yang berubah.

    Anda juga dapat membuat kunci dari Google Cloud Console. Buka key ring, klik **Create key**, pilih **Generated key**, atur tujuan dan algoritma ke symmetric encrypt and decrypt, lalu pilih **HSM** di bawah protection level.

    <Frame caption="Buat kunci symmetric encrypt/decrypt (enkripsi/dekripsi simetris) yang dilindungi HSM.">
      ![Halaman Create key Google Cloud KMS dengan protection level HSM dan tujuan Symmetric encrypt/decrypt.](https://platform.claude.com/docs/images/cmek/gcp-create-key.png)
    </Frame>
  </Step>

  <Step title="Berikan akses ke kunci kepada service account Anthropic">
    Diperlukan dua binding IAM tingkat kunci. Keduanya dicakupkan pada satu crypto key saja, bukan seluruh proyek atau seluruh key ring.

    Encrypt dan decrypt, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi data key yang melindungi data workspace Anda ("envelope encryption" (enkripsi amplop)):

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

    Dari Console, pilih kunci, buka panel **Permissions**, klik **Grant access**, dan tambahkan service account dengan peran Cloud KMS CryptoKey Encrypter/Decrypter dan Cloud KMS Viewer. Pastikan Anda berada di halaman permissions milik kunci, bukan key ring atau proyek, sehingga pemberian akses hanya dicakupkan pada kunci ini.

    <Frame caption="Berikan kedua peran kepada service account Anthropic melalui Grant access (berikan akses), dicakupkan pada kunci.">
      ![Dialog Grant access dengan service account Anthropic yang diberi peran Cloud KMS CryptoKey Encrypter/Decrypter dan Viewer.](https://platform.claude.com/docs/images/cmek/gcp-grant-access.png)
    </Frame>
  </Step>

  <Step title="Catat nama resource lengkap kunci">
    Anda memberikan ini kepada Anthropic saat mendaftarkan kunci. Formatnya adalah:

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

    <Frame caption="Salin nama resource lengkap kunci melalui Copy resource name (salin nama resource) dari menu tindakan.">
      ![Detail key ring Google Cloud dengan tindakan Copy resource name disorot di menu tindakan kunci.](https://platform.claude.com/docs/images/cmek/gcp-copy-resource-name.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API, menggunakan nama resource dari langkah Catat nama resource lengkap kunci di bagian Penyiapan kunci enkripsi.

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
          -H "content-type: application/json" \
          -d '{}'
        ```

        Respons yang berhasil terlihat seperti ini:

        ```json
        { "type": "external_key_validation", "status": "success", "error": null }
        ```

        Jika validasi gagal, penyebab umumnya adalah:

        * **VPC Service Controls:** jika service perimeter melindungi Cloud KMS di proyek Anda, tambahkan Anthropic ke access level pada perimeter tersebut (atau kecualikan proyek kunci) agar Anthropic dapat menjangkau kunci.
        * **Domain restricted sharing:** kebijakan organisasi `constraints/iam.allowedPolicyMemberDomains` dapat menghapus binding service account Anthropic (lihat catatan sebelumnya). Pastikan binding ada dengan `gcloud kms keys get-iam-policy <your-key-name> --project=<your-project-id> --location=<region> --keyring=<your-keyring-name>`.
        * **Versi kunci dinonaktifkan atau dihancurkan:** pastikan versi utama kunci diaktifkan, dan tidak dinonaktifkan, dijadwalkan untuk dihancurkan, atau sudah dihancurkan.
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
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Google Cloud**, tempelkan nama resource lengkap kunci dari langkah sebelumnya, dan klik **Continue**. Anthropic memvalidasi kunci dengan proses enkripsi dan dekripsi bolak-balik. Setelah kunci ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK sejak saat itu.

    Di Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan satu organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `google` dengan resource `google_kms_key_ring`, `google_kms_crypto_key`, dan `google_kms_crypto_key_iam_member`.
