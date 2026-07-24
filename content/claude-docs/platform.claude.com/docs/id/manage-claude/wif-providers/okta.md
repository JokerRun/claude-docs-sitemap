---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/okta
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 9a381618e3f2785b499fd78a2f841cd2060dbdb483e7b1a22b5e40efc8cb3c91
---

# Menggunakan WIF dengan Okta

Federasikan identitas aplikasi layanan Okta ke Claude API dengan Workload Identity Federation.

---

Okta dapat bertindak sebagai penyedia identitas workload dengan menerbitkan token akses OIDC ke **aplikasi layanan** melalui grant OAuth 2.0 `client_credentials`. Workload Anda melakukan autentikasi ke Okta (biasanya dengan `private_key_jwt`, sehingga tidak ada shared secret yang disimpan), menerima "JSON Web Token" (token web JSON), atau JWT, yang ditandatangani, dan menukarkan JWT tersebut dengan Anthropic untuk mendapatkan token akses berumur pendek.

URL issuer dari authorization server Okta berbentuk `https://<your-domain>.okta.com/oauth2/<auth-server-id>`. Jika Anda menggunakan server default bawaan, path-nya adalah `/oauth2/default`.

<Note>
  Anda harus menggunakan **custom authorization server** Okta (termasuk yang `default`). Token yang diterbitkan langsung oleh authorization server org Okta (endpoint `/oauth2/v1/token` tanpa ID authorization server di path) tidak dapat divalidasi oleh pihak eksternal karena Okta tidak mempublikasikan kunci penandatanganan untuk token tersebut.
</Note>

Ada banyak cara untuk mengonfigurasi dan melakukan autentikasi ke Okta yang berada di luar cakupan dokumentasi ini. Pastikan bahwa konfigurasi dan mekanisme autentikasi Anda mengikuti panduan dan praktik keamanan perusahaan Anda.

## Prasyarat

* Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Organisasi Okta dengan API Access Management yang diaktifkan (diperlukan untuk custom authorization server).
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.
* Workload yang dapat meminta token dari endpoint `/v1/token` Okta dan menjangkau `api.anthropic.com`.

## Mengonfigurasi Okta

Secara garis besar Anda perlu:

1. Membuat aplikasi layanan Okta.
2. Mengonfigurasi authorization server default Anda (atau membuat custom authorization server baru) dengan audience, scope, access policy, dan custom claim apa pun yang ingin Anda cocokkan.

Navigasi yang tepat bergantung pada konfigurasi org Okta Anda dan versi admin console. Langkah-langkah bernomor berikut memandu Anda melalui salah satu jalur yang umum:

1. **Buat integrasi service app.** Di Okta Admin Console, buat integrasi aplikasi baru dengan tipe **API Services** (OIDC, machine-to-machine). Catat **Client ID** yang dihasilkan.
2. **Konfigurasikan autentikasi klien.** Untuk pengaturan tanpa kunci rahasia, pilih **Public key / Private key** (`private_key_jwt`) dan daftarkan JWK publik workload Anda. Sebagai alternatif, gunakan client secret jika lingkungan Anda dapat menyimpannya dengan aman. Untuk contoh berikut Anda mungkin perlu menonaktifkan persyaratan DPoP pada aplikasi; pastikan bahwa pengaturan produksi Anda mematuhi persyaratan keamanan organisasi Anda.
3. **Tetapkan audience.** Pada custom authorization server Anda, tetapkan audience ke `https://api.anthropic.com` sehingga token akses yang diterbitkan membawa klaim `aud` tersebut. Anthropic memvalidasi `aud` terhadap nilai tetap ini.
4. **Berikan scope.** Pada custom authorization server Anda, pastikan setidaknya ada satu scope yang boleh diminta oleh service app (misalnya, `anthropic.access`). Okta menolak permintaan `client_credentials` yang tidak menyertakan scope yang telah diberikan.
5. **Buat access policy.** Pada custom authorization server Anda, buat access policy dengan setidaknya satu aturan yang mengizinkan service app Anda meminta scope yang Anda berikan pada langkah 4.
6. **(Opsional) Tambahkan custom claim.** Jika Anda ingin mencocokkan pada sesuatu selain client ID, tambahkan klaim ke token akses di tab **Claims** pada authorization server Anda.

