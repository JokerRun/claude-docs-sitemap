---
source: platform
url: https://platform.claude.com/docs/id/api/beta-headers
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 555bca63507c28061e161d42dea6d843fcf9f95eca2b287463ae21d78cd30434
---

---
title: Header beta
url: https://platform.claude.com/docs/id/api/beta-headers
description: Akses fitur eksperimental sebelum menjadi bagian dari API standar dengan header `anthropic-beta` atau parameter `betas` pada SDK.
---

"Beta headers" (header beta) memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

<Info>
  Setiap [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) menyediakan namespace `beta` untuk memanggil API dengan fitur beta yang diaktifkan.
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

Dokumentasi setiap fitur menyebutkan nama beta yang tepat untuk dikirim. [Ikhtisar API](https://platform.claude.com/docs/id/api/overview) mencantumkan API yang saat ini dalam tahap beta.

Contoh berikut menunjukkan permintaan yang sama dengan cURL, CLI `ant`, dan SDK, menggunakan beta [pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing) sebagai contoh. SDK menerima nama beta dalam parameter `betas` dan mengirimkan header `anthropic-beta` untuk Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: context-management-2025-06-27" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta context-management-2025-06-27 \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      betas=["context-management-2025-06-27"],
  )

  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const msg = await client.beta.messages.create({
    model: "claude-opus-5",
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
          Model = "claude-opus-5",
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
  	Model:     anthropic.ModelClaudeOpus5,
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
    .model(Model.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
      betas: ['context-management-2025-06-27'],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-opus-5",
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
  * Memiliki "rate limit" (batas laju) atau harga yang berbeda
  * Tidak tersedia di semua wilayah
</Warning>

### Beberapa fitur beta

Untuk menggunakan beberapa fitur beta dalam satu permintaan, sertakan semua nama fitur dalam header yang dipisahkan dengan koma:

```http
anthropic-beta: feature1,feature2,feature3
```

Saat menggunakan SDK, cantumkan setiap fitur dalam parameter `betas` (misalnya, `betas=["feature1", "feature2"]`). Dengan CLI, berikan satu flag `--beta` dengan nama fitur yang dipisahkan dengan koma (misalnya, `--beta feature1,feature2`). Hindari mengulang flag tersebut: saat ini hanya nilai flag pertama yang berlaku.

### Header khusus endpoint

Beberapa API beta dibatasi pada endpoint tertentu dan memerlukan header beta khusus fitur pada setiap permintaan:

| Endpoint                                         | Header beta                 |
| ------------------------------------------------ | --------------------------- |
| `/v1/agents`, `/v1/sessions`, `/v1/environments` | `managed-agents-2026-04-01` |
| `/v1/tunnels`                                    | `mcp-tunnels-2026-06-22`    |
| `/v1/memory_stores` dan sub-resource-nya         | `agent-memory-2026-07-22`   |

Namespace `beta` pada SDK menambahkan header ini secara otomatis. Tambahkan sendiri hanya saat membuat permintaan HTTP mentah. Lihat [ikhtisar Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), [Menggunakan memori agen](https://platform.claude.com/docs/id/managed-agents/memory), dan [referensi MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api) untuk detailnya.

Header khusus endpoint yang berlaku untuk endpoint yang sama tidak selalu dapat digabungkan. Pada endpoint memory store, `agent-memory-2026-07-22` menggantikan `managed-agents-2026-04-01`: mengirim keduanya pada permintaan yang sama akan mengembalikan error `400`. SDK klien mengirimkan header yang benar untuk setiap endpoint secara otomatis.

### Konvensi penamaan versi

Nama fitur beta biasanya mengikuti pola `feature-name-YYYY-MM-DD`, di mana tanggal menunjukkan kapan beta tersebut dirilis. Selalu gunakan nama fitur beta yang tepat seperti yang didokumentasikan.

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
    Jelajahi fitur-fitur Claude API, termasuk API yang saat ini dalam tahap beta.
  </Card>
</CardGroup>
