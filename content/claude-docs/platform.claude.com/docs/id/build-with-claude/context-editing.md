---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-editing
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 219ea5502763f40497f6d33e16032f5a839c015fb857438485a89fb392e86dcc
---

# Pengeditan konteks

Kelola percakapan konteks secara otomatis saat berkembang dengan pengeditan konteks.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Ikhtisar

<Note>
Untuk sebagian besar kasus penggunaan, [pemadatan sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk mengelola konteks dalam percakapan yang berjalan lama. Strategi di halaman ini berguna untuk skenario spesifik di mana Anda memerlukan kontrol yang lebih halus atas konten apa yang dihapus.
</Note>

Pengeditan konteks memungkinkan Anda untuk secara selektif menghapus konten tertentu dari riwayat percakapan saat berkembang. Selain mengoptimalkan biaya dan tetap dalam batas, ini tentang secara aktif mengkurasi apa yang Claude lihat: konteks adalah sumber daya yang terbatas dengan hasil yang semakin berkurang, dan konten yang tidak relevan merusak fokus model. Pengeditan konteks memberi Anda kontrol runtime yang halus atas kurasi tersebut. Untuk prinsip yang lebih luas di balik manajemen konteks, lihat [Rekayasa konteks yang efektif](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Halaman ini mencakup:

- **Penghapusan hasil alat** - Terbaik untuk alur kerja agentic dengan penggunaan alat yang berat di mana hasil alat lama tidak lagi diperlukan
- **Penghapusan blok pemikiran** - Untuk mengelola blok pemikiran saat menggunakan pemikiran yang diperluas, dengan opsi untuk mempertahankan pemikiran terbaru untuk kontinuitas konteks
- **Pemadatan SDK sisi klien** - Alternatif berbasis SDK untuk manajemen konteks berbasis ringkasan (pemadatan sisi server umumnya lebih disukai)

| Pendekatan | Tempat dijalankan | Strategi | Cara kerjanya |
|----------|---------------|------------|--------------|
| **Sisi server** | API | Penghapusan hasil alat (`clear_tool_uses_20250919`)<br/>Penghapusan blok pemikiran (`clear_thinking_20251015`) | Diterapkan sebelum prompt mencapai Claude. Menghapus konten tertentu dari riwayat percakapan. Setiap strategi dapat dikonfigurasi secara independen. |
| **Sisi klien** | SDK | Pemadatan | Tersedia di [Python, TypeScript, dan Ruby SDKs](/docs/id/api/client-sdks) saat menggunakan [`tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner). Menghasilkan ringkasan dan mengganti riwayat percakapan lengkap. Lihat [Pemadatan sisi klien](#client-side-compaction-sdk) di bawah. |

## Strategi sisi server

<Note>
Pengeditan konteks dalam beta dengan dukungan untuk penghapusan hasil alat dan penghapusan blok pemikiran. Untuk mengaktifkannya, gunakan header beta `context-management-2025-06-27` dalam permintaan API Anda.

Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88).
</Note>

### Penghapusan hasil alat

Strategi `clear_tool_uses_20250919` menghapus hasil alat ketika konteks percakapan tumbuh melampaui ambang batas yang dikonfigurasi. Ini sangat berguna untuk alur kerja agentic dengan penggunaan alat yang berat. Hasil alat yang lebih lama (seperti konten file atau hasil pencarian) tidak lagi diperlukan setelah Claude memprosesnya.

Ketika diaktifkan, API secara otomatis menghapus hasil alat tertua dalam urutan kronologis. API mengganti setiap hasil yang dihapus dengan teks placeholder sehingga Claude tahu itu telah dihapus. Secara default, hanya hasil alat yang dihapus. Anda dapat secara opsional menghapus baik hasil alat maupun panggilan alat (parameter penggunaan alat) dengan mengatur `clear_tool_inputs` ke true.

### Penghapusan blok pemikiran

Strategi `clear_thinking_20251015` mengelola blok `thinking` dalam percakapan ketika pemikiran yang diperluas diaktifkan. Strategi ini memberi Anda kontrol atas pelestarian pemikiran: Anda dapat memilih untuk menyimpan lebih banyak blok pemikiran untuk mempertahankan kontinuitas penalaran, atau menghapusnya lebih agresif untuk menghemat ruang konteks.

<Tip>
**Perilaku default:** Ketika pemikiran yang diperluas diaktifkan tanpa mengonfigurasi strategi `clear_thinking_20251015`, API secara otomatis menyimpan hanya blok pemikiran dari giliran asisten terakhir (setara dengan `keep: {type: "thinking_turns", value: 1}`).

Untuk memaksimalkan cache hits, pertahankan semua blok pemikiran dengan mengatur `keep: "all"`.
</Tip>

Giliran percakapan asisten mungkin mencakup beberapa blok konten (misalnya saat menggunakan alat) dan beberapa blok pemikiran (misalnya dengan [pemikiran yang disisipi](/docs/id/build-with-claude/extended-thinking#interleaved-thinking)).

### Pengeditan konteks terjadi sisi server

Pengeditan konteks diterapkan sisi server sebelum prompt mencapai Claude. Aplikasi klien Anda mempertahankan riwayat percakapan lengkap yang tidak dimodifikasi. Anda tidak perlu menyinkronkan status klien Anda dengan versi yang diedit. Terus kelola riwayat percakapan lengkap Anda secara lokal seperti biasanya.

### Pengeditan konteks dan caching prompt

Interaksi pengeditan konteks dengan [prompt caching](/docs/id/build-with-claude/prompt-caching) bervariasi menurut strategi:

- **Penghapusan hasil alat**: Membatalkan prefix prompt yang di-cache ketika konten dihapus. Untuk memperhitungkan ini, hapus cukup token untuk membuat pembatalan cache layak. Gunakan parameter `clear_at_least` untuk memastikan jumlah token minimum dihapus setiap kali. Anda akan dikenakan biaya penulisan cache setiap kali konten dihapus, tetapi permintaan berikutnya dapat menggunakan kembali prefix yang baru di-cache.

- **Penghapusan blok pemikiran**: Ketika blok pemikiran **disimpan** dalam konteks (tidak dihapus), cache prompt dipertahankan, memungkinkan cache hits dan mengurangi biaya token input. Ketika blok pemikiran **dihapus**, cache dibatalkan pada titik di mana penghapusan terjadi. Konfigurasikan parameter `keep` berdasarkan apakah Anda ingin memprioritaskan kinerja cache atau ketersediaan jendela konteks.

## Model yang didukung

Pengeditan konteks tersedia di semua model Claude yang didukung.

## Penggunaan penghapusan hasil alat

Cara paling sederhana untuk mengaktifkan penghapusan hasil alat adalah dengan menentukan hanya jenis strategi. Semua [opsi konfigurasi](#configuration-options-for-tool-result-clearing) lainnya menggunakan nilai default mereka:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Search for recent developments in AI"}],
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-7",
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

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = "claude-opus-4-7",
    MaxTokens = 4096,
    Messages = [
        new() { Role = Role.User, Content = "Search for recent developments in AI" }
    ],
    Tools = [
        new() { Type = "web_search_20250305", Name = "web_search" }
    ],
    ContextManagement = new BetaContextManagementConfig()
    {
        Edits = [new BetaClearToolUses20250919Edit()]
    },
    Betas = ["context-management-2025-06-27"]
};

var response = await client.Beta.Messages.Create(parameters);
Console.WriteLine(response);
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
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
}
```

```java Java hidelines={1..4,9..12,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaWebSearchTool20250305;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class WebSearchExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(4096L)
            .addUserMessage("Search for recent developments in AI")
            .addTool(BetaWebSearchTool20250305.builder().build())
            .contextManagement(BetaContextManagementConfig.builder()
                .addEdit(BetaClearToolUses20250919Edit.builder().build())
                .build())
            .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        ['role' => 'user', 'content' => 'Search for recent developments in AI']
    ],
    model: 'claude-opus-4-7',
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

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-7",
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

```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-7",
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
model: claude-opus-4-7
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
    model="claude-opus-4-7",
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
                # Trigger clearing when threshold is exceeded
                "trigger": {"type": "input_tokens", "value": 30000},
                # Number of tool uses to keep after clearing
                "keep": {"type": "tool_uses", "value": 3},
                # Optional: Clear at least this many tokens
                "clear_at_least": {"type": "input_tokens", "value": 5000},
                # Exclude these tools from being cleared
                "exclude_tools": ["web_search"],
            }
        ]
    },
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-7",
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
        // Trigger clearing when threshold is exceeded
        trigger: {
          type: "input_tokens",
          value: 30000
        },
        // Number of tool uses to keep after clearing
        keep: {
          type: "tool_uses",
          value: 3
        },
        // Optional: Clear at least this many tokens
        clear_at_least: {
          type: "input_tokens",
          value: 5000
        },
        // Exclude these tools from being cleared
        exclude_tools: ["web_search"]
      }
    ]
  }
});
```

```csharp C# nocheck
using System;
using System.Collections.Generic;
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
            Model = "claude-opus-4-7",
            MaxTokens = 4096,
            Messages = new List<BetaMessageParam>
            {
                new() { Role = Role.User, Content = "Create a simple command line calculator app using Python" }
            },
            Tools = new List<object>
            {
                new Dictionary<string, object>
                {
                    { "type", "text_editor_20250728" },
                    { "name", "str_replace_based_edit_tool" },
                    { "max_characters", 10000 }
                },
                new Dictionary<string, object>
                {
                    { "type", "web_search_20250305" },
                    { "name", "web_search" },
                    { "max_uses", 3 }
                }
            },
            Betas = new List<string> { "context-management-2025-06-27" },
            ContextManagement = new Dictionary<string, object>
            {
                {
                    "edits", new List<object>
                    {
                        new Dictionary<string, object>
                        {
                            { "type", "clear_tool_uses_20250919" },
                            { "trigger", new Dictionary<string, object>
                                {
                                    { "type", "input_tokens" },
                                    { "value", 30000 }
                                }
                            },
                            { "keep", new Dictionary<string, object>
                                {
                                    { "type", "tool_uses" },
                                    { "value", 3 }
                                }
                            },
                            { "clear_at_least", new Dictionary<string, object>
                                {
                                    { "type", "input_tokens" },
                                    { "value", 5000 }
                                }
                            },
                            { "exclude_tools", new List<string> { "web_search" } }
                        }
                    }
                }
            }
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
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
}
```

```java Java nocheck hidelines={1..4,13..16,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
import com.anthropic.models.beta.messages.BetaWebSearchTool20250305;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
import com.anthropic.models.beta.messages.BetaInputTokensClearAtLeast;
import com.anthropic.models.beta.messages.BetaToolUsesKeep;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class ContextManagementExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        [
            'role' => 'user',
            'content' => 'Create a simple command line calculator app using Python'
        ]
    ],
    model: 'claude-opus-4-7',
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

echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-7",
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

## Penggunaan pembersihan blok pemikiran

Aktifkan pembersihan blok pemikiran untuk mengelola konteks dan prompt caching secara efektif ketika pemikiran yang diperluas diaktifkan:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": "Hello"}],
        "thinking": {
            "type": "enabled",
            "budget_tokens": 10000
        },
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
model: claude-opus-4-6
max_tokens: 16000
messages:
  - role: user
    content: Hello
thinking:
  type: enabled
  budget_tokens: 10000
context_management:
  edits:
    - type: clear_thinking_20251015
      keep:
        type: thinking_turns
        value: 2
YAML
```

```python Python nocheck
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    messages=[...],
    thinking={"type": "enabled", "budget_tokens": 10000},
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

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  messages: [
    // ...
  ],
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
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

```csharp C# nocheck
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
            Model = "claude-opus-4-6",
            MaxTokens = 16000,
            Messages = [],
            Thinking = new BetaThinkingParam
            {
                Type = "enabled",
                BudgetTokens = 10000
            },
            Betas = ["context-management-2025-06-27"],
            ContextManagement = new BetaContextManagementConfig()
            {
                Edits = [
                    new BetaClearThinking20251015Edit()
                    {
                        Keep = new BetaThinkingTurnsKeep
                        {
                            Type = "thinking_turns",
                            Value = 2
                        }
                    }
                ]
            }
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 16000,
		Messages:  []anthropic.BetaMessageParam{},
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(10000),
		Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaContextManagement2025_06_27},
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
}
```

