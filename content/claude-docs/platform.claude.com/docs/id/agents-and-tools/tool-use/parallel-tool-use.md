---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/parallel-tool-use
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 55cbd5988e9dfdb18ee59362963692081adbc83360679cd1ab9968530144cd6f
---

# Penggunaan alat paralel

Aktifkan dan format panggilan alat paralel, dengan panduan riwayat pesan dan pemecahan masalah.

---

Halaman ini mencakup panggilan alat paralel: ketika Claude memanggil beberapa alat dalam satu giliran, cara memformat riwayat pesan sehingga paralelisme terus berfungsi, dan cara menonaktifkannya. Untuk alur panggilan tunggal, lihat [Handle tool calls](/docs/id/agents-and-tools/tool-use/handle-tool-calls).

Secara default, Claude dapat menggunakan beberapa alat untuk menjawab pertanyaan pengguna. Anda dapat menonaktifkan perilaku ini dengan:

- Mengatur `disable_parallel_tool_use=true` ketika tipe tool_choice adalah `auto`, yang memastikan bahwa Claude menggunakan **paling banyak satu** alat
- Mengatur `disable_parallel_tool_use=true` ketika tipe tool_choice adalah `any` atau `tool`, yang memastikan bahwa Claude menggunakan **tepat satu** alat

## Contoh yang dikerjakan

<Note>
**Lebih Sederhana dengan Tool Runner**: Contoh di bawah menunjukkan penanganan alat paralel manual. Untuk sebagian besar kasus penggunaan, [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner) secara otomatis menangani eksekusi alat paralel dengan kode yang jauh lebih sedikit.
</Note>

Berikut adalah skrip lengkap yang dapat dijalankan untuk menguji dan memverifikasi bahwa panggilan alat paralel berfungsi dengan benar:

<CodeGroup>
```python Python hidelines={1..9}
#!/usr/bin/env python3
"""Test script to verify parallel tool calls with the Claude API"""

import os
from anthropic import Anthropic

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_time",
        "description": "Get the current time in a given timezone",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone, e.g. America/New_York",
                }
            },
            "required": ["timezone"],
        },
    },
]

# Test conversation with parallel tool calls
messages = [
    {
        "role": "user",
        "content": "What's the weather in SF and NYC, and what time is it there?",
    }
]

# Make initial request
print("Requesting parallel tool calls...")
response = client.messages.create(
    model="claude-opus-4-7", max_tokens=1024, messages=messages, tools=tools
)

# Check for parallel tool calls
tool_uses = [block for block in response.content if block.type == "tool_use"]
print(f"\n✓ Claude made {len(tool_uses)} tool calls")

if len(tool_uses) > 1:
    print("✓ Parallel tool calls detected!")
    for tool in tool_uses:
        print(f"  - {tool.name}: {tool.input}")
else:
    print("✗ No parallel tool calls detected")

# Simulate tool execution and format results correctly
tool_results = []
for tool_use in tool_uses:
    if tool_use.name == "get_weather":
        if "San Francisco" in str(tool_use.input):
            result = "San Francisco: 68°F, partly cloudy"
        else:
            result = "New York: 45°F, clear skies"
    else:  # get_time
        if "Los_Angeles" in str(tool_use.input):
            result = "2:30 PM PST"
        else:
            result = "5:30 PM EST"

    tool_results.append(
        {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
    )

# Continue conversation with tool results
messages.extend(
    [
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": tool_results},  # All results in one message!
    ]
)

# Get final response
print("\nGetting final response...")
final_response = client.messages.create(
    model="claude-opus-4-7", max_tokens=1024, messages=messages, tools=tools
)

print(f"\nClaude's response:\n{final_response.content[0].text}")

# Verify formatting
print("\n--- Verification ---")
print(f"✓ Tool results sent in single user message: {len(tool_results)} results")
print("✓ No text before tool results in content array")
print("✓ Conversation formatted correctly for future parallel tool use")
```

