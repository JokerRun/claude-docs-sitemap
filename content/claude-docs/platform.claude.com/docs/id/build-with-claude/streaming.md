---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/streaming
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: 598fdeb72b7158f958310c8008e94ea7590cf59df6b88040cfae8075d13aef2a
---

# Streaming pesan

Lakukan streaming respons Messages API secara bertahap dengan server-sent events, termasuk delta teks, penggunaan alat, dan pemikiran diperpanjang.

---

Saat membuat Message, Anda dapat mengatur `"stream": true` untuk melakukan streaming respons secara bertahap menggunakan [server-sent events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents) (SSE).

## Streaming dengan SDK

SDK [Python](https://github.com/anthropics/anthropic-sdk-python) dan [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript) menawarkan beberapa cara untuk melakukan streaming. SDK [PHP](https://github.com/anthropics/anthropic-sdk-php) menyediakan streaming melalui `createStream()`. SDK Python memungkinkan stream sinkron maupun asinkron. Lihat dokumentasi di setiap SDK untuk detailnya.

<CodeGroup>
  ```bash CLI
  ant messages create --stream --format jsonl \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello"}' \
    | jq -rj 'select(.delta.type? == "text_delta") | .delta.text'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello"}],
      model="claude-opus-4-8",
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  await client.messages
    .stream({
      messages: [{ role: "user", content: "Hello" }],
      model: "claude-opus-4-8",
      max_tokens: 1024
    })
    .on("text", (text) => {
      console.log(text);
    });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages = [new() { Role = Role.User, Content = "Hello" }]
          };

          await foreach (var msg in client.Messages.CreateStreaming(parameters))
          {
              Console.Write(msg);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model("claude-opus-4-8")
      .maxTokens(1024L)
      .addUserMessage("Hello")
      .build();

  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockDelta().ifPresent(deltaEvent ->
              deltaEvent.delta().text().ifPresent(td ->
                  System.out.print(td.text())
              )
          );
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
  );

  foreach ($stream as $message) {
      echo $message;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }]
  )

  stream.text.each { |text| print(text) }
  ```
</CodeGroup>

## Mendapatkan pesan akhir tanpa menangani event

Jika Anda tidak perlu memproses teks saat teks tersebut tiba, SDK menyediakan cara untuk menggunakan streaming di balik layar sambil mengembalikan objek `Message` lengkap, identik dengan yang dikembalikan oleh `.create()`. Ini sangat berguna untuk permintaan dengan nilai `max_tokens` yang besar, di mana SDK mengharuskan streaming untuk menghindari timeout HTTP.

<CodeGroup>
  ```bash CLI
  # Flag --stream pada CLI ant mengeluarkan satu event per baris dan tidak
  # mengakumulasikannya menjadi Message akhir. Untuk generasi panjang, lakukan streaming
  # event mentahnya:
  ant messages create --stream --format jsonl <<'YAML'
  model: claude-opus-4-8
  max_tokens: 128000
  messages:
    - role: user
      content: Write a detailed analysis...
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      max_tokens=128000,
      messages=[{"role": "user", "content": "Write a detailed analysis..."}],
      model="claude-opus-4-8",
  ) as stream:
      message = stream.get_final_message()

  print(message.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }],
    model: "claude-opus-4-8"
  });

  const message = await stream.finalMessage();
  const textBlock = message.content.find((block) => block.type === "text");
  if (textBlock && textBlock.type === "text") {
    console.log(textBlock.text);
  }
  ```

  ```csharp C#
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main()
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 128000,
              Messages = [new() { Role = Role.User, Content = "Write a detailed analysis..." }]
          };

          var fullText = "";
          await foreach (var msg in client.Messages.CreateStreaming(parameters))
          {
              fullText += msg;
          }

          Console.WriteLine(fullText);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 128000,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a detailed analysis...")),
  	},
  })

  message := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := message.Accumulate(event); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  import com.anthropic.helpers.MessageAccumulator;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(128000L)
              .addUserMessage("Write a detailed analysis...")
              .build();

          MessageAccumulator accumulator = MessageAccumulator.create();
          try (var streamResponse = client.messages().createStreaming(params)) {
              streamResponse.stream().forEach(accumulator::accumulate);
          }

          Message message = accumulator.message();
          message.content().get(0).text().ifPresent(tb -> System.out.println(tb.text()));
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 128000,
      messages: [
          ['role' => 'user', 'content' => 'Write a detailed analysis...']
      ],
      model: 'claude-opus-4-8',
  );

  $fullText = '';
  foreach ($stream as $event) {
      if ($event->type === 'content_block_delta') {
          $fullText .= $event->delta->text;
      }
  }

  echo $fullText;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 128000,
    messages: [{ role: "user", content: "Write a detailed analysis..." }]
  ).accumulated_message

  puts message.content.first.text
  ```
</CodeGroup>

Pemanggilan `.stream()` menjaga koneksi HTTP tetap aktif dengan server-sent events, kemudian `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) mengakumulasi semua event dan mengembalikan objek `Message` lengkap. Di Go, Anda memanggil `message.Accumulate(event)` di dalam loop stream untuk membangun `Message` lengkap yang sama. Di Java, gunakan `MessageAccumulator.create()` dan panggil `accumulator.accumulate(event)` pada setiap event. Di C#, gunakan await pada metode ekstensi `.Aggregate()` milik stream untuk mendapatkan `Message` lengkap, atau berikan `MessageContentAggregator` ke `.CollectAsync()` untuk mengagregasi sambil menangani event. Di Ruby, panggil `.accumulated_message` pada stream. Di SDK PHP, Anda melakukan iterasi atas event stream secara manual untuk mengakumulasi respons.

## Tipe event

Setiap server-sent event menyertakan tipe event bernama dan data JSON terkait. Setiap event menggunakan nama event SSE (misalnya, `event: message_stop`), dan menyertakan `type` event yang sesuai dalam datanya.

Setiap stream menggunakan alur event berikut:

1. `message_start`: berisi objek `Message` dengan `content` kosong.
2. Serangkaian content block, yang masing-masing memiliki `content_block_start`, satu atau lebih event `content_block_delta`, dan event `content_block_stop`. Setiap content block memiliki `index` yang sesuai dengan indeksnya dalam array `content` Message akhir. Satu pengecualian: selama respons [server-side fallback](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), content block `fallback` tiba di setiap batas model sebagai pasangan `content_block_start` dan `content_block_stop` tanpa delta di antaranya.
3. Satu atau lebih event `message_delta`, yang menunjukkan perubahan tingkat atas pada objek `Message` akhir.
4. Event `message_stop` terakhir.

<Warning>
  Jumlah token yang ditampilkan di field `usage` dari event `message_delta` bersifat *kumulatif*.
</Warning>

### Event ping

Stream event juga dapat menyertakan sejumlah event `ping`.

### Event error

API terkadang dapat mengirim [error](/docs/id/api/errors) dalam stream event. Misalnya, selama periode penggunaan tinggi, Anda mungkin menerima `overloaded_error`, yang biasanya akan sesuai dengan HTTP 529 dalam konteks non-streaming:

```sse Example error
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

### Event lainnya

Sesuai dengan [kebijakan versioning](/docs/id/api/versioning), tipe event baru dapat ditambahkan, dan kode Anda harus menangani tipe event yang tidak dikenal dengan baik.

## Tipe delta content block

Setiap event `content_block_delta` berisi `delta` dari suatu tipe yang memperbarui blok `content` pada `index` tertentu.

### Delta teks

Delta content block `text` terlihat seperti:

```sse Text delta
event: content_block_delta
data: {"type": "content_block_delta","index": 0,"delta": {"type": "text_delta", "text": "ello frien"}}
```

### Delta input JSON

Delta untuk content block `tool_use` sesuai dengan pembaruan untuk field `input` dari blok tersebut. Untuk mendukung granularitas maksimum, delta adalah *string JSON parsial*, sedangkan `tool_use.input` akhir selalu berupa *objek*.

Anda dapat mengakumulasi delta string dan mem-parse JSON setelah Anda menerima event `content_block_stop`, dengan menggunakan library seperti [Pydantic](https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing) untuk melakukan parsing JSON parsial, atau dengan menggunakan [SDK](/docs/id/cli-sdks-libraries/overview), yang menyediakan helper untuk mengakses nilai inkremental yang telah di-parse.

Delta content block `tool_use` terlihat seperti:

```sse Input JSON delta
event: content_block_delta
data: {"type": "content_block_delta","index": 1,"delta": {"type": "input_json_delta","partial_json": "{\"location\": \"San Fra"}}}
```

Catatan: Model saat ini hanya mendukung pengiriman satu properti key dan value lengkap dari `input` pada satu waktu. Oleh karena itu, saat menggunakan alat, mungkin ada jeda antara event streaming saat model sedang bekerja. Setelah key dan value `input` terakumulasi, keduanya dikirim sebagai beberapa event `content_block_delta` dengan JSON parsial yang dipecah sehingga format tersebut dapat secara otomatis mendukung granularitas yang lebih halus di model mendatang.

### Delta thinking

Saat menggunakan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#streaming-thinking) dengan streaming diaktifkan, Anda akan menerima konten thinking melalui event `thinking_delta`. Delta ini sesuai dengan field `thinking` dari content block `thinking`.

Untuk konten thinking, event `signature_delta` khusus dikirim tepat sebelum event `content_block_stop`. Signature ini digunakan untuk memverifikasi integritas blok thinking.

Ketika `display: "omitted"` diatur pada konfigurasi thinking, tidak ada event `thinking_delta` yang dikirim. Blok thinking terbuka, menerima satu `signature_delta`, dan tertutup. Lihat [Mengontrol tampilan thinking](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display).

Delta thinking yang umum terlihat seperti:

```sse Thinking delta
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}
```

Delta signature terlihat seperti:

```sse Signature delta
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}
```

## Respons stream HTTP lengkap

Gunakan [SDK klien](/docs/id/cli-sdks-libraries/overview) saat menggunakan mode streaming. Namun, jika Anda membangun integrasi API langsung, Anda perlu menangani event ini sendiri.

Respons stream terdiri dari:

1. Event `message_start`

2. Kemungkinan beberapa content block, yang masing-masing berisi:

   * Event `content_block_start`
   * Kemungkinan beberapa event `content_block_delta`
   * Event `content_block_stop`

3. Satu atau lebih event `message_delta`

4. Event `message_stop`

Mungkin juga ada event `ping` yang tersebar di seluruh respons. Lihat [Tipe event](#event-types) untuk detail lebih lanjut tentang formatnya.

### Permintaan streaming dasar

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --data \
  '{
    "model": "claude-opus-4-8",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 256,
    "stream": true
  }'
  ```

  ```bash CLI
  ant messages create --stream --format jsonl \
    --model claude-opus-4-8 \
    --max-tokens 256 \
    --message '{role: user, content: Hello}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      messages=[{"role": "user", "content": "Hello"}],
      max_tokens=256,
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    messages: [{ role: "user", content: "Hello" }],
    max_tokens: 256
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  ```

  ```csharp C#
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 256,
              Messages = [new() { Role = Role.User, Content = "Hello" }]
          };

          await foreach (var msg in client.Messages.CreateStreaming(parameters))
          {
              Console.Write(msg);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 256,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(256L)
      .addUserMessage("Hello")
      .build();

  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockDelta().ifPresent(deltaEvent ->
              deltaEvent.delta().text().ifPresent(td ->
                  System.out.print(td.text())
              )
          );
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 256,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
  );

  foreach ($stream as $message) {
      echo $message;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    messages: [{ role: "user", content: "Hello" }],
    max_tokens: 256
  )

  stream.text.each { |text| print(text) }
  ```
</CodeGroup>

```sse Response
event: message_start
data: {"type": "message_start", "message": {"id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-8", "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "!"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence":null}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}

