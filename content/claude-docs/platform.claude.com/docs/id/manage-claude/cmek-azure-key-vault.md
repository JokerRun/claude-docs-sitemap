---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
fetched_at: 2026-10-21T02:21:05.363362Z
sha256: 95d8d6560e13ff40efcdd6605409e89bef6b87f7ef40825c6581a7fdc4b08935
---

---
title: Mengonfigurasi Azure Key Vault untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
description: Gunakan Azure Key Vault untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan Azure Key Vault
```

Panduan ini menunjukkan cara menggunakan kunci Azure Key Vault sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci Key Vault Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda mulai.
</Warning>

## Prasyarat

* Azure Key Vault dengan pengaturan berikut:

  * Otorisasi RBAC diaktifkan (`enableRbacAuthorization: true`).
  * Akses jaringan publik diizinkan. Private endpoint tidak didukung.
  * Perlindungan purge diaktifkan (`enablePurgeProtection: true`). Anda tidak dapat menonaktifkan perlindungan purge setelah mengaktifkannya.
  * Pengaturan diagnostik merutekan kategori log `AuditEvent` ke Log Analytics, akun penyimpanan, atau event hub. Tanpa pengaturan ini, Anda tidak memiliki jejak audit atas operasi kunci Anthropic, seperti `KeyWrap`, `KeyUnwrap`, dan `KeyGet`.

* Izin untuk membuat kunci di vault dan untuk menetapkan peran RBAC padanya.

* Izin untuk membuat service principal di tenant Entra Anda (`Application Administrator`, `Cloud Application Administrator`, atau peran kustom yang setara).

* [`az` CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) terinstal dan terautentikasi, atau Cloud Shell di portal Azure. Beberapa langkah tidak memiliki padanan di portal.

* Untuk mendaftarkan kunci melalui API, kunci Admin API Anthropic untuk organisasi Anda.

## Informasi aplikasi Anthropic

Anda memberikan akses ke kunci Anda kepada aplikasi multitenant Anthropic berikut. Aplikasi ini tidak meminta izin Microsoft Graph apa pun.

| Field                               | Nilai                                  |
| ----------------------------------- | -------------------------------------- |
| Client ID aplikasi multitenant (US) | `8635ae1a-3e5d-44e8-a4ed-e0f614466f87` |
| Nama tampilan aplikasi              | `anthropic-cmek-client-us`             |

<Warning>
  Gunakan hanya client ID dan nama tampilan yang dipublikasikan ini. Jangan pernah mempercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

Kunci harus memenuhi persyaratan berikut:

* **Tipe:** RSA, 3072-bit atau lebih besar. Untuk kunci yang didukung HSM, gunakan `RSA-HSM`, yang memerlukan vault dengan SKU Premium.
* **Operasi yang diizinkan:** `wrapKey` dan `unwrapKey`. Langkah-langkah dalam panduan ini menonaktifkan semua operasi lainnya, sehingga Anthropic hanya dapat membaca kunci serta melakukan wrap dan unwrap dengannya.
* **Tag organisasi:** `anthropic-org-<ORGANIZATION_UUID>` dengan nilai `true`. Ganti `<ORGANIZATION_UUID>` dengan ID organisasi Anthropic Anda dalam huruf kecil. Validasi gagal tanpa tag ini.
* **Akses:** peran `Key Vault Crypto User` untuk service principal Anthropic, yang ditetapkan pada kunci.

<Note>
  **Menemukan ID organisasi Anda:** Gunakan UUID polos, bukan ID dengan awalan `org_`. Salin dari salah satu tempat berikut:

  * **Claude Console:** kolom **Organization ID** di halaman [Organization](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`)
  * **claude.ai:** kolom **Organization ID** di bawah **Organization settings > Organization**
  * **Admin API:** field `id` dari endpoint [Organization Info](https://platform.claude.com/docs/id/api/organization/retrieve)
</Note>

### Membuat kunci dan memberikan akses

<Tabs>
  <Tab title="Portal Azure">
    <Steps>
      <Step title="Membuat service principal Anthropic">
        Buka Cloud Shell dari bilah navigasi atas portal. Jalankan perintah ini:

        ```bash
        az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
        ```

        Jika service principal sudah ada, lanjutkan ke langkah berikutnya.
      </Step>

      <Step title="Memastikan service principal sudah ada">
        Buka **Microsoft Entra ID > Enterprise applications** dan hapus filter tipe aplikasi default. Cari `anthropic-cmek-client-us`.

        <Frame caption="Service principal anthropic-cmek-client-us di aplikasi enterprise Entra.">
          ![Ikhtisar aplikasi enterprise Microsoft Entra untuk anthropic-cmek-client-us, yang menampilkan Application ID dan Object ID-nya.](https://platform.claude.com/docs/images/cmek/azure-service-principal.png)
        </Frame>
      </Step>

      <Step title="Membuka halaman Create a key">
        Buka key vault Anda dan pilih **Keys**. Klik **Generate/Import**.
      </Step>

      <Step title="Membuat kunci RSA di vault Anda">
        Atur nilai-nilai berikut:

        * **Name:** nama untuk kunci
        * **Key type:** RSA
        * **RSA key size:** 3072 atau lebih besar

        Klik tautan di sebelah **Tags**.
      </Step>

      <Step title="Menambahkan tag organisasi">
        Masukkan nilai-nilai berikut:

        * **Tag Name:** `anthropic-org-<ORGANIZATION_UUID>`
        * **Tag Value:** `true`

        Klik **OK**, lalu klik **Create**.

        <Frame caption="Buat kunci RSA berukuran 3072 atau lebih besar, dengan tag anthropic-org-<ORGANIZATION_UUID> diatur ke true.">
          ![Halaman Create a key di Azure Key Vault dengan RSA, ukuran kunci 3072, dan tag anthropic-org diatur ke true.](https://platform.claude.com/docs/images/cmek/azure-create-key-tag.png)
        </Frame>
      </Step>

      <Step title="Membatasi operasi yang diizinkan">
        Buka kunci baru tersebut, lalu buka versi saat ini. Di bawah **Permitted operations**, hapus centang semua kotak kecuali **Wrap Key** dan **Unwrap Key**. Klik **Save**.

        <Frame caption="Batasi operasi yang diizinkan ke Wrap Key dan Unwrap Key. Versi kunci menampilkan tag organisasi.">
          ![Versi kunci di Azure Key Vault dengan 1 tag dan Permitted operations dibatasi ke Wrap Key dan Unwrap Key.](https://platform.claude.com/docs/images/cmek/azure-permitted-operations-tag.png)
        </Frame>
      </Step>

      <Step title="Membuka kontrol akses kunci">
        Buka kunci itu sendiri, bukan vault. Pilih tab **Access control (IAM)**-nya dan klik **Add > Add role assignment**.
      </Step>

      <Step title="Memilih peran">
        Di tab **Role**, pilih **Key Vault Crypto User**. Klik **Next**.
      </Step>

      <Step title="Menambahkan service principal Anthropic">
        Di tab **Members**, klik **Select members**. Cari `anthropic-cmek-client-us` dan pilih. Klik **Select**, lalu klik **Next**.
      </Step>

      <Step title="Meninjau dan menetapkan">
        Di tab **Review + assign**, klik **Review + assign**.
      </Step>
    </Steps>

    Untuk menggunakan kunci yang sudah Anda miliki, ikuti langkah-langkah berikut sebagai pengganti langkah 3 hingga 6, lalu lanjutkan dari langkah 7:

    1. Di key vault Anda, pilih **Keys** dan buka kunci tersebut. Buka versi saat ini.
    2. Klik tautan di sebelah **Tags**.
    3. Tambahkan tag organisasi dan klik **OK**.
    4. Di bawah **Permitted operations**, hapus centang semua kotak kecuali **Wrap Key** dan **Unwrap Key**.
    5. Klik **Save**.
  </Tab>

  <Tab title="Azure CLI">
    <Steps>
      <Step title="Membuat service principal Anthropic">
        ```bash
        az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
        ```

        Salin field `id` dari output.

        Jika perintah berakhir dengan error "already exists", dapatkan `id` dengan perintah ini sebagai gantinya:

        ```bash
        az ad sp show --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87 --query id -o tsv
        ```
      </Step>

      <Step title="Membuat kunci RSA di vault Anda">
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

      <Step title="Memberikan service principal Anthropic akses ke kunci Anda">
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

    Untuk menggunakan kunci yang sudah Anda miliki, jalankan perintah ini sebagai pengganti langkah 2:

    ```bash
    az keyvault key set-attributes \
      --vault-name <your-vault-name> \
      --name <your-key-name> \
      --ops wrapKey unwrapKey \
      --tags anthropic-org-<ORGANIZATION_UUID>=true
    ```

    Perintah ini menggantikan tag yang sudah ada pada versi tersebut. Tambahkan setiap tag yang sudah ada ke `--tags` sebagai `name=value`.
  </Tab>
</Tabs>

<Note>
  **Opsional:**

  * Untuk berbagi satu kunci di antara beberapa organisasi Anthropic, tambahkan satu tag organisasi untuk masing-masing. Sebuah versi kunci dapat membawa paling banyak 15 tag, termasuk milik Anda sendiri.
  * Jika vault hanya berisi kunci ini, Anda dapat menetapkan peran pada vault alih-alih pada kunci.
</Note>

### Memeriksa konfigurasi vault Anda

Jalankan perintah ini dengan Azure CLI atau di Cloud Shell. Ganti `<your-vault-name>` dengan nama key vault Anda.

```bash
az keyvault show --name <your-vault-name> \
  --query "{rbac:properties.enableRbacAuthorization, purge:properties.enablePurgeProtection, pub:properties.publicNetworkAccess, net:properties.networkAcls.defaultAction, ipRules:properties.networkAcls.ipRules, uri:properties.vaultUri, tenantId:properties.tenantId}"
```

Konfirmasikan nilai-nilai berikut:

* `rbac`: `true`
* `purge`: `true`. Jika nilainya `false` atau `null`, aktifkan perlindungan purge sebelum Anda melanjutkan.
* `pub`: `"Enabled"`. Jika nilainya `"Disabled"`, aktifkan akses jaringan publik.
* `net`: `"Allow"`, atau `"Deny"` dengan rentang IP keluar Anthropic di `ipRules`. Untuk rentang tersebut, lihat [Alamat IP keluar](https://platform.claude.com/docs/id/api/ip-addresses#outbound-ip-addresses).

Salin nilai-nilai berikut untuk mendaftarkan kunci:

* `uri`: URI vault
* `tenantId`: ID tenant yang mengatur vault

## Mendaftarkan kunci dengan Anthropic

<Tabs>
  <Tab title="Claude Platform">
    <Tabs>
      <Tab title="Claude Console">
        <Steps>
          <Step title="Buka pengaturan kunci enkripsi">
            Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy#encryption-keys) (`platform.claude.com/settings/privacy`). Jika Anda tidak melihat **Encryption keys**, pilih **Organization** dari menu dropdown di bagian atas halaman.
          </Step>

          <Step title="Tambahkan kunci">
            Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name** dan pilih **Azure Key Vault**. Klik **Continue**.
          </Step>

          <Step title="Memasukkan detail kunci">
            Kotak dialog menampilkan **Organization tag**. Periksa bahwa kunci Anda memiliki tag ini. Masukkan nilai-nilai berikut:

            * **Vault URI:** nilai `uri` yang Anda salin
            * **Key name:** nama kunci
            * **Tenant ID:** nilai `tenantId` yang Anda salin

            Klik **Add**.
          </Step>

          <Step title="Memvalidasi kunci">
            Di daftar **Encryption keys**, klik **Verify** di sebelah kunci. **Connected** muncul ketika pemeriksaan berhasil. Jika gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#troubleshoot-validation) untuk penyebab umum.
          </Step>

          <Step title="Melampirkan kunci ke workspace">
            Melampirkan kunci tidak dapat dibatalkan. Jika memungkinkan, lampirkan kunci ke workspace baru sebelum workspace tersebut menerima permintaan apa pun. Di workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

            Di halaman Data retention, pilih workspace dari menu dropdown di bagian atas halaman. Di bawah **Encryption key**, pilih kunci dan klik **Save**.
          </Step>

          <Step title="Konfirmasi perubahan">
            Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Confirm**.
          </Step>
        </Steps>
      </Tab>

      <Tab title="API">
        <Steps>
          <Step title="Buat kunci eksternal">
            Ganti placeholder:

            * **`<friendly-name>`:** nama tampilan untuk kunci
            * **`<your-vault-name>`:** nama key vault Anda
            * **`<your-key-name>`:** nama kunci
            * **`<your-tenant-id>`:** nilai `tenantId` yang Anda salin

            <CodeGroup>
              ```bash cURL
              curl -sS "https://api.anthropic.com/v1/organizations/external_keys" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
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

              ```bash CLI
              ant organization:external-keys create <<'YAML'
              display_name: "<friendly-name>"
              geo: us
              provider_config:
                type: azure
                vault_uri: "https://<your-vault-name>.vault.azure.net/"
                key_name: "<your-key-name>"
                tenant_id: "<your-tenant-id>"
              YAML
              ```

              ```python Python
              client = anthropic.Anthropic()

              external_key = client.organization.external_keys.create(
                  display_name="<friendly-name>",
                  geo="us",
                  provider_config={
                      "type": "azure",
                      "vault_uri": "https://<your-vault-name>.vault.azure.net/",
                      "key_name": "<your-key-name>",
                      "tenant_id": "<your-tenant-id>",
                  },
              )

              print(f"id: {external_key.id}")
              print(f"display_name: {external_key.display_name}")
              ```

              ```typescript TypeScript
              const client = new Anthropic();

              const externalKey = await client.organization.externalKeys.create({
                display_name: "<friendly-name>",
                geo: "us",
                provider_config: {
                  type: "azure",
                  vault_uri: "https://<your-vault-name>.vault.azure.net/",
                  key_name: "<your-key-name>",
                  tenant_id: "<your-tenant-id>"
                }
              });

              console.log(`id: ${externalKey.id}`);
              console.log(`display_name: ${externalKey.display_name}`);
              ```

              ```csharp C#
              using Anthropic.Models.Organization.ExternalKeys;

              AnthropicClient client = new();

              var externalKey = await client.Organization.ExternalKeys.Create(new()
              {
                  DisplayName = "<friendly-name>",
                  Geo = Geo.Us,
                  ProviderConfig = new AzureExternalKeyConfigParam
                  {
                      VaultUri = "https://<your-vault-name>.vault.azure.net/",
                      KeyName = "<your-key-name>",
                      TenantID = "<your-tenant-id>"
                  }
              });

              Console.WriteLine($"id: {externalKey.ID}");
              Console.WriteLine($"display_name: {externalKey.DisplayName}");
              ```

              ```go Go
              client := anthropic.NewClient()

              externalKey, err := client.Organization.ExternalKeys.New(context.Background(), anthropic.OrganizationExternalKeyNewParams{
              	DisplayName: anthropic.String("<friendly-name>"),
              	Geo:         anthropic.OrganizationExternalKeyNewParamsGeoUs,
              	ProviderConfig: anthropic.OrganizationExternalKeyNewParamsProviderConfigUnion{
              		OfAzure: &anthropic.AzureExternalKeyConfigParam{
              			VaultURI: "https://<your-vault-name>.vault.azure.net/",
              			KeyName:  "<your-key-name>",
              			TenantID: "<your-tenant-id>",
              		},
              	},
              })
              if err != nil {
              	log.Fatal(err)
              }

              fmt.Printf("id: %s\n", externalKey.ID)
              fmt.Printf("display_name: %s\n", externalKey.DisplayName)
              ```

              ```java Java
              import com.anthropic.models.organization.externalkeys.AzureExternalKeyConfigParam;
              import com.anthropic.models.organization.externalkeys.ExternalKeyCreateParams;

              void main() {
                  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

                  var params = ExternalKeyCreateParams.builder()
                      .displayName("<friendly-name>")
                      .geo(ExternalKeyCreateParams.Geo.US)
                      .providerConfig(AzureExternalKeyConfigParam.builder()
                          .vaultUri("https://<your-vault-name>.vault.azure.net/")
                          .keyName("<your-key-name>")
                          .tenantId("<your-tenant-id>")
                          .build())
                      .build();
                  var externalKey = client.organization().externalKeys().create(params);

                  IO.println("id: " + externalKey.id());
                  IO.println("display_name: " + externalKey.displayName().orElseThrow());
              }
              ```

              ```php PHP
              use Anthropic\Organization\ExternalKeys\ExternalKeyCreateParams\Geo;
              // ...

              $client = new Client();

              $externalKey = $client->organization->externalKeys->create(
                  displayName: '<friendly-name>',
                  geo: Geo::US,
                  providerConfig: [
                      'type' => 'azure',
                      'vaultURI' => 'https://<your-vault-name>.vault.azure.net/',
                      'keyName' => '<your-key-name>',
                      'tenantID' => '<your-tenant-id>',
                  ],
              );

              echo "id: {$externalKey->id}\n";
              echo "display_name: {$externalKey->displayName}\n";
              ```

              ```ruby Ruby
              client = Anthropic::Client.new

              external_key = client.organization.external_keys.create(
                display_name: "<friendly-name>",
                geo: :us,
                provider_config: {
                  type: :azure,
                  vault_uri: "https://<your-vault-name>.vault.azure.net/",
                  key_name: "<your-key-name>",
                  tenant_id: "<your-tenant-id>"
                }
              )

              puts "id: #{external_key.id}"
              puts "display_name: #{external_key.display_name}"
              ```
            </CodeGroup>

            Field `id` pada respons berisi ID kunci eksternal. Salin untuk dua langkah berikutnya:

            ```json
            {
              "type": "external_key",
              "id": "ekey_<id>",
              "display_name": "<friendly-name>"
            }
            ```
          </Step>

          <Step title="Memvalidasi kunci">
            Ganti `ekey_<id>` dengan ID kunci eksternal.

            <CodeGroup>
              ```bash cURL
              curl -sS -X POST "https://api.anthropic.com/v1/organizations/external_keys/ekey_<id>/validate" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
                -H "anthropic-version: 2023-06-01"
              ```

              ```bash CLI
              ant organization:external-keys validate --external-key-id "ekey_<id>"
              ```

              ```python Python
              client = anthropic.Anthropic()

              validation = client.organization.external_keys.validate("ekey_<id>")

              print(f"status: {validation.status}")
              print(f"error: {validation.error}")
              ```

              ```typescript TypeScript
              const client = new Anthropic();

              const validation = await client.organization.externalKeys.validate("ekey_<id>");

              console.log(`status: ${validation.status}`);
              console.log(`error: ${validation.error}`);
              ```

              ```csharp C#
              AnthropicClient client = new();

              var validation = await client.Organization.ExternalKeys.Validate("ekey_<id>");

              Console.WriteLine($"status: {validation.Status.Raw()}");
              Console.WriteLine($"error: {validation.Error}");
              ```

              ```go Go
              client := anthropic.NewClient()

              validation, err := client.Organization.ExternalKeys.Validate(context.Background(), "ekey_<id>")
              if err != nil {
              	log.Fatal(err)
              }

              fmt.Printf("status: %s\n", validation.Status)
              fmt.Printf("error: %s\n", validation.Error)
              ```

              ```java Java
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var validation = client.organization().externalKeys().validate("ekey_<id>");

              IO.println("status: " + validation.status().asString());
              IO.println("error: " + validation.error().orElse(""));
              ```

              ```php PHP
              $client = new Client();

              $validation = $client->organization->externalKeys->validate(
                  externalKeyID: 'ekey_<id>',
              );

              echo "status: {$validation->status}\n";
              echo "error: {$validation->error}\n";
              ```

              ```ruby Ruby
              client = Anthropic::Client.new

              validation = client.organization.external_keys.validate("ekey_<id>")

              puts "status: #{validation.status}"
              puts "error: #{validation.error}"
              ```
            </CodeGroup>

            Respons yang berhasil terlihat seperti ini:

            ```json
            { "type": "external_key_validation", "status": "success", "error": null }
            ```

            Jika validasi gagal, field `error` menjelaskan masalahnya. Untuk penyebab umum, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#troubleshoot-validation).
          </Step>

          <Step title="Melampirkan kunci ke workspace">
            Melampirkan kunci tidak dapat dibatalkan. Jika memungkinkan, lampirkan kunci ke workspace baru sebelum workspace tersebut menerima permintaan apa pun. Di workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

            Ganti `<workspace-id>` dengan ID workspace dan `ekey_<id>` dengan ID kunci eksternal.

            <CodeGroup>
              ```bash cURL
              curl -sS -X POST "https://api.anthropic.com/v1/organizations/workspaces/<workspace-id>" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
                -H "anthropic-version: 2023-06-01" \
                -H "content-type: application/json" \
                -d '{
                  "external_key_id": "ekey_<id>"
                }'
              ```

              ```bash CLI
              ant organization:workspaces update \
                --workspace-id "<workspace-id>" \
                --external-key-id "ekey_<id>"
              ```

              ```python Python
              client = anthropic.Anthropic()

              workspace = client.organization.workspaces.update(
                  "<workspace-id>", external_key_id="ekey_<id>"
              )

              print(f"id: {workspace.id}")
              print(f"external_key_id: {workspace.external_key_id}")
              ```

              ```typescript TypeScript
              const client = new Anthropic();

              const workspace = await client.organization.workspaces.update("<workspace-id>", {
                external_key_id: "ekey_<id>"
              });

              console.log(`id: ${workspace.id}`);
              console.log(`external_key_id: ${workspace.external_key_id}`);
              ```

              ```csharp C#
              AnthropicClient client = new();

              var workspace = await client.Organization.Workspaces.Update("<workspace-id>", new()
              {
                  ExternalKeyID = "ekey_<id>"
              });

              Console.WriteLine($"id: {workspace.ID}");
              Console.WriteLine($"external_key_id: {workspace.ExternalKeyID}");
              ```

              ```go Go
              client := anthropic.NewClient()

              workspace, err := client.Organization.Workspaces.Update(
              	context.Background(),
              	"<workspace-id>",
              	anthropic.OrganizationWorkspaceUpdateParams{
              		ExternalKeyID: anthropic.String("ekey_<id>"),
              	},
              )
              if err != nil {
              	log.Fatal(err)
              }

              fmt.Printf("id: %s\n", workspace.ID)
              fmt.Printf("external_key_id: %s\n", workspace.ExternalKeyID)
              ```

              ```java Java
              import com.anthropic.models.organization.workspaces.WorkspaceUpdateParams;

              void main() {
                  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

                  var params = WorkspaceUpdateParams.builder()
                      .externalKeyId("ekey_<id>")
                      .build();
                  var workspace = client.organization().workspaces().update("<workspace-id>", params);

                  IO.println("id: " + workspace.id());
                  IO.println("external_key_id: " + workspace.externalKeyId().orElseThrow());
              }
              ```

              ```php PHP
              $client = new Client();

              $workspace = $client->organization->workspaces->update(
                  workspaceID: '<workspace-id>',
                  externalKeyID: 'ekey_<id>',
              );

              echo "id: {$workspace->id}\n";
              echo "external_key_id: {$workspace->externalKeyID}\n";
              ```

              ```ruby Ruby
              client = Anthropic::Client.new

              workspace = client.organization.workspaces.update(
                "<workspace-id>",
                external_key_id: "ekey_<id>"
              )

              puts "id: #{workspace.id}"
              puts "external_key_id: #{workspace.external_key_id}"
              ```
            </CodeGroup>
          </Step>
        </Steps>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Claude Enterprise">
    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, dan sebuah organisasi hanya dapat memiliki satu kunci.

    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Buka [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) dan temukan **Encryption keys**.
      </Step>

      <Step title="Tambahkan kunci">
        Klik **Add key**. Masukkan **Display name** dan pilih **Azure Key Vault**. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Continue**.
      </Step>

      <Step title="Memasukkan detail kunci">
        Kotak dialog menampilkan **Organization tag**. Periksa bahwa kunci Anda memiliki tag ini. Masukkan nilai-nilai berikut:

        * **Vault URI:** nilai `uri` yang Anda salin
        * **Key name:** nama kunci
        * **Tenant ID:** nilai `tenantId` yang Anda salin

        Klik **Add**.
      </Step>

      <Step title="Konfirmasi bahwa validasi berhasil">
        Ketika pemeriksaan berhasil, **Encryption key configured** muncul, dan organisasi Anda dilindungi CMEK sejak saat itu. Jika pemeriksaan gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#troubleshoot-validation).
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Memecahkan masalah validasi

Jika validasi gagal, penyebab umumnya adalah:

* **Tag organisasi salah:** Pastikan versi kunci saat ini memiliki tag `anthropic-org-<ORGANIZATION_UUID>` dengan nilai `true`. ID organisasi harus berupa UUID polos dalam huruf kecil.
* **Penundaan propagasi RBAC:** Penetapan peran dapat memerlukan beberapa menit untuk berlaku. Tunggu dan coba lagi.
* **Network ACL memblokir Anthropic:** Konfirmasikan akses jaringan publik dan `ipRules`, seperti yang dijelaskan di [Memeriksa konfigurasi vault Anda](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#check-your-vault-configuration).
* **Kebijakan conditional access pada workload identity:** Jika tenant Anda memiliki kebijakan conditional access yang menargetkan service principal, kecualikan service principal Anthropic. Atau tambahkan rentang IP keluar Anthropic ke named location kebijakan tersebut.

## Terraform

Untuk membuat kunci dengan Terraform, gunakan provider `azurerm` dan `azuread`.
