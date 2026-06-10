---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/search-results
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 5fd82d688647236d0be767d2be2cb658d8143fb8b22444d7091fedbd69a17b7e
---

# Hasil pencarian

Aktifkan sitasi alami untuk aplikasi RAG dengan menyediakan hasil pencarian beserta atribusi sumber

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Blok konten hasil pencarian memungkinkan sitasi alami dengan atribusi sumber yang tepat, menghadirkan sitasi berkualitas setara pencarian web ke aplikasi kustom Anda. Fitur ini sangat berguna untuk aplikasi "RAG" (Retrieval-Augmented Generation) di mana Anda membutuhkan Claude untuk mengutip sumber secara akurat.

Fitur hasil pencarian tersedia pada model-model berikut:

- Claude Opus 4.8 (claude-opus-4-8)
- Claude Opus 4.7 (`claude-opus-4-7`)
- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) (`claude-opus-4-1-20250805`)
- Claude Opus 4 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) (`claude-opus-4-20250514`)
- Claude Sonnet 4 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)) (`claude-sonnet-4-20250514`)
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- Claude Haiku 3.5 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)) (`claude-3-5-haiku-20241022`)

## Manfaat utama \{#key-benefits}

- **Sitasi alami:** Mencapai kualitas sitasi yang sama seperti pencarian web untuk konten apa pun
- **Integrasi fleksibel:** Gunakan dalam hasil pengembalian alat untuk RAG dinamis atau sebagai konten tingkat atas untuk data yang telah diambil sebelumnya
- **Atribusi sumber yang tepat:** Setiap hasil menyertakan informasi sumber dan judul untuk atribusi yang jelas
- **Tidak perlu solusi alternatif berbasis dokumen:** Menghilangkan kebutuhan akan solusi alternatif berbasis dokumen
- **Format sitasi yang konsisten:** Sesuai dengan kualitas dan format sitasi dari fungsionalitas pencarian web Claude

## Cara kerjanya \{#how-it-works}

Hasil pencarian dapat disediakan dengan dua cara:

1. **Dari pemanggilan alat:** Alat kustom Anda mengembalikan hasil pencarian, memungkinkan aplikasi RAG dinamis
2. **Sebagai konten tingkat atas:** Anda menyediakan hasil pencarian secara langsung dalam pesan pengguna untuk konten yang telah diambil sebelumnya atau di-cache

Dalam kedua kasus tersebut, Claude dapat secara otomatis mengutip informasi dari hasil pencarian dengan atribusi sumber yang tepat.

### Skema hasil pencarian \{#search-result-schema}

Hasil pencarian menggunakan struktur berikut:

```json
{
  "type": "search_result",
  "source": "https://example.com/article", // Required: Source URL or identifier
  "title": "Article Title", // Required: Title of the result
  "content": [
    // Required: Array of text blocks
    {
      "type": "text",
      "text": "The actual content of the search result..."
    }
  ],
  "citations": {
    // Optional: Citation configuration
    "enabled": true // Enable/disable citations for this result
  }
}
```

### Field wajib \{#required-fields}

| Field | Tipe | Deskripsi |
|-------|------|-------------|
| `type` | string | Harus berupa `"search_result"` |
| `source` | string | URL sumber atau pengidentifikasi untuk konten |
| `title` | string | Judul deskriptif untuk hasil pencarian |
| `content` | array | Array blok teks yang berisi konten sebenarnya |

### Field opsional \{#optional-fields}

| Field | Tipe | Deskripsi |
|-------|------|-------------|
| `citations` | object | Konfigurasi sitasi dengan field boolean `enabled` |
| `cache_control` | object | Pengaturan kontrol cache (misalnya, `{"type": "ephemeral"}`) |

Setiap item dalam array `content` harus berupa blok teks dengan:
- `type`: Harus berupa `"text"`
- `text`: Konten teks sebenarnya (string yang tidak kosong)

## Metode 1: Hasil pencarian dari pemanggilan alat \{#method-1-search-results-from-tool-calls}

Kasus penggunaan yang paling kuat adalah mengembalikan hasil pencarian dari alat kustom Anda. Ini memungkinkan aplikasi RAG dinamis di mana alat mengambil dan mengembalikan konten yang relevan dengan sitasi otomatis.

### Contoh: Alat basis pengetahuan \{#example-knowledge-base-tool}

<CodeGroup>

