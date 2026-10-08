---
source: platform
url: https://platform.claude.com/docs/id/api/beta-headers
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 7a798353d59526dd0594b8bf9eeffded99ba5961a4b18a437bb087df8b33f559
---

---
title: Header beta
url: https://platform.claude.com/docs/id/api/beta-headers
description: Akses fitur eksperimental sebelum menjadi bagian dari API standar dengan header `anthropic-beta` atau parameter `betas` pada SDK.
---

"Beta headers" (header beta) memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

<Info>
  [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) menyediakan namespace `client.beta` (python, typescript, ruby; csharp, go: `client.Beta`; java: `client.beta()`; php: `$client->beta`) untuk memanggil API dengan fitur beta yang diaktifkan.
</Info>

## Cara menggunakan header beta

Untuk mengakses fitur beta, sertakan header `anthropic-beta` dalam permintaan API Anda:

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
anthropic-beta: BETA_FEATURE_NAME
content-type: application/json
```

Dokumentasi setiap fitur menyebutkan nama beta persis yang harus dikirim. [Ikhtisar API](https://platform.claude.com/docs/id/api/overview) mencantumkan API yang saat ini dalam tahap beta.

Contoh berikut menunjukkan permintaan yang sama dengan cURL, CLI `ant`, dan SDK, menggunakan beta [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) sebagai contoh. SDK menerima nama beta melalui `betas` (python, typescript, php, ruby; csharp, go: `Betas`; java: `.addBeta()`) dan mengirimkan header `anthropic-beta` untuk Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: context-management-2025-06-27" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta context-management-2025-06-27 \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      betas=["context-management-2025-06-27"],
  )

  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const msg = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["context-management-2025-06-27"]
  });

  console.log(msg.content);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var message = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = "claude-opus-5-5",
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
          Betas = ["context-management-2025-06-27"],
      }
  );

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_5_5)
    .maxTokens(1024)
    .addUserMessage("Hello, Claude")
    .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
    .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-opus-5-5',
      betas: ['context-management-2025-06-27'],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    betas: ["context-management-2025-06-27"]
  )

  puts(message.content)
  ```
</CodeGroup>

<Warning>
  Fitur beta bersifat eksperimental dan mungkin:

  * Mengalami perubahan yang merusak kompatibilitas dengan pemberitahuan
  * Dihentikan atau dihapus
  * Memiliki batas laju atau harga yang berbeda
  * Tidak tersedia di semua wilayah
</Warning>

### Beberapa fitur beta

Untuk menggunakan beberapa fitur beta dalam satu permintaan, sertakan semua nama fitur dalam header yang dipisahkan dengan koma:

```http
anthropic-beta: feature1,feature2,feature3
```

Anda juga dapat mengirim header `anthropic-beta` lebih dari sekali dalam permintaan yang sama. Claude API membaca setiap header `anthropic-beta`, sehingga contoh berikut setara dengan contoh sebelumnya:

```http
anthropic-beta: feature1
anthropic-beta: feature2
anthropic-beta: feature3
```

Dengan SDK, cantumkan setiap fitur (misalnya, `betas=["feature1", "feature2"]` (python; typescript, ruby: `betas: ["feature1", "feature2"]`; php: `betas: ['feature1', 'feature2']`; csharp: `Betas = ["feature1", "feature2"]`; go: `Betas: []anthropic.AnthropicBeta{"feature1", "feature2"}`; java: `.addBeta("feature1").addBeta("feature2")`)). Dengan CLI, berikan satu flag `--beta` dengan nama-nama fitur yang dipisahkan koma (misalnya, `--beta feature1,feature2`). Anda juga dapat mengulang flag tersebut (misalnya, `--beta feature1 --beta feature2`).

### Fitur beta di platform lain

Nama beta sama di setiap platform yang menerimanya, tetapi tidak setiap platform menerima setiap beta. [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai) menerima nama beta di header `anthropic-beta`, seperti halnya Claude API. Untuk mengirim beberapa beta, letakkan nama-namanya dalam satu header, dipisahkan dengan koma: Google Cloud hanya membaca satu header `anthropic-beta` dan mengabaikan sisanya, sehingga beta di header lainnya tidak berlaku.

Di Amazon Bedrock, lokasi nama beta bergantung pada API yang Anda panggil:

* [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) (endpoint `bedrock-mantle`) menerimanya di header `anthropic-beta`.
* [InvokeModel API](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) membacanya dari body permintaan, bukan dari header. Cantumkan di array `anthropic_beta` pada body, satu nama per elemen, misalnya `"anthropic_beta": ["feature1", "feature2"]`.

### Header khusus endpoint

Beberapa API beta dibatasi pada endpoint tertentu dan memerlukan header beta khusus fitur pada setiap permintaan:

| Endpoint                                         | Header beta                 |
| ------------------------------------------------ | --------------------------- |
| `/v1/agents`, `/v1/sessions`, `/v1/environments` | `managed-agents-2026-04-01` |
| `/v1/tunnels`                                    | `mcp-tunnels-2026-06-22`    |
| `/v1/memory_stores` dan sub-resource-nya         | `agent-memory-2026-07-22`   |

Namespace `client.beta` (python, typescript, ruby; csharp, go: `client.Beta`; java: `client.beta()`; php: `$client->beta`) pada SDK menambahkan header ini secara otomatis. Tambahkan sendiri hanya saat membuat permintaan HTTP mentah. Lihat [ikhtisar Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), [Menggunakan memori agen](https://platform.claude.com/docs/id/managed-agents/memory), dan [referensi MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api) untuk detailnya.

Header khusus endpoint yang berlaku untuk endpoint yang sama tidak selalu dapat digabungkan. Pada endpoint memory store, `agent-memory-2026-07-22` menggantikan `managed-agents-2026-04-01`: mengirim keduanya pada permintaan yang sama akan menghasilkan error `400`. SDK mengirimkan header yang benar untuk setiap endpoint secara otomatis.

### Konvensi penamaan versi

Nama fitur beta biasanya mengikuti pola `feature-name-YYYY-MM-DD`, di mana tanggal menunjukkan kapan beta tersebut dirilis. Selalu gunakan nama fitur beta yang persis seperti yang didokumentasikan.

## Penanganan error

Jika Anda menggunakan nama beta yang tidak valid, atau beta yang tidak dapat diakses oleh organisasi Anda, Anda akan menerima respons error `400`:

```json Output
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Unexpected value(s) `invalid-beta-name` for the `anthropic-beta` header. Please consult our documentation at platform.claude.com/docs or try again without the header."
  },
  "request_id": "req_011CcnGfC9fELffo2EALu4Wd"
}
```

## Mendapatkan bantuan

Untuk pembaruan fitur beta, lihat [catatan rilis](https://platform.claude.com/docs/id/release-notes/overview). Untuk bantuan terkait masalah produksi, hubungi [dukungan](https://support.claude.com/).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Error" icon="info" href="https://platform.claude.com/docs/id/api/errors">
    Pahami kode status HTTP, bentuk respons error, dan ID permintaan yang dikembalikan Claude API, serta tangani error dengan exception bertipe pada SDK.
  </Card>

  <Card title="Ikhtisar API" icon="compass" href="https://platform.claude.com/docs/id/api/overview">
    Jelajahi fitur-fitur Claude API, termasuk API yang saat ini berstatus beta.
  </Card>
</CardGroup>
