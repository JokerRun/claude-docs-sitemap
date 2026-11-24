---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: c363f7bd674e762e1926658e09b4d89d475ac343e8cccd6e017bfa6190d2418b
---

---
title: Menyiapkan penyimpanan milik pelanggan
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage
description: Buat bucket di akun cloud Anda sendiri, hubungkan bucket tersebut di Claude Console, dan pastikan data keselamatan tersegel Anda masuk ke dalamnya.
---

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

Dengan Enterprise Frontier Safeguards (EFS), [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage) menyimpan data keselamatan tersegel sebuah workspace di bucket dalam akun cloud Anda sendiri.

<Where cloud="aws" label="Claude Platform on AWS">

Mulailah dengan [Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws), dan gunakan halaman ini untuk bucket itu sendiri.

</Where>

<Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">

Mulailah dengan [Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed).

</Where>

<Where bucket="s3" label="Amazon S3">

## Menyiapkan penyimpanan milik pelanggan di Amazon S3

<Where method="console" label="Claude Console">

Untuk menyiapkan penyimpanan Anda di Amazon S3, buat sumber daya di akun cloud Anda sendiri, lalu hubungkan di Claude Console:

1. [Perbarui kebijakan organisasi cloud Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic) untuk mengizinkan akses dari akun eksternal tertentu.
2. [Buat bucket Anda dan kunci enkripsinya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket).
3. [Buat peran](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-roles) yang memberi Anthropic akses ke bucket Anda.
4. [Hubungkan bucket Anda di Claude Console](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#connect-the-bucket), lalu uji penyiapan.

Setelah pengujian lolos, Anda dapat [menggunakan bucket Anda di workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#use-your-bucket-in-a-workspace).

Dialog **Connect storage** memberi Anda file penyiapan dan menguji penyiapan Anda.

</Where>

<Where method="api" label="Admin API">

Anda dapat menggunakan Admin API untuk mendaftarkan, memeriksa, dan melampirkan bucket Amazon S3 Anda untuk [penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage). Admin API berguna jika Anda ingin membuat skrip untuk penyiapan Anda atau mengelola banyak workspace. Meskipun Anda dapat menangani sebagian besar langkah melalui API, Anda tetap perlu mendapatkan file penyiapan dari Claude Console, seperti yang dijelaskan di [Dapatkan file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#get-the-setup-file).

Di API, External Storage adalah catatan Anthropic tentang bucket Anda, bukan bucket Anda itu sendiri.

</Where>

## Sebelum Anda memulai

Pastikan Anda memiliki hal-hal berikut:

* **Organization Admin** di Claude Console, yang mendapatkan file penyiapan dan menghubungkan bucket Anda.
* **[Akses ke Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console).** Jika organisasi Anda memilikinya, halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console menampilkannya dengan tombol **Configure**.
* **Akun cloud untuk bucket Anda.** Anthropic merekomendasikan akun khusus yang hanya menampung bucket ini dan belum pernah digunakan oleh organisasi Anthropic lain untuk penyimpanan milik pelanggan. Anda juga dapat [menggunakan akun yang menampung bucket lain](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles).
* **Tidak ada otomatisasi yang menghapus bucket Anda, kuncinya, atau peran.** Tanyakan kepada tim yang mengelola akun cloud tersebut, karena beberapa akun uji memiliki job pembersihan. Jika sesuatu menghapus salah satunya, [bucket Anda berhenti berfungsi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#if-your-bucket-stops-working).

<Warning title="Menggunakan bucket mengikatnya ke satu organisasi Anthropic">
  Saat pertama kali Anda menggunakan bucket, Anda mengikat bucket, namanya, kuncinya, dan peran-perannya ke organisasi ini. Penggunaan pertama itu terjadi saat Anda memilih bucket untuk sebuah workspace dan menyimpannya, atau membuat workspace dengan bucket tersebut (di API, permintaan attach pertama yang berhasil). Anggap ikatan ini bersifat permanen. Jangan berencana agar organisasi Anthropic lain menggunakan bucket, namanya, kuncinya, atau peran-perannya untuk penyimpanan milik pelanggan.
</Warning>

<Where method="api" label="Admin API">

### Autentikasi permintaan Anda

<Tabs>
  <Tab title="cURL">
    Setiap permintaan di halaman ini mengirim `anthropic-version: 2026-10-21` dan `anthropic-beta: efs-2026-10-01`. Kirim salah satu kredensial berikut dengan setiap permintaan:

    * **Token bearer OAuth dengan cakupan `org:admin`:** Setiap permintaan di halaman ini menerimanya di header `authorization: Bearer`. Untuk mendapatkannya, lihat [Token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token). Contoh-contohnya membacanya dari `$ANTHROPIC_AUTH_TOKEN`. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.
    * **Kunci pribadi atau kunci akun layanan:** Setiap permintaan di halaman ini menerimanya di `x-api-key`. Gunakan kunci yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Admin API menolak kunci yang dibatasi pada sebuah workspace, bahkan untuk permintaan pada workspace tersebut.
    * **Kunci Admin API:** Kunci ini tidak dapat melampirkan atau melepas penyimpanan: permintaan tersebut mengembalikan error izin. Permintaan External Storage menerimanya di `x-api-key`. Untuk mendapatkannya, lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).

    Untuk token atau kunci pribadi atau kunci akun layanan, akunnya harus memiliki peran admin. Untuk menggunakan kunci, ganti header `authorization` di setiap contoh dengan `x-api-key: $ANTHROPIC_API_KEY`.
  </Tab>

  <Tab title="CLI">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, CLI `ant` mengirim kunci. Token berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru. Biarkan `ANTHROPIC_WORKSPACE_ID` tidak diatur: jika diatur, kunci akan mendapatkan error 400 pada permintaan ini.

    CLI mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, CLI juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, CLI tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` dengan `--beta`, seperti yang ditunjukkan contoh attach dan detach.

    Saat API menolak permintaan, CLI mencetak seluruh body respons. Cari `error.details.error_code` di sana.
  </Tab>

  <Tab title="Python">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="TypeScript">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="C#">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="Go">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="Java">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="PHP">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>

  <Tab title="Ruby">
    Gunakan satu kredensial untuk setiap permintaan di halaman ini. Gunakan [token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan cakupan `org:admin`. Atau gunakan kunci pribadi atau kunci akun layanan yang tidak dibatasi pada sebuah workspace (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Apa pun pilihannya, akun tersebut harus memiliki peran admin. Jangan gunakan kunci Admin API: kunci tersebut tidak dapat melampirkan atau melepas penyimpanan.

    Atur `ANTHROPIC_AUTH_TOKEN` ke token, atau `ANTHROPIC_API_KEY` ke kunci. Atur hanya salah satunya: jika keduanya diatur, SDK mengirim kunci. Token tersebut berumur pendek: jika permintaan mengembalikan error 401, dapatkan token baru.

    SDK mengirim kredensial Anda dan header `anthropic-version` untuk Anda. Pada permintaan External Storage, SDK juga mengirim `anthropic-beta: efs-2026-10-01`. Pada permintaan workspace yang mengatur `inference_data_privacy`, SDK tidak mengirimnya, jadi teruskan sendiri `efs-2026-10-01` ke SDK, seperti yang ditunjukkan contoh-contoh lampirkan dan lepas.

    Ketika API menolak permintaan, panggilan SDK gagal dengan error yang teksnya memuat seluruh body respons. Cari di sana `error.details.error_code`.
  </Tab>
</Tabs>

## Daftarkan bucket Anda

Anda dapat mendaftarkan bucket Anda sebelum Anda membuatnya. Claude Console menggunakan detail yang Anda daftarkan untuk mengisi [file penyiapan Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#get-the-setup-file).

Beri tahu Anthropic bucket mana yang akan Anda gunakan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/organizations/external_storage \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01" \
    -H "content-type: application/json" \
    -d '{
      "display_name": "Claude retention",
      "provider_config": {
        "type": "aws",
        "account_id": "111122223333",
        "bucket_name": "acme-claude-retention",
        "region": "us-east-2"
      }
    }'
  ```

  ```bash CLI
  ant beta:organization:external-storage create \
    --display-name "Claude retention" \
    --provider-config '{type: aws, account_id: "111122223333", bucket_name: acme-claude-retention, region: us-east-2}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  storage = client.beta.organization.external_storage.create(
      display_name="Claude retention",
      provider_config={
          "type": "aws",
          "account_id": "111122223333",
          "bucket_name": "acme-claude-retention",
          "region": "us-east-2",
      },
  )

  print(f"id: {storage.id}")
  print(f"status: {storage.status.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const storage = await client.beta.organization.externalStorage.create({
    display_name: "Claude retention",
    provider_config: {
      type: "aws",
      account_id: "111122223333",
      bucket_name: "acme-claude-retention",
      region: "us-east-2"
    }
  });

  console.log(`id: ${storage.id}`);
  console.log(`status: ${storage.status.type}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ExternalStorage;

  AnthropicClient client = new();

  var storage = await client.Beta.Organization.ExternalStorage.Create(new()
  {
      DisplayName = "Claude retention",
      ProviderConfig = new BetaAwsExternalStorageConfigParam
      {
          AccountID = "111122223333",
          BucketName = "acme-claude-retention",
          Region = "us-east-2",
      },
  });

  Console.WriteLine($"id: {storage.ID}");
  Console.WriteLine($"status: {storage.Status.Type.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  storage, err := client.Beta.Organization.ExternalStorage.New(
  	context.Background(),
  	anthropic.BetaOrganizationExternalStorageNewParams{
  		DisplayName: anthropic.String("Claude retention"),
  		ProviderConfig: anthropic.BetaOrganizationExternalStorageNewParamsProviderConfigUnion{
  			OfAWS: &anthropic.BetaAWSExternalStorageConfigParam{
  				AccountID:  "111122223333",
  				BucketName: "acme-claude-retention",
  				Region:     "us-east-2",
  			},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", storage.ID)
  fmt.Printf("status: %s\n", storage.Status.Type)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.externalstorage.BetaAwsExternalStorageConfigParam;
  import com.anthropic.models.beta.organization.externalstorage.ExternalStorageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ExternalStorageCreateParams.builder()
          .displayName("Claude retention")
          .providerConfig(BetaAwsExternalStorageConfigParam.builder()
              .accountId("111122223333")
              .bucketName("acme-claude-retention")
              .region("us-east-2")
              .build())
          .build();
      var storage = client.beta().organization().externalStorage().create(params);

      IO.println("id: " + storage.id());
      IO.println("status: " + storage.status().type());
  }
  ```

  ```php PHP
  $client = new Client();

  $storage = $client->beta->organization->externalStorage->create(
      displayName: 'Claude retention',
      providerConfig: [
          'type' => 'aws',
          'accountID' => '111122223333',
          'bucketName' => 'acme-claude-retention',
          'region' => 'us-east-2',
      ],
  );

  echo "id: {$storage->id}\n";
  echo "status: {$storage->status->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  storage = client.beta.organization.external_storage.create(
    display_name: "Claude retention",
    provider_config: {
      type: :aws,
      account_id: "111122223333",
      bucket_name: "acme-claude-retention",
      region: "us-east-2"
    }
  )

  puts "id: #{storage.id}"
  puts "status: #{storage.status.type}"
  ```
</CodeGroup>

`provider_config` mengidentifikasi bucket Anda. Sebelum Anda mengirim permintaan, periksa setiap field terhadap batasannya:

* `type`: `aws`.
* `account_id`: ID 12 digit dari akun AWS yang memiliki bucket Anda. [Buat dan hubungkan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles) menguraikan kapan sebuah akun dapat menampung lebih dari satu bucket.
* `bucket_name`: unik secara global, terdiri dari 3 hingga 63 huruf kecil, angka, dan tanda hubung, diawali dan diakhiri dengan huruf atau angka, tanpa titik. Jika file penyiapan yang membuat bucket Anda, jangan gunakan kembali nama bucket yang sudah Anda miliki.
* `region`: region AWS tempat bucket Anda berada, salah satu dari [region yang didukung Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket). Jika bucket Anda tidak berada di region yang Anda berikan, [pengaktifan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-activate) akan gagal.

Responsnya terlihat seperti ini:

```json
{
  "type": "external_storage",
  "id": "estrg_01SDCCSbTxrXDpWc1phhtcfK",
  "display_name": "Claude retention",
  "provider_config": {
    "type": "aws",
    "account_id": "111122223333",
    "bucket_name": "acme-claude-retention",
    "region": "us-east-2"
  },
  "status": {
    "type": "pending_configuration"
  },
  "setup_template_version": null,
  "created_at": "2026-10-08T17:00:00Z",
  "updated_at": "2026-10-08T17:00:00Z"
}
```

Simpan `id` bucket Anda, yang diawali `estrg_`, untuk digunakan pada langkah-langkah selanjutnya.

Permintaan dapat gagal karena alasan seperti berikut:

* **Organisasi Anda belum disetujui:** Jika organisasi Anda dapat membuat permintaan ini tetapi Anthropic belum menyetujuinya untuk menggunakan penyimpanan milik pelanggan, respons akan meminta Anda menghubungi tim akun Anthropic Anda.
* **Organisasi Anda tidak memenuhi syarat:** Jika `error.details.error_code` bernilai `organization_not_eligible`, penyimpanan milik pelanggan tidak tersedia untuk organisasi Anda.
* **Bucket sudah terdaftar:** Anthropic menolak pendaftaran kedua untuk bucket yang sama. Untuk menemukan yang sudah ada, tampilkan daftar External Storage Anda dengan `GET /v1/organizations/external_storage`.

</Where>

## Buat dan hubungkan bucket Anda

Untuk menyiapkan penyimpanan milik pelanggan, Anda perlu membuat tiga hal di akun AWS Anda: bucket Anda, kunci KMS, dan peran IAM. Dengan CloudFormation atau Terraform, satu file membuat semuanya. Dengan tooling Anda sendiri, Anda membuat masing-masing sendiri.

Anda dapat menempatkan lebih dari satu bucket di akun AWS yang sama, bahkan jika bucket-bucket tersebut milik organisasi Anthropic yang berbeda. Jika Anda melakukannya, atau jika tim lain bekerja di akun tersebut, perhatikan hal-hal berikut:

* **Sumber daya terpisah:** Setiap organisasi memerlukan bucket dan kunci KMS-nya sendiri, dan setiap bucket memerlukan stack-nya sendiri atau, dengan Terraform, folder-nya sendiri.
* **Siapa lagi yang bekerja di akun tersebut:** Siapa pun di akun AWS tersebut yang dapat membuat peran IAM, atau yang memiliki izin Amazon S3 dan AWS KMS yang luas, dapat membaca transkrip dan file Safety Case Anda, menghapus file, dan memutus akses Anthropic.

### 1. Perbarui kebijakan organisasi AWS Anda

Pada langkah ini, Anda menambahkan pengecualian untuk akun AWS Anthropic ke kebijakan organisasi AWS Anda, agar Anthropic dapat menjangkau bucket Anda. Anda hanya memerlukan langkah ini jika organisasi AWS Anda memiliki kebijakan kontrol sumber daya (RCP) yang menolak tindakan AWS STS untuk principal di luar organisasi. Jika Anda melewati perubahan ini di bawah kebijakan seperti itu, **Test setup** gagal pada peran IAM. Perubahan ini sering kali dilakukan oleh tim lain, jadi sebaiknya mintalah sejak awal.

Anthropic menjangkau bucket Anda melalui peran IAM yang Anda buat di langkah selanjutnya. Anthropic mengambil alih (assume) peran-peran tersebut dari akun AWS miliknya, `804820989669`, dan bekerja di Amazon S3 dan AWS KMS sebagai peran-peran tersebut. Di bawah RCP jenis itu, AWS menolak permintaan Anthropic untuk mengambil alih peran-peran tersebut, apa pun isi kebijakan kepercayaan peran.

#### Cari tahu apakah langkah ini berlaku

Jika Anda membuat akun AWS Anda dengan **Sign up for AWS (new)**, langkah ini berlaku. Akun tersebut termasuk dalam organisasi AWS yang kebijakannya dikelola oleh AWS, dan kebijakan tersebut mencakup RCP jenis ini. Kebijakannya adalah `ManagedAccountResourceControlPolicy`, dan pernyataannya adalah `DenyAnyoneOutsideMyOrgAndAWS`. Sebelum Anda mencoba mengubah kebijakan tersebut, baca [Kebijakan terkelola untuk organisasi Anda](https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html) di dokumentasi AWS.

Untuk akun lainnya, tanyakan kepada tim yang mengelola kebijakan organisasi AWS Anda apakah ada RCP yang menolak tindakan AWS STS untuk principal di luar organisasi. Jika tidak ada, lewati perubahan ini dan lanjutkan ke [langkah 2](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket).

#### Tambahkan akun AWS Anthropic ke kebijakan

Mintalah tim yang mengelola kebijakan organisasi AWS Anda untuk menambahkan akun AWS Anthropic ke pernyataan yang menolak principal luar. Dalam contoh ini, baris yang ditambahkan adalah `aws:PrincipalAccount`, di samping ID organisasi:

```json
{
  "Sid": "EnforceOrgIdentities",
  "Effect": "Deny",
  "Principal": "*",
  "Action": ["sts:*", "s3:*", "kms:*"],
  "Resource": "*",
  "Condition": {
    "StringNotEqualsIfExists": {
      "aws:PrincipalOrgID": "o-exampleorgid",
      "aws:PrincipalAccount": "804820989669"
    },
    "BoolIfExists": { "aws:PrincipalIsAWSService": "false" }
  }
}
```

Jika pernyataan Anda sendiri sudah mencantumkan akun di bawah `aws:PrincipalAccount`, tambahkan `804820989669` ke daftar itu alih-alih menambahkan baris kedua.

Jika sebuah workspace di Claude Platform juga menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys) di AWS KMS, Anthropic memanggil kunci tersebut dari akun `915198916910`. Jika pernyataan Anda menolak tindakan AWS KMS, tambahkan juga akun tersebut.

Baris yang ditambahkan dalam contoh tersebut mengecualikan setiap principal di akun AWS Anthropic, untuk setiap tindakan dan setiap sumber daya yang dicakup pernyataan tersebut. Pengecualian yang lebih sempit seharusnya sudah cukup, tetapi sejauh ini Anthropic hanya melihat **Test setup** lolos dengan pengecualian untuk seluruh akun. Untuk mengetahui apa yang harus diizinkan oleh pengecualian yang lebih sempit, lihat [Referensi template](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#template-reference).

<Where method="console" label="Claude Console">

#### Pastikan perubahan berhasil

Untuk memeriksa perubahan, jalankan **Test setup** di langkah 4. Jika sebuah kebijakan memblokir Anthropic, pengujian menampilkan [beberapa pemeriksaan yang gagal](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).

</Where>

### 2. Buat bucket Anda dan kunci KMS-nya

Pada langkah ini, Anda membuat bucket yang menyimpan data Anda, beserta kunci KMS-nya. Kunci KMS adalah kunci enkripsi default bucket, sehingga kunci tersebut mengenkripsi apa yang ditulis Anthropic di sana. Kunci ini terpisah dari [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) yang Anda lampirkan ke workspace.

Buat bucket Anda dan kunci KMS-nya di salah satu region AWS berikut: `us-east-2`, `us-east-1`, `us-west-2`, `eu-central-1`, `eu-west-1`, `ap-northeast-1`, atau `ap-southeast-2`. Anda tidak dapat mengubah region bucket di kemudian hari. Region bucket Anda menentukan tempat penyedia cloud Anda menyimpan objek-objek bucket. Region tersebut tidak mengubah [tempat inferensi model berjalan](https://platform.claude.com/docs/id/manage-claude/data-residency#inference-geo) atau tempat Anthropic memproses data Anda. Anthropic merekomendasikan `us-east-2` karena Anthropic membaca dan menulis bucket Anda dari `us-east-2`.

File penyiapan membuat kunci dan bucket dengan pengaturan berikut:

| Sumber daya | Pengaturan |
| ----- | ----- |
| Kunci KMS | Kunci single-region di akun AWS dan region yang sama dengan bucket, dengan rotasi aktif. Akun Anda yang mengelolanya. Kebijakannya tidak menyebut Anthropic maupun peran-peran tersebut. |
| Bucket | Pembuatan versi aktif. Enkripsi default dengan kunci KMS, yang disebutkan berdasarkan ARN kuncinya, dengan S3 Bucket Key aktif. Akses publik diblokir. ACL nonaktif (`BucketOwnerEnforced`). S3 Object Lock nonaktif. |
| Aturan siklus hidup | Tabel berikutnya mencantumkan apa yang dilakukannya. |
| S3 Inventory | Laporan harian untuk `slab/` dan `media/`. Amazon S3 mengirimkannya di bawah `inventory/` di bucket yang sama. Dua laporan lagi mencakup prefiks yang sama di bawah `safeguards-data/` dan ditempatkan di bawah `safeguards-data/inventory/`. |
| Kebijakan bucket | Kebijakan ini menolak penghapusan permanen versi objek di bawah `slab/`, menolak permintaan tanpa TLS, dan mengizinkan Amazon S3 mengirimkan laporan inventaris. Kebijakan ini juga menolak setiap peran IAM yang namanya diawali `anthropic-efs-`, kecuali milik penyiapan ini. |

Jangan gunakan `anthropic-efs-` dalam nama dan path peran Anda sendiri, termasuk peran yang men-deploy file tersebut, karena kebijakan bucket menolak peran-peran tersebut.

Aturan siklus hidup melakukan hal berikut:

| Yang menjadi sasaran aturan siklus hidup | Yang dilakukannya |
| ----- | ----- |
| Versi lama di bawah `slab/` dan `media/` | Menghapusnya setelah 3 hari |
| Multipart upload yang tidak selesai | Menghentikannya setelah 7 hari |
| Laporan inventaris | Membuatnya kedaluwarsa setelah 14 hari |
| Penanda hapus yang tersisa | Menghapusnya |
| Transkrip dan ringkasan Safety Case | Membuatnya kedaluwarsa setelah 28 hari, dan menghapus versi sebelumnya 3 hari kemudian |
| File Safety Case lainnya, termasuk respons tim Anda | Membuatnya kedaluwarsa setelah 2.555 hari (sekitar 7 tahun), dan menyimpan setiap versi sebelumnya selama jumlah hari yang sama setelah versi tersebut tidak lagi menjadi versi terkini |

#### Dapatkan file penyiapan Anda

<Where method="console" label="Claude Console">

Dapatkan file penyiapan dan perintahnya dari langkah **Create in AWS** pada dialog **Connect storage**. Jika dialog belum terbuka, buka dialog seperti yang dijelaskan di [langkah 4](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#connect-the-bucket), masukkan detail bucket Anda, dan berhenti di **Create in AWS**. Simpan file dan perintah tersebut, karena Claude Console tidak menampilkannya lagi setelah pengujian lolos. Jika orang lain yang menjalankan file tersebut di AWS, kirimkan file dan perintah tersebut kepada mereka, lalu klik **Test setup** saat mereka sudah selesai.

</Where>

<Where method="api" label="Admin API">

Dapatkan file penyiapan dan perintah-perintahnya dari Claude Console, yang mengisikan nilai-nilai Anda. Sebagai Organization Admin, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) dan pilih **Organisasi** di bagian atas. Klik **Finish setup** di samping bucket yang Anda daftarkan, dan berhenti di **Create in AWS**. Jalankan file tersebut seperti yang dijelaskan di [Buat bucket Anda dan kunci KMS-nya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket). Anda juga dapat membuat sumber daya yang sama dengan cara lain, asalkan sesuai dengan file tersebut.

</Where>

Buat semuanya di region yang Anda masukkan di dialog, meskipun header file menyebut `us-east-2`. Untuk bucket baru, jalankan hanya file yang diberikan dialog, yang membuat tujuh peran. Jika Anda sudah menjalankan file sebelumnya yang membuat peran dengan nama tetap, lihat “Test setup menyatakan bahwa Anthropic tidak dapat mengambil alih peran verify” di [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).

<Warning title="Jangan jalankan file tujuh peran di atas penyiapan dengan nama peran tetap">
  Jika Anda memiliki penyiapan yang telah lolos **Test setup** dan perannya memiliki nama tetap, seperti `anthropic-efs-ingest`, biarkan penyiapan tersebut dan tujuan penyimpanannya apa adanya. Di folder Terraform penyiapan tersebut, jangan terapkan file yang membuat tujuh peran, karena apply akan menghapus peran-peran bernama tetap tersebut dan memutus akses Anthropic.
</Warning>

<Tabs>
  <Tab title="CloudFormation">
    #### Deploy stack CloudFormation

    1. **Periksa akun AWS.** Simpan file di folder kosong. Dari folder tersebut, jalankan `aws sts get-caller-identity` dan pastikan perintah itu menampilkan akun AWS untuk bucket Anda.
    2. **Deploy stack.** Di terminal yang sama, jalankan perintah deploy dari dialog persis seperti yang ditampilkan, yang sudah berisi nilai-nilai Anda. Jangan ubah nama stack, `anthropic-storage-<RoleDigest>`, karena template menolak nama lain. `RoleDigest` adalah nilai 20 karakter yang sudah ada di dalam perintah.

    **Pastikan berhasil.** Perintah mencetak `Successfully created/updated stack` dan nama stack Anda. Jika deploy gagal, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).
  </Tab>

  <Tab title="Terraform">
    #### Terapkan file Terraform

    File Terraform memerlukan Terraform 1.5 atau lebih baru dan versi 5 atau 6 dari provider AWS.

    1. **Periksa akun AWS.** Simpan file di folder kosong, karena Terraform memuat setiap file `.tf` di folder tersebut. Jalankan `aws sts get-caller-identity` dan pastikan perintah itu menampilkan akun AWS untuk bucket Anda.
    2. **Terapkan file.** Dari folder itu, jalankan perintah-perintah dari dialog, yang sudah berisi nilai-nilai Anda. Jangan edit file tersebut. Baca rencana sebelum Anda mengetik `yes`, pada apply ini dan setiap apply berikutnya, dan berhenti jika rencana pertama menampilkan sesuatu yang akan dihancurkan.

    **Pastikan berhasil.** Apply diakhiri dengan `Apply complete!` dan mencantumkan output-nya, termasuk nama bucket, region-nya, dan ARN kunci. Jika apply gagal, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).

    Simpan seluruh folder, termasuk `terraform.tfstate`, `.terraform/`, dan `.terraform.lock.hcl`. File tersebut tidak memiliki blok backend, sehingga Terraform menyimpan state-nya di sana. Jika Anda kehilangan state tersebut, apply berikutnya gagal pada bucket hingga Anda memulihkan state atau menjalankan `terraform import` untuk sumber daya tersebut.
  </Tab>

  <Tab title="Your own tooling">
    #### Buat kunci dan bucket sendiri

    Dengan tooling Anda sendiri, Anda membangun dari template CloudFormation. [Buka langkah **Create in AWS**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#get-the-setup-file) pada dialog **Connect storage**, pilih **CloudFormation** untuk mengunduh template, lalu pilih **Your own tooling** dan catat external ID dan ARN peran. Salin setiap pengaturan dari template tersebut, karena **Test setup** memeriksa sebagian penyiapan Anda terhadap template tersebut. Ganti placeholder `${…}` dalam template dengan nilai Anda sendiri. Untuk partisi, gunakan `aws`.

    **Buat kunci:**

    * Buat kunci KMS single-region di akun AWS bucket Anda, di region tempat Anda membuat bucket. Samakan dengan kunci template, yang bersifat simetris dan rotasinya aktif.
    * Salin kebijakan kunci template, yang mengizinkan akun Anda mengelola kunci. Kebijakan itu juga mengizinkan Amazon S3 memanggil `kms:GenerateDataKey` untuk akun ini dan bucket ini, agar S3 Inventory dapat mengirimkan laporan hariannya.

    **Buat bucket** dengan pengaturan di tabel langkah ini. Salin aturan siklus hidup, konfigurasi S3 Inventory, dan kebijakan bucket dari template, dan jangan tambahkan aturan siklus hidup lain.

    Di enkripsi default bucket, sebutkan kunci berdasarkan ARN kuncinya. **Test setup** gagal jika Anda menyebut kunci berdasarkan nama alias, ARN alias, atau ID kunci saja. Test setup juga gagal jika bucket Anda tidak memiliki salah satu aturan siklus hidup wajib dari template, atau memiliki aturan lain yang membuat objek kedaluwarsa.

    **Test setup** tidak memeriksa bagian-bagian berikut dari penyiapan Anda, jadi bandingkan sendiri dengan template:

    * Sisa kebijakan bucket. **Test setup** hanya memeriksa dua pernyataan yang menolak peran milik penyiapan lain.
    * Konfigurasi S3 Inventory.
    * Kebijakan kunci KMS dan pengaturannya, seperti rotasi. **Test setup** hanya mengonfirmasi bahwa Anthropic dapat menggunakan kunci tersebut melalui Amazon S3.
  </Tab>
</Tabs>

### 3. Buat peran IAM

Langkah ini membahas tujuh peran IAM yang memberi Anthropic akses ke bucket Anda. Setiap peran mengizinkan satu jenis pekerjaan. Nama setiap peran adalah `anthropic-efs-<RoleDigest>-<ending>`, dengan `RoleDigest` adalah nilai 20 karakter yang khusus untuk penyiapan ini.

| Akhiran nama peran | Yang dilakukan Anthropic melalui peran ini | Yang dapat dilakukannya dengan kunci KMS bucket Anda |
| ----- | ----- | ----- |
| `ingest` | Menulis data keselamatan tersegel Anda di bawah `slab/` dan `media/`. | `kms:GenerateDataKey` dan `kms:Decrypt` |
| `read` | Membaca di bawah `slab/`, `media/`, dan `slab-manifest/`, serta mencantumkan ketiga prefiks tersebut. | `kms:Decrypt` |
| `maintenance` | Membaca dan menulis objek di bawah `slab/`, `media/`, dan `slab-manifest/`, serta menambahkan penanda hapus pada objek tersebut. Membaca laporan inventaris di bawah `inventory/` dan konfigurasi bucket. Mencantumkan `slab/`, `media/`, `slab-manifest/`, dan `inventory/`. Dapat mencantumkan multipart upload yang belum selesai di mana saja di dalam bucket. Peran ini tidak pernah menghapus versi objek. | `kms:GenerateDataKey` dan `kms:Decrypt` |
| `media-erasure` | Mencantumkan `media/` dan menghapus versi objek di bawahnya secara permanen, dan tidak melakukan hal lain. | Tidak ada |
| `verify` | Menulis, membaca, dan menghapus objek uji beserta versinya di bawah `verify/`, serta mencantumkan versi objek di sana. Membaca konfigurasi bucket. Dapat membaca manifes laporan inventaris di bawah `inventory/`, dan mencantumkan `inventory/`. | `kms:GenerateDataKey`, `kms:Decrypt`, dan `kms:DescribeKey` |
| `transcripts` | Menulis transkrip di bawah `transcripts/`. Mencantumkan dan menghapus versinya secara permanen. Peran ini tidak dapat membaca transkrip. | `kms:GenerateDataKey` dan `kms:Decrypt` |
| `review` | Menulis, membaca, dan mencantumkan Safety Cases di bawah `review-cases/`. Menulis ringkasan dan Safety Notices di bawah `review-summaries/` dan `review-notices/`. Membaca dan mencantumkan respons tim Anda di bawah `review-responses/`. Dapat menghapus kasus, ringkasan, dan Safety Notices secara permanen. Peran ini tidak dapat membaca transkrip, atau menulis, mengubah, maupun menghapus respons. | `kms:GenerateDataKey` dan `kms:Decrypt` |

Setiap peran hanya memercayai peran di akun AWS Anthropic, `804820989669`, yang namanya diawali dengan `anthropic-storage-broker-` (untuk peran review, `anthropic-review-broker-`). Pemanggil harus berada di organisasi AWS milik Anthropic. Setiap peran juga mewajibkan external ID Anda dan source identity dari kumpulan yang diizinkan untuk peran tersebut. File penyiapan Anda berisi kebijakan lengkap setiap peran.

Untuk masing-masing dari lima peran pertama dalam tabel, izinnya juga berlaku untuk prefiks yang sama di bawah `safeguards-data/`, seperti `safeguards-data/slab/`. Aturan siklus hidup dan kebijakan bucket juga mencakup prefiks tersebut. [Apa yang melindungi versi objek di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#what-protects-object-versions) menjelaskan apa yang tidak dapat dihapus oleh peran Anthropic.

<Tabs>
  <Tab title="CloudFormation">
    #### Gunakan peran dari stack CloudFormation

    Stack yang Anda deploy di [langkah 2](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket) telah membuat semua peran, jadi tidak ada yang perlu dijalankan di sini.
  </Tab>

  <Tab title="Terraform">
    #### Gunakan peran dari apply Terraform

    Apply di [langkah 2](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket) telah membuat semua peran, jadi tidak ada yang perlu dijalankan di sini.
  </Tab>

  <Tab title="Your own tooling">
    #### Buat peran sendiri

    Opsi **Your own tooling** di langkah **Create in AWS** mencantumkan ARN peran. Buat satu peran untuk setiap ARN, dengan nama persis seperti yang tercantum di ARN tersebut.

    Salin seluruh kebijakan kepercayaan setiap peran dan izinnya dari template CloudFormation Anda. Izin peran `transcripts` dan `review` ada di `TranscriptsRolePolicy` dan `ReviewRolePolicy`. Lalu, sesuaikan setiap salinan:

    * **Kebijakan kepercayaan:** Atur external ID ke nilai yang ditampilkan **Your own tooling**, dan jangan ubah hal lain.
    * **Izin:** Ganti referensi template dengan nilai Anda sendiri, termasuk region dan ARN kunci KMS Anda.

    Untuk setiap peran, bandingkan sendiri izin dan kebijakan kepercayaannya dengan template. **Test setup** tidak membaca izin maupun kebijakan kepercayaan peran mana pun.
  </Tab>
</Tabs>

<Warning title="Biarkan bucket dan peran apa adanya">
  Setelah Anda membuat bucket dan peran-perannya, jangan ubah bucket, kebijakan bucket-nya, kebijakan kunci KMS-nya, atau peran-perannya. Satu-satunya perubahan yang dapat Anda lakukan adalah mengatur [`ReviewExpiryDays`](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#template-reference). Jika pemeriksaan Anthropic menemukan perubahan lain, pemeriksaan tersebut gagal.
</Warning>

<Where method="console" label="Claude Console">

### 4. Hubungkan bucket Anda di Claude Console

Masuk ke Claude Console di organisasi Anthropic yang workspace-nya akan menggunakan bucket Anda, karena peran-peran tersebut hanya menerima ID organisasi tersebut.

Di halaman [Data retention](https://platform.claude.com/settings/privacy), pilih **Organisasi** di bagian atas. Di bawah **Storage destinations**, klik **Connect storage**, atau klik **Finish setup** jika Anda sudah memulai dialog. Tujuan penyimpanan adalah catatan Claude Console tentang bucket Anda.

#### Pilih penyedia Anda

Pilih **Amazon S3**, lalu klik **Continue**.

#### Masukkan detail bucket Anda

Masukkan ID akun AWS dan region AWS tempat Anda akan membuat bucket Anda. Di bawah **New bucket name**, masukkan nama yang akan Anda berikan untuk bucket baru Anda. Jangan gunakan kembali nama bucket yang sudah Anda miliki.

#### Create in AWS

Jika Anda sudah menjalankan file dari langkah ini, lanjutkan ke **Test setup**. Jika belum, pilih **CloudFormation**, **Terraform**, atau **Your own tooling**, lalu ikuti [langkah 1 hingga 3](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic).

#### Uji penyiapan

Klik **Test setup**. Anthropic memeriksa bucket Anda, kuncinya, dan peran-peran untuk data keselamatan tersegel, serta mencantumkan apa pun yang perlu diperbaiki. Jika pengujian gagal, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).

</Where>

<Where method="api" label="Admin API">

### 4. Aktifkan bucket Anda

Minta Anthropic untuk memeriksa penyiapan Anda. Permintaan ini tidak memiliki body:

<CodeGroup>
  ```bash cURL
  curl -X POST https://api.anthropic.com/v1/organizations/external_storage/estrg_01SDCCSbTxrXDpWc1phhtcfK/activate \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01"
  ```

  ```bash CLI
  ant beta:organization:external-storage activate \
    --external-storage-id estrg_01SDCCSbTxrXDpWc1phhtcfK
  ```

  ```python Python
  client = anthropic.Anthropic()

  storage = client.beta.organization.external_storage.activate(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  )

  print(f"status: {storage.status.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const storage = await client.beta.organization.externalStorage.activate(
    "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  console.log(`status: ${storage.status.type}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var storage = await client.Beta.Organization.ExternalStorage.Activate(
      "estrg_01SDCCSbTxrXDpWc1phhtcfK"
  );

  Console.WriteLine($"status: {storage.Status.Type.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  storage, err := client.Beta.Organization.ExternalStorage.Activate(
  	context.Background(),
  	"estrg_01SDCCSbTxrXDpWc1phhtcfK",
  	anthropic.BetaOrganizationExternalStorageActivateParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("status: %s\n", storage.Status.Type)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var storage = client.beta().organization().externalStorage()
      .activate("estrg_01SDCCSbTxrXDpWc1phhtcfK");

  IO.println("status: " + storage.status().type());
  ```

  ```php PHP
  $client = new Client();

  $storage = $client->beta->organization->externalStorage->activate(
      externalStorageID: 'estrg_01SDCCSbTxrXDpWc1phhtcfK',
  );

  echo "status: {$storage->status->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  storage = client.beta.organization.external_storage.activate("estrg_01SDCCSbTxrXDpWc1phhtcfK")

  puts "status: #{storage.status.type}"
  ```
</CodeGroup>

Anthropic memeriksa bucket Anda, kunci KMS-nya, dan peran untuk data keselamatan tersegel selagi permintaan berjalan. Jika semuanya lolos, statusnya menjadi `available` dan bucket Anda siap untuk dilampirkan. Jika suatu pemeriksaan gagal, lihat [Pemecahan masalah di Mengelola penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-troubleshooting).

</Where>

## Gunakan tujuan penyimpanan Anda di workspace

<Where method="console" label="Claude Console">

Setelah bucket Anda lolos pengujian, pilih bucket tersebut untuk setiap workspace yang akan menggunakannya. Lakukan ini sebelum workspace menangani lalu lintas yang perlu Anda simpan di bucket Anda, karena [perubahan tidak langsung berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Jika organisasi Anda memiliki pengaturan Legacy Zero Data Retention (ZDR), pilih kartu **Enterprise Frontier Safeguards** dan bucket Anda saat Anda membuat workspace. <Where cloud="aws" label="Claude Platform on AWS">Ikuti langkah-langkah Legacy ZDR di [Siapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws).</Where>

</Where>

Anthropic sangat menyarankan kunci yang dikelola pelanggan untuk workspace yang menggunakan penyimpanan milik pelanggan, tetapi tidak mewajibkannya. Sebelum Anda memutuskan, baca [apa yang ditambahkan oleh kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#if-you-use-your-own-bucket) di luar kunci KMS milik bucket Anda sendiri.

<Where method="console" label="Claude Console">

<Warning>
  Memilih bucket untuk sebuah workspace [mengikat bucket tersebut ke organisasi ini](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#before-you-begin). Anggap ikatan ini bersifat permanen. Sebelum Anda memilih bucket, pastikan Anda berada di organisasi Anthropic yang workspace-nya akan menggunakan bucket ini.
</Warning>

Di halaman [Data retention](https://platform.claude.com/settings/privacy) workspace, pilih kartu **Enterprise Frontier Safeguards**, lalu pilih bucket Anda di bawah **Sealed Safety Data storage**. <Where cloud="aws" label="Claude Platform on AWS">Pilih juga bucket Anda di bawah **Safety Case and Transcript storage**.</Where> <Where cloud="claude" label="Claude Platform">**Safety Case and Transcript storage** bersifat opsional. Tanpa bucket di bawah pengaturan tersebut, tim Anda hanya mendapatkan Safety Cases jika organisasi Anda memiliki [akses ke Safety Cases API](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#get-access). Anda dapat memilih bucket Anda di bawahnya jika bucket Anda [dapat menerima transkrip dan Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket).</Where>

Lalu, simpan workspace. Jika Anthropic menolak bucket Anda saat Anda menyimpan, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting).

Tindakan menyimpan akan menonaktifkan Anthropic Human Review, yang [dapat memakan waktu hingga 2 jam](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Untuk memeriksa bahwa penyimpanan Anda berhasil, pastikan **Case review by** menunjukkan **My organization** di panel samping workspace di halaman [Workspaces](https://platform.claude.com/settings/workspaces). Jika **Case review by** tidak menunjukkan **My organization**, buka workspace tersebut di halaman [Data retention](https://platform.claude.com/settings/privacy) dan klik **Save** lagi, meskipun Anda tidak mengubah apa pun. Jika Anda tidak dapat melakukannya, atau **Case review by** masih tidak menunjukkan **My organization**, hubungi tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan.

</Where>

<Where method="api" label="Admin API">

### Lampirkan bucket Anda ke workspace

Lampirkan bucket Anda ke setiap workspace yang seharusnya menggunakannya. Melampirkan memberi tahu Anthropic untuk menyimpan data keselamatan tersegel workspace tersebut di bucket Anda.

Di organisasi yang memiliki pengaturan Legacy Zero Data Retention (ZDR), jangan lampirkan bucket Anda ke workspace yang retensi datanya nonaktif. Sebagai gantinya, [buat workspace dengan bucket Anda yang sudah terlampir](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-create-workspace-attached).

<Warning>
  Sebelum Anda mengirim permintaan ini, pastikan kunci atau token Anda milik organisasi yang workspace-nya akan menggunakan bucket ini. Permintaan attach pertama yang berhasil [mengikat bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#before-you-begin), namanya, kunci KMS-nya, dan peran IAM-nya ke organisasi tersebut. Anggap hal ini permanen.
</Warning>

Untuk melampirkan bucket Anda, perbarui workspace dengan `POST /v1/organizations/workspaces/{workspace_id}` dan atur `inference_data_privacy.safeguards_storage` ke tipe `external` dengan ID bucket Anda. Field ini adalah **Sealed Safety Data storage** di Claude Console.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: efs-2026-10-01" \
    -H "content-type: application/json" \
    -d '{
      "inference_data_privacy": {
        "safeguards_storage": {
          "type": "external",
          "external_storage_id": "estrg_01SDCCSbTxrXDpWc1phhtcfK"
        },
        "human_review": {
          "type": "disabled"
        }
      }
    }'
  ```

  ```bash CLI
  ant beta:organization:workspaces update \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --beta efs-2026-10-01 <<YAML
  inference_data_privacy:
    safeguards_storage:
      type: external
      external_storage_id: estrg_01SDCCSbTxrXDpWc1phhtcfK
    human_review:
      type: disabled
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.workspaces.update(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      inference_data_privacy={
          "safeguards_storage": {
              "type": "external",
              "external_storage_id": "estrg_01SDCCSbTxrXDpWc1phhtcfK",
          },
          "human_review": {"type": "disabled"},
      },
      betas=["efs-2026-10-01"],
  )

  privacy = workspace.inference_data_privacy
  if privacy and privacy.safeguards_storage:
      print(f"safeguards_storage: {privacy.safeguards_storage.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.workspaces.update(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    {
      inference_data_privacy: {
        safeguards_storage: {
          type: "external",
          external_storage_id: "estrg_01SDCCSbTxrXDpWc1phhtcfK"
        },
        human_review: { type: "disabled" }
      },
      betas: ["efs-2026-10-01"]
    }
  );

  const type = workspace.inference_data_privacy?.safeguards_storage?.type;
  console.log(`safeguards_storage: ${type}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Workspaces;

  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.Workspaces.Update(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new()
      {
          InferenceDataPrivacy = new()
          {
              SafeguardsStorage = new BetaExternalStorageMemberParam
              {
                  ExternalStorageID = "estrg_01SDCCSbTxrXDpWc1phhtcfK",
              },
              HumanReview = new() { Type = BetaAnthropicHumanReviewParamType.Disabled },
          },
          Betas = ["efs-2026-10-01"],
      }
  );

  var type = workspace.InferenceDataPrivacy?.SafeguardsStorage?.Type.Raw();
  Console.WriteLine($"safeguards_storage: {type}");
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Beta.Organization.Workspaces.Update(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.BetaOrganizationWorkspaceUpdateParams{
  		InferenceDataPrivacy: anthropic.BetaInferenceDataPrivacyUpdateParam{
  			SafeguardsStorage: anthropic.BetaStorageMemberParamOfExternal("estrg_01SDCCSbTxrXDpWc1phhtcfK"),
  			HumanReview: anthropic.BetaAnthropicHumanReviewParam{
  				Type: anthropic.BetaAnthropicHumanReviewParamTypeDisabled,
  			},
  		},
  		Betas: []anthropic.AnthropicBeta{"efs-2026-10-01"},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("safeguards_storage: %s\n", workspace.InferenceDataPrivacy.SafeguardsStorage.Type)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.BetaAnthropicHumanReviewParam;
  import com.anthropic.models.beta.organization.workspaces.BetaInferenceDataPrivacyUpdateParam;
  import com.anthropic.models.beta.organization.workspaces.WorkspaceUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceUpdateParams.builder()
          .inferenceDataPrivacy(BetaInferenceDataPrivacyUpdateParam.builder()
              .externalSafeguardsStorage("estrg_01SDCCSbTxrXDpWc1phhtcfK")
              .humanReview(BetaAnthropicHumanReviewParam.builder()
                  .type(BetaAnthropicHumanReviewParam.Type.DISABLED)
                  .build())
              .build())
          .addBeta("efs-2026-10-01")
          .build();
      var workspace = client.beta().organization().workspaces()
          .update("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      IO.println("safeguards_storage: " + workspace.inferenceDataPrivacy()
          .flatMap(privacy -> privacy.safeguardsStorage())
          .map(storage -> storage.type().asString())
          .orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->workspaces->update(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      inferenceDataPrivacy: [
          'safeguardsStorage' => [
              'type' => 'external',
              'externalStorageID' => 'estrg_01SDCCSbTxrXDpWc1phhtcfK',
          ],
          'humanReview' => ['type' => 'disabled'],
      ],
      betas: ['efs-2026-10-01'],
  );

  echo "safeguards_storage: {$workspace->inferenceDataPrivacy?->safeguardsStorage?->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace = client.beta.organization.workspaces.update(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    inference_data_privacy: {
      safeguards_storage: {
        type: :external,
        external_storage_id: "estrg_01SDCCSbTxrXDpWc1phhtcfK"
      },
      human_review: {
        type: :disabled
      }
    },
    betas: ["efs-2026-10-01"]
  )

  puts "safeguards_storage: #{workspace.inference_data_privacy&.safeguards_storage&.type}"
  ```
</CodeGroup>

Jika permintaan berhasil, status bucket Anda menjadi `active`. Contoh permintaan juga mengatur `inference_data_privacy.human_review` ke tipe `disabled`, karena di Admin API pelampiran saja tidak menonaktifkan [Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review). Dengan Enterprise Frontier Safeguards (EFS), Anthropic Human Review selalu nonaktif dan tim Anda sendiri yang meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) workspace tersebut.

Pelampiran [tidak langsung berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Sampai pelampiran berlaku, data keselamatan tersegel dari workspace yang tidak memiliki [bucket data keselamatan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) mungkin masuk ke penyimpanan yang dikelola Anthropic. Sampai 10 menit setelah objek baru pertama masuk, kirim hanya permintaan uji tanpa data sensitif, karena server Anthropic tidak menerapkan perubahan tersebut secara bersamaan. Untuk memastikan bahwa pelampiran telah berlaku, perhatikan objek baru yang masuk di bawah `slab/` atau `safeguards-data/slab/` di bucket Anda. Baik status `active` maupun membaca kembali workspace tidak menunjukkan bahwa pelampiran telah berlaku. Jika workspace lain sudah mengirim data ke bucket ini, objek baru juga tidak menunjukkannya, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan.

Untuk memindahkan workspace ke bucket lain, ikuti [Ubah bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-your-bucket). Pada langkah 1, [daftarkan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-register) dan [aktifkan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-activate) bucket baru Anda. Pada langkah 2, kirim permintaan attach dengan ID bucket baru sebagai gantinya. Jika `transcripts_storage` menyebut bucket lama Anda, atur field tersebut ke ID bucket baru dalam permintaan yang sama. Jangan [lepaskan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-stop) terlebih dahulu, atau data keselamatan tersegel yang baru dapat masuk ke penyimpanan yang dikelola Anthropic.

Permintaan attach dapat mengembalikan error seperti berikut:

* `human_review_on_with_external_storage`: Anthropic dapat mengembalikan ini jika Anda tidak menyertakan `human_review` saat Anthropic Human Review aktif.
* `approval_required`: Organisasi Anda tidak memiliki persetujuan Anthropic untuk menonaktifkan Anthropic Human Review. Permintaan tidak mengubah apa pun.
* `workspace_policy_violation`: Kebijakan organisasi Anda menolak permintaan, misalnya karena kebijakan tersebut mewajibkan Anthropic Human Review.
* `transcripts_storage_required`: Tidak ada yang berubah. [Atur juga `transcripts_storage`](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-attach-transcripts) dalam permintaan yang sama.

Untuk informasi lebih lanjut tentang error attach, lihat [Pemecahan masalah di Mengelola penyimpanan milik pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#api-troubleshooting).

#### Kirim transkrip dan Safety Cases ke bucket

Untuk mengirim transkrip dan Safety Cases ke bucket Anda, atur `inference_data_privacy.transcripts_storage` ke tipe `external` dengan ID yang sama seperti `safeguards_storage`. Field ini adalah **Safety Case and Transcript storage** di Claude Console. Anda dapat mengatur kedua field penyimpanan dalam permintaan yang sama. Jika pemeriksaan gagal pada salah satu field, Anthropic menghentikan seluruh permintaan. [Transkrip dan Safety Cases di bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#case-and-transcript-bucket) menjelaskan bucket mana yang dapat menerimanya.

#### Buat workspace dengan bucket Anda yang sudah terlampir

Untuk membuat workspace dengan bucket Anda yang sudah terlampir, kirim pengaturan `inference_data_privacy` yang sama ke `POST /v1/organizations/workspaces`. Pelampiran tetap [tidak langsung berlaku](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#how-long-changes-take). Di organisasi yang memiliki pengaturan Legacy ZDR, retensi data dapat nonaktif untuk workspace baru. Jika nonaktif, tidak ada apa pun yang masuk ke bucket Anda sampai Anda mengaktifkannya. Untuk mengaktifkannya, buka halaman [Retensi data](https://platform.claude.com/settings/privacy) workspace tersebut di Claude Console, klik **Finish switching**, lalu klik **Accept**. Workspace mulai menyimpan data keselamatan tersegel saat **Accept**, jadi beri waktu agar pelampiran berlaku terlebih dahulu. Kirim hanya permintaan uji sampai 10 menit setelah objek baru pertama masuk.

Jika permintaan pembuatan mengembalikan `approval_required`, `grant_required`, `authorization_check_unavailable`, `human_review_on_with_external_storage`, atau `transcripts_storage_required`, workspace tidak dibuat.

Persetujuan untuk workspace yang dipilih tidak dapat mencakup workspace yang belum ada. Jika permintaan pembuatan mengembalikan `grant_required` di organisasi yang memiliki pengaturan Legacy ZDR, jangan buat workspace tanpa bucket Anda. Hubungi tim akun Anthropic Anda. Di organisasi lainnya, buat workspace tanpa `inference_data_privacy`, minta tim akun Anthropic Anda agar workspace tersebut disetujui, lalu lampirkan bucket Anda seperti yang dijelaskan di [Lampirkan bucket Anda ke workspace](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#api-attach).

</Where>

<Where cloud="claude" label="Claude Platform">

Untuk langkah-langkah lengkapnya, termasuk pengaturan lain pada workspace tersebut, lihat [Siapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#turn-on-efs-for-a-workspace).

</Where>

<Where cloud="aws" label="Claude Platform on AWS">

Untuk langkah-langkah lengkapnya, termasuk pengaturan lain pada workspace tersebut, lihat [Siapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws#turn-on-efs-for-a-workspace).

</Where>

Anda dapat menggunakan [kebijakan untuk workspace baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#set-organization-defaults) untuk mewajibkan penyimpanan milik pelanggan bagi setiap workspace baru yang menyimpan data keselamatan tersegel.

### Pastikan perubahan telah berlaku

Sebelum workspace menangani lalu lintas yang perlu Anda simpan di bucket Anda, kirim permintaan uji tanpa data sensitif sampai objek baru masuk di bawah `slab/` atau `safeguards-data/slab/`. Lalu, tunggu 10 menit lagi, karena server Anthropic tidak menerapkan perubahan tersebut secara bersamaan. Hingga waktu tunggu tersebut berakhir, kirim hanya permintaan uji, karena data keselamatan tersegel Anda mungkin dikirim ke penyimpanan yang dikelola Anthropic. Jika workspace lain sudah mengirim data ke bucket ini, objek baru tidak menunjukkan bahwa perubahan ini telah berlaku, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas sungguhan. Jika tidak ada objek baru yang muncul di bawah `slab/` atau `safeguards-data/slab/` 4 jam setelah Anda melakukan perubahan, hubungi tim akun Anthropic Anda.

Perubahan tidak langsung berlaku. Selama Anda menunggu, hal-hal berikut merupakan hal yang wajar, bahkan saat penyiapan berhasil:

* **Waktu tunggu.** Saat workspace baru, atau workspace yang menggunakan penyimpanan yang dikelola Anthropic, mulai menggunakan bucket Anda, perubahan biasanya berlaku dalam 10 menit, tetapi dapat memakan waktu lebih lama.
* **Tidak ada objek baru.** Hingga perubahan berlaku, data keselamatan tersegel Anda dari permintaan workspace tersebut mungkin dikirim ke penyimpanan yang dikelola Anthropic, dan objek baru mungkin belum muncul di bawah `slab/` atau `safeguards-data/slab/`.
* **Status Active tanpa objek.** Bucket Anda dapat ditampilkan sebagai **Active** di **Storage destinations** sebelum perubahan berlaku, jadi **Active** tidak berarti objek sudah masuk.
* **Anthropic Human Review.** Jika perubahan juga menonaktifkan Anthropic Human Review, hal itu dapat memakan waktu hingga 2 jam. Hingga saat itu, tim peninjau Anthropic mungkin masih meninjau data workspace tersebut.

Jika nanti Anda memindahkan workspace ke bucket lain atau keluar dari EFS, perpindahan tersebut juga tidak langsung berlaku. Setelah perpindahan antara dua bucket Amazon S3 dalam satu kali simpan atau satu permintaan, data keselamatan tersegel yang baru masih dapat masuk ke bucket lama Anda untuk sementara waktu. Perpindahan tersebut tidak dengan sendirinya mengirim data baru ke penyimpanan yang dikelola Anthropic. Simpan bucket lama Anda, dan akses Anthropic ke bucket tersebut, seperti yang dijelaskan di [Ubah atau berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-or-stop-using-your-bucket).

## Transkrip dan Safety Cases di bucket Anda

Untuk menerima transkrip dan Safety Cases sebuah workspace di bucket Anda, pastikan bucket tersebut dapat menerimanya, lalu pilih bucket tersebut untuk workspace. Transkrip dan Safety Cases dikirim ke bucket yang sama, dan Anda tidak dapat memilih salah satunya tanpa yang lain.

<Where cloud="aws" label="Claude Platform on AWS">

[Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws) berisi langkah-langkah untuk **Safety Case and Transcript storage**.

</Where>

<Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">

[Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#turn-on-efs-for-a-workspace) berisi langkah-langkah untuk **Safety Case and Transcript storage**.

</Where>

<Where cloud="claude" label="Claude Platform">

Untuk mengetahui apakah sebuah bucket dapat menerima transkrip dan Safety Cases, lihat nama peran-perannya:

* **Nama yang diawali `anthropic-efs-<RoleDigest>-`:** Bucket dapat menerima transkrip dan Safety Cases.
* **Nama tetap, seperti `anthropic-efs-ingest`:** Bucket tidak dapat menerimanya. Untuk menerimanya, [ganti ke bucket baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-your-bucket) dan pilih bucket tersebut di bawah kedua pengaturan penyimpanan.

Jika bucket dapat menerimanya, buka halaman [Data retention](https://platform.claude.com/settings/privacy) workspace. Jika halaman tersebut menampilkan **Safety Case and Transcript storage**, pilih bucket yang sama di bawah pengaturan tersebut dan di bawah **Sealed Safety Data storage**. Jika Anda memilih bucket yang berbeda, bucket tersebut mungkin tidak menerima transkrip dan Safety Cases, meskipun penyimpanan berhasil. Saat Anda menyimpan, Anthropic memeriksa bahwa bucket telah disiapkan untuk transkrip dan Safety Cases. Jika Anthropic menolak bucket tersebut, seluruh penyimpanan akan berhenti. Untuk memperbaikinya, lihat [Pemecahan masalah](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#troubleshooting). Jika halaman tidak menampilkan **Safety Case and Transcript storage** saat kartu **Enterprise Frontier Safeguards** dipilih, hubungi tim akun Anthropic Anda.

Setiap jenis file memiliki prefiksnya sendiri:

| Prefiks | Isinya | Siapa yang menulisnya |
| ----- | ----- | ----- |
| `transcripts/` | Transkrip | Anthropic |
| `review-cases/`, `review-summaries/`, dan `review-notices/` | File Safety Case | Anthropic |
| `review-responses/` | Respons tim Anda | Tim Anda. Tidak ada peran Anthropic yang dapat menulis, mengubah, atau menghapusnya. |

Aturan siklus hidup file penyiapan membuat semua file ini kedaluwarsa setelah [jumlah hari yang ditetapkan untuk masing-masing](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket).

</Where>

### Berikan tim Anda akses ke bucket

Untuk memberi tim Anda akses, tambahkan izin berikut ke kebijakan IAM pengguna Anda sendiri. Tidak ada yang dibuat oleh file penyiapan yang perlu diubah.

* **Untuk membaca transkrip dan Safety Cases:** izinkan `s3:GetObject` di bawah `transcripts/` dan prefiks review (`review-cases/`, `review-responses/`, `review-summaries/`, dan `review-notices/`), `s3:ListBucket` pada bucket dengan kondisi `s3:prefix` yang membatasinya ke prefiks-prefiks tersebut, dan `kms:Decrypt` pada kunci. Jangan berikan akses S3 ke prefiks lain.
* **Untuk membaca versi sebelumnya dari sebuah file:** izinkan juga `s3:GetObjectVersion` dan `s3:ListBucketVersions`, dengan batasan yang sama.
* **Untuk menulis respons di bawah `review-responses/`:** izinkan juga `s3:PutObject` pada `review-responses/*` dan `kms:GenerateDataKey` pada kunci. Tulis respons dengan enkripsi default bucket, karena Anthropic tidak dapat membaca respons yang dienkripsi dengan kunci KMS lain.

Untuk proses peninjauan, lihat [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases).

## Pemecahan masalah

<AccordionGroup>
  <Accordion title="Deploy CloudFormation gagal">
    Jika deploy langsung berhenti dengan error tentang `Fn::Select`, nama stack dan `RoleDigest` tidak cocok. Tidak ada yang berubah, jadi jalankan perintah dari dialog persis seperti yang ditampilkan. Jika Anda sedang memperbarui stack dengan nama lain, biarkan stack tersebut apa adanya dan hubungi tim akun Anthropic Anda.

    Untuk menemukan penyebab kegagalan lainnya, jalankan dua perintah hanya-baca yang ditampilkan langkah **Create in AWS** di bawah perintah deploy, atau buka tab **Events** stack di konsol AWS CloudFormation.

    Jika nama bucket sudah dipakai, hapus stack yang gagal dan tujuan penyimpanan, lalu hubungkan tujuan penyimpanan baru dengan nama bucket lain. Jika penyebabnya masih belum jelas, kirim seluruh output ke tim akun Anthropic Anda. Jangan tambahkan `--debug` ke perintah apa pun, karena output debug dapat menyertakan token sesi AWS Anda.
  </Accordion>

  <Accordion title="Apply Terraform gagal">
    Jika apply pertama gagal di tengah jalan, jalankan apply yang sama lagi untuk membuat apa yang belum ada. Jika apply gagal karena akun AWS lain sudah memiliki bucket dengan nama yang Anda masukkan, Terraform tidak membuat apa pun, dan menjalankan apply lagi tidak membantu. Sebagai gantinya, hapus tujuan penyimpanan, hubungkan tujuan penyimpanan baru dengan nama bucket lain, dan jalankan apply dengan perintah yang diberikan dialog untuk tujuan penyimpanan baru tersebut. Jika akun AWS Anda sendiri memiliki bucket tersebut dari apply sebelumnya, pertahankan namanya, dan pulihkan state folder atau jalankan `terraform import`.
  </Accordion>

  <Accordion title="Test setup menyatakan bahwa Anthropic tidak dapat menjalankan pengujian">
    Jalankan pengujian lagi dalam beberapa menit. Jika pengujian terus menampilkan pesan ini, beri tahu tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Test setup menyatakan bahwa Anthropic tidak dapat mengambil alih peran verify">
    Dengan masalah ini, **Test setup** dapat menampilkan beberapa pemeriksaan yang gagal. Pesan pemeriksaan gagal yang pertama diawali dengan “Anthropic could not assume the verify role”, dan pesan lainnya menyatakan bahwa sebuah peran “must have the setup template’s trust policy”. Hal ini dapat terjadi bahkan saat Anda membuat bucket dan peran persis seperti yang dijelaskan.

    Pertama, lihat nama peran IAM Anda. Jika bucket ini belum pernah lolos **Test setup** dan perannya memiliki nama tetap, seperti `anthropic-efs-ingest`, penyiapan Anda berasal dari file penyiapan lama. Anthropic tidak menerima bucket baru yang perannya memiliki nama tetap, dan mengubah peran tersebut tidak membuat pengujian lolos. Sebagai gantinya, lakukan hal berikut:

    1. Hapus tujuan penyimpanan.
    2. [Mulai lagi dengan **Connect storage**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles), dengan nama bucket baru, dan gunakan file atau nilai yang diberikan dialog. Dengan Terraform, gunakan folder baru, dan jangan jalankan apply di folder lama.
    3. Setelahnya, jika tidak ada bucket lain yang menggunakan peran lama tersebut, Anda dapat menghapusnya, seperti yang dijelaskan langkah **Remove Anthropic’s access** di [Berhenti menggunakan bucket Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#stop-using-your-bucket). Lalu, Anda dapat menghapus bucket yang tidak digunakan.

    Jika peran Anda tidak memiliki nama tetap, atau bucket ini pernah lolos **Test setup** sebelumnya, lakukan pemeriksaan berikut:

    1. Pastikan penyiapan Anda di AWS telah selesai dengan file atau nilai dari dialog. Pastikan ID akun AWS dan region yang Anda masukkan adalah akun dan region tempat Anda melakukan deploy. Untuk mengubah salah satunya, hapus tujuan penyimpanan dan hubungkan yang baru. Salinan file dari tempat lain dapat membuat peran dengan nama lain, yang tidak dapat ditemukan oleh pengujian. Jika Anda menggunakan salinan seperti itu, hapus tujuan penyimpanan, hubungkan yang baru dengan nama bucket baru, dan gunakan file yang diberikan dialog.

    2. Pastikan Anda menjalankan perintah dari dialog persis seperti yang ditampilkan, agar external ID dan nama peran benar. Apa yang harus dilakukan bergantung pada apa yang Anda ubah:

       * **ID organisasi:** Jalankan lagi perintah dari dialog. Jika Terraform kemudian berhenti karena ID organisasi berubah, pesannya menyebutkan apa yang perlu ditambahkan ke perintah. Dengan CloudFormation, jika nama stack Anda berbeda dari nama dalam perintah dialog, ikuti item berikutnya sebagai gantinya.

       * **`RoleDigest`, dengan CloudFormation:** Buka stack yang deploy-nya berhasil di konsol AWS CloudFormation. Periksa **Created time** di tab **Stack info** dan `BucketName` di tab **Outputs**. Apa yang harus dilakukan bergantung pada apa yang ditampilkan:

         * **Created time adalah saat Anda pertama kali melakukan deploy untuk bucket ini:** Hapus stack, yang akan meninggalkan bucket dan kunci KMS-nya. Hapus bucket yang tidak digunakan itu, serta stack gagal mana pun yang memiliki nama dalam perintah dialog. Lalu, jalankan perintah dari dialog dengan file dari dialog.
         * **Stack lebih lama dari itu, dan menampilkan bucket lain:** Biarkan stack tersebut, dan jalankan perintah dari dialog untuk bucket ini.
         * **Stack lebih lama dari itu, dan menampilkan bucket ini:** Deploy Anda mengubah stack milik bucket lain. Jangan jalankan apa pun lagi, dan segera hubungi tim akun Anthropic Anda.

       * **Nama bucket:** Beri tahu tim akun Anthropic Anda.

    3. Jika dua pemeriksaan pertama tidak menemukan masalah, periksa apakah [kebijakan organisasi AWS memblokir Anthropic](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#if-an-aws-organization-policy-blocks-anthropic). Satu kebijakan yang menolak Anthropic dapat menyebabkan semua pemeriksaan gagal. Jika kebijakan adalah penyebabnya, file penyiapan tidak perlu diubah.

    Setelah perbaikan, klik **Test again**. Jika Anda menutup dialog, klik **Finish setup** di **Storage destinations**, lalu klik **Test setup**. Jika pengujian masih gagal, beri tahu tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Test setup menyebutkan External Storage organisasi lain">
    Bagian ini berlaku saat **Test setup** gagal dengan satu pemeriksaan yang pesannya diawali “Another organization’s External Storage”. Pemeriksaan ini gagal saat organisasi Anthropic lain telah menggunakan sebagian penyiapan ini, atau saat nama bucket sedang digunakan di akun AWS yang berbeda. Pemeriksaan ini juga dapat menghitung tujuan penyimpanan milik organisasi yang telah dihapus.

    Jika organisasi lain telah menggunakan akun AWS ini, Anda dapat tetap menggunakan akun tersebut. Pertama, pastikan Anda men-deploy file yang diberikan dialog untuk bucket ini, lalu uji lagi.

    Jika pengujian masih gagal, atau tidak ada organisasi lain yang telah menggunakan akun AWS ini, gunakan nama bucket baru, dengan kunci dan peran tersendiri. Mulai lagi dengan **Connect storage**, karena **Finish setup** mempertahankan akun AWS dan nama bucket yang Anda masukkan. Jika bucket baru gagal dengan cara yang sama, beri tahu tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Anthropic menolak bucket Anda saat Anda menyimpan workspace">
    Saat pertama kali Anda memilih bucket untuk sebuah workspace dan menyimpannya, Anthropic mengulangi pemeriksaan dari **Test setup**. Jika Anthropic menolak bucket Anda, salah satu pemeriksaan tersebut mungkin gagal, karena salah satu dari dua alasan:

    * Sesuatu telah berubah sejak pengujian lolos: pengaturan bucket, kunci KMS bucket, peran IAM, atau kebijakan organisasi AWS.
    * Organisasi Anthropic lain telah menggunakan sebagian penyiapan ini atau, jika peran Anda memiliki nama tetap, akun AWS ini.

    Claude Console mencantumkan pemeriksaan yang gagal dalam sebuah dialog. Jika Anda memilih bucket di bawah **Safety Case and Transcript storage**, tidak ada pemeriksaan yang dicantumkan, dan pesan error tidak menyebutkan Human Review, lanjutkan ke masalah berikutnya, “Anthropic menolak bucket Anda di bawah Safety Case and Transcript storage”.

    Jika satu-satunya pemeriksaan yang gagal diawali “Another organization’s External Storage”, apa yang harus dilakukan bergantung pada pengaturan tempat pesan error berada:

    * **Safety Case and Transcript storage:** Hubungi tim akun Anthropic Anda.
    * **Sealed Safety Data storage:** Gunakan nama bucket baru, dengan kunci dan peran tersendiri. Lalu, [mulai lagi dengan **Connect storage**](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-bucket-and-roles).

    Untuk pemeriksaan gagal lainnya, perbaiki penyebabnya, lalu simpan workspace lagi. Jika Anda tidak dapat mengetahui penyebabnya, hubungi tim akun Anthropic Anda. Jika pesan error berada di bawah **Safety Case and Transcript storage**, ikuti masalah berikutnya, “Anthropic menolak bucket Anda di bawah Safety Case and Transcript storage”.

    Jika pesan error menyatakan bahwa Enterprise Frontier Safeguards memerlukan Anthropic Human Review dinonaktifkan, tindakan menyimpan tersebut tidak mengubah apa pun. Hal yang sama berlaku jika pesan error menyatakan bahwa Anthropic tidak menawarkan Human Review untuk data di penyimpanan Anda sendiri. Organisasi Anda memerlukan persetujuan Anthropic untuk menonaktifkan Anthropic Human Review, dan kebijakan organisasi Anda tidak boleh mewajibkan Anthropic Human Review. Jika organisasi Anda belum memiliki persetujuan tersebut, mintalah Organization Admin untuk [menyetujui ketentuan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#get-access). Jika ketentuan tersebut tidak ditawarkan, tanyakan kepada tim akun Anthropic Anda. Jika kebijakan mewajibkan Anthropic Human Review, mintalah admin untuk mengubah kebijakan tersebut. Di bawah kebijakan tersebut, kartu **Enterprise Frontier Safeguards** mungkin menampilkan **Ineligible**. Jika tidak satu pun berlaku, muat ulang halaman dan simpan lagi. Jika error muncul kembali, hubungi tim akun Anthropic Anda.
  </Accordion>

  <Accordion title="Anthropic menolak bucket Anda di bawah Safety Case and Transcript storage">
    Jika peran bucket Anda memiliki nama tetap, seperti `anthropic-efs-ingest`, bucket tersebut tidak dapat menerima transkrip dan Safety Cases, dan mencoba lagi tidak membantu. <Where cloud="aws" label="Claude Platform on AWS">Tanyakan kepada tim akun Anthropic Anda sebelum Anda melakukan hal lain.</Where> Jangan gunakan [file penyiapan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#get-the-setup-file) untuk memperbarui penyiapan bucket tersebut. Untuk menerima transkrip dan Safety Cases, [ganti ke bucket baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage#change-your-bucket) dan pilih bucket tersebut di bawah **Sealed Safety Data storage** dan **Safety Case and Transcript storage** sebelum Anda menyimpan. Jika dialog memberi Anda file dengan nama peran tetap, jangan jalankan file tersebut, dan hubungi tim akun Anthropic Anda.

    Jika peran bucket Anda tidak memiliki nama tetap, perbaiki apa yang dicantumkan pemeriksaan yang gagal, lalu simpan workspace lagi. Jika satu-satunya pemeriksaan yang gagal diawali “Another organization’s External Storage”, hubungi tim akun Anthropic Anda. Hubungi juga tim akun Anthropic Anda jika pesan menyatakan bahwa bucket tidak dapat menyimpan Cases dan transkrip, atau bahwa penyimpanan belum dapat dilampirkan untuk transkrip.

    Jika pesan error menyatakan bahwa Anthropic tidak dapat memeriksa penyiapan bucket, atau hanya menyatakan bahwa pengaturan workspace gagal diperbarui, pastikan bucket Anda masih dipilih di bawah kedua pengaturan penyimpanan, lalu simpan lagi. Jika error muncul kembali, hubungi tim akun Anthropic Anda.

    <Where cloud="claude" label="Claude Platform">

    Untuk menyimpan hanya **Sealed Safety Data storage**, pilih **Not copied to your storage** di bawah **Safety Case and Transcript storage** jika halaman menawarkan pilihan tersebut. Jika tidak, hubungi tim akun Anthropic Anda.

    </Where>
  </Accordion>
</AccordionGroup>

## Referensi template

Tinjau template CloudFormation atau file Terraform yang diberikan langkah **Create in AWS** sebelum Anda menjalankannya. File tersebut berisi kebijakan lengkap setiap peran, dengan setiap tindakan dan kondisi.

Untuk mengubah kapan file Safety Case dan respons tim Anda kedaluwarsa, atur `ReviewExpiryDays` (di Terraform, `review_expiry_days`), satu-satunya nilai yang dapat Anda atur sendiri. Ini adalah jumlah hari hingga file-file tersebut kedaluwarsa, hingga 9.999. Default-nya adalah 2.555, sekitar 7 tahun. Aturan berikut berlaku, jadi bacalah sebelum Anda mengubahnya:

* Ringkasan kedaluwarsa setelah 28 hari jika itu lebih cepat.
* File kedaluwarsa meskipun peninjauannya belum selesai, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda menetapkan angka yang rendah.
* Angka baru juga berlaku untuk file yang sudah ada di bucket Anda, sehingga angka yang lebih rendah dapat membuat file lama kedaluwarsa dan menghapus versi sebelumnya.
* File yang kedaluwarsa, diganti, atau dihapus tetap tersimpan sebagai versi sebelumnya selama jumlah hari yang sama lagi, atau paling lama 3 hari untuk ringkasan. Untuk menghapus file seketika, hapus semua versinya.
* Dengan Terraform, teruskan `review_expiry_days` pada setiap apply. Apply tanpa nilai tersebut akan kembali ke default.

<AccordionGroup>
  <Accordion title="Apa yang dapat dilakukan peran dengan kunci KMS bucket Anda">
    Setiap izin KMS dalam [tabel peran](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#create-the-roles) hanya berlaku untuk kunci KMS yang dibuat oleh file penyiapan untuk bucket Anda. `kms:GenerateDataKey` dan `kms:Decrypt` juga membawa kondisi `kms:ViaService` untuk Amazon S3 di region bucket Anda, sehingga sebuah peran dapat mengenkripsi dan mendekripsi dengan kunci tersebut hanya melalui Amazon S3, bukan dengan memanggil AWS KMS secara langsung.
  </Accordion>

  <Accordion title="Apa yang harus diizinkan oleh pengecualian kebijakan organisasi AWS yang lebih sempit">
    Pengecualian yang lebih sempit harus mengizinkan dua panggilan, `sts:AssumeRole` dan `sts:SetSourceIdentity`. Panggilan tersebut berasal dari peran IAM di akun AWS Anthropic yang namanya diawali `anthropic-storage-broker-` atau `anthropic-review-broker-`. Panggilan tersebut hanya ditujukan ke peran milik penyiapan ini, di akun AWS yang menampung bucket Anda, dan file penyiapan tidak mengizinkan hal lain bagi pemanggil Anthropic. Pekerjaan Anthropic di Amazon S3 dan AWS KMS kemudian berjalan sebagai peran milik penyiapan ini, yang merupakan principal di akun AWS Anda sendiri. Pengecualian yang mengizinkan kedua panggilan tersebut seharusnya sudah cukup, tetapi sejauh ini Anthropic hanya melihat **Test setup** lolos dengan pengecualian untuk seluruh akun. **Test setup** tidak pernah mencoba peran `review`, sehingga pengujian yang lolos tidak menunjukkan bahwa pengecualian Anda mencakup `anthropic-review-broker-`.
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Mengelola penyimpanan milik pelanggan" icon="database" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage-manage">
    Periksa status bucket Anda, perbaiki bucket yang berhenti berfungsi, dan ubah atau berhenti menggunakannya.
  </Card>

  <Where cloud="claude" label="Claude Platform">

  <Card title="Menyiapkan Enterprise Frontier Safeguards di Claude Platform" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console">
    Pilih tujuan penyimpanan Anda untuk workspace, lalu periksa penyiapan Anda.
  </Card>

  </Where>

  <Where cloud="aws" label="Claude Platform on AWS">

  <Card title="Menyiapkan Enterprise Frontier Safeguards di Claude Platform on AWS" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-platform-on-aws">
    Pilih tujuan penyimpanan Anda untuk workspace, lalu periksa penyiapan Anda.
  </Card>

  </Where>

  <Card title="Menggunakan kunci yang dikelola pelanggan" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys">
    Enkripsi data Anda menggunakan kunci yang Anda simpan di layanan manajemen kunci Anda sendiri.
  </Card>
</CardGroup>

</Where>

<Where bucket="gcs" label="Google Cloud Storage">

## Menyiapkan penyimpanan milik pelanggan di Google Cloud Storage

Bucket Google Cloud Storage di akun cloud Anda sendiri menyimpan [data keselamatan tersegel](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-owned-storage#what-is-stored) ruang kerja. Untuk menyiapkan bucket, buat bucket dengan Terraform dan hubungkan bucket tersebut di Claude Console. Tim Anda tidak dapat membaca data keselamatan tersegel. Sebelum Anda memulai, baca [Gunakan bucket Cloud Storage Anda di ruang kerja](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace).

Penyiapan terdiri dari tiga bagian:

1. [Periksa kebijakan organisasi Google Cloud Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#check-your-policies).
2. [Buat dan uji bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket).
3. [Gunakan bucket Cloud Storage Anda di ruang kerja](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-use-your-bucket-in-a-workspace).

## Sebelum Anda memulai

Pastikan Anda memiliki hal-hal berikut:

* **[Akses ke Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console).**

  <Where cloud="claude" label="Claude Platform">Jika organisasi Anda memilikinya, halaman [Programs](https://platform.claude.com/settings/programs) di Claude Console menampilkannya dengan tombol **Configure**.</Where>
* **Cara untuk menghubungkan bucket Anda.** Di Claude Platform, pastikan Anda dapat memilih **Google Cloud Storage** di bawah **Connect storage**. **Connect storage** ada di halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console, dengan **Organisasi** dipilih di bagian atas. Jika Anda tidak dapat memilih **Google Cloud Storage**, hubungi tim akun Anthropic Anda sebelum Anda memulai bagian 1.
* **Organization Admin** di Claude Console, yang mendapatkan file penyiapan dan menghubungkan bucket Anda. <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">Di Claude Models on Google Cloud (Anthropic managed), itu adalah seseorang dengan [`roles/claude.admin`](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#using-the-claude-console) pada proyek Google Cloud yang organisasinya akan menggunakan bucket ini.</Where>
* **Proyek Google Cloud** tempat tidak ada otomatisasi yang menghapus peran kustom, pemberian izin, atau bucket.
* **Alat:** [Terraform 1.9 atau yang lebih baru](https://developer.hashicorp.com/terraform/install) dan [Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk).
* **Peran pada proyek:** Owner proyek atau semua dari `roles/storage.admin`, `roles/cloudkms.admin`, `roles/iam.roleAdmin`, dan `roles/serviceusage.serviceUsageAdmin`.
* **Peran untuk perubahan kebijakan:** `roles/orgpolicy.policyAdmin` pada organisasi Google Cloud. Owner proyek tidak mencakupnya.

## 1. Periksa kebijakan organisasi Google Cloud Anda

Pada langkah ini, Anda memastikan bahwa kebijakan organisasi Google Cloud Anda mengizinkan file penyiapan membuat resource-nya dan memberikan akses kepada Anthropic ke bucket Anda.

### Mengizinkan akun-akun

Agar file penyiapan dapat memberikan akses kepada Anthropic, izinkan akun-akun berikut jika domain-restricted sharing aktif. Pembatasan ini menjadi default di organisasi Google Cloud yang dibuat pada atau setelah 3 Mei 2024, dan hanya mengizinkan pemberian izin IAM kepada anggota organisasi Anda. Jika Anda tidak mengizinkan akun-akun tersebut, apply akan berhenti dengan error seperti “One or more users named in the policy do not belong to a permitted customer.”

Akun terakhir adalah service agent Cloud Storage milik proyek Anda sendiri, yang menggunakan kunci bucket:

* `anthropic-efs-ingest@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-read@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-maintenance@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-media-erasure@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-verify@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-transcripts@anthropic-storage-us.iam.gserviceaccount.com`
* `anthropic-efs-review@anthropic-storage-us.iam.gserviceaccount.com`
* `service-123456789012@gs-project-accounts.iam.gserviceaccount.com`, dengan nomor proyek Anda

Dalam kebijakan, tulis `serviceAccount:` sebelum setiap alamat. Ubah setiap batasan (constraint) yang berlaku untuk proyek ini:

* **`constraints/iam.managed.allowedPolicyMembers`** mencantumkan akun satu per satu. Tambahkan semuanya.

* **`constraints/iam.allowedPolicyMemberDomains`** hanya mencantumkan seluruh organisasi. Pilih salah satu opsi berikut:

  * Pada proyek ini, berlakukan `constraints/iam.managed.allowedPolicyMembers` dengan organisasi Anda sendiri dan akun-akun ini, lalu timpa (override) `constraints/iam.allowedPolicyMemberDomains`.
  * Lepaskan batasan dari proyek ini, lakukan apply, lalu pasang kembali batasan tersebut ([memaksakan akses akun](https://docs.cloud.google.com/organization-policy/restrict-domains#forcing_access)). Ulangi pada setiap apply berikutnya yang menambahkan atau mengganti pemberian izin.

Tunggu hingga 15 menit agar perubahan kebijakan berlaku.

### Periksa kebijakan Anda yang lain

Pastikan kebijakan organisasi Anda yang lain memberikan apa yang dibutuhkan penyiapan:

| Kebijakan | Apa yang dibutuhkan penyiapan |
| ----- | ----- |
| `constraints/cloudkms.allowedProtectionLevels` | Mengizinkan `HSM` |
| `constraints/gcp.resourceLocations` | Mengizinkan [region](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#supported-regions) bucket Anda |
| `constraints/storage.softDeletePolicySeconds` | Mengizinkan 0 |
| `constraints/gcp.restrictCmekCryptoKeyProjects` | Mengizinkan proyek ini |
| `constraints/storage.retentionPolicySeconds` | Tidak berlaku untuk proyek ini |
| Perimeter VPC Service Controls | Aturan ingress mengizinkan akun-akun Anthropic, dari sumber mana pun, ke `storage.googleapis.com` |
| Pemfilteran IP atau kebijakan penolakan IAM (IAM deny policy) | Tidak menjangkau akun-akun Anthropic |

## 2. Buat dan uji bucket

Pada langkah ini, Anda mengunduh file Terraform dari Claude Console, melakukan apply, dan menguji hasilnya. File tersebut membuat bucket, kunci Cloud KMS `HSM` yang mengenkripsinya, peran kustom, dan pemberian izin kepada akun-akun Anthropic. File tersebut juga menyiapkan bucket untuk menampung transkrip dan Safety Cases.

Aturan siklus hidup bucket itu sendiri menghapus setiap objek data keselamatan tersegel setelah objek tersebut berumur 28 hari dan menghapusnya secara permanen setidaknya satu hari kemudian.

<Warning>
  Siapa pun yang memiliki peran Viewer pada proyek dapat mengunduh objek di semua bucket dalam proyek tersebut, termasuk transkrip dan file Safety Case apa pun. File-file tersebut tidak tersegel, sehingga siapa pun yang mengunduhnya dapat membacanya. Siapa pun yang memiliki peran Editor atau Owner juga dapat mengubah atau menghapus objek tersebut. Gunakan satu proyek untuk lebih dari satu organisasi Anthropic hanya jika Anda menerima akses tersebut.
</Warning>

1. Di halaman [Retensi data](https://platform.claude.com/settings/privacy) di Claude Console, pilih **Organisasi** di bagian atas dan klik **Connect storage**. Pastikan Anda berada di organisasi Anthropic yang ruang kerjanya akan menggunakan bucket ini.

   * **Di Claude Models on Google Cloud (Anthropic managed):** Dialog tidak meminta penyedia, dan dialog mengisi nomor proyek yang organisasinya akan menggunakan bucket ini. Jika dialog melakukan hal lain, Anda berada di organisasi yang salah. Buka Claude Console dari proyek tersebut.
   * **Di Claude Platform:** Pilih **Google Cloud Storage**.
   * Jika **Connect storage** tidak ada atau tidak tersedia, atau **Google Cloud Storage** menampilkan **Not available yet**, hubungi tim akun Anthropic Anda.

2. Masukkan nomor proyek Anda, atau periksa nomor tersebut jika dialog telah mengisinya. Lalu, masukkan nama bucket baru yang kemungkinan besar belum digunakan. Di bawah **Google Cloud region**, pertahankan `us-east5` atau pilih [region lain](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#supported-regions). Setelah Anda mengklik **Continue**, Anda hanya dapat mengubah ketiga nilai ini dengan [menghapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#delete-a-storage-destination) dan menghubungkannya kembali.

3. Pilih **Terraform**, masukkan ID proyek Anda, lalu unduh `customer-bucket-setup-gcs.tf` ke folder kosong.

4. Di folder tersebut, jalankan perintah-perintah berikut. Dialog menampilkan dua perintah `terraform` dengan nilai Anda sendiri.

```bash
gcloud auth login
gcloud auth application-default login
gcloud services enable storage.googleapis.com --project acme-claude-storage
gcloud services enable cloudkms.googleapis.com --project acme-claude-storage
gcloud services enable iam.googleapis.com --project acme-claude-storage

terraform init
terraform apply \
  -var "project_id=acme-claude-storage" \
  -var "project_number=123456789012" \
  -var "organization_id=8a3f2c1e-5b7d-4e9a-a1c6-2f4e8d0b7c35" \
  -var "bucket_name=acme-claude-retention" \
  -var "region=us-east5"
```

Pada apply pertama Anda, di `Enter a value:`, jawab `yes` hanya jika rencana menampilkan `Plan: 42 to add, 0 to change, 0 to destroy.` Jika tidak, jawab `no`, unduh file tersebut lagi untuk menimpa file lama, lalu jalankan kedua perintah `terraform` lagi. Jika rencana masih berbeda, hubungi tim akun Anthropic Anda.

Simpan seluruh folder dan perintah apply. Claude Console tidak menampilkan perintah tersebut lagi setelah pengujian lulus.

Setelah apply, tunggu 10 menit agar pemberian izin berlaku, lalu klik **Test setup** dan tunggu hingga **Ready**.

<Warning title="Biarkan apa yang dibuat file apa adanya">
  Jika Anda mengubah apa yang dibuat file, Anda dapat kehilangan data atau mengakhiri akses Anthropic ke bucket Anda.
</Warning>

Secara khusus, jangan:

* Menambahkan aturan siklus hidup yang menghapus objek.
* Menonaktifkan versioning.
* Mengubah atau menghapus aturan, peran, pemberian izin, atau label dari file.
* Mengaktifkan soft delete, retention policy, object retention, default hold, atau Requester Pays.
* Mengubah kunci default bucket.
* Menonaktifkan atau menghancurkan kunci atau versinya, atau menghapus pemberian izin kunci kepada Cloud Storage. Objek akan menjadi tidak dapat dibaca.
* Mengubah, memindahkan, menghapus, atau menambahkan objek di folder yang dinamai sesuai ID organisasi Anthropic Anda. Pengecualiannya adalah [file respons](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#response-file) tim Anda, yang ditempatkan di bawah `review-responses/` di folder tersebut.
* Menghapus `prevent_destroy` dari file.
* Menjalankan `terraform taint` atau `terraform apply -replace=...` pada pemberian izin.

### Region yang didukung

Anda dapat menggunakan region mana pun dalam daftar **Google Cloud region** di dialog. Anthropic merekomendasikan `us-east5`, karena Anthropic membaca dan menulis bucket Anda dari `us-east5`. Bucket di region lain dapat memengaruhi biaya transfer jaringan Anda. Region bucket Anda menentukan tempat penyedia cloud Anda menyimpan objek bucket. Region tersebut tidak mengubah [tempat inferensi model berjalan](https://platform.claude.com/docs/id/manage-claude/data-residency#inference-geo) atau tempat Anthropic memproses data Anda.

### Jika proses apply atau Test setup gagal

Untuk memperbaiki kegagalan, temukan kegagalan tersebut di tabel ini dan lakukan apa yang dinyatakannya. Untuk kegagalan lainnya, lakukan apply lagi dari folder yang sama dengan nilai yang sama.

| Apa yang Anda lihat | Apa yang harus dilakukan |
| ----- | ----- |
| Di proyek baru, Google Cloud menolak pemberian izin atau bucket. | Tunggu 10 menit, lalu lakukan apply lagi. |
| Google Cloud menolak pemberian izin kepada salah satu akun Anthropic atau kepada Cloud Storage. | [Izinkan akun-akun](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#allow-the-accounts), lalu lakukan apply lagi. |
| Kebijakan organisasi menolak kunci atau bucket. | [Periksa kebijakan Anda yang lain](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#check-your-other-policies), lalu lakukan apply lagi. |
| “Instance cannot be destroyed.” atau “organization\_id differs from the value that Terraform’s state keeps” | Berikan nilai dari apply pertama. Jika `organization_id` pada apply tersebut salah, jangan ubah apa pun dan hubungi tim akun Anthropic Anda. |
| Pemberian izin “is tainted, so must be replaced.” | Jangan terapkan rencana tersebut. Jika pemberian izin tersebut ada di Google Cloud, jalankan `terraform untaint` dengan alamatnya. Jika tidak ada, jalankan `terraform state rm` dengan alamatnya dan lakukan apply lagi. |
| Nama bucket sudah digunakan. | [Hapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#delete-a-storage-destination), lalu mulai lagi dari [Buat dan uji bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket) dengan nama baru dan folder kosong baru. Kunci dan peran dari apply pertama tetap berada di proyek Anda. |
| **Test setup** menyatakan bahwa organisasi lain telah menggunakan bucket ini. | [Hapus tujuan penyimpanan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#delete-a-storage-destination), lalu mulai lagi dari [Buat dan uji bucket](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#gcs-create-the-bucket) dengan nama bucket baru dan folder kosong baru. Bucket, kunci, dan peran dari apply pertama tetap berada di tempatnya. |

### Memperbarui bucket dari file penyiapan sebelumnya

Jika **Test setup** menyatakan bahwa bucket berasal dari template penyiapan sebelumnya, perbarui bucket dengan file saat ini:

1. Di mana pun Anda mencantumkan akun-akun Anthropic, tambahkan akun yang baru di [Izinkan akun-akun](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#allow-the-accounts).
2. Klik **Finish setup**, masukkan ID proyek Anda, lalu unduh file tersebut untuk menimpa file lama di folder Anda.
3. Jalankan `terraform init`, lalu perintah apply Anda dengan nilai yang sama. Jika rencana gagal atau akan menghancurkan atau mengganti apa pun, jawab `no` dan hubungi tim akun Anthropic Anda.
4. Tunggu 10 menit, lalu klik **Test setup**.

### Menghapus tujuan penyimpanan

Untuk menghapus tujuan penyimpanan yang menampilkan **Needs setup** atau **Ready**, pilih **Delete** di menu barisnya di bawah **Storage destinations**. Bucket dan pemberian izin kepada Anthropic tetap berada di proyek Anda.

## 3. Gunakan bucket Cloud Storage Anda di ruang kerja

Setelah bucket Anda lulus pengujian, pilih bucket tersebut untuk setiap ruang kerja yang seharusnya menggunakannya. Jika organisasi Anda memiliki pengaturan Legacy Zero Data Retention (ZDR), pilih kartu **Enterprise Frontier Safeguards** dan bucket Anda saat Anda membuat ruang kerja.

Dengan EFS, Anthropic Human Review selalu nonaktif, sehingga meninjau [Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases) menjadi tugas tim Anda sendiri.

Sebelum Anda memilih bucket, pastikan Anda berada di organisasi Anthropic yang ruang kerjanya akan menggunakannya. Setelah Anda menyimpan atau membuat ruang kerja dengan bucket terpilih, Anda tidak dapat menghapus tujuan penyimpanan. Setelah itu, tidak ada organisasi Anthropic lain yang dapat menggunakan bucket tersebut untuk penyimpanan milik pelanggan.

<Warning>
  Bicarakan dengan tim akun Anthropic Anda sebelum Anda memilih bucket jika:

  * **Organisasi Anda menggunakan Legacy Zero Data Retention.** Data keselamatan tersegel [mungkin masuk ke penyimpanan yang dikelola Anthropic pada awalnya](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#confirm-that-objects-arrive).
  * **Anda menginginkan lebih dari satu bucket atau banyak ruang kerja.** Anthropic membatasi jumlah masing-masing. Jika Anda melampaui batas, data tidak masuk ke bucket Anda, dan Claude Console tidak menampilkan error.
</Warning>

Melampirkan [kunci yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/customer-managed-keys#attach-a-customer-managed-key) ke ruang kerja bersifat permanen. Gunakan kunci yang berbeda dari kunci bucket itu sendiri.

Di halaman [Retensi data](https://platform.claude.com/settings/privacy) ruang kerja, pilih kartu **Enterprise Frontier Safeguards**, lalu pilih bucket Anda di bawah **Sealed Safety Data storage**. Di bawah **Safety Case and Transcript storage**, Anda memilih bucket untuk transkrip dan Safety Cases dalam bentuk yang dapat dibaca tim Anda. Jika halaman menampilkan pengaturan tersebut, Anda dapat memilih bucket yang sama. <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">Tindakan simpan Anda gagal jika Anda tidak memilih bucket di bawah pengaturan tersebut. Jika halaman tidak menampilkan pengaturan tersebut, hubungi tim akun Anthropic Anda sebelum Anda menyimpan.</Where> Lalu, simpan ruang kerja. Jika Anthropic menolak bucket Anda saat Anda menyimpan, hubungi tim akun Anthropic Anda sebelum Anda menghubungkan bucket lain. <Where cloud="claude" label="Claude Platform">Untuk langkah lengkapnya, lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Platform](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#turn-on-efs-for-a-workspace).</Where> <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">Untuk langkah lengkapnya, lihat [Menyiapkan Enterprise Frontier Safeguards di Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-claude-models-on-google-cloud-anthropic-managed#turn-on-efs-for-a-workspace).</Where>

Menyimpan akan menonaktifkan Anthropic Human Review, yang dapat memerlukan waktu hingga 2 jam. Untuk memastikan penyimpanan Anda berhasil, pastikan **Case review by** menunjukkan **My organization** di panel samping ruang kerja di halaman [Workspaces](https://platform.claude.com/settings/workspaces). Jika tidak menunjukkan **My organization**, buka ruang kerja di halaman [Retensi data](https://platform.claude.com/settings/privacy) dan klik **Save** lagi, meskipun Anda tidak mengubah apa pun. Jika Anda tidak dapat melakukannya, atau **Case review by** masih tidak menunjukkan **My organization**, hubungi tim akun Anthropic Anda sebelum Anda mengirim lalu lintas nyata.

Di bucket Anda, file-file yang dijelaskan di [file Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files) masuk ke folder yang dinamai sesuai ID organisasi Anthropic Anda, seperti `<organization ID>/review-cases/<id>.json` dan `<organization ID>/review-responses/<case_id>.json`.

Untuk meninjau Safety Cases di bucket Anda, tim Anda perlu menampilkan daftar dan membaca file di bawah `transcripts/`, `review-cases/`, `review-summaries/`, `review-notices/`, dan `review-responses/` di folder organisasi Anda. Untuk merespons, tim Anda juga perlu membuat file di bawah `review-responses/`. File penyiapan tidak memberikan akses ini kepada tim Anda, jadi berikan sendiri di Google Cloud IAM. Batasi akses baca ke folder-folder ini, dan batasi akses pembuatan ke `review-responses/`.

### Pastikan objek tiba

Sebelum ruang kerja menangani lalu lintas yang perlu disimpan di bucket Anda, pastikan objek baru tiba. Lalu, tunggu 10 menit lagi, karena server Anthropic tidak semuanya menerapkan perubahan secara bersamaan. Hingga saat itu, kirim hanya permintaan uji, karena data keselamatan tersegel ruang kerja mungkin masuk ke penyimpanan yang dikelola Anthropic. Jika ruang kerja lain sudah mengirim data ke bucket ini, objek baru tidak menunjukkan bahwa perubahan ini telah berlaku, jadi tanyakan kepada tim akun Anthropic Anda sebelum Anda mengirim lalu lintas nyata.

Kirim permintaan uji tanpa data sensitif ke ruang kerja tersebut. <Where cloud="claude" label="Claude Platform">Gunakan kredensial untuk ruang kerja tersebut.</Where> Lalu, tampilkan daftar isi `slab/` dengan `bucket_name` dan `organization_id` dari perintah apply Anda:

```bash
gcloud storage ls gs://acme-claude-retention/8a3f2c1e-5b7d-4e9a-a1c6-2f4e8d0b7c35/safeguards-data/slab/
```

Status **Active** dapat muncul sebelum objek tiba, jadi jangan mengandalkannya. Jika perintah tersebut masih berhenti dengan “One or more URLs matched no objects.”, hubungi tim akun Anthropic Anda. Objek di bawah `slab/` menunjukkan bahwa data keselamatan tersegel tiba. Objek tersebut tidak menunjukkan bahwa transkrip atau Safety Cases tiba.

### Jika bucket Anda berhenti berfungsi

Untuk menghindari kehilangan data, pulihkan bucket yang berhenti berfungsi sesegera mungkin. Jika penulisan ke bucket Anda gagal, Anthropic mencoba ulang penulisan tersebut, lalu menghapus data sekitar satu hari setelah permintaan. Tidak ada yang dapat memulihkan data tersebut, dan data tersebut tidak masuk ke penyimpanan yang dikelola Anthropic.

Untuk mengetahui adanya kegagalan, pantau objek baru di bawah `slab/`. Jangan mengandalkan email atau status bucket untuk memperingatkan Anda. Jika Anda mengetahui adanya kegagalan, beri tahu tim akun Anthropic Anda sesegera mungkin.

Untuk memulihkan bucket Anda, lakukan tindakan yang sesuai dengan perubahannya:

* **Pemberian izin atau pengaturan:** Lakukan apply lagi dengan nilai yang sama. Rencana seharusnya tidak menghancurkan apa pun.
* **Peran kustom yang dihapus:** Jalankan `gcloud iam roles undelete` dalam 7 hari. Apply tidak memulihkannya.
* **Versi kunci yang dinonaktifkan:** Jalankan `gcloud kms keys versions enable`, setelah `restore` jika versi tersebut dijadwalkan untuk dihancurkan.
* **Hal lainnya:** Hubungi tim akun Anthropic Anda.

## Berhenti menggunakan bucket Anda

Untuk berhenti menggunakan bucket Anda, ikuti langkah-langkah ini secara berurutan, atau Anda dapat kehilangan data. <Where cloud="gcp" label="Claude Models on Google Cloud (Anthropic managed)">Ikuti langkah-langkah ini sebelum Anda membatalkan langganan atau menghapus proyek Anda. Tidak satu pun dari tindakan tersebut melepaskan ruang kerja dari bucket.</Where>

Sebelum Anda mengubah atau menghapus bucket ruang kerja, [tanggapi Safety Cases yang masih terbuka di ruang kerja tersebut](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#respond-to-a-case) dan [tunggu hingga Safety Cases tersebut ditutup](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#after-you-respond). Jika Anda mengubah atau menghapus bucket terlebih dahulu, Anthropic mungkin tidak membaca file respons Anda.

<Warning title="Simpan file penyiapan beserta state-nya">
  Tanpa file tersebut, Terraform merencanakan untuk menghancurkan semua yang masih ada di state, dan `prevent_destroy` tidak lagi menghentikannya.
</Warning>

1. Lepaskan setiap ruang kerja dari bucket. Di halaman [Retensi data](https://platform.claude.com/settings/privacy) setiap ruang kerja, pilih bucket lain di bawah **Sealed Safety Data storage**. Atau, pilih kartu **Anthropic managed** atau, jika tercantum, kartu **Legacy ZDR**. Bicarakan dengan tim akun Anthropic Anda sebelum Anda memilih bucket lain. Jika **Safety Case and Transcript storage** masih menampilkan bucket ini, ubah juga pengaturan tersebut. Lalu, simpan.

   * **Jika Anda tidak dapat memilih kartu Anthropic managed,** ubah [kebijakan untuk ruang kerja baru](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-console#set-organization-defaults) organisasi Anda terlebih dahulu.
   * Kartu mana pun melepaskan ruang kerja dari EFS, dan kartu **Anthropic managed** dapat [mengaktifkan kembali Anthropic Human Review](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/human-review-and-access-transparency#turn-off-anthropic-human-review). Untuk menggunakan EFS lagi setelah **Legacy ZDR**, buat ruang kerja baru dengan kartu **Enterprise Frontier Safeguards**.

2. Kirim permintaan uji tanpa data sensitif dari setiap ruang kerja, lalu jalankan [perintah daftar](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/external-storage#confirm-that-objects-arrive) dengan `--recursive --long` sampai tidak ada objek baru yang masuk. Status **Draining** dapat muncul lebih awal dan tidak memiliki tanggal berakhir, jadi jangan mengandalkannya.

3. Cegah pipeline apa pun menerapkan file tersebut, karena `terraform apply` akan membuat pemberian izin Anthropic kembali. Lalu, bicarakan dengan tim akun Anthropic Anda dan tunggu jawaban mereka. Anthropic masih memerlukan aksesnya setelah berhenti menulis, untuk membaca apa yang tersimpan dan menghapus apa yang telah kedaluwarsa. Setelah tim tersebut mengonfirmasi bahwa Anthropic telah berhenti menggunakan bucket tersebut, hapus hanya pemberian izin Anthropic, dengan nilai dari apply terakhir Anda:

```bash
terraform destroy \
  -target=google_storage_bucket_iam_member.object \
  -target=google_storage_bucket_iam_member.list \
  -target=google_storage_bucket_iam_member.bucket \
  -target=google_storage_bucket_iam_member.review_object \
  -target=google_storage_bucket_iam_member.review_bucket \
  -var "project_id=acme-claude-storage" \
  -var "project_number=123456789012" \
  -var "organization_id=8a3f2c1e-5b7d-4e9a-a1c6-2f4e8d0b7c35" \
  -var "bucket_name=acme-claude-retention" \
  -var "region=us-east5"
```

Rencana tidak boleh menambahkan atau mengubah apa pun, dan hanya boleh menghancurkan resource `google_storage_bucket_iam_member`. Menonaktifkan kunci tidak mengakhiri akses Anthropic, karena akun-akun tersebut masih dapat menampilkan daftar objek dan menghapus objek.

</Where>
