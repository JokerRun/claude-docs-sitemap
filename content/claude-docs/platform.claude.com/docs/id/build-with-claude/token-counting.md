---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/token-counting
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 6eca6ae61c31bf68f400be042bc3e20625576fc0fee5eb3e097bdb06330ccf9d
---

# Penghitungan token

Pelajari cara menghitung token dalam pesan sebelum mengirimnya ke Claude untuk membuat keputusan yang tepat tentang prompt dan penggunaan Anda.

---

Penghitungan token memungkinkan Anda menentukan jumlah token dalam pesan sebelum mengirimnya ke Claude, membantu Anda membuat keputusan yang tepat tentang prompt dan penggunaan Anda. Dengan penghitungan token, Anda dapat
- Mengelola batas laju dan biaya secara proaktif
- Membuat keputusan perutean model yang cerdas
- Mengoptimalkan prompt agar memiliki panjang tertentu

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

---

## Cara menghitung token pesan

Titik akhir [penghitungan token](/docs/id/api/messages-count-tokens) menerima daftar input terstruktur yang sama untuk membuat pesan, termasuk dukungan untuk prompt sistem, [alat](/docs/id/agents-and-tools/tool-use/overview), [gambar](/docs/id/build-with-claude/vision), dan [PDF](/docs/id/build-with-claude/pdf-support). Respons berisi jumlah total token input.

<Note>
Jumlah token harus dianggap sebagai **perkiraan**. Dalam beberapa kasus, jumlah token input aktual yang digunakan saat membuat pesan mungkin berbeda dalam jumlah kecil.

Jumlah token mungkin mencakup token yang ditambahkan secara otomatis oleh Anthropic untuk optimasi sistem. **Anda tidak ditagih untuk token yang ditambahkan sistem**. Penagihan hanya mencerminkan konten Anda.
</Note>

### Model yang didukung
Semua [model aktif](/docs/id/about-claude/models/overview) mendukung penghitungan token.

### Hitung token dalam pesan dasar

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-opus-4-6",
      "system": "You are a scientist",
      "messages": [{
        "role": "user",
        "content": "Hello, Claude"
      }]
    }'