```python Python nocheck hidelines={1}
from anthropic import Anthropic
from anthropic.types import (
    MessageParam,
    TextBlockParam,
    SearchResultBlockParam,
    ToolResultBlockParam,
)

client = Anthropic()

# Definisikan alat pencarian basis pengetahuan
knowledge_base_tool = {
    "name": "search_knowledge_base",
    "description": "Search the company knowledge base for information",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "The search query"}},
        "required": ["query"],
    },
}


# Fungsi untuk menangani panggilan alat
def search_knowledge_base(query):
    # Logika pencarian Anda di sini
    # Mengembalikan hasil pencarian dalam format yang benar
    return [
        SearchResultBlockParam(
            type="search_result",
            source="https://docs.company.com/product-guide",
            title="Product Configuration Guide",
            content=[
                TextBlockParam(
                    type="text",
                    text="To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.",
                )
            ],
            citations={"enabled": True},
        ),
        SearchResultBlockParam(
            type="search_result",
            source="https://docs.company.com/troubleshooting",
            title="Troubleshooting Guide",
            content=[
                TextBlockParam(
                    type="text",
                    text="If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.",
                )
            ],
            citations={"enabled": True},
        ),
    ]


# Buat pesan dengan alat tersebut
response = client.messages.create(
    model="claude-opus-4-8",  # Works with all supported models
    max_tokens=1024,
    tools=[knowledge_base_tool],
    messages=[
        MessageParam(role="user", content="How do I configure the timeout settings?")
    ],
)

# Ketika Claude memanggil alat, berikan hasil pencarian
if response.content[0].type == "tool_use":
    tool_result = search_knowledge_base(response.content[0].input["query"])

    # Kirim kembali hasil alat
    final_response = client.messages.create(
        model="claude-opus-4-8",  # Works with all supported models
        max_tokens=1024,
        messages=[
            MessageParam(
                role="user", content="How do I configure the timeout settings?"
            ),
            MessageParam(role="assistant", content=response.content),
            MessageParam(
                role="user",
                content=[
                    ToolResultBlockParam(
                        type="tool_result",
                        tool_use_id=response.content[0].id,
                        content=tool_result,  # Search results go here
                    )
                ],
            ),
        ],
    )
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Definisikan alat pencarian basis pengetahuan
const knowledgeBaseTool: Anthropic.Messages.Tool = {
  name: "search_knowledge_base",
  description: "Search the company knowledge base for information",
  input_schema: {
    type: "object" as const,
    properties: {
      query: {
        type: "string",
        description: "The search query"
      }
    },
    required: ["query"]
  }
};

// Fungsi untuk menangani pemanggilan alat
function searchKnowledgeBase(query: string) {
  // Logika pencarian Anda di sini
  // Mengembalikan hasil pencarian dalam format yang benar
  return [
    {
      type: "search_result" as const,
      source: "https://docs.company.com/product-guide",
      title: "Product Configuration Guide",
      content: [
        {
          type: "text" as const,
          text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
        }
      ],
      citations: { enabled: true }
    },
    {
      type: "search_result" as const,
      source: "https://docs.company.com/troubleshooting",
      title: "Troubleshooting Guide",
      content: [
        {
          type: "text" as const,
          text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
        }
      ],
      citations: { enabled: true }
    }
  ];
}

// Buat pesan dengan alat tersebut
const response = await anthropic.messages.create({
  model: "claude-opus-4-8", // Works with all supported models
  max_tokens: 1024,
  tools: [knowledgeBaseTool],
  messages: [
    {
      role: "user",
      content: "How do I configure the timeout settings?"
    }
  ]
});

// Tangani penggunaan alat dan berikan hasilnya
if (response.content[0].type === "tool_use") {
  const input = response.content[0].input as { query: string };
  const toolResult = searchKnowledgeBase(input.query);

  const finalResponse = await anthropic.messages.create({
    model: "claude-opus-4-8", // Works with all supported models
    max_tokens: 1024,
    messages: [
      { role: "user", content: "How do I configure the timeout settings?" },
      { role: "assistant", content: response.content },
      {
        role: "user",
        content: [
          {
            type: "tool_result" as const,
            tool_use_id: response.content[0].id,
            content: toolResult // Search results go here
          }
        ]
      }
    ]
  });
}
```

