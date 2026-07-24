---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 763bcfad45b9ae483dae7349318d7c41c528f44421f5d9e8fe01f9c61407f961
---

# Penggunaan alat dengan Claude

Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang cocok untuk tugas Anda.

---

"Tool use" (penggunaan alat) memungkinkan Claude memanggil fungsi yang Anda definisikan atau yang disediakan oleh Anthropic. Claude menentukan kapan harus memanggil alat berdasarkan permintaan pengguna dan deskripsi alat tersebut. Kemudian Claude mengembalikan panggilan terstruktur yang dieksekusi oleh aplikasi Anda (alat klien) atau yang dieksekusi oleh Anthropic (alat server).

Berikut adalah contoh minimal menggunakan alat server, yaitu [alat Web search](/docs/id/agents-and-tools/tool-use/web-search-tool), yang dieksekusi oleh Anthropic untuk Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [{"type": "web_search_20260209", "name": "web_search"}],
      "messages": [{"role": "user", "content": "What'\''s the latest on the Mars rover?"}]
    }'
  ```

  ```bash CLI
  ant messages create --transform content --format yaml \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --tool '{type: web_search_20260209, name: web_search}' \
    --message '{role: user, content: "What is the latest on the Mars rover?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[{"type": "web_search_20260209", "name": "web_search"}],
      messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [{ type: "web_search_20260209", name: "web_search" }],
    messages: [{ role: "user", content: "What's the latest on the Mars rover?" }]
  });
  console.log(response.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = [new ToolUnion(new WebSearchTool20260209())],
      Messages = [new() { Role = Role.User, Content = "What's the latest on the Mars rover?" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message.Content);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfWebSearchTool20260209: &anthropic.WebSearchTool20260209Param{}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the latest on the Mars rover?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  import com.anthropic.models.messages.WebSearchTool20260209;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(WebSearchTool20260209.builder().build())
          .addUserMessage("What's the latest on the Mars rover?")
          .build();

      Message response = client.messages().create(params);
      IO.println(response.content());
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: [
          ['type' => 'web_search_20260209', 'name' => 'web_search'],
      ],
      messages: [
          ['role' => 'user', 'content' => "What's the latest on the Mars rover?"],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [{ type: "web_search_20260209", name: "web_search" }],
    messages: [{ role: "user", content: "What's the latest on the Mars rover?" }]
  )
  puts message.content
  ```
</CodeGroup>

Claude menjalankan pencarian di infrastruktur Anthropic dan mengembalikan hasil yang disertai kutipan dalam respons yang sama. Agar Claude memanggil fungsi yang Anda definisikan, kirimkan alat dengan `input_schema`, lalu eksekusi panggilan tersebut ketika Claude mengembalikan blok `tool_use`. [Cara kerja penggunaan alat](#how-tool-use-works) menunjukkan perjalanan bolak-balik tersebut dari awal hingga akhir. Pelajari lebih lanjut tentang [mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) dan [menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Cara kerja penggunaan alat

Alat terutama berbeda berdasarkan di mana kode dieksekusi. **Alat klien** (termasuk alat yang didefinisikan pengguna dan alat dengan skema yang didefinisikan Anthropic, seperti `bash` dan `text_editor`) berjalan di aplikasi Anda. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`. Kode Anda mengeksekusi operasi tersebut dan mengirimkan kembali `tool_result`. **Alat server** (seperti `web_search`, `web_fetch`, `code_execution`, dan `tool_search`) berjalan di infrastruktur Anthropic: Anda melihat hasilnya secara langsung tanpa menangani eksekusi, kecuali Claude memanggil alat tersebut dalam kelompok panggilan alat paralel yang sama dengan salah satu alat klien Anda (lihat [Stop reasons dan fallback](/docs/id/build-with-claude/handling-stop-reasons#tool-use)).

Berikut adalah perjalanan bolak-balik lengkap untuk alat klien. Permintaan pertama mendefinisikan alat `get_weather`, dan Claude menjawab pertanyaan dengan memanggilnya: respons membawa blok `tool_use`, kode Anda menjalankan pencarian, dan permintaan kedua mengirimkan hasilnya kembali dalam blok `tool_result` sehingga Claude dapat membalas dengan jawabannya.

<CodeGroup>
  ```bash cURL
  # Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
  TOOLS='[
    {
      "name": "get_weather",
      "description": "Get the current weather for a given location.",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "City and state, e.g. San Francisco, CA"}
        },
        "required": ["location"]
      }
    }
  ]'
  USER_MSG="What's the weather in San Francisco?"
  RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n --argjson tools "$TOOLS" --arg msg "$USER_MSG" '{
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: $tools,
      # Minta paling banyak satu pemanggilan alat per giliran.
      tool_choice: {type: "auto", disable_parallel_tool_use: true},
      messages: [{role: "user", content: $msg}]
    }')")
  TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
  echo "Claude called $(echo "$TOOL_USE" | jq -r '.name') with $(echo "$TOOL_USE" | jq -c '.input')"

  # Jalankan alatnya, lalu kirim kembali hasilnya dalam blok tool_result.
  WEATHER="15 degrees Celsius, partly cloudy"
  FOLLOWUP=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n \
      --argjson tools "$TOOLS" \
      --arg msg "$USER_MSG" \
      --argjson assistant "$(echo "$RESPONSE" | jq '.content')" \
      --arg tool_use_id "$(echo "$TOOL_USE" | jq -r '.id')" \
      --arg weather "$WEATHER" \
      '{
        model: "claude-opus-4-8",
        max_tokens: 1024,
        tools: $tools,
        tool_choice: {type: "auto", disable_parallel_tool_use: true},
        messages: [
          {role: "user", content: $msg},
          {role: "assistant", content: $assistant},
          {role: "user", content: [
            {type: "tool_result", tool_use_id: $tool_use_id, content: $weather}
          ]}
        ]
      }')")

  # Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  echo "$FOLLOWUP" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  # ant membaca body permintaan sebagai YAML dari stdin; jq membawa status
  # percakapan ke dalam permintaan kedua.
  USER_MSG="What's the weather in San Francisco?"
  MESSAGES=$(jq -n --arg msg "$USER_MSG" '[{role: "user", content: $msg}]')
  call_api() {
    {
      cat <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  # Minta paling banyak satu panggilan alat per giliran.
  tool_choice: {type: auto, disable_parallel_tool_use: true}
  tools:
    - name: get_weather
      description: Get the current weather for a given location.
      input_schema:
        type: object
        properties:
          location: {type: string, description: "City and state, e.g. San Francisco, CA"}
        required: [location]
  YAML
      printf 'messages: %s\n' "$MESSAGES"
    } | ant messages create --format json
  }

  # Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
  RESPONSE=$(call_api)
  TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
  echo "Claude called $(jq -r '.name' <<<"$TOOL_USE") with $(jq -c '.input' <<<"$TOOL_USE")"

  # Jalankan alat tersebut, lalu kirim kembali hasilnya dalam blok tool_result.
  WEATHER="15 degrees Celsius, partly cloudy"
  MESSAGES=$(jq \
    --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
    --arg tool_use_id "$(jq -r '.id' <<<"$TOOL_USE")" \
    --arg weather "$WEATHER" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: [
        {type: "tool_result", tool_use_id: $tool_use_id, content: $weather}
      ]}
    ]' <<<"$MESSAGES")
  FOLLOWUP=$(call_api)

  # Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  jq -r '.content[] | select(.type == "text") | .text' <<<"$FOLLOWUP"
  ```

  ```python Python
  client = anthropic.Anthropic()

  tools = [
      {
          "name": "get_weather",
          "description": "Get the current weather for a given location.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "location": {
                      "type": "string",
                      "description": "City and state, e.g. San Francisco, CA",
                  }
              },
              "required": ["location"],
          },
      }
  ]
  messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]

  # Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=tools,
      # Minta paling banyak satu pemanggilan alat per giliran.
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=messages,
  )
  tool_use = next(block for block in response.content if block.type == "tool_use")
  print(f"Claude called {tool_use.name} with {json.dumps(tool_use.input)}")

  # Jalankan alatnya, lalu kirim kembali hasilnya dalam blok tool_result.
  weather = "15 degrees Celsius, partly cloudy"  # your weather lookup goes here
  messages += [
      {"role": "assistant", "content": response.content},
      {
          "role": "user",
          "content": [
              {"type": "tool_result", "tool_use_id": tool_use.id, "content": weather}
          ],
      },
  ]
  followup = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=messages,
  )

  # Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  final_text = next(block for block in followup.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const tools: Anthropic.Tool[] = [
    {
      name: "get_weather",
      description: "Get the current weather for a given location.",
      input_schema: {
        type: "object",
        properties: {
          location: { type: "string", description: "City and state, e.g. San Francisco, CA" }
        },
        required: ["location"]
      }
    }
  ];
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "What's the weather in San Francisco?" }
  ];

  // Claude membalas dengan blok tool_use yang menyebutkan nama alat beserta argumennya.
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools,
    // Minta paling banyak satu pemanggilan alat per giliran.
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages
  });
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
  )!;
  console.log(`Claude called ${toolUse.name} with ${JSON.stringify(toolUse.input)}`);

  // Jalankan alatnya, lalu kirim kembali hasilnya dalam blok tool_result.
  const weather = "15 degrees Celsius, partly cloudy"; // your weather lookup goes here
  messages.push(
    { role: "assistant", content: response.content },
    {
      role: "user",
      content: [{ type: "tool_result", tool_use_id: toolUse.id, content: weather }]
    }
  );
  const followup = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages
  });

  // Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  const finalText = followup.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  )!;
  console.log(finalText.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get the current weather for a given location.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "string",
                      description = "City and state, e.g. San Francisco, CA",
                  }),
              },
              Required = ["location"],
          },
      }),
  ];

  // Minta paling banyak satu pemanggilan alat per giliran.
  var toolChoice = new ToolChoice(new ToolChoiceAuto { DisableParallelToolUse = true });

  const string userPrompt = "What's the weather in San Francisco?";

  // Claude membalas dengan blok tool_use yang menyebutkan nama alat beserta argumennya.
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages = [new() { Role = Role.User, Content = userPrompt }],
  });
  ToolUseBlock? toolUse = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var picked))
      {
          toolUse = picked;
          break;
      }
  }
  Console.WriteLine($"Claude called {toolUse!.Name} with {JsonSerializer.Serialize(toolUse.Input)}");

  // Jalankan alat tersebut, lalu kirim kembali hasilnya dalam blok tool_result.
  var weather = "15 degrees Celsius, partly cloudy";
  List<ContentBlockParam> toolResults =
  [
      new ContentBlockParam(new ToolResultBlockParam()
      {
          ToolUseID = toolUse.ID,
          Content = weather,
      }),
  ];
  var followup = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages =
      [
          new() { Role = Role.User, Content = userPrompt },
          new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
          new() { Role = Role.User, Content = new MessageParamContent(toolResults) },
      ],
  });

  // Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  foreach (var block in followup.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  tools := []anthropic.ToolUnionParam{
  	{OfTool: &anthropic.ToolParam{
  		Name:        "get_weather",
  		Description: anthropic.String("Get the current weather for a given location."),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"location": map[string]any{
  					"type":        "string",
  					"description": "City and state, e.g. San Francisco, CA",
  				},
  			},
  			Required: []string{"location"},
  		},
  	}},
  }
  // Minta paling banyak satu pemanggilan alat per giliran.
  toolChoice := anthropic.ToolChoiceUnionParam{
  	OfAuto: &anthropic.ToolChoiceAutoParam{DisableParallelToolUse: anthropic.Bool(true)},
  }
  messages := []anthropic.MessageParam{
  	anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in San Francisco?")),
  }

  // Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
  response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeOpus4_8,
  	MaxTokens:  1024,
  	Tools:      tools,
  	ToolChoice: toolChoice,
  	Messages:   messages,
  })
  if err != nil {
  	log.Fatal(err)
  }
  var toolUse anthropic.ContentBlockUnion
  for _, block := range response.Content {
  	if block.Type == "tool_use" {
  		toolUse = block
  		break
  	}
  }
  fmt.Printf("Claude called %s with %s\n", toolUse.Name, string(toolUse.Input))

  // Jalankan alat tersebut, lalu kirim kembali hasilnya dalam blok tool_result.
  weather := "15 degrees Celsius, partly cloudy"
  var assistantContent []anthropic.ContentBlockParamUnion
  for _, block := range response.Content {
  	assistantContent = append(assistantContent, block.ToParam())
  }
  messages = append(messages,
  	anthropic.NewAssistantMessage(assistantContent...),
  	anthropic.NewUserMessage(anthropic.NewToolResultBlock(toolUse.ID, weather, false)),
  )
  followup, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeOpus4_8,
  	MaxTokens:  1024,
  	Tools:      tools,
  	ToolChoice: toolChoice,
  	Messages:   messages,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  for _, block := range followup.Content {
  	if block.Type == "text" {
  		fmt.Println(block.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlockParam;
  // ...
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoiceAuto;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool weatherTool = Tool.builder()
          .name("get_weather")
          .description("Get the current weather for a given location.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "location", Map.of(
                      "type", "string",
                      "description", "City and state, e.g. San Francisco, CA"
                  )
              )))
              .required(List.of("location"))
              .build())
          .build();

      // Minta paling banyak satu pemanggilan alat per giliran.
      ToolChoiceAuto toolChoice = ToolChoiceAuto.builder()
          .disableParallelToolUse(true)
          .build();

      String userPrompt = "What's the weather in San Francisco?";

      // Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(weatherTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .build());
      ToolUseBlock toolUse = response.content().stream()
          .flatMap(block -> block.toolUse().stream())
          .findFirst()
          .orElseThrow();
      IO.println("Claude called " + toolUse.name() + " with " + toolUse._input());

      // Jalankan alat tersebut, lalu kirim kembali hasilnya dalam blok tool_result.
      String weather = "15 degrees Celsius, partly cloudy";
      Message followup = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(weatherTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .addMessage(response)
          .addUserMessageOfBlockParams(List.of(ContentBlockParam.ofToolResult(
              ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  .content(weather)
                  .build())))
          .build());

      // Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
      followup.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Messages\ToolChoiceAuto;

  $client = new Client();

  $tools = [
      [
          'name' => 'get_weather',
          'description' => 'Get the current weather for a given location.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'City and state, e.g. San Francisco, CA',
                  ],
              ],
              'required' => ['location'],
          ],
      ],
  ];
  $userMessage = ['role' => 'user', 'content' => "What's the weather in San Francisco?"];

  // Minta paling banyak satu panggilan alat per giliran.
  $toolChoice = ToolChoiceAuto::with(disableParallelToolUse: true);

  // Claude membalas dengan blok tool_use yang menyebutkan alat dan argumennya.
  $response = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [$userMessage],
  );
  $toolUse = null;
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolUse = $block;
          break;
      }
  }
  printf("Claude called %s with %s\n", $toolUse->name, json_encode($toolUse->input));

  // Jalankan alat tersebut, lalu kirim kembali hasilnya dalam blok tool_result.
  $weather = '15 degrees Celsius, partly cloudy';
  $followup = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [
          $userMessage,
          ['role' => 'assistant', 'content' => $response->content],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUse->id,
                      'content' => $weather,
                  ],
              ],
          ],
      ],
  );

  // Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  foreach ($followup->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tools = [
    {
      name: "get_weather",
      description: "Get the current weather for a given location.",
      input_schema: {
        type: "object",
        properties: {
          location: {type: "string", description: "City and state, e.g. San Francisco, CA"}
        },
        required: ["location"]
      }
    }
  ]
  messages = [{role: "user", content: "What's the weather in San Francisco?"}]

  # Claude membalas dengan blok tool_use yang menyebutkan nama alat dan argumennya.
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    # Minta paling banyak satu pemanggilan alat per giliran.
    tool_choice: {type: "auto", disable_parallel_tool_use: true},
    messages: messages
  )
  tool_use = response.content.find { |block| block.type == :tool_use }
  puts "Claude called #{tool_use.name} with #{JSON.generate(tool_use.input)}"

  # Jalankan alatnya, lalu kirim kembali hasilnya dalam blok tool_result.
  weather = "15 degrees Celsius, partly cloudy"
  messages += [
    {role: "assistant", content: response.content},
    {
      role: "user",
      content: [
        {type: "tool_result", tool_use_id: tool_use.id, content: weather}
      ]
    }
  ]
  followup = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: {type: "auto", disable_parallel_tool_use: true},
    messages: messages
  )

  # Claude menggunakan hasil tersebut untuk menjawab pertanyaan awal.
  final_text = followup.content.find { |block| block.type == :text }
  puts final_text.text
  ```
</CodeGroup>

```text Output wrap
Claude called get_weather with {"location": "San Francisco, CA"}
The current weather in San Francisco is 15 degrees Celsius with partly cloudy skies.
```

[Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) membahas setiap langkah secara rinci, termasuk pemformatan hasil dan pemberian sinyal kesalahan; [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use) membahas respons yang memanggil beberapa alat sekaligus. Untuk melewati penulisan perjalanan bolak-balik ini sendiri, gunakan [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner): SDK akan mengeksekusi alat Anda dan mengirimkan hasilnya kembali secara otomatis.

Untuk model konseptual lengkap termasuk loop agentik dan kapan harus memilih setiap pendekatan, lihat [Cara kerja penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Untuk terhubung ke server Model Context Protocol (MCP), lihat [konektor MCP](/docs/id/agents-and-tools/mcp-connector). Untuk membangun klien MCP Anda sendiri, lihat panduan Model Context Protocol tentang [membangun klien MCP](https://modelcontextprotocol.io/docs/develop/build-client).

## Kapan Claude menggunakan alat

Dengan `tool_choice` default `{"type": "auto"}`, Claude menentukan pada setiap giliran apakah akan memanggil alat atau merespons secara langsung. Claude memanggil alat ketika permintaan sesuai dengan kemampuan yang dideskripsikan alat tersebut dan jawabannya belum ada dalam konteks. Claude merespons secara langsung untuk pengetahuan yang stabil, tugas kreatif, dan giliran percakapan.

Batasan ini dapat diarahkan melalui prompt sistem Anda. Jika Claude tidak memanggil alat ketika Anda mengharapkannya, instruksi ringan seperti `"Use the tools to investigate before responding."` akan meningkatkan penggunaan alat. Bentuk yang lebih kuat seperti `"Always call a tool first before responding."` mendorong lebih jauh. Sebaliknya, `"Use your judgment about whether to call a tool or respond directly."` menjaga perilaku pemicu tetap konservatif.

Untuk mewajibkan panggilan alat alih-alih mengandalkan prompting, atur [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).

<Tip>
  **Jamin kesesuaian skema dengan strict tool use**

  Tambahkan `strict: true` ke definisi alat kustom Anda untuk memastikan panggilan alat Claude selalu cocok persis dengan skema Anda. Lihat [Strict tool use](/docs/id/agents-and-tools/tool-use/strict-tool-use).
</Tip>

Halaman setiap alat server mendeskripsikan batasan pemicunya sendiri secara lebih rinci.

<Accordion title="Ketika parameter yang diperlukan tidak ada">
  Jika prompt pengguna tidak menyertakan informasi yang cukup untuk mengisi semua parameter yang diperlukan untuk sebuah alat, Claude Opus jauh lebih mungkin untuk mengenali bahwa ada parameter yang hilang dan menanyakannya. Claude Sonnet mungkin bertanya, terutama ketika diminta untuk berpikir sebelum mengeluarkan permintaan alat. Tetapi Claude Sonnet juga mungkin menyimpulkan nilai yang masuk akal.

  Misalnya, dengan alat `get_weather` yang memerlukan parameter `location`, jika Anda bertanya kepada Claude "Bagaimana cuacanya?" tanpa menentukan lokasi, Claude (khususnya Claude Sonnet) mungkin menebak nilai yang tidak Anda berikan:

  ```json JSON
  {
    "type": "tool_use",
    "id": "toolu_01A09q90qw90lq917835lq9",
    "name": "get_weather",
    "input": { "location": "New York, NY", "unit": "fahrenheit" }
  }
  ```

  Perilaku ini tidak dijamin, terutama untuk prompt yang lebih ambigu dan untuk model yang kurang mumpuni.
</Accordion>

## Memilih alat

Untuk string `type`, versi, dan header beta, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

### Alat Anda sendiri

Untuk alat yang Anda definisikan, Anda menulis skemanya dan aplikasi Anda mengeksekusi setiap panggilan.

<CardGroup cols={2}>
  <Card title="Definisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi, dan kendalikan kapan Claude memanggil alat Anda.
  </Card>

  <Card title="Tangani panggilan alat" icon="arrows-left-right" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Parse blok `tool_use`, format respons `tool_result`, dan tangani kesalahan.
  </Card>
</CardGroup>

### Alat klien dengan skema Anthropic

Anthropic menerbitkan skema dan melatih Claude dengannya. Aplikasi Anda tetap mengeksekusi setiap panggilan dan mengembalikan `tool_result`.

<CardGroup cols={2}>
  <Card title="Alat Memory" icon="brain" href="/docs/id/agents-and-tools/tool-use/memory-tool">
    Simpan dan ambil informasi lintas percakapan dalam file yang Anda kendalikan.
  </Card>

  <Card title="Alat Bash" icon="terminal" href="/docs/id/agents-and-tools/tool-use/bash-tool">
    Jalankan perintah shell dalam sesi persisten yang mempertahankan state.
  </Card>

  <Card title="Alat Text editor" icon="edit" href="/docs/id/agents-and-tools/tool-use/text-editor-tool">
    Lihat dan modifikasi file teks untuk men-debug, memperbaiki, dan meningkatkan kode.
  </Card>

  <Card title="Alat Computer use" icon="computer" href="/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Ambil tangkapan layar dan kendalikan mouse serta keyboard di lingkungan desktop.
  </Card>
</CardGroup>

### Alat server

Alat server berjalan di infrastruktur Anthropic, tanpa kode handler di aplikasi Anda. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) untuk mekanisme yang mereka bagikan.

<CardGroup cols={2}>
  <Card title="Alat Web search" icon="browser" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Cari informasi di web di luar batas pengetahuan, dengan sumber yang dikutip.
  </Card>

  <Card title="Alat Web fetch" icon="download" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.
  </Card>

  <Card title="Alat Code execution" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam kontainer sandbox untuk menganalisis data dan menghasilkan file.
  </Card>

  <Card title="Alat Advisor" icon="lightbulb" href="/docs/id/agents-and-tools/tool-use/advisor-tool">
    Biarkan model eksekutor yang lebih cepat berkonsultasi dengan model penasihat berintelegensi lebih tinggi di tengah proses generasi.
  </Card>

  <Card title="Alat Tool search" icon="library" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Bekerja dengan ribuan alat dengan menemukan dan memuatnya sesuai kebutuhan.
  </Card>

  <Card title="Konektor MCP" icon="link" href="/docs/id/agents-and-tools/mcp-connector">
    Hubungkan ke server MCP jarak jauh dari Messages API tanpa klien MCP terpisah.
  </Card>
</CardGroup>

<Note>
  [Claude Managed Agents](/docs/id/managed-agents/overview) menyediakan kumpulan alat bawaan yang digunakan Claude secara otonom dalam sebuah sesi. Untuk kumpulan alat tersebut dan cara Managed Agents menambahkan alat kustom, lihat halaman [Tools](/docs/id/managed-agents/tools)-nya.
</Note>

## Harga

Permintaan penggunaan alat dikenakan biaya berdasarkan:

1. Jumlah total token input yang dikirim ke model (termasuk dalam parameter `tools`)
2. Jumlah token output yang dihasilkan
3. Untuk alat sisi server, biaya tambahan berbasis penggunaan (misalnya, pencarian web dikenakan biaya per pencarian yang dilakukan)

Alat sisi klien dikenakan biaya yang sama seperti permintaan API Claude lainnya, sedangkan alat sisi server dapat dikenakan biaya tambahan berdasarkan penggunaan spesifiknya.

Token tambahan dari penggunaan alat berasal dari:

* Parameter `tools` dalam permintaan API (nama alat, deskripsi, dan skema)
* Blok konten `tool_use` dalam permintaan dan respons API
* Blok konten `tool_result` dalam permintaan API

Ketika Anda menggunakan `tools`, API juga secara otomatis menyertakan prompt sistem khusus untuk model yang mengaktifkan penggunaan alat. Jumlah token penggunaan alat yang diperlukan untuk setiap model tercantum di bawah ini (tidak termasuk token tambahan yang tercantum di atas). Perhatikan bahwa tabel ini mengasumsikan setidaknya 1 alat disediakan. Jika tidak ada `tools` yang disediakan, maka pilihan alat `none` menggunakan 0 token prompt sistem tambahan.

| Model                                                                                                          | Pilihan alat                   | Jumlah token prompt sistem penggunaan alat |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------ |
| Claude Opus 4.8                                                                                                | `auto`, `none`***`any`, `tool` | 290 token***410 token                      |
| Claude Opus 4.7                                                                                                | `auto`, `none`***`any`, `tool` | 675 token***804 token                      |
| Claude Opus 4.6                                                                                                | `auto`, `none`***`any`, `tool` | 497 token***589 token                      |
| Claude Opus 4.5                                                                                                | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations))                             | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Opus 4 ([dihentikan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations))                | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Sonnet 5                                                                                                | `auto`, `none`***`any`, `tool` | 354 token***474 token                      |
| Claude Sonnet 4.6                                                                                              | `auto`, `none`***`any`, `tool` | 497 token***589 token                      |
| Claude Sonnet 4.5                                                                                              | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations))  | `auto`, `none`***`any`, `tool` | 313 token***315 token                      |
| Claude Haiku 4.5                                                                                               | `auto`, `none`***`any`, `tool` | 496 token***588 token                      |
| Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)) | `auto`, `none`***`any`, `tool` | 264 token***355 token                      |

Jumlah token ini ditambahkan ke token input dan output normal Anda untuk menghitung total biaya permintaan.

Lihat tabel [Ikhtisar model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk harga per model terkini.

Ketika Anda mengirim prompt penggunaan alat, seperti permintaan API lainnya, respons menyertakan jumlah token input dan output dalam metrik `usage` yang dilaporkan.

Beberapa alat server menambahkan biaya berbasis penggunaan di atas token: lihat [alat Web search](/docs/id/agents-and-tools/tool-use/web-search-tool#usage-and-pricing) dan [alat Code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk tarifnya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card href="/docs/id/agents-and-tools/tool-use/how-tool-use-works" title="Cara kerja penggunaan alat" icon="compass">
    Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat alih-alih prosa.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Bangun agen yang menggunakan alat" icon="graduation-cap">
    Panduan langkah demi langkah dari satu panggilan alat hingga loop agentik yang siap produksi.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
