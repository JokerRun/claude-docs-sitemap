---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: 81d1a0304d14d42be3700b119e031aef33a4ad2b51ffb7a6f7a347599f938a79
---

---
title: Menyiapkan CMEK dengan Azure Key Vault
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
description: Buat kunci Azure Key Vault, berikan Anthropic akses ke kunci tersebut, dan gunakan kunci itu di Claude Platform atau Claude Enterprise.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan Azure Key Vault
```

## Sebelum Anda mulai

Di Claude:

* Kunci enkripsi yang dikelola pelanggan (CMEK) telah [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/cmek#availability).
* Anda memiliki ID organisasi Anthropic Anda, yaitu UUID tanpa awalan `org_`. Salin ID tersebut dari [Organisasi](https://platform.claude.com/settings/organization) di Claude Console, atau dari **Pengaturan organisasi > Organisasi dan Akses** di claude.ai. Siapa pun yang membuat kunci memerlukannya.
* Anda adalah Admin organisasi di Claude Platform, atau Pemilik atau Pemilik utama di Claude Enterprise.
* Di Claude Platform, Anda memiliki workspace yang [menyimpan data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention), idealnya workspace baru, karena [data yang sudah ada tetap berada di bawah kunci milik Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).
* Di Claude Enterprise, Anda mengetahui [fitur mana yang dinonaktifkan atau berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).

Di Azure:

* Anda dapat membuat kunci di key vault Anda dan menetapkan peran RBAC padanya.
* Anda dapat membuat service principal di tenant Entra Anda (Application Administrator, Cloud Application Administrator, atau peran kustom yang setara).
* Vault memiliki pengaturan diagnostik untuk kategori log `AuditEvent`. Tanpa pengaturan tersebut, operasi kunci oleh Anthropic tidak meninggalkan jejak audit.

## Di Azure: buat kunci

Setelah **Verifikasi** atau **Tambahkan** gagal, lihat [perbaikan untuk Azure Key Vault](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#azure-key-vault).

Langkah-langkah ini memberikan akses ke kunci Anda kepada aplikasi multitenant Anthropic:

* **Nama:** `anthropic-cmek-client-us`
* **Client ID:** `8635ae1a-3e5d-44e8-a4ed-e0f614466f87`

Gunakan hanya client ID dan nama ini, jangan pernah yang dikirim melalui email atau chat. Aplikasi ini tidak meminta izin Microsoft Graph apa pun.

### Periksa vault

Untuk latensi terendah, gunakan vault di `northcentralus` atau `eastus2`. Jalankan perintah ini terlebih dahulu, di Azure CLI atau Cloud Shell:

```bash
az keyvault show --name <your-vault-name> \
  --query "{rbac:properties.enableRbacAuthorization, purge:properties.enablePurgeProtection, pub:properties.publicNetworkAccess, net:properties.networkAcls.defaultAction, ipRules:properties.networkAcls.ipRules, uri:properties.vaultUri, tenantId:properties.tenantId}"