```typescript TypeScript hidelines={1..4}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Define tools
const tools: Anthropic.Tool[] = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object" as const,
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  },
  {
    name: "get_time",
    description: "Get the current time in a given timezone",
    input_schema: {
      type: "object" as const,
      properties: {
        timezone: {
          type: "string",
          description: "The timezone, e.g. America/New_York"
        }
      },
      required: ["timezone"]
    }
  }
];

async function testParallelTools() {
  // Make initial request
  console.log("Requesting parallel tool calls...");
  const response = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      }
    ],
    tools: tools
  });

  // Check for parallel tool calls
  const toolUses = response.content.filter((block) => block.type === "tool_use");
  console.log(`\nClaude made ${toolUses.length} tool calls`);

  if (toolUses.length > 1) {
    console.log("Parallel tool calls detected!");
    toolUses.forEach((tool) => {
      if (tool.type === "tool_use") {
        console.log(`  - ${tool.name}: ${JSON.stringify(tool.input)}`);
      }
    });
  }

  // Simulate tool execution and format results correctly
  const toolResults: Anthropic.ToolResultBlockParam[] = toolUses
    .filter((block): block is Anthropic.ToolUseBlock => block.type === "tool_use")
    .map((toolUse) => {
      const input = toolUse.input as Record<string, string>;
      let result: string;
      if (toolUse.name === "get_weather") {
        result = input.location?.includes("San Francisco")
          ? "San Francisco: 68F, partly cloudy"
          : "New York: 45F, clear skies";
      } else {
        result = input.timezone?.includes("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST";
      }

      return {
        type: "tool_result" as const,
        tool_use_id: toolUse.id,
        content: result
      };
    });

  // Get final response with correct formatting
  console.log("\nGetting final response...");
  const finalResponse = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      },
      { role: "assistant", content: response.content },
      { role: "user", content: toolResults }
    ],
    tools: tools
  });

  for (const block of finalResponse.content) {
    if (block.type === "text") {
      console.log(`\nClaude's response:\n${block.text}`);
    }
  }

  // Verify formatting
  console.log("\n--- Verification ---");
  console.log(`Tool results sent in single user message: ${toolResults.length} results`);
}

