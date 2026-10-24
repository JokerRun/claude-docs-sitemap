---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-10-24T02:19:09.817678Z
sha256: 9e77cc07cf9538206f547165e9dd3f0cef197ef1b94439e5f14eb0e8e19bafe3
---

---
title: Menyiapkan CMEK dengan Google Cloud KMS
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
description: Buat kunci Google Cloud KMS, berikan Anthropic akses ke kunci tersebut, dan gunakan kunci itu di Claude Platform atau Claude Enterprise.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan Google Cloud KMS
```

## Sebelum Anda mulai

Di Claude:

* Kunci enkripsi yang dikelola pelanggan (CMEK) telah [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/cmek#availability).
* Anda memiliki ID organisasi Anthropic Anda, yaitu UUID tanpa awalan `org_`. Salin ID tersebut dari [Organization](https://platform.claude.com/settings/organization) di Claude Console, atau dari **Organization settings > Organization and access** di claude.ai. Siapa pun yang membuat kunci memerlukannya.
* Anda adalah Organization Admin di Claude Platform, atau Owner atau Primary Owner di Claude Enterprise.
* Di Claude Platform, Anda memiliki workspace yang [menyimpan data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention), idealnya workspace baru, karena [data yang sudah ada tetap berada di bawah kunci milik Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).
* Di Claude Enterprise, Anda mengetahui [fitur mana yang dinonaktifkan atau berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

Di Google Cloud:

* Cloud KMS API sudah diaktifkan.
* Anda dapat membuat key ring dan kunci, serta menetapkan kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau yang setara).
* [Log audit Data Access](https://docs.cloud.google.com/logging/docs/audit/configure-data-access) Cloud KMS (Data Read dan Data Write) sudah diaktifkan, sehingga Cloud Logging mencatat penggunaan kunci Anda oleh Anthropic. Log ini nonaktif secara default.
* Jika organisasi Google Cloud Anda menerapkan berbagi terbatas domain (`constraints/iam.allowedPolicyMemberDomains`), hal ini memblokir pemberian akses ke akun layanan Anthropic. Tambahkan pengecualian di tingkat proyek, atau izinkan ID pelanggan Cloud Identity milik Anthropic. Hubungi Anthropic untuk mendapatkan ID tersebut.

## Di Google Cloud: buat kunci

Setelah **Verify** atau **Add** gagal, lihat [perbaikan untuk Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#google-cloud-kms).

Langkah-langkah ini memberi kunci label berupa ID organisasi Anthropic Anda dalam huruf kecil (`<ORGANIZATION_UUID>`) dan memberikan akses ke akun layanan Anthropic:

```text wrap
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

Gunakan hanya alamat ini, jangan pernah alamat yang dikirim melalui email atau chat.

Anda dapat menggunakan lokasi Cloud KMS mana pun. Untuk latensi terendah, gunakan `us-east5` atau `us-central1`. Anthropic sangat menyarankan perlindungan HSM.

