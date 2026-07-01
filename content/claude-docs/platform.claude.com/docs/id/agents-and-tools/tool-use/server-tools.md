---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: c9803f97792cfe9294f2773f660c410a0ea5e8b807f1c392ac0d364dd75cae3d
---

# Alat server

Bekerja dengan alat yang dieksekusi Anthropic: blok server_tool_use, kelanjutan pause_turn, giliran yang mencampur alat server dan klien, serta pemfilteran domain.

---

Alat yang dieksekusi server memiliki mekanisme yang sama: blok `server_tool_use`, kelanjutan `pause_turn`, giliran yang mencampur alat server dan klien, kelayakan "Zero Data Retention" (Retensi Data Nol), atau ZDR, dan pemfilteran domain. Untuk alat individual, lihat [referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Blok server\_tool\_use

Blok `server_tool_use` muncul dalam respons Claude ketika alat yang dieksekusi server dijalankan. Field `id`-nya menggunakan prefiks `srvtoolu_` untuk membedakannya dari panggilan alat klien:

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_01A2B3C4D5E6F7G8H9",
  "name": "web_search",
  "input": { "query": "latest quantum computing breakthroughs" }
}
```

API mengeksekusi alat secara internal. Anda melihat panggilan dan hasilnya dalam respons, tetapi Anda tidak menangani eksekusinya. Tidak seperti blok `tool_use` klien, Anda tidak perlu merespons dengan `tool_result`. Blok hasil alat (misalnya, `web_search_tool_result` untuk pencarian web) mengikuti blok `server_tool_use` dalam giliran asisten yang sama, dipasangkan berdasarkan `tool_use_id`. Jika Claude memanggil salah satu alat klien Anda pada saat yang sama, blok `server_tool_use` muncul tanpa hasilnya, dan respons berakhir dengan `stop_reason: "tool_use"`. API menjalankan alat tersebut ketika Anda mengembalikan blok `tool_result` klien dalam permintaan Anda berikutnya.

## Loop sisi server dan pause\_turn

Saat menggunakan alat server seperti pencarian web, API mengeksekusi panggilan alat dalam loop agentik sisi server. Pada giliran yang berjalan lama, API mungkin menjeda loop tersebut dan mengembalikan stop reason `pause_turn`.

Berikut cara menangani stop reason `pause_turn`:

<CodeGroup>
  ```bash cURL
  # Permintaan awal. Jika "stop_reason" dalam respons adalah "pause_turn", lanjutkan
  # giliran dengan mengirim ulang permintaan dengan konten asisten ditambahkan ke messages.
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
          "content": "Search for comprehensive information about quantum computing breakthroughs in 2025"
        }
      ],
      "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
    }' | jq '{stop_reason, content}'
  ```

  ```bash CLI
  # Permintaan awal. Jika "stop_reason" pada output adalah "pause_turn", jalankan ulang dengan
  # konten asisten ditambahkan ke messages (lihat tab SDK).
  ant messages create --format json <<'YAML' | jq '{stop_reason, content}'
  model: claude-opus-4-8
  max_tokens: 1024
  tools:
    - {type: web_search_20250305, name: web_search, max_uses: 10}
  messages:
    - {role: user, content: "Search for comprehensive information about quantum computing breakthroughs in 2025"}
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Permintaan awal dengan pencarian web
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
          }
      ],
      tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
  )

  # Periksa apakah respons memiliki stop_reason pause_turn
  if response.stop_reason == "pause_turn":
      # Lanjutkan percakapan dengan konten yang dijeda
      messages = [
          {
              "role": "user",
              "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
          },
          {"role": "assistant", "content": response.content},
      ]

      # Kirim permintaan lanjutan
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=messages,
          tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
      )

      print(continuation)
  else:
      print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Permintaan awal dengan pencarian web
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  });

  // Periksa apakah respons memiliki stop_reason pause_turn
  if (response.stop_reason === "pause_turn") {
    // Lanjutkan percakapan dengan konten yang dijeda
    const messages: Anthropic.MessageParam[] = [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      { role: "assistant", content: response.content }
    ];

    // Kirim permintaan lanjutan
    const continuation = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages,
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 10
        }
      ]
    });

    console.log(continuation);
  } else {
    console.log(response);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
          }
      ],
      Tools = [new ToolUnion(new WebSearchTool20250305 { MaxUses = 10 })]
  };

  var response = await client.Messages.Create(parameters);

  if (response.StopReason?.Value() == StopReason.PauseTurn)
  {
      // Lanjutkan percakapan dengan konten yang dijeda
      var continuationParams = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [
              new() {
                  Role = Role.User,
                  Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
              },
              new() {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              }
          ],
          Tools = [new ToolUnion(new WebSearchTool20250305 { MaxUses = 10 })]
      };

      var continuation = await client.Messages.Create(continuationParams);
      Console.WriteLine(continuation);
  }
  else
  {
      Console.WriteLine(response);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  webSearchTool := []anthropic.ToolUnionParam{
  	{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
  		MaxUses: anthropic.Int(10),
  	}},
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
  	},
  	Tools: webSearchTool,
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == anthropic.StopReasonPauseTurn {
  	// Kirim kembali respons yang dijeda apa adanya agar Claude dapat melanjutkan giliran
  	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
  			response.ToParam(),
  		},
  		Tools: webSearchTool,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(continuation)
  } else {
  	fmt.Println(response)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.WebSearchTool20250305;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
          .addTool(WebSearchTool20250305.builder()
              .maxUses(10L)
              .build())
          .build();

      Message response = client.messages().create(params);

      if (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.PAUSE_TURN)) {
          MessageCreateParams continuationParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
              .addMessage(response)
              .addTool(WebSearchTool20250305.builder()
                  .maxUses(10L)
                  .build())
              .build();

          Message continuation = client.messages().create(continuationParams);
          IO.println(continuation);
      } else {
          IO.println(response);
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
          ]
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 10
          ]
      ],
  );

  if ($response->stopReason === 'pause_turn') {
      $messages = [
          [
              'role' => 'user',
              'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
          ],
          [
              'role' => 'assistant',
              'content' => $response->content
          ]
      ];

      $continuation = $client->messages->create(
          maxTokens: 1024,
          messages: $messages,
          model: 'claude-opus-4-8',
          tools: [
              [
                  'type' => 'web_search_20250305',
                  'name' => 'web_search',
                  'max_uses' => 10
              ]
          ],
      );

      echo $continuation;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  )

  if response.stop_reason == :pause_turn
    messages = [
      {
        role: "user",
        content: "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      {
        role: "assistant",
        content: response.content
      }
    ]

    continuation = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages,
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 10
        }
      ]
    )

    puts continuation
  else
    puts response
  end
  ```
</CodeGroup>

Saat menangani `pause_turn`:

* **Lanjutkan percakapan:** Kirim kembali respons yang dijeda apa adanya dalam permintaan berikutnya agar Claude dapat melanjutkan gilirannya.
* **Pertahankan status alat:** Sertakan alat yang sama dalam permintaan kelanjutan. Giliran yang dijeda dapat berakhir dengan blok `server_tool_use` yang alatnya belum dijalankan, dan API mengembalikan error validasi jika alat tersebut tidak ada dalam kelanjutan.
* **Ulangi sesuai kebutuhan:** Giliran yang dilanjutkan dapat dijeda lagi. Periksa `stop_reason` pada setiap respons dan lanjutkan hingga Anda mendapatkan stop reason yang berbeda, dengan membatasi jumlah kelanjutan seperti halnya loop retry lainnya.

Untuk nilai `stop_reason` lainnya dan pola penanganan umum, lihat [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons).

## Mencampur alat server dan alat klien dalam satu giliran

Claude dapat memanggil alat server dan alat klien dalam grup panggilan alat paralel yang sama, misalnya, `web_fetch` bersama dengan alat yang didefinisikan pengguna. Alat klien adalah alat apa pun yang dieksekusi oleh kode Anda dan yang menghasilkan blok `tool_use`, baik itu didefinisikan pengguna maupun alat klien dengan skema Anthropic seperti [alat Bash](/docs/id/agents-and-tools/tool-use/bash-tool). Ketika itu terjadi, API tidak menjalankan alat server. API segera mengembalikan respons agar Anda dapat menjalankan alat klien terlebih dahulu:

* `stop_reason` adalah `"tool_use"`, bukan `"pause_turn"`.
* `content` berisi blok `server_tool_use` dan blok `tool_use` klien, tetapi tidak ada blok hasil untuk alat server: panggilan tersebut belum selesai.
* Tidak ada penanda lain. Deteksi status ini dengan mencari blok `server_tool_use` yang `id`-nya tidak memiliki blok hasil yang cocok dalam respons. Blok `mcp_tool_use` dari [konektor MCP](/docs/id/agents-and-tools/mcp-connector) berperilaku dengan cara yang sama. Panggilan alat server yang sudah memiliki blok hasilnya dalam respons yang sama telah selesai dan tidak memerlukan apa pun dari Anda.

<Note>
  Dengan [pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling), bentuk respons yang sama memiliki arti yang berbeda. Blok `tool_use` klien berasal dari kode yang berjalan di alat `code_execution` dan bukan dari Claude secara langsung, dan field `caller`-nya menyebutkan blok `code_execution` yang memanggilnya. Kode tersebut sudah mulai berjalan: kode dijeda menunggu blok `tool_result` Anda, dan mengirimkannya akan melanjutkan eksekusi alih-alih memulai alat yang ditangguhkan. Blok hasil dari blok `code_execution` itu sendiri tiba setelah kode selesai, yang dapat memerlukan lebih dari satu putaran hasil alat. Pesan pengguna lanjutan itu sendiri sama dalam kedua kasus; dengan pemanggilan alat terprogram, kirim juga kembali `id` dari field `container` respons, seperti yang ditunjukkan halaman tersebut.
</Note>

```json
{
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "text",
      "text": "I'll fetch the article and check your system at the same time."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01HxbWnMRmbWyMfUtJKC45rA",
      "name": "web_fetch",
      "input": { "url": "https://example.com/article" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "name": "run_command",
      "input": { "command": "uname -a" }
    }
  ]
}
```

Untuk melanjutkan giliran, jalankan alat klien dan kirim pesan pengguna yang kontennya hanya berisi blok `tool_result`, satu untuk setiap blok `tool_use` dalam respons tersebut. Pertahankan array `tools` yang sama: permintaan lanjutan yang tidak lagi mendefinisikan alat server yang menunggu akan gagal dengan error 400 yang pesannya diakhiri dengan ``but no `web_fetch` tool was provided``.

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "content": "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
    }
  ]
}
```

