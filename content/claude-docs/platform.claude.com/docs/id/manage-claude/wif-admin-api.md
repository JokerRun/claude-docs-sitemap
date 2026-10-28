---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-admin-api
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: 8d466e55ccee84202a88a85fa7e778be05824e8e77857a4b6625bc4d4d88defe
---

---
title: Mengelola WIF dengan Admin API
url: https://platform.claude.com/docs/id/manage-claude/wif-admin-api
description: Buat dan kelola akun layanan, penerbit, dan aturan Workload Identity Federation secara terprogram untuk alur kerja infrastructure-as-code dan CI.
---

Admin API memungkinkan Anda membuat dan mengelola sumber daya [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) secara terprogram: akun layanan, penerbit federasi, dan aturan federasi. Gunakan API ini untuk menyimpan konfigurasi federasi Anda sebagai “infrastructure as code” (infrastruktur sebagai kode), menyediakannya dari CI, dan mereproduksinya di berbagai organisasi alih-alih mengklik satu per satu di Claude Console. Endpoint ini berbagi awalan path `/v1/organizations` dengan bagian lain dari [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api).

## Prasyarat

Setiap permintaan di halaman ini diautentikasi dengan “bearer token” (token pembawa) OAuth yang membawa scope `org:admin`. Scope ini hanya diberikan kepada anggota organisasi dengan peran admin, owner, atau primary owner, dan memberikan akses ke seluruh organisasi: setiap pengikatan workspace diabaikan. Ada dua cara untuk memperoleh token, dan keduanya membawa izin yang berbeda: token dari login Anda sendiri bertindak sebagai pengguna, sedangkan token terfederasi bertindak sebagai akun layanan dan tidak dapat melakukan setiap operasi di halaman ini.

### Interaktif (terminal Anda)