```csharp C# nocheck
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var knowledgeBaseTool = new Tool
        {
            Name = "search_knowledge_base",
            Description = "Search the company knowledge base for information",
            InputSchema = new
            {
                type = "object",
                properties = new
                {
                    query = new
                    {
                        type = "string",
                        description = "The search query"
                    }
                },
                required = new[] { "query" }
            }
        };

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1024,
            Tools = new[] { knowledgeBaseTool },
            Messages = new[]
            {
                new MessageParam
                {
                    Role = Role.User,
                    Content = "How do I configure the timeout settings?"
                }
            }
        };

        var response = await client.Messages.Create(parameters);

        if (response.Content[0] is ToolUseBlock toolUse)
        {
            var toolResult = SearchKnowledgeBase(toolUse.Input["query"].ToString());

            var finalParameters = new MessageCreateParams
            {
                Model = Model.ClaudeOpus4_8,
                MaxTokens = 1024,
                Messages = new[]
                {
                    new MessageParam { Role = Role.User, Content = "How do I configure the timeout settings?" },
                    new MessageParam { Role = Role.Assistant, Content = response.Content },
                    new MessageParam
                    {
                        Role = Role.User,
                        Content = new[]
                        {
                            new ToolResultBlockParam
                            {
                                ToolUseID = toolUse.Id,
                                Content = toolResult
                            }
                        }
                    }
                }
            };

            var finalResponse = await client.Messages.Create(finalParameters);
            Console.WriteLine(finalResponse);
        }
    }

    private static List<SearchResultBlockParam> SearchKnowledgeBase(string query)
    {
        return new List<SearchResultBlockParam>
        {
            new SearchResultBlockParam
            {
                Source = "https://docs.company.com/product-guide",
                Title = "Product Configuration Guide",
                Content = new[]
                {
                    new TextBlockParam
                    {
                        Text = "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
                    }
                },
                Citations = new CitationsConfigParam { Enabled = true }
            },
            new SearchResultBlockParam
            {
                Source = "https://docs.company.com/troubleshooting",
                Title = "Troubleshooting Guide",
                Content = new[]
                {
                    new TextBlockParam
                    {
                        Text = "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
                    }
                },
                Citations = new CitationsConfigParam { Enabled = true }
            }
        };
    }
}
```

```go Go nocheck hidelines={1..12,77..78}
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	knowledgeBaseTool := anthropic.ToolUnionParam{
		OfTool: &anthropic.ToolParam{
			Name:        "search_knowledge_base",
			Description: anthropic.String("Search the company knowledge base for information"),
			InputSchema: anthropic.ToolInputSchemaParam{
				Properties: map[string]any{
					"query": map[string]any{
						"type":        "string",
						"description": "The search query",
					},
				},
				Required: []string{"query"},
			},
		},
	}

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools:     []anthropic.ToolUnionParam{knowledgeBaseTool},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.ToolUseBlock:
			var input struct {
				Query string `json:"query"`
			}
			if err := json.Unmarshal(variant.Input, &input); err != nil {
				log.Fatal(err)
			}
			toolResults := searchKnowledgeBase(input.Query)

			// Bangun pesan asisten dari respons
			assistantParam := response.ToParam()

			finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
				Model:     anthropic.ModelClaudeOpus4_8,
				MaxTokens: 1024,
				Messages: []anthropic.MessageParam{
					anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
					assistantParam,
					anthropic.NewUserMessage(anthropic.ContentBlockParamUnion{
						OfToolResult: &anthropic.ToolResultBlockParam{
							ToolUseID: variant.ID,
							Content:   toolResults,
						},
					}),
				},
			})
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println(finalResponse)
		}
	}
}

func searchKnowledgeBase(query string) []anthropic.ToolResultBlockParamContentUnion {
	return []anthropic.ToolResultBlockParamContentUnion{
		{OfSearchResult: &anthropic.SearchResultBlockParam{
			Content: []anthropic.TextBlockParam{
				{Text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."},
			},
			Source:    "https://docs.company.com/product-guide",
			Title:     "Product Configuration Guide",
			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
		}},
		{OfSearchResult: &anthropic.SearchResultBlockParam{
			Content: []anthropic.TextBlockParam{
				{Text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."},
			},
			Source:    "https://docs.company.com/troubleshooting",
			Title:     "Troubleshooting Guide",
			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
		}},
	}
}
```

