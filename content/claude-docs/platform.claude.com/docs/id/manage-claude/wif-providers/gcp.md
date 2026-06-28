---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/gcp
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 767f6774c0502fa9951f05b50d2447bd51084a497d3e1218a7d28f4dbf78cd53
---

# Menggunakan WIF dengan Google Cloud

Federasikan workload Google Cloud (Cloud Run, Cloud Functions, App Engine, GCE, GKE) ke Claude API menggunakan token identitas yang ditandatangani Google alih-alih kunci API statis.

---

Setiap lingkungan komputasi Google Cloud yang memiliki akses ke server metadata instance (Cloud Run, Cloud Functions, App Engine, Compute Engine (GCE), dan GKE dengan Workload Identity) dapat meminta token identitas yang ditandatangani Google untuk service account yang terpasang padanya. Issuer token tersebut adalah `https://accounts.google.com`, dan Anthropic dapat memvalidasinya secara langsung melalui OIDC discovery standar, tanpa memerlukan konfigurasi Google Cloud tambahan.

Panduan ini menunjukkan cara mendaftarkan issuer Google ke Anthropic, mengikat service account Google ke service account Anthropic, dan membuat workload Anda menukar token identitasnya dengan access token Claude API berumur pendek.

## Prasyarat

* Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Proyek Google Cloud dengan workload yang berjalan di Cloud Run, Cloud Functions, App Engine, Compute Engine, atau GKE.
* Service account Google yang dikelola pengguna dan terpasang pada workload tersebut (bukan service account default Compute Engine).
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

## Mengonfigurasi Google Cloud

Google menerbitkan token identitas secara otomatis ke setiap workload yang memiliki service account terpasang. Tidak ada yang perlu diaktifkan di sisi Google selain memasang service account yang tepat, tetapi langkah-langkahnya sedikit berbeda antara komputasi standar dan GKE.

