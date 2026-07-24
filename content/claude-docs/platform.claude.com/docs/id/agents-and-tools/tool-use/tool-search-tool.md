---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 376041cb8b28dd0f30516c63d5d94ca0ca15d6f44dec412829368a425bf87ec1
---

# Tool search tool

Skalakan hingga ratusan atau ribuan alat dengan membiarkan Claude mencari katalog alat Anda dan memuat hanya alat yang dibutuhkannya.

---

Tool search tool (alat pencarian alat) memungkinkan Claude bekerja dengan ratusan atau ribuan alat dengan menemukan dan memuatnya sesuai permintaan. Alih-alih memuat semua definisi alat ke dalam jendela konteks di awal, Claude mencari katalog alat Anda (termasuk nama alat, deskripsi, nama argumen, dan deskripsi argumen) dan memuat hanya alat yang dibutuhkannya.

Memuat setiap definisi alat di awal menyebabkan dua masalah seiring bertambahnya pustaka alat:

* **Pembengkakan konteks:** Pengaturan multiserver yang umum (GitHub, Slack, Sentry, Grafana, dan Splunk) dapat mengonsumsi \~55k token dalam definisi sebelum Claude melakukan pekerjaan apa pun. Tool search biasanya mengurangi ini lebih dari 85 persen, memuat hanya 3–5 alat yang dibutuhkan Claude untuk permintaan tertentu.
* **Akurasi pemilihan alat:** Kemampuan Claude untuk memilih alat yang tepat menurun setelah Anda melebihi 30–50 alat yang tersedia. Karena tool search hanya memuat sekumpulan alat relevan yang terfokus sesuai permintaan, akurasi pemilihan tetap tinggi bahkan di antara ribuan alat.

