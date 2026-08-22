---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: c2bc737e5ff893da6502689f3a570d2e2ee1c846cbff48db293bc131ea575263
---

---
title: Menggunakan WIF dengan GitHub Actions
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions
description: Autentikasi workflow GitHub Actions ke Claude API dengan token identitas berumur pendek alih-alih kunci API berumur panjang.
---

Setiap eksekusi workflow GitHub Actions dapat meminta token identitas bertanda tangan dari issuer yang di-host GitHub di `https://token.actions.githubusercontent.com`. Dengan Workload Identity Federation, workflow Anda menukarkan token tersebut dengan token akses Anthropic berumur pendek, sehingga job CI Anda dapat memanggil Claude API tanpa secret `ANTHROPIC_API_KEY` yang disimpan di repositori Anda.

Claim `sub` pada token mengodekan repositori dan konteks pemicu. Untuk push ke sebuah branch, bentuknya adalah `repo:<owner>/<repo>:ref:refs/heads/<branch>`. Eksekusi pull-request menggunakan `repo:<owner>/<repo>:pull_request`, dan deployment yang dibatasi environment menggunakan `repo:<owner>/<repo>:environment:<name>`. Aturan federasi Anda mencocokkan claim ini (dan claim lainnya, seperti `repository_owner` dan `ref`) untuk menentukan eksekusi workflow mana yang diizinkan untuk melakukan autentikasi.

## Prasyarat

