---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 60be812a3c52db35b1fc929d3b624ce618b59801bdf78903e270b7f03403bc56
---

---
title: Mengonfigurasi Azure Key Vault untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
description: Gunakan Azure Key Vault untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Azure Key Vault"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci Azure Key Vault sebagai ["customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci Key Vault Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Azure Key Vault dengan **otorisasi RBAC diaktifkan** (`enableRbacAuthorization: true`) dan **akses jaringan publik diizinkan**. Anthropic memanggil vault Anda melalui endpoint data-plane publik; private endpoint tidak didukung.
* **Purge protection diaktifkan** (`enablePurgeProtection: true`) pada vault. Tanpanya, kunci yang dihapus dapat di-purge secara permanen selama jendela retensi soft-delete, yang menyebabkan kehilangan data terlindungi CMEK Anda secara permanen. Purge protection tidak dapat dinonaktifkan setelah diaktifkan.
* Izin untuk membuat kunci di vault dan untuk menetapkan peran RBAC pada vault tersebut.
* Izin untuk membuat service principal di tenant Entra Anda (`Application Administrator`, `Cloud Application Administrator`, atau peran kustom yang setara).
* Kunci Admin API Anthropic untuk organisasi Anda.
* [CLI `az`](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) terinstal dan terautentikasi.
* **Diagnostic Settings** dikonfigurasi pada vault untuk merutekan kategori log `AuditEvent` ke Log Analytics, storage account, atau event hub. Azure Key Vault tidak mengeluarkan log audit data-plane (seperti `KeyWrap`, `KeyUnwrap`, dan `KeyGet`) secara default, sehingga tanpa ini Anda tidak mendapatkan jejak audit untuk operasi kunci yang dilakukan Anthropic.

## Informasi aplikasi Anthropic

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus mengonfigurasi ID aplikasi multitenant Anthropic dan nama tampilannya. Nilai-nilai tersebut adalah:

| Field                               | Nilai                                  |
| ----------------------------------- | -------------------------------------- |
| Client ID aplikasi multitenant (US) | `8635ae1a-3e5d-44e8-a4ed-e0f614466f87` |
| Nama tampilan aplikasi              | `anthropic-cmek-client-us`             |

