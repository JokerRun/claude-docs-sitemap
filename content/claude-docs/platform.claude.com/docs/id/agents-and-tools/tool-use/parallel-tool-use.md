---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 1d182f1317b4d2bd1a56876970fdb2735da04bf24da79118465ad191de73eb8e
---

# Penggunaan alat paralel

Mengaktifkan, memformat, dan menonaktifkan panggilan alat paralel, dengan panduan riwayat pesan dan pemecahan masalah.

---

Secara default, Claude dapat memanggil beberapa alat dalam satu respons. Halaman ini membahas cara menjalankan panggilan tersebut, cara memformat riwayat pesan agar paralelisme tetap berfungsi, dan cara menonaktifkan penggunaan alat paralel saat Anda membutuhkannya. Untuk alur panggilan tunggal, lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

## Semantik eksekusi

Ketika Claude memanggil alat, respons memiliki `stop_reason` berupa `tool_use` dan dapat berisi beberapa blok `tool_use` dalam satu giliran asisten. Cara Anda menjalankan panggilan tersebut adalah keputusan Anda. API tidak menentukan urutan eksekusi: Anda dapat menjalankan panggilan secara bersamaan (`Promise.all`, `asyncio.gather`), secara berurutan sesuai urutan kemunculannya, atau dalam kombinasi apa pun yang sesuai dengan alat Anda.

Pilih strategi berdasarkan apa yang dilakukan alat Anda. Operasi independen yang hanya membaca biasanya aman dijalankan secara paralel untuk "latency" (latensi) yang lebih rendah. Alat dengan efek samping, state bersama, atau persyaratan urutan mungkin lebih baik dijalankan secara berurutan.

