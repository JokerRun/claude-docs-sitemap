---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: b8048cd2892d433568772e7de3308741c0830c3df7d83aa12a3ca79fde88545c
---

# Penggunaan alat ketat

Terapkan kepatuhan JSON Schema pada input alat Claude dengan grammar-constrained sampling.

---

Mengatur `strict: true` pada definisi alat menjamin input alat Claude sesuai dengan JSON Schema Anda dengan membatasi sampling token model ke output yang valid terhadap skema (teknik yang disebut "grammar-constrained sampling" atau sampling yang dibatasi tata bahasa). Halaman ini membahas mengapa mode ketat penting untuk agen, cara mengaktifkannya, dan kasus penggunaan umum. Untuk subset JSON Schema yang didukung, lihat [batasan JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Untuk panduan skema non-ketat, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools).

Penggunaan alat ketat memvalidasi parameter alat, memastikan Claude memanggil fungsi Anda dengan argumen yang bertipe benar. Gunakan penggunaan alat ketat ketika Anda perlu:

* Memvalidasi parameter alat
* Membangun alur kerja agentik
* Memastikan pemanggilan fungsi yang type-safe
* Menangani alat kompleks dengan properti bersarang

## Mengapa penggunaan alat ketat penting untuk agen

Membangun sistem agentik yang andal memerlukan jaminan kesesuaian skema. Tanpa mode ketat, Claude mungkin mengembalikan tipe yang tidak kompatibel (`"2"` alih-alih `2`) atau menghilangkan field yang wajib, merusak fungsi Anda dan menyebabkan error runtime.

Penggunaan alat ketat menjamin parameter yang type-safe:

* Fungsi menerima argumen yang bertipe benar setiap saat
* Tidak perlu memvalidasi dan mengulangi pemanggilan alat
* Agen siap produksi yang bekerja secara konsisten dalam skala besar

Sebagai contoh, misalkan sistem pemesanan memerlukan `passengers: int`. Tanpa mode ketat, Claude mungkin memberikan `passengers: "two"` atau `passengers: "2"`. Dengan `strict: true`, respons selalu berisi `passengers: 2`.

