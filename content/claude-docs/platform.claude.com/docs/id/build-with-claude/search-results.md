---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/search-results
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: c9373265af3c78352b761ed19dcb25c20200f6695fe280b3129fe2e5f698fc56
---

# Hasil pencarian

Aktifkan kutipan alami untuk aplikasi RAG dengan menyediakan hasil pencarian dengan atribusi sumber

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Blok konten hasil pencarian memungkinkan kutipan alami dengan atribusi sumber yang tepat, membawa kutipan berkualitas pencarian web ke aplikasi kustom Anda. Fitur ini sangat kuat untuk aplikasi RAG (Retrieval-Augmented Generation) di mana Anda perlu Claude mengutip sumber dengan akurat.

Fitur hasil pencarian tersedia pada model berikut:

- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations)) (`claude-3-7-sonnet-20250219`)
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations)) (`claude-3-5-haiku-20241022`)

## Manfaat utama

- **Kutipan alami** - Capai kualitas kutipan yang sama seperti pencarian web untuk konten apa pun
- **Integrasi fleksibel** - Gunakan dalam pengembalian alat untuk RAG dinamis atau sebagai konten tingkat atas untuk data yang telah diambil sebelumnya
- **Atribusi sumber yang tepat** - Setiap hasil mencakup informasi sumber dan judul untuk atribusi yang jelas
- **Tidak perlu solusi berbasis dokumen** - Menghilangkan kebutuhan akan solusi berbasis dokumen
- **Format kutipan yang konsisten** - Cocok dengan kualitas dan format kutipan dari fungsi pencarian web Claude

## Cara kerjanya

Hasil pencarian dapat disediakan dalam dua cara:

1. **Dari panggilan alat** - Alat kustom Anda mengembalikan hasil pencarian, memungkinkan aplikasi RAG dinamis
2. **Sebagai konten tingkat atas** - Anda menyediakan hasil pencarian langsung dalam pesan pengguna untuk konten yang telah diambil sebelumnya atau di-cache

Dalam kedua kasus, Claude dapat secara otomatis mengutip informasi dari hasil pencarian dengan atribusi sumber yang tepat.

### Skema hasil pencarian

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

### Bidang yang diperlukan

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Harus `"search_result"` |
| `source` | string | URL sumber atau pengenal untuk konten |
| `title` | string | Judul deskriptif untuk hasil pencarian |
| `content` | array | Larik blok teks yang berisi konten sebenarnya |

### Bidang opsional

| Field | Type | Description |
|-------|------|-------------|
| `citations` | object | Konfigurasi kutipan dengan bidang boolean `enabled` |
| `cache_control` | object | Pengaturan kontrol cache (misalnya, `{"type": "ephemeral"}`) |

Setiap item dalam larik `content` harus berupa blok teks dengan:
- `type`: Harus `"text"`
- `text`: Konten teks sebenarnya (string tidak kosong)

## Metode 1: Hasil pencarian dari panggilan alat

Kasus penggunaan paling kuat adalah mengembalikan hasil pencarian dari alat kustom Anda. Ini memungkinkan aplikasi RAG dinamis di mana alat mengambil dan mengembalikan konten yang relevan dengan kutipan otomatis.

### Contoh: Alat basis pengetahuan

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

# Define a knowledge base search tool
knowledge_base_tool = {
    "name": "search_knowledge_base",
    "description": "Search the company knowledge base for information",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "The search query"}},
        "required": ["query"],
    },
}


# Function to handle the tool call
def search_knowledge_base(query):
    # Your search logic here
    # Returns search results in the correct format
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


# Create a message with the tool
response = client.messages.create(
    model="claude-opus-4-6",  # Works with all supported models
    max_tokens=1024,
    tools=[knowledge_base_tool],
    messages=[
        MessageParam(role="user", content="How do I configure the timeout settings?")
    ],
)