API melampirkan hasil Anda ke giliran asisten yang masih terbuka, menjalankan alat server yang ditangguhkan (untuk eksekusi kode yang dijeda, melanjutkannya), dan kemudian membiarkan Claude melanjutkan. Untuk alat server yang dipanggil Claude secara langsung, respons berikutnya dimulai dengan blok hasil yang menjawab `id` `server_tool_use` dari respons sebelumnya, diikuti oleh konten yang baru dihasilkan dan `stop_reason` baru:

```json
{
  "stop_reason": "end_turn",
  "content": [
    {
      "type": "web_fetch_tool_result",
      "tool_use_id": "srvtoolu_01HxbWnMRmbWyMfUtJKC45rA",
      "content": {
        "type": "web_fetch_result",
        "url": "https://example.com/article",
        "content": {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "Full text content of the article..."
          }
        }
      }
    },
    {
      "type": "text",
      "text": "The article argues that... and your machine is running Linux..."
    }
  ]
}
```

Blok `server_tool_use` dan blok hasilnya dipasangkan berdasarkan `tool_use_id`, bukan berdasarkan posisi: dalam alur ini keduanya tiba dalam dua respons yang berbeda, dan blok `server_tool_use` tidak diulang dalam respons kedua. Pada permintaan selanjutnya, simpan seluruh pertukaran dalam array `messages` Anda secara berurutan: respons pertama sebagai pesan `assistant`, pesan pengguna `tool_result`, dan kemudian respons berikutnya sebagai pesan `assistant` lainnya, dengan cara yang sama seperti Anda mengakumulasi pertukaran penggunaan alat lainnya.