```java Java nocheck hidelines={1..4,10..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearThinking20251015Edit;
import com.anthropic.models.beta.messages.BetaThinkingTurns;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(16000L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(10000L)
                .build())
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 16000,
    messages: [/* ... */],
    model: 'claude-opus-4-6',
    betas: ['context-management-2025-06-27'],
    thinking: [
        'type' => 'enabled',
        'budget_tokens' => 10000
    ],
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

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new
messages = [{ role: "user", content: "Explain quantum computing in simple terms" }]

response = client.beta.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 16000,
  messages: messages,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
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

### Opsi konfigurasi untuk pembersihan blok pemikiran

Strategi `clear_thinking_20251015` mendukung konfigurasi berikut:

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `keep` | `{type: "thinking_turns", value: 1}` | Menentukan berapa banyak putaran asisten terbaru dengan blok pemikiran yang akan dipertahankan. Gunakan `{type: "thinking_turns", value: N}` di mana N harus > 0 untuk mempertahankan N putaran terakhir, atau `"all"` untuk mempertahankan semua blok pemikiran. |

**Contoh konfigurasi:**

Pertahankan blok pemikiran dari 3 putaran asisten terakhir:

```json
{
  "type": "clear_thinking_20251015",
  "keep": {
    "type": "thinking_turns",
    "value": 3
  }
}
```

Pertahankan semua blok pemikiran (memaksimalkan cache hits):

```json
{
  "type": "clear_thinking_20251015",
  "keep": "all"
}
```

### Menggabungkan strategi

Anda dapat menggunakan pembersihan blok pemikiran dan pembersihan hasil alat bersama-sama:

<Note>
Ketika menggunakan beberapa strategi, strategi `clear_thinking_20251015` harus didaftar terlebih dahulu dalam array `edits`.
</Note>

<CodeGroup>

```bash CLI
ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
model: claude-opus-4-6
max_tokens: 16000
thinking:
  type: enabled
  budget_tokens: 10000
messages:
  - role: user
    content: Hello
tools:
  - type: web_search_20250305
    name: web_search
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

```python Python nocheck
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    messages=[...],
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[...],
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
```

