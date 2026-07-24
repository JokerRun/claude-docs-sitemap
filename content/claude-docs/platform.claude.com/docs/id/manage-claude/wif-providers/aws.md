---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/aws
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e3489c5271ef03fcbdb67ea640b2724d95ce8ee097d7764f67c1e97ae9b45c0c
---

# Menggunakan WIF dengan AWS

Autentikasi workload AWS di Lambda, EC2, ECS, atau EKS ke Claude API dengan Workload Identity Federation dan token identitas yang diterbitkan STS.

---

Workload AWS dapat melakukan autentikasi ke Claude API tanpa kunci API statis dengan menukarkan token identitas OIDC yang ditandatangani AWS. Jalur yang direkomendasikan memanggil API AWS STS [`GetWebIdentityToken`](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetWebIdentityToken.html), yang berfungsi di mana pun workload memiliki kredensial AWS: Lambda, EC2, ECS, dan EKS. Workload EKS dapat secara alternatif menggunakan [jalur projected-token Kubernetes](#use-eks-projected-service-account-tokens), yang memiliki lebih sedikit langkah konfigurasi tetapi hanya berfungsi di dalam pod.

Panduan ini menunjukkan kedua jalur tersebut. Untuk konsep yang mendasarinya (service account, federation issuer, dan federation rule), lihat [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation).

## Prasyarat

* Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Workload AWS (pod EKS, task ECS, fungsi Lambda, atau instance EC2) dengan IAM role yang terpasang.
* CLI `aws` atau AWS SDK yang tersedia di dalam workload.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

## Menggunakan token web identity STS (direkomendasikan)

API AWS STS `GetWebIdentityToken` mengembalikan token OIDC yang ditandatangani oleh AWS yang menyatakan identitas IAM pemanggil. Karena menggunakan kredensial AWS ambient milik workload, integrasi yang sama mencakup Lambda, EC2, ECS, dan EKS.

### Konfigurasi AWS

<Steps>
  <Step title="Aktifkan outbound web identity federation untuk akun">
    Ini adalah flag tingkat akun, nonaktif secara default. Di konsol AWS, buka **IAM**, pilih **Account settings**, dan aktifkan **Outbound web identity federation**. Untuk mengaktifkannya secara terprogram:

    ```bash
    python3 -c "import boto3; boto3.client('iam').enable_outbound_web_identity_federation()"
    ```

    Jika ini tidak diaktifkan, panggilan ke `GetWebIdentityToken` akan gagal dengan `OutboundWebIdentityFederationDisabledException`.
  </Step>

  <Step title="Berikan izin kepada IAM role workload untuk memanggil API">
    Lampirkan kebijakan ini ke IAM role yang digunakan oleh fungsi Lambda, instance EC2, atau task ECS Anda:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["sts:GetWebIdentityToken"],
          "Resource": "*"
        }
      ]
    }
    ```
  </Step>

  <Step title="Temukan URL issuer STS akun Anda">
    Setelah mengaktifkan outbound federation, halaman **IAM > Account settings** menampilkan bidang **Get Token Issuer URL** dengan nilai dalam bentuk `https://<uuid>.tokens.sts.global.api.aws`. URL ini unik untuk akun AWS Anda; salin untuk langkah berikutnya. Untuk mengambilnya secara terprogram:

    ```bash
    python3 -c "import boto3; print(boto3.client('iam').get_outbound_web_identity_federation_info())"
    ```
  </Step>
</Steps>

### Konfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **AWS**. Wizard akan memandu Anda melalui pendaftaran issuer, pembuatan service account, dan pembuatan federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Daftarkan URL issuer STS per-akun yang Anda salin pada langkah sebelumnya. URL ini mengekspos endpoint JWKS publik, jadi gunakan mode discovery.

```json
{
  "name": "aws-sts",
  "issuer_url": "https://<uuid>.tokens.sts.global.api.aws",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Cocokkan audience yang Anda berikan ke `GetWebIdentityToken` dan ARN IAM role dari role pemanggil dalam klaim `sub`. Nilai `sub` adalah ARN IAM role dari workload yang memanggil API, dalam bentuk `arn:aws:iam::<account>:role/<role-name>`. Token juga membawa klaim `https://sts.amazonaws.com/` dengan `aws_account`, `org_id`, `principal_id`, dan `request_tags` apa pun yang Anda berikan; Anda dapat mencocokkan nilai-nilai tersebut dengan map `claims` pada rule atau `condition` CEL untuk kontrol yang lebih halus.

