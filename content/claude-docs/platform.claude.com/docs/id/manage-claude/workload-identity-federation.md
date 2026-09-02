---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workload-identity-federation
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: f72b0a81232a543ac29026bd20a278875a59d3c0326e6c4bdeeaf0d5c2afb705
---

---
title: Workload Identity Federation
url: https://platform.claude.com/docs/id/manage-claude/workload-identity-federation
description: Autentikasi workload ke Claude API dengan token identitas berumur pendek dari penyedia identitas Anda sendiri, alih-alih kunci API statis berumur panjang.
---

Workload Identity Federation (WIF) memungkinkan workload Anda melakukan autentikasi ke Claude API dengan token OpenID Connect (OIDC) berumur pendek alih-alih kunci API `sk-ant-...` berumur panjang. Token tersebut berasal dari "identity provider" (penyedia identitas), atau IdP, yang sudah Anda operasikan: AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar seperti GitHub Actions, Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta.

Workload Anda menyajikan JWT bertanda tangan dari penyedia identitas Anda. Anthropic memvalidasinya terhadap aturan kepercayaan yang Anda konfigurasikan di Claude Console dan mengembalikan token akses Anthropic berumur pendek yang terikat pada sebuah service account di organisasi Anda. Tidak ada rahasia statis yang perlu dibuat, disimpan di CI, dirotasi, atau berisiko bocor.

Workload Identity Federation memperkuat postur keamanan Anda dengan mengganti kunci API statis dengan token yang kedaluwarsa dalam hitungan menit, bukan tidak pernah kedaluwarsa. Ini bukan solusi keamanan yang lengkap dengan sendirinya: autentikasi terfederasi hanya sekuat penyedia identitas hulu yang menandatangani JWT. Padukan Workload Identity Federation dengan kontrol yang sudah didukung IdP Anda (pengikatan identitas workload, akses bersyarat, pencatatan audit) untuk pertahanan berlapis.

## Konsep

Anda mengonfigurasi tiga sumber daya di Claude Console sebelum workload apa pun dapat melakukan federasi. Bersama-sama, ketiganya menyatakan "token yang ditandatangani oleh penerbit X, dengan klaim yang terlihat seperti Y, boleh bertindak sebagai service account Z."

### Service account

**Service account** (akun layanan) (`svac_...`) adalah identitas non-manusia bernama di dalam organisasi Anthropic Anda. Ini adalah principal yang diwakili oleh [kunci service account](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) atau token terfederasi saat bertindak. Service account berada di tingkat organisasi dan menjadi aktif di sebuah workspace ketika Anda menambahkannya sebagai anggota workspace tersebut. Pada saat pertukaran, Anthropic memeriksa bahwa workspace pada aturan federasi cocok dengan salah satu keanggotaan workspace milik service account; token yang dicetak kemudian mengikuti batas laju dan atribusi penggunaan workspace tersebut, sama seperti kunci API. Tidak seperti pengguna manusia, service account tidak memiliki email, kata sandi, maupun login Console. Setiap service account secara implisit merupakan anggota workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain tempat service account tersebut perlu bertindak. Agar kunci service account yang berlaku untuk semua workspace dapat bertindak di sebuah workspace, tambahkan service account tersebut ke workspace itu.

Perbedaan utama dibandingkan kunci API workspace: kunci API workspace *adalah* sebuah kredensial, sedangkan service account *memiliki* kredensial. Anda dapat lebih mudah mengaudit workload mana yang bertindak sebagai service account mana.

### Federation issuer