<Tabs>
  <Tab title="Cloud Run, Cloud Functions, App Engine, GCE">
    Pasang service account khusus ke layanan atau instance Anda:

    ```bash CLI
    gcloud run deploy my-service \
      --service-account inference-worker@my-project.iam.gserviceaccount.com
    ```

    Di dalam workload, server metadata mengembalikan token identitas yang ditandatangani sesuai permintaan. Minta token tersebut dengan `audience` yang ingin Anda daftarkan di sisi Anthropic, dan sertakan `format=full` agar respons menyertakan klaim `email`:

    ```text wrap
    GET http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full
    Metadata-Flavor: Google
    ```

    Atau, dengan gcloud CLI:

    ```bash CLI
    gcloud auth print-identity-token \
      --audiences="https://api.anthropic.com" \
      --include-email
    ```

    Padanan SDK ditunjukkan di [Memperoleh dan menggunakan token](#acquire-and-use-the-token).

    Payload token yang telah didekode terlihat seperti ini:

    ```json
    {
      "iss": "https://accounts.google.com",
      "aud": "https://api.anthropic.com",
      "sub": "104892...",
      "azp": "104892...",
      "email": "inference-worker@my-project.iam.gserviceaccount.com",
      "email_verified": true,
      "exp": 1775527120
    }
    ```

    Klaim `sub` adalah ID unik numerik opaque dari service account Google. Klaim `email` adalah alamat service account yang dapat dibaca manusia. Cocokkan pada `sub` dan `email` sekaligus dalam federation rule Anda.
  </Tab>

  <Tab title="GKE dengan Workload Identity">
    Aktifkan [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) pada cluster Anda dan ikat service account Kubernetes Anda ke service account Google dengan anotasi `iam.gke.io/gcp-service-account`:

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: inference-worker
      namespace: prod
      annotations:
        iam.gke.io/gcp-service-account: inference-worker@my-project.iam.gserviceaccount.com
    ```

    Dengan pengikatan ini, server metadata GKE mengembalikan token yang ditandatangani Google yang identik dengan kasus Cloud Run dan GCE: issuer `https://accounts.google.com` yang sama, klaim `email` yang sama, URL pengambilan yang sama. Konfigurasikan Anthropic persis seperti di bagian berikutnya.

    Token `format=full` dari GKE juga menyertakan klaim `google.compute_engine.project_id`, `google.compute_engine.zone`, dan `google.compute_engine.instance_name`, yang dapat Anda rujuk dalam matcher `condition` pada federation rule (ekspresi CEL seperti `claims.google.compute_engine.project_id == "my-project"`) untuk membatasi akses ke cluster atau node pool tertentu.

    <Note>
      Jika Anda tidak ingin mengikat service account Kubernetes ke service account Google, pod GKE dapat menggunakan issuer OIDC milik cluster itu sendiri (`https://container.googleapis.com/v1/projects/PROJECT/locations/REGION/clusters/CLUSTER`) dengan volume `serviceAccountToken` yang diproyeksikan. Jalur tersebut menggunakan issuer per-cluster alih-alih `accounts.google.com`. Lihat [Menggunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes) untuk pola tersebut.
    </Note>
  </Tab>
</Tabs>

## Mengonfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **Google Cloud**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Google memublikasikan dokumen OIDC discovery-nya secara publik, jadi gunakan mode discovery. Satu issuer ini mencakup setiap permukaan Google Cloud (Cloud Run, GCE, Cloud Functions, App Engine, dan GKE dengan Workload Identity). Bedakan workload dengan rule, bukan issuer.

```json
{
  "name": "gcp",
  "issuer_url": "https://accounts.google.com",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Cocokkan pada klaim `sub` dan `email` sekaligus. `email` adalah alamat service account yang dapat dibaca; `sub` adalah ID unik numerik service account, yang tidak pernah digunakan kembali oleh Google, sehingga menyematkannya melindungi rule jika service account dihapus dan yang baru kemudian dibuat dengan email yang sama. Temukan ID unik dengan `gcloud iam service-accounts describe SA_EMAIL --format='value(uniqueId)'`.

```json
{
  "name": "gcp-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "audience": "https://api.anthropic.com",
    "claims": {
      "sub": "104892101234567890123",
      "email": "inference-worker@my-project.iam.gserviceaccount.com"
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

Di dalam workload Google Cloud Anda, ambil token identitas dari server metadata, tukarkan di `POST /v1/oauth/token`, dan gunakan bearer token yang dikembalikan untuk memanggil Claude API. Setiap SDK Anthropic menangani pertukaran dan loop refresh untuk Anda ketika Anda menyediakan callable token-provider yang mengembalikan token identitas baru dari server metadata, seperti yang ditunjukkan dalam contoh berikut.

<CodeGroup>
  ```bash cURL
  # Ambil token identitas yang ditandatangani Google dari server metadata
  JWT=$(curl -sS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full")

  # Tukarkan dengan token akses Anthropic
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    --data @- <<JSON
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$JWT",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )
  ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r .access_token)

  # Panggil API Claude
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from Cloud Run"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os
  import anthropic
  import google.auth.transport.requests
  import google.oauth2.id_token
  from anthropic import WorkloadIdentityCredentials

  AUDIENCE = "https://api.anthropic.com"


  def fetch_google_identity_token() -> str:
      request = google.auth.transport.requests.Request()
      return google.oauth2.id_token.fetch_id_token(request, AUDIENCE)


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_google_identity_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from Cloud Run"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";

  const METADATA_URL =
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full";

  async function fetchGoogleIdentityToken(): Promise<string> {
    const response = await fetch(METADATA_URL, {
      headers: { "Metadata-Flavor": "Google" }
    });
    return response.text();
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchGoogleIdentityToken,
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
    messages: [{ role: "user", content: "Hello from Cloud Run" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  const audience = "https://api.anthropic.com"

  googleIDToken := func(ctx context.Context) (string, error) {
  	creds, err := idtoken.NewCredentials(&idtoken.Options{Audience: audience})
  	if err != nil {
  		return "", err
  	}
  	tok, err := creds.Token(ctx)
  	if err != nil {
  		return "", err
  	}
  	return tok.Value, nil
  }

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(googleIDToken, option.FederationOptions{
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from Cloud Run")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  HttpClient http = HttpClient.newHttpClient();
  HttpRequest metadataRequest = HttpRequest.newBuilder()
          .uri(URI.create("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full"))
          .header("Metadata-Flavor", "Google")
          .build();

  IdentityTokenProvider fetchGoogleIdentityToken = () -> {
      try {
          return http.send(metadataRequest, HttpResponse.BodyHandlers.ofString()).body();
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  };

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  fetchGoogleIdentityToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(1024)
          .addUserMessage("Hello from Cloud Run")
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
      IdentityTokenProvider = new MetadataTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from Cloud Run" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class MetadataTokenProvider : IIdentityTokenProvider
  {
      private const string METADATA_URL =
          "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full";

      private static readonly HttpClient httpClient = new()
      {
          DefaultRequestHeaders = { { "Metadata-Flavor", "Google" } },
      };

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          return await httpClient.GetStringAsync(METADATA_URL, ct);
      }
  }
  ```

  ```bash CLI
  # Tulis token identitas yang ditandatangani Google ke file yang dapat dibaca CLI
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full" \
    > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID, dan
  # ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca dari environment.
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Cloud Run"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  const METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full';

  $context = stream_context_create([
      'http' => ['header' => "Metadata-Flavor: Google\r\n"],
  ]);

  $credentials = new WorkloadIdentityCredentials(
      identityTokenProvider: fn() => file_get_contents(METADATA_URL, false, $context),
      federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
      organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
      serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
      workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
  );
  $client = new Client(credentials: $credentials);

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from Cloud Run']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "net/http"

  METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full"

  credentials = Anthropic::WorkloadIdentityCredentials.new(
    identity_token_provider: -> { Net::HTTP.get(URI(METADATA_URL), {"Metadata-Flavor" => "Google"}) },
    federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
    organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
    service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
    workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
  )
  client = Anthropic::Client.new(credentials: credentials)

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Cloud Run"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

Token identitas Google kedaluwarsa setelah kira-kira satu jam. SDK akan memanggil ulang token provider dan menukar ulang secara otomatis sebelum kedaluwarsa. Untuk skrip shell yang berjalan lebih lama dari `expires_in` access token, lakukan refresh dengan timer dan ulangi pertukaran.

## Memverifikasi penyiapan

Dari dalam workload Anda, dekode token identitas dan konfirmasikan bahwa klaim cocok dengan rule Anda:

```bash cURL
curl -sS -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full" \
  | jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson'
```

Periksa bahwa `iss` adalah `https://accounts.google.com`, `aud` adalah `https://api.anthropic.com`, dan `email` cocok dengan nilai dalam federation rule Anda. Kemudian jalankan pertukaran dari bagian sebelumnya. Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum di sisi Google Cloud adalah klaim `email` yang hilang (minta token dengan `format=full` agar klaim tersebut disertakan).

## Membatasi cakupan rule Anda

<Warning>
  Klaim `sub` Google adalah ID unik numerik opaque dari service account dan tidak memiliki prefiks yang stabil. `subject_prefix` dengan akhiran `*` akan cocok dengan service account sembarang di setiap proyek Google Cloud, dan salah satu dari mereka dapat memperoleh token Anthropic terfederasi.
</Warning>

Kunci blok `match` pada rule ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Cocokkan `sub` secara persis:** Tetapkan ID unik numerik lengkap di `claims.sub` dan jangan pernah gunakan `subject_prefix` untuk token Google.
* **Sematkan klaim `email`:** Tambahkan `claims.email` di samping `sub` sehingga ID stabil dan alamat yang dapat dibaca harus cocok keduanya.
* **Sematkan audience:** Tetapkan `audience` ke nilai persis yang Anda minta dari server metadata sehingga token yang dibuat untuk konsumen lain ditolak.
* **Sematkan proyek pada GKE:** Untuk token `format=full`, tambahkan `condition` seperti `claims.google.compute_engine.project_id == "my-project"` untuk membatasi rule ke node dari satu proyek.

## Langkah selanjutnya

* Baca halaman [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) untuk model resource lengkap dan urutan prioritas kredensial SDK.
* Tambahkan federation rule terpisah per lingkungan (produksi, staging) sehingga Anda dapat mencabut salah satunya tanpa memengaruhi yang lain.