```typescript TypeScript nocheck
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  messages: [
    // ...
  ],
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [
    // ...
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
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Beta.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_6,
            MaxTokens = 16000,
            Messages = [],
            Thinking = new BetaThinkingParam
            {
                Type = "enabled",
                BudgetTokens = 10000
            },
            Tools = [],
            Betas = ["context-management-2025-06-27"],
            ContextManagement = new BetaContextManagementConfig()
            {
                Edits = [
                    new BetaClearThinking20251015Edit()
                    {
                        Keep = new BetaThinkingTurnsKeep
                        {
                            Type = "thinking_turns",
                            Value = 2
                        }
                    },
                    new BetaClearToolUses20250919Edit()
                    {
                        Trigger = new BetaInputTokensTrigger
                        {
                            Type = "input_tokens",
                            Value = 50000
                        },
                        Keep = new BetaToolUsesKeep
                        {
                            Type = "tool_uses",
                            Value = 5
                        }
                    }
                ]
            }
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_6,
		MaxTokens: 16000,
		Messages:  []anthropic.BetaMessageParam{},
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(10000),
		Tools:     []anthropic.BetaToolUnionParam{},
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
}
```

```java Java nocheck hidelines={1..4,13..16,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearThinking20251015Edit;
import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
import com.anthropic.models.beta.messages.BetaThinkingTurns;
import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
import com.anthropic.models.beta.messages.BetaToolUsesKeep;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class ContextManagementExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_6)
            .maxTokens(16000L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(10000L)
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 16000,
    messages: [/* ... */],
    model: 'claude-opus-4-6',
    betas: ['context-management-2025-06-27'],
    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
    tools: [/* ... */],
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

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new
messages = [{ role: "user", content: "Explain quantum computing in simple terms" }]

response = client.beta.messages.create(
  model: "claude-opus-4-6",
  max_tokens: 16000,
  messages: messages,
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [
    # ...
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

## Opsi konfigurasi untuk pembersihan hasil alat

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `trigger` | 100.000 token input | Menentukan kapan strategi pengeditan konteks diaktifkan. Setelah prompt melebihi ambang batas ini, pembersihan akan dimulai. Anda dapat menentukan nilai ini dalam `input_tokens` atau `tool_uses`. |
| `keep` | 3 penggunaan alat | Menentukan berapa banyak pasangan penggunaan alat/hasil terbaru yang akan dipertahankan setelah pembersihan terjadi. API menghapus interaksi alat tertua terlebih dahulu, mempertahankan yang paling baru. |
| `clear_at_least` | Tidak ada | Memastikan jumlah token minimum dihapus setiap kali strategi diaktifkan. Jika API tidak dapat menghapus setidaknya jumlah yang ditentukan, strategi tidak akan diterapkan. Ini membantu menentukan apakah pembersihan konteks layak memecahkan cache prompt Anda. |
| `exclude_tools` | Tidak ada | Daftar nama alat yang penggunaan alat dan hasilnya tidak boleh pernah dihapus. Berguna untuk mempertahankan konteks penting. |
| `clear_tool_inputs` | `false` | Mengontrol apakah parameter panggilan alat dihapus bersama dengan hasil alat. Secara default, hanya hasil alat yang dihapus sambil menjaga panggilan alat asli Claude tetap terlihat. |

## Respons pengeditan konteks

Anda dapat melihat pengeditan konteks mana yang diterapkan pada permintaan Anda menggunakan bidang respons `context_management`, bersama dengan statistik berguna tentang konten dan token input yang dihapus.

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
      // Ketika menggunakan `clear_thinking_20251015`
      {
        "type": "clear_thinking_20251015",
        "cleared_thinking_turns": 3,
        "cleared_input_tokens": 15000
      },
      // Ketika menggunakan `clear_tool_uses_20250919`
      {
        "type": "clear_tool_uses_20250919",
        "cleared_tool_uses": 8,
        "cleared_input_tokens": 50000
      }
    ]
  }
}
```

Untuk respons streaming, pengeditan konteks akan disertakan dalam acara `message_delta` terakhir:

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

Titik akhir [penghitungan token](/docs/id/build-with-claude/token-counting) mendukung manajemen konteks, memungkinkan Anda melihat pratinjau berapa banyak token yang akan digunakan prompt Anda setelah pengeditan konteks diterapkan.

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-7",
        "messages": [
            {
                "role": "user",
                "content": "Continue our conversation..."
            }
        ],
        "tools": [],
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
model: claude-opus-4-7
messages:
  - role: user
    content: Continue our conversation...
tools: []
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
  --format yaml < request.yaml)

INPUT_TOKENS=$(ant beta:messages count-tokens \
  --beta context-management-2025-06-27 \
  --transform input_tokens --format yaml < request.yaml)

