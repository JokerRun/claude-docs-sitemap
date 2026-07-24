---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/search-results
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e68e484c459faa61ff95198a95d9b879e5c9dbdcdd32e76ac7e7e91a949bd134
---

# Hasil pencarian

Aktifkan sitasi alami untuk aplikasi RAG dengan menyediakan hasil pencarian beserta atribusi sumber

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Blok konten hasil pencarian memungkinkan Claude mengutip konten Anda sendiri dengan cara yang sama seperti mengutip hasil pencarian web: setiap sitasi membawa sumber dan judul yang Anda berikan. Gunakan blok ini dalam aplikasi RAG (Retrieval-Augmented Generation) di mana Claude perlu mengatribusikan jawaban ke dokumen Anda.

Semua [model aktif](/docs/id/about-claude/models/overview) mendukung hasil pencarian dengan sitasi, dengan pengecualian Claude Haiku 3. Tidak diperlukan header beta: hasil pencarian adalah bagian dari Messages API standar.

## Cara kerjanya

Hasil pencarian dapat disediakan dengan dua cara:

1. **Dari pemanggilan alat:** Alat kustom Anda mengembalikan hasil pencarian, memungkinkan aplikasi RAG dinamis
2. **Sebagai konten tingkat atas:** Anda menyediakan hasil pencarian langsung dalam pesan pengguna untuk konten yang telah diambil sebelumnya atau di-cache

Dalam kedua kasus tersebut, Claude mengutip hasil pencarian secara otomatis ketika sitasi diaktifkan. Tidak diperlukan prompting khusus: ajukan pertanyaan Anda, dan sitasi akan muncul pada blok teks yang mengambil dari konten Anda.

### Skema hasil pencarian

Hasil pencarian menggunakan struktur berikut:

```json
{
  "type": "search_result",
  "source": "https://example.com/article", // Required: Source URL or identifier
  "title": "Article Title", // Required: Title of the result
  "content": [
    // Required: Array of text blocks
    {
      "type": "text",
      "text": "The actual content of the search result..."
    }
  ],
  "citations": {
    // Optional: Citation configuration
    "enabled": true // Enable/disable citations for this result
  }
}
```

### Field yang wajib

| Field     | Tipe   | Deskripsi                                                                                                             |
| --------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| `type`    | string | Harus `"search_result"`                                                                                               |
| `source`  | string | Sumber konten. String stabil apa pun dapat digunakan: URL, atau pengidentifikasi internal seperti `kb://article-1234` |
| `title`   | string | Judul deskriptif untuk hasil pencarian                                                                                |
| `content` | array  | Array blok teks yang berisi konten sebenarnya                                                                         |

### Field opsional