```java Java nocheck hidelines={1..3,5..7,9..19,75..76,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.CitationsConfigParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.SearchResultBlockParam;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlock;
import com.anthropic.models.messages.ToolUseBlockParam;
import com.anthropic.core.JsonValue;
import java.util.List;
import java.util.Map;

public class SearchKnowledgeBaseExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        Tool knowledgeBaseTool = Tool.builder()
            .name("search_knowledge_base")
            .description("Search the company knowledge base for information")
            .inputSchema(Tool.InputSchema.builder()
                .properties(JsonValue.from(Map.of(
                    "query", Map.of(
                        "type", "string",
                        "description", "The search query"
                    )
                )))
                .putAdditionalProperty("required", JsonValue.from(List.of("query")))
                .build())
            .build();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addTool(knowledgeBaseTool)
            .addUserMessage("How do I configure the timeout settings?")
            .build();

        Message response = client.messages().create(params);

        response.content().get(0).toolUse().ifPresent(toolUse -> {
            List<ContentBlockParam> toolResult = searchKnowledgeBase(
                (String) ((Map<?, ?>) toolUse._input()).get("query")
            );

            MessageCreateParams finalParams = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024L)
                .addUserMessage("How do I configure the timeout settings?")
                .addAssistantMessageOfBlockParams(List.of(
                    ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                        .id(toolUse.id())
                        .name(toolUse.name())
                        .input(toolUse._input())
                        .build())
                ))
                .addUserMessageOfBlockParams(List.of(
                    ContentBlockParam.ofToolResult(
                        ToolResultBlockParam.builder()
                            .toolUseId(toolUse.id())
                            .contentOfBlockParams(toolResult)
                            .build()
                    )
                ))
                .build();

            Message finalResponse = client.messages().create(finalParams);
            System.out.println(finalResponse);
        });
    }

    private static List<ContentBlockParam> searchKnowledgeBase(String query) {
        return List.of(
            ContentBlockParam.ofSearchResult(
                SearchResultBlockParam.builder()
                    .source("https://docs.company.com/product-guide")
                    .title("Product Configuration Guide")
                    .content(List.of(
                        TextBlockParam.builder()
                            .text("To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.")
                            .build()
                    ))
                    .citations(CitationsConfigParam.builder().enabled(true).build())
                    .build()
            ),
            ContentBlockParam.ofSearchResult(
                SearchResultBlockParam.builder()
                    .source("https://docs.company.com/troubleshooting")
                    .title("Troubleshooting Guide")
                    .content(List.of(
                        TextBlockParam.builder()
                            .text("If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.")
                            .build()
                    ))
                    .citations(CitationsConfigParam.builder().enabled(true).build())
                    .build()
            )
        );
    }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$knowledgeBaseTool = [
    'name' => 'search_knowledge_base',
    'description' => 'Search the company knowledge base for information',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'query' => [
                'type' => 'string',
                'description' => 'The search query'
            ]
        ],
        'required' => ['query']
    ]
];

function searchKnowledgeBase($query) {
    return [
        [
            'type' => 'search_result',
            'source' => 'https://docs.company.com/product-guide',
            'title' => 'Product Configuration Guide',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.'
                ]
            ],
            'citations' => ['enabled' => true]
        ],
        [
            'type' => 'search_result',
            'source' => 'https://docs.company.com/troubleshooting',
            'title' => 'Troubleshooting Guide',
            'content' => [
                [
                    'type' => 'text',
                    'text' => 'If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.'
                ]
            ],
            'citations' => ['enabled' => true]
        ]
    ];
}

$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'How do I configure the timeout settings?']
    ],
    model: 'claude-opus-4-8',
    tools: [$knowledgeBaseTool],
);

$toolUseBlock = null;
foreach ($response->content as $block) {
    if ($block->type === 'tool_use') {
        $toolUseBlock = $block;
        break;
    }
}

if ($toolUseBlock !== null) {
    $toolResult = searchKnowledgeBase($toolUseBlock->input['query']);

    $finalResponse = $client->messages->create(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'How do I configure the timeout settings?'],
            ['role' => 'assistant', 'content' => $response->content],
            [
                'role' => 'user',
                'content' => [
                    [
                        'type' => 'tool_result',
                        'tool_use_id' => $toolUseBlock->id,
                        'content' => $toolResult
                    ]
                ]
            ]
        ],
        model: 'claude-opus-4-8',
    );
    echo $finalResponse;
} else {
    echo $response;
}
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

knowledge_base_tool = {
  name: "search_knowledge_base",
  description: "Search the company knowledge base for information",
  input_schema: {
    type: "object",
    properties: {
      query: { type: "string", description: "The search query" }
    },
    required: ["query"]
  }
}

def search_knowledge_base(query)
  [
    {
      type: "search_result",
      source: "https://docs.company.com/product-guide",
      title: "Product Configuration Guide",
      content: [
        {
          type: "text",
          text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
        }
      ],
      citations: { enabled: true }
    },
    {
      type: "search_result",
      source: "https://docs.company.com/troubleshooting",
      title: "Troubleshooting Guide",
      content: [
        {
          type: "text",
          text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
        }
      ],
      citations: { enabled: true }
    }
  ]
end

response = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [knowledge_base_tool],
  messages: [
    { role: "user", content: "How do I configure the timeout settings?" }
  ]
)

if response.content.first.type == :tool_use
  tool_result = search_knowledge_base(response.content.first.input["query"])

  final_response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "How do I configure the timeout settings?" },
      { role: "assistant", content: response.content },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: response.content.first.id,
            content: tool_result
          }
        ]
      }
    ]
  )
  puts final_response
end
```
</CodeGroup>

