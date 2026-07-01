---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/compaction
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: d5415fdcdb71727934586d1b90bf2cf64b5dcf453988388dfe0095610a7266f4
---

# Compaction

Pemadatan konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.

---

<Note>
  Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

<Tip>
  "Compaction" (pemadatan) sisi server adalah strategi yang direkomendasikan untuk mengelola konteks dalam percakapan yang berjalan lama dan alur kerja agentik. Fitur ini menangani manajemen konteks secara otomatis, tanpa kode peringkasan sisi klien.
</Tip>

Compaction memperpanjang panjang konteks efektif untuk percakapan dan tugas yang berjalan lama dengan secara otomatis meringkas konteks yang lebih lama ketika mendekati batas jendela konteks. Fitur ini juga menjaga konteks aktif tetap kecil: seiring percakapan bertambah panjang, kualitas respons menurun, sehingga compaction menggantikan konten yang lebih lama dengan ringkasan yang padat.

<Tip>
  Untuk pemahaman lebih dalam tentang mengapa konteks panjang mengalami penurunan kualitas dan bagaimana compaction membantu, lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Fitur ini ideal untuk:

* Percakapan multi-giliran berbasis chat di mana Anda ingin pengguna menggunakan satu chat untuk jangka waktu yang lama
* Prompt berorientasi tugas yang memerlukan banyak pekerjaan lanjutan (sering kali penggunaan alat) yang mungkin melebihi jendela konteks

<Note>
  Compaction masih dalam versi beta. Sertakan [beta header](/docs/id/api/beta-headers) `compact-2026-01-12` dalam permintaan API Anda untuk menggunakan fitur ini.
</Note>

## Model yang didukung

Compaction didukung pada model-model berikut:

* Claude Fable 5 (claude-fable-5)
* [Claude Mythos 5](https://anthropic.com/glasswing) (claude-mythos-5)
* [Claude Mythos Preview](https://anthropic.com/glasswing) (claude-mythos-preview)
* Claude Opus 4.8 (claude-opus-4-8)
* Claude Opus 4.7 (claude-opus-4-7)
* Claude Opus 4.6 (claude-opus-4-6)
* Claude Sonnet 5 (claude-sonnet-5)
* Claude Sonnet 4.6 (claude-sonnet-4-6)

## Cara kerja compaction

Ketika compaction diaktifkan, Claude secara otomatis meringkas percakapan Anda ketika mencapai ambang batas token yang dikonfigurasi. API akan:

1. Mendeteksi ketika token input mencapai ambang batas pemicu yang Anda tentukan.
2. Menghasilkan ringkasan dari percakapan saat ini.
3. Membuat blok `compaction` yang berisi ringkasan tersebut.
4. Melanjutkan respons dengan konteks yang telah dipadatkan.

Pada permintaan berikutnya, tambahkan respons ke pesan Anda. API secara otomatis menghapus semua blok konten sebelum blok `compaction`, melanjutkan percakapan dari ringkasan.

![Alur compaction: ketika token input mencapai pemicu, Claude menulis ringkasan ke dalam blok compaction dan melanjutkan](/docs/images/compaction-flow.svg)

## Penggunaan dasar

Aktifkan compaction dengan menambahkan strategi `compact_20260112` ke `context_management.edits` dalam permintaan Messages API Anda.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Help me build a website"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112"
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta compact-2026-01-12 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Help me build a website
  context_management:
    edits:
      - type: compact_20260112
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  messages = [{"role": "user", "content": "Help me build a website"}]

  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  )

  # Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
  messages.append({"role": "assistant", "content": response.content})
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Help me build a website" }
  ];

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112"
        }
      ]
    }
  });

  // Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
  messages.push({
    role: "assistant",
    content: response.content
  });
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var messages = new List<BetaMessageParam>
          {
              new() { Role = Role.User, Content = "Help me build a website" }
          };

          var parameters = new MessageCreateParams
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit()]
              }
          };

          var response = await client.Beta.Messages.Create(parameters);

          // Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
          messages.Add(new BetaMessageParam
          {
              Role = Role.Assistant,
              Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
          });

          Console.WriteLine(response);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  messages := []anthropic.BetaMessageParam{
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Help me build a website")),
  }

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages:  messages,
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
  messages = append(messages, response.ToParam())

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .addBeta("compact-2026-01-12")
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addUserMessage("Help me build a website")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder().build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);

          // Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
          // dengan menyertakannya dalam pesan permintaan berikutnya
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $messages = [
      ['role' => 'user', 'content' => 'Help me build a website']
  ];

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              ['type' => 'compact_20260112']
          ]
      ]
  );

  // Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
  $messages[] = ['role' => 'assistant', 'content' => $response->content];

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  messages = [
    { role: "user", content: "Help me build a website" }
  ]

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )

  # Tambahkan respons (termasuk blok pemadatan apa pun) untuk melanjutkan percakapan
  messages << { role: "assistant", content: response.content }

  puts response
  ```
</CodeGroup>

## Parameter

| Parameter                | Tipe    | Default                                     | Deskripsi                                                                                                                  |
| ------------------------ | ------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `type`                   | string  | Wajib                                       | Harus berupa `"compact_20260112"`                                                                                          |
| `trigger`                | object  | `{"type": "input_tokens", "value": 150000}` | Kapan compaction dipicu. `input_tokens` adalah satu-satunya tipe pemicu yang didukung. `value` harus minimal 50.000 token. |
| `pause_after_compaction` | boolean | `false`                                     | Apakah akan berhenti sejenak setelah menghasilkan ringkasan compaction                                                     |
| `instructions`           | string  | `null`                                      | Prompt peringkasan kustom. Sepenuhnya menggantikan prompt default jika disediakan.                                         |

### Konfigurasi pemicu

Konfigurasikan kapan compaction dipicu menggunakan parameter `trigger`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112",
            "trigger": {
              "type": "input_tokens",
              "value": 150000
            }
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta compact-2026-01-12 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
        trigger:
          type: input_tokens
          value: 150000
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={
          "edits": [
              {
                  "type": "compact_20260112",
                  "trigger": {"type": "input_tokens", "value": 150000},
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: {
            type: "input_tokens",
            value: 150000
          }
        }
      ]
    }
  });
  ```

  ```csharp C#
  AnthropicClient client = new();
  List<BetaMessageParam> messages = [new() { Role = Role.User, Content = "Hello" }];

  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 4096,
      Betas = ["compact-2026-01-12"],
      Messages = messages,
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaCompact20260112Edit
          {
              Trigger = new BetaInputTokensTrigger(150000)
          }]
      }
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()
  messages := []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))}

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages:  messages,
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  				Trigger: anthropic.BetaInputTokensTriggerParam{Value: 150000},
  			}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addBeta("compact-2026-01-12")
              .addUserMessage("Hello, Claude")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .trigger(BetaInputTokensTrigger.builder()
                          .value(150000L)
                          .build())
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'compact_20260112',
                  'trigger' => [
                      'type' => 'input_tokens',
                      'value' => 150000
                  ]
              ]
          ]
      ]
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = [{ role: "user", content: "Hello, Claude" }]

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: {
            type: "input_tokens",
            value: 150000
          }
        }
      ]
    }
  )
  puts response
  ```
</CodeGroup>

### Instruksi peringkasan kustom

Prompt peringkasan default bervariasi menurut model. Setiap default menginstruksikan Claude untuk menulis ringkasan di dalam tag `<summary></summary>` dengan informasi yang diperlukan untuk melanjutkan tugas di jendela konteks berikutnya. Sebagai contoh, beberapa model menggunakan prompt berikut:

```text wrap
You have written a partial transcript for the initial task above. Please write a summary of the transcript. The purpose of this summary is to provide continuity so you can continue to make progress towards solving the task in a future context, where the raw history above may not be accessible and will be replaced with this summary. Write down anything that would be helpful, including the state, next steps, learnings etc. You must wrap your summary in a <summary></summary> block.
```