testParallelTools().catch(console.error);
```

```csharp C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main()
    {
        AnthropicClient client = new();

        var tools = new List<ToolUnion>
        {
            new ToolUnion(new Tool()
            {
                Name = "get_weather",
                Description = "Get the current weather in a given location",
                InputSchema = new InputSchema()
                {
                    Properties = new Dictionary<string, JsonElement>
                    {
                        ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                    },
                    Required = ["location"],
                },
            }),
            new ToolUnion(new Tool()
            {
                Name = "get_time",
                Description = "Get the current time in a given timezone",
                InputSchema = new InputSchema()
                {
                    Properties = new Dictionary<string, JsonElement>
                    {
                        ["timezone"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The timezone, e.g. America/New_York" }),
                    },
                    Required = ["timezone"],
                },
            }),
        };

        Console.WriteLine("Requesting parallel tool calls...");
        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 1024,
            Messages = [new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" }],
            Tools = tools
        };

        var response = await client.Messages.Create(parameters);

        var toolUses = new List<ToolUseBlock>();
        foreach (var block in response.Content)
        {
            if (block.TryPickToolUse(out var toolUse))
            {
                toolUses.Add(toolUse);
            }
        }
        Console.WriteLine($"\n✓ Claude made {toolUses.Count} tool calls");

        if (toolUses.Count > 1)
        {
            Console.WriteLine("✓ Parallel tool calls detected!");
            foreach (var tool in toolUses)
            {
                Console.WriteLine($"  - {tool.Name}: {tool.Input}");
            }
        }
        else
        {
            Console.WriteLine("✗ No parallel tool calls detected");
        }

        var toolResults = new List<ContentBlockParam>();
        foreach (var toolUse in toolUses)
        {
            string result;
            if (toolUse.Name == "get_weather")
            {
                result = toolUse.Input.ToString()!.Contains("San Francisco")
                    ? "San Francisco: 68°F, partly cloudy"
                    : "New York: 45°F, clear skies";
            }
            else
            {
                result = toolUse.Input.ToString()!.Contains("Los_Angeles")
                    ? "2:30 PM PST"
                    : "5:30 PM EST";
            }

            toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
            {
                ToolUseID = toolUse.ID,
                Content = result,
            }));
        }

        Console.WriteLine("\nGetting final response...");
        var finalParameters = new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_7,
            MaxTokens = 1024,
            Messages = [
                new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" },
                new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
                new() { Role = Role.User, Content = new MessageParamContent(toolResults) }
            ],
            Tools = tools
        };

        var finalResponse = await client.Messages.Create(finalParameters);
        finalResponse.Content[0].TryPickText(out var text);
        Console.WriteLine($"\nClaude's response:\n{text?.Text}");

        Console.WriteLine("\n--- Verification ---");
        Console.WriteLine($"✓ Tool results sent in single user message: {toolResults.Count} results");
        Console.WriteLine("✓ No text before tool results in content array");
        Console.WriteLine("✓ Conversation formatted correctly for future parallel tool use");
    }
}
```

```go Go hidelines={1..15,-11..-1}
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	tools := []anthropic.ToolUnionParam{
		{OfTool: &anthropic.ToolParam{
			Name:        "get_weather",
			Description: anthropic.String("Get the current weather in a given location"),
			InputSchema: anthropic.ToolInputSchemaParam{
				Properties: map[string]any{
					"location": map[string]any{
						"type":        "string",
						"description": "The city and state, e.g. San Francisco, CA",
					},
				},
				Required: []string{"location"},
			},
		}},
		{OfTool: &anthropic.ToolParam{
			Name:        "get_time",
			Description: anthropic.String("Get the current time in a given timezone"),
			InputSchema: anthropic.ToolInputSchemaParam{
				Properties: map[string]any{
					"timezone": map[string]any{
						"type":        "string",
						"description": "The timezone, e.g. America/New_York",
					},
				},
				Required: []string{"timezone"},
			},
		}},
	}

	fmt.Println("Requesting parallel tool calls...")
	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
		},
		Tools: tools,
	})
	if err != nil {
		log.Fatal(err)
	}

	// Find tool use blocks using type switch
	type toolUseInfo struct {
		ID    string
		Name  string
		Input json.RawMessage
	}
	var toolUses []toolUseInfo
	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.ToolUseBlock:
			toolUses = append(toolUses, toolUseInfo{
				ID:    variant.ID,
				Name:  variant.Name,
				Input: variant.Input,
			})
		}
	}

	fmt.Printf("\n✓ Claude made %d tool calls\n", len(toolUses))

	if len(toolUses) > 1 {
		fmt.Println("✓ Parallel tool calls detected!")
		for _, tool := range toolUses {
			fmt.Printf("  - %s: %s\n", tool.Name, string(tool.Input))
		}
	} else {
		fmt.Println("✗ No parallel tool calls detected")
	}

	// Build tool results
	var toolResults []anthropic.ContentBlockParamUnion
	for _, toolUse := range toolUses {
		var result string
		inputStr := string(toolUse.Input)

		if toolUse.Name == "get_weather" {
			if strings.Contains(inputStr, "San Francisco") {
				result = "San Francisco: 68°F, partly cloudy"
			} else {
				result = "New York: 45°F, clear skies"
			}
		} else {
			if strings.Contains(inputStr, "Los_Angeles") {
				result = "2:30 PM PST"
			} else {
				result = "5:30 PM EST"
			}
		}

		toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, result, false))
	}

	// Convert response content to param types for the assistant message
	var contentParams []anthropic.ContentBlockParamUnion
	for _, block := range response.Content {
		contentParams = append(contentParams, block.ToParam())
	}

	fmt.Println("\nGetting final response...")
	finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
			anthropic.NewAssistantMessage(contentParams...),
			anthropic.NewUserMessage(toolResults...),
		},
		Tools: tools,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("\nClaude's response:\n%s\n", finalResponse.Content[0].Text)

	fmt.Println("\n--- Verification ---")
	fmt.Printf("✓ Tool results sent in single user message: %d results\n", len(toolResults))
	fmt.Println("✓ No text before tool results in content array")
	fmt.Println("✓ Conversation formatted correctly for future parallel tool use")
}
```

```java Java hidelines={1..17,-1}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlock;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    Tool weatherTool = Tool.builder()
        .name("get_weather")
        .description("Get the current weather in a given location")
        .inputSchema(InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "location", Map.of(
                    "type", "string",
                    "description", "The city and state, e.g. San Francisco, CA"
                )
            )))
            .putAdditionalProperty("required", JsonValue.from(List.of("location")))
            .build())
        .build();

    Tool timeTool = Tool.builder()
        .name("get_time")
        .description("Get the current time in a given timezone")
        .inputSchema(InputSchema.builder()
            .properties(JsonValue.from(Map.of(
                "timezone", Map.of(
                    "type", "string",
                    "description", "The timezone, e.g. America/New_York"
                )
            )))
            .putAdditionalProperty("required", JsonValue.from(List.of("timezone")))
            .build())
        .build();

    MessageCreateParams params = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .addTool(weatherTool)
        .addTool(timeTool)
        .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
        .build();

    IO.println("Requesting parallel tool calls...");
    Message response = client.messages().create(params);

    List<ToolUseBlock> toolUses = new ArrayList<>();
    for (ContentBlock block : response.content()) {
        if (block.toolUse().isPresent()) {
            toolUses.add(block.toolUse().get());
        }
    }

    IO.println("\n✓ Claude made " + toolUses.size() + " tool calls");

    if (toolUses.size() > 1) {
        IO.println("✓ Parallel tool calls detected!");
        for (ToolUseBlock tool : toolUses) {
            IO.println("  - " + tool.name() + ": " + tool._input());
        }
    } else {
        IO.println("✗ No parallel tool calls detected");
    }

    List<ContentBlockParam> toolResults = new ArrayList<>();
    for (ToolUseBlock toolUse : toolUses) {
        String result;
        if (toolUse.name().equals("get_weather")) {
            String location = toolUse._input().toString();
            result = location.contains("San Francisco")
                ? "San Francisco: 68°F, partly cloudy"
                : "New York: 45°F, clear skies";
        } else {
            String timezone = toolUse._input().toString();
            result = timezone.contains("Los_Angeles")
                ? "2:30 PM PST"
                : "5:30 PM EST";
        }
        toolResults.add(ContentBlockParam.ofToolResult(
            ToolResultBlockParam.builder()
                .toolUseId(toolUse.id())
                .content(result)
                .build()
        ));
    }

    IO.println("\nGetting final response...");
    MessageCreateParams finalParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_OPUS_4_7)
        .maxTokens(1024L)
        .addTool(weatherTool)
        .addTool(timeTool)
        .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
        .addMessage(response)
        .addUserMessageOfBlockParams(toolResults)
        .build();

    Message finalResponse = client.messages().create(finalParams);
    finalResponse.content().stream()
        .flatMap(block -> block.text().stream())
        .forEach(textBlock -> IO.println("\nClaude's response:\n" + textBlock.text()));

    IO.println("\n--- Verification ---");
    IO.println("✓ Tool results sent in single user message: " + toolResults.size() + " results");
    IO.println("✓ No text before tool results in content array");
    IO.println("✓ Conversation formatted correctly for future parallel tool use");
}
```

```php PHP hidelines={1..6}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$tools = [
    [
        'name' => 'get_weather',
        'description' => 'Get the current weather in a given location',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'location' => [
                    'type' => 'string',
                    'description' => 'The city and state, e.g. San Francisco, CA'
                ]
            ],
            'required' => ['location']
        ]
    ],
    [
        'name' => 'get_time',
        'description' => 'Get the current time in a given timezone',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'timezone' => [
                    'type' => 'string',
                    'description' => 'The timezone, e.g. America/New_York'
                ]
            ],
            'required' => ['timezone']
        ]
    ]
];