printf 'Original tokens: %s\n' "$ORIGINAL"
printf 'After clearing: %s\n' "$INPUT_TOKENS"
printf 'Savings: %s tokens\n' "$((ORIGINAL - INPUT_TOKENS))"
```

```python Python nocheck
response = client.beta.messages.count_tokens(
    model="claude-opus-4-7",
    messages=[{"role": "user", "content": "Continue our conversation..."}],
    tools=[...],  # Your tool definitions
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

print(f"Original tokens: {response.context_management['original_input_tokens']}")
print(f"After clearing: {response.input_tokens}")
print(
    f"Savings: {response.context_management['original_input_tokens'] - response.input_tokens} tokens"
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.countTokens({
  model: "claude-opus-4-7",
  messages: [
    {
      role: "user",
      content: "Continue our conversation..."
    }
  ],
  tools: [
    // ...
  ], // Your tool definitions
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

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Beta.Messages;

var client = new AnthropicClient
{
    ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
};

var parameters = new BetaMessageTokensCountParams
{
    Model = "claude-opus-4-7",
    Messages = [new() { Role = Role.User, Content = "Continue our conversation..." }],
    Betas = ["context-management-2025-06-27"],
    ContextManagement = new BetaContextManagementConfig
    {
        Edits = [
            new BetaClearToolUses20250919Edit
            {
                Trigger = new BetaInputTokensTrigger { Value = 30000 },
                Keep = new BetaToolUsesKeep { Value = 5 }
            }
        ]
    }
};

var response = await client.Beta.Messages.CountTokens(parameters);

Console.WriteLine($"Original tokens: {response.ContextManagement?.OriginalInputTokens}");
Console.WriteLine($"After clearing: {response.InputTokens}");
Console.WriteLine($"Savings: {(response.ContextManagement?.OriginalInputTokens ?? 0) - response.InputTokens} tokens");
```

```go Go hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.CountTokens(context.TODO(), anthropic.BetaMessageCountTokensParams{
		Model: anthropic.ModelClaudeOpus4_7,
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
}
```

```java Java hidelines={1..2,10..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMessageTokensCount;
import com.anthropic.models.beta.messages.MessageCountTokensParams;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
import com.anthropic.models.beta.messages.BetaInputTokensTrigger;
import com.anthropic.models.beta.messages.BetaToolUsesKeep;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class TokenCountExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCountTokensParams params = MessageCountTokensParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
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

        System.out.println("Original tokens: " + response.contextManagement().get().originalInputTokens());
        System.out.println("After clearing: " + response.inputTokens());
        System.out.println("Savings: " + (response.contextManagement().get().originalInputTokens() - response.inputTokens()) + " tokens");
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->countTokens(
    messages: [
        ['role' => 'user', 'content' => 'Continue our conversation...']
    ],
    model: 'claude-opus-4-7',
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

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.count_tokens(
  model: "claude-opus-4-7",
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

Respons menunjukkan baik jumlah token akhir setelah manajemen konteks diterapkan (`input_tokens`) dan jumlah token asli sebelum pembersihan apa pun terjadi (`original_input_tokens`).

## Menggunakan dengan Alat Memory

Pengeditan konteks dapat digabungkan dengan [alat memory](/docs/id/agents-and-tools/tool-use/memory-tool). Ketika konteks percakapan Anda mendekati ambang batas pembersihan yang dikonfigurasi, Claude menerima peringatan otomatis untuk menyimpan informasi penting. Ini memungkinkan Claude untuk menyimpan hasil alat atau konteks ke file memory sebelum dihapus dari riwayat percakapan.

Kombinasi ini memungkinkan Anda untuk:

- **Menyimpan konteks penting**: Claude dapat menulis informasi penting dari hasil alat ke file memory sebelum hasil tersebut dihapus
- **Mempertahankan alur kerja jangka panjang**: Mengaktifkan alur kerja agentic yang sebaliknya akan melampaui batas konteks dengan memindahkan informasi ke penyimpanan persisten
- **Mengakses informasi sesuai permintaan**: Claude dapat mencari informasi yang sebelumnya dihapus dari file memory saat diperlukan, daripada menyimpan semuanya di jendela konteks aktif

Misalnya, dalam alur kerja pengeditan file di mana Claude melakukan banyak operasi, Claude dapat merangkum perubahan yang selesai ke file memory saat konteks berkembang. Ketika hasil alat dihapus, Claude mempertahankan akses ke informasi tersebut melalui sistem memory dan dapat terus bekerja secara efektif.

Untuk menggunakan kedua fitur bersama-sama, aktifkan keduanya dalam permintaan API Anda:

<CodeGroup>

```bash CLI
ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
model: claude-opus-4-7
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

```python Python nocheck
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[...],
    tools=[
        {"type": "memory_20250818", "name": "memory"},
        # Your other tools
    ],
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
)
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4096,
  messages: [
    // ...
  ],
  tools: [
    {
      type: "memory_20250818",
      name: "memory"
    }
    // Your other tools
  ],
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [{ type: "clear_tool_uses_20250919" }]
  }
});
```

```csharp C# nocheck
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
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 4096,
            Messages = [],
            Tools = [
                new() {
                    Type = "memory_20250818",
                    Name = "memory"
                }
            ],
            Betas = ["context-management-2025-06-27"],
            ContextManagement = new BetaContextManagementConfig() {
                Edits = [
                    new BetaClearToolUses20250919Edit()
                ]
            }
        };

        var response = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(response);
    }
}
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 4096,
		Messages:  []anthropic.BetaMessageParam{},
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
}
```

```java Java nocheck hidelines={1..4,9..12,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaMemoryTool20250818;
import com.anthropic.models.beta.messages.BetaContextManagementConfig;
import com.anthropic.models.beta.messages.BetaClearToolUses20250919Edit;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.messages.Model;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(4096L)
            .addTool(BetaMemoryTool20250818.builder().build())
            .addBeta(AnthropicBeta.CONTEXT_MANAGEMENT_2025_06_27)
            .contextManagement(BetaContextManagementConfig.builder()
                .addEdit(BetaClearToolUses20250919Edit.builder().build())
                .build())
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [],
    model: 'claude-opus-4-7',
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

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 4096,
  messages: [
    # ...
  ],
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

Untuk referensi alat memory lengkap termasuk perintah dan contoh, lihat [Alat Memory](/docs/id/agents-and-tools/tool-use/memory-tool).

## Pemadatan sisi klien (SDK)

<Warning>
**Anthropic merekomendasikan pemadatan sisi server daripada pemadatan SDK.** [Pemadatan sisi server](/docs/id/build-with-claude/compaction) menangani manajemen konteks secara otomatis dengan kompleksitas integrasi yang lebih rendah, perhitungan penggunaan token yang lebih baik, dan tanpa batasan sisi klien. Gunakan pemadatan SDK hanya jika Anda secara khusus memerlukan kontrol sisi klien atas proses perangkuman.
</Warning>

<Note>
Pemadatan tersedia di [Python, TypeScript, dan Ruby SDKs](/docs/id/api/client-sdks) saat menggunakan [metode `tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner).
</Note>

Pemadatan adalah fitur SDK yang secara otomatis mengelola konteks percakapan dengan menghasilkan ringkasan ketika penggunaan token tumbuh terlalu besar. Tidak seperti strategi pengeditan konteks sisi server yang menghapus konten, pemadatan menginstruksikan Claude untuk merangkum riwayat percakapan, kemudian mengganti riwayat lengkap dengan ringkasan tersebut. Ini memungkinkan Claude untuk terus bekerja pada tugas jangka panjang yang sebaliknya akan melampaui [jendela konteks](/docs/id/build-with-claude/context-windows).

### Cara kerja pemadatan

Ketika pemadatan diaktifkan, SDK memantau penggunaan token setelah setiap respons model:

1. **Pemeriksaan ambang batas:** SDK menghitung total token sebagai `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`.
2. **Pembuatan ringkasan:** Ketika ambang batas terlampaui, prompt ringkasan disuntikkan sebagai giliran pengguna, dan Claude menghasilkan ringkasan terstruktur yang dibungkus dalam tag `<summary></summary>`.
3. **Penggantian konteks:** SDK mengekstrak ringkasan dan mengganti seluruh riwayat pesan dengannya.
4. **Kelanjutan:** Percakapan dilanjutkan dari ringkasan, dengan Claude melanjutkan dari tempat ia berhenti.

### Menggunakan pemadatan

Tambahkan `compaction_control` ke panggilan `tool_runner` Anda untuk mengaktifkan perangkuman otomatis ketika penggunaan token melampaui ambang batas.

<Tabs>
<Tab title="CLI">

<Note>
CLI tidak menyertakan pembantu `tool_runner`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani pemadatan di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Python">

```python Python hidelines={1..10}
import anthropic
from anthropic import beta_tool


@beta_tool
def read_file(path: str) -> str:
    """Read the contents of a file."""
    return "file contents..."


client = anthropic.Anthropic()

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-7",
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

```typescript TypeScript hidelines={1..15,-3..}
import Anthropic from "@anthropic-ai/sdk";
import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";

const readFile = betaTool({
  name: "read_file",
  description: "Read the contents of a file",
  inputSchema: {
    type: "object",
    properties: { path: { type: "string" } },
    required: ["path"]
  },
  run: async () => "file contents..."
});

async function main() {
  const client = new Anthropic();

  const runner = client.beta.messages.toolRunner({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    tools: [readFile],
    messages: [{ role: "user", content: "What's in config.json?" }],
    compactionControl: { enabled: true, contextTokenThreshold: 100000 }
  });

  for await (const message of runner) {
    console.log(`Tokens used: ${message.usage.input_tokens}`);
  }
}

main();
```

</Tab>
<Tab title="C#">

<Note>
SDK C# tidak menyertakan pembantu `tool_runner`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani pemadatan di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Go">

<Note>
`tool_runner` SDK Go tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani pemadatan di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Java">

<Note>
`tool_runner` SDK Java tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani pemadatan di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="PHP">

<Note>
`tool_runner` SDK PHP tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani pemadatan di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Ruby">

```ruby Ruby hidelines={1..15}
require "anthropic"

class ReadFileInput < Anthropic::BaseModel
  required :path, String, doc: "Path to the file"
end

class ReadFile < Anthropic::BaseTool
  doc "Read the contents of a file"
  input_schema ReadFileInput

  def call(input)
    "file contents..."
  end
end

client = Anthropic::Client.new

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
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

#### Apa yang terjadi selama pemadatan

Seiring percakapan berkembang, riwayat pesan terakumulasi:

**Sebelum pemadatan (mendekati 100k token):**
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

Ketika token melampaui ambang batas, SDK menyuntikkan permintaan ringkasan dan Claude menghasilkan ringkasan. Seluruh riwayat kemudian diganti:

**Setelah pemadatan (kembali ke ~2-3k token):**
```json
[
  {
    "role": "assistant",
    "content": "# Task Overview\nThe user requested analysis of directory files to produce a summary report...\n\n# Current State\nAnalyzed 52 files across 3 subdirectories. Key findings documented in report.md...\n\n# Important Discoveries\n- Configuration files use YAML format\n- Found 3 deprecated dependencies\n- Test coverage at 67%\n\n# Next Steps\n1. Analyze remaining files in /src/legacy\n2. Complete final report sections...\n\n# Context to Preserve\nUser prefers markdown format with executive summary first..."
  }
]
```

Claude melanjutkan bekerja dari ringkasan ini seolah-olah itu adalah riwayat percakapan asli.

### Opsi konfigurasi

| Parameter | Tipe | Diperlukan | Default | Deskripsi |
|-----------|------|----------|---------|-------------|
| `enabled` | boolean | Ya | - | Apakah akan mengaktifkan pemadatan otomatis |
| `context_token_threshold` | number | Tidak | 100,000 | Jumlah token di mana pemadatan dipicu |
| `model` | string | Tidak | Model yang sama dengan model utama | Model yang digunakan untuk menghasilkan ringkasan |
| `summary_prompt` | string | Tidak | Lihat di bawah | Prompt khusus untuk pembuatan ringkasan |

#### Memilih ambang batas token

Ambang batas menentukan kapan pemadatan terjadi. Ambang batas yang lebih rendah berarti pemadatan yang lebih sering dengan jendela konteks yang lebih kecil. Ambang batas yang lebih tinggi memungkinkan lebih banyak konteks tetapi berisiko mencapai batas.

<CodeGroup>

```python Python
# More frequent compaction for memory-constrained scenarios
compaction_control = {"enabled": True, "context_token_threshold": 50000}

# Less frequent compaction when you need more context
compaction_control = {"enabled": True, "context_token_threshold": 150000}
```

```typescript TypeScript hidelines={1,7..9,-1}
const _ = {
  // More frequent compaction for memory-constrained scenarios
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 50000
  }
};

const __ = {
  // Less frequent compaction when you need more context
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 150000
  }
};
```

</CodeGroup>

#### Menggunakan model berbeda untuk ringkasan

Anda dapat menggunakan model yang lebih cepat atau lebih murah untuk menghasilkan ringkasan:

<CodeGroup>

```python Python
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "model": "claude-haiku-4-5",
}
```

```typescript TypeScript hidelines={1,-1}
const _ = {
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 100000,
    model: "claude-haiku-4-5"
  }
};
```

</CodeGroup>

#### Prompt ringkasan khusus

Anda dapat memberikan prompt khusus untuk kebutuhan spesifik domain. Prompt Anda harus menginstruksikan Claude untuk membungkus ringkasannya dalam tag `<summary></summary>`.

<CodeGroup>

```python Python
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "summary_prompt": """Summarize the research conducted so far, including:
- Sources consulted and key findings
- Questions answered and remaining unknowns
- Recommended next steps

Wrap your summary in <summary></summary> tags.""",
}
```

```typescript TypeScript hidelines={1,-1}
const _ = {
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 100000,
    summaryPrompt: `Summarize the research conducted so far, including:
- Sources consulted and key findings
- Questions answered and remaining unknowns
- Recommended next steps

Wrap your summary in <summary></summary> tags.`
  }
};
```

</CodeGroup>

### Prompt ringkasan default

Prompt ringkasan bawaan menginstruksikan Claude untuk membuat ringkasan kelanjutan terstruktur yang mencakup:

1. **Ikhtisar Tugas:** Permintaan inti pengguna, kriteria kesuksesan, dan batasan.
2. **Status Saat Ini:** Apa yang telah selesai, file yang dimodifikasi, dan artefak yang dihasilkan.
3. **Penemuan Penting:** Batasan teknis, keputusan yang dibuat, kesalahan yang diselesaikan, dan pendekatan yang gagal.
4. **Langkah Berikutnya:** Tindakan spesifik yang diperlukan, pemblokir, dan urutan prioritas.
5. **Konteks untuk Dipertahankan:** Preferensi pengguna, detail spesifik domain, dan komitmen yang dibuat.

Struktur ini memungkinkan Claude untuk melanjutkan pekerjaan secara efisien tanpa kehilangan konteks penting atau mengulangi kesalahan.

<section title="Lihat prompt default lengkap">

```text
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

