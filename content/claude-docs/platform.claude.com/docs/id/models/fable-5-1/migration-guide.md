---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5-1/migration-guide
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: da1d9fdfd9ecbdad85cb842c61586c468dbfbc69d622ba13606a3fa73455f52e
---

---
title: Migrasi ke Claude Fable 5.1 dan Claude Mythos 5.1
url: https://platform.claude.com/docs/id/models/fable-5-1/migration-guide
description: "Migrasi ke Claude Fable 5.1 dan Claude Mythos 5.1 dari Claude Fable 5, Claude Mythos 5, Claude Opus 5, atau Claude Opus 4.8: ID model, perubahan yang merusak kompatibilitas, dan daftar periksa migrasi."
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-fable-5-1
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

[Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1) menggantikan Claude Fable 5 dengan harga input dan output yang sama, dengan pembacaan cache seperempat dari biayanya. Model ini tersedia di Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). [Claude Mythos 5.1](https://anthropic.com/glasswing) memiliki kemampuan yang sama dan hanya ditawarkan kepada pelanggan yang disetujui dalam Project Glasswing. Untuk perbedaan perilaku dan pola prompting, lihat [Prompting Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).

Pengaturan dasar yang dimiliki bersama oleh `claude-fable-5-1` dan `claude-mythos-5-1`:

* **Thinking:** [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) selalu aktif, tidak berubah dari Claude Fable 5. Model memutuskan kapan dan seberapa banyak harus berpikir. Tidak diperlukan konfigurasi `thinking`. Baik `thinking: {type: "disabled"}` maupun "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Prefill:** Melakukan prefill pada pesan asisten mengembalikan error 400, tidak berubah dari Claude Fable 5. Gunakan instruksi "system prompt" (prompt sistem) sebagai gantinya.
* **Tool choice:** `{type: "auto"}` (default) dan `{type: "none"}` didukung. Memaksa pemanggilan alat dengan `{type: "any"}` atau `{type: "tool", name: "..."}` mengembalikan error 400. Lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).
* **Thinking yang dipertahankan lintas model:** Claude Fable 5.1 membaca blok thinking dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude sebelumnya. Tidak satu pun dari model tersebut dapat membaca blok milik Claude Fable 5.1. Lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).
* **Jendela konteks dan output:** ["Context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan hingga 128k token output per permintaan.
* **Harga:** $10 USD per juta token input dan $50 USD per juta token output, sama dengan Claude Fable 5. Pembacaan cache prompt seharga $0,25 USD per juta token, seperempat dari tarif Claude Fable 5. Lihat [Harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
* **Retensi data:** Kedua model memerlukan retensi data 30 hari, tidak tersedia di bawah pengaturan "zero data retention" (retensi data nol), atau ZDR, kecuali diizinkan secara tegas oleh Anthropic, dan ditetapkan sebagai Covered Models, sama seperti Claude Fable 5 dan Claude Mythos 5. Di Claude API, permintaan dari organisasi atau workspace tanpa retensi 30 hari mengembalikan `invalid_request_error` 400. Organisasi dengan pengaturan ZDR harus menghubungi tim akun Anthropic mereka, atau mengonfigurasi retensi per workspace. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.

Di mana kedua model berbeda:

* **Ketersediaan:** Claude Fable 5.1 tidak memerlukan persetujuan akses. Claude Mythos 5.1 hanya tersedia bagi pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing). Hubungi tim akun Anthropic Anda untuk mendapatkan akses.
* **Pengklasifikasi keamanan:** Claude Fable 5.1 menjalankan pengklasifikasi keamanan yang mencakup kategori `stop_details` yang sama dengan Claude Fable 5. Permintaan yang ditolak mengembalikan `stop_reason: "refusal"` dengan `stop_details.category`, dan dapat beralih ke model lain dengan parameter `fallbacks` atau percobaan ulang di sisi klien. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* **Priority Tier:** Tidak satu pun dari kedua model didukung di [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models). Claude Fable 5 didukung.

## Migrasi ke Claude Fable 5.1 dari Claude Fable 5

Migrasi sebagian besar bersifat drop-in. Permukaan API, batasan, harga per token, tokenizer, adaptive thinking yang selalu aktif, penanganan penolakan, dan kategori `stop_details` semuanya sama dengan Claude Fable 5. Yang berubah: tool choice paksa mengembalikan error 400, blok thinking hanya dipertahankan untuk model yang menghasilkannya atau model yang lebih baru dan hanya dalam percakapan yang menghasilkannya, pembacaan cache lebih murah, dan perilaku agent-loop berbeda dalam tiga hal. Perubahan yang sama berlaku untuk [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-mythos-5-to-claude-mythos-5-1), kecuali pemeriksaan percakapan pada blok thinking, yang tidak dijalankan oleh Claude Mythos 5.1.

### Perbarui nama model Anda

```python
model = "claude-fable-5"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5-1"  # After
```

### Perubahan yang merusak kompatibilitas

1. **Tool choice paksa tidak didukung:** Claude Fable 5 menerima `tool_choice` `auto`, `none`, `any`, dan `tool`. Pada `claude-fable-5-1`, `{type: "any"}` dan `{type: "tool", name: "..."}` mengembalikan `invalid_request_error` 400:

   ```text wrap
   tool_choice: type "tool" and "any" are not supported for this model.
   ```

   Pemeriksaan ini berlaku pada Messages API, Message Batches API, dan endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

   Sebelum (Claude Fable 5):

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d @- <<'EOF'
     {
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
     }
     EOF
     ```

     <MultiFileExample language="cli" label="CLI">
       ```bash CLI
       ant messages create < request.yaml
       ```

       <File filename="request.yaml">
         ```yaml
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
         ```
       </File>
     </MultiFileExample>

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
         Messages = [
             new() { Role = Role.User, Content = "Summarize: The meeting moved to Thursday." }
         ]
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
         model: 'claude-fable-5',
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

   Sesudah (Claude Fable 5.1): biarkan `tool_choice` pada `auto`, sebutkan nama alat dalam instruksi, dan atur `strict: true` agar pemanggilan sesuai dengan skema Anda. (Dalam organisasi [CMEK](https://platform.claude.com/docs/id/manage-claude/cmek), di mana [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (output terstruktur), termasuk `strict: true`, tidak tersedia pada model Claude Fable, andalkan instruksi saja.) Sebagai contoh:

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d @- <<'EOF'
     {
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
     }
     EOF
     ```

     <MultiFileExample language="cli" label="CLI">
       ```bash CLI
       ant messages create < request.yaml
       ```

       <File filename="request.yaml">
         ```yaml
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
         ```
       </File>
     </MultiFileExample>

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
         Model = "claude-fable-5-1",
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
             new() { Role = Role.User, Content = "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result." }
         ]
     };

     var message = await client.Messages.Create(parameters);
     Console.WriteLine(message);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-fable-5-1",
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
             .model("claude-fable-5-1")
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
         { role: "user", content: "Summarize: The meeting moved to Thursday. Call the record_summary tool with your result." }
       ]
     )
     puts message
     ```
   </CodeGroup>

   Lihat [Penggunaan alat strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) dan [Memaksa penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use). Jika Anda memaksa alat hanya untuk mendapatkan JSON yang sesuai skema, gunakan [output JSON](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-outputs) (`output_config.format`) sebagai gantinya.

   Jika aplikasi Anda, bukan pengguna, memerlukan pemanggilan alat tertentu pada giliran saat ini dalam percakapan multi-giliran, tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) setelah giliran `user` terakhir. Sebutkan nama alat, nyatakan bahwa pemanggilan tersebut wajib untuk giliran ini, dan minta Claude untuk membuka responsnya dengan pemanggilan itu. Karena pesan ditambahkan di akhir alih-alih ditulis ke dalam prompt `system` tingkat atas, giliran sebelumnya tetap identik byte demi byte dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) mereka:

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d @- <<'EOF'
     {
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
           "content": "Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."
         }
       ]
     }
     EOF
     ```

     <MultiFileExample language="cli" label="CLI">
       ```bash CLI
       ant messages create < request.yaml
       ```

       <File filename="request.yaml">
         ```yaml
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
         ```
       </File>
     </MultiFileExample>

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
             # Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
             # kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem membuat
             # giliran sebelumnya tidak berubah.
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
         // Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
         // kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem
         // membiarkan giliran sebelumnya tidak berubah.
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
         Model = "claude-fable-5-1",
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
             new() { Role = Role.User, Content = "My headphones from order A1234 arrived yesterday." },
             new() { Role = Role.Assistant, Content = "Thanks for confirming. How can I help with order A1234?" },
             new() { Role = Role.User, Content = "I opened the box. Can I still return them?" },
             // Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
             // kebijakan apa pun. Menambahkan persyaratan ini sebagai pesan sistem
             // membiarkan giliran sebelumnya tidak berubah.
             new()
             {
                 Role = Role.System,
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
     	Model:     "claude-fable-5-1",
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
     		// Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
     		// kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem
     		// membiarkan giliran sebelumnya tidak berubah.
     		{
     			Role: anthropic.MessageParamRoleSystem,
     			Content: []anthropic.ContentBlockParamUnion{
     				anthropic.NewTextBlock("Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only."),
     			},
     		},
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
             .model("claude-fable-5-1")
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
             // Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
             // kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem membuat
             // giliran sebelumnya tidak berubah.
             .addMessage(MessageParam.builder()
                 .role(MessageParam.Role.SYSTEM)
                 .content("Tool-use requirement for the current turn: the application requires a call to the search_help_center tool in your response to the user's latest message. Begin your response with the search_help_center tool call. Do not reply with text only.")
                 .build())
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
             // Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
             // kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem
             // membiarkan giliran sebelumnya tidak berubah.
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
         # Aplikasi mewajibkan pencarian pusat bantuan sebelum jawaban
         # kebijakan apa pun. Menambahkan persyaratan sebagai pesan sistem membuat
         # giliran sebelumnya tetap tidak berubah.
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

2. **Blok thinking hanya dipertahankan untuk model yang menghasilkannya, atau model yang lebih baru:** Setiap blok `thinking` mencatat model mana yang menghasilkannya. Claude Fable 5.1 membaca bloknya sendiri dan blok dari Claude Mythos 5.1, Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model Claude sebelumnya. Percakapan yang berpindah ke `claude-fable-5-1` dari salah satu model tersebut mempertahankan penalaran sebelumnya. Kondisi ini bersifat satu arah: selain Claude Mythos 5.1, tidak satu pun dari model tersebut dapat membaca blok milik Claude Fable 5.1.

   Percakapan yang berjalan di Claude Fable 5.1 dapat berakhir di model yang lebih lama melalui peralihan router, percobaan ulang di sisi klien, atau [fallback penolakan pengklasifikasi](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback), termasuk [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback). API menghapus blok yang tidak dapat dibaca model tersebut sebelum model melihatnya, permintaan berhasil, dan Anda tidak ditagih untuk token input yang dibuang. Model target merencanakan ulang tanpa penalaran tersebut, yang dapat meningkatkan biaya dan latensi pada giliran pertama setelah peralihan. Untuk melihat apa yang dibuang, kirim [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01`: respons kemudian membawa array `input_transformations` yang menyebutkan setiap blok yang dibuang dengan `reason: "model_binding_mismatch"`. Lihat [Thinking yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-for-model).

3. **Mengedit giliran sebelumnya membatalkan blok thinking:** Setiap blok `thinking` dari Claude Fable 5.1 hanya valid terhadap prompt `system`, `tools`, dan riwayat percakapan yang mendahuluinya. Jika Claude Code, claude.ai, [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), atau [Claude Agent SDK](https://code.claude.com/docs/id/agent-sdk/overview) mengelola riwayat percakapan Anda, prefiks tersebut sudah dijaga tetap utuh. Jika kode Anda membangun array `messages` sendiri, butir ini berlaku untuk Anda, dan [Thinking yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) adalah panduan integrasi lengkapnya. Di mana pemeriksaan ini diberlakukan, permintaan yang mengirim kembali blok tersebut setelah salah satu dari hal-hal itu berubah akan ditolak dengan error 400:

   ```text wrap
   messages.5.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block". That setting requires the `thinking-binding-controls-2026-08-01` value in the `anthropic-beta` header.
   ```

   API memberlakukan pemeriksaan ini untuk akun baru yang dibuat pada atau setelah 31 Agustus 2026. Untuk akun yang dibuat lebih awal, API mencatat ketidakcocokan tetapi tidak menindaklanjutinya kecuali permintaan mengatur `thinking.block_binding.prefix_mismatch_behavior`, yang mengaktifkan pemberlakuan. Anthropic berencana memberlakukan pemeriksaan ini untuk setiap akun pada model mendatang, jadi buatlah aplikasi Anda kompatibel sekarang: pola yang sama menjaga cache prompt tetap hangat, dan Anda dapat menguji terhadap pemeriksaan ini dari akun mana pun dengan mengirim `prefix_mismatch_behavior`. Jika Anda merilis alat atau framework yang dijalankan orang dengan kunci API mereka sendiri, ujilah dengan cara itu sebelum peluncuran: kunci Anda kemungkinan berada di akun yang lebih lama, dan pengguna Anda di akun baru akan terkena pemeriksaan ini sebelum Anda. Untuk melihat apakah akun Anda sendiri diberlakukan secara default, kirim permintaan yang mengedit riwayat tanpa header beta: error 400 yang menyebutkan header tersebut berarti ya.

   Error ini bersifat permanen untuk body permintaan tersebut: loop percobaan ulang otomatis tidak akan menghilangkannya. Untuk melanjutkan tanpa penalaran yang dibatalkan alih-alih gagal, hapus blok `thinking` dari riwayat dan coba ulang sekali, atau kirim [header beta](https://platform.claude.com/docs/id/api/beta-headers) `thinking-binding-controls-2026-08-01` dan atur `prefix_mismatch_behavior` ke `"drop_block"` (default-nya adalah `"error"`). Dengan `"drop_block"`, API membuang blok yang tidak cocok dan setiap blok thinking setelahnya dalam percakapan, dan melaporkan masing-masing dengan `reason: "prefix_binding_mismatch"` dalam array `input_transformations` pada respons:

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

     <MultiFileExample language="cli" label="CLI">
       ```bash CLI
       ant beta:messages create \
         --beta thinking-binding-controls-2026-08-01 \
         --transform '{content.#(type=="text")#.text,input_transformations}' \
         --format yaml < request.yaml
       ```

       <File filename="request.yaml">
         ```yaml
         model: claude-fable-5-1
         max_tokens: 16000
         thinking:
           type: adaptive
           block_binding:
             prefix_mismatch_behavior: drop_block
         messages:
           - role: user
             content: What is the greatest common divisor of 1071 and 462?
         ```
       </File>
     </MultiFileExample>

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

     AnthropicClient client = new();

     var response = await client.Beta.Messages.Create(
         new()
         {
             Model = "claude-fable-5-1",
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
                 new()
                 {
                     Role = Role.User,
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
     	Model:     "claude-fable-5-1",
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

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model("claude-fable-5-1")
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
       model: "claude-fable-5-1",
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

   Endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) menjalankan pemeriksaan yang sama. Lihat [Kontrol untuk blok yang tidak dipertahankan (beta)](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-thinking-controls) untuk bentuk respons dan penempatan streaming.

   Pola yang membatalkan blok thinking berikutnya, dan apa yang harus dilakukan sebagai gantinya:

   * Mengedit, mengurutkan ulang, atau menghapus giliran sebelumnya. Ini termasuk menghapus hasil alat lama, memotong giliran dari tengah transkrip, dan compaction sisi klien yang mempertahankan giliran terbaru beserta blok thinking-nya secara verbatim di belakang ringkasan (termasuk compaction latar belakang yang menukar ringkasannya beberapa giliran kemudian). Sebagai gantinya, gunakan [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) ([pembersihan hasil alat](https://platform.claude.com/docs/id/build-with-claude/context-editing#tool-result-clearing) untuk hasil alat lama), atau salah satu bentuk compaction sisi klien di [Pangkas konteks di server](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-trim-context).
   * Menyisipkan konten yang tidak Anda simpan, misalnya pengingat per giliran yang ditambahkan setelah blok `tool_result` dan dihapus pada permintaan berikutnya. Sebagai gantinya, kirim pengingat sebagai [pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) dan biarkan dalam riwayat.
   * Membangun ulang prompt `system` tingkat atas atau array `tools` di antara permintaan dalam percakapan yang sama, misalnya untuk memperbarui tanggal saat ini atau untuk menambah atau menghapus alat. Sebagai gantinya, tambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) yang membawa instruksi baru ("The current date is 2026-09-14.") atau blok `tool_addition` dan `tool_removal`.
   * URL gambar atau dokumen yang menyajikan byte berbeda pada permintaan berikutnya. Pemeriksaan mencakup byte-nya, bukan string URL, jadi signed URL yang berotasi untuk file yang sama tidak masalah. Untuk konten yang Anda referensikan lintas giliran, unggah sekali dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan kirim `file_id`, atau kirim base64.

   Setiap pengganti juga menjaga giliran sebelumnya identik byte demi byte dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) yang akan hilang jika riwayat, prompt `system`, atau array `tools` diedit.

   Pola yang tetap berfungsi:

   * Riwayat append-only: menambahkan giliran dan mengirim kembali giliran sebelumnya persis seperti yang dikirim dan diterima, termasuk pesan `role: "system"` yang ditambahkan.
   * Menghapus blok thinking dari giliran asisten sebelumnya, dimulai dari yang terlama.
   * Mengubah `effort`, `max_tokens`, atau parameter permintaan lain di luar `system`, `tools`, dan `messages`, serta menambah atau memindahkan penanda `cache_control`.
   * Compaction sisi server dan context editing, termasuk [pembersihan blok thinking](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing). Keduanya tidak dihitung sebagai pengeditan, karena pemeriksaan membandingkan percakapan sebagaimana Anda mengirimnya.

   Untuk memeriksa integrasi yang sudah ada:

   1. Tangkap body permintaan persis yang dikirimnya selama beberapa giliran normal, termasuk compaction atau perubahan alat jika produk Anda memilikinya. Untuk setiap pasangan permintaan berurutan, bandingkan prompt `system`, array `tools`, dan prefiks bersama dari `messages`. Semuanya harus identik byte demi byte hingga giliran yang baru ditambahkan.
   2. Jalankan sesi multi-giliran normal terhadap `claude-fable-5-1` dengan header beta `thinking-binding-controls-2026-08-01` dan `prefix_mismatch_behavior: "drop_block"`, dan catat `input_transformations` pada setiap respons. Array kosong pada setiap giliran berarti riwayat utuh. Entri dengan `reason: "prefix_binding_mismatch"` berarti sesuatu sebelum blok di `path` berubah sejak permintaan sebelumnya. Entri dengan `reason: "model_binding_mismatch"` berarti percakapan berpindah model, yang bukan bug dalam kode Anda. Ini berfungsi dari akun mana pun, karena mengatur field tersebut mengaktifkan pemberlakuan untuk permintaan itu. Di CI, atur `"error"` sebagai gantinya agar pengeditan menggagalkan proses.
   3. Pilih pengaturan produksi. Biarkan default `"error"` jika ketidakcocokan prefiks hanya dapat berarti bug dalam kode Anda, atau atur `"drop_block"` untuk membuang blok yang terpengaruh alih-alih gagal, dan pantau error 400 atau entri `input_transformations` dalam kedua kasus.

   Membuang blok thinking sekali, misalnya pada batas compaction, hanya berdampak kecil. Integrasi yang membatalkan thinking sebelumnya pada setiap permintaan memulai ulang cache prompt setiap kali, yang dapat meningkatkan biaya per tugas (lihat [Jaga riwayat percakapan tetap append-only](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)).

### Perubahan perilaku

1. **Lebih sedikit pemanggilan alat paralel dalam agent loop panjang:** Dalam loop yang berjalan lama di mana pembacaan independen berikutnya hanya tersirat dari tugas (agen coding kustom, harness bash-dan-editor, computer use), Claude Fable 5.1 mungkin mengeluarkan satu pemanggilan alat per giliran. Setiap giliran tambahan memakan token, satu round trip, dan waktu nyata. Tambahkan instruksi batching satu kalimat setelah setiap pesan pengguna sebagai [pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: "next_user_message"`, beta), atau, tanpa beta, dalam blok teks setelah blok `tool_result`, dan biarkan salinan sebelumnya dalam riwayat pada permintaan berikutnya. Lihat [Batch pemanggilan alat independen dalam agent loop](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops).

2. **Lebih sedikit pesan progres di antara pemanggilan alat:** Claude Fable 5.1 menulis lebih sedikit pembaruan status selama urutan alat yang panjang dibandingkan Claude Fable 5, dan ringkasan agentic coding-nya lebih pendek. Jika antarmuka Anda merender pembaruan tersebut, atur `thinking.display` ke `"updates"` (beta) atau `"summarized"` dan minta secara eksplisit melalui prompt. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates) dan [Minta pembaruan progres untuk pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates).

