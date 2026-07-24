---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: c7931cfc75833f66c71c76f08ca5fc44bb1db444c2df0f6eb661f182c631c971
---

# Streaming alat berbutir halus

Streaming input alat tanpa buffering JSON sisi server untuk aplikasi yang sensitif terhadap latensi.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

"Fine-grained tool streaming" (streaming alat berbutir halus) mengirimkan input alat ke klien Anda saat Claude menghasilkannya, tanpa buffering sisi server atau validasi JSON. Melewati langkah buffering mengurangi waktu hingga fragmen pertama dari parameter besar, seperti dokumen atau blok kode, dan fragmen-fragmen tersebut tiba melalui event [Streaming messages](/docs/id/build-with-claude/streaming) yang sama seperti penggunaan alat standar.

<Warning>
  Karena API tidak melakukan buffering atau memvalidasi input alat sebelum melakukan streaming, Anda mungkin menerima JSON yang parsial atau tidak valid. Respons yang berakhir dengan [stop reason](/docs/id/build-with-claude/handling-stop-reasons) `max_tokens` juga dapat memotong parameter di tengah jalan. Akumulasikan fragmen-fragmennya, lindungi proses parsing, dan lihat [Menangani JSON tidak valid dalam respons alat](#handling-invalid-json-in-tool-responses) untuk cara mengembalikan input yang tidak dapat di-parse ke Claude.
</Warning>

## Cara menggunakan streaming alat berbutir halus

Semua model mendukung streaming alat berbutir halus di Claude API, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Untuk menggunakannya, atur `eager_input_streaming` ke `true` pada alat yang didefinisikan pengguna di mana Anda ingin streaming berbutir halus diaktifkan, dan aktifkan streaming pada permintaan Anda.

Field `eager_input_streaming` bersifat opsional. Mengaturnya ke `true` mengaktifkan streaming berbutir halus untuk alat tersebut, dan menghilangkannya memberi Anda streaming buffered standar, di mana API melakukan buffering dan memvalidasi setiap nilai parameter sebelum melakukan streaming kembali. Pengecualiannya adalah permintaan yang masih mengirimkan header beta lama `fine-grained-tool-streaming-2025-05-14`, yang mengaktifkan streaming berbutir halus untuk alat yang tidak mengatur field tersebut. Field per-alat menggantikan header tersebut, dan nilai `false` yang eksplisit mempertahankan streaming buffered untuk sebuah alat bahkan ketika permintaan masih mengirimkannya. Lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference) untuk definisi field.

