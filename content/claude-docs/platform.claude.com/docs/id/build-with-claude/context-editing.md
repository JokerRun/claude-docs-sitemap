---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-editing
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 9d5d033ad7058e50b677008fa1618e55c61f124c759dd050cc428094e138372b
---

# Pengeditan konteks

Kelola konteks percakapan secara otomatis seiring pertumbuhannya dengan pengeditan konteks.

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Ikhtisar \{#overview}

<Note>
Untuk sebagian besar kasus penggunaan, [server-side compaction](/docs/id/build-with-claude/compaction) adalah strategi utama untuk mengelola konteks dalam percakapan yang berjalan lama. Strategi di halaman ini berguna untuk skenario spesifik di mana Anda memerlukan kontrol yang lebih terperinci atas konten apa yang dihapus.
</Note>

"Context editing" (pengeditan konteks) memungkinkan Anda menghapus konten tertentu secara selektif dari riwayat percakapan seiring pertumbuhannya. Selain mengoptimalkan biaya dan tetap berada dalam batas, ini tentang secara aktif mengkurasi apa yang dilihat Claude: konteks adalah sumber daya terbatas dengan hasil yang semakin berkurang, dan konten yang tidak relevan menurunkan fokus model. Pengeditan konteks memberi Anda kontrol runtime yang terperinci atas kurasi tersebut. Untuk prinsip yang lebih luas di balik manajemen konteks, lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Halaman ini mencakup:

- **Penghapusan hasil alat** - Paling cocok untuk alur kerja agentik dengan penggunaan alat yang intensif di mana hasil alat lama tidak lagi diperlukan
- **Penghapusan blok pemikiran** - Untuk mengelola blok pemikiran saat menggunakan pemikiran diperpanjang, dengan opsi untuk mempertahankan pemikiran terbaru demi kontinuitas konteks
- **Compaction SDK sisi klien** - Alternatif berbasis SDK untuk manajemen konteks berbasis ringkasan (server-side compaction umumnya lebih disarankan)

| Pendekatan | Di mana dijalankan | Strategi | Cara kerja |
|----------|---------------|------------|--------------|
| **Sisi server** | API | Penghapusan hasil alat (`clear_tool_uses_20250919`)<br/>Penghapusan blok pemikiran (`clear_thinking_20251015`) | Diterapkan sebelum prompt mencapai Claude. Menghapus konten tertentu dari riwayat percakapan. Setiap strategi dapat dikonfigurasi secara independen. |
| **Sisi klien** | SDK | Compaction | Tersedia di [SDK Python, TypeScript, dan Ruby](/docs/id/cli-sdks-libraries/overview) saat menggunakan [`tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner). Menghasilkan ringkasan dan menggantikan seluruh riwayat percakapan. Lihat [Compaction sisi klien](#client-side-compaction-sdk). |

## Strategi sisi server \{#server-side-strategies}

<Note>
Pengeditan konteks masih dalam tahap beta dengan dukungan untuk penghapusan hasil alat dan penghapusan blok pemikiran. Untuk mengaktifkannya, gunakan header beta `context-management-2025-06-27` dalam permintaan API Anda.

Bagikan masukan tentang fitur ini melalui [formulir masukan](https://forms.gle/YXC2EKGMhjN1c4L88).
</Note>

### Penghapusan hasil alat \{#tool-result-clearing}

Strategi `clear_tool_uses_20250919` menghapus hasil alat ketika konteks percakapan tumbuh melampaui ambang batas yang Anda konfigurasikan. Ini sangat berguna untuk alur kerja agentik dengan penggunaan alat yang intensif. Hasil alat yang lebih lama (seperti konten file atau hasil pencarian) tidak lagi diperlukan setelah Claude memprosesnya.

Saat diaktifkan, API secara otomatis menghapus hasil alat tertua dalam urutan kronologis. API mengganti setiap hasil yang dihapus dengan teks placeholder sehingga Claude mengetahui bahwa hasil tersebut telah dihapus. Secara default, hanya hasil alat yang dihapus. Anda dapat secara opsional menghapus hasil alat sekaligus panggilan alat (parameter penggunaan alat) dengan mengatur `clear_tool_inputs` ke true.

### Penghapusan blok pemikiran \{#thinking-block-clearing}

Strategi `clear_thinking_20251015` mengelola blok `thinking` dalam percakapan ketika pemikiran diperpanjang diaktifkan. Strategi ini memberi Anda kontrol atas preservasi pemikiran: Anda dapat memilih untuk menyimpan lebih banyak blok pemikiran guna mempertahankan kontinuitas penalaran, atau menghapusnya secara lebih agresif untuk menghemat ruang konteks.

<Tip>
**Perilaku default:** Default bervariasi berdasarkan kelas model.

| Kelas model | Simpan semua pemikiran sebelumnya | Simpan hanya pemikiran dari giliran terakhir |
| --- | --- | --- |
| Opus | Claude Opus 4.5 dan yang lebih baru | Claude Opus 4.1 (tidak digunakan lagi) dan yang lebih lama |
| Sonnet | Claude Sonnet 4.6 dan yang lebih baru | Claude Sonnet 4.5 dan yang lebih lama |
| Haiku | (tidak ada) | Semua model hingga Claude Haiku 4.5 |

Gunakan strategi ini untuk menimpa default. Jika kode Anda berjalan di beberapa tingkatan model, atur `keep` secara eksplisit daripada mengandalkan default per-model.
</Tip>

Satu giliran percakapan asisten dapat mencakup beberapa blok konten (misalnya, saat menggunakan alat) dan beberapa blok pemikiran (misalnya, dengan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking)).

### Pengeditan konteks terjadi di sisi server \{#context-editing-happens-server-side}

Pengeditan konteks diterapkan di sisi server sebelum prompt mencapai Claude. Aplikasi klien Anda mempertahankan riwayat percakapan lengkap yang tidak dimodifikasi. Anda tidak perlu menyinkronkan state klien Anda dengan versi yang telah diedit. Lanjutkan mengelola riwayat percakapan lengkap Anda secara lokal seperti biasa.

### Pengeditan konteks dan caching prompt \{#context-editing-and-prompt-caching}

Interaksi pengeditan konteks dengan [caching prompt](/docs/id/build-with-claude/prompt-caching) bervariasi berdasarkan strategi:

- **Penghapusan hasil alat**: Membatalkan prefiks prompt yang di-cache ketika konten dihapus. Untuk mengatasi hal ini, hapus token dalam jumlah yang cukup agar pembatalan cache menjadi sepadan. Gunakan parameter `clear_at_least` untuk memastikan jumlah minimum token dihapus setiap kali. Anda akan dikenakan biaya penulisan cache setiap kali konten dihapus, tetapi permintaan berikutnya dapat menggunakan kembali prefiks yang baru di-cache.

- **Penghapusan blok pemikiran**: Ketika blok pemikiran **disimpan** dalam konteks (tidak dihapus), cache prompt dipertahankan, memungkinkan cache hit dan mengurangi biaya token input. Ketika blok pemikiran **dihapus**, cache dibatalkan pada titik di mana penghapusan terjadi. Konfigurasikan parameter `keep` berdasarkan apakah Anda ingin memprioritaskan performa cache atau ketersediaan jendela konteks.

## Model yang didukung \{#supported-models}

Pengeditan konteks tersedia di semua model Claude yang didukung.

## Penggunaan penghapusan hasil alat \{#tool-result-clearing-usage}

Cara paling sederhana untuk mengaktifkan penghapusan hasil alat adalah dengan hanya menentukan tipe strategi. Semua [opsi konfigurasi](#configuration-options-for-tool-result-clearing) lainnya menggunakan nilai default:

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

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

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

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Beta.Messages;

AnthropicClient client = new();

var parameters = new MessageCreateParams
{
    Model = "claude-opus-4-8",
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

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

```ruby Ruby hidelines={1..2}
require "anthropic"

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

### Konfigurasi lanjutan \{#advanced-configuration}

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
                # Picu pembersihan ketika ambang batas terlampaui
                "trigger": {"type": "input_tokens", "value": 30000},
                # Jumlah penggunaan alat yang dipertahankan setelah pembersihan
                "keep": {"type": "tool_uses", "value": 3},
                # Opsional: Bersihkan setidaknya sejumlah token ini
                "clear_at_least": {"type": "input_tokens", "value": 5000},
                # Kecualikan alat-alat ini dari pembersihan
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
        // Picu pembersihan ketika ambang batas terlampaui
        trigger: {
          type: "input_tokens",
          value: 30000
        },
        // Jumlah penggunaan alat yang dipertahankan setelah pembersihan
        keep: {
          type: "tool_uses",
          value: 3
        },
        // Opsional: Bersihkan setidaknya sejumlah token ini
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
            Model = "claude-opus-4-8",
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
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->beta->messages->create(
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

echo $message;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

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

## Penggunaan penghapusan blok pemikiran \{#thinking-block-clearing-usage}

Aktifkan penghapusan blok pemikiran untuk mengelola konteks dan caching prompt secara efektif ketika pemikiran diperpanjang diaktifkan:

<CodeGroup>

```bash cURL
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

$client = new Client();

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

### Opsi konfigurasi untuk penghapusan blok pemikiran \{#configuration-options-for-thinking-block-clearing}

Strategi `clear_thinking_20251015` mendukung konfigurasi berikut:

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `keep` | Spesifik per model | Menentukan berapa banyak giliran asisten terbaru dengan blok pemikiran yang akan dipertahankan. Gunakan `{type: "thinking_turns", value: N}` di mana N harus > 0 untuk menyimpan N giliran terakhir, atau `"all"` untuk menyimpan semua blok pemikiran. Opus 4.5+ dan Sonnet 4.6+: semua giliran. Opus/Sonnet yang lebih lama dan semua Haiku: hanya giliran terakhir. |

**Contoh konfigurasi:**

Simpan blok pemikiran dari 3 giliran asisten terakhir:

```json
{
  "type": "clear_thinking_20251015",
  "keep": {
    "type": "thinking_turns",
    "value": 3
  }
}
```

Simpan semua blok pemikiran (memaksimalkan cache hit):

```json
{
  "type": "clear_thinking_20251015",
  "keep": "all"
}
```

### Menggabungkan strategi \{#combining-strategies}

Anda dapat menggunakan penghapusan blok pemikiran dan penghapusan hasil alat secara bersamaan:

<Note>
Saat menggunakan beberapa strategi, strategi `clear_thinking_20251015` harus dicantumkan terlebih dahulu dalam array `edits`.
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

$client = new Client();

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

## Opsi konfigurasi untuk penghapusan hasil alat \{#configuration-options-for-tool-result-clearing}

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `trigger` | 100.000 token input | Menentukan kapan strategi pengeditan konteks diaktifkan. Setelah prompt melebihi ambang batas ini, penghapusan akan dimulai. Anda dapat menentukan nilai ini dalam `input_tokens` atau `tool_uses`. |
| `keep` | 3 penggunaan alat | Menentukan berapa banyak pasangan penggunaan/hasil alat terbaru yang akan disimpan setelah penghapusan terjadi. API menghapus interaksi alat tertua terlebih dahulu, mempertahankan yang terbaru. |
| `clear_at_least` | Tidak ada | Memastikan jumlah minimum token dihapus setiap kali strategi diaktifkan. Jika API tidak dapat menghapus setidaknya jumlah yang ditentukan, strategi tidak akan diterapkan. Ini membantu menentukan apakah penghapusan konteks sepadan dengan rusaknya cache prompt Anda. |
| `exclude_tools` | Tidak ada | Daftar nama alat yang penggunaan dan hasilnya tidak boleh dihapus. Berguna untuk mempertahankan konteks penting. |
| `clear_tool_inputs` | `false` | Mengontrol apakah parameter panggilan alat dihapus bersama dengan hasil alat. Secara default, hanya hasil alat yang dihapus sementara panggilan alat asli Claude tetap terlihat. |

## Respons pengeditan konteks \{#context-editing-response}

Anda dapat melihat pengeditan konteks mana yang diterapkan pada permintaan Anda menggunakan field respons `context_management`, beserta statistik berguna tentang konten dan token input yang dihapus.

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

Untuk respons streaming, pengeditan konteks akan disertakan dalam event `message_delta` terakhir:

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

## Penghitungan token \{#token-counting}

Endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) mendukung manajemen konteks, memungkinkan Anda melihat pratinjau berapa banyak token yang akan digunakan prompt Anda setelah pengeditan konteks diterapkan.

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
model: claude-opus-4-8
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
  --raw-output < request.yaml)

INPUT_TOKENS=$(ant beta:messages count-tokens \
  --beta context-management-2025-06-27 \
  --transform input_tokens --raw-output < request.yaml)

printf 'Original tokens: %s\n' "$ORIGINAL"
printf 'After clearing: %s\n' "$INPUT_TOKENS"
printf 'Savings: %s tokens\n' "$((ORIGINAL - INPUT_TOKENS))"
```

```python Python nocheck
response = client.beta.messages.count_tokens(
    model="claude-opus-4-8",
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
  model: "claude-opus-4-8",
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
    Model = "claude-opus-4-8",
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

        System.out.println("Original tokens: " + response.contextManagement().get().originalInputTokens());
        System.out.println("After clearing: " + response.inputTokens());
        System.out.println("Savings: " + (response.contextManagement().get().originalInputTokens() - response.inputTokens()) + " tokens");
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

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

```ruby Ruby hidelines={1..2}
require "anthropic"

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

Respons menunjukkan jumlah token akhir setelah manajemen konteks diterapkan (`input_tokens`) dan jumlah token asli sebelum penghapusan apa pun terjadi (`original_input_tokens`).

## Menggunakan dengan alat memori \{#using-with-the-memory-tool}

Pengeditan konteks dapat dikombinasikan dengan [alat memori](/docs/id/agents-and-tools/tool-use/memory-tool). Ketika konteks percakapan Anda mendekati ambang batas penghapusan yang dikonfigurasi, Claude menerima peringatan otomatis untuk menyimpan informasi penting. Ini memungkinkan Claude menyimpan hasil alat atau konteks ke file memorinya sebelum dihapus dari riwayat percakapan.

Kombinasi ini memungkinkan Anda untuk:

- **Mempertahankan konteks penting**: Claude dapat menulis informasi esensial dari hasil alat ke file memori sebelum hasil tersebut dihapus
- **Mempertahankan alur kerja yang berjalan lama**: Memungkinkan alur kerja agentik yang seharusnya melebihi batas konteks dengan memindahkan informasi ke penyimpanan persisten
- **Mengakses informasi sesuai kebutuhan**: Claude dapat mencari informasi yang sebelumnya dihapus dari file memori saat diperlukan, daripada menyimpan semuanya di jendela konteks aktif

Misalnya, dalam alur kerja pengeditan file di mana Claude melakukan banyak operasi, Claude dapat meringkas perubahan yang telah diselesaikan ke file memori seiring pertumbuhan konteks. Ketika hasil alat dihapus, Claude tetap memiliki akses ke informasi tersebut melalui sistem memorinya dan dapat terus bekerja secara efektif.

Untuk menggunakan kedua fitur secara bersamaan, aktifkan keduanya dalam permintaan API Anda:

<CodeGroup>

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

```python Python nocheck
response = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    messages=[...],
    tools=[
        {"type": "memory_20250818", "name": "memory"},
        # Alat Anda yang lain
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
  model: "claude-opus-4-8",
  max_tokens: 4096,
  messages: [
    // ...
  ],
  tools: [
    {
      type: "memory_20250818",
      name: "memory"
    }
    // Alat Anda lainnya
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
            Model = Model.ClaudeOpus4_8,
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
		Model:     anthropic.ModelClaudeOpus4_8,
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
            .model(Model.CLAUDE_OPUS_4_8)
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

$client = new Client();

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [],
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

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-8",
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

Untuk referensi lengkap alat memori termasuk perintah dan contoh, lihat [Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool).

## Compaction sisi klien (SDK) \{#client-side-compaction-sdk}

<Warning>
**Anthropic merekomendasikan server-side compaction dibandingkan SDK compaction.** [Server-side compaction](/docs/id/build-with-claude/compaction) menangani manajemen konteks secara otomatis dengan kompleksitas integrasi yang lebih rendah, perhitungan penggunaan token yang lebih baik, dan tanpa keterbatasan sisi klien. Gunakan SDK compaction hanya jika Anda secara spesifik memerlukan kontrol sisi klien atas proses peringkasan.
</Warning>

<Note>
Compaction tersedia di [SDK Python, TypeScript, dan Ruby](/docs/id/cli-sdks-libraries/overview) saat menggunakan [metode `tool_runner`](/docs/id/agents-and-tools/tool-use/tool-runner).
</Note>

"Compaction" (pemadatan) adalah fitur SDK yang secara otomatis mengelola konteks percakapan dengan menghasilkan ringkasan ketika penggunaan token tumbuh terlalu besar. Tidak seperti strategi pengeditan konteks sisi server yang menghapus konten, compaction menginstruksikan Claude untuk meringkas riwayat percakapan, lalu mengganti seluruh riwayat dengan ringkasan tersebut. Ini memungkinkan Claude untuk terus mengerjakan tugas yang berjalan lama yang seharusnya melebihi [jendela konteks](/docs/id/build-with-claude/context-windows).

### Cara kerja compaction \{#how-compaction-works}

Ketika compaction diaktifkan, SDK memantau penggunaan token setelah setiap respons model:

1. **Pemeriksaan ambang batas:** SDK menghitung total token sebagai `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`.
2. **Pembuatan ringkasan:** Ketika ambang batas terlampaui, prompt ringkasan disisipkan sebagai giliran pengguna, dan Claude menghasilkan ringkasan terstruktur yang dibungkus dalam tag `<summary></summary>`.
3. **Penggantian konteks:** SDK mengekstrak ringkasan dan mengganti seluruh riwayat pesan dengannya.
4. **Kelanjutan:** Percakapan dilanjutkan dari ringkasan, dengan Claude melanjutkan dari titik terakhir.

### Menggunakan compaction \{#using-compaction}

Tambahkan `compaction_control` ke panggilan `tool_runner` Anda untuk mengaktifkan peringkasan otomatis ketika penggunaan token melebihi ambang batas.

<Tabs>
<Tab title="CLI">

<Note>
CLI tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
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

```typescript TypeScript hidelines={1..14}
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
SDK C# tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Go">

<Note>
SDK Go tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="Java">

<Note>
SDK Java tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
</Note>

</Tab>
<Tab title="PHP">

<Note>
SDK PHP tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya, yang menangani compaction di server Anthropic tanpa integrasi sisi SDK.
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

#### Apa yang terjadi selama compaction \{#what-happens-during-compaction}

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

Ketika token melebihi ambang batas, SDK menyisipkan permintaan ringkasan dan Claude menghasilkan ringkasan. Seluruh riwayat kemudian diganti:

**Setelah compaction (kembali ke ~2-3k token):**
```json
[
  {
    "role": "assistant",
    "content": "# Task Overview\nThe user requested analysis of directory files to produce a summary report...\n\n# Current State\nAnalyzed 52 files across 3 subdirectories. Key findings documented in report.md...\n\n# Important Discoveries\n- Configuration files use YAML format\n- Found 3 deprecated dependencies\n- Test coverage at 67%\n\n# Next Steps\n1. Analyze remaining files in /src/legacy\n2. Complete final report sections...\n\n# Context to Preserve\nUser prefers markdown format with executive summary first..."
  }
]
```

Claude melanjutkan pekerjaan dari ringkasan ini seolah-olah itu adalah riwayat percakapan asli.

### Opsi konfigurasi \{#configuration-options}

| Parameter | Tipe | Wajib | Default | Deskripsi |
|-----------|------|----------|---------|-------------|
| `enabled` | boolean | Ya | - | Apakah akan mengaktifkan compaction otomatis |
| `context_token_threshold` | number | Tidak | 100.000 | Jumlah token di mana compaction dipicu |
| `model` | string | Tidak | Sama dengan model utama | Model yang digunakan untuk menghasilkan ringkasan |
| `summary_prompt` | string | Tidak | Lihat di bawah | Prompt kustom untuk pembuatan ringkasan |

#### Memilih ambang batas token \{#choosing-a-token-threshold}

Ambang batas menentukan kapan compaction terjadi. Ambang batas yang lebih rendah berarti compaction lebih sering dengan jendela konteks yang lebih kecil. Ambang batas yang lebih tinggi memungkinkan lebih banyak konteks tetapi berisiko mencapai batas.

<CodeGroup>

```python Python
# Pemadatan lebih sering untuk skenario dengan memori terbatas
compaction_control = {"enabled": True, "context_token_threshold": 50000}

# Pemadatan lebih jarang ketika Anda membutuhkan lebih banyak konteks
compaction_control = {"enabled": True, "context_token_threshold": 150000}
```

```typescript TypeScript hidelines={1,7..9,-1}
const _ = {
  // Pemadatan lebih sering untuk skenario dengan keterbatasan memori
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 50000
  }
};

const __ = {
  // Pemadatan lebih jarang ketika Anda membutuhkan lebih banyak konteks
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 150000
  }
};
```

</CodeGroup>

#### Menggunakan model berbeda untuk ringkasan \{#using-a-different-model-for-summaries}

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

#### Prompt ringkasan kustom \{#custom-summary-prompts}

Anda dapat menyediakan prompt kustom untuk kebutuhan spesifik domain. Prompt Anda harus menginstruksikan Claude untuk membungkus ringkasannya dalam tag `<summary></summary>`.

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

### Prompt ringkasan default \{#default-summary-prompt}

Prompt ringkasan bawaan menginstruksikan Claude untuk membuat ringkasan kelanjutan terstruktur yang mencakup:

1. **Ikhtisar Tugas:** Permintaan inti pengguna, kriteria keberhasilan, dan batasan.
2. **Status Saat Ini:** Apa yang telah diselesaikan, file yang dimodifikasi, dan artefak yang dihasilkan.
3. **Penemuan Penting:** Batasan teknis, keputusan yang dibuat, kesalahan yang diselesaikan, dan pendekatan yang gagal.
4. **Langkah Selanjutnya:** Tindakan spesifik yang diperlukan, hambatan, dan urutan prioritas.
5. **Konteks yang Perlu Dipertahankan:** Preferensi pengguna, detail spesifik domain, dan komitmen yang dibuat.

Struktur ini memungkinkan Claude melanjutkan pekerjaan secara efisien tanpa kehilangan konteks penting atau mengulangi kesalahan.

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

### Keterbatasan \{#limitations}

#### Alat sisi server \{#server-side-tools}

<Warning>
Compaction memerlukan pertimbangan khusus saat menggunakan alat sisi server seperti [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool).
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

- Gunakan endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan panjang konteks yang akurat
- Hindari compaction saat menggunakan alat sisi server secara ekstensif

#### Kasus khusus penggunaan alat \{#tool-use-edge-cases}

Ketika SDK memicu compaction saat respons penggunaan alat masih tertunda, SDK menghapus blok penggunaan alat dari riwayat pesan sebelum menghasilkan ringkasan. Claude akan mengeluarkan kembali panggilan alat setelah melanjutkan dari ringkasan jika masih diperlukan.

### Memantau compaction \{#monitoring-compaction}

Memahami kapan compaction dipicu membantu Anda menyesuaikan ambang batas dan memverifikasi perilaku yang diharapkan.

<Tabs>
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

```typescript TypeScript hidelines={1..24}
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

const client = new Anthropic();

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-8",
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
```

</Tab>
<Tab title="C#">

<Note>
SDK C# tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Go">

<Note>
SDK Go tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Java">

<Note>
SDK Java tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="PHP">

<Note>
SDK PHP tidak menyertakan helper `tool_runner`. Gunakan [server-side compaction](/docs/id/build-with-claude/compaction) sebagai gantinya.
</Note>

</Tab>
<Tab title="Ruby">

SDK Ruby mendukung callback `on_compact:` yang dipicu ketika compaction terjadi. Tambahkan ke konfigurasi `compaction_control` Anda:

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

### Kapan menggunakan compaction \{#when-to-use-compaction}

**Kasus penggunaan yang cocok:**

- Tugas agen yang berjalan lama yang memproses banyak file atau sumber data
- Alur kerja riset yang mengakumulasi informasi dalam jumlah besar
- Tugas multi-langkah dengan kemajuan yang jelas dan terukur
- Tugas yang menghasilkan artefak (file, laporan) yang bertahan di luar percakapan

**Kasus penggunaan yang kurang ideal:**

- Tugas yang memerlukan pengingatan presisi atas detail percakapan awal
- Alur kerja yang menggunakan alat sisi server secara ekstensif
- Tugas yang perlu mempertahankan state yang tepat di banyak variabel