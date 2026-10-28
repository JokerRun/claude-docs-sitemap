---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/claude-tag-api
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: d3d3086dc2e8ca69724b3160f9cff785f28ea09d0915ffb474614ebf3053bf27
---

---
title: Claude Tag API
url: https://platform.claude.com/docs/id/manage-claude/claude-tag-api
description: "Kelola Claude Tag di Slack untuk organisasi Claude Enterprise Anda dari sistem Anda sendiri: baca dan ubah pengaturan pada channel dan workspace Slack, lihat pengaturan mana yang berlaku dan alasannya, serta lampirkan Access bundle."
---

[Claude Tag](https://claude.com/docs/claude-tag/overview) adalah Claude yang bekerja sebagai rekan tim di Slack: seseorang menyebut Claude di sebuah channel dan Claude menjawab di thread. Claude Tag API memungkinkan Anda membaca dan mengubah, dari sistem Anda sendiri, pengaturan Claude Tag yang tanpa API ini diatur secara manual oleh pemilik organisasi di [claude.ai > Organization settings > Claude Tag](https://claude.ai/admin-settings/claude-tag). Gunakan API ini untuk mengaktifkan Claude channel demi channel dari alur kerja persetujuan, menyimpan konfigurasi Anda dalam “version control” (kontrol versi), atau mengaudit apa yang berlaku di setiap channel.

Claude Tag adalah produk claude.ai. API ini mengelolanya untuk organisasi Claude Enterprise dan tidak ada hubungannya dengan workspace Claude Platform, penggunaan API, atau Claude Console.

<Check>
  **Diperlukan kunci Admin API dengan cakupan (scope)**

  Endpoint ini memerlukan kunci Admin API dengan cakupan `read:claude_tag` (untuk endpoint `GET`) atau cakupan `write:claude_tag` (untuk endpoint `POST` dan `DELETE`); lihat [Cakupan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#scopes). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana pemilik utama Anda membuatnya.
</Check>

<Note>
  Claude Tag API berstatus **beta** dan hanya tersedia untuk organisasi Claude Enterprise. API ini tidak tersedia untuk organisasi Claude Platform (Claude Console).

  Setiap permintaan harus menyertakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `anthropic-beta: experimental-claude-tag-2026-10-21` (SDK dan CLI `ant` mengirimkannya untuk Anda). Permintaan tanpa header tersebut mengembalikan `404`, persis seolah-olah endpoint tersebut tidak ada.
</Note>

## Endpoint

API ini menyediakan 14 endpoint di empat resource:

| Resource                                                                                                                                                                                           | Endpoint                                                                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Channel Slack:** menyiapkan channel, mencantumkan channel dari sebuah workspace atau menemukan satu channel berdasarkan ID Slack-nya, membaca satu channel, mengubah pengaturannya, menghapusnya | `POST /v1/organizations/claude_tag/slack_channels`<br />`GET /v1/organizations/claude_tag/slack_channels`<br />`GET /v1/organizations/claude_tag/slack_channels/{id}`<br />`POST /v1/organizations/claude_tag/slack_channels/{id}`<br />`DELETE /v1/organizations/claude_tag/slack_channels/{id}`      |
| **Workspace Slack:** mencantumkan workspace Anda atau menemukan satu workspace berdasarkan ID Slack-nya, membaca satu workspace, mengubah pengaturannya                                            | `GET /v1/organizations/claude_tag/slack_workspaces`<br />`GET /v1/organizations/claude_tag/slack_workspaces/{id}`<br />`POST /v1/organizations/claude_tag/slack_workspaces/{id}`                                                                                                                       |
| **Bundle:** mencantumkan Access bundle organisasi Anda, membaca satu bundle (hanya-baca)                                                                                                           | `GET /v1/organizations/claude_tag/bundles`<br />`GET /v1/organizations/claude_tag/bundles/{bundle_id}`                                                                                                                                                                                                 |
| **Target bundle:** mencantumkan di mana sebuah Bundle dilampirkan, melampirkannya ke channel atau workspace, membaca satu lampiran, melepaskannya                                                  | `GET /v1/organizations/claude_tag/bundles/{bundle_id}/targets`<br />`POST /v1/organizations/claude_tag/bundles/{bundle_id}/targets`<br />`GET /v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}`<br />`DELETE /v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}` |

Rilis ini mencakup Slack. Menghubungkan dan memutuskan workspace Slack atau Enterprise Grid, default Slack organisasi Anda, membuat dan mengedit Access bundle, batas pengeluaran, serta setiap pengaturan Claude Tag selain lima pengaturan di [Pengaturan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#settings) tetap dilakukan di claude.ai.

## Prasyarat

* Organisasi Anda harus menggunakan paket Claude Enterprise, dengan [Claude Tag yang sudah disiapkan](https://claude.com/docs/claude-tag/admins/setup-overview) dan setidaknya satu workspace Slack atau Enterprise Grid yang terhubung.
* Pemilik utama Anda membuat kunci Admin API dengan cakupan `read:claude_tag`, cakupan `write:claude_tag`, atau keduanya di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Lihat [Membuat kunci untuk organisasi Claude Enterprise](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization).
* Setiap permintaan membawa tiga header: `x-api-key`, `anthropic-version: 2023-06-01` (lihat [Versi API](https://platform.claude.com/docs/id/api/versioning)), dan `anthropic-beta: experimental-claude-tag-2026-10-21`.

Di Python, TypeScript, C#, Go, Java, PHP, dan Ruby, SDK menyediakan endpoint ini di bawah `client.beta.organization.claude_tag` (typescript: `client.beta.organization.claudeTag`; csharp, go: `client.Beta.Organization.ClaudeTag`; java: `client.beta().organization().claudeTag()`; php: `$client->beta->organization->claudeTag`), dan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) di bawah `ant beta:organization:claude-tag`; keduanya mengirimkan header `anthropic-version` dan `anthropic-beta` untuk Anda. Contoh di halaman ini membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`. Ketika SDK atau CLI mengambil halaman berikutnya untuk Anda, `limit` menetapkan ukuran halaman, bukan total (lihat [Paginasi](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#pagination)).

Kunci API adalah milik organisasi dan tetap berfungsi setelah orang yang membuatnya keluar. Jangan bagikan kunci tersebut atau memasukkannya ke kontrol sumber.

## Mulai cepat

Cantumkan workspace Slack organisasi Anda di Claude Tag:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_workspaces" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-workspaces list
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspaces = client.beta.organization.claude_tag.slack_workspaces.list()

  # Otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for workspace in workspaces:
      print(f"{workspace.id}: {workspace.slack.workspace_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspaces = await client.beta.organization.claudeTag.slackWorkspaces.list();

  for await (const workspace of workspaces) {
    console.log(`${workspace.id}: ${workspace.slack.workspace_id}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ClaudeTag.SlackWorkspaces.List();

  await foreach (var workspace in page.Paginate())
  {
      Console.WriteLine($"{workspace.ID}: {workspace.Slack.WorkspaceID}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  workspaces := client.Beta.Organization.ClaudeTag.SlackWorkspaces.ListAutoPaging(
  	context.Background(),
  	anthropic.BetaOrganizationClaudeTagSlackWorkspaceListParams{},
  )

  for workspaces.Next() {
  	workspace := workspaces.Current()
  	fmt.Printf("%s: %s\n", workspace.ID, workspace.Slack.WorkspaceID)
  }
  if err := workspaces.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var workspaces = client.beta().organization().claudeTag().slackWorkspaces().list();

  for (var workspace : workspaces.autoPager()) {
      IO.println(workspace.id() + ": " + workspace.slack().workspaceId());
  }
  ```

  ```php PHP
  $client = new Client();

  $workspaces = $client->beta->organization->claudeTag->slackWorkspaces->list();

  // Hanya halaman ini; untuk berikutnya, panggil list() lagi dengan page: $workspaces->nextPage.
  foreach ($workspaces->getItems() as $workspace) {
      echo "{$workspace->id}: {$workspace->slack->workspaceID}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.claude_tag.slack_workspaces.list

  page.auto_paging_each do |workspace|
    puts "#{workspace.id}: #{workspace.slack.workspace_id}"
  end
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "type": "slack_workspace",
      "id": "slws_011CZkZnWa7xPc3uJfZe5LgT",
      "slack": {
        "workspace_id": "T01ABCD2EFG"
      },
      "settings": {
        "enabled": null,
        "instructions": "Answer in English unless asked otherwise.",
        "model": null,
        "environment_id": null,
        "guest_policy": null
      },
      "sources": {
        "enabled": null,
        "instructions": [
          {
            "type": "slack_workspace",
            "slack_workspace_id": "slws_011CZkZnWa7xPc3uJfZe5LgT"
          }
        ],
        "model": null,
        "environment_id": null,
        "guest_policy": null
      },
      "created_at": "2026-09-02T17:04:11Z",
      "updated_at": "2026-10-06T09:41:53Z"
    }
  ],
  "next_page": null
}
```

Pengaturan yang bernilai `null` di `settings` tidak ditetapkan pada workspace ini, sehingga workspace mewarisinya dan tidak memiliki sumber untuknya. Untuk membaca apa yang berlaku sebagai gantinya, lihat [Nilai tersimpan dan nilai warisan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#stored-and-inherited-values).

## Scope

| Scope              | Memberikan                                                                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read:claude_tag`  | Setiap endpoint `GET` di halaman ini.                                                                                                                          |
| `write:claude_tag` | Setiap endpoint `POST` dan `DELETE` di halaman ini. Scope ini tidak memberikan akses baca, meskipun respons terhadap perubahan berisi sumber daya yang diubah. |

Sebuah kunci dapat membawa kedua cakupan. Integrasi yang mencari sebuah channel lalu mengubahnya memerlukan keduanya. Tidak ada cakupan lain yang memberikan akses ke endpoint ini, dan kunci yang dibuat di Claude Console tidak berfungsi di sini.

Kunci harus dimiliki oleh organisasi secara keseluruhan. Organisasi selalu merupakan organisasi pemilik kunci, dan tidak ada permintaan yang menyebutkan organisasi. Header `anthropic-workspace-id` diabaikan, karena tidak ada apa pun di sini yang dimiliki oleh workspace Claude Platform.

## Konsep utama

### Nama di halaman ini dan di claude.ai

| API ini          | claude.ai dan Slack                                                                                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Workspace Slack  | Sebuah workspace Slack. API milik Slack sendiri menyebutnya team, sehingga ID workspace milik Slack sendiri di halaman ini adalah team ID di sana. Ini tidak terkait dengan workspace Claude Platform, yang ID-nya diawali `wrkspc_`. |
| Default Slack    | **Default Slack access**: pengaturan yang berlaku untuk setiap workspace dan channel. Pemilik organisasi mengubahnya di claude.ai; API ini menunjukkan di mana channel atau workspace mewarisinya.                                    |
| Level pengaturan | Sebuah [scope](https://claude.com/docs/claude-tag/admins/customize): channel, workspace, atau default Slack                                                                                                                           |
| Bundle           | Sebuah Access bundle ([glosarium Claude Tag](https://claude.com/docs/claude-tag/concepts/glossary#access-bundle))                                                                                                                     |
| `enabled`        | Toggle **Enable Claude Tag in Slack**                                                                                                                                                                                                 |
| `instructions`   | **Custom instructions**                                                                                                                                                                                                               |
| `model`          | **Model**                                                                                                                                                                                                                             |
| `environment_id` | **Environment**                                                                                                                                                                                                                       |
| `guest_policy`   | **How should Claude work in channels with guests**: `restrict` adalah **Restrict**, `channel_only` adalah **Channel only**, dan `allow` adalah **Full access**                                                                        |

### Channel dan workspace yang sudah disiapkan

Sebuah channel atau workspace **sudah disiapkan** ketika Claude Tag menyimpan catatan pengaturan untuknya. Hanya channel atau workspace yang sudah disiapkan yang memiliki `id`, dan hanya itu yang dicantumkan: Slack, bukan API ini, yang menyimpan daftar lengkap channel sebuah workspace.

* Sebuah **workspace** disiapkan ketika pemilik organisasi menghubungkannya di claude.ai. Ketika pemilik menghubungkan Slack Enterprise Grid, workspace-workspace dalam Grid tersebut disiapkan tidak lama kemudian. Penggunaan pertama Claude di sebuah workspace, atau channel pertama yang Anda [siapkan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel) di dalamnya, menyiapkan workspace yang belum disiapkan. Tidak ada endpoint lain yang menyiapkan workspace, dan tidak ada yang menghapusnya.
* Sebuah **channel** disiapkan di claude.ai, oleh penggunaan pertama Claude di dalamnya, atau dengan [Menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel).

Organisasi Anda memiliki sebuah workspace selama koneksinya ke workspace tersebut aktif, dan memiliki channel-channel di dalamnya. Slack Enterprise Grid mengelompokkan beberapa workspace di bawah satu perusahaan. Selama koneksi organisasi Anda ke sebuah Grid aktif, organisasi Anda juga memiliki setiap workspace di Grid tersebut yang belum dihubungkan oleh organisasi lain. Workspace seperti itu sama dengan workspace lainnya: setelah disiapkan, ia memiliki `id`, dicantumkan, dan dapat dibaca, diubah, dan diberi Bundle, serta channel-channelnya dapat dicantumkan. Grid itu sendiri bukan resource dari API ini dan tidak memiliki `id`. Channel atau workspace yang bukan milik Anda mengembalikan `404` yang sama seperti yang tidak ada.

Workspace yang dimiliki organisasi Anda hanya melalui sebuah Grid mengembalikan `404` tersebut hingga disiapkan, di mana pun sebuah permintaan menyebutkannya dengan ID milik Slack sendiri: ketika Anda menemukan workspace tersebut, mencantumkan channel-channelnya, atau mencari channel di dalamnya yang belum disiapkan. Anda tetap dapat [menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel) di dalamnya, yang juga menyiapkan workspace tersebut, tanpa pengaturan yang tersimpan.

Channel yang dibagikan dengan seluruh Grid dapat disimpan di bawah ID Slack milik Grid itu sendiri, yang diawali `E`, sebagai pengganti ID workspace. ID tersebut kemudian menjadi `slack.workspace_id` dari channel, dan [mencantumkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-channels) dengan ID tersebut sebagai `slack_workspace_id` mengembalikan channel-channel tersebut. Tidak ada objek workspace yang memilikinya: jika pemilik menyimpan pengaturan pada Grid itu sendiri di claude.ai, `sources` dapat menyebutkannya sebagai `slack_workspace` yang `id`-nya mengembalikan `404` ketika Anda membacanya.

### ID

Anda mengenali sebuah channel dari ID yang ditampilkan Slack kepada Anda. Cari `id`-nya sekali dengan [Menemukan channel berdasarkan ID Slack-nya](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#find-a-channel-by-its-slack-ids), lalu simpan dan gunakan `id` tersebut.

| ID                               | Prefiks                                                                                                                                                                                             | Tempat kemunculan                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Resource channel Slack           | `slch_`                                                                                                                                                                                             | `id` pada channel; `slack_channel_id` di body permintaan dan respons     |
| Resource workspace Slack         | `slws_`                                                                                                                                                                                             | `id` pada workspace; `slack_workspace_id` di body permintaan dan respons |
| Bundle                           | `capp_`                                                                                                                                                                                             | `id` pada Bundle; `{bundle_id}` di path                                  |
| Target bundle                    | `btgt_`                                                                                                                                                                                             | `id` pada target Bundle; `{target_id}` di path                           |
| ID workspace milik Slack sendiri | `T`, atau `E` untuk ID milik Grid itu sendiri (lihat [Channel dan workspace yang sudah disiapkan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-channels-and-workspaces)) | `slack.workspace_id`; parameter query `slack_workspace_id`               |
| ID channel milik Slack sendiri   | `C` atau `G`                                                                                                                                                                                        | `slack.channel_id`; parameter query `slack_channel_id`                   |

<Warning>
  `slack_channel_id` dan `slack_workspace_id` masing-masing memiliki dua arti. Dalam **parameter query**, masing-masing adalah ID milik Slack sendiri (`C05HJKL6MNP`, `T01ABCD2EFG`). Dalam **body permintaan atau respons**, masing-masing adalah `id` yang diterbitkan API ini (`slch_...`, `slws_...`). ID milik Slack sendiri di body atau respons selalu berada di bawah `slack`.
</Warning>

ID channel Slack dalam parameter query atau body permintaan yang tidak diawali `C` atau `G` mengembalikan `400`, demikian pula setiap ID Slack yang memiliki karakter selain huruf kapital dan angka setelah huruf pertamanya atau lebih panjang dari 32 karakter.

Sebuah `id` tidak berubah selama channel atau workspace tersebut disiapkan, apa pun yang Anda ubah padanya, dengan satu pengecualian yang dijelaskan di [Mode hanya-baca](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-only-mode). Channel atau workspace yang dihapus lalu disiapkan kembali memiliki `id` baru, dan `id` lama tetap mengembalikan `404`. Ketika `id` yang tersimpan mengembalikan `404` tanpa `error_code`, [cantumkan workspace Anda](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-workspaces) dengan kunci dan header yang sama. Permintaan tersebut tidak menyebutkan channel atau workspace apa pun, jadi jika mengembalikan `200`, `id` tersebut sudah tidak ada: temukan kembali channel atau workspace tersebut berdasarkan ID Slack-nya. Status lain apa pun tidak mengatakan apa-apa tentang `id` tersebut: pertahankan nilai `id` yang tersimpan dan lihat [Respons kesalahan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#error-responses).

### Pengaturan

Setiap tingkat pengaturan menyimpan lima pengaturan yang sama, semuanya opsional:

| Pengaturan       | Tipe    | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`        | boolean | Apakah Claude aktif.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `instructions`   | string  | Panduan tetap yang dibaca Claude di setiap sesi. Paling banyak 8.192 karakter setelah spasi di awal dan akhir dipangkas. Teks kosong menghapus pengaturan ini.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `model`          | string  | Model yang digunakan saat sesi baru dimulai: sebuah [ID model](https://platform.claude.com/docs/id/models/overview) yang dapat digunakan organisasi Anda dengan Claude Tag. Paling banyak 128 karakter.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `environment_id` | string  | Lingkungan cloud tempat sesi berjalan, dengan prefiks `env_`. Lingkungan ini harus aktif dan dimiliki oleh organisasi Anda.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `guest_policy`   | object  | Apa yang dilakukan Claude di sebuah channel selama ada tamu Slack di dalamnya, untuk semua orang di channel: `{"type": "allow"}` (Claude menjawab), `{"type": "restrict"}` (Claude tidak menjawab), atau `{"type": "channel_only"}` (Claude menjawab hanya dengan Bundle yang dilampirkan ke channel itu sendiri; jika `channel_only` tidak tersedia untuk organisasi Anda, permintaan yang menetapkannya mengembalikan `400`). Lihat [Membatasi channel dengan tamu](https://claude.com/docs/claude-tag/admins/restrict-access#restrict-guest-channels) untuk maknanya di channel yang dibagikan melalui Slack Connect atau di seluruh Enterprise Grid. |

`model` dan `environment_id` diperiksa saat Anda menuliskannya dan tidak diperiksa lagi: jika model atau lingkungan tersebut kemudian berubah, respons tetap mengembalikan nilai yang tersimpan.

Jika pemilik organisasi telah menempatkan sebuah tingkat pengaturan pada pool runner self-hosted di claude.ai, `environment_id`-nya mengembalikan ID pool tersebut, yang diawali dengan `ccpool_`. API ini tidak dapat menetapkan pool runner, dan mengembalikan `400` untuk permintaan yang mengubah atau menghapus `environment_id` pada tingkat pengaturan yang menyimpan pool runner.

### Nilai tersimpan dan nilai warisan

Pengaturan ada di tiga level: channel, workspace tempat channel berada, dan default Slack organisasi Anda, yang ditetapkan oleh pemilik organisasi di claude.ai. Setiap level hanya menyimpan apa yang ditetapkan padanya. `settings` dari objek channel atau workspace dapat berisi salah satu dari dua hal:

* **Apa yang disimpannya.** Inilah isi respons kecuali Anda meminta sebaliknya. Pengaturan yang tidak ditetapkan pada channel atau workspace bernilai `null`. Gunakan ini untuk membandingkan dengan konfigurasi yang Anda simpan di tempat lain.
* **Apa yang berlaku di dalamnya**, setelah semua level diperhitungkan. Untuk mendapatkannya, tambahkan parameter query `include_inherited=true` ke permintaan `GET` apa pun yang mengembalikan channel atau workspace, termasuk kedua daftar. Gunakan ini untuk audit, atau untuk mencari tahu mengapa Claude berperilaku seperti itu di satu channel. Parameter ini default-nya `false`, dan nilai yang bukan Boolean mengembalikan `400`. Permintaan yang menyiapkan channel atau mengubah pengaturan tidak menerima parameter ini dan mengembalikan `400` jika Anda mengirimkannya; responsnya berisi apa yang tersimpan.

Dalam kedua kasus, `sources` menyebutkan, untuk setiap pengaturan, level asal nilai di `settings`. Tanpa `include_inherited`, sumber dari pengaturan yang disimpan channel atau workspace menyebutkan channel atau workspace itu sendiri, dan pengaturan yang tidak disimpannya tidak memiliki sumber: `null`, atau daftar kosong untuk `instructions`. Dengan `include_inherited=true`, setiap pengaturan kecuali `instructions` memiliki sumber, dan pengaturan yang tidak ditetapkan oleh level mana pun memiliki sumber `{"type": "default"}`; ketika tidak ada level yang menetapkan `instructions`, nilainya `null` dan daftar sumbernya kosong. Jadi, untuk membedakan nilai yang ditetapkan channel atau workspace itu sendiri dari nilai yang diwarisinya, lihat sumbernya, bukan apakah nilainya `null`.

Setiap pengaturan ditentukan secara terpisah:

| Pengaturan       | Aturan                                                                                                                                                                | Ketika tidak ada level yang menetapkannya       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `enabled`        | Level terdekat yang menetapkannya menentukan nilainya, sehingga `true` pada sebuah channel mengaktifkan Claude di sana bahkan ketika workspace-nya menyimpan `false`. | `true`                                          |
| `instructions`   | Aditif. Teks dari setiap level yang menetapkannya digabungkan, mulai dari yang paling luas, dengan satu baris kosong di antaranya.                                    | `null`                                          |
| `model`          | Level terdekat yang menetapkannya menentukan nilainya.                                                                                                                | `null`: Claude menggunakan model default produk |
| `environment_id` | Level terdekat yang menetapkannya menentukan nilainya.                                                                                                                | `null`                                          |
| `guest_policy`   | Level terdekat yang menetapkannya menentukan nilainya.                                                                                                                | `restrict`                                      |

Sebagai contoh, sebuah organisasi menyimpan instruksi pada default Slack-nya, menonaktifkan Claude pada sebuah workspace, dan menetapkan model pada satu channel di workspace tersebut. Jika dibaca dengan `include_inherited=true`, channel tersebut menunjukkan ketiga nilai dan asal masing-masing:

```json
{
  "type": "slack_channel",
  "id": "slch_011CZkZmRt4vNq8sHbYw2KdX",
  "slack": {
    "workspace_id": "T01ABCD2EFG",
    "channel_id": "C05HJKL6MNP"
  },
  "settings": {
    "enabled": false,
    "instructions": "Be brief.",
    "model": "claude-opus-5-5",
    "environment_id": null,
    "guest_policy": { "type": "restrict" }
  },
  "sources": {
    "enabled": {
      "type": "slack_workspace",
      "slack_workspace_id": "slws_011CZkZnWa7xPc3uJfZe5LgT"
    },
    "instructions": [{ "type": "slack_default" }],
    "model": {
      "type": "slack_channel",
      "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX"
    },
    "environment_id": { "type": "default" },
    "guest_policy": { "type": "default" }
  },
  "created_at": "2026-10-19T16:20:05Z",
  "updated_at": "2026-10-19T16:24:38Z"
}
```

Jika dibaca tanpa parameter tersebut, channel yang sama memiliki `model`-nya dan empat pengaturan `null` di `settings`; di `sources`, `model` menyebutkan channel, `instructions` berupa daftar kosong, dan tiga lainnya `null`.

Sebuah sumber adalah salah satu dari:

| `type`                 | Arti                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `slack_channel`        | Channel, disebutkan di `slack_channel_id`.                                                                                                                                                                                                                                                                                                                                  |
| `slack_workspace`      | Workspace, disebutkan di `slack_workspace_id`.                                                                                                                                                                                                                                                                                                                              |
| `slack_parent_channel` | Induk dari sebuah code channel, disebutkan di `slack_channel_id`. Code channel adalah channel yang dimulai dari channel lain. Selama induknya adalah channel publik di workspace yang sama, induk tersebut berada di antara channel dan workspace dan hanya menyumbangkan `instructions` dan `environment_id`.                                                              |
| `slack_grid_channel`   | Channel Slack yang sama seperti yang disiapkan di bawah workspace lain dari Slack Enterprise Grid-nya, disebutkan dengan ID milik Slack sendiri di bawah `slack`. Ini hanya menyumbangkan `enabled`: ketika baik channel maupun workspace-nya tidak menetapkan `enabled`, nilai `true` yang disimpan untuk channel tersebut di bawah workspace lain dari Grid yang berlaku. |
| `slack_default`        | Default Slack organisasi Anda, yang tidak memiliki ID.                                                                                                                                                                                                                                                                                                                      |
| `default`              | Tidak ada level yang menetapkan nilai, sehingga default bawaan yang berlaku.                                                                                                                                                                                                                                                                                                |

`sources.instructions` mencantumkan setiap level yang menyumbangkan teks, mulai dari yang paling luas, yang merupakan urutan teksnya di `settings.instructions`, dan kosong ketika tidak ada yang menyumbang. Daftar ini memberi tahu teks siapa yang muncul lebih dulu, bukan di mana teks satu level berakhir: untuk mendapatkan teks milik satu level, baca channel atau workspace tersebut tanpa `include_inherited`, atau, untuk default Slack, lihat di claude.ai. Sumber yang menyebutkan channel atau workspace selalu membawa ID-nya, yang tidak pernah `null`: `id` dari API ini di `slack_channel_id` atau `slack_workspace_id`, atau, pada `slack_grid_channel`, ID milik Slack sendiri di bawah `slack` seperti pada objek channel.

Dengan `include_inherited=true`, permintaan gagal dengan `503` jika sebuah level tidak dapat dibaca, alih-alih menjawab tanpa level tersebut.

### Mengubah pengaturan

Kedua endpoint pembaruan dan [Menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel) menerima objek `settings` dengan aturan yang sama:

* **Pengaturan yang Anda abaikan tidak berubah.** `{"settings": {"enabled": false}}` menonaktifkan Claude dan membiarkan empat pengaturan lainnya apa adanya.
* **Pengaturan yang Anda kirim sebagai `null` dihapus**, sehingga level tersebut kembali mewarisinya.
* **Semua atau tidak sama sekali.** Jika ada satu nilai dalam permintaan yang ditolak, tidak ada pengaturan dalam permintaan tersebut yang disimpan.
* **Aman untuk diulang.** Setiap perubahan meninggalkan resource dalam keadaan yang sama seperti yang ditinggalkan oleh permintaan identik pertama, sehingga tidak ada endpoint yang menerima `Idempotency-Key`. Permintaan yang tidak mengubah apa pun tidak menulis apa pun dan tidak mencatat event Activity Feed.
* **Penulisan terakhir yang menang.** Tidak ada permintaan yang menerima prasyarat. Dua pemanggil yang masing-masing membaca sebuah resource lalu mengubah pengaturan yang sama akan saling menimpa. `409` hanya dikembalikan ketika perubahan lain tumpang tindih dengan permintaan Anda saat permintaan tersebut berjalan; tidak ada yang diminta untuk diubah atau dihapus oleh permintaan Anda yang dilakukan, kecuali bahwa permintaan penyiapan mungkin sudah menyiapkan channel, jadi baca kembali resource tersebut dan kirim ulang perubahan jika masih diperlukan.

Perubahan pada `guest_policy` di sebuah channel dapat mengakhiri sesi yang sedang berjalan di channel tersebut. Sesi-sesi itu berakhir di latar belakang, dan respons tidak menunggunya.

### Mode hanya-baca

**API / Terraform read-only mode** adalah pengaturan yang diaktifkan dan dinonaktifkan oleh pemilik organisasi di pengaturan Claude Tag di claude.ai. Namanya menggambarkan claude.ai dan Slack: selama mode ini aktif, keduanya menolak perubahan yang dilakukan seseorang terhadap apa yang dikelola API ini, sehingga hanya kunci yang membuat perubahan tersebut. Keduanya juga menolak beberapa perubahan terkait yang tidak dilakukan oleh kunci mana pun, seperti mengubah pengaturan pada default Slack, sehingga tidak ada yang dapat melakukannya hingga pemilik menonaktifkan mode tersebut. Mode ini tidak membuat API ini menjadi hanya-baca. Setiap endpoint di halaman ini menjawab dengan cara yang sama baik mode ini aktif maupun tidak, dan tidak ada endpoint yang membaca atau mengubahnya.

Selama mode nonaktif, orang dan kunci mengubah pengaturan yang sama serta melampirkan dan melepaskan Bundle yang sama, dan setiap perubahan menggantikan apa yang tersimpan. Aktifkan mode ini jika pipeline Anda harus menjadi satu-satunya sumber perubahan.

Selama mode aktif, claude.ai dan Slack menolak:

* Mengubah salah satu dari lima pengaturan pada channel, workspace, atau default Slack (yang juga tidak diubah oleh kunci mana pun)
* Menyiapkan channel, menghapus channel, menambahkan workspace dari Enterprise Grid yang terhubung, atau memutuskan workspace atau Grid di claude.ai
* Melampirkan Bundle ke channel atau workspace, melepaskannya, atau menghapus Bundle yang dilampirkan ke salah satunya

Beberapa hal tetap dapat dilakukan dalam kedua keadaan: pemilik tetap dapat menghubungkan workspace atau Grid baru, membuat dan mengedit Bundle, serta mengubah pengaturan Claude Tag yang tidak dikelola API ini. Penggunaan pertama Claude tetap menyiapkan channel, atau workspace Grid yang belum disiapkan, menghapus channel di Slack tetap menghapusnya, dan meng-uninstall aplikasi Slack Claude tetap memutuskan workspace atau Grid tersebut.

Selama mode ini nonaktif, menyiapkan di claude.ai sebuah channel yang sudah disiapkan dapat menggantikan catatan channel tersebut, tetapi hanya channel yang belum menyimpan apa pun: channel yang disiapkan oleh penggunaan pertama Claude, atau yang disiapkan API ini tanpa `settings`, dan yang sejak itu belum ada yang menyimpan pengaturan atau melampirkan Bundle padanya. Channel tersebut kemudian memiliki `id` baru, dan `id` lama mengembalikan `404`. Channel lainnya mempertahankan `id`-nya hingga dihapus.

### Pesan langsung grup

Pesan langsung grup Slack memiliki ID dalam format channel, sehingga penggunaan Claude di dalamnya menyiapkannya seperti channel: ia memiliki `id`, dicantumkan, dan dapat dibaca. Menyiapkannya melalui API ini, mengubah pengaturan padanya, melampirkan Bundle padanya, dan menghapusnya masing-masing mengembalikan `400`, kecuali bahwa permintaan penyiapan yang menghilangkan `settings` untuk pesan langsung grup yang sudah disiapkan mengembalikannya dengan `200`, seperti pembacaan. Melepaskan Bundle darinya diperbolehkan.

## Contoh alur kerja

### Aktifkan Claude hanya di channel yang disetujui

Setiap anggota dapat mengundang Claude ke channel publik. Untuk menjaga Claude tetap aktif hanya di tempat yang telah Anda setujui:

1. Minta pemilik organisasi untuk menonaktifkan Claude di mana saja di claude.ai, dengan toggle **Enable Claude Tag in Slack** di bawah **Default Slack access**, yang menyimpan `enabled` sebagai `false` pada default Slack organisasi Anda. [Mode hanya-baca](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-only-mode) harus nonaktif saat mereka melakukannya.
2. Ketika sistem persetujuan Anda menyetujui sebuah channel, [siapkan channel tersebut](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel) dengan `"settings": {"enabled": true}`. Permintaan ini menerima ID milik Slack sendiri dan mengembalikan channel bahkan jika sudah disiapkan, sehingga aman untuk diulang.
3. Dalam proses yang sama, [lampirkan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#attach-a-bundle) Bundle yang disetujui untuk tim tersebut, sehingga sesi pertama channel sudah memiliki alatnya.

### Simpan konfigurasi dalam kontrol versi

1. Gunakan ID yang ditampilkan Slack untuk setiap channel sebagai kunci konfigurasi Anda, dan [temukan setiap channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#find-a-channel-by-its-slack-ids) berdasarkan ID tersebut.
2. Baca setiap channel tanpa `include_inherited` dan bandingkan `settings`-nya dengan apa yang dideklarasikan repositori Anda. Dengan parameter tersebut, nilai warisan akan tercampur.
3. Kirim hanya pengaturan yang berbeda, dan kirim `null` untuk pengaturan yang tidak lagi dideklarasikan repositori Anda.
4. Minta pemilik organisasi untuk mengaktifkan [mode hanya-baca](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-only-mode), agar tidak ada yang mengubah pengaturan yang sama secara manual.

### Audit apa yang berlaku di semua tempat

1. [Cantumkan workspace Anda](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-workspaces), lalu [cantumkan channel setiap workspace](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-channels), keduanya dengan `include_inherited=true` agar setiap item berisi apa yang berlaku di dalamnya. Jika organisasi Anda menghubungkan Enterprise Grid, cantumkan juga channel yang disimpan di bawah ID Slack milik Grid itu sendiri. Lihat [Channel dan workspace yang sudah disiapkan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-channels-and-workspaces).
2. Tandai apa yang dilarang oleh kebijakan Anda, seperti channel di mana `enabled` bernilai `true` tanpa persetujuan yang tercatat, atau di mana `guest_policy` bernilai `allow`.
3. [Cantumkan Bundle Anda](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-bundles), lalu [target setiap Bundle](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-a-bundles-targets), untuk melihat di mana akses ke sistem sensitif dilampirkan.

## Channel Slack

Objek channel menggambarkan satu channel Slack:

| Field        | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | `slack_channel`.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `id`         | Dengan prefiks `slch_`. Lihat [ID](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#ids).                                                                                                                                                                                                                                                                                                                                                |
| `slack`      | ID milik Slack sendiri: `workspace_id` untuk workspace tempat channel berada, dan `channel_id` untuk channel.                                                                                                                                                                                                                                                                                                                                            |
| `settings`   | Apa yang disimpan channel itu sendiri, atau, dengan `include_inherited=true`, apa yang berlaku di dalamnya. Selalu ada, dengan kelima [pengaturan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#settings); pengaturan yang tidak ditetapkan bernilai `null`. Lihat [Nilai tersimpan dan nilai warisan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#stored-and-inherited-values).                                |
| `sources`    | Untuk setiap pengaturan, level asal nilai di `settings`. Selalu ada.                                                                                                                                                                                                                                                                                                                                                                                     |
| `created_at` | Kapan channel disiapkan.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `updated_at` | Kapan catatan Claude Tag tentang channel terakhir berubah. Nilai ini bergerak pada setiap perubahan pengaturan, di sini, di claude.ai, atau di Slack, dan juga dapat bergerak karena perubahan yang tidak ditampilkan respons mana pun di sini. Anggap nilai yang lebih baru sebagai alasan untuk membaca channel lagi, bukan sebagai bukti bahwa sebuah pengaturan berubah. Melampirkan atau melepaskan Bundle tidak dengan sendirinya menggerakkannya. |

`id` yang bukan pengidentifikasi `slch_` yang valid mengembalikan `400`. `id` valid yang tidak menyebutkan channel organisasi Anda mengembalikan `404`.

### Menyiapkan channel

`POST /v1/organizations/claude_tag/slack_channels` menyiapkan channel Slack dan mengembalikannya. `slack.workspace_id` dan `slack.channel_id` wajib diisi dan merupakan ID milik Slack sendiri. `settings` bersifat opsional dan mengikuti [Mengubah pengaturan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#changing-settings). Jika channel sudah disiapkan, permintaan mengembalikan channel yang ada dan menerapkan `settings`; responsnya `200` dalam kedua kasus. Memerlukan cakupan `write:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{
      "slack": {"workspace_id": "T01ABCD2EFG", "channel_id": "C05HJKL6MNP"},
      "settings": {"instructions": "Answer in the language of the question."}
    }'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels create \
    --slack '{workspace_id: T01ABCD2EFG, channel_id: C05HJKL6MNP}' \
    --settings '{instructions: "Answer in the language of the question."}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  channel = client.beta.organization.claude_tag.slack_channels.create(
      slack={"workspace_id": "T01ABCD2EFG", "channel_id": "C05HJKL6MNP"},
      settings={"instructions": "Answer in the language of the question."},
  )

  print(channel.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channel = await client.beta.organization.claudeTag.slackChannels.create({
    slack: { workspace_id: "T01ABCD2EFG", channel_id: "C05HJKL6MNP" },
    settings: { instructions: "Answer in the language of the question." }
  });

  console.log(channel.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var channel = await client.Beta.Organization.ClaudeTag.SlackChannels.Create(
      new()
      {
          Slack = new() { WorkspaceID = "T01ABCD2EFG", ChannelID = "C05HJKL6MNP" },
          Settings = new() { Instructions = "Answer in the language of the question." },
      }
  );

  Console.WriteLine(channel.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  channel, err := client.Beta.Organization.ClaudeTag.SlackChannels.New(
  	context.Background(),
  	anthropic.BetaOrganizationClaudeTagSlackChannelNewParams{
  		Slack: anthropic.BetaClaudeTagSlackChannelIdentifiersParam{
  			WorkspaceID: "T01ABCD2EFG",
  			ChannelID:   "C05HJKL6MNP",
  		},
  		Settings: anthropic.BetaClaudeTagSettingsCreateParam{
  			Instructions: anthropic.String("Answer in the language of the question."),
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(channel.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagSettingsCreate;
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagSlackChannelIdentifiers;
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelCreateParams.builder()
          .slack(BetaClaudeTagSlackChannelIdentifiers.builder()
              .workspaceId("T01ABCD2EFG")
              .channelId("C05HJKL6MNP")
              .build())
          .settings(BetaClaudeTagSettingsCreate.builder()
              .instructions("Answer in the language of the question.")
              .build())
          .build();
      var channel = client.beta().organization().claudeTag().slackChannels().create(params);

      IO.println(channel.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $channel = $client->beta->organization->claudeTag->slackChannels->create(
      slack: ['workspaceID' => 'T01ABCD2EFG', 'channelID' => 'C05HJKL6MNP'],
      settings: ['instructions' => 'Answer in the language of the question.'],
  );

  echo "{$channel->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel = client.beta.organization.claude_tag.slack_channels.create(
    slack: {workspace_id: "T01ABCD2EFG", channel_id: "C05HJKL6MNP"},
    settings: {instructions: "Answer in the language of the question."}
  )

  puts channel.id
  ```
</CodeGroup>

```json Response
{
  "type": "slack_channel",
  "id": "slch_011CZkZmRt4vNq8sHbYw2KdX",
  "slack": {
    "workspace_id": "T01ABCD2EFG",
    "channel_id": "C05HJKL6MNP"
  },
  "settings": {
    "enabled": null,
    "instructions": "Answer in the language of the question.",
    "model": null,
    "environment_id": null,
    "guest_policy": null
  },
  "sources": {
    "enabled": null,
    "instructions": [
      {
        "type": "slack_channel",
        "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX"
      }
    ],
    "model": null,
    "environment_id": null,
    "guest_policy": null
  },
  "created_at": "2026-10-19T16:20:05Z",
  "updated_at": "2026-10-19T16:20:05Z"
}
```

Sebelum channel disiapkan, aplikasi Slack Claude mengonfirmasi dengan Slack bahwa channel tersebut berada di workspace, tidak diarsipkan, dan terlihat oleh aplikasi. Channel yang gagal dalam pemeriksaan tersebut mengembalikan `404`, demikian pula workspace yang tidak memiliki aplikasi Slack Claude terinstal. Untuk workspace yang dimiliki organisasi Anda melalui Enterprise Grid, aplikasi harus diinstal di Grid.

Menyiapkan channel dan menerapkan `settings` adalah dua langkah. Ketika permintaan ini menyiapkan channel lalu `settings` ditolak dengan `400`, `404`, atau `409`, responsnya adalah penolakan tersebut dan channel tetap disiapkan tanpa ada yang tersimpan (setelah `409`, kecuali jika perubahan yang tumpang tindih menghapus atau menggantikannya). Penolakan tersebut membawa `error_code` yang diawali `slack_channel_set_up_` dan `id` channel baru di `error.details.slack_channel_id` (lihat [Respons kesalahan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#error-responses)). Perbaiki `settings` dan kirimkan dalam [pembaruan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#update-a-channel) ke `id` tersebut, atau kirim ulang permintaan penyiapan. Jika channel sudah disiapkan, `settings` yang ditolak mengembalikan kesalahan yang sama seperti [pembaruan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#update-a-channel), dan channel mempertahankan apa yang disimpannya. `500` atau `503` dalam kedua kasus tidak membawa `error_code` dan tidak mengatakan apakah channel sudah disiapkan atau `settings` sudah tersimpan: kirim ulang permintaan penyiapan.

### Mencantumkan channel

`GET /v1/organizations/claude_tag/slack_channels` mencantumkan channel yang sudah disiapkan dari satu workspace, dari yang terbaru berdasarkan `created_at`. `slack_workspace_id` wajib diisi dan merupakan ID milik Slack sendiri untuk workspace tersebut. Tambahkan `include_inherited=true` agar setiap channel berisi apa yang berlaku di dalamnya (lihat [Nilai tersimpan dan nilai warisan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#stored-and-inherited-values)). Sebuah halaman dapat berisi channel lebih sedikit dari `limit`, atau tidak sama sekali, sementara `next_page` masih ditetapkan, jadi terus minta halaman hingga `next_page` bernilai `null` (lihat [Paginasi](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#pagination)). Memerlukan cakupan `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels?slack_workspace_id=T01ABCD2EFG" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels list --slack-workspace-id T01ABCD2EFG
  ```

  ```python Python
  client = anthropic.Anthropic()

  channels = client.beta.organization.claude_tag.slack_channels.list(
      slack_workspace_id="T01ABCD2EFG"
  )

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for channel in channels:
      print(f"{channel.id}: {channel.slack.channel_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channels = await client.beta.organization.claudeTag.slackChannels.list({
    slack_workspace_id: "T01ABCD2EFG"
  });

  for await (const channel of channels) {
    console.log(`${channel.id}: ${channel.slack.channel_id}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ClaudeTag.SlackChannels.List(
      new() { SlackWorkspaceID = "T01ABCD2EFG" }
  );

  await foreach (var channel in page.Paginate())
  {
      Console.WriteLine($"{channel.ID}: {channel.Slack.ChannelID}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  channels := client.Beta.Organization.ClaudeTag.SlackChannels.ListAutoPaging(
  	context.Background(),
  	anthropic.BetaOrganizationClaudeTagSlackChannelListParams{
  		SlackWorkspaceID: "T01ABCD2EFG",
  	},
  )

  for channels.Next() {
  	channel := channels.Current()
  	fmt.Printf("%s: %s\n", channel.ID, channel.Slack.ChannelID)
  }
  if err := channels.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelListParams.builder()
          .slackWorkspaceId("T01ABCD2EFG")
          .build();
      var channels = client.beta().organization().claudeTag().slackChannels().list(params);

      for (var channel : channels.autoPager()) {
          IO.println(channel.id() + ": " + channel.slack().channelId());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $channels = $client->beta->organization->claudeTag->slackChannels->list(
      slackWorkspaceID: 'T01ABCD2EFG',
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $channels->nextPage.
  foreach ($channels->getItems() as $channel) {
      echo "{$channel->id}: {$channel->slack->channelID}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.claude_tag.slack_channels.list(slack_workspace_id: "T01ABCD2EFG")

  page.auto_paging_each do |channel|
    puts "#{channel.id}: #{channel.slack.channel_id}"
  end
  ```
</CodeGroup>

Responsnya adalah `{"data": [...], "next_page": ...}`, di mana setiap item adalah objek channel. `slack_workspace_id` yang menyebutkan workspace yang bukan milik organisasi Anda mengembalikan `404`, demikian pula workspace yang dimilikinya hanya melalui Enterprise Grid hingga workspace tersebut disiapkan (lihat [Channel dan workspace yang sudah disiapkan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-channels-and-workspaces)).

### Menemukan channel berdasarkan ID Slack-nya

Tambahkan `slack_channel_id`, ID milik Slack sendiri untuk channel, untuk mencari satu channel. `data` berisi channel tersebut, atau kosong jika channel belum disiapkan. Di workspace yang belum disiapkan dan yang dimiliki organisasi Anda hanya melalui Enterprise Grid, channel yang belum disiapkan mengembalikan `404` sebagai gantinya. Pencarian tidak menggunakan paginasi: pencarian mengabaikan `page` dan `limit` apa pun dari 1 hingga 100 (`limit` di luar rentang tersebut tetap mengembalikan `400`), dan `next_page`-nya bernilai `null`. Beginilah cara Anda menemukan `id` sebuah channel.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels?slack_workspace_id=T01ABCD2EFG&slack_channel_id=C05HJKL6MNP" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels list \
    --slack-workspace-id T01ABCD2EFG \
    --slack-channel-id C05HJKL6MNP
  ```

  ```python Python
  client = anthropic.Anthropic()

  page = client.beta.organization.claude_tag.slack_channels.list(
      slack_workspace_id="T01ABCD2EFG",
      slack_channel_id="C05HJKL6MNP",
  )

  for channel in page.data:
      print(channel.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const page = await client.beta.organization.claudeTag.slackChannels.list({
    slack_workspace_id: "T01ABCD2EFG",
    slack_channel_id: "C05HJKL6MNP"
  });

  for (const channel of page.data) {
    console.log(channel.id);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ClaudeTag.SlackChannels.List(
      new() { SlackWorkspaceID = "T01ABCD2EFG", SlackChannelID = "C05HJKL6MNP" }
  );

  foreach (var channel in page.Items)
  {
      Console.WriteLine(channel.ID);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  page, err := client.Beta.Organization.ClaudeTag.SlackChannels.List(
  	context.Background(),
  	anthropic.BetaOrganizationClaudeTagSlackChannelListParams{
  		SlackWorkspaceID: "T01ABCD2EFG",
  		SlackChannelID:   anthropic.String("C05HJKL6MNP"),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  for _, channel := range page.Data {
  	fmt.Println(channel.ID)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelListParams.builder()
          .slackWorkspaceId("T01ABCD2EFG")
          .slackChannelId("C05HJKL6MNP")
          .build();
      var page = client.beta().organization().claudeTag().slackChannels().list(params);

      for (var channel : page.items()) {
          IO.println(channel.id());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $channels = $client->beta->organization->claudeTag->slackChannels->list(
      slackWorkspaceID: 'T01ABCD2EFG',
      slackChannelID: 'C05HJKL6MNP',
  );

  foreach ($channels->getItems() as $channel) {
      echo "{$channel->id}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.claude_tag.slack_channels.list(
    slack_workspace_id: "T01ABCD2EFG",
    slack_channel_id: "C05HJKL6MNP"
  )

  page.data&.each do |channel|
    puts channel.id
  end
  ```
</CodeGroup>

Mengirimkan ID `slch_` sebagai `slack_channel_id` mengembalikan `400`.

### Mendapatkan channel

`GET /v1/organizations/claude_tag/slack_channels/{id}` mengembalikan objek channel, yang berisi apa yang disimpan channel. Untuk membaca apa yang berlaku di dalamnya, lihat [Membaca apa yang berlaku di sebuah channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-what-applies-in-a-channel). Memerlukan cakupan `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels/slch_011CZkZmRt4vNq8sHbYw2KdX" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels retrieve \
    --id slch_011CZkZmRt4vNq8sHbYw2KdX
  ```

  ```python Python
  client = anthropic.Anthropic()

  channel = client.beta.organization.claude_tag.slack_channels.retrieve(
      "slch_011CZkZmRt4vNq8sHbYw2KdX"
  )

  print(channel.settings.enabled)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channel = await client.beta.organization.claudeTag.slackChannels.retrieve(
    "slch_011CZkZmRt4vNq8sHbYw2KdX"
  );

  console.log(channel.settings.enabled);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var channel = await client.Beta.Organization.ClaudeTag.SlackChannels.Retrieve(
      "slch_011CZkZmRt4vNq8sHbYw2KdX"
  );

  Console.WriteLine(channel.Settings.Enabled);
  ```

  ```go Go
  client := anthropic.NewClient()

  channel, err := client.Beta.Organization.ClaudeTag.SlackChannels.Get(
  	context.Background(),
  	"slch_011CZkZmRt4vNq8sHbYw2KdX",
  	anthropic.BetaOrganizationClaudeTagSlackChannelGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(channel.Settings.Enabled)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var channel = client.beta().organization().claudeTag().slackChannels()
      .retrieve("slch_011CZkZmRt4vNq8sHbYw2KdX");

  IO.println(channel.settings().enabled().orElse(null));
  ```

  ```php PHP
  $client = new Client();

  $channel = $client->beta->organization->claudeTag->slackChannels->retrieve(
      id: 'slch_011CZkZmRt4vNq8sHbYw2KdX',
  );

  echo json_encode($channel->settings->enabled) . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel_id = "slch_011CZkZmRt4vNq8sHbYw2KdX"
  channel = client.beta.organization.claude_tag.slack_channels.retrieve(channel_id)

  puts channel.settings.enabled
  ```
</CodeGroup>

### Membaca apa yang berlaku di sebuah channel

Permintaan yang sama dengan `include_inherited=true` mengembalikan objek channel dengan `settings` berisi apa yang berlaku di channel, dan `sources` yang menyatakan asal setiap nilai. [Nilai tersimpan dan nilai warisan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#stored-and-inherited-values) menunjukkan respons lengkap; `enabled` dan `guest_policy` tidak pernah `null` di dalamnya. Jika sebuah level tidak dapat dibaca, permintaan gagal dengan `503` alih-alih menjawab tanpa level tersebut. Memerlukan cakupan `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels/slch_011CZkZmRt4vNq8sHbYw2KdX?include_inherited=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels retrieve \
    --id slch_011CZkZmRt4vNq8sHbYw2KdX \
    --include-inherited
  ```

  ```python Python
  client = anthropic.Anthropic()

  channel = client.beta.organization.claude_tag.slack_channels.retrieve(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      include_inherited=True,
  )

  print(channel.settings.instructions)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channel = await client.beta.organization.claudeTag.slackChannels.retrieve(
    "slch_011CZkZmRt4vNq8sHbYw2KdX",
    { include_inherited: true }
  );

  console.log(channel.settings.instructions);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var channel = await client.Beta.Organization.ClaudeTag.SlackChannels.Retrieve(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      new() { IncludeInherited = true }
  );

  Console.WriteLine(channel.Settings.Instructions);
  ```

  ```go Go
  client := anthropic.NewClient()

  channel, err := client.Beta.Organization.ClaudeTag.SlackChannels.Get(
  	context.Background(),
  	"slch_011CZkZmRt4vNq8sHbYw2KdX",
  	anthropic.BetaOrganizationClaudeTagSlackChannelGetParams{
  		IncludeInherited: anthropic.Bool(true),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(channel.Settings.Instructions)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelRetrieveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelRetrieveParams.builder()
          .includeInherited(true)
          .build();
      var channel = client.beta().organization().claudeTag().slackChannels()
          .retrieve("slch_011CZkZmRt4vNq8sHbYw2KdX", params);

      IO.println(channel.settings().instructions().orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $channel = $client->beta->organization->claudeTag->slackChannels->retrieve(
      id: 'slch_011CZkZmRt4vNq8sHbYw2KdX',
      includeInherited: true,
  );

  echo "{$channel->settings->instructions}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel_id = "slch_011CZkZmRt4vNq8sHbYw2KdX"
  channel = client.beta.organization.claude_tag.slack_channels.retrieve(channel_id, include_inherited: true)

  puts channel.settings.instructions
  ```
</CodeGroup>

### Memperbarui channel

`POST /v1/organizations/claude_tag/slack_channels/{id}` mengubah pengaturan channel dan mengembalikan objek channel. `settings` wajib diisi dan mengikuti [Mengubah pengaturan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#changing-settings). Memerlukan scope `write:claude_tag`.

Nonaktifkan Claude di satu channel dan biarkan pengaturan lainnya apa adanya:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels/slch_011CZkZmRt4vNq8sHbYw2KdX" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{"settings": {"enabled": false}}'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels update \
    --id slch_011CZkZmRt4vNq8sHbYw2KdX \
    --settings '{enabled: false}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  channel = client.beta.organization.claude_tag.slack_channels.update(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      settings={"enabled": False},
  )

  print(channel.settings.enabled)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channel = await client.beta.organization.claudeTag.slackChannels.update(
    "slch_011CZkZmRt4vNq8sHbYw2KdX",
    { settings: { enabled: false } }
  );

  console.log(channel.settings.enabled);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var channel = await client.Beta.Organization.ClaudeTag.SlackChannels.Update(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      new() { Settings = new() { Enabled = false } }
  );

  Console.WriteLine(channel.Settings.Enabled);
  ```

  ```go Go
  client := anthropic.NewClient()

  channel, err := client.Beta.Organization.ClaudeTag.SlackChannels.Update(
  	context.Background(),
  	"slch_011CZkZmRt4vNq8sHbYw2KdX",
  	anthropic.BetaOrganizationClaudeTagSlackChannelUpdateParams{
  		Settings: anthropic.BetaClaudeTagSettingsUpdateParam{
  			Enabled: anthropic.Bool(false),
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(channel.Settings.Enabled)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagSettingsUpdate;
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelUpdateParams.builder()
          .settings(BetaClaudeTagSettingsUpdate.builder()
              .enabled(false)
              .build())
          .build();
      var channel = client.beta().organization().claudeTag().slackChannels()
          .update("slch_011CZkZmRt4vNq8sHbYw2KdX", params);

      IO.println(channel.settings().enabled().orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $channel = $client->beta->organization->claudeTag->slackChannels->update(
      id: 'slch_011CZkZmRt4vNq8sHbYw2KdX',
      settings: ['enabled' => false],
  );

  echo json_encode($channel->settings->enabled) . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel_id = "slch_011CZkZmRt4vNq8sHbYw2KdX"
  channel = client.beta.organization.claude_tag.slack_channels.update(
    channel_id,
    settings: {enabled: false}
  )

  puts channel.settings.enabled
  ```
</CodeGroup>

Hapus instruksi channel, sehingga hanya instruksi yang diwarisi yang berlaku:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels/slch_011CZkZmRt4vNq8sHbYw2KdX" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{"settings": {"instructions": null}}'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels update \
    --id slch_011CZkZmRt4vNq8sHbYw2KdX \
    --settings '{instructions: null}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  channel = client.beta.organization.claude_tag.slack_channels.update(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      settings={"instructions": None},
  )

  print(channel.settings.instructions)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const channel = await client.beta.organization.claudeTag.slackChannels.update(
    "slch_011CZkZmRt4vNq8sHbYw2KdX",
    { settings: { instructions: null } }
  );

  console.log(channel.settings.instructions);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var channel = await client.Beta.Organization.ClaudeTag.SlackChannels.Update(
      "slch_011CZkZmRt4vNq8sHbYw2KdX",
      new() { Settings = new() { Instructions = null } }
  );

  Console.WriteLine(channel.Settings.Instructions);
  ```

  ```go Go
  client := anthropic.NewClient()

  channel, err := client.Beta.Organization.ClaudeTag.SlackChannels.Update(
  	context.Background(),
  	"slch_011CZkZmRt4vNq8sHbYw2KdX",
  	anthropic.BetaOrganizationClaudeTagSlackChannelUpdateParams{
  		Settings: anthropic.BetaClaudeTagSettingsUpdateParam{
  			Instructions: param.Null[string](),
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(channel.Settings.Instructions)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagSettingsUpdate;
  import com.anthropic.models.beta.organization.claudetag.slackchannels.SlackChannelUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackChannelUpdateParams.builder()
          .settings(BetaClaudeTagSettingsUpdate.builder()
              .instructions(Optional.empty())
              .build())
          .build();
      var channel = client.beta().organization().claudeTag().slackChannels()
          .update("slch_011CZkZmRt4vNq8sHbYw2KdX", params);

      IO.println(channel.settings().instructions().orElse(null));
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\ClaudeTag\ClaudeTagSettingsUpdate;
  // ...

  $client = new Client();

  // update() membuang nilai null di dalam array, jadi susun objek settings agar mengirim null.
  $channel = $client->beta->organization->claudeTag->slackChannels->update(
      id: 'slch_011CZkZmRt4vNq8sHbYw2KdX',
      settings: (new ClaudeTagSettingsUpdate())->withInstructions(null),
  );

  echo "{$channel->settings->instructions}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel_id = "slch_011CZkZmRt4vNq8sHbYw2KdX"
  channel = client.beta.organization.claude_tag.slack_channels.update(
    channel_id,
    settings: {instructions: nil}
  )

  puts channel.settings.instructions
  ```
</CodeGroup>

### Menghapus channel

`DELETE /v1/organizations/claude_tag/slack_channels/{id}` menghapus sebuah channel dari Claude Tag. Ini adalah penghapusan yang sama dengan yang dilakukan pemilik organisasi di claude.ai, dengan efek yang sama. Ini tidak menghapus, mengarsipkan, atau mengubah channel di Slack, maupun pesan apa pun di dalamnya. Memerlukan scope `write:claude_tag`.

<Warning>
  Penghapusan tidak dapat dibatalkan. Ini menghapus apa yang disimpan Claude Tag untuk channel tersebut:

  * pengaturan tersimpannya dan target Bundle-nya
  * sesi-sesinya beserta transkripnya, termasuk sesi yang sedang berjalan
  * memorinya, yaitu apa yang disimpan Claude tentang channel tersebut dari satu sesi ke sesi berikutnya
  * routine-nya dan artefak yang dipublikasikan darinya
</Warning>

**Sebuah channel hanya dapat dihapus selama Claude nonaktif di dalamnya.** Selama `enabled` terselesaikan menjadi `true` untuk channel tersebut, sebagaimana dikembalikan oleh [Membaca apa yang berlaku di sebuah channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-what-applies-in-a-channel), permintaan mengembalikan `400` dengan `error_code: "slack_channel_enabled"`. Tetapkan `enabled` ke `false` pada channel terlebih dahulu, lalu kirim ulang permintaan. Satu-satunya pengecualian adalah organisasi dengan [konfigurasi kepatuhan yang dibatasi](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#error-responses): organisasi tersebut tidak dapat membuat perubahan itu, sehingga permintaannya menghapus channel baik Claude aktif di dalamnya maupun tidak. Jika sebuah level yang diperlukan pemeriksaan ini tidak dapat dibaca, permintaan mengembalikan `503` dan tidak menghapus apa pun.

Pemeriksaan ini melindungi dari penghapusan keliru terhadap channel yang sedang digunakan. Pemeriksaan ini tidak menjauhkan Claude dari channel setelahnya. Penghapusan menghapus pengaturan milik channel itu sendiri, termasuk `enabled` bernilai `false`, sehingga sejak saat itu hanya apa yang diwarisi channel yang menentukan apakah Claude aktif di sana. Jika hal itu mengaktifkan Claude, Claude akan menjawab di channel lagi pada penyebutan berikutnya, dan penggunaan tersebut menyiapkan channel dari awal: `id` baru, tanpa pengaturan sendiri, dan tanpa memori dari channel yang dihapus.

* Untuk menjauhkan Claude dari sebuah channel, biarkan channel tetap disiapkan dengan `enabled` ditetapkan ke `false` alih-alih menghapusnya, atau pastikan bahwa apa yang akan diwarisinya, yang tidak tersentuh oleh penghapusan, tetap menonaktifkan Claude.
* Agar sebuah channel tidak menyimpan apa pun namun tetap mempertahankan sesi dan memorinya, hapus setiap pengaturan dan lepaskan setiap Bundle sebagai gantinya.

Dua jenis channel sama sekali tidak dapat dihapus di sini, baik Claude aktif maupun nonaktif di dalamnya, dan mengembalikan `400` tanpa `error_code`: [pesan langsung grup](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#group-direct-messages), dan channel yang menyimpan konfigurasi yang tidak dikelola API ini, seperti runner pool atau pengaturan yang hanya dimiliki claude.ai. Hal-hal ini diperiksa sebelum `enabled`, sehingga menonaktifkan Claude tidak membantu; pemilik organisasi menghapus jenis kedua di claude.ai.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/claude_tag/slack_channels/slch_011CZkZmRt4vNq8sHbYw2KdX" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-channels delete \
    --id slch_011CZkZmRt4vNq8sHbYw2KdX
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_channel = client.beta.organization.claude_tag.slack_channels.delete(
      "slch_011CZkZmRt4vNq8sHbYw2KdX"
  )

  print(deleted_channel.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedChannel = await client.beta.organization.claudeTag.slackChannels.delete(
    "slch_011CZkZmRt4vNq8sHbYw2KdX"
  );

  console.log(deletedChannel.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedChannel = await client.Beta.Organization.ClaudeTag.SlackChannels.Delete(
      "slch_011CZkZmRt4vNq8sHbYw2KdX"
  );

  Console.WriteLine(deletedChannel.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedChannel, err := client.Beta.Organization.ClaudeTag.SlackChannels.Delete(
  	context.Background(),
  	"slch_011CZkZmRt4vNq8sHbYw2KdX",
  	anthropic.BetaOrganizationClaudeTagSlackChannelDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(deletedChannel.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedChannel = client.beta().organization().claudeTag().slackChannels()
      .delete("slch_011CZkZmRt4vNq8sHbYw2KdX");

  IO.println(deletedChannel.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedChannel = $client->beta->organization->claudeTag->slackChannels->delete(
      id: 'slch_011CZkZmRt4vNq8sHbYw2KdX',
  );

  echo "{$deletedChannel->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  channel_id = "slch_011CZkZmRt4vNq8sHbYw2KdX"
  deleted_channel = client.beta.organization.claude_tag.slack_channels.delete(channel_id)

  puts deleted_channel.id
  ```
</CodeGroup>

```json Response
{
  "type": "slack_channel_deleted",
  "id": "slch_011CZkZmRt4vNq8sHbYw2KdX"
}
```

`id` mengembalikan `404` segera setelah permintaan kembali, dan sisanya dihapus di latar belakang. Penghapusan berulang mengembalikan `404`, jadi jika Anda mengirim ulang penghapusan setelah `503`, `404` berarti channel sudah tidak ada.

## Workspace Slack

Objek workspace menggambarkan satu workspace Slack. Objek ini memiliki field yang sama dengan [objek channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#slack-channels), kecuali bahwa `type` adalah `slack_workspace`, `id` memiliki prefiks `slws_`, dan `slack` hanya berisi `workspace_id`. Respons [Mulai cepat](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#quick-start) menunjukkan contoh lengkapnya. Jika dibaca dengan `include_inherited=true`, workspace menunjukkan setiap pengaturan sebagaimana diselesaikan oleh workspace dan default Slack, yaitu apa yang diwarisi channel dari workspace tersebut kecuali level yang lebih dekat menetapkan pengaturan tersebut.

`id` yang bukan pengidentifikasi `slws_` yang valid mengembalikan `400`. `id` valid yang tidak menyebutkan workspace organisasi Anda mengembalikan `404`.

### Mencantumkan workspace

`GET /v1/organizations/claude_tag/slack_workspaces` mencantumkan workspace yang sudah disiapkan yang dimiliki organisasi Anda, dari yang terbaru berdasarkan `created_at`. [Mulai cepat](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#quick-start) menunjukkan permintaan dan responsnya. Untuk menemukan satu workspace berdasarkan ID milik Slack sendiri, tambahkan `slack_workspace_id`: `data` berisi workspace tersebut, atau kosong jika belum disiapkan, dan workspace yang bukan milik organisasi Anda mengembalikan `404`. Workspace yang dimilikinya hanya melalui Enterprise Grid juga mengembalikan `404` hingga disiapkan. Tambahkan `include_inherited=true` agar setiap workspace berisi apa yang berlaku di dalamnya (lihat [Nilai tersimpan dan nilai warisan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#stored-and-inherited-values)). Memerlukan cakupan `read:claude_tag`.

### Mendapatkan workspace

`GET /v1/organizations/claude_tag/slack_workspaces/{id}` mengembalikan objek workspace, yang berisi apa yang disimpan workspace, atau, dengan `include_inherited=true` di query seperti pada [Membaca apa yang berlaku di sebuah channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#read-what-applies-in-a-channel), apa yang berlaku di dalamnya. Memerlukan cakupan `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/slack_workspaces/slws_011CZkZnWa7xPc3uJfZe5LgT" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-workspaces retrieve \
    --id slws_011CZkZnWa7xPc3uJfZe5LgT
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.claude_tag.slack_workspaces.retrieve(
      "slws_011CZkZnWa7xPc3uJfZe5LgT"
  )

  print(workspace.settings.instructions)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.claudeTag.slackWorkspaces.retrieve(
    "slws_011CZkZnWa7xPc3uJfZe5LgT"
  );

  console.log(workspace.settings.instructions);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.ClaudeTag.SlackWorkspaces.Retrieve(
      "slws_011CZkZnWa7xPc3uJfZe5LgT"
  );

  Console.WriteLine(workspace.Settings.Instructions);
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Beta.Organization.ClaudeTag.SlackWorkspaces.Get(
  	context.Background(),
  	"slws_011CZkZnWa7xPc3uJfZe5LgT",
  	anthropic.BetaOrganizationClaudeTagSlackWorkspaceGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(workspace.Settings.Instructions)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var workspace = client.beta().organization().claudeTag().slackWorkspaces()
      .retrieve("slws_011CZkZnWa7xPc3uJfZe5LgT");

  IO.println(workspace.settings().instructions().orElse(null));
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->claudeTag->slackWorkspaces->retrieve(
      id: 'slws_011CZkZnWa7xPc3uJfZe5LgT',
  );

  echo "{$workspace->settings->instructions}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "slws_011CZkZnWa7xPc3uJfZe5LgT"
  workspace = client.beta.organization.claude_tag.slack_workspaces.retrieve(workspace_id)

  puts workspace.settings.instructions
  ```
</CodeGroup>

### Memperbarui workspace

`POST /v1/organizations/claude_tag/slack_workspaces/{id}` mengubah pengaturan workspace dan mengembalikan objek workspace. `settings` wajib diisi dan mengikuti [Mengubah pengaturan](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#changing-settings). Apa yang Anda tetapkan di sini berlaku di setiap channel workspace yang tidak menetapkan nilainya sendiri, kecuali `instructions`, yang ditambahkan oleh setiap channel dengan miliknya sendiri alih-alih diganti. Memerlukan cakupan `write:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/slack_workspaces/slws_011CZkZnWa7xPc3uJfZe5LgT" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{"settings": {"guest_policy": {"type": "restrict"}}}'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:slack-workspaces update \
    --id slws_011CZkZnWa7xPc3uJfZe5LgT \
    --settings '{guest_policy: {type: restrict}}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.claude_tag.slack_workspaces.update(
      "slws_011CZkZnWa7xPc3uJfZe5LgT",
      settings={"guest_policy": {"type": "restrict"}},
  )

  print(workspace.settings.guest_policy)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.claudeTag.slackWorkspaces.update(
    "slws_011CZkZnWa7xPc3uJfZe5LgT",
    { settings: { guest_policy: { type: "restrict" } } }
  );

  console.log(workspace.settings.guest_policy?.type);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ClaudeTag;

  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.ClaudeTag.SlackWorkspaces.Update(
      "slws_011CZkZnWa7xPc3uJfZe5LgT",
      new() { Settings = new() { GuestPolicy = new BetaClaudeTagGuestPolicyRestrict() } }
  );

  Console.WriteLine(workspace.Settings.GuestPolicy?.Type.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Beta.Organization.ClaudeTag.SlackWorkspaces.Update(
  	context.Background(),
  	"slws_011CZkZnWa7xPc3uJfZe5LgT",
  	anthropic.BetaOrganizationClaudeTagSlackWorkspaceUpdateParams{
  		Settings: anthropic.BetaClaudeTagSettingsUpdateParam{
  			GuestPolicy: anthropic.BetaClaudeTagGuestPolicyUnionParam{
  				OfRestrict: &anthropic.BetaClaudeTagGuestPolicyRestrictParam{},
  			},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(workspace.Settings.GuestPolicy.Type)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagGuestPolicyRestrict;
  import com.anthropic.models.beta.organization.claudetag.BetaClaudeTagSettingsUpdate;
  import com.anthropic.models.beta.organization.claudetag.slackworkspaces.SlackWorkspaceUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SlackWorkspaceUpdateParams.builder()
          .settings(BetaClaudeTagSettingsUpdate.builder()
              .guestPolicy(BetaClaudeTagGuestPolicyRestrict.builder().build())
              .build())
          .build();
      var workspace = client.beta().organization().claudeTag().slackWorkspaces()
          .update("slws_011CZkZnWa7xPc3uJfZe5LgT", params);

      IO.println(workspace.settings().guestPolicy().map(policy -> policy.type().asString()).orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->claudeTag->slackWorkspaces->update(
      id: 'slws_011CZkZnWa7xPc3uJfZe5LgT',
      settings: ['guestPolicy' => ['type' => 'restrict']],
  );

  echo "{$workspace->settings->guestPolicy?->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "slws_011CZkZnWa7xPc3uJfZe5LgT"
  workspace = client.beta.organization.claude_tag.slack_workspaces.update(
    workspace_id,
    settings: {guest_policy: {type: :restrict}}
  )

  puts workspace.settings.guest_policy&.type
  ```
</CodeGroup>

## Bundle

Bundle adalah apa yang disebut claude.ai sebagai [Access bundle](https://claude.com/docs/claude-tag/admins/add-connections): sekumpulan akses bernama, seperti konektor, repositori, dan kredensial, yang dapat digunakan Claude di sebuah channel atau workspace. Pemilik organisasi membuat, mengedit, dan menghapus Bundle di claude.ai. API ini mencantumkan dan melampirkannya. API ini mengembalikan nama dan deskripsi Bundle dan tidak pernah mengembalikan apa yang diberikan oleh Bundle tersebut.

| Field                      | Deskripsi                                |
| -------------------------- | ---------------------------------------- |
| `type`                     | `bundle`.                                |
| `id`                       | Diawali dengan `capp_`.                  |
| `display_name`             | Nama Bundle.                             |
| `description`              | Kegunaan Bundle. `null` jika tidak ada.  |
| `created_at`, `updated_at` | Kapan Bundle dibuat dan terakhir diubah. |

`bundle_id` yang bukan pengidentifikasi `capp_` yang valid mengembalikan `400`. `bundle_id` valid yang tidak ada atau dimiliki organisasi lain mengembalikan `404`, apa pun isi permintaan lainnya. Bundle yang dikelola Claude Tag untuk dirinya sendiri tidak dicantumkan dan mengembalikan `404`.

### Mencantumkan Bundle

`GET /v1/organizations/claude_tag/bundles` mencantumkan Bundle organisasi Anda, yang terbaru lebih dulu berdasarkan `created_at`. Memerlukan scope `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/bundles" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles list
  ```

  ```python Python
  client = anthropic.Anthropic()

  bundles = client.beta.organization.claude_tag.bundles.list()

  # Otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for bundle in bundles:
      print(f"{bundle.id}: {bundle.display_name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const bundles = await client.beta.organization.claudeTag.bundles.list();

  for await (const bundle of bundles) {
    console.log(`${bundle.id}: ${bundle.display_name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ClaudeTag.Bundles.List();

  await foreach (var bundle in page.Paginate())
  {
      Console.WriteLine($"{bundle.ID}: {bundle.DisplayName}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  bundles := client.Beta.Organization.ClaudeTag.Bundles.ListAutoPaging(
  	context.Background(),
  	anthropic.BetaOrganizationClaudeTagBundleListParams{},
  )

  for bundles.Next() {
  	bundle := bundles.Current()
  	fmt.Printf("%s: %s\n", bundle.ID, bundle.DisplayName)
  }
  if err := bundles.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var bundles = client.beta().organization().claudeTag().bundles().list();

  for (var bundle : bundles.autoPager()) {
      IO.println(bundle.id() + ": " + bundle.displayName());
  }
  ```

  ```php PHP
  $client = new Client();

  $bundles = $client->beta->organization->claudeTag->bundles->list();

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $bundles->nextPage.
  foreach ($bundles->getItems() as $bundle) {
      echo "{$bundle->id}: {$bundle->displayName}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.claude_tag.bundles.list

  page.auto_paging_each do |bundle|
    puts "#{bundle.id}: #{bundle.display_name}"
  end
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "type": "bundle",
      "id": "capp_011CZkZjLP1cWxj5EtMmdgbq",
      "display_name": "Support tools",
      "description": "Issue tracker and the support runbooks repository.",
      "created_at": "2026-09-12T08:15:30Z",
      "updated_at": "2026-09-30T13:02:47Z"
    }
  ],
  "next_page": null
}
```

### Mendapatkan Bundle

`GET /v1/organizations/claude_tag/bundles/{bundle_id}` mengembalikan objek Bundle. Memerlukan scope `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles retrieve \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq
  ```

  ```python Python
  client = anthropic.Anthropic()

  bundle = client.beta.organization.claude_tag.bundles.retrieve(
      "capp_011CZkZjLP1cWxj5EtMmdgbq"
  )

  print(bundle.display_name)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const bundle = await client.beta.organization.claudeTag.bundles.retrieve(
    "capp_011CZkZjLP1cWxj5EtMmdgbq"
  );

  console.log(bundle.display_name);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var bundle = await client.Beta.Organization.ClaudeTag.Bundles.Retrieve(
      "capp_011CZkZjLP1cWxj5EtMmdgbq"
  );

  Console.WriteLine(bundle.DisplayName);
  ```

  ```go Go
  client := anthropic.NewClient()

  bundle, err := client.Beta.Organization.ClaudeTag.Bundles.Get(
  	context.Background(),
  	"capp_011CZkZjLP1cWxj5EtMmdgbq",
  	anthropic.BetaOrganizationClaudeTagBundleGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(bundle.DisplayName)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var bundle = client.beta().organization().claudeTag().bundles()
      .retrieve("capp_011CZkZjLP1cWxj5EtMmdgbq");

  IO.println(bundle.displayName());
  ```

  ```php PHP
  $client = new Client();

  $bundle = $client->beta->organization->claudeTag->bundles->retrieve(
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
  );

  echo "{$bundle->displayName}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  bundle = client.beta.organization.claude_tag.bundles.retrieve(bundle_id)

  puts bundle.display_name
  ```
</CodeGroup>

## Target Bundle

Target Bundle adalah catatan dari satu Bundle yang dilampirkan ke satu channel atau satu workspace. Bundle yang dilampirkan ke sebuah workspace dapat digunakan di workspace tersebut dan di setiap channel di dalamnya. Bundle yang dilampirkan ke sebuah channel hanya dapat digunakan di channel tersebut.

| Field                | Deskripsi                                                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `type`               | `slack_channel` atau `slack_workspace`.                                                                                                |
| `id`                 | Diawali dengan `btgt_`. Ini adalah `{target_id}` dalam path, dan tidak pernah merupakan `id` milik channel atau workspace itu sendiri. |
| `slack_channel_id`   | Pada target `slack_channel`: `id` channel, diawali dengan `slch_`.                                                                     |
| `slack_workspace_id` | Pada target `slack_workspace`: `id` workspace, diawali dengan `slws_`.                                                                 |
| `created_at`         | Kapan Bundle dilampirkan.                                                                                                              |

Sebuah Bundle dilampirkan ke sebuah channel atau workspace paling banyak satu kali, dan pasangan yang sama selalu memiliki `id` yang sama, juga setelah dilepaskan dan dilampirkan kembali. `id` bersifat opaque: dapatkan dari respons pelampiran atau dari daftar. Target Bundle tidak menyimpan `id` Bundle-nya, yang juga diperlukan oleh path-nya, jadi simpan keduanya bersama-sama.

Melampirkan atau melepaskan tidak mengubah pengaturan tersimpan apa pun. Sesi yang sedang berjalan di channel atau workspace diberi tahu bahwa aksesnya berubah.

Bundle yang dilampirkan claude.ai sebagai bagian dari penyiapan on-call dicantumkan dan dapat dibaca, tetapi tidak dapat dilampirkan atau dilepaskan di sini, dan tidak ada yang dapat dilampirkan ke atau dilepaskan dari channel atau workspace yang dikelola oleh penyiapan on-call. Setiap permintaan tersebut mengembalikan `400`.

### Mencantumkan target Bundle

`GET /v1/organizations/claude_tag/bundles/{bundle_id}/targets` mencantumkan channel dan workspace tempat Bundle dilampirkan, yang terbaru lebih dulu berdasarkan `created_at`. Memerlukan scope `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq/targets" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles:targets list \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq
  ```

  ```python Python
  client = anthropic.Anthropic()

  targets = client.beta.organization.claude_tag.bundles.targets.list(
      "capp_011CZkZjLP1cWxj5EtMmdgbq"
  )

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for target in targets:
      print(f"{target.id}: {target.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const targets = await client.beta.organization.claudeTag.bundles.targets.list(
    "capp_011CZkZjLP1cWxj5EtMmdgbq"
  );

  for await (const target of targets) {
    console.log(`${target.id}: ${target.type}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ClaudeTag.Bundles.Targets.List(
      "capp_011CZkZjLP1cWxj5EtMmdgbq"
  );

  await foreach (var target in page.Paginate())
  {
      Console.WriteLine($"{target.ID}: {target.Type.Raw()}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  targets := client.Beta.Organization.ClaudeTag.Bundles.Targets.ListAutoPaging(
  	context.Background(),
  	"capp_011CZkZjLP1cWxj5EtMmdgbq",
  	anthropic.BetaOrganizationClaudeTagBundleTargetListParams{},
  )

  for targets.Next() {
  	target := targets.Current()
  	fmt.Printf("%s: %s\n", target.ID, target.Type)
  }
  if err := targets.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var targets = client.beta().organization().claudeTag().bundles().targets()
      .list("capp_011CZkZjLP1cWxj5EtMmdgbq");

  for (var target : targets.autoPager()) {
      IO.println(target.id() + ": " + target.type().asString());
  }
  ```

  ```php PHP
  $client = new Client();

  $targets = $client->beta->organization->claudeTag->bundles->targets->list(
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $targets->nextPage.
  foreach ($targets->getItems() as $target) {
      echo "{$target->id}: {$target->type}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  page = client.beta.organization.claude_tag.bundles.targets.list(bundle_id)

  page.auto_paging_each do |target|
    puts "#{target.id}: #{target.type}"
  end
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "type": "slack_channel",
      "id": "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
      "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX",
      "created_at": "2026-10-19T16:21:44Z"
    },
    {
      "type": "slack_workspace",
      "id": "btgt_011CZkZuMc3dVk7xQpGw9StZ1CZkZxRe6gTk9uNyVs4adJ",
      "slack_workspace_id": "slws_011CZkZnWa7xPc3uJfZe5LgT",
      "created_at": "2026-09-12T08:17:02Z"
    }
  ],
  "next_page": null
}
```

Hanya lampiran ke channel dan workspace yang dicantumkan. Bundle yang dilampirkan di claude.ai ke hal lain, seperti **Default Slack access**, tidak memiliki target Bundle untuk itu, begitu pula aturan yang menerapkan sebuah Bundle di banyak channel sekaligus. Jadi, Bundle yang dapat digunakan Claude di sebuah channel bisa lebih banyak daripada target yang menyebutkannya. Tidak ada endpoint yang mencantumkan Bundle yang dilampirkan ke satu channel atau workspace.

### Melampirkan Bundle

`POST /v1/organizations/claude_tag/bundles/{bundle_id}/targets` melampirkan Bundle dan mengembalikan target Bundle. Body menyebutkan `type` dan `id` yang sesuai. Channel atau workspace harus sudah disiapkan: melampirkan tidak pernah menyiapkan sebuah channel. Melampirkan pasangan yang sudah dilampirkan mengembalikan `200` dengan target Bundle yang sudah ada. Memerlukan scope `write:claude_tag`.

Lampirkan Bundle ke sebuah channel:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq/targets" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{
      "type": "slack_channel",
      "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX"
    }'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles:targets create \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq \
    --target '{type: slack_channel, slack_channel_id: slch_011CZkZmRt4vNq8sHbYw2KdX}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  target = client.beta.organization.claude_tag.bundles.targets.create(
      "capp_011CZkZjLP1cWxj5EtMmdgbq",
      target={
          "type": "slack_channel",
          "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX",
      },
  )

  print(target.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const target = await client.beta.organization.claudeTag.bundles.targets.create(
    "capp_011CZkZjLP1cWxj5EtMmdgbq",
    { target: { type: "slack_channel", slack_channel_id: "slch_011CZkZmRt4vNq8sHbYw2KdX" } }
  );

  console.log(target.id);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ClaudeTag.Bundles.Targets;

  AnthropicClient client = new();

  var target = await client.Beta.Organization.ClaudeTag.Bundles.Targets.Create(
      "capp_011CZkZjLP1cWxj5EtMmdgbq",
      new()
      {
          Target = new BetaClaudeTagSlackChannelBundleTargetCreate
          {
              SlackChannelID = "slch_011CZkZmRt4vNq8sHbYw2KdX",
          },
      }
  );

  Console.WriteLine(target.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  target, err := client.Beta.Organization.ClaudeTag.Bundles.Targets.New(
  	context.Background(),
  	"capp_011CZkZjLP1cWxj5EtMmdgbq",
  	anthropic.BetaOrganizationClaudeTagBundleTargetNewParams{
  		Target: anthropic.BetaClaudeTagBundleTargetCreateUnionParam{
  			OfSlackChannel: &anthropic.BetaClaudeTagSlackChannelBundleTargetCreateParam{
  				SlackChannelID: "slch_011CZkZmRt4vNq8sHbYw2KdX",
  			},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(target.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.bundles.targets.TargetCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = TargetCreateParams.builder()
          .slackChannelTarget("slch_011CZkZmRt4vNq8sHbYw2KdX")
          .build();
      var target = client.beta().organization().claudeTag().bundles().targets()
          .create("capp_011CZkZjLP1cWxj5EtMmdgbq", params);

      IO.println(target.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $target = $client->beta->organization->claudeTag->bundles->targets->create(
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
      target: [
          'type' => 'slack_channel',
          'slackChannelID' => 'slch_011CZkZmRt4vNq8sHbYw2KdX',
      ],
  );

  echo "{$target->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  target = client.beta.organization.claude_tag.bundles.targets.create(
    bundle_id,
    target: {
      type: :slack_channel,
      slack_channel_id: "slch_011CZkZmRt4vNq8sHbYw2KdX"
    }
  )

  puts target.id
  ```
</CodeGroup>

```json Response
{
  "type": "slack_channel",
  "id": "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
  "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX",
  "created_at": "2026-10-19T16:21:44Z"
}
```

Lampirkan Bundle ke sebuah workspace:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq/targets" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21" \
    -d '{
      "type": "slack_workspace",
      "slack_workspace_id": "slws_011CZkZnWa7xPc3uJfZe5LgT"
    }'
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles:targets create \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq \
    --target '{type: slack_workspace, slack_workspace_id: slws_011CZkZnWa7xPc3uJfZe5LgT}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  target = client.beta.organization.claude_tag.bundles.targets.create(
      "capp_011CZkZjLP1cWxj5EtMmdgbq",
      target={
          "type": "slack_workspace",
          "slack_workspace_id": "slws_011CZkZnWa7xPc3uJfZe5LgT",
      },
  )

  print(target.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const target = await client.beta.organization.claudeTag.bundles.targets.create(
    "capp_011CZkZjLP1cWxj5EtMmdgbq",
    { target: { type: "slack_workspace", slack_workspace_id: "slws_011CZkZnWa7xPc3uJfZe5LgT" } }
  );

  console.log(target.id);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ClaudeTag.Bundles.Targets;

  AnthropicClient client = new();

  var target = await client.Beta.Organization.ClaudeTag.Bundles.Targets.Create(
      "capp_011CZkZjLP1cWxj5EtMmdgbq",
      new()
      {
          Target = new BetaClaudeTagSlackWorkspaceBundleTargetCreate
          {
              SlackWorkspaceID = "slws_011CZkZnWa7xPc3uJfZe5LgT",
          },
      }
  );

  Console.WriteLine(target.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  target, err := client.Beta.Organization.ClaudeTag.Bundles.Targets.New(
  	context.Background(),
  	"capp_011CZkZjLP1cWxj5EtMmdgbq",
  	anthropic.BetaOrganizationClaudeTagBundleTargetNewParams{
  		Target: anthropic.BetaClaudeTagBundleTargetCreateUnionParam{
  			OfSlackWorkspace: &anthropic.BetaClaudeTagSlackWorkspaceBundleTargetCreateParam{
  				SlackWorkspaceID: "slws_011CZkZnWa7xPc3uJfZe5LgT",
  			},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(target.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.bundles.targets.TargetCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = TargetCreateParams.builder()
          .slackWorkspaceTarget("slws_011CZkZnWa7xPc3uJfZe5LgT")
          .build();
      var target = client.beta().organization().claudeTag().bundles().targets()
          .create("capp_011CZkZjLP1cWxj5EtMmdgbq", params);

      IO.println(target.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $target = $client->beta->organization->claudeTag->bundles->targets->create(
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
      target: [
          'type' => 'slack_workspace',
          'slackWorkspaceID' => 'slws_011CZkZnWa7xPc3uJfZe5LgT',
      ],
  );

  echo "{$target->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  target = client.beta.organization.claude_tag.bundles.targets.create(
    bundle_id,
    target: {
      type: :slack_workspace,
      slack_workspace_id: "slws_011CZkZnWa7xPc3uJfZe5LgT"
    }
  )

  puts target.id
  ```
</CodeGroup>

Lampiran ke sebuah channel memiliki kondisi yang menentukan kapan lampiran itu berlaku, seperti hanya selama tidak ada tamu Slack di channel tersebut. Kondisi diatur di claude.ai dan tidak dikembalikan di sini. Melampirkan melalui API ini menggunakan kondisi default, dan melampirkan pasangan yang sudah dilampirkan tidak mengubah kondisinya.

### Mendapatkan target Bundle

`GET /v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}` mengembalikan target Bundle. `target_id` yang bukan pengidentifikasi `btgt_` yang valid mengembalikan `400`. `target_id` valid yang dimiliki Bundle lain, sudah dilepaskan, atau menyebutkan channel atau workspace yang tidak lagi disiapkan mengembalikan `404`. Memerlukan cakupan `read:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq/targets/btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles:targets retrieve \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq \
    --target-id btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH
  ```

  ```python Python
  client = anthropic.Anthropic()

  target = client.beta.organization.claude_tag.bundles.targets.retrieve(
      "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
      bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
  )

  print(target.type)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const target = await client.beta.organization.claudeTag.bundles.targets.retrieve(
    "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
    { bundle_id: "capp_011CZkZjLP1cWxj5EtMmdgbq" }
  );

  console.log(target.type);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var target = await client.Beta.Organization.ClaudeTag.Bundles.Targets.Retrieve(
      "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
      new() { BundleID = "capp_011CZkZjLP1cWxj5EtMmdgbq" }
  );

  Console.WriteLine(target.Type.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  target, err := client.Beta.Organization.ClaudeTag.Bundles.Targets.Get(
  	context.Background(),
  	"btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
  	anthropic.BetaOrganizationClaudeTagBundleTargetGetParams{
  		BundleID: "capp_011CZkZjLP1cWxj5EtMmdgbq",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(target.Type)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.bundles.targets.TargetRetrieveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = TargetRetrieveParams.builder()
          .bundleId("capp_011CZkZjLP1cWxj5EtMmdgbq")
          .build();
      var target = client.beta().organization().claudeTag().bundles().targets()
          .retrieve("btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH", params);

      IO.println(target.type().asString());
  }
  ```

  ```php PHP
  $client = new Client();

  $target = $client->beta->organization->claudeTag->bundles->targets->retrieve(
      targetID: 'btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH',
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
  );

  echo "{$target->type}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  target_id = "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH"
  target = client.beta.organization.claude_tag.bundles.targets.retrieve(
    target_id,
    bundle_id: bundle_id
  )

  puts target.type
  ```
</CodeGroup>

### Melepaskan Bundle

`DELETE /v1/organizations/claude_tag/bundles/{bundle_id}/targets/{target_id}` melepaskan Bundle. Pelepasan berulang mengembalikan `404`, jadi setelah `503`, pelepasan yang dikirim ulang dan mengembalikan `404` berarti target Bundle sudah tidak ada. Memerlukan cakupan `write:claude_tag`.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/claude_tag/bundles/capp_011CZkZjLP1cWxj5EtMmdgbq/targets/btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: experimental-claude-tag-2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:claude-tag:bundles:targets delete \
    --bundle-id capp_011CZkZjLP1cWxj5EtMmdgbq \
    --target-id btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_target = client.beta.organization.claude_tag.bundles.targets.delete(
      "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
      bundle_id="capp_011CZkZjLP1cWxj5EtMmdgbq",
  )

  print(deleted_target.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedTarget = await client.beta.organization.claudeTag.bundles.targets.delete(
    "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
    { bundle_id: "capp_011CZkZjLP1cWxj5EtMmdgbq" }
  );

  console.log(deletedTarget.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedTarget = await client.Beta.Organization.ClaudeTag.Bundles.Targets.Delete(
      "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
      new() { BundleID = "capp_011CZkZjLP1cWxj5EtMmdgbq" }
  );

  Console.WriteLine(deletedTarget.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedTarget, err := client.Beta.Organization.ClaudeTag.Bundles.Targets.Delete(
  	context.Background(),
  	"btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH",
  	anthropic.BetaOrganizationClaudeTagBundleTargetDeleteParams{
  		BundleID: "capp_011CZkZjLP1cWxj5EtMmdgbq",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(deletedTarget.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.claudetag.bundles.targets.TargetDeleteParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = TargetDeleteParams.builder()
          .bundleId("capp_011CZkZjLP1cWxj5EtMmdgbq")
          .build();
      var deletedTarget = client.beta().organization().claudeTag().bundles().targets()
          .delete("btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH", params);

      IO.println(deletedTarget.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $deletedTarget = $client->beta->organization->claudeTag->bundles->targets->delete(
      targetID: 'btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH',
      bundleID: 'capp_011CZkZjLP1cWxj5EtMmdgbq',
  );

  echo "{$deletedTarget->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  bundle_id = "capp_011CZkZjLP1cWxj5EtMmdgbq"
  target_id = "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH"
  deleted_target = client.beta.organization.claude_tag.bundles.targets.delete(
    target_id,
    bundle_id: bundle_id
  )

  puts deleted_target.id
  ```
</CodeGroup>

```json Response
{
  "type": "bundle_target_deleted",
  "id": "btgt_011CZkZpBv9yQd6wKhAr8MnU1CZkZwPd5fSj8tMxUr3ZcH"
}
```

## Nilai yang tidak dikenali

`guest_policy.type`, `type` dari sebuah sumber, `type` dari sebuah target Bundle, dan kode error dapat memperoleh nilai baru kapan saja. Perlakukan nilai yang tidak Anda kenali seperti string tak dikenal lainnya alih-alih menggagalkan proses.

## Pembatasan laju

Permintaan dibatasi untuk setiap organisasi, dalam dua anggaran yang digunakan bersama oleh semua kunci organisasi Anda dan terpisah dari batas Admin API lainnya milik organisasi Anda. Setiap anggaran mengizinkan lonjakan (burst) lalu terisi kembali dengan laju tetap:

| Anggaran  | Permintaan                 | Lonjakan | Pengisian ulang |
| --------- | -------------------------- | -------- | --------------- |
| Pembacaan | Setiap `GET`               | 120      | 2 per detik     |
| Perubahan | Setiap `POST` dan `DELETE` | 60       | 1 per detik     |

Permintaan yang melebihi anggaran mengembalikan **429 Too Many Requests** dengan header `retry-after`: tunggu selama jumlah detik tersebut, lalu kirim ulang permintaan. Permintaan yang sampai ke tahap anggarannya, apa pun hasilnya, mendapatkan header `anthropic-ratelimit-requests-limit`, `anthropic-ratelimit-requests-remaining`, dan `anthropic-ratelimit-requests-reset` untuk anggaran tersebut; permintaan yang ditolak sebelum tahap itu, misalnya karena kunci, cakupan, atau header-nya, atau karena API, perubahan, atau penyimpanan baru tidak diaktifkan untuk organisasi Anda, tidak mendapatkan header tersebut.

## Paginasi

Endpoint daftar menggunakan **kursor opak**. Permintaan pertama mengembalikan hingga `limit` baris ditambah kursor `next_page`; teruskan kursor tanpa diubah sebagai parameter `page` pada permintaan berikutnya, dengan parameter query lainnya tidak diubah, dan ulangi hingga `next_page` bernilai `null`. Kursor yang dikirim dengan nilai `include_inherited` yang berbeda dari permintaan yang mengembalikannya mengembalikan `400`. Perlakukan string kursor sebagai opak: jangan mengurai, memodifikasi, atau menyusunnya sendiri. [Mencantumkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-channels) dapat mengembalikan halaman dengan channel lebih sedikit dari `limit`, atau tidak sama sekali, sementara `next_page` masih ditetapkan, jadi terus minta halaman hingga `next_page` bernilai `null`. Iterator daftar pada SDK Python, TypeScript, C#, Go, Java, dan Ruby serta CLI (kecuali dengan `--format raw`) melakukannya untuk Anda. Di PHP dan curl, minta setiap halaman sendiri dan teruskan `next_page`-nya sebagai `page`.

`limit` default-nya 20, dengan minimum 1 dan maksimum 100; nilai di luar rentang tersebut mengembalikan `400` pada setiap daftar. Setiap daftar diurutkan dari yang terbaru berdasarkan `created_at`, dan tidak menerima urutan lain.

## Respons error

Respons kesalahan mengikuti bentuk standar yang didokumentasikan di [Kesalahan Claude API](https://platform.claude.com/docs/id/api/errors). Sebutkan `request_id` dari body respons saat menghubungi dukungan.

| Status | Arti                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 400    | Input tidak valid, atau operasi tidak berlaku untuk channel, workspace, atau Bundle ini (lihat bagian masing-masing endpoint).                                                                                                                                                                                                                                                                                                                                                                   |
| 401    | Header `x-api-key` tidak ada, atau kunci tidak dikenali.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 403    | Kunci bukan kunci dengan cakupan tingkat organisasi, tidak memiliki cakupan yang diperlukan, atau organisasi Anda tidak dapat membuat perubahan ini.                                                                                                                                                                                                                                                                                                                                             |
| 404    | Resource tidak ditemukan, atau bukan milik organisasi Anda. Juga dikembalikan ketika permintaan menghilangkan nilai `anthropic-beta`, atau API tidak diaktifkan untuk organisasi Anda, sehingga endpoint terbaca sebagai tidak ada.                                                                                                                                                                                                                                                              |
| 409    | Sesuatu yang lain mengubah atau menghapus resource saat permintaan berjalan. Tidak ada yang diminta oleh permintaan yang dilakukan: tidak ada pengaturan yang disimpan, tidak ada yang dilampirkan, dilepaskan, atau dihapus. Satu-satunya pengecualian adalah permintaan penyiapan, yang mungkin telah menyiapkan channel sebelum `settings`-nya mengalami konflik (`slack_channel_set_up_settings_conflict`). Baca kembali resource tersebut dan kirim ulang permintaan jika masih diperlukan. |
| 429    | “Rate limit” (batas laju) terlampaui. Lihat [Pembatasan laju](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#rate-limiting).                                                                                                                                                                                                                                                                                                                                                   |
| 500    | Kesalahan internal.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 503    | Sementara. Pada sebuah perubahan, status ini tidak mengatakan apakah perubahan sudah disimpan. Setiap perubahan aman untuk diulang, jadi kirim ulang permintaan tanpa diubah. Jika `DELETE` yang dikirim ulang kemudian mengembalikan `404`, channel atau target Bundle sudah tidak ada.                                                                                                                                                                                                         |

Ketika satu status memiliki beberapa penyebab yang akan Anda tangani secara berbeda, error juga membawa `error.details.error_code`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "...",
    "details": {
      "error_code": "slack_channel_set_up_settings_refused",
      "slack_channel_id": "slch_011CZkZmRt4vNq8sHbYw2KdX"
    }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

| `error_code`                                 | Status | Arti dan apa yang harus dilakukan                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `organization_level_scoped_api_key_required` | 403    | Kredensial bukan kunci Admin API dengan cakupan yang dimiliki organisasi secara keseluruhan. Mintalah satu kepada pemilik utama Anda.                                                                                                                                                                                                                                                                                                                                         |
| `api_key_scope_missing`                      | 403    | Kunci tidak memiliki `read:claude_tag` atau `write:claude_tag`, mana pun yang diperlukan endpoint.                                                                                                                                                                                                                                                                                                                                                                            |
| `claude_tag_writes_not_enabled`              | 403    | Organisasi Anda dapat membaca melalui API ini tetapi tidak diaktifkan untuk melakukan perubahan.                                                                                                                                                                                                                                                                                                                                                                              |
| `compliance_configuration_restricted`        | 403    | Organisasi Anda memiliki konfigurasi kepatuhan di mana Claude Tag tidak menyimpan hal baru apa pun, seperti zero data retention. Menyiapkan channel, memperbarui pengaturan (bahkan untuk menghapusnya), dan melampirkan Bundle ditolak. Melepaskan Bundle dan menghapus channel tidak ditolak, dan organisasi seperti itu dapat [menghapus](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#remove-a-channel) channel bahkan saat Claude aktif di dalamnya. |
| `environment_not_found`                      | 404    | `environment_id` tidak menyebutkan lingkungan yang dapat digunakan organisasi Anda di sini. `id` di path tidak bermasalah.                                                                                                                                                                                                                                                                                                                                                    |
| `environment_archived`                       | 400    | `environment_id` menyebutkan lingkungan yang diarsipkan.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `slack_channel_set_up_settings_refused`      | 400    | Permintaan menyiapkan channel, lalu `settings` ditolak. `details.slack_channel_id` adalah channel tersebut. Lihat [Menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel).                                                                                                                                                                                                                                                    |
| `slack_channel_set_up_environment_not_found` | 404    | Permintaan menyiapkan channel, lalu `environment_id` tidak ditemukan. `details.slack_channel_id` adalah channel tersebut. Lihat [Menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel).                                                                                                                                                                                                                                      |
| `slack_channel_set_up_settings_conflict`     | 409    | Permintaan menyiapkan channel, lalu perubahan lain tumpang tindih dengan `settings`. Tidak ada bagian dari `settings` yang disimpan. `details.slack_channel_id` adalah channel tersebut. Lihat [Menyiapkan channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#set-up-a-channel).                                                                                                                                                                       |
| `slack_channel_enabled`                      | 400    | Claude aktif di channel (`enabled` terselesaikan menjadi `true`), sehingga channel tidak dapat dihapus. Tetapkan `enabled` ke `false` terlebih dahulu. Lihat [Menghapus channel](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#remove-a-channel).                                                                                                                                                                                                          |

Kode baru dapat ditambahkan. Perlakukan kode yang tidak Anda kenali seperti Anda memperlakukan statusnya. `404` tanpa `error_code` memiliki salah satu dari dua penyebab. Entah sesuatu yang disebutkan permintaan tidak ditemukan (`id` di path, atau channel atau workspace Slack di body atau query), atau setiap endpoint terbaca sebagai tidak ada karena permintaan menghilangkan nilai `anthropic-beta` atau API tidak diaktifkan untuk organisasi Anda. Untuk membedakannya, [cantumkan workspace Anda](https://platform.claude.com/docs/id/manage-claude/claude-tag-api#list-workspaces) dengan kunci dan header yang sama: permintaan tersebut tidak menyebutkan apa pun, sehingga hanya mengembalikan `404` pada kasus kedua.

## Event Activity Feed

Setiap perubahan melalui API ini dicatat di [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda, diatribusikan ke kunci API sebagai `api_actor` yang membawa ID `apikey_`-nya. Event tersebut sama dengan yang dicatat oleh feed ketika perubahan yang sama dilakukan di claude.ai, sehingga satu kueri dapat menemukan suatu perubahan dengan cara apa pun perubahan itu dilakukan.

| Event                             | Dipancarkan ketika                                                                           |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| `ccr_agent_created`               | Sebuah channel disiapkan.                                                                    |
| `ccr_agent_updated`               | Sebuah pengaturan berubah pada channel atau workspace.                                       |
| `ccr_agent_deleted`               | Sebuah channel dihapus. Target Bundle-nya ikut terhapus dan tidak memancarkan event sendiri. |
| `ccr_agent_proxy_profile_bound`   | Sebuah Bundle dilampirkan.                                                                   |
| `ccr_agent_proxy_profile_unbound` | Sebuah Bundle dilepaskan.                                                                    |

Event menyebutkan channel atau workspace dengan pengidentifikasi milik feed itu sendiri, `agent_id` (dengan prefiks `cagt_`), yang tidak ada di respons mana pun dari API ini, sehingga Anda belum dapat mencocokkan event dengan `id` channel atau workspace. Kedua event Bundle menyebutkan Bundle di `profile_id` dan channel atau workspace, dengan `agent_id` yang sama, di `scope_id`.

Event `ccr_agent_updated` mencantumkan apa yang berubah di `updated_fields`, menggunakan nama-nama milik feed itu sendiri:

| Pengaturan       | Nama di `updated_fields` |
| ---------------- | ------------------------ |
| `enabled`        | `slackbot_version`       |
| `instructions`   | `system_prompt_addendum` |
| `model`          | `default_model`          |
| `environment_id` | `default_environment_id` |
| `guest_policy`   | `guest_policy`           |

`updated_fields` juga dapat berisi `is_virtual`, yang tidak menyebutkan pengaturan apa pun. Nilai ini muncul di samping nama pengaturan yang berubah dalam event untuk perubahan melalui API ini yang merupakan hal pertama yang disimpan siapa pun pada channel atau workspace: channel yang disiapkan oleh penggunaan pertama Claude, atau yang disiapkan API ini tanpa `settings`, atau workspace di mana Claude belum pernah digunakan, dan yang belum pernah ada yang menyimpan pengaturan atau melampirkan Bundle padanya, di sini atau di claude.ai. `model` yang digunakan code channel saat dimulai tidak dihitung sebagai tersimpan. Melampirkan Bundle hanya mencatat `ccr_agent_proxy_profile_bound`.

Pembacaan, permintaan yang tidak mengubah apa pun, dan permintaan yang ditolak sebelum apa pun disimpan tidak mencatat apa pun. Permintaan penyiapan yang menyiapkan sebuah channel dan yang `settings`-nya kemudian ditolak akan mencatat `ccr_agent_created`.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Membuat kunci Admin API" href="https://platform.claude.com/docs/id/manage-claude/admin-api-keys">
    Tempat pemilik utama Anda membuat kunci dengan scope tertentu.
  </Card>

  <Card title="Dokumentasi Claude Tag" href="https://claude.com/docs/claude-tag/overview">
    Apa itu Claude Tag, cara menyiapkannya, dan apa fungsi setiap pengaturan di Slack.
  </Card>

  <Card title="Compliance API Activity Feed" href="https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed">
    Jejak audit dari setiap perubahan yang dilakukan di sini dan di claude.ai.
  </Card>

  <Card title="Plugins API" href="https://platform.claude.com/docs/id/manage-claude/plugins-api">
    Kelola plugin di organisasi Claude Enterprise Anda.
  </Card>
</CardGroup>
