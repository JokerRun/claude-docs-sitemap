---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 9a2278d848fb49597b08670a730e86a7626019b7265cccce0a069634f04c19f0
---

# Menggunakan WIF dengan GitHub Actions

Autentikasi alur kerja GitHub Actions ke Claude API dengan token identitas berumur pendek alih-alih kunci API berumur panjang.

---

Setiap eksekusi alur kerja GitHub Actions dapat meminta token identitas yang ditandatangani dari issuer yang di-host GitHub di `https://token.actions.githubusercontent.com`. Dengan Workload Identity Federation, alur kerja Anda menukar token tersebut dengan token akses Anthropic berumur pendek, sehingga job CI Anda dapat memanggil Claude API tanpa secret `ANTHROPIC_API_KEY` yang disimpan di repositori Anda.

Klaim `sub` pada token mengenkode repositori dan konteks pemicu. Untuk push ke sebuah branch, klaim ini memiliki bentuk `repo:<owner>/<repo>:ref:refs/heads/<branch>`. Eksekusi pull-request menggunakan `repo:<owner>/<repo>:pull_request`, dan deployment yang dibatasi environment menggunakan `repo:<owner>/<repo>:environment:<name>`. Aturan federasi Anda mencocokkan terhadap klaim ini (dan klaim lainnya, seperti `repository_owner` dan `ref`) untuk menentukan eksekusi alur kerja mana yang diizinkan untuk melakukan autentikasi.

## Prasyarat \{#prerequisites}