Strategi apa pun yang Anda gunakan, kembalikan satu `tool_result` untuk setiap blok `tool_use`, semuanya bersama-sama dalam pesan pengguna berikutnya. Cocokkan setiap hasil dengan panggilannya menggunakan `tool_use_id`, dan letakkan setiap blok `tool_result` sebelum konten teks apa pun dalam pesan tersebut. Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk aturan pemformatan lengkap. Jika Anda memilih untuk tidak menjalankan panggilan tertentu (misalnya, karena Anda menjalankan batch secara berurutan dan panggilan sebelumnya gagal), tetap kembalikan `tool_result` untuknya dengan `is_error: true` dan penjelasan singkat.

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_02",
  "is_error": true,
  "content": "Not executed: the preceding write_file call failed."
}
```

## Menguji panggilan alat paralel

<Note>
  **Gunakan Tool Runner untuk sebagian besar aplikasi:** [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner) SDK menangani respons dengan beberapa panggilan alat dan memformat hasilnya untuk Anda, sehingga Anda tidak perlu menulis penanganan ini sendiri. Gunakan pola manual di halaman ini ketika Anda memerlukan kontrol langsung atas cara panggilan dijalankan, seperti batching kustom, pengurutan, atau penanganan kesalahan.
</Note>

Skrip berikut mengirimkan permintaan yang seharusnya memicu panggilan alat paralel, memverifikasi bahwa respons berisi panggilan tersebut, dan memformat hasil alat agar paralelisme tetap berfungsi. Jalankan dengan `ANTHROPIC_API_KEY` yang diatur di lingkungan Anda:

<CodeGroup>
  ```bash cURL
  # Alur pengujian end-to-end ini tidak cocok diubah menjadi perintah shell sekali jalan.
  # Lihat tab SDK untuk alur lengkapnya. Permintaan HTTP yang mendasarinya adalah permintaan
  # penggunaan alat standar dengan beberapa alat yang didefinisikan.
  ```

  ```bash CLI
  # Alur pengujian end-to-end ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
  # Lihat tab SDK untuk alur lengkapnya.
  ```

  ```python Python
  client = Anthropic()

  # Definisikan alat
  tools = [
      {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
              "type": "object",
              "properties": {
                  "location": {
                      "type": "string",
                      "description": "The city and state, e.g. San Francisco, CA",
                  }
              },
              "required": ["location"],
          },
      },
      {
          "name": "get_time",
          "description": "Get the current time in a given timezone",
          "input_schema": {
              "type": "object",
              "properties": {
                  "timezone": {
                      "type": "string",
                      "description": "The timezone, e.g. America/New_York",
                  }
              },
              "required": ["timezone"],
          },
      },
  ]

  # Uji percakapan dengan pemanggilan alat paralel
  messages = [
      {
          "role": "user",
          "content": "What's the weather in SF and NYC, and what time is it there?",
      }
  ]

  # Buat permintaan awal
  print("Requesting parallel tool calls...")
  response = client.messages.create(
      model="claude-opus-4-8", max_tokens=1024, messages=messages, tools=tools
  )

  # Periksa pemanggilan alat paralel
  tool_uses = [block for block in response.content if block.type == "tool_use"]
  print(f"\n✓ Claude made {len(tool_uses)} tool calls")

  if len(tool_uses) > 1:
      print("✓ Parallel tool calls detected!")
      for tool in tool_uses:
          print(f"  - {tool.name}: {tool.input}")
  else:
      print("✗ No parallel tool calls detected")

  # Simulasikan eksekusi alat dan format hasilnya dengan benar
  tool_results = []
  for tool_use in tool_uses:
      if tool_use.name == "get_weather":
          if "San Francisco" in str(tool_use.input):
              result = "San Francisco: 68°F, partly cloudy"
          else:
              result = "New York: 45°F, clear skies"
      else:  # get_time
          if "Los_Angeles" in str(tool_use.input):
              result = "2:30 PM PST"
          else:
              result = "5:30 PM EST"

      tool_results.append(
          {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
      )

  # Lanjutkan percakapan dengan hasil alat
  messages.extend(
      [
          {"role": "assistant", "content": response.content},
          {"role": "user", "content": tool_results},  # All results in one message!
      ]
  )

  # Dapatkan respons akhir
  print("\nGetting final response...")
  final_response = client.messages.create(
      model="claude-opus-4-8", max_tokens=1024, messages=messages, tools=tools
  )

  final_text = next(
      block.text for block in final_response.content if block.type == "text"
  )
  print(f"\nClaude's response:\n{final_text}")

  # Verifikasi pemformatan
  print("\n--- Verification ---")
  print(f"✓ Tool results sent in single user message: {len(tool_results)} results")
  print("✓ No text before tool results in content array")
  print("✓ Conversation formatted correctly for future parallel tool use")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Definisikan alat
  const tools: Anthropic.Tool[] = [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object" as const,
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          }
        },
        required: ["location"]
      }
    },
    {
      name: "get_time",
      description: "Get the current time in a given timezone",
      input_schema: {
        type: "object" as const,
        properties: {
          timezone: {
            type: "string",
            description: "The timezone, e.g. America/New_York"
          }
        },
        required: ["timezone"]
      }
    }
  ];

  // Buat permintaan awal
  console.log("Requesting parallel tool calls...");
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      }
    ],
    tools: tools
  });

  // Periksa pemanggilan alat paralel
  const toolUses = response.content.filter((block) => block.type === "tool_use");
  console.log(`\n✓ Claude made ${toolUses.length} tool calls`);

  if (toolUses.length > 1) {
    console.log("✓ Parallel tool calls detected!");
    for (const tool of toolUses) {
      if (tool.type === "tool_use") {
        console.log(`  - ${tool.name}: ${JSON.stringify(tool.input)}`);
      }
    }
  } else {
    console.log("✗ No parallel tool calls detected");
  }

  // Simulasikan eksekusi alat dan format hasilnya dengan benar
  const toolResults: Anthropic.ToolResultBlockParam[] = toolUses
    .filter((block): block is Anthropic.ToolUseBlock => block.type === "tool_use")
    .map((toolUse) => {
      const input = toolUse.input as Record<string, string>;
      let result: string;
      if (toolUse.name === "get_weather") {
        result = input.location?.includes("San Francisco")
          ? "San Francisco: 68F, partly cloudy"
          : "New York: 45F, clear skies";
      } else {
        result = input.timezone?.includes("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST";
      }

      return {
        type: "tool_result" as const,
        tool_use_id: toolUse.id,
        content: result
      };
    });

  // Dapatkan respons akhir dengan format yang benar
  console.log("\nGetting final response...");
  const finalResponse = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      },
      { role: "assistant", content: response.content },
      { role: "user", content: toolResults }
    ],
    tools: tools
  });

  for (const block of finalResponse.content) {
    if (block.type === "text") {
      console.log(`\nClaude's response:\n${block.text}`);
    }
  }

  // Verifikasi format
  console.log("\n--- Verification ---");
  console.log(`✓ Tool results sent in single user message: ${toolResults.length} results`);
  console.log("✓ No text before tool results in content array");
  console.log("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```csharp C#
  AnthropicClient client = new();

  var tools = new List<ToolUnion>
  {
      new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get the current weather in a given location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
              },
              Required = ["location"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "get_time",
          Description = "Get the current time in a given timezone",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["timezone"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The timezone, e.g. America/New_York" }),
              },
              Required = ["timezone"],
          },
      }),
  };

  Console.WriteLine("Requesting parallel tool calls...");
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" }],
      Tools = tools
  };

  var response = await client.Messages.Create(parameters);

  var toolUses = new List<ToolUseBlock>();
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          toolUses.Add(toolUse);
      }
  }
  Console.WriteLine($"\n✓ Claude made {toolUses.Count} tool calls");

  if (toolUses.Count > 1)
  {
      Console.WriteLine("✓ Parallel tool calls detected!");
      foreach (var tool in toolUses)
      {
          Console.WriteLine($"  - {tool.Name}: {JsonSerializer.Serialize(tool.Input)}");
      }
  }
  else
  {
      Console.WriteLine("✗ No parallel tool calls detected");
  }

  var toolResults = new List<ContentBlockParam>();
  foreach (var toolUse in toolUses)
  {
      string result;
      if (toolUse.Name == "get_weather")
      {
          result = JsonSerializer.Serialize(toolUse.Input).Contains("San Francisco")
              ? "San Francisco: 68°F, partly cloudy"
              : "New York: 45°F, clear skies";
      }
      else
      {
          result = JsonSerializer.Serialize(toolUse.Input).Contains("Los_Angeles")
              ? "2:30 PM PST"
              : "5:30 PM EST";
      }

      toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
      {
          ToolUseID = toolUse.ID,
          Content = result,
      }));
  }

  Console.WriteLine("\nGetting final response...");
  var finalParameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [
          new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" },
          new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
          new() { Role = Role.User, Content = new MessageParamContent(toolResults) }
      ],
      Tools = tools
  };

  var finalResponse = await client.Messages.Create(finalParameters);
  finalResponse.Content[0].TryPickText(out var text);
  Console.WriteLine($"\nClaude's response:\n{text?.Text}");

  Console.WriteLine("\n--- Verification ---");
  Console.WriteLine($"✓ Tool results sent in single user message: {toolResults.Count} results");
  Console.WriteLine("✓ No text before tool results in content array");
  Console.WriteLine("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```go Go
  client := anthropic.NewClient()

  tools := []anthropic.ToolUnionParam{
  	{OfTool: &anthropic.ToolParam{
  		Name:        "get_weather",
  		Description: anthropic.String("Get the current weather in a given location"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"location": map[string]any{
  					"type":        "string",
  					"description": "The city and state, e.g. San Francisco, CA",
  				},
  			},
  			Required: []string{"location"},
  		},
  	}},
  	{OfTool: &anthropic.ToolParam{
  		Name:        "get_time",
  		Description: anthropic.String("Get the current time in a given timezone"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"timezone": map[string]any{
  					"type":        "string",
  					"description": "The timezone, e.g. America/New_York",
  				},
  			},
  			Required: []string{"timezone"},
  		},
  	}},
  }

  fmt.Println("Requesting parallel tool calls...")
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
  	},
  	Tools: tools,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Temukan blok tool_use menggunakan type switch
  type toolUseInfo struct {
  	ID    string
  	Name  string
  	Input json.RawMessage
  }
  var toolUses []toolUseInfo
  for _, block := range response.Content {
  	switch variant := block.AsAny().(type) {
  	case anthropic.ToolUseBlock:
  		toolUses = append(toolUses, toolUseInfo{
  			ID:    variant.ID,
  			Name:  variant.Name,
  			Input: variant.Input,
  		})
  	}
  }

  fmt.Printf("\n✓ Claude made %d tool calls\n", len(toolUses))

  if len(toolUses) > 1 {
  	fmt.Println("✓ Parallel tool calls detected!")
  	for _, tool := range toolUses {
  		fmt.Printf("  - %s: %s\n", tool.Name, string(tool.Input))
  	}
  } else {
  	fmt.Println("✗ No parallel tool calls detected")
  }

  // Bangun hasil alat
  var toolResults []anthropic.ContentBlockParamUnion
  for _, toolUse := range toolUses {
  	var result string
  	inputStr := string(toolUse.Input)

  	if toolUse.Name == "get_weather" {
  		if strings.Contains(inputStr, "San Francisco") {
  			result = "San Francisco: 68°F, partly cloudy"
  		} else {
  			result = "New York: 45°F, clear skies"
  		}
  	} else {
  		if strings.Contains(inputStr, "Los_Angeles") {
  			result = "2:30 PM PST"
  		} else {
  			result = "5:30 PM EST"
  		}
  	}

  	toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, result, false))
  }

  fmt.Println("\nGetting final response...")
  finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
  		response.ToParam(),
  		anthropic.NewUserMessage(toolResults...),
  	},
  	Tools: tools,
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("\nClaude's response:\n%s\n", finalResponse.Content[0].Text)

  fmt.Println("\n--- Verification ---")
  fmt.Printf("✓ Tool results sent in single user message: %d results\n", len(toolResults))
  fmt.Println("✓ No text before tool results in content array")
  fmt.Println("✓ Conversation formatted correctly for future parallel tool use")
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Tool weatherTool = Tool.builder()
      .name("get_weather")
      .description("Get the current weather in a given location")
      .inputSchema(InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "location", Map.of(
                  "type", "string",
                  "description", "The city and state, e.g. San Francisco, CA"
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("location")))
          .build())
      .build();

  Tool timeTool = Tool.builder()
      .name("get_time")
      .description("Get the current time in a given timezone")
      .inputSchema(InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "timezone", Map.of(
                  "type", "string",
                  "description", "The timezone, e.g. America/New_York"
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("timezone")))
          .build())
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(weatherTool)
      .addTool(timeTool)
      .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
      .build();

  IO.println("Requesting parallel tool calls...");
  Message response = client.messages().create(params);

  List<ToolUseBlock> toolUses = new ArrayList<>();
  for (ContentBlock block : response.content()) {
      if (block.toolUse().isPresent()) {
          toolUses.add(block.toolUse().get());
      }
  }

  IO.println("\n✓ Claude made " + toolUses.size() + " tool calls");

  if (toolUses.size() > 1) {
      IO.println("✓ Parallel tool calls detected!");
      for (ToolUseBlock tool : toolUses) {
          IO.println("  - " + tool.name() + ": " + tool._input());
      }
  } else {
      IO.println("✗ No parallel tool calls detected");
  }

  List<ContentBlockParam> toolResults = new ArrayList<>();
  for (ToolUseBlock toolUse : toolUses) {
      String result;
      if (toolUse.name().equals("get_weather")) {
          String location = toolUse._input().toString();
          result = location.contains("San Francisco")
              ? "San Francisco: 68°F, partly cloudy"
              : "New York: 45°F, clear skies";
      } else {
          String timezone = toolUse._input().toString();
          result = timezone.contains("Los_Angeles")
              ? "2:30 PM PST"
              : "5:30 PM EST";
      }
      toolResults.add(ContentBlockParam.ofToolResult(
          ToolResultBlockParam.builder()
              .toolUseId(toolUse.id())
              .content(result)
              .build()
      ));
  }

  IO.println("\nGetting final response...");
  MessageCreateParams finalParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(weatherTool)
      .addTool(timeTool)
      .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
      .addMessage(response)
      .addUserMessageOfBlockParams(toolResults)
      .build();

  Message finalResponse = client.messages().create(finalParams);
  finalResponse.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> IO.println("\nClaude's response:\n" + textBlock.text()));

  IO.println("\n--- Verification ---");
  IO.println("✓ Tool results sent in single user message: " + toolResults.size() + " results");
  IO.println("✓ No text before tool results in content array");
  IO.println("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```php PHP
  $client = new Client();

  $tools = [
      [
          'name' => 'get_weather',
          'description' => 'Get the current weather in a given location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'The city and state, e.g. San Francisco, CA'
                  ]
              ],
              'required' => ['location']
          ]
      ],
      [
          'name' => 'get_time',
          'description' => 'Get the current time in a given timezone',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'timezone' => [
                      'type' => 'string',
                      'description' => 'The timezone, e.g. America/New_York'
                  ]
              ],
              'required' => ['timezone']
          ]
      ]
  ];

  echo "Requesting parallel tool calls...\n";
  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"]
      ],
      model: 'claude-opus-4-8',
      tools: $tools,
  );

  $toolUses = array_filter($response->content, fn($block) => $block->type === 'tool_use');
  echo "\n✓ Claude made " . count($toolUses) . " tool calls\n";

  if (count($toolUses) > 1) {
      echo "✓ Parallel tool calls detected!\n";
      foreach ($toolUses as $tool) {
          echo "  - {$tool->name}: " . json_encode($tool->input) . "\n";
      }
  } else {
      echo "✗ No parallel tool calls detected\n";
  }

  $toolResults = [];
  foreach ($toolUses as $toolUse) {
      if ($toolUse->name === 'get_weather') {
          $result = str_contains(json_encode($toolUse->input), 'San Francisco')
              ? 'San Francisco: 68°F, partly cloudy'
              : 'New York: 45°F, clear skies';
      } else {
          $result = str_contains(json_encode($toolUse->input), 'Los_Angeles')
              ? '2:30 PM PST'
              : '5:30 PM EST';
      }

      $toolResults[] = [
          'type' => 'tool_result',
          'tool_use_id' => $toolUse->id,
          'content' => $result
      ];
  }

  echo "\nGetting final response...\n";
  $finalResponse = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"],
          ['role' => 'assistant', 'content' => $response->content],
          ['role' => 'user', 'content' => $toolResults]
      ],
      model: 'claude-opus-4-8',
      tools: $tools,
  );

  echo "\nClaude's response:\n{$finalResponse->content[0]->text}\n";

  echo "\n--- Verification ---\n";
  echo "✓ Tool results sent in single user message: " . count($toolResults) . " results\n";
  echo "✓ No text before tool results in content array\n";
  echo "✓ Conversation formatted correctly for future parallel tool use\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tools = [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          }
        },
        required: ["location"]
      }
    },
    {
      name: "get_time",
      description: "Get the current time in a given timezone",
      input_schema: {
        type: "object",
        properties: {
          timezone: {
            type: "string",
            description: "The timezone, e.g. America/New_York"
          }
        },
        required: ["timezone"]
      }
    }
  ]

  puts "Requesting parallel tool calls..."
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" }
    ],
    tools: tools
  )

  tool_uses = response.content.select { |block| block.type == :tool_use }
  puts "\n✓ Claude made #{tool_uses.length} tool calls"

  if tool_uses.length > 1
    puts "✓ Parallel tool calls detected!"
    tool_uses.each do |tool|
      puts "  - #{tool.name}: #{tool.input}"
    end
  else
    puts "✗ No parallel tool calls detected"
  end

  tool_results = tool_uses.map do |tool_use|
    result = if tool_use.name == "get_weather"
      location = tool_use.input[:location].to_s
      location.include?("San Francisco") ? "San Francisco: 68°F, partly cloudy" : "New York: 45°F, clear skies"
    else
      timezone = tool_use.input[:timezone].to_s
      timezone.include?("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST"
    end

    {
      type: "tool_result",
      tool_use_id: tool_use.id,
      content: result
    }
  end

  puts "\nGetting final response..."
  final_response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" },
      { role: "assistant", content: response.content },
      { role: "user", content: tool_results }
    ],
    tools: tools
  )

  final_text = final_response.content.find { |block| block.type == :text }
  puts "\nClaude's response:\n#{final_text.text}"

  puts "\n--- Verification ---"
  puts "✓ Tool results sent in single user message: #{tool_results.length} results"
  puts "✓ No text before tool results in content array"
  puts "✓ Conversation formatted correctly for future parallel tool use"
  ```
</CodeGroup>

Baris ringkasan di akhir menyatakan kembali dua aturan pemformatan yang menjaga paralelisme tetap berfungsi: setiap hasil alat dikembalikan dalam satu pesan pengguna, dan tidak ada konten teks yang muncul sebelum hasil alat dalam pesan tersebut.

## Memaksimalkan penggunaan alat paralel

Model Claude 4 melakukan panggilan alat paralel secara default ketika permintaan mendapat manfaat dari beberapa alat. Untuk semua model, Anda dapat meningkatkan kemungkinan panggilan alat paralel dengan prompting yang terarah:

<AccordionGroup>
  <Accordion title="Prompt sistem untuk penggunaan alat paralel">
    Untuk model Claude 4, tambahkan ini ke prompt sistem Anda:

    ```text wrap
    For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
    ```

    Untuk penggunaan alat paralel yang lebih kuat lagi (direkomendasikan jika default tidak cukup), gunakan:

    ```text wrap
    <use_parallel_tool_calls>
    For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. When running multiple read-only commands like `ls` or `list_dir`, always run all of the commands in parallel. Err on the side of maximizing parallel tool calls rather than running too many tools sequentially.
    </use_parallel_tool_calls>
    ```
  </Accordion>

  <Accordion title="Prompting pesan pengguna">
    Anda juga dapat mendorong penggunaan alat paralel dalam pesan pengguna tertentu:

    ```text wrap
    Instead of:
    "What's the weather in Paris? Also check London."

    Use:
    "Check the weather in Paris and London simultaneously."

    Or be explicit:
    "Please use parallel tool calls to get the weather for Paris, London, and Tokyo at the same time."
    ```
  </Accordion>
</AccordionGroup>

## Menonaktifkan penggunaan alat paralel

Penggunaan alat paralel aktif secara default. Untuk menonaktifkannya, atur `disable_parallel_tool_use: true` di dalam objek [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use). Ini bukan parameter permintaan tingkat atas. Efeknya bergantung pada tipe `tool_choice`.

### Paling banyak satu panggilan alat

Ketika tipe `tool_choice` adalah `auto` (default), mengatur `disable_parallel_tool_use: true` berarti Claude memanggil paling banyak satu alat per respons. Claude masih dapat menjawab dalam teks biasa tanpa memanggil alat apa pun. Baris yang disorot adalah satu-satunya perubahan dari permintaan penggunaan alat standar:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }],
      "tool_choice": {"type": "auto", "disable_parallel_tool_use": true},
      "messages": [
        {"role": "user", "content": "What is the weather in San Francisco and New York?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
  tool_choice:
    type: auto
    disable_parallel_tool_use: true
  messages:
    - role: user
      content: What is the weather in San Francisco and New York?
  YAML
  ```

  ```python Python
  client = Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      }
                  },
                  "required": ["location"],
              },
          }
      ],
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "What is the weather in San Francisco and New York?",
          }
      ],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [{ role: "user", content: "What is the weather in San Francisco and New York?" }]
  });
  console.log(response.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                  },
                  Required = ["location"],
              },
          }),
      ],
      ToolChoice = new ToolChoiceAuto { DisableParallelToolUse = true },
      Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco and New York?" }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	ToolChoice: anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{
  			DisableParallelToolUse: anthropic.Bool(true),
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco and New York?")),
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
                  )
              )
          )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(
          Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(schema)
              .build()
      )
      .toolChoice(ToolChoiceAuto.builder().disableParallelToolUse(true).build())
      .addUserMessage("What is the weather in San Francisco and New York?")
      .build();

  Message response = client.messages().create(params);
  IO.println(response.content());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather in San Francisco and New York?']
      ],
      model: 'claude-opus-4-8',
      toolChoice: ['type' => 'auto', 'disableParallelToolUse' => true],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [
      { role: "user", content: "What is the weather in San Francisco and New York?" }
    ]
  )
  puts response.content
  ```