Untuk service app yang menggunakan `client_credentials`, Okta menetapkan klaim `sub` dari token akses yang diterbitkan ke **Client ID** aplikasi, dan `iss` ke URL issuer dari authorization server.

## Mengonfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih **Custom OIDC**. Wizard akan memandu Anda melalui pendaftaran issuer, pembuatan service account, dan pembuatan federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Gunakan URL custom authorization server Okta Anda dan mode discovery. Anthropic membaca dokumen discovery `.well-known/openid-configuration` Okta dan mengambil JWKS dari `jwks_uri` yang diiklankannya.

```json
{
  "name": "okta-prod",
  "issuer_url": "https://acme.okta.com/oauth2/aus1a2b3c4d5e6f7g8h9",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Cocokkan pada klaim `sub` Okta, yang merupakan Client ID dari service app. Jika Anda mendefinisikan custom claim di Okta, Anda dapat mencocokkan pada klaim tersebut sebagai gantinya dengan map `claims` atau `condition` CEL.

```json
{
  "name": "okta-pipeline",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "0oa1b2c3d4e5f6g7h8i9",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

## Memperoleh token dan memanggil Claude API

Tidak seperti penyedia platform-native (AWS, Google Cloud, Kubernetes), yang menyediakan token di dalam runtime workload (melalui file yang diproyeksikan atau endpoint metadata lokal), Okta tidak melakukannya. Workload Anda harus memanggil endpoint token Okta untuk mendapatkan JWT, lalu meneruskan JWT tersebut ke Anthropic SDK sebagai token identitas.

<CodeGroup>
  ```bash cURL
  # 1. Minta token akses dari Okta (client_credentials dengan private_key_jwt).
  OKTA_JWT=$(curl -sS "https://acme.okta.com/oauth2/aus1a2b3c4d5e6f7g8h9/v1/token" \
    -d grant_type=client_credentials \
    -d scope=anthropic.access \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion="$SIGNED_CLIENT_ASSERTION" \
    | jq -r .access_token)

  # 2. Tukarkan JWT Okta dengan token akses Anthropic.
  ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON | jq -r .access_token
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$OKTA_JWT",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )

  # 3. Panggil Claude API.
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"model": "claude-opus-4-8", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello, Claude"}]}' \
    | jq -r '.content[0].text'
  ```

  ```python Python
  import os
  import httpx
  import anthropic
  from anthropic import WorkloadIdentityCredentials


  def fetch_okta_token() -> str:
      response = httpx.post(
          f"{os.environ['OKTA_ISSUER']}/v1/token",
          data={
              "grant_type": "client_credentials",
              "scope": "anthropic.access",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              # Bangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
              "client_assertion": build_signed_client_assertion(),
          },
      )
      response.raise_for_status()
      return response.json()["access_token"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_okta_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
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

  async function fetchOktaToken(): Promise<string> {
    const response = await fetch(`${process.env.OKTA_ISSUER}/v1/token`, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        scope: "anthropic.access",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        // Bangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
        client_assertion: buildSignedClientAssertion()
      })
    });
    const body = (await response.json()) as { access_token: string };
    return body.access_token;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchOktaToken,
      federationRuleId: process.env.ANTHROPIC_FEDERATION_RULE_ID!,
      organizationId: process.env.ANTHROPIC_ORGANIZATION_ID!,
      serviceAccountId: process.env.ANTHROPIC_SERVICE_ACCOUNT_ID,
      workspaceId: process.env.ANTHROPIC_WORKSPACE_ID,
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
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"net/http"
  	"net/url"
  	"os"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func fetchOktaToken(ctx context.Context) (string, error) {
  	form := url.Values{
  		"grant_type":            {"client_credentials"},
  		"scope":                 {"anthropic.access"},
  		"client_assertion_type": {"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"},
  		// Bangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
  		"client_assertion": {buildSignedClientAssertion()},
  	}
  	req, err := http.NewRequestWithContext(ctx, http.MethodPost,
  		os.Getenv("OKTA_ISSUER")+"/v1/token", strings.NewReader(form.Encode()))
  	if err != nil {
  		return "", err
  	}
  	req.Header.Set("content-type", "application/x-www-form-urlencoded")
  	resp, err := http.DefaultClient.Do(req)
  	if err != nil {
  		return "", err
  	}
  	defer resp.Body.Close()
  	var body struct {
  		AccessToken string `json:"access_token"`
  	}
  	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
  		return "", err
  	}
  	return body.AccessToken, nil
  }

  func main() {
  	client := anthropic.NewClient(
  		option.WithFederationTokenProvider(option.IdentityTokenFunc(fetchOktaToken), option.FederationOptions{
  			FederationRuleID: os.Getenv("ANTHROPIC_FEDERATION_RULE_ID"),
  			OrganizationID:   os.Getenv("ANTHROPIC_ORGANIZATION_ID"),
  			ServiceAccountID: os.Getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
  			WorkspaceID:      os.Getenv("ANTHROPIC_WORKSPACE_ID"),
  		}),
  	)
  	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content[0].Text)
  }
  ```

  ```java Java
  IdentityTokenProvider fetchOktaToken = () -> {
      try {
          var form = Map.of(
                          "grant_type", "client_credentials",
                          "scope", "anthropic.access",
                          "client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                          // Bangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
                          "client_assertion", buildSignedClientAssertion())
                  .entrySet().stream()
                  .map(entry -> entry.getKey() + "=" + URLEncoder.encode(entry.getValue(), UTF_8))
                  .collect(Collectors.joining("&"));
          var request = HttpRequest.newBuilder(URI.create(System.getenv("OKTA_ISSUER") + "/v1/token"))
                  .header("content-type", "application/x-www-form-urlencoded")
                  .POST(HttpRequest.BodyPublishers.ofString(form))
                  .build();
          var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
          return new ObjectMapper().readTree(response.body()).get("access_token").asText();
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  };

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  fetchOktaToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var credentials = new WorkloadIdentityCredentials(new WorkloadIdentityOptions
  {
      FederationRuleId = Environment.GetEnvironmentVariable("ANTHROPIC_FEDERATION_RULE_ID")!,
      OrganizationId = Environment.GetEnvironmentVariable("ANTHROPIC_ORGANIZATION_ID"),
      ServiceAccountId = Environment.GetEnvironmentVariable("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      WorkspaceId = Environment.GetEnvironmentVariable("ANTHROPIC_WORKSPACE_ID"),
      IdentityTokenProvider = new OktaTokenProvider(),
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

  class OktaTokenProvider : IIdentityTokenProvider
  {
      private static readonly HttpClient Http = new();

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          var form = new FormUrlEncodedContent(new Dictionary<string, string>
          {
              ["grant_type"] = "client_credentials",
              ["scope"] = "anthropic.access",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              // Membangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
              ["client_assertion"] = BuildSignedClientAssertion(),
          });
          var response = await Http.PostAsync(
              $"{Environment.GetEnvironmentVariable("OKTA_ISSUER")}/v1/token", form, ct);
          response.EnsureSuccessStatusCode();
          using var json = await JsonDocument.ParseAsync(
              await response.Content.ReadAsStreamAsync(ct), default, ct);
          return json.RootElement.GetProperty("access_token").GetString()!;
      }
  }
  ```

  ```bash CLI
  # 1. Minta token akses dari Okta dan tulis ke file sementara.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS "$OKTA_ISSUER/v1/token" \
    -d grant_type=client_credentials \
    -d scope=anthropic.access \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion="$SIGNED_CLIENT_ASSERTION" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # 2. Panggil Claude API. CLI membaca ANTHROPIC_FEDERATION_RULE_ID,
  # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan
  # ANTHROPIC_IDENTITY_TOKEN_FILE lalu melakukan pertukaran.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  function fetchOktaToken(): string
  {
      $ch = curl_init(getenv('OKTA_ISSUER') . '/v1/token');
      curl_setopt_array($ch, [
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_POSTFIELDS => http_build_query([
              'grant_type' => 'client_credentials',
              'scope' => 'anthropic.access',
              'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
              // Bangun JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
              'client_assertion' => buildSignedClientAssertion(),
          ]),
      ]);
      $body = json_decode(curl_exec($ch), true);
      curl_close($ch);
      return $body['access_token'];
  }

  $client = new Client(
      credentials: new WorkloadIdentityCredentials(
          identityTokenProvider: fetchOktaToken(...),
          federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
          organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
          serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
          workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
      ),
  );

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "json"
  require "net/http"

  def fetch_okta_token
    uri = URI("#{ENV.fetch('OKTA_ISSUER')}/v1/token")
    response = Net::HTTP.post_form(
      uri,
      "grant_type" => "client_credentials",
      "scope" => "anthropic.access",
      "client_assertion_type" => "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      # Buat JWT client_assertion RFC 7523 yang ditandatangani dengan kunci privat aplikasi Okta Anda
      "client_assertion" => build_signed_client_assertion
    )
    JSON.parse(response.body).fetch("access_token")
  end

  client = Anthropic::Client.new(
    credentials: Anthropic::WorkloadIdentityCredentials.new(
      identity_token_provider: -> { fetch_okta_token },
      federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
      organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
      service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
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

Setiap tab SDK menunjukkan pola callable: Anthropic SDK memanggil penyedia token identitas Anda lagi setiap kali token akses Anthropic mendekati kedaluwarsa, sehingga fetcher Okta Anda harus mengembalikan token baru pada setiap panggilan alih-alih menyimpan satu token dalam cache tanpa batas waktu. CLI `ant` membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pertukaran, jadi segarkan file tersebut dengan timer untuk shell yang berjalan lama.

## Memverifikasi pengaturan

Pertukaran yang berhasil mengembalikan `access_token` yang dimulai dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum di sisi Okta adalah ketidakcocokan `issuer_url` (harus menyertakan path `/oauth2/<auth-server-id>`; authorization server org Okta tidak dapat digunakan).

## Membatasi cakupan rule Anda

<Warning>
  Beberapa service app di bawah authorization server Okta yang sama berbagi issuer yang sama. Rule yang menghilangkan `subject_prefix` akan cocok dengan setiap service app pada server tersebut, sehingga tim mana pun yang dapat mendaftarkan satu service app dapat memperoleh token Anthropic terfederasi.
</Warning>

Kunci blok `match` pada rule ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Tetapkan Client ID yang tepat:** Atur `subject_prefix` ke Client ID lengkap dari service app tanpa `*` di akhir.
* **Tetapkan audience:** Cocokkan nilai `audience` yang Anda konfigurasikan pada authorization server sehingga token yang dibuat untuk audience yang berbeda akan ditolak.
* **Cocokkan pada custom claim:** Untuk pembatasan cakupan yang lebih terperinci, tambahkan klaim di tab **Claims** pada authorization server dan cocokkan dengan map `claims` pada rule atau `condition` CEL.
* **Gunakan satu rule per service app:** Buat federation rule terpisah untuk setiap service app alih-alih berbagi satu rule di antara beberapa aplikasi.

## Langkah selanjutnya

* Tinjau [referensi WIF](/docs/id/manage-claude/wif-reference) untuk urutan resolusi kredensial lengkap dan konfigurasi profil.
* Lihat [referensi WIF](/docs/id/manage-claude/wif-reference#rule-matching-semantics) untuk mencocokkan pada custom claim Okta dengan ekspresi CEL.