## Metode 2: Hasil pencarian sebagai konten tingkat atas \{#method-2-search-results-as-top-level-content}

Anda juga dapat menyediakan hasil pencarian secara langsung dalam pesan pengguna. Ini berguna untuk:
- Konten yang telah diambil sebelumnya dari infrastruktur pencarian Anda
- Hasil pencarian yang di-cache dari kueri sebelumnya
- Konten dari layanan pencarian eksternal
- Pengujian dan pengembangan

### Contoh: Hasil pencarian langsung \{#example-direct-search-results}

<CodeGroup>
```bash cURL
#!/bin/sh
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "search_result",
                    "source": "https://docs.company.com/api-reference",
                    "title": "API Reference - Authentication",
                    "content": [
                        {
                            "type": "text",
                            "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                        }
                    ],
                    "citations": {
                        "enabled": true
                    }
                },
                {
                    "type": "search_result",
                    "source": "https://docs.company.com/quickstart",
                    "title": "Getting Started Guide",
                    "content": [
                        {
                            "type": "text",
                            "text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                        }
                    ],
                    "citations": {
                        "enabled": true
                    }
                },
                {
                    "type": "text",
                    "text": "Based on these search results, how do I authenticate API requests and what are the rate limits?"
                }
            ]
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content:
      - type: search_result
        source: https://docs.company.com/api-reference
        title: API Reference - Authentication
        content:
          - type: text
            text: >-
              All API requests must include an API key in the Authorization
              header. Keys can be generated from the dashboard. Rate limits:
              1000 requests per hour for standard tier, 10000 for premium.
        citations:
          enabled: true
      - type: search_result
        source: https://docs.company.com/quickstart
        title: Getting Started Guide
        content:
          - type: text
            text: >-
              To get started: 1) Sign up for an account, 2) Generate an API
              key from the dashboard, 3) Install our SDK using pip install
              company-sdk, 4) Initialize the client with your API key.
        citations:
          enabled: true
      - type: text
        text: >-
          Based on these search results, how do I authenticate API requests
          and what are the rate limits?
YAML
```

```python Python hidelines={1}
from anthropic import Anthropic
from anthropic.types import MessageParam, TextBlockParam, SearchResultBlockParam

client = Anthropic()

# Berikan hasil pencarian langsung dalam pesan pengguna
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        MessageParam(
            role="user",
            content=[
                SearchResultBlockParam(
                    type="search_result",
                    source="https://docs.company.com/api-reference",
                    title="API Reference - Authentication",
                    content=[
                        TextBlockParam(
                            type="text",
                            text="All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
                        )
                    ],
                    citations={"enabled": True},
                ),
                SearchResultBlockParam(
                    type="search_result",
                    source="https://docs.company.com/quickstart",
                    title="Getting Started Guide",
                    content=[
                        TextBlockParam(
                            type="text",
                            text="To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
                        )
                    ],
                    citations={"enabled": True},
                ),
                TextBlockParam(
                    type="text",
                    text="Based on these search results, how do I authenticate API requests and what are the rate limits?",
                ),
            ],
        )
    ],
)

print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Berikan hasil pencarian langsung dalam pesan pengguna
const response = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "search_result" as const,
          source: "https://docs.company.com/api-reference",
          title: "API Reference - Authentication",
          content: [
            {
              type: "text" as const,
              text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
            }
          ],
          citations: { enabled: true }
        },
        {
          type: "search_result" as const,
          source: "https://docs.company.com/quickstart",
          title: "Getting Started Guide",
          content: [
            {
              type: "text" as const,
              text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
            }
          ],
          citations: { enabled: true }
        },
        {
          type: "text" as const,
          text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
        }
      ]
    }
  ]
});

console.log(response);
```