Anda dapat memberikan instruksi kustom melalui parameter `instructions`. Instruksi kustom tidak melengkapi prompt default. Instruksi tersebut menggantikannya sepenuhnya:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112",
            "instructions": "Focus on preserving code snippets, variable names, and technical decisions."
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta compact-2026-01-12 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
        instructions: >-
          Focus on preserving code snippets, variable names, and
          technical decisions.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={
          "edits": [
              {
                  "type": "compact_20260112",
                  "instructions": "Focus on preserving code snippets, variable names, and technical decisions.",
              }
          ]
      },
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          instructions:
            "Focus on preserving code snippets, variable names, and technical decisions."
        }
      ]
    }
  });
  ```

  ```csharp C#
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages =
              [
                  new BetaMessageParam { Role = Role.User, Content = "Help me build a Python web scraper" },
                  new BetaMessageParam { Role = Role.Assistant, Content = "I'll help you build a web scraper..." },
                  new BetaMessageParam { Role = Role.User, Content = "Add support for JavaScript-rendered pages" }
              ],
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit
                  {
                      Instructions = "Focus on preserving code snippets, variable names, and technical decisions."
                  }]
              }
          };

          var message = await client.Beta.Messages.Create(parameters);
          Console.WriteLine(message);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Help me build a Python web scraper")),
  		{Role: anthropic.BetaMessageParamRoleAssistant, Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("I'll help you build a web scraper...")}},
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Add support for JavaScript-rendered pages")),
  	},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  				Instructions: anthropic.String("Focus on preserving code snippets, variable names, and technical decisions."),
  			}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .addBeta("compact-2026-01-12")
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addUserMessage("Help me build a Python web scraper")
              .addAssistantMessage("I'll help you build a web scraper...")
              .addUserMessage("Add support for JavaScript-rendered pages")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .instructions("Focus on preserving code snippets, variable names, and technical decisions.")
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Help me build a Python web scraper'],
          ['role' => 'assistant', 'content' => "I'll help you build a web scraper..."],
          ['role' => 'user', 'content' => 'Add support for JavaScript-rendered pages']
      ],
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'compact_20260112',
                  'instructions' => 'Focus on preserving code snippets, variable names, and technical decisions.'
              ]
          ]
      ]
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Help me build a Python web scraper" },
      { role: "assistant", content: "I'll help you build a web scraper..." },
      { role: "user", content: "Add support for JavaScript-rendered pages" }
    ],
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          instructions:
            "Focus on preserving code snippets, variable names, and technical decisions."
        }
      ]
    }
  )

  puts response
  ```
</CodeGroup>

### Berhenti sejenak setelah compaction

Gunakan `pause_after_compaction` untuk menjeda API setelah menghasilkan ringkasan compaction. Ini memungkinkan Anda menambahkan blok konten tambahan (seperti mempertahankan pesan terbaru atau pesan berorientasi instruksi tertentu) sebelum API melanjutkan dengan respons.

Ketika diaktifkan, API mengembalikan pesan dengan stop reason `compaction` setelah menghasilkan blok compaction:

<CodeGroup>
  ```bash cURL
  # pause_after_compaction menghentikan respons tepat setelah ringkasan
  # pemadatan agar Anda dapat menyesuaikan pesan sebelum melanjutkan. Langkah
  # lanjutan tidak cocok dijalankan sebagai perintah shell sekali jalan; lihat tab SDK
  # untuk alur jeda-dan-lanjutkan lengkap. Permintaan tunggal yang dijeda:
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112",
            "pause_after_compaction": true
          }
        ]
      }
    }'
  ```

  ```bash CLI
  # pause_after_compaction menghentikan respons tepat setelah ringkasan
  # pemadatan agar Anda dapat menyesuaikan pesan sebelum melanjutkan. Langkah
  # lanjutan tidak cocok untuk perintah CLI sekali jalan; lihat tab SDK
  # untuk alur jeda-dan-lanjutkan lengkap. Permintaan tunggal yang dijeda:
  ant beta:messages create \
    --beta compact-2026-01-12 \
    --format jsonl <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
        pause_after_compaction: true
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={
          "edits": [{"type": "compact_20260112", "pause_after_compaction": True}]
      },
  )

  # Periksa apakah pemadatan memicu jeda
  if response.stop_reason == "compaction":
      # Respons hanya berisi blok pemadatan
      messages.append({"role": "assistant", "content": response.content})

      # Lanjutkan permintaan
      response = client.beta.messages.create(
          betas=["compact-2026-01-12"],
          model="claude-opus-4-8",
          max_tokens=4096,
          messages=messages,
          context_management={"edits": [{"type": "compact_20260112"}]},
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  let response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          pause_after_compaction: true
        }
      ]
    }
  });

  // Periksa apakah pemadatan memicu jeda
  if (response.stop_reason === "compaction") {
    // Respons hanya berisi blok pemadatan
    messages.push({
      role: "assistant",
      content: response.content
    });

    // Lanjutkan permintaan
    response = await client.beta.messages.create({
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages,
      context_management: {
        edits: [{ type: "compact_20260112" }]
      }
    });
  }
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta.Messages;
  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Threading.Tasks;

  class Program
  {
      static async Task Main(string[] args)
      {
          var client = new AnthropicClient();
          var messages = new List<BetaMessageParam>
          {
              new() { Role = Role.User, Content = "Hello, Claude" }
          };

          var parameters = new MessageCreateParams
          {
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Betas = ["compact-2026-01-12"],
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit
                  {
                      PauseAfterCompaction = true
                  }]
              }
          };

          var response = await client.Beta.Messages.Create(parameters);

          if (response.StopReason == BetaStopReason.Compaction)
          {
              messages.Add(new BetaMessageParam
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
              });

              parameters = new()
              {
                  Model = "claude-opus-4-8",
                  MaxTokens = 4096,
                  Betas = ["compact-2026-01-12"],
                  Messages = messages,
                  ContextManagement = new BetaContextManagementConfig
                  {
                      Edits = [new BetaCompact20260112Edit()]
                  }
              };

              response = await client.Beta.Messages.Create(parameters);
          }

          Console.WriteLine(response);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  messages := []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))}

  compactEdit := anthropic.BetaContextManagementConfigParam{
  	Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  		{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  			PauseAfterCompaction: anthropic.Bool(true),
  		}},
  	},
  }

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:             anthropic.ModelClaudeOpus4_8,
  	MaxTokens:         4096,
  	Messages:          messages,
  	ContextManagement: compactEdit,
  	Betas:             []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "compaction" {
  	messages = append(messages, response.ToParam())

  	response, err = client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Messages:  messages,
  		ContextManagement: anthropic.BetaContextManagementConfigParam{
  			Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  				{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  			},
  		},
  		Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaStopReason;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addBeta("compact-2026-01-12")
              .addUserMessage("Help me build a website")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .pauseAfterCompaction(true)
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);

          // Periksa apakah pemadatan memicu jeda
          if (response.stopReason().isPresent()
                  && response.stopReason().get().equals(BetaStopReason.COMPACTION)) {
              // Tambahkan blok pemadatan dan lanjutkan permintaan
              // dengan membuat permintaan baru menggunakan konteks yang dipadatkan
              MessageCreateParams continueParams = MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .maxTokens(4096L)
                  .addBeta("compact-2026-01-12")
                  .addUserMessage("Help me build a website")
                  .addMessage(response)
                  .contextManagement(BetaContextManagementConfig.builder()
                      .addEdit(BetaCompact20260112Edit.builder().build())
                      .build())
                  .build();

              response = client.beta().messages().create(continueParams);
          }

          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'compact_20260112',
                  'pause_after_compaction' => true
              ]
          ]
      ]
  );

  if ($response->stopReason === 'compaction') {
      $messages[] = [
          'role' => 'assistant',
          'content' => $response->content
      ];

      $response = $client->beta->messages->create(
          maxTokens: 4096,
          messages: $messages,
          model: 'claude-opus-4-8',
          betas: ['compact-2026-01-12'],
          contextManagement: [
              'edits' => [
                  ['type' => 'compact_20260112']
              ]
          ]
      );
  }

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = [{ role: "user", content: "Hello, Claude" }]

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          pause_after_compaction: true
        }
      ]
    }
  )

  if response.stop_reason == :compaction
    messages << { role: "assistant", content: response.content }

    response = client.beta.messages.create(
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages,
      context_management: {
        edits: [{ type: "compact_20260112" }]
      }
    )
  end

  puts response
  ```
</CodeGroup>

#### Menerapkan anggaran token total

Ketika model mengerjakan tugas panjang dengan banyak iterasi penggunaan alat, konsumsi token total dapat meningkat secara signifikan. Anda dapat menggabungkan `pause_after_compaction` dengan penghitung compaction untuk memperkirakan penggunaan kumulatif dan menyelesaikan tugas dengan baik setelah anggaran tercapai.

Contoh ini hanya muncul dalam bahasa SDK: nilainya terletak pada logika pelacakan anggaran di sekitar permintaan. Permintaan mentahnya menggabungkan `trigger` dari [Konfigurasi pemicu](#trigger-configuration) dengan `pause_after_compaction` dari [Berhenti sejenak setelah compaction](#pausing-after-compaction).

<CodeGroup>
  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  TRIGGER_THRESHOLD = 100_000
  TOTAL_TOKEN_BUDGET = 3_000_000
  n_compactions = 0

  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={
          "edits": [
              {
                  "type": "compact_20260112",
                  "trigger": {"type": "input_tokens", "value": TRIGGER_THRESHOLD},
                  "pause_after_compaction": True,
              }
          ]
      },
  )

  if response.stop_reason == "compaction":
      n_compactions += 1
      messages.append({"role": "assistant", "content": response.content})

      # Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
      if n_compactions * TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET:
          messages.append(
              {
                  "role": "user",
                  "content": "Please wrap up your current work and summarize the final state.",
              }
          )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];
  const TRIGGER_THRESHOLD = 100_000;
  const TOTAL_TOKEN_BUDGET = 3_000_000;
  let compactionCount = 0;

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: { type: "input_tokens", value: TRIGGER_THRESHOLD },
          pause_after_compaction: true
        }
      ]
    }
  });

  if (response.stop_reason === "compaction") {
    compactionCount += 1;
    messages.push({ role: "assistant", content: response.content });

    // Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
    if (compactionCount * TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET) {
      messages.push({
        role: "user",
        content: "Please wrap up your current work and summarize the final state."
      });
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();
  List<BetaMessageParam> messages = [new() { Role = Role.User, Content = "Hello, Claude" }];

  const int TriggerThreshold = 100_000;
  const int TotalTokenBudget = 3_000_000;
  int compactionCount = 0;

  var response = await client.Beta.Messages.Create(new()
  {
      Betas = ["compact-2026-01-12"],
      Model = "claude-opus-4-8",
      MaxTokens = 4096,
      Messages = messages,
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaCompact20260112Edit
          {
              Trigger = new BetaInputTokensTrigger(TriggerThreshold),
              PauseAfterCompaction = true
          }]
      }
  });

  if (response.StopReason == BetaStopReason.Compaction)
  {
      compactionCount += 1;
      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
      });

      // Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
      if (compactionCount * TriggerThreshold >= TotalTokenBudget)
      {
          messages.Add(new()
          {
              Role = Role.User,
              Content = "Please wrap up your current work and summarize the final state."
          });
      }
  }

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()
  messages := []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))}

  const triggerThreshold = 100_000
  const totalTokenBudget = 3_000_000
  compactionCount := 0

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages:  messages,
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  				Trigger:              anthropic.BetaInputTokensTriggerParam{Value: triggerThreshold},
  				PauseAfterCompaction: anthropic.Bool(true),
  			}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "compaction" {
  	compactionCount++
  	messages = append(messages, response.ToParam())

  	// Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
  	if compactionCount*triggerThreshold >= totalTokenBudget {
  		messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Please wrap up your current work and summarize the final state.")))
  	}
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  import com.anthropic.models.beta.messages.BetaStopReason;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          long triggerThreshold = 100_000;
          long totalTokenBudget = 3_000_000;
          int compactionCount = 0;

          List<BetaMessageParam> messages = new ArrayList<>();
          messages.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .content("Hello, Claude")
              .build());

          MessageCreateParams params = MessageCreateParams.builder()
              .addBeta("compact-2026-01-12")
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .messages(messages)
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .trigger(BetaInputTokensTrigger.builder()
                          .value(triggerThreshold)
                          .build())
                      .pauseAfterCompaction(true)
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);

          if (response.stopReason().isPresent()
                  && response.stopReason().get().equals(BetaStopReason.COMPACTION)) {
              compactionCount += 1;
              messages.add(response.toParam());

              // Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
              if (compactionCount * triggerThreshold >= totalTokenBudget) {
                  messages.add(BetaMessageParam.builder()
                      .role(BetaMessageParam.Role.USER)
                      .content("Please wrap up your current work and summarize the final state.")
                      .build());
              }
          }

          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $triggerThreshold = 100_000;
  $totalTokenBudget = 3_000_000;
  $compactionCount = 0;

  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              [
                  'type' => 'compact_20260112',
                  'trigger' => ['type' => 'input_tokens', 'value' => $triggerThreshold],
                  'pause_after_compaction' => true
              ]
          ]
      ]
  );

  if ($response->stopReason === 'compaction') {
      $compactionCount += 1;
      $messages[] = ['role' => 'assistant', 'content' => $response->content];

      // Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
      if ($compactionCount * $triggerThreshold >= $totalTokenBudget) {
          $messages[] = [
              'role' => 'user',
              'content' => 'Please wrap up your current work and summarize the final state.'
          ];
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = [{ role: "user", content: "Hello, Claude" }]
  TRIGGER_THRESHOLD = 100_000
  TOTAL_TOKEN_BUDGET = 3_000_000
  compaction_count = 0

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [
        {
          type: "compact_20260112",
          trigger: { type: "input_tokens", value: TRIGGER_THRESHOLD },
          pause_after_compaction: true
        }
      ]
    }
  )

  if response.stop_reason == :compaction
    compaction_count += 1
    messages << { role: "assistant", content: response.content }

    # Estimasi total token yang dikonsumsi; minta penutupan jika melebihi anggaran
    if compaction_count * TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET
      messages << {
        role: "user",
        content: "Please wrap up your current work and summarize the final state."
      }
    end
  end
  ```