Untuk menggunakan kunci yang sudah Anda miliki, [tambahkan label organisasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#organization-label) terlebih dahulu.

<Tabs>
  <Tab title="Google Cloud Console">
    <Steps>
      <Step title="Buat atau pilih key ring">
        Di Google Cloud console, buka halaman [Key management](https://console.cloud.google.com/security/kms). Buka sebuah key ring, atau buat key ring di lokasi seperti `us-east5`.
      </Step>

      <Step title="Konfigurasikan kunci">
        Klik **Create key** dan masukkan nama. Pilih opsi-opsi berikut:

        * **Protection level:** HSM
        * **Key material:** Generated key
        * **Purpose:** Symmetric encrypt/decrypt
        * **Algorithm:** Google symmetric key
      </Step>

      <Step title="Tambahkan label organisasi">
        Klik **Additional settings**, lalu **Add label**. Masukkan label organisasi:

        * **Key 1:** `anthropic-org-<ORGANIZATION_UUID>`
        * **Value 1:** `true`

        Klik **Create**.

        <Frame caption="Kunci enkripsi/dekripsi simetris yang dilindungi HSM dengan label organisasi.">
          ![Halaman Create key Google Cloud KMS dengan perlindungan HSM, enkripsi/dekripsi simetris, dan label anthropic-org yang disetel ke true.](https://platform.claude.com/docs/images/cmek/gcp-create-key-label.png)
        </Frame>
      </Step>

      <Step title="Buka izin kunci">
        Di halaman detail key ring, pilih kotak centang di sebelah kunci. Buka panel **Permissions** dan klik **Grant access**.
      </Step>

      <Step title="Berikan akun layanan Anthropic akses ke kunci">
        Periksa bahwa **Resource** menampilkan kunci, bukan key ring atau proyek. Masukkan nilai-nilai berikut:

        * **New principals:** `anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com`
        * **Role:** Cloud KMS CryptoKey Encrypter/Decrypter

        Klik **Add another role** dan pilih **Cloud KMS Viewer**. Klik **Save**.

        <Frame caption="Berikan kedua peran kepada akun layanan Anthropic, dengan cakupan pada kunci.">
          ![Dialog Grant access dengan akun layanan Anthropic yang diberi peran Cloud KMS CryptoKey Encrypter/Decrypter dan Viewer.](https://platform.claude.com/docs/images/cmek/gcp-grant-access.png)
        </Frame>
      </Step>

      <Step title="Salin nama resource lengkap kunci">
        Di halaman detail key ring, buka menu **Actions** milik kunci dan klik **Copy resource name**.

        <Frame caption="Salin nama resource lengkap kunci dari menu actions.">
          ![Detail key ring Google Cloud dengan tindakan Copy resource name disorot di menu actions milik kunci.](https://platform.claude.com/docs/images/cmek/gcp-copy-resource-name.png)
        </Frame>
      </Step>
    </Steps>
  </Tab>

  <Tab title="gcloud CLI">
    Di setiap perintah, ganti placeholder berikut:

    * **`<your-project-id>`:** ID proyek Google Cloud Anda
    * **`<region>`:** lokasi kunci, seperti `us-east5`
    * **`<your-keyring-name>`:** nama key ring
    * **`<your-key-name>`:** nama kunci
    * **`<ORGANIZATION_UUID>`:** ID organisasi Anthropic Anda dalam huruf kecil

    <Steps>
      <Step title="Buat atau pilih key ring">
        Lewati langkah ini jika Anda sudah memiliki key ring untuk digunakan kembali.

        ```bash
        gcloud kms keyrings create <your-keyring-name> \
          --project=<your-project-id> \
          --location=<region>
        ```
      </Step>

      <Step title="Buat kunci">
        ```bash
        gcloud kms keys create <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --purpose=encryption \
          --protection-level=hsm \
          --labels=anthropic-org-<ORGANIZATION_UUID>=true
        ```

        Untuk perlindungan perangkat lunak, hilangkan `--protection-level=hsm`.
      </Step>

      <Step title="Berikan akun layanan Anthropic akses ke kunci">
        Jalankan kedua perintah:

        ```bash
        gcloud kms keys add-iam-policy-binding <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
          --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
        ```

        ```bash
        gcloud kms keys add-iam-policy-binding <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
          --role=roles/cloudkms.viewer
        ```
      </Step>

      <Step title="Dapatkan nama resource lengkap kunci">
        ```bash
        gcloud kms keys describe <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --format="value(name)"
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

Siapa pun yang menambahkan kunci di Claude memerlukan nama resource lengkapnya, dalam format ini:

```text wrap
projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>
```

### Tambahkan label organisasi ke kunci yang sudah Anda miliki

Verifikasi gagal kecuali kunci memiliki label `anthropic-org-<ORGANIZATION_UUID>` yang disetel ke `true`, dengan ID organisasi Anthropic Anda dalam huruf kecil. Untuk menambahkan label, jalankan:

```bash
gcloud kms keys update <your-key-name> \
  --project=<your-project-id> \
  --location=<region> \
  --keyring=<your-keyring-name> \
  --update-labels=anthropic-org-<ORGANIZATION_UUID>=true
```

Nilai-nilai lainnya ada di nama resource lengkap kunci, dan perintah ini mempertahankan label yang sudah ada. Kemudian lanjutkan ke [langkah-langkah yang memberikan akses](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#encryption-key-setup).

## Di Claude: tambahkan dan lampirkan kunci

Untuk membuat skrip bagian ini di Claude Platform, [gunakan Admin API](https://platform.claude.com/docs/id/manage-claude/cmek-admin-api) sebagai gantinya.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Di Claude Console, buka [Encryption keys](https://platform.claude.com/settings/privacy#encryption-keys) di halaman Data retention. Jika bagian tersebut tidak ada, pilih **Organization** dari menu dropdown di bagian atas.
      </Step>

      <Step title="Tambahkan kunci">
        Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name**, pilih **Google Cloud KMS**, dan klik **Continue**.
      </Step>

      <Step title="Masukkan nama resource kunci">
        Periksa bahwa kunci Anda memiliki **Organization label** yang ditampilkan di kotak dialog. Tempelkan nama resource lengkap kunci ke **Key resource name** dan klik **Add**.
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
        Klik **Add key**. Masukkan **Display name** dan pilih **Google Cloud KMS**. Pilih kotak centang untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Continue**.
      </Step>

      <Step title="Masukkan nama resource kunci">
        Periksa bahwa kunci Anda memiliki **Organization label** yang ditampilkan di kotak dialog. Tempelkan nama resource lengkap kunci ke **Key resource name** dan klik **Add**.
      </Step>

      <Step title="Konfirmasi bahwa kunci telah ditambahkan">
        Pemeriksaan dapat memakan waktu hingga 30 detik. Saat **Encryption key configured.** muncul, klik **Done**. Jika yang muncul justru **The encryption key couldn’t be added.**, [temukan penyebabnya dan coba lagi](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#claude-ai-add-fails).

        Kunci Anda melindungi data yang ditulis sejak saat itu. Beri tahu pengguna Anda [fitur mana yang berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).
      </Step>
    </Steps>
  </Tab>
</Tabs>
