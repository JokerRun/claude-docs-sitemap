---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 3ee2c445a8e3981e09c1a1e773f6f83b4491429fe8e62152db10f1112d7fe14e
---

---
title: Pesan sistem dan perubahan alat di tengah percakapan
url: https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages
description: Ubah instruksi sistem atau ketersediaan alat di tengah percakapan tanpa membatalkan prefiks yang telah di-cache sebelumnya.
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Instruksi sistem biasanya berada di field `system` tingkat atas, mendahului setiap pesan dalam percakapan. Posisi itu sangat baik untuk [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching): "system prompt" (prompt sistem) merupakan bagian dari prefiks yang stabil, sehingga giliran berikutnya mengenai cache. Posisi itu buruk untuk instruksi yang baru Anda sadari diperlukan di tengah sesi, karena mengedit field `system` tingkat atas mengubah bagian paling awal dari prompt dan membatalkan cache untuk semua yang mengikutinya.

Pesan sistem di tengah percakapan menutup celah itu. Anda menambahkan pesan `{"role": "system"}` pada titik dalam percakapan di mana instruksi baru menjadi relevan, alih-alih mengedit field `system` tingkat atas. Prefiks yang di-cache tetap sama, sehingga permintaan berikutnya masih membacanya dari cache, dan instruksi baru tetap diterapkan sebagai instruksi sistem, bukan sebagai teks pengguna biasa.