Contoh berikut mengaktifkan streaming berbutir halus untuk alat `make_file` dan meminta Claude membuat puisi panjang, sehingga input alat cukup besar untuk diamati saat streaming masuk:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 65536,
      "tools": [
        {
          "name": "make_file",
          "description": "Write text to a file",
          "eager_input_streaming": true,
          "input_schema": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "description": "The filename to write text to"
              },
              "lines_of_text": {
                "type": "array",
                "description": "An array of lines of text to write to the file"
              }
            },
            "required": ["filename", "lines_of_text"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Can you write a long poem and make a file called poem.txt?"
        }
      ],
      "stream": true
    }'
  ```

  ```bash CLI
  ant messages create --stream --format jsonl <<'YAML' |
  model: claude-opus-4-8
  max_tokens: 65536
  tools:
    - name: make_file
      description: Write text to a file
      eager_input_streaming: true
      input_schema:
        type: object
        properties:
          filename:
            type: string
            description: The filename to write text to
          lines_of_text:
            type: array
            description: An array of lines of text to write to the file
        required:
          - filename
          - lines_of_text
  messages:
    - role: user
      content: Can you write a long poem and make a file called poem.txt?
  YAML
    jq -rj 'select(.delta.type == "input_json_delta") | .delta.partial_json'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=65536,
      model="claude-opus-4-8",
      tools=[
          {
              "name": "make_file",
              "description": "Write text to a file",
              "eager_input_streaming": True,
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "filename": {
                          "type": "string",
                          "description": "The filename to write text to",
                      },
                      "lines_of_text": {
                          "type": "array",
                          "description": "An array of lines of text to write to the file",
                      },
                  },
                  "required": ["filename", "lines_of_text"],
              },
          }
      ],
      messages=[
          {
              "role": "user",
              "content": "Can you write a long poem and make a file called poem.txt?",
          }
      ],
  ) as stream:
      for event in stream:
          if event.type == "input_json":
              print(event.partial_json, end="", flush=True)
      final_message = stream.get_final_message()

  print()
  for block in final_message.content:
      if block.type == "tool_use":
          print(f"Complete tool input: {block.input}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 65536,
    tools: [
      {
        name: "make_file",
        description: "Write text to a file",
        eager_input_streaming: true,
        input_schema: {
          type: "object",
          properties: {
            filename: {
              type: "string",
              description: "The filename to write text to"
            },
            lines_of_text: {
              type: "array",
              description: "An array of lines of text to write to the file"
            }
          },
          required: ["filename", "lines_of_text"]
        }
      }
    ],
    messages: [
      {
        role: "user",
        content: "Can you write a long poem and make a file called poem.txt?"
      }
    ]
  });

  stream.on("inputJson", (partialJson) => {
    process.stdout.write(partialJson);
  });

  const message = await stream.finalMessage();
  console.log();
  for (const block of message.content) {
    if (block.type === "tool_use") {
      console.log("Complete tool input:", block.input);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  MessageCreateParams parameters = new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 65536,
      Tools =
      [
          new Tool
          {
              Name = "make_file",
              Description = "Write text to a file",
              EagerInputStreaming = true,
              InputSchema = new InputSchema
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["filename"] = JsonSerializer.SerializeToElement(
                          new { type = "string", description = "The filename to write text to" }
                      ),
                      ["lines_of_text"] = JsonSerializer.SerializeToElement(
                          new { type = "array", description = "An array of lines of text to write to the file" }
                      ),
                  },
                  Required = ["filename", "lines_of_text"],
              },
          },
      ],
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Can you write a long poem and make a file called poem.txt?",
          },
      ],
  };

  // Contoh C# merakit input-nya sendiri: indeks blok konten -> JSON yang terakumulasi
  var toolInputs = new Dictionary<long, StringBuilder>();

  await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
  {
      if (
          streamEvent.TryPickContentBlockStart(out var start)
          && start.ContentBlock.TryPickToolUse(out _)
      )
      {
          toolInputs[start.Index] = new StringBuilder();
      }
      else if (
          streamEvent.TryPickContentBlockDelta(out var delta)
          && delta.Delta.TryPickInputJson(out var inputJson)
      )
      {
          Console.Write(inputJson.PartialJson);
          toolInputs[delta.Index].Append(inputJson.PartialJson);
      }
  }

  Console.WriteLine();
  foreach (var accumulatedInput in toolInputs.Values)
  {
      Console.WriteLine($"Complete tool input: {accumulatedInput}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  makeFileTool := anthropic.ToolParam{
  	Name:                "make_file",
  	Description:         anthropic.String("Write text to a file"),
  	EagerInputStreaming: anthropic.Bool(true),
  	InputSchema: anthropic.ToolInputSchemaParam{
  		Properties: map[string]any{
  			"filename": map[string]any{
  				"type":        "string",
  				"description": "The filename to write text to",
  			},
  			"lines_of_text": map[string]any{
  				"type":        "array",
  				"description": "An array of lines of text to write to the file",
  			},
  		},
  		Required: []string{"filename", "lines_of_text"},
  	},
  }

  stream := client.Messages.NewStreaming(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 65536,
  	Tools:     []anthropic.ToolUnionParam{{OfTool: &makeFileTool}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Can you write a long poem and make a file called poem.txt?",
  		)),
  	},
  })

  message := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := message.Accumulate(event); err != nil {
  		panic(err)
  	}
  	if delta, ok := event.AsAny().(anthropic.ContentBlockDeltaEvent); ok {
  		if inputJSON, ok := delta.Delta.AsAny().(anthropic.InputJSONDelta); ok {
  			fmt.Print(inputJSON.PartialJSON)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }

  fmt.Println()
  for _, block := range message.Content {
  	if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  		fmt.Printf("Complete tool input: %s\n", toolUse.Input)
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Tool makeFileTool = Tool.builder()
      .name("make_file")
      .description("Write text to a file")
      .eagerInputStreaming(true)
      .inputSchema(Tool.InputSchema.builder()
          .properties(Tool.InputSchema.Properties.builder()
              .putAdditionalProperty("filename", JsonValue.from(Map.of(
                  "type", "string",
                  "description", "The filename to write text to")))
              .putAdditionalProperty("lines_of_text", JsonValue.from(Map.of(
                  "type", "array",
                  "description", "An array of lines of text to write to the file")))
              .build())
          .addRequired("filename")
          .addRequired("lines_of_text")
          .build())
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(65536L)
      .addTool(makeFileTool)
      .addUserMessage("Can you write a long poem and make a file called poem.txt?")
      .build();

  MessageAccumulator accumulator = MessageAccumulator.create();

  try (StreamResponse<RawMessageStreamEvent> streamResponse =
          client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          accumulator.accumulate(event);
          if (event.isContentBlockDelta()) {
              var delta = event.asContentBlockDelta().delta();
              if (delta.isInputJson()) {
                  IO.print(delta.asInputJson().partialJson());
              }
          }
      });
  }

  IO.println("");
  accumulator.message().content().forEach(block ->
      block.toolUse().ifPresent(toolUse ->
          IO.println("Complete tool input: " + toolUse._input())));
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Messages\InputJSONDelta;
  use Anthropic\Messages\Model;
  use Anthropic\Messages\RawContentBlockDeltaEvent;
  use Anthropic\Messages\RawContentBlockStartEvent;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 65536,
      model: Model::CLAUDE_OPUS_4_8,
      tools: [
          [
              'name' => 'make_file',
              'description' => 'Write text to a file',
              'eager_input_streaming' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'filename' => [
                          'type' => 'string',
                          'description' => 'The filename to write text to',
                      ],
                      'lines_of_text' => [
                          'type' => 'array',
                          'description' => 'An array of lines of text to write to the file',
                      ],
                  ],
                  'required' => ['filename', 'lines_of_text'],
              ],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Can you write a long poem and make a file called poem.txt?',
          ],
      ],
  );

  // Contoh PHP merakit input-nya sendiri: index => string JSON yang terakumulasi
  $toolInputs = [];

  foreach ($stream as $event) {
      if (
          $event instanceof RawContentBlockStartEvent
          && $event->contentBlock instanceof ToolUseBlock
      ) {
          $toolInputs[$event->index] = '';
      } elseif (
          $event instanceof RawContentBlockDeltaEvent
          && $event->delta instanceof InputJSONDelta
      ) {
          echo $event->delta->partialJSON;
          $toolInputs[$event->index] .= $event->delta->partialJSON;
      }
  }

  echo "\n";
  foreach ($toolInputs as $toolInput) {
      echo "Complete tool input: {$toolInput}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: Anthropic::Models::Model::CLAUDE_OPUS_4_8,
    max_tokens: 65_536,
    tools: [
      {
        name: "make_file",
        description: "Write text to a file",
        eager_input_streaming: true,
        input_schema: {
          type: "object",
          properties: {
            filename: {
              type: "string",
              description: "The filename to write text to"
            },
            lines_of_text: {
              type: "array",
              description: "An array of lines of text to write to the file"
            }
          },
          required: ["filename", "lines_of_text"]
        }
      }
    ],
    messages: [
      {
        role: "user",
        content: "Can you write a long poem and make a file called poem.txt?"
      }
    ]
  )

  stream.each do |event|
    print event.partial_json if event.is_a?(Anthropic::Streaming::InputJsonEvent)
  end

  puts
  stream.accumulated_message.content.each do |block|
    puts "Complete tool input: #{block.input}" if block.type == :tool_use
  end
  ```
</CodeGroup>

Setiap tab mengaktifkan streaming berbutir halus untuk alat `make_file`. Tab SDK mencetak setiap fragmen input saat tiba, lalu mencetak input terakumulasi lengkap setelah stream berakhir. Tab cURL menampilkan stream event mentah, dan tab CLI menggunakan `jq` untuk mencetak hanya fragmen-fragmennya. Karena fragmen yang dicetak bergabung menjadi input alat lengkap, puisi tersebut memenuhi terminal Anda saat Claude menulisnya:

```text wrap
{"filename": "poem.txt", "lines_of_text": ["The Wanderer's Journey", "", "I.", "", "Beneath the vast and star-strewn sky,", "Where silver moonbeams softly lie,", ...
Complete tool input: {"filename": "poem.txt", "lines_of_text": ["The Wanderer's Journey", ...]}
```

Tanpa `eager_input_streaming`, API melakukan buffering dan memvalidasi setiap nilai parameter sebelum melakukan streaming kembali, sehingga tidak ada yang dicetak untuk parameter besar sampai Claude selesai menghasilkannya. Dengannya, fragmen mulai tiba segera setelah Claude memulai parameter tersebut, dan biasanya lebih panjang, dengan lebih sedikit pemotongan di tengah kata.

## Mengakumulasi delta input alat

Kontrak akumulasi sama dengan streaming penggunaan alat standar, jadi bagian ini berlaku dengan dan tanpa `eager_input_streaming`. Lihat [Input JSON delta](/docs/id/build-with-claude/streaming#input-json-delta) di Streaming messages untuk format event. Streaming alat berbutir halus mengubah apa yang dapat Anda asumsikan tentang hasilnya: server melakukan streaming fragmen tanpa memvalidasinya, sehingga string yang terakumulasi mungkin bukan JSON yang valid.

Ketika blok konten `tool_use` di-streaming, event `content_block_start` awal berisi `input: {}` (objek kosong). Ini adalah placeholder. Input sebenarnya tiba sebagai serangkaian event `input_json_delta`, masing-masing membawa fragmen string `partial_json`. Untuk merakit input lengkap, gabungkan fragmen-fragmen ini dan parse hasilnya ketika blok ditutup.

Jika SDK Anda menyediakan helper akumulator (seperti yang dilakukan tab Python, TypeScript, Go, Java, dan Ruby pada contoh sebelumnya), helper tersebut menanganinya untuk Anda. Pola manual ditujukan untuk SDK tanpa helper, atau ketika Anda menginginkan kontrol penuh atas cara input dirakit.

Kontrak akumulasi:

1. Pada `content_block_start` dengan `type: "tool_use"`, inisialisasi string kosong: `input_json = ""`
2. Untuk setiap `content_block_delta` dengan `type: "input_json_delta"`, tambahkan: `input_json += event.delta.partial_json`
3. Pada `content_block_stop`, parse string yang terakumulasi

Lindungi proses parsing, seperti yang dilakukan contoh SDK berikut. Respons juga dapat berhenti pada `max_tokens` di tengah parameter. Periksa [stop reason](/docs/id/build-with-claude/handling-stop-reasons) dan putuskan apakah akan mencoba ulang permintaan dengan `max_tokens` yang lebih tinggi atau memperbaiki input parsial.

Ketidakcocokan tipe antara `input: {}` awal (objek) dan `partial_json` (string) memang disengaja. Objek kosong menandai slot dalam array konten. String delta membangun nilai sebenarnya.

<CodeGroup>
  ```bash cURL
  # Mengakumulasi delta input per blok memerlukan bahasa pemrograman; tab CLI pada
  # contoh pertama menampilkan fragmen mentah dengan jq. Lihat tab SDK.
  ```

  ```bash CLI
  # Mengakumulasi delta input per-blok memerlukan bahasa pemrograman; tab CLI pada
  # contoh pertama menampilkan fragmen mentah dengan jq. Lihat tab SDK.
  ```

  ```python Python
  client = anthropic.Anthropic()

  tool_inputs: dict[int, str] = {}  # index -> accumulated JSON string

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get current weather for a city",
              "eager_input_streaming": True,
              "input_schema": {
                  "type": "object",
                  "properties": {"city": {"type": "string"}},
                  "required": ["city"],
              },
          }
      ],
      messages=[{"role": "user", "content": "Weather in Paris?"}],
  ) as stream:
      for event in stream:
          match event.type:
              case "content_block_start" if event.content_block.type == "tool_use":
                  tool_inputs[event.index] = ""
              case "content_block_delta" if event.delta.type == "input_json_delta":
                  tool_inputs[event.index] += event.delta.partial_json
              case "content_block_stop" if event.index in tool_inputs:
                  raw_input = tool_inputs[event.index]
                  try:
                      parsed = json.loads(raw_input)
                  except json.JSONDecodeError:
                      # String yang terakumulasi tidak dijamin merupakan JSON yang valid.
                      # Lihat "Menangani JSON yang tidak valid dalam respons alat" di halaman ini.
                      print(f"Invalid tool input: {raw_input}")
                  else:
                      print(f"Tool input: {parsed}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const toolInputs = new Map<number, string>();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a city",
        eager_input_streaming: true,
        input_schema: {
          type: "object",
          properties: { city: { type: "string" } },
          required: ["city"]
        }
      }
    ],
    messages: [{ role: "user", content: "Weather in Paris?" }]
  });

  for await (const event of stream) {
    if (event.type === "content_block_start" && event.content_block.type === "tool_use") {
      toolInputs.set(event.index, "");
    } else if (event.type === "content_block_delta" && event.delta.type === "input_json_delta") {
      toolInputs.set(
        event.index,
        (toolInputs.get(event.index) ?? "") + event.delta.partial_json
      );
    } else if (event.type === "content_block_stop" && toolInputs.has(event.index)) {
      const rawInput = toolInputs.get(event.index)!;
      try {
        console.log("Tool input:", JSON.parse(rawInput));
      } catch {
        // String yang terakumulasi tidak dijamin merupakan JSON yang valid.
        // Lihat "Menangani JSON tidak valid dalam respons alat" di halaman ini.
        console.log("Invalid tool input:", rawInput);
      }
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  MessageCreateParams parameters = new()
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools =
      [
          new Tool
          {
              Name = "get_weather",
              Description = "Get current weather for a city",
              EagerInputStreaming = true,
              InputSchema = new InputSchema
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["city"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  },
                  Required = ["city"],
              },
          },
      ],
      Messages = [new() { Role = Role.User, Content = "Weather in Paris?" }],
  };

  // Indeks blok -> fragmen JSON yang terakumulasi
  // Contoh ini mengakumulasi delta secara manual untuk menampilkan stream mentah;
  // MessageContentAggregator dari SDK juga dapat mengakumulasi input alat secara otomatis.
  var toolInputs = new Dictionary<long, StringBuilder>();

  await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
  {
      if (
          streamEvent.TryPickContentBlockStart(out var start)
          && start.ContentBlock.TryPickToolUse(out _)
      )
      {
          toolInputs[start.Index] = new StringBuilder();
      }
      else if (
          streamEvent.TryPickContentBlockDelta(out var delta)
          && delta.Delta.TryPickInputJson(out var inputJson)
      )
      {
          toolInputs[delta.Index].Append(inputJson.PartialJson);
      }
      else if (
          streamEvent.TryPickContentBlockStop(out var stop)
          && toolInputs.TryGetValue(stop.Index, out var accumulated)
      )
      {
          try
          {
              using var parsed = JsonDocument.Parse(accumulated.ToString());
              Console.WriteLine($"Tool input: {parsed.RootElement}");
          }
          catch (JsonException)
          {
              // String yang terakumulasi tidak dijamin merupakan JSON yang valid.
              // Lihat "Handling invalid JSON in tool responses" di halaman ini.
              Console.WriteLine($"Invalid tool input: {accumulated}");
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  toolInputs := map[int64]string{} // content block index -> accumulated JSON

  stream := client.Messages.NewStreaming(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{{
  		OfTool: &anthropic.ToolParam{
  			Name:                "get_weather",
  			Description:         anthropic.String("Get current weather for a city"),
  			EagerInputStreaming: anthropic.Bool(true),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"city": map[string]any{"type": "string"},
  				},
  				Required: []string{"city"},
  			},
  		},
  	}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Weather in Paris?")),
  	},
  })

  for stream.Next() {
  	switch event := stream.Current().AsAny().(type) {
  	case anthropic.ContentBlockStartEvent:
  		if _, ok := event.ContentBlock.AsAny().(anthropic.ToolUseBlock); ok {
  			toolInputs[event.Index] = ""
  		}
  	case anthropic.ContentBlockDeltaEvent:
  		if delta, ok := event.Delta.AsAny().(anthropic.InputJSONDelta); ok {
  			toolInputs[event.Index] += delta.PartialJSON
  		}
  	case anthropic.ContentBlockStopEvent:
  		if accumulated, ok := toolInputs[event.Index]; ok {
  			var parsed map[string]any
  			if err := json.Unmarshal([]byte(accumulated), &parsed); err != nil {
  				// String yang terakumulasi tidak dijamin merupakan JSON yang valid.
  				// Lihat "Menangani JSON yang tidak valid dalam respons alat" di halaman ini.
  				fmt.Println("Invalid tool input:", accumulated)
  			} else {
  				fmt.Println("Tool input:", parsed)
  			}
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();
  ObjectMapper objectMapper = new ObjectMapper();

  Tool weatherTool = Tool.builder()
          .name("get_weather")
          .description("Get current weather for a city")
          .eagerInputStreaming(true)
          .inputSchema(Tool.InputSchema.builder()
                  .properties(Tool.InputSchema.Properties.builder()
                          .putAdditionalProperty("city", JsonValue.from(Map.of("type", "string")))
                          .build())
                  .addRequired("city")
                  .build())
          .build();

  MessageCreateParams createParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addTool(weatherTool)
          .addUserMessage("Weather in Paris?")
          .build();

  // Indeks blok konten -> JSON input alat yang terakumulasi
  Map<Long, StringBuilder> toolInputs = new HashMap<>();

  try (StreamResponse<RawMessageStreamEvent> streamResponse = client.messages().createStreaming(createParams)) {
      var eventIterator = streamResponse.stream().iterator();
      while (eventIterator.hasNext()) {
          RawMessageStreamEvent event = eventIterator.next();
          if (event.isContentBlockStart()) {
              var blockStart = event.asContentBlockStart();
              if (blockStart.contentBlock().isToolUse()) {
                  toolInputs.put(blockStart.index(), new StringBuilder());
              }
          } else if (event.isContentBlockDelta()) {
              var blockDelta = event.asContentBlockDelta();
              if (blockDelta.delta().isInputJson() && toolInputs.containsKey(blockDelta.index())) {
                  toolInputs.get(blockDelta.index()).append(blockDelta.delta().asInputJson().partialJson());
              }
          } else if (event.isContentBlockStop()) {
              var blockStop = event.asContentBlockStop();
              if (toolInputs.containsKey(blockStop.index())) {
                  String accumulated = toolInputs.get(blockStop.index()).toString();
                  try {
                      IO.println("Tool input: " + objectMapper.readTree(accumulated));
                  } catch (JsonProcessingException e) {
                      // String yang terakumulasi tidak dijamin merupakan JSON yang valid.
                      // Lihat "Menangani JSON yang tidak valid dalam respons alat" di halaman ini.
                      IO.println("Invalid tool input: " + accumulated);
                  }
              }
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Messages\InputJSONDelta;
  use Anthropic\Messages\Model;
  use Anthropic\Messages\RawContentBlockDeltaEvent;
  use Anthropic\Messages\RawContentBlockStartEvent;
  use Anthropic\Messages\RawContentBlockStopEvent;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  // SDK PHP tidak menyediakan akumulator stream untuk input alat;
  // pola manual yang ditunjukkan di sini adalah pendekatan yang didukung.
  $toolInputs = []; // index => accumulated JSON string

  $stream = $client->messages->createStream(
      maxTokens: 1024,
      model: Model::CLAUDE_OPUS_4_8,
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get current weather for a city',
              'eager_input_streaming' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => ['city' => ['type' => 'string']],
                  'required' => ['city'],
              ],
          ],
      ],
      messages: [['role' => 'user', 'content' => 'Weather in Paris?']],
  );

  foreach ($stream as $event) {
      if (
          $event instanceof RawContentBlockStartEvent
          && $event->contentBlock instanceof ToolUseBlock
      ) {
          $toolInputs[$event->index] = '';
      } elseif (
          $event instanceof RawContentBlockDeltaEvent
          && $event->delta instanceof InputJSONDelta
      ) {
          $toolInputs[$event->index] .= $event->delta->partialJSON;
      } elseif (
          $event instanceof RawContentBlockStopEvent
          && isset($toolInputs[$event->index])
      ) {
          $accumulated = $toolInputs[$event->index];
          try {
              $parsed = json_decode($accumulated, associative: true, flags: JSON_THROW_ON_ERROR);
              echo "Tool input: " . json_encode($parsed) . "\n";
          } catch (JsonException $e) {
              // String yang terakumulasi tidak dijamin merupakan JSON yang valid.
              // Lihat "Menangani JSON tidak valid dalam respons alat" di halaman ini.
              echo "Invalid tool input: {$accumulated}\n";
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tool_inputs = {} # index -> accumulated JSON string

  stream = client.messages.stream_raw(
    model: Anthropic::Models::Model::CLAUDE_OPUS_4_8,
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a city",
        eager_input_streaming: true,
        input_schema: {
          type: "object",
          properties: {city: {type: "string"}},
          required: ["city"]
        }
      }
    ],
    messages: [{role: "user", content: "Weather in Paris?"}]
  )

  stream.each do |event|
    case event
    when Anthropic::Models::RawContentBlockStartEvent
      tool_inputs[event.index] = +"" if event.content_block.type == :tool_use
    when Anthropic::Models::RawContentBlockDeltaEvent
      if event.delta.is_a?(Anthropic::Models::InputJSONDelta)
        tool_inputs[event.index] << event.delta.partial_json
      end
    when Anthropic::Models::RawContentBlockStopEvent
      if tool_inputs.key?(event.index)
        accumulated = tool_inputs[event.index]
        begin
          parsed = JSON.parse(accumulated)
          puts "Tool input: #{parsed}"
        rescue JSON::ParserError
          # String yang terakumulasi tidak dijamin merupakan JSON yang valid.
          # Lihat "Menangani JSON yang tidak valid dalam respons alat" di halaman ini.
          puts "Invalid tool input: #{accumulated}"
        end
      end
    end
  end
  ```
</CodeGroup>

<Tip>
  Bereaksi terhadap fragmen dan merakitnya adalah dua hal yang terpisah. Contoh pertama bereaksi terhadap setiap fragmen saat tiba dan tetap menyerahkan perakitan ke SDK pada tab yang menggunakan helper akumulator. Gunakan pola manual ketika Anda tidak menggunakan helper akumulator atau ketika Anda menginginkan kontrol penuh atas perakitan.
</Tip>

## Menangani JSON tidak valid dalam respons alat

Dengan streaming alat berbutir halus, input terakumulasi untuk pemanggilan alat mungkin berupa JSON yang tidak valid atau tidak lengkap. Ketika itu terjadi, Anda tidak dapat menjalankan alat tersebut, jadi laporkan kegagalan tersebut kembali ke Claude. `content` dari hasil alat tidak harus berupa JSON, tetapi membungkus string mentah dalam objek JSON di bawah satu kunci membuatnya jelas bagi Claude bahwa Anda menerima JSON yang tidak valid, dan mempertahankan input asli untuk debugging:

```json
{
  "INVALID_JSON": "<the unparseable input you received>"
}
```

Kembalikan wrapper tersebut, yang diserialisasi menjadi string, sebagai `content` dari blok konten [tool result](/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-errors-with-is-error) dengan `is_error` diatur ke `true`:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
  "is_error": true,
  "content": "{\"INVALID_JSON\": \"<the unparseable input you received>\"}"
}
```

<Note>
  Bangun wrapper dengan pustaka JSON Anda alih-alih dengan menggabungkan string, sehingga tanda kutip dan karakter khusus lainnya dalam input yang tidak valid di-escape dengan benar.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Jendela konteks" icon="stack" href="/docs/id/build-with-claude/context-windows">
    Pahami cara kerja jendela konteks, bagaimana pemikiran diperpanjang dan penggunaan alat dihitung di dalamnya, dan cara mengelola konteks saat percakapan berkembang.
  </Card>

  <Card title="Streaming messages" icon="lightning" href="/docs/id/build-with-claude/streaming">
    Streaming respons Messages API secara bertahap dengan server-sent events, termasuk teks, penggunaan alat, dan delta pemikiran diperpanjang.
  </Card>

  <Card title="Menangani pemanggilan alat" icon="arrows-left-right" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Parse blok tool\_use, format respons tool\_result, dan tangani error dengan is\_error.
  </Card>

  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
