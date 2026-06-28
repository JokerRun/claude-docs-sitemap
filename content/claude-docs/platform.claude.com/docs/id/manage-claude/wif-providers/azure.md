---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/azure
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 8e4cb9fdd86b04fdc309e8fc0372ff0c05c169ebcf59f225cdd1245cc4d7c076
---

# Menggunakan WIF dengan Microsoft Entra ID

Federasikan managed identity Azure dan Entra Workload Identity dengan Claude API sehingga workload Azure Anda dapat memanggil Claude tanpa kunci API statis.

---

Workload Azure melakukan autentikasi ke Claude API dengan menyajikan "JSON Web Token" (Token Web JSON), atau JWT, yang diterbitkan oleh Microsoft Entra ID, lalu menukarnya dengan access token Anthropic berumur pendek. Ada dua cara umum untuk memperoleh token yang diterbitkan Entra:

* **Managed identity (VM, App Service, Functions, Container Apps):** Workload memanggil Azure Instance Metadata Service (IMDS) di `http://169.254.169.254/metadata/identity/oauth2/token` dan menerima JWT untuk identitas yang ditetapkan padanya.
* **Entra Workload Identity (pod AKS):** Kubernetes memproyeksikan token service account (ditandatangani oleh OIDC issuer klaster AKS) ke dalam pod pada path yang ada di `AZURE_FEDERATED_TOKEN_FILE`. Workload menukar token tersebut di Entra untuk mendapatkan access token yang diterbitkan Entra.

