---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 1f2df128aa9a452be0a14c215813a7ca235b8230fcebf338ef32ccb4fb86a0da
---

---
title: Tool search tool
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
description: Skalakan hingga ratusan atau ribuan alat dengan membiarkan Claude mencari katalog alat Anda dan memuat hanya alat yang dibutuhkannya.
---

Tool search tool memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuatnya sesuai permintaan. Alih-alih memuat semua definisi alat ke dalam jendela konteks di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan memuat hanya alat yang dibutuhkannya.

Memuat setiap definisi alat di awal menyebabkan dua masalah seiring bertumbuhnya pustaka alat:

* **Pembengkakan konteks:** Pengaturan multiserver yang umum (GitHub, Slack, Sentry, Grafana, dan Splunk) dapat mengonsumsi \~55k token dalam definisi sebelum Claude melakukan pekerjaan apa pun. Tool search biasanya mengurangi ini lebih dari 85 persen, memuat hanya 3–5 alat yang dibutuhkan Claude untuk permintaan tertentu.
* **Akurasi pemilihan alat:** Kemampuan Claude untuk memilih alat yang tepat menurun setelah Anda melampaui 30–50 alat yang tersedia. Karena tool search memuat hanya sekumpulan alat relevan yang terfokus sesuai permintaan, akurasi pemilihan tetap tinggi bahkan di seluruh ribuan alat.

Untuk model yang mendukung tool search, lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#model-compatibility).

<Tip>
  Untuk latar belakang tentang tantangan penskalaan yang dipecahkan oleh tool search, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai permintaan dari tool search juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Tool search berjalan sebagai alat sisi server, tetapi Anda juga dapat mengimplementasikan tool search sisi klien Anda sendiri. Lihat [Implementasi tool search kustom](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#custom-tool-search-implementation) untuk detailnya.

<Note>
  Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA).
</Note>

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

<Warning>
  Di Amazon Bedrock, tool search sisi server hanya tersedia melalui [InvokeModel API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html), bukan Converse API.
</Warning>

<Note>
  Di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), tool search sisi server bekerja secara identik dengan Claude API. Claude Platform on AWS menggunakan Anthropic Messages API secara langsung, sehingga tidak ada perbedaan InvokeModel atau Converse.
</Note>

## Model compatibility

Kedua varian tool search tersedia pada model berikut:

| Model                                          | Versi alat                                                          |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| Claude Fable 5.1 (claude-fable-5-1)            | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Mythos 5.1 (claude-mythos-5-1)          | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Fable 5 (claude-fable-5)                | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Mythos 5 (claude-mythos-5)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 5 (claude-opus-5)                  | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.8 (claude-opus-4-8)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.7 (claude-opus-4-7)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.6 (claude-opus-4-6)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.6 (claude-sonnet-4-6)          | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.5 (claude-opus-4-5-20251101)     | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001)   | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |

Claude Opus 4.1 dan model sebelumnya tidak mendukung tool search tool.

## How tool search works

Ada dua varian tool search:

* **Regex** (`tool_search_tool_regex_20251119`): Claude membangun pola regex untuk mencari alat.
* **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat.

Ketika Anda mengaktifkan tool search tool:

1. Anda menyertakan tool search tool (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar `tools` Anda.
2. Anda menyediakan setiap definisi alat dalam array `tools` dan mengatur `defer_loading: true` pada alat yang tidak boleh dimuat di awal. Setidaknya satu alat, biasanya tool search tool itu sendiri, harus tetap non-deferred.
3. Awalnya, konteks Claude hanya berisi tool search tool dan alat non-deferred apa pun.
4. Ketika Claude membutuhkan alat tambahan, ia mencari menggunakan tool search tool.
5. API menjalankan pencarian dan mengembalikan alat yang cocok sebagai blok `tool_reference` (hingga 5 secara default; Claude dapat mengatur `limit` dalam input pencariannya).
6. API secara otomatis memperluas referensi ini menjadi definisi alat lengkap.
7. Claude memilih dari alat yang ditemukan dan memanggilnya.

## Quick start

Contoh berikut menyertakan tool search tool dan dua alat deferred:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d '{
          "model": "claude-opus-5",
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
  model: claude-opus-5
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
      model="claude-opus-5",
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
    model: "claude-opus-5",
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
      Model = Model.ClaudeOpus5,
      MaxTokens = 2048,
      Messages = [
          new() {
              Role = Role.User,
              Content = "What is the weather in San Francisco?"
          }
      ],
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
  	Model:     anthropic.ModelClaudeOpus5,
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
          .model(Model.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
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
    model: "claude-opus-5",
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

Claude mencari katalog, menemukan `get_weather`, dan memanggilnya. Respons berakhir dengan `stop_reason: "tool_use"`. Jalankan alat yang ditemukan dan kembalikan `tool_result` seperti dalam [Menangani panggilan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls). [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#response-format) menunjukkan blok yang Anda dapatkan kembali dan apa yang harus dikirim selanjutnya.

## Tool definition

Tool search tool memiliki dua varian:

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

  Dengan `tool_search_tool_regex_20251119`, Claude menulis pola `re.search()` Python, bukan kueri bahasa alami. Pencocokan tidak peka huruf besar-kecil. Pola umum meliputi berikut ini:

  * `"weather"`: cocok dengan nama alat dan deskripsi yang mengandung "weather"
  * `"get_.*_data"`: cocok dengan alat seperti `get_user_data` dan `get_weather_data`
  * `"database.*query|query.*database"`: cocok dengan urutan kata mana pun

  Panjang pola maksimum: 200 karakter
</Warning>

<Note>
  **Format kueri varian BM25: bahasa alami**

  Dengan `tool_search_tool_bm25_20251119`, Claude mencari dengan kueri bahasa alami. Panjang kueri maksimum: 500 karakter.
</Note>

### Deferred tool loading

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

* Anda tetap mengirim definisi lengkap setiap alat dalam array `tools` pada setiap permintaan, termasuk yang deferred. API membutuhkannya di sisi server untuk menjalankan pencarian dan memperluas blok `tool_reference`.
* Alat tanpa `defer_loading` dimuat ke dalam konteks segera.
* Alat dengan `defer_loading: true` dimuat hanya ketika Claude menemukannya melalui pencarian.
* Jangan pernah mengatur `defer_loading: true` pada tool search tool itu sendiri.
* Jaga agar 3–5 alat yang paling sering digunakan tetap non-deferred sehingga Claude dapat memanggilnya tanpa mencari terlebih dahulu.

Toolset computer use dan browser use (`computer_toolset_20260801` dan `browser_toolset_20260801`) mengambil `defer_loading` per alat anggota di dalam objek `configs` entri, bukan pada entri itu sendiri; permintaan yang mengaturnya di tingkat entri akan ditolak. Karena toolset menunda dan memperluas sebagai satu unit, `defer_loading` harus menghasilkan nilai yang sama pada setiap anggota yang diaktifkan, dan ketika Claude menemukan toolset melalui pencarian, setiap anggota yang diaktifkan dimuat sekaligus. Lihat [Client toolsets](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) untuk format `configs`.

Kedua varian tool search (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

Secara internal, API mengecualikan alat deferred dari prefiks prompt sistem. Ketika Claude menemukan alat deferred melalui tool search, API menambahkan blok `tool_reference` secara inline dalam percakapan, lalu memperluasnya menjadi definisi alat lengkap sebelum meneruskannya ke Claude. Prefiks tidak tersentuh, sehingga caching prompt dipertahankan. Tata bahasa untuk [mode ketat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) (aturan yang membatasi output panggilan alat agar cocok dengan skema Anda) dibangun dari toolset lengkap, sehingga `defer_loading` dan mode ketat disusun tanpa kompilasi ulang tata bahasa.

## Response format

Ketika Claude menggunakan tool search tool, respons menyertakan jenis blok berikut:

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

### Understanding the response

* **`server_tool_use`:** Panggilan Claude ke tool search tool. Pencarian berjalan di server Anthropic. Jangan pernah mengembalikan `tool_result` untuk ID `srvtoolu_...`-nya. `input` menyimpan pencarian (`pattern` untuk varian regex, `query` untuk BM25) dan dapat menyertakan `limit` opsional, sebuah integer dari 1 hingga 10.000 yang membatasi berapa banyak alat yang cocok yang dikembalikan pencarian (default: 5).
* **`tool_search_tool_result`:** hasil pencarian, dalam objek `tool_search_tool_search_result` bersarang. Simpan apa adanya dalam riwayat pesan.
* **`tool_references`:** sebuah array objek `tool_reference` yang menunjuk ke alat yang ditemukan. API memperluasnya untuk Claude. Anda tidak pernah memperluasnya sendiri.
* **`tool_use`:** Panggilan Claude ke alat yang ditemukan. Jalankan dan kembalikan `tool_result` persis seperti dalam penggunaan alat standar.

API secara otomatis memperluas blok `tool_reference` menjadi definisi alat lengkap sebelum menampilkannya ke Claude. Anda tidak perlu menangani perluasan ini sendiri, selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

### Continuing the conversation

Pada permintaan berikutnya, teruskan konten asisten kembali tanpa perubahan, termasuk blok `server_tool_use` dan `tool_search_tool_result`. Tambahkan `tool_result` Anda untuk alat yang ditemukan dalam pesan pengguna, dan kirim array `tools` yang sama: alat pencarian ditambah setiap definisi deferred. Jangan mengembalikan `tool_result` untuk ID `srvtoolu_...`: API menolak permintaan tersebut. API memperluas blok `tool_reference` di seluruh riwayat percakapan, sehingga Claude dapat menggunakan kembali alat yang ditemukan di giliran berikutnya tanpa mencari ulang. Pencarian yang tidak cocok dengan apa pun mengembalikan `tool_search_tool_search_result` dengan array `tool_references` kosong, bukan kesalahan.

## MCP integration

Jika alat Anda berasal dari server MCP melalui [MCP connector](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), Anda tidak mengatur `defer_loading` pada definisi alat individual. Sebaliknya, atur sekali pada `default_config` entri `mcp_toolset` untuk seluruh server, atau per alat dalam `configs`-nya. Lihat [Konfigurasi MCP toolset](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration).

## Custom tool search implementation

Anda dapat mengimplementasikan logika tool search Anda sendiri (misalnya, menggunakan embedding atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat kustom. Ketika Claude memanggil alat pencarian kustom Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas, biasanya dengan `defer_loading: true`. Ini memungkinkan Anda menggunakan metode pencarian yang tidak disediakan oleh varian bawaan, seperti pengambilan berbasis embedding, dan API memperluas blok `tool_reference` yang dikembalikan dengan cara yang sama.

<Note>
  Format `tool_search_tool_result` yang ditunjukkan di bagian [Format respons](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#response-format) adalah format sisi server yang digunakan secara internal oleh tool search bawaan Anthropic. Untuk implementasi sisi klien kustom, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan dalam contoh sebelumnya.
</Note>

Untuk contoh lengkap menggunakan embedding, lihat resep [tool search with embeddings](https://platform.claude.com/cookbook/tool-use-tool-search-with-embeddings).

## Error handling

<Note>
  [Contoh penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples) bekerja dengan tool search: ketika Claude menemukan alat deferred, API memperluas `input_examples`-nya bersama dengan definisinya.
</Note>

### HTTP errors (400 status)

Kesalahan ini mencegah API memproses permintaan:

**Semua alat deferred:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "At least one tool must have defer_loading=false. All tools cannot be deferred."
  }
}
```

**Definisi alat hilang:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Tool reference 'unknown_tool' not found in available tools"
  }
}
```

### Tool result errors (200 status)

Ketika operasi tool search gagal selama eksekusi, API mengembalikan respons 200 dengan kesalahan di body:

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

Field `error_code` memiliki empat nilai yang mungkin:

* `invalid_tool_input`: input pencarian tidak valid, misalnya pola regex yang salah bentuk atau pola yang melebihi batas 200 karakter
* `unavailable`: pencarian tidak dapat berjalan, misalnya karena waktu habis atau layanan tidak tersedia
* `too_many_requests`: batas laju terlampaui untuk operasi tool search
* `execution_time_exceeded`: pencarian melampaui batas waktu eksekusinya

### Common mistakes

<Accordion title="Kesalahan 400: semua alat deferred">
  **Penyebab:** Anda mengatur `defer_loading: true` pada setiap alat, termasuk tool search tool.

  **Perbaikan:** Hapus `defer_loading` dari tool search tool:

  ```json
  {
    "type": "tool_search_tool_regex_20251119",
    "name": "tool_search_tool_regex"
  }
  ```
</Accordion>

<Accordion title="Kesalahan 400: definisi alat hilang">
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
  3. Pencocokan tidak peka huruf besar-kecil, jadi perbedaan huruf besar-kecil bukan masalahnya.
  4. Claude menggunakan pola luas seperti `".*weather.*"`, bukan pencocokan persis.

  **Tip:** Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemudahan penemuan.
</Accordion>

## Prompt caching

Untuk mempelajari bagaimana `defer_loading` mempertahankan caching prompt, lihat [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

Alat dengan `defer_loading: true` tidak dapat juga membawa `cache_control`: API mengembalikan 400. Letakkan breakpoint cache pada alat non-deferred.

## Streaming

Dengan streaming diaktifkan, Anda akan menerima event tool search sebagai bagian dari stream:

```sse
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "tool_search_tool_regex"}}

// Search pattern streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"pattern\":\"weather\"}"}}

// Pause while search executes

// Search results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "tool_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"type": "tool_search_tool_search_result", "tool_references": [{"type": "tool_reference", "tool_name": "get_weather"}]}}}

// Claude continues with discovered tools
```

## Batch requests

Anda dapat menyertakan tool search tool dalam [Messages Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing).

## Limits and best practices

### Limits

* **Alat deferred maksimum:** 10.000 alat dengan `defer_loading: true` per permintaan
* **Hasil pencarian:** setiap pencarian mengembalikan hingga 5 alat yang cocok secara default; Claude dapat mengatur `limit` dalam input pencariannya ke integer mana pun dari 1 hingga 10.000
* **Panjang pola dan kueri:** maksimum 200 karakter untuk pola regex dan 500 karakter untuk kueri BM25
* **Dukungan model:** lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool#model-compatibility)

### When to use tool search

Gunakan tool search ketika salah satu dari berikut ini berlaku:

* Anda memiliki 10 atau lebih alat yang tersedia.
* Definisi alat Anda mengonsumsi lebih dari 10k token.
* Akurasi pemilihan alat menurun seiring bertumbuhnya toolset Anda.
* Anda mengagregasi beberapa server MCP (200+ alat).
* Pustaka alat Anda bertumbuh seiring waktu.

Pemanggilan alat standar, tanpa tool search, lebih cocok ketika Anda memiliki kurang dari 10 alat, setiap alat digunakan dalam setiap permintaan, atau definisi alat Anda kecil (kurang dari 100 token total).

### Optimization tips

* Jaga agar 3–5 alat yang paling sering digunakan tetap non-deferred.
* Tulis nama dan deskripsi alat yang jelas dan deskriptif.
* Gunakan namespacing yang konsisten dalam nama alat: beri prefiks berdasarkan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga satu pencarian cocok dengan seluruh grup.
* Gunakan kata kunci dalam deskripsi yang cocok dengan cara pengguna mendeskripsikan tugas.
* Tambahkan bagian prompt sistem yang mendeskripsikan kategori alat yang tersedia: "Anda dapat mencari alat untuk berinteraksi dengan Slack, GitHub, dan Jira."
* Pantau alat mana yang ditemukan Claude untuk menyempurnakan deskripsi Anda.

## Usage

Tool search tidak diukur sebagai alat server terpisah. Objek `usage.server_tool_use` dari respons tidak memiliki field tool search, dan definisi alat yang dimuat pencarian ke dalam konteks dihitung sebagai token input seperti definisi alat lainnya.

## Next steps

<CardGroup cols={2}>
  <Card title="Memory tool" icon="brain" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool">
    Biarkan Claude menyimpan dan mengambil informasi di seluruh percakapan dengan mengimplementasikan operasi file dari memory tool di aplikasi Anda.
  </Card>

  <Card title="Tool reference" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>

  <Card title="MCP connector" icon="link" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-connector">
    Konfigurasikan MCP toolset dengan pemuatan deferred.
  </Card>

  <Card title="Tool use with prompt caching" icon="bolt" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.
  </Card>

  <Card title="Define tools" icon="hammer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