```csharp C# nocheck
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
            MaxTokens = 1024,
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content =
                    [
                        new SearchResultBlockParam
                        {
                            Source = "https://docs.company.com/api-reference",
                            Title = "API Reference - Authentication",
                            Content =
                            [
                                new TextBlockParam
                                {
                                    Text = "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                                }
                            ],
                            Citations = new CitationsConfigParam { Enabled = true }
                        },
                        new SearchResultBlockParam
                        {
                            Source = "https://docs.company.com/quickstart",
                            Title = "Getting Started Guide",
                            Content =
                            [
                                new TextBlockParam
                                {
                                    Text = "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                                }
                            ],
                            Citations = new CitationsConfigParam { Enabled = true }
                        },
                        new TextBlockParam
                        {
                            Text = "Based on these search results, how do I authenticate API requests and what are the rate limits?"
                        }
                    ]
                }
            ]
        };

        var message = await client.Messages.Create(parameters);
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(
				anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
					Content: []anthropic.TextBlockParam{
						{Text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."},
					},
					Source:    "https://docs.company.com/api-reference",
					Title:     "API Reference - Authentication",
					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
				}},
				anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
					Content: []anthropic.TextBlockParam{
						{Text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."},
					},
					Source:    "https://docs.company.com/quickstart",
					Title:     "Getting Started Guide",
					Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
				}},
				anthropic.NewTextBlock("Based on these search results, how do I authenticate API requests and what are the rate limits?"),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..3,5..7,9..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.CitationsConfigParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.SearchResultBlockParam;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class SearchResultExample {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024L)
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofSearchResult(
                    SearchResultBlockParam.builder()
                        .source("https://docs.company.com/api-reference")
                        .title("API Reference - Authentication")
                        .content(List.of(
                            TextBlockParam.builder()
                                .text("All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.")
                                .build()
                        ))
                        .citations(CitationsConfigParam.builder().enabled(true).build())
                        .build()
                ),
                ContentBlockParam.ofSearchResult(
                    SearchResultBlockParam.builder()
                        .source("https://docs.company.com/quickstart")
                        .title("Getting Started Guide")
                        .content(List.of(
                            TextBlockParam.builder()
                                .text("To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.")
                                .build()
                        ))
                        .citations(CitationsConfigParam.builder().enabled(true).build())
                        .build()
                ),
                ContentBlockParam.ofText(
                    TextBlockParam.builder()
                        .text("Based on these search results, how do I authenticate API requests and what are the rate limits?")
                        .build()
                )
            ))
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$message = $client->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'search_result',
                    'source' => 'https://docs.company.com/api-reference',
                    'title' => 'API Reference - Authentication',
                    'content' => [
                        [
                            'type' => 'text',
                            'text' => 'All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.'
                        ]
                    ],
                    'citations' => ['enabled' => true]
                ],
                [
                    'type' => 'search_result',
                    'source' => 'https://docs.company.com/quickstart',
                    'title' => 'Getting Started Guide',
                    'content' => [
                        [
                            'type' => 'text',
                            'text' => 'To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.'
                        ]
                    ],
                    'citations' => ['enabled' => true]
                ],
                [
                    'type' => 'text',
                    'text' => 'Based on these search results, how do I authenticate API requests and what are the rate limits?'
                ]
            ]
        ]
    ],
    model: 'claude-opus-4-8',
);

echo json_encode($message, JSON_PRETTY_PRINT);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "search_result",
          source: "https://docs.company.com/api-reference",
          title: "API Reference - Authentication",
          content: [
            {
              type: "text",
              text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
            }
          ],
          citations: { enabled: true }
        },
        {
          type: "search_result",
          source: "https://docs.company.com/quickstart",
          title: "Getting Started Guide",
          content: [
            {
              type: "text",
              text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
            }
          ],
          citations: { enabled: true }
        },
        {
          type: "text",
          text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
        }
      ]
    }
  ]
)

puts message
```
</CodeGroup>

## Respons Claude dengan sitasi \{#claudes-response-with-citations}

