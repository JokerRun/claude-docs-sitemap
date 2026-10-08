---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workspaces
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 6ec03343c5c345b321881ca12fce4ffca0c9d1bb97e1f39f56a57115fa683fd1
---

---
title: Workspace
url: https://platform.claude.com/docs/id/manage-claude/workspaces
description: Atur kunci API, kelola akses tim, dan kendalikan biaya dengan workspaces.
---

Workspaces menyediakan cara untuk mengatur penggunaan API Anda dalam sebuah organisasi. Gunakan workspaces untuk memisahkan proyek, lingkungan, atau tim yang berbeda sambil mempertahankan penagihan dan administrasi terpusat.

## Cara kerja workspaces

Setiap organisasi memiliki **Default Workspace** yang tidak dapat diganti nama, diarsipkan, atau dihapus. Ketika Anda membuat workspaces tambahan, Anda dapat menetapkan anggota, akun layanan, kunci API, dan batas sumber daya untuk masing-masing.

Karakteristik utama:

* **Pengidentifikasi workspace** menggunakan awalan `wrkspc_` (misalnya, `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`)
* **Maksimum 100 workspaces** per organisasi secara default (workspaces yang diarsipkan tidak dihitung); hubungi tim akun Anda jika Anda membutuhkan lebih banyak
* **Default Workspace** memiliki ID `wrkspc_` seperti workspace lainnya (dikembalikan dalam [header respons `anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response) dan diterima oleh [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve)), tetapi hanya muncul dalam hasil [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) ketika Anda meneruskan `include_default=true`, dan kunci API, laporan penggunaan, serta laporan biaya menampilkan `null` untuk `workspace_id`-nya, begitu pula kunci API untuk semua workspace (field `scope` pada kunci API membedakan keduanya; untuk kunci yang terikat ke Default Workspace, field tersebut memuat ID yang sebenarnya)
* **Kunci API** dapat dicakupkan ke satu workspace. Dalam hal ini, kunci tersebut hanya dapat mengakses sumber daya dalam workspace tersebut. Beberapa kunci API dapat diberikan izin di beberapa workspaces, dan menyediakan [header ID workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) untuk mengakses sumber daya dalam workspace tersebut

### Workspace Claude Code

Ketika anggota organisasi Anda pertama kali masuk ke [Claude Code](https://code.claude.com/docs/en/overview) dengan akun Claude Console mereka, Anthropic secara otomatis membuat workspace **Claude Code** di organisasi dan menambahkan anggota tersebut ke dalamnya. Setiap anggota berikutnya yang masuk ke Claude Code ditambahkan dengan cara yang sama.

Workspace Claude Code menjaga lalu lintas Claude Code terpisah dari beban kerja API Anda yang lain:

* Claude Code mencetak kunci API per-pengguna di workspace ini saat masuk. Anda tidak dapat membuat kunci di dalamnya secara manual dari Console.
* Kunci Claude Code berhenti bekerja jika pemiliknya dihapus dari workspace atau organisasi, tidak seperti kunci workspace.
* Penggunaan Claude Code dibatasi lajunya secara terpisah, dan admin dapat membatasi bagiannya dari batas organisasi di bawah [Settings > Workspaces](https://platform.claude.com/settings/workspaces).
* Ini adalah satu-satunya workspace yang mendukung batas pengeluaran bulanan per-pengguna.

<Warning>
  Mengarsipkan workspace Claude Code menonaktifkan masuk Claude Code melalui penagihan Console untuk seluruh organisasi.
</Warning>

## Peran dan izin workspace

Anggota dapat memiliki peran yang berbeda di setiap workspace, memungkinkan kontrol akses yang terperinci.

| Peran                       | Izin                                                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Workspace User              | Hanya menggunakan playground                                                                                         |
| Workspace Limited Developer | Membuat dan mengelola kunci API, menggunakan API. Tidak dapat mengakses tampilan pelacakan sesi atau mengunduh file. |
| Workspace Developer         | Membuat dan mengelola kunci API, menggunakan API                                                                     |
| Workspace Admin             | Kontrol penuh atas pengaturan dan anggota workspace                                                                  |
| Workspace Billing           | Melihat informasi penagihan workspace (diwarisi dari peran penagihan organisasi)                                     |

### Pewarisan peran

* **Admin organisasi** secara otomatis menerima akses Workspace Admin ke semua workspaces
* **Anggota penagihan organisasi** secara otomatis menerima akses Workspace Billing ke semua workspaces
* **Pengguna dan developer organisasi** harus ditambahkan secara eksplisit ke setiap workspace
* **Akun layanan** ditambahkan ke workspaces di [Settings > Service accounts](https://platform.claude.com/settings/service-accounts): pilih **Add to workspace** di menu akun atau di halamannya sendiri. Untuk melihat akun dalam satu workspace, filter daftar berdasarkan workspace.

<Note>
  Peran Workspace Billing tidak dapat ditetapkan secara manual. Peran ini diwarisi dari memiliki peran penagihan organisasi.
</Note>

## Mengelola workspaces

<Note>
  Hanya admin organisasi yang dapat membuat workspaces. Pengguna dan developer organisasi harus ditambahkan ke workspaces oleh admin.
</Note>

### Menggunakan Console

Buat dan kelola workspaces di [Claude Console](https://platform.claude.com/settings/workspaces).

#### Membuat workspace

<Steps>
  <Step title="Buka pengaturan workspace">
    Di Claude Console, buka **Settings > Workspaces**.
  </Step>

  <Step title="Buat workspace">
    Klik **Create workspace**.
  </Step>

  <Step title="Konfigurasikan workspace">
    Masukkan nama workspace dan pilih warna untuk identifikasi visual.
  </Step>

  <Step title="Buat workspace">
    Klik **Create** untuk menyelesaikan.
  </Step>
</Steps>

<Tip>
  Untuk beralih antar workspaces di Console, gunakan pemilih **Workspaces** di sudut kiri atas.
</Tip>

#### Mengedit detail workspace

Untuk mengubah nama atau warna workspace:

1. Pilih workspace dari daftar.
2. Klik menu elipsis (**...**) dan pilih **Edit details**.
3. Perbarui nama atau warna dan simpan perubahan Anda.

<Note>
  Default Workspace tidak dapat diganti nama atau dihapus.
</Note>

#### Menambahkan anggota ke workspace

1. Navigasikan ke tab **Members** workspace.
2. Klik **Add to Workspace**.
3. Pilih anggota organisasi dan tetapkan [peran workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#workspace-roles-and-permissions) kepada mereka.
4. Konfirmasikan penambahan.

Untuk menghapus anggota, klik ikon tempat sampah di sebelah nama mereka.

<Note>
  Admin organisasi dan anggota penagihan tidak dapat dihapus dari workspaces selama mereka memegang peran organisasi tersebut.
</Note>

#### Menetapkan batas workspace

Pengaturan setiap workspace membagi ini ke dalam dua tab:

* **Rate limits:** Di tab **Rate limits**, tetapkan batas per tingkat model untuk permintaan per menit, token input, atau token output
* **Spend limits:** Di tab **Spend limits**, batasi pengeluaran bulanan dan konfigurasikan peringatan ketika pengeluaran mencapai ambang batas tertentu

#### Mengarsipkan workspace

Untuk mengarsipkan workspace, klik menu elipsis (**...**) dan pilih **Archive**. Pengarsipan:

* Mempertahankan data historis untuk pelaporan
* Menonaktifkan workspace dan mengarsipkan setiap kunci API yang dibuat untuknya
* Tidak dapat dibatalkan

<Warning>
  Mengarsipkan workspace mengarsipkan setiap kunci API yang dibuat untuk workspace tersebut dalam hitungan detik (kunci tersebut tetap terdaftar di Admin API sebagai diarsipkan), dan kunci multi-workspace tidak dapat lagi bertindak di dalamnya. Tindakan ini tidak dapat dibatalkan. Jika Anda mengarsipkan [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), anggota organisasi Anda tidak dapat lagi masuk ke Claude Code melalui penagihan Console.
</Warning>

### Menggunakan Admin API

Kelola workspaces secara terprogram menggunakan [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api).

<Note>
  Endpoint Admin API menerima [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys), token OAuth `org:admin`, atau kunci akun pribadi atau layanan yang tidak dicakupkan ke workspace tertentu. Kunci workspace tidak berfungsi di sana. Lihat [Authentication](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication).
</Note>

Contoh SDK dan CLI berikut membuat klien default, yang membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`; SDK mengekspos endpoint ini di bawah `client.organization.workspaces` (csharp, go: `client.Organization.Workspaces`; java: `client.organization().workspaces()`; php: `$client->organization->workspaces`). Metode list pada SDK mengambil halaman berikutnya sesuai kebutuhan, sehingga `limit` menetapkan ukuran halaman; contoh PHP, Ruby, dan curl mengembalikan satu halaman.

Membuat workspace:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/workspaces" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"name": "Production"}'
  ```

  ```bash CLI
  ant organization:workspaces create --name Production
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.organization.workspaces.create(name="Production")

  print(f"id: {workspace.id}")
  print(f"name: {workspace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.organization.workspaces.create({ name: "Production" });

  console.log(`id: ${workspace.id}`);
  console.log(`name: ${workspace.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspace = await client.Organization.Workspaces.Create(new()
  {
      Name = "Production"
  });

  Console.WriteLine($"id: {workspace.ID}");
  Console.WriteLine($"name: {workspace.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Organization.Workspaces.New(context.Background(), anthropic.OrganizationWorkspaceNewParams{
  	Name: "Production",
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", workspace.ID)
  fmt.Printf("name: %s\n", workspace.Name)
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.WorkspaceCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceCreateParams.builder()
          .name("Production")
          .build();
      var workspace = client.organization().workspaces().create(params);

      IO.println("id: " + workspace.id());
      IO.println("name: " + workspace.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->organization->workspaces->create(
      name: 'Production',
  );

  echo "id: {$workspace->id}\n";
  echo "name: {$workspace->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace = client.organization.workspaces.create(name: "Production")

  puts "id: #{workspace.id}"
  puts "name: #{workspace.name}"
  ```
</CodeGroup>

Mendaftar workspaces:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces?limit=10&include_archived=false" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:workspaces list --limit 10 --include-archived=false
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspaces = client.organization.workspaces.list(limit=10, include_archived=False)

  for workspace in workspaces:
      print(f"{workspace.id}: {workspace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspaces = await client.organization.workspaces.list({
    limit: 10,
    include_archived: false
  });

  for await (const workspace of workspaces) {
    console.log(`${workspace.id}: ${workspace.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspaces = await client.Organization.Workspaces.List(new()
  {
      Limit = 10,
      IncludeArchived = false
  });

  await foreach (var workspace in workspaces.Paginate())
  {
      Console.WriteLine($"{workspace.ID}: {workspace.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  workspaces := client.Organization.Workspaces.ListAutoPaging(context.Background(), anthropic.OrganizationWorkspaceListParams{
  	Limit:           anthropic.Int(10),
  	IncludeArchived: anthropic.Bool(false),
  })

  for workspaces.Next() {
  	workspace := workspaces.Current()
  	fmt.Printf("%s: %s\n", workspace.ID, workspace.Name)
  }
  if err := workspaces.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.WorkspaceListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceListParams.builder()
          .limit(10)
          .includeArchived(false)
          .build();
      var workspaces = client.organization().workspaces().list(params);

      for (var workspace : workspaces.autoPager()) {
          IO.println(workspace.id() + ": " + workspace.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $workspaces = $client->organization->workspaces->list(
      limit: 10,
      includeArchived: false,
  );

  foreach ($workspaces->getItems() as $workspace) {
      echo "{$workspace->id}: {$workspace->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspaces = client.organization.workspaces.list(limit: 10, include_archived: false)

  workspaces.data.each do |workspace|
    puts "#{workspace.id}: #{workspace.name}"
  end
  ```
</CodeGroup>

Mengarsipkan workspace:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:workspaces archive --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.organization.workspaces.archive("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")

  print(f"id: {workspace.id}")
  print(f"archived_at: {workspace.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.organization.workspaces.archive(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  console.log(`id: ${workspace.id}`);
  console.log(`archived_at: ${workspace.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspace = await client.Organization.Workspaces.Archive(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  Console.WriteLine($"id: {workspace.ID}");
  Console.WriteLine($"archived_at: {workspace.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Organization.Workspaces.Archive(context.Background(), "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", workspace.ID)
  fmt.Printf("archived_at: %s\n", workspace.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var workspace = client.organization().workspaces()
      .archive("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ");

  IO.println("id: " + workspace.id());
  IO.println("archived_at: " + workspace.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->organization->workspaces->archive(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  echo "id: {$workspace->id}\n";
  echo "archived_at: {$workspace->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  workspace = client.organization.workspaces.archive(workspace_id)

  puts "id: #{workspace.id}"
  puts "archived_at: #{workspace.archived_at}"
  ```
</CodeGroup>

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve).

### Mengelola anggota workspace

Menambahkan anggota ke workspace:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "user_id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "workspace_role": "workspace_developer"
    }'
  ```

  ```bash CLI
  ant organization:workspaces:members add \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-role workspace_developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  member = client.organization.workspaces.members.add(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      user_id="user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_role="workspace_developer",
  )

  print(f"user_id: {member.user_id}")
  print(f"workspace_role: {member.workspace_role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const member = await client.organization.workspaces.members.add(
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
  using Anthropic.Models.Organization.Workspaces;

  AnthropicClient client = new();

  var member = await client.Organization.Workspaces.Members.Add(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new()
      {
          UserID = "user_01XyDMpzjS89pFZXqSFUBDr6",
          WorkspaceRole = NoBillingWorkspaceRole.WorkspaceDeveloper
      }
  );

  Console.WriteLine($"user_id: {member.UserID}");
  Console.WriteLine($"workspace_role: {member.WorkspaceRole.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  member, err := client.Organization.Workspaces.Members.Add(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.OrganizationWorkspaceMemberAddParams{
  		UserID:        "user_01XyDMpzjS89pFZXqSFUBDr6",
  		WorkspaceRole: anthropic.NoBillingWorkspaceRoleWorkspaceDeveloper,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", member.UserID)
  fmt.Printf("workspace_role: %s\n", member.WorkspaceRole)
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.NoBillingWorkspaceRole;
  import com.anthropic.models.organization.workspaces.members.MemberAddParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberAddParams.builder()
          .userId("user_01XyDMpzjS89pFZXqSFUBDr6")
          .workspaceRole(NoBillingWorkspaceRole.WORKSPACE_DEVELOPER)
          .build();
      var member = client.organization().workspaces().members()
          .add("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      IO.println("user_id: " + member.userId());
      IO.println("workspace_role: " + member.workspaceRole().asString());
  }
  ```

  ```php PHP
  use Anthropic\Organization\Workspaces\NoBillingWorkspaceRole;
  // ...

  $client = new Client();

  $member = $client->organization->workspaces->members->add(
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
  member = client.organization.workspaces.members.add(
    workspace_id,
    user_id: "user_01XyDMpzjS89pFZXqSFUBDr6",
    workspace_role: :workspace_developer
  )

  puts "user_id: #{member.user_id}"
  puts "workspace_role: #{member.workspace_role}"
  ```
</CodeGroup>

Memperbarui peran anggota:

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"workspace_role": "workspace_admin"}'
  ```

  ```bash CLI
  ant organization:workspaces:members update \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --workspace-role workspace_admin
  ```

  ```python Python
  client = anthropic.Anthropic()

  member = client.organization.workspaces.members.update(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      workspace_role="workspace_admin",
  )

  print(f"user_id: {member.user_id}")
  print(f"workspace_role: {member.workspace_role}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const member = await client.organization.workspaces.members.update(
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
  using Anthropic.Models.Organization.Workspaces;

  AnthropicClient client = new();

  var member = await client.Organization.Workspaces.Members.Update(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      new()
      {
          WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
          WorkspaceRole = WorkspaceRole.WorkspaceAdmin
      }
  );

  Console.WriteLine($"user_id: {member.UserID}");
  Console.WriteLine($"workspace_role: {member.WorkspaceRole.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  member, err := client.Organization.Workspaces.Members.Update(
  	context.Background(),
  	"user_01XyDMpzjS89pFZXqSFUBDr6",
  	anthropic.OrganizationWorkspaceMemberUpdateParams{
  		WorkspaceID:   "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  		WorkspaceRole: anthropic.WorkspaceRoleWorkspaceAdmin,
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", member.UserID)
  fmt.Printf("workspace_role: %s\n", member.WorkspaceRole)
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.WorkspaceRole;
  import com.anthropic.models.organization.workspaces.members.MemberUpdateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberUpdateParams.builder()
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .workspaceRole(WorkspaceRole.WORKSPACE_ADMIN)
          .build();
      var member = client.organization().workspaces().members()
          .update("user_01XyDMpzjS89pFZXqSFUBDr6", params);

      IO.println("user_id: " + member.userId());
      IO.println("workspace_role: " + member.workspaceRole().asString());
  }
  ```

  ```php PHP
  use Anthropic\Organization\Workspaces\WorkspaceRole;
  // ...

  $client = new Client();

  $member = $client->organization->workspaces->members->update(
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
  member = client.organization.workspaces.members.update(
    user_id,
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    workspace_role: :workspace_admin
  )

  puts "user_id: #{member.user_id}"
  puts "workspace_role: #{member.workspace_role}"
  ```
</CodeGroup>

Menghapus anggota dari workspace:

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/members/user_01XyDMpzjS89pFZXqSFUBDr6" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:workspaces:members remove \
    --user-id user_01XyDMpzjS89pFZXqSFUBDr6 \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  removed_member = client.organization.workspaces.members.remove(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  )

  print(f"user_id: {removed_member.user_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const removedMember = await client.organization.workspaces.members.remove(
    "user_01XyDMpzjS89pFZXqSFUBDr6",
    { workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" }
  );

  console.log(`user_id: ${removedMember.user_id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var removedMember = await client.Organization.Workspaces.Members.Remove(
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      new() { WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" }
  );

  Console.WriteLine($"user_id: {removedMember.UserID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  removedMember, err := client.Organization.Workspaces.Members.Remove(
  	context.Background(),
  	"user_01XyDMpzjS89pFZXqSFUBDr6",
  	anthropic.OrganizationWorkspaceMemberRemoveParams{
  		WorkspaceID: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("user_id: %s\n", removedMember.UserID)
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.members.MemberRemoveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MemberRemoveParams.builder()
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .build();
      var removedMember = client.organization().workspaces().members()
          .remove("user_01XyDMpzjS89pFZXqSFUBDr6", params);

      IO.println("user_id: " + removedMember.userId());
  }
  ```

  ```php PHP
  $client = new Client();

  $removedMember = $client->organization->workspaces->members->remove(
      userID: 'user_01XyDMpzjS89pFZXqSFUBDr6',
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  echo "user_id: {$removedMember->userID}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  user_id = "user_01XyDMpzjS89pFZXqSFUBDr6"
  removed_member = client.organization.workspaces.members.remove(
    user_id,
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  puts "user_id: #{removed_member.user_id}"
  ```
</CodeGroup>

Untuk detail parameter lengkap, lihat [referensi API Workspace Members](https://platform.claude.com/docs/id/api/organization/workspaces/members/retrieve).

## Kunci API dan pencakupan sumber daya

Setiap permintaan berjalan di tepat satu workspace dan hanya dapat mengakses sumber daya dalam workspace tersebut. Workspace mana bergantung pada [jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types):

* Sebuah **kunci workspace** (kunci lama tanpa pemilik) milik workspace tempat kunci tersebut dibuat dan selalu berjalan di sana.
* Sebuah **kunci pribadi** atau **kunci akun layanan** bertindak sebagai pengguna atau akun layanannya. Kunci satu-workspace selalu berjalan di workspace yang dipilih saat dibuat. Kunci multi-workspace berjalan di workspace yang dinamai oleh header `anthropic-workspace-id` setiap permintaan. Akun harus memiliki akses ke workspace untuk menggunakannya.

Sumber daya yang dicakupkan ke workspaces meliputi:

* **Files** yang dibuat melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* **Message Batches** yang dibuat melalui [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* **Skills** yang dibuat melalui [Skills API](https://platform.claude.com/docs/id/build-with-claude/skills-guide)

Beberapa sumber daya dikelola secara berbeda:

* **[MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview)** dikelola dengan token OAuth `workspace:manage_tunnels` yang diperoleh melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation), bukan kunci API. Tunnels dibuat di workspace, dan daftar **MCP tunnels** Console serta pemilih server Managed Agent menampilkan tunnels di workspace saat ini saja; batas 10 tunnels aktif berlaku di seluruh organisasi. Pengelolaan tunnel memerlukan peran dengan izin pengelolaan tunnel; developer organisasi dapat melihat tetapi tidak mengubahnya.
* **Workspaces** itu sendiri dan **anggota organisasi** dikelola di tingkat organisasi melalui [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), menggunakan kunci Admin API, token OAuth `org:admin`, atau kunci akun pribadi atau layanan yang tidak dicakupkan ke workspace tertentu.

Untuk mencari ID workspace organisasi Anda, panggil endpoint [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) (teruskan `include_default=true` untuk menyertakan Default Workspace) atau temukan di [Claude Console](https://platform.claude.com/settings/workspaces).

<Note>
  [Prompt caches](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) juga diisolasi per workspace pada Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Pada Amazon Bedrock dan Google Cloud, prompt caches diisolasi per organisasi.
</Note>

## Mengidentifikasi workspace di balik respons API

Respons Claude API menyertakan header `anthropic-workspace-id` bersama dengan [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) `request-id` dan `anthropic-organization-id`. Nilainya adalah ID berawalan `wrkspc_` dari workspace yang diselesaikan oleh kunci API atau token akses permintaan, termasuk ketika workspace tersebut adalah Default Workspace. Misalnya, respons yang berhasil menyertakan header seperti ini:

```http
HTTP/1.1 200 OK
request-id: req_018EeWyXxfu5pfWkrYcMdjWG
anthropic-organization-id: 0d0e7a3b-52f1-4c7e-9a51-3f6f2f7c1b9e
anthropic-workspace-id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
```

Header tidak ada ketika kredensial tidak diselesaikan ke workspace (misalnya, pada permintaan Admin API) atau ketika permintaan gagal sebelum autentikasi selesai, seperti kesalahan 401.

Contoh berikut mengirim permintaan Messages API dan mencetak ID workspace dari header respons:

<CodeGroup>
  ```bash cURL
  # -D - mencetak header respons; -o /dev/null membuang body
  curl -sS -D - -o /dev/null https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | grep -i '^anthropic-workspace-id'
  ```

  ```bash CLI
  # --debug mencetak respons HTTP, termasuk Anthropic-Workspace-Id
  # header, ke stderr; > /dev/null menyembunyikan body JSON di stdout
  ant --debug messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' > /dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.with_raw_response.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  workspace_id = response.headers.get("anthropic-workspace-id")
  print(f"Workspace ID: {workspace_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const { response } = await client.messages
    .create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    })
    .withResponse();
  console.log("Workspace ID:", response.headers.get("anthropic-workspace-id"));
  ```

  ```csharp C#
  AnthropicClient client = new();

  using var response = await client.WithRawResponse.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }]
  });
  var workspaceId = response.GetHeaderValues("anthropic-workspace-id").First();
  Console.WriteLine($"Workspace ID: {workspaceId}");
  ```

  ```go Go
  client := anthropic.NewClient()

  var response *http.Response
  _, err := client.Messages.New(
  	context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	},
  	option.WithResponseInto(&response),
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println("Workspace ID:", response.Header.Get("anthropic-workspace-id"))
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponseFor;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      HttpResponseFor<Message> response = client.messages().withRawResponse().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build()
      );

      String workspaceId = response.headers().values("anthropic-workspace-id").getFirst();
      IO.println("Workspace ID: " + workspaceId);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->raw->create([
      'model' => Model::CLAUDE_OPUS_5_5,
      'maxTokens' => 1024,
      'messages' => [['role' => 'user', 'content' => 'Hello, Claude']],
  ]);
  echo 'Workspace ID: ' . $response->getHeaderLine('anthropic-workspace-id') . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Baca header respons di middleware per-permintaan, yang menerima
  # respons HTTP mentah sebelum SDK mem-parsing-nya
  workspace_id = nil
  read_workspace_id = lambda do |request, call_next|
    response = call_next.call(request)
    # Kunci di response.headers menggunakan huruf kecil
    workspace_id = response.headers["anthropic-workspace-id"]
    response
  end

  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    request_options: { middleware: [read_workspace_id] }
  )
  puts "Workspace ID: #{workspace_id}"
  ```
</CodeGroup>

```text Output wrap
Workspace ID: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
```

Accessor yang sama membaca header dari endpoint Claude API lainnya juga, termasuk API [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview). Misalnya, baca `anthropic-workspace-id` dari respons yang [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions) untuk mencatat workspace mana yang menjadi milik sesi tersebut.

Dengan ID workspace dari respons, Anda dapat:

* Mengonfirmasi penggunaan, biaya, dan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) workspace mana yang dihitung oleh permintaan tersebut
* Mencocokkannya dengan bidang `workspace_id` dalam laporan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) dan pada objek [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) seperti kunci API (keduanya melaporkan `null` untuk Default Workspace, seperti halnya kunci API untuk kunci semua-workspaces; bidang `scope` kunci API membedakan keduanya dan, untuk kunci yang terikat ke satu workspace, membawa ID workspace yang sebenarnya)
* Memeriksa apakah itu ID Default Workspace Anda dengan meneruskannya ke [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve) menggunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys): Default Workspace dikembalikan dengan `"name": "Default"`, meskipun [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) menghilangkannya kecuali Anda meneruskan `include_default=true`
* Membuka workspace tersebut di [Console](https://platform.claude.com/settings/workspaces) untuk menemukan sumber daya permintaan, seperti sesi, file, message batches, dan skills

## Batas workspace

Anda dapat menetapkan batas pengeluaran dan batas laju khusus untuk setiap workspace untuk melindungi dari penggunaan berlebihan dan memastikan distribusi sumber daya yang adil.

### Menetapkan batas workspace

Anda dapat menetapkan batas workspace lebih rendah dari (tetapi tidak lebih tinggi dari) batas organisasi Anda:

* **Spend limits:** Batasi pengeluaran bulanan untuk workspace. Tetapkan ini di tab pengaturan **Spend limits** workspace di [Claude Console](https://platform.claude.com/settings/workspaces).
* **Rate limits:** Batasi permintaan per menit, token input per menit, atau token output per menit. Tetapkan ini di tab pengaturan **Rate limits** workspace di [Claude Console](https://platform.claude.com/settings/workspaces).

<Note>
  - Anda tidak dapat menetapkan batas pada Default Workspace
  - Jika tidak ditetapkan, batas workspace sesuai dengan batas organisasi
  - Batas di seluruh organisasi selalu berlaku, bahkan jika batas workspace berjumlah lebih banyak
</Note>

Untuk informasi terperinci tentang batas laju dan cara kerjanya, lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits). Anda juga dapat membaca batas laju organisasi dan workspace Anda saat ini secara terprogram dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Pelacakan penggunaan dan biaya

Lacak penggunaan dan biaya berdasarkan workspace menggunakan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api):

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
group_by[]=workspace_id&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Penggunaan dan biaya yang diatribusikan ke Default Workspace memiliki nilai `null` untuk `workspace_id`.

## Kasus penggunaan umum

### Pemisahan lingkungan

Buat workspaces terpisah untuk pengembangan, staging, dan produksi:

| Workspace   | Tujuan                                                       |
| ----------- | ------------------------------------------------------------ |
| Development | Pengujian dan eksperimen dengan batas laju yang lebih rendah |
| Staging     | Pengujian pra-produksi dengan batas seperti produksi         |
| Production  | Lalu lintas langsung dengan batas laju penuh dan pemantauan  |

### Isolasi tim atau departemen

Tetapkan workspaces ke tim yang berbeda untuk alokasi biaya dan kontrol akses:

* **Tim engineering** dengan akses developer
* **Tim data science** dengan kunci API mereka sendiri
* **Tim support** dengan akses terbatas untuk alat pelanggan

### Organisasi berbasis proyek

Buat workspaces untuk proyek atau produk tertentu untuk melacak penggunaan dan biaya secara terpisah.

## Praktik terbaik

<Steps>
  <Step title="Rencanakan struktur workspace Anda">
    Pertimbangkan bagaimana Anda akan mengatur workspaces sebelum membuatnya. Pikirkan tentang kebutuhan penagihan, kontrol akses, dan pelacakan penggunaan.
  </Step>

  <Step title="Gunakan nama yang bermakna">
    Beri nama workspaces dengan jelas untuk menunjukkan tujuannya (misalnya, "Production - Customer Chatbot" atau "Dev - Internal Tools").
  </Step>

  <Step title="Tetapkan batas yang sesuai">
    Konfigurasikan batas pengeluaran dan batas laju untuk mencegah biaya tak terduga dan memastikan distribusi sumber daya yang adil.
  </Step>

  <Step title="Audit akses secara teratur">
    Tinjau keanggotaan workspace secara berkala untuk memastikan hanya pengguna yang sesuai yang memiliki akses.
  </Step>

  <Step title="Pantau penggunaan">
    Gunakan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) untuk melacak konsumsi tingkat workspace.
  </Step>
</Steps>

## FAQ

<AccordionGroup>
  <Accordion title="Apa itu Default Workspace?">
    Setiap organisasi memiliki "Default Workspace" yang tidak dapat diganti namanya, diarsipkan, atau dihapus. Seperti setiap workspace, workspace ini memiliki ID `wrkspc_`: API mengembalikannya dalam [header respons `anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response), dan Anda dapat meneruskannya ke [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve) dan [Update Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/update). Workspace ini tidak memiliki daftar anggota sendiri, karena akses ke workspace ini mengikuti peran organisasi setiap anggota. Workspace ini hanya muncul dalam hasil [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) ketika Anda meneruskan `include_default=true`, dan kunci API, laporan penggunaan, serta laporan biaya yang dimilikinya menampilkan `null` untuk `workspace_id`, begitu pula kunci API untuk semua workspace; field `scope` pada kunci API membedakan keduanya dan, untuk kunci yang dimiliki oleh Default Workspace, memuat ID sebenarnya.
  </Accordion>

  <Accordion title="Apa itu workspace Claude Code?">
    Anthropic membuat workspace Claude Code secara otomatis pertama kali anggota organisasi Anda masuk ke Claude Code dengan akun Console mereka. Ia mengisolasi kunci API, penggunaan, dan batas laju Claude Code dari beban kerja Anda yang lain. Lihat [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace) untuk detailnya.
  </Accordion>

  <Accordion title="Apakah ada batas pada workspaces?">
    Ya. Setiap organisasi dapat memiliki hingga 100 workspaces secara default, dan workspaces yang diarsipkan tidak dihitung terhadap batas ini. Jika Anda membutuhkan lebih banyak, hubungi tim akun Anda.
  </Accordion>

  <Accordion title="Bagaimana peran organisasi memengaruhi akses workspace?">
    Admin organisasi secara otomatis mendapatkan peran Workspace Admin di semua workspaces. Anggota penagihan organisasi secara otomatis mendapatkan peran Workspace Billing. Pengguna dan developer organisasi harus ditambahkan secara manual ke setiap workspace.
  </Accordion>

  <Accordion title="Peran mana yang dapat ditetapkan di workspaces?">
    Pengguna dan developer organisasi dapat ditetapkan peran Workspace Admin, Workspace Developer, Workspace Limited Developer, atau Workspace User. Peran Workspace Billing tidak dapat ditetapkan secara manual; ia diwarisi dari memiliki peran `billing` organisasi.
  </Accordion>

  <Accordion title="Dapatkah peran workspace admin organisasi atau anggota penagihan diubah?">
    Admin organisasi dan anggota penagihan tidak dapat mengubah peran workspace mereka atau dihapus dari workspaces selama mereka memegang peran organisasi tersebut (dengan satu pengecualian: anggota penagihan dapat ditingkatkan ke peran Workspace Admin). Untuk semua orang lain yang tercakup oleh batasan ini, ubah peran organisasi mereka terlebih dahulu untuk mengubah akses workspace mereka.
  </Accordion>

  <Accordion title="Apa yang terjadi pada akses workspace ketika peran organisasi berubah?">
    Jika admin organisasi atau anggota penagihan diturunkan menjadi pengguna atau developer, mereka kehilangan akses ke semua workspaces kecuali yang peran mereka ditetapkan secara manual. Ketika pengguna dipromosikan ke peran admin atau penagihan, mereka mendapatkan akses otomatis ke semua workspaces.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API ketika pengguna dihapus dari workspace?">
    Perilaku bergantung pada [jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types).

    Kunci akun pribadi atau layanan berhenti bekerja di workspace segera setelah pengguna atau akun layanannya dihapus darinya. Kunci akun layanan tetap bekerja bahkan jika pengguna yang membuatnya dihapus. Kunci API workspace terus bekerja. Di [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), setiap kunci terikat ke anggota yang membuatnya dan berhenti bekerja ketika anggota tersebut dihapus.

    Kunci pribadi diarsipkan ketika penggunanya dihapus dari organisasi. Jika pengguna diundang kembali, mereka perlu membuat kunci baru; kunci yang diarsipkan tidak dipulihkan.
  </Accordion>
</AccordionGroup>

## Lihat juga

* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/organization)
* [Batas laju](https://platform.claude.com/docs/id/api/rate-limits)
* [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api)
