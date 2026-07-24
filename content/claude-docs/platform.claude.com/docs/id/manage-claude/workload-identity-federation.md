---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workload-identity-federation
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 50a033aa52e426500919df194220c0d7e477b7ff85caa0aefcd3e9907b2d0e1e
---

# Workload Identity Federation

Autentikasi workload ke Claude API dengan token identitas berumur pendek dari penyedia identitas Anda sendiri alih-alih kunci API statis berumur panjang.

---

"Workload Identity Federation" (federasi identitas workload), atau WIF, memungkinkan workload Anda melakukan autentikasi ke Claude API dengan token OpenID Connect (OIDC) berumur pendek alih-alih kunci API `sk-ant-...` berumur panjang. Token tersebut berasal dari "identity provider" (penyedia identitas), atau IdP, yang sudah Anda operasikan: AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar seperti GitHub Actions, Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta.

Workload Anda menyajikan JWT yang ditandatangani dari penyedia identitas Anda. Anthropic memvalidasinya terhadap aturan kepercayaan yang Anda konfigurasikan di Claude Console dan mengembalikan token akses Anthropic berumur pendek yang terikat pada akun layanan di organisasi Anda. Tidak ada rahasia statis yang perlu dibuat, disimpan di CI, dirotasi, atau bocor.

Workload Identity Federation memperkuat postur keamanan Anda dengan mengganti kunci API statis dengan token yang kedaluwarsa dalam hitungan menit, bukan tidak pernah kedaluwarsa. Ini bukan solusi keamanan yang lengkap dengan sendirinya: autentikasi terfederasi hanya sekuat penyedia identitas hulu yang menandatangani JWT. Padukan Workload Identity Federation dengan kontrol yang sudah didukung IdP Anda (pengikatan identitas workload, akses bersyarat, pencatatan audit) untuk pertahanan berlapis.

## Konsep

Anda mengonfigurasi tiga sumber daya di Claude Console sebelum workload apa pun dapat melakukan federasi. Bersama-sama, ketiganya menyatakan "token yang ditandatangani oleh penerbit X, dengan klaim yang terlihat seperti Y, dapat bertindak sebagai akun layanan Z."

### Akun layanan

**Akun layanan** (`svac_...`) adalah identitas non-manusia bernama di dalam organisasi Anthropic Anda. Ini adalah prinsipal yang diwakili oleh token terfederasi. Akun layanan berada di tingkat organisasi dan menjadi aktif di sebuah workspace ketika Anda menambahkannya sebagai anggota workspace tersebut. Pada saat pertukaran, Anthropic memeriksa bahwa workspace aturan federasi cocok dengan salah satu keanggotaan workspace akun layanan; token yang diterbitkan kemudian mengikuti batas laju dan atribusi penggunaan workspace tersebut, sama seperti kunci API. Tidak seperti pengguna manusia, akun layanan tidak memiliki email, kata sandi, dan login Console. Setiap akun layanan secara implisit adalah anggota workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain tempat akun tersebut harus bertindak.

Perbedaan utama dari kunci API: kunci API *adalah* kredensial, sedangkan akun layanan *memiliki* kredensial yang diterbitkan untuknya sesuai permintaan. Anda dapat mengaudit workload mana yang bertindak sebagai akun layanan mana.

### Penerbit federasi