## Mulai cepat

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "What is the weather in San Francisco?"}
      ],
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "strict": true,
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["location"],
          "additionalProperties": false
        }
      }]
    }'
  ```

  ```bash CLI
  ant messages create --transform content <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: What is the weather in San Francisco?
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      strict: true
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
          unit:
            type: string
            enum: [celsius, fahrenheit]
        required: [location]
        additionalProperties: false
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "strict": True,  # Enable strict mode
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      },
                      "unit": {
                          "type": "string",
                          "enum": ["celsius", "fahrenheit"],
                          "description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
                      },
                  },
                  "required": ["location"],
                  "additionalProperties": False,
              },
          }
      ],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather like in San Francisco?"
      }
    ],
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        strict: true, // Enable strict mode
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"],
          additionalProperties: false
        }
      }
    ]
  });
  console.log(response.content);
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }],
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              Strict = true,
              InputSchema = new InputSchema(new Dictionary<string, JsonElement>
              {
                  ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                  {
                      ["location"] = new { type = "string", description = "The city and state, e.g. San Francisco, CA" },
                      ["unit"] = new { type = "string", @enum = new[] { "celsius", "fahrenheit" } },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "location" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              }),
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
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			Strict:      anthropic.Bool(true),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  					"unit": map[string]any{
  						"type": "string",
  						"enum": []string{"celsius", "fahrenheit"},
  					},
  				},
  				Required: []string{"location"},
  				ExtraFields: map[string]any{
  					"additionalProperties": false,
  				},
  			}}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  InputSchema schema = InputSchema.builder()
      .properties(
          JsonValue.from(
              Map.of(
                  "location", Map.of(
                      "type", "string",
                      "description", "The city and state, e.g. San Francisco, CA"
                  ),
                  "unit", Map.of(
                      "type", "string",
                      "enum", List.of("celsius", "fahrenheit")
                  )
              )
          )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("What's the weather like in San Francisco?")
      .addTool(
          Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .strict(true)
              .inputSchema(schema)
              .build()
      )
      .build();

  Message response = client.messages().create(params);
  IO.println(response.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'strict' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ],
                      'unit' => [
                          'type' => 'string',
                          'enum' => ['celsius', 'fahrenheit']
                      ]
                  ],
                  'required' => ['location'],
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
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather like in San Francisco?" }
    ],
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"]
            }
          },
          required: ["location"],
          additionalProperties: false
        }
      }
    ]
  )
  puts message.content
  ```
</CodeGroup>

**Format respons:** Blok tool use dengan input yang tervalidasi di `response.content[x].input`

```json Output
{
  "type": "tool_use",
  "name": "get_weather",
  "input": {
    "location": "San Francisco, CA"
  }
}
```

**Jaminan:**

* `input` alat secara ketat mengikuti `input_schema`
* `name` alat selalu valid (dari alat yang disediakan atau alat server)

## Cara kerjanya

<Steps>
  <Step title="Definisikan skema alat Anda">
    Buat skema JSON untuk `input_schema` alat Anda. Skema menggunakan format JSON Schema standar dengan beberapa batasan (lihat [batasan JSON Schema](/docs/id/build-with-claude/structured-outputs#json-schema-limitations)).
  </Step>

  <Step title="Tambahkan strict: true">
    Atur `"strict": true` sebagai properti tingkat atas dalam definisi alat Anda, bersama dengan `name`, `description`, dan `input_schema`.
  </Step>

  <Step title="Tangani pemanggilan alat">
    Ketika Claude menggunakan alat, field `input` dalam blok tool\_use secara ketat mengikuti `input_schema` Anda, dan `name` selalu valid.
  </Step>
</Steps>

## Kasus penggunaan umum

<AccordionGroup>
  <Accordion title="Input alat tervalidasi">
    Pastikan parameter alat sama persis dengan skema Anda:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-4-8",
          "max_tokens": 1024,
          "messages": [
            {"role": "user", "content": "Search for flights to Tokyo departing June 1, 2026"}
          ],
          "tools": [{
            "name": "search_flights",
            "strict": true,
            "input_schema": {
              "type": "object",
              "properties": {
                "destination": {"type": "string"},
                "departure_date": {"type": "string", "format": "date"},
                "passengers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
              },
              "required": ["destination", "departure_date"],
              "additionalProperties": false
            }
          }]
        }'
      ```

      ```bash CLI
      ant messages create <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content: Search for flights to Tokyo departing June 1, 2026
      tools:
        - name: search_flights
          strict: true
          input_schema:
            type: object
            properties:
              destination:
                type: string
              departure_date:
                type: string
                format: date
              passengers:
                type: integer
                enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            required: [destination, departure_date]
            additionalProperties: false
      YAML
      ```

      ```python Python
      client = Anthropic()
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[
              {
                  "role": "user",
                  "content": "Search for flights to Tokyo departing June 1, 2026",
              }
          ],
          tools=[
              {
                  "name": "search_flights",
                  "strict": True,
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "destination": {"type": "string"},
                          "departure_date": {"type": "string", "format": "date"},
                          "passengers": {
                              "type": "integer",
                              "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          },
                      },
                      "required": ["destination", "departure_date"],
                      "additionalProperties": False,
                  },
              }
          ],
      )

      print(response)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const searchFlightsTool: Anthropic.Tool = {
        name: "search_flights",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: { type: "string" },
            departure_date: { type: "string", format: "date" },
            passengers: { type: "integer", enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] }
          },
          required: ["destination", "departure_date"],
          additionalProperties: false
        }
      };

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Search for flights to Tokyo departing June 1, 2026" }],
        tools: [searchFlightsTool]
      });

      console.log(response);
      ```

      ```csharp C#
      using System.Text.Json;
      using Anthropic;
      using Anthropic.Models.Messages;

      AnthropicClient client = new();

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Search for flights to Tokyo departing June 1, 2026" }],
          Tools = [
              new ToolUnion(new Tool()
              {
                  Name = "search_flights",
                  Strict = true,
                  InputSchema = new InputSchema(new Dictionary<string, JsonElement>
                  {
                      ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                      {
                          ["destination"] = new { type = "string" },
                          ["departure_date"] = new { type = "string", format = "date" },
                          ["passengers"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 } },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "departure_date" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  }),
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
      	MaxTokens: 1024,
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Search for flights to Tokyo departing June 1, 2026")),
      	},
      	Tools: []anthropic.ToolUnionParam{
      		{OfTool: &anthropic.ToolParam{
      			Name:   "search_flights",
      			Strict: anthropic.Bool(true),
      			InputSchema: anthropic.ToolInputSchemaParam{
      				Properties: map[string]any{
      					"destination": map[string]any{
      						"type": "string",
      					},
      					"departure_date": map[string]any{
      						"type":   "string",
      						"format": "date",
      					},
      					"passengers": map[string]any{
      						"type": "integer",
      						"enum": []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
      					},
      				},
      				Required: []string{"destination", "departure_date"},
      				ExtraFields: map[string]any{
      					"additionalProperties": false,
      				},
      			}}},
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      InputSchema schema = InputSchema.builder()
          .properties(
              JsonValue.from(
                  Map.of(
                      "destination", Map.of("type", "string"),
                      "departure_date", Map.of("type", "string", "format", "date"),
                      "passengers", Map.of(
                          "type", "integer",
                          "enum", List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
                      )
                  )
              )
          )
          .putAdditionalProperty("required", JsonValue.from(List.of("destination", "departure_date")))
          .putAdditionalProperty("additionalProperties", JsonValue.from(false))
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Search for flights to Tokyo departing June 1, 2026")
          .addTool(
              Tool.builder()
                  .name("search_flights")
                  .strict(true)
                  .inputSchema(schema)
                  .build()
          )
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
      ```

      ```php PHP
      $client = new Client();

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Search for flights to Tokyo departing June 1, 2026']
          ],
          model: 'claude-opus-4-8',
          tools: [
              [
                  'name' => 'search_flights',
                  'strict' => true,
                  'input_schema' => [
                      'type' => 'object',
                      'properties' => [
                          'destination' => ['type' => 'string'],
                          'departure_date' => ['type' => 'string', 'format' => 'date'],
                          'passengers' => [
                              'type' => 'integer',
                              'enum' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                          ]
                      ],
                      'required' => ['destination', 'departure_date'],
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
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          { role: "user", content: "Search for flights to Tokyo departing June 1, 2026" }
        ],
        tools: [
          {
            name: "search_flights",
            strict: true,
            input_schema: {
              type: "object",
              properties: {
                destination: { type: "string" },
                departure_date: { type: "string", format: "date" },
                passengers: {
                  type: "integer",
                  enum: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                }
              },
              required: ["destination", "departure_date"],
              additionalProperties: false
            }
          }
        ]
      )
      puts message
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Alur kerja agentik dengan beberapa alat tervalidasi">
    Bangun agen multilangkah yang andal dengan parameter alat yang terjamin:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-4-8",
          "max_tokens": 1024,
          "messages": [
            {"role": "user", "content": "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026"}
          ],
          "tools": [
            {
              "name": "search_flights",
              "strict": true,
              "input_schema": {
                "type": "object",
                "properties": {
                  "origin": {"type": "string"},
                  "destination": {"type": "string"},
                  "departure_date": {"type": "string", "format": "date"},
                  "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]}
                },
                "required": ["origin", "destination", "departure_date"],
                "additionalProperties": false
              }
            },
            {
              "name": "search_hotels",
              "strict": true,
              "input_schema": {
                "type": "object",
                "properties": {
                  "city": {"type": "string"},
                  "check_in": {"type": "string", "format": "date"},
                  "guests": {"type": "integer", "enum": [1, 2, 3, 4]}
                },
                "required": ["city", "check_in"],
                "additionalProperties": false
              }
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
          content: >-
            Help me plan a trip from New York to Paris for 2 people,
            departing June 1, 2026
      tools:
        - name: search_flights
          strict: true
          input_schema:
            type: object
            properties:
              origin: {type: string}
              destination: {type: string}
              departure_date: {type: string, format: date}
              travelers: {type: integer, enum: [1, 2, 3, 4, 5, 6]}
            required: [origin, destination, departure_date]
            additionalProperties: false
        - name: search_hotels
          strict: true
          input_schema:
            type: object
            properties:
              city: {type: string}
              check_in: {type: string, format: date}
              guests: {type: integer, enum: [1, 2, 3, 4]}
            required: [city, check_in]
            additionalProperties: false
      YAML
      ```

      ```python Python
      client = Anthropic()
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[
              {
                  "role": "user",
                  "content": "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026",
              }
          ],
          tools=[
              {
                  "name": "search_flights",
                  "strict": True,
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "origin": {"type": "string"},
                          "destination": {"type": "string"},
                          "departure_date": {"type": "string", "format": "date"},
                          "travelers": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6]},
                      },
                      "required": ["origin", "destination", "departure_date"],
                      "additionalProperties": False,
                  },
              },
              {
                  "name": "search_hotels",
                  "strict": True,
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "city": {"type": "string"},
                          "check_in": {"type": "string", "format": "date"},
                          "guests": {"type": "integer", "enum": [1, 2, 3, 4]},
                      },
                      "required": ["city", "check_in"],
                      "additionalProperties": False,
                  },
              },
          ],
      )

      print(response)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const tools: Anthropic.Tool[] = [
        {
          name: "search_flights",
          strict: true,
          input_schema: {
            type: "object",
            properties: {
              origin: { type: "string" },
              destination: { type: "string" },
              departure_date: { type: "string", format: "date" },
              travelers: { type: "integer", enum: [1, 2, 3, 4, 5, 6] }
            },
            required: ["origin", "destination", "departure_date"],
            additionalProperties: false
          }
        },
        {
          name: "search_hotels",
          strict: true,
          input_schema: {
            type: "object",
            properties: {
              city: { type: "string" },
              check_in: { type: "string", format: "date" },
              guests: { type: "integer", enum: [1, 2, 3, 4] }
            },
            required: ["city", "check_in"],
            additionalProperties: false
          }
        }
      ];

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content:
              "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026"
          }
        ],
        tools: tools
      });

      console.log(response);
      ```

      ```csharp C#
      using System.Text.Json;
      using Anthropic;
      using Anthropic.Models.Messages;

      AnthropicClient client = new();

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026" }],
          Tools = [
              new ToolUnion(new Tool()
              {
                  Name = "search_flights",
                  Strict = true,
                  InputSchema = new InputSchema(new Dictionary<string, JsonElement>
                  {
                      ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                      {
                          ["origin"] = new { type = "string" },
                          ["destination"] = new { type = "string" },
                          ["departure_date"] = new { type = "string", format = "date" },
                          ["travelers"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4, 5, 6 } },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "origin", "destination", "departure_date" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  }),
              }),
              new ToolUnion(new Tool()
              {
                  Name = "search_hotels",
                  Strict = true,
                  InputSchema = new InputSchema(new Dictionary<string, JsonElement>
                  {
                      ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                      {
                          ["city"] = new { type = "string" },
                          ["check_in"] = new { type = "string", format = "date" },
                          ["guests"] = new { type = "integer", @enum = new[] { 1, 2, 3, 4 } },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "city", "check_in" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  }),
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
      	MaxTokens: 1024,
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026")),
      	},
      	Tools: []anthropic.ToolUnionParam{
      		{OfTool: &anthropic.ToolParam{
      			Name:   "search_flights",
      			Strict: anthropic.Bool(true),
      			InputSchema: anthropic.ToolInputSchemaParam{
      				Properties: map[string]any{
      					"origin":         map[string]any{"type": "string"},
      					"destination":    map[string]any{"type": "string"},
      					"departure_date": map[string]any{"type": "string", "format": "date"},
      					"travelers":      map[string]any{"type": "integer", "enum": []int{1, 2, 3, 4, 5, 6}},
      				},
      				Required: []string{"origin", "destination", "departure_date"},
      				ExtraFields: map[string]any{
      					"additionalProperties": false,
      				},
      			}}},
      		{OfTool: &anthropic.ToolParam{
      			Name:   "search_hotels",
      			Strict: anthropic.Bool(true),
      			InputSchema: anthropic.ToolInputSchemaParam{
      				Properties: map[string]any{
      					"city":     map[string]any{"type": "string"},
      					"check_in": map[string]any{"type": "string", "format": "date"},
      					"guests":   map[string]any{"type": "integer", "enum": []int{1, 2, 3, 4}},
      				},
      				Required: []string{"city", "check_in"},
      				ExtraFields: map[string]any{
      					"additionalProperties": false,
      				},
      			}}},
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      InputSchema flightsSchema = InputSchema.builder()
          .properties(
              JsonValue.from(
                  Map.of(
                      "origin", Map.of("type", "string"),
                      "destination", Map.of("type", "string"),
                      "departure_date", Map.of("type", "string", "format", "date"),
                      "travelers", Map.of("type", "integer", "enum", List.of(1, 2, 3, 4, 5, 6))
                  )
              )
          )
          .putAdditionalProperty("required", JsonValue.from(List.of("origin", "destination", "departure_date")))
          .putAdditionalProperty("additionalProperties", JsonValue.from(false))
          .build();

      InputSchema hotelsSchema = InputSchema.builder()
          .properties(
              JsonValue.from(
                  Map.of(
                      "city", Map.of("type", "string"),
                      "check_in", Map.of("type", "string", "format", "date"),
                      "guests", Map.of("type", "integer", "enum", List.of(1, 2, 3, 4))
                  )
              )
          )
          .putAdditionalProperty("required", JsonValue.from(List.of("city", "check_in")))
          .putAdditionalProperty("additionalProperties", JsonValue.from(false))
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026")
          .addTool(
              Tool.builder()
                  .name("search_flights")
                  .strict(true)
                  .inputSchema(flightsSchema)
                  .build()
          )
          .addTool(
              Tool.builder()
                  .name("search_hotels")
                  .strict(true)
                  .inputSchema(hotelsSchema)
                  .build()
          )
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
      ```

      ```php PHP
      $client = new Client();

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026']
          ],
          model: 'claude-opus-4-8',
          tools: [
              [
                  'name' => 'search_flights',
                  'strict' => true,
                  'input_schema' => [
                      'type' => 'object',
                      'properties' => [
                          'origin' => ['type' => 'string'],
                          'destination' => ['type' => 'string'],
                          'departure_date' => ['type' => 'string', 'format' => 'date'],
                          'travelers' => ['type' => 'integer', 'enum' => [1, 2, 3, 4, 5, 6]]
                      ],
                      'required' => ['origin', 'destination', 'departure_date'],
                      'additionalProperties' => false
                  ]
              ],
              [
                  'name' => 'search_hotels',
                  'strict' => true,
                  'input_schema' => [
                      'type' => 'object',
                      'properties' => [
                          'city' => ['type' => 'string'],
                          'check_in' => ['type' => 'string', 'format' => 'date'],
                          'guests' => ['type' => 'integer', 'enum' => [1, 2, 3, 4]]
                      ],
                      'required' => ['city', 'check_in'],
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
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [
          { role: "user", content: "Help me plan a trip from New York to Paris for 2 people, departing June 1, 2026" }
        ],
        tools: [
          {
            name: "search_flights",
            strict: true,
            input_schema: {
              type: "object",
              properties: {
                origin: { type: "string" },
                destination: { type: "string" },
                departure_date: { type: "string", format: "date" },
                travelers: { type: "integer", enum: [1, 2, 3, 4, 5, 6] }
              },
              required: ["origin", "destination", "departure_date"],
              additionalProperties: false
            }
          },
          {
            name: "search_hotels",
            strict: true,
            input_schema: {
              type: "object",
              properties: {
                city: { type: "string" },
                check_in: { type: "string", format: "date" },
                guests: { type: "integer", enum: [1, 2, 3, 4] }
              },
              required: ["city", "check_in"],
              additionalProperties: false
            }
          }
        ]
      )
      puts message
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

## Retensi data

Penggunaan alat ketat mengompilasi definisi `input_schema` alat menjadi tata bahasa menggunakan pipeline yang sama dengan [structured outputs](/docs/id/build-with-claude/structured-outputs). Skema alat di-cache sementara hingga 24 jam sejak penggunaan terakhir. Prompt dan respons tidak disimpan setelah respons API.

Penggunaan alat ketat memenuhi syarat HIPAA, tetapi **PHI tidak boleh disertakan dalam definisi skema alat**. API menyimpan cache skema yang telah dikompilasi secara terpisah dari konten pesan, dan skema yang di-cache ini tidak menerima perlindungan PHI yang sama seperti prompt dan respons. Jangan sertakan PHI dalam nama properti `input_schema`, nilai `enum`, nilai `const`, atau ekspresi reguler `pattern`. PHI hanya boleh muncul dalam konten pesan (prompt dan respons), di mana PHI dilindungi di bawah perlindungan HIPAA.

Untuk kelayakan ZDR dan HIPAA di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat web fetch" icon="link" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil dan baca konten dari URL tertentu untuk membawa konten web langsung ke dalam konteks Claude.
  </Card>

  <Card title="Penggunaan alat dengan caching prompt" icon="database" href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh giliran untuk mengurangi biaya dan latensi.
  </Card>

  <Card title="Structured outputs" icon="code-brackets" href="/docs/id/build-with-claude/structured-outputs">
    Dapatkan respons JSON tervalidasi menggunakan grammar-constrained sampling yang sama.
  </Card>

  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi yang efektif, dan kendalikan kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