- Pemahaman tentang [konsep WIF](/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
- Repositori GitHub tempat Anda dapat mengedit file alur kerja dan memberikan izin `id-token: write`.
- Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.
- ID organisasi Anthropic Anda. Anda dapat menemukannya di Claude Console pada **Settings → Organization**.

## Mengonfigurasi alur kerja Anda \{#configure-your-workflow}

GitHub hanya menerbitkan token identitas untuk job yang secara eksplisit memintanya. Tambahkan izin `id-token: write` di tingkat alur kerja atau job:

```yaml
permissions:
  id-token: write
  contents: read
```

Di dalam job, runner mengekspos dua variabel lingkungan: `ACTIONS_ID_TOKEN_REQUEST_URL` dan `ACTIONS_ID_TOKEN_REQUEST_TOKEN`. Panggil URL permintaan dengan token permintaan sebagai kredensial bearer dan audience pilihan Anda sebagai parameter kueri, lalu tulis JSON Web Token (JWT) yang dikembalikan ke sebuah file:

```yaml nocheck
- name: Fetch GitHub OIDC token
  run: |
    curl -sS -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
      "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=https://api.anthropic.com" \
      | jq -r .value > /tmp/gha-jwt
```

Jika Anda lebih memilih JavaScript, `actions/github-script` mengekspos kemampuan yang sama melalui `core.getIDToken(audience)`:

```yaml nocheck
- name: Fetch GitHub OIDC token
  uses: actions/github-script@v8
  with:
    script: |
      const fs = require('fs');
      const token = await core.getIDToken('https://api.anthropic.com');
      fs.writeFileSync('/tmp/gha-jwt', token);
```

Token yang telah didekode membawa klaim yang mendeskripsikan eksekusi alur kerja. Aturan federasi Anda mencocokkan terhadap klaim-klaim ini:

```json
{
  "iss": "https://token.actions.githubusercontent.com",
  "sub": "repo:your-org/your-repo:ref:refs/heads/main",
  "aud": "https://api.anthropic.com",
  "repository": "your-org/your-repo",
  "repository_owner": "your-org",
  "ref": "refs/heads/main",
  "sha": "abc123...",
  "workflow": "CI",
  "actor": "octocat",
  "event_name": "push"
}
```

Lihat [referensi klaim subjek OIDC GitHub](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims) untuk daftar lengkap format `sub`.

## Mengonfigurasi Anthropic \{#configure-anthropic}

Ikuti [panduan penyiapan](/docs/id/manage-claude/workload-identity-federation#set-up-federation) untuk mendaftarkan federation issuer, membuat service account Anthropic, dan membuat federation rule di Claude Console. Gunakan nilai-nilai khusus GitHub Actions berikut.

**Federation issuer:** GitHub memublikasikan dokumen OIDC discovery dan JWKS-nya secara publik, jadi gunakan mode discovery. Anthropic menyegarkan kunci secara otomatis ketika GitHub merotasinya.

```json
{
  "name": "github-actions",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks_source": "discovery"
}
```

**Federation rule:** Cocokkan hanya eksekusi alur kerja yang ingin Anda percaya. Lihat [Membatasi alur kerja mana yang dapat melakukan autentikasi](#membatasi-alur-kerja-mana-yang-dapat-melakukan-autentikasi) untuk cara membatasi cakupan klaim ini dengan aman.

```json
{
  "name": "gha-main",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "repo:your-org/your-repo:ref:refs/heads/main",
    "audience": "https://api.anthropic.com",
    "claims": {
      "repository_owner": "your-org"
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

Buat sespesifik mungkin sesuai yang diizinkan oleh workload. Longgarkan `subject_prefix` menjadi `repo:your-org/your-repo:*` (dipasangkan dengan batasan `claims.ref`) hanya jika aturan harus mencocokkan beberapa jenis event dari repositori yang sama, karena segmen akhir dari `sub` bervariasi antara event `ref:...`, `environment:...`, dan `pull_request`.

## Memperoleh dan menggunakan token \{#acquire-and-use-a-token}

Atur variabel lingkungan federasi pada job dan panggil SDK seperti biasa. `Anthropic()` membaca `ANTHROPIC_IDENTITY_TOKEN_FILE`, menukar JWT pada permintaan pertama, dan menyegarkan token akses secara otomatis sebelum kedaluwarsa.

<CodeGroup>

```yaml Workflow nocheck
name: Call Claude
on: push

permissions:
  id-token: write
  contents: read

jobs:
  call-claude:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_FEDERATION_RULE_ID: fdrl_...
      ANTHROPIC_ORGANIZATION_ID: 00000000-0000-0000-0000-000000000000
      ANTHROPIC_SERVICE_ACCOUNT_ID: svac_...
      ANTHROPIC_WORKSPACE_ID: wrkspc_...  # required when the rule covers multiple workspaces
      ANTHROPIC_IDENTITY_TOKEN_FILE: /tmp/gha-jwt
    steps:
      - uses: actions/checkout@v5
      - name: Fetch GitHub OIDC token
        run: |
          curl -sS -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
            "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=https://api.anthropic.com" \
            | jq -r .value > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
      - name: Run your script
        run: |
          pip install anthropic
          python your_script.py
```

```bash cURL nocheck
JWT=$(cat /tmp/gha-jwt)

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
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }' | jq -r '.content[0].text'
```

```python Python nocheck
import anthropic

# Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
# ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
# dari lingkungan job.
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

// Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
// ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
// dari lingkungan job.
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
	// Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
	// ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
	// dari lingkungan job.
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
# dari lingkungan job.
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
// dari lingkungan job.
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
# dari lingkungan job.
client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}]
)
puts message.content.first.text
```

</CodeGroup>

Setiap token identitas yang diterbitkan GitHub kedaluwarsa sekitar lima menit setelah diterbitkan. Endpoint permintaan token (`ACTIONS_ID_TOKEN_REQUEST_URL`) tetap valid selama seluruh job berlangsung, sehingga Anda dapat mengambil token baru kapan saja. SDK menukar token pada penggunaan pertama dan menyimpan token akses Anthropic yang dihasilkan dalam cache. Untuk job yang berjalan lebih lama dari masa berlaku token Anthropic, SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap penyegaran, jadi jalankan kembali langkah pengambilan secara berkala (atau bungkus dalam loop latar belakang) untuk menjaga file tetap terkini. Sebagai alternatif, berikan callback penyedia token ke SDK yang memanggil `ACTIONS_ID_TOKEN_REQUEST_URL` secara langsung alih-alih menggunakan path file.

## Memverifikasi penyiapan \{#verify-the-setup}

Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pada `400 invalid_grant`, lihat [Memecahkan masalah pertukaran yang gagal](/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange); penyebab paling umum dari sisi GitHub Actions adalah format klaim `sub` yang tidak cocok (segmen akhirnya bervariasi antara event `ref:...`, `environment:...`, dan `pull_request`).

## Membatasi alur kerja mana yang dapat melakukan autentikasi \{#restrict-which-workflows-can-authenticate}

<Warning>
`subject_prefix` berupa `repo:your-org/*` saja akan mencocokkan setiap repositori di organisasi Anda, dan tanpa batasan `ref`, ini juga mencocokkan eksekusi `pull_request` yang dipicu dari fork. Siapa pun yang dapat membuka pull request terhadap repositori yang cocok dapat memperoleh token Anthropic terfederasi.
</Warning>

Kunci blok `match` pada aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

- **Pin ke satu repositori:** Gunakan `subject_prefix: "repo:your-org/your-repo:*"` sehingga repositori lain di organisasi tidak cocok.
- **Pin ke branch yang dilindungi:** Tambahkan `"ref": "refs/heads/main"` (atau branch rilis Anda) di bawah `claims` sehingga eksekusi pull-request dan feature branch tidak cocok.
- **Pin pemilik secara eksplisit:** Tambahkan `"repository_owner": "your-org"` di bawah `claims` sebagai pemeriksaan pertahanan berlapis terhadap kasus tepi parsing `sub`.
- **Pin ke environment deployment:** Untuk job deploy, cocokkan `subject_prefix: "repo:your-org/your-repo:environment:production"` dan batasi environment tersebut dengan required reviewers di GitHub.

## Langkah selanjutnya \{#next-steps}

- [Workload Identity Federation](/docs/id/manage-claude/workload-identity-federation): panduan penyiapan lengkap, variabel lingkungan, dan prioritas kredensial.
- [Autentikasi](/docs/id/manage-claude/authentication): bagaimana federasi dibandingkan dengan kunci API.