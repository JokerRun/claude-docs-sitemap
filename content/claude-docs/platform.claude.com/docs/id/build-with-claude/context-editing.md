---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-editing
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: b15a2e65e6a50a40fc730a6d30404c0aafc9e29ee7d4c000c4c659c99f7ad508
---

# Pengeditan konteks

Kelola konteks percakapan secara otomatis seiring pertumbuhannya dengan pengeditan konteks.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Ikhtisar

<Note>
  Untuk sebagian besar kasus penggunaan, [compaction sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk mengelola konteks dalam percakapan yang berjalan lama. Strategi di halaman ini berguna untuk skenario spesifik di mana Anda memerlukan kontrol yang lebih terperinci atas konten apa yang dihapus.
</Note>

Pengeditan konteks memungkinkan Anda untuk secara selektif menghapus konten tertentu dari riwayat percakapan seiring pertumbuhannya. Di luar mengoptimalkan biaya dan tetap berada dalam batas, ini adalah tentang secara aktif mengkurasi apa yang dilihat Claude: konteks adalah sumber daya terbatas dengan hasil yang semakin berkurang, dan konten yang tidak relevan menurunkan fokus model. Pengeditan konteks memberi Anda kontrol runtime yang terperinci atas kurasi tersebut. Untuk prinsip yang lebih luas di balik manajemen konteks, lihat [Rekayasa konteks yang efektif](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Halaman ini mencakup:

* **Penghapusan hasil alat** - Terbaik untuk alur kerja agentik dengan penggunaan alat yang berat di mana hasil alat lama tidak lagi diperlukan
* **Penghapusan blok pemikiran** - Untuk mengelola blok pemikiran saat menggunakan pemikiran diperpanjang, dengan opsi untuk mempertahankan pemikiran terbaru demi kontinuitas konteks
* **Compaction SDK sisi klien** - Alternatif berbasis SDK untuk manajemen konteks berbasis ringkasan (compaction sisi server umumnya lebih disarankan)

| Pendekatan      | Di mana berjalan | Strategi                                                                                                   | Cara kerja                                                                                                                                                                                                                                                                                             |
| --------------- | ---------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Sisi server** | API              | Penghapusan hasil alat (`clear_tool_uses_20250919`) Penghapusan blok pemikiran (`clear_thinking_20251015`) | Diterapkan sebelum prompt mencapai Claude. Menghapus konten tertentu dari riwayat percakapan. Setiap strategi dapat dikonfigurasi secara independen.                                                                                                                                                   |
| **Sisi klien**  | SDK              | Compaction                                                                                                 | Tersedia di [SDK Python, TypeScript, dan Ruby](/docs/id/cli-sdks-libraries/overview) saat menggunakan [`tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner). Menghasilkan ringkasan dan menggantikan riwayat percakapan lengkap. Lihat [Compaction sisi klien](#client-side-compaction-sdk). |

## Strategi sisi server

<Note>
  Pengeditan konteks berada dalam tahap beta dengan dukungan untuk penghapusan hasil alat dan penghapusan blok pemikiran. Untuk mengaktifkannya, gunakan header beta `context-management-2025-06-27` dalam permintaan API Anda.

  Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88).
</Note>

### Penghapusan hasil alat

Strategi `clear_tool_uses_20250919` menghapus hasil alat ketika konteks percakapan tumbuh melampaui ambang batas yang Anda konfigurasikan. Ini sangat berguna untuk alur kerja agentik dengan penggunaan alat yang berat. Hasil alat yang lebih lama (seperti konten file atau hasil pencarian) tidak lagi diperlukan setelah Claude memprosesnya.

Saat diaktifkan, API secara otomatis menghapus hasil alat tertua dalam urutan kronologis. API menggantikan setiap hasil yang dihapus dengan teks placeholder sehingga Claude tahu bahwa hasil tersebut telah dihapus. Secara default, hanya hasil alat yang dihapus. Anda dapat secara opsional menghapus baik hasil alat maupun panggilan alat (parameter tool use) dengan mengatur `clear_tool_inputs` ke true.

### Penghapusan blok pemikiran

Strategi `clear_thinking_20251015` mengelola blok `thinking` dalam percakapan ketika pemikiran diperpanjang diaktifkan. Strategi ini memberi Anda kontrol atas pelestarian pemikiran: Anda dapat memilih untuk menyimpan lebih banyak blok pemikiran untuk mempertahankan kontinuitas penalaran, atau menghapusnya secara lebih agresif untuk menghemat ruang konteks.

<Tip>
  **Perilaku default:** Default bervariasi berdasarkan kelas model.

  | Kelas model | Simpan semua pemikiran sebelumnya     | Simpan hanya pemikiran dari giliran terakhir |
  | ----------- | ------------------------------------- | -------------------------------------------- |
  | Opus        | Claude Opus 4.5 dan yang lebih baru   | Claude Opus 4.1 (usang) dan yang lebih lama  |
  | Sonnet      | Claude Sonnet 4.6 dan yang lebih baru | Claude Sonnet 4.5 dan yang lebih lama        |
  | Haiku       | (tidak ada)                           | Semua model hingga Claude Haiku 4.5          |

  Gunakan strategi ini untuk mengganti default. Jika kode Anda berjalan di beberapa tingkatan model, atur `keep` secara eksplisit daripada mengandalkan default per-model.
</Tip>

Giliran percakapan asisten dapat mencakup beberapa blok konten (misalnya, saat menggunakan alat) dan beberapa blok pemikiran (misalnya, dengan [pemikiran berselang](/docs/id/build-with-claude/extended-thinking#interleaved-thinking)).

### Pengeditan konteks terjadi di sisi server

Pengeditan konteks diterapkan di sisi server sebelum prompt mencapai Claude. Aplikasi klien Anda mempertahankan riwayat percakapan lengkap yang tidak dimodifikasi. Anda tidak perlu menyinkronkan status klien Anda dengan versi yang diedit. Lanjutkan mengelola riwayat percakapan lengkap Anda secara lokal seperti biasa.

### Pengeditan konteks dan caching prompt

Interaksi pengeditan konteks dengan [caching prompt](/docs/id/build-with-claude/prompt-caching) bervariasi berdasarkan strategi:

* **Penghapusan hasil alat**: Membatalkan prefiks prompt yang di-cache ketika konten dihapus. Untuk memperhitungkan hal ini, hapus token yang cukup agar pembatalan cache sepadan. Gunakan parameter `clear_at_least` untuk memastikan jumlah minimum token dihapus setiap kali. Anda akan dikenakan biaya penulisan cache setiap kali konten dihapus, tetapi permintaan berikutnya dapat menggunakan kembali prefiks yang baru di-cache.

* **Penghapusan blok pemikiran**: Ketika blok pemikiran **disimpan** dalam konteks (tidak dihapus), cache prompt dipertahankan, memungkinkan cache hit dan mengurangi biaya token input. Ketika blok pemikiran **dihapus**, cache dibatalkan pada titik di mana penghapusan terjadi. Konfigurasikan parameter `keep` berdasarkan apakah Anda ingin memprioritaskan kinerja cache atau ketersediaan jendela konteks.

## Model yang didukung

Pengeditan konteks tersedia di semua model Claude yang didukung.

## Penggunaan penghapusan hasil alat

Cara paling sederhana untuk mengaktifkan penghapusan hasil alat adalah dengan hanya menentukan tipe strategi. Semua [opsi konfigurasi](#configuration-options-for-tool-result-clearing) lainnya menggunakan nilai default-nya:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Search for recent developments in AI"
              }
          ],
          "tools": [
              {
                  "type": "web_search_20250305",
                  "name": "web_search"
              }
          ],
          "context_management": {
              "edits": [
                  {"type": "clear_tool_uses_20250919"}
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Search for recent developments in AI
  tools:
    - type: web_search_20250305
      name: web_search
  context_management:
    edits:
      - type: clear_tool_uses_20250919
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[{"role": "user", "content": "Search for recent developments in AI"}],
      tools=[{"type": "web_search_20250305", "name": "web_search"}],
      betas=["context-management-2025-06-27"],
      context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Search for recent developments in AI"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search"
      }
    ],
    context_management: {
      edits: [{ type: "clear_tool_uses_20250919" }]
    },
    betas: ["context-management-2025-06-27"]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [
          new() { Role = Role.User, Content = "Search for recent developments in AI" }
      ],
      Tools = [
          new BetaWebSearchTool20250305()
      ],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaClearToolUses20250919Edit()]
      },
      Betas = [AnthropicBeta.ContextManagement2025_06_27]
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Search for recent developments in AI")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfWebSearchTool20250305: &anthropic.BetaWebSearchTool20250305Param{}},
  	},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearToolUses20250919: &anthropic.BetaClearToolUses20250919EditParam{}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaContextManagement2025_06_27,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaWebSearchTool20250305;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Search for recent developments in AI")
          .addTool(BetaWebSearchTool20250305.builder().build())
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearToolUses20250919Edit.builder().build())
              .build())
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Search for recent developments in AI']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      tools: [
          ['type' => 'web_search_20250305', 'name' => 'web_search']
      ],
      contextManagement: [
          'edits' => [
              ['type' => 'clear_tool_uses_20250919']
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Search for recent developments in AI" }
    ],
    tools: [
      { type: "web_search_20250305", name: "web_search" }
    ],
    context_management: {
      edits: [
        { type: "clear_tool_uses_20250919" }
      ]
    },
    betas: ["context-management-2025-06-27"]
  )
  puts response
  ```
</CodeGroup>

### Konfigurasi lanjutan

Anda dapat menyesuaikan perilaku penghapusan hasil alat dengan parameter tambahan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Create a simple command line calculator app using Python"
              }
          ],
          "tools": [
              {
                  "type": "text_editor_20250728",
                  "name": "str_replace_based_edit_tool",
                  "max_characters": 10000
              },
              {
                  "type": "web_search_20250305",
                  "name": "web_search",
                  "max_uses": 3
              }
          ],
          "context_management": {
              "edits": [
                  {
                      "type": "clear_tool_uses_20250919",
                      "trigger": {
                          "type": "input_tokens",
                          "value": 30000
                      },
                      "keep": {
                          "type": "tool_uses",
                          "value": 3
                      },
                      "clear_at_least": {
                          "type": "input_tokens",
                          "value": 5000
                      },
                      "exclude_tools": ["web_search"]
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Create a simple command line calculator app using Python
  tools:
    - type: text_editor_20250728
      name: str_replace_based_edit_tool
      max_characters: 10000
    - type: web_search_20250305
      name: web_search
      max_uses: 3
  context_management:
    edits:
      - type: clear_tool_uses_20250919
        trigger:
          type: input_tokens
          value: 30000
        keep:
          type: tool_uses
          value: 3
        clear_at_least:
          type: input_tokens
          value: 5000
        exclude_tools:
          - web_search
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Create a simple command line calculator app using Python",
          }
      ],
      tools=[
          {
              "type": "text_editor_20250728",
              "name": "str_replace_based_edit_tool",
              "max_characters": 10000,
          },
          {"type": "web_search_20250305", "name": "web_search", "max_uses": 3},
      ],
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_tool_uses_20250919",
                  # Memicu pembersihan saat ambang batas terlampaui
                  "trigger": {"type": "input_tokens", "value": 30000},
                  # Jumlah penggunaan alat yang dipertahankan setelah pembersihan
                  "keep": {"type": "tool_uses", "value": 3},
                  # Opsional: Bersihkan setidaknya sebanyak token ini
                  "clear_at_least": {"type": "input_tokens", "value": 5000},
                  # Kecualikan alat-alat ini dari pembersihan
                  "exclude_tools": ["web_search"],
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Create a simple command line calculator app using Python"
      }
    ],
    tools: [
      {
        type: "text_editor_20250728",
        name: "str_replace_based_edit_tool",
        max_characters: 10000
      },
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 3
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_tool_uses_20250919",
          // Memicu pembersihan saat ambang batas terlampaui
          trigger: {
            type: "input_tokens",
            value: 30000
          },
          // Jumlah penggunaan alat yang dipertahankan setelah pembersihan
          keep: {
            type: "tool_uses",
            value: 3
          },
          // Opsional: Bersihkan setidaknya sebanyak token ini
          clear_at_least: {
            type: "input_tokens",
            value: 5000
          },
          // Kecualikan alat-alat ini dari pembersihan
          exclude_tools: ["web_search"]
        }
      ]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [
          new() { Role = Role.User, Content = "Create a simple command line calculator app using Python" }
      ],
      Tools = [
          new BetaToolTextEditor20250728 { MaxCharacters = 10000 },
          new BetaWebSearchTool20250305 { MaxUses = 3 }
      ],
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearToolUses20250919Edit
              {
                  Trigger = new BetaInputTokensTrigger(30000),
                  Keep = new BetaToolUsesKeep(3),
                  ClearAtLeast = new BetaInputTokensClearAtLeast(5000),
                  ExcludeTools = ["web_search"]
              }
          ]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a simple command line calculator app using Python")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfTextEditor20250728: &anthropic.BetaToolTextEditor20250728Param{
  			MaxCharacters: anthropic.Int(10000),
  		}},
  		{OfWebSearchTool20250305: &anthropic.BetaWebSearchTool20250305Param{
  			MaxUses: anthropic.Int(3),
  		}},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearToolUses20250919: &anthropic.BetaClearToolUses20250919EditParam{
  				Trigger: anthropic.BetaClearToolUses20250919EditTriggerUnionParam{
  					OfInputTokens: &anthropic.BetaInputTokensTriggerParam{
  						Value: 30000,
  					},
  				},
  				Keep: anthropic.BetaToolUsesKeepParam{
  					Value: 3,
  				},
  				ClearAtLeast: anthropic.BetaInputTokensClearAtLeastParam{
  					Value: 5000,
  				},
  				ExcludeTools: []string{"web_search"},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
  import com.anthropic.models.beta.messages.BetaWebSearchTool20250305;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  import com.anthropic.models.beta.messages.BetaInputTokensClearAtLeast;
  import com.anthropic.models.beta.messages.BetaToolUsesKeep;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Create a simple command line calculator app using Python")
          .addTool(BetaToolTextEditor20250728.builder()
              .maxCharacters(10000L)
              .build())
          .addTool(BetaWebSearchTool20250305.builder()
              .maxUses(3L)
              .build())
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearToolUses20250919Edit.builder()
                  .trigger(BetaInputTokensTrigger.builder()
                      .value(30000L)
                      .build())
                  .keep(BetaToolUsesKeep.builder()
                      .value(3L)
                      .build())
                  .clearAtLeast(BetaInputTokensClearAtLeast.builder()
                      .value(5000L)
                      .build())
                  .addExcludeTool("web_search")
                  .build())
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a simple command line calculator app using Python'
          ]
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      tools: [
          [
              'type' => 'text_editor_20250728',
              'name' => 'str_replace_based_edit_tool',
              'max_characters' => 10000
          ],
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 3
          ]
      ],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_tool_uses_20250919',
                  'trigger' => [
                      'type' => 'input_tokens',
                      'value' => 30000
                  ],
                  'keep' => [
                      'type' => 'tool_uses',
                      'value' => 3
                  ],
                  'clear_at_least' => [
                      'type' => 'input_tokens',
                      'value' => 5000
                  ],
                  'exclude_tools' => ['web_search']
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Create a simple command line calculator app using Python"
      }
    ],
    tools: [
      {
        type: "text_editor_20250728",
        name: "str_replace_based_edit_tool",
        max_characters: 10000
      },
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 3
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_tool_uses_20250919",
          trigger: {
            type: "input_tokens",
            value: 30000
          },
          keep: {
            type: "tool_uses",
            value: 3
          },
          clear_at_least: {
            type: "input_tokens",
            value: 5000
          },
          exclude_tools: ["web_search"]
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

## Penggunaan penghapusan blok pemikiran

Aktifkan penghapusan blok pemikiran untuk mengelola konteks dan caching prompt secara efektif ketika pemikiran diperpanjang diaktifkan:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 16000,
          "messages": [{"role": "user", "content": "Hello"}],
          "thinking": {"type": "adaptive"},
          "context_management": {
              "edits": [
                  {
                      "type": "clear_thinking_20251015",
                      "keep": {
                          "type": "thinking_turns",
                          "value": 2
                      }
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 16000
  messages:
    - role: user
      content: Hello
  thinking:
    type: adaptive
  context_management:
    edits:
      - type: clear_thinking_20251015
        keep:
          type: thinking_turns
          value: 2
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      messages=[{"role": "user", "content": "Hello"}],
      thinking={"type": "adaptive"},
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_thinking_20251015",
                  "keep": {"type": "thinking_turns", "value": 2},
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 2
          }
        }
      ]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Messages = [
          new() { Role = Role.User, Content = "Hello" }
      ],
      Thinking = new BetaThinkingConfigAdaptive(),
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearThinking20251015Edit
              {
                  Keep = new BetaThinkingTurns(2)
              }
          ]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  	},
  	Thinking: anthropic.BetaThinkingConfigParamUnion{OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{}},
  	Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearThinking20251015: &anthropic.BetaClearThinking20251015EditParam{
  				Keep: anthropic.BetaClearThinking20251015EditKeepUnionParam{
  					OfThinkingTurns: &anthropic.BetaThinkingTurnsParam{
  						Value: 2,
  					},
  				},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearThinking20251015Edit;
  import com.anthropic.models.beta.messages.BetaThinkingTurns;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .addUserMessage("Hello")
          .thinking(BetaThinkingConfigAdaptive.builder().build())
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearThinking20251015Edit.builder()
                  .keep(BetaThinkingTurns.builder()
                      .value(2L)
                      .build())
                  .build())
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      thinking: ['type' => 'adaptive'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_thinking_20251015',
                  'keep' => [
                      'type' => 'thinking_turns',
                      'value' => 2
                  ]
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 2
          }
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