Dalam kedua kasus tersebut, token yang diterbitkan Entra yang Anda sajikan ke Anthropic membawa issuer Entra spesifik tenant (langkah [Mengonfigurasi Anthropic](#configure-anthropic) menunjukkan URL persis yang harus didaftarkan) dan object ID dari managed identity dalam klaim `sub` dan `oid`. Anda mendaftarkan issuer tersebut ke Anthropic satu kali, menulis federation rule yang cocok dengan klaim yang diharapkan, dan workload Anda menukar token Entra-nya dengan access token `sk-ant-oat01-...` saat runtime.

<Tip>
  Pod AKS dapat secara alternatif melewati pertukaran Entra dan menyajikan token service account yang diproyeksikan Kubernetes langsung ke Anthropic. Jalur tersebut mendaftarkan OIDC issuer klaster AKS Anda ke Anthropic alih-alih tenant Entra Anda. Lihat [Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk alur tersebut.
</Tip>

## Prasyarat

* Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Langganan Azure dengan izin untuk menetapkan managed identity (atau mengonfigurasi Entra Workload Identity di AKS).
* Tenant ID Microsoft Entra Anda. Temukan di portal Azure pada **Microsoft Entra ID → Overview → Tenant ID**.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

## Mengonfigurasi Azure

Siapkan identitas yang akan diterbitkan tokennya oleh Microsoft Entra ID. Pilih jalur yang sesuai dengan tempat workload Anda berjalan.

<Tabs>
  <Tab title="VM, App Service, Functions, Container Apps">
    Aktifkan managed identity system-assigned atau user-assigned pada resource Azure Anda. Di portal Azure, buka resource tersebut, masuk ke **Identity**, dan aktifkan **System assigned** (atau lampirkan identitas user-assigned).

    Setelah identitas dibuat, catat **Object (principal) ID**-nya. GUID ini muncul sebagai klaim `sub` dan `oid` dalam token yang diterbitkan, dan federation rule Anthropic Anda akan mencocokkan berdasarkan nilai ini. Anda dapat menemukannya di halaman **Identity** resource tersebut, atau di bawah **Microsoft Entra ID → Enterprise applications** untuk identitas user-assigned.

    Tidak diperlukan konfigurasi lebih lanjut di sisi Azure. Azure Instance Metadata Service dapat dijangkau di `169.254.169.254` dari dalam resource setelah identitas dilampirkan.
  </Tab>

  <Tab title="Entra Workload Identity (AKS)">
    Entra Workload Identity memfederasikan service account Kubernetes dengan aplikasi Entra sehingga pod dapat menukar token service account yang diterbitkan klaster dengan access token yang diterbitkan Entra.

    1. Aktifkan OIDC issuer pada klaster AKS Anda (`az aks update --enable-oidc-issuer --enable-workload-identity ...`).
    2. Deploy mutating webhook `azure-workload-identity`.
    3. Buat managed identity user-assigned dan federated credential yang memercayai OIDC issuer klaster untuk service account Kubernetes Anda.
    4. Beri label pada spesifikasi pod Anda dengan `azure.workload.identity/use: "true"` dan atur `serviceAccountName` ke service account yang difederasikan.

    Webhook menyuntikkan `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID`, dan `AZURE_TENANT_ID` ke dalam pod. File di `AZURE_FEDERATED_TOKEN_FILE` berisi token service account yang diproyeksikan Kubernetes, ditandatangani oleh OIDC issuer klaster AKS.
  </Tab>
</Tabs>

### Klaim token

Token yang diterbitkan Entra untuk managed identity membawa klaim-klaim berikut (token v2 ditampilkan; lihat Catatan di bawah [Mengonfigurasi Anthropic](#configure-anthropic) untuk mengetahui perbedaan `iss` dan `aud` pada token v1):

```json
{
  "iss": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
  "sub": "9f8e7d6c-1a2b-3c4d-5e6f-...",
  "aud": "00000000-0000-0000-0000-000000000000",
  "oid": "9f8e7d6c-1a2b-3c4d-5e6f-...",
  "tid": "<TENANT_ID>",
  "azp": "<CLIENT_ID>",
  "exp": 1775527120
}
```

`sub` dan `oid` identik (object ID dari managed identity). `azp` adalah application ID atau client ID. Klaim `aud` bergantung pada versi token: token v2 membawa client ID aplikasi Entra Anda (sebuah GUID); token v1 membawa resource identifier yang diminta, yaitu nilai apa pun yang Anda berikan sebagai `resource` saat mengambil token (misalnya, `https://api.anthropic.com`). Cocokkan pada `oid` untuk mengotorisasi satu identitas spesifik, atau pada `azp` untuk mengotorisasi identitas apa pun yang terkait dengan registrasi aplikasi. Klaim `tid` mengulangi tenant ID Anda; mencocokkan pada klaim ini merupakan lapisan pertahanan tambahan, karena URL issuer sudah mengunci tenant.

## Mengonfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **Microsoft Entra ID**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Entra memublikasikan dokumen OIDC discovery di URL issuer per-tenant, jadi gunakan mode discovery. Setiap tenant Microsoft Entra yang Anda federasikan memerlukan record issuer-nya sendiri.

```json
{
  "name": "azure-prod-tenant",
  "issuer_url": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
  "jwks": { "type": "discovery" }
}
```

<Note>
  Nilai `iss` pada access token mungkin berupa `https://sts.windows.net/<TENANT_ID>/` (v1.0), dan klaim `aud` mungkin membawa URL resource yang diminta (`https://api.anthropic.com`) alih-alih GUID. Bentuk mana yang diterima workload ditentukan oleh `api.requestedAccessTokenVersion` pada registrasi aplikasi **resource**: nilai default (`null`) menghasilkan token v1.0, sehingga token managed identity untuk audience kustom adalah v1.0 kecuali registrasi tersebut mengatur `requestedAccessTokenVersion: 2`. Decode token managed identity Anda (bagian Verifikasi di bagian selanjutnya dalam panduan ini menunjukkan caranya), daftarkan nilai `iss` apa pun yang terkandung di dalamnya, dan atur `audience` pada federation rule ke nilai `aud` apa pun yang terkandung di dalamnya. Kedua URL issuer tersebut berbagi JWKS yang sama, sehingga mode discovery berfungsi untuk keduanya.
</Note>

**Federation rule:** Cocokkan pada object ID managed identity dan tenant ID Anda. Untuk token v2, nilai `audience` adalah client ID aplikasi Entra Anda (sebuah GUID); gunakan nilai `aud` persis dari token Anda yang telah di-decode.

```json
{
  "name": "azure-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "audience": "00000000-0000-0000-0000-000000000000",
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

Saat runtime, workload Anda mengambil token Entra-nya, menukarnya di `POST /v1/oauth/token`, dan menggunakan bearer token yang dikembalikan untuk memanggil Claude. Setiap SDK Anthropic menangani loop pertukaran dan refresh ketika Anda menyediakan callable token-provider, seperti yang ditunjukkan dalam contoh berikut. Tab cURL menunjukkan alur mentahnya.

<CodeGroup>
  ```bash cURL
  # 1. Ambil token yang diterbitkan Entra dari IMDS (managed identity).
  #    Untuk AKS dengan Entra Workload Identity, gunakan pertukaran dua langkah di
  #    bagian "On AKS with Entra Workload Identity" sebagai gantinya.
  ENTRA_TOKEN=$(curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com" \
    | jq -r .access_token)

  # 2. Tukarkan dengan token akses Anthropic.
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    --data @- <<JSON
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

  IMDS_URL = "http://169.254.169.254/metadata/identity/oauth2/token"


  def fetch_entra_token() -> str:
      """Fetch a managed identity token from Azure IMDS."""
      response = requests.get(
          IMDS_URL,
          headers={"Metadata": "true"},
          params={"api-version": "2018-02-01", "resource": "https://api.anthropic.com"},
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

  const IMDS_URL =
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com";

  async function fetchEntraToken(): Promise<string> {
    const response = await fetch(IMDS_URL, {
      headers: { Metadata: "true" }
    });
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

  const imdsURL = "http://169.254.169.254/metadata/identity/oauth2/token" +
  	"?api-version=2018-02-01&resource=https://api.anthropic.com"

  // azureIMDSToken mengambil token identitas terkelola dari Azure IMDS.
  func azureIMDSToken(ctx context.Context) (string, error) {
  	req, err := http.NewRequestWithContext(ctx, http.MethodGet, imdsURL, nil)
  	if err != nil {
  		return "", err
  	}
  	req.Header.Set("Metadata", "true")
  	resp, err := http.DefaultClient.Do(req)
  	if err != nil {
  		return "", fmt.Errorf("call IMDS: %w", err)
  	}
  	defer resp.Body.Close()
  	var body struct {
  		AccessToken string `json:"access_token"`
  	}
  	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
  		return "", fmt.Errorf("decode IMDS response: %w", err)
  	}
  	return body.AccessToken, nil
  }

  func main() {
  	client := anthropic.NewClient(
  		option.WithFederationTokenProvider(azureIMDSToken, option.FederationOptions{
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
  HttpRequest metadataRequest = HttpRequest.newBuilder()
          .uri(URI.create("http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com"))
          .header("Metadata", "true")
          .build();

  IdentityTokenProvider fetchEntraToken = () -> {
      try {
          var response = http.send(metadataRequest, HttpResponse.BodyHandlers.ofString());
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
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
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
      private const string IMDS_URL =
          "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com";

      private static readonly HttpClient httpClient = new()
      {
          DefaultRequestHeaders = { { "Metadata", "true" } },
      };

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          using var json = await JsonDocument.ParseAsync(
              await httpClient.GetStreamAsync(IMDS_URL, ct), default, ct);
          return json.RootElement.GetProperty("access_token").GetString()!;
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  const IMDS_URL = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com';

  function fetchEntraToken(): string
  {
      $context = stream_context_create([
          'http' => ['header' => "Metadata: true\r\n"],
      ]);
      $body = json_decode(file_get_contents(IMDS_URL, false, $context), true);
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

  IMDS_URL = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com"

  def fetch_entra_token
    response = Net::HTTP.get(URI(IMDS_URL), {"Metadata" => "true"})
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
  # Tulis access token yang diterbitkan Entra ke file yang dapat dibaca CLI
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS -H "Metadata: true" \
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://api.anthropic.com" \
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

### Di AKS dengan Entra Workload Identity

Di AKS, file di `AZURE_FEDERATED_TOKEN_FILE` adalah token service account yang diproyeksikan Kubernetes dan ditandatangani oleh OIDC issuer klaster Anda, bukan token yang diterbitkan Entra. Untuk tetap pada jalur yang dimediasi Entra seperti yang dijelaskan di halaman ini, tukar token tersebut di `https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token` (grant `client_credentials` federated) terlebih dahulu, lalu berikan access token Entra yang dihasilkan ke SDK Anthropic sebagai identity token.

<CodeGroup>
  ```bash cURL
  # 1. Tukarkan token yang diproyeksikan Kubernetes (di $AZURE_FEDERATED_TOKEN_FILE)
  #    dengan JWT yang diterbitkan Entra.
  ENTRA_JWT=$(curl -sS "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
    -d grant_type=client_credentials \
    -d "client_id=$AZURE_CLIENT_ID" \
    --data-urlencode "scope=https://api.anthropic.com/.default" \
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
  import httpx
  import anthropic
  from anthropic import WorkloadIdentityCredentials


  def fetch_entra_token_via_federation() -> str:
      federated_token = Path(os.environ["AZURE_FEDERATED_TOKEN_FILE"]).read_text()
      response = httpx.post(
          f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}/oauth2/v2.0/token",
          data={
              "client_id": os.environ["AZURE_CLIENT_ID"],
              "grant_type": "client_credentials",
              "scope": "https://api.anthropic.com/.default",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              "client_assertion": federated_token,
          },
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
          scope: "https://api.anthropic.com/.default",
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
  		"scope":                 {"https://api.anthropic.com/.default"},
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
                          "scope", "https://api.anthropic.com/.default",
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
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
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
              ["scope"] = "https://api.anthropic.com/.default",
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
              'scope' => 'https://api.anthropic.com/.default',
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
      "scope" => "https://api.anthropic.com/.default",
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
  # 1. Tukarkan token yang diproyeksikan Kubernetes dengan token akses yang diterbitkan Entra
  # dan tulis ke file sementara yang dapat dibaca oleh CLI.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
    -d client_id="$AZURE_CLIENT_ID" \
    -d grant_type=client_credentials \
    --data-urlencode scope=https://api.anthropic.com/.default \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion@"$AZURE_FEDERATED_TOKEN_FILE" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # 2. Panggil API Claude. ANTHROPIC_FEDERATION_RULE_ID,
  # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca
  # dari environment.
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Azure"}'
  ```
</CodeGroup>

Sebagai alternatif, daftarkan OIDC issuer klaster AKS Anda ke Anthropic secara langsung dan lewati langkah Entra. Lihat [Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk pola tersebut.

## Memverifikasi pengaturan

Dari resource Azure Anda, jalankan pertukaran cURL yang ditunjukkan sebelumnya dan pastikan bahwa `POST /v1/oauth/token` mengembalikan `200` dengan `access_token` yang diawali `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Jika mendapat `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum di sisi Azure adalah ketidakcocokan antara `issuer_url` yang Anda daftarkan dan klaim `iss` dalam token Anda yang telah di-decode. Keduanya harus cocok persis. Untuk token managed identity, nilai `iss` adalah `https://login.microsoftonline.com/<TENANT_ID>/v2.0` atau `https://sts.windows.net/<TENANT_ID>/`.

## Membatasi cakupan rule Anda

<Warning>
  Klaim `oid` adalah GUID dari managed identity dan tidak memiliki prefiks yang stabil. `subject_prefix` dengan `*` akan cocok dengan identitas sembarang dalam tenant, sehingga workload apa pun yang memegang managed identity dapat memperoleh token Anthropic yang difederasikan.
</Warning>

Kunci blok `match` pada rule ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Cocokkan `oid` sebagai nilai persis:** Atur `claims.oid` ke object ID lengkap managed identity dan jangan pernah gunakan `subject_prefix` untuk token Entra.
* **Kunci `tid` sebagai lapisan pertahanan tambahan:** URL issuer sudah mengunci tenant Anda, tetapi menambahkan `claims.tid` melindungi dari pergeseran konfigurasi jika record issuer diedit di kemudian hari.
* **Kunci audience:** Atur `audience` ke nilai `aud` persis dari token Anda yang telah di-decode sehingga token yang dibuat untuk aplikasi lain akan ditolak.
* **Gunakan rule terpisah untuk setiap managed identity:** Buat satu rule per identitas alih-alih satu rule yang mengotorisasi beberapa identitas, sehingga Anda dapat mencabut akses satu workload tanpa memengaruhi yang lain.

## Langkah selanjutnya

* Tinjau model konfigurasi lengkap di [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation).
* Lihat [panduan penyedia](/docs/id/manage-claude/workload-identity-federation#identity-providers) untuk AWS, Google Cloud, GitHub Actions, dan Kubernetes.
* Untuk variabel lingkungan, file profil, dan urutan prioritas kredensial, lihat [referensi WIF](/docs/id/manage-claude/wif-reference).
