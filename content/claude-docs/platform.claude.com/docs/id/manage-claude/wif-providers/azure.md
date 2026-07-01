---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/azure
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: fe7dc1cb98b38f8d4616aee8d2d2ebfd5fb05ed2a18b4e8d1511dacbdc684bdb
---

# Menggunakan WIF dengan Microsoft Entra ID

Federasikan managed identity Azure dan Entra Workload Identity dengan Claude API sehingga workload Azure Anda dapat memanggil Claude tanpa kunci API statis.

---

Workload Azure melakukan autentikasi ke Claude API dengan menyajikan "JSON Web Token" (token web JSON), atau JWT, yang diterbitkan oleh Microsoft Entra ID, lalu menukarnya dengan access token Anthropic berumur pendek. Ada dua cara umum untuk memperoleh token yang diterbitkan Entra:

* **Managed identity (VM, App Service, Functions, Container Apps):** Workload meminta JWT untuk identitas yang ditetapkan padanya dari endpoint token lokal platform: Azure Instance Metadata Service (IMDS) di `http://169.254.169.254/metadata/identity/oauth2/token` pada VM dan VM Scale Sets, atau endpoint dalam variabel lingkungan `IDENTITY_ENDPOINT` pada App Service, Functions, dan Container Apps.
* **Entra Workload Identity (pod AKS):** Kubernetes memproyeksikan token service account (ditandatangani oleh OIDC issuer klaster AKS) ke dalam pod pada path yang ada di `AZURE_FEDERATED_TOKEN_FILE`. Workload menukar token tersebut di Entra untuk mendapatkan access token yang diterbitkan Entra.