echo "Requesting parallel tool calls...\n";
$response = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"]
    ],
    model: 'claude-opus-4-7',
    tools: $tools,
);

$toolUses = array_filter($response->content, fn($block) => $block->type === 'tool_use');
echo "\n✓ Claude made " . count($toolUses) . " tool calls\n";

if (count($toolUses) > 1) {
    echo "✓ Parallel tool calls detected!\n";
    foreach ($toolUses as $tool) {
        echo "  - {$tool->name}: " . json_encode($tool->input) . "\n";
    }
} else {
    echo "✗ No parallel tool calls detected\n";
}

$toolResults = [];
foreach ($toolUses as $toolUse) {
    if ($toolUse->name === 'get_weather') {
        $result = str_contains(json_encode($toolUse->input), 'San Francisco')
            ? 'San Francisco: 68°F, partly cloudy'
            : 'New York: 45°F, clear skies';
    } else {
        $result = str_contains(json_encode($toolUse->input), 'Los_Angeles')
            ? '2:30 PM PST'
            : '5:30 PM EST';
    }

    $toolResults[] = [
        'type' => 'tool_result',
        'tool_use_id' => $toolUse->id,
        'content' => $result
    ];
}

echo "\nGetting final response...\n";
$finalResponse = $client->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"],
        ['role' => 'assistant', 'content' => $response->content],
        ['role' => 'user', 'content' => $toolResults]
    ],
    model: 'claude-opus-4-7',
    tools: $tools,
);