</CodeGroup>

### Tepat satu panggilan alat

Ketika tipe `tool_choice` adalah `any` atau `tool`, mengatur `disable_parallel_tool_use: true` berarti Claude memanggil tepat satu alat. Contoh berikut menggunakan `any`. Field yang sama berfungsi dengan `tool`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }],
      "tool_choice": {"type": "any", "disable_parallel_tool_use": true},
      "messages": [
        {"role": "user", "content": "What is the weather in San Francisco and New York?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
  tool_choice:
    type: any
    disable_parallel_tool_use: true
  messages:
    - role: user
      content: What is the weather in San Francisco and New York?
  YAML
  ```

  ```python Python
  client = Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      }
                  },
                  "required": ["location"],
              },
          }
      ],
      tool_choice={"type": "any", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "What is the weather in San Francisco and New York?",
          }
      ],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "any", disable_parallel_tool_use: true },
    messages: [{ role: "user", content: "What is the weather in San Francisco and New York?" }]
  });
  console.log(response.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                  },
                  Required = ["location"],
              },
          }),
      ],
      ToolChoice = new ToolChoiceAny { DisableParallelToolUse = true },
      Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco and New York?" }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	ToolChoice: anthropic.ToolChoiceUnionParam{
  		OfAny: &anthropic.ToolChoiceAnyParam{
  			DisableParallelToolUse: anthropic.Bool(true),
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco and New York?")),
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
                  )
              )
          )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(
          Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(schema)
              .build()
      )
      .toolChoice(ToolChoiceAny.builder().disableParallelToolUse(true).build())
      .addUserMessage("What is the weather in San Francisco and New York?")
      .build();

  Message response = client.messages().create(params);
  IO.println(response.content());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather in San Francisco and New York?']
      ],
      model: 'claude-opus-4-8',
      toolChoice: ['type' => 'any', 'disableParallelToolUse' => true],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "any", disable_parallel_tool_use: true },
    messages: [
      { role: "user", content: "What is the weather in San Francisco and New York?" }
    ]
  )
  puts response.content
  ```
</CodeGroup>

## Pemecahan masalah

Jika Claude tidak melakukan panggilan alat paralel saat diharapkan, periksa masalah umum berikut:

**1. Pemformatan hasil alat yang salah**

Masalah paling umum adalah memformat hasil alat secara tidak benar dalam riwayat percakapan. Ini "mengajari" Claude untuk menghindari panggilan paralel.

Khusus untuk penggunaan alat paralel:

* **Salah:** pesan pengguna terpisah untuk setiap hasil alat
* **Benar:** semua hasil alat bersama-sama dalam satu pesan pengguna

```json
// Wrong: separate user messages reduce parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1]},
  {"role": "user", "content": [tool_result_2]}  // Separate message
]

