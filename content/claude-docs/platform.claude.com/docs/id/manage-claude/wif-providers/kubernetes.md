---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/kubernetes
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: b936f271a066448cf057b415b49025c548f6825e30b303bfaa6b726be8caebb5
---

# Menggunakan WIF dengan Kubernetes

Autentikasi ke Claude API dari klaster Kubernetes yang dikelola sendiri menggunakan projected service account token.

---

Klaster Kubernetes yang dikelola sendiri (kubeadm, k3s, OpenShift, dan distribusi on-premises) menandatangani OIDC JSON Web Token (JWT) untuk setiap pod melalui [projected service account token](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection). API server klaster bertindak sebagai OIDC issuer, dan klaim `sub` pada setiap token mengikuti format `system:serviceaccount:<namespace>:<service-account>`. Anda dapat menemukan URL issuer klaster Anda dengan membaca dokumen discovery-nya:

```bash cURL nocheck
kubectl get --raw /.well-known/openid-configuration | jq -r .issuer
```

<Note>
Mekanisme pada halaman ini (projected service-account token, API server klaster sebagai OIDC issuer) adalah bawaan Kubernetes itu sendiri, sehingga mendasari setiap distribusi Kubernetes. Jika Anda menjalankan layanan Kubernetes terkelola, panduan penyedia cloud menjelaskan di mana menemukan URL issuer yang dikelola penyedia: [AWS (EKS)](/docs/id/manage-claude/wif-providers/aws#use-eks-projected-service-account-tokens), [Google Cloud (GKE)](/docs/id/manage-claude/wif-providers/gcp), atau [Azure (AKS)](/docs/id/manage-claude/wif-providers/azure). Jika klaster Anda menjalankan SPIRE, SPIRE OIDC Discovery Provider adalah issuer-nya, bukan API server klaster; lihat [SPIFFE](/docs/id/manage-claude/wif-providers/spiffe). Untuk distribusi lain atau penyedia terkelola yang tidak tercantum di sana, ikuti panduan ini dan gunakan URL issuer yang dilaporkan klaster Anda.
</Note>

## Prasyarat \{#prerequisites}

- Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
- Klaster Kubernetes dengan flag [`--service-account-issuer`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) yang dikonfigurasi pada API server. Sebagian besar distribusi mengatur ini secara default; klaster kubeadm biasanya menggunakan `https://kubernetes.default.svc.cluster.local`. Tim platform Anda dapat mengonfirmasi nilainya jika Anda tidak memiliki akses langsung ke konfigurasi API server.
- Salah satu dari berikut ini agar Anthropic dapat memvalidasi tanda tangan token:
  - Endpoint JWKS issuer dapat dijangkau dari internet publik melalui HTTPS pada port 443, atau
  - Anda dapat mengambil JWKS dari dalam klaster dan mendaftarkannya dalam mode `inline` (dibahas di [Konfigurasi Anthropic](#configure-anthropic)).
- Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

## Konfigurasi Kubernetes \{#configure-kubernetes}

Proyeksikan service account token ke dalam pod Anda dengan audience dan masa berlaku yang diharapkan oleh federation rule Anda. Proyeksi `serviceAccountToken` menulis JWT baru ke mount path dan merotasinya sebelum `expirationSeconds` berlalu.

```yaml Pod nocheck
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

Token yang diterbitkan untuk pod ini membawa `sub: "system:serviceaccount:inference:inference-worker"` dan `aud: ["https://api.anthropic.com"]`.

## Konfigurasi Anthropic \{#configure-anthropic}

Ikuti [panduan penyiapan](/docs/id/manage-claude/workload-identity-federation#set-up-federation) untuk mendaftarkan federation issuer, membuat service account Anthropic, dan membuat federation rule di Claude Console. Gunakan nilai-nilai khusus Kubernetes berikut.

**Federation issuer:** Banyak klaster yang dikelola sendiri menggunakan URL issuer seperti `https://kubernetes.default.svc.cluster.local` yang tidak dapat dijangkau dari internet publik. Jika hal itu berlaku untuk klaster Anda, pilih sumber JWKS **inline** dan tempelkan kunci klaster. Ambil kunci tersebut dari dalam klaster:

```bash cURL nocheck
kubectl get --raw /openid/v1/jwks
```

Kemudian konfigurasikan issuer dengan isi array `keys` yang dikembalikan (bukan pembungkus `{"keys": [...]}` di sekitarnya):

```json
{
  "name": "onprem-k8s",
  "issuer_url": "https://kubernetes.default.svc.cluster.local",
  "jwks_source": "inline",
  "jwks_keys": [{ "kty": "RSA", "kid": "...", "n": "...", "e": "AQAB" }]
}
```

Dalam mode `inline`, `issuer_url` hanya dibandingkan dengan klaim `iss` pada JWT; Anthropic tidak pernah mencoba menjangkaunya. Jika issuer Anda dapat dijangkau secara publik, gunakan `"jwks_source": "discovery"` sebagai gantinya dan hilangkan `jwks_keys`.

<Warning>
Dengan kunci `inline`, Anda bertanggung jawab untuk memperbarui issuer ketika klaster merotasi kunci penandatanganan service account-nya. Rotasi jarang terjadi (biasanya hanya selama upgrade klaster), tetapi pertukaran token akan gagal dengan error tanda tangan sampai Anda mengirimkan JWKS yang baru.
</Warning>

**Federation rule:** Cocokkan klaim `sub` service account dan audience yang Anda tetapkan pada projected token.

```json
{
  "name": "onprem-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "system:serviceaccount:inference:inference-worker",
    "audience": "https://api.anthropic.com"
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

Buat sespesifik mungkin sesuai yang diizinkan workload. Longgarkan `subject_prefix` menjadi `system:serviceaccount:inference:*` (tanda `*` di akhir menjadikannya pencocokan prefiks) hanya jika setiap service account di namespace tersebut harus dipetakan ke service account Anthropic yang sama. Tambahkan ID `fdrl_...` dari rule tersebut ke variabel lingkungan `ANTHROPIC_FEDERATION_RULE_ID` pada pod Anda.

## Memperoleh dan menggunakan token \{#acquire-and-use-the-token}

Spesifikasi pod di [Konfigurasi Kubernetes](#configure-kubernetes) menetapkan `ANTHROPIC_IDENTITY_TOKEN_FILE` ke mount path yang diproyeksikan, bersama dengan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan `ANTHROPIC_WORKSPACE_ID`. Dengan semua itu tersedia, SDK membaca token dari disk pada setiap pertukaran dan menyegarkan access token Anthropic secara otomatis.

<CodeGroup>

```bash cURL nocheck
JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  --data @- <<JSON | jq -r .access_token
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

curl https://api.anthropic.com/v1/messages \
  -H "authorization: Bearer $ACCESS_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }' | jq -r '.content[0].text'
```

```python Python nocheck
import anthropic

# Membaca ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
# ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID
# dari environment pod.
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(message.content[0].text)
```

```typescript TypeScript nocheck
import Anthropic from "@anthropic-ai/sdk";

// Membaca ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
// ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID
// dari lingkungan pod.
const client = new Anthropic();

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

```go Go nocheck hidelines={1..10,-1}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	// Membaca ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
	// ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID
	// dari environment pod.
	client := anthropic.NewClient()

	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
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

```java Java nocheck hidelines={1..6,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

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

var result = AnthropicCredentials.Resolve()
    ?? throw new InvalidOperationException("No federation credentials found in environment");
using var client = new AnthropicOidcClient(result);

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

```bash CLI nocheck
# Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
# ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
ant messages create \
  --model claude-sonnet-4-6 \
  --max-tokens 1024 \
  --message '{role: user, content: "Hello, Claude"}'
```

```php PHP nocheck hidelines={1..3}
<?php
require 'vendor/autoload.php';

use Anthropic\Client;

// Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
// ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
$client = new Client();

$message = $client->messages->create(
    model: 'claude-sonnet-4-6',
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
);
echo $message->content[0]->text, PHP_EOL;
```

```ruby Ruby nocheck
require "anthropic"

# Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
# ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}]
)
puts message.content.first.text
```

</CodeGroup>

## Verifikasi penyiapan \{#verify-the-setup}

Pertukaran yang berhasil mengembalikan `access_token` yang dimulai dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum dari sisi Kubernetes adalah ketidakcocokan kunci JWKS (untuk mode `inline`, ambil ulang dengan `kubectl get --raw /openid/v1/jwks` dan perbarui issuer).

## Batasi cakupan rule Anda \{#scope-your-rule}

<Warning>
`subject_prefix` dengan nilai `system:serviceaccount:*` mencocokkan setiap service account di klaster, sehingga pod mana pun dapat memperoleh token Anthropic terfederasi. Tanpa matcher `audience`, rule tersebut juga mencocokkan token dengan audience default klaster, yang sudah diproyeksikan ke setiap pod.
</Warning>

Kunci blok `match` pada rule ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

- **Tetapkan namespace dan nama service-account secara spesifik:** Gunakan nilai lengkap `system:serviceaccount:<namespace>:<name>` tanpa `*` di akhir.
- **Selalu tetapkan audience:** Wajibkan `audience` pada rule dan tetapkan nilai yang sama pada proyeksi `serviceAccountToken` pod sehingga token dengan audience default ditolak.
- **Gunakan rule terpisah per namespace:** Buat rule dan service account Anthropic yang berbeda untuk setiap namespace daripada memperluas satu rule.
- **Batasi cakupan issuer inline-JWKS ke satu klaster:** Ketika beberapa klaster berbagi URL issuer yang sama, daftarkan JWKS setiap klaster sebagai federation issuer tersendiri dan ikat rule hanya ke issuer tersebut.

## Langkah selanjutnya \{#next-steps}

- [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation): konsep, alur token-exchange, dan opsi konfigurasi SDK.
- [Referensi WIF](/docs/id/manage-claude/wif-reference): variabel lingkungan, mode sumber JWKS, dan mode pencocokan rule.