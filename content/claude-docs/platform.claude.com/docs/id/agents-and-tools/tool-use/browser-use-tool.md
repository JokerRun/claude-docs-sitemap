---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 135530dc70c2ab01ec9336917e6fbe17b2bbbf1916e1cd8e7a33ac329670dba0
---

---
title: Alat penggunaan browser
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool
description: Biarkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di lingkungan browser Anda sendiri dengan alat penggunaan browser.
featureMetadata:
  status: stable
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Alat sisi klien. Anthropic tidak menjalankan tindakan browser atau menyimpan konten halaman di luar penanganan API standar.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-opus-4-8
  supportedPlatforms:
    Claude API: stable
    Claude Models on Google Cloud (Google managed): stable
---

<Note>
  **Mulai dengan toolset SDK:** SDK Python dan TypeScript memiliki kelas toolset browser, dalam versi beta. Mulailah dari [integrasi mitra](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#partner-integrations), atau lihat [Penggunaan browser dan komputer dengan toolset SDK](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk). Gunakan halaman ini sebagai referensi alat, atau saat Anda menangani panggilan alat sendiri.
</Note>

Alat penggunaan browser memungkinkan Claude menavigasi, membaca, dan berinteraksi dengan halaman web di browser yang dijalankan oleh aplikasi Anda. Claude bekerja dengan halaman baik melalui strukturnya (accessibility tree, elemen, formulir, dan tab) maupun melalui screenshot dan koordinat viewport.

Alat ini adalah [client toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) yang didefinisikan oleh Anthropic: satu entri `browser_toolset_20260801` di `tools` memberi Claude 27 alat anggota secara default, seperti `navigate`, `read_page`, `left_click`, dan `screenshot`, ditambah empat lagi ketika Anda [mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools). Aplikasi Anda menjalankan setiap panggilan terhadap otomatisasi browsernya sendiri; tidak ada yang berjalan di sisi Anthropic. Alat ini saat ini tidak tersedia di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/tools).

Pilih penggunaan browser ketika tugas tetap berada di dalam halaman web dan berarti melakukan tindakan pada halaman tersebut, atau ketika halaman membangun kontennya dengan JavaScript. Ketika tugas membutuhkan seluruh desktop, gunakan [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), yang bekerja hanya melalui screenshot dan koordinat. Untuk membaca halaman yang dapat Anda tunjukkan kepada Claude, atau menemukan sumber di web, [alat web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) dan [alat web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool) lebih ringan. Keduanya adalah [server tools](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) yang dijalankan API untuk Anda, tanpa browser yang perlu dioperasikan.

Dengan penggunaan browser, Claude membaca dan bertindak pada halaman web langsung, sehingga semua yang disediakan halaman adalah input yang tidak tepercaya dan tindakan yang diambil Claude dapat memiliki efek nyata. Lihat [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations) sebelum Anda melakukan deploy.

## Mulai cepat

