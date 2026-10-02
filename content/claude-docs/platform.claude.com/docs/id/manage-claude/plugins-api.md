---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/plugins-api
fetched_at: 2026-10-02T02:24:19.323378Z
sha256: 863e07aa7c17d719884fedcd4d242f72007c2d9c33e3d1fcdf67f4be7cba0f8c
---

---
title: API Plugin
url: https://platform.claude.com/docs/id/manage-claude/plugins-api
description: "Inventarisasi dan kelola plugin di organisasi Claude Enterprise Anda: unggah plugin dan versi, pilih versi yang disajikan kepada anggota, kendalikan siapa yang dapat menggunakan setiap plugin, unduh file plugin untuk ditinjau, dan validasi marketplace sebelum Anda menghubungkannya."
---

Plugins API memungkinkan Anda menginventarisasi setiap plugin di organisasi Claude Enterprise Anda, memublikasikan plugin dan versi baru dari pipeline Anda sendiri, memilih versi mana yang disajikan kepada anggota, mengendalikan siapa yang dapat menggunakan setiap plugin, mengunduh file plugin untuk ditinjau, dan memeriksa marketplace Git sebelum Anda menghubungkannya.

Untuk pelaporan *penggunaan* plugin (plugin dan skill mana yang digunakan anggota, dan seberapa sering), lihat [Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api).

<Check>
  **Diperlukan kunci Admin API dengan cakupan tertentu**

  Endpoint ini memerlukan kunci Admin API dengan "scope" (cakupan) `read:plugins` (untuk endpoint `GET`, termasuk unduhan arsip) atau cakupan `write:plugins` (untuk endpoint `POST` dan `DELETE`, kecuali validasi marketplace, yang diizinkan oleh salah satu dari kedua cakupan tersebut); [Cakupan](https://platform.claude.com/docs/id/manage-claude/plugins-api#scopes) berisi detailnya, termasuk dua cakupan baca lain yang juga berfungsi. Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana pemilik utama Anda membuatnya. Teruskan kunci di header `x-api-key` pada setiap permintaan, bersama dengan header [`anthropic-version`](https://platform.claude.com/docs/id/api/versioning) dan header beta yang ditunjukkan dalam catatan berikut.
</Check>

<Note>
  Plugins API berstatus **beta** dan hanya tersedia untuk organisasi Claude Enterprise. API ini tidak tersedia untuk organisasi Claude Platform (Claude Console), atau untuk organisasi yang mengaktifkan kesiapan HIPAA.

  Setiap permintaan harus menyertakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `anthropic-beta: ce-plugins-2026-09-01` (SDK dan CLI `ant` mengirimkannya untuk Anda). Permintaan tanpa header tersebut mengembalikan `404`, persis seolah-olah endpoint tersebut tidak ada.
</Note>

## Endpoint

API ini menyediakan 18 endpoint di lima sumber daya:

| Sumber daya                                                                                                                                                                                       | Endpoint                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Plugin**: mencantumkan setiap plugin di organisasi, mengunggah plugin baru, mencari satu plugin, memilih versi yang disajikan kepada anggota (rollback atau promosi), menghapus satu plugin     | `GET /v1/organizations/plugins` `POST /v1/organizations/plugins` `GET /v1/organizations/plugins/{plugin_id}` `POST /v1/organizations/plugins/{plugin_id}` `DELETE /v1/organizations/plugins/{plugin_id}`                                                                                              |
| **Versi plugin**: mencantumkan riwayat versi plugin, mengunggah versi baru, mencari satu versi, mengunduh file suatu versi                                                                        | `GET /v1/organizations/plugins/{plugin_id}/versions` `POST /v1/organizations/plugins/{plugin_id}/versions` `GET /v1/organizations/plugins/{plugin_id}/versions/{version}` `GET /v1/organizations/plugins/{plugin_id}/versions/{version}/content`                                                      |
| **Pengaturan instalasi**: membaca siapa yang dapat menggunakan plugin milik organisasi, menetapkannya untuk seluruh organisasi atau untuk satu grup, menghapus pengaturan satu grup               | `GET /v1/organizations/plugins/{plugin_id}/installation_settings` `POST /v1/organizations/plugins/{plugin_id}/installation_settings/{target}` `DELETE /v1/organizations/plugins/{plugin_id}/installation_settings/{target}`                                                                           |
| **Berbagi**: membaca dengan siapa seorang anggota telah membagikan plugin miliknya sendiri (hanya-baca)                                                                                           | `GET /v1/organizations/plugins/{plugin_id}/shares`                                                                                                                                                                                                                                                    |
| **Marketplace plugin**: menemukan ID marketplace, mencari satu marketplace, menetapkan pengaturan instalasi default untuk plugin-pluginnya, memeriksa konten marketplace sebelum menghubungkannya | `GET /v1/organizations/plugin_marketplaces` `GET /v1/organizations/plugin_marketplaces/{marketplace_id}` `POST /v1/organizations/plugin_marketplaces/{marketplace_id}` `POST /v1/organizations/plugin_marketplaces/validate_repository` `POST /v1/organizations/plugin_marketplaces/validate_archive` |

Rilis ini tidak mencakup skill mandiri (skill yang ditulis anggota di editor skill atau diunggah sebagai satu skill di claude.ai). Skill tersebut tidak muncul dalam inventaris dan tidak dapat dibuat di sini. Plugin yang dipublikasikan Anthropic juga tidak diinventarisasi; penggunaannya dilaporkan oleh [Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api). Marketplace dibuat, dihubungkan ke repositori, dan dihapus di claude.ai, bukan melalui API ini.

## Prasyarat

* Organisasi Anda harus menggunakan paket Claude Enterprise.
* Pemilik utama Anda membuat kunci Admin API dengan cakupan `read:plugins`, cakupan `write:plugins`, atau keduanya di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization).
* Setiap permintaan membawa tiga header: `x-api-key`, `anthropic-version: 2023-06-01`, dan `anthropic-beta: ce-plugins-2026-09-01`.

SDK Python, TypeScript, C#, Go, Java, PHP, dan Ruby menyediakan endpoint ini di bawah `client.beta.organization` (csharp, go: `client.Beta.Organization`; java: `client.beta().organization()`; php: `$client->beta->organization`), dan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) di bawah `ant beta:organization`; keduanya mengirimkan header `anthropic-version` dan `anthropic-beta` untuk Anda. Contoh di halaman ini menggunakan klien default setiap SDK, yang, seperti CLI, membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`; contoh curl membaca kunci dari variabel yang sama dan meneruskannya di header `x-api-key`. Dalam contoh daftar Python, TypeScript, C#, Go, Java, dan Ruby serta di CLI, SDK mengambil halaman berikutnya saat Anda melakukan iterasi, sehingga `limit` menetapkan ukuran halaman, bukan total; contoh PHP dan curl mengembalikan satu halaman (lihat [Paginasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#pagination)).

Kunci API adalah milik organisasi dan tetap berfungsi setelah orang yang membuatnya keluar. Jangan bagikan kunci tersebut atau memasukkannya ke kontrol sumber.

## Mulai cepat

