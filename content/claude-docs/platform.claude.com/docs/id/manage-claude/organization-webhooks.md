---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/organization-webhooks
fetched_at: 2026-10-22T02:21:21.745661Z
sha256: 1ac37c3ededdfdfca3e3e671cf7e08988721ef8437314235bbb2b987632eee2a
---

---
title: Webhook organisasi
url: https://platform.claude.com/docs/id/manage-claude/organization-webhooks
description: Daftarkan endpoint webhook untuk event tentang tindakan penegakan pada profil pengguna organisasi Anda.
featureMetadata:
  status: beta
  betaHeader: webhooks-2026-10-07
  supportedPlatforms:
    Claude API: beta
---

Endpoint webhook organisasi menerima sebuah event ketika Anthropic membatasi atau memblokir salah satu [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) organisasi Anda, dan ketika pembatasan atau pemblokiran tersebut berakhir. Anda mengelolanya dengan Admin API di bawah `/v1/organizations/webhooks`.

<Note>
  Pengiriman event belum aktif: Anthropic tidak mengirimkan kedua event tersebut, sehingga endpoint yang Anda daftarkan tidak menerima apa pun. Anda dapat mendaftarkan endpoint dan membangun handler Anda berdasarkan format event di halaman ini.
</Note>

Setiap anggota organisasi Anda dapat menampilkan daftar endpoint webhook organisasi dan melihatnya dengan API, tetapi hanya anggota dengan peran admin, owner, atau primary owner yang dapat membuat, mengubah, atau menghapusnya, atau mengganti signing secret-nya.

## Sebelum Anda memulai

Anda memerlukan hal-hal berikut:

* Organisasi di Claude API yang webhook organisasinya telah diaktifkan dan yang tidak mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness). Untuk meminta akses, hubungi tim akun Anthropic Anda.

