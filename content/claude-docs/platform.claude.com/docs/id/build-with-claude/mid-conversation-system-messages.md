---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages
fetched_at: 2026-09-26T02:19:50.539049Z
sha256: bf9dbabc953fb0c70aa84d71c5431789637ae5cfc04a1dadb12b7222c1e0c8cd
---

---
title: Pesan sistem dan perubahan alat di tengah percakapan
url: https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages
description: Ubah instruksi sistem atau ketersediaan alat di tengah percakapan tanpa membatalkan prefiks yang di-cache sebelumnya.
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Instruksi sistem biasanya ditempatkan di field `system` tingkat atas, sebelum semua pesan dalam percakapan. Posisi itu sangat cocok untuk ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching): "system prompt" (prompt sistem) menjadi bagian dari prefiks yang stabil, sehingga giliran-giliran berikutnya mendapatkan cache hit. Namun, posisi itu kurang cocok untuk instruksi yang baru Anda sadari perlukan di tengah sesi. Mengedit field `system` tingkat atas akan mengubah bagian paling awal dari prompt dan membatalkan cache untuk semua yang ada setelahnya.

Pesan sistem di tengah percakapan mengatasi masalah tersebut. Alih-alih mengedit field `system` tingkat atas, Anda menambahkan pesan `{"role": "system"}` pada titik dalam percakapan ketika instruksi baru tersebut mulai relevan. Prefiks yang di-cache tetap sama, sehingga permintaan berikutnya tetap membacanya dari cache. Instruksi baru itu juga tetap diterapkan sebagai instruksi sistem, bukan sebagai teks pengguna biasa.