echo "\nClaude's response:\n{$finalResponse->content[0]->text}\n";

echo "\n--- Verification ---\n";
echo "✓ Tool results sent in single user message: " . count($toolResults) . " results\n";
echo "✓ No text before tool results in content array\n";
echo "✓ Conversation formatted correctly for future parallel tool use\n";
```

```ruby Ruby
require "anthropic"

client = Anthropic::Client.new

tools = [
  {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA"
        }
      },
      required: ["location"]
    }
  },
  {
    name: "get_time",
    description: "Get the current time in a given timezone",
    input_schema: {
      type: "object",
      properties: {
        timezone: {
          type: "string",
          description: "The timezone, e.g. America/New_York"
        }
      },
      required: ["timezone"]
    }
  }
]

puts "Requesting parallel tool calls..."
response = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" }
  ],
  tools: tools
)

tool_uses = response.content.select { |block| block.type == :tool_use }
puts "\n✓ Claude made #{tool_uses.length} tool calls"

if tool_uses.length > 1
  puts "✓ Parallel tool calls detected!"
  tool_uses.each do |tool|
    puts "  - #{tool.name}: #{tool.input}"
  end
else
  puts "✗ No parallel tool calls detected"
end

tool_results = tool_uses.map do |tool_use|
  result = if tool_use.name == "get_weather"
    location = tool_use.input["location"].to_s
    location.include?("San Francisco") ? "San Francisco: 68°F, partly cloudy" : "New York: 45°F, clear skies"
  else
    timezone = tool_use.input["timezone"].to_s
    timezone.include?("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST"
  end

  {
    type: "tool_result",
    tool_use_id: tool_use.id,
    content: result
  }
end

puts "\nGetting final response..."
final_response = client.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" },
    { role: "assistant", content: response.content },
    { role: "user", content: tool_results }
  ],
  tools: tools
)

puts "\nClaude's response:\n#{final_response.content.first.text}"