3. **Lebih sedikit pemanggilan pencarian dan retrieval pada effort rendah:** Pada effort `low`, Claude Fable 5.1 lebih sering menjawab dari memori dibandingkan Claude Fable 5 alih-alih memanggil alat pencarian atau retrieval. Jika produk Anda mengandalkan retrieval pada effort rendah, naikkan effort untuk permintaan tersebut atau beri tahu model kapan harus mencari. Lihat [Pemicuan pencarian pada effort rendah](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort).

Untuk perbedaan dalam kepadatan prosa, pemformatan chat, pengutipan dalam ringkasan, dan pengeditan file, yang tidak memengaruhi integrasi API, lihat [Berubah dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/whats-new-fable-5-1#changed-from-claude-fable-5).

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib, tetapi masing-masing menurunkan biaya atau latensi atau menghilangkan mode kegagalan:

1. **Ubah effort di tengah percakapan (beta):** Pada Claude Fable 5, `output_config.effort` berada di tingkat permintaan, dan mengubahnya di antara permintaan membuang prefiks yang di-cache dari giliran sebelumnya. Pada `claude-fable-5-1`, pesan `role: "system"` yang hanya membawa `output_config` menaikkan effort untuk langkah yang sulit atau menurunkannya untuk langkah rutin tanpa membatalkan [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching):

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

     <MultiFileExample language="cli" label="CLI">
       ```bash CLI
       ant beta:messages create \
         --beta mid-conversation-output-config-2026-07-01 \
         --transform 'content.#(type=="text").text' \
         --raw-output < request.yaml
       ```

       <File filename="request.yaml">
         ```yaml
         model: claude-fable-5-1
         max_tokens: 4096
         output_config:
           effort: high
         messages:
           - role: user
             content: Plan a migration from SQLite to PostgreSQL in three short steps.
           - role: assistant
             content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
           # Effort-only system message: the new level takes effect from the next user turn.
           - role: system
             content: []
             output_config:
               effort: low
           - role: user
             content: Summarize the plan in one sentence.
         ```
       </File>
     </MultiFileExample>

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

     AnthropicClient client = new();

     var response = await client.Beta.Messages.Create(new MessageCreateParams
     {
         Model = "claude-fable-5-1",
         MaxTokens = 4096,
         OutputConfig = new() { Effort = Effort.High },
         Messages =
         [
             new() { Role = Role.User, Content = "Plan a migration from SQLite to PostgreSQL in three short steps." },
             new() { Role = Role.Assistant, Content = "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
             // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             new()
             {
                 Role = Role.System,
                 Content = new([]),
                 OutputConfig = new() { Effort = BetaSystemMessageOutputConfigEffort.Low },
             },
             new() { Role = Role.User, Content = "Summarize the plan in one sentence." },
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
     	Model:     "claude-fable-5-1",
     	MaxTokens: 4096,
     	OutputConfig: anthropic.BetaOutputConfigParam{
     		Effort: anthropic.BetaOutputConfigEffortHigh,
     	},
     	Messages: []anthropic.BetaMessageParam{
     		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Plan a migration from SQLite to PostgreSQL in three short steps.")),
     		{
     			Role:    anthropic.BetaMessageParamRoleAssistant,
     			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
     		},
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
     import com.anthropic.models.beta.messages.BetaMessageParam;
     import com.anthropic.models.beta.messages.BetaOutputConfig;
     import com.anthropic.models.beta.messages.BetaSystemMessageOutputConfig;
     import com.anthropic.models.beta.messages.MessageCreateParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         MessageCreateParams params = MessageCreateParams.builder()
             .model("claude-fable-5-1")
             .maxTokens(4096L)
             .addBeta(AnthropicBeta.MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01)
             .outputConfig(BetaOutputConfig.builder()
                 .effort(BetaOutputConfig.Effort.HIGH)
                 .build())
             .addUserMessage("Plan a migration from SQLite to PostgreSQL in three short steps.")
             .addAssistantMessage("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")
             // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
             .addMessage(BetaMessageParam.builder()
                 .role(BetaMessageParam.Role.SYSTEM)
                 .contentOfBetaContentBlockParams(List.of())
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
       model: "claude-fable-5-1",
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

   Nilai tersebut berlaku untuk giliran pengguna berikutnya dan setiap giliran setelahnya hingga pesan `role: "system"` lain mengubahnya. Hanya level bernama yang diterima (`low`, `medium`, `high`, `xhigh`, `max`), dan header beta `mid-conversation-output-config-2026-07-01` diperlukan. Lihat [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta).

2. **Ubah instruksi dan alat dengan pesan sistem di tengah percakapan:** Untuk mengubah instruksi atau alat di tengah sesi, tambahkan [pesan `role: "system"`](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), dengan blok `tool_addition` dan `tool_removal` untuk perubahan alat (header beta `mid-conversation-tool-changes-2026-07-01`, dengan set alat lengkap dideklarasikan dalam `tools` di awal sesi). Ini mempertahankan hit cache prompt pada giliran sebelumnya dan menjaga riwayat percakapan tetap append-only. Pesan yang sama menggantikan `tool_choice` paksa ketika alat tertentu harus dijalankan pada giliran saat ini (lihat [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes)). Untuk pengingat yang hanya berlaku untuk satu giliran, kirim sebagai pesan `role: "system"` terpisah yang hanya berisi teks dengan `clear_at: "next_user_message"` ([pesan sistem cakupan giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages), header beta `mid-conversation-system-clear-at-2026-08-21`) dan biarkan dalam riwayat: pesan tersebut berhenti dirender setelah pesan pengguna berikutnya dan tidak memakan token setelah dibersihkan. Pesan yang membawa blok `tool_addition` atau `tool_removal` tidak dapat dicakup per giliran.

3. **Gunakan `fallbacks: "default"` untuk penolakan:** Tetap tangani `stop_reason: "refusal"` dan baca `stop_details.category` sebelum konten respons. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, atur `fallbacks: "default"` (beta, header `server-side-fallback-2026-07-01`). `"default"` mencoba ulang permintaan yang ditolak pada model yang direkomendasikan Anthropic untuk kategori tersebut. Target fallback yang diizinkan untuk Claude Fable 5.1 adalah Claude Opus 4.8 (`claude-opus-4-8`) dan Claude Opus 5 (`claude-opus-5`). Daftar `fallbacks` eksplisit dapat menyebutkan salah satunya. Model fallback tidak menerima blok thinking milik Claude Fable 5.1. Jika Anda membangun percobaan ulang sendiri, [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit) berlaku dengan ketentuan yang sama seperti Claude Fable 5. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

4. **Mulai dari effort `high` dan lakukan sweep:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah `high`, dan kelima level didukung. Pertahankan panduan Claude Fable 5: `high` untuk sebagian besar pekerjaan, dan `medium` sebagai kontrol biaya yang layak diuji. Peningkatan Claude Fable 5.1 dibandingkan Claude Fable 5 paling besar pada `xhigh` dan `max`, tetapi level tersebut juga menambah waktu berpikir dan waktu hingga respons pertama, jadi naikkan ke level tersebut untuk tugas yang paling sensitif terhadap kemampuan dan di mana eval Anda menunjukkan peningkatan. Jalankan sweep baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Fable 5. Lihat [Level effort yang direkomendasikan untuk Claude Fable 5.1](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-fable-5-1).

5. **Pangkas konteks di server, atau lakukan compaction dalam bentuk yang tidak membawa thinking usang:** Jika kode Anda memotong atau meringkas giliran lama di klien, perbaikan paling sederhana adalah memindahkan pekerjaan itu ke [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) sisi server atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing). Keduanya tidak dihitung sebagai pengeditan, karena [pemeriksaan riwayat](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking) membandingkan percakapan sebagaimana Anda mengirimnya, sehingga tidak ada yang dihapusnya membatalkan blok thinking berikutnya, dan [parameter `instructions`](https://platform.claude.com/docs/id/build-with-claude/compaction#custom-summarization-instructions) pada compaction menerima prompt peringkasan Anda sendiri. Jika Anda mempertahankan compaction di klien, pilih salah satu dari tiga bentuk:

   * **Compaction sederhana (direkomendasikan):** ganti seluruh riwayat dengan satu pesan ringkasan ditambah giliran pengguna baru dan jangan putar ulang apa pun lainnya. Tidak ada blok thinking yang dibawa, sehingga tidak ada yang gagal. Model Claude dilatih pada tugas jangka panjang dengan skema ini, dan kinerjanya sebanding dengan skema yang lebih rumit untuk sebagian besar beban kerja.
   * **Compaction keep-tail:** jika Anda mempertahankan giliran terbaru secara verbatim di belakang ringkasan, hapus blok `thinking` dan `redacted_thinking` dari giliran tersebut (teks dan pemanggilan alat boleh tetap ada), atau atur `prefix_mismatch_behavior: "drop_block"`. Thinking-nya dihasilkan terhadap riwayat lengkap dan akan gagal di belakang ringkasan jika tidak.
   * **Compaction latar belakang:** jika Anda membangun ringkasan di luar jalur kritis dan menukarnya kemudian, setiap giliran yang dihasilkan sementara itu membawa thinking yang mendahului penukaran. Kirim `"drop_block"` pada setiap permintaan yang masih membawa blok thinking yang dihasilkan sebelum penukaran (atau hapus blok tersebut sendiri; `input_transformations` pada respons pertama setelah penukaran mencantumkan persis blok mana saja), atau lakukan compaction secara sinkron.

   Jangan memotong giliran individual dari tengah transkrip: itu membatalkan setiap blok thinking berikutnya dan tidak ada bentuk sisi klien yang menghindarinya. Gunakan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) untuk perubahan instruksi yang Anda buat, atau [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) sisi server untuk penghapusan selektif. Lihat [Mengirim kembali blok compaction](https://platform.claude.com/docs/id/build-with-claude/compaction#passing-compaction-blocks-back).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-fable-5` menjadi `claude-fable-5-1` (atau `claude-mythos-5` menjadi `claude-mythos-5-1`).
* Ganti `tool_choice` paksa (`{type: "any"}` atau `{type: "tool", ...}`). Ini mengembalikan error 400. Gunakan `{type: "auto"}` ditambah instruksi eksplisit dan alat `strict: true`, atau output JSON. Letakkan instruksi di giliran `user`, atau di pesan `role: "system"` di tengah percakapan ketika aplikasi Anda mengharuskan pemanggilan tersebut.
* Terus kirimkan kembali blok `thinking` tanpa perubahan pada setiap giliran, termasuk yang kosong. Claude Fable 5.1 membaca blok dari Claude Opus 5, Claude Fable 5, Claude Mythos 5, dan model sebelumnya. Memindahkan percakapan dari Claude Fable 5.1 ke model sebelumnya akan membuang bloknya (Claude Mythos 5.1 membacanya).
* Jika kode Anda membangun array `messages` sendiri, periksa apakah kode tersebut [mengedit giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking): jalankan sesi dengan header beta `thinking-binding-controls-2026-08-01` dan `prefix_mismatch_behavior: "drop_block"`, catat `input_transformations`, dan perbaiki setiap `prefix_binding_mismatch`. Entri `model_binding_mismatch` setelah pergantian model adalah hal yang diharapkan.
* Jaga riwayat percakapan agar hanya-tambah (append-only): bekukan `system` dan `tools` pada awal sesi dan pindahkan perubahan di tengah sesi ke pesan `role: "system"` serta blok `tool_addition` / `tool_removal`, kirim pengingat per giliran sebagai pesan sistem lingkup-giliran yang tidak pernah Anda hapus, pangkas konteks di sisi server atau hapus blok thinking dari giliran mana pun yang Anda bawa melintasi ringkasan sisi klien, dan referensikan file lintas giliran dengan `file_id`.
* Pilih `prefix_mismatch_behavior` produksi (`"error"` secara default, atau `"drop_block"`) dan pantau. Jika Anda memelihara alat yang dijalankan orang lain dengan kunci API mereka sendiri, uji dengan field tersebut disetel: akun baru diberlakukan secara default meskipun akun Anda tidak.
* Tinjau loop agen untuk perilaku satu-pemanggilan-alat-per-giliran dan tambahkan instruksi batching.
* Jika antarmuka Anda merender teks progres di antara pemanggilan alat, setel `thinking.display` ke `"updates"` (beta) atau `"summarized"` dan minta pembaruan melalui prompt.
* Jika Anda mengubah effort di antara permintaan, pindahkan perubahan tersebut ke pesan `role: "system"` [effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta) untuk mempertahankan cache hit.
* Tangani `stop_reason: "refusal"` dan baca `stop_details.category`. Pertimbangkan `fallbacks: "default"` (beta).
* Evaluasi ulang `effort` dengan sapuan baru, dimulai dari `high`, dan tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah. Pembacaan cache prompt berbiaya seperempat dari tarif Claude Fable 5.

## Migrasi ke Claude Fable 5.1 dari Claude Opus 5

Claude Fable 5.1 menggunakan pola [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) dan [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 5. Model ini mempertahankan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, [128k token output maksimum](https://platform.claude.com/docs/id/models/overview), minimum caching prompt 512 token, dan dukungan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Pembatasan prefill, pembatasan parameter sampling, dan default `"omitted"` untuk `thinking.display` juga tetap berlaku. Terapkan semua yang ada di [Migrasi ke Claude Fable 5.1 dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1), ditambah hal-hal berikut.

### Perbarui nama model Anda

```python
model = "claude-opus-5"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5-1"  # After
```

### Apa yang berubah

1. **Thinking tidak dapat lagi dinonaktifkan:** Claude Opus 5 menerima `thinking: {type: "disabled"}` pada level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Pada `claude-fable-5-1` dan `claude-mythos-5-1`, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) selalu aktif, dan `thinking: {type: "disabled"}` mengembalikan error 400 pada level effort apa pun. Hapus field tersebut, kendalikan pengeluaran token dengan level effort yang lebih rendah, dan tinjau kembali `max_tokens` untuk beban kerja yang berjalan dengan thinking dinonaktifkan.

2. **Pilihan alat paksa tidak didukung:** Claude Opus 5 menerima `tool_choice` `any` dan `tool`. `claude-fable-5-1` mengembalikan error 400. Lihat [Perubahan yang merusak](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).

3. **Thinking yang dipertahankan lintas model:** Claude Fable 5.1 membaca blok thinking Claude Opus 5: percakapan yang berpindah dari `claude-opus-5` ke `claude-fable-5-1` mempertahankan penalarannya. Claude Opus 5 tidak dapat membaca blok Claude Fable 5.1. Blok Claude Fable 5.1 juga [berhenti valid ketika giliran sebelumnya berubah](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking): jika kode Anda mengedit pesan sebelumnya, membangun ulang `system` atau `tools`, atau melakukan kompaksi di klien di antara permintaan, Claude Opus 5 tidak keberatan, tetapi `claude-fable-5-1` menolak atau membuang setiap blok thinking berikutnya. Jalankan pemeriksaan tiga langkah di bagian tersebut sebelum mengalihkan lalu lintas. Lihat [Perubahan yang merusak](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-breaking-changes).

4. **Teks di antara pemanggilan alat dikembalikan dalam blok thinking:** Pada Claude Opus 5, teks yang ditulis model di antara pemanggilan alat dikembalikan sebagai blok `text`. Pada `claude-fable-5-1`, seperti pada Claude Fable 5, narasi tersebut dikembalikan sebagai blok `thinking` pembaruan progres, satu sebelum setiap pemanggilan alat. Di bawah `thinking.display` default `"omitted"`, blok tersebut tidak membawa teks yang dapat dibaca. Jika antarmuka Anda merender narasi tersebut, setel `display: "updates"` (beta) untuk menerima pembaruan progres sebagai teks sementara penalaran tetap tersembunyi, atau `"summarized"` untuk menerima keduanya. Kemudian render blok `thinking` yang tidak kosong di antara blok `tool_use`. Lihat [Pembaruan progres di antara pemanggilan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates).

5. **Pengklasifikasi keamanan dan perutean fallback:** Claude Fable 5.1 menjalankan pengklasifikasi keamanan yang mencakup kategori `stop_details` yang sama dengan Claude Fable 5, kumpulan yang lebih luas daripada pengklasifikasi khusus keamanan siber milik Claude Opus 5. Harapkan nilai `stop_details.category` di luar `"cyber"`, seperti `"bio"` dan `"reasoning_extraction"`; lihat [tabel kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk kumpulan lengkapnya. Untuk konfigurasi `fallbacks` dan target yang diizinkan, lihat [Gunakan `fallbacks: "default"` untuk penolakan](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-recommended-changes).

6. **Harga:** $10 USD per juta token input dan $50 USD per juta token output, dibandingkan dengan $5 USD dan $25 USD untuk Claude Opus 5. Pembacaan cache prompt adalah $0,25 USD per juta token, setengah dari tarif Claude Opus 5. Lihat [Harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

7. **Retensi data:** Claude Fable 5.1 dan Claude Mythos 5.1 memerlukan retensi data 30 hari, tidak tersedia di bawah pengaturan zero data retention (ZDR) kecuali diizinkan secara tegas oleh Anthropic, dan ditetapkan sebagai Covered Models. Claude Opus 5 tersedia di bawah ZDR. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan terlebih dahulu: model-model ini tidak tersedia di bawah ZDR kecuali diizinkan secara tegas oleh Anthropic. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-5` menjadi `claude-fable-5-1` (atau `claude-mythos-5-1`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun: ini mengembalikan error 400 pada `claude-fable-5-1`. Kendalikan pengeluaran token dengan level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah, dan tinjau kembali `max_tokens`.
* Ganti `tool_choice` paksa (`any` atau `tool`) dengan `auto` ditambah instruksi eksplisit (giliran `user` atau pesan sistem di tengah percakapan) dan alat `strict: true`, atau dengan output JSON.
* Jika antarmuka Anda merender teks di antara pemanggilan alat, setel `display: "updates"` (beta) atau `"summarized"` dan render blok `thinking` yang tidak kosong.
* Terapkan item thinking yang dipertahankan, pengeditan riwayat, perilaku, effort, dan fallback dari [daftar periksa Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migration-checklist-fable-5-1-from-fable-5).
* Tetapkan ulang baseline biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah. Harga per token berbeda.

## Migrasi ke Claude Fable 5.1 dari Claude Opus 4.8 atau sebelumnya

Pertama terapkan [Migrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Opus 4.8](https://platform.claude.com/docs/id/models/fable-5/migration-guide#migrating-from-claude-opus-48) untuk perubahan tingkat API dari Claude Opus 4.8. Panduan tersebut mencakup adaptive thinking, output thinking, penolakan, effort, minimum caching, harga, dan retensi data. Kemudian terapkan delta yang tersisa di [Migrasi ke Claude Fable 5.1 dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1). Pada Claude Opus 4.7 atau sebelumnya, mulailah dengan bagian [Migrasi ke Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide) yang sesuai.

### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5-1"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5-1"  # After
```

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan terlebih dahulu: model-model ini tidak tersedia di bawah ZDR kecuali diizinkan secara tegas oleh Anthropic. Claude Opus 4.8 tersedia di bawah ZDR.
* Perbarui nama model dari `claude-opus-4-8` menjadi `claude-fable-5-1` (atau `claude-mythos-5-1`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun dan tinjau kembali `max_tokens`. Permintaan tanpa field `thinking` berjalan dengan adaptive thinking.
* Ganti `tool_choice` paksa (`any` atau `tool`) dengan `auto` ditambah instruksi eksplisit (giliran `user` atau pesan sistem di tengah percakapan) dan alat `strict: true`, atau dengan output JSON.
* Kirimkan kembali blok `thinking` tanpa perubahan dan perlakukan teksnya sebagai hanya-untuk-tampilan. Claude Fable 5.1 membaca blok thinking Claude Opus 4.8: percakapan yang berpindah ke `claude-fable-5-1` mempertahankan penalaran sebelumnya. Claude Opus 4.8 tidak dapat membaca blok Claude Fable 5.1.
* Jika kode Anda membangun array `messages` sendiri, periksa apakah kode tersebut [mengedit giliran sebelumnya](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking). Integrasi yang ditulis untuk Claude Opus 4.8 dan sebelumnya sering memotong giliran lama, menghapus atau membangun ulang pesan sebelumnya, atau menyegarkan prompt `system` setiap permintaan, dan Claude Opus 4.8 tidak pernah keberatan. Pada `claude-fable-5-1` masing-masing hal tersebut membuat blok thinking berikutnya tidak valid.
* Tangani `stop_reason: "refusal"`, baca `stop_details.category`, dan pertimbangkan `fallbacks: "default"` (beta).
* Terapkan item thinking yang dipertahankan, pengeditan riwayat, perilaku, effort per pesan, dan pembaruan progres dari [daftar periksa Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migration-checklist-fable-5-1-from-fable-5).
* Evaluasi ulang `effort` (mulai dari `high`), tinjau prompt yang mendekati minimum caching 512 token, dan tetapkan ulang baseline biaya dan latensi. Harga per token berbeda.

## Migrasi ke Claude Mythos 5.1 dari Claude Mythos 5

[Claude Mythos 5.1](https://anthropic.com/glasswing) adalah pasangan berakses terbatas dari Claude Fable 5.1. Konfirmasikan akses organisasi Anda dengan tim akun Anthropic Anda sebelum mengganti ID model.

Delta tingkat API sama dengan [Migrasi ke Claude Fable 5.1 dari Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1): pilihan alat paksa mengembalikan error 400, dan blok thinking dipertahankan hanya untuk model yang menghasilkannya atau model yang lebih baru (Claude Mythos 5.1 membaca blok Claude Mythos 5, bukan sebaliknya). Tidak seperti Claude Fable 5.1, Claude Mythos 5.1 tidak menjalankan pemeriksaan percakapan, sehingga mengedit giliran sebelumnya tidak [membuat blok thinking tidak valid](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#fable-5-1-preserved-thinking), meskipun tetap memulai ulang cache prompt.

### Perbarui nama model Anda

```python
model = "claude-mythos-5"  # Before
model = "claude-mythos-5-1"  # After
```

### Daftar periksa migrasi

* Perbarui nama model dari `claude-mythos-5` menjadi `claude-mythos-5-1`.
* Ganti `tool_choice` paksa (`any` atau `tool`) dengan `auto` ditambah instruksi eksplisit (giliran `user` atau pesan sistem di tengah percakapan) dan alat `strict: true`, atau dengan output JSON.
* Tangani `stop_reason: "refusal"` dan baca `stop_details.category` sebelum konten respons. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Terus kirimkan kembali blok `thinking` tanpa perubahan pada setiap giliran, termasuk yang kosong.
* Jika kode Anda membangun array `messages` sendiri, jaga riwayat percakapan agar hanya-tambah untuk menjaga cache prompt tetap hangat. Claude Mythos 5.1 tidak menjalankan [pemeriksaan percakapan](https://platform.claude.com/docs/id/build-with-claude/thinking#preserved-in-conversation), sehingga pengeditan tidak membuat blok thinking-nya tidak valid.
* Terapkan perubahan perilaku dan perubahan yang direkomendasikan dari [bagian Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5-1/migration-guide#migrating-from-claude-fable-5-to-claude-fable-5-1), kecuali item pengeditan riwayat, yang tidak berlaku untuk Claude Mythos 5.1.
* Evaluasi ulang `effort` dengan sapuan baru dan tetapkan ulang baseline biaya dan latensi. Pembacaan cache prompt berbiaya seperempat dari tarif Claude Mythos 5.