Alat penggunaan browser tersedia di Claude API dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed): tambahkan satu entri bertipe `browser_toolset_20260801`, tanpa `name`, ke array `tools` dari permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
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
  model: claude-opus-5-5
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
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
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
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 2048,
      Tools = [new BrowserToolset20260801()],
      Messages =
      [
          new UserMessageParam { Content = "Open example.com/docs and tell me how to get started." },
      ],
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
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
      model: Model::CLAUDE_OPUS_5_5,
      tools: [
          ['type' => 'browser_toolset_20260801'],
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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
  "model": "claude-opus-5-5",
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

Executor Anda (bagian dari aplikasi Anda yang mengendalikan browser dan menghasilkan hasil alat) menjalankan `navigate`, lalu `read_page`. Aplikasi Anda mengembalikan satu `tool_result` untuk setiap blok dalam permintaan berikutnya, dengan menggemakan `toolset_name` pada masing-masing. Hasil `navigate` melaporkan tab yang dimuatnya dalam blok `browser_state`; hasil `read_page` adalah teks di mana setiap elemen membawa referensi:

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

Claude sekarang memegang referensi yang dapat ditindaklanjuti, sehingga giliran berikutnya dapat mengklik `ref_2` untuk membuka halaman getting-started, tanpa perlu menemukan tautan di screenshot terlebih dahulu.

## Cara kerja penggunaan browser

Penggunaan browser berjalan sebagai agent loop di aplikasi Anda: Claude mengembalikan panggilan alat anggota, executor Anda menjalankannya terhadap browser, dan Anda mengembalikan hasilnya hingga Claude menjawab dalam teks.

<Steps>
  <Step title="Berikan Claude alat penggunaan browser dan prompt pengguna">
    * Tambahkan entri `browser_toolset_20260801`, dan opsional alat lainnya, ke permintaan API Anda.
    * Sertakan prompt pengguna yang memerlukan bekerja dengan halaman web, misalnya, “Open example.com/docs and tell me how to get started.”
  </Step>

  <Step title="Claude merespons dengan panggilan alat anggota">
    * Claude mengembalikan satu atau lebih blok `tool_use` dalam satu giliran assistant; beberapa blok dalam satu giliran membentuk batch action, misalnya, `left_click`, lalu `type`, lalu `key`.
    * `name` setiap blok adalah nama anggota, masing-masing membawa `"toolset_name": "browser"`, dan `input` hanya berisi parameter anggota tersebut, tanpa field `action`. `stop_reason` respons adalah `tool_use`.
  </Step>

  <Step title="Jalankan panggilan secara berurutan dan kembalikan hasilnya">
    * Iterasi setiap blok `tool_use` di `response.content` (jangan berasumsi hanya ada satu) dan jalankan secara berurutan, sesuai urutan kemunculannya, karena panggilan berikutnya biasanya bergantung pada panggilan sebelumnya.
    * Kembalikan satu `tool_result` untuk setiap blok dalam pesan `user` baru, dicocokkan dengan `tool_use_id`, dan gemakan `"toolset_name": "browser"` pada masing-masing. Jawab setiap panggilan, atau permintaan berikutnya akan ditolak.
    * Jika panggilan gagal, kembalikan `is_error: true` dengan deskripsi teks untuk blok tersebut, lalu terapkan aturan penghentian di [Batch actions](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) ke setiap blok berikutnya dalam giliran tersebut.
  </Step>

  <Step title="Claude melanjutkan hingga tugas selesai">
    * Claude membaca hasilnya (teks halaman, accessibility tree, screenshot, status tab) dan, jika membutuhkan lebih, mengembalikan panggilan anggota lebih lanjut, yang membawa Anda kembali ke langkah 3.
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
              "source": {
                  "type": "base64",
                  "media_type": "image/png",
                  "data": PLACEHOLDER_PNG,
              },
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
  const PLACEHOLDER_PNG =
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";

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
          data: PLACEHOLDER_PNG
        }
      }
    ];
  }

  function handleBrowserAction(
    action: string,
    input: unknown
  ): string | Anthropic.ImageBlockParam[] {
    const params: object = typeof input === "object" && input !== null ? input : {};
    if (action === "navigate" && "url" in params) {
      return navigate(String(params.url));
    } else if (action === "read_page") {
      return readPage();
    } else if (action === "left_click" && "target" in params) {
      // target adalah referensi elemen dari read_page atau koordinat viewport
      const target: object =
        typeof params.target === "object" && params.target !== null ? params.target : {};
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
          default => throw new \RuntimeException("Unknown or unimplemented member: {$name}"),
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

Bagian kedua menjalankan batch secara berurutan, mengirimkan setiap blok ke handler tersebut, menggemakan `toolset_name` pada setiap hasil, dan menerapkan aturan penghentian dari [Batch actions](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions), mengubah error handler menjadi hasil error. Sampling loop yang memanggilnya adalah yang ditunjukkan di [Memahami agent loop](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#understanding-the-agentic-loop), dengan toolset browser di `tools`.

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
    isError?: boolean
  ): Anthropic.ToolResultBlockParam {
    return {
      type: "tool_result",
      tool_use_id: toolUseId,
      toolset_name: "browser",
      content,
      is_error: isError
    };
  }

  function processToolCalls(response: Anthropic.Message): Anthropic.ToolResultBlockParam[] {
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
        // Batch berhenti pada kegagalan pertama; jawab aksi berikutnya tanpa menjalankannya
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
  // membangun satu tool_result untuk setiap blok tool_use. Setelah kegagalan pertama, sisanya
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
   * tool_result for each tool_use block. After the first failure, skip the rest:
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
              result = browserResult(toolUse)
                  .content(HALT_TEXT)
                  .isError(true)
                  .build();
          } else {
              try {
                  Map<String, JsonValue> input =
                      (Map<String, JsonValue>) toolUse._input().asObject().get();
                  ToolResultBlockParam.Content output = handleBrowserAction(toolUse.name(), input);
                  // Executor sungguhan juga menambahkan blok browser_state ke hasil navigasi dan
                  // manajemen tab; lihat "Lacak tab dengan browser_state" di halaman ini.
                  result = browserResult(toolUse)
                      .content(output)
                      .build();
              } catch (RuntimeException e) {
                  failed = true;
                  result = browserResult(toolUse)
                      .content("Error: " + e.getMessage())
                      .isError(true)
                      .build();
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
          if (!($block instanceof \Anthropic\Messages\ToolUseBlock) || $block->toolsetName !== 'browser') {
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
          } catch (\Throwable $e) {
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
  # tool_result untuk setiap blok tool_use. Setelah kegagalan pertama, lewati sisanya:
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

Kirimkan setiap blok berdasarkan pasangan (`toolset_name`, `name`) alih-alih hanya berdasarkan `name`, karena alat kustom dalam permintaan yang sama mungkin memiliki nama yang sama dengan anggota; [Client toolsets](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) menjelaskan bagian-bagian kontrak ini yang dimiliki bersama oleh kedua toolset. Jika Claude menyebutkan anggota yang tidak diimplementasikan executor Anda, atau yang telah Anda nonaktifkan, jawab blok tersebut dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor) alih-alih membuangnya.

Saat Anda melakukan streaming respons, `input` setiap anggota tiba sebagai satu `input_json_delta` lengkap alih-alih sebagai fragmen, jadi tunggu hingga giliran selesai sebelum menjalankan batch.

### Batch actions

Giliran dengan beberapa panggilan anggota adalah batch action: jalankan panggilan sesuai urutan kemunculannya, berhenti pada kegagalan pertama, dan jawab setiap panggilan berikutnya dengan `is_error: true` dan teks persis `Not executed: an earlier action in this turn failed.` Batch menggunakan bentuk respons yang sama dengan [penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use); perbedaannya adalah Anda menjalankan blok secara berurutan alih-alih secara bersamaan. Di sini Claude mengklik kotak pencarian yang ditemukannya sebelumnya, mengetik kueri, dan menekan Enter dalam satu giliran:

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

Aplikasi Anda mengembalikan tiga blok `tool_result` dalam satu pesan `user`, masing-masing membawa `toolset_name` dan pengakuan teks singkat seperti `Clicked element ref_3.` Menekan Enter memuat halaman hasil, sehingga hasil `key` juga membawa blok `browser_state` dengan URL tab yang diperbarui ([Konteks tab pada hasil lain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-context-on-other-results)). Jika klik tersebut gagal, hasilnya akan membawa teks error Anda dan dua hasil lainnya akan membawa teks penghentian, seperti yang ditunjukkan di bawah [Mengembalikan error dari executor Anda](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor).

Anda tidak perlu mengembalikan screenshot setelah setiap panggilan. Claude biasanya mengakhiri batch dengan panggilan observasi (`screenshot`, `read_page`, atau `get_page_text`), dan aplikasi Anda juga dapat melampirkan observasinya sendiri, seperti screenshot atau accessibility tree baru, sebagai blok konten tambahan pada hasil terakhir dalam batch untuk menghemat satu round trip. Karena hasil manajemen tab harus berupa tepat satu blok `browser_state`, lampirkan pada hasil terakhir yang bukan panggilan manajemen tab.

Jika executor Anda hanya dapat menjalankan satu panggilan untuk setiap round trip, atur `disable_parallel_tool_use` ke `true` di `tool_choice` dan Claude mengembalikan paling banyak satu panggilan anggota untuk setiap giliran, dengan konsekuensi lebih banyak round trip ([Menonaktifkan penggunaan alat paralel](https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use#disable-parallel-tool-use)). Sisa kontrak di bawah [Batch actions untuk alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions) tetap berlaku, termasuk satu `tool_result` untuk setiap `tool_use` dalam pesan `user` berikutnya, kecuali dua hal: teks penghentian dan apa yang berisi `content` dari hasil yang berhasil. Konten hasil mengikuti [Alat anggota](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#member-tools) di halaman ini: hasil `new_tab`, `switch_tab`, `close_tab`, atau `list_tabs` adalah tepat satu blok `browser_state` tanpa teks atau gambar ([Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results)), dan hasil anggota lain mana pun dapat menambahkan blok `browser_state` ke teks atau gambarnya ([Konteks tab pada hasil lain](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-context-on-other-results)). Di mana cache breakpoint di dalam batch berlaku dijelaskan di baris `cache_control` dari [Parameter alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#tool-parameters) alat penggunaan komputer.

### Target dan koordinat

Alat anggota yang bertindak pada suatu lokasi mengambil objek `target`, yang berupa koordinat piksel viewport atau referensi ke elemen yang dikembalikan oleh `read_page` atau `find`. Tabel [Alat anggota](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#member-tools) menuliskan `Target` untuk parameter yang menerima salah satu bentuk.

| Bentuk             | `target.type`  | Field                                      | Diterima oleh                                                                                                                                                                             |
| ------------------ | -------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CoordinateTarget` | `"coordinate"` | `x`, `y` (integer, piksel viewport)        | `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `hover`, `left_click_drag` (`from` dan `target`), `left_mouse_down`, `left_mouse_up`, `mouse_move`, `scroll` |
| `RefTarget`        | `"ref"`        | `ref` (referensi elemen seperti `"ref_2"`) | `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click`, `hover`, `scroll_to`, `form_input`, `file_upload`                                                            |

**Koordinat adalah piksel viewport**, ruang piksel dari `screenshot` viewport penuh dengan titik asal di kiri atas halaman yang dirender; tidak ada desktop atau bingkai jendela di sekelilingnya. Toolset tidak mendeklarasikan dimensi tampilan dan Claude menyimpulkan ukuran viewport dari screenshot yang Anda kembalikan, jadi pertahankan satu ukuran yang konsisten. `zoom` tidak mengubah bingkai, sehingga `region`-nya dan koordinat apa pun yang dikeluarkan Claude setelah menerima gambar yang di-zoom tetap berupa piksel viewport penuh.

**Screenshot harus sesuai dengan batas gambar.** API tidak memperkecil skala gambar toolset: screenshot atau gambar zoom yang melebihi [batas ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) model Anda, atau melebihi batas per gambar yang lebih ketat yang berlaku setelah permintaan berisi [lebih dari 20 gambar](https://platform.claude.com/docs/id/build-with-claude/vision#request-limits), akan ditolak. Ubah ukuran sebelum mengembalikan, dan skalakan kembali koordinat Claude dengan kebalikan dari faktor Anda sebelum mengirimkannya ([Menyesuaikan ukuran screenshot agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)).

**Referensi elemen berasal dari `read_page` dan `find`.** Setiap elemen dalam output keduanya membawa tag seperti `[ref_2]`, seperti pada hasil Mulai cepat:

```text wrap
link "Documentation" [ref_1]
link "Getting started" [ref_2]
textbox "Search docs" [ref_3]
button "Search" [ref_4]
link "Pricing" [ref_5]
```

Claude mengembalikan referensi sebagai target `{"type": "ref", "ref": "ref_2"}` pada panggilan klik, `hover`, `scroll_to`, `form_input`, atau `file_upload` berikutnya, atau sebagai parameter `ref` pada `read_page` untuk membaca subtree. Executor Anda menetapkan referensi, menyimpan pemetaan dari masing-masing ke node yang mendasarinya (ID accessibility-node, selector yang disimpan, atau yang setara), dan bertindak pada node tersebut ketika referensi dikembalikan.

Referensi dibatasi pada tab yang menghasilkannya dan tetap valid hingga tab tersebut bernavigasi atau DOM-nya berubah secara material. API tidak dapat mendeteksi referensi yang kedaluwarsa atau tidak dikenal, jadi ketika Claude mengirimkan referensi yang tidak lagi dikenali executor Anda, kembalikan hasil error seperti `Error: ref_3 is stale or not found on the current page. Re-read the page to get fresh references.` Claude kemudian membaca halaman lagi. Jangan menomori ulang referensi yang telah Anda berikan untuk suatu tab hingga tab tersebut bernavigasi, karena hal itu secara diam-diam membatalkan referensi yang masih dipegang Claude.

Claude menggunakan kedua gaya penargetan dan beralih di antara keduanya berdasarkan apa yang diekspos halaman; prompt Anda dan apa yang dikembalikan executor Anda mengarahkan pilihannya:

* **Utamakan referensi di mana halaman memiliki accessibility tree yang dapat digunakan.** Referensi bertahan dari pergeseran tata letak dan reflow yang membuat koordinat piksel rapuh, dan memungkinkan Claude bertindak pada kontrol yang sulit diklik dengan pointer.
* **Gunakan koordinat sebagai cadangan untuk konten yang tidak dijelaskan oleh tree.** Antarmuka yang dirender dengan canvas, video tertanam atau permukaan remote-desktop, daftar yang sangat tervirtualisasi, dan elemen di dalam iframe lintas-origin sering kali tidak memiliki node yang berguna, sehingga Claude bekerja dari `screenshot` dan `zoom` dan mengklik berdasarkan koordinat; executor Anda menentukan frame mana yang terkena koordinat tersebut.
* **Batasi cakupan pembacaan, dan baca tree sebelum mengambil screenshot.** Pada halaman besar, `read_page` dengan `filter: "interactive"` atau `ref` dari sebuah container mengembalikan subtree yang terfokus, dan pembacaan tree dari halaman biasa sering kali memakan lebih sedikit token input dibandingkan screenshot sekaligus memberi Claude referensi yang dapat langsung ditindaklanjuti. Screenshot tetap menjadi observasi yang tepat ketika tata letak visual, gambar, atau status rendering penting.

## Pertimbangan keamanan

Penggunaan browser membawa risiko yang tidak dimiliki fitur API standar, karena Claude membaca dan bertindak pada konten dari web terbuka, di mana halaman mana pun dapat berisi teks yang ditulis untuk memanipulasinya.

<Warning>
  Untuk mengurangi risiko ini, ambil tindakan pencegahan seperti berikut:

  1. Jalankan browser dan executor Anda di container atau mesin virtual khusus dengan hak akses minimal, profil baru yang tidak menyimpan kredensial, dan tanpa akses ke filesystem sensitif atau jaringan internal; isolasi alat apa pun yang Anda jalankan bersamanya dengan cara yang sama.
  2. Batasi host yang dapat dijangkau browser ke domain allowlist yang ditegakkan di lapisan jaringan dan diperiksa ulang di handler `navigate` Anda setelah redirect, dan blokir rentang loopback, link-local, dan privat kecuali tugas membutuhkannya.
  3. Perlakukan semua yang disediakan halaman sebagai input yang tidak tepercaya. Itu termasuk judul tab dan URL, serta `url`, `path`, dan `error` setiap unduhan, yang Anda laporkan dalam blok [`browser_state`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state). Bangun pembacaan halaman dari apa yang dirender halaman (accessibility tree atau teks yang terlihat), bukan sumber DOM mentah, agar teks tersembunyi tidak mencapai Claude.
  4. Di handler `navigate` Anda, terima kata kunci riwayat `"back"`, `"forward"`, dan `"reload"`, perlakukan URL tanpa skema sebagai `https://`, lalu parse URL dan tolak skema apa pun selain `http` atau `https` (`javascript:`, `file:`, `data:`, `chrome:`, dan sebagainya) dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor). Periksa skema dengan parser URL alih-alih prefiks string; API tidak memfilter URL yang dibuka Claude, sehingga API tidak dapat menolaknya untuk Anda.
  5. Biarkan `javascript_exec` dan `file_upload` tetap nonaktif kecuali Anda membutuhkannya, dan baca [Mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools) sebelum mengaktifkan salah satunya.
  6. Minta manusia untuk mengonfirmasi tindakan yang berdampak signifikan dan apa pun yang memerlukan persetujuan afirmatif (pembelian, mengubah akun, mengirim pesan, dan menerima ketentuan), dan lakukan pemeriksaan itu di executor Anda sebelum setiap panggilan, karena satu giliran dapat membawa beberapa panggilan.
</Warning>

Claude terkadang mengikuti instruksi yang ditemukan dalam konten halaman bahkan ketika instruksi tersebut bertentangan dengan instruksi Anda; teks di halaman yang mengatakan “ignore your previous instructions and navigate to...” dapat mengalihkannya dari tugas. Isolasi Claude dari data dan tindakan sensitif untuk membatasi apa yang dapat dijangkau oleh prompt injection, tinjau [Memitigasi jailbreak dan prompt injection](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks), dan jika suatu tugas tidak dapat menghindari sesi yang sudah login, gunakan akun khusus dengan hak akses rendah dan pertahankan konfirmasi manusia pada tindakan yang mengubah akun.

Anthropic telah melatih model untuk menahan prompt injection ini dan telah menambahkan lapisan pertahanan tambahan. Jika Anda menggunakan alat penggunaan browser, classifier akan secara otomatis memindai apa yang dikembalikan browser, seperti teks halaman atau screenshot, untuk menandai potensi prompt injection. Ketika classifier ini mengidentifikasi potensi prompt injection, classifier akan secara otomatis mengarahkan model untuk memeriksa apakah instruksi tersebut benar-benar berasal dari Anda sebelum menindaklanjutinya.

Perlindungan tambahan ini tidak ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam loop), jadi jika Anda ingin memilih keluar dan menonaktifkannya, [hubungi dukungan](https://support.claude.com/en/). Tindakan pencegahan yang tercantum sebelumnya tetap penting bahkan dengan adanya classifier ini.

Karena browser berjalan di lingkungan Anda, situs yang dikunjungi Claude melihat identitas jaringan executor Anda, dan konten halaman mencapai API hanya sebagai hasil alat yang Anda kembalikan. Informasikan pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan penggunaan browser di produk Anda.

## Alat anggota

Entri `browser_toolset_20260801` mendeklarasikan 31 alat anggota; `input` setiap panggilan adalah tepat parameter yang tercantum di sini, dan `tab_id`, jika opsional, secara default adalah tab aktif. `Target`, `CoordinateTarget`, dan `RefTarget` adalah bentuk yang dijelaskan di [Target dan koordinat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#targets-and-coordinates). Empat anggota (`javascript_exec`, `file_upload`, `read_console`, dan `read_network`) dinonaktifkan secara default dan hanya muncul ketika Anda mengaktifkannya (lihat [Mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools)). Batas input dan konvensi output yang dicatat di baris setiap anggota dinyatakan kepada Claude, tidak ditegakkan oleh API, jadi validasi input (termasuk koordinat terhadap viewport Anda) dan terapkan konvensi tersebut di executor Anda.

Hanya `screenshot` dan `zoom` yang memerlukan [blok `image`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-results-from-client-tools) dalam hasilnya, dan empat anggota manajemen tab (`new_tab`, `list_tabs`, `switch_tab`, dan `close_tab`) mengembalikan tepat satu blok `browser_state` (lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results)). Setiap anggota lain mengembalikan blok `text`: baik pengakuan singkat seperti `Clicked element ref_2.` atau output anggota tersebut. Hasil apa pun selain hasil manajemen tab juga dapat membawa blok `image`, biasanya screenshot yang diambil setelah tindakan, sehingga Claude menerima hasilnya tanpa panggilan `screenshot` terpisah; [Batch actions](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) menunjukkan di mana melampirkannya dalam batch. `tool_result` anggota hanya boleh berisi blok konten `text`, `image`, dan `browser_state`.

### Navigasi dan pengambilan gambar

| Anggota      | Input               | Deskripsi                                                                                                                                                                                                                                                                                          |
| ------------ | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `navigate`   | `url`, `tab_id?`    | Memuat URL `http` atau `https`, atau bergerak melalui riwayat dengan `"back"`, `"forward"`, atau `"reload"`. Perlakukan URL tanpa skema sebagai `https://` dan tolak skema lain dengan hasil error. Kembalikan pengakuan singkat, ditambah blok `browser_state` ketika URL atau judul tab berubah. |
| `screenshot` | `tab_id?`           | Mengambil gambar viewport dan mengembalikan blok `image`.                                                                                                                                                                                                                                          |
| `zoom`       | `region`, `tab_id?` | Mengembalikan `image` yang dipotong dan diperbesar dari `region`, diberikan sebagai `[x0, y0, x1, y1]` dalam piksel viewport, untuk inspeksi lebih dekat terhadap teks atau kontrol kecil.                                                                                                         |

### Pointer

| Anggota           | Input                                                                       | Deskripsi                                                                                                                                                                    |
| ----------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `left_click`      | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri pada koordinat atau elemen yang direferensikan. `modifiers` adalah chord yang ditahan selama klik, misalnya, `"shift"` atau `"ctrl+shift"`.                        |
| `right_click`     | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kanan pada koordinat atau elemen.                                                                                                                                       |
| `middle_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik tengah pada koordinat atau elemen.                                                                                                                                      |
| `double_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri ganda pada koordinat atau elemen.                                                                                                                                  |
| `triple_click`    | `target: Target`, `modifiers?`, `tab_id?`                                   | Klik kiri tiga kali pada koordinat atau elemen, yang biasanya memilih satu baris atau paragraf.                                                                              |
| `hover`           | `target: Target`, `tab_id?`                                                 | Menggerakkan pointer di atas koordinat atau elemen tanpa mengklik.                                                                                                           |
| `left_click_drag` | `from: CoordinateTarget`, `target: CoordinateTarget`, `tab_id?`             | Menekan di `from`, menyeret ke `target`, dan melepaskan.                                                                                                                     |
| `left_mouse_down` | `target: CoordinateTarget`, `tab_id?`                                       | Menekan dan menahan tombol kiri pada koordinat; pasangkan dengan `left_mouse_up` untuk seret kustom.                                                                         |
| `left_mouse_up`   | `target: CoordinateTarget`, `tab_id?`                                       | Melepaskan tombol kiri pada koordinat.                                                                                                                                       |
| `mouse_move`      | `target: CoordinateTarget`, `tab_id?`                                       | Menggerakkan pointer ke koordinat.                                                                                                                                           |
| `scroll`          | `target: CoordinateTarget`, `scroll_direction`, `scroll_amount?`, `tab_id?` | Menggulir pada posisi viewport. `scroll_direction` adalah `"up"`, `"down"`, `"left"`, atau `"right"`; `scroll_amount` dalam satuan takik roda gulir, 1 hingga 10, default 3. |
| `scroll_to`       | `target: RefTarget`, `tab_id?`                                              | Menggulir elemen yang direferensikan ke dalam tampilan.                                                                                                                      |

### Keyboard dan waktu

| Anggota    | Input                         | Deskripsi                                                                                                                                                                                                               |
| ---------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`     | `text`, `tab_id?`             | Mengetik string literal pada fokus saat ini.                                                                                                                                                                            |
| `key`      | `text`, `repeat?`, `tab_id?`  | Menekan tombol atau chord. `text` adalah satu tombol (`"Enter"`), chord yang digabungkan dengan `+` (`"ctrl+a"`), atau urutan yang dipisahkan spasi (`"Backspace Backspace"`); `repeat` adalah 1 hingga 100, default 1. |
| `hold_key` | `text`, `duration`, `tab_id?` | Menahan tombol atau chord selama `duration` detik, 0 hingga 30.                                                                                                                                                         |
| `wait`     | `duration`, `tab_id?`         | Menjeda selama `duration` detik, 0 hingga 30.                                                                                                                                                                           |

### Membaca halaman

| Anggota         | Input                                  | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_page`     | `filter?`, `depth?`, `ref?`, `tab_id?` | Mengembalikan accessibility tree halaman sebagai teks dengan setiap elemen ditandai dengan referensi seperti `[ref_2]`. Dengan `filter` dihilangkan, kembalikan setiap elemen yang terlihat; dengan `"interactive"`, hanya elemen interaktif yang terlihat; dengan `"all"`, juga elemen di luar viewport. `depth` membatasi kedalaman tree (minimum 1, default 15) dan `ref` membatasi pembacaan ke subtree elemen tersebut. Batasi output hingga 50.000 karakter dan nyatakan hal itu dalam teks; Claude kemudian mempersempit dengan `depth` yang lebih kecil atau `ref`. |
| `find`          | `query`, `tab_id?`                     | Menemukan elemen yang cocok dengan deskripsi bahasa alami seperti `"search field"` atau `"add to cart button"`, dan mengembalikan hingga 20 kecocokan dalam format bertanda yang sama dengan `read_page`.                                                                                                                                                                                                                                                                                                                                                                   |
| `get_page_text` | `tab_id?`                              | Mengembalikan teks halaman yang terlihat sebagai teks biasa, dengan memprioritaskan konten artikel utama; cocok untuk artikel, dokumentasi, dan halaman lain yang padat teks.                                                                                                                                                                                                                                                                                                                                                                                               |

### Formulir dan file

| Anggota                                 | Input                                                     | Deskripsi                                                                                                                                                                                                                                                                                     |
| --------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `form_input`                            | `target: RefTarget`, `value`, `tab_id?`                   | Mengatur nilai elemen formulir secara langsung. `value` adalah `string`, `number`, atau `boolean`; gunakan `boolean` untuk checkbox dan nilai opsi atau teks yang terlihat untuk select.                                                                                                      |
| `file_upload` (nonaktif secara default) | `target: RefTarget`, `paths?`, `document_ids?`, `tab_id?` | Mengatur file pada elemen file-input dari `paths` di filesystem executor, `document_ids` yang telah disiapkan aplikasi Anda, atau keduanya; setidaknya satu diperlukan. Lihat [Mengunggah file](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#upload-files). |

### Diagnostik dan scripting

| Anggota                                     | Input             | Deskripsi                                                                                                                                                                                                                                                                                            |
| ------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_console` (nonaktif secara default)    | `tab_id?`         | Mengembalikan entri konsol tab (baris log, peringatan, dan error) yang terakumulasi sejak pembacaan terakhir, satu baris per entri. Lihat [Membaca aktivitas konsol dan jaringan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#read-console-and-network-activity). |
| `read_network` (nonaktif secara default)    | `tab_id?`         | Mengembalikan permintaan jaringan tab (metode, URL, status, tipe MIME, waktu) sejak pembacaan terakhir, satu baris per entri.                                                                                                                                                                        |
| `javascript_exec` (nonaktif secara default) | `text`, `tab_id?` | Menjalankan `text` sebagai JavaScript dalam konteks halaman dan mengembalikan nilai ekspresi terakhir sebagai teks. Lihat [Mengaktifkan anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools).                              |

### Manajemen tab

| Anggota      | Input            | Deskripsi                                |
| ------------ | ---------------- | ---------------------------------------- |
| `new_tab`    | (tidak ada)      | Membuka tab dan menjadikannya tab aktif. |
| `list_tabs`  | (tidak ada)      | Melaporkan inventaris tab.               |
| `switch_tab` | `tab_id` (wajib) | Menjadikan `tab_id` sebagai tab aktif.   |
| `close_tab`  | `tab_id` (wajib) | Menutup `tab_id`.                        |

Jika berhasil, masing-masing mengembalikan tepat satu blok `browser_state` tanpa teks atau gambar; lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results).

## Mengonfigurasi toolset

Selain `type`, entri toolset menerima `configs`, `cache_control`, dan `allowed_callers`; aturan yang dimiliki bersama field-field ini dengan toolset penggunaan komputer tercantum di bawah [Client toolsets](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets), dan bagian ini membahas default khusus browser. `configs` adalah objek yang dikunci berdasarkan nama anggota, dan nilai setiap anggota menerima dua field:

| Field           | Default                                                                                                                                                             | Arti                                                                                                                                                                                                                                                                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`       | `true`, kecuali `false` untuk empat [anggota opsional](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#enable-optional-member-tools) | Apakah anggota ditawarkan kepada Claude.                                                                                                                                                                                                                                                                                                                               |
| `defer_loading` | `false`                                                                                                                                                             | Apakah definisi toolset ditangguhkan untuk tool search. Harus menghasilkan nilai yang sama pada setiap anggota yang diaktifkan. Dengan empat anggota opsional tetap nonaktif, menangguhkan toolset berarti mengaturnya pada 27 anggota lainnya; lihat [Client toolsets](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets). |

### Mengaktifkan atau menonaktifkan alat anggota

Cantumkan hanya anggota yang ingin Anda ubah di `configs`; setiap anggota yang Anda hilangkan mempertahankan default-nya. Misalnya, executor yang mengimplementasikan pembacaan konsol tetapi tidak mengimplementasikan kontrol pointer tingkat rendah atau menahan tombol mengaktifkan `read_console` dan menahan tiga anggota:

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

Anggota yang dinonaktifkan menghilang dari definisi yang diterima Claude; hal itu tidak menjamin Claude tidak akan pernah menyebutkannya, jadi executor Anda tetap menjawab panggilan semacam itu dengan [hasil error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#return-errors-from-your-executor).

### Menggabungkan dengan alat lain

Deklarasikan alat penggunaan browser bersama alat Anda sendiri dan alat lain yang disediakan Anthropic dalam array `tools` yang sama. Alat kustom boleh memiliki nama yang sama dengan anggota (misalnya `navigate` Anda sendiri), karena `toolset_name` membedakan panggilan Claude, tetapi tidak ada entri lain yang boleh bernama `browser`, dan sebuah permintaan hanya boleh berisi satu entri toolset browser.

Anda juga dapat mendeklarasikannya bersama [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), baik toolset maupun versi alat penggunaan komputer yang lebih lama. Keduanya bekerja secara independen, masing-masing dalam bingkai koordinatnya sendiri (piksel viewport di sini, piksel screenshot desktop di sana), dan panggilan Claude ke anggota yang memiliki nama sama, seperti `screenshot` atau `key`, dibedakan oleh `toolset_name`.

## Mengaktifkan anggota opsional

Empat alat anggota dinonaktifkan secara default: `javascript_exec` dan `file_upload` karena keduanya memperluas apa yang dapat dibuat Claude lakukan oleh halaman yang dimanipulasi, serta `read_console` dan `read_network` karena tidak setiap stack otomatisasi browser dapat menyediakan log tersebut dan keduanya memperluas konten yang dikendalikan halaman yang mencapai Claude. Aktifkan masing-masing dengan `configs` (misalnya, `"configs": {"file_upload": {"enabled": true}}`) hanya ketika executor Anda mengimplementasikannya dan tugas membutuhkannya.

### Mengunggah file

`file_upload` mengatur file pada elemen `<input type="file">` secara langsung, yang lebih andal daripada mengendalikan pemilih file native. `target`-nya hanya berupa referensi, karena panggilan membutuhkan identitas elemen, dan menerima `paths`, `document_ids`, atau keduanya:

* `paths` adalah path file di filesystem executor, untuk deployment di mana executor dapat membaca file aplikasi Anda secara langsung (kondisi yang sama di mana Anda mengisi `path` unduhan).
* `document_ids` adalah pengidentifikasi untuk file yang telah disiapkan aplikasi Anda untuk browser, untuk deployment di mana executor tidak dapat melakukannya. Aplikasi Anda menentukan arti pengidentifikasi tersebut; batasi resolusinya seperti Anda membatasi `paths`, yaitu ke file yang disiapkan untuk tugas ini.

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

Claude menulis path ini saat membaca halaman yang tidak tepercaya, sehingga implementasi yang tidak dibatasi akan memungkinkan halaman berbahaya mengarahkan pengunggahan file apa pun yang dapat dibaca executor ke situs yang dikendalikan halaman tersebut. Aktifkan anggota ini hanya ketika executor Anda meresolusi setiap path (mengikuti symlink dan segmen `..`) dan tidak menerima apa pun di luar direktori unggahan khusus yang masuk allowlist yang hanya berisi file yang ditujukan untuk tugas tersebut. Jangan gunakan kembali direktori unduhan browser untuk ini; jika Anda melakukannya, setiap file yang menyebabkan browser mengunduh oleh halaman menjadi dapat diunggah.

### Menjalankan JavaScript di halaman

`javascript_exec` menjalankan ekspresi yang ditulis Claude dalam konteks halaman dan mengembalikan nilai ekspresi terakhir sebagai teks; Claude menulis ekspresi, bukan pernyataan `return`. Kode berjalan dengan hak akses penuh halaman, termasuk cookie, storage, dan permintaan same-origin-nya. Aktifkan anggota ini hanya dalam sesi yang tidak menyimpan kredensial, pertahankan domain allowlist dari [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations) tetap berlaku, perlakukan nilai yang dikembalikan sebagai input yang tidak tepercaya, dan catat kode yang dikeluarkan Claude.

### Membaca aktivitas konsol dan jaringan

`read_console` mengembalikan entri konsol tab dan `read_network` mengembalikan permintaan jaringannya, masing-masing sebagai teks dengan satu baris untuk setiap entri yang terakumulasi sejak pembacaan sebelumnya pada tab tersebut. Baris konsol membawa entri log, peringatan, atau error; baris jaringan membawa metode, URL, status, tipe MIME, dan waktu. Entri hanya ada sejak saat otomatisasi browser Anda terhubung ke tab, sehingga hasil kosong tidak berarti tab yang sudah terbuka sebelumnya tidak memiliki lalu lintas.

Anggota-anggota ini memungkinkan Claude mendiagnosis halaman yang bermasalah (permintaan gagal di balik spinner, error skrip di balik tombol yang tidak responsif) tanpa screenshot berulang. Entri konsol dan jaringan dikendalikan oleh halaman dan sering berisi rahasia seperti token dalam URL permintaan, jadi redaksi nilai yang menyerupai kredensial yang tidak Anda inginkan dalam konteks Claude dan potong entri yang sangat panjang sebelum mengembalikannya.

## Melacak tab dengan `browser_state`

Claude mengacu pada tab melalui `tab_id`, aplikasi Anda adalah sumber kebenaran tentang tab mana yang ada, dan Anda melaporkan status tersebut dalam blok konten `browser_state` yang tidak pernah diterima Claude secara langsung: API merender teks yang dibaca Claude darinya.

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

* `tabs` adalah inventaris lengkap tab yang terbuka setelah panggilan, bukan delta. Nilainya boleh kosong; setiap kali tidak kosong, tepat satu entri memiliki `"active": true`.
* `state_changes` (tidak ditampilkan di sini) melaporkan efek samping dari panggilan: entri `tab_opened` untuk setiap tab yang dibuka oleh panggilan dan masih terbuka saat panggilan selesai, yang `tab_id`-nya juga harus muncul di `tabs`, serta [peristiwa unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads). Hilangkan field ini ketika tidak ada yang perlu dilaporkan; array kosong akan ditolak.
* Kirim blok ini hanya pada hasil yang menjawab panggilan anggota browser, paling banyak sekali untuk setiap `tool_result`, dan jangan pernah pada hasil dengan `is_error: true`. Anda menyatakan “tidak ada status tab untuk dilaporkan” dengan menghilangkan blok ini.
* API merender `tabs`, dan entri unduhan apa pun di `state_changes`, menjadi teks untuk Claude. Dua bagian berikutnya dan [Melaporkan unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads) menunjukkan teks tersebut.

**Anda yang menetapkan nilai `tab_id`.** String stabil apa pun dapat digunakan, seperti pengidentifikasi halaman dari pustaka otomatisasi Anda atau penghitung Anda sendiri, selama Anda tidak menggunakan ulang `tab_id` ketika tab dengan pengidentifikasi tersebut masih tercantum sebagai terbuka pada hasil sebelumnya. API memberlakukan batasan berikut pada blok ini:

* Setiap `tab_id`, `title`, dan `url` paling banyak 4.096 karakter, `tab_id` tidak boleh kosong, dan tidak satu pun boleh berisi karakter kontrol (termasuk baris baru) atau pemisah baris atau paragraf Unicode.
* Satu blok dapat mencantumkan paling banyak 100 tab dan 200 perubahan status.
* Batasan yang sama berlaku untuk `tab_id` yang diteruskan Claude ke `switch_tab` dan `close_tab`, karena API merendernya ke dalam teks hasil, jadi jawab panggilan yang `tab_id`-nya melanggar batasan tersebut dengan hasil error, bukan blok `browser_state`.

<Warning>
  Judul dan URL tab berasal dari halaman dan dirender menjadi teks yang dibaca Claude, sehingga keduanya merupakan permukaan “prompt injection” (injeksi prompt). API merender URL tab apa adanya, jadi sanitasi URL yang berasal dari halaman sebelum mengisi `tabs`. API meng-escape tanda kutip ganda dan backslash dalam judul saat merendernya, jadi jangan melakukan pre-escape pada judul (judul yang sudah di-escape akan sampai ke Claude dalam keadaan ter-escape ganda); memotong atau membuang judul yang mencurigakan tetap bermanfaat. `url`, `path`, dan `error` dari entri unduhan juga dirender menjadi teks yang dibaca Claude, jadi perlakukan juga sebagai tidak tepercaya; API memberi tanda kutip dan meng-escape nilai-nilai tersebut seperti halnya judul. Batasan panjang dan karakter yang diberlakukan API adalah batas minimum, bukan pertahanan.
</Warning>

### Hasil manajemen tab

Untuk `new_tab`, `switch_tab`, `close_tab`, dan `list_tabs`, `content` dari hasil yang berhasil adalah tepat satu blok `browser_state` tanpa teks atau gambar, dan API menulis teks yang diterima Claude. Blok dari hasil `new_tab` juga harus memuat tepat satu perubahan status `tab_opened` yang `tab_id`-nya cocok dengan entri yang ditandai `active: true`.

| Anggota      | Teks yang diterima Claude                                                                                                        |
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

Sebagai contoh, ketika Claude memanggil `new_tab` (`input`-nya kosong), executor Anda membuka tab, menjadikannya aktif, dan mengembalikan inventaris dengan satu entri `tab_opened`:

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

Claude menerima `Created new tab with tab_id: tab-3, URL: about:blank. It is now the current tab.` Laporkan URL tempat tab dibuka, seperti di sini, bukan URL yang kemudian menjadi tujuan pengalihannya; hasil berikutnya melaporkan URL tab yang berlaku saat itu.

### Konteks tab pada hasil lainnya

Pada setiap anggota lainnya, blok ini bersifat opsional: kirimkan ketika kumpulan tab yang terbuka, tab aktif, atau judul maupun URL suatu tab berubah, atau ketika ada `state_changes` untuk dilaporkan, dan selalu sertakan inventaris `tabs` lengkap. Ketika sebuah hasil memuat teks dan blok `browser_state` sekaligus, API menambahkan footer `Tab Context` ke teks hasil tersebut, dipisahkan dari teks Anda dengan satu baris kosong, sehingga Claude menerima status baru tanpa panggilan `list_tabs` terpisah:

```text wrap
Tab Context:
- Executed on tab_id: tab-1
- Available tabs:
  • tab_id tab-1: "Documentation" (https://example.com/docs)
  • tab_id tab-2: "Pricing" (https://example.com/pricing)
```

`Executed on` menyebutkan tab tempat panggilan dijalankan, yaitu input `tab_id`-nya jika ada dan selain itu tab aktif, dan baris-baris tab pada footer tidak memuat penanda `(current)`. Jangan menambahkan teks ini sendiri; kirim blok terstruktur dan biarkan API merendernya. Footer ini dideduplikasi, sehingga status tab yang identik tidak dirender lagi pada hasil berikutnya dan mengisi blok secara leluasa tidak menimbulkan biaya apa pun.

Tiga kasus tidak merender footer meskipun blok tersedia:

* Setiap hasil `zoom`.
* Hasil tanpa blok `text` (misalnya, hasil `screenshot` yang hanya berisi gambar). Tidak ada yang dirender atau diingat untuk hasil tersebut; konteks tab muncul pada hasil berikutnya yang memuat teks dan blok `browser_state` sekaligus, jadi sertakan blok teks singkat bersama gambar ketika Anda ingin perubahan tab sampai ke Claude pada hasil yang sama. Pengecualiannya adalah hasil yang bloknya melaporkan [peristiwa unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads). API menambahkan baris-baris unduhan sebagai blok teks, dan footer mengikutinya seperti pada hasil mana pun yang berisi teks.
* Hasil yang daftar `tabs`-nya kosong pada panggilan yang tidak membawa `tab_id`, karena tidak ada tab yang dapat disebutkan.

Sebagai contoh, ketika Claude mengklik tautan “Pricing” (`ref_5`) sebelumnya dalam sesi ini, halaman membukanya di tab baru yang tidak diminta Claude, dan tanpa laporan Claude harus memanggil `list_tabs` untuk menemukannya. Kembalikan konfirmasi klik ditambah blok yang `state_changes`-nya menyebutkan tab yang dibuka, dengan menandai tab mana pun yang dibiarkan aktif oleh executor Anda:

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

Claude menerima `Clicked element ref_5.` diikuti footer Tab Context yang ditampilkan sebelumnya. Tab yang dibuka selama panggilan yang gagal tidak mendapatkan entri `tab_opened`, karena hasil error tidak memuat `browser_state`; tab tersebut muncul di inventaris `tabs` dari hasil berhasil berikutnya. Dalam sebuah batch, lampirkan blok ke hasil panggilan tempat perubahan terjadi, dan berikan blok tersendiri untuk setiap hasil manajemen tab yang berhasil meskipun hasil sebelumnya dalam giliran yang sama telah melaporkan status yang sama.

### Melaporkan unduhan

Ketika sebuah klik atau navigasi memulai unduhan file, laporkan di `state_changes` pada hasil panggilan tempat unduhan tersebut terjadi, dikorelasikan di seluruh hasil melalui `download_id` yang Anda tetapkan. Unduhan berjalan secara asinkron dan dapat mencakup beberapa hasil, sehingga ada tiga jenis peristiwa:

| `type`               | Field                                        | Kapan dikirim                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `download_started`   | `download_id`, `url`                         | Pada hasil panggilan tempat unduhan dimulai. `url` adalah URL akhir tempat file disajikan, setelah pengalihan.                                                                                                                                                                                                                                                                    |
| `download_completed` | `download_id`, `url`, `path?`, `size_bytes?` | Pada hasil dari panggilan berikutnya mana pun yang sedang berjalan ketika unduhan selesai. Sertakan `path` hanya ketika alat lain di lingkungan yang sama (misalnya, [alat bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool) atau `file_upload`) dapat membaca file di sana; jika tidak, `download_id` adalah satu-satunya pengidentifikasi unduhan. |
| `download_failed`    | `download_id`, `url`, `error?`               | Ketika unduhan gagal atau dibatalkan, dengan alasannya di `error` jika browser menyediakannya.                                                                                                                                                                                                                                                                                    |

API merender setiap entri sebagai satu baris teks untuk Claude, sesuai urutan kemunculan entri. API menambahkan baris-baris tersebut setelah teks hasil, dipisahkan oleh satu baris kosong, dan sebelum footer Tab Context mana pun. Setiap jenis hasil anggota memuat baris-baris ini, termasuk hasil `zoom` dan hasil manajemen tab. Hasil tanpa blok `text` mendapatkannya sebagai blok teks tersendiri. Setiap baris memberikan `download_id` dan `url`, ditambah `path` dan `size_bytes` (untuk `download_completed`) atau `error` (untuk `download_failed`) jika Anda mengirimkannya. Anda tidak perlu mendeskripsikan unduhan dalam teks Anda sendiri. API membungkus `url`, `path`, dan `error` dengan tanda kutip ganda dan meng-escape tanda kutip ganda serta backslash di dalamnya, jadi jangan melakukan pre-escape pada nilai-nilai ini.

Sebagai contoh, klik pada “Download price list (CSV)” (`ref_8`) di tab Pricing memulai unduhan, sehingga hasil klik tersebut memuat entri `download_started` dengan `download_id` `"dl-1"` dan URL file. Unduhan selesai ketika panggilan `screenshot` berikutnya sedang berjalan, sehingga `content` hasil tersebut berisi gambar, blok teks seperti `Screenshot captured.`, dan blok `browser_state` berikut yang melaporkan penyelesaian di bawah `download_id` yang sama:

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

Claude menerima `Screenshot captured.` diikuti baris kosong dan baris seperti ini:

```text wrap
Download completed with download_id: dl-1, URL: "https://example.com/pricing/price-list.csv". Saved to "/home/user/downloads/price-list.csv". Size: 48213 bytes.
```

Laporan unduhan mengikuti aturan berikut:

* Kirim paling banyak satu entri untuk setiap `download_id` dalam satu blok, sehingga unduhan yang dimulai dan selesai selama panggilan yang sama hanya melaporkan `download_completed`.
* Jangan pernah mengirim `state_changes` pada hasil `is_error: true`; laporkan peristiwa unduhan yang terjadi selama panggilan yang gagal pada hasil berhasil berikutnya.
* `state_changes` bukanlah inventaris unduhan yang sedang berlangsung; laporkan setiap peristiwa satu kali.
* Setiap entri hanya memuat field yang dideklarasikan oleh `type`-nya. `size_bytes` adalah bilangan bulat non-negatif, `download_id` tidak boleh kosong, dan masing-masing `download_id`, `url`, `path`, dan `error` paling banyak 4.096 karakter tanpa karakter kontrol atau pemisah baris atau paragraf Unicode. `url` berasal dari server jarak jauh dan sering kali memuat kredensial query-string bertanda tangan setelah pengalihan, jadi hapus parameter query yang tidak Anda inginkan dalam konteks Claude dan sanitasi URL tersebut sebelum melaporkannya atau menggunakannya dalam path sistem file.

## Menangani error

Laporkan panggilan yang gagal kepada Claude sebagai hasil error biasa: `is_error: true`, konten teks yang menjelaskan apa yang salah, `toolset_name` yang digemakan kembali, dan tanpa blok `browser_state`.

### Mengembalikan error dari executor Anda

Buat teks error yang spesifik, karena Claude membacanya dan beradaptasi: `Error: Navigation to https://example.com/status timed out after 30 seconds. The page may be unavailable.` memberi Claude sesuatu untuk ditindaklanjuti, sedangkan `Error: navigation failed` yang polos tidak. Kasus umum lainnya:

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

  <Accordion title="Anggota yang dinonaktifkan atau tidak diimplementasikan">
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
    Ketika `left_click` pada `ref_3` dari [Tindakan batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions) gagal dengan error referensi kedaluwarsa yang ditampilkan sebelumnya, panggilan `type` dan `key` setelahnya masing-masing mendapatkan hasil ini:

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

API memvalidasi entri toolset serta setiap blok `tool_use` dan `tool_result` anggota dalam percakapan. Ketika salah satunya tidak valid, API mengembalikan `invalid_request_error` sebelum Claude berjalan. Pada tabel berikut, kolom kiri menyebutkan apa yang Anda kirim.

| Permintaan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Mengapa gagal dan apa yang harus dilakukan                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Opsi atau kombinasi yang tidak diterima oleh entri toolset, misalnya, `name`, `strict: true`, `input_examples`, `defer_loading` pada entri itu sendiri, kunci `configs` yang bukan nama anggota, field selain `enabled` atau `defer_loading` dalam nilai `configs` suatu anggota ([Mengonfigurasi toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset)), anggota yang diaktifkan dengan nilai `defer_loading` yang berbeda ([Mengonfigurasi toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset)), `configs` yang tidak menyisakan satu pun anggota yang diaktifkan, pemanggil eksekusi kode di `allowed_callers`, header beta lama `fine-grained-tool-streaming-2025-05-14` pada permintaan, `tool_choice` bertipe `tool` yang menyebut `browser` atau suatu anggota, atau entri toolset browser kedua atau alat lain bernama `browser` | Hal-hal ini tidak didukung pada toolset klien. Lihat [Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets) untuk setiap aturan beserta alternatifnya.                                                                            |
| `tool_result` yang menjawab panggilan anggota tanpa `"toolset_name": "browser"` atau dengan nilai yang berbeda, atau `toolset_name` pada hasil yang panggilannya bukan panggilan anggota                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Gemakan kembali `toolset_name` secara persis pada hasil anggota, dan hanya pada hasil tersebut.                                                                                                                                                                                          |
| `tool_use` anggota dari giliran sebelumnya tanpa `tool_result` yang sesuai                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Jawab setiap panggilan anggota, termasuk yang tidak Anda jalankan setelah terjadi kegagalan.                                                                                                                                                                                             |
| Blok konten selain `text`, `image`, atau `browser_state` dalam hasil anggota                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Hasil anggota hanya menerima ketiga jenis blok tersebut.                                                                                                                                                                                                                                 |
| Blok `browser_state` yang melanggar aturan di [Melacak tab dengan `browser_state`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state), misalnya, blok pada hasil `is_error: true` atau pada hasil yang tidak menjawab panggilan anggota browser, lebih dari satu blok dalam satu hasil, `tabs` yang tidak kosong tanpa tepat satu entri `active: true`, `tab_id` duplikat, array `state_changes` kosong, `tab_opened` yang `tab_id`-nya tidak ada di `tabs`, dua perubahan status untuk satu `download_id` atau field perubahan status yang tidak dideklarasikan oleh `type`-nya ([Melaporkan unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#report-downloads)), atau field yang melebihi batasnya                                                                                                                                                           | Perbaiki blok tersebut. “Tidak ada yang perlu dilaporkan” dinyatakan dengan menghilangkan blok atau field `state_changes`, bukan dengan nilai kosong.                                                                                                                                    |
| Hasil `new_tab`, `switch_tab`, `close_tab`, atau `list_tabs` yang berhasil yang `content`-nya bukan tepat satu blok `browser_state`, atau hasil `new_tab` tanpa tepat satu `tab_opened` yang cocok dengan tab aktif                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | API merender hasil-hasil ini dari blok tersebut dan membutuhkannya dalam bentuk yang persis seperti itu; lihat [Hasil manajemen tab](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#tab-management-results).                                             |
| `image` dalam hasil yang melebihi [batas ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) model Anda, atau melebihi batas per gambar yang lebih ketat yang berlaku setelah permintaan memuat [lebih dari 20 gambar](https://platform.claude.com/docs/id/build-with-claude/vision#request-limits), termasuk screenshot dan gambar `zoom` pada hasil sebelumnya                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | API tidak memperkecil gambar toolset. Ubah ukuran screenshot sebelum mengembalikannya ([Sesuaikan ukuran screenshot agar sesuai dengan batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions)). |
| `model` yang tidak mendukung `browser_toolset_20260801`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Lihat [Dukungan API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#availability-feature-support) untuk model yang didukung.                                                                                                                             |

## Keterbatasan

* **Ketersediaan platform:** Penggunaan browser tersedia di Claude API dan [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed).
* **Hanya streaming input utuh:** Ketika Anda melakukan streaming, `input` setiap anggota tiba sebagai satu `input_json_delta` yang lengkap ([Toolset klien](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference#client-toolsets)).
* **Referensi elemen bersifat upaya terbaik:** Halaman yang sangat dinamis (daftar tervirtualisasi, antarmuka yang dirender dengan canvas, halaman yang dirender ulang saat di-scroll) mungkin tidak mengekspos referensi yang stabil, dan di sana Claude beralih ke screenshot dan klik berbasis koordinat.
* **`read_console` dan `read_network` bergantung pada otomatisasi browser Anda:** Keduanya hanya melaporkan apa yang dapat ditangkap oleh otomatisasi tersebut, dan hanya sejak saat otomatisasi terhubung ke sebuah tab.
* **Keterbatasan agen secara umum berlaku:** Latency, akurasi visual, dan risiko prompt injection berlaku juga dari penggunaan komputer (lihat [Keterbatasan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#understand-computer-use-limitations) pada alat penggunaan komputer), dan panduannya di bawah [Mengoptimalkan kinerja model dengan prompting](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#optimize-model-performance-with-prompting), [Mengelola riwayat screenshot](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#manage-screenshot-history), dan [Mengikuti praktik terbaik implementasi](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#follow-implementation-best-practices) (jeda tindakan, validasi tindakan, dan logging) juga berlaku untuk executor browser.

## Harga dan retensi data

Penggunaan browser mengikuti [harga penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat penggunaan browser:

**Overhead definisi toolset:** Mendeklarasikan `browser_toolset_20260801` dengan anggota default-nya menambahkan sekitar 6.600 token input ke sebuah permintaan (sekitar 6.670 pada Claude Sonnet 5 dan sekitar 6.610 pada model lain yang didukung), yang mencakup definisi alat anggota dan prompt sistem penggunaan alat. Mengaktifkan keempat anggota opsional menambahkan sekitar 880 token, dan menonaktifkan anggota dengan `configs` mengurangi jumlahnya. Jumlah pasti untuk sebuah permintaan dilaporkan dalam `usage` respons, dan Anda dapat memperkirakannya terlebih dahulu dengan [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting).

**Konsumsi token tambahan:**

* Gambar tangkapan layar dan zoom yang dikembalikan dalam hasil alat, ditagih sebagai input gambar (lihat [Harga Vision](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size))
* Hasil alat berupa teks yang dikembalikan ke Claude, seperti pohon aksesibilitas, teks halaman, dan entri konsol atau jaringan

<Note>
  Jika Anda juga menggunakan alat penggunaan komputer, alat bash, alat editor teks, atau alat Anda sendiri bersama penggunaan browser, alat-alat tersebut memiliki biaya token masing-masing seperti yang didokumentasikan di halaman terkait.
</Note>

Sesi browser, unduhan, dan file yang diunggah tetap berada di lingkungan Anda; screenshot, teks halaman, dan status tab yang Anda kembalikan merupakan bagian dari konten permintaan API Anda dan mengikuti kebijakan retensi standar, atau pengaturan ZDR Anda jika Anda memilikinya. Alat penggunaan browser memenuhi syarat ZDR; lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) untuk periode retensi dan kelayakan di seluruh fitur.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Penggunaan browser dan komputer dengan toolset SDK" icon="code" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk">
    Mulai dari driver mitra, atau tulis driver Anda sendiri dalam Python atau TypeScript. SDK menjalankan loop dan pemeriksaan yang Anda konfigurasi.
  </Card>

  <Card title="Alat penggunaan komputer" icon="computer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Berikan Claude kendali atas desktop penuh ketika tugas keluar dari browser; panduan implementasinya juga berlaku untuk executor browser.
  </Card>

  <Card title="Menangani panggilan alat" icon="wrench" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls">
    Format blok `tool_result`, kembalikan gambar dan error, serta lanjutkan percakapan.
  </Card>

  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi toolset klien dan setiap alat lain yang disediakan Anthropic, beserta versi dan parameternya.
  </Card>
</CardGroup>

## Ketersediaan

Alat penggunaan browser tersedia di model tertentu dan layak untuk retensi data nol.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status   | Platform cloud                                                                                                                                                   | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia | Claude API, [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tidak tersedia

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                   | HIPAA                                                                                                    |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))                                                                                   | Tidak layak                                                                                              |
| Detail | Alat sisi klien. Anthropic tidak menjalankan tindakan browser atau menyimpan konten halaman di luar penanganan API standar. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#data-retention) | Tidak tercakup dalam kesiapan HIPAA; permintaan yang menyertakan alat penggunaan browser tidak diblokir. |

Endpoint yang berlaku:

* `/v1/messages` dengan toolset `browser`
