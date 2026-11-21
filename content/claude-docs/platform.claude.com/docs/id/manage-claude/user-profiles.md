---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-profiles
fetched_at: 2026-11-21T02:12:50.066053Z
sha256: 54ce7981b1f9720d9b59920b6ac7b54f65c044536428cae60d263556b787f4a4
---

---
title: Profil pengguna untuk atribusi pelanggan akhir
url: https://platform.claude.com/docs/id/manage-claude/user-profiles
description: Atribusikan permintaan API ke pelanggan akhir yang dilayani platform Anda, sehingga tindakan penegakan keamanan dapat diterapkan pada satu profil alih-alih seluruh organisasi Anda.
---

Profil pengguna (“profil”) memberi tahu Anthropic untuk pelanggan akhir mana setiap permintaan API ditujukan. Tindakan penegakan keamanan, seperti pembatasan atau pemblokiran, kemudian dapat diterapkan pada satu pelanggan akhir alih-alih pada seluruh organisasi Anda. Ketika hal itu terjadi, lalu lintas Anda yang lain tidak terpengaruh.

Jika Anda mengoperasikan platform atau gateway, atau menjual kembali akses API, permintaan yang Anda kirim untuk pelanggan akhir Anda tiba di bawah organisasi Anda. Anthropic menjalankan “safety classifier” (pengklasifikasi keamanan) otomatis pada lalu lintas API. Tanpa profil pada permintaan, satu pelanggan akhir dapat memicu tindakan penegakan yang berlaku untuk seluruh organisasi Anda.

Anda mendaftarkan setiap pelanggan akhir satu kali dengan `POST /v1/user_profiles` dan menyimpan ID `uprof_` yang dikembalikannya. Kemudian Anda mengirim ID tersebut di header `anthropic-user-profile-id` pada setiap permintaan yang Anda buat atas nama pelanggan akhir tersebut.

Dengan sendirinya, profil tidak mengubah penagihan atau harga. Jika Anda menggunakan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections), profil juga merupakan cara Anda mengidentifikasi pelanggan yang akan ditagih.

## Tentukan siapa yang mendapatkan profil