Cantumkan plugin di marketplace milik organisasi Anda sendiri, dimulai dari yang terbaru:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins?owner_type=organization&limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins list --owner-type organization --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  plugins = client.beta.organization.plugins.list(owner_type="organization", limit=20)

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for plugin in plugins:
      print(f"{plugin.id}: {plugin.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const plugins = await client.beta.organization.plugins.list({
    owner_type: "organization",
    limit: 20
  });

  for await (const plugin of plugins) {
    console.log(`${plugin.id}: ${plugin.name}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Plugins;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Plugins.List(
      new() { OwnerType = OwnerType.Organization, Limit = 20 }
  );

  await foreach (var plugin in page.Paginate())
  {
      Console.WriteLine($"{plugin.ID}: {plugin.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  plugins := client.Beta.Organization.Plugins.ListAutoPaging(context.Background(), anthropic.BetaOrganizationPluginListParams{
  	OwnerType: anthropic.BetaOrganizationPluginListParamsOwnerTypeOrganization,
  	Limit:     anthropic.Int(20),
  })

  for plugins.Next() {
  	plugin := plugins.Current()
  	fmt.Printf("%s: %s\n", plugin.ID, plugin.Name)
  }
  if err := plugins.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.PluginListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginListParams.builder()
          .ownerType(PluginListParams.OwnerType.ORGANIZATION)
          .limit(20)
          .build();
      var plugins = client.beta().organization().plugins().list(params);

      for (var plugin : plugins.autoPager()) {
          IO.println(plugin.id() + ": " + plugin.name());
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Plugins\PluginListParams\OwnerType;
  // ...

  $client = new Client();

  $plugins = $client->beta->organization->plugins->list(
      limit: 20,
      ownerType: OwnerType::ORGANIZATION,
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $plugins->nextPage.
  foreach ($plugins->getItems() as $plugin) {
      echo "{$plugin->id}: {$plugin->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.plugins.list(owner_type: :organization, limit: 20)

  page.auto_paging_each do |plugin|
    puts "#{plugin.id}: #{plugin.name}"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "plugin",
      "id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      "name": "sales-toolkit",
      "display_name": "Sales Toolkit",
      "description": "Account research and call prep for the sales team.",
      "served_version_id": "pluginver_01Km7tL4pR9xF5sU2zV3jP6q",
      "served_version_pinned": true,
      "latest_version_id": "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
      "manifest_version": "1.4.0",
      "owner": { "type": "organization" },
      "marketplace_id": "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
      "created_by": { "type": "api_actor", "api_key_id": "apikey_01Nq9vN6rT2zH7uW4bX5mR8s" },
      "organization_installation_preference": "available",
      "organization_installation_preference_inherited": true,
      "content_scan": { "status": "completed", "assessment": "pass", "reason": null },
      "components": [
        {
          "type": "skill",
          "name": "account-research",
          "description": "Researches a customer account before a call."
        },
        { "type": "mcp_server", "name": "crm", "description": null }
      ],
      "reach": "remote",
      "created_at": "2026-09-01T17:04:11Z",
      "updated_at": "2026-09-15T14:12:30Z"
    }
  ],
  "next_page": "page_xK9f2LqT7vNw3pRzBd8sHy"
}
```

Dalam contoh ini plugin disematkan ke versi sebelumnya: versi yang lebih baru (`latest_version_id`) sudah disimpan tetapi belum disajikan.

## Cakupan

| Cakupan                    | Memberikan                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read:plugins`             | Setiap endpoint `GET` di halaman ini, termasuk unduhan arsip, ditambah validasi marketplace.                                                                                                                                                                                                                                                                                                          |
| `write:plugins`            | Setiap endpoint `POST` dan `DELETE` di halaman ini: membuat plugin, membuat versi, mengubah versi yang disajikan, menghapus plugin, menetapkan dan menghapus pengaturan instalasi, dan menetapkan default marketplace, ditambah validasi marketplace. Cakupan ini tidak memberikan akses baca.                                                                                                        |
| `read:org_audit`           | Cakupan hanya-baca untuk integrasi audit keamanan: setiap endpoint `GET` di halaman ini, termasuk unduhan arsip, ditambah endpoint baca [manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management) dan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Cakupan ini tidak memberikan validasi marketplace atau operasi tulis apa pun. |
| `read:compliance_org_data` | Cakupan Compliance API untuk metadata organisasi (nama, jenis, peran, dan grup) dan pengaturan efektif. Memberikan setiap endpoint `GET` di halaman ini, persis seperti `read:org_audit`, sehingga Compliance Access Key dapat membaca plugin tanpa kunci kedua. Cakupan ini tidak memberikan validasi marketplace atau operasi tulis apa pun.                                                        |

Sebuah kunci dapat membawa beberapa cakupan. Integrasi yang mengunggah plugin lalu membacanya kembali memerlukan `read:plugins` dan `write:plugins`. Di mana pun halaman ini menyatakan bahwa suatu endpoint memerlukan cakupan `read:plugins`, kunci dengan `read:org_audit` atau `read:compliance_org_data` juga berfungsi.

### Akses ke file plugin anggota

Masing-masing cakupan baca ini (`read:plugins`, `read:org_audit`, dan `read:compliance_org_data`) dapat mengunduh file plugin di marketplace pribadi anggota, termasuk file yang tidak ditampilkan oleh pengaturan admin claude.ai, dan kunci `read:org_audit` atau `read:compliance_org_data` yang terikat ke organisasi induk Anda dapat melakukan hal ini di organisasi mana pun di bawahnya yang memiliki akses ke API ini, dengan meneruskan `organization_id` (lihat [Membaca organisasi lain di bawah induk yang sama](https://platform.claude.com/docs/id/manage-claude/plugins-api#reading-another-organization-under-the-same-parent)). Setiap unduhan tersebut mencatat peristiwa `claude_plugin_archive_accessed` di [Activity Feed Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), yang mengidentifikasi kunci, plugin, versi, dan anggota (lihat [Peristiwa Activity Feed](https://platform.claude.com/docs/id/manage-claude/plugins-api#activity-feed-events)). Unduhan plugin milik organisasi tidak dicatat.

### Membaca organisasi lain di bawah induk yang sama

Kunci `read:plugins` dan `write:plugins` hanya membaca dan menulis organisasi tempat kunci tersebut dibuat. Jika perusahaan Anda memiliki beberapa organisasi Claude yang ditautkan di bawah satu organisasi induk, kunci `read:org_audit` atau `read:compliance_org_data` yang dibuat oleh pemilik utama organisasi induk untuk semua organisasi tertaut (lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization)) juga dapat membaca organisasi mana pun di antaranya yang memiliki akses ke API ini: teruskan ID organisasi tersebut di parameter kueri `organization_id` pada endpoint `GET` mana pun di halaman ini. ID tersebut adalah UUID organisasi yang ditampilkan di pengaturan claude.ai (bentuk berawalan `org_`-nya juga diterima). Tanpa parameter tersebut, kunci membaca organisasi tempat kunci itu dibuat. `404` berarti organisasi yang disebutkan tidak berada di bawah induk kunci tersebut atau API tidak tersedia untuknya; nilai yang bukan UUID atau ID `org_` mengembalikan `400`. Kunci lain mana pun yang menyebutkan organisasi selain organisasinya sendiri mendapatkan `404`. Operasi tulis tidak menerima `organization_id`.

## Konsep utama

### Plugin dan komponen

**Plugin** adalah paket yang memperluas Claude untuk anggota organisasi Anda. Plugin berisi kombinasi apa pun dari komponen berikut:

| Komponen   | Apa itu                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------- |
| Skill      | Instruksi dan file yang dimuat Claude ketika suatu tugas memerlukannya.                                             |
| Command    | Prompt tersimpan yang dijalankan anggota dengan mengetik `/` diikuti nama command tersebut.                         |
| Agent      | Asisten pembantu dengan instruksinya sendiri, yang dapat menerima sebagian tugas dari Claude.                       |
| Hook       | Perintah yang berjalan otomatis ketika suatu peristiwa terjadi dalam sesi, seperti sebelum Claude menggunakan alat. |
| Server MCP | Koneksi dari Claude ke alat dan data di sistem lain (Model Context Protocol).                                       |
| CLI        | Program baris perintah yang diizinkan plugin untuk dijalankan oleh Claude.                                          |

Setiap plugin memiliki manifest di `.claude-plugin/plugin.json`. `name` pada manifest menjadi `name` plugin: pengenal huruf kecil yang unik di dalam marketplace-nya.

### Marketplace

**Marketplace** adalah wadah plugin. Setiap marketplace memiliki pemilik dan sumber.

* **Pemilik.** Organisasi memiliki marketplace-nya sendiri. Setiap anggota juga dapat memiliki marketplace pribadi.
* **Sumber.** `manual` berarti plugin diunggah, di claude.ai atau, untuk marketplace organisasi, melalui API ini. `github`, `gitlab`, dan `public_git` berarti plugin disinkronkan dari repositori Git yang dihubungkan oleh pemilik. Tidak ada yang dapat diunggah ke marketplace yang disinkronkan, dan API ini tidak dapat menghapus pluginnya, karena sinkronisasi berikutnya akan membatalkan perubahan mana pun. Sebagai gantinya, ubah repositorinya.

"Library marketplace" (marketplace pustaka) organisasi Anda adalah marketplace `manual` milik organisasi yang menjadi tujuan unggahan ketika Anda tidak menyebutkan marketplace. Marketplace ini dibuat saat pertama kali sesuatu diunggah ke sana.

### Plugin milik organisasi dan milik anggota

`owner.type` pada plugin menyatakan di marketplace milik siapa plugin tersebut berada:

* `organization`: Anda dapat mengelolanya melalui API ini, kecuali bahwa plugin di marketplace yang disinkronkan dari Git tidak dapat menerima unggahan atau dihapus di sini.
* `user`: plugin berada di marketplace pribadi seorang anggota. Anda dapat membaca detailnya dan mengunduh filenya, serta menghapusnya jika marketplace-nya `manual`. Mengunggah versi dan memilih versi yang disajikan mengembalikan `403`. Berbagi hanya dikelola oleh anggota tersebut, di claude.ai.

Menghapus anggota dari organisasi tidak menghapus plugin mereka. Plugin tersebut tetap ada di inventaris di bawah `user_id` anggota, dan filter `owner_user_id` masih menemukannya, sehingga Anda dapat meninjau dan menghapus konten anggota yang telah keluar. Plugin tersebut dihapus ketika akun anggota dihapus.

### Versi dan versi yang disajikan

Setiap unggahan membuat **versi** baru yang tidak dapat diubah, baik berasal dari API ini, dari claude.ai, maupun dari sinkronisasi Git. Plugin memiliki dua penunjuk ke versinya:

* `latest_version_id`: versi terbaru.
* `served_version_id`: "served version" (versi yang disajikan), yaitu versi yang disajikan kepada anggota.

Secara default `served_version_pinned` bernilai `false`: versi yang disajikan mengikuti versi terbaru, dan setiap versi baru disajikan segera setelah disimpan.

Memilih versi dengan `POST /v1/organizations/plugins/{plugin_id}` akan **menyematkan** ("pin") plugin (`served_version_pinned: true`). Begitu pula ketika administrator memilih versi di claude.ai, atau menerima permintaan anggota untuk memublikasikan ke plugin tersebut. Sejak saat itu, unggahan baru disimpan dan memajukan `latest_version_id`, tetapi anggota tetap mendapatkan versi yang disematkan hingga Anda mengarahkan `served_version_id` ke versi lain. Plugin yang kedua penunjuknya berbeda memiliki versi tersimpan yang tidak sedang disajikan.

Hal ini memungkinkan pipeline rilis mengunggah setiap build, mengujinya, lalu mempromosikannya. Agar pipeline Anda yang menentukan kapan setiap build disajikan, sematkan plugin sekali dengan menetapkan `served_version_id` ke versinya saat ini; sejak saat itu, promosikan setiap build yang ingin Anda sajikan. Dengan pemindaian konten aktif, penyematan pertama tersebut mengembalikan `409 scan_pending` hingga pemindaian versi saat ini selesai, dan `400 scan_failed` jika pemindaian selesai dengan `fail` atau `unknown`, atau mengalami error (`warn` diterima). Plugin yang telah disematkan saat ini tidak dapat dilepas sematannya, baik di sini maupun di claude.ai.

Untuk melakukan rollback, tetapkan `served_version_id` ke versi sebelumnya. Maju ke versi yang lebih baru dengan cara yang sama.

Aturan ini menjelaskan plugin milik organisasi. Versi yang disajikan dari plugin milik anggota dikendalikan oleh pemiliknya di claude.ai.

### Pengaturan instalasi

**Pengaturan instalasi** menentukan siapa yang dapat menggunakan plugin milik organisasi. Setiap pengaturan memiliki salah satu dari empat nilai, yang dibawa dalam field bernama `installation_preference` (dan, pada objek plugin dan marketplace, `organization_installation_preference` dan `default_installation_preference`):

| Nilai           | Yang dilihat anggota                      |
| --------------- | ----------------------------------------- |
| `required`      | Plugin terinstal dan tidak dapat dihapus. |
| `auto_install`  | Plugin terinstal dan dapat dihapus.       |
| `available`     | Plugin dapat diinstal sesuai permintaan.  |
| `not_available` | Plugin disembunyikan.                     |

Plugin dapat memiliki satu pengaturan tingkat organisasi dan satu pengaturan per grup (grup kontrol akses berbasis peran yang dikelola di [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management#groups)). Anggota mendapatkan nilai berdasarkan aturan berikut:

1. Nilai tingkat organisasi adalah pengaturan tingkat organisasi milik plugin itu sendiri jika ada, jika tidak maka default marketplace-nya, jika tidak maka `not_available`. Plugin melaporkan nilai ini di `organization_installation_preference`, dengan `organization_installation_preference_inherited: true` selama nilai tersebut berasal dari default marketplace.
2. Anggota yang tidak termasuk dalam grup mana pun yang memiliki pengaturan untuk plugin tersebut mendapatkan nilai tingkat organisasi.
3. Anggota yang termasuk dalam satu atau lebih grup yang memiliki pengaturan mendapatkan pengaturan paling permisif dari grup-grup tersebut sebagai gantinya, dengan urutan `required`, `auto_install`, `available`, `not_available`.

Pengaturan grup menggantikan nilai tingkat organisasi untuk anggotanya; pengaturan tersebut tidak menambahkannya. Misalnya, jika nilai tingkat organisasi adalah `required` dan grup Pilot memiliki `available`, anggota Pilot mendapatkan `available`. Saat Anda memindahkan plugin dari grup percontohan ke seluruh organisasi, tetapkan nilai tingkat organisasi lalu hapus pengaturan grup (menetapkan nilai tingkat organisasi secara permanen menghentikan plugin mewarisi default marketplace-nya, seperti yang dijelaskan di [Menetapkan pengaturan instalasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#set-an-installation-setting)).

Plugin yang dibuat melalui API ini dimulai tanpa pengaturannya sendiri, sehingga mewarisi default marketplace-nya: `not_available` kecuali seseorang telah menetapkan default. Menghapus grup akan menghapus pengaturannya dari setiap plugin.

### Berbagi

"Shares" (berbagi) menentukan siapa yang dapat menggunakan plugin milik anggota. Pemilik membagikannya di claude.ai dengan setiap anggota, dengan grup, atau dengan anggota tertentu. API ini mencantumkan berbagi tetapi tidak dapat mengubahnya.

Jika organisasi Anda telah menonaktifkan suatu jenis berbagi di pengaturan claude.ai-nya, berbagi jenis tersebut tetap muncul dalam daftar tetapi tidak memberikan akses kepada siapa pun selama pengaturan tersebut nonaktif; daftar itu sendiri tidak menunjukkan apakah pengaturan tersebut nonaktif.

### Pemindaian konten

"Content scanning" (pemindaian konten) adalah pengaturan organisasi di claude.ai. Saat aktif, versi yang baru disimpan akan dipindai (claude.ai mengecualikan beberapa) dan hasilnya dilaporkan di `content_scan`; versi yang tidak dipindai, misalnya versi yang disimpan sebelum pemindaian diaktifkan, memiliki `content_scan: null`. Pemindaian tidak ditawarkan kepada organisasi yang menggunakan kunci enkripsi yang dikelola pelanggan atau retensi data nol.

Selama pemindaian aktif, anggota hanya disajikan plugin ketika pemindaian versi yang disajikan berstatus `completed` dengan `pass` atau `warn`. Selama pemindaian berjalan, atau setelah pemindaian gagal, mengalami error, atau tidak mencapai putusan, plugin ditahan dari anggota, dan versi sebelumnya tidak disajikan sebagai gantinya. Versi yang tidak pernah dipindai (`content_scan: null`) disajikan secara normal.

Pada plugin yang tidak disematkan, setiap unggahan langsung menjadi versi yang disajikan. Anggota kehilangan plugin hingga pemindaian versi baru lolos, dan tetap tanpa plugin tersebut jika pemindaian gagal. Jika anggota harus tetap menggunakan versi saat ini selama versi baru dipindai, sematkan plugin terlebih dahulu (lihat [Versi dan versi yang disajikan](https://platform.claude.com/docs/id/manage-claude/plugins-api#versions-and-the-served-version)).

Setelah unggahan, `content_scan.status` bernilai `processing` dan putusan tiba secara asinkron. Baca versi tersebut untuk melihatnya; objek plugin hanya menampilkan pemindaian versi yang disajikan. Mengubah versi yang disajikan ke versi yang pemindaiannya masih berjalan mengembalikan `409 scan_pending`; ke versi yang pemindaiannya gagal, `400 scan_failed`.

### Jangkauan

`reach` merangkum, dalam satu nilai, seberapa jauh jangkauan suatu versi di mesin anggota dan di luarnya:

| Nilai        | Arti                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `remote`     | Mendeklarasikan server MCP atau CLI, apa pun yang dideklarasikannya selain itu.                                                                                                                                                                                                                                                                                                                                                         |
| `privileged` | Tidak mendeklarasikan server MCP atau CLI, tetapi mendeklarasikan hook, monitor (perintah latar belakang yang terus berjalan selama sesi), server LSP (Language Server Protocol), atau pengaturan yang diterapkan plugin ke aplikasi anggota, atau berisi skill atau command yang menyetujui alat untuk dirinya sendiri sebelumnya (`allowed-tools` di frontmatter-nya). Semua ini berjalan, atau berlaku, di komputer anggota sendiri. |
| `contained`  | Tidak mendeklarasikan server MCP, CLI, hook, monitor, server LSP, atau pengaturan aplikasi, dan tidak ada skill atau command-nya yang menyetujui alat sebelumnya (misalnya, plugin yang hanya berisi skill, command, dan agent, tanpa satu pun yang memiliki `allowed-tools`).                                                                                                                                                          |

`reach` memperhitungkan semua yang dideklarasikan versi tersebut, termasuk monitor, server LSP, dan pengaturan aplikasi, yang tidak dicantumkan oleh `components`, sehingga versi dengan daftar `components` kosong tetap dapat bernilai `privileged`. Nilainya `null` untuk versi yang disimpan sebelum komponen dicatat, dan untuk versi yang jangkauannya tidak dapat ditentukan karena salah satu file skill atau command-nya tidak dapat dibaca; perlakukan `null` sebagai tidak terklasifikasi.

### Persyaratan unggahan

Unggahan mengikuti aturan yang sama dengan unggahan plugin di claude.ai, sehingga arsip yang sama diterima di kedua tempat.

* Unggahan berupa satu arsip `.zip` atau `.plugin`, atau sekumpulan file individual. Arsip dapat membungkus semuanya dalam satu folder tingkat atas.
* Unggahan harus berisi tepat satu manifest, di `.claude-plugin/plugin.json`, yang harus mendeklarasikan `name`. `SKILL.md` saja tanpa manifest akan ditolak.
* `SKILL.md` tingkat atas yang frontmatter-nya mendeklarasikan komponen plugin digabungkan ke dalam manifest; `plugin.json` yang berlaku di mana pun keduanya menetapkan nilai.
* `name` dapat berisi huruf kecil (dari alfabet apa pun), angka, dan tanda hubung, hingga 64 karakter. Huruf besar, spasi, garis bawah, dan tanda baca lainnya ditolak.
* `displayName` paling banyak 64 karakter dan `description` paling banyak 500.
* Setiap `SKILL.md` memerlukan frontmatter YAML yang valid dengan `name` dan `description`, yang keduanya tidak boleh berisi tag XML seperti `<example>`. Dua skill, atau dua command, tidak boleh memiliki nama yang sama.
* Tidak boleh ada file di bawah direktori `bin/` tingkat atas.
* Tidak boleh ada file `.zip` bersarang. Server MCP terpaket (`.mcpb`, `.dxt`) diizinkan.
* Path file harus relatif, tidak berisi `..`, dan hanya menggunakan huruf, angka, spasi, dan `_ . - / ( ) ,`.
* Body permintaan dan arsip yang tidak terkompresi masing-masing paling besar 200 MB; body permintaan yang melebihi batas mengembalikan `413` (`request_too_large`), bukan `400`. Unggahan memiliki paling banyak 5.000 file, kedalaman path 12, path sepanjang 472 karakter, dan nama file atau folder sepanjang 255 karakter.
* Arsip ZIP harus menggunakan kompresi DEFLATE atau STORE, dan tidak boleh dienkripsi atau berisi tautan simbolik.
* Marketplace menampung paling banyak 500 item, termasuk plugin-nya dan skill mandiri apa pun yang disimpan anggota di dalamnya. Batas ini dan batas 5.000 file adalah nilai saat ini yang dapat dinaikkan.

## Contoh alur kerja

### Publikasikan setiap build dari pipeline rilis

Unggah setiap build bertag dari CI, dan biarkan pipeline menentukan kapan suatu build disajikan.

1. Temukan marketplace tujuan unggahan dengan `GET /v1/organizations/plugin_marketplaces?owner_type=organization`, atau hilangkan `marketplace_id` untuk menggunakan library marketplace.
2. Pada rilis pertama, [buat plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api#create-a-plugin) dengan `POST /v1/organizations/plugins`. Pada setiap rilis berikutnya, catat `latest_version_id` plugin, lalu [unggah versi](https://platform.claude.com/docs/id/manage-claude/plugins-api#create-a-version) dengan `POST /v1/organizations/plugins/{plugin_id}/versions`. Jika respons unggahan hilang, baca plugin dan coba lagi hanya jika `latest_version_id` tidak berubah (lihat [Mencoba ulang unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#retrying-uploads)).
3. Agar anggota tetap menggunakan versi saat ini selama setiap build baru diperiksa, sematkan plugin sekali dengan menetapkan `served_version_id` ke versinya saat ini. Sejak saat itu setiap unggahan disimpan tanpa disajikan, dan sematan tidak dapat dibatalkan: setiap build yang ingin Anda sajikan memerlukan langkah 5.
4. Saat pemindaian konten aktif, lakukan polling `GET /v1/organizations/plugins/{plugin_id}/versions/{version}` hingga `content_scan.status` tidak lagi `processing`, dan promosikan hanya jika nilainya `completed` dengan `pass` atau `warn`.
5. [Promosikan build](https://platform.claude.com/docs/id/manage-claude/plugins-api#change-the-served-version) dengan `POST /v1/organizations/plugins/{plugin_id}` dan `{"served_version_id": "<the new version's ID>"}`. Untuk rollback, kirim ID versi sebelumnya dengan cara yang sama.

### Luncurkan plugin ke grup percontohan, lalu ke semua orang

1. Cari ID grup percontohan dengan `GET /v1/organizations/rbac_groups`. Panggilan tersebut memerlukan cakupan `read:rbac_groups`, yang memerlukan kunci yang dibuat untuk semua organisasi tertaut (lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management#groups)). Langkah-langkah berikutnya memerlukan `write:plugins`, yang hanya bertindak pada organisasi tempat kuncinya dibuat, jadi di perusahaan dengan beberapa organisasi tertaut, buat kunci ini di organisasi yang memiliki plugin tersebut dan berikan kedua cakupan, atau gunakan kunci kedua yang dibuat di sana untuk langkah-langkah tersebut.

2. [Berikan grup pengaturannya sendiri](https://platform.claude.com/docs/id/manage-claude/plugins-api#set-an-installation-setting), misalnya `auto_install`, dengan `POST /v1/organizations/plugins/{plugin_id}/installation_settings/{target}`, di mana `{target}` adalah ID `rbac_group_` grup tersebut, sementara nilai tingkat organisasi tetap `not_available`. Hanya anggota grup yang mendapatkan plugin.

3. Saat masa percontohan berakhir, tetapkan nilai tingkat organisasi (ini secara permanen menghentikan plugin mewarisi default marketplace-nya, seperti yang dijelaskan di [Menetapkan pengaturan instalasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#set-an-installation-setting)), lalu hapus pengaturan grup agar grup kembali mengikuti organisasi:

   <CodeGroup>
     ```bash cURL
     curl -X POST "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/installation_settings/organization" \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "anthropic-beta: ce-plugins-2026-09-01" \
       -d '{"installation_preference": "required"}'
     ```

     ```bash CLI
     ant beta:organization:plugins:installation-settings set \
       --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
       --target organization \
       --installation-preference required
     ```

     ```python Python
     client = anthropic.Anthropic()

     setting = client.beta.organization.plugins.installation_settings.set(
         "organization",
         plugin_id="plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
         installation_preference="required",
     )

     print(f"plugin_id: {setting.plugin_id}")
     print(f"installation_preference: {setting.installation_preference}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const setting = await client.beta.organization.plugins.installationSettings.set(
       "organization",
       {
         plugin_id: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
         installation_preference: "required"
       }
     );

     console.log(`plugin_id: ${setting.plugin_id}`);
     console.log(`installation_preference: ${setting.installation_preference}`);
     ```

     ```csharp C#
     using Anthropic.Models.Beta.Organization.Plugins.InstallationSettings;

     AnthropicClient client = new();

     var setting = await client.Beta.Organization.Plugins.InstallationSettings.Set(
         "organization",
         new()
         {
             PluginID = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
             InstallationPreference = InstallationPreference.Required,
         }
     );

     Console.WriteLine($"plugin_id: {setting.PluginID}");
     Console.WriteLine($"installation_preference: {setting.InstallationPreference.Raw()}");
     ```

     ```go Go
     client := anthropic.NewClient()

     setting, err := client.Beta.Organization.Plugins.InstallationSettings.Set(
     	context.Background(),
     	"organization",
     	anthropic.BetaOrganizationPluginInstallationSettingSetParams{
     		PluginID:               "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
     		InstallationPreference: anthropic.BetaOrganizationPluginInstallationSettingSetParamsInstallationPreferenceRequired,
     	},
     )
     if err != nil {
     	log.Fatal(err)
     }

     fmt.Printf("plugin_id: %s\n", setting.PluginID)
     fmt.Printf("installation_preference: %s\n", setting.InstallationPreference)
     ```

     ```java Java
     import com.anthropic.models.beta.organization.plugins.installationsettings.InstallationSettingSetParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = InstallationSettingSetParams.builder()
             .pluginId("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")
             .installationPreference(InstallationSettingSetParams.InstallationPreference.REQUIRED)
             .build();
         var setting = client.beta().organization().plugins().installationSettings()
             .set("organization", params);

         IO.println("plugin_id: " + setting.pluginId());
         IO.println("installation_preference: " + setting.installationPreference().asString());
     }
     ```

     ```php PHP
     use Anthropic\Beta\Organization\Plugins\InstallationSettings\InstallationSettingSetParams\InstallationPreference;
     // ...

     $client = new Client();

     $setting = $client->beta->organization->plugins->installationSettings->set(
         target: 'organization',
         pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
         installationPreference: InstallationPreference::REQUIRED,
     );

     echo "plugin_id: {$setting->pluginID}\n";
     echo "installation_preference: {$setting->installationPreference}\n";
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
     setting = client.beta.organization.plugins.installation_settings.set(
       "organization",
       plugin_id: plugin_id,
       installation_preference: :required
     )

     puts "plugin_id: #{setting.plugin_id}"
     puts "installation_preference: #{setting.installation_preference}"
     ```
   </CodeGroup>

   Kemudian hapus pengaturan grup dengan `DELETE /v1/organizations/plugins/{plugin_id}/installation_settings/{target}`, di mana `{target}` adalah ID grup. Pengaturan grup menggantikan nilai tingkat organisasi untuk anggotanya alih-alih menambahkannya, sehingga pengaturan grup `available` yang tersisa akan membuat anggota tersebut tetap pada `available`.

### Jaga inventaris keamanan tetap sinkron

Jalankan job malam hari yang menandai plugin yang menjangkau di luar sesi anggota atau gagal dalam pemindaian kontennya.

1. Telusuri halaman demi halaman [`GET /v1/organizations/plugins?limit=100`](https://platform.claude.com/docs/id/manage-claude/plugins-api#list-plugins) hingga `next_page` bernilai `null`, dengan meneruskan sendiri `next_page` setiap halaman sebagai `page` alih-alih menggunakan iterator daftar SDK, yang dapat berhenti lebih awal pada daftar ini (lihat [Paginasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#pagination)). Baca `reach` dan `content_scan` setiap plugin dari daftar tersebut pada setiap eksekusi: putusan pemindaian yang tiba belakangan tidak mengubah `updated_at`. `updated_at` memberi tahu Anda plugin mana yang memiliki konten baru atau versi yang disajikan baru sejak eksekusi terakhir (layak untuk diunduh ulang arsipnya); pencantuman ulang secara penuh juga yang menangkap penghapusan, karena plugin yang dihapus oleh sinkronisasi Git atau penghapusan akun menghilang tanpa peristiwa.
2. Tandai setiap plugin yang `reach`-nya `remote` (mendeklarasikan server MCP atau CLI), atau yang `content_scan.assessment`-nya `fail` atau `unknown`.
3. Untuk setiap plugin yang ditandai, unduh arsip versi yang disajikan untuk ditinjau dengan `GET /v1/organizations/plugins/{plugin_id}/versions/{served_version_id}/content` (lihat [Mengunduh file suatu versi](https://platform.claude.com/docs/id/manage-claude/plugins-api#download-a-versions-files)).
4. Untuk menarik plugin dari anggota selama Anda meninjaunya, lihat [Menghapus plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api#delete-a-plugin) untuk opsi yang dapat dibatalkan (milik organisasi) dan yang permanen.

## Plugin

Objek plugin menjelaskan plugin di salah satu marketplace organisasi Anda atau di marketplace pribadi anggota (respons [Mulai cepat](https://platform.claude.com/docs/id/manage-claude/plugins-api#quick-start) menunjukkan contoh lengkapnya). `display_name`, `description`, `manifest_version`, `content_scan`, `components`, dan `reach`-nya menjelaskan versi yang **disajikan**, sehingga satu panggilan daftar menunjukkan apa yang sedang disajikan kepada anggota.

| Field                                                                                    | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                                     | Berawalan `plugin_`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `name`                                                                                   | Dari manifest. Unik di dalam marketplace-nya, bukan di seluruh organisasi. Tetap untuk plugin milik organisasi; berubah jika anggota mengganti nama plugin miliknya sendiri di claude.ai.                                                                                                                                                                                                                                                                                                                                                                                                             |
| `display_name`, `description`, `manifest_version`                                        | `displayName`, `description`, dan `version` manifest dari versi yang disajikan; masing-masing bernilai `null` jika manifest tidak mendeklarasikannya. `manifest_version` dinormalisasi untuk tampilan: satu awalan `v` atau `V` dihapus, sehingga `version` manifest `"v1.4.0"` dikembalikan sebagai `"1.4.0"`. Nilainya juga `null` untuk nilai yang tidak terlihat seperti nomor versi, seperti `"latest"`, dan untuk versi plugin yang dibuat sebelum claude.ai mulai mencatat field ini pada Agustus 2026. Unggahan tidak pernah ditolak karena `version`-nya, dan `manifest_version` tidak unik. |
| `served_version_id`, `latest_version_id`                                                 | Berawalan `pluginver_`: versi yang disajikan kepada anggota, dan versi terbaru. Lihat [Versi dan versi yang disajikan](https://platform.claude.com/docs/id/manage-claude/plugins-api#versions-and-the-served-version).                                                                                                                                                                                                                                                                                                                                                                                |
| `served_version_pinned`                                                                  | `false` selama versi yang disajikan mengikuti setiap versi baru; `true` setelah suatu versi dipilih secara eksplisit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `owner`                                                                                  | `{"type": "organization"}`, atau `{"type": "user", "user_id": "user_..."}` untuk marketplace pribadi anggota.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `marketplace_id`                                                                         | Berawalan `marketplace_`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `created_by`                                                                             | Siapa yang membuat plugin: `{"type": "user_actor", "user_id": "user_...", "email_address": "..."}` untuk orang di claude.ai (`email_address` dapat bernilai `null`), atau `{"type": "api_actor", "api_key_id": "apikey_..."}` untuk kunci API. Jenis aktor lain dapat muncul. `null` jika tidak ada pembuat yang tercatat, seperti untuk plugin yang disinkronkan dari Git.                                                                                                                                                                                                                           |
| `organization_installation_preference`, `organization_installation_preference_inherited` | Milik organisasi: nilai tingkat organisasi, dan apakah nilai tersebut berasal dari default marketplace (lihat [Pengaturan instalasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#installation-settings)). Milik anggota: keduanya `null`.                                                                                                                                                                                                                                                                                                                                           |
| `content_scan`                                                                           | Hasil pemindaian versi yang disajikan, berupa objek dengan `status`, `assessment`, dan `reason` (dijelaskan setelah tabel ini). `null` jika tidak pernah dipindai.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `components`                                                                             | Komponen versi yang disajikan, masing-masing `{"type", "name", "description"}` dengan `type` salah satu dari `skill`, `mcp_server`, `command`, `agent`, `hook`, atau `cli`, dicantumkan dalam urutan jenis tersebut lalu berdasarkan nama. Untuk server MCP, `name` adalah kuncinya di manifest; untuk hook, peristiwa tempat hook tersebut berjalan; untuk CLI, nama executable-nya. `description` selalu `null` untuk server MCP, hook, dan CLI. `null` jika tidak tercatat.                                                                                                                        |
| `reach`                                                                                  | `contained`, `privileged`, atau `remote`. Lihat [Jangkauan](https://platform.claude.com/docs/id/manage-claude/plugins-api#reach).                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `updated_at`                                                                             | Hanya berubah ketika versi baru disimpan atau versi yang disajikan berubah. Tidak berubah untuk pengaturan instalasi, berbagi, atau hasil pemindaian baru.                                                                                                                                                                                                                                                                                                                                                                                                                                            |

Objek `content_scan`:

| Field        | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `status`     | `processing` selama pemindaian berjalan, `completed` ketika selesai, atau `errored` ketika tidak dapat diselesaikan (atau, sesekali, ketika hasilnya tidak dapat dibaca untuk respons ini, dalam hal ini pembacaan berikutnya mungkin melaporkannya). Anggota tidak disajikan versi yang pemindaiannya `processing` atau `errored`; mengunggah konten lagi sebagai versi baru akan mendapatkan pemindaian baru. |
| `assessment` | Ditetapkan ketika `status` bernilai `completed`: `pass` (tidak ada yang ditemukan), `warn` (ditemukan sesuatu yang tidak memblokir penggunaan), `fail` (ditemukan sesuatu yang memblokir penggunaan), atau `unknown` (tidak ada putusan). Selain itu `null`.                                                                                                                                                    |
| `reason`     | Untuk `warn` dan `fail`, kekhawatiran utama, dari daftar berikut. Selain itu `null`, dan juga `null` pada pemindaian lama yang dibuat sebelum alasan mulai dicatat.                                                                                                                                                                                                                                             |

<Accordion title="Nilai reason pemindaian konten">
  | `reason`                          | Arti                                                                                                                                             |
  | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
  | `covert-usage-telemetry`          | Memerintahkan Claude untuk mengirim informasi tentang anggota atau penggunaannya ke alamat luar tanpa memberi tahu mereka.                       |
  | `undisclosed-data-destination`    | Mengirim file, email, dokumen, atau konten lain ke tujuan luar yang tetap, yang tidak ditampilkan kepada anggota dan tidak dikendalikan olehnya. |
  | `remote-code-instruction-loader`  | Memerintahkan Claude untuk mengunduh dan menjalankan, atau mengikuti instruksi dari, konten luar yang dapat berubah setelah plugin diinstal.     |
  | `credential-exposure`             | Berisi kredensial aktif, atau mengumpulkan kredensial atau token dari lingkungan anggota.                                                        |
  | `guardrail-tampering`             | Melemahkan pengaman anggota, misalnya dengan menyetujui sebelumnya setiap prompt izin.                                                           |
  | `system-prompt-spoofing`          | Meniru atau mencoba menggantikan instruksi sistem Claude.                                                                                        |
  | `covert-record-tampering`         | Diam-diam mengubah, menyembunyikan, atau menghapus informasi yang seharusnya dilihat anggota.                                                    |
  | `covert-behavior-override`        | Mengubah perilaku Claude melampaui tujuan plugin dan menyembunyikan perubahan tersebut dari anggota.                                             |
  | `hidden-code-execution`           | Menjalankan kode yang dibundel sambil memerintahkan Claude untuk tidak mengungkapkan apa yang dilakukannya.                                      |
  | `undisclosed-promotion-injection` | Menyisipkan konten promosi yang tidak diungkapkan ke dalam output Claude.                                                                        |
  | `hidden-identity-gate`            | Mengubah atau menghentikan perilakunya tergantung pada akun mana yang menjalankannya, tanpa menjelaskan alasannya.                               |
  | `destructive-persistence`         | Dapat menghapus atau merusak file anggota, atau menginstal program yang tetap ada setelah plugin tidak ada lagi.                                 |
  | `unanalyzable-binary`             | Menyertakan program yang dikompilasi atau tidak dapat dibaca, sehingga pemindaian tidak dapat memverifikasi apa yang dilakukannya.               |
  | `other`                           | Kekhawatiran lain apa pun, termasuk yang lebih baru dari daftar ini.                                                                             |
</Accordion>

`plugin_id` yang tidak memiliki awalan `plugin_` mengembalikan `400`. `plugin_id` yang memiliki awalan tersebut tetapi tidak dapat di-resolve, milik organisasi lain, atau merujuk ke skill mandiri mengembalikan `404`.

### Daftar plugin

`GET /v1/organizations/plugins` mencantumkan setiap plugin di organisasi Anda, di marketplace organisasi dan di marketplace pribadi anggota, diurutkan berdasarkan `created_at` secara menurun. Filter berdasarkan `owner_type` (`organization` atau `user`), `owner_user_id` (berawalan `user_`; plugin milik seorang anggota, termasuk setelah anggota tersebut keluar dari organisasi), `marketplace_id`, dan `created_at[gte]`, `created_at[gt]`, `created_at[lte]`, `created_at[lt]` (timestamp RFC 3339). Filter digabungkan dengan AND. `marketplace_id` atau `owner_user_id` yang tidak cocok dengan apa pun di organisasi Anda mengembalikan halaman kosong, bukan error. Respons memiliki bentuk yang ditunjukkan di [Mulai cepat](https://platform.claude.com/docs/id/manage-claude/plugins-api#quick-start). Memerlukan cakupan `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins?owner_type=organization&limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins list --owner-type organization --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  plugins = client.beta.organization.plugins.list(owner_type="organization", limit=20)

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for plugin in plugins:
      print(f"{plugin.id}: {plugin.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const plugins = await client.beta.organization.plugins.list({
    owner_type: "organization",
    limit: 20
  });

  for await (const plugin of plugins) {
    console.log(`${plugin.id}: ${plugin.name}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Plugins;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Plugins.List(
      new() { OwnerType = OwnerType.Organization, Limit = 20 }
  );

  await foreach (var plugin in page.Paginate())
  {
      Console.WriteLine($"{plugin.ID}: {plugin.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  plugins := client.Beta.Organization.Plugins.ListAutoPaging(context.Background(), anthropic.BetaOrganizationPluginListParams{
  	OwnerType: anthropic.BetaOrganizationPluginListParamsOwnerTypeOrganization,
  	Limit:     anthropic.Int(20),
  })

  for plugins.Next() {
  	plugin := plugins.Current()
  	fmt.Printf("%s: %s\n", plugin.ID, plugin.Name)
  }
  if err := plugins.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.PluginListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginListParams.builder()
          .ownerType(PluginListParams.OwnerType.ORGANIZATION)
          .limit(20)
          .build();
      var plugins = client.beta().organization().plugins().list(params);

      for (var plugin : plugins.autoPager()) {
          IO.println(plugin.id() + ": " + plugin.name());
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Plugins\PluginListParams\OwnerType;
  // ...

  $client = new Client();

  $plugins = $client->beta->organization->plugins->list(
      limit: 20,
      ownerType: OwnerType::ORGANIZATION,
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $plugins->nextPage.
  foreach ($plugins->getItems() as $plugin) {
      echo "{$plugin->id}: {$plugin->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.plugins.list(owner_type: :organization, limit: 20)

  page.auto_paging_each do |plugin|
    puts "#{plugin.id}: #{plugin.name}"
  end
  ```
</CodeGroup>

### Membuat plugin

`POST /v1/organizations/plugins` membuat plugin milik organisasi beserta versi pertamanya dalam satu panggilan; versi tersebut menjadi "served version" (versi yang disajikan). Body berupa `multipart/form-data`: `files[]` berisi satu arsip `.zip` atau `.plugin`, atau satu part per file, dengan nama file setiap part berupa path file tersebut di dalam plugin (misalnya `.claude-plugin/plugin.json`). Field opsionalnya adalah `marketplace_id` (marketplace `manual` milik organisasi; default-nya adalah marketplace library Anda, yang dibuat saat pertama kali digunakan) dan `release_notes` (hingga 5.000 karakter, ditampilkan di riwayat versi claude.ai dan dikembalikan pada versi). `name`, `display_name`, `description`, dan `manifest_version` plugin diambil dari manifest yang diunggah, dan unggahan harus memenuhi [persyaratan unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#upload-requirements). Saat pemindaian konten aktif, `content_scan.status` pada respons bernilai `processing` dan hasil pemindaiannya tiba secara asinkron. Mengembalikan plugin. Memerlukan scope `write:plugins`.

Mengunggah arsip:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugins" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -F "files[]=@dist/sales-toolkit.zip" \
    -F "release_notes=First release"
  ```

  ```bash CLI
  ant beta:organization:plugins create \
    --file dist/sales-toolkit.zip \
    --release-notes "First release"
  ```

  ```python Python
  client = anthropic.Anthropic()

  with open("dist/sales-toolkit.zip", "rb") as archive:
      plugin = client.beta.organization.plugins.create(
          files=[archive],
          release_notes="First release",
      )

  print(f"id: {plugin.id}")
  print(f"served_version_id: {plugin.served_version_id}")
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  const plugin = await client.beta.organization.plugins.create({
    files: [fs.createReadStream("dist/sales-toolkit.zip")],
    release_notes: "First release"
  });

  console.log(`id: ${plugin.id}`);
  console.log(`served_version_id: ${plugin.served_version_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var plugin = await client.Beta.Organization.Plugins.Create(
      new()
      {
          Files = [File.OpenRead("dist/sales-toolkit.zip")],
          ReleaseNotes = "First release",
      }
  );

  Console.WriteLine($"id: {plugin.ID}");
  Console.WriteLine($"served_version_id: {plugin.ServedVersionID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  archive, err := os.Open("dist/sales-toolkit.zip")
  if err != nil {
  	log.Fatal(err)
  }
  defer archive.Close()

  plugin, err := client.Beta.Organization.Plugins.New(context.Background(), anthropic.BetaOrganizationPluginNewParams{
  	Files:        []io.Reader{archive},
  	ReleaseNotes: anthropic.String("First release"),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", plugin.ID)
  fmt.Printf("served_version_id: %s\n", plugin.ServedVersionID)
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.organization.plugins.PluginCreateParams;

  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Susun bagian `files[]` secara manual agar arsip dikirim beserta nama filenya,
      // yang diwajibkan oleh proses unggah.
      var archive = MultipartField.<List<InputStream>>builder()
          .value(List.of(Files.newInputStream(Path.of("dist/sales-toolkit.zip"))))
          .filename("sales-toolkit.zip")
          .contentType("application/octet-stream")
          .build();
      var params = PluginCreateParams.builder()
          .files(archive)
          .releaseNotes("First release")
          .build();
      var plugin = client.beta().organization().plugins().create(params);

      IO.println("id: " + plugin.id());
      IO.println("served_version_id: " + plugin.servedVersionId());
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  $plugin = $client->beta->organization->plugins->create(
      files: [
          FileParam::fromResource(fopen('dist/sales-toolkit.zip', 'r')),
      ],
      releaseNotes: 'First release',
  );

  echo "id: {$plugin->id}\n";
  echo "served_version_id: {$plugin->servedVersionID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin = client.beta.organization.plugins.create(
    files: [Pathname("dist/sales-toolkit.zip")],
    release_notes: "First release"
  )

  puts "id: #{plugin.id}"
  puts "served_version_id: #{plugin.served_version_id}"
  ```
</CodeGroup>

```json
{
  "type": "plugin",
  "id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  "name": "sales-toolkit",
  "display_name": "Sales Toolkit",
  "description": "Account research and call prep for the sales team.",
  "served_version_id": "pluginver_01Km7tL4pR9xF5sU2zV3jP6q",
  "served_version_pinned": false,
  "latest_version_id": "pluginver_01Km7tL4pR9xF5sU2zV3jP6q",
  "manifest_version": "1.4.0",
  "owner": { "type": "organization" },
  "marketplace_id": "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
  "created_by": { "type": "api_actor", "api_key_id": "apikey_01Nq9vN6rT2zH7uW4bX5mR8s" },
  "organization_installation_preference": "available",
  "organization_installation_preference_inherited": true,
  "content_scan": { "status": "processing", "assessment": null, "reason": null },
  "components": [
    {
      "type": "skill",
      "name": "account-research",
      "description": "Researches a customer account before a call."
    },
    { "type": "mcp_server", "name": "crm", "description": null }
  ],
  "reach": "remote",
  "created_at": "2026-09-01T17:04:11Z",
  "updated_at": "2026-09-01T17:04:11Z"
}
```

Mengunggah file satu per satu ke marketplace tertentu. Lampirkan setiap file dengan path-nya di dalam plugin (sufiks `;filename=` pada contoh cURL, argumen nama file pada contoh SDK); file yang dikirim hanya dengan nama dasarnya akan membuat manifest tidak ditemukan. SDK TypeScript dan Java serta CLI `ant` belum dapat melampirkan file dengan path, sehingga contoh-contoh tersebut mengunggah plugin sebagai satu arsip ke marketplace:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugins" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -F "files[]=@.claude-plugin/plugin.json;filename=.claude-plugin/plugin.json" \
    -F "files[]=@skills/account-research/SKILL.md;filename=skills/account-research/SKILL.md" \
    -F "marketplace_id=marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  ```

  ```bash CLI
  # CLI mengirim setiap file hanya dengan nama dasarnya,
  # jadi unggah plugin sebagai satu arsip saja.
  ant beta:organization:plugins create \
    --file dist/sales-toolkit.zip \
    --marketplace-id marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Tuple (filename, file) mempertahankan path setiap file di dalam plugin;
  # objek file biasa hanya akan dikirim dengan nama dasarnya saja.
  with (
      open(".claude-plugin/plugin.json", "rb") as manifest,
      open("skills/account-research/SKILL.md", "rb") as skill_md,
  ):
      plugin = client.beta.organization.plugins.create(
          files=[
              (".claude-plugin/plugin.json", manifest),
              ("skills/account-research/SKILL.md", skill_md),
          ],
          marketplace_id="marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
      )

  print(f"id: {plugin.id}")
  print(f"served_version_id: {plugin.served_version_id}")
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  // SDK TypeScript mengirim setiap file dengan nama dasarnya,
  // jadi unggah plugin sebagai satu arsip.
  const plugin = await client.beta.organization.plugins.create({
    files: [fs.createReadStream("dist/sales-toolkit.zip")],
    marketplace_id: "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  });

  console.log(`id: ${plugin.id}`);
  console.log(`served_version_id: ${plugin.served_version_id}`);
  ```

  ```csharp C#
  using Anthropic.Core;

  AnthropicClient client = new();

  // FileName mempertahankan path setiap file di dalam plugin; tanpanya, FileStream
  // hanya dikirim dengan nama dasarnya.
  var plugin = await client.Beta.Organization.Plugins.Create(
      new()
      {
          Files =
          [
              new BinaryContent
              {
                  Stream = File.OpenRead(".claude-plugin/plugin.json"),
                  FileName = ".claude-plugin/plugin.json",
              },
              new BinaryContent
              {
                  Stream = File.OpenRead("skills/account-research/SKILL.md"),
                  FileName = "skills/account-research/SKILL.md",
              },
          ],
          MarketplaceID = "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
      }
  );

  Console.WriteLine($"id: {plugin.ID}");
  Console.WriteLine($"served_version_id: {plugin.ServedVersionID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  manifest, err := os.Open(".claude-plugin/plugin.json")
  if err != nil {
  	log.Fatal(err)
  }
  defer manifest.Close()

  skillMd, err := os.Open("skills/account-research/SKILL.md")
  if err != nil {
  	log.Fatal(err)
  }
  defer skillMd.Close()

  // anthropic.File mempertahankan path setiap file di dalam plugin sebagai nama file bagian tersebut;
  // *os.File biasa akan dikirim dengan nama dasarnya sehingga manifest tidak akan ditemukan.
  plugin, err := client.Beta.Organization.Plugins.New(context.Background(), anthropic.BetaOrganizationPluginNewParams{
  	Files: []io.Reader{
  		anthropic.File(manifest, ".claude-plugin/plugin.json", "application/json"),
  		anthropic.File(skillMd, "skills/account-research/SKILL.md", "text/markdown"),
  	},
  	MarketplaceID: anthropic.String("marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", plugin.ID)
  fmt.Printf("served_version_id: %s\n", plugin.ServedVersionID)
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.organization.plugins.PluginCreateParams;

  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Setter `files` pada PluginCreateParams hanya menerima satu nama file untuk seluruh
      // daftar, jadi unggah plugin sebagai satu arsip saja: satu bagian yang dibuat manual
      // yang membawa nama file arsip tersebut, sebagaimana diwajibkan oleh proses unggah.
      var archive = MultipartField.<List<InputStream>>builder()
          .value(List.of(Files.newInputStream(Path.of("dist/sales-toolkit.zip"))))
          .filename("sales-toolkit.zip")
          .contentType("application/octet-stream")
          .build();
      var params = PluginCreateParams.builder()
          .files(archive)
          .marketplaceId("marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r")
          .build();
      var plugin = client.beta().organization().plugins().create(params);

      IO.println("id: " + plugin.id());
      IO.println("served_version_id: " + plugin.servedVersionId());
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  $plugin = $client->beta->organization->plugins->create(
      files: [
          FileParam::fromResource(
              fopen('.claude-plugin/plugin.json', 'r'),
              filename: '.claude-plugin/plugin.json',
          ),
          FileParam::fromResource(
              fopen('skills/account-research/SKILL.md', 'r'),
              filename: 'skills/account-research/SKILL.md',
          ),
      ],
      marketplaceID: 'marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r',
  );

  echo "id: {$plugin->id}\n";
  echo "served_version_id: {$plugin->servedVersionID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # FilePart dengan filename: mempertahankan path tiap file di dalam plugin;
  # Pathname biasa hanya akan dikirim dengan nama dasarnya saja.
  plugin = client.beta.organization.plugins.create(
    files: [
      Anthropic::FilePart.new(
        Pathname(".claude-plugin/plugin.json"),
        filename: ".claude-plugin/plugin.json"
      ),
      Anthropic::FilePart.new(
        Pathname("skills/account-research/SKILL.md"),
        filename: "skills/account-research/SKILL.md"
      )
    ],
    marketplace_id: "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  )

  puts "id: #{plugin.id}"
  puts "served_version_id: #{plugin.served_version_id}"
  ```
</CodeGroup>

Selain `400` untuk unggahan yang melanggar [persyaratan unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#upload-requirements) (`413` untuk body permintaan lebih dari 200 MB) dan respons bersama (`403` ketika `marketplace_id` adalah marketplace pribadi milik anggota; lihat [Respons error](https://platform.claude.com/docs/id/manage-claude/plugins-api#error-responses)), pembuatan plugin dapat gagal dengan:

| Status                     | Penyebab                                                                                                           | Yang harus dilakukan                                                                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 404                        | `marketplace_id` bukan marketplace milik organisasi Anda.                                                          | Ambil ID dari [Mencantumkan marketplace](https://platform.claude.com/docs/id/manage-claude/plugins-api#list-marketplaces).                                                                         |
| 400                        | Marketplace disinkronkan dari Git, atau sudah berisi 500 plugin dan skill.                                         | Unggah ke marketplace `manual`, atau ubah repositorinya.                                                                                                                                           |
| 409 `plugin_name_taken`    | Nama tersebut sudah dipakai di marketplace itu.                                                                    | Lanjutkan dengan `details.plugin_id` (unggah versi ke plugin tersebut), atau ubah `name` pada manifest.                                                                                            |
| 409 `skill_name_taken`     | Plugin akan masuk ke marketplace library dan salah satu skill-nya memiliki nama yang sama dengan skill organisasi. | Ganti nama skill tersebut, atau hapus skill organisasi di claude.ai.                                                                                                                               |
| 409 (tanpa `error_code`)   | Unggahan lain dengan nama yang sama ke marketplace yang sama masih berlangsung.                                    | Coba lagi sebentar lagi.                                                                                                                                                                           |
| 503 `registration_pending` | Plugin telah dibuat tetapi pendaftarannya belum selesai.                                                           | Jangan kirim ulang; unggah file yang sama sebagai versi dari `details.plugin_id` (lihat [Mencoba ulang unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#retrying-uploads)). |

### Mendapatkan plugin

`GET /v1/organizations/plugins/{plugin_id}` mengembalikan satu plugin. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins retrieve \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL
  ```

  ```python Python
  client = anthropic.Anthropic()

  plugin = client.beta.organization.plugins.retrieve("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")

  print(f"id: {plugin.id}")
  print(f"name: {plugin.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const plugin = await client.beta.organization.plugins.retrieve(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  );

  console.log(`id: ${plugin.id}`);
  console.log(`name: ${plugin.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var plugin = await client.Beta.Organization.Plugins.Retrieve("plugin_01Hq3vX8kZcN2mB7pR4tY9wL");

  Console.WriteLine($"id: {plugin.ID}");
  Console.WriteLine($"name: {plugin.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  plugin, err := client.Beta.Organization.Plugins.Get(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", plugin.ID)
  fmt.Printf("name: %s\n", plugin.Name)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var plugin = client.beta().organization().plugins()
      .retrieve("plugin_01Hq3vX8kZcN2mB7pR4tY9wL");

  IO.println("id: " + plugin.id());
  IO.println("name: " + plugin.name());
  ```

  ```php PHP
  $client = new Client();

  $plugin = $client->beta->organization->plugins->retrieve(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
  );

  echo "id: {$plugin->id}\n";
  echo "name: {$plugin->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  plugin = client.beta.organization.plugins.retrieve(plugin_id)

  puts "id: #{plugin.id}"
  puts "name: #{plugin.name}"
  ```
</CodeGroup>

### Mengubah versi yang disajikan

`POST /v1/organizations/plugins/{plugin_id}` mengubah versi plugin milik organisasi yang disajikan kepada anggota. Berikan versi yang lebih lama untuk melakukan rollback, atau versi yang lebih baru untuk mempromosikan build yang disimpan tanpa disajikan. Tindakan ini menyematkan ("pin") plugin, dan plugin yang disematkan saat ini tidak dapat dilepas sematannya, baik di sini maupun di claude.ai (lihat [Versi dan versi yang disajikan](https://platform.claude.com/docs/id/manage-claude/plugins-api#versions-and-the-served-version)). Satu-satunya field yang dapat diperbarui adalah `served_version_id`, dan field ini wajib. Perubahan sampai ke anggota sebelum respons dikembalikan dan tidak membuat versi baru. Saat pemindaian konten aktif, versi tersebut harus merupakan versi yang boleh disajikan kepada anggota (lihat [Pemindaian konten](https://platform.claude.com/docs/id/manage-claude/plugins-api#content-scanning)). Memberikan versi yang sudah disajikan pada plugin yang disematkan tidak mengubah apa pun; memberikannya pada plugin yang tidak disematkan akan menyematkan plugin pada versi tersebut, sehingga unggahan berikutnya tidak lagi disajikan secara otomatis. Mengembalikan plugin. Memerlukan scope `write:plugins`.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -d '{"served_version_id": "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p"}'
  ```

  ```bash CLI
  ant beta:organization:plugins update \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --served-version-id pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p
  ```

  ```python Python
  client = anthropic.Anthropic()

  plugin = client.beta.organization.plugins.update(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      served_version_id="pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
  )

  print(f"id: {plugin.id}")
  print(f"served_version_id: {plugin.served_version_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const plugin = await client.beta.organization.plugins.update(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
    { served_version_id: "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p" }
  );

  console.log(`id: ${plugin.id}`);
  console.log(`served_version_id: ${plugin.served_version_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var plugin = await client.Beta.Organization.Plugins.Update(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      new() { ServedVersionID = "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p" }
  );

  Console.WriteLine($"id: {plugin.ID}");
  Console.WriteLine($"served_version_id: {plugin.ServedVersionID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  plugin, err := client.Beta.Organization.Plugins.Update(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginUpdateParams{
  		ServedVersionID: "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", plugin.ID)
  fmt.Printf("served_version_id: %s\n", plugin.ServedVersionID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.PluginUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginUpdateParams.builder()
          .servedVersionId("pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p")
          .build();
      var plugin = client.beta().organization().plugins()
          .update("plugin_01Hq3vX8kZcN2mB7pR4tY9wL", params);

      IO.println("id: " + plugin.id());
      IO.println("served_version_id: " + plugin.servedVersionId());
  }
  ```

  ```php PHP
  $client = new Client();

  $plugin = $client->beta->organization->plugins->update(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
      servedVersionID: 'pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p',
  );

  echo "id: {$plugin->id}\n";
  echo "served_version_id: {$plugin->servedVersionID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  plugin = client.beta.organization.plugins.update(
    plugin_id,
    served_version_id: "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p"
  )

  puts "id: #{plugin.id}"
  puts "served_version_id: #{plugin.served_version_id}"
  ```
</CodeGroup>

```json
{
  "type": "plugin",
  "id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  "name": "sales-toolkit",
  "display_name": "Sales Toolkit",
  "description": "Account research and call prep for the sales team.",
  "served_version_id": "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
  "served_version_pinned": true,
  "latest_version_id": "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
  "manifest_version": "1.5.0",
  "owner": { "type": "organization" },
  "marketplace_id": "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
  "created_by": { "type": "api_actor", "api_key_id": "apikey_01Nq9vN6rT2zH7uW4bX5mR8s" },
  "organization_installation_preference": "available",
  "organization_installation_preference_inherited": true,
  "content_scan": { "status": "completed", "assessment": "pass", "reason": null },
  "components": [
    {
      "type": "skill",
      "name": "account-research",
      "description": "Researches a customer account before a call."
    },
    { "type": "mcp_server", "name": "crm", "description": null },
    {
      "type": "command",
      "name": "call-prep",
      "description": "Builds a one-page brief for an upcoming call."
    }
  ],
  "reach": "remote",
  "created_at": "2026-09-01T17:04:11Z",
  "updated_at": "2026-09-16T10:02:45Z"
}
```

Selain respons bersama (`403` untuk plugin milik anggota, serta `409 scan_pending` atau `400 scan_failed` untuk versi yang tidak boleh disajikan kepada anggota; lihat [Respons error](https://platform.claude.com/docs/id/manage-claude/plugins-api#error-responses)), permintaan dapat gagal dengan:

| Status                   | Penyebab                                                                                                                                                             | Yang harus dilakukan                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 400                      | Body tidak menyertakan `served_version_id`, mengaturnya ke `null`, atau berisi field lain; atau nilainya tidak memiliki prefiks `pluginver_` atau bernilai `latest`. | Kirim tepat `{"served_version_id": "pluginver_…"}`.                                                                               |
| 404                      | `served_version_id` bukan versi dari plugin ini.                                                                                                                     | Ambil ID dari [Mencantumkan versi plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api#list-a-plugins-versions). |
| 409 (tanpa `error_code`) | Unggahan ke plugin ini atau perubahan versi yang disajikan lainnya masih berlangsung.                                                                                | Coba lagi sebentar lagi.                                                                                                          |
| 409 `skill_name_taken`   | Plugin berada di marketplace library dan versi tersebut memiliki skill yang namanya kini dipakai oleh skill organisasi.                                              | Pilih versi lain, atau ganti nama salah satu skill.                                                                               |

### Menghapus plugin

`DELETE /v1/organizations/plugins/{plugin_id}` menghapus plugin secara permanen beserta setiap versi yang dimilikinya, sama seperti penghapusan oleh administrator di claude.ai. Endpoint ini berfungsi untuk plugin apa pun di marketplace `manual`, termasuk plugin milik anggota, bahkan jika anggota tersebut telah keluar dari organisasi. Saat penghapusan selesai, plugin, versinya, dan file-filenya hilang dari setiap pembacaan, dan plugin tersebut tidak lagi disajikan kepada anggota. Pengaturan instalasi plugin milik organisasi ikut dihapus; pembagian plugin milik anggota ditarik, dan plugin tersebut juga hilang bagi pemiliknya. Plugin di marketplace yang disinkronkan dari Git mengembalikan `400`: hapus plugin tersebut dari repositori, atau hapus marketplace di claude.ai. Memerlukan scope `write:plugins`.

Penghapusan tidak dapat dibatalkan, dan tidak ada penghapusan per versi. Untuk menahan plugin milik organisasi secara reversibel, atur pengaturan instalasi tingkat organisasinya ke `not_available` (plugin yang sebelumnya mewarisi default marketplace-nya akan memiliki pengaturannya sendiri sejak saat itu), lalu hapus (atau atur ke `not_available`) setiap pengaturan grup yang dicantumkan oleh `GET /v1/organizations/plugins/{plugin_id}/installation_settings`, karena pengaturan grup menimpa nilai tingkat organisasi bagi anggotanya. Kirim penulisan ini satu per satu, bukan secara paralel (lihat [Menetapkan pengaturan instalasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#set-an-installation-setting)). Plugin milik anggota tidak dapat ditahan melalui API ini kecuali dengan menghapusnya, dan hanya jika marketplace-nya bertipe `manual`.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins delete --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_plugin = client.beta.organization.plugins.delete(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  )

  print(f"id: {deleted_plugin.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedPlugin = await client.beta.organization.plugins.delete(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  );

  console.log(`id: ${deletedPlugin.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedPlugin = await client.Beta.Organization.Plugins.Delete(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  );

  Console.WriteLine($"id: {deletedPlugin.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedPlugin, err := client.Beta.Organization.Plugins.Delete(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginDeleteParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deletedPlugin.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedPlugin = client.beta().organization().plugins()
      .delete("plugin_01Hq3vX8kZcN2mB7pR4tY9wL");

  IO.println("id: " + deletedPlugin.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedPlugin = $client->beta->organization->plugins->delete(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
  );

  echo "id: {$deletedPlugin->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  deleted_plugin = client.beta.organization.plugins.delete(plugin_id)

  puts "id: #{deleted_plugin.id}"
  ```
</CodeGroup>

```json
{ "type": "plugin_deleted", "id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL" }
```

## Versi plugin

Versi plugin adalah snapshot yang tidak dapat diubah ("immutable") dari file-file plugin dari satu unggahan (respons [Membuat versi](https://platform.claude.com/docs/id/manage-claude/plugins-api#create-a-version) menampilkan objek lengkapnya). Field-fieldnya mencerminkan field versi yang disajikan pada plugin (`display_name`, `description`, `manifest_version`, `content_scan`, `components`, `reach`) untuk versi ini, ditambah `release_notes` (sebagaimana diberikan saat unggahan; ditampilkan di riwayat versi claude.ai) dan `created_by` (siapa yang mengunggahnya).

`{version}` yang tidak memiliki prefiks `pluginver_` mengembalikan `400` (kecuali literal `latest` jika disebutkan). Nilai yang memiliki prefiks tersebut tetapi tidak mengidentifikasi versi dari plugin itu mengembalikan `404`.

### Mencantumkan versi plugin

`GET /v1/organizations/plugins/{plugin_id}/versions` mencantumkan versi-versi plugin, diurutkan berdasarkan `created_at` secara menurun; item pertama adalah versi yang diidentifikasi oleh `latest_version_id`. `limit` bernilai 1 hingga 1.000. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/versions?limit=50" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins:versions list \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --limit 50
  ```

  ```python Python
  client = anthropic.Anthropic()

  versions = client.beta.organization.plugins.versions.list(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL", limit=50
  )

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for version in versions:
      print(f"{version.id}: {version.manifest_version}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const versions = await client.beta.organization.plugins.versions.list(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
    { limit: 50 }
  );

  for await (const version of versions) {
    console.log(`${version.id}: ${version.manifest_version}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Plugins.Versions.List(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      new() { Limit = 50 }
  );

  await foreach (var version in page.Paginate())
  {
      Console.WriteLine($"{version.ID}: {version.ManifestVersion}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  versions := client.Beta.Organization.Plugins.Versions.ListAutoPaging(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginVersionListParams{
  		Limit: anthropic.Int(50),
  	},
  )

  for versions.Next() {
  	version := versions.Current()
  	fmt.Printf("%s: %s\n", version.ID, version.ManifestVersion)
  }
  if err := versions.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.versions.VersionListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = VersionListParams.builder()
          .limit(50)
          .build();
      var versions = client.beta().organization().plugins().versions()
          .list("plugin_01Hq3vX8kZcN2mB7pR4tY9wL", params);

      for (var version : versions.autoPager()) {
          IO.println(version.id() + ": " + version.manifestVersion().orElse(null));
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $versions = $client->beta->organization->plugins->versions->list(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
      limit: 50,
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $versions->nextPage.
  foreach ($versions->getItems() as $version) {
      echo "{$version->id}: {$version->manifestVersion}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  page = client.beta.organization.plugins.versions.list(plugin_id, limit: 50)

  page.auto_paging_each do |version|
    puts "#{version.id}: #{version.manifest_version}"
  end
  ```
</CodeGroup>

### Membuat versi

`POST /v1/organizations/plugins/{plugin_id}/versions` menambahkan versi ke plugin milik organisasi di marketplace `manual`. Body berupa `multipart/form-data`, dengan field `files[]` dan `release_notes`, [persyaratan unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#upload-requirements), serta error file, manifest, arsip, dan ukuran yang sama seperti [Membuat plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api#create-a-plugin). Nama yang diunggah (`name` pada manifest) harus sama dengan `name` plugin. Jika plugin tidak disematkan, versi baru langsung disajikan begitu disimpan; jika disematkan, versi tersebut disimpan tetapi tidak disajikan sampai Anda mengubah versi yang disajikan ke versi itu. Untuk memeriksanya, bandingkan `id` pada respons dengan `served_version_id` plugin. Mengembalikan versi. Memerlukan scope `write:plugins`.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -F "files[]=@dist/sales-toolkit.zip" \
    -F "release_notes=Adds the call-prep command."
  ```

  ```bash CLI
  ant beta:organization:plugins:versions create \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --file dist/sales-toolkit.zip \
    --release-notes "Adds the call-prep command."
  ```

  ```python Python
  client = anthropic.Anthropic()

  with open("dist/sales-toolkit.zip", "rb") as archive:
      version = client.beta.organization.plugins.versions.create(
          "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
          files=[archive],
          release_notes="Adds the call-prep command.",
      )

  print(f"id: {version.id}")
  print(f"manifest_version: {version.manifest_version}")
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  const version = await client.beta.organization.plugins.versions.create(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
    {
      files: [fs.createReadStream("dist/sales-toolkit.zip")],
      release_notes: "Adds the call-prep command."
    }
  );

  console.log(`id: ${version.id}`);
  console.log(`manifest_version: ${version.manifest_version}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var version = await client.Beta.Organization.Plugins.Versions.Create(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      new()
      {
          Files = [File.OpenRead("dist/sales-toolkit.zip")],
          ReleaseNotes = "Adds the call-prep command.",
      }
  );

  Console.WriteLine($"id: {version.ID}");
  Console.WriteLine($"manifest_version: {version.ManifestVersion}");
  ```

  ```go Go
  client := anthropic.NewClient()

  archive, err := os.Open("dist/sales-toolkit.zip")
  if err != nil {
  	log.Fatal(err)
  }
  defer archive.Close()

  version, err := client.Beta.Organization.Plugins.Versions.New(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginVersionNewParams{
  		Files:        []io.Reader{archive},
  		ReleaseNotes: anthropic.String("Adds the call-prep command."),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", version.ID)
  fmt.Printf("manifest_version: %s\n", version.ManifestVersion)
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.organization.plugins.versions.VersionCreateParams;

  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Susun bagian `files[]` secara manual agar arsip dikirim beserta nama filenya,
      // yang diwajibkan oleh proses unggah.
      var archive = MultipartField.<List<InputStream>>builder()
          .value(List.of(Files.newInputStream(Path.of("dist/sales-toolkit.zip"))))
          .filename("sales-toolkit.zip")
          .contentType("application/octet-stream")
          .build();
      var params = VersionCreateParams.builder()
          .files(archive)
          .releaseNotes("Adds the call-prep command.")
          .build();
      var version = client.beta().organization().plugins().versions()
          .create("plugin_01Hq3vX8kZcN2mB7pR4tY9wL", params);

      IO.println("id: " + version.id());
      IO.println("manifest_version: " + version.manifestVersion().orElse(null));
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  $version = $client->beta->organization->plugins->versions->create(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
      files: [
          FileParam::fromResource(fopen('dist/sales-toolkit.zip', 'r')),
      ],
      releaseNotes: 'Adds the call-prep command.',
  );

  echo "id: {$version->id}\n";
  echo "manifest_version: {$version->manifestVersion}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  version = client.beta.organization.plugins.versions.create(
    plugin_id,
    files: [Pathname("dist/sales-toolkit.zip")],
    release_notes: "Adds the call-prep command."
  )

  puts "id: #{version.id}"
  puts "manifest_version: #{version.manifest_version}"
  ```
</CodeGroup>

```json
{
  "type": "plugin_version",
  "id": "pluginver_01Jd5sK2nQ8wE4rT6yU1iO3p",
  "plugin_id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  "display_name": "Sales Toolkit",
  "description": "Account research and call prep for the sales team.",
  "manifest_version": "1.5.0",
  "release_notes": "Adds the call-prep command.",
  "created_by": { "type": "api_actor", "api_key_id": "apikey_01Nq9vN6rT2zH7uW4bX5mR8s" },
  "content_scan": { "status": "processing", "assessment": null, "reason": null },
  "components": [
    {
      "type": "skill",
      "name": "account-research",
      "description": "Researches a customer account before a call."
    },
    { "type": "mcp_server", "name": "crm", "description": null },
    {
      "type": "command",
      "name": "call-prep",
      "description": "Builds a one-page brief for an upcoming call."
    }
  ],
  "reach": "remote",
  "created_at": "2026-09-15T14:12:30Z"
}
```

Selain `400` untuk unggahan yang melanggar [persyaratan unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#upload-requirements) (`413` untuk body permintaan lebih dari 200 MB) dan respons bersama (`403` untuk plugin milik anggota; lihat [Respons error](https://platform.claude.com/docs/id/manage-claude/plugins-api#error-responses)), permintaan dapat gagal dengan:

| Status                     | Penyebab                                                                                                                 | Yang harus dilakukan                                                                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400                        | Plugin berada di marketplace yang disinkronkan dari Git, atau nama yang diunggah berbeda dari nama plugin.               | Ubah repositorinya, atau perbaiki `name` pada manifest.                                                                                                                                            |
| 409 (tanpa `error_code`)   | Unggahan lain ke plugin ini, atau perubahan versi yang disajikan, masih berlangsung.                                     | Coba lagi sebentar lagi.                                                                                                                                                                           |
| 409 `skill_name_taken`     | Plugin berada di marketplace library dan versi tersebut menambahkan skill dengan nama yang sama dengan skill organisasi. | Ganti nama skill tersebut, atau hapus skill organisasi di claude.ai.                                                                                                                               |
| 503 `registration_pending` | Versi telah disimpan tetapi pendaftarannya belum selesai.                                                                | Kirim ulang permintaan yang sama jika respons menyertakan `x-should-retry: true` (lihat [Mencoba ulang unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#retrying-uploads)). |

### Mendapatkan versi

`GET /v1/organizations/plugins/{plugin_id}/versions/{version}` mengembalikan satu versi. `{version}` adalah ID versi, atau `latest` untuk versi yang diidentifikasi oleh `latest_version_id` pada saat permintaan. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/versions/latest" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins:versions retrieve \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --version latest
  ```

  ```python Python
  client = anthropic.Anthropic()

  version = client.beta.organization.plugins.versions.retrieve(
      "latest",
      plugin_id="plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  )

  print(f"id: {version.id}")
  print(f"manifest_version: {version.manifest_version}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const version = await client.beta.organization.plugins.versions.retrieve("latest", {
    plugin_id: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  });

  console.log(`id: ${version.id}`);
  console.log(`manifest_version: ${version.manifest_version}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var version = await client.Beta.Organization.Plugins.Versions.Retrieve(
      "latest",
      new() { PluginID = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL" }
  );

  Console.WriteLine($"id: {version.ID}");
  Console.WriteLine($"manifest_version: {version.ManifestVersion}");
  ```

  ```go Go
  client := anthropic.NewClient()

  version, err := client.Beta.Organization.Plugins.Versions.Get(
  	context.Background(),
  	"latest",
  	anthropic.BetaOrganizationPluginVersionGetParams{
  		PluginID: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", version.ID)
  fmt.Printf("manifest_version: %s\n", version.ManifestVersion)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.versions.VersionRetrieveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = VersionRetrieveParams.builder()
          .pluginId("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")
          .build();
      var version = client.beta().organization().plugins().versions()
          .retrieve("latest", params);

      IO.println("id: " + version.id());
      IO.println("manifest_version: " + version.manifestVersion().orElse(null));
  }
  ```

  ```php PHP
  $client = new Client();

  $version = $client->beta->organization->plugins->versions->retrieve(
      version: 'latest',
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
  );

  echo "id: {$version->id}\n";
  echo "manifest_version: {$version->manifestVersion}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  version = client.beta.organization.plugins.versions.retrieve("latest", plugin_id: plugin_id)

  puts "id: #{version.id}"
  puts "manifest_version: #{version.manifest_version}"
  ```
</CodeGroup>

### Mengunduh file versi

`GET /v1/organizations/plugins/{plugin_id}/versions/{version}/content` mengunduh file-file suatu versi sebagai arsip `.zip` yang tersimpan (`Content-Type: application/zip`). Arsip dikembalikan apa pun hasil pemindaian kontennya, sehingga Anda dapat memeriksa versi yang ditahan dari anggota. Arsip disajikan persis seperti yang disimpan, sehingga untuk plugin milik organisasi di marketplace `manual` Anda dapat mengunggahnya kembali tanpa perubahan sebagai versi baru, asalkan memenuhi persyaratan unggahan saat ini. `{version}` harus berupa ID versi, bukan `latest`: baca terlebih dahulu `served_version_id` atau `latest_version_id` plugin, atau resolusikan `latest` dengan `GET /v1/organizations/plugins/{plugin_id}/versions/latest`. Nama file pada `Content-Disposition` diturunkan dari nama plugin dan tidak unik; beri nama file yang disimpan berdasarkan ID plugin dan ID versi. Memerlukan scope `read:plugins`.

Mengunduh arsip plugin **milik anggota** mencatat event `claude_plugin_archive_accessed` pada Activity Feed Compliance API, yang mengidentifikasi kunci (sebagai `api_actor`), plugin dan marketplace-nya, versi, serta anggota pemilik berdasarkan ID; event ini tidak memuat nama. Mengunduh arsip plugin milik organisasi tidak mencatat apa pun.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/versions/pluginver_01Km7tL4pR9xF5sU2zV3jP6q/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -o plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip
  ```

  ```bash CLI
  ant beta:organization:plugins:versions download \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --version pluginver_01Km7tL4pR9xF5sU2zV3jP6q \
    --output plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip
  ```

  ```python Python
  client = anthropic.Anthropic()

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  version_id = "pluginver_01Km7tL4pR9xF5sU2zV3jP6q"

  with client.beta.organization.plugins.versions.with_streaming_response.download(
      version_id,
      plugin_id=plugin_id,
  ) as response:
      response.stream_to_file(f"{plugin_id}_{version_id}.zip")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();

  const pluginId = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL";
  const versionId = "pluginver_01Km7tL4pR9xF5sU2zV3jP6q";

  const response = await client.beta.organization.plugins.versions.download(versionId, {
    plugin_id: pluginId
  });
  if (!response.body) throw new Error("The download returned no body");

  await writeFile(`${pluginId}_${versionId}.zip`, response.body);
  ```

  ```csharp C#
  AnthropicClient client = new();

  using var response = await client.Beta.Organization.Plugins.Versions.Download(
      "pluginver_01Km7tL4pR9xF5sU2zV3jP6q",
      new() { PluginID = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL" }
  );

  using var content = await response.ReadAsStream();
  using var file = File.Create(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip"
  );
  await content.CopyToAsync(file);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Organization.Plugins.Versions.Download(
  	context.Background(),
  	"pluginver_01Km7tL4pR9xF5sU2zV3jP6q",
  	anthropic.BetaOrganizationPluginVersionDownloadParams{
  		PluginID: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }
  defer response.Body.Close()

  out, err := os.Create("plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip")
  if err != nil {
  	log.Fatal(err)
  }
  defer out.Close()

  if _, err := io.Copy(out, response.Body); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.core.http.HttpResponse;
  import com.anthropic.models.beta.organization.plugins.versions.VersionDownloadParams;

  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = VersionDownloadParams.builder()
          .pluginId("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")
          .build();
      try (HttpResponse response = client.beta().organization().plugins().versions()
              .download("pluginver_01Km7tL4pR9xF5sU2zV3jP6q", params)) {
          Files.copy(
              response.body(),
              Path.of("plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip"),
              StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  $client = new Client();

  // download() akan mengembalikan seluruh arsip sebagai satu string, jadi ambil
  // respons mentahnya dan salin body-nya ke disk secara bertahap (per chunk).
  $response = $client->beta->organization->plugins->versions->raw->download(
      version: 'pluginver_01Km7tL4pR9xF5sU2zV3jP6q',
      params: ['pluginID' => 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL'],
  );

  $archive = $response->getBody();
  $file = fopen('plugin_01Hq3vX8kZcN2mB7pR4tY9wL_pluginver_01Km7tL4pR9xF5sU2zV3jP6q.zip', 'wb');
  while (!$archive->eof()) {
      fwrite($file, $archive->read(1024 * 1024));
  }
  fclose($file);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  version_id = "pluginver_01Km7tL4pR9xF5sU2zV3jP6q"
  archive = client.beta.organization.plugins.versions.download(version_id, plugin_id: plugin_id)

  # SDK mengembalikan arsip yang sudah dibaca ke dalam memori, sebagai StringIO.
  File.binwrite("#{plugin_id}_#{version_id}.zip", archive.string)
  ```
</CodeGroup>

## Pengaturan instalasi plugin

Endpoint-endpoint ini berlaku untuk plugin milik organisasi. Endpoint ini mengembalikan `404` untuk plugin milik anggota, yang memiliki [pembagian](https://platform.claude.com/docs/id/manage-claude/plugins-api#plugin-shares) sebagai gantinya. `{target}` adalah literal `organization` untuk pengaturan tingkat organisasi plugin, atau ID `rbac_group_` suatu grup untuk pengaturan grup tersebut; nilai lain mengembalikan `400`. ID grup diperoleh dari `GET /v1/organizations/rbac_groups` (scope `read:rbac_groups`; lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management#groups)). Pengaturan tidak memiliki `id` sendiri: pengaturan dialamatkan dengan `(plugin_id, target)`, dan tidak ada aktor yang dicatat padanya (aktor tercatat pada event aktivitas `plugin_installation_preference_updated`).

### Mencantumkan pengaturan instalasi plugin

`GET /v1/organizations/plugins/{plugin_id}/installation_settings` mencantumkan pengaturan yang dimiliki plugin milik organisasi, diurutkan berdasarkan `created_at` secara menurun: pengaturan tingkat organisasinya sendiri (tidak ada selama plugin mewarisi default marketplace-nya) dan pengaturan setiap grup. Filter berdasarkan `target_type` (`organization` atau `rbac_group`). Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/installation_settings" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins:installation-settings list \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL
  ```

  ```python Python
  client = anthropic.Anthropic()

  settings = client.beta.organization.plugins.installation_settings.list(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  )

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for setting in settings:
      print(f"{setting.plugin_id}: {setting.installation_preference}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const settings = await client.beta.organization.plugins.installationSettings.list(
    "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  );

  for await (const setting of settings) {
    console.log(`${setting.plugin_id}: ${setting.installation_preference}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Plugins.InstallationSettings.List(
      "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  );

  await foreach (var setting in page.Paginate())
  {
      Console.WriteLine($"{setting.PluginID}: {setting.InstallationPreference.Raw()}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  settings := client.Beta.Organization.Plugins.InstallationSettings.ListAutoPaging(
  	context.Background(),
  	"plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	anthropic.BetaOrganizationPluginInstallationSettingListParams{},
  )

  for settings.Next() {
  	setting := settings.Current()
  	fmt.Printf("%s: %s\n", setting.PluginID, setting.InstallationPreference)
  }
  if err := settings.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var settings = client.beta().organization().plugins().installationSettings()
      .list("plugin_01Hq3vX8kZcN2mB7pR4tY9wL");

  for (var setting : settings.autoPager()) {
      IO.println(setting.pluginId() + ": " + setting.installationPreference().asString());
  }
  ```

  ```php PHP
  $client = new Client();

  $settings = $client->beta->organization->plugins->installationSettings->list(
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $settings->nextPage.
  foreach ($settings->getItems() as $setting) {
      echo "{$setting->pluginID}: {$setting->installationPreference}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  page = client.beta.organization.plugins.installation_settings.list(plugin_id)

  page.auto_paging_each do |setting|
    puts "#{setting.plugin_id}: #{setting.installation_preference}"
  end
  ```
</CodeGroup>

### Menetapkan pengaturan instalasi

`POST /v1/organizations/plugins/{plugin_id}/installation_settings/{target}` menetapkan pengaturan instalasi satu target untuk plugin milik organisasi, dengan membuatnya atau mengubah nilai yang sudah dimilikinya. Satu-satunya field pada body adalah `installation_preference` (`required`, `auto_install`, `available`, atau `not_available`), dan field ini wajib. Menetapkan nilai yang sudah dimiliki target tidak mengubah apa pun. Menetapkan target `organization` membuat plugin berhenti mewarisi default marketplace-nya (`organization_installation_preference_inherited` menjadi `false`), bahkan ketika nilainya sama dengan default; hal ini tidak dapat dibatalkan, karena pengaturan tingkat organisasi tidak dapat dihapus, sehingga plugin tidak lagi mengikuti perubahan default marketplace selanjutnya. Target grup harus berupa grup yang dapat dilihat organisasi Anda di `GET /v1/organizations/rbac_groups`, jika tidak permintaan mengembalikan `404`. Perubahan ini tidak mengubah `updated_at` plugin; perubahan dicatat di Activity Feed. Mengembalikan pengaturan. Memerlukan scope `write:plugins`.

Kirim penulisan pengaturan instalasi untuk suatu plugin satu per satu. Jika beberapa penulisan untuk plugin yang sama tiba bersamaan, server menanganinya satu per satu dan dapat menjawab sebagian di antaranya dengan `503` alih-alih menerapkannya. `503` tersebut menyertakan `x-should-retry: true`, dan penulisan tersebut aman untuk diulang: tunggu satu atau dua detik, lalu kirim lagi.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/installation_settings/rbac_group_01F3xQqQzXyWvUtSrQpOnMlK" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -d '{"installation_preference": "available"}'
  ```

  ```bash CLI
  ant beta:organization:plugins:installation-settings set \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --target rbac_group_01F3xQqQzXyWvUtSrQpOnMlK \
    --installation-preference available
  ```

  ```python Python
  client = anthropic.Anthropic()

  setting = client.beta.organization.plugins.installation_settings.set(
      "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
      plugin_id="plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      installation_preference="available",
  )

  print(f"plugin_id: {setting.plugin_id}")
  print(f"installation_preference: {setting.installation_preference}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const setting = await client.beta.organization.plugins.installationSettings.set(
    "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
    {
      plugin_id: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
      installation_preference: "available"
    }
  );

  console.log(`plugin_id: ${setting.plugin_id}`);
  console.log(`installation_preference: ${setting.installation_preference}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Plugins.InstallationSettings;

  AnthropicClient client = new();

  var setting = await client.Beta.Organization.Plugins.InstallationSettings.Set(
      "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
      new()
      {
          PluginID = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
          InstallationPreference = InstallationPreference.Available,
      }
  );

  Console.WriteLine($"plugin_id: {setting.PluginID}");
  Console.WriteLine($"installation_preference: {setting.InstallationPreference.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  setting, err := client.Beta.Organization.Plugins.InstallationSettings.Set(
  	context.Background(),
  	"rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
  	anthropic.BetaOrganizationPluginInstallationSettingSetParams{
  		PluginID:               "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  		InstallationPreference: anthropic.BetaOrganizationPluginInstallationSettingSetParamsInstallationPreferenceAvailable,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("plugin_id: %s\n", setting.PluginID)
  fmt.Printf("installation_preference: %s\n", setting.InstallationPreference)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.installationsettings.InstallationSettingSetParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InstallationSettingSetParams.builder()
          .pluginId("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")
          .installationPreference(InstallationSettingSetParams.InstallationPreference.AVAILABLE)
          .build();
      var setting = client.beta().organization().plugins().installationSettings()
          .set("rbac_group_01F3xQqQzXyWvUtSrQpOnMlK", params);

      IO.println("plugin_id: " + setting.pluginId());
      IO.println("installation_preference: " + setting.installationPreference().asString());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Plugins\InstallationSettings\InstallationSettingSetParams\InstallationPreference;
  // ...

  $client = new Client();

  $setting = $client->beta->organization->plugins->installationSettings->set(
      target: 'rbac_group_01F3xQqQzXyWvUtSrQpOnMlK',
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
      installationPreference: InstallationPreference::AVAILABLE,
  );

  echo "plugin_id: {$setting->pluginID}\n";
  echo "installation_preference: {$setting->installationPreference}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  group_id = "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK"
  setting = client.beta.organization.plugins.installation_settings.set(
    group_id,
    plugin_id: plugin_id,
    installation_preference: :available
  )

  puts "plugin_id: #{setting.plugin_id}"
  puts "installation_preference: #{setting.installation_preference}"
  ```
</CodeGroup>

```json
{
  "type": "plugin_installation_setting",
  "plugin_id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  "target": { "type": "rbac_group", "rbac_group_id": "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK" },
  "installation_preference": "available",
  "created_at": "2026-09-02T10:00:00Z",
  "updated_at": "2026-09-02T10:00:00Z"
}
```

### Menghapus pengaturan instalasi grup

`DELETE /v1/organizations/plugins/{plugin_id}/installation_settings/{target}` menghapus pengaturan satu grup untuk plugin milik organisasi. Anggota grup tersebut kembali menggunakan nilai tingkat organisasi, atau pengaturan dari grup lain tempat mereka bergabung. Pengaturan tingkat organisasi tidak dapat dihapus setelah ditetapkan, sama seperti di claude.ai (`{target}` bernilai `organization` mengembalikan `400`); ubah nilainya sebagai gantinya. Grup yang tidak memiliki pengaturan untuk plugin ini mengembalikan `404`. Respons menyertakan kunci komposit sebagai pengganti `id`. Memerlukan scope `write:plugins`.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/plugins/plugin_01Hq3vX8kZcN2mB7pR4tY9wL/installation_settings/rbac_group_01F3xQqQzXyWvUtSrQpOnMlK" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins:installation-settings remove \
    --plugin-id plugin_01Hq3vX8kZcN2mB7pR4tY9wL \
    --target rbac_group_01F3xQqQzXyWvUtSrQpOnMlK
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_setting = client.beta.organization.plugins.installation_settings.remove(
      "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
      plugin_id="plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  )

  print(f"plugin_id: {removed_setting.plugin_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedSetting = await client.beta.organization.plugins.installationSettings.remove(
    "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
    { plugin_id: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL" }
  );

  console.log(`plugin_id: ${removedSetting.plugin_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedSetting = await client.Beta.Organization.Plugins.InstallationSettings.Remove(
      "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
      new() { PluginID = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL" }
  );

  Console.WriteLine($"plugin_id: {removedSetting.PluginID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedSetting, err := client.Beta.Organization.Plugins.InstallationSettings.Remove(
  	context.Background(),
  	"rbac_group_01F3xQqQzXyWvUtSrQpOnMlK",
  	anthropic.BetaOrganizationPluginInstallationSettingRemoveParams{
  		PluginID: "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("plugin_id: %s\n", removedSetting.PluginID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.plugins.installationsettings.InstallationSettingRemoveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InstallationSettingRemoveParams.builder()
          .pluginId("plugin_01Hq3vX8kZcN2mB7pR4tY9wL")
          .build();
      var removedSetting = client.beta().organization().plugins().installationSettings()
          .remove("rbac_group_01F3xQqQzXyWvUtSrQpOnMlK", params);

      IO.println("plugin_id: " + removedSetting.pluginId());
  }
  ```

  ```php PHP
  $client = new Client();

  $removedSetting = $client->beta->organization->plugins->installationSettings->remove(
      target: 'rbac_group_01F3xQqQzXyWvUtSrQpOnMlK',
      pluginID: 'plugin_01Hq3vX8kZcN2mB7pR4tY9wL',
  );

  echo "plugin_id: {$removedSetting->pluginID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
  group_id = "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK"
  removed_setting = client.beta.organization.plugins.installation_settings.remove(
    group_id,
    plugin_id: plugin_id
  )

  puts "plugin_id: #{removed_setting.plugin_id}"
  ```
</CodeGroup>

```json
{
  "type": "plugin_installation_setting_deleted",
  "plugin_id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL",
  "target": { "type": "rbac_group", "rbac_group_id": "rbac_group_01F3xQqQzXyWvUtSrQpOnMlK" }
}
```

## Pembagian plugin

Pembagian ("share") hanya ada pada plugin milik anggota dan bersifat hanya-baca di API ini (lihat [Pembagian](https://platform.claude.com/docs/id/manage-claude/plugins-api#shares)).

### Mencantumkan pembagian plugin

`GET /v1/organizations/plugins/{plugin_id}/shares` mencantumkan pihak-pihak yang telah diberi akses oleh pemilik plugin milik anggota, diurutkan berdasarkan `granted_at` secara menurun: setiap anggota (`organization`), sebuah grup (`rbac_group`), atau anggota tertentu (`organization_member`). Filter berdasarkan `target_type`. Plugin yang belum dibagikan oleh pemiliknya mengembalikan daftar kosong; plugin milik organisasi mengembalikan `404`. Pembagian bersifat hanya-baca di API ini, dan pembagian yang tercantum hanya memberikan akses selama jenis pembagian tersebut diaktifkan untuk organisasi Anda di claude.ai (lihat [Pembagian](https://platform.claude.com/docs/id/manage-claude/plugins-api#shares)). `granted_at` adalah waktu pembagian diberikan; jika pemilik kemudian mengubah pembagian tersebut di claude.ai, nilainya adalah waktu perubahan itu. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugins/plugin_01Mr2wP7sU3aJ8vX5cY6nS9t/shares" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugins:shares list \
    --plugin-id plugin_01Mr2wP7sU3aJ8vX5cY6nS9t
  ```

  ```python Python
  client = anthropic.Anthropic()

  shares = client.beta.organization.plugins.shares.list("plugin_01Mr2wP7sU3aJ8vX5cY6nS9t")

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for share in shares:
      print(f"plugin_id: {share.plugin_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const shares = await client.beta.organization.plugins.shares.list(
    "plugin_01Mr2wP7sU3aJ8vX5cY6nS9t"
  );

  for await (const share of shares) {
    console.log(`plugin_id: ${share.plugin_id}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Plugins.Shares.List("plugin_01Mr2wP7sU3aJ8vX5cY6nS9t");

  await foreach (var share in page.Paginate())
  {
      Console.WriteLine($"plugin_id: {share.PluginID}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  shares := client.Beta.Organization.Plugins.Shares.ListAutoPaging(
  	context.Background(),
  	"plugin_01Mr2wP7sU3aJ8vX5cY6nS9t",
  	anthropic.BetaOrganizationPluginShareListParams{},
  )

  for shares.Next() {
  	share := shares.Current()
  	fmt.Printf("plugin_id: %s\n", share.PluginID)
  }
  if err := shares.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var shares = client.beta().organization().plugins().shares()
      .list("plugin_01Mr2wP7sU3aJ8vX5cY6nS9t");

  for (var share : shares.autoPager()) {
      IO.println("plugin_id: " + share.pluginId());
  }
  ```

  ```php PHP
  $client = new Client();

  $shares = $client->beta->organization->plugins->shares->list(
      pluginID: 'plugin_01Mr2wP7sU3aJ8vX5cY6nS9t',
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $shares->nextPage.
  foreach ($shares->getItems() as $share) {
      echo "plugin_id: {$share->pluginID}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  plugin_id = "plugin_01Mr2wP7sU3aJ8vX5cY6nS9t"
  page = client.beta.organization.plugins.shares.list(plugin_id)

  page.auto_paging_each do |share|
    puts "plugin_id: #{share.plugin_id}"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "plugin_share",
      "plugin_id": "plugin_01Mr2wP7sU3aJ8vX5cY6nS9t",
      "target": { "type": "organization_member", "user_id": "user_01WCz9BvGLdMYRUMmcAxMWvW" },
      "granted_at": "2026-08-20T15:12:00Z"
    }
  ],
  "next_page": null
}
```

## Marketplace plugin

API ini membaca [marketplace](https://platform.claude.com/docs/id/manage-claude/plugins-api#marketplaces) dan menetapkan pengaturan instalasi default marketplace organisasi; marketplace itu sendiri dibuat, dihubungkan ke repositori, dan dihapus di claude.ai.

```json
{
  "type": "plugin_marketplace",
  "id": "marketplace_01VbNcMxZaSdFgHjKlQwErTy",
  "name": "engineering-tools",
  "owner": { "type": "organization" },
  "source": "github",
  "sync_status": "success",
  "last_sync_ended_at": "2026-09-10T22:15:03Z",
  "last_sync_read_sha": "9fceb02d0ae598e95dc970b74767f19372d61af8",
  "default_installation_preference": "available",
  "created_at": "2026-06-12T08:45:00Z"
}
```

| Field                             | Deskripsi                                                                                                                                                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                            | Nama marketplace. Tetap sepanjang masa hidupnya.                                                                                                                                                                                                     |
| `owner`                           | Bentuknya sama seperti pada plugin.                                                                                                                                                                                                                  |
| `source`                          | `manual`, `github`, `gitlab`, atau `public_git`. Lihat [Marketplace](https://platform.claude.com/docs/id/manage-claude/plugins-api#marketplaces).                                                                                                    |
| `sync_status`                     | Hasil sinkronisasi terbaru: `success`, `in_progress`, `failed_content`, `failed_transient`, `failed_auth`, atau `failed_limits`. `null` sampai sinkronisasi pertama kali dicoba, yang tidak pernah terjadi untuk marketplace dengan sumber `manual`. |
| `last_sync_ended_at`              | Waktu selesainya upaya sinkronisasi terbaru, apa pun hasilnya; untuk repositori terhubung yang belum pernah disinkronkan, waktu marketplace dibuat. `null` untuk marketplace yang tidak disinkronkan.                                                |
| `last_sync_read_sha`              | Commit yang dibaca dari repositori pada sinkronisasi terakhir. Belum tentu commit asal versi-versi yang disajikan. `null` untuk marketplace yang tidak disinkronkan.                                                                                 |
| `default_installation_preference` | Marketplace organisasi: nilai tingkat organisasi untuk setiap plugin di dalamnya yang tidak memiliki pengaturan sendiri (`not_available` jika belum pernah ditetapkan). Marketplace pribadi: `null`.                                                 |

`marketplace_id` yang tidak memiliki prefiks `marketplace_` mengembalikan `400`. Nilai yang memiliki prefiks tersebut tetapi tidak dapat diresolusikan, atau milik organisasi lain, mengembalikan `404`.

### Mencantumkan marketplace

`GET /v1/organizations/plugin_marketplaces` mencantumkan marketplace organisasi Anda dan marketplace pribadi anggota, diurutkan berdasarkan `created_at` secara menurun. Gunakan endpoint ini untuk menemukan ID marketplace, untuk memfilter daftar plugin berdasarkan marketplace tersebut atau untuk mengunggah ke dalamnya, sebelum marketplace itu berisi plugin apa pun. Marketplace library muncul setelah sesuatu pertama kali dibuat di dalamnya, di claude.ai atau melalui API ini. Filter berdasarkan `owner_type` (`organization` atau `user`) dan `source`. `limit` bernilai 1 hingga 1.000. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugin_marketplaces?owner_type=organization" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugin-marketplaces list --owner-type organization
  ```

  ```python Python
  client = anthropic.Anthropic()

  marketplaces = client.beta.organization.plugin_marketplaces.list(
      owner_type="organization"
  )

  # Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
  for marketplace in marketplaces:
      print(f"{marketplace.id}: {marketplace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const marketplaces = await client.beta.organization.pluginMarketplaces.list({
    owner_type: "organization"
  });

  for await (const marketplace of marketplaces) {
    console.log(`${marketplace.id}: ${marketplace.name}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.PluginMarketplaces;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.PluginMarketplaces.List(
      new() { OwnerType = OwnerType.Organization }
  );

  await foreach (var marketplace in page.Paginate())
  {
      Console.WriteLine($"{marketplace.ID}: {marketplace.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  marketplaces := client.Beta.Organization.PluginMarketplaces.ListAutoPaging(
  	context.Background(),
  	anthropic.BetaOrganizationPluginMarketplaceListParams{
  		OwnerType: anthropic.BetaOrganizationPluginMarketplaceListParamsOwnerTypeOrganization,
  	},
  )

  for marketplaces.Next() {
  	marketplace := marketplaces.Current()
  	fmt.Printf("%s: %s\n", marketplace.ID, marketplace.Name)
  }
  if err := marketplaces.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.pluginmarketplaces.PluginMarketplaceListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginMarketplaceListParams.builder()
          .ownerType(PluginMarketplaceListParams.OwnerType.ORGANIZATION)
          .build();
      var marketplaces = client.beta().organization().pluginMarketplaces().list(params);

      for (var marketplace : marketplaces.autoPager()) {
          IO.println(marketplace.id() + ": " + marketplace.name());
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\PluginMarketplaces\PluginMarketplaceListParams\OwnerType;
  // ...

  $client = new Client();

  $marketplaces = $client->beta->organization->pluginMarketplaces->list(
      ownerType: OwnerType::ORGANIZATION,
  );

  // Hanya halaman ini; untuk halaman berikutnya, panggil list() lagi dengan page: $marketplaces->nextPage.
  foreach ($marketplaces->getItems() as $marketplace) {
      echo "{$marketplace->id}: {$marketplace->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.plugin_marketplaces.list(owner_type: :organization)

  page.auto_paging_each do |marketplace|
    puts "#{marketplace.id}: #{marketplace.name}"
  end
  ```
</CodeGroup>

### Mendapatkan marketplace

`GET /v1/organizations/plugin_marketplaces/{marketplace_id}` mengembalikan satu marketplace. Memerlukan scope `read:plugins`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/plugin_marketplaces/marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01"
  ```

  ```bash CLI
  ant beta:organization:plugin-marketplaces retrieve \
    --marketplace-id marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r
  ```

  ```python Python
  client = anthropic.Anthropic()

  marketplace = client.beta.organization.plugin_marketplaces.retrieve(
      "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  )

  print(f"id: {marketplace.id}")
  print(f"name: {marketplace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const marketplace = await client.beta.organization.pluginMarketplaces.retrieve(
    "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  );

  console.log(`id: ${marketplace.id}`);
  console.log(`name: ${marketplace.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var marketplace = await client.Beta.Organization.PluginMarketplaces.Retrieve(
      "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  );

  Console.WriteLine($"id: {marketplace.ID}");
  Console.WriteLine($"name: {marketplace.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  marketplace, err := client.Beta.Organization.PluginMarketplaces.Get(
  	context.Background(),
  	"marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
  	anthropic.BetaOrganizationPluginMarketplaceGetParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", marketplace.ID)
  fmt.Printf("name: %s\n", marketplace.Name)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var marketplace = client.beta().organization().pluginMarketplaces()
      .retrieve("marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r");

  IO.println("id: " + marketplace.id());
  IO.println("name: " + marketplace.name());
  ```

  ```php PHP
  $client = new Client();

  $marketplace = $client->beta->organization->pluginMarketplaces->retrieve(
      marketplaceID: 'marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r',
  );

  echo "id: {$marketplace->id}\n";
  echo "name: {$marketplace->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  marketplace_id = "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  marketplace = client.beta.organization.plugin_marketplaces.retrieve(marketplace_id)

  puts "id: #{marketplace.id}"
  puts "name: #{marketplace.name}"
  ```
</CodeGroup>

### Menetapkan pengaturan instalasi default marketplace

`POST /v1/organizations/plugin_marketplaces/{marketplace_id}` menetapkan pengaturan instalasi default dari marketplace milik organisasi. Setiap plugin di marketplace yang tidak memiliki pengaturan tingkat organisasinya sendiri melaporkan default ini sebagai `organization_installation_preference`-nya, termasuk plugin yang ditambahkan kemudian. Endpoint ini berfungsi untuk marketplace `manual` maupun yang disinkronkan; marketplace pribadi milik anggota mengembalikan `403`. Satu-satunya field yang dapat diperbarui adalah `default_installation_preference`, dan field ini wajib. Nilainya tidak dapat dikembalikan ke `null`: setelah marketplace memiliki default, marketplace tersebut akan tetap memilikinya, seperti di claude.ai. Perubahan dicatat sebagai satu event `marketplace_updated` tanpa event per plugin, dan tidak mengubah `updated_at` plugin mana pun. Menetapkan nilai yang sudah ditetapkan tidak mengubah apa pun, dengan satu pengecualian: marketplace yang default-nya belum pernah ditetapkan melaporkan `not_available` tetapi tidak memiliki pengaturan, sehingga penulisan pertamanya (bahkan `not_available`) dihitung sebagai perubahan. Mengembalikan marketplace. Memerlukan scope `write:plugins`.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugin_marketplaces/marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -d '{"default_installation_preference": "available"}'
  ```

  ```bash CLI
  ant beta:organization:plugin-marketplaces update \
    --marketplace-id marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r \
    --default-installation-preference available
  ```

  ```python Python
  client = anthropic.Anthropic()

  marketplace = client.beta.organization.plugin_marketplaces.update(
      "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
      default_installation_preference="available",
  )

  print(f"id: {marketplace.id}")
  print(f"default_installation_preference: {marketplace.default_installation_preference}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const marketplace = await client.beta.organization.pluginMarketplaces.update(
    "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
    { default_installation_preference: "available" }
  );

  console.log(`id: ${marketplace.id}`);
  console.log(`default_installation_preference: ${marketplace.default_installation_preference}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.PluginMarketplaces;

  AnthropicClient client = new();

  var marketplace = await client.Beta.Organization.PluginMarketplaces.Update(
      "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
      new() { DefaultInstallationPreference = DefaultInstallationPreference.Available }
  );

  Console.WriteLine($"id: {marketplace.ID}");
  Console.WriteLine(
      $"default_installation_preference: {marketplace.DefaultInstallationPreference?.Raw()}"
  );
  ```

  ```go Go
  client := anthropic.NewClient()

  marketplace, err := client.Beta.Organization.PluginMarketplaces.Update(
  	context.Background(),
  	"marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r",
  	anthropic.BetaOrganizationPluginMarketplaceUpdateParams{
  		DefaultInstallationPreference: anthropic.BetaOrganizationPluginMarketplaceUpdateParamsDefaultInstallationPreferenceAvailable,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", marketplace.ID)
  fmt.Printf("default_installation_preference: %s\n", marketplace.DefaultInstallationPreference)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.pluginmarketplaces.PluginMarketplaceUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginMarketplaceUpdateParams.builder()
          .defaultInstallationPreference(PluginMarketplaceUpdateParams.DefaultInstallationPreference.AVAILABLE)
          .build();
      var marketplace = client.beta().organization().pluginMarketplaces()
          .update("marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r", params);

      IO.println("id: " + marketplace.id());
      IO.println("default_installation_preference: "
          + marketplace.defaultInstallationPreference().map(preference -> preference.asString()).orElse(null));
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\PluginMarketplaces\PluginMarketplaceUpdateParams\DefaultInstallationPreference;
  // ...

  $client = new Client();

  $marketplace = $client->beta->organization->pluginMarketplaces->update(
      marketplaceID: 'marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r',
      defaultInstallationPreference: DefaultInstallationPreference::AVAILABLE,
  );

  echo "id: {$marketplace->id}\n";
  echo "default_installation_preference: {$marketplace->defaultInstallationPreference}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  marketplace_id = "marketplace_01Lp8uM5qS1yG6tV3aW4kQ7r"
  marketplace = client.beta.organization.plugin_marketplaces.update(
    marketplace_id,
    default_installation_preference: :available
  )

  puts "id: #{marketplace.id}"
  puts "default_installation_preference: #{marketplace.default_installation_preference}"
  ```
</CodeGroup>

### Memvalidasi konten marketplace

Dua endpoint melaporkan apa yang akan dilakukan sinkronisasi terhadap konten marketplace yang diberikan, tanpa menghubungkan atau menyimpan apa pun: `POST /v1/organizations/plugin_marketplaces/validate_repository` membaca repositori GitHub publik, dan `POST /v1/organizations/plugin_marketplaces/validate_archive` membaca `.zip` dari direktori marketplace yang Anda unggah. Keduanya mengembalikan laporan yang sama: apakah `marketplace.json` terbentuk dengan benar, plugin mana yang akan dilewati dan alasannya, serta plugin mana yang akan disinkronkan dengan sebagian kontennya tidak disertakan. Pemeriksaan yang dilakukan sama dengan yang dijalankan oleh sinkronisasi sebenarnya. Masalah pada konten dikembalikan dalam laporan, bukan sebagai error HTTP: permintaan berhasil dengan `valid: false`, bahkan ketika repositori atau arsip sama sekali tidak dapat dibaca. Validasi dihitung sebagai pembacaan, dan kedua endpoint tersebut secara bersama-sama juga dibatasi hingga 10 validasi per menit per organisasi (lihat [Pembatasan laju](https://platform.claude.com/docs/id/manage-claude/plugins-api#rate-limiting)); keduanya tidak mencatat apa pun di Activity Feed. Validasi dapat memakan waktu hingga 120 detik sebelum kembali, jadi atur timeout klien Anda di atas nilai tersebut. Kedua endpoint memerlukan scope `read:plugins` atau `write:plugins` (`read:org_audit` dan `read:compliance_org_data` tidak memberikan akses tersebut).

Repositori, dan sumber plugin apa pun di luarnya yang berada di GitHub, dibaca secara anonim, sehingga repositori privat atau sumber plugin privat dilaporkan sebagai tidak ditemukan. Sumber plugin di host selain GitHub tidak diambil; plugin semacam itu biasanya mendapat peringatan `marketplace_validate_source_not_checked` dan diperiksa saat marketplace benar-benar disinkronkan. Jika repositori tersebut adalah, atau arsip tersebut menyebutkan, marketplace yang disinkronkan Anthropic ke setiap organisasi, aturan yang lebih ketat berlaku: setiap sumber plugin di luar marketplace harus disematkan ke SHA commit lengkap, sumber yang tidak disematkan atau berada di host yang tidak didukung dilaporkan sebagai error plugin, dan branch yang dibaca secara default adalah branch yang menjadi sumber sinkronisasi marketplace tersebut.

`validate_repository` menerima body JSON dengan dua field: `repository_url`, URL `https://` dari repositori publik di github.com (wajib), dan `ref`, nama branch atau SHA commit lengkap 40 karakter (opsional; jika dihilangkan atau `null`, digunakan branch yang akan dibaca oleh sinkronisasi, biasanya branch default repositori). `validate_archive` menerima `multipart/form-data` dengan tepat satu part, `archive`, yang dikirim sebagai part file dengan nama file: `.zip` dari direktori marketplace, maksimal 32 MB, dengan isinya berada di root atau dibungkus dalam satu folder (seperti yang dihasilkan oleh unduhan dari host Git), hanya dengan kompresi DEFLATE atau STORE. Tidak ada field formulir lain yang diterima.

Memvalidasi repositori publik pada suatu branch:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugin_marketplaces/validate_repository" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -d '{"repository_url": "https://github.com/example-org/claude-plugins", "ref": "release-candidate"}'
  ```

  ```bash CLI
  ant beta:organization:plugin-marketplaces validate-repository \
    --repository-url https://github.com/example-org/claude-plugins \
    --ref release-candidate
  ```

  ```python Python
  client = anthropic.Anthropic()

  report = client.beta.organization.plugin_marketplaces.validate_repository(
      repository_url="https://github.com/example-org/claude-plugins",
      ref="release-candidate",
  )

  print(f"valid: {str(report.valid).lower()}")
  print(f"total_plugin_count: {report.total_plugin_count}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const report = await client.beta.organization.pluginMarketplaces.validateRepository({
    repository_url: "https://github.com/example-org/claude-plugins",
    ref: "release-candidate"
  });

  console.log(`valid: ${report.valid}`);
  console.log(`total_plugin_count: ${report.total_plugin_count}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var report = await client.Beta.Organization.PluginMarketplaces.ValidateRepository(
      new()
      {
          RepositoryUrl = "https://github.com/example-org/claude-plugins",
          Ref = "release-candidate",
      }
  );

  Console.WriteLine($"valid: {report.Valid.ToString().ToLowerInvariant()}");
  Console.WriteLine($"total_plugin_count: {report.TotalPluginCount}");
  ```

  ```go Go
  client := anthropic.NewClient()

  report, err := client.Beta.Organization.PluginMarketplaces.ValidateRepository(
  	context.Background(),
  	anthropic.BetaOrganizationPluginMarketplaceValidateRepositoryParams{
  		RepositoryURL: "https://github.com/example-org/claude-plugins",
  		Ref:           anthropic.String("release-candidate"),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("valid: %t\n", report.Valid)
  fmt.Printf("total_plugin_count: %d\n", report.TotalPluginCount)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.pluginmarketplaces.PluginMarketplaceValidateRepositoryParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PluginMarketplaceValidateRepositoryParams.builder()
          .repositoryUrl("https://github.com/example-org/claude-plugins")
          .ref("release-candidate")
          .build();
      var report = client.beta().organization().pluginMarketplaces().validateRepository(params);

      IO.println("valid: " + report.valid());
      IO.println("total_plugin_count: " + report.totalPluginCount());
  }
  ```

  ```php PHP
  $client = new Client();

  $report = $client->beta->organization->pluginMarketplaces->validateRepository(
      repositoryURL: 'https://github.com/example-org/claude-plugins',
      ref: 'release-candidate',
  );

  echo 'valid: ' . ($report->valid ? 'true' : 'false') . "\n";
  echo "total_plugin_count: {$report->totalPluginCount}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  report = client.beta.organization.plugin_marketplaces.validate_repository(
    repository_url: "https://github.com/example-org/claude-plugins",
    ref: "release-candidate"
  )

  puts "valid: #{report.valid}"
  puts "total_plugin_count: #{report.total_plugin_count}"
  ```
</CodeGroup>

```json
{
  "type": "plugin_marketplace_validation_report",
  "valid": false,
  "ref": "release-candidate",
  "commit_sha": "9fceb02d0ae598e95dc970b74767f19372d61af8",
  "total_plugin_count": 3,
  "manifest_error": null,
  "manifest_error_code": null,
  "plugin_errors": [
    {
      "name": "deploy-helper",
      "error": "The plugin has a top-level bin/ directory.",
      "error_code": "marketplace_sync_bin_directory_not_allowed"
    }
  ],
  "plugin_warnings": [
    {
      "name": "release-notes",
      "warnings": [
        {
          "message": "plugin.json has unrecognized top-level keys: owners",
          "error_code": "marketplace_sync_plugin_unrecognized_keys"
        }
      ]
    }
  ]
}
```

| Field                                   | Deskripsi                                                                                                                                                                                                                                                              |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `valid`                                 | `true` ketika `marketplace.json` terbentuk dengan benar dan tidak ada plugin yang akan dilewati. Peringatan tidak membuatnya bernilai `false`.                                                                                                                         |
| `ref`                                   | Branch yang dibaca, berdasarkan nama; `null` ketika tidak ada branch yang disebutkan dan branch default yang dibaca, untuk SHA commit, atau untuk arsip.                                                                                                               |
| `commit_sha`                            | Commit yang divalidasi. Untuk arsip yang diunduh dari host Git, commit yang dicatat host di field komentar file ZIP, jika ada (tidak diverifikasi).                                                                                                                    |
| `total_plugin_count`                    | Jumlah plugin yang dideklarasikan `marketplace.json`; `0` jika file tersebut tidak dapat dibaca.                                                                                                                                                                       |
| `manifest_error`, `manifest_error_code` | Diisi ketika tidak ada yang dapat divalidasi: sumber tidak dapat dibaca, atau `marketplace.json` tidak ada, salah format, atau melebihi batas. Validasi yang tidak selesai dalam 120 detik melaporkan `manifest_error_code: "marketplace_validate_deadline_exceeded"`. |
| `plugin_errors`                         | Satu `{name, error, error_code}` per plugin yang akan dilewati oleh sinkronisasi.                                                                                                                                                                                      |
| `plugin_warnings`                       | Satu `{name, warnings: [{message, error_code}]}` per plugin yang akan disinkronkan dengan sebagian kontennya tidak disertakan.                                                                                                                                         |

Sebagai alternatif, validasi salinan lokal direktori marketplace sebagai `.zip`; responsnya berupa laporan yang sama:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/plugin_marketplaces/validate_archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: ce-plugins-2026-09-01" \
    -F "archive=@marketplace.zip"
  ```

  ```bash CLI
  ant beta:organization:plugin-marketplaces validate-archive \
    --archive marketplace.zip
  ```

  ```python Python
  client = anthropic.Anthropic()

  with open("marketplace.zip", "rb") as archive:
      report = client.beta.organization.plugin_marketplaces.validate_archive(
          archive=archive
      )

  print(f"valid: {str(report.valid).lower()}")
  print(f"total_plugin_count: {report.total_plugin_count}")
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  const report = await client.beta.organization.pluginMarketplaces.validateArchive({
    archive: fs.createReadStream("marketplace.zip")
  });

  console.log(`valid: ${report.valid}`);
  console.log(`total_plugin_count: ${report.total_plugin_count}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var report = await client.Beta.Organization.PluginMarketplaces.ValidateArchive(
      new() { Archive = File.OpenRead("marketplace.zip") }
  );

  Console.WriteLine($"valid: {report.Valid.ToString().ToLowerInvariant()}");
  Console.WriteLine($"total_plugin_count: {report.TotalPluginCount}");
  ```

  ```go Go
  client := anthropic.NewClient()

  archive, err := os.Open("marketplace.zip")
  if err != nil {
  	log.Fatal(err)
  }
  defer archive.Close()

  report, err := client.Beta.Organization.PluginMarketplaces.ValidateArchive(
  	context.Background(),
  	anthropic.BetaOrganizationPluginMarketplaceValidateArchiveParams{
  		Archive: archive,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("valid: %t\n", report.Valid)
  fmt.Printf("total_plugin_count: %d\n", report.TotalPluginCount)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.pluginmarketplaces.PluginMarketplaceValidateArchiveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Teruskan sebuah Path agar bagian `archive` dikirim beserta nama file, yang diwajibkan oleh endpoint ini.
      var params = PluginMarketplaceValidateArchiveParams.builder()
          .archive(Path.of("marketplace.zip"))
          .build();
      var report = client.beta().organization().pluginMarketplaces().validateArchive(params);

      IO.println("valid: " + report.valid());
      IO.println("total_plugin_count: " + report.totalPluginCount());
  }
  ```

  ```php PHP
  use Anthropic\Core\FileParam;

  $client = new Client();

  $report = $client->beta->organization->pluginMarketplaces->validateArchive(
      archive: FileParam::fromResource(fopen('marketplace.zip', 'r')),
  );

  echo 'valid: ' . ($report->valid ? 'true' : 'false') . "\n";
  echo "total_plugin_count: {$report->totalPluginCount}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  report = client.beta.organization.plugin_marketplaces.validate_archive(
    archive: Pathname("marketplace.zip")
  )

  puts "valid: #{report.valid}"
  puts "total_plugin_count: #{report.total_plugin_count}"
  ```
</CodeGroup>

Masalah pada konten tidak pernah membuat permintaan gagal. Selain respons yang dimiliki bersama oleh setiap endpoint (`403` untuk kunci yang hanya memiliki `read:org_audit` atau `read:compliance_org_data`; lihat [Respons error](https://platform.claude.com/docs/id/manage-claude/plugins-api#error-responses) dan [Pembatasan laju](https://platform.claude.com/docs/id/manage-claude/plugins-api#rate-limiting)), permintaan itu sendiri dapat gagal dengan:

| Status | Penyebab                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Yang harus dilakukan                                                   |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 400    | Pada `validate_repository`: body bukan objek JSON; `repository_url` tidak ada, lebih panjang dari 2.048 karakter, memuat kredensial, atau tidak berbentuk `https://github.com/{owner}/{repo}` (sufiks `.git` diterima; host lain, path yang lebih panjang seperti `/tree/main` dari halaman branch, atau port selain 443 atau 80 tidak diterima); `ref` kosong, lebih panjang dari 255 karakter, mengandung `..`, atau mengandung karakter selain huruf ASCII, angka, `.`, `_`, `-`, `+`, dan `/`; atau terdapat field lain. `ref` yang lolos pemeriksaan ini tetapi menyebutkan branch yang tidak dimiliki repositori tidak ditolak: permintaan berhasil dengan `valid: false` dan `manifest_error` menyatakan bahwa branch tidak ditemukan. Pada `validate_archive`: body bukan `multipart/form-data`, part `archive` tidak ada, berulang, atau tidak dikirim sebagai part file dengan nama file, atau terdapat field formulir lain. | Perbaiki permintaan dan kirim ulang.                                   |
| 413    | Pada `validate_archive`: part `archive`, atau panjang body yang dideklarasikan pada permintaan, melebihi 32 MB.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Validasi repositori melalui URL sebagai gantinya, atau perkecil arsip. |

#### Kode laporan

Setiap temuan dalam laporan memiliki kode yang stabil: `manifest_error_code` ketika tidak ada yang dapat divalidasi, `error_code` pada setiap entri `plugin_errors`, dan `error_code` pada setiap peringatan. Ketika sebuah plugin memiliki beberapa masalah, `error_code` adalah kode masalah pertama dan `error` menggabungkan pesan-pesannya. Kode baru dapat ditambahkan; `manifest_error_code` yang tidak dikenali tetap berarti konten tidak dapat divalidasi, kode yang tidak dikenali pada entri `plugin_errors` tetap berarti plugin akan dilewati, dan kode yang tidak dikenali pada peringatan tetap berarti plugin akan disinkronkan. Kode-kode berikut menunjukkan kondisi sementara, sehingga permintaan yang sama mungkin berhasil nanti: `marketplace_host_rate_limited`, `marketplace_host_server_error`, `marketplace_host_timeout`, `marketplace_host_unreachable`, `marketplace_repo_access_denied`, `marketplace_sync_transient_fetch_budget_exhausted`, `marketplace_validate_network_error`, dan biasanya `marketplace_validate_deadline_exceeded`.

## Nilai yang tidak dikenali

Setiap nilai string di halaman ini (tipe komponen, `reach`, field pemindaian, `source` marketplace, kode error) dapat memperoleh nilai baru kapan saja. Perlakukan nilai yang tidak Anda kenali seperti string tak dikenal lainnya, alih-alih membuat proses gagal.

## Pembatasan laju

Permintaan baca (setiap endpoint `GET` di halaman ini) berbagi "rate limit" (batas laju) sebesar **300 permintaan per menit** per organisasi, dan permintaan tulis (membuat plugin atau versi, mengubah versi yang disajikan, menghapus, menetapkan atau menghapus pengaturan instalasi, dan memperbarui marketplace) berbagi batas sebesar **60 permintaan per menit** per organisasi. Validasi marketplace (endpoint mana pun) dihitung sebagai pembacaan, dan validasi juga dibatasi hingga 10 per menit per organisasi untuk kedua endpoint secara gabungan; kedua batas diperiksa sebelum body permintaan dibaca. Batas-batas ini dihitung untuk semua kunci organisasi Anda dan terpisah dari batas Admin API lainnya milik organisasi Anda. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests** dengan header `retry-after`. Respons menyertakan header `anthropic-ratelimit-requests-*` untuk batas yang berlaku (pada validasi marketplace, batas 10 per menitnya; pada `429`, batas mana pun yang menolak permintaan).

Unggahan, perubahan versi yang disajikan, atau validasi juga dapat mengembalikan `429` dengan `retry-after` ketika layanan untuk sementara tidak memiliki kapasitas untuk permintaan lain, dan unggahan mengembalikan `429` ketika organisasi Anda telah melampaui laju pemindaian kontennya. Tangani semua kasus ini dengan cara yang sama: tunggu sesuai `retry-after`, lalu coba lagi. Terpisah dari batas-batas ini, kirim penulisan pengaturan instalasi untuk plugin yang sama satu per satu: ketika beberapa tiba bersamaan, sebagian dapat dijawab dengan `503` dan `x-should-retry: true`, dan permintaan tersebut aman untuk dikirim lagi setelah satu atau dua detik (lihat [Menetapkan pengaturan instalasi](https://platform.claude.com/docs/id/manage-claude/plugins-api#set-an-installation-setting)).

## Paginasi

Endpoint daftar menggunakan **cursor buram** ("opaque cursor"). Permintaan pertama mengembalikan hingga `limit` baris ditambah cursor `next_page`; berikan cursor tersebut tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, dan ulangi hingga `next_page` bernilai `null`. Perlakukan string cursor sebagai buram: jangan mengurai, mengubah, atau menyusunnya sendiri. [Mencantumkan plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api#list-plugins) dapat mengembalikan halaman dengan plugin kurang dari `limit`, atau tanpa plugin sama sekali, sementara `next_page` masih terisi, jadi teruslah meminta halaman hingga `next_page` bernilai `null`. Iterator daftar pada SDK mengambil halaman berikutnya saat Anda melakukan iterasi tetapi berhenti pada halaman kosong pertama, sehingga pada daftar plugin iterator tersebut dapat berhenti lebih awal; ketika Anda memerlukan setiap plugin, seperti pada [alur kerja inventaris keamanan](https://platform.claude.com/docs/id/manage-claude/plugins-api#keep-a-security-inventory-in-sync), minta setiap halaman sendiri dan berikan `next_page`-nya sebagai `page`.

`limit` memiliki default 20 dan minimum 1. Maksimumnya adalah 100 untuk plugin, pengaturan instalasi, dan pembagian, serta 1.000 untuk versi dan marketplace. Setiap daftar diurutkan dari yang terbaru.

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Error](https://platform.claude.com/docs/id/api/errors). Sertakan `request_id` dari body respons saat menghubungi dukungan.

| Status | Arti                                                                                                                                                                                                                                                                                                                          |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | Input tidak valid, atau operasi tidak berlaku untuk plugin atau marketplace ini (lihat bagian masing-masing endpoint). Juga dikembalikan untuk parameter kueri yang tidak dikenali oleh endpoint, dan untuk organisasi yang bukan organisasi Claude Enterprise (`this endpoint is not supported for this organization type`). |
| 401    | Header `x-api-key` tidak ada, atau kunci tidak dikenali.                                                                                                                                                                                                                                                                      |
| 403    | Kunci tidak memiliki scope yang diperlukan, atau permintaan mengunggah ke plugin atau marketplace pribadi milik anggota, mengubah versi yang disajikannya, atau menetapkan default-nya. (Menghapus plugin milik anggota diizinkan.)                                                                                           |
| 404    | Sumber daya tidak ditemukan. Juga dikembalikan ketika permintaan tidak menyertakan nilai `anthropic-beta`, atau API tidak diaktifkan untuk organisasi Anda, sehingga endpoint tampak seolah-olah tidak ada.                                                                                                                   |
| 409    | Sebuah nama sudah digunakan, pemindaian konten masih berjalan, atau unggahan yang bertentangan sedang berlangsung.                                                                                                                                                                                                            |
| 413    | Body permintaan melebihi batas ukuran: 200 MB untuk unggahan, 32 MB untuk validasi marketplace.                                                                                                                                                                                                                               |
| 429    | "Rate limit" (batas laju) terlampaui. Lihat [Pembatasan laju](https://platform.claude.com/docs/id/manage-claude/plugins-api#rate-limiting).                                                                                                                                                                                   |
| 500    | Error internal.                                                                                                                                                                                                                                                                                                               |
| 503    | Sementara. Juga dikembalikan ketika beberapa penulisan pengaturan instalasi untuk satu plugin tiba pada saat yang sama; kirimkan penulisan tersebut satu per satu. Coba lagi dengan backoff, kecuali `registration_pending` (lihat tabel berikut).                                                                            |

Ketika satu status memiliki beberapa penyebab yang perlu Anda tangani secara berbeda, error juga menyertakan `error.details.error_code`, serta `error.details.plugin_id` atau `error.details.plugin_version_id` ketika penyebabnya melibatkan salah satunya:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "...",
    "details": {
      "error_code": "plugin_name_taken",
      "plugin_id": "plugin_01Hq3vX8kZcN2mB7pR4tY9wL"
    }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

| `error_code`                                    | Status | Arti dan apa yang harus dilakukan                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin_name_taken`                             | 409    | Plugin dengan nama ini sudah ada di marketplace. `details.plugin_id` adalah plugin tersebut. Jika Anda mencoba ulang pembuatan yang responsnya hilang, lanjutkan dengan plugin tersebut. Ketika `plugin_id` tidak ada, nama tersebut dipegang oleh skill mandiri: unggah dengan nama lain, atau hapus skill tersebut di claude.ai. |
| `skill_name_taken`                              | 409    | Plugin berada di marketplace pustaka dan salah satu skill-nya memiliki nama yang sama dengan skill organisasi (skill yang diunggah administrator untuk seluruh organisasi di claude.ai). `details.skill_name` menyebutkan namanya. Ganti nama atau hapus salah satunya.                                                            |
| `registration_pending`                          | 503    | File telah disimpan, tetapi skill plugin belum dapat disediakan untuk anggota. Lihat [Mencoba ulang unggahan](https://platform.claude.com/docs/id/manage-claude/plugins-api#retrying-uploads).                                                                                                                                     |
| `scan_pending`                                  | 409    | Pemindaian konten versi tersebut masih berjalan. Coba lagi setelah selesai.                                                                                                                                                                                                                                                        |
| `scan_failed`                                   | 400    | Pemindaian konten versi tersebut gagal, mengalami error, atau tidak mencapai keputusan, sehingga versi tersebut tidak dapat disajikan. Pilih versi lain.                                                                                                                                                                           |
| `cmek_key_disabled`, `cmek_key_network_blocked` | 400    | Kunci enkripsi yang dikelola pelanggan milik organisasi Anda tidak tersedia. Lihat [Kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/plugins-api#customer-managed-encryption-keys).                                                                                                       |

Kode baru dapat ditambahkan. Perlakukan kode yang tidak Anda kenali sebagaimana Anda memperlakukan statusnya.

### Mencoba ulang unggahan

Tidak ada endpoint yang menerima `Idempotency-Key`. Mengubah versi yang disajikan, menetapkan pengaturan instalasi, dan menetapkan default marketplace aman untuk diulang. Penghapusan yang diulang, atau penghapusan pengaturan instalasi grup yang diulang, mengembalikan `404`.

Unggahan yang mengembalikan error tidak menyimpan apa pun, dengan satu pengecualian: `503` dengan `error_code: "registration_pending"`. Setelah menyimpan file unggahan, server mendaftarkan skill versi baru ke claude.ai, yang membuat skill tersebut dapat digunakan oleh anggota; `registration_pending` berarti file telah disimpan tetapi langkah terakhir tersebut tidak selesai. Mengunggah file yang sama sekali lagi akan menyelesaikannya (dan menyimpan satu versi lagi yang identik):

* Pada `POST /v1/organizations/plugins`, plugin *telah* dibuat, dan respons menyertakan `x-should-retry: false`: jangan kirim ulang permintaan pembuatan (pengiriman ulang mengembalikan `409 plugin_name_taken`); sebagai gantinya, unggah file yang sama sebagai versi dari `details.plugin_id`.
* Pada `POST /v1/organizations/plugins/{plugin_id}/versions`, versi *telah* disimpan (`details.plugin_version_id`); kirim ulang permintaan yang sama ketika respons menyertakan `x-should-retry: true`, dan jangan lakukan ketika respons menyertakan `false`.

Jika respons pembuatan hilang, coba lagi: percobaan ulang mengembalikan `409 plugin_name_taken` dengan ID plugin di `details.plugin_id`, dan Anda melanjutkan dengan plugin tersebut. Mencoba ulang pembuatan versi yang responsnya hilang akan menyimpan versi kedua yang identik. Untuk menghindarinya, catat `latest_version_id` plugin sebelum setiap unggahan; jika respons hilang, baca plugin tersebut dan coba lagi hanya jika `latest_version_id` tidak berubah.

## Event Activity Feed

Setiap penulisan melalui API ini dicatat di [Compliance API Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) organisasi Anda, diatribusikan ke kunci API sebagai `api_actor` yang membawa ID `apikey_`-nya. Aktor yang sama muncul di `created_by` pada plugin dan versi yang dibuat oleh kunci tersebut.

| Event                                    | Dipancarkan ketika                                                                                                                                                                                         |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `claude_plugin_created`                  | Plugin dibuat melalui unggahan (di sini atau di claude.ai) atau melalui permintaan publikasi yang diterima. Plugin yang dibuat melalui sinkronisasi Git hanya memancarkan `claude_plugin_version_created`. |
| `claude_plugin_version_created`          | Sebuah versi disimpan. Versi yang disimpan melalui sinkronisasi Git diatribusikan ke `system_actor`.                                                                                                       |
| `claude_plugin_updated`                  | Versi baru diunggah ke plugin yang sudah ada.                                                                                                                                                              |
| `claude_plugin_served_version_updated`   | Versi yang disajikan berubah.                                                                                                                                                                              |
| `claude_plugin_deleted`                  | Plugin dihapus secara tersendiri, di sini atau di claude.ai.                                                                                                                                               |
| `plugin_installation_preference_updated` | Pengaturan instalasi ditetapkan atau dihapus.                                                                                                                                                              |
| `marketplace_created`                    | Unggahan pertama membuat marketplace pustaka.                                                                                                                                                              |
| `marketplace_updated`                    | Pengaturan instalasi default marketplace berubah, atau administrator atau pemilik memulai sinkronisasi di claude.ai.                                                                                       |
| `marketplace_deleted`                    | Marketplace dihapus di claude.ai bersama dengan plugin-pluginnya (tanpa event per plugin).                                                                                                                 |
| `claude_plugin_archive_accessed`         | Arsip plugin milik anggota diunduh.                                                                                                                                                                        |
| `claude_plugin_security_scan_completed`  | Pemindaian konten selesai.                                                                                                                                                                                 |

ID plugin, versi, dan marketplace dalam event ini adalah ID yang sama dengan yang dikembalikan API ini. `plugin_installation_preference_updated` mengidentifikasi plugin berdasarkan `name` dan `marketplace_id`-nya, bukan `id`-nya.

Mengubah default marketplace mencatat satu event `marketplace_updated` dan tidak ada event per plugin, meskipun perubahan tersebut mengubah nilai setiap plugin yang mewarisi default tersebut. Pembacaan tidak dicatat, kecuali unduhan arsip plugin milik anggota. Penulisan yang tidak mengubah apa pun tidak mencatat apa pun.

Pembagian yang diberikan atau ditarik di claude.ai muncul di feed sebagai event `role_assignment_granted` dan `role_assignment_revoked`. API ini tidak melaporkan penghapusan: plugin yang dihapus hanya tidak muncul di daftar berikutnya. Plugin yang dihapus melalui sinkronisasi Git, melalui penghapusan marketplace-nya (satu event `marketplace_deleted`), atau melalui penghapusan akun anggota atau organisasi tidak memancarkan event per plugin, jadi tampilkan ulang daftar inventaris lengkap secara berkala untuk mendeteksi penghapusan.

## Kunci enkripsi yang dikelola pelanggan

Jika organisasi Anda menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek), `description`, `release_notes`, `components`, dan file suatu versi dienkripsi dengan kunci tersebut. Selama kunci tidak tersedia:

* Pembacaan dan daftar tetap berhasil, dengan `description`, `release_notes`, dan `components` dikembalikan sebagai `null`.
* Unduhan arsip, pembuatan, pembuatan versi, dan perubahan versi yang disajikan mengembalikan `400` dengan `cmek_key_disabled` atau `cmek_key_network_blocked`.
* Menghapus plugin di marketplace pustaka mengembalikan `400 cmek_key_disabled` dan tidak menghapus apa pun, karena skill-nya harus terlebih dahulu ditarik dari claude.ai dan hal itu memerlukan kunci tersebut. Penghapusan lainnya, pengaturan instalasi, dan default marketplace berfungsi seperti biasa.

Memulihkan kunci akan menghilangkan semua kondisi ini.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Membuat kunci Admin API" href="https://platform.claude.com/docs/id/manage-claude/admin-api-keys">
    Tempat pemilik utama Anda membuat kunci dengan scope tertentu.
  </Card>

  <Card title="Manajemen pengguna" href="https://platform.claude.com/docs/id/manage-claude/user-management">
    Endpoint grup yang menyediakan ID `rbac_group_` yang digunakan dalam pengaturan instalasi.
  </Card>

  <Card title="Compliance API Activity Feed" href="https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed">
    Tempat penulisan plugin dan unduhan arsip anggota dicatat.
  </Card>

  <Card title="API Analitik" href="https://platform.claude.com/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan plugin dan skill untuk Claude Enterprise.
  </Card>
</CardGroup>