Login dengan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) di bawah profil khusus, dengan meminta scope `org:admin` (lihat [Akses admin](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor bearer token. Login dengan `--profile admin` menyimpan kredensial `org:admin` di bawah nama profilnya sendiri dan juga menjadikannya profil aktif CLI, dan variabel yang diekspor berlaku untuk setiap panggilan SDK dan CLI di shell tersebut; jadi gunakan shell yang Anda khususkan untuk administrasi, hapus variabel tersebut setelah selesai, dan alihkan CLI kembali dengan `ant profile activate default`:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_AUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek; jika permintaan mulai mengembalikan 401, jalankan ulang perintah ekspor (perintah ini menyegarkan token secara otomatis).

SDK dan CLI `ant` membaca `ANTHROPIC_AUTH_TOKEN` secara otomatis; biarkan `ANTHROPIC_API_KEY` tidak diatur di shell yang sama, karena endpoint ini menolak kunci API dan setiap klien menggunakan kunci tersebut ketika keduanya diatur.

### Workload (CI dan otomatisasi)

Buat aturan federasi dengan `oauth_scope: org:admin` yang menargetkan akun layanan yang `organization_role`-nya adalah `admin`. Aturan itu sendiri harus dibuat di Claude Console: memberikan akses admin organisasi kepada sebuah workload adalah tindakan manusia yang disengaja, bukan sesuatu yang dapat di-bootstrap sendiri oleh otomatisasi. Bagian berikutnya menjelaskan penyiapan satu kali per organisasi ini.

## Bootstrap workload untuk mengelola WIF

Satu aturan yang dibuat di Console sudah cukup untuk menempatkan sisa konfigurasi federasi Anda di bawah infrastructure as code: berikan scope `org:admin` kepada satu workload tepercaya, dan biarkan workload tersebut mengelola penerbit federasi dan setiap aturan federasi berlingkup workspace melalui API ini.

<Steps>
  <Step title="Buat aturan org:admin di Console">
    Di Claude Console, buka halaman [Workload identity](https://platform.claude.com/settings/workload-identity-federation) (`platform.claude.com/settings/workload-identity-federation`) dan pilih **Connect workload** untuk membuat satu aturan federasi bagi workload otomatisasi Anda, misalnya workflow GitHub Actions di repositori infrastruktur Anda. Di bawah **Advanced rule options**, atur scope OAuth aturan ke `org:admin`: wizard kemudian membuat akun layanan baru dengan peran organisasi Admin (atau meminta Anda memilih akun layanan admin yang sudah ada sebagai target).

    <Warning>
      Cocokkan aturan dengan satu identitas workload yang persis, bukan pola yang luas. `subject_prefix` adalah pencocokan persis kecuali diakhiri dengan `*`. Untuk GitHub Actions, sematkan subject ke branch yang dilindungi, seperti `repo:my-org/my-repo:ref:refs/heads/main`. Wildcard di akhir seperti `repo:my-org/my-repo:*` juga cocok dengan run `pull_request`, termasuk run yang dipicu dari fork, sehingga siapa pun yang dapat membuka pull request terhadap repositori tersebut dapat mencetak token `org:admin`. Lihat [Membatasi workflow mana yang dapat diautentikasi](https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate).
    </Warning>
  </Step>

  <Step title="Tukarkan token identitas workload">
    Workload yang menggunakan salah satu SDK atau CLI `ant` tidak melakukan pertukaran itu sendiri. Arahkan klien ke aturan dengan variabel lingkungan federasi dan buat klien tanpa argumen, persis seperti untuk inferensi di [Membuat klien SDK](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#construct-the-sdk-client); klien menukarkan token identitas pada permintaan pertama dan, sebelum token akses yang dihasilkan kedaluwarsa, membaca ulang token identitas dan menukarkannya lagi:

    ```bash
    export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...        # the org:admin rule from step 1
    export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
    export ANTHROPIC_SERVICE_ACCOUNT_ID=svac_...       # the rule's target service account
    export ANTHROPIC_IDENTITY_TOKEN_FILE=/path/to/jwt  # or ANTHROPIC_IDENTITY_TOKEN
    # ANTHROPIC_WORKSPACE_ID hanya diperlukan jika aturan diaktifkan untuk semua
    # workspace atau lebih dari satu; endpoint org:admin mengabaikan binding tersebut.
    unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN       # both take precedence over federation
    ```

    CLI `ant` membaca variabel yang sama, atau menerima flag `--federation-rule`, `--organization-id`, `--service-account-id`, dan `--identity-token-file`. Untuk workload yang menjalankan lebih dari satu perintah `ant`, gunakan [profil federasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) alih-alih flag atau variabel lingkungan: dengan flag atau variabel, CLI menukarkan token identitas lagi di setiap proses, dan token identitas yang membawa klaim `jti` (token GitHub Actions membawanya) hanya diterima sekali, sehingga perintah kedua akan ditolak; profil juga merupakan satu-satunya cara untuk memberikan `workspace_id` kepada CLI untuk pertukaran ketika aturan diaktifkan untuk semua workspace atau lebih dari satu, karena tidak seperti SDK, CLI tidak meneruskan `ANTHROPIC_WORKSPACE_ID` atau `--workspace-id` ke dalam pertukaran. Setiap SDK juga menerima pengaturan yang sama sebagai argumen konstruktor eksplisit, yang ditunjukkan per bahasa di [Membuat klien SDK](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#construct-the-sdk-client). Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables) dan [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence) untuk daftar lengkap dan urutannya.

    Workload yang memanggil API dengan curl menukarkan JWT dengan bearer token `org:admin` berumur pendek secara mandiri, menggunakan [pertukaran token](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload) yang sama seperti workload terfederasi lainnya, dan mengirimkannya di header `authorization: Bearer`.
  </Step>

  <Step title="Kelola penerbit dan aturan berlingkup workspace melalui API">
    Dengan klien yang telah dikonfigurasi (atau, untuk curl, token yang dicetak di `ANTHROPIC_AUTH_TOKEN`), workload membuat dan mengelola konfigurasi federasi Anda menggunakan endpoint di halaman ini.
  </Step>
</Steps>

Untuk operasi yang dapat dan tidak dapat dilakukan oleh token yang dicetak workload, lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). Jika Anda sudah membuat penerbit, akun layanan, atau aturan dengan wizard **Connect workload**, tampilkan daftarnya dengan endpoint berikut dan impor ke state infrastructure-as-code Anda alih-alih membuatnya ulang.

## Autentikasi

Semua endpoint berada di bawah `https://api.anthropic.com/v1/organizations/`. Setiap permintaan ke endpoint federasi dan akun layanan memerlukan header versi API dan bearer token:

Di SDK, endpoint ini adalah `client.organization.service_accounts` (typescript: `client.organization.serviceAccounts`; csharp, go: `client.Organization.ServiceAccounts`; java: `client.organization().serviceAccounts()`; php: `$client->organization->serviceAccounts`), `client.organization.federation.issuers` (csharp, go: `client.Organization.Federation.Issuers`; java: `client.organization().federation().issuers()`; php: `$client->organization->federation->issuers`), dan `client.organization.federation.rules` (csharp, go: `client.Organization.Federation.Rules`; java: `client.organization().federation().rules()`; php: `$client->organization->federation->rules`) (`ant organization:service-accounts`, `federation:issuers`, dan `federation:rules` di CLI). Contoh SDK dan CLI membuat klien default, yang mengirimkan bearer token dari `ANTHROPIC_AUTH_TOKEN`, atau, dalam workload otomatis, melakukan pertukaran federasi sendiri seperti yang dijelaskan di [Bootstrap workload untuk mengelola WIF](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#bootstrap-a-workload-to-manage-wif). Metode list SDK mengambil halaman berikutnya sesuai permintaan, sehingga `limit` mengatur ukuran halaman; contoh PHP dan Ruby membaca satu halaman.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:service-accounts list
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_accounts = client.organization.service_accounts.list()

  for service_account in service_accounts:
      print(f"{service_account.id}: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const serviceAccount of client.organization.serviceAccounts.list()) {
    console.log(`${serviceAccount.id}: ${serviceAccount.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.ServiceAccounts.List();

  await foreach (var serviceAccount in page.Paginate())
  {
      Console.WriteLine($"{serviceAccount.ID}: {serviceAccount.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccounts := client.Organization.ServiceAccounts.ListAutoPaging(context.Background(), anthropic.OrganizationServiceAccountListParams{})

  for serviceAccounts.Next() {
  	serviceAccount := serviceAccounts.Current()
  	fmt.Printf("%s: %s\n", serviceAccount.ID, serviceAccount.Name)
  }
  if err := serviceAccounts.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var serviceAccounts = client.organization().serviceAccounts().list();

  for (var serviceAccount : serviceAccounts.autoPager()) {
      IO.println(serviceAccount.id() + ": " + serviceAccount.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $serviceAccounts = $client->organization->serviceAccounts->list();

  foreach ($serviceAccounts->getItems() as $serviceAccount) {
      echo "{$serviceAccount->id}: {$serviceAccount->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_accounts = client.organization.service_accounts.list

  service_accounts.data.each do |service_account|
    puts "#{service_account.id}: #{service_account.name}"
  end
  ```
</CodeGroup>

Kunci Admin API tidak diterima pada endpoint ini; contoh `x-api-key` di halaman Admin API tidak berlaku di sini.

## Akun layanan

[Akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts) (`svac_...`) adalah identitas non-manusia yang diperankan oleh token terfederasi. Atur `organization_role` ke `developer`.

Buat akun layanan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "inference-worker",
      "organization_role": "developer"
    }'
  ```

  ```bash CLI
  ant organization:service-accounts create \
    --name inference-worker \
    --organization-role developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_account = client.organization.service_accounts.create(
      name="inference-worker", organization_role="developer"
  )

  print(f"id: {service_account.id}")
  print(f"name: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const serviceAccount = await client.organization.serviceAccounts.create({
    name: "inference-worker",
    organization_role: "developer"
  });

  console.log(`id: ${serviceAccount.id}`);
  console.log(`name: ${serviceAccount.name}`);
  ```

  ```csharp C#
  using Anthropic.Models.Organization.ServiceAccounts;

  AnthropicClient client = new();

  var serviceAccount = await client.Organization.ServiceAccounts.Create(new()
  {
      Name = "inference-worker",
      OrganizationRole = OrganizationRole.Developer
  });

  Console.WriteLine($"id: {serviceAccount.ID}");
  Console.WriteLine($"name: {serviceAccount.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccount, err := client.Organization.ServiceAccounts.New(context.Background(), anthropic.OrganizationServiceAccountNewParams{
  	Name:             "inference-worker",
  	OrganizationRole: anthropic.OrganizationServiceAccountNewParamsOrganizationRoleDeveloper,
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", serviceAccount.ID)
  fmt.Printf("name: %s\n", serviceAccount.Name)
  ```

  ```java Java
  import com.anthropic.models.organization.serviceaccounts.ServiceAccountCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ServiceAccountCreateParams.builder()
          .name("inference-worker")
          .organizationRole(ServiceAccountCreateParams.OrganizationRole.DEVELOPER)
          .build();
      var serviceAccount = client.organization().serviceAccounts().create(params);

      IO.println("id: " + serviceAccount.id());
      IO.println("name: " + serviceAccount.name());
  }
  ```

  ```php PHP
  use Anthropic\Organization\ServiceAccounts\ServiceAccountCreateParams\OrganizationRole;
  // ...

  $client = new Client();

  $serviceAccount = $client->organization->serviceAccounts->create(
      name: 'inference-worker',
      organizationRole: OrganizationRole::DEVELOPER,
  );

  echo "id: {$serviceAccount->id}\n";
  echo "name: {$serviceAccount->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_account = client.organization.service_accounts.create(
    name: "inference-worker",
    organization_role: :developer
  )

  puts "id: #{service_account.id}"
  puts "name: #{service_account.name}"
  ```
</CodeGroup>

Tampilkan daftar akun layanan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts?limit=20" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:service-accounts list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_accounts = client.organization.service_accounts.list(limit=20)

  for service_account in service_accounts:
      print(f"{service_account.id}: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const serviceAccount of client.organization.serviceAccounts.list({
    limit: 20
  })) {
    console.log(`${serviceAccount.id}: ${serviceAccount.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.ServiceAccounts.List(new() { Limit = 20 });

  await foreach (var serviceAccount in page.Paginate())
  {
      Console.WriteLine($"{serviceAccount.ID}: {serviceAccount.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccounts := client.Organization.ServiceAccounts.ListAutoPaging(context.Background(), anthropic.OrganizationServiceAccountListParams{
  	Limit: anthropic.Int(20),
  })

  for serviceAccounts.Next() {
  	serviceAccount := serviceAccounts.Current()
  	fmt.Printf("%s: %s\n", serviceAccount.ID, serviceAccount.Name)
  }
  if err := serviceAccounts.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.serviceaccounts.ServiceAccountListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ServiceAccountListParams.builder()
          .limit(20)
          .build();
      var serviceAccounts = client.organization().serviceAccounts().list(params);

      for (var serviceAccount : serviceAccounts.autoPager()) {
          IO.println(serviceAccount.id() + ": " + serviceAccount.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $serviceAccounts = $client->organization->serviceAccounts->list(limit: 20);

  foreach ($serviceAccounts->getItems() as $serviceAccount) {
      echo "{$serviceAccount->id}: {$serviceAccount->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_accounts = client.organization.service_accounts.list(limit: 20)

  service_accounts.data.each do |service_account|
    puts "#{service_account.id}: #{service_account.name}"
  end
  ```
</CodeGroup>

Arsipkan akun layanan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/organizations/service_accounts/svac_01ABCDEFabcdef0123456789XY/archive" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:service-accounts archive svac_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_account = client.organization.service_accounts.archive(
      "svac_01ABCDEFabcdef0123456789XY"
  )

  print(f"id: {service_account.id}")
  print(f"archived_at: {service_account.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const serviceAccount = await client.organization.serviceAccounts.archive(
    "svac_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${serviceAccount.id}`);
  console.log(`archived_at: ${serviceAccount.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var serviceAccount = await client.Organization.ServiceAccounts.Archive(
      "svac_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {serviceAccount.ID}");
  Console.WriteLine($"archived_at: {serviceAccount.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccount, err := client.Organization.ServiceAccounts.Archive(
  	context.Background(),
  	"svac_01ABCDEFabcdef0123456789XY",
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", serviceAccount.ID)
  fmt.Printf("archived_at: %s\n", serviceAccount.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var serviceAccount = client.organization().serviceAccounts()
      .archive("svac_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + serviceAccount.id());
  IO.println("archived_at: " + serviceAccount.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $serviceAccount = $client->organization->serviceAccounts->archive(
      serviceAccountID: 'svac_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$serviceAccount->id}\n";
  echo "archived_at: {$serviceAccount->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_account_id = "svac_01ABCDEFabcdef0123456789XY"
  service_account = client.organization.service_accounts.archive(service_account_id)

  puts "id: #{service_account.id}"
  puts "archived_at: #{service_account.archived_at}"
  ```
</CodeGroup>

Endpoint create mengembalikan akun layanan baru:

```json
{
  "id": "svac_...",
  "name": "inference-worker",
  "organization_role": "developer",
  "created_at": "...",
  "type": "service_account",
  "...": "..."
}
```

Untuk membaca atau memperbarui satu akun layanan, gunakan `GET` dan `POST` pada `/v1/organizations/service_accounts/{service_account_id}`. Akun layanan harus menjadi anggota workspace sebelum token terfederasi dapat bertindak di dalamnya. Setiap akun layanan memiliki keanggotaan implisit di workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain dengan `GET`, `POST`, dan `DELETE` pada `/v1/organizations/service_accounts/{service_account_id}/workspaces`, di mana `DELETE` menargetkan `.../workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [Referensi API akun layanan](https://platform.claude.com/docs/id/api/organization/service_accounts).

## Penerbit federasi

[Penerbit federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#federation-issuers) (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Field `jwks` adalah “discriminated union” (union terdiskriminasi) yang mengontrol cara Anthropic mengambil kunci penandatanganan penyedia:

| Nilai `jwks`                             | Kapan digunakan                                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| `{"type": "discovery"}`                  | Penyedia menyajikan `/.well-known/openid-configuration` di URL penerbit.         |
| `{"type": "explicit_url", "url": "..."}` | Arahkan langsung ke endpoint JWKS.                                               |
| `{"type": "inline", "keys": [...]}`      | Unggah set kunci untuk penyedia yang tidak dapat dijangkau dari internet publik. |

Daftarkan penerbit. Contoh ini mendaftarkan GitHub Actions dengan penemuan JWKS:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "github-actions",
      "issuer_url": "https://token.actions.githubusercontent.com",
      "jwks": {"type": "discovery"}
    }'
  ```

  ```bash CLI
  ant organization:federation:issuers create \
    --name github-actions \
    --issuer-url https://token.actions.githubusercontent.com \
    --jwks '{type: discovery}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuer = client.organization.federation.issuers.create(
      name="github-actions",
      issuer_url="https://token.actions.githubusercontent.com",
      jwks={"type": "discovery"},
  )

  print(f"id: {issuer.id}")
  print(f"name: {issuer.name}")
  print(f"issuer_url: {issuer.issuer_url}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const issuer = await client.organization.federation.issuers.create({
    name: "github-actions",
    issuer_url: "https://token.actions.githubusercontent.com",
    jwks: { type: "discovery" }
  });

  console.log(`id: ${issuer.id}`);
  console.log(`name: ${issuer.name}`);
  console.log(`issuer_url: ${issuer.issuer_url}`);
  ```

  ```csharp C#
  using Anthropic.Models.Organization.Federation.Issuers;

  AnthropicClient client = new();

  var issuer = await client.Organization.Federation.Issuers.Create(new()
  {
      Name = "github-actions",
      IssuerUrl = "https://token.actions.githubusercontent.com",
      Jwks = new JwksDiscovery()
  });

  Console.WriteLine($"id: {issuer.ID}");
  Console.WriteLine($"name: {issuer.Name}");
  Console.WriteLine($"issuer_url: {issuer.IssuerUrl}");
  ```

  ```go Go
  client := anthropic.NewClient()

  issuer, err := client.Organization.Federation.Issuers.New(context.Background(), anthropic.OrganizationFederationIssuerNewParams{
  	Name:      "github-actions",
  	IssuerURL: "https://token.actions.githubusercontent.com",
  	JWKS: anthropic.OrganizationFederationIssuerNewParamsJWKSUnion{
  		OfDiscovery: &anthropic.JWKSDiscoveryParam{},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", issuer.ID)
  fmt.Printf("name: %s\n", issuer.Name)
  fmt.Printf("issuer_url: %s\n", issuer.IssuerURL)
  ```

  ```java Java
  import com.anthropic.models.organization.federation.issuers.JwksDiscovery;
  import com.anthropic.models.organization.federation.issuers.IssuerCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IssuerCreateParams.builder()
          .name("github-actions")
          .issuerUrl("https://token.actions.githubusercontent.com")
          .jwks(JwksDiscovery.builder().build())
          .build();
      var issuer = client.organization().federation().issuers().create(params);

      IO.println("id: " + issuer.id());
      IO.println("name: " + issuer.name());
      IO.println("issuer_url: " + issuer.issuerUrl());
  }
  ```

  ```php PHP
  $client = new Client();

  $issuer = $client->organization->federation->issuers->create(
      name: 'github-actions',
      issuerURL: 'https://token.actions.githubusercontent.com',
      jwks: ['type' => 'discovery'],
  );

  echo "id: {$issuer->id}\n";
  echo "name: {$issuer->name}\n";
  echo "issuer_url: {$issuer->issuerURL}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  issuer = client.organization.federation.issuers.create(
    name: "github-actions",
    issuer_url: "https://token.actions.githubusercontent.com",
    jwks: {type: :discovery}
  )

  puts "id: #{issuer.id}"
  puts "name: #{issuer.name}"
  puts "issuer_url: #{issuer.issuer_url}"
  ```
</CodeGroup>

Tampilkan daftar penerbit:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers?limit=20" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:federation:issuers list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuers = client.organization.federation.issuers.list(limit=20)

  for issuer in issuers:
      print(f"{issuer.id}: {issuer.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const issuer of client.organization.federation.issuers.list({ limit: 20 })) {
    console.log(`${issuer.id}: ${issuer.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.Federation.Issuers.List(new() { Limit = 20 });

  await foreach (var issuer in page.Paginate())
  {
      Console.WriteLine($"{issuer.ID}: {issuer.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  issuers := client.Organization.Federation.Issuers.ListAutoPaging(context.Background(), anthropic.OrganizationFederationIssuerListParams{
  	Limit: anthropic.Int(20),
  })

  for issuers.Next() {
  	issuer := issuers.Current()
  	fmt.Printf("%s: %s\n", issuer.ID, issuer.Name)
  }
  if err := issuers.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.federation.issuers.IssuerListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IssuerListParams.builder()
          .limit(20)
          .build();
      var issuers = client.organization().federation().issuers().list(params);

      for (var issuer : issuers.autoPager()) {
          IO.println(issuer.id() + ": " + issuer.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $issuers = $client->organization->federation->issuers->list(limit: 20);

  foreach ($issuers->getItems() as $issuer) {
      echo "{$issuer->id}: {$issuer->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  issuers = client.organization.federation.issuers.list(limit: 20)

  issuers.data.each do |issuer|
    puts "#{issuer.id}: #{issuer.name}"
  end
  ```
</CodeGroup>

Arsipkan penerbit:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/organizations/federation_issuers/fdis_01ABCDEFabcdef0123456789XY/archive" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:federation:issuers archive \
    --federation-issuer-id fdis_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuer = client.organization.federation.issuers.archive(
      "fdis_01ABCDEFabcdef0123456789XY"
  )

  print(f"id: {issuer.id}")
  print(f"archived_at: {issuer.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const issuer = await client.organization.federation.issuers.archive(
    "fdis_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${issuer.id}`);
  console.log(`archived_at: ${issuer.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var issuer = await client.Organization.Federation.Issuers.Archive(
      "fdis_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {issuer.ID}");
  Console.WriteLine($"archived_at: {issuer.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  issuer, err := client.Organization.Federation.Issuers.Archive(
  	context.Background(),
  	"fdis_01ABCDEFabcdef0123456789XY",
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", issuer.ID)
  fmt.Printf("archived_at: %s\n", issuer.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var issuer = client.organization().federation().issuers()
      .archive("fdis_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + issuer.id());
  IO.println("archived_at: " + issuer.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $issuer = $client->organization->federation->issuers->archive(
      federationIssuerID: 'fdis_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$issuer->id}\n";
  echo "archived_at: {$issuer->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  issuer_id = "fdis_01ABCDEFabcdef0123456789XY"
  issuer = client.organization.federation.issuers.archive(issuer_id)

  puts "id: #{issuer.id}"
  puts "archived_at: #{issuer.archived_at}"
  ```
</CodeGroup>

Untuk membaca atau memperbarui satu penerbit, gunakan `GET` dan `POST` pada `/v1/organizations/federation_issuers/{issuer_id}`. Pemanggil OAuth tidak dapat memperbarui penerbit yang mendukung aturan dengan `oauth_scope` selain `workspace:developer` atau `workspace:inference`; lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).

Untuk detail parameter lengkap dan skema respons, lihat [Referensi API penerbit federasi](https://platform.claude.com/docs/id/api/organization/federation/issuers).

## Aturan federasi

[Aturan federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#federation-rules) (`fdrl_...`) mengikat penerbit ke akun layanan: JWT dari penerbit yang memenuhi kondisi pencocokan aturan dapat mencetak token yang bertindak sebagai target aturan. `workspace_id` dalam permintaan create mengaktifkan aturan di workspace tersebut saat pembuatan; tambahkan workspace lain nanti melalui sub-resource `/federation_rules/{rule_id}/workspaces`. Salah satu dari `workspace_id` atau `applies_to_all_workspaces: true` wajib diisi saat create.

Buat aturan. Contoh ini memungkinkan deploy GitHub Actions dari branch main bertindak sebagai akun layanan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "gha-deploy",
      "issuer_id": "fdis_01ABCDEFabcdef0123456789XY",
      "match": {
        "subject_prefix": "repo:my-org/my-repo:ref:refs/heads/main",
        "claims": {"repository_owner": "my-org"}
      },
      "target": {
        "type": "service_account",
        "service_account_id": "svac_01ABCDEFabcdef0123456789XY"
      },
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "oauth_scope": "workspace:developer",
      "token_lifetime_seconds": 600
    }'
  ```

  ```bash CLI
  ant organization:federation:rules create <<'YAML'
  name: gha-deploy
  issuer_id: fdis_01ABCDEFabcdef0123456789XY
  match:
    subject_prefix: "repo:my-org/my-repo:ref:refs/heads/main"
    claims:
      repository_owner: my-org
  target:
    type: service_account
    service_account_id: svac_01ABCDEFabcdef0123456789XY
  workspace_id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  oauth_scope: "workspace:developer"
  token_lifetime_seconds: 600
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  rule = client.organization.federation.rules.create(
      name="gha-deploy",
      issuer_id="fdis_01ABCDEFabcdef0123456789XY",
      match={
          "subject_prefix": "repo:my-org/my-repo:ref:refs/heads/main",
          "claims": {"repository_owner": "my-org"},
      },
      target={
          "type": "service_account",
          "service_account_id": "svac_01ABCDEFabcdef0123456789XY",
      },
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      oauth_scope="workspace:developer",
      token_lifetime_seconds=600,
  )

  print(f"id: {rule.id}")
  print(f"name: {rule.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rule = await client.organization.federation.rules.create({
    name: "gha-deploy",
    issuer_id: "fdis_01ABCDEFabcdef0123456789XY",
    match: {
      subject_prefix: "repo:my-org/my-repo:ref:refs/heads/main",
      claims: { repository_owner: "my-org" }
    },
    target: {
      type: "service_account",
      service_account_id: "svac_01ABCDEFabcdef0123456789XY"
    },
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    oauth_scope: "workspace:developer",
    token_lifetime_seconds: 600
  });

  console.log(`id: ${rule.id}`);
  console.log(`name: ${rule.name}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rule = await client.Organization.Federation.Rules.Create(new()
  {
      Name = "gha-deploy",
      IssuerID = "fdis_01ABCDEFabcdef0123456789XY",
      Match = new()
      {
          SubjectPrefix = "repo:my-org/my-repo:ref:refs/heads/main",
          Claims = new Dictionary<string, string> { ["repository_owner"] = "my-org" }
      },
      Target = new() { ServiceAccountID = "svac_01ABCDEFabcdef0123456789XY" },
      WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      OAuthScope = "workspace:developer",
      TokenLifetimeSeconds = 600
  });

  Console.WriteLine($"id: {rule.ID}");
  Console.WriteLine($"name: {rule.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  rule, err := client.Organization.Federation.Rules.New(context.Background(), anthropic.OrganizationFederationRuleNewParams{
  	Name:     "gha-deploy",
  	IssuerID: "fdis_01ABCDEFabcdef0123456789XY",
  	Match: anthropic.FederationRuleMatchParam{
  		SubjectPrefix: anthropic.String("repo:my-org/my-repo:ref:refs/heads/main"),
  		Claims:        map[string]string{"repository_owner": "my-org"},
  	},
  	Target: anthropic.ServiceAccountTargetParam{
  		ServiceAccountID: "svac_01ABCDEFabcdef0123456789XY",
  	},
  	WorkspaceID:          anthropic.String("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"),
  	OAuthScope:           "workspace:developer",
  	TokenLifetimeSeconds: anthropic.Int(600),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", rule.ID)
  fmt.Printf("name: %s\n", rule.Name)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.organization.federation.rules.FederationRuleMatch;
  import com.anthropic.models.organization.federation.rules.ServiceAccountTarget;
  import com.anthropic.models.organization.federation.rules.RuleCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var match = FederationRuleMatch.builder()
          .subjectPrefix("repo:my-org/my-repo:ref:refs/heads/main")
          .claims(FederationRuleMatch.Claims.builder()
              .putAdditionalProperty("repository_owner", JsonValue.from("my-org"))
              .build())
          .build();
      var params = RuleCreateParams.builder()
          .name("gha-deploy")
          .issuerId("fdis_01ABCDEFabcdef0123456789XY")
          .match(match)
          .target(ServiceAccountTarget.of("svac_01ABCDEFabcdef0123456789XY"))
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .oauthScope("workspace:developer")
          .tokenLifetimeSeconds(600)
          .build();
      var rule = client.organization().federation().rules().create(params);

      IO.println("id: " + rule.id());
      IO.println("name: " + rule.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $rule = $client->organization->federation->rules->create(
      name: 'gha-deploy',
      issuerID: 'fdis_01ABCDEFabcdef0123456789XY',
      match: [
          'subjectPrefix' => 'repo:my-org/my-repo:ref:refs/heads/main',
          'claims' => ['repository_owner' => 'my-org'],
      ],
      target: [
          'type' => 'service_account',
          'serviceAccountID' => 'svac_01ABCDEFabcdef0123456789XY',
      ],
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      oauthScope: 'workspace:developer',
      tokenLifetimeSeconds: 600,
  );

  echo "id: {$rule->id}\n";
  echo "name: {$rule->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rule = client.organization.federation.rules.create(
    name: "gha-deploy",
    issuer_id: "fdis_01ABCDEFabcdef0123456789XY",
    match: {
      subject_prefix: "repo:my-org/my-repo:ref:refs/heads/main",
      claims: {repository_owner: "my-org"}
    },
    target: {
      type: :service_account,
      service_account_id: "svac_01ABCDEFabcdef0123456789XY"
    },
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    oauth_scope: "workspace:developer",
    token_lifetime_seconds: 600
  )

  puts "id: #{rule.id}"
  puts "name: #{rule.name}"
  ```
</CodeGroup>

Tampilkan daftar aturan, secara opsional difilter berdasarkan penerbit:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules?issuer_id=fdis_01ABCDEFabcdef0123456789XY" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:federation:rules list \
    --issuer-id fdis_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  rules = client.organization.federation.rules.list(
      issuer_id="fdis_01ABCDEFabcdef0123456789XY"
  )

  for rule in rules:
      print(f"{rule.id}: {rule.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const rule of client.organization.federation.rules.list({
    issuer_id: "fdis_01ABCDEFabcdef0123456789XY"
  })) {
    console.log(`${rule.id}: ${rule.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Organization.Federation.Rules.List(new()
  {
      IssuerID = "fdis_01ABCDEFabcdef0123456789XY"
  });

  await foreach (var rule in page.Paginate())
  {
      Console.WriteLine($"{rule.ID}: {rule.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rules := client.Organization.Federation.Rules.ListAutoPaging(context.Background(), anthropic.OrganizationFederationRuleListParams{
  	IssuerID: anthropic.String("fdis_01ABCDEFabcdef0123456789XY"),
  })

  for rules.Next() {
  	rule := rules.Current()
  	fmt.Printf("%s: %s\n", rule.ID, rule.Name)
  }
  if err := rules.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.federation.rules.RuleListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RuleListParams.builder()
          .issuerId("fdis_01ABCDEFabcdef0123456789XY")
          .build();
      var rules = client.organization().federation().rules().list(params);

      for (var rule : rules.autoPager()) {
          IO.println(rule.id() + ": " + rule.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rules = $client->organization->federation->rules->list(
      issuerID: 'fdis_01ABCDEFabcdef0123456789XY',
  );

  foreach ($rules->getItems() as $rule) {
      echo "{$rule->id}: {$rule->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rules = client.organization.federation.rules.list(
    issuer_id: "fdis_01ABCDEFabcdef0123456789XY"
  )

  rules.data.each do |rule|
    puts "#{rule.id}: #{rule.name}"
  end
  ```
</CodeGroup>

Arsipkan aturan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/organizations/federation_rules/fdrl_01ABCDEFabcdef0123456789XY/archive" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:federation:rules archive \
    --federation-rule-id fdrl_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  rule = client.organization.federation.rules.archive("fdrl_01ABCDEFabcdef0123456789XY")

  print(f"id: {rule.id}")
  print(f"archived_at: {rule.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rule = await client.organization.federation.rules.archive(
    "fdrl_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${rule.id}`);
  console.log(`archived_at: ${rule.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rule = await client.Organization.Federation.Rules.Archive(
      "fdrl_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {rule.ID}");
  Console.WriteLine($"archived_at: {rule.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  rule, err := client.Organization.Federation.Rules.Archive(
  	context.Background(),
  	"fdrl_01ABCDEFabcdef0123456789XY",
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", rule.ID)
  fmt.Printf("archived_at: %s\n", rule.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rule = client.organization().federation().rules()
      .archive("fdrl_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + rule.id());
  IO.println("archived_at: " + rule.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $rule = $client->organization->federation->rules->archive(
      federationRuleID: 'fdrl_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$rule->id}\n";
  echo "archived_at: {$rule->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rule_id = "fdrl_01ABCDEFabcdef0123456789XY"
  rule = client.organization.federation.rules.archive(rule_id)

  puts "id: #{rule.id}"
  puts "archived_at: #{rule.archived_at}"
  ```
</CodeGroup>

Endpoint list mengembalikan satu halaman aturan dan cursor untuk halaman berikutnya:

```json
{
  "data": [{ "id": "fdrl_...", "name": "gha-deploy", "...": "..." }],
  "next_page": "..."
}
```

Untuk membaca atau memperbarui satu aturan, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}`. Untuk mengelola workspace tempat aturan dapat mencetak token, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}/workspaces`, dan `DELETE` pada `/v1/organizations/federation_rules/{rule_id}/workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [Referensi API aturan federasi](https://platform.claude.com/docs/id/api/organization/federation/rules).

## Izin dan batasan

<Note>
  * Pemanggil yang diautentikasi dengan OAuth hanya dapat membuat atau memodifikasi aturan yang `oauth_scope`-nya adalah `workspace:developer` atau `workspace:inference`. Untuk membuat atau memodifikasi aturan dengan scope lain (seperti `org:admin` atau `workspace:manage_tunnels`), gunakan Console.
  * Pemanggil OAuth tidak dapat memperbarui penerbit federasi yang mendukung aturan dengan `oauth_scope` selain `workspace:developer` atau `workspace:inference` (seperti `org:admin` atau `workspace:manage_tunnels`). Pertimbangkan untuk mendaftarkan penerbit khusus untuk aturan bootstrap agar penerbit di balik aturan berlingkup workspace tetap dapat diperbarui melalui API.
  * Kunci Admin API tidak diterima pada endpoint ini, baik untuk baca maupun tulis; gunakan token OAuth `org:admin`.
</Note>

Aturan dengan `oauth_scope: org:admin` harus menargetkan akun layanan yang `organization_role`-nya adalah `admin`. Nama sumber daya harus cocok dengan `^[a-z0-9-]+$`, terdiri dari 1 hingga 255 karakter, dan unik dalam satu organisasi untuk setiap jenis sumber daya; untuk batasan tingkat field selengkapnya, lihat [Aturan validasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#validation-rules).

## Paginasi dan pengarsipan

Endpoint list akun layanan, penerbit federasi, dan aturan federasi menerima `limit` (1 hingga 100, default 20) dan cursor `page` yang diambil dari respons sebelumnya. Teruskan nilai `next_page` dari respons sebagai parameter query `page` pada permintaan berikutnya. List sub-resource rule-workspaces mengembalikan set lengkap tanpa paginasi. Sumber daya yang diarsipkan disembunyikan dari daftar secara default; teruskan `include_archived=true` untuk menyertakannya.

Pengarsipan adalah “soft delete” (penghapusan lunak) dan bersifat idempoten: mengarsipkan sumber daya yang sudah diarsipkan akan berhasil. Mengarsipkan penerbit atau akun layanan mengembalikan `400` selama aturan federasi yang aktif masih mereferensikannya; arsipkan aturan tersebut terlebih dahulu.

## Lihat juga

* [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation): konsep dan panduan penyiapan di Console
* [Referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference): variabel lingkungan, aturan validasi, scope OAuth, dan kode error
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api): bagian lain dari permukaan manajemen organisasi
* [Referensi Admin API](https://platform.claude.com/docs/id/api/organization): skema permintaan dan respons yang dihasilkan untuk endpoint akun layanan dan federasi