<Warning>
  Pesan pengguna lanjutan tidak boleh berisi apa pun kecuali blok `tool_result`. Blok yang ditambahkan setelah hasil, seperti teks, memberi tahu API bahwa giliran asisten telah selesai. Untuk alat server yang dipanggil Claude secara langsung, hal itu membuat giliran memiliki panggilan alat server yang belum terselesaikan, dan permintaan gagal dengan `invalid_request_error` 400:

  ```text wrap
  `web_fetch` tool use with id `srvtoolu_01HxbWnMRmbWyMfUtJKC45rA` was found without a corresponding `web_fetch_tool_result` block
  ```

  Lanjutan yang menempatkan konten sebelum hasil, hanya menjawab sebagian ID `tool_use` klien, atau tidak berisi blok `tool_result` sama sekali akan gagal lebih awal, dengan error alat klien yang dijelaskan dalam [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls):

  ```text wrap
  `tool_use` ids were found without `tool_result` blocks immediately after: toolu_01PjgRJLbXrXEMZwDNYLnBqk. Each `tool_use` block must have a corresponding `tool_result` block in the next message.
  ```

  Untuk memberikan input lebih lanjut kepada Claude, kirimkan sebagai pesan pengguna terpisah setelah giliran selesai.
</Warning>

**Perbedaannya dengan `pause_turn`:** [Respons `pause_turn`](#the-server-side-loop-and-pause-turn) juga dapat berakhir dengan blok `server_tool_use` yang belum dijalankan, tetapi tidak pernah meninggalkan blok `tool_use` klien yang menunggu Anda, jadi Anda melanjutkannya dengan mengirim ulang konten asisten apa adanya. Respons yang meninggalkan blok `tool_use` klien yang menunggu Anda tidak pernah memiliki `stop_reason` berupa `pause_turn`: ketika Claude berhenti untuk memanggil alat Anda, `stop_reason` adalah `tool_use`, dan Anda melanjutkannya dengan mengirim blok `tool_result` klien alih-alih mengirim ulang respons. Dalam kedua kasus, API menjalankan alat server yang tertunda di awal permintaan berikutnya.

Contoh berikut mengaktifkan web fetch bersama dengan alat `run_command` yang didefinisikan pengguna dan menangani respons campuran:

<CodeGroup>
  ```bash cURL
  # Jika "stop_reason" adalah "tool_use" dan blok server_tool_use tidak memiliki
  # blok hasil yang cocok, panggilan itu belum selesai. Jalankan alat klien, lalu POST
  # lagi dengan satu pesan user tambahan yang hanya berisi blok tool_result mereka
  # dan array tools yang sama (lihat tab SDK).
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
          "content": "Summarize https://example.com/article and run uname -a to tell me what system this is on."
        }
      ],
      "tools": [
        {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5},
        {
          "name": "run_command",
          "description": "Run a shell command on this computer and return its output.",
          "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "The command to run"}},
            "required": ["command"]
          }
        }
      ]
    }' | jq '{stop_reason, content}'
  ```

  ```bash CLI
  # Jika "stop_reason" adalah "tool_use" dan blok server_tool_use tidak memiliki
  # blok hasil yang cocok, jalankan alat klien dan jalankan ulang dengan pesan user yang hanya
  # berisi blok tool_result mereka yang ditambahkan (lihat tab SDK).
  ant messages create --format json <<'YAML' | jq '{stop_reason, content}'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  tools:
    - {type: web_fetch_20250910, name: web_fetch, max_uses: 5}
    - name: run_command
      description: Run a shell command on this computer and return its output.
      input_schema:
        type: object
        properties:
          command: {type: string, description: The command to run}
        required: [command]
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  tools = [
      {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5},
      {
          "name": "run_command",
          "description": "Run a shell command on this computer and return its output.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "command": {"type": "string", "description": "The command to run"}
              },
              "required": ["command"],
          },
      },
  ]
  messages = [
      {
          "role": "user",
          "content": "Summarize https://example.com/article and run uname -a to tell me what system this is on.",
      }
  ]

  response = client.messages.create(
      model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages
  )

  tool_results = [
      {
          "type": "tool_result",
          "tool_use_id": block.id,
          # Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
          "content": "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux",
      }
      for block in response.content
      if block.type == "tool_use"
  ]

  if response.stop_reason == "tool_use" and tool_results:
      # Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
      # Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=tools,
          messages=[
              *messages,
              {"role": "assistant", "content": response.content},
              {"role": "user", "content": tool_results},
          ],
      )
      # Jika web_fetch ditangguhkan, ia berjalan pada permintaan ini dan
      # web_fetch_tool_result-nya adalah blok pertama dari continuation.content.
      print(continuation)
  else:
      print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const webFetchTool = {
    type: "web_fetch_20250910",
    name: "web_fetch",
    max_uses: 5
  } as const;
  const runCommandTool: Anthropic.Tool = {
    name: "run_command",
    description: "Run a shell command on this computer and return its output.",
    input_schema: {
      type: "object" as const,
      properties: {
        command: { type: "string", description: "The command to run" }
      },
      required: ["command"]
    }
  };
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content:
        "Summarize https://example.com/article and run uname -a to tell me what system this is on."
    }
  ];

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [webFetchTool, runCommandTool],
    messages
  });

  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        // Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
        content: "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
      });
    }
  }

  if (response.stop_reason === "tool_use" && toolResults.length > 0) {
    // Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
    // Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
    const continuation = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [webFetchTool, runCommandTool],
      messages: [
        ...messages,
        { role: "assistant", content: response.content },
        { role: "user", content: toolResults }
      ]
    });
    // Jika web_fetch ditangguhkan, ia dijalankan pada permintaan ini dan
    // web_fetch_tool_result-nya adalah blok pertama dari continuation.content.
    console.log(continuation);
  } else {
    console.log(response);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 }),
      new ToolUnion(new Tool()
      {
          Name = "run_command",
          Description = "Run a shell command on this computer and return its output.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["command"] = JsonSerializer.SerializeToElement(
                      new { type = "string", description = "The command to run" }
                  ),
              },
              Required = ["command"],
          },
      }),
  ];
  MessageParam userMessage = new()
  {
      Role = Role.User,
      Content = "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  };

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      Messages = [userMessage]
  });

  var toolResults = new List<ContentBlockParam>();
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
          {
              ToolUseID = toolUse.ID,
              // Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
              Content = "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux",
          }));
      }
  }

  if (response.StopReason?.Value() == StopReason.ToolUse && toolResults.Count > 0)
  {
      // Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
      // Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
      var continuation = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = tools,
          Messages =
          [
              userMessage,
              new()
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new() { Role = Role.User, Content = new MessageParamContent(toolResults) }
          ]
      });
      // Jika web_fetch ditangguhkan, ia dijalankan pada permintaan ini dan
      // web_fetch_tool_result-nya adalah blok pertama dari continuation.Content.
      Console.WriteLine(continuation);
  }
  else
  {
      Console.WriteLine(response);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  tools := []anthropic.ToolUnionParam{
  	{OfWebFetchTool20250910: &anthropic.WebFetchTool20250910Param{
  		MaxUses: anthropic.Int(5),
  	}},
  	{OfTool: &anthropic.ToolParam{
  		Name:        "run_command",
  		Description: anthropic.String("Run a shell command on this computer and return its output."),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"command": map[string]any{
  					"type":        "string",
  					"description": "The command to run",
  				},
  			},
  			Required: []string{"command"},
  		},
  	}},
  }
  userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize https://example.com/article and run uname -a to tell me what system this is on."))

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools:     tools,
  	Messages:  []anthropic.MessageParam{userMessage},
  })
  if err != nil {
  	log.Fatal(err)
  }

  var toolResults []anthropic.ContentBlockParamUnion
  for _, block := range response.Content {
  	if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  		// Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
  		output := "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
  		toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, output, false))
  	}
  }

  if response.StopReason == anthropic.StopReasonToolUse && len(toolResults) > 0 {
  	// Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
  	// Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
  	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages: []anthropic.MessageParam{
  			userMessage,
  			response.ToParam(),
  			anthropic.NewUserMessage(toolResults...),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	// Jika web_fetch ditangguhkan, ia dijalankan pada permintaan ini dan
  	// web_fetch_tool_result-nya adalah blok pertama dari continuation.Content.
  	fmt.Println(continuation)
  } else {
  	fmt.Println(response)
  }
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool runCommandTool = Tool.builder()
          .name("run_command")
          .description("Run a shell command on this computer and return its output.")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "command", Map.of("type", "string", "description", "The command to run")
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("command")))
              .build())
          .build();
      String prompt = "Summarize https://example.com/article and run uname -a to tell me what system this is on.";

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(WebFetchTool20250910.builder().maxUses(5L).build())
          .addTool(runCommandTool)
          .addUserMessage(prompt)
          .build());

      List<ContentBlockParam> toolResults = new ArrayList<>();
      for (ContentBlock block : response.content()) {
          block.toolUse().ifPresent(toolUse -> toolResults.add(ContentBlockParam.ofToolResult(
              ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  // Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
                  .content("Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux")
                  .build()
          )));
      }

      boolean isToolUse = response.stopReason()
          .map(StopReason.TOOL_USE::equals)
          .orElse(false);
      if (isToolUse && !toolResults.isEmpty()) {
          // Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
          // Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
          Message continuation = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(WebFetchTool20250910.builder().maxUses(5L).build())
              .addTool(runCommandTool)
              .addUserMessage(prompt)
              .addMessage(response)
              .addUserMessageOfBlockParams(toolResults)
              .build());
          // Jika web_fetch ditangguhkan, ia dijalankan pada permintaan ini dan
          // web_fetch_tool_result-nya adalah blok pertama dari continuation.content().
          IO.println(continuation);
      } else {
          IO.println(response);
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $tools = [
      ['type' => 'web_fetch_20250910', 'name' => 'web_fetch', 'max_uses' => 5],
      [
          'name' => 'run_command',
          'description' => "Run a shell command on this computer and return its output.",
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'command' => ['type' => 'string', 'description' => 'The command to run']
              ],
              'required' => ['command']
          ]
      ]
  ];
  $userMessage = ['role' => 'user', 'content' => 'Summarize https://example.com/article and run uname -a to tell me what system this is on.'];

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [$userMessage],
      model: 'claude-opus-4-8',
      tools: $tools,
  );

  $toolResults = [];
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolResults[] = [
              'type' => 'tool_result',
              'tool_use_id' => $block->id,
              // Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
              'content' => 'Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux'
          ];
      }
  }

  if ($response->stopReason === 'tool_use' && count($toolResults) > 0) {
      // Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
      // Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
      $continuation = $client->messages->create(
          maxTokens: 1024,
          messages: [
              $userMessage,
              ['role' => 'assistant', 'content' => $response->content],
              ['role' => 'user', 'content' => $toolResults],
          ],
          model: 'claude-opus-4-8',
          tools: $tools,
      );
      // Jika web_fetch ditangguhkan, ia berjalan pada permintaan ini dan
      // web_fetch_tool_result-nya adalah blok pertama dari $continuation->content.
      echo $continuation;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tools = [
    { type: "web_fetch_20250910", name: "web_fetch", max_uses: 5 },
    {
      name: "run_command",
      description: "Run a shell command on this computer and return its output.",
      input_schema: {
        type: "object",
        properties: {
          command: { type: "string", description: "The command to run" }
        },
        required: ["command"]
      }
    }
  ]
  user_message = {
    role: "user",
    content: "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  }

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    messages: [user_message]
  )

  tool_results = []
  response.content.each do |block|
    next unless block.type == :tool_use

    tool_results << {
      type: "tool_result",
      tool_use_id: block.id,
      # Jalankan alat Anda di sini. Contoh ini mengembalikan string tetap.
      content: "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
    }
  end

  if response.stop_reason == :tool_use && !tool_results.empty?
    # Blok server_tool_use tanpa blok hasil dalam respons ini belum selesai; hasilnya tiba di respons berikutnya.
    # Kirim kembali hanya blok tool_result klien, dengan alat yang sama.
    continuation = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: tools,
      messages: [
        user_message,
        { role: "assistant", content: response.content },
        { role: "user", content: tool_results }
      ]
    )
    # Jika web_fetch ditangguhkan, ia berjalan pada permintaan ini dan
    # web_fetch_tool_result-nya adalah blok pertama dari continuation.content.
    puts continuation
  else
    puts response
  end
  ```
</CodeGroup>

Kode ini juga benar ketika Claude tidak mencampur kedua jenis panggilan. Giliran dengan hanya blok `tool_use` klien mengambil jalur kelanjutan yang sama, dan giliran dengan hanya panggilan alat server tidak memerlukan blok `tool_result` klien dari Anda: blok hasilnya biasanya sudah ada, dan yang kembali dalam keadaan ditangguhkan, seperti [respons `pause_turn`](#the-server-side-loop-and-pause-turn), dikirim ulang apa adanya.

## ZDR dan allowed\_callers

Versi dasar dari pencarian web (`web_search_20250305`) dan web fetch (`web_fetch_20250910`) memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/manage-claude/api-and-data-retention).

Versi `_20260209` dan yang lebih baru dengan pemfilteran dinamis **tidak** memenuhi syarat ZDR secara default karena pemfilteran dinamis bergantung pada eksekusi kode secara internal.

Untuk menggunakan alat server `_20260209` atau yang lebih baru dengan ZDR, nonaktifkan pemfilteran dinamis dengan mengatur `"allowed_callers": ["direct"]` pada alat tersebut:

```json
{
  "type": "web_search_20260209",
  "name": "web_search",
  "allowed_callers": ["direct"]
}
```

Ini membatasi alat hanya untuk pemanggilan langsung, melewati langkah eksekusi kode internal.

`allowed_callers` mengontrol bagaimana alat dapat dipanggil: secara langsung oleh Claude (`"direct"`), dari dalam container eksekusi kode (misalnya, `"code_execution_20260120"`), atau keduanya. Versi `_20260209` dari alat web secara default hanya menggunakan pemanggil eksekusi kode; versi sebelumnya secara default menggunakan `["direct"]`. Pada model yang tidak mendukung pemanggilan alat terprogram, versi ini memerlukan `allowed_callers: ["direct"]`; tanpa itu API mengembalikan error validasi yang menyatakan untuk mengaturnya.

<Note>
  Bahkan ketika web fetch digunakan dalam konfigurasi yang memenuhi syarat ZDR, penerbit situs web mungkin menyimpan parameter apa pun yang diteruskan ke URL jika Claude mengambil konten dari situs mereka.
</Note>

## Pemfilteran domain

Alat server yang mengakses web menerima parameter `allowed_domains` dan `blocked_domains` untuk mengontrol domain mana yang dapat dijangkau Claude. Keduanya adalah field pada objek alat:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "allowed_domains": ["example.com", "docs.python.org"]
}
```

Saat menggunakan filter domain:

* Domain tidak boleh menyertakan skema HTTP/HTTPS (gunakan `example.com` alih-alih `https://example.com`).
* Subdomain secara otomatis disertakan (`example.com` mencakup `docs.example.com`).
* Subdomain spesifik membatasi hasil hanya ke subdomain tersebut (`docs.example.com` hanya mengembalikan hasil dari subdomain tersebut, bukan dari `example.com` atau `api.example.com`).
* Subpath didukung untuk pencarian web dan mencocokkan apa pun setelah path (`example.com/blog` cocok dengan `example.com/blog/post-1`).
* Web fetch hanya mencocokkan berdasarkan domain: entri yang menyertakan path tidak pernah cocok dengan URL web fetch.
* Anda dapat menggunakan `allowed_domains` atau `blocked_domains`, tetapi tidak keduanya dalam permintaan yang sama.

