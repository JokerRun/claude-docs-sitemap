---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-admin-api
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: fd2c9a88056f2e65a075b9ba419945dda8d3bf03d936e7ddbc96f8f2b3515876
---

---
title: Mengelola WIF dengan Admin API
url: https://platform.claude.com/docs/id/manage-claude/wif-admin-api
description: Buat dan kelola akun layanan, issuer, dan aturan Workload Identity Federation secara terprogram untuk alur kerja infrastructure-as-code dan CI.
---

Admin API memungkinkan Anda membuat dan mengelola sumber daya [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) secara terprogram: akun layanan (service account), issuer federasi (federation issuer), dan aturan federasi (federation rule). Gunakan API ini untuk menyimpan konfigurasi federasi Anda sebagai "infrastructure as code" (infrastruktur sebagai kode), memprovisikannya dari CI, dan mereproduksinya di berbagai organisasi alih-alih mengklik melalui Claude Console. Endpoint ini berbagi prefiks path `/v1/organizations` dengan bagian lain dari [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api).

## Prasyarat

Setiap permintaan di halaman ini diautentikasi dengan bearer token OAuth yang membawa scope `org:admin`. Scope ini hanya diberikan kepada anggota organisasi dengan peran admin, owner, atau primary owner, dan memberikan akses ke seluruh organisasi: pengikatan workspace apa pun diabaikan. Ada dua cara untuk memperoleh token, dan keduanya membawa izin yang berbeda: token dari login Anda sendiri bertindak sebagai pengguna, sedangkan token terfederasi bertindak sebagai akun layanan dan tidak dapat melakukan setiap operasi di halaman ini.

### Interaktif (terminal Anda)