Terlepas dari bagaimana hasil pencarian disediakan, Claude secara otomatis menyertakan sitasi saat menggunakan informasi dari hasil tersebut:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    },
    {
      "type": "text",
      "text": "\n\nTo set this up from scratch, you'll need to "
    },
    {
      "type": "text",
      "text": "sign up for an account, generate an API key from the dashboard, install the SDK using `pip install company-sdk`, and initialize the client with your API key.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
          "source": "https://docs.company.com/quickstart",
          "title": "Getting Started Guide",
          "search_result_index": 1,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    }
  ]
}
```

### Field sitasi \{#citation-fields}

Setiap sitasi mencakup:

| Field | Tipe | Deskripsi |
|-------|------|-------------|
| `type` | string | Selalu `"search_result_location"` untuk sitasi hasil pencarian |
| `source` | string | Sumber dari hasil pencarian asli |
| `title` | string atau null | Judul dari hasil pencarian asli |
| `cited_text` | string | Teks lengkap dari blok yang dikutip, digabungkan. Sama dengan isi dari `content[start_block_index:end_block_index]` yang digabungkan bersama. Tidak dihitung terhadap token output. |
| `search_result_index` | integer | Indeks berbasis 0 dari hasil pencarian yang dikutip di antara semua blok `search_result` dalam permintaan, sesuai urutan kemunculannya (di seluruh pesan dan hasil alat). |
| `start_block_index` | integer | Indeks berbasis 0 dari blok pertama yang dikutip dalam array `content` hasil pencarian. |
| `end_block_index` | integer | Indeks akhir eksklusif dari rentang blok yang dikutip dalam array `content` hasil pencarian. Selalu lebih besar dari `start_block_index`. |

Indeks blok mengidentifikasi potongan dari array `content` hasil pencarian, dan `cited_text` adalah teks lengkap dari potongan tersebut. Blok teks adalah unit terkecil yang dapat dikutip: Claude mengutip seluruh blok, bukan substring di dalam sebuah blok. Untuk mendapatkan sitasi yang lebih terperinci, pisahkan konten hasil pencarian Anda menjadi blok-blok yang lebih kecil (lihat [Beberapa blok konten](#multiple-content-blocks)).

## Beberapa blok konten \{#multiple-content-blocks}

Hasil pencarian dapat berisi beberapa blok teks dalam array `content`:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "content": [
    {
      "type": "text",
      "text": "Authentication: All API requests require an API key."
    },
    {
      "type": "text",
      "text": "Rate Limits: The API allows 1000 requests per hour per key."
    },
    {
      "type": "text",
      "text": "Error Handling: The API returns standard HTTP status codes."
    }
  ]
}
```

Sitasi yang mereferensikan blok batas laju terlihat seperti ini:

```json
{
  "type": "search_result_location",
  "cited_text": "Rate Limits: The API allows 1000 requests per hour per key.",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "search_result_index": 0,
  "start_block_index": 1,
  "end_block_index": 2
}
```

Ketika hasil pencarian ini dikutip, `start_block_index` dan `end_block_index` mengidentifikasi blok mana dari blok-blok ini yang dicakup oleh sitasi, dan `cited_text` berisi persis teks dari blok-blok tersebut. Memisahkan konten menjadi blok-blok yang lebih kecil dan terfokus memberi Claude batas sitasi yang lebih terperinci; menggabungkan konten menjadi satu blok berarti setiap sitasi mengembalikan teks lengkap. Ini adalah model yang sama yang digunakan oleh [dokumen konten kustom](/docs/id/build-with-claude/citations#custom-content-documents) dalam fitur Citations.

## Penggunaan lanjutan \{#advanced-usage}

### Menggabungkan kedua metode \{#combining-both-methods}

Anda dapat menggunakan hasil pencarian berbasis alat dan tingkat atas dalam percakapan yang sama:

```python nocheck
from anthropic.types import MessageParam, SearchResultBlockParam, TextBlockParam

# Pesan pertama dengan hasil pencarian tingkat atas
messages = [
    MessageParam(
        role="user",
        content=[
            SearchResultBlockParam(
                type="search_result",
                source="https://docs.company.com/overview",
                title="Product Overview",
                content=[
                    TextBlockParam(
                        type="text", text="Our product helps teams collaborate..."
                    )
                ],
                citations={"enabled": True},
            ),
            TextBlockParam(
                type="text",
                text="Tell me about this product and search for pricing information",
            ),
        ],
    )
]

# Claude mungkin merespons dan memanggil alat untuk mencari harga
# Kemudian Anda memberikan hasil alat dengan lebih banyak hasil pencarian
```

### Menggabungkan dengan tipe konten lain \{#combining-with-other-content-types}

Kedua metode mendukung pencampuran hasil pencarian dengan konten lain:

```python nocheck
from anthropic.types import SearchResultBlockParam, TextBlockParam

# Dalam hasil alat
tool_result = [
    SearchResultBlockParam(
        type="search_result",
        source="https://docs.company.com/guide",
        title="User Guide",
        content=[TextBlockParam(type="text", text="Configuration details...")],
        citations={"enabled": True},
    ),
    TextBlockParam(
        type="text", text="Additional context: This applies to version 2.0 and later."
    ),
]

# Dalam konten tingkat atas
user_content = [
    SearchResultBlockParam(
        type="search_result",
        source="https://research.com/paper",
        title="Research Paper",
        content=[TextBlockParam(type="text", text="Key findings...")],
        citations={"enabled": True},
    ),
    {
        "type": "image",
        "source": {"type": "url", "url": "https://example.com/chart.png"},
    },
    TextBlockParam(
        type="text", text="How does the chart relate to the research findings?"
    ),
]
```

### Kontrol cache \{#cache-control}

Tambahkan kontrol cache untuk performa yang lebih baik:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "..." }],
  "cache_control": {
    "type": "ephemeral"
  }
}
```

### Kontrol sitasi \{#citation-control}

Secara default, sitasi dinonaktifkan untuk hasil pencarian. Anda dapat mengaktifkan sitasi dengan secara eksplisit mengatur konfigurasi `citations`:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "Important documentation..." }],
  "citations": {
    "enabled": true // Enable citations for this result
  }
}
```