Dalam kedua kasus tersebut, token yang diterbitkan Entra yang Anda sajikan ke Anthropic membawa issuer Entra khusus tenant (langkah [Mengonfigurasi Anthropic](#configure-anthropic) menunjukkan URL persis yang harus didaftarkan) dan object ID managed identity dalam klaim `sub` dan `oid`. Anda mendaftarkan issuer tersebut ke Anthropic satu kali, menulis aturan federasi yang cocok dengan klaim yang diharapkan, dan workload Anda menukar token Entra-nya dengan access token `sk-ant-oat01-...` saat runtime.

<Tip>
  Pod AKS dapat secara alternatif melewati pertukaran Entra dan menyajikan token service account yang diproyeksikan Kubernetes langsung ke Anthropic. Jalur tersebut mendaftarkan OIDC issuer klaster AKS Anda ke Anthropic alih-alih tenant Entra Anda. Lihat [Menggunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk alur tersebut.
</Tip>

## Prasyarat

* Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan aturan federasi.
* Langganan Azure dengan izin untuk menetapkan managed identity (atau mengonfigurasi Entra Workload Identity pada AKS).
* Izin untuk membuat app registration dan service principal di tenant Microsoft Entra Anda. Entra hanya menerbitkan token untuk audience yang ada di tenant, sehingga langkah [Mendaftarkan audience token](#register-the-token-audience) diperlukan sebelum permintaan token apa pun berhasil.
* Tenant ID Microsoft Entra Anda. Temukan di portal Azure pada **Microsoft Entra ID → Overview → Tenant ID**.
* Izin untuk membuat service account, federation issuer, dan aturan federasi di Claude Console untuk organisasi Anthropic Anda.

## Mengonfigurasi Azure

Pertama daftarkan audience yang akan menjadi target penerbitan token Entra, lalu siapkan identitas yang memintanya.

### Mendaftarkan audience token

Microsoft Entra ID hanya menerbitkan token ketika audience yang diminta ada di tenant Anda sebagai app registration dengan service principal. Buat satu app registration untuk merepresentasikan audience Claude API; setiap workload di tenant dapat meminta token untuknya. Tanpa registrasi ini, permintaan token gagal dengan error "resource not found in tenant" (`AADSTS50001` dari endpoint managed identity, `AADSTS500011` dari endpoint token Entra).

```bash
# Buat registrasi aplikasi yang merepresentasikan audiens Claude API.
APP_ID=$(az ad app create --display-name claude-api-federation --query appId -o tsv)

# Minta access token v2.0 dan atur URI pengidentifikasi api://<APP_ID>.
az ad app update --id "$APP_ID" \
  --identifier-uris "api://$APP_ID" \
  --set api.requestedAccessTokenVersion=2

# Buat service principal agar audiens dapat di-resolve di tenant Anda.
az ad sp create --id "$APP_ID"
```

<Note>
  Gunakan format identifier URI `api://<APP_ID>`. Entra membatasi identifier URI `https://` hanya untuk domain terverifikasi milik tenant Anda sendiri, sehingga URI seperti `https://api.anthropic.com` tidak dapat didaftarkan di sebagian besar tenant; `api://<APP_ID>` diterima di mana saja. Dengan `requestedAccessTokenVersion: 2`, token untuk audience ini adalah v2.0: klaim `iss` adalah `https://login.microsoftonline.com/<TENANT_ID>/v2.0` dan klaim `aud` adalah client ID registrasi (`<APP_ID>`). Panduan ini mengasumsikan token v2.0; jika Anda menggunakan kembali registrasi yang sudah ada yang menghasilkan token v1.0, lihat Catatan di bawah [Mengonfigurasi Anthropic](#configure-anthropic).
</Note>

### Menyiapkan workload identity

Pilih jalur yang sesuai dengan tempat workload Anda berjalan.

<Tabs>
  <Tab title="VM, App Service, Functions, Container Apps">
    Aktifkan managed identity system-assigned atau user-assigned pada resource Azure Anda. Di portal Azure, buka resource tersebut, masuk ke **Identity**, dan aktifkan **System assigned** (atau lampirkan identitas user-assigned).

    Setelah identitas dibuat, catat **Object (principal) ID**-nya. GUID ini muncul sebagai klaim `sub` dan `oid` dalam token yang diterbitkan, dan aturan federasi Anthropic Anda akan mencocokkannya. Anda dapat menemukannya di halaman **Identity** resource; untuk identitas user-assigned, ini adalah **Object (principal) ID** di halaman **Overview** resource managed identity. (Managed identity hanya memiliki service principal di Microsoft Entra ID, bukan app registration.)

    Platform mengekspos endpoint token lokal setelah identitas dilampirkan:

    * **VM dan VM Scale Sets:** IMDS di `http://169.254.169.254/metadata/identity/oauth2/token` dengan header `Metadata: true` dan `api-version=2018-02-01`.
    * **App Service, Functions, dan Container Apps:** URL dalam variabel lingkungan `IDENTITY_ENDPOINT` dengan header `X-IDENTITY-HEADER` yang diatur ke nilai `IDENTITY_HEADER`, dan `api-version=2019-08-01`. IMDS tidak dapat dijangkau pada platform ini.

    Jika resource memiliki lebih dari satu managed identity user-assigned, tambahkan `client_id=<IDENTITY_CLIENT_ID>` ke permintaan token untuk memilih salah satunya. Azure merekomendasikan untuk selalu menentukannya: tanpa itu, permintaan akan gagal segera setelah identitas kedua dilampirkan, atau kembali ke identitas system-assigned dan kemudian gagal pada pencocokan `oid` aturan federasi Anda.
  </Tab>

  <Tab title="Entra Workload Identity (AKS)">
    Entra Workload Identity memfederasikan service account Kubernetes dengan aplikasi Entra sehingga pod dapat menukar token service account yang diterbitkan klaster mereka dengan access token yang diterbitkan Entra.

    1. Aktifkan OIDC issuer dan workload identity pada klaster AKS Anda (`az aks update --enable-oidc-issuer --enable-workload-identity ...`). Mengaktifkan workload identity akan menginstal mutating webhook `azure-workload-identity` untuk Anda; deploy secara manual hanya pada klaster non-AKS.
    2. Buat managed identity user-assigned. Catat **Client ID**-nya (digunakan dalam anotasi service account) dan **Object (principal) ID**-nya, yang ditampilkan di halaman **Overview** managed identity; aturan federasi Anthropic Anda akan mencocokkan Object ID dalam klaim `oid`. Kemudian buat service account Kubernetes yang dianotasi dengan `azure.workload.identity/client-id: <IDENTITY_CLIENT_ID>`. Webhook membaca anotasi ini untuk menyuntikkan `AZURE_CLIENT_ID` ke dalam pod, yang dibaca oleh sampel di [Pada AKS dengan Entra Workload Identity](#on-aks-with-entra-workload-identity) dari lingkungan.
    3. Buat federated credential pada managed identity yang memercayai OIDC issuer klaster untuk service account tersebut.
    4. Beri label spesifikasi pod Anda dengan `azure.workload.identity/use: "true"` dan atur `serviceAccountName` ke service account tersebut.

    Webhook menyuntikkan `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID`, dan `AZURE_TENANT_ID` ke dalam pod. File di `AZURE_FEDERATED_TOKEN_FILE` berisi token service account yang diproyeksikan Kubernetes, ditandatangani oleh OIDC issuer klaster AKS.
  </Tab>
</Tabs>

### Klaim token

Token yang diterbitkan Entra untuk managed identity membawa klaim berikut (token v2.0 ditampilkan; lihat Catatan di bawah [Mengonfigurasi Anthropic](#configure-anthropic) untuk perbedaan token v1.0):

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

`sub` dan `oid` identik (object ID managed identity). Client ID identitas pemanggil muncul di `azp` pada token v2.0 dan di `appid` pada token v1.0; kedua klaim tersebut tidak pernah muncul dalam token yang sama, jadi periksa `ver` sebelum menulis aturan terhadap salah satunya. Klaim `aud` juga bergantung pada versi token: token v2.0 membawa client ID app registration audience (GUID `<APP_ID>` dari [Mendaftarkan audience token](#register-the-token-audience)); token v1.0 membawa identifier URI yang Anda berikan sebagai `resource` (misalnya, `api://<APP_ID>`). Cocokkan pada `oid` untuk mengotorisasi satu managed identity tertentu. Klaim client ID (`azp` pada token v2.0, `appid` pada token v1.0) adalah alternatif ketika Anda ingin mengotorisasi setiap workload yang berbagi satu app registration alih-alih satu object ID; untuk managed identity, klaim ini unik untuk identitas tersebut, sehingga mencocokkannya setara dengan mencocokkan `oid`. Klaim `tid` mengulangi tenant ID Anda; mencocokkannya adalah pertahanan berlapis, karena URL issuer sudah mengunci tenant.

## Mengonfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **Microsoft Entra**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat aturan federasi.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Entra memublikasikan dokumen OIDC discovery di URL issuer per-tenant, jadi gunakan mode discovery. Setiap tenant Microsoft Entra yang Anda federasikan memerlukan record issuer-nya sendiri. Selector **Token issuer** pada wizard secara default adalah **v1 (sts.windows.net)**; pilih **v2.0 (login.microsoftonline.com)** agar cocok dengan token v2.0 yang dikonfigurasi panduan ini, dan pilih v1 hanya jika Anda menggunakan kembali registrasi yang menghasilkan token v1.0.

```json
{
  "name": "azure-prod-tenant",
  "issuer_url": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
  "jwks": { "type": "discovery" },
  "max_jwt_lifetime_seconds": 86400
}
```

<Warning>
  Token Entra bertahan lebih lama dari masa hidup JWT maksimum default 1 jam, jadi atur `max_jwt_lifetime_seconds` pada issuer atau pertukaran akan gagal dengan `invalid_grant`. Token managed identity diterbitkan dengan jarak hingga 24 jam antara `iat` dan `exp` dan di-cache oleh Azure tanpa cara untuk memaksa refresh lebih awal, sehingga workload managed identity memerlukan `86400`. Token Entra Workload Identity (`client_credentials`) secara default memiliki masa hidup acak 60 hingga 90 menit; tile Microsoft Entra pada wizard Connect workload mengisi awal `7500` (sedikit lebih dari 2 jam), yang mencakup jalur tersebut tetapi tidak untuk token managed identity. Masa hidup yang diterima lebih lama berarti token Entra yang bocor tetap dapat ditukar lebih lama, jadi jaga kondisi pencocokan aturan tetap ketat, seperti dijelaskan di [Membatasi cakupan aturan Anda](#scope-your-rule).
</Warning>

<Note>
  Jika klaim `ver` pada token Anda yang telah di-decode adalah `1.0` (app registration audience membiarkan `api.requestedAccessTokenVersion` tidak diatur), maka `iss` adalah `https://sts.windows.net/<TENANT_ID>/`, dan `aud` adalah identifier URI yang Anda minta (misalnya, `api://<APP_ID>`). Daftarkan nilai `iss` persis yang dibawa token Anda dan atur `audience` aturan federasi ke nilai `aud` persis. Kedua URL issuer berbagi JWKS yang sama, sehingga mode discovery berfungsi untuk keduanya.
</Note>

**Aturan federasi:** Cocokkan pada object ID managed identity dan tenant ID Anda. Untuk token v2.0, nilai `audience` adalah client ID app registration audience (GUID `<APP_ID>` dari [Mendaftarkan audience token](#register-the-token-audience)); untuk token v1.0, nilainya adalah identifier URI (`api://<APP_ID>`). Gunakan nilai `aud` persis dari token Anda yang telah di-decode.

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

## Memperoleh dan menggunakan token

Saat runtime, workload Anda mengambil token Entra-nya, menukarnya di `POST /v1/oauth/token`, dan menggunakan bearer token yang dikembalikan untuk memanggil Claude. Setiap SDK Anthropic menangani loop pertukaran dan refresh ketika Anda menyediakan callable penyedia token, seperti yang ditunjukkan dalam contoh berikut. Tab cURL menunjukkan alur mentahnya.

Sampel mengambil token managed identity dari endpoint token platform: IMDS pada VM dan VM Scale Sets, atau layanan `IDENTITY_ENDPOINT` pada App Service, Functions, dan Container Apps. Ganti `api://<APP_ID>` dengan identifier URI dari [Mendaftarkan audience token](#register-the-token-audience).

<Tip>
  Jika workload Anda sudah menggunakan pustaka klien Azure Identity, berikan akuisisi tokennya (`DefaultAzureCredential` dengan scope `api://<APP_ID>/.default`) sebagai penyedia token identitas alih-alih memanggil endpoint token secara langsung. Pustaka tersebut memilih endpoint yang benar pada setiap platform Azure, termasuk AKS dengan Entra Workload Identity.
</Tip>

<CodeGroup>
  ```bash cURL
  # 1. Ambil token yang diterbitkan Entra (managed identity).
  #    Pada VM atau VM Scale Set, gunakan IMDS. Jika ada beberapa identitas
  #    user-assigned, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  ENTRA_TOKEN=$(curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=api://<APP_ID>" \
    | jq -r .access_token)

  #    Pada App Service, Functions, atau Container Apps, gunakan layanan
  #    token lokal (IMDS tidak dapat dijangkau di sana):
  # ENTRA_TOKEN=$(curl -sS -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" \
  #   "$IDENTITY_ENDPOINT?api-version=2019-08-01&resource=api://<APP_ID>" \
  #   | jq -r .access_token)

  #    Untuk AKS dengan Entra Workload Identity, gunakan pertukaran dua langkah
  #    di bagian "On AKS with Entra Workload Identity" sebagai gantinya.

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

  # 3. Panggil API Claude dengan bearer token tersebut.
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from Azure"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  import requests
  from anthropic import WorkloadIdentityCredentials

  # URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Register the token audience).
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
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from Azure"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";

  // URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Mendaftarkan audiens token).
  const AUDIENCE = "api://<APP_ID>";

  async function fetchEntraToken(): Promise<string> {
    // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
    // VM dan VM Scale Sets menggunakan IMDS.
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
    model: "claude-sonnet-4-6",
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

  // URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Register the token audience).
  const audience = "api://<APP_ID>"

  // fetchEntraToken mengambil token managed identity dari endpoint token
  // platform: IMDS pada VM dan VM Scale Sets, atau layanan IDENTITY_ENDPOINT
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
  		Model:     anthropic.ModelClaudeSonnet4_6,
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
  // URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Register the token audience).
  String audience = "api://<APP_ID>";
  // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
  // VM dan VM Scale Sets menggunakan IMDS.
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
          .model(Model.CLAUDE_SONNET_4_6)
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
      Model = Model.ClaudeSonnet4_6,
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
      // URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Register the token audience).
      private const string Audience = "api://<APP_ID>";

      private static readonly HttpClient httpClient = new();

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
          // VM dan VM Scale Sets menggunakan IMDS.
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

  // URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Register the token audience).
  const AUDIENCE = 'api://<APP_ID>';

  function fetchEntraToken(): string
  {
      // App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
      // VM dan VM Scale Sets menggunakan IMDS.
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
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from Azure']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "json"
  require "net/http"

  # URI pengidentifikasi dari pendaftaran aplikasi audiens (lihat Mendaftarkan audiens token).
  AUDIENCE = "api://<APP_ID>"

  def fetch_entra_token
    # App Service, Functions, dan Container Apps menyuntikkan IDENTITY_ENDPOINT;
    # VM dan VM Scale Sets menggunakan IMDS.
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
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Azure"}]
  )
  puts message.content.first.text
  ```

  ```bash CLI
  # Tulis access token yang diterbitkan Entra ke file yang dapat dibaca oleh CLI.
  # Ditampilkan untuk VM atau VM Scale Set (IMDS). Pada App Service, Functions, atau
  # Container Apps, ambil dari "$IDENTITY_ENDPOINT?api-version=2019-08-01&resource=api://<APP_ID>"
  # dengan -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" sebagai gantinya.
  # Jika ada beberapa user-assigned identity, tambahkan &client_id=<IDENTITY_CLIENT_ID>.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=api://<APP_ID>" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca dari environment.
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Azure"}'
  ```
</CodeGroup>

### Pada AKS dengan Entra Workload Identity

Pada AKS, file di `AZURE_FEDERATED_TOKEN_FILE` adalah token service account yang diproyeksikan Kubernetes yang ditandatangani oleh OIDC issuer klaster Anda, bukan token yang diterbitkan Entra. Untuk tetap pada jalur yang dimediasi Entra yang dijelaskan di halaman ini, tukar token tersebut di `https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token` (grant `client_credentials` federasi) terlebih dahulu, lalu berikan access token Entra yang dihasilkan ke SDK Anthropic sebagai token identitas.

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

  # 3. Panggil API Claude.
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
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
      model="claude-sonnet-4-6",
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
    model: "claude-sonnet-4-6",
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
  		Model:     anthropic.ModelClaudeSonnet4_6,
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
          .model(Model.CLAUDE_SONNET_4_6)
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
      Model = Model.ClaudeSonnet4_6,
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
      model: 'claude-sonnet-4-6',
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
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Azure"}]
  )
  puts message.content.first.text
  ```

  ```bash CLI
  # 1. Tukarkan token yang diproyeksikan Kubernetes dengan access token yang diterbitkan Entra
  # dan tulis ke file sementara yang dapat dibaca oleh CLI.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
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
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Azure"}'
  ```
</CodeGroup>

Sebagai alternatif, daftarkan OIDC issuer klaster AKS Anda ke Anthropic secara langsung dan lewati langkah Entra. Lihat [Menggunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk pola tersebut.

## Memverifikasi pengaturan

Dari resource Azure Anda, jalankan pertukaran cURL yang ditunjukkan sebelumnya dan konfirmasi bahwa `POST /v1/oauth/token` mengembalikan `200` dengan `access_token` yang dimulai dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, decode token Entra (lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange) untuk perintahnya) dan periksa penyebab paling umum di sisi Azure:

* **Ketidakcocokan issuer:** `issuer_url` yang terdaftar harus cocok persis dengan klaim `iss` token. Periksa klaim `ver`: token v2.0 membawa `https://login.microsoftonline.com/<TENANT_ID>/v2.0`, token v1.0 membawa `https://sts.windows.net/<TENANT_ID>/`.
* **Masa hidup token:** Token managed identity membawa jarak hingga 24 jam antara `iat` dan `exp`, yang melebihi maksimum default 1 jam pada issuer. Atur `max_jwt_lifetime_seconds` seperti dijelaskan di [Mengonfigurasi Anthropic](#configure-anthropic).
* **Ketidakcocokan audience:** `audience` aturan harus sama persis dengan `aud` token: client ID app registration audience untuk token v2.0, atau identifier URI `api://` untuk token v1.0.
* **Ketidakcocokan nama klaim:** Token v1.0 membawa client ID di `appid`, bukan `azp`. Aturan yang mencocokkan pada klaim yang tidak dibawa token tidak akan pernah lolos.

## Membatasi cakupan aturan Anda

<Warning>
  Setiap identitas di tenant Anda dapat meminta token untuk audience yang terdaftar, sehingga `audience` dan `tid` saja tidak mengidentifikasi workload tertentu. Aturan yang menghilangkan pencocokan `oid` (atau `azp`/`appid`), atau yang menggunakan `subject_prefix` wildcard atau GUID parsial, mengotorisasi setiap managed identity dan service principal di tenant.
</Warning>

Kunci blok `match` aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Cocokkan `oid` sebagai nilai persis:** Atur `claims.oid` ke object ID lengkap managed identity. `subject_prefix` yang diatur ke object ID lengkap tersebut adalah setara (wizard Console mengatur keduanya); jangan pernah menggunakan `subject_prefix` wildcard atau GUID parsial, yang mencocokkan lebih banyak identitas dari yang Anda maksudkan.
* **Kunci `tid` sebagai pertahanan berlapis:** URL issuer sudah mengunci tenant Anda, tetapi menambahkan `claims.tid` melindungi dari pergeseran konfigurasi jika record issuer diedit di kemudian hari.
* **Kunci audience:** Atur `audience` ke nilai `aud` persis dari token Anda yang telah di-decode sehingga token yang dibuat untuk aplikasi lain ditolak.
* **Gunakan aturan terpisah untuk setiap managed identity:** Buat satu aturan untuk setiap identitas alih-alih satu aturan yang mengotorisasi beberapa identitas, sehingga Anda dapat mencabut akses satu workload tanpa memengaruhi yang lain.

## Langkah selanjutnya

* Tinjau model konfigurasi lengkap di [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation).
* Lihat [panduan penyedia](/docs/id/manage-claude/workload-identity-federation#identity-providers) untuk AWS, Google Cloud, GitHub Actions, dan Kubernetes.
* Untuk variabel lingkungan, file profil, dan urutan prioritas kredensial, lihat [referensi WIF](/docs/id/manage-claude/wif-reference).
