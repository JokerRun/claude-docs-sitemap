---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/authentication
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 35ff0e1df0e4a382c5c7024d9d9c9beae4c6273e6c2497854c571a29f2444b3c
---

# Autentikasi

Autentikasi ke Claude API dengan kunci API atau Workload Identity Federation.

---

Claude API mendukung dua cara untuk mengautentikasi permintaan:

| Metode | Kredensial | Paling cocok untuk |
|---|---|---|
| [Kunci API](#api-keys) | Rahasia `sk-ant-api...` berumur panjang di header `x-api-key` | Pengembangan lokal, pembuatan prototipe, skrip, dan server single-tenant di mana Anda mengontrol penyimpanan rahasia |
| [Workload Identity Federation](#workload-identity-federation) | Bearer token berumur pendek yang ditukar dari identity token milik identity provider Anda | Workload produksi pada platform cloud (AWS, Google Cloud, Azure), pipeline CI/CD, dan Kubernetes, di mana Anda ingin menghilangkan rahasia statis |

Kedua metode memberikan akses yang sama ke endpoint Claude API. Pilih kunci API untuk memulai dengan cepat, dan beralih ke Workload Identity Federation ketika workload Anda sudah memiliki identitas yang diterbitkan platform yang dapat Anda federasikan.

## Kunci API \{#api-keys}

Kunci API adalah rahasia statis yang Anda buat di Claude Console dan kirimkan pada setiap permintaan.

- **Buat kunci:** Buka [Settings → API keys](https://platform.claude.com/settings/keys) di Claude Console. Gunakan [workspace](https://platform.claude.com/settings/workspaces) untuk membatasi cakupan kunci berdasarkan proyek atau lingkungan.
- **Kirim kunci:** Atur header `x-api-key` pada permintaan HTTP langsung, atau atur variabel lingkungan `ANTHROPIC_API_KEY` dan [SDK klien](/docs/id/cli-sdks-libraries/overview) akan mengambilnya secara otomatis.

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Kunci API tidak memiliki masa kedaluwarsa. Simpan di secrets manager, rotasi secara berkala, dan cabut kunci apa pun yang Anda curigai telah bocor.

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

```python Python hidelines={1..2}
from anthropic import Anthropic

client = Anthropic(api_key="my-anthropic-api-key")
# atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
client = Anthropic()
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: "my-anthropic-api-key" });
// atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
// const client = new Anthropic();
```

```go Go hidelines={1..8,12..13}
package main

import (
	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient(
		option.WithAPIKey("sk-ant-api03-..."), // defaults to os.LookupEnv("ANTHROPIC_API_KEY")
	)
	_ = client
}
```

```java Java nocheck
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

// Eksplisit
AnthropicClient client = AnthropicOkHttpClient.builder()
  .apiKey("my-anthropic-api-key")
  .build();

// Dari ANTHROPIC_API_KEY (atau properti sistem anthropic.apiKey)
AnthropicClient clientFromEnv = AnthropicOkHttpClient.fromEnv();
```

```csharp C#
using Anthropic;

AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
// Atau, dengan ANTHROPIC_API_KEY yang sudah diatur di environment:
// AnthropicClient client = new();
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

// Membaca ANTHROPIC_API_KEY dari environment
$client = new Client();
// Atau berikan kunci secara eksplisit:
$client = new Client(apiKey: 'my-anthropic-api-key');
```

```ruby Ruby hidelines={1..2}
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")
# atau, dengan ANTHROPIC_API_KEY yang diatur di environment:
anthropic = Anthropic::Client.new
```

```bash CLI
# Lihat /docs/en/cli-sdks-libraries/cli/authentication#api-key untuk varian zsh, bash, dan Windows
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

</CodeGroup>

## Workload Identity Federation \{#workload-identity-federation}

"Workload Identity Federation" (federasi identitas workload), atau WIF, memungkinkan workload melakukan autentikasi dengan identity token berumur pendek yang diterbitkan oleh "identity provider" (penyedia identitas), atau IdP, yang sudah Anda percaya, seperti AWS IAM, Google Cloud, atau penerbit OIDC apa pun yang sesuai standar (seperti GitHub Actions, service account Kubernetes, SPIFFE, Microsoft Entra ID, atau Okta). Workload menukar JWT yang diterbitkan IdP-nya di `POST /v1/oauth/token` dengan access token Claude API berumur pendek, dan SDK menyegarkan token tersebut secara otomatis sebelum kedaluwarsa. Tidak ada string `sk-ant-api...` yang perlu dibuat, didistribusikan, atau dirotasi.

Federasi menghilangkan kunci Claude API berumur panjang dari lingkungan Anda, yang memperkecil dampak kebocoran kredensial dan memungkinkan Anda mengelola akses dengan kontrol IdP yang sama yang sudah Anda gunakan untuk sumber daya cloud. Namun, federasi tidak dengan sendirinya menjamin keamanan end-to-end: rantai kepercayaan hanya sekuat konfigurasi identity provider Anda, dan rahasia berumur panjang satu tingkat di hulu (misalnya, kredensial cloud statis yang dapat menerbitkan token IdP) masih dapat melemahkannya. Padukan federasi dengan kontrol dari provider Anda, seperti daftar IP yang diizinkan, MFA, dan audit logging.

Untuk mengonfigurasi federasi, Anda membuat tiga sumber daya di Claude Console (service account, federation issuer, dan federation rule) lalu mengarahkan SDK Anda ke rule tersebut. Lihat [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation) untuk panduan penyiapan lengkap.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Siapkan Workload Identity Federation" icon="lock" href="/docs/id/manage-claude/workload-identity-federation">
    Konfigurasikan issuer, rule, dan service account, lalu tukarkan token
  </Card>
  <Card title="Panduan identity provider" icon="cloud" href="/docs/id/manage-claude/workload-identity-federation#identity-providers">
    Panduan langkah demi langkah untuk AWS, Google Cloud, Azure, GitHub Actions, Kubernetes, SPIFFE, dan Okta
  </Card>
  <Card title="Referensi WIF" icon="book" href="/docs/id/manage-claude/wif-reference">
    Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error
  </Card>
  <Card title="SDK Klien" icon="code" href="/docs/id/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, Ruby, dan CLI
  </Card>
</CardGroup>