### Opsi konfigurasi untuk penghapusan blok pemikiran

Strategi `clear_thinking_20251015` mendukung konfigurasi berikut:

| Opsi konfigurasi | Default            | Deskripsi                                                                                                                                                                                                                                                                                                                                                              |
| ---------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `keep`           | Spesifik per model | Menentukan berapa banyak giliran asisten terbaru dengan blok pemikiran yang akan dipertahankan. Gunakan `{type: "thinking_turns", value: N}` di mana N harus > 0 untuk menyimpan N giliran terakhir, atau `"all"` untuk menyimpan semua blok pemikiran. Opus 4.5+ dan Sonnet 4.6+: semua giliran. Opus/Sonnet yang lebih lama dan semua Haiku: hanya giliran terakhir. |

**Contoh konfigurasi:**

Simpan blok pemikiran dari 3 giliran asisten terakhir:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 16000,
          "messages": [{"role": "user", "content": "Hello"}],
          "thinking": {"type": "adaptive"},
          "context_management": {
              "edits": [
                  {
                      "type": "clear_thinking_20251015",
                      "keep": {
                          "type": "thinking_turns",
                          "value": 3
                      }
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 16000
  messages:
    - role: user
      content: Hello
  thinking:
    type: adaptive
  context_management:
    edits:
      - type: clear_thinking_20251015
        keep:
          type: thinking_turns
          value: 3
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      messages=[{"role": "user", "content": "Hello"}],
      thinking={"type": "adaptive"},
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_thinking_20251015",
                  "keep": {"type": "thinking_turns", "value": 3},
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 3
          }
        }
      ]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Messages = [
          new() { Role = Role.User, Content = "Hello" }
      ],
      Thinking = new BetaThinkingConfigAdaptive(),
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearThinking20251015Edit
              {
                  Keep = new BetaThinkingTurns(3)
              }
          ]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  	},
  	Thinking: anthropic.BetaThinkingConfigParamUnion{OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{}},
  	Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearThinking20251015: &anthropic.BetaClearThinking20251015EditParam{
  				Keep: anthropic.BetaClearThinking20251015EditKeepUnionParam{
  					OfThinkingTurns: &anthropic.BetaThinkingTurnsParam{
  						Value: 3,
  					},
  				},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(16000L)
      .addUserMessage("Hello")
      .thinking(BetaThinkingConfigAdaptive.builder().build())
      .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
      .contextManagement(BetaContextManagementConfig.builder()
          .addEdit(BetaClearThinking20251015Edit.builder()
              .keep(BetaThinkingTurns.builder()
                  .value(3L)
                  .build())
              .build())
          .build())
      .build();

  BetaMessage response = client.beta().messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      thinking: ['type' => 'adaptive'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_thinking_20251015',
                  'keep' => [
                      'type' => 'thinking_turns',
                      'value' => 3
                  ]
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 3
          }
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

Simpan semua blok pemikiran (memaksimalkan cache hit):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 16000,
          "messages": [{"role": "user", "content": "Hello"}],
          "thinking": {"type": "adaptive"},
          "context_management": {
              "edits": [
                  {
                      "type": "clear_thinking_20251015",
                      "keep": "all"
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 16000
  messages:
    - role: user
      content: Hello
  thinking:
    type: adaptive
  context_management:
    edits:
      - type: clear_thinking_20251015
        keep: all
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      messages=[{"role": "user", "content": "Hello"}],
      thinking={"type": "adaptive"},
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_thinking_20251015",
                  "keep": "all",
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: "all"
        }
      ]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Messages = [
          new() { Role = Role.User, Content = "Hello" }
      ],
      Thinking = new BetaThinkingConfigAdaptive(),
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearThinking20251015Edit
              {
                  Keep = new All()
              }
          ]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  	},
  	Thinking: anthropic.BetaThinkingConfigParamUnion{OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{}},
  	Betas:    []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearThinking20251015: &anthropic.BetaClearThinking20251015EditParam{
  				Keep: anthropic.BetaClearThinking20251015EditKeepUnionParam{
  					OfAll: constant.ValueOf[constant.All](),
  				},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(16000L)
      .addUserMessage("Hello")
      .thinking(BetaThinkingConfigAdaptive.builder().build())
      .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
      .contextManagement(BetaContextManagementConfig.builder()
          .addEdit(BetaClearThinking20251015Edit.builder()
              .keepAll()
              .build())
          .build())
      .build();

  BetaMessage response = client.beta().messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      thinking: ['type' => 'adaptive'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_thinking_20251015',
                  'keep' => 'all'
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [{ role: "user", content: "Hello" }],
    thinking: { type: "adaptive" },
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: "all"
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

### Menggabungkan strategi

Anda dapat menggunakan penghapusan blok pemikiran dan penghapusan hasil alat secara bersamaan:

<Note>
  Saat menggunakan beberapa strategi, strategi `clear_thinking_20251015` harus dicantumkan terlebih dahulu dalam array `edits`.
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 16000,
          "messages": [
              {
                  "role": "user",
                  "content": "Search for the latest developments in quantum error correction and summarize the key breakthroughs."
              }
          ],
          "thinking": {"type": "adaptive"},
          "tools": [
              {
                  "type": "web_search_20250305",
                  "name": "web_search",
                  "max_uses": 5
              }
          ],
          "context_management": {
              "edits": [
                  {
                      "type": "clear_thinking_20251015",
                      "keep": {
                          "type": "thinking_turns",
                          "value": 2
                      }
                  },
                  {
                      "type": "clear_tool_uses_20250919",
                      "trigger": {
                          "type": "input_tokens",
                          "value": 50000
                      },
                      "keep": {
                          "type": "tool_uses",
                          "value": 5
                      }
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 16000
  messages:
    - role: user
      content: Search for the latest developments in quantum error correction and summarize the key breakthroughs.
  thinking:
    type: adaptive
  tools:
    - type: web_search_20250305
      name: web_search
      max_uses: 5
  context_management:
    edits:
      - type: clear_thinking_20251015
        keep:
          type: thinking_turns
          value: 2
      - type: clear_tool_uses_20250919
        trigger:
          type: input_tokens
          value: 50000
        keep:
          type: tool_uses
          value: 5
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      messages=[
          {
              "role": "user",
              "content": "Search for the latest developments in quantum error correction and summarize the key breakthroughs.",
          }
      ],
      thinking={"type": "adaptive"},
      tools=[
          {
              "type": "web_search_20250305",
              "name": "web_search",
              "max_uses": 5,
          }
      ],
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_thinking_20251015",
                  "keep": {"type": "thinking_turns", "value": 2},
              },
              {
                  "type": "clear_tool_uses_20250919",
                  "trigger": {"type": "input_tokens", "value": 50000},
                  "keep": {"type": "tool_uses", "value": 5},
              },
          ]
      },
  )

  print(response)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [
      {
        role: "user",
        content:
          "Search for the latest developments in quantum error correction and summarize the key breakthroughs."
      }
    ],
    thinking: { type: "adaptive" },
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 5
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 2
          }
        },
        {
          type: "clear_tool_uses_20250919",
          trigger: {
            type: "input_tokens",
            value: 50000
          },
          keep: {
            type: "tool_uses",
            value: 5
          }
        }
      ]
    }
  });

  console.log(response);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Messages = [
          new() { Role = Role.User, Content = "Search for the latest developments in quantum error correction and summarize the key breakthroughs." }
      ],
      Thinking = new BetaThinkingConfigAdaptive(),
      Tools = [
          new BetaWebSearchTool20250305 { MaxUses = 5 }
      ],
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearThinking20251015Edit
              {
                  Keep = new BetaThinkingTurns(2)
              },
              new BetaClearToolUses20250919Edit
              {
                  Trigger = new BetaInputTokensTrigger(50000),
                  Keep = new BetaToolUsesKeep(5)
              }
          ]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Search for the latest developments in quantum error correction and summarize the key breakthroughs.")),
  	},
  	Thinking: anthropic.BetaThinkingConfigParamUnion{OfAdaptive: &anthropic.BetaThinkingConfigAdaptiveParam{}},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfWebSearchTool20250305: &anthropic.BetaWebSearchTool20250305Param{
  			MaxUses: anthropic.Int(5),
  		}},
  	},
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaContextManagement2025_06_27,
  	},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearThinking20251015: &anthropic.BetaClearThinking20251015EditParam{
  				Keep: anthropic.BetaClearThinking20251015EditKeepUnionParam{
  					OfThinkingTurns: &anthropic.BetaThinkingTurnsParam{
  						Value: 2,
  					},
  				},
  			}},
  			{OfClearToolUses20250919: &anthropic.BetaClearToolUses20250919EditParam{
  				Trigger: anthropic.BetaClearToolUses20250919EditTriggerUnionParam{
  					OfInputTokens: &anthropic.BetaInputTokensTriggerParam{
  						Value: 50000,
  					},
  				},
  				Keep: anthropic.BetaToolUsesKeepParam{
  					Value: 5,
  				},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaThinkingConfigAdaptive;
  import com.anthropic.models.beta.messages.BetaWebSearchTool20250305;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearThinking20251015Edit;
  import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
  import com.anthropic.models.beta.messages.BetaThinkingTurns;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  import com.anthropic.models.beta.messages.BetaToolUsesKeep;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .addUserMessage("Search for the latest developments in quantum error correction and summarize the key breakthroughs.")
          .thinking(BetaThinkingConfigAdaptive.builder().build())
          .addTool(BetaWebSearchTool20250305.builder()
              .maxUses(5L)
              .build())
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearThinking20251015Edit.builder()
                  .keep(BetaThinkingTurns.builder()
                      .value(2L)
                      .build())
                  .build())
              .addEdit(BetaClearToolUses20250919Edit.builder()
                  .trigger(BetaInputTokensTrigger.builder()
                      .value(50000L)
                      .build())
                  .keep(BetaToolUsesKeep.builder()
                      .value(5L)
                      .build())
                  .build())
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 16000,
      messages: [
          [
              'role' => 'user',
              'content' => 'Search for the latest developments in quantum error correction and summarize the key breakthroughs.'
          ]
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      thinking: ['type' => 'adaptive'],
      tools: [
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 5
          ]
      ],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_thinking_20251015',
                  'keep' => [
                      'type' => 'thinking_turns',
                      'value' => 2
                  ]
              ],
              [
                  'type' => 'clear_tool_uses_20250919',
                  'trigger' => [
                      'type' => 'input_tokens',
                      'value' => 50000
                  ],
                  'keep' => [
                      'type' => 'tool_uses',
                      'value' => 5
                  ]
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [
      {
        role: "user",
        content: "Search for the latest developments in quantum error correction and summarize the key breakthroughs."
      }
    ],
    thinking: { type: "adaptive" },
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 5
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_thinking_20251015",
          keep: {
            type: "thinking_turns",
            value: 2
          }
        },
        {
          type: "clear_tool_uses_20250919",
          trigger: {
            type: "input_tokens",
            value: 50000
          },
          keep: {
            type: "tool_uses",
            value: 5
          }
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

## Opsi konfigurasi untuk penghapusan hasil alat

| Opsi konfigurasi    | Default             | Deskripsi                                                                                                                                                                                                                                                               |
| ------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trigger`           | 100.000 token input | Menentukan kapan strategi pengeditan konteks diaktifkan. Setelah prompt melebihi ambang batas ini, penghapusan akan dimulai. Anda dapat menentukan nilai ini dalam `input_tokens` atau `tool_uses`.                                                                     |
| `keep`              | 3 tool use          | Menentukan berapa banyak pasangan tool use/hasil terbaru yang akan disimpan setelah penghapusan terjadi. API menghapus interaksi alat tertua terlebih dahulu, mempertahankan yang terbaru.                                                                              |
| `clear_at_least`    | Tidak ada           | Memastikan jumlah minimum token dihapus setiap kali strategi diaktifkan. Jika API tidak dapat menghapus setidaknya jumlah yang ditentukan, strategi tidak akan diterapkan. Ini membantu menentukan apakah penghapusan konteks sepadan dengan merusak cache prompt Anda. |
| `exclude_tools`     | Tidak ada           | Daftar nama alat yang tool use dan hasilnya tidak boleh dihapus. Berguna untuk mempertahankan konteks penting.                                                                                                                                                          |
| `clear_tool_inputs` | `false`             | Mengontrol apakah parameter panggilan alat dihapus bersama dengan hasil alat. Secara default, hanya hasil alat yang dihapus sementara panggilan alat asli Claude tetap terlihat.                                                                                        |

## Respons pengeditan konteks

Anda dapat melihat pengeditan konteks mana yang diterapkan pada permintaan Anda menggunakan bidang respons `context_management`, bersama dengan statistik yang berguna tentang konten dan token input yang dihapus.

```json Output
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    // ...
  ],
  "usage": {
    // ...
  },
  "context_management": {
    "applied_edits": [
      // When using `clear_thinking_20251015`
      {
        "type": "clear_thinking_20251015",
        "cleared_thinking_turns": 3,
        "cleared_input_tokens": 15000
      },
      // When using `clear_tool_uses_20250919`
      {
        "type": "clear_tool_uses_20250919",
        "cleared_tool_uses": 8,
        "cleared_input_tokens": 50000
      }
    ]
  }
}
```

Untuk respons streaming, pengeditan konteks disertakan dalam event `message_delta` terakhir:

```json Streaming Response
{
  "type": "message_delta",
  "delta": {
    "stop_reason": "end_turn",
    "stop_sequence": null
  },
  "usage": {
    "output_tokens": 1024
  },
  "context_management": {
    "applied_edits": [
      // ...
    ]
  }
}
```

## Penghitungan token

Endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) mendukung manajemen konteks, memungkinkan Anda untuk melihat pratinjau berapa banyak token yang akan digunakan prompt Anda setelah pengeditan konteks diterapkan.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "messages": [
              {
                  "role": "user",
                  "content": "Continue our conversation..."
              }
          ],
          "context_management": {
              "edits": [
                  {
                      "type": "clear_tool_uses_20250919",
                      "trigger": {
                          "type": "input_tokens",
                          "value": 30000
                      },
                      "keep": {
                          "type": "tool_uses",
                          "value": 5
                      }
                  }
              ]
          }
      }'
  ```

  ```bash CLI
  cat > request.yaml <<'YAML'
  model: claude-opus-4-8
  messages:
    - role: user
      content: Continue our conversation...
  context_management:
    edits:
      - type: clear_tool_uses_20250919
        trigger:
          type: input_tokens
          value: 30000
        keep:
          type: tool_uses
          value: 5
  YAML

  ORIGINAL=$(ant beta:messages count-tokens \
    --beta context-management-2025-06-27 \
    --transform context_management.original_input_tokens \
    --raw-output < request.yaml)

  INPUT_TOKENS=$(ant beta:messages count-tokens \
    --beta context-management-2025-06-27 \
    --transform input_tokens --raw-output < request.yaml)

  printf 'Original tokens: %s\n' "$ORIGINAL"
  printf 'After clearing: %s\n' "$INPUT_TOKENS"
  printf 'Savings: %s tokens\n' "$((ORIGINAL - INPUT_TOKENS))"
  ```

  ```python Python
  response = client.beta.messages.count_tokens(
      model="claude-opus-4-8",
      messages=[{"role": "user", "content": "Continue our conversation..."}],
      betas=["context-management-2025-06-27"],
      context_management={
          "edits": [
              {
                  "type": "clear_tool_uses_20250919",
                  "trigger": {"type": "input_tokens", "value": 30000},
                  "keep": {"type": "tool_uses", "value": 5},
              }
          ]
      },
  )

  print(f"Original tokens: {response.context_management.original_input_tokens}")
  print(f"After clearing: {response.input_tokens}")
  print(
      f"Savings: {response.context_management.original_input_tokens - response.input_tokens} tokens"
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.countTokens({
    model: "claude-opus-4-8",
    messages: [
      {
        role: "user",
        content: "Continue our conversation..."
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_tool_uses_20250919",
          trigger: {
            type: "input_tokens",
            value: 30000
          },
          keep: {
            type: "tool_uses",
            value: 5
          }
        }
      ]
    }
  });

  console.log(`Original tokens: ${response.context_management?.original_input_tokens}`);
  console.log(`After clearing: ${response.input_tokens}`);
  console.log(
    `Savings: ${
      (response.context_management?.original_input_tokens || 0) - response.input_tokens
    } tokens`
  );
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCountTokensParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      Messages = [new() { Role = Role.User, Content = "Continue our conversation..." }],
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [
              new BetaClearToolUses20250919Edit
              {
                  Trigger = new BetaInputTokensTrigger(30000),
                  Keep = new BetaToolUsesKeep(5)
              }
          ]
      }
  };

  var response = await client.Beta.Messages.CountTokens(parameters);

  Console.WriteLine($"Original tokens: {response.ContextManagement?.OriginalInputTokens}");
  Console.WriteLine($"After clearing: {response.InputTokens}");
  Console.WriteLine($"Savings: {(response.ContextManagement?.OriginalInputTokens ?? 0) - response.InputTokens} tokens");
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.CountTokens(context.TODO(), anthropic.BetaMessageCountTokensParams{
  	Model: anthropic.ModelClaudeOpus4_8,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Continue our conversation...")),
  	},
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaContextManagement2025_06_27,
  	},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearToolUses20250919: &anthropic.BetaClearToolUses20250919EditParam{
  				Trigger: anthropic.BetaClearToolUses20250919EditTriggerUnionParam{
  					OfInputTokens: &anthropic.BetaInputTokensTriggerParam{
  						Value: 30000,
  					},
  				},
  				Keep: anthropic.BetaToolUsesKeepParam{
  					Value: 5,
  				},
  			}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Original tokens: %d\n", response.ContextManagement.OriginalInputTokens)
  fmt.Printf("After clearing: %d\n", response.InputTokens)
  fmt.Printf("Savings: %d tokens\n", response.ContextManagement.OriginalInputTokens-response.InputTokens)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMessageTokensCount;
  import com.anthropic.models.beta.messages.MessageCountTokensParams;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  import com.anthropic.models.beta.messages.BetaToolUsesKeep;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCountTokensParams params = MessageCountTokensParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .addUserMessage("Continue our conversation...")
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearToolUses20250919Edit.builder()
                  .trigger(BetaInputTokensTrigger.builder()
                      .value(30000L)
                      .build())
                  .keep(BetaToolUsesKeep.builder()
                      .value(5L)
                      .build())
                  .build())
              .build())
          .build();

      BetaMessageTokensCount response = client.beta().messages().countTokens(params);

      IO.println("Original tokens: " + response.contextManagement().get().originalInputTokens());
      IO.println("After clearing: " + response.inputTokens());
      IO.println("Savings: " + (response.contextManagement().get().originalInputTokens() - response.inputTokens()) + " tokens");
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->countTokens(
      messages: [
          ['role' => 'user', 'content' => 'Continue our conversation...']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'clear_tool_uses_20250919',
                  'trigger' => [
                      'type' => 'input_tokens',
                      'value' => 30000
                  ],
                  'keep' => [
                      'type' => 'tool_uses',
                      'value' => 5
                  ]
              ]
          ]
      ],
  );

  echo "Original tokens: " . $response->contextManagement->originalInputTokens . "\n";
  echo "After clearing: " . $response->inputTokens . "\n";
  echo "Savings: " . ($response->contextManagement->originalInputTokens - $response->inputTokens) . " tokens\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.count_tokens(
    model: "claude-opus-4-8",
    messages: [
      { role: "user", content: "Continue our conversation..." }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        {
          type: "clear_tool_uses_20250919",
          trigger: {
            type: "input_tokens",
            value: 30000
          },
          keep: {
            type: "tool_uses",
            value: 5
          }
        }
      ]
    }
  )

  puts "Original tokens: #{response.context_management.original_input_tokens}"
  puts "After clearing: #{response.input_tokens}"
  puts "Savings: #{response.context_management.original_input_tokens - response.input_tokens} tokens"
  ```