Ketika `citations.enabled` diatur ke `true`, Claude menyertakan referensi sitasi saat menggunakan informasi dari hasil pencarian. Ini memungkinkan:
- Sitasi alami untuk aplikasi RAG kustom Anda
- Atribusi sumber saat berinteraksi dengan basis pengetahuan proprietary
- Sitasi berkualitas setara pencarian web untuk alat kustom apa pun yang mengembalikan hasil pencarian

<Warning>
Sitasi bersifat semua-atau-tidak-sama-sekali: semua hasil pencarian dalam sebuah permintaan harus mengaktifkan sitasi, atau semuanya harus menonaktifkannya. Mencampur hasil pencarian dengan pengaturan sitasi yang berbeda akan menghasilkan error.
</Warning>

## Praktik terbaik \{#best-practices}

### Untuk pencarian berbasis alat (Metode 1) \{#for-tool-based-search-method-1}

- **Konten dinamis:** Gunakan untuk pencarian real-time dan aplikasi RAG dinamis
- **Penanganan error:** Kembalikan pesan yang sesuai ketika pencarian gagal
- **Batas hasil:** Kembalikan hanya hasil yang paling relevan untuk menghindari konteks yang meluap

### Untuk pencarian tingkat atas (Metode 2) \{#for-top-level-search-method-2}

- **Konten yang telah diambil sebelumnya:** Gunakan ketika Anda sudah memiliki hasil pencarian
- **Pemrosesan batch:** Ideal untuk memproses beberapa hasil pencarian sekaligus
- **Pengujian:** Sangat baik untuk menguji perilaku sitasi dengan konten yang diketahui

### Praktik terbaik umum \{#general-best-practices}

1. **Strukturkan hasil secara efektif:**
   - Gunakan URL sumber yang jelas dan permanen
   - Berikan judul yang deskriptif
   - Pecah konten panjang menjadi blok teks yang logis untuk memberi Claude batas sitasi yang lebih terperinci

2. **Jaga konsistensi:**
   - Gunakan format sumber yang konsisten di seluruh aplikasi Anda
   - Pastikan judul secara akurat mencerminkan konten
   - Jaga format tetap konsisten

3. **Tangani error dengan baik:**
   
   ```python nocheck
   def search_with_fallback(query):
       try:
           results = perform_search(query)
           if not results:
               return {"type": "text", "text": "No results found."}
           return format_as_search_results(results)
       except Exception as e:
           return {"type": "text", "text": f"Search error: {str(e)}"}
   ```

## Batasan \{#limitations}

- Blok konten hasil pencarian tersedia di Claude API, Amazon Bedrock, dan Vertex AI dari Google Cloud
- Hanya konten teks yang didukung dalam hasil pencarian (tidak ada gambar atau media lainnya)
- Array `content` harus berisi setidaknya satu blok teks