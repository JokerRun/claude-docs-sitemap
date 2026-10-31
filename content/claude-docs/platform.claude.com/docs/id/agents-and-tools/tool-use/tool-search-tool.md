---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 075e4b3a254e53f381e75b7f97c42d71efd58d78acf4aacd3e525cbe1156cea2
---

---
title: Alat pencarian alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
description: Skalakan hingga ratusan atau ribuan alat dengan membiarkan Claude mencari katalog alat Anda dan memuat hanya alat yang dibutuhkannya.
featureMetadata:
  status: stable
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Alat sisi server yang dijalankan oleh Anthropic; definisi alat dalam permintaan dicari di memori per panggilan dan tidak ada yang disimpan setelah respons.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: stable
    Claude Platform on AWS: stable
    Amazon Bedrock: stable
    Amazon Bedrock (InvokeModel):
      availability: stable
      note: Di Amazon Bedrock, alat ini tidak tersedia melalui Converse API.
    Claude Models on Google Cloud (Google managed): stable
    Microsoft Foundry: stable
---

Alat pencarian alat (tool search tool) memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuatnya sesuai permintaan. Alih-alih memuat semua definisi alat ke dalam “context window” (jendela konteks) di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan hanya memuat alat yang dibutuhkannya.

Memuat setiap definisi alat di awal menimbulkan dua masalah seiring bertambahnya pustaka alat:

* **Pembengkakan konteks:** Penyiapan multiserver yang umum (GitHub, Slack, Sentry, Grafana, dan Splunk) dapat menghabiskan \~55k token untuk definisi sebelum Claude melakukan pekerjaan apa pun. Pencarian alat biasanya mengurangi ini lebih dari 85 persen, dengan hanya memuat 3–5 alat yang dibutuhkan Claude untuk permintaan tertentu.
* **Akurasi pemilihan alat:** Kemampuan Claude untuk memilih alat yang tepat menurun setelah Anda melebihi 30–50 alat yang tersedia. Karena pencarian alat hanya memuat sekumpulan alat relevan yang terfokus sesuai permintaan, akurasi pemilihan tetap tinggi bahkan di antara ribuan alat.

Untuk model yang mendukung pencarian alat, lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#model-compatibility).

<Tip>
  Untuk latar belakang tentang tantangan penskalaan yang diselesaikan oleh pencarian alat, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai permintaan pada pencarian alat juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Pencarian alat berjalan sebagai alat sisi server, tetapi Anda juga dapat mengimplementasikan pencarian alat sisi klien Anda sendiri. Lihat [Implementasi pencarian alat kustom](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#custom-tool-search-implementation) untuk detailnya.

<Note>
  Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA).
</Note>

<Warning>
  Di Amazon Bedrock, pencarian alat sisi server hanya tersedia melalui [InvokeModel API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html), bukan Converse API.
</Warning>

<Note>
  Di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), pencarian alat sisi server bekerja identik dengan Claude API. Claude Platform on AWS menggunakan Anthropic Messages API secara langsung, sehingga tidak ada perbedaan antara InvokeModel atau Converse.
</Note>

## Kompatibilitas model

Kedua varian pencarian alat tersedia pada model berikut:

| Model                                                                                                                                        | Versi alat                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Claude Fable 5.1 (claude-fable-5-1)                                                                                                          | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Mythos 5.1 (claude-mythos-5-1)                                                                                                        | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Fable 5 (claude-fable-5)                                                                                                              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Mythos 5 (claude-mythos-5)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 5.5 (claude-opus-5-5)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 5 (claude-opus-5)                                                                                                                | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 5.5 (claude-sonnet-5-5)                                                                                                        | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 5 (claude-sonnet-5)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Haiku 5.5 (claude-haiku-5-5)                                                                                                          | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.8 (claude-opus-4-8)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.7 (claude-opus-4-7)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.6 (claude-opus-4-6)                                                                                                            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.6 (claude-sonnet-4-6)                                                                                                        | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.5 (claude-opus-4-5-20251101)                                                                                                   | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) ([tidak digunakan lagi](https://platform.claude.com/docs/id/about-claude/model-deprecations)) | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001)                                                                                                 | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |

Claude Opus 4.1 dan model yang lebih lama tidak mendukung alat pencarian alat.

## Cara kerja pencarian alat

Ada dua varian pencarian alat:

* **Regex** (`tool_search_tool_regex_20251119`): Claude menyusun pola regex untuk mencari alat.
* **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat.

Saat Anda mengaktifkan alat pencarian alat:

1. Anda menyertakan alat pencarian alat (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar `tools` Anda.
2. Anda menyediakan setiap definisi alat dalam array `tools` dan mengatur `defer_loading: true` pada alat yang tidak boleh dimuat di awal. Setidaknya satu alat, biasanya alat pencarian alat itu sendiri, harus tetap tidak ditangguhkan.
3. Awalnya, konteks Claude hanya berisi alat pencarian alat dan alat apa pun yang tidak ditangguhkan.
4. Ketika Claude membutuhkan alat tambahan, Claude mencarinya menggunakan alat pencarian alat.
5. API menjalankan pencarian dan mengembalikan alat yang cocok sebagai blok `tool_reference` (hingga 5 secara default, meskipun Claude dapat mengatur `limit` dalam input pencariannya).
6. API secara otomatis memperluas referensi ini menjadi definisi alat lengkap.
7. Claude memilih dari alat yang ditemukan dan memanggilnya.

## Mulai cepat

Contoh berikut menyertakan alat pencarian alat dan dua alat yang ditangguhkan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 2048,
      "messages": [
        {
          "role": "user",
          "content": "What is the weather in San Francisco?"
        }
      ],
      "tools": [
        {
          "type": "tool_search_tool_regex_20251119",
          "name": "tool_search_tool_regex"
        },
        {
          "name": "get_weather",
          "description": "Get the weather at a specific location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string"},
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
              }
            },
            "required": ["location"]
          },
          "defer_loading": true
        },
        {
          "name": "search_files",
          "description": "Search through files in the workspace",
          "input_schema": {
            "type": "object",
            "properties": {
              "query": {"type": "string"},
              "file_types": {
                "type": "array",
                "items": {"type": "string"}
              }
            },
            "required": ["query"]
          },
          "defer_loading": true
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 2048
  messages:
    - role: user
      content: What is the weather in San Francisco?
  tools:
    - type: tool_search_tool_regex_20251119
      name: tool_search_tool_regex
    - name: get_weather
      description: Get the weather at a specific location
      input_schema:
        type: object
        properties:
          location:
            type: string
          unit:
            type: string
            enum: [celsius, fahrenheit]
        required: [location]
      defer_loading: true
    - name: search_files
      description: Search through files in the workspace
      input_schema:
        type: object
        properties:
          query:
            type: string
          file_types:
            type: array
            items:
              type: string
        required: [query]
      defer_loading: true
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=2048,
      messages=[{"role": "user", "content": "What is the weather in San Francisco?"}],
      tools=[
          {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
          {
              "name": "get_weather",
              "description": "Get the weather at a specific location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {"type": "string"},
                      "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                  },
                  "required": ["location"],
              },
              "defer_loading": True,
          },
          {
              "name": "search_files",
              "description": "Search through files in the workspace",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "query": {"type": "string"},
                      "file_types": {"type": "array", "items": {"type": "string"}},
                  },
                  "required": ["query"],
              },
              "defer_loading": True,
          },
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "What is the weather in San Francisco?"
      }
    ],
    tools: [
      {
        type: "tool_search_tool_regex_20251119",
        name: "tool_search_tool_regex"
      },
      {
        name: "get_weather",
        description: "Get the weather at a specific location",
        input_schema: {
          type: "object" as const,
          properties: {
            location: { type: "string" },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"]
        },
        defer_loading: true
      },
      {
        name: "search_files",
        description: "Search through files in the workspace",
        input_schema: {
          type: "object" as const,
          properties: {
            query: { type: "string" },
            file_types: {
              type: "array",
              items: { type: "string" }
            }
          },
          required: ["query"]
        },
        defer_loading: true
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 2048,
      Messages = [new UserMessageParam { Content = "What is the weather in San Francisco?" }],
      Tools = [
          new ToolUnion(new ToolSearchToolRegex20251119
          {
              Type = ToolSearchToolRegex20251119Type.ToolSearchToolRegex20251119
          }),
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the weather at a specific location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                      ["unit"] = JsonSerializer.SerializeToElement(new { type = "string", @enum = new[] { "celsius", "fahrenheit" } }),
                  },
                  Required = ["location"],
              },
              DeferLoading = true,
          }),
          new ToolUnion(new Tool()
          {
              Name = "search_files",
              Description = "Search through files in the workspace",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["query"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                      ["file_types"] = JsonSerializer.SerializeToElement(new { type = "array", items = new { type = "string" } }),
                  },
                  Required = ["query"],
              },
              DeferLoading = true,
          }),
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 2048,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco?")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfToolSearchToolRegex20251119: &anthropic.ToolSearchToolRegex20251119Param{
  			Type: anthropic.ToolSearchToolRegex20251119TypeToolSearchToolRegex20251119,
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the weather at a specific location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{"type": "string"},
  					"unit": map[string]any{
  						"type": "string",
  						"enum": []string{"celsius", "fahrenheit"},
  					},
  				},
  				Required: []string{"location"},
  			},
  			DeferLoading: anthropic.Bool(true),
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "search_files",
  			Description: anthropic.String("Search through files in the workspace"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"query":      map[string]any{"type": "string"},
  					"file_types": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
  				},
  				Required: []string{"query"},
  			},
  			DeferLoading: anthropic.Bool(true),
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.ToolSearchToolRegex20251119;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      InputSchema weatherSchema = InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "location", Map.of("type", "string"),
              "unit", Map.of(
                  "type", "string",
                  "enum", List.of("celsius", "fahrenheit")
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("location")))
          .build();

      InputSchema searchSchema = InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "query", Map.of("type", "string"),
              "file_types", Map.of(
                  "type", "array",
                  "items", Map.of("type", "string")
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("query")))
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(2048L)
          .addUserMessage("What is the weather in San Francisco?")
          .addTool(ToolSearchToolRegex20251119.builder()
              .type(ToolSearchToolRegex20251119.Type.TOOL_SEARCH_TOOL_REGEX_20251119)
              .build())
          .addTool(Tool.builder()
              .name("get_weather")
              .description("Get the weather at a specific location")
              .inputSchema(weatherSchema)
              .deferLoading(true)
              .build())
          .addTool(Tool.builder()
              .name("search_files")
              .description("Search through files in the workspace")
              .inputSchema(searchSchema)
              .deferLoading(true)
              .build())
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 2048,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather in San Francisco?'],
      ],
      model: Model::CLAUDE_OPUS_5_5,
      tools: [
          [
              'type' => 'tool_search_tool_regex_20251119',
              'name' => 'tool_search_tool_regex',
          ],
          [
              'name' => 'get_weather',
              'description' => 'Get the weather at a specific location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => ['type' => 'string'],
                      'unit' => [
                          'type' => 'string',
                          'enum' => ['celsius', 'fahrenheit'],
                      ],
                  ],
                  'required' => ['location'],
              ],
              'defer_loading' => true,
          ],
          [
              'name' => 'search_files',
              'description' => 'Search through files in the workspace',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'query' => ['type' => 'string'],
                      'file_types' => [
                          'type' => 'array',
                          'items' => ['type' => 'string'],
                      ],
                  ],
                  'required' => ['query'],
              ],
              'defer_loading' => true,
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 2048,
    messages: [
      { role: "user", content: "What is the weather in San Francisco?" }
    ],
    tools: [
      {
        type: "tool_search_tool_regex_20251119",
        name: "tool_search_tool_regex"
      },
      {
        name: "get_weather",
        description: "Get the weather at a specific location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string" },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"]
        },
        defer_loading: true
      },
      {
        name: "search_files",
        description: "Search through files in the workspace",
        input_schema: {
          type: "object",
          properties: {
            query: { type: "string" },
            file_types: {
              type: "array",
              items: { type: "string" }
            }
          },
          required: ["query"]
        },
        defer_loading: true
      }
    ]
  )

  puts message
  ```
</CodeGroup>

Claude mencari katalog, menemukan `get_weather`, dan memanggilnya. Respons diakhiri dengan `stop_reason: "tool_use"`. Jalankan alat yang ditemukan dan kembalikan `tool_result` seperti dalam [Menangani panggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls). [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#response-format) menunjukkan blok yang Anda terima kembali dan apa yang harus dikirim selanjutnya.

## Definisi alat

Alat pencarian alat memiliki dua varian:

```json JSON
{
  "type": "tool_search_tool_regex_20251119",
  "name": "tool_search_tool_regex"
}
```

```json JSON
{
  "type": "tool_search_tool_bm25_20251119",
  "name": "tool_search_tool_bm25"
}
```

<Warning>
  **Format kueri varian regex: regex Python, bukan bahasa alami**

  Dengan `tool_search_tool_regex_20251119`, Claude menulis pola `re.search()` Python, bukan kueri bahasa alami. Pencocokan tidak peka huruf besar/kecil. Pola umum mencakup hal berikut:

  * `"weather"`: mencocokkan nama alat dan deskripsi yang mengandung “weather”
  * `"get_.*_data"`: mencocokkan alat seperti `get_user_data` dan `get_weather_data`
  * `"database.*query|query.*database"`: mencocokkan kedua urutan kata

  Panjang pola maksimum: 200 karakter
</Warning>

<Note>
  **Format kueri varian BM25: bahasa alami**

  Dengan `tool_search_tool_bm25_20251119`, Claude mencari dengan kueri bahasa alami. Panjang kueri maksimum: 500 karakter.
</Note>

### Pemuatan alat yang ditangguhkan

Tandai alat untuk pemuatan sesuai permintaan dengan menambahkan `defer_loading: true`:

```json JSON
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" },
      "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["location"]
  },
  "defer_loading": true
}
```

`defer_loading` mengontrol apa yang masuk ke jendela konteks, bukan apa yang Anda kirim dalam permintaan:

* Anda tetap mengirim definisi lengkap setiap alat dalam array `tools` pada setiap permintaan, termasuk yang ditangguhkan. API membutuhkannya di sisi server untuk menjalankan pencarian dan memperluas blok `tool_reference`.
* Alat tanpa `defer_loading` langsung dimuat ke dalam konteks.
* Alat dengan `defer_loading: true` hanya dimuat ketika Claude menemukannya melalui pencarian.
* Jangan pernah mengatur `defer_loading: true` pada alat pencarian alat itu sendiri.
* Pertahankan 3–5 alat yang paling sering Anda gunakan agar tidak ditangguhkan sehingga Claude dapat memanggilnya tanpa mencari terlebih dahulu.

Toolset penggunaan komputer dan browser use (`computer_toolset_20260801` dan `browser_toolset_20260801`) menerima `defer_loading` untuk setiap alat anggota di dalam objek `configs` milik entri, bukan pada entri itu sendiri; permintaan yang mengaturnya di tingkat entri akan ditolak. Karena toolset ditangguhkan dan diperluas sebagai satu kesatuan, `defer_loading` harus bernilai sama pada setiap anggota yang diaktifkan, dan ketika Claude menemukan toolset melalui pencarian, setiap anggota yang diaktifkan dimuat sekaligus. Lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) untuk format `configs`.

Kedua varian pencarian alat (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

Secara internal, API mengecualikan alat yang ditangguhkan dari prefiks prompt sistem. Ketika Claude menemukan alat yang ditangguhkan melalui pencarian alat, API menambahkan blok `tool_reference` secara inline dalam percakapan, lalu memperluasnya menjadi definisi alat lengkap sebelum meneruskannya ke Claude. Prefiks tidak tersentuh, sehingga “prompt caching” (caching prompt) tetap terjaga. Grammar untuk [mode strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) (aturan yang membatasi output panggilan alat agar sesuai dengan skema Anda) dibangun dari toolset lengkap, sehingga `defer_loading` dan mode strict dapat digabungkan tanpa kompilasi ulang grammar.

## Format respons

Ketika Claude menggunakan alat pencarian alat, respons menyertakan jenis blok berikut:

```json JSON
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll search for tools to help with the weather information."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01ABC123",
      "name": "tool_search_tool_regex",
      "input": {
        "pattern": "weather",
        "limit": 10
      }
    },
    {
      "type": "tool_search_tool_result",
      "tool_use_id": "srvtoolu_01ABC123",
      "content": {
        "type": "tool_search_tool_search_result",
        "tool_references": [{ "type": "tool_reference", "tool_name": "get_weather" }]
      }
    },
    {
      "type": "text",
      "text": "I found a weather tool. Let me get the weather for San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01XYZ789",
      "name": "get_weather",
      "input": { "location": "San Francisco", "unit": "fahrenheit" }
    }
  ],
  "stop_reason": "tool_use"
}
```

### Memahami respons

* **`server_tool_use`:** panggilan Claude ke alat pencarian alat. Pencarian berjalan di server Anthropic. Jangan pernah mengembalikan `tool_result` untuk ID `srvtoolu_...`-nya. `input` berisi pencarian (`pattern` untuk varian regex, `query` untuk BM25) dan mungkin menyertakan `limit` opsional, bilangan bulat dari 1 hingga 10.000 yang membatasi berapa banyak alat yang cocok yang dikembalikan pencarian (default: 5).
* **`tool_search_tool_result`:** hasil pencarian, dalam objek `tool_search_tool_search_result` bertingkat. Simpan dalam riwayat pesan apa adanya.
* **`tool_references`:** array objek `tool_reference` yang menunjuk ke alat yang ditemukan. API memperluas ini untuk Claude. Anda tidak pernah memperluasnya sendiri.
* **`tool_use`:** panggilan Claude ke alat yang ditemukan. Jalankan dan kembalikan `tool_result` persis seperti dalam “tool use” (penggunaan alat) standar.

API secara otomatis memperluas blok `tool_reference` menjadi definisi alat lengkap sebelum menampilkannya kepada Claude. Anda tidak perlu menangani perluasan ini sendiri, selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

### Melanjutkan percakapan

Pada permintaan berikutnya, kirimkan kembali konten asisten tanpa perubahan, termasuk blok `server_tool_use` dan `tool_search_tool_result`. Tambahkan `tool_result` Anda untuk alat yang ditemukan dalam pesan pengguna, dan kirim array `tools` yang sama: alat pencarian ditambah setiap definisi yang ditangguhkan. Jangan mengembalikan `tool_result` untuk ID `srvtoolu_...`: API akan menolak permintaan tersebut. API memperluas blok `tool_reference` di seluruh riwayat percakapan, sehingga Claude dapat menggunakan kembali alat yang ditemukan pada giliran berikutnya tanpa mencari ulang. Pencarian yang tidak mencocokkan apa pun mengembalikan `tool_search_tool_search_result` dengan array `tool_references` kosong, bukan error.

## Integrasi MCP

Jika alat Anda berasal dari server MCP melalui [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), Anda tidak mengatur `defer_loading` pada definisi alat individual. Sebagai gantinya, atur sekali pada `default_config` milik entri `mcp_toolset` untuk seluruh server, atau per alat dalam `configs`-nya. Lihat [Konfigurasi toolset MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration).

## Implementasi pencarian alat kustom

Anda dapat mengimplementasikan logika pencarian alat Anda sendiri (misalnya, menggunakan embedding atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat kustom. Ketika Claude memanggil alat pencarian kustom Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas, biasanya dengan `defer_loading: true`. Ini memungkinkan Anda menggunakan metode pencarian yang tidak disediakan oleh varian bawaan, seperti pengambilan berbasis embedding, dan API memperluas blok `tool_reference` yang dikembalikan dengan cara yang sama.

<Note>
  Format `tool_search_tool_result` yang ditampilkan di bagian [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#response-format) adalah format sisi server yang digunakan secara internal oleh pencarian alat bawaan Anthropic. Untuk implementasi sisi klien kustom, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan pada contoh sebelumnya.
</Note>

Untuk contoh lengkap menggunakan embedding, lihat resep [pencarian alat dengan embedding](https://platform.claude.com/cookbook/tool-use-tool-search-with-embeddings).

## Penanganan error

<Note>
  [Contoh penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples) bekerja dengan pencarian alat: ketika Claude menemukan alat yang ditangguhkan, API memperluas `input_examples`-nya bersama dengan definisinya.
</Note>

### Error HTTP (status 400)

Error ini mencegah API memproses permintaan:

**Semua alat ditangguhkan:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "At least one tool must have defer_loading=false. All tools cannot be deferred."
  }
}
```