// Correct: one user message with all results maintains parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1, tool_result_2]}  // Single message
]
```

Lihat [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk aturan pemformatan lainnya.

**2. Prompting yang lemah**

Prompting default mungkin tidak cukup. Gunakan prompt sistem yang lebih kuat dari [Memaksimalkan penggunaan alat paralel](#maximizing-parallel-tool-use).

**3. Mengukur penggunaan alat paralel**

Untuk memverifikasi bahwa panggilan alat paralel berfungsi:

<CodeGroup>
  ```bash cURL
  # Mengukur penggunaan alat paralel adalah analisis sisi klien terhadap respons yang sudah
  # Anda kumpulkan, jadi tidak bisa dijadikan perintah shell sekali jalan. Lihat tab SDK.
  ```

  ```bash CLI
  # Mengukur penggunaan alat paralel adalah analisis sisi klien terhadap respons yang sudah Anda
  # kumpulkan, jadi tidak bisa diterjemahkan menjadi satu perintah shell sekali jalan. Lihat tab SDK.
  ```

  ```python Python
  messages = []  # Message objects returned by client.messages.create across your run

  tool_call_messages = [
      msg for msg in messages if any(block.type == "tool_use" for block in msg.content)
  ]
  total_tool_calls = sum(
      len([block for block in msg.content if block.type == "tool_use"])
      for msg in tool_call_messages
  )
  avg_tools_per_message = (
      total_tool_calls / len(tool_call_messages) if tool_call_messages else 0.0
  )
  print(f"Average tools per message: {avg_tools_per_message}")
  # Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```typescript TypeScript
  const messages: Anthropic.Message[] = []; // Message objects returned by client.messages.create across your run

  const toolCallMessages = messages.filter((message) =>
    message.content.some((block) => block.type === "tool_use")
  );
  const totalToolCalls = toolCallMessages.reduce(
    (sum, message) => sum + message.content.filter((block) => block.type === "tool_use").length,
    0
  );
  const avgToolsPerMessage =
    toolCallMessages.length > 0 ? totalToolCalls / toolCallMessages.length : 0;
  console.log(`Average tools per message: ${avgToolsPerMessage}`);
  // Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```csharp C#
  List<Message> messages = []; // Message objects returned by client.Messages.Create across your run

  var toolCallMessages = messages
      .Where(message => message.Content.Any(block => block.TryPickToolUse(out _)))
      .ToList();
  var totalToolCalls = toolCallMessages
      .Sum(message => message.Content.Count(block => block.TryPickToolUse(out _)));
  var avgToolsPerMessage = toolCallMessages.Count > 0 ? (double)totalToolCalls / toolCallMessages.Count : 0.0;
  Console.WriteLine($"Average tools per message: {avgToolsPerMessage}");
  // Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```go Go
  var messages []anthropic.Message // Message values returned by client.Messages.New across your run

  toolCallMessageCount := 0
  totalToolCalls := 0
  for _, message := range messages {
  	callsInMessage := 0
  	for _, block := range message.Content {
  		if block.Type == "tool_use" {
  			callsInMessage++
  		}
  	}
  	if callsInMessage > 0 {
  		toolCallMessageCount++
  		totalToolCalls += callsInMessage
  	}
  }

  avgToolsPerMessage := 0.0
  if toolCallMessageCount > 0 {
  	avgToolsPerMessage = float64(totalToolCalls) / float64(toolCallMessageCount)
  }
  fmt.Println("Average tools per message:", avgToolsPerMessage)
  // Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```java Java
  List<Message> messages = List.of(); // Message objects returned by client.messages().create() across your run

  List<Message> toolCallMessages = messages.stream()
      .filter(message -> message.content().stream().anyMatch(ContentBlock::isToolUse))
      .toList();
  long totalToolCalls = toolCallMessages.stream()
      .mapToLong(message -> message.content().stream().filter(ContentBlock::isToolUse).count())
      .sum();
  double avgToolsPerMessage = toolCallMessages.isEmpty() ? 0.0 : (double) totalToolCalls / toolCallMessages.size();
  IO.println("Average tools per message: " + avgToolsPerMessage);
  // Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```php PHP
  // $messages: Objek Message yang dikembalikan oleh $client->messages->create() selama eksekusi Anda
  $messages = [];

  $toolCallMessages = array_values(array_filter(
      $messages,
      fn ($message) => count(array_filter($message->content, fn ($block) => $block->type === 'tool_use')) > 0
  ));
  $totalToolCalls = array_sum(array_map(
      fn ($message) => count(array_filter($message->content, fn ($block) => $block->type === 'tool_use')),
      $toolCallMessages
  ));
  $avgToolsPerMessage = count($toolCallMessages) > 0 ? $totalToolCalls / count($toolCallMessages) : 0.0;
  echo "Average tools per message: {$avgToolsPerMessage}\n";
  // Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```

  ```ruby Ruby
  messages = [] # Message objects returned by client.messages.create across your run

  tool_call_messages = messages.select { |message| message.content.any? { |block| block.type == :tool_use } }
  total_tool_calls = tool_call_messages.sum { |message| message.content.count { |block| block.type == :tool_use } }
  avg_tools_per_message = tool_call_messages.empty? ? 0.0 : total_tool_calls.to_f / tool_call_messages.size
  puts "Average tools per message: #{avg_tools_per_message}"
  # Seharusnya > 1.0 jika panggilan paralel berfungsi
  ```
