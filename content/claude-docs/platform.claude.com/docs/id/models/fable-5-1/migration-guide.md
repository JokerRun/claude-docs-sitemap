---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-1/migration-guide
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 6f28b3cae4474920540c2955263d1eb60b4391a49e1cce43bac06f1d3439dd35
---

---
title: Panduan migrasi Claude Fable 5.1 dan Claude Mythos 5.1
url: https://platform.claude.com/docs/id/models/fable-5-1/migration-guide
description: Beralih ke Claude Fable 5.1 dan Claude Mythos 5.1 dari Claude Fable 5, Claude Mythos 5, Claude Opus 5, atau Claude Opus 4.8 dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Fable 5.1 dan Claude Mythos 5.1 mencakup ID model, perubahan yang dapat merusak, dan daftar periksa migrasi.
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

Biarkan Claude Code memigrasikan kode Anda

```text
/claude-api migrate proyek ini ke claude-fable-5-1
```

[Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) menggantikan Claude Fable 5 dengan harga input dan output yang sama, dengan pembacaan cache seharga seperempat biayanya. Model ini tersedia di Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). Claude Fable 5.1 tidak memerlukan persetujuan akses. [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview) memiliki kemampuan yang sama dan hanya tersedia bagi organisasi yang telah diverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Untuk meminta akses, daftarlah ke program yang mencakup kasus penggunaan Anda atau hubungi tim akun Anthropic Anda. Untuk perbedaan perilaku dan pola prompting, lihat [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).

Pengaturan dasar yang dimiliki bersama oleh `claude-fable-5-1` dan `claude-mythos-5-1`:

* **Thinking:** [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif, tidak berubah dari Claude Fable 5. Model menentukan kapan dan seberapa banyak berpikir. Tidak diperlukan konfigurasi `thinking`. Baik `thinking: {type: "disabled"}` maupun “extended thinking” (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Prefill:** Melakukan prefill pada pesan asisten mengembalikan error 400, tidak berubah dari Claude Fable 5. Gunakan instruksi prompt sistem sebagai gantinya.
* **Tool choice:** `{type: "auto"}` (default) dan `{type: "none"}` didukung. Memaksa pemanggilan alat dengan `{type: "any"}` atau `{type: "tool", name: "..."}` mengembalikan error 400. Lihat [Perubahan yang dapat merusak](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).
* **Pemikiran yang dipertahankan lintas model:** Claude Fable 5.1 dan Claude Mythos 5.1 dapat membaca blok pemikiran dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude sebelumnya. Tidak satu pun dari model-model tersebut yang dapat membaca blok dari Claude Fable 5.1 atau Claude Mythos 5.1. Lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).
* **Pengeditan pada giliran sebelumnya:** Blok pemikiran hanya tetap valid selama semua yang dikirim sebelumnya tidak berubah, jadi pertahankan riwayat percakapan agar hanya bersifat tambahan (append-only). Lihat [Mengedit giliran sebelumnya membuat blok pemikiran tidak valid](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking).
* **Jendela konteks dan output:** Kedua model memiliki [“context window” (jendela konteks) sebesar 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) dan mengembalikan hingga 128k token output untuk setiap permintaan.
* **Harga:** $10 USD per juta token input dan $50 USD per juta token output, sama seperti Claude Fable 5. Pembacaan cache prompt seharga $0,25 USD per juta token, seperempat dari tarif Claude Fable 5. Lihat [Harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
* **Retensi data:** Kedua model memerlukan retensi data 30 hari, tidak tersedia di bawah pengaturan zero data retention (ZDR) kecuali secara tegas diizinkan oleh Anthropic, dan ditetapkan sebagai Covered Models, sama seperti Claude Fable 5 dan Claude Mythos 5. Di Claude API, permintaan dari organisasi atau workspace tanpa retensi 30 hari mengembalikan 400 `invalid_request_error`. Organisasi dengan pengaturan ZDR sebaiknya menghubungi tim akun Anthropic mereka atau mengonfigurasi retensi untuk workspace individual. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.
* **Priority Tier:** Tidak satu pun dari kedua model didukung di [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models). Claude Fable 5 didukung.

## Migrasi ke Claude Fable 5.1 dari Claude Fable 5

Migrasi sebagian besar bersifat drop-in. Permukaan API, batas, harga per token, tokenizer, adaptive thinking yang selalu aktif, penanganan penolakan, dan kategori `stop_details` semuanya sama dengan Claude Fable 5. Perubahan berikut berlaku:

* Permintaan yang memaksa pemanggilan alat akan mendapatkan error 400.
* Hanya Claude Fable 5.1 dan Claude Mythos 5.1 yang dapat membaca blok pemikiran Claude Fable 5.1.
* [Mengedit giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking) membuat blok pemikiran berikutnya menjadi tidak valid.
* Pembacaan cache lebih murah.
* Advisor tool (beta) menerima lebih sedikit advisor.
* Perilaku agent loop berbeda dalam tiga hal.

### Perbarui nama model Anda

```python
model = "claude-fable-5"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk Claude Mythos 5.1, yang menawarkan kemampuan yang sama bagi organisasi terverifikasi:
model = "claude-mythos-5-1"  # After
```

### Perubahan yang dapat merusak

1. **Tool choice yang dipaksakan tidak didukung:** Claude Fable 5 menerima `tool_choice` `auto`, `none`, `any`, dan `tool`. Di `claude-fable-5-1`, `{type: "any"}` dan `{type: "tool", name: "..."}` mengembalikan 400 `invalid_request_error`:

   ```text wrap
   tool_choice: type "tool" and "any" are not supported for this model.
   ```

   Pemeriksaan ini berlaku di Messages API, Message Batches API, dan endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

   Sebelum (Claude Fable 5):

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-fable-5",
         "max_tokens": 16000,
         "tools": [
           {
             "name": "record_summary",
             "description": "Record the structured summary of the document.",
             "input_schema": {
               "type": "object",
               "properties": {"summary": {"type": "string"}},
               "required": ["summary"]
             }
           }
         ],
         "tool_choice": {"type": "tool", "name": "record_summary"},
         "messages": [
           {"role": "user", "content": "Summarize: The meeting moved to Thursday."}
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-fable-5
     max_tokens: 16000
     tools:
       - name: record_summary
         description: Record the structured summary of the document.
         input_schema:
           type: object
           properties:
             summary:
               type: string
           required: [summary]
     tool_choice:
       type: tool
       name: record_summary
     messages:
       - role: user
         content: "Summarize: The meeting moved to Thursday."
     YAML
     ```

     ```python Python
     client = anthropic.Anthropic()

     record_summary_tool = {
         "name": "record_summary",
         "description": "Record the structured summary of the document.",
         "input_schema": {
             "type": "object",
             "properties": {"summary": {"type": "string"}},
             "required": ["summary"],
         },
     }

     response = client.messages.create(
         model="claude-fable-5",
         max_tokens=16000,
         tools=[record_summary_tool],
         tool_choice={"type": "tool", "name": "record_summary"},
         messages=[{"role": "user", "content": "Summarize: The meeting moved to Thursday."}],
     )
     print(response.content)
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.messages.create({
       model: "claude-fable-5",
       max_tokens: 16000,
       tools: [
         {
           name: "record_summary",
           description: "Record the structured summary of the document.",
           input_schema: {
             type: "object",
             properties: { summary: { type: "string" } },
             required: ["summary"]
           }
         }
       ],
       tool_choice: { type: "tool", name: "record_summary" },
       messages: [{ role: "user", content: "Summarize: The meeting moved to Thursday." }]
     });

     console.log(response.content);
     ```

     ```csharp C#
     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeFable5,
         MaxTokens = 16000,
         Tools = [
             new ToolUnion(new Tool()
             {
                 Name = "record_summary",
                 Description = "Record the structured summary of the document.",
                 InputSchema = new InputSchema()
                 {
                     Properties = new Dictionary<string, JsonElement>
                     {
                         ["summary"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                     },
                     Required = ["summary"],
                 },
             }),
         ],
         ToolChoice = new ToolChoiceTool { Name = "record_summary" },
         Messages = [new UserMessageParam { Content = "Summarize: The meeting moved to Thursday." }]
     };

     var message = await client.Messages.Create(parameters);
     Console.WriteLine(message);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeFable5,
     	MaxTokens: 16000,
     	Tools: []anthropic.ToolUnionParam{
     		{OfTool: &anthropic.ToolParam{
     			Name:        "record_summary",
     			Description: anthropic.String("Record the structured summary of the document."),
     			InputSchema: anthropic.ToolInputSchemaParam{
     				Properties: map[string]any{
     					"summary": map[string]any{"type": "string"},
     				},
     				Required: []string{"summary"},
     			},
     		}},
     	},
     	ToolChoice: anthropic.ToolChoiceUnionParam{OfTool: &anthropic.ToolChoiceToolParam{Name: "record_summary"}},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize: The meeting moved to Thursday.")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response.RawJSON())
     ```

     ```java Java

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model(Model.CLAUDE_FABLE_5)
             .maxTokens(16000L)
             .addTool(Tool.builder()
                 .name("record_summary")
                 .description("Record the structured summary of the document.")
                 .inputSchema(InputSchema.builder()
                     .properties(JsonValue.from(Map.of("summary", Map.of("type", "string"))))
                     .required(List.of("summary"))
                     .build())
                 .build())
             .toolChoice(ToolChoice.ofTool(ToolChoiceTool.builder()
                 .name("record_summary")
                 .build()))
             .addUserMessage("Summarize: The meeting moved to Thursday.")
             .build();

         Message response = client.messages().create(params);
         IO.println(response);
     }
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [
             ['role' => 'user', 'content' => 'Summarize: The meeting moved to Thursday.']
         ],
         model: Model::CLAUDE_FABLE_5,
         toolChoice: ['type' => 'tool', 'name' => 'record_summary'],
         tools: [
             [
                 'name' => 'record_summary',
                 'description' => 'Record the structured summary of the document.',
                 'input_schema' => [
                     'type' => 'object',
                     'properties' => [
                         'summary' => ['type' => 'string']
                     ],
                     'required' => ['summary']
                 ]
             ]
         ],
     );

     echo $message;
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: Anthropic::Model::CLAUDE_FABLE_5,
       max_tokens: 16000,
       tools: [
         {
           name: "record_summary",
           description: "Record the structured summary of the document.",
           input_schema: {
             type: "object",
             properties: { summary: { type: "string" } },
             required: ["summary"]
           }
         }
       ],
       tool_choice: { type: "tool", name: "record_summary" },
       messages: [
         { role: "user", content: "Summarize: The meeting moved to Thursday." }
       ]
     )
     puts message
     ```
   </CodeGroup>

   Sesudah (Claude Fable 5.1): biarkan `tool_choice` pada `auto`, sebutkan nama alat dalam instruksi, dan atur `strict: true` agar pemanggilan sesuai dengan skema Anda. (Dalam organisasi [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek), di mana [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), termasuk `strict: true`, tidak tersedia pada model Claude Fable, andalkan instruksi saja.) Sebagai contoh:

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-fable-5-1",
         "max_tokens": 16000,
         "tools": [
           {
             "name": "record_summary",
             "description": "Record the structured summary of the document.",
             "strict": true,
             "input_schema": {
               "type": "object",
               "properties": {"summary": {"type": "string"}},
               "required": ["summary"],
               "additionalProperties": false
             }
           }
         ],
         "tool_choice": {"type": "auto"},
         "messages": [
           {"role": "user", "content": "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result."}
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-fable-5-1
     max_tokens: 16000
     tools:
       - name: record_summary
         description: Record the structured summary of the document.
         strict: true
         input_schema:
           type: object
           properties:
             summary:
               type: string
           required: [summary]
           additionalProperties: false
     tool_choice:
       type: auto
     messages:
       - role: user
         content: "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result."
     YAML
     ```

     ```python Python
     client = anthropic.Anthropic()

     record_summary_tool = {
         "name": "record_summary",
         "description": "Record the structured summary of the document.",
         "strict": True,
         "input_schema": {
             "type": "object",
             "properties": {"summary": {"type": "string"}},
             "required": ["summary"],
             "additionalProperties": False,
         },
     }

     response = client.messages.create(
         model="claude-fable-5-1",
         max_tokens=16000,
         tools=[record_summary_tool],
         tool_choice={"type": "auto"},
         messages=[
             {
                 "role": "user",
                 "content": "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result.",
             }
         ],
     )
     print(response.content)
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.messages.create({
       model: "claude-fable-5-1",
       max_tokens: 16000,
       tools: [
         {
           name: "record_summary",
           description: "Record the structured summary of the document.",
           strict: true,
           input_schema: {
             type: "object",
             properties: { summary: { type: "string" } },
             required: ["summary"],
             additionalProperties: false
           }
         }
       ],
       tool_choice: { type: "auto" },
       messages: [
         {
           role: "user",
           content:
             "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result."
         }
       ]
     });

     console.log(response.content);
     ```

     ```csharp C#
     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeFable5_1,
         MaxTokens = 16000,
         Tools = [
             new ToolUnion(new Tool()
             {
                 Name = "record_summary",
                 Description = "Record the structured summary of the document.",
                 Strict = true,
                 InputSchema = new InputSchema(new Dictionary<string, JsonElement>
                 {
                     ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                     {
                         ["summary"] = new { type = "string" },
                     }),
                     ["required"] = JsonSerializer.SerializeToElement(new[] { "summary" }),
                     ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                 }),
             }),
         ],
         ToolChoice = new ToolChoiceAuto(),
         Messages = [
             new UserMessageParam { Content = "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result." }
         ]
     };

     var message = await client.Messages.Create(parameters);
     Console.WriteLine(message);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeFable5_1,
     	MaxTokens: 16000,
     	Tools: []anthropic.ToolUnionParam{
     		{OfTool: &anthropic.ToolParam{
     			Name:        "record_summary",
     			Description: anthropic.String("Record the structured summary of the document."),
     			Strict:      anthropic.Bool(true),
     			InputSchema: anthropic.ToolInputSchemaParam{
     				Properties: map[string]any{
     					"summary": map[string]any{"type": "string"},
     				},
     				Required: []string{"summary"},
     				ExtraFields: map[string]any{
     					"additionalProperties": false,
     				},
     			},
     		}},
     	},
     	ToolChoice: anthropic.ToolChoiceUnionParam{OfAuto: &anthropic.ToolChoiceAutoParam{}},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize: The meeting moved to Thursday. Call the record_summary tool with your result.")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response.RawJSON())
     ```

     ```java Java

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model(Model.CLAUDE_FABLE_5_1)
             .maxTokens(16000L)
             .addTool(Tool.builder()
                 .name("record_summary")
                 .description("Record the structured summary of the document.")
                 .inputSchema(InputSchema.builder()
                     .properties(JsonValue.from(Map.of("summary", Map.of("type", "string"))))
                     .putAdditionalProperty("required", JsonValue.from(List.of("summary")))
                     .putAdditionalProperty("additionalProperties", JsonValue.from(false))
                     .build())
                 .strict(true)
                 .build())
             .toolChoice(ToolChoice.ofAuto(ToolChoiceAuto.builder().build()))
             .addUserMessage("Summarize: The meeting moved to Thursday. Call the record_summary tool with your result.")
             .build();

         Message response = client.messages().create(params);
         IO.println(response);
     }
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [
             ['role' => 'user', 'content' => 'Summarize: The meeting moved to Thursday. Call the record_summary tool with your result.']
         ],
         model: 'claude-fable-5-1',
         toolChoice: ['type' => 'auto'],
         tools: [
             [
                 'name' => 'record_summary',
                 'description' => 'Record the structured summary of the document.',
                 'strict' => true,
                 'input_schema' => [
                     'type' => 'object',
                     'properties' => [
                         'summary' => ['type' => 'string']
                     ],
                     'required' => ['summary'],
                     'additionalProperties' => false
                 ]
             ]
         ],
     );

     echo $message;
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: Anthropic::Model::CLAUDE_FABLE_5_1,
       max_tokens: 16000,
       tools: [
         {
           name: "record_summary",
           description: "Record the structured summary of the document.",
           strict: true,
           input_schema: {
             type: "object",
             properties: { summary: { type: "string" } },
             required: ["summary"],
             additionalProperties: false
           }
         }
       ],
       tool_choice: { type: "auto" },
       messages: [
         { role: "user", content: "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result." }
       ]
     )
     puts message
     ```
   </CodeGroup>

   Lihat [Penggunaan alat strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) dan [Memaksa penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use). Jika Anda memaksakan alat hanya untuk mendapatkan JSON yang sesuai skema, gunakan [JSON outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#usage) (`output_config.format`) sebagai gantinya.

   Jika aplikasi Anda, bukan pengguna, memerlukan pemanggilan alat tertentu pada giliran saat ini dalam percakapan multi-giliran, tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) setelah giliran `user` terbaru. Sebutkan nama alatnya, nyatakan bahwa pemanggilan diperlukan untuk giliran ini, dan minta Claude untuk membuka responsnya dengan pemanggilan tersebut. Karena pesan ditambahkan alih-alih ditulis ke dalam prompt `system` tingkat atas, giliran sebelumnya tetap identik byte demi byte dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching):

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-fable-5-1",
         "max_tokens": 16000,
         "system": "You are a customer support assistant for an online electronics store.",
         "tools": [
           {
             "name": "search_help_center",
             "description": "Search the help center for policy and troubleshooting articles.",
             "strict": true,
             "input_schema": {
               "type": "object",
               "properties": {"query": {"type": "string"}},
               "required": ["query"],
               "additionalProperties": false
             }
           }
         ],
         "messages": [
           {"role": "user", "content": "My headphones from order A1234 arrived yesterday."},
           {"role": "assistant", "content": "Thanks for confirming. How can I help with order A1234?"},
           {"role": "user", "content": "I opened the box. Can I still return them?"},
           {
             "role": "system",
             "content": "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the latest message from the user. Begin your response with the search_help_center tool call. Do not reply with text only."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-fable-5-1
     max_tokens: 16000
     system: You are a customer support assistant for an online electronics store.
     tools:
       - name: search_help_center
         description: Search the help center for policy and troubleshooting articles.
         strict: true
         input_schema:
           type: object
           properties:
             query:
               type: string
           required: [query]
           additionalProperties: false
     messages:
       - role: user
         content: My headphones from order A1234 arrived yesterday.
       - role: assistant
         content: Thanks for confirming. How can I help with order A1234?
       - role: user
         content: I opened the box. Can I still return them?
       - role: system
         content: >-
           Tool-use requirement for the current turn: the application requires a call
           to the search_help_center tool in your response to the user's latest message.
           Begin your response with the search_help_center tool call. Do not reply with
           text only.
     YAML
     ```

     ```python Python
     client = anthropic.Anthropic()

     search_help_center_tool = {
         "name": "search_help_center",
         "description": "Search the help center for policy and troubleshooting articles.",
         "strict": True,
         "input_schema": {
             "type": "object",
             "properties": {"query": {"type": "string"}},
             "required": ["query"],
             "additionalProperties": False,
         },
     }

     response = client.messages.create(
         model="claude-fable-5-1",
         max_tokens=16000,
         system="You are a customer support assistant for an online electronics store.",
         tools=[search_help_center_tool],
         messages=[
             {
                 "role": "user",
                 "content": "My headphones from order A1234 arrived yesterday.",
             },
             {
                 "role": "assistant",
                 "content": "Thanks for confirming. How can I help with order A1234?",
             },
             {"role": "user", "content": "I opened the box. Can I still return them?"},
             # Aplikasi mewajibkan pencarian di pusat bantuan sebelum setiap jawaban
             # terkait kebijakan. Menambahkan persyaratan ini sebagai pesan sistem membuat
             # giliran sebelumnya tetap tidak berubah.
             {
                 "role": "system",
                 "content": "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only.",
             },
         ],
     )
     print(response.content)
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.messages.create({
       model: "claude-fable-5-1",
       max_tokens: 16000,
       system: "You are a customer support assistant for an online electronics store.",
       tools: [
         {
           name: "search_help_center",
           description: "Search the help center for policy and troubleshooting articles.",
           strict: true,
           input_schema: {
             type: "object",
             properties: { query: { type: "string" } },
             required: ["query"],
             additionalProperties: false
           }
         }
       ],
       messages: [
         { role: "user", content: "My headphones from order A1234 arrived yesterday." },
         { role: "assistant", content: "Thanks for confirming. How can I help with order A1234?" },
         { role: "user", content: "I opened the box. Can I still return them?" },
         // Aplikasi mengharuskan pencarian di pusat bantuan sebelum jawaban apa pun
         // terkait kebijakan. Menambahkan persyaratan ini sebagai pesan sistem membuat
         // giliran-giliran sebelumnya tetap tidak berubah.
         {
           role: "system",
           content:
             "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."
         }
       ]
     });

     console.log(response.content);
     ```

     ```csharp C#
     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeFable5_1,
         MaxTokens = 16000,
         System = "You are a customer support assistant for an online electronics store.",
         Tools = [
             new ToolUnion(new Tool()
             {
                 Name = "search_help_center",
                 Description = "Search the help center for policy and troubleshooting articles.",
                 Strict = true,
                 InputSchema = new InputSchema(new Dictionary<string, JsonElement>
                 {
                     ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                     {
                         ["query"] = new { type = "string" },
                     }),
                     ["required"] = JsonSerializer.SerializeToElement(new[] { "query" }),
                     ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                 }),
             }),
         ],
         Messages = [
             new UserMessageParam { Content = "My headphones from order A1234 arrived yesterday." },
             new AssistantMessageParam { Content = "Thanks for confirming. How can I help with order A1234?" },
             new UserMessageParam { Content = "I opened the box. Can I still return them?" },
             // Aplikasi mewajibkan pencarian di pusat bantuan sebelum jawaban
             // kebijakan apa pun. Menambahkan persyaratan ini sebagai pesan sistem membuat
             // giliran sebelumnya tetap tidak berubah.
             new SystemMessageParam
             {
                 Content = "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."
             }
         ]
     };

     var message = await client.Messages.Create(parameters);
     Console.WriteLine(message);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeFable5_1,
     	MaxTokens: 16000,
     	System: []anthropic.TextBlockParam{
     		{Text: "You are a customer support assistant for an online electronics store."},
     	},
     	Tools: []anthropic.ToolUnionParam{
     		{OfTool: &anthropic.ToolParam{
     			Name:        "search_help_center",
     			Description: anthropic.String("Search the help center for policy and troubleshooting articles."),
     			Strict:      anthropic.Bool(true),
     			InputSchema: anthropic.ToolInputSchemaParam{
     				Properties: map[string]any{
     					"query": map[string]any{"type": "string"},
     				},
     				Required: []string{"query"},
     				ExtraFields: map[string]any{
     					"additionalProperties": false,
     				},
     			},
     		}},
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("My headphones from order A1234 arrived yesterday.")),
     		anthropic.NewAssistantMessage(anthropic.NewTextBlock("Thanks for confirming. How can I help with order A1234?")),
     		anthropic.NewUserMessage(anthropic.NewTextBlock("I opened the box. Can I still return them?")),
     		// Aplikasi mewajibkan pencarian di pusat bantuan sebelum jawaban
     		// kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem membuat
     		// giliran sebelumnya tetap tidak berubah.
     		{OfSystem: &anthropic.SystemMessageParam{
     			Content: []anthropic.TextBlockParam{
     				{Text: "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."},
     			},
     		}},
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response.RawJSON())
     ```

     ```java Java

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model(Model.CLAUDE_FABLE_5_1)
             .maxTokens(16000L)
             .system("You are a customer support assistant for an online electronics store.")
             .addTool(Tool.builder()
                 .name("search_help_center")
                 .description("Search the help center for policy and troubleshooting articles.")
                 .inputSchema(InputSchema.builder()
                     .properties(JsonValue.from(Map.of("query", Map.of("type", "string"))))
                     .putAdditionalProperty("required", JsonValue.from(List.of("query")))
                     .putAdditionalProperty("additionalProperties", JsonValue.from(false))
                     .build())
                 .strict(true)
                 .build())
             .addUserMessage("My headphones from order A1234 arrived yesterday.")
             .addAssistantMessage("Thanks for confirming. How can I help with order A1234?")
             .addUserMessage("I opened the box. Can I still return them?")
             // Aplikasi mewajibkan pencarian di pusat bantuan sebelum memberikan jawaban
             // terkait kebijakan. Menambahkan persyaratan ini sebagai pesan sistem membuat
             // giliran-giliran sebelumnya tetap tidak berubah.
             .addSystemMessage("Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only.")
             .build();

         Message response = client.messages().create(params);
         IO.println(response);
     }
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [
             ['role' => 'user', 'content' => 'My headphones from order A1234 arrived yesterday.'],
             ['role' => 'assistant', 'content' => 'Thanks for confirming. How can I help with order A1234?'],
             ['role' => 'user', 'content' => 'I opened the box. Can I still return them?'],
             // Aplikasi mewajibkan pencarian di pusat bantuan sebelum memberi jawaban
             // terkait kebijakan. Menambahkan persyaratan ini sebagai pesan sistem membuat
             // giliran sebelumnya tetap tidak berubah.
             ['role' => 'system', 'content' => 'Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user\'s latest message. Begin your response with the search_help_center tool call. Do not reply with text only.']
         ],
         model: 'claude-fable-5-1',
         system: 'You are a customer support assistant for an online electronics store.',
         tools: [
             [
                 'name' => 'search_help_center',
                 'description' => 'Search the help center for policy and troubleshooting articles.',
                 'strict' => true,
                 'input_schema' => [
                     'type' => 'object',
                     'properties' => [
                         'query' => ['type' => 'string']
                     ],
                     'required' => ['query'],
                     'additionalProperties' => false
                 ]
             ]
         ],
     );

     echo $message;
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: Anthropic::Model::CLAUDE_FABLE_5_1,
       max_tokens: 16000,
       system: "You are a customer support assistant for an online electronics store.",
       tools: [
         {
           name: "search_help_center",
           description: "Search the help center for policy and troubleshooting articles.",
           strict: true,
           input_schema: {
             type: "object",
             properties: { query: { type: "string" } },
             required: ["query"],
             additionalProperties: false
           }
         }
       ],
       messages: [
         { role: "user", content: "My headphones from order A1234 arrived yesterday." },
         { role: "assistant", content: "Thanks for confirming. How can I help with order A1234?" },
         { role: "user", content: "I opened the box. Can I still return them?" },
         # Aplikasi mewajibkan pencarian di pusat bantuan sebelum jawaban
         # kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem membuat
         # giliran sebelumnya tidak berubah.
         {
           role: "system",
           content: "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."
         }
       ]
     )
     puts message
     ```
   </CodeGroup>

   Pertahankan pesan `role: "system"` dalam riwayat pada permintaan berikutnya, seperti giliran lainnya. Pesan sistem di tengah percakapan tidak memerlukan header beta. `tool_choice: {"type": "none"}` tetap berfungsi untuk giliran yang tidak boleh memanggil alat.

2. **Hanya Claude Fable 5.1 dan Claude Mythos 5.1 yang membaca blok thinking Claude Fable 5.1:** Setiap blok `thinking` mencatat model mana yang menghasilkannya. Claude Fable 5.1 membaca bloknya sendiri serta blok dari Claude Mythos 5.1, Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude yang lebih lama. Percakapan yang berpindah ke `claude-fable-5-1` dari salah satu model tersebut tetap mempertahankan penalaran sebelumnya. Kondisi ini bersifat satu arah: selain Claude Mythos 5.1, tidak satu pun dari model tersebut yang dapat membaca blok Claude Fable 5.1.

   Percakapan yang berjalan di Claude Fable 5.1 dapat berpindah ke model lain, lebih lama atau lebih baru, melalui peralihan router, retry sisi klien, atau [fallback penolakan classifier](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback), termasuk [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback). API menghapus blok yang tidak dapat dibaca model tersebut sebelum model menerimanya, permintaan berhasil, dan Anda tidak ditagih untuk token input yang dibuang. Model target merencanakan ulang tanpa penalaran tersebut, yang dapat meningkatkan biaya dan “latency” (latensi) pada giliran pertama setelah peralihan. Untuk melihat apa yang dibuang, kirim [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01`: respons kemudian membawa array `input_transformations` yang menyebutkan setiap blok yang dibuang dengan `reason: "model_binding_mismatch"`. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