</CodeGroup>

## Bekerja dengan blok compaction

Ketika compaction dipicu, API mengembalikan blok `compaction` di awal respons asisten.

Percakapan yang berjalan lama mungkin menghasilkan beberapa compaction. Blok compaction terakhir mencerminkan keadaan akhir prompt, menggantikan konten sebelumnya dengan ringkasan yang dihasilkan.

```json Output
{
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation: The user requested help building a web scraper..."
    },
    {
      "type": "text",
      "text": "Based on our conversation so far..."
    }
  ]
}
```

### Mengirim kembali blok compaction

Anda harus mengirim kembali blok `compaction` ke API pada permintaan berikutnya untuk melanjutkan percakapan dengan prompt yang telah dipersingkat. Pendekatan paling sederhana adalah menambahkan seluruh konten respons ke pesan Anda:

<CodeGroup>
  ```bash cURL
  # Konten respons, termasuk blok pemadatan, harus dikirim kembali ke
  # API sebagai giliran asisten pada permintaan berikutnya. Mengelola daftar pesan itu
  # tidak cocok dilakukan lewat perintah shell sekali jalan; lihat tab CLI dan SDK
  # untuk alur lengkapnya. Permintaan pertama:
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112"
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta compact-2026-01-12 \
    --transform content \
    --format jsonl <<'YAML' > content.json
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
  YAML

  # Setelah menerima respons dengan blok pemadatan, tambahkan sebagai
  # giliran asisten dan lanjutkan percakapan
  ant beta:messages create --beta compact-2026-01-12 <<YAML
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
    - role: assistant
      content: $(cat content.json)
    - role: user
      content: Now add error handling
  context_management:
    edits:
      - type: compact_20260112
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  )
  # Setelah menerima respons dengan blok pemadatan
  messages.append({"role": "assistant", "content": response.content})

  # Lanjutkan percakapan
  messages.append({"role": "user", "content": "Now add error handling"})

  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });

  // Setelah menerima respons dengan blok pemadatan
  messages.push({
    role: "assistant",
    content: response.content
  });

  // Lanjutkan percakapan
  messages.push({ role: "user", content: "Now add error handling" });

  const nextResponse = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta.Messages;
  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Threading.Tasks;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var messages = new List<BetaMessageParam>
          {
              new() { Role = Role.User, Content = "Help me build a web scraper" }
          };

          var response = await client.Beta.Messages.Create(new()
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit()]
              }
          });

          messages.Add(new BetaMessageParam
          {
              Role = Role.Assistant,
              Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
          });

          messages.Add(new BetaMessageParam { Role = Role.User, Content = "Now add error handling" });

          var nextResponse = await client.Beta.Messages.Create(new()
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit()]
              }
          });

          Console.WriteLine(nextResponse);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  messages := []anthropic.BetaMessageParam{
  	anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Help me build a web scraper")),
  }

  compactEdit := anthropic.BetaContextManagementConfigParam{
  	Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  		{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  	},
  }

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:             anthropic.ModelClaudeOpus4_8,
  	MaxTokens:         4096,
  	Messages:          messages,
  	ContextManagement: compactEdit,
  	Betas:             []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  messages = append(messages, response.ToParam())

  messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Now add error handling")))

  nextResponse, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:             anthropic.ModelClaudeOpus4_8,
  	MaxTokens:         4096,
  	Messages:          messages,
  	ContextManagement: compactEdit,
  	Betas:             []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(nextResponse)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          // Permintaan pertama
          BetaMessage response = client.beta().messages().create(
              MessageCreateParams.builder()
                  .addBeta("compact-2026-01-12")
                  .model("claude-opus-4-8")
                  .maxTokens(4096L)
                  .addUserMessage("Help me build a web scraper")
                  .contextManagement(BetaContextManagementConfig.builder()
                      .addEdit(BetaCompact20260112Edit.builder().build())
                      .build())
                  .build());

          // Setelah menerima respons dengan blok pemadatan, tambahkan seluruh
          // konten (termasuk blok pemadatan) dan lanjutkan percakapan
          BetaMessage nextResponse = client.beta().messages().create(
              MessageCreateParams.builder()
                  .addBeta("compact-2026-01-12")
                  .model("claude-opus-4-8")
                  .maxTokens(4096L)
                  .addUserMessage("Help me build a web scraper")
                  .addMessage(response)
                  .addUserMessage("Now add error handling")
                  .contextManagement(BetaContextManagementConfig.builder()
                      .addEdit(BetaCompact20260112Edit.builder().build())
                      .build())
                  .build());

          System.out.println(nextResponse);
  ```

  ```php PHP
  $client = new Client();

  $messages = [
      ['role' => 'user', 'content' => 'Help me build a web scraper']
  ];

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [['type' => 'compact_20260112']]
      ]
  );

  $messages[] = ['role' => 'assistant', 'content' => $response->content];

  $messages[] = ['role' => 'user', 'content' => 'Now add error handling'];

  $nextResponse = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [['type' => 'compact_20260112']]
      ]
  );

  echo $nextResponse->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  messages = [
    { role: "user", content: "Help me build a web scraper" }
  ]

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )

  messages << { role: "assistant", content: response.content }

  messages << { role: "user", content: "Now add error handling" }

  next_response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )

  puts next_response.content
  ```
