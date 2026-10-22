---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
fetched_at: 2026-10-22T02:21:21.745661Z
sha256: fd4af02b4e756d61323ddb54a8e1f93f8a0a8979d125a220773224412b3f192b
---

---
title: Mengonfigurasi Google Cloud KMS untuk CMEK
url: https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms
description: Gunakan Google Cloud KMS untuk menyediakan kunci enkripsi bagi organisasi Anda.
---

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
/claude-api bantu saya mengonfigurasi kunci enkripsi yang dikelola pelanggan dengan Google Cloud KMS
```

Panduan ini menunjukkan cara menggunakan kunci Google Cloud KMS sebagai [customer-managed encryption key (CMEK)](https://platform.claude.com/docs/id/manage-claude/cmek) untuk organisasi Anthropic Anda.

<Warning>
  Mengaktifkan CMEK bersifat permanen. Jika kunci Anda dihapus atau dinonaktifkan, Anthropic tidak dapat memulihkan data yang dienkripsi dengannya. Tinjau [peringatan dan batasan](https://platform.claude.com/docs/id/manage-claude/cmek) sebelum Anda memulai.
</Warning>

## Prasyarat

* Proyek Google Cloud dengan penagihan diaktifkan.
* Cloud KMS API diaktifkan (`cloudkms.googleapis.com`).
* Izin untuk membuat key ring dan kunci KMS, serta untuk menetapkan kebijakan IAM pada keduanya (`roles/cloudkms.admin` atau setara).
* Cloud KMS Data Access audit logs (Data Read dan Data Write) diaktifkan untuk proyek, sehingga Cloud Logging mencatat penggunaan kunci Anda oleh Anthropic. Log ini nonaktif secara default. Untuk mengaktifkannya, lihat [Enable Data Access audit logs](https://docs.cloud.google.com/logging/docs/audit/configure-data-access) dari Google.
* Untuk membuat kunci dari baris perintah, [`gcloud` CLI](https://cloud.google.com/cli) terinstal dan terautentikasi.
* Untuk mendaftarkan kunci melalui API, kunci Admin API Anthropic untuk organisasi Anda.

## Email akun layanan Anthropic

Dalam panduan ini, Anda memberikan akses ke kunci Anda kepada akun layanan Anthropic berikut:

```text wrap
anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com
```

<Warning>
  Gunakan hanya email akun layanan yang dipublikasikan ini. Jangan pernah memercayai pengenal yang diberikan melalui email, chat, atau saluran onboarding apa pun.
</Warning>

<Note>
  **Berbagi terbatas domain:** Jika organisasi Google Cloud Anda menerapkan `constraints/iam.allowedPolicyMemberDomains`, organisasi tersebut akan menolak binding IAM untuk akun layanan ini. Tambahkan pengecualian tingkat proyek pada constraint tersebut, atau tambahkan ID pelanggan Cloud Identity Anthropic (format `C0xxxxxxxx`) ke daftar yang diizinkan. Hubungi Anthropic untuk mendapatkan ID pelanggan tersebut.
</Note>

## Penyiapan kunci enkripsi

Kunci harus memenuhi persyaratan berikut:

* **Lokasi:** Gunakan lokasi AS single-region, seperti `us-east5`. Lokasi multi-region seperti `us` dan `global` tidak didukung. Lihat [Ketersediaan dan wilayah](https://platform.claude.com/docs/id/manage-claude/cmek#availability-and-regions).
* **Tipe:** Gunakan kunci simetris dengan tujuan `ENCRYPT_DECRYPT`. Anthropic sangat merekomendasikan perlindungan HSM.
* **Label organisasi:** Tambahkan label `anthropic-org-<ORGANIZATION_UUID>` dengan nilai `true`. Ganti `<ORGANIZATION_UUID>` dengan ID organisasi Anthropic Anda dalam huruf kecil. Validasi akan gagal tanpa label ini. Untuk memberi label pada kunci yang sudah ada, lihat [Kunci yang sudah Anda miliki](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#existing-key-label).
* **Akses:** Berikan peran `roles/cloudkms.cryptoKeyEncrypterDecrypter` dan `roles/cloudkms.viewer` kepada akun layanan Anthropic pada kunci itu sendiri.

<Note>
  **Menemukan ID organisasi Anda:** Gunakan UUID polos, bukan ID yang berawalan `org_`. Salin dari salah satu tempat berikut:

  * **Claude Console:** kolom **Organization ID** di halaman [Organization](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`)
  * **claude.ai:** kolom **Organization ID** di bawah **Organization settings > Organization**
  * **Admin API:** field `id` dari endpoint [Organization Info](https://platform.claude.com/docs/id/api/organization/retrieve)
</Note>

<Tabs>
  <Tab title="Google Cloud Console">
    <Steps>
      <Step title="Buat atau pilih key ring">
        Di Google Cloud console, buka halaman [Key management](https://console.cloud.google.com/security/kms). Buka key ring di lokasi AS single-region, seperti `us-east5`, atau buat yang baru.
      </Step>

      <Step title="Konfigurasikan kunci">
        Klik **Create key** dan masukkan nama. Pilih opsi berikut:

        * **Protection level:** HSM
        * **Key material:** Generated key
        * **Purpose:** Symmetric encrypt/decrypt
        * **Algorithm:** Google symmetric key
      </Step>

      <Step title="Tambahkan label organisasi">
        Klik **Additional settings**, lalu **Add label**. Masukkan label organisasi:

        * **Key 1:** `anthropic-org-<ORGANIZATION_UUID>`
        * **Value 1:** `true`

        Klik **Create**.

        <Frame caption="Kunci symmetric encrypt/decrypt yang dilindungi HSM dengan label organisasi.">
          ![Halaman Create key di Google Cloud KMS dengan perlindungan HSM, symmetric encrypt/decrypt, dan label anthropic-org diatur ke true.](https://platform.claude.com/docs/images/cmek/gcp-create-key-label.png)
        </Frame>
      </Step>

      <Step title="Buka izin kunci">
        Di halaman detail key ring, centang kotak di samping kunci. Buka panel **Permissions** dan klik **Grant access**.
      </Step>

      <Step title="Berikan akun layanan Anthropic akses ke kunci">
        Pastikan **Resource** menampilkan kunci, bukan key ring atau proyek. Masukkan nilai berikut:

        * **New principals:** `anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com`
        * **Role:** Cloud KMS CryptoKey Encrypter/Decrypter

        Klik **Add another role** dan pilih **Cloud KMS Viewer**. Klik **Save**.

        <Frame caption="Berikan akun layanan Anthropic kedua peran, dicakup ke kunci.">
          ![Dialog Grant access dengan akun layanan Anthropic yang diberi peran Cloud KMS CryptoKey Encrypter/Decrypter dan Viewer.](https://platform.claude.com/docs/images/cmek/gcp-grant-access.png)
        </Frame>
      </Step>

      <Step title="Salin nama resource kunci lengkap">
        Di halaman detail key ring, buka menu **Actions** kunci dan klik **Copy resource name**.

        <Frame caption="Salin nama resource lengkap kunci dari menu tindakan.">
          ![Detail key ring di Google Cloud dengan tindakan Copy resource name disorot di menu tindakan kunci.](https://platform.claude.com/docs/images/cmek/gcp-copy-resource-name.png)
        </Frame>
      </Step>
    </Steps>
  </Tab>

  <Tab title="gcloud CLI">
    Di setiap perintah, ganti placeholder berikut:

    * **`<your-project-id>`:** ID proyek Google Cloud Anda
    * **`<region>`:** lokasi kunci, seperti `us-east5`
    * **`<your-keyring-name>`:** nama key ring
    * **`<your-key-name>`:** nama kunci
    * **`<ORGANIZATION_UUID>`:** ID organisasi Anthropic Anda dalam huruf kecil

    <Steps>
      <Step title="Buat atau pilih key ring">
        Lewati langkah ini jika Anda sudah memiliki key ring untuk digunakan kembali.

        ```bash
        gcloud kms keyrings create <your-keyring-name> \
          --project=<your-project-id> \
          --location=<region>
        ```
      </Step>

      <Step title="Buat kunci">
        ```bash
        gcloud kms keys create <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --purpose=encryption \
          --protection-level=hsm \
          --labels=anthropic-org-<ORGANIZATION_UUID>=true
        ```

        Untuk perlindungan perangkat lunak, hilangkan `--protection-level=hsm`.
      </Step>

      <Step title="Berikan akun layanan Anthropic akses ke kunci">
        Jalankan kedua perintah:

        ```bash
        gcloud kms keys add-iam-policy-binding <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
          --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
        ```

        ```bash
        gcloud kms keys add-iam-policy-binding <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --member="serviceAccount:anthropic-cmek-client-us@gcp-anthropic-cmek-clients.iam.gserviceaccount.com" \
          --role=roles/cloudkms.viewer
        ```
      </Step>

      <Step title="Dapatkan nama resource kunci lengkap">
        ```bash
        gcloud kms keys describe <your-key-name> \
          --project=<your-project-id> \
          --location=<region> \
          --keyring=<your-keyring-name> \
          --format="value(name)"
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

Anda mendaftarkan kunci dengan nama resource lengkapnya, dalam format berikut:

```text wrap
projects/<your-project-id>/locations/<region>/keyRings/<your-keyring-name>/cryptoKeys/<your-key-name>
```

<Note>
  **Kunci yang sudah Anda miliki:** Tambahkan label organisasi dengan perintah ini, di Cloud Shell atau dengan gcloud CLI:

  ```bash
  gcloud kms keys update <your-key-name> \
    --project=<your-project-id> \
    --location=<region> \
    --keyring=<your-keyring-name> \
    --update-labels=anthropic-org-<ORGANIZATION_UUID>=true
  ```

  Placeholder tersebut sesuai dengan bagian-bagian dari nama resource lengkap kunci. Perintah ini menggabungkan label dengan label apa pun yang sudah dimiliki kunci. Kemudian berikan akses dan salin nama resource seperti yang dijelaskan pada langkah-langkah sebelumnya.

  Untuk berbagi satu kunci di antara beberapa organisasi Anthropic, tambahkan satu label organisasi untuk masing-masing.
</Note>

## Daftarkan kunci dengan Anthropic

<Tabs>
  <Tab title="Claude Platform">
    <Tabs>
      <Tab title="Claude Console">
        <Steps>
          <Step title="Buka pengaturan kunci enkripsi">
            Di Claude Console, buka halaman [Data retention](https://platform.claude.com/settings/privacy#encryption-keys) (`platform.claude.com/settings/privacy`). Jika Anda tidak melihat **Encryption keys**, pilih **Organization** dari menu dropdown di bagian atas halaman.
          </Step>

          <Step title="Tambahkan kunci">
            Di bawah **Encryption keys**, klik **Add key**. Masukkan **Display name** dan pilih **Google Cloud KMS**. Klik **Continue**.
          </Step>

          <Step title="Masukkan nama resource kunci">
            Kotak dialog menampilkan **Organization label**. Pastikan kunci Anda memiliki label ini. Tempelkan nama resource kunci lengkap ke **Key resource name**, lalu klik **Add**.
          </Step>

          <Step title="Validasi kunci">
            Di daftar **Encryption keys**, klik **Verify** di samping kunci. **Connected** muncul saat pemeriksaan berhasil. Jika gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#troubleshoot-validation) untuk penyebab umum.
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
            Ganti `<friendly-name>` dengan nama tampilan. Ganti nilai yang diawali `projects/` dengan nama resource kunci lengkap.

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

            Jika validasi gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#troubleshoot-validation).
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
        Klik **Add key**. Masukkan **Display name** dan pilih **Google Cloud KMS**. Centang kotak untuk mengonfirmasi bahwa Anda telah membaca dokumentasi CMEK, lalu klik **Continue**.
      </Step>

      <Step title="Masukkan nama resource kunci">
        Kotak dialog menampilkan **Organization label**. Pastikan kunci Anda memiliki label ini. Tempelkan nama resource kunci lengkap ke **Key resource name**, lalu klik **Add**.
      </Step>

      <Step title="Konfirmasi bahwa validasi berhasil">
        Ketika pemeriksaan berhasil, **Encryption key configured** muncul, dan organisasi Anda dilindungi CMEK sejak saat itu. Jika pemeriksaan gagal, lihat [Memecahkan masalah validasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#troubleshoot-validation).
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Memecahkan masalah validasi

Jika validasi gagal, penyebab umumnya adalah:

* **Label organisasi salah:** Pastikan kunci memiliki [label organisasi](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#organization-label), dengan ID organisasi polos Anda dalam huruf kecil.
* **VPC Service Controls:** Perimeter layanan yang melindungi Cloud KMS di proyek Anda dapat memblokir Anthropic. Tambahkan Anthropic ke access level pada perimeter, atau kecualikan proyek kunci dari perimeter tersebut.
* **Berbagi terbatas domain:** Kebijakan org `constraints/iam.allowedPolicyMemberDomains` memblokir binding untuk akun layanan Anthropic. Untuk memeriksa bahwa binding tersebut ada, jalankan `gcloud kms keys get-iam-policy <your-key-name> --project=<your-project-id> --location=<region> --keyring=<your-keyring-name>`. Untuk mengizinkannya, lihat [Email akun layanan Anthropic](https://platform.claude.com/docs/id/manage-claude/cmek-google-cloud-kms#anthropic-service-account-email).
* **Versi kunci dinonaktifkan atau dihancurkan:** Konfirmasikan bahwa versi utama kunci diaktifkan.

## Terraform

Untuk membuat kunci dengan Terraform, gunakan resource `google_kms_key_ring`, `google_kms_crypto_key`, dan `google_kms_crypto_key_iam_member` dari provider `google`.