**Dukungan wildcard:**

* Wildcard (`*`) tidak diizinkan dalam domain itu sendiri, hanya dalam path setelahnya.
* Valid: `example.com/*`, `example.com/*/articles`
* Tidak valid: `*.example.com`, `ex*.com`

Format domain yang tidak valid ditolak pada saat permintaan dengan `invalid_request_error` 400.

<Note>
  Pembatasan domain tingkat permintaan bekerja bersama dengan pembatasan domain tingkat organisasi yang dikonfigurasi di Claude Console. `allowed_domains` tingkat permintaan harus merupakan subset dari daftar yang diizinkan tingkat organisasi; entri di luar itu menyebabkan API mengembalikan error validasi. Domain yang diblokir organisasi Anda dihapus dari daftar yang diizinkan tingkat permintaan alih-alih mengembalikan error.
</Note>

<Warning>
  Karakter Unicode dalam nama domain dapat melewati filter domain melalui serangan homograf: `аmazon.com` (dengan `а` Sirilik) terlihat identik dengan `amazon.com` tetapi merupakan domain yang berbeda. Gunakan nama domain yang hanya berisi ASCII dalam daftar izin dan blokir, dan audit entri yang ada untuk karakter non-ASCII.
</Warning>

## Pemfilteran dinamis dengan eksekusi kode

