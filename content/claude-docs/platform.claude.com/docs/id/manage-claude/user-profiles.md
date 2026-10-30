---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-profiles
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 7fd45819fa33e331aec79800eaa1b90a0fa85008e690b6f2ba06baf1481843f9
---

---
title: Profil pengguna untuk atribusi pelanggan akhir
url: https://platform.claude.com/docs/id/manage-claude/user-profiles
description: Atribusikan permintaan API ke pelanggan akhir yang dilayani platform Anda, sehingga tindakan penegakan keamanan dapat diterapkan pada satu profil alih-alih seluruh organisasi Anda.
---

Profil pengguna (“profil”) memberi tahu Anthropic untuk pelanggan akhir mana setiap permintaan API ditujukan. Tindakan penegakan keamanan, seperti pembatasan atau pemblokiran, kemudian dapat diterapkan pada satu pelanggan akhir alih-alih pada seluruh organisasi Anda. Ketika hal itu terjadi, lalu lintas Anda yang lain tidak terpengaruh.

Jika Anda mengoperasikan platform atau gateway, atau menjual kembali akses API, permintaan yang Anda kirim untuk pelanggan akhir Anda tiba di bawah organisasi Anda. Anthropic menjalankan “safety classifier” (pengklasifikasi keamanan) otomatis pada lalu lintas API. Tanpa profil pada permintaan, satu pelanggan akhir dapat memicu tindakan penegakan yang berlaku untuk seluruh organisasi Anda.

Anda mendaftarkan setiap pelanggan akhir satu kali dengan `POST /v1/user_profiles` dan menyimpan ID `uprof_` yang dikembalikannya. Kemudian Anda mengirim ID tersebut di header `anthropic-user-profile-id` pada setiap permintaan yang Anda buat atas nama pelanggan akhir tersebut.

Profil tidak dikenakan biaya dan tidak memengaruhi harga.

## Tentukan siapa yang mendapatkan profil

Apa yang diwakili oleh sebuah profil bergantung pada cara Anda menjual Claude: seseorang yang menggunakan produk Anda, atau perusahaan tempat Anda menjual kembali akses API. Kedua kasus ini mencakup sebagian besar platform. Field `access_type` pada profil menyatakan kasus mana yang berlaku.