| Field           | Tipe   | Deskripsi                                                                                                                                                                                                                                                                                          |
| --------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `citations`     | object | Konfigurasi sitasi dengan field Boolean `enabled`. Sitasi dinonaktifkan secara default; setiap contoh di halaman ini menetapkan `"enabled": true` secara eksplisit. Semua hasil pencarian dalam satu permintaan harus menggunakan pengaturan yang sama (lihat [Kontrol sitasi](#citation-control)) |
| `cache_control` | object | Pengaturan kontrol cache (misalnya, `{"type": "ephemeral"}`)                                                                                                                                                                                                                                       |

Setiap item dalam array `content` harus berupa blok teks dengan:

* `type`: Harus `"text"`
* `text`: Konten teks sebenarnya (string yang tidak kosong)

Hasil pencarian hanya menampung teks. Gambar dan media lainnya tidak didukung di dalam array `content`.

## Metode 1: Hasil pencarian dari pemanggilan alat

Mengembalikan hasil pencarian dari alat kustom Anda memungkinkan aplikasi RAG dinamis: alat mengambil konten saat runtime, dan Claude mengutipnya dalam respons. Contoh berikut memaksa pemanggilan alat dengan [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use), sehingga langkah pengambilan berjalan setiap saat.

### Contoh: Alat basis pengetahuan

<CodeGroup>
  ```bash cURL
  # Alur pemanggilan alat memerlukan logika pencarian di sisi aplikasi yang tidak
  # dapat diubah menjadi satu perintah shell sekali jalan. Lihat tab SDK untuk alur lengkapnya.
  # Bentuk mentah dari percakapan alat dengan hasil pencarian ditampilkan di tab
  # cURL Menggabungkan kedua metode; Metode 2 menunjukkan bentuk tingkat atasnya.
  ```

  ```bash CLI
  # Alur pemanggilan alat memerlukan logika pencarian di sisi aplikasi yang tidak
  # dapat diubah menjadi satu perintah shell sekali jalan. Lihat tab SDK untuk alur lengkapnya.
  # Bentuk mentah percakapan alat dengan hasil pencarian ditampilkan di tab cURL
  # Combining both methods; Method 2 menunjukkan bentuk tingkat atasnya.
  ```

  ```python Python
  from anthropic.types import (
      MessageParam,
      TextBlockParam,
      SearchResultBlockParam,
      ToolResultBlockParam,
  )

  client = Anthropic()

  # Definisikan alat pencarian basis pengetahuan
  knowledge_base_tool = {
      "name": "search_knowledge_base",
      "description": "Search the company knowledge base for information",
      "input_schema": {
          "type": "object",
          "properties": {"query": {"type": "string", "description": "The search query"}},
          "required": ["query"],
      },
  }


  # Fungsi untuk menangani pemanggilan alat
  def search_knowledge_base(query):
      # Logika pencarian Anda di sini
      # Mengembalikan hasil pencarian dalam format yang benar
      return [
          SearchResultBlockParam(
              type="search_result",
              source="https://docs.company.com/product-guide",
              title="Product Configuration Guide",
              content=[
                  TextBlockParam(
                      type="text",
                      text="To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.",
                  )
              ],
              citations={"enabled": True},
          ),
          SearchResultBlockParam(
              type="search_result",
              source="https://docs.company.com/troubleshooting",
              title="Troubleshooting Guide",
              content=[
                  TextBlockParam(
                      type="text",
                      text="If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.",
                  )
              ],
              citations={"enabled": True},
          ),
      ]


  # Bangun percakapan dalam sebuah list, dimulai dari pertanyaan pengguna
  messages = [
      MessageParam(role="user", content="How do I configure the timeout settings?")
  ]

  # Buat pesan dengan alat tersebut
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[knowledge_base_tool],
      tool_choice={"type": "tool", "name": "search_knowledge_base"},
      messages=messages,
  )

  # Saat Claude memanggil alat, berikan hasil pencariannya.
  # Blok tool_use tidak selalu berada di urutan pertama: lakukan iterasi untuk menemukannya.
  tool_use = next((block for block in response.content if block.type == "tool_use"), None)
  if tool_use is not None:
      tool_result = search_knowledge_base(tool_use.input["query"])

      # Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
      messages.append(MessageParam(role="assistant", content=response.content))
      messages.append(
          MessageParam(
              role="user",
              content=[
                  ToolResultBlockParam(
                      type="tool_result",
                      tool_use_id=tool_use.id,
                      content=tool_result,  # Search results go here
                  )
              ],
          )
      )

      # Kirim kembali hasil alat
      final_response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=messages,
      )
      print(final_response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Definisikan alat pencarian basis pengetahuan
  const knowledgeBaseTool: Anthropic.Tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object" as const,
      properties: {
        query: {
          type: "string",
          description: "The search query"
        }
      },
      required: ["query"]
    }
  };

  // Fungsi untuk menangani pemanggilan alat
  function searchKnowledgeBase(query: string) {
    // Logika pencarian Anda di sini
    // Mengembalikan hasil pencarian dalam format yang benar
    return [
      {
        type: "search_result" as const,
        source: "https://docs.company.com/product-guide",
        title: "Product Configuration Guide",
        content: [
          {
            type: "text" as const,
            text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
          }
        ],
        citations: { enabled: true }
      },
      {
        type: "search_result" as const,
        source: "https://docs.company.com/troubleshooting",
        title: "Troubleshooting Guide",
        content: [
          {
            type: "text" as const,
            text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
          }
        ],
        citations: { enabled: true }
      }
    ];
  }

  // Bangun percakapan dalam sebuah list, dimulai dengan pertanyaan pengguna
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "How do I configure the timeout settings?" }
  ];

  // Buat pesan dengan alat tersebut
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [knowledgeBaseTool],
    tool_choice: { type: "tool", name: "search_knowledge_base" },
    messages
  });

  // Tangani penggunaan alat dan berikan hasilnya.
  // Blok tool_use tidak selalu berada di urutan pertama: cari di dalam array content.
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
  );
  if (toolUse) {
    const input = toolUse.input as { query: string };
    const toolResult = searchKnowledgeBase(input.query);

    // Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
    messages.push({ role: "assistant", content: response.content });
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result" as const,
          tool_use_id: toolUse.id,
          content: toolResult // Search results go here
        }
      ]
    });

    // Kirim kembali hasil alat
    const finalResponse = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages
    });
    console.log(finalResponse);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var tools = new List<ToolUnion>
  {
      new ToolUnion(new Tool()
      {
          Name = "search_knowledge_base",
          Description = "Search the company knowledge base for information",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["query"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The search query" }),
              },
              Required = ["query"],
          },
      }),
  };

  // Fungsi untuk menangani pemanggilan alat
  static List<Block> SearchKnowledgeBase(string query)
  {
      // Logika pencarian Anda di sini
      // Mengembalikan hasil pencarian dalam format yang benar
      return
      [
          new SearchResultBlockParam
          {
              Source = "https://docs.company.com/product-guide",
              Title = "Product Configuration Guide",
              Content = [new() { Text = "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs." }],
              Citations = new() { Enabled = true },
          },
          new SearchResultBlockParam
          {
              Source = "https://docs.company.com/troubleshooting",
              Title = "Troubleshooting Guide",
              Content = [new() { Text = "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values." }],
              Citations = new() { Enabled = true },
          },
      ];
  }

  // Bangun percakapan dalam sebuah list, dimulai dari pertanyaan pengguna
  List<MessageParam> messages = [new() { Role = Role.User, Content = "How do I configure the timeout settings?" }];

  // Buat pesan dengan alat tersebut
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = new ToolChoiceTool { Name = "search_knowledge_base" },
      Messages = messages,
  });

  // Saat Claude memanggil alat, berikan hasil pencariannya.
  // Blok tool_use tidak selalu berada di urutan pertama: cari yang pertama.
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          var query = toolUse.Input["query"].GetString() ?? "";
          var toolResults = SearchKnowledgeBase(query);

          // Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
          messages.Add(new() { Role = Role.Assistant, Content = response.Content.Select(contentBlock => new ContentBlockParam(contentBlock.Json)).ToList() });
          messages.Add(new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
                  [new ContentBlockParam(new ToolResultBlockParam() { ToolUseID = toolUse.ID, Content = new ToolResultBlockParamContent(toolResults) })]
              ),
          });

          // Kirim kembali hasil alat
          var finalResponse = await client.Messages.Create(new()
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages = messages,
          });
          Console.WriteLine(finalResponse);
          break;
      }
  }
  ```

  ```go Go
  	client := anthropic.NewClient()

  	knowledgeBaseTool := anthropic.ToolUnionParam{
  		OfTool: &anthropic.ToolParam{
  			Name:        "search_knowledge_base",
  			Description: anthropic.String("Search the company knowledge base for information"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"query": map[string]any{
  						"type":        "string",
  						"description": "The search query",
  					},
  				},
  				Required: []string{"query"},
  			},
  		},
  	}

  	// Bangun percakapan dalam sebuah slice, dimulai dari pertanyaan pengguna
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
  	}

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus4_8,
  		MaxTokens:  1024,
  		Tools:      []anthropic.ToolUnionParam{knowledgeBaseTool},
  		ToolChoice: anthropic.ToolChoiceUnionParam{OfTool: &anthropic.ToolChoiceToolParam{Name: "search_knowledge_base"}},
  		Messages:   messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Blok tool_use tidak selalu berada di urutan pertama: cari di daftar konten
  	var toolUse *anthropic.ToolUseBlock
  	for _, block := range response.Content {
  		if variant, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  			toolUse = &variant
  			break
  		}
  	}

  	if toolUse != nil {
  		var input struct {
  			Query string `json:"query"`
  		}
  		if err := json.Unmarshal(toolUse.Input, &input); err != nil {
  			log.Fatal(err)
  		}
  		toolResults := searchKnowledgeBase(input.Query)

  		// Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
  		messages = append(messages, response.ToParam())
  		messages = append(messages, anthropic.NewUserMessage(anthropic.ContentBlockParamUnion{
  			OfToolResult: &anthropic.ToolResultBlockParam{
  				ToolUseID: toolUse.ID,
  				Content:   toolResults,
  			},
  		}))

  		// Kirim kembali hasil alat
  		finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		fmt.Println(finalResponse)
  	}
  // ...
  func searchKnowledgeBase(query string) []anthropic.ToolResultBlockParamContentUnion {
  	return []anthropic.ToolResultBlockParamContentUnion{
  		{OfSearchResult: &anthropic.SearchResultBlockParam{
  			Content: []anthropic.TextBlockParam{
  				{Text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."},
  			},
  			Source:    "https://docs.company.com/product-guide",
  			Title:     "Product Configuration Guide",
  			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  		}},
  		{OfSearchResult: &anthropic.SearchResultBlockParam{
  			Content: []anthropic.TextBlockParam{
  				{Text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."},
  			},
  			Source:    "https://docs.company.com/troubleshooting",
  			Title:     "Troubleshooting Guide",
  			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  		}},
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.ToolChoice;
  import com.anthropic.models.messages.ToolChoiceTool;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.core.JsonValue;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool knowledgeBaseTool = Tool.builder()
          .name("search_knowledge_base")
          .description("Search the company knowledge base for information")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "query", Map.of(
                      "type", "string",
                      "description", "The search query"
                  )
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("query")))
              .build())
          .build();

      // Bangun percakapan dalam sebuah list, dimulai dari pertanyaan pengguna
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("How do I configure the timeout settings?")
          .build());

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(knowledgeBaseTool)
          .toolChoice(ToolChoice.ofTool(ToolChoiceTool.builder()
              .name("search_knowledge_base")
              .build()))
          .messages(messages)
          .build();

      Message response = client.messages().create(params);

      // Blok tool_use tidak selalu berada di urutan pertama: cari di dalam daftar content
      response.content().stream()
          .flatMap(contentBlock -> contentBlock.toolUse().stream())
          .findFirst()
          .ifPresent(toolUse -> {
              Map<String, JsonValue> input =
                  (Map<String, JsonValue>) toolUse._input().asObject().get();
              List<ToolResultBlockParam.Content.Block> toolResult = searchKnowledgeBase(
                  input.get("query").asStringOrThrow()
              );

              // Tambahkan seluruh giliran Claude ke percakapan yang sedang berjalan, lalu hasil alatnya.
              // Membangun ulang hanya blok tool_use akan menghilangkan blok konten lain yang Claude
              // kembalikan (mis. teks pembuka saat pemanggilan alat tidak dipaksa) — tambahkan
              // giliran lengkapnya, seperti pada tab bahasa lainnya.
              messages.add(MessageParam.builder()
                  .role(MessageParam.Role.ASSISTANT)
                  .contentOfBlockParams(
                      response.content().stream()
                          .map(block -> block.toParam())
                          .toList()
                  )
                  .build());
              messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .contentOfBlockParams(List.of(
                      ContentBlockParam.ofToolResult(
                          ToolResultBlockParam.builder()
                              .toolUseId(toolUse.id())
                              .contentOfBlocks(toolResult)
                              .build()
                      )
                  ))
                  .build());

              // Kirim kembali hasil alat
              MessageCreateParams finalParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
                  .maxTokens(1024L)
                  .messages(messages)
                  .build();

              Message finalResponse = client.messages().create(finalParams);
              System.out.println(finalResponse);
          });
  }

  static List<ToolResultBlockParam.Content.Block> searchKnowledgeBase(String query) {
      return List.of(
          ToolResultBlockParam.Content.Block.ofSearchResult(
              SearchResultBlockParam.builder()
                  .source("https://docs.company.com/product-guide")
                  .title("Product Configuration Guide")
                  .content(List.of(
                      TextBlockParam.builder()
                          .text("To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.")
                          .build()
                  ))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()
          ),
          ToolResultBlockParam.Content.Block.ofSearchResult(
              SearchResultBlockParam.builder()
                  .source("https://docs.company.com/troubleshooting")
                  .title("Troubleshooting Guide")
                  .content(List.of(
                      TextBlockParam.builder()
                          .text("If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.")
                          .build()
                  ))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()
          )
      );
  }
  ```

  ```php PHP
  $client = new Client();

  $knowledgeBaseTool = [
      'name' => 'search_knowledge_base',
      'description' => 'Search the company knowledge base for information',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'query' => [
                  'type' => 'string',
                  'description' => 'The search query'
              ]
          ],
          'required' => ['query']
      ]
  ];

  function searchKnowledgeBase($query) {
      return [
          [
              'type' => 'search_result',
              'source' => 'https://docs.company.com/product-guide',
              'title' => 'Product Configuration Guide',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.'
                  ]
              ],
              'citations' => ['enabled' => true]
          ],
          [
              'type' => 'search_result',
              'source' => 'https://docs.company.com/troubleshooting',
              'title' => 'Troubleshooting Guide',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.'
                  ]
              ],
              'citations' => ['enabled' => true]
          ]
      ];
  }

  // Bangun percakapan dalam sebuah list, dimulai dari pertanyaan pengguna
  $messages = [
      ['role' => 'user', 'content' => 'How do I configure the timeout settings?']
  ];

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: $messages,
      model: 'claude-opus-4-8',
      toolChoice: ['type' => 'tool', 'name' => 'search_knowledge_base'],
      tools: [$knowledgeBaseTool],
  );

  $toolUseBlock = null;
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolUseBlock = $block;
          break;
      }
  }

  if ($toolUseBlock !== null) {
      $toolResult = searchKnowledgeBase($toolUseBlock->input['query']);

      // Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = [
          'role' => 'user',
          'content' => [
              [
                  'type' => 'tool_result',
                  'tool_use_id' => $toolUseBlock->id,
                  'content' => $toolResult
              ]
          ]
      ];

      // Kirim kembali hasil alat
      $finalResponse = $client->messages->create(
          maxTokens: 1024,
          messages: $messages,
          model: 'claude-opus-4-8',
      );
      echo $finalResponse;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  knowledge_base_tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  }

  def search_knowledge_base(query)
    [
      {
        type: "search_result",
        source: "https://docs.company.com/product-guide",
        title: "Product Configuration Guide",
        content: [
          {
            type: "text",
            text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
          }
        ],
        citations: { enabled: true }
      },
      {
        type: "search_result",
        source: "https://docs.company.com/troubleshooting",
        title: "Troubleshooting Guide",
        content: [
          {
            type: "text",
            text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
          }
        ],
        citations: { enabled: true }
      }
    ]
  end

  # Bangun percakapan dalam sebuah list, dimulai dari pertanyaan pengguna
  messages = [
    { role: "user", content: "How do I configure the timeout settings?" }
  ]

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [knowledge_base_tool],
    tool_choice: { type: "tool", name: "search_knowledge_base" },
    messages: messages
  )

  # Blok tool_use tidak selalu berada di urutan pertama: cari di dalam array content
  tool_use = response.content.find { |block| block.type == :tool_use }

  if tool_use
    tool_result = search_knowledge_base(tool_use.input[:query])

    # Tambahkan giliran Claude, lalu hasil alat, ke percakapan yang sedang berjalan
    messages << { role: "assistant", content: response.content }
    messages << {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: tool_result
        }
      ]
    }

    # Kirim kembali hasil alat
    final_response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages
    )
    puts final_response
  end
  ```
</CodeGroup>

## Metode 2: Hasil pencarian sebagai konten tingkat atas

Anda juga dapat menyediakan hasil pencarian langsung dalam pesan pengguna. Ini berguna untuk:

* Konten yang telah diambil sebelumnya dari infrastruktur pencarian Anda
* Hasil pencarian yang di-cache dari kueri sebelumnya
* Konten dari layanan pencarian eksternal
* Pengujian dan pengembangan

### Contoh: Hasil pencarian langsung

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "search_result",
              "source": "https://docs.company.com/api-reference",
              "title": "API Reference - Authentication",
              "content": [
                {
                  "type": "text",
                  "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                }
              ],
              "citations": {
                "enabled": true
              }
            },
            {
              "type": "search_result",
              "source": "https://docs.company.com/quickstart",
              "title": "Getting Started Guide",
              "content": [
                {
                  "type": "text",
                  "text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                }
              ],
              "citations": {
                "enabled": true
              }
            },
            {
              "type": "text",
              "text": "Based on these search results, how do I authenticate API requests and what are the rate limits?"
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: search_result
          source: https://docs.company.com/api-reference
          title: API Reference - Authentication
          content:
            - type: text
              text: >-
                All API requests must include an API key in the Authorization
                header. Keys can be generated from the dashboard. Rate limits:
                1000 requests per hour for standard tier, 10000 for premium.
          citations:
            enabled: true
        - type: search_result
          source: https://docs.company.com/quickstart
          title: Getting Started Guide
          content:
            - type: text
              text: >-
                To get started: 1) Sign up for an account, 2) Generate an API
                key from the dashboard, 3) Install our SDK using pip install
                company-sdk, 4) Initialize the client with your API key.
          citations:
            enabled: true
        - type: text
          text: >-
            Based on these search results, how do I authenticate API requests
            and what are the rate limits?
  YAML
  ```

  ```python Python
  from anthropic.types import MessageParam, TextBlockParam, SearchResultBlockParam

  client = Anthropic()

  # Berikan hasil pencarian langsung di dalam pesan pengguna
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          MessageParam(
              role="user",
              content=[
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/api-reference",
                      title="API Reference - Authentication",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/quickstart",
                      title="Getting Started Guide",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  TextBlockParam(
                      type="text",
                      text="Based on these search results, how do I authenticate API requests and what are the rate limits?",
                  ),
              ],
          )
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Berikan hasil pencarian langsung di pesan pengguna
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result" as const,
            source: "https://docs.company.com/api-reference",
            title: "API Reference - Authentication",
            content: [
              {
                type: "text" as const,
                text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "search_result" as const,
            source: "https://docs.company.com/quickstart",
            title: "Getting Started Guide",
            content: [
              {
                type: "text" as const,
                text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text" as const,
            text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Sediakan hasil pencarian langsung di dalam pesan pengguna
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/api-reference",
                      Title = "API Reference - Authentication",
                      Content = [new() { Text = "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/quickstart",
                      Title = "Getting Started Guide",
                      Content = [new() { Text = "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new TextBlockParam { Text = "Based on these search results, how do I authenticate API requests and what are the rate limits?" }),
              ]),
          },
      ],
  });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."},
  				},
  				Source:    "https://docs.company.com/api-reference",
  				Title:     "API Reference - Authentication",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."},
  				},
  				Source:    "https://docs.company.com/quickstart",
  				Title:     "Getting Started Guide",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.NewTextBlock("Based on these search results, how do I authenticate API requests and what are the rate limits?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofSearchResult(
                  SearchResultBlockParam.builder()
                      .source("https://docs.company.com/api-reference")
                      .title("API Reference - Authentication")
                      .content(List.of(
                          TextBlockParam.builder()
                              .text("All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.")
                              .build()
                      ))
                      .citations(CitationsConfigParam.builder().enabled(true).build())
                      .build()
              ),
              ContentBlockParam.ofSearchResult(
                  SearchResultBlockParam.builder()
                      .source("https://docs.company.com/quickstart")
                      .title("Getting Started Guide")
                      .content(List.of(
                          TextBlockParam.builder()
                              .text("To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.")
                              .build()
                      ))
                      .citations(CitationsConfigParam.builder().enabled(true).build())
                      .build()
              ),
              ContentBlockParam.ofText(
                  TextBlockParam.builder()
                      .text("Based on these search results, how do I authenticate API requests and what are the rate limits?")
                      .build()
              )
          ))
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/api-reference',
                      'title' => 'API Reference - Authentication',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/quickstart',
                      'title' => 'Getting Started Guide',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Based on these search results, how do I authenticate API requests and what are the rate limits?'
                  ]
              ]
          ]
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($message, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result",
            source: "https://docs.company.com/api-reference",
            title: "API Reference - Authentication",
            content: [
              {
                type: "text",
                text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "search_result",
            source: "https://docs.company.com/quickstart",
            title: "Getting Started Guide",
            content: [
              {
                type: "text",
                text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
          }
        ]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

## Respons Claude dengan sitasi

Terlepas dari bagaimana hasil pencarian disediakan, Claude secara otomatis menyertakan sitasi saat menggunakan informasi dari hasil tersebut:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    },
    {
      "type": "text",
      "text": "\n\nTo set this up from scratch, you'll need to "
    },
    {
      "type": "text",
      "text": "sign up for an account, generate an API key from the dashboard, install the SDK using `pip install company-sdk`, and initialize the client with your API key.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
          "source": "https://docs.company.com/quickstart",
          "title": "Getting Started Guide",
          "search_result_index": 1,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    }
  ]
}
```

### Field sitasi

Setiap sitasi mencakup:

| Field                 | Tipe             | Deskripsi                                                                                                                                                               |
| --------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                | string           | Selalu `"search_result_location"` untuk sitasi hasil pencarian                                                                                                          |
| `source`              | string           | Sumber dari hasil pencarian asli                                                                                                                                        |
| `title`               | string atau null | Judul dari hasil pencarian asli                                                                                                                                         |
| `cited_text`          | string           | Teks lengkap dari blok yang dikutip, digabungkan. Sama dengan isi `content[start_block_index:end_block_index]` yang digabungkan. Tidak dihitung sebagai output tokens.  |
| `search_result_index` | integer          | Indeks berbasis 0 dari hasil pencarian yang dikutip di antara semua blok `search_result` dalam permintaan, sesuai urutan kemunculannya (di semua pesan dan hasil alat). |
| `start_block_index`   | integer          | Indeks berbasis 0 dari blok pertama yang dikutip dalam array `content` hasil pencarian.                                                                                 |
| `end_block_index`     | integer          | Indeks akhir eksklusif dari rentang blok yang dikutip dalam array `content` hasil pencarian. Selalu lebih besar dari `start_block_index`.                               |

Indeks blok mengidentifikasi irisan dari array `content` hasil pencarian, dan `cited_text` adalah teks lengkap dari irisan tersebut. Blok teks adalah unit terkecil yang dapat dikutip: Claude mengutip blok secara utuh, bukan substring di dalam sebuah blok. Untuk mendapatkan sitasi yang lebih terperinci, pecah konten hasil pencarian Anda menjadi blok-blok yang lebih kecil (lihat [Beberapa blok konten](#multiple-content-blocks)).

## Beberapa blok konten

Hasil pencarian dapat berisi beberapa blok teks dalam array `content`:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "content": [
    {
      "type": "text",
      "text": "Authentication: All API requests require an API key."
    },
    {
      "type": "text",
      "text": "Rate Limits: The API allows 1000 requests per hour per key."
    },
    {
      "type": "text",
      "text": "Error Handling: The API returns standard HTTP status codes."
    }
  ],
  "citations": { "enabled": true }
}
```