* Salah satu kredensial berikut:

  * [Kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).
  * [Token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan scope `org:admin`.
  * [Kunci pribadi atau kunci akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) yang tidak dibatasi pada sebuah workspace.

## Jenis event

Endpoint webhook organisasi menerima dua jenis event. Keduanya berkaitan dengan ["enforcement action" (tindakan penegakan)](https://platform.claude.com/docs/id/manage-claude/user-profiles#check-whether-anthropic-has-restricted-or-banned-a-profile) pada profil pengguna.

| Event                                      | Pemicu                                                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `user_profile.enforcement_action_opened`   | Anthropic membuka tindakan penegakan pada sebuah profil pengguna.                                      |
| `user_profile.enforcement_action_resolved` | Sebuah tindakan penegakan berakhir. Anthropic menyelesaikannya, atau waktu `expires_at`-nya terlewati. |

Menghapus sebuah profil akan mengakhiri tindakan-tindakan terbukanya tanpa event `user_profile.enforcement_action_resolved`.

### Sebelum event pertama Anda

Dalam setiap permintaan yang header `anthropic-beta`-nya berisi `user-profiles-2026-09-04` atau nilai yang lebih lama, respons tidak menyertakan field `enforcement_status` dan `enforcement_actions`, dan filter daftar `enforcement_status[]` mengembalikan `400`. Untuk mendapatkan field tersebut, hapus nilai itu dari permintaan Anda.

Jika sebuah tindakan penegakan dibuka sebelum Anthropic mengaktifkan pengiriman event untuk organisasi Anda, atau sebelum Anda mendaftarkan endpoint Anda, Anda tidak mendapatkan event `user_profile.enforcement_action_opened` untuknya. Tindakan tersebut tetap muncul pada profil. Untuk menemukan tindakan-tindakan ini, [tampilkan daftar profil Anda](https://platform.claude.com/docs/id/api/user_profiles/list) dengan `enforcement_status[]=restricted` dan `enforcement_status[]=banned`. Sebuah respons mungkin mengembalikan lebih sedikit profil daripada `limit`, atau tidak ada sama sekali, sebelum daftar berakhir, jadi teruslah meminta halaman sampai `next_page` bernilai `null`.

### Isi sebuah event

Event membawa ID, bukan tindakan atau profilnya. `data.id` adalah ID profil, dan `data.enforcement_action_id` adalah ID tindakan, yang diawali dengan `enac_`:

```json
{
  "type": "event",
  "id": "whe_4f2a9c1e7b3d5a8f0e6c2b9d1a7f3e5c",
  "created_at": "2026-10-15T17:02:41Z",
  "data": {
    "type": "user_profile.enforcement_action_opened",
    "id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
    "enforcement_action_id": "enac_011CZkZEq4TnWb7xLfRgPm2v",
    "organization_id": "org_011CZkZBj9RsYd3wNcHvKq6t"
  }
}
```

Untuk melihat apa yang berubah, [ambil profil tersebut](https://platform.claude.com/docs/id/api/user_profiles/retrieve) dengan `GET /v1/user_profiles/{id}` (python, ruby: `client.user_profiles.retrieve()`; typescript: `client.userProfiles.retrieve()`; go: `client.UserProfiles.Get()`; java: `client.userProfiles().retrieve()`; csharp: `client.UserProfiles.Retrieve()`; php: `$client->userProfiles->retrieve()`; cli: `ant user-profiles retrieve`), menggunakan `data.id`. Daftar `enforcement_actions`-nya menunjukkan tindakan-tindakan terbukanya. Setiap tindakan memiliki `type` (`restriction` atau `ban`), `id`, `reason`, waktu `opened_at`, dan waktu `expires_at` atau `null`. `enforcement_status` merangkumnya: `banned` selama ada pemblokiran yang terbuka, `restricted` selama ada tindakan lain yang terbuka, dan `unrestricted` ketika tidak ada. Perlakukan nilai lain apa pun sebagai `restricted`.

Anthropic mengirimkan event hanya setelah profil menunjukkan perubahan tersebut, sehingga profil yang Anda ambil menunjukkan perubahan itu atau perubahan yang lebih baru. Event mungkin tiba terlambat atau tidak berurutan, jadi gunakan status profil saat ini, bukan urutan kedatangan event. Setelah `user_profile.enforcement_action_resolved`, tindakan yang telah diselesaikan tidak lagi ada dalam daftar. `404` berarti profil tersebut telah dihapus.

## Field endpoint

Endpoint webhook organisasi memiliki field-field berikut:

| Field             | Tipe             | Deskripsi                                                                                                                                                                                                        |
| ----------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`              | string           | ID endpoint, yang diawali dengan `wep_`. Ditetapkan oleh Anthropic.                                                                                                                                              |
| `url`             | string           | Tempat Anthropic mengirimkan event. Harus HTTPS pada port 443, dengan nama domain publik, bukan alamat IP. Dua endpoint webhook organisasi yang diaktifkan di organisasi Anda tidak dapat berbagi URL yang sama. |
| `enabled_events`  | array of strings | [Jenis event](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#event-types) yang diterima endpoint ini. Permintaan pembuatan harus mencantumkan setidaknya satu.                          |
| `name`            | string           | Label opsional untuk penggunaan Anda sendiri.                                                                                                                                                                    |
| `description`     | string           | Deskripsi opsional untuk penggunaan Anda sendiri.                                                                                                                                                                |
| `state`           | string           | `enabled` atau `disabled`.                                                                                                                                                                                       |
| `disabled_reason` | string           | Alasan Anthropic menonaktifkan endpoint. Kosong jika tidak.                                                                                                                                                      |
| `created_at`      | string           | Waktu endpoint dibuat. Ditetapkan oleh Anthropic.                                                                                                                                                                |
| `updated_at`      | string           | Waktu endpoint terakhir berubah. Ditetapkan oleh Anthropic.                                                                                                                                                      |
| `signing_secret`  | string           | Secret berawalan `whsec_`, dibuat bersama endpoint. Hanya respons yang membuat endpoint atau mengganti secret yang menyertakannya, jadi simpanlah dengan aman.                                                   |

```json
{
  "id": "wep_011CZkZDf8HnUq2mTxRbVn4s",
  "url": "https://example.com/anthropic-webhooks",
  "name": "Enforcement actions",
  "description": "",
  "enabled_events": [
    "user_profile.enforcement_action_opened",
    "user_profile.enforcement_action_resolved"
  ],
  "state": "enabled",
  "disabled_reason": "",
  "created_at": "2026-10-20T19:00:00Z",
  "updated_at": "2026-10-20T19:00:00Z"
}
```

Sebuah organisasi dapat memiliki hingga 32 endpoint webhook organisasi. Endpoint webhook yang dinonaktifkan tetap dihitung dalam total ini.

## Pengiriman

Pengiriman mengikuti spesifikasi [Standard Webhooks](https://www.standardwebhooks.com/). Setiap pengiriman membawa header `webhook-id`, `webhook-timestamp`, dan `webhook-signature`. Sebelum Anda memercayai sebuah event, verifikasi tanda tangannya dengan signing secret endpoint, menggunakan library Standard Webhooks apa pun.

Kembalikan status `2xx` apa pun dalam 5 detik, dan lakukan pekerjaan yang lambat setelahnya. Respons lain apa pun, atau tidak adanya respons, dihitung sebagai percobaan yang gagal.

* **Duplikat:** Sebuah endpoint mungkin menerima event yang sama lebih dari sekali, dengan `id` event yang sama (nilai yang sama dengan header `webhook-id`). Lakukan deduplikasi berdasarkan nilai tersebut.

* **Percobaan ulang:** Jika pengiriman gagal, Anthropic mencoba ulang pengiriman tersebut beberapa kali selama beberapa menit berikutnya. Jika setiap percobaan gagal, Anthropic membuang event tersebut. Untuk mengejar ketertinggalan, tampilkan daftar profil Anda berdasarkan status penegakan, seperti di [Sebelum event pertama Anda](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#before-your-first-event).

* **Penonaktifan otomatis:** Anthropic menonaktifkan sebuah endpoint ketika:

  * Endpoint mengembalikan redirect (`3xx`).
  * URL-nya di-resolve ke alamat IP non-publik.
  * Pengirimannya terus gagal.

  Anthropic melewati event untuk endpoint yang dinonaktifkan dan tidak mengirimkannya di kemudian hari.

## Mengelola endpoint

Dengan Admin API, Anda dapat membuat permintaan-permintaan berikut:

| Tugas                                                                                    | Permintaan                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Menampilkan daftar endpoint organisasi Anda                                              | [`GET /v1/organizations/webhooks`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/list)                                                                       |
| Membuat endpoint                                                                         | [`POST /v1/organizations/webhooks`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/create)                                                                    |
| Mendapatkan satu endpoint                                                                | [`GET /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/retrieve)                                             |
| Memperbarui `url`, `name`, `description`, `enabled_events`, atau `state` sebuah endpoint | [`POST /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/update)                                              |
| Menghapus endpoint                                                                       | [`DELETE /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/delete)                                            |
| Mengganti signing secret                                                                 | [`POST /v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/regenerate_signing_secret) |

Dalam pembaruan, `enabled_events` menggantikan seluruh daftar jenis event endpoint. Daftar kosong tidak mengosongkan daftar: endpoint tetap mempertahankan jenis event yang dimilikinya. Untuk menghentikan pengiriman, kirim `"state": "disabled"` atau hapus endpoint tersebut.

Untuk mengaktifkan kembali sebuah endpoint, termasuk setelah Anthropic menonaktifkannya, kirim `"state": "enabled"` dalam permintaan pembaruan.

Ketika Anda mengganti signing secret, secret lama langsung berhenti berfungsi. Pengiriman sejak saat itu, termasuk percobaan ulang event sebelumnya, ditandatangani dengan secret baru, jadi segera perbarui penerima Anda.

Kirim header `anthropic-beta: webhooks-2026-10-07` dengan setiap permintaan. SDK dan CLI mengirimkannya untuk Anda. Contoh ini menampilkan daftar endpoint organisasi Anda, menggunakan kunci Admin API dari `ANTHROPIC_API_KEY`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/webhooks" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: webhooks-2026-10-07"
  ```

  ```bash CLI
  ant beta:organization:webhooks list
  ```

  ```python Python
  client = anthropic.Anthropic()

  endpoints = client.beta.organization.webhooks.list()

  for endpoint in endpoints:
      print(f"{endpoint.id}: {endpoint.url} ({endpoint.state})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const endpoints = await client.beta.organization.webhooks.list();

  for await (const endpoint of endpoints) {
    console.log(`${endpoint.id}: ${endpoint.url} (${endpoint.state})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Webhooks.List();

  await foreach (var endpoint in page.Paginate())
  {
      Console.WriteLine($"{endpoint.ID}: {endpoint.Url} ({endpoint.State.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  endpoints := client.Beta.Organization.Webhooks.ListAutoPaging(context.Background(), anthropic.BetaOrganizationWebhookListParams{})

  for endpoints.Next() {
  	endpoint := endpoints.Current()
  	fmt.Printf("%s: %s (%s)\n", endpoint.ID, endpoint.URL, endpoint.State)
  }
  if err := endpoints.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var endpoints = client.beta().organization().webhooks().list();

  for (var endpoint : endpoints.autoPager()) {
      IO.println(endpoint.id() + ": " + endpoint.url() + " (" + endpoint.state().asString() + ")");
  }
  ```

  ```php PHP
  $client = new Client();

  $endpoints = $client->beta->organization->webhooks->list();

  foreach ($endpoints->pagingEachItem() as $endpoint) {
      echo "{$endpoint->id}: {$endpoint->url} ({$endpoint->state})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  endpoints = client.beta.organization.webhooks.list

  endpoints.auto_paging_each do |endpoint|
    puts "#{endpoint.id}: #{endpoint.url} (#{endpoint.state})"
  end
  ```
</CodeGroup>

Tanpa endpoint, API mengembalikan daftar kosong:

```json
{
  "data": [],
  "has_more": false
}
```

Sebuah daftar mengembalikan hingga 20 endpoint secara default. Atur `limit` untuk mendapatkan hingga 100. Jika `has_more` bernilai `true`, teruskan `last_id` dari respons sebagai `after_id` untuk mendapatkan halaman berikutnya.

Contoh ini membuat endpoint yang menerima kedua jenis event:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/webhooks" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: webhooks-2026-10-07" \
    -H "content-type: application/json" \
    -d '{
      "url": "https://example.com/anthropic-webhooks",
      "name": "Enforcement actions",
      "enabled_events": [
        "user_profile.enforcement_action_opened",
        "user_profile.enforcement_action_resolved"
      ]
    }'
  ```

  ```bash CLI
  ant beta:organization:webhooks create \
    --url https://example.com/anthropic-webhooks \
    --name "Enforcement actions" \
    --enabled-event user_profile.enforcement_action_opened \
    --enabled-event user_profile.enforcement_action_resolved
  ```

  ```python Python
  client = anthropic.Anthropic()

  endpoint = client.beta.organization.webhooks.create(
      url="https://example.com/anthropic-webhooks",
      name="Enforcement actions",
      enabled_events=[
          "user_profile.enforcement_action_opened",
          "user_profile.enforcement_action_resolved",
      ],
  )

  print(endpoint.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const endpoint = await client.beta.organization.webhooks.create({
    url: "https://example.com/anthropic-webhooks",
    name: "Enforcement actions",
    enabled_events: [
      "user_profile.enforcement_action_opened",
      "user_profile.enforcement_action_resolved"
    ]
  });

  console.log(endpoint.id);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Webhooks;

  AnthropicClient client = new();

  var endpoint = await client.Beta.Organization.Webhooks.Create(new WebhookCreateParams
  {
      UrlValue = "https://example.com/anthropic-webhooks",
      Name = "Enforcement actions",
      EnabledEvents =
      [
          EnabledEvent.UserProfileEnforcementActionOpened,
          EnabledEvent.UserProfileEnforcementActionResolved,
      ],
  });

  Console.WriteLine(endpoint.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  endpoint, err := client.Beta.Organization.Webhooks.New(context.Background(), anthropic.BetaOrganizationWebhookNewParams{
  	URL:  "https://example.com/anthropic-webhooks",
  	Name: anthropic.String("Enforcement actions"),
  	EnabledEvents: []string{
  		"user_profile.enforcement_action_opened",
  		"user_profile.enforcement_action_resolved",
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(endpoint.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.webhooks.WebhookCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WebhookCreateParams.builder()
          .url("https://example.com/anthropic-webhooks")
          .name("Enforcement actions")
          .addEnabledEvent(WebhookCreateParams.EnabledEvent.USER_PROFILE_ENFORCEMENT_ACTION_OPENED)
          .addEnabledEvent(WebhookCreateParams.EnabledEvent.USER_PROFILE_ENFORCEMENT_ACTION_RESOLVED)
          .build();

      var endpoint = client.beta().organization().webhooks().create(params);

      IO.println(endpoint.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $endpoint = $client->beta->organization->webhooks->create(
      url: 'https://example.com/anthropic-webhooks',
      name: 'Enforcement actions',
      enabledEvents: [
          'user_profile.enforcement_action_opened',
          'user_profile.enforcement_action_resolved',
      ],
  );

  echo $endpoint->id, "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  endpoint = client.beta.organization.webhooks.create(
    url: "https://example.com/anthropic-webhooks",
    name: "Enforcement actions",
    enabled_events: [
      "user_profile.enforcement_action_opened",
      "user_profile.enforcement_action_resolved"
    ]
  )

  puts endpoint.id
  ```
</CodeGroup>

Responsnya adalah endpoint baru, seperti yang ditunjukkan di [Field endpoint](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#endpoint-fields), ditambah `signing_secret`-nya.

## Error

Sebuah permintaan mengembalikan `400` jika:

* `url`-nya tidak memenuhi aturan di [Field endpoint](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#endpoint-fields), atau permintaan pembuatan tidak mencantumkan jenis event apa pun. Pesan error menjelaskan apa yang salah.
* Organisasi Anda tidak memiliki workspace default.
* Webhook organisasi tidak tersedia untuk organisasi Anda karena workspace default-nya menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek). Pesan error menyatakan hal tersebut.
* Permintaan tersebut akan membuat organisasi Anda memiliki lebih dari 32 endpoint webhook organisasi.
* Permintaan tersebut memasukkan jenis event selain dua jenis di [Jenis event](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#event-types) ke dalam `enabled_events`. Pesan error mencantumkan jenis-jenis yang diterima.

Sebuah permintaan mengembalikan `403` jika peran akun Anda tidak mencakup izin yang dibutuhkan permintaan tersebut. Error tersebut menyebutkan nama izin itu.

Sebuah permintaan mengembalikan `404` jika:

* Permintaan tersebut tidak mengirimkan header `anthropic-beta: webhooks-2026-10-07`.
* Anthropic belum mengaktifkan webhook organisasi untuk organisasi Anda.
* Organisasi Anda mengaktifkan kesiapan HIPAA.
* Permintaan tersebut menggunakan jenis kredensial yang tidak diterima oleh permintaan-permintaan ini.
* `webhook_endpoint_id`-nya tidak cocok dengan endpoint mana pun di organisasi Anda.

Sebuah permintaan mengembalikan `409` jika:

* Permintaan tersebut akan membuat dua endpoint webhook organisasi yang diaktifkan berbagi URL yang sama.
* Permintaan lain mengubah endpoint organisasi Anda pada saat yang sama. Coba ulang permintaan tersebut.