3. **Mengedit giliran sebelumnya membuat blok thinking tidak valid:** Pada Claude Fable 5.1 dan Claude Mythos 5.1, blok thinking yang Anda kirim kembali hanya tetap valid selama semua yang dikirim sebelumnya tidak berubah: prompt `system`, `tools`, dan pesan-pesan sebelumnya. Claude Code, claude.ai, [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), dan [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) menjaga riwayat tersebut tetap utuh untuk Anda. Jika kode Anda membangun array `messages` sendiri, poin ini berlaku untuk Anda, dan [Preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) adalah panduan integrasi lengkapnya.

   Field `thinking.block_binding.prefix_mismatch_behavior` (beta header `thinking-binding-controls-2026-08-01`) menentukan apa yang dilakukan API terhadap blok yang tidak valid. `"error"` menolak permintaan dengan error 400. `"drop_block"` membuang blok yang tidak valid beserta setiap blok thinking setelahnya, dan permintaan berhasil. Jika permintaan tidak mengatur field tersebut, hasilnya bergantung pada model dan pada kapan akun Anda dibuat:

   | Model             | Akun dibuat pada atau setelah 31 Agustus 2026 | Akun dibuat sebelum 31 Agustus 2026              |
   | ----------------- | --------------------------------------------- | ------------------------------------------------ |
   | Claude Fable 5.1  | Error 400                                     | Tidak ada error (blok yang gagal mencapai model) |
   | Claude Mythos 5.1 | Error 400                                     | Error 400                                        |

   Untuk melihat error 400 dari akun Anda sendiri, atur field tersebut ke `"error"` pada permintaan pengujian Anda. Lakukan ini sebelum Anda merilis alat yang dijalankan orang dengan kunci API mereka sendiri: akun mereka bisa mendapatkan error 400 sementara akun Anda tidak. Tabel lengkapnya, beserta platform yang berlaku, ada di [Ketika `prefix_mismatch_behavior` tidak diatur](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#enforcement).

   Error 400 terlihat seperti ini:

   ```text wrap
   messages.5.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block". That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.
   ```

   Error ini muncul kembali setiap kali permintaan mengirimkan blok yang tidak valid, sehingga loop percobaan ulang tidak akan menghilangkannya. Untuk melanjutkan tanpa penalaran yang telah dibatalkan validitasnya, hapus blok yang disebutkan dalam error beserta setiap blok `thinking` dan `redacted_thinking` setelahnya, lalu coba ulang sekali. Sebagai alternatif, kirimkan [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01` dan atur `prefix_mismatch_behavior` ke `"drop_block"` pada setiap permintaan berikutnya dalam percakapan tersebut. Respons kemudian melaporkan setiap blok yang dibuang dalam array `input_transformations` dengan `reason: "prefix_binding_mismatch"`:

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "anthropic-beta: thinking-binding-controls-2026-08-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-fable-5-1",
         "max_tokens": 16000,
         "thinking": {
           "type": "adaptive",
           "block_binding": {
             "prefix_mismatch_behavior": "drop_block"
           }
         },
         "messages": [
           {
             "role": "user",
             "content": "What is the greatest common divisor of 1071 and 462?"
           }
         ]
       }'
     ```

     ```bash CLI
     ant beta:messages create --beta thinking-binding-controls-2026-08-01 <<'YAML'
     model: claude-fable-5-1
     max_tokens: 16000
     thinking:
       type: adaptive
       block_binding:
         prefix_mismatch_behavior: drop_block
     messages:
       - role: user
         content: What is the greatest common divisor of 1071 and 462?
     YAML
     ```

     ```python Python
     client = anthropic.Anthropic()

     response = client.beta.messages.create(
         model="claude-fable-5-1",
         max_tokens=16000,
         thinking={
             "type": "adaptive",
             "block_binding": {"prefix_mismatch_behavior": "drop_block"},
         },
         messages=[
             {
                 "role": "user",
                 "content": "What is the greatest common divisor of 1071 and 462?",
             }
         ],
         betas=["thinking-binding-controls-2026-08-01"],
     )

     for block in response.content:
         if block.type == "text":
             print(block.text)

     print(f"Input transformations: {len(response.input_transformations or [])}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.beta.messages.create({
       model: "claude-fable-5-1",
       max_tokens: 16000,
       thinking: {
         type: "adaptive",
         block_binding: { prefix_mismatch_behavior: "drop_block" }
       },
       messages: [
         { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
       ],
       betas: ["thinking-binding-controls-2026-08-01"]
     });

     for (const block of response.content) {
       if (block.type === "text") {
         console.log(block.text);
       }
     }
     console.log(`Input transformations: ${response.input_transformations?.length ?? 0}`);
     ```

     ```csharp C#
     using Anthropic.Models.Beta;
     using Anthropic.Models.Beta.Messages;
     using Model = Anthropic.Models.Messages.Model;

     AnthropicClient client = new();

     var response = await client.Beta.Messages.Create(
         new()
         {
             Model = Model.ClaudeFable5_1,
             MaxTokens = 16000,
             Thinking = new BetaThinkingConfigAdaptive
             {
                 BlockBinding = new()
                 {
                     PrefixMismatchBehavior = BetaThinkingPrefixMismatchBehavior.DropBlock,
                 },
             },
             Messages =
             [
                 new BetaUserMessageParam
                 {
                     Content = "What is the greatest common divisor of 1071 and 462?",
                 },
             ],
             Betas = [AnthropicBeta.ThinkingBindingControls2026_08_01],
         }
     );

     foreach (var block in response.Content)
     {
         if (block.TryPickText(out var textBlock))
         {
             Console.WriteLine(textBlock.Text);
         }
     }

     Console.WriteLine($"Input transformations: {response.InputTransformations?.Count ?? 0}");
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
     	Model:     anthropic.ModelClaudeFable5_1,
     	MaxTokens: 16000,
     	Thinking: anthropic.BetaThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{
     			BlockBinding: anthropic.BetaThinkingBlockBindingParam{
     				PrefixMismatchBehavior: anthropic.BetaThinkingPrefixMismatchBehaviorDropBlock,
     			},
     		},
     	},
     	Messages: []anthropic.BetaMessageParam{
     		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What is the greatest common divisor of 1071 and 462?")),
     	},
     	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaThinkingBindingControls2026_08_01},
     })
     if err != nil {
     	log.Fatal(err)
     }

     for _, block := range response.Content {
     	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
     		fmt.Println(textBlock.Text)
     	}
     }
     fmt.Printf("Input transformations: %d\n", len(response.InputTransformations))
     ```

     ```java Java
     import com.anthropic.models.beta.AnthropicBeta;
     import com.anthropic.models.beta.messages.BetaMessage;
     import com.anthropic.models.beta.messages.BetaThinkingBlockBinding;
     import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
     import com.anthropic.models.beta.messages.BetaThinkingPrefixMismatchBehavior;
     import com.anthropic.models.beta.messages.MessageCreateParams;
     import com.anthropic.models.messages.Model;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model(Model.CLAUDE_FABLE_5_1)
             .maxTokens(16000L)
             .addBeta(AnthropicBeta.THINKING_BINDING_CONTROLS_2026_08_01)
             .thinking(BetaThinkingConfigAdaptive.builder()
                 .blockBinding(BetaThinkingBlockBinding.builder()
                     .prefixMismatchBehavior(BetaThinkingPrefixMismatchBehavior.DROP_BLOCK)
                     .build())
                 .build())
             .addUserMessage("What is the greatest common divisor of 1071 and 462?")
             .build();

         BetaMessage response = client.beta().messages().create(params);

         response.content().stream()
             .flatMap(block -> block.text().stream())
             .forEach(textBlock -> IO.println(textBlock.text()));
         IO.println("Input transformations: "
             + response.inputTransformations().map(List::size).orElse(0));
     }
     ```

     ```php PHP
     use Anthropic\Beta\AnthropicBeta;
     use Anthropic\Beta\Messages\BetaThinkingBlockBinding;
     use Anthropic\Beta\Messages\BetaThinkingConfigAdaptive;
     use Anthropic\Beta\Messages\BetaThinkingPrefixMismatchBehavior;
     use Anthropic\Client;

     $client = new Client();

     $response = $client->beta->messages->create(
         model: 'claude-fable-5-1',
         maxTokens: 16000,
         thinking: BetaThinkingConfigAdaptive::with(
             blockBinding: BetaThinkingBlockBinding::with(
                 prefixMismatchBehavior: BetaThinkingPrefixMismatchBehavior::DROP_BLOCK,
             ),
         ),
         messages: [
             ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?'],
         ],
         betas: [AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01],
     );

     foreach ($response->content as $block) {
         if ($block->type === 'text') {
             echo $block->text, PHP_EOL;
         }
     }

     echo 'Input transformations: ', count($response->inputTransformations ?? []), PHP_EOL;
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     response = client.beta.messages.create(
       model: Anthropic::Model::CLAUDE_FABLE_5_1,
       max_tokens: 16_000,
       thinking: {
         type: "adaptive",
         block_binding: {prefix_mismatch_behavior: "drop_block"}
       },
       messages: [
         {role: "user", content: "What is the greatest common divisor of 1071 and 462?"}
       ],
       betas: [Anthropic::AnthropicBeta::THINKING_BINDING_CONTROLS_2026_08_01]
     )

     response.content.each do |block|
       puts block.text if block.type == :text
     end

     puts "Input transformations: #{response.input_transformations&.length || 0}"
     ```
   </CodeGroup>

   Endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) menjalankan pemeriksaan yang sama. Lihat [Mengatur perilaku ketidakcocokan dan membaca `input_transformations`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#preserved-thinking-controls) untuk bentuk respons dan penempatan streaming.

   Pola yang membatalkan validitas blok thinking berikutnya, dan apa yang harus dilakukan sebagai gantinya:

   * Mengedit, menyusun ulang, atau menghapus giliran sebelumnya. Ini termasuk menghapus hasil alat lama, memotong giliran dari tengah transkrip, dan compaction sisi klien yang mempertahankan giliran terbaru beserta blok thinking-nya secara verbatim di belakang ringkasan (termasuk compaction latar belakang yang menukar ringkasannya beberapa giliran kemudian). Sebagai gantinya, gunakan [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) ([pembersihan hasil alat](https://platform.claude.com/docs/id/build-with-claude/context-editing#tool-result-clearing) untuk hasil alat lama), atau salah satu bentuk compaction sisi klien di bawah [Pangkas konteks di server, atau lakukan compaction dalam bentuk yang tidak membawa thinking usang](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-trim-context).
   * Menyisipkan konten yang tidak Anda simpan, misalnya pengingat per giliran yang ditambahkan setelah blok `tool_result` dan dihapus pada permintaan berikutnya. Sebagai gantinya, kirim pengingat sebagai [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dan biarkan dalam riwayat.
   * Membangun ulang prompt `system` tingkat atas atau array `tools` di antara permintaan dalam percakapan yang sama, misalnya untuk memperbarui tanggal saat ini atau untuk menambah atau menghapus alat. Sebagai gantinya, tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) yang membawa instruksi baru (“The current date is 2026-09-14.”) atau blok `tool_addition` dan `tool_removal`. Alat yang tidak dideklarasikan dalam `tools` di awal dapat [didefinisikan di dalam blok `tool_addition`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta) (header beta `inline-tools-2026-09-15`).
   * URL gambar atau dokumen yang menyajikan byte berbeda pada permintaan berikutnya. Pemeriksaan prefiks mencakup byte, bukan string URL, sehingga URL bertanda tangan yang berotasi untuk file yang sama tidak masalah. Untuk konten yang Anda referensikan lintas giliran, unggah sekali dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan kirim `file_id`, atau kirim base64.

   Setiap pengganti juga menjaga giliran sebelumnya tetap identik byte demi byte dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) yang akan hilang jika riwayat, prompt `system`, atau array `tools` diedit.

   Pola yang tetap berfungsi:

   * Riwayat append-only: menambahkan giliran dan mengirim kembali giliran sebelumnya persis seperti yang dikirim dan diterima, termasuk pesan `role: "system"` yang ditambahkan.
   * Menghapus blok pemikiran tertua (dari awal riwayat), yang terbaru (dari akhir), atau semuanya.
   * Mengubah `effort`, `max_tokens`, atau parameter permintaan lain di luar `model`, `system`, `tools`, dan `messages`, serta menambah atau memindahkan penanda `cache_control`.
   * Compaction sisi server dan context editing, termasuk [pembersihan blok thinking](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing). Keduanya tidak dihitung sebagai edit, karena pemeriksaan membandingkan percakapan sebagaimana Anda mengirimkannya.

   Untuk memeriksa integrasi yang sudah ada:

   1. Tangkap body permintaan persis yang dikirimnya selama beberapa giliran normal, termasuk compaction atau perubahan alat jika produk Anda memilikinya. Untuk setiap pasangan permintaan berurutan, bandingkan prompt `system`, array `tools`, dan prefiks bersama dari `messages`. Semuanya harus identik byte demi byte hingga giliran yang baru ditambahkan. Pengecualian yang diharapkan adalah permintaan yang menukar masuk blok `compaction` bertanda tangan dari [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand): blok tersebut menggantikan pesan yang diringkasnya di bagian depan `messages`, dan segala sesuatu setelahnya tetap harus cocok.
   2. Jalankan sesi multi-giliran normal terhadap `claude-fable-5-1` dengan header beta `thinking-binding-controls-2026-08-01` dan `prefix_mismatch_behavior: "drop_block"`. Catat `input_transformations` pada setiap respons. Dalam sesi yang responsnya menyertakan blok thinking, array kosong pada setiap giliran berarti riwayatnya utuh. Entri dengan `reason: "prefix_binding_mismatch"` berarti sesuatu sebelum blok di `path` telah berubah sejak blok tersebut dihasilkan. Entri dengan `reason: "model_binding_mismatch"` berarti percakapan beralih model, yang bukan merupakan bug dalam kode Anda. Karena setiap permintaan menetapkan field tersebut, pengujian ini berfungsi dari akun mana pun. Di CI, tetapkan `"error"` sebagai gantinya agar suatu pengeditan menggagalkan proses tersebut.
   3. Pilih pengaturan produksi dan kirimkan pada setiap permintaan. Gunakan `"error"` jika ketidakcocokan prefiks hanya dapat berarti bug dalam kode Anda. Gunakan `"drop_block"` jika Anda lebih memilih membuang blok yang terdampak daripada gagal. Apa pun pilihannya, pantau error 400 atau entri `input_transformations`.

   Membuang blok thinking sekali, misalnya pada batas compaction, hanya berdampak kecil. Integrasi yang membatalkan validitas thinking sebelumnya pada setiap permintaan akan memulai ulang cache prompt setiap kali, yang dapat meningkatkan biaya per tugas (lihat [Jaga riwayat percakapan tetap append-only](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)).

4. **Advisor tool menerima lebih sedikit advisor:** Dengan [advisor tool](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) (beta), advisor harus setidaknya sama mampunya dengan executor. Dengan executor `claude-fable-5-1`, advisor yang kurang mampu, seperti `claude-fable-5` atau `claude-opus-5-5`, mengembalikan 400 `invalid_request_error`. Pilih advisor yang tercantum untuk executor tersebut di [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility).

### Perubahan perilaku

1. **Lebih sedikit pemanggilan alat paralel dalam agent loop panjang:** Dalam loop yang berjalan lama di mana pembacaan independen berikutnya hanya tersirat oleh tugas (agen coding kustom, harness bash-dan-editor, computer use), Claude Fable 5.1 mungkin mengeluarkan satu pemanggilan alat di setiap giliran. Setiap giliran tambahan menghabiskan token, satu round trip, dan waktu nyata. Tambahkan instruksi batching satu kalimat setelah setiap pesan pengguna sebagai [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: "next_user_message"`, beta), atau, tanpa beta, dalam blok teks setelah blok `tool_result`, dan biarkan salinan sebelumnya dalam riwayat pada permintaan berikutnya. Lihat [Batch pemanggilan alat independen dalam agent loop](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops).

2. **Lebih sedikit pesan progres di antara pemanggilan alat:** Claude Fable 5.1 menulis lebih sedikit pembaruan status selama urutan alat yang panjang dibandingkan Claude Fable 5, dan ringkasan coding agentiknya lebih pendek. Jika antarmuka Anda menampilkan pembaruan tersebut, atur `thinking.display` ke `"updates"` (beta) atau `"summarized"` dan minta pembaruan secara eksplisit dalam prompt. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) dan [Minta pembaruan progres yang ditujukan kepada pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates).

3. **Lebih sedikit pemanggilan pencarian dan pengambilan pada effort rendah:** Pada effort `low`, Claude Fable 5.1 lebih sering menjawab dari memori dibandingkan Claude Fable 5 alih-alih memanggil alat pencarian atau pengambilan. Jika produk Anda mengandalkan pengambilan pada effort rendah, naikkan effort untuk permintaan tersebut atau beri tahu model kapan harus mencari. Lihat [Pemicuan pencarian pada effort rendah](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort).

Untuk perbedaan dalam kepadatan prosa, pemformatan chat, pengutipan dalam ringkasan, dan edit file, yang tidak memengaruhi integrasi API, lihat [Perubahan dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#changed-from-claude-fable-5).

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib, tetapi masing-masing menurunkan biaya atau latency atau menghilangkan suatu mode kegagalan:

1. **Ubah effort di tengah percakapan (beta):** Di Claude Fable 5, `output_config.effort` berada di tingkat permintaan, dan mengubahnya di antara permintaan membuang prefiks yang di-cache dari giliran sebelumnya. Di `claude-fable-5-1`, pesan `role: "system"` yang hanya membawa `output_config` menaikkan effort untuk langkah yang sulit atau menurunkannya untuk langkah rutin tanpa membatalkan validitas [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching):

   <CodeGroup>
     ```bash cURL
     # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "anthropic-beta: mid-conversation-output-config-2026-07-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-fable-5-1",
         "max_tokens": 4096,
         "output_config": {"effort": "high"},
         "messages": [
           {"role": "user", "content": "Plan a migration from SQLite to PostgreSQL in three short steps."},
           {"role": "assistant", "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."},
           {"role": "system", "content": [], "output_config": {"effort": "low"}},
           {"role": "user", "content": "Summarize the plan in one sentence."}
         ]
       }'
     ```

     ```bash CLI
     ant beta:messages create \
       --beta mid-conversation-output-config-2026-07-01 <<'YAML'
     model: claude-fable-5-1
     max_tokens: 4096
     output_config:
       effort: high
     messages:
       - role: user
         content: Plan a migration from SQLite to PostgreSQL in three short steps.
       - role: assistant
         content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
       # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
       - role: system
         content: []
         output_config:
           effort: low
       - role: user
         content: Summarize the plan in one sentence.
     YAML
     ```

     ```python Python
     client = anthropic.Anthropic()

     response = client.beta.messages.create(
         model="claude-fable-5-1",
         max_tokens=4096,
         output_config={"effort": "high"},
         messages=[
             {
                 "role": "user",
                 "content": "Plan a migration from SQLite to PostgreSQL in three short steps.",
             },
             {
                 "role": "assistant",
                 "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.",
             },
             # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             {"role": "system", "content": [], "output_config": {"effort": "low"}},
             {"role": "user", "content": "Summarize the plan in one sentence."},
         ],
         betas=["mid-conversation-output-config-2026-07-01"],
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
       output_config: { effort: "high" },
       messages: [
         {
           role: "user",
           content: "Plan a migration from SQLite to PostgreSQL in three short steps."
         },
         {
           role: "assistant",
           content:
             "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
         },
         // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
         { role: "system", content: [], output_config: { effort: "low" } },
         { role: "user", content: "Summarize the plan in one sentence." }
       ],
       betas: ["mid-conversation-output-config-2026-07-01"]
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
     using Model = Anthropic.Models.Messages.Model;

     AnthropicClient client = new();

     var response = await client.Beta.Messages.Create(new MessageCreateParams
     {
         Model = Model.ClaudeFable5_1,
         MaxTokens = 4096,
         OutputConfig = new() { Effort = Effort.High },
         Messages =
         [
             new BetaUserMessageParam { Content = "Plan a migration from SQLite to PostgreSQL in three short steps." },
             new BetaAssistantMessageParam { Content = "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
             // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             new BetaSystemMessageParam
             {
                 Content = new([]),
                 OutputConfig = new() { Effort = BetaSystemMessageOutputConfigEffort.Low },
             },
             new BetaUserMessageParam { Content = "Summarize the plan in one sentence." },
         ],
         Betas = [AnthropicBeta.MidConversationOutputConfig2026_07_01],
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
     	Model:     anthropic.ModelClaudeFable5_1,
     	MaxTokens: 4096,
     	OutputConfig: anthropic.BetaOutputConfigParam{
     		Effort: anthropic.BetaOutputConfigEffortHigh,
     	},
     	Messages: []anthropic.BetaMessageParam{
     		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Plan a migration from SQLite to PostgreSQL in three short steps.")),
     		{OfAssistant: &anthropic.BetaAssistantMessageParam{
     			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
     		}},
     		// Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
     		anthropic.NewBetaSystemMessage(anthropic.BetaSystemMessageOutputConfigParam{
     			Effort: anthropic.BetaSystemMessageOutputConfigEffortLow,
     		}),
     		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize the plan in one sentence.")),
     	},
     	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaMidConversationOutputConfig2026_07_01},
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
     import com.anthropic.models.beta.messages.BetaOutputConfig;
     import com.anthropic.models.beta.messages.BetaSystemMessageOutputConfig;
     import com.anthropic.models.beta.messages.BetaSystemMessageParam;
     import com.anthropic.models.beta.messages.MessageCreateParams;
     import com.anthropic.models.messages.Model;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model(Model.CLAUDE_FABLE_5_1)
             .maxTokens(4096L)
             .addBeta(AnthropicBeta.MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01)
             .outputConfig(BetaOutputConfig.builder()
                 .effort(BetaOutputConfig.Effort.HIGH)
                 .build())
             .addUserMessage("Plan a migration from SQLite to PostgreSQL in three short steps.")
             .addAssistantMessage("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")
             // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             .addMessage(BetaSystemMessageParam.builder()
                 .contentOfBlocks(List.of())
                 .outputConfig(BetaSystemMessageOutputConfig.builder()
                     .effort(BetaSystemMessageOutputConfig.Effort.LOW)
                     .build())
                 .build())
             .addUserMessage("Summarize the plan in one sentence.")
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
     use Anthropic\Beta\Messages\BetaOutputConfig;
     use Anthropic\Beta\Messages\BetaSystemMessageOutputConfig;
     use Anthropic\Client;

     $client = new Client();

     $response = $client->beta->messages->create(
         model: 'claude-fable-5-1',
         maxTokens: 4096,
         outputConfig: BetaOutputConfig::with(effort: 'high'),
         messages: [
             BetaMessageParam::with(role: 'user', content: 'Plan a migration from SQLite to PostgreSQL in three short steps.'),
             BetaMessageParam::with(role: 'assistant', content: '1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.'),
             // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             BetaMessageParam::with(
                 role: 'system',
                 content: [],
                 outputConfig: BetaSystemMessageOutputConfig::with(effort: 'low'),
             ),
             BetaMessageParam::with(role: 'user', content: 'Summarize the plan in one sentence.'),
         ],
         betas: [AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01],
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
       model: Anthropic::Model::CLAUDE_FABLE_5_1,
       max_tokens: 4096,
       output_config: {effort: :high},
       messages: [
         {role: "user", content: "Plan a migration from SQLite to PostgreSQL in three short steps."},
         {role: "assistant", content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."},
         # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
         {role: "system", content: [], output_config: {effort: :low}},
         {role: "user", content: "Summarize the plan in one sentence."}
       ],
       betas: [Anthropic::AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01]
     )

     response.content.each do |block|
       puts block.text if block.type == :text
     end
     ```
   </CodeGroup>

   Jika ditempatkan di antara giliran `assistant` dan giliran `user` berikutnya, seperti di sini, pesan berlaku mulai dari giliran `user` tersebut. Jika ditempatkan langsung setelah giliran `user` dengan input baru, pesan menetapkan tingkat untuk balasan Claude pada giliran tersebut. Giliran `user` yang hanya berisi hasil alat tidak dihitung sebagai input baru: perubahan menunggu giliran `user` berikutnya dengan input baru. Tingkat tersebut kemudian bertahan hingga pesan `role: "system"` lain mengubahnya. Hanya tingkat bernama yang diterima (`low`, `medium`, `high`, `xhigh`, `max`), dan header beta `mid-conversation-output-config-2026-07-01` diperlukan. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).

2. **Ubah instruksi dan alat dengan pesan sistem di tengah percakapan:** Untuk mengubah instruksi atau alat di tengah sesi, tambahkan [pesan `role: "system"`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), dengan blok `tool_addition` dan `tool_removal` untuk perubahan alat (header beta `inline-tools-2026-09-15` di Claude API). Blok `tool_addition` dapat menyebutkan alat yang dideklarasikan dalam `tools` di awal sesi atau [membawa definisi lengkap alat](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#define-tools-in-a-message-beta), sehingga alat yang tidak diketahui di awal sesi tidak perlu berada dalam `tools`. Ini mempertahankan hit cache prompt pada giliran sebelumnya dan menjaga riwayat percakapan tetap append-only. Header `mid-conversation-tool-changes-2026-07-01` yang lebih lama tetap berfungsi untuk perubahan yang menyebutkan alat melalui referensi, di Claude API, Amazon Bedrock, dan Claude Models on Google Cloud (Google managed). Pesan yang sama menggantikan `tool_choice` yang dipaksakan ketika alat tertentu harus dijalankan pada giliran saat ini (lihat [Perubahan yang dapat merusak](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes)). Untuk pengingat yang hanya berlaku untuk satu giliran, kirim sebagai pesan `role: "system"` terpisah yang hanya berisi teks dengan `clear_at: "next_user_message"` ([pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages), header beta `mid-conversation-system-clear-at-2026-08-21`) dan biarkan dalam riwayat: pesan berhenti dirender setelah pesan pengguna berikutnya dan tidak memakan token setelah dibersihkan. Pesan yang membawa blok `tool_addition` atau `tool_removal` tidak dapat berlingkup giliran.

3. **Gunakan `fallbacks: "default"` untuk penolakan:** Tetap tangani `stop_reason: "refusal"` dan baca `stop_details.category` sebelum konten respons. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, atur `fallbacks: "default"` (beta, header `server-side-fallback-2026-07-01`). `"default"` mencoba ulang permintaan yang ditolak pada model yang direkomendasikan Anthropic untuk kategori tersebut. Target fallback yang diizinkan untuk Claude Fable 5.1 adalah Claude Opus 4.8 (`claude-opus-4-8`) dan Claude Opus 5 (`claude-opus-5`). Daftar `fallbacks` eksplisit dapat menyebutkan salah satunya. Model fallback tidak menerima blok thinking Claude Fable 5.1. Parameter `fallbacks` tidak tersedia di Amazon Bedrock, Claude Models on Google Cloud (Google managed), atau Microsoft Foundry. Di platform tersebut, gunakan [fallback sisi klien](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) sebagai gantinya. Jika Anda membangun retry sendiri, [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit) berlaku dengan ketentuan yang sama seperti Claude Fable 5. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

4. **Mulai dari effort `high` dan lakukan sweep:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah `high`, dan kelima tingkat didukung. Pertahankan panduan Claude Fable 5: `high` untuk sebagian besar pekerjaan, dan `medium` sebagai kontrol biaya yang layak diuji. Peningkatan Claude Fable 5.1 dibandingkan Claude Fable 5 paling besar pada `xhigh` dan `max`, tetapi tingkat tersebut juga menambah waktu berpikir dan waktu hingga respons pertama, jadi naikkan ke tingkat tersebut untuk tugas yang paling sensitif terhadap kemampuan dan di mana eval Anda menunjukkan peningkatan. Jalankan sweep baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Fable 5. Lihat [Tingkat effort yang direkomendasikan untuk Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-fable-5-1).

5. **Pangkas konteks di server, atau lakukan compaction dalam bentuk yang tidak membawa thinking usang:** Jika kode Anda memotong atau meringkas giliran lama di klien, solusi paling sederhana adalah memindahkan pekerjaan tersebut ke [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) sisi server. Keduanya tidak dihitung sebagai edit: [pemeriksaan prefiks](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking) membandingkan percakapan sebagaimana Anda mengirimkannya, sehingga apa pun yang dihapusnya tidak membatalkan validitas blok thinking berikutnya. [Parameter `instructions`](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#custom-summarization-instructions) milik compaction juga menerima prompt peringkasan Anda sendiri. Jika Anda mempertahankan giliran terbaru secara verbatim di belakang ringkasan, atau meringkas di latar belakang sementara percakapan berlanjut, gunakan [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) (header beta `compact-2026-09-04`) alih-alih ringkasan yang ditulis klien. API menulis blok ringkasan bertanda tangan yang Anda tempatkan menggantikan pesan yang diringkasnya. Blok thinking dalam giliran yang Anda pertahankan dapat tetap valid, dengan kondisi di [Compaction dan preserved thinking](https://platform.claude.com/docs/id/build-with-claude/compaction-thinking-blocks#conditions-for-kept-thinking-to-stay-valid). Jika Anda mempertahankan compaction di klien, pilih salah satu dari tiga bentuk:

   * **Compaction sederhana (direkomendasikan):** ganti seluruh riwayat dengan satu pesan ringkasan ditambah giliran pengguna baru dan jangan memutar ulang apa pun lainnya. Tidak ada blok thinking yang dibawa, sehingga tidak ada yang gagal. Model Claude dilatih pada tugas jangka panjang dengan skema ini, dan kinerjanya sebanding dengan skema yang lebih rumit untuk sebagian besar beban kerja.
   * **Compaction keep-tail:** jika Anda mempertahankan giliran terbaru secara verbatim di belakang ringkasan, hapus blok `thinking` dan `redacted_thinking` dari giliran tersebut (teks dan pemanggilan alat dapat tetap ada), atau atur `prefix_mismatch_behavior: "drop_block"`. Thinking mereka dihasilkan terhadap riwayat lengkap dan akan gagal di belakang ringkasan jika tidak demikian.
   * **Compaction latar belakang:** jika Anda membangun ringkasan di luar jalur kritis dan menukarnya masuk kemudian, setiap giliran yang dihasilkan sementara itu membawa thinking yang mendahului penukaran. Kirim `"drop_block"` pada setiap permintaan yang masih membawa blok thinking yang dihasilkan sebelum penukaran (atau hapus blok tersebut sendiri; `input_transformations` pada respons pertama setelah penukaran mencantumkan dengan tepat blok mana saja), atau lakukan compaction secara sinkron.

   Jangan memotong giliran individual dari tengah transkrip: hal itu membatalkan validitas setiap blok thinking berikutnya dan tidak ada bentuk sisi klien yang dapat menghindarinya. Gunakan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) untuk perubahan instruksi yang Anda lakukan, atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) sisi server untuk penghapusan selektif. Lihat [Mengirim kembali blok compaction](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#passing-compaction-blocks-back).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-fable-5` ke `claude-fable-5-1` (atau `claude-mythos-5` ke `claude-mythos-5-1`).
* Ganti `tool_choice` paksa (`{type: "any"}` atau `{type: "tool", ...}`): permintaan yang mengaturnya akan mendapatkan error 400. Gunakan `{type: "auto"}` dengan instruksi eksplisit dan alat `strict: true`, atau gunakan output JSON. Ketika aplikasi Anda mengharuskan pemanggilan tersebut, letakkan instruksi di giliran `user` atau di pesan `role: "system"` di tengah percakapan.
* Jika Anda menggunakan [advisor tool](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) (beta), perbarui juga `model` advisor. Advisor yang kurang mampu dibandingkan Claude Fable 5.1, seperti `claude-fable-5` atau `claude-opus-5-5`, mengembalikan error 400.
* Tetap kirim kembali blok `thinking` tanpa perubahan pada setiap giliran, termasuk yang kosong. Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model yang lebih lama. Memindahkan percakapan dari Claude Fable 5.1 ke model apa pun selain Claude Mythos 5.1 akan membuang blok-bloknya.
* Jika kode Anda membangun array `messages` sendiri, periksa apakah kode tersebut [mengedit giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking): jalankan sesi dengan header beta `thinking-binding-controls-2026-08-01` dan `prefix_mismatch_behavior: "drop_block"`, catat `input_transformations`, dan perbaiki setiap `prefix_binding_mismatch`. Entri `model_binding_mismatch` setelah peralihan model memang diharapkan.
* Pertahankan riwayat percakapan agar hanya bersifat tambahan (append-only). Bekukan `system` dan `tools` saat sesi dimulai dan pindahkan perubahan di tengah sesi ke pesan `role: "system"` serta blok `tool_addition` / `tool_removal`. Kirim pengingat per giliran sebagai pesan sistem yang terbatas pada giliran tersebut dan tidak pernah Anda hapus. Pangkas konteks di sisi server atau hapus blok thinking dari giliran mana pun yang Anda bawa melintasi ringkasan sisi klien. Rujuk file lintas giliran menggunakan `file_id`.
* Atur `prefix_mismatch_behavior` pada setiap permintaan produksi. `"error"` menggagalkan permintaan yang mengirim kembali blok thinking yang tidak valid. `"drop_block"` membuang blok yang tidak valid dan membiarkan permintaan berhasil. Pantau error 400 atau entri `input_transformations`.
* Tinjau agent loop untuk perilaku satu pemanggilan alat per giliran dan tambahkan instruksi batching.
* Jika antarmuka Anda menampilkan teks progres di antara pemanggilan alat, atur `thinking.display` ke `"updates"` (beta) atau `"summarized"` dan minta pembaruan dalam prompt.
* Jika Anda mengubah effort di antara permintaan, pindahkan perubahan ke pesan `role: "system"` [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta) untuk mempertahankan hit cache.
* Tangani `stop_reason: "refusal"` dan baca `stop_details.category`. Pertimbangkan `fallbacks: "default"` (beta).
* Evaluasi ulang `effort` dengan sweep baru, dimulai dari `high`, dan tetapkan ulang baseline biaya dan latency pada beban kerja Anda sendiri. Tokenizer tidak berubah. Pembacaan cache prompt seharga seperempat tarif Claude Fable 5.
* Jika Anda memiliki [komitmen Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#existing-priority-tier-commitments) untuk model Anda saat ini, komitmen tersebut tidak mencakup Claude Fable 5.1, yang tidak didukung di Priority Tier.

## Migrasi ke Claude Fable 5.1 dari Claude Opus 5

Claude Fable 5.1 menggunakan pola [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) dan [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 5. Model ini mempertahankan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, [128k token output maksimum](https://platform.claude.com/docs/id/models/overview), minimum caching prompt 512 token, dan dukungan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Pembatasan prefill, pembatasan parameter sampling, dan default `"omitted"` untuk `thinking.display` juga tetap berlaku. Terapkan semua yang ada di [Migrasi ke Claude Fable 5.1 dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1), ditambah hal berikut.

### Perbarui nama model Anda

```python
model = "claude-opus-5"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk Claude Mythos 5.1, yang menawarkan kemampuan yang sama bagi organisasi terverifikasi:
model = "claude-mythos-5-1"  # After
```

### Apa yang berubah

1. **Thinking tidak dapat dinonaktifkan:** Claude Opus 5 menerima `thinking: {type: "disabled"}` pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Pada `claude-fable-5-1` dan `claude-mythos-5-1`, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) selalu aktif, dan `thinking: {type: "disabled"}` mengembalikan error 400 pada tingkat effort apa pun. Hapus field tersebut, kendalikan penggunaan token dengan tingkat effort yang lebih rendah, dan tinjau kembali `max_tokens` untuk beban kerja yang berjalan dengan thinking dinonaktifkan. Respons dari beban kerja tersebut dapat dimulai dengan blok `thinking`, jadi pilih blok konten berdasarkan `type`, bukan berdasarkan posisi.

2. **Pilihan alat paksa tidak didukung:** Claude Opus 5 menerima `tool_choice` `any` dan `tool`. `claude-fable-5-1` dan `claude-mythos-5-1` mengembalikan error 400. Lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).

3. **Pemikiran yang dipertahankan lintas model:** Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok pemikiran Claude Opus 5: percakapan yang berpindah dari `claude-opus-5` ke `claude-fable-5-1` atau `claude-mythos-5-1` mempertahankan penalarannya. Claude Opus 5 tidak dapat membaca blok dari kedua model tersebut. Lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).

4. **Mengedit giliran sebelumnya membuat blok pemikiran tidak valid:** Claude Opus 5 tidak menjalankan pemeriksaan prefiks. Pada `claude-fable-5-1` dan `claude-mythos-5-1`, mengedit pesan sebelumnya, membangun ulang `system` atau `tools`, atau melakukan pemadatan di sisi klien di antara permintaan akan membuat setiap blok pemikiran berikutnya tidak valid. Sebelum Anda mengalihkan lalu lintas, jalankan [pemeriksaan tiga langkah](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-check-integration) dari bagian Claude Fable 5.

5. **Teks di antara pemanggilan alat dikembalikan dalam blok thinking:** Pada Claude Opus 5, teks yang ditulis model di antara pemanggilan alat dikembalikan sebagai blok `text`. Pada `claude-fable-5-1`, seperti pada Claude Fable 5, narasi tersebut dikembalikan sebagai blok `thinking` berupa pembaruan progres, satu sebelum setiap pemanggilan alat. Dengan `thinking.display` default berupa `"omitted"`, blok-blok tersebut tidak berisi teks yang dapat dibaca. Jika antarmuka Anda menampilkan narasi tersebut, atur `thinking.display` ke `"updates"` (beta) untuk menerima pembaruan progres sebagai teks sementara penalaran tetap tersembunyi, atau ke `"summarized"` untuk menerima keduanya. Kemudian tampilkan blok `thinking` yang tidak kosong di antara blok `tool_use`. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).

6. **Pengklasifikasi keamanan dan perutean fallback:** Claude Fable 5.1 menjalankan pengklasifikasi keamanan yang mencakup kategori `stop_details` yang sama dengan Claude Fable 5, yaitu cakupan yang lebih luas daripada pengklasifikasi Claude Opus 5. Perkirakan adanya nilai `stop_details.category` tambahan, seperti `"bio"`; lihat [tabel kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar lengkapnya. Untuk konfigurasi `fallbacks` dan target yang diizinkan, lihat [Gunakan `fallbacks: "default"` untuk penolakan](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-recommended-changes).

7. **Harga:** $10 USD per juta token input dan $50 USD per juta token output, dibandingkan dengan $5 USD dan $25 USD untuk Claude Opus 5. Pembacaan dari caching prompt dikenakan biaya $0,25 USD per juta token, setengah dari tarif Claude Opus 5. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

8. **Retensi data:** Claude Fable 5.1 dan Claude Mythos 5.1 memerlukan retensi data 30 hari, tidak tersedia di bawah pengaturan ZDR kecuali secara tegas diizinkan oleh Anthropic, dan ditetapkan sebagai Covered Models. Claude Opus 5 tersedia di bawah ZDR. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan retensi data nol (ZDR), konfirmasikan kelayakan terlebih dahulu: model-model ini tidak tersedia di bawah ZDR kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-5` menjadi `claude-fable-5-1` (atau `claude-mythos-5-1`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun: konfigurasi tersebut mengembalikan error 400 pada `claude-fable-5-1`. Kendalikan penggunaan token dengan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah, dan tinjau kembali `max_tokens`.
* Jika Anda menghapus `thinking: {type: "disabled"}`, perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text`: respons dapat dimulai dengan blok `thinking`, jadi pilih blok konten berdasarkan `type` sebagai gantinya.
* Ganti `tool_choice` paksa (`any` atau `tool`) dengan `auto` ditambah instruksi eksplisit (giliran `user` atau pesan sistem di tengah percakapan) dan alat `strict: true`, atau dengan output JSON.
* Jika antarmuka Anda menampilkan teks di antara pemanggilan alat, atur `display: "updates"` (beta) atau `"summarized"` dan tampilkan blok `thinking` yang tidak kosong.
* Terapkan item advisor, preserved-thinking, append-only, perilaku, effort, dan fallback dari [daftar periksa Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migration-checklist-fable-5-1-from-fable-5).
* Tetapkan ulang baseline biaya pada beban kerja Anda sendiri. Tokenizer tidak berubah. Harga per token berbeda.

## Migrasi ke Claude Fable 5.1 dari Claude Opus 4.8 atau sebelumnya

Ikuti daftar periksa berikut. Pada Claude Opus 4.7 atau sebelumnya, mulailah dengan bagian yang sesuai dalam [panduan migrasi Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/migration-guide).

### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk Claude Mythos 5.1, yang menawarkan kemampuan yang sama bagi organisasi terverifikasi:
model = "claude-mythos-5-1"  # After
```

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan retensi data nol (ZDR), konfirmasikan kelayakan terlebih dahulu: model-model ini tidak tersedia di bawah ZDR kecuali diizinkan secara tegas oleh Anthropic. Claude Opus 4.8 tersedia di bawah ZDR.
* Perbarui nama model dari `claude-opus-4-8` menjadi `claude-fable-5-1` (atau `claude-mythos-5-1`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun dan tinjau kembali `max_tokens`. Permintaan tanpa field `thinking` berjalan dengan adaptive thinking.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text`: respons dapat dimulai dengan blok `thinking`, jadi pilih blok konten berdasarkan `type` sebagai gantinya.
* Ganti `tool_choice` paksa (`any` atau `tool`) dengan `auto` ditambah instruksi eksplisit (giliran `user` atau pesan sistem di tengah percakapan) dan alat `strict: true`, atau dengan output JSON.
* Kirim kembali blok `thinking` tanpa perubahan dan perlakukan teksnya hanya untuk tampilan. Claude Fable 5.1 dan Claude Mythos 5.1 membaca blok thinking Claude Opus 4.8: percakapan yang berpindah ke `claude-fable-5-1` atau `claude-mythos-5-1` mempertahankan penalaran sebelumnya. Claude Opus 4.8 tidak dapat membaca blok milik kedua model tersebut.
* Jika kode Anda membangun array `messages` sendiri, periksa apakah kode tersebut [mengedit giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking). Integrasi yang ditulis untuk Claude Opus 4.8 dan sebelumnya sering memotong giliran lama, menghapus atau membangun ulang pesan sebelumnya, atau menyegarkan prompt `system` di setiap permintaan, dan Claude Opus 4.8 tidak mengembalikan error untuk semua itu. Pada `claude-fable-5-1` dan `claude-mythos-5-1`, masing-masing hal tersebut membuat blok thinking berikutnya tidak valid.
* Tangani `stop_reason: "refusal"`, baca `stop_details.category`, dan pertimbangkan `fallbacks: "default"` (beta).
* Terapkan item advisor, Priority Tier, preserved-thinking, append-only, perilaku, effort per pesan, dan pembaruan progres dari [daftar periksa Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migration-checklist-fable-5-1-from-fable-5).
* Evaluasi ulang `effort` (mulai dari `high`), tinjau prompt yang mendekati [batas minimum caching](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) 512 token (1.024 token pada Claude Opus 4.8), dan tetapkan ulang baseline biaya dan latensi. Harga per token berbeda, dan token thinking ditagih sebagai token output, sehingga beban kerja yang berjalan tanpa thinking pada Claude Opus 4.8 dapat menghasilkan lebih banyak token output per permintaan.

## Migrasi ke Claude Mythos 5.1 dari Claude Mythos 5

[Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview) adalah padanan Claude Fable 5.1 untuk organisasi yang terverifikasi melalui program verifikasi Anthropic, seperti [Cyber Verification Program](https://support.claude.com/en/articles/14604842). Pastikan organisasi Anda memiliki akses ke Claude Mythos 5.1 sebelum Anda mengganti ID model.

Semua yang ada di [Migrasi ke Claude Fable 5.1 dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1) berlaku, dengan `claude-mythos-5` dan `claude-mythos-5-1` sebagai pengganti ID model Claude Fable. Claude Mythos 5.1 dapat membaca blok pemikiran Claude Mythos 5; Claude Mythos 5 tidak dapat membaca blok pemikiran Claude Mythos 5.1. Pada Claude Mythos 5.1, permintaan yang mengirimkan kembali blok pemikiran yang tidak valid dan membiarkan `prefix_mismatch_behavior` tidak diatur akan mendapatkan error 400 (lihat [Ketika `prefix_mismatch_behavior` tidak diatur](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#enforcement)).

### Perbarui nama model Anda

```python
model = "claude-mythos-5"  # Before
model = "claude-mythos-5-1"  # After
```

### Daftar periksa migrasi

* Kerjakan [daftar periksa Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migration-checklist-fable-5-1-from-fable-5) dengan ID model Claude Mythos. Lewati item Priority Tier-nya: Claude Mythos 5 tidak didukung di Priority Tier.
* Jalankan pemeriksaannya untuk [pengeditan pada giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking) sebelum Anda beralih: Claude Mythos 5 menerima pengeditan tersebut, tetapi pengeditan itu membuat blok pemikiran Claude Mythos 5.1 menjadi tidak valid.