</CodeGroup>

```json Output
{
  "input_tokens": 25000,
  "context_management": {
    "original_input_tokens": 70000
  }
}
```

Respons menunjukkan baik jumlah token akhir setelah manajemen konteks diterapkan (`input_tokens`) maupun jumlah token asli sebelum penghapusan apa pun terjadi (`original_input_tokens`).

## Menggunakan dengan alat memori

Pengeditan konteks dapat dikombinasikan dengan [alat memori](/docs/id/agents-and-tools/tool-use/memory-tool). Ketika konteks percakapan Anda mendekati ambang batas penghapusan yang dikonfigurasi, Claude menerima peringatan otomatis untuk mempertahankan informasi penting. Ini memungkinkan Claude untuk menyimpan hasil alat atau konteks ke file memorinya sebelum dihapus dari riwayat percakapan.

Kombinasi ini memungkinkan Anda untuk:

* **Mempertahankan konteks penting:** Claude dapat menulis informasi penting dari hasil alat ke file memori sebelum hasil tersebut dihapus
* **Mempertahankan alur kerja yang berjalan lama:** Memungkinkan alur kerja agentik yang jika tidak akan melebihi batas konteks dengan memindahkan informasi ke penyimpanan persisten
* **Mengakses informasi sesuai permintaan:** Claude dapat mencari informasi yang sebelumnya dihapus dari file memori saat diperlukan, daripada menyimpan semuanya di jendela konteks aktif