</CodeGroup>

Ketika API menerima blok `compaction`, semua blok konten sebelumnya diabaikan. Anda dapat:

* Menyimpan pesan asli dalam daftar Anda dan membiarkan API menangani penghapusan konten yang telah dipadatkan
* Secara manual menghapus pesan yang telah dipadatkan dan hanya menyertakan blok compaction dan seterusnya

### Streaming

Blok compaction di-stream secara berbeda dari blok teks. Anda menerima event `content_block_start`, diikuti oleh satu `content_block_delta` dengan konten ringkasan lengkap (tanpa streaming perantara), dan kemudian event `content_block_stop`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "stream": true,
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112"
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --stream \
    --beta compact-2026-01-12 \
    --format jsonl <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]

  with client.beta.messages.stream(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  ) as stream:
      for event in stream:
          if event.type == "content_block_start":
              if event.content_block.type == "compaction":
                  print("Compaction started...")
              elif event.content_block.type == "text":
                  print("Text response started...")

          elif event.type == "content_block_delta":
              if event.delta.type == "compaction_delta":
                  print(f"Compaction complete: {len(event.delta.content or '')} chars")
              elif event.delta.type == "text_delta":
                  print(event.delta.text, end="", flush=True)

      # Dapatkan pesan akhir yang terakumulasi
      message = stream.get_final_message()
      messages.append({"role": "assistant", "content": message.content})
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  const stream = await client.beta.messages.stream({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });

  for await (const event of stream) {
    if (event.type === "content_block_start") {
      if (event.content_block.type === "compaction") {
        console.log("Compaction started...");
      } else if (event.content_block.type === "text") {
        console.log("Text response started...");
      }
    } else if (event.type === "content_block_delta") {
      if (event.delta.type === "compaction_delta") {
        console.log(`Compaction complete: ${event.delta.content?.length ?? 0} chars`);
      } else if (event.delta.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
    }
  }

  // Dapatkan pesan akhir yang terakumulasi
  const message = await stream.finalMessage();
  messages.push({
    role: "assistant",
    content: message.content
  });
  ```

  ```csharp C#
  var client = new AnthropicClient();
  List<BetaMessageParam> messages = [new() { Role = Role.User, Content = "Hello" }];

  var parameters = new MessageCreateParams
  {
      Betas = ["compact-2026-01-12"],
      Model = "claude-opus-4-8",
      MaxTokens = 4096,
      Messages = messages,
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaCompact20260112Edit()]
      }
  };

  await foreach (var streamEvent in client.Beta.Messages.CreateStreaming(parameters))
  {
      if (streamEvent.TryPickContentBlockStart(out var startEvent))
      {
          if (startEvent.ContentBlock.TryPickBetaCompaction(out _))
          {
              Console.WriteLine("Compaction started...");
          }
          else if (startEvent.ContentBlock.TryPickBetaText(out _))
          {
              Console.WriteLine("Text response started...");
          }
      }
      else if (streamEvent.TryPickContentBlockDelta(out var deltaEvent))
      {
          if (deltaEvent.Delta.TryPickCompaction(out var compactionDelta))
          {
              Console.WriteLine($"Compaction complete: {compactionDelta.Content?.Length ?? 0} chars");
          }
          else if (deltaEvent.Delta.TryPickText(out var textDelta))
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  messages := []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))}

  stream := client.Beta.Messages.NewStreaming(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages:  messages,
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.BetaRawContentBlockStartEvent:
  		switch eventVariant.ContentBlock.AsAny().(type) {
  		case anthropic.BetaCompactionBlock:
  			fmt.Println("Compaction started...")
  		case anthropic.BetaTextBlock:
  			fmt.Println("Text response started...")
  		}
  	case anthropic.BetaRawContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.BetaCompactionContentBlockDelta:
  			fmt.Printf("Compaction complete: %d chars\n", len(deltaVariant.Content))
  		case anthropic.BetaTextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addBeta("compact-2026-01-12")
              .addUserMessage("Hello, Claude")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder().build())
                  .build())
              .build();

          try (var streamResponse = client.beta().messages().createStreaming(params)) {
              streamResponse.stream().forEach(event -> {
                  event.contentBlockStart().ifPresent(startEvent -> {
                      startEvent.contentBlock().compaction().ifPresent(c ->
                          System.out.println("Compaction started...")
                      );
                      startEvent.contentBlock().text().ifPresent(t ->
                          System.out.println("Text response started...")
                      );
                  });

                  event.contentBlockDelta().ifPresent(deltaEvent -> {
                      deltaEvent.delta().compaction().ifPresent(cd ->
                          System.out.println("Compaction complete: " + cd.content().map(String::length).orElse(0) + " chars")
                      );
                      deltaEvent.delta().text().ifPresent(td ->
                          System.out.print(td.text())
                      );
                  });
              });
          }
  ```

  ```php PHP
  $client = new Client();
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $stream = $client->beta->messages->createStream(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              ['type' => 'compact_20260112']
          ]
      ]
  );

  foreach ($stream as $event) {
      if ($event->type === 'content_block_start') {
          if ($event->contentBlock->type === 'compaction') {
              echo "Compaction started...\n";
          } elseif ($event->contentBlock->type === 'text') {
              echo "Text response started...\n";
          }
      } elseif ($event->type === 'content_block_delta') {
          if ($event->delta->type === 'compaction_delta') {
              echo "Compaction complete: " . strlen($event->delta->content ?? '') . " chars\n";
          } elseif ($event->delta->type === 'text_delta') {
              echo $event->delta->text;
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = [{ role: "user", content: "Hello, Claude" }]

  stream = client.beta.messages.stream(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )

  stream.each do |event|
    case event.type
    when :content_block_start
      if event.content_block.type == :compaction
        puts "Compaction started..."
      elsif event.content_block.type == :text
        puts "Text response started..."
      end
    when :content_block_delta
      if event.delta.type == :compaction_delta
        puts "Compaction complete: #{(event.delta.content || "").length} chars"
      elsif event.delta.type == :text_delta
        print event.delta.text
      end
    end
  end
  ```
</CodeGroup>

### Caching prompt

Compaction bekerja dengan baik bersama [caching prompt](/docs/id/build-with-claude/prompt-caching). Anda dapat menambahkan breakpoint `cache_control` pada blok compaction untuk meng-cache konten yang telah diringkas.

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "compaction",
      "content": "[summary text]",
      "cache_control": { "type": "ephemeral" }
    },
    {
      "type": "text",
      "text": "Based on our conversation..."
    }
  ]
}
```

#### Memaksimalkan cache hit dengan prompt sistem

Ketika compaction terjadi, ringkasan menjadi konten baru yang perlu ditulis ke cache. Tanpa breakpoint cache tambahan, hal ini juga akan membatalkan prompt sistem yang telah di-cache, sehingga perlu di-cache ulang bersama dengan ringkasan compaction.

Untuk memaksimalkan tingkat cache hit, tambahkan breakpoint `cache_control` di akhir prompt sistem Anda. Ini menjaga prompt sistem tetap di-cache secara terpisah dari percakapan, sehingga ketika compaction terjadi:

* Cache prompt sistem tetap valid dan dibaca dari cache
* Hanya ringkasan compaction yang perlu ditulis sebagai entri cache baru

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "system": [
        {
          "type": "text",
          "text": "You are a helpful coding assistant...",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112"
          }
        ]
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta compact-2026-01-12 <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  system:
    - type: text
      text: You are a helpful coding assistant...
      cache_control:
        type: ephemeral
  messages:
    - role: user
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  response = client.beta.messages.create(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      max_tokens=4096,
      system=[
          {
              "type": "text",
              "text": "You are a helpful coding assistant...",
              "cache_control": {
                  "type": "ephemeral"
              },  # Cache the system prompt separately
          }
      ],
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Hello, Claude" }
  ];

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    system: [
      {
        type: "text",
        text: "You are a helpful coding assistant...",
        cache_control: { type: "ephemeral" } // Cache the system prompt separately
      }
    ],
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          var client = new AnthropicClient();

          var parameters = new MessageCreateParams
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              System = new List<BetaTextBlockParam>
              {
                  new()
                  {
                      Text = "You are a helpful coding assistant...",
                      CacheControl = new BetaCacheControlEphemeral()
                  }
              },
              Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit()]
              }
          };

          var response = await client.Beta.Messages.Create(parameters);
          Console.WriteLine(response);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	System: []anthropic.BetaTextBlockParam{
  		{
  			Text:         "You are a helpful coding assistant...",
  			CacheControl: anthropic.NewBetaCacheControlEphemeralParam(),
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))},
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaCacheControlEphemeral;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .addBeta("compact-2026-01-12")
              .systemOfBetaTextBlockParams(List.of(
                  BetaTextBlockParam.builder()
                      .text("You are a helpful coding assistant...")
                      .cacheControl(BetaCacheControlEphemeral.builder().build())
                      .build()
              ))
              .addUserMessage("Hello, Claude")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder().build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      system: [
          [
              'type' => 'text',
              'text' => 'You are a helpful coding assistant...',
              'cache_control' => [
                  'type' => 'ephemeral'
              ]
          ]
      ],
      contextManagement: [
          'edits' => [
              ['type' => 'compact_20260112']
          ]
      ]
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 4096,
    system: [
      {
        type: "text",
        text: "You are a helpful coding assistant...",
        cache_control: {
          type: "ephemeral"
        }
      }
    ],
    messages: [{ role: "user", content: "Hello, Claude" }],
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )
  puts response
  ```
</CodeGroup>

Ini menjaga prompt sistem yang panjang tetap di-cache di sepanjang beberapa peristiwa compaction selama percakapan.

## Memahami penggunaan

Compaction memerlukan langkah sampling tambahan, yang berkontribusi pada batas laju dan penagihan. API mengembalikan informasi penggunaan terperinci dalam respons:

```json Output
{
  "usage": {
    "input_tokens": 23000,
    "output_tokens": 1000,
    "iterations": [
      {
        "type": "compaction",
        "input_tokens": 180000,
        "output_tokens": 3500
      },
      {
        "type": "message",
        "input_tokens": 23000,
        "output_tokens": 1000
      }
    ]
  }
}
```

Array `iterations` menunjukkan penggunaan untuk setiap iterasi sampling. Ketika compaction terjadi, Anda akan melihat iterasi `compaction` diikuti oleh iterasi `message` utama. `input_tokens` dan `output_tokens` tingkat atas sama persis dengan iterasi `message` dalam contoh ini karena hanya ada satu iterasi non-compaction. Jumlah token iterasi terakhir mencerminkan ukuran konteks efektif setelah compaction.

<Note>
  `input_tokens` dan `output_tokens` tingkat atas tidak menyertakan penggunaan iterasi compaction. Keduanya mencerminkan jumlah dari semua iterasi non-compaction. Untuk menghitung total token yang dikonsumsi dan ditagih untuk sebuah permintaan, jumlahkan semua entri dalam array `usage.iterations`.

  Jika sebelumnya Anda mengandalkan `usage.input_tokens` dan `usage.output_tokens` untuk pelacakan biaya atau audit, Anda perlu memperbarui logika pelacakan Anda untuk mengagregasi di seluruh `usage.iterations` ketika compaction diaktifkan. Dengan beta compaction diaktifkan, setiap respons menyertakan `usage.iterations`, bahkan jika tidak ada compaction yang terjadi. Entri `compaction` hanya muncul ketika compaction baru dipicu selama permintaan. Menerapkan kembali blok `compaction` sebelumnya tidak menimbulkan biaya compaction tambahan, dan field penggunaan tingkat atas tetap akurat dalam kasus tersebut.
</Note>

## Menggabungkan dengan fitur lain

### Alat server

Saat menggunakan alat server (seperti pencarian web), pemicu compaction diperiksa di awal setiap iterasi sampling. Compaction mungkin terjadi beberapa kali dalam satu permintaan tergantung pada ambang batas pemicu Anda dan jumlah output yang dihasilkan.

### Penghitungan token

Endpoint penghitungan token (`/v1/messages/count_tokens`) menerapkan blok `compaction` yang sudah ada dalam prompt Anda tetapi tidak memicu compaction baru. Gunakan endpoint ini untuk memeriksa jumlah token efektif Anda setelah compaction sebelumnya:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "messages": [
        {
          "role": "user",
          "content": "Hello, Claude"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112"
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
      content: Hello, Claude
  context_management:
    edits:
      - type: compact_20260112
  YAML

  CURRENT=$(ant beta:messages count-tokens \
    --beta compact-2026-01-12 \
    --transform input_tokens \
    --raw-output < request.yaml)

  ORIGINAL=$(ant beta:messages count-tokens \
    --beta compact-2026-01-12 \
    --transform context_management.original_input_tokens \
    --raw-output < request.yaml)

  printf 'Current tokens: %s\n' "$CURRENT"
  printf 'Original tokens: %s\n' "$ORIGINAL"
  ```

  ```python Python
  client = anthropic.Anthropic()
  messages = [{"role": "user", "content": "Hello, Claude"}]
  count_response = client.beta.messages.count_tokens(
      betas=["compact-2026-01-12"],
      model="claude-opus-4-8",
      messages=messages,
      context_management={"edits": [{"type": "compact_20260112"}]},
  )

  print(f"Current tokens: {count_response.input_tokens}")
  print(f"Original tokens: {count_response.context_management.original_input_tokens}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Summarize the key points of our conversation so far." }
  ];

  const countResponse = await client.beta.messages.countTokens({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  });

  console.log(`Current tokens: ${countResponse.input_tokens}`);
  console.log(`Original tokens: ${countResponse.context_management!.original_input_tokens}`);
  ```

  ```csharp C#
  AnthropicClient client = new();
  List<BetaMessageParam> messages = [new() { Role = Role.User, Content = "Hello" }];

  var countParams = new MessageCountTokensParams
  {
      Model = "claude-opus-4-8",
      Messages = messages,
      ContextManagement = new BetaContextManagementConfig
      {
          Edits = [new BetaCompact20260112Edit()]
      },
      Betas = ["compact-2026-01-12"]
  };

  var countResponse = await client.Beta.Messages.CountTokens(countParams);
  Console.WriteLine($"Current tokens: {countResponse.InputTokens}");
  Console.WriteLine($"Original tokens: {countResponse.ContextManagement?.OriginalInputTokens}");
  ```

  ```go Go
  client := anthropic.NewClient()
  messages := []anthropic.BetaMessageParam{anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude"))}

  countResponse, err := client.Beta.Messages.CountTokens(context.TODO(), anthropic.BetaMessageCountTokensParams{
  	Model:    anthropic.ModelClaudeOpus4_8,
  	Messages: messages,
  	ContextManagement: anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  		},
  	},
  	Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Current tokens: %d\n", countResponse.InputTokens)
  fmt.Printf("Original tokens: %d\n", countResponse.ContextManagement.OriginalInputTokens)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMessageTokensCount;
  import com.anthropic.models.beta.messages.MessageCountTokensParams;
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCountTokensParams params = MessageCountTokensParams.builder()
              .model("claude-opus-4-8")
              .addUserMessage("Hello, Claude")
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder().build())
                  .build())
              .addBeta("compact-2026-01-12")
              .build();

          BetaMessageTokensCount countResponse = client.beta().messages().countTokens(params);
          System.out.println("Current tokens: " + countResponse.inputTokens());
          System.out.println("Original tokens: " + countResponse.contextManagement().get().originalInputTokens());
  ```

  ```php PHP
  $client = new Client();
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $countResponse = $client->beta->messages->countTokens(
      messages: $messages,
      model: 'claude-opus-4-8',
      betas: ['compact-2026-01-12'],
      contextManagement: [
          'edits' => [
              ['type' => 'compact_20260112']
          ]
      ]
  );

  echo "Current tokens: " . $countResponse->inputTokens . "\n";
  echo "Original tokens: " . $countResponse->contextManagement->originalInputTokens . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = [{ role: "user", content: "Hello, Claude" }]

  count_response = client.beta.messages.count_tokens(
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    messages: messages,
    context_management: {
      edits: [{ type: "compact_20260112" }]
    }
  )

  puts "Current tokens: #{count_response.input_tokens}"
  puts "Original tokens: #{count_response.context_management.original_input_tokens}"
  ```