# When Claude calls the tool, provide the search results
if response.content[0].type == "tool_use":
    tool_result = search_knowledge_base(response.content[0].input["query"])

    # Send the tool result back
    final_response = client.messages.create(
        model="claude-opus-4-6",  # Works with all supported models
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

// Define a knowledge base search tool
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

// Function to handle the tool call
function searchKnowledgeBase(query: string) {
  // Your search logic here
  // Returns search results in the correct format
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

// Create a message with the tool
const response = await anthropic.messages.create({
  model: "claude-opus-4-6", // Works with all supported models
  max_tokens: 1024,
  tools: [knowledgeBaseTool],
  messages: [
    {
      role: "user",
      content: "How do I configure the timeout settings?"
    }
  ]
});

// Handle tool use and provide results
if (response.content[0].type === "tool_use") {
  const input = response.content[0].input as { query: string };
  const toolResult = searchKnowledgeBase(input.query);

  const finalResponse = await anthropic.messages.create({
    model: "claude-opus-4-6", // Works with all supported models
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
            Model = Model.ClaudeOpus4_6,
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
                Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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

			// Build assistant message from the response
			assistantParam := response.ToParam()

			finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
				Model:     anthropic.ModelClaudeOpus4_6,
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
            .model(Model.CLAUDE_OPUS_4_6)
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
                .model(Model.CLAUDE_OPUS_4_6)
                .maxTokens(1024L)
                .addTool(knowledgeBaseTool)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
    model: 'claude-opus-4-6',
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
        model: 'claude-opus-4-6',
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
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [knowledge_base_tool],
  messages: [
    { role: "user", content: "How do I configure the timeout settings?" }
  ]
)

if response.content.first.type == :tool_use
  tool_result = search_knowledge_base(response.content.first.input["query"])

  final_response = client.messages.create(
    model: "claude-opus-4-6",
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

## Metode 2: Hasil pencarian sebagai konten tingkat atas

Anda juga dapat menyediakan hasil pencarian langsung dalam pesan pengguna. Ini berguna untuk:
- Konten yang telah diambil sebelumnya dari infrastruktur pencarian Anda
- Hasil pencarian yang di-cache dari kueri sebelumnya
- Konten dari layanan pencarian eksternal
- Pengujian dan pengembangan

### Contoh: Hasil pencarian langsung

<CodeGroup>
```bash Shell
#!/bin/sh
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
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
model: claude-opus-4-6
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

# Provide search results directly in the user message
response = client.messages.create(
    model="claude-opus-4-6",
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

print(response.model_dump_json(indent=2))
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

// Provide search results directly in the user message
const response = await anthropic.messages.create({
  model: "claude-opus-4-6",
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
            Model = Model.ClaudeOpus4_6,
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
		Model:     anthropic.ModelClaudeOpus4_6,
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
            .model(Model.CLAUDE_OPUS_4_6)
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

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

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
    model: 'claude-opus-4-6',
);

echo json_encode($message, JSON_PRETTY_PRINT);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-opus-4-6",
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

## Respons Claude dengan kutipan

Terlepas dari bagaimana hasil pencarian disediakan, Claude secara otomatis menyertakan kutipan saat menggunakan informasi dari hasil tersebut:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "To authenticate API requests, you need to include an API key in the Authorization header",
      "citations": [
        {
          "type": "search_result_location",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "cited_text": "All API requests must include an API key in the Authorization header",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 0
        }
      ]
    },
    {
      "type": "text",
      "text": ". You can generate API keys from your dashboard",
      "citations": [
        {
          "type": "search_result_location",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "cited_text": "Keys can be generated from the dashboard",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 0
        }
      ]
    },
    {
      "type": "text",
      "text": ". The rate limits are 1,000 requests per hour for the standard tier and 10,000 requests per hour for the premium tier.",
      "citations": [
        {
          "type": "search_result_location",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "cited_text": "Rate limits: 1000 requests per hour for standard tier, 10000 for premium",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 0
        }
      ]
    }
  ]
}
```

### Bidang kutipan

Setiap kutipan mencakup:

| Bidang | Tipe | Deskripsi |
|-------|------|-------------|
| `type` | string | Selalu `"search_result_location"` untuk kutipan hasil pencarian |
| `source` | string | Sumber dari hasil pencarian asli |
| `title` | string atau null | Judul dari hasil pencarian asli |
| `cited_text` | string | Teks yang tepat sedang dikutip |
| `search_result_index` | integer | Indeks hasil pencarian (berbasis 0) |
| `start_block_index` | integer | Posisi awal dalam array konten |
| `end_block_index` | integer | Posisi akhir dalam array konten |

Catatan: `search_result_index` mengacu pada indeks blok konten hasil pencarian (berbasis 0), terlepas dari bagaimana hasil pencarian disediakan (panggilan alat atau konten tingkat atas).

## Blok konten berganda

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

Claude dapat mengutip blok spesifik menggunakan bidang `start_block_index` dan `end_block_index`.

## Penggunaan lanjutan

### Menggabungkan kedua metode

Anda dapat menggunakan hasil pencarian berbasis alat dan tingkat atas dalam percakapan yang sama:

```python nocheck
from anthropic.types import MessageParam, SearchResultBlockParam, TextBlockParam

# First message with top-level search results
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

# Claude might respond and call a tool to search for pricing
# Then you provide tool results with more search results
```

### Menggabungkan dengan tipe konten lainnya

Kedua metode mendukung pencampuran hasil pencarian dengan konten lainnya:

```python nocheck
from anthropic.types import SearchResultBlockParam, TextBlockParam

# In tool results
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

# In top-level content
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

### Kontrol cache

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

### Kontrol kutipan

Secara default, kutipan dinonaktifkan untuk hasil pencarian. Anda dapat mengaktifkan kutipan dengan secara eksplisit menetapkan konfigurasi `citations`:

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

Ketika `citations.enabled` diatur ke `true`, Claude menyertakan referensi kutipan saat menggunakan informasi dari hasil pencarian. Ini memungkinkan:
- Kutipan alami untuk aplikasi RAG kustom Anda
- Atribusi sumber saat berinteraksi dengan basis pengetahuan proprietary
- Kutipan berkualitas pencarian web untuk alat kustom apa pun yang mengembalikan hasil pencarian

Jika bidang `citations` dihilangkan, kutipan dinonaktifkan secara default.

<Warning>
Kutipan adalah semua-atau-tidak-sama-sekali: baik semua hasil pencarian dalam permintaan harus memiliki kutipan diaktifkan, atau semua harus dinonaktifkan. Mencampur hasil pencarian dengan pengaturan kutipan yang berbeda menghasilkan kesalahan. Jika Anda perlu menonaktifkan kutipan untuk beberapa sumber, Anda harus menonaktifkannya untuk semua hasil pencarian dalam permintaan tersebut.
</Warning>

## Praktik terbaik

### Untuk pencarian berbasis alat (Metode 1)

- **Konten dinamis:** Gunakan untuk pencarian real-time dan aplikasi RAG dinamis
- **Penanganan kesalahan:** Kembalikan pesan yang sesuai ketika pencarian gagal
- **Batas hasil:** Kembalikan hanya hasil yang paling relevan untuk menghindari overflow konteks

### Untuk pencarian tingkat atas (Metode 2)

- **Konten yang sudah diambil:** Gunakan ketika Anda sudah memiliki hasil pencarian
- **Pemrosesan batch:** Ideal untuk memproses beberapa hasil pencarian sekaligus
- **Pengujian:** Bagus untuk menguji perilaku kutipan dengan konten yang diketahui

### Praktik terbaik umum

1. **Struktur hasil secara efektif**
   - Gunakan URL sumber yang jelas dan permanen
   - Berikan judul deskriptif
   - Pisahkan konten panjang menjadi blok teks logis

2. **Pertahankan konsistensi**
   - Gunakan format sumber yang konsisten di seluruh aplikasi Anda
   - Pastikan judul secara akurat mencerminkan konten
   - Pertahankan pemformatan yang konsisten

3. **Tangani kesalahan dengan baik**
   
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

## Keterbatasan

- Blok konten hasil pencarian tersedia di Claude API, Amazon Bedrock, dan Google Cloud's Vertex AI
- Hanya konten teks yang didukung dalam hasil pencarian (tidak ada gambar atau media lainnya)
- Array `content` harus berisi setidaknya satu blok teks