</section>

### Batasan

#### Alat sisi server

<Warning>
Pemadatan memerlukan pertimbangan khusus saat menggunakan alat sisi server seperti [pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool).
</Warning>

Saat menggunakan alat sisi server, SDK mungkin menghitung penggunaan token secara tidak benar, menyebabkan pemadatan dipicu pada waktu yang salah.

Misalnya, setelah operasi pencarian web, respons API mungkin menunjukkan:

```json Output
{
  "usage": {
    "input_tokens": 63000,
    "cache_read_input_tokens": 270000,
    "output_tokens": 1400
  }
}
```

SDK menghitung penggunaan total sebagai 63.000 + 270.000 = 333.000 token. Namun, nilai `cache_read_input_tokens` mencakup pembacaan terakumulasi dari beberapa panggilan API internal yang dibuat oleh alat sisi server, bukan konteks percakapan aktual Anda. Panjang konteks nyata Anda mungkin hanya 63.000 `input_tokens`, tetapi SDK melihat 333k dan memicu pemadatan secara prematur.

**Solusi:**

- Gunakan endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan panjang konteks yang akurat
- Hindari pemadatan saat menggunakan alat sisi server secara ekstensif

#### Kasus tepi penggunaan alat

Ketika SDK memicu pemadatan saat respons penggunaan alat tertunda, ia menghapus blok penggunaan alat dari riwayat pesan sebelum menghasilkan ringkasan. Claude akan mengeluarkan kembali panggilan alat setelah melanjutkan dari ringkasan jika masih diperlukan.