Setiap pelanggan akhir mendapatkan satu profil, sehingga sebuah perusahaan mendapatkan satu profil untuk seluruh perusahaan, bukan satu profil untuk setiap orang di perusahaan tersebut. Kirim ID profil tersebut pada setiap permintaan yang Anda buat untuk siapa pun di perusahaan tersebut. Untuk juga memberi tahu Anthropic dari siapa sebuah permintaan berasal, lihat [Identifikasi satu orang dalam sebuah perusahaan](https://platform.claude.com/docs/id/manage-claude/user-profiles#identify-individual-users-within-a-company).

Field `access_type` pada profil menyatakan apakah pelanggan akhir menggunakan produk Anda atau membeli akses API dari Anda, misalnya melalui gateway Anda:

| Pelanggan akhir | `access_type` |
| ----- | ----- |
| Menggunakan produk Anda | `application` (default, ditetapkan saat Anda menghilangkan `access_type`) |
| Merupakan perusahaan yang membeli akses API dari Anda | `passthrough` (bukan default, sehingga Anda harus mengirimkannya) |

Jangan buat profil untuk kedua hal berikut:

* **Penggunaan Anda sendiri:** Anthropic menghitung permintaan tanpa ID profil sebagai penggunaan Anda sendiri. Tempatkan penggunaan tersebut di organisasi terpisah, seperti yang dijelaskan di [Sebelum Anda memulai](https://platform.claude.com/docs/id/manage-claude/user-profiles#before-you-begin).
* **Workspace di organisasi Anda:** Profil dimiliki oleh organisasi Anda, bukan oleh workspace, sehingga ID profil tersebut berfungsi pada permintaan melalui workspace mana pun di organisasi tersebut. Pengecualiannya adalah workspace yang memiliki profil berbeda yang dilampirkan melalui `user_profile_id` di [Buat Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/create) atau [Perbarui Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/update). Setiap permintaan inferensi melalui workspace tersebut harus membawa ID profil yang dilampirkan, dan API menolak permintaan dengan ID lain atau tanpa ID.

## Apa isi profil dan bagaimana Anthropic menggunakannya

Profil hanya berisi apa yang Anda kirim tentang pelanggan akhir, ditambah [status program](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal#after-the-end-customer-links-the-profile) atau status penegakan apa pun yang ditetapkan Anthropic. Profil tidak berisi konten percakapan. Anthropic menggunakan detail yang Anda kirim untuk mengatribusikan permintaan, memantau penyalahgunaan, menegakkan [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup), serta memungkinkan pengajuan dan akses ke program akses tepercaya. Anthropic tidak memverifikasi detail tersebut.

Anthropic memproses profil sesuai dengan [Kebijakan Privasi](https://www.anthropic.com/legal/privacy).

## Sebelum Anda memulai

Anda membuat dan mengelola profil di salah satu dari berikut ini:

* Organisasi di Claude API.
* Organisasi di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Principal yang memanggil memerlukan [tindakan IAM profil pengguna](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#user-profiles).
* Organisasi di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), tempat Anda dapat membuat, mengambil, mencantumkan, dan memperbarui profil. Gunakan versi terbaru [klien SDK untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#install-an-sdk), atau panggil [base URL tingkat organisasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#making-requests) secara langsung, dengan kredensial Google Cloud alih-alih kunci API.

Endpoint `/v1/user_profiles` tidak tersedia di Claude Models on Google Cloud (Google managed) atau Amazon Bedrock. Jika inferensi Anda berjalan di sana, buat profil Anda di organisasi di Claude API atau Claude Platform on AWS. Di Amazon Bedrock, apakah profil berfungsi bergantung pada modelnya. Lihat [Atribusikan permintaan di Claude Models on Google Cloud (Google managed) dan Amazon Bedrock](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud).

Jika inferensi Anda berjalan pada deployment [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) yang [di-hosting di Anthropic](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#hosting-options), buat profil Anda di organisasi di Claude API. Sebelum permintaan Foundry Anda dapat menggunakan ID profil tersebut, Anthropic harus menautkan resource Foundry Anda ke organisasi tersebut. Untuk meminta penautan ini, hubungi tim akun Anthropic Anda. Endpoint `/v1/user_profiles` tidak tersedia di Microsoft Foundry.

Tempatkan lalu lintas yang Anda kirim untuk pelanggan akhir Anda di satu organisasi dan penggunaan internal Anda sendiri di organisasi lain. Profil dimiliki oleh organisasi, bukan workspace, sehingga workspace terpisah dalam satu organisasi tidak cukup. Hanya organisasi untuk lalu lintas pelanggan akhir yang memerlukan profil pengguna. Untuk membuat organisasi lain di Claude API, lihat bagian “How to create a new organization” dari [Buat dan kelola Workspace di Claude Console](https://support.claude.com/en/articles/9796807) di Pusat Bantuan Claude.

Contoh-contoh ini memanggil Claude API dengan kunci API. Anda tidak memerlukan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys). Di Claude Platform on AWS, gunakan base URL dan autentikasinya.

## Buat profil untuk setiap pelanggan akhir

Buat satu profil untuk setiap pelanggan akhir yang lalu lintasnya Anda kirim ke Claude. Buat sekali saja, dalam alur onboarding pelanggan Anda. `POST /v1/user_profiles` tidak “idempotent” (idempoten), sehingga setiap panggilan membuat profil baru, bahkan ketika `reference_id` cocok dengan profil yang sudah ada. Jika Anda sudah memiliki pelanggan akhir tanpa profil, lihat panduan nanti di bagian ini tentang mendaftarkan basis pelanggan yang sudah ada.

Contoh berikut mendaftarkan perusahaan yang membeli akses API dari Anda, sehingga permintaan tersebut menetapkan `access_type` ke `passthrough`. Untuk profil `application`, hilangkan `access_type`. [Tentukan siapa yang mendapatkan profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#decide-who-gets-a-profile) menjelaskan jenis akses mana yang harus digunakan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "name": "Acme Analytics, Inc.",
      "access_type": "passthrough",
      "external_user_details": {
        "reference_id": "cust-8f2a1c",
        "country": "US"
      }
    }'
  ```

  ```bash CLI
  ant user-profiles create \
    --name "Acme Analytics, Inc." \
    --access-type passthrough \
    --external-user-details '{reference_id: cust-8f2a1c, country: US}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  profile = client.user_profiles.create(
      name="Acme Analytics, Inc.",
      access_type="passthrough",
      external_user_details={"reference_id": "cust-8f2a1c", "country": "US"},
  )

  print(profile.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const profile = await client.userProfiles.create({
    name: "Acme Analytics, Inc.",
    access_type: "passthrough",
    external_user_details: { reference_id: "cust-8f2a1c", country: "US" }
  });

  console.log(profile.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var profile = await client.UserProfiles.Create(new()
  {
      Name = "Acme Analytics, Inc.",
      AccessType = UserProfileAccessType.Passthrough,
      ExternalUserDetails = new()
      {
          ReferenceID = "cust-8f2a1c",
          Country = "US"
      }
  });

  Console.WriteLine(profile.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  profile, err := client.UserProfiles.New(context.Background(), anthropic.UserProfileNewParams{
  	Name:       anthropic.String("Acme Analytics, Inc."),
  	AccessType: anthropic.UserProfileAccessTypePassthrough,
  	ExternalUserDetails: anthropic.UserProfileExternalUserDetailsParams{
  		ReferenceID: anthropic.String("cust-8f2a1c"),
  		Country:     anthropic.String("US"),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(profile.ID)
  ```

  ```java Java
  import com.anthropic.models.userprofiles.UserProfileAccessType;
  import com.anthropic.models.userprofiles.UserProfileCreateParams;
  import com.anthropic.models.userprofiles.UserProfileExternalUserDetailsParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserProfileCreateParams.builder()
          .name("Acme Analytics, Inc.")
          .accessType(UserProfileAccessType.PASSTHROUGH)
          .externalUserDetails(UserProfileExternalUserDetailsParams.builder()
              .referenceId("cust-8f2a1c")
              .country("US")
              .build())
          .build();
      var profile = client.userProfiles().create(params);

      IO.println(profile.id());
      // ...
  }
  ```

  ```php PHP
  $client = new Client();

  $profile = $client->userProfiles->create(
      name: 'Acme Analytics, Inc.',
      accessType: 'passthrough',
      externalUserDetails: ['referenceID' => 'cust-8f2a1c', 'country' => 'US'],
  );

  echo $profile->id, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  profile = client.user_profiles.create(
    name: "Acme Analytics, Inc.",
    access_type: :passthrough,
    external_user_details: { reference_id: "cust-8f2a1c", country: "US" }
  )

  puts profile.id
  ```
</CodeGroup>

Responsnya adalah profil baru:

```json
{
  "type": "user_profile",
  "id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
  "name": "Acme Analytics, Inc.",
  "access_type": "passthrough",
  "external_user_details": {
    "reference_id": "cust-8f2a1c",
    "onboarded_at": null,
    "account_status": null,
    "entity_type": null,
    "country": "US",
    "name_hash": null,
    "email_hash": null
  },
  "metadata": {},
  "programs": {
    "cyber": null,
    "efs": null
  },
  "created_at": "2026-03-15T10:00:00Z",
  "updated_at": "2026-03-15T10:00:00Z"
}
```

Simpan `id` pada catatan pelanggan Anda, dan minta instance layanan Anda membacanya dari sana alih-alih membuat profil sendiri. Anda mengambil, memperbarui, dan menghapus profil berdasarkan `id` tersebut. Field `programs` bersifat read-only, dan atribusi tidak menggunakannya. Field ini menyimpan status pelanggan akhir di setiap program yang dijalankan Anthropic. Untuk arti nilai-nilainya, lihat [program mana yang berlaku untuk profil](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal#after-the-end-customer-links-the-profile). [Periksa apakah Anthropic telah membatasi atau memblokir profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#check-whether-anthropic-has-restricted-or-banned-a-profile) menjelaskan field `enforcement_status` dan `enforcement_actions`.

Tidak ada batas jumlah profil dalam sebuah organisasi, tetapi pembuatan profil dikenai “rate limit” (batas laju). Sebelum Anda mendaftarkan basis pelanggan yang sudah ada secara massal, hubungi tim akun Anthropic Anda.

### Apa yang perlu diberitahukan kepada Anthropic tentang pelanggan akhir

Setiap field bersifat opsional. Anda dapat mengirim `name`, `metadata`, dan field-field berikut di `external_user_details`: `entity_type`, `country`, `reference_id`, `onboarded_at`, `account_status`, `name_hash`, dan `email_hash`. Referensi [Membuat profil](https://platform.claude.com/docs/id/api/user_profiles/create) menjelaskan setiap field, beserta tipe, format, dan batas panjangnya.

Ikuti aturan berikut saat Anda menetapkan field:

* **Nilai yang tidak diketahui:** Jika Anda tidak mengetahui suatu nilai, hilangkan alih-alih mengirim placeholder. Anda dapat mengganti nilai di `external_user_details` nanti, tetapi Anda tidak dapat mengosongkannya.
* **Nama:** Di `name`, kirim nama asli pelanggan akhir. Untuk perusahaan, kirim nama resmi perusahaan tersebut jika Anda mengetahuinya.
* **Nama dan alamat email yang tidak dapat Anda bagikan:** Hilangkan `name` dan kirim `external_user_details.name_hash` sebagai gantinya. Untuk alamat email, kirim `external_user_details.email_hash`, karena profil tidak memiliki field untuk alamat email itu sendiri.
* **Negara:** Di `country`, kirim negara pelanggan akhir, bukan negara Anda.
* **ID Anda sendiri:** Di `reference_id`, kirim pengidentifikasi stabil Anda sendiri untuk pelanggan akhir. Nilai ini tidak harus unik.
* **Hash:** Hitung hash sendiri dengan fungsi yang Anda pilih. Hash tersebut menunjukkan kepada Anthropic profil mana milik Anda yang memiliki nama atau alamat email yang sama. Hanya nilai yang dihitung dengan cara yang sama yang akan cocok, sehingga untuk setiap profil, gunakan fungsi yang sama dan tangani huruf besar-kecil dan spasi dengan cara yang sama.

## Atribusikan setiap permintaan

Kirim ID profil di header `anthropic-user-profile-id` pada setiap permintaan yang Anda buat atas nama pelanggan akhir. SDK dan CLI memiliki argumen yang mengirimkan header tersebut untuk Anda: `user_profile_id` (java: `userProfileId`; php: `userProfileID`; csharp, go: `UserProfileID`; cli: `--user-profile-id`).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-user-profile-id: $PROFILE_ID" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --user-profile-id "$PROFILE_ID"
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      user_profile_id=profile_id,
  )

  print(message)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: profileId
  });

  console.log(message);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new UserMessageParam { Content = "Hello, Claude" }],
      UserProfileID = profileId
  };
  var message = await client.Messages.Create(parameters);

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  	UserProfileID: anthropic.String(profileID),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .userProfileId(profileId)
          .build();
      var message = client.messages().create(params);

      IO.println(message);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
      userProfileID: $profileId,
  );

  echo json_encode($message, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: profile_id
  )

  puts message
  ```
</CodeGroup>

Header ini bekerja dengan cara yang sama pada permintaan [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting), [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing), dan [kompatibilitas OpenAI SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk). Pada batch, header ini berlaku untuk setiap permintaan dalam batch tersebut.

Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed), dan deployment Microsoft Foundry yang di-hosting di Anthropic memeriksa ID pada setiap permintaan. Jika ID tidak valid formatnya atau bukan milik organisasi yang mengirim permintaan, API mengembalikan `400` `invalid_request_error`. Secara default, platform-platform ini hanya menerima ID profil pada permintaan dari organisasi yang membuat profil tersebut. Ini berarti bahwa jika Anda mengirim lalu lintas di bawah lebih dari satu organisasi, misalnya satu di Claude API dan satu di Claude Platform on AWS, permintaan dari organisasi yang tidak membuat profil tersebut akan mendapatkan `400` yang sama. Pada deployment Microsoft Foundry yang di-hosting di Anthropic, setiap ID profil mendapatkan `400` ini hingga Anthropic [menautkan resource Foundry Anda](https://platform.claude.com/docs/id/manage-claude/user-profiles#before-you-begin) ke organisasi yang membuat profil tersebut.

Message Batches adalah pengecualian: pembuatan batch hanya memeriksa format ID. Jika ID yang formatnya valid bukan milik organisasi yang mengirim batch, batch tetap dibuat, dan setiap permintaan di dalamnya kemudian gagal dengan hasil `errored` yang berisi `invalid_request_error` yang sama.

### Identifikasi satu orang dalam sebuah perusahaan

Profil untuk perusahaan mengidentifikasi perusahaan tersebut, bukan orang yang menjadi asal sebuah permintaan. Jika sebuah permintaan berasal dari satu orang yang dapat Anda identifikasi, tetapkan juga [`metadata.user_id`](https://platform.claude.com/docs/id/api/messages/create) pada permintaan Messages ke pengidentifikasi untuk orang tersebut. Field ini berada di objek `metadata` milik permintaan itu sendiri, bukan di field `metadata` pada profil. Pengidentifikasi ini bersifat opsional dan membantu Anthropic mendeteksi penyalahgunaan oleh satu orang.

### Atribusikan permintaan di Claude Models on Google Cloud (Google managed) dan Amazon Bedrock

ID profil dari kedua jenis akses juga berfungsi di Claude Models on Google Cloud (Google managed). Di Amazon Bedrock, ID profil berfungsi untuk model yang tercantum setelah tabel berikut. Anda menggunakan kredensial organisasi Anthropic Anda hanya untuk membuat dan mengelola profil. Inferensi tetap menggunakan kredensial AWS atau Google Cloud Anda yang sudah ada.

| Platform | Membuat profil | Kirim ID profil di |
| ----- | ----- | ----- |
| Claude API | Ya | Header `anthropic-user-profile-id` |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | Ya | Header `anthropic-user-profile-id` |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), deployment yang di-hosting di Anthropic | Tidak. Buat profil di Claude API, dan [minta Anthropic menautkan resource Foundry Anda](https://platform.claude.com/docs/id/manage-claude/user-profiles#before-you-begin). | Header `anthropic-user-profile-id` |
| [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | Ya | Header `anthropic-user-profile-id` |
| [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed) | Tidak. Buat di Claude API atau Claude Platform on AWS. | Header `anthropic-user-profile-id` |
| [Claude di Amazon Bedrock (`bedrock-mantle`)](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Claude di Amazon Bedrock (`bedrock-runtime`)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), untuk model yang tercantum setelah tabel ini | Tidak. Buat di Claude API atau Claude Platform on AWS. | Field `user_profile_id` di body permintaan |

Profil berfungsi di [Claude di Amazon Bedrock (`bedrock-mantle`)](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan dengan `InvokeModel` di [Claude di Amazon Bedrock (`bedrock-runtime`)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy), termasuk streaming dengan `InvokeModelWithResponseStream`. Tidak setiap model dalam daftar berikut tersedia di kedua endpoint. Kirim ID profil pada permintaan untuk model-model berikut:

* Model Claude 4.7 dan yang lebih baru
* Claude Sonnet 4.6
* Claude Haiku 4.5

Jangan sertakan ID pada permintaan untuk model lain mana pun, karena permintaan yang membawanya dapat gagal dengan `400`. Jangan sertakan juga ID tersebut pada job inferensi batch Amazon Bedrock. Tanpa ID, permintaan ini tetap berfungsi, tetapi diproses tanpa atribusi.

API `Converse` tidak mendukung profil pengguna.

Di Amazon Bedrock, letakkan ID di tingkat teratas body permintaan. Contoh berikut menunjukkan body permintaan untuk endpoint `bedrock-mantle`:

```json
{
  "model": "anthropic.claude-opus-5-5",
  "max_tokens": 1024,
  "user_profile_id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
  "messages": [{ "role": "user", "content": "Hello, Claude" }]
}
```

Jika Anda memanggil `InvokeModel` secara langsung, ID model ditempatkan di URL permintaan (`modelId` di AWS SDK), bukan di body. Body juga memerlukan field `anthropic_version`, seperti `"anthropic_version": "bedrock-2023-05-31"`.

Jika Anda memanggil `InvokeModel` melalui `AnthropicBedrock` (csharp: `AnthropicBedrockClient`; go: `bedrock.WithLoadDefaultConfig()`; java: `BedrockBackend`; php: `Bedrock\Client`; ruby: `Anthropic::BedrockClient`), [versi terbaru SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/overview#latest-versions) akan menempatkan [argumen profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-each-request) di body permintaan untuk Anda. Versi sebelumnya dapat tidak menyertakan ID di body. Permintaan tersebut kemudian berhasil tetapi diproses tanpa atribusi.

Permintaan `InvokeModel` ke Claude Sonnet 4.6 dan Claude Haiku 4.5 dapat gagal dengan `400` pada versi API yang dikirimkan oleh SDK terbaru. Untuk model-model ini, tetaplah menggunakan versi mayor SDK sebelumnya. Untuk menginstalnya, gunakan perintah di [Instal SDK untuk mengakses Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#install-an-sdk-for-accessing-bedrock).

Jika Anda memanggil `InvokeModel` melalui versi SDK sebelumnya, tambahkan `user_profile_id` ke body sendiri dengan `extra_body` (typescript: `body`; php: `extraBodyParams`; java: `.putAdditionalBodyProperty()`; go: `option.WithJSONSet()`; csharp: `MessageCreateParams.FromRawUnchecked()`). Penambahan ini harus membiarkan bagian body lainnya tetap utuh. SDK membangun URL dari `model` di body dan, jika Anda melakukan streaming, `stream: true`.

Jika Anda memulai dari contoh di [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#making-requests), ubah modelnya ke salah satu [model yang menerima ID profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud).

Tautkan akun cloud Anda ke organisasi Anthropic yang membuat profil Anda. Di Amazon Bedrock, tautkan setiap akun AWS yang mengirim permintaan. Di Claude Models on Google Cloud (Google managed), tautkan setiap proyek Google Cloud yang mengirim permintaan. Untuk masing-masing, ikuti langkah-langkah berikut:

1. Admin organisasi tersebut memulai penautan di Verification Portal di `portal.anthropic.com`, di bawah **Linked accounts (akun tertaut)**.
2. Seseorang yang dapat mengelola IAM di akun AWS atau proyek Google Cloud menjalankan perintah yang disediakan portal.
3. Admin menyelesaikan verifikasi di portal.

Program yang berlaku untuk sebuah profil hanya berlaku untuk permintaan sebuah akun setelah akun tersebut ditautkan dan portal menampilkannya sebagai **Linked**. Program-program tersebut mencakup program yang disetujui untuk organisasi pelanggan akhir setelah pelanggan akhir [menautkan profil ke organisasi tersebut](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal) dan, untuk tingkat akses Cyber Verification Program, mengaktifkannya untuk profil tersebut di portal.

Claude Models on Google Cloud (Google managed) memeriksa format ID tetapi tidak mencari profilnya. Amazon Bedrock melakukan hal yang sama pada [model yang menerima ID profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud). Kedua platform menolak ID yang formatnya tidak valid dengan `400`. Keduanya menerima ID apa pun yang formatnya valid, sehingga respons yang berhasil tidak mengonfirmasi bahwa ID tersebut cocok dengan sebuah profil. Permintaan tanpa ID diproses tanpa atribusi, dan jika memicu tindakan penegakan, tindakan tersebut berlaku untuk seluruh organisasi Anda.

## Memeriksa apakah Anthropic telah membatasi atau memblokir sebuah profil

Field `enforcement_status` dan `enforcement_actions` pada sebuah profil melaporkan tindakan penegakan yang sedang dibuka Anthropic terhadap pelanggan akhir. Tindakan penegakan adalah pembatasan atau pemblokiran. Setiap respons yang mengembalikan profil menyertakan kedua field tersebut: pembuatan, pengambilan, pembaruan, dan setiap profil dalam daftar. Kirim permintaan ini tanpa nilai `user-profiles-` di header `anthropic-beta`, karena `user-profiles-2026-09-04` dan nilai-nilai sebelumnya tidak menyertakan field tersebut. Contoh berikut menunjukkan field tersebut pada profil yang diambil, dengan field lainnya dihilangkan:

```json
{
  "type": "user_profile",
  "id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
  "enforcement_status": "restricted",
  "enforcement_actions": [
    {
      "type": "restriction",
      "id": "enac_011CZkZEq4TnWb7xLfRgPm2v",
      "reason": "fraud_or_abuse",
      "action": null,
      "opened_at": "2026-10-02T19:30:00Z",
      "expires_at": null
    }
  ]
}
```

`enforcement_status` merangkum tindakan yang terbuka dalam satu nilai:

* `unrestricted`: Tidak ada tindakan yang terbuka.
* `restricted`: Setidaknya satu tindakan terbuka dan tidak ada satu pun yang merupakan pemblokiran.
* `banned`: Sebuah pemblokiran sedang terbuka.

Selama sebuah tindakan terbuka, Anthropic menolak sebagian atau seluruh permintaan inferensi yang membawa ID profil tersebut.

`enforcement_actions` mencantumkan tindakan yang terbuka dan kosong jika tidak ada. Tindakan yang berakhir akan keluar dari daftar. Setiap tindakan memiliki field berikut:

* `type`: `restriction` atau `ban`.
* `id`: ID tindakan, yang diawali dengan `enac_`.
* `reason`: Alasan Anthropic membuka tindakan tersebut. Nilainya salah satu dari `unsupported_region`, `fraud_or_abuse`, `high_harm`, `usage_policy_violation`, `account_compromise`, atau `unspecified`.
* `action`: Apa yang dapat dilakukan pelanggan akhir untuk mencabut tindakan tersebut, atau `null` jika tidak ada yang dapat mereka lakukan.
* `opened_at`: Kapan Anthropic membuka tindakan tersebut.
* `expires_at`: Kapan tindakan tersebut berakhir dengan sendirinya, atau `null` jika tidak memiliki tanggal berakhir.

Untuk memeriksa sebuah profil, ambil profil tersebut dengan [`GET /v1/user_profiles/{id}`](https://platform.claude.com/docs/id/api/user_profiles/retrieve). Untuk menemukan profil yang memiliki tindakan terbuka, [tampilkan daftar profil Anda](https://platform.claude.com/docs/id/api/user_profiles/list) dengan `enforcement_status[]=restricted` dan `enforcement_status[]=banned`. Untuk mendapatkan event saat sebuah tindakan dibuka atau berakhir, lihat [Webhook organisasi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks). Tanpa event, bandingkan kedua field tersebut dengan nilai yang terakhir Anda lihat. Sebuah perubahan tidak selalu memperbarui `updated_at`.

Anthropic yang menetapkan kedua field tersebut. Jika permintaan create atau update menyertakan salah satunya, API mengembalikan `400`. `enforcement_status` terpisah dari `external_user_details.account_status`, yang mencatat keputusan Anda sendiri tentang akun tersebut.

Anthropic dapat menambahkan nilai baru. Perlakukan `enforcement_status` yang tidak Anda kenali sebagai `restricted`, `type` yang tidak Anda kenali sebagai `restriction`, `reason` yang tidak Anda kenali sebagai `unspecified`, dan `action` yang tidak Anda kenali sebagai `null`.

Di Claude Platform on AWS, kedua field tersebut tidak melaporkan tindakan penegakan: `enforcement_status` selalu `unrestricted`, dan `enforcement_actions` selalu kosong. Anthropic tidak menolak permintaan di sana karena adanya tindakan yang terbuka.

## Jaga profil tetap terkini

Perbarui profil ketika detail atau status akun pelanggan akhir berubah, dan hapus profil ketika mereka menutup akun atau meminta Anda menghapus data mereka.

### Perbarui profil

[`POST /v1/user_profiles/{id}`](https://platform.claude.com/docs/id/api/user_profiles/update) hanya mengubah field yang Anda kirim. Misalnya, gunakan ini ketika perusahaan melakukan rebranding atau Anda menangguhkan akun.

* `name` dan `access_type` menggantikan nilai yang tersimpan.
* Setiap field yang Anda kirim di `external_user_details` menggantikan nilai yang tersimpan. Anda tidak dapat mengosongkan nilai. API menolak `null` dengan `400`.
* `metadata` digabungkan per kunci. Kunci yang Anda kirim menimpa nilai yang tersimpan, string kosong menghapus kunci tersebut, dan kunci yang tidak Anda kirim tetap seperti semula.

Contoh berikut menandai akun sebagai ditangguhkan dan menghapus kunci metadata `trial_cohort`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/user_profiles/$PROFILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "external_user_details": {"account_status": "suspended"},
      "metadata": {"trial_cohort": ""}
    }'
  ```

  ```bash CLI
  ant user-profiles update \
    --user-profile-id "$PROFILE_ID" \
    --external-user-details '{account_status: suspended}' \
    --metadata '{trial_cohort: ""}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  profile = client.user_profiles.update(
      profile_id,
      external_user_details={"account_status": "suspended"},
      metadata={"trial_cohort": ""},
  )

  print(profile)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const profile = await client.userProfiles.update(profileId, {
    external_user_details: { account_status: "suspended" },
    metadata: { trial_cohort: "" }
  });

  console.log(profile);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var profile = await client.UserProfiles.Update(profileId, new()
  {
      ExternalUserDetails = new()
      {
          AccountStatus = UserProfileExternalUserAccountStatus.Suspended
      },
      Metadata = new Dictionary<string, string> { ["trial_cohort"] = "" }
  });

  Console.WriteLine(profile);
  ```

  ```go Go
  client := anthropic.NewClient()

  profile, err := client.UserProfiles.Update(
  	context.Background(),
  	profileID,
  	anthropic.UserProfileUpdateParams{
  		ExternalUserDetails: anthropic.UserProfileExternalUserDetailsParams{
  			AccountStatus: anthropic.UserProfileExternalUserAccountStatusSuspended,
  		},
  		Metadata: map[string]string{"trial_cohort": ""},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(profile)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.userprofiles.UserProfileExternalUserAccountStatus;
  import com.anthropic.models.userprofiles.UserProfileExternalUserDetailsParams;
  import com.anthropic.models.userprofiles.UserProfileUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserProfileUpdateParams.builder()
          .userProfileId(profileId)
          .externalUserDetails(UserProfileExternalUserDetailsParams.builder()
              .accountStatus(UserProfileExternalUserAccountStatus.SUSPENDED)
              .build())
          .metadata(UserProfileUpdateParams.Metadata.builder()
              .putAdditionalProperty("trial_cohort", JsonValue.from(""))
              .build())
          .build();
      var profile = client.userProfiles().update(params);

      IO.println(profile);
  }
  ```

  ```php PHP
  $client = new Client();

  $profile = $client->userProfiles->update(
      $profileId,
      externalUserDetails: ['accountStatus' => 'suspended'],
      metadata: ['trial_cohort' => ''],
  );

  echo json_encode($profile, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  profile = client.user_profiles.update(
    profile_id,
    external_user_details: { account_status: :suspended },
    metadata: { trial_cohort: "" }
  )

  puts profile
  ```
</CodeGroup>

### Hapus profil

[`DELETE /v1/user_profiles/{id}`](https://platform.claude.com/docs/id/api/user_profiles/delete) menghapus profil secara permanen beserta semua yang Anda berikan untuknya, termasuk `name`, `external_user_details`, dan `metadata`. Tindakan ini tidak menghapus catatan kepercayaan dan keamanan yang disimpan Anthropic tentang ID profil tersebut.

Hapus profil ketika pelanggan akhir menutup akunnya atau meminta Anda menghapus datanya. Sebelum Anda menghapus profil, berhentilah mengirim ID-nya pada permintaan pelanggan akhir tersebut. Jika pelanggan akhir tetap bersama Anda setelah permintaan penghapusan data, buat profil baru dan beralihlah ke ID-nya. Kemudian hapus profil yang lama.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/user_profiles/$PROFILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant user-profiles delete --user-profile-id "$PROFILE_ID"
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted = client.user_profiles.delete(profile_id)

  print(deleted.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deleted = await client.userProfiles.delete(profileId);

  console.log(deleted.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deleted = await client.UserProfiles.Delete(profileId);

  Console.WriteLine(deleted.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  deleted, err := client.UserProfiles.Delete(
  	context.Background(),
  	profileID,
  	anthropic.UserProfileDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(deleted.ID)
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var deleted = client.userProfiles().delete(profileId);

      IO.println(deleted.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $deleted = $client->userProfiles->delete($profileId);

  echo $deleted->id, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  deleted = client.user_profiles.delete(profile_id)

  puts deleted.id
  ```
</CodeGroup>

Respons mengulang ID dengan `"type": "user_profile_deleted"`. Jika penghapusan mengembalikan error server, coba lagi. `404` pada percobaan ulang berarti penghapusan pertama telah berhasil.

Setelah penghapusan, endpoint profil mengembalikan `404` untuk ID tersebut. Hingga sekitar 10 menit, permintaan inferensi yang membawa ID yang telah dihapus masih dapat berhasil. Setelah itu, [platform yang memeriksa ID pada setiap permintaan](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-each-request) menolak permintaan tersebut dengan `400`. Claude Models on Google Cloud (Google managed) tidak mencari profil, sehingga tetap menerima ID tersebut. Hal yang sama berlaku untuk Amazon Bedrock pada [model yang menerima ID profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud).

## Langkah selanjutnya

Referensi API berisi field, tipe, dan batasan setiap endpoint: [Membuat profil](https://platform.claude.com/docs/id/api/user_profiles/create), [Mengambil profil](https://platform.claude.com/docs/id/api/user_profiles/retrieve), [Memperbarui profil](https://platform.claude.com/docs/id/api/user_profiles/update), [Menghapus profil](https://platform.claude.com/docs/id/api/user_profiles/delete), dan [Mencantumkan profil](https://platform.claude.com/docs/id/api/user_profiles/list).

Jika persetujuan program pelanggan akhir harus berlaku ketika mereka menggunakan Claude melalui platform Anda, lihat [Kirim tautan ke Verification Portal kepada pelanggan akhir](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal).

Untuk menagihkan permintaan suatu profil ke organisasi Claude milik pelanggan tersebut, lihat [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections).

Untuk mendapatkan event saat Anthropic membatasi atau memblokir salah satu pelanggan akhir Anda, atau saat pembatasan atau pemblokiran tersebut berakhir, lihat [Webhook organisasi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks).

<CardGroup cols={2}>
  <Card title="Autentikasi" href="https://platform.claude.com/docs/id/manage-claude/authentication">
    Pilih cara layanan Anda melakukan autentikasi ke Claude API.
  </Card>

  <Card title="Usage and Cost Analytics API" href="https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api">
    Lacak penggunaan token dan biaya untuk organisasi Anda.
  </Card>

  <Card title="Residensi data" href="https://platform.claude.com/docs/id/manage-claude/data-residency">
    Kelola tempat inferensi model dijalankan dan tempat data disimpan.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-api">
    Audit aktivitas di seluruh organisasi Anda.
  </Card>
</CardGroup>