</CodeGroup>

## Contoh

Berikut adalah contoh lengkap percakapan yang berjalan lama dengan compaction:

<CodeGroup>
  ```bash cURL
  # curl mengirim permintaan individual; kelola array messages di
  # skrip pemanggil. Lihat tab SDK untuk loop chat() lengkap. Bentuk
  # permintaan satu giliran:
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Help me build a Python web scraper"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112",
            "trigger": {
              "type": "input_tokens",
              "value": 100000
            }
          }
        ]
      }
    }'
  ```

  ```bash CLI
  # CLI menangani giliran individual; pertahankan array messages di
  # skrip pemanggil. Lihat tab SDK untuk loop chat() lengkap. Bentuk
  # permintaan satu giliran:
  ant beta:messages create \
    --beta compact-2026-01-12 \
    --transform 'content.#(type=="text").text' \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Help me build a Python web scraper
  context_management:
    edits:
      - type: compact_20260112
        trigger:
          type: input_tokens
          value: 100000
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  messages: list[dict] = []


  def chat(user_message: str) -> str:
      messages.append({"role": "user", "content": user_message})

      response = client.beta.messages.create(
          betas=["compact-2026-01-12"],
          model="claude-opus-4-8",
          max_tokens=4096,
          messages=messages,
          context_management={
              "edits": [
                  {
                      "type": "compact_20260112",
                      "trigger": {"type": "input_tokens", "value": 100000},
                  }
              ]
          },
      )

      # Tambahkan respons (blok pemadatan otomatis disertakan)
      messages.append({"role": "assistant", "content": response.content})

      # Kembalikan konten teks
      return next(block.text for block in response.content if block.type == "text")


  # Jalankan percakapan panjang
  print(chat("Help me build a Python web scraper"))
  print(chat("Add support for JavaScript-rendered pages"))
  print(chat("Now add rate limiting and error handling"))
  # Terus panggil chat() selama percakapan masih diperlukan
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [];

  async function chat(userMessage: string): Promise<string> {
    messages.push({ role: "user", content: userMessage });

    const response = await client.beta.messages.create({
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages,
      context_management: {
        edits: [
          {
            type: "compact_20260112",
            trigger: { type: "input_tokens", value: 100000 }
          }
        ]
      }
    });

    // Tambahkan respons (blok pemadatan otomatis disertakan)
    messages.push({ role: "assistant", content: response.content });

    // Kembalikan konten teks
    const textBlock = response.content.find((block) => block.type === "text");
    return textBlock?.text ?? "";
  }

  // Jalankan percakapan panjang
  console.log(await chat("Help me build a Python web scraper"));
  console.log(await chat("Add support for JavaScript-rendered pages"));
  console.log(await chat("Now add rate limiting and error handling"));
  // Terus panggil chat() selama percakapan masih diperlukan
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  public class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();
          List<BetaMessageParam> messages = new();

          Console.WriteLine(await Chat(client, messages, "Help me build a Python web scraper"));
          Console.WriteLine(await Chat(client, messages, "Add support for JavaScript-rendered pages"));
          Console.WriteLine(await Chat(client, messages, "Now add rate limiting and error handling"));
      }

      static async Task<string> Chat(AnthropicClient client, List<BetaMessageParam> messages, string userMessage)
      {
          messages.Add(new() { Role = Role.User, Content = userMessage });

          var parameters = new MessageCreateParams
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit
                  {
                      Trigger = new BetaInputTokensTrigger(100000)
                  }]
              }
          };

          var response = await client.Beta.Messages.Create(parameters);

          messages.Add(new()
          {
              Role = Role.Assistant,
              Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
          });

          return response.Content
              .Select(b => b.Value)
              .OfType<BetaTextBlock>()
              .Select(tb => tb.Text)
              .FirstOrDefault() ?? "";
      }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  var (
  	client   = anthropic.NewClient()
  	messages []anthropic.BetaMessageParam
  )

  func chat(userMessage string) string {
  	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(userMessage)))

  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Messages:  messages,
  		ContextManagement: anthropic.BetaContextManagementConfigParam{
  			Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  				{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  					Trigger: anthropic.BetaInputTokensTriggerParam{Value: 100000},
  				}},
  			},
  		},
  		Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	messages = append(messages, response.ToParam())

  	for _, block := range response.Content {
  		if variant, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  			return variant.Text
  		}
  	}
  	return ""
  }

  func main() {
  	fmt.Println(chat("Help me build a Python web scraper"))
  	fmt.Println(chat("Add support for JavaScript-rendered pages"))
  	fmt.Println(chat("Now add rate limiting and error handling"))
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  // ...
      private static final AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      private static final List<BetaMessageParam> messages = new ArrayList<>();

      public static void main(String[] args) {
          System.out.println(chat("Help me build a Python web scraper"));
          System.out.println(chat("Add support for JavaScript-rendered pages"));
          System.out.println(chat("Now add rate limiting and error handling"));
      }

      private static String chat(String userMessage) {
          messages.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .content(userMessage)
              .build());

          MessageCreateParams params = MessageCreateParams.builder()
              .addBeta("compact-2026-01-12")
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .messages(messages)
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .trigger(BetaInputTokensTrigger.builder()
                          .value(100000L)
                          .build())
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);

          // Tambahkan respons (blok pemadatan otomatis disertakan)
          messages.add(response.toParam());

          return response.content().stream()
              .filter(block -> block.text().isPresent())
              .map(block -> block.text().get().text())
              .findFirst()
              .orElse("");
      }
  ```

  ```php PHP
  $client = new Client();
  $messages = [];

  function chat($client, &$messages, $userMessage) {
      $messages[] = ['role' => 'user', 'content' => $userMessage];

      $response = $client->beta->messages->create(
          maxTokens: 4096,
          messages: $messages,
          model: 'claude-opus-4-8',
          betas: ['compact-2026-01-12'],
          contextManagement: [
              'edits' => [
                  [
                      'type' => 'compact_20260112',
                      'trigger' => ['type' => 'input_tokens', 'value' => 100000]
                  ]
              ]
          ]
      );

      $messages[] = ['role' => 'assistant', 'content' => $response->content];

      foreach ($response->content as $block) {
          if ($block->type === 'text') {
              return $block->text;
          }
      }
      return '';
  }

  echo chat($client, $messages, "Help me build a Python web scraper") . "\n";
  echo chat($client, $messages, "Add support for JavaScript-rendered pages") . "\n";
  echo chat($client, $messages, "Now add rate limiting and error handling") . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = []

  def chat(client, messages, user_message)
    messages << { role: "user", content: user_message }

    response = client.beta.messages.create(
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages,
      context_management: {
        edits: [
          {
            type: "compact_20260112",
            trigger: { type: "input_tokens", value: 100000 }
          }
        ]
      }
    )

    messages << { role: "assistant", content: response.content }

    response.content.find { |block| block.type == :text }&.text || ""
  end

  puts chat(client, messages, "Help me build a Python web scraper")
  puts chat(client, messages, "Add support for JavaScript-rendered pages")
  puts chat(client, messages, "Now add rate limiting and error handling")
  ```