**Definisi alat tidak ada:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Tool reference 'unknown_tool' not found in available tools"
  }
}
```

### Error hasil alat (status 200)

Ketika operasi pencarian alat gagal selama eksekusi, API mengembalikan respons 200 dengan error di dalam body:

```json JSON
{
  "type": "tool_search_tool_result",
  "tool_use_id": "srvtoolu_01ABC123",
  "content": {
    "type": "tool_search_tool_result_error",
    "error_code": "invalid_tool_input",
    "error_message": "Invalid regular expression pattern: missing ) at position 1"
  }
}
```

API mendefinisikan nilai `error_code` berikut:

* `invalid_tool_input`: input pencarian tidak valid, misalnya pola regex yang salah format atau pola yang melebihi batas 200 karakter
* `unavailable`: pencarian tidak dapat dijalankan, misalnya karena waktu habis atau layanan tidak tersedia
* `too_many_requests`: “rate limit” (batas laju) terlampaui untuk operasi pencarian alat
* `execution_time_exceeded`: tidak dikembalikan oleh pencarian alat, yang melaporkan waktu habis sebagai `unavailable`

### Kesalahan umum

<Accordion title="Error 400: semua alat ditangguhkan">
  **Penyebab:** Anda mengatur `defer_loading: true` pada setiap alat, termasuk alat pencarian alat.

  **Perbaikan:** Hapus `defer_loading` dari alat pencarian alat:

  ```json
  {
    "type": "tool_search_tool_regex_20251119",
    "name": "tool_search_tool_regex"
  }
  ```
</Accordion>

<Accordion title="Error 400: definisi alat tidak ada">
  **Penyebab:** Sebuah `tool_reference` menunjuk ke alat yang tidak ada dalam array `tools` Anda.

  **Perbaikan:** Pastikan setiap alat yang dapat ditemukan memiliki definisi lengkap:

  ```json
  {
    "name": "my_tool",
    "description": "Full description here",
    "input_schema": {
      "type": "object"
    },
    "defer_loading": true
  }
  ```
</Accordion>

<Accordion title="Claude tidak menemukan alat yang diharapkan">
  **Penyebab:** Pola regex tidak cocok dengan nama alat, deskripsi, nama argumen, atau deskripsi argumen.

  **Langkah debugging:**

  1. Periksa nama alat, deskripsi, nama argumen, dan deskripsi argumen. Claude mencari semua field ini.
  2. Uji pola Anda: `import re; re.search(r"your_pattern", "tool_name", re.IGNORECASE)`.
  3. Pencocokan tidak peka huruf besar/kecil, jadi perbedaan huruf besar/kecil bukan masalahnya.
  4. Claude menggunakan pola luas seperti `".*weather.*"`, bukan kecocokan persis.

  **Tip:** Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemudahan penemuan.
</Accordion>

## Caching prompt

Untuk mempelajari bagaimana `defer_loading` mempertahankan caching prompt, lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

Alat dengan `defer_loading: true` tidak dapat sekaligus membawa `cache_control`: API mengembalikan 400. Letakkan cache breakpoint pada alat yang tidak ditangguhkan.

## Streaming

Dengan streaming diaktifkan, Anda akan menerima event pencarian alat sebagai bagian dari stream:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "tool_search_tool_regex"}}

// Search pattern streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"pattern\":\"weather\"}"}}

// Pause while search runs

// Search results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "tool_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "tool_search_tool_search_result", "tool_references": [{"type": "tool_reference", "tool_name": "get_weather"}]}}}

// Claude continues with discovered tools
```