```

| Bidang  | Harus bernilai                                                                                                                                        |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rbac`  | `true`                                                                                                                                                |
| `purge` | `true`. Jika nilainya `false` atau `null`, aktifkan perlindungan purge terlebih dahulu. Anda tidak dapat menonaktifkannya lagi.                       |
| `pub`   | `"Enabled"`. Endpoint privat tidak didukung.                                                                                                          |
| `net`   | `"Allow"`, atau `"Deny"` dengan [alamat IP keluar Anthropic](https://platform.claude.com/docs/id/api/ip-addresses#outbound-ip-addresses) di `ipRules` |

Salin `uri` (URI vault) dan `tenantId`.

### Buat kunci dan berikan akses

Di halaman ini, `<ORGANIZATION_UUID>` adalah [ID organisasi Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#prerequisites) Anda dalam huruf kecil. Untuk menggunakan kunci yang sudah Anda miliki, [tambahkan tag organisasi](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#organization-tag) terlebih dahulu.

<Tabs>
  <Tab title="Portal Azure">
    <Steps>
      <Step title="Buat service principal Anthropic">
        Buka Cloud Shell dari bilah navigasi atas portal. Jalankan perintah ini:

        ```bash
        az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
        ```

        Jika service principal sudah ada, lanjutkan ke langkah berikutnya.
      </Step>

      <Step title="Konfirmasi bahwa service principal sudah ada">
        Buka **Microsoft Entra ID > Enterprise applications** dan hapus filter jenis aplikasi default. Cari `anthropic-cmek-client-us`.

        <Frame caption="Service principal anthropic-cmek-client-us di aplikasi enterprise Entra.">
          ![Ikhtisar aplikasi enterprise Microsoft Entra untuk anthropic-cmek-client-us, yang menampilkan Application ID dan Object ID-nya.](https://platform.claude.com/docs/images/cmek/azure-service-principal.png)
        </Frame>
      </Step>

      <Step title="Buka halaman Create a key">
        Buka key vault Anda dan pilih **Keys**. Klik **Generate/Import**.
      </Step>

      <Step title="Buat kunci RSA di vault Anda">
        Tetapkan nilai-nilai berikut:

        * **Name:** nama untuk kunci
        * **Key type:** RSA
        * **RSA key size:** 3072 atau lebih besar

        Klik tautan di sebelah **Tags**.
      </Step>

      <Step title="Tambahkan tag organisasi">
        Masukkan nilai-nilai berikut:

        * **Tag Name:** `anthropic-org-<ORGANIZATION_UUID>`
        * **Tag Value:** `true`

        Klik **OK**, lalu klik **Create**.

        <Frame caption="Buat kunci RSA berukuran 3072 atau lebih besar, dengan tag anthropic-org-<ORGANIZATION_UUID> yang diatur ke true.">
          ![Halaman Create a key di Azure Key Vault dengan RSA, ukuran kunci 3072, dan tag anthropic-org yang diatur ke true.](https://platform.claude.com/docs/images/cmek/azure-create-key-tag.png)
        </Frame>
      </Step>

      <Step title="Batasi operasi yang diizinkan">
        Buka kunci baru tersebut, lalu buka versinya saat ini. Di bawah **Permitted operations**, hapus centang semua kotak kecuali **Wrap Key** dan **Unwrap Key**. Klik **Save**.

        <Frame caption="Batasi operasi yang diizinkan ke Wrap Key dan Unwrap Key. Versi kunci menampilkan tag organisasi.">
          ![Versi kunci Azure Key Vault dengan 1 tag dan Permitted operations yang dibatasi ke Wrap Key dan Unwrap Key.](https://platform.claude.com/docs/images/cmek/azure-permitted-operations-tag.png)
        </Frame>
      </Step>

      <Step title="Buka kontrol akses kunci">
        Buka kunci itu sendiri, bukan vault. Pilih tab **Access control (IAM)** miliknya dan klik **Add > Add role assignment**.
      </Step>

      <Step title="Pilih peran">
        Di tab **Role**, pilih **Key Vault Crypto User**. Klik **Next**.
      </Step>

      <Step title="Tambahkan service principal Anthropic">
        Di tab **Members**, klik **Select members**. Cari `anthropic-cmek-client-us` dan pilih. Klik **Select**, lalu klik **Next**.
      </Step>

      <Step title="Tinjau dan tetapkan">
        Di tab **Review + assign**, klik **Review + assign**.
      </Step>
    </Steps>
  </Tab>

  <Tab title="Azure CLI">
    <Steps>
      <Step title="Buat service principal Anthropic">
        ```bash
        az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
        ```

        Salin bidang `id` dari output.

        Jika perintah berhenti dengan galat “already exists”, dapatkan `id` dengan perintah ini sebagai gantinya:

        ```bash
        az ad sp show --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87 --query id -o tsv
        ```
      </Step>

      <Step title="Buat kunci RSA di vault Anda">
        ```bash
        az keyvault key create \
          --vault-name <your-vault-name> \
          --name <your-key-name> \
          --kty RSA --size 3072 \
          --ops wrapKey unwrapKey \
          --tags anthropic-org-<ORGANIZATION_UUID>=true
        ```

        Ganti placeholder:

        * **`<your-vault-name>`:** nama key vault Anda
        * **`<your-key-name>`:** nama untuk kunci
        * **`<ORGANIZATION_UUID>`:** ID organisasi Anthropic Anda dalam huruf kecil

        Untuk kunci yang didukung HSM, gunakan `--kty RSA-HSM`.
      </Step>

      <Step title="Berikan service principal Anthropic akses ke kunci Anda">
        ```bash
        VAULT_ID=$(az keyvault show --name <your-vault-name> --query id -o tsv)

        az role assignment create \
          --role "Key Vault Crypto User" \
          --assignee-object-id <sp-object-id> \
          --assignee-principal-type ServicePrincipal \
          --scope "${VAULT_ID}/keys/<your-key-name>"
        ```

        Ganti placeholder:

        * **`<your-vault-name>`:** nama key vault Anda
        * **`<sp-object-id>`:** nilai `id` dari langkah pertama
        * **`<your-key-name>`:** nama kunci
      </Step>
    </Steps>
  </Tab>
</Tabs>

Siapa pun yang menambahkan kunci di Claude memerlukan URI vault, nama kunci, dan ID tenant.

### Tambahkan tag organisasi ke kunci yang sudah Anda miliki

Verifikasi gagal tanpa tag organisasi. Kunci harus berjenis RSA, 3072-bit atau lebih besar.

Alih-alih membuat kunci, jalankan perintah ini di Azure CLI atau Cloud Shell. Perintah ini membatasi kunci ke `wrapKey` dan `unwrapKey`. Perintah ini juga mengganti tag versi saat ini, jadi cantumkan tag apa pun yang ingin Anda pertahankan di `--tags` sebagai `name=value`.

```bash
az keyvault key set-attributes \
  --vault-name <your-vault-name> \
  --name <your-key-name> \
  --ops wrapKey unwrapKey \
  --tags anthropic-org-<ORGANIZATION_UUID>=true
```

Anda tetap memerlukan langkah-langkah service principal dan penetapan peran.

## Di Claude: tambahkan dan lampirkan kunci

Untuk membuat skrip bagian ini di Claude Platform, [gunakan Admin API](https://platform.claude.com/docs/id/manage-claude/cmek-admin-api) sebagai gantinya.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Di Claude Console, buka [Kunci enkripsi](https://platform.claude.com/settings/privacy#encryption-keys) di halaman Retensi data. Jika bagian tersebut tidak ada, pilih **Organisasi** dari menu dropdown di bagian atas.
      </Step>

      <Step title="Tambahkan kunci">
        Di bawah **Kunci enkripsi**, klik **Tambahkan kunci**. Masukkan **Nama tampilan**, pilih **Azure Key Vault**, dan klik **Lanjutkan**.
      </Step>

      <Step title="Masukkan detail kunci">
        Periksa bahwa kunci Anda memiliki **Tag organisasi** yang ditampilkan di kotak dialog. Masukkan **URI Vault**, **Nama kunci**, dan **ID tenant**, biarkan **ID Klien** kosong, lalu klik **Tambahkan**.
      </Step>

      <Step title="Verifikasi kunci">
        Di daftar **Kunci enkripsi**, klik **Verifikasi** di samping kunci. **Terhubung** muncul saat pemeriksaan berhasil. Jika yang muncul justru **Koneksi gagal**, lihat [Memecahkan masalah CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting).
      </Step>

      <Step title="Lampirkan kunci ke workspace">
        <Warning>
          Melampirkan kunci [tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Anda tidak dapat melepasnya dari workspace atau menggantinya. Jika kunci dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya.
        </Warning>

        1. Di bagian atas halaman Retensi data, pilih workspace dari menu dropdown.
        2. Di bawah **Kunci enkripsi**, pilih kunci lalu klik **Simpan**.
        3. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Konfirmasi**.

        Anda akan melihat **Pengaturan ruang kerja diperbarui.** Setelah kunci [mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), log audit penyedia cloud Anda menampilkan panggilan Anthropic ke kunci tersebut.

        Dalam [organisasi ZDR](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#zdr-organizations), setelah Anda memilih workspace, pilih **Retensi data standar** agar **Kunci enkripsi** muncul. Setelah Anda mengklik **Simpan**, klik **Terima** pada ketentuan retensi data.
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
        Buka [claude.ai > Pengaturan organisasi > Data dan privasi](https://claude.ai/admin-settings/data-privacy-controls) dan temukan **Kunci enkripsi**.
      </Step>

      <Step title="Tambahkan kunci">
        Klik **Tambah kunci**. Masukkan **Nama tampilan** dan pilih **Azure Key Vault**. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Lanjutkan**.
      </Step>

      <Step title="Masukkan detail kunci">
        Periksa bahwa kunci Anda memiliki **Tag organisasi** yang ditampilkan di kotak dialog. Masukkan **URI Vault**, **Nama kunci**, dan **Tenant ID**, biarkan **Client ID** kosong, lalu klik **Tambahkan**.
      </Step>

      <Step title="Konfirmasi bahwa kunci telah ditambahkan">
        Pemeriksaan dapat memakan waktu hingga 30 detik. Saat **Kunci enkripsi terkonfigurasi.** muncul, klik **Selesai**. Jika yang muncul justru **Kunci enkripsi tidak dapat ditambahkan.**, [temukan penyebabnya dan coba lagi](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#claude-ai-add-fails).

        Kunci Anda melindungi data yang ditulis sejak saat itu. Beri tahu pengguna Anda [fitur mana yang berubah](https://platform.claude.com/docs/id/manage-claude/cmek-coverage-claude-enterprise#turned-off-or-changed).
      </Step>
    </Steps>
  </Tab>
</Tabs>