Misalnya, dalam alur kerja pengeditan file di mana Claude melakukan banyak operasi, Claude dapat merangkum perubahan yang telah selesai ke file memori seiring pertumbuhan konteks. Ketika hasil alat dihapus, Claude tetap memiliki akses ke informasi tersebut melalui sistem memorinya dan dapat terus bekerja secara efektif.

Untuk menggunakan kedua fitur bersama-sama, aktifkan keduanya dalam permintaan API Anda:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --header "anthropic-beta: context-management-2025-06-27" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Hello"
              }
          ],
          "tools": [
              {
                  "type": "memory_20250818",
                  "name": "memory"
              }
          ],
          "context_management": {
              "edits": [
                  {"type": "clear_tool_uses_20250919"}
              ]
          }
      }'
  ```

  ```bash CLI
  ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello
  tools:
    - type: memory_20250818
      name: memory
  context_management:
    edits:
      - type: clear_tool_uses_20250919
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[{"role": "user", "content": "Hello"}],
      tools=[{"type": "memory_20250818", "name": "memory"}],
      betas=["context-management-2025-06-27"],
      context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
  )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [{ role: "user", content: "Hello" }],
    tools: [
      {
        type: "memory_20250818",
        name: "memory"
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [{ type: "clear_tool_uses_20250919" }]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [
          new() { Role = Role.User, Content = "Hello" }
      ],
      Tools = [
          new BetaMemoryTool20250818()
      ],
      Betas = [AnthropicBeta.ContextManagement2025_06_27],
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaClearToolUses20250919Edit()]
      }
  };

  var response = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfMemoryTool20250818: &anthropic.BetaMemoryTool20250818Param{}},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfClearToolUses20250919: &anthropic.BetaClearToolUses20250919EditParam{}},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMemoryTool20250818;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
  import com.anthropic.models.beta.AnthropicBeta;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addUserMessage("Hello")
          .addTool(BetaMemoryTool20250818.builder().build())
          .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
          .contextManagement(BetaContextManagementConfig.builder()
              .addEdit(BetaClearToolUses20250919Edit.builder().build())
              .build())
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Hello']
      ],
      model: 'claude-opus-4-8',
      betas: ['context-management-2025-06-27'],
      tools: [
          [
              'type' => 'memory_20250818',
              'name' => 'memory'
          ]
      ],
      contextManagement: [
          'edits' => [
              ['type' => 'clear_tool_uses_20250919']
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [{ role: "user", content: "Hello" }],
    tools: [
      {
        type: "memory_20250818",
        name: "memory"
      }
    ],
    betas: ["context-management-2025-06-27"],
    context_management: {
      edits: [
        { type: "clear_tool_uses_20250919" }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

Untuk referensi lengkap alat memori termasuk perintah dan contoh, lihat [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool).

## Compaction sisi klien (SDK)

<Warning>
  **Anthropic merekomendasikan compaction sisi server daripada compaction SDK.** [Compaction sisi server](/docs/id/build-with-claude/compaction) menangani manajemen konteks secara otomatis dengan kompleksitas integrasi yang lebih rendah, perhitungan penggunaan token yang lebih baik, dan tanpa keterbatasan sisi klien. Gunakan compaction SDK hanya jika Anda secara khusus memerlukan kontrol sisi klien atas proses peringkasan.

  Parameter `compaction_control` sudah usang di SDK Python, TypeScript, dan Ruby dan akan dihapus di versi mendatang. SDK mengeluarkan peringatan penghentian ketika parameter ini diaktifkan. Untuk menggunakan compaction sisi server dengan tool runner, teruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
</Warning>

<Note>
  Compaction tersedia di [SDK Python, TypeScript, dan Ruby](/docs/id/cli-sdks-libraries/overview) saat menggunakan [metode `tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner).
</Note>

Compaction adalah fitur SDK yang secara otomatis mengelola konteks percakapan dengan menghasilkan ringkasan ketika penggunaan token tumbuh terlalu besar. Tidak seperti strategi pengeditan konteks sisi server yang menghapus konten, compaction menginstruksikan Claude untuk merangkum riwayat percakapan, lalu menggantikan riwayat lengkap dengan ringkasan tersebut. Ini memungkinkan Claude untuk terus mengerjakan tugas yang berjalan lama yang jika tidak akan melebihi [jendela konteks](/docs/id/build-with-claude/context-windows).

### Cara kerja compaction

Ketika compaction diaktifkan, SDK memantau penggunaan token setelah setiap respons model:

1. **Pemeriksaan ambang batas:** SDK menghitung total token sebagai `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`.
2. **Pembuatan ringkasan:** Ketika ambang batas terlampaui, prompt ringkasan disisipkan sebagai giliran pengguna, dan Claude menghasilkan ringkasan terstruktur yang dibungkus dalam tag `<summary></summary>`.
3. **Penggantian konteks:** SDK mengekstrak ringkasan dan menggantikan seluruh riwayat pesan dengannya.
4. **Kelanjutan:** Percakapan dilanjutkan dari ringkasan, dengan Claude melanjutkan dari titik terakhirnya.

### Menggunakan compaction

Tambahkan `compaction_control` ke panggilan `tool_runner` Anda untuk mengaktifkan peringkasan otomatis ketika penggunaan token melebihi ambang batas.

<Tabs>
  <Tab title="cURL">
    <Note>
      Compaction berjalan di sisi klien dalam helper `tool_runner` SDK, sehingga tidak memiliki padanan HTTP langsung. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic.
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI tidak menyertakan helper `tool_runner`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python Python
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[read_file],
        messages=[{"role": "user", "content": "What's in config.json?"}],
        compaction_control={"enabled": True, "context_token_threshold": 100000},
    )

    for message in runner:
        print(f"Tokens used: {message.usage.input_tokens}")
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript TypeScript
    const client = new Anthropic();

    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [readFile],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compactionControl: { enabled: true, contextTokenThreshold: 100000 }
    });

    for await (const message of runner) {
      console.log(`Tokens used: ${message.usage.input_tokens}`);
    }
    ```
  </Tab>

  <Tab title="C#">
    <Note>
      SDK C# menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Go">
    <Note>
      SDK Go menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Java">
    <Note>
      SDK Java menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="PHP">
    <Note>
      SDK PHP menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Ruby">
    ```ruby Ruby
    client = Anthropic::Client.new

    runner = client.beta.messages.tool_runner(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [ReadFile.new],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compaction_control: { enabled: true, context_token_threshold: 100000 }
    )

    runner.each_message do |message|
      puts "Tokens used: #{message.usage.input_tokens}"
    end
    ```
  </Tab>
</Tabs>

#### Apa yang terjadi selama compaction

Seiring pertumbuhan percakapan, riwayat pesan terakumulasi:

**Sebelum compaction (mendekati 100k token):**

```json
[
  { "role": "user", "content": "Analyze all files and write a report..." },
  { "role": "assistant", "content": "I'll help. Let me start by reading..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "Based on file1.txt, I see..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "After analyzing file2.txt..." }
  // ... 50 more exchanges like this ...
]
```

Ketika token melebihi ambang batas, SDK menyisipkan permintaan ringkasan dan Claude menghasilkan ringkasan. Seluruh riwayat kemudian digantikan:

**Setelah compaction (kembali ke \~2–3k token):**

```json
[
  {
    "role": "assistant",
    "content": "# Task Overview\nThe user requested analysis of directory files to produce a summary report...\n\n# Current State\nAnalyzed 52 files across 3 subdirectories. Key findings documented in report.md...\n\n# Important Discoveries\n- Configuration files use YAML format\n- Found 3 deprecated dependencies\n- Test coverage at 67%\n\n# Next Steps\n1. Analyze remaining files in /src/legacy\n2. Complete final report sections...\n\n# Context to Preserve\nUser prefers markdown format with executive summary first..."
  }
]
```

Claude terus bekerja dari ringkasan ini seolah-olah itu adalah riwayat percakapan asli.

### Opsi konfigurasi

| Parameter                 | Tipe    | Wajib | Default                                                   | Deskripsi                                         |
| ------------------------- | ------- | ----- | --------------------------------------------------------- | ------------------------------------------------- |
| `enabled`                 | boolean | Ya    | -                                                         | Apakah mengaktifkan compaction otomatis           |
| `context_token_threshold` | number  | Tidak | 100.000                                                   | Jumlah token di mana compaction dipicu            |
| `model`                   | string  | Tidak | Sama dengan model utama                                   | Model yang digunakan untuk menghasilkan ringkasan |
| `summary_prompt`          | string  | Tidak | Lihat [Prompt ringkasan default](#default-summary-prompt) | Prompt kustom untuk pembuatan ringkasan           |

#### Memilih ambang batas token

Ambang batas menentukan kapan compaction terjadi. Ambang batas yang lebih rendah berarti compaction yang lebih sering dengan jendela konteks yang lebih kecil. Ambang batas yang lebih tinggi memungkinkan lebih banyak konteks tetapi berisiko mencapai batas.

<Tabs>
  <Tab title="cURL">
    <Note>
      Compaction berjalan di sisi klien dalam helper `tool_runner` SDK, sehingga tidak memiliki padanan HTTP langsung. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic.
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI tidak menyertakan helper `tool_runner`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python Python
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[read_file],
        messages=[{"role": "user", "content": "What's in config.json?"}],
        # Nilai yang lebih rendah melakukan pemadatan lebih sering; naikkan ke 150000 jika tugas membutuhkan lebih banyak konteks
        compaction_control={"enabled": True, "context_token_threshold": 50000},
    )

    for message in runner:
        print(f"Tokens used: {message.usage.input_tokens}")
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript TypeScript
    const client = new Anthropic();

    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [readFile],
      messages: [{ role: "user", content: "What's in config.json?" }],
      // Nilai yang lebih rendah memadatkan lebih sering; naikkan ke 150000 jika tugas membutuhkan lebih banyak konteks
      compactionControl: { enabled: true, contextTokenThreshold: 50000 }
    });

    for await (const message of runner) {
      console.log(`Tokens used: ${message.usage.input_tokens}`);
    }
    ```
  </Tab>

  <Tab title="C#">
    <Note>
      SDK C# menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Go">
    <Note>
      SDK Go menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Java">
    <Note>
      SDK Java menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="PHP">
    <Note>
      SDK PHP menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Ruby">
    ```ruby Ruby
    client = Anthropic::Client.new

    runner = client.beta.messages.tool_runner(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [ReadFile.new],
      messages: [{ role: "user", content: "What's in config.json?" }],
      # Nilai yang lebih rendah melakukan pemadatan lebih sering; naikkan ke 150000 jika tugas membutuhkan lebih banyak konteks
      compaction_control: { enabled: true, context_token_threshold: 50000 }
    )

    runner.each_message do |message|
      puts "Tokens used: #{message.usage.input_tokens}"
    end
    ```
  </Tab>
</Tabs>

#### Menggunakan model yang berbeda untuk ringkasan

Anda dapat menggunakan model yang lebih cepat atau lebih murah untuk menghasilkan ringkasan:

<Tabs>
  <Tab title="cURL">
    <Note>
      Compaction berjalan di sisi klien dalam helper `tool_runner` SDK, sehingga tidak memiliki padanan HTTP langsung. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic.
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI tidak menyertakan helper `tool_runner`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python Python
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[read_file],
        messages=[{"role": "user", "content": "What's in config.json?"}],
        compaction_control={
            "enabled": True,
            "context_token_threshold": 100000,
            "model": "claude-haiku-4-5",
        },
    )

    for message in runner:
        print(f"Tokens used: {message.usage.input_tokens}")
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript TypeScript
    const client = new Anthropic();

    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [readFile],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compactionControl: {
        enabled: true,
        contextTokenThreshold: 100000,
        model: "claude-haiku-4-5"
      }
    });

    for await (const message of runner) {
      console.log(`Tokens used: ${message.usage.input_tokens}`);
    }
    ```
  </Tab>

  <Tab title="C#">
    <Note>
      SDK C# menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Go">
    <Note>
      SDK Go menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Java">
    <Note>
      SDK Java menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="PHP">
    <Note>
      SDK PHP menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Ruby">
    ```ruby Ruby
    client = Anthropic::Client.new

    runner = client.beta.messages.tool_runner(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [ReadFile.new],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compaction_control: {
        enabled: true,
        context_token_threshold: 100000,
        model: "claude-haiku-4-5"
      }
    )

    runner.each_message do |message|
      puts "Tokens used: #{message.usage.input_tokens}"
    end
    ```
  </Tab>
</Tabs>

#### Prompt ringkasan kustom

Anda dapat memberikan prompt kustom untuk kebutuhan spesifik domain. Prompt Anda harus menginstruksikan Claude untuk membungkus ringkasannya dalam tag `<summary></summary>`.

<Tabs>
  <Tab title="cURL">
    <Note>
      Compaction berjalan di sisi klien dalam helper `tool_runner` SDK, sehingga tidak memiliki padanan HTTP langsung. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic.
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI tidak menyertakan helper `tool_runner`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python Python
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[read_file],
        messages=[{"role": "user", "content": "What's in config.json?"}],
        compaction_control={
            "enabled": True,
            "context_token_threshold": 100000,
            "summary_prompt": """Summarize the research conducted so far, including:
    - Sources consulted and key findings
    - Questions answered and remaining unknowns
    - Recommended next steps

    Wrap your summary in <summary></summary> tags.""",
        },
    )

    for message in runner:
        print(f"Tokens used: {message.usage.input_tokens}")
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript TypeScript
    const client = new Anthropic();

    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [readFile],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compactionControl: {
        enabled: true,
        contextTokenThreshold: 100000,
        summaryPrompt: `Summarize the research conducted so far, including:
    - Sources consulted and key findings
    - Questions answered and remaining unknowns
    - Recommended next steps

    Wrap your summary in <summary></summary> tags.`
      }
    });

    for await (const message of runner) {
      console.log(`Tokens used: ${message.usage.input_tokens}`);
    }
    ```
  </Tab>

  <Tab title="C#">
    <Note>
      SDK C# menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Go">
    <Note>
      SDK Go menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Java">
    <Note>
      SDK Java menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="PHP">
    <Note>
      SDK PHP menyertakan tool runner, tetapi tidak mendukung `compaction_control` sisi klien. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya: ini bekerja dengan tool runner dengan meneruskan edit `compact_20260112` dalam parameter `context_management` permintaan.
    </Note>
  </Tab>

  <Tab title="Ruby">
    ```ruby Ruby
    client = Anthropic::Client.new

    runner = client.beta.messages.tool_runner(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [ReadFile.new],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compaction_control: {
        enabled: true,
        context_token_threshold: 100000,
        summary_prompt: <<~PROMPT
          Summarize the research conducted so far, including:
          - Sources consulted and key findings
          - Questions answered and remaining unknowns
          - Recommended next steps

          Wrap your summary in <summary></summary> tags.
        PROMPT
      }
    )

    runner.each_message do |message|
      puts "Tokens used: #{message.usage.input_tokens}"
    end
    ```
  </Tab>
</Tabs>

### Prompt ringkasan default

Prompt ringkasan bawaan menginstruksikan Claude untuk membuat ringkasan kelanjutan terstruktur yang mencakup:

1. **Ikhtisar Tugas:** Permintaan inti pengguna, kriteria keberhasilan, dan batasan.
2. **Status Saat Ini:** Apa yang telah diselesaikan, file yang dimodifikasi, dan artefak yang dihasilkan.
3. **Penemuan Penting:** Batasan teknis, keputusan yang dibuat, kesalahan yang diselesaikan, dan pendekatan yang gagal.
4. **Langkah Selanjutnya:** Tindakan spesifik yang diperlukan, penghambat, dan urutan prioritas.
5. **Konteks yang Harus Dipertahankan:** Preferensi pengguna, detail spesifik domain, dan komitmen yang dibuat.

Struktur ini memungkinkan Claude untuk melanjutkan pekerjaan secara efisien tanpa kehilangan konteks penting atau mengulangi kesalahan.

<Accordion title="Lihat prompt default lengkap">
  ```text wrap
  You have been working on the task described above but have not yet completed it. Write a continuation summary that will allow you (or another instance of yourself) to resume work efficiently in a future context window where the conversation history will be replaced with this summary. Your summary should be structured, concise, and actionable. Include:

  1. Task Overview
  The user's core request and success criteria
  Any clarifications or constraints they specified

  2. Current State
  What has been completed so far
  Files created, modified, or analyzed (with paths if relevant)
  Key outputs or artifacts produced

  3. Important Discoveries
  Technical constraints or requirements uncovered
  Decisions made and their rationale
  Errors encountered and how they were resolved
  What approaches were tried that didn't work (and why)

  4. Next Steps
  Specific actions needed to complete the task
  Any blockers or open questions to resolve
  Priority order if multiple steps remain

  5. Context to Preserve
  User preferences or style requirements
  Domain-specific details that aren't obvious
  Any promises made to the user

  Be concise but complete—err on the side of including information that would prevent duplicate work or repeated mistakes. Write in a way that enables immediate resumption of the task.

  Wrap your summary in <summary></summary> tags.
  ```
</Accordion>

### Keterbatasan

#### Alat sisi server

<Warning>
  Compaction memerlukan pertimbangan khusus saat menggunakan alat sisi server seperti [pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool).
</Warning>

Saat menggunakan alat sisi server, SDK mungkin salah menghitung penggunaan token, menyebabkan compaction dipicu pada waktu yang salah.

Misalnya, setelah operasi pencarian web, respons API mungkin menunjukkan:

```json Output
{
  "usage": {
    "input_tokens": 63000,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 270000,
    "output_tokens": 1400
  }
}
```

SDK menghitung total penggunaan sebagai 63.000 + 0 + 270.000 + 1.400 = 334.400 token. Namun, nilai `cache_read_input_tokens` mencakup pembacaan terakumulasi dari beberapa panggilan API internal yang dibuat oleh alat sisi server, bukan konteks percakapan Anda yang sebenarnya. Panjang konteks Anda yang sebenarnya mungkin hanya 63.000 `input_tokens`, tetapi SDK melihat 334k dan memicu compaction secara prematur.

**Solusi alternatif:**

* Gunakan endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan panjang konteks yang akurat
* Hindari compaction saat menggunakan alat sisi server secara ekstensif

#### Kasus khusus penggunaan alat

Ketika SDK memicu compaction saat respons tool use masih tertunda, SDK menghapus blok tool use dari riwayat pesan sebelum menghasilkan ringkasan. Claude akan mengeluarkan kembali panggilan alat setelah melanjutkan dari ringkasan jika masih diperlukan.

### Memantau compaction

Memahami kapan compaction dipicu membantu Anda menyetel ambang batas dan memverifikasi perilaku yang diharapkan.

<Tabs>
  <Tab title="cURL">
    <Note>
      Compaction berjalan di sisi klien dalam helper `tool_runner` SDK, sehingga tidak memiliki padanan HTTP langsung. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic.
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      CLI tidak menyertakan helper `tool_runner`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
    </Note>
  </Tab>

  <Tab title="Python">
    SDK Python mencatat event compaction pada level INFO. Aktifkan logger `anthropic.lib.tools`:

    ```python Python
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("anthropic.lib.tools").setLevel(logging.INFO)

    # Log akan menampilkan:
    # INFO: Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
    # INFO: Compaction complete. New token usage: 2500
    ```
  </Tab>

  <Tab title="TypeScript">
    `toolRunner` SDK TypeScript mendukung compaction tetapi tidak mencatat event. Deteksi compaction dengan mengamati `runner.params.messages.length` yang menyusut di antara giliran:

    ```typescript TypeScript
    let prevMsgCount = 0;
    for await (const message of runner) {
      const currMsgCount = runner.params.messages.length;
      if (currMsgCount < prevMsgCount) {
        console.log(`Compaction occurred: ${prevMsgCount} -> ${currMsgCount} messages`);
        console.log(`Input tokens after compaction: ${message.usage.input_tokens}`);
      }
      prevMsgCount = currMsgCount;
    }
    ```
  </Tab>

  <Tab title="C#">
    <Note>
      Tool runner SDK C# tidak mendukung `compaction_control`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Go">
    <Note>
      Tool runner SDK Go tidak mendukung `compaction_control`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Java">
    <Note>
      Tool runner SDK Java tidak mendukung `compaction_control`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="PHP">
    <Note>
      Tool runner SDK PHP tidak mendukung `compaction_control`. Gunakan [compaction sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
    </Note>
  </Tab>

  <Tab title="Ruby">
    SDK Ruby mendukung callback `on_compact:` yang dipicu ketika compaction terjadi. Tambahkan ke konfigurasi `compaction_control` Anda:

    ```ruby Ruby
    client = Anthropic::Client.new

    runner = client.beta.messages.tool_runner(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [ReadFile.new],
      messages: [{ role: "user", content: "What's in config.json?" }],
      compaction_control: {
        enabled: true,
        context_token_threshold: 100000,
        on_compact: ->(tokens_before, tokens_after) do
          puts "Compaction occurred: #{tokens_before} -> #{tokens_after} tokens"
        end
      }
    )

    runner.each_message do |message|
      puts "Tokens: #{message.usage.input_tokens}"
    end
    ```
  </Tab>
</Tabs>

### Kapan menggunakan compaction

**Kasus penggunaan yang baik:**

* Tugas agen yang berjalan lama yang memproses banyak file atau sumber data
* Alur kerja riset yang mengakumulasi sejumlah besar informasi
* Tugas multilangkah dengan kemajuan yang jelas dan terukur
* Tugas yang menghasilkan artefak (file, laporan) yang bertahan di luar percakapan

**Kasus penggunaan yang kurang ideal:**

* Tugas yang memerlukan pengingatan tepat atas detail percakapan awal
* Alur kerja yang menggunakan alat sisi server secara ekstensif
* Tugas yang perlu mempertahankan status yang tepat di banyak variabel

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Compaction" icon="arrows-clockwise" href="/docs/id/build-with-claude/compaction">
    Kelola percakapan panjang dengan compaction sisi server, strategi yang direkomendasikan untuk sebagian besar kasus penggunaan.
  </Card>

  <Card title="Caching prompt" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Kurangi biaya dan latensi dengan melakukan caching pada prefiks prompt, dan pelajari bagaimana pengeditan konteks berinteraksi dengan cache.
  </Card>
</CardGroup>
