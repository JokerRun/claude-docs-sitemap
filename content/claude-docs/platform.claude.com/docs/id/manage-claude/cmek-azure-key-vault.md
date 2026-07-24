---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e9b043b34eacc59d632dc6cc8f035c90024e755e15c5c2eb5f42c4cc7b3a9566
---

# Mengonfigurasi Azure Key Vault untuk CMEK

Gunakan Azure Key Vault untuk menyediakan kunci enkripsi bagi organisasi Anda.

---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Azure Key Vault"
```

Panduan ini menjelaskan cara mengonfigurasi kunci Azure Key Vault sebagai [customer-managed encryption key (CMEK)](/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci Key Vault Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Azure Key Vault dengan **otorisasi RBAC diaktifkan** (`enableRbacAuthorization: true`) dan **akses jaringan publik diizinkan**. Anthropic memanggil vault Anda melalui endpoint data-plane publik; private endpoint tidak didukung.
* **Purge protection diaktifkan** (`enablePurgeProtection: true`) pada vault. Tanpanya, kunci yang dihapus dapat dibersihkan secara permanen selama jendela retensi soft-delete, menyebabkan kehilangan data yang dilindungi CMEK Anda secara tidak dapat dipulihkan. Purge protection tidak dapat dinonaktifkan setelah diaktifkan.
* Izin untuk membuat kunci di vault dan untuk menetapkan peran RBAC padanya.
* Izin untuk membuat service principal di tenant Entra Anda (`Application Administrator`, `Cloud Application Administrator`, atau peran kustom yang setara).
* Kunci Admin API Anthropic untuk organisasi Anda.
* [`az` CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) terpasang dan terautentikasi.
* **Diagnostic Settings** dikonfigurasi pada vault untuk merutekan kategori log `AuditEvent` ke Log Analytics, akun penyimpanan, atau event hub. Azure Key Vault tidak mengeluarkan log audit data-plane (seperti `KeyWrap`, `KeyUnwrap`, dan `KeyGet`) secara default, jadi tanpa ini Anda tidak mendapatkan jejak audit untuk operasi kunci Anthropic.

## Informasi aplikasi Anthropic

Agar Anthropic menggunakan kunci enkripsi Anda, Anda harus mengonfigurasi ID aplikasi multitenant Anthropic dan nama tampilannya. Nilai-nilai tersebut adalah:

| Field                               | Value                                  |
| ----------------------------------- | -------------------------------------- |
| Client ID aplikasi multitenant (US) | `8635ae1a-3e5d-44e8-a4ed-e0f614466f87` |
| Nama tampilan aplikasi              | `anthropic-cmek-client-us`             |

<Warning>
  Gunakan hanya client ID dan nama tampilan yang dipublikasikan ini. Jangan pernah mempercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Berikan persetujuan untuk aplikasi multitenant Anthropic">
    Ini membuat service principal di tenant Entra Anda untuk aplikasi klien CMEK Anthropic. Aplikasi ini tidak meminta izin Microsoft Graph apa pun; aplikasi ini hanya ada sebagai target federasi untuk akses data-plane Key Vault.

    ```bash
    az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
    ```

    Dari output, catat field `id`. Ini adalah object ID service principal di tenant Anda, yang Anda gunakan saat menetapkan peran RBAC.

    ```json
    {
      "appId": "8635ae1a-3e5d-44e8-a4ed-e0f614466f87",
      "displayName": "anthropic-cmek-client-us",
      "id": "<sp-object-id>"
    }
    ```

    Jika service principal sudah ada di tenant Anda (dari percobaan sebelumnya atau integrasi lain), `az ad sp create` keluar dengan kesalahan "already exists". Ambil object ID-nya sebagai gantinya:

    ```bash
    az ad sp show --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87 --query id -o tsv
    ```

    Langkah ini tidak memiliki padanan di Portal. Jika Anda tidak memiliki Azure CLI terpasang secara lokal, buka Cloud Shell dari bilah navigasi atas Portal. Setelah perintah berhasil, Anda dapat menemukan object ID service principal di **Microsoft Entra ID > Enterprise applications** dengan menghapus filter tipe aplikasi default dan mencari `anthropic-cmek-client-us`.

    <Frame caption="Temukan Object ID service principal pada ikhtisar aplikasi enterprise Entra-nya.">
      ![Ikhtisar aplikasi enterprise Microsoft Entra untuk anthropic-cmek-client-us, menampilkan Application ID dan Object ID-nya.](/docs/images/cmek/azure-service-principal.png)
    </Frame>
  </Step>

  <Step title="Buat kunci RSA di vault Anda">
    Azure Key Vault tidak mendukung symmetric key wrapping, jadi kunci harus berupa RSA (3072-bit atau lebih besar) dengan `wrapKey` dan `unwrapKey` dalam operasi yang diizinkan.

    ```bash
    az keyvault key create \
      --vault-name <your-vault-name> \
      --name <your-key-name> \
      --kty RSA --size 3072 \
      --ops wrapKey unwrapKey
    ```

    Untuk kunci yang didukung HSM, gunakan `--kty RSA-HSM` (memerlukan vault dengan SKU Premium). Kunci RSA yang dilindungi perangkat lunak dapat diterima untuk integrasi ini.

    Dari Portal, buka Key Vault Anda, pilih **Keys**, lalu **Generate/Import**. Atur tipe kunci ke RSA dan ukurannya ke 3072 atau lebih besar. Untuk membatasi kunci hanya untuk wrap dan unwrap, buka versi kunci, gulir ke **Permitted operations**, dan hapus centang semuanya kecuali **Wrap Key** dan **Unwrap Key**.

    <Frame caption="Buat kunci RSA berukuran 3072 atau lebih besar.">
      ![Halaman Create a key Azure Key Vault dengan opsi Generate, tipe kunci RSA, dan ukuran kunci RSA 3072 dipilih.](/docs/images/cmek/azure-create-key.png)
    </Frame>

    <Frame caption="Batasi permitted operations ke Wrap Key dan Unwrap Key.">
      ![Versi kunci Azure Key Vault dengan Permitted operations dibatasi ke Wrap Key dan Unwrap Key.](/docs/images/cmek/azure-permitted-operations.png)
    </Frame>
  </Step>

  <Step title="Berikan akses ke kunci Anda untuk service principal Anthropic">
    Tetapkan peran `Key Vault Crypto User` ke service principal dari langkah pertama, dengan cakupan pada **kunci individual** alih-alih seluruh vault.

    ```bash
    VAULT_ID=$(az keyvault show --name <your-vault-name> --query id -o tsv)

    az role assignment create \
      --role "Key Vault Crypto User" \
      --assignee-object-id <sp-object-id> \
      --assignee-principal-type ServicePrincipal \
      --scope "${VAULT_ID}/keys/<your-key-name>"
    ```

    Peran bawaan `Key Vault Crypto User` memberikan operasi kriptografi kunci (encrypt, decrypt, wrap, unwrap, sign, verify) ditambah pembacaan kunci pada cakupan yang ditetapkan. Pembatasan `--ops wrapKey unwrapKey` yang Anda atur pada kunci di langkah sebelumnya lebih lanjut mempersempit operasi mana yang dapat berhasil terhadap kunci ini, jadi dalam praktiknya Anthropic hanya dapat melakukan wrap dan unwrap.

    Dari Portal, buka **kunci** (bukan vault), pilih tab **Access control (IAM)**-nya, klik **Add > Add role assignment**, pilih **Key Vault Crypto User**, dan tetapkan ke service principal `anthropic-cmek-client-us`.

    <Note>
      **Alternatif vault khusus:** Microsoft merekomendasikan vault khusus per aplikasi dengan peran yang ditetapkan pada cakupan vault. Jika Anda menyediakan vault yang hanya menyimpan kunci CMEK Anthropic ini, Anda dapat menetapkan peran pada cakupan vault sebagai gantinya dan efeknya identik. Gunakan cakupan pada kunci individual ketika kunci berada di vault bersama.
    </Note>

    <Frame caption="Tetapkan Key Vault Crypto User ke service principal Anthropic, dengan cakupan pada kunci.">
      ![Penetapan peran IAM Key Vault yang menampilkan anthropic-cmek-client-us ditetapkan peran Key Vault Crypto User.](/docs/images/cmek/azure-role-assignment.png)
    </Frame>
  </Step>

  <Step title="Verifikasi konfigurasi vault Anda">
    ```bash
    az keyvault show --name <your-vault-name> \
      --query "{rbac:properties.enableRbacAuthorization, purge:properties.enablePurgeProtection, pub:properties.publicNetworkAccess, net:properties.networkAcls.defaultAction, ipRules:properties.networkAcls.ipRules, uri:properties.vaultUri, tenantId:properties.tenantId}"
    ```

    Konfirmasikan bahwa:

    * `rbac` adalah `true`.
    * `purge` adalah `true`. Jika nilainya `false` atau `null`, aktifkan purge protection pada vault sebelum melanjutkan. Tanpanya, kunci yang di-soft-delete dapat dibersihkan secara permanen selama jendela retensi, membuat data yang dilindungi CMEK Anda tidak dapat dipulihkan.
    * `pub` adalah `"Enabled"`. Jika nilainya `"Disabled"`, Anthropic tidak dapat menjangkau vault melalui endpoint data-plane publiknya dan validasi gagal.
    * `net` adalah `"Allow"`, atau, jika nilainya `"Deny"`, pastikan `ipRules` menyertakan rentang egress Anthropic (hubungi Anthropic untuk daftar terkini).
    * `uri` adalah URI vault yang Anda gunakan saat mendaftarkan kunci.
    * `tenantId` adalah tenant yang mengatur vault. Gunakan nilai ini sebagai `tenant_id` saat Anda mendaftarkan kunci, bukan tenant dari langganan yang sedang aktif (keduanya dapat berbeda dalam penyiapan lintas tenant).
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
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
              "type": "azure",
              "vault_uri": "https://<your-vault-name>.vault.azure.net/",
              "key_name": "<your-key-name>",
              "tenant_id": "<your-tenant-id>"
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
        Picu round-trip enkripsi dan dekripsi terhadap kunci Anda. Ini mengonfirmasi bahwa Anthropic dapat melakukan autentikasi ke tenant Anda dan melakukan operasi wrap dan unwrap.

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

        Jika validasi gagal, field `error` menjelaskan masalahnya. Penyebab umum adalah:

        * **Penundaan propagasi RBAC:** penetapan peran dapat memerlukan beberapa menit untuk berlaku. Tunggu dan coba lagi.
        * **ACL jaringan memblokir Anthropic:** konfirmasikan akses jaringan publik dan `ipRules` seperti yang dijelaskan pada langkah verifikasi.
        * **Kebijakan conditional access pada workload identity:** jika tenant Anda memiliki kebijakan conditional access yang menargetkan service principal, kecualikan service principal Anthropic atau tambahkan rentang egress Anthropic ke named locations kebijakan tersebut.
      </Step>

      <Step title="Lampirkan kunci ke workspace">
        Setelah kunci divalidasi, lampirkan ke workspace untuk mengaktifkan CMEK bagi data workspace tersebut.

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
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Azure**, masukkan URI vault, nama kunci, dan tenant ID dari langkah verifikasi, lalu klik **Continue**. Anthropic memvalidasi kunci dengan round-trip enkripsi dan dekripsi. Setelah ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK sejak saat itu.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, jadi tidak ada langkah pelampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `azurerm` dan `azuread`.
