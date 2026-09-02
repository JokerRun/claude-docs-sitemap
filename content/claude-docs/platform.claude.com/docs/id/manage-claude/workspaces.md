---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workspaces
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d2e9217091598ea34a291548cdfcc80febb16aac50bb6b64754f8b7be56589c4
---

---
title: Workspace
url: https://platform.claude.com/docs/id/manage-claude/workspaces
description: Atur kunci API, kelola akses tim, dan kendalikan biaya dengan workspace.
---

Workspace menyediakan cara untuk mengatur penggunaan API Anda dalam sebuah organisasi. Gunakan workspace untuk memisahkan berbagai proyek, lingkungan, atau tim sambil tetap mempertahankan penagihan dan administrasi yang terpusat.

## Cara kerja workspace

Setiap organisasi memiliki **Default Workspace** yang tidak dapat diubah namanya, diarsipkan, atau dihapus. Saat Anda membuat workspace tambahan, Anda dapat menetapkan anggota, service account, kunci API, dan batas sumber daya untuk masing-masing workspace.

Karakteristik utama:

* **Pengenal workspace** menggunakan prefiks `wrkspc_` (misalnya, `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`)
* **Maksimum 100 workspace** per organisasi secara default (workspace yang diarsipkan tidak dihitung); hubungi tim akun Anda jika Anda membutuhkan lebih banyak
* **Default Workspace** memiliki ID `wrkspc_` seperti workspace lainnya (dikembalikan dalam [header respons `anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response) dan diterima oleh [Get Workspace](https://platform.claude.com/docs/id/api/admin/workspaces/retrieve)), tetapi tidak muncul dalam hasil [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list), dan kunci API, laporan penggunaan, serta laporan biaya menampilkan `null` untuk `workspace_id`-nya, begitu pula kunci API semua-workspace (field `scope` pada kunci API membedakan keduanya; untuk kunci yang terikat pada Default Workspace, field tersebut memuat ID yang sebenarnya)
* **Kunci API** dapat dibatasi cakupannya ke satu workspace. Dalam hal ini, kunci tersebut hanya dapat mengakses sumber daya di dalam workspace itu. Beberapa kunci API dapat diberi izin di beberapa workspace, dan menyertakan [header ID workspace](https://platform.claude.com/docs/id/manage-claude/authentication#select-a-workspace) untuk mengakses sumber daya di dalam workspace tersebut

### Workspace Claude Code

Ketika seorang anggota organisasi Anda pertama kali masuk ke [Claude Code](https://code.claude.com/docs/en/overview) dengan akun Claude Console mereka, Anthropic secara otomatis membuat workspace **Claude Code** di organisasi tersebut dan menambahkan anggota itu ke dalamnya. Setiap anggota berikutnya yang masuk ke Claude Code ditambahkan dengan cara yang sama.

Workspace Claude Code menjaga lalu lintas Claude Code terpisah dari beban kerja API Anda yang lain:

* Claude Code membuat kunci API per pengguna di workspace ini saat masuk. Anda tidak dapat membuat kunci di dalamnya secara manual dari Console.
* Kunci Claude Code berhenti berfungsi jika pemiliknya dihapus dari workspace atau organisasi, tidak seperti kunci workspace.
* Penggunaan Claude Code dikenai "rate limit" (batas laju) secara terpisah, dan admin dapat membatasi porsinya dari batas organisasi di [Settings > Workspaces](https://platform.claude.com/settings/workspaces).
* Ini adalah satu-satunya workspace yang mendukung batas pengeluaran bulanan per pengguna.

<Warning>
  Mengarsipkan workspace Claude Code akan menonaktifkan proses masuk Claude Code melalui penagihan Console untuk seluruh organisasi.
</Warning>

## Peran dan izin workspace

Anggota dapat memiliki peran yang berbeda di setiap workspace, sehingga memungkinkan kontrol akses yang terperinci.

| Peran                       | Izin                                                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Workspace User              | Hanya menggunakan playground                                                                                         |
| Workspace Limited Developer | Membuat dan mengelola kunci API, menggunakan API. Tidak dapat mengakses tampilan pelacakan sesi atau mengunduh file. |
| Workspace Developer         | Membuat dan mengelola kunci API, menggunakan API                                                                     |
| Workspace Admin             | Kontrol penuh atas pengaturan dan anggota workspace                                                                  |
| Workspace Billing           | Melihat informasi penagihan workspace (diwarisi dari peran billing organisasi)                                       |

### Pewarisan peran

* **Admin organisasi** secara otomatis menerima akses Workspace Admin ke semua workspace
* **Anggota billing organisasi** secara otomatis menerima akses Workspace Billing ke semua workspace
* **User dan developer organisasi** harus ditambahkan secara eksplisit ke setiap workspace
* **Service account** ditambahkan ke workspace dari halaman service account di [Settings → Service accounts](https://platform.claude.com/settings/service-accounts) atau dari tab **Service accounts** pada workspace

<Note>
  Peran Workspace Billing tidak dapat ditetapkan secara manual. Peran ini diwarisi dari kepemilikan peran billing organisasi.
</Note>

## Mengelola workspace

<Note>
  Hanya admin organisasi yang dapat membuat workspace. User dan developer organisasi harus ditambahkan ke workspace oleh admin.
</Note>

### Menggunakan Console

Buat dan kelola workspace di [Claude Console](https://platform.claude.com/settings/workspaces).

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

  <Step title="Buat workspace tersebut">
    Klik **Create** untuk menyelesaikan.
  </Step>
</Steps>

<Tip>
  Untuk berpindah antar workspace di Console, gunakan pemilih **Workspaces** di sudut kiri atas.
</Tip>

#### Mengedit detail workspace

Untuk mengubah nama atau warna workspace:

1. Pilih workspace dari daftar.
2. Klik menu elipsis (**...**) dan pilih **Edit details**.
3. Perbarui nama atau warna dan simpan perubahan Anda.

<Note>
  Default Workspace tidak dapat diubah namanya atau dihapus.
</Note>

#### Menambahkan anggota ke workspace

1. Buka tab **Members** pada workspace.
2. Klik **Add to Workspace**.
3. Pilih anggota organisasi dan tetapkan [peran workspace](https://platform.claude.com/docs/id/manage-claude/workspaces#workspace-roles-and-permissions) untuk mereka.
4. Konfirmasikan penambahan tersebut.

Untuk menghapus anggota, klik ikon tempat sampah di sebelah nama mereka.

<Note>
  Admin organisasi dan anggota billing tidak dapat dihapus dari workspace selama mereka memegang peran organisasi tersebut.
</Note>

#### Menetapkan batas workspace

Pengaturan setiap workspace membagi batas-batas ini ke dalam dua tab:

* **Batas laju:** Pada tab **Rate limits**, tetapkan batas per tingkat model untuk permintaan per menit, token input, atau token output
* **Batas pengeluaran:** Pada tab **Spend limits**, batasi pengeluaran bulanan dan konfigurasikan peringatan ketika pengeluaran mencapai ambang tertentu

#### Mengarsipkan workspace

Untuk mengarsipkan workspace, klik menu elipsis (**...**) dan pilih **Archive**. Pengarsipan:

* Mempertahankan data historis untuk pelaporan
* Menonaktifkan workspace dan mengarsipkan setiap kunci API yang dibuat untuknya
* Tidak dapat dibatalkan

<Warning>
  Mengarsipkan workspace akan mengarsipkan setiap kunci API yang dibuat untuk workspace tersebut dalam hitungan detik (kunci-kunci itu tetap tercantum di Admin API sebagai diarsipkan), dan kunci multi-workspace tidak dapat lagi beroperasi di dalamnya. Tindakan ini tidak dapat dibatalkan. Jika Anda mengarsipkan [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), anggota organisasi Anda tidak dapat lagi masuk ke Claude Code melalui penagihan Console.
</Warning>

### Menggunakan Admin API

Kelola workspace secara terprogram menggunakan [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api).

<Note>
  Endpoint Admin API menerima [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys), token OAuth `org:admin`, atau kunci personal maupun kunci service account yang tidak dibatasi cakupannya ke workspace tertentu. Kunci workspace tidak berfungsi di sana. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication).
</Note>

Contoh SDK dan CLI berikut membuat client default, yang membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`; SDK mengekspos endpoint ini di bawah `client.beta.organization.workspaces`. Metode list pada SDK mengambil halaman berikutnya sesuai permintaan, sehingga `limit` menetapkan ukuran halaman; contoh PHP, Ruby, dan curl mengembalikan satu halaman.

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
  ant beta:organization:workspaces create --name Production
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.workspaces.create(name="Production")

  print(f"id: {workspace.id}")
  print(f"name: {workspace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.workspaces.create({ name: "Production" });

  console.log(`id: ${workspace.id}`);
  console.log(`name: ${workspace.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.Workspaces.Create(new()
  {
      Name = "Production"
  });

  Console.WriteLine($"id: {workspace.ID}");
  Console.WriteLine($"name: {workspace.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Beta.Organization.Workspaces.New(context.Background(), anthropic.BetaOrganizationWorkspaceNewParams{
  	Name: "Production",
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", workspace.ID)
  fmt.Printf("name: %s\n", workspace.Name)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.workspaces.WorkspaceCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceCreateParams.builder()
          .name("Production")
          .build();
      var workspace = client.beta().organization().workspaces().create(params);

      IO.println("id: " + workspace.id());
      IO.println("name: " + workspace.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->workspaces->create(
      name: 'Production',
  );

  echo "id: {$workspace->id}\n";
  echo "name: {$workspace->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace = client.beta.organization.workspaces.create(name: "Production")

  puts "id: #{workspace.id}"
  puts "name: #{workspace.name}"
  ```
</CodeGroup>

Mendaftar workspace:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces?limit=10&include_archived=false" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:workspaces list --limit 10 --include-archived=false
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspaces = client.beta.organization.workspaces.list(limit=10, include_archived=False)

  for workspace in workspaces:
      print(f"{workspace.id}: {workspace.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspaces = await client.beta.organization.workspaces.list({
    limit: 10,
    include_archived: false
  });

  for await (const workspace of workspaces) {
    console.log(`${workspace.id}: ${workspace.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspaces = await client.Beta.Organization.Workspaces.List(new()
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

  workspaces := client.Beta.Organization.Workspaces.ListAutoPaging(context.Background(), anthropic.BetaOrganizationWorkspaceListParams{
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
  import com.anthropic.models.beta.organization.workspaces.WorkspaceListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = WorkspaceListParams.builder()
          .limit(10)
          .includeArchived(false)
          .build();
      var workspaces = client.beta().organization().workspaces().list(params);

      for (var workspace : workspaces.autoPager()) {
          IO.println(workspace.id() + ": " + workspace.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $workspaces = $client->beta->organization->workspaces->list(
      limit: 10,
      includeArchived: false,
  );

  foreach ($workspaces->getItems() as $workspace) {
      echo "{$workspace->id}: {$workspace->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspaces = client.beta.organization.workspaces.list(limit: 10, include_archived: false)

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
  ant beta:organization:workspaces archive --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  workspace = client.beta.organization.workspaces.archive(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  print(f"id: {workspace.id}")
  print(f"archived_at: {workspace.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const workspace = await client.beta.organization.workspaces.archive(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  console.log(`id: ${workspace.id}`);
  console.log(`archived_at: ${workspace.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var workspace = await client.Beta.Organization.Workspaces.Archive(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  Console.WriteLine($"id: {workspace.ID}");
  Console.WriteLine($"archived_at: {workspace.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  workspace, err := client.Beta.Organization.Workspaces.Archive(context.Background(), "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", workspace.ID)
  fmt.Printf("archived_at: %s\n", workspace.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var workspace = client.beta().organization().workspaces()
      .archive("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ");

  IO.println("id: " + workspace.id());
  IO.println("archived_at: " + workspace.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $workspace = $client->beta->organization->workspaces->archive(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  echo "id: {$workspace->id}\n";
  echo "archived_at: {$workspace->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  workspace = client.beta.organization.workspaces.archive(workspace_id)

  puts "id: #{workspace.id}"
  puts "archived_at: #{workspace.archived_at}"
  ```
</CodeGroup>

Untuk detail parameter lengkap dan skema respons, lihat [referensi Workspaces API](https://platform.claude.com/docs/id/api/admin/workspaces/retrieve).

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

Menghapus anggota dari workspace:

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
      "user_01XyDMpzjS89pFZXqSFUBDr6",
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
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

Untuk detail parameter lengkap, lihat [referensi Workspace Members API](https://platform.claude.com/docs/id/api/admin/workspaces/members/retrieve).

## Kunci API dan cakupan sumber daya

Setiap permintaan berjalan di tepat satu workspace dan hanya dapat mengakses sumber daya di dalam workspace tersebut. Workspace mana yang digunakan bergantung pada [jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types):

* **Kunci workspace** (kunci lama tanpa pemilik) milik workspace tempat kunci itu dibuat dan selalu berjalan di sana.
* **Kunci personal** atau **kunci service account** bertindak sebagai pengguna atau service account-nya. Kunci satu-workspace selalu berjalan di workspace yang dipilih saat kunci itu dibuat. Kunci multi-workspace berjalan di workspace yang disebutkan oleh header `anthropic-workspace-id` pada setiap permintaan. Akun harus memiliki akses ke workspace tersebut untuk menggunakannya.

Sumber daya yang dibatasi cakupannya ke workspace meliputi:

* **File** yang dibuat melalui [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* **Message Batches** yang dibuat melalui [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* **Skills** yang dibuat melalui [Skills API](https://platform.claude.com/docs/id/build-with-claude/skills-guide)

Beberapa sumber daya dikelola secara berbeda:

* **[MCP tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview)** dikelola dengan token OAuth `workspace:manage_tunnels` yang diperoleh melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation), bukan kunci API. Tunnel dibuat di dalam sebuah workspace, dan daftar **MCP tunnels** di Console serta pemilih server Managed Agent hanya menampilkan tunnel di workspace saat ini; batas 10 tunnel aktif berlaku untuk seluruh organisasi. Pengelolaan tunnel memerlukan peran dengan izin pengelolaan tunnel; developer organisasi dapat melihat tetapi tidak dapat mengubahnya.
* **Workspace** itu sendiri dan **anggota organisasi** dikelola di tingkat organisasi melalui [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api), menggunakan kunci Admin API, token OAuth `org:admin`, atau kunci personal maupun kunci service account yang tidak dibatasi cakupannya ke workspace tertentu.

Untuk mencari ID workspace organisasi Anda, panggil endpoint [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list) atau temukan di [Claude Console](https://platform.claude.com/settings/workspaces).

<Note>
  [Cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) juga diisolasi per workspace pada Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Pada Amazon Bedrock dan Google Cloud, cache prompt diisolasi per organisasi.
</Note>

## Mengidentifikasi workspace di balik respons API

Respons Claude API menyertakan header `anthropic-workspace-id` bersama dengan [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) `request-id` dan `anthropic-organization-id`. Nilainya adalah ID berprefiks `wrkspc_` dari workspace yang menjadi tujuan resolusi kunci API atau access token permintaan tersebut, termasuk ketika workspace itu adalah Default Workspace. Misalnya, respons yang berhasil menyertakan header seperti ini:

```http
HTTP/1.1 200 OK
request-id: req_018EeWyXxfu5pfWkrYcMdjWG
anthropic-organization-id: 0d0e7a3b-52f1-4c7e-9a51-3f6f2f7c1b9e
anthropic-workspace-id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
```

Header ini tidak ada ketika kredensial tidak teresolusi ke sebuah workspace (misalnya, pada permintaan Admin API) atau ketika permintaan gagal sebelum autentikasi selesai, seperti error 401.

Contoh berikut mengirim permintaan Messages API dan mencetak ID workspace dari header respons:

<CodeGroup>
  ```bash cURL
  # -D - mencetak header respons; -o /dev/null membuang body
  curl -sS -D - -o /dev/null https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | grep -i '^anthropic-workspace-id'
  ```

  ```bash CLI
  # --debug mencetak respons HTTP, termasuk header Anthropic-Workspace-Id,
  # ke stderr; > /dev/null menyembunyikan body JSON di stdout
  ant --debug messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' > /dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.with_raw_response.create(
      model="claude-opus-5",
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
      model: "claude-opus-5",
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
      Model = Model.ClaudeOpus5,
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
  		Model:     anthropic.ModelClaudeOpus5,
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
              .model(Model.CLAUDE_OPUS_5)
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
      'model' => Model::CLAUDE_OPUS_5,
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
    # Kunci dalam response.headers menggunakan huruf kecil
    workspace_id = response.headers["anthropic-workspace-id"]
    response
  end

  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5,
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

Accessor yang sama juga membaca header ini dari endpoint Claude API lainnya, termasuk API [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview). Misalnya, baca `anthropic-workspace-id` dari respons yang [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions) untuk mencatat workspace mana yang memiliki sesi tersebut.

Dengan ID workspace dari sebuah respons, Anda dapat:

* Mengonfirmasi penggunaan, biaya, dan [batas laju](https://platform.claude.com/docs/id/api/rate-limits) workspace mana yang diperhitungkan untuk permintaan tersebut
* Mencocokkannya dengan field `workspace_id` dalam laporan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) dan pada objek [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) seperti kunci API (keduanya melaporkan `null` untuk Default Workspace, seperti halnya kunci API untuk kunci semua-workspace; field `scope` pada kunci API membedakan keduanya dan, untuk kunci yang terikat pada satu workspace, memuat ID sebenarnya dari workspace tersebut)
* Memeriksa apakah itu ID Default Workspace Anda dengan meneruskannya ke [Get Workspace](https://platform.claude.com/docs/id/api/admin/workspaces/retrieve) menggunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys): Default Workspace dikembalikan dengan `"name": "Default"`, meskipun [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list) tidak menyertakannya
* Membuka workspace tersebut di [Console](https://platform.claude.com/settings/workspaces) untuk menemukan sumber daya permintaan itu, seperti sesi, file, message batch, dan skill

## Batas workspace

Anda dapat menetapkan batas pengeluaran dan batas laju khusus untuk setiap workspace guna melindungi dari penggunaan berlebih dan memastikan distribusi sumber daya yang adil.

### Menetapkan batas workspace

Anda dapat menetapkan batas workspace lebih rendah dari (tetapi tidak lebih tinggi dari) batas organisasi Anda:

* **Batas pengeluaran:** Batasi pengeluaran bulanan untuk sebuah workspace. Tetapkan ini pada tab pengaturan **Spend limits** workspace di [Claude Console](https://platform.claude.com/settings/workspaces).
* **Batas laju:** Batasi permintaan per menit, token input per menit, atau token output per menit. Tetapkan ini pada tab pengaturan **Rate limits** workspace di [Claude Console](https://platform.claude.com/settings/workspaces).

<Note>
  - Anda tidak dapat menetapkan batas pada Default Workspace
  - Jika tidak ditetapkan, batas workspace sama dengan batas organisasi
  - Batas seluruh organisasi selalu berlaku, meskipun jumlah batas workspace lebih besar
</Note>

Untuk informasi terperinci tentang batas laju dan cara kerjanya, lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits). Anda juga dapat membaca batas laju organisasi dan workspace Anda saat ini secara terprogram dengan [Rate Limits API](https://platform.claude.com/docs/id/manage-claude/rate-limits-api).

## Pelacakan penggunaan dan biaya

Lacak penggunaan dan biaya per workspace menggunakan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api):

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

Buat workspace terpisah untuk development, staging, dan production:

| Workspace   | Tujuan                                                       |
| ----------- | ------------------------------------------------------------ |
| Development | Pengujian dan eksperimen dengan batas laju yang lebih rendah |
| Staging     | Pengujian pra-produksi dengan batas yang menyerupai produksi |
| Production  | Lalu lintas langsung dengan batas laju penuh dan pemantauan  |

### Isolasi tim atau departemen

Tetapkan workspace ke tim yang berbeda untuk alokasi biaya dan kontrol akses:

* **Tim engineering** dengan akses developer
* **Tim data science** dengan kunci API mereka sendiri
* **Tim support** dengan akses terbatas untuk alat pelanggan

### Pengaturan berbasis proyek

Buat workspace untuk proyek atau produk tertentu guna melacak penggunaan dan biaya secara terpisah.

## Praktik terbaik

<Steps>
  <Step title="Rencanakan struktur workspace Anda">
    Pertimbangkan bagaimana Anda akan mengatur workspace sebelum membuatnya. Pikirkan kebutuhan penagihan, kontrol akses, dan pelacakan penggunaan.
  </Step>

  <Step title="Gunakan nama yang bermakna">
    Beri nama workspace dengan jelas untuk menunjukkan tujuannya (misalnya, "Production - Customer Chatbot" atau "Dev - Internal Tools").
  </Step>

  <Step title="Tetapkan batas yang sesuai">
    Konfigurasikan batas pengeluaran dan batas laju untuk mencegah biaya tak terduga dan memastikan distribusi sumber daya yang adil.
  </Step>

  <Step title="Audit akses secara berkala">
    Tinjau keanggotaan workspace secara berkala untuk memastikan hanya pengguna yang sesuai yang memiliki akses.
  </Step>

  <Step title="Pantau penggunaan">
    Gunakan [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) untuk melacak konsumsi di tingkat workspace.
  </Step>
</Steps>

## FAQ

<AccordionGroup>
  <Accordion title="Apa itu Default Workspace?">
    Setiap organisasi memiliki "Default Workspace" yang tidak dapat diubah namanya, diarsipkan, atau dihapus. Seperti setiap workspace, ia memiliki ID `wrkspc_`: API mengembalikannya dalam [header respons `anthropic-workspace-id`](https://platform.claude.com/docs/id/manage-claude/workspaces#identify-the-workspace-behind-an-api-response), dan Anda dapat meneruskannya ke [Get Workspace](https://platform.claude.com/docs/id/api/admin/workspaces/retrieve) dan [Update Workspace](https://platform.claude.com/docs/id/api/admin/workspaces/update). Ia tidak memiliki daftar anggota sendiri, karena akses ke dalamnya mengikuti peran organisasi setiap anggota. Ia tidak muncul dalam hasil [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list), dan kunci API, laporan penggunaan, serta laporan biaya yang menjadi miliknya menampilkan `null` untuk `workspace_id`, begitu pula kunci API semua-workspace; field `scope` pada kunci API membedakan keduanya dan, untuk kunci yang menjadi milik Default Workspace, memuat ID sebenarnya.
  </Accordion>

  <Accordion title="Apa itu workspace Claude Code?">
    Anthropic membuat workspace Claude Code secara otomatis saat pertama kali seorang anggota organisasi Anda masuk ke Claude Code dengan akun Console mereka. Workspace ini mengisolasi kunci API, penggunaan, dan batas laju Claude Code dari beban kerja Anda yang lain. Lihat [Workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace) untuk detailnya.
  </Accordion>

  <Accordion title="Apakah ada batasan pada workspace?">
    Ya. Setiap organisasi dapat memiliki hingga 100 workspace secara default, dan workspace yang diarsipkan tidak dihitung terhadap batas ini. Jika Anda membutuhkan lebih banyak, hubungi tim akun Anda.
  </Accordion>

  <Accordion title="Bagaimana peran organisasi memengaruhi akses workspace?">
    Admin organisasi secara otomatis mendapatkan peran Workspace Admin di semua workspace. Anggota billing organisasi secara otomatis mendapatkan peran Workspace Billing. User dan developer organisasi harus ditambahkan secara manual ke setiap workspace.
  </Accordion>

  <Accordion title="Peran apa saja yang dapat ditetapkan di workspace?">
    User dan developer organisasi dapat diberi peran Workspace Admin, Workspace Developer, Workspace Limited Developer, atau Workspace User. Peran Workspace Billing tidak dapat ditetapkan secara manual; peran ini diwarisi dari kepemilikan peran `billing` organisasi.
  </Accordion>

  <Accordion title="Dapatkah peran workspace admin organisasi atau anggota billing diubah?">
    Admin organisasi dan anggota billing tidak dapat diubah peran workspace-nya atau dihapus dari workspace selama mereka memegang peran organisasi tersebut (dengan satu pengecualian: anggota billing dapat ditingkatkan ke peran Workspace Admin). Untuk semua orang lain yang tercakup oleh batasan ini, ubah peran organisasi mereka terlebih dahulu untuk mengubah akses workspace mereka.
  </Accordion>

  <Accordion title="Apa yang terjadi pada akses workspace ketika peran organisasi berubah?">
    Jika admin organisasi atau anggota billing diturunkan menjadi user atau developer, mereka kehilangan akses ke semua workspace kecuali workspace tempat mereka ditetapkan perannya secara manual. Ketika pengguna dipromosikan ke peran admin atau billing, mereka mendapatkan akses otomatis ke semua workspace.
  </Accordion>

  <Accordion title="Apa yang terjadi pada kunci API ketika pengguna dihapus dari workspace?">
    Perilakunya bergantung pada [jenis kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-types).

    Kunci personal atau kunci service account berhenti berfungsi di sebuah workspace tak lama setelah pengguna atau service account-nya dihapus dari workspace tersebut. Kunci service account tetap berfungsi meskipun pengguna yang membuatnya dihapus. Kunci API workspace tetap berfungsi. Di [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), setiap kunci terikat pada anggota yang membuatnya dan berhenti berfungsi ketika anggota tersebut dihapus.

    Kunci personal diarsipkan ketika penggunanya dihapus dari organisasi. Jika pengguna tersebut diundang kembali, mereka perlu membuat kunci baru; kunci yang diarsipkan tidak dipulihkan.
  </Accordion>
</AccordionGroup>

## Lihat juga

* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/admin)
* [Batas laju](https://platform.claude.com/docs/id/api/rate-limits)
* [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api)
