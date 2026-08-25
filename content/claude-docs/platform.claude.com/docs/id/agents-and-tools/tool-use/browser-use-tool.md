---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 4c31974d7d9150aa984c45b40478f82b042e6254bd0e4fdf3c3ab8a9e16b6bb3
---

---
title: Alat penggunaan browser
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool
description: Biarkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di lingkungan browser Anda sendiri dengan alat penggunaan browser.
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): eligible (excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))
- Supported models: `claude-fable-5`, `claude-mythos-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-opus-4-8`
- Platforms: Claude API; not available on Claude Platform on AWS, Amazon Bedrock, Google Cloud, Microsoft Foundry

"Browser use tool" (alat penggunaan browser) memungkinkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di browser yang dijalankan oleh aplikasi Anda. Alat ini bekerja dengan halaman baik melalui strukturnya ("accessibility tree" (pohon aksesibilitas), elemen, formulir, dan tab) maupun melalui piksel ("screenshot" (tangkapan layar) dan koordinat viewport), sedangkan [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja dengan seluruh desktop hanya melalui tangkapan layar dan koordinat. Ini adalah [toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) yang didefinisikan Anthropic: satu entri `browser_toolset_20260801` dalam array `tools` Anda memberi Claude 27 "member tools" (alat anggota) secara default, seperti `navigate`, `read_page`, `left_click`, dan `screenshot`, ditambah empat lagi (`javascript_exec`, `file_upload`, `read_console`, dan `read_network`) ketika Anda [mengaktifkannya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools). Aplikasi Anda menjalankan setiap panggilan terhadap otomatisasi browsernya sendiri; tidak ada yang berjalan di sisi Anthropic. Alat ini saat ini tidak tersedia di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/tools). Halaman ini menggunakan istilah "aplikasi Anda" untuk loop agen yang memanggil Messages API dan "eksekutor Anda" untuk bagian darinya yang mengendalikan browser dan menghasilkan hasil alat.

Pilih penggunaan browser daripada penggunaan komputer ketika tugas tetap berada di dalam halaman web: Claude dapat membaca struktur halaman, bertindak pada elemen berdasarkan referensi selain berdasarkan koordinat, mengatur nilai formulir secara langsung, dan bekerja lintas tab, dan Anda tidak perlu menjalankan desktop. Jika Claude hanya perlu membaca halaman yang dapat Anda tunjukkan, atau menemukan sumber di web, [alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) dan [alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) bahkan lebih ringan, karena keduanya adalah [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) yang dijalankan API untuk Anda tanpa browser yang perlu dioperasikan. Pilih penggunaan browser sebagai gantinya ketika halaman membangun kontennya dengan JavaScript atau tugasnya berarti bertindak pada halaman, bukan hanya membacanya.

Dengan penggunaan browser, Claude membaca dan bertindak pada halaman web langsung, sehingga semua yang disediakan halaman adalah input yang tidak tepercaya dan tindakan yang diambil Claude dapat memiliki efek nyata. Lihat [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations) sebelum Anda melakukan deployment.

## Mulai cepat

