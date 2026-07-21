---
source: platform
url: https://platform.claude.com/docs/id/api/beta-headers
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 8ef0a41cd0ef646227519cb27fe400501ef38721988021eca5e42a197838e0f1
---

# Header beta

Akses fitur eksperimental sebelum ketersediaan umum dengan header `anthropic-beta` atau parameter `betas` pada SDK.

---

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

<Info>
  Setiap [SDK klien](/docs/id/cli-sdks-libraries/overview) menyediakan namespace `beta` untuk memanggil API dengan fitur beta diaktifkan.
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

Dokumentasi setiap fitur menyebutkan nama beta yang tepat untuk dikirim. [Ikhtisar API](/docs/id/api/overview) mencantumkan API yang saat ini dalam tahap beta.

Contoh berikut menunjukkan permintaan yang sama dengan cURL, CLI `ant`, dan SDK. SDK menerima nama beta dalam parameter `betas` dan mengirimkan header `anthropic-beta` untuk Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello, Claude"}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta files-api-2025-04-14 \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      betas=["files-api-2025-04-14"],
  )

  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const msg = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["files-api-2025-04-14"]
  });

  console.log(msg.content);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var message = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = "claude-opus-4-8",
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
          Betas = ["files-api-2025-04-14"],
      }
  );

  Console.WriteLine(string.Join("\n", message.Content));
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("%+v\n", message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_8)
    .maxTokens(1024)
    .addUserMessage("Hello, Claude")
    .addBeta(AnthropicBeta.FILES_API_2025_04_14)
    .build();

  BetaMessage message = client.beta().messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-opus-4-8',
      betas: ['files-api-2025-04-14'],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    betas: ["files-api-2025-04-14"]
  )

  puts(message.content)
  ```
</CodeGroup>

<Warning>
  Fitur beta bersifat eksperimental dan mungkin:

  * Memiliki perubahan yang merusak (breaking changes) dengan pemberitahuan
  * Dihentikan atau dihapus
  * Memiliki batas laju atau harga yang berbeda
  * Tidak tersedia di semua wilayah
</Warning>

### Beberapa fitur beta

Untuk menggunakan beberapa fitur beta dalam satu permintaan, sertakan semua nama fitur dalam header yang dipisahkan dengan koma:

```http
anthropic-beta: feature1,feature2,feature3
```

Saat menggunakan SDK, cantumkan setiap fitur dalam parameter `betas` (misalnya, `betas=["feature1", "feature2"]`). Dengan CLI, berikan satu flag `--beta` dengan nama fitur yang dipisahkan dengan koma (misalnya, `--beta feature1,feature2`). Hindari mengulang flag tersebut: saat ini hanya nilai flag pertama yang berlaku.

### Header khusus endpoint

Beberapa API beta terbatas pada endpoint tertentu dan memerlukan header beta khusus fitur pada setiap permintaan:

| Endpoint                                         | Header beta                 |
| ------------------------------------------------ | --------------------------- |
| `/v1/agents`, `/v1/sessions`, `/v1/environments` | `managed-agents-2026-04-01` |
| `/v1/tunnels`                                    | `mcp-tunnels-2026-06-22`    |

Namespace `beta` pada SDK menambahkan header ini secara otomatis. Tambahkan sendiri hanya saat membuat permintaan HTTP mentah. Lihat [ikhtisar Managed Agents](/docs/id/managed-agents/overview) dan [referensi MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/reference#tunnels-api) untuk detailnya.

### Konvensi penamaan versi

Nama fitur beta biasanya mengikuti pola `feature-name-YYYY-MM-DD`, di mana tanggal menunjukkan kapan beta tersebut dirilis. Selalu gunakan nama fitur beta yang tepat sebagaimana didokumentasikan.

## Penanganan kesalahan

Jika Anda menggunakan nama beta yang tidak valid, atau beta yang tidak dapat diakses oleh organisasi Anda, Anda akan menerima respons kesalahan `400`:

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

Untuk pembaruan fitur beta, lihat [catatan rilis](/docs/id/release-notes/overview). Untuk bantuan terkait masalah produksi, hubungi [dukungan](https://support.claude.com/).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kesalahan" icon="info" href="/docs/id/api/errors">
    Pahami kode status HTTP, bentuk respons kesalahan, dan ID permintaan yang dikembalikan oleh Claude API, serta tangani kesalahan dengan exception bertipe dari SDK.
  </Card>

  <Card title="Ikhtisar API" icon="compass" href="/docs/id/api/overview">
    Jelajahi fitur-fitur Claude API, termasuk API yang saat ini dalam tahap beta.
  </Card>
</CardGroup>