### Memantau pemadatan

Memahami kapan pemadatan dipicu membantu Anda menyetel ambang batas dan memverifikasi perilaku yang diharapkan.

<Tabs>
<Tab title="Python">

SDK Python mencatat peristiwa pemadatan pada tingkat INFO. Aktifkan logger `anthropic.lib.tools`:

```python Python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("anthropic.lib.tools").setLevel(logging.INFO)

# Logs will show:
# INFO: Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
# INFO: Compaction complete. New token usage: 2500
```

</Tab>
<Tab title="TypeScript">

`toolRunner` SDK TypeScript mendukung pemadatan tetapi tidak mencatat peristiwa. Deteksi pemadatan dengan menonton `runner.params.messages.length` menyusut antar putaran:

```typescript TypeScript hidelines={1..25,-3..}
import Anthropic from "@anthropic-ai/sdk";
import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";

const readFile = betaTool({
  name: "read_file",
  description: "Read the contents of a file",
  inputSchema: {
    type: "object",
    properties: { path: { type: "string" } },
    required: ["path"]
  },
  run: async () => "file contents..."
});

async function main() {
  const client = new Anthropic();

  const runner = client.beta.messages.toolRunner({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    tools: [readFile],
    messages: [{ role: "user", content: "What's in config.json?" }],
    compactionControl: { enabled: true, contextTokenThreshold: 100000 }
  });

  let prevMsgCount = 0;
  for await (const message of runner) {
    const currMsgCount = runner.params.messages.length;
    if (currMsgCount < prevMsgCount) {
      console.log(`Compaction occurred: ${prevMsgCount} -> ${currMsgCount} messages`);
      console.log(`Input tokens after compaction: ${message.usage.input_tokens}`);
    }
    prevMsgCount = currMsgCount;
  }
}

main();
```