Alat penggunaan browser tersedia di Claude API tanpa header beta: tambahkan satu entri bertipe `browser_toolset_20260801`, tanpa `name`, ke array `tools` dari permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 2048,
      "tools": [
        {
          "type": "browser_toolset_20260801"
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Open example.com/docs and tell me how to get started."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 2048
  tools:
    - type: browser_toolset_20260801
  messages:
    - role: user
      content: Open example.com/docs and tell me how to get started.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=2048,
      tools=[{"type": "browser_toolset_20260801"}],
      messages=[
          {
              "role": "user",
              "content": "Open example.com/docs and tell me how to get started.",
          }
      ],
  )
  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 2048,
    tools: [{ type: "browser_toolset_20260801" }],
    messages: [
      {
        role: "user",
        content: "Open example.com/docs and tell me how to get started."
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 2048,
      Tools = [new BrowserToolset20260801()],
      Messages =
      [
          new MessageParam
          {
              Role = Role.User,
              Content = "Open example.com/docs and tell me how to get started.",
          },
      ],
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 2048,
  	Tools: []anthropic.ToolUnionParam{
  		{OfBrowserToolset20260801: &anthropic.BrowserToolset20260801Param{}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Open example.com/docs and tell me how to get started.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.BrowserToolset20260801;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(2048L)
          .addTool(BrowserToolset20260801.builder().build())
          .addUserMessage("Open example.com/docs and tell me how to get started.")
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 2048,
      messages: [
          ['role' => 'user', 'content' => 'Open example.com/docs and tell me how to get started.'],
      ],
      model: 'claude-opus-5',
      tools: [
          ['type' => 'browser_toolset_20260801'],
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 2048,
    tools: [
      { type: "browser_toolset_20260801" }
    ],
    messages: [
      {
        role: "user",
        content: "Open example.com/docs and tell me how to get started."
      }
    ]
  )

  puts response
  ```
</CodeGroup>

Respons pertama Claude berakhir dengan `stop_reason: "tool_use"` dan membawa satu atau lebih blok `tool_use` anggota, masing-masing menyebutkan alat anggota di `name` dan membawa `"toolset_name": "browser"`:

```json Output
{
  "id": "msg_01HCDu4XSTLzTAcodEQ58vDo",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-5",
  "content": [
    {
      "type": "text",
      "text": "I'll open the documentation and read the page to find the getting-started instructions."
    },
    {
      "type": "tool_use",
      "id": "toolu_01NRLabsLyVHZPKxbKvkfSMn",
      "name": "navigate",
      "toolset_name": "browser",
      "input": { "url": "https://example.com/docs" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01UvHU5cDyTZ2vXKf5wCkPqR",
      "name": "read_page",
      "toolset_name": "browser",
      "input": { "filter": "interactive" }
    }
  ],
  "stop_reason": "tool_use",
  "stop_sequence": null
}
```

Eksekutor Anda menjalankan `navigate`, lalu `read_page`, dan aplikasi Anda mengembalikan satu `tool_result` per blok dalam permintaan berikutnya, menggemakan `toolset_name` pada masing-masing. Hasil `navigate` melaporkan tab yang dimuatnya dalam blok `browser_state`; hasil `read_page` adalah teks di mana setiap elemen membawa referensi:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01NRLabsLyVHZPKxbKvkfSMn",
      "toolset_name": "browser",
      "content": [
        { "type": "text", "text": "Navigated to https://example.com/docs" },
        {
          "type": "browser_state",
          "tabs": [
            {
              "tab_id": "tab-1",
              "title": "Documentation",
              "url": "https://example.com/docs",
              "active": true
            }
          ]
        }
      ]
    },
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01UvHU5cDyTZ2vXKf5wCkPqR",
      "toolset_name": "browser",
      "content": [
        {
          "type": "text",
          "text": "link \"Documentation\" [ref_1]\nlink \"Getting started\" [ref_2]\ntextbox \"Search docs\" [ref_3]\nbutton \"Search\" [ref_4]\nlink \"Pricing\" [ref_5]"
        }
      ]
    }
  ]
}
```

Claude sekarang memegang referensi yang dapat ditindaklanjutinya, sehingga giliran berikutnya dapat mengklik `ref_2` untuk membuka halaman getting-started, tanpa perlu menemukan tautan tersebut dalam tangkapan layar terlebih dahulu.

## Cara kerja penggunaan browser

Penggunaan browser berjalan sebagai "agent loop" (loop agen): Claude mengembalikan panggilan alat anggota, eksekutor Anda menjalankannya terhadap browser, dan Anda mengembalikan hasilnya hingga Claude menjawab dalam teks.

<Steps>
  <Step title="Berikan Claude alat penggunaan browser dan prompt pengguna" icon="tool">
    * Tambahkan entri `browser_toolset_20260801`, dan secara opsional alat lain, ke permintaan API Anda.
    * Sertakan prompt pengguna yang memerlukan pekerjaan dengan halaman web, misalnya, "Buka example.com/docs dan beri tahu saya cara memulai."
  </Step>

  <Step title="Claude merespons dengan panggilan alat anggota" icon="wrench">
    * Claude mengembalikan satu atau lebih blok `tool_use` dalam satu giliran asisten; beberapa blok dalam satu giliran membentuk aksi batch, misalnya, `left_click`, lalu `type`, lalu `key`.
    * `name` setiap blok adalah nama anggota, masing-masing membawa `"toolset_name": "browser"`, dan `input` hanya berisi parameter anggota tersebut, tanpa field `action`. `stop_reason` respons adalah `tool_use`.
  </Step>

  <Step title="Jalankan panggilan secara berurutan dan kembalikan hasilnya" icon="browser">
    * Iterasi setiap blok `tool_use` dalam `response.content` (jangan berasumsi hanya ada satu) dan jalankan secara berurutan, sesuai urutan kemunculannya, karena panggilan yang lebih belakang biasanya bergantung pada yang lebih awal.
    * Kembalikan satu `tool_result` per blok dalam pesan `user` baru, dicocokkan berdasarkan `tool_use_id`, dan gemakan `"toolset_name": "browser"` pada masing-masing. Setiap panggilan harus dijawab atau permintaan berikutnya akan ditolak.
    * Jika sebuah panggilan gagal, kembalikan `is_error: true` dengan deskripsi teks untuk blok tersebut, lalu terapkan aturan penghentian di [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) pada setiap blok berikutnya dalam giliran itu.
  </Step>

  <Step title="Claude melanjutkan hingga tugas selesai" icon="arrows-clockwise">
    * Claude membaca hasilnya (teks halaman, pohon aksesibilitas, tangkapan layar, status tab) dan, jika membutuhkan lebih banyak, mengembalikan panggilan anggota lebih lanjut, yang membawa Anda kembali ke langkah 3.
    * Jika tidak, Claude mengembalikan respons teks kepada pengguna.
  </Step>
</Steps>

Berikut kerangka langkah panggilan alat dari loop tersebut dalam dua bagian. Pertama, handler anggota stub menggantikan otomatisasi browser Anda. Lima anggota (`navigate`, `read_page`, `left_click`, `type`, dan `screenshot`) mengembalikan teks, atau untuk `screenshot` blok gambar, yang menjadi konten hasil, dan dispatcher memunculkan error untuk anggota apa pun yang tidak diimplementasikannya.

<CodeGroup exclude="shell">
  ```python Python
  # Data gambar placeholder; eksekutor nyata menangkap viewport dan mengembalikan byte PNG
  PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


  def navigate(url):
      return f"navigated to {url}"


  def read_page():
      return 'link "Docs" [ref_1]\nbutton "Search" [ref_2]'


  def click(target):
      # Target adalah referensi elemen dari read_page atau find, atau koordinat viewport
      if target["type"] == "ref":
          return f"clicked {target['ref']}"
      return f"clicked at ({target['x']}, {target['y']})"


  def type_text(text):
      return f"typed: {text}"


  def capture_screenshot() -> list[ImageBlockParam]:
      # screenshot menjawab dengan blok gambar, bukan teks: kembalikan daftar konten hasil
      return [
          {
              "type": "image",
              "source": {"type": "base64", "media_type": "image/png", "data": PLACEHOLDER_PNG},
          }
      ]


  def handle_browser_action(name, tool_input):
      if name == "navigate":
          return navigate(tool_input["url"])
      elif name == "read_page":
          return read_page()
      elif name == "left_click":
          return click(tool_input["target"])
      elif name == "type":
          return type_text(tool_input["text"])
      elif name == "screenshot":
          return capture_screenshot()
      # Tangani aksi lain sesuai kebutuhan
      raise ValueError(f"Unknown or unimplemented member: {name}")
  ```

  ```typescript TypeScript
  // Data gambar placeholder; executor nyata menangkap viewport sebagai byte PNG
  const PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

  function navigate(url: string): string {
    return `navigated to ${url}`;
  }

  function readPage(): string {
    return 'link "Docs" [ref_1]\nbutton "Search" [ref_2]';
  }

  function clickElement(ref: string): string {
    return `clicked ${ref}`;
  }

  function clickAt(x: number, y: number): string {
    return `clicked at (${x}, ${y})`;
  }

  function typeText(text: string): string {
    return `typed: ${text}`;
  }

  function captureScreenshot(): Anthropic.ImageBlockParam[] {
    // screenshot menjawab dengan blok gambar, bukan teks
    return [
      {
        type: "image",
        source: {
          type: "base64",
          media_type: "image/png",
          data: PLACEHOLDER_PNG,
        },
      },
    ];
  }

  function handleBrowserAction(
    action: string,
    input: unknown,
  ): string | Anthropic.ImageBlockParam[] {
    const params: object =
      typeof input === "object" && input !== null ? input : {};
    if (action === "navigate" && "url" in params) {
      return navigate(String(params.url));
    } else if (action === "read_page") {
      return readPage();
    } else if (action === "left_click" && "target" in params) {
      // target adalah referensi elemen dari read_page atau koordinat viewport
      const target: object =
        typeof params.target === "object" && params.target !== null
          ? params.target
          : {};
      if ("type" in target && target.type === "ref" && "ref" in target) {
        return clickElement(String(target.ref));
      } else if ("x" in target && "y" in target) {
        return clickAt(Number(target.x), Number(target.y));
      }
    } else if (action === "type" && "text" in params) {
      return typeText(String(params.text));
    } else if (action === "screenshot") {
      return captureScreenshot();
    }
    // Tangani aksi lain sesuai kebutuhan
    throw new Error(`Unknown or unimplemented member: ${action}`);
  }
  ```

  ```csharp C#
  // Data gambar placeholder; eksekutor nyata menangkap viewport dan mengembalikan byte PNG
  const string PlaceholderPng = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

  string Navigate(string url) => $"navigated to {url}";

  string ReadPage() =>
      """
      link "Docs" [ref_1]
      button "Search" [ref_2]
      """;

  string ClickRef(string elementRef) => $"clicked {elementRef}";

  string ClickAt(int x, int y) => $"clicked at ({x}, {y})";

  // target berupa {"type": "ref", "ref": "ref_1"} atau {"type": "coordinate", "x": 640, "y": 380}
  string Click(JsonElement target) =>
      target.GetProperty("type").GetString() == "ref"
          ? ClickRef(target.GetProperty("ref").GetString()!)
          : ClickAt(target.GetProperty("x").GetInt32(), target.GetProperty("y").GetInt32());

  string TypeText(string text) => $"typed: {text}";

  // screenshot menjawab dengan blok gambar, bukan teks: kembalikan daftar konten hasil
  List<Block> CaptureScreenshot() =>
      [
          new ImageBlockParam(
              new Base64ImageSource { Data = PlaceholderPng, MediaType = MediaType.ImagePng }
          ),
      ];

  ToolResultBlockParamContent HandleBrowserAction(
      string action,
      IReadOnlyDictionary<string, JsonElement> input
  ) =>
      action switch
      {
          "navigate" => Navigate(input["url"].GetString()!),
          "read_page" => ReadPage(),
          "left_click" => Click(input["target"]),
          "type" => TypeText(input["text"].GetString()!),
          "screenshot" => CaptureScreenshot(),
          // Tangani aksi lain sesuai kebutuhan
          _ => throw new NotSupportedException($"Unknown or unimplemented member: {action}"),
      };
  ```

  ```go Go
  // placeholderPNG menggantikan tangkapan layar asli: executor mengembalikan
  // viewport sebagai data PNG yang dienkode base64.
  const placeholderPNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

  // textContent membungkus teks sebagai konten tool_result.
  func textContent(text string) []anthropic.ToolResultBlockParamContentUnion {
  	return []anthropic.ToolResultBlockParamContentUnion{
  		{OfText: &anthropic.TextBlockParam{Text: text}},
  	}
  }

  func navigate(url string) string {
  	return fmt.Sprintf("navigated to %s", url)
  }

  func readPage() string {
  	return "link \"Docs\" [ref_1]\nbutton \"Search\" [ref_2]"
  }

  func clickRef(ref string) string {
  	return fmt.Sprintf("clicked %s", ref)
  }

  func clickAt(x, y int) string {
  	return fmt.Sprintf("clicked at (%d, %d)", x, y)
  }

  func typeText(text string) string {
  	return fmt.Sprintf("typed: %s", text)
  }

  // captureScreenshot mengembalikan blok gambar, bukan teks.
  func captureScreenshot() []anthropic.ToolResultBlockParamContentUnion {
  	return []anthropic.ToolResultBlockParamContentUnion{{
  		OfImage: &anthropic.ImageBlockParam{
  			Source: anthropic.ImageBlockParamSourceUnion{
  				OfBase64: &anthropic.Base64ImageSourceParam{
  					MediaType: anthropic.Base64ImageSourceMediaTypeImagePNG,
  					Data:      placeholderPNG,
  				},
  			},
  		},
  	}}
  }

  func handleBrowserAction(action string, params map[string]any) ([]anthropic.ToolResultBlockParamContentUnion, error) {
  	switch action {
  	case "navigate":
  		if url, ok := params["url"].(string); ok {
  			return textContent(navigate(url)), nil
  		}
  	case "read_page":
  		return textContent(readPage()), nil
  	case "left_click":
  		// target berupa referensi elemen dari read_page atau koordinat viewport
  		target, _ := params["target"].(map[string]any)
  		if ref, ok := target["ref"].(string); ok && target["type"] == "ref" {
  			return textContent(clickRef(ref)), nil
  		}
  		x, xok := target["x"].(float64)
  		y, yok := target["y"].(float64)
  		if xok && yok {
  			return textContent(clickAt(int(x), int(y))), nil
  		}
  	case "type":
  		if text, ok := params["text"].(string); ok {
  			return textContent(typeText(text)), nil
  		}
  	case "screenshot":
  		return captureScreenshot(), nil
  	// Tangani aksi lain sesuai kebutuhan
  	default:
  		return nil, fmt.Errorf("unknown or unimplemented member: %s", action)
  	}
  	// Tercapai saat input anggota kehilangan field atau field bertipe salah
  	return nil, fmt.Errorf("invalid input for %s", action)
  }

  ```

  ```java Java
  /** Placeholder pixels; a real executor captures the viewport and base64-encodes the PNG. */
  static final String PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

  ToolResultBlockParam.Content captureScreenshot() {
      ImageBlockParam image = ImageBlockParam.builder()
              .source(Base64ImageSource.builder()
                      .mediaType(Base64ImageSource.MediaType.IMAGE_PNG)
                      .data(PLACEHOLDER_PNG)
                      .build())
              .build();
      return ToolResultBlockParam.Content.ofBlocks(
              List.of(ToolResultBlockParam.Content.Block.ofImage(image)));
  }

  String navigate(String url) {
      return "navigated to " + url;
  }

  String readPage() {
      return """
              link "Docs" [ref_1]
              button "Search" [ref_2]""";
  }

  String clickRef(String ref) {
      return "clicked " + ref;
  }

  String clickAt(long x, long y) {
      return "clicked at (" + x + ", " + y + ")";
  }

  String typeText(String text) {
      return "typed: " + text;
  }

  /** Runs one browser toolset member; {@code action} is the tool_use block's name. */
  ToolResultBlockParam.Content handleBrowserAction(String action, Map<String, JsonValue> input) {
      if (action.equals("screenshot")) {
          return captureScreenshot(); // the one member here that answers with an image block
      }
      String output = switch (action) {
          case "navigate" -> navigate(input.get("url").asStringOrThrow());
          case "read_page" -> readPage();
          case "left_click" -> {
              // target berupa {"type": "ref", "ref": "ref_1"} atau {"type": "coordinate", "x": 640, "y": 380}
              Map<String, JsonValue> target =
                      (Map<String, JsonValue>) input.get("target").asObject().get();
              if (target.get("type").asStringOrThrow().equals("ref")) {
                  yield clickRef(target.get("ref").asStringOrThrow());
              }
              long x = ((Number) target.get("x").asNumber().get()).longValue();
              long y = ((Number) target.get("y").asNumber().get()).longValue();
              yield clickAt(x, y);
          }
          case "type" -> typeText(input.get("text").asStringOrThrow());
          // Tangani aksi lain sesuai kebutuhan
          default -> throw new UnsupportedOperationException("Unknown or unimplemented member: " + action);
      };
      return ToolResultBlockParam.Content.ofString(output);
  }
  ```

  ```php PHP
  // Pengganti untuk byte PNG asli; executor nyata menangkap viewport
  const PLACEHOLDER_PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';

  function navigateTo(string $url): string
  {
      return "navigated to {$url}";
  }

  function readPage(): string
  {
      return <<<'TEXT'
          link "Docs" [ref_1]
          button "Search" [ref_2]
          TEXT;
  }

  function clickTarget(array $target): string
  {
      // Target adalah referensi elemen dari read_page atau find, atau koordinat piksel viewport
      if ($target['type'] === 'ref') {
          return "clicked {$target['ref']}";
      }

      return "clicked at ({$target['x']}, {$target['y']})";
  }

  function typeText(string $text): string
  {
      return "typed: {$text}";
  }

  function captureScreenshot(): array
  {
      // screenshot menjawab dengan blok gambar, bukan teks, jadi kembalikan daftar konten hasil
      $image = [
          'type' => 'image',
          'source' => ['type' => 'base64', 'media_type' => 'image/png', 'data' => PLACEHOLDER_PNG],
      ];

      return [$image];
  }

  function handleBrowserAction(string $name, array $input): string|array
  {
      return match ($name) {
          'navigate' => navigateTo($input['url']),
          'read_page' => readPage(),
          'left_click' => clickTarget($input['target']),
          'type' => typeText($input['text']),
          'screenshot' => captureScreenshot(),
          // Tangani aksi lain sesuai kebutuhan
          default => throw new RuntimeException("Unknown or unimplemented member: {$name}"),
      };
  }
  ```

  ```ruby Ruby
  # Data gambar pengganti; eksekutor nyata menangkap viewport sebagai PNG.
  PLACEHOLDER_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

  def navigate(url)
    "navigated to #{url}"
  end

  def read_page
    <<~TREE
      link "Docs" [ref_1]
      button "Search" [ref_2]
    TREE
  end

  def click(target)
    return "clicked #{target[:ref]}" if target[:type] == "ref"

    "clicked at (#{target[:x]}, #{target[:y]})"
  end

  def type_text(text)
    "typed: #{text}"
  end

  def capture_screenshot
    [
      {
        type: "image",
        source: { type: "base64", media_type: "image/png", data: PLACEHOLDER_PNG }
      }
    ]
  end

  def handle_browser_action(name, input)
    case name
    when "navigate"
      navigate(input[:url])
    when "read_page"
      read_page
    when "left_click"
      # target adalah referensi elemen (dari read_page atau find) atau koordinat
      click(input[:target])
    when "type"
      type_text(input[:text])
    when "screenshot"
      capture_screenshot
    # Tangani aksi lain sesuai kebutuhan
    else
      raise ArgumentError, "Unknown or unimplemented member: #{name}"
    end
  end
  ```
</CodeGroup>

Bagian kedua menjalankan batch secara berurutan, mengirim setiap blok ke handler tersebut, menggemakan `toolset_name` pada setiap hasil, dan menerapkan aturan penghentian dari [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions), mengubah error handler menjadi hasil error. Loop sampling yang memanggilnya adalah yang ditunjukkan di [Memahami loop agen](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#understanding-the-agentic-loop), dengan toolset browser di `tools`.

<CodeGroup exclude="shell">
  ```python Python
  NOT_EXECUTED = "Not executed: an earlier action in this turn failed."


  def process_tool_calls(response: Message) -> list[ToolResultBlockParam]:
      """
      Run the browser actions in Claude's response in order and answer each
      one. After the first failure the rest are skipped, because Claude planned
      them assuming the earlier actions succeeded.
      """
      tool_results: list[ToolResultBlockParam] = []
      failed = False
      for block in response.content:
          # Hanya toolset browser yang dideklarasikan; arahkan alat lain ke sini jika Anda menambahkannya
          if block.type != "tool_use" or block.toolset_name != "browser":
              continue
          result: ToolResultBlockParam = {
              "type": "tool_result",
              "tool_use_id": block.id,
              "toolset_name": "browser",
          }
          if failed:
              result["content"] = NOT_EXECUTED
              result["is_error"] = True
          else:
              try:
                  # String atau daftar blok konten; eksekutor nyata juga menambahkan
                  # blok browser_state ke hasil navigasi dan pengelolaan tab
                  result["content"] = handle_browser_action(block.name, block.input)
              except Exception as err:
                  result["content"] = f"Error: {err}"
                  result["is_error"] = True
                  failed = True
          tool_results.append(result)
      return tool_results
  ```

  ```typescript TypeScript
  const HALT_TEXT = "Not executed: an earlier action in this turn failed.";

  function browserResult(
    toolUseId: string,
    content: string | Anthropic.ImageBlockParam[],
    isError?: boolean,
  ): Anthropic.ToolResultBlockParam {
    return {
      type: "tool_result",
      tool_use_id: toolUseId,
      toolset_name: "browser",
      content,
      is_error: isError,
    };
  }

  function processToolCalls(
    response: Anthropic.Message,
  ): Anthropic.ToolResultBlockParam[] {
    const toolResults: Anthropic.ToolResultBlockParam[] = [];
    let failed = false;
    for (const block of response.content) {
      if (block.type !== "tool_use") {
        continue;
      }
      if (block.toolset_name !== "browser") {
        // Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain
        // ke sini jika Anda menambahkannya.
        continue;
      }
      if (failed) {
        // Batch berhenti pada kegagalan pertama; jawab aksi berikutnya sebagai tidak dieksekusi
        toolResults.push(browserResult(block.id, HALT_TEXT, true));
        continue;
      }
      try {
        // String atau daftar blok gambar; executor nyata juga menambahkan
        // blok browser_state ke hasil navigasi dan manajemen tab
        const result = handleBrowserAction(block.name, block.input);
        toolResults.push(browserResult(block.id, result));
      } catch (error) {
        failed = true;
        const message = error instanceof Error ? error.message : String(error);
        toolResults.push(browserResult(block.id, `Error: ${message}`, true));
      }
    }
    return toolResults;
  }
  ```

  ```csharp C#
  const string HaltText = "Not executed: an earlier action in this turn failed.";

  List<ContentBlockParam> ProcessToolCalls(Message response)
  {
      List<ContentBlockParam> toolResults = [];
      var failed = false;
      foreach (var block in response.Content)
      {
          if (!block.TryPickToolUse(out var toolUse))
          {
              continue;
          }

          if (toolUse.ToolsetName != "browser")
          {
              // Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain
              // ke sini jika Anda menambahkannya.
              continue;
          }

          if (failed)
          {
              // Batch berhenti pada kegagalan pertama; jawab aksi berikutnya tanpa menjalankannya
              toolResults.Add(
                  new ToolResultBlockParam(toolUse.ID)
                  {
                      Content = HaltText,
                      IsError = true,
                      ToolsetName = "browser",
                  }
              );
              continue;
          }

          try
          {
              // String atau daftar blok konten; eksekutor nyata juga menambahkan
              // blok browser_state ke hasil navigasi dan pengelolaan tab
              var result = HandleBrowserAction(toolUse.Name, toolUse.Input);
              toolResults.Add(
                  new ToolResultBlockParam(toolUse.ID) { Content = result, ToolsetName = "browser" }
              );
          }
          catch (Exception e)
          {
              failed = true;
              toolResults.Add(
                  new ToolResultBlockParam(toolUse.ID)
                  {
                      Content = $"Error: {e.Message}",
                      IsError = true,
                      ToolsetName = "browser",
                  }
              );
          }
      }
      return toolResults;
  }
  ```

  ```go Go
  const notExecuted = "Not executed: an earlier action in this turn failed."

  // browserToolResult membangun hasil untuk satu aksi browser. Berbeda dengan
  // hasil alat biasa, ia harus menyertakan kembali nama toolset. Executor asli juga
  // menambahkan blok browser_state ke hasil navigasi dan pengelolaan tab.
  func browserToolResult(toolUseID string, content []anthropic.ToolResultBlockParamContentUnion, isError bool) anthropic.ContentBlockParamUnion {
  	result := anthropic.ToolResultBlockParam{
  		ToolUseID:   toolUseID,
  		ToolsetName: anthropic.String("browser"),
  		Content:     content,
  	}
  	if isError {
  		result.IsError = anthropic.Bool(true)
  	}
  	return anthropic.ContentBlockParamUnion{OfToolResult: &result}
  }

  // processToolCalls menjalankan aksi browser dalam respons Claude secara berurutan dan
  // membangun satu tool_result per blok tool_use. Setelah kegagalan pertama, sisanya
  // dilewati: Claude merencanakannya dengan asumsi aksi sebelumnya berhasil.
  func processToolCalls(response *anthropic.Message) []anthropic.ContentBlockParamUnion {
  	var toolResults []anthropic.ContentBlockParamUnion
  	failed := false
  	for _, block := range response.Content {
  		switch variant := block.AsAny().(type) {
  		case anthropic.ToolUseBlock:
  			// Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain ke sini jika Anda menambahkannya.
  			if variant.ToolsetName != "browser" {
  				continue
  			}
  			if failed {
  				toolResults = append(toolResults, browserToolResult(variant.ID, textContent(notExecuted), true))
  				continue
  			}
  			var input map[string]any
  			var content []anthropic.ToolResultBlockParamContentUnion
  			err := json.Unmarshal(variant.Input, &input)
  			if err == nil {
  				content, err = handleBrowserAction(variant.Name, input)
  			}
  			if err != nil {
  				failed = true
  				content = textContent("Error: " + err.Error())
  			}
  			toolResults = append(toolResults, browserToolResult(variant.ID, content, err != nil))
  		}
  	}
  	return toolResults
  }

  ```

  ```java Java
  /** The exact text the toolset contract prescribes for member calls skipped after a failure. */
  static final String HALT_TEXT = "Not executed: an earlier action in this turn failed.";

  /** Every result answering a browser toolset member echoes toolset_name. */
  ToolResultBlockParam.Builder browserResult(ToolUseBlock toolUse) {
      return ToolResultBlockParam.builder()
              .toolUseId(toolUse.id())
              .toolsetName("browser");
  }

  /**
   * Run the browser actions in Claude's response in order and build one
   * tool_result per tool_use block. After the first failure, skip the rest:
   * Claude planned them assuming the earlier actions succeeded.
   */
  List<ContentBlockParam> processToolCalls(Message response) {
      List<ContentBlockParam> toolResults = new ArrayList<>();
      boolean failed = false;
      for (ContentBlock block : response.content()) {
          // Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain ke sini jika Anda menambahkannya.
          if (!block.isToolUse() || !block.asToolUse().toolsetName().equals(Optional.of("browser"))) {
              continue;
          }
          ToolUseBlock toolUse = block.asToolUse();
          ToolResultBlockParam result;
          if (failed) {
              result = browserResult(toolUse).content(HALT_TEXT).isError(true).build();
          } else {
              try {
                  Map<String, JsonValue> input =
                          (Map<String, JsonValue>) toolUse._input().asObject().get();
                  ToolResultBlockParam.Content output = handleBrowserAction(toolUse.name(), input);
                  // Executor sungguhan juga menambahkan blok browser_state ke hasil navigasi dan
                  // manajemen tab; lihat "Lacak tab dengan browser_state" di halaman ini.
                  result = browserResult(toolUse).content(output).build();
              } catch (RuntimeException e) {
                  failed = true;
                  result = browserResult(toolUse).content("Error: " + e.getMessage()).isError(true).build();
              }
          }
          toolResults.add(ContentBlockParam.ofToolResult(result));
      }
      return toolResults;
  }
  ```

  ```php PHP
  const HALT_TEXT = 'Not executed: an earlier action in this turn failed.';

  function processToolCalls(Message $response): array
  {
      $toolResults = [];
      $failed = false;
      foreach ($response->content as $block) {
          // Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain ke sini jika Anda menambahkannya.
          if (!($block instanceof ToolUseBlock) || $block->toolsetName !== 'browser') {
              continue;
          }
          $result = ['type' => 'tool_result', 'tool_use_id' => $block->id, 'toolset_name' => 'browser'];
          if ($failed) {
              // Batch berhenti pada kegagalan pertama; aksi sisanya dijawab tanpa dijalankan
              $toolResults[] = [...$result, 'content' => HALT_TEXT, 'is_error' => true];
              continue;
          }
          try {
              // Executor nyata juga mengembalikan blok browser_state pada hasil navigasi dan manajemen tab
              $toolResults[] = [...$result, 'content' => handleBrowserAction($block->name, $block->input)];
          } catch (Throwable $e) {
              $failed = true;
              $toolResults[] = [...$result, 'content' => 'Error: ' . $e->getMessage(), 'is_error' => true];
          }
      }

      return $toolResults;
  }
  ```

  ```ruby Ruby
  NOT_EXECUTED = "Not executed: an earlier action in this turn failed."

  # Jalankan aksi browser dalam respons Claude secara berurutan dan buat satu
  # tool_result per blok tool_use. Setelah kegagalan pertama, lewati sisanya:
  # Claude merencanakannya dengan asumsi aksi sebelumnya berhasil.
  def process_tool_calls(response)
    tool_results = []
    failed = false
    response.content.each do |block|
      # Contoh ini hanya mendeklarasikan toolset browser; arahkan alat lain ke sini
      # jika Anda menambahkannya.
      next unless block.type == :tool_use && block.toolset_name == "browser"

      result = { type: "tool_result", tool_use_id: block.id, toolset_name: "browser" }
      if failed
        result.update(content: NOT_EXECUTED, is_error: true)
      else
        begin
          # Sebuah String, atau blok konten untuk screenshot. Eksekutor nyata juga menambahkan
          # blok browser_state ke hasil navigasi dan pengelolaan tab.
          result[:content] = handle_browser_action(block.name, block.input)
        rescue => e
          result.update(content: "Error: #{e.message}", is_error: true)
          failed = true
        end
      end
      tool_results << result
    end
    tool_results
  end
  ```
</CodeGroup>

Kirim setiap blok berdasarkan pasangan (`toolset_name`, `name`) bukan berdasarkan `name` saja, karena alat kustom dalam permintaan yang sama mungkin memiliki nama yang sama dengan anggota; [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) menjelaskan bagian-bagian kontrak ini yang dimiliki bersama oleh kedua toolset. Jika Claude menyebutkan anggota yang tidak diimplementasikan eksekutor Anda, atau yang Anda nonaktifkan, jawab blok tersebut dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor) daripada membuangnya.

Ketika Anda melakukan streaming respons, `input` setiap anggota tiba sebagai satu `input_json_delta` lengkap, bukan sebagai fragmen, jadi tunggu hingga giliran selesai sebelum menjalankan batch.

### Aksi batch

Giliran dengan beberapa panggilan anggota adalah "batch action" (aksi batch): jalankan panggilan sesuai urutan kemunculannya, berhenti pada kegagalan pertama, dan jawab setiap panggilan berikutnya dengan `is_error: true` dan teks persis `Not executed: an earlier action in this turn failed.` Batch menggunakan bentuk respons yang sama dengan [penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use); perbedaannya adalah Anda menjalankan blok secara berurutan, bukan secara bersamaan. Di sini Claude mengklik kotak pencarian yang ditemukannya sebelumnya, mengetik kueri, dan menekan Enter dalam satu giliran:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
      "name": "left_click",
      "toolset_name": "browser",
      "input": { "target": { "type": "ref", "ref": "ref_3" } }
    },
    {
      "type": "tool_use",
      "id": "toolu_01Ez4kLb1nQ2vXo8sJ9pWm3c",
      "name": "type",
      "toolset_name": "browser",
      "input": { "text": "install" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01FkP8rTz6uYh2mNq4LsXw7v",
      "name": "key",
      "toolset_name": "browser",
      "input": { "text": "Enter" }
    }
  ]
}
```

Aplikasi Anda mengembalikan tiga blok `tool_result` dalam satu pesan `user`, masing-masing membawa `toolset_name` dan pengakuan teks singkat seperti `Clicked element ref_3.` Menekan Enter memuat halaman hasil, sehingga hasil `key` juga membawa blok `browser_state` dengan URL tab yang diperbarui ([Konteks tab pada hasil lain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-context-on-other-results)). Jika klik tersebut gagal, hasilnya akan membawa teks error Anda dan dua hasil lainnya akan membawa teks penghentian, seperti ditunjukkan di [Mengembalikan error dari eksekutor Anda](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor).

Anda tidak perlu mengembalikan tangkapan layar setelah setiap panggilan. Claude biasanya mengakhiri batch dengan panggilan observasi (`screenshot`, `read_page`, atau `get_page_text`), dan aplikasi Anda juga dapat melampirkan observasinya sendiri, seperti tangkapan layar baru atau pohon aksesibilitas, sebagai blok konten tambahan pada hasil terakhir dalam batch untuk menghemat satu round trip. Karena hasil manajemen tab harus berupa tepat satu blok `browser_state`, lampirkan pada hasil terakhir yang bukan panggilan manajemen tab.

Jika eksekutor Anda hanya dapat menjalankan satu panggilan per round trip, atur `disable_parallel_tool_use` ke `true` di `tool_choice` dan Claude mengembalikan paling banyak satu panggilan anggota per giliran, dengan biaya lebih banyak round trip ([Menonaktifkan penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use#disable-parallel-tool-use)). Sisa kontrak di [Aksi batch untuk alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions) tetap berlaku, termasuk satu `tool_result` untuk setiap `tool_use` dalam pesan `user` berikutnya, kecuali dua hal: teks penghentian dan apa yang dimuat `content` dari hasil yang berhasil. Konten hasil mengikuti [Alat anggota](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#member-tools) di halaman ini sebagai gantinya: hasil `new_tab`, `switch_tab`, `close_tab`, atau `list_tabs` adalah tepat satu blok `browser_state` tanpa teks atau gambar ([Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results)), dan hasil anggota lainnya dapat menambahkan blok `browser_state` ke teks atau gambarnya ([Konteks tab pada hasil lain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-context-on-other-results)). Di mana breakpoint cache di dalam batch berlaku dijelaskan di baris `cache_control` pada [Parameter alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#tool-parameters) alat penggunaan komputer.

### Target dan koordinat

Alat anggota yang bertindak pada suatu lokasi menerima objek `target`, yang berupa koordinat piksel viewport atau referensi ke elemen yang dikembalikan `read_page` atau `find`. Tabel [Alat anggota](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#member-tools) menulis `Target` untuk parameter yang menerima salah satu bentuk.

| Bentuk             | `target.type`  | Field                                      | Diterima oleh                                                                                                                                                                             |
| ------------------ | -------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CoordinateTarget` | `"coordinate"` | `x`, `y` (integer, piksel viewport)        | `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `hover`, `left_click_drag` (`from` dan `target`), `left_mouse_down`, `left_mouse_up`, `mouse_move`, `scroll` |
| `RefTarget`        | `"ref"`        | `ref` (referensi elemen seperti `"ref_2"`) | `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `hover`, `scroll_to`, `form_input`, `file_upload`                                                            |

**Koordinat adalah piksel viewport**, ruang piksel dari `screenshot` viewport penuh dengan titik asal di kiri atas halaman yang dirender; tidak ada desktop atau bingkai jendela di sekelilingnya. Toolset tidak mendeklarasikan dimensi tampilan dan Claude menyimpulkan ukuran viewport dari tangkapan layar yang Anda kembalikan, jadi pertahankan satu ukuran yang konsisten. `zoom` tidak mengubah bingkai, sehingga `region`-nya dan koordinat apa pun yang dikeluarkan Claude setelah melihat gambar yang diperbesar tetap merupakan piksel viewport penuh.

**Tangkapan layar harus sesuai dengan batas gambar.** API tidak memperkecil gambar toolset: tangkapan layar atau gambar zoom yang melebihi [batas ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) model Anda, atau melebihi batas per gambar yang lebih ketat yang berlaku setelah permintaan memuat [lebih dari 20 gambar](https://platform.claude.com/docs/id/build-with-claude/vision#request-limits), akan ditolak. Ubah ukuran sebelum mengembalikan, dan skalakan kembali koordinat Claude dengan kebalikan faktor Anda sebelum mengirimkannya ([Mengukur tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)).

**Referensi elemen berasal dari `read_page` dan `find`.** Setiap elemen dalam outputnya membawa tag seperti `[ref_2]`, seperti pada hasil Mulai cepat:

```text wrap
link "Documentation" [ref_1]
link "Getting started" [ref_2]
textbox "Search docs" [ref_3]
button "Search" [ref_4]
link "Pricing" [ref_5]
```

Claude mengirimkan kembali referensi sebagai target `{"type": "ref", "ref": "ref_2"}` pada panggilan klik, `hover`, `scroll_to`, `form_input`, atau `file_upload` berikutnya, atau sebagai parameter `ref` pada `read_page` untuk membaca subpohon. Eksekutor Anda menetapkan referensi, menyimpan pemetaan dari masing-masing ke node yang mendasarinya (ID node aksesibilitas, selector tersimpan, atau yang setara), dan bertindak pada node tersebut ketika referensi kembali.

Referensi dibatasi pada tab yang menghasilkannya dan tetap valid hingga tab tersebut bernavigasi atau DOM-nya berubah secara material. API tidak dapat mendeteksi referensi yang kedaluwarsa atau tidak dikenal, jadi ketika Claude mengirimkan referensi yang tidak lagi dikenali eksekutor Anda, kembalikan hasil error seperti `Error: ref_3 is stale or not found on the current page. Re-read the page to get fresh references.` Claude kemudian membaca halaman lagi. Jangan menomori ulang referensi yang sudah Anda berikan untuk sebuah tab hingga tab tersebut bernavigasi, karena itu secara diam-diam membatalkan referensi yang masih dipegang Claude.

Claude menggunakan kedua gaya penargetan dan beralih di antaranya berdasarkan apa yang diekspos halaman; prompt Anda dan apa yang dikembalikan eksekutor Anda mengarahkan pilihan tersebut:

* **Utamakan referensi di mana halaman memiliki pohon aksesibilitas yang dapat digunakan.** Referensi bertahan dari pergeseran tata letak dan reflow yang membuat koordinat piksel rapuh, dan memungkinkan Claude bertindak pada kontrol yang sulit dikenai dengan pointer.
* **Kembali ke koordinat untuk konten yang tidak dijelaskan pohon.** Antarmuka yang dirender canvas, video tersemat atau permukaan remote-desktop, daftar yang sangat tervirtualisasi, dan elemen di dalam iframe lintas-origin sering tidak memiliki node yang berguna, sehingga Claude bekerja dari `screenshot` dan `zoom` dan mengklik berdasarkan koordinat; eksekutor Anda menentukan frame mana yang dikenai koordinat.
* **Batasi cakupan pembacaan, dan baca pohon sebelum Anda mengambil tangkapan layar.** Pada halaman besar, `read_page` dengan `filter: "interactive"` atau `ref` dari sebuah kontainer mengembalikan subpohon yang terfokus, dan pembacaan pohon dari halaman biasa sering menghabiskan lebih sedikit token input daripada tangkapan layar sambil memberi Claude referensi yang dapat langsung ditindaklanjuti. Tangkapan layar tetap menjadi observasi yang tepat ketika tata letak visual, gambar, atau status rendering penting.

## Pertimbangan keamanan

Penggunaan browser membawa risiko yang tidak dimiliki fitur API standar, karena Claude membaca dan bertindak pada konten dari web terbuka, di mana halaman apa pun dapat berisi teks yang ditulis untuk memanipulasinya.

<Warning>
  Untuk mengurangi risiko ini, ambil tindakan pencegahan seperti berikut:

  1. Jalankan browser dan eksekutor Anda dalam container atau mesin virtual khusus dengan hak akses minimal, profil baru yang tidak menyimpan kredensial, dan tanpa akses ke filesystem sensitif atau jaringan internal; isolasi alat apa pun yang Anda jalankan bersamanya dengan cara yang sama.
  2. Batasi host yang dapat dijangkau browser ke allowlist domain yang diberlakukan di lapisan jaringan dan diperiksa ulang di handler `navigate` Anda setelah redirect, dan blokir rentang loopback, link-local, dan privat kecuali tugas membutuhkannya.
  3. Perlakukan semua yang disediakan halaman sebagai input yang tidak tepercaya, termasuk judul tab dan URL yang Anda laporkan dalam blok [`browser_state`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state), dan bangun pembacaan halaman dari apa yang dirender halaman (pohon aksesibilitas atau teks yang terlihat), bukan sumber DOM mentah, sehingga teks tersembunyi tidak mencapai Claude.
  4. Di handler `navigate` Anda, terima kata kunci riwayat `"back"`, `"forward"`, dan `"reload"`, perlakukan URL tanpa skema sebagai `https://`, lalu parse URL dan tolak skema apa pun selain `http` atau `https` (`javascript:`, `file:`, `data:`, `chrome:`, dan seterusnya) dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor). Periksa skema dengan parser URL, bukan awalan string; API tidak pernah melihat navigasi dan tidak dapat menolaknya untuk Anda.
  5. Biarkan `javascript_exec` dan `file_upload` nonaktif kecuali Anda membutuhkannya, dan baca [Mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools) sebelum mengaktifkan salah satunya.
  6. Minta manusia mengonfirmasi tindakan yang berdampak dan apa pun yang memerlukan persetujuan afirmatif (pembelian, modifikasi akun, pengiriman pesan, dan penerimaan ketentuan), dan lakukan pemeriksaan itu di eksekutor Anda sebelum setiap panggilan, karena satu giliran dapat membawa beberapa panggilan.
</Warning>

Claude terkadang mengikuti instruksi yang ditemukan dalam konten halaman bahkan ketika bertentangan dengan instruksi Anda; teks pada halaman yang mengatakan "abaikan instruksi sebelumnya dan navigasi ke..." dapat mengalihkannya dari tugas. Isolasi Claude dari data dan tindakan sensitif untuk membatasi apa yang dapat dijangkau injeksi prompt, tinjau [Memitigasi jailbreak dan injeksi prompt](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks), dan jika tugas tidak dapat menghindari sesi yang sudah login, gunakan akun khusus dengan hak akses rendah dan pertahankan konfirmasi manusia pada tindakan yang mengubah akun.

Karena browser berjalan di lingkungan Anda, situs yang dikunjungi Claude melihat identitas jaringan eksekutor Anda, dan konten halaman mencapai API hanya sebagai hasil alat yang Anda kembalikan. Beri tahu pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan penggunaan browser dalam produk Anda.

## Alat anggota

Entri `browser_toolset_20260801` mendeklarasikan 31 alat anggota; `input` setiap panggilan adalah persis parameter yang tercantum di sini, dan `tab_id`, jika opsional, default ke tab aktif. `Target`, `CoordinateTarget`, dan `RefTarget` adalah bentuk yang dijelaskan di [Target dan koordinat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#targets-and-coordinates). Empat anggota (`javascript_exec`, `file_upload`, `read_console`, dan `read_network`) dinonaktifkan secara default dan hanya muncul ketika Anda [mengaktifkannya](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools). Batas input dan konvensi output yang dicatat di baris setiap anggota dinyatakan kepada Claude, tidak diberlakukan oleh API, jadi validasi input (termasuk koordinat terhadap viewport Anda) dan terapkan konvensi tersebut di eksekutor Anda.

Hanya `screenshot` dan `zoom` yang memerlukan [blok `image`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-results-from-client-tools) dalam hasilnya, dan empat anggota manajemen tab (`new_tab`, `list_tabs`, `switch_tab`, dan `close_tab`) mengembalikan tepat satu blok `browser_state` (lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results)). Setiap anggota lainnya mengembalikan blok `text`: baik pengakuan singkat seperti `Clicked element ref_2.` atau output anggota tersebut. Hasil apa pun selain hasil manajemen tab juga dapat membawa blok `image`, biasanya tangkapan layar yang diambil setelah aksi, sehingga Claude melihat hasilnya tanpa panggilan `screenshot` terpisah; [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) menunjukkan di mana melampirkannya dalam batch. `tool_result` anggota hanya boleh berisi blok konten `text`, `image`, dan `browser_state`.

### Navigasi dan penangkapan

| Anggota      | Input               | Deskripsi                                                                                                                                                                                                                                                                                        |
| ------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `navigate`   | `url`, `tab_id?`    | Muat URL `http` atau `https`, atau bergerak melalui riwayat dengan `"back"`, `"forward"`, atau `"reload"`. Perlakukan URL tanpa skema sebagai `https://` dan tolak skema lain dengan hasil error. Kembalikan pengakuan singkat, ditambah blok `browser_state` ketika URL atau judul tab berubah. |
| `screenshot` | `tab_id?`           | Tangkap viewport dan kembalikan blok `image`.                                                                                                                                                                                                                                                    |
| `zoom`       | `region`, `tab_id?` | Kembalikan `image` yang dipotong dan diperbesar dari `region`, diberikan sebagai `[x0, y0, x1, y1]` dalam piksel viewport, untuk pemeriksaan lebih dekat terhadap teks atau kontrol kecil.                                                                                                       |

### Pointer

| Anggota           | Input                                                                       | Deskripsi                                                                                                                                                         |
| ----------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `left_click`      | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri pada koordinat atau elemen yang direferensikan. `modifiers` adalah chord yang ditahan selama klik, misalnya, `"shift"` atau `"ctrl+shift"`.             |
| `right_click`     | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kanan pada koordinat atau elemen.                                                                                                                            |
| `middle_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik tengah pada koordinat atau elemen.                                                                                                                           |
| `double_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri ganda pada koordinat atau elemen.                                                                                                                       |
| `triple_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri tiga kali pada koordinat atau elemen, yang biasanya memilih satu baris atau paragraf.                                                                   |
| `hover`           | `target: Target`, `tab_id?`                                                 | Gerakkan pointer ke atas koordinat atau elemen tanpa mengklik.                                                                                                    |
| `left_click_drag` | `from: CoordinateTarget`, `target: CoordinateTarget`, `tab_id?`             | Tekan di `from`, seret ke `target`, dan lepaskan.                                                                                                                 |
| `left_mouse_down` | `target: CoordinateTarget`, `tab_id?`                                       | Tekan dan tahan tombol kiri pada koordinat; pasangkan dengan `left_mouse_up` untuk seret kustom.                                                                  |
| `left_mouse_up`   | `target: CoordinateTarget`, `tab_id?`                                       | Lepaskan tombol kiri pada koordinat.                                                                                                                              |
| `mouse_move`      | `target: CoordinateTarget`, `tab_id?`                                       | Gerakkan pointer ke koordinat.                                                                                                                                    |
| `scroll`          | `target: CoordinateTarget`, `scroll_direction`, `scroll_amount?`, `tab_id?` | Gulir pada posisi viewport. `scroll_direction` adalah `"up"`, `"down"`, `"left"`, atau `"right"`; `scroll_amount` dalam takik roda gulir, 1 hingga 10, default 3. |
| `scroll_to`       | `target: RefTarget`, `tab_id?`                                              | Gulir elemen yang direferensikan hingga terlihat.                                                                                                                 |

### Keyboard dan pengaturan waktu

| Anggota    | Input                         | Deskripsi                                                                                                                                                                                                          |
| ---------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`     | `text`, `tab_id?`             | Ketik string literal pada fokus saat ini.                                                                                                                                                                          |
| `key`      | `text`, `repeat?`, `tab_id?`  | Tekan tombol atau chord. `text` adalah satu tombol (`"Enter"`), chord yang digabung dengan `+` (`"ctrl+a"`), atau urutan yang dipisahkan spasi (`"Backspace Backspace"`); `repeat` adalah 1 hingga 100, default 1. |
| `hold_key` | `text`, `duration`, `tab_id?` | Tahan tombol atau chord selama `duration` detik, 0 hingga 30.                                                                                                                                                      |
| `wait`     | `duration`, `tab_id?`         | Jeda selama `duration` detik, 0 hingga 30.                                                                                                                                                                         |

### Pembacaan halaman

| Anggota         | Input                                  | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_page`     | `filter?`, `depth?`, `ref?`, `tab_id?` | Kembalikan pohon aksesibilitas halaman sebagai teks dengan setiap elemen ditandai dengan referensi seperti `[ref_2]`. Dengan `filter` dihilangkan, kembalikan setiap elemen yang terlihat; dengan `"interactive"`, hanya elemen interaktif yang terlihat; dengan `"all"`, juga elemen di luar viewport. `depth` membatasi kedalaman pohon (minimum 1, default 15) dan `ref` membatasi pembacaan ke subpohon elemen tersebut. Batasi output pada 50.000 karakter dan nyatakan demikian dalam teks; Claude kemudian mempersempit dengan `depth` yang lebih kecil atau `ref`. |
| `find`          | `query`, `tab_id?`                     | Cari elemen yang cocok dengan deskripsi bahasa alami seperti `"search field"` atau `"add to cart button"`, dan kembalikan hingga 20 kecocokan dalam format bertanda yang sama dengan `read_page`.                                                                                                                                                                                                                                                                                                                                                                          |
| `get_page_text` | `tab_id?`                              | Kembalikan teks halaman yang terlihat sebagai teks biasa, memprioritaskan konten artikel utama; cocok untuk artikel, dokumentasi, dan halaman lain yang padat teks.                                                                                                                                                                                                                                                                                                                                                                                                        |

### Formulir dan file

| Anggota                                 | Input                                                     | Deskripsi                                                                                                                                                                                                                                                                                  |
| --------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `form_input`                            | `target: RefTarget`, `value`, `tab_id?`                   | Atur nilai elemen formulir secara langsung. `value` adalah `string`, `number`, atau `boolean`; gunakan `boolean` untuk checkbox dan nilai opsi atau teks yang terlihat untuk select.                                                                                                       |
| `file_upload` (nonaktif secara default) | `target: RefTarget`, `paths?`, `document_ids?`, `tab_id?` | Atur file pada elemen file-input dari `paths` di filesystem eksekutor, `document_ids` yang telah disiapkan aplikasi Anda, atau keduanya; setidaknya satu diperlukan. Lihat [Mengunggah file](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#upload-files). |

### Diagnostik dan scripting

| Anggota                                     | Input             | Deskripsi                                                                                                                                                                                                                                                                                         |
| ------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_console` (nonaktif secara default)    | `tab_id?`         | Kembalikan entri konsol tab (baris log, peringatan, dan error) yang terakumulasi sejak pembacaan terakhir, satu baris per entri. Lihat [Membaca aktivitas konsol dan jaringan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#read-console-and-network-activity). |
| `read_network` (nonaktif secara default)    | `tab_id?`         | Kembalikan permintaan jaringan tab (metode, URL, status, tipe MIME, waktu) sejak pembacaan terakhir, satu baris per entri.                                                                                                                                                                        |
| `javascript_exec` (nonaktif secara default) | `text`, `tab_id?` | Jalankan `text` sebagai JavaScript dalam konteks halaman dan kembalikan nilai ekspresi terakhir sebagai teks. Lihat [Mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools).                                 |

### Manajemen tab

| Anggota      | Input            | Deskripsi                       |
| ------------ | ---------------- | ------------------------------- |
| `new_tab`    | (tidak ada)      | Buka tab dan jadikan tab aktif. |
| `list_tabs`  | (tidak ada)      | Laporkan inventaris tab.        |
| `switch_tab` | `tab_id` (wajib) | Jadikan `tab_id` tab aktif.     |
| `close_tab`  | `tab_id` (wajib) | Tutup `tab_id`.                 |

Jika berhasil, masing-masing mengembalikan tepat satu blok `browser_state` dan tanpa teks atau gambar; lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results).

## Mengonfigurasi toolset

Selain `type`, entri toolset menerima `configs`, `cache_control`, dan `allowed_callers`; aturan yang dimiliki bersama field ini dengan toolset penggunaan komputer tercantum di [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets), dan bagian ini mencakup default khusus browser. `configs` adalah objek yang dikunci berdasarkan nama anggota, dan nilai setiap anggota menerima dua field:

| Field           | Default                                                                                                                                                             | Arti                                                                                                                                                                                                                                                                                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`       | `true`, kecuali `false` untuk empat [anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools) | Apakah anggota ditawarkan kepada Claude.                                                                                                                                                                                                                                                                                                                                    |
| `defer_loading` | `false`                                                                                                                                                             | Apakah definisi toolset ditangguhkan untuk pencarian alat. Harus menghasilkan nilai yang sama pada setiap anggota yang diaktifkan. Dengan empat anggota opsional dibiarkan nonaktif, menangguhkan toolset berarti mengaturnya pada 27 anggota lainnya; lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets). |

### Mengaktifkan atau menonaktifkan alat anggota

Cantumkan hanya anggota yang ingin Anda ubah di `configs`; setiap anggota yang Anda hilangkan mempertahankan defaultnya. Misalnya, eksekutor yang mengimplementasikan pembacaan konsol tetapi tidak kontrol pointer tingkat rendah atau penahanan tombol mengaktifkan `read_console` dan menahan tiga anggota:

```json
{
  "type": "browser_toolset_20260801",
  "configs": {
    "read_console": { "enabled": true },
    "left_mouse_down": { "enabled": false },
    "left_mouse_up": { "enabled": false },
    "hold_key": { "enabled": false }
  }
}
```

Anggota yang dinonaktifkan menghilang dari definisi yang dilihat Claude; itu tidak menjamin Claude tidak pernah menyebutkannya, jadi eksekutor Anda tetap menjawab panggilan seperti itu dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor).

### Menggabungkan dengan alat lain

Deklarasikan alat penggunaan browser bersama alat Anda sendiri dan alat lain yang disediakan Anthropic dalam array `tools` yang sama. Alat kustom boleh memiliki nama yang sama dengan anggota (`navigate` Anda sendiri, misalnya), karena `toolset_name` membedakan panggilan Claude, tetapi tidak ada entri lain yang boleh bernama `browser`, dan permintaan hanya boleh berisi satu entri toolset browser.

Anda juga dapat mendeklarasikannya bersama [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), baik toolset maupun versi alat penggunaan komputer yang lebih lama. Keduanya bekerja secara independen, masing-masing dalam bingkai koordinatnya sendiri (piksel viewport di sini, piksel tangkapan layar desktop di sana), dan panggilan Claude ke anggota yang memiliki nama yang sama, seperti `screenshot` atau `key`, dibedakan oleh `toolset_name`.

## Mengaktifkan anggota opsional

Empat alat anggota dinonaktifkan secara default: `javascript_exec` dan `file_upload` karena memperluas apa yang dapat dibuat halaman yang dimanipulasi agar dilakukan Claude, dan `read_console` dan `read_network` karena tidak setiap stack otomatisasi browser dapat menyediakan log tersebut dan keduanya memperluas konten yang dikendalikan halaman yang mencapai Claude. Aktifkan masing-masing dengan `configs` (misalnya, `"configs": {"file_upload": {"enabled": true}}`) hanya ketika eksekutor Anda mengimplementasikannya dan tugas membutuhkannya.

### Mengunggah file

`file_upload` mengatur file pada elemen `<input type="file">` secara langsung, yang lebih andal daripada mengendalikan pemilih file native. `target`-nya hanya berupa referensi, karena panggilan membutuhkan identitas elemen, dan menerima `paths`, `document_ids`, atau keduanya:

* `paths` adalah path file di filesystem eksekutor, untuk deployment di mana eksekutor dapat membaca file aplikasi Anda secara langsung (kondisi yang sama di mana Anda mengisi `path` unduhan).
* `document_ids` adalah pengenal untuk file yang telah disiapkan aplikasi Anda untuk browser, untuk deployment di mana eksekutor tidak dapat melakukannya. Aplikasi Anda mendefinisikan arti pengenal tersebut; batasi resolusinya seperti Anda membatasi `paths`, ke file yang disiapkan untuk tugas ini.

```json
{
  "type": "tool_use",
  "id": "toolu_01N7gVzFEfZjLjgsYwnrPgrF",
  "name": "file_upload",
  "toolset_name": "browser",
  "input": {
    "target": { "type": "ref", "ref": "ref_12" },
    "paths": ["/home/user/uploads/summary.pdf"],
    "tab_id": "tab-2"
  }
}
```

Claude menulis path ini saat membaca halaman yang tidak tepercaya, sehingga implementasi tanpa batasan akan memungkinkan halaman berbahaya mengarahkan pengunggahan file apa pun yang dapat dibaca eksekutor ke situs yang dikendalikan halaman tersebut. Aktifkan anggota ini hanya ketika eksekutor Anda me-resolve setiap path (mengikuti symlink dan segmen `..`) dan tidak menerima apa pun di luar direktori unggahan khusus yang masuk allowlist dan hanya berisi file yang dimaksudkan untuk tugas. Jangan gunakan ulang direktori unduhan browser untuk ini; jika Anda melakukannya, setiap file yang menyebabkan browser mengunduhnya karena halaman menjadi dapat diunggah.

### Menjalankan JavaScript di halaman

`javascript_exec` menjalankan ekspresi yang ditulis Claude dalam konteks halaman dan mengembalikan nilai ekspresi terakhir sebagai teks; Claude menulis ekspresi, bukan pernyataan `return`. Kode berjalan dengan hak akses penuh halaman, termasuk cookie, storage, dan permintaan same-origin-nya. Aktifkan anggota ini hanya dalam sesi yang tidak menyimpan kredensial, pertahankan allowlist domain dari [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations) tetap berlaku, perlakukan nilai yang dikembalikan sebagai input yang tidak tepercaya, dan catat kode yang dikeluarkan Claude.

### Membaca aktivitas konsol dan jaringan

`read_console` mengembalikan entri konsol tab dan `read_network` mengembalikan permintaan jaringannya, masing-masing sebagai teks dengan satu baris per entri yang terakumulasi sejak pembacaan sebelumnya dari tab tersebut. Baris konsol membawa entri log, peringatan, atau error; baris jaringan membawa metode, URL, status, tipe MIME, dan waktu. Entri hanya ada sejak saat otomatisasi browser Anda terhubung ke tab, sehingga hasil kosong tidak berarti tab yang sudah terbuka tidak memiliki lalu lintas.

Anggota ini memungkinkan Claude mendiagnosis halaman yang bermasalah (permintaan gagal di balik spinner, error skrip di balik tombol yang tidak berfungsi) tanpa tangkapan layar berulang. Entri konsol dan jaringan dikendalikan halaman dan sering berisi rahasia seperti token dalam URL permintaan, jadi sensor nilai yang menyerupai kredensial yang tidak Anda inginkan dalam konteks Claude dan potong entri yang sangat panjang sebelum mengembalikannya.

## Melacak tab dengan `browser_state`

Claude merujuk tab berdasarkan `tab_id`, aplikasi Anda adalah sumber kebenaran mengenai tab mana yang ada, dan Anda melaporkan status tersebut dalam blok konten `browser_state` yang tidak pernah dilihat Claude secara langsung: API merender teks yang dibaca Claude darinya.

```json
{
  "type": "browser_state",
  "tabs": [
    {
      "tab_id": "tab-1",
      "title": "Documentation",
      "url": "https://example.com/docs",
      "active": true
    },
    { "tab_id": "tab-2", "title": "Pricing", "url": "https://example.com/pricing" }
  ]
}
```

* `tabs` adalah inventaris lengkap tab yang terbuka setelah panggilan, bukan delta. Nilainya boleh kosong; kapan pun tidak kosong, tepat satu entri membawa `"active": true`.
* `state_changes` (tidak ditampilkan di sini) melaporkan efek samping dari panggilan: satu entri `tab_opened` untuk setiap tab yang dibuka oleh panggilan dan masih terbuka saat panggilan selesai, yang `tab_id`-nya juga harus muncul di `tabs`, serta [peristiwa unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads). Hilangkan field ini ketika tidak ada yang perlu dilaporkan; array kosong akan ditolak.
* Kirim blok ini hanya pada hasil yang menjawab panggilan anggota browser, paling banyak sekali per `tool_result`, dan jangan pernah pada hasil dengan `is_error: true`. Anda menyatakan "tidak ada status tab untuk dilaporkan" dengan menghilangkan blok tersebut.
* API merender `tabs` menjadi teks untuk Claude seperti yang dijelaskan dua bagian berikutnya; entri unduhan di `state_changes` divalidasi tetapi tidak dirender.

**Anda yang menetapkan nilai `tab_id`.** String stabil apa pun dapat digunakan, seperti pengenal halaman dari pustaka otomasi Anda atau penghitung Anda sendiri, selama Anda tidak menggunakan ulang `tab_id` sementara tab dengan pengenal tersebut masih tercantum sebagai terbuka pada hasil sebelumnya. API memberlakukan batasan berikut pada blok ini:

* Setiap `tab_id`, `title`, dan `url` boleh paling banyak 4.096 karakter, `tab_id` tidak boleh kosong, dan tidak satu pun boleh berisi karakter kontrol (termasuk baris baru) atau pemisah baris atau paragraf Unicode.
* Satu blok boleh mencantumkan paling banyak 100 tab dan 200 perubahan status.
* Batasan yang sama berlaku untuk `tab_id` yang diteruskan Claude ke `switch_tab` dan `close_tab`, karena API merendernya ke dalam teks hasil, jadi jawablah panggilan yang `tab_id`-nya melanggar batasan tersebut dengan hasil error alih-alih blok `browser_state`.

<Warning>
  Judul dan URL tab berasal dari halaman dan dirender menjadi teks yang dibaca Claude, sehingga keduanya merupakan permukaan "prompt injection" (injeksi prompt). API merender URL apa adanya, jadi sanitasi URL yang berasal dari halaman sebelum mengisi `tabs`. API meng-escape tanda kutip ganda dan garis miring terbalik pada judul saat merendernya, jadi jangan meng-escape judul terlebih dahulu (judul yang sudah di-escape sebelumnya akan sampai ke Claude dalam keadaan ter-escape ganda); memotong atau membuang judul yang mencurigakan tetap bermanfaat. Batasan panjang dan karakter yang diberlakukan API adalah batas bawah, bukan pertahanan.
</Warning>

### Hasil manajemen tab

Untuk `new_tab`, `switch_tab`, `close_tab`, dan `list_tabs`, `content` dari hasil yang berhasil adalah tepat satu blok `browser_state` tanpa teks atau gambar, dan API menulis teks yang dilihat Claude. Blok pada hasil `new_tab` juga harus membawa tepat satu perubahan status `tab_opened` yang `tab_id`-nya cocok dengan entri yang ditandai `active: true`.

| Anggota      | Teks yang dilihat Claude                                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `switch_tab` | `Switched to tab {tab_id}`, diambil dari `input.tab_id` panggilan                                                                |
| `close_tab`  | `Closed tab {tab_id}`, diambil dari `input.tab_id` panggilan                                                                     |
| `new_tab`    | `Created new tab with tab_id: {tab_id}, URL: {url}. It is now the current tab.`, diambil dari entri yang ditandai `active: true` |
| `list_tabs`  | `Available tabs:` diikuti satu baris per tab, atau `No tabs available` ketika `tabs` kosong                                      |

Hasil `list_tabs` yang bloknya mencantumkan dua tab dengan tab pertama aktif dirender sebagai berikut, dengan setiap baris diindentasi dua spasi dan `(current)` ditambahkan hanya pada tab yang aktif:

```text wrap
Available tabs:
  • tab_id tab-1: "Documentation" (https://example.com/docs) (current)
  • tab_id tab-2: "Pricing" (https://example.com/pricing)
```

Hasil error untuk salah satu anggota ini adalah kebalikannya: teks error biasa di `content`, `is_error: true`, dan tanpa blok `browser_state`.

Sebagai contoh, ketika Claude memanggil `new_tab` (`input`-nya kosong), eksekutor Anda membuka tab, menjadikannya aktif, dan mengembalikan inventaris dengan satu entri `tab_opened`:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01WvHSbQVV9j5nWGvTmk4vNL",
      "toolset_name": "browser",
      "content": [
        {
          "type": "browser_state",
          "tabs": [
            { "tab_id": "tab-1", "title": "Documentation", "url": "https://example.com/docs" },
            { "tab_id": "tab-2", "title": "Pricing", "url": "https://example.com/pricing" },
            { "tab_id": "tab-3", "title": "", "url": "about:blank", "active": true }
          ],
          "state_changes": [{ "type": "tab_opened", "tab_id": "tab-3" }]
        }
      ]
    }
  ]
}
```

Claude melihat `Created new tab with tab_id: tab-3, URL: about:blank. It is now the current tab.` Laporkan URL tempat tab dibuka, seperti di sini, bukan URL tujuan pengalihan setelahnya; hasil-hasil berikutnya melaporkan URL tab yang berlaku saat itu.

### Konteks tab pada hasil lainnya

Pada setiap anggota lainnya, blok ini bersifat opsional: kirimkan ketika kumpulan tab yang terbuka, tab aktif, atau judul maupun URL suatu tab berubah, atau ketika ada `state_changes` untuk dilaporkan, dan selalu sertakan inventaris `tabs` lengkap. Ketika suatu hasil membawa teks sekaligus blok `browser_state`, API menambahkan footer `Tab Context` pada teks hasil tersebut, dipisahkan dari teks Anda oleh satu baris kosong, sehingga Claude menerima status baru tanpa panggilan `list_tabs` terpisah:

```text wrap
Tab Context:
- Executed on tab_id: tab-1
- Available tabs:
  • tab_id tab-1: "Documentation" (https://example.com/docs)
  • tab_id tab-2: "Pricing" (https://example.com/pricing)
```

`Executed on` menyebutkan tab tempat panggilan dijalankan, yaitu input `tab_id`-nya jika ada dan jika tidak, tab aktif, dan baris-baris tab pada footer tidak membawa penanda `(current)`. Jangan menambahkan teks ini sendiri; kirim blok terstruktur dan biarkan API merendernya. Footer ini dideduplikasi, sehingga status tab yang identik tidak dirender lagi pada hasil berikutnya dan mengisi blok secara bebas tidak menimbulkan biaya apa pun.

Tiga kasus tidak merender footer meskipun blok ada:

* Hasil `zoom` apa pun.
* Hasil tanpa blok `text` (misalnya hasil `screenshot` yang hanya berisi gambar). Tidak ada yang dirender atau diingat untuk hasil tersebut; konteks tab muncul pada hasil berikutnya yang membawa teks sekaligus blok `browser_state`, jadi sertakan blok teks singkat di samping gambar ketika Anda ingin Claude melihat perubahan tab pada hasil yang sama.
* Hasil yang daftar `tabs`-nya kosong pada panggilan yang tidak membawa `tab_id`, karena tidak ada tab untuk disebutkan.

Sebagai contoh, ketika Claude mengklik tautan "Pricing" (`ref_5`) sebelumnya dalam sesi ini, halaman membukanya di tab baru yang tidak diminta Claude, dan tanpa laporan Claude harus memanggil `list_tabs` untuk menemukannya. Kembalikan konfirmasi klik ditambah blok yang `state_changes`-nya menyebutkan tab yang dibuka, dengan menandai tab mana pun yang dibiarkan aktif oleh eksekutor Anda:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01EgTXj1FjE2FCTt2zNFWLao",
      "toolset_name": "browser",
      "content": [
        { "type": "text", "text": "Clicked element ref_5." },
        {
          "type": "browser_state",
          "tabs": [
            {
              "tab_id": "tab-1",
              "title": "Documentation",
              "url": "https://example.com/docs",
              "active": true
            },
            { "tab_id": "tab-2", "title": "Pricing", "url": "https://example.com/pricing" }
          ],
          "state_changes": [{ "type": "tab_opened", "tab_id": "tab-2" }]
        }
      ]
    }
  ]
}
```

Claude melihat `Clicked element ref_5.` diikuti footer Tab Context yang ditampilkan sebelumnya. Tab yang dibuka selama panggilan yang gagal tidak mendapatkan entri `tab_opened`, karena hasil error tidak membawa `browser_state`; tab tersebut muncul di inventaris `tabs` pada hasil berhasil berikutnya. Dalam batch, lampirkan blok pada hasil dari panggilan yang selama pelaksanaannya perubahan terjadi, dan berikan setiap hasil manajemen tab yang berhasil bloknya sendiri meskipun hasil sebelumnya pada giliran yang sama telah melaporkan status yang sama.

### Melaporkan unduhan

Ketika klik atau navigasi memulai unduhan file, laporkan di `state_changes` pada hasil dari panggilan yang selama pelaksanaannya unduhan terjadi, dikorelasikan antarhasil melalui `download_id` yang Anda tetapkan. Unduhan berjalan secara asinkron dan dapat mencakup beberapa hasil, sehingga ada tiga jenis peristiwa:

| `type`               | Field                                        | Kapan dikirim                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `download_started`   | `download_id`, `url`                         | Pada hasil dari panggilan yang selama pelaksanaannya unduhan dimulai. `url` adalah URL final tempat file disajikan, setelah pengalihan.                                                                                                                                                                                                                                 |
| `download_completed` | `download_id`, `url`, `path?`, `size_bytes?` | Pada hasil dari panggilan berikutnya mana pun yang sedang berjalan saat unduhan selesai. Sertakan `path` hanya ketika alat lain di lingkungan yang sama (misalnya, [alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool) atau `file_upload`) dapat membaca file di sana; jika tidak, `download_id` adalah satu-satunya pengenal unduhan. |
| `download_failed`    | `download_id`, `url`, `error?`               | Ketika unduhan gagal atau dibatalkan, dengan alasannya di `error` jika browser menyediakannya.                                                                                                                                                                                                                                                                          |

API memvalidasi entri-entri ini tetapi tidak merendernya menjadi teks yang dilihat Claude, jadi ketika Claude perlu bertindak atas file tersebut, sebutkan juga nama file atau `path` di blok `text` pada hasil yang sama.

Sebagai contoh, klik pada "Download price list (CSV)" (`ref_8`) di tab Pricing memulai unduhan, sehingga hasil klik tersebut membawa entri `download_started` dengan `download_id` `"dl-1"` dan URL file. Unduhan selesai saat panggilan `screenshot` berikutnya sedang berjalan, sehingga `content` hasil tersebut berisi gambar, blok teks seperti `Screenshot captured. Download complete: /home/user/downloads/price-list.csv (48,213 bytes).`, dan blok `browser_state` ini yang melaporkan penyelesaian di bawah `download_id` yang sama:

```json
{
  "type": "browser_state",
  "tabs": [
    { "tab_id": "tab-1", "title": "Documentation", "url": "https://example.com/docs" },
    {
      "tab_id": "tab-2",
      "title": "Pricing",
      "url": "https://example.com/pricing",
      "active": true
    }
  ],
  "state_changes": [
    {
      "type": "download_completed",
      "download_id": "dl-1",
      "url": "https://example.com/pricing/price-list.csv",
      "path": "/home/user/downloads/price-list.csv",
      "size_bytes": 48213
    }
  ]
}
```

Laporan unduhan mengikuti aturan berikut:

* Paling banyak satu entri per `download_id` dalam satu blok, sehingga unduhan yang dimulai dan selesai selama panggilan yang sama hanya melaporkan `download_completed`.
* Jangan pernah mengirim `state_changes` pada hasil `is_error: true`; laporkan peristiwa unduhan yang terjadi selama panggilan yang gagal pada hasil berhasil berikutnya.
* `state_changes` bukan inventaris unduhan yang sedang berlangsung; laporkan setiap peristiwa sekali.
* Setiap entri hanya membawa field yang dideklarasikan oleh `type`-nya. `size_bytes` adalah bilangan bulat non-negatif, `download_id` tidak boleh kosong, dan `download_id`, `url`, `path`, serta `error` masing-masing paling banyak 4.096 karakter tanpa karakter kontrol atau pemisah baris atau paragraf Unicode. `url` berasal dari server jarak jauh dan sering membawa kredensial query-string bertanda tangan setelah pengalihan, jadi hapus parameter query yang tidak Anda inginkan dalam konteks Claude dan sanitasi sebelum melaporkannya atau menggunakannya dalam path sistem file.

## Menangani error

Laporkan panggilan yang gagal kepada Claude sebagai hasil error biasa: `is_error: true`, konten teks yang menjelaskan apa yang salah, `toolset_name` digemakan kembali, dan tanpa blok `browser_state`.

### Mengembalikan error dari eksekutor Anda

Buat teks error spesifik, karena Claude membacanya dan beradaptasi: `Error: Navigation to https://example.com/status timed out after 30 seconds. The page may be unavailable.` memberi Claude sesuatu untuk ditindaklanjuti, sedangkan `Error: navigation failed` saja tidak. Kasus umum lainnya:

<AccordionGroup>
  <Accordion title="Skema navigasi yang ditolak">
    ```json
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01LeUTyqkhRxBFq1QTG3pkwN",
      "toolset_name": "browser",
      "is_error": true,
      "content": "Error: Navigation refused. Only http and https URLs are allowed."
    }
    ```
  </Accordion>

  <Accordion title="Referensi elemen yang kedaluwarsa atau tidak dikenal">
    ```json
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
      "toolset_name": "browser",
      "is_error": true,
      "content": "Error: ref_3 is stale or not found on the current page. Re-read the page to get fresh references."
    }
    ```
  </Accordion>

  <Accordion title="Anggota yang dinonaktifkan atau belum diimplementasikan">
    ```json
    {
      "type": "tool_result",
      "tool_use_id": "toolu_013h2Q55HcNwVyapSpy2s5ZG",
      "toolset_name": "browser",
      "is_error": true,
      "content": "Error: javascript_exec is not enabled in this environment."
    }
    ```
  </Accordion>

  <Accordion title="Dilewati setelah kegagalan sebelumnya dalam giliran">
    Ketika `left_click` pada `ref_3` dari [Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) gagal dengan error referensi kedaluwarsa yang ditampilkan sebelumnya, panggilan `type` dan `key` setelahnya masing-masing mendapatkan hasil ini:

    ```json
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01FkP8rTz6uYh2mNq4LsXw7v",
      "toolset_name": "browser",
      "is_error": true,
      "content": "Not executed: an earlier action in this turn failed."
    }
    ```
  </Accordion>
</AccordionGroup>

### Error permintaan

API memvalidasi entri toolset dan setiap blok `tool_use` dan `tool_result` anggota dalam percakapan. Ketika salah satunya salah bentuk, API mengembalikan `invalid_request_error` sebelum Claude berjalan. Pada tabel berikut, kolom kiri menyebutkan apa yang Anda kirim.

| Permintaan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Mengapa gagal dan apa yang harus dilakukan                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Opsi atau kombinasi yang tidak diterima entri toolset, misalnya, `name`, `strict: true`, `input_examples`, `defer_loading` pada entri itu sendiri, kunci `configs` yang bukan nama anggota, field selain `enabled` atau `defer_loading` dalam nilai `configs` suatu anggota ([Mengonfigurasi toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset)), anggota yang diaktifkan dengan nilai `defer_loading` yang berbeda ([Mengonfigurasi toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset)), `configs` yang tidak menyisakan anggota yang diaktifkan, pemanggil eksekusi kode di `allowed_callers`, header beta lama `fine-grained-tool-streaming-2025-05-14` pada permintaan, `tool_choice` bertipe `tool` yang menyebut `browser` atau suatu anggota, atau entri toolset browser kedua atau alat lain bernama `browser` | Hal-hal ini tidak didukung pada toolset klien. Lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) untuk setiap aturan dan alternatifnya.                                                                                      |
| `tool_result` yang menjawab panggilan anggota tanpa `"toolset_name": "browser"` atau dengan nilai berbeda, atau `toolset_name` pada hasil yang panggilannya bukan panggilan anggota                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Gemakan `toolset_name` secara persis pada hasil anggota, dan hanya pada hasil tersebut.                                                                                                                                                                                                        |
| `tool_use` anggota dari giliran sebelumnya tanpa `tool_result` yang cocok                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Jawab setiap panggilan anggota, termasuk yang tidak Anda jalankan setelah kegagalan.                                                                                                                                                                                                           |
| Blok konten selain `text`, `image`, atau `browser_state` dalam hasil anggota                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Hasil anggota hanya menerima ketiga jenis blok tersebut.                                                                                                                                                                                                                                       |
| Blok `browser_state` yang melanggar aturan di [Melacak tab dengan `browser_state`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state), misalnya, blok pada hasil `is_error: true` atau pada hasil yang tidak menjawab panggilan anggota browser, lebih dari satu dalam satu hasil, `tabs` tidak kosong tanpa tepat satu entri `active: true`, `tab_id` duplikat, array `state_changes` kosong, `tab_opened` yang `tab_id`-nya tidak ada di `tabs`, dua perubahan status untuk satu `download_id` atau field perubahan status yang tidak dideklarasikan oleh `type`-nya ([Melaporkan unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads)), atau field yang melebihi batasnya                                                                                                                                                       | Perbaiki blok tersebut. "Tidak ada yang dilaporkan" dinyatakan dengan menghilangkan blok atau field `state_changes`, bukan dengan nilai kosong.                                                                                                                                                |
| Hasil `new_tab`, `switch_tab`, `close_tab`, atau `list_tabs` yang berhasil tetapi `content`-nya bukan tepat satu blok `browser_state`, atau hasil `new_tab` tanpa tepat satu `tab_opened` yang cocok dengan tab aktif                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | API merender hasil-hasil ini dari blok dan membutuhkannya dalam bentuk yang persis seperti itu; lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results).                                                            |
| `image` dalam hasil yang melebihi [batas ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) model Anda, atau melebihi batas per gambar yang lebih ketat yang berlaku begitu permintaan berisi [lebih dari 20 gambar](https://platform.claude.com/docs/id/build-with-claude/vision#request-limits), termasuk tangkapan layar dan gambar `zoom` pada hasil sebelumnya                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | API tidak memperkecil gambar toolset. Ubah ukuran tangkapan layar sebelum mengembalikannya ([Menyesuaikan ukuran tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)). |
| `model` yang tidak mendukung `browser_toolset_20260801`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Lihat [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#compatibility) untuk model yang didukung.                                                                                                                                                |

## Keterbatasan

* **Ketersediaan platform:** Penggunaan browser hanya tersedia di Claude API.
* **Hanya streaming input utuh:** Ketika Anda melakukan streaming, `input` setiap anggota tiba sebagai satu `input_json_delta` lengkap ([Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets)).
* **Referensi elemen bersifat upaya terbaik:** Halaman yang sangat dinamis (daftar tervirtualisasi, antarmuka yang dirender dengan canvas, halaman yang merender ulang saat digulir) mungkin tidak mengekspos referensi yang stabil, dan Claude beralih ke tangkapan layar dan klik koordinat di sana.
* **`read_console` dan `read_network` bergantung pada otomasi browser Anda:** Keduanya hanya melaporkan apa yang dapat ditangkapnya, dan hanya sejak saat otomasi tersebut terhubung ke suatu tab.
* **Keterbatasan agen umum berlaku:** Latensi, akurasi visi, dan risiko injeksi prompt terbawa dari penggunaan komputer (lihat [Keterbatasan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#understand-computer-use-limitations) alat penggunaan komputer), dan panduannya di bawah [Mengoptimalkan kinerja model dengan prompting](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#optimize-model-performance-with-prompting), [Mengelola riwayat tangkapan layar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#manage-screenshot-history), dan [Mengikuti praktik terbaik implementasi](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#follow-implementation-best-practices) (penundaan aksi, validasi aksi, dan pencatatan log) juga berlaku untuk eksekutor browser.

## Harga dan retensi data

Browser use (penggunaan browser) mengikuti [harga penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat browser use:

**Overhead definisi toolset:** Mendeklarasikan `browser_toolset_20260801` dengan anggota defaultnya menambahkan sekitar 6.600 token input ke sebuah permintaan (sekitar 6.610 pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, dan Claude Opus 4.8, serta sekitar 6.670 pada Claude Sonnet 5), yang mencakup definisi alat anggota dan prompt sistem penggunaan alat. Mengaktifkan keempat anggota opsional menambahkan sekitar 880 token, dan menonaktifkan anggota dengan `configs` mengurangi jumlahnya. Jumlah pasti untuk sebuah permintaan dilaporkan dalam `usage` respons, dan Anda dapat memperkirakannya terlebih dahulu dengan [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

**Konsumsi token tambahan:**

* Gambar screenshot dan zoom yang dikembalikan dalam hasil alat, ditagih sebagai input gambar (lihat [Harga Vision](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size))
* Hasil alat berupa teks yang dikembalikan ke Claude, seperti accessibility tree, teks halaman, dan entri konsol atau jaringan

<Note>
  Jika Anda juga menggunakan alat computer use, alat bash, alat editor teks, atau alat Anda sendiri bersama browser use, alat-alat tersebut memiliki biaya token masing-masing seperti yang didokumentasikan di halaman masing-masing.
</Note>

Sesi browser, unduhan, dan file yang diunggah tetap berada di lingkungan Anda; tangkapan layar, teks halaman, dan status tab yang Anda kembalikan merupakan bagian dari konten permintaan API Anda dan mengikuti kebijakan retensi standar, atau pengaturan ZDR Anda jika Anda memilikinya. Alat penggunaan browser memenuhi syarat ZDR; lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) untuk periode retensi dan kelayakan di seluruh fitur.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Alat penggunaan komputer" icon="computer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Berikan Claude kendali atas desktop penuh ketika tugas keluar dari browser; panduan implementasinya juga berlaku untuk eksekutor browser.
  </Card>

  <Card title="Menangani panggilan alat" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Format blok `tool_result`, kembalikan gambar dan error, dan lanjutkan percakapan.
  </Card>

  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi toolset klien dan setiap alat lain yang disediakan Anthropic, beserta versi dan parameternya.
  </Card>
</CardGroup>
