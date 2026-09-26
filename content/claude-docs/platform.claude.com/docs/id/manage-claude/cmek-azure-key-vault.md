---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
fetched_at: 2026-09-26T02:19:50.539049Z
sha256: 568e6d6c7edde169038809a04c5f213a103d6f3a0b26bae86b8d720308e4cc2e
---

---
title: Mengonfigurasi Azure Key Vault untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault
description: Gunakan Azure Key Vault untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Azure Key Vault"
```

Panduan ini memandu Anda mengonfigurasi kunci Azure Key Vault sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci Key Vault Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda mulai.
</Warning>

## Prasyarat

* Sebuah Azure Key Vault dengan **otorisasi RBAC diaktifkan** (`enableRbacAuthorization: true`) dan **akses jaringan publik diizinkan**. Anthropic memanggil vault Anda melalui endpoint data-plane publik; private endpoint tidak didukung.
* **Perlindungan purge diaktifkan** (`enablePurgeProtection: true`) pada vault. Tanpa itu, kunci yang dihapus dapat di-purge secara permanen selama jendela retensi soft-delete, menyebabkan kehilangan data yang dilindungi CMEK Anda secara tidak dapat dipulihkan. Perlindungan purge tidak dapat dinonaktifkan setelah diaktifkan.
* Izin untuk membuat kunci di vault dan untuk menetapkan peran RBAC padanya.
* Izin untuk membuat service principal di tenant Entra Anda (`Application Administrator`, `Cloud Application Administrator`, atau peran kustom yang setara).
* Sebuah kunci Admin API Anthropic untuk organisasi Anda.
* [`az` CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) terinstal dan terautentikasi.
* **Diagnostic Settings** dikonfigurasi pada vault untuk merutekan kategori log `AuditEvent` ke Log Analytics, akun penyimpanan, atau event hub. Azure Key Vault tidak memancarkan log audit data-plane (seperti `KeyWrap`, `KeyUnwrap`, dan `KeyGet`) secara default, jadi tanpa ini Anda tidak mendapatkan jejak audit untuk operasi kunci Anthropic.

## Informasi aplikasi Anthropic

Agar Anthropic menggunakan kunci enkripsi Anda, Anda harus mengonfigurasi ID aplikasi multitenant Anthropic dan nama tampilan. Nilai-nilai tersebut adalah:

| Field                          | Value                                  |
| ------------------------------ | -------------------------------------- |
| Multitenant app client ID (US) | `8635ae1a-3e5d-44e8-a4ed-e0f614466f87` |
| App display name               | `anthropic-cmek-client-us`             |

<Warning>
  Gunakan hanya client ID dan nama tampilan yang dipublikasikan ini. Jangan pernah mempercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Menyetujui aplikasi multitenant Anthropic">
    Ini membuat service principal di tenant Entra Anda untuk aplikasi client CMEK Anthropic. Aplikasi tidak meminta izin Microsoft Graph; aplikasi ini ada semata-mata sebagai target federasi untuk akses data-plane Key Vault.

    ```bash
    az ad sp create --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87
    ```

    Dari output, tangkap field `id`. Ini adalah object ID service principal di tenant Anda, yang Anda gunakan saat menetapkan peran RBAC.

    ```json
    {
      "appId": "8635ae1a-3e5d-44e8-a4ed-e0f614466f87",
      "displayName": "anthropic-cmek-client-us",
      "id": "<sp-object-id>"
    }
    ```

    Jika service principal sudah ada di tenant Anda (dari upaya sebelumnya atau integrasi lain), `az ad sp create` keluar dengan error "already exists". Ambil object ID-nya sebagai gantinya:

    ```bash
    az ad sp show --id 8635ae1a-3e5d-44e8-a4ed-e0f614466f87 --query id -o tsv
    ```

    Langkah ini tidak memiliki padanan di Portal. Jika Anda tidak memiliki Azure CLI terinstal secara lokal, buka Cloud Shell dari bilah navigasi atas Portal. Setelah perintah berhasil, Anda dapat menemukan object ID service principal di **Microsoft Entra ID > Enterprise applications** dengan menghapus filter tipe aplikasi default dan mencari `anthropic-cmek-client-us`.

    <Frame caption="Temukan Object ID service principal pada ikhtisar aplikasi enterprise Entra-nya.">
      ![Ikhtisar aplikasi enterprise Microsoft Entra untuk anthropic-cmek-client-us, yang menampilkan Application ID dan Object ID-nya.](https://platform.claude.com/docs/images/cmek/azure-service-principal.png)
    </Frame>
  </Step>

  <Step title="Membuat kunci RSA di vault Anda">
    Azure Key Vault tidak mendukung pembungkusan kunci simetris, jadi kunci harus berupa RSA (3072-bit atau lebih besar) dengan `wrapKey` dan `unwrapKey` dalam operasi yang diizinkannya.

    Opsi `--tags` menambahkan tag organisasi, `anthropic-org-<ORGANIZATION_UUID>` dengan nilai `true`, di mana `<ORGANIZATION_UUID>` adalah ID organisasi Anthropic Anda dalam huruf kecil. Tag ini diperlukan agar Anthropic dapat memvalidasi kunci.

    <Note>
      **Menemukan ID organisasi Anda:** Salin field **Organization ID** di bawah **Settings > Organization** di Claude Console, atau di bawah **Organization settings > Organization** di claude.ai, atau baca field `id` dari endpoint [Organization Info](https://platform.claude.com/docs/id/api/beta/organization/retrieve). Gunakan UUID polos, bukan ID berawalan `org_`.
    </Note>

    ```bash
    az keyvault key create \
      --vault-name <VAULT_NAME> \
      --name <KEY_NAME> \
      --kty RSA --size 3072 \
      --ops wrapKey unwrapKey \
      --tags anthropic-org-<ORGANIZATION_UUID>=true
    ```

    Untuk kunci yang didukung HSM, gunakan `--kty RSA-HSM` (memerlukan vault Premium-SKU). Kunci RSA yang dilindungi perangkat lunak dapat diterima untuk integrasi ini.

    Dari Portal, buka Key Vault Anda, pilih **Keys**, lalu **Generate/Import**. Atur tipe kunci ke RSA dan ukuran ke 3072 atau lebih besar. Untuk membatasi kunci hanya untuk wrap dan unwrap, buka versi kunci, gulir ke **Permitted operations**, dan hapus centang semuanya kecuali **Wrap Key** dan **Unwrap Key**.

    Pada halaman **Create a key**, tambahkan juga tag organisasi di bawah **Tags**.

    <Frame caption="Buat kunci RSA berukuran 3072 atau lebih besar, dengan tag anthropic-org-<ORGANIZATION_UUID> diatur ke true.">
      ![Halaman Create a key di Azure Key Vault dengan RSA, ukuran kunci 3072, dan tag anthropic-org diatur ke true.](https://platform.claude.com/docs/images/cmek/azure-create-key-tag.png)
    </Frame>

    <Frame caption="Batasi operasi yang diizinkan ke Wrap Key dan Unwrap Key. Versi kunci menampilkan tag organisasi.">
      ![Versi kunci di Azure Key Vault dengan 1 tag dan Permitted operations dibatasi ke Wrap Key dan Unwrap Key.](https://platform.claude.com/docs/images/cmek/azure-permitted-operations-tag.png)
    </Frame>

    Untuk berbagi satu kunci di antara beberapa organisasi Anthropic, tambahkan satu tag semacam itu untuk setiap organisasi. Sebuah versi kunci dapat membawa paling banyak 15 tag, termasuk milik Anda sendiri.

    <Note>
      Untuk menambahkan tag ke kunci yang sudah Anda miliki, buka versi kunci saat ini di Portal, pilih tautan di sebelah **Tags**, tambahkan tag, dan klik **Save**. Dengan Azure CLI, jalankan `az keyvault key set-attributes --vault-name <VAULT_NAME> --name <KEY_NAME> --tags anthropic-org-<ORGANIZATION_UUID>=true`. Opsi `--tags`-nya menggantikan tag versi, jadi masukkan juga setiap tag yang sudah dimiliki versi tersebut di `--tags`, sebagai `name=value`. Untuk kunci di Managed HSM, gunakan `--hsm-name <HSM_NAME>` alih-alih `--vault-name`.
    </Note>
  </Step>

  <Step title="Memberikan service principal Anthropic akses ke kunci Anda">
    Tetapkan peran `Key Vault Crypto User` ke service principal dari langkah pertama, dengan cakupan ke **kunci individual** alih-alih seluruh vault.

    ```bash
    VAULT_ID=$(az keyvault show --name <your-vault-name> --query id -o tsv)

    az role assignment create \
      --role "Key Vault Crypto User" \
      --assignee-object-id <sp-object-id> \
      --assignee-principal-type ServicePrincipal \
      --scope "${VAULT_ID}/keys/<your-key-name>"
    ```

    Peran bawaan `Key Vault Crypto User` memberikan operasi kriptografi kunci (encrypt, decrypt, wrap, unwrap, sign, verify) ditambah pembacaan kunci pada cakupan yang ditetapkannya. Pembatasan `--ops wrapKey unwrapKey` yang Anda atur pada kunci di langkah sebelumnya lebih lanjut mempersempit operasi mana dari operasi tersebut yang dapat berhasil terhadap kunci ini, sehingga dalam praktiknya Anthropic hanya dapat melakukan wrap dan unwrap.

    Dari Portal, buka **kunci** (bukan vault), pilih tab **Access control (IAM)**-nya, klik **Add > Add role assignment**, pilih **Key Vault Crypto User**, dan tetapkan ke service principal `anthropic-cmek-client-us`.

    <Note>
      **Alternatif vault khusus:** Microsoft merekomendasikan vault khusus per aplikasi dengan peran yang ditetapkan pada cakupan vault. Jika Anda menyediakan vault yang hanya menyimpan kunci CMEK Anthropic ini, Anda dapat menetapkan peran pada cakupan vault sebagai gantinya dan efeknya identik. Cakupkan ke kunci individual ketika kunci berada di vault bersama.
    </Note>

    <Frame caption="Tetapkan Key Vault Crypto User ke service principal Anthropic, dengan cakupan ke kunci.">
      ![Penetapan peran IAM Key Vault yang menunjukkan peran Key Vault Crypto User ditetapkan ke anthropic-cmek-client-us.](https://platform.claude.com/docs/images/cmek/azure-role-assignment.png)
    </Frame>
  </Step>

  <Step title="Memverifikasi konfigurasi vault Anda">
    ```bash
    az keyvault show --name <your-vault-name> \
      --query "{rbac:properties.enableRbacAuthorization, purge:properties.enablePurgeProtection, pub:properties.publicNetworkAccess, net:properties.networkAcls.defaultAction, ipRules:properties.networkAcls.ipRules, uri:properties.vaultUri, tenantId:properties.tenantId}"
    ```

    Konfirmasikan bahwa:

    * `rbac` adalah `true`.
    * `purge` adalah `true`. Jika `false` atau `null`, aktifkan perlindungan purge pada vault sebelum melanjutkan. Tanpa itu, kunci yang di-soft-delete dapat di-purge secara permanen selama jendela retensi, membuat data yang dilindungi CMEK Anda tidak dapat dipulihkan.
    * `pub` adalah `"Enabled"`. Jika `"Disabled"`, Anthropic tidak dapat menjangkau vault melalui endpoint data-plane publiknya dan validasi gagal.
    * `net` adalah `"Allow"`, atau, jika `"Deny"`, bahwa `ipRules` menyertakan rentang egress Anthropic (hubungi Anthropic untuk daftar terkini).
    * `uri` adalah URI vault yang Anda gunakan saat mendaftarkan kunci.
    * `tenantId` adalah tenant yang mengatur vault. Gunakan nilai ini sebagai `tenant_id` saat Anda mendaftarkan kunci, bukan tenant dari langganan yang sedang aktif saat ini (keduanya dapat berbeda dalam penyiapan lintas-tenant).
  </Step>
</Steps>

## Mendaftarkan kunci dengan Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk mana yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    Anda dapat menyiapkan kunci di Claude Console atau melalui Admin API, dengan hasil yang sama.

    <Tabs>
      <Tab title="Claude Console">
        <Steps>
          <Step title="Mendaftarkan kunci dengan Anthropic">
            Di Claude Console, buka **Settings > Encryption keys** dan klik **Add key**. Masukkan nama tampilan, pilih **Azure Key Vault**, dan klik **Continue**. Isi **Vault URI**, **Key name**, dan **Tenant ID**, lalu klik **Add**.

            Langkah detail kunci menampilkan tag organisasi. Tambahkan ke kunci, seperti yang dijelaskan [langkah pembuatan](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#organization-tag), sebelum Anda klik **Add**.
          </Step>

          <Step title="Memvalidasi kunci">
            Pada halaman **Encryption keys**, klik **Verify** di sebelah kunci. **Connected** muncul ketika pemeriksaan lolos. Jika gagal, sebuah pesan memberikan alasannya.
          </Step>

          <Step title="Melampirkan kunci ke workspace">
            Di Claude Console, buka [Manage > Security](https://platform.claude.com/settings/workspaces/default/security-compliance) dan pilih workspace di pemilih workspace di bagian atas sidebar. Di bawah **Encryption key**, pilih kunci, klik **Save**, dan konfirmasikan. Melampirkan kunci tidak dapat dibatalkan. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).
          </Step>
        </Steps>
      </Tab>

      <Tab title="API">
        <Steps>
          <Step title="Mendaftarkan kunci dengan Anthropic">
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

          <Step title="Memvalidasi kunci">
            Picu round-trip encrypt dan decrypt terhadap kunci Anda. Ini mengonfirmasi bahwa Anthropic dapat mengautentikasi ke tenant Anda dan melakukan operasi wrap dan unwrap.

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

            Jika validasi gagal, field `error` menjelaskan masalahnya. Penyebab umum adalah:

            * **Penundaan propagasi RBAC:** penetapan peran dapat memerlukan beberapa menit untuk berlaku. Tunggu dan coba lagi.
            * **Network ACL memblokir Anthropic:** konfirmasikan akses jaringan publik dan `ipRules` seperti yang dijelaskan dalam langkah verifikasi.
            * **Kebijakan conditional access pada workload identity:** jika tenant Anda memiliki kebijakan conditional access yang menargetkan service principal, kecualikan service principal Anthropic atau tambahkan rentang egress Anthropic ke named location kebijakan.
          </Step>

          <Step title="Melampirkan kunci ke workspace">
            Setelah kunci divalidasi, lampirkan ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).

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
    </Tabs>
  </Tab>

  <Tab title="Claude Enterprise">
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Azure**, masukkan URI vault, nama kunci, dan tenant ID dari langkah verifikasi, lalu klik **Continue**. Anthropic memvalidasi kunci dengan round-trip encrypt dan decrypt. Setelah ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK mulai dari titik itu.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, jadi tidak ada langkah lampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `azurerm` dan `azuread`.
