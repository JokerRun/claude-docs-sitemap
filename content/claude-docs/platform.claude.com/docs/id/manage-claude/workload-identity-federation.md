---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workload-identity-federation
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: ca19dca160e71aa5ce3ae6788b5ce032222924e872841e667dc85d611362d264
---

# Workload Identity Federation

Autentikasi workload ke Claude API dengan token identitas berumur pendek dari penyedia identitas Anda sendiri, alih-alih kunci API statis berumur panjang.

---

"Workload Identity Federation" (federasi identitas workload), atau WIF, memungkinkan workload Anda melakukan autentikasi ke Claude API dengan token OpenID Connect (OIDC) berumur pendek, alih-alih kunci API `sk-ant-...` berumur panjang. Token tersebut berasal dari "identity provider" (penyedia identitas), atau IdP, yang sudah Anda operasikan: AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar seperti GitHub Actions, Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta.

Workload Anda menyajikan JWT yang ditandatangani dari penyedia identitas Anda. Anthropic memvalidasinya terhadap aturan kepercayaan yang Anda konfigurasikan di Claude Console dan mengembalikan token akses Anthropic berumur pendek yang terikat ke service account di organisasi Anda. Tidak ada rahasia statis yang perlu dibuat, disimpan di CI, dirotasi, atau berisiko bocor.

Workload Identity Federation memperkuat postur keamanan Anda dengan mengganti kunci API statis dengan token yang kedaluwarsa dalam hitungan menit, bukan tidak pernah kedaluwarsa. Namun, ini bukan solusi keamanan yang lengkap dengan sendirinya: autentikasi terfederasi hanya sekuat penyedia identitas hulu yang menandatangani JWT tersebut. Padukan Workload Identity Federation dengan kontrol yang sudah didukung IdP Anda (pengikatan identitas workload, akses bersyarat, pencatatan audit) untuk pertahanan berlapis.

## Konsep \{#concepts}

Anda mengonfigurasi tiga sumber daya di Claude Console sebelum workload apa pun dapat melakukan federasi. Bersama-sama, ketiganya menyatakan "token yang ditandatangani oleh penerbit X, dengan klaim yang terlihat seperti Y, boleh bertindak sebagai service account Z."

### Service account \{#service-accounts}

**Service account** (`svac_...`) adalah identitas non-manusia yang diberi nama di dalam organisasi Anthropic Anda. Ini adalah principal yang diwakili oleh token terfederasi. Service account berada di tingkat organisasi dan menjadi aktif di sebuah workspace ketika Anda menambahkannya sebagai anggota workspace tersebut. Pada saat pertukaran, Anthropic memeriksa bahwa workspace pada federation rule cocok dengan salah satu keanggotaan workspace service account; token yang dihasilkan kemudian mengikuti batas laju dan atribusi penggunaan workspace tersebut, sama seperti kunci API. Tidak seperti pengguna manusia, service account tidak memiliki email, kata sandi, maupun login Console. Setiap service account secara implisit merupakan anggota workspace default organisasi Anda; tambahkan keanggotaan eksplisit untuk workspace lain tempat service account tersebut harus bertindak.

Perbedaan utama dari kunci API: kunci API *adalah* kredensial, sedangkan service account *memiliki* kredensial yang dibuat untuknya sesuai permintaan. Anda dapat mengaudit workload mana yang bertindak sebagai service account mana.

### Federation issuer \{#federation-issuers}

