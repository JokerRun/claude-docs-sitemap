---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 93053e0d3ae165db60cdde7aa50e8c4933abcea64e4897eb1a86f39a02c5f1c0
---

---
title: Mengonfigurasi AWS KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
description: Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with AWS KMS"
```

Panduan ini menjelaskan cara mengonfigurasi kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

<Note>
  **Claude Platform on AWS:** Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), kebijakan kunci Anda memberikan akses ke principal layanan AWS alih-alih peran IAM Anthropic, tidak ada langkah validasi terpisah, dan Anda mendaftarkan serta melampirkan kunci di Claude Console. Ikuti [Menyiapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) pada halaman ini alih-alih langkah-langkah di bagian berikutnya.
</Note>

## Prasyarat

* Akun AWS dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Kunci Admin API Anthropic untuk organisasi Anda.
* [AWS CLI](https://aws.amazon.com/cli/) yang terpasang dan terautentikasi.

## Amazon Resource Name (ARN) untuk Anthropic

Agar Anthropic menggunakan kunci enkripsi Anda, Anda harus memberikan peran IAM Anthropic sebuah kunci KMS yang dapat digunakannya untuk mengenkripsi data. ARN untuk Anthropic CMEK adalah:

```text wrap
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Membuat kunci KMS dengan kebijakan kunci lintas-akun">
    Kebijakan kunci memberikan peran IAM Anthropic akses lintas-akun. Tiga pernyataan diperlukan:

    1. **Admin root akun:** pola KMS standar. Akun Anda mempertahankan kontrol admin penuh.
    2. **Enkripsi dan dekripsi Anthropic:** aksi `kms:Encrypt` dan `kms:Decrypt`, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda (enkripsi envelope).
    3. **Describe Anthropic:** pembacaan metadata yang dilakukan Anthropic saat startup. Ini diberikan secara terpisah karena `DescribeKey` tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada aksi ini akan selalu menolak.

    ```bash
    export YOUR_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

    aws kms create-key \
      --region <region> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [
          {
            \"Sid\": \"AccountRootAdmin\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::${YOUR_ACCOUNT}:root\"},
            \"Action\": \"kms:*\",
            \"Resource\": \"*\"
          },
          {
            \"Sid\": \"AllowAnthropicCMEKCrypto\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::915198916910:role/anthropic-cmek-client-us\"},
            \"Action\": [\"kms:Encrypt\", \"kms:Decrypt\"],
            \"Resource\": \"*\",
            \"Condition\": {
              \"StringEquals\": {
                \"kms:EncryptionContext:anthropic:compartment_uuid\": [
                  \"00000000-0000-0000-0000-000000000000\",
                  \"<compartment-uuid>\"
                ]
              }
            }
          },
          {
            \"Sid\": \"AllowAnthropicCMEKDescribe\",
            \"Effect\": \"Allow\",
            \"Principal\": {\"AWS\": \"arn:aws:iam::915198916910:role/anthropic-cmek-client-us\"},
            \"Action\": \"kms:DescribeKey\",
            \"Resource\": \"*\"
          }
        ]
      }"
    ```

    Tangkap `KeyMetadata.Arn` dari output. Anda membutuhkannya saat mendaftarkan kunci di langkah berikutnya.

    Kondisi `EncryptionContext` direkomendasikan tetapi opsional. Anthropic selalu menyertakan ID compartment workspace Anda dalam konteks enkripsi, sehingga ciphertext terikat secara kriptografis ke compartment tersebut terlepas dari apa pun. Menambahkan kondisi ini memberikan defense-in-depth pada lapisan IAM. Untuk memulai tanpanya, hilangkan blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan tambahkan nanti dengan `kms:PutKeyPolicy`.

    <Note>
      **Menemukan ID compartment Anda:** Tempat menemukan ID compartment Anda berbeda antara Claude Platform dan Claude Enterprise. Lihat tab **Claude Platform** dan **Claude Enterprise** di bawah **Mendaftarkan kunci dengan Anthropic**.
    </Note>

    Anda juga dapat membuat kunci dari AWS Console. Pilih kunci simetris dengan penggunaan kunci enkripsi dan dekripsi, kunci single-region, dan asal material kunci KMS. Wizard Create-key menetapkan kebijakan kunci pada langkah **Review**-nya: Jika Anda menambahkan ID akun Anthropic `915198916910` di bawah izin penggunaan kunci di sana, kebijakan yang dihasilkan memberikan seluruh akun Anthropic aksi yang lebih luas (seperti `kms:ReEncrypt*` dan `kms:GenerateDataKey*`) tanpa kondisi `EncryptionContext`, dan validasi tetap akan berhasil terhadapnya. Untuk menghindari meninggalkan kunci yang terlalu permisif, selesaikan wizard hanya dengan izin administratif, lalu buka tab **Key policy** kunci dan ganti JSON dengan kebijakan yang dibatasi peran yang ditunjukkan sebelumnya (tiga pernyataan yang dibatasi ke peran `anthropic-cmek-client-us`, dengan kondisi `EncryptionContext`).

    <Frame caption="Configure key: symmetric, encrypt and decrypt, single-region key.">
      ![AWS KMS Create key wizard on the Configure key step, with Symmetric key type, Encrypt and decrypt key usage, and Single-Region key selected.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
    </Frame>

    <Frame caption="Tambahkan alias dan deskripsi untuk kunci.">
      ![AWS KMS Add labels step with an alias of anthropic-cmek and a description of Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
    </Frame>

    <Frame caption="Tentukan izin administratif kunci (opsional). Akun Anda mempertahankan kontrol admin penuh.">
      ![AWS KMS Define key administrative permissions step listing IAM roles that can administer the key.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
    </Frame>

    <Frame caption="Jangan tambahkan ID akun Anthropic di sini. Langkah wizard ini menghasilkan kebijakan yang terlalu permisif. Biarkan izin penggunaan kosong dan edit JSON Key policy setelah pembuatan (lihat kebijakan kunci sebelumnya).">
      ![AWS KMS Define key usage permissions step with Anthropic's account ID entered under Other AWS accounts.](https://platform.claude.com/docs/images/cmek/aws-usage-permissions.png)
    </Frame>
  </Step>
</Steps>

## Mendaftarkan kunci dengan Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk mana yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Note>
      **Claude Platform on AWS:** Principal, kebijakan kunci, dan alur pendaftaran berbeda, dan tidak ada langkah validasi terpisah. Ikuti [Menyiapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) alih-alih tab ini.
    </Note>

    <Note>
      **Menemukan ID compartment Anda:** Setiap workspace memiliki ID compartment yang membatasi data CMEK-nya. Temukan di Claude Console di bawah **Workspace > Security**, di bawah **Encryption key** (bidang **Compartment ID**), atau baca bidang `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/admin-api/workspaces/get-workspace). Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci sebelumnya.

      Validasi kunci selalu mengirim UUID compartment semua-nol (`00000000-0000-0000-0000-000000000000`) sebagai konteks enkripsi, karena validasi berjalan sebelum kunci dilampirkan ke workspace mana pun. Lalu lintas langsung mengirim ID compartment dari setiap workspace yang dilampirkan.

      Kondisi `EncryptionContext` apa pun harus mengizinkan nilai semua-nol ditambah ID compartment dari setiap workspace tempat kunci dilampirkan. Validasi juga berjalan lagi setiap kali penyiapan kunci dijalankan ulang, jadi pertahankan entri semua-nol secara permanen.

      Untuk melampirkan kunci ke workspace tambahan, tambahkan ID compartment workspace tersebut ke kondisi dengan `kms:PutKeyPolicy` sebelum melampirkan.
    </Note>

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
                "type": "aws",
                "kms_arn": "<key-arn-from-create-key-step>"
              }
            }'
          ```

          ```bash CLI
          ant beta:organization:external-keys create <<'YAML'
          display_name: "<friendly-name>"
          geo: us
          provider_config:
            type: aws
            kms_arn: "<key-arn-from-create-key-step>"
          YAML
          ```

          ```python Python
          client = anthropic.Anthropic()

          external_key = client.beta.organization.external_keys.create(
              display_name="<friendly-name>",
              geo="us",
              provider_config={"type": "aws", "kms_arn": "<key-arn-from-create-key-step>"},
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
              type: "aws",
              kms_arn: "<key-arn-from-create-key-step>"
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
              ProviderConfig = new BetaAwsExternalKeyConfig
              {
                  KmsArn = "<key-arn-from-create-key-step>"
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
          		OfAWS: &anthropic.BetaAWSExternalKeyConfigParam{
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
          import com.anthropic.models.beta.organization.externalkeys.BetaAwsExternalKeyConfig;
          import com.anthropic.models.beta.organization.externalkeys.ExternalKeyCreateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = ExternalKeyCreateParams.builder()
                  .displayName("<friendly-name>")
                  .geo(ExternalKeyCreateParams.Geo.US)
                  .providerConfig(BetaAwsExternalKeyConfig.builder()
                      .kmsArn("<key-arn-from-create-key-step>")
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
                  'type' => 'aws',
                  'kmsARN' => '<key-arn-from-create-key-step>',
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
              type: :aws,
              kms_arn: "<key-arn-from-create-key-step>"
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
        Picu round-trip enkripsi dan dekripsi terhadap kunci Anda.

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

          external_key_id = "ekey_<id>"
          validation = client.beta.organization.external_keys.validate(external_key_id)

          puts "status: #{validation.status}"
          puts "error: #{validation.error}"
          ```
        </CodeGroup>

        Respons yang berhasil terlihat seperti ini:

        ```json
        { "type": "external_key_validation", "status": "success", "error": null }
        ```

        Jika validasi gagal, penyebab umumnya adalah:

        * **Ketidakcocokan konteks enkripsi:** Validasi gagal sementara lalu lintas data berfungsi (atau sebaliknya) dengan `AccessDeniedException` yang tidak jelas ketika kondisi `kms:EncryptionContext:anthropic:compartment_uuid` hanya mengizinkan salah satu dari dua nilai yang dikirim Anthropic. Validasi mengirim UUID semua-nol (`00000000-0000-0000-0000-000000000000`); lalu lintas langsung mengirim ID compartment workspace yang dilampirkan. Konfirmasikan bahwa kondisi mencantumkan keduanya. Untuk mengesampingkan kondisi sepenuhnya, hapus sementara blok `Condition` dari pernyataan `AllowAnthropicCMEKCrypto` dan validasi ulang.
        * **Resource control policies (RCPs):** Jika organisasi AWS Anda memiliki RCP yang menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan org Anda, ini memblokir peran lintas-akun Anthropic. RCP memerlukan pengecualian untuk kunci ini atau untuk ARN peran Anthropic. Service control policies tidak berlaku di sini, karena tidak dievaluasi untuk principal eksternal yang memanggil melalui kebijakan berbasis sumber daya.
        * **Akses diberikan melalui IAM alih-alih kebijakan kunci:** Akses KMS lintas-akun harus diberikan dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Periksa dengan `aws kms get-key-policy --key-id <id> --policy-name default`.
        * **Ketidakcocokan region:** Konfirmasikan bahwa region kunci adalah salah satu yang dioperasikan Anthropic untuk tingkat geo yang Anda konfigurasikan.
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

          workspace_id = "<workspace-id>"
          workspace = client.beta.organization.workspaces.update(
            workspace_id,
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
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **AWS** dan klik **Continue**, lalu tempel Key ARN dari langkah sebelumnya dan klik **Add**. Anthropic memvalidasi kunci dengan round-trip enkripsi dan dekripsi. Setelah ditampilkan sebagai terverifikasi, organisasi Anda terlindungi CMEK sejak saat itu.

    Langkah detail kunci dari alur ini menampilkan **Compartment ID** organisasi Anda dengan tombol salin. Gantikan nilai tersebut untuk `<compartment-uuid>` dalam kebijakan kunci (lihat langkah Membuat kunci KMS di bawah Penyiapan kunci enkripsi); Anda dapat membuka alur untuk menyalin ID sebelum membuat kunci. Setelah penyiapan, ID tetap terlihat pada kunci di bawah **Encryption keys**.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah lampir workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Menyiapkan CMEK di Claude Platform on AWS

Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya menggunakan kunci AWS KMS, dan penyiapan berbeda dari bagian sebelumnya dalam hal-hal berikut:

* **Principal:** Kebijakan kunci Anda memberikan akses ke principal layanan AWS `aws-external-anthropic.amazonaws.com`. Peran IAM dan ID akun Anthropic tidak digunakan, sehingga [ARN untuk Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#amazon-resource-name-arn-for-anthropic) tidak berlaku.
* **Persyaratan kunci:** Kunci harus berupa kunci KMS simetris dengan penggunaan enkripsi dan dekripsi, single-region, dan berada di akun serta region AWS yang sama dengan workspace tempat Anda melampirkannya. Kunci lintas-akun tidak didukung: kunci harus berada di akun AWS yang menghosting organisasi Anda. Kunci multi-region (ID kunci yang dimulai dengan `mrk-`) dan ARN alias ditolak saat Anda mendaftarkan kunci; gunakan ARN kunci.
* **Tidak ada langkah validasi terpisah:** Selain pemeriksaan pada ARN kunci saat pendaftaran, kunci divalidasi saat Anda melampirkannya ke workspace. Panggilan lampir melakukan round enkripsi/dekripsi terhadap kunci dengan ID compartment workspace tersebut sebagai konteks enkripsi, sehingga masalah kebijakan kunci muncul pada saat lampir alih-alih saat pendaftaran. Tidak seperti kebijakan Claude Platform sebelumnya pada halaman ini, kondisi `EncryptionContext` karenanya tidak memerlukan entri semua-nol.
* **Tempat Anda mengelola kunci:** Daftarkan dan lampirkan kunci di Claude Console, masuk melalui AWS dengan peran Admin. Endpoint kunci eksternal juga tersedia di Claude Platform on AWS, diotorisasi melalui [aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys); di sana, sebuah kunci diidentifikasi oleh ARN kunci KMS-nya alih-alih ID `ekey_`.

<Warning>
  Gunakan hanya nama principal layanan yang dipublikasikan ini. Jangan pernah memercayai pengidentifikasi yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

### Prasyarat

* Akun AWS yang menghosting organisasi Claude Platform on AWS Anda, dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Peran **Admin** di Claude Console untuk Claude Platform on AWS. Lihat [Menggunakan Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console).
* Untuk principal IAM yang Anda gunakan untuk masuk ke Claude Console: selain `aws-external-anthropic:AssumeConsole`, [aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys) untuk operasi yang Anda lakukan di sana, karena halaman Encryption keys dan pelampiran kunci melewati gateway AWS. Mendaftarkan kunci adalah `RegisterKey` (dengan `ListKeys` dan `GetKey` untuk melihat pendaftaran), dan melampirkan satu adalah `UpdateWorkspace` atau `CreateWorkspace`. Aksi kunci eksternal (dan `CreateWorkspace`) dibatasi akun, jadi berikan pada `Resource: "*"`; kebijakan yang dibatasi ke ARN workspace tidak menyertakannya.
* Untuk principal IAM yang melampirkan kunci ke workspace (identitas yang Anda gunakan untuk masuk ke Claude Console): `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci. Akses principal Anda ke kunci diperiksa saat Anda melampirkannya, selain principal layanan.
* Opsional, untuk pemilih kunci di Claude Console: `kms:ListKeys` dan `kms:DescribeKey` untuk principal yang Anda gunakan untuk masuk. Tanpanya, tempel ARN kunci sebagai gantinya.

### Membuat kunci KMS

Kebijakan kunci memiliki tiga pernyataan: pernyataan admin root akun Anda; pernyataan yang memungkinkan principal layanan Claude Platform on AWS mengenkripsi, mendekripsi, dan menghasilkan kunci data; dan pernyataan terpisah untuk `kms:DescribeKey`. Kedua pernyataan principal layanan membawa kondisi `aws:SourceArn` yang direkomendasikan: layanan memanggil kunci Anda atas nama workspace tertentu dan meneruskan [ARN workspace tersebut](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#service-details) sebagai ARN sumber, sehingga pola yang ditunjukkan membatasi pemberian ke workspace di akun AWS Anda sendiri. `DescribeKey` diberikan secara terpisah karena tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada aksi tersebut akan selalu menolak.

Jika Anda berencana menggunakan kondisi `EncryptionContext` opsional yang ditunjukkan di sini, buat workspace terlebih dahulu (tanpa kunci) dan salin ID compartment-nya dari Claude Console di bawah **Workspace > Security**, di bawah **Encryption key** (bidang **Compartment ID**), atau dari bidang `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/admin-api/workspaces/get-workspace). Gantikan untuk `<compartment-uuid>`. Jika tidak, hapus entri `StringEquals` dari blok `Condition` pernyataan tersebut dan pertahankan entri `ArnLike`.

```bash
export YOUR_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

aws kms create-key \
  --region <workspace-region> \
  --description "Anthropic CMEK (Claude Platform on AWS)" \
  --key-usage ENCRYPT_DECRYPT \
  --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Sid\": \"AccountRootAdmin\",
        \"Effect\": \"Allow\",
        \"Principal\": {\"AWS\": \"arn:aws:iam::${YOUR_ACCOUNT}:root\"},
        \"Action\": \"kms:*\",
        \"Resource\": \"*\"
      },
      {
        \"Sid\": \"AllowClaudePlatformOnAWSCrypto\",
        \"Effect\": \"Allow\",
        \"Principal\": {\"Service\": \"aws-external-anthropic.amazonaws.com\"},
        \"Action\": [\"kms:Encrypt\", \"kms:Decrypt\", \"kms:GenerateDataKey\"],
        \"Resource\": \"*\",
        \"Condition\": {
          \"ArnLike\": {
            \"aws:SourceArn\": \"arn:aws:aws-external-anthropic:*:${YOUR_ACCOUNT}:workspace/*\"
          },
          \"StringEquals\": {
            \"kms:EncryptionContext:anthropic:compartment_uuid\": [
              \"<compartment-uuid>\"
            ]
          }
        }
      },
      {
        \"Sid\": \"AllowClaudePlatformOnAWSDescribe\",
        \"Effect\": \"Allow\",
        \"Principal\": {\"Service\": \"aws-external-anthropic.amazonaws.com\"},
        \"Action\": \"kms:DescribeKey\",
        \"Resource\": \"*\",
        \"Condition\": {
          \"ArnLike\": {
            \"aws:SourceArn\": \"arn:aws:aws-external-anthropic:*:${YOUR_ACCOUNT}:workspace/*\"
          }
        }
      }
    ]
  }"
```

Tangkap `KeyMetadata.Arn` dari output. Anda membutuhkannya saat mendaftarkan kunci.

Kedua kondisi adalah pengerasan opsional, dan keduanya dapat digabungkan. Kondisi `aws:SourceArn` dapat ditulis sebelum workspace mana pun ada; untuk menyematkan kunci ke workspace tertentu alih-alih seluruh akun Anda, cantumkan ARN workspace lengkapnya sebagai ganti pola wildcard, dan untuk memulai tanpanya, hapus entri `ArnLike` dari kedua pernyataan principal layanan (menghapus blok `Condition` yang ditinggalkan kosong oleh ini). Kondisi `EncryptionContext` juga opsional. Setiap panggilan enkripsi, dekripsi, dan kunci data yang dibuat untuk workspace, termasuk pemeriksaan saat lampir, membawa ID compartment workspace tersebut sebagai `anthropic:compartment_uuid`, sehingga kondisi mencantumkan ID compartment dari setiap workspace tempat Anda melampirkan kunci dan tidak memerlukan entri semua-nol. Menambahkannya mengikat kunci ke workspace yang Anda cantumkan pada lapisan IAM juga. Karena ID compartment hanya ada setelah workspace-nya ada, urutannya adalah: buat workspace, masukkan ID compartment-nya ke dalam kondisi (saat pembuatan kunci, atau nanti dengan `kms:PutKeyPolicy`), lalu lampirkan kunci. Sebelum melampirkan kunci ke setiap workspace tambahan, tambahkan ID compartment workspace tersebut dengan cara yang sama. Untuk memulai tanpanya, hapus entri `StringEquals` dari blok `Condition` pernyataan `AllowClaudePlatformOnAWSCrypto`; jika Anda menambahkannya nanti, sertakan ID compartment dari setiap workspace tempat kunci sudah dilampirkan.

Anda juga dapat membuat kunci dari AWS Console: pilih kunci simetris dengan penggunaan kunci enkripsi dan dekripsi, kunci single-region, dan asal material kunci KMS, di region workspace. Biarkan izin penggunaan kunci kosong di wizard Create-key, lalu buka tab **Key policy** kunci dan ganti JSON dengan kebijakan yang ditunjukkan di sini.

### Mendaftarkan dan melampirkan kunci

<Steps>
  <Step title="Mendaftarkan kunci">
    Di Claude Console, buka **Settings > Encryption keys** dan klik **Add key**. Masukkan nama tampilan, lalu pilih kunci dari pemilih kunci atau pilih **Enter ARN manually** dan tempel ARN kunci, lalu klik **Add**. Kunci harus berada di akun AWS yang menghosting organisasi Anda; kunci lintas-akun tidak didukung. Pemilih mencantumkan kunci simetris single-region yang diaktifkan dan dikelola pelanggan di akun Anda di salah satu region organisasi Anda; untuk kunci yang tidak dicantumkan pemilih, masukkan ARN. Ini mencantumkan kunci hanya jika principal yang Anda gunakan untuk masuk dapat memanggil `kms:ListKeys` dan `kms:DescribeKey`.
  </Step>

  <Step title="Melampirkan kunci ke workspace">
    Lampirkan kunci ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works). Di Claude Console, buka workspace dan, di bawah **Security**, pilih kunci di **Encryption key**, simpan, dan konfirmasikan. Anda juga dapat memilih kunci saat membuat workspace di Claude Console, tetapi hanya jika kebijakan kunci Anda belum menamai workspace tertentu (tidak ada kondisi `EncryptionContext`, dan pola `aws:SourceArn` seluruh akun alih-alih ARN workspace individual), karena ID workspace dan ID compartment ditetapkan saat pembuatan. Setelah dilampirkan, kunci workspace tidak dapat diubah.

    Inilah saat kunci divalidasi: panggilan lampir memeriksa akses principal Anda ke kunci dan melakukan round enkripsi/dekripsi terhadapnya dengan ID compartment workspace sebagai konteks enkripsi, sehingga masalah dengan kebijakan kunci atau izin principal Anda muncul sebagai kesalahan pada panggilan tersebut. Jika lampir gagal dengan kesalahan akses KMS, periksa hal berikut:

    * Kebijakan kunci menamai principal layanan `aws-external-anthropic.amazonaws.com` dan memberikan `kms:Encrypt`, `kms:Decrypt`, dan `kms:GenerateDataKey`, ditambah `kms:DescribeKey` dalam pernyataan terpisah yang tidak memiliki kondisi `EncryptionContext`.
    * Kondisi `aws:SourceArn` cocok dengan ARN workspace ini (ID akun Anda, dan workspace jika Anda mencantumkan ARN tertentu), dan kondisi `EncryptionContext` apa pun menyertakan ID compartment workspace ini.
    * Kunci diaktifkan, single-region, dan berada di akun serta region AWS yang sama dengan workspace.
    * Principal yang Anda gunakan untuk masuk memiliki `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci.
    * Tidak ada service control policy atau resource control policy di organisasi AWS Anda yang mencegah principal layanan atau principal Anda menggunakan kunci.
    * Jika kebijakan terlihat benar dan lampir masih gagal, temukan event `kms:` yang ditolak di CloudTrail di akun kunci (ini menunjukkan principal pemanggil dan, untuk panggilan kriptografis, konteks enkripsi), lalu coba lagi dengan kondisi `aws:SourceArn` dihapus sementara untuk membedakan ketidakcocokan source-ARN dari ketidakcocokan konteks enkripsi.
  </Step>
</Steps>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke penyedia `aws` dengan sumber daya `aws_kms_key` dan `aws_kms_alias`.