</CodeGroup>

Berikut adalah contoh yang menggunakan `pause_after_compaction` untuk mempertahankan pertukaran sebelumnya dan pesan pengguna saat ini (total tiga pesan) secara verbatim alih-alih meringkasnya:

<CodeGroup>
  ```bash cURL
  # curl mengirim permintaan individual; kelola array messages di skrip
  # pemanggil. Lihat tab SDK untuk loop chat() lengkap dengan penanganan
  # jeda-dan-pertahankan. Bentuk permintaan satu giliran:
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: compact-2026-01-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "messages": [
        {
          "role": "user",
          "content": "Help me build a Python web scraper"
        }
      ],
      "context_management": {
        "edits": [
          {
            "type": "compact_20260112",
            "trigger": {
              "type": "input_tokens",
              "value": 100000
            },
            "pause_after_compaction": true
          }
        ]
      }
    }'
  ```

  ```bash CLI
  # CLI menangani giliran individual; pertahankan array messages di
  # skrip pemanggil. Lihat tab SDK untuk loop chat() lengkap dengan
  # penanganan jeda-dan-pertahankan. Bentuk permintaan satu giliran:
  ant beta:messages create \
    --beta compact-2026-01-12 \
    --transform 'content.#(type=="text").text' \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Help me build a Python web scraper
  context_management:
    edits:
      - type: compact_20260112
        trigger:
          type: input_tokens
          value: 100000
        pause_after_compaction: true
  YAML
  ```

  ```python Python
  from typing import Any

  client = anthropic.Anthropic()

  messages: list[dict[str, Any]] = []


  def chat(user_message: str) -> str:
      messages.append({"role": "user", "content": user_message})

      response = client.beta.messages.create(
          betas=["compact-2026-01-12"],
          model="claude-opus-4-8",
          max_tokens=4096,
          messages=messages,
          context_management={
              "edits": [
                  {
                      "type": "compact_20260112",
                      "trigger": {"type": "input_tokens", "value": 100000},
                      "pause_after_compaction": True,
                  }
              ]
          },
      )

      # Periksa apakah pemadatan terjadi dan dijeda
      if response.stop_reason == "compaction":
          # Ambil blok pemadatan dari respons
          compaction_block = response.content[0]

          # Pertahankan pertukaran sebelumnya + pesan pengguna saat ini (3 pesan)
          # dengan menyertakannya setelah blok pemadatan
          preserved_messages = messages[-3:] if len(messages) >= 3 else messages

          # Bangun daftar pesan baru: pemadatan + pesan yang dipertahankan
          new_assistant_content = [compaction_block]
          messages_after_compaction = [
              {"role": "assistant", "content": new_assistant_content}
          ] + preserved_messages

          # Lanjutkan permintaan dengan konteks yang dipadatkan + pesan yang dipertahankan
          response = client.beta.messages.create(
              betas=["compact-2026-01-12"],
              model="claude-opus-4-8",
              max_tokens=4096,
              messages=messages_after_compaction,
              context_management={"edits": [{"type": "compact_20260112"}]},
          )

          # Perbarui daftar pesan kita untuk mencerminkan pemadatan
          messages.clear()
          messages.extend(messages_after_compaction)

      # Tambahkan respons akhir
      messages.append({"role": "assistant", "content": response.content})

      # Kembalikan konten teks
      return next(block.text for block in response.content if block.type == "text")


  # Jalankan percakapan panjang
  print(chat("Help me build a Python web scraper"))
  print(chat("Add support for JavaScript-rendered pages"))
  print(chat("Now add rate limiting and error handling"))
  # Terus panggil chat() selama percakapan masih membutuhkannya
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  let messages: Anthropic.Beta.Messages.BetaMessageParam[] = [];

  async function chat(userMessage: string): Promise<string> {
    messages.push({ role: "user", content: userMessage });

    let response = await client.beta.messages.create({
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages,
      context_management: {
        edits: [
          {
            type: "compact_20260112",
            trigger: { type: "input_tokens", value: 100000 },
            pause_after_compaction: true
          }
        ]
      }
    });

    // Periksa apakah pemadatan terjadi dan dijeda
    if (response.stop_reason === "compaction") {
      // Ambil blok pemadatan dari respons
      const compactionBlock = response.content[0];

      // Pertahankan pertukaran sebelumnya + pesan pengguna saat ini (3 pesan)
      // dengan menyertakannya setelah blok pemadatan
      const preservedMessages = messages.length >= 3 ? messages.slice(-3) : [...messages];

      // Bangun daftar pesan baru: pemadatan + pesan yang dipertahankan
      const messagesAfterCompaction: Anthropic.Beta.Messages.BetaMessageParam[] = [
        { role: "assistant", content: [compactionBlock] },
        ...preservedMessages
      ];

      // Lanjutkan permintaan dengan konteks yang dipadatkan + pesan yang dipertahankan
      response = await client.beta.messages.create({
        betas: ["compact-2026-01-12"],
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages: messagesAfterCompaction,
        context_management: {
          edits: [{ type: "compact_20260112" }]
        }
      });

      // Perbarui daftar pesan kita untuk mencerminkan pemadatan
      messages = messagesAfterCompaction;
    }

    // Tambahkan respons akhir
    messages.push({ role: "assistant", content: response.content });

    // Kembalikan konten teks
    const textBlock = response.content.find((block) => block.type === "text");
    return textBlock?.text ?? "";
  }

  // Jalankan percakapan panjang
  console.log(await chat("Help me build a Python web scraper"));
  console.log(await chat("Add support for JavaScript-rendered pages"));
  console.log(await chat("Now add rate limiting and error handling"));
  // Terus panggil chat() selama percakapan masih membutuhkannya
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;

  public class CompactionExample
  {
      private static AnthropicClient client = new();
      private static List<BetaMessageParam> messages = new();

      static async Task<string> Chat(string userMessage)
      {
          messages.Add(new() { Role = Role.User, Content = userMessage });

          var response = await client.Beta.Messages.Create(new()
          {
              Betas = ["compact-2026-01-12"],
              Model = "claude-opus-4-8",
              MaxTokens = 4096,
              Messages = messages,
              ContextManagement = new BetaContextManagementConfig
              {
                  Edits = [new BetaCompact20260112Edit
                  {
                      Trigger = new BetaInputTokensTrigger(100000),
                      PauseAfterCompaction = true
                  }]
              }
          });

          if (response.StopReason == BetaStopReason.Compaction)
          {
              if (!response.Content[0].TryPickCompaction(out _))
                  throw new InvalidOperationException("Expected compaction block");

              var preserved = messages.Count >= 3
                  ? messages.Skip(messages.Count - 3).ToList()
                  : new List<BetaMessageParam>(messages);

              var messagesAfterCompaction = new List<BetaMessageParam>
              {
                  new()
                  {
                      Role = Role.Assistant,
                      Content = new List<BetaContentBlockParam> { new BetaContentBlockParam(response.Content[0].Json) }
                  }
              };
              messagesAfterCompaction.AddRange(preserved);

              response = await client.Beta.Messages.Create(new()
              {
                  Betas = ["compact-2026-01-12"],
                  Model = "claude-opus-4-8",
                  MaxTokens = 4096,
                  Messages = messagesAfterCompaction,
                  ContextManagement = new BetaContextManagementConfig
                  {
                      Edits = [new BetaCompact20260112Edit()]
                  }
              });

              messages = messagesAfterCompaction;
          }

          messages.Add(new()
          {
              Role = Role.Assistant,
              Content = response.Content.Select(b => new BetaContentBlockParam(b.Json)).ToList()
          });

          return response.Content
              .Select(b => b.Value)
              .OfType<BetaTextBlock>()
              .Select(tb => tb.Text)
              .FirstOrDefault() ?? "";
      }

      static async Task Main()
      {
          Console.WriteLine(await Chat("Help me build a Python web scraper"));
          Console.WriteLine(await Chat("Add support for JavaScript-rendered pages"));
          Console.WriteLine(await Chat("Now add rate limiting and error handling"));
      }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  var (
  	client   = anthropic.NewClient()
  	messages []anthropic.BetaMessageParam
  )

  func chat(userMessage string) string {
  	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(userMessage)))

  	compactEdit := anthropic.BetaContextManagementConfigParam{
  		Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  			{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{
  				Trigger:              anthropic.BetaInputTokensTriggerParam{Value: 100000},
  				PauseAfterCompaction: anthropic.Bool(true),
  			}},
  		},
  	}

  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:             anthropic.ModelClaudeOpus4_8,
  		MaxTokens:         4096,
  		Messages:          messages,
  		ContextManagement: compactEdit,
  		Betas:             []anthropic.AnthropicBeta{"compact-2026-01-12"},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	if response.StopReason == "compaction" {
  		compactionParam := response.Content[0].ToParam()

  		var preserved []anthropic.BetaMessageParam
  		if len(messages) >= 3 {
  			preserved = messages[len(messages)-3:]
  		} else {
  			preserved = messages
  		}

  		messagesAfterCompaction := []anthropic.BetaMessageParam{
  			{Role: anthropic.BetaMessageParamRoleAssistant, Content: []anthropic.BetaContentBlockParamUnion{compactionParam}},
  		}
  		messagesAfterCompaction = append(messagesAfterCompaction, preserved...)

  		response, err = client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 4096,
  			Messages:  messagesAfterCompaction,
  			ContextManagement: anthropic.BetaContextManagementConfigParam{
  				Edits: []anthropic.BetaContextManagementConfigEditUnionParam{
  					{OfCompact20260112: &anthropic.BetaCompact20260112EditParam{}},
  				},
  			},
  			Betas: []anthropic.AnthropicBeta{"compact-2026-01-12"},
  		})
  		if err != nil {
  			log.Fatal(err)
  		}

  		messages = messagesAfterCompaction
  	}

  	messages = append(messages, response.ToParam())

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  			return textBlock.Text
  		}
  	}
  	return ""
  }

  func main() {
  	fmt.Println(chat("Help me build a Python web scraper"))
  	fmt.Println(chat("Add support for JavaScript-rendered pages"))
  	fmt.Println(chat("Now add rate limiting and error handling"))
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaContextManagementConfig;
  import com.anthropic.models.beta.messages.BetaCompact20260112Edit;
  import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
  import com.anthropic.models.beta.messages.BetaStopReason;
  // ...
      private static final AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      private static final List<BetaMessageParam> messages = new ArrayList<>();

      public static String chat(String userMessage) {
          messages.add(BetaMessageParam.builder()
              .role(BetaMessageParam.Role.USER)
              .content(userMessage)
              .build());

          MessageCreateParams params = MessageCreateParams.builder()
              .addBeta("compact-2026-01-12")
              .model("claude-opus-4-8")
              .maxTokens(4096L)
              .messages(messages)
              .contextManagement(BetaContextManagementConfig.builder()
                  .addEdit(BetaCompact20260112Edit.builder()
                      .trigger(BetaInputTokensTrigger.builder()
                          .value(100000L)
                          .build())
                      .pauseAfterCompaction(true)
                      .build())
                  .build())
              .build();

          BetaMessage response = client.beta().messages().create(params);

          // Periksa apakah pemadatan terjadi dan dijeda
          if (response.stopReason().isPresent()
                  && response.stopReason().get().equals(BetaStopReason.COMPACTION)) {
              // Pertahankan pertukaran sebelumnya + pesan pengguna saat ini (3 pesan)
              List<BetaMessageParam> preservedMessages = messages.size() >= 3
                  ? new ArrayList<>(messages.subList(messages.size() - 3, messages.size()))
                  : new ArrayList<>(messages);

              // Bangun daftar pesan baru: pemadatan + pesan yang dipertahankan
              List<BetaMessageParam> messagesAfterCompaction = new ArrayList<>();
              messagesAfterCompaction.add(response.toParam());
              messagesAfterCompaction.addAll(preservedMessages);

              // Lanjutkan permintaan dengan konteks yang dipadatkan + pesan yang dipertahankan
              MessageCreateParams continueParams = MessageCreateParams.builder()
                  .addBeta("compact-2026-01-12")
                  .model("claude-opus-4-8")
                  .maxTokens(4096L)
                  .messages(messagesAfterCompaction)
                  .contextManagement(BetaContextManagementConfig.builder()
                      .addEdit(BetaCompact20260112Edit.builder().build())
                      .build())
                  .build();

              response = client.beta().messages().create(continueParams);

              // Perbarui daftar pesan kita untuk mencerminkan pemadatan
              messages.clear();
              messages.addAll(messagesAfterCompaction);
          }

          // Tambahkan respons akhir
          messages.add(response.toParam());

          return response.content().stream()
              .filter(block -> block.text().isPresent())
              .map(block -> block.text().get().text())
              .findFirst()
              .orElse("");
      }

      public static void main(String[] args) {
          System.out.println(chat("Help me build a Python web scraper"));
          System.out.println(chat("Add support for JavaScript-rendered pages"));
          System.out.println(chat("Now add rate limiting and error handling"));
      }
  ```

  ```php PHP
  $client = new Client();
  $messages = [];

  function chat($client, &$messages, $userMessage) {
      $messages[] = ['role' => 'user', 'content' => $userMessage];

      $response = $client->beta->messages->create(
          maxTokens: 4096,
          messages: $messages,
          model: 'claude-opus-4-8',
          betas: ['compact-2026-01-12'],
          contextManagement: [
              'edits' => [
                  [
                      'type' => 'compact_20260112',
                      'trigger' => ['type' => 'input_tokens', 'value' => 100000],
                      'pause_after_compaction' => true
                  ]
              ]
          ]
      );

      if ($response->stopReason === 'compaction') {
          $compactionBlock = $response->content[0];

          $preserved = count($messages) >= 3
              ? array_slice($messages, -3)
              : $messages;

          $messagesAfterCompaction = array_merge(
              [['role' => 'assistant', 'content' => [$compactionBlock]]],
              $preserved
          );

          $response = $client->beta->messages->create(
              maxTokens: 4096,
              messages: $messagesAfterCompaction,
              model: 'claude-opus-4-8',
              betas: ['compact-2026-01-12'],
              contextManagement: [
                  'edits' => [['type' => 'compact_20260112']]
              ]
          );

          $messages = $messagesAfterCompaction;
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];

      foreach ($response->content as $block) {
          if ($block->type === 'text') {
              return $block->text;
          }
      }
      return '';
  }

  echo chat($client, $messages, "Help me build a Python web scraper") . "\n";
  echo chat($client, $messages, "Add support for JavaScript-rendered pages") . "\n";
  echo chat($client, $messages, "Now add rate limiting and error handling") . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  messages = []

  def chat(client, messages, user_message)
    messages << { role: "user", content: user_message }

    response = client.beta.messages.create(
      betas: ["compact-2026-01-12"],
      model: "claude-opus-4-8",
      max_tokens: 4096,
      messages: messages,
      context_management: {
        edits: [
          {
            type: "compact_20260112",
            trigger: { type: "input_tokens", value: 100000 },
            pause_after_compaction: true
          }
        ]
      }
    )

    if response.stop_reason == :compaction
      compaction_block = response.content[0]

      preserved = messages.length >= 3 ? messages[-3..-1] : messages.dup

      messages_after_compaction = [
        { role: "assistant", content: [compaction_block] }
      ] + preserved

      response = client.beta.messages.create(
        betas: ["compact-2026-01-12"],
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages: messages_after_compaction,
        context_management: {
          edits: [{ type: "compact_20260112" }]
        }
      )

      messages.clear
      messages.concat(messages_after_compaction)
    end

    messages << { role: "assistant", content: response.content }

    response.content.find { |block| block.type == :text }&.text || ""
  end

  puts chat(client, messages, "Help me build a Python web scraper")
  puts chat(client, messages, "Add support for JavaScript-rendered pages")
  puts chat(client, messages, "Now add rate limiting and error handling")
  ```