**Federation issuer** (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Mendaftarkan issuer memberi tahu Anthropic "JWT yang ditandatangani oleh penyedia ini boleh menyatakan identitas workload untuk organisasi saya."

Sebuah issuer memiliki dua bagian konfigurasi:

- **Issuer URL:** Nilai klaim `iss` persis yang muncul di JWT penyedia, misalnya `https://token.actions.githubusercontent.com` atau `https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLE`.
- **Sumber JWKS:** Cara Anthropic mengambil kunci publik untuk memverifikasi tanda tangan JWT. Gunakan `discovery` (default) untuk penyedia apa pun yang menyajikan `/.well-known/openid-configuration` di URL issuer-nya. Gunakan `explicit_url` untuk menunjuk langsung ke endpoint JWKS, atau `inline` untuk mengunggah kumpulan kunci bagi issuer yang tidak dapat dijangkau dari internet publik (misalnya, klaster Kubernetes privat).

URL issuer dan JWKS harus menggunakan `https`, pada port 443, dan menggunakan nama host DNS publik yang me-resolve ke alamat IP publik; literal IP tidak diterima. Batasan ini hanya berlaku untuk URL yang diambil Anthropic; dalam mode `explicit_url` dan `inline`, `issuer_url` dibandingkan sebagai string dan boleh merujuk ke nama host internal.

Anda biasanya mendaftarkan satu issuer per lingkungan: klaster EKS produksi Anda, klaster staging Anda, dan GitHub Actions adalah tiga issuer terpisah.

### Federation rule \{#federation-rules}

**Federation rule** (`fdrl_...`) adalah jembatan antara issuer dan service account: "ketika JWT dari issuer X memiliki klaim yang terlihat seperti Y, buat token untuk service account Z dengan scope S."

Sebuah rule mendefinisikan kondisi pencocokan, target, serta scope otorisasi dan masa berlaku token yang diterapkan ketika rule tersebut cocok:

- **Match:** Kondisi yang harus dipenuhi oleh JWT yang masuk. Anda dapat mencocokkan pada `subject_prefix` (misalnya, `system:serviceaccount:prod:worker`, atau dengan `*` di akhir untuk pencocokan prefiks), `audience` yang persis, map nilai klaim yang persis, ekspresi `condition` [CEL](https://cel.dev/) untuk logika kompleks, atau kombinasi apa pun. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur, dan semua matcher yang dikonfigurasi harus lolos agar JWT diterima.
- **Target:** Service account yang dipetakan ke JWT yang cocok.
- **Authorization:** `scope` OAuth yang diberikan pada token yang dihasilkan. Default-nya adalah `workspace:developer`, yang memberikan akses yang sama dengan kunci API yang diterbitkan untuk workspace tersebut. Beberapa produk mengunci scope ketika Anda membuat rule dari alur mereka; misalnya, modal create-tunnel pada [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) membuat rule dengan scope `org:manage_tunnels`. Lihat [OAuth scopes](/docs/id/manage-claude/wif-reference#oauth-scopes). Rule juga mengatur `token_lifetime_seconds` (60 hingga 86400, default 3600).

Satu issuer dapat memiliki banyak rule: satu per tim, namespace, atau tingkat izin. Rule dievaluasi berdasarkan ID: klien menentukan rule mana yang akan digunakan dalam permintaan pertukaran, dan Anthropic memverifikasi bahwa JWT memenuhi kriteria pencocokan rule tersebut. Tidak ada pencarian rule implisit.

## Cara kerjanya \{#how-it-works}

1. **IdP Anda menerbitkan JWT ke workload.** Pada sebagian besar platform, ini bersifat ambient: projected service-account token Kubernetes, server metadata Google Cloud, Azure IMDS, atau endpoint OIDC GitHub Actions. Klaim `iss` pada JWT mengidentifikasi penyedia, dan klaim `sub` serta klaim lainnya mengidentifikasi workload spesifik.
2. **SDK menukar JWT dengan token akses Anthropic.** SDK mengirim JWT ke `POST /v1/oauth/token` menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). Anthropic memverifikasi JWT terhadap JWKS issuer dan kondisi pencocokan federation rule, lalu mengembalikan token `sk-ant-oat01-...` berumur pendek yang bertindak atas nama service account target rule tersebut.
3. **SDK mengirim token pada setiap permintaan dan me-refresh-nya sebelum kedaluwarsa.** Kode aplikasi Anda membangun klien tanpa `api_key` dan memanggil API seperti biasa. SDK menjalankan ulang pertukaran sebelum token kedaluwarsa.

## Menyiapkan federasi \{#set-up-federation}

Anda memerlukan peran admin, owner, atau primary owner di organisasi Anthropic Anda, penyedia identitas yang mendukung OIDC dengan endpoint JWKS yang dapat dijangkau (atau dokumen JWKS yang dapat Anda tempel, untuk klaster air-gapped), dan workload yang dapat memperoleh token identitas dari penyedia tersebut.

Wizard **Connect workload** membuat ketiga sumber daya (issuer, service account, dan federation rule) dalam satu alur terpandu, lalu memverifikasi koneksi secara end-to-end.

<Steps>
  <Step title="Buka Connect workload">
    Di Claude Console, buka **Settings → Workload identity** dan pilih **Connect workload**.
  </Step>

  <Step title="Pilih penyedia Anda">
    Pilih kartu untuk penyedia identitas Anda: GitHub Actions, AWS, Google Cloud, Microsoft Entra ID, atau Kubernetes. Setiap kartu mengisi otomatis pola URL issuer dan field pencocokan yang didukung JWT penyedia tersebut. Untuk penyedia lain yang sesuai standar (seperti SPIFFE atau Okta), pilih **Custom OIDC**.
  </Step>

  <Step title="Isi field terpandu">
    Wizard memandu Anda melalui field spesifik penyedia: konfigurasi issuer, kondisi pencocokan untuk JWT yang masuk, dan nama untuk service account dan federation rule yang dibuatnya. Wizard mengisi otomatis `oauth_scope=workspace:developer` dan `token_lifetime_seconds=600` (default API ketika `token_lifetime_seconds` dihilangkan adalah 3600); sesuaikan ini jika workload Anda memerlukan scope atau masa berlaku yang berbeda.
  </Step>

  <Step title="Verifikasi issuer">
    Secara opsional, pilih **Verify issuer** untuk menjalankan dry-run konfigurasi issuer sebelum apa pun dibuat. Verifikasi mengonfirmasi bahwa Anthropic dapat mengambil dan mengurai JWKS dari URL yang Anda masukkan, yang membantu menangkap kesalahan keterjangkauan dan konfigurasi lebih awal.
  </Step>

  <Step title="Uji koneksi">
    Wizard membuat issuer, service account, dan federation rule, lalu menunggu pertukaran token yang berhasil selama 15 menit. Picu pertukaran dari workload Anda dalam jendela waktu tersebut (lihat [Autentikasi dari workload Anda](#authenticate-from-your-workload)) untuk mengonfirmasi bahwa penyiapan berfungsi. Jika jendela waktu berlalu, sumber daya tetap ada; Anda dapat menjalankan ulang pengujian dari halaman detail federation rule. Catat ID rule (`fdrl_...`) dan ID service account (`svac_...`) yang dibuat wizard: workload Anda meneruskan keduanya, bersama dengan ID organisasi Anda (dan ID workspace Anda ketika rule mencakup lebih dari satu workspace), dalam setiap permintaan pertukaran token.
  </Step>
</Steps>

Untuk mengelola sumber daya ini secara terprogram, lihat [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api) untuk panduan curl, atau lihat [referensi API Service accounts](/docs/id/api/admin/service_accounts), [referensi API Federation issuers](/docs/id/api/admin/federation_issuers), dan [referensi API Federation rules](/docs/id/api/admin/federation_rules) untuk detail parameter lengkap dan skema respons.

## Autentikasi dari workload Anda \{#authenticate-from-your-workload}

Dengan federasi yang telah dikonfigurasi, workload Anda menukar JWT yang diterbitkan IdP dengan token Anthropic saat runtime. SDK menangani pertukaran dan loop refresh untuk Anda. Tab cURL menunjukkan pertukaran HTTP yang mendasarinya untuk skrip shell, debugging, atau bahasa tanpa dukungan SDK.

### Membangun klien SDK \{#construct-the-sdk-client}

Anda dapat membangun klien dengan kredensial eksplisit atau tanpa argumen. Tanpa argumen, SDK me-resolve kredensial dari variabel lingkungan atau profil aktif, seperti dijelaskan di bawah [Prioritas kredensial](#credential-precedence). Bentuk tanpa argumen adalah pola yang direkomendasikan untuk workload produksi: kirimkan image container yang sama ke mana saja dan injeksikan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, dan `ANTHROPIC_IDENTITY_TOKEN_FILE` per lingkungan.

<CodeGroup>

```bash cURL nocheck
# 1. Dapatkan JWT dari IdP Anda (spesifik per platform; lihat panduan masing-masing penyedia).
JWT=$(cat /var/run/secrets/anthropic.com/token)

# 2. Tukarkan dengan token akses Anthropic berumur pendek.
RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  --data @- <<JSON
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
  --data @- <<'JSON' | jq -r '.content[0].text'
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "Hello, Claude"}]
}
JSON
```

```python Python nocheck
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
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(message.content[0].text)
```

```typescript TypeScript nocheck
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
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }]
});
for (const block of message.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
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
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(message.Content[0].Text)
}
```

```java Java nocheck hidelines={1..11,-1}
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
            .model(Model.CLAUDE_SONNET_4_6)
            .maxTokens(1024)
            .addUserMessage("Hello, Claude")
            .build());

    IO.println(message.content());
}
```

```csharp C# nocheck hidelines={1..3}
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
    Model = Model.ClaudeSonnet4_6,
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

```php PHP nocheck hidelines={1..4}
<?php

require_once __DIR__ . '/vendor/autoload.php';

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
    model: 'claude-sonnet-4-6',
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
);

echo $message->content[0]->text . PHP_EOL;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

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
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}]
)

puts message.content.first.text
```

</CodeGroup>

Respons pertukaran token mengikuti [RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1). Lihat [Respons pertukaran token](/docs/id/manage-claude/wif-reference#token-exchange-response) untuk referensi field.

## Prioritas kredensial \{#credential-precedence}

Setiap SDK me-resolve kredensial dalam urutan lima tingkat yang sama: argumen konstruktor, lalu `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`, lalu `ANTHROPIC_PROFILE` eksplisit, lalu variabel lingkungan federasi, lalu profil aktif implisit. Sumber pertama yang menghasilkan kredensial akan menang.

<Warning>
  `ANTHROPIC_API_KEY` berada di atas tingkat federasi, sehingga kunci yang tertinggal di
  lingkungan secara diam-diam membayangi federasi. Saat memigrasikan workload dari kunci
  API ke Workload Identity Federation, pastikan `ANTHROPIC_API_KEY` tidak diatur di mana pun workload tersebut
  berjalan (env container, secret CI, profil shell). Perintah [`ant auth status`](/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status)
  pada CLI melaporkan sumber mana yang menang.
</Warning>

Untuk tabel prioritas lengkap, semantik per tingkat, dan skema file profil, lihat [Prioritas kredensial](/docs/id/manage-claude/wif-reference#credential-precedence) di referensi WIF.

## Migrasi dari kunci API \{#migrate-from-api-keys}

Untuk mengalihkan workload yang ada dari kunci API statis ke federasi tanpa downtime:

1. **Konfigurasikan federasi secara paralel.** Selesaikan [panduan penyiapan](#set-up-federation) dan konfirmasi bahwa federation rule cocok dengan token workload Anda. Biarkan `ANTHROPIC_API_KEY` yang ada tetap di tempatnya untuk saat ini.
2. **Lakukan smoke-test untuk melihat kredensial mana yang menang.** Jalankan `ant auth status` dari dalam workload (atau periksa log debug SDK). Karena `ANTHROPIC_API_KEY` berada di atas tingkat federasi dalam rantai prioritas, kunci API masih menang pada tahap ini.
3. **Hapus `ANTHROPIC_API_KEY` di mana pun ia diinjeksikan.** Hapus dari secret CI, lingkungan container, dan profil shell (lihat peringatan sebelumnya). Jalankan ulang `ant auth status` dan konfirmasi bahwa sumber federasi sekarang terpilih.
4. **Cabut kunci API.** Setelah workload berjalan dengan token terfederasi, hapus kunci tersebut di Claude Console di bawah **Settings → API keys**.

## Masa berlaku dan refresh token \{#token-lifetime-and-refresh}

Masa berlaku token Anthropic yang dihasilkan adalah nilai yang lebih kecil antara (a) `token_lifetime_seconds` pada rule (default 3600 detik) dan (b) dua kali sisa masa berlaku JWT IdP yang Anda sajikan. Hasilnya tidak pernah kurang dari 60 detik. Batasan kedua mencegah token Anthropic bertahan lebih lama dari identitas hulu yang menjadi sumbernya dengan selisih lebih dari margin kecil.

SDK menyimpan token dalam cache dan me-refresh-nya dengan jadwal dua tingkat yang dimodelkan dari `botocore`:

- **Advisory refresh** pada waktu kedaluwarsa dikurangi 120 detik. SDK mencoba pertukaran baru. Jika endpoint token tidak dapat dijangkau, SDK terus menyajikan token yang di-cache, yang masih valid selama kira-kira 90 detik lagi.
- **Mandatory refresh** pada waktu kedaluwarsa dikurangi 30 detik. Pertukaran yang gagal pada titik ini memunculkan error. Token yang di-cache terlalu dekat dengan waktu kedaluwarsa untuk dianggap aman.

Karena SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pertukaran, SDK secara transparan mengambil projected token yang dirotasi (token service-account Kubernetes, misalnya, dirotasi jauh sebelum `exp`-nya).

## Penyedia identitas \{#identity-providers}

Setiap panduan membahas dari mana JWT berasal pada platform tersebut, seperti apa klaimnya, serta konfigurasi issuer dan rule yang perlu didaftarkan.

<CardGroup cols={3}>
  <Card title="AWS" icon="cloud" href="/docs/id/manage-claude/wif-providers/aws">
    Token identitas web STS, atau projected token EKS IRSA.
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
    Klaster self-managed dan on-premises menggunakan projected service-account token.
  </Card>
  <Card title="SPIFFE" icon="fingerprint" href="/docs/id/manage-claude/wif-providers/spiffe">
    Workload dengan SPIFFE JWT-SVID dari SPIRE atau issuer lain yang sesuai standar.
  </Card>
  <Card title="Okta" icon="lock" href="/docs/id/manage-claude/wif-providers/okta">
    Aplikasi layanan Okta menggunakan alur client-credentials.
  </Card>
</CardGroup>

## Lihat juga \{#see-also}

- [Mengelola WIF dengan Admin API](/docs/id/manage-claude/wif-admin-api): membuat issuer, service account, dan rule dari infrastructure as code
- [Referensi WIF](/docs/id/manage-claude/wif-reference): variabel lingkungan, skema file profil, aturan validasi, dan kode error
- [Autentikasi](/docs/id/manage-claude/authentication): semua opsi autentikasi di seluruh SDK Anthropic
- [Referensi Admin API](/docs/id/api/admin): skema permintaan dan respons yang dihasilkan untuk setiap endpoint Admin API