---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/azure
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 017ded6192b22af4d0fd76ab8220faece0985a837480b3789059b55b923e2e91
---

# Menggunakan WIF dengan Microsoft Entra ID

Federasikan managed identity Azure dan Entra Workload Identity dengan Claude API sehingga workload Azure Anda dapat memanggil Claude tanpa kunci API statis.

---

Workload Azure melakukan autentikasi ke Claude API dengan menyajikan JSON Web Token (JWT) yang diterbitkan oleh Microsoft Entra ID, lalu menukarnya dengan token akses Anthropic berumur pendek. Penyiapannya mengikuti bentuk yang sama di setiap platform Azure:

1. **Daftarkan audiens token:** Buat satu app registration di tenant Microsoft Entra Anda untuk merepresentasikan audiens Claude API. Setiap workload di tenant meminta token Entra untuknya.
2. **Siapkan identitas untuk platform Anda:** Managed identity pada VM, VM Scale Set, App Service, Functions, dan Container Apps, atau Entra Workload Identity pada AKS.
3. **Konfigurasikan Anthropic:** Daftarkan issuer Entra tenant Anda, buat service account, dan tulis aturan federasi yang cocok dengan klaim token.
4. **Tukar saat runtime:** Workload Anda menukar token yang diterbitkan Entra di `POST /v1/oauth/token` dengan token akses Anthropic `sk-ant-oat01-...` dan memanggil Claude dengannya.