<Note>
  Pesan sistem di tengah percakapan tersedia di Claude API, [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai).

  Fitur ini tersedia di Claude Fable 5.1, [Claude Mythos 5.1](https://anthropic.com/glasswing), Claude Fable 5, [Claude Mythos 5](https://anthropic.com/glasswing), Claude Opus 4.8, dan Claude Opus 5. Tidak diperlukan header beta untuk pesan sistem di tengah percakapan. Fitur ini tidak tersedia di Claude Sonnet 5. Gunakan field `system` tingkat atas di sana sebagai gantinya.

  [Perubahan alat di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) berada dalam versi beta dan memerlukan header beta `mid-conversation-tool-changes-2026-07-01`. Fitur ini tersedia pada model yang sama, di Claude API, Amazon Bedrock, dan Google Cloud.

  [Pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at`) berada dalam versi beta dan memerlukan header beta `mid-conversation-system-clear-at-2026-08-21`, pada model dan platform yang sama dengan pesan sistem di tengah percakapan.
</Note>

## Perubahan alat di tengah percakapan

Array `tools` berada lebih awal lagi dalam prefiks permintaan yang di-hash dibandingkan field `system` tingkat atas, sehingga mengeditnya membatalkan [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) untuk seluruh percakapan. Perubahan alat di tengah percakapan adalah padanan alat dari pesan sistem di tengah percakapan. Alih-alih menetapkan daftar alat selama masa hidup percakapan, Anda mengubah alat mana yang ditawarkan kepada model di antara giliran: deklarasikan set alat lengkap di `tools` sejak awal, lalu gunakan blok `tool_addition` dan `tool_removal` untuk menawarkan alat kepada model, atau menariknya, mulai dari titik tertentu dalam percakapan dan seterusnya. Array `tools` itu sendiri tidak pernah berubah, sehingga prefiks yang di-cache tetap utuh.

`tool_addition` dan `tool_removal` adalah blok konten dalam array `content` dari pesan `role: "system"`, dan keduanya dapat dicampur dengan blok `text` dalam pesan yang sama. Pesan tersebut mengikuti aturan penempatan yang sama seperti pesan sistem di tengah percakapan lainnya (lihat [Keterbatasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)), dan perubahan berlaku mulai dari titik itu dalam percakapan dan seterusnya. Field `tool` pada setiap blok mereferensikan alat, bukan mendefinisikannya: `{"type": "tool_reference", "name": "..."}` menyebut nama alat yang dideklarasikan dalam array `tools` permintaan, dan alat [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector) dapat direferensikan satu per satu dengan `mcp_tool_reference` (`server_name` dan `name`) atau sebagai keseluruhan toolset dengan `mcp_toolset_reference` (`server_name`). Mereferensikan nama yang tidak dideklarasikan di `tools` mengembalikan error 400.

Setiap alat yang dideklarasikan di `tools` ditawarkan kepada model sejak awal percakapan kecuali dideklarasikan dengan `defer_loading: true`, yang membuatnya tetap ditahan hingga blok `tool_addition` memunculkannya. `tool_addition` juga menawarkan kembali alat yang sebelumnya ditarik oleh `tool_removal`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mid-conversation-tool-changes-2026-07-01" \
    -d '{
      "model": "claude-opus-5",
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
  ant beta:messages create --beta mid-conversation-tool-changes-2026-07-01 \
    --transform 'content.#(type=="text").text' --raw-output <<'YAML'
  model: claude-opus-5
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
      model="claude-opus-5",
      max_tokens=1024,
      betas=["mid-conversation-tool-changes-2026-07-01"],
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
          # Tarik get_weather mulai dari titik ini. Blok ini merujuk
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
    model: "claude-opus-5",
    max_tokens: 1024,
    betas: ["mid-conversation-tool-changes-2026-07-01"],
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
      // Tarik get_weather mulai dari titik ini. Blok ini merujuk ke
      // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
      // identik per byte dan cache tetap kena.
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
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5,
      MaxTokens = 1024,
      Betas = ["mid-conversation-tool-changes-2026-07-01"],
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
          // Tarik get_weather mulai dari titik ini. Blok ini merujuk
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
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{"mid-conversation-tool-changes-2026-07-01"},
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
  		// Tarik get_weather mulai dari titik ini. Blok ini merujuk
  		// alat berdasarkan nama alih-alih mengedit Tools, sehingga giliran sebelumnya tetap
  		// identik per byte dan cache tetap hit.
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
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaRequestToolRemovalBlock;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Set alat lengkap dideklarasikan di awal dan tidak pernah berubah, sehingga
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
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .addBeta("mid-conversation-tool-changes-2026-07-01")
          .addTool(weatherTool)
          .addUserMessage("Say OK.")
          // Tarik get_weather mulai dari titik ini. Blok ini merujuk
          // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
          // identik per byte dan cache tetap hit.
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
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 1024,
      betas: ['mid-conversation-tool-changes-2026-07-01'],
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
          // Tarik get_weather mulai dari titik ini. Blok ini merujuk
          // alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
          // identik per byte dan cache tetap hit.
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
    model: "claude-opus-5",
    max_tokens: 1024,
    betas: ["mid-conversation-tool-changes-2026-07-01"],
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
      # Tarik get_weather mulai dari titik ini. Blok ini merujuk
      # alat berdasarkan nama alih-alih mengedit `tools`, sehingga giliran sebelumnya tetap
      # identik per byte dan cache tetap terkena (hit).
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

Perubahan alat di tengah percakapan berada dalam versi beta. Untuk menggunakannya, sertakan header beta `mid-conversation-tool-changes-2026-07-01` dalam permintaan Anda.

## Kapan menggunakan pesan sistem di tengah percakapan

[Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) meng-hash prefiks permintaan secara berurutan: `tools`, lalu `system`, lalu `messages`. Cache hit mengharuskan prefiks cocok persis dengan permintaan terbaru, byte demi byte, hingga breakpoint cache.

Urutan itu berarti field `system` tingkat atas berada di dekat bagian paling awal dari prefiks yang di-hash. Perubahan apa pun padanya, bahkan menambahkan satu kalimat, menghasilkan hash yang berbeda, dan permintaan tersebut melewatkan cache untuk prompt sistem dan setiap pesan yang di-cache setelahnya.

Pesan sistem di tengah percakapan memungkinkan Anda menambahkan instruksi di **akhir** riwayat pesan sebagai gantinya. Semua yang ada sebelum instruksi baru tidak berubah, sehingga entri cache yang ada masih cocok, dan hanya pesan baru yang diproses sebagai input baru.

Beberapa situasi di mana hal ini penting:

* **Perubahan kebijakan atau persona di tengah sesi.** Sesi agentik yang panjang memerlukan batasan baru ("mulai sekarang, tulis semua SQL sebagai kueri berparameter") setelah puluhan giliran yang di-cache. Menambahkannya ke field `system` tingkat atas akan memproses ulang seluruh riwayat.
* **Konteks per giliran yang harus bersifat otoritatif.** Anda ingin menyisipkan catatan kesegaran, tenggat sesi, atau perubahan ketersediaan alat dengan bobot tingkat sistem, dan hal itu berubah terlalu sering untuk berada dalam prefiks yang di-cache.
* **Pengingat per giliran yang tidak boleh menumpuk.** Sebuah harness mendorong model setelah setiap batch hasil alat ("minta pembacaan independen secara bersamaan", "pengguna sudah lama tidak mendengar kabar dari Anda") dan ingin model hanya melihat salinan terbaru. [Pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dirender untuk satu giliran lalu tidak memakan biaya apa pun, tanpa menghapus apa pun dari riwayat.
* **Perubahan status yang diamati aplikasi Anda.** Aplikasi Anda menyadari sesuatu yang harus diperlakukan Claude sebagai fakta tingkat operator: file berubah di disk, pengguna mengubah pengaturan persetujuan otomatis, alat yang tersedia berubah, atau sisa anggaran token turun di bawah ambang batas.
* **Input pengguna yang tidak boleh menginterupsi loop agentik.** Pengguna mengetik tindak lanjut saat Claude masih mengeksekusi alat untuk permintaan sebelumnya. Meneruskannya sebagai pesan sistem setelah hasil alat berikutnya memungkinkan Claude menggabungkan input baru ke dalam pekerjaan yang sedang dilakukannya, alih-alih memperlakukannya sebagai permintaan baru untuk beralih. Lihat [Penempatan setelah hasil alat](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#placement-after-tool-results).
* **Peralihan mode yang memberikan izin tetap.** Mode tingkat sesi dapat menggunakan pesan sistem di tengah percakapan untuk memberikan persetujuan tetap terhadap kapabilitas yang mahal, seperti meluncurkan alur kerja multiagen secara otomatis, dengan penyegaran singkat setiap beberapa giliran dan pemberitahuan keluar saat mode dimatikan. Untuk contoh lengkap, lihat [Membangun mode orkestrasi](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-effort-example).

Dalam semua kasus ini Anda dapat menempatkan instruksi dalam pesan `user` biasa, dan Claude memang mengikuti instruksi yang datang dalam giliran pengguna. Perbedaannya adalah prioritas: pesan `user` diperlakukan sebagai berasal dari pengguna akhir, sedangkan pesan `system` diperlakukan sebagai berasal dari Anda, operator aplikasi. Ketika keduanya bertentangan, instruksi sistem diutamakan, jadi gunakan role `system` untuk fakta dan batasan tingkat operator yang harus tetap berlaku meskipun pengguna akhir meminta sesuatu yang berbeda. Pesan sistem di tengah percakapan mempertahankan prioritas tingkat operator itu tanpa membayar biaya cache miss akibat mengedit field `system` tingkat atas.

## Cara kerjanya

Tambahkan pesan dengan `"role": "system"` ke array `messages`. Gunakan string biasa atau blok konten untuk `content`, sama seperti giliran `user` atau `assistant`. Instruksi berlaku mulai dari titik itu dalam percakapan dan seterusnya. Ketika instruksi bertentangan, pesan sistem yang lebih baru diutamakan daripada yang lebih lama, dan pesan sistem di tengah percakapan diutamakan daripada field `system` tingkat atas untuk giliran yang mengikutinya.

Anda masih dapat mengatur field `system` tingkat atas untuk instruksi yang harus berlaku untuk seluruh percakapan. Cadangkan pesan sistem di tengah percakapan untuk instruksi yang baru menjadi relevan kemudian, atau yang ingin Anda tambahkan tanpa membatalkan prefiks yang di-cache.

Pesan `role: "system"` juga dapat membawa `output_config.effort` untuk mengubah tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) mulai dari giliran `user` berikutnya. Ini berada dalam versi beta di Claude Fable 5.1, Claude Mythos 5.1, dan Claude Opus 5 di Claude API dan memerlukan header beta `mid-conversation-output-config-2026-07-01`. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
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
  model: claude-opus-5
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
      model="claude-opus-5",
      max_tokens=1024,
      # Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
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
          # lolos kebijakan strict typing tim. Menambahkan instruksi
          # di sini menjaga giliran sebelumnya tetap identik per byte, sehingga
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
    model: "claude-opus-5",
    max_tokens: 1024,
    // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
    // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
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
      // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
      // kebijakan pengetikan ketat milik tim. Menambahkan instruksi di sini menjaga
      // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
      // permintaan sebelumnya masih dibaca dari cache.
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
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
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
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
          // kebijakan strict typing tim. Menambahkan instruksi di sini menjaga
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
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	// Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
  	// dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
  	CacheControl: anthropic.NewCacheControlEphemeralParam(),
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a code review assistant. Be concise."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review process() in utils.py for performance issues.")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Now review the calling code that invokes process().")),
  		// Peninjau menyadari di tengah sesi bahwa semua saran juga harus
  		// lolos kebijakan strict typing tim. Menambahkan instruksi
  		// di sini menjaga giliran sebelumnya identik per byte, sehingga prefiks yang di-cache oleh
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
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
          // dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
          .cacheControl(CacheControlEphemeral.builder().build())
          .system("You are a code review assistant. Be concise.")
          .addUserMessage("Review process() in utils.py for performance issues.")
          .addAssistantMessage("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")
          .addUserMessage("Now review the calling code that invokes process().")
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
          // kebijakan pengetikan ketat milik tim. Menambahkan instruksi di sini menjaga
          // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
          // permintaan sebelumnya masih dibaca dari cache.
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
          // Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
          // kebijakan pengetikan ketat milik tim. Menambahkan instruksi di sini menjaga
          // giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
          // permintaan sebelumnya masih dibaca dari cache.
          ['role' => 'system', 'content' => 'From now on, every suggestion must include explicit type annotations.']
      ],
      model: 'claude-opus-5',
      // Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
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
    model: "claude-opus-5",
    max_tokens: 1024,
    # Caching prompt otomatis: setiap permintaan meng-cache percakapan sejauh ini,
    # dan permintaan berikutnya membaca prefiks yang tidak berubah dari cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      { role: "user", content: "Review process() in utils.py for performance issues." },
      { role: "assistant", content: "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list." },
      { role: "user", content: "Now review the calling code that invokes process()." },
      # Peninjau menyadari di tengah sesi bahwa semua saran juga harus lolos
      # kebijakan typing ketat milik tim. Menambahkan instruksi di sini menjaga
      # giliran sebelumnya tetap identik per byte, sehingga prefiks yang di-cache oleh
      # permintaan sebelumnya masih dibaca dari cache.
      { role: "system", content: "From now on, every suggestion must include explicit type annotations." }
    ]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

Contoh ini mengaktifkan [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) dengan field `cache_control` tingkat atas. Caching prompt bersifat opt-in: jika permintaan tidak memiliki field `cache_control` (otomatis atau [breakpoint eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints)), tidak ada yang di-cache dan setiap permintaan membayar harga token input reguler untuk seluruh percakapan. Dengan caching diaktifkan, menambahkan pesan sistem membiarkan giliran yang sudah di-cache tidak berubah, sehingga permintaan yang membawa instruksi baru masih membacanya dari cache alih-alih memprosesnya lagi. Caching juga mengharuskan percakapan memenuhi [panjang prompt minimum yang dapat di-cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations); contoh sesingkat ini berada di bawahnya, sehingga `cache_creation_input_tokens` dan `cache_read_input_tokens` tetap 0 hingga percakapan bertambah panjang.

Pesan sistem di tengah percakapan harus langsung mengikuti giliran `user` (atau giliran `assistant` yang berakhir dengan hasil alat server), dan harus menjadi entri terakhir di `messages` atau langsung diikuti oleh giliran `assistant`. Pesan `user` yang membawa blok `tool_result` termasuk: dalam loop agentik Anda dapat menempatkan pesan sistem tepat setelah hasil alat, sebelum giliran Claude berikutnya. Posisi lain apa pun, termasuk di antara blok `tool_use` `assistant` dan `tool_result` yang menjawabnya, mengembalikan error 400.

### Penempatan setelah hasil alat

Dalam [loop agentik](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview), pesan sistem ditempatkan setelah pesan `user` yang menyampaikan hasil alat. Di sini juga aplikasi Anda dapat meneruskan input yang diketik pengguna saat Claude sedang bekerja, sehingga konteks baru diserap tanpa memulai ulang giliran:

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

Rumuskan konten sistem sebagai konteks, bukan sebagai perintah yang mengesampingkan pengguna. Nyatakan faktanya ("input baru tiba dari pengguna: X", "sisa anggaran token sekarang Y") dan biarkan Claude bertindak berdasarkan itu. Claude dilatih untuk menolak instruksi yang tampak bekerja melawan pengguna, dan perlindungan itu tetap berlaku untuk role sistem, sehingga bahasa seperti "abaikan apa yang dikatakan pengguna" kurang efektif dibandingkan menyatakan apa yang berubah.

Pola ini untuk meneruskan input dari pengguna akhir percakapan itu sendiri. Jangan menggunakannya untuk meneruskan output alat, dokumen yang diambil, atau konten pihak ketiga lainnya; simpan konten itu dalam blok `tool_result` (lihat [Keterbatasan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)).

### Pesan sistem dengan cakupan giliran

Untuk membatasi cakupan pesan `role: "system"` pada giliran saat ini, atur field `clear_at`-nya. Field ini menerima salah satu dari dua nilai:

* `"never"` (default): pesan dirender pada posisinya di setiap permintaan yang menyertakannya. Menghilangkan field ini hasilnya identik.
* `"next_user_message"`: pesan **bercakupan giliran**. Teksnya hanya dirender selama tidak ada pesan `role: "user"` yang datang setelahnya di `messages`. Pesan pengguna yang hanya membawa blok `tool_result` dihitung sebagai pesan pengguna di sini. Begitu ada pesan pengguna yang lebih baru, pesan tersebut **dibersihkan**: pesan tetap berada dalam array tetapi tidak merender apa pun dan tidak memakan biaya token input, pada permintaan itu dan setiap permintaan berikutnya.

Pesan sistem dengan cakupan giliran berada dalam versi beta. Sertakan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-system-clear-at-2026-08-21`. Tanpanya, `clear_at` ditolak sebagai field yang tidak dikenal.

```json
{
  "role": "system",
  "clear_at": "next_user_message",
  "content": "First privately list what you need next; then request every item that doesn't depend on another's result in this one response."
}
```

Penggunaan utamanya adalah pengingat per giliran dalam loop alat. Tambahkan pengingat setelah pesan `tool_result` setiap kali Anda ingin model melihatnya, dan biarkan setiap salinan sebelumnya di tempatnya. Model hanya melihat salinan yang datang setelah pesan pengguna terakhir, sehingga pengingat tidak pernah menumpuk. Tidak ada yang berubah pada bagian awal `messages`, sehingga [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) tetap cocok. Di Claude Fable 5.1 ini juga menjaga [blok thinking berikutnya tetap valid](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation): menghapus pengingat sebelumnya akan mengubah percakapan sebelum blok-blok itu dan menggagalkan pemeriksaan percakapan, sedangkan pesan yang dibersihkan tetap berada dalam array dan membiarkan percakapan itu tidak berubah.

Permintaan berikut adalah langkah lanjutan dari loop agen. `messages[3]` dirender pada permintaan sebelumnya, ketika ia menjadi pesan terakhir dalam array. Begitu `messages[5]` (pesan pengguna yang lebih baru) ada, `messages[3]` dibersihkan: pesan yang dibersihkan tetap berada dalam array, sehingga percakapan sebelum blok thinking di `messages[4]` tidak berubah, tetapi model tidak lagi melihat teksnya. `messages[6]` dan `messages[7]` keduanya dirender, secara berurutan.

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

Aturan untuk pesan bercakupan giliran:

* **Kirim ulang pesan yang dibersihkan secara verbatim.** Pesan yang dibersihkan masih merupakan bagian dari riwayat percakapan. Membangunnya kembali dari status saat ini (jumlah token baru, stempel waktu), membuangnya karena dianggap redundan, atau mengubah nilai `clear_at`-nya merupakan pengeditan terhadap pesan sebelumnya. Cache prompt meleset mulai dari titik itu, dan di Claude Fable 5.1 setiap blok thinking yang dihasilkan setelahnya gagal dalam [pemeriksaan percakapan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation).
* **Hanya teks.** `content` berupa satu atau lebih blok `text` (atau string). Blok `tool_addition` dan `tool_removal` mengembalikan error 400 pada pesan bercakupan giliran, begitu pula `output_config`. Gunakan pesan `role: "system"` terpisah tanpa `clear_at` untuk itu.
* **Tidak ada `cache_control` pada bloknya.** Pesan yang dibersihkan tidak pernah menjadi bagian dari kunci cache, sehingga breakpoint padanya tidak akan pernah cocok. Letakkan breakpoint pada blok terakhir dari giliran pengguna sebelumnya, seperti pada contoh. Field [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) tingkat atas melewati pesan bercakupan giliran saat memilih breakpoint. Pada permintaan yang membersihkan pesan, prefiks cache yang dapat digunakan kembali berakhir pada giliran pengguna sebelumnya, sehingga hanya satu giliran asisten di antara pesan itu dan pesan pengguna baru yang diproses ulang.
* **Aturan penempatan tetap berlaku**, dibersihkan atau tidak. Pesan bercakupan giliran harus mengikuti giliran `user` (atau giliran `assistant` yang berakhir dengan hasil alat server) dan mendahului giliran `assistant` atau mengakhiri array, seperti pesan sistem di tengah percakapan lainnya. Pesan yang mengakhiri array selalu dirender. Pesan yang langsung diikuti oleh pesan `user` lain adalah error 400, bukan pesan yang dibersihkan: letakkan semua hasil dari satu putaran alat dalam satu pesan pengguna dan pengingat setelahnya.
* **Giliran asisten tidak membersihkannya.** Giliran asisten yang di-prefill atau [dijeda](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#pause-turn) setelah pesan tersebut, atau loop alat sisi server, tidak menambahkan pesan pengguna, sehingga pesan masih dirender pada kelanjutan itu. Untuk menjaga pengingat tetap terlihat sepanjang loop alat sisi klien, tambahkan lagi setelah setiap pesan `tool_result`.
* **Penghitungan token mengikuti apa yang dirender.** Pesan yang dibersihkan tidak menambahkan apa pun ke `usage.input_tokens` atau ke [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).
* **Riwayat yang diimpor.** Dalam transkrip yang Anda susun dalam satu langkah (contoh few-shot, percakapan yang dimigrasikan), pesan bercakupan giliran yang sudah memiliki giliran asisten dan pesan pengguna setelahnya dibersihkan sejak permintaan pertama dan tidak pernah dirender. Itu adalah status yang tepat untuk pengingat per giliran yang Anda bawa. Biarkan `clear_at` tidak diatur hanya pada pesan yang harus dilihat model di setiap permintaan.

Error validasinya adalah:

```text wrap
messages.3.clear_at: Extra inputs are not permitted
messages.3.clear_at: clear_at is only permitted on role 'system' messages
messages.3.clear_at: Input should be 'next_user_message' or 'never'
messages.3: a turn-scoped system message supports text blocks only (clear_at: 'next_user_message')
messages.3: output_config is not permitted on a turn-scoped system message (clear_at: 'next_user_message')
messages.3.content.0: cache_control is not permitted on a turn-scoped system message (clear_at: 'next_user_message')
```

Yang pertama adalah error yang dikembalikan tanpa header beta. Di Amazon Bedrock dan Google Cloud, teruskan nilai beta seperti dijelaskan dalam [Header beta](https://platform.claude.com/docs/id/api/beta-headers).

Melalui SDK, atur `clear_at` pada entri `role: "system"` di `messages` dan kirim header beta. Contoh berikut menambahkan pengingat bercakupan giliran setelah giliran pengguna; pada permintaan berikutnya, begitu ada pesan pengguna yang lebih baru, pengingat tetap berada dalam array tetapi tidak lagi dirender:

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

* **Aktifkan caching secara eksplisit.** Caching hanya terjadi ketika permintaan menyertakan `cache_control`, baik field [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) tingkat atas maupun [breakpoint eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints) pada blok konten. Pesan sistem di tengah percakapan tidak membuat entri cache dengan sendirinya, dan tanpa caching diaktifkan tidak ada penghematan yang perlu dipertahankan.
* **Cache prefiks yang stabil seperti biasa.** Letakkan `cache_control` pada blok terakhir yang tetap sama di seluruh permintaan, baik itu akhir dari field `system` tingkat atas, akhir dari definisi alat Anda, atau titik stabil dalam riwayat pesan.
* **Tambahkan pesan sistem setelah breakpoint.** Karena ia datang setelah prefiks yang di-cache, ia tidak mengubah hash prefiks dan cache tetap hit.
* **Pesan sistem di tengah percakapan itu sendiri dapat di-cache.** Begitu berada dalam percakapan, ia menjadi bagian dari riwayat yang stabil. Pada giliran berikutnya Anda dapat memindahkan breakpoint cache melewatinya (atau mengandalkan [caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) untuk melakukannya) dan pesan sistem dibaca dari cache seperti giliran lainnya.

Hindari mengedit atau menghapus pesan sistem di tengah percakapan yang sudah dikirim. Seperti perubahan lain pada pesan sebelumnya, hal itu membatalkan cache mulai dari titik itu dan seterusnya. Di Claude Fable 5.1 hal itu juga membatalkan [blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation) di setiap giliran asisten berikutnya. Untuk panduan yang hanya berlaku untuk satu giliran, gunakan [pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dan biarkan di tempatnya. Jika instruksi perlu berkembang, tambahkan pesan sistem baru alih-alih menulis ulang yang lama. Pesan sistem berurutan diterima dan diperlakukan sebagai satu bagian sistem, yang mengikuti aturan penempatan yang sama secara keseluruhan.

## Keterbatasan

* **Bukan untuk pesan pertama.** Pesan `system` yang membawa konten tidak dapat menjadi entri pertama di `messages`. Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal.
* **Penempatan dibatasi.** Pesan `system` yang membawa konten (blok `text`, `tool_addition`, atau `tool_removal`) harus langsung mengikuti giliran `user` (termasuk giliran `user` yang membawa blok `tool_result`) atau giliran `assistant` yang berakhir dengan hasil alat server, dan harus mendahului giliran `assistant` atau mengakhiri array. Pesan ini tidak dapat berada di antara blok `tool_use` dan `tool_result`-nya. Menempatkannya di tempat lain mengembalikan error 400. Pesan dengan `content` kosong yang hanya mengatur [`output_config.effort`](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) tidak merender apa pun pada posisinya dan diterima di mana saja dalam `messages`, termasuk di posisi pertama atau di antara giliran `assistant` dan giliran `user`. Pesan `system` berurutan dinilai bersama, sehingga menambahkan pesan yang membawa teks di sebelah pesan yang hanya berisi effort membuat seluruh kelompok mengikuti aturan konten.
* **Pesan bercakupan giliran hanya berisi teks dan dikirim ulang secara verbatim.** Pesan `clear_at: "next_user_message"` tidak membawa `tool_addition`, `tool_removal`, `output_config`, atau `cache_control`, dan begitu dibersihkan ia harus tetap berada di `messages` byte demi byte pada permintaan berikutnya. Lihat [Pesan sistem dengan cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages).
* **Bukan tempat untuk konten yang tidak tepercaya.** Claude memperlakukan konten sistem sebagai instruksi operator dan mengikutinya. Jangan menempatkan teks dari luar percakapan, seperti output alat mentah, dokumen yang diambil, atau konten web, langsung dalam pesan sistem; melakukannya memberi teks itu otoritas tingkat operator. Simpan data itu dalam blok `tool_result` dan terus ikuti [Mitigasi jailbreak dan injeksi prompt](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks).

## Terkait

<CardGroup cols={2}>
  <Card title="Caching prompt" icon="bolt" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Cara kerja caching, di mana menempatkan breakpoint, dan cara membaca field penggunaan cache.
  </Card>

  <Card title="Diagnostik cache" icon="magnifying-glass" href="https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics">
    Cari tahu persis di mana dua permintaan berbeda ketika cache hit yang Anda harapkan tidak terjadi.
  </Card>

  <Card title="Menggunakan Messages API" icon="message" href="https://platform.claude.com/docs/id/build-with-claude/working-with-messages">
    Struktur pesan, percakapan multi-giliran, dan field `system`.
  </Card>

  <Card title="Praktik terbaik prompting" icon="text" href="https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Menulis prompt dan instruksi sistem yang efektif.
  </Card>

  <Card title="Penggunaan alat dengan Claude" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview">
    Bagaimana blok `tool_use` dan `tool_result` disusun dalam array `messages`.
  </Card>
</CardGroup>