</CodeGroup>

## Batasan saat ini

* **Model yang sama untuk peringkasan:** Model yang ditentukan dalam permintaan Anda digunakan untuk peringkasan. Tidak ada opsi untuk menggunakan model yang berbeda (misalnya, yang lebih murah) untuk ringkasan.

* **Compaction mungkin gagal ketika alat didefinisikan:** Ketika permintaan Anda menyertakan `tools`, model terkadang memanggil alat selama langkah peringkasan internal alih-alih menulis ringkasan. Ketika ini terjadi, respons berisi blok `compaction` dengan `content: null`. Untuk mencegah hal ini, atur [`instructions`](#custom-summarization-instructions) ke prompt yang secara eksplisit memberi tahu model untuk tidak memanggil alat, misalnya:

  ```text wrap
  Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary for continuing the task in the next context window. Do not call any tools while writing this summary; respond with text only.
  ```

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Pengeditan konteks" icon="edit" href="/docs/id/build-with-claude/context-editing">
    Kelola konteks percakapan secara otomatis seiring pertumbuhannya dengan pengeditan konteks.
  </Card>

  <Card title="Jendela konteks" icon="arrows-left-right" href="/docs/id/build-with-claude/context-windows">
    Pelajari tentang ukuran jendela konteks dan strategi pengelolaannya.
  </Card>

  <Card title="Cookbook pemadatan memori sesi" icon="book" href="https://platform.claude.com/cookbook/misc-session-memory-compaction">
    Jelajahi implementasi praktis yang mengelola percakapan yang berjalan lama dengan pemadatan memori sesi instan menggunakan background threading dan caching prompt.
  </Card>
</CardGroup>