* Pemahaman tentang [konsep WIF](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule (aturan federasi).
* Repositori GitHub tempat Anda dapat mengedit file workflow dan memberikan izin `id-token: write`.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.
* ID organisasi Anthropic Anda. Anda dapat menemukannya di Claude Console pada **Settings → Organization**.

## Konfigurasikan workflow Anda

GitHub hanya menerbitkan token identitas untuk job yang secara eksplisit memintanya. Tambahkan izin `id-token: write` di tingkat workflow atau job:

```yaml
permissions:
  id-token: write
  contents: read
```

Di dalam job, runner mengekspos dua variabel lingkungan: `ACTIONS_ID_TOKEN_REQUEST_URL` dan `ACTIONS_ID_TOKEN_REQUEST_TOKEN`. Panggil URL permintaan tersebut dengan request token sebagai kredensial bearer dan audience pilihan Anda sebagai parameter query, lalu tulis "JSON Web Token" (token web JSON), atau JWT, yang dikembalikan ke sebuah file:

```yaml
- name: Fetch GitHub OIDC token
  run: |
    curl -sS -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
      "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=https://api.anthropic.com" \
      | jq -r .value > /tmp/gha-jwt
```

Jika Anda lebih suka JavaScript, `actions/github-script` mengekspos kemampuan yang sama melalui `core.getIDToken(audience)`:

```yaml
- name: Fetch GitHub OIDC token
  uses: actions/github-script@v8
  with:
    script: |
      const fs = require('fs');
      const token = await core.getIDToken('https://api.anthropic.com');
      fs.writeFileSync('/tmp/gha-jwt', token);
```

Token yang telah di-decode membawa claim yang mendeskripsikan eksekusi workflow. Aturan federasi Anda mencocokkan claim-claim ini:

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

Lihat [referensi subject claim OIDC GitHub](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims) untuk daftar lengkap format `sub`.

## Konfigurasikan Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih tile **GitHub Actions**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat aturan federasi.

Wizard ini membuat sumber daya tersebut untuk Anda. Gunakan nilai-nilai berikut baik saat Anda memasukkannya di wizard maupun saat mengirimkannya ke [Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** GitHub memublikasikan dokumen discovery OIDC dan JWKS-nya secara publik, jadi gunakan mode discovery. Anthropic memperbarui kunci secara otomatis ketika GitHub merotasinya.

```json
{
  "name": "github-actions",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Cocokkan hanya eksekusi workflow yang memang ingin Anda percayai. Lihat [Batasi workflow mana yang dapat melakukan autentikasi](https://platform.claude.com/docs/id/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate) untuk cara membatasi cakupan claim ini dengan aman.

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

Buatlah sespesifik yang dimungkinkan oleh workload. Longgarkan `subject_prefix` menjadi `repo:your-org/your-repo:*` (dipasangkan dengan batasan `claims.ref`) hanya jika aturan harus mencocokkan beberapa jenis event dari repositori yang sama, karena segmen akhir `sub` bervariasi antara event `ref:...`, `environment:...`, dan `pull_request`.

## Peroleh dan gunakan token

Atur variabel lingkungan federasi pada job dan panggil SDK seperti biasa. `Anthropic()` membaca `ANTHROPIC_IDENTITY_TOKEN_FILE`, menukarkan JWT pada permintaan pertama, dan memperbarui token akses secara otomatis sebelum kedaluwarsa.

<CodeGroup>
  ```yaml Workflow
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

  ```bash cURL
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
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```python Python
  import anthropic

  # Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  # dari environment job.
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(next(block.text for block in message.content if block.type == "text"))
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  // Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  // dari environment job.
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5",
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
  // Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  // dari environment job.
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var result = AnthropicCredentials.Resolve()
      ?? throw new InvalidOperationException("No federation credentials found in environment");
  using var client = new AnthropicOidcClient(result);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5,
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

  ```bash CLI
  # Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  # dari environment job.
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```php PHP
  use Anthropic\Client;

  // Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  // dari environment job.
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-opus-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  # Membaca ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, dan ANTHROPIC_IDENTITY_TOKEN_FILE
  # dari environment job.
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )
  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

Setiap token identitas yang diterbitkan GitHub kedaluwarsa kira-kira lima menit setelah diterbitkan. Endpoint permintaan token (`ACTIONS_ID_TOKEN_REQUEST_URL`) tetap valid selama seluruh job berlangsung, sehingga Anda dapat mengambil token baru kapan saja. SDK menukarkan token pada penggunaan pertama dan menyimpan token akses Anthropic yang dihasilkan dalam cache. Untuk job yang berjalan lebih lama daripada masa berlaku token Anthropic, SDK membaca ulang `ANTHROPIC_IDENTITY_TOKEN_FILE` pada setiap pembaruan, jadi jalankan ulang langkah pengambilan secara berkala (atau bungkus dalam loop latar belakang) agar file tetap mutakhir. Sebagai alternatif, berikan callback penyedia token ke SDK yang memanggil `ACTIONS_ID_TOKEN_REQUEST_URL` secara langsung alih-alih menggunakan path file.

## Verifikasi penyiapan

Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-` dan nilai `expires_in` dalam detik. Pertukaran yang ditolak mengembalikan `401` `authentication_error` yang tidak transparan dengan pesan tetap `Authentication failed`, apa pun pemeriksaan yang gagal; dalam sebagian besar kasus, alasan penolakan dicatat pada entri percobaan tersebut di [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history), dan [Memecahkan masalah pertukaran yang gagal](https://platform.claude.com/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange) menelusuri pemeriksaan secara berurutan. Penyebab paling umum di sisi GitHub Actions adalah format claim `sub` yang tidak cocok (segmen akhirnya bervariasi antara event `ref:...`, `environment:...`, dan `pull_request`); entri riwayat menampilkan alasan `match_subject_prefix`.

## Batasi workflow mana yang dapat melakukan autentikasi

<Warning>
  `subject_prefix` berupa `repo:your-org/*` saja akan cocok dengan setiap repositori di organisasi Anda, dan tanpa batasan `ref`, ia juga cocok dengan eksekusi `pull_request` yang dipicu dari fork. Siapa pun yang dapat membuka pull request terhadap repositori yang cocok dapat memperoleh token Anthropic terfederasi.
</Warning>

Kunci blok `match` pada aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Sematkan ke satu repositori:** Gunakan `subject_prefix: "repo:your-org/your-repo:*"` agar repositori lain di organisasi tidak cocok.
* **Sematkan ke branch yang dilindungi:** Tambahkan `"ref": "refs/heads/main"` (atau branch rilis Anda) di bawah `claims` agar eksekusi pull-request dan feature branch tidak cocok.
* **Sematkan owner secara eksplisit:** Tambahkan `"repository_owner": "your-org"` di bawah `claims` sebagai pemeriksaan defense-in-depth terhadap kasus tepi dalam parsing `sub`.
* **Sematkan ke environment deployment:** Untuk job deploy, cocokkan `subject_prefix: "repo:your-org/your-repo:environment:production"` dan batasi environment tersebut dengan reviewer wajib di GitHub.

## Langkah selanjutnya

* [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation): panduan penyiapan lengkap, variabel lingkungan, dan prioritas kredensial.
* [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication): perbandingan federasi dengan kunci API.