puts "\n--- Verification ---"
puts "✓ Tool results sent in single user message: #{tool_results.length} results"
puts "✓ No text before tool results in content array"
puts "✓ Conversation formatted correctly for future parallel tool use"
```
</CodeGroup>

Skrip ini mendemonstrasikan:
- Cara memformat dengan benar panggilan alat paralel dan hasil
- Cara memverifikasi bahwa panggilan paralel sedang dilakukan
- Struktur pesan yang benar yang mendorong penggunaan alat paralel di masa depan
- Kesalahan umum yang harus dihindari (seperti teks sebelum hasil alat)

Jalankan skrip ini untuk menguji implementasi Anda dan memastikan Claude membuat panggilan alat paralel secara efektif.

## Memaksimalkan penggunaan alat paralel

Meskipun model Claude 4 memiliki kemampuan penggunaan alat paralel yang sangat baik secara default, Anda dapat meningkatkan kemungkinan eksekusi alat paralel di semua model dengan prompting yang ditargetkan:

<section title="Prompt sistem untuk penggunaan alat paralel">

Untuk model Claude 4 (Opus 4 (deprecated), dan Sonnet 4 (deprecated)), tambahkan ini ke prompt sistem Anda:
```text
For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
```

Untuk penggunaan alat paralel yang bahkan lebih kuat (direkomendasikan jika default tidak cukup), gunakan:
```text
<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. When running multiple read-only commands like `ls` or `list_dir`, always run all of the commands in parallel. Err on the side of maximizing parallel tool calls rather than running too many tools sequentially.
</use_parallel_tool_calls>
```

</section>
<section title="Prompting pesan pengguna">

Anda juga dapat mendorong penggunaan alat paralel dalam pesan pengguna tertentu:

```text
Sebagai gantinya:
"What's the weather in Paris? Also check London."

Gunakan:
"Check the weather in Paris and London simultaneously."

Atau jadilah eksplisit:
"Please use parallel tool calls to get the weather for Paris, London, and Tokyo at the same time."
```

</section>

## Pemecahan masalah

Jika Claude tidak membuat panggilan alat paralel seperti yang diharapkan, periksa masalah umum ini:

**1. Format hasil alat yang tidak benar**

Masalah paling umum adalah memformat hasil alat dengan tidak benar dalam riwayat percakapan. Ini "mengajarkan" Claude untuk menghindari panggilan paralel.

Khusus untuk penggunaan alat paralel:
- ❌ **Salah**: Mengirim pesan pengguna terpisah untuk setiap hasil alat
- ✅ **Benar**: Semua hasil alat harus berada dalam satu pesan pengguna

```json
// ❌ Ini mengurangi penggunaan alat paralel
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1]},
  {"role": "user", "content": [tool_result_2]}  // Pesan terpisah
]

// ✅ Ini mempertahankan penggunaan alat paralel
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1, tool_result_2]}  // Pesan tunggal
]
```

Lihat [Handle tool calls](/docs/id/agents-and-tools/tool-use/handle-tool-calls) untuk aturan pemformatan lainnya.

**2. Prompting yang lemah**

Prompting default mungkin tidak cukup. Gunakan prompt sistem yang lebih kuat dari bagian [Memaksimalkan penggunaan alat paralel](#memaksimalkan-penggunaan-alat-paralel) di atas.

**3. Mengukur penggunaan alat paralel**

Untuk memverifikasi panggilan alat paralel berfungsi:

```python hidelines={1}
messages = []  # Riwayat percakapan Anda dari objek Message asisten
# Hitung rata-rata alat per pesan yang memanggil alat
tool_call_messages = [
    msg for msg in messages if any(block.type == "tool_use" for block in msg.content)
]
total_tool_calls = sum(
    len([b for b in msg.content if b.type == "tool_use"]) for msg in tool_call_messages
)
avg_tools_per_message = (
    total_tool_calls / len(tool_call_messages) if tool_call_messages else 0.0
)
print(f"Average tools per message: {avg_tools_per_message}")
# Harus > 1.0 jika panggilan paralel berfungsi
```

## Langkah berikutnya

- Untuk alur panggilan alat tunggal dan aturan pemformatan `tool_result`, lihat [Handle tool calls](/docs/id/agents-and-tools/tool-use/handle-tool-calls).
- Untuk abstraksi SDK yang menangani eksekusi paralel secara otomatis, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).
- Untuk alur kerja penggunaan alat lengkap, lihat [Define tools](/docs/id/agents-and-tools/tool-use/define-tools).