```json
{
  "name": "prod-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "arn:aws:iam::123456789012:role/inference-worker",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

Buat sespesifik mungkin sesuai yang dimungkinkan oleh workload. Cocokkan ARN role secara persis, dan hanya perluas `subject_prefix` (misalnya, menjadi `arn:aws:iam::123456789012:role/*`) jika beberapa IAM role harus dipetakan ke service account Anthropic yang sama.

### Memperoleh dan menggunakan token

Panggil `GetWebIdentityToken` dengan `https://api.anthropic.com` sebagai audience, lalu berikan hasilnya ke kredensial federasi SDK. Token provider adalah sebuah callable, sehingga SDK memanggil ulang STS pada setiap refresh.

<Note>
  `GetWebIdentityToken` hanya tersedia pada endpoint STS regional. Jika Anda menerima `'STS' object has no attribute 'get_web_identity_token'` atau error serupa, tetapkan klien STS Anda ke sebuah region (misalnya, `boto3.client("sts", region_name="us-east-1")`) dan pastikan AWS SDK Anda cukup baru untuk menyertakan API tersebut.
</Note>

<CodeGroup>
  ```bash cURL
  JWT=$(aws sts get-web-identity-token \
    --region us-east-1 \
    --audience "https://api.anthropic.com" \
    --signing-algorithm RS256 \
    --duration-seconds 900 \
    --query WebIdentityToken --output text)

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

  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from AWS"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  import boto3
  from anthropic import WorkloadIdentityCredentials


  def get_sts_web_identity_token() -> str:
      sts = boto3.client("sts", region_name="us-east-1")
      resp = sts.get_web_identity_token(
          Audience=["https://api.anthropic.com"],
          SigningAlgorithm="RS256",
          DurationSeconds=900,
      )
      return resp["WebIdentityToken"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=get_sts_web_identity_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from AWS"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { STSClient, GetWebIdentityTokenCommand } from "@aws-sdk/client-sts";

  const sts = new STSClient({ region: "us-east-1" });

  async function getStsWebIdentityToken(): Promise<string> {
    const out = await sts.send(
      new GetWebIdentityTokenCommand({
        Audience: ["https://api.anthropic.com"],
        SigningAlgorithm: "RS256",
        DurationSeconds: 900
      })
    );
    return out.WebIdentityToken!;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: getStsWebIdentityToken,
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
    messages: [{ role: "user", content: "Hello from AWS" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  ctx := context.TODO()
  cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1"))
  if err != nil {
  	panic(err)
  }
  stsClient := sts.NewFromConfig(cfg)

  getStsToken := option.IdentityTokenFunc(func(ctx context.Context) (string, error) {
  	out, err := stsClient.GetWebIdentityToken(ctx, &sts.GetWebIdentityTokenInput{
  		Audience:         []string{"https://api.anthropic.com"},
  		SigningAlgorithm: "RS256",
  		DurationSeconds:  aws.Int32(900),
  	})
  	if err != nil {
  		return "", err
  	}
  	return *out.WebIdentityToken, nil
  })

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(getStsToken, option.FederationOptions{
  		FederationRuleID: os.Getenv("ANTHROPIC_FEDERATION_RULE_ID"),
  		OrganizationID:   os.Getenv("ANTHROPIC_ORGANIZATION_ID"),
  		ServiceAccountID: os.Getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
  		WorkspaceID:      os.Getenv("ANTHROPIC_WORKSPACE_ID"),
  	}),
  )

  message, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from AWS")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  StsClient sts = StsClient.builder().region(Region.US_EAST_1).build();

  IdentityTokenProvider getStsToken = () -> sts.getWebIdentityToken(
                  GetWebIdentityTokenRequest.builder()
                          .audience("https://api.anthropic.com")
                          .signingAlgorithm("RS256")
                          .durationSeconds(900)
                          .build())
          .webIdentityToken();

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  getStsToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Hello from AWS")
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
      IdentityTokenProvider = new StsTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from AWS" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class StsTokenProvider : IIdentityTokenProvider
  {
      private readonly AmazonSecurityTokenServiceClient _sts = new(Amazon.RegionEndpoint.USEast1);

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          var resp = await _sts.GetWebIdentityTokenAsync(new GetWebIdentityTokenRequest
          {
              Audience = ["https://api.anthropic.com"],
              SigningAlgorithm = "RS256",
              DurationSeconds = 900,
          }, ct);
          return resp.WebIdentityToken;
      }
  }
  ```

  ```bash CLI
  TOKEN_FILE=$(mktemp)
  aws sts get-web-identity-token \
    --region us-east-1 \
    --audience "https://api.anthropic.com" \
    --signing-algorithm RS256 \
    --duration-seconds 900 \
    --query WebIdentityToken --output text > "$TOKEN_FILE"

  export ANTHROPIC_IDENTITY_TOKEN_FILE="$TOKEN_FILE"
  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID, dan
  # ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID dibaca dari environment
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from AWS"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;
  use Aws\Sts\StsClient;

  $sts = new StsClient(['region' => 'us-east-1', 'version' => 'latest']);
  $client = new Client(credentials: new WorkloadIdentityCredentials(
      identityTokenProvider: fn() => $sts->getWebIdentityToken([
          'Audience' => ['https://api.anthropic.com'],
          'SigningAlgorithm' => 'RS256',
          'DurationSeconds' => 900,
      ])['WebIdentityToken'],
      federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
      organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
      serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
      workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
  ));

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from AWS']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "aws-sdk-sts"

  sts = Aws::STS::Client.new(region: "us-east-1")
  client = Anthropic::Client.new(
    credentials: Anthropic::WorkloadIdentityCredentials.new(
      identity_token_provider: -> {
        sts.get_web_identity_token(
          audience: ["https://api.anthropic.com"],
          signing_algorithm: "RS256",
          duration_seconds: 900,
        ).web_identity_token
      },
      federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
      organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
      service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"],
    ),
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from AWS"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

### Verifikasi pengaturan

Dari dalam workload, tukarkan token yang diterbitkan STS secara langsung dan periksa responsnya:

```bash cURL
JWT=$(aws sts get-web-identity-token \
  --region us-east-1 \
  --audience "https://api.anthropic.com" \
  --signing-algorithm RS256 \
  --duration-seconds 900 \
  --query WebIdentityToken --output text)

curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  -d "{
    \"grant_type\": \"urn:ietf:params:oauth:grant-type:jwt-bearer\",
    \"assertion\": \"$JWT\",
    \"federation_rule_id\": \"fdrl_...\",
    \"organization_id\": \"00000000-0000-0000-0000-000000000000\",
    \"service_account_id\": \"svac_...\",
    \"workspace_id\": \"wrkspc_...\"
  }" | jq
```

Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum di sisi AWS adalah ketidakcocokan `iss` (URL issuer STS per-akun harus sama persis dengan `issuer_url` yang terdaftar).

## Menggunakan token service-account terproyeksi EKS

Jika workload Anda berjalan di pod EKS, Anda dapat melewati panggilan STS dan membaca token service-account yang diproyeksikan Kubernetes langsung dari disk. Kubernetes secara native memproyeksikan token yang kompatibel dengan OIDC ke dalam pod, dan SDK dapat membacanya dari path file, sehingga tidak diperlukan callable token-provider. Jalur ini memiliki dua langkah konfigurasi AWS lebih sedikit dibandingkan jalur STS tetapi hanya berfungsi di dalam pod; mekanisme yang mendasarinya sama dengan [integrasi Kubernetes generik](/docs/id/manage-claude/wif-providers/kubernetes).

Jalur ini juga memerlukan klaster EKS dengan [IAM OIDC provider yang diaktifkan](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) dan akses `kubectl` ke klaster tersebut.

### Konfigurasi klaster EKS Anda

<Steps>
  <Step title="Temukan URL issuer OIDC klaster Anda">
    Setiap klaster EKS memiliki issuer OIDC yang unik. Ambil dengan AWS CLI:

    ```bash CLI
    aws eks describe-cluster \
      --name <cluster-name> \
      --query "cluster.identity.oidc.issuer" \
      --output text
    ```

    Output-nya terlihat seperti `https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...`. Anda akan mendaftarkan URL ini sebagai federation issuer di bagian berikutnya.
  </Step>

  <Step title="Buat service account dan proyeksikan token dengan audience Anthropic">
    Webhook pod identity EKS mendeteksi anotasi `eks.amazonaws.com/role-arn` dan secara otomatis memproyeksikan token dengan `aud: sts.amazonaws.com`, mengekspos path-nya sebagai `AWS_WEB_IDENTITY_TOKEN_FILE`. Token tersebut digunakan untuk asumsi role AWS. Untuk pertukaran Anthropic, proyeksikan token kedua dengan `audience: https://api.anthropic.com` dan pasang di path khusus.

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: inference-worker
      namespace: inference
      annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/inference-worker
    ```

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: inference-worker
      namespace: inference
    spec:
      serviceAccountName: inference-worker
      volumes:
        - name: anthropic-token
          projected:
            sources:
              - serviceAccountToken:
                  audience: https://api.anthropic.com
                  expirationSeconds: 3600
                  path: token
      containers:
        - name: app
          image: your-registry/inference-worker:latest
          env:
            - name: ANTHROPIC_IDENTITY_TOKEN_FILE
              value: /var/run/secrets/anthropic.com/token
            - name: ANTHROPIC_FEDERATION_RULE_ID
              value: fdrl_...
            - name: ANTHROPIC_ORGANIZATION_ID
              value: 00000000-0000-0000-0000-000000000000
            - name: ANTHROPIC_SERVICE_ACCOUNT_ID
              value: svac_...
            - name: ANTHROPIC_WORKSPACE_ID  # required when the rule covers multiple workspaces
              value: wrkspc_...
          volumeMounts:
            - name: anthropic-token
              mountPath: /var/run/secrets/anthropic.com
              readOnly: true
    ```
  </Step>

  <Step title="Perhatikan bentuk klaim token">
    Token yang diproyeksikan adalah JSON Web Token (JWT) yang ditandatangani oleh issuer OIDC klaster Anda. Klaim `sub`-nya mengikuti konvensi Kubernetes `system:serviceaccount:<namespace>:<service-account-name>`:

    ```json
    {
      "iss": "https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...",
      "sub": "system:serviceaccount:inference:inference-worker",
      "aud": ["https://api.anthropic.com"],
      "kubernetes.io": {
        "namespace": "inference",
        "serviceaccount": { "name": "inference-worker", "uid": "..." }
      },
      "exp": 1775527120,
      "iat": 1775523520
    }
    ```

    Proyeksi `serviceAccountToken` menetapkan `aud` ke `https://api.anthropic.com`. Token terpisah yang diinjeksikan IRSA di `AWS_WEB_IDENTITY_TOKEN_FILE` membawa `aud: sts.amazonaws.com` dan digunakan untuk panggilan API AWS, bukan untuk pertukaran ini.
  </Step>
</Steps>

### Konfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **AWS**. Wizard akan memandu Anda melalui pendaftaran issuer, pembuatan service account, dan pembuatan federation rule.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Issuer EKS mengekspos endpoint JWKS publik, jadi gunakan mode discovery. URL issuer harus sama persis dengan klaim `iss` pada token. Daftarkan satu issuer per klaster.

```json
{
  "name": "prod-eks-uswest2",
  "issuer_url": "https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Cocokkan klaim `sub` Kubernetes dan audience Anthropic `https://api.anthropic.com`. (Proyeksikan token service-account khusus dengan audience tersebut; jangan gunakan kembali token default IRSA `sts.amazonaws.com`.)

```json
{
  "name": "prod-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "system:serviceaccount:inference:inference-worker",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

Buat sespesifik mungkin sesuai yang dimungkinkan oleh workload. Longgarkan `subject_prefix` menjadi `system:serviceaccount:inference:*` (tanda `*` di akhir menjadikannya pencocokan prefix) hanya jika setiap service account di namespace tersebut harus dipetakan ke service account Anthropic yang sama.

### Memperoleh dan menggunakan token

Di dalam pod, token yang diproyeksikan berada di `/var/run/secrets/anthropic.com/token` (diekspos sebagai `ANTHROPIC_IDENTITY_TOKEN_FILE` dalam spesifikasi Pod). Berikan file tersebut ke kredensial federasi SDK dan SDK akan menangani pertukaran dan refresh.

<CodeGroup>
  ```bash cURL
  JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

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

  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from EKS"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  from anthropic import IdentityTokenFile, WorkloadIdentityCredentials

  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=IdentityTokenFile(
              os.environ["ANTHROPIC_IDENTITY_TOKEN_FILE"]
          ),
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from EKS"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { identityTokenFromFile } from "@anthropic-ai/sdk/lib/credentials/identity-token";

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: identityTokenFromFile(process.env.ANTHROPIC_IDENTITY_TOKEN_FILE!),
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
    messages: [{ role: "user", content: "Hello from EKS" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  tokenPath := os.Getenv("ANTHROPIC_IDENTITY_TOKEN_FILE")

  readToken := option.IdentityTokenFunc(func(ctx context.Context) (string, error) {
  	raw, err := os.ReadFile(tokenPath)
  	if err != nil {
  		return "", fmt.Errorf("read identity token: %w", err)
  	}
  	return string(raw), nil
  })

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(readToken, option.FederationOptions{
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from EKS")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Hello from EKS")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var result = AnthropicCredentials.Resolve()
      ?? throw new InvalidOperationException("No federation credentials found in environment");
  using var client = new AnthropicOidcClient(result);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from EKS" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```bash CLI
  # Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from EKS"}'
  ```

  ```php PHP
  use Anthropic\Client;

  // Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from EKS']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  # Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from EKS"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

<Tip>
  Spesifikasi Pod sudah menetapkan `ANTHROPIC_IDENTITY_TOKEN_FILE`, `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan `ANTHROPIC_WORKSPACE_ID`, sehingga Anda dapat membuat klien tanpa argumen dan SDK akan membaca variabel lingkungan federasi secara otomatis.
</Tip>

### Verifikasi pengaturan

Dari dalam pod, tukarkan token yang diproyeksikan secara langsung dan periksa responsnya:

```bash cURL
JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  -d "{
    \"grant_type\": \"urn:ietf:params:oauth:grant-type:jwt-bearer\",
    \"assertion\": \"$JWT\",
    \"federation_rule_id\": \"$ANTHROPIC_FEDERATION_RULE_ID\",
    \"organization_id\": \"$ANTHROPIC_ORGANIZATION_ID\",
    \"service_account_id\": \"$ANTHROPIC_SERVICE_ACCOUNT_ID\",
    \"workspace_id\": \"$ANTHROPIC_WORKSPACE_ID\"
  }" | jq
```

Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum di sisi EKS adalah `aud` pada token yang diproyeksikan tidak cocok dengan rule (proyeksikan token dengan `audience: https://api.anthropic.com`, bukan default IRSA `sts.amazonaws.com`).

## Batasi cakupan rule Anda

<Warning>
  `subject_prefix` dengan nilai `arn:aws:iam::123456789012:role/*` cocok dengan setiap IAM role di akun tersebut. Principal mana pun yang dapat mengasumsikan role yang cocok dapat memperoleh token Anthropic terfederasi.
</Warning>

Kunci blok `match` pada rule ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Tetapkan ARN role lengkap:** Gunakan `subject_prefix: "arn:aws:iam::<account>:role/<role-name>"` tanpa `*` di akhir sehingga role lain di akun tersebut tidak cocok.
* **Tetapkan ID akun:** Cocokkan bidang `aws_account` dari klaim `https://sts.amazonaws.com/` pada token dengan map `claims` atau `condition` CEL sebagai pemeriksaan defense-in-depth terhadap prefix yang salah konfigurasi.
* **Tetapkan namespace dan service account di EKS:** Gunakan nilai `system:serviceaccount:<namespace>:<name>` yang persis tanpa `*` setelah prefix `system:serviceaccount:`.
* **Gunakan rule terpisah per lingkungan:** Buat rule yang berbeda untuk workload produksi, staging, dan pengembangan alih-alih memperluas satu prefix untuk mencakup semuanya.

## Langkah selanjutnya

* Tinjau [referensi WIF](/docs/id/manage-claude/wif-reference) untuk referensi lengkap tentang urutan prioritas kredensial, konfigurasi profil, dan pencocokan rule.
* Untuk klaster Kubernetes yang dikelola sendiri dan tidak berada di EKS, lihat [Menggunakan WIF dengan Kubernetes](/docs/id/manage-claude/wif-providers/kubernetes).
