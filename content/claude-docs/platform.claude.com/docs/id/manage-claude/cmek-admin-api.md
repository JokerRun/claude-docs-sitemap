---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-admin-api
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 58e0eac55c6913f0fda96cf99552b85d772df77d4ba0a49b30a7ce79e91ccdfc
---

---
title: Menambahkan dan melampirkan kunci enkripsi dengan Admin API
url: https://platform.claude.com/docs/id/manage-claude/cmek-admin-api
description: Buat, validasi, dan lampirkan kunci enkripsi yang dikelola pelanggan dengan tiga panggilan Admin API.
---

Panggilan-panggilan ini berfungsi di Claude Platform. Di Claude Enterprise atau Claude Platform on AWS, ikuti [halaman penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/cmek#set-it-up).

Membuat kunci eksternal adalah apa yang dilakukan **Add key** di Claude Console, dan memvalidasinya adalah apa yang dilakukan **Verify**.

## Sebelum Anda memulai

* “Customer-managed encryption keys” (kunci enkripsi yang dikelola pelanggan), atau CMEK, telah [diaktifkan untuk organisasi Anda](https://platform.claude.com/docs/id/manage-claude/cmek#availability).
* Anda memiliki [kunci API Admin](https://platform.claude.com/docs/id/manage-claude/admin-api-keys). Contoh-contoh membacanya dari `ANTHROPIC_API_KEY`.
* Anda telah membuat kunci Anda di [AWS KMS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#encryption-key-setup), [Google Cloud KMS](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#encryption-key-setup), atau [Azure Key Vault](https://platform.claude.com/docs/id/manage-claude/cmek-azure-key-vault#encryption-key-setup), dan menyimpan nilai-nilai yang diminta untuk disalin oleh langkah-langkah penyiapan.
* Anda memiliki workspace yang [menyimpan data](https://platform.claude.com/docs/id/manage-claude/cmek-data-retention#data-retention), idealnya workspace baru, karena [data yang sudah ada tetap berada di bawah kunci milik Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect).

## Membuat, memvalidasi, dan melampirkan kunci

<Steps>
  <Step title="Buat kunci eksternal">
    <Tabs>
      <Tab title="AWS">
        Ganti `<friendly-name>` dengan nama tampilan dan `<key-arn-from-create-key-step>` dengan ARN kunci.

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
                "type": "aws",
                "kms_arn": "<key-arn-from-create-key-step>"
              }
            }'
          ```

          ```bash CLI
          ant organization:external-keys create <<'YAML'
          display_name: "<friendly-name>"
          geo: us
          provider_config:
            type: aws
            kms_arn: "<key-arn-from-create-key-step>"
          YAML
          ```

          ```python Python
          client = anthropic.Anthropic()

          external_key = client.organization.external_keys.create(
              display_name="<friendly-name>",
              geo="us",
              provider_config={"type": "aws", "kms_arn": "<key-arn-from-create-key-step>"},
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
              type: "aws",
              kms_arn: "<key-arn-from-create-key-step>"
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
              ProviderConfig = new AwsExternalKeyConfig
              {
                  KmsArn = "<key-arn-from-create-key-step>"
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
          		OfAWS: &anthropic.AWSExternalKeyConfigParam{
          			KMSARN: "<key-arn-from-create-key-step>",
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
          import com.anthropic.models.organization.externalkeys.AwsExternalKeyConfig;
          import com.anthropic.models.organization.externalkeys.ExternalKeyCreateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = ExternalKeyCreateParams.builder()
                  .displayName("<friendly-name>")
                  .geo(ExternalKeyCreateParams.Geo.US)
                  .providerConfig(AwsExternalKeyConfig.builder()
                      .kmsArn("<key-arn-from-create-key-step>")
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
                  'type' => 'aws',
                  'kmsARN' => '<key-arn-from-create-key-step>',
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
              type: :aws,
              kms_arn: "<key-arn-from-create-key-step>"
            }
          )

          puts "id: #{external_key.id}"
          puts "display_name: #{external_key.display_name}"
          ```
        </CodeGroup>
      </Tab>

      <Tab title="Google Cloud">
        Ganti `<friendly-name>` dengan nama tampilan. Ganti nilai yang diawali dengan `projects/` dengan nama resource kunci lengkap.

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
                "type": "gcp",
                "key_name": "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
              }
            }'
          ```

          ```bash CLI
          ant organization:external-keys create <<'YAML'
          display_name: "<friendly-name>"
          geo: us
          provider_config:
            type: gcp
            key_name: "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
          YAML
          ```

          ```python Python
          client = anthropic.Anthropic()

          external_key = client.organization.external_keys.create(
              display_name="<friendly-name>",
              geo="us",
              provider_config={
                  "type": "gcp",
                  "key_name": "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>",
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
              type: "gcp",
              key_name:
                "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
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
              ProviderConfig = new GcpExternalKeyConfig
              {
                  KeyName = "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
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
          		OfGCP: &anthropic.GCPExternalKeyConfigParam{
          			KeyName: "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>",
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
          import com.anthropic.models.organization.externalkeys.ExternalKeyCreateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = ExternalKeyCreateParams.builder()
                  .displayName("<friendly-name>")
                  .geo(ExternalKeyCreateParams.Geo.US)
                  .gcpProviderConfig("projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>")
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
                  'type' => 'gcp',
                  'keyName' => 'projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>',
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
              type: :gcp,
              key_name: "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
            }
          )

          puts "id: #{external_key.id}"
          puts "display_name: #{external_key.display_name}"
          ```
        </CodeGroup>
      </Tab>

      <Tab title="Azure">
        Ganti placeholder berikut:

        * `<friendly-name>`: nama tampilan
        * `https://<your-vault-name>.vault.azure.net/`: URI vault
        * `<your-key-name>`: nama kunci
        * `<your-tenant-id>`: ID tenant vault

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
      </Tab>
    </Tabs>

    `id` dalam respons adalah ID kunci eksternal. Salin untuk dua langkah berikutnya.

    ```json
    {
      "type": "external_key",
      "id": "ekey_<id>",
      "display_name": "<friendly-name>"
    }
    ```
  </Step>

  <Step title="Validasi kunci">
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

      external_key_id = "ekey_<id>"
      validation = client.organization.external_keys.validate(external_key_id)

      puts "status: #{validation.status}"
      puts "error: #{validation.error}"
      ```
    </CodeGroup>

    Respons yang berhasil terlihat seperti ini:

    ```json
    { "type": "external_key_validation", "status": "success", "error": null }
    ```

    Jika `status` bernilai `failure`, field `error` menyebutkan alasannya. Lihat [Memecahkan masalah CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting).
  </Step>

  <Step title="Lampirkan kunci ke workspace">
    <Warning>
      Melampirkan kunci [tidak dapat dibatalkan](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does). Jika kunci dihapus, Anthropic tidak dapat memulihkan data yang dilindunginya.
    </Warning>

    Ganti `<workspace-id>` dengan ID workspace, yang diawali dengan `wrkspc_`, dan `ekey_<id>` dengan ID kunci eksternal.

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

      workspace_id = "<workspace-id>"
      workspace = client.organization.workspaces.update(
        workspace_id,
        external_key_id: "ekey_<id>"
      )

      puts "id: #{workspace.id}"
      puts "external_key_id: #{workspace.external_key_id}"
      ```
    </CodeGroup>

    Respons menampilkan ID kunci yang dilampirkan di `external_key_id`. Jika permintaan ditolak, [cari errornya](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#refused).
  </Step>
</Steps>