| Untuk siapa lalu lintas tersebut                                           | Profil                                                                                                                                                                                                                                | `access_type`                                                             |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Pengguna terdaftar produk Anda                                             | Satu untuk setiap pengguna, dibuat saat mereka mendaftar.                                                                                                                                                                             | `application` (default, ditetapkan saat Anda menghilangkan `access_type`) |
| Perusahaan tempat Anda menjual kembali akses API, misalnya sebagai gateway | Satu untuk setiap perusahaan, bukan untuk setiap orang di dalamnya.                                                                                                                                                                   | `passthrough` (bukan default, sehingga Anda harus mengirimkannya)         |
| Organisasi Anda sendiri                                                    | Tidak ada. Anthropic menghitung permintaan tanpa ID profil sebagai penggunaan Anda sendiri. Tempatkan penggunaan tersebut di [organisasi terpisah](https://platform.claude.com/docs/id/manage-claude/user-profiles#before-you-begin). | Tidak berlaku                                                             |
| Workspace di organisasi Anda                                               | Tidak ada profil terpisah. Profil dimiliki oleh organisasi Anda, dan ID-nya berfungsi pada permintaan melalui workspace mana pun di dalamnya.                                                                                         | Tidak berlaku                                                             |

## Apa isi profil dan bagaimana Anthropic menggunakannya

Profil hanya berisi apa yang Anda kirim tentang pelanggan akhir, ditambah [status program](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal#after-the-end-customer-links-the-profile) atau status penegakan apa pun yang ditetapkan Anthropic. Profil tidak berisi konten percakapan. Anthropic menggunakan detail yang Anda kirim untuk mengatribusikan permintaan, memantau penyalahgunaan, menegakkan [Kebijakan Penggunaan](https://www.anthropic.com/legal/aup), serta memungkinkan pengajuan dan akses ke program akses tepercaya. Anthropic tidak memverifikasi detail tersebut.

Anthropic memproses profil sesuai dengan [Kebijakan Privasi](https://www.anthropic.com/legal/privacy).

## Sebelum Anda memulai

Anda membuat dan mengelola profil di salah satu dari berikut ini:

* Organisasi di Claude API.
* Organisasi di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Principal yang memanggil memerlukan [tindakan IAM profil pengguna](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#user-profiles).
* Deployment [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) yang [di-hosting di Anthropic](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry#hosting-options), bukan yang di-hosting di Azure. Anda tidak memerlukan organisasi di Claude API atau Claude Platform on AWS. Gunakan endpoint Foundry Anda, dengan base URL dan autentikasi yang sama dengan yang Anda gunakan untuk inferensi.
* Organisasi di [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), tempat Anda dapat membuat, mengambil, mencantumkan, dan memperbarui profil. Gunakan versi terbaru [klien SDK untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#install-an-sdk), atau panggil [base URL tingkat organisasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#making-requests) secara langsung, dengan kredensial Google Cloud alih-alih kunci API.

Amazon Bedrock dan Claude Models on Google Cloud (Google managed) tidak memiliki endpoint `/v1/user_profiles`. Jika inferensi Anda berjalan di sana, buat profil Anda di organisasi di Claude API atau Claude Platform on AWS. Di Amazon Bedrock, profil hanya berfungsi dengan [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock). Lihat [Atribusikan permintaan di Amazon Bedrock dan Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud).

Tempatkan lalu lintas yang Anda kirim untuk pelanggan akhir Anda di satu organisasi dan penggunaan internal Anda sendiri di organisasi lain. Profil dimiliki oleh organisasi, bukan workspace, sehingga workspace terpisah dalam satu organisasi tidak cukup. Hanya organisasi untuk lalu lintas pelanggan akhir yang memerlukan profil pengguna. Untuk membuat organisasi lain di Claude API, lihat bagian “How to create a new organization” dari [Creating and managing Workspaces in the Claude Console](https://support.claude.com/en/articles/9796807) di Claude Help Center.

Contoh-contoh ini memanggil Claude API dengan kunci API. Anda tidak memerlukan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys). Di Claude Platform on AWS, gunakan base URL dan autentikasinya.

## Buat profil untuk setiap pelanggan akhir

Buat satu profil untuk setiap pelanggan akhir yang lalu lintasnya Anda kirim ke Claude. Buat sekali saja, dalam alur onboarding pelanggan Anda. `POST /v1/user_profiles` tidak “idempotent” (idempoten), sehingga setiap panggilan membuat profil baru, bahkan ketika `reference_id` cocok dengan profil yang sudah ada. Jika Anda sudah memiliki pelanggan akhir tanpa profil, lihat panduan nanti di bagian ini tentang mendaftarkan basis pelanggan yang sudah ada.

Contoh berikut mendaftarkan perusahaan yang membeli akses API melalui gateway, sehingga menetapkan `access_type` ke `passthrough`. Untuk profil `application`, hilangkan `access_type`, dan deskripsikan satu pengguna akhir di `name` dan `external_user_details` alih-alih perusahaan. [Tentukan siapa yang mendapatkan profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#decide-who-gets-a-profile) membandingkan kedua jenis akses tersebut.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
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

Setiap field bersifat opsional. Anda dapat mengirim `name`, `metadata`, dan field-field berikut di `external_user_details`: `entity_type`, `country`, `reference_id`, `onboarded_at`, `account_status`, `name_hash`, dan `email_hash`. Referensi [Create a profile](https://platform.claude.com/docs/id/api/user_profiles/create) menjelaskan setiap field, beserta tipe, format, dan batas panjangnya.

Ikuti aturan berikut saat Anda menetapkan field:

* **Nilai yang tidak diketahui:** Jika Anda tidak mengetahui suatu nilai, hilangkan alih-alih mengirim placeholder. Anda dapat mengganti nilai di `external_user_details` nanti, tetapi Anda tidak dapat mengosongkannya.
* **Nama perusahaan:** Untuk profil `passthrough`, kirim nama resmi perusahaan di `name` jika Anda mengetahuinya.
* **Negara:** Di `country`, kirim negara pelanggan akhir, bukan negara Anda.
* **ID Anda sendiri:** Di `reference_id`, kirim pengidentifikasi stabil Anda sendiri untuk pelanggan akhir. Nilai ini tidak harus unik.
* **Nama dan alamat email yang tidak dapat Anda bagikan:** Hilangkan `name` dan kirim `external_user_details.name_hash` sebagai gantinya. Untuk alamat email, kirim `external_user_details.email_hash`. Profil tidak memiliki field untuk alamat itu sendiri.
* **Hash:** Hitung hash sendiri, dengan fungsi yang Anda pilih. Hash menunjukkan kepada Anthropic profil mana milik Anda yang memiliki nama atau alamat email yang sama. Gunakan fungsi yang sama serta normalisasi huruf besar-kecil dan spasi yang sama untuk setiap profil, karena hanya nilai yang dihitung dengan cara yang sama yang akan cocok.

## Atribusikan setiap permintaan

Kirim ID profil di header `anthropic-user-profile-id` pada setiap permintaan yang Anda buat atas nama pelanggan akhir. SDK dan CLI memiliki argumen yang mengirimkan header tersebut untuk Anda: `user_profile_id` (java: `userProfileId`; php: `userProfileID`; csharp, go: `UserProfileID`; cli: `--user-profile-id`).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
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

Claude API, Claude Platform on AWS, deployment Microsoft Foundry yang di-hosting di Anthropic, dan Claude Models on Google Cloud (Anthropic managed) memeriksa ID pada setiap permintaan. Jika ID tidak valid formatnya atau bukan milik organisasi yang mengirim permintaan, API mengembalikan `400` `invalid_request_error`. Secara default, platform-platform ini hanya menerima ID profil pada permintaan dari organisasi yang membuat profil tersebut. Ini berarti bahwa jika Anda mengirim lalu lintas di bawah lebih dari satu organisasi, misalnya satu di Claude API dan satu di Claude Platform on AWS, permintaan dari organisasi yang tidak membuat profil tersebut akan mendapatkan `400` yang sama.

Message Batches adalah pengecualian: pembuatan batch hanya memeriksa format ID. Jika ID yang formatnya valid bukan milik organisasi yang mengirim batch, batch tetap dibuat, dan setiap permintaan di dalamnya kemudian gagal dengan hasil `errored` yang berisi `invalid_request_error` yang sama.

### Atribusikan permintaan di Amazon Bedrock dan Claude Models on Google Cloud (Google managed)

ID profil dari kedua jenis akses juga berfungsi di [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan di Claude Models on Google Cloud (Google managed). ID ini tidak berfungsi dengan [integrasi Amazon Bedrock sebelumnya](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) yang Anda panggil dengan `InvokeModel` atau `Converse`. Anda menggunakan kredensial organisasi Anthropic Anda hanya untuk membuat dan mengelola profil. Inferensi tetap menggunakan kredensial AWS atau Google Cloud Anda yang sudah ada.

| Platform                                                                                                                                                   | Membuat profil                                         | Kirim ID profil di                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------ |
| Claude API                                                                                                                                                 | Ya                                                     | Header `anthropic-user-profile-id`         |
| [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                                                     | Ya                                                     | Header `anthropic-user-profile-id`         |
| [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), deployment yang di-hosting di Anthropic            | Ya                                                     | Header `anthropic-user-profile-id`         |
| [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | Ya                                                     | Header `anthropic-user-profile-id`         |
| [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)       | Tidak. Buat di Claude API atau Claude Platform on AWS. | Header `anthropic-user-profile-id`         |
| [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)                                                 | Tidak. Buat di Claude API atau Claude Platform on AWS. | Field `user_profile_id` di body permintaan |

Di Claude di Amazon Bedrock, letakkan ID di tingkat teratas body permintaan:

```json
{
  "model": "anthropic.claude-opus-5-5",
  "max_tokens": 1024,
  "user_profile_id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
  "messages": [{ "role": "user", "content": "Hello, Claude" }]
}
```

Tautkan setiap akun AWS yang mengirim permintaan ke Claude di Amazon Bedrock, dan setiap proyek Google Cloud yang mengirim permintaan ke Claude Models on Google Cloud (Google managed), ke organisasi Anthropic yang membuat profil Anda:

1. Admin atau pemilik organisasi tersebut memulai penautan di Verification Portal di `portal.anthropic.com`, di bawah **Linked accounts**.
2. Seseorang yang dapat mengelola IAM di akun AWS atau proyek Google Cloud menjalankan perintah yang disediakan portal.
3. Admin atau pemilik menyelesaikan verifikasi di portal.

Program yang berlaku untuk sebuah profil hanya berlaku untuk permintaan sebuah akun setelah akun tersebut ditautkan dan portal menampilkannya sebagai **Linked**. Program-program tersebut mencakup program yang disetujui untuk organisasi pelanggan akhir setelah pelanggan akhir [menautkan profil ke organisasi tersebut](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal) dan, untuk tingkat akses Cyber Verification Program, mengaktifkannya untuk profil tersebut di portal.

Claude di Amazon Bedrock dan Claude Models on Google Cloud (Google managed) memeriksa format ID tetapi tidak mencari profilnya. Keduanya menolak ID yang formatnya tidak valid dengan `400`. Keduanya menerima ID apa pun yang formatnya valid, sehingga respons yang berhasil tidak mengonfirmasi bahwa ID tersebut cocok dengan sebuah profil. Permintaan tanpa ID diproses tanpa atribusi, dan jika memicu tindakan penegakan, tindakan tersebut berlaku untuk seluruh organisasi Anda.

### Identifikasi pengguna individual dalam sebuah perusahaan

Profil `passthrough` mengidentifikasi perusahaan, bukan orang yang membuat permintaan. Jika permintaan berasal dari satu orang yang dapat diidentifikasi, kirim juga pengidentifikasi untuk orang tersebut di field [`metadata.user_id`](https://platform.claude.com/docs/id/api/messages/create) pada permintaan Messages. Ini adalah objek `metadata` milik permintaan itu sendiri, bukan field `metadata` milik profil. Pengidentifikasi ini opsional, dan membantu Anthropic mendeteksi penyalahgunaan oleh satu orang.

## Memeriksa apakah Anthropic telah membatasi atau memblokir sebuah profil

Field `enforcement_status` dan `enforcement_actions` pada sebuah profil melaporkan tindakan penegakan yang sedang dibuka Anthropic terhadap pelanggan akhir. Tindakan penegakan adalah pembatasan atau pemblokiran. Setiap respons yang mengembalikan profil menyertakan kedua field tersebut: create, retrieve, update, dan setiap profil dalam daftar. Kirim permintaan ini tanpa nilai `user-profiles-` di header `anthropic-beta`, karena `user-profiles-2026-09-04` dan nilai-nilai sebelumnya tidak menyertakan field tersebut. Contoh berikut menunjukkan field tersebut pada profil yang diambil, dengan field lainnya dihilangkan:

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
    -H "anthropic-version: 2023-06-01" \
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
    -H "anthropic-version: 2023-06-01"
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

Setelah penghapusan, endpoint profil mengembalikan `404` untuk ID tersebut. Hingga sekitar 10 menit, permintaan inferensi yang membawa ID yang telah dihapus masih dapat berhasil. Setelah itu, platform yang memeriksa ID pada setiap permintaan menolak permintaan tersebut dengan `400`. Claude di Amazon Bedrock dan Claude Models on Google Cloud (Google managed) tidak mencari profil, sehingga keduanya tetap menerimanya.

## Langkah selanjutnya

Referensi API berisi field, tipe, dan batasan setiap endpoint: [Membuat profil](https://platform.claude.com/docs/id/api/user_profiles/create), [Mengambil profil](https://platform.claude.com/docs/id/api/user_profiles/retrieve), [Memperbarui profil](https://platform.claude.com/docs/id/api/user_profiles/update), [Menghapus profil](https://platform.claude.com/docs/id/api/user_profiles/delete), dan [Mencantumkan profil](https://platform.claude.com/docs/id/api/user_profiles/list).

Jika persetujuan program pelanggan akhir harus berlaku ketika mereka menggunakan Claude melalui platform Anda, lihat [Kirim tautan ke Verification Portal kepada pelanggan akhir](https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal).

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