Sitasi yang merujuk pada blok batas laju terlihat seperti:

```json
{
  "type": "search_result_location",
  "cited_text": "Rate Limits: The API allows 1000 requests per hour per key.",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "search_result_index": 0,
  "start_block_index": 1,
  "end_block_index": 2
}
```

Ketika hasil pencarian ini dikutip, `start_block_index` dan `end_block_index` mengidentifikasi blok mana yang dicakup oleh sitasi, dan `cited_text` berisi tepat teks dari blok-blok tersebut. Memecah konten menjadi blok-blok yang lebih kecil dan terfokus memberi Claude batas sitasi yang lebih terperinci; menggabungkan konten menjadi satu blok berarti setiap sitasi mengembalikan teks lengkap. Ini adalah model yang sama yang digunakan oleh [dokumen konten kustom](/docs/id/build-with-claude/citations#custom-content-documents) dalam fitur Citations.

## Penggunaan lanjutan

### Menggabungkan kedua metode

Anda dapat mencampur kedua metode dalam percakapan yang sama. Claude mengutip dari salah satu sumber, dan `search_result_index` menghitung semua blok `search_result` sesuai urutan permintaan, terlepas dari sumbernya.

Contoh berikut memutar ulang percakapan lengkap. Pesan pengguna pertama membawa hasil pencarian yang telah diambil sebelumnya, giliran asisten memanggil alat basis pengetahuan, dan hasil alat mengembalikan hasil pencarian kedua. Jawaban Claude mengutip kedua sumber:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "search_knowledge_base",
          "description": "Search the company knowledge base for information",
          "input_schema": {
            "type": "object",
            "properties": {
              "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "search_result",
              "source": "https://docs.company.com/overview",
              "title": "Product Overview",
              "content": [
                {
                  "type": "text",
                  "text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
                }
              ],
              "citations": {"enabled": true}
            },
            {
              "type": "text",
              "text": "What does Acme Dashboard do, and what plans is it available on?"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Let me check the pricing information."
            },
            {
              "type": "tool_use",
              "id": "toolu_01A09q90qw90lq917835lq9",
              "name": "search_knowledge_base",
              "input": {"query": "Acme Dashboard pricing plans"}
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "tool_result",
              "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
              "content": [
                {
                  "type": "search_result",
                  "source": "https://docs.company.com/pricing",
                  "title": "Pricing Plans",
                  "content": [
                    {
                      "type": "text",
                      "text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                    }
                  ],
                  "citations": {"enabled": true}
                }
              ]
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  tools:
    - name: search_knowledge_base
      description: Search the company knowledge base for information
      input_schema:
        type: object
        properties:
          query:
            type: string
            description: The search query
        required: [query]
  messages:
    - role: user
      content:
        - type: search_result
          source: https://docs.company.com/overview
          title: Product Overview
          content:
            - type: text
              text: >-
                Acme Dashboard is a monitoring tool for distributed systems.
                It supports real-time alerting and custom metric dashboards.
          citations:
            enabled: true
        - type: text
          text: What does Acme Dashboard do, and what plans is it available on?
    - role: assistant
      content:
        - type: text
          text: Let me check the pricing information.
        - type: tool_use
          id: toolu_01A09q90qw90lq917835lq9
          name: search_knowledge_base
          input:
            query: Acme Dashboard pricing plans
    - role: user
      content:
        - type: tool_result
          tool_use_id: toolu_01A09q90qw90lq917835lq9
          content:
            - type: search_result
              source: https://docs.company.com/pricing
              title: Pricing Plans
              content:
                - type: text
                  text: >-
                    Acme Dashboard is available on the Starter plan at $10 per
                    user per month and the Enterprise plan with custom pricing.
              citations:
                enabled: true
  YAML
  ```

  ```python Python
  from anthropic.types import (
      MessageParam,
      SearchResultBlockParam,
      TextBlockParam,
      ToolResultBlockParam,
      ToolUseBlockParam,
  )

  client = Anthropic()

  knowledge_base_tool = {
      "name": "search_knowledge_base",
      "description": "Search the company knowledge base for information",
      "input_schema": {
          "type": "object",
          "properties": {"query": {"type": "string", "description": "The search query"}},
          "required": ["query"],
      },
  }

  # Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  # pertama membawa hasil yang sudah diambil sebelumnya, tool result mengembalikan hasil lainnya
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[knowledge_base_tool],
      messages=[
          MessageParam(
              role="user",
              content=[
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/overview",
                      title="Product Overview",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  TextBlockParam(
                      type="text",
                      text="What does Acme Dashboard do, and what plans is it available on?",
                  ),
              ],
          ),
          MessageParam(
              role="assistant",
              content=[
                  TextBlockParam(
                      type="text", text="Let me check the pricing information."
                  ),
                  ToolUseBlockParam(
                      type="tool_use",
                      id="toolu_01A09q90qw90lq917835lq9",
                      name="search_knowledge_base",
                      input={"query": "Acme Dashboard pricing plans"},
                  ),
              ],
          ),
          MessageParam(
              role="user",
              content=[
                  ToolResultBlockParam(
                      type="tool_result",
                      tool_use_id="toolu_01A09q90qw90lq917835lq9",
                      content=[
                          SearchResultBlockParam(
                              type="search_result",
                              source="https://docs.company.com/pricing",
                              title="Pricing Plans",
                              content=[
                                  TextBlockParam(
                                      type="text",
                                      text="Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
                                  )
                              ],
                              citations={"enabled": True},
                          )
                      ],
                  )
              ],
          ),
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const knowledgeBaseTool: Anthropic.Tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  };

  // Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  // pertama membawa hasil yang sudah diambil sebelumnya, tool result mengembalikan hasil lainnya
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [knowledgeBaseTool],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result" as const,
            source: "https://docs.company.com/overview",
            title: "Product Overview",
            content: [
              {
                type: "text" as const,
                text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text" as const,
            text: "What does Acme Dashboard do, and what plans is it available on?"
          }
        ]
      },
      {
        role: "assistant",
        content: [
          { type: "text" as const, text: "Let me check the pricing information." },
          {
            type: "tool_use" as const,
            id: "toolu_01A09q90qw90lq917835lq9",
            name: "search_knowledge_base",
            input: { query: "Acme Dashboard pricing plans" }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result" as const,
            tool_use_id: "toolu_01A09q90qw90lq917835lq9",
            content: [
              {
                type: "search_result" as const,
                source: "https://docs.company.com/pricing",
                title: "Pricing Plans",
                content: [
                  {
                    type: "text" as const,
                    text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                  }
                ],
                citations: { enabled: true }
              }
            ]
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  // pertama membawa hasil yang sudah diambil sebelumnya, tool result mengembalikan hasil lainnya
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools =
      [
          new ToolUnion(new Tool()
          {
              Name = "search_knowledge_base",
              Description = "Search the company knowledge base for information",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["query"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The search query" }),
                  },
                  Required = ["query"],
              },
          }),
      ],
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/overview",
                      Title = "Product Overview",
                      Content = [new() { Text = "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new TextBlockParam { Text = "What does Acme Dashboard do, and what plans is it available on?" }),
              ]),
          },
          new()
          {
              Role = Role.Assistant,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new TextBlockParam { Text = "Let me check the pricing information." }),
                  new ContentBlockParam(new ToolUseBlockParam
                  {
                      ID = "toolu_01A09q90qw90lq917835lq9",
                      Name = "search_knowledge_base",
                      Input = new Dictionary<string, JsonElement>
                      {
                          ["query"] = JsonSerializer.SerializeToElement("Acme Dashboard pricing plans"),
                      },
                  }),
              ]),
          },
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new ToolResultBlockParam()
                  {
                      ToolUseID = "toolu_01A09q90qw90lq917835lq9",
                      Content = new ToolResultBlockParamContent(
                      [
                          new SearchResultBlockParam
                          {
                              Source = "https://docs.company.com/pricing",
                              Title = "Pricing Plans",
                              Content = [new() { Text = "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing." }],
                              Citations = new() { Enabled = true },
                          },
                      ]),
                  }),
              ]),
          },
      ],
  });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  knowledgeBaseTool := anthropic.ToolUnionParam{
  	OfTool: &anthropic.ToolParam{
  		Name:        "search_knowledge_base",
  		Description: anthropic.String("Search the company knowledge base for information"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"query": map[string]any{"type": "string", "description": "The search query"},
  			},
  			Required: []string{"query"},
  		},
  	},
  }

  // Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  // pertama membawa hasil yang telah diambil sebelumnya, tool result mengembalikan hasil lainnya
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools:     []anthropic.ToolUnionParam{knowledgeBaseTool},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."},
  				},
  				Source:    "https://docs.company.com/overview",
  				Title:     "Product Overview",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.NewTextBlock("What does Acme Dashboard do, and what plans is it available on?"),
  		),
  		anthropic.NewAssistantMessage(
  			anthropic.NewTextBlock("Let me check the pricing information."),
  			anthropic.ContentBlockParamUnion{OfToolUse: &anthropic.ToolUseBlockParam{
  				ID:    "toolu_01A09q90qw90lq917835lq9",
  				Name:  "search_knowledge_base",
  				Input: map[string]any{"query": "Acme Dashboard pricing plans"},
  			}},
  		),
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfToolResult: &anthropic.ToolResultBlockParam{
  				ToolUseID: "toolu_01A09q90qw90lq917835lq9",
  				Content: []anthropic.ToolResultBlockParamContentUnion{
  					{OfSearchResult: &anthropic.SearchResultBlockParam{
  						Content: []anthropic.TextBlockParam{
  							{Text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."},
  						},
  						Source:    "https://docs.company.com/pricing",
  						Title:     "Pricing Plans",
  						Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  					}},
  				},
  			}},
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.CitationsConfigParam;
  import com.anthropic.models.messages.ContentBlockParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlockParam;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool knowledgeBaseTool = Tool.builder()
          .name("search_knowledge_base")
          .description("Search the company knowledge base for information")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "query", Map.of("type", "string", "description", "The search query")
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("query")))
              .build())
          .build();

      // Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan
      // pengguna pertama membawa hasil yang sudah diambil sebelumnya, hasil alat mengembalikan hasil lainnya
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(knowledgeBaseTool)
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofSearchResult(SearchResultBlockParam.builder()
                  .source("https://docs.company.com/overview")
                  .title("Product Overview")
                  .content(List.of(TextBlockParam.builder()
                      .text("Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.")
                      .build()))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()),
              ContentBlockParam.ofText(TextBlockParam.builder()
                  .text("What does Acme Dashboard do, and what plans is it available on?")
                  .build())
          ))
          .addAssistantMessageOfBlockParams(List.of(
              ContentBlockParam.ofText(TextBlockParam.builder()
                  .text("Let me check the pricing information.")
                  .build()),
              ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                  .id("toolu_01A09q90qw90lq917835lq9")
                  .name("search_knowledge_base")
                  .input(JsonValue.from(Map.of("query", "Acme Dashboard pricing plans")))
                  .build())
          ))
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                  .toolUseId("toolu_01A09q90qw90lq917835lq9")
                  .contentOfBlocks(List.of(
                      ToolResultBlockParam.Content.Block.ofSearchResult(SearchResultBlockParam.builder()
                          .source("https://docs.company.com/pricing")
                          .title("Pricing Plans")
                          .content(List.of(TextBlockParam.builder()
                              .text("Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.")
                              .build()))
                          .citations(CitationsConfigParam.builder().enabled(true).build())
                          .build())
                  ))
                  .build())
          ))
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $knowledgeBaseTool = [
      'name' => 'search_knowledge_base',
      'description' => 'Search the company knowledge base for information',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'query' => ['type' => 'string', 'description' => 'The search query']
          ],
          'required' => ['query']
      ]
  ];

  // Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  // pertama membawa hasil yang telah diambil sebelumnya, tool result mengembalikan hasil lainnya
  $response = $client->messages->create(
      maxTokens: 1024,
      tools: [$knowledgeBaseTool],
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/overview',
                      'title' => 'Product Overview',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What does Acme Dashboard do, and what plans is it available on?'
                  ]
              ]
          ],
          [
              'role' => 'assistant',
              'content' => [
                  ['type' => 'text', 'text' => 'Let me check the pricing information.'],
                  [
                      'type' => 'tool_use',
                      'id' => 'toolu_01A09q90qw90lq917835lq9',
                      'name' => 'search_knowledge_base',
                      'input' => ['query' => 'Acme Dashboard pricing plans']
                  ]
              ]
          ],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => 'toolu_01A09q90qw90lq917835lq9',
                      'content' => [
                          [
                              'type' => 'search_result',
                              'source' => 'https://docs.company.com/pricing',
                              'title' => 'Pricing Plans',
                              'content' => [
                                  [
                                      'type' => 'text',
                                      'text' => 'Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.'
                                  ]
                              ],
                              'citations' => ['enabled' => true]
                          ]
                      ]
                  ]
              ]
          ]
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  knowledge_base_tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  }

  # Memutar ulang percakapan yang menyediakan hasil pencarian dengan dua cara: pesan pengguna
  # pertama membawa hasil yang sudah diambil sebelumnya, tool result mengembalikan hasil lainnya
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [knowledge_base_tool],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result",
            source: "https://docs.company.com/overview",
            title: "Product Overview",
            content: [
              {
                type: "text",
                text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "What does Acme Dashboard do, and what plans is it available on?"
          }
        ]
      },
      {
        role: "assistant",
        content: [
          { type: "text", text: "Let me check the pricing information." },
          {
            type: "tool_use",
            id: "toolu_01A09q90qw90lq917835lq9",
            name: "search_knowledge_base",
            input: { query: "Acme Dashboard pricing plans" }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_01A09q90qw90lq917835lq9",
            content: [
              {
                type: "search_result",
                source: "https://docs.company.com/pricing",
                title: "Pricing Plans",
                content: [
                  {
                    type: "text",
                    text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                  }
                ],
                citations: { enabled: true }
              }
            ]
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

Respons mengutip kedua sumber. Hasil yang telah diambil sebelumnya adalah `search_result_index: 0` dan hasil yang dikembalikan alat adalah `search_result_index: 1`, sesuai dengan urutan kemunculan blok `search_result` dalam percakapan:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here's what I found about Acme Dashboard:\n\n**What it does:** "
    },
    {
      "type": "text",
      "text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
          "source": "https://docs.company.com/overview",
          "title": "Product Overview",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    },
    {
      "type": "text",
      "text": "\n\n**Available plans:** "
    },
    {
      "type": "text",
      "text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
          "source": "https://docs.company.com/pricing",
          "title": "Pricing Plans",
          "search_result_index": 1,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    }
  ]
}
```

### Mencampur dengan tipe konten lain

Dalam pesan pengguna, blok `search_result` dapat berdampingan dengan blok konten lainnya. Contoh Metode 2 memasangkan hasil pencarian dengan pertanyaan `text`, dan blok gambar atau dokumen dapat bergabung dengan cara yang sama.

Hasil alat lebih ketat: jika ada blok dalam array konten `tool_result` yang merupakan `search_result`, semua bloknya harus berupa `search_result`. Mencampur hasil pencarian dengan tipe blok lain dalam hasil alat yang sama akan mengembalikan kesalahan validasi. Untuk mengembalikan teks pendukung bersama hasil pencarian yang bersumber dari alat, sertakan teks tersebut sebagai blok teks di dalam salah satu array `content` hasil pencarian, di mana teks tersebut juga menjadi dapat dikutip.

### Kontrol cache

Tambahkan `cache_control` pada blok hasil pencarian untuk menyimpannya dalam cache agar dapat digunakan kembali di berbagai permintaan. Ini berada berdampingan dengan `citations` pada blok yang sama:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "..." }],
  "citations": { "enabled": true },
  "cache_control": { "type": "ephemeral" }
}
```

Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching) untuk panjang minimum yang dapat di-cache dan persyaratan lainnya.

