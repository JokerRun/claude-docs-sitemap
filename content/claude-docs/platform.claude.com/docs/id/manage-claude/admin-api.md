---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/admin-api
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: ece205f1ab65547bd9bf031c2ec6cd31f0da4277aa46fda36e6927bcc7755db7
---

---
title: Admin API
url: https://platform.claude.com/docs/id/manage-claude/admin-api
description: Kelola anggota organisasi, workspace, undangan, dan kunci API secara terprogram dengan Admin API, menggunakan kunci Admin API, token OAuth `org:admin`, atau kunci personal maupun kunci service account.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, siapkan organisasi Anda di **Console → Settings → Organization**.
</Tip>

[Admin API](https://platform.claude.com/docs/id/api/admin) memungkinkan Anda mengelola anggota, workspace, undangan, dan kunci API organisasi Anda secara terprogram alih-alih secara manual di [Claude Console](https://platform.claude.com/).

<Check>
  **Admin API memerlukan akses khusus**

  Admin API menerima tiga jenis kredensial:

  * **Kunci Admin API** (diawali dengan `sk-ant-admin...`) yang dikirim dalam header `x-api-key`. Hanya anggota organisasi dengan peran admin yang dapat membuatnya. Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).
  * **Token bearer OAuth** dengan scope `org:admin` yang dikirim dalam header `authorization: Bearer`. Hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperolehnya. Lihat [Memperoleh token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token).
  * **Kunci personal** atau **kunci service account** yang tidak dibatasi pada workspace tertentu, dikirim dalam header `x-api-key`. Kunci tersebut memiliki izin yang sama dengan akun yang tertaut. Lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types).
</Check>

