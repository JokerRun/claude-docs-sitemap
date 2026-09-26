---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-09-26T02:19:50.539049Z
sha256: 61158262a7eb63295ad2c68a770ce3cb134425e1783eeded03cf4fa8a1bc483a
---

---
title: Konfigurasikan AWS KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
description: Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with AWS KMS"
```

Panduan ini memandu proses konfigurasi kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

<Note>
  **Claude Platform on AWS:** Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), kebijakan kunci Anda memberikan akses ke principal layanan AWS alih-alih peran IAM Anthropic, tidak ada langkah validasi terpisah, dan Anda mendaftarkan serta melampirkan kunci di Claude Console. Ikuti [Siapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) pada halaman ini alih-alih langkah-langkah di bagian berikutnya.
</Note>

## Prasyarat

* Akun AWS dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Kunci Admin API untuk organisasi Anda.
* [AWS CLI](https://aws.amazon.com/cli/) terpasang dan terautentikasi.

## Amazon Resource Name (ARN) untuk Anthropic

Agar Anthropic menggunakan kunci enkripsi Anda, Anda harus memberikan peran IAM Anthropic sebuah kunci KMS yang dapat digunakannya untuk mengenkripsi data. ARN untuk Anthropic CMEK adalah:

```text wrap
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat kunci KMS dengan kebijakan kunci lintas akun">
    <Note>
      **Claude Platform on AWS:** Lewati langkah ini. Kebijakan kunci Anda memberikan akses ke principal layanan AWS, dan tidak memiliki kondisi organisasi. [Siapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) memberikan kebijakan tersebut.
    </Note>

    Kebijakan kunci memberikan peran IAM Anthropic akses lintas akun. Tiga pernyataan diperlukan:

    1. **Admin root akun:** pola KMS standar. Akun Anda mempertahankan kontrol admin penuh.
    2. **Enkripsi dan dekripsi Anthropic:** aksi `kms:Encrypt` dan `kms:Decrypt`, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi kunci data yang melindungi data workspace Anda (enkripsi envelope).
    3. **Describe Anthropic:** pembacaan metadata yang dilakukan Anthropic saat startup. Ini diberikan secara terpisah karena `DescribeKey` tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada aksi ini akan selalu menolak.

    Untuk menemukan [ID akun AWS Anda](https://docs.aws.amazon.com/IAM/latest/UserGuide/console-account-id.html), jalankan `aws sts get-caller-identity --query Account --output text`.

    Dalam kebijakan, ganti `<AWS_ACCOUNT_ID>` dengan ID akun AWS Anda dan `<ORGANIZATION_UUID>` dengan ID organisasi Anda. Kondisi `StringEquals` pada `kms:EncryptionContext:anthropic:org_uuid` mengikat kunci ke organisasi Anthropic Anda, dan validasi menolak kunci tanpanya. Untuk berbagi satu kunci di antara beberapa organisasi Anthropic, cantumkan setiap ID organisasi dalam nilai kondisi.

    <Note>
      **Menemukan ID organisasi Anda:** Salin bidang **Organization ID** di bawah **Settings > Organization** di Claude Console, atau di bawah **Organization settings > Organization** di claude.ai, atau baca bidang `id` dari endpoint [Organization Info](https://platform.claude.com/docs/id/api/beta/organization/retrieve). Gunakan UUID polos, bukan ID berawalan `org_`.
    </Note>

    Simpan kebijakan sebagai `key-policy.json`. Untuk membuat kunci di AWS Console sebagai gantinya, tempel kebijakan di sana, seperti dijelaskan nanti dalam langkah ini.

    ```json key-policy.json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AccountRootAdmin",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:root"
          },
          "Action": "kms:*",
          "Resource": "*"
        },
        {
          "Sid": "AllowAnthropicCMEKCrypto",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
          },
          "Action": ["kms:Encrypt", "kms:Decrypt"],
          "Resource": "*",
          "Condition": {
            "StringEquals": {
              "kms:EncryptionContext:anthropic:org_uuid": ["<ORGANIZATION_UUID>"]
            }
          }
        },
        {
          "Sid": "AllowAnthropicCMEKDescribe",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
          },
          "Action": "kms:DescribeKey",
          "Resource": "*"
        }
      ]
    }
    ```

    <Note>
      **Opsional:** Untuk membatasi kunci ke beberapa workspace Anda, gunakan pernyataan `AllowAnthropicCMEKCrypto` ini alih-alih yang ada di JSON kebijakan sebelumnya, dengan satu ID compartment untuk setiap workspace. Tambahkan ID compartment workspace sebelum Anda melampirkan kunci ke sana. Untuk workspace baru, buat tanpa kunci, tambahkan ID compartment-nya, lalu lampirkan kunci.

      ```json
      {
        "Sid": "AllowAnthropicCMEKCrypto",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
        },
        "Action": ["kms:Encrypt", "kms:Decrypt"],
        "Resource": "*",
        "Condition": {
          "StringEquals": {
            "kms:EncryptionContext:anthropic:org_uuid": ["<ORGANIZATION_UUID>"]
          },
          "StringEqualsIfExists": {
            "kms:EncryptionContext:anthropic:compartment_uuid": ["<COMPARTMENT_UUID>"]
          }
        }
      }
      ```
    </Note>

    ```bash
    aws kms create-key \
      --region <REGION> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy file://key-policy.json
    ```

    Tangkap `KeyMetadata.Arn` dari output. Anda membutuhkannya saat mendaftarkan kunci di langkah berikutnya.

    <Warning>
      Jika kunci sudah dikonfigurasi untuk CMEK dan melindungi data yang ada, Anda harus menambahkan pernyataan yang memungkinkan Anthropic mendekripsi data tersebut, selain tiga pernyataan dalam kebijakan sebelumnya. Dalam kondisinya, cantumkan ID compartment dari setiap workspace tempat kunci dilampirkan atau pernah dilampirkan.

      ```json
      {
        "Sid": "AllowAnthropicCMEKDecryptExistingData",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::915198916910:role/anthropic-cmek-client-us"
        },
        "Action": "kms:Decrypt",
        "Resource": "*",
        "Condition": {
          "StringEquals": {
            "kms:EncryptionContext:anthropic:compartment_uuid": ["<COMPARTMENT_UUID>"]
          }
        }
      }
      ```
    </Warning>

    Anthropic memvalidasi kunci saat Anda memverifikasinya atau melampirkannya ke workspace. Setiap validasi menambahkan empat kesalahan access-denied ke CloudTrail. Ini diharapkan. Jika Anda perlu memfilternya, filter pada ketiga nilai berikut. Yang pertama saja tidak cukup, karena pemanggil mana pun dapat menetapkannya:

    * `requestParameters.encryptionContext.associatedData`: `Y21lay12YWxpZGF0aW9u`
    * `userIdentity.accountId`: `915198916910`
    * `resources.ARN`: `arn:aws:kms:<REGION>:<AWS_ACCOUNT_ID>:key/<KEY_ID>`

    <Note>
      **Menemukan ID compartment Anda:** Lihat tab **Claude Platform** di bawah **Daftarkan kunci dengan Anthropic**.
    </Note>

    Anda juga dapat membuat kunci dari AWS Console. Pilih kunci simetris dengan penggunaan kunci encrypt dan decrypt, kunci single-region, dan asal material kunci KMS. Wizard Create-key menetapkan kebijakan kunci pada langkah **Review**-nya: Jika Anda menambahkan ID akun Anthropic `915198916910` di bawah izin penggunaan kunci di sana, kebijakan yang dihasilkan memberikan seluruh akun Anthropic aksi yang lebih luas (seperti `kms:ReEncrypt*` dan `kms:GenerateDataKey*`) tanpa kondisi `EncryptionContext`, dan validasi menolaknya. Untuk menghindari meninggalkan kunci yang terlalu permisif, selesaikan wizard dengan izin administratif saja, lalu buka tab **Key policy** kunci dan ganti JSON dengan kebijakan `key-policy.json` yang ditunjukkan sebelumnya dalam langkah ini.

    <Frame caption="Configure key: symmetric, encrypt and decrypt, single-region key.">
      ![Wizard Create-key di AWS KMS pada langkah Configure key, dengan tipe kunci simetris, penggunaan kunci encrypt dan decrypt, dan kunci single-region dipilih.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
    </Frame>

    <Frame caption="Tambahkan alias dan deskripsi untuk kunci.">
      ![Langkah Add labels di AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
    </Frame>

    <Frame caption="Tentukan izin administratif kunci (opsional). Akun Anda mempertahankan kontrol admin penuh.">
      ![Langkah Define key administrative permissions di AWS KMS yang mencantumkan peran IAM yang dapat mengelola kunci.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
    </Frame>

    <Frame caption="Jangan tambahkan ID akun Anthropic di sini. Langkah wizard ini menghasilkan kebijakan yang terlalu permisif. Biarkan izin penggunaan kosong dan edit JSON Key policy setelah pembuatan (lihat kebijakan kunci sebelumnya).">
      ![Langkah Define key usage permissions di AWS KMS dengan ID akun Anthropic yang dimasukkan di bawah Other AWS accounts.](https://platform.claude.com/docs/images/cmek/aws-usage-permissions.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci dengan Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk mana yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Note>
      **Claude Platform on AWS:** Principal, kebijakan kunci, dan alur pendaftaran berbeda, dan tidak ada langkah validasi terpisah. Ikuti [Siapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws) alih-alih tab ini.
    </Note>

    <Note>
      **Menemukan ID compartment Anda:** Setiap workspace memiliki ID compartment yang membatasi data CMEK-nya. Untuk menemukannya di Claude Console, buka [Manage > Security](https://platform.claude.com/settings/workspaces/default/security-compliance) dan pilih workspace di pemilih workspace di bagian atas sidebar. ID berada di bawah **Encryption key**, di bidang **Compartment ID**. Anda juga dapat membaca bidang `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/beta/organization/workspaces/retrieve).
    </Note>

    Anda dapat menyiapkan kunci di Claude Console atau melalui Admin API, dengan hasil yang sama.

    <Tabs>
      <Tab title="Claude Console">
        <Steps>
          <Step title="Daftarkan kunci dengan Anthropic">
            Di Claude Console, buka **Settings > Encryption keys** dan klik **Add key**. Masukkan nama tampilan, pilih **AWS KMS**, dan klik **Continue**. Tempel ARN kunci ke **KMS key ARN**, dan klik **Add**.

            Langkah detail kunci menampilkan ID organisasi Anda. Tambahkan ke [kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) sebelum Anda mengklik **Add**.
          </Step>

          <Step title="Validasi kunci">
            Pada halaman **Encryption keys**, klik **Verify** di samping kunci. **Connected** muncul ketika pemeriksaan lolos. Jika gagal, pesan memberikan alasannya.
          </Step>

          <Step title="Lampirkan kunci ke workspace">
            Di Claude Console, buka [Manage > Security](https://platform.claude.com/settings/workspaces/default/security-compliance) dan pilih workspace di pemilih workspace di bagian atas sidebar. Di bawah **Encryption key**, pilih kunci, klik **Save**, dan konfirmasi. Melampirkan kunci tidak dapat dibatalkan. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works).
          </Step>
        </Steps>
      </Tab>

      <Tab title="API">
        <Steps>
          <Step title="Daftarkan kunci dengan Anthropic">
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

          <Step title="Validasi kunci">
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

            Jika validasi gagal, penyebab umum adalah:

            * **Ketidakcocokan konteks enkripsi:** Jika kebijakan memiliki kondisi `kms:EncryptionContext:anthropic:compartment_uuid`, pastikan kondisi tersebut mencantumkan ID compartment dari setiap workspace tempat kunci dilampirkan. Validasi mengirimkan ID compartment dari workspace yang diperiksanya. Kunci lama yang pernyataan compartment-nya masih mengizinkan `kms:Encrypt` divalidasi dengan nilai semua-nol (`00000000-0000-0000-0000-000000000000`) saat tidak dilampirkan, jadi pertahankan nilai tersebut dalam daftarnya.
            * **Resource control policies (RCP):** Jika organisasi AWS Anda memiliki RCP yang menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan org Anda, itu memblokir peran lintas akun Anthropic. RCP memerlukan pengecualian untuk kunci ini atau untuk ARN peran Anthropic. Service control policies tidak berlaku di sini, karena tidak dievaluasi untuk principal eksternal yang memanggil melalui kebijakan berbasis sumber daya.
            * **Akses diberikan melalui IAM alih-alih kebijakan kunci:** Akses KMS lintas akun harus diberikan dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Periksa dengan `aws kms get-key-policy --key-id <id> --policy-name default`.
            * **Ketidakcocokan region:** Konfirmasikan region kunci adalah salah satu yang dioperasikan Anthropic untuk tier geo yang Anda konfigurasikan.
          </Step>

          <Step title="Lampirkan kunci ke workspace">
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
    </Tabs>
  </Tab>

  <Tab title="Claude Enterprise">
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **AWS** dan klik **Continue**, lalu tempel Key ARN dari langkah sebelumnya dan klik **Add**. Anthropic memvalidasi kunci dengan round-trip enkripsi dan dekripsi. Setelah ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK sejak saat itu.

    Langkah detail kunci dari alur ini menampilkan **Organization ID for the key policy** Anda dengan tombol salin. Gantikan nilai tersebut untuk `<ORGANIZATION_UUID>` dalam kebijakan kunci. Anda dapat membuka alur untuk menyalin ID sebelum Anda membuat kunci.

    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah lampiran workspace terpisah, dan organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Siapkan CMEK di Claude Platform on AWS

Pada [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), CMEK hanya menggunakan kunci AWS KMS, dan penyiapan berbeda dari bagian sebelumnya dalam hal berikut:

* **Principal:** Kebijakan kunci Anda memberikan akses ke principal layanan AWS `aws-external-anthropic.amazonaws.com`. Peran IAM dan ID akun Anthropic tidak digunakan, sehingga [ARN untuk Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#amazon-resource-name-arn-for-anthropic) tidak berlaku.
* **Persyaratan kunci:** Kunci harus berupa kunci KMS simetris dengan penggunaan encrypt dan decrypt, single-region, dan berada di akun serta region AWS yang sama dengan workspace tempat Anda melampirkannya. Kunci lintas akun tidak didukung: kunci harus berada di akun AWS yang menghosting organisasi Anda. Kunci multi-region (ID kunci yang dimulai dengan `mrk-`) dan ARN alias ditolak saat Anda mendaftarkan kunci; gunakan ARN kunci.
* **Tidak ada langkah validasi terpisah:** Selain pemeriksaan pada ARN kunci saat pendaftaran, kunci divalidasi saat Anda melampirkannya ke workspace. Panggilan lampiran melakukan round enkripsi/dekripsi terhadap kunci dengan ID compartment workspace tersebut sebagai konteks enkripsi, sehingga masalah kebijakan kunci muncul pada waktu lampiran alih-alih pada pendaftaran. Oleh karena itu, kondisi `EncryptionContext` tidak memerlukan entri semua-nol.
* **Di mana Anda mengelola kunci:** Daftarkan dan lampirkan kunci di Claude Console, masuk melalui AWS dengan peran Admin. Endpoint kunci eksternal juga tersedia di Claude Platform on AWS, diotorisasi melalui [aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys); di sana, kunci diidentifikasi oleh ARN kunci KMS-nya alih-alih ID `ekey_`.

<Warning>
  Gunakan hanya nama principal layanan yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

### Prasyarat

* Akun AWS yang menghosting organisasi Claude Platform on AWS Anda, dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Peran **Admin** di Claude Console untuk Claude Platform on AWS. Lihat [Menggunakan Claude Console](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#using-the-claude-console).
* Untuk principal IAM yang Anda gunakan untuk masuk ke Claude Console: selain `aws-external-anthropic:AssumeConsole`, [aksi IAM](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#encryption-keys) untuk operasi yang Anda lakukan di sana, karena halaman Encryption keys dan lampiran kunci melewati gateway AWS. Mendaftarkan kunci adalah `RegisterKey` (dengan `ListKeys` dan `GetKey` untuk melihat pendaftaran), dan melampirkan satu adalah `UpdateWorkspace` atau `CreateWorkspace`. Aksi kunci eksternal (dan `CreateWorkspace`) bersifat account-scoped, jadi berikan pada `Resource: "*"`; kebijakan yang terbatas pada ARN workspace tidak menyertakannya.
* Untuk principal IAM yang melampirkan kunci ke workspace (identitas yang Anda gunakan untuk masuk ke Claude Console): `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci. Akses principal Anda ke kunci diperiksa saat Anda melampirkannya, selain principal layanan.
* Opsional, untuk pemilih kunci di Claude Console: `kms:ListKeys` dan `kms:DescribeKey` untuk principal yang Anda gunakan untuk masuk. Tanpanya, tempel ARN kunci sebagai gantinya.

### Buat kunci KMS

Kebijakan kunci memiliki tiga pernyataan: pernyataan admin root akun Anda; pernyataan yang memungkinkan principal layanan Claude Platform on AWS mengenkripsi, mendekripsi, dan menghasilkan kunci data; serta pernyataan terpisah untuk `kms:DescribeKey`. Pernyataan kripto membawa kondisi `EncryptionContext` opsional yang mengikat kunci ke workspace yang Anda cantumkan. `DescribeKey` diberikan secara terpisah karena tidak memiliki parameter `EncryptionContext`, sehingga kondisi `EncryptionContext` pada aksi tersebut akan selalu menolak.

Jika Anda berencana menggunakan kondisi `EncryptionContext` opsional yang ditunjukkan di sini, buat workspace terlebih dahulu (tanpa kunci), salin ID compartment-nya, dan gunakan sebagai pengganti `<compartment-uuid>`. Untuk menemukan ID tersebut di Claude Console, buka [Manage > Security](https://platform.claude.com/settings/workspaces/default/security-compliance) dan pilih workspace di pemilih workspace di bagian atas sidebar. ID tersebut berada di bawah **Encryption key**, di bidang **Compartment ID**. Anda juga dapat membacanya dari bidang `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/beta/organization/workspaces/retrieve). Jika Anda tidak berencana menggunakan kondisi tersebut, hapus blok `Condition` dari pernyataan itu.

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
        \"Resource\": \"*\"
      }
    ]
  }"
```

Tangkap `KeyMetadata.Arn` dari output. Anda membutuhkannya saat mendaftarkan kunci.

Kondisi `EncryptionContext` bersifat opsional. Setiap panggilan enkripsi, dekripsi, dan kunci data yang dilakukan untuk sebuah workspace, termasuk pemeriksaan pada waktu lampiran, membawa ID compartment workspace tersebut sebagai `anthropic:compartment_uuid`, sehingga kondisi tersebut mencantumkan ID compartment setiap workspace tempat Anda melampirkan kunci dan tidak memerlukan entri semua-nol. Menambahkannya juga mengikat kunci ke workspace yang Anda cantumkan di lapisan IAM. Karena ID compartment baru ada setelah workspace-nya ada, urutannya adalah: buat workspace, masukkan ID compartment-nya ke dalam kondisi (saat pembuatan kunci, atau nanti dengan `kms:PutKeyPolicy`), lalu lampirkan kunci. Sebelum melampirkan kunci ke setiap workspace tambahan, tambahkan ID compartment workspace tersebut dengan cara yang sama. Untuk memulai tanpa kondisi tersebut, hapus blok `Condition` dari pernyataan `AllowClaudePlatformOnAWSCrypto`; jika Anda menambahkannya nanti, sertakan ID compartment setiap workspace yang sudah dilampiri kunci.

Anda dapat membatasi lebih lanjut kedua pernyataan principal layanan dengan kondisi `aws:SourceArn`. Layanan meneruskan [ARN workspace](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#service-details) (`arn:aws:aws-external-anthropic:<region>:<account-id>:workspace/<workspace-id>`) sebagai ARN sumber pada setiap panggilan yang dilakukannya dengan kunci Anda, sehingga `"ArnLike": {"aws:SourceArn": "arn:aws:aws-external-anthropic:*:<account-id>:workspace/*"}` membatasi pemberian izin pada workspace di akun AWS Anda sendiri, dan daftar ARN workspace lengkap membatasinya pada workspace tersebut. Kondisi ini tidak wajib; kondisi `EncryptionContext` saja sudah mengikat kunci ke workspace yang Anda cantumkan.

Anda juga dapat membuat kunci dari AWS Console: pilih kunci simetris dengan penggunaan kunci encrypt dan decrypt, kunci single-region, dan asal material kunci KMS, di region workspace. Biarkan izin penggunaan kunci kosong di wizard Create-key, lalu buka tab **Key policy** kunci dan ganti JSON dengan kebijakan yang ditunjukkan di sini.

### Daftarkan dan lampirkan kunci

<Steps>
  <Step title="Daftarkan kunci">
    Di Claude Console, buka **Settings > Encryption keys** dan klik **Add key**. Masukkan nama tampilan, lalu pilih kunci dari pemilih kunci atau pilih **Enter ARN manually** dan tempel ARN kunci, dan klik **Add**. Kunci harus berada di akun AWS yang menghosting organisasi Anda; kunci lintas akun tidak didukung. Pemilih mencantumkan kunci yang diaktifkan, customer-managed, simetris, single-region di akun Anda di salah satu region organisasi Anda; untuk kunci yang tidak dicantumkan pemilih, masukkan ARN. Pemilih mencantumkan kunci hanya jika principal yang Anda gunakan untuk masuk dapat memanggil `kms:ListKeys` dan `kms:DescribeKey`.
  </Step>

  <Step title="Lampirkan kunci ke workspace">
    Lampirkan kunci ke workspace baru sebelum Anda mengirim permintaan apa pun ke workspace tersebut. Untuk workspace yang sudah menerima permintaan, kunci dapat memerlukan [hingga satu hari untuk berlaku](https://platform.claude.com/docs/id/manage-claude/cmek#how-it-works). Di Claude Console, buka [Manage > Security](https://platform.claude.com/settings/workspaces/default/security-compliance) dan pilih workspace di pemilih workspace di bagian atas sidebar. Di bawah **Encryption key**, pilih kunci, klik **Save**, lalu konfirmasi. Anda juga dapat memilih kunci saat membuat workspace di Claude Console, tetapi hanya jika kebijakan kunci Anda belum menyebutkan workspace tertentu (tanpa kondisi `EncryptionContext`), karena ID compartment workspace ditetapkan saat pembuatan. Setelah dilampirkan, kunci sebuah workspace tidak dapat diubah.

    Inilah saat kunci divalidasi: panggilan lampiran memeriksa akses principal Anda ke kunci dan melakukan round enkripsi/dekripsi terhadapnya dengan ID compartment workspace sebagai konteks enkripsi, sehingga masalah dengan kebijakan kunci atau izin principal Anda muncul sebagai kesalahan pada panggilan tersebut. Jika lampiran gagal dengan kesalahan akses KMS, periksa hal berikut:

    * Kebijakan kunci menyebutkan principal layanan `aws-external-anthropic.amazonaws.com` dan memberikan `kms:Encrypt`, `kms:Decrypt`, dan `kms:GenerateDataKey`, ditambah `kms:DescribeKey` dalam pernyataan terpisah yang tidak memiliki kondisi `EncryptionContext`.
    * Setiap kondisi `EncryptionContext` menyertakan ID compartment workspace ini, dan setiap kondisi `aws:SourceArn` yang Anda tambahkan cocok dengan ARN workspace ini.
    * Kunci diaktifkan, single-region, dan berada di akun serta region AWS yang sama dengan workspace.
    * Principal yang Anda gunakan untuk masuk memiliki `kms:DescribeKey`, `kms:Encrypt`, dan `kms:Decrypt` pada kunci.
    * Tidak ada service control policy atau resource control policy di organisasi AWS Anda yang mencegah principal layanan atau principal Anda menggunakan kunci.
    * Jika kebijakan terlihat benar dan lampiran masih gagal, temukan event `kms:` yang ditolak di CloudTrail pada akun kunci (event tersebut menampilkan principal pemanggil dan, untuk panggilan kriptografis, konteks enkripsi), lalu perbaiki kondisi dengan `kms:PutKeyPolicy` dan coba lagi.
  </Step>
</Steps>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `aws` dengan sumber daya `aws_kms_key` dan `aws_kms_alias`.