## Permintaan batch

Anda dapat menyertakan alat pencarian alat dalam [Messages Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing).

## Batasan dan praktik terbaik

### Batasan

* **Maksimum alat yang ditangguhkan:** 10.000 alat dengan `defer_loading: true` untuk setiap permintaan
* **Hasil pencarian:** setiap pencarian mengembalikan hingga 5 alat yang cocok secara default; Claude dapat mengatur `limit` dalam input pencariannya ke bilangan bulat apa pun dari 1 hingga 10.000
* **Panjang pola dan kueri:** maksimum 200 karakter untuk pola regex dan 500 karakter untuk kueri BM25
* **Dukungan model:** lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#model-compatibility)

### Kapan menggunakan pencarian alat

Gunakan pencarian alat ketika salah satu dari hal berikut berlaku:

* Anda memiliki 10 alat atau lebih yang tersedia.
* Definisi alat Anda menghabiskan lebih dari 10k token.
* Akurasi pemilihan alat menurun seiring bertambahnya toolset Anda.
* Anda menggabungkan beberapa server MCP (200+ alat).
* Pustaka alat Anda bertambah seiring waktu.

Pemanggilan alat standar, tanpa pencarian alat, lebih cocok ketika Anda memiliki kurang dari 10 alat, setiap alat digunakan dalam setiap permintaan, atau definisi alat Anda kecil (total kurang dari 100 token).

