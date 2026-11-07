---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/user-management
fetched_at: 2026-11-07T02:12:06.793583Z
sha256: bb6aab3f7423a6fabbc57cad605065e28eae7d8782466dfd02ed43f0be4c2e6a
---

---
title: Manajemen pengguna
url: https://platform.claude.com/docs/id/manage-claude/user-management
description: "Kelola orang-orang di organisasi Claude Enterprise Anda dengan Admin API: daftarkan anggota dan ubah peran, kirim dan tarik undangan, kelola grup, dan baca peran kustom."
---

Halaman ini membahas pengelolaan orang-orang di organisasi **Claude Enterprise** (claude.ai) Anda secara terprogram, menggunakan [Admin API](https://platform.claude.com/docs/id/api/beta/organization):

* Mencantumkan anggota dan mencarinya berdasarkan alamat email
* Mengubah peran anggota
* Menghapus anggota, atau mengeluarkan mereka dari semua sesi di mana pun tanpa menghapus mereka (beta)
* Mengirim dan menarik kembali undangan
* Mengelola grup enterprise Anda beserta keanggotaannya
* Membaca peran kustom organisasi Anda

Untuk organisasi Claude Console (Claude Platform), lihat [panduan Admin API untuk Claude Console](https://platform.claude.com/docs/id/manage-claude/admin-api).

## Endpoint mana yang dapat digunakan organisasi Anda?

Admin API adalah satu set endpoint di bawah `https://api.anthropic.com/v1/organizations/`. Organisasi Claude Console dan Claude Enterprise melakukan autentikasi dengan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys) yang berbeda dan masing-masing memiliki akses ke subset endpoint yang berbeda:

| Endpoint                                                                                                                                                                                                                                                                                                                                                | Claude Console (Claude Platform)                                                                                           | Claude Enterprise (claude.ai)                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Anggota](https://platform.claude.com/docs/id/manage-claude/user-management#members) dan [undangan](https://platform.claude.com/docs/id/manage-claude/user-management#invites)                                                                                                                                                                          | Tersedia; lihat [panduan Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)                           | Tersedia (halaman ini)                                                                                                                                                                                                                                                               |
| [Grup](https://platform.claude.com/docs/id/manage-claude/user-management#groups)                                                                                                                                                                                                                                                                        | Tidak tersedia                                                                                                             | Tersedia (halaman ini)                                                                                                                                                                                                                                                               |
| [Peran kustom](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles)                                                                                                                                                                                                                                                          | Tidak tersedia                                                                                                             | Tersedia, hanya-baca (halaman ini)                                                                                                                                                                                                                                                   |
| [Plugin](https://platform.claude.com/docs/id/manage-claude/plugins-api) dan [Claude Tag](https://platform.claude.com/docs/id/manage-claude/claude-tag-api)                                                                                                                                                                                              | Tidak tersedia                                                                                                             | Tersedia dalam beta                                                                                                                                                                                                                                                                  |
| [Batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api)                                                                                                                                                                                                                                                                 | Tidak tersedia                                                                                                             | Tersedia                                                                                                                                                                                                                                                                             |
| Laporan penggunaan dan biaya                                                                                                                                                                                                                                                                                                                            | Tersedia; lihat [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) | Tersedia melalui [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) dan [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api) |
| [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces), [kunci API](https://platform.claude.com/docs/id/manage-claude/admin-api#api-keys), [batas laju](https://platform.claude.com/docs/id/manage-claude/rate-limits-api), dan endpoint lain dalam [panduan Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) | Tersedia                                                                                                                   | Tidak tersedia                                                                                                                                                                                                                                                                       |

Anggota dan undangan menggunakan endpoint yang sama untuk kedua jenis organisasi; halaman ini mendokumentasikan perilakunya di Claude Enterprise, termasuk [peran organisasi](https://platform.claude.com/docs/id/manage-claude/user-management#organization-roles) Claude Enterprise. Endpoint grup dan peran kustom hanya ada untuk Claude Enterprise.

<Check>
  **Memerlukan kunci Admin API dengan scope**

  Endpoint ini memerlukan kunci Admin API dengan scope yang sesuai dengan permintaan. Endpoint `GET` anggota dan undangan, serta semua endpoint peran kustom, memerlukan `read:members` (tidak ada scope peran terpisah). Endpoint `POST` dan `DELETE` anggota dan undangan memerlukan `write:members`. Endpoint `GET` grup memerlukan `read:rbac_groups`, dan endpoint `POST` dan `DELETE` grup memerlukan `write:rbac_groups`. Menetapkan peran `managed`, atau grup pada undangan, memerlukan `write:rbac_groups` selain `write:members`. Kunci yang membawa scope `read:org_audit` (scope hanya-baca untuk integrasi audit keamanan) juga dapat memanggil setiap endpoint `GET` di halaman ini dan endpoint baca [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana membuatnya dan scope mana yang harus dipilih. Kirimkan kunci di header `x-api-key` pada setiap permintaan, bersama dengan header [`anthropic-version`](https://platform.claude.com/docs/id/api/versioning).
</Check>

## Ikhtisar

Halaman ini membahas lima sumber daya:

| Sumber daya      | Endpoint                                                                                                                                                                                                                                                     | Digunakan untuk                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Anggota**      | `GET /v1/organizations/users`<br />`GET /v1/organizations/users/{user_id}`<br />`POST /v1/organizations/users/{user_id}`<br />`DELETE /v1/organizations/users/{user_id}`<br />`POST /v1/organizations/users/{user_id}/sign_out` (beta)                       | Mendaftar anggota organisasi atau mencari satu anggota berdasarkan email; mengubah peran anggota; menghapus anggota; mengeluarkan anggota dari semua sesi di mana pun. |
| **Undangan**     | `POST /v1/organizations/invites`<br />`GET /v1/organizations/invites`<br />`GET /v1/organizations/invites/{invite_id}`<br />`DELETE /v1/organizations/invites/{invite_id}`                                                                                   | Mengundang seseorang ke organisasi, melacak status undangan, dan menariknya sebelum diterima.                                                                          |
| **Grup**         | `GET /v1/organizations/rbac_groups`<br />`GET /v1/organizations/rbac_groups/{rbac_group_id}`<br />`POST /v1/organizations/rbac_groups`<br />`POST /v1/organizations/rbac_groups/{rbac_group_id}`<br />`DELETE /v1/organizations/rbac_groups/{rbac_group_id}` | Membaca grup enterprise Anda dan peran kustom yang terlampir pada masing-masing; membuat, mengganti nama, dan menghapus grup.                                          |
| **Anggota grup** | `GET /v1/organizations/rbac_groups/{rbac_group_id}/members`<br />`POST /v1/organizations/rbac_groups/{rbac_group_id}/members`<br />`DELETE /v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}`                                                  | Membaca anggota grup; menambah dan menghapus anggota.                                                                                                                  |
| **Peran kustom** | `GET /v1/organizations/rbac_roles`<br />`GET /v1/organizations/rbac_roles/{rbac_role_id}`<br />`GET /v1/organizations/rbac_roles/{rbac_role_id}/permissions`                                                                                                 | Membaca peran kustom organisasi Anda dan izin yang diberikan setiap peran.                                                                                             |

Peran kustom dan lampirannya ke grup dikelola di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings); API dapat membacanya tetapi tidak dapat mengubahnya.

## Mulai cepat

Atur variabel lingkungan `ANTHROPIC_API_KEY` ke kunci Admin API Anda. Contoh-contoh di halaman ini membaca kunci dari variabel tersebut. SDK dan CLI `ant` mengirimkan header `Authorization` dan `anthropic-version` untuk Anda.

Tampilkan daftar anggota organisasi, yang terbaru terlebih dahulu:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/users?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:users list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  users = client.organization.users.list(limit=20)

  for user in users:
      print(f"{user.id}: {user.email} ({user.role})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const users = await client.organization.users.list({ limit: 20 });

  for await (const user of users) {
    console.log(`${user.id}: ${user.email} (${user.role})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.Users.List(new() { Limit = 20 });

  await foreach (var user in page.Paginate())
  {
      Console.WriteLine($"{user.ID}: {user.Email} ({user.Role.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  users := client.Organization.Users.ListAutoPaging(context.Background(), anthropic.OrganizationUserListParams{
  	Limit: anthropic.Int(20),
  })

  for users.Next() {
  	user := users.Current()
  	fmt.Printf("%s: %s (%s)\n", user.ID, user.Email, user.Role)
  }
  if err := users.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.users.UserListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserListParams.builder()
          .limit(20)
          .build();
      var users = client.organization().users().list(params);

      for (var user : users.autoPager()) {
          IO.println(user.id() + ": " + user.email() + " (" + user.role().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $users = $client->organization->users->list(limit: 20);

  foreach ($users->pagingEachItem() as $user) {
      echo "{$user->id}: {$user->email} ({$user->role})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  users = client.organization.users.list(limit: 20)

  users.auto_paging_each do |user|
    puts "#{user.id}: #{user.email} (#{user.role})"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "user",
      "id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "name": "Jane Smith",
      "role": "user",
      "added_at": "2026-06-12T09:14:03Z"
    }
  ],
  "has_more": false,
  "first_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "last_id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

## Konsep utama

### Peran organisasi

Setiap anggota memiliki tepat satu peran organisasi. Operasi baca mengembalikan peran anggota sebagai salah satu dari lima nilai:

| Peran              | Arti                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------ |
| `user`             | Anggota standar.                                                                     |
| `managed`          | Anggota yang izinnya diberikan melalui peran kustom yang terlampir pada grup mereka. |
| `owner`            | Pemilik organisasi.                                                                  |
| `membership_admin` | Anggota yang dapat mengelola anggota organisasi.                                     |
| `primary_owner`    | Pemilik utama organisasi. Hanya ada tepat satu.                                      |

API hanya dapat menetapkan peran `user` dan `managed`, saat pembuatan undangan dan pembaruan peran. Menetapkan `managed` memerlukan scope `write:rbac_groups` selain `write:members`, karena izin anggota managed berasal dari peran kustom yang terlampir pada grup mereka. Peran administratif (`owner`, `membership_admin`, dan `primary_owner`) ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat diubah atau dihapus melalui API ini.

### Anggota dan undangan

Seseorang menjadi anggota dengan menerima undangan (atau melalui “single sign-on” (masuk tunggal), atau SSO, organisasi Anda, jika dikonfigurasi). Membuat undangan akan mengirimkan email undangan; undangan kemudian berstatus `pending` hingga penerima menerimanya (`accepted`) atau `expires_at` yang ditetapkan server terlewati (`expired`). Hanya undangan `pending` yang dapat ditarik. Untuk mengubah alamat email atau peran undangan yang tertunda, tarik undangan tersebut dan buat yang baru.

Jika paket organisasi Anda mengambil anggota dari kumpulan kursi (seat) terbatas yang dibeli, undangan yang tertunda menggunakan satu kursi. Endpoint pembuatan undangan tidak menerima parameter kursi atau tier: kursi ditetapkan secara otomatis dari tier terendah yang masih tersedia. Membuat undangan saat tidak ada kursi kosong akan gagal dengan error 400 alih-alih membeli kursi. Menarik undangan, membiarkannya kedaluwarsa, atau menghapus anggota di kemudian hari akan mengembalikan kursi ke kumpulan.

### Grup dan peran

Grup menghubungkan anggota dengan peran kustom (“role-based access control” (kontrol akses berbasis peran), yaitu `rbac` dalam path endpoint dan nama scope). Grup dimiliki oleh organisasi induk Anda beserta setiap organisasi di bawahnya, bukan oleh satu organisasi saja. Jadi, scope grup (`read:rbac_groups` dan `write:rbac_groups`) memerlukan kunci yang dibuat untuk semua organisasi yang tertaut. Setiap grup memiliki `source_type`: `direct` untuk grup yang dibuat di claude.ai, `scim` untuk grup yang disediakan oleh penyedia identitas Anda. Field `role_ids` pada grup mencantumkan ID peran kustom yang terlampir padanya. Uraikan ID tersebut menjadi nama dan izin dengan [endpoint peran kustom](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles). Setiap organisasi memiliki katalog perannya sendiri, tetapi grup digunakan bersama di seluruh organisasi induk Anda. Jadi, mengambil peran yang dimiliki organisasi lain di bawah organisasi induk Anda akan mengembalikan 404 untuk kunci Anda. Field `role_ids` bernilai `null` (bukan `[]`) ketika data peran untuk sementara tidak tersedia, jadi coba lagi untuk membedakan pembacaan yang terdegradasi dari grup yang tidak memiliki peran.

## Pembuatan versi

Kirimkan header `anthropic-version` pada setiap permintaan; lihat [Versi](https://platform.claude.com/docs/id/api/versioning) untuk versi yang tersedia.

## Batas laju

Endpoint Admin API berbagi batas per organisasi sebesar **100 permintaan per menit**; pembuatan undangan memiliki batasnya sendiri sebesar **1.200 permintaan per jam** sebagai gantinya. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi

Daftar anggota dan undangan menggunakan paginasi berbasis ID: berikan `limit` (default 20, maksimum 1.000) ditambah paling banyak salah satu dari `before_id` atau `after_id`, lalu lakukan paginasi menggunakan field `first_id` dan `last_id` dari setiap respons hingga `has_more` bernilai `false`. Daftar grup dan peran kustom menggunakan **kursor opak** sebagai gantinya: berikan nilai `next_page` dari respons tanpa diubah sebagai parameter `page` pada permintaan berikutnya, hingga `next_page` bernilai `null`.

Saat Anda melakukan iterasi atas hasil, SDK mengambil halaman berikutnya untuk Anda, sehingga `limit` menetapkan ukuran halaman, bukan total. Di CLI, `--limit` menetapkan jumlah total hasil untuk daftar anggota dan undangan. Untuk daftar grup dan peran, opsi ini menetapkan ukuran halaman.

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Error Claude API](https://platform.claude.com/docs/id/api/errors).

## Anggota

### Mendaftar anggota

`GET /v1/organizations/users` mengembalikan anggota organisasi, yang paling baru ditambahkan terlebih dahulu. Filter berdasarkan `email` untuk mencari anggota tertentu; pencocokan tidak peka huruf besar/kecil dan menoleransi varian umum dari alamat yang sama (misalnya, `jane+hiring@example.com` cocok dengan `jane@example.com`). Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar pengguna](https://platform.claude.com/docs/id/api/organization/users/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/users?email=jane@example.com" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:users list --email jane@example.com
  ```

  ```python Python
  client = anthropic.Anthropic()

  users = client.organization.users.list(email="jane@example.com")

  for user in users:
      print(f"{user.id}: {user.email} ({user.role})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const users = await client.organization.users.list({ email: "jane@example.com" });

  for await (const user of users) {
    console.log(`${user.id}: ${user.email} (${user.role})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.Users.List(new() { Email = "jane@example.com" });

  await foreach (var user in page.Paginate())
  {
      Console.WriteLine($"{user.ID}: {user.Email} ({user.Role.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  users := client.Organization.Users.ListAutoPaging(context.Background(), anthropic.OrganizationUserListParams{
  	Email: anthropic.String("jane@example.com"),
  })

  for users.Next() {
  	user := users.Current()
  	fmt.Printf("%s: %s (%s)\n", user.ID, user.Email, user.Role)
  }
  if err := users.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.users.UserListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserListParams.builder()
          .email("jane@example.com")
          .build();
      var users = client.organization().users().list(params);

      for (var user : users.autoPager()) {
          IO.println(user.id() + ": " + user.email() + " (" + user.role().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $users = $client->organization->users->list(email: 'jane@example.com');

  foreach ($users->pagingEachItem() as $user) {
      echo "{$user->id}: {$user->email} ({$user->role})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  users = client.organization.users.list(email: "jane@example.com")

  users.auto_paging_each do |user|
    puts "#{user.id}: #{user.email} (#{user.role})"
  end
  ```
</CodeGroup>

### Mendapatkan anggota

`GET /v1/organizations/users/{user_id}` mengembalikan satu anggota berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Dapatkan pengguna](https://platform.claude.com/docs/id/api/organization/users/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:users retrieve --user-id user_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  user = client.organization.users.retrieve("user_01AbCdEfGhIjKlMnOpQrSt")

  print(f"id: {user.id}")
  print(f"email: {user.email}")
  print(f"role: {user.role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const user = await client.organization.users.retrieve("user_01AbCdEfGhIjKlMnOpQrSt");

  console.log(`id: ${user.id}`);
  console.log(`email: ${user.email}`);
  console.log(`role: ${user.role}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var user = await client.Organization.Users.Retrieve("user_01AbCdEfGhIjKlMnOpQrSt");

  Console.WriteLine($"id: {user.ID}");
  Console.WriteLine($"email: {user.Email}");
  Console.WriteLine($"role: {user.Role.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  user, err := client.Organization.Users.Get(context.Background(), "user_01AbCdEfGhIjKlMnOpQrSt")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", user.ID)
  fmt.Printf("email: %s\n", user.Email)
  fmt.Printf("role: %s\n", user.Role)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var user = client.organization().users()
      .retrieve("user_01AbCdEfGhIjKlMnOpQrSt");

  IO.println("id: " + user.id());
  IO.println("email: " + user.email());
  IO.println("role: " + user.role().asString());
  ```

  ```php PHP
  $client = new Client();

  $user = $client->organization->users->retrieve(
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
  );

  echo "id: {$user->id}\n";
  echo "email: {$user->email}\n";
  echo "role: {$user->role}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user = client.organization.users.retrieve("user_01AbCdEfGhIjKlMnOpQrSt")

  puts "id: #{user.id}"
  puts "email: #{user.email}"
  puts "role: #{user.role}"
  ```
</CodeGroup>

### Mengubah peran anggota

`POST /v1/organizations/users/{user_id}` menetapkan peran anggota menjadi `user` atau `managed`. Anggota yang memegang peran administratif (`owner`, `membership_admin`, atau `primary_owner`) tidak dapat diubah melalui endpoint ini, dan peran administratif tidak dapat ditetapkan; keduanya mengembalikan 400 dan dikelola di pengaturan organisasi claude.ai. Jika penyedia identitas organisasi Anda mengelola peran (SSO lanjutan atau penyediaan SCIM lanjutan), pembaruan peran mengembalikan 400. Memerlukan scope `write:members`, ditambah `write:rbac_groups` saat mengubah peran menjadi `managed`.

Untuk detail parameter lengkap dan skema respons, lihat [Perbarui pengguna](https://platform.claude.com/docs/id/api/organization/users/update) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{"role": "managed"}'
  ```

  ```bash CLI
  ant organization:users update \
    --user-id user_01AbCdEfGhIjKlMnOpQrSt \
    --role managed
  ```

  ```python Python
  client = anthropic.Anthropic()

  user = client.organization.users.update("user_01AbCdEfGhIjKlMnOpQrSt", role="managed")

  print(f"id: {user.id}")
  print(f"role: {user.role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const user = await client.organization.users.update("user_01AbCdEfGhIjKlMnOpQrSt", {
    role: "managed"
  });

  console.log(`id: ${user.id}`);
  console.log(`role: ${user.role}`);
  ```

  ```csharp C#
  using Anthropic.Models.Organization.Users;
  // ...

  AnthropicClient client = new();

  var user = await client.Organization.Users.Update(
      "user_01AbCdEfGhIjKlMnOpQrSt",
      new() { Role = Role.Managed }
  );

  Console.WriteLine($"id: {user.ID}");
  Console.WriteLine($"role: {user.Role.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  user, err := client.Organization.Users.Update(
  	context.Background(),
  	"user_01AbCdEfGhIjKlMnOpQrSt",
  	anthropic.OrganizationUserUpdateParams{
  		Role: anthropic.OrganizationUserUpdateParamsRoleManaged,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", user.ID)
  fmt.Printf("role: %s\n", user.Role)
  ```

  ```java Java
  import com.anthropic.models.organization.users.UserUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserUpdateParams.builder()
          .role(UserUpdateParams.Role.MANAGED)
          .build();
      var user = client.organization().users()
          .update("user_01AbCdEfGhIjKlMnOpQrSt", params);

      IO.println("id: " + user.id());
      IO.println("role: " + user.role().asString());
  }
  ```

  ```php PHP
  use Anthropic\Organization\Users\UserUpdateParams\Role;
  // ...

  $client = new Client();

  $user = $client->organization->users->update(
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
      role: Role::MANAGED,
  );

  echo "id: {$user->id}\n";
  echo "role: {$user->role}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01AbCdEfGhIjKlMnOpQrSt"
  user = client.organization.users.update(user_id, role: :managed)

  puts "id: #{user.id}"
  puts "role: #{user.role}"
  ```
</CodeGroup>

### Menghapus anggota

`DELETE /v1/organizations/users/{user_id}` menghapus anggota dari organisasi, mengembalikan kursi yang dibeli yang mereka tempati ke kumpulan organisasi. Anggota yang memegang peran administratif tidak dapat dihapus melalui endpoint ini, dan jika penyedia identitas Anda mengelola keanggotaan (SCIM), penghapusan mengembalikan 400. Memerlukan scope `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Keluarkan pengguna](https://platform.claude.com/docs/id/api/organization/users/remove) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:users remove --user-id user_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_user = client.organization.users.remove("user_01AbCdEfGhIjKlMnOpQrSt")

  print(f"id: {removed_user.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedUser = await client.organization.users.remove("user_01AbCdEfGhIjKlMnOpQrSt");

  console.log(`id: ${removedUser.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedUser = await client.Organization.Users.Remove("user_01AbCdEfGhIjKlMnOpQrSt");

  Console.WriteLine($"id: {removedUser.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedUser, err := client.Organization.Users.Remove(context.Background(), "user_01AbCdEfGhIjKlMnOpQrSt")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", removedUser.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var removedUser = client.organization().users()
      .remove("user_01AbCdEfGhIjKlMnOpQrSt");

  IO.println("id: " + removedUser.id());
  ```

  ```php PHP
  $client = new Client();

  $removedUser = $client->organization->users->remove(
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
  );

  echo "id: {$removedUser->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01AbCdEfGhIjKlMnOpQrSt"
  removed_user = client.organization.users.remove(user_id)

  puts "id: #{removed_user.id}"
  ```
</CodeGroup>

```json
{
  "type": "user_deleted",
  "id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

### Mengeluarkan anggota dari semua sesi di mana saja

`POST /v1/organizations/users/{user_id}/sign_out` mengeluarkan anggota dari Claude di setiap browser dan perangkat, tanpa menghapus mereka dari organisasi. Gunakan ini ketika perangkat anggota hilang atau dicuri, selama insiden keamanan, atau saat Anda menyelidiki sebuah akun sebelum memutuskan apakah akan menghapus anggota tersebut. Memerlukan scope `write:members`.

<Note>
  Endpoint ini berstatus **beta** untuk organisasi Claude Enterprise.

  Setiap permintaan harus menyertakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `anthropic-beta: admin-user-sign-out-2026-10-08`. Permintaan tanpa header tersebut mengembalikan 400, dengan pesan yang menyebutkan nilainya. SDK dan CLI mengirimkannya untuk Anda.

  Jika versi SDK atau CLI `ant` Anda tidak memiliki endpoint ini, kirim permintaan melalui HTTP dengan header ini.
</Note>

Pengeluaran sesi ini menjangkau seluruh akun Claude milik orang tersebut, termasuk sesi mereka di organisasi lain dan pada paket individu. Anggota tetap mempertahankan kursi dan perannya serta dapat masuk kembali saat itu juga. Untuk mencegah seseorang masuk, [hapus mereka](https://platform.claude.com/docs/id/manage-claude/user-management#remove-a-member) atau, jika organisasi Anda mewajibkan single sign-on, nonaktifkan akun mereka di penyedia identitas Anda. Menonaktifkan akun menghentikan proses masuk baru tetapi tetap mempertahankan mereka di daftar anggota Anda. Jika Anda menghapus seseorang dan membiarkan akun penyedia identitas mereka tetap aktif, penyediaan otomatis dapat menambahkan mereka kembali saat mereka masuk berikutnya. Jika penyedia identitas Anda mengelola keanggotaan, Anda hanya dapat menghapus anggota di sana.

Buat kunci sebelum Anda membutuhkannya. Lihat [Membuat kunci untuk organisasi Claude Enterprise](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization). Kunci `write:members` hanya berfungsi di organisasi tempat kunci tersebut dibuat, sehingga setiap organisasi yang tertaut memerlukan kuncinya sendiri. Pemilik utama organisasi tersebut yang membuatnya. Untuk mencari anggota berdasarkan alamat email dengan kunci yang sama, pilih juga scope `read:members`.

Permintaan ini tidak memiliki body. Teruskan `id` anggota, yang dikembalikan oleh [Mendaftar anggota](https://platform.claude.com/docs/id/manage-claude/user-management#list-members):

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt/sign_out" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: admin-user-sign-out-2026-10-08"
  ```

  ```bash CLI
  ant beta:organization:users sign-out --user-id user_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  user = client.beta.organization.users.sign_out("user_01AbCdEfGhIjKlMnOpQrSt")

  print(f"id: {user.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const user = await client.beta.organization.users.signOut("user_01AbCdEfGhIjKlMnOpQrSt");

  console.log(`id: ${user.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var user = await client.Beta.Organization.Users.SignOut("user_01AbCdEfGhIjKlMnOpQrSt");

  Console.WriteLine($"id: {user.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  user, err := client.Beta.Organization.Users.SignOut(context.Background(), "user_01AbCdEfGhIjKlMnOpQrSt", anthropic.BetaOrganizationUserSignOutParams{})
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", user.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var user = client.beta().organization().users()
      .signOut("user_01AbCdEfGhIjKlMnOpQrSt");

  IO.println("id: " + user.id());
  ```

  ```php PHP
  $client = new Client();

  $user = $client->beta->organization->users->signOut(
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
  );

  echo "id: {$user->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user = client.beta.organization.users.sign_out("user_01AbCdEfGhIjKlMnOpQrSt")

  puts "id: #{user.id}"
  ```
</CodeGroup>

Permintaan yang berhasil mengembalikan 200 beserta data anggota, yang peran dan field lainnya tidak berubah:

```json
{
  "type": "user",
  "id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "email": "jane@example.com",
  "name": "Jane Smith",
  "role": "user",
  "added_at": "2026-06-12T09:14:03Z"
}
```

Jika Anda belum memiliki kunci, seorang pemilik dapat menggunakan tindakan **Keluar dari semua perangkat** di halaman Anggota pada [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) sebagai gantinya. Tindakan ini mengakhiri sesi, perangkat tepercaya, dan token OAuth yang sama, serta menghapus registrasi notifikasi push yang sama. Pemilik tidak dapat menggunakannya pada akunnya sendiri: mereka mengeluarkan sesi mereka sendiri dari pengaturan akun mereka di claude.ai.

#### Apa yang diakhiri oleh permintaan ini

Permintaan ini mengakhiri semua hal berikut untuk anggota:

* **Sesi masuk:** Semuanya untuk akun orang tersebut, di setiap browser dan perangkat.
* **Perangkat tepercaya:** Setiap browser, komputer, atau ponsel yang didaftarkan orang tersebut sebagai tepercaya untuk tindakan sensitif. Orang tersebut harus mendaftarkan setiap perangkat lagi.
* **Token OAuth yang diterbitkan untuk organisasi ini:** Aplikasi mana pun yang memegangnya, seperti Claude Code atau aplikasi pihak ketiga. Aplikasi tersebut harus masuk kembali. Token hampir selalu langsung berhenti berfungsi, dan paling lama dalam satu jam.

Permintaan ini juga menghapus catatan browser tempat orang tersebut memilih untuk melewati verifikasi dua langkah Claude, sehingga proses masuk berikutnya di sana akan meminta langkah kedua lagi. Permintaan ini juga menghapus registrasi notifikasi push yang disimpan Claude untuk ponsel, aplikasi desktop, dan browser orang tersebut, sehingga Claude berhenti mengirimkan notifikasi ke perangkat tersebut. Penghapusan ini berjalan secara asinkron: biasanya selesai dalam satu menit, tetapi dalam kasus yang jarang dapat memakan waktu lebih lama. Respons 200 tidak mengonfirmasi kedua langkah ini.

Hanya token OAuth yang terbatas pada organisasi ini. Sesi, perangkat tepercaya, dan registrasi notifikasi push adalah milik akun orang tersebut, sehingga pengeluaran sesi ini juga menjangkau organisasi mereka yang lain dan paket individu apa pun.

Permintaan ini tidak menghapus apa pun yang sudah tersimpan di perangkat.

#### Apa yang tidak diakhiri oleh permintaan ini

Permintaan ini tidak mengakhiri hal-hal berikut:

* **Kunci API:** Kunci tersebut tetap berfungsi, termasuk kunci Admin API yang dibuat oleh orang tersebut. Untuk menghentikan kunci Admin API, hapus kunci tersebut di bagian **Kunci** pada [claude.ai > Pengaturan organisasi > API](https://claude.ai/admin-settings/api-access).
* **Token OAuth untuk organisasi lain:** Untuk mengakhirinya, kirim permintaan di setiap organisasi dengan kunci organisasi tersebut. Orang tersebut memiliki `id` yang sama di setiap organisasi. Token OAuth yang diterbitkan untuk akun orang tersebut dan bukan untuk sebuah organisasi juga tetap berfungsi, dan permintaan ini tidak dapat mengakhirinya.
* **Sesi cloud dan routine Claude Code:** Sesi yang berjalan di infrastruktur Anthropic, seperti Claude Code di web, atau di salah satu [lingkungan self-hosted](https://code.claude.com/docs/en/self-hosted-environments) Anda tetap berjalan. Pekerjaan yang sedang berlangsung saat Anda mengirim permintaan, atau yang dimulai segera setelahnya, dapat gagal. Sesi tersebut kemudian mendapatkan kredensial baru tanpa orang tersebut masuk kembali, dan terus berjalan. [Routine](https://code.claude.com/docs/en/routines) milik orang tersebut yang berjalan sesuai jadwal atau pada event GitHub tetap memulai sesi baru. Tindakan **Keluar dari semua perangkat** juga membiarkan hal-hal ini tetap berjalan.
* **Komputer yang ditautkan ke Cowork:** Komputer tersebut tetap tertaut.
* **Proses masuk yang sedang berlangsung:** Proses masuk yang sudah berjalan dapat selesai selama permintaan, atau hingga 5 menit setelahnya. Jika [ekspor log audit](https://platform.claude.com/docs/id/manage-claude/compliance-api#export-audit-logs) atau [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) menunjukkan orang tersebut masuk setelah permintaan, kirim permintaan lagi. Proses masuk ke aplikasi seperti Claude Code tidak dicatat di sana, jadi jika orang tersebut sedang masuk ke salah satunya, kirim permintaan lagi setelah 5 menit.

#### Siapa yang tidak dapat Anda keluarkan

Permintaan ini tidak dapat mengeluarkan pemilik utama organisasi: permintaan mengembalikan 400 dengan kode error `cannot_sign_out_primary_owner`. Tidak seorang pun di organisasi Anda dapat mengeluarkan pemilik utama, termasuk di halaman Anggota. Pemilik utama mengeluarkan sesi mereka sendiri dari pengaturan akun mereka di claude.ai.

Kunci dengan scope `write:members` dapat mengeluarkan semua orang lainnya. Itu termasuk pemilik, anggota yang peran kustomnya mencakup izin untuk mengelola pemilik, dan anggota dengan peran `membership_admin`. Pemilik dan pemilik utama dapat melakukan hal yang sama dengan tindakan **Keluar dari semua perangkat** di halaman Anggota. Hanya peran anggota di organisasi ini yang diperhitungkan, sehingga Anda dapat mengeluarkan seseorang yang merupakan pemilik utama dari organisasi lain.

Kunci tetap berfungsi setelah orang yang membuatnya berganti peran atau meninggalkan organisasi. Lihat [Apa yang terjadi pada kunci Admin API ketika orang yang membuatnya keluar?](https://platform.claude.com/docs/id/manage-claude/user-management#what-happens-to-an-admin-api-key-when-the-person-who-created-it-leaves).

#### Respons

| Status                                  | Arti                                                                                                                                                                                                                                                                                     |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200                                     | Pengeluaran sesi telah selesai. Aman untuk dicoba ulang: permintaan yang tidak menemukan apa pun lagi untuk diakhiri juga mengembalikan 200, dan permintaan kedua mengakhiri sesi, perangkat tepercaya, atau token OAuth apa pun yang diperoleh orang tersebut sejak permintaan pertama. |
| 400 `cannot_sign_out_primary_owner`     | Anggota tersebut adalah pemilik utama, yang tidak dapat dikeluarkan. Lihat [Siapa yang tidak dapat Anda keluarkan](https://platform.claude.com/docs/id/manage-claude/user-management#who-you-cant-sign-out).                                                                             |
| 400 `organization_not_enrolled_in_beta` | Endpoint ini tidak tersedia untuk organisasi Anda.                                                                                                                                                                                                                                       |
| 400                                     | Permintaan tidak menyertakan nilai `anthropic-beta`, yang disebutkan dalam pesan, atau `id` di path tidak diawali dengan `user_`.                                                                                                                                                        |
| 401                                     | Kunci tidak ada, tidak valid, atau telah dihapus, atau kunci dibuat untuk organisasi induk dan tidak terikat pada satu organisasi.                                                                                                                                                       |
| 403                                     | Kunci tidak memiliki scope `write:members`.                                                                                                                                                                                                                                              |
| 404                                     | Tidak ada anggota dengan ID tersebut di organisasi Anda.                                                                                                                                                                                                                                 |
| 429                                     | Organisasi melebihi [batas laju](https://platform.claude.com/docs/id/manage-claude/user-management#rate-limits) yang digunakan bersama oleh endpoint Admin API. Header `retry-after` menunjukkan kapan harus mencoba ulang. Pengeluaran sesi tidak memiliki batas terpisah.              |
| 503                                     | Layanan yang diperlukan permintaan untuk sementara tidak tersedia. Apa yang sudah diakhiri oleh permintaan tetap berakhir. Kirim permintaan lagi untuk mengakhiri sisanya.                                                                                                               |

Respons error mengikuti bentuk standar yang didokumentasikan di [Error Claude API](https://platform.claude.com/docs/id/api/errors), dengan kode error di `error.details.error_code`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "...",
    "details": {
      "error_code": "cannot_sign_out_primary_owner"
    }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

#### Tempat pengeluaran sesi dicatat

Setiap pengeluaran sesi yang selesai dicatat sebagai `org_user_trusted_devices_revoked`, event yang sama yang dicatat oleh tindakan **Keluar dari semua perangkat**. Event ini muncul di [ekspor log audit](https://platform.claude.com/docs/id/manage-claude/compliance-api#export-audit-logs) yang diunduh owner di claude.ai. Jika organisasi Anda memiliki Compliance API, event ini juga muncul di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), dengan jumlah perangkat tepercaya dan sesi yang diakhiri oleh permintaan. Permintaan yang berhenti di tengah jalan juga muncul di Activity Feed, dengan `completed` diatur ke `false`, dan tidak muncul di log audit.

## Undangan

### Membuat undangan

`POST /v1/organizations/invites` mengirimkan email undangan dan mengembalikan undangan dengan `expires_at` yang ditetapkan server. `role` harus berupa `user` atau `managed`. Jika undangan tertunda sudah ada untuk alamat email tersebut, atau alamat tersebut sudah milik seorang anggota, permintaan mengembalikan 400 yang menyebutkan sumber daya yang sudah ada. Organisasi yang penyedia identitasnya menyediakan pengguna secara otomatis (JIT atau SCIM) tidak dapat membuat undangan melalui API. Memerlukan scope `write:members`, ditambah `write:rbac_groups` saat `role` bernilai `managed`.

Pada paket yang mengambil anggota dari kumpulan kursi terbatas, undangan secara otomatis mengambil kursi dari tier terendah yang masih tersedia. API tidak menerima parameter tier. Jika tidak ada kursi kosong, permintaan gagal dengan error 400 alih-alih membeli kursi. Tambahkan kursi melalui manajemen paket organisasi dan coba lagi.

Field opsional `rbac_group_ids` mencantumkan grup (berdasarkan ID berawalan `rbac_group_`) yang akan ditetapkan kepada anggota saat mereka menerima undangan. Mengirimkan `rbac_group_ids` yang tidak kosong juga mengharuskan kunci membawa scope `write:rbac_groups`, karena penetapan grup dapat memberikan izin yang terlampir pada peran grup tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [Buat undangan](https://platform.claude.com/docs/id/api/organization/invites/create) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/invites" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{
      "email": "newhire@example.com",
      "role": "managed",
      "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
    }'
  ```

  ```bash CLI
  ant organization:invites create \
    --email newhire@example.com \
    --role managed \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn
  ```

  ```python Python
  client = anthropic.Anthropic()

  invite = client.organization.invites.create(
      email="newhire@example.com",
      role="managed",
      rbac_group_ids=["rbac_group_01UvWxYzAbCdEfGhIjKlMn"],
  )

  print(f"id: {invite.id}")
  print(f"email: {invite.email}")
  print(f"status: {invite.status}")
  print(f"expires_at: {invite.expires_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const invite = await client.organization.invites.create({
    email: "newhire@example.com",
    role: "managed",
    rbac_group_ids: ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
  });

  console.log(`id: ${invite.id}`);
  console.log(`email: ${invite.email}`);
  console.log(`status: ${invite.status}`);
  console.log(`expires_at: ${invite.expires_at}`);
  ```

  ```csharp C#
  using Anthropic.Models.Organization.Invites;
  // ...

  AnthropicClient client = new();

  var invite = await client.Organization.Invites.Create(new()
  {
      Email = "newhire@example.com",
      Role = Role.Managed,
      RbacGroupIds = ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
  });

  Console.WriteLine($"id: {invite.ID}");
  Console.WriteLine($"email: {invite.Email}");
  Console.WriteLine($"status: {invite.Status.Raw()}");
  Console.WriteLine($"expires_at: {invite.ExpiresAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  invite, err := client.Organization.Invites.New(context.Background(), anthropic.OrganizationInviteNewParams{
  	Email:        "newhire@example.com",
  	Role:         anthropic.OrganizationInviteNewParamsRoleManaged,
  	RBACGroupIDs: []string{"rbac_group_01UvWxYzAbCdEfGhIjKlMn"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", invite.ID)
  fmt.Printf("email: %s\n", invite.Email)
  fmt.Printf("status: %s\n", invite.Status)
  fmt.Printf("expires_at: %s\n", invite.ExpiresAt.Format(time.RFC3339))
  ```

  ```java Java
  import com.anthropic.models.organization.invites.InviteCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InviteCreateParams.builder()
          .email("newhire@example.com")
          .role(InviteCreateParams.Role.MANAGED)
          .addRbacGroupId("rbac_group_01UvWxYzAbCdEfGhIjKlMn")
          .build();
      var invite = client.organization().invites().create(params);

      IO.println("id: " + invite.id());
      IO.println("email: " + invite.email());
      IO.println("status: " + invite.status().asString());
      IO.println("expires_at: " + invite.expiresAt());
  }
  ```

  ```php PHP
  use Anthropic\Organization\Invites\InviteCreateParams\Role;
  // ...

  $client = new Client();

  $invite = $client->organization->invites->create(
      email: 'newhire@example.com',
      role: Role::MANAGED,
      rbacGroupIDs: ['rbac_group_01UvWxYzAbCdEfGhIjKlMn'],
  );

  echo "id: {$invite->id}\n";
  echo "email: {$invite->email}\n";
  echo "status: {$invite->status}\n";
  echo "expires_at: {$invite->expiresAt->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invite = client.organization.invites.create(
    email: "newhire@example.com",
    role: :managed,
    rbac_group_ids: ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
  )

  puts "id: #{invite.id}"
  puts "email: #{invite.email}"
  puts "status: #{invite.status}"
  puts "expires_at: #{invite.expires_at.iso8601}"
  ```
</CodeGroup>

```json
{
  "type": "invite",
  "id": "invite_01QrStUvWxYzAbCdEfGhIj",
  "email": "newhire@example.com",
  "role": "managed",
  "invited_at": "2026-07-06T16:20:11Z",
  "expires_at": "2026-07-27T16:20:11Z",
  "accepted_at": null,
  "status": "pending",
  "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
}
```

### Mendaftar undangan

`GET /v1/organizations/invites` mengembalikan undangan organisasi, yang terbaru terlebih dahulu, di seluruh status `pending`, `accepted`, dan `expired`. Untuk mendaftar hanya undangan dengan status tertentu, kirimkan `statuses[]` satu kali untuk setiap status, misalnya `statuses[]=pending`. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar undangan](https://platform.claude.com/docs/id/api/organization/invites/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/invites?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:invites list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  invites = client.organization.invites.list(limit=20)

  for invite in invites:
      print(f"{invite.id}: {invite.email} ({invite.status})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const invites = await client.organization.invites.list({ limit: 20 });

  for await (const invite of invites) {
    console.log(`${invite.id}: ${invite.email} (${invite.status})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.Invites.List(new() { Limit = 20 });

  await foreach (var invite in page.Paginate())
  {
      Console.WriteLine($"{invite.ID}: {invite.Email} ({invite.Status.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  invites := client.Organization.Invites.ListAutoPaging(context.Background(), anthropic.OrganizationInviteListParams{
  	Limit: anthropic.Int(20),
  })

  for invites.Next() {
  	invite := invites.Current()
  	fmt.Printf("%s: %s (%s)\n", invite.ID, invite.Email, invite.Status)
  }
  if err := invites.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.invites.InviteListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InviteListParams.builder()
          .limit(20)
          .build();
      var invites = client.organization().invites().list(params);

      for (var invite : invites.autoPager()) {
          IO.println(invite.id() + ": " + invite.email() + " (" + invite.status().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $invites = $client->organization->invites->list(limit: 20);

  foreach ($invites->pagingEachItem() as $invite) {
      echo "{$invite->id}: {$invite->email} ({$invite->status})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invites = client.organization.invites.list(limit: 20)

  invites.auto_paging_each do |invite|
    puts "#{invite.id}: #{invite.email} (#{invite.status})"
  end
  ```
</CodeGroup>

### Mendapatkan undangan

`GET /v1/organizations/invites/{invite_id}` mengembalikan satu undangan berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Dapatkan undangan](https://platform.claude.com/docs/id/api/organization/invites/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:invites retrieve --invite-id invite_01QrStUvWxYzAbCdEfGhIj
  ```

  ```python Python
  client = anthropic.Anthropic()

  invite = client.organization.invites.retrieve("invite_01QrStUvWxYzAbCdEfGhIj")

  print(f"id: {invite.id}")
  print(f"email: {invite.email}")
  print(f"status: {invite.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const invite = await client.organization.invites.retrieve("invite_01QrStUvWxYzAbCdEfGhIj");

  console.log(`id: ${invite.id}`);
  console.log(`email: ${invite.email}`);
  console.log(`status: ${invite.status}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var invite = await client.Organization.Invites.Retrieve("invite_01QrStUvWxYzAbCdEfGhIj");

  Console.WriteLine($"id: {invite.ID}");
  Console.WriteLine($"email: {invite.Email}");
  Console.WriteLine($"status: {invite.Status.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  invite, err := client.Organization.Invites.Get(context.Background(), "invite_01QrStUvWxYzAbCdEfGhIj")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", invite.ID)
  fmt.Printf("email: %s\n", invite.Email)
  fmt.Printf("status: %s\n", invite.Status)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var invite = client.organization().invites()
      .retrieve("invite_01QrStUvWxYzAbCdEfGhIj");

  IO.println("id: " + invite.id());
  IO.println("email: " + invite.email());
  IO.println("status: " + invite.status().asString());
  ```

  ```php PHP
  $client = new Client();

  $invite = $client->organization->invites->retrieve(
      inviteID: 'invite_01QrStUvWxYzAbCdEfGhIj',
  );

  echo "id: {$invite->id}\n";
  echo "email: {$invite->email}\n";
  echo "status: {$invite->status}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invite = client.organization.invites.retrieve("invite_01QrStUvWxYzAbCdEfGhIj")

  puts "id: #{invite.id}"
  puts "email: #{invite.email}"
  puts "status: #{invite.status}"
  ```
</CodeGroup>

### Menarik undangan

`DELETE /v1/organizations/invites/{invite_id}` menarik undangan `pending`, menonaktifkan tautan di email undangan. Menarik undangan `accepted` mengembalikan 400 (hapus anggotanya sebagai gantinya); menarik undangan `expired` mengembalikan 400. Memerlukan scope `write:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Hapus undangan](https://platform.claude.com/docs/id/api/organization/invites/delete) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant organization:invites delete --invite-id invite_01QrStUvWxYzAbCdEfGhIj
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_invite = client.organization.invites.delete("invite_01QrStUvWxYzAbCdEfGhIj")

  print(f"id: {deleted_invite.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedInvite = await client.organization.invites.delete(
    "invite_01QrStUvWxYzAbCdEfGhIj"
  );

  console.log(`id: ${deletedInvite.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedInvite = await client.Organization.Invites.Delete("invite_01QrStUvWxYzAbCdEfGhIj");

  Console.WriteLine($"id: {deletedInvite.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedInvite, err := client.Organization.Invites.Delete(context.Background(), "invite_01QrStUvWxYzAbCdEfGhIj")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deletedInvite.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedInvite = client.organization().invites()
      .delete("invite_01QrStUvWxYzAbCdEfGhIj");

  IO.println("id: " + deletedInvite.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedInvite = $client->organization->invites->delete(
      inviteID: 'invite_01QrStUvWxYzAbCdEfGhIj',
  );

  echo "id: {$deletedInvite->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invite_id = "invite_01QrStUvWxYzAbCdEfGhIj"
  deleted_invite = client.organization.invites.delete(invite_id)

  puts "id: #{deleted_invite.id}"
  ```
</CodeGroup>

## Grup

Grup yang dibuat langsung oleh enterprise Anda, di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau melalui API ini (`source_type: "direct"`), mendukung setiap endpoint di bagian ini. Grup yang disediakan oleh penyedia identitas Anda (`source_type: "scim"`) dapat dibaca tetapi tidak dapat diubah: mengganti nama atau menghapus grup SCIM, atau mengubah keanggotaannya, mengembalikan 400, karena penyedia identitas Anda yang memilikinya.

### Mendaftar grup

`GET /v1/organizations/rbac_groups` mengembalikan grup enterprise Anda, termasuk grup yang dikelola penyedia identitas (`scim`). Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_groups?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-groups list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  groups = client.beta.organization.rbac_groups.list(limit=20)

  for group in groups:
      print(f"{group.id}: {group.name} ({group.source_type})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const groups = await client.beta.organization.rbacGroups.list({ limit: 20 });

  for await (const group of groups) {
    console.log(`${group.id}: ${group.name} (${group.source_type})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.RbacGroups.List(new() { Limit = 20 });

  await foreach (var group in page.Paginate())
  {
      Console.WriteLine($"{group.ID}: {group.Name} ({group.SourceType.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  groups := client.Beta.Organization.RBACGroups.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRBACGroupListParams{
  	Limit: anthropic.Int(20),
  })

  for groups.Next() {
  	group := groups.Current()
  	fmt.Printf("%s: %s (%s)\n", group.ID, group.Name, group.SourceType)
  }
  if err := groups.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.RbacGroupListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RbacGroupListParams.builder()
          .limit(20)
          .build();
      var groups = client.beta().organization().rbacGroups().list(params);

      for (var group : groups.autoPager()) {
          IO.println(group.id() + ": " + group.name() + " (" + group.sourceType().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $groups = $client->beta->organization->rbacGroups->list(limit: 20);

  foreach ($groups->pagingEachItem() as $group) {
      echo "{$group->id}: {$group->name} ({$group->sourceType})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  groups = client.beta.organization.rbac_groups.list(limit: 20)

  groups.auto_paging_each do |group|
    puts "#{group.id}: #{group.name} (#{group.source_type})"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "rbac_group",
      "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "name": "Engineering",
      "source_type": "direct",
      "role_ids": ["rbac_role_01CdEfGhIjKlMnOpQrStUv"],
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Mendapatkan grup

`GET /v1/organizations/rbac_groups/{rbac_group_id}` mengembalikan satu grup berdasarkan ID. Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Dapatkan grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-groups retrieve \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn
  ```

  ```python Python
  client = anthropic.Anthropic()

  group = client.beta.organization.rbac_groups.retrieve(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  )

  print(f"id: {group.id}")
  print(f"name: {group.name}")
  print(f"source_type: {group.source_type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const group = await client.beta.organization.rbacGroups.retrieve(
    "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  );

  console.log(`id: ${group.id}`);
  console.log(`name: ${group.name}`);
  console.log(`source_type: ${group.source_type}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var group = await client.Beta.Organization.RbacGroups.Retrieve("rbac_group_01UvWxYzAbCdEfGhIjKlMn");

  Console.WriteLine($"id: {group.ID}");
  Console.WriteLine($"name: {group.Name}");
  Console.WriteLine($"source_type: {group.SourceType.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  group, err := client.Beta.Organization.RBACGroups.Get(context.Background(), "rbac_group_01UvWxYzAbCdEfGhIjKlMn")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", group.ID)
  fmt.Printf("name: %s\n", group.Name)
  fmt.Printf("source_type: %s\n", group.SourceType)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var group = client.beta().organization().rbacGroups()
      .retrieve("rbac_group_01UvWxYzAbCdEfGhIjKlMn");

  IO.println("id: " + group.id());
  IO.println("name: " + group.name());
  IO.println("source_type: " + group.sourceType().asString());
  ```

  ```php PHP
  $client = new Client();

  $group = $client->beta->organization->rbacGroups->retrieve(
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
  );

  echo "id: {$group->id}\n";
  echo "name: {$group->name}\n";
  echo "source_type: {$group->sourceType}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  group = client.beta.organization.rbac_groups.retrieve(rbac_group_id)

  puts "id: #{group.id}"
  puts "name: #{group.name}"
  puts "source_type: #{group.source_type}"
  ```
</CodeGroup>

### Membuat grup

`POST /v1/organizations/rbac_groups` membuat grup dengan `name` yang diberikan (1–255 karakter) tanpa peran atau anggota. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Buat grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/create) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{"name": "Engineering"}'
  ```

  ```bash CLI
  ant beta:organization:rbac-groups create --name Engineering
  ```

  ```python Python
  client = anthropic.Anthropic()

  group = client.beta.organization.rbac_groups.create(name="Engineering")

  print(f"id: {group.id}")
  print(f"name: {group.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const group = await client.beta.organization.rbacGroups.create({ name: "Engineering" });

  console.log(`id: ${group.id}`);
  console.log(`name: ${group.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var group = await client.Beta.Organization.RbacGroups.Create(new()
  {
      Name = "Engineering"
  });

  Console.WriteLine($"id: {group.ID}");
  Console.WriteLine($"name: {group.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  group, err := client.Beta.Organization.RBACGroups.New(context.Background(), anthropic.BetaOrganizationRBACGroupNewParams{
  	Name: "Engineering",
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", group.ID)
  fmt.Printf("name: %s\n", group.Name)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.RbacGroupCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RbacGroupCreateParams.builder()
          .name("Engineering")
          .build();
      var group = client.beta().organization().rbacGroups().create(params);

      IO.println("id: " + group.id());
      IO.println("name: " + group.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $group = $client->beta->organization->rbacGroups->create(
      name: 'Engineering',
  );

  echo "id: {$group->id}\n";
  echo "name: {$group->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  group = client.beta.organization.rbac_groups.create(name: "Engineering")

  puts "id: #{group.id}"
  puts "name: #{group.name}"
  ```
</CodeGroup>

```json
{
  "type": "rbac_group",
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "name": "Engineering",
  "source_type": "direct",
  "role_ids": [],
  "created_at": "2026-07-09T18:00:00Z",
  "updated_at": "2026-07-09T18:00:00Z"
}
```

### Mengganti nama grup

`POST /v1/organizations/rbac_groups/{rbac_group_id}` memperbarui grup. `name` adalah satu-satunya field yang dapat diubah oleh endpoint ini. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Perbarui grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/update) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{"name": "Platform Engineering"}'
  ```

  ```bash CLI
  ant beta:organization:rbac-groups update \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn \
    --name "Platform Engineering"
  ```

  ```python Python
  client = anthropic.Anthropic()

  group = client.beta.organization.rbac_groups.update(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn", name="Platform Engineering"
  )

  print(f"id: {group.id}")
  print(f"name: {group.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const group = await client.beta.organization.rbacGroups.update(
    "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
    { name: "Platform Engineering" }
  );

  console.log(`id: ${group.id}`);
  console.log(`name: ${group.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var group = await client.Beta.Organization.RbacGroups.Update(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      new() { Name = "Platform Engineering" }
  );

  Console.WriteLine($"id: {group.ID}");
  Console.WriteLine($"name: {group.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  group, err := client.Beta.Organization.RBACGroups.Update(
  	context.Background(),
  	"rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  	anthropic.BetaOrganizationRBACGroupUpdateParams{
  		Name: anthropic.String("Platform Engineering"),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", group.ID)
  fmt.Printf("name: %s\n", group.Name)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.RbacGroupUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RbacGroupUpdateParams.builder()
          .name("Platform Engineering")
          .build();
      var group = client.beta().organization().rbacGroups()
          .update("rbac_group_01UvWxYzAbCdEfGhIjKlMn", params);

      IO.println("id: " + group.id());
      IO.println("name: " + group.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $group = $client->beta->organization->rbacGroups->update(
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
      name: 'Platform Engineering',
  );

  echo "id: {$group->id}\n";
  echo "name: {$group->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  group = client.beta.organization.rbac_groups.update(rbac_group_id, name: "Platform Engineering")

  puts "id: #{group.id}"
  puts "name: #{group.name}"
  ```
</CodeGroup>

### Menghapus grup

`DELETE /v1/organizations/rbac_groups/{rbac_group_id}` menghapus grup. Anggotanya tetap menjadi anggota organisasi mereka, tetapi mereka kehilangan izin dari peran yang terlampir pada grup tersebut, dan [batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api) grup, jika ada, tidak lagi berlaku bagi mereka. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Hapus grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/delete) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-groups delete \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_group = client.beta.organization.rbac_groups.delete(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  )

  print(f"id: {deleted_group.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedGroup = await client.beta.organization.rbacGroups.delete(
    "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  );

  console.log(`id: ${deletedGroup.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedGroup = await client.Beta.Organization.RbacGroups.Delete(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  );

  Console.WriteLine($"id: {deletedGroup.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedGroup, err := client.Beta.Organization.RBACGroups.Delete(context.Background(), "rbac_group_01UvWxYzAbCdEfGhIjKlMn")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deletedGroup.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedGroup = client.beta().organization().rbacGroups()
      .delete("rbac_group_01UvWxYzAbCdEfGhIjKlMn");

  IO.println("id: " + deletedGroup.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedGroup = $client->beta->organization->rbacGroups->delete(
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
  );

  echo "id: {$deletedGroup->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  deleted_group = client.beta.organization.rbac_groups.delete(rbac_group_id)

  puts "id: #{deleted_group.id}"
  ```
</CodeGroup>

```json
{
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "type": "rbac_group_deleted"
}
```

### Mendaftar anggota grup

`GET /v1/organizations/rbac_groups/{rbac_group_id}/members` mengembalikan anggota grup (masing-masing dengan `user_id` dan email mereka), yang terlama terlebih dahulu. Hanya anggota saat ini dari organisasi-organisasi enterprise Anda yang dikembalikan, sehingga satu halaman mungkin berisi lebih sedikit dari `limit` entri sementara `has_more` bernilai `true`. Memerlukan scope `read:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar anggota grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members?limit=100" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-groups:members list \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn \
    --limit 100
  ```

  ```python Python
  client = anthropic.Anthropic()

  members = client.beta.organization.rbac_groups.members.list(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn", limit=100
  )

  for member in members:
      print(f"{member.user_id}: {member.email}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const members = await client.beta.organization.rbacGroups.members.list(
    "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
    { limit: 100 }
  );

  for await (const member of members) {
    console.log(`${member.user_id}: ${member.email}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.RbacGroups.Members.List(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      new() { Limit = 100 }
  );

  await foreach (var member in page.Paginate())
  {
      Console.WriteLine($"{member.UserID}: {member.Email}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  members := client.Beta.Organization.RBACGroups.Members.ListAutoPaging(
  	context.Background(),
  	"rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  	anthropic.BetaOrganizationRBACGroupMemberListParams{
  		Limit: anthropic.Int(100),
  	},
  )

  for members.Next() {
  	member := members.Current()
  	fmt.Printf("%s: %s\n", member.UserID, member.Email)
  }
  if err := members.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.members.MemberListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberListParams.builder()
          .limit(100)
          .build();
      var members = client.beta().organization().rbacGroups().members()
          .list("rbac_group_01UvWxYzAbCdEfGhIjKlMn", params);

      for (var member : members.autoPager()) {
          IO.println(member.userId() + ": " + member.email());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $members = $client->beta->organization->rbacGroups->members->list(
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
      limit: 100,
  );

  foreach ($members->pagingEachItem() as $member) {
      echo "{$member->userID}: {$member->email}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  members = client.beta.organization.rbac_groups.members.list(rbac_group_id, limit: 100)

  members.auto_paging_each do |member|
    puts "#{member.user_id}: #{member.email}"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "rbac_group_member",
      "rbac_group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "created_at": "2026-04-07T12:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Menambahkan anggota ke grup

`POST /v1/organizations/rbac_groups/{rbac_group_id}/members` menambahkan anggota organisasi ke grup berdasarkan `user_id`. Pengguna harus sudah menjadi anggota salah satu organisasi enterprise Anda (jika tidak, permintaan mengembalikan 404), dan menambahkan seseorang yang sudah ada di grup mengembalikan 400. Untuk grup `scim`, keanggotaan dikelola di penyedia identitas Anda dan permintaan ini mengembalikan 400. Untuk menetapkan grup kepada seseorang yang belum bergabung, gunakan `rbac_group_ids` pada [pembuatan undangan](https://platform.claude.com/docs/id/manage-claude/user-management#create-an-invite) sebagai gantinya. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Menambahkan anggota grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/add) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -d '{"user_id": "user_01AbCdEfGhIjKlMnOpQrSt"}'
  ```

  ```bash CLI
  ant beta:organization:rbac-groups:members add \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn \
    --user-id user_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  member = client.beta.organization.rbac_groups.members.add(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn", user_id="user_01AbCdEfGhIjKlMnOpQrSt"
  )

  print(f"user_id: {member.user_id}")
  print(f"email: {member.email}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const member = await client.beta.organization.rbacGroups.members.add(
    "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
    { user_id: "user_01AbCdEfGhIjKlMnOpQrSt" }
  );

  console.log(`user_id: ${member.user_id}`);
  console.log(`email: ${member.email}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var member = await client.Beta.Organization.RbacGroups.Members.Add(
      "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      new() { UserID = "user_01AbCdEfGhIjKlMnOpQrSt" }
  );

  Console.WriteLine($"user_id: {member.UserID}");
  Console.WriteLine($"email: {member.Email}");
  ```

  ```go Go
  client := anthropic.NewClient()

  member, err := client.Beta.Organization.RBACGroups.Members.Add(
  	context.Background(),
  	"rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  	anthropic.BetaOrganizationRBACGroupMemberAddParams{
  		UserID: "user_01AbCdEfGhIjKlMnOpQrSt",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", member.UserID)
  fmt.Printf("email: %s\n", member.Email)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.members.MemberAddParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberAddParams.builder()
          .userId("user_01AbCdEfGhIjKlMnOpQrSt")
          .build();
      var member = client.beta().organization().rbacGroups().members()
          .add("rbac_group_01UvWxYzAbCdEfGhIjKlMn", params);

      IO.println("user_id: " + member.userId());
      IO.println("email: " + member.email());
  }
  ```

  ```php PHP
  $client = new Client();

  $member = $client->beta->organization->rbacGroups->members->add(
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
  );

  echo "user_id: {$member->userID}\n";
  echo "email: {$member->email}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  member = client.beta.organization.rbac_groups.members.add(
    rbac_group_id,
    user_id: "user_01AbCdEfGhIjKlMnOpQrSt"
  )

  puts "user_id: #{member.user_id}"
  puts "email: #{member.email}"
  ```
</CodeGroup>

```json
{
  "type": "rbac_group_member",
  "rbac_group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "email": "jane@example.com",
  "created_at": "2026-07-09T18:00:00Z"
}
```

### Menghapus anggota dari grup

`DELETE /v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}` menghapus anggota dari grup; mereka tetap menjadi anggota organisasi mereka. Permintaan mengembalikan 404 jika pengguna bukan anggota grup, dan 400 untuk grup `scim`, yang keanggotaannya dikelola di penyedia identitas Anda. Memerlukan scope `write:rbac_groups`.

Untuk detail parameter lengkap dan skema respons, lihat [Menghapus anggota grup](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/remove) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members/user_01AbCdEfGhIjKlMnOpQrSt" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-groups:members remove \
    --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn \
    --user-id user_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_member = client.beta.organization.rbac_groups.members.remove(
      "user_01AbCdEfGhIjKlMnOpQrSt", rbac_group_id="rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  )

  print(f"user_id: {removed_member.user_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedMember = await client.beta.organization.rbacGroups.members.remove(
    "user_01AbCdEfGhIjKlMnOpQrSt",
    { rbac_group_id: "rbac_group_01UvWxYzAbCdEfGhIjKlMn" }
  );

  console.log(`user_id: ${removedMember.user_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedMember = await client.Beta.Organization.RbacGroups.Members.Remove(
      "user_01AbCdEfGhIjKlMnOpQrSt",
      new() { RbacGroupID = "rbac_group_01UvWxYzAbCdEfGhIjKlMn" }
  );

  Console.WriteLine($"user_id: {removedMember.UserID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedMember, err := client.Beta.Organization.RBACGroups.Members.Remove(
  	context.Background(),
  	"user_01AbCdEfGhIjKlMnOpQrSt",
  	anthropic.BetaOrganizationRBACGroupMemberRemoveParams{
  		RBACGroupID: "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", removedMember.UserID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacgroups.members.MemberRemoveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberRemoveParams.builder()
          .rbacGroupId("rbac_group_01UvWxYzAbCdEfGhIjKlMn")
          .build();
      var removedMember = client.beta().organization().rbacGroups().members()
          .remove("user_01AbCdEfGhIjKlMnOpQrSt", params);

      IO.println("user_id: " + removedMember.userId());
  }
  ```

  ```php PHP
  $client = new Client();

  $removedMember = $client->beta->organization->rbacGroups->members->remove(
      userID: 'user_01AbCdEfGhIjKlMnOpQrSt',
      rbacGroupID: 'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
  );

  echo "user_id: {$removedMember->userID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_group_id = "rbac_group_01UvWxYzAbCdEfGhIjKlMn"
  removed_member = client.beta.organization.rbac_groups.members.remove(
    "user_01AbCdEfGhIjKlMnOpQrSt",
    rbac_group_id: rbac_group_id
  )

  puts "user_id: #{removed_member.user_id}"
  ```
</CodeGroup>

```json
{
  "rbac_group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "type": "rbac_group_member_deleted"
}
```

## Peran kustom

Peran kustom bersifat hanya-baca melalui API: endpoint ini mengatalogkan peran kustom organisasi Anda (yang didefinisikan di [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) atau disediakan oleh Anthropic) dan izin yang diberikan setiap peran. Pembacaan peran kustom menggunakan scope `read:members` (tidak ada scope peran terpisah) dan berfungsi dengan kunci tingkat organisasi, dan katalog yang dikembalikan adalah milik organisasi Anda sendiri.

Baca nama peran dari field `display_name`-nya. Untuk peran yang disediakan oleh Anthropic, `display_name` dapat berbeda dari label yang ditampilkan claude.ai, dan Anthropic mungkin mengubah namanya. Untuk menyimpan referensi permanen ke suatu peran, simpan `id`-nya.

### Mendaftar peran

`GET /v1/organizations/rbac_roles` mengembalikan peran kustom organisasi Anda. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar peran](https://platform.claude.com/docs/id/api/beta/organization/rbac_roles/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_roles?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-roles list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  roles = client.beta.organization.rbac_roles.list(limit=20)

  for role in roles:
      print(f"{role.id}: {role.display_name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const roles = await client.beta.organization.rbacRoles.list({ limit: 20 });

  for await (const role of roles) {
    console.log(`${role.id}: ${role.display_name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.RbacRoles.List(new() { Limit = 20 });

  await foreach (var role in page.Paginate())
  {
      Console.WriteLine($"{role.ID}: {role.DisplayName}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  roles := client.Beta.Organization.RBACRoles.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRBACRoleListParams{
  	Limit: anthropic.Int(20),
  })

  for roles.Next() {
  	role := roles.Current()
  	fmt.Printf("%s: %s\n", role.ID, role.DisplayName)
  }
  if err := roles.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacroles.RbacRoleListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RbacRoleListParams.builder()
          .limit(20)
          .build();
      var roles = client.beta().organization().rbacRoles().list(params);

      for (var role : roles.autoPager()) {
          IO.println(role.id() + ": " + role.displayName());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $roles = $client->beta->organization->rbacRoles->list(limit: 20);

  foreach ($roles->pagingEachItem() as $role) {
      echo "{$role->id}: {$role->displayName}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  roles = client.beta.organization.rbac_roles.list(limit: 20)

  roles.auto_paging_each do |role|
    puts "#{role.id}: #{role.display_name}"
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "rbac_role",
      "id": "rbac_role_01CdEfGhIjKlMnOpQrStUv",
      "display_name": "Engineering base",
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Mendapatkan peran

`GET /v1/organizations/rbac_roles/{rbac_role_id}` mengembalikan satu peran berdasarkan ID. Memerlukan scope `read:members`.

Untuk detail parameter lengkap dan skema respons, lihat [Dapatkan peran](https://platform.claude.com/docs/id/api/beta/organization/rbac_roles/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-roles retrieve \
    --rbac-role-id rbac_role_01CdEfGhIjKlMnOpQrStUv
  ```

  ```python Python
  client = anthropic.Anthropic()

  role = client.beta.organization.rbac_roles.retrieve("rbac_role_01CdEfGhIjKlMnOpQrStUv")

  print(f"id: {role.id}")
  print(f"display_name: {role.display_name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const role = await client.beta.organization.rbacRoles.retrieve(
    "rbac_role_01CdEfGhIjKlMnOpQrStUv"
  );

  console.log(`id: ${role.id}`);
  console.log(`display_name: ${role.display_name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var role = await client.Beta.Organization.RbacRoles.Retrieve("rbac_role_01CdEfGhIjKlMnOpQrStUv");

  Console.WriteLine($"id: {role.ID}");
  Console.WriteLine($"display_name: {role.DisplayName}");
  ```

  ```go Go
  client := anthropic.NewClient()

  role, err := client.Beta.Organization.RBACRoles.Get(context.Background(), "rbac_role_01CdEfGhIjKlMnOpQrStUv")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", role.ID)
  fmt.Printf("display_name: %s\n", role.DisplayName)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var role = client.beta().organization().rbacRoles()
      .retrieve("rbac_role_01CdEfGhIjKlMnOpQrStUv");

  IO.println("id: " + role.id());
  IO.println("display_name: " + role.displayName());
  ```

  ```php PHP
  $client = new Client();

  $role = $client->beta->organization->rbacRoles->retrieve(
      rbacRoleID: 'rbac_role_01CdEfGhIjKlMnOpQrStUv',
  );

  echo "id: {$role->id}\n";
  echo "display_name: {$role->displayName}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_role_id = "rbac_role_01CdEfGhIjKlMnOpQrStUv"
  role = client.beta.organization.rbac_roles.retrieve(rbac_role_id)

  puts "id: #{role.id}"
  puts "display_name: #{role.display_name}"
  ```
</CodeGroup>

### Mendaftar izin peran

`GET /v1/organizations/rbac_roles/{rbac_role_id}/permissions` mengembalikan izin peran. Setiap izin memasangkan `resource` (tempat izin berlaku: fitur produk organisasi, alat konektor, scope OAuth konektor, satu konektor, atau setiap konektor) dengan `action` (apa yang diberikan pada sumber daya tersebut). Baris untuk fitur yang tidak diaktifkan untuk organisasi Anda dihilangkan, sehingga satu halaman mungkin berisi lebih sedikit dari `limit` baris sementara `has_more` bernilai `true`. Memerlukan scope `read:members`.

Dua nilai `action` memerlukan perhatian khusus. Izin `organization` yang action-nya adalah `capability_access_all` (setiap fitur produk) atau `capability_access_all_ga` (setiap fitur produk yang stabil, yaitu setiap fitur yang tidak berlabel beta atau pratinjau riset) merupakan pemberian menyeluruh. Izin ini dicantumkan sebagai satu baris tersebut alih-alih diuraikan. Pemberian menyeluruh tidak mencakup akses model maupun izin panel admin berawalan `permission_`, maupun `inference_hooks_inspection`, yang hanya dimiliki suatu peran melalui baris yang menyebutkannya. Saat Anda menghitung apa yang diberikan suatu peran, perlakukan baris menyeluruh sebagai mencakup semua yang dijelaskan variannya, bukan hanya fitur yang disebutkan di baris lain.

Untuk detail parameter lengkap dan skema respons, lihat [Daftar izin peran](https://platform.claude.com/docs/id/api/beta/organization/rbac_roles/permissions/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv/permissions?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21"
  ```

  ```bash CLI
  ant beta:organization:rbac-roles:permissions list \
    --rbac-role-id rbac_role_01CdEfGhIjKlMnOpQrStUv \
    --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  permissions = client.beta.organization.rbac_roles.permissions.list(
      "rbac_role_01CdEfGhIjKlMnOpQrStUv", limit=20
  )

  for permission in permissions:
      print(permission.action)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const permissions = await client.beta.organization.rbacRoles.permissions.list(
    "rbac_role_01CdEfGhIjKlMnOpQrStUv",
    { limit: 20 }
  );

  for await (const permission of permissions) {
    console.log(permission.action);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.RbacRoles.Permissions.List(
      "rbac_role_01CdEfGhIjKlMnOpQrStUv",
      new() { Limit = 20 }
  );

  await foreach (var permission in page.Paginate())
  {
      Console.WriteLine(permission.Action);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  permissions := client.Beta.Organization.RBACRoles.Permissions.ListAutoPaging(
  	context.Background(),
  	"rbac_role_01CdEfGhIjKlMnOpQrStUv",
  	anthropic.BetaOrganizationRBACRolePermissionListParams{
  		Limit: anthropic.Int(20),
  	},
  )

  for permissions.Next() {
  	permission := permissions.Current()
  	fmt.Println(permission.Action)
  }
  if err := permissions.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.rbacroles.permissions.PermissionListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = PermissionListParams.builder()
          .limit(20)
          .build();
      var permissions = client.beta().organization().rbacRoles().permissions()
          .list("rbac_role_01CdEfGhIjKlMnOpQrStUv", params);

      for (var permission : permissions.autoPager()) {
          IO.println(permission.action());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $permissions = $client->beta->organization->rbacRoles->permissions->list(
      rbacRoleID: 'rbac_role_01CdEfGhIjKlMnOpQrStUv',
      limit: 20,
  );

  foreach ($permissions->pagingEachItem() as $permission) {
      echo "{$permission->action}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rbac_role_id = "rbac_role_01CdEfGhIjKlMnOpQrStUv"
  permissions = client.beta.organization.rbac_roles.permissions.list(rbac_role_id, limit: 20)

  permissions.auto_paging_each do |permission|
    puts permission.action
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "organization",
        "organization_id": "12345678-1234-5678-1234-567812345678"
      },
      "action": "capability_access_all_ga"
    },
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "connector_tool",
        "connector_id": "mcpsrv_01WxYzAbCdEfGhIjKlMnOp",
        "tool_name": "search_tickets"
      },
      "action": "use"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Contoh alur kerja

### Offboarding karyawan yang keluar

1. Cari anggota berdasarkan email:

   <CodeGroup>
     ```bash cURL
     curl "https://api.anthropic.com/v1/organizations/users?email=departing@example.com" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2026-10-21"
     ```

     ```bash CLI
     ant organization:users list --email departing@example.com
     ```

     ```python Python
     client = anthropic.Anthropic()

     users = client.organization.users.list(email="departing@example.com")

     for user in users:
         print(f"{user.id}: {user.email} ({user.role})")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const users = await client.organization.users.list({ email: "departing@example.com" });

     for await (const user of users) {
       console.log(`${user.id}: ${user.email} (${user.role})`);
     }
     ```

     ```csharp C#
     AnthropicClient client = new();

     var page = await client.Organization.Users.List(new() { Email = "departing@example.com" });

     await foreach (var user in page.Paginate())
     {
         Console.WriteLine($"{user.ID}: {user.Email} ({user.Role.Raw()})");
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     users := client.Organization.Users.ListAutoPaging(context.Background(), anthropic.OrganizationUserListParams{
     	Email: anthropic.String("departing@example.com"),
     })

     for users.Next() {
     	user := users.Current()
     	fmt.Printf("%s: %s (%s)\n", user.ID, user.Email, user.Role)
     }
     if err := users.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.organization.users.UserListParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = UserListParams.builder()
             .email("departing@example.com")
             .build();
         var users = client.organization().users().list(params);

         for (var user : users.autoPager()) {
             IO.println(user.id() + ": " + user.email() + " (" + user.role().asString() + ")");
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $users = $client->organization->users->list(email: 'departing@example.com');

     foreach ($users->pagingEachItem() as $user) {
         echo "{$user->id}: {$user->email} ({$user->role})\n";
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     users = client.organization.users.list(email: "departing@example.com")

     users.auto_paging_each do |user|
       puts "#{user.id}: #{user.email} (#{user.role})"
     end
     ```
   </CodeGroup>

2. Hapus mereka dengan `DELETE /v1/organizations/users/{user_id}`, menggunakan `id` dari respons. Kursi mereka, jika ada, kembali ke kumpulan.

3. Jika orang tersebut belum bergabung, pencarian tidak mengembalikan anggota; daftarkan undangan dan tarik undangan `pending` mereka sebagai gantinya.

### Menanggapi perangkat yang hilang atau dicuri

Sebelum Anda membutuhkan alur kerja ini, buat kunci dengan scope `write:members` dan `read:members` untuk [endpoint pengeluaran sesi](https://platform.claude.com/docs/id/manage-claude/user-management#sign-a-member-out-everywhere). Jika Anda belum memiliki kunci, seorang pemilik dapat menggunakan tindakan **Keluar dari semua perangkat** di halaman Anggota pada [pengaturan organisasi claude.ai](https://claude.ai/admin-settings) sebagai pengganti langkah 2 hingga 4. Pemilik tidak dapat menggunakannya pada akunnya sendiri: mereka mengeluarkan sesi mereka sendiri dari pengaturan akun mereka di claude.ai.

1. Pertama, keluarkan orang tersebut dari penyedia identitas Anda, atau nonaktifkan akun mereka di sana. Jika tidak, siapa pun yang memegang perangkat yang hilang dapat masuk ke Claude lagi melalui sesi penyedia identitas di perangkat tersebut atau kotak surat orang tersebut.

2. Cari anggota berdasarkan alamat email, seperti pada langkah 1 di [Offboarding karyawan yang keluar](https://platform.claude.com/docs/id/manage-claude/user-management#offboard-a-departing-employee). Pencocokan email menoleransi varian dari alamat yang sama, jadi periksa apakah respons tersebut adalah orang yang tepat.

3. Keluarkan mereka dengan `POST /v1/organizations/users/{user_id}/sign_out`, menggunakan `id` dari respons. [Mengeluarkan anggota dari semua sesi di mana saja](https://platform.claude.com/docs/id/manage-claude/user-management#sign-a-member-out-everywhere) mencantumkan header yang diperlukan permintaan dan apa yang diakhirinya.

4. Jika permintaan mengembalikan 503, kirim lagi hingga mengembalikan 200. Jika mengembalikan 400 dengan `cannot_sign_out_primary_owner`, lihat [Siapa yang tidak dapat Anda keluarkan](https://platform.claude.com/docs/id/manage-claude/user-management#who-you-cant-sign-out).

5. Periksa [ekspor log audit](https://platform.claude.com/docs/id/manage-claude/compliance-api#export-audit-logs) atau [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) untuk proses masuk setelah permintaan pertama. Jika Anda menemukannya, atau orang tersebut sedang masuk ke aplikasi seperti Claude Code, kirim permintaan lagi setelah 5 menit. Jika Anda tidak dapat mengirim permintaan, gunakan tindakan **Keluar dari semua perangkat** lagi sebagai gantinya. Ini juga mengeluarkan anggota dari sesi apa pun yang telah mereka mulai sejak saat itu, jadi beri tahu mereka terlebih dahulu.

6. Konfirmasikan pengeluaran sesi [di tempat pencatatannya](https://platform.claude.com/docs/id/manage-claude/user-management#where-the-sign-out-is-recorded), dan tinjau [apa yang tidak diakhiri oleh permintaan ini](https://platform.claude.com/docs/id/manage-claude/user-management#what-the-request-doesnt-end).

### Mengaudit keanggotaan grup

1. Tampilkan daftar grup dan catat `id`, `name`, dan `role_ids` setiap grup.

2. Untuk setiap grup yang membawa peran sensitif, telusuri halaman `GET /v1/organizations/rbac_groups/{rbac_group_id}/members` dan bandingkan email anggota dengan daftar di penyedia identitas Anda.

3. Hapus anggota yang seharusnya tidak lagi berada di grup dengan `DELETE /v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}`. Untuk grup `scim`, lakukan perubahan di penyedia identitas Anda sebagai gantinya.

Untuk alur kerja yang menggabungkan keanggotaan grup dengan kenaikan batas pengeluaran sementara, lihat [Menaikkan sementara batas pengeluaran anggota selama insiden](https://platform.claude.com/docs/id/manage-claude/spend-limits-api#temporarily-raise-a-members-spend-limit-during-an-incident) di halaman Spend Limits API.

## Pertanyaan yang sering diajukan

### Apakah ini API yang berbeda dari Admin API?

Tidak. Endpoint anggota dan undangan adalah endpoint `/v1/organizations/` yang sama yang digunakan organisasi Claude Console; halaman ini mendokumentasikan perilakunya di Claude Enterprise. Endpoint grup dan peran kustom adalah bagian dari API yang sama dan hanya ada untuk organisasi Claude Enterprise. [Tabel ketersediaan](https://platform.claude.com/docs/id/manage-claude/user-management#which-endpoints-can-your-organization-use) menunjukkan endpoint mana yang dapat dipanggil oleh setiap jenis organisasi.

### Dapatkah API menetapkan peran owner atau admin keanggotaan?

Tidak. API hanya menetapkan `user` dan `managed`, saat pembuatan undangan dan pembaruan peran. Peran administratif ditetapkan di pengaturan organisasi claude.ai, dan anggota yang memegangnya tidak dapat diubah atau dihapus melalui API.

### Dapatkah API membuat atau mengubah grup?

Ya, dengan scope `write:rbac_groups`: buat, ganti nama, dan hapus grup, serta tambahkan atau hapus anggotanya. Dua hal yang tidak dapat diubah oleh API: grup yang disediakan oleh penyedia identitas Anda (`source_type: "scim"`), yang nama dan keanggotaannya dimiliki oleh penyedia identitas, dan [peran kustom](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles), yang dikelola di pengaturan organisasi claude.ai (API hanya membacanya).

### Apakah undangan yang belum diterima menggunakan kursi?

Pada paket dengan kumpulan kursi terbatas, ya: undangan `pending` menahan satu kursi. Menarik undangan atau membiarkannya kedaluwarsa akan membebaskan kursi tersebut. Pada paket tanpa kumpulan kursi, undangan tidak menggunakan apa pun.

### Operasi mana yang berfungsi saat organisasi Anda menggunakan single sign-on?

Jika penyedia identitas Anda menyediakan pengguna secara otomatis (JIT atau SCIM), pembuatan undangan mengembalikan 400. Jika penyedia identitas mengelola peran (SSO lanjutan atau penyediaan SCIM lanjutan), pembaruan peran mengembalikan 400. Jika penyedia identitas mengelola keanggotaan (penyediaan SCIM), penghapusan anggota mengembalikan 400. Operasi baca tetap berfungsi. Begitu pula [mengeluarkan anggota dari semua sesi di mana pun](https://platform.claude.com/docs/id/manage-claude/user-management#sign-a-member-out-everywhere), apa pun mode single sign-on yang digunakan organisasi Anda.

### Apakah mengeluarkan anggota mencegah mereka masuk kembali?

Tidak. [Mengeluarkan anggota](https://platform.claude.com/docs/id/manage-claude/user-management#sign-a-member-out-everywhere) mengakhiri sesi masuk, perangkat tepercaya, dan token OAuth mereka untuk organisasi Anda, tetapi mereka dapat masuk kembali saat itu juga. Untuk mencegah seseorang masuk, [hapus mereka](https://platform.claude.com/docs/id/manage-claude/user-management#remove-a-member) atau, jika organisasi Anda mewajibkan single sign-on, nonaktifkan akun mereka di penyedia identitas Anda. Menonaktifkan akun saja mungkin tidak mengakhiri sesi yang sudah terbuka, jadi pertama-tama keluarkan orang tersebut dari penyedia identitas Anda, lalu keluarkan mereka dari Claude, kemudian hapus mereka atau nonaktifkan akun mereka.

### Apa yang terjadi pada kunci Admin API ketika orang yang membuatnya keluar?

Kunci tetap berfungsi. Kunci Admin API dicakup ke organisasi, bukan ke pengguna individu, dan kunci yang dibuat di claude.ai tidak kedaluwarsa. Menghapus pembuatnya dari organisasi atau mencabut penyediaannya melalui penyedia identitas Anda mengakhiri akses mereka sendiri, tetapi tidak mengakhiri kunci yang mereka buat. Menurunkan peran mereka juga tidak mengubah kunci: setiap kunci tetap aktif dengan scope aslinya. Saat Anda melakukan offboarding terhadap seseorang yang membuat kunci Admin API, hapus kunci tersebut di bagian **Kunci** pada [claude.ai > Pengaturan organisasi > API](https://claude.ai/admin-settings/api-access) dan buat penggantinya.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Membuat kunci Admin API" href="https://platform.claude.com/docs/id/manage-claude/admin-api-keys">
    Tempat membuat kunci dengan scope dan scope mana yang harus dipilih.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-api">
    Audit aktivitas serta ambil atau hapus konten pengguna di seluruh organisasi Anda.
  </Card>

  <Card title="Usage and Cost Analytics API" href="https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api">
    Lacak penggunaan token dan biaya untuk organisasi Anda.
  </Card>

  <Card title="Spend Limits API" href="https://platform.claude.com/docs/id/manage-claude/spend-limits-api">
    Tetapkan batas pengeluaran per anggota dan tinjau permintaan kenaikan.
  </Card>
</CardGroup>