**Penerbit federasi** (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Mendaftarkan penerbit memberi tahu Anthropic "JWT yang ditandatangani oleh penyedia ini dapat menyatakan identitas workload untuk organisasi saya."

Penerbit memiliki dua bagian konfigurasi:

* **URL penerbit:** Nilai klaim `iss` persis yang muncul di JWT penyedia, misalnya `https://token.actions.githubusercontent.com` atau `https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLE`.
* **Sumber JWKS:** Cara Anthropic mengambil kunci publik untuk memverifikasi tanda tangan JWT. Gunakan `discovery` (default) untuk penyedia apa pun yang menyajikan `/.well-known/openid-configuration` di URL penerbitnya. Gunakan `explicit_url` untuk menunjuk langsung ke endpoint JWKS, atau `inline` untuk mengunggah kumpulan kunci bagi penerbit yang tidak dapat dijangkau dari internet publik (misalnya, klaster Kubernetes privat).

URL penerbit dan JWKS harus `https`, pada port 443, dan menggunakan nama host DNS publik yang diselesaikan ke alamat IP publik; literal IP tidak diterima. Batasan ini hanya berlaku untuk URL yang diambil oleh Anthropic; dalam mode `explicit_url` dan `inline`, `issuer_url` dibandingkan sebagai string dan dapat merujuk ke nama host internal.

Anda biasanya mendaftarkan satu penerbit per lingkungan: klaster EKS produksi Anda, klaster staging Anda, dan GitHub Actions adalah tiga penerbit terpisah.

### Aturan federasi

**Aturan federasi** (`fdrl_...`) adalah jembatan antara penerbit dan akun layanan: "ketika JWT dari penerbit X memiliki klaim yang terlihat seperti Y, terbitkan token untuk akun layanan Z dengan cakupan S."

Aturan mendefinisikan kondisi pencocokan, target, serta cakupan otorisasi dan masa berlaku token yang berlaku ketika aturan cocok:

* **Pencocokan:** Kondisi yang harus dipenuhi oleh JWT yang masuk. Anda dapat mencocokkan berdasarkan `subject_prefix` (misalnya, `system:serviceaccount:prod:worker`, atau dengan `*` di akhir untuk pencocokan awalan), `audience` yang persis, peta nilai klaim yang persis, ekspresi `condition` [CEL](https://cel.dev/) untuk logika kompleks, atau kombinasi apa pun. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur, dan semua pencocok yang dikonfigurasi harus lolos agar JWT diterima.
* **Target:** Akun layanan yang dipetakan oleh JWT yang cocok.
* **Otorisasi:** `scope` OAuth yang diberikan pada token yang diterbitkan. Default-nya adalah `workspace:developer`, yang memberikan akses yang sama dengan kunci API yang diterbitkan untuk workspace tersebut. Beberapa produk mengunci cakupan ketika Anda membuat aturan dari alurnya; misalnya, modal create-tunnel pada [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) membuat aturan dengan cakupan `workspace:manage_tunnels`. Lihat [Cakupan OAuth](/docs/id/manage-claude/wif-reference#oauth-scopes). Aturan juga mengatur `token_lifetime_seconds` (60 hingga 86400, default 3600).

Satu penerbit dapat memiliki banyak aturan: satu per tim, namespace, atau tingkat izin. Aturan dievaluasi berdasarkan ID: klien menentukan aturan mana yang akan digunakan dalam permintaan pertukaran, dan Anthropic memverifikasi bahwa JWT memenuhi kriteria pencocokan aturan tersebut. Tidak ada pencarian aturan implisit.

## Cara kerjanya

1. **IdP Anda menerbitkan JWT ke workload.** Pada sebagian besar platform, ini bersifat ambien: token akun layanan terproyeksi Kubernetes, server metadata Google Cloud, Azure IMDS, atau endpoint OIDC GitHub Actions. Klaim `iss` pada JWT mengidentifikasi penyedia, dan klaim `sub` serta klaim lainnya mengidentifikasi workload spesifik.
2. **SDK menukar JWT dengan token akses Anthropic.** SDK mengirimkan JWT ke `POST /v1/oauth/token` menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). Anthropic memverifikasi JWT terhadap JWKS penerbit dan kondisi pencocokan aturan federasi, lalu mengembalikan token `sk-ant-oat01-...` berumur pendek yang bertindak atas nama akun layanan target aturan tersebut.
3. **SDK mengirimkan token pada setiap permintaan dan menyegarkannya sebelum kedaluwarsa.** Kode aplikasi Anda membangun klien tanpa `api_key` dan memanggil API seperti biasa. SDK menjalankan ulang pertukaran sebelum token kedaluwarsa.

## Menyiapkan federasi

Anda memerlukan peran admin, owner, atau primary owner di organisasi Anthropic Anda, penyedia identitas berkemampuan OIDC dengan endpoint JWKS yang dapat dijangkau (atau dokumen JWKS yang dapat Anda tempel, untuk klaster yang terisolasi dari internet), dan workload yang dapat memperoleh token identitas dari penyedia tersebut.

Wizard **Connect workload** membuat ketiga sumber daya (penerbit, akun layanan, dan aturan federasi) dalam satu alur terpandu, lalu memverifikasi koneksi dari ujung ke ujung.

<Steps>
  <Step title="Buka Connect workload">
    Di Claude Console, buka **Settings → Workload identity** dan pilih **Connect workload**.
  </Step>

  <Step title="Pilih penyedia Anda">
    Pilih kotak untuk penyedia identitas Anda: GitHub Actions, AWS, Google Cloud, Microsoft Entra ID, atau Kubernetes. Setiap kotak mengisi otomatis pola URL penerbit dan bidang pencocokan yang didukung oleh JWT penyedia tersebut. Untuk penyedia lain yang sesuai standar (seperti SPIFFE atau Okta), pilih **Custom OIDC**.
  </Step>

  <Step title="Isi bidang terpandu">
    Wizard memandu Anda melalui bidang khusus penyedia: konfigurasi penerbit, kondisi pencocokan untuk JWT yang masuk, dan nama untuk akun layanan serta aturan federasi yang dibuatnya. Wizard mengisi otomatis `oauth_scope=workspace:developer` dan `token_lifetime_seconds=600` (default API ketika `token_lifetime_seconds` dihilangkan adalah 3600); sesuaikan nilai-nilai ini jika workload Anda memerlukan cakupan atau masa berlaku yang berbeda.
  </Step>

  <Step title="Verifikasi penerbit">
    Secara opsional, pilih **Verify issuer** untuk menguji coba konfigurasi penerbit sebelum apa pun dibuat. Verifikasi mengonfirmasi bahwa Anthropic dapat mengambil dan mengurai JWKS dari URL yang Anda masukkan, yang menangkap kesalahan keterjangkauan dan konfigurasi sejak dini.
  </Step>

  <Step title="Uji koneksi">
    Wizard membuat penerbit, akun layanan, dan aturan federasi, lalu mendengarkan pertukaran token yang berhasil selama 15 menit. Picu pertukaran dari workload Anda dalam jendela waktu tersebut (lihat [Autentikasi dari workload Anda](#authenticate-from-your-workload)) untuk mengonfirmasi bahwa penyiapan berfungsi. Jika jendela waktu berlalu, sumber daya tetap ada; Anda dapat menjalankan ulang pengujian dari halaman detail aturan federasi. Catat ID aturan (`fdrl_...`) dan ID akun layanan (`svac_...`) yang dibuat wizard: workload Anda meneruskan keduanya, bersama dengan ID organisasi Anda (dan ID workspace Anda ketika aturan mencakup lebih dari satu workspace), dalam setiap permintaan pertukaran token.
  </Step>
</Steps>

Untuk mengelola sumber daya ini secara terprogram, lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api) untuk panduan curl, atau lihat [Referensi API Service accounts](/docs/id/api/admin/service_accounts), [Referensi API Federation issuers](/docs/id/api/admin/federation_issuers), dan [Referensi API Federation rules](/docs/id/api/admin/federation_rules) untuk detail parameter lengkap dan skema respons.

## Autentikasi dari workload Anda

Dengan federasi yang telah dikonfigurasi, workload Anda menukar JWT yang diterbitkan IdP dengan token Anthropic saat runtime. SDK menangani pertukaran dan loop penyegaran untuk Anda. Tab cURL menunjukkan pertukaran HTTP yang mendasarinya untuk skrip shell, debugging, atau bahasa tanpa dukungan SDK.

### Membangun klien SDK

Anda dapat membangun klien dengan kredensial eksplisit atau tanpa argumen. Tanpa argumen, SDK menyelesaikan kredensial dari variabel lingkungan atau profil aktif, seperti yang dijelaskan di bawah [Prioritas kredensial](#credential-precedence). Bentuk tanpa argumen adalah pola yang direkomendasikan untuk workload produksi: kirimkan image container yang sama ke mana-mana dan injeksikan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, dan `ANTHROPIC_IDENTITY_TOKEN_FILE` per lingkungan.

<CodeGroup>
  ```bash cURL
  # 1. Dapatkan JWT dari IdP Anda (spesifik per platform; lihat panduan masing-masing penyedia).
  JWT=$(cat /var/run/secrets/anthropic.com/token)

  # 2. Tukarkan dengan token akses Anthropic berumur pendek.
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$JWT",
    "federation_rule_id": "fdrl_...",
    "organization_id": "00000000-0000-0000-0000-000000000000",
    "service_account_id": "svac_...",
    "workspace_id": "wrkspc_..."
  }
  JSON
  )

  ACCESS_TOKEN=$(jq -r .access_token <<<"$RESPONSE")
  EXPIRES_IN=$(jq -r .expires_in <<<"$RESPONSE")  # seconds; re-exchange before this elapses

  # 3. Panggil API dengan token akses tersebut di header Authorization: Bearer.
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<'JSON' | jq -r '.content[0].text'
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }
  JSON
  ```

  ```python Python
  from anthropic import Anthropic, WorkloadIdentityCredentials, IdentityTokenFile

  client = Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=IdentityTokenFile(
              "/var/run/secrets/anthropic.com/token"
          ),
          federation_rule_id="fdrl_...",
          organization_id="00000000-0000-0000-0000-000000000000",
          service_account_id="svac_...",
          workspace_id="wrkspc_...",
      ),
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { identityTokenFromFile } from "@anthropic-ai/sdk/lib/credentials/identity-token";

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: identityTokenFromFile("/var/run/secrets/anthropic.com/token"),
      federationRuleId: "fdrl_...",
      organizationId: "00000000-0000-0000-0000-000000000000",
      serviceAccountId: "svac_...",
      workspaceId: "wrkspc_...",
      baseURL: "https://api.anthropic.com",
      fetch
    })
  });

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(
  		option.IdentityTokenFile("/var/run/secrets/anthropic.com/token"),
  		option.FederationOptions{
  			FederationRuleID: "fdrl_...",
  			OrganizationID:   "00000000-0000-0000-0000-000000000000",
  			ServiceAccountID: "svac_...",
  			WorkspaceID:      "wrkspc_...",
  		},
  	),
  )

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.config.AuthenticationConfig;
  import com.anthropic.config.AuthenticationType;
  import com.anthropic.config.IdentityTokenConfig;
  import com.anthropic.config.InMemoryProfileConfigProvider;
  import com.anthropic.config.ProfileConfig;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
              .fromEnv()
              .configurationProvider(InMemoryProfileConfigProvider.of(ProfileConfig.builder()
                      .organizationId("00000000-0000-0000-0000-000000000000")
                      .workspaceId("wrkspc_...")
                      .authentication(AuthenticationConfig.builder()
                              .type(AuthenticationType.OIDC_FEDERATION)
                              .federationRuleId("fdrl_...")
                              .serviceAccountId("svac_...")
                              .identityToken(IdentityTokenConfig.builder()
                                      .source("file")
                                      .path("/var/run/secrets/anthropic.com/token")
                                      .build())
                              .build())
                      .build()))
              .build();

      var message = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build());

      IO.println(message.content());
  }
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Oidc;

  var credentials = new WorkloadIdentityCredentials(new WorkloadIdentityOptions
  {
      FederationRuleId = "fdrl_...",
      OrganizationId = "00000000-0000-0000-0000-000000000000",
      ServiceAccountId = "svac_...",
      WorkspaceId = "wrkspc_...",
      IdentityTokenProvider = new FileIdentityTokenProvider("/var/run/secrets/anthropic.com/token"),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Lib\Credentials\CredentialResult;
  use Anthropic\Lib\Credentials\IdentityTokenFile;
  use Anthropic\Lib\Credentials\TokenCache;
  use Anthropic\Lib\Credentials\WorkloadIdentityCredentials;

  $client = new Client(credentials: new CredentialResult(
      provider: new TokenCache(
          new WorkloadIdentityCredentials(
              identityProvider: new IdentityTokenFile('/var/run/secrets/anthropic.com/token'),
              federationRuleId: 'fdrl_...',
              organizationId: '00000000-0000-0000-0000-000000000000',
              serviceAccountId: 'svac_...',
              workspaceId: 'wrkspc_...',
          ),
      ),
  ));

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );

  echo $message->content[0]->text . PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new(
    credentials: Anthropic::Credentials::WorkloadIdentity.new(
      identity_token_provider: Anthropic::Credentials::IdentityTokenFile.new(
        "/var/run/secrets/anthropic.com/token"
      ),
      federation_rule_id: "fdrl_...",
      organization_id: "00000000-0000-0000-0000-000000000000",
      service_account_id: "svac_...",
      workspace_id: "wrkspc_..."
    )
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

Respons pertukaran token mengikuti [RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1). Lihat [Respons pertukaran token](/docs/id/manage-claude/wif-reference#token-exchange-response) untuk referensi bidangnya.

## Prioritas kredensial

Setiap SDK menyelesaikan kredensial dalam urutan lima tingkat yang sama: argumen konstruktor, lalu `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`, lalu `ANTHROPIC_PROFILE` eksplisit, lalu variabel lingkungan federasi, lalu profil aktif implisit. Sumber pertama yang menghasilkan kredensial yang menang.

<Warning>
  `ANTHROPIC_API_KEY` berada di atas tingkat federasi, sehingga kunci yang tersisa di lingkungan secara diam-diam menutupi federasi. Saat memigrasikan workload dari kunci API ke Workload Identity Federation, pastikan `ANTHROPIC_API_KEY` tidak diatur di mana pun workload tersebut berjalan (env container, rahasia CI, profil shell). Perintah CLI [`ant auth status`](/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) melaporkan sumber mana yang menang.
</Warning>

Untuk tabel prioritas lengkap, semantik per tingkat, dan skema file profil, lihat [Prioritas kredensial di referensi WIF](/docs/id/manage-claude/wif-reference#credential-precedence).

## Migrasi dari kunci API

Untuk mengalihkan workload yang ada dari kunci API statis ke federasi tanpa downtime:

1. **Konfigurasikan federasi secara paralel.** Selesaikan [panduan penyiapan](#set-up-federation) dan konfirmasikan bahwa aturan federasi cocok dengan token workload Anda. Biarkan `ANTHROPIC_API_KEY` yang ada tetap di tempatnya untuk saat ini.
2. **Uji coba kredensial mana yang menang.** Jalankan `ant auth status` dari dalam workload (atau periksa log debug SDK). Karena `ANTHROPIC_API_KEY` berada di atas tingkat federasi dalam rantai prioritas, kunci API masih menang pada tahap ini.
3. **Hapus pengaturan `ANTHROPIC_API_KEY` di mana pun ia diinjeksikan.** Hapus dari rahasia CI, lingkungan container, dan profil shell (lihat peringatan sebelumnya). Jalankan ulang `ant auth status` dan konfirmasikan bahwa sumber federasi sekarang dipilih.
4. **Cabut kunci API.** Setelah workload berjalan dengan token terfederasi, hapus kunci di Claude Console di bawah **Settings → API keys**.

## Masa berlaku dan penyegaran token

Masa berlaku token Anthropic yang diterbitkan adalah yang lebih kecil antara (a) `token_lifetime_seconds` aturan (default 3.600 detik) dan (b) dua kali sisa masa berlaku JWT IdP yang Anda sajikan. Hasilnya tidak pernah kurang dari 60 detik. Batas kedua mencegah token Anthropic hidup lebih lama dari identitas hulu asalnya dengan selisih yang lebih dari sedikit.

SDK menyimpan token dalam cache dan menyegarkannya dengan jadwal dua tingkat yang dimodelkan berdasarkan `botocore`:

* **Penyegaran advisory** pada waktu kedaluwarsa dikurangi 120 detik. SDK mencoba pertukaran baru. Jika endpoint token tidak dapat dijangkau, SDK terus menyajikan token yang di-cache, yang masih valid selama kira-kira 90 detik lagi.
* **Penyegaran wajib** pada waktu kedaluwarsa dikurangi 30 detik. Pertukaran yang gagal pada titik ini memunculkan kesalahan. Token yang di-cache terlalu dekat dengan waktu kedaluwarsa untuk dianggap aman.

Karena SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pertukaran, SDK secara transparan mengambil token terproyeksi yang dirotasi (token akun layanan Kubernetes, misalnya, dirotasi jauh sebelum `exp`-nya).

## Penyedia identitas

Setiap panduan membahas dari mana JWT berasal di platform tersebut, seperti apa klaimnya, dan konfigurasi penerbit serta aturan yang perlu didaftarkan.

<CardGroup cols={3}>
  <Card title="AWS" icon="cloud" href="/docs/id/manage-claude/wif-providers/aws">
    Token web identity STS, atau token terproyeksi EKS IRSA.
  </Card>

  <Card title="Google Cloud" icon="cloud" href="/docs/id/manage-claude/wif-providers/gcp">
    Token identitas yang ditandatangani Google dari server metadata.
  </Card>

  <Card title="Microsoft Entra ID" icon="cloud" href="/docs/id/manage-claude/wif-providers/azure">
    Managed Identity (IMDS) dan Entra Workload ID di AKS.
  </Card>

  <Card title="GitHub Actions" icon="github-logo" href="/docs/id/manage-claude/wif-providers/github-actions">
    Autentikasi CI tanpa kunci dengan token OIDC Actions.
  </Card>

  <Card title="Kubernetes" icon="cube" href="/docs/id/manage-claude/wif-providers/kubernetes">
    Klaster yang dikelola sendiri dan on-premises menggunakan token akun layanan terproyeksi.
  </Card>

  <Card title="SPIFFE" icon="fingerprint" href="/docs/id/manage-claude/wif-providers/spiffe">
    Workload dengan SPIFFE JWT-SVID dari SPIRE atau penerbit lain yang sesuai.
  </Card>

  <Card title="Okta" icon="lock" href="/docs/id/manage-claude/wif-providers/okta">
    Aplikasi layanan Okta menggunakan alur client-credentials.
  </Card>
</CardGroup>

## Lihat juga

* [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api): membuat penerbit, akun layanan, dan aturan dari infrastructure as code
* [Referensi WIF](/docs/id/manage-claude/wif-reference): variabel lingkungan, skema file profil, aturan validasi, dan kode kesalahan
* [Autentikasi](/docs/id/manage-claude/authentication): semua opsi autentikasi di seluruh SDK Anthropic
* [Referensi Admin API](/docs/id/api/admin): skema permintaan dan respons yang dihasilkan untuk setiap endpoint Admin API
