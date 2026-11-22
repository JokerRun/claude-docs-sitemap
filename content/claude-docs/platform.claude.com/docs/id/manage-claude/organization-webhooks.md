---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/organization-webhooks
fetched_at: 2026-11-22T02:13:35.406200Z
sha256: c6303996e58469597d336ada2085f7b3b1d52d391e3c6c5f38b7202193938475
---

---
title: Webhook organisasi
url: https://platform.claude.com/docs/id/manage-claude/organization-webhooks
description: Daftarkan endpoint webhook untuk event tentang profil pengguna dan kunci enkripsi yang dikelola pelanggan milik organisasi Anda, lalu tanggapi setiap event.
featureMetadata:
  status: beta
  betaHeader: webhooks-2026-10-07
  supportedPlatforms:
    Claude API: beta
---

Endpoint webhook organisasi adalah URL tempat Anthropic mengirimkan event tentang organisasi Anda, seperti kunci enkripsi yang berhenti berfungsi. Gunakan halaman ini untuk memilih event yang Anda perlukan, mendaftarkan endpoint, menanggapi setiap event, dan mengejar ketertinggalan ketika sebuah event tidak tiba. Anda mengelola endpoint dengan Admin API di bawah `/v1/organizations/webhooks`, atau [di Claude Console](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#manage-endpoints) untuk beberapa jenis event.

<Note>
  Pengiriman dua [event profil pengguna](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#user-profile-events) tidak aktif: Anthropic tidak mengirimkannya. Anda dapat mendaftarkan endpoint untuk event tersebut dan membangun handler Anda berdasarkan format event di halaman ini.
</Note>

## Sebelum Anda memulai

Anda memerlukan hal-hal berikut:

* Organisasi di Claude API yang webhook organisasinya telah diaktifkan. Tanpa itu, [permintaan mengembalikan `404`](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#errors). Yang berlaku adalah kasus pertama yang sesuai dengan organisasi Anda:

  * Organisasi mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness): organisasi tersebut tidak dapat menggunakan webhook organisasi.
  * Organisasi dapat menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek): organisasi tersebut memiliki webhook organisasi.
  * Organisasi lainnya: hubungi tim akun Anthropic Anda untuk meminta akses.

* Salah satu kredensial berikut:

  * [Kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).
  * [Token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token) dengan scope `org:admin`.
  * [Kunci pribadi atau kunci akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) yang tidak dibatasi pada sebuah workspace.

Dengan kunci Admin API, Anda dapat membuat setiap permintaan di [Mengelola endpoint](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#manage-endpoints). Dengan token `org:admin`, Anda dapat membuat permintaan yang sama. Jika token tersebut terikat pada workspace selain [workspace default](https://platform.claude.com/docs/id/manage-claude/workspaces#how-workspaces-work) organisasi Anda, Anda tidak dapat membuat satu pun permintaan tersebut. Dengan kunci pribadi atau kunci akun layanan, permintaan yang dapat Anda buat bergantung pada [peran organisasi](https://platform.claude.com/docs/id/manage-claude/admin-api#organization-roles-and-permissions) akun tersebut:

* Untuk menampilkan daftar atau mendapatkan endpoint webhook: `developer` atau `admin`
* Untuk membuat, memperbarui, atau menghapus endpoint webhook, atau untuk mengganti signing secret: `admin`

## Jenis event

Sebuah endpoint menerima jenis event yang Anda cantumkan di [`enabled_events`](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#endpoint-fields)-nya saat Anda [membuat atau memperbaruinya](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#manage-endpoints). Halaman ini membahas kelompok jenis event berikut:

* [Event profil pengguna](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#user-profile-events): Anthropic membatasi atau memblokir salah satu [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) Anda, atau pembatasan atau pemblokiran tersebut berakhir.
* [Event kunci enkripsi](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#encryption-key-events): “key management service” (layanan manajemen kunci), atau KMS, Anda terus menolak salah satu kunci enkripsi yang dikelola pelanggan Anda, atau kunci tersebut berfungsi kembali.

Untuk jenis event lainnya, lihat `enabled_events` di [referensi API untuk membuat endpoint](https://platform.claude.com/docs/id/api/beta/organization/webhooks/create).

## Event profil pengguna

Jenis-jenis event berikut berkaitan dengan [tindakan penegakan](https://platform.claude.com/docs/id/manage-claude/user-profiles#check-whether-anthropic-has-restricted-or-banned-a-profile) pada profil pengguna. Anthropic tidak mengirimkannya.

| Event | Pemicu |
| ----- | ----- |
| `user_profile.enforcement_action_opened` | Anthropic membuka tindakan penegakan pada sebuah profil pengguna. |
| `user_profile.enforcement_action_resolved` | Sebuah tindakan penegakan berakhir. Anthropic menyelesaikannya, atau waktu `expires_at`-nya terlewati. |

Menghapus sebuah profil akan mengakhiri tindakan-tindakan terbukanya tanpa event `user_profile.enforcement_action_resolved`.

### Sebelum event pertama Anda

Dalam setiap permintaan yang header `anthropic-beta`-nya berisi `user-profiles-2026-09-04` atau nilai yang lebih lama, respons tidak menyertakan field `enforcement_status` dan `enforcement_actions`, dan filter daftar `enforcement_status[]` mengembalikan `400`. Untuk mendapatkan field tersebut, hapus nilai itu dari permintaan Anda.

Jika sebuah tindakan penegakan dibuka sebelum Anthropic mengaktifkan pengiriman event untuk organisasi Anda, atau sebelum Anda mendaftarkan endpoint Anda, Anda tidak mendapatkan event `user_profile.enforcement_action_opened` untuknya. Tindakan tersebut tetap muncul pada profil. Untuk menemukan tindakan-tindakan ini, [tampilkan daftar profil Anda](https://platform.claude.com/docs/id/api/user_profiles/list) dengan `enforcement_status[]=restricted` dan `enforcement_status[]=banned`. Sebuah respons mungkin mengembalikan lebih sedikit profil daripada `limit`, atau tidak ada sama sekali, sebelum daftar berakhir, jadi terus minta halaman berikutnya hingga `next_page` bernilai `null`.

### Isi sebuah event

Event profil pengguna membawa ID, bukan tindakan atau profilnya. `data.id` adalah ID profil, dan `data.enforcement_action_id` adalah ID tindakan, yang diawali dengan `enac_`:

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

## Event kunci enkripsi

Event ini berkaitan dengan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek) (CMEK) milik organisasi Anda. Admin API menyebut kunci seperti itu sebagai external key, sehingga jenis event diawali dengan `external_key`:

| Event | Pemicu |
| ----- | ----- |
| `external_key.failed` | KMS Anda terus menolak penggunaan sebuah kunci oleh Anthropic, misalnya karena seseorang menonaktifkan kunci tersebut atau mencabut akses Anthropic ke kunci tersebut. |
| `external_key.recovered` | Setelah Anthropic mengirimkan `external_key.failed`, kunci tersebut berfungsi kembali saat Anthropic menggunakannya. |

Hanya penolakan nyata yang memicu event ini. Tidak ada event uji.

Ketika sebuah kunci gagal atau pulih, Anthropic biasanya juga mengirim email kepada anggota organisasi Anda yang dapat mengelola kunci enkripsi. Email kegagalan menyebutkan workspace yang baru-baru ini ditolak oleh KMS Anda, tetapi mungkin tidak mencantumkan semuanya.

Event menyebutkan kunci di `data.id`, yang diawali dengan `ekey_`:

```json
{
  "type": "event",
  "id": "whe_8c1d5e2a9f4b7036d1e8a5c2f9b40d73",
  "created_at": "2026-11-20T09:14:07.482913Z",
  "data": {
    "type": "external_key.failed",
    "id": "ekey_011CZkZFr7KpXc4nMgSvQh3w",
    "organization_id": "org_011CZkZBj9RsYd3wNcHvKq6t"
  }
}
```

* **Waktu:** `created_at` adalah waktu Anthropic pertama kali mencoba mengirimkan event, bukan waktu kunci gagal atau pulih. Nilainya dapat mencakup pecahan detik.
* **Workspace:** Event tidak menyebutkan workspace, karena beberapa workspace dapat menggunakan satu kunci.

### Menanggapi event kunci enkripsi

Setelah Anda mengembalikan `2xx` untuk salah satu event, [validasi kunci tersebut](https://platform.claude.com/docs/id/api/organization/external_keys/validate) dengan `POST /v1/organizations/external_keys/{external_key_id}/validate`. Gunakan `data.id` sebagai ID, serta kunci Admin API atau token `org:admin`. Apa yang Anda lakukan selanjutnya bergantung pada `status` dalam respons:

* **`failure`, dan pesan `error` menyebutkan untuk mencoba lagi:** Lakukan apa yang disebutkannya, lalu validasi lagi.
* **`failure`, dengan pesan lain apa pun:** Temukan perbaikannya di [Memecahkan masalah CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting).
* **`success`:** Periksa setiap workspace yang menggunakan kunci tersebut, karena validasi menguji paling banyak satu workspace. KMS Anda mungkin menolak workspace lain, seperti pada [kebijakan kunci AWS yang mencantumkan workspace](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms-workspaces).

Untuk memeriksa workspace:

1. [Tampilkan daftar workspace Anda](https://platform.claude.com/docs/id/api/organization/workspaces/list) dengan `include_default=true`.
2. Temukan workspace yang memiliki ID kunci tersebut di `external_key_id`.
3. Kirim permintaan Messages API di masing-masing workspace, dengan kunci API yang dapat bertindak di workspace tersebut.

| Hasil permintaan | Artinya bagi workspace |
| ----- | ----- |
| Error [`cmek_key_disabled`](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cmek-key-disabled) atau [`cmek_key_network_blocked`](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cmek-key-network-blocked) | KMS Anda menolak Anthropic. |
| Error [`cmek_key_unreachable`](https://platform.claude.com/docs/id/manage-claude/cmek-troubleshooting#cmek-key-unreachable) | Anthropic tidak dapat menjangkau KMS Anda. |
| Berhasil | Kunci berfungsi, atau kunci berhenti berfungsi kurang dari satu jam yang lalu. |

[Permintaan dapat berhasil hingga 1 jam](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle#what-each-action-does) setelah kunci berhenti berfungsi, jadi jika sebuah permintaan berhasil, kirim ulang permintaan tersebut satu jam setelah `external_key.failed`. Error dapat bertahan beberapa menit setelah perbaikan.

Setelah perbaikan, ulangi pemeriksaan ini. Jangan menunggu `external_key.recovered`, yang mungkin tidak tiba.

### Kapan event kunci enkripsi tiba

Jika setiap workspace yang menggunakan kunci menerima sekitar satu permintaan Messages API per menit, event biasanya tiba pada waktu-waktu berikut. Dengan lalu lintas yang lebih sedikit, event memerlukan waktu lebih lama:

* **`external_key.failed`:** Dalam 30 menit setelah seseorang menonaktifkan kunci atau mencabut akses Anthropic ke kunci tersebut. Permintaan mungkin masih berhasil saat event ini tiba.
* **`external_key.recovered`:** Sekitar 30 menit setelah kunci berfungsi kembali.

### Kapan event kunci enkripsi mungkin tidak tiba

Jangan jadikan event ini satu-satunya sinyal Anda. Pasang juga peringatan untuk tiga error `cmek_key` dari Messages API, dan [kejar event yang terlewat](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#catch-up-on-missed-events) secara berkala.

Dalam kasus-kasus berikut, Anda mungkin melewatkan salah satu atau kedua event:

| Kasus | Apa yang mungkin Anda lewatkan |
| ----- | ----- |
| Tidak ada permintaan yang menggunakan kunci | `external_key.failed`, karena Anthropic melihat penolakan hanya ketika sebuah permintaan menggunakan kunci tersebut |
| Tidak ada permintaan yang menggunakan kunci dalam sekitar satu hari sejak penolakan terakhir | `external_key.recovered`, karena Anthropic berhenti menunggu keberhasilan |
| KMS Anda mengalami gangguan atau timeout | Kedua event, karena gangguan bukanlah penolakan |
| Kunci di beberapa organisasi mulai gagal pada waktu yang hampir bersamaan | Kedua event dan email-emailnya, karena penyebabnya mungkin Anthropic atau penyedia cloud |
| [Kunci workspace default Anda](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#if-your-default-workspace-uses-an-encryption-key) gagal, dan kunci tersebut mengenkripsi sebuah nilai endpoint Anda | Setiap event hingga kunci berfungsi kembali, termasuk `external_key.failed` miliknya sendiri |

Karena Anda dapat melewatkan salah satu event, Anda mungkin menerima `external_key.failed` dua kali berturut-turut, atau `external_key.recovered` tanpa `external_key.failed` sebelumnya.

## Field endpoint

Endpoint webhook organisasi memiliki field-field berikut:

| Field | Tipe | Deskripsi |
| ----- | ----- | ----- |
| `id` | string | ID endpoint, yang diawali dengan `wep_`. Ditetapkan oleh Anthropic. |
| `url` | string | Tempat Anthropic mengirimkan event. Harus HTTPS pada port 443, dengan nama domain publik, bukan alamat IP. Dua endpoint webhook organisasi yang diaktifkan di organisasi Anda tidak dapat berbagi URL yang sama. |
| `enabled_events` | array string | [Jenis event](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#event-types) yang diterima endpoint ini. Permintaan pembuatan harus mencantumkan setidaknya satu. |
| `name` | string | Label opsional untuk penggunaan Anda sendiri. |
| `description` | string | Deskripsi opsional untuk penggunaan Anda sendiri. |
| `state` | string | `enabled` atau `disabled`. |
| `disabled_reason` | string | Alasan Anthropic menonaktifkan endpoint. Kosong jika tidak. |
| `created_at` | string | Waktu endpoint dibuat. Ditetapkan oleh Anthropic. |
| `updated_at` | string | Waktu endpoint terakhir berubah. Ditetapkan oleh Anthropic. |
| `signing_secret` | string | Secret berawalan `whsec_`, dibuat bersama endpoint. Hanya respons yang membuat endpoint atau mengganti secret yang menyertakannya, jadi simpanlah dengan aman. |

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

* **Percobaan ulang:** Jika pengiriman gagal, Anthropic mencoba ulang pengiriman tersebut beberapa kali selama beberapa menit berikutnya. Jika setiap percobaan gagal, Anthropic membuang event tersebut, sehingga gangguan singkat pada endpoint Anda pun dapat menghilangkan event.

* **Penonaktifan otomatis:** Anthropic menonaktifkan sebuah endpoint ketika:

  * Endpoint mengembalikan redirect (`3xx`).
  * URL-nya di-resolve ke alamat IP non-publik.
  * Pengirimannya terus gagal.

  Anthropic melewati event untuk endpoint yang dinonaktifkan dan tidak mengirimkannya di kemudian hari.

### Mengejar event yang terlewat

Anthropic tidak memberi tahu Anda ketika membuang event, menonaktifkan endpoint, atau melewati event untuk endpoint yang dinonaktifkan. Kejar ketertinggalan secara berkala, misalnya sekali sehari, dan pada waktu-waktu berikut:

* Saat Anda pertama kali menambahkan jenis event ke sebuah endpoint
* Setelah endpoint Anda mengalami gangguan
* Setelah Anda mengaktifkan kembali sebuah endpoint

Setiap kali, periksa bahwa `state` endpoint Anda bernilai `enabled`. Kemudian, periksa sumber daya di balik setiap kelompok event yang Anda gunakan:

* **Profil pengguna:** Tampilkan daftar profil Anda berdasarkan status penegakan, seperti di [Sebelum event pertama Anda](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#before-your-first-event). Profil yang tidak ada dalam daftar tersebut tidak memiliki tindakan terbuka.
* **Kunci enkripsi:** [Tampilkan daftar kunci Anda](https://platform.claude.com/docs/id/api/organization/external_keys/list), dan [validasi masing-masing](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#respond-to-an-encryption-key-event). Jika Anda tidak menerima event untuk kunci tersebut, `success` tidak memerlukan pemeriksaan lebih lanjut kecuali permintaan Messages API gagal.

## Mengelola endpoint

Dengan Admin API, Anda dapat membuat permintaan-permintaan berikut:

| Tugas | Permintaan |
| ----- | ----- |
| Menampilkan daftar endpoint organisasi Anda | [`GET /v1/organizations/webhooks`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/list) |
| Membuat endpoint | [`POST /v1/organizations/webhooks`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/create) |
| Mendapatkan satu endpoint | [`GET /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/retrieve) |
| Memperbarui `url`, `name`, `description`, `enabled_events`, atau `state` sebuah endpoint | [`POST /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/update) |
| Menghapus endpoint | [`DELETE /v1/organizations/webhooks/{webhook_endpoint_id}`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/delete) |
| Mengganti signing secret | [`POST /v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret`](https://platform.claude.com/docs/id/api/beta/organization/webhooks/regenerate_signing_secret) |

Dalam pembaruan, `enabled_events` menggantikan seluruh daftar jenis event endpoint. Daftar kosong tidak mengosongkan daftar: endpoint tetap mempertahankan jenis event yang dimilikinya. Untuk menghentikan pengiriman, kirim `"state": "disabled"` atau hapus endpoint tersebut.

Untuk mengaktifkan kembali sebuah endpoint, termasuk setelah Anthropic menonaktifkannya, kirim `"state": "enabled"` dalam permintaan pembaruan.

Ketika Anda mengganti signing secret, secret lama langsung berhenti berfungsi. Pengiriman sejak saat itu, termasuk percobaan ulang event sebelumnya, ditandatangani dengan secret baru, jadi segera perbarui penerima Anda.

Kirim header `anthropic-beta: webhooks-2026-10-07` dengan setiap permintaan. SDK dan CLI mengirimkannya untuk Anda. Contoh ini menampilkan daftar endpoint organisasi Anda, menggunakan kunci Admin API dari `ANTHROPIC_API_KEY`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/webhooks" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
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

Contoh ini membuat endpoint untuk dua event profil pengguna, yang tidak dikirimkan oleh Anthropic. Untuk menerima event lain, seperti `external_key.failed` dan `external_key.recovered`, cantumkan jenisnya di `enabled_events` sebagai gantinya:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/webhooks" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
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

Jika Anda memiliki peran organisasi `admin`, Anda dapat mengelola endpoint untuk event kunci enkripsi di Claude Console sebagai gantinya. Gunakan tab **Organisasi** di halaman [Webhook](https://platform.claude.com/settings/webhooks), yang menampilkan signing secret satu kali, saat Anda membuat endpoint atau mengganti secret-nya.

## Jika workspace default Anda menggunakan kunci enkripsi

Anthropic menyimpan endpoint organisasi Anda di [workspace default](https://platform.claude.com/docs/id/manage-claude/workspaces#how-workspaces-work) Anda. Jika workspace tersebut menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek), Anthropic mengenkripsi nilai-nilai berikut dengan kunci tersebut:

| Nilai | Permintaan yang mengenkripsinya |
| ----- | ----- |
| `name` dan `description` | Membuat endpoint, atau mengirim pembaruan apa pun ke endpoint tersebut |
| Signing secret | Membuat endpoint, atau mengganti secret |

Anthropic tidak mengenkripsi field lain, seperti `url`, dengan kunci Anda.

Pada endpoint yang dibuat sebelum [kunci Anda mulai berlaku](https://platform.claude.com/docs/id/manage-claude/cmek-how-it-works#when-your-key-takes-effect), setiap nilai tetap berada di bawah kunci Anthropic hingga salah satu permintaan tersebut mengenkripsinya. Tidak ada field yang menunjukkan kunci mana yang melindungi sebuah nilai. Untuk memindahkan nilai-nilai sebuah endpoint ke bawah kunci Anda, perbarui endpoint tersebut dan ganti secret-nya.

Setelah kunci Anda mengenkripsi nilai apa pun dari sebuah endpoint, endpoint tersebut bergantung pada kunci itu. Selama Anthropic tidak dapat menggunakan kunci tersebut, pengiriman dan permintaan yang memerlukannya akan gagal. Permintaan biasanya mengembalikan error `500`:

| Apa yang gagal | Untuk endpoint mana |
| ----- | ----- |
| Pengiriman setiap jenis event | Endpoint yang bergantung pada kunci tersebut |
| Permintaan untuk mengambil dan menghapus | Endpoint yang bergantung pada kunci tersebut |
| Permintaan untuk menampilkan daftar | Semua, jika ada endpoint yang bergantung pada kunci tersebut |
| Permintaan untuk membuat, memperbarui, dan mengganti secret | Biasanya semua |

Anthropic membuang event yang tidak dapat dikirimkannya, dan tidak mengirimkannya di kemudian hari. Endpoint tetap diaktifkan, dan pengiriman dilanjutkan setelah Anthropic dapat menggunakan kunci tersebut. Kemudian, [kejar event yang terlewat](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#catch-up-on-missed-events).

Jika Anda menghapus kunci di KMS Anda, semua kegagalan ini bersifat permanen, dan Anda tidak dapat membuat endpoint lain. Untuk mengetahui apa lagi yang membuat Anthropic tidak dapat menggunakan sebuah kunci, lihat [Apa yang terjadi saat Anda merotasi, menonaktifkan, atau menghapus kunci enkripsi Anda](https://platform.claude.com/docs/id/manage-claude/cmek-key-lifecycle).

## Error

Sebuah permintaan mengembalikan `400` jika:

* `url`-nya tidak memenuhi aturan di [Field endpoint](https://platform.claude.com/docs/id/manage-claude/organization-webhooks#endpoint-fields), atau permintaan pembuatan tidak mencantumkan jenis event apa pun. Pesan error menjelaskan apa yang salah.
* Organisasi Anda tidak memiliki workspace default.
* Permintaan tersebut akan membuat organisasi Anda memiliki lebih dari 32 endpoint webhook organisasi.
* `enabled_events`-nya mencakup jenis event yang tidak diterima oleh endpoint webhook organisasi. Pesan error mencantumkan jenis-jenis yang diterima.

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