Tool search tersedia secara umum di Claude API. Untuk model yang didukung, lihat [Kompatibilitas model](#model-compatibility).

<Tip>
  Untuk latar belakang tentang tantangan penskalaan yang diselesaikan oleh tool search, lihat [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Pemuatan sesuai permintaan dari tool search juga merupakan contoh dari prinsip pengambilan just-in-time yang lebih luas yang dijelaskan dalam [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Tool search berjalan sebagai alat sisi server, tetapi Anda juga dapat mengimplementasikan tool search sisi klien Anda sendiri. Lihat [Implementasi tool search kustom](#custom-tool-search-implementation) untuk detailnya.

<Note>
  Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/MhcGFFwLxuwnWTkYA).
</Note>

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

<Warning>
  Di Amazon Bedrock, tool search sisi server hanya tersedia melalui [InvokeModel API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html), bukan Converse API.
</Warning>

<Note>
  Di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), tool search sisi server bekerja identik dengan Claude API. Claude Platform on AWS menggunakan Anthropic Messages API secara langsung, sehingga tidak ada perbedaan InvokeModel atau Converse.
</Note>

## Kompatibilitas model

Kedua varian tool search tersedia pada model-model berikut:

| Model                                          | Versi alat                                                          |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| Claude Fable 5 (claude-fable-5)                | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Mythos 5 (claude-mythos-5)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.8 (claude-opus-4-8)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.7 (claude-opus-4-7)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.6 (claude-opus-4-6)              | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.6 (claude-sonnet-4-6)          | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Opus 4.5 (claude-opus-4-5-20251101)     | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001)   | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` |

Claude Opus 4.1 dan model yang lebih lama tidak mendukung tool search tool.

## Cara kerja tool search

Ada dua varian tool search:

* **Regex** (`tool_search_tool_regex_20251119`): Claude membangun pola regex untuk mencari alat.
* **BM25** (`tool_search_tool_bm25_20251119`): Claude menggunakan kueri bahasa alami untuk mencari alat.

Ketika Anda mengaktifkan tool search tool:

1. Anda menyertakan tool search tool (misalnya, `tool_search_tool_regex_20251119` atau `tool_search_tool_bm25_20251119`) dalam daftar `tools` Anda.
2. Anda menyediakan setiap definisi alat dalam array `tools` dan menyetel `defer_loading: true` pada alat yang tidak boleh dimuat di awal. Setidaknya satu alat, biasanya tool search tool itu sendiri, harus tetap non-deferred.
3. Awalnya, konteks Claude hanya berisi tool search tool dan alat non-deferred apa pun.
4. Ketika Claude membutuhkan alat tambahan, ia mencari menggunakan tool search tool.
5. API menjalankan pencarian dan mengembalikan alat yang cocok sebagai blok `tool_reference` (hingga 5 secara default).
6. API secara otomatis memperluas referensi ini menjadi definisi alat lengkap.
7. Claude memilih dari alat yang ditemukan dan memanggilnya.

## Mulai cepat

Contoh berikut menyertakan tool search tool dan dua alat yang ditangguhkan (deferred):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
      Model = Model.ClaudeOpus4_8,
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
  fmt.Println(response)
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
          .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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

Claude mencari katalog, menemukan `get_weather`, dan memanggilnya. Respons berakhir dengan `stop_reason: "tool_use"`. Jalankan alat yang ditemukan dan kembalikan `tool_result` seperti dalam [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls). [Format respons](#response-format) menunjukkan blok yang Anda dapatkan kembali dan apa yang harus dikirim selanjutnya.

## Definisi alat

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

  Dengan `tool_search_tool_regex_20251119`, Claude menulis pola `re.search()` Python, bukan kueri bahasa alami. Pencocokan tidak peka huruf besar-kecil. Pola umum meliputi yang berikut:

  * `"weather"`: mencocokkan nama alat dan deskripsi yang mengandung "weather"
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
* Alat tanpa `defer_loading` dimuat ke dalam konteks segera.
* Alat dengan `defer_loading: true` hanya dimuat ketika Claude menemukannya melalui pencarian.
* Jangan pernah menyetel `defer_loading: true` pada tool search tool itu sendiri.
* Pertahankan 3–5 alat yang paling sering Anda gunakan sebagai non-deferred sehingga Claude dapat memanggilnya tanpa mencari terlebih dahulu.

Kedua varian tool search (`regex` dan `bm25`) mencari nama alat, deskripsi, nama argumen, dan deskripsi argumen.

Secara internal, API mengecualikan alat yang ditangguhkan dari prefiks prompt sistem. Ketika Claude menemukan alat yang ditangguhkan melalui tool search, API menambahkan blok `tool_reference` secara inline dalam percakapan, lalu memperluasnya menjadi definisi alat lengkap sebelum meneruskannya ke Claude. Prefiks tidak tersentuh, sehingga caching prompt tetap terjaga. Grammar untuk [strict mode](/docs/id/agents-and-tools/tool-use/strict-tool-use) (aturan yang membatasi output panggilan alat agar sesuai dengan skema Anda) dibangun dari seluruh toolset, sehingga `defer_loading` dan strict mode dapat digabungkan tanpa kompilasi ulang grammar.

## Format respons

Ketika Claude menggunakan tool search tool, respons menyertakan tipe blok berikut:

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
        "pattern": "weather"
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

* **`server_tool_use`:** panggilan Claude ke tool search tool. Pencarian berjalan di server Anthropic. Jangan pernah mengembalikan `tool_result` untuk ID `srvtoolu_...`-nya.
* **`tool_search_tool_result`:** hasil pencarian, dalam objek `tool_search_tool_search_result` bersarang. Pertahankan dalam riwayat pesan apa adanya.
* **`tool_references`:** array objek `tool_reference` yang menunjuk ke alat yang ditemukan. API memperluas ini untuk Claude. Anda tidak pernah memperluasnya sendiri.
* **`tool_use`:** panggilan Claude ke alat yang ditemukan. Jalankan dan kembalikan `tool_result` persis seperti dalam penggunaan alat standar.

API secara otomatis memperluas blok `tool_reference` menjadi definisi alat lengkap sebelum menampilkannya ke Claude. Anda tidak perlu menangani perluasan ini sendiri, selama Anda menyediakan semua definisi alat yang cocok dalam parameter `tools`.

### Melanjutkan percakapan

Pada permintaan berikutnya, teruskan kembali konten asisten tanpa perubahan, termasuk blok `server_tool_use` dan `tool_search_tool_result`. Tambahkan `tool_result` Anda untuk alat yang ditemukan dalam pesan pengguna, dan kirim array `tools` yang sama: alat pencarian ditambah setiap definisi yang ditangguhkan. Jangan mengembalikan `tool_result` untuk ID `srvtoolu_...`: API akan menolak permintaan tersebut. API memperluas blok `tool_reference` di seluruh riwayat percakapan, sehingga Claude dapat menggunakan kembali alat yang ditemukan di giliran berikutnya tanpa mencari ulang. Pencarian yang tidak menemukan apa pun mengembalikan `tool_search_tool_search_result` dengan array `tool_references` kosong, bukan error.

## Integrasi MCP

Jika alat Anda berasal dari server MCP melalui [konektor MCP](/docs/id/agents-and-tools/mcp-connector), Anda tidak menyetel `defer_loading` pada definisi alat individual. Sebagai gantinya, setel sekali pada `default_config` entri `mcp_toolset` untuk seluruh server, atau per alat dalam `configs`-nya. Lihat [Konfigurasi toolset MCP](/docs/id/agents-and-tools/mcp-connector#mcp-toolset-configuration).

## Implementasi tool search kustom

Anda dapat mengimplementasikan logika tool search Anda sendiri (misalnya, menggunakan embeddings atau pencarian semantik) dengan mengembalikan blok `tool_reference` dari alat kustom. Ketika Claude memanggil alat pencarian kustom Anda, kembalikan `tool_result` standar dengan blok `tool_reference` dalam array konten:

```json JSON
{
  "type": "tool_result",
  "tool_use_id": "toolu_your_tool_id",
  "content": [{ "type": "tool_reference", "tool_name": "discovered_tool_name" }]
}
```

Setiap alat yang direferensikan harus memiliki definisi alat yang sesuai dalam parameter `tools` tingkat atas, biasanya dengan `defer_loading: true`. Ini memungkinkan Anda menggunakan metode pencarian yang tidak disediakan oleh varian bawaan, seperti pengambilan berbasis embedding, dan API memperluas blok `tool_reference` yang dikembalikan dengan cara yang sama.

<Note>
  Format `tool_search_tool_result` yang ditunjukkan di bagian [Format respons](#response-format) adalah format sisi server yang digunakan secara internal oleh tool search bawaan Anthropic. Untuk implementasi sisi klien kustom, selalu gunakan format `tool_result` standar dengan blok konten `tool_reference` seperti yang ditunjukkan pada contoh sebelumnya.
</Note>

Untuk contoh lengkap menggunakan embeddings, lihat resep [tool search dengan embeddings](https://platform.claude.com/cookbook/tool-use-tool-search-with-embeddings).

## Penanganan error

<Note>
  [Contoh penggunaan alat](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples) bekerja dengan tool search: ketika Claude menemukan alat yang ditangguhkan, API memperluas `input_examples`-nya bersama dengan definisinya.
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

### Error hasil alat (status 200)

Ketika operasi tool search gagal selama eksekusi, API mengembalikan respons 200 dengan error di dalam body:

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

Field `error_code` memiliki empat kemungkinan nilai:

* `invalid_tool_input`: input pencarian tidak valid, misalnya pola regex yang salah bentuk atau pola yang melebihi batas 200 karakter
* `unavailable`: pencarian tidak dapat berjalan, misalnya karena waktu habis atau layanan tidak tersedia
* `too_many_requests`: batas laju terlampaui untuk operasi tool search
* `execution_time_exceeded`: pencarian melebihi batas waktu eksekusinya

### Kesalahan umum

<Accordion title="Error 400: semua alat ditangguhkan">
  **Penyebab:** Anda menyetel `defer_loading: true` pada setiap alat, termasuk tool search tool.

  **Perbaikan:** Hapus `defer_loading` dari tool search tool:

  ```json
  {
    "type": "tool_search_tool_regex_20251119",
    "name": "tool_search_tool_regex"
  }
  ```
</Accordion>

<Accordion title="Error 400: definisi alat hilang">
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

  1. Periksa nama alat, deskripsi, nama argumen, dan deskripsi argumen. Claude mencari di semua field ini.
  2. Uji pola Anda: `import re; re.search(r"your_pattern", "tool_name", re.IGNORECASE)`.
  3. Pencocokan tidak peka huruf besar-kecil, jadi perbedaan huruf besar-kecil bukan masalahnya.
  4. Claude menggunakan pola yang luas seperti `".*weather.*"`, bukan pencocokan persis.

  **Tip:** Tambahkan kata kunci umum ke deskripsi alat untuk meningkatkan kemudahan penemuan.
</Accordion>

## Caching prompt

Untuk bagaimana `defer_loading` mempertahankan caching prompt, lihat [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching).

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

## Permintaan batch

Anda dapat menyertakan tool search tool dalam [Messages Batches API](/docs/id/build-with-claude/batch-processing).

## Batasan dan praktik terbaik

### Batasan

* **Maksimum alat yang ditangguhkan:** 10.000 alat dengan `defer_loading: true` per permintaan
* **Hasil pencarian:** setiap pencarian mengembalikan hingga 5 alat yang cocok secara default
* **Panjang pola dan kueri:** maksimum 200 karakter untuk pola regex dan 500 karakter untuk kueri BM25
* **Dukungan model:** lihat [Kompatibilitas model](#model-compatibility)

### Kapan menggunakan tool search

Gunakan tool search ketika salah satu dari hal berikut berlaku:

* Anda memiliki 10 alat atau lebih yang tersedia.
* Definisi alat Anda mengonsumsi lebih dari 10k token.
* Akurasi pemilihan alat menurun seiring bertambahnya toolset Anda.
* Anda menggabungkan beberapa server MCP (200+ alat).
* Pustaka alat Anda bertambah seiring waktu.

Pemanggilan alat standar, tanpa tool search, lebih cocok ketika Anda memiliki kurang dari 10 alat, setiap alat digunakan dalam setiap permintaan, atau definisi alat Anda kecil (kurang dari 100 token total).

### Tips optimasi

* Pertahankan 3–5 alat yang paling sering Anda gunakan sebagai non-deferred.
* Tulis nama dan deskripsi alat yang jelas dan deskriptif.
* Gunakan namespacing yang konsisten dalam nama alat: beri prefiks berdasarkan layanan atau sumber daya (misalnya, `github_`, `slack_`) sehingga satu pencarian mencocokkan seluruh grup.
* Gunakan kata kunci dalam deskripsi yang cocok dengan cara pengguna mendeskripsikan tugas.
* Tambahkan bagian prompt sistem yang mendeskripsikan kategori alat yang tersedia: "Anda dapat mencari alat untuk berinteraksi dengan Slack, GitHub, dan Jira."
* Pantau alat mana yang ditemukan Claude untuk menyempurnakan deskripsi Anda.

## Penggunaan

Tool search tidak diukur sebagai alat server terpisah. Objek `usage.server_tool_use` pada respons tidak memiliki field tool search, dan definisi alat yang dimuat oleh pencarian ke dalam konteks dihitung sebagai input\_tokens seperti definisi alat lainnya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Memory tool" icon="brain" href="/docs/id/agents-and-tools/tool-use/memory-tool">
    Biarkan Claude menyimpan dan mengambil informasi di seluruh percakapan dengan mengimplementasikan operasi file memory tool di aplikasi Anda.
  </Card>

  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>

  <Card title="Konektor MCP" icon="link" href="/docs/id/agents-and-tools/mcp-connector">
    Konfigurasikan toolset MCP dengan pemuatan yang ditangguhkan.
  </Card>

  <Card title="Penggunaan alat dengan caching prompt" icon="bolt" href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.
  </Card>

  <Card title="Definisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