Pada kedua jalur tersebut, token yang Anda sajikan ke Anthropic membawa issuer Entra spesifik tenant Anda dan object ID managed identity dalam klaim `sub` dan `oid`; yang berbeda hanyalah cara workload memperoleh token tersebut. Pilih bagian sesuai tempat workload Anda berjalan: [Menggunakan managed identity](#use-a-managed-identity) untuk VM, VM Scale Set, App Service, Functions, atau Container Apps; [Menggunakan Entra Workload Identity pada AKS](#use-entra-workload-identity-on-aks) untuk AKS.

## Prasyarat

* Keakraban dengan [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Langganan Azure dengan izin untuk menetapkan managed identity (atau mengonfigurasi Entra Workload Identity pada AKS).
* Izin untuk membuat satu app registration dan service principal di tenant Microsoft Entra Anda (audiens Claude API bersama). Entra hanya menerbitkan token untuk audiens yang ada di tenant, sehingga langkah [Daftarkan audiens token](#register-the-token-audience) diperlukan sebelum permintaan token apa pun berhasil.
* ID tenant Microsoft Entra Anda. Temukan di portal Azure di bawah **Microsoft Entra ID → Overview → Tenant ID**.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

## Daftarkan audiens token

Microsoft Entra ID hanya menerbitkan token ketika audiens yang diminta ada di tenant Anda sebagai app registration dengan service principal. Buat satu app registration untuk merepresentasikan audiens Claude API; setiap workload di tenant dapat meminta token untuknya. Tanpa registrasi ini, permintaan token gagal dengan kesalahan "resource not found in tenant" (`AADSTS50001` dari endpoint managed identity, `AADSTS500011` dari endpoint token Entra).

```bash
# Buat pendaftaran aplikasi yang merepresentasikan audiens Claude API.
APP_ID=$(az ad app create --display-name claude-api-federation --query appId -o tsv)

# Minta token akses v2.0 dan atur URI pengenal api://<APP_ID>.
az ad app update --id "$APP_ID" \
  --identifier-uris "api://$APP_ID" \
  --set api.requestedAccessTokenVersion=2

# Buat service principal agar audiens dapat di-resolve di tenant Anda.
az ad sp create --id "$APP_ID"
```

<Note>
  Gunakan format identifier URI `api://<APP_ID>`. Entra membatasi identifier URI `https://` hanya untuk domain terverifikasi dari tenant Anda sendiri, sehingga URI seperti `https://api.anthropic.com` tidak dapat didaftarkan di sebagian besar tenant; `api://<APP_ID>` diterima di mana saja. Dengan `requestedAccessTokenVersion: 2`, token untuk audiens ini adalah v2.0, yang merupakan asumsi panduan ini. Jika Anda menggunakan kembali registrasi yang sudah ada yang mengeluarkan token v1.0, lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0).
</Note>

## Menggunakan managed identity

Gunakan jalur ini ketika workload Anda berjalan pada VM, VM Scale Set, App Service, Functions, atau Container Apps. Workload meminta JWT yang diterbitkan Entra untuk managed identity yang ditetapkan padanya dari endpoint token lokal platform, lalu menukar JWT tersebut dengan Anthropic.

### Konfigurasikan managed identity

<Steps>
  <Step title="Lampirkan managed identity">
    Aktifkan managed identity yang ditetapkan sistem (system-assigned) atau ditetapkan pengguna (user-assigned) pada sumber daya Azure Anda. Di portal Azure, buka sumber daya tersebut, masuk ke **Identity**, dan aktifkan **System assigned** (atau lampirkan identitas yang ditetapkan pengguna).

    Setelah identitas dibuat, catat **Object (principal) ID**-nya. GUID ini muncul sebagai klaim `sub` dan `oid` dalam token yang diterbitkan, dan federation rule Anthropic Anda akan mencocokkannya. Anda dapat menemukannya di halaman **Identity** sumber daya; untuk identitas yang ditetapkan pengguna, itu adalah **Object (principal) ID** pada halaman **Overview** sumber daya managed identity. (Managed identity hanya memiliki service principal di Microsoft Entra ID, bukan app registration.)
  </Step>

  <Step title="Temukan endpoint token platform">
    Platform mengekspos endpoint token lokal setelah identitas dilampirkan:

    * **VM dan VM Scale Set:** IMDS di `http://169.254.169.254/metadata/identity/oauth2/token` dengan header `Metadata: true` dan `api-version=2018-02-01`.
    * **App Service, Functions, dan Container Apps:** URL dalam variabel lingkungan `IDENTITY_ENDPOINT` dengan header `X-IDENTITY-HEADER` yang diatur ke nilai `IDENTITY_HEADER`, dan `api-version=2019-08-01`. IMDS tidak dapat dijangkau pada platform ini.

    Jika sumber daya memiliki lebih dari satu managed identity yang ditetapkan pengguna, tambahkan `client_id=<IDENTITY_CLIENT_ID>` ke permintaan token untuk memilih salah satunya. Azure merekomendasikan untuk selalu menentukannya. Tanpa itu, hasilnya bergantung pada apakah sumber daya juga memiliki identitas yang ditetapkan sistem yang diaktifkan: jika ya, permintaan secara diam-diam beralih ke identitas tersebut dan kemudian gagal pada pencocokan `oid` federation rule Anda; jika tidak, permintaan langsung gagal begitu identitas yang ditetapkan pengguna kedua dilampirkan.
  </Step>

  <Step title="Dekode token sampel">
    Minta token dari endpoint dan dekode payload-nya untuk mengonfirmasi klaim yang perlu dicocokkan oleh federation rule Anda. (Untuk perintah dekode, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange).) Token v2.0 untuk managed identity membawa klaim berikut:

    ```json
    {
      "iss": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
      "sub": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "aud": "<APP_ID>",
      "oid": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "tid": "<TENANT_ID>",
      "azp": "<IDENTITY_CLIENT_ID>",
      "ver": "2.0",
      "exp": 1775527120
    }
    ```

    | Klaim | Nilai                                                                                                             | Cocokkan ini ketika                                                                                                                                                     |
    | ----- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `oid` | Object ID managed identity, identik dengan `sub`                                                                  | Anda ingin mengotorisasi satu managed identity tertentu. Ini adalah default; aturan di [Konfigurasikan Anthropic](#configure-anthropic) mencocokkannya.                 |
    | `azp` | Client ID identitas pemanggil                                                                                     | Anda ingin mengotorisasi setiap workload yang berbagi satu app registration. Untuk managed identity, `azp` unik untuk identitas tersebut, sehingga setara dengan `oid`. |
    | `aud` | Client ID app registration audiens (GUID `<APP_ID>` dari [Daftarkan audiens token](#register-the-token-audience)) | Selalu. Bidang `audience` aturan harus sama persis dengan nilai `aud` token.                                                                                            |
    | `tid` | ID tenant Anda                                                                                                    | Anda menginginkan pertahanan berlapis. URL issuer sudah mengunci tenant.                                                                                                |

    Jika klaim `ver` token yang didekode adalah `1.0`, nama dan nilai klaimnya berbeda. Lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0) sebelum melanjutkan.
  </Step>
</Steps>

### Konfigurasikan Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih ubin **Microsoft Entra**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Pilih **v2.0 (login.microsoftonline.com)** di pemilih **Token issuer** pada wizard. (Pemilih ini default ke v1; default tersebut ada untuk tenant yang menggunakan kembali registrasi lama yang masih mengeluarkan token v1.0.) Entra menerbitkan dokumen discovery OIDC di URL issuer per-tenant, jadi gunakan mode discovery. Setiap tenant Microsoft Entra yang Anda federasikan memerlukan catatan issuer-nya sendiri.

```json
{
  "name": "azure-prod-tenant",
  "issuer_url": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
  "jwks": { "type": "discovery" },
  "max_jwt_lifetime_seconds": 86400
}
```

<Warning>
  Workload managed identity memerlukan `max_jwt_lifetime_seconds: 86400`. Azure menerbitkan token managed identity dengan hingga 24 jam antara `iat` dan `exp` karena Azure menyimpan cache token setiap sumber daya untuk jendela waktu tersebut dan tidak menawarkan cara untuk memaksa penyegaran lebih awal, dan default 1 jam pada issuer menolak token tersebut dengan `invalid_grant`. Ubin Microsoft Entra pada wizard Connect workload membuat issuer dengan `max_jwt_lifetime_seconds` diatur ke `7500` dan tidak menyediakan bidang untuk mengubahnya selama pembuatan, jadi selesaikan wizard, lalu buka **Settings → Workload identity → Issuers**, edit issuer, dan naikkan nilainya ke `86400`. Anda juga dapat memperbarui issuer melalui Admin API.
</Warning>

Masa berlaku yang diterima lebih lama berarti token Entra yang bocor tetap dapat ditukar lebih lama. Jika token bocor, tuasnya adalah menonaktifkan federation rule; pencocokan `oid` yang ketat membatasi identitas mana yang dapat menukar token sejak awal, seperti dijelaskan di [Batasi cakupan aturan Anda](#scope-your-rule).

**Federation rule:** Cocokkan pada object ID managed identity dan ID tenant Anda. Untuk token v2.0 yang dikonfigurasi panduan ini, nilai `audience` adalah client ID app registration audiens (GUID `<APP_ID>` dari [Daftarkan audiens token](#register-the-token-audience)). Gunakan nilai `aud` yang persis dari token yang Anda dekode.

```json
{
  "name": "azure-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "audience": "<APP_ID>",
    "claims": {
      "oid": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "tid": "<TENANT_ID>"
    }
  },
  "target": {
    "type": "service_account",
    "service_account_id": "svac_..."
  },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

`token_lifetime_seconds` adalah masa berlaku token akses Anthropic yang dikembalikan oleh pertukaran, bukan masa berlaku token Entra; SDK menyegarkannya untuk Anda.

### Dapatkan dan gunakan token

Saat runtime, workload Anda mengambil token Entra-nya, menukarnya di `POST /v1/oauth/token`, dan menggunakan bearer token yang dikembalikan untuk memanggil Claude. Setiap SDK Anthropic menangani pertukaran dan loop penyegaran ketika Anda menyediakan callable penyedia token, seperti ditunjukkan dalam contoh berikut. Tab cURL menunjukkan alur mentahnya.

Sampel mengambil token managed identity dari endpoint token platform: IMDS pada VM dan VM Scale Set, atau layanan `IDENTITY_ENDPOINT` pada App Service, Functions, dan Container Apps. Ganti `<APP_ID>` dalam nilai resource `api://<APP_ID>` dengan client ID app registration audiens dari [Daftarkan audiens token](#register-the-token-audience).

<Tip>
  Jika workload Anda sudah menggunakan pustaka klien Azure Identity, berikan akuisisi tokennya (`DefaultAzureCredential` dengan scope `api://<APP_ID>/.default`) sebagai penyedia token identitas alih-alih memanggil endpoint token secara langsung. Pustaka tersebut memilih endpoint yang benar di setiap platform Azure, termasuk AKS dengan Entra Workload Identity.
</Tip>

<CodeGroup>
  ```bash cURL
  # 1. Ambil token yang diterbitkan Entra (managed identity).
  #    Pada VM atau VM Scale Set, gunakan IMDS. Dengan beberapa identitas
  #    user-assigned, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  ENTRA_TOKEN=$(curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=api://<APP_ID>" \
    | jq -r .access_token)

  #    Pada App Service, Functions, atau Container Apps, gunakan layanan token
  #    lokal sebagai gantinya (IMDS tidak dapat dijangkau di sana):
  # ENTRA_TOKEN=$(curl -sS -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" \
  #   "$IDENTITY_ENDPOINT?api-version=2019-08-01&resource=api://<APP_ID>" \
  #   | jq -r .access_token)

  #    Untuk AKS dengan Entra Workload Identity, gunakan pertukaran dua tahap
  #    pada bagian "Use Entra Workload Identity on AKS" sebagai gantinya.

  # 2. Tukarkan token tersebut dengan token akses Anthropic.
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$ENTRA_TOKEN",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )

  ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r .access_token)

  # 3. Panggil Claude API dengan bearer token tersebut.
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from Azure"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  import requests
  from anthropic import WorkloadIdentityCredentials

  # URI pengenal dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  AUDIENCE = "api://<APP_ID>"


  def fetch_entra_token() -> str:
      """Fetch a managed identity token from the platform's token endpoint."""
      # Dengan beberapa identitas yang ditetapkan pengguna, tambahkan client_id=<IDENTITY_CLIENT_ID>
      # ke parameter permintaan untuk memilih salah satunya.
      if endpoint := os.environ.get("IDENTITY_ENDPOINT"):
          # App Service, Functions, Container Apps
          response = requests.get(
              endpoint,
              headers={"X-IDENTITY-HEADER": os.environ["IDENTITY_HEADER"]},
              params={"api-version": "2019-08-01", "resource": AUDIENCE},
              timeout=5,
          )
      else:
          # VM atau VM Scale Set: Azure Instance Metadata Service (IMDS)
          response = requests.get(
              "http://169.254.169.254/metadata/identity/oauth2/token",
              headers={"Metadata": "true"},
              params={"api-version": "2018-02-01", "resource": AUDIENCE},
              timeout=5,
          )
      response.raise_for_status()
      return response.json()["access_token"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_entra_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from Azure"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";

  // URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  const AUDIENCE = "api://<APP_ID>";

  async function fetchEntraToken(): Promise<string> {
    // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
    // VM dan VM Scale Set menggunakan IMDS.
    // Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
    const identityEndpoint = process.env.IDENTITY_ENDPOINT;
    const url = identityEndpoint
      ? `${identityEndpoint}?api-version=2019-08-01&resource=${AUDIENCE}`
      : `http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=${AUDIENCE}`;
    const headers: Record<string, string> = identityEndpoint
      ? { "X-IDENTITY-HEADER": process.env.IDENTITY_HEADER! }
      : { Metadata: "true" };
    const response = await fetch(url, { headers });
    const body = (await response.json()) as { access_token: string };
    return body.access_token;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchEntraToken,
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
    messages: [{ role: "user", content: "Hello from Azure" }]
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
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  // URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  const audience = "api://<APP_ID>"

  // fetchEntraToken mengambil token managed identity dari endpoint token
  // platform: IMDS pada VM dan VM Scale Set, atau layanan IDENTITY_ENDPOINT
  // pada App Service, Functions, dan Container Apps.
  func fetchEntraToken(ctx context.Context) (string, error) {
  	// Jika ada beberapa user-assigned identity, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  	tokenURL := "http://169.254.169.254/metadata/identity/oauth2/token" +
  		"?api-version=2018-02-01&resource=" + audience
  	header, value := "Metadata", "true"
  	if endpoint := os.Getenv("IDENTITY_ENDPOINT"); endpoint != "" {
  		tokenURL = endpoint + "?api-version=2019-08-01&resource=" + audience
  		header, value = "X-IDENTITY-HEADER", os.Getenv("IDENTITY_HEADER")
  	}
  	req, err := http.NewRequestWithContext(ctx, http.MethodGet, tokenURL, nil)
  	if err != nil {
  		return "", err
  	}
  	req.Header.Set(header, value)
  	resp, err := http.DefaultClient.Do(req)
  	if err != nil {
  		return "", fmt.Errorf("call token endpoint: %w", err)
  	}
  	defer resp.Body.Close()
  	var body struct {
  		AccessToken string `json:"access_token"`
  	}
  	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
  		return "", fmt.Errorf("decode token response: %w", err)
  	}
  	return body.AccessToken, nil
  }

  func main() {
  	client := anthropic.NewClient(
  		option.WithFederationTokenProvider(fetchEntraToken, option.FederationOptions{
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
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from Azure")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content[0].Text)
  }
  ```

  ```java Java
  HttpClient http = HttpClient.newHttpClient();
  // URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  String audience = "api://<APP_ID>";
  // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
  // VM dan VM Scale Set menggunakan IMDS.
  // Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  String identityEndpoint = System.getenv("IDENTITY_ENDPOINT");
  HttpRequest tokenRequest = identityEndpoint != null
          ? HttpRequest.newBuilder(URI.create(identityEndpoint + "?api-version=2019-08-01&resource=" + audience))
                  .header("X-IDENTITY-HEADER", System.getenv("IDENTITY_HEADER"))
                  .build()
          : HttpRequest.newBuilder(URI.create("http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=" + audience))
                  .header("Metadata", "true")
                  .build();

  IdentityTokenProvider fetchEntraToken = () -> {
      try {
          var response = http.send(tokenRequest, HttpResponse.BodyHandlers.ofString());
          return new ObjectMapper().readTree(response.body()).get("access_token").asText();
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  };

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  fetchEntraToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
                  System.getenv("ANTHROPIC_WORKSPACE_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Hello from Azure")
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
      IdentityTokenProvider = new EntraTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from Azure" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class EntraTokenProvider : IIdentityTokenProvider
  {
      // URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
      private const string Audience = "api://<APP_ID>";

      private static readonly HttpClient httpClient = new();

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
          // VM dan VM Scale Set menggunakan IMDS.
          // Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
          var identityEndpoint = Environment.GetEnvironmentVariable("IDENTITY_ENDPOINT");
          using var request = identityEndpoint is not null
              ? new HttpRequestMessage(HttpMethod.Get,
                  $"{identityEndpoint}?api-version=2019-08-01&resource={Audience}")
              {
                  Headers = { { "X-IDENTITY-HEADER", Environment.GetEnvironmentVariable("IDENTITY_HEADER") } },
              }
              : new HttpRequestMessage(HttpMethod.Get,
                  $"http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource={Audience}")
              {
                  Headers = { { "Metadata", "true" } },
              };
          using var response = await httpClient.SendAsync(request, ct);
          response.EnsureSuccessStatusCode();
          using var json = await JsonDocument.ParseAsync(
              await response.Content.ReadAsStreamAsync(ct), default, ct);
          return json.RootElement.GetProperty("access_token").GetString()!;
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  // URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  const AUDIENCE = 'api://<APP_ID>';

  function fetchEntraToken(): string
  {
      // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
      // VM dan VM Scale Set menggunakan IMDS.
      // Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
      $identityEndpoint = getenv('IDENTITY_ENDPOINT');
      if ($identityEndpoint !== false) {
          $url = $identityEndpoint . '?api-version=2019-08-01&resource=' . AUDIENCE;
          $header = 'X-IDENTITY-HEADER: ' . getenv('IDENTITY_HEADER');
      } else {
          $url = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=' . AUDIENCE;
          $header = 'Metadata: true';
      }
      $context = stream_context_create([
          'http' => ['header' => $header . "\r\n"],
      ]);
      $body = json_decode(file_get_contents($url, false, $context), true);
      return $body['access_token'];
  }

  $credentials = new WorkloadIdentityCredentials(
      identityTokenProvider: fetchEntraToken(...),
      federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
      organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
      serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
      workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
  );
  $client = new Client(credentials: $credentials);

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from Azure']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "json"
  require "net/http"

  # URI pengidentifikasi dari registrasi aplikasi audiens (lihat Mendaftarkan audiens token).
  AUDIENCE = "api://<APP_ID>"

  def fetch_entra_token
    # App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
    # VM dan VM Scale Set menggunakan IMDS.
    # Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
    if (endpoint = ENV["IDENTITY_ENDPOINT"])
      url = "#{endpoint}?api-version=2019-08-01&resource=#{AUDIENCE}"
      headers = {"X-IDENTITY-HEADER" => ENV.fetch("IDENTITY_HEADER")}
    else
      url = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=#{AUDIENCE}"
      headers = {"Metadata" => "true"}
    end
    response = Net::HTTP.get(URI(url), headers)
    JSON.parse(response).fetch("access_token")
  end

  credentials = Anthropic::WorkloadIdentityCredentials.new(
    identity_token_provider: -> { fetch_entra_token },
    federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
    organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
    service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
    workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
  )
  client = Anthropic::Client.new(credentials: credentials)

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Azure"}]
  )
  puts message.content.first.text
  ```

  ```bash CLI
  # Tulis token akses yang diterbitkan Entra ke file yang dapat dibaca oleh CLI.
  # Ditampilkan untuk VM atau VM Scale Set (IMDS). Pada App Service, Functions, atau
  # Container Apps, ambil dari "$IDENTITY_ENDPOINT?api-version=2019-08-01&resource=api://<APP_ID>"
  # dengan -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" sebagai gantinya.
  # Dengan beberapa identitas yang ditetapkan pengguna, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  trap 'rm -f "$ANTHROPIC_IDENTITY_TOKEN_FILE"' EXIT
  curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=api://<APP_ID>" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca dari environment.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Azure"}'
  ```
</CodeGroup>

### Verifikasi penyiapan

Dari sumber daya Azure Anda, jalankan pertukaran cURL yang ditunjukkan di [Dapatkan dan gunakan token](#acquire-and-use-the-token) dan konfirmasikan bahwa `POST /v1/oauth/token` mengembalikan `200` dengan `access_token` yang dimulai dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, dekode token Entra (lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange) untuk perintahnya) dan periksa penyebab paling umum di sisi Azure:

* **Ketidakcocokan issuer:** `issuer_url` yang terdaftar harus sama persis dengan klaim `iss` token. Token v2.0 membawa `https://login.microsoftonline.com/<TENANT_ID>/v2.0`; jika klaim `ver` yang didekode adalah `1.0`, lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0).
* **Masa berlaku token:** Token managed identity membawa hingga 24 jam antara `iat` dan `exp`. Jika issuer masih memiliki nilai `7500` dari wizard (atau default 1 jam), naikkan `max_jwt_lifetime_seconds` ke `86400` seperti dijelaskan di [Konfigurasikan Anthropic](#configure-anthropic).
* **Ketidakcocokan audiens:** `audience` aturan harus sama persis dengan `aud` token: client ID app registration audiens untuk token v2.0 yang dikonfigurasi panduan ini.
* **Ketidakcocokan nama klaim:** Aturan yang mencocokkan klaim yang tidak dibawa token tidak akan pernah lolos. Token v1.0 membawa client ID dalam `appid`, bukan `azp`; lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0).

## Menggunakan Entra Workload Identity pada AKS

Gunakan jalur ini ketika workload Anda berjalan dalam pod AKS. Entra Workload Identity memfederasikan service account Kubernetes dengan managed identity yang ditetapkan pengguna: Kubernetes memproyeksikan token service account (ditandatangani oleh issuer OIDC klaster AKS) ke dalam pod pada path di `AZURE_FEDERATED_TOKEN_FILE`. Token yang diproyeksikan tersebut bukan token yang diterbitkan Entra, jadi untuk tetap berada di jalur yang dimediasi Entra yang dijelaskan di halaman ini, workload melakukan pertukaran dua langkah: pertama menukarkan token yang diproyeksikan di `https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token` (grant `client_credentials` terfederasi) dengan token akses yang diterbitkan Entra, lalu meneruskan token Entra tersebut ke SDK Anthropic sebagai token identitas.

<Tip>
  Pod AKS dapat secara alternatif melewati pertukaran Entra dan menyajikan token service account yang diproyeksikan Kubernetes langsung ke Anthropic. Jalur tersebut mendaftarkan issuer OIDC klaster AKS Anda ke Anthropic alih-alih tenant Entra Anda. Lihat [Menggunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk alur tersebut.
</Tip>

### Konfigurasikan Entra Workload Identity

<Steps>
  <Step title="Aktifkan issuer OIDC dan workload identity pada klaster Anda">
    Mengaktifkan workload identity akan menginstal mutating webhook `azure-workload-identity` untuk Anda; deploy secara manual hanya pada klaster non-AKS. Catat URL issuer OIDC klaster untuk federated credential yang Anda buat di langkah berikutnya.

    ```bash
    az aks update \
      --resource-group <RESOURCE_GROUP> \
      --name <CLUSTER_NAME> \
      --enable-oidc-issuer \
      --enable-workload-identity

    AKS_OIDC_ISSUER=$(az aks show \
      --resource-group <RESOURCE_GROUP> \
      --name <CLUSTER_NAME> \
      --query oidcIssuerProfile.issuerUrl -o tsv)
    ```
  </Step>

  <Step title="Buat managed identity yang ditetapkan pengguna">
    Catat dua nilai dari identitas tersebut: **Client ID** masuk ke anotasi service account (dan disuntikkan ke dalam pod sebagai `AZURE_CLIENT_ID`), dan **Object (principal) ID** muncul sebagai klaim `oid` yang dicocokkan oleh federation rule Anthropic Anda.

    ```bash
    az identity create \
      --resource-group <RESOURCE_GROUP> \
      --name claude-inference-identity \
      --location <LOCATION>

    # Masuk ke anotasi service account; diinjeksikan ke dalam pod sebagai AZURE_CLIENT_ID.
    IDENTITY_CLIENT_ID=$(az identity show \
      --resource-group <RESOURCE_GROUP> \
      --name claude-inference-identity \
      --query clientId -o tsv)

    # Muncul sebagai klaim oid yang dicocokkan oleh aturan federasi Anda.
    IDENTITY_OBJECT_ID=$(az identity show \
      --resource-group <RESOURCE_GROUP> \
      --name claude-inference-identity \
      --query principalId -o tsv)
    ```
  </Step>

  <Step title="Buat service account Kubernetes yang dianotasi">
    Webhook `azure-workload-identity` membaca anotasi `azure.workload.identity/client-id` untuk menyuntikkan `AZURE_CLIENT_ID` ke dalam pod, yang dibaca dari lingkungan oleh sampel di [Dapatkan dan gunakan token](#acquire-and-use-the-token-2).

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: claude-inference
      namespace: inference
      annotations:
        azure.workload.identity/client-id: <IDENTITY_CLIENT_ID>
    ```
  </Step>

  <Step title="Buat federated credential pada managed identity">
    Federated credential mempercayai issuer OIDC klaster Anda untuk service account spesifik tersebut. Nilai `--audience api://AzureADTokenExchange` adalah audiens tetap Entra untuk token service account Kubernetes yang masuk; nilai ini tidak terkait dengan audiens Claude API yang Anda daftarkan sebelumnya.

    ```bash
    az identity federated-credential create \
      --resource-group <RESOURCE_GROUP> \
      --identity-name claude-inference-identity \
      --name claude-inference-aks \
      --issuer "$AKS_OIDC_ISSUER" \
      --subject system:serviceaccount:inference:claude-inference \
      --audience api://AzureADTokenExchange
    ```
  </Step>

  <Step title="Beri label pada pod dan atur service account-nya">
    Pod harus membawa label `azure.workload.identity/use: "true"` dan berjalan sebagai service account yang dianotasi. Webhook kemudian menyuntikkan `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID`, dan `AZURE_TENANT_ID` ke dalam pod. File di `AZURE_FEDERATED_TOKEN_FILE` berisi token service account yang diproyeksikan Kubernetes, ditandatangani oleh issuer OIDC klaster AKS.

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: inference-worker
      namespace: inference
      labels:
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: claude-inference
      containers:
        - name: app
          image: your-registry/inference-worker:latest
    ```
  </Step>

  <Step title="Dekode token sampel">
    Token yang dilihat oleh federation rule Anthropic Anda bukanlah file yang diproyeksikan; melainkan token yang diterbitkan Entra yang dikembalikan oleh pertukaran `client_credentials`. Dari dalam pod yang berlabel, jalankan langkah 1 dari sampel cURL di [Dapatkan dan gunakan token](#acquire-and-use-the-token-2) dan dekode hasilnya. Token ini membawa bentuk klaim yang sama dengan jalur managed identity:

    ```json
    {
      "iss": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
      "sub": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "aud": "<APP_ID>",
      "oid": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "tid": "<TENANT_ID>",
      "azp": "<IDENTITY_CLIENT_ID>",
      "ver": "2.0",
      "exp": 1775527120
    }
    ```

    `sub` dan `oid` adalah object ID managed identity, `aud` adalah client ID app registration audiens, dan `azp` adalah client ID managed identity (nilai dari `AZURE_CLIENT_ID`). Masa berlakunya berbeda dari jalur managed identity: token `client_credentials` secara default memiliki jendela acak 60 hingga 90 menit antara `iat` dan `exp`, bukan 24 jam.
  </Step>
</Steps>

### Konfigurasikan Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih ubin **Microsoft Entra**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Pilih **v2.0 (login.microsoftonline.com)** di pemilih **Token issuer** pada wizard. (Pemilih ini default ke v1; default tersebut ada untuk tenant yang menggunakan kembali registrasi lama yang masih mengeluarkan token v1.0.) Entra menerbitkan dokumen discovery OIDC di URL issuer per-tenant, jadi gunakan mode discovery. Setiap tenant Microsoft Entra yang Anda federasikan memerlukan catatan issuer-nya sendiri.

```json
{
  "name": "azure-prod-tenant",
  "issuer_url": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
  "jwks": { "type": "discovery" },
  "max_jwt_lifetime_seconds": 7500
}
```

<Warning>
  Ubin Microsoft Entra pada wizard Connect workload membuat issuer dengan `max_jwt_lifetime_seconds` diatur ke `7500` (sedikit lebih dari 2 jam), yang mencakup masa berlaku default 60 hingga 90 menit dari token `client_credentials`. Kebijakan masa berlaku token tenant atau Continuous Access Evaluation (CAE) dapat memperpanjang masa berlaku tersebut. Jika `exp` dikurangi `iat` pada token yang Anda dekode melebihi 7500 detik, edit issuer di **Settings → Workload identity → Issuers** dan naikkan `max_jwt_lifetime_seconds` agar sesuai, atau pertukaran akan gagal dengan `invalid_grant`. Jika tenant Anda juga menjalankan workload managed identity dari [Menggunakan managed identity](#use-a-managed-identity), gunakan nilai `86400` dari bagian tersebut, yang mencakup kedua jalur.
</Warning>

Masa berlaku yang diterima lebih lama berarti token Entra yang bocor tetap dapat ditukar lebih lama. Jika token bocor, tuasnya adalah menonaktifkan federation rule; pencocokan `oid` yang ketat membatasi identitas mana yang dapat menukar token sejak awal, seperti dijelaskan di [Batasi cakupan aturan Anda](#scope-your-rule).

**Federation rule:** Cocokkan pada object ID managed identity dan ID tenant Anda. Untuk token v2.0 yang dikonfigurasi panduan ini, nilai `audience` adalah client ID app registration audiens (GUID `<APP_ID>` dari [Daftarkan audiens token](#register-the-token-audience)). Gunakan nilai `aud` yang persis dari token yang Anda dekode.

```json
{
  "name": "azure-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "audience": "<APP_ID>",
    "claims": {
      "oid": "9f8e7d6c-1a2b-3c4d-5e6f-...",
      "tid": "<TENANT_ID>"
    }
  },
  "target": {
    "type": "service_account",
    "service_account_id": "svac_..."
  },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

`token_lifetime_seconds` adalah masa berlaku token akses Anthropic yang dikembalikan oleh pertukaran, bukan masa berlaku token Entra; SDK menyegarkannya untuk Anda.

### Dapatkan dan gunakan token

Saat runtime, pod melakukan pertukaran dua langkah: pod mengirim token yang diproyeksikan Kubernetes (file di `AZURE_FEDERATED_TOKEN_FILE`) ke endpoint token Entra sebagai assertion `client_credentials` terfederasi, lalu menukar token akses Entra yang dihasilkan di `POST /v1/oauth/token`. Setiap SDK Anthropic menangani pertukaran kedua dan loop penyegaran ketika Anda menyediakan pengambilan Entra sebagai callable penyedia token, seperti ditunjukkan dalam contoh berikut. Tab cURL menunjukkan alur mentahnya.

Dua client ID yang berbeda muncul dalam sampel. `<APP_ID>` adalah client ID app registration audiens dari [Daftarkan audiens token](#register-the-token-audience); scope `api://<APP_ID>/.default` meminta Entra untuk token yang dialamatkan ke audiens tersebut. `$AZURE_CLIENT_ID` adalah client ID managed identity, disuntikkan oleh webhook, dan mengidentifikasi pemanggil. Jangan menukar satu dengan yang lain.

<Tip>
  Jika workload Anda sudah menggunakan pustaka klien Azure Identity, berikan akuisisi tokennya (`DefaultAzureCredential` dengan scope `api://<APP_ID>/.default`) sebagai penyedia token identitas alih-alih melakukan pertukaran dua langkah sendiri. Pustaka tersebut membaca variabel lingkungan `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID`, dan `AZURE_TENANT_ID` yang sama dan menangani pertukaran Entra.
</Tip>

<CodeGroup>
  ```bash cURL
  # 1. Tukarkan token yang diproyeksikan Kubernetes (di $AZURE_FEDERATED_TOKEN_FILE)
  #    dengan JWT yang diterbitkan Entra.
  ENTRA_JWT=$(curl -sS "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
    -d grant_type=client_credentials \
    -d "client_id=$AZURE_CLIENT_ID" \
    --data-urlencode "scope=api://<APP_ID>/.default" \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode "client_assertion@$AZURE_FEDERATED_TOKEN_FILE" \
    | jq -r .access_token)

  # 2. Tukarkan JWT Entra dengan token akses Anthropic.
  ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON | jq -r .access_token
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$ENTRA_JWT",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )

  # 3. Panggil Claude API.
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from Azure"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os
  from pathlib import Path

  import anthropic
  import requests
  from anthropic import WorkloadIdentityCredentials


  def fetch_entra_token_via_federation() -> str:
      federated_token = Path(os.environ["AZURE_FEDERATED_TOKEN_FILE"]).read_text()
      response = requests.post(
          f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}/oauth2/v2.0/token",
          data={
              "client_id": os.environ["AZURE_CLIENT_ID"],
              "grant_type": "client_credentials",
              "scope": "api://<APP_ID>/.default",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              "client_assertion": federated_token,
          },
          timeout=5,
      )
      response.raise_for_status()
      return response.json()["access_token"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_entra_token_via_federation,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from Azure"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { readFile } from "node:fs/promises";

  async function fetchEntraTokenViaFederation(): Promise<string> {
    const federatedToken = await readFile(process.env.AZURE_FEDERATED_TOKEN_FILE!, "utf8");
    const response = await fetch(
      `https://login.microsoftonline.com/${process.env.AZURE_TENANT_ID}/oauth2/v2.0/token`,
      {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: process.env.AZURE_CLIENT_ID!,
          grant_type: "client_credentials",
          scope: "api://<APP_ID>/.default",
          client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
          client_assertion: federatedToken
        })
      }
    );
    const body = (await response.json()) as { access_token: string };
    return body.access_token;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchEntraTokenViaFederation,
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
    messages: [{ role: "user", content: "Hello from Azure" }]
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

  func fetchEntraTokenViaFederation(ctx context.Context) (string, error) {
  	federatedToken, err := os.ReadFile(os.Getenv("AZURE_FEDERATED_TOKEN_FILE"))
  	if err != nil {
  		return "", err
  	}
  	form := url.Values{
  		"client_id":             {os.Getenv("AZURE_CLIENT_ID")},
  		"grant_type":            {"client_credentials"},
  		"scope":                 {"api://<APP_ID>/.default"},
  		"client_assertion_type": {"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"},
  		"client_assertion":      {strings.TrimSpace(string(federatedToken))},
  	}
  	tokenURL := "https://login.microsoftonline.com/" + os.Getenv("AZURE_TENANT_ID") + "/oauth2/v2.0/token"
  	req, err := http.NewRequestWithContext(ctx, http.MethodPost, tokenURL, strings.NewReader(form.Encode()))
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
  		option.WithFederationTokenProvider(option.IdentityTokenFunc(fetchEntraTokenViaFederation), option.FederationOptions{
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
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from Azure")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content[0].Text)
  }
  ```

  ```java Java
  IdentityTokenProvider fetchEntraTokenViaFederation = () -> {
      try {
          var form = Map.of(
                          "client_id", System.getenv("AZURE_CLIENT_ID"),
                          "grant_type", "client_credentials",
                          "scope", "api://<APP_ID>/.default",
                          "client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                          "client_assertion", Files.readString(Path.of(System.getenv("AZURE_FEDERATED_TOKEN_FILE"))))
                  .entrySet().stream()
                  .map(entry -> entry.getKey() + "=" + URLEncoder.encode(entry.getValue(), UTF_8))
                  .collect(Collectors.joining("&"));
          var request = HttpRequest.newBuilder(URI.create(
                          "https://login.microsoftonline.com/" + System.getenv("AZURE_TENANT_ID") + "/oauth2/v2.0/token"))
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
                  fetchEntraTokenViaFederation,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
                  System.getenv("ANTHROPIC_WORKSPACE_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Hello from Azure")
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
      IdentityTokenProvider = new EntraFederationTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from Azure" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class EntraFederationTokenProvider : IIdentityTokenProvider
  {
      private static readonly HttpClient Http = new();

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          var federatedToken = await File.ReadAllTextAsync(
              Environment.GetEnvironmentVariable("AZURE_FEDERATED_TOKEN_FILE")!, ct);
          var tenantId = Environment.GetEnvironmentVariable("AZURE_TENANT_ID");
          var form = new FormUrlEncodedContent(new Dictionary<string, string>
          {
              ["client_id"] = Environment.GetEnvironmentVariable("AZURE_CLIENT_ID")!,
              ["grant_type"] = "client_credentials",
              ["scope"] = "api://<APP_ID>/.default",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              ["client_assertion"] = federatedToken,
          });
          var response = await Http.PostAsync(
              $"https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token", form, ct);
          response.EnsureSuccessStatusCode();
          using var json = await JsonDocument.ParseAsync(
              await response.Content.ReadAsStreamAsync(ct), default, ct);
          return json.RootElement.GetProperty("access_token").GetString()!;
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  function fetchEntraTokenViaFederation(): string
  {
      $ch = curl_init('https://login.microsoftonline.com/' . getenv('AZURE_TENANT_ID') . '/oauth2/v2.0/token');
      curl_setopt_array($ch, [
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_POSTFIELDS => http_build_query([
              'client_id' => getenv('AZURE_CLIENT_ID'),
              'grant_type' => 'client_credentials',
              'scope' => 'api://<APP_ID>/.default',
              'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
              'client_assertion' => file_get_contents(getenv('AZURE_FEDERATED_TOKEN_FILE')),
          ]),
      ]);
      $body = json_decode(curl_exec($ch), true);
      curl_close($ch);
      return $body['access_token'];
  }

  $client = new Client(
      credentials: new WorkloadIdentityCredentials(
          identityTokenProvider: fetchEntraTokenViaFederation(...),
          federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
          organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
          serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
          workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
      ),
  );

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from Azure']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "json"
  require "net/http"

  def fetch_entra_token_via_federation
    tenant_id = ENV.fetch("AZURE_TENANT_ID")
    federated_token = File.read(ENV.fetch("AZURE_FEDERATED_TOKEN_FILE"))
    response = Net::HTTP.post_form(
      URI("https://login.microsoftonline.com/#{tenant_id}/oauth2/v2.0/token"),
      "client_id" => ENV.fetch("AZURE_CLIENT_ID"),
      "grant_type" => "client_credentials",
      "scope" => "api://<APP_ID>/.default",
      "client_assertion_type" => "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      "client_assertion" => federated_token
    )
    JSON.parse(response.body).fetch("access_token")
  end

  client = Anthropic::Client.new(
    credentials: Anthropic::WorkloadIdentityCredentials.new(
      identity_token_provider: -> { fetch_entra_token_via_federation },
      federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
      organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
      service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
    )
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Azure"}]
  )
  puts message.content.first.text
  ```

  ```bash CLI
  # 1. Tukarkan token yang diproyeksikan Kubernetes dengan token akses yang
  # diterbitkan Entra, lalu tulis ke file sementara yang dapat dibaca CLI.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  trap 'rm -f "$ANTHROPIC_IDENTITY_TOKEN_FILE"' EXIT
  curl -sS "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
    -d client_id="$AZURE_CLIENT_ID" \
    -d grant_type=client_credentials \
    --data-urlencode "scope=api://<APP_ID>/.default" \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion@"$AZURE_FEDERATED_TOKEN_FILE" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # 2. Panggil Claude API. ANTHROPIC_FEDERATION_RULE_ID,
  # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca
  # dari environment.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Azure"}'
  ```
</CodeGroup>

### Verifikasi penyiapan

Dari dalam pod yang berlabel, jalankan pertukaran cURL yang ditunjukkan di [Dapatkan dan gunakan token](#acquire-and-use-the-token-2) dan konfirmasikan bahwa `POST /v1/oauth/token` mengembalikan `200` dengan `access_token` yang dimulai dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, dekode token yang diterbitkan Entra dari langkah 1 (lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange) untuk perintahnya) dan periksa penyebab paling umum di sisi Azure:

* **Ketidakcocokan issuer:** `issuer_url` yang terdaftar harus sama persis dengan klaim `iss` token. Token v2.0 membawa `https://login.microsoftonline.com/<TENANT_ID>/v2.0`; jika klaim `ver` yang didekode adalah `1.0`, lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0).
* **Masa berlaku token:** Jika kebijakan masa berlaku token tenant atau CAE memperpanjang token `client_credentials` melewati 7500 detik, naikkan `max_jwt_lifetime_seconds` issuer seperti dijelaskan di [Konfigurasikan Anthropic](#configure-anthropic-2).
* **Ketidakcocokan audiens:** `audience` aturan harus sama persis dengan `aud` token: client ID app registration audiens untuk token v2.0 yang dikonfigurasi panduan ini.
* **Ketidakcocokan nama klaim:** Aturan yang mencocokkan klaim yang tidak dibawa token tidak akan pernah lolos. Token v1.0 membawa client ID dalam `appid`, bukan `azp`; lihat [Jika token Anda adalah v1.0](#if-your-tokens-are-v1-0).

## Jika token Anda adalah v1.0

Panduan ini mengonfigurasi app registration audiens dengan `api.requestedAccessTokenVersion: 2`, sehingga setiap token yang ditunjukkannya adalah v2.0. Jika Anda menggunakan kembali registrasi yang sudah ada yang membiarkan `requestedAccessTokenVersion` tidak diatur, Entra menerbitkan token v1.0 sebagai gantinya. Dekode token sampel dan periksa klaim `ver`-nya; jika nilainya `1.0`, empat hal berubah:

* **Issuer:** Klaim `iss` adalah `https://sts.windows.net/<TENANT_ID>/` alih-alih `https://login.microsoftonline.com/<TENANT_ID>/v2.0`. Daftarkan URL issuer persis seperti yang dibawa klaim `iss` token Anda. Kedua URL berbagi JWKS yang sama, sehingga mode discovery berfungsi untuk keduanya.
* **Pemilih wizard:** Pilih **v1 (sts.windows.net)** di pemilih **Token issuer** pada wizard Connect workload alih-alih **v2.0 (login.microsoftonline.com)**.
* **Audiens:** Klaim `aud` adalah identifier URI yang Anda berikan sebagai `resource` (misalnya, `api://<APP_ID>`), bukan client ID registrasi. Atur `audience` federation rule ke nilai `aud` yang persis dari token yang Anda dekode.
* **Klaim client ID:** Client ID identitas pemanggil muncul di `appid`, bukan `azp`. Kedua klaim tidak pernah muncul dalam token yang sama, sehingga aturan yang mencocokkan `azp` tidak akan pernah lolos terhadap token v1.0.

Klaim `oid`, `sub`, dan `tid` membawa nilai yang sama di kedua versi, sehingga sisa panduan ini berlaku tanpa perubahan.

## Batasi cakupan aturan Anda

Federation rule dapat mencocokkan subjek token dengan `subject_prefix` sebagai tambahan (atau pengganti) peta `claims`; lihat [Semantik pencocokan aturan](/docs/id/manage-claude/wif-reference#rule-matching-semantics) untuk cara bidang-bidang tersebut digabungkan. Nilai `sub` Entra untuk identitas ini adalah GUID kanonis dengan panjang tetap, sehingga `subject_prefix` yang berisi object ID 36 karakter lengkap hanya cocok dengan subjek tersebut; ini adalah properti dari format subjek Entra, bukan dari `subject_prefix` secara umum.

<Warning>
  Setiap identitas di tenant Anda dapat meminta token untuk audiens yang terdaftar, sehingga `audience` dan `tid` saja tidak mengidentifikasi workload tertentu. Aturan yang menghilangkan pencocokan `oid` (atau `azp`/`appid`), atau yang menggunakan wildcard atau `subject_prefix` GUID parsial, mengotorisasi setiap managed identity dan service principal di tenant.
</Warning>

Kunci blok `match` aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Cocokkan `oid` sebagai nilai persis:** Atur `claims.oid` ke object ID lengkap managed identity. `subject_prefix` yang diatur ke object ID lengkap tersebut setara (wizard Console mengatur keduanya); jangan pernah menggunakan wildcard atau `subject_prefix` GUID parsial, yang cocok dengan lebih banyak identitas daripada yang Anda maksudkan.
* **Kunci `tid` sebagai pertahanan berlapis:** URL issuer sudah mengunci tenant Anda, tetapi menambahkan `claims.tid` melindungi dari penyimpangan konfigurasi jika catatan issuer diedit di kemudian hari.
* **Kunci audiens:** Atur `audience` ke nilai `aud` yang persis dari token yang Anda dekode sehingga token yang dicetak untuk aplikasi lain ditolak.
* **Gunakan aturan terpisah untuk setiap managed identity:** Buat satu aturan untuk setiap identitas alih-alih satu aturan yang mengotorisasi beberapa identitas, sehingga Anda dapat mencabut akses satu workload tanpa memengaruhi yang lain.

## Langkah selanjutnya

* Tinjau model konfigurasi lengkap di [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation).
* Lihat [panduan penyedia](/docs/id/manage-claude/workload-identity-federation#identity-providers) untuk AWS, Google Cloud, GitHub Actions, dan Kubernetes.
* Untuk variabel lingkungan, file profil, dan prioritas kredensial, lihat [referensi WIF](/docs/id/manage-claude/wif-reference).