<Note>
  Pesan sistem di tengah percakapan tersedia di Claude API, [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai).

  Fitur ini tersedia di Claude Fable 5.1, [Claude Mythos 5.1](https://anthropic.com/glasswing), Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 5.5, Claude Opus 4.8, dan Claude Opus 5. Pesan sistem di tengah percakapan tidak memerlukan header beta. Fitur ini tidak tersedia di Claude Sonnet 5. Di model tersebut, gunakan field `system` tingkat atas.

  [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) masih dalam tahap beta pada model yang sama. Di Claude API, kirim header beta `inline-tools-2026-09-15`. Header ini juga mencakup [pendefinisian alat di dalam blok `tool_addition`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta). Pendefinisian alat di dalam pesan hanya tersedia di Claude API, dan [penambahan server MCP dengan cara tersebut](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#add-an-mcp-server-mid-conversation-beta) juga memerlukan header beta `mcp-client-2026-09-15`. Header lama `mid-conversation-tool-changes-2026-07-01` masih berfungsi untuk perubahan yang menyebut alat berdasarkan referensi, di Claude API, Amazon Bedrock, dan Google Cloud.

  [Pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at`) masih dalam tahap beta dan memerlukan header beta `mid-conversation-system-clear-at-2026-08-21`. Fitur ini tersedia pada model dan platform yang sama dengan pesan sistem di tengah percakapan.
</Note>

## Perubahan alat di tengah percakapan

Array `tools` berada lebih awal lagi dalam prefiks permintaan yang di-hash dibandingkan field `system` tingkat atas. Karena itu, mengeditnya akan membatalkan [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk seluruh percakapan. Perubahan alat di tengah percakapan adalah padanan pesan sistem di tengah percakapan untuk alat. Alih-alih menetapkan daftar alat untuk seluruh masa percakapan, Anda mengubah alat yang ditawarkan kepada model di antara giliran. Deklarasikan set alat lengkap di `tools` sejak awal, lalu gunakan blok `tool_addition` dan `tool_removal` untuk menawarkan alat kepada model, atau menariknya kembali, mulai dari titik tertentu dalam percakapan. Array `tools` itu sendiri tidak pernah berubah, sehingga prefiks yang di-cache tetap utuh. Perubahan alat di tengah percakapan masih dalam tahap beta dan menggunakan header beta `inline-tools-2026-09-15` di Claude API. Di Amazon Bedrock dan Google Cloud, gunakan header lama `mid-conversation-tool-changes-2026-07-01`, yang mencakup perubahan yang menyebut alat berdasarkan referensi.

`tool_addition` dan `tool_removal` adalah blok konten dalam array `content` dari pesan `role: "system"`, dan keduanya dapat dicampur dengan blok `text` dalam pesan yang sama. Pesan tersebut mengikuti aturan penempatan yang berlaku untuk semua pesan sistem di tengah percakapan, dengan satu batasan tambahan setelah giliran yang dijeda (lihat [Batasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Perubahan berlaku mulai dari titik tersebut dalam percakapan. Field `tool` pada setiap blok mereferensikan alat, bukan mendefinisikannya:

* `{"type": "tool_reference", "name": "..."}` menyebut alat yang dideklarasikan dalam array `tools` pada permintaan.
* Alat [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) dapat direferensikan satu per satu dengan `mcp_tool_reference` (`server_name` dan `name`), atau sebagai satu toolset utuh dengan `mcp_toolset_reference` (`server_name`).

Mereferensikan nama yang tidak dideklarasikan di `tools` akan menghasilkan error 400 (di Claude API, dengan `error.details.error_code` bernilai `tool_reference_unresolved`). Sebagai alternatif, blok `tool_addition` dapat [membawa definisi lengkap alat](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta). Cara ini tidak didukung oleh header lama `mid-conversation-tool-changes-2026-07-01`.

Setiap alat yang dideklarasikan di `tools` ditawarkan kepada model sejak awal percakapan, kecuali jika dideklarasikan dengan `defer_loading: true`. Alat seperti itu ditahan sampai blok `tool_addition` memunculkannya. `tool_addition` juga dapat menawarkan kembali alat yang sebelumnya ditarik oleh `tool_removal`.

Permintaan berikut mendeklarasikan `get_weather` di `tools`, lalu menariknya setelah giliran pengguna pertama dengan blok `tool_removal`. Permintaan ini mengirim header beta `inline-tools-2026-09-15`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: inline-tools-2026-09-15" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather for a location.",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Say OK."
        },
        {
          "role": "system",
          "content": [
            {
              "type": "tool_removal",
              "tool": {"type": "tool_reference", "name": "get_weather"}
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta inline-tools-2026-09-15 \
    --transform 'content.#(type=="text").text' --raw-output <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather for a location.
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: City name
        required:
          - location
  messages:
    - role: user
      content: Say OK.
    - role: system
      content:
        - type: tool_removal
          tool:
            type: tool_reference
            name: get_weather
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      betas=["inline-tools-2026-09-15"],
      # Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
      # prefiks yang di-cache tetap utuh.
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather for a location.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
      messages=[
          {
              "role": "user",
              "content": "Say OK.",
          },
          # Tarik get_weather mulai titik ini. Blok ini merujuk
          # alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
          # identik per byte dan cache tetap hit.
          {
              "role": "system",
              "content": [
                  {
                      "type": "tool_removal",
                      "tool": {"type": "tool_reference", "name": "get_weather"},
                  },
              ],
          },
      ],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    betas: ["inline-tools-2026-09-15"],
    // Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
    // prefiks yang di-cache tetap utuh.
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "City name"
            }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "Say OK." },
      // Tarik get_weather mulai titik ini dan seterusnya. Blok ini merujuk
      // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
      // identik per byte dan cache tetap terkena (hit).
      {
        role: "system",
        content: [
          {
            type: "tool_removal",
            tool: { type: "tool_reference", name: "get_weather" }
          }
        ]
      }
    ]
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Betas = [AnthropicBeta.InlineTools2026_09_15],
      // Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
      // prefiks yang di-cache tetap utuh.
      Tools =
      [
          new BetaTool
          {
              Name = "get_weather",
              Description = "Get the current weather for a location.",
              InputSchema = new InputSchema
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
                  },
                  Required = ["location"],
              },
          },
      ],
      Messages =
      [
          new() { Role = Role.User, Content = "Say OK." },
          // Tarik get_weather mulai titik ini. Blok ini merujuk
          // alat berdasarkan nama alih-alih mengedit `Tools`, sehingga giliran sebelumnya tetap
          // identik per byte dan cache tetap hit.
          new()
          {
              Role = Role.System,
              Content = new(
              [
                  new BetaRequestToolRemovalBlock
                  {
                      Tool = new BetaToolChangeToolReference { Name = "get_weather" },
                  },
              ]),
          },
      ],
  });

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaInlineTools2026_09_15},
  	// Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
  	// prefiks yang di-cache tetap utuh.
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfTool: &anthropic.BetaToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather for a location."),
  			InputSchema: anthropic.BetaToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Say OK.")),
  		// Tarik get_weather mulai titik ini dan seterusnya. Blok ini merujuk
  		// alat berdasarkan namanya alih-alih mengedit Tools, sehingga giliran sebelumnya tetap
  		// identik byte demi byte dan cache tetap hit.
  		{
  			Role: anthropic.BetaMessageParamRoleSystem,
  			Content: []anthropic.BetaContentBlockParamUnion{
  				anthropic.NewBetaToolRemovalBlock(anthropic.BetaToolChangeToolReferenceParam{
  					Name: "get_weather",
  				}),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaRequestToolRemovalBlock;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
      // prefiks yang di-cache tetap utuh.
      BetaTool weatherTool = BetaTool.builder()
          .name("get_weather")
          .description("Get the current weather for a location.")
          .inputSchema(BetaTool.InputSchema.builder()
              .properties(BetaTool.InputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addBeta(AnthropicBeta.INLINE_TOOLS_2026_09_15)
          .addTool(weatherTool)
          .addUserMessage("Say OK.")
          // Tarik get_weather mulai dari titik ini. Blok ini mereferensikan
          // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
          // identik byte demi byte dan cache tetap hit.
          .addMessage(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.SYSTEM)
              .contentOfBetaContentBlockParams(List.of(
                  BetaContentBlockParam.ofToolRemoval(BetaRequestToolRemovalBlock.builder()
                      .referenceTool("get_weather")
                      .build())))
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  // ...

  $client = new Client();

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      betas: [AnthropicBeta::INLINE_TOOLS_2026_09_15],
      // Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
      // prefiks yang di-cache tetap utuh.
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather for a location.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'City name',
                      ],
                  ],
                  'required' => ['location'],
              ],
          ],
      ],
      messages: [
          ['role' => 'user', 'content' => 'Say OK.'],
          // Tarik get_weather mulai titik ini. Blok ini merujuk
          // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
          // identik per byte dan cache tetap terkena (hit).
          [
              'role' => 'system',
              'content' => [
                  [
                      'type' => 'tool_removal',
                      'tool' => ['type' => 'tool_reference', 'name' => 'get_weather'],
                  ],
              ],
          ],
      ],
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    betas: [Anthropic::AnthropicBeta::INLINE_TOOLS_2026_09_15],
    # Seluruh set alat dideklarasikan di awal dan tidak pernah berubah, sehingga
    # prefiks yang di-cache tetap utuh.
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "Say OK." },
      # Tarik get_weather mulai titik ini. Blok ini merujuk
      # alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
      # identik per byte dan cache tetap hit.
      {
        role: "system",
        content: [
          {
            type: "tool_removal",
            tool: { type: "tool_reference", name: "get_weather" }
          }
        ]
      }
    ]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

### Mendefinisikan alat di dalam pesan (beta)

Dengan header beta `inline-tools-2026-09-15`, blok `tool_addition` dapat mendefinisikan alat berdasarkan nilai, yaitu dengan membawa definisi lengkapnya, alih-alih menyebutnya berdasarkan referensi. Dengan begitu, Anda dapat memperkenalkan alat yang belum diketahui di awal percakapan, atau alat yang skemanya berubah kemudian, cukup dengan menambahkan pesan `role: "system"`. Array `tools` dan semua pesan sebelumnya tetap persis seperti yang dikirim. Akibatnya, cache prompt tetap mendapatkan hit dan hanya pesan yang ditambahkan yang diproses sebagai input baru. Satu-satunya pengecualian, yaitu array `tools` tanpa alat non-deferred, dibahas dalam aturan di bawah. Header ini juga mencakup penambahan dan penghapusan alat berdasarkan referensi, sehingga Anda tidak perlu mengirim `mid-conversation-tool-changes-2026-07-01` juga.

Bungkus definisi dalam objek `tool` bertipe `tool_definition`. `definition` adalah entri `tools`, seperti alat kustom atau alat klien maupun server yang didefinisikan Anthropic, lengkap dengan konfigurasinya yang biasa, termasuk `cache_control` dan `defer_loading`. Selama masa beta, beberapa tipe alat (termasuk alat computer use) belum dapat didefinisikan di dalam pesan. Alat-alat tersebut akan menghasilkan error 400 yang menyatakan hal itu. Deklarasikan alat tersebut di `tools` dan tambahkan berdasarkan referensi. Sebagai contoh, untuk mendefinisikan alat kustom di tengah percakapan:

```json
{
  "role": "system",
  "content": [
    {
      "type": "tool_addition",
      "tool": {
        "type": "tool_definition",
        "definition": {
          "name": "db_query",
          "description": "Run a read-only SQL query against the analytics database.",
          "input_schema": {
            "type": "object",
            "properties": { "sql": { "type": "string" } },
            "required": ["sql"]
          }
        }
      }
    }
  ]
}
```

Mulai dari posisi tersebut, model dapat memanggil alat itu dengan cara yang sama seperti memanggil alat yang dideklarasikan di `tools`. Mengirim ulang definisi yang identik tidak mengubah apa pun, sehingga klien dapat mengirimnya ulang dengan aman, misalnya saat mencoba ulang permintaan.

Permintaan berikut mempertahankan `get_weather` di `tools` dan mendefinisikan `db_query` setelah giliran pengguna pertama:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: inline-tools-2026-09-15" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather for a location.",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "How many orders shipped yesterday?"
        },
        {
          "role": "system",
          "content": [
            {
              "type": "tool_addition",
              "tool": {
                "type": "tool_definition",
                "definition": {
                  "name": "db_query",
                  "description": "Run a read-only SQL query against the analytics database.",
                  "input_schema": {
                    "type": "object",
                    "properties": {"sql": {"type": "string"}},
                    "required": ["sql"]
                  }
                }
              }
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta inline-tools-2026-09-15 <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  # Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
  # belakangan tidak mengubah awal prompt yang dirender.
  tools:
    - name: get_weather
      description: Get the current weather for a location.
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: City name
        required:
          - location
  messages:
    - role: user
      content: How many orders shipped yesterday?
    # Definisikan db_query berdasarkan nilai mulai titik ini. `tools` dan
    # pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
    - role: system
      content:
        - type: tool_addition
          tool:
            type: tool_definition
            definition:
              name: db_query
              description: Run a read-only SQL query against the analytics database.
              input_schema:
                type: object
                properties:
                  sql:
                    type: string
                required:
                  - sql
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      betas=["inline-tools-2026-09-15"],
      # Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
      # belakangan tidak mengubah bagian awal prompt yang dirender.
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather for a location.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
      messages=[
          {"role": "user", "content": "How many orders shipped yesterday?"},
          # Definisikan db_query secara langsung (by value) mulai titik ini. `tools` dan
          # pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
          {
              "role": "system",
              "content": [
                  {
                      "type": "tool_addition",
                      "tool": {
                          "type": "tool_definition",
                          "definition": {
                              "name": "db_query",
                              "description": "Run a read-only SQL query against the analytics database.",
                              "input_schema": {
                                  "type": "object",
                                  "properties": {"sql": {"type": "string"}},
                                  "required": ["sql"],
                              },
                          },
                      },
                  },
              ],
          },
      ],
  )

  for block in response.content:
      if block.type == "tool_use":
          print(block.name, block.input)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    betas: ["inline-tools-2026-09-15"],
    // Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
    // belakangan tidak mengubah bagian awal prompt yang dirender.
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "How many orders shipped yesterday?" },
      // Definisikan db_query berdasarkan nilai mulai titik ini. `tools` dan
      // pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
      {
        role: "system",
        content: [
          {
            type: "tool_addition",
            tool: {
              type: "tool_definition",
              definition: {
                name: "db_query",
                description: "Run a read-only SQL query against the analytics database.",
                input_schema: {
                  type: "object",
                  properties: { sql: { type: "string" } },
                  required: ["sql"]
                }
              }
            }
          }
        ]
      }
    ]
  });

  for (const block of response.content) {
    if (block.type === "tool_use") {
      console.log(block.name, JSON.stringify(block.input));
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Betas = [AnthropicBeta.InlineTools2026_09_15],
      // Pertahankan setidaknya satu alat non-deferred di `Tools`, agar alat yang didefinisikan
      // belakangan tidak mengubah bagian awal prompt yang dirender.
      Tools =
      [
          new BetaTool
          {
              Name = "get_weather",
              Description = "Get the current weather for a location.",
              InputSchema = new InputSchema
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
                  },
                  Required = ["location"],
              },
          },
      ],
      Messages =
      [
          new() { Role = Role.User, Content = "How many orders shipped yesterday?" },
          // Definisikan db_query berdasarkan nilai mulai titik ini. `Tools` dan
          // pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
          new()
          {
              Role = Role.System,
              Content = new(
              [
                  new BetaRequestToolAdditionBlock
                  {
                      Tool = new BetaToolChangeToolDefinitionParam
                      {
                          Definition = new BetaTool
                          {
                              Name = "db_query",
                              Description = "Run a read-only SQL query against the analytics database.",
                              InputSchema = new InputSchema
                              {
                                  Properties = new Dictionary<string, JsonElement>
                                  {
                                      ["sql"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                                  },
                                  Required = ["sql"],
                              },
                          },
                      },
                  },
              ]),
          },
      ],
  });

  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          Console.WriteLine($"{toolUse.Name} {JsonSerializer.Serialize(toolUse.Input)}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaInlineTools2026_09_15},
  	// Pertahankan setidaknya satu alat non-deferred di Tools, agar alat yang didefinisikan
  	// belakangan tidak mengubah bagian awal prompt yang dirender.
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfTool: &anthropic.BetaToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather for a location."),
  			InputSchema: anthropic.BetaToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("How many orders shipped yesterday?")),
  		// Definisikan db_query secara langsung (by value) mulai dari sini. Tools dan
  		// pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache hit tetap terjadi.
  		{
  			Role: anthropic.BetaMessageParamRoleSystem,
  			Content: []anthropic.BetaContentBlockParamUnion{
  				anthropic.NewBetaToolAdditionBlock(anthropic.BetaToolChangeToolDefinitionParam{
  					Definition: anthropic.BetaToolUnionParam{OfTool: &anthropic.BetaToolParam{
  						Name:        "db_query",
  						Description: anthropic.String("Run a read-only SQL query against the analytics database."),
  						InputSchema: anthropic.BetaToolInputSchemaParam{
  							Properties: map[string]any{
  								"sql": map[string]any{"type": "string"},
  							},
  							Required: []string{"sql"},
  						},
  					}},
  				}),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if toolUse, ok := block.AsAny().(anthropic.BetaToolUseBlock); ok {
  		fmt.Println(toolUse.Name, toolUse.Input)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaRequestToolAdditionBlock;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaTool weatherTool = BetaTool.builder()
          .name("get_weather")
          .description("Get the current weather for a location.")
          .inputSchema(BetaTool.InputSchema.builder()
              .properties(BetaTool.InputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build();

      BetaTool dbQueryTool = BetaTool.builder()
          .name("db_query")
          .description("Run a read-only SQL query against the analytics database.")
          .inputSchema(BetaTool.InputSchema.builder()
              .properties(BetaTool.InputSchema.Properties.builder()
                  .putAdditionalProperty("sql", JsonValue.from(Map.of("type", "string")))
                  .build())
              .addRequired("sql")
              .build())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addBeta(AnthropicBeta.INLINE_TOOLS_2026_09_15)
          // Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
          // belakangan tidak mengubah bagian awal prompt yang dirender.
          .addTool(weatherTool)
          .addUserMessage("How many orders shipped yesterday?")
          // Definisikan db_query secara langsung (by value) mulai titik ini. `tools` dan
          // pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
          .addSystemMessageOfBetaContentBlockParams(List.of(
              BetaContentBlockParam.ofToolAddition(BetaRequestToolAdditionBlock.builder()
                  .definitionTool(dbQueryTool)
                  .build())))
          .build();

      BetaMessage response = client.beta().messages().create(params);
      response.content().stream()
          .flatMap(block -> block.toolUse().stream())
          .forEach(toolUse -> IO.println(toolUse.name() + " " + toolUse._input()));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaToolUseBlock;
  // ...

  $client = new Client();

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      betas: [AnthropicBeta::INLINE_TOOLS_2026_09_15],
      // Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
      // belakangan tidak mengubah bagian awal prompt yang dirender.
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather for a location.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'City name',
                      ],
                  ],
                  'required' => ['location'],
              ],
          ],
      ],
      messages: [
          ['role' => 'user', 'content' => 'How many orders shipped yesterday?'],
          // Definisikan db_query secara langsung (by value) mulai titik ini. `tools` dan
          // pesan-pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache hit tetap terjadi.
          [
              'role' => 'system',
              'content' => [
                  [
                      'type' => 'tool_addition',
                      'tool' => [
                          'type' => 'tool_definition',
                          'definition' => [
                              'name' => 'db_query',
                              'description' => 'Run a read-only SQL query against the analytics database.',
                              'input_schema' => [
                                  'type' => 'object',
                                  'properties' => ['sql' => ['type' => 'string']],
                                  'required' => ['sql'],
                              ],
                          ],
                      ],
                  ],
              ],
          ],
      ],
  );

  foreach ($response->content as $block) {
      if ($block instanceof BetaToolUseBlock) {
          echo $block->name, ' ', json_encode($block->input), PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    betas: [Anthropic::AnthropicBeta::INLINE_TOOLS_2026_09_15],
    # Pertahankan setidaknya satu alat non-deferred di `tools`, agar alat yang didefinisikan
    # belakangan tidak mengubah bagian awal prompt yang dirender.
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "How many orders shipped yesterday?" },
      # Definisikan db_query secara langsung (by value) mulai titik ini. `tools` dan
      # pesan sebelumnya tetap persis seperti yang dikirim, sehingga cache tetap hit.
      {
        role: "system",
        content: [
          {
            type: "tool_addition",
            tool: {
              type: "tool_definition",
              definition: {
                name: "db_query",
                description: "Run a read-only SQL query against the analytics database.",
                input_schema: {
                  type: "object",
                  properties: { sql: { type: "string" } },
                  required: ["sql"]
                }
              }
            }
          }
        ]
      }
    ]
  )

  response.content.each do |block|
    puts "#{block.name} #{block.input}" if block.is_a?(Anthropic::Beta::BetaToolUseBlock)
  end
  ```
</CodeGroup>

`content` pada respons menyertakan blok `tool_use` untuk alat baru tersebut, misalnya:

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "db_query",
  "input": {
    "sql": "SELECT COUNT(*) FROM orders WHERE shipped_at::date = CURRENT_DATE - 1"
  }
}
```

Untuk mengubah skema alat, atau untuk memindahkan alat server ke versi yang lebih baru, kirim definisi yang berbeda dengan nama yang sama. Definisi baru menggantikan definisi sebelumnya mulai dari posisi tersebut. Definisi yang memakai ulang nama dari tipe alat yang berbeda akan menghasilkan error 400 dengan `error.details.error_code` bernilai `tool_name_conflict`. Versi yang lebih baru dari alat yang sama tidak dihitung sebagai tipe yang berbeda. `tool_removal` tetap menggunakan referensi, dan alat yang telah dihapus dapat didefinisikan atau ditawarkan kembali nanti.

Beberapa aturan berikut muncul dari posisi tempat definisi dirender:

* **Deklarasikan alat yang sudah Anda ketahui sejak awal.** Alat yang sudah Anda ketahui pada permintaan pertama sebaiknya ditempatkan di `tools`. Jika model belum boleh melihatnya, gunakan `defer_loading: true` dan referensi `tool_addition` di kemudian hari. Definisikan berdasarkan nilai hanya alat yang belum diketahui pada permintaan pertama atau yang berubah kemudian.
* **Pertahankan setidaknya satu alat non-deferred di `tools`.** Percakapan yang array `tools`-nya tidak memiliki alat non-deferred tetap diterima. Namun, alat pertama yang didefinisikan berdasarkan nilai akan mengubah awal prompt yang dirender, sehingga permintaan tersebut mengalami satu cache miss penuh. [Alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) dihitung sebagai alat non-deferred.
* **Tipe alat bertanggal tetap memerlukan header beta masing-masing.** Jika alat server yang Anda definisikan berdasarkan nilai memerlukan header beta sendiri, kirim header tersebut pada setiap permintaan berikutnya dalam percakapan.
* **Tempatkan `cache_control` pada blok atau di dalam definisi, tidak keduanya.** `cache_control` dihitung terhadap batas breakpoint permintaan. Definisi yang ditangguhkan (deferred) tidak dapat membawa `cache_control`.

Permintaan akan menghasilkan error 400 dengan `error.details.error_code` bernilai `available_tools_limit_exceeded` jika salah satu batas berikut terlampaui:

* Lebih dari 10.000 alat deferred tersedia setelah pesan mana pun.
* Lebih dari 10.000 alat yang didefinisikan setelah pesan pengguna pertama tersedia setelah pesan mana pun.
* Total definisi alat yang dikirim setelah pesan pengguna pertama dan masih tersedia setelah pesan mana pun melebihi 4 MB (4.194.304 byte).
* Teks alat yang dirender lebih besar dari 4 MB (4.194.304 byte).

### Menambahkan server MCP di tengah percakapan (beta)

Untuk menambahkan server [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) di tengah percakapan, kirimkan header beta `mcp-client-2026-09-15` bersama dengan `inline-tools-2026-09-15`. Dengan begitu, `definition` dalam blok `tool_addition` dapat berupa `mcp_toolset`, sehingga alat-alat server tersebut menjadi tersedia tanpa mengedit `tools`. Cantumkan detail koneksi server di `mcp_servers` seperti biasa, lalu tambahkan toolset pada titik ketika server tersebut menjadi tersedia:

```json
{
  "role": "system",
  "content": [
    {
      "type": "tool_addition",
      "tool": {
        "type": "tool_definition",
        "definition": { "type": "mcp_toolset", "mcp_server_name": "calendar" }
      }
    }
  ]
}
```

Objek `mcp_toolset` sama dengan objek yang akan Anda tempatkan di `tools`, termasuk `default_config` dan `configs`. Blok `tool_addition` tidak pernah memuat URL server atau token. Keduanya tetap berada di `mcp_servers`.

Permintaan berikut mempertahankan `get_weather` di `tools`, mencantumkan server kalender di `mcp_servers`, dan menambahkan toolset server tersebut setelah giliran pengguna pertama:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: inline-tools-2026-09-15,mcp-client-2026-09-15" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "mcp_servers": [
        {
          "type": "url",
          "url": "https://mcp.example.com/calendar",
          "name": "calendar",
          "authorization_token": "YOUR_TOKEN"
        }
      ],
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather for a location.",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "What'\''s on my calendar tomorrow?"
        },
        {
          "role": "system",
          "content": [
            {
              "type": "tool_addition",
              "tool": {
                "type": "tool_definition",
                "definition": {
                  "type": "mcp_toolset",
                  "mcp_server_name": "calendar"
                }
              }
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta inline-tools-2026-09-15,mcp-client-2026-09-15 <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  mcp_servers:
    - type: url
      url: https://mcp.example.com/calendar
      name: calendar
      authorization_token: YOUR_TOKEN
  tools:
    - name: get_weather
      description: Get the current weather for a location.
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: City name
        required:
          - location
  messages:
    - role: user
      content: What's on my calendar tomorrow?
    # Sediakan alat dari server kalender mulai titik ini dan seterusnya.
    # Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
    - role: system
      content:
        - type: tool_addition
          tool:
            type: tool_definition
            definition:
              type: mcp_toolset
              mcp_server_name: calendar
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      betas=["inline-tools-2026-09-15", "mcp-client-2026-09-15"],
      mcp_servers=[
          {
              "type": "url",
              "url": "https://mcp.example.com/calendar",
              "name": "calendar",
              "authorization_token": "YOUR_TOKEN",
          },
      ],
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather for a location.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string", "description": "City name"},
                  },
                  "required": ["location"],
              },
          },
      ],
      messages=[
          {"role": "user", "content": "What's on my calendar tomorrow?"},
          # Sediakan alat dari server kalender mulai titik ini dan seterusnya.
          # Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
          {
              "role": "system",
              "content": [
                  {
                      "type": "tool_addition",
                      "tool": {
                          "type": "tool_definition",
                          "definition": {
                              "type": "mcp_toolset",
                              "mcp_server_name": "calendar",
                          },
                      },
                  },
              ],
          },
      ],
  )

  # Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  # jadi periksa tipe setiap blok alih-alih membaca content[0].
  for block in response.content:
      match block.type:
          case "mcp_tool_listing":
              print(block.mcp_server_name, [tool.name for tool in block.tools])
          case "text":
              print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    betas: ["inline-tools-2026-09-15", "mcp-client-2026-09-15"],
    mcp_servers: [
      {
        type: "url",
        url: "https://mcp.example.com/calendar",
        name: "calendar",
        authorization_token: "YOUR_TOKEN"
      }
    ],
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "What's on my calendar tomorrow?" },
      // Sediakan alat dari server kalender mulai titik ini dan seterusnya.
      // Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
      {
        role: "system",
        content: [
          {
            type: "tool_addition",
            tool: {
              type: "tool_definition",
              definition: { type: "mcp_toolset", mcp_server_name: "calendar" }
            }
          }
        ]
      }
    ]
  });

  // Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  // jadi periksa tipe setiap blok alih-alih membaca content[0].
  for (const block of response.content) {
    switch (block.type) {
      case "mcp_tool_listing":
        console.log(
          block.mcp_server_name,
          block.tools.map((tool) => tool.name)
        );
        break;
      case "text":
        console.log(block.text);
        break;
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Betas = [AnthropicBeta.InlineTools2026_09_15, AnthropicBeta.McpClient2026_09_15],
      McpServers =
      [
          new BetaRequestMcpServerUrlDefinition
          {
              Url = "https://mcp.example.com/calendar",
              Name = "calendar",
              AuthorizationToken = "YOUR_TOKEN",
          },
      ],
      Tools =
      [
          new BetaTool
          {
              Name = "get_weather",
              Description = "Get the current weather for a location.",
              InputSchema = new InputSchema
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
                  },
                  Required = ["location"],
              },
          },
      ],
      Messages =
      [
          new() { Role = Role.User, Content = "What's on my calendar tomorrow?" },
          // Sediakan alat dari server kalender mulai titik ini dan seterusnya.
          // Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
          new()
          {
              Role = Role.System,
              Content = new(
              [
                  new BetaRequestToolAdditionBlock
                  {
                      Tool = new BetaToolChangeToolDefinitionParam
                      {
                          Definition = new BetaMcpToolset("calendar"),
                      },
                  },
              ]),
          },
      ],
  });

  // Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  // jadi periksa tipe setiap blok alih-alih membaca Content[0].
  foreach (var block in response.Content)
  {
      if (block.TryPickMcpToolListing(out var listing))
      {
          Console.WriteLine($"{listing.McpServerName} {JsonSerializer.Serialize(listing.Tools.Select(tool => tool.Name))}");
      }
      else if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaInlineTools2026_09_15,
  		anthropic.AnthropicBetaMCPClient2026_09_15,
  	},
  	MCPServers: []anthropic.BetaRequestMCPServerURLDefinitionParam{
  		{
  			URL:                "https://mcp.example.com/calendar",
  			Name:               "calendar",
  			AuthorizationToken: anthropic.String("YOUR_TOKEN"),
  		},
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfTool: &anthropic.BetaToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather for a location."),
  			InputSchema: anthropic.BetaToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "City name",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What's on my calendar tomorrow?")),
  		// Sediakan alat dari server kalender mulai titik ini dan seterusnya.
  		// Blok ini menyebutkan nama server; blok ini tidak pernah menyimpan URL atau token.
  		{
  			Role: anthropic.BetaMessageParamRoleSystem,
  			Content: []anthropic.BetaContentBlockParamUnion{
  				anthropic.NewBetaToolAdditionBlock(anthropic.BetaToolChangeToolDefinitionParam{
  					Definition: anthropic.BetaToolUnionParam{OfMCPToolset: &anthropic.BetaMCPToolsetParam{
  						MCPServerName: "calendar",
  					}},
  				}),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  // jadi periksa tipe setiap blok alih-alih membaca Content[0].
  for _, block := range response.Content {
  	switch variant := block.AsAny().(type) {
  	case anthropic.BetaMCPToolListingBlock:
  		var toolNames []string
  		for _, tool := range variant.Tools {
  			toolNames = append(toolNames, tool.Name)
  		}
  		fmt.Println(variant.MCPServerName, toolNames)
  	case anthropic.BetaTextBlock:
  		fmt.Println(variant.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMcpTool;
  import com.anthropic.models.beta.messages.BetaMcpToolset;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
  import com.anthropic.models.beta.messages.BetaRequestToolAdditionBlock;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaTool weatherTool = BetaTool.builder()
          .name("get_weather")
          .description("Get the current weather for a location.")
          .inputSchema(BetaTool.InputSchema.builder()
              .properties(BetaTool.InputSchema.Properties.builder()
                  .putAdditionalProperty("location", JsonValue.from(Map.of(
                      "type", "string",
                      "description", "City name")))
                  .build())
              .addRequired("location")
              .build())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addBeta(AnthropicBeta.INLINE_TOOLS_2026_09_15)
          .addBeta(AnthropicBeta.MCP_CLIENT_2026_09_15)
          .addMcpServer(BetaRequestMcpServerUrlDefinition.builder()
              .url("https://mcp.example.com/calendar")
              .name("calendar")
              .authorizationToken("YOUR_TOKEN")
              .build())
          .addTool(weatherTool)
          .addUserMessage("What's on my calendar tomorrow?")
          // Sediakan alat dari server kalender mulai titik ini dan seterusnya.
          // Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
          .addSystemMessageOfBetaContentBlockParams(List.of(
              BetaContentBlockParam.ofToolAddition(BetaRequestToolAdditionBlock.builder()
                  .definitionTool(BetaMcpToolset.builder()
                      .mcpServerName("calendar")
                      .build())
                  .build())))
          .build();

      BetaMessage response = client.beta().messages().create(params);

      // Respons diawali dengan blok mcp_tool_listing untuk server kalender,
      // jadi periksa tipe setiap blok alih-alih membaca blok pertama.
      for (var block : response.content()) {
          switch (block.type().value()) {
              case MCP_TOOL_LISTING -> {
                  var listing = block.asMcpToolListing();
                  var toolNames = listing.tools().stream().map(BetaMcpTool::name).toList();
                  IO.println(listing.mcpServerName() + " " + toolNames);
              }
              case TEXT -> IO.println(block.asText().text());
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaMCPTool;
  use Anthropic\Beta\Messages\BetaMCPToolListingBlock;
  use Anthropic\Beta\Messages\BetaTextBlock;
  // ...

  $client = new Client();

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      betas: [
          AnthropicBeta::INLINE_TOOLS_2026_09_15,
          AnthropicBeta::MCP_CLIENT_2026_09_15,
      ],
      mcpServers: [
          [
              'type' => 'url',
              'url' => 'https://mcp.example.com/calendar',
              'name' => 'calendar',
              'authorization_token' => 'YOUR_TOKEN',
          ],
      ],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather for a location.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'City name',
                      ],
                  ],
                  'required' => ['location'],
              ],
          ],
      ],
      messages: [
          ['role' => 'user', 'content' => "What's on my calendar tomorrow?"],
          // Sediakan alat dari server kalender mulai titik ini dan seterusnya.
          // Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
          [
              'role' => 'system',
              'content' => [
                  [
                      'type' => 'tool_addition',
                      'tool' => [
                          'type' => 'tool_definition',
                          'definition' => [
                              'type' => 'mcp_toolset',
                              'mcp_server_name' => 'calendar',
                          ],
                      ],
                  ],
              ],
          ],
      ],
  );

  // Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  // jadi periksa tipe setiap blok alih-alih membaca content[0].
  foreach ($response->content as $block) {
      switch (true) {
          case $block instanceof BetaMCPToolListingBlock:
              $toolNames = array_map(fn (BetaMCPTool $tool) => $tool->name, $block->tools);
              echo $block->mcpServerName, ' ', json_encode($toolNames), PHP_EOL;
              break;
          case $block instanceof BetaTextBlock:
              echo $block->text, PHP_EOL;
              break;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    betas: [
      Anthropic::AnthropicBeta::INLINE_TOOLS_2026_09_15,
      Anthropic::AnthropicBeta::MCP_CLIENT_2026_09_15
    ],
    mcp_servers: [
      {
        type: "url",
        url: "https://mcp.example.com/calendar",
        name: "calendar",
        authorization_token: "YOUR_TOKEN"
      }
    ],
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather for a location.",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "What's on my calendar tomorrow?" },
      # Sediakan alat dari server kalender mulai titik ini dan seterusnya.
      # Blok ini menyebutkan nama server; blok ini tidak pernah memuat URL atau token.
      {
        role: "system",
        content: [
          {
            type: "tool_addition",
            tool: {
              type: "tool_definition",
              definition: { type: "mcp_toolset", mcp_server_name: "calendar" }
            }
          }
        ]
      }
    ]
  )

  # Respons diawali dengan blok mcp_tool_listing untuk server kalender,
  # jadi periksa tipe setiap blok alih-alih membaca content[0].
  response.content.each do |block|
    case block
    when Anthropic::Beta::BetaMCPToolListingBlock
      puts "#{block.mcp_server_name} #{block.tools.map(&:name)}"
    when Anthropic::Beta::BetaTextBlock
      puts block.text
    end
  end
  ```
</CodeGroup>

Dengan `mcp-client-2026-09-15`, jika API mengambil daftar alat dari server untuk sebuah respons, respons tersebut diawali dengan blok `mcp_tool_listing`, satu blok untuk setiap server yang diambil. Jika kode Anda membaca `content[0]`, lewati blok-blok ini.

Kirimkan kembali pesan asisten tanpa perubahan, termasuk blok ini, dan tetap kirimkan `mcp-client-2026-09-15` pada setiap permintaan yang membawanya. Permintaan berikutnya kemudian menggunakan daftar yang tercatat alih-alih menanyakan server lagi. Untuk menyematkan toolset sendiri, salin daftar tersebut ke field `tools` milik `mcp_toolset`, seperti yang dijelaskan dalam [Menyematkan daftar alat server MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#pin-mcp-tool-list).

`mcp-client-2026-09-15` mencakup semua yang dicakup oleh `mcp-client-2025-11-20`, sehingga Anda tidak perlu mengirimkan keduanya. Fitur-fitur ini tersedia di Claude API. Permintaan yang menggunakan konektor MCP tetap tunduk pada ketentuan [retensi data](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#data-retention) konektor tersebut.

## Kapan menggunakan pesan sistem di tengah percakapan

[Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) melakukan hash pada prefiks permintaan secara berurutan: `tools`, lalu `system`, lalu `messages`. Agar terjadi cache hit, prefiks harus sama persis dengan permintaan terbaru, byte demi byte, hingga breakpoint cache.

Dengan urutan tersebut, field `system` tingkat atas berada di dekat awal prefiks yang di-hash. Perubahan apa pun padanya, bahkan sekadar menambahkan satu kalimat, menghasilkan hash yang berbeda. Akibatnya, permintaan tidak mengenai cache untuk prompt sistem maupun setiap pesan yang di-cache setelahnya.

Pesan sistem di tengah percakapan memungkinkan Anda menambahkan instruksi di **akhir** riwayat pesan. Semua yang ada sebelum instruksi baru tidak berubah, sehingga entri cache yang ada tetap cocok. Hanya pesan baru yang diproses sebagai input baru.

Beberapa situasi ketika hal ini penting:

* **Perubahan kebijakan atau persona di tengah sesi.** Sebuah sesi agentik yang panjang memerlukan batasan baru ("mulai sekarang, tulis semua SQL sebagai kueri berparameter") setelah puluhan giliran yang di-cache. Menambahkannya ke field `system` tingkat atas akan memproses ulang seluruh riwayat.
* **Konteks per giliran yang harus otoritatif.** Anda ingin menyisipkan catatan kebaruan data, tenggat sesi, atau perubahan ketersediaan alat dengan bobot tingkat sistem. Informasi tersebut terlalu sering berubah untuk ditempatkan di prefiks yang di-cache.
* **Pengingat per giliran yang tidak boleh menumpuk.** Sebuah harness mengingatkan model setelah setiap batch hasil alat ("minta pembacaan yang saling independen secara bersamaan", "pengguna sudah lama tidak mendapat kabar dari Anda") dan ingin model hanya melihat salinan terbaru. [Pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dirender untuk satu giliran, lalu tidak lagi memakan biaya, tanpa perlu menghapus apa pun dari riwayat.
* **Perubahan status yang diamati aplikasi Anda.** Aplikasi Anda mendeteksi sesuatu yang harus diperlakukan Claude sebagai fakta tingkat operator. Contohnya: file di disk berubah, pengguna mengaktifkan pengaturan persetujuan otomatis, alat yang tersedia berubah, atau sisa anggaran token turun di bawah ambang batas.
* **Input pengguna yang tidak boleh menginterupsi loop agentik.** Pengguna mengetik pesan lanjutan saat Claude masih menjalankan alat untuk permintaan sebelumnya. Jika input itu diteruskan sebagai pesan sistem setelah hasil alat berikutnya, Claude dapat memasukkannya ke dalam pekerjaan yang sedang berjalan, alih-alih memperlakukannya sebagai permintaan baru yang mengharuskannya beralih tugas. Lihat [Penempatan setelah hasil alat](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#placement-after-tool-results).
* **Peralihan mode yang memberikan izin tetap.** Mode tingkat sesi dapat menggunakan pesan sistem di tengah percakapan untuk memberikan persetujuan tetap atas kemampuan yang mahal, seperti meluncurkan alur kerja multiagen secara otomatis. Mode ini dapat disertai pengingat singkat setiap beberapa giliran dan pemberitahuan saat mode dinonaktifkan. Untuk contoh lengkap, lihat [Membangun mode orkestrasi](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-effort-example).

Dalam semua kasus ini, Anda sebenarnya dapat menempatkan instruksi dalam pesan `user` biasa, dan Claude memang mengikuti instruksi yang datang dalam giliran pengguna. Perbedaannya terletak pada prioritas. Pesan `user` diperlakukan sebagai berasal dari pengguna akhir, sedangkan pesan `system` diperlakukan sebagai berasal dari Anda, operator aplikasi. Jika keduanya bertentangan, instruksi sistem lebih diutamakan. Karena itu, gunakan peran `system` untuk fakta dan batasan tingkat operator yang harus tetap berlaku meskipun pengguna akhir meminta hal yang berbeda. Pesan sistem di tengah percakapan mempertahankan prioritas tingkat operator tersebut tanpa biaya cache miss yang timbul saat mengedit field `system` tingkat atas.

## Cara kerjanya

Tambahkan pesan dengan `"role": "system"` ke array `messages`. Gunakan string biasa atau blok konten untuk `content`, sama seperti giliran `user` atau `assistant`. Instruksi berlaku mulai dari titik tersebut dalam percakapan. Ketika instruksi bertentangan, pesan sistem yang lebih baru lebih diutamakan daripada yang lebih lama. Pesan sistem di tengah percakapan juga lebih diutamakan daripada field `system` tingkat atas untuk giliran-giliran yang mengikutinya.

Anda tetap dapat mengatur field `system` tingkat atas untuk instruksi yang harus berlaku di seluruh percakapan. Gunakan pesan sistem di tengah percakapan untuk instruksi yang baru relevan kemudian, atau yang ingin Anda tambahkan tanpa membatalkan prefiks yang di-cache.

Pesan `role: "system"` juga dapat membawa `output_config.effort` untuk mengubah tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) mulai dari giliran `user` berikutnya. Fitur ini masih dalam tahap beta di Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, dan Claude Opus 5 di Claude API dan Google Cloud, serta memerlukan header beta `mid-conversation-output-config-2026-07-01`. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are a code review assistant. Be concise.",
      "messages": [
        {
          "role": "user",
          "content": "Review process() in utils.py for performance issues."
        },
        {
          "role": "assistant",
          "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
        },
        {
          "role": "user",
          "content": "Now review the calling code that invokes process()."
        },
        {
          "role": "system",
          "content": "From now on, every suggestion must include explicit type annotations."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create --transform 'content.#(type=="text").text' --raw-output <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: You are a code review assistant. Be concise.
  messages:
    - role: user
      content: Review process() in utils.py for performance issues.
    - role: assistant
      content: >-
        The list comprehension is fine for small inputs. For large inputs,
        consider a generator to avoid materializing the full list.
    - role: user
      content: Now review the calling code that invokes process().
    - role: system
      content: From now on, every suggestion must include explicit type annotations.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      # Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
      # dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
      cache_control={"type": "ephemeral"},
      system="You are a code review assistant. Be concise.",
      messages=[
          {
              "role": "user",
              "content": "Review process() in utils.py for performance issues.",
          },
          {
              "role": "assistant",
              "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.",
          },
          {
              "role": "user",
              "content": "Now review the calling code that invokes process().",
          },
          # Di tengah sesi, peninjau menyadari bahwa semua saran juga harus
          # lolos kebijakan typing ketat milik tim. Menambahkan
          # instruksi di sini menjaga giliran sebelumnya tetap identik per byte, sehingga
          # prefiks yang di-cache oleh permintaan sebelumnya tetap dibaca dari cache.
          {
              "role": "system",
              "content": "From now on, every suggestion must include explicit type annotations.",
          },
      ],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    // Caching prompt otomatis: setiap request menyimpan percakapan sejauh ini ke cache,
    // dan request berikutnya membaca prefiks yang tidak berubah dari cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      {
        role: "user",
        content: "Review process() in utils.py for performance issues."
      },
      {
        role: "assistant",
        content:
          "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
      },
      {
        role: "user",
        content: "Now review the calling code that invokes process()."
      },
      // Di tengah sesi, peninjau menyadari bahwa semua saran juga harus lolos
      // kebijakan typing ketat milik tim. Menambahkan instruksi di sini menjaga
      // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
      // request sebelumnya tetap dibaca dari cache.
      {
        role: "system",
        content: "From now on, every suggestion must include explicit type annotations."
      }
    ]
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      // Automatic prompt caching (caching prompt otomatis): setiap permintaan meng-cache percakapan sejauh ini,
      // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
      CacheControl = new CacheControlEphemeral(),
      System = "You are a code review assistant. Be concise.",
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Review process() in utils.py for performance issues."
          },
          new()
          {
              Role = Role.Assistant,
              Content = "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
          },
          new()
          {
              Role = Role.User,
              Content = "Now review the calling code that invokes process()."
          },
          // Di tengah sesi, peninjau menyadari bahwa semua saran juga harus lolos
          // kebijakan typing ketat milik tim. Menambahkan instruksi di sini menjaga
          // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
          // permintaan sebelumnya tetap dibaca dari cache.
          new()
          {
              Role = Role.System,
              Content = "From now on, every suggestion must include explicit type annotations."
          }
      ]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	// Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
  	// dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
  	CacheControl: anthropic.NewCacheControlEphemeralParam(),
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a code review assistant. Be concise."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review process() in utils.py for performance issues.")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Now review the calling code that invokes process().")),
  		// Di tengah sesi, peninjau menyadari bahwa semua saran juga harus
  		// lolos kebijakan typing ketat milik tim. Menambahkan instruksi
  		// di sini menjaga giliran sebelumnya tetap identik per byte, jadi prefiks yang di-cache oleh
  		// permintaan sebelumnya tetap dibaca dari cache.
  		{
  			Role: anthropic.MessageParamRoleSystem,
  			Content: []anthropic.ContentBlockParamUnion{
  				anthropic.NewTextBlock("From now on, every suggestion must include explicit type annotations."),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.CacheControlEphemeral;
  // ...
  import com.anthropic.models.messages.MessageParam;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          // Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
          // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
          .cacheControl(CacheControlEphemeral.builder().build())
          .system("You are a code review assistant. Be concise.")
          .addUserMessage("Review process() in utils.py for performance issues.")
          .addAssistantMessage("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")
          .addUserMessage("Now review the calling code that invokes process().")
          // Di tengah sesi, peninjau menyadari bahwa semua saran juga harus lolos
          // kebijakan typing ketat milik tim. Menambahkan instruksi di sini menjaga
          // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh permintaan
          // sebelumnya tetap dibaca dari cache.
          .addMessage(MessageParam.builder()
              .role(MessageParam.Role.SYSTEM)
              .content("From now on, every suggestion must include explicit type annotations.")
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  use Anthropic\Messages\CacheControlEphemeral;
  // ...
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Review process() in utils.py for performance issues.'],
          ['role' => 'assistant', 'content' => 'The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.'],
          ['role' => 'user', 'content' => 'Now review the calling code that invokes process().'],
          // Di tengah sesi, peninjau menyadari bahwa semua saran juga harus lolos
          // kebijakan typing ketat tim. Menambahkan instruksi di sini menjaga
          // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
          // permintaan sebelumnya tetap dibaca dari cache.
          ['role' => 'system', 'content' => 'From now on, every suggestion must include explicit type annotations.']
      ],
      model: 'claude-opus-5-5',
      // "Prompt caching" (caching prompt) otomatis: tiap permintaan meng-cache percakapan sejauh ini,
      // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
      cacheControl: CacheControlEphemeral::with(),
      system: 'You are a code review assistant. Be concise.',
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    # Caching prompt otomatis: setiap permintaan menyimpan percakapan sejauh ini ke cache,
    # dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      { role: "user", content: "Review process() in utils.py for performance issues." },
      { role: "assistant", content: "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list." },
      { role: "user", content: "Now review the calling code that invokes process()." },
      # Di tengah sesi, peninjau menyadari bahwa semua saran juga harus lolos
      # kebijakan typing ketat milik tim. Menambahkan instruksi di sini menjaga
      # giliran sebelumnya tetap identik byte demi byte, sehingga prefiks yang di-cache permintaan
      # sebelumnya masih dibaca dari cache.
      { role: "system", content: "From now on, every suggestion must include explicit type annotations." }
    ]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

Contoh ini mengaktifkan [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) dengan field `cache_control` tingkat atas. Caching prompt bersifat opt-in. Jika permintaan tidak memiliki field `cache_control` (baik otomatis maupun [breakpoint eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints)), tidak ada yang di-cache, dan setiap permintaan membayar harga token input reguler untuk seluruh percakapan. Dengan caching diaktifkan, menambahkan pesan sistem tidak mengubah giliran yang sudah di-cache. Karena itu, permintaan yang membawa instruksi baru tetap membaca giliran tersebut dari cache alih-alih memprosesnya lagi. Caching juga mengharuskan percakapan memenuhi [panjang prompt minimum yang dapat di-cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations). Contoh sependek ini berada di bawah batas tersebut, sehingga `cache_creation_input_tokens` dan `cache_read_input_tokens` tetap bernilai 0 sampai percakapan bertambah panjang.

Pesan sistem di tengah percakapan harus langsung mengikuti giliran `user` (atau giliran `assistant` yang diakhiri dengan hasil alat server). Pesan tersebut juga harus menjadi entri terakhir di `messages` atau langsung diikuti oleh giliran `assistant`. Pesan `user` yang membawa blok `tool_result` juga dihitung sebagai giliran `user`. Dalam loop agentik, Anda dapat menempatkan pesan sistem tepat setelah hasil alat, sebelum giliran Claude berikutnya. Posisi lain mana pun menghasilkan error 400, termasuk di antara blok `tool_use` milik `assistant` dan `tool_result` yang menjawabnya.

### Penempatan setelah hasil alat

Dalam [loop agentik](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview), pesan sistem ditempatkan setelah pesan `user` yang mengirimkan hasil alat. Di posisi ini pula aplikasi Anda dapat meneruskan input yang diketik pengguna saat Claude sedang bekerja, sehingga konteks baru dapat diserap tanpa memulai ulang giliran:

```json
[
  { "role": "user", "content": "Run the test suite and fix any failures." },
  {
    "role": "assistant",
    "content": [{ "type": "tool_use", "id": "toolu_01", "name": "run_tests", "input": {} }]
  },
  {
    "role": "user",
    "content": [
      { "type": "tool_result", "tool_use_id": "toolu_01", "content": "12 passed, 0 failed" }
    ]
  },
  {
    "role": "system",
    "content": "The user sent the following message while you were working: also update the changelog before you finish."
  }
]
```

Rumuskan konten sistem sebagai konteks, bukan sebagai perintah yang mengesampingkan pengguna. Nyatakan faktanya ("input baru diterima dari pengguna: X", "sisa anggaran token sekarang Y") dan biarkan Claude bertindak berdasarkan fakta tersebut. Claude dilatih untuk menolak instruksi yang tampak merugikan pengguna, dan perlindungan ini tetap berlaku untuk peran sistem. Karena itu, kalimat seperti "abaikan apa yang dikatakan pengguna" kurang efektif dibandingkan menyatakan apa yang berubah.

Pola ini ditujukan untuk meneruskan input dari pengguna akhir percakapan itu sendiri. Jangan gunakan pola ini untuk meneruskan output alat, dokumen yang diambil, atau konten pihak ketiga lainnya. Simpan konten semacam itu dalam blok `tool_result` (lihat [Batasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)).

### Pesan sistem berlingkup giliran

Untuk membatasi lingkup pesan `role: "system"` pada giliran saat ini, atur field `clear_at`-nya. Field ini menerima salah satu dari dua nilai:

* `"never"` (default): pesan dirender pada posisinya di setiap permintaan yang menyertakannya. Menghilangkan field ini memberikan hasil yang sama.
* `"next_user_message"`: pesan bersifat **"turn-scoped" (berlingkup giliran)**. Teksnya hanya dirender selama tidak ada pesan `role: "user"` yang muncul setelahnya di `messages`. Pesan pengguna yang hanya membawa blok `tool_result` juga dihitung sebagai pesan pengguna di sini. Begitu ada pesan pengguna yang lebih baru, pesan tersebut **dibersihkan**. Pesan tetap berada di array, tetapi tidak merender apa pun dan tidak memakan token input, baik pada permintaan tersebut maupun setiap permintaan berikutnya.

Pesan sistem berlingkup giliran masih dalam tahap beta. Sertakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-system-clear-at-2026-08-21`. Tanpa header tersebut, `clear_at` ditolak sebagai field yang tidak dikenal.

```json
{
  "role": "system",
  "clear_at": "next_user_message",
  "content": "First privately list what you need next; then request every item that doesn't depend on another's result in this one response."
}
```

Kegunaan utamanya adalah pengingat per giliran dalam loop alat. Tambahkan pengingat setelah pesan `tool_result` setiap kali Anda ingin model melihatnya, dan biarkan setiap salinan sebelumnya tetap di tempatnya. Model hanya melihat salinan yang muncul setelah pesan pengguna terakhir, sehingga pengingat tidak pernah menumpuk. Tidak ada yang berubah di bagian awal `messages`, sehingga [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) tetap cocok. Di Claude Fable 5.1 dan Claude Opus 5.5, cara ini juga menjaga [blok thinking berikutnya tetap valid](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation). Menghapus pengingat sebelumnya akan mengubah percakapan sebelum blok-blok tersebut dan menggagalkan pemeriksaan percakapan. Sebaliknya, pesan yang dibersihkan tetap berada di array dan tidak mengubah percakapan tersebut.

Permintaan berikut adalah langkah lanjutan dari sebuah loop agen. `messages[3]` dirender pada permintaan sebelumnya, ketika pesan tersebut masih menjadi pesan terakhir di array. Begitu `messages[5]` (pesan pengguna yang lebih baru) ada, `messages[3]` dibersihkan. Pesan yang dibersihkan tetap berada di array, sehingga percakapan sebelum blok thinking di `messages[4]` tidak berubah, tetapi model tidak lagi melihat teksnya. `messages[6]` dan `messages[7]` keduanya dirender, secara berurutan.

```json
{
  "model": "claude-fable-5-1",
  "max_tokens": 16000,
  "messages": [
    { "role": "user", "content": "Fix the failing test." },
    {
      "role": "assistant",
      "content": [
        { "type": "thinking", "thinking": "", "signature": "..." },
        {
          "type": "tool_use",
          "id": "toolu_01",
          "name": "read_file",
          "input": { "path": "test_auth.py" }
        }
      ]
    },
    {
      "role": "user",
      "content": [{ "type": "tool_result", "tool_use_id": "toolu_01", "content": "..." }]
    },
    {
      "role": "system",
      "clear_at": "next_user_message",
      "content": "Request independent reads in one turn."
    },
    {
      "role": "assistant",
      "content": [
        { "type": "thinking", "thinking": "", "signature": "..." },
        {
          "type": "tool_use",
          "id": "toolu_02",
          "name": "read_file",
          "input": { "path": "auth.py" }
        },
        {
          "type": "tool_use",
          "id": "toolu_03",
          "name": "read_file",
          "input": { "path": "tokens.py" }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        { "type": "tool_result", "tool_use_id": "toolu_02", "content": "..." },
        {
          "type": "tool_result",
          "tool_use_id": "toolu_03",
          "content": "...",
          "cache_control": { "type": "ephemeral" }
        }
      ]
    },
    {
      "role": "system",
      "clear_at": "next_user_message",
      "content": "Request independent reads in one turn."
    },
    {
      "role": "system",
      "clear_at": "next_user_message",
      "content": "The shell exited with status 137."
    }
  ]
}
```

Aturan untuk pesan berlingkup giliran:

* **Kirim ulang pesan yang dibersihkan apa adanya.** Pesan yang dibersihkan tetap merupakan bagian dari riwayat percakapan. Membangunnya ulang dari status saat ini (jumlah token terbaru, stempel waktu), membuangnya karena dianggap berlebihan, atau mengubah nilai `clear_at`-nya sama dengan mengedit pesan sebelumnya. Cache prompt akan mengalami miss mulai dari titik tersebut. Di Claude Fable 5.1 dan Claude Opus 5.5, setiap blok thinking yang dihasilkan setelahnya juga gagal dalam [pemeriksaan percakapan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation).
* **Hanya teks.** `content` berupa satu atau lebih blok `text` (atau sebuah string). Blok `tool_addition` dan `tool_removal` menghasilkan error 400 pada pesan berlingkup giliran, begitu pula `output_config`. Untuk hal-hal tersebut, gunakan pesan `role: "system"` terpisah tanpa `clear_at`.
* **Tidak ada `cache_control` pada bloknya.** Pesan yang dibersihkan tidak pernah menjadi bagian dari kunci cache, sehingga breakpoint padanya tidak akan pernah cocok. Tempatkan breakpoint pada blok terakhir dari giliran pengguna sebelumnya, seperti dalam contoh. Field [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) tingkat atas melewati pesan berlingkup giliran saat memilih breakpoint. Pada permintaan yang membersihkan sebuah pesan, prefiks cache yang dapat digunakan ulang berakhir pada giliran pengguna sebelum pesan tersebut. Akibatnya, hanya satu giliran asisten di antara pesan tersebut dan pesan pengguna baru yang diproses ulang.
* **Aturan penempatan tetap berlaku**, baik pesan dibersihkan maupun tidak. Seperti pesan sistem di tengah percakapan lainnya, pesan berlingkup giliran harus mengikuti giliran `user` (atau giliran `assistant` yang diakhiri dengan hasil alat server). Pesan tersebut juga harus mendahului giliran `assistant` atau mengakhiri array. Pesan yang mengakhiri array selalu dirender. Pesan yang langsung diikuti oleh pesan `user` lain menghasilkan error 400, bukan pesan yang dibersihkan. Tempatkan semua hasil dari satu putaran alat dalam satu pesan pengguna, lalu tempatkan pengingat setelahnya.
* **Giliran asisten tidak membersihkannya.** Giliran asisten yang di-prefill atau [dijeda](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#pause-turn) setelah pesan tersebut tidak menambahkan pesan pengguna, begitu pula loop alat sisi server. Karena itu, pesan tetap dirender pada kelanjutan tersebut. Agar pengingat tetap terlihat sepanjang loop alat sisi klien, tambahkan pengingat itu lagi setelah setiap pesan `tool_result`.
* **Penghitungan token mengikuti apa yang dirender.** Pesan yang dibersihkan tidak menambah apa pun pada `usage.input_tokens` atau pada [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).
* **Riwayat yang diimpor.** Anda mungkin menyusun transkrip dalam satu langkah (contoh few-shot, percakapan yang dimigrasikan). Dalam transkrip seperti itu, pesan berlingkup giliran yang sudah diikuti oleh giliran asisten dan pesan pengguna akan dibersihkan sejak permintaan pertama dan tidak pernah dirender. Itulah status yang tepat untuk pengingat per giliran yang Anda bawa. Biarkan `clear_at` tidak diatur hanya pada pesan yang harus dilihat model di setiap permintaan.

Error validasinya adalah:

```text wrap
messages.3.clear_at: Extra inputs are not permitted
messages.3.clear_at: clear_at is only permitted on role 'system' messages
messages.3.clear_at: Input should be 'next_user_message' or 'never'
messages.3: a turn-scoped system message supports text blocks only (clear_at: 'next_user_message')
messages.3: output_config is not permitted on a turn-scoped system message (clear_at: 'next_user_message')
messages.3.content.0: cache_control is not permitted on a turn-scoped system message (clear_at: 'next_user_message')
```

Error pertama adalah error yang dikembalikan tanpa header beta. Di Amazon Bedrock dan Google Cloud, teruskan nilai beta seperti yang dijelaskan dalam [Header beta](https://platform.claude.com/docs/id/api/beta-headers).

Melalui SDK, atur `clear_at` pada entri `role: "system"` di `messages` dan kirimkan header beta. Contoh berikut menambahkan pengingat berlingkup giliran setelah giliran pengguna. Pada permintaan berikutnya, begitu ada pesan pengguna yang lebih baru, pengingat tetap berada di array tetapi tidak lagi dirender:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mid-conversation-system-clear-at-2026-08-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5-1",
      "max_tokens": 4096,
      "messages": [
        {"role": "user", "content": "Draft a short status update on the database migration for the team channel."},
        {"role": "system", "clear_at": "next_user_message", "content": "The reader is on call: keep this reply under 50 words."}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta mid-conversation-system-clear-at-2026-08-21 \
    --transform 'content.#(type=="text").text' --raw-output <<'YAML'
  model: claude-fable-5-1
  max_tokens: 4096
  messages:
    - role: user
      content: Draft a short status update on the database migration for the team channel.
    # Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
    - role: system
      clear_at: next_user_message
      content: "The reader is on call: keep this reply under 50 words."
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5-1",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Draft a short status update on the database migration for the team channel.",
          },
          # Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
          {
              "role": "system",
              "clear_at": "next_user_message",
              "content": "The reader is on call: keep this reply under 50 words.",
          },
      ],
      betas=["mid-conversation-system-clear-at-2026-08-21"],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5-1",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Draft a short status update on the database migration for the team channel."
      },
      // Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
      {
        role: "system",
        clear_at: "next_user_message",
        content: "The reader is on call: keep this reply under 50 words."
      }
    ],
    betas: ["mid-conversation-system-clear-at-2026-08-21"]
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = "claude-fable-5-1",
      MaxTokens = 4096,
      Messages =
      [
          new() { Role = Role.User, Content = "Draft a short status update on the database migration for the team channel." },
          // Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
          new()
          {
              Role = Role.System,
              ClearAt = ClearAt.NextUserMessage,
              Content = "The reader is on call: keep this reply under 50 words.",
          },
      ],
      Betas = [AnthropicBeta.MidConversationSystemClearAt2026_08_21],
  });

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     "claude-fable-5-1",
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Draft a short status update on the database migration for the team channel.")),
  		// Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
  		{
  			Role:    anthropic.BetaMessageParamRoleSystem,
  			ClearAt: anthropic.BetaMessageParamClearAtNextUserMessage,
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("The reader is on call: keep this reply under 50 words.")},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaMidConversationSystemClearAt2026_08_21},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-fable-5-1")
          .maxTokens(4096L)
          .addBeta(AnthropicBeta.MID_CONVERSATION_SYSTEM_CLEAR_AT_2026_08_21)
          .addUserMessage("Draft a short status update on the database migration for the team channel.")
          // Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
          .addMessage(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.SYSTEM)
              .clearAt(BetaMessageParam.ClearAt.NEXT_USER_MESSAGE)
              .content("The reader is on call: keep this reply under 50 words.")
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Client;

  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5-1',
      maxTokens: 4096,
      messages: [
          BetaMessageParam::with(role: 'user', content: 'Draft a short status update on the database migration for the team channel.'),
          // Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
          BetaMessageParam::with(
              role: 'system',
              clearAt: 'next_user_message',
              content: 'The reader is on call: keep this reply under 50 words.',
          ),
      ],
      betas: [AnthropicBeta::MID_CONVERSATION_SYSTEM_CLEAR_AT_2026_08_21],
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5-1",
    max_tokens: 4096,
    messages: [
      {role: "user", content: "Draft a short status update on the database migration for the team channel."},
      # Pengingat lingkup giliran: dirender untuk giliran ini, lalu dihapus setelah ada pesan pengguna berikutnya.
      {role: "system", clear_at: :next_user_message, content: "The reader is on call: keep this reply under 50 words."}
    ],
    betas: [Anthropic::AnthropicBeta::MID_CONVERSATION_SYSTEM_CLEAR_AT_2026_08_21]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Menggabungkan dengan caching prompt

Pesan sistem di tengah percakapan dan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) dirancang untuk digunakan bersama:

* **Aktifkan caching secara eksplisit.** Caching hanya terjadi ketika permintaan menyertakan `cache_control`, baik berupa field [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) di tingkat atas maupun [breakpoint eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints) pada sebuah blok konten. Pesan sistem di tengah percakapan tidak membuat entri cache dengan sendirinya, dan tanpa caching yang diaktifkan, tidak ada penghematan yang perlu dipertahankan.
* **Cache prefiks yang stabil seperti biasa.** Tempatkan `cache_control` pada blok terakhir yang tetap sama di seluruh permintaan, baik itu akhir dari field `system` tingkat atas, akhir dari definisi alat Anda, atau titik yang stabil dalam riwayat pesan.
* **Tambahkan pesan sistem setelah breakpoint.** Karena pesan tersebut berada setelah prefiks yang di-cache, pesan itu tidak mengubah hash prefiks dan cache tetap mengalami hit.
* **Pesan sistem di tengah percakapan itu sendiri dapat di-cache.** Setelah berada dalam percakapan, pesan tersebut menjadi bagian dari riwayat yang stabil. Pada giliran berikutnya, Anda dapat memindahkan breakpoint cache Anda melewatinya (atau mengandalkan [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) untuk melakukannya) dan pesan sistem dibaca dari cache seperti giliran lainnya.

Hindari mengedit atau menghapus pesan sistem di tengah percakapan yang sudah dikirim. Seperti perubahan lain pada pesan sebelumnya, hal itu membatalkan cache mulai dari titik tersebut dan seterusnya. Pada Claude Fable 5.1 dan Claude Opus 5.5, hal itu juga membatalkan [blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation) di setiap giliran asisten berikutnya. Untuk panduan yang seharusnya hanya berlaku untuk satu giliran, gunakan [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dan biarkan tetap di tempatnya. Jika instruksi perlu berkembang, tambahkan pesan sistem baru alih-alih menulis ulang yang lama. Pesan sistem yang berurutan diterima dan diperlakukan sebagai satu bagian sistem, yang secara keseluruhan mengikuti aturan penempatan yang sama.

## Batasan

* **Tidak dapat menjadi pesan pertama.** Pesan `system` yang membawa konten tidak dapat menjadi entri pertama di `messages`. Untuk instruksi yang berlaku sejak awal, gunakan field `system` tingkat atas.

* **Penempatan dibatasi.** Pesan `system` yang membawa konten (blok `text`, `tool_addition`, atau `tool_removal`) harus memenuhi aturan berikut:

  * Pesan itu harus langsung mengikuti giliran `user` (termasuk giliran `user` yang membawa blok `tool_result`) atau giliran `assistant` yang diakhiri dengan hasil alat server.
  * Pesan itu harus mendahului giliran `assistant` atau menjadi akhir array.
  * Pesan itu tidak dapat berada di antara blok `tool_use` dan `tool_result`-nya.

  Menempatkannya di posisi lain mengembalikan error 400. Ada satu pengecualian: blok `tool_addition` dan `tool_removal` tidak diterima tepat setelah giliran `assistant` yang [dijeda](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#pause-turn) (yaitu giliran yang diakhiri dengan hasil alat server), meskipun blok `text` diterima. Dalam kasus ini, lanjutkan dulu giliran yang dijeda, lalu kirim perubahan alat dalam pesan `system` berikutnya.

  Pesan dengan `content` kosong yang hanya mengatur [`output_config.effort`](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) tidak merender apa pun pada posisinya. Pesan seperti ini diterima di posisi mana pun di `messages`, termasuk sebagai entri pertama atau di antara giliran `assistant` dan giliran `user`. Pesan `system` yang berurutan dinilai sebagai satu kelompok. Jadi, jika Anda menambahkan pesan yang membawa teks di samping pesan yang hanya berisi effort, seluruh kelompok harus mengikuti aturan untuk pesan yang membawa konten.

* **Pesan berlingkup giliran hanya berisi teks dan harus dikirim ulang apa adanya.** Pesan `clear_at: "next_user_message"` tidak dapat membawa `tool_addition`, `tool_removal`, `output_config`, atau `cache_control`. Setelah dibersihkan, pesan tersebut harus tetap berada di `messages` tanpa perubahan sedikit pun (byte demi byte) pada permintaan berikutnya. Lihat [Pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages).

* **Bukan tempat untuk konten yang tidak tepercaya.** Claude memperlakukan konten sistem sebagai instruksi operator dan mengikutinya. Jangan tempatkan teks dari luar percakapan, seperti output alat mentah, dokumen yang diambil, atau konten web, langsung dalam pesan sistem. Jika Anda melakukannya, teks tersebut akan memperoleh otoritas tingkat operator. Simpan data semacam itu dalam blok `tool_result` dan tetap ikuti panduan [Memitigasi jailbreak dan injeksi prompt](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks).

## Terkait

<CardGroup cols={2}>
  <Card title="Caching prompt" icon="bolt" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Cara kerja caching, tempat menempatkan breakpoint, dan cara membaca field penggunaan cache.
  </Card>

  <Card title="Diagnostik cache" icon="magnifying-glass" href="https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics">
    Temukan titik persis perbedaan antara dua permintaan ketika cache hit yang Anda harapkan tidak terjadi.
  </Card>

  <Card title="Menggunakan Messages API" icon="message" href="https://platform.claude.com/docs/id/build-with-claude/working-with-messages">
    Struktur pesan, percakapan multi-giliran, dan field `system`.
  </Card>

  <Card title="Praktik terbaik prompting" icon="text" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Menulis prompt dan instruksi sistem yang efektif.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Struktur blok `tool_use` dan `tool_result` dalam array `messages`.
  </Card>
</CardGroup>