<Warning>
  Gunakan hanya client ID dan nama tampilan yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Berikan persetujuan untuk aplikasi multitenant Anthropic">
    Langkah ini membuat service principal di tenant Entra Anda untuk aplikasi klien CMEK Anthropic. Aplikasi ini tidak meminta izin Microsoft Graph apa pun; aplikasi ini hanya ada sebagai target federasi untuk akses data-plane Key Vault.

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

    Jika service principal sudah ada di tenant Anda (dari percobaan sebelumnya atau integrasi lain), `az ad sp create` akan keluar dengan error "already exists". Ambil object ID-nya sebagai gantinya:

    ```bash
    az ad sp show --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87 --query id -o tsv
    ```

    Langkah ini tidak memiliki padanan di Portal. Jika Anda tidak memiliki Azure CLI yang terinstal secara lokal, buka Cloud Shell dari bilah navigasi atas Portal. Setelah perintah berhasil, Anda dapat menemukan object ID service principal di **Microsoft Entra ID > Enterprise applications** dengan menghapus filter tipe aplikasi default dan mencari `anthropic-cmek-client-us`.

    <Frame caption="Temukan Object ID service principal pada halaman ringkasan enterprise application Entra-nya.">
      ![Ringkasan enterprise application Microsoft Entra untuk anthropic-cmek-client-us, yang menampilkan Application ID dan Object ID-nya.](https://platform.claude.com/docs/images/cmek/azure-service-principal.png)
    </Frame>
  </Step>

  <Step title="Buat kunci RSA di vault Anda">
    Azure Key Vault tidak mendukung symmetric key wrapping, sehingga kunci harus berupa RSA (3072-bit atau lebih besar) dengan `wrapKey` dan `unwrapKey` dalam operasi yang diizinkan.

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
      ![Halaman Create a key di Azure Key Vault dengan opsi Generate, tipe kunci RSA, dan ukuran kunci RSA 3072 dipilih.](https://platform.claude.com/docs/images/cmek/azure-create-key.png)
    </Frame>

    <Frame caption="Batasi Permitted operations (operasi yang diizinkan) ke Wrap Key dan Unwrap Key.">
      ![Versi kunci Azure Key Vault dengan Permitted operations dibatasi ke Wrap Key dan Unwrap Key.](https://platform.claude.com/docs/images/cmek/azure-permitted-operations.png)
    </Frame>
  </Step>

  <Step title="Berikan akses ke kunci Anda kepada service principal Anthropic">
    Tetapkan peran `Key Vault Crypto User` ke service principal dari langkah pertama, dengan cakupan pada **kunci individual**, bukan seluruh vault.

    ```bash
    VAULT_ID=$(az keyvault show --name <your-vault-name> --query id -o tsv)

    az role assignment create \
      --role "Key Vault Crypto User" \
      --assignee-object-id <sp-object-id> \
      --assignee-principal-type ServicePrincipal \
      --scope "${VAULT_ID}/keys/<your-key-name>"
    ```

    Peran bawaan `Key Vault Crypto User` memberikan operasi kriptografi kunci (encrypt, decrypt, wrap, unwrap, sign, verify) ditambah pembacaan kunci pada cakupan yang ditetapkan. Pembatasan `--ops wrapKey unwrapKey` yang Anda atur pada kunci di langkah sebelumnya semakin mempersempit operasi mana yang dapat berhasil terhadap kunci ini, sehingga dalam praktiknya Anthropic hanya dapat melakukan wrap dan unwrap.

    Dari Portal, buka **kunci** (bukan vault), pilih tab **Access control (IAM)**, klik **Add > Add role assignment**, pilih **Key Vault Crypto User**, dan tetapkan ke service principal `anthropic-cmek-client-us`.

    <Note>
      **Alternatif vault khusus:** Microsoft merekomendasikan vault khusus per aplikasi dengan peran yang ditetapkan pada cakupan vault. Jika Anda menyediakan vault yang hanya menyimpan kunci CMEK Anthropic ini, Anda dapat menetapkan peran pada cakupan vault sebagai gantinya dan efeknya identik. Gunakan cakupan pada kunci individual ketika kunci berada di vault bersama.
    </Note>

    <Frame caption="Tetapkan Key Vault Crypto User ke service principal Anthropic, dengan cakupan pada kunci.">
      ![Penetapan peran IAM Key Vault yang menampilkan anthropic-cmek-client-us diberi peran Key Vault Crypto User.](https://platform.claude.com/docs/images/cmek/azure-role-assignment.png)
    </Frame>
  </Step>

  <Step title="Verifikasi konfigurasi vault Anda">
    ```bash
    az keyvault show --name <your-vault-name> \
      --query "{rbac:properties.enableRbacAuthorization, purge:properties.enablePurgeProtection, pub:properties.publicNetworkAccess, net:properties.networkAcls.defaultAction, ipRules:properties.networkAcls.ipRules, uri:properties.vaultUri, tenantId:properties.tenantId}"
    ```

    Pastikan bahwa:

    * `rbac` bernilai `true`.
    * `purge` bernilai `true`. Jika bernilai `false` atau `null`, aktifkan purge protection pada vault sebelum melanjutkan. Tanpanya, kunci yang di-soft-delete dapat di-purge secara permanen selama jendela retensi, sehingga data terlindungi CMEK Anda tidak dapat dipulihkan.
    * `pub` bernilai `"Enabled"`. Jika bernilai `"Disabled"`, Anthropic tidak dapat menjangkau vault melalui endpoint data-plane publiknya dan validasi akan gagal.
    * `net` bernilai `"Allow"`, atau, jika bernilai `"Deny"`, pastikan `ipRules` mencakup rentang egress Anthropic (hubungi Anthropic untuk daftar terbaru).
    * `uri` adalah URI vault yang Anda gunakan saat mendaftarkan kunci.
    * `tenantId` adalah tenant yang mengatur vault. Gunakan nilai ini sebagai `tenant_id` saat Anda mendaftarkan kunci, bukan tenant dari subscription Anda yang sedang aktif (keduanya dapat berbeda dalam penyiapan lintas tenant).
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API.

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
          ant beta:organization:external-keys create <<'YAML'
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

          external_key = client.beta.organization.external_keys.create(
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

          const externalKey = await client.beta.organization.externalKeys.create({
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
          using Anthropic.Models.Beta.Organization.ExternalKeys;

          AnthropicClient client = new();

          var externalKey = await client.Beta.Organization.ExternalKeys.Create(new()
          {
              DisplayName = "<friendly-name>",
              Geo = Geo.Us,
              ProviderConfig = new BetaAzureExternalKeyConfigParam
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

          externalKey, err := client.Beta.Organization.ExternalKeys.New(context.Background(), anthropic.BetaOrganizationExternalKeyNewParams{
          	DisplayName: anthropic.String("<friendly-name>"),
          	Geo:         anthropic.BetaOrganizationExternalKeyNewParamsGeoUs,
          	ProviderConfig: anthropic.BetaOrganizationExternalKeyNewParamsProviderConfigUnion{
          		OfAzure: &anthropic.BetaAzureExternalKeyConfigParam{
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
          import com.anthropic.models.beta.organization.externalkeys.BetaAzureExternalKeyConfigParam;
          import com.anthropic.models.beta.organization.externalkeys.ExternalKeyCreateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = ExternalKeyCreateParams.builder()
                  .displayName("<friendly-name>")
                  .geo(ExternalKeyCreateParams.Geo.US)
                  .providerConfig(BetaAzureExternalKeyConfigParam.builder()
                      .vaultUri("https://<your-vault-name>.vault.azure.net/")
                      .keyName("<your-key-name>")
                      .tenantId("<your-tenant-id>")
                      .build())
                  .build();
              var externalKey = client.beta().organization().externalKeys().create(params);

              IO.println("id: " + externalKey.id());
              IO.println("display_name: " + externalKey.displayName().orElseThrow());
          }
          ```

          ```php PHP
          use Anthropic\Beta\Organization\ExternalKeys\ExternalKeyCreateParams\Geo;
          // ...

          $client = new Client();

          $externalKey = $client->beta->organization->externalKeys->create(
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

          external_key = client.beta.organization.external_keys.create(
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
        Picu proses encrypt dan decrypt bolak-balik terhadap kunci Anda. Ini memastikan bahwa Anthropic dapat melakukan autentikasi ke tenant Anda dan melakukan operasi wrap dan unwrap.

        <CodeGroup>
          ```bash cURL
          curl -sS -X POST "https://api.anthropic.com/v1/organizations/external_keys/ekey_<id>/validate" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01"
          ```

          ```bash CLI
          ant beta:organization:external-keys validate --external-key-id "ekey_<id>"
          ```

          ```python Python
          client = anthropic.Anthropic()

          validation = client.beta.organization.external_keys.validate("ekey_<id>")

          print(f"status: {validation.status}")
          print(f"error: {validation.error}")
          ```

          ```typescript TypeScript
          const client = new Anthropic();

          const validation = await client.beta.organization.externalKeys.validate("ekey_<id>");

          console.log(`status: ${validation.status}`);
          console.log(`error: ${validation.error}`);
          ```

          ```csharp C#
          AnthropicClient client = new();

          var validation = await client.Beta.Organization.ExternalKeys.Validate("ekey_<id>");

          Console.WriteLine($"status: {validation.Status.Raw()}");
          Console.WriteLine($"error: {validation.Error}");
          ```

          ```go Go
          client := anthropic.NewClient()

          validation, err := client.Beta.Organization.ExternalKeys.Validate(context.Background(), "ekey_<id>")
          if err != nil {
          	log.Fatal(err)
          }

          fmt.Printf("status: %s\n", validation.Status)
          fmt.Printf("error: %s\n", validation.Error)
          ```

          ```java Java
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          var validation = client.beta().organization().externalKeys().validate("ekey_<id>");

          IO.println("status: " + validation.status().asString());
          IO.println("error: " + validation.error().orElse(""));
          ```

          ```php PHP
          $client = new Client();

          $validation = $client->beta->organization->externalKeys->validate(
              externalKeyID: 'ekey_<id>',
          );

          echo "status: {$validation->status}\n";
          echo "error: {$validation->error}\n";
          ```

          ```ruby Ruby
          client = Anthropic::Client.new

          validation = client.beta.organization.external_keys.validate("ekey_<id>")

          puts "status: #{validation.status}"
          puts "error: #{validation.error}"
          ```
        </CodeGroup>

        Respons yang berhasil terlihat seperti ini:

        ```json
        { "type": "external_key_validation", "status": "success", "error": null }
        ```

        Jika validasi gagal, field `error` menjelaskan masalahnya. Penyebab umumnya adalah:

        * **Penundaan propagasi RBAC:** penetapan peran dapat memerlukan beberapa menit untuk berlaku. Tunggu dan coba lagi.
        * **ACL jaringan memblokir Anthropic:** pastikan akses jaringan publik dan `ipRules` seperti yang dijelaskan pada langkah verifikasi.
        * **Kebijakan conditional access pada workload identity:** jika tenant Anda memiliki kebijakan conditional access yang menargetkan service principal, kecualikan service principal Anthropic atau tambahkan rentang egress Anthropic ke named locations kebijakan tersebut.
      </Step>

      <Step title="Lampirkan kunci ke workspace">
        Setelah kunci divalidasi, lampirkan ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan waktu [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

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
          ant beta:organization:workspaces update \
            --workspace-id "<workspace-id>" \
            --external-key-id "ekey_<id>"
          ```

          ```python Python
          client = anthropic.Anthropic()

          workspace = client.beta.organization.workspaces.update(
              "<workspace-id>", external_key_id="ekey_<id>"
          )

          print(f"id: {workspace.id}")
          print(f"external_key_id: {workspace.external_key_id}")
          ```

          ```typescript TypeScript
          const client = new Anthropic();

          const workspace = await client.beta.organization.workspaces.update("<workspace-id>", {
            external_key_id: "ekey_<id>"
          });

          console.log(`id: ${workspace.id}`);
          console.log(`external_key_id: ${workspace.external_key_id}`);
          ```

          ```csharp C#
          AnthropicClient client = new();

          var workspace = await client.Beta.Organization.Workspaces.Update("<workspace-id>", new()
          {
              ExternalKeyID = "ekey_<id>"
          });

          Console.WriteLine($"id: {workspace.ID}");
          Console.WriteLine($"external_key_id: {workspace.ExternalKeyID}");
          ```

          ```go Go
          client := anthropic.NewClient()

          workspace, err := client.Beta.Organization.Workspaces.Update(
          	context.Background(),
          	"<workspace-id>",
          	anthropic.BetaOrganizationWorkspaceUpdateParams{
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
          import com.anthropic.models.beta.organization.workspaces.WorkspaceUpdateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = WorkspaceUpdateParams.builder()
                  .externalKeyId("ekey_<id>")
                  .build();
              var workspace = client.beta().organization().workspaces().update("<workspace-id>", params);

              IO.println("id: " + workspace.id());
              IO.println("external_key_id: " + workspace.externalKeyId().orElseThrow());
          }
          ```

          ```php PHP
          $client = new Client();

          $workspace = $client->beta->organization->workspaces->update(
              workspaceID: '<workspace-id>',
              externalKeyID: 'ekey_<id>',
          );

          echo "id: {$workspace->id}\n";
          echo "external_key_id: {$workspace->externalKeyID}\n";
          ```

          ```ruby Ruby
          client = Anthropic::Client.new

          workspace = client.beta.organization.workspaces.update(
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

  <Tab title="Claude Enterprise">
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Azure**, masukkan URI vault, nama kunci, dan tenant ID dari langkah verifikasi, lalu klik **Continue**. Anthropic memvalidasi kunci dengan proses encrypt dan decrypt bolak-balik. Setelah kunci ditampilkan sebagai terverifikasi, organisasi Anda terlindungi CMEK sejak saat itu.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan satu organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `azurerm` dan `azuread`.