```

```bash CLI
ant messages count-tokens \
  --model claude-opus-4-6 \
  --system "You are a scientist" \
  --message '{role: user, content: "Hello, Claude"}'
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-6",
    system="You are a scientist",
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(response.json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.countTokens({
  model: "claude-opus-4-6",
  system: "You are a scientist",
  messages: [
    {
      role: "user",
      content: "Hello, Claude"
    }
  ]
});

console.log(response);
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCountTokensParams
        {
            Model = Model.ClaudeOpus4_6,
            System = "You are a scientist",
            Messages = [new() { Role = Role.User, Content = "Hello, Claude" }]
        };

        var response = await client.Messages.CountTokens(parameters);
        Console.WriteLine(response);
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

	response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
		Model: anthropic.ModelClaudeOpus4_6,
		System: anthropic.MessageCountTokensParamsSystemUnion{
			OfString: anthropic.String("You are a scientist"),
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(response)
}
```

```java Java hidelines={1..2,5..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCountTokensParams;
import com.anthropic.models.messages.MessageTokensCount;
import com.anthropic.models.messages.Model;

public class CountTokensExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCountTokensParams params = MessageCountTokensParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .system("You are a scientist")
      .addUserMessage("Hello, Claude")
      .build();

    MessageTokensCount count = client.messages().countTokens(params);
    System.out.println(count);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->countTokens(
    messages: [
        ['role' => 'user', 'content' => 'Hello, Claude']
    ],
    model: 'claude-opus-4-6',
    system: 'You are a scientist',
);

echo json_encode($response);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.count_tokens(
  model: "claude-opus-4-6",
  system: "You are a scientist",
  messages: [
    { role: "user", content: "Hello, Claude" }
  ]
)

puts response
```
</CodeGroup>

```json Output
{ "input_tokens": 14 }
```

### Hitung token dalam pesan dengan alat

<Note>
Jumlah token [alat server](/docs/id/agents-and-tools/tool-use/server-tools) hanya berlaku untuk panggilan sampling pertama.
</Note>

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-opus-4-6",
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "What'\''s the weather like in San Francisco?"
        }
      ]
    }'
```

```bash CLI
ant messages count-tokens <<'YAML'
model: claude-opus-4-6
tools:
  - name: get_weather
    description: Get the current weather in a given location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      required:
        - location
messages:
  - role: user
    content: What's the weather like in San Francisco?
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-6",
    tools=[
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
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)

print(response.json())
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.countTokens({
  model: "claude-opus-4-6",
  tools: [
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
    }
  ],
  messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
});

console.log(response);
```

```csharp C#
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCountTokensParams
        {
            Model = Model.ClaudeOpus4_6,
            Tools =
            [
                new MessageCountTokensTool(new Tool()
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
            ],
            Messages = [new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }]
        };

        var count = await client.Messages.CountTokens(parameters);
        Console.WriteLine(count);
    }
}
```

```go Go hidelines={1..14,-1}
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

	response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
		Model: anthropic.ModelClaudeOpus4_6,
		Tools: []anthropic.MessageCountTokensToolUnionParam{
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
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	jsonData, _ := json.MarshalIndent(response, "", "  ")
	fmt.Println(string(jsonData))
}
```

```java Java hidelines={1..3,6..14,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.MessageCountTokensParams;
import com.anthropic.models.messages.MessageTokensCount;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.List;
import java.util.Map;

public class CountTokensWithToolsExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    InputSchema schema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of(
            "location",
            Map.of(
              "type",
              "string",
              "description",
              "The city and state, e.g. San Francisco, CA"
            )
          )
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

    MessageCountTokensParams params = MessageCountTokensParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .addTool(
        Tool.builder()
          .name("get_weather")
          .description("Get the current weather in a given location")
          .inputSchema(schema)
          .build()
      )
      .addUserMessage("What's the weather like in San Francisco?")
      .build();

    MessageTokensCount count = client.messages().countTokens(params);
    System.out.println(count);
  }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->countTokens(
    messages: [
        ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
    ],
    model: 'claude-opus-4-6',
    tools: [
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
        ]
    ],
);

echo json_encode($response, JSON_PRETTY_PRINT);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.count_tokens(
  model: "claude-opus-4-6",
  tools: [
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
    }
  ],
  messages: [
    { role: "user", content: "What's the weather like in San Francisco?" }
  ]
)

puts response
```
</CodeGroup>

```json Output
{ "input_tokens": 403 }
```

### Hitung token dalam pesan dengan gambar

<CodeGroup>
```bash Shell
#!/bin/sh

IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
IMAGE_MEDIA_TYPE="image/jpeg"
IMAGE_BASE64=$(curl -s "$IMAGE_URL" | base64 | tr -d '\n')

curl https://api.anthropic.com/v1/messages/count_tokens \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data @- <<EOF
{
    "model": "claude-opus-4-6",
    "messages": [
        {"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "$IMAGE_MEDIA_TYPE",
                "data": "$IMAGE_BASE64"
            }},
            {"type": "text", "text": "Describe this image"}
        ]}
    ]
}
EOF
```

```bash CLI nocheck
IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
curl -s "$IMAGE_URL" -o ./ant.jpg

ant messages count-tokens <<'YAML'
model: claude-opus-4-6
messages:
  - role: user
    content:
      - type: image
        source:
          type: base64
          media_type: image/jpeg
          data: "@./ant.jpg"
      - type: text
        text: Describe this image
YAML
```

```python Python nocheck hidelines={1}
import anthropic
import base64
import httpx

image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-6",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "Describe this image"},
            ],
        }
    ],
)
print(response.json())
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const image_url =
  "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
const image_media_type = "image/jpeg";
const image_array_buffer = await (await fetch(image_url)).arrayBuffer();
const image_data = Buffer.from(image_array_buffer).toString("base64");

const response = await anthropic.messages.countTokens({
  model: "claude-opus-4-6",
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: image_media_type,
            data: image_data
          }
        },
        {
          type: "text",
          text: "Describe this image"
        }
      ]
    }
  ]
});
console.log(response);
```

```csharp C# nocheck
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        string imageUrl = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";

        using HttpClient httpClient = new();
        byte[] imageBytes = await httpClient.GetByteArrayAsync(imageUrl);
        string imageData = Convert.ToBase64String(imageBytes);

        var parameters = new MessageCountTokensParams
        {
            Model = Model.ClaudeOpus4_6,
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new ImageBlockParam(
                            new ImageBlockParamSource(new Base64ImageSource()
                            {
                                Data = imageData,
                                MediaType = MediaType.ImageJpeg,
                            })
                        )),
                        new ContentBlockParam(new TextBlockParam("Describe this image")),
                    }),
                }
            ]
        };

        var count = await client.Messages.CountTokens(parameters);
        Console.WriteLine(count);
    }
}
```

```go Go nocheck hidelines={1..14,-1}
package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	imageURL := "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"

	req, err := http.NewRequest("GET", imageURL, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("User-Agent", "AnthropicDocsBot/1.0")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	imageBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	imageData := base64.StdEncoding.EncodeToString(imageBytes)

	client := anthropic.NewClient()

	response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
		Model: anthropic.ModelClaudeOpus4_6,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(
				anthropic.NewImageBlockBase64("image/jpeg", imageData),
				anthropic.NewTextBlock("Describe this image"),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..2,4..5,8..19,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Base64ImageSource;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.ImageBlockParam;
import com.anthropic.models.messages.MessageCountTokensParams;
import com.anthropic.models.messages.MessageTokensCount;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Base64;
import java.util.List;

public class CountTokensImageExample {

  public static void main(String[] args) throws Exception {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    String imageUrl =
      "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
    String imageMediaType = "image/jpeg";

    HttpClient httpClient = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder().uri(URI.create(imageUrl)).build();
    byte[] imageBytes = httpClient
      .send(request, HttpResponse.BodyHandlers.ofByteArray())
      .body();
    String imageBase64 = Base64.getEncoder().encodeToString(imageBytes);

    ContentBlockParam imageBlock = ContentBlockParam.ofImage(
      ImageBlockParam.builder()
        .source(
          Base64ImageSource.builder()
            .mediaType(Base64ImageSource.MediaType.IMAGE_JPEG)
            .data(imageBase64)
            .build()
        )
        .build()
    );

    ContentBlockParam textBlock = ContentBlockParam.ofText(
      TextBlockParam.builder().text("Describe this image").build()
    );

    MessageCountTokensParams params = MessageCountTokensParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .addUserMessageOfBlockParams(List.of(imageBlock, textBlock))
      .build();

    MessageTokensCount count = client.messages().countTokens(params);
    System.out.println(count);
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$imageUrl = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
$imageMediaType = "image/jpeg";
$imageData = base64_encode(file_get_contents($imageUrl));

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->countTokens(
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'image',
                    'source' => [
                        'type' => 'base64',
                        'media_type' => $imageMediaType,
                        'data' => $imageData
                    ]
                ],
                ['type' => 'text', 'text' => 'Describe this image']
            ]
        ]
    ],
    model: 'claude-opus-4-6',
);
print_r($response);
```

```ruby Ruby nocheck hidelines={1}
require "anthropic"
require "base64"
require "net/http"

image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"

uri = URI(image_url)
image_data = Base64.strict_encode64(Net::HTTP.get(uri))

client = Anthropic::Client.new

response = client.messages.count_tokens(
  model: "claude-opus-4-6",
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: image_media_type,
            data: image_data
          }
        },
        { type: "text", text: "Describe this image" }
      ]
    }
  ]
)
puts response
```
</CodeGroup>

```json Output
{ "input_tokens": 1551 }
```

### Hitung token dalam pesan dengan pemikiran yang diperluas

<Note>
Lihat [bagaimana jendela konteks dihitung dengan pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking#how-context-window-is-calculated-with-extended-thinking) untuk detail lebih lanjut
- Blok pemikiran dari giliran asisten **sebelumnya** diabaikan dan **tidak** dihitung terhadap token input Anda
- Pemikiran giliran asisten **saat ini** **dihitung** terhadap token input Anda
</Note>

<CodeGroup>

```bash Shell nocheck
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-sonnet-4-6",
      "thinking": {
        "type": "enabled",
        "budget_tokens": 16000
      },
      "messages": [
        {
          "role": "user",
          "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "thinking",
              "thinking": "This is a nice number theory question. Lets think about it step by step...",
              "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
            },
            {
              "type": "text",
              "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
            }
          ]
        },
        {
          "role": "user",
          "content": "Can you write a formal proof?"
        }
      ]
    }'
```

```bash CLI nocheck
ant messages count-tokens <<'YAML'
model: claude-sonnet-4-6
thinking:
  type: enabled
  budget_tokens: 16000
messages:
  - role: user
    content: Are there an infinite number of prime numbers such that n mod 4 == 3?
  - role: assistant
    content:
      - type: thinking
        thinking: >-
          This is a nice number theory question. Lets think about it step by step...
        signature: >-
          EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...
      - type: text
        text: Yes, there are infinitely many prime numbers p such that p mod 4 = 3...
  - role: user
    content: Can you write a formal proof?
YAML
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    thinking={"type": "enabled", "budget_tokens": 16000},
    messages=[
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?",
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "This is a nice number theory question. Let's think about it step by step...",
                    "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
                },
                {
                    "type": "text",
                    "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3...",
                },
            ],
        },
        {"role": "user", "content": "Can you write a formal proof?"},
    ],
)

print(response.json())
```

```typescript TypeScript nocheck hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.countTokens({
  model: "claude-sonnet-4-6",
  thinking: {
    type: "enabled",
    budget_tokens: 16000
  },
  messages: [
    {
      role: "user",
      content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "thinking",
          thinking:
            "This is a nice number theory question. Let's think about it step by step...",
          signature:
            "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
        },
        {
          type: "text",
          text: "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
        }
      ]
    },
    {
      role: "user",
      content: "Can you write a formal proof?"
    }
  ]
});

console.log(response);
```

```csharp C# nocheck
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Anthropic;
using Anthropic.Models.Messages;

public class Program
{
    public static async Task Main(string[] args)
    {
        AnthropicClient client = new()
        {
            ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
        };

        var parameters = new MessageCountTokensParams
        {
            Model = Model.ClaudeSonnet4_6,
            Thinking = new ThinkingConfigEnabled(budgetTokens: 16000),
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = "Are there an infinite number of prime numbers such that n mod 4 == 3?"
                },
                new()
                {
                    Role = Role.Assistant,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new ThinkingBlockParam()
                        {
                            Thinking = "This is a nice number theory question. Let's think about it step by step...",
                            Signature = "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
                        }),
                        new ContentBlockParam(new TextBlockParam("Yes, there are infinitely many prime numbers p such that p mod 4 = 3...")),
                    }),
                },
                new()
                {
                    Role = Role.User,
                    Content = "Can you write a formal proof?"
                }
            ]
        };

        var response = await client.Messages.CountTokens(parameters);
        Console.WriteLine(response);
    }
}
```

```go Go nocheck hidelines={1..13,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	thinkingBlock := anthropic.NewThinkingBlock(
		"EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
		"This is a nice number theory question. Let's think about it step by step...",
	)

	textBlock := anthropic.NewTextBlock(
		"Yes, there are infinitely many prime numbers p such that p mod 4 = 3...",
	)

	response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
		Model:    anthropic.Model("claude-sonnet-4-6"),
		Thinking: anthropic.ThinkingConfigParamOfEnabled(16000),
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Are there an infinite number of prime numbers such that n mod 4 == 3?")),
			anthropic.NewAssistantMessage(thinkingBlock, textBlock),
			anthropic.NewUserMessage(anthropic.NewTextBlock("Can you write a formal proof?")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%+v\n", response)
}
```

```java Java nocheck hidelines={1..3,6..7,9..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.MessageCountTokensParams;
import com.anthropic.models.messages.MessageTokensCount;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.ThinkingBlockParam;
import java.util.List;

public class CountTokensThinkingExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    List<ContentBlockParam> assistantBlocks = List.of(
      ContentBlockParam.ofThinking(
        ThinkingBlockParam.builder()
          .thinking(
            "This is a nice number theory question. Let's think about it step by step..."
          )
          .signature(
            "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
          )
          .build()
      ),
      ContentBlockParam.ofText(
        TextBlockParam.builder()
          .text("Yes, there are infinitely many prime numbers p such that p mod 4 = 3...")
          .build()
      )
    );

    MessageCountTokensParams params = MessageCountTokensParams.builder()
      .model(Model.CLAUDE_SONNET_4_6)
      .enabledThinking(16000)
      .addUserMessage("Are there an infinite number of prime numbers such that n mod 4 == 3?")
      .addAssistantMessageOfBlockParams(assistantBlocks)
      .addUserMessage("Can you write a formal proof?")
      .build();

    MessageTokensCount count = client.messages().countTokens(params);
    System.out.println(count);
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->messages->countTokens(
    messages: [
        [
            'role' => 'user',
            'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?'
        ],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'thinking',
                    'thinking' => 'This is a nice number theory question. Let\'s think about it step by step...',
                    'signature' => 'EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...'
                ],
                [
                    'type' => 'text',
                    'text' => 'Yes, there are infinitely many prime numbers p such that p mod 4 = 3...'
                ]
            ]
        ],
        [
            'role' => 'user',
            'content' => 'Can you write a formal proof?'
        ]
    ],
    model: 'claude-sonnet-4-6',
    thinking: [
        'type' => 'enabled',
        'budget_tokens' => 16000
    ],
);

echo json_encode($response);
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.messages.count_tokens(
  model: "claude-sonnet-4-6",
  thinking: {
    type: "enabled",
    budget_tokens: 16000
  },
  messages: [
    {
      role: "user",
      content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "thinking",
          thinking: "This is a nice number theory question. Let's think about it step by step...",
          signature: "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
        },
        {
          type: "text",
          text: "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
        }
      ]
    },
    {
      role: "user",
      content: "Can you write a formal proof?"
    }
  ]
)

puts response
```
</CodeGroup>

```json Output
{ "input_tokens": 88 }
```

### Hitung token dalam pesan dengan PDF

<Note>
Penghitungan token mendukung PDF dengan [batasan](/docs/id/build-with-claude/pdf-support#pdf-support-limitations) yang sama seperti Messages API.
</Note>

<CodeGroup>
```bash Shell hidelines={1..3}
PDF_URL="https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
PDF_BASE64=$(curl -s "$PDF_URL" | base64 | tr -d '\n')

curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data @- <<EOF
{
  "model": "claude-opus-4-6",
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "$PDF_BASE64"
        }
      },
      {
        "type": "text",
        "text": "Please summarize this document."
      }
    ]
  }]
}
EOF
```

```bash CLI hidelines={1..3}
PDF_URL="https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
curl -s "$PDF_URL" -o document.pdf

ant messages count-tokens <<'YAML'
model: claude-opus-4-6
messages:
  - role: user
    content:
      - type: document
        source:
          type: base64
          media_type: application/pdf
          data: "@./document.pdf"
      - type: text
        text: Please summarize this document.
YAML
```

```python Python nocheck
import base64
import anthropic

client = anthropic.Anthropic()

with open("document.pdf", "rb") as pdf_file:
    pdf_base64 = base64.standard_b64encode(pdf_file.read()).decode("utf-8")

response = client.messages.count_tokens(
    model="claude-opus-4-6",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64,
                    },
                },
                {"type": "text", "text": "Please summarize this document."},
            ],
        }
    ],
)

print(response.json())
```

```typescript TypeScript nocheck hidelines={1}
import Anthropic from "@anthropic-ai/sdk";
import { readFile } from "fs/promises";

const client = new Anthropic();

const pdfBase64 = await readFile("document.pdf", { encoding: "base64" });

const response = await client.messages.countTokens({
  model: "claude-opus-4-6",
  messages: [
    {
      role: "user",
      content: [
        {
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: pdfBase64
          }
        },
        {
          type: "text",
          text: "Please summarize this document."
        }
      ]
    }
  ]
});

console.log(response);
```

```csharp C# nocheck
using System;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        byte[] pdfBytes = await File.ReadAllBytesAsync("document.pdf");
        string pdfBase64 = Convert.ToBase64String(pdfBytes);

        var parameters = new MessageCountTokensParams
        {
            Model = Model.ClaudeOpus4_6,
            Messages =
            [
                new()
                {
                    Role = Role.User,
                    Content = new MessageParamContent(new List<ContentBlockParam>
                    {
                        new ContentBlockParam(new DocumentBlockParam(
                            new DocumentBlockParamSource(new Base64PdfSource()
                            {
                                Data = pdfBase64,
                                MediaType = MediaType.ApplicationPdf,
                            })
                        )),
                        new ContentBlockParam(new TextBlockParam("Please summarize this document.")),
                    }),
                }
            ]
        };

        var count = await client.Messages.CountTokens(parameters);
        Console.WriteLine(count);
    }
}
```

```go Go nocheck hidelines={1..15,-1}
package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	pdfBytes, err := os.ReadFile("document.pdf")
	if err != nil {
		log.Fatal(err)
	}
	pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

	response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
		Model: anthropic.ModelClaudeOpus4_6,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(
				anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
					Data: pdfBase64,
				}),
				anthropic.NewTextBlock("Please summarize this document."),
			),
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..2,4,8..17,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Base64PdfSource;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.DocumentBlockParam;
import com.anthropic.models.messages.MessageCountTokensParams;
import com.anthropic.models.messages.MessageTokensCount;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;
import java.util.List;

public class CountTokensPdfExample {

  public static void main(String[] args) throws Exception {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    byte[] fileBytes = Files.readAllBytes(Path.of("document.pdf"));
    String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

    ContentBlockParam documentBlock = ContentBlockParam.ofDocument(
      DocumentBlockParam.builder()
        .source(
          Base64PdfSource.builder()
            .mediaType(Base64PdfSource.MediaType.APPLICATION_PDF)
            .data(pdfBase64)
            .build()
        )
        .build()
    );

    ContentBlockParam textBlock = ContentBlockParam.ofText(
      TextBlockParam.builder().text("Please summarize this document.").build()
    );

    MessageCountTokensParams params = MessageCountTokensParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .addUserMessageOfBlockParams(List.of(documentBlock, textBlock))
      .build();

    MessageTokensCount count = client.messages().countTokens(params);
    System.out.println(count);
  }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$pdfBase64 = base64_encode(file_get_contents("document.pdf"));

$response = $client->messages->countTokens(
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'document',
                    'source' => [
                        'type' => 'base64',
                        'media_type' => 'application/pdf',
                        'data' => $pdfBase64
                    ]
                ],
                [
                    'type' => 'text',
                    'text' => 'Please summarize this document.'
                ]
            ]
        ]
    ],
    model: 'claude-opus-4-6',
);

echo json_encode($response);
```

```ruby Ruby nocheck hidelines={1}
require "anthropic"
require "base64"

client = Anthropic::Client.new

pdf_base64 = Base64.strict_encode64(File.binread("document.pdf"))

response = client.messages.count_tokens(
  model: "claude-opus-4-6",
  messages: [
    {
      role: "user",
      content: [
        {
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: pdf_base64
          }
        },
        {
          type: "text",
          text: "Please summarize this document."
        }
      ]
    }
  ]
)

puts response
```
</CodeGroup>

```json Output
{ "input_tokens": 2188 }
```

---

## Harga dan batas laju

Penghitungan token **gratis digunakan** tetapi tunduk pada batas laju permintaan per menit berdasarkan [tingkat penggunaan](/docs/id/api/rate-limits#rate-limits) Anda. Jika Anda memerlukan batas yang lebih tinggi, hubungi penjualan melalui [Claude Console](/settings/limits).

| Tingkat penggunaan | Permintaan per menit (RPM) |
|------------|---------------------------|
| 1          | 100                       |
| 2          | 2.000                     |
| 3          | 4.000                     |
| 4          | 8.000                     |

<Note>
  Penghitungan token dan pembuatan pesan memiliki batas laju yang terpisah dan independen. Penggunaan satu tidak dihitung terhadap batas yang lain.
</Note>

---
## FAQ

  <section title="Apakah penghitungan token menggunakan prompt caching?">

    Tidak, penghitungan token memberikan perkiraan tanpa menggunakan logika caching. Meskipun Anda dapat memberikan blok `cache_control` dalam permintaan penghitungan token Anda, prompt caching hanya terjadi selama pembuatan pesan aktual.
  
</section>