</Tab>
<Tab title="C#">

<Note>
SDK C# tidak menyertakan pembantu `tool_runner`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Go">

<Note>
`tool_runner` SDK Go tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Java">

<Note>
`tool_runner` SDK Java tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="PHP">

<Note>
`tool_runner` SDK PHP tidak mendukung `compaction_control`. Gunakan [pemadatan sisi server](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Ruby">

SDK Ruby mendukung callback `on_compact:` yang diaktifkan saat pemadatan terjadi. Tambahkan ke konfigurasi `compaction_control` Anda:

```ruby Ruby hidelines={1..15}
require "anthropic"

class ReadFileInput < Anthropic::BaseModel
  required :path, String, doc: "Path to the file"
end

class ReadFile < Anthropic::BaseTool
  doc "Read the contents of a file"
  input_schema ReadFileInput

  def call(input)
    "file contents..."
  end
end

client = Anthropic::Client.new

runner = client.beta.messages.tool_runner(
  model: "claude-opus-4-7",
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

### Kapan menggunakan pemadatan

**Kasus penggunaan yang baik:**

- Tugas agen jangka panjang yang memproses banyak file atau sumber data
- Alur kerja penelitian yang mengumpulkan sejumlah besar informasi
- Tugas multi-langkah dengan kemajuan yang jelas dan terukur
- Tugas yang menghasilkan artefak (file, laporan) yang bertahan di luar percakapan

**Kasus penggunaan yang kurang ideal:**

- Tugas yang memerlukan recall presisi dari detail percakapan awal
- Alur kerja menggunakan alat sisi server secara ekstensif
- Tugas yang perlu mempertahankan status yang tepat di banyak variabel