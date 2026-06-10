---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/workload-identity-federation
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 5af4d8979567fd9ee658e4d60de85a51f39a9b8568d43a9ab612dcb79809d2bc
---

# Workload Identity Federation

Autentikasi workload ke Claude API dengan token identitas berumur pendek dari penyedia identitas Anda sendiri, alih-alih kunci API statis berumur panjang.

---

"Workload Identity Federation" (federasi identitas workload), atau WIF, memungkinkan workload Anda melakukan autentikasi ke Claude API dengan token OpenID Connect (OIDC) berumur pendek alih-alih kunci API `sk-ant-...` berumur panjang. Token tersebut berasal dari "identity provider" (penyedia identitas), atau IdP, yang sudah Anda operasikan: AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar seperti GitHub Actions, Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta.

Workload Anda menyajikan JWT yang ditandatangani dari penyedia identitas Anda. Anthropic memvalidasinya terhadap aturan kepercayaan yang Anda konfigurasikan di Claude Console dan mengembalikan token akses Anthropic berumur pendek yang terikat ke akun layanan di organisasi Anda. Tidak ada rahasia statis yang perlu dibuat, disimpan di CI, dirotasi, atau berisiko bocor.

Workload Identity Federation memperkuat postur keamanan Anda dengan mengganti kunci API statis dengan token yang kedaluwarsa dalam hitungan menit, bukan tidak pernah kedaluwarsa. Namun, ini bukan solusi keamanan yang lengkap dengan sendirinya: autentikasi terfederasi hanya sekuat penyedia identitas upstream yang menandatangani JWT tersebut. Padukan Workload Identity Federation dengan kontrol yang sudah didukung IdP Anda (pengikatan identitas workload, akses bersyarat, pencatatan audit) untuk pertahanan berlapis.

## Konsep \{#concepts}

Anda mengonfigurasi tiga sumber daya di Claude Console sebelum workload apa pun dapat melakukan federasi. Bersama-sama, ketiganya menyatakan "token yang ditandatangani oleh penerbit X, dengan klaim yang terlihat seperti Y, boleh bertindak sebagai akun layanan Z."

### Akun layanan \{#service-accounts}

**Akun layanan** (`svac_...`) adalah identitas non-manusia bernama di dalam organisasi Anthropic Anda. Ini adalah prinsipal yang diwakili oleh token terfederasi saat bertindak. Akun layanan berada di tingkat organisasi dan menjadi aktif di sebuah workspace ketika Anda menambahkannya sebagai anggota workspace tersebut. Pada saat pertukaran, Anthropic memeriksa bahwa workspace pada aturan federasi cocok dengan salah satu keanggotaan workspace akun layanan; token yang dibuat kemudian mengikuti batas laju dan atribusi penggunaan workspace tersebut, sama seperti kunci API. Tidak seperti pengguna manusia, akun layanan tidak memiliki email, kata sandi, maupun login Console.

Perbedaan utama dari kunci API: kunci API *adalah* kredensial, sedangkan akun layanan *memiliki* kredensial yang dibuat untuknya sesuai permintaan. Anda dapat mengaudit workload mana yang bertindak sebagai akun layanan mana.

### Penerbit federasi \{#federation-issuers}

**Penerbit federasi** (`fdis_...`) mendaftarkan penyedia identitas OIDC ke organisasi Anda. Mendaftarkan penerbit memberi tahu Anthropic "JWT yang ditandatangani oleh penyedia ini boleh menyatakan identitas workload untuk organisasi saya."

Sebuah penerbit memiliki dua bagian konfigurasi:

- **Issuer URL:** Nilai klaim `iss` persis yang muncul di JWT penyedia, misalnya `https://token.actions.githubusercontent.com` atau `https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLE`.
- **Sumber JWKS:** Cara Anthropic mengambil kunci publik untuk memverifikasi tanda tangan JWT. Gunakan `discovery` (default) untuk penyedia apa pun yang menyajikan `/.well-known/openid-configuration` di URL penerbitnya. Gunakan `explicit_url` untuk menunjuk langsung ke endpoint JWKS, atau `inline` untuk mengunggah kumpulan kunci bagi penerbit yang tidak dapat dijangkau dari internet publik (misalnya, klaster Kubernetes privat).

URL penerbit dan JWKS harus menggunakan `https`, pada port 443, dan menggunakan nama host DNS publik yang me-resolve ke alamat IP publik; literal IP tidak diterima. Batasan ini hanya berlaku untuk URL yang diambil Anthropic; dalam mode `explicit_url` dan `inline`, `issuer_url` dibandingkan sebagai string dan boleh merujuk ke nama host internal.