Login dengan [CLI `ant`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart) di bawah profil khusus, dengan meminta scope `org:admin` (lihat [Akses admin](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#admin-access)), lalu ekspor bearer token. Login dengan `--profile admin` menyimpan kredensial `org:admin` di bawah nama profilnya sendiri dan juga menjadikannya profil aktif CLI, dan variabel yang diekspor berlaku untuk setiap panggilan SDK dan CLI di shell tersebut; jadi gunakan shell yang Anda khususkan untuk administrasi, hapus variabel tersebut (unset) ketika Anda selesai, dan kembalikan CLI dengan `ant profile activate default`:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_AUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Token interaktif berumur pendek; jika permintaan mulai mengembalikan 401, jalankan ulang perintah ekspor (perintah tersebut memperbarui token secara otomatis).

SDK dan CLI `ant` membaca `ANTHROPIC_AUTH_TOKEN` secara otomatis; biarkan `ANTHROPIC_API_KEY` tidak disetel di shell yang sama, karena endpoint ini menolak kunci API dan beberapa klien lebih memilih kunci tersebut ketika keduanya disetel.

### Workload (CI dan otomatisasi)

Buat aturan federasi dengan `oauth_scope: org:admin` yang menargetkan akun layanan yang `organization_role`-nya adalah `admin`. Aturan itu sendiri harus dibuat di Claude Console: memberikan akses admin organisasi kepada sebuah workload adalah tindakan manusia yang disengaja, bukan sesuatu yang dapat di-bootstrap oleh otomatisasi untuk dirinya sendiri. Bagian berikutnya memandu Anda melalui penyiapan sekali-per-organisasi ini.

## Bootstrap workload untuk mengelola WIF

Satu aturan yang dibuat di Console sudah cukup untuk menempatkan sisa konfigurasi federasi Anda di bawah infrastructure as code: berikan scope `org:admin` kepada satu workload tepercaya, dan biarkan workload tersebut mengelola issuer federasi dan setiap aturan federasi dengan scope workspace melalui API ini.

<Steps>
  <Step title="Buat aturan org:admin di Console">
    Di Claude Console, buka **Settings → Workload identity** dan pilih **Connect workload** untuk membuat satu aturan federasi bagi workload otomatisasi Anda, misalnya alur kerja GitHub Actions di repositori infrastruktur Anda. Di bawah **Advanced rule options**, setel OAuth scope aturan ke `org:admin`: wizard kemudian membuat akun layanan baru dengan peran organisasi Admin (atau meminta Anda memilih akun layanan admin yang sudah ada sebagai target).

    <Warning>
      Cocokkan aturan dengan satu identitas workload yang tepat, bukan pola yang luas. `subject_prefix` adalah pencocokan persis kecuali jika diakhiri dengan `*`. Untuk GitHub Actions, sematkan subject ke branch yang dilindungi, seperti `repo:my-org/my-repo:ref:refs/heads/main`. Wildcard di akhir seperti `repo:my-org/my-repo:*` juga cocok dengan run `pull_request`, termasuk run yang dipicu dari fork, sehingga siapa pun yang dapat membuka pull request terhadap repositori tersebut dapat mencetak token `org:admin`. Lihat [Membatasi alur kerja mana yang dapat melakukan autentikasi](https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate).
    </Warning>
  </Step>

  <Step title="Tukarkan token identitas workload">
    Workload yang menggunakan salah satu SDK atau CLI `ant` tidak melakukan penukaran itu sendiri. Arahkan klien ke aturan dengan variabel lingkungan federasi dan buat klien tanpa argumen, persis seperti untuk inferensi di [Membuat klien SDK](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#construct-the-sdk-client); klien menukarkan token identitas pada permintaan pertama dan, sebelum access token yang dihasilkan kedaluwarsa, membaca ulang token identitas dan menukarkannya lagi:

    ```bash
    export ANTHROPIC_FEDERATION_RULE_ID=fdrl_...        # the org:admin rule from step 1
    export ANTHROPIC_ORGANIZATION_ID=00000000-0000-0000-0000-000000000000
    export ANTHROPIC_SERVICE_ACCOUNT_ID=svac_...       # the rule's target service account
    export ANTHROPIC_IDENTITY_TOKEN_FILE=/path/to/jwt  # or ANTHROPIC_IDENTITY_TOKEN
    # ANTHROPIC_WORKSPACE_ID hanya diperlukan jika aturan diaktifkan untuk semua
    # workspace atau lebih dari satu; endpoint org:admin mengabaikan pengikatan ini.
    unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN       # both take precedence over federation
    ```

    CLI `ant` membaca variabel yang sama, atau menerima flag `--federation-rule`, `--organization-id`, `--service-account-id`, dan `--identity-token-file`. Untuk workload yang menjalankan lebih dari satu perintah `ant`, gunakan [profil federasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file) alih-alih flag atau variabel lingkungan: dengan flag atau variabel, CLI menukarkan token identitas lagi di setiap proses, dan token identitas yang membawa klaim `jti` (token GitHub Actions membawanya) hanya diterima sekali, sehingga perintah kedua akan ditolak; profil juga merupakan satu-satunya cara untuk memberikan `workspace_id` kepada CLI untuk penukaran ketika aturan diaktifkan untuk semua workspace atau lebih dari satu, karena tidak seperti SDK, CLI tidak meneruskan `ANTHROPIC_WORKSPACE_ID` atau `--workspace-id` ke dalam penukaran. Setiap SDK juga menerima pengaturan yang sama sebagai argumen konstruktor eksplisit, yang ditampilkan per bahasa di [Membuat klien SDK](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#construct-the-sdk-client). Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables) dan [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence) untuk daftar lengkap dan urutannya.

    Workload yang memanggil API dengan curl menukarkan sendiri JWT dengan bearer token `org:admin` berumur pendek, menggunakan [penukaran token](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload) yang sama seperti workload terfederasi lainnya, dan mengirimkannya di header `authorization: Bearer`.
  </Step>

  <Step title="Kelola issuer dan aturan dengan scope workspace melalui API">
    Dengan klien yang telah dikonfigurasi (atau, untuk curl, token yang telah dicetak di `ANTHROPIC_AUTH_TOKEN`), workload membuat dan mengelola konfigurasi federasi Anda menggunakan endpoint di halaman ini.
  </Step>
</Steps>

Untuk operasi yang dapat dan tidak dapat dilakukan oleh token yang dicetak workload, lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints). Jika Anda sudah membuat issuer, akun layanan, atau aturan dengan wizard **Connect workload**, daftarkan semuanya dengan endpoint berikut dan impor ke dalam state infrastructure-as-code Anda alih-alih membuatnya ulang.

## Autentikasi

Semua endpoint berada di bawah `https://api.anthropic.com/v1/organizations/`. Setiap permintaan ke endpoint federasi dan akun layanan memerlukan header versi API dan bearer token:

Di SDK, endpoint ini adalah `client.beta.organization.service_accounts`, `client.beta.organization.federation.issuers`, dan `client.beta.organization.federation.rules` (`ant beta:organization:service-accounts`, `federation:issuers`, dan `federation:rules` di CLI). Contoh SDK dan CLI membuat klien default, yang mengirimkan bearer token dari `ANTHROPIC_AUTH_TOKEN`, atau, dalam workload otomatis, melakukan penukaran federasi sendiri seperti yang dijelaskan di [Bootstrap workload untuk mengelola WIF](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#bootstrap-a-workload-to-manage-wif). Metode list SDK mengambil halaman selanjutnya sesuai permintaan, sehingga `limit` menetapkan ukuran halaman; contoh PHP dan Ruby membaca satu halaman.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:service-accounts list
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_accounts = client.beta.organization.service_accounts.list()

  for service_account in service_accounts:
      print(f"{service_account.id}: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const serviceAccount of client.beta.organization.serviceAccounts.list()) {
    console.log(`${serviceAccount.id}: ${serviceAccount.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ServiceAccounts.List();

  await foreach (var serviceAccount in page.Paginate())
  {
      Console.WriteLine($"{serviceAccount.ID}: {serviceAccount.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccounts := client.Beta.Organization.ServiceAccounts.ListAutoPaging(context.Background(), anthropic.BetaOrganizationServiceAccountListParams{})

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

  var serviceAccounts = client.beta().organization().serviceAccounts().list();

  for (var serviceAccount : serviceAccounts.autoPager()) {
      IO.println(serviceAccount.id() + ": " + serviceAccount.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $serviceAccounts = $client->beta->organization->serviceAccounts->list();

  foreach ($serviceAccounts->getItems() as $serviceAccount) {
      echo "{$serviceAccount->id}: {$serviceAccount->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_accounts = client.beta.organization.service_accounts.list

  service_accounts.data.each do |service_account|
    puts "#{service_account.id}: #{service_account.name}"
  end
  ```
</CodeGroup>

Kunci Admin API tidak diterima di endpoint ini; contoh `x-api-key` di halaman Admin API tidak berlaku di sini.

## Akun layanan

[Akun layanan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#service-accounts) (`svac_...`) adalah identitas non-manusia yang diperankan oleh token terfederasi. Setel `organization_role` ke `developer`.

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
  ant beta:organization:service-accounts create \
    --name inference-worker \
    --organization-role developer
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_account = client.beta.organization.service_accounts.create(
      name="inference-worker", organization_role="developer"
  )

  print(f"id: {service_account.id}")
  print(f"name: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const serviceAccount = await client.beta.organization.serviceAccounts.create({
    name: "inference-worker",
    organization_role: "developer"
  });

  console.log(`id: ${serviceAccount.id}`);
  console.log(`name: ${serviceAccount.name}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.ServiceAccounts;

  AnthropicClient client = new();

  var serviceAccount = await client.Beta.Organization.ServiceAccounts.Create(new()
  {
      Name = "inference-worker",
      OrganizationRole = OrganizationRole.Developer
  });

  Console.WriteLine($"id: {serviceAccount.ID}");
  Console.WriteLine($"name: {serviceAccount.Name}");
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccount, err := client.Beta.Organization.ServiceAccounts.New(context.Background(), anthropic.BetaOrganizationServiceAccountNewParams{
  	Name:             "inference-worker",
  	OrganizationRole: anthropic.BetaOrganizationServiceAccountNewParamsOrganizationRoleDeveloper,
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", serviceAccount.ID)
  fmt.Printf("name: %s\n", serviceAccount.Name)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.serviceaccounts.ServiceAccountCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ServiceAccountCreateParams.builder()
          .name("inference-worker")
          .organizationRole(ServiceAccountCreateParams.OrganizationRole.DEVELOPER)
          .build();
      var serviceAccount = client.beta().organization().serviceAccounts().create(params);

      IO.println("id: " + serviceAccount.id());
      IO.println("name: " + serviceAccount.name());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\ServiceAccounts\ServiceAccountCreateParams\OrganizationRole;
  // ...

  $client = new Client();

  $serviceAccount = $client->beta->organization->serviceAccounts->create(
      name: 'inference-worker',
      organizationRole: OrganizationRole::DEVELOPER,
  );

  echo "id: {$serviceAccount->id}\n";
  echo "name: {$serviceAccount->name}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_account = client.beta.organization.service_accounts.create(
    name: "inference-worker",
    organization_role: :developer
  )

  puts "id: #{service_account.id}"
  puts "name: #{service_account.name}"
  ```
</CodeGroup>

Daftarkan akun layanan:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts?limit=20" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:service-accounts list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_accounts = client.beta.organization.service_accounts.list(limit=20)

  for service_account in service_accounts:
      print(f"{service_account.id}: {service_account.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const serviceAccount of client.beta.organization.serviceAccounts.list({
    limit: 20
  })) {
    console.log(`${serviceAccount.id}: ${serviceAccount.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.ServiceAccounts.List(new() { Limit = 20 });

  await foreach (var serviceAccount in page.Paginate())
  {
      Console.WriteLine($"{serviceAccount.ID}: {serviceAccount.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccounts := client.Beta.Organization.ServiceAccounts.ListAutoPaging(context.Background(), anthropic.BetaOrganizationServiceAccountListParams{
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
  import com.anthropic.models.beta.organization.serviceaccounts.ServiceAccountListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = ServiceAccountListParams.builder()
          .limit(20)
          .build();
      var serviceAccounts = client.beta().organization().serviceAccounts().list(params);

      for (var serviceAccount : serviceAccounts.autoPager()) {
          IO.println(serviceAccount.id() + ": " + serviceAccount.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $serviceAccounts = $client->beta->organization->serviceAccounts->list(limit: 20);

  foreach ($serviceAccounts->getItems() as $serviceAccount) {
      echo "{$serviceAccount->id}: {$serviceAccount->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_accounts = client.beta.organization.service_accounts.list(limit: 20)

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
  ant beta:organization:service-accounts archive svac_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  service_account = client.beta.organization.service_accounts.archive(
      "svac_01ABCDEFabcdef0123456789XY"
  )

  print(f"id: {service_account.id}")
  print(f"archived_at: {service_account.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const serviceAccount = await client.beta.organization.serviceAccounts.archive(
    "svac_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${serviceAccount.id}`);
  console.log(`archived_at: ${serviceAccount.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var serviceAccount = await client.Beta.Organization.ServiceAccounts.Archive(
      "svac_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {serviceAccount.ID}");
  Console.WriteLine($"archived_at: {serviceAccount.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  serviceAccount, err := client.Beta.Organization.ServiceAccounts.Archive(
  	context.Background(),
  	"svac_01ABCDEFabcdef0123456789XY",
  	anthropic.BetaOrganizationServiceAccountArchiveParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", serviceAccount.ID)
  fmt.Printf("archived_at: %s\n", serviceAccount.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var serviceAccount = client.beta().organization().serviceAccounts()
      .archive("svac_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + serviceAccount.id());
  IO.println("archived_at: " + serviceAccount.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $serviceAccount = $client->beta->organization->serviceAccounts->archive(
      serviceAccountID: 'svac_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$serviceAccount->id}\n";
  echo "archived_at: {$serviceAccount->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  service_account_id = "svac_01ABCDEFabcdef0123456789XY"
  service_account = client.beta.organization.service_accounts.archive(service_account_id)

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

Untuk membaca atau memperbarui satu akun layanan, gunakan `GET` dan `POST` pada `/v1/organizations/service_accounts/{service_account_id}`. Akun layanan harus menjadi anggota sebuah workspace sebelum token terfederasi dapat bertindak di dalamnya. Setiap akun layanan memiliki keanggotaan implisit di workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain dengan `GET`, `POST`, dan `DELETE` pada `/v1/organizations/service_accounts/{service_account_id}/workspaces`, di mana `DELETE` menargetkan `.../workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Akun layanan](https://platform.claude.com/docs/id/api/admin/service_accounts).

## Issuer federasi

[Issuer federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#federation-issuers) (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Field `jwks` adalah discriminated union yang mengontrol cara Anthropic mengambil kunci penandatanganan penyedia:

| Nilai `jwks`                             | Kapan digunakan                                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| `{"type": "discovery"}`                  | Penyedia menyajikan `/.well-known/openid-configuration` di URL issuer.           |
| `{"type": "explicit_url", "url": "..."}` | Arahkan langsung ke endpoint JWKS.                                               |
| `{"type": "inline", "keys": [...]}`      | Unggah set kunci untuk penyedia yang tidak dapat dijangkau dari internet publik. |

Daftarkan issuer. Contoh ini mendaftarkan GitHub Actions dengan JWKS discovery:

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
  ant beta:organization:federation:issuers create \
    --name github-actions \
    --issuer-url https://token.actions.githubusercontent.com \
    --jwks '{type: discovery}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuer = client.beta.organization.federation.issuers.create(
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

  const issuer = await client.beta.organization.federation.issuers.create({
    name: "github-actions",
    issuer_url: "https://token.actions.githubusercontent.com",
    jwks: { type: "discovery" }
  });

  console.log(`id: ${issuer.id}`);
  console.log(`name: ${issuer.name}`);
  console.log(`issuer_url: ${issuer.issuer_url}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Federation.Issuers;

  AnthropicClient client = new();

  var issuer = await client.Beta.Organization.Federation.Issuers.Create(new()
  {
      Name = "github-actions",
      IssuerUrl = "https://token.actions.githubusercontent.com",
      Jwks = new BetaJwksDiscovery()
  });

  Console.WriteLine($"id: {issuer.ID}");
  Console.WriteLine($"name: {issuer.Name}");
  Console.WriteLine($"issuer_url: {issuer.IssuerUrl}");
  ```

  ```go Go
  client := anthropic.NewClient()

  issuer, err := client.Beta.Organization.Federation.Issuers.New(context.Background(), anthropic.BetaOrganizationFederationIssuerNewParams{
  	Name:      "github-actions",
  	IssuerURL: "https://token.actions.githubusercontent.com",
  	JWKS: anthropic.BetaOrganizationFederationIssuerNewParamsJWKSUnion{
  		OfDiscovery: &anthropic.BetaJWKSDiscoveryParam{},
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
  import com.anthropic.models.beta.organization.federation.issuers.BetaJwksDiscovery;
  import com.anthropic.models.beta.organization.federation.issuers.IssuerCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IssuerCreateParams.builder()
          .name("github-actions")
          .issuerUrl("https://token.actions.githubusercontent.com")
          .jwks(BetaJwksDiscovery.builder().build())
          .build();
      var issuer = client.beta().organization().federation().issuers().create(params);

      IO.println("id: " + issuer.id());
      IO.println("name: " + issuer.name());
      IO.println("issuer_url: " + issuer.issuerUrl());
  }
  ```

  ```php PHP
  $client = new Client();

  $issuer = $client->beta->organization->federation->issuers->create(
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

  issuer = client.beta.organization.federation.issuers.create(
    name: "github-actions",
    issuer_url: "https://token.actions.githubusercontent.com",
    jwks: {type: :discovery}
  )

  puts "id: #{issuer.id}"
  puts "name: #{issuer.name}"
  puts "issuer_url: #{issuer.issuer_url}"
  ```
</CodeGroup>

Daftarkan issuer yang ada:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers?limit=20" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:federation:issuers list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuers = client.beta.organization.federation.issuers.list(limit=20)

  for issuer in issuers:
      print(f"{issuer.id}: {issuer.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const issuer of client.beta.organization.federation.issuers.list({ limit: 20 })) {
    console.log(`${issuer.id}: ${issuer.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Federation.Issuers.List(new() { Limit = 20 });

  await foreach (var issuer in page.Paginate())
  {
      Console.WriteLine($"{issuer.ID}: {issuer.Name}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  issuers := client.Beta.Organization.Federation.Issuers.ListAutoPaging(context.Background(), anthropic.BetaOrganizationFederationIssuerListParams{
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
  import com.anthropic.models.beta.organization.federation.issuers.IssuerListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IssuerListParams.builder()
          .limit(20)
          .build();
      var issuers = client.beta().organization().federation().issuers().list(params);

      for (var issuer : issuers.autoPager()) {
          IO.println(issuer.id() + ": " + issuer.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $issuers = $client->beta->organization->federation->issuers->list(limit: 20);

  foreach ($issuers->getItems() as $issuer) {
      echo "{$issuer->id}: {$issuer->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  issuers = client.beta.organization.federation.issuers.list(limit: 20)

  issuers.data.each do |issuer|
    puts "#{issuer.id}: #{issuer.name}"
  end
  ```
</CodeGroup>

Arsipkan issuer:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -X POST "https://api.anthropic.com/v1/organizations/federation_issuers/fdis_01ABCDEFabcdef0123456789XY/archive" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:federation:issuers archive \
    --federation-issuer-id fdis_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  issuer = client.beta.organization.federation.issuers.archive(
      "fdis_01ABCDEFabcdef0123456789XY"
  )

  print(f"id: {issuer.id}")
  print(f"archived_at: {issuer.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const issuer = await client.beta.organization.federation.issuers.archive(
    "fdis_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${issuer.id}`);
  console.log(`archived_at: ${issuer.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var issuer = await client.Beta.Organization.Federation.Issuers.Archive(
      "fdis_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {issuer.ID}");
  Console.WriteLine($"archived_at: {issuer.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  issuer, err := client.Beta.Organization.Federation.Issuers.Archive(
  	context.Background(),
  	"fdis_01ABCDEFabcdef0123456789XY",
  	anthropic.BetaOrganizationFederationIssuerArchiveParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", issuer.ID)
  fmt.Printf("archived_at: %s\n", issuer.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var issuer = client.beta().organization().federation().issuers()
      .archive("fdis_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + issuer.id());
  IO.println("archived_at: " + issuer.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $issuer = $client->beta->organization->federation->issuers->archive(
      federationIssuerID: 'fdis_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$issuer->id}\n";
  echo "archived_at: {$issuer->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  issuer_id = "fdis_01ABCDEFabcdef0123456789XY"
  issuer = client.beta.organization.federation.issuers.archive(issuer_id)

  puts "id: #{issuer.id}"
  puts "archived_at: #{issuer.archived_at}"
  ```
</CodeGroup>

Untuk membaca atau memperbarui satu issuer, gunakan `GET` dan `POST` pada `/v1/organizations/federation_issuers/{issuer_id}`. Pemanggil OAuth tidak dapat memperbarui issuer yang mendukung aturan yang `oauth_scope`-nya selain `workspace:developer` atau `workspace:inference`; lihat [Izin dan batasan](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#permissions-and-constraints).

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Issuer federasi](https://platform.claude.com/docs/id/api/admin/federation_issuers).

## Aturan federasi

[Aturan federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#federation-rules) (`fdrl_...`) mengikat issuer ke akun layanan: JWT dari issuer yang memenuhi kondisi pencocokan aturan dapat mencetak token yang bertindak sebagai target aturan tersebut. `workspace_id` dalam permintaan create mengaktifkan aturan di workspace tersebut saat pembuatan; tambahkan lebih banyak workspace nanti melalui sub-resource `/federation_rules/{rule_id}/workspaces`. Salah satu dari `workspace_id` atau `applies_to_all_workspaces: true` wajib ada saat create.

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
  ant beta:organization:federation:rules create <<'YAML'
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

  rule = client.beta.organization.federation.rules.create(
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

  const rule = await client.beta.organization.federation.rules.create({
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

  var rule = await client.Beta.Organization.Federation.Rules.Create(new()
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

  rule, err := client.Beta.Organization.Federation.Rules.New(context.Background(), anthropic.BetaOrganizationFederationRuleNewParams{
  	Name:     "gha-deploy",
  	IssuerID: "fdis_01ABCDEFabcdef0123456789XY",
  	Match: anthropic.BetaFederationRuleMatchParam{
  		SubjectPrefix: anthropic.String("repo:my-org/my-repo:ref:refs/heads/main"),
  		Claims:        map[string]string{"repository_owner": "my-org"},
  	},
  	Target: anthropic.BetaServiceAccountTargetParam{
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
  import com.anthropic.models.beta.organization.federation.rules.BetaFederationRuleMatch;
  import com.anthropic.models.beta.organization.federation.rules.BetaServiceAccountTarget;
  import com.anthropic.models.beta.organization.federation.rules.RuleCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var match = BetaFederationRuleMatch.builder()
          .subjectPrefix("repo:my-org/my-repo:ref:refs/heads/main")
          .claims(BetaFederationRuleMatch.Claims.builder()
              .putAdditionalProperty("repository_owner", JsonValue.from("my-org"))
              .build())
          .build();
      var params = RuleCreateParams.builder()
          .name("gha-deploy")
          .issuerId("fdis_01ABCDEFabcdef0123456789XY")
          .match(match)
          .target(BetaServiceAccountTarget.of("svac_01ABCDEFabcdef0123456789XY"))
          .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .oauthScope("workspace:developer")
          .tokenLifetimeSeconds(600)
          .build();
      var rule = client.beta().organization().federation().rules().create(params);

      IO.println("id: " + rule.id());
      IO.println("name: " + rule.name());
  }
  ```

  ```php PHP
  $client = new Client();

  $rule = $client->beta->organization->federation->rules->create(
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

  rule = client.beta.organization.federation.rules.create(
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

Daftarkan aturan, dengan filter opsional berdasarkan issuer:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules?issuer_id=fdis_01ABCDEFabcdef0123456789XY" \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:federation:rules list \
    --issuer-id fdis_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  rules = client.beta.organization.federation.rules.list(
      issuer_id="fdis_01ABCDEFabcdef0123456789XY"
  )

  for rule in rules:
      print(f"{rule.id}: {rule.name}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  for await (const rule of client.beta.organization.federation.rules.list({
    issuer_id: "fdis_01ABCDEFabcdef0123456789XY"
  })) {
    console.log(`${rule.id}: ${rule.name}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Federation.Rules.List(new()
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

  rules := client.Beta.Organization.Federation.Rules.ListAutoPaging(context.Background(), anthropic.BetaOrganizationFederationRuleListParams{
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
  import com.anthropic.models.beta.organization.federation.rules.RuleListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RuleListParams.builder()
          .issuerId("fdis_01ABCDEFabcdef0123456789XY")
          .build();
      var rules = client.beta().organization().federation().rules().list(params);

      for (var rule : rules.autoPager()) {
          IO.println(rule.id() + ": " + rule.name());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rules = $client->beta->organization->federation->rules->list(
      issuerID: 'fdis_01ABCDEFabcdef0123456789XY',
  );

  foreach ($rules->getItems() as $rule) {
      echo "{$rule->id}: {$rule->name}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rules = client.beta.organization.federation.rules.list(
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
  ant beta:organization:federation:rules archive \
    --federation-rule-id fdrl_01ABCDEFabcdef0123456789XY
  ```

  ```python Python
  client = anthropic.Anthropic()

  rule = client.beta.organization.federation.rules.archive(
      "fdrl_01ABCDEFabcdef0123456789XY"
  )

  print(f"id: {rule.id}")
  print(f"archived_at: {rule.archived_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rule = await client.beta.organization.federation.rules.archive(
    "fdrl_01ABCDEFabcdef0123456789XY"
  );

  console.log(`id: ${rule.id}`);
  console.log(`archived_at: ${rule.archived_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rule = await client.Beta.Organization.Federation.Rules.Archive(
      "fdrl_01ABCDEFabcdef0123456789XY"
  );

  Console.WriteLine($"id: {rule.ID}");
  Console.WriteLine($"archived_at: {rule.ArchivedAt:O}");
  ```

  ```go Go
  client := anthropic.NewClient()

  rule, err := client.Beta.Organization.Federation.Rules.Archive(
  	context.Background(),
  	"fdrl_01ABCDEFabcdef0123456789XY",
  	anthropic.BetaOrganizationFederationRuleArchiveParams{},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", rule.ID)
  fmt.Printf("archived_at: %s\n", rule.ArchivedAt)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rule = client.beta().organization().federation().rules()
      .archive("fdrl_01ABCDEFabcdef0123456789XY");

  IO.println("id: " + rule.id());
  IO.println("archived_at: " + rule.archivedAt().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $rule = $client->beta->organization->federation->rules->archive(
      federationRuleID: 'fdrl_01ABCDEFabcdef0123456789XY',
  );

  echo "id: {$rule->id}\n";
  echo "archived_at: {$rule->archivedAt?->format(DATE_ATOM)}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rule_id = "fdrl_01ABCDEFabcdef0123456789XY"
  rule = client.beta.organization.federation.rules.archive(rule_id)

  puts "id: #{rule.id}"
  puts "archived_at: #{rule.archived_at}"
  ```
</CodeGroup>

Endpoint list mengembalikan satu halaman aturan dan kursor untuk halaman berikutnya:

```json
{
  "data": [{ "id": "fdrl_...", "name": "gha-deploy", "...": "..." }],
  "next_page": "..."
}
```

Untuk membaca atau memperbarui satu aturan, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}`. Untuk mengelola workspace tempat aturan dapat mencetak token, gunakan `GET` dan `POST` pada `/v1/organizations/federation_rules/{rule_id}/workspaces`, dan `DELETE` pada `/v1/organizations/federation_rules/{rule_id}/workspaces/{workspace_id}`.

Untuk detail parameter lengkap dan skema respons, lihat [referensi API Aturan federasi](https://platform.claude.com/docs/id/api/admin/federation_rules).

## Izin dan batasan

<Note>
  * Pemanggil yang diautentikasi dengan OAuth hanya dapat membuat atau memodifikasi aturan yang `oauth_scope`-nya adalah `workspace:developer` atau `workspace:inference`. Untuk membuat atau memodifikasi aturan dengan scope lain (seperti `org:admin` atau `workspace:manage_tunnels`), gunakan Console.
  * Pemanggil OAuth tidak dapat memperbarui issuer federasi yang mendukung aturan yang `oauth_scope`-nya selain `workspace:developer` atau `workspace:inference` (seperti `org:admin` atau `workspace:manage_tunnels`). Pertimbangkan untuk mendaftarkan issuer khusus untuk aturan bootstrap sehingga issuer di balik aturan dengan scope workspace tetap dapat diperbarui melalui API.
  * Kunci Admin API tidak diterima di endpoint ini, baik untuk baca maupun tulis; gunakan token OAuth `org:admin`.
</Note>

Aturan dengan `oauth_scope: org:admin` harus menargetkan akun layanan yang `organization_role`-nya adalah `admin`. Nama sumber daya harus cocok dengan `^[a-z0-9-]+$`, terdiri dari 1 hingga 255 karakter, dan unik dalam satu organisasi untuk setiap jenis sumber daya; untuk batasan lengkap tingkat field, lihat [Aturan validasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#validation-rules).

## Paginasi dan pengarsipan

Endpoint list akun layanan, issuer federasi, dan aturan federasi menerima `limit` (1 hingga 100, default 20) dan kursor `page` yang diambil dari respons sebelumnya. Teruskan nilai `next_page` dari respons sebagai parameter query `page` pada permintaan berikutnya. List sub-resource rule-workspaces mengembalikan set lengkap tanpa paginasi. Sumber daya yang diarsipkan disembunyikan dari daftar secara default; teruskan `include_archived=true` untuk menyertakannya.

Pengarsipan adalah soft delete dan bersifat idempoten: mengarsipkan sumber daya yang sudah diarsipkan akan berhasil. Mengarsipkan issuer atau akun layanan mengembalikan `400` selama aturan federasi aktif masih mereferensikannya; arsipkan aturannya terlebih dahulu.

## Lihat juga

* [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation): konsep dan panduan penyiapan di Console
* [Referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference): variabel lingkungan, aturan validasi, OAuth scope, dan kode error
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api): bagian lain dari permukaan manajemen organisasi
* [Referensi Admin API](https://platform.claude.com/docs/id/api/admin): skema permintaan dan respons yang dihasilkan untuk setiap endpoint Admin API