Versi `_20260209` dan yang lebih baru dari pencarian web dan web fetch menggunakan eksekusi kode secara internal untuk menerapkan filter dinamis terhadap hasil pencarian.

<Note>
  Anda tidak perlu menambahkan alat `code_execution` untuk versi ini: ketika pemfilteran dinamis berjalan, API menyediakan eksekusi kode untuk permintaan secara otomatis, dan kedua alat berbagi satu container eksekusi. Jika Anda menyertakannya, gunakan `code_execution_20260120` atau yang lebih baru; API menolak versi eksekusi kode yang lebih lama bersama dengan versi alat web ini.
</Note>

## Streaming event alat server

Event alat server di-stream sebagai bagian dari alur "server-sent events" (event yang dikirim server), atau SSE, yang normal. Blok `server_tool_use` yang dipanggil Claude secara langsung di-stream seperti blok `tool_use` klien: event `content_block_start` diikuti oleh event `input_json_delta`. Blok hasil tiba lengkap dalam satu event `content_block_start`, tanpa delta.

Lihat [Streaming](/docs/id/build-with-claude/streaming) untuk referensi event lengkap. Halaman alat individual mendokumentasikan nama event spesifik alat jika berbeda.

## Permintaan batch

Semua alat server mendukung pemrosesan batch. Dalam batch, loop agentik berjalan sama seperti untuk permintaan sinkron, dengan batas iterasi per giliran yang lebih tinggi. Jika loop mencapai batas tersebut, respons berakhir dengan `stop_reason: "pause_turn"`; Anda dapat melanjutkannya dengan mengirimkan permintaan lanjutan dengan konten yang dikembalikan. Lihat [Alat server dan loop agentik](/docs/id/build-with-claude/batch-processing#server-tools-and-the-agentic-loop) untuk detailnya.

Beban kerja batch yang umum mencakup memperkaya dataset dengan informasi dari web, memeriksa sekumpulan besar dokumen terhadap sumber terkini, dan menjalankan kode analisis pada banyak file.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Pemecahan masalah penggunaan alat" icon="wrench" href="/docs/id/agents-and-tools/tool-use/troubleshooting-tool-use">
    Perbaiki error penggunaan alat yang paling umum dengan tabel diagnostik gejala-ke-perbaikan.
  </Card>

  <Card title="Alat pencarian web" icon="browser" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Cari di web dan kutip hasilnya.
  </Card>

  <Card title="Alat web fetch" icon="download" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil dan baca konten dari URL tertentu untuk memperkaya konteks Claude dengan konten web langsung.
  </Card>

  <Card title="Alat eksekusi kode" icon="terminal" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam container sandbox untuk menganalisis data, menghasilkan file, dan melakukan iterasi pada solusi.
  </Card>

  <Card title="Alat pencarian alat" icon="compass" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Temukan dan muat alat sesuai permintaan.
  </Card>
</CardGroup>