</CodeGroup>

**4. Panggilan dalam satu batch tampak saling bergantung**

Urutan eksekusi adalah pilihan Anda. Jika alat Anda memiliki ketergantungan urutan, menjalankan batch secara berurutan dan berhenti pada kegagalan pertama adalah strategi yang valid: kembalikan `is_error: true` untuk setiap panggilan yang tidak Anda jalankan. Jika Anda menjalankan secara paralel dan sebuah panggilan gagal karena prasyaratnya belum selesai, kembalikan `is_error: true` dengan pesan kesalahan yang alami. Claude akan mengeluarkan kembali panggilan tersebut pada giliran berikutnya. Untuk mengurangi panggilan yang saling bergantung muncul bersamaan, tambahkan ini ke prompt sistem Anda: "Only batch tool calls that are independent of each other."

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Tool Runner (SDK)" icon="wrench" href="/docs/id/agents-and-tools/tool-use/tool-runner">
    Gunakan abstraksi Tool Runner dari SDK untuk menangani loop agentik, pembungkusan kesalahan, dan keamanan tipe secara otomatis.
  </Card>

  <Card title="Menangani panggilan alat" icon="arrows-left-right" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Mengurai blok tool\_use, memformat respons tool\_result, dan menangani kesalahan dengan is\_error.
  </Card>

  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Menentukan skema alat, menulis deskripsi yang efektif, dan mengontrol kapan Claude memanggil alat Anda.
  </Card>
</CardGroup>
