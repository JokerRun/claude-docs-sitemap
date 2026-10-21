---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
fetched_at: 2026-10-21T02:21:05.363362Z
sha256: 435b2b3d8b68ccf06c2fe56fc2a73a658363f7ab2a0f5416bdd4f3dc7e036176
---

---
title: Konfigurasikan AWS KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms
description: Gunakan AWS KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan AWS KMS
```

Panduan ini menunjukkan cara menggunakan kunci [AWS KMS](https://aws.amazon.com/kms/) sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

<Note>
  **Claude Platform on AWS:** Jika sidebar Claude Console Anda menampilkan **Account managed by AWS**, organisasi Anda berada di Claude Platform on AWS. Sebagai gantinya, ikuti [Menyiapkan CMEK di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/cmek-claude-platform-on-aws).
</Note>

## Prasyarat

* Akun AWS dengan izin untuk membuat kunci KMS dan menetapkan kebijakan kunci (`kms:CreateKey` dan `kms:PutKeyPolicy`).
* Untuk membuat kunci dari baris perintah, [AWS CLI](https://aws.amazon.com/cli/) terpasang dan terautentikasi.
* Untuk mendaftarkan kunci melalui API, kunci Admin API Anthropic untuk organisasi Anda.

## Amazon Resource Name (ARN) untuk Anthropic

Kebijakan kunci dalam panduan ini memberikan akses ke kunci Anda kepada peran IAM Anthropic berikut:

```text wrap
arn:aws:iam::915198916910:role/anthropic-cmek-client-us
```

<Warning>
  Gunakan hanya ARN yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

## Penyiapan kunci enkripsi

### Menyiapkan kebijakan kunci

Salin kebijakan ini ke editor teks:

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

Ganti kedua placeholder:

* **`<AWS_ACCOUNT_ID>`:** [ID akun AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/console-account-id.html) Anda. Untuk menampilkannya dengan AWS CLI, jalankan `aws sts get-caller-identity --query Account --output text`.
* **`<ORGANIZATION_UUID>`:** ID organisasi Anthropic Anda

<Note>
  **Menemukan ID organisasi Anda:** Gunakan UUID polos, bukan ID yang berawalan `org_`. Salin dari salah satu tempat berikut:

  * **Claude Console:** kolom **Organization ID** di halaman [Organization](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`)
  * **claude.ai:** kolom **Organization ID** di bawah **Organization settings > Organization**
  * **Admin API:** field `id` dari endpoint [Organization Info](https://platform.claude.com/docs/id/api/organization/retrieve)
</Note>

Jangan hapus kondisi `kms:EncryptionContext:anthropic:org_uuid`, atau validasi akan gagal. Untuk berbagi satu kunci di antara beberapa organisasi Anthropic, cantumkan setiap ID organisasi di dalamnya. Untuk membatasi kunci ke workspace tertentu, lihat [kondisi workspace opsional](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#workspace-condition).

<Warning>
  **Kunci yang sudah melindungi data:** Jika kunci sudah dikonfigurasi untuk CMEK, tambahkan pernyataan keempat ini agar Anthropic tetap dapat mendekripsi data yang ada. Dalam kondisinya, cantumkan [ID compartment](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#compartment-id) dari setiap workspace tempat kunci dilampirkan atau pernah dilampirkan.

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

### Membuat kunci

Buat kunci di [region AS](https://platform.claude.com/docs/id/manage-claude/cmek#availability-and-regions). Untuk latensi terendah, gunakan `us-east-2`.

<Tabs>
  <Tab title="AWS Console">
    <Steps>
      <Step title="Buka wizard Create key">
        Buka [konsol AWS KMS](https://console.aws.amazon.com/kms) dan beralih ke region untuk kunci tersebut. Buka **Customer managed keys** dan klik **Create key**.
      </Step>

      <Step title="Konfigurasikan kunci">
        Pastikan opsi-opsi berikut dipilih:

        * **Key type:** Symmetric
        * **Key usage:** Encrypt and decrypt
        * **Advanced options > Key material origin:** KMS
        * **Advanced options > Regionality:** Single-Region key

        Klik **Next**.

        <Frame caption="Kunci simetris, encrypt dan decrypt, single-Region.">
          ![Wizard Create-key di AWS KMS pada langkah Configure key, dengan tipe kunci simetris, penggunaan kunci encrypt dan decrypt, dan kunci single-region dipilih.](https://platform.claude.com/docs/images/cmek/aws-configure-key.png)
        </Frame>
      </Step>

      <Step title="Tambahkan label">
        Masukkan **Alias** untuk kunci tersebut, seperti `anthropic-cmek`. Klik **Next**.

        <Frame caption="Alias untuk kunci.">
          ![Langkah Add labels di AWS KMS dengan alias anthropic-cmek dan deskripsi Anthropic CMEK.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
        </Frame>
      </Step>

      <Step title="Tentukan izin administratif kunci">
        Jangan pilih administrator kunci apa pun. Kebijakan kunci Anda sudah memberikan kontrol admin penuh kepada akun AWS Anda. Klik **Next**.

        <Frame caption="Biarkan administrator kunci kosong.">
          ![Langkah Define key administrative permissions di AWS KMS yang mencantumkan peran IAM yang dapat mengelola kunci.](https://platform.claude.com/docs/images/cmek/aws-admin-permissions.png)
        </Frame>
      </Step>

      <Step title="Tentukan izin penggunaan kunci">
        Jangan pilih pengguna kunci apa pun, dan jangan tambahkan apa pun di bawah **Other AWS accounts**. Kebijakan kunci Anda sudah memberikan akses yang diperlukan. Klik **Next**.
      </Step>

      <Step title="Edit kebijakan kunci">
        Klik **Edit**. Ganti seluruh kebijakan dengan kebijakan kunci Anda, lalu klik **Next**.
      </Step>

      <Step title="Tinjau">
        Klik **Finish**.
      </Step>

      <Step title="Salin ARN kunci">
        Di **Customer managed keys**, buka kunci baru tersebut dan salin ARN-nya. Anda memerlukan ARN tersebut untuk mendaftarkan kunci.
      </Step>
    </Steps>

    Untuk mengganti kebijakan kunci pada kunci yang sudah ada:

    1. Buka kunci tersebut dan klik tab **Key policy**.
    2. Jika Anda melihat **Switch to policy view**, klik opsi tersebut.
    3. Klik **Edit**.
    4. Ganti JSON dengan kebijakan kunci Anda.
    5. Klik **Save changes**.
  </Tab>

  <Tab title="AWS CLI">
    Simpan kebijakan kunci Anda sebagai `key-policy.json`, lalu buat kunci. Ganti `<REGION>` dengan region kunci tersebut.

    ```bash
    aws kms create-key \
      --region <REGION> \
      --description "Anthropic CMEK" \
      --key-usage ENCRYPT_DECRYPT \
      --policy file://key-policy.json
    ```

    Salin `KeyMetadata.Arn` dari output. Anda memerlukannya untuk mendaftarkan kunci.
  </Tab>
</Tabs>

<Note>
  **Opsional:** Untuk membatasi kunci ke workspace tertentu, ganti pernyataan `AllowAnthropicCMEKCrypto` dalam kebijakan kunci dengan pernyataan ini. Cantumkan satu ID compartment untuk setiap workspace.

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

  Tambahkan ID compartment setiap workspace sebelum Anda melampirkan kunci ke workspace tersebut. Untuk workspace baru:

  1. Buat workspace tanpa kunci.
  2. Tambahkan ID compartment-nya ke kebijakan.
  3. Lampirkan kunci.

  **Menemukan ID compartment Anda:** Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy) (`platform.claude.com/settings/privacy`). Pilih workspace dari menu dropdown di bagian atas halaman. ID tersebut berada di bawah **Encryption key**, di kolom **Compartment ID**. Anda juga dapat membaca kolom `compartment_id` yang dikembalikan oleh endpoint [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve).
</Note>

## Daftarkan kunci dengan Anthropic

Memvalidasi kunci akan menambahkan kesalahan access-denied yang memang diharapkan ke CloudTrail. Jika Anda memasang peringatan untuk kesalahan ini, lihat [Kesalahan yang diharapkan di CloudTrail](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#expected-errors-in-cloud-trail) terlebih dahulu.

<Tabs>
  <Tab title="Claude Platform">
    <Tabs>
      <Tab title="Claude Console">
        <Steps>
          <Step title="Buka pengaturan kunci enkripsi">
            Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy#encryption-keys) (`platform.claude.com/settings/privacy`). Jika Anda tidak melihat **Encryption keys**, pilih **Organization** dari menu dropdown di bagian atas halaman.
          </Step>

          <Step title="Tambahkan kunci">
            Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name** dan pilih **AWS KMS**. Klik **Continue**.
          </Step>

          <Step title="Masukkan ARN kunci">
            Kotak dialog menampilkan **Organization ID for the key policy**. Periksa bahwa [kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) Anda berisi ID ini. Tempelkan ARN kunci ke **KMS key ARN**, lalu klik **Add**.
          </Step>

          <Step title="Validasi kunci">
            Di daftar **Encryption keys**, klik **Verify** di samping kunci. **Connected** muncul saat pemeriksaan berhasil. Jika gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#troubleshoot-validation) untuk penyebab umum.
          </Step>

          <Step title="Lampirkan kunci ke workspace">
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

            Field `id` pada respons berisi ID kunci eksternal. Salin untuk dua langkah berikutnya:

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

            Jika validasi gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#troubleshoot-validation).
          </Step>

          <Step title="Lampirkan kunci ke workspace">
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

              workspace_id = "<workspace-id>"
              workspace = client.organization.workspaces.update(
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
    Pada Claude Enterprise, CMEK berlaku untuk seluruh organisasi, dan sebuah organisasi hanya dapat memiliki satu kunci.

    <Steps>
      <Step title="Buka pengaturan kunci enkripsi">
        Buka [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) dan temukan **Encryption keys**.
      </Step>

      <Step title="Tambahkan kunci">
        Klik **Add key**. Masukkan **Display name** dan pilih **AWS KMS**. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Continue**.
      </Step>

      <Step title="Masukkan ARN kunci">
        Kotak dialog menampilkan **Organization ID for the key policy**. Periksa bahwa [kebijakan kunci](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#key-policy) Anda berisi ID ini. Tempelkan ARN kunci ke **KMS key ARN**, lalu klik **Add**.
      </Step>

      <Step title="Konfirmasi bahwa validasi berhasil">
        Ketika pemeriksaan berhasil, **Encryption key configured** muncul, dan organisasi Anda dilindungi CMEK sejak saat itu. Jika pemeriksaan gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#troubleshoot-validation).
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Memecahkan masalah validasi

Jika validasi gagal, penyebab umum adalah:

* **ID organisasi salah:** Pastikan kondisi `org_uuid` mencantumkan ID organisasi polos Anda, bukan ID yang berawalan `org_`.
* **Ketidakcocokan konteks enkripsi:** Jika kebijakan memiliki kondisi `kms:EncryptionContext:anthropic:compartment_uuid`, pastikan kondisi tersebut mencantumkan [ID compartment](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#compartment-id) dari setiap workspace tempat kunci dilampirkan. Pada kunci lama, pernyataan compartment mungkin masih mengizinkan `kms:Encrypt`. Dalam hal ini, pertahankan juga nilai semua-nol (`00000000-0000-0000-0000-000000000000`) dalam daftar.
* **Resource control policies (RCP):** Beberapa RCP menolak operasi KMS ketika `aws:PrincipalOrgID` tidak cocok dengan organisasi AWS Anda. RCP seperti ini memblokir peran Anthropic. Tambahkan pengecualian di dalamnya untuk kunci ini atau untuk ARN peran Anthropic. Service control policies tidak berlaku di sini.
* **Akses diberikan melalui IAM alih-alih kebijakan kunci:** Berikan akses kepada peran Anthropic di dalam kebijakan kunci itu sendiri, bukan melalui kebijakan IAM di akun Anda. Untuk memeriksa kebijakan kunci, jalankan `aws kms get-key-policy --region <REGION> --key-id <KEY_ARN> --policy-name default`.
* **Ketidakcocokan region:** Konfirmasikan bahwa kunci berada di region AS.

### Kesalahan yang diharapkan di CloudTrail

Anthropic memvalidasi kunci setiap kali Anda memverifikasinya, melampirkannya ke workspace, atau melihatnya di pengaturan Claude Enterprise. Setiap validasi menambahkan empat kesalahan access-denied ke CloudTrail. Kesalahan ini memang diharapkan.

Untuk memfilternya, cocokkan ketiga nilai berikut:

* `requestParameters.encryptionContext.associatedData`: `Y21lay12YWxpZGF0aW9u`
* `userIdentity.accountId`: `915198916910`
* `resources.ARN`: `arn:aws:kms:<REGION>:<AWS_ACCOUNT_ID>:key/<KEY_ID>`

Nilai pertama saja tidak cukup, karena pemanggil mana pun dapat menetapkannya.

## Terraform

Untuk membuat kunci dengan Terraform, gunakan resource `aws_kms_key` dan `aws_kms_alias` dari provider `aws`.