Anda biasanya mendaftarkan satu penerbit per lingkungan: klaster EKS produksi Anda, klaster staging Anda, dan GitHub Actions adalah tiga penerbit terpisah.

### Aturan federasi \{#federation-rules}

**Aturan federasi** (`fdrl_...`) adalah jembatan antara penerbit dan akun layanan: "ketika JWT dari penerbit X memiliki klaim yang terlihat seperti Y, buat token untuk akun layanan Z dengan cakupan S."

Sebuah aturan mendefinisikan kondisi pencocokan, target, serta cakupan otorisasi dan masa berlaku token yang diterapkan ketika aturan tersebut cocok:

- **Match:** Kondisi yang harus dipenuhi oleh JWT yang masuk. Anda dapat mencocokkan berdasarkan `subject_prefix` (misalnya, `system:serviceaccount:prod:worker`, atau dengan `*` di akhir untuk pencocokan prefiks), `audience` yang persis, map nilai klaim yang persis, ekspresi `condition` [CEL](https://cel.dev/) untuk logika kompleks, atau kombinasi apa pun. Setidaknya salah satu dari `subject_prefix`, `claims`, atau `condition` harus diatur, dan semua pencocok yang dikonfigurasi harus lolos agar JWT diterima.
- **Target:** Akun layanan yang dipetakan ke JWT yang cocok.
- **Authorization:** `scope` OAuth yang diberikan pada token yang dibuat. Default-nya adalah `workspace:developer`, yang memberikan akses yang sama seperti kunci API yang diterbitkan untuk workspace tersebut. Beberapa produk mengunci cakupan ketika Anda membuat aturan dari alur mereka; misalnya, modal create-tunnel pada [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) membuat aturan dengan cakupan `org:manage_tunnels`. Lihat [Cakupan OAuth](/docs/id/manage-claude/wif-reference#oauth-scopes). Aturan ini juga mengatur `token_lifetime_seconds` (60 hingga 86400, default 3600).

Satu penerbit dapat memiliki banyak aturan: satu per tim, namespace, atau tingkat izin. Aturan dievaluasi berdasarkan ID: klien menentukan aturan mana yang akan digunakan dalam permintaan pertukaran, dan Anthropic memverifikasi bahwa JWT memenuhi kriteria pencocokan aturan tersebut. Tidak ada pencarian aturan implisit.

## Cara kerjanya \{#how-it-works}

1. **IdP Anda menerbitkan JWT ke workload.** Pada sebagian besar platform, ini bersifat ambien: token service-account terproyeksi Kubernetes, server metadata Google Cloud, Azure IMDS, atau endpoint OIDC GitHub Actions. Klaim `iss` pada JWT mengidentifikasi penyedia, dan klaim `sub` serta klaim lainnya mengidentifikasi workload spesifik.
2. **SDK menukar JWT dengan token akses Anthropic.** SDK mengirim JWT ke `POST /v1/oauth/token` menggunakan grant `jwt-bearer` [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523). Anthropic memverifikasi JWT terhadap JWKS penerbit dan kondisi pencocokan aturan federasi, lalu mengembalikan token `sk-ant-oat01-...` berumur pendek yang bertindak atas nama akun layanan target aturan tersebut.
3. **SDK mengirim token pada setiap permintaan dan me-refresh-nya sebelum kedaluwarsa.** Kode aplikasi Anda membuat klien tanpa `api_key` dan memanggil API seperti biasa. SDK menjalankan ulang pertukaran sebelum token kedaluwarsa.

## Menyiapkan federasi \{#set-up-federation}

Anda memerlukan akses admin ke organisasi Anthropic Anda, penyedia identitas berkemampuan OIDC dengan endpoint JWKS yang dapat dijangkau (atau dokumen JWKS yang dapat Anda tempel, untuk klaster air-gapped), dan workload yang dapat memperoleh token identitas dari penyedia tersebut.

Di Claude Console, buka **Settings → Workload identity**.

<Steps>
  <Step title="Daftarkan penerbit">
    Pada tab **Issuers**, pilih **Create issuer**.

    | Kolom | Nilai |
    | --- | --- |
    | Name | Label untuk referensi Anda, seperti `prod-eks` atau `gha`. Huruf kecil, angka, dan tanda hubung. |
    | Issuer URL | Klaim `iss` persis yang dimasukkan IdP Anda ke dalam JWT-nya. Jika Anda tidak yakin, dekode token sampel: <code>jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' token</code> |
    | JWKS source | `discovery` untuk sebagian besar IdP terkelola. Pilih `explicit_url` atau `inline` hanya jika discovery tidak tersedia. |
    | Discovery base / JWKS URL / Inline keys | Spesifik per mode. Biarkan kosong untuk discovery jika IdP menyajikan `.well-known` di URL penerbit. |
    | CA cert PEM | Hanya jika IdP Anda menyajikan TLS dari CA privat. Sebagian besar IdP terkelola menggunakan CA publik, jadi biarkan kosong. |

    Console menyertakan preset untuk AWS dan Google Cloud yang mengisi otomatis pola URL penerbit dan aturan default yang masuk akal, ditambah opsi OIDC generik untuk penyedia lain yang sesuai standar (seperti GitHub Actions, penerbit service-account Kubernetes, Microsoft Entra ID, atau Okta).
  </Step>

  <Step title="Buat akun layanan">
    Buka **Settings → Service accounts → Create service account**. Berikan nama (misalnya, `inference-worker` atau `ci-deploy`) dan deskripsi opsional.

    Ini adalah identitas yang diwakili oleh token yang dibuat. Tambahkan akun layanan ke setiap workspace tempat ia harus bertindak dari halaman **Members** workspace tersebut. Aturan federasi pada langkah berikutnya menargetkan satu workspace, dan token yang dibuat dicakup ke batas laju dan atribusi penggunaan workspace tersebut. Catat ID akun layanan (`svac_...`).
  </Step>

  <Step title="Buat aturan federasi">
    Kembali ke halaman **Workload identity**, buka tab **Federation rules** dan pilih **Create rule**.

    | Bagian | Nilai |
    | --- | --- |
    | Basic info | Nama dan deskripsi opsional. Pilih penerbit yang Anda daftarkan di langkah 1. |
    | Match | Pilih **Static** untuk pencocokan prefiks subjek, audience, dan klaim persis, atau **CEL** untuk ekspresi. Buat sespesifik yang diizinkan oleh klaim IdP Anda: aturan yang mencocokkan terlalu luas memberikan akses lebih dari yang Anda maksudkan. |
    | Target | Pilih akun layanan yang Anda buat di langkah 2. |
    | Authorization | Cakupan OAuth (`workspace:developer` secara default, atau cakupan spesifik produk seperti `org:manage_tunnels`; lihat [Cakupan OAuth](/docs/id/manage-claude/wif-reference#oauth-scopes)) dan masa berlaku token dalam detik. |

    Catat ID aturan (`fdrl_...`). Workload Anda meneruskan ID ini di setiap permintaan pertukaran token.
  </Step>
</Steps>

## Autentikasi dari workload Anda \{#authenticate-from-your-workload}

Dengan federasi yang telah dikonfigurasi, workload Anda menukar JWT yang diterbitkan IdP dengan token Anthropic pada saat runtime. SDK menangani pertukaran dan loop refresh untuk Anda. Tab cURL menunjukkan pertukaran HTTP yang mendasarinya untuk skrip shell, debugging, atau bahasa tanpa dukungan SDK.

### Membuat klien SDK \{#construct-the-sdk-client}

Anda dapat membuat klien dengan kredensial eksplisit atau tanpa argumen. Tanpa argumen, SDK me-resolve kredensial dari variabel lingkungan atau profil aktif, seperti dijelaskan di bagian [Prioritas kredensial](#credential-precedence). Bentuk tanpa argumen adalah pola yang direkomendasikan untuk workload produksi: kirimkan image container yang sama ke mana saja dan injeksikan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, dan `ANTHROPIC_IDENTITY_TOKEN_FILE` per lingkungan.

<CodeGroup>

```bash cURL nocheck
# 1. Dapatkan JWT dari IdP Anda (spesifik platform; lihat panduan per penyedia).
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

Respons pertukaran token mengikuti [RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1). Lihat [Respons pertukaran token](/docs/id/manage-claude/wif-reference#token-exchange-response) untuk referensi kolom.

## Prioritas kredensial \{#credential-precedence}

Setiap SDK me-resolve kredensial dalam urutan lima tingkat yang sama: argumen konstruktor, lalu `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`, lalu `ANTHROPIC_PROFILE` eksplisit, lalu variabel lingkungan federasi, lalu profil aktif implisit. Sumber pertama yang menghasilkan kredensial akan menang.

<Warning>
  `ANTHROPIC_API_KEY` berada di atas tingkat federasi, sehingga kunci yang tertinggal di
  lingkungan secara diam-diam membayangi federasi. Saat memigrasikan workload dari kunci
  API ke Workload Identity Federation, pastikan `ANTHROPIC_API_KEY` tidak diatur di mana pun workload tersebut
  berjalan (env container, rahasia CI, profil shell). Perintah [`ant auth status`](/docs/id/cli-sdks-libraries/cli/authentication#check-authentication-status)
  pada CLI melaporkan sumber mana yang menang.
</Warning>

Untuk tabel prioritas lengkap, semantik per tingkat, dan skema file profil, lihat [Prioritas kredensial](/docs/id/manage-claude/wif-reference#credential-precedence) di referensi WIF.

## Migrasi dari kunci API \{#migrate-from-api-keys}

Untuk mengalihkan workload yang ada dari kunci API statis ke federasi tanpa downtime:

1. **Konfigurasikan federasi secara paralel.** Selesaikan [panduan penyiapan](#set-up-federation) dan pastikan aturan federasi cocok dengan token workload Anda. Biarkan `ANTHROPIC_API_KEY` yang ada tetap di tempatnya untuk saat ini.
2. **Lakukan smoke-test untuk melihat kredensial mana yang menang.** Jalankan `ant auth status` dari dalam workload (atau periksa log debug SDK). Karena `ANTHROPIC_API_KEY` berada di atas tingkat federasi dalam rantai prioritas, kunci API masih menang pada tahap ini.
3. **Hapus pengaturan `ANTHROPIC_API_KEY` di mana pun ia diinjeksikan.** Hapus dari rahasia CI, lingkungan container, dan profil shell (lihat peringatan sebelumnya). Jalankan ulang `ant auth status` dan pastikan sumber federasi sekarang terpilih.
4. **Cabut kunci API.** Setelah workload berjalan dengan token terfederasi, hapus kunci tersebut di Claude Console di bawah **Settings → API keys**.

## Masa berlaku token dan refresh \{#token-lifetime-and-refresh}

Masa berlaku token Anthropic yang dibuat adalah nilai yang lebih kecil antara (a) `token_lifetime_seconds` aturan (default 3600 detik) dan (b) dua kali sisa masa berlaku JWT IdP yang Anda sajikan. Hasilnya tidak pernah kurang dari 60 detik. Batasan kedua mencegah token Anthropic bertahan lebih lama dari identitas upstream asalnya dengan selisih lebih dari margin kecil.

SDK menyimpan token dalam cache dan me-refresh-nya dengan jadwal dua tingkat yang dimodelkan dari `botocore`:

- **Advisory refresh** pada waktu kedaluwarsa dikurangi 120 detik. SDK mencoba pertukaran baru. Jika endpoint token tidak dapat dijangkau, SDK terus menyajikan token yang di-cache, yang masih valid selama sekitar 90 detik lagi.
- **Mandatory refresh** pada waktu kedaluwarsa dikurangi 30 detik. Pertukaran yang gagal pada titik ini memunculkan error. Token yang di-cache terlalu dekat dengan waktu kedaluwarsa untuk aman digunakan.

Karena SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pertukaran, SDK secara transparan mengambil token terproyeksi yang dirotasi (token service-account Kubernetes, misalnya, dirotasi jauh sebelum `exp`-nya).

## Penyedia identitas \{#identity-providers}

Setiap panduan membahas dari mana JWT berasal pada platform tersebut, seperti apa klaimnya, serta konfigurasi penerbit dan aturan yang perlu didaftarkan.

<CardGroup cols={3}>
  <Card title="AWS" icon="cloud" href="/docs/id/manage-claude/wif-providers/aws">
    Token identitas web STS, atau token terproyeksi EKS IRSA.
  </Card>
  <Card title="Google Cloud" icon="cloud" href="/docs/id/manage-claude/wif-providers/gcp">
    Token identitas yang ditandatangani Google dari server metadata.
  </Card>
  <Card title="Microsoft Azure" icon="cloud" href="/docs/id/manage-claude/wif-providers/azure">
    Managed Identity (IMDS) dan Entra Workload ID di AKS.
  </Card>
  <Card title="GitHub Actions" icon="github-logo" href="/docs/id/manage-claude/wif-providers/github-actions">
    Autentikasi CI tanpa kunci dengan token OIDC Actions.
  </Card>
  <Card title="Kubernetes" icon="cube" href="/docs/id/manage-claude/wif-providers/kubernetes">
    Klaster yang dikelola sendiri dan on-premises menggunakan token service-account terproyeksi.
  </Card>
  <Card title="SPIFFE" icon="fingerprint" href="/docs/id/manage-claude/wif-providers/spiffe">
    Workload dengan SPIFFE JWT-SVID dari SPIRE atau penerbit lain yang sesuai standar.
  </Card>
  <Card title="Okta" icon="lock" href="/docs/id/manage-claude/wif-providers/okta">
    Aplikasi layanan Okta menggunakan alur client-credentials.
  </Card>
</CardGroup>

## Lihat juga \{#see-also}

- [Referensi WIF](/docs/id/manage-claude/wif-reference): variabel lingkungan, skema file profil, aturan validasi, dan kode error
- [Autentikasi](/docs/id/manage-claude/authentication): semua opsi autentikasi di seluruh SDK Anthropic