<Note>
  **Claude Enterprise:** Organisasi Claude Enterprise (claude.ai) memanggil Admin API dengan kunci API ber-scope yang dibuat di claude.ai. Dari halaman ini, hanya endpoint anggota dan undangan yang berlaku untuk mereka. Mereka juga mendapatkan endpoint khusus Enterprise: pembacaan grup dan peran kustom, serta [batas pengeluaran](https://platform.claude.com/docs/id/manage-claude/spend-limits-api). Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management).
</Note>

<Note>
  **Claude Platform on AWS:** Hanya endpoint workspace (create, get, list, update, dan archive pada `/v1/organizations/workspaces`) dan endpoint external key (register, get, list, update, dan delete pada `/v1/organizations/external_keys`, untuk [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek-aws-kms#claude-platform-on-aws); tidak ada endpoint validate, karena kunci divalidasi saat dilampirkan ke workspace) yang tersedia di Claude Platform on AWS. Anggota organisasi, anggota workspace, undangan, kunci API, serta laporan penggunaan, biaya, dan batas laju tidak tersedia. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

## Autentikasi

Lakukan autentikasi dengan salah satu dari tiga kredensial tersebut. Kunci Admin API mencakup sebagian besar endpoint. Endpoint service-account, federation-issuer, dan federation-rule hanya menerima token OAuth `org:admin`. Kirim kunci personal atau kunci service account dalam header `x-api-key`, sama seperti kunci Admin API. Contoh berikut memanggil [endpoint info organisasi](https://platform.claude.com/docs/id/manage-claude/admin-api#accessing-organization-info) dengan token OAuth dan dengan kunci Admin API.

SDK Python, TypeScript, C#, Go, Java, PHP, dan Ruby mengekspos Admin API di bawah `client.beta.organization`, dan CLI `ant` di bawah `ant beta:organization`. Contoh di halaman ini menggunakan client default, yang membaca kunci Admin API dari `ANTHROPIC_API_KEY` atau token bearer OAuth dari `ANTHROPIC_AUTH_TOKEN`. Metode list SDK di Python, TypeScript, C#, Go, dan Java mengembalikan iterator yang mengambil halaman tambahan sesuai permintaan, sehingga `limit` menetapkan ukuran halaman, bukan total. Contoh PHP, Ruby, dan curl mengembalikan satu halaman. Di CLI, `--limit` membatasi hasil pada daftar anggota, undangan, workspace, anggota workspace, dan kunci API. Untuk parameter dan respons setiap endpoint, lihat [referensi Admin API](https://platform.claude.com/docs/id/api/admin).

### Token bearer OAuth

Login dengan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) menggunakan profil khusus dengan scope `org:admin` (lihat [Akses admin](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor token bearer. `--profile admin` menyimpan kredensial `org:admin` di bawah profilnya sendiri dan menjadikannya profil aktif CLI. Variabel yang diekspor berlaku untuk setiap panggilan SDK dan CLI di shell tersebut. Gunakan shell yang Anda khususkan untuk administrasi, hapus variabel tersebut setelah selesai, dan kembalikan CLI dengan `ant profile activate default`:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_AUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek. Jika permintaan mulai mengembalikan 401, jalankan kembali perintah `export` untuk memperbarui token.

SDK dan CLI `ant` membaca `ANTHROPIC_AUTH_TOKEN` secara otomatis. Biarkan `ANTHROPIC_API_KEY` tidak diatur di shell yang sama agar keduanya mengirim token bearer. Beban kerja otomatis melewati proses login: mereka melakukan autentikasi melalui workload identity federation, dan SDK serta CLI melakukan pertukaran token dari variabel lingkungan federation. Lihat [Bootstrap beban kerja untuk mengelola WIF](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#bootstrap-a-workload-to-manage-wif).

Panggil Admin API dengan token yang telah diekspor:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization retrieve
  ```

  ```python Python
  client = anthropic.Anthropic()

  organization = client.beta.organization.retrieve()

  print(f"id: {organization.id}")
  print(f"name: {organization.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const organization = await client.beta.organization.retrieve();

  console.log(`id: ${organization.id}`);
  console.log(`name: ${organization.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var organization = await client.Beta.Organization.Retrieve();

  Console.WriteLine($"id: {organization.ID}");
  Console.WriteLine($"name: {organization.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  organization, err := client.Beta.Organization.Get(context.Background())
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", organization.ID)
  fmt.Printf("name: %s\n", organization.Name)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var organization = client.beta().organization().retrieve();

  IO.println("id: " + organization.id());
  IO.println("name: " + organization.name());
  ```

  ```php PHP
  $client = new Client();

  $organization = $client->beta->organization->retrieve();

  echo "id: {$organization->id}\n";
  echo "name: {$organization->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  organization = client.beta.organization.retrieve

  puts "id: #{organization.id}"
  puts "name: #{organization.name}"
  ```
</CodeGroup>

Token `org:admin` memberikan akses ke seluruh organisasi, terlepas dari workspace tempat profil yang mendasarinya atau [federation rule](https://platform.claude.com/docs/id/manage-claude/admin-api#federation-rules) terikat.

Untuk CI dan beban kerja non-interaktif lainnya, buat token dengan Workload Identity Federation alih-alih login secara interaktif. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#workload-ci-and-automation).

### Kunci Admin API

Untuk membuat kunci Admin API sesuai jenis organisasi Anda, lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys).

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization retrieve
  ```

  ```python Python
  client = anthropic.Anthropic()

  organization = client.beta.organization.retrieve()

  print(f"id: {organization.id}")
  print(f"name: {organization.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const organization = await client.beta.organization.retrieve();

  console.log(`id: ${organization.id}`);
  console.log(`name: ${organization.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var organization = await client.Beta.Organization.Retrieve();

  Console.WriteLine($"id: {organization.ID}");
  Console.WriteLine($"name: {organization.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  organization, err := client.Beta.Organization.Get(context.Background())
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", organization.ID)
  fmt.Printf("name: %s\n", organization.Name)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var organization = client.beta().organization().retrieve();

  IO.println("id: " + organization.id());
  IO.println("name: " + organization.name());
  ```

  ```php PHP
  $client = new Client();

  $organization = $client->beta->organization->retrieve();

  echo "id: {$organization->id}\n";
  echo "name: {$organization->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  organization = client.beta.organization.retrieve

  puts "id: #{organization.id}"
  puts "name: #{organization.name}"
  ```
</CodeGroup>

## Cara kerja Admin API

Lakukan autentikasi dengan kredensial apa pun dari [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication), lalu kelola sumber daya berikut:

* Anggota organisasi dan perannya
* Undangan organisasi
* Workspace dan anggotanya
* Kunci API
* Service account, federation issuer, dan federation rule (hanya token OAuth `org:admin`)

Penggunaan umum mencakup otomatisasi onboarding dan offboarding, pengelolaan akses workspace, dan audit kunci API.

## Peran dan izin organisasi

Ada lima peran tingkat organisasi. Untuk detailnya, lihat [Peran dan izin API Console](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions).

| Peran              | Izin                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------- |
| user               | Dapat menggunakan playground                                                             |
| claude\_code\_user | Dapat menggunakan playground dan [Claude Code](https://code.claude.com/docs/en/overview) |
| developer          | Dapat menggunakan playground dan mengelola kunci API                                     |
| billing            | Dapat menggunakan playground dan mengelola detail penagihan                              |
| admin              | Dapat melakukan semua hal di atas, ditambah mengelola pengguna                           |

Owner dan primary owner organisasi memiliki semua izin admin dan juga dapat mengelola admin. Semua rujukan ke peran admin di halaman ini juga berlaku untuk owner dan primary owner.

## Konsep utama

### Anggota organisasi

Daftarkan [anggota organisasi](https://platform.claude.com/docs/id/api/admin-api/users/get-user), perbarui perannya, dan hapus mereka.

Daftarkan anggota organisasi Anda:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/users?limit=10" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:users list --limit 10
  ```

  ```python Python
  client = anthropic.Anthropic()

  users = client.beta.organization.users.list(limit=10)

  # Secara otomatis mengambil halaman lainnya sesuai kebutuhan.
  for user in users:
      print(f"{user.id}: {user.email} ({user.role})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const users = await client.beta.organization.users.list({ limit: 10 });

  for await (const user of users) {
    console.log(`${user.id}: ${user.email} (${user.role})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Users.List(new() { Limit = 10 });

  await foreach (var user in page.Paginate())
  {
      Console.WriteLine($"{user.ID}: {user.Email} ({user.Role.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  users := client.Beta.Organization.Users.ListAutoPaging(context.Background(), anthropic.BetaOrganizationUserListParams{
  	Limit: anthropic.Int(10),
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
  import com.anthropic.models.beta.organization.users.UserListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserListParams.builder()
          .limit(10)
          .build();
      var users = client.beta().organization().users().list(params);

      for (var user : users.autoPager()) {
          IO.println(user.id() + ": " + user.email() + " (" + user.role().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $users = $client->beta->organization->users->list(limit: 10);

  foreach ($users->getItems() as $user) {
      echo "{$user->id}: {$user->email} ({$user->role})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  users = client.beta.organization.users.list(limit: 10)

  users.data.each do |user|
    puts "#{user.id}: #{user.email} (#{user.role})"
  end
  ```
</CodeGroup>

Perbarui peran anggota:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/users/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"role": "developer"}'
  ```

  ```bash CLI
  ant beta:organization:users update \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --role developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  user = client.beta.organization.users.update(
      "user_01XyDMpzjS89pFZXqSFUBDr6", role="developer"
  )

  print(f"id: {user.id}")
  print(f"role: {user.role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const user = await client.beta.organization.users.update("user_01XyDMpzjS89pFZXqSFUBDr6", {
    role: "developer"
  });

  console.log(`id: ${user.id}`);
  console.log(`role: ${user.role}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Users;
  // ...

  AnthropicClient client = new();

  var user = await client.Beta.Organization.Users.Update(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      new() { Role = Role.Developer }
  );

  Console.WriteLine($"id: {user.ID}");
  Console.WriteLine($"role: {user.Role.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  user, err := client.Beta.Organization.Users.Update(
  	context.Background(),
  	"user_01XyDMpzjS89pFZXqSFUBDr6",
  	anthropic.BetaOrganizationUserUpdateParams{
  		Role: anthropic.BetaOrganizationUserUpdateParamsRoleDeveloper,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", user.ID)
  fmt.Printf("role: %s\n", user.Role)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.users.UserUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserUpdateParams.builder()
          .role(UserUpdateParams.Role.DEVELOPER)
          .build();
      var user = client.beta().organization().users()
          .update("user_01XyDMpzjS89pFZXqSFUBDr6", params);

      IO.println("id: " + user.id());
      IO.println("role: " + user.role().asString());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Users\UserUpdateParams\Role;
  // ...

  $client = new Client();

  $user = $client->beta->organization->users->update(
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
      role: Role::DEVELOPER,
  );

  echo "id: {$user->id}\n";
  echo "role: {$user->role}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01XyDMpzjS89pFZXqSFUBDr6"
  user = client.beta.organization.users.update(user_id, role: :developer)

  puts "id: #{user.id}"
  puts "role: #{user.role}"
  ```
</CodeGroup>

Hapus anggota dari organisasi:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/users/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:users remove --user-id user_01XyDMpzjS89pFZXqSFUBDr6
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_user = client.beta.organization.users.remove("user_01XyDMpzjS89pFZXqSFUBDr6")

  print(f"id: {removed_user.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedUser = await client.beta.organization.users.remove(
    "user_01XyDMpzjS89pFZXqSFUBDr6"
  );

  console.log(`id: ${removedUser.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedUser = await client.Beta.Organization.Users.Remove("user_01XyDMpzjS89pFZXqSFUBDr6");

  Console.WriteLine($"id: {removedUser.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedUser, err := client.Beta.Organization.Users.Remove(context.Background(), "user_01XyDMpzjS89pFZXqSFUBDr6")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", removedUser.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var removedUser = client.beta().organization().users()
      .remove("user_01XyDMpzjS89pFZXqSFUBDr6");

  IO.println("id: " + removedUser.id());
  ```

  ```php PHP
  $client = new Client();

  $removedUser = $client->beta->organization->users->remove(
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
  );

  echo "id: {$removedUser->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01XyDMpzjS89pFZXqSFUBDr6"
  removed_user = client.beta.organization.users.remove(user_id)

  puts "id: #{removed_user.id}"
  ```
</CodeGroup>

### Undangan organisasi

Undang pengguna ke organisasi Anda dan kelola [undangan](https://platform.claude.com/docs/id/api/admin-api/invites/get-invite) yang tertunda.

Undang pengguna ke organisasi Anda:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/invites" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "email": "user@example.com",
      "role": "developer"
    }'
  ```

  ```bash CLI
  ant beta:organization:invites create --email user@example.com --role developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  invite = client.beta.organization.invites.create(
      email="user@example.com", role="developer"
  )

  print(f"id: {invite.id}")
  print(f"email: {invite.email}")
  print(f"status: {invite.status}")
  print(f"expires_at: {invite.expires_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const invite = await client.beta.organization.invites.create({
    email: "user@example.com",
    role: "developer"
  });

  console.log(`id: ${invite.id}`);
  console.log(`email: ${invite.email}`);
  console.log(`status: ${invite.status}`);
  console.log(`expires_at: ${invite.expires_at}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Invites;
  // ...

  AnthropicClient client = new();

  var invite = await client.Beta.Organization.Invites.Create(new()
  {
      Email = "user@example.com",
      Role = Role.Developer
  });

  Console.WriteLine($"id: {invite.ID}");
  Console.WriteLine($"email: {invite.Email}");
  Console.WriteLine($"status: {invite.Status.Raw()}");
  Console.WriteLine($"expires_at: {invite.ExpiresAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  invite, err := client.Beta.Organization.Invites.New(context.Background(), anthropic.BetaOrganizationInviteNewParams{
  	Email: "user@example.com",
  	Role:  anthropic.BetaOrganizationInviteNewParamsRoleDeveloper,
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
  import com.anthropic.models.beta.organization.invites.InviteCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InviteCreateParams.builder()
          .email("user@example.com")
          .role(InviteCreateParams.Role.DEVELOPER)
          .build();
      var invite = client.beta().organization().invites().create(params);

      IO.println("id: " + invite.id());
      IO.println("email: " + invite.email());
      IO.println("status: " + invite.status().asString());
      IO.println("expires_at: " + invite.expiresAt());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Invites\InviteCreateParams\Role;
  // ...

  $client = new Client();

  $invite = $client->beta->organization->invites->create(
      email: 'user@example.com',
      role: Role::DEVELOPER,
  );

  echo "id: {$invite->id}\n";
  echo "email: {$invite->email}\n";
  echo "status: {$invite->status}\n";
  echo "expires_at: {$invite->expiresAt->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invite = client.beta.organization.invites.create(email: "user@example.com", role: :developer)

  puts "id: #{invite.id}"
  puts "email: #{invite.email}"
  puts "status: #{invite.status}"
  puts "expires_at: #{invite.expires_at.iso8601}"
  ```
</CodeGroup>

Daftarkan undangan yang tertunda:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/invites?limit=10" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:invites list --limit 10
  ```

  ```python Python
  client = anthropic.Anthropic()

  invites = client.beta.organization.invites.list(limit=10)

  # Secara otomatis mengambil halaman tambahan sesuai kebutuhan.
  for invite in invites:
      print(f"{invite.id}: {invite.email} ({invite.status})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const invites = await client.beta.organization.invites.list({ limit: 10 });

  for await (const invite of invites) {
    console.log(`${invite.id}: ${invite.email} (${invite.status})`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Invites.List(new() { Limit = 10 });

  await foreach (var invite in page.Paginate())
  {
      Console.WriteLine($"{invite.ID}: {invite.Email} ({invite.Status.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  invites := client.Beta.Organization.Invites.ListAutoPaging(context.Background(), anthropic.BetaOrganizationInviteListParams{
  	Limit: anthropic.Int(10),
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
  import com.anthropic.models.beta.organization.invites.InviteListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = InviteListParams.builder()
          .limit(10)
          .build();
      var invites = client.beta().organization().invites().list(params);

      for (var invite : invites.autoPager()) {
          IO.println(invite.id() + ": " + invite.email() + " (" + invite.status().asString() + ")");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $invites = $client->beta->organization->invites->list(limit: 10);

  foreach ($invites->getItems() as $invite) {
      echo "{$invite->id}: {$invite->email} ({$invite->status})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invites = client.beta.organization.invites.list(limit: 10)

  invites.data.each do |invite|
    puts "#{invite.id}: #{invite.email} (#{invite.status})"
  end
  ```
</CodeGroup>

Hapus undangan:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/invites/invite_015gWxHNr6h6TdRPZTmuCGnn" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:invites delete --invite-id invite_015gWxHNr6h6TdRPZTmuCGnn
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_invite = client.beta.organization.invites.delete(
      "invite_015gWxHNr6h6TdRPZTmuCGnn"
  )

  print(f"id: {deleted_invite.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedInvite = await client.beta.organization.invites.delete(
    "invite_015gWxHNr6h6TdRPZTmuCGnn"
  );

  console.log(`id: ${deletedInvite.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedInvite = await client.Beta.Organization.Invites.Delete(
      "invite_015gWxHNr6h6TdRPZTmuCGnn"
  );

  Console.WriteLine($"id: {deletedInvite.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedInvite, err := client.Beta.Organization.Invites.Delete(context.Background(), "invite_015gWxHNr6h6TdRPZTmuCGnn")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deletedInvite.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedInvite = client.beta().organization().invites()
      .delete("invite_015gWxHNr6h6TdRPZTmuCGnn");

  IO.println("id: " + deletedInvite.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedInvite = $client->beta->organization->invites->delete(
      inviteID: 'invite_015gWxHNr6h6TdRPZTmuCGnn',
  );

  echo "id: {$deletedInvite->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  invite_id = "invite_015gWxHNr6h6TdRPZTmuCGnn"
  deleted_invite = client.beta.organization.invites.delete(invite_id)

  puts "id: #{deleted_invite.id}"
  ```
</CodeGroup>

### Workspace

Lihat [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces) untuk contoh Console dan API.

### Anggota workspace

Kelola [akses pengguna ke workspace tertentu](https://platform.claude.com/docs/id/api/admin-api/workspace_members/get-workspace-member):

Tambahkan anggota ke workspace:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "user_id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "workspace_role": "workspace_developer"
    }'
  ```

  ```bash CLI
  ant beta:organization:workspaces:members add \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-role workspace_developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  member = client.beta.organization.workspaces.members.add(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      user_id="user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_role="workspace_developer",
  )

  print(f"user_id: {member.user_id}")
  print(f"workspace_role: {member.workspace_role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const member = await client.beta.organization.workspaces.members.add(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    {
      user_id: "user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_role: "workspace_developer"
    }
  );

  console.log(`user_id: ${member.user_id}`);
  console.log(`workspace_role: ${member.workspace_role}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Workspaces;

  AnthropicClient client = new();

  var member = await client.Beta.Organization.Workspaces.Members.Add(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new()
      {
          UserID = "user_01XyDMpzjS89pFZXqSFUBDr6",
          WorkspaceRole = BetaNoBillingWorkspaceRole.WorkspaceDeveloper
      }
  );

  Console.WriteLine($"user_id: {member.UserID}");
  Console.WriteLine($"workspace_role: {member.WorkspaceRole.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  member, err := client.Beta.Organization.Workspaces.Members.Add(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.BetaOrganizationWorkspaceMemberAddParams{
  		UserID:        "user_01XyDMpzjS89pFZXqSFUBDr6",
  		WorkspaceRole: anthropic.BetaNoBillingWorkspaceRoleWorkspaceDeveloper,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", member.UserID)
  fmt.Printf("workspace_role: %s\n", member.WorkspaceRole)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.BetaNoBillingWorkspaceRole;
  import com.anthropic.models.beta.organization.workspaces.members.MemberAddParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberAddParams.builder()
          .userId("user_01XyDMpzjS89pFZXqSFUBDr6")
          .workspaceRole(BetaNoBillingWorkspaceRole.WORKSPACE_DEVELOPER)
          .build();
      var member = client.beta().organization().workspaces().members()
          .add("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      IO.println("user_id: " + member.userId());
      IO.println("workspace_role: " + member.workspaceRole().asString());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Workspaces\NoBillingWorkspaceRole;
  // ...

  $client = new Client();

  $member = $client->beta->organization->workspaces->members->add(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
      workspaceRole: NoBillingWorkspaceRole::WORKSPACE_DEVELOPER,
  );

  echo "user_id: {$member->userID}\n";
  echo "workspace_role: {$member->workspaceRole}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  member = client.beta.organization.workspaces.members.add(
    workspace_id,
    user_id: "user_01XyDMpzjS89pFZXqSFUBDr6",
    workspace_role: :workspace_developer
  )

  puts "user_id: #{member.user_id}"
  puts "workspace_role: #{member.workspace_role}"
  ```
</CodeGroup>

Daftarkan anggota workspace:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members?limit=10" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:workspaces:members list \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --limit 10
  ```

  ```python Python
  client = anthropic.Anthropic()

  members = client.beta.organization.workspaces.members.list(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", limit=10
  )

  # Secara otomatis mengambil halaman tambahan sesuai kebutuhan.
  for member in members:
      print(f"{member.user_id}: {member.workspace_role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const members = await client.beta.organization.workspaces.members.list(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    { limit: 10 }
  );

  for await (const member of members) {
    console.log(`${member.user_id}: ${member.workspace_role}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Workspaces.Members.List(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new() { Limit = 10 }
  );

  await foreach (var member in page.Paginate())
  {
      Console.WriteLine($"{member.UserID}: {member.WorkspaceRole.Raw()}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  members := client.Beta.Organization.Workspaces.Members.ListAutoPaging(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.BetaOrganizationWorkspaceMemberListParams{
  		Limit: anthropic.Int(10),
  	},
  )

  for members.Next() {
  	member := members.Current()
  	fmt.Printf("%s: %s\n", member.UserID, member.WorkspaceRole)
  }
  if err := members.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.members.MemberListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberListParams.builder()
          .limit(10)
          .build();
      var members = client.beta().organization().workspaces().members()
          .list("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      for (var member : members.autoPager()) {
          IO.println(member.userId() + ": " + member.workspaceRole().asString());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $members = $client->beta->organization->workspaces->members->list(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      limit: 10,
  );

  foreach ($members->getItems() as $member) {
      echo "{$member->userID}: {$member->workspaceRole}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  members = client.beta.organization.workspaces.members.list(workspace_id, limit: 10)

  members.data.each do |member|
    puts "#{member.user_id}: #{member.workspace_role}"
  end
  ```
</CodeGroup>

Perbarui peran anggota workspace:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"workspace_role": "workspace_admin"}'
  ```

  ```bash CLI
  ant beta:organization:workspaces:members update \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --workspace-role workspace_admin
  ```

  ```python Python
  client = anthropic.Anthropic()

  member = client.beta.organization.workspaces.members.update(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      workspace_role="workspace_admin",
  )

  print(f"user_id: {member.user_id}")
  print(f"workspace_role: {member.workspace_role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const member = await client.beta.organization.workspaces.members.update(
    "user_01XyDMpzjS89pFZXqSFUBDr6",
    {
      workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      workspace_role: "workspace_admin"
    }
  );

  console.log(`user_id: ${member.user_id}`);
  console.log(`workspace_role: ${member.workspace_role}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Workspaces;

  AnthropicClient client = new();

  var member = await client.Beta.Organization.Workspaces.Members.Update(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      new()
      {
          WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
          WorkspaceRole = BetaWorkspaceRole.WorkspaceAdmin
      }
  );

  Console.WriteLine($"user_id: {member.UserID}");
  Console.WriteLine($"workspace_role: {member.WorkspaceRole.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  member, err := client.Beta.Organization.Workspaces.Members.Update(
  	context.Background(),
  	"user_01XyDMpzjS89pFZXqSFUBDr6",
  	anthropic.BetaOrganizationWorkspaceMemberUpdateParams{
  		WorkspaceID:   "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  		WorkspaceRole: anthropic.BetaWorkspaceRoleWorkspaceAdmin,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", member.UserID)
  fmt.Printf("workspace_role: %s\n", member.WorkspaceRole)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.BetaWorkspaceRole;
  import com.anthropic.models.beta.organization.workspaces.members.MemberUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberUpdateParams.builder()
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .workspaceRole(BetaWorkspaceRole.WORKSPACE_ADMIN)
          .build();
      var member = client.beta().organization().workspaces().members()
          .update("user_01XyDMpzjS89pFZXqSFUBDr6", params);

      IO.println("user_id: " + member.userId());
      IO.println("workspace_role: " + member.workspaceRole().asString());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Workspaces\WorkspaceRole;
  // ...

  $client = new Client();

  $member = $client->beta->organization->workspaces->members->update(
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      workspaceRole: WorkspaceRole::WORKSPACE_ADMIN,
  );

  echo "user_id: {$member->userID}\n";
  echo "workspace_role: {$member->workspaceRole}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01XyDMpzjS89pFZXqSFUBDr6"
  member = client.beta.organization.workspaces.members.update(
    user_id,
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    workspace_role: :workspace_admin
  )

  puts "user_id: #{member.user_id}"
  puts "workspace_role: #{member.workspace_role}"
  ```
</CodeGroup>

Hapus anggota dari workspace:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:workspaces:members remove \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_member = client.beta.organization.workspaces.members.remove(
      "user_01XyDMpzjS89pFZXqSFUBDr6", workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  print(f"user_id: {removed_member.user_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedMember = await client.beta.organization.workspaces.members.remove(
    "user_01XyDMpzjS89pFZXqSFUBDr6",
    { workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" }
  );

  console.log(`user_id: ${removedMember.user_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedMember = await client.Beta.Organization.Workspaces.Members.Remove(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      new() { WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" }
  );

  Console.WriteLine($"user_id: {removedMember.UserID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedMember, err := client.Beta.Organization.Workspaces.Members.Remove(
  	context.Background(),
  	"user_01XyDMpzjS89pFZXqSFUBDr6",
  	anthropic.BetaOrganizationWorkspaceMemberRemoveParams{
  		WorkspaceID: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", removedMember.UserID)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.members.MemberRemoveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberRemoveParams.builder()
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .build();
      var removedMember = client.beta().organization().workspaces().members()
          .remove("user_01XyDMpzjS89pFZXqSFUBDr6", params);

      IO.println("user_id: " + removedMember.userId());
  }
  ```

  ```php PHP
  $client = new Client();

  $removedMember = $client->beta->organization->workspaces->members->remove(
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  echo "user_id: {$removedMember->userID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01XyDMpzjS89pFZXqSFUBDr6"
  removed_member = client.beta.organization.workspaces.members.remove(
    user_id,
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  puts "user_id: #{removed_member.user_id}"
  ```
</CodeGroup>

### Kunci API

Pantau dan kelola [kunci API](https://platform.claude.com/docs/id/api/admin/api_keys/list). Setiap kunci dalam respons menyertakan timestamp `expires_at` (`null` untuk kunci tanpa [masa kedaluwarsa](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration)) dan `principal`, yaitu identitas yang diwakilinya (lihat [Jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types)). Untuk kunci personal, `principal` adalah `{"type": "user_actor", "user_id": "user_..."}`; untuk kunci service account, `{"type": "service_account_actor", "service_account_id": "svac_..."}`; dan untuk kunci workspace, `null`. Setiap kunci juga memiliki objek `scope`: `{"type": "workspace", "workspace_id": "wrkspc_..."}` untuk kunci yang terikat pada satu workspace, atau `{"type": "organization"}` untuk kunci yang dapat bekerja di workspace mana pun yang dapat diakses akun tersebut. Field `workspace_id` tingkat atas sudah deprecated dan bernilai `null` baik untuk kunci yang terikat pada Default Workspace maupun untuk kunci tanpa scope workspace; gunakan `scope` untuk membedakannya. Memfilter daftar berdasarkan `workspace_id` dengan ID Default Workspace hanya mengembalikan kunci yang terikat pada Default Workspace; kunci tanpa scope workspace tidak dikembalikan di bawah filter `workspace_id` apa pun.

Daftarkan kunci API aktif di sebuah workspace:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/api_keys?limit=10&status=active&workspace_id=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:api-keys list \
    --limit 10 \
    --status active \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  api_keys = client.beta.organization.api_keys.list(
      limit=10, status="active", workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  # Secara otomatis mengambil halaman tambahan sesuai kebutuhan.
  for api_key in api_keys:
      print(f"{api_key.id}: {api_key.name} ({api_key.status})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const apiKeys = await client.beta.organization.apiKeys.list({
    limit: 10,
    status: "active",
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  });

  for await (const apiKey of apiKeys) {
    console.log(`${apiKey.id}: ${apiKey.name} (${apiKey.status})`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ApiKeys;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.ApiKeys.List(new()
  {
      Limit = 10,
      Status = ApiKeyListParamsStatus.Active,
      WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  });

  await foreach (var apiKey in page.Paginate())
  {
      Console.WriteLine($"{apiKey.ID}: {apiKey.Name} ({apiKey.Status.Raw()})");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  apiKeys := client.Beta.Organization.APIKeys.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAPIKeyListParams{
  	Limit:       anthropic.Int(10),
  	Status:      anthropic.BetaOrganizationAPIKeyListParamsStatusActive,
  	WorkspaceID: anthropic.String("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"),
  })

  for apiKeys.Next() {
  	apiKey := apiKeys.Current()
  	fmt.Printf("%s: %s (%s)\n", apiKey.ID, apiKey.Name, apiKey.Status)
  }
  if err := apiKeys.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.apikeys.ApiKeyListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ApiKeyListParams.builder()
          .limit(10)
          .status(ApiKeyListParams.Status.ACTIVE)
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .build();
      var apiKeys = client.beta().organization().apiKeys().list(params);

      for (var apiKey : apiKeys.autoPager()) {
          IO.println(apiKey.id() + ": " + apiKey.name() + " (" + apiKey.status().asString() + ")");
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\APIKeys\APIKeyListParams\Status;
  // ...

  $client = new Client();

  $apiKeys = $client->beta->organization->apiKeys->list(
      limit: 10,
      status: Status::ACTIVE,
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  foreach ($apiKeys->getItems() as $apiKey) {
      echo "{$apiKey->id}: {$apiKey->name} ({$apiKey->status})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  api_keys = client.beta.organization.api_keys.list(
    limit: 10,
    status: :active,
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  api_keys.data.each do |api_key|
    puts "#{api_key.id}: #{api_key.name} (#{api_key.status})"
  end
  ```
</CodeGroup>

Ganti nama atau nonaktifkan kunci API:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/api_keys/apikey_01Rj2N8SVvo6BePZj99NhmiT" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "status": "inactive",
      "name": "New Key Name"
    }'
  ```

  ```bash CLI
  ant beta:organization:api-keys update \
    --api-key-id apikey_01Rj2N8SVvo6BePZj99NhmiT \
    --status inactive \
    --name "New Key Name"
  ```

  ```python Python
  client = anthropic.Anthropic()

  api_key = client.beta.organization.api_keys.update(
      "apikey_01Rj2N8SVvo6BePZj99NhmiT", status="inactive", name="New Key Name"
  )

  print(f"id: {api_key.id}")
  print(f"name: {api_key.name}")
  print(f"status: {api_key.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const apiKey = await client.beta.organization.apiKeys.update(
    "apikey_01Rj2N8SVvo6BePZj99NhmiT",
    {
      status: "inactive",
      name: "New Key Name"
    }
  );

  console.log(`id: ${apiKey.id}`);
  console.log(`name: ${apiKey.name}`);
  console.log(`status: ${apiKey.status}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ApiKeys;

  AnthropicClient client = new();

  var apiKey = await client.Beta.Organization.ApiKeys.Update(
      "apikey_01Rj2N8SVvo6BePZj99NhmiT",
      new()
      {
          Status = Status.Inactive,
          Name = "New Key Name"
      }
  );

  Console.WriteLine($"id: {apiKey.ID}");
  Console.WriteLine($"name: {apiKey.Name}");
  Console.WriteLine($"status: {apiKey.Status.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  apiKey, err := client.Beta.Organization.APIKeys.Update(
  	context.Background(),
  	"apikey_01Rj2N8SVvo6BePZj99NhmiT",
  	anthropic.BetaOrganizationAPIKeyUpdateParams{
  		Status: anthropic.BetaOrganizationAPIKeyUpdateParamsStatusInactive,
  		Name:   anthropic.String("New Key Name"),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", apiKey.ID)
  fmt.Printf("name: %s\n", apiKey.Name)
  fmt.Printf("status: %s\n", apiKey.Status)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.apikeys.ApiKeyUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ApiKeyUpdateParams.builder()
          .status(ApiKeyUpdateParams.Status.INACTIVE)
          .name("New Key Name")
          .build();
      var apiKey = client.beta().organization().apiKeys()
          .update("apikey_01Rj2N8SVvo6BePZj99NhmiT", params);

      IO.println("id: " + apiKey.id());
      IO.println("name: " + apiKey.name());
      IO.println("status: " + apiKey.status().asString());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\APIKeys\APIKeyUpdateParams\Status;
  // ...

  $client = new Client();

  $apiKey = $client->beta->organization->apiKeys->update(
      apiKeyID: 'apikey_01Rj2N8SVvo6BePZj99NhmiT',
      status: Status::INACTIVE,
      name: 'New Key Name',
  );

  echo "id: {$apiKey->id}\n";
  echo "name: {$apiKey->name}\n";
  echo "status: {$apiKey->status}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  api_key_id = "apikey_01Rj2N8SVvo6BePZj99NhmiT"
  api_key = client.beta.organization.api_keys.update(
    api_key_id,
    status: :inactive,
    name: "New Key Name"
  )

  puts "id: #{api_key.id}"
  puts "name: #{api_key.name}"
  puts "status: #{api_key.status}"
  ```
</CodeGroup>

### Service account

Buat dan kelola service account (`svac_...`), yaitu identitas non-manusia yang diwakili oleh [kunci service account](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) dan token [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Endpoint ini, seperti endpoint federation-issuer dan federation-rule, memerlukan token OAuth `org:admin`. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#service-accounts).

### Federation issuer

Daftarkan penyedia identitas OIDC (`fdis_...`) yang tokennya dapat menyatakan identitas beban kerja untuk organisasi Anda. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-issuers).

### Federation rule

Kelola aturan (`fdrl_...`) yang memetakan token issuer ke service account dan scope. Lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-rules).

## Mengakses info organisasi

Endpoint `/v1/organizations/me` mengembalikan organisasi tempat kredensial Anda berada:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/me" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization retrieve
  ```

  ```python Python
  client = anthropic.Anthropic()

  organization = client.beta.organization.retrieve()

  print(f"id: {organization.id}")
  print(f"name: {organization.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const organization = await client.beta.organization.retrieve();

  console.log(`id: ${organization.id}`);
  console.log(`name: ${organization.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var organization = await client.Beta.Organization.Retrieve();

  Console.WriteLine($"id: {organization.ID}");
  Console.WriteLine($"name: {organization.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  organization, err := client.Beta.Organization.Get(context.Background())
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", organization.ID)
  fmt.Printf("name: %s\n", organization.Name)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var organization = client.beta().organization().retrieve();

  IO.println("id: " + organization.id());
  IO.println("name: " + organization.name());
  ```

  ```php PHP
  $client = new Client();

  $organization = $client->beta->organization->retrieve();

  echo "id: {$organization->id}\n";
  echo "name: {$organization->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  organization = client.beta.organization.retrieve

  puts "id: #{organization.id}"
  puts "name: #{organization.name}"
  ```
</CodeGroup>

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "type": "organization",
  "name": "Organization Name"
}
```

Untuk detail parameter dan skema respons, lihat [referensi Organization Info API](https://platform.claude.com/docs/id/api/admin-api/organization/get-me).

## Laporan penggunaan dan biaya

Lacak penggunaan dan biaya organisasi Anda dengan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api).

## Analitik Claude Code

Pantau produktivitas developer dan adopsi Claude Code dengan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api).

## Batas laju

Baca "rate limit" (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Compliance API

Ambil data audit dan aktivitas untuk organisasi Anda dengan [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api). Kunci Admin API hanya dapat membaca Activity Feed. Untuk akses penuh, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

## Praktik terbaik

* Gunakan nama dan deskripsi yang bermakna untuk workspace dan kunci API
* Tangani error dari operasi yang gagal
* Audit peran dan izin anggota secara berkala
* Bersihkan workspace yang tidak digunakan dan undangan yang kedaluwarsa
* Pantau penggunaan kunci API, audit [`expires_at`](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) setiap kunci, dan rotasi kunci secara berkala

## FAQ

<AccordionGroup>
  <Accordion title="Izin apa yang diperlukan untuk menggunakan Admin API?">
    Admin API menerima kunci Admin API (diawali dengan `sk-ant-admin`), token bearer OAuth dengan scope `org:admin`, atau kunci personal maupun kunci service account yang tidak dibatasi pada workspace tertentu. Hanya anggota organisasi dengan peran admin yang dapat membuat kunci Admin API, dan hanya anggota dengan peran admin, owner, atau primary owner yang dapat memperoleh token `org:admin`. Kunci personal atau kunci service account memiliki izin yang sama dengan akun yang tertaut. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication).
  </Accordion>

  <Accordion title="Bisakah saya membuat kunci API baru melalui Admin API?">
    Tidak. Anda membuat kunci API di Claude Console. Admin API hanya dapat membaca, mengganti nama, dan mengubah status kunci yang sudah ada.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API saat menghapus pengguna?">
    Perilakunya bergantung pada [jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types).

    Kunci personal berhenti berfungsi ketika penggunanya dihapus dari organisasi. Kunci service account berhenti berfungsi jika service account-nya diarsipkan, tetapi tetap berfungsi meskipun pengguna yang membuatnya dihapus. Kunci API workspace tetap berfungsi. Di [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), setiap kunci terikat pada anggota yang membuatnya dan berhenti berfungsi ketika anggota tersebut dihapus.
  </Accordion>

  <Accordion title="Bisakah admin organisasi dihapus melalui API?">
    Tidak. API tidak dapat menghapus anggota dengan peran admin.
  </Accordion>

  <Accordion title="Berapa lama undangan organisasi berlaku?">
    Undangan kedaluwarsa setelah 21 hari. Periode kedaluwarsa tidak dapat dikonfigurasi.
  </Accordion>
</AccordionGroup>

Untuk pertanyaan khusus workspace, lihat [FAQ Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#faq).