**Federation issuer** (penerbit federasi) (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Mendaftarkan issuer memberi tahu Anthropic bahwa "JWT yang ditandatangani oleh penyedia ini boleh menyatakan identitas workload untuk organisasi saya."

Sebuah issuer memiliki dua bagian konfigurasi:

* **Issuer URL:** Nilai klaim `iss` persis yang muncul di JWT penyedia, misalnya `https://token.actions.githubusercontent.com` atau `https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLE`.
* **Sumber JWKS:** Cara Anthropic mengambil kunci publik untuk memverifikasi tanda tangan JWT. Gunakan `discovery` (default) untuk penyedia apa pun yang menyajikan `/.well-known/openid-configuration` di issuer URL-nya. Gunakan `explicit_url` untuk menunjuk langsung ke endpoint JWKS, atau `inline` untuk mengunggah set kunci bagi issuer yang tidak dapat dijangkau dari internet publik (misalnya, klaster Kubernetes privat).

Issuer URL dan JWKS URL harus menggunakan `https`, pada port 443, dan menggunakan hostname DNS publik yang me-resolve ke alamat IP publik; literal IP tidak diterima. Batasan ini hanya berlaku untuk URL yang diambil oleh Anthropic; dalam mode `explicit_url` dan `inline`, `issuer_url` dibandingkan sebagai string dan boleh merujuk ke hostname internal.

Biasanya Anda mendaftarkan satu issuer per lingkungan: klaster EKS produksi Anda, klaster staging Anda, dan GitHub Actions adalah tiga issuer terpisah.

### Federation rule

**Federation rule** (aturan federasi) (`fdrl_...`) adalah jembatan antara issuer dan service account: "ketika JWT dari issuer X memiliki klaim yang terlihat seperti Y, cetak token untuk service account Z dengan scope S."

Sebuah aturan mendefinisikan kondisi pencocokan, target, serta scope otorisasi dan masa berlaku token yang diterapkan ketika aturan cocok:

* **Match:** Kondisi yang harus dipenuhi oleh JWT yang masuk. Anda dapat mencocokkan berdasarkan `subject_prefix` (misalnya, `system:serviceaccount:prod:worker`, atau dengan `*` di akhir untuk pencocokan prefiks), `audience` yang persis, peta nilai klaim yang persis, ekspresi `condition` [CEL](https://cel.dev/) untuk logika kompleks, atau kombinasi apa pun. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur, dan semua matcher yang dikonfigurasi harus lolos agar JWT diterima.
* **Target:** Service account yang menjadi tujuan pemetaan JWT yang cocok.
* **Authorization:** `scope` OAuth yang diberikan pada token yang dicetak. Default-nya adalah `workspace:developer`, yang memberikan akses yang sama dengan kunci API workspace. Beberapa produk mengunci scope ketika Anda membuat aturan dari alurnya; misalnya, modal create-tunnel pada [MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) membuat aturan dengan scope `workspace:manage_tunnels`. Lihat [OAuth scopes](https://platform.claude.com/docs/id/manage-claude/wif-reference#oauth-scopes). Aturan juga menetapkan `token_lifetime_seconds` (60 hingga 86400, default 3600).

Satu issuer dapat memiliki banyak aturan: satu per tim, namespace, atau tingkat izin. Aturan dievaluasi berdasarkan ID: klien menentukan aturan mana yang digunakan dalam permintaan pertukaran, dan Anthropic memverifikasi bahwa JWT memenuhi kriteria pencocokan aturan tersebut. Tidak ada pencarian aturan secara implisit.

## Cara kerjanya

1. **IdP Anda menerbitkan JWT ke workload.** Di sebagian besar platform, ini bersifat ambient: token service-account terproyeksi Kubernetes, server metadata Google Cloud, Azure IMDS, atau endpoint OIDC GitHub Actions. Klaim `iss` pada JWT mengidentifikasi penyedia, dan klaim `sub` serta klaim lainnya mengidentifikasi workload spesifik.
2. **SDK menukar JWT dengan token akses Anthropic.** SDK mengirim JWT ke `POST /v1/oauth/token` menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). Anthropic memverifikasi JWT terhadap JWKS milik issuer dan kondisi pencocokan pada aturan federasi, lalu mengembalikan token `sk-ant-oat01-...` berumur pendek yang bertindak atas nama service account target aturan tersebut.
3. **SDK mengirim token pada setiap permintaan dan memperbaruinya sebelum kedaluwarsa.** Kode aplikasi Anda membuat klien tanpa `api_key` dan memanggil API seperti biasa. SDK menjalankan ulang pertukaran sebelum token kedaluwarsa.

## Menyiapkan federasi

Anda memerlukan peran admin, owner, atau primary owner di organisasi Anthropic Anda, penyedia identitas berkemampuan OIDC dengan endpoint JWKS yang dapat dijangkau (atau dokumen JWKS yang dapat Anda tempel, untuk klaster air-gapped), dan workload yang dapat memperoleh token identitas dari penyedia tersebut.

Wizard **Connect workload** membuat ketiga sumber daya (issuer, service account, dan aturan federasi) dalam satu alur terpandu, lalu memverifikasi koneksi secara menyeluruh.

<Steps>
  <Step title="Buka Connect workload">
    Di Claude Console, buka **Settings → Workload identity** dan pilih **Connect workload**.
  </Step>

  <Step title="Pilih penyedia Anda">
    Pilih tile untuk penyedia identitas Anda: GitHub Actions, AWS, Google Cloud, Microsoft Entra ID, atau Kubernetes. Setiap tile mengisi otomatis pola issuer URL dan field pencocokan yang didukung JWT penyedia tersebut. Untuk penyedia lain yang sesuai standar (seperti SPIFFE atau Okta), pilih **Custom OIDC**.
  </Step>

  <Step title="Isi field terpandu">
    Wizard memandu Anda melalui field khusus penyedia: konfigurasi issuer, kondisi pencocokan untuk JWT yang masuk, serta nama untuk service account dan aturan federasi yang dibuatnya. Wizard mengisi otomatis `oauth_scope=workspace:developer` dan `token_lifetime_seconds=600` (default API ketika `token_lifetime_seconds` dihilangkan adalah 3600); sesuaikan nilai ini jika workload Anda memerlukan scope atau masa berlaku yang berbeda.
  </Step>

  <Step title="Verifikasi issuer">
    Secara opsional, pilih **Verify issuer** untuk melakukan dry-run konfigurasi issuer sebelum apa pun dibuat. Verifikasi memastikan Anthropic dapat mengambil dan mem-parsing JWKS dari URL yang Anda masukkan, sehingga kesalahan keterjangkauan dan konfigurasi terdeteksi lebih awal.
  </Step>

  <Step title="Uji koneksi">
    Wizard membuat issuer, service account, dan aturan federasi, lalu menunggu pertukaran token yang berhasil selama 15 menit. Picu pertukaran dari workload Anda dalam jendela waktu tersebut (lihat [Autentikasi dari workload Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload)) untuk memastikan penyiapan berfungsi. Jika jendela waktu habis, sumber daya tetap ada; Anda dapat menjalankan ulang pengujian dari halaman detail aturan federasi. Catat ID aturan (`fdrl_...`) dan ID service account (`svac_...`) yang dibuat wizard: workload Anda mengirimkan keduanya, bersama ID organisasi Anda (dan ID workspace Anda ketika aturan mencakup lebih dari satu workspace), dalam setiap permintaan pertukaran token.
  </Step>
</Steps>

Untuk mengelola sumber daya ini secara terprogram, lihat [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api) untuk panduan curl, atau lihat [referensi API Service accounts](https://platform.claude.com/docs/id/api/admin/service_accounts), [referensi API Federation issuers](https://platform.claude.com/docs/id/api/admin/federation_issuers), dan [referensi API Federation rules](https://platform.claude.com/docs/id/api/admin/federation_rules) untuk detail parameter lengkap dan skema respons.

## Autentikasi dari workload Anda

Dengan federasi terkonfigurasi, workload Anda menukar JWT yang diterbitkan IdP dengan token Anthropic saat runtime. SDK menangani pertukaran dan siklus pembaruan untuk Anda. Tab cURL menunjukkan pertukaran HTTP yang mendasarinya untuk skrip shell, debugging, atau bahasa tanpa dukungan SDK.

### Membuat klien SDK

Anda dapat membuat klien dengan kredensial eksplisit atau tanpa argumen. Tanpa argumen, SDK me-resolve kredensial dari variabel lingkungan atau profil aktif, seperti dijelaskan di bagian [Prioritas kredensial](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#credential-precedence). Bentuk tanpa argumen adalah pola yang direkomendasikan untuk workload produksi: kirimkan image container yang sama ke mana pun dan injeksikan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, dan `ANTHROPIC_IDENTITY_TOKEN_FILE` per lingkungan.

<CodeGroup>
  ```bash cURL
  # 1. Dapatkan JWT dari IdP Anda (spesifik platform; lihat panduan per penyedia).
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

  # 3. Panggil API dengan token akses di header Authorization: Bearer.
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d @- <<'JSON' | jq -r '.content[] | select(.type == "text") | .text'
  {
    "model": "claude-opus-5",
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
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(next(block.text for block in message.content if block.type == "text"))
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
    model: "claude-opus-5",
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
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
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
              .model(Model.CLAUDE_OPUS_5)
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
      Model = Model.ClaudeOpus5,
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
      model: 'claude-opus-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );

  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text . PHP_EOL;
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
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

Respons pertukaran token mengikuti [RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1). Lihat [Respons pertukaran token](https://platform.claude.com/docs/id/manage-claude/wif-reference#token-exchange-response) untuk referensi field.

## Prioritas kredensial

Setiap SDK me-resolve kredensial dalam urutan lima tingkat yang sama: argumen konstruktor, lalu `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`, lalu `ANTHROPIC_PROFILE` eksplisit, lalu variabel lingkungan federasi, lalu profil aktif implisit. Sumber pertama yang menghasilkan kredensial yang menang.

<Warning>
  `ANTHROPIC_API_KEY` berada di atas tingkat federasi, sehingga kunci yang tertinggal di lingkungan secara diam-diam membayangi federasi. Saat memigrasikan workload dari kunci API ke Workload Identity Federation, pastikan `ANTHROPIC_API_KEY` tidak diatur di mana pun workload tersebut berjalan (env container, rahasia CI, profil shell). Perintah [`ant auth status`](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status) pada CLI melaporkan sumber mana yang menang.
</Warning>

Untuk tabel prioritas lengkap, semantik per tingkat, dan skema file profil, lihat [Prioritas kredensial di referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference#credential-precedence).

## Migrasi dari kunci API

Untuk mengalihkan workload yang ada dari kunci API statis ke federasi tanpa downtime:

1. **Konfigurasikan federasi secara paralel.** Selesaikan [panduan penyiapan](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#set-up-federation) dan pastikan aturan federasi cocok dengan token workload Anda. Biarkan `ANTHROPIC_API_KEY` yang ada tetap di tempatnya untuk saat ini.
2. **Lakukan smoke-test kredensial mana yang menang.** Jalankan `ant auth status` dari dalam workload (atau periksa log debug SDK). Karena `ANTHROPIC_API_KEY` berada di atas tingkat federasi dalam rantai prioritas, kunci API masih menang pada tahap ini.
3. **Hapus pengaturan `ANTHROPIC_API_KEY` di mana pun ia diinjeksikan.** Hapus dari rahasia CI, lingkungan container, dan profil shell (lihat peringatan sebelumnya). Jalankan ulang `ant auth status` dan pastikan sumber federasi kini terpilih.
4. **Hapus kunci API.** Setelah workload berjalan dengan token terfederasi, hapus kunci tersebut di Claude Console pada **Settings → API keys**.

## Masa berlaku dan pembaruan token

Masa berlaku token Anthropic yang dicetak adalah nilai terkecil dari (a) `token_lifetime_seconds` pada aturan (default 3.600 detik) dan (b) dua kali sisa masa berlaku JWT IdP yang Anda sajikan. Hasilnya tidak pernah kurang dari 60 detik. Batas kedua mencegah token Anthropic bertahan lebih lama dari identitas hulu asalnya melebihi margin kecil.

SDK menyimpan token dalam cache dan memperbaruinya dengan jadwal dua tingkat yang dimodelkan dari `botocore`:

* **Pembaruan anjuran (advisory refresh)** pada waktu kedaluwarsa dikurangi 120 detik. SDK mencoba pertukaran baru. Jika endpoint token tidak dapat dijangkau, SDK terus menyajikan token dalam cache, yang masih berlaku selama kira-kira 90 detik lagi.
* **Pembaruan wajib (mandatory refresh)** pada waktu kedaluwarsa dikurangi 30 detik. Pertukaran yang gagal pada titik ini memunculkan error. Token dalam cache terlalu dekat dengan kedaluwarsa untuk dianggap aman.

Karena SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pertukaran, SDK secara transparan mengambil token terproyeksi yang telah dirotasi (token service-account Kubernetes, misalnya, dirotasi jauh sebelum `exp`-nya).

Secara default, token identitas yang membawa klaim `jti` bersifat sekali pakai: setiap pertukaran harus menyajikan JWT yang belum pernah ditukar sebelumnya, dan menyajikan ulang JWT yang sama akan gagal dengan alasan `jti_reused` di [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history). Jika workload Anda mengambil tokennya sendiri dari penyedia identitas Anda, cetak JWT baru untuk setiap pertukaran alih-alih menggunakan ulang JWT dalam cache (loop retry adalah penyebab yang umum). Hal yang sama berlaku untuk token yang dibaca dari `ANTHROPIC_IDENTITY_TOKEN_FILE`: SDK membaca ulang file tersebut pada setiap pertukaran, sehingga file harus berisi token baru sebelum setiap pembaruan. Pembaruan yang membaca ulang token yang belum dirotasi, atau proses yang dimulai ulang dan menyajikan ulang token yang sudah pernah ditukarnya, ditolak dengan cara yang sama. Merotasi token jauh di dalam masa berlaku token yang dicetak menjaga file tetap mendahului jadwal pembaruan; jika sumber token Anda tidak dapat merotasi sesering itu, Anda dapat menonaktifkan `check_jti` untuk issuer tersebut sebagai upaya terakhir (ini menghapus perlindungan replay untuk setiap aturan pada issuer tersebut). Lihat [Verifikasi JWT](https://platform.claude.com/docs/id/manage-claude/wif-reference#jwt-verification) untuk detailnya.

## Penyedia identitas

Setiap panduan membahas dari mana JWT berasal di platform tersebut, seperti apa klaimnya, serta konfigurasi issuer dan aturan yang perlu didaftarkan.

<CardGroup cols={3}>
  <Card title="AWS" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/aws">
    Token web identity STS, atau token terproyeksi EKS IRSA.
  </Card>

  <Card title="Google Cloud" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/gcp">
    Token identitas bertanda tangan Google dari server metadata.
  </Card>

  <Card title="Microsoft Entra ID" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/azure">
    Managed Identity (IMDS) dan Entra Workload ID di AKS.
  </Card>

  <Card title="GitHub Actions" icon="github-logo" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions">
    Autentikasi CI tanpa kunci dengan token OIDC Actions.
  </Card>

  <Card title="Kubernetes" icon="cube" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/kubernetes">
    Klaster yang dikelola sendiri dan on-premises menggunakan token service-account terproyeksi.
  </Card>

  <Card title="SPIFFE" icon="fingerprint" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe">
    Workload dengan SPIFFE JWT-SVID dari SPIRE atau penerbit lain yang sesuai.
  </Card>

  <Card title="Okta" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/okta">
    Aplikasi layanan Okta yang menggunakan alur client-credentials.
  </Card>
</CardGroup>

## Lihat juga

* [Mengelola WIF dengan Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api): membuat issuer, service account, dan aturan dari infrastructure as code
* [Referensi WIF](https://platform.claude.com/docs/id/manage-claude/wif-reference): variabel lingkungan, skema file profil, aturan validasi, dan kode error
* [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication): semua opsi autentikasi di seluruh SDK Anthropic
* [Referensi Admin API](https://platform.claude.com/docs/id/api/admin): skema permintaan dan respons yang dihasilkan untuk setiap endpoint Admin API
