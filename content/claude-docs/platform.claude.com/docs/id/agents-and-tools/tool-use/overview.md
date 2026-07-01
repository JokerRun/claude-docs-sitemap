---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 0406c4ee436ecdfcc1f6d839a2edac737f290f19421b07f1a342a0b170d55662
---

# Penggunaan alat dengan Claude

Hubungkan Claude ke alat dan API eksternal. Lihat di mana alat dieksekusi, kapan Claude memanggilnya, dan alat mana yang sesuai dengan tugas Anda.

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

Claude menjalankan pencarian pada infrastruktur Anthropic dan mengembalikan hasil yang disertai sitasi dalam respons yang sama. Agar Claude memanggil fungsi yang Anda definisikan, berikan alat dengan `input_schema`, lalu eksekusi panggilan tersebut ketika Claude mengembalikan blok `tool_use`. [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools) dan [Menangani panggilan alat](/docs/id/agents-and-tools/tool-use/handle-tool-calls) membahas siklus bolak-balik tersebut.

## Cara kerja penggunaan alat

Alat dibedakan terutama berdasarkan di mana kodenya dieksekusi. **Alat klien** (termasuk alat yang didefinisikan pengguna dan alat dengan skema yang didefinisikan Anthropic, seperti `bash` dan `text_editor`) berjalan di aplikasi Anda. Claude merespons dengan `stop_reason: "tool_use"` dan satu atau lebih blok `tool_use`. Kode Anda mengeksekusi operasi tersebut dan mengirimkan kembali `tool_result`. **Alat server** (seperti `web_search`, `web_fetch`, `code_execution`, dan `tool_search`) berjalan pada infrastruktur Anthropic: Anda melihat hasilnya secara langsung tanpa menangani eksekusi, kecuali Claude memanggil alat tersebut dalam kelompok panggilan alat paralel yang sama dengan salah satu alat klien Anda (lihat [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons#tool-use)).

Untuk model konseptual lengkap termasuk loop agentik dan kapan memilih setiap pendekatan, lihat [Cara kerja penggunaan alat](/docs/id/agents-and-tools/tool-use/how-tool-use-works).

Untuk menghubungkan ke server Model Context Protocol (MCP), lihat [MCP connector](/docs/id/agents-and-tools/mcp-connector). Untuk membangun klien MCP Anda sendiri, lihat panduan Model Context Protocol untuk [membangun klien MCP](https://modelcontextprotocol.io/docs/develop/build-client).

## Kapan Claude menggunakan alat

Dengan `tool_choice` default `{"type": "auto"}`, Claude menentukan pada setiap giliran apakah akan memanggil alat atau merespons secara langsung. Claude memanggil alat ketika permintaan sesuai dengan kemampuan yang dijelaskan alat tersebut dan jawabannya belum ada dalam konteks. Claude merespons secara langsung untuk pengetahuan yang stabil, tugas kreatif, dan giliran percakapan biasa.

Batasan ini dapat diarahkan melalui prompt sistem Anda. Jika Claude tidak memanggil alat saat Anda mengharapkannya, instruksi ringan seperti `"Use the tools to investigate before responding."` akan meningkatkan penggunaan alat. Bentuk yang lebih kuat seperti `"Always call a tool first before responding."` mendorong lebih jauh. Sebaliknya, `"Use your judgment about whether to call a tool or respond directly."` menjaga perilaku pemicu tetap konservatif.

Untuk mewajibkan panggilan alat alih-alih mengandalkan prompting, atur [`tool_choice`](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).

<Tip>
  **Jamin kesesuaian skema dengan strict tool use**

  Tambahkan `strict: true` ke definisi alat kustom Anda untuk memastikan panggilan alat Claude selalu cocok persis dengan skema Anda. Lihat [Strict tool use](/docs/id/agents-and-tools/tool-use/strict-tool-use).
</Tip>

Setiap halaman alat server menjelaskan batasan pemicunya sendiri secara lebih rinci.

<Accordion title="Ketika parameter wajib tidak tersedia">
  Jika prompt pengguna tidak menyertakan informasi yang cukup untuk mengisi semua parameter wajib suatu alat, Claude Opus jauh lebih mungkin mengenali bahwa ada parameter yang hilang dan menanyakannya. Claude Sonnet mungkin bertanya, terutama ketika diminta untuk berpikir sebelum mengeluarkan permintaan alat. Tetapi Claude Sonnet juga mungkin menyimpulkan nilai yang masuk akal.

  Misalnya, diberikan alat `get_weather` yang memerlukan parameter `location`, jika Anda bertanya kepada Claude "What's the weather?" tanpa menentukan lokasi, Claude (khususnya Claude Sonnet) mungkin menebak nilai yang tidak Anda berikan:

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
  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tentukan skema alat, tulis deskripsi, dan kontrol kapan Claude memanggil alat Anda.
  </Card>

  <Card title="Menangani panggilan alat" icon="arrows-left-right" href="/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Parse blok `tool_use`, format respons `tool_result`, dan tangani error.
  </Card>
</CardGroup>

### Alat klien dengan skema Anthropic

Anthropic menerbitkan skemanya dan melatih Claude dengannya. Aplikasi Anda tetap mengeksekusi setiap panggilan dan mengembalikan `tool_result`.

<CardGroup cols={2}>
  <Card title="Alat Memory" icon="brain" href="/docs/id/agents-and-tools/tool-use/memory-tool">
    Simpan dan ambil informasi lintas percakapan dalam file yang Anda kontrol.
  </Card>

  <Card title="Alat Bash" icon="terminal" href="/docs/id/agents-and-tools/tool-use/bash-tool">
    Jalankan perintah shell dalam sesi persisten yang mempertahankan state.
  </Card>

  <Card title="Alat Text editor" icon="edit" href="/docs/id/agents-and-tools/tool-use/text-editor-tool">
    Lihat dan modifikasi file teks untuk debug, memperbaiki, dan meningkatkan kode.
  </Card>

  <Card title="Alat Computer use" icon="computer" href="/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Ambil tangkapan layar dan kontrol mouse serta keyboard di lingkungan desktop.
  </Card>
</CardGroup>

### Alat server

Alat server berjalan pada infrastruktur Anthropic, tanpa kode handler di aplikasi Anda. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools) untuk mekanisme yang mereka miliki bersama.

<CardGroup cols={2}>
  <Card title="Alat Web search" icon="browser" href="/docs/id/agents-and-tools/tool-use/web-search-tool">
    Cari informasi di web di luar batas pengetahuan, dengan sumber yang disitasi.
  </Card>

  <Card title="Alat Web fetch" icon="download" href="/docs/id/agents-and-tools/tool-use/web-fetch-tool">
    Ambil konten lengkap dari halaman web dan dokumen PDF yang ditentukan.
  </Card>

  <Card title="Alat Code execution" icon="code" href="/docs/id/agents-and-tools/tool-use/code-execution-tool">
    Jalankan kode Python dan bash dalam kontainer sandbox untuk menganalisis data dan menghasilkan file.
  </Card>

  <Card title="Alat Advisor" icon="lightbulb" href="/docs/id/agents-and-tools/tool-use/advisor-tool">
    Biarkan model eksekutor yang lebih cepat berkonsultasi dengan model advisor yang lebih cerdas di tengah proses generasi.
  </Card>

  <Card title="Alat Tool search" icon="library" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Bekerja dengan ribuan alat dengan menemukan dan memuatnya sesuai kebutuhan.
  </Card>

  <Card title="MCP connector" icon="link" href="/docs/id/agents-and-tools/mcp-connector">
    Hubungkan ke server MCP jarak jauh dari Messages API tanpa klien MCP terpisah.
  </Card>
</CardGroup>

<Note>
  [Claude Managed Agents](/docs/id/managed-agents/overview) menyediakan toolset bawaan yang digunakan Claude secara otonom dalam sebuah sesi. Untuk toolset tersebut dan cara Managed Agents menambahkan alat kustom, lihat halaman [Tools](/docs/id/managed-agents/tools)-nya.
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

Lihat tabel [Ikhtisar model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk harga per model saat ini.

Ketika Anda mengirim prompt penggunaan alat, seperti permintaan API lainnya, respons menyertakan jumlah token input dan output dalam metrik `usage` yang dilaporkan.

Beberapa alat server menambahkan biaya berbasis penggunaan di atas token: lihat [Alat Web search](/docs/id/agents-and-tools/tool-use/web-search-tool#usage-and-pricing) dan [Alat Code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk tarifnya.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card href="/docs/id/agents-and-tools/tool-use/how-tool-use-works" title="Cara kerja penggunaan alat" icon="compass">
    Pahami loop penggunaan alat, di mana alat dieksekusi, dan kapan menggunakan alat alih-alih prosa.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/build-a-tool-using-agent" title="Tutorial: Membangun agen yang menggunakan alat" icon="graduation-cap">
    Panduan langkah demi langkah dari satu panggilan alat hingga loop agentik yang siap produksi.
  </Card>

  <Card href="/docs/id/agents-and-tools/tool-use/tool-reference" title="Referensi alat" icon="book">
    Direktori alat yang disediakan Anthropic dan referensi untuk properti definisi alat opsional.
  </Card>
</CardGroup>