### Kontrol sitasi

Secara default, sitasi dinonaktifkan untuk hasil pencarian. Anda dapat mengaktifkan sitasi dengan menetapkan konfigurasi `citations` secara eksplisit:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "Important documentation..." }],
  "citations": {
    "enabled": true // Enable citations for this result
  }
}
```

Ketika `citations.enabled` disetel ke `true`, Claude melampirkan referensi sitasi ke blok teks yang mengambil dari hasil pencarian.

<Warning>
  Sitasi bersifat semua-atau-tidak-sama-sekali: semua hasil pencarian dalam satu permintaan harus mengaktifkan sitasi, atau semuanya harus menonaktifkannya. Mencampur hasil pencarian dengan pengaturan sitasi yang berbeda akan menghasilkan kesalahan.
</Warning>

## Praktik terbaik

### Untuk pencarian berbasis alat (Metode 1)

* **Konten dinamis:** Gunakan untuk pencarian real-time dan aplikasi RAG dinamis
* **Penanganan kesalahan:** Kembalikan pesan yang sesuai ketika pencarian gagal
* **Batas hasil:** Kembalikan hanya hasil yang paling relevan untuk menghindari luapan konteks

### Untuk pencarian tingkat atas (Metode 2)

* **Konten yang telah diambil sebelumnya:** Gunakan ketika Anda sudah memiliki hasil pencarian
* **Pemrosesan batch:** Ideal untuk memproses beberapa hasil pencarian sekaligus
* **Pengujian:** Sangat baik untuk menguji perilaku sitasi dengan konten yang sudah diketahui

### Praktik terbaik umum

1. **Susun hasil secara efektif:**

   * Gunakan URL sumber yang jelas dan permanen
   * Berikan judul yang deskriptif
   * Pecah konten panjang menjadi blok teks yang logis untuk memberi Claude batas sitasi yang lebih terperinci

2. **Jaga konsistensi:**

   * Gunakan format sumber yang konsisten di seluruh aplikasi Anda
   * Pastikan judul mencerminkan konten secara akurat
   * Jaga format tetap konsisten

3. **Tangani kesalahan dengan baik:** ketika pencarian gagal atau tidak mengembalikan apa pun, kembalikan blok teks biasa yang menjelaskan hasilnya (misalnya, `{"type": "text", "text": "No results found."}`) alih-alih memunculkan kesalahan: Claude menjelaskan hasil kosong tersebut kepada pengguna, dan percakapan berlanjut.

## Keterbatasan

* Blok konten hasil pencarian tersedia di Claude API, Amazon Bedrock, dan Google Cloud.
* Hanya konten teks yang didukung di dalam hasil pencarian (tidak ada gambar atau media lainnya).
* Blok `search_result` hanya dapat muncul dalam pesan pengguna (termasuk di dalam hasil alat). Pesan asisten dengan hasil pencarian akan ditolak.
* Ketika [alat pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) diaktifkan dalam permintaan yang sama, sitasi harus diaktifkan pada semua blok `search_result`.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penolakan streaming" icon="lock" href="/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals">
    Deteksi dan tangani alasan berhenti karena penolakan dalam respons streaming, dan coba ulang permintaan yang ditolak pada model cadangan.
  </Card>

  <Card title="Sitasi" icon="book" href="/docs/id/build-with-claude/citations">
    Landaskan respons Claude pada dokumen sumber Anda. Sitasi mengembalikan bagian teks persis yang mendukung setiap klaim, sehingga Anda dapat memverifikasi jawaban dan menampilkan sumber kepada pengguna Anda.
  </Card>

  <Card title="Alat pencarian web" icon="browser" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Beri Claude akses ke konten web terkini dengan sumber yang dikutip, pemfilteran dinamis opsional, dan kontrol domain.
  </Card>

  <Card title="Referensi Messages API" icon="code" href="/docs/id/api/messages/create">
    Lihat dokumentasi Messages API lengkap, termasuk tipe blok konten.
  </Card>

  <Card title="Caching prompt" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Simpan hasil pencarian dalam cache dengan `cache_control` untuk mengurangi biaya dan latensi pada permintaan berulang.
  </Card>
</CardGroup>
