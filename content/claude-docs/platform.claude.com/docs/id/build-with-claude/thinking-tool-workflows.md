---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 369dd14963fcf48f5a17c688e9a5c62a62b05964d2bee53e999ec06adc4276d8
---

---
title: Thinking dalam alur kerja alat dan multi-giliran
url: https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows
description: Telusuri perjalanan bolak-balik penggunaan alat dua giliran yang lengkap yang mempertahankan blok thinking dengan benar, dan lihat bagaimana interleaved thinking mengubah alurnya.
---

<Note>
  Untuk mempelajari bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku untuk fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Halaman ini menelusuri perjalanan bolak-balik "tool use" (penggunaan alat) dua giliran yang lengkap dengan thinking diaktifkan: Claude berpikir, meminta pemanggilan alat, menerima hasilnya, dan menyelesaikan jawabannya, dengan blok thinking ditangani dengan benar di setiap langkah. Aturan lengkapnya ada di halaman [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking), di [Thinking dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use) dan [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks); halaman ini menunjukkan aturan-aturan tersebut diterapkan dalam kode yang dapat dijalankan.

## Aturan yang diterapkan dalam panduan ini

Setiap tautan mengarah ke pernyataan lengkapnya di halaman Thinking:

* [Batasi pilihan alat ke `auto` atau `none` dalam mode manual](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use): opsi `tool_choice` yang memaksa penggunaan alat mengembalikan error dengan "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled"}`); adaptive thinking mendukung penggunaan alat yang dipaksakan.
* [Pertahankan satu konfigurasi thinking per giliran asisten](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use): loop penggunaan alat adalah satu giliran asisten, jadi ubah konfigurasi hanya di antara giliran.
* [Kirim kembali blok thinking secara lengkap dan tanpa modifikasi](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks): saat Anda mengembalikan hasil alat, blok thinking dari pesan asisten harus ikut dikembalikan bersamanya.
* [Gemakan pesan asisten persis seperti yang diterima](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks): membangun ulang pesan atau menyaring blok `redacted_thinking` akan memicu error 400.

Contoh-contoh ini menggunakan adaptive thinking; pada model yang hanya mendukung pemikiran diperpanjang, ganti dengan `thinking: {type: "enabled", budget_tokens: N}`. Aturan perjalanan bolak-baliknya identik.

## Menelusuri perjalanan bolak-balik penggunaan alat dua giliran

Contoh ini mendefinisikan alat `get_weather`, membiarkan Claude berpikir dan meminta pemanggilan alat, lalu mengembalikan hasil alat bersama dengan giliran asisten yang digemakan persis seperti yang diterima, termasuk blok thinking.

<Steps>
  <Step title="Buat permintaan pertama dengan alat yang tersedia">
    Kirim permintaan dengan adaptive thinking diaktifkan dan alat didefinisikan. Selain parameter `thinking`, ini adalah permintaan [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) standar:

    <CodeGroup>
      ```bash CLI
      ant messages create --transform content <<'YAML'
      model: claude-opus-4-8
      max_tokens: 16000
      thinking:
        type: adaptive
      tools:
        - name: get_weather
          description: Get current weather for a location
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
          content: "What's the weather in Paris?"
      YAML
      ```

      ```python Python

      client = anthropic.Anthropic()

      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }

      # Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      print(response)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      // Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });
      console.log(response);
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [new() { Role = Role.User, Content = "What's the weather in Paris?" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      import com.anthropic.models.messages.ThinkingConfigAdaptive;
      // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(Tool.builder()
                  .name("get_weather")
                  .description("Get current weather for a location")
                  .inputSchema(Tool.InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                          "location", Map.of("type", "string", "description", "City name")
                      )))
                      .required(List.of("location"))
                      .build())
                  .build())
              .addUserMessage("What's the weather in Paris?")
              .build();

          Message response = client.messages().create(params);
          IO.println(response);
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => ['type' => 'string', 'description' => 'City name']
              ],
              'required' => ['location']
          ]
      ];

      $message = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );
      echo $message;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )
      puts message
      ```
    </CodeGroup>
  </Step>

  <Step title="Tangkap array content untuk digemakan kembali">
    Anda akan melihat blok `thinking`, `text`, dan `tool_use` dalam content respons pada eksekusi di mana Claude memilih untuk berpikir (pada permintaan yang lebih sederhana, mode adaptive mungkin melewatkan blok thinking). Jaga array content ini tetap utuh: langkah berikutnya mengirimkannya kembali kata demi kata.

    <Note>
      Untuk melihat teks thinking seperti output ini, tambahkan `display: "summarized"` ke permintaan. Pada model di mana display secara default dihilangkan, termasuk claude-opus-4-8, field `thinking` akan dikembalikan sebagai string kosong dengan hanya `signature` yang terisi. Bagaimanapun juga, gemakan kembali array content tanpa perubahan; lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).
    </Note>

    ```json Output
    {
      "content": [
        {
          "type": "thinking",
          "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
          "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5T...."
        },
        {
          "type": "text",
          "text": "I can help you get the current weather information for Paris. Let me check that for you"
        },
        {
          "type": "tool_use",
          "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
          "name": "get_weather",
          "input": {
            "location": "Paris"
          }
        }
      ]
    }
    ```
  </Step>

  <Step title="Kembalikan hasil alat, dengan menggemakan giliran asisten kata demi kata">
    Jalankan alat di sisi Anda, lalu kirim permintaan kedua yang menambahkan dua pesan ke percakapan. Yang pertama adalah content asisten yang digemakan kembali persis seperti yang diterima, sehingga blok thinking tetap tidak berubah di samping blok `tool_use`. Yang kedua adalah pesan pengguna yang membawa `tool_result`.

    Setiap contoh adalah skrip mandiri: skrip ini mengulangi permintaan pertama, lalu segera mengirim tindak lanjutnya menggunakan respons yang baru saja diterima.

    <CodeGroup>
      ```bash CLI
      # Giliran pertama: tulis array konten asisten (blok thinking dan tool_use,
      # tanda tangan utuh) ke file. Mengalirkan teks hasil model
      # melalui file menjauhkannya dari posisi ekspansi shell nantinya.
      ant messages create --transform content --format jsonl \
        > assistant_content.json <<'YAML'
      model: claude-opus-4-8
      max_tokens: 16000
      thinking:
        type: adaptive
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required: [location]
      messages:
        - role: user
          content: What's the weather in Paris?
      YAML

      # Giliran kedua: jq mengisi dua placeholder null dari file yang ditangkap,
      # sehingga blok kembali persis sebagai pesan asisten. Blok thinking
      # HARUS menyertai blok tool_use. Delimiter berkutip mencegah
      # shell mengekspansi apa pun di dalam isi.
      jq --slurpfile blocks assistant_content.json '
        .messages[1].content = $blocks[0] |
        .messages[2].content[0].tool_use_id =
          ($blocks[0][] | select(.type == "tool_use") | .id)
      ' <<'JSON' | ant messages create
      {
        "model": "claude-opus-4-8",
        "max_tokens": 16000,
        "thinking": {"type": "adaptive"},
        "tools": [{
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }],
        "messages": [
          {"role": "user", "content": "What's the weather in Paris?"},
          {"role": "assistant", "content": null},
          {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": null,
            "content": "Current temperature: 88°F"
          }]}
        ]
      }
      JSON
      ```

      ```python Python

      client = anthropic.Anthropic()
      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      # Ekstrak blok tool use untuk mendapatkan ID-nya bagi tool result
      tool_use_block = next(block for block in response.content if block.type == "tool_use")

      # Panggil API cuaca Anda yang sebenarnya, di sinilah panggilan API Anda yang sebenarnya ditempatkan
      # Anggap saja inilah yang kita terima kembali
      weather_data = {"temperature": 88}

      # Permintaan kedua - Sertakan giliran asisten dan tool result
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[
              {"role": "user", "content": "What's the weather in Paris?"},
              # Kembalikan konten asisten persis seperti yang diterima. Ketika blok thinking
              # ada, blok tersebut harus menyertai blok tool_use.
              {"role": "assistant", "content": response.content},
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": tool_use_block.id,
                          "content": f"Current temperature: {weather_data['temperature']}°F",
                      }
                  ],
              },
          ],
      )
      print(continuation)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });

      // Ekstrak blok tool_use untuk mendapatkan ID-nya bagi tool_result
      const toolUseBlock = response.content.find(
        (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
      );

      // Panggil API cuaca Anda yang sebenarnya, di sinilah panggilan API Anda yang sebenarnya ditempatkan
      // Anggap saja inilah yang kita terima kembali
      const weatherData = { temperature: 88 };

      if (toolUseBlock) {
        // Permintaan kedua - Sertakan giliran asisten dan tool_result
        const continuation = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 16000,
          thinking: {
            type: "adaptive"
          },
          tools: [weatherTool],
          messages: [
            { role: "user", content: "What's the weather in Paris?" },
            // Kembalikan konten asisten persis seperti yang diterima. Ketika blok thinking
            // ada, blok tersebut harus menyertai blok tool_use.
            { role: "assistant", content: response.content },
            {
              role: "user",
              content: [
                {
                  type: "tool_result" as const,
                  tool_use_id: toolUseBlock.id,
                  content: `Current temperature: ${weatherData.temperature}°F`
                }
              ]
            }
          ]
        });
        console.log(continuation);
      }
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" }
          ]
      };

      var response = await client.Messages.Create(parameters);

      // Ekstrak blok tool_use untuk mendapatkan ID-nya bagi hasil alat
      ToolUseBlock? toolUseBlock = null;
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              toolUseBlock = toolUse;
              break;
          }
      }

      var weatherData = new { temperature = 88 };

      // Bangun kelanjutan dengan hasil alat
      var continuationParams = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" },
              // response.Content mencakup blok thinking; mengirimkannya kembali wajib dilakukan
              new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
              new() { Role = Role.User, Content = new MessageParamContent(new List<ContentBlockParam>
              {
                  new ContentBlockParam(new ToolResultBlockParam()
                  {
                      ToolUseID = toolUseBlock?.ID ?? "",
                      Content = $"Current temperature: {weatherData.temperature}°F"
                  })
              })}
          ]
      };

      var continuation = await client.Messages.Create(continuationParams);
      Console.WriteLine(continuation);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      var toolUseBlock anthropic.ToolUseBlock
      for _, block := range response.Content {
      	if v, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
      		toolUseBlock = v
      		break
      	}
      }

      weatherData := map[string]int{"temperature": 88}

      continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      		response.ToParam(),
      		anthropic.NewUserMessage(
      			anthropic.NewToolResultBlock(toolUseBlock.ID, fmt.Sprintf("Current temperature: %d°F", weatherData["temperature"]), false),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Println(continuation)
      ```

      ```java Java
      import com.anthropic.models.messages.ThinkingConfigAdaptive;
      // ...

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          Tool weatherTool = Tool.builder()
              .name("get_weather")
              .description("Get current weather for a location")
              .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of("type", "string", "description", "City name")
                  )))
                  .required(List.of("location"))
                  .build())
              .build();

          MessageCreateParams initialParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .build();

          Message response = client.messages().create(initialParams);

          ToolUseBlock toolUseBlock = null;
          for (var block : response.content()) {
              if (block.toolUse().isPresent()) {
                  toolUseBlock = block.toolUse().get();
                  break;
              }
          }

          int temperature = 88;

          // Permintaan kedua: kirim ulang giliran asisten sebagaimana diterima, lalu hasil alat
          MessageCreateParams continuationParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .addMessage(response)
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofToolResult(
                      ToolResultBlockParam.builder()
                          .toolUseId(toolUseBlock.id())
                          .content("Current temperature: " + temperature + "°F")
                          .build()
                  )
              ))
              .build();

          Message continuation = client.messages().create(continuationParams);
          IO.println(continuation);
      }
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'City name'
                  ]
              ],
              'required' => ['location']
          ]
      ];

      $response = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );

      $toolUseBlock = null;
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolUseBlock = $block;
              break;
          }
      }

      $weatherData = ['temperature' => 88];

      $continuation = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"],
              ['role' => 'assistant', 'content' => $response->content],
              ['role' => 'user', 'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUseBlock->id,
                      'content' => "Current temperature: {$weatherData['temperature']}°F"
                  ]
              ]]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );

      echo $continuation;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )

      tool_use_block = response.content.find { |block| block.type == :tool_use }

      raise "No tool_use block found" unless tool_use_block

      weather_data = { temperature: 88 }

      continuation = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" },
          { role: "assistant", content: response.content },
          { role: "user", content: [
            {
              type: "tool_result",
              tool_use_id: tool_use_block.id,
              content: "Current temperature: #{weather_data[:temperature]}°F"
            }
          ] }
        ]
      )

      puts continuation
      ```
    </CodeGroup>
  </Step>

  <Step title="Baca respons akhir">
    Anda akan melihat Claude menyelesaikan giliran dengan teks. Karena [interleaved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) bersifat otomatis dalam mode adaptive, kelanjutannya juga dapat dibuka dengan blok thinking baru sebelum teks akhir:

    ```json Output
    {
      "content": [
        {
          "type": "text",
          "text": "Currently in Paris, the temperature is 88°F (31°C)"
        }
      ]
    }
    ```
  </Step>
</Steps>

## Bagaimana interleaved thinking mengubah alur

"Interleaved thinking" (pemikiran berselang-seling) memungkinkan Claude berpikir di antara pemanggilan alat, bernalar tentang setiap hasil alat sebelum menindaklanjutinya. Konsep dan ketersediaan per model dibahas di [Interleaved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) pada halaman Thinking; interleaving mengubah di mana blok thinking muncul, bukan apakah pemanggilan alat dapat dirangkai. Perbandingan berikut menunjukkan apa yang diubah oleh interleaved thinking dalam alur kerja dua alat:

<AccordionGroup>
  <Accordion title="Penggunaan alat tanpa interleaved thinking">
    Tanpa interleaved thinking, Claude berpikir sekali di awal giliran asisten. Respons berikutnya setelah hasil alat berlanjut tanpa blok thinking baru.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Response 1: [thinking] "I need to calculate 150 * $50, then check the database..."
                [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Response 2: [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
                ↑ no thinking block
      ↓ tool result: "5200"

    Response 3: [text] "The total revenue is $7,500, which is 44% above your
                average monthly revenue of $5,200."
                ↑ no thinking block
    ```
  </Accordion>

  <Accordion title="Penggunaan alat dengan interleaved thinking">
    Dengan interleaved thinking diaktifkan, Claude dapat berpikir setelah menerima setiap hasil alat, memungkinkannya bernalar tentang hasil antara sebelum melanjutkan.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Response 1: [thinking] "I need to calculate 150 * $50 first..."
                [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Response 2: [thinking] "Got $7,500. Now I should query the database to compare..."
                [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
                ↑ thinking after receiving calculator result
      ↓ tool result: "5200"

    Response 3: [thinking] "$7,500 vs $5,200 average - that's a 44% increase..."
                [text] "The total revenue is $7,500, which is 44% above your
                average monthly revenue of $5,200."
                ↑ thinking before final answer
    ```
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Ikhtisarnya: aktifkan thinking, baca output thinking, dan tinjau aturan lengkap untuk penggunaan alat, caching, dan streaming.
  </Card>

  <Card title="Mengarahkan thinking" icon="compass" href="https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost">
    Arahkan seberapa sering dan seberapa dalam Claude berpikir dengan tingkat effort dan panduan berbasis prompt.
  </Card>

  <Card title="Pemikiran diperpanjang" icon="clock" href="https://platform.claude.com/docs/id/build-with-claude/extended-thinking">
    Anggaran thinking manual pada model lama: mekanisme `budget_tokens` dan migrasi ke adaptive.
  </Card>
</CardGroup>