```

### Permintaan streaming dengan penggunaan alat

<Tip>
  Penggunaan alat mendukung [fine-grained streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) untuk nilai parameter. Aktifkan per alat dengan `eager_input_streaming`.
</Tip>

Permintaan ini meminta Claude untuk menggunakan alat guna melaporkan cuaca.

<CodeGroup>
  ```bash cURL
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-4-8",
        "max_tokens": 1024,
        "tools": [
          {
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
          }
        ],
        "tool_choice": {"type": "any"},
        "messages": [
          {
            "role": "user",
            "content": "What is the weather like in San Francisco?"
          }
        ],
        "stream": true
      }'
  ```

  ```bash CLI
  ant messages create --stream --format jsonl <<'YAML'
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
        required:
          - location
  tool_choice:
    type: any
  messages:
    - role: user
      content: What is the weather like in San Francisco?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

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
      }
  ]

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "any"},
      messages=[
          {"role": "user", "content": "What is the weather like in San Francisco?"}
      ],
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const tools: Anthropic.Tool[] = [
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
  ];

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: { type: "any" },
    messages: [
      {
        role: "user",
        content: "What is the weather like in San Francisco?"
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  ```

  ```csharp C#
  using System;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
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
              ToolChoice = new ToolChoiceAny(),
              Messages = [
                  new() { Role = Role.User, Content = "What is the weather like in San Francisco?" }
              ]
          };

          await foreach (var msg in client.Messages.CreateStreaming(parameters))
          {
              Console.Write(msg);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
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
  	ToolChoice: anthropic.ToolChoiceUnionParam{OfAny: &anthropic.ToolChoiceAnyParam{}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather like in San Francisco?")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addTool(Tool.builder()
          .name("get_weather")
          .description("Get the current weather in a given location")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "location", Map.of(
                      "type", "string",
                      "description", "The city and state, e.g. San Francisco, CA"
                  )
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("location")))
              .build())
          .build())
      .toolChoice(ToolChoice.ofAny(ToolChoiceAny.builder().build()))
      .addUserMessage("What is the weather like in San Francisco?")
      .build();

  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockDelta().ifPresent(deltaEvent ->
              deltaEvent.delta().text().ifPresent(td ->
                  System.out.print(td.text())
              )
          );
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather like in San Francisco?']
      ],
      model: 'claude-opus-4-8',
      toolChoice: ['type' => 'any'],
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

  foreach ($stream as $message) {
      echo $message;
  }
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
    }
  ]

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    tool_choice: { type: "any" },
    messages: [
      { role: "user", content: "What is the weather like in San Francisco?" }
    ]
  )

  stream.text.each { |text| print(text) }
  ```
</CodeGroup>

```sse Response
event: message_start
data: {"type":"message_start","message":{"id":"msg_014p7gG3wDgGV9EUtLvnow3U","type":"message","role":"assistant","model":"claude-opus-4-8","stop_sequence":null,"usage":{"input_tokens":472,"output_tokens":2},"content":[],"stop_reason":null}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Okay"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" let"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"'s"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" for"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" Francisco"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":","}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" CA"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":":"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"tool_use","id":"toolu_01T1x1fJ34qAmk2tNTrN7Up6","name":"get_weather","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"location\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"San"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" Francisc"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"o,"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" CA\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"tool_use","stop_sequence":null},"usage":{"output_tokens":89}}

event: message_stop
data: {"type":"message_stop"}
```

### Permintaan streaming dengan pemikiran diperpanjang

Permintaan ini mengaktifkan pemikiran diperpanjang dengan streaming. Pengaturan `display: "summarized"` melakukan streaming ringkasan singkat dari penalaran Claude alih-alih rantai pemikiran lengkap.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-opus-4-8",
      "max_tokens": 20000,
      "stream": true,
      "thinking": {
          "type": "adaptive",
          "display": "summarized"
      },
      "messages": [
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?"
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages create --stream --format jsonl \
    --model claude-opus-4-8 \
    --max-tokens 20000 \
    --thinking '{type: adaptive, display: summarized}' \
    --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=20000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  ) as stream:
      for event in stream:
          if event.type == "content_block_delta":
              if event.delta.type == "thinking_delta":
                  print(event.delta.thinking, end="", flush=True)
              elif event.delta.type == "text_delta":
                  print(event.delta.text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 20000,
    thinking: { type: "adaptive", display: "summarized" },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta") {
      if (event.delta.type === "thinking_delta") {
        process.stdout.write(event.delta.thinking);
      } else if (event.delta.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
    }
  }
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 20000,
      Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
      Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
  };

  await foreach (var msg in client.Messages.CreateStreaming(parameters))
  {
      Console.Write(msg);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 20000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
  			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.ThinkingDelta:
  			fmt.Print(deltaVariant.Thinking)
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(20000L)
      .thinking(ThinkingConfigAdaptive.builder()
          .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
          .build())
      .addUserMessage("What is the greatest common divisor of 1071 and 462?")
      .build();

  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockDelta().ifPresent(deltaEvent -> {
              deltaEvent.delta().thinking().ifPresent(td ->
                  IO.print(td.thinking())
              );
              deltaEvent.delta().text().ifPresent(td ->
                  IO.print(td.text())
              );
          });
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 20000,
      messages: [
          ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
      ],
      model: 'claude-opus-4-8',
      thinking: ['type' => 'adaptive', 'display' => 'summarized'],
  );

  foreach ($stream as $message) {
      echo $message;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 20000,
    thinking: { type: "adaptive", display: "summarized" },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ]
  )

  stream.each do |event|
    if event.type == :content_block_delta
      if event.delta.type == :thinking_delta
        print(event.delta.thinking)
      elsif event.delta.type == :text_delta
        print(event.delta.text)
      end
    end
  end
  ```
</CodeGroup>

```sse Response
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-8", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n147 = 7 × 21 + 0"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\nThe remainder is 0, so GCD(1071, 462) = 21."}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

### Permintaan streaming dengan penggunaan alat pencarian web

Permintaan ini meminta Claude untuk mencari di web informasi cuaca terkini.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "stream": true,
      "tools": [
          {
              "type": "web_search_20250305",
              "name": "web_search",
              "max_uses": 5
          }
      ],
      "messages": [
          {
              "role": "user",
              "content": "What is the weather like in New York City today?"
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages create --stream --format jsonl \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --tool '{type: web_search_20250305, name: web_search, max_uses: 5}' \
    --message '{role: user, content: What is the weather like in New York City today?}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
      messages=[
          {"role": "user", "content": "What is the weather like in New York City today?"}
      ],
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [{ type: "web_search_20250305", name: "web_search", max_uses: 5 }],
    messages: [{ role: "user", content: "What is the weather like in New York City today?" }]
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = [new ToolUnion(new WebSearchTool20250305() { MaxUses = 5 })],
      Messages = [new() { Role = Role.User, Content = "What is the weather like in New York City today?" }]
  };

  await foreach (var msg in client.Messages.CreateStreaming(parameters))
  {
      Console.Write(msg);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{
  			OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
  				MaxUses: anthropic.Int(5),
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather like in New York City today?")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.WebSearchTool20250305;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(WebSearchTool20250305.builder()
                  .maxUses(5L)
                  .build())
              .addUserMessage("What is the weather like in New York City today?")
              .build();

          try (var streamResponse = client.messages().createStreaming(params)) {
              streamResponse.stream().forEach(event -> {
                  event.contentBlockDelta().ifPresent(deltaEvent ->
                      deltaEvent.delta().text().ifPresent(td ->
                          System.out.print(td.text())
                      )
                  );
              });
          }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather like in New York City today?']
      ],
      model: 'claude-opus-4-8',
      tools: [
          ['type' => 'web_search_20250305', 'name' => 'web_search', 'max_uses' => 5]
      ],
  );

  foreach ($stream as $message) {
      echo $message;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: :"claude-opus-4-8",
    max_tokens: 1024,
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 5
      }
    ],
    messages: [
      {
        role: "user",
        content: "What is the weather like in New York City today?"
      }
    ]
  )

  stream.text.each { |text| print(text) }
  ```
</CodeGroup>

```sse Response
event: message_start
data: {"type":"message_start","message":{"id":"msg_01G...","type":"message","role":"assistant","model":"claude-opus-4-8","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":2679,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":3}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"I'll check"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" the current weather in New York City for you"}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"server_tool_use","id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","name":"web_search","input":{}}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\"query"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"\":"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" \"weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":" NY"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"C to"}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"day\"}"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1 }

event: content_block_start
data: {"type":"content_block_start","index":2,"content_block":{"type":"web_search_tool_result","tool_use_id":"srvtoolu_014hJH82Qum7Td6UV8gDXThB","content":[{"type":"web_search_result","title":"Weather in New York City in May 2025 (New York) - detailed Weather Forecast for a month","url":"https://world-weather.info/forecast/usa/new_york/may-2025/","encrypted_content":"Ev0DCioIAxgCIiQ3NmU4ZmI4OC1k...","page_age":null},...]}}

event: content_block_stop
data: {"type":"content_block_stop","index":2}

event: content_block_start
data: {"type":"content_block_start","index":3,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"Here's the current weather information for New York"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" City:\n\n# Weather"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":" in New York City"}}

event: content_block_delta
data: {"type":"content_block_delta","index":3,"delta":{"type":"text_delta","text":"\n\n"}}

...

event: content_block_stop
data: {"type":"content_block_stop","index":17}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"input_tokens":10682,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":510,"server_tool_use":{"web_search_requests":1}}}

event: message_stop
data: {"type":"message_stop"}
```

## Pemulihan error

### Claude 4.5 dan sebelumnya

Untuk model Claude 4.5 dan sebelumnya, Anda dapat memulihkan permintaan streaming yang terputus karena masalah jaringan, timeout, atau error lainnya dengan melanjutkan dari titik di mana stream terputus. Pendekatan ini menghemat Anda dari memproses ulang seluruh respons.

Strategi pemulihan dasar meliputi:

1. **Tangkap respons parsial:** Simpan semua konten yang berhasil diterima sebelum error terjadi
2. **Susun permintaan lanjutan:** Buat permintaan API baru yang menyertakan respons asisten parsial sebagai awal dari pesan asisten baru
3. **Lanjutkan streaming:** Lanjutkan menerima sisa respons dari titik di mana stream terputus

### Claude 4.6 dan setelahnya

Untuk model Claude 4.6 dan setelahnya, strategi tangkap-dan-lanjutkan yang sama berlaku, tetapi langkah 2 berubah: alih-alih menempatkan respons parsial dalam pesan asisten, tambahkan pesan pengguna yang menginstruksikan model untuk melanjutkan dari titik terakhirnya.

1. **Tangkap respons parsial:** Simpan semua konten yang berhasil diterima sebelum error terjadi
2. **Susun permintaan lanjutan:** Buat permintaan API baru dengan pesan pengguna yang berisi respons parsial dan instruksi untuk melanjutkan, misalnya:
   ```text Sample prompt wrap
   Your previous response was interrupted and ended with [previous_response]. Continue from where you left off.
   ```
3. **Lanjutkan streaming:** Lanjutkan menerima sisa respons dari titik di mana stream terputus

### Praktik terbaik pemulihan error

1. **Gunakan fitur SDK:** Manfaatkan kemampuan akumulasi pesan dan penanganan error bawaan SDK
2. **Tangani tipe konten:** Perhatikan bahwa pesan dapat berisi beberapa content block (`text`, `tool_use`, `thinking`). Blok penggunaan alat dan pemikiran diperpanjang tidak dapat dipulihkan secara parsial. Anda dapat melanjutkan streaming dari blok teks terbaru.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Stop reason dan fallback" icon="list" href="/docs/id/build-with-claude/handling-stop-reasons">
    Tangani setiap nilai `stop_reason` setelah stream selesai.
  </Card>

  <Card title="Fine-grained tool streaming" icon="wrench" href="/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming">
    Lakukan streaming JSON input alat tanpa buffering sisi server untuk latensi yang lebih rendah.
  </Card>

  <Card title="Pemikiran diperpanjang" icon="brain" href="/docs/id/build-with-claude/extended-thinking">
    Lakukan streaming output pemikiran diperpanjang dengan event `thinking_delta` dan `signature_delta`.
  </Card>

  <Card title="SDK klien" icon="code" href="/docs/id/cli-sdks-libraries/overview">
    Gunakan SDK resmi, yang menangani streaming, akumulasi, dan koneksi ulang untuk Anda.
  </Card>

  <Card title="Pemrosesan batch" icon="stack" href="/docs/id/build-with-claude/batch-processing">
    Proses permintaan dalam volume besar secara asinkron ketika Anda tidak memerlukan respons real-time.
  </Card>
</CardGroup>
