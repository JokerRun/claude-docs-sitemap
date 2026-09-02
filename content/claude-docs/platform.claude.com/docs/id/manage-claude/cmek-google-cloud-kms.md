---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: b68840ba1d619af46944af9c533cb9a9eeab2a733a190278b7d62b34f59a4c60
---

---
title: Mengonfigurasi Google Cloud KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
description: Gunakan Google Cloud KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

```bash Configure with the /claude-api skill in Claude Code
claude "/claude-api help me configure a customer-managed encryption key with Google Cloud KMS"
```

Panduan ini menjelaskan langkah-langkah mengonfigurasi kunci Google Cloud KMS sebagai ["customer-managed encryption key" (kunci enkripsi yang dikelola pelanggan), atau CMEK](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci KMS Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengan kunci tersebut. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Proyek Google Cloud dengan penagihan yang diaktifkan.
* Cloud KMS API diaktifkan (`cloudkms.googleapis.com`).
* Izin untuk membuat key ring dan kunci KMS, serta untuk menetapkan kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau yang setara).
* Kunci API Admin Anthropic untuk organisasi Anda.
* [CLI `gcloud`](https://cloud.google.com/cli) terinstal dan terautentikasi.
* **Data Access audit logs** Cloud KMS diaktifkan untuk proyek (IAM & Admin > Audit Logs > Cloud Key Management Service, dengan `DATA_READ` dan `DATA_WRITE`). Log ini nonaktif secara default; tanpanya, operasi enkripsi dan dekripsi Anthropic tidak menghasilkan entri apa pun di Cloud Logging.

## Email service account Anthropic

Agar Anthropic dapat menggunakan kunci enkripsi Anda, Anda harus memberikan service account Anthropic sebuah kunci yang dapat digunakannya untuk mengenkripsi data. Email service account untuk CMEK Anthropic adalah:

```text wrap
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

<Warning>
  Gunakan hanya email service account yang dipublikasikan ini. Jangan pernah mempercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

<Note>
  **Domain restricted sharing:** Jika proyek Anda berada di bawah organisasi Google Cloud yang menerapkan `constraints/iam.allowedPolicyMemberDomains`, binding IAM berikut akan ditolak karena service account Anthropic berada di luar organisasi Anda. Anda memerlukan pengecualian tingkat proyek pada constraint tersebut, atau menambahkan customer ID Cloud Identity Anthropic (format `C0xxxxxxxx`) ke daftar yang diizinkan. Hubungi Anthropic untuk mendapatkan customer ID jika diperlukan.
</Note>

## Penyiapan kunci enkripsi

<Steps>
  <Step title="Buat atau pilih key ring">
    Lewati langkah ini jika Anda sudah memiliki key ring untuk digunakan kembali. Key ring bersifat regional. Pilih lokasi US region tunggal seperti `us-east5` yang sesuai dengan geografi Anthropic yang Anda konfigurasikan. Lokasi multi-region seperti `us` dan `global` tidak didukung.

    ```bash
    gcloud kms keyrings create <your-keyring-name> \
      --project=<your-project-id> \
      --location=<region>
    ```
  </Step>

  <Step title="Buat crypto key">
    Buat kunci simetris dengan tujuan `ENCRYPT_DECRYPT`. Anthropic sangat merekomendasikan perlindungan HSM: kunci HSM Cloud KMS tervalidasi FIPS 140-2 Level 3, dan selisih biayanya dibandingkan kunci perangkat lunak kecil.

    ```bash
    gcloud kms keys create <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --purpose=encryption \
      --protection-level=hsm
    ```

    Untuk perlindungan perangkat lunak sebagai gantinya, hilangkan `--protection-level=hsm`. Tidak ada hal lain dalam panduan ini yang berubah.

    Anda juga dapat membuat kunci dari Google Cloud Console. Buka key ring, klik **Create key**, pilih **Generated key**, atur tujuan dan algoritma ke symmetric encrypt and decrypt, lalu pilih **HSM** di bawah protection level.

    <Frame caption="Buat kunci symmetric encrypt/decrypt (enkripsi/dekripsi simetris) yang dilindungi HSM.">
      ![Halaman Create key Google Cloud KMS dengan protection level HSM dan tujuan Symmetric encrypt/decrypt.](https://platform.claude.com/docs/images/cmek/gcp-create-key.png)
    </Frame>
  </Step>

  <Step title="Berikan akses ke kunci untuk service account Anthropic">
    Diperlukan dua binding IAM tingkat kunci. Keduanya dicakup pada satu crypto key saja, bukan seluruh proyek atau seluruh key ring.

    Encrypt dan decrypt, yang digunakan Anthropic untuk mengenkripsi dan mendekripsi data key yang melindungi data workspace Anda ("envelope encryption" (enkripsi amplop)):

    ```bash
    gcloud kms keys add-iam-policy-binding <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
      --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
    ```

    Viewer, untuk pembacaan metadata (`cryptoKeys.get`) yang dilakukan Anthropic saat startup untuk memvalidasi tujuan dan algoritma kunci:

    ```bash
    gcloud kms keys add-iam-policy-binding <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
      --role=roles/cloudkms.viewer
    ```

    Dari Console, pilih kunci, buka panel **Permissions**, klik **Grant access**, dan tambahkan service account dengan kedua peran Cloud KMS CryptoKey Encrypter/Decrypter dan Cloud KMS Viewer. Pastikan Anda berada di halaman permissions milik kunci, bukan key ring atau proyek, sehingga pemberian akses hanya dicakup pada kunci ini.

    <Frame caption="Berikan kedua peran kepada service account Anthropic melalui Grant access (berikan akses), dicakup pada kunci.">
      ![Dialog Grant access dengan service account Anthropic yang diberi peran Cloud KMS CryptoKey Encrypter/Decrypter dan Viewer.](https://platform.claude.com/docs/images/cmek/gcp-grant-access.png)
    </Frame>
  </Step>

  <Step title="Catat nama resource lengkap kunci">
    Anda memberikan ini kepada Anthropic saat mendaftarkan kunci. Formatnya adalah:

    ```text wrap
    projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>
    ```

    Ambil dengan:

    ```bash
    gcloud kms keys describe <your-key-name> \
      --project=<your-project-id> \
      --location=<region> \
      --keyring=<your-keyring-name> \
      --format="value(name)"
    ```

    Dari Console, buka halaman detail kunci dan klik **Copy resource name**.

    <Frame caption="Salin nama resource lengkap kunci melalui Copy resource name (salin nama resource) dari menu tindakan.">
      ![Detail key ring Google Cloud dengan tindakan Copy resource name disorot di menu tindakan kunci.](https://platform.claude.com/docs/images/cmek/gcp-copy-resource-name.png)
    </Frame>
  </Step>
</Steps>

## Daftarkan kunci ke Anthropic

Cara Anda mendaftarkan kunci bergantung pada produk yang Anda gunakan.

<Tabs>
  <Tab title="Claude Platform">
    <Steps>
      <Step title="Daftarkan kunci ke Anthropic">
        Buat konfigurasi kunci eksternal melalui Admin API, menggunakan nama resource dari langkah Catat nama resource lengkap kunci di bagian Penyiapan kunci enkripsi.

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
          ant beta:organization:external-keys create <<'YAML'
          display_name: "<friendly-name>"
          geo: us
          provider_config:
            type: gcp
            key_name: "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
          YAML
          ```

          ```python Python
          client = anthropic.Anthropic()

          external_key = client.beta.organization.external_keys.create(
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

          const externalKey = await client.beta.organization.externalKeys.create({
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
          using Anthropic.Models.Beta.Organization.ExternalKeys;

          AnthropicClient client = new();

          var externalKey = await client.Beta.Organization.ExternalKeys.Create(new()
          {
              DisplayName = "<friendly-name>",
              Geo = Geo.Us,
              ProviderConfig = new BetaGcpExternalKeyConfig
              {
                  KeyName = "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
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
          		OfGCP: &anthropic.BetaGCPExternalKeyConfigParam{
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
          import com.anthropic.models.beta.organization.externalkeys.ExternalKeyCreateParams;

          void main() {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              var params = ExternalKeyCreateParams.builder()
                  .displayName("<friendly-name>")
                  .geo(ExternalKeyCreateParams.Geo.US)
                  .gcpProviderConfig("projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>")
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
                  'type' => 'gcp',
                  'keyName' => 'projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>',
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
              type: :gcp,
              key_name: "projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>"
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
        Picu proses bolak-balik enkripsi dan dekripsi terhadap kunci Anda.

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

        * **VPC Service Controls:** jika service perimeter melindungi Cloud KMS di proyek Anda, tambahkan Anthropic ke access level pada perimeter tersebut (atau kecualikan proyek kunci) agar Anthropic dapat menjangkau kunci.
        * **Domain restricted sharing:** kebijakan organisasi `constraints/iam.allowedPolicyMemberDomains` dapat menghapus binding service account Anthropic (lihat catatan sebelumnya). Pastikan binding tersebut ada dengan `gcloud kms keys get-iam-policy <your-key-name> --project=<your-project-id> --location=<region> --keyring=<your-keyring-name>`.
        * **Versi kunci dinonaktifkan atau dihancurkan:** pastikan versi utama kunci diaktifkan, dan tidak dinonaktifkan, dijadwalkan untuk dihancurkan, atau sudah dihancurkan.
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
    Di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), buka **Encryption keys**, lalu klik **Add key**. Pilih **Google Cloud**, tempelkan nama resource lengkap kunci dari langkah sebelumnya, dan klik **Continue**. Anthropic memvalidasi kunci dengan proses bolak-balik enkripsi dan dekripsi. Setelah kunci ditampilkan sebagai terverifikasi, organisasi Anda dilindungi CMEK sejak saat itu.

    Di Claude Enterprise, CMEK berlaku untuk seluruh organisasi, sehingga tidak ada langkah pelampiran workspace terpisah, dan sebuah organisasi hanya dapat memiliki satu kunci.
  </Tab>
</Tabs>

## Terraform

Untuk deployment infrastructure-as-code, langkah-langkah yang sama dipetakan ke provider `google` dengan resource `google_kms_key_ring`, `google_kms_crypto_key`, dan `google_kms_crypto_key_iam_member`.
