---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal
fetched_at: 2026-10-23T02:21:28.653315Z
sha256: b5de1ba373b681adb90e489a492e914b827ff345fa8e16f18d085b5b8a87bcd1
---

---
title: Kirim tautan ke Verification Portal kepada pelanggan akhir
url: https://platform.claude.com/docs/id/manage-claude/user-profiles-verification-portal
description: Buat tautan pendaftaran untuk profil pengguna, lihat apa yang dilakukan pelanggan akhir Anda di Verification Portal, dan periksa program mana yang berlaku untuk profil tersebut setelahnya.
---

Anthropic menjalankan program yang permohonannya dapat diajukan oleh sebuah organisasi di Verification Portal. Agar persetujuan "end customer" (pelanggan akhir) berlaku saat mereka menggunakan Claude melalui platform Anda, pelanggan akhir menautkan "user profile" (profil pengguna) mereka ke organisasi Anthropic milik mereka sendiri di portal. Anda yang memulai prosesnya: buat "enrollment link" (tautan pendaftaran) untuk profil tersebut dan berikan kepada pelanggan akhir.

Profil pengguna memberi tahu Anthropic untuk pelanggan akhir mana setiap permintaan API ditujukan. Anda membuat satu profil untuk setiap pelanggan akhir dan mengirimkan ID `uprof_`-nya pada setiap permintaan yang Anda buat untuk mereka. Profil harus sudah ada sebelum Anda dapat membuat tautan untuknya. Untuk membuatnya, lihat [Profil pengguna untuk atribusi pelanggan akhir](https://platform.claude.com/docs/id/manage-claude/user-profiles).

Anda dapat melewati halaman ini jika Anda hanya memerlukan atribusi, atau jika pembuatan tautan pendaftaran tidak diaktifkan untuk organisasi Anda.

## Membuat tautan

Untuk membuat tautan pendaftaran untuk sebuah profil, panggil [`POST /v1/user_profiles/{id}/action_urls`](https://platform.claude.com/docs/id/api/user_profiles/action_urls/create) dengan ID profil tersebut di path. Di badan permintaan, atur `action.type` ke `enroll_end_user`.

Panggilan ini mengembalikan `404` jika pembuatan tautan pendaftaran tidak diaktifkan untuk organisasi Anda. Status tersebut sama dengan status untuk ID profil yang tidak dapat ditemukan, jadi periksa ID terlebih dahulu.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles/uprof_011CZkZCu8hGbp5mYRQgUmz9/action_urls \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"action": {"type": "enroll_end_user"}}'
  ```

  ```bash CLI
  ant user-profiles:action-urls create \
    --user-profile-id uprof_011CZkZCu8hGbp5mYRQgUmz9 \
    --action '{type: enroll_end_user}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  action_url = client.user_profiles.action_urls.create(
      "uprof_011CZkZCu8hGbp5mYRQgUmz9",
      action={"type": "enroll_end_user"},
  )

  print(action_url.url)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const actionURL = await client.userProfiles.actionURLs.create(
    "uprof_011CZkZCu8hGbp5mYRQgUmz9",
    { action: { type: "enroll_end_user" } }
  );

  console.log(actionURL.url);
  ```

  ```csharp C#
  using Anthropic.Models.UserProfiles.ActionUrls;

  AnthropicClient client = new();

  var actionUrl = await client.UserProfiles.ActionUrls.Create(
      "uprof_011CZkZCu8hGbp5mYRQgUmz9",
      new() { Action = new UserProfileEnrollEndUserAction() }
  );

  Console.WriteLine(actionUrl.Url);
  ```

  ```go Go
  client := anthropic.NewClient()

  actionURL, err := client.UserProfiles.ActionURLs.New(
  	context.Background(),
  	"uprof_011CZkZCu8hGbp5mYRQgUmz9",
  	anthropic.UserProfileActionURLNewParams{
  		Action: anthropic.UserProfileActionUnionParam{
  			OfEnrollEndUser: &anthropic.UserProfileEnrollEndUserActionParam{},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(actionURL.URL)
  ```

  ```java Java
  import com.anthropic.models.userprofiles.actionurls.ActionUrlCreateParams;
  import com.anthropic.models.userprofiles.actionurls.UserProfileEnrollEndUserAction;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ActionUrlCreateParams.builder()
          .userProfileId("uprof_011CZkZCu8hGbp5mYRQgUmz9")
          .action(UserProfileEnrollEndUserAction.builder().build())
          .build();
      var actionUrl = client.userProfiles().actionUrls().create(params);

      IO.println(actionUrl.url());
  }
  ```

  ```php PHP
  $client = new Client();

  $actionURL = $client->userProfiles->actionURLs->create(
      'uprof_011CZkZCu8hGbp5mYRQgUmz9',
      action: ['type' => 'enroll_end_user'],
  );

  echo $actionURL->url, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  action_url = client.user_profiles.action_urls.create(
    "uprof_011CZkZCu8hGbp5mYRQgUmz9",
    action: { type: :enroll_end_user }
  )

  puts action_url.url
  ```
</CodeGroup>

Respons berisi tautan dan waktu tautan tersebut berhenti berfungsi:

```json
{
  "type": "user_profile_action_url",
  "url": "https://portal.anthropic.com/enroll?enrollment_token=...",
  "expires_at": "2026-03-15T11:00:00Z"
}
```

Tautan berfungsi hingga waktu yang tercantum di `expires_at`, sekitar satu jam setelah Anda membuatnya. Buat tautan saat pelanggan akhir memintanya, misalnya saat mereka mengklik tombol di produk Anda, bukan jauh sebelumnya dalam email yang mungkin baru mereka baca nanti. Mereka dapat membuka tautan lebih dari sekali hingga tautan kedaluwarsa. Jika sudah kedaluwarsa, buat tautan baru: setiap panggilan mengembalikan tautan baru. Membuat tautan baru tidak membatalkan tautan sebelumnya.

Siapa pun yang memiliki tautan dapat menggunakannya hingga kedaluwarsa, jadi berikan hanya kepada pelanggan akhir yang dituju. Kirimkan kepada admin atau pemilik organisasi Anthropic pelanggan akhir, karena hanya admin atau pemilik yang dapat menautkan profil. Jangan mengurai URL atau membuatnya sendiri. Formatnya dapat berubah.

Jika Anda menggunakan Claude Platform on AWS, buat tautan dengan `POST /v1/user_profiles/{id}/enrollment_url` sebagai gantinya, dan kirimkan header `anthropic-beta: user-profiles-2026-08-18`. Permintaan tersebut tidak menerima body, dan responsnya memiliki field `url` dan `expires_at` yang sama. Di SDK dan CLI, panggilan tersebut berada di namespace beta: `client.beta.user_profiles.create_enrollment_url()` (typescript: `client.beta.userProfiles.createEnrollmentURL()`; csharp: `client.Beta.UserProfiles.CreateEnrollmentUrl()`; go: `client.Beta.UserProfiles.NewEnrollmentURL()`; java: `client.beta().userProfiles().createEnrollmentUrl()`; php: `$client->beta->userProfiles->createEnrollmentURL()`; cli: `ant beta:user-profiles create-enrollment-url`).

`POST /v1/user_profiles/{id}/action_urls` tidak tersedia di Microsoft Foundry.

## Apa yang dilihat pelanggan akhir

Tautan membuka Verification Portal milik Anthropic di `portal.anthropic.com`. Setelah pelanggan akhir masuk, portal menampilkan nama organisasi Anthropic Anda dan ID profil.

<Steps>
  <Step title="Masuk">
    Pelanggan akhir masuk dengan akun Anthropic: akun yang sudah mereka gunakan untuk Claude Console atau claude.ai, atau akun baru yang mereka buat pada langkah ini. Portal menyimpan sesi login-nya sendiri, terpisah dari Claude Console dan claude.ai. Jika mereka tergabung dalam lebih dari satu organisasi, mereka memilih organisasi yang akan ditautkan.

    <Frame caption="Sebelum masuk, pelanggan akhir melihat alasan mereka diarahkan ke portal.">
      ![Kartu Verification Portal berjudul Link your account to apply for trusted access, dengan tombol Continue to log in.](https://platform.claude.com/docs/images/user-profiles/portal-log-in.png)
    </Frame>
  </Step>

  <Step title="Menautkan profil">
    Portal menampilkan kartu berjudul **Link your partner profile**. Kartu ini menyebutkan platform Anda, ID profil, organisasi pelanggan akhir, dan kapan undangan kedaluwarsa. Pelanggan akhir memilih **Link profile** untuk menerima atau **Skip for now** untuk melanjutkan ke portal tanpa menautkan.

    <Frame caption="Pelanggan akhir mengonfirmasi ke organisasi mana profil tersebut ditautkan.">
      ![Kartu Verification Portal berjudul Link your partner profile, yang menampilkan partner, ID profil, organisasi, dan waktu kedaluwarsa.](https://platform.claude.com/docs/images/user-profiles/portal-link-profile.png)
    </Frame>

    Hanya admin atau pemilik organisasi yang dapat menautkan profil. Orang lain akan melihat **Admin access needed** dan tidak dapat menautkan profil. Mereka dapat beralih ke organisasi tempat mereka menjadi admin atau pemilik. Jika tidak, beri tahu pelanggan akhir bahwa admin atau pemilik organisasi Anthropic mereka harus membuka tautan tersebut.
  </Step>

  <Step title="Melihat konfirmasi">
    Portal mengonfirmasi dengan **Profile linked**. Pelanggan akhir tetap berada di portal, tempat mereka dapat melihat program yang tersedia untuk organisasi mereka dan mengajukan permohonan ke program tersebut.

    <Frame caption="Setelah penautan, pelanggan akhir tetap berada di portal.">
      ![Konfirmasi Verification Portal berjudul Profile linked, dengan tombol View programs dan View linked accounts.](https://platform.claude.com/docs/images/user-profiles/portal-profile-linked.png)
    </Frame>
  </Step>
</Steps>

Jika tautan sudah kedaluwarsa saat admin atau pemilik membukanya dan masuk, portal menampilkan **This invitation has expired** dan meminta mereka untuk meminta tautan baru kepada Anda.

Sebuah profil ditautkan ke satu organisasi. Jika profil sudah ditautkan ke organisasi lain, portal menampilkan **This partner profile is already linked to a different organization** dan tidak menautkannya. Admin atau pemilik organisasi tempat profil tersebut ditautkan dapat membatalkan penautannya di bawah **Linked accounts** di portal. Setelah itu, buat tautan baru dan kirimkan kepada pelanggan akhir.

## Setelah pelanggan akhir menautkan profil

Portal tidak mengarahkan pelanggan akhir kembali ke produk Anda, dan Anthropic tidak memberi tahu Anda. Beri tahu pelanggan akhir di antarmuka Anda sendiri untuk kembali setelah mereka selesai.

Penautan tidak menyetujui apa pun dengan sendirinya. Penautan menghubungkan profil ke organisasi pelanggan akhir, sehingga program yang telah disetujui untuk organisasi tersebut berlaku untuk permintaan yang membawa ID profil, kecuali tingkat akses Cyber Verification Program, yang diaktifkan oleh pelanggan akhir untuk setiap profil tertaut di portal. Profil tidak memiliki field yang menyatakan bahwa profil tersebut tertaut.

Untuk melihat program mana yang berlaku untuk sebuah profil, [ambil profil tersebut](https://platform.claude.com/docs/id/api/user_profiles/retrieve) dan baca `programs`. Field ini memiliki key untuk setiap program, seperti `cyber` dan `efs`, dan setiap profil memiliki semua key tersebut. Setiap key berisi salah satu dari berikut ini:

* `null`: Anthropic tidak memiliki status untuk dilaporkan bagi program tersebut. Setiap key bernilai `null` jika Anthropic belum mengaktifkan program untuk organisasi Anda.
* Sebuah objek: `status`-nya adalah `active` ketika program berlaku untuk profil, jika tidak maka `pending` atau `rejected`.

Pelanggan akhir dapat melihat profil yang ditautkan di bawah **Linked accounts** di portal.

Jika inferensi Anda berjalan di Claude di Amazon Bedrock atau Claude Models on Google Cloud (Google managed), Anda juga harus menautkan akun Anda sendiri. Program berlaku untuk permintaan dari akun AWS atau proyek Google Cloud hanya setelah Anda menautkannya ke organisasi Anthropic yang membuat profil Anda. Lihat [Atribusikan permintaan di Amazon Bedrock dan Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/manage-claude/user-profiles#attribute-requests-on-amazon-bedrock-and-google-cloud).

## Langkah selanjutnya

Untuk setiap field yang terdapat dalam profil yang diambil, lihat referensi [Retrieve a profile](https://platform.claude.com/docs/id/api/user_profiles/retrieve).

Untuk membuat profil, mengirimkan ID-nya pada permintaan Anda, dan menjaganya tetap terkini, lihat [Profil pengguna untuk atribusi pelanggan akhir](https://platform.claude.com/docs/id/manage-claude/user-profiles).