### Tips optimasi

* Pertahankan 3–5 alat yang paling sering Anda gunakan agar tidak ditangguhkan.
* Tulis nama dan deskripsi alat yang jelas dan deskriptif.
* Gunakan namespacing yang konsisten dalam nama alat: beri prefiks berdasarkan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga satu pencarian mencocokkan seluruh grup.
* Gunakan kata kunci dalam deskripsi yang sesuai dengan cara pengguna mendeskripsikan tugas.
* Tambahkan bagian “system prompt” (prompt sistem) yang menjelaskan kategori alat yang tersedia: “You can search for tools to interact with Slack, GitHub, and Jira.”
* Pantau alat mana yang ditemukan Claude untuk menyempurnakan deskripsi Anda.

## Penggunaan

Pencarian alat tidak diukur sebagai alat server terpisah. Objek `usage.server_tool_use` dalam respons tidak memiliki field pencarian alat, dan definisi alat yang dimuat pencarian ke dalam konteks dihitung sebagai token input seperti definisi alat lainnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat memori" icon="brain" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool">
    Biarkan Claude menyimpan dan mengambil informasi di seluruh percakapan dengan mengimplementasikan operasi file alat memori di aplikasi Anda.
  </Card>

  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>

  <Card title="Konektor MCP" icon="link" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-connector">
    Konfigurasikan toolset MCP dengan pemuatan yang ditangguhkan.
  </Card>

  <Card title="Penggunaan alat dengan caching prompt" icon="bolt" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.
  </Card>

  <Card title="Mendefinisikan alat" icon="hammer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>

## Ketersediaan

Alat pencarian alat tersedia di semua model dan layak untuk retensi data nol.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status               | Platform cloud                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Model                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Tersedia             | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Semua model](https://platform.claude.com/docs/id/models/overview) |
| Tersedia<sup>1</sup> | [Amazon Bedrock (InvokeModel)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)                                                                                                                                                                                                                                                                                                                                                              | [Semua model](https://platform.claude.com/docs/id/models/overview) |

1. Di Amazon Bedrock, alat ini tidak tersedia melalui Converse API.

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tidak tersedia

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                 | HIPAA       |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements)) | Tidak layak |
| Detail | Alat sisi server yang dijalankan oleh Anthropic; definisi alat dalam permintaan dicari di memori per panggilan dan tidak ada yang disimpan setelah respons.      | —           |

Endpoint yang berlaku:

* `/v1/messages` dengan alat `tool_search`
